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
from scipy.ndimage import (distance_transform_edt, gaussian_filter, label,
                           maximum_filter, minimum_filter)

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
ap.add_argument("--edge-frac", type=float, default=1.0 / 3.0,
                help="E08 A3 invariant: the edge erosion may never exceed this "
                     "fraction of a structure's OWN local half-width. For a bar "
                     "the area it removes equals this number exactly.")
# WITHDRAWN (E08 Amendment 3): --edge-max-area-loss halted on stratum area-loss, a
# perimeter-to-area statistic that swings +/-10 points on shape alone. It fired on a
# build whose invariant held exactly. The stratum table survives as a DIAGNOSTIC.
ap.add_argument("--bg-de", type=float, default=10.0,
                help="CIE76 dE below which a sampled colour counts as the twin's "
                     "background. 10 is the external constant for 'plainly different "
                     "colour', so under it means indistinguishable from background.")
ap.add_argument("--bg-max-pct", type=float, default=2.0,
                help="ANDON: halt if more than this share of the texels a relaxed "
                     "erosion NEWLY admits sit within --bg-de of the twin's "
                     "background. Chosen, and stated so it can be ruled on: A2's "
                     "ratified relaxation measured 0.18% against 0.32% for the "
                     "already-trusted set, so 2% is an order of magnitude above work "
                     "already accepted, while E01's contamination (a third of a "
                     "region keyed as figure) would exceed it outright.")
ap.add_argument("--edge-min-struct", type=int, default=50,
                help="structures smaller than this are keying specks, not parts")
ap.add_argument("--edge-absolute", action="store_true",
                help="historical absolute erosion, scaled by GLOBAL figure width. "
                     "Reproducing any arm before E08 needs --mask-keyed AND this.")
ap.add_argument("--mask-keyed", action="store_true",
                help="answer 'is there surface here' with restylize_views' keyed clay "
                     "mask instead of the raycast silhouette. Reproduces every arm "
                     "before E08 Arm A byte-for-byte; measured to lose 34,970 px of a "
                     "146,356 px silhouette on W3, interior rather than at the rim.")
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


def srgb_to_lab(rgb):
    """sRGB -> linear -> XYZ(D65) -> CIE Lab. dE below is CIE76."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


def local_thickness(dist):
    """Half-width of the structure each pixel belongs to.

    `dist` is the distance transform of the figure mask, so dist(c) is the radius of
    the largest disc centred at c that fits inside the figure, and a pixel p belongs to
    that disc when ||p - c|| <= dist(c). Taking the largest such disc over all c gives
    the local thickness (Hildebrand & Ruegsegger). Evaluated with one EDT per integer
    radius band rather than an explicit disc dilation, which would be O(r^2) per pixel.
    """
    R = np.zeros_like(dist, dtype=np.float32)
    for r in range(int(np.ceil(dist.max())), 0, -1):
        core = dist >= r
        if not core.any():
            continue
        cover = distance_transform_edt(~core) <= r
        R[cover & (R == 0)] = r
    return R


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
    # TWO masks, two questions. Conflating them is what cost 480k texels:
    #   is there real surface here?   -> the MESH silhouette, NOT eroded
    #   is the paint here trustworthy? -> the TWIN's painted figure, eroded
    #
    # The first question is answered from GEOMETRY, by raycasting the view. It used to
    # be answered by `figure_mask` thresholding the CLAY RENDER, saved beside the twin
    # by restylize_views.py — a keyed render impersonating a silhouette. E01 had
    # already established that a Workbench clay is flat grey on flat grey and that a
    # threshold cannot find the figure in it; it fixed the CONTROL-IMAGE path by
    # compositing onto contrast first, and left this consumer keying the same render.
    # Measured on W3 (E08 Arm A): the saved mask held 111,602 px of a 146,356 px
    # silhouette — IoU 0.76, 34,970 px of mesh missing, and the loss INTERIOR rather
    # than a rim: a stripe down the whole blade, patches through pauldrons, chest,
    # greaves and boots, following shading boundaries. It cost 257,511 texels of
    # reference. Registration was ruled out at shift (0,0). Nothing caught it for four
    # experiments because nothing ever compared the mask to the geometry.
    # Geometry has no tolerance, no threshold, and no dependence on how the render was
    # lit. --mask-keyed reproduces the historical path.
    #
    # ⚠ CORRECTED IN PLACE (E08 Arm A). This block used to justify eroding the twin's
    # mask with: "The twin is painted fatter than the mesh (measured 15.8% of frame
    # against 9.9%, IoU 0.777), so eroding the TWIN's mask never reaches the mesh
    # boundary." Both numbers reproduce exactly — against the wrong objects. 15.81% is
    # the ERODED TWIN figure and 9.94% is the SAVED KEYED MASK, so that was twin
    # against mask, never twin against mesh. Against the true silhouette:
    #   twin 17.43% of frame   vs   MESH 19.01%   IoU 0.911
    # The MESH is fatter, and 12,625 px of it falls outside the twin's painted figure.
    # Eroding the twin's mask therefore DOES reach the mesh boundary. The erosion is
    # kept because E01's background-keying failure is real and is a separate question —
    # it answers "is the paint trustworthy", which is the twin's own to answer — but it
    # is no longer justified by a claim that the twin covers the mesh, because it does
    # not.
    twin_fm = figure_mask(img)
    fm = twin_fm
    H, W = img.shape[:2]
    dtc = view["dtc"]
    if args.mask_keyed:
        mpath = os.path.splitext(view["path"])[0] + "_mask.png"
        assert os.path.exists(mpath), f"ANDON: --mask-keyed but no {mpath}"
        mesh_fm = maximum_filter(
            (np.asarray(Image.open(mpath).convert("L"), dtype=np.float32)
             / 255.0 > 0.5).astype(np.float32), size=5)
        print(f"[twins] {view['name']}: HISTORICAL keyed mask "
              f"({mesh_fm.mean() * 100:.1f}% of frame after un-erode)", flush=True)
    else:
        look = -dtc
        rgt = view["right"]
        upv = np.cross(rgt, look)
        upv /= np.linalg.norm(upv) + 1e-12
        gx_ = (np.arange(W) + 0.5) / W * h_ext - h_ext / 2
        gy_ = v_ext / 2 - (np.arange(H) + 0.5) / H * v_ext
        g1, g2 = np.meshgrid(gx_, gy_)
        o2 = (bmid[None, None, :] + g1[..., None] * rgt[None, None, :]
              + g2[..., None] * upv[None, None, :] - look[None, None, :] * 2.0)
        mesh_fm = np.isfinite(rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [o2, np.broadcast_to(look, o2.shape)], axis=-1
        ).reshape(-1, 6).astype(np.float32)))["t_hit"].numpy().reshape(H, W)
        ).astype(np.float32)
        print(f"[twins] {view['name']}: mesh silhouette from GEOMETRY "
              f"({mesh_fm.mean() * 100:.1f}% of frame), twin paint "
              f"{twin_fm.mean() * 100:.1f}%", flush=True)
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
    # ⚠ REBUILT (E08 A3). This erosion used to be an ABSOLUTE distance, scaled by the
    # figure's GLOBAL width and then applied to LOCAL structures. On W3 that took
    # 3.8 px off each side of a ~15 px blade — 51% of its half-width — so the blade
    # arrived at stage 2 as a hole for the brush to invent into, and reached the
    # Director wearing skin tones. Third instance of one shape in this repo: the blade
    # pixel-rectangle texpass_loop.ps1 was rewritten to remove, E01's 480k-texel
    # silhouette-band erosion, and this.
    #
    # THE INVARIANT: never remove more than a bounded fraction of a structure's OWN
    # width. `dist_in` already carries it — the maximal inscribed disc covering a pixel
    # is the local half-width — so the bound needs no new input. For a bar of
    # half-width R eroded by e the area removed is exactly e/R, which makes
    # --edge-frac simultaneously the input bound and the area it costs; blobs, having
    # lower perimeter-to-area, come in under it.
    #
    # The erosion is NOT deleted. Its stated justification is void (the mesh is fatter
    # than the twin — see above), but the white-fleck failure it was built for is real
    # and nothing else addresses it.
    fx = np.where((fm > 0.5).any(axis=0))[0]
    fig_w = float(fx.max() - fx.min()) if len(fx) else float(W)
    esc = fig_w / args.edge_ref
    ed_body = max(args.edge_floor, args.edge_dist * esc)
    ed_head = max(args.edge_floor, args.head_edge_dist * esc)
    thick = local_thickness(dist_in)          # the gate needs it in BOTH modes
    if args.edge_absolute:
        ed = np.where(headband[idx], ed_head, ed_body)
        e_img = np.full_like(dist_in, ed_body)
        print(f"[twins] {view['name']}: HISTORICAL absolute edge-dist {ed_body:.1f}px "
              f"body / {ed_head:.1f}px head (figure {fig_w:.0f}px wide)", flush=True)
    else:
        cap = args.edge_frac * bilinear(thick, px, py)
        ed = np.minimum(np.where(headband[idx], ed_head, ed_body), cap)
        e_img = np.minimum(ed_body, args.edge_frac * thick)
        med = float(np.median((args.edge_frac * thick)[fm > 0.5]))
        print(f"[twins] {view['name']}: edge-dist = min({ed_body:.1f}px, "
              f"{args.edge_frac:.3f} x local half-width); median local cap {med:.1f}px "
              f"(figure {fig_w:.0f}px wide)", flush=True)
    # DIAGNOSTIC, required, and never a halt (E08 Amendment 3). Erosion cost by LOCAL
    # HALF-WIDTH — the row that earned this arm: under the historical absolute distance
    # the 1-2 / 2-4 / 4-8 px strata lose 100 / 100 / 77.6% against 4.4% at 32px+, and
    # the blade lives in that 4-8 px stratum, three quarters of it removed by a guard
    # built to delete a 1-2 px rim.
    # It carried a halt for exactly one run and the halt was withdrawn: stratum
    # area-loss is a perimeter-to-area statistic that swings +/-10 points on SHAPE
    # alone, so it cannot carry one. A diagnostic and a gate are different objects.
    # (Stratification by thickness replaced a per-connected-component version that was
    # rejected on measurement — the twin's whole front figure is ONE component of
    # 121,709 px because the blade touches the hand, so a blade losing three quarters
    # of its area read as 12.3% overall.)
    fig = fm > 0.5
    kept = dist_in >= e_img
    print(f"[twins] {view['name']}: erosion cost by structure half-width —", flush=True)
    for a_, b_ in ((1, 2), (2, 4), (4, 8), (8, 16), (16, 32), (32, 1e9)):
        sel = fig & (thick >= a_) & (thick < b_)
        n = int(sel.sum())
        if n < args.edge_min_struct:
            continue
        lost = 1.0 - float((sel & kept).sum()) / n
        nm = f"{a_}-{'inf' if b_ > 1e8 else b_}px"
        print(f"[twins]     half-width {nm:<9s} {n:>8,}px  removed {lost*100:5.1f}%",
              flush=True)
    d_s = bilinear(dist_in, px, py)
    e_abs_s = np.where(headband[idx], ed_head, ed_body)
    # IMPLEMENTATION ASSERTION, not a gate: e <= frac*R holds BY CONSTRUCTION, so this
    # cannot fail on a correct build. It catches an operand-order slip or a bad
    # half-width lookup. By this repo's own rule that makes it a unit test; it is not
    # promoted to an andon, and halting on it fired on correct work once already.
    if not args.edge_absolute:
        R_s = bilinear(thick, px, py)
        ok_inv = ed <= args.edge_frac * np.maximum(R_s, 1e-6) + 1e-4
        assert ok_inv.all(), (
            f"IMPLEMENTATION: e > {args.edge_frac:.4f} x local half-width for "
            f"{int((~ok_inv).sum()):,} samples — the cap is not being applied")
    inm = (d_s >= ed) & (bilinear(mesh_fm[..., None], px, py)[:, 0] > 0.5)
    idx, px, py = idx[inm], px[inm], py[inm]
    col = bilinear(img, px, py).astype(np.float32)

    # ANDON, on the direction the invariant does NOT bound (E08 Amendment 3).
    # e <= frac*R forecloses OVER-erosion by construction — which is exactly why a
    # halt there fires on correct work. The live risk of a LOOSER acceptance is the
    # opposite one: admitting the twin's BACKGROUND at its painted boundary, E01's
    # white-fleck failure, about which the invariant says nothing.
    # Probe: the texels the relaxation newly admits must not approach the background
    # colour. Reported against the texels that would have been accepted anyway, so the
    # comparison is against a set already trusted in the SAME image rather than an
    # invented absolute.
    bgc = np.median(np.concatenate([img[:8, :8].reshape(-1, 3),
                                    img[:8, -8:].reshape(-1, 3)]), axis=0)
    relaxed = d_s[inm] < e_abs_s[inm]
    dE_bg = np.linalg.norm(srgb_to_lab(col) - srgb_to_lab(bgc[None, :]), axis=-1)
    p_tr = float((dE_bg[~relaxed] < args.bg_de).mean() * 100) if (~relaxed).any() else 0.0
    if relaxed.any():
        p_rx = float((dE_bg[relaxed] < args.bg_de).mean() * 100)
        print(f"[twins] {view['name']}: background probe — newly admitted "
              f"{int(relaxed.sum()):,} texels, median dE {np.median(dE_bg[relaxed]):.1f} "
              f"from background rgb {tuple(int(c*255) for c in bgc)}; "
              f"within dE {args.bg_de:.0f} of it {p_rx:.2f}% "
              f"(already-trusted texels: {p_tr:.2f}%)", flush=True)
        assert p_rx <= args.bg_max_pct, (
            f"ANDON: {p_rx:.2f}% of newly-admitted texels sit within dE {args.bg_de:.0f} "
            f"of the twin's background, over the {args.bg_max_pct:.1f}% limit — the "
            f"relaxed acceptance is projecting background onto the mesh.")
    else:
        print(f"[twins] {view['name']}: background probe — no relaxation to test "
              f"(already-trusted texels within dE {args.bg_de:.0f} of background: "
              f"{p_tr:.2f}%)", flush=True)
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
