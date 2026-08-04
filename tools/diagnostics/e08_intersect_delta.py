"""E08 Amendment 26 — what the trust-mask intersection actually moved.

Reads two `project_twins --diag-npz` dumps (flag off, flag on) and decomposes the
difference. A swap is not a gain until you have looked at what left, so gains and losses are
counted separately and characterised, never netted.

Three things it reports that a styled count cannot:

  1. GAIN / LOSS, per view and unioned. With `ed` fixed, a pure mask intersection can only
     lose — `dist_in` of a subset mask is pointwise <= the original — so a nonzero gain is a
     correctness signal about the implementation, not a finding about the subject.
  2. WHERE the losses sit: by R0 edge distance, by local half-width, and by height in the
     twin frame, because "near ground contact" is a claim that has to be measured.
  3. The `dist_in` DELTA FIELD inside the silhouette — the direct analogue of the halt
     report's 27.49% / 21.24% / 36.22px on view 6, computed here for the adopted pair.

  e08_intersect_delta.py --r0 diag_R0.npz --r1 diag_R1.npz [--sheet out.png] [--out-json j]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, label

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--r0", required=True)
ap.add_argument("--r1", required=True)
ap.add_argument("--sheet")
ap.add_argument("--out-json")
args = ap.parse_args()

Z0 = np.load(args.r0, allow_pickle=False)
Z1 = np.load(args.r1, allow_pickle=False)
views = [str(x) for x in Z0["__views__"]]
assert views == [str(x) for x in Z1["__views__"]], "ANDON: view lists differ"
assert not bool(Z0["__trust_intersect__"]), "ANDON: --r0 was run WITH --trust-intersect"
assert bool(Z1["__trust_intersect__"]), "ANDON: --r1 was run WITHOUT --trust-intersect"

NV = int(Z0["__valid__"])
s0, s1 = Z0["__styled__"], Z1["__styled__"]
out = {"valid": NV,
       "R0": {"styled": int(s0.sum()), "variance": float(Z0["__variance__"]),
              "holes": int(Z0["__holes__"]),
              "reachable": int(Z0["__reachable__"].sum())},
       "R1": {"styled": int(s1.sum()), "variance": float(Z1["__variance__"]),
              "holes": int(Z1["__holes__"]),
              "reachable": int(Z1["__reachable__"].sum())},
       "views": {}}

print("=" * 78)
print("UNION")
print("=" * 78)
g_u = int((s1 & ~s0).sum())
l_u = int((s0 & ~s1).sum())
print(f"  R0 styled {int(s0.sum()):>9,}   R1 styled {int(s1.sum()):>9,}   "
      f"net {int(s1.sum()) - int(s0.sum()):+,}")
print(f"  GAINED (R1 not R0) {g_u:>9,}      LOST (R0 not R1) {l_u:>9,}")
print(f"  reachable R0 {int(Z0['__reachable__'].sum()):,} == R1 "
      f"{int(Z1['__reachable__'].sum()):,}: "
      f"{int(Z0['__reachable__'].sum()) == int(Z1['__reachable__'].sum())}")
print(f"  variance {float(Z0['__variance__']):.5f} -> {float(Z1['__variance__']):.5f}   "
       f"holes {int(Z0['__holes__']):,} -> {int(Z1['__holes__']):,} "
       f"({int(Z1['__holes__']) - int(Z0['__holes__']):+,})")
out["union"] = {"gained": g_u, "lost": l_u,
                "net": int(s1.sum()) - int(s0.sum()),
                "reachable_identical": int(Z0["__reachable__"].sum())
                == int(Z1["__reachable__"].sum())}

STRATA = ((0, 4), (4, 8), (8, 16), (16, 32), (32, 1e9))
panels = []
for nm in views:
    print("\n" + "=" * 78)
    print(f"VIEW {nm}")
    print("=" * 78)
    c0, c1 = Z0[f"{nm}/cand_idx"], Z1[f"{nm}/cand_idx"]
    assert np.array_equal(c0, c1), (
        f"ANDON: {nm}: the candidate set moved. facing+visibility must be identical "
        f"across arms — the flag is not supposed to touch them.")
    a0, a1 = Z0[f"{nm}/accepted"], Z1[f"{nm}/accepted"]
    d0, d1 = Z0[f"{nm}/d_s"], Z1[f"{nm}/d_s"]
    ed0, ed1 = Z0[f"{nm}/ed"], Z1[f"{nm}/ed"]
    th0 = Z0[f"{nm}/thick_s"]
    D0, D1 = Z0[f"{nm}/dist_in"], Z1[f"{nm}/dist_in"]
    mesh = Z0[f"{nm}/mesh_fm"]
    twin = Z0[f"{nm}/twin_fm"]
    assert np.array_equal(mesh, Z1[f"{nm}/mesh_fm"]), f"ANDON: {nm}: mesh_fm moved"
    assert np.array_equal(twin, Z1[f"{nm}/twin_fm"]), f"ANDON: {nm}: twin_fm moved"

    print(f"  fig_w   raw {float(Z0[f'{nm}/fig_w_raw']):.0f}px   "
          f"R0 used {float(Z0[f'{nm}/fig_w']):.0f}px   "
          f"R1 used {float(Z1[f'{nm}/fig_w']):.0f}px")
    print(f"  ed(body) R0 {float(np.max(ed0)):.2f}px   R1 {float(np.max(ed1)):.2f}px   "
          f"identical: {np.array_equal(ed0, ed1)}")
    bt, bm = Z0[f"{nm}/bbox_twin"], Z0[f"{nm}/bbox_mesh"]
    print(f"  raw bbox twin {int(bt[0])}x{int(bt[1])}   mesh {int(bm[0])}x{int(bm[1])}   "
          f"IoU(twin,mesh) {float(Z0[f'{nm}/iou_tm']):.4f}   centroid "
          f"dx {float(Z0[f'{nm}/centroid_off'][0]):+.1f} "
          f"dy {float(Z0[f'{nm}/centroid_off'][1]):+.1f}px")
    print(f"  keyed OUTSIDE the silhouette {int(Z0[f'{nm}/outside_px']):,}px  "
          f"largest component {int(Z0[f'{nm}/outside_cc']):,}px")

    # ---- dist_in delta INSIDE the silhouette: the view-6 analogue
    dd = D0 - D1                       # >= 0 pointwise if the intersection is a subset op
    ins = mesh
    n_ins = int(ins.sum())
    neg = int((dd[ins] < -1e-6).sum())
    row_d = {}
    for t in (0.5, 2.0):
        n = int((dd[ins] > t).sum())
        row_d[f"changed_gt_{t}px"] = n
        print(f"  dist_in inside silhouette: changed > {t:>3}px  {n:>8,} of {n_ins:,}  "
              f"{n / max(n_ins, 1) * 100:5.2f}%")
    row_d["max_change_px"] = round(float(dd[ins].max()), 2)
    row_d["inside_silhouette_px"] = n_ins
    row_d["increases_px"] = neg
    print(f"  dist_in inside silhouette: max change {float(dd[ins].max()):.2f}px   "
          f"pixels where dist_in INCREASED: {neg:,} "
          f"(a subset intersection cannot increase it; nonzero = bug)")

    # ---- gain / loss for this view
    gained = a1 & ~a0
    lost = a0 & ~a1
    ng, nl = int(gained.sum()), int(lost.sum())
    print(f"\n  accepted R0 {int(a0.sum()):,}  R1 {int(a1.sum()):,}  "
          f"net {int(a1.sum()) - int(a0.sum()):+,}")
    print(f"  GAINED {ng:,}   LOST {nl:,}")

    row = {"fig_w_raw": float(Z0[f"{nm}/fig_w_raw"]),
           "fig_w_R0": float(Z0[f"{nm}/fig_w"]),
           "fig_w_R1": float(Z1[f"{nm}/fig_w"]),
           "ed_body_R0": round(float(np.max(ed0)), 3),
           "ed_body_R1": round(float(np.max(ed1)), 3),
           "ed_identical": bool(np.array_equal(ed0, ed1)),
           "bbox_twin": [int(bt[0]), int(bt[1])],
           "bbox_mesh": [int(bm[0]), int(bm[1])],
           "iou_twin_mesh": round(float(Z0[f"{nm}/iou_tm"]), 4),
           "centroid_offset_px": [round(float(Z0[f"{nm}/centroid_off"][0]), 2),
                                  round(float(Z0[f"{nm}/centroid_off"][1]), 2)],
           "keyed_outside_px": int(Z0[f"{nm}/outside_px"]),
           "keyed_outside_largest_cc_px": int(Z0[f"{nm}/outside_cc"]),
           "dist_in_delta": row_d,
           "accepted_R0": int(a0.sum()), "accepted_R1": int(a1.sum()),
           "gained": ng, "lost": nl}

    # ---- characterise the losses: by R0 edge distance, half-width, and height
    if nl:
        dl = d0[lost]
        print(f"  lost samples' R0 edge distance: median {np.median(dl):.2f}px  "
              f"p90 {np.percentile(dl, 90):.2f}px  max {dl.max():.2f}px  "
              f"(threshold was {float(np.max(ed0)):.2f}px)")
        print(f"  losses by R0 edge distance above the threshold:")
        bands = ((0.0, 0.5), (0.5, 1.0), (1.0, 2.0), (2.0, 4.0), (4.0, 1e9))
        excess = dl - ed0[lost]
        by_x = {}
        for a_, b_ in bands:
            n = int(((excess >= a_) & (excess < b_)).sum())
            by_x[f"{a_}-{'inf' if b_ > 1e8 else b_}px"] = n
            print(f"      excess {a_:>4}-{'inf' if b_ > 1e8 else b_:<4} px  {n:>8,}  "
                  f"{n / nl * 100:5.1f}%")
        row["lost_by_edge_excess"] = by_x
        row["lost_edge_dist_R0"] = {"median": round(float(np.median(dl)), 2),
                                    "p90": round(float(np.percentile(dl, 90)), 2),
                                    "max": round(float(dl.max()), 2)}
        by_t = {}
        print(f"  losses by LOCAL HALF-WIDTH (R0 field):")
        for a_, b_ in STRATA:
            sel = (th0[lost] >= a_) & (th0[lost] < b_)
            n = int(sel.sum())
            tot = int(((th0 >= a_) & (th0 < b_) & a0).sum())
            by_t[f"{a_}-{'inf' if b_ > 1e8 else b_}px"] = {
                "lost": n, "accepted_R0_in_stratum": tot,
                "pct_of_stratum": round(n / max(tot, 1) * 100, 2)}
            print(f"      half-width {a_:>3}-{'inf' if b_ > 1e8 else b_:<4}px  lost "
                  f"{n:>8,} of {tot:>9,} accepted in R0  {n / max(tot, 1) * 100:5.2f}%")
        row["lost_by_half_width"] = by_t
        # WHERE the losses sit, measured rather than inferred from a picture. Two
        # questions, because the sheet suggested the answer to the second is not the
        # obvious one: how high in the figure, and how far from the paint that was
        # removed. If the losses are not local to the removed region, the mechanism is
        # not "the shadow" and saying so would be wrong.
        ys_m = np.where(mesh.any(axis=1))[0]
        y0, y1 = int(ys_m.min()), int(ys_m.max())
        rem = twin & ~mesh
        pyl = Z0[f"{nm}/py"][lost]
        pxl = Z0[f"{nm}/px"][lost]
        hf = (pyl - y0) / max(y1 - y0, 1)
        print(f"  lost samples' height in the figure (0 = crown, 1 = sole): "
              f"median {float(np.median(hf)):.3f}   "
              f"in bottom decile {float((hf > 0.9).mean()) * 100:.1f}%   "
              f"in bottom third {float((hf > 0.667).mean()) * 100:.1f}%")
        # distance from each lost sample to the nearest REMOVED pixel
        dr = distance_transform_edt(~rem).astype(np.float32)
        pyi = np.clip(pyl.round().astype(int), 0, mesh.shape[0] - 1)
        pxi = np.clip(pxl.round().astype(int), 0, mesh.shape[1] - 1)
        dl_rem = dr[pyi, pxi]
        print(f"  lost samples' distance to the nearest REMOVED pixel: "
              f"median {float(np.median(dl_rem)):.1f}px   "
              f"within 5px {float((dl_rem <= 5).mean()) * 100:.1f}%   "
              f"within 20px {float((dl_rem <= 20).mean()) * 100:.1f}%   "
              f"max {float(dl_rem.max()):.0f}px")
        chg = ((D0 - D1) > 0.5) & mesh
        dc = dr[chg]
        print(f"  dist_in-changed silhouette pixels' distance to nearest REMOVED pixel: "
              f"median {float(np.median(dc)):.1f}px   within 5px "
              f"{float((dc <= 5).mean()) * 100:.1f}%   max {float(dc.max()):.0f}px")
        row["lost_location"] = {
            "height_fraction_median": round(float(np.median(hf)), 3),
            "pct_bottom_decile": round(float((hf > 0.9).mean()) * 100, 1),
            "pct_bottom_third": round(float((hf > 0.667).mean()) * 100, 1),
            "dist_to_removed_median_px": round(float(np.median(dl_rem)), 1),
            "dist_to_removed_within_5px_pct": round(float((dl_rem <= 5).mean()) * 100, 1),
            "dist_to_removed_within_20px_pct": round(float((dl_rem <= 20).mean()) * 100, 1),
            "dist_to_removed_max_px": round(float(dl_rem.max()), 0),
            "changed_px_dist_to_removed_median_px": round(float(np.median(dc)), 1),
            "changed_px_within_5px_pct": round(float((dc <= 5).mean()) * 100, 1)}
        ys_r = np.where(rem.any(axis=1))[0]
        frac_lo = (np.where(rem)[0] - y0) / max(y1 - y0, 1)
        print(f"  removed region spans y {int(ys_r.min())}-{int(ys_r.max())} "
              f"(silhouette y {y0}-{y1}); "
              f"{float((frac_lo > 0.9).mean()) * 100:.1f}% of it in the bottom decile "
              f"of the figure, median height fraction {float(np.median(frac_lo)):.3f}")
        row["removed_region"] = {
            "y_span": [int(ys_r.min()), int(ys_r.max())],
            "silhouette_y_span": [y0, y1],
            "pct_in_bottom_decile": round(float((frac_lo > 0.9).mean()) * 100, 1),
            "median_height_fraction": round(float(np.median(frac_lo)), 3)}
        lab_r, n_r = label(rem)
        if n_r:
            sizes = np.bincount(lab_r.ravel())[1:]
            print(f"  removed region components: {n_r} "
                  f"({', '.join(f'{int(s):,}' for s in np.sort(sizes)[::-1][:5])} ...)")
            row["removed_region"]["n_components"] = int(n_r)
            row["removed_region"]["top_components"] = [
                int(s) for s in np.sort(sizes)[::-1][:5]]
    if ng:
        dg = d1[gained]
        print(f"  ⚠ GAINED {ng:,} samples with ed identical "
              f"({np.array_equal(ed0, ed1)}) — median R1 edge distance "
              f"{np.median(dg):.2f}px. With a subset mask and a fixed threshold this "
              f"should be impossible; investigate before reading any other number.")
        row["gained_edge_dist_R1_median"] = round(float(np.median(dg)), 2)

    out["views"][nm] = row

    if args.sheet:
        H, W = mesh.shape
        p = np.zeros((H, W, 3), dtype=np.uint8)
        p[mesh] = (60, 60, 66)
        p[twin & ~mesh] = (255, 40, 200)        # keyed paint on NO surface -> removed
        p[mesh & ~twin] = (40, 160, 255)        # surface the twin never painted
        dmask = (D0 - D1) > 0.5
        p[dmask & mesh] = (255, 190, 40)        # real surface whose edge distance moved
        panels.append(p)

if args.sheet and panels:
    sheet = np.concatenate(panels, axis=1)
    os.makedirs(os.path.dirname(os.path.abspath(args.sheet)), exist_ok=True)
    Image.fromarray(sheet).save(args.sheet)
    print(f"\n[delta] wrote {args.sheet}")
    print(f"[delta]   grey = silhouette · MAGENTA = keyed paint on no surface (removed) · "
          f"blue = surface the twin never painted · YELLOW = real surface whose edge "
          f"distance moved > 0.5px")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"[delta] wrote {args.out_json}")
