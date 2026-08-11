"""E32 Gate 0 - a concept plate's OWN geometry, before anything reconstructs it. NO VERDICT.

WHY A COMMITTED TOOL AND NOT A SCRATCH SCRIPT. E32's predictions P1 and P3 are stated
against numbers read off the plate - the count of openings the lattice shows, and the
width of its thinnest member in pixels - so those numbers decide whether a prediction hit.
`e12_twin_readout.py` records what happens when numbers like these come from throwaway
scripts: three reports rest on figures with no artifact behind them. This is the artifact.

NOTHING HERE MEASURES A MESH. Every existing plate-side instrument in this repo takes a
mesh-derived mask as an input - `e12_twin_readout` requires `--mask`, `silhouette_masks`
raycasts geometry, `e14_twin_registration` compares a twin to a silhouette. That is correct
for their question (is the paint registered to the surface) and useless for this one, which
is asked BEFORE a mesh exists. Enumerated before commissioning; the gap is real.

THE MASK IS KEYED, AND THAT IS A LAST RESORT WITH A STATED REASON. This repo retires
corner-median keying after three failures and says "where geometry can answer the question,
use geometry." There is no geometry here - the plate is the reconstructor's INPUT, so a key
is the only available answer and the failure modes are met head-on:

  * the background is the route's own FITTED quadratic over a border ring
    (`mask_geometry.fit_background`, imported, and asserted by T64 to be bit-identical to
    `project_twins`' own body - that file parses argv at module level and cannot be
    imported, which is why five hand-copies of this model exist in the repo). It reduces
    to the corner median on a flat field rather than assuming one, and this plate has a
    vertical gradient - precisely the case a single sample gets wrong;
  * NO EROSION. `figure_mask` applies `minimum_filter(size=5)`, which removes 2 px from
    every side of every structure. On a thin-tube subject that is not a rim trim, it is the
    subject: CLAUDE.md records an erosion tuned on a wide figure annihilating 100% / 100% /
    77.6% of the three thinnest strata. A tool built to measure thin members may not begin
    by deleting them;
  * the tolerance is SWEPT, not chosen. A single key threshold is one number standing where
    a distribution belongs, and the sweep shows whether the readings are threshold-driven or
    stable. Every derived quantity is reported at every tolerance;
  * POLARITY is a flag, because `abs()` is not free. E32's plate carries a hard dark band
    across its bottom third that no quadratic fits, and a two-sided residual swallowed it:
    835,526 px keyed at tol 0.06, bbox the full 2048 px frame width, median width 350 px on
    a subject whose limbs are ~20. `--polarity lighter` keys only pixels ABOVE the fitted
    background, which excludes a dark ground BY CONSTRUCTION rather than by threshold. It
    is a statement about the plate class - a light clay subject on darker ground - and it is
    declared per run, never inferred. Default stays `both`, so every number this tool has
    already produced reproduces unchanged.

THE BBOX CHECK IS A DISJUNCTION, and the first draft got that wrong. E08's case is "751 px
wide in a 752 px frame when the mesh is 388" - ONE dimension. Requiring both to blow out
made the flag a conjunction, and it stayed silent on this plate at exactly the tolerance
where the key was worst: 2048/2048 wide, 1673/2048 tall, reported clean. A composite
condition is governed by its rarest clause, and the rare clause here was the one nobody
needed. It now fires on either dimension and names which.

WIDTH IS A DIAMETER, STATED. `mask_geometry.local_thickness` (imported) returns the
HALF-width - the radius of the largest inscribed disc a pixel belongs to. Limb width in this
tool is 2x that, because "the limb is 15 px wide" is the quantity a prediction is stated in
and confusing it with the radius is a factor-of-two error in the operand. Both are printed.

OPENINGS ARE COUNTED AS A CURVE, NOT AT A THRESHOLD. An opening is a connected component of
NOT-figure that does not touch the frame border. At min-area 1 that count includes every
antialiasing pinhole; at min-area 16384 it misses real gaps. The repo's two-threshold rule
(report the total AND the largest component) generalises here to a count-versus-min-area
curve, so a single arbitrary cut never decides P1's operand.

ALPHA IS REPORTED BECAUSE IT DECIDES WHICH CODE PATH RUNS DOWNSTREAM. `pipe.run` runs
`rembg` only where the input has no alpha (E29 Ruling 4). A plate whose alpha channel is
present but constant-255 is, for that branch, an image with no alpha. Presence and
non-triviality are therefore different facts and both are printed.

  e32_plate_geometry.py --image P.png [--tols 0.03,0.06,0.10] [--ring 24] [--out J.json]

Standards compliance: PIN_PER_STEP - every constant is a flag echoed into the JSON.
ANDON_AUTHORITY - NONE, deliberately. This tool measures an INPUT; it has no result to halt
on, and a bbox that fills the frame is reported as a degraded reading rather than raising -
the same choice `e12_twin_readout` made, for the same reason. NAMED_COMPENSATORS - writes at
most one JSON to a new path; the plate is opened read-only. EXTERNAL_VERIFIER - reports
measurements only; it ranks nothing and recommends nothing.
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, label

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mask_geometry import fit_background, local_thickness  # noqa: E402

MIN_AREAS = [1, 4, 16, 64, 256, 1024, 4096, 16384]
WIDTH_BANDS = [(0, 4), (4, 8), (8, 16), (16, 32), (32, 64), (64, 1000000)]


def alpha_facts(im):
    """Present is not the same as non-trivial, and pipe.run's rembg branch keys on the
    difference. Returns both."""
    if "A" not in im.getbands():
        return {"channel_present": False, "non_trivial": False,
                "min": None, "max": None, "frac_below_255": None}
    a = np.asarray(im.getchannel("A"))
    below = float((a < 255).mean())
    return {"channel_present": True,
            "non_trivial": bool(below > 0.0),
            "min": int(a.min()), "max": int(a.max()),
            "frac_below_255": below}


def openings(mask):
    """Areas of the connected components of NOT-figure that never touch the frame border.

    A component touching the border is the surrounding background, not an opening. Labelling
    the background with scipy's default 4-connectivity is the complement of 8-connectivity on
    the figure, which is the pairing that makes a 1 px diagonal tube a barrier rather than a
    leak - the wrong pairing would count a lattice's cells as one connected background.
    """
    lab, n = label(~mask)
    if n == 0:
        return []
    border = set(np.unique(np.concatenate(
        [lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]])).tolist())
    border.discard(0)
    areas = np.bincount(lab.ravel(), minlength=n + 1)
    return sorted((int(areas[i]) for i in range(1, n + 1) if i not in border),
                  reverse=True)


def keyed(rgb, bg, tol, polarity):
    """Pixels the background model does not explain, at the declared polarity.

    `both` is the historical two-sided residual. `lighter` keeps only pixels ABOVE the
    fitted surface and `darker` only those below - the max over channels of the SIGNED
    residual, so a light subject is separated from a dark ground by construction rather
    than by choosing a threshold that happens to sit between them.
    """
    d = rgb - bg
    if polarity == "lighter":
        return d.max(axis=-1) > tol
    if polarity == "darker":
        return (-d).max(axis=-1) > tol
    return np.abs(d).max(axis=-1) > tol


def measure(path, tols, ring, polarity="both", mask_path=None):
    im = Image.open(path)
    facts = {"path": os.path.abspath(path), "size": list(im.size), "mode": im.mode,
             "bands": list(im.getbands()), "alpha": alpha_facts(im)}
    rgb = np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
    H, W = rgb.shape[:2]
    facts["frame_px"] = int(H * W)

    bg = fit_background(rgb, b=ring)
    # The gradient the plate actually carries, read off the fitted MODEL over the whole
    # frame - not off the border ring it was fitted on, which would understate it.
    channels = {}
    for i, c in enumerate("rgb"):
        ch = bg[..., i] * 255.0
        channels[c] = {"min": float(ch.min()), "max": float(ch.max()),
                       "span": float(ch.max() - ch.min())}
    lum = bg.mean(axis=-1) * 255.0
    channels["luma"] = {"min": float(lum.min()), "max": float(lum.max()),
                        "span": float(lum.max() - lum.min()),
                        "top_row_mean": float(lum[0].mean()),
                        "bottom_row_mean": float(lum[-1].mean())}
    facts["background_fit"] = {"ring_px": ring, "channels": channels}

    resid = np.abs(rgb - bg).max(axis=-1)
    facts["polarity"] = polarity
    facts["mask_source"] = mask_path
    facts["residual"] = {"p50": float(np.percentile(resid, 50)),
                         "p99": float(np.percentile(resid, 99)),
                         "max": float(resid.max())}

    supplied = None
    if mask_path is not None:
        mi = Image.open(mask_path)
        a = np.asarray(mi.getchannel("A") if "A" in mi.getbands()
                       else mi.convert("L"))
        if a.shape != (H, W):
            raise SystemExit("ANDON: mask is %r, plate is %r - a mask measured against "
                             "a different frame answers a different question"
                             % (a.shape, (H, W)))
        supplied = a > 127
        facts["supplied_mask"] = {"area_px": int(supplied.sum()),
                                  "frac_of_frame": float(supplied.mean()),
                                  "from_alpha": bool("A" in mi.getbands())}

    rows = []
    for tol in tols:
        m = supplied if supplied is not None else keyed(rgb, bg, tol, polarity)
        area = int(m.sum())
        row = {"tol": tol, "area_px": area, "frac_of_frame": area / float(H * W)}
        if area == 0:
            rows.append(row)
            continue
        ys, xs = np.nonzero(m)
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
        bw, bh = x1 - x0 + 1, y1 - y0 + 1
        row["bbox_xyxy"] = [x0, y0, x1, y1]
        row["bbox_wh"] = [bw, bh]
        row["bbox_frac_of_frame_w"] = bw / float(W)
        row["bbox_frac_of_frame_h"] = bh / float(H)
        row["bbox_aspect_w_over_h"] = bw / float(bh)
        row["fill_of_bbox"] = area / float(bw * bh)
        # The free check that runs FIRST (E08 registration): a figure that fills its frame is
        # a broken key, and its downstream numbers are contaminated rather than merely small.
        # EITHER dimension, not both - E08's own case blew out in width alone.
        blow = [d for d, v, n in (("w", bw, W), ("h", bh, H)) if v >= 0.98 * n]
        row["bbox_blowout"] = bool(blow)
        row["bbox_blowout_axes"] = blow

        half = local_thickness(distance_transform_edt(m))
        hv = half[m]
        hw = {"min": float(hv.min()), "max": float(hv.max()),
              "p01": float(np.percentile(hv, 1)), "p05": float(np.percentile(hv, 5)),
              "p50": float(np.percentile(hv, 50)), "p95": float(np.percentile(hv, 95))}
        row["half_width_px"] = hw
        row["width_px"] = dict((k, v * 2.0) for k, v in hw.items())
        # Area-weighted: what share of the subject sits in each width band. A lattice of thin
        # tubes and a solid figure carrying a thin sword differ here and nowhere else.
        row["width_band_share"] = dict(
            ("%d-%d" % (lo, hi), float(((hv * 2 >= lo) & (hv * 2 < hi)).mean()))
            for lo, hi in WIDTH_BANDS)

        areas = openings(m)
        row["openings"] = dict(("min_area_%d" % a,
                                int(sum(1 for ar in areas if ar >= a)))
                               for a in MIN_AREAS)
        row["opening_areas_top20"] = areas[:20]
        rows.append(row)
    facts["tolerance_sweep"] = rows
    return facts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--tols", default="0.03,0.06,0.10",
                    help="residual-above-background key tolerances to sweep")
    ap.add_argument("--ring", type=int, default=24,
                    help="border ring width the background quadratic is fitted over")
    ap.add_argument("--polarity", default="both", choices=["both", "lighter", "darker"],
                    help="which side of the fitted background counts as subject; "
                         "'lighter' excludes a dark ground by construction")
    ap.add_argument("--mask", default=None,
                    help="use THIS mask (alpha, or L>127) instead of keying. The route's "
                         "own segmenter answers better than any key this tool can run.")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    tols = [float(t) for t in a.tols.split(",") if t.strip()]
    facts = measure(a.image, tols, a.ring, a.polarity, a.mask)
    txt = json.dumps(facts, indent=2, sort_keys=True)
    print(txt)
    if a.out:
        d = os.path.dirname(os.path.abspath(a.out))
        if d and not os.path.isdir(d):
            os.makedirs(d)  # scripts create their own output directories
        with open(a.out, "w", encoding="ascii") as fh:
            fh.write(txt)
        print("wrote %s" % a.out)


if __name__ == "__main__":
    main()
