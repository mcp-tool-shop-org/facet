# E12 handoff 12 — blind predictions, registered before anything runs

**Executor session, 2026-08-06.** Written before the v9 rebuild, before any v9 artifact exists,
and before `e13_harmonize.py` exists.

## Blind status, disclosed exactly

**Blind to every outcome. Not blind to the v8 baselines**, which the dispatch asks these
predictions to be stated against. Two things were measured *before* this file was written and
both are disclosed rather than hidden, because both are inputs to the prediction rather than
outcomes of it:

1. **A term-level diff** of `beast.json` against the v8 prompts file on disk: exactly one
   comma-term is **substituted in place** at index 5 — `storm-grey wing membranes` →
   `leathery storm-grey wing membranes`. Term count unchanged at 20. P1a is therefore near
   certain by construction and is registered anyway.
2. **The v8 membrane baseline**, which did not exist until now — no instrument in this repo had
   ever reported what colour the membranes actually *are*. Measured on geometry-derived wing
   boxes (world box carried into the render frame by the route's own arithmetic), masked to the
   exact silhouette:

| v8 | v0 | v1 | v2 | v3 | v4 | v5 | v6 | v7 |
|---|---|---|---|---|---|---|---|---|
| median C\*, presented wing | 19.8 | 26.0 | 22.8 | 23.2 | 15.2 | 20.5 | 24.9 | 18.6 |
| median hue | 87.6 | 108.2 | 127.9 | 122.5 | 90.3 | 121.2 | 129.9 | 128.0 |
| share under C\* 12.0 | 23.9% | 2.9% | 15.5% | 11.1% | 22.6% | 26.7% | 19.3% | 27.1% |

**This is Ruling 22b's premise as a number for the first time**: storm-grey is a neutral, and
every membrane box measures chromatic (median C\* 15.2–26.0) at a warm-yellow to yellow-green
hue. View 4 is the least-warm, exactly as 22c says.

**Not yet done:** the v9 build · any v9 artifact · any submission · any line of
`e13_harmonize.py` · any harmonized output.

---

## Task 1 — the v9 stems

- **P1a — the delta is exactly one in-place substitution.** Entry stays **20 terms**;
  `storm-grey wing membranes` → `leathery storm-grey wing membranes` at index 5. The ANDON,
  asserted as construction: map the new spelling back to the old in every v9 stem and what
  remains is **byte-equal to the matching v8 stem**, on all nine. *Near-certain; registered
  because an ANDON expected to pass still has to be stated first.*
- **P1b — nothing else moves.** Drop map byte-identical; per-view counts unchanged at
  **20/20/20/14/16/14/20/20**, `headclay_0` **18**; full-string views still {0,1,2,6,7}. The
  membrane term is in neither the mouth family nor the horn family, and D3's surface is visible
  from every yaw, so no drop is added or removed.

## Task 2 — seven views regenerated (4 excluded)

- **P2a — the membranes move toward neutral, and this is the round's question.** Predicted:
  **median C\* falls by ≥ 3 points on at least 5 of the 7** regenerated views' presented-wing
  boxes, landing mostly in the **12–19** range, with the share under the chroma floor **rising**
  on at least 5. *Confidence: medium.* **The named alternative, pre-registered as a real
  possibility rather than a hedge:** `leathery` is a *surface* cue and the model may spend it on
  relief — more wrinkle and vein structure at the same warm hue — moving chroma by less than 2
  points. That outcome is a full success and it says the opacity cue does not contest the
  translucency prior either, which closes the word lever and hands the question to the
  escalation arm (reference conditioning) or to harmonization.
- **P2b — a does-nothing band, stated so the result cannot be read generously.** Any view whose
  median C\* moves by **less than 2.0 points** counts as unmoved. If the mean absolute move
  across the seven is under 2.0, P2a is falsified outright.
- **P2c — hue direction.** Where chroma does fall, I expect the median hue of the pixels still
  clearing the floor to move **little** (the ruled hue family is unchanged by 22b). Predicted:
  no view's membrane hue moves more than **25°**. A large hue swing would mean the term did
  something other than what it was written for.
- **P2d — re-rolls.** Predicted **1–3 of 7**. **View 3 is named near-certain** — 21c banks the
  deterministic flat-black limb at 770700 across two independent stem generations, so a third is
  expected and its re-roll to 770701 is pre-registered as process, not surprise. No other view
  is named; if a second or third spend happens it will be on a spec-visible miss and stated with
  its grounds.
- **P2e — regressions, because a changed prompt re-rolls every landing.** Predicted: the gate
  number moves on **all seven** (none reproduces its v8 reading); the nape charcoal holds within
  **±8 points** on views 0 and 7 (the two clean nape presenters among the regenerated); and
  whole-figure pale stays within **±30%** of each view's v8 value. Anything outside those is a
  regression I will report as one rather than absorb.
- **P2f — registration and backdrops.** Predicted IoU **0.950–0.985** on all seven, and **0 or
  1** of the seven paints a graded backdrop. If one does, the bbox/grading check catches it
  before the number is believed.
- **P2g — 0 credits.** All sixteen reused inputs return handoff 8's recorded content-hash names.

## Task 3 — the harmonization instrument

- **P3a — identity on the reference is EXACT.** View 1's v9 twin harmonized toward view 1's v9
  twin comes back **byte-identical** — 0 differing pixels, and the same sha256. Not "within
  rounding"; **zero**. This is the works-perfectly test and the instrument does not get read
  until it passes. *Confidence: high, but it is not free* — a naive implementation that
  round-trips through Lab and back to 8-bit will lose a few least-significant bits on some
  pixels, so the identity has to be arranged for, not assumed.
- **P3b — the transfer's own arithmetic is exact by construction.** After transfer, every
  view's per-channel mean and σ inside the figure mask equal the reference's to within
  **0.01**, because that is what a first-and-second-moment transfer does. This prediction
  cannot fail on a correct build and is registered as the implementation check it is, **not**
  as evidence the pass is good.
- **P3c — the size of the correction, which is the part that is not free.** Predicted: at least
  one of the seven non-reference views needs a **mean-L\* correction of ≥ 4.0** units, and the
  spread of mean L\* across the eight-view set (v9 ×7 + v8-A view 4) is **≥ 8.0** L\* units
  before harmonization. That spread is the Director's "not very consistent" as a number; if it
  turns out to be under 4.0, his observation is about something a tonal transfer cannot reach
  and I will say so.
- **P3d — what harmonization cannot do, pre-registered so its output is not over-read.** A
  first-and-second-moment transfer unifies tone; it cannot move an element into a different
  colour family. Predicted: on any view whose membranes are still warm after Task 2, the
  harmonized membranes stay warm — the membrane-box median hue moves **less than 20°** under
  harmonization. If harmonization *does* fix the membranes, the transfer is doing semantic work
  it was not commissioned for and that is a finding about the instrument, not a success.
- **P3e — nothing is adopted.** No harmonized output enters any projection input; view 4-A is
  not regenerated and not harmonized into the raw set.

## What would falsify the dispatch's own framing

- If `leathery` moves the membranes fully to neutral (median C\* under 10 on most views), the
  material-cue mechanism is stronger than 22b claims and the escalation arm is unnecessary.
- If view 3 comes back clean at 770700, the 21c seed×view map has a counter-case on its
  best-evidenced entry, and that is the session's headline.
- If the pre-harmonization mean-L\* spread is small, the Director's consistency observation is
  not a tonal problem and the harmonization arm is aimed at the wrong quantity.

## The works-perfectly test, per arm

- **The term:** does nothing → the seven twins reproduce their v8 predecessors near-exactly at
  the pinned seeds, so *any* broad change is signal and the membrane box is the register to read
  first. Works perfectly → membranes neutral grey, chroma down, hue withheld below the floor.
- **The transfer:** does nothing → every view is byte-identical to its raw twin, which would
  mean the instrument is inert and P3b failed. Works perfectly → identity on view 1, exact
  moment-matching everywhere else, and the eight views read as one dragon at the Director's zoom.
  Note what a *pass* on P3b does **not** prove: matching moments is not reading as one dragon,
  and only his eye closes that gap.
