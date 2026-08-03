"""Prepare the front render for the paint pass.

Scale + pad ONLY -- no crop, no non-uniform resample -- because the painted result is
going to be projected back onto the same mesh, and project_texture.py fits an
ORTHOGRAPHIC (cx, cy, side) mapping by silhouette. A uniform scale plus symmetric
padding is exactly representable in that model; anything that distorts the figure is not.

Target 768x1344: the native Qwen bucket that produced the Director-approved sharp_B.
"""
from pathlib import Path
from PIL import Image

WORK = Path(r"E:/AI/training/saltroad_bake_fix")
OUT = Path(__file__).parent
SRC = WORK / "turn_proj" / "proj_0.png"
TW, TH = 768, 1344
BG = (87, 87, 92)          # Blender viewport bg 0.34,0.34,0.36 -> sRGB bytes

src = Image.open(SRC).convert("RGB")
w, h = src.size
s = TW / w
nw, nh = TW, round(h * s)
scaled = src.resize((nw, nh), Image.LANCZOS)

canvas = Image.new("RGB", (TW, TH), BG)
ox, oy = (TW - nw) // 2, (TH - nh) // 2
canvas.paste(scaled, (ox, oy))
canvas.save(OUT / "front_padded.png")

print(f"src {w}x{h} -> scaled {nw}x{nh} (x{s:.4f}) -> canvas {TW}x{TH} at offset ({ox},{oy})")
print(f"figure occupies {100*nh/TH:.1f}% of frame height")
print(f"wrote {OUT/'front_padded.png'}")
