"""Where did this pixel's colour actually come from?

Three provenances are possible for any texel in a finished asset, and they mean
completely different things:

  TWINS      — stage 1 projected it from twin_front/twin_back. It is the styled
               reference being carried faithfully. If a patch is grime in the twin,
               it is grime here, and it is canon.
  BRUSH n    — stroke n synthesised it. That is invention, the same class as the
               belt braid E02 caught, and it is only as trustworthy as the prompt.
  DILATION   — no camera painted it; texpass_finalize grew it in from neighbours.
               Atlas adjacency is not surface adjacency, so the colour may have come
               from a geometrically unrelated island. This is the defect class.

Distinguishing them is a measurement, not a discussion, and this tool makes it one.

The per-stroke claim is reconstructed by REPLAYING texpass_iter.commit's filter chain
offline from the saved job directories, in stroke order, starting from stage 1's hole
map. commit is deterministic given (holes, job mask, inpainted image, cam, prep), all
of which are on disk, so the replay is exact and costs no GPU — rather than re-running
the loop and trusting that the brush reproduces byte-for-byte.

  texel_provenance.py --prep DIR --state DIR --stage1 styled_stage1.png
                      --order y+045_e+00,y+315_e+00,... [--render head.png]
                      [--regions "forehead:480,340,55;temple:430,415,35"]

Standards compliance: PIN_PER_STEP — stroke order and every path are explicit.
EXTERNAL_VERIFIER — reports provenance counts; it does not say whether any of them is
good, which is the Director's call.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import distance_transform_edt, median_filter, minimum_filter

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--state", required=True)
ap.add_argument("--stage1", required=True, help="stage-1 atlas; _holes/_styled_mask beside it")
ap.add_argument("--order", required=True, help="comma-separated job keys, in stroke order")
ap.add_argument("--facing-min", type=float, default=0.25)
ap.add_argument("--edge-dist", type=float, default=4.0)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--render", help="head render to sample through")
ap.add_argument("--head-crop", default="360,240,700,600")
ap.add_argument("--crop-res", type=int, default=1024)
ap.add_argument("--bound", type=float, default=0.55)
ap.add_argument("--pad", type=float, default=1.25)
ap.add_argument("--res", type=int, default=1024)
ap.add_argument("--regions", default="",
                help="name:cx,cy,r;... in render pixels")
ap.add_argument("--blotch", type=float, default=0.10,
                help="|luminance - local median| above which a pixel counts as a blotch")
ap.add_argument("--out-json")
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
base = os.path.splitext(args.stage1)[0]
holes = np.asarray(Image.open(base + "_holes.png").convert("L"), dtype=np.float32) / 255 > 0.5
styled0 = np.load(base + "_styled_mask.npy")

pos_e = np.load(os.path.join(args.prep, "pos.npy"))
nor_e = np.load(os.path.join(args.prep, "nor.npy"))
lo = np.array(meta["lo"]); hi = np.array(meta["hi"])

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
uv = np.asarray(m.visual.uv, dtype=np.float64)
maxabs_l = np.abs(v).max()
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / maxabs_l * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))


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


# 0 = twins (stage 1); 1..N = the stroke that claimed it; 255 = never painted -> dilation
claim = np.full(RES * RES, 255, dtype=np.uint8)
claim[np.where(styled0.reshape(-1))[0]] = 0
h = holes.reshape(-1).copy()
order = [k.strip() for k in args.order.split(",") if k.strip()]
print(f"[prov] replaying {len(order)} commits from stage-1 holes "
      f"{int((h & valid.reshape(-1)).sum()):,}", flush=True)
for si, keyname in enumerate(order, start=1):
    J = os.path.join(args.state, "job_" + keyname)
    cam = json.load(open(os.path.join(J, "cam.json")))
    edited = np.asarray(Image.open(os.path.join(J, "inpainted.png")).convert("RGB"),
                        dtype=np.float32) / 255
    jobmask = np.asarray(Image.open(os.path.join(J, "mask.png")).convert("L"),
                         dtype=np.float32) / 255
    hidx = np.where(h & valid.reshape(-1))[0]
    P = (pos_e.reshape(-1, 3)[hidx].astype(np.float64) * (hi - lo) + lo) / meta["maxabs"] * 0.5
    N = nor_e.reshape(-1, 3)[hidx].astype(np.float64) * 2.0 - 1.0
    N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
    look, right, up = basis(cam["yaw"], cam["el"])
    dtc = -look
    keep = (N @ dtc) > args.facing_min
    hidx, P, N = hidx[keep], P[keep], N[keep]
    org = (P + N * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(dtc.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
    vis = ~np.isfinite(t)
    hidx, P = hidx[vis], P[vis]
    bmid = np.array(cam["bmid"])
    px = ((P - bmid) @ right / cam["h_ext"] + 0.5) * cam["W"] - 0.5
    py = (0.5 - (P - bmid) @ up / cam["v_ext"]) * cam["H"] - 0.5
    inj = bilin(jobmask, px, py) > 0.5
    hidx, px, py = hidx[inj], px[inj], py[inj]
    c8 = np.concatenate([edited[:8, :8].reshape(-1, 3), edited[:8, -8:].reshape(-1, 3)])
    bg = np.median(c8, axis=0)
    fm = minimum_filter((np.abs(edited - bg).max(axis=-1) > 0.06).astype(np.float32), size=5)
    ok = bilin(distance_transform_edt(fm > 0.5).astype(np.float32), px, py) >= args.edge_dist
    hidx = hidx[ok]
    claim[hidx] = si
    h[hidx] = False
    print(f"[prov] stroke {si} {keyname}: claimed {len(hidx):,}; holes left "
          f"{int((h & valid.reshape(-1)).sum()):,}", flush=True)

vf = valid.reshape(-1)
print(f"\n[prov] whole atlas, valid texels {int(vf.sum()):,}")
for lab, sel in ([("TWINS (stage 1)", claim == 0)]
                 + [(f"BRUSH stroke {i} ({order[i-1]})", claim == i)
                    for i in range(1, len(order) + 1)]
                 + [("DILATION (never painted)", claim == 255)]):
    n = int((sel.reshape(-1) & vf).sum())
    print(f"[prov]   {lab:<34s} {n:>9,}  {n/max(int(vf.sum()),1)*100:5.1f}%")

if not args.render:
    raise SystemExit(0)

# ---- head camera, matching tools/verify/head_render.py exactly ----
CX0, CY0, CX1, CY1 = [float(x) for x in args.head_crop.split(",")]
b = args.bound
sx0 = (CX0 / args.crop_res) * 2 * b - b
sx1 = (CX1 / args.crop_res) * 2 * b - b
sz0 = b - (CY1 / args.crop_res) * 2 * b
sz1 = b - (CY0 / args.crop_res) * 2 * b
cx, cz = (sx0 + sx1) / 2, (sz0 + sz1) / 2
span = max(sx1 - sx0, sz1 - sz0) * args.pad
R = args.res
midy = (v[:, 1].min() + v[:, 1].max()) / 2
xs = cx + (np.arange(R) + 0.5) / R * span - span / 2
zs = cz + span / 2 - (np.arange(R) + 0.5) / R * span
gx, gz = np.meshgrid(xs, zs)
org = np.stack([gx, np.full_like(gx, midy - 6.0), gz], axis=-1)
ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
    [org, np.broadcast_to(np.array([0.0, 1.0, 0.0]), org.shape)],
    axis=-1).reshape(-1, 6).astype(np.float32)))
prim = ans["primitive_ids"].numpy().reshape(R, R)
buv = ans["primitive_uvs"].numpy().reshape(R, R, 2)
hit = np.isfinite(ans["t_hit"].numpy().reshape(R, R))
tex = np.full((R, R), -1, dtype=np.int64)
if hit.any():
    tr = f[prim[hit]]
    wu, wv = buv[hit][:, 0:1], buv[hit][:, 1:2]
    uvp = (1 - wu - wv) * uv[tr[:, 0]] + wu * uv[tr[:, 1]] + wv * uv[tr[:, 2]]
    ax = np.clip((uvp[:, 0] * RES).astype(np.int64), 0, RES - 1)
    ay = np.clip(((1 - uvp[:, 1]) * RES).astype(np.int64), 0, RES - 1)
    tex[hit] = ay * RES + ax

im = np.asarray(Image.open(args.render).convert("RGB"), dtype=np.float32) / 255
lum = im.mean(-1)
dev = np.abs(lum - median_filter(lum, size=5))
blotch = (dev > args.blotch) & hit
print(f"\n[prov] head render: figure {int(hit.sum()):,}px, "
      f"blotch (|lum-median|>{args.blotch}) {int(blotch.sum()):,}px "
      f"({blotch.sum()/max(int(hit.sum()),1)*100:.2f}%)")

LBL = {0: "TWINS", 255: "DILATION"}


def hist(sel, name):
    idx = tex[sel]
    idx = idx[idx >= 0]
    if not len(idx):
        print(f"[prov]   {name}: no surface")
        return {}
    c = claim[idx]
    out = {}
    print(f"[prov]   {name}  ({len(idx):,} px)")
    for k in [0] + list(range(1, len(order) + 1)) + [255]:
        n = int((c == k).sum())
        if not n:
            continue
        lab = LBL.get(k, f"BRUSH s{k} {order[k-1] if k <= len(order) else ''}")
        out[lab] = round(n / len(idx) * 100, 1)
        print(f"[prov]       {lab:<28s} {n:>7,}  {n/len(idx)*100:5.1f}%")
    return out


report = {"whole_head_blotch": hist(blotch, "ALL blotch pixels"),
          "whole_head_clean": hist(hit & ~blotch, "ALL clean pixels")}
yy, xx = np.mgrid[0:R, 0:R]
for spec in [s for s in args.regions.split(";") if s.strip()]:
    name, rest = spec.split(":")
    cxp, cyp, rr = [float(t) for t in rest.split(",")]
    disc = ((xx - cxp) ** 2 + (yy - cyp) ** 2) <= rr * rr
    print(f"\n[prov] region '{name}' at ({cxp:.0f},{cyp:.0f}) r{rr:.0f}")
    report[name + "_blotch"] = hist(disc & blotch, f"{name}: blotch")
    report[name + "_clean"] = hist(disc & hit & ~blotch, f"{name}: clean")

if args.out_json:
    json.dump(report, open(args.out_json, "w"), indent=1)
    print(f"\n[prov] wrote {args.out_json}")
np.save(os.path.join(args.state, "claim.npy"), claim.reshape(RES, RES))
print(f"[prov] wrote {os.path.join(args.state, 'claim.npy')}")
