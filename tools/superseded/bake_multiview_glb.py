"""Bake N turnaround views onto a mesh with facing-weighted blending, export GLB.

⚠ MEASURED TRAP (2026-08-03, cost one blank-white GLB): Blender meshes cap at 8 UV
layers and `uv_layers.new()` returns **None silently** at the cap — no exception. A
naive 8-projector + 1-bake-target design needs 9 layers; the bake target never exists,
smart_project silently overwrites the last projector layer, and the export renders
white. THIS design uses exactly TWO layers: `uv_bake` (created FIRST) + one cycling
projector layer, accumulating per-view bakes in numpy:

  for each view i: project -> bake colour*weight -> bake weight -> accumulate
  final atlas = sum(colour_i * w_i) / sum(w_i),  w_i = max(dot(n, view_dir_i), 0)^power

RETRY-OF-A-FALSIFIED-LEVER NOTE: the store falsified "project restylized views onto
the head" for INDEPENDENT per-view restylizes. This retries it because the mechanism
changed: projection-primed views (denoise 0.70, control to 1.0) all derive from one
twin projection — aligned by construction. Judge the head at x5 before trusting.

  blender -b -P bake_multiview_glb.py -- --glb mesh.glb --views "dir/n{}.png"
          --out styled.glb [--power 6] [--res 2048]
"""
import argparse
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--views", required=True, help="pattern with {} for view index 0..7")
ap.add_argument("--out", required=True)
ap.add_argument("--azimuths", default="0,45,90,135,180,225,270,315",
                help="bake-frame yaw per view, degrees (MV-Adapter mapping: bake yaw "
                     "= adapter azimuth + 90; its canonical set = 0,90,180,270 + top/bottom)")
ap.add_argument("--elevations", default=None,
                help="elevation per view, degrees (default all 0)")
ap.add_argument("--power", type=float, default=6.0)
ap.add_argument("--res", type=int, default=2048)
ap.add_argument("--aspect-w", type=int, default=752)
ap.add_argument("--aspect-h", type=int, default=1024)
args = ap.parse_args(argv)

AZ = [float(x) for x in args.azimuths.split(",")]
EL = ([float(x) for x in args.elevations.split(",")]
      if args.elevations else [0.0] * len(AZ))
assert len(AZ) == len(EL), "azimuths and elevations must match"
N = len(AZ)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=args.glb)
meshes = [o for o in scene.objects if o.type == "MESH"]
bpy.ops.object.select_all(action="DESELECT")
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
# drop any imported UV layers so our two are the only ones (stay far from the cap of 8)
while obj.data.uv_layers:
    obj.data.uv_layers.remove(obj.data.uv_layers[0])

lo = Vector((1e9,) * 3)
hi = Vector((-1e9,) * 3)
for c in obj.bound_box:
    w = obj.matrix_world @ Vector(c)
    lo = Vector((min(lo[i], w[i]) for i in range(3)))
    hi = Vector((max(hi[i], w[i]) for i in range(3)))
size = hi - lo
mid = (lo + hi) / 2
radius = max(size.x, size.y) * 3.0
ortho = size.z * 1.204

# bake-target UVs FIRST (layer 1 of 2)
uv_bake = obj.data.uv_layers.new(name="uv_bake")
assert uv_bake is not None, "uv_bake creation failed"
obj.data.uv_layers.active = uv_bake
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.003)
bpy.ops.object.mode_set(mode="OBJECT")

cams = []
for i in range(N):
    th = math.radians(AZ[i])
    el = math.radians(EL[i])
    cd = bpy.data.cameras.new(f"p{i}")
    cd.type = "ORTHO"
    cd.ortho_scale = ortho
    cam = bpy.data.objects.new(f"p{i}", cd)
    scene.collection.objects.link(cam)
    cam.location = (mid.x + radius * math.sin(th) * math.cos(el),
                    mid.y - radius * math.cos(th) * math.cos(el),
                    mid.z + radius * math.sin(el))
    cam.rotation_euler = (math.radians(90) - el, 0, th)
    cams.append(cam)

scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 1
bake_img = bpy.data.images.new("pass_img", args.res, args.res, alpha=False,
                               float_buffer=True)
bake_img.colorspace_settings.name = "Non-Color"

mat = bpy.data.materials.new("mv")
mat.use_nodes = True
obj.data.materials.clear()
obj.data.materials.append(mat)
nt = mat.node_tree

acc_c = np.zeros(args.res * args.res * 4, dtype=np.float64)
acc_w = np.zeros(args.res * args.res * 4, dtype=np.float64)

for i in range(N):
    uv_proj = obj.data.uv_layers.new(name="uv_proj")
    assert uv_proj is not None, f"uv_proj creation failed at view {i}"
    m = obj.modifiers.new("prj", "UV_PROJECT")
    m.uv_layer = "uv_proj"
    m.projector_count = 1
    m.projectors[0].object = cams[i]
    m.aspect_x = args.aspect_w
    m.aspect_y = args.aspect_h
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=m.name)

    th = math.radians(AZ[i])
    el = math.radians(EL[i])
    vdir = (math.sin(th) * math.cos(el), -math.cos(th) * math.cos(el), math.sin(el))

    for mode in ("cw", "w"):
        nt.nodes.clear()
        out_node = nt.nodes.new("ShaderNodeOutputMaterial")
        emit = nt.nodes.new("ShaderNodeEmission")
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        dot = nt.nodes.new("ShaderNodeVectorMath")
        dot.operation = "DOT_PRODUCT"
        dot.inputs[1].default_value = vdir
        nt.links.new(geo.outputs["Normal"], dot.inputs[0])
        mx = nt.nodes.new("ShaderNodeMath")
        mx.operation = "MAXIMUM"
        mx.inputs[1].default_value = 0.0
        nt.links.new(dot.outputs["Value"], mx.inputs[0])
        pw0 = nt.nodes.new("ShaderNodeMath")
        pw0.operation = "POWER"
        pw0.inputs[1].default_value = args.power
        nt.links.new(mx.outputs["Value"], pw0.inputs[0])
        # weight FLOOR: all 8 view dirs are horizontal, so up/down-facing facets get
        # ~zero from every view and divide to BLACK SPECKS (measured 2026-08-03).
        # The floor gives such texels an all-view average instead of black.
        pw = nt.nodes.new("ShaderNodeMath")
        pw.operation = "ADD"
        pw.inputs[1].default_value = 0.002
        nt.links.new(pw0.outputs["Value"], pw.inputs[0])
        if mode == "cw":
            img = bpy.data.images.load(args.views.format(i))
            tex = nt.nodes.new("ShaderNodeTexImage")
            tex.image = img
            uvn = nt.nodes.new("ShaderNodeUVMap")
            uvn.uv_map = "uv_proj"
            nt.links.new(uvn.outputs["UV"], tex.inputs["Vector"])
            mul = nt.nodes.new("ShaderNodeVectorMath")
            mul.operation = "SCALE"
            nt.links.new(tex.outputs["Color"], mul.inputs[0])
            nt.links.new(pw.outputs["Value"], mul.inputs["Scale"])
            nt.links.new(mul.outputs[0], emit.inputs["Color"])
        else:
            comb = nt.nodes.new("ShaderNodeCombineXYZ")
            for k in range(3):
                nt.links.new(pw.outputs["Value"], comb.inputs[k])
            nt.links.new(comb.outputs[0], emit.inputs["Color"])
        nt.links.new(emit.outputs["Emission"], out_node.inputs["Surface"])
        bake_node = nt.nodes.new("ShaderNodeTexImage")
        bake_node.image = bake_img
        uvb = nt.nodes.new("ShaderNodeUVMap")
        uvb.uv_map = "uv_bake"
        nt.links.new(uvb.outputs["UV"], bake_node.inputs["Vector"])
        nt.nodes.active = bake_node
        obj.data.uv_layers.active = obj.data.uv_layers["uv_bake"]
        bpy.ops.object.bake(type="EMIT")
        px = np.array(bake_img.pixels[:], dtype=np.float64)
        if mode == "cw":
            acc_c += px
        else:
            acc_w += px
    lyr = obj.data.uv_layers.get("uv_proj")
    obj.data.uv_layers.remove(lyr)
    print(f"[mvbake] view {i} accumulated", flush=True)

w = np.maximum(acc_w, 1e-4)
final = acc_c / w
final[3::4] = 1.0

# dilation fill: texels no bake pass covered (outside islands / margin gaps) are
# black and bleed at seams as specks. Fill them from valid neighbours.
res = args.res
img4 = final.reshape(res, res, 4)
w4 = acc_w.reshape(res, res, 4)[..., 0]
valid = w4 > 0.004          # floor contributes 8*0.002=0.016 on real surface texels
for _ in range(24):
    if valid.all():
        break
    acc_n = np.zeros((res, res, 3))
    cnt = np.zeros((res, res))
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb_v = np.roll(valid, (dy, dx), axis=(0, 1))
        nb_c = np.roll(img4[..., :3], (dy, dx), axis=(0, 1))
        acc_n += nb_c * nb_v[..., None]
        cnt += nb_v
    fill = (~valid) & (cnt > 0)
    img4[..., :3][fill] = acc_n[fill] / cnt[fill][..., None]
    valid = valid | fill
final = img4.reshape(-1)
print(f"[mvbake] dilation left {int((~valid).sum())} unfilled texels", flush=True)

var = float(np.var(final[: 4 * 8192]))
print(f"[mvbake] final atlas var {var:.5f}", flush=True)
if var < 0.001:
    print("[mvbake] ANDON: final atlas is uniform — accumulation failed", file=sys.stderr)
    sys.exit(2)

# the accumulator holds LINEAR values (float Non-Color bakes). An 8-bit image's
# pixel buffer stores raw values in the image's own encoding, so write sRGB-ENCODED
# values or the export decodes them a second time and crushes the midtones
# (measured 2026-08-03: green tunic rendered black).
lin = np.clip(final, 0.0, 1.0)
srgb = np.where(lin <= 0.0031308, lin * 12.92,
                1.055 * np.power(lin, 1.0 / 2.4) - 0.055)
srgb[3::4] = 1.0
final_img = bpy.data.images.new("styled_atlas", args.res, args.res, alpha=False)
final_img.pixels[:] = srgb.tolist()
final_img.pack()

nt.nodes.clear()
out2 = nt.nodes.new("ShaderNodeOutputMaterial")
bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
tex_final = nt.nodes.new("ShaderNodeTexImage")
tex_final.image = final_img
uvf = nt.nodes.new("ShaderNodeUVMap")
uvf.uv_map = "uv_bake"
nt.links.new(uvf.outputs["UV"], tex_final.inputs["Vector"])
nt.links.new(tex_final.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.85
nt.links.new(bsdf.outputs["BSDF"], out2.inputs["Surface"])

out = os.path.abspath(args.out)
bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.gltf(filepath=out, use_selection=True, export_format="GLB")
print(f"[mvbake] wrote {out}  ({os.path.getsize(out)//1024} KB)", flush=True)
