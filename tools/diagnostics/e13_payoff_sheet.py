"""E13 H3 — the judging artifact: clay | A0 | A1 | provenance, one camera, one crop, one scale.

CLAUDE.md's cheapest diagnostic, built BEFORE the metrics are argued about rather than after:
*reference | asset | provenance | error* on one sheet. E07 ran four arms and two gates without
once putting the asset next to the thing it is supposed to look like; when the sheet was
finally built the Director read the whole thesis off panel 2 in a sentence.

Everything on a row is rendered at the SAME camera (the route frame, --fit-axis width) and
cropped to the SAME pixel rect, computed from the measured head box by the route's own
arithmetic. Rendering the clay at the crop camera and the atlas at the route camera would put
two framings in one sheet and invite the eye to compare framing instead of paint.

The provenance column is not decoration. This is the arc's FIRST crop projection, and a
coverage number cannot tell you whether the crop paint reached the region it was generated
for — the ownership map can, and it is the only panel that answers "did the thing under test
actually do anything here".

Standards compliance:
  PIN_PER_STEP — the crop rect derives from head_00003.json by the route's arithmetic, printed.
  ANDON_AUTHORITY — raises if a panel is missing or a size disagrees, rather than composing a
    sheet with a silently mismatched row.
  NAMED_COMPENSATORS — writes PNGs under --out. Undo = delete them.
  EXTERNAL_VERIFIER — it composes; it scores nothing. The Director's eye is the verifier.

  e13_payoff_sheet.py --prep DIR --headbox J --yaw 0 --clay C.png
                      --panel LABEL=render.png [...] --out DIR [--pad 1.25] [--zoom 2]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--headbox", required=True)
ap.add_argument("--yaw", type=float, required=True)
ap.add_argument("--panel", action="append", required=True, metavar="LABEL=PATH",
                help="a full-frame render, in the order they should appear")
ap.add_argument("--out", required=True)
ap.add_argument("--tag", default="sheet")
ap.add_argument("--pad", type=float, default=1.25, help="padding around the head box's rect")
ap.add_argument("--zoom", type=float, default=2.0)
ap.add_argument("--aspect", default="1792,1024")
ap.add_argument("--margin", type=float, default=1.204)
args = ap.parse_args()

AW, AH = [float(x) for x in args.aspect.split(",")]
meta = json.load(open(os.path.join(args.prep, "meta.json")))
maxabs = float(meta["maxabs"])
lo = np.array(meta["lo"], dtype=np.float64) / maxabs * 0.5
hi = np.array(meta["hi"], dtype=np.float64) / maxabs * 0.5
bmid = (lo + hi) / 2
h_ext = float(max(hi[0] - lo[0], hi[1] - lo[1])) * args.margin       # --fit-axis width
v_ext = h_ext * (AH / AW)

hb = json.load(open(args.headbox))
bl, bh = [np.array(v, dtype=np.float64) / maxabs * 0.5 for v in hb["head_box_blender"]]

th = np.radians(args.yaw)
rgt = np.array([np.cos(th), np.sin(th), 0.0])
up = np.array([0.0, 0.0, 1.0])
corners = np.array([[x, y, z] for x in (bl[0], bh[0])
                    for y in (bl[1], bh[1]) for z in (bl[2], bh[2])])
xr = corners @ rgt - bmid @ rgt
zu = corners @ up - bmid @ up
px = (xr / h_ext + 0.5) * AW - 0.5
py = (0.5 - zu / v_ext) * AH - 0.5
cx, cy = (px.min() + px.max()) / 2, (py.min() + py.max()) / 2
hw = (px.max() - px.min()) / 2 * args.pad
hh = (py.max() - py.min()) / 2 * args.pad
rect = (max(0, int(cx - hw)), max(0, int(cy - hh)),
        min(int(AW), int(cx + hw)), min(int(AH), int(cy + hh)))
print(f"[sheet] yaw {args.yaw:+.0f}: head box -> route-frame rect {rect} "
      f"({rect[2]-rect[0]}x{rect[3]-rect[1]} px, pad {args.pad:g}), shown at {args.zoom:g}x",
      flush=True)

panels = []
for spec in args.panel:
    k, _, p = spec.partition("=")
    if not (p and os.path.exists(p)):
        raise AssertionError(f"ANDON: --panel {k}: no such file {p}")
    im = Image.open(p).convert("RGB")
    if not (im.size == (int(AW), int(AH))):
        raise AssertionError(
            f"ANDON: {k} is {im.size}, not the route frame {(int(AW), int(AH))} — a sheet whose "
            f"rows are at different framings compares framing, not paint")
    c = im.crop(rect)
    c = c.resize((int(c.width * args.zoom), int(c.height * args.zoom)), Image.LANCZOS)
    panels.append((k, c))

W = sum(p.width for _, p in panels) + 8 * (len(panels) + 1)
BAR = 34
H = panels[0][1].height + BAR + 16
sheet = Image.new("RGB", (W, H), (18, 18, 20))
d = ImageDraw.Draw(sheet)
x = 8
for k, p in panels:
    sheet.paste(p, (x, BAR + 8))
    d.text((x + 6, 10), k, fill=(235, 235, 240))
    x += p.width + 8
os.makedirs(args.out, exist_ok=True)
path = os.path.join(args.out, f"{args.tag}_y{int(args.yaw)}_{args.zoom:g}x.png")
sheet.save(path)
print(f"[sheet] wrote {path}  ({sheet.width}x{sheet.height}) — DONE (no verdict attached)",
      flush=True)
