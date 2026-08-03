"""Does the ControlNet hint actually SEE the green apron, the fingers, and the 3/4 face?

The restylize deletes the green apron in every output view while it is present in every
input render. Before tuning any sampler setting, ask what the control branch is even being
told. This replicates ComfyUI's core Canny node EXACTLY -- kornia.filters.canny at the
pipeline's own thresholds -- and crops the three regions in question.

    kornia.filters.canny(img.movedim(-1,1), low, high)[1]      <- ComfyUI Canny node

Runs on CPU. No models loaded, no VRAM touched.
"""
import sys
from pathlib import Path

import numpy as np
import torch
import kornia
from PIL import Image, ImageDraw

WORK = Path(r"E:/AI/training/saltroad_bake_fix")
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
LOW, HIGH = 0.235, 0.588          # the pipeline's own canny thresholds

VIEWS = {"7": "turn_proj/proj_7.png", "0": "turn_proj/proj_0.png", "1": "turn_proj/proj_1.png"}

# regions of interest, as fractions of (w, h) -- x0, y0, x1, y1
ROI = {
    "face":  (0.36, 0.07, 0.66, 0.24),
    "apron": (0.22, 0.36, 0.80, 0.62),
    "hand":  (0.55, 0.48, 0.80, 0.62),
}


def canny(img: Image.Image) -> np.ndarray:
    """ComfyUI's Canny node, exactly: kornia canny on [0,1] RGB, take output[1]."""
    a = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    t = torch.from_numpy(a)[None]                       # 1 H W C, as LoadImage gives it
    edges = kornia.filters.canny(t.movedim(-1, 1), LOW, HIGH)[1]
    return (edges[0, 0].numpy() * 255).astype(np.uint8)


def crop(arr_or_img, box, w, h):
    x0, y0, x1, y1 = box
    b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
    im = arr_or_img if isinstance(arr_or_img, Image.Image) else Image.fromarray(arr_or_img)
    return im.crop(b)


def main():
    rows = []
    stats = []
    for vname, rel in VIEWS.items():
        src = Image.open(WORK / rel).convert("RGB")
        w, h = src.size
        e = canny(src)
        Image.fromarray(e).save(OUT / f"canny_full_{vname}.png")

        # measure edge density inside each ROI -- a region the control cannot see is a
        # region diffusion is free to invent.
        for rname, box in ROI.items():
            sub = np.asarray(crop(e, box, w, h))
            stats.append((vname, rname, 100.0 * (sub > 127).mean()))

        for rname, box in ROI.items():
            rows.append((f"view {vname} / {rname}",
                         crop(src, box, w, h).convert("RGB"),
                         crop(e, box, w, h).convert("RGB")))

    # contact sheet: source | canny, one pair per row, scaled to a common width
    CW = 520
    tiles = []
    for label, a, b in rows:
        sc = CW / a.width
        a2 = a.resize((CW, int(a.height * sc)), Image.LANCZOS)
        b2 = b.resize((CW, int(b.height * sc)), Image.NEAREST)
        tiles.append((label, a2, b2))
    gap, hdr = 8, 20
    W = CW * 2 + gap
    H = sum(t[1].height + hdr + gap for t in tiles)
    sheet = Image.new("RGB", (W, H), (18, 18, 20))
    d = ImageDraw.Draw(sheet)
    y = 0
    for label, a2, b2 in tiles:
        d.text((4, y + 5), f"{label}   (left: render   right: CANNY 0.235/0.588)", fill=(255, 210, 90))
        y += hdr
        sheet.paste(a2, (0, y)); sheet.paste(b2, (CW + gap, y))
        y += a2.height + gap
    sheet.save(OUT / "CANNY_PROBE.png")

    print(f"{'view':>5} {'region':>7} {'edge px %':>10}")
    for v, r, p in stats:
        print(f"{v:>5} {r:>7} {p:>9.2f}%")
    print(f"\nwrote {OUT/'CANNY_PROBE.png'}")


if __name__ == "__main__":
    main()
