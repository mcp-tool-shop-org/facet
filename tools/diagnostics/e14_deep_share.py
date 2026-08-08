"""The STANDING DEPTH DIAGNOSTIC — E14 Ruling 17c, required beside every gate table.

WHY IT IS STANDING, in the ruling's own terms. The lavender-rim band was admitted as a
RIM-ADMISSION so the gate's totals mean something on accepted work. The blindness that buys
is priced and named: the hue count can no longer see interior backdrop-family arrivals,
because they sit inside an allowed band. So the thing hue can no longer watch is watched by
DEPTH instead - every twin's gate report carries the lavender band's deep share (> 2 px from
the silhouette boundary) beside its totals.

THE RECORDED BASELINE CLASS is the accepted pair's own deep remnant: 144 px = 0.160% of
figure, UNCONCENTRATED, spread across rows 0.13-0.91. A deep, CONCENTRATED lavender
population on any twin is a finding for the eye regardless of any total - concentration is
what separates an interior arrival from scattered noise, so this file reports the largest
connected component of the deep set and its row spread, not just its count.

PERIMETER, NOT AREA (the standing law). Rim quantities scale with perimeter and this
subject's figure area swings 2.061x between views (Ruling 10c), so the shallow share is
reported per perimeter as well as absolute.

  e14_deep_share.py --images I0.png,... --masks M0.png,... --labels v0,... [--out J.json]

Standards compliance: PIN_PER_STEP - the band, floor and depth threshold are flags with the
ruled defaults and land in the JSON. ANDON_AUTHORITY - none; this is a diagnostic beside a
report-only gate, exactly as 17d leaves it. EXTERNAL_VERIFIER - depth comes from the exact
raycast silhouette, an independent path from the generator and from the hue gate.
"""
import argparse
import json
import os

import cv2
import numpy as np
from PIL import Image
from scipy.ndimage import label

ap = argparse.ArgumentParser()
ap.add_argument("--images", required=True)
ap.add_argument("--masks", required=True)
ap.add_argument("--labels", required=True)
ap.add_argument("--floor", type=float, default=12.0, help="ruled at E14 17a")
ap.add_argument("--band", default="292,314", help="the lavender-rim band, ruled at 17c")
ap.add_argument("--deep", type=float, default=2.0, help="depth px above which a pixel is DEEP")
ap.add_argument("--out", default=None)
args = ap.parse_args()

LO, HI = (float(v) for v in args.band.split(","))


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


rows = []
print("[deep] lavender-rim band %g-%g, floor C* > %g, deep = depth > %g px"
      % (LO, HI, args.floor, args.deep))
print("[deep] BASELINE CLASS (the accepted pair, Ruling 17c): 144 px = 0.160%% of figure, "
      "unconcentrated, rows 0.13-0.91")
print("\n[deep] %-6s %9s %9s %8s %9s %8s %9s   %s"
      % ("view", "band px", "DEEP px", "deep %", "largest CC", "rows", "shallow", "per perim"))
for ip, mp, lb in zip(args.images.split(","), args.masks.split(","), args.labels.split(",")):
    img = np.asarray(Image.open(ip).convert("RGB")).astype(np.float64) / 255.0
    msk = np.asarray(Image.open(mp).convert("L")) > 127
    lab = srgb_to_lab(img)
    C = np.hypot(lab[..., 1], lab[..., 2])
    Hu = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0
    dep = cv2.distanceTransform(msk.astype(np.uint8), cv2.DIST_L2, 5)
    er = cv2.erode(msk.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1) > 0
    perim = int((msk & ~er).sum())
    H = msk.shape[0]

    inband = (Hu >= LO) & (Hu <= HI) if LO <= HI else ((Hu >= LO) | (Hu <= HI))
    sel = msk & (C > args.floor) & inband
    deep = sel & (dep > args.deep)
    shallow = sel & ~deep
    lb_arr, n = label(deep)
    cc = int(np.bincount(lb_arr.ravel())[1:].max()) if n else 0
    if deep.sum():
        rr = np.where(deep)[0] / float(H)
        r5, r95 = float(np.percentile(rr, 5)), float(np.percentile(rr, 95))
    else:
        r5 = r95 = float("nan")
    print("[deep] %-6s %9s %9s %7.3f%% %10s %4.2f-%4.2f %9s %9.3f"
          % (lb, f"{int(sel.sum()):,}", f"{int(deep.sum()):,}",
             100.0 * deep.sum() / max(int(msk.sum()), 1), f"{cc:,}", r5, r95,
             f"{int(shallow.sum()):,}", shallow.sum() / max(perim, 1)))
    rows.append({"label": lb, "figure_px": int(msk.sum()), "perimeter_px": perim,
                 "band_px": int(sel.sum()), "deep_px": int(deep.sum()),
                 "deep_pct_of_figure": round(100.0 * float(deep.sum()) / max(int(msk.sum()), 1), 4),
                 "deep_largest_cc": cc,
                 "deep_row_p05": None if np.isnan(r5) else round(r5, 4),
                 "deep_row_p95": None if np.isnan(r95) else round(r95, 4),
                 "shallow_px": int(shallow.sum()),
                 "shallow_per_perimeter": round(float(shallow.sum()) / max(perim, 1), 4)})

print("\n[deep] READ IT THIS WAY (17c): a deep, CONCENTRATED population is the finding - a "
      "large largest-CC with a narrow row span. Scattered deep pixels at the pair's own "
      "0.160%% order are the baseline class, not a defect.")
if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump({"floor": args.floor, "band": [LO, HI], "deep_threshold": args.deep,
               "baseline_class": {"px": 144, "pct": 0.160, "rows": [0.13, 0.91],
                                  "source": "the accepted pair, E14 Ruling 17c"},
               "views": rows}, open(args.out, "w"), indent=1)
    print("[deep] wrote %s" % args.out)
