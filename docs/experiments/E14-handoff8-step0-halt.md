# E14 handoff 8 — step 0's count assert FIRED. The lane halts before stroke 2.

**Executor session, 2026-08-08.** Ruling 27c (`7a401f7`), executed as written. **The repair's
ruled predicate yields 1,431 texels where the ruling asserts 1,086. Nothing was written to the
live state; no stroke was emitted, graphed or submitted; 0 credits.**

> **27c:** *"re-derive the mask by the recorded predicate (territory ∩ within 0.010 of the
> stone mask's bottom edge ∩ stage-1b hue in the gold band), **assert the count 1,086** (a
> different count HALTS)"*

It halted. This report is the evidence.

---

## 1. ⚠ ONE INHERITED PATH CLAIM WAS WRONG, AND IT MATTERS

The dispatch's path sketch says `state/` is *"current (post-reprojection, post-stroke-1)"*.
**It is not.** Measured by SHA-256 before anything else was done:

| file | sha256 (24) | what it actually is |
|---|---|---|
| `state0/atlas.png` | `69f61f32a3e2281aff653fb2` | the pristine stage-1b atlas — matches the works-perfectly gate's recorded hash |
| `run/state/atlas.png` | `6a9b93e04c696da3802a2de9` | post-re-projection, **pre-stroke-1** |
| `run/s1b/atlas.prev.png` | `6a9b93e04c696da3802a2de9` | identical to the above — proving s1b was committed from state |
| **`run/s1b/atlas.png`** | **`fa75204e8bc61627eae43b46`** | **the LIVE state: post-stroke-1** |

`run/s1b/commit.log` reads *"wrote 4,344 texels; holes 2,005,056 → 2,000,712"*, matching
handoff 7's report exactly. `state0/` also sits at `E14_strokes/state0/`, a sibling of `run/`,
not inside it as the sketch draws it.

**Had the repair been pointed at `state/` it would have edited a superseded checkpoint and
stroke 1's 4,344 texels would have silently left the lane.** The inherited-claim law, paying
for itself in the first five minutes.

## 2. What the assert measured

Ruling 27c's predicate, transcribed into `tools/diagnostics/e14_repair_collar.py` before it
was run, with one reading made explicit in the docstring: **"hue in the gold band" carries the
palette's chroma floor** (the route's own law — below a floor a hue is not a colour — and
`canon/E14-longsword-palette.json` defines its bands only above `min_chroma 12.0`). The
convention is `palette_gate.py`'s exactly: C\* > 12.0 strict, hue inclusive both edges. The
floor-less alternative was **not run and not compared**: choosing between readings by which
one returns 1,086 would be tuning a mask against the number it is asserted to hit.

```
[repair] landmark re-walked: the stone's bottom edge z = 0.4340 (asserted)
[repair]   territory                          67,904
[repair]   z <= 0.4340 + 0.01                3,506,984
[repair]   stage-1b gold 42-104 above C* 12     131,802
[repair]   territory AND edge                  8,859
[repair] THE MASK (all three legs)             1,431
AssertionError: ANDON: the ruled predicate yields 1,431 texels, but Ruling 27c names 1,086.
```

## 3. ⚠ THE TWO SETS DO NOT NEST. The ruling names a count from a different definition.

The report's 1,086 **reproduces exactly**, and it is an *outcome* set — the texels whose hue
landed in the forbidden band after the rotation and had not been there before:

| definition | count |
|---|---|
| territory ∩ forbidden-after ∩ NOT forbidden-before | **1,086** |
| the same on the stone's geometric mask instead of the territory | **1,086** |
| **the ruling's stated predicate** (territory ∩ edge ∩ stage-1b gold) | **1,431** |
| in both | 1,081 |
| in the outcome set only (**not** in the ruled predicate) | **5** |
| in the ruled predicate only | **350** |

**The outcome set is not a subset of the ruled predicate.** Five texels landed forbidden
without having been gold-above-floor at stage 1b. So the two cannot be reconciled as
"superset and subset"; they are two different sets that overlap in 1,081.

Handoff 7's §5 table reported *"their hue BEFORE the rotation: gold band share 100.0%"* for
the 1,086. Measured with the palette's floor it is **99.5%** (1,081 of 1,086) — the five are
below the floor at 1b, where a hue is not a colour. That is the chroma-floor law's fourth
firing on this route, and it is the reason the count cannot be re-derived from the description.

**What the extra 350 are.** All 350 are owned by the **drifted views 1/3/5/7** after the
corrected projection, so all of them *were* rotated. They simply did not travel far enough to
cross the band edge: **286 are still in the gold band 42–104** after the rotation and **64 fell
below the C\* floor**. None was forbidden at stage 1b. They are the shallow end of the same
gold arc — the same structure, the same line, a smaller move (median \|Δ\| from state0 of 12
8-bit levels against the 1,086-class's 24).

## 4. Stroke 1 did not touch any of them

| | |
|---|---|
| texels stroke 1 changed anywhere on the atlas | 4,344 |
| of the 1,086-class, changed by stroke 1 | **0** |
| of the ruled 1,431, changed by stroke 1 | **0** |

The repair target is exactly the re-projection's output, uncontaminated by the stroke. Either
candidate can be restored from `state0/` without interacting with committed brush paint.

## 5. The sheet — `run/gates/STEP0_collar_repair_candidates.png`

Built on **scratch copies**; `run/s1b/atlas.png` was SHA'd before and after and is unmoved
(`fa75204e8bc61627eae43b46`). Panels per view row, FLAT light, 6×, crop located automatically
by where the candidates disagree rather than by eye: **FIXTURE | A live | B the 1,086 restored
| C the 1,431 restored | D provenance** (red = the 1,086, cyan = the extra 350).

**In plain words, my eye, before the numbers below.** Panel A carries a thin green line lying
along the *top rim of the gold collar*, at both yaws — the defect the ruling located. In B it
is gone and the collar's top rim reads gold. C looks the same as B to me; I cannot separate
them. Panel D shows red and cyan interleaved along that same rim, the cyan sitting among the
red rather than anywhere else — the extra 350 are the same line, not a second structure.

Measured, on the rendered figure (240×1024, both candidate renders against the live one):

| view | panel | forbidden-band px on the figure | of those, in the junction crop (rows 114–169) |
|---|---|---|---|
| 0 | A live | 295 (0.120%) | **50** |
| 0 | B 1,086 | 265 (0.108%) | **20** |
| 0 | C 1,431 | 265 (0.108%) | **20** |
| 1 | A live | 189 (0.077%) | **56** |
| 1 | B 1,086 | 156 (0.063%) | **23** |
| 1 | C 1,431 | 155 (0.063%) | **22** |

| comparison | px differing in the render | max Δ (8-bit levels) |
|---|---|---|
| A → B (view 0 / view 1) | 67 / 77 | 42 / 40 |
| **B → C** (view 0 / view 1) | **16 / 30** | **5 / 12** |

Reported, not ruled: the whole 1,431-texel question moves **at most 30 render pixels by at
most 12 levels** once the 1,086 are restored, and leaves the junction's forbidden count
identical at view 0 and one pixel apart at view 1. A residue of ~20 forbidden px stays in the
crop under *both* candidates — it is not in the restored set and this session did not chase it.

## 6. What has NOT been done

- **No stroke.** Strokes 2–8 were not emitted, not graphed, not submitted. The ruled order is
  untouched and the re-roll budgets are unspent.
- **Nothing written to any live state.** `run/s1b/` is byte-identical to how this session found
  it, all three files. No `atlas.prev.png` was created; no commit ran.
- **No repair applied.** The tool halted at its assert before opening the state for writing.
- **0 credits** — no submission of any kind was made this session.
- No profile, fixture, palette or ruling edit; no memory-store write; no gate armed; no
  finalize, no pack.

## 7. What is on disk for the ruling

```
tools/diagnostics/e14_repair_collar.py            the op, halted at its own assert; --undo and
                                                  --verify-undo present and unexercised (the
                                                  real op was never offered)
run/gates/STEP0_collar_repair_candidates.png      the five-panel sheet, two view rows
run/step0_candidate_masks.npz                     both candidate masks as flat atlas indices,
                                                  so whichever the ruling picks is re-derivable
                                                  to the texel without re-deriving the predicate
docs/experiments/E14-handoff8-predictions.md      the blind predictions, committed before any
                                                  stroke submitted (the dispatch's requirement,
                                                  honoured even though the lane halted)
```

## 8. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The landmark re-walked by the demotion's own code rather than pasted; `state0`'s SHA asserted against the works-perfectly gate's recorded stage-1b hash before the mask was derived; the chroma-floor reading fixed in the docstring before the count was looked at; every state file SHA'd |
| ANDON_AUTHORITY | **3** | The count assert fired and the session stopped — no second reading tried, no predicate adjusted, no stroke launched past it. The assert sits before the state is opened for writing, so a fired gate leaves nothing half-written |
| NAMED_COMPENSATORS | **3** | Nothing irreversible happened: 0 credits, the live state byte-identical, the demotion's compensator still standing and unused. The repair's own compensator is written and would have been exercised on scratch before the real op |
| DECOMPOSE_BY_SECRETS | **3** | The two candidate sets are separated by *definition* (outcome vs predicate) rather than reported as one disagreement; the extra 350 characterised by ownership, by post-rotation band and by magnitude; the render effect separated from the texel count |
| UNCERTAINTY_GATED_HUMANS | **3** | The halt goes up with both candidates rendered side by side and the difference between them quantified, and with no recommendation as to which is the repair mask — that is a ruling |
| EXTERNAL_VERIFIER | **2** | The count was measured by a file the re-projection did not write, against `state0` and the shipped projector's own owner array; the render check uses Blender and the palette bands rather than the repair tool's own arithmetic. `skip:` on a second model per precedent |

---

## HALT — the ruled predicate and the ruled count describe different sets

**The finding, in one sentence:** Ruling 27c's three legs are *descriptive statistics of an
outcome-defined set* — every one of the 1,086 satisfies them — but read as a **generating**
predicate they admit 1,431, because 350 more texels satisfy the same description without
having crossed the band edge, and 5 of the 1,086 do not satisfy them at all.

**What returns to the ruling's table:**

1. **Which set is the repair mask** — the outcome-defined 1,086, the predicate's 1,431, or a
   third thing the ruling names. Both are on disk as flat indices; either is one command away.
   Note that a predicate written as *"restore the texels the rotation pushed into the forbidden
   band"* is an outcome predicate on a *known, deterministic* prior state, not a colour-tuned
   mask — which may be why the ruling's own count came from it — but that is the ruling's call
   to make, not mine.
2. **The five.** If the mask stays defined by geometry-and-provenance, five texels that are
   forbidden today fall outside it. If it is defined by outcome, 350 rotated gold texels stay
   rotated.
3. **Whether the count assert stays absolute.** It did exactly what it was written to do —
   catch that the mask about to be edited is not the mask the ruling adopted. I did not weaken
   it and I am not asking to.

**The lane is otherwise ready.** The live state is located and verified, the tools read, the
stems and cleared block checked, the blind predictions committed. The seven strokes need one
line of the repair's definition and nothing else.
