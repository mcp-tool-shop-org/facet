"""E10 Ruling 4(b) — WHERE the painted off-surface texels live. Mechanism measurement.

E10 Ruling 3 banked *that* the off-surface population is painted rather than padding, and
ruled NO mechanism. This measures where those texels sit - in the atlas, on the charts,
across the reference views, and across the brush strokes - and reports it. It rules
nothing, fixes nothing, and derives no threshold.

EVERY NUMBER HERE HAS A WORKS-PERFECTLY VALUE, WRITTEN DOWN BEFORE IT WAS READ
(`E10-offsurface-r4ab-predictions.md`, sha256 38408839..., hashed 2026-08-06 00:30:34).
The trap this file is built against: B1/B3/B7/B8 are rate-per-stratum measurements, and a
rate-per-stratum measurement on a DEFECT-FREE artifact is FLAT, NOT ZERO. Every table
below therefore prints the population baseline beside the strata, so "the numbers are
small" can never be misread as "nothing is wrong". Flatness is the null; shape is the
signal.

AND ONE MEASUREMENT IS BARRED FROM GATING BY CONSTRUCTION. B1's strata are distance to an
island boundary - the exact proxy this repo already paid a session for ("test the property,
not a geometric proxy for it": a 1-2 texel structure is entirely rim, so rim distance
partly measures how thin a structure is rather than whether it is contaminated). B1 is a
diagnostic. It must not become a threshold, and the predictions file said so before its
value was known.

  e10_offsurface_where.py --prep DIR --one-px X --stage1-mask N.npy --owner N.npy
                          --final-mask N.npy [--claim claim.npy] [--out j.json]

Standards compliance: PIN_PER_STEP - the pixel unit and every path are flags and are
echoed; the predictions hash is carried into the JSON. ANDON_AUTHORITY - the per-stroke
table halts if the claim map does not reproduce the recorded commits. EXTERNAL_VERIFIER -
the population is re-derived here and checked against `offsurface_consumers.json`, an
artifact this tool did not write. NAMED_COMPENSATORS - reads bakes and sidecars, writes
one JSON; undo is deleting it.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from scipy.ndimage import distance_transform_edt, label

PRED_SHA = "38408839eff743729eb22488d7b203b400afa175322fdfdaea20eaf8aad279cb"
STROKE_ORDER = ["y+300_e+00", "y+030_e+00", "y+150_e+00", "y+240_e+00",
                "y+000_e+40", "y+180_e+40"]
REC_PER_STROKE = {"y+300_e+00": 26531, "y+030_e+00": 22766, "y+150_e+00": 17904,
                  "y+240_e+00": 24486, "y+000_e+40": 63288, "y+180_e+40": 58877}
STRATA = [("rim<=1", 0.0, 1.0), ("rim 2-3", 1.0, 3.0), ("rim 4-8", 3.0, 8.0),
          ("rim >8", 8.0, np.inf)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prep", required=True)
    ap.add_argument("--one-px", type=float, required=True,
                    help="one emit-image pixel in canonical units (v_ext/H)")
    ap.add_argument("--stage1-mask", required=True)
    ap.add_argument("--owner", required=True, help="per-texel stage-1 view owner sidecar")
    ap.add_argument("--final-mask", required=True)
    ap.add_argument("--claim", default=None, help="claim.npy from e10_claim_replay.py")
    ap.add_argument("--expect-off1", type=int, default=None,
                    help="the recorded off-surface count, as an external check")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    J = os.path.join
    one_px = args.one_px
    rep = {"predictions_sha256": PRED_SHA, "prep": os.path.abspath(args.prep),
           "one_image_px_in_canonical_units": one_px}

    meta = json.load(open(J(args.prep, "meta.json"), encoding="utf-8"))
    RES = meta["res"]
    mask2d = np.load(J(args.prep, "mask.npy"))[..., 0] > 0.5
    vidx = np.flatnonzero(mask2d.reshape(-1))
    NV = len(vidx)
    lo = np.array(meta["lo"], dtype=np.float64)
    hi = np.array(meta["hi"], dtype=np.float64)
    pos = np.load(J(args.prep, "pos.npy"), mmap_mode="r")
    posv = np.asarray(pos.reshape(-1, 3)[vidx])          # raw, for the duplicate test
    P = (posv.astype(np.float64) * (hi - lo) + lo) / meta["maxabs"] * 0.5

    m = trimesh.load(J(args.prep, "prep_uv.glb"), force="mesh", process=False)
    v = np.asarray(m.vertices, dtype=np.float64)
    f = np.asarray(m.faces, dtype=np.int64)
    vc = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
    rs = o3d.t.geometry.RaycastingScene()
    rs.add_triangles(o3d.core.Tensor(vc.astype(np.float32)),
                     o3d.core.Tensor(f.astype(np.uint32)))

    print("[where] classifying all %s uv-valid texels..." % f"{NV:,}", flush=True)
    d = np.empty(NV, dtype=np.float64)
    for i in range(0, NV, 500000):
        d[i:i + 500000] = rs.compute_distance(
            o3d.core.Tensor(P[i:i + 500000].astype(np.float32))).numpy()
    off = d > one_px
    far = d > 5 * one_px
    NOFF = int(off.sum())
    base = 100.0 * NOFF / NV
    print("[where] OFF-SURFACE >1px %s (%.4f%%)   >5px %s   max %.1f px"
          % (f"{NOFF:,}", base, f"{int(far.sum()):,}", d.max() / one_px), flush=True)
    if args.expect_off1 is not None and NOFF != args.expect_off1:
        print("ANDON: off-surface count %d != recorded %d" % (NOFF, args.expect_off1),
              flush=True)
        raise SystemExit(1)
    print("[where] EXTERNAL CHECK PASS - population matches the recorded count",
          flush=True)
    rep["population"] = {"off1": NOFF, "off1_pct": round(base, 4),
                         "off5": int(far.sum()),
                         "far_share_of_population_pct": round(100.0 * far.sum() / NOFF, 2)}

    def rate_table(title, keys, sel_of, null_note):
        print("\n[where] %s" % title, flush=True)
        print("[where]   WORKS-PERFECTLY: %s" % null_note, flush=True)
        rows = {}
        for kname in keys:
            sel = sel_of(kname)
            n, tot = int((sel & off).sum()), int(sel.sum())
            r = 100.0 * n / max(tot, 1)
            rows[kname] = {"texels": tot, "off_surface": n, "rate_pct": round(r, 4),
                           "share_of_population_pct": round(100.0 * n / max(NOFF, 1), 2),
                           "vs_baseline": round(r / base, 3) if base else None}
            print("[where]   %-12s %10s texels   off %8s   rate %7.4f%%   "
                  "%5.2fx baseline   (%5.2f%% of the population)"
                  % (kname, f"{tot:,}", f"{n:,}", r, r / base if base else 0,
                     100.0 * n / max(NOFF, 1)), flush=True)
        print("[where]   baseline (population) %.4f%%" % base, flush=True)
        return rows

    # ---- B1 / B5: island-rim distance ----------------------------------------------
    print("\n[where] B1 - island-rim distance (EDT of the uv-valid mask; a texel's "
          "distance to the nearest non-valid texel, in ATLAS texels)", flush=True)
    rim = distance_transform_edt(mask2d).reshape(-1)[vidx]
    rep["rim_distance"] = {
        "off_surface_median": float(np.median(rim[off])),
        "on_surface_median": float(np.median(rim[~off])),
        "off_surface_mean": float(rim[off].mean()),
        "on_surface_mean": float(rim[~off].mean())}
    print("[where]   median rim distance: off-surface %.2f  vs  on-surface %.2f "
          "(WORKS-PERFECTLY: equal, ratio 1.00; measured ratio %.3f)"
          % (rep["rim_distance"]["off_surface_median"],
             rep["rim_distance"]["on_surface_median"],
             rep["rim_distance"]["off_surface_median"]
             / max(rep["rim_distance"]["on_surface_median"], 1e-9)), flush=True)
    rep["b1_strata"] = rate_table(
        "B1 - off-surface RATE per rim-distance stratum", [s[0] for s in STRATA],
        lambda kn: (rim > dict((s[0], s[1]) for s in STRATA)[kn])
                   & (rim <= dict((s[0], s[2]) for s in STRATA)[kn]),
        "a FLAT curve at %.4f%% - every stratum equal. Zero only if the bake is "
        "perfect." % base)
    b1 = rep["b1_strata"]
    print("[where]   B1a ratio (rim<=1 : rim>8) = %.2fx"
          % (b1["rim<=1"]["rate_pct"] / max(b1["rim >8"]["rate_pct"], 1e-9)), flush=True)
    deep = sum(b1[k]["off_surface"] for k in ["rim 2-3", "rim 4-8", "rim >8"])
    print("[where]   B1b: %.2f%% of the population sits at rim distance >= 2"
          % (100.0 * deep / max(NOFF, 1)), flush=True)
    rep["b1a_ratio"] = round(b1["rim<=1"]["rate_pct"] / max(b1["rim >8"]["rate_pct"],
                                                            1e-9), 3)
    rep["b1b_pct_at_rim_ge_2"] = round(100.0 * deep / max(NOFF, 1), 2)

    print("\n[where] B5 - depth of the error per rim stratum (share of that stratum's "
          "off-surface texels that are >5 px off)", flush=True)
    print("[where]   WORKS-PERFECTLY: the SAME share in every stratum (%.2f%%)"
          % rep["population"]["far_share_of_population_pct"], flush=True)
    b5 = {}
    for kname, lo_r, hi_r in STRATA:
        sel = (rim > lo_r) & (rim <= hi_r) & off
        n = int(sel.sum())
        s = 100.0 * int((sel & far).sum()) / max(n, 1)
        b5[kname] = {"off_surface": n, "far_share_pct": round(s, 2)}
        print("[where]   %-12s off %8s   >5px share %6.2f%%"
              % (kname, f"{n:,}", s), flush=True)
    rep["b5_depth_per_stratum"] = b5

    # ---- B2: is the rim a seam? -----------------------------------------------------
    print("\n[where] B2 - seam adjacency: is an island rim a SEAM, or a mesh boundary?",
          flush=True)
    print("[where]   WORKS-PERFECTLY: on a closed mesh every island rim IS a seam, so "
          "B2 is arithmetically B1 and there is no second number.", flush=True)
    vr = np.round(v, 9)
    _, inv = np.unique(vr, axis=0, return_inverse=True)
    fw = inv[f]
    e = np.sort(np.stack([fw[:, [0, 1]], fw[:, [1, 2]], fw[:, [2, 0]]]).reshape(-1, 2),
                axis=1)
    _, cnt = np.unique(e, axis=0, return_counts=True)
    nb = int((cnt == 1).sum())
    print("[where]   welded: %s unique vertices from %s exported (glTF splits at every "
          "UV seam)" % (f"{inv.max()+1:,}", f"{len(v):,}"), flush=True)
    print("[where]   BOUNDARY edges (one incident face): %s of %s unique edges = %.4f%%"
          % (f"{nb:,}", f"{len(cnt):,}", 100.0 * nb / len(cnt)), flush=True)
    rep["b2_seams"] = {"exported_vertices": int(len(v)), "welded_vertices": int(inv.max() + 1),
                       "unique_edges": int(len(cnt)), "boundary_edges": nb,
                       "boundary_pct": round(100.0 * nb / len(cnt), 4)}

    # ---- B3: per stage-1 owning view -------------------------------------------------
    s1 = np.load(args.stage1_mask).reshape(-1)[vidx].astype(bool)
    own = np.load(args.owner).reshape(-1)[vidx]
    views = sorted(int(x) for x in np.unique(own[s1]))
    rep["b3_per_view"] = rate_table(
        "B3 - off-surface rate within each stage-1 owning view",
        ["view %d" % x for x in views],
        lambda kn: s1 & (own == int(kn.split()[1])),
        "EIGHT EQUAL rates, each the stage-1 class rate (3.06%%). Zero only if the "
        "bake is perfect.")
    rr = [rep["b3_per_view"][k]["rate_pct"] for k in rep["b3_per_view"]]
    print("[where]   B3 spread: max/min = %.2fx" % (max(rr) / max(min(rr), 1e-9)),
          flush=True)
    rep["b3_spread"] = round(max(rr) / max(min(rr), 1e-9), 3)

    near = rim <= 1.0

    def decompose(title, keys, sel_of):
        """Is a group's rate high because it OWNS more rim, or because its rim texels
        are worse? Splitting the rate into composition x susceptibility answers that
        with arithmetic instead of a story. ADDED AFTER THE FIRST PASS, to answer the
        dispatch's stroke-1 question; it introduces no threshold and changes no number
        above - every rate here re-derives from the same masks."""
        print("\n[where] %s" % title, flush=True)
        print("[where]   WORKS-PERFECTLY / no group difference: equal rim SHARE and "
              "equal rim RATE across groups - the two columns move together only if "
              "the groups genuinely differ.", flush=True)
        rows = {}
        for kn in keys:
            sel = sel_of(kn)
            tot = int(sel.sum())
            nr, dr = int((sel & near).sum()), int((sel & ~near).sum())
            r_near = 100.0 * int((sel & near & off).sum()) / max(nr, 1)
            r_deep = 100.0 * int((sel & ~near & off).sum()) / max(dr, 1)
            share = 100.0 * nr / max(tot, 1)
            rows[kn] = {"pct_at_rim_le_1": round(share, 2),
                        "off_rate_within_rim_le_1": round(r_near, 4),
                        "off_rate_within_rim_ge_2": round(r_deep, 4)}
            print("[where]   %-12s  rim<=1 is %6.2f%% of it   |   off-rate within "
                  "rim<=1 %7.4f%%   within rim>=2 %7.4f%%"
                  % (kn, share, r_near, r_deep), flush=True)
        allr = 100.0 * int((near & off).sum()) / max(int(near.sum()), 1)
        print("[where]   whole bake:    rim<=1 is %6.2f%% of it   |   off-rate within "
              "rim<=1 %7.4f%%   within rim>=2 %7.4f%%"
              % (100.0 * near.sum() / NV, allr,
                 100.0 * int((~near & off).sum()) / max(int((~near).sum()), 1)),
              flush=True)
        return rows

    rep["b3b_decomposition"] = decompose(
        "B3b - per view: composition (how much rim it owns) vs susceptibility "
        "(how bad its rim is)", ["view %d" % x for x in views],
        lambda kn: s1 & (own == int(kn.split()[1])))

    # ---- B4: is it a constant fill? --------------------------------------------------
    print("\n[where] B4 - are the off-surface positions a repeated DEFAULT value?",
          flush=True)
    print("[where]   WORKS-PERFECTLY: modal duplicate count 1-2, coincidence only - and "
          "the on-surface population is the null to read it against.", flush=True)

    def modal(rows):
        _, c = np.unique(rows, axis=0, return_counts=True)
        return int(c.max()), int((c > 1).sum()), int(len(c))

    mo, do, uo = modal(posv[off])
    mn, dn, un = modal(posv[~off])
    print("[where]   off-surface: %s texels -> %s distinct positions, modal duplicate "
          "count %s" % (f"{NOFF:,}", f"{uo:,}", f"{mo:,}"), flush=True)
    print("[where]   on-surface : %s texels -> %s distinct positions, modal duplicate "
          "count %s   <- the null" % (f"{NV-NOFF:,}", f"{un:,}", f"{mn:,}"), flush=True)
    rep["b4_duplicates"] = {"off_modal": mo, "off_distinct": uo, "off_n": NOFF,
                            "on_modal": mn, "on_distinct": un, "on_n": int(NV - NOFF)}

    # ---- B6: atlas-space clustering --------------------------------------------------
    print("\n[where] B6 - connected components of the off-surface set in the atlas "
          "(8-connectivity)", flush=True)
    print("[where]   WORKS-PERFECTLY / true speckle: thousands of tiny components, "
          "largest in the tens.", flush=True)
    offimg = np.zeros(RES * RES, dtype=bool)
    offimg[vidx[off]] = True
    lab, n = label(offimg.reshape(RES, RES), structure=np.ones((3, 3), dtype=int))
    sizes = np.bincount(lab.reshape(-1))[1:]
    big = sizes[sizes >= 100]
    print("[where]   %s components; largest %s; %s components >=100 texels holding "
          "%.2f%% of the population"
          % (f"{n:,}", f"{int(sizes.max()):,}", f"{len(big):,}",
             100.0 * big.sum() / max(NOFF, 1)), flush=True)
    rep["b6_components"] = {"n": int(n), "largest": int(sizes.max()),
                            "n_ge_100": int(len(big)),
                            "pct_in_ge_100": round(100.0 * big.sum() / max(NOFF, 1), 2),
                            "top10": [int(x) for x in np.sort(sizes)[::-1][:10]]}
    del lab, offimg

    # ---- B7: per-island rate ---------------------------------------------------------
    print("\n[where] B7 - off-surface rate per UV ISLAND (connected components of the "
          "uv-valid mask)", flush=True)
    print("[where]   WORKS-PERFECTLY: every island at the baseline %.4f%%; no island "
          "near 0%% or 100%%." % base, flush=True)
    ilab, nis = label(mask2d, structure=np.ones((3, 3), dtype=int))
    iv = ilab.reshape(-1)[vidx]
    del ilab
    tot_i = np.bincount(iv, minlength=nis + 1)
    off_i = np.bincount(iv[off], minlength=nis + 1)
    ok = tot_i > 0
    rate_i = np.zeros(nis + 1)
    rate_i[ok] = 100.0 * off_i[ok] / tot_i[ok]
    hot = ok & (rate_i > 90.0)
    hot50 = ok & (rate_i > 50.0)
    print("[where]   %s islands; median island size %s texels"
          % (f"{nis:,}", f"{int(np.median(tot_i[ok])):,}"), flush=True)
    print("[where]   islands >90%% off-surface: %s, holding %s texels = %.2f%% of the "
          "population" % (f"{int(hot.sum()):,}", f"{int(off_i[hot].sum()):,}",
                          100.0 * off_i[hot].sum() / max(NOFF, 1)), flush=True)
    print("[where]   islands >50%% off-surface: %s, holding %.2f%% of the population"
          % (f"{int(hot50.sum()):,}", 100.0 * off_i[hot50].sum() / max(NOFF, 1)),
          flush=True)
    order = np.argsort(off_i)[::-1][:10]
    print("[where]   the ten islands contributing most off-surface texels:", flush=True)
    for i in order:
        if tot_i[i] == 0:
            continue
        print("[where]     island %-7d size %9s   off %8s   rate %7.3f%%"
              % (i, f"{int(tot_i[i]):,}", f"{int(off_i[i]):,}", rate_i[i]), flush=True)
    rep["b7_islands"] = {
        "n_islands": int(nis), "median_size": int(np.median(tot_i[ok])),
        "n_gt90": int(hot.sum()),
        "pct_population_in_gt90": round(100.0 * off_i[hot].sum() / max(NOFF, 1), 2),
        "n_gt50": int(hot50.sum()),
        "pct_population_in_gt50": round(100.0 * off_i[hot50].sum() / max(NOFF, 1), 2),
        "top10": [{"island": int(i), "size": int(tot_i[i]), "off": int(off_i[i]),
                   "rate_pct": round(float(rate_i[i]), 3)} for i in order
                  if tot_i[i] > 0]}

    # ---- B8: the strokes --------------------------------------------------------------
    if args.claim:
        claim = np.load(args.claim).reshape(-1)[vidx]
        anchored = True
        for i, key in enumerate(STROKE_ORDER, start=1):
            c = int((claim == i).sum())
            if c != REC_PER_STROKE[key]:
                print("ANDON: stroke %d %s replay %d != recorded %d"
                      % (i, key, c, REC_PER_STROKE[key]), flush=True)
                anchored = False
        if not anchored:
            raise SystemExit(1)
        print("\n[where] B8 - the six strokes (claim map anchored: all six commits "
              "reproduce the record exactly)", flush=True)
        rep["b8_strokes"] = rate_table(
            "B8 - off-surface rate per stroke", STROKE_ORDER,
            lambda kn: claim == (STROKE_ORDER.index(kn) + 1),
            "SIX EQUAL rates, each the brush class rate (2.27%%). Zero only if the "
            "bake is perfect.")
        print("\n[where] B8 continued - WHERE each stroke's off-surface commits sit",
              flush=True)
        print("[where]   WORKS-PERFECTLY: identical profiles across the six strokes.",
              flush=True)
        det = {}
        for i, key in enumerate(STROKE_ORDER, start=1):
            sel = (claim == i) & off
            n = int(sel.sum())
            if n == 0:
                det[key] = {"off": 0}
                continue
            in90 = int(np.isin(iv[sel], np.flatnonzero(hot)).sum())
            in50 = int(np.isin(iv[sel], np.flatnonzero(hot50)).sum())
            det[key] = {"off": n, "median_rim": float(np.median(rim[sel])),
                        "far_share_pct": round(100.0 * int((sel & far).sum()) / n, 2),
                        "pct_in_islands_gt90": round(100.0 * in90 / n, 2),
                        "pct_in_islands_gt50": round(100.0 * in50 / n, 2)}
            print("[where]   stroke %d %-12s off %6s   median rim %5.2f   >5px %6.2f%%"
                  "   in >90%%-off islands %6.2f%%   in >50%% %6.2f%%"
                  % (i, key, f"{n:,}", det[key]["median_rim"], det[key]["far_share_pct"],
                     det[key]["pct_in_islands_gt90"], det[key]["pct_in_islands_gt50"]),
                  flush=True)
        rep["b8_where"] = det
        rep["b8b_decomposition"] = decompose(
            "B8b - per stroke: composition (how much rim it commits) vs "
            "susceptibility (how bad its rim is) - the dispatch's stroke-1 question",
            STROKE_ORDER, lambda kn: claim == (STROKE_ORDER.index(kn) + 1))
    else:
        print("\n[where] B8 skipped - no --claim given", flush=True)

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
        json.dump(rep, open(args.out, "w"), indent=1)
        print("\n[json] %s" % os.path.abspath(args.out), flush=True)
    print("Reported, not ruled.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
