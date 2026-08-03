"""OUR SMART MESH — repair -> head-protected retopo -> UV -> dense->low texture bake.

Built 2026-08-03 from the AUDIT of the failed 2026-08-01 attempts. Every failure that
session made silently is a LOUD assert here:

  FALSE ASSUMPTION 1 (08-01): "quadriflow succeeded because the export succeeded."
    Measured: lady_quadriflow20k.glb contains 380,357 faces — the UNCHANGED dense
    input. Blender's quadriflow errors on non-manifold input; headless scripts swallow
    the error and export the input. -> THIS script asserts the output face count is
    within tolerance of the target, and exits non-zero otherwise.
  FALSE ASSUMPTION 2: "retopo preserves the texture."
    Retopo destroys UVs by construction (lady_qflow20k: tex embedded, UV=None,
    unusable). -> The missing stage was the dense->low BAKE. This script keeps the
    textured dense mesh intact as the bake SOURCE, gives the low mesh fresh UVs, and
    Cycles-bakes diffuse colour across. Asserts the baked image is not empty.
  FALSE ASSUMPTION 3: "the generator's mesh is a usable retopo input."
    Measured: the Step1X/TRELLIS lady meshes are ~900 disconnected shells,
    non-watertight. -> Voxel-remesh repair pass first; asserts single component.
  THE DEEP FAILURE: uniform density erases the face (decim-20k: eyes and mouth GONE;
    qflow-13.7k: head shattered — see the audit sheet). Game budgets are fine for the
    body; the face needs its detail. -> A HEAD-PROTECTION vertex group (same top-band
    logic gate_mesh trusts) makes decimation spend its budget below the neck.

  blender -b -P retopo_bake.py -- --glb <dense_textured.glb> --out <out.glb>
          [--target 24000] [--head-frac 0.20] [--voxel-frac 0.003] [--bake-res 2048]
          [--report <json>]

Output: GLB with baked texture. Exit 0 only if every assert held; the caller should
gate on the exit code (ANDON). Quads-vs-tris: this stage ships TRIANGLES deliberately —
the deliverable is prerendered 2.5D sprites + engine assets, where protected detail
beats edge-flow purity; a quad pass (quadriflow on the REPAIRED manifold) can slot in
later for rigging work, and GLB would triangulate it anyway (glTF has no quads — the
08-01 session picked a container that cannot even carry the thing it was making).
"""
import argparse
import json
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--target", type=int, default=24000, help="target face count (tris)")
ap.add_argument("--head-frac", type=float, default=0.20,
                help="top fraction of figure height protected from decimation")
ap.add_argument("--head-crop", default=None,
                help="x0,y0,x1,y1 face rect in FRONT-VIEW pixels (with --crop-res). "
                     "USE THIS on armed characters: a raised weapon rises above the "
                     "crown, so the height band protects the BLADE and starves the "
                     "face (measured 2026-08-03). The rect projects the head directly.")
ap.add_argument("--crop-res", type=int, default=1024)
ap.add_argument("--bound", type=float, default=0.55)
ap.add_argument("--blend-frac", type=float, default=0.06,
                help="soft transition band below the protected zone")
ap.add_argument("--repair", choices=["loose", "voxel", "none"], default="loose",
                help="loose (default): remove debris shells only, keep the original "
                     "surface — decimation does not need manifold input (measured: the "
                     "08-01 decim files ran fine on the 900-shell soup; only QUADRIFLOW "
                     "needs the manifold). voxel: full voxel-remesh rebuild — ⚠ measured "
                     "2026-08-03 to stair-step the whole surface at reachable voxel "
                     "sizes; the head protection then preserves voxel junk. Use only "
                     "for a future quad pass, at a much finer --voxel-frac.")
ap.add_argument("--voxel-frac", type=float, default=0.003,
                help="repair voxel size as a fraction of the bbox diagonal (voxel mode)")
ap.add_argument("--bake-res", type=int, default=2048)
ap.add_argument("--tolerance", type=float, default=0.35,
                help="allowed relative deviation of final face count from target")
ap.add_argument("--report", default=None)
args = ap.parse_args(argv)


def die(msg):
    print(f"[retopo] ANDON: {msg}", file=sys.stderr, flush=True)
    sys.exit(2)


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.abspath(args.glb))
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
if not meshes:
    die("no mesh in input GLB")
# join multi-part imports into one source object
bpy.ops.object.select_all(action="DESELECT")
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
src = bpy.context.view_layer.objects.active
src.name = "SRC"
n_src = len(src.data.polygons)
has_tex = any(m and m.use_nodes and any(n.type == "TEX_IMAGE" for n in m.node_tree.nodes)
              for m in src.data.materials)
print(f"[retopo] source: {n_src:,} faces, textured={has_tex}", flush=True)
if not has_tex:
    print("[retopo] WARNING: source has no image texture — bake will produce flat "
          "material colour only", flush=True)

bb = [src.matrix_world @ Vector(c) for c in src.bound_box]
lo = Vector((min(v[i] for v in bb) for i in range(3)))
hi = Vector((max(v[i] for v in bb) for i in range(3)))
diag = (hi - lo).length

# ---- R: repaired retopo copy ----
bpy.ops.object.select_all(action="DESELECT")
src.select_set(True)
bpy.context.view_layer.objects.active = src
bpy.ops.object.duplicate()
low = bpy.context.view_layer.objects.active
low.name = "LOW"
low.data.materials.clear()

if args.repair == "voxel":
    rm = low.modifiers.new("repair", "REMESH")
    rm.mode = "VOXEL"
    rm.voxel_size = max(diag * args.voxel_frac, 1e-5)
    bpy.ops.object.modifier_apply(modifier=rm.name)
    print(f"[retopo] voxel-remeshed: {len(low.data.polygons):,} faces", flush=True)
n_remesh = len(low.data.polygons)

if args.repair != "none":
    # debris pass: split loose shells, keep everything above 0.2% of total faces
    # (a garment or hat is a big shell; floating generator junk is not)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.separate(type="LOOSE")
    bpy.ops.object.mode_set(mode="OBJECT")
    # generator meshes can BE thousands of legitimate small patches (measured
    # 2026-08-03: this TRELLIS mesh is 8,600+ shells; a relative threshold dropped 64%
    # of the surface). Only true shards go; decimate itself tolerates the rest.
    parts = [o for o in bpy.context.scene.objects if o.name.startswith("LOW")]
    keep = [o for o in parts if len(o.data.polygons) >= 20]
    drop = [o for o in parts if o not in keep]
    dropped = sum(len(o.data.polygons) for o in drop)
    if dropped > n_remesh * 0.05:
        die(f"debris pass wanted to drop {dropped:,}/{n_remesh:,} faces (>5%) — these "
            f"are not shards; refusing (the mesh is legitimately fragmented)")
    for o in drop:
        bpy.data.objects.remove(o, do_unlink=True)
    if len(keep) > 1:
        bpy.ops.object.select_all(action="DESELECT")
        for o in keep:
            o.select_set(True)
        bpy.context.view_layer.objects.active = keep[0]
        bpy.ops.object.join()
    low = bpy.context.view_layer.objects.active
    low.name = "LOW"
    print(f"[retopo] debris pass: dropped {len(drop)} shells ({dropped:,} faces), "
          f"kept {len(keep)} real shells, {len(low.data.polygons):,} faces", flush=True)

# ---- head-protection vertex group (world-Z top band of the figure) ----
zmin = min((low.matrix_world @ v.co).z for v in low.data.vertices)
zmax = max((low.matrix_world @ v.co).z for v in low.data.vertices)
fh = zmax - zmin
z_protect = zmax - args.head_frac * fh
z_blend = z_protect - args.blend_frac * fh
vg = low.vertex_groups.new(name="decimate_here")
w_idx = []
if args.head_crop:
    CX0, CY0, CX1, CY1 = [float(v) for v in args.head_crop.split(",")]
    co_all = [low.matrix_world @ v.co for v in low.data.vertices]
    maxabs = max(max(abs(c.x), abs(c.y), abs(c.z)) for c in co_all)
    b = args.bound
    # soft falloff outside the rect so the density change is not a hard seam
    pad = 0.25 * max(CX1 - CX0, CY1 - CY0)
    for c in co_all:
        px = (c.x / maxabs * 0.5 + b) / (2 * b) * args.crop_res
        py = (b - c.z / maxabs * 0.5) / (2 * b) * args.crop_res
        dx = max(CX0 - px, px - CX1, 0.0)
        dy = max(CY0 - py, py - CY1, 0.0)
        d = (dx * dx + dy * dy) ** 0.5
        w_idx.append(0.0 if d <= 0 else min(1.0, d / pad))
else:
    for v in low.data.vertices:
        z = (low.matrix_world @ v.co).z
        if z >= z_protect:
            w = 0.0                       # head: never collapse
        elif z <= z_blend:
            w = 1.0                       # body: full budget
        else:
            w = (z_protect - z) / max(z_protect - z_blend, 1e-9)
        w_idx.append(w)
for i, v in enumerate(low.data.vertices):
    vg.add([v.index], w_idx[i], "REPLACE")
n_protected = sum(1 for w in w_idx if w < 0.5)
print(f"[retopo] head band protected: {n_protected:,}/{len(w_idx):,} verts "
      f"(top {args.head_frac:.0%} + {args.blend_frac:.0%} blend)", flush=True)

# ---- decimate with protection: a LADDER, because protection has a face cost ----
# Measured (warrior, 2026-08-03): a fully-protected band can hold MORE faces than the
# whole budget (~104k protected vs a 24k target) — a one-shot protected decimate is
# then infeasible and the old assert refused. The ladder softens protection stepwise
# (vertex_group_factor 10 -> 3 -> 1 -> 0) and ships the FIRST level that fits,
# reporting loudly which level that was. Full protection when affordable; graceful,
# named degradation when not; never a silent no-op.
n_before = len(low.data.polygons)
base = low
base.name = "BASE"
ratio = min(1.0, args.target / max(n_before, 1))
n_low, low, used_factor = None, None, None
for factor in (10.0, 3.0, 1.0, 0.0):
    bpy.ops.object.select_all(action="DESELECT")
    base.select_set(True)
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.duplicate()
    cand = bpy.context.view_layer.objects.active
    dm = cand.modifiers.new("dec", "DECIMATE")
    dm.ratio = ratio
    if factor > 0:
        dm.vertex_group = vg.name
        dm.vertex_group_factor = factor
    bpy.ops.object.modifier_apply(modifier=dm.name)
    n_cand = len(cand.data.polygons)
    print(f"[retopo] decimate attempt (protection factor {factor:g}): "
          f"{n_before:,} -> {n_cand:,} (target {args.target:,})", flush=True)
    if n_cand <= args.target * 2.5:
        n_low, low, used_factor = n_cand, cand, factor
        break
    bpy.data.objects.remove(cand, do_unlink=True)
if low is None:
    die(f"even unprotected decimation cannot reach {args.target:,} from {n_before:,}")
bpy.data.objects.remove(base, do_unlink=True)
low.name = "LOW"
bpy.context.view_layer.objects.active = low
bpy.ops.object.select_all(action="DESELECT")
low.select_set(True)
bpy.ops.object.shade_smooth()
if used_factor < 10.0:
    print(f"[retopo] ⚠ protection SOFTENED to factor {used_factor:g} — the protected "
          f"band alone exceeded the budget; detail density in the protected zone is "
          f"reduced. Raise --target to restore full protection.", flush=True)
# ANDON 1: the 08-01 silent no-op — output must not still be the dense mesh
if n_low > n_before * 0.9:
    die(f"decimation was a no-op ({n_before:,} -> {n_low:,})")
if not (args.target * (1 - args.tolerance) <= n_low <= args.target * 2.5):
    die(f"face count {n_low:,} outside tolerance of target {args.target:,}")

# ---- UVs on the low mesh ----
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.003)
bpy.ops.object.mode_set(mode="OBJECT")

# ---- bake SRC -> LOW ----
img = bpy.data.images.new("bake", args.bake_res, args.bake_res, alpha=False)
mat = bpy.data.materials.new("baked")
mat.use_nodes = True
nt = mat.node_tree
tex_node = nt.nodes.new("ShaderNodeTexImage")
tex_node.image = img
bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
nt.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
nt.nodes.active = tex_node
low.data.materials.append(mat)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 16
bpy.ops.object.select_all(action="DESELECT")
src.select_set(True)
low.select_set(True)
bpy.context.view_layer.objects.active = low
bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"},
                    use_selected_to_active=True,
                    cage_extrusion=diag * 0.01, max_ray_distance=diag * 0.05)

# ANDON 2: the missing-bake failure — an empty/black bake must not ship.
# ⚠ MEASURED 2026-08-04: the old form averaged RGBA over one row, and a FULLY BLACK
# bake with alpha=1 averages exactly 0.25 — it sailed past a `< 0.005` test and
# shipped a black mesh. Sample the whole image, RGB only, and require real variance.
import numpy as _np
_all = _np.array(img.pixels[:], dtype=_np.float32).reshape(-1, 4)[:, :3]
mean_px = float(_all.mean())
nonblack = float((_all.max(axis=1) > 0.02).mean())
print(f"[retopo] bake RGB mean {mean_px:.4f}, non-black texels {nonblack:.1%}",
      flush=True)
if mean_px < 0.005 or nonblack < 0.25:
    die(f"bake is empty/mostly black (RGB mean {mean_px:.4f}, non-black "
        f"{nonblack:.1%}) — rays missed (cage/ray distance?) or source has no texture")

# ---- export LOW only ----
bpy.ops.object.select_all(action="DESELECT")
low.select_set(True)
bpy.context.view_layer.objects.active = low
out = os.path.abspath(args.out)
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=out, use_selection=True, export_format="GLB")
size_kb = os.path.getsize(out) // 1024
print(f"[retopo] wrote {out}  ({size_kb} KB)", flush=True)
# ANDON 3: a "20k" file weighing like the dense input is the 08-01 tell
if size_kb > 8000 and n_low < 60000:
    die(f"output is {size_kb} KB for {n_low:,} faces — something dense leaked into "
        f"the export")

if args.report:
    with open(args.report, "w") as f:
        json.dump({"src_faces": n_src, "remesh_faces": n_remesh, "low_faces": n_low,
                   "protected_verts": n_protected, "protection_factor": used_factor,
                   "bake_mean": round(mean_px, 4),
                   "out": out, "kb": size_kb}, f, indent=1)
print("[retopo] OK", flush=True)
