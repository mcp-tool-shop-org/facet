"""How much of each twin's keyed paint sits on no surface at all?

Comparability instrument, not an arm. The halt report quotes 3,772 px for view 2 and 8,991
for view 6 from an ad-hoc check; `project_twins --trust-intersect` now reports the same
quantity from its own fitted key and its own raycast silhouette. If the two disagree, the
views-0/4 numbers cannot be read against the views-2/6 numbers, so the definition is pinned
here and run over every twin with one code path.

No projection, no atlas, no decision — the key and the raycast, nothing else.

  keyed_outside.py --prep DIR --twins DIR --views 0,1,2,3,4,5,6,7 [--out-json j]
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import label, minimum_filter

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--twins", required=True)
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--pattern", default="twin_{k}.png")
ap.add_argument("--step", type=float, default=45.0)
ap.add_argument("--aspect", default="752,1024")
ap.add_argument("--tol", type=float, default=0.06)
ap.add_argument("--erode", type=int, default=5)
ap.add_argument("--out-json")
args = ap.parse_args()
AW, AH = [float(x) for x in args.aspect.split(",")]

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
    th = np.radians(deg)

    def snap(a):
        return np.array([0.0 if abs(x) < 1e-12
                         else (float(round(x)) if abs(abs(x) - 1.0) < 1e-12 else float(x))
                         for x in a])
    return snap([np.sin(th), -np.cos(th), 0.0]), snap([np.cos(th), np.sin(th), 0.0])


def figure_mask(img, tol, erode):
    """project_twins' FITTED estimator, verbatim. Corner-median is retired."""
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    ring = np.zeros((H, W), dtype=bool)
    b = 24
    ring[:b, :] = ring[-b:, :] = ring[:, :b] = ring[:, -b:] = True
    cols = [np.ones(H * W), xx.ravel() / W, yy.ravel() / H,
            (xx.ravel() / W) ** 2, (yy.ravel() / H) ** 2,
            (xx.ravel() / W) * (yy.ravel() / H)]
    A = np.stack(cols, axis=1)
    Xr = A.reshape(H, W, -1)[ring]
    resid = np.zeros((H, W, 3), dtype=np.float32)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(Xr, img[..., c][ring], rcond=None)
        resid[..., c] = img[..., c] - (A @ coef).reshape(H, W)
    return minimum_filter((np.abs(resid).max(axis=-1) > tol).astype(np.float32),
                          size=erode) > 0.5


rows = {}
print(f"{'view':>5} {'yaw':>6} {'keyed':>9} {'sil':>9} {'OUTSIDE':>9} {'largest':>9} "
      f"{'%keyed':>7} {'IoU':>7} {'dx':>6} {'dy':>6} {'bbox twin':>11} {'bbox mesh':>11}")
for k in [int(x) for x in args.views.split(",")]:
    p = os.path.join(args.twins, args.pattern.format(k=k))
    assert os.path.exists(p), f"ANDON: no twin at {p}"
    img = np.asarray(Image.open(p).convert("RGB"), dtype=np.float32) / 255.0
    H, W = img.shape[:2]
    twin = figure_mask(img, args.tol, args.erode)
    deg = k * args.step
    dtc, rgt = cam_axes(deg)
    look = -dtc
    upv = np.cross(rgt, look)
    upv /= np.linalg.norm(upv) + 1e-12
    gx_ = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
    gy_ = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
    g1, g2 = np.meshgrid(gx_, gy_)
    o2 = (bmid[None, None, :] + g1[..., None] * rgt[None, None, :]
          + g2[..., None] * upv[None, None, :] - look[None, None, :] * 2.0)
    mesh = np.isfinite(rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [o2, np.broadcast_to(look, o2.shape)], axis=-1
    ).reshape(-1, 6).astype(np.float32)))["t_hit"].numpy().reshape(H, W))

    outside = twin & ~mesh
    lab_o, n_lab = label(outside)
    cc = int(np.bincount(lab_o.ravel())[1:].max()) if n_lab else 0
    ys_t, xs_t = np.where(twin)
    ys_m, xs_m = np.where(mesh)
    bt = (int(ys_t.max() - ys_t.min()), int(xs_t.max() - xs_t.min()))
    bm = (int(ys_m.max() - ys_m.min()), int(xs_m.max() - xs_m.min()))
    iou = float((twin & mesh).sum() / max((twin | mesh).sum(), 1))
    dx = float(xs_t.mean() - xs_m.mean())
    dy = float(ys_t.mean() - ys_m.mean())
    n_out = int(outside.sum())
    rows[str(k)] = {"yaw": deg, "keyed_px": int(twin.sum()), "silhouette_px": int(mesh.sum()),
                    "outside_px": n_out, "largest_cc_px": cc, "n_components": int(n_lab),
                    "pct_of_keyed": round(n_out / max(int(twin.sum()), 1) * 100, 2),
                    "iou_twin_mesh": round(iou, 4),
                    "centroid_offset_px": [round(dx, 1), round(dy, 1)],
                    "bbox_twin": list(bt), "bbox_mesh": list(bm),
                    "bbox_ratio_h": round(bt[0] / bm[0], 3),
                    "bbox_ratio_w": round(bt[1] / bm[1], 3)}
    print(f"{k:>5} {deg:>6.0f} {int(twin.sum()):>9,} {int(mesh.sum()):>9,} {n_out:>9,} "
          f"{cc:>9,} {n_out / max(int(twin.sum()), 1) * 100:>6.2f}% {iou:>7.4f} "
          f"{dx:>+6.1f} {dy:>+6.1f} {bt[0]:>5}x{bt[1]:<5} {bm[0]:>5}x{bm[1]:<5}")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(rows, open(args.out_json, "w"), indent=1)
    print(f"\n[outside] wrote {args.out_json}")
