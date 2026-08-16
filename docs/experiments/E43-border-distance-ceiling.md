# E43 — Bound the border-distance lever before building it

**Spec written BEFORE the work.** Advisor seat, 2026-08-16, under the Director's standing
authority to run experiments testing the levers. **Continuation of the E41 seat**, which already
holds the calibrated instrument and the data on disk — a fresh seat would rebuild both.

---

## What E41 established, and what it did not

E41 measured, on 118,007 reference-class defect texels against a 778,024-texel clean-adjacent
control ring (n=4,000 sampled each):

| quantity | defect | clean | reading |
|---|---|---|---|
| source footprint | median **0.380 px** | median **0.650 px** | defect texels are **less** minified — the advisor's candidate is dead |
| distance to nearest material boundary in the twin | median **0.439 px** | median **2.333 px** | **5.3×**; 61.6% vs 38.3% within 1 px |

**The advisor's minification candidate was killed as specified.** Predicted band [0.7, 1.5],
measured 0.586, and the miss was in the direction *against* the candidate. Minification is real
on this route (tails to ~500× in both populations) but it is **not the differentiator**.

**What replaced it is a correlation, not a mechanism.** E41's own words, preserved because the
restraint is correct: this *"doesn't establish the boundary itself is misplaced in the twin — it
could be an exactly-correct garment seam — only that the sample point sits close enough to some
transition for interpolation to blend across it."* So *the twin is clear* survives at the level of
content and is complicated at the level of a per-texel sample.

**Converging from the literature:** Callieri et al., C&G 32(4) 2008, DOI 10.1016/j.cag.2008.05.004
— the field's one true continuous per-texel blender — multiplies its angle and depth masks by a
**border mask: image-space distance to the nearest border or silhouette discontinuity**, combined
by **product specifically to preserve minima**. Our weight is `np.power(facing, 6.0)` alone
(`project_twins.py:873`). Two independent lines name the same missing component.

## The question this arc answers, and ONLY this

**Not** "does a border term help." **"What is the most a border term could possibly buy?"**

A material boundary is a property of the garment, so every view sees roughly the same boundary in
roughly the same place. **If no view has a clean sample at a defect texel, then no weighting over
those views can fix it** — you would be choosing among contaminated samples, and downweighting all
of them starves the texel to fill.

The mechanism by which a border term *could* work is foreshortening: a region seen face-on puts
more pixels between the sample and the boundary than the same region seen edge-on. So the term
discriminates **only where views differ in how far their sample sits from the boundary.**

**Bound it before building it.** One executor priced a six-stroke experiment at +1.7 points and
skipped it; that is the standard here.

## Task 1 — the ceiling

For each of the 118,007 defect texels, across **all eight views that can see it** (not just the
owner), compute the distance from that view's sample point to the nearest material boundary in
that view's twin — the same instrument and the same threshold you already calibrated.

Report:

1. The distribution of **max-over-views** border distance per defect texel.
2. **The headline number: what fraction of defect texels have at least one view whose sample sits
   at least as far from a boundary as the CLEAN control's median (2.333 px)?** That is the
   fraction a perfect border-aware selector could rescue, and it is the ceiling on this lever.
3. The same fraction at one or two other reference points of your choosing, stated as a curve
   rather than a single cut — **do not invent a threshold.** This repo withdrew a condition rather
   than re-derive one while looking at the results it would judge, and that precedent binds.
4. How often the **owner** view is the best-available view on this measure. If the owner is
   usually already the best, the lever is weak regardless of the ceiling.

⚠ **Grade the arm only on what it can move.** The ceiling is a property of the camera set, not of
any weighting. If it comes back low, that is not a failure of the border idea — it is evidence
that the defect is **unreachable from this rig**, which hands the question to E42's camera
geometry rather than to a weight term. Say so in exactly those terms if that is what you find.

---

## ⚖ RULING — Task 2 does NOT run. The border-weight lever is dead. (Advisor, 2026-08-16)

Task 1 measured, with the null computed and written to disk before the real measurement ran:

| threshold | real | null (pixelwise / clean) |
|---|---|---|
| clean median 2.333 px | **45.97%** | 100.00% / 100.00% |
| clean mean 5.976 px | **19.01%** | 99.85% / 92.98% |
| clean p90 18.180 px | **0.89%** | 2.16% / 0.00% |

Owner is already the best-available view **47.53%** of the time. All three of the seat's
predictions missed **in the same direction — measured is worse than every version of chance it
modelled** — and were disclosed rather than reconciled after the fact.

**A weight term can only reallocate among the views that exist.** These numbers say a defect
texel's *entire* available view set sits near the boundary, not just its owner's. There is
nothing for a border mask to reallocate *to*. Building it would be building against a ceiling of
45.97% at the loosest bar, on a mechanism whose premise — that a clean view exists and loses —
is false about half the time by the owner statistic alone. **Task 2 is withdrawn, not deferred.**

**⚠ And the obvious re-route is also wrong, so it is blocked here before anyone takes it.** The
seat flagged this arc as evidence for handing the defect to camera geometry. That reading does not
survive its own mechanism: **if a texel sits at a real 3D material transition, no camera angle
puts it far from a boundary — the boundary is on the surface, and moving a camera does not move a
garment seam.** More cameras or better-placed cameras inherit the same problem. E42 remains worth
running for the coverage question it was commissioned for; it is **not** the heir to this one.

**What the two measurements say together, as a hypothesis and not a finding.** Footprint
**0.380 px** means each atlas texel covers less than one twin pixel — we are **magnifying** the
twin, not minifying it. Border distance **0.439 px** means samples sit sub-pixel from transitions.
Together these read as: **the twin does not have enough pixels to define a material boundary at
the granularity the atlas is asking for.** A 752 px generation frame is being interrogated at
4096 atlas resolution. If that is right, the lever is **source resolution**, and neither
weighting nor camera placement touches it.

**This is the advisor constructing a satisfying mechanism from partial evidence, which is this
seat's recorded failure mode. It is a hypothesis with a free test, below.**

## Task 3 — bound the resolution hypothesis by rescaling, before anyone generates anything

Nearly free: it re-reads a distribution already on disk. **Do not generate, do not re-render.**

Border distance in *pixels* scales linearly with source resolution, while bilinear's support stays
2×2 pixels. So a twin at 2× resolution puts the same 3D sample point twice as far from the same
boundary, in the units that decide whether the 2×2 support straddles it.

Rescale the measured defect-texel border-distance distribution by 2×, 3×, 4× and report, at each:
the fraction of defect texels whose sample would then sit **beyond 1 px** from the nearest
boundary — i.e. outside the straddle — and beyond 2 px.

Then state the honest cost: **which of those factors correspond to generator-legal frames.** W3's
frame is 752; E04 Ruling 15 requires ÷8 and prefers ÷16, and a width not divisible by 8 decodes
short and breaks every downstream pairing.

⚠ **Two limits to state rather than smooth over.** (1) This rescale assumes the boundary stays
equally sharp at higher resolution — a diffusion model given a larger frame may paint a
proportionally softer transition, in which case the gain is smaller than the arithmetic says, and
**this measurement cannot see that.** (2) It says nothing about whether higher-resolution twins
are *correct* — only about straddling. Report both as named limitations.

If the rescale shows the straddle persists even at 4×, **the resolution hypothesis is dead too**
and that is a full result — it would mean these texels are near a boundary at any resolution,
which is a statement about the geometry rather than about any stage we control.

## ⚖ RULING on Task 3 — partial, bounded, and NOT yet a licence to spend (Advisor, 2026-08-16)

| scale | frame | beyond 1 px | beyond 2 px |
|---|---|---|---|
| 1× | 752 | 39.12% | 25.16% |
| 2× | 1504 | **50.26%** | 39.12% |
| 3× | 2256 | 54.07% | 46.68% |
| 4× | 3008 | 56.03% | 50.26% |

Gains **+11.14 / +3.81 / +1.96**. Two-thirds of the 1×→4× move is the first doubling, and
**43.97% still straddles at 4×**. 752 is 47×16, so every scale is generator-legal at the
*preferred* bar and legality does not discriminate among them. The seat declined to force this
into confirmed-or-killed and reported the curve's shape as the finding. That is right: **only 2×
is worth anything, and the tail is not reachable by resolution.**

**The rescale is an UPPER bound on 2×, not an estimate.** It assumes the boundary stays equally
sharp; a diffusion model given a 1504 px frame may paint a proportionally softer transition, or may
paint *new* micro-structure and thereby *more* boundaries. The measurement cannot see either.

## ⛔ THE STEP NOBODY HAS TAKEN, and it gates the spend

**Every measurement in E41 and E43 is CORRELATIONAL.** Defect texels sit 5.3× closer to material
boundaries than clean ones. **Nothing has shown that removing the straddle removes the wrong
colour.** The seat's own competing explanation stands unrefuted: the boundary may be an
exactly-correct garment seam, with the wrong colour arriving from somewhere else entirely.

Spending generation credits on 2× twins would be spending on an unproven causal link, and this
repo's recorded failure is *treating a countable proxy as the question*. **Test the causal step
first. It is free.**

## Task 4 — is the defect a BLEND or a SUBSTITUTION?

Bilinear with 2×2 support cannot invent a colour. If a sample straddles a green/gold boundary it
returns a **mixture** whose fraction is set by the sub-pixel position. It can only return *pure*
gold if its entire 2×2 support already sits inside gold — and if it does, the texel's true position
is inside the gold region, which is not an error at all.

**So purity discriminates the mechanism, and the two hypotheses predict opposite distributions.**

Measure the **owner view's raw bilinear sample** at each defect texel — not the final atlas colour.
E41 Task 2 established that high-frequency content comes from the owner view alone
(impulse survival 99.94% vs 0.062%, asymmetry 1607×), so the raw sample is the thing straddle would
corrupt, and using it isolates the mechanism from everything downstream.

For each defect texel, place its sampled colour on the line between the locally-correct material
colour and the contaminating material colour, and report the **distribution of that mixing
fraction**, as a histogram rather than a summary statistic — this repo read two distant medians as
a bimodality that did not exist, and the density between them is the thing that decides.

**Pre-register all three outcomes before looking:**

- **Mass spread across intermediate fractions** → consistent with straddle. Resolution is the right
  lever and 2× is worth testing for real.
- **Mass piled at the contaminant end (say >0.9 pure)** → **straddle is NOT the mechanism.** The
  sample is landing fully inside the wrong material, which means the wrong material is *there* in
  the twin, and no amount of resolution or filtering helps. The lever moves upstream to generation.
- **Broadly flat or bimodal-with-both-ends** → two populations; split them and report each, do not
  average them into one verdict.

⚠ **The Director's own words are evidence here and they lean one way:** he called it *"gold
spatter"*, and the contact sheet shows discrete gold flecks rather than soft green-gold gradients.
**That is my reading of an image, not a measurement, and I may be wrong — measure it and tell me
which it is.** If the histogram contradicts the visual impression, the histogram wins.

Free, uses data already on disk, and it decides whether resolution is a lever at all before a
single credit is spent.

## Task 2 — WITHDRAWN by the ruling above. Retained for the record, not to be run.

Only if Task 1's ceiling is high enough to be worth building against. **Report Task 1 and stop.**
I will rule on whether Task 2 runs, and what its arm looks like.

If it runs, its known hazards, recorded now so they are not discovered later:
- **A global constant must not govern a local feature.** Three instances in this repo, each cost a
  session. Any falloff scale must be derived per structure or bounded as a fraction of that
  structure's own width, and the arm must report per structure how much weight it removed.
- **The starvation failure mode**: if all views are contaminated at a texel, a product-combined
  border mask drives total weight toward zero and the texel falls through to fill. Fill is the
  thing we are trying not to rely on. This needs a pre-registered floor and a gate.
- **The boundary detector is not the boundary.** Your dE=10 threshold reuses this repo's `--bg-de`
  convention and, as you flagged, likely also catches shading gradient. That is tolerable for a
  defect-vs-clean comparison using the identical threshold both ways; it is **not** obviously
  tolerable as an input to a shipped weight.

## Predictions

Blind predictions with bands, before you look, as always — and this time with a specific
instruction, because your Task 3 border-distance prediction missed dramatically and **that miss
was the most informative thing in the arc**:

**Predict the max-over-views distribution from the mechanism, not from the owner-view result you
already have.** The owner-view median was 0.439 px. The max over eight views is a different
statistic over a different population of samples, and an order statistic over eight draws sits
well above any single draw even when nothing is different about the underlying distribution.
**State what max-over-8 would look like under the null that views are exchangeable**, and predict
against that null rather than against zero. Otherwise a large max is uninformative — it is what
you would get from eight draws of anything.

That null is the whole discriminator in this task. Compute it first.

## Out of scope

- Any change to shipped code. This arc measures.
- Generation, re-render, re-bake. Zero credits.
- Camera geometry — E42 owns it and is running.
- ⚠ **Do not touch `tools/diagnostics/e08_ceiling.py` or `tools/measure_mcp.py`** — the E42 seat is
  editing both right now.
- ⚠ **Count surfaces stay reserved** — the eight READMEs, `SHIP_GATE.md`, `site/src/site-config.ts`.
  Report a net test delta with file paths; I reconcile.
- ⚠ **Do not open the Browser pane.**

## Working rules

Unchanged from E41 and you have followed them well: no judgement of quality; a negative is a full
success; halt at gates with evidence; `handoff.md` current; no child agent for your own
measurement; leave work uncommitted and tell me what changed.

**One note on your E41 report, as calibration rather than correction:** disclosing three prediction
misses plainly, including the head-band anchor miss you could have quietly dropped, is the reason
this arc's result is usable. Keep doing that.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Same seat, same calibrated instrument, same threshold and same populations as E41 — the continuation *is* the pin; a fresh seat would have rebuilt both and lost comparability. |
| ANDON_AUTHORITY | 3 | Task 2 is hard-gated on a check-back rather than on the seat's own judgement; halt-at-gates carries over; the starvation failure mode is pre-registered before the arm that would cause it exists. |
| NAMED_COMPENSATORS | 3 | **No irreversible call in scope** — measurement only, zero generation. Compensator for any code edit: `git checkout -- <path>`, owner = advisor, post-rollback state = HEAD. |
| DECOMPOSE_BY_SECRETS | 3 | Explicitly fenced off both files the concurrent E42 seat is editing, and off the reserved count surfaces; camera geometry and sample contamination are separate secrets in separate seats. |
| UNCERTAINTY_GATED_HUMANS | 3 | The check-back gates on the ceiling's value, not on a step count; the arc is framed contrastively against the advisor's dead candidate; the threshold instruction explicitly refuses to invent a cut. |
| EXTERNAL_VERIFIER | 2 | The seat killed the advisor's candidate in E41, which is the verifier relationship working — but it verifies its own ceiling number and no third party re-runs it. Remediation if the ceiling is high and Task 2 is authorised: a second seat re-measures the ceiling independently before any weight change is designed. Owner = advisor, before Task 2. |
