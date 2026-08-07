"""E13 — the SPIRAL LAW's guard, run before a brush opens on a job.

The standing law: order strokes to spiral outward from already-painted regions, or the brush
composes a NEW character instead of continuing one. That is a correctness constraint, not a
preference, and the number that guards it is the painted-adjacency fraction: of the pixels
this job asks the brush to invent, how many sit next to paint that already exists.

⚠ CORRECTED IN PLACE, with the measurement that overturned it (handoff 15, stroke 1). The
first version defined `painted = hit & ~job mask` and HALTED stroke 1 at 57.42% against the
ruled simulation's 92.34%. That was a false halt on an operand of my own making: `mask.png` is
the hole map **dilated by mask-dilate**, measured here at **2.40× the hole set** (187,904 px
against 78,380), so subtracting it removes a collar of genuinely-painted surface from
"painted" and the fraction falls by construction. Measured three ways on the same job:

  (A) painted = hit & ~job mask              57.42%   the brush's FIXED CONTEXT
  (B) painted = hit & ~undilated holes       87.96%   THE SIMULATION'S OPERAND — the gated one
  (C) (B) asked of the undilated holes only  71.13%

(B) lands within 4.4 points of the simulation's 92.34% — the ruling's basis stands, and the
gate is on (B). (A) is real and interesting and is now REPORTED, never gated: no bound for it
exists anywhere in the record, and inventing one while looking at the number it would judge is
the move that is always wrong. A diagnostic and a gate are different objects.

Measured on emit's own outputs, so it is the job the brush will actually receive:

  job mask  mask.png                         the holes DILATED, ∩ hit — what the brush may touch
  holes     erode(job mask, --radius)        the inverse of the dilation that made the job
  painted   hit & ~holes                     surface already carrying paint (the gated operand)
  adjacency fraction of job-mask pixels within --radius of a painted pixel

--radius defaults to the profile's mask-dilate, so both the erosion and the adjacency question
are asked at the same scale the job mask was grown at.

HALTS below --min. The handoff-14 simulation put the four strokes at 92.34 / 87.93 / 87.72 /
81.87 percent against the ship's 80.82-84.74 band; a stroke arriving far under that is a
hole-dominated frame and is exactly what the order exists to avoid opening on.

Standards compliance:
  ANDON_AUTHORITY — halts; --min is an argument so the bound is declared, not buried.
  NAMED_COMPENSATORS — writes at most one overlay PNG. Reads the job otherwise.
  EXTERNAL_VERIFIER — measures the job the brush receives, not the plan that produced it.
"""
import argparse
import os

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, binary_erosion, label

ap = argparse.ArgumentParser()
ap.add_argument("--job", required=True)
ap.add_argument("--radius", type=int, default=9)
ap.add_argument("--min", type=float, default=0.70,
                help="halt below this. 0.70 is the executor's pre-registered "
                     "hole-dominated line, well under the simulation's 81.87 worst case "
                     "and the ship's 80.82 floor.")
ap.add_argument("--expected", type=float, default=None,
                help="the simulation's figure for this stroke; reported as a delta")
ap.add_argument("--overlay")
args = ap.parse_args()

job = np.asarray(Image.open(os.path.join(args.job, "mask.png")).convert("L")) > 127
hit = np.asarray(Image.open(os.path.join(args.job, "hit.png")).convert("L")) > 127
assert job.shape == hit.shape, "ANDON: mask and hit disagree on shape"
K = np.ones((args.radius, args.radius), bool)
holes = binary_erosion(job, K)                    # undo emit's dilation to recover the holes
painted = hit & ~holes                            # THE GATED OPERAND (the simulation's)
context = hit & ~job                              # what the brush sees as fixed - diagnostic
grown = binary_dilation(painted, K)
n = int(job.sum())
assert n > 0, "ANDON: this job asks the brush to paint nothing"
adj = float((job & grown).sum()) / n
adj_ctx = float((job & binary_dilation(context, K)).sum()) / n
adj_holes = (float((holes & grown).sum()) / int(holes.sum())) if holes.any() else 0.0

lab, ncc = label(job)
sizes = np.bincount(lab.ravel())[1:] if ncc else np.array([0])
orphan = int(sizes[[not (job & grown)[lab == i + 1].any() for i in range(ncc)]].sum()) \
    if ncc else 0

print(f"[anchor] {os.path.basename(args.job)}: job {n:,} px (holes {int(holes.sum()):,} "
      f"dilated {n/max(int(holes.sum()),1):.2f}x)  painted {int(painted.sum()):,} px  "
      f"radius {args.radius}", flush=True)
print(f"[anchor]   painted-adjacency {adj*100:.2f}%  <- GATED"
      + (f"   simulation said {args.expected:.2f}%  (delta {adj*100-args.expected:+.2f})"
         if args.expected is not None else ""), flush=True)
print(f"[anchor]   DIAGNOSTICS, not gated: fixed-context adjacency {adj_ctx*100:.2f}% "
      f"(the collar the dilation hands to the brush); adjacency of the undilated holes "
      f"{adj_holes*100:.2f}%", flush=True)
print(f"[anchor]   job components {ncc:,}  largest {int(sizes.max()):,}  "
      f"in components touching NO paint: {orphan:,} px ({orphan/n*100:.2f}%)", flush=True)
if args.overlay:
    ov = np.zeros(job.shape + (3,), dtype=np.uint8)
    ov[hit] = (110, 110, 116)
    ov[job] = (232, 64, 64)
    ov[job & grown] = (60, 200, 90)
    Image.fromarray(ov).save(args.overlay)
    print(f"[anchor]   overlay -> {args.overlay} (green = anchored, red = NOT)", flush=True)

assert adj >= args.min, (
    f"ANDON: painted-adjacency {adj*100:.2f}% is below the {args.min*100:.0f}% floor. This "
    f"frame is hole-dominated and the brush at full denoise composes a NEW subject on one. "
    f"Do not open this stroke; report it.")
print(f"[anchor] PASS - the brush opens on paint.", flush=True)
