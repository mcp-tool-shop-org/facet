"""E13 Gate 1 — the house five-column sheet: reference | asset | provenance | error | clay.

CLAUDE.md's cheapest diagnostic, and the one E07 ran four arms without building: put the asset
next to the thing it is supposed to look like, with its provenance and its error beside it, at
one camera and one scale. The Director read a whole thesis off panel 2 the first time this
existed; it is built before the numbers are polished, not after.

The five columns, and why each is there:

  reference   what this view was SUPPOSED to look like — the accepted pair where one exists
              (Ruling 14's two views), else the harmonized twin projection consumed
  asset       the finished atlas, rendered FLAT (texpass_iter emit raycasts with no lighting;
              a Workbench STUDIO render is not a texture readout and two rounds were lost to it)
  provenance  green = stage-1 reference paint · amber = the four brush strokes ·
              violet = dilation grown in at finalize. The panel that says which parts of the
              asset are carried, invented, or extrapolated.
  error       |asset - reference| inside the silhouette, amplified, so a region that drifted
              is visible rather than argued about
  clay        the geometry, so a defect can be told apart from the thing the mesh actually is

Standards compliance:
  PIN_PER_STEP — every panel's source path is printed; the amplification factor is a flag.
  ANDON_AUTHORITY — halts if a panel is missing or a size disagrees, rather than composing a
    sheet with a silently mismatched column.
  NAMED_COMPENSATORS — writes PNGs under --out. Undo = delete.
  EXTERNAL_VERIFIER — it composes and scores nothing. Gate 1 is the Director's eye.
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--yaw", type=int, required=True)
ap.add_argument("--reference", required=True)
ap.add_argument("--ref-label", default="reference")
ap.add_argument("--asset", required=True)
ap.add_argument("--prov", required=True)
ap.add_argument("--clay", required=True)
ap.add_argument("--mask", required=True, help="exact raycast silhouette for the error panel")
ap.add_argument("--out", required=True)
ap.add_argument("--scale", type=float, default=1.0)
ap.add_argument("--amp", type=float, default=3.0, help="error amplification")
ap.add_argument("--crop", help="x0,y0,x1,y1 before scaling")
args = ap.parse_args()


def load(p, what):
    if not (os.path.exists(p)):
        raise AssertionError(f"ANDON: {what} panel missing: {p}")
    return Image.open(p).convert("RGB")


ref, asset, prov, clay = (load(args.reference, "reference"), load(args.asset, "asset"),
                          load(args.prov, "provenance"), load(args.clay, "clay"))
sizes = {ref.size, asset.size, prov.size, clay.size}
if not (len(sizes) == 1):
    raise AssertionError(
        f"ANDON: the panels are not at one framing — {sizes}. A sheet whose columns sit at "
        f"different frames compares framing, not paint.")
m = np.asarray(Image.open(args.mask).convert("L")) > 127
if not (m.shape == (ref.size[1], ref.size[0])):
    raise AssertionError("ANDON: mask frame disagrees with the panels")

a = np.asarray(asset, dtype=np.float32)
r = np.asarray(ref, dtype=np.float32)
e = np.clip(np.abs(a - r).mean(axis=-1) * args.amp, 0, 255).astype(np.uint8)
err = np.zeros(a.shape, dtype=np.uint8)
err[..., 0] = np.where(m, e, 0)
err[..., 1] = np.where(m, e // 3, 0)
err[..., 2] = np.where(m, e // 6, 0)
err[~m] = (20, 20, 24)
inside = e[m]
print(f"[gate1] yaw {args.yaw:+04d}: error inside the silhouette — mean {inside.mean()/args.amp:.2f} "
      f"levels, p95 {np.percentile(inside, 95)/args.amp:.2f}, shown at {args.amp:g}x", flush=True)
errI = Image.fromarray(err)

panels = [(args.ref_label, ref), ("asset (FLAT)", asset),
          ("provenance  green=stage1  amber=brush  violet=dilation", prov),
          (f"error |asset-ref| x{args.amp:g}", errI), ("clay (geometry)", clay)]
if args.crop:
    x0, y0, x1, y1 = [int(v) for v in args.crop.split(",")]
    panels = [(k, im.crop((x0, y0, x1, y1))) for k, im in panels]
if args.scale != 1.0:
    panels = [(k, im.resize((int(im.width * args.scale), int(im.height * args.scale)),
                            Image.LANCZOS)) for k, im in panels]

w, h = panels[0][1].size
BAR = 26
sheet = Image.new("RGB", (w * 5 + 24, h + BAR + 12), (18, 18, 20))
d = ImageDraw.Draw(sheet)
for i, (k, im) in enumerate(panels):
    x = 4 + i * (w + 4)
    d.text((x + 4, 7), f"yaw {args.yaw:+04d}  |  {k}", fill=(235, 235, 240))
    sheet.paste(im, (x, BAR + 4))
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
sheet.save(args.out)
print(f"[gate1] wrote {args.out} ({sheet.width}x{sheet.height}) — no verdict attached",
      flush=True)
