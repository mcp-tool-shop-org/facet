"""Matched-framing turnaround render of a GLB.

Framing is derived from the figure's bounding box ONCE and then held fixed while the
CAMERA orbits, so every view is directly comparable and a mask drawn on one view means the
same thing on another. Same conventions as saltroad_v21_full_figure.py, which produced the
renders this run has to line up with: ORTHO, Workbench, glTF front faces -Y after import.

--flat matters and is not cosmetic. STUDIO lighting multiplies and the AgX view transform
tone-maps, so a default render is NOT a readout of the texture it carries. When the atlas
holds DATA (a projection-confidence map) rather than colour, the render must be FLAT light
+ Standard transform or the numbers come back wrong. That mistake already cost a debugging
round on this asset (a self-check failed at 34/255 that should have passed at ~1/255).

  blender -b -P turn_render.py -- --glb <in.glb> --out <dir> --tag proj [--views 0,1,7]
                                  [--w 757 --h 1024] [--flat] [--clay]
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
ap.add_argument("--tag", default="view")
ap.add_argument("--views", default="0,1,2,3,4,5,6,7",
                help="comma-separated view indices; index i = i*step deg of yaw, 0 = front")
ap.add_argument("--step", type=float, default=45.0,
                help="degrees per view index (45 = the classic 8-direction turnaround; "
                     "smaller steps give a dense sweep for head-pose estimation)")
ap.add_argument("--w", type=int, default=757)
ap.add_argument("--h", type=int, default=1024)
ap.add_argument("--flat", action="store_true",
                help="FLAT light + Standard view transform: render the texture VALUE, not a lit look")
ap.add_argument("--clay", action="store_true", help="uniform grey: geometry only, no texture")
ap.add_argument("--exposure", type=float, default=0.85,
                help="stops. Camera-relative lighting lights every view IDENTICALLY, which is "
                     "the point -- but it lands ~1.75x below the old world-space-lit renders on "
                     "the FRONT view. 0.85 stops matches that reference on the front while "
                     "keeping the back views lit the same instead of dropping them into shadow.")
ap.add_argument("--yaw-offset", type=float, default=0.0,
                help="degrees added to every view's camera yaw. This is how a third-party mesh "
                     "in a foreign orientation is consumed IN PLACE: rotate the CAMERA, never "
                     "the mesh (mesh rotation via to_mesh() destroys authored vertex normals).")
args = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=args.glb)
meshes = [o for o in scene.objects if o.type == "MESH"]
assert meshes, "no mesh in GLB"

lo = Vector((1e9, 1e9, 1e9))
hi = Vector((-1e9, -1e9, -1e9))
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        lo = Vector((min(lo[i], w[i]) for i in range(3)))
        hi = Vector((max(hi[i], w[i]) for i in range(3)))
size = hi - lo
mid = (lo + hi) / 2
# Orbit radius from the bounding SPHERE, so the camera never clips a shoulder at 45 deg
# even though the framing box was measured head-on.
radius = max(size.x, size.y) * 3.0

cam_data = bpy.data.cameras.new("cam")
cam_data.type = "ORTHO"
# 1.204, not v21's 1.08. MEASURED against the renders this has to line up with: the
# reference figure is 852 px tall in a 1024 px frame and v21's framing gives 950 px, so
# the margin was calibrated to the existing set rather than guessed (1.08 * 950/852).
cam_data.ortho_scale = size.z * 1.204
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam

scene.render.resolution_x = args.w
scene.render.resolution_y = args.h
scene.render.image_settings.file_format = "PNG"
scene.render.engine = "BLENDER_WORKBENCH"
sh = scene.display.shading
sh.light = "FLAT" if args.flat else "STUDIO"
# ALWAYS Standard. An earlier version inferred AgX from the reference renders' darker
# background (118 vs 151) -- WRONG, and the error is instructive: the Workbench viewport
# background does NOT pass through the view transform, so it cannot testify about it. The
# FIGURE does, and it is 2x apart: AgX put the figure's mean at 52/255 where the reference
# sits at 100. Calibrate on the thing that responds to the knob, not the thing beside it.
scene.view_settings.view_transform = "Standard"
scene.view_settings.exposure = args.exposure
sh.background_color = (0.181, 0.181, 0.188)   # measured to land at the reference's 118/255
sh.color_type = "SINGLE" if args.clay else "TEXTURE"
sh.show_cavity = False
sh.background_type = "VIEWPORT"
# EXPLICIT, and load-bearing. With world-space lighting the camera orbit walks the figure
# through a fixed light, so the back views come back ~3x darker and ~3.5x less saturated --
# measured on the previous renders (front 100/255 -> back 32/255). That is a lighting
# artifact, NOT a texture defect: under FLAT the back reads 62.7 against the front's 63.0.
# A turnaround fed to a restylize must be lit identically per view or the sprite set
# inherits a shadow gradient nothing in the asset justifies.
sh.use_world_space_lighting = False


for idx in [int(v) for v in args.views.split(",")]:
    # View 0 looks along +Y (glTF front faces -Y after import). Positive index steps the
    # camera around +Z; the convention is CHECKED against the existing renders rather than
    # assumed -- see the sanity diff in the session record.
    th = math.radians(idx * args.step + args.yaw_offset)
    cam.location = (mid.x + radius * math.sin(th),
                    mid.y - radius * math.cos(th),
                    mid.z)
    cam.rotation_euler = (math.radians(90), 0, th)
    scene.render.filepath = f"{args.out}/{args.tag}_{idx}.png"
    bpy.ops.render.render(write_still=True)
    print(f"[turn] view {idx}  yaw {idx*args.step + args.yaw_offset:6.1f}deg  -> {args.tag}_{idx}.png", flush=True)
