"""Rotate a third-party GLB into the pipeline's convention WITHOUT destroying it.

The downstream chain (project_texture, turn_render, facing_atlas, project_multiview) assumes
glTF **+Y up** with the figure's FRONT facing **+Z** — what TRELLIS.2 emits, and what
"view 0 = front" means everywhere. Tripo does not follow that: measured 2026-08-02 across
three separate exports, the front faces **+X** (correct only at view 2). Feeding an unrotated
Tripo mesh to project_texture silently projects the concept onto the figure's SIDE.

⛔⛔ THE BUG THIS FILE EXISTS TO NOT REPEAT — measured, do not reintroduce.

`trimesh.Scene.to_mesh()` DESTROYS the GLB's authored vertex normals. trimesh then recomputes
them per-face and a smooth 4,869-face head renders **heavily faceted** — every polygon
visible. It looks exactly like a bad texture bake from the generator, and on 2026-08-02 it
nearly got a third-party mesh blamed for damage this tool had done.

Measured, mean vertex-normal spread within a face (0 = flat/faceted, higher = smooth):

    source as loaded ................ 0.7122
    to_mesh() ....................... 0.1457   <- 80% of the smoothing destroyed
    load(process=False) + to_mesh() .. 0.1457   <- process=False does NOT save you
    no to_mesh() + carry normals ..... 0.7122   <- what this file does now

⚠ An earlier "fix" captured `vertex_normals` AFTER `to_mesh()` and rotated those — i.e. it
carefully preserved already-destroyed data, and still measured 0.1457. **Capture before you
concatenate, or better, never concatenate.**

⭐ NOTE: rotating the mesh at all is the second-best answer. The right fix is a `--yaw-offset`
on the CAMERA in `turn_render.py` / `project_texture.py`, so a third-party mesh is consumed
in place and never rewritten. This tool exists because that does not exist yet.

  normalize_mesh.py --glb in.glb --out out.glb [--yaw -90] [--zup] [--verify]
"""
import argparse
import math
from pathlib import Path

import numpy as np
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--yaw", type=float, default=-90.0, help="degrees about +Y; Tripo needs -90")
ap.add_argument("--zup", action="store_true", help="first rotate -90 about X (Z-up sources)")
ap.add_argument("--verify", action="store_true", default=True,
                help="assert the normals survived; abort rather than emit a faceted mesh")
args = ap.parse_args()


def normal_spread(m):
    """Mean disagreement between a face's own vertex normals. 0 => flat-shaded."""
    vn = np.asarray(m.vertex_normals)
    return float(np.linalg.norm(vn[m.faces[:, 0]] - vn[m.faces[:, 1]], axis=1).mean())


# ⛔ process=False AND no to_mesh(). Both matter.
scene = trimesh.load(args.glb, process=False)
if isinstance(scene, trimesh.Scene):
    geoms = list(scene.geometry.values())
    if len(geoms) != 1:
        raise SystemExit(f"ERROR: {len(geoms)} geometries. Concatenating would destroy the "
                         "authored normals — handle this case explicitly, do not to_mesh().")
    mesh = geoms[0]
else:
    mesh = scene

before_spread = normal_spread(mesh)
before_ext = (mesh.bounds[1] - mesh.bounds[0]).round(3)

R = np.eye(4)
if args.zup:
    R = trimesh.transformations.rotation_matrix(math.radians(-90), [1, 0, 0]) @ R
if args.yaw:
    R = trimesh.transformations.rotation_matrix(math.radians(args.yaw), [0, 1, 0]) @ R

if not np.allclose(R, np.eye(4)):
    n0 = np.asarray(mesh.vertex_normals).copy()      # capture BEFORE any mutation
    mesh.apply_transform(R)
    n = n0 @ R[:3, :3].T
    mesh.vertex_normals = n / np.linalg.norm(n, axis=1, keepdims=True).clip(1e-8)

lo, hi = mesh.bounds
mesh.apply_translation(-(lo + hi) / 2.0)

after_spread = normal_spread(mesh)
after_ext = (mesh.bounds[1] - mesh.bounds[0]).round(3)

print(f"[norm] extent {before_ext} -> {after_ext}")
print(f"[norm] tall axis {['X','Y','Z'][int(np.argmax(after_ext))]} (want Y)")
print(f"[norm] normal spread {before_spread:.4f} -> {after_spread:.4f} (want unchanged)")

if args.verify and after_spread < before_spread * 0.9:
    raise SystemExit(f"ABORT: vertex normals degraded {before_spread:.4f} -> {after_spread:.4f}. "
                     "The mesh would render faceted. Nothing written.")

Path(args.out).parent.mkdir(parents=True, exist_ok=True)
mesh.export(args.out)
print(f"[out ] {args.out} ({Path(args.out).stat().st_size/1e6:.1f} MB)")
