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

  e04_frame_agree.py --glb g.glb --masks DIR --tag t --views 1,7 --aspect 1066,1024
                     --fit-axis width [--margin 1.204]

Standards compliance: PIN_PER_STEP - every camera parameter is derived from the same
arguments turn_render takes. ANDON_AUTHORITY - the bound is 0 px and this tool exits
non-zero above it; it does not choose a tolerance. EXTERNAL_VERIFIER - it compares two
independent implementations of one convention and cannot pass by agreeing with itself.
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
# Blender's glTF import remap, the same one silhouette_masks and project_twins apply
vb = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1)
lo, hi = vb.min(0), vb.max(0)
size = hi - lo
mid = (lo + hi) / 2

# turn_render's ortho_scale, verbatim
if args.fit_axis == "height":
    ortho = size[2] * args.margin
    v_ext, h_ext = ortho, ortho * (W / H)          # sensor_fit VERTICAL
else:
    ortho = max(size[0], size[1]) * args.margin
    h_ext, v_ext = ortho, ortho * (H / W)          # sensor_fit HORIZONTAL
print("[agree] fit-axis %s  ortho_scale %.6f  ->  h_ext %.6f  v_ext %.6f  frame %dx%d"
      % (args.fit_axis, ortho, h_ext, v_ext, W, H), flush=True)

rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vb.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
radius = max(size[0], size[1]) * 3.0
worst = 0
rows = []
for k in [int(x) for x in args.views.split(",")]:
    th = np.radians(k * args.step)
    right = np.array([np.cos(th), np.sin(th), 0.0])
    up = np.array([0.0, 0.0, 1.0])
    look = np.array([-np.sin(th), np.cos(th), 0.0])       # camera at +r*(sin,-cos), looks back
    xs = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    ys = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    gx, gy = np.meshgrid(xs, ys)
    org = (mid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * radius)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1).reshape(-1, 6).astype(np.float32)))
    hit = np.isfinite(ans["t_hit"].numpy().reshape(H, W))

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
    row = {"view": k, "differing_px": n, "hit_px": int(hit.sum()), "sil_px": int(sil.sum())}
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

print("\n[agree] ANCHOR 1c (geometry vs geometry, bound 0 px): worst %d px -> %s"
      % (worst, "PASS" if worst == 0 else "*** HALT ***"), flush=True)
sys.exit(0 if worst == 0 else 2)
