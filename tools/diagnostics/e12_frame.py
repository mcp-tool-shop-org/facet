"""E12 Gate 0 — derive a turnaround render frame from THIS mesh, and show the derivation.

`turn_render.py` at `--fit-axis height` (the default) sets `ortho_scale = size.z * margin`
and `sensor_fit = VERTICAL`, so the frame's vertical world coverage is `size.z * margin` and
its horizontal coverage is that times `W/H`. A frame narrower than the subject crops it.
E04's Gate 0 driver measured each hull's bbox for exactly this reason: the character line's
752x1024 would have cut the bowsprit off every sheet.

WHAT THIS ADDS TO THE PRECEDENT, AND WHY. E04's driver used `max(ex, ey) / ez` — the widest
AXIS over the height. That bounds views 0, 2, 4 and 6, which look straight down a world
axis. It does not bound views 1, 3, 5 and 7: at 45 degrees the camera's horizontal axis is
`(cos th, sin th, 0)` and the projected width can exceed either axis alone — up to
`(ex + ey)/sqrt(2)` for a shape that fills its box. On the galleons the gap was 3.7% and the
1.204 margin absorbed it. A dragon with a wingspread in x and a tail sweep in y can close
that margin, and a cropped wingtip on a designation sheet is the bowsprit mistake with
wings. So this computes the requirement at **every yaw actually rendered**, from the
vertices, and prints the precedent's axis-only number beside it so the difference is
visible rather than silent.

The width is also **rounded up to a multiple of 16**: the Qwen VAE downsamples by 8, a width
not divisible by 8 decodes short, and E04 Ruling 15 cost eight twins at 1066 -> 1064. Gate
0's frame becomes the twin frame if this mesh is designated, so it is chosen as if it will
be kept.

The half-width is measured about `mid = (lo + hi) / 2`, not as a raw span, because that is
where `turn_render` puts the camera: an asymmetric shape needs `2 * max|dot(p - mid, right)|`,
which is >= its span.

Standards compliance:
  PIN_PER_STEP — margin, step, views, base height and the rounding are flags; every derived
    quantity is printed and written to JSON.
  ANDON_AUTHORITY — raises if the chosen frame does not in fact contain the subject at every
    rendered yaw. The check is the arithmetic the frame was derived from, run in the
    opposite direction, so it can fail.
  NAMED_COMPENSATORS — reads a GLB, writes one JSON. Undo = delete it.
  DECOMPOSE_BY_SECRETS — nothing about the frame is inherited from another subject.
  EXTERNAL_VERIFIER — emits a frame and its derivation; judges no mesh.

  e12_frame.py --glb m.glb [--h 1024] [--margin 1.204] [--step 45]
               [--views 0,1,2,3,4,5,6,7] [--round 16] [--out frame.json]
"""
import argparse
import json
import math
import os

import numpy as np
import trimesh

ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--label", default=None)
ap.add_argument("--h", type=int, default=1024, help="render height; the fitted axis")
ap.add_argument("--margin", type=float, default=1.204, help="turn_render's --margin")
ap.add_argument("--step", type=float, default=45.0, help="turn_render's --step")
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--round", type=int, default=16,
                help="round the width UP to a multiple of this; 16 per the generator-legal "
                     "constraint (VAE /8 is the floor, /16 preferred)")
ap.add_argument("--out", default=None)
args = ap.parse_args()

GLTF_TO_BLENDER = np.array([[1.0, 0.0, 0.0],
                            [0.0, 0.0, -1.0],
                            [0.0, 1.0, 0.0]])

m = trimesh.load(args.glb, force="mesh", process=False)
co = np.asarray(m.vertices, dtype=np.float64) @ GLTF_TO_BLENDER.T
lo, hi = co.min(axis=0), co.max(axis=0)
mid = (lo + hi) / 2.0
ext = hi - lo
rel = co - mid

views = [int(v) for v in args.views.split(",")]
per_view = {}
need = 0.0
for idx in views:
    th = math.radians(idx * args.step)
    rgt = np.array([math.cos(th), math.sin(th), 0.0])
    w = 2.0 * float(np.abs(rel @ rgt).max())
    per_view[str(idx)] = round(w, 6)
    need = max(need, w)

axis_only = float(max(ext[0], ext[1]))
ratio_axis = axis_only / float(ext[2])
ratio_8 = need / float(ext[2])
raw_w = args.h * ratio_8
rx = int(math.ceil(raw_w / args.round) * args.round)
ry = args.h

# ANDON, run in the opposite direction from the derivation so it can actually fail:
# does the chosen frame contain the subject at every rendered yaw?
cover_h = float(ext[2]) * args.margin
cover_w = cover_h * (rx / ry)
worst = max(per_view.values())
if not (cover_w >= worst):
    raise AssertionError(
        "ANDON: frame %dx%d covers %.6f horizontally but view %s needs %.6f"
        % (rx, ry, cover_w, max(per_view, key=per_view.get), worst))
if not (cover_h >= float(ext[2])):
    raise AssertionError(
        "ANDON: frame %dx%d covers %.6f vertically against a height of %.6f"
        % (rx, ry, cover_h, ext[2]))

lab = args.label or os.path.splitext(os.path.basename(args.glb))[0]
print("[frame] %s  extent (Blender xyz) x=%.4f y=%.4f z=%.4f" % (lab, *ext), flush=True)
print("[frame]   widest AXIS / height   = %.4f   (E04's quantity: max(ex,ey)/ez)"
      % ratio_axis, flush=True)
print("[frame]   worst of %d YAWS / height = %.4f   at view %s   (+%.2f%% over the axis "
      "number)" % (len(views), ratio_8, max(per_view, key=per_view.get),
                   100 * (ratio_8 / ratio_axis - 1)), flush=True)
print("[frame]   %d * %.4f = %.1f -> round up to /%d -> RENDER %dx%d"
      % (args.h, ratio_8, raw_w, args.round, rx, ry), flush=True)
print("[frame]   horizontal margin at the worst view: %.4f (vertical %.4f by construction)"
      % (cover_w / worst, args.margin), flush=True)

rec = {"label": lab, "glb": os.path.abspath(args.glb),
       "extent_blender": [round(float(v), 6) for v in ext],
       "bbox_blender": [[round(float(v), 6) for v in lo], [round(float(v), 6) for v in hi]],
       "margin": args.margin, "step": args.step, "views": views, "round_to": args.round,
       "projected_width_per_view": per_view,
       "ratio_axis_only": round(ratio_axis, 6),
       "ratio_worst_yaw": round(ratio_8, 6),
       "worst_view": int(max(per_view, key=per_view.get)),
       "raw_width_px": round(raw_w, 2), "render_w": rx, "render_h": ry,
       "coverage_world": {"w": round(cover_w, 6), "h": round(cover_h, 6)},
       "horizontal_margin_at_worst_view": round(cover_w / worst, 6)}
if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(rec, open(args.out, "w"), indent=1)
    print("[frame] wrote %s" % os.path.abspath(args.out), flush=True)
