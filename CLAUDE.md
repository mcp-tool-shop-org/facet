# Working in this repo

This file is about **how to work here**. What is *true* here lives in
[README.md](README.md) (the measured state of every tool) and
[docs/experiments](docs/experiments/) (the evidence trail). Read those for facts; read
this for method.

---

## Why this discipline exists

An earlier arc of this project ran ten sessions in which each session judged its own
output, wrote its conclusions to a shared memory store, and the next session read those
conclusions as established fact. Nothing in the loop was checkable and nothing was gated on
the Director's eye, so errors compounded silently for weeks.

The rules below are not process decorum. Each one was paid for. In the single session that
produced this repo, **six inherited or asserted claims were falsified** — the clay
provenance, the shell count, the facial ceiling, an archived resolution observation, a
coverage baseline, and a pass condition — and every one of them took minutes to overturn
*because it sat next to runnable code*.

---

## The three roles

| role | does | must not |
|---|---|---|
| **Director** (Mike) | sets direction; judges every artifact by eye | — |
| **Advisor** | writes specs, rules on reports, folds findings into the repo | execute, or grade its own rulings |
| **Executor** | runs the spec, measures, reports evidence | decide what results *mean*, or judge quality |

The separation is the point: the session that designs an experiment does not grade its
results, and the session that runs it does not decide their meaning.

## Rules for an executor session

1. **Never judge whether output is good.** Produce measurements and comparison sheets. The
   Director judges. The words *verified, shipped, works, decisive, validated, proven* do not
   belong in a report, a commit message, or a doc.
2. **State a prediction before you look**, and disclose whether it was blind. A hypothesis
   with no prediction cannot be wrong, and one that cannot be wrong teaches nothing.
3. **Stop at every gate. Never improvise past one.** A session that changed a parameter and
   re-ran when a gate fired hit the same gate harder. If a gate fires, report it with its
   evidence and halt.
4. **Do not write to the memory store.** The advisor folds findings into the repo after the
   Director has seen them. The repo is the record.
5. **A negative result is a full success.** Say so plainly and stop, rather than tuning
   toward a number.

## Rules for an advisor session

1. **Rule when the evidence is in; do not predict when it is not.** Deciding is the job.
   Guessing is not — check the advisor's own record below.
2. **Correct in place, with the measurement that overturned the claim.** Never quietly
   delete a wrong statement; the correction is more useful than the original.
3. **Pick a pass-condition unit the experiment cannot move.** Four conditions in this repo
   were mis-specified: two ratios whose denominators moved, then an absolute that broke
   because the experiment *halved the denominator on purpose* — painting 907,825 of 1.7M
   holes read as a "miss" against 923,466 of 3.5M. Ask what the intervention is designed to
   change, then measure something orthogonal to it. Here the honest unit was **dilated texel
   count** (2,551,893 → 813,773, a 68% fall), which cannot be gamed from either side.

   The fourth was a different mistake and is worth its own line: **never define a pass
   condition as a fraction of a quantity you have not measured yet.** E07 asked a ratio to
   "close half the distance from its baseline to 1.0". At the predicted baseline of 1.5 that
   is a trivial move; at the measured 5.5 it demands a 41% cut. The bar's difficulty scaled
   with how bad the problem turned out to be, which is backwards. When no calibrated threshold
   exists, **suspend rather than invent one** — `project_twins`' `assert seen.mean() > 0.30`
   is the precedent — report the numerator and denominator separately, and let the Director's
   eye rule. Retuning a condition after seeing the result is the one move that is always wrong.
4. **Own errors in the commit message.** They are how the next session learns which parts of
   the record to distrust.
5. **Do not end a session the Director has not ended.**

## Rules for everyone

**An inherited claim is a hypothesis wearing a fact's clothes.** Checking one costs minutes;
building on one costs a session. If a spec, README or handoff asserts a number, verify it
before designing around it — including numbers written by the advisor.

**When you fix a root cause, find its other consumers.** E01 established that a Workbench clay
render is flat grey on flat grey, so a threshold cannot find the figure in it — and fixed the
*control-image* path by compositing onto contrast first. The **same function on the same
render** still keys the figure mask, and it was silently losing a quarter of the silhouette:
146,356 px of true surface against 111,602 used, the loss *interior* rather than at the rim —
a stripe down the whole blade, patches through pauldrons, chest and greaves. A root cause has
as many sites as it has callers. Grep for them when you fix one.

**A number that reproduces exactly can still be measured against the wrong object.**
`project_twins` justified eroding the twin's mask with "the twin is painted fatter than the
mesh — 15.8% against 9.9%." Both figures reproduce to the digit. 15.81% is the *eroded twin*
and 9.94% is the *broken keyed mask*; against the true silhouette it is 17.43% against 19.01%,
and **the mesh is fatter**. Reproducibility is not validity. Check what the operands are, not
just whether the arithmetic replays.

**A global constant must not govern a local feature.** Three instances now, and each cost a
session: a blade rectangle measured on one character's silhouette and applied to a mesh 38%
narrower; an erosion tuned on a wide figure that ate 480k texels where the surface turns
edge-on; and an edge-distance scaled by *global figure width* that leaves a ~15 px blade with
no interior after 3.8 px is taken from each side. The cost of a fixed peel runs inversely with
local feature width. Derive the quantity per structure, or bound it as a fraction of that
structure's own width — and gate it by reporting, per structure, how much of its area the
operation removed.

**Grade an arm only on what it can move.** A stage-1 arm cannot be graded on reference
agreement: recovered texels carry the reference's own colour, so the comparison returns ~0
however the change went. An advisor asked for exactly that and an executor refused it, which
was right. Before adopting a metric for an arm, ask what value it takes when the arm does
nothing and when it works perfectly — if those are the same number, it is not measuring the arm.

**When you widen an acceptance mask, test that you did not admit background.** The check is
cheap and it is now standard here: compare the newly-admitted texels against the source's own
background colour. A2 admitted 257,506 texels at median ΔE 38.31 from background with 0.18%
within ΔE 10 — cleaner than the set already trusted. That is what makes a widening adoptable
rather than merely larger.

**Distant medians do not imply a gap between them.** An advisor read two summary statistics —
region medians around 25 against a contaminated set's median of 4.9 — as evidence of a
separable distribution, and specified a threshold "derived from the measured bimodality."
Measured, the density rises monotonically from ~5 to 30 with **no antimode at all**, and the
two views disagree about where a dip even is. Two populations with different medians overlap
continuously unless you have looked at the density between them. Plot it before you claim a cut
exists.

**A threshold method reports its own confidence in the wrong partition.** Otsu returned
η = 0.661 — a healthy-looking score — while cutting dark paint from light paint and rejecting
41,194 px at a median depth of 8 px, deep in the figure's interior. The class we cared about
was 0.5% of the data, and between-class variance finds the *dominant* split, not the one you
want. When the target class is a small minority, a global thresholding method will confidently
answer a different question.

**A guard whose stated reason is wrong may still be load-bearing for a reason nobody wrote
down.** The edge erosion justified itself with a comparison measured against the wrong objects
— and was simultaneously removing background-contaminated tendrils from the twin's mask, which
nothing in the repo had noticed and no comment mentioned. Voiding a justification is not
grounds for deleting a guard; it is grounds for **measuring what the guard actually removes**.
Take it out in a run you are prepared to throw away, and look at what comes back.

**Test the property, not a geometric proxy for it.** The question was *is this pixel
background-contaminated*. The pipeline asked *is this pixel near a boundary*, which is a proxy
that fails precisely where the subject is thin — a 1–2 px structure is entirely boundary, so
half-width turns out to measure what fraction of a structure is edge rather than how thin it
is. Contamination concentrated 200× in the thinnest strata while being 0.5% of the mask
overall, invisible in aggregate for four experiments. When the property is directly
measurable, measure it; a proxy inherits every failure mode of the thing it stands in for and
adds its own.

**Put the andon on the direction the invariant does not bound.** When a change introduces an
invariant, that invariant forecloses one failure direction *by construction* — so a halt aimed
there fires on correct work while the live risk goes unwatched. A3 bounded over-erosion with
`e ≤ ⅓ × local half-width` and was then gated on how much area the erosion removed: the
invariant held exactly, zero violations, and the gate halted the build anyway. The unwatched
direction was the opposite one — a looser mask admitting background at the reference's painted
boundary — and the instrument for it already existed. Ask which way the change can still go
wrong *after* the invariant, and gate that.

**A diagnostic and a gate are different objects.** The same measurement can be the best
evidence you have and an unusable halt. Stratum area-loss proved the shipped erosion was
annihilating thin structure — 100% / 100% / 77.6% of the three thinnest strata, by a guard
built to delete a 1–2 px rim — and it is required in every report of that arm. It cannot gate:
it is a perimeter-to-area statistic that swings ±10 points on shape alone and is not bounded
by the invariant it was meant to protect. Before promoting a number to a halt, ask what else
moves it besides the thing you are watching.

**A check that cannot fail is not a check.** An executor tested the erosion hypothesis by
comparing the saved mask against its own dilation — an operation that cannot lose a pixel — and
got 0.00%. It was reported as *untested* rather than as confirmation, which is exactly right,
and it is the same family as the silhouette-IoU gate that returned 1.00000 on a holed mesh.
Before trusting a 0, ask what a non-zero would have required.

**When a number will not move, check the baseline.** The most valuable measurement in this
repo's history came from an executor who stopped chasing a stuck figure and asked whether
the thing it was compared against was real. It was not.

**Bound an expensive arm before spending it.** Compute the ceiling first. One executor
priced a six-stroke experiment at +1.7 points before running it, and skipped it.

**Validate a metric against a rejected artifact before building an experiment on it.** Take
something the Director has already turned down, and the region he named, and confirm the
number fires there. E07 graded four arms with blotch counts, speckle, a step ratio and a
flattening guard — **four of the five are 5×5 high-pass statistics, and the fifth is
indifferent to where a colour lands.** The defect that decides acceptance is a *large region
of the wrong material*: a steel blade wearing skin, a boot wearing gold. Such a region is
smooth inside itself and contributes only its rim to every one of those numbers. So an arm
took source distance down 70×, mean fallback to zero and speckle below A0 — and the asset was
unchanged to the eye. A metric that cannot separate an asset he rejected from one he accepted
is not a metric. This cost four experiments; every gate error below cost one.

**A gate must test the operation's failure mode, not its success mode.** A cull was gated on
silhouette IoU — which is structurally blind to holes punched through *visible* surface,
because the ray behind a removed face still hits geometry. IoU returned 1.00000 on a mesh
with a hole clean through it. The executor noticed the gate could not see its own failure,
added a first-hit depth comparison, and it fired immediately. **Ask what the operation would
look like if it went wrong, then check for that.**

**And gate on the failure itself, not on a proxy for it.** The second version of that error is
subtler and cost a halt in E07. A surface-aware lookup fails by *sourcing colour from
somewhere else on the figure*; the gate was written on **normal disagreement**, a stand-in for
it. The stand-in inverted — the back-facing sources were the *closest* ones, 0.77 triangle
edges away, opposing faces of a sheet thinner than its own tessellation — while **no** lookup
reached beyond 20 edges, against 72.2% for the flood it replaced. A proxy fires on whatever
correlates with it, including the subject's own geometry. If the quantity you care about is
measurable, gate on that quantity and leave the proxy as a reported diagnostic. Then check
what the threshold's unit is pinned to: E07's replacement is stated in *triangle edges*, and
`texpass_finalize.py` had that edge length hardcoded from one mesh.

**Prefer eliminating a risk to gating it.** When the same cull was changed from *deleting*
faces to *excluding them from the atlas*, the failure became impossible rather than
detectable — geometry is never modified, so the silhouette cannot change and a future camera
sees flat grey instead of a hole. A guarantee that depends on nobody adding a camera is not a
guarantee.

**Failures stay in the repo, next to the code, with the reason.** `tools/superseded/` is not
an archive; it is the mechanism that stops a falsified approach quietly becoming doctrine
again. Anyone can run those tools and watch them fail the same way.

## Judging artifacts

- **Textures under FLAT light.** A Blender Workbench STUDIO render is not a texture readout —
  grey chalky facet mosaics are specular highlights on flat-shaded normals and vanish under
  `--flat`. Two debugging rounds were lost to this.
- **Geometry under `--clay`.** Texture hides geometry; that confusion caused a whole session
  of misdirected work.
- **At the Director's zoom, not from a contact sheet.** Defects that decide acceptance are
  invisible at thumbnail scale.
- **Beside the reference, with provenance.** The cheapest diagnostic in this repo is
  *reference | asset | provenance | error* on one sheet, and it did not exist until E08's
  Gate 0. E07 ran four arms and two gates without once putting the asset next to the thing it
  is supposed to look like. When the sheet was finally built, the Director read the whole
  thesis off panel 2 in a sentence — the blade is flesh where the reference is steel, and the
  provenance panel shows it carries no reference at all. **Build that sheet before the
  metrics, not after them.** A number tells you a region is wrong; the sheet tells you what it
  was supposed to be, which is the part that decides what to do next.

## Experiments

Every non-trivial change runs as a numbered experiment in `docs/experiments/`:

```
spec written BEFORE the work  →  report written AFTER  →  advisor ruling LAST
```

A spec carries: the question, hypotheses with predictions, arms varying one thing each,
the metrics, the gates, an explicit out-of-scope section, and a standards-compliance block
scoring the six workflow standards. Amendments are appended in place with dates and reasons
— a spec that hides its own corrections is the thing we are trying to get away from.

## Environment

This is the Robot rig — **drives C and E only. No D:, no F:.** Any `F:/AI/...` path in an
inherited document means `E:/AI/...`.

```
python    E:\AI-Models\trellis2-env\Scripts\python.exe
blender   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
assets    E:\AI\training\facet_E0*\  and  E:\AI\training\saltroad_bake_fix\
```

**Run all Blender work through PowerShell** — Git Bash mangles the paths and every call
fails with `Error: Please select a file`.

**Launch ComfyUI capped:** `--reserve-vram 8.0 --disable-smart-memory`. A bare launch peaks
at the VRAM watchdog's kill ceiling and gets terminated mid-run. This has happened twice.
Cap the consumer; never raise the ceiling.

**argparse eats leading minus signs** — use `--views=-30,0,30`.

**Scripts must create their own output directories.** Two runs died on this.

## Standing technical constraints

These are physics and measured traps, not settings. They are subject-independent and stay in
code rather than in a profile — see [docs/profiles-design.md](docs/profiles-design.md) for
the boundary.

- **Weld before decimating.** An exported glTF splits a vertex at every UV seam; collapse
  decimation on the result tears holes because per-triangle shells have no neighbours.
- **No volumetric predicate on an exported mesh.** It is not a solid — signed distance at the
  centre of a standing figure's chest reads *outside*. Containment, thickness and
  inside/outside must run on the welded mesh, before export.
- **A ray along the surface normal measures the tessellation, not the geometry.**
- **Twins belong to a mesh, not to a character.** Regenerate them for whatever you are about
  to texture.
- **Build the control image; Canny cannot find a silhouette that is not there.**
- **One mask cannot answer two questions** — the mesh silhouette answers *is there surface*,
  the twin's own mask answers *is the paint trustworthy*.
- **Order strokes to spiral outward from already-painted regions**, or the brush composes a
  new character instead of continuing one.

## The advisor's record, for calibration

Kept because a future advisor should know which parts of this repo to distrust. In the
founding session the advisor was wrong about: the shell-soup premise, the clay provenance,
the double-subscribe diagnosis, `--no-head-scale`, the head-pixel multiplier, the halo
hypothesis, `angle_limit` as a lever, deferring the blade fix, and two pass conditions.

In E07 the advisor was wrong about two of its own gates, both written into the spec: the
back-facing ANDON, which measured a proxy that inverted on this mesh and halted a correct
arm, and a pass condition defined as a fraction of a baseline nobody had measured. Both were
caught by an executor who ran them as written and reported the evidence rather than tuning
past them. The spec's step ratio and its Gate 0 premise tests held up.

The advisor was useful at: ruling once evidence was in, killing options with reasons,
refusing to commission a metric where no honest one existed, bounding an expensive arm before
spending it, and correcting the record in place.

**Deciding is the job. Predicting is not.**
