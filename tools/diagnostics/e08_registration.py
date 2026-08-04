"""E08 — does a twin register against the mesh it is supposed to be a reference for?

E01 made this load-bearing: silhouette IoU 0.290 -> 0.777 was the fix that stopped the model
regenerating the character freely, and carrying a mis-registered twin collapsed styled
coverage 62% -> 22.7%. So "is this a better reference" has an answer in this repo already,
and it does not need taste.

Reports, per twin, against the EXACT raycast mesh silhouette:

  painted fraction   the twin's own keyed figure as a share of frame, against 19.01% truth
  IoU                keyed figure vs silhouette
  centroid offset    px, and bbox extents — registration signals that do NOT depend on how
                     much of the figure the keying managed to find
  IoU at 3 tolerances  so a ranking can be checked for keying sensitivity rather than assumed

⚠ CONFOUND, stated up front: keying a figure against BLUE is easier than against GREY, so a
blue-background twin can score better for reasons that have nothing to do with registration.
Only compare within a background. The clean isolation is grey-vs-grey, where keying difficulty
is identical and the control is the only difference.

  e08_registration.py --prep DIR --twins name=path,name=path ... --view 0|4
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
ap.add_argument("--sets", required=True,
                help="label=dir,label=dir — each dir holding w3clay_0.png / w3clay_4.png")
ap.add_argument("--shipped", help="dir of the shipped twins, listed first if given")
ap.add_argument("--aspect", default="752,1024")
ap.add_argument("--out-json")
args = ap.parse_args()
AW, AH = [int(x) for x in args.aspect.split(",")]

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
vv = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
v = np.stack([vv[:, 0], -vv[:, 2], vv[:, 1]], axis=1) / np.abs(vv).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))
blo, bhi = v.min(axis=0), v.max(axis=0)
bmid = (blo + bhi) / 2
v_ext = (bhi[2] - blo[2]) * 1.204
h_ext = v_ext * (AW / AH)


def silhouette(dtc, right):
    look = -dtc
    up = np.cross(right, look)
    up = up / np.linalg.norm(up)
    xs = (np.arange(AW) + 0.5) / AW * h_ext - h_ext / 2
    ys = v_ext / 2 - (np.arange(AH) + 0.5) / AH * v_ext
    gx, gy = np.meshgrid(xs, ys)
    org = (bmid[None, None, :] + gx[..., None] * right[None, None, :]
           + gy[..., None] * up[None, None, :] - look[None, None, :] * 2.0)
    return np.isfinite(rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(look, org.shape)], axis=-1
    ).reshape(AH, AW, 6).reshape(-1, 6).astype(np.float32)))["t_hit"].numpy()
        .reshape(AH, AW))


VIEWS = {0: (np.array([0.0, -1.0, 0.0]), np.array([1.0, 0.0, 0.0])),
         4: (np.array([0.0, 1.0, 0.0]), np.array([-1.0, 0.0, 0.0]))}
SIL = {i: silhouette(*VIEWS[i]) for i in VIEWS}


def keyed(img, tol):
    """Figure mask against a background that may not be flat.

    ⚠ The corner-median key used everywhere else in this pipeline FAILS on these twins
    and the failure is loud: it returned painted fractions of 31-76% against a 19.01%
    silhouette, with figure bounding boxes 751 px wide in a 752 px frame — it was keying
    the background. Diffusion paints a lit studio gradient, not the flat field it was
    given, so a single corner median is the wrong background model and every pixel far
    from a corner exceeds tolerance.

    Fitted instead: a quadratic surface per channel, least-squares over a border ring the
    figure cannot reach, then threshold the residual. Reduces to the corner median when
    the background really is flat, which is why the shipped twin's numbers are unchanged.
    """
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    ring = np.zeros((H, W), dtype=bool)
    b = 24
    ring[:b, :] = ring[-b:, :] = ring[:, :b] = ring[:, -b:] = True
    X = np.stack([np.ones(ring.sum()), xx[ring] / W, yy[ring] / H,
                  (xx[ring] / W) ** 2, (yy[ring] / H) ** 2,
                  (xx[ring] / W) * (yy[ring] / H)], axis=1)
    A = np.stack([np.ones(H * W), xx.ravel() / W, yy.ravel() / H,
                  (xx.ravel() / W) ** 2, (yy.ravel() / H) ** 2,
                  (xx.ravel() / W) * (yy.ravel() / H)], axis=1)
    resid = np.zeros((H, W, 3), dtype=np.float32)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(X, img[..., c][ring], rcond=None)
        resid[..., c] = img[..., c] - (A @ coef).reshape(H, W)
    return np.abs(resid).max(axis=-1) > tol


def stats(mask, sil):
    inter = int((mask & sil).sum())
    union = int((mask | sil).sum())
    yy, xx = np.mgrid[0:AH, 0:AW]
    out = {"pct_of_frame": round(float(mask.mean() * 100), 2),
           "iou": round(inter / max(union, 1), 4)}
    if mask.any():
        out["centroid_dx"] = round(float(xx[mask].mean() - xx[sil].mean()), 1)
        out["centroid_dy"] = round(float(yy[mask].mean() - yy[sil].mean()), 1)
        ys_, xs_ = np.where(mask)
        sy, sx = np.where(sil)
        out["bbox_h"] = int(ys_.max() - ys_.min())
        out["bbox_w"] = int(xs_.max() - xs_.min())
        out["sil_bbox_h"] = int(sy.max() - sy.min())
        out["sil_bbox_w"] = int(sx.max() - sx.min())
    return out


sets = []
if args.shipped:
    sets.append(("shipped", args.shipped))
for spec in args.sets.split(","):
    lab, d = spec.split("=", 1)
    sets.append((lab, d))

out = {"silhouette_pct_of_frame": round(float(SIL[0].mean() * 100), 2)}
print(f"[reg] exact mesh silhouette: {int(SIL[0].sum()):,}px = "
      f"{SIL[0].mean()*100:.2f}% of frame — the truth every twin is measured against\n")
for view in (0, 4):
    print(f"[reg] === view {view} ===")
    print(f"[reg]   {'twin':<12s} {'painted%':>9s} {'IoU':>7s}   "
          f"{'IoU@.04':>8s} {'IoU@.10':>8s}   {'dx':>6s} {'dy':>6s}   {'bbox h x w':>12s}")
    for lab, d in sets:
        p = os.path.join(d, f"w3clay_{view}.png")
        if not os.path.exists(p):
            continue
        img = np.asarray(Image.open(p).convert("RGB"), dtype=np.float32) / 255.0
        s6 = stats(keyed(img, 0.06), SIL[view])
        s4 = stats(keyed(img, 0.04), SIL[view])
        s10 = stats(keyed(img, 0.10), SIL[view])
        out.setdefault(f"view{view}", {})[lab] = {
            "tol_0.06": s6, "iou_tol_0.04": s4["iou"], "iou_tol_0.10": s10["iou"]}
        print(f"[reg]   {lab:<12s} {s6['pct_of_frame']:>8.2f}% {s6['iou']:>7.4f}   "
              f"{s4['iou']:>8.4f} {s10['iou']:>8.4f}   "
              f"{s6.get('centroid_dx',0):>6.1f} {s6.get('centroid_dy',0):>6.1f}   "
              f"{s6.get('bbox_h',0):>5d} x {s6.get('bbox_w',0):<4d}"
              f"  (mesh {s6.get('sil_bbox_h',0)} x {s6.get('sil_bbox_w',0)})")
    print()

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"[reg] wrote {args.out_json}")
