"""The two channels the palette gate is BLIND TO, per twin: achromatic mass, and registration.

WHY A COMMITTED TOOL. Both channels were measured at handoffs 8, 9 and 10 by throwaway scripts
that were never committed, so three reports rest on numbers with no artifact behind them — the
same gap `e12_stem_delta.py` was written to close for the stem ANDON. This is that artifact for
these two.

CHANNEL 1 — ACHROMATIC MASS (E12 Ruling 17d). The palette gate keys on HUE above a chroma
floor, so a near-black region carries no hue and the gate cannot see it. Handoff 8 measured the
consequence: the twin the gate scored CLEANEST (view 3, 0.36% off-palette) carried a 43,999 px
flat-black region across the far foreleg, chest and under-wing — a declared moss-green surface
painted as a silhouette. This channel is `L* < 20 AND C* < 12` inside the exact mesh
silhouette, reported as a total AND as its largest connected component, because ordinary shadow
is diffuse and an invented void is one blob (the total-and-blob rule, third instrument here to
need it).

NO BOUND IS ARMED, and that is a decision. The only baseline that exists is the ACCEPTED pair
(15.16% / CC 14,816 on view 1; 12.54% / CC 13,049 on view 5) and five of eight handoff-8 twins
sat inside it — one artifact does not license a threshold. The tool prints the pair's own
numbers beside every reading so a value is never read without the thing it is compared to.

CHANNEL 2 — REGISTRATION. IoU between the twin's own painted figure and the EXACT raycast
silhouette, plus the bbox comparison that is the real guard. Two constructions, both load-bearing
and both paid for:

  * the background is FITTED over a border ring, never a corner median — corner-median keying
    has failed three independent times in this project (CLAUDE.md retires it);
  * the BBOX CHECK RUNS FIRST and is free. *A figure cannot be 1792 px wide in a 1792 px frame
    when the mesh is 1487.* It caught handoff 10's vignetted re-roll before its IoU of 0.459
    was believed. A twin whose bbox blows out to the frame gets its IoU reported as
    CONTAMINATED rather than as a registration failure, and the tool says which.

⚠ THE BORDER-RING FIT ASSUMES A FLAT-*ENOUGH* FIELD (handoff 10 section 5, banked). A graded
backdrop defeats it. The ring-vs-whole-background medians and the fraction of background past
the key threshold are printed for every twin, so the caller can see the assumption holding or
failing instead of inferring it from a bad IoU.

  e12_twin_readout.py --image LABEL=PATH ... --mask LABEL=PATH ... [--out J.json]

Standards compliance: PIN_PER_STEP — every constant (L*/C* cut, ring width, key tolerance) is a
flag with its value echoed into the JSON. ANDON_AUTHORITY — deliberately NONE on the numbers;
the bbox check DEGRADES a reading rather than halting, because a contaminated key is a
diagnostic finding and not a reason to stop measuring the other seven views. NAMED_COMPENSATORS
— writes at most one JSON. EXTERNAL_VERIFIER — registration is measured against geometry the
generator does not control.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None

# The accepted pair's own readings, from handoff 8 tasks 2-3. Printed beside every twin so a
# number is never read without its baseline. NOT a bound.
PAIR = {"view 1": (15.16, 14816), "view 5": (12.54, 13049)}

ap = argparse.ArgumentParser()
ap.add_argument("--image", action="append", required=True, metavar="LABEL=PATH")
ap.add_argument("--mask", action="append", required=True, metavar="LABEL=PATH",
                help="EXACT raycast mesh silhouette, matched to --image by LABEL")
ap.add_argument("--l-max", type=float, default=20.0, help="achromatic: L* below this")
ap.add_argument("--c-max", type=float, default=12.0, help="achromatic: C* below this")
ap.add_argument("--ring", type=int, default=24, help="border ring width for the background fit")
ap.add_argument("--key-tol", type=float, default=0.06, help="residual above which a pixel is paint")
ap.add_argument("--bbox-blowout", type=float, default=1.25,
                help="twin bbox larger than the mesh bbox by more than this factor in either "
                     "dimension marks the key CONTAMINATED and the IoU unusable")
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


def ring_fit(img, b):
    """Per-channel quadratic over a border ring — project_twins' figure_mask, same construction.

    Reduces to the corner median on a genuinely flat field, so nothing prior loses comparability.
    """
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    ring = np.zeros((H, W), bool)
    ring[:b, :] = ring[-b:, :] = ring[:, :b] = ring[:, -b:] = True
    A = np.stack([np.ones(H * W), xx.ravel() / W, yy.ravel() / H,
                  (xx.ravel() / W) ** 2, (yy.ravel() / H) ** 2,
                  (xx.ravel() / W) * (yy.ravel() / H)], axis=1)
    Xr = A.reshape(H, W, -1)[ring]
    resid = np.zeros((H, W, 3), np.float32)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(Xr, img[..., c][ring], rcond=None)
        resid[..., c] = img[..., c] - (A @ coef).reshape(H, W)
    return resid, ring


print("[readout] achromatic = L* < %.0f AND C* < %.0f, inside the EXACT silhouette. "
      "NO BOUND IS ARMED." % (args.l_max, args.c_max))
print("[readout] accepted-pair baseline: %s"
      % "; ".join("%s %.2f%% / CC %s" % (k, v[0], f"{v[1]:,}") for k, v in PAIR.items()))
print()
print("[readout] %-10s | %9s %9s | %8s %9s %9s | %s"
      % ("label", "achrom %", "largest CC", "reg IoU", "twin bbox", "mesh bbox", "key health"))
rows = {}
for lab in sorted(IM, key=lambda s: (len(s), s)):
    rgb = np.asarray(Image.open(IM[lab]).convert("RGB"), np.float32) / 255.0
    fm = np.asarray(Image.open(MK[lab]).convert("L")) > 127
    if fm.shape != rgb.shape[:2]:
        raise SystemExit("ANDON: %s mask %s vs image %s" % (lab, fm.shape, rgb.shape[:2]))

    lab_img = to_lab(rgb)
    C = np.hypot(lab_img[..., 1], lab_img[..., 2])
    dark = (lab_img[..., 0] < args.l_max) & (C < args.c_max) & fm
    n_dark = int(dark.sum())
    lb, nl = ndimage.label(dark)
    cc = int(np.bincount(lb.ravel())[1:].max()) if nl else 0
    pct = n_dark / max(int(fm.sum()), 1) * 100

    resid, ring = ring_fit(rgb, args.ring)
    key = np.abs(resid).max(axis=-1) > args.key_tol
    key = ndimage.minimum_filter(key.astype(np.float32), size=5) > 0.5
    ys_t, xs_t = np.where(key)
    ys_m, xs_m = np.where(fm)
    if not len(ys_t):
        rows[lab] = {"achromatic_pct": pct, "achromatic_px": n_dark, "largest_cc": cc,
                     "key": "EMPTY"}
        print("[readout] %-10s | %8.2f%% %9s | key keyed NOTHING" % (lab, pct, f"{cc:,}"))
        continue
    tb = [int(xs_t.min()), int(ys_t.min()), int(xs_t.max()), int(ys_t.max())]
    mb = [int(xs_m.min()), int(ys_m.min()), int(xs_m.max()), int(ys_m.max())]
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    mw, mh = mb[2] - mb[0], mb[3] - mb[1]
    blown = tw > mw * args.bbox_blowout or th > mh * args.bbox_blowout
    iou = float((key & fm).sum() / max(int((key | fm).sum()), 1))

    # is the flat-ENOUGH assumption holding? (handoff 10 section 5)
    bgm_ring = np.median(rgb[ring].reshape(-1, 3), axis=0)
    outside = ~fm
    bgm_all = np.median(rgb[outside].reshape(-1, 3), axis=0)
    past = float((np.abs(resid).max(axis=-1)[outside] > args.key_tol).mean() * 100)
    graded = past > 5.0 or float(np.abs(bgm_ring - bgm_all).max() * 255) > 4.0

    rows[lab] = {"achromatic_pct": round(pct, 3), "achromatic_px": n_dark, "largest_cc": cc,
                 "reg_iou": round(iou, 6), "twin_bbox": tb, "mesh_bbox": mb,
                 "bbox_blown": bool(blown),
                 "ring_median": [int(v * 255) for v in bgm_ring],
                 "background_median": [int(v * 255) for v in bgm_all],
                 "background_past_key_pct": round(past, 2), "backdrop_graded": bool(graded),
                 "iou_usable": bool(not blown and not graded)}
    note = "flat, IoU usable"
    if blown:
        note = "BBOX BLOWN OUT — key CONTAMINATED, IoU is NOT a registration number"
    elif graded:
        note = ("GRADED backdrop (%.1f%% past key, ring %s vs bg %s) — IoU suspect"
                % (past, tuple(int(v * 255) for v in bgm_ring),
                   tuple(int(v * 255) for v in bgm_all)))
    print("[readout] %-10s | %8.2f%% %9s | %8.6f %4dx%-4d %4dx%-4d | %s"
          % (lab, pct, f"{cc:,}", iou, tw, th, mw, mh, note))

if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"_what": "E12 Ruling 17d achromatic channel + registration, per twin. "
                            "NO BOUND IS ARMED on either; the accepted pair is the only "
                            "baseline that exists.",
                   "_params": {"l_max": args.l_max, "c_max": args.c_max, "ring": args.ring,
                               "key_tol": args.key_tol, "bbox_blowout": args.bbox_blowout},
                   "_accepted_pair_baseline": {k: {"achromatic_pct": v[0], "largest_cc": v[1]}
                                               for k, v in PAIR.items()},
                   "views": rows}, fh, indent=1)
        fh.write("\n")
    print("\n[readout] wrote %s" % args.out)
