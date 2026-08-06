# E12 handoff 4, Task 1 — blind predictions, the beast's canny derivation

**Written BEFORE any Canny has been run on this subject by this seat**, before the sweep
tool executes, before any silhouette is re-rendered. Committed first so it cannot be edited
against a result.

## Blindness disclosure — what is NOT blind

Four numbers reach this seat from E12 Ruling 10c and `beast.json`'s falsified `canny-low`
entry, and they are **read, not blind**:

> at 0.4/0.8 the control carries **5.20% / 2.13%** of the figure interior where the same clay
> at 0.05/0.15 carries **15.80% / 11.15%** (3.0× / 5.2×)

Those are the previous seat's measurement of views 1 and 5. The **instrument that produced
them is not in the repo** — no script, no JSON, and no stated definition of "figure
interior." So the numbers are inherited claims, and this session treats them as hypotheses
wearing a fact's clothes: C2 below is a prediction *about reproducing them*, not an
assumption that they are right.

Also not blind: the recorded control-image counts from the previous session's
`E12_pair/geom.log` — view 1 canny 36,011 px, view 5 canny 22,642 px, contour 25,256 px on
both, figure 490,941 px (26.754% of a 1792×1024 frame). Those ARE in the repo's record with
their invocation.

Everything below about the *shape* of the curve, the composition of the admitted set, and
the works-perfectly test is blind.

## The pre-registered grid — fixed here so it cannot be tuned afterwards

Sixteen candidate `(canny-low, canny-high)` pairs. `control_image` passes
`int(low*255), int(high*255)` to `cv2.Canny`, so the integer pair is what the operator
actually sees and is quoted beside every candidate.

| ladder (ratio ~2.2-3.0) | | fixed-low probe (high alone) |
|---|---|---|
| 0.02 / 0.06 -> 5/15 | 0.15 / 0.35 -> 38/89 | 0.05 / 0.10 -> 12/25 |
| 0.03 / 0.09 -> 7/22 | 0.20 / 0.45 -> 51/114 | 0.05 / 0.20 -> 12/51 |
| **0.05 / 0.15 -> 12/38** *(the rejection measurement's point)* | 0.25 / 0.55 -> 63/140 | 0.05 / 0.30 -> 12/76 |
| 0.08 / 0.20 -> 20/51 | 0.30 / 0.65 -> 76/165 | 0.10 / 0.20 -> 25/51 |
| 0.10 / 0.25 -> 25/63 | **0.40 / 0.80 -> 102/204** *(the profile's falsified point)* | 0.10 / 0.40 -> 25/102 |
| 0.12 / 0.30 -> 30/76 | | |

Views: **1 and 5** (the pair, the dispatch's minimum) plus **2** (yaw 90, profile head —
the most relief-dense head view on the per-view visibility table, 12.79% head-box first-hit)
and **4** (yaw 180, the true rear — the most membrane-dominated view). Four views, so the
curve is not read off two samples.

## Definitions, stated before the numbers exist

- **figure** = the exact mesh silhouette from `silhouette_masks.py` under
  `profiles/beast.json`, not a keyed mask.
- **interior** = the figure eroded by 5 px. The erosion exists to remove the composite
  boundary — `control_image` composites the figure onto `bg 0,0,0`, which makes the
  silhouette rim a maximal step that fires at every threshold and would otherwise dominate
  every candidate identically. Reported at erosion 3/5/9 as well, so the headline number is
  visibly not an artifact of choosing 5.
- **interior edge fraction** = (Canny pixels inside `interior`) / (area of `interior`).
- **admitted set** for a candidate = Canny pixels present at that candidate and absent at the
  profile's 0.4/0.8 — i.e. exactly what lowering the pair buys.

## The works-perfectly test, stated BEFORE reading anything

*What value does this measurement take when the lower pair works perfectly, and what value
when it does nothing?* If those are the same number it is not measuring the arm.

A lower canny pair **works perfectly** when the admitted set is **mesh relief** — scale rows,
frill layering, tooth rows, membrane vein ridges, horn flutes — i.e. edges that sit where the
render shows geometry. It **fails** when the admitted set is any of: backdrop gradient
banding, 8-bit quantization contours in smooth shading, or antialiasing speckle at the rim.
Four instruments separate those, none of which returns the same value in both cases:

1. **W-outside** — admitted pixels lying outside the figure, excluding a 5 px boundary ring.
   Perfect: 0. Failing on backdrop banding: large.
2. **W-band** — the fraction of admitted pixels whose local Sobel magnitude (|Gx|+|Gy|, the
   quantity `cv2.Canny` itself thresholds) sits at or below **8**, which is the two-LSB step
   of an 8-bit render. A 1-LSB quantization contour in smooth shading produces magnitude ~4.
   Perfect: ~0. Failing on banding: large. *(Not circular: the candidate's own low threshold
   is a floor on this quantity, so the test only has content for candidates whose
   `int(low*255)` sits at or below 8 — which is why the grid's bottom rung is 0.02 -> 5.)*
3. **W-speckle** — the fraction of admitted pixels in connected components of <= 3 px.
   Perfect: small (relief runs are long). Failing on AA speckle: large.
4. **W-eye** — 5x crops of the admitted set over the render, at a **smooth membrane field**
   (which carries no relief and should admit little) and at a **scaled flank/chest** (which
   carries relief and should admit much). Perfect: the two crops look different. Failing: the
   two crops look the same.

## Predictions

**C1 — instrument anchor (checkable).** A replica of `restylize_views.control_image`'s Canny
arithmetic, run at 0.4/0.8 on `E12_pair/clay/dragonclay_{1,5}.png` with the
`E12_pair/masks/` silhouettes, reproduces the recorded counts **exactly**: 36,011 px on
view 1 and 22,642 px on view 5. Any mismatch halts before the sweep is believed
(the validated-before-used pattern, E12 Ruling 6c).

**C1b — silhouette re-render is byte-identical.** Re-rendering silhouettes for all eight
views into a fresh directory reproduces views 1 and 5 **byte-for-byte** against
`E12_pair/masks/` (same mesh, same profile, same code — nothing has changed). Predicted
identical; a mismatch is a finding about determinism, not a licence to proceed.

**C2 — the inherited four reproduce within +/-1.0 point.** At erosion 5, the interior edge
fraction lands within 1.0 percentage point of 5.20% (view 1) and 2.13% (view 5) at 0.4/0.8,
and within 1.0 point of 15.80% and 11.15% at 0.05/0.15. *Falsifiable in both directions; a
miss means the previous seat's "figure interior" was a different object than this one, which
is worth knowing before the ruling cites those numbers again.*

**C3 — no knee. The curve is continuous and the choice is a judgement, not a discovery.**
Interior edge fraction rises monotonically as the pair falls, and **no adjacent pair of grid
candidates differs by a factor greater than 1.5**. Grounds: the underlying signal is
Workbench diffuse shading over scale relief, which has no contrast gap to find — the
"distant medians do not imply a gap" law, predicted forward rather than discovered after.
*If this is falsified and a real knee exists, that knee is the answer and this prediction
being wrong is the session's most valuable result.*

**C4 — backdrop banding cannot be admitted at all.** W-outside = **0 px** at every candidate
including 0.02/0.06, because `control_image` composites onto uniform `bg 0,0,0` before Canny
runs. The dispatch names backdrop banding as a works-perfectly risk; the prediction is that
the composite already forecloses it by construction and the risk is misattributed.

**C5 — the banding floor sits between the grid's bottom two rungs.** W-band (magnitude <= 8)
is **>= 15%** of the admitted set at 0.02/0.06 (`int(low*255)` = 5, below the 1-LSB step) and
**< 2%** at 0.05/0.15 (`int(low*255)` = 12, three LSB). So 8-bit quantization is a real
hazard at the very bottom of the grid and already excluded at the rejection measurement's
point.

**C6 — speckle rises as the pair falls, but stays a minority.** W-speckle is **higher at
0.05/0.15 than at 0.20/0.45** on every view, and **below 25%** at 0.05/0.15. Relief runs are
long; if speckle is the majority at 0.05/0.15 that pair is not adoptable.

**C7 — view 5 gains proportionally more than view 1.** The ratio (interior fraction at
0.05/0.15) / (interior fraction at 0.4/0.8) is **larger on view 5 than on view 1** — the
ruling's 5.2x against 3.0x says so and this seat is not blind to it. The blind part:
**view 4** (the true rear, most membrane-dominated of the four) has a **larger** ratio than
view 5, and **view 2** (profile head, most relief-dense) has the **smallest** ratio of the
four. Grounds: the high pair already fires on the head's hard structure, so the head view has
least left to gain.

**C8 — the fixed-low probe shows `high` is the weaker lever.** Holding low at 0.05 and moving
high across 0.10 -> 0.30 changes the interior edge fraction by **less than half** the change
from moving low across 0.05 -> 0.15 at fixed ratio. Grounds: hysteresis only extends chains
that a low-threshold seed already started.

**C9 — the proposal.** This seat will propose a pair in the range **0.05-0.12 low**. Stated
in advance so that landing outside it is visible as a surprise rather than reported as
though it were expected.

## A finding flagged BEFORE generation, so it is on the record blind

`beast.json`'s `restylize_views.negative` is
`"watermark, text, logo, blurry, photo, deformed"` — a FIRST-RUN OPERATING POINT inherited
from two subjects that ran a **painterly** register. Under Ruling 10b the beast's register is
**ultra-realistic**, and the negative prompt asks the sampler to move *away from* `photo`.
This seat does not change it: the negative is a decided profile value, profile writes are the
advisor's (Ruling 9e), and changing it alongside the register and the control would put three
variables in one run. It is recorded here, before the re-pair exists, as a finding for the
ruling rather than an observation made after seeing an outcome.

## What this task does not do

No threshold is armed as a gate (Ruling 10d: the structural channel at a style gate is the
eye). No value is written to `profiles/beast.json` — profile writes are the advisor's
(Ruling 9e). The rejected pair is **not** a baseline: nothing here is compared against it.
