"""Bake FORESHORTENING severity into a GLB's atlas, so it can be rendered per view.

Why not project_texture.py's own `atlas_weight.png`: that map is w = smoothstep over
[facing_min, facing_full] = [0.15, 0.45], i.e. every texel within 63 deg of the projection
camera scores a flat 1.0. Rendered, it comes back almost entirely white over the whole
visible figure -- correct for its job (deciding whether to sample at all) and useless for
this one, because the measured 3/4-face defect is FORESHORTENING, and 45-70 deg is exactly
the band w flattens.

The honest quantity is the raw cosine n.z_front. A texel whose normal is 70 deg off the
projection axis received 1/cos(70) = 2.9x fewer source pixels per unit surface area than a
frontal one -- it is stretched by that factor, which is the smear. So:

    facing = clamp(n . z_front, 0, 1)        1.0 = square-on, 0.0 = edge-on/back

Rendered from any view, this gives a per-pixel map of "how much real source detail is
under this pixel" -- the substrate for a graded denoise mask that OPENS where the texture
is stretched and PRESERVES where it is sharp.

  facing_atlas.py --glb <in.glb> --out <facing.glb> [--atlas facing.png]
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import torch
import trimesh
import trimesh.visual
from PIL import Image

sys.path.insert(0, r"E:/AI/sprite-foundry/3d-prerender")
import uv_rasterize                                                   # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--atlas", default=None, help="also write the facing atlas as a PNG")
args = ap.parse_args()

dev = "cuda" if torch.cuda.is_available() else "cpu"
scene = trimesh.load(args.glb)
mesh = scene.to_mesh() if isinstance(scene, trimesh.Scene) else scene
mat = mesh.visual.material
assert mat is not None and mat.baseColorTexture is not None, "GLB has no baked baseColorTexture"
T = mat.baseColorTexture.size[0]

F = torch.as_tensor(np.asarray(mesh.faces), dtype=torch.int64, device=dev)
UV = torch.as_tensor(np.asarray(mesh.visual.uv).copy(), dtype=torch.float32, device=dev)
N = torch.as_tensor(np.asarray(mesh.vertex_normals).copy(), dtype=torch.float32, device=dev)

rast = uv_rasterize.rasterize(UV, F, T)
covered = rast[0, ..., 3] > 0
nrm, _ = uv_rasterize.interpolate(N, rast, F)
nrm = nrm[0]
nrm = nrm / nrm.norm(dim=-1, keepdim=True).clamp(min=1e-8)

# glTF +Z is the axis the front projection was taken along (project_texture.project()).
facing = nrm[..., 2].clamp(0, 1)
facing = facing * covered.float()

img = (facing.cpu().numpy() * 255).astype(np.uint8)
# project_texture writes its debug atlas through to_raster_rows(); match that so this map
# overlays the same atlas. Getting it backwards yields plausible garbage, not a crash.
img = img[::-1].copy()

cov = covered.cpu().numpy()
f = facing.cpu().numpy()[cov]
print(f"[face] covered texels {cov.sum():,}  ({100*cov.mean():.1f}% of atlas)")
for lo, hi, name in [(0.94, 1.01, "  0-20 deg  square-on"),
                     (0.77, 0.94, " 20-40 deg"),
                     (0.50, 0.77, " 40-60 deg  stretching"),
                     (0.17, 0.50, " 60-80 deg  SMEAR"),
                     (0.00, 0.17, " 80-90 deg  edge-on/back")]:
    print(f"[face] {name:26s} {100*((f >= lo) & (f < hi)).mean():5.1f}% of covered texels")

if args.atlas:
    Image.fromarray(img).save(args.atlas)
    print(f"[face] {args.atlas}")

new_mat = mat.copy()
new_mat.baseColorTexture = Image.fromarray(np.dstack([img, img, img]), mode="RGB")
if hasattr(new_mat, "baseColorFactor"):
    new_mat.baseColorFactor = np.array([255, 255, 255, 255], dtype=np.uint8)
mesh.visual = trimesh.visual.TextureVisuals(uv=mesh.visual.uv, material=new_mat)
Path(args.out).parent.mkdir(parents=True, exist_ok=True)
mesh.export(args.out)
print(f"[out ] {args.out} ({Path(args.out).stat().st_size/1e6:.1f} MB)")
