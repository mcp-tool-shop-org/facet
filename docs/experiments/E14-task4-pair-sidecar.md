# E14 styled target pair — sidecar, written at birth

**SPECIFICATION SOURCE AND VISUAL TARGET, NEVER A PROJECTION REFERENCE.**

This is what the two images at `E:\AI\training\facet_next\E14_prep\pair\` are for, and the
sentence above is the whole of it. They exist so that "did the element land" has a ground
truth on the route's first prop, and so the Director has something to overrule. **They are
not twins**, they were not registered to anything, and nothing projects from them.

## What they are

| | |
|---|---|
| subject | `longsword_00001_raw.glb` — E14 Ruling 1's designated prop |
| views | **0** (yaw 0, face-on) and **1** (yaw 45) |
| frame | 240×1024, fit-axis height, margin 1.204 — `prop.json`'s framing family, ÷16 legal |
| identity | `canon/LONGSWORD-IDENTITY.md`, five named elements |
| prompt | `docs/experiments/E14-twin-prompts.json` v1, built by the committed builder from `prop.json`'s protective entry; views 0 and 1 are **FULL stems, byte-equal to the entry** |
| backdrop word | `plain lavender background` — **E14 Ruling 7**, blue-violet family |
| canny pair | **0.10 / 0.25** — E14 Ruling 6, derived on this subject's own clay |
| register | ultra-realistic, **LoRA NONE** — E14 Ruling 5a, the Director's sentence |
| recipe | seed 770700 · steps 20 · cfg 2.5 · denoise 0.92 · cn-strength 0.9 — `prop.json` first-run operating points |
| graphs | `E14_prep/cloud/pair_view0.json`, `pair_view1.json`, `pair_view1_reroll.json` — saved **before** submission, pre-flighted in code |
| cost | **0 credits** — `estimate_credits` returned "no paid API nodes" on all three submissions; the graph is entirely OSS models, so this is GPU time on the subscription and not metered API spend |

## The re-roll, declared

**View 1's first generation was REJECTED and is preserved in the record**, not deleted:

```
REJECTED_swordclay_1_seed770700.png        the artifact
REJECTED_SHEET_1_seed770700.png            its sheet
REJECTED_SHEET_1_seed770700_HILT.png       its hilt at 4x
readout_REJECTED_view1_seed770700.json     its measurement
```

**The pre-registered rule it violates**, authored before any generation existed: the fixture's
occupancy audit assigns *"both quillon arms end to end — the stepped chamfered ends included —
and the guard's underside"* to **L2, blackened iron**, and states that no family word rides
more surfaces than it owns. On the rejected artifact the crossguard is **gold**, and L3's
material occupies L2's surface. The rule would have been the same whatever came out, which is
the test that separates rejecting a spec violation from selecting a result.

**One re-roll, new seed 770701, recorded as an explicit deviation by the builder's own
pre-flight.** A second failure would have been the result rather than a third roll; it did not
occur. View 0's re-roll was not spent — it shows no pre-registered violation.

## What supersedes what

- **The pair supersedes `canon/longsword-materials-estimated.json`** the moment it exists (the
  galleon rule, and the estimates file says so itself). The estimated L1 at rgb(150,153,158)
  / L\* 63.1 is superseded by the realised L\* 21–24: **this steel is dark**, and the
  sensitivity table's named risk was the opposite direction.
- **The pair supersedes the derived backdrop triple** (214,214,255 · L\* 86.9 · C\* 21.4). The
  realised backdrop is darker and more saturated on all three artifacts, and sits at hue ~305.
- **The palette bands are NOT derived here.** They derive from the fixture's named materials
  cross-checked against this pair — never against the twins they will gate — and that is a
  later ruling's work.

## What must not be done with these

- **Do not project from them.** They are not registered to the mesh and carry no such claim.
- **Do not re-choose the backdrop word or the canny pair on what they show.** Both are ruled
  (Rulings 6 and 7), and Ruling 7b says in terms that the word is not re-chosen while looking
  at the artifact it would judge. The cool-cast finding below is a *finding*, routed to the
  palette-bands derivation.
- **Do not arm a numeric gate on L5.** The gem is below any area floor by construction at
  route frames; the D8 lesson stands and its landing is judged by eye at the hilt crop.
