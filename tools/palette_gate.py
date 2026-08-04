"""PALETTE GATE — does this twin contain material the specification never named?

WHY THIS EXISTS, and why it is the deliverable rather than the asset it was built for.
E08 Arm B generated eight twins from one specification. Seven contained exactly 0 px of colour
outside the spec's palette. View 6 came back with a NAVY BLUE SLEEVE on a tunic the
specification calls SLEEVELESS — 5,590 px, 6.17% of the figure, 4,882 of them in ONE connected
blob. View 2 is the same camera from the other side with the same prompt and renders correctly,
so it is neither the prompt nor the spec: it is a per-view roll, and every future character will
hit it.

Nothing in the route would have caught it. The twin would have been projected and the garment
painted onto the mesh. This is the defect class E07 established the shipped metrics are blind
to — *a large region of the wrong material*, smooth inside itself, contributing only its rim to
every 5x5 high-pass statistic. A blotch count cannot see it. A speckle score cannot see it. It
is the class that decided the Director's rejection.

RUN IT BEFORE PROJECTION, NOT AFTER. A contaminated twin is cheap to reject and expensive to
un-paint.

TWO NUMBERS, BECAUSE THEY ARE TWO DIFFERENT FAILURES. Total off-palette area and the LARGEST
CONNECTED COMPONENT. An invented garment is one big blob; antialiasing along a material boundary
is a similar total spread over hundreds of specks. A single total conflates them and would either
miss the garment or fire on every clean twin.

THE CHROMA FLOOR IS LOAD-BEARING, NOT A TUNING KNOB. Hue is undefined at low chroma — the same
fact that made the contradiction test's hue-delta column unreadable wherever chroma collapsed.
W3's steel greatsword measures C* 1.6-2.8 at hue 266-268, which is squarely inside the blue
band. Without the floor this gate flags the sword on every single view.

WHAT IT CANNOT DO, stated so a green light is not over-read: it tests COLOUR, not PLACEMENT.
Gold on the boots passes every band while being flatly wrong. It catches material that is not
in the specification at all — exactly and only the failure it was built from.

Standards compliance:
  PIN_PER_STEP — bands, chroma floor and both thresholds live in a versioned palette JSON, not
    in this file; the palette path and every threshold are echoed into the report.
  ANDON_AUTHORITY — exits non-zero when either bound is exceeded, so a loop halts rather than
    projecting a contaminated twin. --report-only downgrades it to a measurement.
  NAMED_COMPENSATORS — writes only an overlay PNG and a JSON report. Undo = delete them. No
    input is modified. Owner: the session running it.
  EXTERNAL_VERIFIER — it grades colour against a declaration written before the run; it does not
    decide whether the twin is good. It emits an overlay for a human.

  palette_gate.py --palette W3-palette.json --images twin_*.png --masks mask_*.png
                  [--out-json J.json] [--overlay DIR] [--report-only]
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import label

ap = argparse.ArgumentParser()
ap.add_argument("--palette", required=True)
ap.add_argument("--images", nargs="+", required=True)
ap.add_argument("--masks", nargs="+", required=True,
                help="figure mask per image, parallel to --images. The EXACT mesh silhouette — "
                     "a keyed mask would let background colour into the measurement, which is "
                     "the failure mode E01 and E08 A2 both paid for.")
ap.add_argument("--out-json")
ap.add_argument("--overlay", help="directory for per-image overlays marking the flagged texels")
ap.add_argument("--report-only", action="store_true",
                help="measure and report without a non-zero exit; the gate becomes a diagnostic")
args = ap.parse_args()

assert len(args.images) == len(args.masks), (
    f"ANDON: {len(args.masks)} masks for {len(args.images)} images — --masks is parallel "
    f"to --images")

PAL = json.load(open(args.palette, encoding="utf-8"))
BANDS = [(b["name"], float(b["hue_deg"][0]), float(b["hue_deg"][1])) for b in PAL["allowed_bands"]]
CMIN = float(PAL["min_chroma"])
# max_offpalette_pct may be null: WITHDRAWN 2026-08-04 because its stated derivation did not
# describe it (it cited a 0 px baseline that came from a different, blue-only check) and because
# its denominator moves 1.65x with camera angle while off-palette pixels scale with perimeter.
# A null bound reports the percentage as a DIAGNOSTIC and gates on the blob alone. It is not
# replaced with a looser number — withdrawing is not choosing a new threshold.
_mp = PAL["gate"].get("max_offpalette_pct")
MAXPCT = None if _mp is None else float(_mp)
MAXBLOB = int(PAL["gate"]["max_offpalette_blob_px"])


def to_lab(rgb):
    """sRGB -> linear -> XYZ (D65) -> Lab. Same transform as e08_deltaE.py."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16,
                     500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


print(f"[palette] {os.path.basename(args.palette)}: min_chroma {CMIN}  bands "
      f"{', '.join(f'{n} {lo:.0f}-{hi:.0f}deg' for n, lo, hi in BANDS)}", flush=True)
if MAXPCT is None:
    print(f"[palette] gate: largest blob <= {MAXBLOB:,} px. The percentage bound is WITHDRAWN "
          f"(see the palette JSON) — % is reported as a diagnostic and gates nothing, so "
          f"DIFFUSE off-palette contamination is currently unbounded.", flush=True)
else:
    print(f"[palette] gate: off-palette <= {MAXPCT}% of figure AND largest blob <= "
          f"{MAXBLOB:,} px", flush=True)
print(f"\n[palette] {'image':<22s} {'figure px':>10s} {'offpal':>9s} {'%':>7s} "
      f"{'blob':>8s}  verdict", flush=True)

rows, failed = [], []
for img_path, mask_path in zip(args.images, args.masks):
    rgb = np.asarray(Image.open(img_path).convert("RGB"), dtype=np.float32) / 255.0
    fm = np.asarray(Image.open(mask_path).convert("L"), dtype=np.float32) / 255.0 > 0.5
    assert fm.shape == rgb.shape[:2], (
        f"ANDON: mask {fm.shape} vs image {rgb.shape[:2]} for {img_path}")

    lab = to_lab(rgb)
    C = np.hypot(lab[..., 1], lab[..., 2])
    Hd = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0

    in_band = np.zeros(Hd.shape, bool)
    for _n, lo, hi in BANDS:
        in_band |= (Hd >= lo) & (Hd <= hi) if lo <= hi else ((Hd >= lo) | (Hd <= hi))

    off = (C > CMIN) & (~in_band) & fm
    n_off, n_fig = int(off.sum()), int(fm.sum())
    pct = 100.0 * n_off / max(n_fig, 1)

    lb, k = label(off)
    blob = int(np.bincount(lb.ravel())[1:].max()) if k else 0

    ok = (blob <= MAXBLOB) and (MAXPCT is None or pct <= MAXPCT)
    stem = os.path.basename(img_path)
    print(f"[palette] {stem:<22s} {n_fig:>10,} {n_off:>9,} {pct:>6.2f}% {blob:>8,}  "
          f"{'ok' if ok else 'OFF-PALETTE'}", flush=True)

    # what the off-palette mass actually is, so a failure is diagnosable not just flagged
    domin = None
    if n_off:
        hh = Hd[off]
        hist, edges = np.histogram(hh, bins=36, range=(0, 360))
        i = int(hist.argmax())
        domin = {"hue_lo": float(edges[i]), "hue_hi": float(edges[i + 1]),
                 "share_of_offpalette": round(float(hist[i] / hist.sum() * 100), 1),
                 "median_chroma": round(float(np.median(C[off])), 1),
                 "median_rgb": [int(v) for v in (np.median(rgb[off], axis=0) * 255).round()]}
        print(f"[palette]   dominant off-palette hue {domin['hue_lo']:.0f}-{domin['hue_hi']:.0f}deg "
              f"({domin['share_of_offpalette']:.0f}% of it), median C* {domin['median_chroma']}, "
              f"rgb {tuple(domin['median_rgb'])}", flush=True)

    rows.append({"image": os.path.abspath(img_path), "figure_px": n_fig,
                 "offpalette_px": n_off, "offpalette_pct": round(pct, 4),
                 "largest_blob_px": blob, "pass": bool(ok), "dominant": domin})
    if not ok:
        failed.append(stem)

    if args.overlay:
        os.makedirs(args.overlay, exist_ok=True)
        vis = (np.clip(rgb, 0, 1) * 255).astype(np.uint8).copy()
        vis[~fm] = (vis[~fm] * 0.35).astype(np.uint8)
        vis[off] = (255, 40, 220)
        im = Image.fromarray(vis)
        d = ImageDraw.Draw(im)
        try:
            f = ImageFont.truetype("arial.ttf", 20)
        except Exception:
            f = ImageFont.load_default()
        d.text((8, 8), f"{stem}   off-palette {n_off:,} px ({pct:.2f}%)  blob {blob:,}",
               fill=(255, 40, 220), font=f)
        p = os.path.join(args.overlay, os.path.splitext(stem)[0] + "_offpalette.png")
        im.save(p)

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)) or ".", exist_ok=True)
    json.dump({"palette": os.path.abspath(args.palette), "min_chroma": CMIN,
               "bands": [{"name": n, "lo": lo, "hi": hi} for n, lo, hi in BANDS],
               "gate": {"max_pct": MAXPCT, "max_blob_px": MAXBLOB},
               "results": rows}, open(args.out_json, "w"), indent=1)
    print(f"\n[palette] wrote {args.out_json}")

if failed:
    msg = (f"ANDON: {len(failed)} of {len(rows)} twins carry colour the specification never "
           f"named: {', '.join(failed)}. Projecting one paints that material onto the mesh.")
    if args.report_only:
        print(f"[palette] {msg}  (--report-only: not halting)")
    else:
        sys.exit(msg)
print(f"[palette] {len(rows)} image(s), {len(rows) - len(failed)} within the declared palette")
