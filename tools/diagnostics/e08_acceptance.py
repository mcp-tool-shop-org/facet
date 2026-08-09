"""E08 Arm A — what does each acceptance test actually cost?

Gate 0 measured that the twins style 681,212 of the 1,265,391 texels their cameras can
physically reach: the acceptance stage discards 46.2% of reachable surface. Three tests
are fused in one line of project_twins and nobody has separated them:

  FACING   facing > 0.45 body / 0.18 head          (line 185, absolute, before ownership)
  EDGE     distance into the TWIN's figure mask >= scaled edge-dist   (line 215)
  MASK     inside the saved MESH silhouette mask                      (line 215)

This reports each one's cost in texels, per view and unioned, plus coverage as a function
of the facing floor. Pure geometry and image lookups — no diffusion, no GPU, and it writes
no atlas.

It also tests the reorder premise by construction rather than by argument. The ruling says
the absolute gate at 185 runs before the comparative ownership rule at 222, so "a texel seen
obliquely by every camera gets discarded by all of them instead of assigned to the one that
sees it best." Whether that costs anything depends on something checkable: project_twins
accumulates each view's accepted set independently and takes `w > best_w`, so a texel the
best view rejects can already be supplied by a worse one. If that is so, reordering at fixed
floor is a NO-OP and the only lever in it is the floor itself — which matters, because
lowering the floor to 0.10 was already falsified by the Director (streak bands on skull
sides and sword, 2026-08-04).

  e08_acceptance.py --prep DIR --front f.png --back b.png [--floors 0.45,0.35,...]

Verification anchor: at the production floors the styled count must reproduce 681,212,
E06's measured TWINS provenance. The tool asserts it.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import distance_transform_edt, maximum_filter, minimum_filter

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--front", required=True)
ap.add_argument("--back", required=True)
ap.add_argument("--floors", default="0.45,0.35,0.25,0.18,0.10,0.05")
ap.add_argument("--head-facing-min", type=float, default=0.18)
ap.add_argument("--edge-dist", type=float, default=7.0)
ap.add_argument("--head-edge-dist", type=float, default=3.0)
ap.add_argument("--edge-ref", type=float, default=700.0)
ap.add_argument("--edge-floor", type=float, default=2.5)
ap.add_argument("--bias", type=float, default=3e-3)
ap.add_argument("--noffs", type=float, default=1.5e-3)
ap.add_argument("--aspect", default="752,1024")
ap.add_argument("--expect-styled", type=int, default=681212)
# ⚠ EXPLICIT MASK PATHS (E08 Amendment 27 §7). The derived path — the twin's own stem plus
# "_mask.png" — cannot reach the ARMB layout at all: there, `twin_0.png` sits beside
# `w3clay_0_mask.png`, so the derivation looks for a `twin_0_mask.png` that does not exist.
# An override is the whole fix; a stem-rewriting convention would be one more thing to get
# subtly wrong.
ap.add_argument("--front-mask", help="exact silhouette for the front view; overrides the "
                                    "derived <twin stem>_mask.png")
ap.add_argument("--back-mask", help="exact silhouette for the back view; same")
ap.add_argument("--trust-intersect", action="store_true",
                help="E08 Amendment 26, mirrored from project_twins so the instrument "
                     "and the pipeline share the operand: the TRUST mask (fm) is "
                     "intersected with the UNDILATED sidecar silhouette before the "
                     "distance transform and before fig_w. The size-5 maximum_filter "
                     "below stays where it is — it is mask_ok's sampling tolerance, a "
                     "different question. WARNING: With this on, --expect-styled cannot apply: "
                     "the anchor pins the HISTORICAL acceptance, and this deliberately "
                     "changes it. The assert is scoped to the flag being off rather "
                     "than re-derived, since re-deriving an anchor while looking at the "
                     "output it would judge is how the last three thresholds went "
                     "wrong.")
ap.add_argument("--sheet", help="look at what is being rejected, before theorising")
ap.add_argument("--out-json")
args = ap.parse_args()
AW, AH = [float(x) for x in args.aspect.split(",")]

meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
mask = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
lo = np.array(meta["lo"], dtype=np.float64)
hi = np.array(meta["hi"], dtype=np.float64)
valid = mask.reshape(-1)
P = (np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3)[valid].astype(np.float64)
     * (hi - lo) + lo) / meta["maxabs"] * 0.5
N = np.load(os.path.join(args.prep, "nor.npy")).reshape(-1, 3)[valid].astype(np.float64) \
    * 2.0 - 1.0
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
NV = P.shape[0]
CX0, CY0, CX1, CY1 = meta["crop"]
b_std = 0.55
px1k = (P[:, 0] + b_std) / (2 * b_std) * meta["crop_res"]
py1k = (b_std - P[:, 2]) / (2 * b_std) * meta["crop_res"]
headband = ((px1k >= CX0) & (px1k <= CX1) & (py1k >= CY0) & (py1k <= CY1))

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
up = np.array([0.0, 0.0, 1.0])


def figure_mask(img, tol=0.06, erode=5):
    """⚠ CORNER-MEDIAN, DELIBERATELY. This instrument's --expect-styled anchor pins the
    HISTORICAL acceptance, and that history ran on this key; porting the fitted estimator
    in would silently retire the anchor. So the key stays, and a guard below refuses to
    report numbers when it has failed — see keyed_bbox_guard.

    Corner-median keying is retired for the ROUTE (project_twins uses the fitted
    estimator). It survives here as the object being reproduced, not as a recommendation.
    """
    c = np.concatenate([img[:8, :8].reshape(-1, 3), img[:8, -8:].reshape(-1, 3)])
    bg = np.median(c, axis=0)
    return minimum_filter((np.abs(img - bg).max(axis=-1) > tol).astype(np.float32), size=erode)


def keyed_bbox_guard(name, twin_fm, sil, tol=0.25):
    """Bbox-check a keyed mask against the geometry before reading a number from it.

    The repo's standing rule, and this instrument did not have it. Found by running
    Amendment 27 step 3: pointed at the ARMB twins, the corner-median key above returns
    465,363 px — 60.4% of frame against a 19.01% truth — because a diffusion model paints
    a lit studio backdrop and a single corner sample is the wrong model for it. That is the
    documented 31-76% failure, and without this guard the instrument reported 1,063,039
    styled texels off it, a number that measures the key's collapse and nothing else.

    The guard is on the KEY. The Amendment-27 guard added below is on the SILHOUETTE. Two
    operands, two checks; verifying one says nothing about the other.
    """
    ys_t, xs_t = np.where(twin_fm > 0.5)
    ys_m, xs_m = np.where(sil)
    if not (len(ys_t) and len(ys_m)):
        raise AssertionError(f"ANDON: {name}: empty keyed or silhouette mask")
    th, tw = ys_t.max() - ys_t.min(), xs_t.max() - xs_t.min()
    mh, mw = ys_m.max() - ys_m.min(), xs_m.max() - xs_m.min()
    if not (th <= mh * (1 + tol) and tw <= mw * (1 + tol)):
        raise AssertionError(
            f"ANDON: {name}: the corner-median key's bbox {th}x{tw} exceeds the mesh "
            f"silhouette's {mh}x{mw} by more than {tol*100:.0f}% — it has keyed the backdrop, "
            f"not the figure ({twin_fm.mean()*100:.1f}% of frame against the silhouette's "
            f"{sil.mean()*100:.1f}%). This instrument keys with a corner median to reproduce "
            f"its own anchor, and corner-median keying fails on any non-flat backdrop. Nothing "
            f"it reports on this twin would mean anything; use project_twins, whose key is the "
            f"fitted estimator.")


def bilinear(img, x, y):
    H, W = img.shape[:2]
    x = np.clip(x, 0.0, W - 1.001); y = np.clip(y, 0.0, H - 1.001)
    x0, y0 = x.astype(np.int64), y.astype(np.int64)
    fx, fy = (x - x0)[:, None], (y - y0)[:, None]
    a, b_, c, d = img[y0, x0], img[y0, x0 + 1], img[y0 + 1, x0], img[y0 + 1, x0 + 1]
    if a.ndim == 1:
        fx, fy = fx[:, 0], fy[:, 0]
    return a * (1 - fx) * (1 - fy) + b_ * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy


VIEWS = [{"name": "front", "path": args.front, "dtc": np.array([0.0, -1.0, 0.0]),
          "right": np.array([1.0, 0.0, 0.0]), "mask": args.front_mask},
         {"name": "back", "path": args.back, "dtc": np.array([0.0, 1.0, 0.0]),
          "right": np.array([-1.0, 0.0, 0.0]), "mask": args.back_mask}]


def live_silhouette(view):
    """The exact silhouette by raycast, project_twins' construction. The authoritative
    answer to 'is there surface here' (A2), and the object --trust-intersect must use."""
    dtc = view["dtc"]
    look, rgt = -dtc, view["right"]
    upv = np.cross(rgt, look)
    upv = upv / np.linalg.norm(upv)
    Wi, Hi = int(AW), int(AH)
    xs2 = (np.arange(Wi) + 0.5) / Wi * h_ext - h_ext / 2
    ys2 = v_ext / 2 - (np.arange(Hi) + 0.5) / Hi * v_ext
    g1, g2 = np.meshgrid(xs2, ys2)
    o2 = (bmid[None, None, :] + g1[..., None] * rgt[None, None, :]
          + g2[..., None] * upv[None, None, :] - look[None, None, :] * 2.0)
    return np.isfinite(rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [o2, np.broadcast_to(look, o2.shape)], axis=-1
    ).reshape(-1, 6).astype(np.float32)))["t_hit"].numpy().reshape(Hi, Wi))


if not args.trust_intersect:
    # ASCII only in prints: U+26A0 is not in cp1252 and raises UnicodeEncodeError on a
    # Windows console. Comments and docstrings never reach stdout, so they keep the glyph.
    print("[acc] !! MEASURING THE PRE-ADOPTION OPERAND. The route default is now "
          "trust-intersect ON (E08 Amendment 27); this run has it off, which is what the "
          f"--expect-styled {args.expect_styled:,} anchor pins. Do not read these numbers "
          "as the route's current behaviour.", flush=True)

st = {}
for view in VIEWS:
    img = np.asarray(Image.open(view["path"]).convert("RGB"), dtype=np.float32) / 255.0
    twin_fm = figure_mask(img)
    mp = view["mask"] or os.path.splitext(view["path"])[0] + "_mask.png"
    if not (os.path.exists(mp)):
        raise AssertionError(
            f"ANDON: no silhouette at {mp}. Pass --{view['name']}-mask explicitly — the "
            f"derived <twin stem>_mask.png does not exist in every twin layout.")
    rawm = (np.asarray(Image.open(mp).convert("L"), dtype=np.float32) / 255.0 > 0.5)
    mesh_fm = maximum_filter(rawm.astype(np.float32), size=5)
    # THE KEY's guard, before anything is computed off it. Against the LIVE silhouette
    # rather than the sidecar, so a broken sidecar cannot excuse a broken key.
    keyed_bbox_guard(view["name"], twin_fm, live_silhouette(view))
    # THE TRUST OPERAND, mirrored from project_twins (E08 Amendment 26). Intersected with
    # the UNDILATED sidecar, not with mesh_fm: the size-5 dilation is a sampling tolerance
    # for mask_ok and would admit a 2px collar of non-surface back into the trust mask.
    if args.trust_intersect:
        # ANDON (E08 Amendment 27 §7): the sidecar must BE the exact silhouette, not merely
        # be named like one. Intersecting an E01-era keyed clay mask measured -388,764
        # styled texels — a measurement of a broken mask, not of the intersection. The
        # authoritative object is the raycast, so verify against it rather than trust the
        # filename. Eliminating the hazard, not documenting it.
        sil = live_silhouette(view)
        nd = int((sil != rawm).sum())
        if not (nd == 0):
            raise AssertionError(
                f"ANDON: {view['name']}: the sidecar {os.path.basename(mp)} differs from the "
                f"live raycast silhouette by {nd:,} px ({int(rawm.sum()):,} vs "
                f"{int(sil.sum()):,}) — it is NOT the exact silhouette, so intersecting with "
                f"it measures the sidecar's defect. E01-era masks score IoU 0.523/0.578 here. "
                f"Point --{view['name']}-mask at an exact silhouette (silhouette_masks.py "
                f"writes them; silhouette_agree.py checks them).")
        print(f"[acc] {view['name']}: sidecar == live raycast silhouette, 0 differing px "
              f"({int(sil.sum()):,}px)", flush=True)
        fm = (twin_fm > 0.5) & rawm
        print(f"[acc] {view['name']}: TRUST INTERSECT — keyed paint "
              f"{int((twin_fm > 0.5).sum()):,}px -> trust {int(fm.sum()):,}px "
              f"(outside the undilated silhouette: "
              f"{int(((twin_fm > 0.5) & ~rawm).sum()):,}px)", flush=True)
        fm = fm.astype(np.float32)
    else:
        fm = twin_fm
    H, W = img.shape[:2]
    dtc = view["dtc"]
    facing = (N @ dtc).astype(np.float64)
    # visibility for every FRONT-FACING texel, so a lower floor can be evaluated
    # without re-raycasting; project_twins only casts the facing-passing set
    cand = np.where(facing > 0.0)[0]
    org = (P[cand] + N[cand] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
    t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(dtc.astype(np.float32), org.shape)], axis=1)))["t_hit"].numpy()
    vis = np.zeros(NV, dtype=bool)
    vis[cand[~np.isfinite(t)]] = True
    xr = (P @ view["right"]) - (bmid @ view["right"])
    zu = (P @ up) - (bmid @ up)
    px = (xr / h_ext + 0.5) * W - 0.5
    py = (0.5 - zu / v_ext) * H - 0.5
    dist_in = distance_transform_edt(fm > 0.5).astype(np.float32)
    fx = np.where((fm > 0.5).any(axis=0))[0]
    fig_w = float(fx.max() - fx.min()) if len(fx) else float(W)
    esc = fig_w / args.edge_ref
    ed = np.where(headband, max(args.edge_floor, args.head_edge_dist * esc),
                  max(args.edge_floor, args.edge_dist * esc))
    edge_ok = bilinear(dist_in, px, py) >= ed
    mask_ok = bilinear(mesh_fm[..., None], px, py)[:, 0] > 0.5
    st[view["name"]] = {"facing": facing, "vis": vis, "edge": edge_ok, "mask": mask_ok,
                        "px": px, "py": py, "img": img, "mesh_fm": mesh_fm,
                        "raw_mask": rawm}
    print(f"[acc] {view['name']}: figure {fig_w:.0f}px wide, edge-dist "
          f"{max(args.edge_floor, args.edge_dist*esc):.1f}px body / "
          f"{max(args.edge_floor, args.head_edge_dist*esc):.1f}px head", flush=True)

out = {"valid": int(NV), "floors": {}}


def fmin_arr(body):
    return np.where(headband, args.head_facing_min, body)


def accepted(name, body):
    s = st[name]
    return (s["facing"] > fmin_arr(body)) & s["vis"] & s["edge"] & s["mask"]


def reachable(name, body):
    s = st[name]
    return (s["facing"] > fmin_arr(body)) & s["vis"]


# ---- production floors: separate the three costs
BODY = 0.45
print(f"\n[acc] PRODUCTION floors (body {BODY} / head {args.head_facing_min}) — "
      f"what each test costs")
R = np.zeros(NV, dtype=bool)
A = np.zeros(NV, dtype=bool)
per = {}
for view in VIEWS:
    n = view["name"]
    s = st[n]
    r = reachable(n, BODY)
    a = accepted(n, BODY)
    e_fail = r & ~s["edge"]
    m_fail = r & ~s["mask"]
    per[n] = {"reachable": int(r.sum()), "accepted": int(a.sum()),
              "edge_fail": int(e_fail.sum()), "mask_fail": int(m_fail.sum()),
              "edge_only": int((e_fail & ~m_fail).sum()),
              "mask_only": int((m_fail & ~e_fail).sum()),
              "both": int((e_fail & m_fail).sum())}
    print(f"[acc]   {n}: reachable {int(r.sum()):>9,}  accepted {int(a.sum()):>9,}  "
          f"lost {int((r & ~a).sum()):>9,} ({(r&~a).sum()/max(int(r.sum()),1)*100:.1f}%)")
    print(f"[acc]       EDGE only {int((e_fail & ~m_fail).sum()):>9,}   "
          f"MASK only {int((m_fail & ~e_fail).sum()):>8,}   "
          f"both {int((e_fail & m_fail).sum()):>8,}")
    R |= r
    A |= a
out["per_view_production"] = per
lost = R & ~A
print(f"[acc]   UNION: reachable {int(R.sum()):,}  styled {int(A.sum()):,}  "
      f"lost {int(lost.sum()):,} = {lost.sum()/max(int(R.sum()),1)*100:.1f}% of reachable")
out["union_production"] = {"reachable": int(R.sum()), "styled": int(A.sum()),
                           "lost": int(lost.sum())}
if args.trust_intersect:
    print(f"[acc]   anchor NOT APPLICABLE under --trust-intersect: it pins the "
          f"HISTORICAL acceptance ({args.expect_styled:,}) and this run changes the "
          f"trust operand on purpose. Delta {int(A.sum()) - args.expect_styled:+,}.")
else:
    if not (abs(int(A.sum()) - args.expect_styled) <= 2):
        raise AssertionError(
            f"ANDON: styled {int(A.sum()):,} does not reproduce E06's measured TWINS "
            f"{args.expect_styled:,} — the replica of project_twins' acceptance is wrong")
    print(f"[acc]   anchor OK: styled reproduces E06's TWINS provenance "
          f"({args.expect_styled:,})")

# ---- counterfactual: drop one test at a time, production floors
print(f"\n[acc] counterfactual coverage, production floors, one test removed at a time")
combos = {"as shipped": ("edge", "mask"), "no EDGE test": ("mask",),
          "no MASK test": ("edge",), "neither test": ()}
cf = {}
for lab, keep in combos.items():
    U = np.zeros(NV, dtype=bool)
    for view in VIEWS:
        s = st[view["name"]]
        a = reachable(view["name"], BODY)
        for k in keep:
            a = a & s[k]
        U |= a
    cf[lab] = {"styled": int(U.sum()), "pct_of_valid": round(float(U.mean() * 100), 2)}
    print(f"[acc]   {lab:<14s} styled {int(U.sum()):>9,}  {U.mean()*100:5.2f}% of valid "
          f"({int(U.sum())-int(A.sum()):+,} vs shipped)")
out["counterfactual_production"] = cf

# ---- the facing floor ladder, with edge+mask still applied
print(f"\n[acc] facing floor ladder (head stays {args.head_facing_min}, edge+mask applied)")
lad = {}
for t in [float(x) for x in args.floors.split(",")]:
    U = np.zeros(NV, dtype=bool)
    Rr = np.zeros(NV, dtype=bool)
    for view in VIEWS:
        U |= accepted(view["name"], t)
        Rr |= reachable(view["name"], t)
    lad[f"{t}"] = {"reachable": int(Rr.sum()), "styled": int(U.sum()),
                   "styled_pct": round(float(U.mean() * 100), 2),
                   "acceptance_rate": round(float(U.sum() / max(int(Rr.sum()), 1) * 100), 1)}
    print(f"[acc]   floor {t:<5} reachable {int(Rr.sum()):>9,}  styled {int(U.sum()):>9,}  "
          f"{U.mean()*100:5.2f}% of valid   acceptance {U.sum()/max(int(Rr.sum()),1)*100:5.1f}%")
out["floor_ladder"] = lad

# ---- the reorder premise, tested by construction
print(f"\n[acc] REORDER premise: does comparative ownership differ from the absolute gate?")
print(f"[acc]   comparative = assign each texel to the view with the highest facing")
print(f"[acc]                 among views that see it and pass edge+mask, floor applied last")
same_all = True
for t in [0.45, 0.25, 0.10]:
    absU = np.zeros(NV, dtype=bool)
    for view in VIEWS:
        absU |= accepted(view["name"], t)
    best = np.full(NV, -np.inf)
    win = np.zeros(NV, dtype=bool)
    for view in VIEWS:
        s = st[view["name"]]
        elig = s["vis"] & s["edge"] & s["mask"] & (s["facing"] > fmin_arr(t))
        better = elig & (s["facing"] > best)
        best[better] = s["facing"][better]
        win |= elig
    ident = bool((absU == win).all())
    same_all &= ident
    print(f"[acc]   floor {t}: absolute {int(absU.sum()):>9,}   comparative "
          f"{int(win.sum()):>9,}   identical: {ident}")
out["reorder_identical"] = bool(same_all)

# ---- LOOK at what is being rejected, before theorising about it (CLAUDE.md, 2026-08-05)
if args.sheet:
    panels = []
    for view in VIEWS:
        n = view["name"]
        s = st[n]
        H, W = s["img"].shape[:2]
        base = (s["img"] * 255).astype(np.uint8)
        # the saved mask as-is against its opened form: min-then-max is an OPENING,
        # not an identity, so anything narrower than the kernel never comes back
        rawm = s["raw_mask"]
        opened = s["mesh_fm"] > 0.5
        cmp_ = np.zeros((H, W, 3), dtype=np.uint8)
        cmp_[rawm] = (90, 90, 96)
        cmp_[opened & ~rawm] = (70, 160, 220)      # restored by the un-erode
        cmp_[rawm & ~opened] = (240, 70, 60)       # LOST to the opening, never restored
        r = reachable(n, BODY)
        lay = base.copy()
        pxi = np.clip(s["px"].round().astype(int), 0, W - 1)
        pyi = np.clip(s["py"].round().astype(int), 0, H - 1)
        acc_i = r & s["edge"] & s["mask"]
        edge_i = r & ~s["edge"]
        mask_i = r & ~s["mask"]
        lay[pyi[acc_i], pxi[acc_i]] = (40, 200, 90)
        lay[pyi[edge_i], pxi[edge_i]] = (60, 130, 240)
        lay[pyi[mask_i], pxi[mask_i]] = (240, 60, 50)
        panels += [base, cmp_, lay]
    sheet = np.concatenate(panels, axis=1)
    os.makedirs(os.path.dirname(os.path.abspath(args.sheet)), exist_ok=True)
    Image.fromarray(sheet).save(args.sheet)
    print(f"\n[acc] wrote {args.sheet}")
    print(f"[acc]   per view: twin | mask (grey=kept, RED=lost to the opening, "
          f"blue=restored) | rejections (green=accepted, blue=EDGE, RED=MASK)")
    # The MASK test's premise is that the saved mask IS the mesh silhouette. That is
    # checkable against the silhouette itself, which the raycasting scene already
    # built. (An earlier version of this check compared the saved mask against its own
    # dilation, which cannot lose a pixel by construction and always returned 0 — a
    # guard that could not see its own failure.)
    print(f"\n[acc] is the saved mask actually the mesh silhouette?")
    for view in VIEWS:
        n = view["name"]
        s = st[n]
        dtc = view["dtc"]
        look, rgt = -dtc, view["right"]
        upv = np.cross(rgt, look); upv = upv / np.linalg.norm(upv)
        Wi, Hi = int(AW), int(AH)
        xs2 = (np.arange(Wi) + 0.5) / Wi * h_ext - h_ext / 2
        ys2 = v_ext / 2 - (np.arange(Hi) + 0.5) / Hi * v_ext
        g1, g2 = np.meshgrid(xs2, ys2)
        o2 = (bmid[None, None, :] + g1[..., None] * rgt[None, None, :]
              + g2[..., None] * upv[None, None, :] - look[None, None, :] * 2.0)
        sil = np.isfinite(rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [o2, np.broadcast_to(look, o2.shape)], axis=-1
        ).reshape(-1, 6).astype(np.float32)))["t_hit"].numpy().reshape(Hi, Wi))
        used = s["mesh_fm"] > 0.5
        out.setdefault("mask_vs_silhouette", {})[n] = {
            "true_silhouette_px": int(sil.sum()),
            "mask_used_px": int(used.sum()),
            "mesh_outside_mask_px": int((sil & ~used).sum()),
            "mask_outside_mesh_px": int((used & ~sil).sum()),
            "iou": round(float((sil & used).sum() / max((sil | used).sum(), 1)), 4)}
        print(f"[acc]   {n}: true silhouette {int(sil.sum()):>8,}px   mask used "
              f"{int(used.sum()):>8,}px   IoU {(sil&used).sum()/max((sil|used).sum(),1):.4f}")
        print(f"[acc]       mesh NOT in the mask {int((sil & ~used).sum()):>8,}px   "
              f"mask not on the mesh {int((used & ~sil).sum()):>6,}px")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[acc] wrote {args.out_json}")
