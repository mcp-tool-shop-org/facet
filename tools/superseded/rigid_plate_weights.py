"""SUPERSEDED 2026-09-22 - this does NOT fix the tearing it was built for. Kept, with the
measurement, so the approach does not quietly become doctrine again.

WHAT WAS TRIED AND WHAT IT DID, all on one rig with one variable, judged on the same front
view of the same 110 deg arm rotation:

    no repair                     shoulders shredded
    rigid bind, shells <  5%      INDISTINGUISHABLE from no repair
    rigid bind, shells < 20%      WORSE - the arm armour stays in the bind orientation
                                  while the arm moves, and detaches
    weight smoothing x8, f 0.50   spikes shorter and fewer; shoulders still torn

So the premise below is wrong. The tear is not a pauldron split between two bones across a
joint: rigid-binding every small shell changes nothing at all, which it could not do if
shell splitting were the mechanism. The spikes are single vertices bound to a distant bone
while their neighbours are not - a per-vertex artifact INSIDE the one large shell, which
this tool deliberately leaves alone - and smoothing only shortens them.

The shell census it prints is still accurate and still useful (1,447 shells on Drell, the
largest 27.99%, and the four next largest carrying dominant shares of only 0.19-0.29), so
--report is worth keeping. The repair is not.

---

Rigid-bind the small shells of an armoured figure, so plates stop tearing.

THE DEFECT, measured 2026-09-22. Rotating Tripo's auto-rigged upper arm ~110 deg to reach a
shipping pose SHREDS the shoulders - pauldrons torn into spikes - while ~20 deg is clean.
The mechanism is visible in this reconstruction class: the armour's plates are SEPARATE
SHELLS, and an auto-rigger blends each shell's vertices across whatever bones are near, so a
pauldron ends up half-weighted to the torso and half to the arm and comes apart between them.

THE FIX IS PHYSICAL, NOT COSMETIC. A plate is a rigid body. It should move with exactly one
bone, and a smooth blend across a joint is wrong for it in a way it is not wrong for flesh.
So: every connected shell smaller than --max-shell of the mesh is bound rigidly to its own
dominant bone - the one its vertices already weight most - and the large shell that is the
body keeps its blended weights, because a torso genuinely does span joints.

WHAT THIS IS NOT. It is not weight painting and it is not a smoothing pass. It makes one
decision per shell, from the weights the rigger already produced, and it cannot invent a
bone the rigger did not choose. A shell that the rigger got wrong stays wrong, rigidly.

  blender -b -P rigid_plate_weights.py -- --glb rigged.glb --out repaired.glb
                                          [--max-shell 0.05] [--report]
"""
import argparse
import sys
from collections import defaultdict

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", default=None)
ap.add_argument("--max-shell", type=float, default=0.05,
                help="a shell at or below this fraction of the mesh's faces is treated as a "
                     "rigid plate. Above it, the shell keeps its blended weights because a "
                     "body shell genuinely spans joints. Stated, not derived from the "
                     "result being judged.")
ap.add_argument("--report", action="store_true", help="print the shells and write nothing")
ap.add_argument("--smooth", type=int, default=0,
                help="iterations of vertex-weight smoothing over ALL groups, run AFTER any "
                     "rigid binding. This is the remedy for the defect rigid binding turned "
                     "out NOT to fix: spikes radiating from the shoulder are single vertices "
                     "bound to a distant bone while their neighbours are not, which is a "
                     "per-vertex artifact inside one shell, not a split between shells.")
ap.add_argument("--smooth-factor", type=float, default=0.5)
args = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=args.glb)

# Only meshes the armature actually deforms. Tripo ships a stray unskinned Icosphere.
meshes = [o for o in bpy.context.scene.objects
          if o.type == "MESH" and any(m.type == "ARMATURE" for m in o.modifiers)]
if len(meshes) != 1:
    raise SystemExit("ANDON: expected exactly one skinned mesh, got %d" % len(meshes))
obj = meshes[0]
me = obj.data
groups = {g.index: g.name for g in obj.vertex_groups}
if not groups:
    raise SystemExit("ANDON: the mesh carries no vertex groups, so it is not skinned")

# connected components over the edge graph
parent = list(range(len(me.vertices)))


def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a


def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra


for e in me.edges:
    union(e.vertices[0], e.vertices[1])

shells = defaultdict(list)
for v in me.vertices:
    shells[find(v.index)].append(v.index)
shells = sorted(shells.values(), key=len, reverse=True)
total_v = len(me.vertices)
limit = args.max_shell * total_v

print("mesh %r  vertices %d  shells %d  largest %d (%.2f%%)  threshold %d verts (%.1f%%)"
      % (obj.name, total_v, len(shells), len(shells[0]),
         100.0 * len(shells[0]) / total_v, int(limit), 100.0 * args.max_shell))


def dominant(idxs):
    """Which bone do these vertices already weight most? Sum, do not count."""
    tally = defaultdict(float)
    for i in idxs:
        for g in me.vertices[i].groups:
            tally[g.group] += g.weight
    if not tally:
        return None, 0.0
    gi = max(tally, key=tally.get)
    return gi, tally[gi] / max(1e-9, sum(tally.values()))


small = [s for s in shells if len(s) <= limit]
print("  %d shells at or below the threshold, %d vertices in them (%.2f%% of the mesh)"
      % (len(small), sum(len(s) for s in small),
         100.0 * sum(len(s) for s in small) / total_v))

if args.report:
    print("\n  the fifteen largest shells:")
    for s in shells[:15]:
        gi, share = dominant(s)
        print("    %7d verts (%5.2f%%)  %-28s dominant share %.3f  %s"
              % (len(s), 100.0 * len(s) / total_v, groups.get(gi, "-"), share,
                 "RIGID" if len(s) <= limit else "kept blended"))
    raise SystemExit(0)

if not args.out:
    raise SystemExit("ANDON: --out is required unless --report")

rigidified = 0
moved = 0
for s in small:
    gi, share = dominant(s)
    if gi is None:
        continue
    name = groups[gi]
    vg = obj.vertex_groups[name]
    others = [obj.vertex_groups[groups[k]] for k in groups if k != gi]
    for o in others:
        o.remove(s)
    vg.add(s, 1.0, "REPLACE")
    rigidified += 1
    moved += len(s)

if args.smooth:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
    bpy.ops.object.vertex_group_smooth(group_select_mode="ALL",
                                       factor=args.smooth_factor,
                                       repeat=args.smooth)
    bpy.ops.object.mode_set(mode="OBJECT")
    print("  smoothed all vertex groups, %d iteration(s) at factor %.2f"
          % (args.smooth, args.smooth_factor))

# Gates. Re-weighting must not move a vertex, lose one, or leave one unweighted.
if len(me.vertices) != total_v:
    raise SystemExit("ANDON: vertex count changed during re-weighting")
unweighted = [v.index for v in me.vertices if not v.groups]
if unweighted:
    raise SystemExit("ANDON: %d vertices carry no weight at all after re-weighting; "
                     "they would collapse to the origin" % len(unweighted))
bad = [v.index for v in me.vertices if abs(sum(g.weight for g in v.groups) - 1.0) > 1e-3]
if bad:
    raise SystemExit("ANDON: %d vertices do not sum to weight 1.0 (first: %d)"
                     % (len(bad), bad[0]))

print("  rigid-bound %d shells, %d vertices (%.2f%% of the mesh)"
      % (rigidified, moved, 100.0 * moved / total_v))

bpy.ops.object.select_all(action="DESELECT")
for o in bpy.context.scene.objects:
    o.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.gltf(filepath=args.out, export_format="GLB", use_selection=True,
                          export_animations=False)
print("WROTE %s" % args.out)
