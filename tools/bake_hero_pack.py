"""Stage D part 3/3 — package the fused atlas into the final GLB.

Imports prep_uv.glb (carries the packed UVs), binds the atlas as Principled base
colour, PACKS the image (unpacked generated images silently drop from glTF export —
measured trap), exports GLB. Standards compliance: see bake_hero_fuse.py.

  blender -b -P bake_hero_pack.py -- --prep-glb prep_uv.glb --atlas atlas.png --out hero.glb
"""
import argparse
import os
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--prep-glb", required=True)
ap.add_argument("--atlas", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=args.prep_glb)
meshes = [o for o in scene.objects if o.type == "MESH"]
if not (len(meshes) == 1):
    raise AssertionError(f"ANDON: expected 1 mesh, got {len(meshes)}")
obj = meshes[0]
if not (obj.data.uv_layers):
    raise AssertionError("ANDON: prep GLB carries no UVs")

img = bpy.data.images.load(os.path.abspath(args.atlas))
img.pack()
if not (img.packed_file is not None):
    raise AssertionError("ANDON: atlas failed to pack")

mat = bpy.data.materials.new("hero")
mat.use_nodes = True
obj.data.materials.clear()
obj.data.materials.append(mat)
nt = mat.node_tree
nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial")
bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
tex = nt.nodes.new("ShaderNodeTexImage")
tex.image = img
uvn = nt.nodes.new("ShaderNodeUVMap")
uvn.uv_map = obj.data.uv_layers[0].name
nt.links.new(uvn.outputs["UV"], tex.inputs["Vector"])
nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.85
nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

outp = os.path.abspath(args.out)
bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.gltf(filepath=outp, use_selection=True, export_format="GLB")
sz = os.path.getsize(outp)
if not (sz > os.path.getsize(args.atlas) * 0.5):
    raise AssertionError("ANDON: GLB too small — texture dropped")
print(f"[pack] wrote {outp} ({sz//1024} KB) — DONE", flush=True)
