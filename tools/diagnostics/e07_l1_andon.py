"""E07 — evidence for the L1 back-facing ANDON. Diagnostic only; writes no atlas.

The halt: 48.67% of surface-aware lookups on C1 take colour from a texel whose normal
opposes the target's. The spec anticipated the reading being ambiguous — "a crevice's
opposing wall is a plausible source and a strictly better prior than whatever island the
packer placed next door; the far side of a thin plate may not be" — and required a halt
rather than a silent hemisphere restriction.

This reports what an advisor needs to tell those two cases apart, and prices the variant
it must NOT apply:

  * source distance split by how much the source normal agrees
  * the same-hemisphere alternative: for every lookup, the nearest painted texel whose
    normal agrees at all (n.n' > 0), and what that costs in distance
  * how much of the back-facing class sits closer than the local plate is thick

  e07_l1_andon.py --prep DIR --state DIR [--k 64] [--out-json j.json]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy.spatial import cKDTree

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--state", required=True)
ap.add_argument("--k", type=int, default=64, help="neighbours searched for an agreeing normal")
ap.add_argument("--edge", type=float, default=0.00290, help="median triangle edge")
ap.add_argument("--out-json")
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
holes = np.asarray(Image.open(os.path.join(args.state, "holes.png")).convert("L"),
                   dtype=np.float32) / 255.0 > 0.5
lo = np.array(meta["lo"]); hi = np.array(meta["hi"])
P = ((np.load(os.path.join(args.prep, "pos.npy")).astype(np.float64) * (hi - lo) + lo)
     / meta["maxabs"] * 0.5).reshape(-1, 3)
N = np.load(os.path.join(args.prep, "nor.npy")).astype(np.float64) * 2.0 - 1.0
N /= np.linalg.norm(N, axis=-1, keepdims=True) + 1e-12
N = N.reshape(-1, 3)

src_i = np.flatnonzero((valid & ~holes).reshape(-1))
tgt_i = np.flatnonzero((valid & holes).reshape(-1))
E = args.edge
out = {"lookups": int(len(tgt_i)), "sources": int(len(src_i)), "edge": E}
print(f"[andon] {len(tgt_i):,} hole texels against {len(src_i):,} painted", flush=True)

tree = cKDTree(P[src_i])
d1, j1 = tree.query(P[tgt_i], k=1, workers=-1)
dot1 = np.einsum("ij,ij->i", N[tgt_i], N[src_i[j1]])

FRONT, OBLIQUE, BACK = dot1 > 0.5, (dot1 <= 0.5) & (dot1 >= 0.0), dot1 < 0.0
print(f"\n[andon] nearest painted texel, by how the source normal agrees:")
for nm, sel in (("agrees  >60deg (n.n'>0.5)", FRONT),
                ("oblique  0..60deg", OBLIQUE),
                ("BACK-FACING (n.n'<0)", BACK)):
    if not sel.any():
        continue
    d = d1[sel]
    out[f"class_{nm.split()[0]}"] = {
        "pct": round(float(sel.mean() * 100), 2),
        "dist_median": round(float(np.median(d)), 6),
        "dist_p95": round(float(np.percentile(d, 95)), 6)}
    print(f"[andon]   {nm:<26s} {sel.mean()*100:5.2f}%   distance median "
          f"{np.median(d):.5f} ({np.median(d)/E:5.2f} edges)  p95 {np.percentile(d,95):.5f}")

# Is the back-facing class a THIN PLATE (source closer than one triangle) or a real
# reach across a gap? This is the discriminator between the spec's two readings.
if BACK.any():
    db = d1[BACK]
    for t, lab in ((1.0, "1 edge"), (2.0, "2 edges"), (5.0, "5 edges")):
        out[f"back_within_{lab.replace(' ','')}"] = round(float((db < t * E).mean() * 100), 2)
    print(f"[andon]   of the BACK-FACING class, source lies within "
          f"1 edge {(db<E).mean()*100:.1f}%   2 edges {(db<2*E).mean()*100:.1f}%   "
          f"5 edges {(db<5*E).mean()*100:.1f}%")

# The variant, PRICED not applied: nearest painted texel whose normal agrees at all.
print(f"\n[andon] pricing the same-hemisphere variant (NOT applied, k={args.k}):", flush=True)
dk, jk = tree.query(P[tgt_i], k=args.k, workers=-1)
agree = np.einsum("ijk,ik->ij", N[src_i[jk]], N[tgt_i]) > 0.0
first = np.argmax(agree, axis=1)
found = agree.any(axis=1)
d2 = np.where(found, dk[np.arange(len(first)), first], np.inf)
out["hemi_unresolved_pct"] = round(float((~found).mean() * 100), 3)
ok = found
out["hemi_dist_median"] = round(float(np.median(d2[ok])), 6)
out["hemi_dist_p95"] = round(float(np.percentile(d2[ok], 95)), 6)
out["hemi_cost_x_median"] = round(float(np.median(d2[ok]) / max(np.median(d1), 1e-12)), 2)
print(f"[andon]   resolvable within k: {found.mean()*100:.3f}%  "
      f"(unresolved {int((~found).sum()):,})")
print(f"[andon]   distance median {np.median(d2[ok]):.5f} "
      f"({np.median(d2[ok])/E:.2f} edges)  p95 {np.percentile(d2[ok],95):.5f}")
print(f"[andon]   vs unrestricted median {np.median(d1):.5f} -> costs "
      f"{np.median(d2[ok])/max(np.median(d1),1e-12):.2f}x in distance")
chg = ok & (jk[np.arange(len(first)), first] != j1)
out["hemi_changes_pct"] = round(float(chg.mean() * 100), 2)
print(f"[andon]   would change the source for {chg.mean()*100:.2f}% of lookups")
if chg.any():
    print(f"[andon]   for those, distance {np.median(d1[chg]):.5f} -> "
          f"{np.median(d2[chg]):.5f} ({np.median(d2[chg])/max(np.median(d1[chg]),1e-12):.2f}x)")
# both source distances stay far below the atlas flood's 0.17733 median (E07 Gate 0)
out["atlas_flood_median_reference"] = 0.17733
print(f"[andon]   reference: the SHIPPED atlas flood sources from a median 0.17733 "
      f"({0.17733/E:.0f} edges)")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[andon] wrote {args.out_json}")
