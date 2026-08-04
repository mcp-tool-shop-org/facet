"""The Gate 1 sheet — reference | asset | provenance | error, at the Director's zoom.

The cheapest diagnostic in this repo and the one E07 ran four arms without: put the asset next
to the thing it is supposed to look like, with where every texel came from and where it
disagrees, on one sheet, at a scale where the defects that decide acceptance are visible.

Built BEFORE the metrics, per CLAUDE.md. Textures come from a --flat render (a STUDIO render is
specular highlights on flat-shaded normals, not a texture readout).

  gate1_sheet.py --twins DIR --asset DIR --prov DIR --masks DIR --views 4,5,6 --out sheet.png
                 [--crop y0,y1,x0,x1] [--label "..."]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--twins", required=True)
ap.add_argument("--asset", required=True)
ap.add_argument("--prov", required=True)
ap.add_argument("--masks", required=True, help="exact silhouettes, for the error denominator")
ap.add_argument("--views", default="4,5,6")
ap.add_argument("--out", required=True)
ap.add_argument("--crop", default=None, help="y0,y1,x0,x1 in the 752x1024 frame")
ap.add_argument("--scale", type=float, default=1.0)
ap.add_argument("--out-json")
args = ap.parse_args()


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


def heat(d, vmax=40.0):
    """ΔE -> perceptual ramp. Dark = agrees, white-hot = disagrees."""
    t = np.clip(d / vmax, 0, 1)
    r = np.clip(2.2 * t, 0, 1)
    g = np.clip(2.2 * t - 0.7, 0, 1)
    b = np.clip(3.0 * t - 2.0, 0, 1)
    return (np.stack([r, g, b], axis=-1) * 255).astype(np.uint8)


VIEWS = [int(v) for v in args.views.split(",")]
rows = []
stats = {}
for k in VIEWS:
    ref = np.asarray(Image.open(os.path.join(args.twins, f"twin_{k}.png")
                                ).convert("RGB"), dtype=np.float32) / 255.0
    ast = np.asarray(Image.open(os.path.join(args.asset, f"final_{k}.png")
                                ).convert("RGB"), dtype=np.float32) / 255.0
    prv = np.asarray(Image.open(os.path.join(args.prov, f"prov_{k}.png")
                                ).convert("RGB"), dtype=np.float32) / 255.0
    sil = np.asarray(Image.open(os.path.join(args.masks, f"w3clay_{k}.png")
                                ).convert("L")) > 127
    dE = np.linalg.norm(lab(ast) - lab(ref), axis=-1)
    err = heat(dE)
    err[~sil] = 20                      # outside the silhouette is not the asset's business
    stats[str(k)] = {"figure_px": int(sil.sum()),
                     "dE_median": round(float(np.median(dE[sil])), 2),
                     "dE_mean": round(float(dE[sil].mean()), 2),
                     "dE_p90": round(float(np.percentile(dE[sil], 90)), 2),
                     "pct_over_10": round(float((dE[sil] > 10).mean() * 100), 1),
                     "pct_over_23": round(float((dE[sil] > 23).mean() * 100), 1)}
    panels = [(ref * 255).astype(np.uint8), (ast * 255).astype(np.uint8),
              (prv * 255).astype(np.uint8), err]
    if args.crop:
        y0, y1, x0, x1 = [int(v) for v in args.crop.split(",")]
        panels = [p[y0:y1, x0:x1] for p in panels]
    rows.append(np.concatenate(panels, axis=1))

sheet = np.concatenate(rows, axis=0)
if args.scale != 1.0:
    im = Image.fromarray(sheet)
    sheet = np.asarray(im.resize((int(im.width * args.scale), int(im.height * args.scale)),
                                 Image.LANCZOS))
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
Image.fromarray(sheet).save(args.out)
print(f"[sheet] wrote {args.out}  {sheet.shape[1]}x{sheet.shape[0]}")
print(f"[sheet] columns: REFERENCE (twin) | ASSET (--flat) | PROVENANCE | ERROR (dE heat)")
print(f"[sheet] provenance: GREEN = reference/stage1 · BLUE = brush · ORANGE = dilation")
print(f"[sheet] rows: views {', '.join(str(v) for v in VIEWS)}")
for k, s in stats.items():
    print(f"[sheet]   view {k}: dE median {s['dE_median']:>5}  mean {s['dE_mean']:>5}  "
          f"p90 {s['dE_p90']:>5}  over-10 {s['pct_over_10']:>5}%  over-23 {s['pct_over_23']:>4}%")
if args.out_json:
    json.dump(stats, open(args.out_json, "w"), indent=1)
    print(f"[sheet] wrote {args.out_json}")
