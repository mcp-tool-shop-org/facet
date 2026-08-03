"""E05 — which of commit's five tests actually rejects the texels?

E02 measured that eight cameras close only 27% of holes, and E05 tried to widen that
from two directions: acceptance width (U3, --facing-min 0.25 -> 0.10) and island size
(U1, keep the generator's xatlas atlas). Neither moved the ratio. This reports WHY, by
replaying texpass_iter.commit's filter chain on one already-painted job and counting
survivors at each stage. It writes nothing.

commit accepts a hole texel only if it passes ALL of:
  1. hole AND valid          — is there anything to paint here
  2. facing > --facing-min   — does the surface face this camera        <- U3 widened this
  3. visibility raycast      — can this camera actually see it
  4. inside the job mask     — did the brush have licence to paint there
  5. edge distance on the brush output — is the paint free of background mix

Whichever stage drops the most is the real constraint, and it is not necessarily the
one that looks tunable.

  commit_funnel.py --prep DIR --state DIR --job job_y+045_e+00 [--facing-min 0.25]
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import distance_transform_edt, minimum_filter

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--state", required=True)
ap.add_argument("--job", required=True)
ap.add_argument("--facing-min", type=float, default=0.25)
ap.add_argument("--edge-dist", type=float, default=4.0)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--stage1-holes", help="holes.png from the arm's STAGE 1, so the funnel "
                                       "is measured against the loop's starting state "
                                       "rather than the post-loop remainder")
args = ap.parse_args()

J = os.path.join(args.state, args.job)
meta = json.load(open(os.path.join(args.prep, "meta.json")))
cam = json.load(open(os.path.join(J, "cam.json")))
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
hpath = args.stage1_holes or os.path.join(args.state, "holes.png")
holes = np.asarray(Image.open(hpath).convert("L"), dtype=np.float32) / 255 > 0.5
edited = np.asarray(Image.open(os.path.join(J, "inpainted.png")).convert("RGB"),
                    dtype=np.float32) / 255
jobmask = np.asarray(Image.open(os.path.join(J, "mask.png")).convert("L"),
                     dtype=np.float32) / 255

pos_e = np.load(os.path.join(args.prep, "pos.npy"))
nor_e = np.load(os.path.join(args.prep, "nor.npy"))
lo = np.array(meta["lo"]); hi = np.array(meta["hi"])

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
fc = np.asarray(m.faces, dtype=np.int64)
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(fc.astype(np.uint32)))


def basis(yaw_d, el_d):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    right = np.cross(look, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    return look, right, up / (np.linalg.norm(up) + 1e-12)


def bilin(img, x, y):
    Hh, Ww = img.shape[:2]
    x = np.clip(x, 0.0, Ww - 1.001); y = np.clip(y, 0.0, Hh - 1.001)
    x0, y0 = x.astype(np.int64), y.astype(np.int64)
    fx, fy = x - x0, y - y0
    if img.ndim == 3:
        fx, fy = fx[:, None], fy[:, None]
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


hole_flat = holes.reshape(-1) & valid.reshape(-1)
hidx = np.where(hole_flat)[0]
n0 = len(hidx)
P = (pos_e.reshape(-1, 3)[hidx].astype(np.float64) * (hi - lo) + lo) / meta["maxabs"] * 0.5
N = nor_e.reshape(-1, 3)[hidx].astype(np.float64) * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
look, right, up = basis(cam["yaw"], cam["el"])
dtc = -look

rows = [("0  hole AND valid", n0)]
facing = N @ dtc
keep = facing > args.facing_min
hidx, P, N = hidx[keep], P[keep], N[keep]
rows.append((f"1  facing > {args.facing_min}", len(hidx)))

org = (P + N * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
    [org, np.broadcast_to(dtc.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
vis = ~np.isfinite(t)
hidx, P = hidx[vis], P[vis]
rows.append(("2  visible from this camera", len(hidx)))

bmid = np.array(cam["bmid"])
px = ((P - bmid) @ right / cam["h_ext"] + 0.5) * cam["W"] - 0.5
py = (0.5 - (P - bmid) @ up / cam["v_ext"]) * cam["H"] - 0.5
injob = bilin(jobmask, px, py) > 0.5
hidx, px, py = hidx[injob], px[injob], py[injob]
rows.append(("3  inside the job mask", len(hidx)))

c8 = np.concatenate([edited[:8, :8].reshape(-1, 3), edited[:8, -8:].reshape(-1, 3)])
bg = np.median(c8, axis=0)
fm = minimum_filter((np.abs(edited - bg).max(axis=-1) > 0.06).astype(np.float32), size=5)
dist = distance_transform_edt(fm > 0.5).astype(np.float32)
ok = bilin(dist, px, py) >= args.edge_dist
rows.append((f"4  edge-dist >= {args.edge_dist} (COMMITTED)", int(ok.sum())))

print(f"[funnel] {args.job}   yaw {cam['yaw']:+.0f} el {cam['el']:+.0f}")
prev = rows[0][1]
for name, n in rows:
    drop = prev - n
    print(f"[funnel] {name:<38s} {n:>10,}   "
          f"{'' if drop == 0 else f'-{drop:,} ({drop/max(prev,1)*100:.1f}% of previous)'}")
    prev = n
print(f"[funnel] survival {rows[-1][1]/max(n0,1)*100:.1f}% of the holes this camera "
      f"was offered")
