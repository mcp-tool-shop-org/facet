"""E04 Arm T — the twin baseline. Measure, report, no bound anywhere.

Every gate this arm could carry is suspended by the spec and by `profiles/ship.json`
(`reg_iou_min: null` -> the tool receives 0.0, `bbox_tol` vacuous, both palette bounds null).
So this reports numerator and denominator per view and asserts nothing. The advisor rules.

Four blocks, all against the EXACT raycast silhouette rather than a keyed mask — the frame
now matches, which it did not on the 1064 batch:

  REGISTRATION  IoU and centroid offset between each twin's own painted figure and the mesh
                silhouette it must register to. Withheld from the previous report because a
                frame-edge mismatch corrupts precisely this number; reportable now.
  LANDING       the twelve declared elements against the measured clusters, per view, by
                e04_bands.py's machinery at its inherited thresholds.
  RED           G7's sub-40deg population per view — the arm's own question, on the fixed
                window whose upper edge predates the arm.
  WATCH         the key margin (fraction of silhouette at or under the key cut), the pale
                near-neutral cluster Ruling 8 banked, and thin-vs-bulk key-out enrichment
                (S2, whose element is G9).

  e04_twin_baseline.py --twins DIR --masks DIR --materials m.json --out DIR
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage

ap = argparse.ArgumentParser()
ap.add_argument("--twins", required=True)
ap.add_argument("--masks", required=True)
ap.add_argument("--materials", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--clusters", type=int, default=14)
ap.add_argument("--chroma-floor", type=float, default=12.0)
ap.add_argument("--seed", type=int, default=770700)
ap.add_argument("--key-cut", type=float, default=0.06, help="project_twins' keying tolerance")
ap.add_argument("--thin-px", type=int, default=2, help="<= this half-width counts as thin")
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)


def lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


def kmeans(X, k, seed):
    rng = np.random.default_rng(seed)
    cen = X[rng.choice(len(X), k, replace=False)].copy()
    li = np.zeros(len(X), dtype=np.int64)
    for _ in range(40):
        for s in range(0, len(X), 60000):
            e = min(s + 60000, len(X))
            li[s:e] = ((X[s:e, None, :] - cen[None, :, :]) ** 2).sum(-1).argmin(1)
        for j in range(k):
            m = li == j
            if m.any():
                cen[j] = X[m].mean(0)
    return cen, li


MATS = json.load(open(args.materials, encoding="utf-8"))["materials"]
VIEWS = [int(v) for v in args.views.split(",")]
out = {"views": {}}

print("REGISTRATION — twin's painted figure against the exact mesh silhouette")
print("view   sil px   twin px      IoU    centroid dx,dy px   bbox sil -> twin")
for v in VIEWS:
    im = np.asarray(Image.open(os.path.join(args.twins, "twin_%d.png" % v)
                               ).convert("RGB"), dtype=np.float32) / 255.0
    sil = np.asarray(Image.open(os.path.join(args.masks, "galleonclay_%d.png" % v)
                                ).convert("L")) > 127
    assert im.shape[:2] == sil.shape, "frame mismatch view %d" % v
    H, W = sil.shape
    ring = np.zeros((H, W), bool)
    ring[:6, :] = ring[-6:, :] = ring[:, :6] = ring[:, -6:] = True
    bg = np.median(im[ring], axis=0)
    dist = np.abs(im - bg[None, None, :]).max(-1)
    # THE RAW KEY, deliberately: no closing, NO FILL_HOLES. A first version filled holes and
    # returned IoU 0.632 on the broadside views against 0.844 here — because a rigged ship is
    # POROUS, and fill_holes swallows every patch of background enclosed by shrouds, ratlines
    # and yards: 464,282 px of "figure" against a 293,865 px silhouette, +58%. The collapse was
    # the morphology, not the registration. Closing alone moves IoU by <0.005 and is dropped as
    # well; "the twin's painted figure" means pixels that differ from the backdrop, and that is
    # what this is. Checked on all eight views before the number was believed.
    fig = dist > args.key_cut
    inter = (fig & sil).sum()
    iou = inter / max((fig | sil).sum(), 1)
    ys, xs = np.nonzero(sil)
    yf, xf = np.nonzero(fig)
    rec = {"sil_px": int(sil.sum()), "twin_px": int(fig.sum()), "iou": round(float(iou), 5),
           "centroid_dx": round(float(xf.mean() - xs.mean()), 2),
           "centroid_dy": round(float(yf.mean() - ys.mean()), 2),
           "sil_bbox_wh": [int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)],
           "twin_bbox_wh": [int(xf.max() - xf.min() + 1), int(yf.max() - yf.min() + 1)]}
    print("  %d %8d %9d  %8.5f   %+6.2f,%+6.2f    %dx%d -> %dx%d"
          % (v, rec["sil_px"], rec["twin_px"], iou, rec["centroid_dx"], rec["centroid_dy"],
             *rec["sil_bbox_wh"], *rec["twin_bbox_wh"]))

    # ---- colour work, inside the exact silhouette
    P = im[sil]
    L = lab(P)
    C = np.hypot(L[:, 1], L[:, 2])
    h = np.degrees(np.arctan2(L[:, 2], L[:, 1])) % 360
    cen, li = kmeans(L, args.clusters, args.seed)
    counts = np.bincount(li, minlength=args.clusters)
    land = []
    for m in MATS:
        exp = lab(np.array([[c / 255.0 for c in m["rgb"]]]))[0]
        dd = np.linalg.norm(cen - exp[None, :], axis=1)
        j = int(np.argmin(dd))
        land.append({"id": m["id"], "dE": round(float(dd[j]), 1),
                     "verdict": "LANDED" if dd[j] <= 25 else
                                ("NEAR" if dd[j] <= 40 else "NOT FOUND"),
                     "share_pct": round(100.0 * counts[j] / len(P), 2)})
    rec["landing"] = land
    rec["landed_n"] = sum(1 for r in land if r["verdict"] == "LANDED")
    rec["G7"] = [r for r in land if r["id"] == "G7"][0]
    rec["red_sub40_px"] = int(((C >= args.chroma_floor) & (h < 40)).sum())

    # ---- watch items
    rec["key_margin_pct"] = round(float(100.0 * (dist[sil] <= args.key_cut).mean()), 3)
    Ccl = np.hypot(cen[:, 1], cen[:, 2])
    pale = [(int(counts[j]), [int(round(x * 255)) for x in np.median(P[li == j], axis=0)])
            for j in range(args.clusters)
            if Ccl[j] < args.chroma_floor and cen[j][0] > 60]
    rec["pale_neutral"] = (max(pale)[1] if pale else None)
    rec["pale_neutral_pct"] = round(100.0 * max(pale)[0] / len(P), 2) if pale else 0.0
    if pale:
        pj = int(np.argmax([counts[j] if (Ccl[j] < args.chroma_floor and cen[j][0] > 60)
                            else -1 for j in range(args.clusters)]))
        rec["pale_neutral_dist_to_bg"] = round(
            float(np.abs(np.median(P[li == pj], axis=0) - bg).max()), 4)

    # thin vs bulk key-out (S2 / G9)
    dt = ndimage.distance_transform_edt(sil)
    thin = sil.copy()
    thin[sil] = dt[sil] <= args.thin_px
    bulk = sil & ~thin
    ko = np.zeros(sil.shape, bool)
    ko[sil] = dist[sil] <= args.key_cut
    rec["thin_keyout_pct"] = round(float(100.0 * ko[thin].mean()), 2) if thin.any() else None
    rec["bulk_keyout_pct"] = round(float(100.0 * ko[bulk].mean()), 2) if bulk.any() else None
    rec["thin_enrichment"] = (round(rec["thin_keyout_pct"] / rec["bulk_keyout_pct"], 2)
                              if rec["bulk_keyout_pct"] else None)
    out["views"][str(v)] = rec

print("\nLANDING / RED / WATCH — per view, no bound anywhere")
print("view  landed/12   G7 dE  G7 verdict   red<40deg px   key margin%   "
      "thin/bulk keyout%   enrich")
for v in VIEWS:
    r = out["views"][str(v)]
    print("  %d      %2d/12  %6.1f  %-10s %10d %12.3f   %5.2f / %-5.2f      %s"
          % (v, r["landed_n"], r["G7"]["dE"], r["G7"]["verdict"], r["red_sub40_px"],
             r["key_margin_pct"], r["thin_keyout_pct"], r["bulk_keyout_pct"],
             r["thin_enrichment"]))

print("\nPALE NEAR-NEUTRAL CLUSTER (Ruling 8's watch item) — the tightest margin on the pair")
print("view    rgb            share%   max-channel distance to the realised backdrop")
for v in VIEWS:
    r = out["views"][str(v)]
    print("  %d    %-16s %6.2f   %s" % (v, str(r["pale_neutral"]), r["pale_neutral_pct"],
                                        r.get("pale_neutral_dist_to_bg")))

json.dump(out, open(os.path.join(args.out, "twin_baseline.json"), "w"), indent=1)
print("\nwrote %s" % os.path.join(args.out, "twin_baseline.json"))
