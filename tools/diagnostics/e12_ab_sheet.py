"""A | B on one view, full size, plus named regions at N x — the sheet a re-roll is judged on.

E12 Ruling 10d/11d: the defect class that decides acceptance here is a LARGE REGION OF THE
WRONG MATERIAL (E07), and no 5x5 statistic can see it — edge-density retention measured
87.6%/102% on a pair the Director rejected. So a re-roll is judged by putting the two
generations side by side at full size and then at the flagged regions' own zoom, and this
file builds exactly that and computes nothing.

The A panel is the REJECTED artifact and it is kept, never tidied away (E08 A23 / E04's
view-7 re-roll precedent): a re-roll's evidence is the pair, not the survivor.

  e12_ab_sheet.py --a PATH --b PATH --a-label ... --b-label ... --out SHEET.png
                  [--region x0,y0,x1,y1:name:SCALE ...]

NAMED_COMPENSATORS: writes only --out and the region files beside it.
EXTERNAL_VERIFIER: emits pictures and no score; the eye is the verifier.
"""
import argparse
import os

from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--a", required=True)
ap.add_argument("--b", required=True)
ap.add_argument("--a-label", default="A")
ap.add_argument("--b-label", default="B")
ap.add_argument("--out", required=True)
ap.add_argument("--width", type=int, default=1792)
ap.add_argument("--region", action="append", default=[],
                help="x0,y0,x1,y1:name:SCALE - cropped from BOTH images, side by side")
args = ap.parse_args()

A = Image.open(args.a).convert("RGB")
B = Image.open(args.b).convert("RGB")
assert A.size == B.size, ("ANDON: %s is %s and %s is %s - an A|B sheet of two different "
                          "frames compares nothing." % (args.a, A.size, args.b, B.size))

W = args.width
h = int(round(W * A.height / A.width))
hdr, gap = 26, 8
os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
sheet = Image.new("RGB", (W, (h + hdr) * 2), (14, 14, 16))
d = ImageDraw.Draw(sheet)
for i, (lab, im) in enumerate(((args.a_label, A), (args.b_label, B))):
    y = i * (h + hdr)
    d.text((6, y + 6), lab, fill=(255, 210, 90))
    sheet.paste(im.resize((W, h), Image.LANCZOS), (0, y + hdr))
sheet.save(args.out)
print("[ab] %s -> %s (%dx%d)" % (os.path.basename(args.a), args.out, sheet.width, sheet.height))

for spec in args.region:
    box, name, scale = spec.split(":")
    x0, y0, x1, y1 = [int(v) for v in box.split(",")]
    s = int(scale)
    w, hh = (x1 - x0) * s, (y1 - y0) * s
    tile = Image.new("RGB", (w * 2 + gap, hh + hdr), (14, 14, 16))
    dr = ImageDraw.Draw(tile)
    for i, (lab, im) in enumerate(((args.a_label, A), (args.b_label, B))):
        c = im.crop((x0, y0, x1, y1)).resize((w, hh), Image.LANCZOS)
        dr.text((i * (w + gap) + 6, 5), "%s  %s  %dx" % (name, lab, s), fill=(255, 210, 90))
        tile.paste(c, (i * (w + gap), hdr))
    p = os.path.join(os.path.dirname(os.path.abspath(args.out)), "AB_%s_%dx.png" % (name, s))
    tile.save(p)
    print("[ab] region %s %d,%d..%d,%d at %dx -> %s" % (name, x0, y0, x1, y1, s,
                                                        os.path.basename(p)))
