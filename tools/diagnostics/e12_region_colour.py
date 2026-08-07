"""Median Lab / chroma / hue inside named regions, masked to the silhouette — the tone channel.

WHY. Ruling 22b asks a question no instrument here answers: *are the membranes storm-grey now.*
`e12_twin_gate.py` answers "is anything outside the declared palette" and reports a hue
histogram over the whole figure; `e12_family_mass.py` answers "how much of a named family sits
in a box". Neither reports what colour a region actually IS. Ruling 22e then asks a second one —
*does the set read as ONE dragon* — which is the same measurement across views.

WHAT IT REPORTS, per image per region, over region ∩ silhouette:

  * median L*, C* and hue, with hue printed ONLY where the median chroma clears the floor.
    Below a chroma floor hue is undefined and it will read as a rotation — the rule that bit
    two instruments in this repo already, so the column is withheld rather than qualified.
  * the CHROMA DISTRIBUTION (share under the floor, and the 25/50/75 percentiles), because
    "neutral grey" is a statement about chroma and a median alone hides a bimodal region.
  * the share of masked pixels inside a caller-named hue band (`--band lo,hi`) — for D3 that
    is the ruled storm-grey family, so "how much of this membrane is actually in its band"
    is a number rather than an impression.
  * mean and sigma per Lab channel — the operands a colour-statistics transfer moves, so a
    harmonization pass can be read against the same instrument that measured its input.

⚠ A BOX IS A REGION OF SPACE, NOT A SEGMENTATION (Gate 0's caveat, carried from
`e12_region_crops.py`). A membrane box contains the finger struts crossing it; the struts are
thin and the sheet is bulk, so the median is the sheet's — but the number is the BOX's and the
caveat rides with it. Read it beside the crop, never alone.

  e12_region_colour.py --image LABEL=PATH ... --mask LABEL=PATH ...
                       --region x0,y0,x1,y1:name ... [--band 190,270] [--chroma-floor 12]
                       [--out J.json]

Regions may be given per image label as `LABEL:x0,y0,x1,y1:name` when views do not share a
frame position — the ordinary case here, since a world box projects to a different rect on
every yaw.

Standards compliance: PIN_PER_STEP — floor, band and every rect are arguments echoed into the
JSON. ANDON_AUTHORITY — none; this is a measurement and it says so. NAMED_COMPENSATORS — writes
at most one JSON. EXTERNAL_VERIFIER — it measures colour against a declaration written before
the images existed, and computes nothing the generator controls.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--image", action="append", required=True, metavar="LABEL=PATH")
ap.add_argument("--mask", action="append", required=True, metavar="LABEL=PATH")
ap.add_argument("--region", action="append", required=True,
                metavar="[LABEL:]x0,y0,x1,y1:name")
ap.add_argument("--band", default=None, metavar="LO,HI",
                help="hue band this region is DECLARED to occupy; the share inside it is "
                     "reported. Wraps if LO > HI.")
ap.add_argument("--chroma-floor", type=float, default=12.0,
                help="below this C* a pixel carries no usable hue (the gate's own floor)")
ap.add_argument("--out", default=None)
args = ap.parse_args()


def kv(specs, what):
    out = {}
    for s in specs:
        k, _, p = s.partition("=")
        assert p, f"ANDON: --{what} wants LABEL=PATH, got {s!r}"
        assert os.path.exists(p), f"ANDON: --{what} {k}: no such file {p}"
        out[k] = p
    return out


IM, MK = kv(args.image, "image"), kv(args.mask, "mask")
if set(IM) != set(MK):
    raise SystemExit("ANDON: labels differ — images %s masks %s" % (sorted(IM), sorted(MK)))

REG = {}          # label -> [(name, rect)]; label None = applies to every image
for spec in args.region:
    head, _, name = spec.rpartition(":")
    lab = None
    if head.count(":"):
        lab, _, head = head.partition(":")
    rect = [int(x) for x in head.split(",")]
    assert len(rect) == 4, f"ANDON: --region wants x0,y0,x1,y1:name, got {spec!r}"
    REG.setdefault(lab, []).append((name, rect))

BAND = None
if args.band:
    lo, hi = (float(x) for x in args.band.split(","))
    BAND = (lo, hi)


def to_lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


print("[colour] chroma floor C* %.1f — hue is withheld where the median does not clear it, "
      "because below a floor hue is undefined and reads as a rotation." % args.chroma_floor)
if BAND:
    print("[colour] declared band: hue %.1f-%.1f" % BAND)
print()
print("[colour] %-14s %-12s %8s | %6s %6s %7s | %8s %8s %8s | %s"
      % ("image", "region", "px", "L*", "C*", "hue", "C*<floor", "C* p25", "C* p75",
         "in-band" if BAND else ""))
rows = {}
for lab in sorted(IM, key=lambda s: (len(s), s)):
    rgb = np.asarray(Image.open(IM[lab]).convert("RGB"), np.float32) / 255.0
    fm = np.asarray(Image.open(MK[lab]).convert("L")) > 127
    if fm.shape != rgb.shape[:2]:
        raise SystemExit("ANDON: %s mask %s vs image %s" % (lab, fm.shape, rgb.shape[:2]))
    L = to_lab(rgb)
    C = np.hypot(L[..., 1], L[..., 2])
    Hd = np.degrees(np.arctan2(L[..., 2], L[..., 1])) % 360.0
    rows[lab] = {}
    for name, (x0, y0, x1, y1) in REG.get(lab, []) + REG.get(None, []):
        sel = np.zeros(fm.shape, bool)
        sel[y0:y1, x0:x1] = True
        sel &= fm
        n = int(sel.sum())
        if n == 0:
            print("[colour] %-14s %-12s %8d | EMPTY (region misses the silhouette)"
                  % (lab, name, 0))
            rows[lab][name] = {"px": 0, "rect": [x0, y0, x1, y1]}
            continue
        Ls, Cs, Hs = L[..., 0][sel], C[sel], Hd[sel]
        mC = float(np.median(Cs))
        under = float((Cs < args.chroma_floor).mean() * 100)
        p25, p75 = (float(v) for v in np.percentile(Cs, [25, 75]))
        # circular median is not defined the way a linear one is; the hue quoted is the median
        # of the pixels that CLEAR the floor, and it is withheld entirely when the region's own
        # median chroma does not.
        usable = Cs >= args.chroma_floor
        mH = float(np.median(Hs[usable])) if usable.any() else float("nan")
        inb = ""
        band_pct = None
        if BAND:
            lo, hi = BAND
            ok = ((Hs >= lo) & (Hs <= hi)) if lo <= hi else ((Hs >= lo) | (Hs <= hi))
            band_pct = float((ok & usable).mean() * 100)
            inb = "%7.2f%%" % band_pct
        hue_col = "%7.1f" % mH if mC >= args.chroma_floor else "  (n/a)"
        print("[colour] %-14s %-12s %8d | %6.1f %6.1f %s | %7.1f%% %8.1f %8.1f | %s"
              % (lab, name, n, float(np.median(Ls)), mC, hue_col, under, p25, p75, inb))
        rows[lab][name] = {
            "px": n, "rect": [x0, y0, x1, y1],
            "median_L": round(float(np.median(Ls)), 2), "median_C": round(mC, 2),
            "median_hue_of_pixels_clearing_floor": None if mC < args.chroma_floor
            else round(mH, 1),
            "hue_withheld_below_floor": bool(mC < args.chroma_floor),
            "chroma_under_floor_pct": round(under, 2),
            "chroma_p25": round(p25, 2), "chroma_p75": round(p75, 2),
            "in_declared_band_pct": None if band_pct is None else round(band_pct, 2),
            "lab_mean": [round(float(L[..., c][sel].mean()), 3) for c in range(3)],
            "lab_sigma": [round(float(L[..., c][sel].std()), 3) for c in range(3)],
        }

if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"_what": "median Lab / chroma / hue per named region, masked to the exact "
                            "silhouette. A BOX IS A REGION OF SPACE, NOT A SEGMENTATION — read "
                            "beside the crop. NO BOUND IS ARMED.",
                   "_chroma_floor": args.chroma_floor, "_declared_band": BAND,
                   "images": rows}, fh, indent=1)
        fh.write("\n")
    print("\n[colour] wrote %s" % args.out)
