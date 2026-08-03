"""Measure whether a GENERATED view's hair boundary agrees with the MESH's hair geometry.

This is the direct measurement of the cause found 2026-08-02: the restylize invents its own
hair boundary, it disagrees with the mesh, and on re-projection hair-coloured pixels land on
face surface. Disagreement is visible in ONE 2D view -- no bake required, which makes the
test ~1 Cloud job instead of 8 + a bake.

    agreement = IoU(hair mask of the generated view, hair mask of the volume-baked render)

The reference mask comes from the VOLUME bake because that is the mesh's own colour and is
therefore registered to the hair geometry by construction.

⚠ Read the DIRECTION too, not just the IoU: `gen_only` is generated-hair sitting where the
mesh has FACE -- that is precisely the surface that smears on bake. A change that raises IoU
but also raises gen_only is not a win.

  hair_agree.py --ref vol_0.png --tests a.png b.png --labels A B [--band 260]
"""
import argparse
import numpy as np
from PIL import Image
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("--ref", required=True, help="the VOLUME-BAKED render (mesh ground truth)")
ap.add_argument("--tests", nargs="+", required=True)
ap.add_argument("--labels", nargs="+", default=None)
ap.add_argument("--band", type=int, default=260)
ap.add_argument("--v-thresh", type=int, default=90)
ap.add_argument("--bg-tol", type=float, default=18.0)
ap.add_argument("--crop-w", type=int, default=752)
args = ap.parse_args()

labels = args.labels or [str(i) for i in range(len(args.tests))]


def hair_mask(path, crop_to):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    corner = a[:12, :12].reshape(-1, 3).mean(axis=0)
    fig = np.abs(a - corner).max(axis=-1) > args.bg_tol
    v = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2HSV)[..., 2].astype(np.int16)
    band = np.zeros(a.shape[:2], bool)
    band[:args.band] = True
    m = (band & fig & (v < args.v_thresh)).astype(np.uint8) * 255
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    if n > 1:
        m = ((lab == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    if m.shape[1] != crop_to:
        dx = (m.shape[1] - crop_to) // 2
        m = m[:, dx:dx + crop_to]
    return m > 0


ref = hair_mask(args.ref, args.crop_w)
print(f"reference (mesh) hair: {ref.sum():,} px\n")
print(f"{'arm':>26} {'IoU':>8} {'gen_only%':>11} {'ref_only%':>11}")
for p, lab in zip(args.tests, labels):
    t = hair_mask(p, args.crop_w)
    inter = (ref & t).sum()
    union = (ref | t).sum()
    iou = inter / max(union, 1)
    gen_only = 100.0 * (t & ~ref).sum() / max(t.sum(), 1)
    ref_only = 100.0 * (ref & ~t).sum() / max(ref.sum(), 1)
    print(f"{lab:>26} {iou:>8.4f} {gen_only:>10.1f}% {ref_only:>10.1f}%")
print("\ngen_only = generated hair sitting on mesh FACE surface -> this is what smears on bake")
