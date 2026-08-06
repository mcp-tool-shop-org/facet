"""clay | control | styled, one row per view, full size — the sheet that serves the eye.

E12 Ruling 10d: at a style gate the structural channel IS the eye, and no 5x5 statistic
substitutes for it (measured twice: edge-density retention read 87.6%/102% on a pair the
Director rejected). CLAUDE.md's own rule is older and blunter — *beside the reference, with
provenance* — and E07 ran four arms and two gates without once putting the asset next to the
thing it is supposed to look like.

So this file builds the one artifact a style ruling needs and does not compute a score. The
three columns are the three things that can be wrong and they are wrong in different places:
the CLAY is what the geometry actually is, the CONTROL is what the generator was told about
it, and the STYLED is what came back. A defect visible in column 3 and absent from column 2
is the generator inventing; a defect present in column 2 is ours.

  e12_pair_sheet.py --clay DIR --control DIR --styled K=PATH ... --tag dragonclay
                    --views 1,5 --out SHEET.png [--crop K:x0,y0,x1,y1:name:SCALE]

NAMED_COMPENSATORS: writes only the files named by --out and --crop; undo = delete them.
EXTERNAL_VERIFIER: emits no number and adopts nothing — it exists so a human judges the
artifact rather than believing a metric about it.
"""
import argparse
import os

from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--clay", required=True)
ap.add_argument("--control", required=True)
ap.add_argument("--styled", action="append", required=True, help="VIEW=PATH, repeatable")
ap.add_argument("--tag", default="dragonclay")
ap.add_argument("--views", default="1,5")
ap.add_argument("--out", required=True)
ap.add_argument("--width", type=int, default=1792, help="per-panel width in the sheet")
ap.add_argument("--label", action="append", default=[], help="VIEW=TEXT row caption")
ap.add_argument("--crop", action="append", default=[],
                help="VIEW:x0,y0,x1,y1:name:SCALE - a zoomed crop of the STYLED output, its "
                     "own file. The Director's zoom, not a contact sheet.")
args = ap.parse_args()

VIEWS = [v.strip() for v in args.views.split(",") if v.strip()]
STYLED = dict(s.split("=", 1) for s in args.styled)
LABEL = dict(s.split("=", 1) for s in args.label)
os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)

rows = []
for v in VIEWS:
    clay = Image.open(os.path.join(args.clay, "%s_%s.png" % (args.tag, v))).convert("RGB")
    ctrl = Image.open(os.path.join(args.control, "%s_%s_control.png"
                                   % (args.tag, v))).convert("RGB")
    sty = Image.open(STYLED[v]).convert("RGB")
    rows.append((v, [("clay  (Workbench, --clay, profile-framed)", clay),
                     ("control  (canny + morphological contour)", ctrl),
                     ("styled  (Comfy Cloud, NO LoRA)", sty)]))

W = args.width
hdr, cap, gap = 26, 30, 8
h = int(round(W * rows[0][1][0][1].height / rows[0][1][0][1].width))
sheet = Image.new("RGB", (W * 3 + gap * 2, (h + hdr + cap) * len(rows)), (14, 14, 16))
d = ImageDraw.Draw(sheet)
for i, (v, tiles) in enumerate(rows):
    y = i * (h + hdr + cap)
    d.text((6, y + 6), "view %s   %s" % (v, LABEL.get(v, "")), fill=(120, 220, 255))
    for j, (lab, im) in enumerate(tiles):
        x = j * (W + gap)
        d.text((x + 6, y + cap + 4), lab, fill=(255, 210, 90))
        sheet.paste(im.resize((W, h), Image.LANCZOS), (x, y + cap + hdr))
sheet.save(args.out)
print("[sheet] %d views x 3 panels -> %s  (%dx%d)"
      % (len(rows), args.out, sheet.width, sheet.height))

for spec in args.crop:
    v, box, name, scale = spec.split(":")
    x0, y0, x1, y1 = [int(t) for t in box.split(",")]
    s = int(scale)
    im = Image.open(STYLED[v.strip()]).convert("RGB").crop((x0, y0, x1, y1))
    im = im.resize(((x1 - x0) * s, (y1 - y0) * s), Image.LANCZOS)
    p = os.path.join(os.path.dirname(os.path.abspath(args.out)),
                     "%s_view%s_%dx.png" % (name, v.strip(), s))
    im.save(p)
    print("[crop] %s  view %s  %d,%d..%d,%d at %dx -> %s"
          % (name, v, x0, y0, x1, y1, s, os.path.basename(p)))
