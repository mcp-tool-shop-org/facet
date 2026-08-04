"""How much surface does the twin's KEY exclude, and does stage 1 paint any of it?

E08 Amendment 27 §9a, generalised from two views to N. The largest single region of mesh
surface that a twin's keyed figure mask does not cover is the greatsword blade — steel at
C* 1.6-2.8 against a grey studio backdrop, sitting on the 0.06 key threshold. Outside `fm`,
`dist_in` is 0 by definition and the edge test needs several px, so every candidate texel
there is rejected: the blade reaches stage 2 as a hole for the brush to invent into, which is
what E07 Gate 0 recorded as "the blade carries no reference at all."

Reads a `project_twins --diag-npz` dump, so it measures the run rather than a re-derivation.

  blade_band.py --diag diag_8cam.npz [--out-json j]
"""
import argparse
import json
import os

import numpy as np
from scipy.ndimage import label

ap = argparse.ArgumentParser()
ap.add_argument("--diag", required=True)
ap.add_argument("--out-json")
args = ap.parse_args()

Z = np.load(args.diag, allow_pickle=False)
views = [str(x) for x in Z["__views__"]]
print(f"trust_intersect: {bool(Z['__trust_intersect__'])}")
print(f"{'view':>9} {'silhouette':>11} {'uncovered':>10} {'%surf':>6} {'comps':>6} "
      f"{'largest':>8} {'bbox h x w':>12} {'cands':>8} {'accepted':>9} {'%acc':>6}")
rows = {}
tot_c = tot_a = 0
for nm in views:
    mesh = Z[f"{nm}/mesh_fm"]
    twin = Z[f"{nm}/twin_fm"]
    unc = mesh & ~twin
    lab, n = label(unc)
    if not n:
        continue
    sz = np.bincount(lab.ravel())[1:]
    bi = int(np.argmax(sz)) + 1
    band = lab == bi
    ys, xs = np.where(band)
    px, py = Z[f"{nm}/px"], Z[f"{nm}/py"]
    acc = Z[f"{nm}/accepted"]
    pyi = np.clip(py.round().astype(int), 0, mesh.shape[0] - 1)
    pxi = np.clip(px.round().astype(int), 0, mesh.shape[1] - 1)
    inb = band[pyi, pxi]
    nc, na = int(inb.sum()), int((inb & acc).sum())
    tot_c += nc
    tot_a += na
    rows[nm] = {"silhouette_px": int(mesh.sum()), "uncovered_px": int(unc.sum()),
                "pct_of_surface": round(int(unc.sum()) / int(mesh.sum()) * 100, 2),
                "n_components": int(n), "largest_band_px": int(band.sum()),
                "band_bbox_h": int(ys.max() - ys.min()),
                "band_bbox_w": int(xs.max() - xs.min()),
                "candidates_in_band": nc, "accepted_in_band": na,
                "pct_accepted": round(na / max(nc, 1) * 100, 2)}
    print(f"{nm:>9} {int(mesh.sum()):>11,} {int(unc.sum()):>10,} "
          f"{int(unc.sum())/int(mesh.sum())*100:>5.2f}% {n:>6} {int(band.sum()):>8,} "
          f"{ys.max()-ys.min():>5}x{xs.max()-xs.min():<6} {nc:>8,} {na:>9,} "
          f"{na/max(nc,1)*100:>5.2f}%")

print(f"\n  summed over views (texels counted once per view they are candidates in): "
      f"{tot_c:,} candidates, {tot_a:,} accepted = {tot_a/max(tot_c,1)*100:.2f}%")
# ASCII in prints. U+26A0 is not in cp1252 and raises on a Windows console; third time this
# session, so it is written down here as well as in the two files that hit it first.
print(f"  !! that sum double-counts texels visible from several cameras. The question a "
      f"summed rate CANNOT answer is whether the blade is painted on the FINISHED atlas — "
      f"for that, ask whether any view accepted a given texel.")

# The union question, which the per-view rates cannot answer: is a texel that lands in SOME
# view's excluded band accepted by ANY view? A texel excluded head-on may be picked up by a
# camera that sees the blade broadside and keys it better.
NVv = int(Z["__valid__"])
in_band_any = np.zeros(NVv, dtype=bool)
acc_any = np.zeros(NVv, dtype=bool)
for nm in views:
    mesh = Z[f"{nm}/mesh_fm"]
    twin = Z[f"{nm}/twin_fm"]
    lab, n = label(mesh & ~twin)
    if not n:
        continue
    sz = np.bincount(lab.ravel())[1:]
    band = lab == (int(np.argmax(sz)) + 1)
    px, py = Z[f"{nm}/px"], Z[f"{nm}/py"]
    pyi = np.clip(py.round().astype(int), 0, mesh.shape[0] - 1)
    pxi = np.clip(px.round().astype(int), 0, mesh.shape[1] - 1)
    idx = Z[f"{nm}/cand_idx"]
    in_band_any[idx[band[pyi, pxi]]] = True
    acc_any[idx[Z[f"{nm}/accepted"]]] = True
n_band = int(in_band_any.sum())
n_saved = int((in_band_any & acc_any).sum())
print(f"\nUNION over {len(views)} cameras — the number the per-view rates cannot give:")
print(f"  texels landing in SOME view's excluded band: {n_band:,}")
print(f"  of those, styled by SOME camera:             {n_saved:,} = "
      f"{n_saved/max(n_band,1)*100:.2f}%")
print(f"  left with no reference at all:               {n_band-n_saved:,}")
out = {"per_view": rows, "trust_intersect": bool(Z["__trust_intersect__"]),
       "summed_candidates": tot_c, "summed_accepted": tot_a,
       "union_in_band_any_view": n_band, "union_styled_by_some_camera": n_saved,
       "union_no_reference": n_band - n_saved}
if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[blade] wrote {args.out_json}")
