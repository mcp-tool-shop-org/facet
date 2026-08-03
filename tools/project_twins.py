"""TEXTURE-SPACE PASS, stage 1 — project the styled twins onto the mesh's atlas.

The Director's flow (live-directed 2026-08-04): form-exaggerated clay -> mesh;
style lives on registered twin references generated at concept time; style is
applied ON THE ASSET, in texture space. This stage writes the twins into the
atlas wherever they can SEE the surface (depth-tested, ownership not averaging)
and emits an explicit HOLE MAP for everything they cannot. Stage 2 (progressive
hole inpainting with the local Qwen+saltroad brush) consumes the hole map.
Deliberately NO dilation fill — holes are stage 2's input, not a defect.

Twin registration (proven in project_prime.py / turn_render.py): ortho cameras,
vertical extent = bbox_z * 1.204, aspect 752:1024, centred on bbox mid; front twin
= yaw 0 (std az -90), back twin = yaw 180 (std az +90).

Consumes bake_hero_prep.py outputs (pos/nor/mask npy + meta.json + prep_uv.glb).

  project_twins.py --prep DIR --front twin_front.png --back twin_back.png
                   --out styled_partial.png [--power 4] [--hole-grey 0.42]
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import distance_transform_edt, gaussian_filter, minimum_filter

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--front", required=True)
ap.add_argument("--back", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--power", type=float, default=6.0)
# 0.45, not 0.10: at 0.10 surfaces up to ~84 deg off-axis accepted STRETCHED twin
# content — measured as long streak bands on skull sides and sword (Director
# rejection, 2026-08-04). An honest hole beats a smeared lie: stage 2's brush
# fills holes with real style but trusts whatever stage 1 marks as styled.
ap.add_argument("--facing-min", type=float, default=0.45)
ap.add_argument("--edge-dist", type=float, default=7.0,
                help="reject samples within this many px of the twin's silhouette "
                     "(mesh/twin outlines mismatch -> edge pixels are wrong-garment "
                     "or background-adjacent content)")
# The head band (front-view crop rect, from prep meta) is the best-registered
# region — canny-locked face content, low smear risk — and the LAST place we want
# diffusion inpainting holes. It gets looser acceptance than body/props, where
# the streaks lived (Director rejection round 2, 2026-08-04).
ap.add_argument("--head-facing-min", type=float, default=0.18)
ap.add_argument("--head-edge-dist", type=float, default=3.0)
ap.add_argument("--edge-ref", type=float, default=700.0,
                help="figure width, in twin pixels, that --edge-dist was tuned "
                     "against (A0's). Erosion is scaled by this figure's width "
                     "over that reference.")
ap.add_argument("--edge-floor", type=float, default=2.5,
                help="never erode less than this, however narrow the figure")
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--aspect", default="752,1024")
ap.add_argument("--hole-grey", type=float, default=0.42,
                help="neutral clay value holes carry in the PREVIEW atlas")
args = ap.parse_args()
AW, AH = [float(x) for x in args.aspect.split(",")]

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
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
CX0, CY0, CX1, CY1 = meta["crop"]
CROP_RES = meta["crop_res"]
b_std = 0.55
px1k = (P[:, 0] + b_std) / (2 * b_std) * CROP_RES
py1k = (b_std - P[:, 2]) / (2 * b_std) * CROP_RES
headband = ((px1k >= CX0) & (px1k <= CX1) & (py1k >= CY0) & (py1k <= CY1))
print(f"[twins] atlas {RES}  valid texels {NV:,}  head band {int(headband.sum()):,}",
      flush=True)

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
vmax = np.abs(v).max()
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))

# twin framing from the mesh bbox in the std frame (project_prime convention)
blo = v.min(axis=0)
bhi = v.max(axis=0)
bmid = (blo + bhi) / 2
v_ext = (bhi[2] - blo[2]) * 1.204
h_ext = v_ext * (AW / AH)


def figure_mask(img, tol=0.06, erode=5):
    c = np.concatenate([img[:8, :8].reshape(-1, 3), img[:8, -8:].reshape(-1, 3)])
    bg = np.median(c, axis=0)
    fm = (np.abs(img - bg).max(axis=-1) > tol).astype(np.float32)
    return minimum_filter(fm, size=erode)


def bilinear(img, x, y):
    H, W = img.shape[:2]
    x = np.clip(x, 0.0, W - 1.001)
    y = np.clip(y, 0.0, H - 1.001)
    x0 = x.astype(np.int64)
    y0 = y.astype(np.int64)
    fx = (x - x0)[:, None]
    fy = (y - y0)[:, None]
    a = img[y0, x0]
    b_ = img[y0, x0 + 1]
    c = img[y0 + 1, x0]
    d = img[y0 + 1, x0 + 1]
    if a.ndim == 1:
        fx, fy = fx[:, 0], fy[:, 0]
    return a * (1 - fx) * (1 - fy) + b_ * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy


VIEWS = [
    {"name": "front", "path": args.front, "dtc": np.array([0.0, -1.0, 0.0]),
     "right": np.array([1.0, 0.0, 0.0])},
    {"name": "back", "path": args.back, "dtc": np.array([0.0, 1.0, 0.0]),
     "right": np.array([-1.0, 0.0, 0.0])},
]
up = np.array([0.0, 0.0, 1.0])

best_w = np.zeros(NV, dtype=np.float32)
owner_c = np.zeros((NV, 3), dtype=np.float32)
sumW = np.zeros(NV, dtype=np.float32)
sumWC = np.zeros((NV, 3), dtype=np.float32)

reachable = np.zeros(NV, dtype=bool)

for view in VIEWS:
    img = np.asarray(Image.open(view["path"]).convert("RGB"), dtype=np.float32) / 255.0
    # Prefer the EXACT mask restylize_views.py saved beside the twin. Re-keying a
    # painted twin heuristically is where background gets projected onto the mesh:
    # on A0's twins the corner-median path keyed 30% of the bottom corners as
    # figure, which a centred standing figure cannot reach (measured, E01).
    mpath = os.path.splitext(view["path"])[0] + "_mask.png"
    if os.path.exists(mpath):
        fm = (np.asarray(Image.open(mpath).convert("L"), dtype=np.float32)
              / 255.0 > 0.5).astype(np.float32)
        print(f"[twins] {view['name']}: exact mask {os.path.basename(mpath)} "
              f"({fm.mean() * 100:.1f}% figure)", flush=True)
    else:
        fm = figure_mask(img)
        print(f"[twins] WARNING {view['name']}: no {os.path.basename(mpath)} — "
              f"falling back to corner-median keying ({fm.mean() * 100:.1f}% "
              f"figure). This path keys background gradients and cast shadows as "
              f"figure; regenerate the twin with restylize_views.py.", flush=True)
    H, W = img.shape[:2]
    dtc = view["dtc"]
    facing = (N @ dtc).astype(np.float32)
    fmin = np.where(headband, args.head_facing_min, args.facing_min)
    idx = np.where(facing > fmin)[0]
    origins = (P[idx] + N[idx] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    dirs = np.broadcast_to(dtc.astype(np.float32), origins.shape)
    t_hit = rs.cast_rays(o3d.core.Tensor(
        np.concatenate([origins, dirs], axis=1)))["t_hit"].numpy()
    vis = ~np.isfinite(t_hit)
    idx = idx[vis]
    # facing + visibility, BEFORE the edge test: this is the ceiling a two-view
    # projection can reach on this mesh. The old coverage number divided by every
    # valid texel including ones no camera can see, which made 100% impossible and
    # made A0's contaminated 62% look like headroom.
    reachable[idx] = True
    xr = (P[idx] @ view["right"]) - (bmid @ view["right"])
    zu = (P[idx] @ up) - (bmid @ up)
    px = (xr / h_ext + 0.5) * W - 0.5
    py = (0.5 - zu / v_ext) * H - 0.5
    dist_in = distance_transform_edt(fm > 0.5).astype(np.float32)
    # Erosion cost scales with perimeter-to-area, not width: 7 px off each side of
    # a ~40 px arm removes a third of it, while the same 7 px barely dents a wide
    # blobby silhouette. The defaults were tuned on A0's figure, so scale them by
    # this figure's width against that reference.
    fx = np.where((fm > 0.5).any(axis=0))[0]
    fig_w = float(fx.max() - fx.min()) if len(fx) else float(W)
    esc = fig_w / args.edge_ref
    ed_body = max(args.edge_floor, args.edge_dist * esc)
    ed_head = max(args.edge_floor, args.head_edge_dist * esc)
    print(f"[twins] {view['name']}: figure {fig_w:.0f}px wide -> edge-dist "
          f"{ed_body:.1f}px body / {ed_head:.1f}px head "
          f"(unscaled {args.edge_dist:.1f}/{args.head_edge_dist:.1f})", flush=True)
    ed = np.where(headband[idx], ed_head, ed_body)
    inm = bilinear(dist_in, px, py) >= ed
    idx, px, py = idx[inm], px[inm], py[inm]
    col = bilinear(img, px, py).astype(np.float32)
    w = np.power(facing[idx], args.power)
    sumW[idx] += w
    sumWC[idx] += col * w[:, None]
    take = w > best_w[idx]
    best_w[idx[take]] = w[take]
    owner_c[idx[take]] = col[take]
    print(f"[twins] {view['name']}: styled {len(idx):,} texels", flush=True)

seen = best_w > 0
print(f"[twins] styled/valid    {seen.sum():,}/{NV:,} = {seen.mean()*100:.1f}% "
      f"(legacy number — denominator includes texels NO camera can see)", flush=True)
print(f"[twins] styled/REACHABLE {seen.sum():,}/{reachable.sum():,} = "
      f"{seen.sum()/max(reachable.sum(),1)*100:.1f}%  <- the real ratio, ceiling 1.0",
      flush=True)
print(f"[twins] reachable/valid  {reachable.sum():,}/{NV:,} = "
      f"{reachable.mean()*100:.1f}% (what two views can physically reach here)",
      flush=True)
# The old `assert seen.mean() > 0.30` is SUSPENDED, not retuned. It encoded a
# constant read off A0, whose twin keyed a third of its own background as figure;
# on that measurement A0 styled 81-100% of a 61.5% ceiling, which is impossible.
# No calibrated threshold exists for the new ratio yet, so this gate only catches
# the degenerate cases rather than inventing another number to inherit.
assert reachable.sum() > 0, "ANDON: no texel is reachable — registration broken"
assert seen.sum() > 0, "ANDON: nothing styled at all"

def scatter(vals, dim):
    a = np.zeros((RES * RES, dim), dtype=np.float32)
    a[np.where(valid)[0]] = vals
    return a.reshape(RES, RES, dim)


M = scatter(owner_c, 3)
B = scatter(sumWC, 3) / np.maximum(scatter(sumW[:, None], 1), 1e-6)
covA = scatter(seen[:, None].astype(np.float32), 1)[..., 0]
blur_c = np.stack([gaussian_filter((B[..., k] - M[..., k]) * covA, 16.0)
                   for k in range(3)], axis=-1)
blur_m = gaussian_filter(covA, 16.0)[..., None]
styled = np.clip(M + blur_c / np.maximum(blur_m, 1e-4) * covA[..., None], 0, 1)

validA = valid.reshape(RES, RES)
hole = validA & (covA < 0.5)
atlas = styled.copy()
atlas[hole] = args.hole_grey
var = float(atlas[validA].var())
print(f"[twins] atlas variance {var:.5f}  holes {int(hole.sum()):,}", flush=True)
assert var > 0.001, "ANDON: atlas uniform"

Image.fromarray((atlas * 255).round().astype(np.uint8)).save(args.out)
Image.fromarray((hole * 255).astype(np.uint8)).save(
    args.out.replace(".png", "_holes.png"))
np.save(args.out.replace(".png", "_styled_mask.npy"), covA > 0.5)
print(f"[twins] wrote {args.out} + _holes.png + _styled_mask.npy — DONE", flush=True)
