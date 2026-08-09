"""E12 Gate 0 — compose one candidate's head crops into ONE artifact, at full size.

Split out of `e12_head_render.py` because Blender's bundled Python carries no Pillow; the
render happens under Blender and the composition under the pipeline's own interpreter.

Full size, never a thumbnail: the defects that decide acceptance in this repo are invisible
at contact-sheet scale, and a head is exactly where the Director's zoom goes. The caption
states what the frame IS — a measured box, not an inherited rect — and that the sheet ranks
nothing.

Standards compliance: NAMED_COMPENSATORS — writes one PNG, undo = delete it.
EXTERNAL_VERIFIER — it lays images out; it scores nothing.

  e12_head_sheet.py --images a.png b.png c.png --labels "yaw +0" ... --out sheet.png
                    [--caption "..."] [--sub "..."]
"""
import argparse
import os

from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--images", nargs="+", required=True)
ap.add_argument("--labels", nargs="*", default=None)
ap.add_argument("--caption", default="")
ap.add_argument("--sub", default="--clay: GEOMETRY only, there is no texture on a raw "
                                 "reconstruction. The frame is this mesh's MEASURED head "
                                 "box, not an inherited face rect. THIS SHEET RANKS NOTHING.")
ap.add_argument("--out", required=True)
args = ap.parse_args()

labels = args.labels or [os.path.basename(p) for p in args.images]
if not (len(labels) == len(args.images)):
    raise AssertionError("ANDON: --labels count must match --images count")
ims = [Image.open(p).convert("RGB") for p in args.images]
w, h = ims[0].size
for p, im in zip(args.images, ims):
    if not (im.size == (w, h)):
        raise AssertionError("ANDON: %s is %s, expected %s" % (p, im.size, (w, h)))

TOP, PAD = 46, 8
sheet = Image.new("RGB", (len(ims) * w + (len(ims) - 1) * PAD, TOP + h), (16, 16, 18))
d = ImageDraw.Draw(sheet)
d.text((10, 10), args.caption or os.path.basename(args.out), fill=(240, 240, 240))
d.text((10, 26), args.sub, fill=(185, 190, 200))
for i, (im, lab) in enumerate(zip(ims, labels)):
    x = i * (w + PAD)
    sheet.paste(im, (x, TOP))
    d.text((x + 8, TOP + 8), lab, fill=(230, 230, 120))
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
sheet.save(args.out)
print("[headsheet] wrote %s  %dx%d" % (args.out, *sheet.size))
