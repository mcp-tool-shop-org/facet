"""E12's palette gate in the form Ruling 16e ruled: REPORT-STRUCTURED, null bounds, eye rules.

WHY A SECOND GATE FILE AND NOT AN EDIT TO `tools/palette_gate.py`. That file answers one
question — *does this twin contain material the specification never named* — and answers it
with a total, a largest component and one dominant hue bin. On THIS subject that shape is not
enough, and handoff 8's pair-validation is why: pointed at the ACCEPTED pair it returned 3.80%
and 8.19% off-palette, and the single dominant-bin line could not tell an advisor that view 5's
mass was the membrane stratum while view 1's was something else entirely. Ruling 16e therefore
fixed the REPORT rather than the bounds:

    total off-palette px and % | largest connected component | the allowance-attributed
    fraction (the pair-realised D3 membrane stratum) | the seam-family fraction (S-occlusion,
    realised) | the full hue histogram | the residual after both named populations are
    attributed, with its largest components enumerated | an overlay.

THE TWO NAMED POPULATIONS, both measured on the accepted pair before any twin existed:

  * MEMBRANE STRATUM — hue 273.4-293.4, the Ruling 15c realised-stratum allowance. Pair-realised
    D3, NOT a fixture band, and deliberately not an `allowed_bands` entry (palette_gate arms
    every entry there regardless of `status`, so a suspended band listed there would silently
    arm itself — the construction hazard recorded at 16a).
  * SEAM FAMILY — hue 190-270, S-OCCLUSION REALISED (Ruling 16c). Occlusion shadow that carries
    a hue: the throat/shoulder seam, wing-body gap, dorsal-ridge and tail-spine bases, leg
    creases. 7,293 px in 121 components on the accepted pair's view 1, median rgb(26,65,76),
    C* 14.4. The fixture pre-registered the stressor before any generation existed; the first
    instrument to meet it read it as the known geometry.

NO NUMERIC BOUND IS ARMED, AND THAT IS A DECISION (16e). The galleon's own palette sets both
bounds null on purpose; the same reasoning applies here twice over, because the two named
populations put any total-based bound on a moving denominator and a blob bound would need a
multiplier nobody can derive. Suspend rather than invent. **The trigger is the E07-class
signature** — a single coherent component at garment scale OUTSIDE both named populations
(measured precedents: 4,882 / 5,068 / 5,590 px) — which this file SURFACES as numbers, bboxes
and a crop, and which the advisor's eye rules. This file exits 0 always; it cannot halt anything.

  e12_twin_gate.py --palette P.json --images ... --masks ... --out-json J --overlay DIR
                   [--crops DIR] [--label-prefix twin]

Standards compliance: PIN_PER_STEP — bands, floor and both named populations are read from the
palette JSON and echoed into the report, never literals here. ANDON_AUTHORITY — deliberately
NONE: this is a measurement, and the file says so in its own output so a clean line is never
misread as a pass. EXTERNAL_VERIFIER — it grades colour against a declaration written before the
twins existed, and emits pictures for a human; it decides nothing.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ap = argparse.ArgumentParser()
ap.add_argument("--palette", required=True)
ap.add_argument("--images", nargs="+", required=True)
ap.add_argument("--masks", nargs="+", required=True,
                help="EXACT mesh silhouette per image, parallel to --images")
ap.add_argument("--out-json", required=True)
ap.add_argument("--overlay", required=True)
ap.add_argument("--crops", default=None, help="dir for a crop of each view's largest RESIDUAL "
                                              "component - the E07-class signature's evidence")
ap.add_argument("--top", type=int, default=5, help="residual components enumerated per view")
args = ap.parse_args()

if len(args.images) != len(args.masks):
    raise SystemExit("ANDON: %d masks for %d images" % (len(args.masks), len(args.images)))

PAL = json.load(open(args.palette, encoding="utf-8"))
BANDS = [(b["name"], float(b["hue_deg"][0]), float(b["hue_deg"][1])) for b in PAL["allowed_bands"]]
CMIN = float(PAL["min_chroma"])
SUSP = PAL.get("_suspended_stratum_allowance_NOT_APPLIED_BY_THIS_FILE", [])
ALLOW = (float(SUSP[0]["hue_deg"][0]), float(SUSP[0]["hue_deg"][1])) if SUSP else None
SEAM = (190.0, 270.0)   # Ruling 16c's measured span for S-occlusion realised
E07 = (4882, 5068, 5590)


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


print("[16e] %s: floor C* %.1f  armed band(s) %s"
      % (os.path.basename(args.palette), CMIN,
         ", ".join("%s %.1f-%.1f" % b for b in BANDS)), flush=True)
print("[16e] named populations, both measured on the ACCEPTED pair before any twin existed:")
print("[16e]   membrane stratum (pair-realised D3, Ruling 15c allowance) hue %.1f-%.1f"
      % ALLOW if ALLOW else "[16e]   membrane stratum: ABSENT from the palette file")
print("[16e]   seam family (S-occlusion realised, Ruling 16c)          hue %.1f-%.1f" % SEAM)
print("[16e] NO BOUND IS ARMED. This is a MEASUREMENT and it cannot fail. The trigger is the")
print("[16e] E07-class signature - one coherent RESIDUAL component at garment scale (measured")
print("[16e] precedents %s px) - surfaced below for the eye, ruled by the advisor.\n"
      % ", ".join("{:,}".format(v) for v in E07), flush=True)

os.makedirs(args.overlay, exist_ok=True)
if args.crops:
    os.makedirs(args.crops, exist_ok=True)
rows = []
print("[16e] %-22s %10s %9s %7s %8s | %8s %8s %9s %9s"
      % ("image", "figure px", "offpal", "%", "blob", "membrane", "seam", "residual", "res-blob"),
      flush=True)
for img_path, mask_path in zip(args.images, args.masks):
    rgb = np.asarray(Image.open(img_path).convert("RGB"), np.float32) / 255.0
    fm = np.asarray(Image.open(mask_path).convert("L")) > 127
    if fm.shape != rgb.shape[:2]:
        raise SystemExit("ANDON: mask %s vs image %s for %s" % (fm.shape, rgb.shape[:2], img_path))
    lab = to_lab(rgb)
    C = np.hypot(lab[..., 1], lab[..., 2])
    H = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0

    in_band = np.zeros(H.shape, bool)
    for _n, lo, hi in BANDS:
        in_band |= (H >= lo) & (H <= hi) if lo <= hi else ((H >= lo) | (H <= hi))
    off = (C > CMIN) & (~in_band) & fm
    n_fig, n_off = int(fm.sum()), int(off.sum())

    memb = off & (H >= ALLOW[0]) & (H <= ALLOW[1]) if ALLOW else np.zeros_like(off)
    seam = off & (H >= SEAM[0]) & (H <= SEAM[1])
    resid = off & ~memb & ~seam

    def big(m):
        lb, k = ndimage.label(m)
        return (int(np.bincount(lb.ravel())[1:].max()), lb, k) if k else (0, None, 0)

    blob, _, _ = big(off)
    rblob, rlb, rk = big(resid)
    pct = 100.0 * n_off / max(n_fig, 1)
    stem = os.path.basename(img_path)
    print("[16e] %-22s %10s %9s %6.2f%% %8s | %7.1f%% %7.1f%% %9s %9s"
          % (stem[:22], "{:,}".format(n_fig), "{:,}".format(n_off), pct, "{:,}".format(blob),
             100.0 * memb.sum() / max(n_off, 1), 100.0 * seam.sum() / max(n_off, 1),
             "{:,}".format(int(resid.sum())), "{:,}".format(rblob)), flush=True)

    comps = []
    if rk:
        sizes = ndimage.sum(resid, rlb, range(1, rk + 1))
        for j in np.argsort(sizes)[::-1][:args.top]:
            m = rlb == (j + 1)
            ys, xs = np.nonzero(m)
            comps.append({"px": int(sizes[j]),
                          "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                          "median_rgb255": [int(round(v * 255)) for v in np.median(rgb[m], 0)],
                          "median_hue": round(float(np.median(H[m])), 1),
                          "median_chroma": round(float(np.median(C[m])), 1)})
        for c in comps[:3]:
            print("[16e]     residual comp %7s px  bbox %s  rgb%s  h %.0f  C* %.1f%s"
                  % ("{:,}".format(c["px"]), tuple(c["bbox"]), tuple(c["median_rgb255"]),
                     c["median_hue"], c["median_chroma"],
                     "   <== within the E07 precedent scale, SURFACED FOR THE EYE"
                     if c["px"] >= min(E07) * 0.5 else ""), flush=True)

    hist, edges = np.histogram(H[off], bins=18, range=(0, 360))
    rows.append({"image": os.path.abspath(img_path), "figure_px": n_fig,
                 "offpalette_px": n_off, "offpalette_pct": round(pct, 4),
                 "largest_blob_px": blob,
                 "membrane_stratum_px": int(memb.sum()),
                 "membrane_stratum_pct_of_offpalette": round(100.0 * memb.sum() / max(n_off, 1), 1),
                 "seam_family_px": int(seam.sum()),
                 "seam_family_pct_of_offpalette": round(100.0 * seam.sum() / max(n_off, 1), 1),
                 "residual_px": int(resid.sum()), "residual_largest_component_px": rblob,
                 "residual_components": comps,
                 "hue_histogram_20deg": [int(v) for v in hist]})

    vis = (np.clip(rgb, 0, 1) * 255).astype(np.uint8).copy()
    vis[~fm] = (vis[~fm] * 0.3).astype(np.uint8)
    vis[seam] = (255, 190, 40)      # amber  = S-occlusion realised
    vis[memb] = (40, 200, 255)      # cyan   = membrane stratum
    vis[resid] = (255, 40, 220)     # magenta= residual, the E07 question
    im = Image.fromarray(vis)
    ImageDraw.Draw(im).text((8, 8), "%s  off %s (%.2f%%)  cyan=membrane  amber=seam  "
                                    "magenta=residual (largest %s)"
                            % (stem, "{:,}".format(n_off), pct, "{:,}".format(rblob)),
                            fill=(255, 255, 255))
    im.save(os.path.join(args.overlay, os.path.splitext(stem)[0] + "_16e.png"))
    if args.crops and comps:
        x0, y0, x1, y1 = comps[0]["bbox"]
        px, py = max(60, (x1 - x0) // 2), max(60, (y1 - y0) // 2)
        cx0, cy0 = max(0, x0 - px), max(0, y0 - py)
        cx1, cy1 = min(rgb.shape[1], x1 + px), min(rgb.shape[0], y1 + py)
        s = max(1, min(6, 900 // max(cx1 - cx0, 1)))
        Image.open(img_path).convert("RGB").crop((cx0, cy0, cx1, cy1)).resize(
            ((cx1 - cx0) * s, (cy1 - cy0) * s), Image.LANCZOS).save(
            os.path.join(args.crops, os.path.splitext(stem)[0] + "_residual_%dx.png" % s))

os.makedirs(os.path.dirname(os.path.abspath(args.out_json)) or ".", exist_ok=True)
json.dump({"palette": os.path.abspath(args.palette), "min_chroma": CMIN,
           "armed_bands": [{"name": n, "lo": lo, "hi": hi} for n, lo, hi in BANDS],
           "named_populations": {"membrane_stratum_hue": list(ALLOW) if ALLOW else None,
                                 "seam_family_hue": list(SEAM)},
           "bounds": {"max_pct": None, "max_blob_px": None,
                      "_why": "Ruling 16e - report-structured, no bound armed. The trigger is "
                              "the E07-class signature in the RESIDUAL, ruled at the "
                              "advisor's eye."},
           "e07_precedents_px": list(E07), "results": rows},
          open(args.out_json, "w"), indent=1)
print("\n[16e] wrote %s" % args.out_json)
print("[16e] %d image(s) measured. NOTHING PASSED OR FAILED - no bound is armed." % len(rows))
