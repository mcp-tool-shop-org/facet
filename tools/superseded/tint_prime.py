"""TINT-PRIME — paint the styled twin's palette onto a clay render, deterministically.

Stage of the clay-sprite pipeline (2026-08-03, Director's architecture): the styled
TWIN (a canny-locked restylize of the clay CONCEPT — pixel-registered by construction)
is the character's colour canon. Before per-view restylize, each clay view is primed
with the twin's colours so the restylize can run at LOW denoise (~0.70), where the
measured colour-PRESERVATION mechanism holds (named garments survive) and proportions
never wander. This replaces colour-INJECTION at high denoise, which was measured
2026-08-03 to fail two ways: named colours cannot pull a grey input to a palette at
0.75, and at 0.92 the freed model re-invents proportions on ambiguous views (the
gnome-head failure).

Method: height-band-wise LAB transfer. The figure is standing, so garments stack
vertically; for each of --bands horizontal slices of figure height, take the twin's
chroma (a,b) per-band mean and paint it onto the clay view's same band, KEEPING the
clay's L channel (the render's shading). Crude on purpose — a prime is an anchor for
denoise 0.7, not a paint job; the sword crossing bands repaints fine because steel
stays named in the prompt.

  tint_prime.py --twin styled_front.png --clay view.png --out primed.png
                [--bands 28] [--strength 0.85] [--bg-tol 18]
"""
import argparse

import numpy as np
from PIL import Image
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("--twin", required=True, help="styled twin (colour canon, any view angle)")
ap.add_argument("--clay", required=True, help="clay render to prime")
ap.add_argument("--out", required=True)
ap.add_argument("--bands", type=int, default=28)
ap.add_argument("--strength", type=float, default=0.85,
                help="0..1 blend of twin chroma into the clay band")
ap.add_argument("--bg-tol", type=float, default=18.0)
args = ap.parse_args()


def fig_mask(rgb, tol):
    corner = rgb[:12, :12].reshape(-1, 3).mean(axis=0)
    m = np.abs(rgb.astype(np.float32) - corner).max(axis=-1) > tol
    return m


def band_rows(mask):
    r = np.where(mask.any(axis=1))[0]
    return r[0], r[-1]


twin = np.asarray(Image.open(args.twin).convert("RGB"))
clay = np.asarray(Image.open(args.clay).convert("RGB"))
tm, cm = fig_mask(twin, args.bg_tol), fig_mask(clay, args.bg_tol)
t0, t1 = band_rows(tm)
c0, c1 = band_rows(cm)

twin_lab = cv2.cvtColor(twin, cv2.COLOR_RGB2LAB).astype(np.float32)
clay_lab = cv2.cvtColor(clay, cv2.COLOR_RGB2LAB).astype(np.float32)
out = clay_lab.copy()

for b in range(args.bands):
    ty0 = t0 + (t1 - t0) * b // args.bands
    ty1 = t0 + (t1 - t0) * (b + 1) // args.bands
    cy0 = c0 + (c1 - c0) * b // args.bands
    cy1 = c0 + (c1 - c0) * (b + 1) // args.bands
    tsel = tm[ty0:ty1]
    csel = cm[cy0:cy1]
    if not tsel.sum() or not csel.sum():
        continue
    ta = twin_lab[ty0:ty1][tsel]
    # DOMINANT chroma cluster per band, not the mean: a band mixing sword-steel,
    # skin and a dark-green tunic averages to beige (measured 2026-08-03, twice —
    # a >12 chroma filter also fails because dark garments sit near the threshold).
    # k-means the (a,b) chroma, drop near-neutral clusters, take the largest.
    ab = ta[:, 1:3].astype(np.float32)
    if len(ab) >= 60:
        _, labels, centers = cv2.kmeans(
            ab, 3, None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 12, 1.0),
            2, cv2.KMEANS_PP_CENTERS)
        counts = np.bincount(labels.ravel(), minlength=3)
        chroma_c = np.hypot(centers[:, 0] - 128.0, centers[:, 1] - 128.0)
        keep = chroma_c > 8.0
        if keep.any():
            counts = np.where(keep, counts, -1)
        k = int(np.argmax(counts))
        mean_a, mean_b = float(centers[k, 0]), float(centers[k, 1])
    else:
        mean_a, mean_b = float(ta[:, 1].mean()), float(ta[:, 2].mean())
    region = out[cy0:cy1]
    s = args.strength
    region[..., 1] = np.where(csel, region[..., 1] * (1 - s) + mean_a * s, region[..., 1])
    region[..., 2] = np.where(csel, region[..., 2] * (1 - s) + mean_b * s, region[..., 2])
    out[cy0:cy1] = region

rgb = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
Image.fromarray(rgb).save(args.out)
print(f"[tint] {args.clay} -> {args.out}  (bands {args.bands}, strength {args.strength})")
