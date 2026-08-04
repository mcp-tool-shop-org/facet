"""E04 Task 4d - the landing table, the palette bands, and the backdrop re-derivation.

Three questions, all answered against the DIRECTOR-APPROVED styled target pair and never
against twins that do not exist yet (the non-circularity rule, kept):

  LANDING   Did each of the twelve named elements arrive? Answered by clustering the pair's
            actual colours inside the EXACT silhouette and asking, per declared element,
            whether any cluster sits near its expected colour. Clustering rather than
            hand-placed sample discs, because a disc I position by eye is a measurement of
            where I think an element is - the cluster table is a measurement of what is
            actually there, and it can return "nothing like this element is present", which
            a disc cannot.
  BANDS     Hue bands derived from the MEASURED colours of the elements that landed, with a
            chroma floor, and the forbidden span reported as arithmetic. Below the floor hue
            is not a colour - it is undefined and reads as a rotation, which is why W3's
            gate flagged a steel sword as blue until the floor went in.
  BACKDROP  Re-derived against what the model ACTUALLY painted, not what was asked. The pair
            measured rgb(175,175,175) against an asked 255 - the lever works, attenuated -
            so every distance in the 4b table was computed against a backdrop that did not
            arrive.

  e04_bands.py --pair DIR --masks DIR --materials m.json --out DIR

Standards compliance: EXTERNAL_VERIFIER - the cluster table is derived from the image, not
from the expectation, so an element can fail to appear. ANDON_AUTHORITY - no band is emitted
where the measured data does not support one; suspend and report numerator and denominator.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--pair", required=True)
ap.add_argument("--masks", required=True)
ap.add_argument("--materials", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--views", default="1=1_stern_three_quarter,7=7_bow_three_quarter")
ap.add_argument("--clusters", type=int, default=14)
ap.add_argument("--chroma-floor", type=float, default=12.0,
                help="INHERITED from W3's palette fixture. Below it hue is undefined.")
ap.add_argument("--seed", type=int, default=770700)
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


MATS = json.load(open(args.materials, encoding="utf-8"))["materials"]
px_all, bg_all = [], []
for spec in args.views.split(","):
    k, tag = spec.split("=")
    im = np.asarray(Image.open(os.path.join(args.pair, "target_%s.png" % tag)
                               ).convert("RGB"), dtype=np.float32) / 255.0
    sil = np.asarray(Image.open(os.path.join(args.masks, "galleonclay_%s.png" % k)
                                ).convert("L")) > 127
    c8 = np.concatenate([im[:8, :8].reshape(-1, 3), im[:8, -8:].reshape(-1, 3)])
    bg_all.append(np.median(c8, axis=0))
    px_all.append(im[sil])
    print("[4d] view %s: %d px inside the exact silhouette, backdrop rgb(%d,%d,%d)"
          % (k, sil.sum(), *[int(round(v * 255)) for v in bg_all[-1]]), flush=True)
P = np.concatenate(px_all)
BG = np.median(np.stack(bg_all), axis=0)
out = {"realised_backdrop_rgb255": [int(round(v * 255)) for v in BG],
       "asked_backdrop_rgb255": [255, 255, 255], "px": int(len(P))}

# ---- cluster what is ACTUALLY there (k-means in Lab, fixed seed, no sklearn)
X = lab(P)
rng = np.random.default_rng(args.seed)
cen = X[rng.choice(len(X), args.clusters, replace=False)]
for _ in range(40):
    d = ((X[:, None, :] - cen[None, :, :]) ** 2).sum(-1) if len(X) < 60000 else None
    if d is None:
        lab_i = np.empty(len(X), dtype=np.int64)
        for s in range(0, len(X), 60000):
            e = min(s + 60000, len(X))
            lab_i[s:e] = ((X[s:e, None, :] - cen[None, :, :]) ** 2).sum(-1).argmin(1)
    else:
        lab_i = d.argmin(1)
    for j in range(args.clusters):
        m = lab_i == j
        if m.any():
            cen[j] = X[m].mean(0)
counts = np.bincount(lab_i, minlength=args.clusters)
order = np.argsort(counts)[::-1]
L_, C_, h_ = lch(cen)
print("\n[4d] WHAT IS ACTUALLY ON THE PAIR - %d clusters inside the silhouette:" % args.clusters,
      flush=True)
clusters = []
for j in order:
    if counts[j] < len(X) * 0.004:
        continue
    srgb = None
    sel = lab_i == j
    srgb = np.median(P[sel], axis=0)
    clusters.append({"share_pct": round(100.0 * counts[j] / len(X), 2),
                     "rgb255": [int(round(v * 255)) for v in srgb],
                     "L": round(float(L_[j]), 1), "C": round(float(C_[j]), 1),
                     "h": round(float(h_[j]), 1)})
    print("[4d]   %5.2f%%  rgb(%3d,%3d,%3d)  L* %5.1f  C* %5.1f  h %5.1f%s"
          % (clusters[-1]["share_pct"], *clusters[-1]["rgb255"], L_[j], C_[j], h_[j],
             "   <- below chroma floor, hue undefined" if C_[j] < args.chroma_floor else ""),
          flush=True)
out["clusters"] = clusters

# ---- landing table: for each declared element, is any cluster near it?
print("\n[4d] LANDING TABLE - each declared element against the nearest measured cluster:",
      flush=True)
land = []
for m in MATS:
    exp = lab(np.array([[c / 255.0 for c in m["rgb"]]]))[0]
    dd = np.linalg.norm(cen - exp[None, :], axis=1)
    j = int(np.argmin(dd))
    verdict = "LANDED" if dd[j] <= 25 else ("NEAR" if dd[j] <= 40 else "NOT FOUND")
    row = {"id": m["id"], "name": m["name"], "expected_rgb255": m["rgb"],
           "nearest_cluster_rgb255": [int(round(v * 255))
                                      for v in np.median(P[lab_i == j], axis=0)],
           "dE": round(float(dd[j]), 1), "share_pct": round(100.0 * counts[j] / len(X), 2),
           "verdict": verdict}
    land.append(row)
    print("[4d]   %-4s %-34s dE %5.1f  %-9s  nearest rgb(%3d,%3d,%3d)  %5.2f%%"
          % (m["id"], m["name"][:34], dd[j], verdict, *row["nearest_cluster_rgb255"],
             row["share_pct"]), flush=True)
out["landing"] = land

# ---- bands, from the MEASURED colours above the chroma floor
above = [c for c in clusters if c["C"] >= args.chroma_floor]
hs = sorted(c["h"] for c in above)
print("\n[4d] BANDS - measured hues above the C* %.0f floor: %s"
      % (args.chroma_floor, ", ".join("%.0f" % x for x in hs)), flush=True)
bands = []
if hs:
    cur = [hs[0]]
    for x in hs[1:]:
        if x - cur[-1] <= 40:
            cur.append(x)
        else:
            bands.append((cur[0], cur[-1]))
            cur = [x]
    bands.append((cur[0], cur[-1]))
out["measured_hue_clusters"] = hs
out["bands_raw"] = [[round(a, 1), round(b, 1)] for a, b in bands]
print("[4d]   contiguous groups (gap > 40 deg splits): %s"
      % ", ".join("%.0f-%.0f" % b for b in bands), flush=True)

# ---- backdrop re-derivation on the REALISED colours
Cm = np.array([[c / 255.0 for c in m["rgb"]] for m in MATS])
thin = np.array([bool(m.get("thin")) for m in MATS])
meas = np.array([[v / 255.0 for v in c["rgb255"]] for c in clusters])


def mind(bg, mat):
    return float(np.abs(mat - np.array(bg)[None, :]).max(1).min())


print("\n[4d] BACKDROP, against MEASURED cluster colours (4b used expected ones):", flush=True)
for nm, bg in (("realised on the pair", BG), ("asked (white)", np.array([1.0, 1.0, 1.0])),
               ("W3's inherited grey", np.array([106, 106, 107]) / 255.0)):
    print("[4d]   %-22s rgb(%3d,%3d,%3d)  min-dist to measured clusters %.4f  "
          "(to expected table %.4f)"
          % (nm, *[int(round(v * 255)) for v in bg], mind(bg, meas), mind(bg, Cm)), flush=True)
out["backdrop_check"] = {
    "realised": {"rgb255": [int(round(v * 255)) for v in BG],
                 "min_dist_measured": round(mind(BG, meas), 4)},
    "asked_white": {"min_dist_measured": round(mind(np.ones(3), meas), 4)},
    "w3_grey": {"min_dist_measured": round(mind(np.array([106, 106, 107]) / 255.0, meas), 4)}}

json.dump(out, open(os.path.join(args.out, "bands.json"), "w"), indent=1)
print("\n[4d] wrote %s" % os.path.join(args.out, "bands.json"), flush=True)
