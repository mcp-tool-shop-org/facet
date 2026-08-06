# E12 handoff 5 — blind predictions

**Written BEFORE the first measurement of this dispatch**: before any crop into the mouth,
before any raycast census, before the view-5 re-roll is submitted, before the companion frame
is derived, before any clay render at head scale exists. Committed first so nothing here can
be edited against a result.

## Blind status — disclosed precisely, because this seat is NOT fresh

This is the holding handoff-4 session. It has already looked at the re-pair. **What this seat
has already seen, and is therefore NOT blind to:**

- Both re-pair outputs at full size, `HEAD_view1_3x.png`, `MEMBRANE_view5_3x.png` and the
  clay|control|styled sheet. So the *character* of the two view-5 material misses and the
  *current* definition of the face at pair scale are observed facts to this seat, not
  predictions. T2 and T3 below predict what happens **next**, from that starting point.
- Gate 0 §6's sentence — *"a tongue visible inside on 00001 and 00002"* — which by omission
  says nothing was seen on 00003. That is a **render observation by a previous seat**, not a
  geometry census, and this dispatch exists because the difference matters.
- Ruling 10f's satellite census: 7 of 8 shells unreachable from all 26 directions, 5 are the
  fangs, 3 are 4-face micro-fragments.

**What this seat has NOT done and is blind to:** any view into the mouth cavity on the mesh,
any raycast of that cavity, any head-scale clay render, any second seed on view 5, and the
companion's frame arithmetic.

## Pre-registered derivations — fixed here so they cannot be tuned afterwards

**The companion frame.** From `head_00003.json`'s `head_box_blender`, extent
**[0.1857, 0.1992, 0.1992]** (x, y, z), padded **1.12** (Gate 0's own head-crop padding),
under the route's own framing rule as `turn_render --fit-axis width` states it
(`ortho_scale = max(size.x, size.y) * margin`, `sensor_fit = HORIZONTAL`):

- horizontal extent = max(0.1857, 0.1992) × 1.12 = **0.223104**
- vertical extent needed = 0.1992 × 1.12 = **0.223104**
- → **aspect exactly 1.000** — the head box's y and z extents are equal to five decimals, so a
  square frame falls out of the route's own rule rather than being chosen.

Scale is fixed by **matching the route's standing pixel budget** (1792 × 1024 = 1,835,008 px)
so the generator stays in the regime the arc has run in: side = √1,835,008 = 1354.6, rounded
to the nearest **÷16-legal** value → **1360 × 1360** (1,849,600 px, +0.8%). Both axes ÷16,
neither is the standing 1024, per the dispatch.

**A frame-correspondence check is owed before that box is used at all**, and it is stated here
as a requirement rather than an assumption: `head_00003.json` measured the box on
`dragon_00003_raw.glb`, while every route consumer renders `E12_prep/prep_uv.glb`. If those
two are not in the same frame the box is meaningless. **Predicted: they agree** — the raw
GLB's recorded `mesh_bbox_blender` already sits in the ±0.5 normalised range, and prep is
documented as running native UVs with no decimation. **If they disagree, that is a halt and a
finding, not a transform invented mid-dispatch.**

## The works-perfectly test, stated before any of it is read

**T1 (tongue).** *Present and reachable* and *absent* are different observable states: a
raycast census of the cavity returns a non-zero count of first-hit-reachable interior
triangles in the first case and zero in the second, and a clay crop into the open jaw shows a
raised tapered body in the first and a plain floor in the second. If the two states produced
the same reading the instrument would be worthless — they do not.

**T2 (re-roll).** *Resolves* = the haunch/shoulder/hindquarter wear D1's moss-green and the
membranes wear D3's storm-grey. *Does not resolve* = either region keeps a colour from
another declared element's family. Both are visible at full size and at 3×, which is where
the E07 large-region class is judged; no statistic is armed (Ruling 10d).

**T3 (companion).** *Resolution-starved* = the face gains structure the pair's face does not
show at the same magnification — separated lids, individual muzzle scales, nostril form.
*Geometry-limited* = the face is no more defined at 100% of frame than it was at ~3%. These
are different pictures. **The one thing this test CANNOT settle is pre-registered here:** at
denoise 0.92 the model may paint plausible eye structure onto a recess that has none, so a
convincing eye on the companion does **not** prove the mesh carries one. That confound is
named now, before the artifact exists, rather than discovered in the reading.

---

## T1 — the tongue

- **T1a — there is no separate tongue SHELL.** The satellite census is closed at 8 (5 fangs,
  3 micro-fragments, Ruling 4c), so any tongue must be main-shell geometry. **Predicted TRUE**,
  and flagged as low-information: it follows from a recorded census rather than from anything
  measured here.
- **T1b — the mouth cavity carries first-hit-REACHABLE interior surface from at least one
  exterior direction.** The jaw on this mesh opens wide and forward. **Predicted TRUE.**
- **T1c — the mouth-floor geometry does NOT read as a distinct tongue** (a raised, tapered,
  separable body) on a 5× clay crop into the cavity; it reads as floor or a low ridge.
  **Predicted TRUE** — this is the informative one, and it is the prediction that makes the
  Director's "the tongue is missing" a geometry fact rather than a paint fact.
- **T1d — the branch this lands on is "present but not a tongue form"**, i.e. neither of the
  dispatch's clean *present-and-visible* / *absent* poles. **Predicted TRUE**, stated so that
  landing in the middle is a recorded expectation and not an improvised reading.

## T2 — the view-5 re-roll, seed as the only delta

- **T2a — the pale-tan region MOVES.** A new seed materially redistributes large-region colour
  assignment; the haunch/shoulder/hindquarter will not be pale-tan in the same shape.
  **Predicted TRUE.**
- **T2b — but it does not fully resolve**: moss-green will NOT cover haunch AND shoulder AND
  near hindquarter together. **Predicted TRUE** (i.e. D1's miss persists in some region).
- **T2c — the membranes do NOT resolve to storm-grey.** **Predicted TRUE** (the miss
  persists). Grounds: on view 5 the stem carries five element terms and two of them are
  `bone-ivory` (D6 spines, D7 claws) while D3 is the only grey; the register's
  `harsh directional light` pushes a large thin sheet bright; and the backdrop is itself a
  grey-family word. D3 is the weakest-anchored term in that stem.
- **T2d — headline: the two misses do NOT both resolve on a seed change alone**, so the
  dispatch's second branch fires and the finding goes up as fixture/arm evidence.
  **Predicted TRUE.**

*If T2d is falsified and both resolve, that is the better outcome for the asset and a full
success for this file being wrong.*

## T3 — the head-crop companion

- **T3a — the face reads MORE defined at bust resolution**, showing at least two of:
  separated upper/lower eyelids, individually resolved muzzle scale plates, distinct nostril
  structure. **Predicted TRUE.**
- **T3b — the eye specifically shows separated lids.** **Predicted TRUE**, *and pre-registered
  as confounded*: Ruling 4c measured the mesh's eye as a shallow lens-shaped recess with no
  separated lids at 7×, so lids appearing here are the model inventing at denoise 0.92, not
  evidence the geometry carries them. Recording both halves now.
- **T3c — D9 lands as a distinguishable tongue: predicted FALSE**, chained on T1c. Paint does
  not restore geometry the mesh does not have (the crevice precedent, designated-in at
  Ruling 1).
- **T3d — D11 reads wine-red rather than slate**, a third time, on a third
  register/control/frame combination. **Predicted TRUE.**
- **T3e — D10 fangs and tooth rows land clearly at this scale. Predicted TRUE.**
- **T3f — the full-figure subject noun (`a winged dragon,`) does NOT produce a whole-body
  composition in the bust frame.** **Predicted TRUE**, on the measured architecture: structure
  comes from the control, attributes from the prompt. This is the dispatch's named risk and it
  is predicted not to fire.
- **T3g — D3 membranes ARE in the crop.** Gate 0 recorded wing membrane passing behind the
  skull on 00003, so the term is predicted KEPT in the companion stem rather than dropped.
  **Predicted TRUE** — verified against the actual clay render before the stem is written,
  per the dispatch.

## What this dispatch does not do

No fixture edit, no profile write (advisor's), no third roll of anything, no gate or bound
invented mid-dispatch, no structure metric armed (Ruling 10d), and nothing compared against
the rejected first pair as a baseline. Task 3 of handoff 4 (bands + D8 closure) stays
acceptance-gated behind the Director's eye.
