"""RGBA-true turnaround frames: real alpha from the raycast silhouettes.

WHY THIS EXISTS. E37 requirement 4, and it is named new work rather than a checkbox: E36
task 0 measured this route's turn renders at **alpha 255 across the whole frame**, so a
"transparent PNG" from `turn_render.py` is opaque everywhere and the background colour is
baked into every consumer. The S03 lesson.

WHERE THE ALPHA COMES FROM, AND WHY NOT FROM THE RENDER. The obvious route is to key the
render's background colour. This repo retired that: *corner-median keying has failed three
times*, and its replacement rule is stated in CLAUDE.md — **where geometry can answer the
question, use geometry**. *Is there surface here* IS the raycast silhouette, exactly. So
alpha is the silhouette mask, copied in, not derived from pixels at all. The composite is
therefore exact by construction rather than accurate to a tolerance.

THE PAIRING IS CHECKED, NOT ASSUMED. A silhouette rendered at a different frame, margin or
yaw convention than the colour pass would misalign, and a misaligned alpha looks plausible.
So the tool refuses unless every pair agrees on shape, and it refuses a mask that is not
strictly binary — a soft mask would smuggle a keyed edge back in through the side door.

WHAT IT DOES NOT DO. It does not anti-alias the silhouette edge, and that is deliberate:
the mask is the geometric truth and softening it is a downstream compositing decision, not
this tool's to make. It does not touch RGB.

Usage:
  rgba_turnaround.py --renders DIR --render-tag perfv3flat --masks DIR --mask-tag perfv3
                     --out DIR --out-tag perfv3rgba [--views 0,1,...] [--json report.json]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image


def compose(render_path, mask_path):
    """Return (rgba array, stats). Raises on any pairing defect - never `assert`, because
    `python -O` deletes those and this decides what gets written to disk."""
    rgb = Image.open(render_path).convert("RGB")
    m = Image.open(mask_path).convert("L")
    if rgb.size != m.size:
        raise SystemExit("ANDON: %s is %s but its mask %s is %s - the colour pass and the "
                         "silhouette were not rendered at one frame"
                         % (os.path.basename(render_path), rgb.size,
                            os.path.basename(mask_path), m.size))
    a = np.asarray(m)
    uniq = np.unique(a)
    if not np.isin(uniq, (0, 255)).all():
        raise SystemExit("ANDON: mask %s is not binary (values %s...) - a soft mask would "
                         "reintroduce a keyed edge"
                         % (os.path.basename(mask_path), uniq[:6].tolist()))
    if not a.any():
        raise SystemExit("ANDON: mask %s is empty - no surface to composite"
                         % os.path.basename(mask_path))
    out = np.dstack([np.asarray(rgb), a]).astype(np.uint8)
    n_on = int((a > 0).sum())
    return out, {"frame": [rgb.size[0], rgb.size[1]], "opaque_px": n_on,
                 "transparent_px": int(a.size - n_on),
                 "opaque_frac_of_frame": round(n_on / float(a.size), 6)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--renders", required=True)
    ap.add_argument("--render-tag", required=True)
    ap.add_argument("--masks", required=True)
    ap.add_argument("--mask-tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--out-tag", default="rgba")
    ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    rows = []
    for v in [int(x) for x in a.views.split(",")]:
        rp = os.path.join(a.renders, "%s_%d.png" % (a.render_tag, v))
        mp = os.path.join(a.masks, "%s_%d.png" % (a.mask_tag, v))
        for p in (rp, mp):
            if not os.path.isfile(p):
                raise SystemExit("ANDON: missing %s" % p)
        rgba, st = compose(rp, mp)
        op = os.path.join(a.out, "%s_%d.png" % (a.out_tag, v))
        Image.fromarray(rgba, mode="RGBA").save(op)
        st.update(view=v, render=rp, mask=mp, out=op)
        rows.append(st)
        print("[rgba] view %d  %dx%d  opaque %d (%.3f%% of frame)  -> %s"
              % (v, st["frame"][0], st["frame"][1], st["opaque_px"],
                 100.0 * st["opaque_frac_of_frame"], os.path.basename(op)))

    # The property this tool exists for, checked on what was actually written.
    for st in rows:
        a_out = np.asarray(Image.open(st["out"]))[..., 3]
        if a_out.min() == 255:
            raise SystemExit("ANDON: view %d wrote alpha 255 everywhere - the flat-255 "
                             "defect this tool exists to fix" % st["view"])
    print("[rgba] %d frames written; none is flat-255" % len(rows))
    if a.json:
        json.dump({"rows": rows}, open(a.json, "w", encoding="utf-8"), indent=1)
        print("[rgba] wrote %s" % a.json)


if __name__ == "__main__":
    main()
