"""TWIN FUSE - per-pixel median of K twins of one view, with a first-class disagreement map.

WHY MEDIAN AND NOT MEAN. Given K independent noisy observations of one clean signal, the
pointwise mean is L2-optimal and the pointwise MEDIAN is L1-optimal (Noise2Noise, Lehtinen
et al. ICML 2018). Speck invention is heavy-tailed, not Gaussian: one seed puts a dot
somewhere no other seed does. A mean drags that dot's darkness into the result at 1/K
strength; a median at K=3 rejects it outright. A mean would need ~10 frames plus sigma
clipping to do the same job, and each frame is a cloud job.

WHY THE DISAGREEMENT MAP IS AN OUTPUT AND NOT AN INTERNAL. Production burst merge computes
a spatially-varying robustness weight and downweights frames that disagree with a reference
(HDR+, Hasinoff et al. TOG 2016) - fusion gated on disagreement, never uniform. And naive
pixel-space averaging of diffusion samples blurs precisely where the samples disagree
STRUCTURALLY (Diffusion Mental Averages, 2026). So this tool refuses to hand back a fused
twin without also handing back where its inputs disagreed, and it halts when that
disagreement is structural rather than speck-scale.

WHAT MAKES A DISAGREEMENT STRUCTURAL, and why the bound is on the LARGEST COMPONENT rather
than the total. Speckle disagreement is many tiny blobs; a fold line, a prop edge or a
material boundary that moved between seeds is ONE large connected region. A total conflates
them and would either miss the ghosting or fire on every honest fusion - the same two-number
lesson palette_gate.py was built from, where a 4,882 px blob and 104 px of boundary speckle
had to be told apart.

WHY STRUCTURAL AGREEMENT IS MEASURED BEFORE THE FUSION IS TRUSTED (E35 R-b). Strong spatial
conditioning is what SHOULD make the seeds agree on structure and differ only in texture,
but measured pixel-level adherence under ControlNet is imperfect (ControlNet++, ECCV 2024),
so the agreement is a measurement and not an assumption. This tool reports inter-seed
silhouette IoU alongside the fused output.

Standards compliance:
  PIN_PER_STEP - every input path and sha256, every threshold, the tool's own sha256 and the
    numpy/scipy versions land in the JSON sidecar.
  ANDON_AUTHORITY - K < 2, a shape mismatch, an empty mask, a full-frame mask and a
    structural disagreement above the bound all `raise`. Never `assert`: -O deletes those.
  NAMED_COMPENSATORS - writes a fused PNG, a disagreement PNG and a JSON sidecar. Undo =
    delete them. No input is modified. Owner: the session running it.
  DECOMPOSE_BY_SECRETS - fusion knows nothing about specks; the detector lives in
    twin_despeckle.py and the census of a fused twin is taken by running that tool on it.
  EXTERNAL_VERIFIER - it does not grade its own output. It emits the disagreement map and
    the agreement metrics for a human to rule on.

  twin_fuse.py --images twin_a.png twin_b.png twin_c.png --mask m.png
               --out fused.png [--disagreement-max-px2 200] [--mad-thresh 6.0]
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np
import scipy
from PIL import Image
from scipy import ndimage

TOOL_VERSION = "1.0.0"


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _lab(rgb_u8):
    c = rgb_u8.astype(np.float64) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ m.T
    t = xyz / np.array([0.95047, 1.0, 1.08883])
    d = 6.0 / 29.0
    f = np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)
    return np.stack([116.0 * f[..., 1] - 16.0,
                     500.0 * (f[..., 0] - f[..., 1]),
                     200.0 * (f[..., 1] - f[..., 2])], axis=-1)


def fuse(stack, mask, mad_thresh, disagreement_max_px2):
    """stack: (K,H,W,3) uint8. Returns (fused_u8, disagreement_bool, metrics)."""
    K = stack.shape[0]
    if K < 2:
        raise SystemExit("ANDON: fusion needs at least 2 twins, got %d" % K)
    fused = np.median(stack.astype(np.float64), axis=0)
    fused_u8 = np.clip(np.rint(fused), 0, 255).astype(np.uint8)

    # per-pixel disagreement in a perceptual unit: the MAXIMUM deviation of any seed from
    # the fused value, in dE.
    #
    # It is a max and not a median absolute deviation, and that is not a style choice - the
    # first implementation used MAD and its own T67 fixtures caught it reading ZERO on five
    # planted disagreements. With K=3 and one dissenting seed the deviations are
    # [large, 0, 0] and their median is 0, so MAD is blind in exactly the case fusion exists
    # to handle. The question a disagreement map answers is "did ANY seed depart from the
    # consensus here", which is a max.
    #
    # Measured in dE rather than RGB counts so a dark region does not look agreed-upon by
    # default.
    fl = _lab(fused_u8)
    dev = np.stack([np.sqrt(((_lab(stack[i]) - fl) ** 2).sum(axis=-1)) for i in range(K)])
    maxdev = dev.max(axis=0)
    dis = (maxdev >= mad_thresh) & mask

    lbl, n = ndimage.label(dis)
    sizes = ndimage.sum(dis, lbl, range(1, n + 1)) if n else np.array([])
    largest = int(sizes.max()) if sizes.size else 0

    # inter-seed structural agreement: silhouette IoU between what each seed painted,
    # where 'painted' is 'differs from the fused consensus by less than the frame's own
    # spread' would be circular - so it is chroma-in-mask, the same figure definition the
    # arc's other instruments use, reported per pair.
    figs = []
    for i in range(K):
        lab_i = _lab(stack[i])
        figs.append((np.hypot(lab_i[..., 1], lab_i[..., 2]) >= 8.0) & mask)
    ious = []
    for i in range(K):
        for j in range(i + 1, K):
            u = float((figs[i] | figs[j]).sum())
            ious.append(float((figs[i] & figs[j]).sum()) / u if u else 1.0)

    metrics = {
        "k": K,
        "dev_thresh_dE": mad_thresh,
        "disagreement_px": int(dis.sum()),
        "disagreement_pct_of_figure": round(100.0 * dis.sum() / max(1, int(mask.sum())), 5),
        "disagreement_components": int(n),
        "largest_disagreement_px2": largest,
        "disagreement_max_px2_bound": disagreement_max_px2,
        "maxdev_median_in_figure": round(float(np.median(maxdev[mask])), 4),
        "maxdev_p99_in_figure": round(float(np.percentile(maxdev[mask], 99)), 4),
        "inter_seed_iou_min": round(float(min(ious)), 5) if ious else None,
        "inter_seed_iou_mean": round(float(np.mean(ious)), 5) if ious else None,
        "inter_seed_iou_all": [round(v, 5) for v in ious],
    }
    return fused_u8, dis, metrics


def build_parser():
    ap = argparse.ArgumentParser(description="median-of-K twin fusion with a disagreement map")
    ap.add_argument("--images", nargs="+", required=True,
                    help="K twins of THE SAME VIEW at different seeds")
    ap.add_argument("--mask", required=True, help="the view's geometry mask")
    ap.add_argument("--out", required=True)
    ap.add_argument("--out-disagreement")
    ap.add_argument("--out-json")
    ap.add_argument("--dev-thresh", "--mad-thresh", dest="mad_thresh", type=float,
                    default=6.0,
                    help="dE by which ANY seed must depart from the fused value for the "
                         "pixel to count as disagreed. Compared against a MAX over the "
                         "stack, not a median - see fuse().")
    ap.add_argument("--disagreement-max-px2", type=int, default=200,
                    help="ANDON: halt if the LARGEST connected disagreement component "
                         "exceeds this. Speckle disagreement is many tiny blobs; a moved "
                         "fold line or material boundary is one large region, and fusing "
                         "across it is what turns median into ghosting. Bounded on the "
                         "largest component, never on the total.")
    ap.add_argument("--report-only", action="store_true",
                    help="measure and write, but do not halt on the structural bound")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    mask = np.asarray(Image.open(args.mask).convert("L")) > 127
    if not mask.any():
        raise SystemExit("ANDON: mask %s is empty" % args.mask)
    my, mx = np.nonzero(mask)
    H, W = mask.shape
    if (mx.max() - mx.min() + 1 >= W) and (my.max() - my.min() + 1 >= H):
        raise SystemExit("ANDON: mask %s spans the whole frame - a figure cannot" % args.mask)

    imgs = []
    for p in args.images:
        a = np.asarray(Image.open(p).convert("RGB"))
        if a.shape[:2] != mask.shape:
            raise SystemExit("ANDON: %s is %s but the mask is %s"
                             % (p, a.shape[:2], mask.shape))
        imgs.append(a)
    stack = np.stack(imgs)

    fused, dis, metrics = fuse(stack, mask, args.mad_thresh, args.disagreement_max_px2)

    print("[fuse] K=%d  inter-seed IoU min %.5f mean %.5f"
          % (metrics["k"], metrics["inter_seed_iou_min"], metrics["inter_seed_iou_mean"]))
    print("[fuse] disagreement %d px (%.5f%% of figure) in %d components; largest %d px2 "
          "(bound %d)"
          % (metrics["disagreement_px"], metrics["disagreement_pct_of_figure"],
             metrics["disagreement_components"], metrics["largest_disagreement_px2"],
             args.disagreement_max_px2))
    print("[fuse] max-deviation in figure: median %.3f dE, p99 %.3f dE"
          % (metrics["maxdev_median_in_figure"], metrics["maxdev_p99_in_figure"]))

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    Image.fromarray(fused).save(args.out)
    print("[fuse] wrote %s" % args.out)
    if args.out_disagreement:
        os.makedirs(os.path.dirname(os.path.abspath(args.out_disagreement)), exist_ok=True)
        Image.fromarray((dis * 255).astype(np.uint8)).save(args.out_disagreement)
        print("[fuse] wrote %s" % args.out_disagreement)

    report = {
        "tool": "twin_fuse.py", "tool_version": TOOL_VERSION,
        "tool_sha256": _sha(os.path.abspath(__file__)),
        "inputs": [{"path": p, "sha256": _sha(p)} for p in args.images],
        "mask": {"path": args.mask, "sha256": _sha(args.mask), "px": int(mask.sum())},
        "params": {"dev_thresh": args.mad_thresh,
                   "disagreement_max_px2": args.disagreement_max_px2,
                   "report_only": bool(args.report_only)},
        "env": {"numpy": np.__version__, "scipy": scipy.__version__,
                "python": sys.version.split()[0]},
        "metrics": metrics,
        "out": args.out,
    }
    if args.out_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.out_json)), exist_ok=True)
        with open(args.out_json, "w") as f:
            json.dump(report, f, indent=1)
        print("[fuse] wrote %s" % args.out_json)

    if metrics["largest_disagreement_px2"] > args.disagreement_max_px2:
        msg = ("ANDON: largest connected disagreement component is %d px2, above the %d px2 "
               "bound - the seeds disagree STRUCTURALLY here, and median fusion across a "
               "structural disagreement is ghosting, not denoising"
               % (metrics["largest_disagreement_px2"], args.disagreement_max_px2))
        if args.report_only:
            print("[fuse] REPORT-ONLY, would have halted: %s" % msg)
        else:
            raise SystemExit(msg)
    return report


if __name__ == "__main__":
    main()
