# E37 Stage B — the three-view re-roll under Ruling 8: report

**Seat:** executor · **Date:** 2026-08-15 · **Spend: 27 → 30 of 40 cloud jobs** (3 jobs,
exactly as authorized). Dispatch: [E37-ruling.md](E37-ruling.md) Ruling 8.

Pre-registration, written **before any payload was emitted and before any job was
submitted**: `E:\AI\training\facet_E37\reroll_preregistration.md`. Seeds, predictions and
the mechanism finding below were all fixed there first.

---

## 1. What was fired, and how it was pinned

**The seeds came from a rule, not a pick:** `seed = 20260815 * 10 + view` — the arc's date
with the view index appended. v1 → **202608151** · v3 → **202608153** · v6 → **202608156**.
No seed in this record begins `2026081`.

**The seed is the only image-affecting field that moved.** Each re-roll payload was diffed
against `payloads_sets/set770700_v<view>.json` — the payload that produced the twin he
rejected, which is the comparison Ruling 8 actually promises. The check asserts the seed
**did** move before asserting nothing else did, so it cannot pass vacuously.

| view | changed fields vs the rejected payload |
|---|---|
| 1 | `13.inputs.seed`, `15.inputs.filename_prefix` |
| 3 | `13.inputs.seed`, `15.inputs.filename_prefix` |
| 6 | `13.inputs.seed`, `15.inputs.filename_prefix` |

Prompt (v-w1, 443/360/443 chars), control, init, negative, recipe (steps 20 · cfg 2.5 ·
denoise 0.92 · euler/simple · shift 3.1 · ControlNet 0.9/0.0/1.0) and frame **368×1024**
all byte-held. Returned filenames carry the seed and view (`e37_reroll202608151_v1` …), so
the provenance is checkable from the artifact rather than from this sentence.

**The emitter was parameterized rather than forked, and the edit is proven non-perturbing.**
`task0/e37_fire_seed_sets.py` expressed a seed × view *cross product* and Ruling 8 needs
*pairs*. A sibling script would have forked the ANDONs that make these payloads
trustworthy, so the tool gained `--pairs` / `--out` / `--prefix-tag` and nothing else.
**Re-emitting the recorded 24 into a scratch directory returns all 24 byte-identical** —
the anchor this repo requires in the commit that edits a cited instrument.

## 2. ⚠ A mechanism finding, measured BEFORE the spend — and the prediction it produced was WRONG

Built before firing, from this repo's cheapest diagnostic (**clay | control | twin** at
zoom, per named defect):

| view | the CLAY geometry | the CONTROL | what the twin PAINTED |
|---|---|---|---|
| 1 | a large protruding nose wedge | the nose drawn as two converging lines | two thin flat lines on a flat cheek — the form gone. The 25 px² census blob at rows 167–182 / cols 143–146 **is one of those lines** |
| 6 | a subtle brow ridge and mouth relief | fragmented brow strokes, a mouth line | heavy black brow arcs and a heavy black mouth arc |
| 3 | a smooth waist-to-pelvis transition | an interior arc across the torso at the waist | a horizontal crease reading as a dent |

**The observation stands and is measured: the control carries a line at all three defect
locations, and the clay carries no defect at any of them.** From it I predicted (P1, live
branch) that a fresh seed against a byte-held control would **reproduce 2 or 3 of the 3
defects** — the ControlNet-literalism family Ruling 5 named for the mole.

**Measured: 0 of 3 reproduced. P1 MISSED, and it missed in the most useful direction.**

The correction is precise and worth more than the prediction was: **the control constrains
where a line is; the seed decides whether it is read as a form or drawn as a line.** The
same control that produced two flat strokes at seed 770700 produced a nose that reads as a
protrusion at seed 202608151. Control-side presence is not control-side determination, and
inferring the second from the first is what went wrong here.

## 3. The named defects — all three gone

Scored by eye at 4–6× on the before/after zooms, **and declared as an eye judgement**: no
measurable proxy for these separates an artifact the Director rejected from one he
accepted, and this repo spent four experiments learning that such a proxy is not a metric.
**The verdict is his.**

| view | his word | at the zoom, after |
|---|---|---|
| 1 | "missing a nose" | a nose reads as a protrusion, with its own shadow, matching the clay's wedge |
| 6 | "a line across the face" | the heavy black brow and mouth arcs are gone; a fine hatched brow and a thin smile remain |
| 3 | "a dent in the lower back" | the crease is gone; the back reads continuous into the pelvis |

## 4. ⚠ THE WASH GUARD FIRED — all three arrivals are tonal outliers

Ruling 8 clause 2, instrumented before anything projects. Register C\*, chroma signature
(the pale instrument's `C_in`), dark census and reg-IoU, each view against **its own**
silhouette and **its own** clay.

| view | role | seed | dark count/area | reg-IoU | register C\* | pale px | C_in |
|---|---|---|---|---|---|---|---|
| 0 | kept | 770700 | 16 / 157 | 0.9559 | 23.30 | 1,772 | 21.94 |
| **1** | **RE-ROLL** | 202608151 | **17 / 69** | 0.9404 | **30.68** | 3,232 | 20.24 |
| 2 | kept | 770700 | 10 / 50 | 0.9116 | 29.90 | 585 | 32.75 |
| **3** | **RE-ROLL** | 202608153 | **34 / 247** | 0.9440 | **46.24** | 341 | 38.56 |
| 4 | kept | 770700 | 12 / 54 | 0.9463 | 26.00 | 835 | 23.75 |
| 5 | kept | 770700 | 16 / 84 | 0.9354 | 24.41 | 487 | 22.33 |
| **6** | **RE-ROLL** | 202608156 | **39 / 233** | 0.9592 | **38.94** | 625 | 34.99 |
| 7 | kept | 770700 | 24 / 86 | 0.9145 | 24.39 | 946 | 24.25 |

Kept rows' census, reg-IoU and C\* are **cited** from `selection.json`; the chroma-split
column is measured here for all eight, because `selection.json` carries no such column and
a guard needs its baseline on the same axis as the thing it guards.

**Kept-five register C\* range: 23.30 – 29.90. All three re-rolls land OUTSIDE it, and all
three moved UP:**

| view | C\* before → after | move |
|---|---|---|
| 1 | 30.26 → 30.68 | +0.42 |
| **3** | 29.98 → **46.24** | **+16.26** |
| **6** | 30.42 → **38.94** | **+8.52** |

**It is not the pale-wash class, and the distinction is load-bearing.** The wash that got
per-view mixing parked was chroma *collapse* — paint reverting toward the grey init, whose
C\* median is **1.18**. These move the other way: `C_in` 38.56 and 34.99 against a kept
range of 21.94–32.75. This is chroma **excess**. Both are "tonal outlier" in Ruling 8's
words; only one of them is the recorded precedent. **Reported as a finding, never
smoothed**, exactly as the ruling requires.

**The reg-IoU ANDON did NOT fire** — 0.9404 / 0.9440 / 0.9592, all three above 0.90 and far
above the 0.80 floor.

**And the census went both ways** — the swap is not uniform: v1 improved (19/155 → 17/69),
v6 improved (55/252 → 39/233), **v3 got substantially worse (8/49 → 34/247)**, which is the
lowest-census view of the ruled set becoming one of the highest.

## 5. Two further observations, mechanical

1. **The ear became a protruding knob on both face-bearing re-rolls.** On v1 and v6 the ear
   renders as a rounded peg standing out from the skull, where the clay carries a flat oval
   ear and the replaced twins painted a flat oval. Same change, two independent seeds, so it
   is a property of the re-roll rather than of one draw. Not one of his named defects; up for
   his eye.
2. **v6 carries concentric wood-grain rings centred on that knob**, which the kept views do
   not.

## 6. Prediction scorecard — 1 of 4

All four were written before the jobs fired; all were blind to the re-rolls, and informed by
`selection.json` and the §2 triptychs, which is disclosed in the pre-registration.

| # | prediction | live branch | measured | |
|---|---|---|---|---|
| P1 | the defects reproduce at a fresh seed | 2–3 of 3 | **0 of 3** | **MISS** |
| P2 | re-roll C\* falls below its predecessor | 2–3 of 3 fall | **0 of 3 fell** (all rose) | **MISS** |
| P3 | all three inside the kept C\* range | all 3 inside | **0 of 3 inside** | **MISS** |
| P4 | reg-IoU ≥ 0.90 on all three | all ≥ 0.90 | 0.9404 / 0.9440 / 0.9592 | **HIT** |

**P2 also disposes of a coincidence, which is what it was for.** The pre-registration
recorded, post-hoc and labelled as such, that the three views he rejected were *exactly* the
top three by register C\* (p ≈ 0.018 under random assignment). If that ordering were a
mechanism, fixing the defects should have pulled C\* down. It rose on all three. **The
co-occurrence does not survive its first test** and no gate was ever built on it — the
pre-registration had already ruled it out as a metric because kept v2 (29.90) sits between
rejected v3 (29.98) and kept v4 (26.00).

## 7. Mechanics — the handoff ritual, re-run clean

An earlier run of the suite overlapped a report write, which is the case `pytest.ini`'s
`fold` marker names as the common one. The recorded remedy is run-then-rerun, and it was
applied rather than argued with.

| gate | result |
|---|---|
| full suite, corpus settled | **1047 passed**, 0 failed, exit **0**, 851 s |
| E15 ritual, scratch `--db` | **PASS** — all four legs, exit 0; determinism **BYTE-IDENTICAL** 12,812,288 bytes; **2,024 pointers / 0 dangling**; 37 experiments, missing none |
| manifests A / B / C / D | **HELD** — 116/116 · 84/84 · 7,312 files & 17,072,807,610 bytes (+0/+0) · 335/335 |
| receipts | all under `facet_E37\handoff\` — **outside every protected tree** |

## 8. HALT — his word gates Stage C

The dispatched sheet is `handoff/E37_stageB_reroll_vs_v0.png` (1472×1213): v0, his named
best, beside the three re-rolls at native 368×1024 with the guard numbers riding. Beside it
`handoff/E37_stageB_reroll_before_after.png` (2208×1213) puts what left next to what
arrived, because a swap is not a gain until you have looked at what left.

**Ruling 8's clause 3 is not reached:** one re-roll per view, and a *second* failure on any
view is a result that returns to the Director. Whether these three are a first success or a
first failure is his call, not this seat's — the three named defects are gone and all three
arrivals are tonal outliers, and both facts are on the sheet.

## Artifact homes

`E:\AI\training\facet_E37\`: `reroll_preregistration.md` · `stageB\payloads_reroll\` (3) ·
`stageB\sets\reroll\twin_v{1,3,6}.png` · `handoff\guard\` (census, 3 registers, 8 pale,
`wash_guard.json`) · `handoff\e37_wash_guard.py` + `.txt` ·
`handoff\e37_verify_reroll_payloads.py` + `e37_reroll_payload_check.txt` ·
`handoff\e37_reroll_sheet.py` · the sheets and the `_defect_*` / `_zoom_*` / `_ba_*`
diagnostics.

Twin sha256: v1 `0e83b7f29ad2f73d…` · v3 `efd8d3a51cf072fa…` · v6 `2d86501640302ef8…`.
Job ids: `974d665a-7c1b-4967-b7c5-b795f25d9169` (v1) · `a71d2828-c8ef-48b3-b14e-08ede2782c68`
(v3) · `dfbaa5de-9172-494f-be51-05cf5c7d649d` (v6).

No protected tree was written to. No sealed band was edited. The five kept views were not
re-generated.
