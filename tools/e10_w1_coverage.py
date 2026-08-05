"""E10 Arm W1 - does the geometric contact band cover what the model painted freehand?

NO GENERATION. This renders the contact mask through the raycast at the eight clay-view
cameras and measures, on view 7, how much of the founding exemplar's painted band the
geometry reaches.

W-H1, pre-registered in the spec and BLIND when this was written: a raycast band at the
placed waterline_z covers >=90% of the founding exemplar's observed band (the rejected
view-7 twin, seed 770700) on the matching view.

WHAT THIS GRADES, AND WHAT IT DOES NOT. Under E10 Ruling 1 decision 6 the exemplar
validates the band's GEOMETRY only - it painted contact where contact lives. It is not a
colour or content target: what it painted was the dynamic half that now belongs to the
shader. So this measures overlap of EXTENT and says nothing about colour, and a shortfall
means the plane and the model disagree about WHERE contact sits, not about what it is.

The denominator is reported BOTH ways because the record distinguishes them (Step 0.1):
2,272 px is the exemplar's total band, 2,002 px is its largest connected component, and
the spec's ">=90% of 2,002" quotes the component. Neither is chosen here.

ANCHOR, and it can fail: the emitted hit mask at each clay view must equal that view's
exact silhouette (masks/galleonclay_N.png). If a frame or a camera has drifted, the
exemplar and the render are not in the same picture and no overlap number means anything.

  e10_w1_coverage.py [--out DIR]
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import label

Image.MAX_IMAGE_PIXELS = None
PY = r"E:\AI-Models\trellis2-env\Scripts\python.exe"
TOOL = r"E:\AI\facet\tools\texpass_iter.py"
REPO = r"E:\AI\facet"
STROKE = r"E:\AI\training\facet_next\E04_stroke"
ARMT = r"E:\AI\training\facet_next\E04_armT72"
PREP = r"E:\AI\training\facet_next\E04_shipprep"
CHROMA_FLOOR, BAND_HUE = 12.0, (240.0, 273.0)


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(STROKE, "e10_w1"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    J = os.path.join
    st = J(STROKE, "e10_contact", "state")
    rep = {"prediction": "W-H1: the raycast band covers >=90% of the founding exemplar's "
                         "band on the matching view. Pre-registered in the spec; BLIND - "
                         "the contact mask had never been rendered at view 7."}

    # ---- render the contact mask at the eight clay views -----------------------------
    per_view = {}
    for i in range(8):
        yaw = i * 45
        r = subprocess.run([PY, TOOL, "emit", "--state", st, "--prep", PREP,
                            "--glb", J(PREP, "prep_uv.glb"), "--yaw", str(yaw),
                            "--el", "0", "--profile", J(REPO, "profiles", "ship.json")],
                           capture_output=True, text=True)
        if r.returncode:
            print("ANDON: emit failed at yaw %d\n%s" % (yaw, r.stderr[-400:]))
            return 1
        job = J(st, "job_y%+04d_e%+03d" % (yaw, 0))
        band = np.asarray(Image.open(J(job, "render.png")).convert("L")) > 127
        hit = np.asarray(Image.open(J(job, "hit.png")).convert("L")) > 0
        clay = np.asarray(Image.open(J(ARMT, "masks", "galleonclay_%d.png" % i))
                          .convert("L")) > 127
        # ANCHOR: same picture as the twins, or nothing downstream means anything
        if hit.shape != clay.shape or not np.array_equal(hit, clay):
            n = int((hit != clay).sum()) if hit.shape == clay.shape else -1
            print("ANDON: view %d emitted silhouette != masks/galleonclay_%d.png "
                  "(%d px differ). The render and the twins are not the same picture. "
                  "HALT." % (i, i, n))
            return 1
        rows = np.where(band.any(axis=1))[0]
        per_view[i] = {
            "yaw": yaw, "band_px": int(band.sum()),
            "top_row": int(rows.min()) if len(rows) else None,
            "bottom_row": int(rows.max()) if len(rows) else None,
            "px_outside_exact_silhouette": int((band & ~hit).sum()),
            "pct_of_figure": 100.0 * band.sum() / max(1, hit.sum()),
            "silhouette_px": int(hit.sum())}
        print("[view %d] yaw %3d  band %6d px (%.2f%% of figure)  rows %s-%s  "
              "outside silhouette %d  [silhouette == clay mask]"
              % (i, yaw, band.sum(), per_view[i]["pct_of_figure"],
                 per_view[i]["top_row"], per_view[i]["bottom_row"],
                 per_view[i]["px_outside_exact_silhouette"]))
        if i == 7:
            np.save(J(args.out, "band_view7.npy"), band)
    rep["per_view"] = per_view

    # ---- the exemplar's band, re-measured the same way Step 0.1 did ------------------
    ex = np.asarray(Image.open(J(ARMT, "twins", "twin_7_REJECTED_seed770700.png"))
                    .convert("RGB"), dtype=np.float32) / 255.0
    sil7 = np.asarray(Image.open(J(ARMT, "masks", "galleonclay_7.png")).convert("L")) > 127
    lab = to_lab(ex)
    C = np.hypot(lab[..., 1], lab[..., 2])
    Hd = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0
    exb = (C > CHROMA_FLOOR) & (Hd >= BAND_HUE[0]) & (Hd <= BAND_HUE[1]) & sil7
    lbl, _ = label(exb)
    sizes = np.bincount(lbl.ravel())[1:]
    cc = lbl == (int(np.argmax(sizes)) + 1)

    band7 = np.load(J(args.out, "band_view7.npy"))
    rep["exemplar"] = {"total_px": int(exb.sum()), "largest_cc_px": int(cc.sum())}
    cov = {}
    for name, ref in (("total_2272", exb), ("largest_cc_2002", cc)):
        inter = int((ref & band7).sum())
        cov[name] = {"denominator": int(ref.sum()), "covered": inter,
                     "coverage_pct": 100.0 * inter / max(1, int(ref.sum()))}
    rep["W_H1_coverage"] = cov
    rep["band7_px"] = int(band7.sum())
    rep["exemplar_outside_band7"] = int((exb & ~band7).sum())

    print("\n[W1] the founding exemplar's band: %d px total, %d px largest component"
          % (exb.sum(), cc.sum()))
    print("[W1] the geometric contact band at view 7: %d px" % band7.sum())
    for name, c in cov.items():
        print("[W1] coverage against %-16s %6d / %6d = %6.2f%%"
              % (name, c["covered"], c["denominator"], c["coverage_pct"]))
    print("\n[W1] PREDICTION was >=90%%, pre-registered and blind.")
    json.dump(rep, open(J(args.out, "w1_coverage.json"), "w"), indent=1)
    print("[json] %s" % J(args.out, "w1_coverage.json"))
    print("Reported, not judged. The advisor rules on what it means.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
