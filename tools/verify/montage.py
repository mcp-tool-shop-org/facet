"""Contact sheet + per-view figure brightness readout.

Two jobs, deliberately together:
  1. lay N views out in a row so a turnaround can be judged as a set
  2. print the FIGURE's mean value/saturation per view

(2) is the regression gate for the world-space-lighting bug. A camera orbiting a fixed
light produces a brightness gradient the restylize will faithfully bake into the sprite
set; it reads exactly like a dead texture on the back half. The per-view spread must be
flat (<1.2x) before any view is sent to a paint pass.

Background is excluded by value+saturation distance from the sampled corner pixel, not by
a computed constant -- the pad colour was derived once as 87/255 when the render's actual
background was 118.

Usage:
  montage.py --glob "dir/tag_{}.png" --views 0,1,2,3,4,5,6,7 --out sheet.png [--scale 0.5]
  montage.py --images a.png b.png --labels A B --out sheet.png
"""
import argparse
import numpy as np
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--glob", default=None, help="format string with {} for the view index")
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--images", nargs="+", default=None)
ap.add_argument("--labels", nargs="+", default=None)
ap.add_argument("--out", required=True)
ap.add_argument("--scale", type=float, default=0.5)
ap.add_argument("--bg-tol", type=float, default=18.0,
                help="max per-channel distance from the sampled corner to count as background")
args = ap.parse_args()

if args.glob:
    idxs = [int(v) for v in args.views.split(",")]
    paths = [args.glob.format(i) for i in idxs]
    labels = [f"v{i}" for i in idxs]
else:
    paths = args.images
    labels = args.labels or [str(i) for i in range(len(paths))]

ims, stats = [], []
for p in paths:
    im = Image.open(p).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    # sample the actual corner rather than assuming a pad value
    corner = a[:12, :12].reshape(-1, 3).mean(axis=0)
    fig = (np.abs(a - corner).max(axis=-1) > args.bg_tol)
    if fig.sum() < 50:
        val = sat = 0.0
        cov = 0.0
    else:
        px = a[fig]
        val = px.mean()
        mx, mn = px.max(axis=-1), px.min(axis=-1)
        sat = float(np.mean(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)) * 100)
        cov = 100.0 * fig.mean()
    stats.append((val, sat, cov, corner.mean()))
    ims.append(im)

BAND = 26
w = int(ims[0].width * args.scale)
h = int(ims[0].height * args.scale)
sheet = Image.new("RGB", (w * len(ims), h + BAND), (24, 24, 26))
d = ImageDraw.Draw(sheet)
for i, (im, lab) in enumerate(zip(ims, labels)):
    sheet.paste(im.resize((w, h), Image.LANCZOS), (i * w, BAND))
    d.text((i * w + 6, 7), f"{lab}  {stats[i][0]:.1f}", fill=(255, 255, 255))
    d.line([(i * w, 0), (i * w, h + BAND)], fill=(90, 90, 96))
sheet.save(args.out)

vals = [s[0] for s in stats]
print(f"wrote {args.out}  {sheet.size[0]}x{sheet.size[1]}")
print(f"{'view':>6} {'figure_val':>11} {'sat%':>7} {'cover%':>8} {'bg':>7}")
for lab, (v, s, c, bg) in zip(labels, stats):
    print(f"{lab:>6} {v:>11.1f} {s:>7.1f} {c:>8.2f} {bg:>7.1f}")
lo, hi = min(vals), max(vals)
spread = hi / max(lo, 1e-6)
verdict = "PASS" if spread < 1.2 else "FAIL"
print(f"\nper-view brightness spread: {spread:.2f}x  (min {lo:.1f}  max {hi:.1f})  [{verdict}, gate <1.20x]")
