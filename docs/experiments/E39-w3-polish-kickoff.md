# E39 — W3's polish: which provenance class carries the wrong-material regions?

**Status: RUNNING.** Opened 2026-08-16 by the advisor, at the Director's live redirect.
This document is the dispatch. Under the dispatched-seat standard (CLAUDE.md, "How an
experiment is run") the advisor spawns the executor and steers it on an open line; the
dispatch IS the spec and lands here so it can be read afterwards. Amendments are appended
in place with dates.

---

## Why this arc exists

**The Director, 2026-08-16, in his words:** *"let's not over focus on the black artifacts.
W3 is far from perfect and needs a serious polish."* And on method: *"do a study-swarm
instead of guessing."*

E38 spent an arc on a class that measures **0.578% of W3's figure pixels and renders zero
black there**. Walk `E:\AI\training\facet_E08\ARMB\out\renders_flat\final_0.png` at native
size and the actual defect is unmistakable and everywhere:

- **gold** blobs and streaks across the green tunic, the skirt, the boot tops
- **gold and rust-brown** patches over the steel blade — the largest single offence
- **green** down the sword grip, which is not cloth
- **brown-green** smears across the hands and the right bracer

Every one of these is *a region wearing another material's colour*. Not speckle. Not noise.
Not black. The advisor has walked all of it at native size at this seat.

## The question, and why answering it decides the road

**Which provenance class carries those regions?**

W3's finished atlas is built from three sources, and the export tree records which one won
every texel (`class_palette`, `tools/e11_manifest.py:95-96`):

| class | rgb | what it means |
|---|---|---|
| `reference` | (60, 200, 110) green | projected from the eight diffusion twins |
| `brush` | (70, 170, 255) blue | painted by the texture-space stroke loop |
| `dilation` | (235, 120, 40) orange | filled by `texpass_finalize.py`'s atlas-space flood |

Two roads follow, and they are not close in cost:

**Road A — `dilation` carries them.** Then this is cross-island bleed, the mechanism
`docs/known-defects.md` already records at **74.9% of 813,773 dilated texels taking colour
from another island**, and the fix is small, local and ours: `texpass_finalize.py:155`'s
predicate is `fill = ~grown & (cnt > 0)` with **no island constraint at all**. The record
tested adding `& valid` and found it insufficient — but **`valid` is not `same island`**, and
constraining the flood to the source texel's own island has never been tested here. It is
what every DCC tool ships as a toggle.

**Road B — `reference` carries them.** Then the twins disagree with each other about
*material identity* — one view paints gold where another paints cloth — and no atlas-space
blend repairs that, because there is no correct answer to average toward. The study-swarm's
two independent agents converged on exactly this: classical multi-view texturing assumes N
photographs of one physically consistent object disagreeing **photometrically**; ours are
independently sampled and disagree **semantically**. The literature's answer is to
synchronise views during denoising (SyncMVD, [arXiv:2311.12891](https://arxiv.org/abs/2311.12891),
**MIT — LICENSE fetched and read directly, not inferred**) rather than to blend better
afterwards.

**Nothing is adopted in this arc.** This arc measures which road we are on. That is all.

## ⚠ The inherited claim this arc exists to test — and it is the advisor's own

The handoff into this seat asserts the mechanism is cross-island bleed. **Treat that as a
candidate and kill it as hard as your own.** Three reasons it may be wrong, all from this
repo's own record:

1. **The enrichment figure behind it cannot see this defect.** `docs/known-defects.md`
   states dilation texels are *"4.8× enriched in visible blotches against a 5% base."* That
   number comes from E07 Gate 0's blotch measure — and CLAUDE.md's own law says of that
   family: *"four of the five are 5×5 high-pass statistics… The defect that decides
   acceptance is a large region of the wrong material… Such a region is smooth inside itself
   and contributes only its rim to every one of those numbers."* A speckle detector is
   **structurally blind** to a gold blob on a green tunic. The 4.8× is evidence about
   speckle, not about what the Director named.
2. **E07 Gate 0 also measured `TWINS | DILATION` boundaries as the FLATTEST class** — 1.750,
   against 4.75–11.75 for brush-vs-twin — with the stated reason that *"dilation blends from
   its neighbour by construction."* That is the opposite of a source of hard-edged
   wrong-material blobs.
3. Read off `prov_0.png` at whole-figure scale, the figure is overwhelmingly green, with
   orange confined to thin rims and part of the blade. **That is a downscaled visual
   impression by the advisor and is NOT a measurement** — it is named here as the advisor's
   prior so you can falsify it, which is its only job.

## What you have — enumerate before commissioning anything

Everything needed is already on disk. **Nothing needs to be generated or re-baked.**

```
E:\AI\training\facet_E08\ARMB\export\turnaround\
  views\<26 view dirs>\
      asset.png                     <- the flat render at that camera
      prov_class_<view>.png          <- EXACT per-pixel class, born indexed, NO antialiasing
      silhouette.png                 <- the figure mask
      cam.json, admission_*.json
  provenance_atlas_indexed.png      <- texture-space class map
  styled_mask.npy                   <- styled/unstyled coverage before the finalize flood
  atlas.png, mesh.glb, asset-source.json
  pair_twin_y+{000..315}_e+00.png   <- the eight twins, for the Road-B follow-on
```

`prov_class` is the channel to use — the manifest says so itself: *"EXACT per-pixel class by
texel-id raycast — born indexed, no antialiasing, PLTE == this palette."* `prov.png` is the
antialiased display form; do not measure on it.

**⚠ This tree is an ACCEPTED ASSET and is manifest-protected. READ ONLY.** Write every
output to `E:\AI\training\facet_E39\`. Confirm at the end that you wrote nothing under
`facet_E08` — a directory listing with mtimes is sufficient evidence.

**W3 cannot be re-baked.** No `prep_uv.glb` / `mask.npy` / `pos.npy` / `meta.json` survives
anywhere under `facet_E08` — verified three times now, including at this seat. Do not plan
around re-running `bake_hero_prep` or `texpass_finalize` on W3. This arc is measurement on
the finished artifact.

---

## Task 1 — the detector, and the gate that proves it is one

**Do not use a speckle or high-pass statistic.** The law above rules them out. The defect is
a *region*.

Build a wrong-material-region detector: for each figure pixel, the colour distance (CIE ΔE,
not RGB) from the median colour of a large window around it; a region is a connected
component above a distance threshold **and** above an area floor that excludes speckle.
State the window size, the threshold and the area floor in the report, and report the whole
result at **three** thresholds so a reader can see whether the ranking moves with the knob.

### GATE 0 — validate the detector against what the Director named, before any number

CLAUDE.md: *"Validate a metric against a rejected artifact before building an experiment on
it. Take something the Director has already turned down, and the region he named, and
confirm the number fires there."*

Produce a sheet at **native pixel size** — render beside detector overlay — for view
`y+000_e+00` and at least two others, and confirm by eye that the detector fires on:

- gold on the green tunic · gold on the skirt · gold on the boot tops
- gold and rust on the steel blade
- green on the sword grip
- brown-green on the hands / right bracer

**If the detector does not fire on the regions the Director named, the detector is wrong and
you HALT and report that.** Do not tune it toward a number after seeing class shares. Tuning
it to fire on the named regions is the point of this gate and must happen *before* any
provenance number is computed; write down the parameters you settled on, then stop touching
them.

### The measurement

1. **Base rate.** Class composition of all figure pixels, per view and pooled over all 26
   views. This is threshold-free and it can settle the question by arithmetic alone: if
   `dilation` is a few percent of the figure, it cannot carry regions that cover a large
   share of the tunic.
2. **Detected-region composition.** Class composition of pixels inside detected regions,
   per view and pooled.
3. **Enrichment per class** = (2) / (1). Report all three classes. Report the ranking at all
   three thresholds.
4. **By region, not only by pixel.** For each of the largest 20 detected regions: its area,
   its dominant class, that class's share within it, and where it is on the figure. A single
   class holding 90% of one large region is a different finding from three classes each
   holding a third of it, and the pooled pixel number cannot tell them apart.

### Predictions — write them BEFORE you look, to `E:\AI\training\facet_E39\predictions.md`

State, with numeric bands and your confidence, and say plainly whether each is blind:

- P1 — `dilation` share of figure pixels, pooled
- P2 — `reference` share of figure pixels, pooled
- P3 — enrichment of `dilation` inside detected regions
- P4 — enrichment of `reference` inside detected regions
- P5 — the dominant class of the single largest detected region
- P6 — whether the ranking in P3/P4 survives all three thresholds

**Read the unit before you predict.** This repo has missed nine consecutive arcs on the
unit/population family. Ask what the denominator is made of, what a "region" is, and whether
the property you are predicting is even defined for every member — *then* write the number.

### Halt conditions

- Gate 0 fails (detector does not fire on the named regions) → **HALT**, report, do not tune.
- Any write lands under `facet_E08` → **HALT** immediately.
- The three thresholds disagree about which class is enriched → that is **not** a halt; it is
  a finding. Report it as one.

## Task 2 — conditional, and I will steer you into it on the open line

**Only if `reference` carries the regions.** Do not start it on your own judgement; report
Task 1 and I will rule.

The question becomes: **do the eight twins disagree about material at the same surface
point?** The twins are on disk (`pair_twin_y+*_e+00.png`). Enumerate what else survives that
records which view owned each texel — `asset-source.json` declares the channel list; the
manifest inserts a `view_owner` channel for subjects that have one. **Check whether W3 has
one before assuming either way.** If it does, disagreement is directly measurable; if it does
not, say so and stop rather than inventing a substitute.

## Out of scope

- Any change to `texpass_finalize.py`, `bake_hero_prep.py` or any route tool. This arc
  measures; it does not fix.
- Any re-bake, re-projection or re-generation of anything.
- Any judgement about whether W3 is acceptable. That is the Director's and only his.
- The E38 dark-mark class, Population A and Population B. Closed elsewhere; not this arc.
- SyncMVD, SAM2 or any external method. Road B's *existence* is what this arc can establish;
  adopting anything is a later decision with the Director in it.

## Rules for this seat

The executor rules in CLAUDE.md bind, and these five are the ones this arc will test:

1. **Never judge whether output is good.** Produce measurements and sheets.
2. **State a prediction before you look**, and disclose whether it was blind.
3. **Stop at every gate. Never improvise past one.**
4. **A negative result is a full success** — including "the advisor's prior was right", which
   is *weaker* evidence than you overturning it and should be reported with that asymmetry
   named.
5. **Write `handoff.md` early in `E:\AI\training\facet_E39\` and keep it current.** Two
   executor transcripts were lost inside E38's first day, one at ~500k tokens and one without
   warning. On-disk state is the record.

**Do not delegate your own core measurement to a child agent.** One E38 seat did and stalled
invisibly.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | every input is a named file at a named path on a frozen, manifest-protected tree; the detector's three parameters are written down before the measurement and not touched after |
| ANDON_AUTHORITY | 3 | Gate 0 halts on a detector that cannot see the named defect; a write under `facet_E08` halts immediately; both are stated before the work and neither can be satisfied by tuning |
| NAMED_COMPENSATORS | n/a — **skip justified** | this arc performs **no irreversible action**: no publish, no push, no external write, no mutation of any existing tree. Its only writes are new files under a new directory `facet_E39`, whose compensator is deleting that directory |
| DECOMPOSE_BY_SECRETS | 2 | Task 1 (attribution, always runs) is separated from Task 2 (twin disagreement, conditional) precisely because the second's *existence* depends on the first's answer |
| UNCERTAINTY_GATED_HUMANS | 2 | the advisor is on an open line and rules the Task 1 → Task 2 transition; the Director is gated in only at an artifact, per the dispatched-seat standard |
| EXTERNAL_VERIFIER | 2 | the executor is a different seat from the advisor who wrote this spec, and its explicit remit is to kill the advisor's stated prior in §"the inherited claim" as hard as its own |

## Amendments

*(appended in place, with dates and reasons)*

### Amendment 1 — Task 1 ruled, and the advisor's candidate is dead (2026-08-16)

Report: `E:\AI\training\facet_E39\task1-report.md`. **Gate 0 PASSED on two legs** — an eye leg
at native 1:1 on all seven regions the Director named, and a specification leg whose material
centres were derived from a *different object* than the one tested (recall 93–99% at ΔE>14).
Nothing was written under `facet_E08`; 818 files, `Compare-Object` clean against a baseline taken
at seat open.

**RULED: the gold class is `reference`-carried. Road B.** `dilation` is genuinely enriched —
1.76× / 1.92× / 2.22×, ranking stable across all three thresholds — and **cannot carry the
regions**: 9.52% of detected-region pixels, **4.27%** of the area of regions ≥300 px, 11 regions
against `reference`'s 369. On the tight population, **gold out of place is 91.05% `reference` at
0.99× — dead on base rate.**

**Two reasons this is accepted rather than dismissed as a boundary artifact**, since the advisor
walked the tunic, skirt and blade zooms at native size at its own seat and the detector is
visibly boundary-dominated: the executor **named that its window-41 bias runs in the direction
that favours the advisor's candidate** and the result went the other way anyway; and the
per-region dominance census does not depend on which components merged. §1 of the report states
the limitation before §6 answers the same question on the tight population. **A leg whose
weakness is declared by its own author, with the direction of the bias named, is worth more than
a leg with no declared weakness.**

**Two findings kept SEPARATE from the gold ruling rather than folded into it:**
- **Green out of place is a different mechanism** — `brush` **5.49×**, `dilation` **3.34×**,
  `reference` down to 68.46%. The same-island flood constraint may well be the right fix *for
  this class*, which is not the class the Director named first.
- **The blade is the one `dilation`-dominant large region**, at a **48.3% plurality** — not a
  majority. A mixed case, and the region he called the largest single offence.

**The unit reconciliation is the report's largest finding** and is folded to
[known-defects.md](../known-defects.md): `dilation` is **26.95% of the written atlas and 4.95% of
rendered figure pixels, 0.18×**. Every dilation figure this repo reasons from is in atlas texels
— **including the ones in this dispatch's own §"The question"** — and overstates what a camera
sees by 5.4×. Two inherited claims reproduce to the digit (68.82%, 26.95%); two do not and are
withdrawn as unattributed rather than corrected (`813,773`, `33.9% of the atlas`).

**The executor's P1/P2 missed badly** (24% → 4.95%; 66% → 92.31%) and its `predictions.md` had
**named that exact trap and then anchored on the inherited atlas number anyway**, which is the
most useful miss in the arc: the ritual saw the hazard and the number still came from the wrong
unit. P3–P6 hit, including P5's own named alternative (the blade → `dilation`) landing as
region #10.

### Amendment 2 — Task 2 redefined before it ran (2026-08-16)

**The `view_owner` route is closed, correctly.** `e11_manifest.py:93` declares
`"owner_channel": False` — *"honestly absent, never synthesized"* — and no `owner_id_*.npy`
exists in any of the 26 view directories. The seat enumerated before designing, which is the law.

**`reference`-carried is consistent with two mechanisms that need completely different fixes**,
and Task 2 as originally written did not separate them:

- **(a) the twins DISAGREE** — one view paints gold where another paints cloth, and the
  projection resolves the conflict badly. This is the study-swarm's finding, and SyncMVD is
  aimed squarely at it.
- **(b) the twins AGREE** — a twin simply painted gold on the tunic, the generator hallucinated
  it *within one view*, and the projection faithfully carried a defect that was already there.
  **No multi-view synchronisation fixes this**, because there is no cross-view conflict to
  resolve.

**Task 2's question is therefore: at gold-out-of-place surface points, do the twins agree or
disagree?** Cheapest decisive form first — establish whether `pair_twin_y+000_e+00.png` is the
same camera and framing as `views/y+000_e+00/asset.png`, because if it is, the front twin and the
final front render compare pixel-to-pixel with no reprojection at all. Check the framing rather
than assume it: this route has been bitten by a 2 px frame mismatch before (E04 Ruling 15).
The eight-view reprojection is built **only if** the cheap form does not resolve it.

**Why this matters beyond this arc:** the study-swarm's convergent recommendation assumes (a).
If the answer is (b), the swarm's headline finding is aimed at the wrong mechanism for this
asset, and adopting SyncMVD on its strength would be the same error this arc was built to
catch — one level up.

### Amendment 3 — Task 2 ruled: BOTH mechanisms are live, roughly 2:1 (2026-08-16)

Report: `E:\AI\training\facet_E39\task2-report.md`. `facet_E08` re-diffed clean at 818 files.

**The cheap form was available and the check was worth insisting on.** All eight twins are
752×1024 and register to their own export render at best shift **(0,0)**, under *two independent
objectives* (median ΔE over a 7×7-eroded silhouette; gradient-magnitude NCC), both unimodal over
|d| ≤ 8. No reprojection, no resampling, no keying was needed. The frame check was demanded
because E04 Ruling 15 cost this route a 2 px mismatch; it came back clean, which is the outcome a
cheap check is *supposed* to have most of the time.

| | exact | tolerant r=3 |
|---|---|---|
| **measure** — twin is gold at gold-out-of-place (n=17,731) | **41.29%** | **55.28%** |
| **ceiling** — twin is gold at *legitimate* gold (pauldron, n=68,855) | 63.66% | 81.14% |
| **floor** — twin is gold at ordinary green tunic (n=335,495) | 0.43% | 1.50% |
| **normalised** (measure − floor)/(ceiling − floor) | **64.6%** | **67.5%** |

**RULED: both mechanisms are live, and neither can be dismissed.**

- **(a) the twins disagree — ≥ 29.9%, a FIRM LOWER BOUND.** Where the twin rendering that pixel
  is clean, the gold demonstrably came from another view. **One view's absence is decisive about
  that view**, which is why this direction bounds firmly.
- **(b) a twin hallucinated internally — ≤ 70.1%, an UPPER BOUND AND NOT A MEASUREMENT OF (b).**
  Twin-gold at view *k* establishes that *k* is *a* source; it cannot poll the other seven. **The
  executor pre-registered that asymmetry before the number existed**, which is what keeps the
  bound honest instead of letting it read as a result.

**The control that makes the number trustworthy is the tolerance plateau**, not the point value:
normalised rises 64.6 → **70.1% by r=6 and does not move through r=10**. Registration slop is
worth ~5.5 points and no more. Median ΔE(twin, asset) reads the same gradient independently —
**22.87** at gold-out-of-place against **3.55** on ordinary green.

**⛔ A pre-registered gate FIRED and the remedy is recorded rather than smoothed.** `y+090`'s own
ceiling is **49.07%**, under the 60% floor set in advance. The remedy was to normalise **per
view** rather than pool raw; **the view was not dropped**, and the firing is reported as a firing.
Alongside it, `y+135` sits at **117.2% — above its own ceiling**, offered as an observation and
not explained. ⚑ **The lead worth chasing: `e11_manifest.py:73-75` records twin_2 and twin_6 —
`y+090` and `y+270` — as the accepted RE-ROLLS**, and `y+090` is the outlier. A re-rolled twin is
a twin that made its material decisions in a separate sampling event.

**The artifact decides it by eye** (`t2/t2_zoom_y+090_e+00.png`, twin | asset | split, 3×
NEAREST, walked at native size at the advisor's seat): the twin carries a **brown leather bracer
and a green skirt** exactly where the asset paints a **large gold hip plate**, marked red across
nearly its whole area, with pose and silhouette agreeing. **And the twin is visibly cleaner and
more materially coherent than the asset built from it** — which is a statement about where
quality is lost, and is not something any number in this arc measured.

**Consequence for the road.** SyncMVD and its family target **(a)**. (a) is **at least 29.9%** of
the gold class and **at most 70.1%** — real, bounded, and *not the whole thing*. **Adopting a
synchronisation method on the study-swarm's strength alone would have been the same error this
arc was built to catch, one level up**, and Amendment 2's caution is now a measurement instead of
a worry.

**The executor's own miss is the most instructive result in the arc.** T2-P1 predicted 75%;
the instrument's ceiling is **63.66%**, so **the prediction named a rate above the instrument's
own maximum**. In its words: *"the controls were in the design and absent from the prediction."*
This is a new member of the unit/population family and it is folded to
[CLAUDE.md](../../CLAUDE.md) as its own law.
