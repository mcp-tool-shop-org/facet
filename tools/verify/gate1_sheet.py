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
ap.add_argument("--views", default="4,5,6",
                help="row keys substituted into the patterns below. Integers on the "
                     "character path; any token works, so an elevated camera can be named "
                     "as its job key (y+000_e+40).")
# ---- FIVE COLUMNS (E04 Ruling 1: the owner channel is part of honest presentation).
# Every argument below is additive with a default that reproduces the character path, so
# an existing invocation is unchanged: no --owner means four columns exactly as before.
ap.add_argument("--owner", help="renders of the OWNER map; adds the fifth column. Which "
                                "camera won each texel - the channel provenance is blind "
                                "to, and the one that makes an owner SEAM visible as a "
                                "seam rather than as an unexplained step")
ap.add_argument("--mask-tag", default="w3clay",
                help="filename stem of the exact silhouettes. Was hardcoded to one "
                     "subject's tag, which is the class of thing profiles exist to flush "
                     "out; defaulted to that value so the character path is unchanged")
ap.add_argument("--ref-pattern", default="twin_{k}.png")
ap.add_argument("--asset-pattern", default="final_{k}.png")
ap.add_argument("--prov-pattern", default="prov_{k}.png")
ap.add_argument("--owner-pattern", default="owner_{k}.png")
ap.add_argument("--no-error", action="store_true",
                help="drop the error column AND the reference-derived statistics. For rows "
                     "whose camera has no per-pixel reference - an elevated stroke camera "
                     "has no twin, and a dE against a DIFFERENT camera is not an error, it "
                     "is a number with no referent. Say so rather than computing it")
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


VIEWS = args.views.split(",")
rows = []
stats = {}


def rd(d, pat, k):
    return np.asarray(Image.open(os.path.join(d, pat.format(k=k))).convert("RGB"),
                      dtype=np.float32) / 255.0


for k in VIEWS:
    ref = rd(args.twins, args.ref_pattern, k)
    ast = rd(args.asset, args.asset_pattern, k)
    prv = rd(args.prov, args.prov_pattern, k)
    panels = [(ref * 255).astype(np.uint8), (ast * 255).astype(np.uint8),
              (prv * 255).astype(np.uint8)]
    if args.owner:
        panels.append((rd(args.owner, args.owner_pattern, k) * 255).astype(np.uint8))
    if not args.no_error:
        sil = np.asarray(Image.open(os.path.join(
            args.masks, f"{args.mask_tag}_{k}.png")).convert("L")) > 127
        dE = np.linalg.norm(lab(ast) - lab(ref), axis=-1)
        err = heat(dE)
        err[~sil] = 20                  # outside the silhouette is not the asset's business
        stats[str(k)] = {"figure_px": int(sil.sum()),
                         "dE_median": round(float(np.median(dE[sil])), 2),
                         "dE_mean": round(float(dE[sil].mean()), 2),
                         "dE_p90": round(float(np.percentile(dE[sil], 90)), 2),
                         "pct_over_10": round(float((dE[sil] > 10).mean() * 100), 1),
                         "pct_over_23": round(float((dE[sil] > 23).mean() * 100), 1)}
        panels.append(err)
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
cols = ["REFERENCE", "ASSET (flat)", "PROVENANCE"]
if args.owner:
    cols.append("OWNER")
if not args.no_error:
    cols.append("ERROR (dE heat)")
print(f"[sheet] wrote {args.out}  {sheet.shape[1]}x{sheet.shape[0]}")
print(f"[sheet] columns: {' | '.join(cols)}")
print(f"[sheet] provenance: GREEN = reference/stage1 · BLUE = brush · ORANGE = dilation")
if args.owner:
    print(f"[sheet] owner: one colour per camera, GREY = dilation (no owner)")
if args.no_error:
    print(f"[sheet] NO ERROR COLUMN — these cameras have no per-pixel reference, and a dE "
          f"against a different camera is not an error")
print(f"[sheet] rows: views {', '.join(str(v) for v in VIEWS)}")
for k, s in stats.items():
    print(f"[sheet]   view {k}: dE median {s['dE_median']:>5}  mean {s['dE_mean']:>5}  "
          f"p90 {s['dE_p90']:>5}  over-10 {s['pct_over_10']:>5}%  over-23 {s['pct_over_23']:>4}%")
if args.out_json:
    json.dump(stats, open(args.out_json, "w"), indent=1)
    print(f"[sheet] wrote {args.out_json}")
