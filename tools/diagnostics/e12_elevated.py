"""Does this subject buy anything from elevated cameras? Measured, the ship's own method.

THE QUESTION. The ship's elevated pair (0/180 @ 40) was DERIVED from deck-coverage
raycasts, not inherited from the character's 55. This subject's up-facing surface is the
spread wing TOPS and the back - large, and unreadable from eye level in the same way decks
were. So: what fraction of up-facing surface do the eight eye-level cameras already reach,
and what does each candidate addition buy on top?

WHAT IS MEASURED, precisely. Up-facing means face normal z > `--up-min` (0.5 by default) in
the canonical frame. Coverage is **FIRST-HIT**, the same criterion `cull_unseen` uses: a face
counts as reached by a camera only if it is the first surface that camera's ray meets, so a
wing top hidden under another wing is not counted. Everything is weighted by **AREA, not face
count** - a reconstruction's faces are not uniform and a face-count share would report
whichever region happens to be finely tessellated.

GREEDY BY MARGINAL GAIN over the eye-level base, which is the ship's own selection method:
each round adds whichever candidate set buys the most currently-unreached up-facing area.

WHAT IT DOES NOT DO. It adopts nothing. If a winning candidate lies outside `cull_unseen`'s
default 26-camera superset, that is a union re-issue the ruling owns (E06's superset rule),
and this tool says so rather than deciding it.

  e12_elevated.py --glb prep_uv.glb [--aspect 1792,1024] [--up-min 0.5] [--out j.json]

Standards compliance: PIN_PER_STEP - every camera, threshold and frame lands in the JSON.
EXTERNAL_VERIFIER - reports coverage; rules nothing. ANDON_AUTHORITY - raises on a degenerate
camera basis rather than silently producing a wrong frame at the pole.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh

D = 2.0

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--aspect", default="1792,1024")
ap.add_argument("--margin", type=float, default=1.204)
ap.add_argument("--fit-axis", default="width", choices=["height", "width"])
ap.add_argument("--up-min", type=float, default=0.5)
ap.add_argument("--base", default="0,45,90,135,180,225,270,315",
                help="the eye-level yaws already owned by stage 1")
ap.add_argument("--rays-per-face", type=float, default=10.0,
                help="E14 Ruling 10a. The ray grid is DERIVED from the mesh so that "
                     "this many rays land on a mean-area face, instead of being "
                     "inherited from a generation frame that knows nothing about "
                     "tessellation. --aspect then supplies the frame's aspect RATIO "
                     "and this supplies its resolution. Default 10 is the density of "
                     "the recorded converged run (1440x6144 = 9.71 rays/face).")
ap.add_argument("--exact-grid", action="store_true",
                help="Use --aspect as literal pixel dimensions instead of deriving the "
                     "resolution. This is how a pre-E16 run is reproduced: the sword's "
                     "recorded ladder is --aspect 240,1024 --fit-axis height "
                     "--exact-grid. The density is printed and warned on either way.")
ap.add_argument("--out", default=None)
args = ap.parse_args()

W, H = (int(x) for x in args.aspect.split(","))
ASPECT_W0, ASPECT_H0 = W, H
m = trimesh.load(args.glb, force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vmax = np.abs(v).max()
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5
mc = trimesh.Trimesh(vertices=v, faces=f, process=False)
area = np.asarray(mc.area_faces, dtype=np.float64)
nz = np.asarray(mc.face_normals, dtype=np.float64)[:, 2]
up = nz > args.up_min
up_area = float(area[up].sum())
print("[elev] %s faces | up-facing (nz > %.2f): %s faces, area %.6f of %.6f total (%.2f%%)"
      % (f"{len(f):,}", args.up_min, f"{int(up.sum()):,}", up_area, area.sum(),
         100 * up_area / area.sum()), flush=True)

rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)), o3d.core.Tensor(f.astype(np.uint32)))
blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2
def _extents(w, h):
    if args.fit_axis == "height":
        ve = (bhi[2] - blo[2]) * args.margin
        return ve * (w / h), ve
    he = max(bhi[0] - blo[0], bhi[1] - blo[1]) * args.margin
    return he, he * (h / w)


# ---- E14 Ruling 10a: the ray grid is derived from the MESH, not from a frame --
# This tool used to take its ray grid straight from --aspect, i.e. from a
# GENERATION frame, which knows the subject's silhouette and nothing about its
# tessellation. On the sword's 240-px profile frame the grid ran 3.71x coarser
# than the mean face and the up-facing answer came back 13.851% against a
# converged 53.920% - wrong by 3.9x, because faces smaller than a ray cell are
# hit only by luck and this subject's up-facing faces are exactly the small
# horizontal steps (coil grooves, nick scoring, stepped quillon ends).
#
# The cell is square in both fit-axis modes (h_ext/W == v_ext/H), so one number
# governs density. The grid is now sized so a mean-area face receives
# --rays-per-face rays, and the ratio is PRINTED whether it was derived or
# inherited - the 7b law sharpened route-wide: a first-hit figure's ray density
# is quoted as the ray-cell-to-mean-face ratio.
#
# --aspect keeps its meaning as the frame's SHAPE; what it stops deciding is the
# RESOLUTION. The extent along the fit axis does not depend on the pixel counts
# at all (height-fit pins v_ext to the bbox, width-fit pins h_ext), so the cell
# side is that fixed extent over one pixel count and the grid can be solved for
# directly. --exact-grid restores the old literal reading, which is how the
# recorded ladder is reproduced.
MEAN_FACE = float(area.mean())
_FIXED = ((bhi[2] - blo[2]) if args.fit_axis == "height"
          else max(bhi[0] - blo[0], bhi[1] - blo[1])) * args.margin
if not args.exact_grid:
    _side_target = (MEAN_FACE / args.rays_per_face) ** 0.5
    if args.fit_axis == "height":
        H = int(np.ceil(_FIXED / _side_target))
        W = max(1, int(round(H * ASPECT_W0 / ASPECT_H0)))
    else:
        W = int(np.ceil(_FIXED / _side_target))
        H = max(1, int(round(W * ASPECT_H0 / ASPECT_W0)))

h_ext, v_ext = _extents(W, H)
# a top-down camera looks along a different axis; give it a frame that contains the subject
top_ext = max(bhi[0] - blo[0], bhi[1] - blo[1]) * args.margin

CELL = (h_ext / W) * (v_ext / H)
RATIO = CELL / MEAN_FACE                    # ray cell / mean face
RAYS_PER_FACE = MEAN_FACE / CELL
print("[elev] RAY DENSITY  frame %dx%d (%s)  cell %.4e  mean face %.4e  "
      "ratio %.3fx  rays/mean-face %.2f  (%.1fM rays per camera)"
      % (W, H, ("--exact-grid, literal --aspect" if args.exact_grid else
                "derived at --rays-per-face %g, shape from --aspect %d:%d"
                % (args.rays_per_face, ASPECT_W0, ASPECT_H0)),
         CELL, MEAN_FACE, RATIO, RAYS_PER_FACE, W * H / 1e6), flush=True)
if RAYS_PER_FACE < 1.0:
    print("[elev] WARNING: the ray grid is COARSER than the mean face (ratio %.3fx, "
          "%.2f rays per mean face). A figure at ratio >= 1 is NOT converged - faces "
          "smaller than a ray cell are hit only by luck, and on the sword this frame "
          "reported 13.851%% against a converged 53.920%%. Every number below is a "
          "lower bound of unknown tightness. [E14 Ruling 10a]"
          % (RATIO, RAYS_PER_FACE), flush=True)
else:
    # Measured in E16-7 on this very subject: meeting the floor is NOT a
    # convergence certificate. Eye-level reach keeps climbing well past it -
    # 53.967% at 10 rays/face, 54.600% at 20, 54.849% at 40 - so the density
    # floor buys "not wrong by 3.9x", not "converged". Say so, because the
    # record's own 53.920% was labelled converged on a ladder that had just
    # moved +2.394 points.
    print("[elev] NOTE: >=1 ray per mean face is a FLOOR, not convergence. On the "
          "sword, reach still rose 53.967 -> 54.600 -> 54.849% from 10 -> 20 -> 40 "
          "rays/face. Quote the density with the number, and ladder it if the "
          "quantity matters. [E14 Ruling 10a]", flush=True)

xs_ = (np.arange(W) + 0.5) / W
ys_ = (np.arange(H) + 0.5) / H


def basis(yaw_d, el_d):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    ref = np.array([0.0, 0.0, 1.0])
    if abs(float(look @ ref)) > 0.999:          # at the pole the z reference is degenerate
        ref = np.array([0.0, 1.0, 0.0])
    right = np.cross(look, ref)
    n = np.linalg.norm(right)
    if not (n > 1e-6):
        raise AssertionError("ANDON: degenerate camera basis at yaw %g el %g" % (yaw_d, el_d))
    right /= n
    upv = np.cross(right, look)
    return look, right, upv / (np.linalg.norm(upv) + 1e-12)


def reached(yaw, el):
    """Set of face ids that are a FIRST HIT from this camera."""
    look, right, upv = basis(yaw, el)
    he, ve = (top_ext, top_ext * (H / W)) if abs(el) > 80 else (h_ext, v_ext)
    gx = (xs_ * he - he / 2)[None, :]
    gy = (ve / 2 - ys_ * ve)[:, None]
    o = (bmid[None, None, :]
         + gx[..., None] * right[None, None, :]
         + gy[..., None] * upv[None, None, :]
         - look[None, None, :] * D)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [o, np.broadcast_to(look, o.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    pid = ans["primitive_ids"].numpy().reshape(-1)
    return np.unique(pid[pid != o3d.t.geometry.RaycastingScene.INVALID_ID])


BASE = [(float(y), 0.0) for y in args.base.split(",")]
CANDS = {
    "0/180 @ 40": [(0.0, 40.0), (180.0, 40.0)],
    "0/180 @ 55": [(0.0, 55.0), (180.0, 55.0)],
    "90/270 @ 40": [(90.0, 40.0), (270.0, 40.0)],
    "90/270 @ 55": [(90.0, 55.0), (270.0, 55.0)],
    "top-down (0 @ 90)": [(0.0, 90.0)],
}

seen = np.zeros(len(f), dtype=bool)
for yaw, el in BASE:
    seen[reached(yaw, el)] = True
base_up = float(area[seen & up].sum())
print("[elev] EYE-LEVEL EIGHT alone reach %.3f%% of up-facing area  (unreached %.3f%%)"
      % (100 * base_up / up_area, 100 * (1 - base_up / up_area)), flush=True)

rec = {"glb": os.path.abspath(args.glb), "up_min": args.up_min,
       "up_faces": int(up.sum()), "up_area": up_area, "total_area": float(area.sum()),
       "base_yaws": args.base, "base_up_reached_pct": 100 * base_up / up_area,
       "rounds": []}

cur = seen.copy()
remaining = dict(CANDS)
for rnd in (1, 2):
    print("\n[elev] round %d - marginal gain on top of what is already reached:" % rnd,
          flush=True)
    scores = {}
    for name, cams in remaining.items():
        t = cur.copy()
        for yaw, el in cams:
            t[reached(yaw, el)] = True
        gain = float(area[t & up].sum()) - float(area[cur & up].sum())
        scores[name] = (gain, float(area[t & up].sum()))
        print("[elev]   %-20s +%.4f area  -> %.3f%% of up-facing  (marginal +%.3f pts)"
              % (name, gain, 100 * scores[name][1] / up_area, 100 * gain / up_area),
              flush=True)
    best = max(scores, key=lambda k: scores[k][0])
    rec["rounds"].append({"round": rnd,
                          "scores": {k: {"marginal_area": s[0],
                                         "cum_pct": 100 * s[1] / up_area,
                                         "marginal_pts": 100 * s[0] / up_area}
                                     for k, s in scores.items()},
                          "winner": best})
    print("[elev]   WINNER round %d: %s  (cumulative %.3f%% of up-facing, unreached %.3f%%)"
          % (rnd, best, 100 * scores[best][1] / up_area,
             100 * (1 - scores[best][1] / up_area)), flush=True)
    for yaw, el in CANDS[best]:
        cur[reached(yaw, el)] = True
    remaining.pop(best)

DEFAULT_SUPERSET = set([(float(y), 0.0) for y in range(0, 360, 15)] + [(0.0, 55.0), (180.0, 55.0)])
w1 = rec["rounds"][0]["winner"]
outside = [c for c in CANDS[w1] if c not in DEFAULT_SUPERSET]
rec["round1_winner_outside_cull_default"] = [list(c) for c in outside]
print("\n[elev] E06 superset check on round 1's winner (%s): %s"
      % (w1, ("INSIDE cull_unseen's 26-camera default - no union re-issue needed"
              if not outside else
              "OUTSIDE the default at %s - a union re-issue is a finding for the ruling"
              % outside)), flush=True)
if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    json.dump(rec, open(args.out, "w"), indent=1)
    print("[elev] wrote %s" % os.path.abspath(args.out), flush=True)
