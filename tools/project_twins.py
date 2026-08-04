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
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import subject_profile
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
ap.add_argument("--front", help="twin at yaw 0. Required unless --view is used.")
ap.add_argument("--back", help="twin at yaw 180. Required unless --view is used.")
ap.add_argument("--view", action="append", default=[], metavar="IDX=PATH",
                help="N-view mode (E08 Arm B): a twin at view index IDX, repeatable. "
                     "Yaw is IDX*--step, matching turn_render's orbit. Supplying any "
                     "--view REPLACES the --front/--back pair. Two views was never a "
                     "property of the projection — everything below VIEWS was already "
                     "N-general — it was a property of this argument list.")
ap.add_argument("--step", type=float, default=45.0,
                help="degrees of yaw per view index; must match turn_render's --step")
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
ap.add_argument("--key-corner-median", action="store_true",
                help="key the twin's paint mask off a single corner median, the "
                     "historical path. Needed to reproduce any arm before E08, and "
                     "measured to fail on any non-flat backdrop.")
ap.add_argument("--bbox-tol", type=float, default=0.25,
                help="ANDON: halt if the keyed twin figure's bbox exceeds the mesh "
                     "silhouette's by more than this in either dimension. Free, and it "
                     "tests the failure mode — a broken key overshot by 93% while every "
                     "correct twin measured within 1%.")
ap.add_argument("--trust-intersect", action=argparse.BooleanOptionalAction, default=True,
                help="ADOPTED AS THE ROUTE DEFAULT, E08 Amendment 27. "
                     "--no-trust-intersect restores the pre-adoption operand and is "
                     "required, alongside the other legacy flags, to reproduce any arm "
                     "before Amendment 27. Measured cost of adoption on the two-camera "
                     "pair: -7,574 styled texels (1,050,368 -> 1,042,794), 43.7% -> "
                     "43.4% of valid, 83.0% -> 82.4% of reachable, ZERO gains, ZERO "
                     "losses in the two thinnest half-width strata, every loss within "
                     "5px of paint that sat on no surface. "
                     "E08 Amendment 26: restrict the TRUST mask to surface that "
                     "exists — fm becomes twin_fm AND mesh_fm before the distance "
                     "transform. Paint outside the silhouette is on no surface at all, "
                     "so asking whether it is trustworthy is a category error, and "
                     "letting it set the boundary of the distance field corrupts the "
                     "answer for texels that DO exist. Measured on the re-rolled "
                     "twin_6, whose cast shadow is CONNECTED to the figure: 27.49% of "
                     "the figure's texels get an edge distance changed by >0.5px, "
                     "21.24% by >2px, max 36.22px. ⚠ Under --mask-keyed, mesh_fm is the "
                     "size-5 DILATED sidecar, not the exact silhouette, so combining "
                     "the two flags is NOT the exact-silhouette intersection.")
ap.add_argument("--reg-iou-min", type=float, default=0.80,
                help="ANDON (E08 Amendment 27): halt if IoU(raw twin_fm, the EXACT "
                     "raycast silhouette) falls below this on any view. Derived from "
                     "both sides of the line and from neither the arm it gates — every "
                     "adjudicated ARMB view measures 0.8329-0.9533 (worst is the "
                     "shadowed profile, view 6) and every measured registration failure "
                     "sits at or below 0.578 (the E01-era sidecars, 0.5230 / 0.5780). "
                     "0.80 clears the worst adjudicated view by 0.033 and the nearest "
                     "failure by 0.22. It CANNOT fire on the current eight — they are "
                     "its calibration set — and its jurisdiction is future twins. "
                     "It CANNOT catch identity substitution: the better-registered "
                     "different man measured 0.9040 against 0.9088, which stays the "
                     "prompt's job. This REPLACES the bbox assert, which tested extent "
                     "against the figure's own width and so fired on the narrowest view "
                     "while passing the two dirtiest. ⚠ Evaluated only where the exact "
                     "silhouette exists, i.e. NOT under --mask-keyed, where mesh_fm is "
                     "the dilated sidecar (which measures 0.6735 / 0.7001 and would "
                     "halt a legacy reproduction on the wrong operand).")
ap.add_argument("--diag-npz",
                help="dump per-view acceptance internals (candidate indices, sample "
                     "edge distances and thresholds, the dist_in field, mesh_fm) so a "
                     "gain/loss decomposition can be computed offline. Writes nothing "
                     "back into the computation — R0 must reproduce with this set.")
ap.add_argument("--mask-keyed", action="store_true",
                help="answer 'is there surface here' with restylize_views' keyed clay "
                     "mask instead of the raycast silhouette. Reproduces every arm "
                     "before E08 Arm A byte-for-byte; measured to lose 34,970 px of a "
                     "146,356 px silhouette on W3, interior rather than at the rim.")
ap.add_argument("--hole-grey", type=float, default=0.42,
                help="neutral clay value holes carry in the PREVIEW atlas")
args = ap.parse_args(subject_profile.bind(ap, "project_twins.py", None))
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


def figure_mask(img, tol=0.06, erode=5, corner_median=False):
    """The twin's own painted figure — "is the paint trustworthy", the one question
    geometry cannot answer, and the last duty this function still holds.

    The background model is FITTED, not a corner median. Corner-median keying has now
    failed three independent times in this project: on A0's painted twin it keyed 30%
    of the bottom corners as figure (E01); on the grey-on-grey clay it lost 24% of the
    silhouette (E08 Arm A); and on a diffusion backdrop it returned painted fractions
    of 31-76% against a 19.01% truth, with figure bounding boxes 751 px wide in a 752 px
    frame (E08 registration). Diffusion paints a lit studio gradient, so a single median
    is the wrong model and every pixel far from a corner exceeds tolerance.

    A per-channel quadratic surface, least-squares over a border ring the figure cannot
    reach, REDUCES to the corner median when the background really is flat — measured:
    the shipped twins move 17.43% -> 17.38% of frame. Nothing prior loses comparability.
    --key-corner-median restores the historical path.
    """
    if corner_median:
        c = np.concatenate([img[:8, :8].reshape(-1, 3), img[:8, -8:].reshape(-1, 3)])
        bg = np.median(c, axis=0)
        fm = (np.abs(img - bg).max(axis=-1) > tol).astype(np.float32)
        return minimum_filter(fm, size=erode)
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
    fm = (np.abs(resid).max(axis=-1) > tol).astype(np.float32)
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


def cam_axes(deg):
    """Direction-to-camera and camera-right for a yaw, matching turn_render's orbit.

    turn_render sets  cam.location = (mid.x + r*sin(th), mid.y - r*cos(th), mid.z)
    with rotation_euler (90deg, 0, th), so dtc = (sin th, -cos th, 0) and the camera's
    right is (cos th, sin th, 0). Verified against turn_render rather than assumed, and
    independently against the shipped silhouette masks (silhouette_masks.py --anchor,
    0 differing px at views 0 and 4).

    ⚠ THE SNAP IS LOAD-BEARING, not tidiness. sin(pi) is 1.2246e-16, not 0, so computing
    the back view's axes would perturb every ray by that much and the two-view default
    would stop reproducing A2 exactly. Components within 1e-12 of 0 or +-1 are snapped to
    the exact value, which makes yaw 0 and 180 bit-identical to the literals this
    replaced. Multiples of 45 that are not multiples of 90 keep their irrational
    components — nothing anchors them.
    """
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


if args.view:
    VIEWS = []
    for spec in args.view:
        k, _, p = spec.partition("=")
        assert p, f"ANDON: --view wants IDX=PATH, got {spec!r}"
        assert os.path.exists(p), f"ANDON: --view {k} path does not exist: {p}"
        deg = int(k) * args.step
        d, r = cam_axes(deg)
        VIEWS.append({"name": f"y{deg:+06.1f}", "path": p, "dtc": d, "right": r})
    assert len({v["name"] for v in VIEWS}) == len(VIEWS), (
        "ANDON: duplicate view index in --view")
    print(f"[twins] N-VIEW mode: {len(VIEWS)} cameras at "
          f"{', '.join(v['name'] for v in VIEWS)}", flush=True)
else:
    assert args.front and args.back, (
        "ANDON: supply --front and --back, or one or more --view IDX=PATH")
    df, rf = cam_axes(0.0)
    db, rb = cam_axes(180.0)
    VIEWS = [
        {"name": "front", "path": args.front, "dtc": df, "right": rf},
        {"name": "back", "path": args.back, "dtc": db, "right": rb},
    ]
    assert np.array_equal(df, [0.0, -1.0, 0.0]) and np.array_equal(rf, [1.0, 0.0, 0.0])
    assert np.array_equal(db, [0.0, 1.0, 0.0]) and np.array_equal(rb, [-1.0, 0.0, 0.0])
up = np.array([0.0, 0.0, 1.0])

best_w = np.zeros(NV, dtype=np.float32)
owner_c = np.zeros((NV, 3), dtype=np.float32)
# WHICH view won, not just what colour it carried (E04 Ruling 2). The ownership partition
# is computed here and was thrown away; E04 Task 1 had to reconstruct it from diag_8cam's
# accepted sets to identify the crown seam, and could not obtain the blend at all. Both are
# free at this point and both are now saved. Additive only - nothing below reads owner_i.
owner_i = np.full(NV, -1, dtype=np.int8)
sumW = np.zeros(NV, dtype=np.float32)
sumWC = np.zeros((NV, 3), dtype=np.float32)

reachable = np.zeros(NV, dtype=bool)
DIAG = {}

for _view_i, view in enumerate(VIEWS):
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
    twin_fm = figure_mask(img, corner_median=args.key_corner_median)
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

    # THE TRUST MASK. One mask cannot answer two questions, and until E08 Amendment 26
    # this one was asked a THIRD: "is the paint here trustworthy" was evaluated over a
    # region that includes pixels sitting on NO SURFACE AT ALL. The re-rolled twin_6
    # painted a cast shadow on the ground, CONNECTED to the figure, and the connection is
    # what does the damage: `distance_transform_edt` measures distance to the mask's
    # boundary, so a phantom boundary metres below the feet inflates the edge distance
    # for every real texel near ground contact. Measured with the shadow removed by hand:
    # 27.49% of the figure's texels move >0.5px, 21.24% >2px, max 36.22px.
    # The intersection is a CORRECTION, not a tune — "restrict the trust mask to surface
    # that exists" is derivable from the two-questions rule and should have been written
    # when A2 landed. It is behind a flag anyway, because it moves dist_in at the rim for
    # EVERY twin and therefore restates A2's number, which does not get replaced quietly.
    if args.trust_intersect:
        fm = ((twin_fm > 0.5) & (mesh_fm > 0.5)).astype(np.float32)
    else:
        fm = twin_fm

    # THE RAW KEY'S OWN DIAGNOSTICS. Measured on twin_fm before any intersection, so
    # they stay comparable across both settings of the flag and keep saying something the
    # intersection cannot make true by construction. A twin that paints a shadow is worth
    # knowing about even once the shadow can no longer reach the distance field.
    #
    # A broken key does not fail subtly: it keys the backdrop, and the figure's bounding
    # box blows out to the frame. Measured — corner-median on a diffusion backdrop gave
    # 936 x 751 in a 752 px frame, a 93% overshoot, while every correctly keyed twin sat
    # within ~1% of the mesh silhouette's own bbox.
    ys_t, xs_t = np.where(twin_fm > 0.5)
    ys_m, xs_m = np.where(mesh_fm > 0.5)
    assert len(ys_t) and len(ys_m), f"ANDON: {view['name']}: empty twin or mesh mask"
    th, tw_ = ys_t.max() - ys_t.min(), xs_t.max() - xs_t.min()
    mh, mw = ys_m.max() - ys_m.min(), xs_m.max() - xs_m.min()
    print(f"[twins] {view['name']}: twin paint bbox {th} x {tw_}  "
          f"mesh silhouette bbox {mh} x {mw}", flush=True)
    # keyed paint on no surface: the quantity the intersection removes, with its largest
    # connected component, because ONE shadow and diffuse rim speckle are different
    # failures and a total alone has to choose which one to miss.
    tb, mb = twin_fm > 0.5, mesh_fm > 0.5
    outside = tb & ~mb
    n_out = int(outside.sum())
    lab_o, n_lab = label(outside)
    cc_out = int(np.bincount(lab_o.ravel())[1:].max()) if n_lab else 0
    inter_n = int((tb & mb).sum())
    iou_tm = float(inter_n / max(int((tb | mb).sum()), 1))
    cy_t, cx_t = float(ys_t.mean()), float(xs_t.mean())
    cy_m, cx_m = float(ys_m.mean()), float(xs_m.mean())
    cdx, cdy = cx_t - cx_m, cy_t - cy_m
    print(f"[twins] {view['name']}: registration — IoU(twin,mesh) {iou_tm:.4f}  "
          f"centroid offset dx {cdx:+.1f} dy {cdy:+.1f} px "
          f"(|d| {np.hypot(cdx, cdy):.1f})", flush=True)
    # ANDON, ARMED (E08 Amendment 27) — on the direction the intersection does NOT
    # foreclose. The intersection kills "shadow paint contaminates the distance field" by
    # construction; it says nothing about a twin that is genuinely registered to the wrong
    # place. That is the live risk, and IoU against the exact silhouette measures it
    # directly rather than through a proxy: 0.80 sits 0.033 below the worst adjudicated
    # view and 0.22 above the nearest measured failure.
    #
    # ⚠ ONLY WHERE THE EXACT SILHOUETTE EXISTS. Under --mask-keyed, mesh_fm is the size-5
    # dilated sidecar — a mask that holds 76,549px of a 146,356px silhouette and scores
    # 0.6735 / 0.7001 against the twins it was shipped beside. Halting on that would be
    # halting a legacy reproduction on the wrong operand, which is the error this repo
    # keeps paying for; so the gate reports itself skipped and names why.
    if args.mask_keyed:
        print(f"[twins] {view['name']}: registration ANDON SKIPPED — --mask-keyed, so "
              f"mesh_fm is the dilated sidecar, not the exact silhouette. IoU "
              f"{iou_tm:.4f} above is against that sidecar and is NOT the gated "
              f"quantity.", flush=True)
    else:
        assert iou_tm >= args.reg_iou_min, (
            f"ANDON: {view['name']}: IoU(raw twin paint, exact silhouette) {iou_tm:.4f} "
            f"is below {args.reg_iou_min:.2f} — the twin is registered to the wrong "
            f"place. Every adjudicated view measures 0.8329 or better; every measured "
            f"registration failure sits at or below 0.578. Regenerate the twin against "
            f"this mesh's control; do not tune this threshold.")
    # NAME THE OPERAND. Under --mask-keyed this is measured against the size-5 dilated
    # SIDECAR, which on the E01-era twins holds 76,549px of a 146,356px silhouette — so
    # calling it "outside the silhouette" there would be the wrong-object error this repo
    # keeps paying for. The label says which mask the count is against.
    ref_nm = "DILATED SIDECAR" if args.mask_keyed else "silhouette"
    print(f"[twins] {view['name']}: keyed OUTSIDE the {ref_nm} {n_out:,}px  "
          f"largest component {cc_out:,}px  "
          f"({n_out / max(int(tb.sum()), 1) * 100:.2f}% of keyed paint)", flush=True)
    # ⚠ THE BBOX HALT IS DEMOTED, PERMANENTLY (E08 Amendments 26 and 27). Two reasons,
    # both measured rather than argued:
    #
    #   1. The intersection kills the pathway it was standing guard over — shadow paint can
    #      no longer reach the distance field — so halting on raw bbox extent would stop
    #      correct work, the same error A3's area-loss gate made.
    #   2. It was measuring the wrong thing. bbox extent is relative to the FIGURE'S OWN
    #      WIDTH, not to how much paint sits off-surface. Across the eight ARMB twins it
    #      fired on view 6 at a 1.921 width ratio — the 279px-wide profile — while passing
    #      views 0, 4 and 5, whose off-surface components (5,911 / 5,487 / 4,562 px) are
    #      LARGER than view 6's 4,436 px, because a 388px-wide figure hides the same band.
    #      A ratio test on a quantity that swings 1.65x with camera geometry cannot carry
    #      a halt. Fourth moving-denominator instance in this repo.
    #
    # It is kept as a printed twin-quality diagnostic: a twin that paints a shadow is worth
    # knowing about. The halt that replaced it is the registration IoU above — aimed at the
    # direction the intersection does NOT foreclose.
    #
    # Also on the record: the amendment's parenthetical for demoting — "intersection makes
    # the bbox match by construction" — is wrong as specified. The bbox is measured on
    # twin_fm, which the intersection does not touch, so it never passed by construction.
    # The demotion rests on the two reasons above.
    bbox_ok = th <= mh * (1 + args.bbox_tol) and tw_ <= mw * (1 + args.bbox_tol)
    if not bbox_ok:
        print(f"[twins] {view['name']}: NOTE (diagnostic, not a halt) — keyed twin bbox "
              f"{th}x{tw_} exceeds the mesh silhouette's {mh}x{mw} by more than "
              f"{args.bbox_tol*100:.0f}%. The twin is painting something outside the "
              f"figure's extent, most likely a cast shadow; the trust mask no longer "
              f"reads it. Gated quantity is the registration IoU above.", flush=True)
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
    # fig_w is the SECOND consumer of the trust mask, and in --edge-absolute mode it is
    # the one that spreads a local defect globally: esc scales ed_body/ed_head, so a
    # shadow that widens the keyed figure by a few percent deepens the erosion over the
    # WHOLE twin, not just near the shadow. Both widths are printed so the difference is
    # visible rather than inferred.
    fx = np.where((fm > 0.5).any(axis=0))[0]
    fig_w = float(fx.max() - fx.min()) if len(fx) else float(W)
    fx_raw = np.where(tb.any(axis=0))[0]
    fig_w_raw = float(fx_raw.max() - fx_raw.min()) if len(fx_raw) else float(W)
    print(f"[twins] {view['name']}: fig_w raw {fig_w_raw:.0f}px  used {fig_w:.0f}px  "
          f"(trust mask {int((fm > 0.5).sum()):,}px of raw {int(tb.sum()):,}px)",
          flush=True)
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
    if args.diag_npz is not None:
        # captured HERE because the next line rebinds idx/px/py. Nothing is read back
        # into the computation — this exists so a gain/loss decomposition can be done
        # offline against the other arm instead of re-deriving it from an atlas.
        DIAG[view["name"]] = {
            "cand_idx": idx.astype(np.int64),
            "px": px.astype(np.float32),
            "py": py.astype(np.float32),
            "d_s": d_s.astype(np.float32),
            "ed": np.asarray(ed, dtype=np.float32),
            "thick_s": bilinear(thick, px, py).astype(np.float32),
            "mask_ok": (bilinear(mesh_fm[..., None], px, py)[:, 0] > 0.5),
            "accepted": inm.astype(bool),
            "dist_in": dist_in,
            "mesh_fm": (mesh_fm > 0.5),
            "twin_fm": tb,
            "fig_w": np.float32(fig_w),
            "fig_w_raw": np.float32(fig_w_raw),
            "bbox_twin": np.array([th, tw_], dtype=np.int64),
            "bbox_mesh": np.array([mh, mw], dtype=np.int64),
            "iou_tm": np.float32(iou_tm),
            "centroid_off": np.array([cdx, cdy], dtype=np.float32),
            "outside_px": np.int64(n_out),
            "outside_cc": np.int64(cc_out),
        }
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
    owner_i[idx[take]] = _view_i
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

# THE TWO SIDECARS (E04 Ruling 2). Both objects already exist above; both were discarded.
#   _owner.npy  which VIEW won each texel, int8, -1 where nothing styled it. This is the
#               partition the crown seam lives on, and E04 Task 1 had to rebuild it from
#               diag_8cam's accepted sets to find that seam at all.
#   _blend.png  B, the facing-weighted blend of every view that accepted the texel. The
#               difference between it and the ownership map M is exactly what the sigma=16
#               levelling corrects at low frequency - so "why did levelling not touch a
#               dE 13 step" is answerable from disk instead of by re-deriving it.
# Written AFTER the atlas, from copies, touching nothing the atlas is built from. An
# additive sidecar that moves an atlas byte is not a sidecar; the E04 gate tests exactly
# that by re-running the eight-camera anchor for pixel-identity.
_owner_grid = np.full(RES * RES, -1, dtype=np.int8)
_owner_grid[np.where(valid)[0]] = owner_i
np.save(args.out.replace(".png", "_owner.npy"), _owner_grid.reshape(RES, RES))
Image.fromarray((np.clip(B, 0, 1) * 255).round().astype(np.uint8)).save(
    args.out.replace(".png", "_blend.png"))
print(f"[twins] wrote {args.out} + _holes.png + _styled_mask.npy "
      f"+ _owner.npy + _blend.png — DONE", flush=True)

if args.diag_npz is not None:
    os.makedirs(os.path.dirname(os.path.abspath(args.diag_npz)), exist_ok=True)
    flat = {"__views__": np.array([v["name"] for v in VIEWS]),
            "__trust_intersect__": np.bool_(args.trust_intersect),
            "__styled__": seen, "__reachable__": reachable,
            "__valid__": np.int64(NV), "__variance__": np.float32(var),
            "__holes__": np.int64(int(hole.sum()))}
    for nm, d in DIAG.items():
        for k, arr in d.items():
            flat[f"{nm}/{k}"] = arr
    np.savez_compressed(args.diag_npz, **flat)
    print(f"[twins] wrote {args.diag_npz} (per-view acceptance internals)", flush=True)
