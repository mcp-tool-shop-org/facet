"""Head-framed close-up renders of a GLB — the Director-zoom verification camera.

Frames the head using the SAME front-view crop-rect convention the face detail pass
used (crop rect in front-view pixel space, bound 0.55, std frame), so the render
close-up shows exactly the region the face view owns. Workbench conventions match
turn_render.py: camera-relative STUDIO light, Standard transform, exposure 0.85.

  blender -b -P head_render.py -- --glb in.glb --out DIR --tag name
          [--views -30,0,30] [--crop 360,240,700,600] [--res 1024] [--pad 1.25]
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
ap.add_argument("--tag", default="head")
ap.add_argument("--views", default="-30,0,30", help="camera yaw degrees, 0 = front")
ap.add_argument("--crop", default="360,240,700,600")
ap.add_argument("--crop-res", type=int, default=1024)
ap.add_argument("--bound", type=float, default=0.55)
ap.add_argument("--res", type=int, default=1024)
ap.add_argument("--pad", type=float, default=1.25)
ap.add_argument("--flat", action="store_true")
ap.add_argument("--clay", action="store_true",
                help="uniform grey: judge GEOMETRY with no texture in the way")
args = ap.parse_args(argv)
CX0, CY0, CX1, CY1 = [float(v) for v in args.crop.split(",")]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=args.glb)
meshes = [o for o in scene.objects if o.type == "MESH"]
assert meshes, "no mesh in GLB"

maxabs = 0.0
mid = Vector((0, 0, 0))
lo = Vector((1e9,) * 3)
hi = Vector((-1e9,) * 3)
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        maxabs = max(maxabs, abs(w.x), abs(w.y), abs(w.z))
        lo = Vector((min(lo[i], w[i]) for i in range(3)))
        hi = Vector((max(hi[i], w[i]) for i in range(3)))
mid = (lo + hi) / 2
k = maxabs / 0.5          # std -> world scale
b = args.bound

# head centre + size from the crop rect, in std then world units
sx0 = (CX0 / args.crop_res) * 2 * b - b
sx1 = (CX1 / args.crop_res) * 2 * b - b
sz0 = b - (CY1 / args.crop_res) * 2 * b
sz1 = b - (CY0 / args.crop_res) * 2 * b
cx = (sx0 + sx1) / 2 * k
cz = (sz0 + sz1) / 2 * k
span = max(sx1 - sx0, sz1 - sz0) * k

cam_data = bpy.data.cameras.new("cam")
cam_data.type = "ORTHO"
cam_data.ortho_scale = span * args.pad
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
radius = maxabs * 6.0

scene.render.resolution_x = args.res
scene.render.resolution_y = args.res
scene.render.image_settings.file_format = "PNG"
scene.render.engine = "BLENDER_WORKBENCH"
sh = scene.display.shading
sh.light = "FLAT" if args.flat else "STUDIO"
scene.view_settings.view_transform = "Standard"
scene.view_settings.exposure = 0.85
sh.background_color = (0.181, 0.181, 0.188)
sh.color_type = "SINGLE" if args.clay else "TEXTURE"
sh.show_cavity = False
sh.background_type = "VIEWPORT"
sh.use_world_space_lighting = False

for yaw in [float(v) for v in args.views.split(",")]:
    th = math.radians(yaw)
    cam.location = (cx + radius * math.sin(th),
                    mid.y - radius * math.cos(th),
                    cz)
    cam.rotation_euler = (math.radians(90), 0, th)
    scene.render.filepath = f"{args.out}/{args.tag}_y{int(yaw):+04d}.png"
    bpy.ops.render.render(write_still=True)
    print(f"[head] yaw {yaw:+.0f} -> {scene.render.filepath}", flush=True)
