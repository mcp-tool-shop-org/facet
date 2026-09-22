"""Pose a Tripo/Mixamo rig by aligning named bones to stated world directions.

No guessed Euler axes. For each bone the script measures its CURRENT world direction
(tail - head), computes the rotation that takes it to a STATED target direction, and
applies that rotation in pose space. The axis convention of the incoming skeleton therefore
never has to be known or assumed - which is the whole reason the first four prop placements
failed, in a different guise.

  blender -b -P pose_rig.py -- --glb rigged.glb --out posed.glb [--report]
                              [--set mixamorig:LeftArm=0.35,-0.90,-0.25] ...
"""
import argparse
import sys

import bpy
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", default=None)
ap.add_argument("--report", action="store_true", help="print the armature and write nothing")
ap.add_argument("--set", action="append", default=[],
                help="bone=x,y,z  target world direction for that bone (Blender frame)")
args = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=args.glb)
arms = [o for o in bpy.context.scene.objects if o.type == "ARMATURE"]
if len(arms) != 1:
    raise SystemExit("ANDON: expected exactly one armature, got %d" % len(arms))
arm = arms[0]
bpy.context.view_layer.objects.active = arm

if args.report:
    bpy.ops.object.mode_set(mode="POSE")
    print("armature %r  bones %d  world matrix scale %s"
          % (arm.name, len(arm.pose.bones), [round(v, 5) for v in arm.matrix_world.to_scale()]))
    for pb in sorted(arm.pose.bones, key=lambda b: -(arm.matrix_world @ b.head).z):
        h = arm.matrix_world @ pb.head
        t = arm.matrix_world @ pb.tail
        d = (t - h)
        L = d.length
        u = d.normalized() if L > 1e-9 else Vector((0, 0, 0))
        print("  %-28s head %7.4f %7.4f %7.4f   dir %6.3f %6.3f %6.3f   len %.4f  parent %s"
              % (pb.name, h.x, h.y, h.z, u.x, u.y, u.z, L,
                 pb.parent.name if pb.parent else "-"))
    raise SystemExit(0)

if not args.out:
    raise SystemExit("ANDON: --out is required unless --report")

bpy.ops.object.mode_set(mode="POSE")
by_name = {pb.name: pb for pb in arm.pose.bones}
for spec in args.set:
    name, _, vec = spec.partition("=")
    if name not in by_name:
        raise SystemExit("ANDON: no bone %r in this armature (have %d)" % (name, len(by_name)))
    target = Vector([float(v) for v in vec.split(",")]).normalized()
    pb = by_name[name]
    # current world direction of the bone
    M = arm.matrix_world @ pb.matrix
    cur = (arm.matrix_world @ pb.tail - arm.matrix_world @ pb.head).normalized()
    rot = cur.rotation_difference(target).to_matrix().to_4x4()
    # re-seat the bone's world matrix with that rotation applied about its head
    head_w = arm.matrix_world @ pb.head
    T = Matrix.Translation(head_w) @ rot @ Matrix.Translation(-head_w)
    pb.matrix = arm.matrix_world.inverted() @ (T @ M)
    bpy.context.view_layer.update()
    got = (arm.matrix_world @ pb.tail - arm.matrix_world @ pb.head).normalized()
    err = got.angle(target) * 57.2957795
    print("  %-28s -> %6.3f %6.3f %6.3f   (asked %6.3f %6.3f %6.3f, error %.3f deg)"
          % (name, got.x, got.y, got.z, target.x, target.y, target.z, err))
    if err > 1.0:
        raise SystemExit("ANDON: %s did not reach its target direction (%.3f deg off). "
                         "A constrained or inherited bone cannot be aimed this way."
                         % (name, err))

bpy.ops.object.mode_set(mode="OBJECT")

# BAKE THE POSE INTO GEOMETRY, and export that alone.
#
# A facing render needs the DEFORMED mesh, not a rig plus a pose. Exporting the armature
# and hoping the consumer applies the pose is how a figure ends up rendered in its bind
# pose without anyone noticing - the file looks right in one viewer and wrong in the next.
# Evaluating the depsgraph gives the deformed vertices as plain geometry, which is
# unambiguous. The rigged GLB stays on disk for the next pose.
# BAKE THE POSE INTO GEOMETRY, and export that alone.
#
# A facing render needs the DEFORMED mesh, not a rig plus a pose: a file that carries a rig
# and expects the consumer to apply the pose renders correctly in one viewer and in the bind
# pose in the next, with nothing to say which happened.
#
# Done with duplicate + modifier_apply, which is the operator that owns this problem.
# An earlier version built the mesh with `bpy.data.meshes.new_from_object(evaluated)` and
# then re-seated matrix_world by hand; that double-applied the transform and exported a
# 1.90 x 2.00 x 2.00 box with 2,669 vertices that were not in the input. Measured, not
# guessed - the bbox check below is what caught it and it stays as a gate.
# Only meshes actually SKINNED to the armature. Tripo's rigged output ships a stray
# unskinned 42-vertex Icosphere at +/-1.0 alongside the body - measured, not guessed - and
# taking every MESH object blew the baked bbox to 1.90 x 2.00 x 2.00 and tripped the size
# gate below. The discriminator is semantic rather than a name or a size threshold: a mesh
# this pose applies to is one the armature deforms.
src = [o for o in bpy.context.scene.objects
       if o.type == "MESH" and any(m.type == "ARMATURE" for m in o.modifiers)]
skipped = [o.name for o in bpy.context.scene.objects
           if o.type == "MESH" and o not in src]
if skipped:
    print("  skipping %d unskinned mesh(es): %s" % (len(skipped), ", ".join(skipped)))
if not src:
    raise SystemExit("ANDON: no ARMATURE-skinned mesh to bake")
before = sum(len(o.data.vertices) for o in src)

baked = []
for o in src:
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.duplicate()
    dup = bpy.context.view_layer.objects.active
    for m in list(dup.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)
    dup.parent = None
    baked.append(dup)

import mathutils
lo = mathutils.Vector((1e9, 1e9, 1e9)); hi = mathutils.Vector((-1e9, -1e9, -1e9))
after = 0
for o in baked:
    after += len(o.data.vertices)
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        lo = mathutils.Vector((min(lo[i], w[i]) for i in range(3)))
        hi = mathutils.Vector((max(hi[i], w[i]) for i in range(3)))
size = [hi[i] - lo[i] for i in range(3)]
print("BAKED %d vertices (input had %d)  bbox %s .. %s  size %s"
      % (after, before, [round(v, 4) for v in lo], [round(v, 4) for v in hi],
         [round(v, 4) for v in size]))

# Gates. Posing moves vertices; it does not create them, and it does not make a figure
# taller than it was. Both of these fired on the first implementation.
if after != before:
    raise SystemExit("ANDON: bake changed the vertex count, %d -> %d. Posing deforms a mesh, "
                     "it does not add to it." % (before, after))
if max(size) > 1.25 or max(size) < 0.75:
    raise SystemExit("ANDON: baked figure is %.4f on its longest axis. A posed reconstruction "
                     "should stay near 1.0; this is a transform applied twice."
                     % max(size))

bpy.ops.object.select_all(action="DESELECT")
for o in baked:
    o.select_set(True)
bpy.context.view_layer.objects.active = baked[0]
bpy.ops.export_scene.gltf(filepath=args.out, export_format="GLB", use_selection=True,
                          export_animations=False)
print("WROTE %s" % args.out)
