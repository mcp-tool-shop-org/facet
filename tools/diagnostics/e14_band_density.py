"""The three questions `e04_bands.py` does not answer, for the prop's palette derivation.

E04's tool clusters and reports contiguous hue groups. On this subject that leaves three
things undecided, and each has burned this repo before:

  1. THE CHROMA FLOOR MUST BE DERIVED, NOT INHERITED. The dispatch is explicit: it comes from
     the SEPARATION STRUCTURE of the pair's realised values and never from where L1's 5.39
     cast falls. So the chroma density is plotted and the antimode located, rather than 12.0
     being carried over from W3 because it is what the last two subjects used.

  2. "DISTANT MEDIANS DO NOT IMPLY A GAP BETWEEN THEM." An advisor once read two summary
     statistics as a separable distribution and specified a threshold "derived from the
     measured bimodality"; the density rose monotonically with no antimode at all. So every
     boundary this file proposes is proposed WITH the density between the two populations,
     and where there is no antimode it says so and suspends.

  3. HUE CANNOT SEPARATE THE BACKDROP RIM FROM THE GEM. `palette_gate.py` measures only
     INSIDE the exact silhouette, so the realised backdrop (C* 32-37, far above any floor)
     enters as ANTIALIASED RIM pixels. L5's gem drifted toward the same hue on the pair's
     view 1. Two categorically different things - a contamination artifact and a declared
     material - at the same hue. **They are separated by PLACEMENT**: rim mixing lives within
     a pixel or two of the silhouette boundary and the gem lives deep inside the pommel. This
     file measures the depth distribution of every above-floor hue population, because
     testing the property directly beats testing a proxy for it.

THE PERIMETER LAW rides on every count: off-palette pixels live at material and silhouette
boundaries, so they scale with PERIMETER while figure AREA swings 2.061x between views on this
subject (E14 Ruling 10c). Counts are reported absolute, per-perimeter, and per-area, and the
three are not interchangeable.

  e14_band_density.py --pairs P0.png,P1.png --masks M0.png,M1.png --labels v0,v1
                      --out DIR [--floor-scan 0,40] [--hue-window 280,320]

Standards compliance: PIN_PER_STEP - every window and bin width is a flag; all densities land
in the JSON beside the plots. ANDON_AUTHORITY - none; this proposes nothing and adopts
nothing. DECOMPOSE_BY_SECRETS - the depth test is placement, measured directly, not a hue
heuristic standing in for it. EXTERNAL_VERIFIER - the sRGB->Lab path is asserted against
e14_backdrop_checks.py's recorded triple before any number is printed.
"""
import argparse
import json
import os

import cv2
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--pairs", required=True)
ap.add_argument("--masks", required=True)
ap.add_argument("--labels", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--floor-scan", default="0,40")
ap.add_argument("--floor-bin", type=float, default=0.5)
ap.add_argument("--hue-window", default="280,320")
ap.add_argument("--hue-bin", type=float, default=1.0)
ap.add_argument("--max-depth", type=int, default=12)
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)


def srgb_to_lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


_e = srgb_to_lab(np.array([[214, 214, 255]]) / 255.0)[0]
assert abs(_e[0] - 86.9) < 0.1 and abs(np.hypot(_e[1], _e[2]) - 21.4) < 0.1, \
    "ANDON: sRGB->Lab disagrees with the recorded derivation triple"

PAIRS = args.pairs.split(",")
MASKS = args.masks.split(",")
LABELS = args.labels.split(",")
assert len(PAIRS) == len(MASKS) == len(LABELS), "ANDON: --pairs/--masks/--labels differ in length"
f0, f1 = (float(v) for v in args.floor_scan.split(","))
h0, h1 = (float(v) for v in args.hue_window.split(","))

out = {"views": {}, "floor_scan": [f0, f1], "hue_window": [h0, h1]}
allC, allH, allD, allV, allRow = [], [], [], [], []
bgC, bgH = [], []

for p, m, lb in zip(PAIRS, MASKS, LABELS):
    img = np.asarray(Image.open(p).convert("RGB")).astype(np.float64) / 255.0
    msk = np.asarray(Image.open(m).convert("L")) > 127
    assert img.shape[:2] == msk.shape, "ANDON: %s and %s differ in shape" % (p, m)
    H, W = msk.shape
    lab = srgb_to_lab(img)
    C = np.hypot(lab[..., 1], lab[..., 2])
    Hu = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0

    # DEPTH INTO THE FIGURE: how far is each figure pixel from the silhouette boundary?
    # distanceTransform on the mask gives exactly that, in pixels.
    dep = cv2.distanceTransform(msk.astype(np.uint8), cv2.DIST_L2, 5)
    # PERIMETER, for the normalisation law: boundary pixels of the exact silhouette
    er = cv2.erode(msk.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1) > 0
    perim = int((msk & ~er).sum())
    rows = np.repeat(np.arange(H)[:, None], W, axis=1)

    allC.append(C[msk]); allH.append(Hu[msk]); allD.append(dep[msk])
    allV.append(np.full(int(msk.sum()), LABELS.index(lb)))
    allRow.append(rows[msk] / float(H))
    bgC.append(C[~msk]); bgH.append(Hu[~msk])
    out["views"][lb] = {"figure_px": int(msk.sum()), "perimeter_px": perim,
                        "area_over_perimeter": round(float(msk.sum()) / max(perim, 1), 2),
                        "frame": [W, H]}
    print("[dens] %-4s figure %s px  perimeter %s px  area/perim %.2f"
          % (lb, f"{int(msk.sum()):,}", f"{perim:,}",
             float(msk.sum()) / max(perim, 1)), flush=True)

C = np.concatenate(allC); Hu = np.concatenate(allH); D = np.concatenate(allD)
V = np.concatenate(allV); R = np.concatenate(allRow)
BC = np.concatenate(bgC); BH = np.concatenate(bgH)
print("[dens] pooled: %s figure px, %s backdrop px" % (f"{len(C):,}", f"{len(BC):,}"))

# ---- 1. THE CHROMA DENSITY, and the antimode the floor must come from -------------------
edges = np.arange(f0, f1 + args.floor_bin, args.floor_bin)
hist, _ = np.histogram(C, bins=edges)
mid = (edges[:-1] + edges[1:]) / 2
print("\n[floor] CHROMA DENSITY over %s figure px (bin %.1f) - the floor comes from THIS"
      % (f"{len(C):,}", args.floor_bin))
print("[floor] %6s %10s %8s   %s" % ("C*", "px", "% fig", "density"))
peak = hist.max()
rows_out = []
for i, (mv, hv) in enumerate(zip(mid, hist)):
    if mv > 40:
        break
    bar = "#" * int(round(60.0 * hv / max(peak, 1)))
    if hv or mv < 20:
        print("[floor] %6.1f %10s %7.3f%%   %s" % (mv, f"{int(hv):,}", 100.0 * hv / len(C), bar))
    rows_out.append({"c": round(float(mv), 2), "px": int(hv),
                     "pct": round(100.0 * hv / len(C), 4)})
out["chroma_density"] = rows_out

# the antimode: the emptiest bin between the achromatic mass and the coloured mass
lo_i = int(np.argmax(hist))                       # the achromatic peak
hi_cand = [i for i in range(lo_i + 1, len(hist)) if mid[i] > 15]
if hi_cand:
    seg = hist[lo_i:hi_cand[0] + 1]
    amin = lo_i + int(np.argmin(seg))
    print("\n[floor] achromatic peak at C* %.1f (%s px); searching to C* 15+"
          % (mid[lo_i], f"{int(hist[lo_i]):,}"))
    print("[floor] ANTIMODE at C* %.1f with %s px (%.4f%% of figure)"
          % (mid[amin], f"{int(hist[amin]):,}", 100.0 * hist[amin] / len(C)))
    out["antimode_c"] = round(float(mid[amin]), 2)
    out["antimode_px"] = int(hist[amin])
    # is it a real valley? compare to the mass on each side
    left = int(hist[lo_i:amin].sum()); right = int(hist[amin:hi_cand[-1]].sum())
    print("[floor] mass below the antimode %s px (%.2f%%) | above %s px (%.2f%%)"
          % (f"{left:,}", 100.0 * left / len(C), f"{right:,}", 100.0 * right / len(C)))
    out["mass_below_antimode_pct"] = round(100.0 * left / len(C), 3)
    out["mass_above_antimode_pct"] = round(100.0 * right / len(C), 3)

for cand in (5.0, 8.0, 10.0, 12.0, 15.0, 18.0, 20.0):
    print("[floor]   candidate floor %5.1f -> %8s px above (%.3f%% of figure)"
          % (cand, f"{int((C >= cand).sum()):,}", 100.0 * (C >= cand).mean()))
out["above_floor_by_candidate"] = {str(c): {"px": int((C >= c).sum()),
                                            "pct": round(100.0 * float((C >= c).mean()), 4)}
                                   for c in (5.0, 8.0, 10.0, 12.0, 15.0, 18.0, 20.0)}

# ---- 2. THE HUE DENSITY IN THE HARD WINDOW ----------------------------------------------
def hue_density(sel_C, sel_H, floor, label):
    s = sel_C >= floor
    h = sel_H[s]
    e = np.arange(h0, h1 + args.hue_bin, args.hue_bin)
    hh, _ = np.histogram(h, bins=e)
    return (e[:-1] + e[1:]) / 2, hh, int(s.sum())


print("\n[hue] DENSITY %g-%g deg above the derived-candidate floor 12.0 - "
      "FIGURE vs BACKDROP" % (h0, h1))
mh, fig_h, nf = hue_density(C, Hu, 12.0, "figure")
_, bg_h, nb = hue_density(BC, BH, 12.0, "backdrop")
pk = max(fig_h.max(), 1)
print("[hue] %6s %10s %10s   %s" % ("hue", "figure px", "bg px", "figure density"))
for mv, fv, bv in zip(mh, fig_h, bg_h):
    print("[hue] %6.1f %10s %10s   %s"
          % (mv, f"{int(fv):,}", f"{int(bv):,}", "#" * int(round(50.0 * fv / pk))))
out["hue_density_window"] = [{"hue": round(float(a), 1), "figure_px": int(b),
                              "backdrop_px": int(c)} for a, b, c in zip(mh, fig_h, bg_h)]
inner = fig_h[(mh > 292) & (mh < 304)]
print("[hue] is there an ANTIMODE between the ~295 cast and the ~305 backdrop?  "
      "min density in 292-304 = %s px against neighbours %s / %s"
      % (f"{int(inner.min()):,}" if len(inner) else "n/a",
         f"{int(fig_h[mh <= 292].max()):,}", f"{int(fig_h[mh >= 304].max()):,}"))
out["window_min_px"] = int(inner.min()) if len(inner) else None

# ---- 3. PLACEMENT: is the above-floor 290-310 population RIM or GEM? --------------------
print("\n[depth] THE PLACEMENT TEST - hue cannot separate rim mixing from the gem; depth can")
print("[depth] %-26s %9s %8s %8s %8s %8s" % ("population (C* >= 12)", "px", "d<=1", "d<=2",
                                             "med d", "med row"))
pops = [("all figure", np.ones(len(C), bool)),
        ("hue 290-310", (Hu >= 290) & (Hu < 310)),
        ("hue 300-310", (Hu >= 300) & (Hu < 310)),
        ("hue 290-300", (Hu >= 290) & (Hu < 300)),
        ("wine 0-25", ((Hu >= 0) & (Hu < 25)) | (Hu >= 350)),
        ("gold 60-95", (Hu >= 60) & (Hu < 95))]
depth_rows = {}
for nm, sel in pops:
    s = sel & (C >= 12.0)
    n = int(s.sum())
    if n < 20:
        print("[depth] %-26s %9s   (too few)" % (nm, f"{n:,}"))
        continue
    d = D[s]
    print("[depth] %-26s %9s %7.1f%% %7.1f%% %8.2f %8.3f"
          % (nm, f"{n:,}", 100.0 * (d <= 1).mean(), 100.0 * (d <= 2).mean(),
             float(np.median(d)), float(np.median(R[s]))))
    depth_rows[nm] = {"px": n, "pct_depth_le_1": round(100.0 * float((d <= 1).mean()), 2),
                      "pct_depth_le_2": round(100.0 * float((d <= 2).mean()), 2),
                      "median_depth": round(float(np.median(d)), 3),
                      "median_row_frac": round(float(np.median(R[s])), 4)}
out["placement"] = depth_rows

# the deep members of the 300-310 population: where are they, and how big?
deep = (Hu >= 300) & (Hu < 310) & (C >= 12.0) & (D > 2)
print("\n[depth] the 300-310 population DEEPER than 2 px: %s px (%.3f%% of figure)"
      % (f"{int(deep.sum()):,}", 100.0 * deep.mean()))
if deep.sum():
    print("[depth]   their row positions: p05 %.3f  median %.3f  p95 %.3f  "
          "(0 = top of frame; the pommel is the top ~8%%)"
          % (np.percentile(R[deep], 5), np.median(R[deep]), np.percentile(R[deep], 95)))
    out["deep_300_310"] = {"px": int(deep.sum()),
                           "row_p05": round(float(np.percentile(R[deep], 5)), 4),
                           "row_median": round(float(np.median(R[deep])), 4),
                           "row_p95": round(float(np.percentile(R[deep], 95)), 4)}

json.dump(out, open(os.path.join(args.out, "band_density.json"), "w"), indent=1)
print("\n[dens] wrote %s" % os.path.join(args.out, "band_density.json"))
