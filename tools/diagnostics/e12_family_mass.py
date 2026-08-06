"""How much of a named region wears a named COLOUR FAMILY - reported per image, never gated.

WHY THIS EXISTS. The defect the Director named ("the bones on the outside of the legs, bottom
of the tail and arms") is the E07 class: a LARGE REGION OF THE WRONG MATERIAL. E07 proved that
five 5x5 high-pass statistics cannot see it - a region of the wrong colour is smooth inside
itself and contributes only its rim. What DOES see it is area: how many pixels of a declared
colour family sit inside a region, and how big the largest connected blob of them is.

THIS IS A DIAGNOSTIC AND NOT A GATE (E12 Ruling 10d; CLAUDE.md - the E07 class is judged by
eye). It emits numbers beside a sheet. It adopts nothing, decides nothing, and no threshold
in it is a pass condition.

FOUR THINGS IT DOES ON PURPOSE, each paid for by a rule in CLAUDE.md:

  * MASKS TO THE GEOMETRY SILHOUETTE FIRST. The ruled backdrop is `plain lavender-grey`, which
    at ~(185,180,195) is L* 74 / C* 6 - INSIDE the pale-bone band. An unmasked pale-family
    count on this subject would be dominated by the backdrop and would mean nothing. The
    silhouette answers `is there surface` and is the right operand (E08 A27's distinction).
  * QUOTES NO HUE BELOW A CHROMA FLOOR. The pale-bone family is DEFINED by low chroma, so it
    is keyed on L* and C* jointly and the hue column is not printed for it. Hue is only used
    for the red/pink family, which carries a C* floor of its own. (Two instruments in this
    repo were bitten by reading hue where chroma had collapsed.)
  * REPORTS THE TOTAL *AND* THE LARGEST CONNECTED COMPONENT. Clean views carry speckle at
    material boundaries; one wrong garment is a blob. A total alone must choose between
    missing the garment and firing on everything.
  * NORMALISES BY THE MASKED AREA OF THE REGION IT WAS GIVEN, and prints that denominator, so
    a percentage can never be read without the thing it is a percentage of.

CHECK IT AGAINST A KNOWN RESULT BEFORE BELIEVING A NEW ONE: --expect lets a caller assert a
published figure on a published artifact, and the tool prints whether it reproduced. A number
from an instrument that has not been re-measured against a case whose answer is already in
the record is not evidence.

  e12_family_mass.py --image LABEL=PATH ... --mask M.png
                     --region x0,y0,x1,y1:name ... --family pale|redpink
                     [--out J.json] [--expect LABEL:name:N]

NAMED_COMPENSATORS: writes at most one JSON (--out); undo = delete it. Reads everything else.
"""
import argparse
import json

import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import color

ap = argparse.ArgumentParser()
ap.add_argument("--image", action="append", required=True, help="LABEL=PATH, repeatable")
ap.add_argument("--mask", required=True, help="geometry silhouette for this view (L, >127 = on)")
ap.add_argument("--region", action="append", required=True, help="x0,y0,x1,y1:name, repeatable")
ap.add_argument("--family", default="pale", choices=["pale", "redpink", "charcoal"])
ap.add_argument("--l-min", type=float, default=62.0, help="pale: L* floor")
ap.add_argument("--c-max", type=float, default=20.0, help="pale: C* ceiling")
ap.add_argument("--c-min", type=float, default=12.0, help="redpink: C* floor")
# CHARCOAL, added at handoff 11 for the mirror image of the defect Ruling 12e fixed. There, a
# five-term pale-bone family painted skeleton down a green-declared body. Here the palette
# correction put THREE charcoal terms in the string (neck spines, dorsal/tail spines, claws)
# and the eye caught green-declared limbs arriving charcoal. Same instrument, other end of L*:
# keyed on L* and C* JOINTLY with no hue quoted, because below a chroma floor hue is undefined.
ap.add_argument("--l-max", type=float, default=38.0, help="charcoal: L* ceiling")
ap.add_argument("--charcoal-c-max", type=float, default=15.0, help="charcoal: C* ceiling")
ap.add_argument("--no-mask", action="store_true",
                help="measure the raw box with NO silhouette restriction. Printed loudly, "
                     "because on this subject the backdrop sits inside the pale band.")
ap.add_argument("--expect", action="append", default=[],
                help="LABEL:region:N - assert a published figure reproduces on a published "
                     "artifact. Printed as reproduced / not, never used to change a result.")
ap.add_argument("--out", default=None)
args = ap.parse_args()

IMAGES = [s.split("=", 1) for s in args.image]
REGIONS = []
for spec in args.region:
    box, _, name = spec.rpartition(":")
    REGIONS.append((name, [int(t) for t in box.split(",")]))

M = np.array(Image.open(args.mask).convert("L")) > 127
print("[mask] %s  on=%d px (%.3f%% of frame)  %s"
      % (args.mask.split("\\")[-1].split("/")[-1], M.sum(), 100.0 * M.mean(),
         "IGNORED (--no-mask)" if args.no_mask else "applied"))
if args.family == "pale":
    print("[family] PALE-BONE: L* >= %.1f AND C* <= %.1f. Hue is NOT quoted - below a chroma "
          "floor hue is undefined, and this family is defined by low chroma." % (args.l_min,
                                                                                args.c_max))
elif args.family == "charcoal":
    print("[family] CHARCOAL: L* <= %.1f AND C* <= %.1f. Hue is NOT quoted - same reason as "
          "pale, at the other end of L*. Mirror of the Ruling 12e defect: there five pale-bone "
          "terms painted skeleton onto green; the string now carries THREE charcoal terms."
          % (args.l_max, args.charcoal_c_max))
else:
    print("[family] RED/PINK: C* >= %.1f AND hue in [340,360) U [0,30) deg. Criterion "
          "transcribed from the handoff-5 report so the recurrence test runs the identical "
          "instrument." % args.c_min)

out = {"_family": args.family, "_mask": args.mask, "_masked": not args.no_mask,
       "_bands": ({"L_min": args.l_min, "C_max": args.c_max} if args.family == "pale"
                  else {"L_max": args.l_max, "C_max": args.charcoal_c_max}
                  if args.family == "charcoal"
                  else {"C_min": args.c_min, "hue_deg": "[340,360) U [0,30)"}),
       "_this_is_a_diagnostic_not_a_gate": "E12 Ruling 10d. No threshold here is a pass "
                                           "condition; the eye rules the E07 class.",
       "images": {}}

for label, path in IMAGES:
    rgb = np.array(Image.open(path).convert("RGB"))
    if rgb.shape[:2] != M.shape:
        raise SystemExit("ANDON: %s is %s but the mask is %s - a masked count across two "
                         "frames measures nothing." % (path, rgb.shape[:2], M.shape))
    lab = color.rgb2lab(rgb / 255.0)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    C = np.hypot(A, B)
    if args.family == "pale":
        fam = (L >= args.l_min) & (C <= args.c_max)
    elif args.family == "charcoal":
        fam = (L <= args.l_max) & (C <= args.charcoal_c_max)
    else:
        h = np.degrees(np.arctan2(B, A)) % 360.0
        fam = (C >= args.c_min) & ((h >= 340.0) | (h < 30.0))
    print("\n=== %s" % label)
    out["images"][label] = {"_path": path, "regions": {}}
    for name, (x0, y0, x1, y1) in REGIONS:
        sub_f = fam[y0:y1, x0:x1]
        sub_m = np.ones_like(sub_f) if args.no_mask else M[y0:y1, x0:x1]
        denom = int(sub_m.sum())
        hit = sub_f & sub_m
        n = int(hit.sum())
        lbl, k = ndimage.label(hit)
        cc = int(ndimage.sum(hit, lbl, range(1, k + 1)).max()) if k else 0
        pct = (100.0 * n / denom) if denom else float("nan")
        # medians reported only over the hit set, and only the columns the family licenses
        if n:
            med_L = float(np.median(L[y0:y1, x0:x1][hit]))
            med_C = float(np.median(C[y0:y1, x0:x1][hit]))
        else:
            med_L = med_C = float("nan")
        print("   %-12s box %4d,%4d..%4d,%4d   masked area %7d px   family %7d px (%6.2f%%)"
              "   largest CC %7d   median L* %5.1f  C* %5.1f"
              % (name, x0, y0, x1, y1, denom, n, pct, cc, med_L, med_C))
        out["images"][label]["regions"][name] = {
            "box": [x0, y0, x1, y1], "masked_area_px": denom, "family_px": n,
            "family_pct_of_masked_area": None if denom == 0 else round(pct, 4),
            "largest_connected_component_px": cc,
            "median_Lstar": None if n == 0 else round(med_L, 2),
            "median_Cstar": None if n == 0 else round(med_C, 2)}

if args.expect:
    print("\n[validate] published figures re-measured on published artifacts:")
    for e in args.expect:
        lab_, name, want = e.split(":")
        got = out["images"][lab_]["regions"][name]["family_px"]
        print("   %-12s %-12s published %-8s measured %-8s  %s"
              % (lab_, name, want, got,
                 "REPRODUCED" if str(got) == want else "DOES NOT REPRODUCE - the instrument "
                                                      "is not the one that produced the "
                                                      "published figure; read the new "
                                                      "numbers accordingly"))
    out["_validation"] = args.expect

if args.out:
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print("\n[family-mass] wrote %s" % args.out)
