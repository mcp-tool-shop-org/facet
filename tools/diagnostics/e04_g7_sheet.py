"""E04 Arm G7 - the comparison sheet. Built before the report is written, not after it.

Two sheets, because the repo's cheapest diagnostic is putting the thing next to the thing it
is supposed to be compared with, at the Director's zoom rather than at contact-sheet scale:

  FULL    before | after | change map, whole frame, 1:1
  ZOOM    before | after | change map, cropped to the gun-port band and scaled up, so a
          feature a few tens of pixels wide is judgeable by eye

The change map is the per-pixel Lab distance inside the exact silhouette, on a fixed 0-30
scale printed in the caption, so two runs of this script are comparable and nothing is
auto-normalised into looking dramatic.

  e04_g7_sheet.py --before B.png --after A.png --mask M.png --crop x0,y0,x1,y1 --out DIR
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--before", required=True)
ap.add_argument("--after", required=True)
ap.add_argument("--mask", required=True)
ap.add_argument("--crop", default="440,700,880,860", help="x0,y0,x1,y1 in source pixels")
ap.add_argument("--zoom", type=int, default=3)
ap.add_argument("--dE-scale", type=float, default=30.0)
ap.add_argument("--out", required=True)
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)


def lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


B = np.asarray(Image.open(args.before).convert("RGB"), dtype=np.float32) / 255.0
A = np.asarray(Image.open(args.after).convert("RGB"), dtype=np.float32) / 255.0
SIL = np.asarray(Image.open(args.mask).convert("L")) > 127
D = np.linalg.norm(lab(A) - lab(B), axis=-1)
D[~SIL] = 0.0
t = np.clip(D / args.dE_scale, 0, 1)
heat = np.stack([t, np.zeros_like(t), 1.0 - t], axis=-1) * (t > 0.02)[..., None]
heat = (heat * 255).astype(np.uint8)

PAD, BAR = 12, 34
for name, box, z in (("FULL", (0, 0, B.shape[1], B.shape[0]), 1),
                     ("ZOOM", tuple(int(v) for v in args.crop.split(",")), args.zoom)):
    x0, y0, x1, y1 = box
    panels = []
    for im in (B, A, heat.astype(np.float32) / 255.0):
        p = Image.fromarray((np.clip(im[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8))
        if z != 1:
            p = p.resize((p.width * z, p.height * z), Image.NEAREST)
        panels.append(p)
    w, h = panels[0].width, panels[0].height
    sheet = Image.new("RGB", (3 * w + 4 * PAD, h + 2 * PAD + BAR), (24, 24, 26))
    d = ImageDraw.Draw(sheet)
    labels = ["BEFORE   red-lined gun port lids",
              "AFTER    red gun port lids",
              "CHANGE   blue 0 -> red dE %.0f+" % args.dE_scale]
    for i, (p, lb) in enumerate(zip(panels, labels)):
        x = PAD + i * (w + PAD)
        sheet.paste(p, (x, PAD + BAR))
        d.text((x + 3, PAD + 8), lb, fill=(232, 232, 236))
    out = os.path.join(args.out, "G7_%s_sheet.png" % name)
    sheet.save(out)
    print("[sheet] %s  %dx%d  crop %s  zoom %dx  ->  %s"
          % (name, sheet.width, sheet.height, box, z, out), flush=True)
