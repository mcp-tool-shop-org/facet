"""Polygon-budget allocation on an ALREADY-TEXTURED mesh — UVs and atlas ride along.

Why this exists (measured 2026-08-04): the retopo->re-UV->bake route failed twice on
this asset. Blender's selected-to-active ray bake returned a black atlas (source is
thousands of shells, rays miss), and re-UVing the decimated mesh produced 119,776
islands whose packing margins collapsed every island to a sliver — 0.4% atlas
coverage, nothing to transfer onto.

Blender's collapse decimate INTERPOLATES existing UV layers, so a textured mesh keeps
working texture coordinates through the cut. No re-UV, no bake, no transfer, no new
failure surface: same atlas, fewer polygons, density spent where the form is.

Head protection uses a FRONT-VIEW FACE RECT, not a height band — a raised weapon rises
above the crown, so a height band protects the blade and starves the face.

  blender -b -P smart_decimate.py -- --glb textured.glb --out smart.glb
          --target 120000 --head-crop 360,240,700,600 [--crop-res 1024] [--pad-frac 0.25]
"""
import argparse
import json
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--target", type=int, default=120000)
ap.add_argument("--head-crop", required=True, help="x0,y0,x1,y1 in front-view pixels")
ap.add_argument("--crop-res", type=int, default=1024)
ap.add_argument("--bound", type=float, default=0.55)
ap.add_argument("--pad-frac", type=float, default=1.5,
                help="falloff distance outside the rect, as a fraction of rect size. "
                     "MEASURED 2026-08-04: 0.25 made protection effectively binary — "
                     "the face kept every polygon and the LEGS ABSORBED THE WHOLE CUT "
                     "and collapsed. Density must ramp, not cliff.")
ap.add_argument("--body-weight", type=float, default=0.8,
                help="max decimation weight far from the face. <1.0 keeps the body "
                     "from being annihilated to pay for the face.")
ap.add_argument("--factor", type=float, default=3.0,
                help="decimate vertex_group_factor; 10 is near-binary, 3 grades")
ap.add_argument("--report", default=None)
args = ap.parse_args(argv)
CX0, CY0, CX1, CY1 = [float(v) for v in args.head_crop.split(",")]


def die(msg):
    print(f"[smart] ANDON: {msg}", file=sys.stderr, flush=True)
    sys.exit(2)


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.abspath(args.glb))
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
if not meshes:
    die("no mesh in input GLB")
bpy.ops.object.select_all(action="DESELECT")
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
me = obj.data
n_before = len(me.polygons)
n_uv = len(me.uv_layers)
has_tex = any(m and m.use_nodes and any(n.type == "TEX_IMAGE" for n in m.node_tree.nodes)
              for m in me.materials)
print(f"[smart] source: {n_before:,} faces, {n_uv} UV layer(s), textured={has_tex}",
      flush=True)
if n_uv == 0:
    die("source has no UVs — this route requires an already-textured mesh")
if not has_tex:
    die("source has no image texture — nothing to carry through the cut")

# ---- protection weights from the face rect ----
co = [obj.matrix_world @ v.co for v in me.vertices]
maxabs = max(max(abs(c.x), abs(c.y), abs(c.z)) for c in co)
b = args.bound
pad = args.pad_frac * max(CX1 - CX0, CY1 - CY0)
vg = obj.vertex_groups.new(name="decimate_here")
n_protected = 0
for i, c in enumerate(co):
    px = (c.x / maxabs * 0.5 + b) / (2 * b) * args.crop_res
    py = (b - c.z / maxabs * 0.5) / (2 * b) * args.crop_res
    dx = max(CX0 - px, px - CX1, 0.0)
    dy = max(CY0 - py, py - CY1, 0.0)
    d = (dx * dx + dy * dy) ** 0.5
    w = 0.0 if d <= 0 else args.body_weight * min(1.0, d / pad)
    if w < 0.5:
        n_protected += 1
    vg.add([i], w, "REPLACE")
print(f"[smart] face rect protects {n_protected:,}/{len(co):,} verts", flush=True)
if n_protected < 100:
    die("face rect protected almost nothing — wrong rect or wrong projection")

ratio = min(1.0, args.target / max(n_before, 1))
dm = obj.modifiers.new("dec", "DECIMATE")
dm.ratio = ratio
dm.vertex_group = vg.name
dm.vertex_group_factor = args.factor
bpy.ops.object.modifier_apply(modifier=dm.name)
me = obj.data
n_after = len(me.polygons)
print(f"[smart] {n_before:,} -> {n_after:,} faces (target {args.target:,})", flush=True)
if n_after > n_before * 0.9:
    die(f"decimation was a no-op ({n_before:,} -> {n_after:,})")
if len(me.uv_layers) == 0:
    die("UV layer did not survive the decimate — the whole point of this route")
bpy.ops.object.shade_smooth()

# ANDON: UVs must still span the atlas, not have collapsed to a point
import numpy as np
nl = len(me.loops)
uv = np.empty(nl * 2, dtype=np.float32)
me.uv_layers[0].data.foreach_get("uv", uv)
uv = uv.reshape(-1, 2)
span = float(uv.max(axis=0).min() - uv.min(axis=0).max())
print(f"[smart] surviving UV span {span:.3f}, var {float(uv.var()):.4f}", flush=True)
if float(uv.var()) < 1e-4:
    die("UVs collapsed during decimate")

out = os.path.abspath(args.out)
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.gltf(filepath=out, use_selection=True, export_format="GLB")
kb = os.path.getsize(out) // 1024
print(f"[smart] wrote {out} ({kb} KB)", flush=True)
if args.report:
    json.dump({"src_faces": n_before, "out_faces": n_after,
               "protected_verts": n_protected, "kb": kb},
              open(args.report, "w"), indent=1)
print("[smart] OK", flush=True)
