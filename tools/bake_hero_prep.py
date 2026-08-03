"""Stage D part 1/3 — Blender prep for the hero ownership baker.

Does the Blender-only work, then hands everything to bake_hero_fuse.py (numpy/open3d):
  1. import GLB -> join -> apply transforms (mesh data == world == Z-up frame, which
     equals render_geomaps' "std" frame exactly: std = remap(gltf) = blender_zup)
  2. smart-UV at 4096 with island_margin 0.004 (16px gutters)
  3. HEAD-BAND island scale x3: head faces found by projecting face centers into the
     FRONT MV view (az -90, el 0, ortho bound 0.55) and testing against the face-crop
     rect — NOT by height, because the sword tip rises above the crown and every
     top-band instrument on this character captures the BLADE (measured trap)
  4. pack_islands (preserves relative island scale -> the x3 survives)
  5. EMIT bakes at 4096: encoded position, encoded normal, coverage mask -> .npy
     (float buffers, Non-Color; saved TOP-origin) + meta.json
  6. export the UV'd mesh as prep_uv.glb

Standards compliance: see bake_hero_fuse.py (one block for the 3-script stage).

  blender -b -P bake_hero_prep.py -- --glb mesh.glb --outdir DIR
          [--res 4096] [--crop 360,240,700,600] [--crop-res 1024] [--head-scale 3]
"""
import argparse
import json
import os
import sys

import bpy
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--outdir", required=True)
ap.add_argument("--res", type=int, default=4096)
ap.add_argument("--crop", default="360,240,700,600",
                help="face-crop rect x0,y0,x1,y1 in front-view pixels")
ap.add_argument("--crop-res", type=int, default=1024,
                help="resolution the crop rect is expressed in")
ap.add_argument("--angle-limit", type=float, default=1.15,
                help="smart_project split angle in radians. Raising it to 1.5 was "
                     "MEASURED to move island count by 0.8% and change nothing: "
                     "smart_project splits on UV DISTORTION as well as angle, and "
                     "decimation's long thin triangles distort whatever the "
                     "threshold. Kept as a flag; do not expect it to merge islands.")
ap.add_argument("--island-margin", type=float, default=0.001,
                help="smart_project margin. Every island pays this as a gutter, so "
                     "the cost scales with ISLAND COUNT, not mesh size: at 8 faces "
                     "per island the old 0.004 (16 px at 4096) wrapped ~20x20 px of "
                     "content in a ~52x52 footprint and packed 4.01%% of the atlas; "
                     "0.001 packs 18.76%%. Caveat: 4 px of gutter is thin at "
                     "aggressive mip levels — fine here because this route "
                     "pre-renders and the dilation fill extends past island borders.")
ap.add_argument("--pack-margin", type=float, default=0.001,
                help="pack_islands margin; same economics as --island-margin")
ap.add_argument("--keep-uvs", action="store_true",
                help="do NOT delete the incoming UV layer and re-unwrap — scale and "
                     "repack the atlas the mesh already carries. TRELLIS ships xatlas "
                     "UVs and smart_decimate carries them through the cut, so the "
                     "default path discards a finished atlas to build a worse one: "
                     "measured on the same 287,170-face W3 mesh, xatlas gives 14,010 "
                     "islands (20.5 faces each) where smart_project gives 34,783 (8.3). "
                     "Island size is what decides whether the dilation fill stays inside "
                     "a region that belongs together — at 8 faces an island is small "
                     "enough to be entirely unpainted, and 54.6%% of them were.")
ap.add_argument("--head-scale", type=float, default=3.0)
ap.add_argument("--no-head-scale", action="store_true",
                help="skip the head-island scale because the INPUT is already "
                     "density-allocated (smart_decimate has run). Both stages "
                     "allocate to the same face rect; composed, they double-subscribe.")
ap.add_argument("--bound", type=float, default=0.55)
args = ap.parse_args(argv)
os.makedirs(args.outdir, exist_ok=True)
CX0, CY0, CX1, CY1 = [float(v) for v in args.crop.split(",")]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=args.glb)
meshes = [o for o in scene.objects if o.type == "MESH"]
assert meshes, "ANDON: no mesh in GLB"
bpy.ops.object.select_all(action="DESELECT")
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = obj.data

if args.keep_uvs:
    assert me.uv_layers, ("ANDON: --keep-uvs but the input GLB carries no UV layer — "
                          "drop the flag, or check the mesh survived smart_decimate "
                          "with its UVs intact")
    me.uv_layers[0].name = "uv_bake"
    while len(me.uv_layers) > 1:
        for lay in me.uv_layers:
            if lay.name != "uv_bake":
                me.uv_layers.remove(lay)
                break
    me.uv_layers.active = me.uv_layers["uv_bake"]
    print("[prep] --keep-uvs: using the atlas the mesh arrived with, no re-unwrap",
          flush=True)
else:
    while me.uv_layers:
        me.uv_layers.remove(me.uv_layers[0])
    uv_bake = me.uv_layers.new(name="uv_bake")
    assert uv_bake is not None, \
        "ANDON: uv_bake creation failed (8-layer cap returns None)"
    me.uv_layers.active = uv_bake
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=args.angle_limit,
                             island_margin=args.island_margin)
    bpy.ops.object.mode_set(mode="OBJECT")
# mode_set rebuilds mesh data — every RNA reference from before is STALE (reading
# through one silently returns zeros; cost one ANDON round). Re-fetch after EVERY
# edit-mode round trip.
me = obj.data
uv_bake = me.uv_layers["uv_bake"]

# ---- head-band faces via FRONT-view projection (std frame == blender Z-up coords) ----
nv = len(me.vertices)
co = np.empty(nv * 3, dtype=np.float32)
me.vertices.foreach_get("co", co)
co = co.reshape(-1, 3)
maxabs = float(np.abs(co).max())
nf = len(me.polygons)
cent = np.empty(nf * 3, dtype=np.float32)
me.polygons.foreach_get("center", cent)
cent = cent.reshape(-1, 3)
std = cent / maxabs * 0.5
b = args.bound
px = (std[:, 0] + b) / (2 * b) * args.crop_res
py = (b - std[:, 2]) / (2 * b) * args.crop_res
head_face = (px >= CX0) & (px <= CX1) & (py >= CY0) & (py <= CY1)
n_head = int(head_face.sum())
print(f"[prep] head-band faces: {n_head:,}/{nf:,}", flush=True)
assert n_head > 500, "ANDON: head band nearly empty — crop rect or projection is wrong"

# ---- UV island partition via union-find on welded UV corners ----
nl = len(me.loops)
luv = np.empty(nl * 2, dtype=np.float32)
uv_bake.data.foreach_get("uv", luv)
luv = luv.reshape(-1, 2)
assert float(luv.var()) > 1e-6, \
    "ANDON: UVs are uniform — smart_project produced nothing or the read is stale"
lvert = np.empty(nl, dtype=np.int64)
me.loops.foreach_get("vertex_index", lvert)
lstart = np.empty(nf, dtype=np.int64)
ltot = np.empty(nf, dtype=np.int64)
me.polygons.foreach_get("loop_start", lstart)
me.polygons.foreach_get("loop_total", ltot)
loop_face = np.repeat(np.arange(nf, dtype=np.int64), ltot)

key = (lvert << 44) ^ ((luv[:, 0] * 5e5).round().astype(np.int64) << 22) \
      ^ (luv[:, 1] * 5e5).round().astype(np.int64)
order = np.argsort(key, kind="stable")
parent = np.arange(nf, dtype=np.int64)


def find(i):
    root = i
    while parent[root] != root:
        root = parent[root]
    while parent[i] != root:
        parent[i], i = root, parent[i]
    return root


sk = key[order]
sf = loop_face[order]
run_start = 0
for j in range(1, nl + 1):
    if j == nl or sk[j] != sk[run_start]:
        if j - run_start > 1:
            r0 = find(sf[run_start])
            for t in range(run_start + 1, j):
                r = find(sf[t])
                if r != r0:
                    parent[r] = r0
        run_start = j
roots = np.array([find(i) for i in range(nf)], dtype=np.int64)
head_roots = set(np.unique(roots[head_face]).tolist())
in_head_island = np.isin(roots, np.fromiter(head_roots, dtype=np.int64))
n_isl = len(np.unique(roots))
print(f"[prep] islands total {n_isl:,} ({nf / max(n_isl, 1):.1f} faces/island); "
      f"head islands {len(head_roots):,} ({int(in_head_island.sum()):,} faces)",
      flush=True)

def head_area_share(luv_flat):
    """Fraction of total UV area held by head islands."""
    uva_ = luv_flat.reshape(nf, 3, 2)
    a_ = 0.5 * np.abs((uva_[:, 1, 0] - uva_[:, 0, 0]) * (uva_[:, 2, 1] - uva_[:, 0, 1])
                      - (uva_[:, 2, 0] - uva_[:, 0, 0]) * (uva_[:, 1, 1] - uva_[:, 0, 1]))
    return float(a_[in_head_island].sum() / max(a_.sum(), 1e-12))


# The gate below compares against the INPUT's own distribution, not a fixed
# multiple of face count. Measured 2026-08-04: run on a mesh smart_decimate has
# already allocated, the head band is 80.7% of faces, and `share_area >
# share_count * 1.5` becomes arithmetically unreachable — the gate fires
# correctly on a mesh that is already right. Density allocation is idempotent by
# intent, not by construction, so the two stages must not both scale.
share_area_pre = head_area_share(luv)
print(f"[prep] head UV-area share before scaling {share_area_pre:.4f} "
      f"(face-count share {float(in_head_island.sum() / nf):.4f})", flush=True)

# scale head islands x3 about their own centroid (overlap is fine — pack fixes it)
loop_in_head = in_head_island[loop_face]
if args.no_head_scale:
    print("[prep] --no-head-scale: input is already density-allocated, "
          "leaving island scale alone", flush=True)
else:
    for r in head_roots:
        sel = (roots[loop_face] == r)
        c = luv[sel].mean(axis=0)
        luv[sel] = c + args.head_scale * (luv[sel] - c)
    uv_bake.data.foreach_set("uv", luv.reshape(-1))
    me.update()

scene.tool_settings.use_uv_select_sync = True
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.pack_islands(margin=args.pack_margin)
bpy.ops.object.mode_set(mode="OBJECT")
me = obj.data                      # stale again after the edit round trip
uv_bake = me.uv_layers["uv_bake"]

# verify the x3 survived the pack: head UV-area share must beat face-count share
luv2 = np.empty(nl * 2, dtype=np.float32)
uv_bake.data.foreach_get("uv", luv2)
luv2 = luv2.reshape(-1, 2)
tri = ltot.max() == 3
assert tri, "ANDON: non-triangle faces after GLB import"
uva = luv2.reshape(nf, 3, 2)
area = 0.5 * np.abs((uva[:, 1, 0] - uva[:, 0, 0]) * (uva[:, 2, 1] - uva[:, 0, 1])
                    - (uva[:, 2, 0] - uva[:, 0, 0]) * (uva[:, 1, 1] - uva[:, 0, 1]))
share_area = float(area[in_head_island].sum() / max(area.sum(), 1e-12))
share_count = float(in_head_island.sum() / nf)
print(f"[prep] head island UV-area share {share_area:.4f} vs face-count share "
      f"{share_count:.4f} (before scaling {share_area_pre:.4f})", flush=True)
if args.no_head_scale:
    # Nothing was scaled, so the question is whether the INPUT already puts texels
    # on the head. Compare UV area against 3D SURFACE area, not face count:
    # smart_decimate allocates POLYGONS, so the head carries many small triangles
    # and its face-count share says nothing about its texel density. Measured
    # 2026-08-04: head band 84.4% of faces but 44.8% of UV area on an allocated
    # mesh — comparing UV area to face count fires on a mesh that is already right.
    lidx = np.empty(nl, dtype=np.int64)
    me.loops.foreach_get("vertex_index", lidx)
    tri3 = co[lidx].reshape(nf, 3, 3)
    a3 = 0.5 * np.linalg.norm(np.cross(tri3[:, 1] - tri3[:, 0],
                                       tri3[:, 2] - tri3[:, 0]), axis=1)
    share_3d = float(a3[in_head_island].sum() / max(a3.sum(), 1e-12))
    print(f"[prep] head 3D-surface share {share_3d:.4f} — UV share must beat it "
          f"for the head to carry more texels per unit surface", flush=True)
    assert share_area > share_3d, (
        f"ANDON: --no-head-scale but the input puts no extra texels on the head — "
        f"head holds {share_area:.4f} of UV area for {share_3d:.4f} of surface "
        f"area; run smart_decimate first or drop --no-head-scale")
else:
    # the scaling must have moved area toward the head, judged against this
    # input's own starting distribution rather than a fixed multiple of face count
    assert share_area > share_area_pre * 1.2, (
        f"ANDON: head islands did not keep their x{args.head_scale:g} scale through "
        f"pack_islands ({share_area_pre:.4f} -> {share_area:.4f})")

# ---- EMIT bakes: encoded position, encoded normal, mask ----
lo = co.min(axis=0)
hi = co.max(axis=0)
size = np.maximum(hi - lo, 1e-9)
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 1
scene.render.bake.margin = 8
bake_img = bpy.data.images.new("bake_buf", args.res, args.res, alpha=False,
                               float_buffer=True)
bake_img.colorspace_settings.name = "Non-Color"
mat = bpy.data.materials.new("bakemat")
mat.use_nodes = True
me.materials.clear()
me.materials.append(mat)
nt = mat.node_tree


def bake_pass(kind):
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    emit = nt.nodes.new("ShaderNodeEmission")
    if kind == "mask":
        emit.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    else:
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        if kind == "pos":
            sub = nt.nodes.new("ShaderNodeVectorMath")
            sub.operation = "SUBTRACT"
            sub.inputs[1].default_value = tuple(lo)
            div = nt.nodes.new("ShaderNodeVectorMath")
            div.operation = "DIVIDE"
            div.inputs[1].default_value = tuple(size)
            nt.links.new(geo.outputs["Position"], sub.inputs[0])
            nt.links.new(sub.outputs[0], div.inputs[0])
            nt.links.new(div.outputs[0], emit.inputs["Color"])
        else:
            mad = nt.nodes.new("ShaderNodeVectorMath")
            mad.operation = "MULTIPLY_ADD"
            mad.inputs[1].default_value = (0.5, 0.5, 0.5)
            mad.inputs[2].default_value = (0.5, 0.5, 0.5)
            nt.links.new(geo.outputs["Normal"], mad.inputs[0])
            nt.links.new(mad.outputs[0], emit.inputs["Color"])
    nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bake_img
    uvn = nt.nodes.new("ShaderNodeUVMap")
    uvn.uv_map = "uv_bake"
    nt.links.new(uvn.outputs["UV"], tex.inputs["Vector"])
    nt.nodes.active = tex
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.bake(type="EMIT")
    px_ = np.array(bake_img.pixels[:], dtype=np.float32).reshape(args.res, args.res, 4)
    px_ = np.flipud(px_)[..., :3]          # save TOP-origin
    assert float(px_.var()) > 1e-8 or kind == "mask", f"ANDON: {kind} bake is uniform"
    np.save(os.path.join(args.outdir, f"{kind}.npy"), px_)
    print(f"[prep] baked {kind}  var={float(px_.var()):.6f}", flush=True)


for k in ("pos", "nor", "mask"):
    bake_pass(k)

meta = {"res": args.res, "lo": lo.tolist(), "hi": hi.tolist(),
        "maxabs": maxabs, "bound": b,
        "crop": [CX0, CY0, CX1, CY1], "crop_res": args.crop_res,
        "head_scale": args.head_scale,
        "head_uv_area_share": share_area, "head_face_share": share_count}
with open(os.path.join(args.outdir, "meta.json"), "w") as fh:
    json.dump(meta, fh, indent=1)

out_glb = os.path.join(args.outdir, "prep_uv.glb")
bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.gltf(filepath=out_glb, use_selection=True, export_format="GLB")
# floor sized to catch an EMPTY export, not a small mesh (char2 is 4.9k faces and
# its legitimate GLB is ~300KB; the warrior's is 30MB — mesh-relative is meaningless
# here, the bake-variance asserts above are the real defect gates)
assert os.path.getsize(out_glb) > 100_000, "ANDON: prep_uv.glb suspiciously small"
print(f"[prep] wrote {out_glb} ({os.path.getsize(out_glb)//1024} KB) — DONE", flush=True)
