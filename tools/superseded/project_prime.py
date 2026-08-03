"""PROJECTION-PRIME — paint the styled twin(s) onto the mesh via camera projection and
render the 8-view primed turnaround. The geometric successor to the FALSIFIED
statistical tint-prime (band colour transfer failed 3x: bands cannot tell arm from
torso; only the mesh knows which surface is which across views).

The twins are canny-locked restylizes of turnaround renders, so they are registered to
the mesh BY CONSTRUCTION. Front twin projects onto front-facing surfaces, back twin
onto back-facing (normal-blended), killing the face-on-occiput trap a single front
projection would create. Output renders are PRIMES for ~0.7-denoise restylize — never
shipped surfaces (mechanism-distinct from the falsified restylize-then-project lever).

  blender -b -P project_prime.py -- --glb mesh.glb --front twin_front.png
          --back twin_back.png --out DIR [--w 752 --h 1024] [--views 0,...,7]
"""
import argparse
import math
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--front", required=True, help="styled twin registered to view 0")
ap.add_argument("--back", required=True, help="styled twin registered to view 4")
ap.add_argument("--out", required=True)
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--w", type=int, default=752)
ap.add_argument("--h", type=int, default=1024)
args = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=args.glb)
meshes = [o for o in scene.objects if o.type == "MESH"]
assert meshes, "no mesh in GLB"
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
ortho = size.z * 1.204   # matches turn_render framing, so the twins map 1:1


def make_cam(name, th_deg):
    th = math.radians(th_deg)
    cd = bpy.data.cameras.new(name)
    cd.type = "ORTHO"
    cd.ortho_scale = ortho
    cam = bpy.data.objects.new(name, cd)
    scene.collection.objects.link(cam)
    cam.location = (mid.x + radius * math.sin(th), mid.y - radius * math.cos(th), mid.z)
    cam.rotation_euler = (math.radians(90), 0, th)
    return cam


proj_front = make_cam("proj_front", 0)
proj_back = make_cam("proj_back", 180)

# two UV maps, one per projector
uv_f = obj.data.uv_layers.new(name="uv_front")
uv_b = obj.data.uv_layers.new(name="uv_back")
for uvname, proj in (("uv_front", proj_front), ("uv_back", proj_back)):
    m = obj.modifiers.new(f"prj_{uvname}", "UV_PROJECT")
    m.uv_layer = uvname
    m.projector_count = 1
    m.projectors[0].object = proj
    m.aspect_x = args.w
    m.aspect_y = args.h

img_f = bpy.data.images.load(args.front)
img_b = bpy.data.images.load(args.back)
mat = bpy.data.materials.new("prime")
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
dot.inputs[1].default_value = (0.0, -1.0, 0.0)   # front axis (glTF front -Y in Blender)
lt = nt.nodes.new("ShaderNodeMath")
lt.operation = "LESS_THAN"                        # normal·front < 0 -> back-facing
lt.inputs[1].default_value = 0.0
nt.links.new(geo.outputs["Normal"], dot.inputs[0])
nt.links.new(dot.outputs["Value"], lt.inputs[0])
nt.links.new(uvn_f.outputs["UV"], tex_f.inputs["Vector"])
nt.links.new(uvn_b.outputs["UV"], tex_b.inputs["Vector"])
nt.links.new(tex_f.outputs["Color"], mix.inputs[6])
nt.links.new(tex_b.outputs["Color"], mix.inputs[7])
nt.links.new(lt.outputs["Value"], mix.inputs[0])
nt.links.new(mix.outputs[2], emit.inputs["Color"])
nt.links.new(emit.outputs["Emission"], out_node.inputs["Surface"])
obj.data.materials.clear()
obj.data.materials.append(mat)

render_cam = make_cam("render_cam", 0)
scene.camera = render_cam
scene.render.resolution_x = args.w
scene.render.resolution_y = args.h
scene.render.image_settings.file_format = "PNG"
scene.render.engine = "CYCLES"          # emission needs a real engine; 8 samples plenty
scene.cycles.samples = 8
scene.cycles.device = "CPU"
scene.view_settings.view_transform = "Standard"
world = bpy.data.worlds.new("bg")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.181, 0.181, 0.188, 1)
scene.world = world

for idx in [int(v) for v in args.views.split(",")]:
    th = math.radians(idx * 45.0)
    render_cam.location = (mid.x + radius * math.sin(th),
                           mid.y - radius * math.cos(th), mid.z)
    render_cam.rotation_euler = (math.radians(90), 0, th)
    scene.render.filepath = f"{args.out}/prime_{idx}.png"
    bpy.ops.render.render(write_still=True)
    print(f"[prime] view {idx} -> prime_{idx}.png", flush=True)
