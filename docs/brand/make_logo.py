#!/usr/bin/env python
"""Build facet's logo from the four accepted assets.

The mark is not an invented device. It is the route's own output: the four
assets the Director accepted at Gate 1, each cut from the **exact silhouette**
its dense export ships beside it, composited onto a flat ground. So the logo
makes the same claim the README makes — four subject classes, one route — and a
reader can check it against the record rather than take it on trust.

Deterministic by construction: fixed source paths, fixed cameras, fixed layout,
no sampling and no randomness. Re-running it on the same export trees returns
the same bytes, which is the standard this repo holds its own artifacts to
("a recipe that does not reproduce its output is not a recipe").

    python docs/brand/make_logo.py --out docs/brand/facet-logo.png

The export trees live under E:\\AI\\training and are NOT in git — they are the
recorded artifacts of E04/E08/E12/E14. Point --root elsewhere if they move.
"""

import argparse
import hashlib
import io
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# The four accepted assets, each with the camera the mark uses and the ruling
# that accepted it. Cameras chosen for legibility at logo scale, not for flattery.
SUBJECTS = [
    ("galleon",   "E04_stroke/export/turnaround",  "y+030_e+00", "E04 Ruling 29"),
    ("dragon",    "E13_stroke/export/turnaround",  "y+045_e+00", "E12 Ruling 28"),
    ("character", "../facet_E08/ARMB/export/turnaround", "y+030_e+00", "E08 Amendment 35"),
    ("longsword", "E14_strokes/export/turnaround", "y+000_e+00", "E14 Ruling 32"),
]

GROUND = (19, 19, 24, 255)      # near-black, matches the org's dark landing pages
RULE   = (58, 58, 70, 255)
WORD   = (233, 233, 240, 255)
SUB    = (138, 138, 155, 255)

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG  = r"C:\Windows\Fonts\segoeui.ttf"


def cut(root, rel, yaw):
    """Cut one asset out of its render using the export's exact silhouette.

    Not a threshold and not a key: the dense export ships `silhouette.png` per
    camera, which is the raycast silhouette itself. Keying was retired here
    three times (E01, E08, the twins) and there is no reason to re-introduce it
    when geometry already answered the question.
    """
    d = os.path.join(root, rel, "views", yaw)
    asset = Image.open(os.path.join(d, "asset.png")).convert("RGB")
    sil = np.array(Image.open(os.path.join(d, "silhouette.png")).convert("L"))
    if sil.shape[:2] != (asset.height, asset.width):
        raise SystemExit("ANDON: silhouette %s does not match asset %s at %s"
                         % (sil.shape[:2], (asset.height, asset.width), d))
    out = Image.new("RGBA", asset.size)
    out.paste(asset, (0, 0))
    out.putalpha(Image.fromarray((sil > 127).astype(np.uint8) * 255))
    bb = out.getbbox()
    if bb is None:
        raise SystemExit("ANDON: silhouette at %s is empty — nothing to cut" % d)
    return out.crop(bb)


def fit(img, box):
    """Scale into `box` preserving aspect. Never upscales past 1:1."""
    w, h = img.size
    s = min(box[0] / w, box[1] / h, 1.0)
    if s < 1.0:
        img = img.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    return img


def build(root, size, wordmark=True):
    W = H = size
    pad = int(size * 0.038)
    band = int(size * 0.150) if wordmark else 0
    cell = ((W - pad * 3) // 2, (H - band - pad * 3) // 2)

    canvas = Image.new("RGBA", (W, H), GROUND)
    prov = []
    for i, (name, rel, yaw, ruling) in enumerate(SUBJECTS):
        tile = fit(cut(root, rel, yaw), cell)
        cx = pad + (i % 2) * (cell[0] + pad) + (cell[0] - tile.width) // 2
        cy = pad + (i // 2) * (cell[1] + pad) + (cell[1] - tile.height) // 2
        canvas.alpha_composite(tile, (cx, cy))
        prov.append({"subject": name, "camera": yaw, "tree": rel, "accepted_at": ruling})

    if wordmark:
        d = ImageDraw.Draw(canvas)
        y0 = H - band - pad // 2
        d.line([(pad, y0), (W - pad, y0)], fill=RULE, width=max(1, size // 700))
        f1 = ImageFont.truetype(FONT_BOLD, int(size * 0.088))
        f2 = ImageFont.truetype(FONT_REG, int(size * 0.035))
        d.text((W // 2, y0 + int(band * 0.36)), "facet", font=f1, fill=WORD, anchor="mm")
        d.text((W // 2, y0 + int(band * 0.75)),
               "styled 2D concept  \u2192  textured 3D asset",
               font=f2, fill=SUB, anchor="mm")
    return canvas, prov


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=r"E:\AI\training\facet_next",
                    help="parent of the export trees (default: %(default)s)")
    ap.add_argument("--size", type=int, default=1060,
                    help="square edge in px; brand minimum is 530 (default: %(default)s)")
    ap.add_argument("--out", default="docs/brand/facet-logo.png")
    ap.add_argument("--no-wordmark", action="store_true")
    args = ap.parse_args()

    if args.size < 530:
        raise SystemExit("ANDON: brand minimum is 530x530; asked for %d" % args.size)

    img, prov = build(args.root, args.size, wordmark=not args.no_wordmark)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    img.convert("RGB").save(args.out)

    with open(args.out, "rb") as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()[:16]
    print("wrote %s  %dx%d  sha256:%s" % (args.out, img.width, img.height, sha))
    print(json.dumps(prov, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
