"""Render the figure and the prop as SEPARATE silhouettes through ONE shared camera.

Framing is copied from tools/verify/turn_render.py so these masks line up pixel-for-pixel
with the facings that ship: framing derived from the WHOLE composite's bbox once, camera
orbits, ORTHO, sensor_fit VERTICAL, ortho_scale = size.z * margin.

Two passes per view. Hiding one object does not move the camera, so the two masks are
directly comparable and the gap between them is a real screen-space distance.

  blender -b -P facing_masks.py -- --glb <composite.glb> --out <dir>
                                   [--body body] [--prop shield] [--views 0,..,7]
"""
import argparse
import math
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--body", default="body")
ap.add_argument("--prop", default="shield")
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--step", type=float, default=45.0)
ap.add_argument("--w", type=int, default=768)
ap.add_argument("--h", type=int, default=1024)
ap.add_argument("--margin", type=float, default=1.204)
args = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=args.glb)
meshes = [o for o in scene.objects if o.type == "MESH"]
if len(meshes) != 2:
    raise SystemExit("ANDON: expected exactly two meshes (figure and prop), got %d: %r"
                     % (len(meshes), [o.name for o in meshes]))
by_name = {o.name: o for o in meshes}
for want in (args.body, args.prop):
    if want not in by_name:
        raise SystemExit("ANDON: no object %r in %s (have %r)"
                         % (want, args.glb, sorted(by_name)))
body, prop = by_name[args.body], by_name[args.prop]

lo = Vector((1e9, 1e9, 1e9))
hi = Vector((-1e9, -1e9, -1e9))
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        lo = Vector((min(lo[i], w[i]) for i in range(3)))
        hi = Vector((max(hi[i], w[i]) for i in range(3)))
size, mid = hi - lo, (lo + hi) / 2
radius = max(size.x, size.y) * 3.0

cam_data = bpy.data.cameras.new("cam")
cam_data.type = "ORTHO"
cam_data.sensor_fit = "VERTICAL"
cam_data.ortho_scale = size.z * args.margin
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
scene.render.resolution_x = args.w
scene.render.resolution_y = args.h
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.film_transparent = True          # the mask IS the alpha
scene.render.engine = "BLENDER_WORKBENCH"
sh = scene.display.shading
sh.light = "FLAT"
sh.color_type = "SINGLE"
sh.show_cavity = False
scene.view_settings.view_transform = "Standard"

for idx in [int(v) for v in args.views.split(",")]:
    th = math.radians(idx * args.step)
    cam.location = (mid.x + radius * math.sin(th), mid.y - radius * math.cos(th), mid.z)
    cam.rotation_euler = (math.radians(90), 0, th)
    for tag, keep, drop in (("body", body, prop), ("prop", prop, body)):
        drop.hide_render = True
        keep.hide_render = False
        scene.render.filepath = "%s/mask_%s_%d.png" % (args.out, tag, idx)
        bpy.ops.render.render(write_still=True)
        print("[mask] view %d  %s" % (idx, tag), flush=True)
    prop.hide_render = False
    body.hide_render = False
