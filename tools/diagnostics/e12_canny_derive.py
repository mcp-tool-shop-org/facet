"""E12 handoff 4 Task 1 — derive the BEAST's Canny threshold pair, measured on its own clay.

E12 Ruling 10c: the profile's 0.4/0.8 is a FIRST-RUN OPERATING POINT carried from an accepted
route and never derived for this subject, and it leaves the figure interior almost empty --
so at denoise 0.92 the interior was the model's to invent, and it invented a generic dragon.
This file measures the curve the replacement is chosen from. It ADOPTS NOTHING and ARMS NO
GATE (Ruling 10d: the structural channel at a style gate is the eye).

WHAT IT REPLICATES, AND WHY REPLICATION IS NOT DUPLICATION
`restylize_views.control_image` is the one place that knows how a control is built, and this
file does not fork it: it reproduces the same three lines

    comp  = rgb * fm + BG * (1 - fm)
    grey  = (comp.mean(-1) * 255).astype(uint8)
    edges = cv2.Canny(grey, int(low * 255), int(high * 255))

and then ANCHORS itself against that tool's own recorded output before any sweep number is
believed -- the validated-before-used pattern (E12 Ruling 6c). `restylize_views.py` cannot be
imported: it runs argparse at module scope. So the arithmetic is replicated and then checked
against digits the tool actually printed, rather than trusted because it looks the same.

THE WORKS-PERFECTLY TEST, WHICH IS THE POINT OF THE FILE
A lower pair "works" when what it admits is mesh RELIEF and "fails" when what it admits is
render ARTIFACT. Those must not evaluate to the same number, so four instruments separate
them (definitions and pre-registered predictions: E12-task1-canny-predictions.md):

  W-outside  admitted px outside the figure, past a 5 px boundary ring.  Artifact -> large.
  W-band     admitted px whose Sobel |Gx|+|Gy| <= 8, the two-LSB step of an 8-bit render.
             A 1-LSB quantization contour in smooth shading measures ~4.  Banding -> large.
             HAS CONTENT ONLY where int(low*255) <= 8 -- above that the candidate's own low
             threshold is a floor on this quantity and the test is circular. Reported as
             `null` where it is circular rather than as a flattering zero.
  W-flat     admitted px whose LOCAL 15x15 grey range (max - min) is small -- i.e. edges
             found in a neighbourhood that has no contrast to carry one. ADDED AFTER the
             crops, and the reason is recorded rather than hidden: W-band measured 1.34-2.82%
             at the bottom rung and said the bottom rung was clean, while the 5x membrane
             crop showed a whole population of wandering closed contours in a flat field
             there. W-band asks about the gradient AT the pixel, which Canny's own low
             threshold bounds from below; the artifact's pixels clear that bar (2-4 LSB
             steps, magnitude ~10-16) and only their NEIGHBOURHOOD gives them away. E07's
             lesson in a new instrument: a per-pixel statistic cannot separate what a look
             separates. Both are reported; neither is a gate.
  W-speckle  admitted px in 8-connected components of <= 3 px.  AA speckle -> large.
  crops      the eye, which is the gate here. --crop VIEW:x0,y0,x1,y1:name, 5x, admitted
             set overlaid on the render.

  e12_canny_derive.py --renders DIR --masks DIR --tag dragonclay --views 1,2,4,5
                      --out DIR [--crop 1:x0,y0,x1,y1:name ...]

Standards compliance. PIN_PER_STEP: the grid, the views, the erosion depths and the anchor
digits are arguments with recorded defaults, and every row lands in one JSON beside the
sheet. ANDON_AUTHORITY: the anchor raises before a single sweep row is written -- there is no
skip flag, because an instrument that cannot reproduce the tool it replicates is measuring a
different object. NAMED_COMPENSATORS: writes only into --out; undo = delete the directory.
DECOMPOSE_BY_SECRETS: no subject constant is baked in -- the mask tag, the views, the crops
and the composite background all arrive as arguments. EXTERNAL_VERIFIER: the file emits a
curve and adopts nothing; the crops exist so a human checks the admitted set rather than
believing this file about it.
"""
import argparse
import json
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_erosion, binary_dilation

# The grid, pre-registered in E12-task1-canny-predictions.md before any measurement.
GRID = [(0.02, 0.06), (0.03, 0.09), (0.05, 0.15), (0.08, 0.20), (0.10, 0.25), (0.12, 0.30),
        (0.15, 0.35), (0.20, 0.45), (0.25, 0.55), (0.30, 0.65), (0.40, 0.80),
        (0.05, 0.10), (0.05, 0.20), (0.05, 0.30), (0.10, 0.20), (0.10, 0.40)]
REF = (0.40, 0.80)          # the profile's falsified pair; the admitted set is measured against it

ap = argparse.ArgumentParser()
ap.add_argument("--renders", required=True, help="dir of profile-rendered clay views")
ap.add_argument("--masks", required=True, help="dir of exact mesh silhouettes, same tag")
ap.add_argument("--tag", default="dragonclay")
ap.add_argument("--views", default="1,2,4,5")
ap.add_argument("--out", required=True)
ap.add_argument("--bg", default="0,0,0", help="composite background, restylize_views' --bg")
ap.add_argument("--erode", default="3,5,9", help="interior erosion depths in px")
ap.add_argument("--headline-erode", type=int, default=5)
ap.add_argument("--band-mag", type=float, default=8.0, help="W-band cut, the two-LSB step")
ap.add_argument("--speckle-max", type=int, default=3, help="W-speckle component size cut")
ap.add_argument("--flat-win", type=int, default=15, help="W-flat neighbourhood, px")
ap.add_argument("--flat-cuts", default="8,12,20",
                help="W-flat local-range cuts; three, so no single arbitrary one decides")
ap.add_argument("--anchor", action="append", default=[],
                help="VIEW=N - assert the replica's Canny count at REF equals N, the digit "
                     "restylize_views itself printed. Repeatable, no skip flag.")
ap.add_argument("--crop", action="append", default=[],
                help="VIEW:x0,y0,x1,y1:name - a 5x crop of the admitted set over the render")
ap.add_argument("--sheet", action="store_true",
                help="write a full-frame CONTROL comparison per view: the profile's pair "
                     "first, then each --crop-pairs candidate, contour term included")
ap.add_argument("--sheet-width", type=int, default=1200)
ap.add_argument("--contour-width", type=int, default=3,
                help="restylize_views' --contour-width, for the sheet's contour term")
ap.add_argument("--crop-pairs", default="0.05/0.15,0.10/0.25",
                help="which candidates the crops are drawn for, low/high comma-separated")
args = ap.parse_args()

os.makedirs(args.out, exist_ok=True)
VIEWS = [v.strip() for v in args.views.split(",") if v.strip()]
ERODE = [int(e) for e in args.erode.split(",")]
FLATCUTS = [int(c) for c in args.flat_cuts.split(",")]
BG = np.array([float(v) for v in args.bg.split(",")], dtype=np.float32)
if BG.max() > 1.0:
    BG = BG / 255.0


def load(view):
    """control_image's first three lines, and nothing else.

    ⚠ THE `.astype(np.float32)` ON THE MASK IS LOAD-BEARING AND WAS PAID FOR BY THIS FILE'S
    OWN ANCHOR. The first draft kept `fm` as bool, which is the obvious way to write it and
    is arithmetically identical on paper. It is not identical in float: `1.0 - fm` on a bool
    array promotes to float64, so the whole composite and its `.mean(axis=-1)` ran at double
    precision, and ~19 px per view landed on the other side of the `uint8` truncation and
    then on the other side of a Canny threshold. Measured: view 1 returned 35,992 against
    restylize_views' recorded 36,011 and view 5 returned 22,658 against 22,642 -- and both
    reproduce EXACTLY once the mask is float32, the dtype `control_image` writes.

    Second instance of this class in two sessions (E12 Ruling 9a was a normalisation that
    cancels mathematically and not in float32). The standing rule caught it both times:
    AN ANCHOR IS COMPUTED WITH THE SOURCE'S OWN ARITHMETIC -- not with arithmetic that is
    equivalent to it.
    """
    rgb = np.asarray(Image.open(os.path.join(args.renders, "%s_%s.png" % (args.tag, view))
                                ).convert("RGB"), dtype=np.float32) / 255.0
    fm = (np.asarray(Image.open(os.path.join(args.masks, "%s_%s.png" % (args.tag, view))
                                ).convert("L"), dtype=np.float32) / 255.0 > 0.5
          ).astype(np.float32)
    comp = rgb * fm[..., None] + BG * (1.0 - fm[..., None])
    grey = (comp.mean(axis=-1) * 255).astype(np.uint8)
    return rgb, fm > 0.5, grey


def canny(grey, low, high):
    return cv2.Canny(grey, int(low * 255), int(high * 255)) > 0


def sobel_mag(grey):
    """|Gx| + |Gy| on a 3x3 Sobel -- the quantity cv2.Canny thresholds with L2gradient=False."""
    gx = cv2.Sobel(grey, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(grey, cv2.CV_32F, 0, 1, ksize=3)
    return np.abs(gx) + np.abs(gy)


DATA = {}
for view in VIEWS:
    rgb, fm, grey = load(view)
    # local dynamic range: what contrast the NEIGHBOURHOOD has to justify an edge at all
    k = np.ones((args.flat_win, args.flat_win), np.uint8)
    lrange = (cv2.dilate(grey, k).astype(np.int16) - cv2.erode(grey, k).astype(np.int16))
    DATA[view] = {"rgb": rgb, "fm": fm, "grey": grey, "mag": sobel_mag(grey), "lrange": lrange,
                  "interior": {e: binary_erosion(fm, np.ones((2 * e + 1, 2 * e + 1), bool))
                               for e in ERODE},
                  "outside": ~binary_dilation(fm, np.ones((11, 11), bool)),
                  "ref": canny(grey, *REF)}

# --- THE ANCHOR: reproduce the digits restylize_views printed, or stop ---------------------
bad = []
for a in args.anchor:
    v, n = a.split("=")
    got = int(DATA[v.strip()]["ref"].sum())
    want = int(n)
    print("[anchor] view %s at %.2f/%.2f: replica %d px  recorded %d px  %s"
          % (v, REF[0], REF[1], got, want, "MATCH" if got == want else "*** MISMATCH ***"),
          flush=True)
    if got != want:
        bad.append("view %s: replica %d != recorded %d" % (v, got, want))
if bad:
    raise SystemExit(
        "ANDON: the replica does not reproduce restylize_views' own recorded Canny counts:\n"
        "  %s\nNothing was swept. An instrument that cannot reproduce the tool it replicates "
        "is measuring a different object, and no curve from it is worth reading. This check "
        "has no skip flag." % "\n  ".join(bad))

# --- the sweep ----------------------------------------------------------------------------
rows = []
for (low, high) in GRID:
    for view in VIEWS:
        d = DATA[view]
        e = canny(d["grey"], low, high)
        row = {"low": low, "high": high, "int_low": int(low * 255), "int_high": int(high * 255),
               "view": view, "canny_px": int(e.sum()),
               "figure_px": int(d["fm"].sum())}
        for k in ERODE:
            inte = d["interior"][k]
            row["interior_px_e%d" % k] = int(inte.sum())
            row["interior_edge_pct_e%d" % k] = round(
                100.0 * float((e & inte).sum()) / max(int(inte.sum()), 1), 4)
        # the admitted set: what lowering the pair BUYS, against the profile's own pair
        adm = e & ~d["ref"]
        na = int(adm.sum())
        row["admitted_px"] = na
        row["lost_px"] = int((d["ref"] & ~e).sum())
        if na:
            row["W_outside_px"] = int((adm & d["outside"]).sum())
            row["W_outside_pct"] = round(100.0 * float((adm & d["outside"]).sum()) / na, 4)
            # W-band has content ONLY below the candidate's own low threshold; above it the
            # threshold is a floor on the magnitude and the test would be circular.
            if row["int_low"] <= args.band_mag:
                row["W_band_pct"] = round(
                    100.0 * float((adm & (d["mag"] <= args.band_mag)).sum()) / na, 4)
            else:
                row["W_band_pct"] = None
            for c in FLATCUTS:
                row["W_flat%d_pct" % c] = round(
                    100.0 * float((adm & (d["lrange"] <= c)).sum()) / na, 4)
            n_lab, lab, stats, _ = cv2.connectedComponentsWithStats(
                adm.astype(np.uint8), connectivity=8)
            sizes = stats[1:, cv2.CC_STAT_AREA]
            small = sizes[sizes <= args.speckle_max].sum()
            row["W_speckle_pct"] = round(100.0 * float(small) / na, 4)
            row["admitted_components"] = int(n_lab - 1)
            row["admitted_median_component"] = float(np.median(sizes)) if len(sizes) else 0.0
            row["admitted_mag_median"] = round(float(np.median(d["mag"][adm])), 3)
        rows.append(row)
        print("[sweep] %5.2f/%4.2f (%3d/%3d) view %s  canny %7d  interior(e%d) %6.3f%%  "
              "admitted %7d  W-out %s  W-band %s  W-speck %s  W-flat%d %s"
              % (low, high, row["int_low"], row["int_high"], view, row["canny_px"],
                 args.headline_erode, row["interior_edge_pct_e%d" % args.headline_erode], na,
                 ("%.3f%%" % row["W_outside_pct"]) if na else "-",
                 ("%.2f%%" % row["W_band_pct"]) if na and row["W_band_pct"] is not None
                 else "n/a",
                 ("%.2f%%" % row["W_speckle_pct"]) if na else "-",
                 FLATCUTS[1],
                 ("%.2f%%" % row["W_flat%d_pct" % FLATCUTS[1]]) if na else "-"), flush=True)

# --- the 8-bit quantization comb, measured on this subject's own renders ------------------
comb = {}
for view in VIEWS:
    d = DATA[view]
    inte = d["interior"][args.headline_erode]
    m = d["mag"][inte]
    comb[view] = {"n": int(inte.sum()),
                  "pct_le_4": round(100.0 * float((m <= 4).mean()), 3),
                  "pct_le_8": round(100.0 * float((m <= 8).mean()), 3),
                  "pct_le_12": round(100.0 * float((m <= 12).mean()), 3),
                  "pct_le_25": round(100.0 * float((m <= 25).mean()), 3),
                  "pct_le_102": round(100.0 * float((m <= 102).mean()), 3),
                  "median": round(float(np.median(m)), 3),
                  "p90": round(float(np.percentile(m, 90)), 3),
                  "p99": round(float(np.percentile(m, 99)), 3)}

# --- crops: the admitted set over the render, 5x, for the eye -----------------------------
CROPPAIRS = []
for s in args.crop_pairs.split(","):
    lo, hi = s.split("/")
    CROPPAIRS.append((float(lo), float(hi)))

for spec in args.crop:
    view, box, name = spec.split(":")
    x0, y0, x1, y1 = [int(v) for v in box.split(",")]
    d = DATA[view.strip()]
    tiles = []
    base = (d["rgb"] * 255).astype(np.uint8)[y0:y1, x0:x1]
    tiles.append(("render", base))
    for (lo, hi) in CROPPAIRS:
        e = canny(d["grey"], lo, hi)
        adm = (e & ~d["ref"])[y0:y1, x0:x1]
        ref = d["ref"][y0:y1, x0:x1]
        ov = base.copy()
        ov[ref] = (90, 160, 255)        # what the PROFILE's pair already had -- blue
        ov[adm] = (255, 210, 60)        # what this candidate ADMITS -- amber
        tiles.append(("%.2f/%.2f" % (lo, hi), ov))
    S = 5
    w, h = (x1 - x0) * S, (y1 - y0) * S
    hdr, gap = 22, 6
    sheet = Image.new("RGB", (w * len(tiles) + gap * (len(tiles) - 1), h + hdr), (18, 18, 20))
    dr = ImageDraw.Draw(sheet)
    for i, (lab, arr) in enumerate(tiles):
        im = Image.fromarray(arr).resize((w, h), Image.NEAREST)
        x = i * (w + gap)
        dr.text((x + 4, 5), "%s  %s" % (name, lab), fill=(255, 210, 90))
        sheet.paste(im, (x, hdr))
    p = os.path.join(args.out, "CROP_%s_%s.png" % (view.strip(), name))
    sheet.save(p)
    print("[crop] %s  view %s  box %d,%d..%d,%d  5x -> %s"
          % (name, view, x0, y0, x1, y1, os.path.basename(p)), flush=True)

# --- the full-frame sheet: the CONTROL as the generator would see it, per candidate --------
# The contour term is the mask's morphological gradient, identical for every candidate by
# construction (it does not depend on a threshold) -- so the sheet shows the whole control,
# not just the Canny half, and the difference between panels is exactly what the pair buys.
if args.sheet:
    pairs = [REF] + CROPPAIRS
    for view in VIEWS:
        d = DATA[view]
        k = np.ones((args.contour_width, args.contour_width), np.uint8)
        contour = cv2.morphologyEx(d["fm"].astype(np.uint8) * 255, cv2.MORPH_GRADIENT, k)
        tiles = []
        for (lo, hi) in pairs:
            ctrl = np.maximum(canny(d["grey"], lo, hi).astype(np.uint8) * 255, contour)
            tiles.append(("%.2f/%.2f  (%d/%d)  %s px"
                          % (lo, hi, int(lo * 255), int(hi * 255),
                             "{:,}".format(int((ctrl > 0).sum()))), ctrl))
        W = args.sheet_width
        h = int(round(W * d["grey"].shape[0] / d["grey"].shape[1]))
        hdr = 24
        sheet = Image.new("RGB", (W, (h + hdr) * len(tiles)), (12, 12, 14))
        dr = ImageDraw.Draw(sheet)
        for i, (lab, arr) in enumerate(tiles):
            im = Image.fromarray(arr).resize((W, h), Image.BILINEAR).convert("RGB")
            y = i * (h + hdr)
            dr.text((6, y + 6), "view %s   CONTROL at %s%s"
                    % (view, lab, "   <- the profile's pair" if i == 0 else ""),
                    fill=(255, 210, 90))
            sheet.paste(im, (0, y + hdr))
        p = os.path.join(args.out, "CONTROL_SHEET_%s.png" % view)
        sheet.save(p)
        print("[sheet] view %s -> %s" % (view, os.path.basename(p)), flush=True)

out = {"grid": [list(g) for g in GRID], "ref_pair": list(REF), "views": VIEWS,
       "erode": ERODE, "headline_erode": args.headline_erode, "bg": args.bg,
       "band_mag_cut": args.band_mag, "speckle_max": args.speckle_max,
       "flat_win": args.flat_win, "flat_cuts": FLATCUTS,
       "anchors": args.anchor, "gradient_comb": comb, "rows": rows}
with open(os.path.join(args.out, "canny_sweep.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)

print("\n[comb] Sobel |Gx|+|Gy| inside the interior (e%d) -- the 8-bit quantization floor"
      % args.headline_erode)
print("       %-6s %10s %8s %8s %8s %8s %8s %8s"
      % ("view", "n", "<=4", "<=8", "<=12", "<=25", "median", "p99"))
for v in VIEWS:
    c = comb[v]
    print("       %-6s %10s %7.2f%% %7.2f%% %7.2f%% %7.2f%% %8.1f %8.1f"
          % (v, "{:,}".format(c["n"]), c["pct_le_4"], c["pct_le_8"], c["pct_le_12"],
             c["pct_le_25"], c["median"], c["p99"]))
print("\n[out] %s" % os.path.join(args.out, "canny_sweep.json"))
