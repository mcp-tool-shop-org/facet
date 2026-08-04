"""Is project_twins' LIVE raycast silhouette the same object as the shipped sidecar mask?

E08 Amendment 26 puts one operand — twin_fm AND mesh_fm — into two places: the pipeline
(project_twins, which raycasts the silhouette live) and the instrument (e08_acceptance,
which reads a sidecar `*_mask.png` written earlier by silhouette_masks.py). If those two
objects differ, the two intersections are different intersections and the regression
measures nothing.

So: recompute the silhouette exactly as project_twins does — same scene construction, same
camera convention, same snap — and count differing pixels against the sidecar. Expect 0.
A nonzero answer is reported, not reconciled: which object is authoritative is a ruling.

  silhouette_agree.py --prep DIR --mask MASKDIR --views 0,4 [--step 45]
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
ap.add_argument("--prep", required=True)
ap.add_argument("--mask", required=True, help="directory of w3clay_<idx>.png sidecars")
ap.add_argument("--views", default="0,4")
ap.add_argument("--step", type=float, default=45.0)
ap.add_argument("--aspect", default="752,1024")
ap.add_argument("--stem", default="w3clay")
# ⚠ EARNED IN THE FIRST RUN OF THIS SCRIPT. The two mask conventions in this project are
# NOT interchangeable: ARMB/masks/ holds `w3clay_<k>.png` (a mask), while a twins/ dir holds
# `w3clay_<k>.png` (the TWIN) beside `w3clay_<k>_mask.png` (its sidecar). Pointing --mask at
# a twins dir without --suffix silently thresholds a painted RGB twin and reports it as a
# silhouette; it gave 10,800px against a 76,549px mask before the binary check below caught
# it. Same shape as the errors this repo already catalogues — arithmetic that replays fine
# over the wrong operand.
ap.add_argument("--suffix", default="",
                help="appended to the stem, e.g. _mask for a twins/ sidecar")
ap.add_argument("--out-json")
args = ap.parse_args()
AW, AH = [float(x) for x in args.aspect.split(",")]

meta = json.load(open(os.path.join(args.prep, "meta.json")))
m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2
v_ext = (bhi[2] - blo[2]) * 1.204
h_ext = v_ext * (AW / AH)


def cam_axes(deg):
    """Copied verbatim from project_twins. The snap is load-bearing — sin(pi) is
    1.2246e-16, not 0, and an unsnapped back camera perturbs every ray."""
    th = np.radians(deg)

    def snap(a):
        out = []
        for x in a:
            if abs(x) < 1e-12:
                out.append(0.0)
            elif abs(abs(x) - 1.0) < 1e-12:
                out.append(float(round(x)))
            else:
                out.append(float(x))
        return np.array(out)
    return snap([np.sin(th), -np.cos(th), 0.0]), snap([np.cos(th), np.sin(th), 0.0])


rows = {}
worst = 0
for k in [int(x) for x in args.views.split(",")]:
    deg = k * args.step
    dtc, rgt = cam_axes(deg)
    look = -dtc
    upv = np.cross(rgt, look)
    upv /= np.linalg.norm(upv) + 1e-12
    W, H = int(AW), int(AH)
    gx_ = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    gy_ = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    g1, g2 = np.meshgrid(gx_, gy_)
    o2 = (bmid[None, None, :] + g1[..., None] * rgt[None, None, :]
          + g2[..., None] * upv[None, None, :] - look[None, None, :] * 2.0)
    live = np.isfinite(rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [o2, np.broadcast_to(look, o2.shape)], axis=-1
    ).reshape(-1, 6).astype(np.float32)))["t_hit"].numpy().reshape(H, W))

    mp = os.path.join(args.mask, f"{args.stem}_{k}{args.suffix}.png")
    assert os.path.exists(mp), f"ANDON: no sidecar at {mp}"
    grey = np.asarray(Image.open(mp).convert("L"))
    # a mask is binary; a twin is not. Cheap, and it tests the failure mode.
    nlev = len(np.unique(grey))
    assert nlev <= 4, (
        f"ANDON: {mp} has {nlev} distinct grey levels — that is an IMAGE, not a mask. "
        f"Point --mask at a mask directory, or add --suffix _mask for a twins/ sidecar.")
    side = grey.astype(np.float32) / 255.0 > 0.5
    assert side.shape == live.shape, (
        f"ANDON: sidecar {side.shape} vs live {live.shape} - different framing")
    diff = int((live != side).sum())
    worst = max(worst, diff)
    rows[str(k)] = {"yaw": deg, "live_px": int(live.sum()), "sidecar_px": int(side.sum()),
                    "differing_px": diff,
                    "live_not_sidecar": int((live & ~side).sum()),
                    "sidecar_not_live": int((side & ~live).sum()),
                    "iou": round(float((live & side).sum() / max((live | side).sum(), 1)), 6)}
    print(f"[agree] view {k} (yaw {deg:+.0f}): live {int(live.sum()):,}px   sidecar "
          f"{int(side.sum()):,}px   DIFFERING {diff:,}px   IoU {rows[str(k)]['iou']:.6f}")
    if diff:
        print(f"[agree]   live-not-sidecar {int((live & ~side).sum()):,}px   "
              f"sidecar-not-live {int((side & ~live).sum()):,}px")

print(f"\n[agree] worst differing pixel count across the tested views: {worst:,}")
if worst:
    print("[agree] !! NONZERO. Reported, not reconciled - which silhouette object is "
          "authoritative is a ruling, not an executor's call.")
else:
    print("[agree] the live raycast and the sidecar are the same object, pixel for pixel.")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump({"views": rows, "worst_differing_px": worst},
              open(args.out_json, "w"), indent=1)
    print(f"[agree] wrote {args.out_json}")
