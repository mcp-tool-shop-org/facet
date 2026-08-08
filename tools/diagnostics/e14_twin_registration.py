"""Per-view twin registration against the EXACT raycast silhouette. Halts SUSPENDED.

E01 made this load-bearing: silhouette IoU 0.290 -> 0.777 was the fix that stopped the model
regenerating the character freely. `prop.json` expresses this subject's halts as vacuous
(reg-iou-min 0.0, bbox-tol 9.99) because the character's 0.80 is W3 data and this subject has
no distribution until its own twins exist - which is what this file measures.

THE KEYING LAWS THIS REPO HAS PAID FOR, all applied here:

  * CORNER-MEDIAN KEYING IS RETIRED - three failures. The background is fitted over a BORDER
    RING with a quadratic, which reduces to the corner median on a flat field so older numbers
    stay comparable. This subject's realised backdrop is neither flat nor stable (L* swings
    16.6 between seeds), so a single sample would be exactly the failure mode.
  * BBOX-CHECK THE KEYED MASK AGAINST THE GEOMETRY BEFORE READING A NUMBER FROM IT. "A figure
    cannot be 751 px wide in a 752 px frame when the mesh is 388." The keyed bbox is compared
    to the silhouette's and reported; a wild ratio invalidates the IoU beside it.
  * REPORT ABSOLUTE PX BESIDE EVERY RATIO. This subject's figure area swings 2.061x between
    views (Ruling 10c), so an IoU spread across views is partly a denominator artifact.
  * IoU AT THREE TOLERANCES, so a ranking can be checked for keying sensitivity rather than
    assumed - the E08 form, kept.

  e14_twin_registration.py --twins T0,... --masks M0,... --labels v0,... [--out J.json]

Standards compliance: PIN_PER_STEP - ring width, tolerances and the fit degree are flags.
ANDON_AUTHORITY - none by design; the profile suspends these halts and this file honours that,
printing what a halt WOULD have seen. EXTERNAL_VERIFIER - the reference is the raycast
silhouette, an independent code path from the generator.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--twins", required=True)
ap.add_argument("--masks", required=True)
ap.add_argument("--labels", required=True)
ap.add_argument("--ring", type=int, default=6, help="border ring width the background is fitted over")
ap.add_argument("--tols", default="0.06,0.10,0.15", help="keying tolerances, max-channel")
ap.add_argument("--out", default=None)
args = ap.parse_args()
TOLS = [float(v) for v in args.tols.split(",")]


def fit_bg(img, ring):
    """quadratic per channel over the border ring; reduces to a constant on a flat field"""
    H, W = img.shape[:2]
    m = np.zeros((H, W), bool)
    m[:ring, :] = m[-ring:, :] = m[:, :ring] = m[:, -ring:] = True
    ys, xs = np.nonzero(m)
    A = np.stack([np.ones_like(xs, float), xs, ys, xs * xs, xs * ys, ys * ys], axis=1)
    yy, xx = np.mgrid[0:H, 0:W]
    Af = np.stack([np.ones_like(xx, float).ravel(), xx.ravel(), yy.ravel(),
                   (xx * xx).ravel(), (xx * yy).ravel(), (yy * yy).ravel()], axis=1)
    out = np.empty_like(img)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, img[..., c][m], rcond=None)
        out[..., c] = (Af @ coef).reshape(H, W)
    return out


rows = []
print("[reg] %-5s %9s %9s %8s %8s %8s %8s %8s %9s   %s"
      % ("view", "sil px", "keyed px", "IoU.06", "IoU.10", "IoU.15", "dx", "dy",
         "bbox w/h", "bbox check"))
for tp, mp, lb in zip(args.twins.split(","), args.masks.split(","), args.labels.split(",")):
    img = np.asarray(Image.open(tp).convert("RGB")).astype(np.float64) / 255.0
    sil = np.asarray(Image.open(mp).convert("L")) > 127
    bg = fit_bg(img, args.ring)
    d = np.abs(img - bg).max(axis=2)
    ious, keyed_main = [], None
    for t in TOLS:
        key = d > t
        inter = int((key & sil).sum())
        union = int((key | sil).sum())
        ious.append(inter / max(union, 1))
        if abs(t - TOLS[0]) < 1e-12:
            keyed_main = key
    ys, xs = np.nonzero(keyed_main)
    sy, sx = np.nonzero(sil)
    if len(xs) and len(sx):
        kw, kh = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        sw, sh = sx.max() - sx.min() + 1, sy.max() - sy.min() + 1
        dx = float(xs.mean() - sx.mean())
        dy = float(ys.mean() - sy.mean())
        wr, hr = kw / sw, kh / sh
        ok = (0.75 <= wr <= 1.35) and (0.75 <= hr <= 1.35)
        chk = "ok" if ok else "SUSPECT"
    else:
        kw = kh = sw = sh = 0
        dx = dy = float("nan")
        wr = hr = float("nan")
        chk = "EMPTY"
    print("[reg] %-5s %9s %9s %8.4f %8.4f %8.4f %8.2f %8.2f %4dx%-4d   %s (%.2fx/%.2fx of the mesh)"
          % (lb, f"{int(sil.sum()):,}", f"{int(keyed_main.sum()):,}", *ious, dx, dy,
             kw, kh, chk, wr, hr))
    rows.append({"label": lb, "silhouette_px": int(sil.sum()),
                 "keyed_px": int(keyed_main.sum()),
                 "iou": {str(t): round(float(i), 5) for t, i in zip(TOLS, ious)},
                 "centroid_dx": round(dx, 3), "centroid_dy": round(dy, 3),
                 "keyed_bbox": [int(kw), int(kh)], "silhouette_bbox": [int(sw), int(sh)],
                 "bbox_ratio_w": round(float(wr), 4), "bbox_ratio_h": round(float(hr), 4),
                 "bbox_check": chk})

i0 = [r["iou"][str(TOLS[0])] for r in rows]
print("\n[reg] IoU at %g across the set: min %.4f (%s)  max %.4f (%s)  spread %.4f"
      % (TOLS[0], min(i0), rows[int(np.argmin(i0))]["label"], max(i0),
         rows[int(np.argmax(i0))]["label"], max(i0) - min(i0)))
print("[reg] HALTS SUSPENDED per prop.json (reg-iou-min 0.0, bbox-tol 9.99). This subject "
      "derives its own bound from THIS spread at its ruling, or keeps reporting - it never "
      "inherits W3's 0.80.")
print("[reg] MIRROR CORROBORATION (Ruling 10c): opposite views share a silhouette by "
      "orthographic construction, so any within-pair IoU difference is the GENERATOR, not "
      "the geometry.")
for a, b in ((0, 4), (1, 5), (2, 6), (3, 7)):
    ra, rb = rows[a], rows[b]
    print("[reg]   v%d vs v%d: sil %s == %s | IoU %.4f vs %.4f  (delta %.4f)"
          % (a, b, f"{ra['silhouette_px']:,}", f"{rb['silhouette_px']:,}",
             ra["iou"][str(TOLS[0])], rb["iou"][str(TOLS[0])],
             abs(ra["iou"][str(TOLS[0])] - rb["iou"][str(TOLS[0])])))

if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump({"ring": args.ring, "tolerances": TOLS, "views": rows},
              open(args.out, "w"), indent=1)
    print("\n[reg] wrote %s" % args.out)
