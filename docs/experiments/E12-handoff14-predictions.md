# E12 handoff 14 — predictions, registered before the work

**Executor session, 2026-08-06.** Written **before** anything in this dispatch was measured:
before the hole map was decomposed, before a candidate camera was scored, before a thin_extent
value was evaluated at the brush level, and before a stem was derived.

**Blind status, disclosed per item** — same three classes as handoff 13, and the labels are
load-bearing:

- **BLIND** — no recorded number bears on it.
- **DERIVED** — computed from numbers already in the repo. A derived miss is the stronger
  finding because the derivation is on the page.
- **CODE-READ** — read off a tool's source before running it.

Read to write this: `CLAUDE.md`, Rulings 7 (7a–7e) and 24 (24a–24f), `profiles/beast.json`
(post-24a), the handoff-13 report, `E04-ruling.md` Ruling 23 (the ship's stroke lifecycle),
`E04-stroke-cameras.json` (the ship's greedy and order precedent, quoted below),
`E12_prep/{thin_curve.json,thin_curve_leftwing.json,ceiling.json}`, and the sources of
`texpass_iter.py`, `e04_stroke_cameras.py` and `brush_reach.py`. Nothing has been run.

---

## The arithmetic everything below rests on

Ruled at 24e: valid **3,240,510** · reach **1,635,304** (50.46%) · A0 styled **1,430,687**
(44.2% of valid, 87.5% of reach) · holes **1,809,823**.

- brush's set = 1,635,304 − 1,430,687 = **204,617**
- dilation's set = 3,240,510 − 1,635,304 = **1,605,206** — and 204,617 + 1,605,206 =
  1,809,823 exactly, so the decomposition closes with no remainder. **88.7% of holes are
  geometry** against the ship's 91%.

## P1 — where the brush's holes are (Task 1)

- **P1a — DERIVED, and it is the prediction the rest hang off. The brush's set is
  overwhelmingly EROSION RIM AND THIN STRUCTURE, not coherent unpainted fields.** Every one of
  those 204,617 texels was *reachable* — some camera had it facing > 0.45 and first-hit
  visible — and was rejected anyway, which leaves only the trust mask and the edge erosion.
  The per-view arithmetic is already on the record: yaw 0 reaches 480,442 and styles 370,108,
  a 110,334 loss at one view. So I predict the holes trace silhouettes: wing trailing edges,
  membrane sheets, spine and frill tips, claw tips, the wing-body gap's lips.
- **P1b — DERIVED. Connected-component structure: many small components, no dominant field.**
  Largest 3-D connected component of the brush set **under 25,000 texels** (12% of it), and
  **over 60%** of the set living in components under 1,000 texels. The ship's holes were two
  coherent surfaces (deck, sides); this subject's should not be.
- **P1c — DERIVED. Up-facing share is small and diffuse.** Brush texels with normal
  z > 0.5: **6–14%** of the set (12,000–29,000 texels). Erosion rim has no orientation
  preference, so up-facing should sit near the mesh's own up-facing share rather than above it.
- **P1d — BLIND. The single most-holed named region is the WING MEMBRANE.** Ranked by holes
  as a share of that region's own reachable texels, the wing boxes beat head, body and limbs.

## P2 — the Ruling 7 elevated re-open check (Task 1's explicit question)

- **P2a — DERIVED. The re-open does NOT fire; it closes the other way, with numbers.**
  Adding the four elevated candidates (0/180 at 40° and 55°, the pair 7a measured) to the
  eight eye-level yaws lifts first-hit coverage of the brush's 204,617 by **under 3
  percentage points**, and there is **no up-facing hole field over 20,000 texels** for an
  elevated stroke to serve. Grounds: 7a's three findings all survive the hole map — the buy
  was +1.768 points on *reach*, the ordering was inside sampling noise, and the unreached half
  is self-occluded. What changed at 24e is that the brush's set is now known to be rim, and a
  rim is served by the camera nearest its own yaw, not by one above it.
- **P2b — DERIVED, the falsifier named in advance.** If P2a is wrong it will be because the
  **wing upper surfaces** are large, up-facing and eroded along their spans — the one place on
  this subject where a big up-facing field could hide. So the check must report the up-facing
  brush set **inside the wing boxes separately**, or it has not answered the question.

## P3 — the stroke cameras and the order (Task 2)

Candidate set I will use, stated before scoring: the **eight route yaws plus the eight
interleaved 22.5° offsets, sixteen at 22.5° spacing, all at elevation 0**, with elevated
candidates added *only* if P2a fails. The route yaws stay IN, unlike the ship's derivation
which excluded its twin yaws — because on this subject the holes are the twins' own erosion
rim, and `texpass_iter`'s commit edge-dist (4.0 px) is far tighter than `project_twins`'
scaled ~14.9 px, so a same-yaw stroke recovers rim the twin refused.

- **P3a — DERIVED. The greedy is FLAT, and that is the finding.** Because the holes are rim
  rather than field, no camera dominates: first pick closes **under 20% of the brush set**,
  and pick 8's marginal is **above 40%** of pick 1's. The ship's decayed 40,759 → 13,126
  (32%) across eight picks on coherent surfaces; a rim-distributed set should decay more
  slowly.
- **P3b — DERIVED. Greedy set size 6–10 at the ship's stopping discipline**, with cumulative
  coverage of the brush set at the stop **55–80%**. Named consequence: whatever the strokes do
  not close falls to dilation at finalize, and that residual should be quoted before the first
  stroke, the way the ship pre-registered its deck plateau.
- **P3c — DERIVED. A clean spiral anchor exists.** Painted-adjacency fraction for the
  best-anchored camera **≥ 0.90**, above the ship's 80.82–84.74 band, because rim holes are
  by construction surrounded by paint on the inboard side. If any camera comes in **below
  0.70** it is a hole-dominated frame and I will name it as one the order must not open on.
- **P3d — CODE-READ. The route yaws win the early picks.** At least two of the first three
  greedy picks are route yaws (multiples of 45°), not interleaves.

## P4 — thin_extent at the brush level (Task 3)

This is the arc's one deliberately undecided value and the tension is now sharp: **the brush's
territory and thin_extent's target are the same surface.**

- **P4a — DERIVED, the headline. Any non-zero thin_extent withholds a LARGE share of the
  brush's own set** — far more than it withholds of the figure. The banked figure-level curve
  says 0.01 withholds 24.85% of view 0's figure and 41.44% of its wing region; the brush's set
  is *selected for thinness*, so the same value should bite two to three times harder on it.
  Predicted withheld fraction of the 204,617: **0.005 → 25–45%**, **0.0075 → 45–65%**,
  **0.01 → 60–80%**.
- **P4b — DERIVED. Membrane holes specifically are withheld harder still**: at 0.0075 and
  0.01, **over 75%** of the brush's membrane-region holes are withheld.
- **P4c — DERIVED. The region-aware candidate is the only one that separates.** A value
  applied inside the wing boxes and a different one outside can hold the withheld fraction of
  the non-wing brush set **under 25%** while still masking the membrane sheet — because
  Q12's 1.78× concentration is a *global* statistic and the wing boxes are exactly the region
  that concentration lives in.
- **P4d — BLIND, on the artifact criterion.** The crops of what 0.01 forbids will show
  **whole structures**, not rims: entire membrane panels, spine rows and frill blades greyed
  out. If instead they show hairline outlines, P4a is wrong and the value is cheap.
- **No proposal is offered and none will be.** Ruling 7c deferred the value to the ruling with
  the wing boxes and the artifact criterion in the room; assembling is the job.

## P5 — the brush prompts and the recipe keys (Task 4)

- **P5a — DERIVED. The ship's `brush_prompts` = one constant string does NOT transfer.**
  Ruling 23 rested that on "this subject has no view-specific anatomy words". The beast fails
  that premise by construction — Ruling 9d, six of eleven elements name head anatomy, and the
  measured drop map already differs per view (20/20/20/14/16/14/20/20). So the draft will be
  **per-stroke stems**, and I predict the stroke stems' term counts span **at least 5** terms
  between the fullest and the thinnest.
- **P5b — CODE-READ. The agreement-by-value trap is real and still live.**
  `profiles/beast.json` records that `brush_cloud_step.py` calls `subject_profile.bind()`
  **zero** times, so no profile block reaches its argparse: it carries its own defaults
  (seed 770700, steps 20, cfg 2.5, lora_w 0.75, cn_strength 1.0) and a hardcoded CLOUD_LORA.
  Predicted: the defaults still read that way in source, **`lora_w 0.75` and the hardcoded
  card are both still present**, and agreement with the beast's ruled `lora-w 0.0` holds only
  by value passed per invocation — nothing structural prevents a forgotten flag from loading
  the saltroad card onto this dragon. I will verify by reading, not assume, and enumerate
  every key with its tool default beside the accepted route's value.
- **P5c — BLIND. `cn_strength` is the one key where the brush stage and the twin stage
  legitimately differ** (1.0 against the twins' 0.9, per the ship's recorded distinction), and
  it is the key most likely to arrive by silence.

## What would falsify each

P1a: holes forming large interior fields rather than tracing silhouettes. P1b: a component
over 25,000. P1c: up-facing outside 6–14%. P2a: elevated adding ≥ 3 points, or any up-facing
field over 20,000. P3a: first pick over 20%, or pick 8 under 40% of pick 1. P3c: best anchor
under 0.90. P4a: any candidate withholding less of the brush set than of the figure. P5a: the
stroke stems coming out within 4 terms of each other. P5b: `brush_cloud_step` binding a
profile, or its defaults having moved.

**No verdicts in this file, and none in the report. Nothing generates, nothing spends, and
thin_extent is assembled rather than proposed.**
