"""E04 Arm G7 - WHERE did the one word land? A change-localisation diagnostic.

POST-HOC AND DECLARED AS SUCH. The arm's pass reading is the pre-registered cluster table in
e04_g7_landing.py and it is not touched by anything here. This script exists because that
table returned NEAR while the crop sheet shows red squares on the upper gun-port row - a
k-means over 318,578 px at k = 14 cannot resolve a feature of a few thousand, and a
measurement that cannot see the thing being asked about should be reported alongside one that
can, not replaced by it.

It asks the question in the direction that assumes nothing: not "is there red" but "what
changed, and where". The change map is the two images' per-pixel Lab distance inside the exact
silhouette; components are ranked by area and reported with their BEFORE and AFTER median
colours, so a reader sees what each region was and what it became. The dE > 10 component
threshold is DESCRIPTIVE - it selects what to print and gates nothing.

Two house conventions are applied unchanged, both inherited rather than chosen here: the
palette gate's "report the total AND the largest connected component" (E08 A23-25), and
"below a chroma floor hue is not a colour" (C* 12.0).

  e04_g7_where.py --before B.png --after A.png --mask M.png --out DIR
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage

ap = argparse.ArgumentParser()
ap.add_argument("--before", required=True)
ap.add_argument("--after", required=True)
ap.add_argument("--mask", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--dE", type=float, default=10.0, help="DESCRIPTIVE component threshold.")
ap.add_argument("--chroma-floor", type=float, default=12.0)
ap.add_argument("--top", type=int, default=12)
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
    return L[..., 0], np.hypot(L[..., 1], L[..., 2]), \
        np.degrees(np.arctan2(L[..., 2], L[..., 1])) % 360


B = np.asarray(Image.open(args.before).convert("RGB"), dtype=np.float32) / 255.0
A = np.asarray(Image.open(args.after).convert("RGB"), dtype=np.float32) / 255.0
SIL = np.asarray(Image.open(args.mask).convert("L")) > 127
LB, LA = lab(B), lab(A)
D = np.linalg.norm(LA - LB, axis=-1)
D[~SIL] = 0.0
out = {"_post_hoc": "Descriptive. The arm's pass reading is e04_g7_landing.py's cluster table.",
       "dE_component_threshold": args.dE, "silhouette_px": int(SIL.sum())}

# ---- the hue composition of the pre-registered red window, both images, unchanged window
print("[where] HUE COMPOSITION of the pre-registered window (C* >= %.0f, h in [350,360) u "
      "[0,50)) - the numerator's own breakdown, no threshold moved:" % args.chroma_floor,
      flush=True)
bins = [(350, 360), (0, 10), (10, 20), (20, 30), (30, 40), (40, 50)]
comp = {}
for tag, L in (("before", LB), ("after", LA)):
    _, C, h = lch(L)
    sel = SIL & (C >= args.chroma_floor) & ((h >= 350) | (h < 50))
    row = {}
    for lo, hi in bins:
        m = sel & (h >= lo) & (h < hi)
        row["%d-%d" % (lo, hi)] = int(m.sum())
    row["total"] = int(sel.sum())
    comp[tag] = row
    print("[where]   %-6s  %s   total %d"
          % (tag, "  ".join("%s:%d" % (k, v) for k, v in row.items() if k != "total"),
             row["total"]), flush=True)
    lb_, n = ndimage.label(sel)
    if n:
        sizes = np.bincount(lb_.ravel())[1:]
        row["components"] = int(n)
        row["largest_cc_px"] = int(sizes.max())
        print("[where]           %d components, largest %d px (E08 palette-gate convention)"
              % (n, sizes.max()), flush=True)
out["red_window_hue_composition"] = comp

# ---- what changed, and where
lbl, n = ndimage.label(D > args.dE)
print("\n[where] CHANGE MAP: %d px over dE %.0f in %d components (silhouette %d px, %.2f%%)"
      % ((D > args.dE).sum(), args.dE, n, SIL.sum(),
         100.0 * (D > args.dE).sum() / SIL.sum()), flush=True)
objs = ndimage.find_objects(lbl)
sizes = np.bincount(lbl.ravel())[1:] if n else np.array([])
rows = []
print("[where]   rank    px   bbox x,y w x h        BEFORE rgb  ->  AFTER rgb        "
      "  B h/C*      A h/C*", flush=True)
for r, j in enumerate(np.argsort(sizes)[::-1][:args.top], 1):
    m = lbl == (j + 1)
    sl = objs[j]
    bm = np.median(B[m], axis=0)
    am = np.median(A[m], axis=0)
    _, bc, bh = lch(np.median(LB[m], axis=0))
    _, ac, ah = lch(np.median(LA[m], axis=0))
    rows.append({"rank": r, "px": int(sizes[j]),
                 "bbox_xywh": [int(sl[1].start), int(sl[0].start),
                               int(sl[1].stop - sl[1].start), int(sl[0].stop - sl[0].start)],
                 "before_rgb255": [int(round(v * 255)) for v in bm],
                 "after_rgb255": [int(round(v * 255)) for v in am],
                 "before_h": round(float(bh), 1), "before_C": round(float(bc), 1),
                 "after_h": round(float(ah), 1), "after_C": round(float(ac), 1),
                 "median_dE": round(float(np.median(D[m])), 1)})
    print("[where]   %4d %6d   %4d,%4d %3dx%3d   rgb(%3d,%3d,%3d) -> rgb(%3d,%3d,%3d)   "
          "%5.1f/%4.1f  %5.1f/%4.1f   dE %5.1f"
          % (r, sizes[j], sl[1].start, sl[0].start, sl[1].stop - sl[1].start,
             sl[0].stop - sl[0].start, *rows[-1]["before_rgb255"], *rows[-1]["after_rgb255"],
             bh, bc, ah, ac, rows[-1]["median_dE"]), flush=True)
out["change_components"] = rows
out["change_px_over_threshold"] = int((D > args.dE).sum())
out["change_components_n"] = int(n)

json.dump(out, open(os.path.join(args.out, "g7_where.json"), "w"), indent=1)
np.save(os.path.join(args.out, "g7_change_dE.npy"), D.astype(np.float32))
print("\n[where] wrote %s" % os.path.join(args.out, "g7_where.json"), flush=True)
