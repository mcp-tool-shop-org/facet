"""E08 background arm, step 1 — derive the render background from the subject's gamut.

A4 failed because the background sits inside the subject's own colour range: mid-grey
(125,126,126) against steel, leather and shadowed cloth. No threshold separates two
populations that are one population. Changing the background creates the separation by
construction instead of thresholding a distribution that has none.

The colour is DERIVED, not chosen to look far enough:

  gamut   every Lab colour the twins paint inside their figure masks, both views unioned,
          eroded so the antialiased fringe (already background-mixed) does not enter it
  answer  the sRGB colour maximising the MINIMUM CIE76 distance to that gamut
  report  that minimum — it is the separation the arm buys, and it is the number the
          arm's premise stands on

Implemented as a distance transform over a quantised Lab grid: mark the cells the gamut
occupies, EDT the complement, then read every realisable sRGB colour off it and take the
argmax. Exhaustive over the quantisation rather than a search that could miss.

  e08_bg_derive.py --twins front.png,back.png [--out-json d.json]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, minimum_filter

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--twins", required=True)
ap.add_argument("--tol", type=float, default=0.06)
ap.add_argument("--erode", type=int, default=5)
ap.add_argument("--gamut-erode", type=int, default=9,
                help="extra erosion of the figure mask before harvesting colours, so the "
                     "background-mixed fringe does not enter the subject's gamut")
ap.add_argument("--cell", type=float, default=2.0, help="Lab grid cell, dE units")
ap.add_argument("--srgb-steps", type=int, default=32, help="candidates per sRGB axis")
ap.add_argument("--out-json")
args = ap.parse_args()


def srgb_to_lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


gamut = []
per_view = {}
for path in [p.strip() for p in args.twins.split(",") if p.strip()]:
    nm = os.path.splitext(os.path.basename(path))[0]
    img = np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0
    c8 = np.concatenate([img[:8, :8].reshape(-1, 3), img[:8, -8:].reshape(-1, 3)])
    bg = np.median(c8, axis=0)
    fm = minimum_filter((np.abs(img - bg).max(axis=-1) > args.tol).astype(np.float32),
                        size=args.erode) > 0.5
    core = minimum_filter(fm.astype(np.float32), size=args.gamut_erode) > 0.5
    lab = srgb_to_lab(img)
    gamut.append(lab[core])
    per_view[nm] = {"background_rgb": [int(x * 255) for x in bg],
                    "figure_px": int(fm.sum()), "gamut_px": int(core.sum())}
    print(f"[bg] {nm}: background rgb {tuple(int(x*255) for x in bg)}  figure "
          f"{int(fm.sum()):,}px  gamut core {int(core.sum()):,}px", flush=True)
G = np.concatenate(gamut, axis=0)
print(f"[bg] subject gamut: {len(G):,} samples from both views", flush=True)

# quantised Lab occupancy -> EDT gives min distance to the gamut for every cell
LO = np.array([0.0, -110.0, -110.0])
HI = np.array([100.0, 110.0, 110.0])
dims = np.ceil((HI - LO) / args.cell).astype(int) + 1
occ = np.zeros(dims, dtype=bool)
gi = np.clip(((G - LO) / args.cell).round().astype(int), 0, dims - 1)
occ[gi[:, 0], gi[:, 1], gi[:, 2]] = True
print(f"[bg] Lab grid {tuple(dims)} @ {args.cell} dE/cell, "
      f"{int(occ.sum()):,} cells occupied", flush=True)
dist = distance_transform_edt(~occ, sampling=(args.cell,) * 3)

# every realisable sRGB colour, read off the transform
s = np.linspace(0.0, 1.0, args.srgb_steps)
r, g, b = np.meshgrid(s, s, s, indexing="ij")
cand = np.stack([r.ravel(), g.ravel(), b.ravel()], axis=-1)
cl = srgb_to_lab(cand)
ci = np.clip(((cl - LO) / args.cell).round().astype(int), 0, dims - 1)
sep = dist[ci[:, 0], ci[:, 1], ci[:, 2]]
order = np.argsort(sep)[::-1]
best = cand[order[0]]
# exact minimum for the winner, against the full gamut rather than the grid
exact = float(np.min(np.linalg.norm(G - srgb_to_lab(best[None, :]), axis=-1)))
cur = np.array(per_view[list(per_view)[0]]["background_rgb"], dtype=np.float64) / 255.0
cur_exact = float(np.min(np.linalg.norm(G - srgb_to_lab(cur[None, :]), axis=-1)))

print(f"\n[bg] DERIVED background rgb {tuple(int(round(x*255)) for x in best)}  "
      f"minimum dE to the subject gamut {exact:.2f}")
print(f"[bg] current  background rgb {tuple(int(round(x*255)) for x in cur)}  "
      f"minimum dE to the subject gamut {cur_exact:.2f}")
print(f"[bg] top candidates (grid separation):")
seen = []
for o in order[:400]:
    c = cand[o]
    if any(np.linalg.norm(c - q) < 0.30 for q in seen):
        continue
    seen.append(c)
    e = float(np.min(np.linalg.norm(G - srgb_to_lab(c[None, :]), axis=-1)))
    print(f"[bg]     rgb {tuple(int(round(x*255)) for x in c)}  min dE {e:.2f}")
    if len(seen) >= 5:
        break

out = {"views": per_view, "gamut_samples": int(len(G)),
       "derived_rgb": [int(round(x * 255)) for x in best],
       "derived_min_dE": round(exact, 2),
       "current_rgb": [int(round(x * 255)) for x in cur],
       "current_min_dE": round(cur_exact, 2)}
if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[bg] wrote {args.out_json}")
