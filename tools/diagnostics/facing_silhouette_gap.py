"""Per-facing silhouette gap. A DIAGNOSTIC. It is deliberately NOT a gate.

⚠ READ THIS BEFORE USING IT TO DECIDE ANYTHING. This was written to answer "is there
visible air between the hand and the shield" and it PASSES the asset that defect is in:
all eight facings report "overlapping", because the shield overlaps the TORSO in
silhouette while meeting the hand over 3.1 sq cm. It measures figure-to-prop, and the
question was hand-to-prop. Gate on tools/verify/prop_contact.py, which measures the
surfaces; read this beside it to see which facings show the join and which hide it.

Kept rather than deleted, with the reason, because the next person to reach for a
screen-space contact check should meet this first.

3D contact is necessary and not sufficient. A billboard is judged on one silhouette per
facing, and two surfaces that touch at a single point in 3D read as separated air from
seven of eight camera yaws. This measures, per view, the shortest distance in PIXELS
between the figure's silhouette and the prop's silhouette, rendered through one shared
camera by facing_masks.py.

  0 px   the silhouettes touch or overlap. No visible air.
  > 0    that many pixels of background lie between them in this facing.

The gate is stated on the command line and is not derived from the result it judges.

  python facing_contact.py --masks <dir> [--max-gap 0] [--json-out ...]
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

ap = argparse.ArgumentParser()
ap.add_argument("--masks", required=True)
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--max-gap", type=float, default=0.0,
                help="pixels of background permitted between figure and prop, per facing")
ap.add_argument("--json-out", default=None)
args = ap.parse_args()

rows = []
for i in [int(v) for v in args.views.split(",")]:
    pb = os.path.join(args.masks, "mask_body_%d.png" % i)
    pp = os.path.join(args.masks, "mask_prop_%d.png" % i)
    for p in (pb, pp):
        if not os.path.exists(p):
            raise SystemExit("ANDON: missing %s - run facing_masks.py first" % p)
    B = np.asarray(Image.open(pb).convert("RGBA"))[..., 3] > 0
    P = np.asarray(Image.open(pp).convert("RGBA"))[..., 3] > 0
    if not B.any() or not P.any():
        raise SystemExit("ANDON: view %d has an empty mask (body %d px, prop %d px) - the "
                         "pass rendered nothing" % (i, int(B.sum()), int(P.sum())))
    overlap = int((B & P).sum())
    if overlap:
        gap, where = 0.0, None
    else:
        # distance from every pixel to the nearest prop pixel, read at the body's pixels
        dt, inds = ndimage.distance_transform_edt(~P, return_indices=True)
        d_on_body = np.where(B, dt, np.inf)
        flat = int(np.argmin(d_on_body))
        y, x = np.unravel_index(flat, d_on_body.shape)
        gap = float(d_on_body[y, x])
        where = [int(x), int(y)]
    rows.append({"view": i, "body_px": int(B.sum()), "prop_px": int(P.sum()),
                 "overlap_px": overlap, "gap_px": gap, "closest_body_px": where})

print("%5s %9s %9s %10s %9s  %s" % ("view", "body px", "prop px", "overlap", "gap px", "closest approach at"))
for r in rows:
    print("%5d %9d %9d %10d %9.2f  %s"
          % (r["view"], r["body_px"], r["prop_px"], r["overlap_px"], r["gap_px"],
             r["closest_body_px"] or "(overlapping)"))

if args.json_out:
    with open(args.json_out, "w", encoding="utf-8") as f:
        json.dump({"max_gap": args.max_gap, "rows": rows}, f, indent=2)

bad = [r for r in rows if r["gap_px"] > args.max_gap]
print()
if bad:
    print("ANDON: %d of %d facings show background between the figure and the prop "
          "(max-gap %.2f px): %s" % (len(bad), len(rows), args.max_gap,
                                     ", ".join("view %d = %.2f px" % (r["view"], r["gap_px"]) for r in bad)))
    sys.exit(2)
print("CONTACT: every facing has the prop touching the figure in silhouette")
