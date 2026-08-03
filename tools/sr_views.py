"""View-space SR via spandrel (MIT) + RealESRGAN_x4plus_anime_6B (BSD-3).

Stage B of the locked GLB-texture architecture ([[glb-texture-architecture-lock]]):
SR happens in VIEW space, pre-bake, with a deterministic GAN — never on the UV atlas
(UV-space SR breaks island borders) and never with a diffusion upscaler (drift).
The model is native x4; the final size is Lanczos-resampled to the requested scale.

  sr_views.py --inputs a.png b.png --outdir DIR [--scale 2] [--model PATH]
"""
import argparse
import os

import numpy as np
import torch
from PIL import Image
from spandrel import ModelLoader

ap = argparse.ArgumentParser()
ap.add_argument("--model", default=r"E:\AI-Models\upscalers\RealESRGAN_x4plus_anime_6B.pth")
ap.add_argument("--inputs", nargs="+", required=True)
ap.add_argument("--outdir", required=True)
ap.add_argument("--scale", type=float, default=2.0, help="output scale vs input")
args = ap.parse_args()

model = ModelLoader().load_from_file(args.model).cuda().eval()
os.makedirs(args.outdir, exist_ok=True)
for p in args.inputs:
    im = Image.open(p).convert("RGB")
    x = (torch.from_numpy(np.asarray(im).astype(np.float32) / 255.0)
         .permute(2, 0, 1)[None].cuda())
    with torch.no_grad():
        y = model(x)
    y = (y[0].clamp(0, 1).permute(1, 2, 0).cpu().numpy() * 255).round().astype(np.uint8)
    out = Image.fromarray(y)
    tgt = (round(im.width * args.scale), round(im.height * args.scale))
    if out.size != tgt:
        out = out.resize(tgt, Image.LANCZOS)
    dst = os.path.join(args.outdir, os.path.basename(p))
    out.save(dst)
    print(f"[sr] {os.path.basename(p)} {im.size} -> {out.size}", flush=True)
