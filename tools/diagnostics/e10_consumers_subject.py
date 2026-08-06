"""E10 Ruling 4(a) — the off-surface consumer sweep, SUBJECT-FLAGGED.

WHY THIS FILE EXISTS AND WHY IT IS NOT `e10_offsurface_consumers.py`. That instrument
answers exactly this question and its method is the one reproduced here - but it is
hardcoded to the ship (`PREP = ...E04_shipprep`, the stage-1 and state paths, and the
ship's recorded anchors as module constants) and its numbers are cited in a closed ruling.
Editing it would rewrite the record. This carries the same method with the subject supplied
by flags and the anchors supplied by a versioned JSON fixture, exactly as `e12_offsurface.py`
carried the bake half. The two tools must agree on any subject both can run.

THE METHOD IS `e10_offsurface_consumers.py`'s, unchanged:
  - the WHOLE bake is classified (no sampling) by distance from each uv-valid texel's
    reconstructed position to the mesh, via open3d's raycasting scene;
  - "excluding" removes off-surface (>1 px) texels from BOTH numerator and denominator;
  - every consumer's replica is anchored against that consumer's own recorded number
    before its excluded recomputation is reported. A failed anchor halts THAT consumer's
    question. Nothing is ever substituted.

FRAMES, named at each conversion. `pos.npy` is the bake's UNIT CUBE (per-axis remap of
meta lo/hi). Positions convert to the CANONICAL mesh frame (Y-up->Z-up re-axed, max-abs
normalised * 0.5) exactly as every shipped consumer converts them. One image px is
`v_ext / H` in canonical units - supplied by --v-ext from the subject's OWN cam.json,
because getting it wrong scales every threshold.

TWO FLOAT ORDERINGS OF ONE CONVERSION live in this codebase and this tool carries both,
as the ship's did: `e10_offsurface.py` / `e12_offsurface.py` compute
`(lo + pos*(hi-lo)) * (0.5/maxabs)`; every route consumer computes
`(pos*(hi-lo) + lo)/maxabs * 0.5`. Algebraically identical, they differ in the last float
digits. The SAMPLE ANCHOR is computed with the source instrument's formula so it can match
to the digit; the exclusions use the consumers' own.

WHAT IT DOES NOT DO. It halts on a missed anchor and on nothing else. It classifies no
result as acceptable, adopts no threshold, and decides nothing about which denominator
family should be quoted - that is a ruling, and this tool's output is its input.

  e10_consumers_subject.py --prep DIR --anchors J.json --stage1-mask N.npy
                           --final-mask N.npy --v-ext X [--aspect W,H]
                           [--facing-min 0.45] [--head-facing-min 0.18]
                           [--cameras 8] [--sample 200000] [--out j.json]

Standards compliance: PIN_PER_STEP - every operand is a flag or a fixture entry and every
one is echoed. ANDON_AUTHORITY - each anchor halts its own question; there is no skip flag.
EXTERNAL_VERIFIER - the anchors come from a fixture this tool cannot write, recording
numbers measured by sessions that did not produce it. NAMED_COMPENSATORS - reads bakes and
sidecars, writes one JSON; undo is deleting it.
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def halt(msg):
    print("ANDON: " + msg, flush=True)
    raise SystemExit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prep", required=True)
    ap.add_argument("--anchors", required=True, help="the recorded-headline JSON fixture")
    ap.add_argument("--stage1-mask", required=True)
    ap.add_argument("--final-mask", required=True)
    ap.add_argument("--v-ext", type=float, required=True,
                    help="emit-camera vertical extent in canonical units, from the "
                         "subject's OWN cam.json")
    ap.add_argument("--aspect", default="752,1024")
    ap.add_argument("--facing-min", type=float, default=0.45)
    ap.add_argument("--head-facing-min", type=float, default=0.18)
    ap.add_argument("--cameras", type=int, default=8)
    ap.add_argument("--bias", type=float, default=3e-3)
    ap.add_argument("--noffs", type=float, default=1.5e-3)
    ap.add_argument("--sample", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sample-anchor", default=None,
                    help="pct1,pct5,median,max_px from the source instrument - the "
                         "cross-tool anchor. Omit to report the sample without anchoring.")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    J = os.path.join
    W, H = (int(x) for x in args.aspect.split(","))
    REC = json.load(open(args.anchors, encoding="utf-8"))
    rep = {"anchors_fixture": os.path.abspath(args.anchors),
           "label": REC.get("label"), "prep": os.path.abspath(args.prep)}

    meta = json.load(open(J(args.prep, "meta.json"), encoding="utf-8"))
    RES = meta["res"]
    one_px = args.v_ext / H
    rep["one_image_px_in_canonical_units"] = one_px
    print("[cons] %s" % REC.get("label"), flush=True)
    print("[cons] v_ext %.10f over H=%d -> ONE EMIT PIXEL = %.6e canonical units"
          % (args.v_ext, H, one_px), flush=True)

    mask2d = np.load(J(args.prep, "mask.npy"))[..., 0] > 0.5
    vidx = np.flatnonzero(mask2d.reshape(-1))       # row-major, the shared ordering
    NV = len(vidx)
    print("[cons] uv-valid texels %s (recorded %s)"
          % (f"{NV:,}", f"{REC['valid']['value']:,}"), flush=True)
    if NV != REC["valid"]["value"]:
        halt("uv-valid count does not reproduce the record - every ratio below would "
             "have a denominator the record does not name")
    rep["valid"] = int(NV)

    lo = np.array(meta["lo"], dtype=np.float64)
    hi = np.array(meta["hi"], dtype=np.float64)
    pos = np.load(J(args.prep, "pos.npy"), mmap_mode="r")
    P = (np.asarray(pos.reshape(-1, 3)[vidx], dtype=np.float64)
         * (hi - lo) + lo) / meta["maxabs"] * 0.5          # the consumers' ordering
    N = np.load(J(args.prep, "nor.npy")).reshape(-1, 3)[vidx].astype(np.float64) * 2.0 - 1.0
    N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12

    m = trimesh.load(J(args.prep, "prep_uv.glb"), force="mesh", process=False)
    v = np.asarray(m.vertices, dtype=np.float64)
    f = np.asarray(m.faces, dtype=np.int64)
    v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
    rs = o3d.t.geometry.RaycastingScene()
    rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                     o3d.core.Tensor(f.astype(np.uint32)))

    # ---- FULL classification (every uv-valid texel; no sampling) --------------------
    print("[cons] classifying all uv-valid texels (distance to surface, chunked)...",
          flush=True)
    d = np.empty(NV, dtype=np.float64)
    CH = 500000
    for i in range(0, NV, CH):
        d[i:i + CH] = rs.compute_distance(
            o3d.core.Tensor(P[i:i + CH].astype(np.float32))).numpy()
    off1 = d > one_px
    off5 = d > 5 * one_px
    on1 = ~off1
    print("[cons] full bake: OFF-SURFACE >1px %s (%.4f%%)   >5px %s (%.4f%%)   max %.1f px"
          % (f"{off1.sum():,}", off1.mean() * 100, f"{off5.sum():,}",
             off5.mean() * 100, d.max() / one_px), flush=True)
    rep["full_bake"] = {"off1": int(off1.sum()),
                        "off1_pct": round(float(off1.mean() * 100), 4),
                        "off5": int(off5.sum()),
                        "off5_pct": round(float(off5.mean() * 100), 4),
                        "max_px": float(d.max() / one_px),
                        "median_px": float(np.median(d) / one_px)}

    # ---- ANCHOR A: the source instrument's rng(seed) sample, its own float ordering --
    ys, xs = np.where(mask2d)
    k = np.random.default_rng(args.seed).choice(len(ys), min(args.sample, len(ys)),
                                                replace=False)
    s_scale = 0.5 / meta["maxabs"]
    Ps = (lo + np.asarray(pos[ys[k], xs[k]], dtype=np.float64) * (hi - lo)) * s_scale
    ds = rs.compute_distance(o3d.core.Tensor(Ps.astype(np.float32))).numpy()
    a = {"pct1": round(float((ds > one_px).mean() * 100), 4),
         "pct5": round(float((ds > 5 * one_px).mean() * 100), 4),
         "median": float(np.median(ds)), "max_px": float(ds.max() / one_px)}
    print("[cons] ANCHOR A (rng(%d) %s sample, source instrument's arithmetic): "
          ">1px %.4f%%  >5px %.4f%%  max %.4f px"
          % (args.seed, f"{len(k):,}", a["pct1"], a["pct5"], a["max_px"]), flush=True)
    if args.sample_anchor:
        p1, p5, med, mx = (float(x) for x in args.sample_anchor.split(","))
        if abs(a["pct1"] - p1) > 5e-5 or abs(a["pct5"] - p5) > 5e-5:
            halt("sample percentages do not reproduce the source instrument "
                 "(%.4f/%.4f vs %.4f/%.4f)" % (a["pct1"], a["pct5"], p1, p5))
        if abs(a["median"] - med) > max(1e-12, 1e-9 * abs(med)):
            halt("sample median %r != source %r" % (a["median"], med))
        if abs(a["max_px"] - mx) > 1e-4:
            halt("sample max %r px != source %r" % (a["max_px"], mx))
        print("[cons] ANCHOR A PASS - the full classification agrees with the source "
              "instrument on the same indices, to its recorded digits", flush=True)
    else:
        print("[cons] ANCHOR A: no --sample-anchor given; reported, NOT anchored",
              flush=True)
    rep["anchor_sample"] = a

    def excl(name, num_mask, den_mask, quoted):
        n0, d0 = int(num_mask.sum()), int(den_mask.sum())
        n1, d1 = int((num_mask & on1).sum()), int((den_mask & on1).sum())
        p0 = 100.0 * n0 / max(d0, 1)
        p1 = 100.0 * n1 / max(d1, 1)
        print("[cons] %s: %s/%s = %.4f%%  ->  excluded %s/%s = %.4f%%   "
              "(num loses %s; delta %+.4f pts; quoted %s)"
              % (name, f"{n0:,}", f"{d0:,}", p0, f"{n1:,}", f"{d1:,}", p1,
                 f"{n0-n1:,}", p1 - p0, quoted), flush=True)
        return {"as_recorded": {"num": n0, "den": d0, "pct": round(p0, 4)},
                "excluded": {"num": n1, "den": d1, "pct": round(p1, 4)},
                "num_off_surface": n0 - n1,
                "delta_pct_points": round(p1 - p0, 4), "recorded_quote": quoted}

    # ---- CONSUMER 1: the reach ceiling ---------------------------------------------
    CX0, CY0, CX1, CY1 = meta["crop"]
    b_std = 0.55
    px1k = (P[:, 0] + b_std) / (2 * b_std) * meta["crop_res"]
    py1k = (b_std - P[:, 2]) / (2 * b_std) * meta["crop_res"]
    headband = (px1k >= CX0) & (px1k <= CX1) & (py1k >= CY0) & (py1k <= CY1)
    print("\n[cons] CONSUMER 1 - e08_ceiling replica (body %.2f / head %.2f, %d "
          "equatorial cameras; head band %s texels)"
          % (args.facing_min, args.head_facing_min, args.cameras,
             f"{int(headband.sum()):,}"), flush=True)

    def dtc_of(yaw_d, el_d=0.0):
        th, el = np.radians(yaw_d), np.radians(el_d)
        cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
        return cd / np.linalg.norm(cd)

    if not np.allclose(dtc_of(0.0), [0.0, -1.0, 0.0]) \
       or not np.allclose(dtc_of(180.0), [0.0, 1.0, 0.0]):
        halt("camera generalisation does not reproduce project_twins' hardcoded pair")

    fmin = np.where(headband, args.head_facing_min, args.facing_min)
    R = np.zeros(NV, dtype=bool)
    for i in range(args.cameras):
        dtc = dtc_of(i * 360.0 / args.cameras)
        idx = np.where((N @ dtc) > fmin)[0]
        org = (P[idx] + N[idx] * args.noffs + dtc[None, :] * args.bias).astype(np.float32)
        t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org, np.broadcast_to(dtc.astype(np.float32), org.shape)],
            axis=1)))["t_hit"].numpy()
        R[idx[~np.isfinite(t)]] = True
    print("[cons] ANCHOR B: replica reachable %s (recorded %s)"
          % (f"{int(R.sum()):,}", f"{REC['reach']['value']:,}"), flush=True)
    if int(R.sum()) != REC["reach"]["value"]:
        halt("ceiling replica does not reproduce the recorded reachable count")
    rep["ceiling"] = excl("ceiling reach/valid", R, np.ones(NV, dtype=bool),
                          REC["reach"]["pct"])
    rep["ceiling"]["off_surface_reach_rate_pct"] = round(
        float(100.0 * (R & off1).sum() / max(int(off1.sum()), 1)), 4)
    print("[cons]   of the off-surface population, %.4f%% is reachable (population "
          "reach rate %.4f%%)"
          % (rep["ceiling"]["off_surface_reach_rate_pct"], 100.0 * R.mean()), flush=True)

    # ---- Class reconstruction + ANCHOR C -------------------------------------------
    print("\n[cons] class reconstruction from native sidecars", flush=True)
    s1 = np.load(args.stage1_mask).reshape(-1)[vidx].astype(bool)
    fin = np.load(args.final_mask).reshape(-1)[vidx].astype(bool)
    brush = fin & ~s1
    dil = ~fin
    got = (int(s1.sum()), int(brush.sum()), int(dil.sum()), int(fin.sum()))
    want = (REC["stage1"]["value"], REC["brush"]["value"], REC["dilation"]["value"],
            REC["painted"]["value"])
    print("[cons] ANCHOR C: stage1 %s (rec %s)  brush %s (rec %s)  dilation %s (rec %s)"
          "  painted %s (rec %s)"
          % tuple(f"{x:,}" for x in
                  (got[0], want[0], got[1], want[1], got[2], want[2], got[3], want[3])),
          flush=True)
    if got != want:
        halt("class reconstruction does not reproduce the record")

    ones = np.ones(NV, dtype=bool)
    print("\n[cons] CONSUMER 2 - acceptance (the quoted mix)", flush=True)
    rep["acceptance_styled_over_valid"] = excl("acceptance styled/valid", s1, ones,
                                               REC["stage1"]["pct"])
    rep["acceptance_styled_over_reachable"] = excl("acceptance styled/reachable", s1, R,
                                                  REC["styled_over_reachable_pct"]["value"])
    print("\n[cons] CONSUMER 3 - texpass_finalize (dilation)", flush=True)
    rep["finalize_dilation"] = excl("finalize dilation/valid", dil, ones,
                                    REC["dilation"]["pct"])
    print("\n[cons] CONSUMER 4 - project_twins (stage-1 commit; same operands as "
          "acceptance styled/valid)", flush=True)
    rep["twins_stage1"] = rep["acceptance_styled_over_valid"]
    print("\n[cons] CONSUMER 5 - texpass_iter commit (brush)", flush=True)
    rep["brush_total"] = excl("brush total/valid", brush, ones, REC["brush"]["pct"])

    # ---- per-stroke splits, where the record can anchor them ------------------------
    if REC.get("splits"):
        print("\n[cons] per-stroke splits, from atlas differences (each anchored)",
              flush=True)
        tbl = {}
        for sp in REC["splits"]:
            b = np.asarray(Image.open(sp["before"]).convert("RGB"))
            af = np.asarray(Image.open(sp["after"]).convert("RGB"))
            if b.shape != af.shape:
                halt("split %r: atlas shapes differ" % sp["label"])
            changed = (b != af).any(axis=-1).reshape(-1)[vidx]
            sm = changed & brush
            n0 = int(sm.sum())
            ok = (n0 == sp["anchor"])
            print("[cons] ANCHOR D %s: atlas-diff within brush %s (recorded %s)  %s"
                  % (sp["label"], f"{n0:,}", f"{sp['anchor']:,}",
                     "OK" if ok else "MISMATCH (%+d)" % (n0 - sp["anchor"])), flush=True)
            if not ok:
                tbl[sp["label"]] = {"replayed": n0, "recorded": sp["anchor"],
                                    "anchored": False,
                                    "note": "NOT anchored - exclusion not computed, "
                                            "nothing substituted"}
                continue
            n1 = int((sm & on1).sum())
            tbl[sp["label"]] = {"anchored": True, "recorded": n0, "excluded": n1,
                                "off_surface": n0 - n1,
                                "off_pct_of_split": round(100.0 * (n0 - n1) / max(n0, 1), 4)}
            print("[cons]   %s: %s -> %s (loses %s = %.4f%%)"
                  % (sp["label"], f"{n0:,}", f"{n1:,}", f"{n0-n1:,}",
                     100.0 * (n0 - n1) / max(n0, 1)), flush=True)
        rep["splits"] = tbl

    # ---- where the off-surface population lives ------------------------------------
    print("\n[cons] off-surface (>1px) population composition by provenance class",
          flush=True)
    tot = max(int(off1.sum()), 1)
    comp = {}
    for lab, sel in [("stage1", s1), ("brush", brush), ("dilation", dil),
                     ("reachable", R)]:
        n = int((sel & off1).sum())
        comp[lab] = {"texels": n,
                     "share_of_off_surface": round(100.0 * n / tot, 4),
                     "off_surface_rate_within_class":
                         round(100.0 * n / max(int(sel.sum()), 1), 4)}
        print("[cons]   %-10s %8s  (%6.2f%% of the off-surface population)   rate "
              "within class %.4f%%"
              % (lab, f"{n:,}", 100.0 * n / tot,
                 100.0 * n / max(int(sel.sum()), 1)), flush=True)
    print("[cons]   population baseline %.4f%%   (reachable overlaps the painted "
          "classes and is listed for comparison, not as a fourth partition)"
          % (off1.mean() * 100), flush=True)
    rep["off_surface_composition"] = comp

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
        json.dump(rep, open(args.out, "w"), indent=1)
        print("\n[json] %s" % os.path.abspath(args.out), flush=True)
    print("Reported, not ruled.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
