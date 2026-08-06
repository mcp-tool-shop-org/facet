"""E04 Step 0 anchor 1c, REPLACEMENT INSTRUMENT — geometry against geometry, bound 0 px.

The withdrawn anchor thresholded a clay render to find the figure and compared its bbox to
`silhouette_masks`' output. That measures the threshold's antialiasing fringe, on the exact
technique this repo retired: *"the mask CANNOT be thresholded off the clay render"* — E01
established a Workbench clay is flat grey on flat grey, and E08 measured a keyed mask holding
111,602 px of a 146,356 px silhouette. A bound built on it was measuring its own instrument.

This asks the question with no threshold anywhere. `turn_render` places an ORTHO camera with
stated parameters; those parameters define a ray grid exactly. Cast it, and compare the hit
mask to the silhouette `silhouette_masks` produced for the same view. Both sides are a
raycast against the same triangles, so the ONLY thing that can differ is the framing
convention the two tools computed — which is precisely what the anchor exists to test.

  turn_render:  ortho_scale on the fitted axis, sensor_fit VERTICAL|HORIZONTAL explicitly,
                camera at (mid.x + r sin th, mid.y - r cos th, mid.z), euler (90deg, 0, th)
  so:           right = (cos th, sin th, 0), up = (0, 0, 1), view dir = (-sin th, cos th, 0)

Pre-registered readings (advisor, Ruling 10), not chosen here:
  0 px                              -> anchor passes
  a few boundary px, uniform scatter-> float edge-ordering at the silhouette; report and halt
  a structural offset               -> the gate's real prey; the fit-axis change needs review

⚠ OPERAND REPAIR, 2026-08-06 (E12 Ruling 9a). THE BOUND DID NOT MOVE AND IS NOT NEGOTIABLE.
This file's replica used to run its raycast in a DIFFERENT FRAME from the source it checks:

  silhouette_masks.py   normalises  v -> [x,-z,y] / max|v| * 0.5,   casts from -look * 2.0,
                        and builds up as  cross(rgt, look) / (norm + 1e-12)
  this file, BEFORE     did not normalise,                          cast from -look * radius,
                        and hardcoded up = (0, 0, 1)

The normalisation is a uniform scale carried by the mesh AND the ray grid, so it cancels
mathematically and NOT in float32; `+ 1e-12` makes the source's up 0.999999999999 rather
than 1.0; and ray origins built at a different magnitude round differently. Measured on the
beast at 1792x1024 (`e12_agree_probe.py`, E12): the old construction disagreed with the
source at ONE grazing rim pixel on view 5 (636,498; centroid shift -0.0007 px; bboxes
identical), and the SAME code run in the source's frame returned 0 px on both views.

**An anchor is computed with the source's own arithmetic** — the standing rule, which
predates this result (the E10 off-surface anchors were built exactly so). So the incidental
numerics below are conformed to `silhouette_masks`: the normalisation, the up-vector
construction, and the ray-back constant. This is an operand repair, not a retune: the rule
would have been the same whatever the measurement returned.

WHAT INDEPENDENCE REMAINS, STATED PLAINLY, because a future session must not over-trust this.
After the repair the two framing derivations are bit-identical arithmetic (they always were
the same FORMULA, written on differently-named variables), so this tool can no longer catch
a shared bug in that formula. It still catches, and these are the failures it was built for:

  * the two tools being GIVEN DIFFERENT FLAGS — aspect, fit-axis, margin or step. That is
    the galleon's historical 4.68% failure in its current form: the derivations moved
    together only once --fit-axis existed on both, and nothing but this check asserts that
    a caller passed the same value to each.
  * a STALE or FOREIGN mask file — wrong tag, wrong mesh, wrong frame size, left over from
    an earlier run. The replica re-derives from the GLB; the mask is read off disk.
  * turn_render's height/width -> sensor_fit VERTICAL/HORIZONTAL branch, encoded here
    explicitly rather than inherited.

The legacy (unconformed) construction is still COMPUTED AND REPORTED every run, as a
diagnostic — so the repair stays auditable and so the float-ordering class remains visible
rather than being silently absorbed. IT DOES NOT GATE. Gating on it would be gating on a
proxy for the question, which is the class of error this repo has paid for repeatedly.

  e04_frame_agree.py --glb g.glb --masks DIR --tag t --views 1,7 --aspect 1066,1024
                     --fit-axis width [--margin 1.204]

Standards compliance: PIN_PER_STEP - every camera parameter is derived from the same
arguments turn_render takes. ANDON_AUTHORITY - the bound is 0 px and this tool exits
non-zero above it; it does not choose a tolerance, and the repair above left it untouched.
EXTERNAL_VERIFIER - it re-derives the framing from the GLB and compares against a mask read
off disk, so it cannot pass by agreeing with itself about what was written; the reduction in
independence from the operand repair is enumerated above rather than left implicit.
"""
import argparse
import os
import sys

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--masks", required=True)
ap.add_argument("--tag", default="galleonclay")
ap.add_argument("--views", default="1,7")
ap.add_argument("--step", type=float, default=45.0)
ap.add_argument("--aspect", required=True)
ap.add_argument("--fit-axis", default="height", choices=["height", "width"])
ap.add_argument("--margin", type=float, default=1.204)
args = ap.parse_args()

W, H = (int(x) for x in args.aspect.split(","))
m = trimesh.load(args.glb, force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
# Blender's glTF import remap, the same one silhouette_masks and project_twins apply.
# ⚠ THE SCALE IS THE SOURCE'S (Ruling 9a): silhouette_masks computes vmax on the PRE-remap
# vertices and then divides, so the order of these two lines is part of the arithmetic.
vmax = np.abs(v).max()
vb = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5
vb_legacy = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1)      # the pre-repair frame


def frame_of(vv):
    """turn_render's ortho_scale, verbatim, in whatever frame `vv` is expressed in."""
    lo_, hi_ = vv.min(0), vv.max(0)
    sz = hi_ - lo_
    if args.fit_axis == "height":
        o = sz[2] * args.margin
        return o, o * (W / H), o, (lo_ + hi_) / 2, sz          # ortho, h_ext, v_ext (VERTICAL)
    o = max(sz[0], sz[1]) * args.margin
    return o, o, o * (H / W), (lo_ + hi_) / 2, sz              # ortho, h_ext, v_ext (HORIZONTAL)


ortho, h_ext, v_ext, mid, size = frame_of(vb)
o_l, h_l, v_l, mid_l, size_l = frame_of(vb_legacy)
print("[agree] fit-axis %s  ortho_scale %.6f  ->  h_ext %.6f  v_ext %.6f  frame %dx%d"
      % (args.fit_axis, ortho, h_ext, v_ext, W, H), flush=True)
print("[agree]   source-frame scale 0.5/%.9f = %.12f applied (Ruling 9a operand repair); "
      "legacy unconformed h_ext %.6f reported below, NOT gated"
      % (vmax, 0.5 / vmax, h_l), flush=True)

rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vb.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
rs_legacy = o3d.t.geometry.RaycastingScene()
rs_legacy.add_triangles(o3d.core.Tensor(vb_legacy.astype(np.float32)),
                        o3d.core.Tensor(f.astype(np.uint32)))
radius_legacy = max(size_l[0], size_l[1]) * 3.0
worst = 0
worst_legacy = 0
rows = []
for k in [int(x) for x in args.views.split(",")]:
    th = np.radians(k * args.step)
    right = np.array([np.cos(th), np.sin(th), 0.0])
    look = np.array([-np.sin(th), np.cos(th), 0.0])       # camera at +r*(sin,-cos), looks back
    # ⚠ THE SOURCE'S OWN up (Ruling 9a). silhouette_masks builds it as cross(rgt, look)
    # normalised by (norm + 1e-12), which lands 0.999999999999 rather than 1.0. Reproduced
    # rather than simplified: an anchor is computed with the source's arithmetic, and a
    # "harmless" simplification here is exactly what cost a halt.
    up = np.cross(right, look)
    up = up / (np.linalg.norm(up) + 1e-12)
    xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    gx, gy = np.meshgrid(xs, ys)
    org = (mid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * 2.0)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    hit = np.isfinite(ans["t_hit"].numpy().reshape(H, W))

    # the pre-repair construction, computed for the record and NOT gated
    xs_l = (np.arange(W) + 0.5) / W * h_l - h_l / 2
    ys_l = v_l / 2 - (np.arange(H) + 0.5) / H * v_l
    gx_l, gy_l = np.meshgrid(xs_l, ys_l)
    org_l = (mid_l[None, None, :] + gx_l[..., None] * right[None, None, :]
             + gy_l[..., None] * np.array([0.0, 0.0, 1.0])[None, None, :]
             - look[None, None, :] * radius_legacy)
    ans_l = rs_legacy.cast_rays(o3d.core.Tensor(np.concatenate(
        [org_l, np.broadcast_to(look, org_l.shape)], axis=-1
    ).reshape(-1, 6).astype(np.float32)))
    hit_legacy = np.isfinite(ans_l["t_hit"].numpy().reshape(H, W))

    p = os.path.join(args.masks, "%s_%d.png" % (args.tag, k))
    sil = np.asarray(Image.open(p).convert("L")) > 127
    if sil.shape != hit.shape:
        print("[agree] view %d: SHAPE MISMATCH mask %s vs frame %s"
              % (k, sil.shape, hit.shape), flush=True)
        worst = 10 ** 9
        continue
    diff = hit ^ sil
    n = int(diff.sum())
    worst = max(worst, n)
    n_legacy = int((hit_legacy ^ sil).sum())
    worst_legacy = max(worst_legacy, n_legacy)
    row = {"view": k, "differing_px": n, "hit_px": int(hit.sum()), "sil_px": int(sil.sum()),
           "legacy_differing_px": n_legacy, "legacy_hit_px": int(hit_legacy.sum())}
    if n:
        ys_, xs_ = np.nonzero(diff)
        # is it scatter at the boundary, or a structural offset? A structural offset moves
        # the centroid; float edge-ordering does not.
        cy_h, cx_h = np.nonzero(hit)
        cy_s, cx_s = np.nonzero(sil)
        row["centroid_shift_px"] = [round(float(cx_h.mean() - cx_s.mean()), 4),
                                    round(float(cy_h.mean() - cy_s.mean()), 4)]
        row["diff_bbox"] = [int(xs_.min()), int(xs_.max()), int(ys_.min()), int(ys_.max())]
        row["hit_bbox_wh"] = [int(cx_h.max() - cx_h.min()), int(cy_h.max() - cy_h.min())]
        row["sil_bbox_wh"] = [int(cx_s.max() - cx_s.min()), int(cy_s.max() - cy_s.min())]
    rows.append(row)
    print("[agree] view %d: differing %d px   (hit %d, mask %d)%s"
          % (k, n, row["hit_px"], row["sil_px"],
             ("  centroid shift %s  hit bbox %s vs mask %s"
              % (row["centroid_shift_px"], row["hit_bbox_wh"], row["sil_bbox_wh"])) if n else ""),
          flush=True)
    print("[agree]   legacy construction (unconformed, NOT gated): %d differing px  (hit %d)"
          % (n_legacy, row["legacy_hit_px"]), flush=True)

print("\n[agree] ANCHOR 1c (geometry vs geometry, bound 0 px): worst %d px -> %s"
      % (worst, "PASS" if worst == 0 else "*** HALT ***"), flush=True)
print("[agree] legacy construction for the record, ungated: worst %d px%s"
      % (worst_legacy,
         "  <- the operand repair is what moved this run" if worst_legacy > worst else ""),
      flush=True)
sys.exit(0 if worst == 0 else 2)
