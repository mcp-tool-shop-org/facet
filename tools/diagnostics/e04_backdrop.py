"""E04 Task 4b - derive the twins' backdrop (S-backdrop).

The key is `max_channel |pixel - backdrop| > 0.06` and the backdrop is PROMPTED, so it is
the only operand in that comparison we choose freely. W3's inherited "plain grey background"
put a mid grey in the middle of everything and the blade died in it. This picks the backdrop
that maximises the MINIMUM distance to every declared material, weighted toward the dark thin
elements, because thin structure antialiases toward the backdrop and keys out 4.2-6.8x more
often than bulk (E04 fixture check).

WHAT THIS CANNOT DO, stated up front: the material colours below are ESTIMATES read off the
fixture's words. They are the weakest link. The fixture's own non-circularity rule says the
palette bands cross-check against the styled target pair once it exists; the same applies
here. If the pair's real materials sit elsewhere, the backdrop follows the pair, not this
table.

  e04_backdrop.py --materials m.json --out DIR [--thin-weight 2.0]

Standards compliance: PIN_PER_STEP - the material table is a file, not a literal. ANDON -
none; this proposes and tabulates. EXTERNAL_VERIFIER - it reports the metric's optimum AND
the best low-saturation option with its cost, because the metric alone does not know that a
saturated backdrop bleeds into a diffusion image.
"""
import argparse
import json
import os

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--materials", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--thin-weight", type=float, default=2.0,
                help="multiplier on the distance requirement for elements flagged thin")
ap.add_argument("--grid", type=int, default=26)
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)

MATS = json.load(open(args.materials, encoding="utf-8"))["materials"]
names = [m["id"] + " " + m["name"] for m in MATS]
C = np.array([[c / 255.0 for c in m["rgb"]] for m in MATS])
thin = np.array([bool(m.get("thin")) for m in MATS])
print("[bg] %d declared materials, %d flagged thin (%s)"
      % (len(MATS), thin.sum(), ", ".join(MATS[i]["id"] for i in np.nonzero(thin)[0])),
      flush=True)


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


def score(bg):
    """the key's own metric: max-channel absolute distance, per material."""
    d = np.abs(C - bg[None, :]).max(axis=1)
    w = np.where(thin, args.thin_weight, 1.0)
    return float((d / w).min()), d


g = np.linspace(0, 1, args.grid)
best = (-1, None)
best_neutral = (-1, None)
best_lowsat = (-1, None)
rows = []
for r in g:
    for gg in g:
        for b in g:
            bg = np.array([r, gg, b])
            s, _ = score(bg)
            sat = float(bg.max() - bg.min())
            if s > best[0]:
                best = (s, bg.copy())
            if sat <= 0.02 and s > best_neutral[0]:
                best_neutral = (s, bg.copy())
            if sat <= 0.18 and s > best_lowsat[0]:
                best_lowsat = (s, bg.copy())

out = {"materials": names, "thin_weight": args.thin_weight, "candidates": {}}
for tag, (s, bg) in (("metric_optimum", best), ("best_low_saturation", best_lowsat),
                     ("best_neutral", best_neutral)):
    _, d = score(bg)
    lab_bg = srgb_to_lab(bg[None, :])[0]
    ent = {"rgb255": [int(round(x * 255)) for x in bg],
           "weighted_min_distance": round(s, 4),
           "raw_min_distance": round(float(d.min()), 4),
           "closest_material": names[int(np.argmin(d))],
           "saturation": round(float(bg.max() - bg.min()), 4),
           "L": round(float(lab_bg[0]), 1),
           "per_material": {names[i]: round(float(d[i]), 4) for i in range(len(names))}}
    out["candidates"][tag] = ent
    print("\n[bg] %-22s rgb(%3d,%3d,%3d)  L* %5.1f  sat %.3f  weighted-min %.4f  "
          "raw-min %.4f (%s)"
          % (tag, *ent["rgb255"], ent["L"], ent["saturation"], s, d.min(),
             names[int(np.argmin(d))]), flush=True)
    order = np.argsort(d)
    for i in order:
        flag = "  <- THIN" if thin[i] else ""
        mark = "  <== MINIMUM" if i == order[0] else ""
        print("[bg]     %-38s %.4f%s%s" % (names[i], d[i], flag, mark), flush=True)

json.dump(out, open(os.path.join(args.out, "backdrop.json"), "w"), indent=1)
print("\n[bg] wrote %s" % os.path.join(args.out, "backdrop.json"), flush=True)
