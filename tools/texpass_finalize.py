"""TEXTURE-SPACE PASS — finalize: fill the residual holes after the brush loop.

Remaining holes after the brush loop are undersides, crevices and the blade flank
(excluded from diffusion BY POLICY — thin hard-surface props take dilated projected
colour, never invented content).

Two fills, selected by --surface-aware:

  DEFAULT (E02..E06 behaviour, kept so those arms reproduce byte-for-byte)
    Iterative 4-neighbour average in ATLAS space from styled texels, then mean
    fallback + gutter dilation for mips.
    ! The docstring here used to claim this was "valid-island-constrained". It is
      not, and never was: the write predicate is `~grown & (cnt > 0)` with no
      `& valid`, so gutter texels are filled on the first iteration and become
      SOURCES on the second. E07 Gate 0 measured what that costs on E06's C1 —
      74.9% of dilated texels take colour from another island, from a median
      0.177 away on a figure ~1.0 tall.

  --surface-aware (E07 arm L1)
    Every hole texel takes the colour of its nearest painted texel IN 3D, by
    cKDTree over the baked positions. The atlas is an index; pos.npy is the
    neighbourhood. Measured on the same C1 state, the median source distance falls
    to 0.00253 — below one triangle edge, a 70x shrink. The 16-step gutter
    dilation still runs afterwards, into INVALID texels only, for mips; it cannot
    walk back into the surface because every valid texel already has colour.

  texpass_finalize.py --state DIR --prep DIR --out atlas_final.png [--surface-aware]

Reads --state, writes only --out: it cannot mutate the arm it is replayed from.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--state", required=True)
ap.add_argument("--prep", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--surface-aware", action="store_true",
                help="E07 L1: nearest painted texel in 3D instead of an atlas-space flood")
ap.add_argument("--back-facing-limit", type=float, default=0.20,
                help="ANDON: halt if more than this share of lookups take colour from a "
                     "back-facing source (n.n' < 0). This is a HALT, not a filter — a "
                     "hemisphere restriction is a variant to be measured, not a fix to "
                     "be assumed.")
ap.add_argument("--json", help="write the lookup measurements here")
args = ap.parse_args()

atlas = np.asarray(Image.open(os.path.join(args.state, "atlas.png")).convert("RGB"),
                   dtype=np.float32) / 255.0
holes = np.asarray(Image.open(os.path.join(args.state, "holes.png")).convert("L"),
                   dtype=np.float32) / 255.0 > 0.5
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
RES = atlas.shape[0]
have = valid & ~holes
need = valid & holes
img = atlas.copy()
print(f"[finalize] filling {int(need.sum()):,} hole texels "
      f"({'surface-aware' if args.surface_aware else 'atlas-space flood'})", flush=True)
rep = {"mode": "surface_aware" if args.surface_aware else "atlas_flood",
       "hole_texels": int(need.sum()), "painted_texels": int(have.sum())}

if args.surface_aware:
    from scipy.spatial import cKDTree
    assert have.any(), "ANDON: nothing is painted — nowhere to source colour from"
    meta = json.load(open(os.path.join(args.prep, "meta.json")))
    lo = np.array(meta["lo"])
    hi = np.array(meta["hi"])
    P = (np.load(os.path.join(args.prep, "pos.npy")).astype(np.float64)
         * (hi - lo) + lo) / meta["maxabs"] * 0.5
    N = np.load(os.path.join(args.prep, "nor.npy")).astype(np.float64) * 2.0 - 1.0
    N /= np.linalg.norm(N, axis=-1, keepdims=True) + 1e-12
    src_i = np.flatnonzero(have.reshape(-1))
    tgt_i = np.flatnonzero(need.reshape(-1))
    Pf, Nf = P.reshape(-1, 3), N.reshape(-1, 3)
    tree = cKDTree(Pf[src_i])
    dist, j = tree.query(Pf[tgt_i], k=1, workers=-1)
    pick = src_i[j]
    img.reshape(-1, 3)[tgt_i] = atlas.reshape(-1, 3)[pick]

    # Report the operation's FAILURE mode, not its success mode. A crevice's opposing
    # wall is a plausible source; the far side of a thin plate may not be.
    dot = np.einsum("ij,ij->i", Nf[tgt_i], Nf[pick])
    edge = 0.00290                       # median triangle edge, this mesh, E07 Gate 0
    over60 = float((dot < 0.5).mean())
    back = float((dot < 0.0).mean())
    rep.update(
        dist_median=round(float(np.median(dist)), 6),
        dist_p95=round(float(np.percentile(dist, 95)), 6),
        dist_max=round(float(dist.max()), 6),
        dist_gt_5edge_pct=round(float((dist > 5 * edge).mean() * 100), 2),
        dist_gt_20edge_pct=round(float((dist > 20 * edge).mean() * 100), 2),
        normal_disagree_gt60_pct=round(over60 * 100, 2),
        normal_back_facing_pct=round(back * 100, 2))
    print(f"[finalize]   source distance  median {np.median(dist):.5f}  "
          f"p95 {np.percentile(dist,95):.5f}  max {dist.max():.5f}  "
          f"(median edge {edge})")
    print(f"[finalize]   beyond  5 edges {(dist>5*edge).mean()*100:5.2f}%   "
          f"beyond 20 edges {(dist>20*edge).mean()*100:5.2f}%")
    print(f"[finalize]   source normal disagrees >60deg {over60*100:5.2f}%   "
          f"BACK-FACING (n.n'<0) {back*100:5.2f}%")
    assert back <= args.back_facing_limit, (
        f"ANDON: {back*100:.2f}% of lookups source from a back-facing normal, over the "
        f"{args.back_facing_limit*100:.0f}% limit. Report it; do not add a hemisphere "
        f"restriction here — that is a variant to be measured.")
    grown = valid.copy()                 # every valid texel now carries colour
    STEPS = 16                           # gutter only, for mips
else:
    grown = have.copy()
    STEPS = 96

for step in range(STEPS):
    todo = valid & ~grown
    if not todo.any() and step >= 16:    # extra 16 = gutter dilation beyond islands
        break
    acc = np.zeros((RES, RES, 3), dtype=np.float32)
    cnt = np.zeros((RES, RES), dtype=np.float32)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb_v = np.roll(grown, (dy, dx), axis=(0, 1))
        acc += np.roll(img, (dy, dx), axis=(0, 1)) * nb_v[..., None]
        cnt += nb_v
    fill = ~grown & (cnt > 0)
    img[fill] = acc[fill] / cnt[fill][..., None]
    grown |= fill
left = int((valid & ~grown).sum())
if left:
    img[valid & ~grown] = img[have].mean(axis=0)
rep["mean_fallback"] = left
print(f"[finalize] done, {left:,} texels took mean fallback", flush=True)
var = float(img[valid].var())
rep["atlas_variance"] = round(var, 5)
assert var > 0.001, "ANDON: final atlas uniform"
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
Image.fromarray((img * 255).round().astype(np.uint8)).save(args.out)
if args.json:
    json.dump(rep, open(args.json, "w"), indent=1)
print(f"[finalize] wrote {args.out}  var {var:.5f}", flush=True)
