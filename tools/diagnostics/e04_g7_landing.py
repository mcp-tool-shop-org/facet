"""E04 Arm G7 - did `red gun port lids` land where `red-lined gun port lids` missed?

A single-view A/B on two images that differ by one word in the prompt and by nothing else:
same control, same init latent, same seed, same sampler, same LoRA. Both cloud uploads are
content-addressed and came back under the filenames already in the pair's saved workflow, so
the two inputs are byte-identical rather than assumed so.

The instrument is `e04_bands.py`'s, run PER IMAGE instead of over the two-view pair, because
this arm is a within-view comparison and a shared cluster space would let one side's colours
define the other's bins. Its inherited thresholds are used unchanged - LANDED at dE <= 25,
chroma floor C* 12.0, k = 14, seed 770700 - so nothing here was chosen while looking at a
result.

Three readings, pre-registered in docs/experiments/E04-g7-predictions.md before the AFTER
image existed:

  LANDING   per image, every declared element against its nearest measured cluster. G7's row
            is the arm; the other eleven are the control that says whether one word knocked
            anything else out.
  RED       a cluster-independent pixel count: C* >= 12 and hue in [350,360) u [0,50). The 50
            edge is the pair's own measured warm-band lower edge (62) minus the 4d band
            convention's 10, floored - data that existed before this arm was designed. A
            cluster table can miss a small feature that this cannot, and vice versa.
  PLACEMENT the red set's centroid and bbox against the silhouette's, because the landing
            table measures colour and not where it landed. The crop sheet is what answers
            placement; the Director's eye is what rules on it.

  e04_g7_landing.py --before B.png --after A.png --mask M.png --materials m.json --out DIR

Standards compliance: PIN_PER_STEP - every threshold is inherited or derived from data that
predates the arm, and the seed is fixed. ANDON_AUTHORITY - the script reports numerator and
denominator for every reading and asserts no pass; the verdict is the advisor's.
EXTERNAL_VERIFIER - the cluster table is derived from the image rather than the expectation,
so an element can fail to appear, and one already has.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--before", required=True)
ap.add_argument("--after", required=True)
ap.add_argument("--mask", required=True)
ap.add_argument("--materials", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--clusters", type=int, default=14)
ap.add_argument("--chroma-floor", type=float, default=12.0,
                help="INHERITED from W3's palette fixture via e04_bands.py.")
ap.add_argument("--seed", type=int, default=770700)
ap.add_argument("--red-hue-lo", type=float, default=350.0)
ap.add_argument("--red-hue-hi", type=float, default=50.0,
                help="Wraps through 0. Upper edge = the pair's measured warm-band lower edge "
                     "62 minus the 4d band convention's 10, floored to 50.")
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


def lch(L):
    C = np.hypot(L[..., 1], L[..., 2])
    h = np.degrees(np.arctan2(L[..., 2], L[..., 1])) % 360
    return L[..., 0], C, h


def kmeans(X, k, seed):
    rng = np.random.default_rng(seed)
    cen = X[rng.choice(len(X), k, replace=False)].copy()
    lab_i = np.zeros(len(X), dtype=np.int64)
    for _ in range(40):
        for s in range(0, len(X), 60000):
            e = min(s + 60000, len(X))
            lab_i[s:e] = ((X[s:e, None, :] - cen[None, :, :]) ** 2).sum(-1).argmin(1)
        for j in range(k):
            m = lab_i == j
            if m.any():
                cen[j] = X[m].mean(0)
    return cen, lab_i


MATS = json.load(open(args.materials, encoding="utf-8"))["materials"]
SIL = np.asarray(Image.open(args.mask).convert("L")) > 127
ys, xs = np.nonzero(SIL)
SIL_BBOX = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
print("[G7] silhouette: %d px, bbox x %d-%d  y %d-%d"
      % (SIL.sum(), SIL_BBOX[0], SIL_BBOX[2], SIL_BBOX[1], SIL_BBOX[3]), flush=True)

out = {"silhouette_px": int(SIL.sum()), "silhouette_bbox_xyxy": list(SIL_BBOX),
       "chroma_floor": args.chroma_floor, "clusters": args.clusters, "seed": args.seed,
       "red_hue_window": [args.red_hue_lo, args.red_hue_hi], "arms": {}}
imgs, sets = {}, {}

for tag, path in (("before", args.before), ("after", args.after)):
    im = np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0
    assert im.shape[:2] == SIL.shape, "%s is %s, mask is %s" % (tag, im.shape[:2], SIL.shape)
    imgs[tag] = im
    P = im[SIL]
    X = lab(P)
    cen, lab_i = kmeans(X, args.clusters, args.seed)
    counts = np.bincount(lab_i, minlength=args.clusters)
    L_, C_, h_ = lch(cen)

    print("\n[G7] %s - clusters inside the exact silhouette:" % tag.upper(), flush=True)
    clusters = []
    for j in np.argsort(counts)[::-1]:
        if counts[j] < len(X) * 0.004:
            continue
        srgb = np.median(P[lab_i == j], axis=0)
        clusters.append({"idx": int(j), "share_pct": round(100.0 * counts[j] / len(X), 2),
                         "rgb255": [int(round(v * 255)) for v in srgb],
                         "L": round(float(L_[j]), 1), "C": round(float(C_[j]), 1),
                         "h": round(float(h_[j]), 1)})
        print("[G7]   %5.2f%%  rgb(%3d,%3d,%3d)  L* %5.1f  C* %5.1f  h %5.1f%s"
              % (clusters[-1]["share_pct"], *clusters[-1]["rgb255"], L_[j], C_[j], h_[j],
                 "   <- below chroma floor, hue undefined" if C_[j] < args.chroma_floor else ""),
              flush=True)

    print("\n[G7] %s - LANDING TABLE (dE <= 25 LANDED, <= 40 NEAR, else NOT FOUND):"
          % tag.upper(), flush=True)
    land = []
    for m in MATS:
        exp = lab(np.array([[c / 255.0 for c in m["rgb"]]]))[0]
        dd = np.linalg.norm(cen - exp[None, :], axis=1)
        j = int(np.argmin(dd))
        verdict = "LANDED" if dd[j] <= 25 else ("NEAR" if dd[j] <= 40 else "NOT FOUND")
        land.append({"id": m["id"], "name": m["name"], "dE": round(float(dd[j]), 1),
                     "verdict": verdict,
                     "nearest_cluster_rgb255": [int(round(v * 255))
                                                for v in np.median(P[lab_i == j], axis=0)],
                     "nearest_cluster_C": round(float(C_[j]), 1),
                     "nearest_cluster_h": round(float(h_[j]), 1),
                     "share_pct": round(100.0 * counts[j] / len(X), 2)})
        print("[G7]   %-4s %-34s dE %5.1f  %-9s  nearest rgb(%3d,%3d,%3d) C* %5.1f h %5.1f  "
              "%5.2f%%" % (m["id"], m["name"][:34], dd[j], verdict,
                           *land[-1]["nearest_cluster_rgb255"], C_[j], h_[j],
                           land[-1]["share_pct"]), flush=True)

    floor = min([r["share_pct"] for r in land if r["verdict"] == "LANDED"], default=None)
    print("[G7]   element floor on %s (smallest share carrying a LANDED element): %s%%"
          % (tag, floor), flush=True)

    # ---- cluster-independent red count
    Lp, Cp, hp = lch(lab(P))
    red = (Cp >= args.chroma_floor) & ((hp >= args.red_hue_lo) | (hp < args.red_hue_hi))
    full = np.zeros(SIL.shape, dtype=bool)
    full[SIL] = red
    sets[tag] = full
    rec = {"clusters": clusters, "landing": land, "element_floor_pct": floor,
           "red_window_px": int(red.sum()),
           "red_window_pct": round(100.0 * red.sum() / len(P), 3)}
    if red.any():
        ry, rx = np.nonzero(full)
        rec["red_bbox_xyxy"] = [int(rx.min()), int(ry.min()), int(rx.max()), int(ry.max())]
        rec["red_centroid_xy"] = [round(float(rx.mean()), 1), round(float(ry.mean()), 1)]
        rec["red_median_rgb255"] = [int(round(v * 255)) for v in np.median(P[red], axis=0)]
        rec["red_median_C"] = round(float(np.median(Cp[red])), 1)
        rec["red_median_h"] = round(float(np.median(hp[red])), 1)
    print("[G7]   red window (C* >= %.0f, h in [%.0f,360) u [0,%.0f)): %d px = %.3f%% of "
          "silhouette" % (args.chroma_floor, args.red_hue_lo, args.red_hue_hi,
                          red.sum(), 100.0 * red.sum() / len(P)), flush=True)
    if red.any():
        print("[G7]   red set: centroid (%.1f, %.1f), bbox x %d-%d y %d-%d, median rgb(%d,%d,%d)"
              " C* %.1f h %.1f"
              % (*rec["red_centroid_xy"], rec["red_bbox_xyxy"][0], rec["red_bbox_xyxy"][2],
                 rec["red_bbox_xyxy"][1], rec["red_bbox_xyxy"][3], *rec["red_median_rgb255"],
                 rec["red_median_C"], rec["red_median_h"]), flush=True)
    out["arms"][tag] = rec

# ---- what one word did to everything else
dE = np.linalg.norm(lab(imgs["after"]) - lab(imgs["before"]), axis=-1)
inside = dE[SIL]
notred = dE[SIL & ~sets["after"]]
out["repaint"] = {
    "median_dE_silhouette": round(float(np.median(inside)), 2),
    "mean_dE_silhouette": round(float(inside.mean()), 2),
    "median_dE_outside_red_set": round(float(np.median(notred)), 2),
    "p90_dE_silhouette": round(float(np.percentile(inside, 90)), 2),
    "e08_contradiction_held_median": 6.23}
print("\n[G7] WHAT ONE WORD DID TO THE REST OF THE SHIP", flush=True)
print("[G7]   median dE inside silhouette          %6.2f" % np.median(inside), flush=True)
print("[G7]   median dE outside the AFTER red set  %6.2f   (E08 8-element held: 6.23)"
      % np.median(notred), flush=True)
print("[G7]   mean %5.2f   p90 %5.2f" % (inside.mean(), np.percentile(inside, 90)), flush=True)

json.dump(out, open(os.path.join(args.out, "g7_landing.json"), "w"), indent=1)
np.save(os.path.join(args.out, "red_mask_after.npy"), sets["after"])
np.save(os.path.join(args.out, "red_mask_before.npy"), sets["before"])
print("\n[G7] wrote %s" % os.path.join(args.out, "g7_landing.json"), flush=True)
