"""E08 — the contradiction test: does the PROMPT override an attribute the route supplies?

Amendment 16 established that 14-15 of the 16 NAMED elements arrive UNPROMPTED, so a
pass-rate over the specification has a denominator of one and cannot separate "the
specification works" from "the LoRA, mesh and control already produce this dwarf". The
test with a real denominator names attributes that CONFLICT with what arrives unbidden
and asks which one the image ends up carrying.

WHAT IS MEASURED, and why it is not a proxy. The contradictions are all colour/material
substitutions on a pinned pose (byte-matched control), so the question "did the named
attribute replace the supplied one" is a question about colour, and colour is what is
measured. Gold against silver is a CHROMA question — both are light metals, they differ
in C* = sqrt(a*^2 + b*^2) and in hue angle, not in luminance. Red beard against white is
chroma AND lightness. Green tunic against blue is hue. So every row reports L*, a*, b*,
C* and h(deg) for BOTH images plus the CIE76 dE between them, and the readout is the
DIRECTION of travel, which is stated per element before the run.

Three separate failure modes are watched:

  1. NO RESPONSE AT ALL. N11 moved the whole figure by median dE 1.07 — the model did not
     react to the phrase. Whole-figure dE is reported first, and against that 1.07, so
     "the supplied attribute won" is never confused with "the prompt was not read".
  2. GLOBAL REPAINT. Eight simultaneous colour changes could repaint the character, in
     which case per-element attribution is weak. The HELD regions — elements not
     contradicted — are the control: they are reported beside the contradicted ones.
  3. A BOX SITTING ON THE WRONG THING. This is what killed N11's gold-pixel count: the
     forearm crop caught the pauldron edge and inverted the truth. The fix here is not a
     cleverer crop, it is (a) every box is DRAWN and labelled on the sheet, and (b) every
     row prints the BASE image's own median colour inside the box, so the box can be
     checked against what it is supposed to be sitting on rather than trusted —
     e08_deltaE.py's pattern.

And one crop-free panel, because a hand-placed box is a hand-placed box: the joint
density of hue x chroma over the whole figure mask, base against arm. Gold sits warm and
chromatic; silver sits on the neutral axis at any hue. If the named metal displaced the
supplied one the warm-chromatic mass moves to the axis, and that is visible without any
threshold being chosen — Amendment 5's rule, plot the density rather than assert a cut.

  e08_contradiction.py --base BASE.png --arm ARM.png --mask SIL.png
                       --regions regions.json [--sheet S.png] [--out-json J.json]
                       [--label-base SPEC --label-arm CONTRA]
  e08_contradiction.py --base IMG.png --regions regions.json --overlay-only OUT.png
"""
import argparse
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True)
ap.add_argument("--arm")
ap.add_argument("--mask", help="exact mesh silhouette; without it the whole frame is used")
ap.add_argument("--regions", required=True)
ap.add_argument("--sheet")
ap.add_argument("--out-json")
ap.add_argument("--label-base", default="BASE")
ap.add_argument("--label-arm", default="ARM")
ap.add_argument("--overlay-only", help="draw the boxes on --base and exit; no arm needed")
args = ap.parse_args()

REG = json.load(open(args.regions, encoding="utf-8"))["regions"]
CLS_COL = {"contra": (255, 90, 70), "coloc": (250, 200, 60), "held": (90, 190, 255)}


def load(p):
    return np.asarray(Image.open(p).convert("RGB"), dtype=np.float32) / 255.0


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


def draw_boxes(img_u8, note=None):
    im = Image.fromarray(img_u8.copy())
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("arial.ttf", 13)
    except Exception:
        f = ImageFont.load_default()
    for r in REG:
        x0, y0, x1, y1 = r["box"]
        col = CLS_COL.get(r["class"], (200, 200, 200))
        d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=col, width=2)
        ty = y0 - 15 if y0 > 16 else y1 + 2
        d.text((x0, ty), r["name"], fill=col, font=f)
    if note:
        d.text((8, 8), note, fill=(255, 255, 255), font=f)
    return np.asarray(im)


base = load(args.base)
H, W = base.shape[:2]
if args.overlay_only:
    os.makedirs(os.path.dirname(os.path.abspath(args.overlay_only)) or ".", exist_ok=True)
    Image.fromarray(draw_boxes((np.clip(base, 0, 1) * 255).astype(np.uint8),
                               "region boxes — red=contradicted  yellow=co-located  "
                               "blue=HELD control")).save(args.overlay_only)
    print(f"[contra] box overlay -> {args.overlay_only}")
    raise SystemExit(0)

assert args.arm, "ANDON: --arm is required unless --overlay-only"
arm = load(args.arm)
assert arm.shape == base.shape, f"ANDON: {arm.shape} vs {base.shape} — not registered"
if args.mask:
    fm = np.asarray(Image.open(args.mask).convert("L"), dtype=np.float32) / 255.0 > 0.5
    assert fm.shape == (H, W), f"ANDON: mask {fm.shape} vs image {(H, W)}"
else:
    fm = np.ones((H, W), bool)

Lb, La = to_lab(base), to_lab(arm)
dE = np.linalg.norm(La - Lb, axis=-1)
out = {"base": os.path.abspath(args.base), "arm": os.path.abspath(args.arm),
       "figure_px": int(fm.sum()), "figure_pct_of_frame": round(float(fm.mean() * 100), 3)}


def chroma_hue(lab):
    c = np.hypot(lab[..., 1], lab[..., 2])
    h = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0
    return c, h


Cb, Hb = chroma_hue(Lb)
Ca, Ha = chroma_hue(La)

d = dE[fm]
out["whole_figure"] = {"px": int(fm.sum()), "median": round(float(np.median(d)), 2),
                       "mean": round(float(d.mean()), 2),
                       "pct_over_2_3": round(float((d > 2.3).mean() * 100), 1),
                       "pct_over_10": round(float((d > 10).mean() * 100), 1)}
print(f"[contra] figure {int(fm.sum()):,} px ({fm.mean()*100:.2f}% of frame)")
print(f"[contra] WHOLE FIGURE {args.label_base} -> {args.label_arm}: median dE "
      f"{out['whole_figure']['median']:.2f}  mean {out['whole_figure']['mean']:.2f}  "
      f">2.3 {out['whole_figure']['pct_over_2_3']:.1f}%  "
      f">10 {out['whole_figure']['pct_over_10']:.1f}%")
print(f"[contra]   N11's whole-figure median was 1.07 — 'the model did not respond to the "
       f"phrase at all'. Read this number against that one FIRST.")

yy, xx = np.mgrid[0:H, 0:W]
rows = []
print(f"\n[contra] {'region':<16s} {'cls':<7s} {'px':>7s}  "
      f"{args.label_base:<22s} -> {args.label_arm:<22s}  "
      f"{'dE':>6s} {'dC*':>7s} {'dh':>7s}")
for r in REG:
    x0, y0, x1, y1 = r["box"]
    sel = (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1) & fm
    n = int(sel.sum())
    if n < 50:
        print(f"[contra] {r['name']:<16s} {r['class']:<7s} {n:>7,}  (too few px in the "
              f"figure mask — box may be off the figure)")
        rows.append({**r, "px": n, "usable": False})
        continue
    brgb = tuple(int(v) for v in (np.median(base[sel], axis=0) * 255).round())
    argb = tuple(int(v) for v in (np.median(arm[sel], axis=0) * 255).round())
    bl = [float(np.median(Lb[sel][:, i])) for i in range(3)]
    al = [float(np.median(La[sel][:, i])) for i in range(3)]
    bc, ac = float(np.median(Cb[sel])), float(np.median(Ca[sel]))
    # circular median is ill-defined; use the chroma-weighted mean direction, which is
    # what "what hue is this region" means when part of it is near-neutral
    def mean_hue(hh, cc):
        w = cc
        if w.sum() < 1e-6:
            return float("nan")
        x = (w * np.cos(np.radians(hh))).sum()
        y = (w * np.sin(np.radians(hh))).sum()
        return float(np.degrees(np.arctan2(y, x)) % 360.0)
    bh = mean_hue(Hb[sel], Cb[sel])
    ah = mean_hue(Ha[sel], Ca[sel])
    dh = (ah - bh + 180.0) % 360.0 - 180.0
    de = float(np.median(dE[sel]))
    row = {**r, "px": n, "usable": True,
           "base_rgb": list(brgb), "arm_rgb": list(argb),
           "base_Lab": [round(v, 1) for v in bl], "arm_Lab": [round(v, 1) for v in al],
           "base_C": round(bc, 1), "arm_C": round(ac, 1), "dC": round(ac - bc, 1),
           "base_h": round(bh, 1), "arm_h": round(ah, 1), "dh": round(dh, 1),
           "dE_median": round(de, 2),
           "dE_mean": round(float(dE[sel].mean()), 2),
           "pct_over_10": round(float((dE[sel] > 10).mean() * 100), 1)}
    rows.append(row)
    print(f"[contra] {r['name']:<16s} {r['class']:<7s} {n:>7,}  "
          f"rgb{str(brgb):<16s} L{bl[0]:5.1f} C{bc:5.1f} h{bh:5.1f} -> "
          f"rgb{str(argb):<16s} L{al[0]:5.1f} C{ac:5.1f} h{ah:5.1f}  "
          f"{de:6.2f} {ac-bc:+7.1f} {dh:+7.1f}")
out["regions"] = rows

grp = {}
for c in ("contra", "coloc", "held"):
    ds = [r["dE_median"] for r in rows if r.get("usable") and r["class"] == c]
    if ds:
        grp[c] = {"n": len(ds), "median_of_region_dE": round(float(np.median(ds)), 2),
                  "min": round(min(ds), 2), "max": round(max(ds), 2)}
out["by_class"] = grp
print(f"\n[contra] region dE by class (the internal control is 'held'):")
for c, g in grp.items():
    print(f"[contra]   {c:<7s} n={g['n']:<3d} median {g['median_of_region_dE']:6.2f}   "
          f"range {g['min']:.2f}-{g['max']:.2f}")

if args.sheet:
    def enc(a):
        return (np.clip(a, 0, 1) * 255).astype(np.uint8)

    hm = np.zeros((H, W, 3), dtype=np.uint8)
    t = np.clip(dE / 25.0, 0, 1)
    hm[..., 0] = (t * 255)
    hm[..., 1] = ((1 - np.abs(t - 0.5) * 2) * 200)
    hm[..., 2] = ((1 - t) * 180)
    hm[~fm] = (30, 30, 34)

    # crop-free panel: joint density of hue x chroma over the figure, base vs arm.
    # No threshold is chosen; the picture is the evidence.
    def hc_panel(hh, cc, title):
        HB, CB = 72, 40
        hist, _, _ = np.histogram2d(hh[fm], np.clip(cc[fm], 0, 60),
                                    bins=[HB, CB], range=[[0, 360], [0, 60]])
        v = np.log1p(hist).T[::-1]
        v = v / max(v.max(), 1e-9)
        img = np.zeros((CB, HB, 3), dtype=np.uint8)
        img[..., 0] = (np.clip(v * 1.6, 0, 1) * 255)
        img[..., 1] = (np.clip(v * 1.1, 0, 1) * 230)
        img[..., 2] = (np.clip(v * 0.7, 0, 1) * 200)
        im = Image.fromarray(img).resize((W, H // 2), Image.NEAREST)
        d2 = ImageDraw.Draw(im)
        try:
            f = ImageFont.truetype("arial.ttf", 15)
        except Exception:
            f = ImageFont.load_default()
        d2.text((8, 6), f"{title}   x = hue 0-360 deg,  y = chroma C* 60 (top) - 0 (bottom)",
                fill=(255, 255, 255), font=f)
        d2.text((8, H // 2 - 20), "neutral / silver lies along the BOTTOM edge; gold is the "
                "warm high-C* mass", fill=(200, 200, 200), font=f)
        return np.asarray(im)

    top = np.concatenate([draw_boxes(enc(base), args.label_base),
                          draw_boxes(enc(arm), args.label_arm), hm], axis=1)
    bot = np.concatenate([hc_panel(Hb, Cb, args.label_base),
                          hc_panel(Ha, Ca, args.label_arm),
                          np.zeros((H // 2, W, 3), np.uint8)], axis=1)
    sheet = np.concatenate([top, bot], axis=0)
    os.makedirs(os.path.dirname(os.path.abspath(args.sheet)) or ".", exist_ok=True)
    Image.fromarray(sheet).save(args.sheet)
    print(f"\n[contra] wrote {args.sheet}"
          f"  ({args.label_base} | {args.label_arm} | dE heat  /  hue-chroma density)")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)) or ".", exist_ok=True)
    json.dump(out, open(args.out_json, "w"), indent=1)
    print(f"[contra] wrote {args.out_json}")
