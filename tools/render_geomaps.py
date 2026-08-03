"""LICENSE-FREE geometry-conditioning renderer for MV-Adapter ig2mv.

Replaces the repo's nvdiffrast leg (NVIDIA 1-way NON-COMMERCIAL licence — the exact
dependency this studio already purged once, sprite-foundry PR #3). Produces the same
position/normal conditioning maps via open3d raycasting (Apache-2.0) + numpy. The
whole path is now: SDXL (OpenRAIL++) + MV-Adapter (open) + our renderer — nothing
non-commercial anywhere.

Conventions replicated from mvadapter.utils.mesh_utils (verified by pixel-diff against
the maps the nvdiffrast path saved on 2026-08-03):
  mesh:    load(force='mesh'), NO centering, rescale vertices/|v|.max()*0.5,
           axis remap up=+y front=+x (std: x=x, y=-z, z=y), vertex normals remapped too
  cameras: ortho, pos = d*(cos(el)cos(az), cos(el)sin(az), sin(el)) in std frame,
           lookat origin, up +Z, bounds +-0.55, d=1.8,
           elevations [0,0,0,0,89.99,-89.99], azimuths [-90,0,90,180,90,90]
  maps:    pos_std + 0.5 -> RGB, normal_std/2 + 0.5 -> RGB, background 0.5 grey
           (normal_background=0.0 pre-encoding)

  render_geomaps.py --glb mesh.glb --out DIR [--res 768]
Writes pos_{i}.png / nor_{i}.png per view + control tensors as ctrl.npy (H,W,6 per view).
"""
import argparse
import math
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--res", type=int, default=768)
ap.add_argument("--elevations", default="0,0,0,0,89.99,-89.99")
ap.add_argument("--azimuths", default="-90,0,90,180,90,90")
ap.add_argument("--distance", type=float, default=1.8)
ap.add_argument("--bound", type=float, default=0.55)
args = ap.parse_args()

os.makedirs(args.out, exist_ok=True)

# --- mesh, exactly like load_mesh(rescale=True) ---
scene = trimesh.load(args.glb, force="mesh", process=False)
if isinstance(scene, trimesh.Scene):
    m = trimesh.Trimesh()
    for g in scene.geometry.values():
        m = trimesh.util.concatenate([m, g])
else:
    m = scene
v = np.asarray(m.vertices, dtype=np.float64)
vn = np.asarray(m.vertex_normals, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
max_scale = np.abs(v).max()
v = v / max_scale * 0.5
# axis remap: std x = mesh x, std y = -mesh z, std z = mesh y
remap = lambda a: np.stack([a[:, 0], -a[:, 2], a[:, 1]], axis=1)
v = remap(v)
vn = remap(vn)
vn /= np.linalg.norm(vn, axis=1, keepdims=True) + 1e-12

rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))

elevs = [float(x) for x in args.elevations.split(",")]
azims = [float(x) for x in args.azimuths.split(",")]
res, b = args.res, args.bound

for i, (el_d, az_d) in enumerate(zip(elevs, azims)):
    el, az = math.radians(el_d), math.radians(az_d)
    cam = np.array([math.cos(el) * math.cos(az),
                    math.cos(el) * math.sin(az),
                    math.sin(el)]) * args.distance
    lookat = -cam / np.linalg.norm(cam)
    up = np.array([0.0, 0.0, 1.0])
    right = np.cross(lookat, up)
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, lookat)
    up /= np.linalg.norm(up) + 1e-12

    # ortho ray grid: pixel centres, x right, y up; NDC v flips for image rows
    xs = (np.arange(res) + 0.5) / res * (2 * b) - b
    ys = b - (np.arange(res) + 0.5) / res * (2 * b)
    gx, gy = np.meshgrid(xs, ys)
    origins = (cam[None, None, :]
               + gx[..., None] * right[None, None, :]
               + gy[..., None] * up[None, None, :])
    dirs = np.broadcast_to(lookat, origins.shape)
    rays = o3d.core.Tensor(
        np.concatenate([origins, dirs], axis=-1).reshape(-1, 6).astype(np.float32))
    ans = rs.cast_rays(rays)
    t_hit = ans["t_hit"].numpy().reshape(res, res)
    prim = ans["primitive_ids"].numpy().reshape(res, res)
    buv = ans["primitive_uvs"].numpy().reshape(res, res, 2)
    hit = np.isfinite(t_hit)

    pos = np.zeros((res, res, 3), dtype=np.float64)
    nor = np.zeros((res, res, 3), dtype=np.float64)
    if hit.any():
        tri = f[prim[hit]]
        w_u = buv[hit][:, 0:1]
        w_v = buv[hit][:, 1:2]
        w0 = 1.0 - w_u - w_v
        pos[hit] = w0 * v[tri[:, 0]] + w_u * v[tri[:, 1]] + w_v * v[tri[:, 2]]
        n = w0 * vn[tri[:, 0]] + w_u * vn[tri[:, 1]] + w_v * vn[tri[:, 2]]
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        nor[hit] = n

    pos_img = np.clip(pos + 0.5, 0, 1)
    nor_img = np.clip(nor / 2 + 0.5, 0, 1)
    pos_img[~hit] = 0.5
    nor_img[~hit] = 0.5
    Image.fromarray((pos_img * 255).round().astype(np.uint8)).save(
        f"{args.out}/pos_{i}.png")
    Image.fromarray((nor_img * 255).round().astype(np.uint8)).save(
        f"{args.out}/nor_{i}.png")
    print(f"[geomaps] view {i} el {el_d} az {az_d}: {int(hit.sum()):,} hits", flush=True)

ctrl = []
for i in range(len(elevs)):
    p = np.asarray(Image.open(f"{args.out}/pos_{i}.png"), dtype=np.float32) / 255.0
    n = np.asarray(Image.open(f"{args.out}/nor_{i}.png"), dtype=np.float32) / 255.0
    ctrl.append(np.concatenate([p, n], axis=-1))
np.save(f"{args.out}/ctrl.npy", np.stack(ctrl))
print(f"[geomaps] wrote {args.out}/ctrl.npy", flush=True)
