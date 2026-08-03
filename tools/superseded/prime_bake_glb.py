"""Bake the projection-prime (front+back styled twins, normal-blended) into a texture
atlas and export a viewable GLB. Preview artifact: occlusion slivers stay smeared —
the 8 restylized views remain the deliverable; this is for LOOKING at the asset in 3D.

  blender -b -P prime_bake_glb.py -- --glb mesh.glb --front twin_f.png --back twin_b.png
          --out styled.glb [--res 2048]
"""
import argparse
import math
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--front", required=True)
ap.add_argument("--back", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--res", type=int, default=2048)
ap.add_argument("--aspect-w", type=int, default=752)
ap.add_argument("--aspect-h", type=int, default=1024)
args = ap.parse_args(argv)

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


def make_proj(name, th_deg):
    th = math.radians(th_deg)
    cd = bpy.data.cameras.new(name)
    cd.type = "ORTHO"
    cd.ortho_scale = ortho
    cam = bpy.data.objects.new(name, cd)
    scene.collection.objects.link(cam)
    cam.location = (mid.x + radius * math.sin(th), mid.y - radius * math.cos(th), mid.z)
    cam.rotation_euler = (math.radians(90), 0, th)
    return cam


for uvname, cam in (("uv_front", make_proj("pf", 0)), ("uv_back", make_proj("pb", 180))):
    obj.data.uv_layers.new(name=uvname)
    m = obj.modifiers.new(f"prj_{uvname}", "UV_PROJECT")
    m.uv_layer = uvname
    m.projector_count = 1
    m.projectors[0].object = cam
    m.aspect_x = args.aspect_w
    m.aspect_y = args.aspect_h
    bpy.ops.object.modifier_apply(modifier=m.name)

# bake target UVs
uv_bake = obj.data.uv_layers.new(name="uv_bake")
obj.data.uv_layers.active = uv_bake
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.003)
bpy.ops.object.mode_set(mode="OBJECT")

img_f = bpy.data.images.load(args.front)
img_b = bpy.data.images.load(args.back)
bake_img = bpy.data.images.new("styled_bake", args.res, args.res, alpha=False)

mat = bpy.data.materials.new("styled")
mat.use_nodes = True
nt = mat.node_tree
nt.nodes.clear()
out_node = nt.nodes.new("ShaderNodeOutputMaterial")
emit = nt.nodes.new("ShaderNodeEmission")
mix = nt.nodes.new("ShaderNodeMix")
mix.data_type = "RGBA"
tex_f = nt.nodes.new("ShaderNodeTexImage")
tex_f.image = img_f
tex_b = nt.nodes.new("ShaderNodeTexImage")
tex_b.image = img_b
uvn_f = nt.nodes.new("ShaderNodeUVMap")
uvn_f.uv_map = "uv_front"
uvn_b = nt.nodes.new("ShaderNodeUVMap")
uvn_b.uv_map = "uv_back"
geo = nt.nodes.new("ShaderNodeNewGeometry")
dot = nt.nodes.new("ShaderNodeVectorMath")
dot.operation = "DOT_PRODUCT"
dot.inputs[1].default_value = (0.0, -1.0, 0.0)
lt = nt.nodes.new("ShaderNodeMath")
lt.operation = "LESS_THAN"
lt.inputs[1].default_value = 0.0
bake_node = nt.nodes.new("ShaderNodeTexImage")
bake_node.image = bake_img
uvn_bake = nt.nodes.new("ShaderNodeUVMap")
uvn_bake.uv_map = "uv_bake"
nt.links.new(uvn_bake.outputs["UV"], bake_node.inputs["Vector"])
nt.links.new(geo.outputs["Normal"], dot.inputs[0])
nt.links.new(dot.outputs["Value"], lt.inputs[0])
nt.links.new(uvn_f.outputs["UV"], tex_f.inputs["Vector"])
nt.links.new(uvn_b.outputs["UV"], tex_b.inputs["Vector"])
nt.links.new(tex_f.outputs["Color"], mix.inputs[6])
nt.links.new(tex_b.outputs["Color"], mix.inputs[7])
nt.links.new(lt.outputs["Value"], mix.inputs[0])
nt.links.new(mix.outputs[2], emit.inputs["Color"])
nt.links.new(emit.outputs["Emission"], out_node.inputs["Surface"])
nt.nodes.active = bake_node
obj.data.materials.clear()
obj.data.materials.append(mat)

scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 8
bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.bake(type="EMIT")

# rewire: baked image becomes the base colour; drop projector UV layers
nt.nodes.clear()
out2 = nt.nodes.new("ShaderNodeOutputMaterial")
bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
tex_final = nt.nodes.new("ShaderNodeTexImage")
tex_final.image = bake_img
uvf = nt.nodes.new("ShaderNodeUVMap")
uvf.uv_map = "uv_bake"
nt.links.new(uvf.outputs["UV"], tex_final.inputs["Vector"])
nt.links.new(tex_final.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.85
nt.links.new(bsdf.outputs["BSDF"], out2.inputs["Surface"])
for name in ("uv_front", "uv_back"):
    lyr = obj.data.uv_layers.get(name)
    if lyr:
        obj.data.uv_layers.remove(lyr)

import os
out = os.path.abspath(args.out)
bpy.ops.export_scene.gltf(filepath=out, use_selection=True, export_format="GLB")
print(f"[bake] wrote {out}  ({os.path.getsize(out)//1024} KB)", flush=True)
