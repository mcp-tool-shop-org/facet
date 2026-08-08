"""Exact mesh-silhouette masks per view, from GEOMETRY — the input restylize_views needs.

WHY THIS EXISTS. `restylize_views.py --masks` needs one exact silhouette per view to build
the control image, and only two existed (`BG2/masks/w3clay_{0,4}.png`). Arm B needs eight.

The mask CANNOT be thresholded off the clay render. E01 established that a Workbench clay is
flat grey on flat grey, and E08 Arm A measured the cost on W3: the keyed mask held 111,602 px
of a 146,356 px silhouette, IoU 0.76, and the loss was INTERIOR — a stripe down the whole
blade — not a rim. Measured again while building this tool: thresholding the clay gives
17.60% of frame against the geometry's 19.01%. `figure_mask` is retired from every path that
governs anything, and this tool is why the eight-view path never needs it.

THE ANSWER IS A RAYCAST, and it is the same one `project_twins.py` already runs — this file
is that code extracted, not a reimplementation, so the two cannot drift apart silently. The
`--anchor` flag exists to prove it: view 0 and view 4 must come back identical to the masks
already on disk, or the convention is wrong and nothing downstream is trustworthy.

CAMERA CONVENTION, verified against `turn_render.py` rather than assumed. turn_render sets

    cam.location = (mid.x + r*sin(th), mid.y - r*cos(th), mid.z)
    cam.rotation_euler = (90deg, 0, th)

so for yaw th the direction TO the camera is (sin th, -cos th, 0) and the camera's right is
(cos th, sin th, 0). At th=0 that is dtc (0,-1,0) / right (1,0,0) and at th=180 it is
(0,1,0) / (-1,0,0) — exactly `project_twins`' hardcoded front/back pair, which is the
reduction that makes this generalisation safe. Blender's glTF import remap (x, -z, y) is the
same remap project_twins applies, so both work in one frame.

Standards compliance:
  PIN_PER_STEP — every camera is derived from --views/--step and echoed per view; no
    literal camera vector in the body.
  ANDON_AUTHORITY — --anchor asserts a byte-identical match against a known-good mask and
    raises on mismatch; an empty or full-frame mask raises regardless.
  NAMED_COMPENSATORS — writes only new PNGs under --out. Undo = delete them. No input is
    modified. Owner: the session running it.
  EXTERNAL_VERIFIER — grades nothing. It emits masks and coverage numbers for a human.

  silhouette_masks.py --prep DIR --out DIR [--tag w3clay] [--views 0,1,2,3,4,5,6,7]
                      [--step 45] [--aspect 752,1024]
                      [--anchor 0=path/w3clay_0.png --anchor 4=path/w3clay_4.png]
"""
import argparse
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import subject_profile
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--tag", default="w3clay")
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--step", type=float, default=45.0,
                help="degrees of yaw per view index; must match turn_render's --step")
ap.add_argument("--aspect", default="752,1024")
ap.add_argument("--fit-axis", default="height", choices=["height", "width"],
                help="MUST match turn_render.py's --fit-axis for the same subject. See the "
                     "block at the framing site: they move together or the mask and the "
                     "render disagree.")
ap.add_argument("--margin", type=float, default=1.204,
                help="framing margin on the fitted axis; must match turn_render's.")
ap.add_argument("--anchor", action="append", default=[],
                help="VIEW=PATH — assert the generated mask matches an existing one exactly. "
                     "Repeatable. This is the only thing standing between a wrong camera "
                     "convention and eight silently misregistered twins.")
args = ap.parse_args(subject_profile.bind(ap, "silhouette_masks.py", None))

AW, AH = (int(x) for x in args.aspect.split(","))
os.makedirs(args.out, exist_ok=True)

# --- geometry setup, identical to project_twins.py ---------------------------------
m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vmax = np.abs(v).max()
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))

blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2
# ⚠ FIT AXIS (E04 Step 0, Ruling 6). THE IDENTICAL BLOCK LIVES IN turn_render.py AND THE
# TWO MUST MOVE TOGETHER. This file derived h_ext from v_ext unconditionally while
# turn_render let Blender map ortho_scale to the larger axis; on a portrait frame those
# agree, on a landscape frame they differ by exactly (AW/AH) and the mask comes out
# 4.68% smaller than the render it is supposed to describe. Measured on the galleon at
# 1072x1024: silhouette bbox 717x850 against the clay's 751x892.
if args.fit_axis == "height":
    v_ext = (bhi[2] - blo[2]) * args.margin
    h_ext = v_ext * (AW / AH)
else:
    h_ext = max(bhi[0] - blo[0], bhi[1] - blo[1]) * args.margin
    v_ext = h_ext * (AH / AW)
print(f"[sil] mesh {len(v):,} verts  {len(f):,} tris   v_ext {v_ext:.6f}  h_ext {h_ext:.6f}",
      flush=True)

anchors = {}
for a in args.anchor:
    k, _, p = a.partition("=")
    if not (p):
        raise AssertionError(f"ANDON: --anchor wants VIEW=PATH, got {a!r}")
    anchors[int(k)] = p

H, W = AH, AW
gx_ = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
gy_ = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
g1, g2 = np.meshgrid(gx_, gy_)

report = {"prep": os.path.abspath(args.prep), "step": args.step,
          "aspect": [AW, AH], "views": {}}

for idx in [int(x) for x in args.views.split(",")]:
    th = np.radians(idx * args.step)
    dtc = np.array([np.sin(th), -np.cos(th), 0.0])
    rgt = np.array([np.cos(th), np.sin(th), 0.0])
    look = -dtc
    upv = np.cross(rgt, look)
    upv /= np.linalg.norm(upv) + 1e-12

    o2 = (bmid[None, None, :] + g1[..., None] * rgt[None, None, :]
          + g2[..., None] * upv[None, None, :] - look[None, None, :] * 2.0)
    hit = np.isfinite(rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [o2, np.broadcast_to(look, o2.shape)], axis=-1
    ).reshape(-1, 6).astype(np.float32)))["t_hit"].numpy().reshape(H, W))

    # ANDON: a silhouette that is empty or fills the frame is not a silhouette.
    pct = float(hit.mean() * 100)
    if not (0.5 < pct < 60.0):
        raise AssertionError(
            f"ANDON: view {idx} silhouette is {pct:.2f}% of frame — empty or runaway, "
            f"the camera convention or the mesh is wrong.")
    ys, xs = np.nonzero(hit)
    bw, bh = int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)

    path = os.path.join(args.out, f"{args.tag}_{idx}.png")
    Image.fromarray((hit * 255).astype(np.uint8), mode="L").save(path)
    print(f"[sil] view {idx}  yaw {idx * args.step:6.1f}deg  "
          f"{pct:6.3f}% of frame  bbox {bw}x{bh}  -> {os.path.basename(path)}", flush=True)
    report["views"][str(idx)] = {"yaw": idx * args.step, "pct_of_frame": round(pct, 4),
                                 "bbox": [bw, bh], "px": int(hit.sum())}

    if idx in anchors:
        ref = np.asarray(Image.open(anchors[idx]).convert("L")) > 127
        if not (ref.shape == hit.shape):
            raise AssertionError(
                f"ANDON: view {idx} anchor is {ref.shape}, generated is {hit.shape}")
        diff = int((ref != hit).sum())
        agree = 100.0 * (1 - diff / ref.size)
        inter = int((ref & hit).sum())
        union = int((ref | hit).sum())
        print(f"[sil]   ANCHOR view {idx}: {diff:,} differing px "
              f"({agree:.4f}% agree, IoU {inter / union:.6f}) vs "
              f"{os.path.basename(anchors[idx])}", flush=True)
        report["views"][str(idx)]["anchor_diff_px"] = diff
        report["views"][str(idx)]["anchor_iou"] = round(inter / union, 6)
        if not (diff == 0):
            raise AssertionError(
                f"ANDON: view {idx} does not reproduce its anchor — {diff:,} differing px, "
                f"IoU {inter / union:.6f}. The camera convention is wrong; every twin built "
                f"on these masks would be misregistered. Fix before generating anything.")

with open(os.path.join(args.out, "silhouettes.json"), "w") as fh:
    json.dump(report, fh, indent=1)
print(f"[sil] wrote {len(report['views'])} masks + silhouettes.json -> {args.out}")
