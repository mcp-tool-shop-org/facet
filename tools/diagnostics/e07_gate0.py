"""E07 Gate 0 — test both premises before either fix is built. No GPU, no brush.

Three measurements, none of which changes anything:

  A  Does colour actually cross the gutter?  Replays texpass_finalize's flood EXACTLY
     as written — including the missing `& valid` on the write predicate — but carries
     a source-island label and a gutter flag beside the front instead of a colour.
     Answers: what share of dilated texels took their colour from a DIFFERENT island,
     and what share of those paths ran through an invalid gutter texel.
     Also runs the island-constrained variant for contrast; it changes nothing on disk.

  B  Is there a step to level?  The cross-provenance step ratio on the finished C1
     head render, from the claim map texel_provenance.py already wrote.
     median|dL| across a provenance boundary / median|dL| within one provenance.
     1.0 = a boundary is indistinguishable from ordinary texture variation.
     Two controls ship with it, chosen before the number was seen: the same ratio
     across ISLAND boundaries at equal provenance (surface structure with no
     provenance step in it), and a per-provenance-pair breakdown.

  C  Fact 3, measured and changed nowhere.  What fraction of a sigma=16 atlas-space
     Gaussian's covered weight falls on a DIFFERENT island, at a styled texel.
     This is stage 1's levelling kernel. Information E08 needs; not an arm here.

Island partition is union-find over welded UV corners and texel->island by closest-point
query against the baked positions — the same construction texpass_metrics.py uses, so
island counts here mean what they mean there.

  e07_gate0.py --prep DIR --state DIR --stage1 styled_stage1.png --render head.png
               [--parts ABC] [--out-json g0.json] [--cache DIR]

Standards compliance: PIN_PER_STEP — every path is a parameter and nothing is written
back to the arm. ANDON_AUTHORITY — the two premise halts live in the caller; this tool
reports numbers and does not rule on them. EXTERNAL_VERIFIER — measures, never judges.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import median_filter

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--prep", required=True)
ap.add_argument("--state", required=True)
ap.add_argument("--stage1", required=True, help="stage-1 atlas; _styled_mask.npy beside it")
ap.add_argument("--render", help="head render matching texel_provenance's camera (part B)")
ap.add_argument("--parts", default="ABC")
ap.add_argument("--sigma", type=float, default=16.0, help="part C: stage-1 levelling sigma")
ap.add_argument("--samples", type=int, default=8000, help="part C: styled texels sampled")
ap.add_argument("--seed", type=int, default=770700)
ap.add_argument("--head-crop", default="360,240,700,600")
ap.add_argument("--crop-res", type=int, default=1024)
ap.add_argument("--bound", type=float, default=0.55)
ap.add_argument("--pad", type=float, default=1.25)
ap.add_argument("--res", type=int, default=1024)
ap.add_argument("--blotch", type=float, default=0.10)
ap.add_argument("--cache", help="dir to cache the texel->island map (expensive to build)")
ap.add_argument("--out-json")
args = ap.parse_args()

out = {}
meta = json.load(open(os.path.join(args.prep, "meta.json")))
RES = meta["res"]
valid = np.load(os.path.join(args.prep, "mask.npy"))[..., 0] > 0.5
holes = np.asarray(Image.open(os.path.join(args.state, "holes.png")).convert("L")) > 127

m = trimesh.load(os.path.join(args.prep, "prep_uv.glb"), force="mesh", process=False)
v = np.asarray(m.vertices, dtype=np.float64)
f = np.asarray(m.faces, dtype=np.int64)
uv = np.asarray(m.visual.uv, dtype=np.float64)
nf = len(f)
vz = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
rs = o3d.t.geometry.RaycastingScene()
rs.add_triangles(o3d.core.Tensor(vz.astype(np.float32)),
                 o3d.core.Tensor(f.astype(np.uint32)))


# ---------------------------------------------------------------- island partition
def build_islands():
    """union-find over welded UV corners — bake_hero_prep / texpass_metrics construction"""
    lvert = f.reshape(-1)
    luv = uv[f].reshape(-1, 2)
    key = (lvert.astype(np.int64) << 44) \
          ^ ((luv[:, 0] * 5e5).round().astype(np.int64) << 22) \
          ^ (luv[:, 1] * 5e5).round().astype(np.int64)
    loop_face = np.repeat(np.arange(nf, dtype=np.int64), 3)
    order = np.argsort(key, kind="stable")
    parent = np.arange(nf, dtype=np.int64)

    def find(i):
        root = i
        while parent[root] != root:
            root = parent[root]
        while parent[i] != root:
            parent[i], i = root, parent[i]
        return root

    sk, sf = key[order], loop_face[order]
    run = 0
    for j in range(1, len(sk) + 1):
        if j == len(sk) or sk[j] != sk[run]:
            if j - run > 1:
                r0 = find(sf[run])
                for t in range(run + 1, j):
                    r = find(sf[t])
                    if r != r0:
                        parent[r] = r0
            run = j
    roots = np.array([find(i) for i in range(nf)], dtype=np.int64)
    uniq, face_island = np.unique(roots, return_inverse=True)
    return len(uniq), face_island


cache_f = os.path.join(args.cache, "isl_grid.npy") if args.cache else None
if cache_f and os.path.exists(cache_f):
    isl = np.load(cache_f)
    n_isl = int(isl.max()) + 1
    print(f"[g0] island grid from cache: {n_isl:,} islands", flush=True)
else:
    n_isl, face_island = build_islands()
    lo = np.array(meta["lo"]); hi = np.array(meta["hi"])
    vflat = valid.reshape(-1)
    P = (np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3)[vflat].astype(np.float64)
         * (hi - lo) + lo) / meta["maxabs"] * 0.5
    prim = np.empty(len(P), dtype=np.int64)
    CH = 1_000_000
    for s in range(0, len(P), CH):
        e = min(s + CH, len(P))
        prim[s:e] = rs.compute_closest_points(o3d.core.Tensor(
            P[s:e].astype(np.float32)))["primitive_ids"].numpy().astype(np.int64)
    isl = np.full(RES * RES, -1, dtype=np.int32)
    isl[np.where(vflat)[0]] = face_island[prim].astype(np.int32)
    isl = isl.reshape(RES, RES)
    if cache_f:
        os.makedirs(args.cache, exist_ok=True)
        np.save(cache_f, isl)
    print(f"[g0] islands {n_isl:,}  faces/island {nf/n_isl:.1f}  "
          f"valid texels {int(valid.sum()):,}", flush=True)
out["islands"] = int(n_isl)
out["valid_texels"] = int(valid.sum())
out["dilated_texels"] = int((valid & holes).sum())


# ------------------------------------------------------- A: does colour cross the gutter
def flood(constrain_to_valid):
    """texpass_finalize.py's flood, carrying a source label instead of a colour.

    constrain_to_valid=False reproduces the shipped code EXACTLY (line 43,
    `fill = ~grown & (cnt > 0)` with no `& valid`). True is the counterfactual.
    """
    have = valid & ~holes
    grown = have.copy()
    src = np.full((RES, RES), -1, dtype=np.int32)
    src[have] = isl[have]
    # the originating painted TEXEL, so the source can be asked how far away it is on
    # the actual surface. "different island" is a label question; two charts meeting at
    # a UV seam are surface-CONTINUOUS, and colour crossing that is not the defect.
    src_i = np.full((RES, RES), -1, dtype=np.int32)
    src_i[have] = np.flatnonzero(have.reshape(-1)).astype(np.int32)
    via = np.zeros((RES, RES), dtype=bool)
    step_a = np.zeros((RES, RES), dtype=np.int32)
    SENT = np.int32(2 ** 31 - 1)
    K = np.int32(20000)
    for step in range(96):
        todo = valid & ~grown
        if not todo.any() and step >= 16:
            break
        cnt = np.zeros((RES, RES), dtype=np.int8)
        best_key = np.full((RES, RES), SENT, dtype=np.int32)
        best_src = np.full((RES, RES), -1, dtype=np.int32)
        best_si = np.full((RES, RES), -1, dtype=np.int32)
        best_via = np.zeros((RES, RES), dtype=bool)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb_g = np.roll(grown, (dy, dx), axis=(0, 1))
            nb_s = np.roll(src, (dy, dx), axis=(0, 1))
            nb_t = np.roll(step_a, (dy, dx), axis=(0, 1))
            nb_v = np.roll(via, (dy, dx), axis=(0, 1))
            nb_ok = np.roll(valid, (dy, dx), axis=(0, 1))
            nb_i = np.roll(src_i, (dy, dx), axis=(0, 1))
            cnt += nb_g
            key = np.where(nb_g, nb_t * K + (nb_s + 2), SENT).astype(np.int32)
            take = key < best_key
            best_key = np.where(take, key, best_key)
            best_src = np.where(take, nb_s, best_src)
            best_si = np.where(take, nb_i, best_si)
            best_via = np.where(take, nb_v | ~nb_ok, best_via)
        fill = ~grown & (cnt > 0)
        if constrain_to_valid:
            fill &= valid
        src[fill] = best_src[fill]
        src_i[fill] = best_si[fill]
        via[fill] = best_via[fill]
        step_a[fill] = step + 1
        grown |= fill
    return src, via, grown, step_a, src_i


if "A" in args.parts:
    # world-space position of every texel, for the "how far away is the source" question
    lo_p = np.array(meta["lo"]); hi_p = np.array(meta["hi"])
    POS = (np.load(os.path.join(args.prep, "pos.npy")).reshape(-1, 3).astype(np.float64)
           * (hi_p - lo_p) + lo_p) / meta["maxabs"] * 0.5
    tri = vz[f]
    edge_med = float(np.median(np.linalg.norm(tri[:, 1] - tri[:, 0], axis=1)))
    texel_sp = float(np.sqrt(((hi_p - lo_p) / meta["maxabs"] * 0.5).prod() ** (2 / 3)
                             / max(int(valid.sum()), 1)))
    out["A_median_edge_len"] = round(edge_med, 6)
    print(f"\n[g0-A] scale reference: median triangle edge {edge_med:.5f} "
          f"(figure ~1.0 tall)", flush=True)

    print("[g0-A] replaying the SHIPPED flood (no `& valid` on the write)", flush=True)
    src, via, grown, step_a, src_i = flood(False)
    D = valid & holes                          # the dilated set
    nD = int(D.sum())
    reached = D & (src >= 0)
    cross = reached & (src != isl)
    gut = reached & via
    unreached = int((D & ~grown).sum())
    out["A_dilated"] = nD
    out["A_mean_fallback"] = unreached
    out["A_cross_island"] = int(cross.sum())
    out["A_cross_island_pct"] = round(cross.sum() / max(nD, 1) * 100, 1)
    out["A_via_gutter"] = int(gut.sum())
    out["A_via_gutter_pct"] = round(gut.sum() / max(nD, 1) * 100, 1)
    out["A_max_front_step"] = int(step_a[D].max()) if nD else 0
    print(f"[g0-A] dilated texels               {nD:,}")
    print(f"[g0-A]   colour from ANOTHER island {int(cross.sum()):,}  "
          f"{cross.sum()/max(nD,1)*100:.1f}%")
    print(f"[g0-A]   path crossed the gutter    {int(gut.sum()):,}  "
          f"{gut.sum()/max(nD,1)*100:.1f}%")
    print(f"[g0-A]   never reached (mean fallback) {unreached:,}")
    print(f"[g0-A]   deepest front step         {out['A_max_front_step']}")

    # how far the foreign colour travelled, and how many islands imported ANY colour
    if int(cross.sum()):
        d = step_a[cross]
        out["A_cross_step_median"] = int(np.median(d))
        out["A_cross_step_p95"] = int(np.percentile(d, 95))
        print(f"[g0-A]   foreign-front depth median {int(np.median(d))} texels, "
              f"p95 {int(np.percentile(d,95))}")
    imp = np.unique(isl[cross]) if int(cross.sum()) else np.array([])
    out["A_islands_importing"] = int(len(imp))
    print(f"[g0-A]   islands importing foreign colour {len(imp):,} / {n_isl:,}")

    # The physical question. A chart boundary is not necessarily a surface boundary:
    # two charts meeting at a UV seam are CONTINUOUS on the surface, and importing
    # colour across that is correct behaviour, not the defect. What makes dilation a
    # defect is the source being somewhere else on the FIGURE.
    dflat = D.reshape(-1)
    sif = src_i.reshape(-1)
    got = dflat & (sif >= 0)
    d3 = np.linalg.norm(POS[np.flatnonzero(got)] - POS[sif[got]], axis=1)
    isl_f = isl.reshape(-1)
    cross_f = got & (isl_f != src.reshape(-1)) & (src.reshape(-1) >= 0)
    d3_cross = np.linalg.norm(POS[np.flatnonzero(cross_f)] - POS[sif[cross_f]], axis=1)
    for nm, arr in (("all", d3), ("crossisland", d3_cross)):
        out[f"A_srcdist_{nm}_median"] = round(float(np.median(arr)), 6)
        out[f"A_srcdist_{nm}_p95"] = round(float(np.percentile(arr, 95)), 6)
        out[f"A_srcdist_{nm}_gt_5edge_pct"] = round(
            float((arr > 5 * edge_med).mean() * 100), 1)
        out[f"A_srcdist_{nm}_gt_20edge_pct"] = round(
            float((arr > 20 * edge_med).mean() * 100), 1)
    print(f"[g0-A]   3D distance from a dilated texel to its COLOUR SOURCE:")
    print(f"[g0-A]     all dilated   median {np.median(d3):.5f}  p95 "
          f"{np.percentile(d3,95):.5f}  >5 edges {(d3>5*edge_med).mean()*100:.1f}%  "
          f">20 edges {(d3>20*edge_med).mean()*100:.1f}%")
    print(f"[g0-A]     cross-island  median {np.median(d3_cross):.5f}  p95 "
          f"{np.percentile(d3_cross,95):.5f}  >5 edges "
          f"{(d3_cross>5*edge_med).mean()*100:.1f}%  >20 edges "
          f"{(d3_cross>20*edge_med).mean()*100:.1f}%")

    # what the SAME texels would get from a surface-aware lookup — L1's bound, free
    from scipy.spatial import cKDTree
    paint_idx = np.flatnonzero((valid & ~holes).reshape(-1))
    tree = cKDTree(POS[paint_idx])
    dq, _ = tree.query(POS[np.flatnonzero(got)], k=1, workers=-1)
    out["A_L1_nearest_median"] = round(float(np.median(dq)), 6)
    out["A_L1_nearest_p95"] = round(float(np.percentile(dq, 95)), 6)
    out["A_L1_improves_pct"] = round(float((dq < d3 - 1e-9).mean() * 100), 1)
    out["A_L1_median_shrink_x"] = round(float(np.median(d3) / max(np.median(dq), 1e-12)), 2)
    print(f"[g0-A]   L1 BOUND — nearest painted texel in 3D for the same set:")
    print(f"[g0-A]     median {np.median(dq):.5f}  p95 {np.percentile(dq,95):.5f}  "
          f"closer for {(dq < d3-1e-9).mean()*100:.1f}% of them  "
          f"(median shrinks {np.median(d3)/max(np.median(dq),1e-12):.1f}x)")

    print("\n[g0-A'] counterfactual: same flood WITH `& valid` (nothing written)",
          flush=True)
    src2, via2, grown2, _, _ = flood(True)
    reached2 = D & (src2 >= 0)
    cross2 = reached2 & (src2 != isl)
    out["Ac_cross_island"] = int(cross2.sum())
    out["Ac_cross_island_pct"] = round(cross2.sum() / max(nD, 1) * 100, 1)
    out["Ac_via_gutter"] = int((reached2 & via2).sum())
    out["Ac_unreached"] = int((D & ~grown2).sum())
    print(f"[g0-A'] cross-island {int(cross2.sum()):,} "
          f"({cross2.sum()/max(nD,1)*100:.1f}%)   via gutter "
          f"{int((reached2 & via2).sum()):,}   unreached {int((D & ~grown2).sum()):,}")
    del src, via, grown, step_a, src_i, src2, via2, grown2

# ---------------------------------------------------------- head camera (parts B)
if "B" in args.parts and args.render:
    CX0, CY0, CX1, CY1 = [float(x) for x in args.head_crop.split(",")]
    b = args.bound
    sx0 = (CX0 / args.crop_res) * 2 * b - b
    sx1 = (CX1 / args.crop_res) * 2 * b - b
    sz0 = b - (CY1 / args.crop_res) * 2 * b
    sz1 = b - (CY0 / args.crop_res) * 2 * b
    cx, cz = (sx0 + sx1) / 2, (sz0 + sz1) / 2
    span = max(sx1 - sx0, sz1 - sz0) * args.pad
    R = args.res
    midy = (vz[:, 1].min() + vz[:, 1].max()) / 2
    xs = cx + (np.arange(R) + 0.5) / R * span - span / 2
    zs = cz + span / 2 - (np.arange(R) + 0.5) / R * span
    gx, gz = np.meshgrid(xs, zs)
    org = np.stack([gx, np.full_like(gx, midy - 6.0), gz], axis=-1)
    ans = rs.cast_rays(o3d.core.Tensor(np.concatenate(
        [org, np.broadcast_to(np.array([0.0, 1.0, 0.0]), org.shape)],
        axis=-1).reshape(-1, 6).astype(np.float32)))
    prim_h = ans["primitive_ids"].numpy().reshape(R, R)
    buv = ans["primitive_uvs"].numpy().reshape(R, R, 2)
    hit = np.isfinite(ans["t_hit"].numpy().reshape(R, R))
    tex = np.full((R, R), -1, dtype=np.int64)
    if hit.any():
        tr = f[prim_h[hit]]
        wu, wv = buv[hit][:, 0:1], buv[hit][:, 1:2]
        uvp = (1 - wu - wv) * uv[tr[:, 0]] + wu * uv[tr[:, 1]] + wv * uv[tr[:, 2]]
        ax = np.clip((uvp[:, 0] * RES).astype(np.int64), 0, RES - 1)
        ay = np.clip(((1 - uvp[:, 1]) * RES).astype(np.int64), 0, RES - 1)
        tex[hit] = ay * RES + ax

    claim = np.load(os.path.join(args.state, "claim.npy")).reshape(-1)
    islf = isl.reshape(-1)
    im = np.asarray(Image.open(args.render).convert("RGB"), dtype=np.float32) / 255
    lum = im.mean(-1)
    dev = np.abs(lum - median_filter(lum, size=5))
    blotch = (dev > args.blotch) & hit
    out["B_figure_px"] = int(hit.sum())
    out["B_blotch_px"] = int(blotch.sum())
    print(f"\n[g0-B] head render: figure {int(hit.sum()):,}px  "
          f"blotch {int(blotch.sum()):,}px  "
          f"(E06 recorded 490,544 / 3,533 — must match to be the same camera+render)")

    ok = hit & (tex >= 0)
    pairs = []
    for ax_ in (0, 1):
        a = [slice(None)] * 2
        c = [slice(None)] * 2
        a[ax_] = slice(0, -1)
        c[ax_] = slice(1, None)
        both = ok[tuple(a)] & ok[tuple(c)]
        t1 = tex[tuple(a)][both]
        t2 = tex[tuple(c)][both]
        dl = np.abs(lum[tuple(a)][both] - lum[tuple(c)][both])
        pairs.append((t1, t2, dl))
    t1 = np.concatenate([p[0] for p in pairs])
    t2 = np.concatenate([p[1] for p in pairs])
    dl = np.concatenate([p[2] for p in pairs])
    p1, p2 = claim[t1], claim[t2]
    i1, i2 = islf[t1], islf[t2]
    same_p = p1 == p2
    same_i = i1 == i2

    # A cross-provenance pair maps to two DIFFERENT texels by construction. A
    # within-provenance pair need not: where the render oversamples the atlas, many
    # neighbouring pixels sample the same texel and contribute a near-zero |dL| that
    # no provenance boundary could ever produce. Using all within-pairs as the
    # denominator therefore measures the magnification as well as the step. The
    # honest denominator is within-provenance AND different-texel; both are reported.
    diff_t = t1 != t2
    same_p_dt = same_p & diff_t
    med_w = float(np.median(dl[same_p]))
    med_w_dt = float(np.median(dl[same_p_dt]))
    med_c = float(np.median(dl[~same_p]))
    ratio = med_c / max(med_w, 1e-9)
    ratio_dt = med_c / max(med_w_dt, 1e-9)
    out["B_pairs_total"] = int(len(dl))
    out["B_pairs_cross_prov"] = int((~same_p).sum())
    out["B_within_same_texel_pct"] = round(float((same_p & ~diff_t).sum()
                                                 / max(int(same_p.sum()), 1) * 100), 1)
    out["B_median_dL_within"] = round(med_w, 5)
    out["B_median_dL_within_diff_texel"] = round(med_w_dt, 5)
    out["B_median_dL_cross"] = round(med_c, 5)
    out["B_step_ratio_naive"] = round(ratio, 3)
    out["B_step_ratio"] = round(ratio_dt, 3)
    print(f"[g0-B] pairs {len(dl):,}  cross-provenance {int((~same_p).sum()):,} "
          f"({(~same_p).mean()*100:.1f}%)")
    print(f"[g0-B]   within-provenance pairs sampling the SAME texel: "
          f"{out['B_within_same_texel_pct']}%  (these cannot contain a step)")
    print(f"[g0-B]   median |dL| within provenance, all pairs   {med_w:.5f}")
    print(f"[g0-B]   median |dL| within provenance, diff texel  {med_w_dt:.5f}  <- denom")
    print(f"[g0-B]   median |dL| across provenance              {med_c:.5f}")
    print(f"[g0-B]   STEP RATIO {ratio_dt:.3f}   (naive, same-texel pairs left in: "
          f"{ratio:.3f})")
    # 8-bit render: luminance is quantised to 1/765, so a median that lands on a small
    # integer multiple of it carries coarse precision. Report the step count directly.
    Q = 1.0 / 765.0
    print(f"[g0-B]   quantisation: denom {med_w_dt/Q:.1f} x 1/765, "
          f"numer {med_c/Q:.1f} x 1/765 (8-bit render floor)")
    out["B_denom_quanta"] = round(med_w_dt / Q, 1)
    out["B_numer_quanta"] = round(med_c / Q, 1)

    # control 1: island boundary at EQUAL provenance — surface structure and atlas
    # discontinuity with no provenance step in it. Same diff-texel denominator.
    ctl_c = dl[same_p & ~same_i & diff_t]
    if len(ctl_c) > 100:
        r_isl = float(np.median(ctl_c)) / max(med_w_dt, 1e-9)
        out["B_ctl_island_ratio"] = round(r_isl, 3)
        out["B_ctl_island_pairs"] = int(len(ctl_c))
        print(f"[g0-B]   CONTROL island boundary, same provenance: "
              f"{np.median(ctl_c):.5f} / {med_w_dt:.5f} = {r_isl:.3f} "
              f"({len(ctl_c):,} pairs)")
    # control 2: cross-provenance ratio measured WITHIN one island only — strips the
    # island confound out entirely, so what survives is the provenance step alone
    cw = dl[~same_p & same_i]
    if len(cw) > 100:
        r_in = float(np.median(cw)) / max(med_w_dt, 1e-9)
        out["B_cross_prov_same_island_ratio"] = round(r_in, 3)
        out["B_cross_prov_same_island_pairs"] = int(len(cw))
        print(f"[g0-B]   CONTROL cross-provenance INSIDE one island: "
              f"{np.median(cw):.5f} / {med_w_dt:.5f} = {r_in:.3f} ({len(cw):,} pairs)")

    LBL = {0: "TWINS", 255: "DILATION"}
    lab = lambda k: LBL.get(int(k), f"s{int(k)}")
    lo_p = np.minimum(p1, p2)
    hi_p = np.maximum(p1, p2)
    key = lo_p.astype(np.int64) * 256 + hi_p.astype(np.int64)
    print(f"[g0-B]   per boundary type (>=2,000 pairs), ratio vs within-median:")
    bt = {}
    for k in np.unique(key[~same_p]):
        sel = (key == k) & ~same_p
        if sel.sum() < 2000:
            continue
        name = f"{lab(k // 256)}|{lab(k % 256)}"
        r = float(np.median(dl[sel])) / max(med_w_dt, 1e-9)
        bt[name] = {"pairs": int(sel.sum()), "ratio": round(r, 3)}
        print(f"[g0-B]       {name:<22s} {int(sel.sum()):>8,} pairs   ratio {r:5.3f}")
    out["B_boundary_types"] = bt

# ------------------------------------------ C: stage-1 sigma=16 kernel, cross-island
if "C" in args.parts:
    base = os.path.splitext(args.stage1)[0]
    covA = np.load(base + "_styled_mask.npy")
    rr = int(round(3 * args.sigma))
    yy, xx = np.mgrid[-rr:rr + 1, -rr:rr + 1]
    G = np.exp(-(xx ** 2 + yy ** 2) / (2 * args.sigma ** 2))
    ys, xs_ = np.where(covA)
    rng = np.random.default_rng(args.seed)
    pick = rng.choice(len(ys), size=min(args.samples, len(ys)), replace=False)
    fr = np.empty(len(pick), dtype=np.float64)
    keep = np.ones(len(pick), dtype=bool)
    for j, p in enumerate(pick):
        y, x = int(ys[p]), int(xs_[p])
        y0, y1 = y - rr, y + rr + 1
        x0, x1 = x - rr, x + rr + 1
        if y0 < 0 or x0 < 0 or y1 > RES or x1 > RES:
            keep[j] = False
            continue
        w = G * covA[y0:y1, x0:x1]
        tot = w.sum()
        if tot <= 0:
            keep[j] = False
            continue
        fr[j] = (w * (isl[y0:y1, x0:x1] != isl[y, x])).sum() / tot
    fr = fr[keep]
    out["C_sigma"] = args.sigma
    out["C_samples"] = int(len(fr))
    out["C_foreign_weight_median"] = round(float(np.median(fr)), 4)
    out["C_foreign_weight_mean"] = round(float(fr.mean()), 4)
    out["C_foreign_weight_q1"] = round(float(np.percentile(fr, 25)), 4)
    out["C_foreign_weight_q3"] = round(float(np.percentile(fr, 75)), 4)
    out["C_frac_above_half"] = round(float((fr > 0.5).mean()), 4)
    print(f"\n[g0-C] stage-1 levelling kernel sigma={args.sigma}, "
          f"{len(fr):,} styled texels sampled")
    print(f"[g0-C]   foreign-island share of covered Gaussian weight:")
    print(f"[g0-C]     median {np.median(fr)*100:.1f}%   mean {fr.mean()*100:.1f}%   "
          f"IQR {np.percentile(fr,25)*100:.1f}-{np.percentile(fr,75)*100:.1f}%")
    print(f"[g0-C]     texels drawing MOST of their correction off-island: "
          f"{(fr>0.5).mean()*100:.1f}%")

if args.out_json:
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"\n[g0] wrote {args.out_json}")
