"""E12 Ruling 9d — per-view element visibility, so the per-view stems are MEASURED not guessed.

Ruling 9d drops from a view's prompt any element whose surface that view cannot see, and
requires the split be verified against each view's actual render before the table is written.
This is the geometry half of that verification. The eye is the other half and neither
replaces the other: this tool cannot tell you an eye socket reads as an eye, and a render
cannot tell you 3 first-hit fang faces out of 384 is what you are squinting at.

WHAT IT MEASURES, per view, under the PROFILE's framing and `silhouette_masks`' own
arithmetic (Ruling 9a — an anchor is computed with the source's arithmetic, and so is
anything that has to line up with one):

  * first-hit faces in total, and their projected area in px
  * first-hit faces whose centroid lies inside the Gate 0 HEAD BOX, as a share of the head
    box's own faces and as px on screen. The box is a two-silhouette visual hull - a region
    of space, not a segmentation (E12 Gate 0's own caveat, carried) - so a neck or a horn
    sweeping through it counts. Read it as "is the head region facing this camera at all".
  * first-hit faces belonging to the FREE-STANDING SHELLS, which on this mesh are D10's
    fangs plus three micro-fragments (E12 Ruling 4c: 5 of 8 satellites, 384 of 396 faces are
    the fangs). This one is a real per-element measurement rather than a regional proxy,
    because D10's geometry is a distinct face set and nothing else occupies it.

WHAT IT DOES NOT DO. It does not decide the split, does not rank views, and does not know
which element occupies which face outside the shell census. D9 (tongue) and D11 (mouth
interior) have no distinct face set on this mesh, so this tool reports the head-box and fang
numbers that BOUND their visibility and says so; their split is decided at the crop, by eye.

  e12_view_visibility.py --glb prep_uv.glb --head-box head_00003.json --aspect 1792,1024
                         --fit-axis width --margin 1.204 --views 0,1,2,3,4,5,6,7
                         --renders DIR --tag dragonclay --out J.json [--crops DIR]

Standards compliance: PIN_PER_STEP - framing and camera come from flags matching the
profile's, echoed per view. ANDON_AUTHORITY - it gates nothing; a split is a ruling's, and
this is evidence for one. DECOMPOSE_BY_SECRETS - the head box is this subject's measured
region loaded from its own file, never a rect from another subject. EXTERNAL_VERIFIER - the
geometry answer and the crop it emits are independent channels on the same question, and the
crops exist precisely so the numbers can be contradicted by eye.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--head-box", required=True, help="Gate 0's head_*.json; box read in Blender frame")
ap.add_argument("--aspect", required=True)
ap.add_argument("--fit-axis", default="width", choices=["height", "width"])
ap.add_argument("--margin", type=float, default=1.204)
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--step", type=float, default=45.0)
ap.add_argument("--renders", default=None, help="dir of profile clay renders, for the crops")
ap.add_argument("--tag", default="dragonclay")
ap.add_argument("--crops", default=None, help="write one head-region crop per view here")
ap.add_argument("--out", required=True)
args = ap.parse_args()

W, H = (int(x) for x in args.aspect.split(","))
m = trimesh.load(args.glb, force="mesh", process=False)
v0 = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)

# silhouette_masks' own arithmetic, verbatim (Ruling 9a)
vmax = np.abs(v0).max()
vb = np.stack([v0[:, 0], -v0[:, 2], v0[:, 1]], axis=1) / vmax * 0.5
SCALE = 0.5 / vmax

blo, bhi = vb.min(0), vb.max(0)
bmid = (blo + bhi) / 2
if args.fit_axis == "height":
    v_ext = (bhi[2] - blo[2]) * args.margin
    h_ext = v_ext * (W / H)
else:
    h_ext = max(bhi[0] - blo[0], bhi[1] - blo[1]) * args.margin
    v_ext = h_ext * (H / W)

# the Gate 0 head box, carried into the same frame by the same uniform scale
hb = json.load(open(args.head_box, encoding="utf-8"))
box = np.asarray(hb["head_box_blender"], dtype=np.float64) * SCALE
print("[vis] head box (source frame): %s .. %s" % (np.round(box[0], 6).tolist(),
                                                   np.round(box[1], 6).tolist()), flush=True)

cent = vb[f].mean(axis=1)
in_box = np.all((cent >= box[0]) & (cent <= box[1]), axis=1)
print("[vis] faces in head box: %d / %d (%.3f%%)"
      % (in_box.sum(), len(f), in_box.mean() * 100), flush=True)

# free-standing shells: D10's fangs plus the micro-fragments (E12 Ruling 4c census)
#
# ⚠ WELD FIRST, and this is not optional. `prep_uv.glb` is an EXPORTED glTF, which splits a
# vertex at every UV seam, so `face_adjacency` on it is adjacency-across-shared-vertices on a
# mesh whose vertices were deliberately un-shared. Measured here before the weld was added:
# 29,048 components with the largest holding 9,015 faces, against Gate 0's 9 welded shells on
# the same geometry. That is the repo's standing "weld before decimating" constraint arriving
# at a second caller - a root cause has as many sites as it has callers - and it would have
# reported every UV island as a satellite.
#
# ⚠ AND THE CENSUS IS COMPUTED WITH `mesh_stats.py`'s OWN ARITHMETIC, because the number it
# has to agree with is `mesh_stats`' (Gate 0: 9 welded shells, 8 satellites, 396 faces). Two
# operands differ from the obvious defaults and both were measured wrong here first:
#
#   trimesh's merge_vertices() defaults to merge_tex=False, merge_norm=False, so on a mesh
#   whose seams exist precisely BECAUSE of differing UVs it welds almost nothing - measured
#   726,671 -> 723,216 verts, and the census still came back as 28,892 shells.
#   mesh_stats passes merge_tex=True, merge_norm=True.
#
#   mesh_stats builds components over SHARED VERTICES, not shared edges. face_adjacency is
#   shared-EDGE connectivity, which fragments a reconstruction into its UV islands: measured
#   29,048 components with the largest holding 9,015 faces, against a true 9.
#
# Same law as Ruling 9a, at a different site: an instrument that must line up with a recorded
# number is computed with the arithmetic that produced it.
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components as _cc

mw = m.copy()
mw.merge_vertices(merge_tex=True, merge_norm=True)
if not (len(mw.faces) == len(f)):
    raise AssertionError(
        "ANDON: welding changed the face count (%d -> %d); component labels would no longer "
        "address the same faces as the raycast scene" % (len(f), len(mw.faces)))
wf = np.asarray(mw.faces)
_e = np.vstack([wf[:, [0, 1]], wf[:, [1, 2]], wf[:, [2, 0]]])
_g = coo_matrix((np.ones(len(_e), dtype=np.int8), (_e[:, 0], _e[:, 1])),
                shape=(len(mw.vertices), len(mw.vertices)))
_, _lab = _cc(_g, directed=False)
face_lab = _lab[wf[:, 0]]
comp = [np.nonzero(face_lab == L)[0] for L in np.unique(face_lab)]
sizes = sorted((len(c) for c in comp), reverse=True)
print("[vis] welded for the shell census (merge_tex/merge_norm, shared-vertex components): "
      "%d verts -> %d, faces unchanged at %d, shells %d"
      % (len(m.vertices), len(mw.vertices), len(f), len(comp)), flush=True)
sat = np.zeros(len(f), bool)
sat_sizes = []
for c in comp:
    if len(c) != sizes[0]:
        sat[c] = True
        sat_sizes.append(len(c))
sat_sizes.sort(reverse=True)
print("[vis] shells: %d total, largest %d faces; satellites %s (%d faces)"
      % (len(comp), sizes[0], sat_sizes, int(sat.sum())), flush=True)

rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vb.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))

rows = {}
for k in [int(x) for x in args.views.split(",")]:
    th = np.radians(k * args.step)
    rgt = np.array([np.cos(th), np.sin(th), 0.0])
    dtc = np.array([np.sin(th), -np.cos(th), 0.0])
    look = -dtc
    up = np.cross(rgt, look)
    up = up / (np.linalg.norm(up) + 1e-12)
    gx = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    gy = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    g1, g2 = np.meshgrid(gx, gy)
    org = (bmid[None, None, :] + g1[..., None] * rgt[None, None, :]
           + g2[..., None] * up[None, None, :] - look[None, None, :] * 2.0)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    hit = np.isfinite(ans["t_hit"].numpy().reshape(H, W))
    pid = ans["primitive_ids"].numpy().reshape(H, W)

    seen = np.unique(pid[hit])
    seen_box = np.intersect1d(seen, np.nonzero(in_box)[0], assume_unique=False)
    seen_sat = np.intersect1d(seen, np.nonzero(sat)[0], assume_unique=False)
    px_box = int(np.isin(pid, seen_box).sum() & 0xFFFFFFFF) if len(seen_box) else 0
    px_box = int((hit & in_box[np.clip(pid, 0, len(f) - 1)]).sum())
    px_sat = int((hit & sat[np.clip(pid, 0, len(f) - 1)]).sum())

    # the head box's screen rectangle, for the crop
    corners = np.array([[x, y, z] for x in box[:, 0] for y in box[:, 1] for z in box[:, 2]])
    sx = (corners - bmid) @ rgt
    sy = (corners - bmid) @ up
    cx = (sx + h_ext / 2) / h_ext * W
    cy = (v_ext / 2 - sy) / v_ext * H
    rect = [int(max(0, cx.min())), int(max(0, cy.min())),
            int(min(W, cx.max())), int(min(H, cy.max()))]

    rows[str(k)] = {
        "yaw": k * args.step,
        "first_hit_faces": int(len(seen)),
        "figure_px": int(hit.sum()),
        "head_box_faces_seen": int(len(seen_box)),
        "head_box_faces_total": int(in_box.sum()),
        "head_box_seen_frac": round(float(len(seen_box)) / max(1, int(in_box.sum())), 6),
        "head_box_px": px_box,
        "head_box_px_frac_of_figure": round(px_box / max(1, int(hit.sum())), 6),
        "satellite_faces_seen": int(len(seen_sat)),
        "satellite_faces_total": int(sat.sum()),
        "satellite_px": px_sat,
        "head_rect_px": rect,
    }
    print("[vis] view %d yaw %5.1f  figure %7d px | head box: %6d/%6d faces seen "
          "(%5.2f%%), %6d px = %5.2f%% of figure | satellites: %3d/%d faces, %d px"
          % (k, k * args.step, rows[str(k)]["figure_px"], len(seen_box), int(in_box.sum()),
             100 * rows[str(k)]["head_box_seen_frac"], px_box,
             100 * rows[str(k)]["head_box_px_frac_of_figure"], len(seen_sat), int(sat.sum()),
             px_sat), flush=True)

    if args.crops and args.renders:
        rp = os.path.join(args.renders, "%s_%d.png" % (args.tag, k))
        if os.path.exists(rp):
            os.makedirs(args.crops, exist_ok=True)
            im = Image.open(rp).convert("RGB")
            pad = 40
            bx = (max(0, rect[0] - pad), max(0, rect[1] - pad),
                  min(W, rect[2] + pad), min(H, rect[3] + pad))
            im.crop(bx).save(os.path.join(args.crops, "head_%d.png" % k))

os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
with open(args.out, "w", encoding="utf-8") as fh:
    json.dump({"glb": os.path.abspath(args.glb), "aspect": [W, H],
               "fit_axis": args.fit_axis, "margin": args.margin, "scale": SCALE,
               "head_box_source_frame": box.tolist(),
               "satellite_face_sizes": sat_sizes, "views": rows}, fh, indent=1)
print("[vis] wrote %s" % args.out, flush=True)
print("[vis] NO SPLIT IS DECIDED HERE. These are the numbers a ruling's split is checked "
      "against, beside the crops.", flush=True)
