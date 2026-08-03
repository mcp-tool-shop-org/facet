"""TEXTURE-SPACE PASS — finalize: classical dilation fill for the residual holes.

Remaining holes after the brush loop are undersides, crevices and the blade flank
(excluded from diffusion BY POLICY — thin hard-surface props take dilated projected
colour, never invented content). Fill = iterative 4-neighbour average from styled
texels, valid-island-constrained, then mean fallback + gutter dilation for mips.

  texpass_finalize.py --state DIR --prep DIR --out atlas_final.png
"""
import argparse
import os

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--state", required=True)
ap.add_argument("--prep", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

atlas = np.asarray(Image.open(os.path.join(args.state, "atlas.png")).convert("RGB"),
                   dtype=np.float32) / 255.0
holes = np.asarray(Image.open(os.path.join(args.state, "holes.png")).convert("L"),
                   dtype=np.float32) / 255.0 > 0.5
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
RES = atlas.shape[0]
have = valid & ~holes
img = atlas.copy()
print(f"[finalize] filling {int((valid & holes).sum()):,} hole texels", flush=True)
grown = have.copy()
for step in range(96):
    todo = valid & ~grown
    if not todo.any() and step >= 16:      # extra 16 = gutter dilation beyond islands
        break
    acc = np.zeros((RES, RES, 3), dtype=np.float32)
    cnt = np.zeros((RES, RES), dtype=np.float32)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb_v = np.roll(grown, (dy, dx), axis=(0, 1))
        acc += np.roll(img, (dy, dx), axis=(0, 1)) * nb_v[..., None]
        cnt += nb_v
    fill = ~grown & (cnt > 0)
    img[fill] = acc[fill] / cnt[fill][..., None]
    grown |= fill
left = int((valid & ~grown).sum())
if left:
    img[valid & ~grown] = img[have].mean(axis=0)
print(f"[finalize] done, {left:,} texels took mean fallback", flush=True)
var = float(img[valid].var())
assert var > 0.001, "ANDON: final atlas uniform"
Image.fromarray((img * 255).round().astype(np.uint8)).save(args.out)
print(f"[finalize] wrote {args.out}  var {var:.5f}", flush=True)
