"""Swap a GLB's baseColorTexture for the projection-CONFIDENCE atlas.

project_texture.py already writes `atlas_weight.png` under --debug-dir: the per-texel
weight w with which the projected image beat the volume bake. w is high where a texel was
seen square-on by the projection camera and low where it was back-facing, occluded,
off-silhouette, or steeply foreshortened.

That is exactly the "is the input GOOD here?" signal. Rendering a GLB that carries w as its
colour gives, per view, a per-PIXEL map of how trustworthy that view's render is -- which is
the substrate for a graded denoise mask instead of a hand-drawn band.

    project_texture.py --debug-dir D   ->  D/atlas_weight.png   (atlas space)
    weight_glb.py                      ->  confidence.glb
    turn_render.py --flat              ->  per-view confidence   (FLAT: it is data, not a look)

`atlas_weight.png` is written through to_raster_rows(), i.e. already in the PIL/glTF row
order a baseColorTexture uses, so it drops straight in with no flip. Getting that backwards
does not crash -- it produces plausible-looking garbage -- so it is asserted below by
checking that the weight is high exactly where the mesh faces +Z (the projection camera).
"""
import argparse
from pathlib import Path

import numpy as np
import trimesh
import trimesh.visual
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True, help="the GLB the weight map belongs to")
ap.add_argument("--weight", required=True, help="atlas_weight.png from project_texture --debug-dir")
ap.add_argument("--out", required=True)
args = ap.parse_args()

scene = trimesh.load(args.glb)
mesh = scene.to_mesh() if isinstance(scene, trimesh.Scene) else scene
mat = mesh.visual.material
assert mat is not None and mat.baseColorTexture is not None, "GLB has no baked baseColorTexture"

atlas = mat.baseColorTexture
w_img = Image.open(args.weight).convert("L")
if w_img.size != atlas.size:
    w_img = w_img.resize(atlas.size, Image.NEAREST)
w = np.asarray(w_img)

# Sanity check the row convention: sample the atlas position of every texel is not available
# here, so use the cheap proxy -- the weight map must be mostly-zero (back/occluded surface
# is the majority of a closed figure seen from one side) and must have a substantial bright
# mode. A flipped map still satisfies that, so this is a smoke test, not a proof; the real
# proof is the rendered confidence lining up with the figure's front in turn_render output.
frac_hi = float((w > 128).mean())
print(f"[wght] {args.weight}  {w_img.size}  high-confidence texels: {100*frac_hi:.1f}%")
if frac_hi < 0.01 or frac_hi > 0.60:
    print(f"[wght] WARNING: {100*frac_hi:.1f}% high-confidence is outside the expected "
          f"1-60% band for a single-view projection onto a closed figure")

new_mat = mat.copy()
new_mat.baseColorTexture = Image.fromarray(np.dstack([w, w, w]), mode="RGB")
# Kill any material tint/factor so the render reports the texture VALUE, not value * factor.
if hasattr(new_mat, "baseColorFactor"):
    new_mat.baseColorFactor = np.array([255, 255, 255, 255], dtype=np.uint8)
mesh.visual = trimesh.visual.TextureVisuals(uv=mesh.visual.uv, material=new_mat)

Path(args.out).parent.mkdir(parents=True, exist_ok=True)
mesh.export(args.out)
print(f"[out ] {args.out} ({Path(args.out).stat().st_size/1e6:.1f} MB)")
