"""Transfer a texture from a DENSE textured mesh onto a RETOPO'd mesh's new atlas.

Replaces Blender's selected-to-active ray bake, which returned a mostly-black atlas
on this asset (measured 2026-08-04): the source is thousands of disconnected shells,
so rays cast along the low mesh's smooth normals miss into empty space.

Nearest-surface transfer cannot miss: for every texel of the NEW atlas take its 3D
position (from the prep pass' EMIT position bake), find the closest point on the
dense mesh (open3d, exact), read that triangle's barycentric UV, and sample the dense
atlas there. Colour is copied byte-for-byte in sRGB — no linear round trip.

  resample_atlas.py --prep SMART_PREP_DIR --dense-glb dense.glb --dense-atlas a.png
                    --out new_atlas.png
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True, help="bake_hero_prep output for the NEW mesh")
ap.add_argument("--dense-glb", required=True, help="dense mesh carrying the good UVs")
ap.add_argument("--dense-atlas", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
pos_e = np.load(os.path.join(args.prep, "pos.npy"))
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
valid = mask.reshape(-1)
P = pos_e.reshape(-1, 3)[valid].astype(np.float64) * (hi - lo) + lo
print(f"[resample] {P.shape[0]:,} texels to fill on the new atlas", flush=True)

m = trimesh.load(args.dense_glb, force="mesh", process=False)
V = np.asarray(m.vertices, dtype=np.float64)
F = np.asarray(m.faces, dtype=np.int64)
UV = np.asarray(m.visual.uv, dtype=np.float64)
assert UV.shape[0] == V.shape[0], "ANDON: dense mesh UVs missing/mismatched"
print(f"[resample] dense source: {F.shape[0]:,} faces with UVs", flush=True)

scene = o3d.t.geometry.RaycastingScene()
scene.add_triangles(o3d.core.Tensor(V.astype(np.float32)),
                    o3d.core.Tensor(F.astype(np.uint32)))
ans = scene.compute_closest_points(o3d.core.Tensor(P.astype(np.float32)))
tri_id = ans["primitive_ids"].numpy().astype(np.int64)
bary = ans["primitive_uvs"].numpy().astype(np.float64)
hit_pt = ans["points"].numpy().astype(np.float64)
dist = np.linalg.norm(hit_pt - P, axis=1)
print(f"[resample] closest-point distance: median {np.median(dist):.5f}, "
      f"p99 {np.percentile(dist, 99):.5f}", flush=True)

tri = F[tri_id]
w1 = bary[:, 0:1]
w2 = bary[:, 1:2]
w0 = 1.0 - w1 - w2
uv = w0 * UV[tri[:, 0]] + w1 * UV[tri[:, 1]] + w2 * UV[tri[:, 2]]

atlas = np.asarray(Image.open(args.dense_atlas).convert("RGB"), dtype=np.uint8)
AH, AW = atlas.shape[:2]
ax = np.clip((uv[:, 0] * AW - 0.5).round().astype(np.int64), 0, AW - 1)
ay = np.clip(((1.0 - uv[:, 1]) * AH - 0.5).round().astype(np.int64), 0, AH - 1)
col = atlas[ay, ax]

out = np.zeros((RES * RES, 3), dtype=np.uint8)
out[np.where(valid)[0]] = col
img = out.reshape(RES, RES, 3)

# gutter dilation so mips and bilinear filtering never pull the black background in
grown = mask.copy()
work = img.astype(np.float32)
for _ in range(16):
    acc = np.zeros((RES, RES, 3), dtype=np.float32)
    cnt = np.zeros((RES, RES), dtype=np.float32)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb = np.roll(grown, (dy, dx), axis=(0, 1))
        acc += np.roll(work, (dy, dx), axis=(0, 1)) * nb[..., None]
        cnt += nb
    fill = ~grown & (cnt > 0)
    work[fill] = acc[fill] / cnt[fill][..., None]
    grown |= fill
img = work.round().astype(np.uint8)

nonblack = float((img.max(axis=2) > 8).mean())
print(f"[resample] non-black texels {nonblack:.1%}", flush=True)
assert nonblack > 0.25, "ANDON: transferred atlas is mostly black"
Image.fromarray(img).save(args.out)
print(f"[resample] wrote {args.out}", flush=True)
