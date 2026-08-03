"""Head-crop comparison sheet, with the head band LOCATED rather than guessed.

Standing rule: judge identity and face quality at HEAD CROP, never off a full-figure
thumbnail.

The head band is found from the figure mask (background = sampled corner pixel), not from
hand-tuned fractions: fractions are a property of one subject's framing and silently
mis-crop the next character. `--auto` takes the topmost figure row and a head height
expressed as a fraction of TOTAL FIGURE HEIGHT, which is stable across subjects.

Usage:
  head_crop.py --images a.png b.png --labels A B --out sheet.png [--auto]
               [--head-frac 0.19] [--scale 3]
Manual override (when the mask is unreliable, e.g. a data atlas render):
  --top 0.03 --frac 0.20 --xpad 0.28
"""
import argparse
import numpy as np
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--images", nargs="+", required=True)
ap.add_argument("--labels", nargs="+", default=None)
ap.add_argument("--out", required=True)
ap.add_argument("--auto", action="store_true", default=True)
ap.add_argument("--no-auto", dest="auto", action="store_false")
ap.add_argument("--head-frac", type=float, default=0.19,
                help="head band height as a fraction of the figure's FULL height")
ap.add_argument("--pad-up", type=float, default=0.02,
                help="headroom above the crown, as a fraction of figure height")
ap.add_argument("--aspect", type=float, default=1.35, help="crop width / crop height")
ap.add_argument("--top", type=float, default=None, help="manual: band start, frac of image H")
ap.add_argument("--frac", type=float, default=None, help="manual: band height, frac of image H")
ap.add_argument("--xpad", type=float, default=None, help="manual: trim per side, frac of image W")
ap.add_argument("--scale", type=int, default=3)
ap.add_argument("--bg-tol", type=float, default=18.0)
args = ap.parse_args()

labels = args.labels or [str(i) for i in range(len(args.images))]
assert len(labels) == len(args.images), "labels must match images"

crops, notes = [], []
for p in args.images:
    im = Image.open(p).convert("RGB")
    W, H = im.size
    manual = args.top is not None and args.frac is not None
    if manual or not args.auto:
        y0, y1 = int(H * args.top), int(H * (args.top + args.frac))
        xp = args.xpad if args.xpad is not None else 0.28
        x0, x1 = int(W * xp), int(W * (1 - xp))
        notes.append("manual")
    else:
        a = np.asarray(im).astype(np.float32)
        corner = a[:12, :12].reshape(-1, 3).mean(axis=0)
        fig = np.abs(a - corner).max(axis=-1) > args.bg_tol
        rows = np.where(fig.any(axis=1))[0]
        if len(rows) < 8:
            raise SystemExit(f"{p}: no figure found (bg-tol {args.bg_tol})")
        top, bot = rows[0], rows[-1]
        fh = bot - top
        y0 = max(0, int(top - args.pad_up * fh))
        y1 = min(H, int(top + args.head_frac * fh))
        # centre horizontally on the HEAD's own pixels, not the whole figure
        band = fig[y0:y1]
        cols = np.where(band.any(axis=0))[0]
        cx = int((cols[0] + cols[-1]) / 2)
        half = int((y1 - y0) * args.aspect / 2)
        x0, x1 = max(0, cx - half), min(W, cx + half)
        notes.append(f"figure rows {top}-{bot} (h={fh}), head band {y0}-{y1}, cx={cx}")
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * args.scale, c.height * args.scale), Image.LANCZOS)
    crops.append(c)

BAND = 32
hmax = max(c.height for c in crops)
w = sum(c.width for c in crops)
sheet = Image.new("RGB", (w, hmax + BAND), (24, 24, 26))
d = ImageDraw.Draw(sheet)
x = 0
for c, lab in zip(crops, labels):
    sheet.paste(c, (x, BAND))
    d.text((x + 8, 9), lab, fill=(255, 255, 255))
    d.line([(x, 0), (x, hmax + BAND)], fill=(90, 90, 96), width=2)
    x += c.width
sheet.save(args.out)
print(f"wrote {args.out}  {sheet.size[0]}x{sheet.size[1]}")
for p, n in zip(args.images, notes):
    print(f"  {p}\n     {n}")
