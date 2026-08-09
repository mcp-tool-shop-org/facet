"""E12 Gate 0 — a head crop render framed by a MEASURED box, not an inherited rect.

`tools/verify/head_render.py` frames its close-up from the front-view crop rect that
`smart_decimate` allocates against — a rectangle authored on one standing humanoid at the
character line's framing. On a beast that rect has not found the head, so this tool takes
the world box `e12_head_evidence.py` derived from the eye on this mesh's own renders and
frames exactly that. Nothing about the region is inherited.

The second reason not to reuse `head_render.py` is a real defect on any off-centre subject:
it orbits at `(cx + r sin th, mid.y - r cos th, cz)` — the head's x and z, but the WHOLE
MESH's y. At yaw 0 that is harmless because y is the view direction; at any other yaw the
head walks out of frame by the distance between the head and the body's centre in y. This
tool orbits the box's own centre in all three axes.

Workbench conventions are `turn_render.py`'s, deliberately: camera-relative STUDIO light,
Standard view transform, exposure 0.85, background 0.181 — so a head crop and the
turnaround it came from are the same render, closer up. `--clay` by standing rule, and
there is no texture on a raw reconstruction to hide behind anyway.

Standards compliance:
  PIN_PER_STEP — box, yaws, resolution and pad are explicit flags echoed per render.
  ANDON_AUTHORITY — raises on a degenerate box or an empty scene rather than rendering
    something and letting a human wonder what they are looking at.
  NAMED_COMPENSATORS — writes new PNGs under --out. Undo = delete them. Owner: the session
    running it.
  EXTERNAL_VERIFIER — it renders; it scores nothing. The Director's eye is the verifier.

  blender -b -P e12_head_render.py -- --glb m.glb --out DIR --tag head_00001
          --box x0,y0,z0,x1,y1,z1 [--views -40,0,40] [--res 1024] [--pad 1.20] [--clay]
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
ap.add_argument("--box", required=True,
                help="x0,y0,z0,x1,y1,z1 in Blender world coords - e12_head_evidence's "
                     "head_box_blender, flattened")
ap.add_argument("--views", default="0", help="camera yaw degrees; 0 = turn_render's view 0")
ap.add_argument("--res", type=int, default=1024)
ap.add_argument("--pad", type=float, default=1.20)
ap.add_argument("--ortho-scale", type=float, default=None,
                help="explicit ortho_scale, replacing the yaw-invariant span. For a "
                     "single-yaw frame whose scale was derived elsewhere and pre-registered.")
ap.add_argument("--res-y", type=int, default=None, help="vertical resolution; defaults to --res")
ap.add_argument("--flat", action="store_true")
ap.add_argument("--clay", action="store_true")
ap.add_argument("--exposure", type=float, default=0.85)
ap.add_argument("--bg", default="0.181,0.181,0.188")
args = ap.parse_args(argv)
# NOTE, paid for once: Blender's bundled Python has NO Pillow, so the composition step
# cannot live here. It is `e12_head_sheet.py`, run under the pipeline's own interpreter.

b = [float(v) for v in args.box.split(",")]
if not (len(b) == 6):
    raise AssertionError("ANDON: --box wants x0,y0,z0,x1,y1,z1")
lo, hi = Vector(b[:3]), Vector(b[3:])
d = hi - lo
if not (min(d) > 0):
    raise AssertionError("ANDON: degenerate head box %s" % (b,))
c = (lo + hi) / 2

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=args.glb)
meshes = [o for o in scene.objects if o.type == "MESH"]
if not (meshes):
    raise AssertionError("ANDON: no mesh in GLB")

mlo = Vector((1e9,) * 3)
mhi = Vector((-1e9,) * 3)
for o in meshes:
    for cn in o.bound_box:
        w = o.matrix_world @ Vector(cn)
        mlo = Vector((min(mlo[i], w[i]) for i in range(3)))
        mhi = Vector((max(mhi[i], w[i]) for i in range(3)))

# One ortho_scale for every yaw: the horizontal diagonal bounds the box's projected width at
# any camera angle, so the head cannot walk out of frame at 45 degrees the way a max-of-axes
# scale would let it.
span = max(math.hypot(d.x, d.y), d.z) * args.pad
if args.ortho_scale is not None:
    # ⚠ A SINGLE-YAW OVERRIDE, and the reason it exists rather than a re-tuned --pad.
    # The span above is the yaw-INVARIANT one: the horizontal diagonal bounds the box's
    # projected width at any camera angle, which is right for a multi-yaw sheet and
    # over-conservative for one view. E12 handoff 5's companion is a single yaw-0 frame whose
    # ortho_scale was PRE-REGISTERED from the route's own rule (turn_render --fit-axis width:
    # max(size.x, size.y) * margin) before the render existed. Reaching that number by
    # solving for --pad would have printed a padding of 0.82 and read as under-padding; this
    # flag states the substitution instead. Both values are printed so the swap is visible.
    print("[headr] ORTHO OVERRIDE: %.6f supplied, replacing the yaw-invariant %.6f "
          "(single-yaw frame; see the pre-registered derivation)"
          % (args.ortho_scale, span), flush=True)
    span = args.ortho_scale
radius = max(mhi.x - mlo.x, mhi.y - mlo.y, mhi.z - mlo.z) * 4.0

cam_data = bpy.data.cameras.new("cam")
cam_data.type = "ORTHO"
cam_data.sensor_fit = "VERTICAL"
cam_data.ortho_scale = span
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam

scene.render.resolution_x = args.res
scene.render.resolution_y = args.res_y or args.res
scene.render.image_settings.file_format = "PNG"
scene.render.engine = "BLENDER_WORKBENCH"
sh = scene.display.shading
sh.light = "FLAT" if args.flat else "STUDIO"
scene.view_settings.view_transform = "Standard"
scene.view_settings.exposure = args.exposure
sh.background_color = tuple(float(x) for x in args.bg.split(","))
sh.color_type = "SINGLE" if args.clay else "TEXTURE"
sh.show_cavity = False
sh.background_type = "VIEWPORT"
sh.use_world_space_lighting = False

print("[headr] box %s -> %s | centre %s | ortho_scale %.6f | orbit r %.4f"
      % ([round(v, 4) for v in lo], [round(v, 4) for v in hi],
         [round(v, 4) for v in c], span, radius), flush=True)

written = []
for yaw in [float(v) for v in args.views.split(",")]:
    th = math.radians(yaw)
    cam.location = (c.x + radius * math.sin(th),
                    c.y - radius * math.cos(th),
                    c.z)
    cam.rotation_euler = (math.radians(90), 0, th)
    scene.render.filepath = "%s/%s_y%+04d.png" % (args.out, args.tag, int(round(yaw)))
    bpy.ops.render.render(write_still=True)
    written.append((yaw, bpy.path.abspath(scene.render.filepath)))
    print("[headr] yaw %+.0f -> %s" % (yaw, scene.render.filepath), flush=True)
