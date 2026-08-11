"""E32 Gate 0 - what the reconstructor ACTUALLY sees, reproduced from its own source.

WHY THIS IS NOT A KEY. `e32_plate_geometry.py`'s quadratic key is contaminated on this
plate: the hard dark band across the bottom third is not representable by the background
model, so a two-sided residual returns the band as subject (835,526 px, full-frame bbox) and
a `lighter` polarity does not rescue it either - a step edge drags the ring fit down until
the flat upper field keys as subject too. Both failures are asserted in T64 rather than
described. The route does not use a key at all, so neither does this.

WHAT IT REPRODUCES, and why reproduction rather than invocation. `Trellis2ImageTo3DPipeline
.preprocess_image` (trellis2_image_to_3d.py:127-160) is four steps, and running it for real
means loading the whole GPU pipeline to reach four lines of PIL and numpy. This file is
those four steps transcribed, in order, with the source lines quoted in comments so the
transcription can be checked rather than trusted - the same construction
`e12_crop_silhouette.py` uses to reproduce `e12_head_render`'s camera.

    has_alpha = mode == 'RGBA' and not all(alpha == 255)
    scale     = min(1, 1024 / max(size))          -> LANCZOS
    output    = input if has_alpha else BiRefNet(input)
    bbox      = argwhere(alpha > 0.8 * 255) -> SQUARE crop about its centre
    output    = rgb * alpha                        -> PREMULTIPLIED, ground goes black

THE SEGMENTER IS BiRefNet AT 1024, not the PyPI rembg. `trellis2/pipelines/rembg/BiRefNet.py`
resizes to (1024, 1024) for inference and resizes the mask back to the input's size. The
route hands it a 1024 image, so it runs 1:1 with no resampling at its input - a fact that
matters to any prediction about thin structure and is invisible from the phrase "runs rembg".

FOUR ARTIFACTS, because they answer four different questions:
  <stem>_route.png   the LANCZOS 1024 downscale - the plate at the scale the segmenter and
                     every mask-derived measurement live in. Emitted so a mask is never
                     paired with a plate at a different resolution, which would compare a
                     width in one space against a width in another.
  <stem>_mask.png    the segmenter's alpha at route scale - the operand for plate geometry
  <stem>_cond.png    the premultiplied square crop - literally the reconstructor's input
  <stem>_pre.json    the numbers: has_alpha, scale, bbox, crop, areas

  e32_route_preprocess.py --image P.png --out-dir D [--stem armature]

Standards compliance: PIN_PER_STEP - the transcription's source file and line range are in
the JSON, and the plate's sha256 with it. ANDON_AUTHORITY - one halt, on the premise this
tool exists to check: if the plate's alpha is non-trivial the segmenter never runs and every
downstream number describes a different code path, so it raises rather than silently
measuring the wrong branch. NAMED_COMPENSATORS - writes three files to a new directory;
compensator `rm -r <out-dir>`. The plate is opened read-only. EXTERNAL_VERIFIER - it
transcribes and measures; it judges nothing.
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image

SRC = "trellis2/pipelines/trellis2_image_to_3d.py:127-160"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def preprocess(img, model):
    """The route's four steps, in the route's order. Returns (cond, mask, facts)."""
    facts = {"source": SRC, "input_size": list(img.size), "input_mode": img.mode}

    # if has alpha channel, use it directly; otherwise, remove background
    has_alpha = False
    if img.mode == "RGBA":
        alpha = np.array(img)[:, :, 3]
        if not np.all(alpha == 255):
            has_alpha = True
    facts["has_alpha"] = has_alpha
    if has_alpha:
        # ANDON: the segmenter never runs on this branch, so nothing measured downstream
        # would describe the route this experiment is about. Halt rather than measure the
        # other branch and label it with this one's name.
        raise SystemExit(
            "ANDON: plate alpha is non-trivial, so preprocess_image takes the has_alpha "
            "branch and BiRefNet is never invoked. Every downstream number would describe "
            "a different code path. Halting.")

    max_size = max(img.size)
    scale = min(1, 1024 / max_size)
    facts["scale"] = scale
    if scale < 1:
        img = img.resize((int(img.width * scale), int(img.height * scale)),
                         Image.Resampling.LANCZOS)
    facts["route_size"] = list(img.size)

    img = img.convert("RGB")
    route_rgb = img.copy()
    out = model(img)
    out_np = np.array(out)
    a = out_np[:, :, 3]
    facts["mask"] = {"area_px": int((a > 0.8 * 255).sum()),
                     "frac_of_route_frame": float((a > 0.8 * 255).mean()),
                     "alpha_min": int(a.min()), "alpha_max": int(a.max()),
                     "frac_partial": float(((a > 0) & (a < 255)).mean())}

    bbox = np.argwhere(a > 0.8 * 255)
    bbox = (np.min(bbox[:, 1]), np.min(bbox[:, 0]),
            np.max(bbox[:, 1]), np.max(bbox[:, 0]))
    facts["alpha_bbox_xyxy"] = [int(v) for v in bbox]
    facts["alpha_bbox_wh"] = [int(bbox[2] - bbox[0] + 1), int(bbox[3] - bbox[1] + 1)]
    center = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
    size = max(bbox[2] - bbox[0], bbox[3] - bbox[1])
    size = int(size * 1)
    crop = (center[0] - size // 2, center[1] - size // 2,
            center[0] + size // 2, center[1] + size // 2)
    facts["square_crop_xyxy"] = [int(v) for v in crop]
    facts["square_crop_size"] = int(size)

    cropped = out.crop(crop)
    arr = np.array(cropped).astype(np.float32) / 255
    premul = arr[:, :, :3] * arr[:, :, 3:4]
    cond = Image.fromarray((premul * 255).astype(np.uint8))
    facts["cond_size"] = list(cond.size)
    facts["cond_mean_luma"] = float(np.asarray(cond).mean())
    return cond, Image.fromarray(a, "L"), route_rgb, facts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--stem", default="plate")
    a = ap.parse_args()
    if not os.path.isdir(a.out_dir):
        os.makedirs(a.out_dir)  # scripts create their own output directories

    sys.path.insert(0, os.environ.get("TRELLIS_REPO", "E:/AI-Models/TRELLIS.2-repo"))
    # torch is imported HERE, not at module level, for the reason E23 ruled: a tool whose
    # recorded invocation form cannot answer `--help` without a GPU stack is not runnable
    # in a hermetic environment, and T62 pins exactly that. The sibling import below was
    # already lazy; this one was left at module scope by oversight and CI caught it.
    import torch
    from trellis2.pipelines import rembg as tr_rembg

    model = tr_rembg.BiRefNet()
    if torch.cuda.is_available():
        model.to("cuda")

    img = Image.open(a.image)
    cond, mask, route_rgb, facts = preprocess(img, model)
    facts["plate_sha256"] = sha256(a.image)
    facts["plate_path"] = os.path.abspath(a.image)

    rp = os.path.join(a.out_dir, a.stem + "_route.png")
    mp = os.path.join(a.out_dir, a.stem + "_mask.png")
    cp = os.path.join(a.out_dir, a.stem + "_cond.png")
    jp = os.path.join(a.out_dir, a.stem + "_pre.json")
    route_rgb.save(rp)
    mask.save(mp)
    cond.save(cp)
    txt = json.dumps(facts, indent=2, sort_keys=True)
    with open(jp, "w", encoding="ascii") as fh:
        fh.write(txt)
    print(txt)
    for p in (rp, mp, cp, jp):
        print("wrote %s" % p)


if __name__ == "__main__":
    main()
