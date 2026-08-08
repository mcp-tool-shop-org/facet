"""Band EDGES by a stated rule, applied once, with the rule's own sensitivity beside it.

A band edge is where a derivation stops being a measurement and starts being a convention.
The galleon said so plainly about its blue band ("the +-10 deg margin is a CONVENTION, not a
measurement, and it is stated as one"), and this file keeps that discipline by making the rule
explicit and reporting what a different rule would have given - so the ruling can see how much
the choice matters instead of taking one number on trust.

THE RULE, stated before it is applied:
  A band is the contiguous span of BODY support (depth > 2 px from the silhouette, so rim
  mixing cannot vote) around a local peak, trimmed where body density falls below
  `--trim-frac` of that band's OWN peak. Per-band normalisation, not a global cut, because
  gold's peak is 58%% of wine's and a global cut would silently trim the smaller band harder.

WHY BODY-ONLY. The placement test measured the 293-313 population at 93-96%% rim - it is
backdrop bleed at the silhouette edge, not a material. Letting rim pixels set a material
band's edges would derive the band from a contamination artifact.

  e14_band_edges.py --pairs P0,P1 --masks M0,M1 --floor 12 --trim-frac 0.01 [--out J.json]

Standards compliance: PIN_PER_STEP - the rule, the floor, the bin and the trim fraction are
all flags and all land in the JSON. ANDON_AUTHORITY - none; emits edges, adopts nothing.
UNCERTAINTY_GATED_HUMANS - the sensitivity table exists so the ruling sees the convention.
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
ap.add_argument("--floor", type=float, default=12.0)
ap.add_argument("--bin", type=float, default=2.0)
ap.add_argument("--depth", type=float, default=2.0)
ap.add_argument("--trim-frac", type=float, default=0.01)
ap.add_argument("--out", default=None)
args = ap.parse_args()


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


Hb, Hr = [], []
for p, m in zip(args.pairs.split(","), args.masks.split(",")):
    img = np.asarray(Image.open(p).convert("RGB")).astype(np.float64) / 255.0
    msk = np.asarray(Image.open(m).convert("L")) > 127
    lab = srgb_to_lab(img)
    C = np.hypot(lab[..., 1], lab[..., 2])
    Hu = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0
    dep = cv2.distanceTransform(msk.astype(np.uint8), cv2.DIST_L2, 5)
    s = msk & (C > args.floor)
    Hb.append(Hu[s & (dep > args.depth)])
    Hr.append(Hu[s & (dep <= args.depth)])
B = np.concatenate(Hb)
R = np.concatenate(Hr)
nb = int(np.ceil(360.0 / args.bin))
e = np.arange(nb + 1) * args.bin
hb, _ = np.histogram(B, bins=e)
hr, _ = np.histogram(R, bins=e)
mid = (e[:-1] + e[1:]) / 2
print("[edges] floor C* > %g, depth > %g px | BODY %s px, RIM %s px, bin %g deg"
      % (args.floor, args.depth, f"{len(B):,}", f"{len(R):,}", args.bin))


def grow(peak_i, frac):
    """walk out from a peak until body density drops below frac * peak, circularly"""
    thr = hb[peak_i] * frac
    lo = peak_i
    while hb[(lo - 1) % nb] >= thr:
        lo = (lo - 1) % nb
        if lo == peak_i:
            break
    hi = peak_i
    while hb[(hi + 1) % nb] >= thr:
        hi = (hi + 1) % nb
        if hi == peak_i:
            break
    return lo, hi


def span_deg(lo, hi):
    return (hi - lo) % nb * args.bin + args.bin


out = {"floor": args.floor, "depth": args.depth, "bin": args.bin,
       "trim_frac": args.trim_frac, "body_px": int(len(B)), "rim_px": int(len(R)),
       "rule": "contiguous BODY support around a local peak, trimmed at trim_frac of that "
               "band's OWN peak; rim pixels excluded so contamination cannot set an edge",
       "bands": {}, "sensitivity": {}}

# the peaks: the two largest body modes, found rather than assumed
used = np.zeros(nb, bool)
peaks = []
for _ in range(3):
    cand = np.where(~used, hb, -1)
    i = int(np.argmax(cand))
    if cand[i] <= 0:
        break
    peaks.append(i)
    lo, hi = grow(i, 0.01)
    j = lo
    while True:
        used[j] = True
        if j == hi:
            break
        j = (j + 1) % nb
print("[edges] body peaks found at hue %s"
      % ", ".join("%.0f (%s px)" % (mid[i], f"{int(hb[i]):,}") for i in peaks))

for frac in (0.01, 0.02, 0.05, 0.10):
    rows = []
    for i in peaks:
        lo, hi = grow(i, frac)
        m = np.zeros(nb, bool)
        j = lo
        while True:
            m[j] = True
            if j == hi:
                break
            j = (j + 1) % nb
        rows.append({"peak_hue": round(float(mid[i]), 1),
                     "lo": round(float(e[lo]), 1), "hi": round(float(e[hi] + args.bin), 1),
                     "span_deg": round(span_deg(lo, hi), 1),
                     "body_px": int(hb[m].sum()), "rim_px": int(hr[m].sum())})
    out["sensitivity"][str(frac)] = rows
    tag = "  <- THE RULE AS STATED" if abs(frac - args.trim_frac) < 1e-9 else ""
    print("\n[edges] trim at %4.0f%% of each band's own peak%s" % (100 * frac, tag))
    for r in rows:
        print("[edges]   peak %5.1f -> band %5.1f - %5.1f  span %5.1f deg  "
              "BODY %7s px  rim %7s px"
              % (r["peak_hue"], r["lo"], r["hi"], r["span_deg"],
                 f"{r['body_px']:,}", f"{r['rim_px']:,}"))
    if abs(frac - args.trim_frac) < 1e-9:
        out["bands"] = rows

cov = np.zeros(nb, bool)
for r in out["bands"]:
    lo_i = int(r["lo"] / args.bin) % nb
    hi_i = int((r["hi"] / args.bin - 1)) % nb
    j = lo_i
    while True:
        cov[j] = True
        if j == hi_i:
            break
        j = (j + 1) % nb
print("\n[edges] FORBIDDEN SPAN above the floor: %.0f deg = %.1f%% of the hue circle"
      % ((~cov).sum() * args.bin, 100.0 * (~cov).mean()))
print("[edges] body px OUTSIDE every band: %s (%.3f%% of body)"
      % (f"{int(hb[~cov].sum()):,}", 100.0 * hb[~cov].sum() / max(len(B), 1)))
print("[edges] rim  px OUTSIDE every band: %s (%.3f%% of rim)"
      % (f"{int(hr[~cov].sum()):,}", 100.0 * hr[~cov].sum() / max(len(R), 1)))
out["forbidden_span_deg"] = float((~cov).sum() * args.bin)
out["body_outside_bands_px"] = int(hb[~cov].sum())
out["rim_outside_bands_px"] = int(hr[~cov].sum())

if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(out, open(args.out, "w"), indent=1)
    print("[edges] wrote %s" % args.out)
