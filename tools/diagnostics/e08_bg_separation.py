"""E08 A4 — is the subject separable from its background, and where does the cut fall?

A4 replaces a geometric proxy (distance into the twin's keyed mask) with the property the
proxy was standing in for: how far a sampled colour sits from the twin's own background.
Half-width was never measuring thinness — it measures what fraction of a structure is
BOUNDARY, which is why a 1-2px structure reads as entirely contaminated and a torso does
not. Contamination is a boundary phenomenon, so test for it directly.

Two things have to be measured before that rule can be written, and neither may be chosen:

  1. THE THRESHOLD, from the bimodality itself.

     ⚠ MEASURED AND FAILED on W3 (E08 A4). Otsu is reported below and is the WRONG TOOL
     here: it maximises between-class variance over the whole distribution, so with the
     contaminated class at 0.5% of the mask it finds the dominant split instead — cut
     33.63, class means 25.8 / 41.6, i.e. dark paint against light paint, rejecting
     41,194 px at a median depth of 8 px, deep in the interior.
     And the premise underneath it does not hold either: the density over the figure
     rises MONOTONICALLY from ~5 to 30 with no antimode at all. The apparent "gap
     between 10 and 25" came from comparing two summary statistics — region medians
     (24.8+) against the contaminated set's median (4.9) — and two distant medians do
     not imply a gap in the density between them.
     The antimode is therefore reported as a measurement that may not exist, never
     assumed. Read `below_threshold_pct` and the depth rows beside it: on W3 only
     47-48% of sub-threshold pixels lie within 2 px of the mask edge, so a colour cut
     is not a proxy for a boundary cut on this subject.

  2. THE DISCRIMINATOR'S OWN PRECONDITION. It degrades when a material approaches its
     background, and E04's galleon is staged for exactly that — grey on grey. Otsu's
     separability eta = between-class variance / total variance is reported every run, so a
     future subject fails visibly instead of silently.

Also measures what residual erosion, if any, the colour rule still needs: a pixel blended
a fraction alpha with the background sits at roughly alpha x the paint's own distance, so
the rule may self-erode the antialiased fringe without an explicit floor.

  e08_bg_separation.py --twins front.png,back.png [--out-json s.json] [--sheet s.png]
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
ap.add_argument("--bins", type=int, default=256)
ap.add_argument("--out-json")
ap.add_argument("--sheet")
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


def otsu(vals, nbins, vmax):
    """Threshold maximising between-class variance, and the separability eta."""
    h, edges = np.histogram(np.clip(vals, 0, vmax), bins=nbins, range=(0, vmax))
    p = h.astype(np.float64) / max(h.sum(), 1)
    mids = (edges[:-1] + edges[1:]) / 2
    w0 = np.cumsum(p)
    m0 = np.cumsum(p * mids)
    mT = m0[-1]
    with np.errstate(invalid="ignore", divide="ignore"):
        sb = (mT * w0 - m0) ** 2 / (w0 * (1 - w0))
    sb = np.nan_to_num(sb)
    i = int(np.argmax(sb))
    var_t = float((p * (mids - mT) ** 2).sum())
    return float(mids[i]), float(sb[i] / var_t) if var_t > 0 else 0.0, h, mids


out = {}
panels = []
for path in [p.strip() for p in args.twins.split(",") if p.strip()]:
    nm = os.path.splitext(os.path.basename(path))[0]
    img = np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0
    c8 = np.concatenate([img[:8, :8].reshape(-1, 3), img[:8, -8:].reshape(-1, 3)])
    bg = np.median(c8, axis=0)
    dE = np.linalg.norm(srgb_to_lab(img) - srgb_to_lab(bg[None, None, :]), axis=-1)
    fm = minimum_filter((np.abs(img - bg).max(axis=-1) > args.tol).astype(np.float32),
                        size=args.erode) > 0.5
    vals = dE[fm]
    thr, eta, h, mids = otsu(vals, args.bins, 60.0)
    # the antimode: the sparsest bin strictly between the two class means, reported so
    # the gap is shown rather than asserted
    lo_m = float(vals[vals <= thr].mean()) if (vals <= thr).any() else 0.0
    hi_m = float(vals[vals > thr].mean()) if (vals > thr).any() else 0.0
    band = (mids > lo_m) & (mids < hi_m)
    anti = float(mids[band][int(np.argmin(h[band]))]) if band.any() else float("nan")
    dist = distance_transform_edt(fm).astype(np.float32)
    row = {"background_rgb": [int(x * 255) for x in bg],
           "figure_px": int(fm.sum()),
           "otsu_threshold": round(thr, 2),
           "otsu_separability_eta": round(eta, 4),
           "class_mean_low": round(lo_m, 2), "class_mean_high": round(hi_m, 2),
           "antimode": round(anti, 2),
           "below_threshold_pct": round(float((vals <= thr).mean() * 100), 2)}
    print(f"\n[sep] {nm}: background rgb {tuple(int(x*255) for x in bg)}, "
          f"figure {int(fm.sum()):,}px")
    print(f"[sep]   Otsu cut {thr:.2f}   separability eta {eta:.4f}   "
          f"class means {lo_m:.1f} / {hi_m:.1f}   antimode {anti:.1f}")
    print(f"[sep]   figure below the cut: {(vals<=thr).mean()*100:.2f}%")
    # what the cut costs, by how much of a structure is boundary
    for a_, b_ in ((1, 2), (2, 4), (4, 8), (8, 16), (16, 32), (32, 1e9)):
        pass
    # residual erosion the colour rule implies on its own: where do rejected pixels sit?
    rej = fm & (dE <= thr)
    for t in (0.5, 1.0, 1.5, 2.0, 3.0):
        row[f"rejected_within_{t}px_of_edge_pct"] = round(
            float((dist[rej] <= t).mean() * 100), 1) if rej.any() else 0.0
    if rej.any():
        print(f"[sep]   pixels the colour cut rejects: {int(rej.sum()):,}  "
              f"within 1px of the mask edge {(dist[rej]<=1.0).mean()*100:.1f}%  "
              f"within 2px {(dist[rej]<=2.0).mean()*100:.1f}%  "
              f"median depth {np.median(dist[rej]):.2f}px")
        row["rejected_px"] = int(rej.sum())
        row["rejected_median_depth_px"] = round(float(np.median(dist[rej])), 2)
    out[nm] = row
    if args.sheet:
        vis = (img * 255).astype(np.uint8).copy()
        vis[rej] = (240, 60, 50)
        panels.append(vis)

if args.sheet and panels:
    os.makedirs(os.path.dirname(os.path.abspath(args.sheet)), exist_ok=True)
    Image.fromarray(np.concatenate(panels, axis=1)).save(args.sheet)
    print(f"\n[sep] wrote {args.sheet} — red = rejected by the colour cut")
if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
