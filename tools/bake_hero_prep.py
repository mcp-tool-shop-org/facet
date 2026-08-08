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
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import subject_profile
import hashlib
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
                     "MEASURED to move island count by 0.8%% and change nothing: "
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
ap.add_argument("--reunwrap", action="store_true",
                help="DELETE the incoming UV layer and rebuild it with smart_project. "
                     "This was the default until E05 and is kept only to reproduce "
                     "historical runs — it discards a finished atlas to build a worse "
                     "one. TRELLIS ships xatlas UVs and smart_decimate carries them "
                     "through the cut; measured on the same 287,170-face W3 mesh, "
                     "xatlas gives 14,010 islands (20.5 faces each) where smart_project "
                     "gives 34,783 (8.3). Island size decides whether the dilation fill "
                     "stays inside a region that belongs together: at 8 faces an island "
                     "is small enough to be entirely unpainted, and 54.6%% of them were. "
                     "Keeping the native atlas painted 923,466 texels against 711,183, "
                     "dropped colourless-island hole texels 14.2 points, and put speckle "
                     "below the rejected A0 asset at two of three thresholds where the "
                     "smart_project path was worse than A0 at all three. Native UVs are "
                     "now the default; this flag is the escape hatch, not the route.")
ap.add_argument("--head-scale", type=float, default=3.0)
ap.add_argument("--no-head-scale", action="store_true",
                help="skip the head-island scale because the INPUT is already "
                     "density-allocated (smart_decimate has run). Both stages "
                     "allocate to the same face rect; composed, they double-subscribe.")
ap.add_argument("--bound", type=float, default=0.55)
ap.add_argument("--visible-mask",
                help="bool .npy from cull_unseen.py, one entry per face. Only visible "
                     "faces are unwrapped and packed; the rest collapse onto ONE shared "
                     "patch in a reserved strip. E05 measured that 49%% of valid atlas "
                     "texels are never visible from any of 46 exterior cameras, and for a "
                     "prerendered deliverable that surface is paid for three times — "
                     "texels in the atlas, a hole in the map, and a dilation that bleeds "
                     "into whatever island the packer placed beside it. Excluding rather "
                     "than DELETING is deliberate: the geometry is never modified, so the "
                     "silhouette cannot change and a camera nobody anticipated sees a flat "
                     "patch instead of straight through the body.")
ap.add_argument("--unseen-strip", type=float, default=24.0,
                help="texel rows reserved at the top of the atlas for the shared unseen "
                     "patch, so it can never collide with a packed island")
args = ap.parse_args(subject_profile.bind(ap, "bake_hero_prep.py", argv))
os.makedirs(args.outdir, exist_ok=True)
CX0, CY0, CX1, CY1 = [float(v) for v in args.crop.split(",")]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=args.glb)
meshes = [o for o in scene.objects if o.type == "MESH"]
if not (meshes):
    raise AssertionError("ANDON: no mesh in GLB")
bpy.ops.object.select_all(action="DESELECT")
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = obj.data

# ---- visible-face mask, and PROOF it still lines up with this mesh ----
# The mask is indexed by glTF face order. Blender preserves that order on import
# (measured: max centroid deviation 5.6e-8 over 287,170 faces), but "measured once" is
# not a guarantee across Blender versions or exporters, and a silently misaligned mask
# would exclude the WRONG faces — a failure with no visible symptom until the atlas is
# already wrong. So the mask carries a checksum of the face centroids it was built
# against, and it is checked here.
nf0 = len(me.polygons)
_co = np.empty(len(me.vertices) * 3, dtype=np.float32)
me.vertices.foreach_get("co", _co)
_co = _co.reshape(-1, 3)
_maxabs = float(np.abs(_co).max())
_cent = np.empty(nf0 * 3, dtype=np.float32)
me.polygons.foreach_get("center", _cent)
_cent = (_cent.reshape(-1, 3) / _maxabs * 0.5).astype(np.float64)

vis_face = np.ones(nf0, dtype=bool)
if args.visible_mask:
    vis_face = np.load(args.visible_mask)
    if not (vis_face.shape == (nf0,)):
        raise AssertionError(
            f"ANDON: visible mask has {vis_face.shape} entries for {nf0:,} faces — it was "
            f"built against a different mesh")
    # Compare face centroids POSITIONALLY, not by hash. This mesh is read through
    # Blender's float32 polygon.center where the mask was built from trimesh's float64
    # vertices; the two agree to ~5e-8, which is geometrically nothing but straddles any
    # rounding boundary, so an exact hash mismatches on a perfectly aligned mask. A mask
    # shuffled by even one face moves a centroid by roughly an edge length (0.0029 median
    # on W3), thousands of times the float noise, so a tolerance separates the two cases
    # cleanly.
    cpath = os.path.splitext(args.visible_mask)[0] + "_centroids.npy"
    if not (os.path.exists(cpath)):
        raise AssertionError(
            f"ANDON: {os.path.basename(cpath)} is missing, so the mask cannot be proved to "
            f"line up with this mesh. Re-run cull_unseen.py to emit it.")
    ref = np.load(cpath).astype(np.float64)
    if not (ref.shape == _cent.shape):
        raise AssertionError(
            f"ANDON: centroid record is {ref.shape} against this mesh's {_cent.shape}")
    dev = float(np.abs(ref - _cent).max())
    if not (dev < 1e-4):
        raise AssertionError(
            f"ANDON: face centroids deviate by up to {dev:.3e} from the mesh the mask was "
            f"built against — far above float noise and comparable to the mesh's own edge "
            f"length. The face order or the mesh changed, and the mask would exclude the "
            f"wrong faces silently.")
    print(f"[prep] visible mask lines up with this mesh (max centroid deviation "
          f"{dev:.2e})", flush=True)
    print(f"[prep] visible mask: {int(vis_face.sum()):,}/{nf0:,} faces "
          f"({vis_face.mean()*100:.1f}%) will be unwrapped and packed; "
          f"{int((~vis_face).sum()):,} collapse to one shared patch", flush=True)

if not args.reunwrap:
    if not (me.uv_layers):
        raise AssertionError(
            "ANDON: the input GLB carries no UV layer, so there is no native atlas to "
            "keep. Either the mesh lost its UVs upstream (smart_decimate carries them "
            "through the cut — check there first), or this input genuinely needs an "
            "unwrap, in which case pass --reunwrap deliberately.")
    me.uv_layers[0].name = "uv_bake"
    while len(me.uv_layers) > 1:
        for lay in me.uv_layers:
            if lay.name != "uv_bake":
                me.uv_layers.remove(lay)
                break
    me.uv_layers.active = me.uv_layers["uv_bake"]
    print("[prep] native UVs: using the atlas the mesh arrived with, no re-unwrap",
          flush=True)
else:
    print("[prep] --reunwrap: DISCARDING the mesh's own atlas for smart_project "
          "(historical path)", flush=True)
    while me.uv_layers:
        me.uv_layers.remove(me.uv_layers[0])
    uv_bake = me.uv_layers.new(name="uv_bake")
    if not (uv_bake is not None):
        raise AssertionError(
            "ANDON: uv_bake creation failed (8-layer cap returns None)")
    me.uv_layers.active = uv_bake
    # unwrap only what will be packed — an unseen face contributes nothing but
    # fragmentation to the chart layout
    me.polygons.foreach_set("select", vis_face.astype(np.int32))
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_mode(type="FACE")
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
if not (n_head > 500):
    raise AssertionError("ANDON: head band nearly empty — crop rect or projection is wrong")

# ---- UV island partition via union-find on welded UV corners ----
nl = len(me.loops)
luv = np.empty(nl * 2, dtype=np.float32)
uv_bake.data.foreach_get("uv", luv)
luv = luv.reshape(-1, 2)
if not (float(luv.var()) > 1e-6):
    raise AssertionError(
        "ANDON: UVs are uniform — smart_project produced nothing or the read is stale")
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
n_isl_vis = len(np.unique(roots[vis_face]))
print(f"[prep] islands total {n_isl:,} ({nf / max(n_isl, 1):.1f} faces/island); "
      f"head islands {len(head_roots):,} ({int(in_head_island.sum()):,} faces)",
      flush=True)
print(f"[prep] islands holding VISIBLE faces {n_isl_vis:,} "
      f"({int(vis_face.sum()) / max(n_isl_vis, 1):.1f} visible faces/island) — this is "
      f"what actually gets packed", flush=True)


def head_area_share(luv_flat):
    """Fraction of UV area held by head islands, over VISIBLE faces only — unseen faces
    collapse to a shared patch, so counting their area would understate the head."""
    uva_ = luv_flat.reshape(nf, 3, 2)
    a_ = 0.5 * np.abs((uva_[:, 1, 0] - uva_[:, 0, 0]) * (uva_[:, 2, 1] - uva_[:, 0, 1])
                      - (uva_[:, 2, 0] - uva_[:, 0, 0]) * (uva_[:, 1, 1] - uva_[:, 0, 1]))
    a_ = a_ * vis_face
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
me.polygons.foreach_set("select", vis_face.astype(np.int32))
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.uv.pack_islands(margin=args.pack_margin)
bpy.ops.object.mode_set(mode="OBJECT")
me = obj.data                      # stale again after the edit round trip
uv_bake = me.uv_layers["uv_bake"]

if args.visible_mask:
    # Reserve a strip at the top of the atlas and park every unseen face on ONE shared
    # patch inside it. Reserved rather than "somewhere in the corner" because pack_islands
    # fills [0,1] and any fixed point would eventually land on a real island — the unseen
    # faces would then sample a piece of the beard, which is the exact artifact class this
    # experiment exists to remove. The patch is a real triangle, not a degenerate point, so
    # the bake marks it valid and it carries a defined colour: a camera nobody anticipated
    # sees a flat patch rather than an untextured void.
    luv3 = np.empty(nl * 2, dtype=np.float32)
    uv_bake.data.foreach_get("uv", luv3)
    luv3 = luv3.reshape(-1, 2)
    strip = args.unseen_strip / args.res
    vis_loop = vis_face[loop_face]
    luv3[vis_loop, 1] *= (1.0 - strip)
    su, sz = 0.01, 10.0 / args.res
    sv = 1.0 - strip + 6.0 / args.res
    corners = np.array([[su, sv], [su + sz, sv], [su, sv + sz]], dtype=np.float32)
    n_unseen = int((~vis_face).sum())
    if n_unseen:
        luv3[np.where(~vis_loop)[0]] = np.tile(corners, (n_unseen, 1))
    uv_bake.data.foreach_set("uv", luv3.reshape(-1))
    me.update()
    print(f"[prep] {n_unseen:,} unseen faces parked on one {int(sz*args.res)}x"
          f"{int(sz*args.res)}-texel patch; visible UVs compressed into the lower "
          f"{(1-strip)*100:.2f}% of v", flush=True)

# verify the x3 survived the pack: head UV-area share must beat face-count share
luv2 = np.empty(nl * 2, dtype=np.float32)
uv_bake.data.foreach_get("uv", luv2)
luv2 = luv2.reshape(-1, 2)
tri = ltot.max() == 3
if not (tri):
    raise AssertionError("ANDON: non-triangle faces after GLB import")
uva = luv2.reshape(nf, 3, 2)
area = 0.5 * np.abs((uva[:, 1, 0] - uva[:, 0, 0]) * (uva[:, 2, 1] - uva[:, 0, 1])
                    - (uva[:, 2, 0] - uva[:, 0, 0]) * (uva[:, 1, 1] - uva[:, 0, 1]))
# every share below is over VISIBLE faces: the unseen ones share one patch, so their UV
# area is a fixed constant that says nothing about allocation, and their 3D area would
# make the head look starved when it is not
area = area * vis_face
share_area = float(area[in_head_island].sum() / max(area.sum(), 1e-12))
share_count = float((in_head_island & vis_face).sum() / max(int(vis_face.sum()), 1))
print(f"[prep] packed UV area covers {area.sum()*100:.2f}% of the atlas", flush=True)
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
                                       tri3[:, 2] - tri3[:, 0]), axis=1) * vis_face
    share_3d = float(a3[in_head_island].sum() / max(a3.sum(), 1e-12))
    print(f"[prep] head 3D-surface share {share_3d:.4f} — UV share must beat it "
          f"for the head to carry more texels per unit surface", flush=True)
    if not (share_area > share_3d):
        raise AssertionError(
            f"ANDON: --no-head-scale but the input puts no extra texels on the head — "
            f"head holds {share_area:.4f} of UV area for {share_3d:.4f} of surface "
            f"area; run smart_decimate first or drop --no-head-scale")
elif args.head_scale > 1.0:
    # the scaling must have moved area toward the head, judged against this
    # input's own starting distribution rather than a fixed multiple of face count
    if not (share_area > share_area_pre * 1.2):
        raise AssertionError(
            f"ANDON: head islands did not keep their x{args.head_scale:g} scale through "
            f"pack_islands ({share_area_pre:.4f} -> {share_area:.4f})")
elif args.head_scale == 1.0:
    # ALLOCATION NONE (E04 Ruling 14, allocation ruled NONE for the galleon; guard
    # specified in Ruling 15). A growth assert cannot be satisfied by the identity, and
    # the original one was written as though head_scale were always > 1 — a character
    # assumption that made a uniform atlas unexpressible and halted a correct bake
    # (E04 Arm T, ANDON 1, measured 0.2432 -> 0.2432). THE GUARD VERIFIES WHAT WAS
    # REQUESTED: at x1 the request is "change nothing", so what must hold is that the
    # identity SURVIVED pack_islands.
    #
    # TOLERANCE 1e-6 RELATIVE, ruled 2026-08-04 (E04 Ruling 16), derived from BOTH SIDES
    # of the line in the centroid-checksum pattern — never from the delta it judges.
    #
    #   noise  1.2e-07 relative. Blender stores UVs as float32; pack_islands may apply a
    #          global uniform scale, which cancels in a ratio but not in the last bits.
    #          Measured once at exactly 2 float32 ULPs (2^-25 at this magnitude).
    #   signal >= 3e-5 relative. One median island is the smallest event that can really
    #          move a share, and the guard's actual prey — a scale silently not surviving
    #          the pack — is factor-level, not last-bit.
    #
    # 1e-6 sits ~8x above the noise floor and >=30x below the smallest real signal. The
    # same number follows from ULP arithmetic and island geometry whatever any run printed.
    #
    # An earlier version of this clause asserted STRICT equality, on a ruling that read
    # "measured: exact" from a %.4f print of a float64 ratio. It fired at 2 ULPs. That
    # condition is WITHDRAWN as mis-derived rather than retuned — the distinction that
    # matters is that this bound comes from the two magnitudes above, not from the delta
    # that overturned it.
    _tol = 1e-6 * share_area_pre
    _delta = abs(share_area - share_area_pre)
    if not (_delta <= _tol):
        raise AssertionError(
            f"ANDON: head-scale 1.0 asks for the identity and pack_islands did not "
            f"preserve it — share_area {share_area!r} vs share_area_pre "
            f"{share_area_pre!r}, delta {_delta!r} against tolerance {_tol!r} "
            f"({_delta / max(share_area_pre, 1e-12):.3e} relative). HALT: report these "
            f"digits, do not choose a tolerance.")
    print(f"[prep] head-scale 1.0: identity survived pack_islands within tolerance "
          f"({share_area_pre:.9f} -> {share_area:.9f}, "
          f"{_delta / max(share_area_pre, 1e-12):.3e} relative against 1.0e-06) — "
          f"uniform atlas, no privileged region", flush=True)
else:
    # A shrink is not specified by any ruling. Refuse rather than invent a symmetric
    # clause: an unspecified guard that silently passes is how a value gets treated as
    # configured while checking nothing.
    raise AssertionError(
        f"ANDON: --head-scale {args.head_scale:g} < 1 is not specified. The growth "
        f"clause applies above 1 and the identity clause at exactly 1; a de-allocating "
        f"scale needs its own ruled condition before it can be verified.")

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
    if not (float(px_.var()) > 1e-8 or kind == "mask"):
        raise AssertionError(f"ANDON: {kind} bake is uniform")
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
if not (os.path.getsize(out_glb) > 100_000):
    raise AssertionError("ANDON: prep_uv.glb suspiciously small")
print(f"[prep] wrote {out_glb} ({os.path.getsize(out_glb)//1024} KB) — DONE", flush=True)
