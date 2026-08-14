"""TWIN DESPECKLE - census the generator's dark-speck class on a twin, before projection.

WHY THIS EXISTS. The Director ruled a second defect class on the performer unacceptable at
his zoom the day after accepting E34: scattered dark brown-to-black specks, 2-6 px at the
352x1024 frame scale. The class was attributed before it was named - the specks survive FLAT
light (texture truth, not shading), they ride in the generated twins themselves, the clay/canny
controls carry ZERO, and every twin carries them, so re-projecting from more views multiplies
their sources. The atlas census puts 61% of the core-black class on twin-painted texels and 39%
on fill-propagated ones, and the fill can only re-import what the paint carries. So the
despeckler's home is THE TWINS, BEFORE PROJECTION. An atlas-side cleanup fights the same dots
twice.

WHY A CENSUS IS A SEPARATE MODE FROM A CORRECTION. The switching-median tradition (Hwang &
Haddad 1995; Ng & Ma 2006) classifies first and touches only what it flagged. Splitting the two
into modes makes the classification auditable on its own: `--mode census` writes a report and
CHANGES NOTHING, so the numbers that decide an A/B are produced by a read-only path.

WHAT IT MEASURES, and why the deviation is LOCAL. A speck is not dark in absolute terms - it is
dark against the register around it, and the register's own value swings across the figure with
material and lighting. So the estimate is a local median field (robust to the specks themselves,
which occupy a small fraction of any window several times their size), and a pixel is a candidate
when it is DARKER than that field by --dark-dl in L* and further than --de-min in dE.

WHY THE SIZE THRESHOLD IS ONE INTEGER. Vincent's grayscale area opening (1993) removes every
connected component below an area lambda in px^2 and leaves everything above it byte-identical
outside its own footprint - one integer bounds blob size instead of a fixed-radius kernel that
would soften the register everywhere. The class is bounded ABOVE, not below: a 6 px dot has a
36 px^2 footprint, and anything larger is a region of material, not a speck. That upper bound
is --blob-max-px2 and it is the tool's one keyed threshold.

WHY THE THRESHOLD IS px^2 AND NEVER A PERCENTAGE OF FRAME. This repo has mis-specified four
pass conditions on moving denominators, and one of them was a boundary quantity normalised by an
area that swings 1.65x between a profile and a rear three-quarter of the same subject. A speck's
size is a property of the speck.

WHY THE CHROMA FLOOR IS LOAD-BEARING AND NOT A TUNING KNOB. The class is specified as "dark
brown-to-black speckles" - a COLOUR specification, not merely a darkness one. Without the
chromatic half, this detector fires on any locally-dark pixel, and the first thing that means is
GEOMETRY SHADING: measured on the E33 clay controls it returned 153 blobs of median chroma 3.0
against 104 on the rejected twin at median chroma 54.2, i.e. it fired MORE on a clean control
than on the artifact the Director rejected. Absolute darkness does not separate them (0 clay
blobs vs 5 twin blobs below max(RGB) 60); chroma separates them by 25x. So a candidate must
carry chroma of its own, and the floor is derived from two sources that are NOT the twin under
test: the class's own recorded cores, (70-95, 40-60, 15-40) -> C* 22.7-24.6, and the control's
material, a neutral Workbench clay at C* 0.9. The default sits between them at 8.0, roughly a
third of the class and nine times the control. It was not scanned. The same law is already load-
bearing in palette_gate.py, where its absence flags a steel sword as blue on every view.

WHAT THE FLOOR EXCLUDES, reported rather than silently dropped. A genuinely ACHROMATIC dark dot
is below the floor and is not censused. Twin-side, no such population is on record - E35 task 0a
measured the twin mid-tone at all six sampled pure-black locations, and that sub-population is
produced downstream of the texture, not painted into it. Every census therefore reports
`candidates_below_chroma_floor`, so a twin that did carry one would surface as a large rejection
count instead of a quiet zero.

WHY THE SIZE BOUND IS ON THE COLOUR STRUCTURE AND NOT ON THE DEVIATION FOOTPRINT. This was the
first implementation's defect and it is this repo's most-repeated lesson - ask what the
denominator is made of. A local-median estimate is blind INSIDE any structure wider than its
window, because the window's median there is the structure's own colour. So a large region does
not read as a large deviation; it reads as its four CORNERS. Measured on a planted 20x20 region
with a 15 px window: four fragments of 23 px^2 each, every one under a 36 px^2 threshold and not
one of them a speck. On a twin that is not hypothetical - it would count the corners of every
dark garment and put a floor under the census that no amount of despeckling could move, which is
exactly the E07 failure of a metric that cannot see a region of the wrong material. The bound
therefore applies to the connected SAME-COLOUR structure a candidate belongs to, using the
tool's existing 'meaningfully different colour' unit (--de-min) as the tolerance so no new
threshold is introduced. The planted region's four corners are then rejected as parts of one
400 px^2 structure and the 3x3 speck (structure 9 px^2) survives. Rejections are counted in the
report as `components_in_a_larger_colour_structure`, never dropped silently.

WHY LoG IS A CROSS-CHECK AND NOT THE DETECTOR. Scale-normalized LoG extrema over a capped sigma
range (Lindeberg 1998) locate a blob and report its diameter in one pass, which makes it a good
INDEPENDENT witness - but it responds to any dark structure at that scale, including legitimate
fine detail. It is reported per blob and never gates.

WHAT A GREEN CENSUS DOES NOT MEAN. It counts DARK-DEVIANT SMALL BLOBS. It cannot see a large
region of the wrong material - the class E07 established the high-pass statistics are blind to,
and the class that decided the Director's rejection there. Run palette_gate.py for that. It also
cannot see the pure-black sub-population measured in E35 task 0a, which is produced downstream of
the texture and is not in the twin at all.

Standards compliance:
  PIN_PER_STEP - every threshold, the input paths and their sha256, the tool's own sha256 and
    the numpy/scipy versions are echoed into the JSON sidecar, so a census replays.
  ANDON_AUTHORITY - shape mismatch between image and mask, an empty mask, and a mask that spans
    the whole frame all `raise`. They are `raise`, never `assert`: `python -O` and
    PYTHONOPTIMIZE=1 delete asserts silently (E21 Ruling 2).
  NAMED_COMPENSATORS - census mode writes only a JSON report and an optional overlay PNG, and
    modifies no input. Undo = delete them. Owner: the session running it.
  DECOMPOSE_BY_SECRETS - the detector is ONE code path (`detect`), returned as data. Nothing
    about correction lives in this file's detection half.
  UNCERTAINTY_GATED_HUMANS - it emits an overlay for a human. It renders no verdict.
  EXTERNAL_VERIFIER - it grades a twin against a locally-fitted estimate of that twin's own
    register, not against its author's expectation; and its validation corpus is the artifacts
    the DIRECTOR rejected, not fixtures chosen by the person who wrote it.

  twin_despeckle.py --mode census --images twin_*.png [--masks mask_*.png]
                    [--blob-max-px2 36] [--dark-dl 12.0] [--de-min 8.0]
                    [--out-json J.json] [--overlay DIR]
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np
import scipy
from PIL import Image, ImageDraw
from scipy import ndimage

TOOL_VERSION = "1.0.0"

# --- the deviation map -------------------------------------------------------------------


def _srgb_to_lab(rgb_u8):
    """sRGB uint8 HxWx3 -> CIE L*a*b* float, D65. Written out rather than imported so the
    numbers do not move if a dependency changes its white point."""
    c = rgb_u8.astype(np.float64) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ m.T
    white = np.array([0.95047, 1.00000, 1.08883])
    t = xyz / white
    d = 6.0 / 29.0
    f = np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)
    L = 116.0 * f[..., 1] - 16.0
    a = 500.0 * (f[..., 0] - f[..., 1])
    b = 200.0 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], axis=-1)


def _fill_outside(lab, mask):
    """Replace every out-of-mask pixel with its NEAREST in-mask value.

    The local median field must estimate the FIGURE's register. Left alone, a window
    straddling the silhouette would pull the backdrop in and bias the estimate exactly where
    the figure is thinnest - the failure mode this repo has already paid for twice (a
    half-width proxy that measures what fraction of a structure is edge, and an erosion tuned
    on a wide figure that annihilated thin strata). A nearest-figure fill makes the window's
    outside a mirror of its inside, so the estimate degrades smoothly instead of collapsing.
    """
    if mask.all():
        return lab
    _, idx = ndimage.distance_transform_edt(~mask, return_indices=True)
    return lab[idx[0], idx[1]]


def deviation_map(rgb, mask, window):
    """Return (dL, dE, local_lab). dL > 0 means the pixel is DARKER than its local register."""
    lab = _srgb_to_lab(rgb)
    filled = _fill_outside(lab, mask)
    local = np.empty_like(filled)
    for ch in range(3):
        local[..., ch] = ndimage.median_filter(filled[..., ch], size=window, mode="nearest")
    dL = local[..., 0] - lab[..., 0]
    dE = np.sqrt(((local - lab) ** 2).sum(axis=-1))
    return dL, dE, local


def log_response(rgb, sigmas):
    """Scale-normalized LoG maximum over a CAPPED sigma range. Positive = dark blob."""
    grey = _srgb_to_lab(rgb)[..., 0]
    best = None
    for s in sigmas:
        r = (s ** 2) * ndimage.gaussian_laplace(grey, sigma=s)
        best = r if best is None else np.maximum(best, r)
    return best


# --- the detector: ONE code path, used by every mode ---------------------------------------


def ring_delta(lab, comp_mask, region_mask, grow=3):
    """dE between a component's mean colour and a thin ring around it. REPORTED, never gates.

    It does not gate because it does not separate cleanly: a corner fragment's ring is half
    region and half register, so a planted 20x20 region's corners measure 14.8 against a true
    speck's 23.2 - a real gap, but one whose cut would have to be chosen after seeing it.
    """
    inner = ndimage.binary_dilation(comp_mask, iterations=1)
    ring = ndimage.binary_dilation(comp_mask, iterations=grow) & ~inner & region_mask
    if not ring.any():
        return None
    return float(np.sqrt(((lab[comp_mask].mean(axis=0) - lab[ring].mean(axis=0)) ** 2).sum()))


def colour_structure_area(lab, comp_mask, region_mask, tol, cap):
    """Area of the connected SAME-COLOUR structure this component belongs to.

    THE SIZE BOUND'S OPERAND. A speck is a small isolated dot of off-register colour, so the
    bound belongs on the COLOUR STRUCTURE, not on the deviation footprint - which is what the
    first implementation bounded, and why a planted 20x20 region survived as four 23 px^2
    corner fragments: a local-median estimate cannot see inside a structure wider than its
    window, so the footprint measured the corners rather than the region. Asking what the
    denominator is made of is this repo's most-repeated lesson.

    `tol` reuses the tool's existing 'meaningfully different colour' unit (--de-min); no new
    threshold is introduced. The search is confined to a window around the component: any
    structure that leaves it has already exceeded the cap.
    """
    ys, xs = np.nonzero(comp_mask)
    pad = int(2 * np.ceil(np.sqrt(cap)) + 6)
    y0, y1 = max(0, ys.min() - pad), min(comp_mask.shape[0], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(comp_mask.shape[1], xs.max() + pad + 1)
    sub_lab = lab[y0:y1, x0:x1]
    sub_comp = comp_mask[y0:y1, x0:x1]
    sub_reg = region_mask[y0:y1, x0:x1]
    mean = lab[comp_mask].mean(axis=0)
    similar = (np.sqrt(((sub_lab - mean) ** 2).sum(axis=-1)) <= tol) & sub_reg
    lbl, _ = ndimage.label(similar | sub_comp)
    ids = np.unique(lbl[sub_comp])
    ids = ids[ids > 0]
    return int(sum((lbl == i).sum() for i in ids))


def detect(rgb, mask, blob_max_px2, dark_dl, de_min, window, log_sigmas, chroma_floor):
    """Flag dark-deviant connected components at or below blob_max_px2.

    Returns (blobs, flagged_mask, diag). `blobs` is a list of dicts; `flagged_mask` is the
    union of the kept components ONLY - every pixel outside it is untouched by construction,
    which is the property a corrector inherits (Vincent 1993).
    """
    if rgb.shape[:2] != mask.shape:
        raise SystemExit("ANDON: image %s and mask %s disagree on shape"
                         % (rgb.shape[:2], mask.shape))
    if not mask.any():
        raise SystemExit("ANDON: figure mask is empty - nothing to census")

    dL, dE, _ = deviation_map(rgb, mask, window)
    lab_img = _srgb_to_lab(rgb)
    chroma = np.hypot(lab_img[..., 1], lab_img[..., 2])
    dark = (dL >= dark_dl) & (dE >= de_min) & mask
    cand = dark & (chroma >= chroma_floor)
    below_floor = int((dark & ~cand).sum())

    logr = log_response(rgb, log_sigmas)
    lab_lbl, n = ndimage.label(cand)
    blobs = []
    keep = np.zeros_like(cand)
    over = 0
    merged = 0
    for i in range(1, n + 1):
        full = (lab_lbl == i)
        area = int(full.sum())
        if area > blob_max_px2:
            over += 1
            continue
        rd = ring_delta(lab_img, full, mask)
        struct = colour_structure_area(lab_img, full, mask, de_min, blob_max_px2)
        if struct > blob_max_px2:
            merged += 1
            continue
        sl = ndimage.find_objects(full.astype(np.uint8))[0]
        comp = full[sl]
        ys, xs = np.nonzero(comp)
        y0, x0 = sl[0].start, sl[1].start
        keep[sl] |= comp
        sub_rgb = rgb[sl][comp]
        blobs.append({
            "area_px2": area,
            "bbox": [int(x0 + xs.min()), int(y0 + ys.min()),
                     int(x0 + xs.max()), int(y0 + ys.max())],
            "centroid": [float(x0 + xs.mean()), float(y0 + ys.mean())],
            "mean_rgb": [round(float(v), 2) for v in sub_rgb.mean(axis=0)],
            "min_rgb": [int(v) for v in sub_rgb.min(axis=0)],
            "dL_max": round(float(dL[sl][comp].max()), 3),
            "dE_max": round(float(dE[sl][comp].max()), 3),
            "L_star": round(float(lab_img[sl][comp][:, 0].mean()), 3),
            "log_max": round(float(logr[sl][comp].max()), 4),
            "ring_dE": round(rd, 3) if rd is not None else None,
            "colour_structure_px2": struct,
        })
    blobs.sort(key=lambda b: (-b["area_px2"], b["bbox"][1], b["bbox"][0]))
    diag = {
        "components_before_size_filter": int(n),
        "components_over_blob_max": over,
        "candidate_px": int(cand.sum()),
        "dark_px_before_chroma_floor": int(dark.sum()),
        "candidates_below_chroma_floor": below_floor,
        "components_in_a_larger_colour_structure": merged,
    }
    return blobs, keep, diag


def census_one(img_path, mask_path, args):
    rgb = np.asarray(Image.open(img_path).convert("RGB"))
    if mask_path:
        m = np.asarray(Image.open(mask_path).convert("L")) > 127
        if m.shape != rgb.shape[:2]:
            raise SystemExit("ANDON: mask %s %s does not match image %s %s"
                             % (mask_path, m.shape, img_path, rgb.shape[:2]))
        ys, xs = np.nonzero(m)
        if m.sum() and (xs.max() - xs.min() + 1 >= rgb.shape[1]
                        and ys.max() - ys.min() + 1 >= rgb.shape[0]):
            raise SystemExit("ANDON: mask %s spans the whole frame - a figure cannot. "
                             "Bbox-check it against the geometry before believing a number "
                             "read from it." % mask_path)
    else:
        m = np.ones(rgb.shape[:2], dtype=bool)

    blobs, keep, diag = detect(rgb, m, args.blob_max_px2, args.dark_dl, args.de_min,
                               args.window, args.log_sigmas, args.chroma_floor)
    total = sum(b["area_px2"] for b in blobs)
    fig = int(m.sum())
    row = {
        "image": img_path, "image_sha256": _sha(img_path),
        "mask": mask_path, "mask_sha256": _sha(mask_path) if mask_path else None,
        "size": [int(rgb.shape[1]), int(rgb.shape[0])],
        "figure_px": fig,
        "count": len(blobs),
        "total_area_px2": total,
        "largest_px2": blobs[0]["area_px2"] if blobs else 0,
        "area_as_figure_fraction_pct": round(100.0 * total / fig, 6) if fig else None,
        "log_agree_pct": (round(100.0 * float(np.mean([b["log_max"] > 0 for b in blobs])), 2)
                          if blobs else None),
        "diag": diag,
        "blobs": blobs,
    }
    return row, keep, rgb


def _sha(path):
    if not path:
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_overlay(rgb, keep, out_path, blobs):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    im = Image.fromarray(rgb).convert("RGB")
    d = ImageDraw.Draw(im)
    for b in blobs:
        x0, y0, x1, y1 = b["bbox"]
        d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], outline=(255, 210, 60))
    im.save(out_path)


def build_parser():
    ap = argparse.ArgumentParser(description="census the dark-speck class on a twin")
    ap.add_argument("--mode", required=True, choices=["census"],
                    help="census: read-only report. (clean lands with the corrector.)")
    ap.add_argument("--images", nargs="+", required=True)
    ap.add_argument("--masks", nargs="*", default=None,
                    help="figure mask per image, parallel to --images. Without it the whole "
                         "frame is censused, which on a twin includes the painted backdrop.")
    ap.add_argument("--blob-max-px2", type=int, default=36,
                    help="THE keyed threshold: keep components at or below this area in px^2. "
                         "36 = a 6 px dot's footprint, the top of the measured 2-6 px class at "
                         "the 352x1024 frame scale. Never a percentage of frame.")
    ap.add_argument("--dark-dl", type=float, default=12.0,
                    help="a candidate is darker than its local register by at least this many "
                         "L* units")
    ap.add_argument("--de-min", type=float, default=8.0,
                    help="and further than this in dE from it")
    ap.add_argument("--chroma-floor", type=float, default=8.0,
                    help="and carries at least this much chroma (C* in Lab) of its own. The "
                         "class is 'dark brown-to-black speckles' - a colour specification. "
                         "Derived from the class's recorded cores (C* 22.7-24.6) and the "
                         "control's neutral clay material (C* 0.9); not scanned. Candidates "
                         "rejected by it are counted in the report, never dropped silently.")
    ap.add_argument("--window", type=int, default=15,
                    help="local median window in px; must exceed the speck class several times "
                         "over so the estimate is robust to the specks themselves")
    ap.add_argument("--log-sigmas", type=float, nargs="+", default=[1.0, 1.5, 2.0, 3.0],
                    help="CAPPED sigma range for the LoG cross-check")
    ap.add_argument("--out-json")
    ap.add_argument("--overlay", help="directory for per-image overlay PNGs")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.masks and len(args.masks) != len(args.images):
        raise SystemExit("ANDON: %d masks for %d images - --masks is parallel to --images"
                         % (len(args.masks), len(args.images)))
    if args.window <= args.blob_max_px2 ** 0.5:
        raise SystemExit("ANDON: --window %d does not exceed the largest kept blob's side "
                         "(%.1f px) - the median field would be contaminated by the specks it "
                         "is meant to measure" % (args.window, args.blob_max_px2 ** 0.5))

    rows = []
    for i, img in enumerate(args.images):
        mp = args.masks[i] if args.masks else None
        row, keep, rgb = census_one(img, mp, args)
        rows.append(row)
        print("[census] %-52s count %5d  total %7d px2  largest %5d  fig %%%s"
              % (os.path.basename(img), row["count"], row["total_area_px2"],
                 row["largest_px2"],
                 ("%.5f" % row["area_as_figure_fraction_pct"])
                 if row["area_as_figure_fraction_pct"] is not None else " n/a"))
        if args.overlay:
            op = os.path.join(args.overlay,
                              os.path.splitext(os.path.basename(img))[0] + "_speck.png")
            write_overlay(rgb, keep, op, row["blobs"])

    report = {
        "tool": "twin_despeckle.py", "tool_version": TOOL_VERSION,
        "tool_sha256": _sha(os.path.abspath(__file__)),
        "mode": args.mode,
        "params": {
            "blob_max_px2": args.blob_max_px2, "dark_dl": args.dark_dl,
            "de_min": args.de_min, "window": args.window, "log_sigmas": args.log_sigmas,
            "chroma_floor": args.chroma_floor,
        },
        "env": {"numpy": np.__version__, "scipy": scipy.__version__,
                "python": sys.version.split()[0]},
        "images": rows,
        "totals": {
            "images": len(rows),
            "count": sum(r["count"] for r in rows),
            "total_area_px2": sum(r["total_area_px2"] for r in rows),
            "largest_px2": max([r["largest_px2"] for r in rows] or [0]),
        },
    }
    print("[census] TOTAL over %d image(s): count %d  area %d px2  largest %d"
          % (len(rows), report["totals"]["count"], report["totals"]["total_area_px2"],
             report["totals"]["largest_px2"]))
    if args.out_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
        with open(args.out_json, "w") as f:
            json.dump(report, f, indent=1)
        print("[census] wrote %s" % args.out_json)
    return report


if __name__ == "__main__":
    main()
