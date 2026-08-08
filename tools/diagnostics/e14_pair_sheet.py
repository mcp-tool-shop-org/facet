"""The styled pair's acceptance sheet: REFERENCE | CONTROL | ASSET, plus the hilt at zoom.

CLAUDE.md names this the cheapest diagnostic in the repo and records that E07 ran four arms
and two gates without once putting the asset next to the thing it is supposed to look like.
So this is built BEFORE any conclusion is drawn about the pair, not after.

The three panels, left to right, and what each is FOR:

  REFERENCE  the profile-rendered clay view - the GEOMETRY the asset is supposed to be. Not
             a colour reference: nothing in this route has ever seen this sword in colour,
             which is the whole reason the pair exists.
  CONTROL    the control image actually submitted, through the RULED canny pair 0.10/0.25.
             This is the provenance panel: what the generator was constrained by. E07's
             lesson is that a number tells you a region is wrong and the provenance panel
             tells you what it was supposed to be.
  ASSET      the generated view at full size.

THE HILT STRIP is separate and at 4x because S-hilt-scale pre-registers the hilt at roughly
7% of frame pixels, and because L5 (the gem) is below any area floor by construction at route
frames - the D8 lesson says no numeric gate may be armed on it and landing is judged by eye
at the hilt crop. This file produces that crop; it does not judge it.

  e14_pair_sheet.py --render R.png --control C.png --pair P.png --label "..." --out S.png
                    [--hilt-rows 60,420] [--hilt-scale 4]

Standards compliance: PIN_PER_STEP - every input path is an argument and is captioned into
the sheet. UNCERTAINTY_GATED_HUMANS - the sheet IS the gate; it ranks nothing and captions
nothing as good or bad. NAMED_COMPENSATORS - writes one PNG.
"""
import argparse
import os

from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--render", required=True)
ap.add_argument("--control", required=True)
ap.add_argument("--pair", required=True)
ap.add_argument("--label", required=True)
ap.add_argument("--hilt-rows", default="60,420")
ap.add_argument("--hilt-scale", type=int, default=4)
ap.add_argument("--out", required=True)
args = ap.parse_args()

R = Image.open(args.render).convert("RGB")
C = Image.open(args.control).convert("RGB")
P = Image.open(args.pair).convert("RGB")
for nm, im in (("control", C), ("pair", P)):
    if im.size != R.size:
        raise SystemExit("ANDON: %s is %s but the render is %s - a sheet that rescales one "
                         "panel is comparing two different framings" % (nm, im.size, R.size))

W, H = R.size
pad, cap = 14, 30
panels = [("REFERENCE  profile clay render (GEOMETRY, not colour)", R),
          ("CONTROL  submitted, ruled canny 0.10/0.25", C),
          ("ASSET  generated", P)]
sw = pad + len(panels) * (W + pad)
sh = cap * 2 + pad + H + pad
sheet = Image.new("RGB", (sw, sh), (16, 16, 18))
d = ImageDraw.Draw(sheet)
d.text((pad, 8), args.label, fill=(255, 205, 80))
x = pad
for t, im in panels:
    sheet.paste(im, (x, cap * 2))
    d.text((x + 2, cap + 4), t, fill=(200, 200, 210))
    x += W + pad
sheet.save(args.out)
print("[sheet] wrote %s  %dx%d" % (args.out, sheet.width, sheet.height))

y0, y1 = (int(v) for v in args.hilt_rows.split(","))
s = args.hilt_scale
hp = []
for t, im in panels:
    hp.append((t.split("  ")[0], im.crop((0, y0, W, y1)).resize(
        (W * s, (y1 - y0) * s), Image.NEAREST)))
hw = pad + len(hp) * (hp[0][1].width + pad)
hh = cap + pad + hp[0][1].height + pad
hs = Image.new("RGB", (hw, hh), (16, 16, 18))
hd = ImageDraw.Draw(hs)
x = pad
for t, im in hp:
    hs.paste(im, (x, cap))
    hd.text((x + 4, 8), "%s  HILT %dx  rows %d-%d" % (t, s, y0, y1), fill=(255, 205, 80))
    x += im.width + pad
hout = os.path.splitext(args.out)[0] + "_HILT.png"
hs.save(hout)
print("[sheet] wrote %s  %dx%d" % (hout, hs.width, hs.height))
