"""E13 H2 — registration of a CROP-framed twin, keyed off a background region a crop frame
actually has.

WHY A NEW INSTRUMENT AND NOT `e12_twin_readout`. That tool fits the background over a BORDER
RING, which is E08's correction to corner-median keying and is right on a full-figure frame:
the 1.204 margin insets the figure ~8% so the ring is guaranteed background. A crop frame has
no such guarantee. Measured on these two crops, the figure reaches the border on both — 53.1%
of frame at yaw 0 with the silhouette touching three edges, 66.7% at yaw 45 touching all four
— and the readout's own key-health guard fired and declared its IoU unusable (94.6% / 67.0%
of the frame past the key, twin bbox 1359x1359 against a 1359x1172 mesh). That guard working
is the reason this file exists rather than a number being quoted anyway.

WHAT IS DIFFERENT, AND WHY IT IS NOT CIRCULAR. The background model is fitted over pixels the
GEOMETRY says are background and are at least --clear px outside the silhouette. Geometry
picks the SAMPLES; it does not decide the answer. The key that follows is a threshold on the
image and is free to disagree with the silhouette anywhere — it under-covers if the twin
painted the figure short and over-covers if it painted past the edge, which is exactly what
registration means. What geometry cannot do here is manufacture agreement: a twin registered
to the wrong place still keys to the wrong place, and the IoU still falls.

Reported, never gated: this subject's registration halt is SUSPENDED (profiles/beast.json,
reg-iou-min 0.0) and nothing here arms it.

Standards compliance:
  PIN_PER_STEP — every operand is a path; the clearance and tolerance print with the result.
  ANDON_AUTHORITY — raises if the clean-background region is too small to fit over, rather
    than fitting on contaminated samples and returning a confident wrong number.
  NAMED_COMPENSATORS — writes one JSON and optional overlays under paths given. Undo = delete.
  EXTERNAL_VERIFIER — it measures paint against geometry the generator does not control.

  e13_crop_registration.py --image LABEL=PATH --mask LABEL=PATH [--clear 24] [--tol 0.06]
                           [--out J] [--overlay DIR]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, distance_transform_edt, label

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--image", action="append", required=True, metavar="LABEL=PATH")
ap.add_argument("--mask", action="append", required=True, metavar="LABEL=PATH",
                help="EXACT raycast silhouette at the SAME camera, matched by LABEL")
ap.add_argument("--clear", type=float, default=24.0,
                help="fit the background only on pixels at least this far OUTSIDE the "
                     "silhouette, so antialiased rim mixing cannot enter the fit")
ap.add_argument("--tol", type=float, default=0.06,
                help="residual from the fitted background above which a pixel is paint. "
                     "figure_mask's own value, kept so the numbers stay comparable.")
ap.add_argument("--min-clean", type=float, default=0.02,
                help="ANDON: halt if the clean-background region is under this share of "
                     "frame — the fit would be unconstrained and the key meaningless")
ap.add_argument("--out")
ap.add_argument("--overlay")
args = ap.parse_args()


def _pairs(specs, what):
    out = {}
    for s in specs:
        k, _, p = s.partition("=")
        if not (p):
            raise AssertionError(f"ANDON: --{what} wants LABEL=PATH, got {s!r}")
        if not (os.path.exists(p)):
            raise AssertionError(f"ANDON: --{what} {k}: no such file {p}")
        out[k] = p
    return out


IM, MK = _pairs(args.image, "image"), _pairs(args.mask, "mask")
if not (set(IM) == set(MK)):
    raise AssertionError(f"ANDON: labels differ — images {sorted(IM)} masks {sorted(MK)}")

print(f"[creg] background fitted on pixels >= {args.clear:g}px OUTSIDE the raycast "
      f"silhouette; paint = residual > {args.tol:g}. NO BOUND IS ARMED "
      f"(beast.json reg-iou-min 0.0).", flush=True)
print(f"[creg] {'label':<10}| {'clean bg':>9} {'keyed':>9} {'mesh':>9} | {'IoU':>9} "
      f"{'twin bbox':>13} {'mesh bbox':>13} | out/in", flush=True)

res = {"_what": "E13 H2 crop-twin registration. Background fitted on geometry-selected clean "
                "samples because a crop frame's border ring is inside the figure.",
       "clear_px": args.clear, "tol": args.tol, "views": {}}

for k in sorted(IM):
    img = np.asarray(Image.open(IM[k]).convert("RGB"), dtype=np.float64) / 255.0
    mesh = np.asarray(Image.open(MK[k]).convert("L"), dtype=np.uint8) > 127
    H, W = mesh.shape
    if not (img.shape[:2] == (H, W)):
        raise AssertionError(f"ANDON: {k}: image {img.shape[:2]} vs mask {(H, W)}")

    # distance OUTSIDE the silhouette; clean = far enough out that rim mixing cannot reach
    d_out = distance_transform_edt(~mesh)
    clean = d_out >= args.clear
    frac_clean = float(clean.mean())
    if not (frac_clean >= args.min_clean):
        raise AssertionError(
            f"ANDON: {k}: only {frac_clean*100:.2f}% of frame is clean background at "
            f"--clear {args.clear:g} — under the {args.min_clean*100:.1f}% floor, so the "
            f"background fit would be unconstrained. Widen the crop or lower --clear "
            f"deliberately; do not read a number off this.")

    ys, xs = np.where(clean)
    xn = xs / W - 0.5
    yn = ys / H - 0.5
    A = np.stack([np.ones_like(xn), xn, yn, xn * xn, xn * yn, yn * yn], axis=1)
    gx, gy = np.meshgrid(np.arange(W) / W - 0.5, np.arange(H) / H - 0.5)
    Afull = np.stack([np.ones_like(gx), gx, gy, gx * gx, gx * gy, gy * gy], axis=-1)
    bg = np.empty_like(img)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, img[ys, xs, c], rcond=None)
        bg[..., c] = Afull @ coef
    keyed = np.abs(img - bg).max(axis=-1) > args.tol

    inter = int((keyed & mesh).sum())
    union = int((keyed | mesh).sum())
    iou = inter / max(union, 1)
    out_px = int((keyed & ~mesh).sum())
    in_px = int((~keyed & mesh).sum())
    lab, n = label(keyed & ~mesh)
    cc = int(np.bincount(lab.ravel())[1:].max()) if n else 0

    def _bb(m):
        yy, xx = np.where(m)
        return ([int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())]
                if len(xx) else [0, 0, 0, 0])
    bt, bm = _bb(keyed), _bb(mesh)
    print(f"[creg] {k:<10}| {frac_clean*100:8.2f}% {int(keyed.sum()):>9,} "
          f"{int(mesh.sum()):>9,} | {iou:9.6f} "
          f"{bt[2]-bt[0]+1:>5}x{bt[3]-bt[1]+1:<7} {bm[2]-bm[0]+1:>5}x{bm[3]-bm[1]+1:<7} | "
          f"{out_px:,}/{in_px:,}", flush=True)
    print(f"[creg]     paint OUTSIDE the silhouette {out_px:,}px (largest component "
          f"{cc:,}px)   silhouette left UNPAINTED {in_px:,}px", flush=True)
    res["views"][k] = {"image": os.path.abspath(IM[k]), "mask": os.path.abspath(MK[k]),
                       "clean_bg_frac": frac_clean, "keyed_px": int(keyed.sum()),
                       "mesh_px": int(mesh.sum()), "iou": iou,
                       "keyed_bbox": bt, "mesh_bbox": bm,
                       "paint_outside_px": out_px, "paint_outside_largest_cc": cc,
                       "silhouette_unpainted_px": in_px}
    if args.overlay:
        os.makedirs(args.overlay, exist_ok=True)
        ov = (img * 255).astype(np.uint8).copy()
        edge = mesh ^ binary_dilation(mesh, np.ones((3, 3), bool))
        ov[edge] = (255, 40, 40)
        ov[keyed & ~mesh] = (40, 220, 255)
        Image.fromarray(ov).save(os.path.join(args.overlay, f"{k}_creg.png"))

if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(res, open(args.out, "w"), indent=1)
    print(f"[creg] wrote {args.out} — DONE (this tool decides nothing)", flush=True)
