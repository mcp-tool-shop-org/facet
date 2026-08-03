"""Build the per-view denoise masks: flat (control) and foreshortening-GRADED (test).

SetLatentNoiseMask + DifferentialDiffusion read the mask as a per-pixel denoise schedule:
255 = repaint freely, 0 = preserve. The proven recipe uses a flat horizontal band -- head
region 71 (0.28), body 255, 34 px feather -- which holds identity but also faithfully
preserves the smeared 3/4 cheek, because it cannot tell a sharp region from a smeared one.

The graded mask can. facing (n . z_front, baked by facing_atlas.py and rendered per view)
says how obliquely the projection camera saw each pixel's surface: 1.0 = square-on, so the
texture under it is real detail worth preserving; low = stretched, so what is under it is a
smear worth repainting. Measured on this head: 28.6% of the front view is beyond 60 deg,
versus 52% of either 3/4 view.

    head pixel value = lerp(PRESERVE, OPEN, 1 - facing)

so a square-on feature keeps the proven 71 and a receding cheek opens toward OPEN. This is
the mechanical form of the rule the hands proved: preserve where the input is good, open
where the input is bad.

Everything outside the head band stays exactly as the proven recipe has it, so the mask is
the only thing that differs between the control and test arms.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument("--work", default=r"E:/AI/training/saltroad_bake_fix")
ap.add_argument("--renders", default="g8/tex_{}.png",
                help="format string for the colour renders. Default is the CORRECTED set "
                     "(camera-relative lighting); the old turn_proj/proj_*.png carry a "
                     "world-space-light shadow gradient that would be baked into the sprites.")
ap.add_argument("--facing", default="face", help="dir of facing renders face_<v>.png")
ap.add_argument("--out", default="masks")
ap.add_argument("--views", default="7,0,1")
ap.add_argument("--preserve", type=int, default=71, help="proven head value (0.28 * 255)")
ap.add_argument("--open", type=int, default=200, help="value a fully-smeared head pixel opens to")
ap.add_argument("--band", type=int, default=288, help="head band height in px, as the proven mask")
ap.add_argument("--feather", type=int, default=34)
ap.add_argument("--crop-w", type=int, default=752, help="crop to a /8-divisible width, as the cloud run does")
args = ap.parse_args()

W = Path(args.work)
OUT = Path(args.out); OUT.mkdir(parents=True, exist_ok=True)
views = [int(v) for v in args.views.split(",")]


def crop(im: Image.Image) -> Image.Image:
    dx = (im.width - args.crop_w) // 2
    return im.crop((dx, 0, dx + args.crop_w, im.height))


for v in views:
    render = Image.open(args.renders.format(v)).convert("RGB")
    facing = Image.open(Path(args.facing) / f"face_{v}.png").convert("L")

    a = np.asarray(render, dtype=np.int16)
    fig = np.abs(a - a[0, 0]).sum(-1) > 18                      # figure vs flat viewport bg
    f = np.asarray(facing, dtype=np.float32) / 255.0

    # ---- control: the proven flat band -------------------------------------------------
    flat = np.full(a.shape[:2], 255, dtype=np.float32)
    flat[:args.band] = args.preserve

    # ---- test: same band, graded inside it by how square-on the source was --------------
    graded = np.full(a.shape[:2], 255, dtype=np.float32)
    band = np.zeros(a.shape[:2], bool); band[:args.band] = True
    val = args.preserve + (args.open - args.preserve) * (1.0 - f)
    graded[band] = args.preserve                                 # background inside the band
    sel = band & fig
    graded[sel] = val[sel]

    for name, m in (("flat", flat), ("graded", graded)):
        im = Image.fromarray(np.clip(m, 0, 255).astype(np.uint8), mode="L")
        im = im.filter(ImageFilter.GaussianBlur(args.feather / 3.0))
        crop(im).convert("RGB").save(OUT / f"mask_{name}_{v}.png")

    crop(render).save(OUT / f"img_{v}.png")
    head = sel
    print(f"view {v}: head pixels {head.sum():6,}  mean facing {f[head].mean():.3f}  "
          f"graded head value mean {graded[head].mean():5.1f} (flat is {args.preserve})  "
          f"opened >120: {100*(graded[head] > 120).mean():4.1f}%")

print(f"\nwrote {2*len(views)} masks + {len(views)} images to {OUT}/  at {args.crop_w}x1024")
