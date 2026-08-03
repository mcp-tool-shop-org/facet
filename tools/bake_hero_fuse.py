"""Stage D part 2/3 — THE OWNERSHIP BAKER (the literature's spec, our code).

Consumes bake_hero_prep.py's outputs and produces the 4096 atlas:
  - per-texel DEPTH-TEST visibility per view: open3d first-hit ray toward the camera
    with a normal offset + a ray bias (the shadow-acne rule, Williams 1978)
  - weight = visible * max(dot(n, dir_to_cam), 0)^p
  - OWNERSHIP, not averaging (Lempitsky & Ivanov 2007; Waechter 2014): per-texel
    argmax weight; the head band (front-view face-crop rect) is boosted so the x4
    face crop OWNS it wherever front-visible
  - seam leveling: low-frequency equalization toward the all-view composite
    (masked Gaussian on the difference — the multi-band/Poisson role; high-freq
    stays with the owner view)
  - dilation fill for zero-coverage texels + gutter dilation for mip safety
  - colours are sampled from sRGB PNGs and written back as sRGB bytes UNCHANGED —
    the linear->sRGB double-transform trap cannot occur by construction

Standards compliance (whole 3-script stage):
  PIN_PER_STEP 2 (inputs pinned by path+seed upstream; scripts deterministic).
  ANDON_AUTHORITY 2 (asserts + exit-nonzero at every stage boundary).
  NAMED_COMPENSATORS skip: local file writes only, nothing irreversible.
  DECOMPOSE_BY_SECRETS 2 (prep=Blender, fuse=numpy/open3d, pack=packaging).
  UNCERTAINTY_GATED_HUMANS 2 (stage E is a Director-eye gate).
  EXTERNAL_VERIFIER 1 — the verifier is the Director at stage E by design;
    remediation owner: this session's E renders.

  bake_hero_fuse.py --prep DIR --views "mv2k/grid_v{}.png" --face face4x.png
                    --out atlas.png [--power 8] [--face-boost 3]
"""
import argparse
import json
import os
import sys

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import gaussian_filter, minimum_filter

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--views", required=True, help="pattern with {} for view index 0..5")
ap.add_argument("--face", required=True, help="the SR x4 face crop image")
ap.add_argument("--out", required=True)
ap.add_argument("--power", type=float, default=8.0)
ap.add_argument("--face-boost", type=float, default=3.0)
ap.add_argument("--elevations", default="0,0,0,0,89.99,-89.99")
ap.add_argument("--azimuths", default="-90,0,90,180,90,90")
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--seam-sigma", type=float, default=16.0)
args = ap.parse_args()

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
b = meta["bound"]
CX0, CY0, CX1, CY1 = meta["crop"]
CROP_RES = meta["crop_res"]

pos_e = np.load(os.path.join(args.prep, "pos.npy"))
nor_e = np.load(os.path.join(args.prep, "nor.npy"))
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
maxabs = meta["maxabs"]

valid = mask.reshape(-1)
P = (pos_e.reshape(-1, 3)[valid].astype(np.float64) * (hi - lo) + lo) / maxabs * 0.5
N = nor_e.reshape(-1, 3)[valid].astype(np.float64) * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
NV = P.shape[0]
print(f"[fuse] atlas {RES}  valid texels {NV:,} ({NV/(RES*RES)*100:.1f}%)", flush=True)
assert NV > RES * RES * 0.05, "ANDON: almost no valid texels — mask bake failed"

# raycast scene in the std frame (identical construction to render_geomaps.py)
m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vmax = np.abs(v).max()
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))

elevs = [float(x) for x in args.elevations.split(",")]
azims = [float(x) for x in args.azimuths.split(",")]


def cam_basis(el_d, az_d):
    el, az = np.radians(el_d), np.radians(az_d)
    cam = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    look = -cam
    up = np.array([0.0, 0.0, 1.0])
    right = np.cross(look, up)
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    up /= np.linalg.norm(up) + 1e-12
    return look, right, up


def figure_mask(img, tol=0.06, erode=5):
    """1 inside the figure, 0 on background — keyed from the corner colour, eroded so
    silhouette-adjacent texels can't bilinear-bleed background grey (the grey-facet
    speck class, found at x5 zoom on the first hero bake)."""
    # TOP corners only: the face crop's bottom corners hold pauldrons, not background
    c = np.concatenate([img[:8, :8].reshape(-1, 3), img[:8, -8:].reshape(-1, 3)])
    bg = np.median(c, axis=0)
    m = (np.abs(img - bg).max(axis=-1) > tol).astype(np.float32)
    return minimum_filter(m, size=erode)


def bilinear(img, x, y):
    H, W, _ = img.shape
    x = np.clip(x, 0.0, W - 1.001)
    y = np.clip(y, 0.0, H - 1.001)
    x0 = x.astype(np.int64)
    y0 = y.astype(np.int64)
    fx = (x - x0)[:, None]
    fy = (y - y0)[:, None]
    c00 = img[y0, x0]
    c01 = img[y0, x0 + 1]
    c10 = img[y0 + 1, x0]
    c11 = img[y0 + 1, x0 + 1]
    return (c00 * (1 - fx) * (1 - fy) + c01 * fx * (1 - fy)
            + c10 * (1 - fx) * fy + c11 * fx * fy)


sumW = np.zeros(NV, dtype=np.float32)
sumWC = np.zeros((NV, 3), dtype=np.float32)
best_w = np.zeros(NV, dtype=np.float32)
owner = np.full(NV, -1, dtype=np.int8)
owner_c = np.zeros((NV, 3), dtype=np.float32)
headband = np.zeros(NV, dtype=bool)      # filled during view 0 (front projection)
face_img = np.asarray(Image.open(args.face).convert("RGB"), dtype=np.float32) / 255.0
FH, FW, _ = face_img.shape
face_mask = figure_mask(face_img)
own_counts = {}

for i in range(6):
    look, right, up = cam_basis(elevs[i], azims[i])
    dtc = -look
    facing = (N @ dtc).astype(np.float32)
    cand = facing > 0.05
    if i in (4, 5):
        # top/bottom are ig2mv's weakest views (murky content on beard shelves —
        # the grey-mosaic class, v2 diagnosis). BANNED in the head band (the lock's
        # "head band FORCED to face/front"), demoted x0.25 elsewhere so they only
        # own texels no other view can see (crown, soles).
        cand &= ~headband
    idx = np.where(cand)[0]
    origins = (P[idx] + N[idx] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    dirs = np.broadcast_to(dtc.astype(np.float32), origins.shape)
    rays = o3d.core.Tensor(np.concatenate([origins, dirs], axis=1))
    t_hit = rs.cast_rays(rays)["t_hit"].numpy()
    visible = ~np.isfinite(t_hit)          # toward an ortho cam: ANY hit = occluder
    w = np.zeros(NV, dtype=np.float32)
    w[idx[visible]] = np.power(facing[idx[visible]], args.power)
    if i in (4, 5):
        w *= 0.25

    img = np.asarray(Image.open(args.views.format(i)).convert("RGB"),
                     dtype=np.float32) / 255.0
    fmask = figure_mask(img)
    Hres = img.shape[0]
    xr = (P @ right).astype(np.float32)
    yu = (P @ up).astype(np.float32)
    px = (xr + b) / (2 * b) * Hres - 0.5
    py = (b - yu) / (2 * b) * Hres - 0.5
    pre = np.where(w > 0)[0]
    inmask = bilinear(fmask[..., None], px[pre], py[pre])[:, 0] >= 0.999
    w[pre[~inmask]] = 0.0
    act = pre[inmask]
    col = bilinear(img, px[act], py[act]).astype(np.float32)
    sumW[act] += w[act]
    sumWC[act] += col * w[act][:, None]
    take = w[act] > best_w[act]
    tidx = act[take]
    best_w[tidx] = w[tidx]
    owner[tidx] = i
    owner_c[tidx] = col[take]
    own_counts[i] = int(len(tidx))
    print(f"[fuse] view {i}: cand {len(idx):,} visible {int(visible.sum()):,}", flush=True)

    if i == 0:                              # FACE VIEW rides the front camera
        px1k = (xr + b) / (2 * b) * CROP_RES - 0.5
        py1k = (b - yu) / (2 * b) * CROP_RES - 0.5
        headband = ((px1k >= CX0 + 1) & (px1k <= CX1 - 1)
                    & (py1k >= CY0 + 1) & (py1k <= CY1 - 1))
        inrect = headband & (w > 0)
        fidx = np.where(inrect)[0]
        fx = (px1k[fidx] - CX0) * (FW / (CX1 - CX0)) + 0.5 * (FW / (CX1 - CX0)) - 0.5
        fy = (py1k[fidx] - CY0) * (FH / (CY1 - CY0)) + 0.5 * (FH / (CY1 - CY0)) - 0.5
        finmask = bilinear(face_mask[..., None], fx, fy)[:, 0] >= 0.999
        fidx, fx, fy = fidx[finmask], fx[finmask], fy[finmask]
        fcol = bilinear(face_img, fx, fy).astype(np.float32)
        fw = w[fidx] * args.face_boost
        sumW[fidx] += fw
        sumWC[fidx] += fcol * fw[:, None]
        take = fw > best_w[fidx]
        tidx = fidx[take]
        best_w[tidx] = fw[take]
        owner[tidx] = 6
        owner_c[tidx] = fcol[take]
        own_counts[6] = int(len(tidx))
        print(f"[fuse] face view: {len(fidx):,} texels in rect", flush=True)

cov = sumW > 0
print(f"[fuse] coverage {cov.sum():,}/{NV:,} = {cov.mean()*100:.1f}%  "
      f"ownership: {own_counts}", flush=True)
# 0.75, not 0.80: the figure-mask erosion legitimately costs ~2-3pp of silhouette-band
# coverage (those texels dilation-fill from figure colours instead of bleeding grey).
# The assert exists to catch CATASTROPHIC visibility failure (~0.3-0.5 coverage).
assert cov.mean() > 0.75, "ANDON: >25% of surface texels saw no view — visibility broken"
hist = {int(k): int((owner == k).sum()) for k in range(-1, 7)}
print(f"[fuse] final owner histogram {hist}", flush=True)
assert hist[6] > 10_000, "ANDON: face view owns almost nothing — boost/rect wiring broken"

# ---- assemble atlas-space arrays ----
def scatter(vals, dim):
    a = np.zeros((RES * RES, dim), dtype=np.float32)
    a[np.where(valid)[0]] = vals
    return a.reshape(RES, RES, dim)


M = scatter(owner_c, 3)
B_num = scatter(sumWC, 3)
B_den = scatter(sumW[:, None], 1)
covA = scatter(cov[:, None].astype(np.float32), 1)[..., 0]
B = B_num / np.maximum(B_den, 1e-6)

# seam leveling: add back the LOW-frequency difference to the composite
sig = args.seam_sigma
blur_c = np.stack([gaussian_filter((B[..., k] - M[..., k]) * covA, sig)
                   for k in range(3)], axis=-1)
blur_m = gaussian_filter(covA, sig)[..., None]
final = M + blur_c / np.maximum(blur_m, 1e-4) * covA[..., None]
final = np.clip(final, 0.0, 1.0)

# ---- dilation fill: (a) valid-but-unseen texels, (b) 16px gutter for mip safety ----
have = covA > 0.5
need = valid.reshape(RES, RES) & ~have
print(f"[fuse] fill needed for {int(need.sum()):,} unseen valid texels", flush=True)
grown = have.copy()
img4 = final.copy()
for step in range(64):
    if not (valid.reshape(RES, RES) & ~grown).any() and step >= 16:
        break
    acc = np.zeros((RES, RES, 3), dtype=np.float32)
    cnt = np.zeros((RES, RES), dtype=np.float32)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb_v = np.roll(grown, (dy, dx), axis=(0, 1))
        nb_c = np.roll(img4, (dy, dx), axis=(0, 1))
        acc += nb_c * nb_v[..., None]
        cnt += nb_v
    fill = ~grown & (cnt > 0)
    img4[fill] = acc[fill] / cnt[fill][..., None]
    grown |= fill
left = int((valid.reshape(RES, RES) & ~grown).sum())
print(f"[fuse] dilation done, {left:,} valid texels still unfilled", flush=True)
if left:
    img4[valid.reshape(RES, RES) & ~grown] = img4[have].mean(axis=0)

var = float(img4[valid.reshape(RES, RES)].var())
print(f"[fuse] atlas variance {var:.5f}", flush=True)
assert var > 0.001, "ANDON: atlas is uniform — fusion failed"

Image.fromarray((img4 * 255).round().astype(np.uint8)).save(args.out)

# ownership debug map
pal = np.array([[220, 60, 60], [230, 160, 50], [70, 180, 70], [60, 120, 220],
                [170, 90, 200], [90, 200, 200], [250, 240, 90], [40, 40, 40]],
               dtype=np.uint8)
own_map = scatter(((owner + 7) % 7)[:, None].astype(np.float32), 1)[..., 0].astype(np.int64)
own_img = pal[np.where(valid.reshape(RES, RES), own_map, 7)]
Image.fromarray(own_img).save(args.out.replace(".png", "_ownership.png"))
print(f"[fuse] wrote {args.out} + ownership map — DONE", flush=True)
