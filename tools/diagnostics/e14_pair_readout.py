"""The styled pair's pre-registered readout — E14 Ruling 7b's checks, plus element landing.

WHAT RULING 7b PRE-REGISTERED, before this artifact existed, and what this measures:

  (a) L1's realised LIGHTNESS AND CHROMA. The named risk is cool-cast materialisation —
      worn steel arriving ABOVE the C* 5.0 floor INSIDE blue-violet's own 225-300 band,
      i.e. the ruled backdrop bleeding into the subject's largest and most vulnerable
      surface. Reported with its hue ONLY where chroma clears the floor, because below the
      floor a hue is not a colour (CLAUDE.md; the same fact has bitten two instruments here).
  (b) The realised BACKDROP's own L*/C* against the derivation's estimate
      (214,214,255 · L* 86.9 · C* 21.4). The beast's realised C* 11.0 is the precedent for
      the estimate coming back weaker than derived.

WHAT IT DOES NOT DO. It arms nothing and rules nothing. The word is NOT re-chosen on what
this prints — Ruling 7b says so in terms: "the word is not re-chosen while looking at the
artifact it would judge." And no numeric gate is placed on L5 (the D8 lesson: an element
below any area floor is judged by eye at the hilt crop, never by a number).

REGIONS ARE THE MESH'S, NOT THE IMAGE'S. The figure comes from the exact raycast silhouette
at the same frame, never from keying the generated image — corner-median keying is retired
and the generated backdrop is exactly the painted-studio-backdrop case that killed it. The
blade region is the Gate 0 landmark's (shoulder at 69.46% of height), the same box the thin
curve used, so the two readouts speak about the same surface.

  e14_pair_readout.py --pair P.png --mask M.png --label view0 [--shoulder-frac 0.694594]
                      [--out j.json]

Standards compliance: PIN_PER_STEP - every region boundary is a flag with a recorded default
and lands in the JSON. ANDON_AUTHORITY - none; this reports. DECOMPOSE_BY_SECRETS - the
chroma floor is a stated constant with its reason, not folded into a hue table.
EXTERNAL_VERIFIER - the sRGB->Lab path is re-derived here and asserted against
e14_backdrop_checks.py's on the estimate triple, so the pair and the derivation are quoted in
one colour space rather than two.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--pair", required=True)
ap.add_argument("--mask", required=True, help="the EXACT mesh silhouette at this frame")
ap.add_argument("--label", required=True)
ap.add_argument("--shoulder-frac", type=float, default=0.694594,
                help="Gate 0's blade shoulder as a fraction of height above the tip")
ap.add_argument("--chroma-floor", type=float, default=5.0)
ap.add_argument("--hilt-band", type=float, default=0.80,
                help="rows above this fraction of height are the hilt band for reporting")
ap.add_argument("--erode", type=int, default=0,
                help="erode the figure mask by N px before reading. THE RIM IS THE REASON: "
                     "antialiased pixels just inside the silhouette mix with the backdrop, "
                     "so on a lavender ground they carry lavender chroma and inflate any "
                     "'L1 cleared the chroma floor' count without any cast existing. Same "
                     "move that settled the off-surface question this session - if the "
                     "above-floor share collapses under erosion it was perimeter mixing, "
                     "and a thin blade is proportionally MORE perimeter than any prior "
                     "subject.")
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


# EXTERNAL_VERIFIER: the same conversion the derivation used, on the derivation's own triple
_est = srgb_to_lab(np.array([[214, 214, 255]]) / 255.0)[0]
assert abs(_est[0] - 86.9) < 0.1 and abs(np.hypot(_est[1], _est[2]) - 21.4) < 0.1, (
    "ANDON: this file's sRGB->Lab disagrees with e14_backdrop_checks.py on the estimate "
    "triple (got L* %.2f C* %.2f against the recorded 86.9 / 21.4)"
    % (_est[0], np.hypot(_est[1], _est[2])))

img = np.asarray(Image.open(args.pair).convert("RGB")).astype(np.float64) / 255.0
msk = np.asarray(Image.open(args.mask).convert("L")) > 127
if args.erode:
    import cv2
    k = np.ones((2 * args.erode + 1, 2 * args.erode + 1), np.uint8)
    msk = cv2.erode(msk.astype(np.uint8), k, iterations=1) > 0
assert img.shape[:2] == msk.shape, ("ANDON: pair %s and mask %s differ in shape"
                                    % (img.shape[:2], msk.shape))
H, W = msk.shape
lab = srgb_to_lab(img)
L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
C = np.hypot(A, B)
Hue = np.degrees(np.arctan2(B, A)) % 360.0

rows = np.arange(H)[:, None] * np.ones((1, W))
frac_above_tip = 1.0 - (rows + 0.5) / H          # 0 at the bottom (tip), 1 at the top
blade = msk & (frac_above_tip < args.shoulder_frac)
hilt = msk & (frac_above_tip >= args.hilt_band)
bg = ~msk


def band(name, sel):
    n = int(sel.sum())
    if n < 50:
        return {"name": name, "px": n, "note": "too few px to report"}
    c = C[sel]
    above = c >= args.chroma_floor
    d = {"name": name, "px": n,
         "L_median": round(float(np.median(L[sel])), 2),
         "L_p05": round(float(np.percentile(L[sel], 5)), 2),
         "L_p95": round(float(np.percentile(L[sel], 95)), 2),
         "C_median": round(float(np.median(c)), 2),
         "C_p95": round(float(np.percentile(c, 95)), 2),
         "pct_above_chroma_floor": round(100.0 * float(above.mean()), 2),
         "rgb_median": [int(round(np.median(img[..., i][sel]) * 255)) for i in range(3)]}
    if above.any():
        hv = Hue[sel][above]
        d["hue_median_of_above_floor"] = round(float(np.median(hv)), 1)
        d["pct_in_blue_violet_225_300"] = round(
            100.0 * float(((hv >= 225) & (hv < 300)).mean()), 2)
        d["pct_of_band_in_blue_violet"] = round(
            100.0 * float(((hv >= 225) & (hv < 300)).sum()) / n, 2)
    else:
        d["hue_median_of_above_floor"] = None
    return d


out = {"label": args.label, "pair": os.path.abspath(args.pair),
       "chroma_floor": args.chroma_floor, "shoulder_frac": args.shoulder_frac,
       "frame": [W, H], "figure_px": int(msk.sum()),
       "estimate_backdrop": {"rgb": [214, 214, 255], "L": 86.9, "C": 21.4},
       "bands": {}}
print("[pair] %s  frame %dx%d  figure %s px (%.2f%% of frame)"
      % (args.label, W, H, f"{int(msk.sum()):,}", 100.0 * msk.mean()))
print("[pair] %-22s %8s %8s %8s %8s %8s %10s %8s %s"
      % ("band", "px", "L*med", "L*p05", "L*p95", "C*med", ">=floor%", "hue", "rgb"))
for nm, sel in (("L1 blade region", blade), ("hilt band (top 20%)", hilt),
                ("figure, all", msk), ("BACKDROP", bg)):
    d = band(nm, sel)
    out["bands"][nm] = d
    if "L_median" not in d:
        print("[pair] %-22s %8d   %s" % (nm, d["px"], d["note"]))
        continue
    hs = ("%.0f" % d["hue_median_of_above_floor"]
          if d["hue_median_of_above_floor"] is not None else "UNDEF")
    print("[pair] %-22s %8s %8.2f %8.2f %8.2f %8.2f %9.2f%% %8s %s"
          % (nm, f"{d['px']:,}", d["L_median"], d["L_p05"], d["L_p95"], d["C_median"],
             d["pct_above_chroma_floor"], hs, d["rgb_median"]))

# --- Ruling 7b (a): the cool-cast question, stated as the ruling framed it -----------------
b = out["bands"]["L1 blade region"]
print()
print("[7b-a] L1 REALISED: L* %.2f  C* %.2f  (floor %.1f)"
      % (b["L_median"], b["C_median"], args.chroma_floor))
if b["C_median"] < args.chroma_floor:
    print("[7b-a] L1's median chroma is BELOW the floor - steel arrived achromatic, its hue "
          "undefined and NOT quoted. The pre-registered cool-cast risk did not materialise "
          "at the median.")
else:
    print("[7b-a] ⚠ L1's median chroma CLEARS the floor at hue %s - %.2f%% of the blade "
          "region sits inside blue-violet's own 225-300 band. This is the pre-registered "
          "cool-cast risk materialising; it is a FINDING for the palette-bands derivation, "
          "and the word is NOT re-chosen on it (Ruling 7b)."
          % (b.get("hue_median_of_above_floor"), b.get("pct_of_band_in_blue_violet", 0.0)))
print("[7b-a] blade px above the floor: %.2f%%   (a median can hide a tail)"
      % b["pct_above_chroma_floor"])

# --- Ruling 7b (b): the realised backdrop against the estimate -----------------------------
g = out["bands"]["BACKDROP"]
print()
print("[7b-b] BACKDROP REALISED rgb%s  L* %.2f  C* %.2f   against the ESTIMATE "
      "rgb[214, 214, 255]  L* 86.9  C* 21.4"
      % (g["rgb_median"], g["L_median"], g["C_median"]))
print("[7b-b] delta: L* %+.2f   C* %+.2f   (the beast's precedent: realised C* came back "
      "WEAKER than derived)" % (g["L_median"] - 86.9, g["C_median"] - 21.4))
out["deltas_vs_estimate"] = {"L": round(g["L_median"] - 86.9, 2),
                             "C": round(g["C_median"] - 21.4, 2)}

if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(out, open(args.out, "w"), indent=1)
    print("\n[pair] wrote %s" % args.out)
