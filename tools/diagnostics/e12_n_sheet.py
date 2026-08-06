"""N generations of ONE view, stacked full size, plus named regions at N x - and no number.

`e12_ab_sheet.py` asserts exactly two panels, which is right for a re-roll (a re-roll's
evidence is the pair). A PROGRESSION is a different object: handoff 6 has three generations of
view 5 - two under the old palette at two seeds, one under the corrected palette at the first
of those seeds - and the thing a reader needs to see is that the SEED move and the CANON move
are different moves. Two panels cannot show that; three can.

Every panel is kept, including the rejected ones (E08 A23 / E04's view-7 re-roll precedent).
A rejected artifact is evidence, never a baseline to score against (E12 handoff 6 dispatch).

  e12_n_sheet.py --panel LABEL=PATH --panel LABEL=PATH ... --out SHEET.png
                 [--region x0,y0,x1,y1:name:SCALE ...]

Every panel must share one frame; differing frames raise, because a progression across two
frames compares nothing. Region crops are emitted as one strip per region, panels left to
right in the order given.

NAMED_COMPENSATORS: writes only --out and the region strips beside it; undo = delete them.
EXTERNAL_VERIFIER: emits pictures and no score - the eye is the verifier (E12 Ruling 10d).
"""
import argparse
import os

from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--panel", action="append", required=True, help="LABEL=PATH, repeatable, in order")
ap.add_argument("--out", required=True)
ap.add_argument("--width", type=int, default=1792)
ap.add_argument("--region", action="append", default=[],
                help="x0,y0,x1,y1:name:SCALE - cropped from EVERY panel, left to right")
args = ap.parse_args()

PANELS = [s.split("=", 1) for s in args.panel]
if len(PANELS) < 2:
    raise SystemExit("ANDON: a progression needs at least two panels.")
ims = [(lab, Image.open(p).convert("RGB")) for lab, p in PANELS]
sizes = {im.size for _, im in ims}
if len(sizes) != 1:
    raise SystemExit("ANDON: panels have %d different frames (%s) - a progression across two "
                     "frames compares nothing. No sheet written." % (len(sizes), sorted(sizes)))

W = args.width
cap = 30
h = int(round(W * ims[0][1].height / ims[0][1].width))
sheet = Image.new("RGB", (W, (h + cap) * len(ims)), (14, 14, 16))
d = ImageDraw.Draw(sheet)
for i, (lab, im) in enumerate(ims):
    y = i * (h + cap)
    d.text((6, y + 9), "%d/%d   %s" % (i + 1, len(ims), lab), fill=(120, 220, 255))
    sheet.paste(im.resize((W, h), Image.LANCZOS), (0, y + cap))
os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
sheet.save(args.out)
print("[n-sheet] %d panels -> %s  (%dx%d)" % (len(ims), args.out, sheet.width, sheet.height))

for spec in args.region:
    box, name, scale = spec.rsplit(":", 2)
    x0, y0, x1, y1 = [int(t) for t in box.split(",")]
    s = int(scale)
    cw, ch = (x1 - x0) * s, (y1 - y0) * s
    strip = Image.new("RGB", (cw * len(ims) + 4 * (len(ims) - 1), ch + cap), (14, 14, 16))
    sd = ImageDraw.Draw(strip)
    for i, (lab, im) in enumerate(ims):
        x = i * (cw + 4)
        sd.text((x + 6, 9), "%d  %s" % (i + 1, lab), fill=(255, 210, 90))
        strip.paste(im.crop((x0, y0, x1, y1)).resize((cw, ch), Image.LANCZOS), (x, cap))
    p = os.path.join(os.path.dirname(os.path.abspath(args.out)), "%s_%dx.png" % (name, s))
    strip.save(p)
    print("[region] %-12s %d,%d..%d,%d at %dx -> %s" % (name, x0, y0, x1, y1, s,
                                                        os.path.basename(p)))
