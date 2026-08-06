"""E10 Ruling 4's dispatched measurement — per consumer, does excluding the
off-surface 2.5% move your headline number?

READ-ONLY over the route: no route tool is edited, no accepted artifact is opened for
writing. Writes one JSON into e10_contact/ beside the finding it extends.

The population is the one e10_offsurface.py measured (2.5065% of uv-valid texels carry
positions >1 image px off the mesh). This tool classifies the WHOLE bake (no sampling),
anchors that classification against the recorded 200k sample to the digit, anchors each
consumer's replica against the consumer's own recorded number, and only then reports
the excluded recomputation. A failed anchor halts that consumer's question rather than
substituting a number.

Frames (named per E10 Rulings 2/4): pos.npy is the bake's UNIT CUBE (per-axis remap of
meta lo/hi); positions are converted to the CANONICAL mesh frame (Y-up->Z-up re-axed,
max-abs normalised * 0.5) exactly as every shipped consumer converts them; one image px
is cam.json's v_ext/H in canonical units, the same constant offsurface.json recorded.

  e10_offsurface_consumers.py [--claim PATH]   # claim.npy from texel_provenance's
                                               # replay (run against a state COPY);
                                               # omit to skip per-stroke exclusion
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh

PREP = r"E:\AI\training\facet_next\E04_shipprep"
STROKE = r"E:\AI\training\facet_next\E04_stroke"
STAGE1 = r"E:\AI\training\facet_next\E04_armT72\stage1"

# Recorded anchors — the numbers this tool must reproduce before its recomputes
# mean anything. Sources: e10_contact/offsurface.json, E04-h4-ceiling.md,
# out/provenance.json. None of them is presumed wrong; they are what "anchored" means.
REC_SAMPLE = {"pct1": 2.5065, "pct5": 2.0940, "median": 6.7309556470718235e-06,
              "max_px": 147.4324188232422}
REC_CEILING_REACH = 1329359
REC_STAGE1 = 1147959
REC_BRUSH = 213852
REC_DILATION = 1750006
REC_PAINTED = 1361811
REC_VALID = 3111817
REC_PER_STROKE = {"y+300_e+00": 26531, "y+030_e+00": 22766, "y+150_e+00": 17904,
                  "y+240_e+00": 24486, "y+000_e+40": 63288, "y+180_e+40": 58877}
STROKE_ORDER = ["y+300_e+00", "y+030_e+00", "y+150_e+00", "y+240_e+00",
                "y+000_e+40", "y+180_e+40"]


def halt(msg):
    print("ANDON: " + msg)
    raise SystemExit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim", help="claim.npy from texel_provenance replay (state COPY)")
    ap.add_argument("--out", default=os.path.join(STROKE, "e10_contact",
                                                  "offsurface_consumers.json"))
    args = ap.parse_args()
    J = os.path.join
    rep = {"predictions_sha256":
           "cf16bb5552981d44228d95bda9d9d5ca9312b8d0fed94c579856137de35813ee"}

    meta = json.load(open(J(PREP, "meta.json"), encoding="utf-8"))
    RES = meta["res"]
    cam = json.load(open(J(STROKE, "sheet", "asset", "job_y+000_e+00", "cam.json")))
    one_px = cam["v_ext"] / cam["H"]
    rep["one_image_px_in_canonical_units"] = one_px

    mask2d = np.load(J(PREP, "mask.npy"))[..., 0] > 0.5
    valid_flat = mask2d.reshape(-1)
    vidx = np.flatnonzero(valid_flat)          # row-major, the shared ordering
    NV = len(vidx)
    print(f"[cons] uv-valid texels {NV:,}  (recorded {REC_VALID:,}; "
          f"E04-h4-ceiling.md quotes 3,111,832 - both reported, measured value governs)")
    rep["valid_measured"] = int(NV)

    lo = np.array(meta["lo"], dtype=np.float64)
    hi = np.array(meta["hi"], dtype=np.float64)
    pos = np.load(J(PREP, "pos.npy"), mmap_mode="r")
    P = (np.asarray(pos.reshape(-1, 3)[vidx], dtype=np.float64)
         * (hi - lo) + lo) / meta["maxabs"] * 0.5
    N = np.load(J(PREP, "nor.npy")).reshape(-1, 3)[vidx].astype(np.float64) * 2.0 - 1.0
    N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12

    m = trimesh.load(J(PREP, "prep_uv.glb"), force="mesh", process=False)
    v = np.asarray(m.vertices, dtype=np.float64)
    f = np.asarray(m.faces, dtype=np.int64)
    v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
    rs = o3d.t.geometry.RaycastingScene()
    rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                     o3d.core.Tensor(f.astype(np.uint32)))

    # ---- FULL classification (every uv-valid texel; no sampling) -------------------
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
    print(f"[cons] full bake: OFF-SURFACE >1px {off1.sum():,} ({off1.mean()*100:.4f}%)"
          f"   >5px {off5.sum():,} ({off5.mean()*100:.4f}%)   max {d.max()/one_px:.1f} px")
    rep["full_bake"] = {"off1": int(off1.sum()), "off1_pct": round(float(off1.mean() * 100), 4),
                        "off5": int(off5.sum()), "off5_pct": round(float(off5.mean() * 100), 4),
                        "max_px": float(d.max() / one_px)}

    # ---- ANCHOR A: the recorded 200k sample, reproduced with e10_offsurface.py's OWN
    # arithmetic. Two float expressions of the same conversion live in this codebase:
    # e10_offsurface computes (lo + pos*(hi-lo)) * (0.5/maxabs); every route consumer
    # computes (pos*(hi-lo) + lo) / maxabs * 0.5. Algebraically identical, they differ
    # by ~3e-6 px at the sample's max — enough to fail a digit anchor. Each computation
    # is anchored against its own formula; the report carries the variant note.
    ys, xs = np.where(mask2d)
    k = np.random.default_rng(0).choice(len(ys), min(200000, len(ys)), replace=False)
    flat_sample = ys[k] * RES + xs[k]
    si = np.searchsorted(vidx, flat_sample)
    if not np.array_equal(vidx[si], flat_sample):
        halt("sample indices do not map into the valid set - ordering assumption broken")
    s_scale = 0.5 / meta["maxabs"]
    Ps = (lo + np.asarray(pos[ys[k], xs[k]], dtype=np.float64) * (hi - lo)) * s_scale
    ds = rs.compute_distance(o3d.core.Tensor(Ps.astype(np.float32))).numpy()
    dv = np.abs(ds - d[si])
    print(f"[cons] formula-variant delta on the sample: max |d_A - d_B| = "
          f"{dv.max()/one_px:.2e} px (two float orderings of one conversion)")
    a = {"pct1": round(float((ds > one_px).mean() * 100), 4),
         "pct5": round(float((ds > 5 * one_px).mean() * 100), 4),
         "median": float(np.median(ds)),
         "max_px": float(ds.max() / one_px)}
    print(f"[cons] ANCHOR A (recorded rng(0) sample): >1px {a['pct1']:.4f}% "
          f"(rec {REC_SAMPLE['pct1']:.4f})   >5px {a['pct5']:.4f}% "
          f"(rec {REC_SAMPLE['pct5']:.4f})")
    if abs(a["pct1"] - REC_SAMPLE["pct1"]) > 5e-5 or abs(a["pct5"] - REC_SAMPLE["pct5"]) > 5e-5:
        halt("sample percentages do not reproduce offsurface.json")
    if abs(a["median"] - REC_SAMPLE["median"]) > 1e-12 * max(1.0, REC_SAMPLE["median"]) \
       and abs(a["median"] - REC_SAMPLE["median"]) > 1e-12:
        halt(f"sample median {a['median']!r} != recorded {REC_SAMPLE['median']!r}")
    if abs(a["max_px"] - REC_SAMPLE["max_px"]) > 1e-6:
        halt(f"sample max {a['max_px']!r} px != recorded {REC_SAMPLE['max_px']!r}")
    print("[cons] ANCHOR A PASS - full classification agrees with the recorded sample "
          "to the recorded digits")
    rep["anchor_sample"] = a

    def excl(name, num_mask, den_mask, rec_pct):
        """Headline = num/den. Excluded = both restricted to on-surface (>1px)."""
        n0, d0 = int(num_mask.sum()), int(den_mask.sum())
        n1 = int((num_mask & on1).sum())
        d1 = int((den_mask & on1).sum())
        p0 = 100.0 * n0 / max(d0, 1)
        p1 = 100.0 * n1 / max(d1, 1)
        row = {"as_recorded": {"num": n0, "den": d0, "pct": round(p0, 4)},
               "excluded": {"num": n1, "den": d1, "pct": round(p1, 4)},
               "num_off_surface": n0 - n1,
               "delta_pct_points": round(p1 - p0, 4),
               "recorded_quote": rec_pct}
        print(f"[cons] {name}: {n0:,}/{d0:,} = {p0:.4f}%  ->  excluded "
              f"{n1:,}/{d1:,} = {p1:.4f}%   (num loses {n0-n1:,}; "
              f"delta {p1-p0:+.4f} pts; quoted {rec_pct})")
        return row

    # ---- CONSUMER 1: e08_ceiling (42.72%) -------------------------------------------
    # THE SHIP'S RULED FLOORS ARE UNIFORM 0.45: ship.json pins head-facing-min equal to
    # facing-min on purpose ("a ship has no head, so the band must grant no looser
    # acceptance than the body" - Ruling 14), and the recorded 1,329,359 is that
    # configuration - a first replica at W3's production split (0.45/0.18) reached
    # +67,172 MORE, which is the head band's looser floor admitting texels the ship's
    # route never admits. The W3-lineage crop rect is inert here by the same ruling.
    print("\n[cons] CONSUMER 1 - e08_ceiling replica (uniform 0.45, the ship's ruled "
          "floors, 8 equatorial cameras)", flush=True)
    fmin = 0.45
    BIAS, NOFFS = 3e-3, 1.5e-3

    def dtc_of(yaw_d, el_d=0.0):
        th, el = np.radians(yaw_d), np.radians(el_d)
        cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
        return cd / np.linalg.norm(cd)

    if not np.allclose(dtc_of(0.0), [0.0, -1.0, 0.0]):
        halt("camera generalisation does not reproduce project_twins' front")

    R = np.zeros(NV, dtype=bool)
    for yaw in [i * 45.0 for i in range(8)]:
        dtc = dtc_of(yaw)
        facing = N @ dtc
        idx = np.where(facing > fmin)[0]
        org = (P[idx] + N[idx] * NOFFS + dtc[None, :] * BIAS).astype(np.float32)
        t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org, np.broadcast_to(dtc.astype(np.float32), org.shape)],
            axis=1)))["t_hit"].numpy()
        R[idx[~np.isfinite(t)]] = True
    print(f"[cons] ANCHOR B: replica reachable {R.sum():,} (recorded {REC_CEILING_REACH:,})")
    if int(R.sum()) != REC_CEILING_REACH:
        halt("ceiling replica does not reproduce the recorded reachable count")
    rep["ceiling"] = excl("e08_ceiling  reach/valid", R, np.ones(NV, dtype=bool), "42.72")
    rep["ceiling"]["off_surface_reach_rate_pct"] = round(
        float(100.0 * (R & off1).sum() / max(int(off1.sum()), 1)), 4)

    # ---- Class reconstruction + ANCHOR C1 -------------------------------------------
    print("\n[cons] class reconstruction from native sidecars", flush=True)
    s1 = np.load(J(STAGE1, "stage1_8cam_styled_mask.npy")).reshape(-1)[vidx].astype(bool)
    fin = np.load(J(STROKE, "state", "styled_mask.npy")).reshape(-1)[vidx].astype(bool)
    brush = fin & ~s1
    dil = ~fin
    counts = (int(s1.sum()), int(brush.sum()), int(dil.sum()), int(fin.sum()))
    print(f"[cons] ANCHOR C1: stage1 {counts[0]:,} (rec {REC_STAGE1:,})  brush "
          f"{counts[1]:,} (rec {REC_BRUSH:,})  dilation {counts[2]:,} "
          f"(rec {REC_DILATION:,})  painted {counts[3]:,} (rec {REC_PAINTED:,})")
    if counts[:3] != (REC_STAGE1, REC_BRUSH, REC_DILATION) or counts[3] != REC_PAINTED:
        halt("class reconstruction does not reproduce provenance.json")

    ones = np.ones(NV, dtype=bool)
    print("\n[cons] CONSUMER 2 - e08_acceptance (the quoted acceptance figures)")
    rep["acceptance_styled_over_valid"] = excl("acceptance styled/valid", s1, ones, "36.89")
    rep["acceptance_styled_over_reachable"] = excl("acceptance styled/reachable", s1, R, "86.4")

    print("\n[cons] CONSUMER 3 - texpass_finalize (the 56.24% flood)")
    print("[cons]   scoping fact: the shipped galleon finalize ran mode atlas_flood - "
          "the pos.npy branch (surface-aware, line 82) did not execute on this asset")
    rep["finalize_dilation"] = excl("finalize dilation/valid", dil, ones, "56.24")

    print("\n[cons] CONSUMER 4 - project_twins (stage-1 commit)")
    rep["twins_stage1"] = excl("project_twins stage1/valid", s1, ones, "36.89")

    print("\n[cons] CONSUMER 5 - texpass_iter commit (per-stroke counts)")
    rep["brush_total"] = excl("brush total/valid", brush, ones, "6.87")
    if args.claim:
        claim = np.load(args.claim).reshape(-1)[vidx]
        per = {}
        anchored = True
        for i, key in enumerate(STROKE_ORDER, start=1):
            c = int((claim == i).sum())
            ok = (c == REC_PER_STROKE[key])
            anchored &= ok
            per[key] = {"replayed": c, "recorded": REC_PER_STROKE[key], "anchored": ok}
            print(f"[cons] ANCHOR C2 stroke {i} {key}: replay {c:,} vs recorded "
                  f"{REC_PER_STROKE[key]:,}  {'OK' if ok else 'MISMATCH'}")
        rep["per_stroke_anchor"] = per
        if anchored:
            tbl = {}
            for i, key in enumerate(STROKE_ORDER, start=1):
                smask = claim == i
                n0 = int(smask.sum())
                n1 = int((smask & on1).sum())
                tbl[key] = {"recorded": n0, "excluded": n1, "off_surface": n0 - n1,
                            "off_pct_of_stroke": round(100.0 * (n0 - n1) / max(n0, 1), 4)}
                print(f"[cons]   stroke {i} {key}: {n0:,} -> {n1:,} "
                      f"(loses {n0-n1:,} = {100.0*(n0-n1)/max(n0,1):.4f}%)")
            rep["per_stroke_excluded"] = tbl
        else:
            print("[cons]   per-stroke exclusion NOT computed - replay is not anchored; "
                  "reported as a limit, nothing substituted")
    else:
        print("[cons]   no --claim given: per-stroke exclusion skipped this pass")

    # ---- P0: where the off-surface population lives ---------------------------------
    print("\n[cons] off-surface (>1px) population composition by provenance class")
    comp = {}
    for lab, sel in [("stage1", s1), ("brush", brush), ("dilation", dil)]:
        n = int((sel & off1).sum())
        comp[lab] = {"texels": n, "share_of_off_surface":
                     round(100.0 * n / max(int(off1.sum()), 1), 4)}
        print(f"[cons]   {lab:<9s} {n:>7,}  ({100.0*n/max(int(off1.sum()),1):6.2f}% "
              f"of the off-surface population)")
    rep["off_surface_composition"] = comp

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(rep, open(args.out, "w"), indent=1)
    print(f"\n[json] {args.out}")
    print("Reported, not ruled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
