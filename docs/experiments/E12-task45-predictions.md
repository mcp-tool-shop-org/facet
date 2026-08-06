# E12 handoff 3 — predictions, pre-registered before Tasks 4 and 5 run

**Executor session, 2026-08-05.** Written and committed **before** any render, any
silhouette, any control, any submission and any clustering. Nothing measured in this
session existed when these were written.

## Blindness, disclosed exactly

**Blind** to: every number Tasks 4 and 5 produce. No render at the profile's framing
exists; no silhouette at 1792x1024 exists; no styled image of this dragon exists in any
form anywhere.

**Not blind** to, and it is disclosed because it moves some of these:

- I have **looked at the Gate 0 clay renders of views 1 and 5** at full size (they are how
  the head-side / tail-side reading in the dispatch was checked at pre-flight). Those ran
  fit-axis **height** with tag `clay`, so they are not the artifacts being predicted — but
  they tell me the pose, and F2/F3 lean on that.
- I have read `frame_00003.json` (frame 1792x1024, `coverage_world` w 1.210068 / h 0.691468)
  and `E12_prep/meta.json` (the bake's bbox).
- I have **not** opened `E12-gate0-report.md`'s coverage figures, `E12-task2-report.md`, or
  `silhouettes.json` from any prior run. F2 is a prediction, not a recollection.
- The galleon's 4c/4d numbers are read and are the stated prior throughout; where a
  prediction is "the ship's shape repeats", that is an inherited prior and is labeled.

---

## Task 4.1 — the geometry legs

| # | prediction | why |
|---|---|---|
| **F1** | `e04_frame_agree` returns **0 differing px** on both views at 1792x1024 fit-axis width — PASS at its own bound. | Both `turn_render` and `silhouette_masks` now carry the identical fit-axis block and `beast.json` pins `width` on both. This is the check the galleon could not pass before the flag existed (4.68% at 1072x1024). If it fires, the framing family is broken on a landscape subject *again* and nothing downstream is trustworthy. |
| **F2** | Silhouette **20-30% of frame on view 1**, **22-32% on view 5**, and **view 5 > view 1**. | W3 sat at 19.01% in a portrait frame. A winged quadruped in a landscape frame has large empty pockets between wing and body, which caps it well under a solid subject. View 5 puts both membranes nearer face-on than view 1 does. |
| **F3** | Control **contour > 20,000 px** on both views, and **Canny edges exceed contour on both**. | The frills, spines, scalloped membrane rims and claw fringe give this subject an unusually high perimeter-to-area ratio (it is why `bg-max-pct` is suspended). Canny exceeding contour is the scale relief: this mesh reconstructs scale as *geometry*, so a clay render composited onto black fires interior edges everywhere. |
| **F4** | The `n_contour < 500` ANDON does **not** fire. | Corollary of F3, stated separately so a fire is scored against a named expectation. |

## Task 4.2 — the styled target pair

| # | prediction | why |
|---|---|---|
| **G1** | **9, 10 or 11 of the 11 elements land** at the galleon's own read (dE <= ~15 to the nearest cluster). | The ship landed 11/12 and W3 landed 8/8. This subject asks for more elements at smaller sizes. |
| **G2** | The misses, if any, are **D8 (eyes) and/or D9 (tongue)** — not D1/D2/D3. | Both are pre-registered as below any area floor. G7's precedent is exact: a small element, declared, that simply never arrived above the chroma floor. The three large materials cannot hide. |
| **G3** | **The five ivory elements (D4/D5/D6/D7/D10) collapse into one cluster**, exactly as the galleon's four gilded elements did into rgb(179,141,49). | They are declared as the same material. This is the merge question answering itself. |
| **G4** | The **realised backdrop is less chromatic than the asked (121,121,172)** — realised C\* below asked C\* — while staying in the blue-violet hue family (h 250-320). | The one measured ask->realise transfer on this exact recipe is the galleon's: asked 255, realised 173, i.e. pulled toward mid grey. Direction inherited; magnitude not predicted. |
| **G5** | **D3 (storm-grey membranes) lands**, and its cluster is among the **three largest** by share. | Largest single surface class on the subject, unambiguous word, and the backdrop derivation was bound by it at every optimum. |
| **G6** | **View 5 comes back with no head anatomy grafted onto the hindquarters** despite its prompt naming six head elements. | E08's B4: an exact-silhouette control locks orientation without the prompt being filtered. This is the first test of that claim on a subject whose elements *are* anatomy — see the finding in `E12-twin-prompts.json`. A failure here is the most informative single outcome available in this session. |
| **G7** | **0 re-rolls used** of the 1 allowed. | The palette-gate re-roll trigger is off-palette material, not a disappointing element. The galleon used 0 of 1. |

## Task 5 — the palette bands

| # | prediction | why |
|---|---|---|
| **H1** | **Forbidden span 180-230 deg (50-64%)** — between W3's 170 deg (47.2%) and the galleon's 288 deg (80.0%). | Above a C\* 12 floor the declared hues are wine-red, ember-orange, bone-tan/ivory and moss-green: one long warm-to-green arc, with the whole blue-cyan half empty. Wider than the character's, narrower than the ship's, because green *and* red are both declared here and the ship declared neither. |
| **H2** | **The ivory family's bands merge into one band.** | Corollary of G3; stated separately because the dispatch asks the merge question directly. |
| **H3** | **D3 (storm-grey) and D11 (slate) fall below the C\* 12 chroma floor** and carry no band at all. | Both are declared as neutrals. This is the galleon's near-neutral-pale-cluster fact arriving by design rather than by surprise — and it is why "below a chroma floor, hue is not a colour" is load-bearing on this subject. |
| **H4** | **At least one measured cluster sits outside every declared element's expectation** (the galleon had 14 clusters against 12 names). | Painted subjects carry shading, rim light and transition colours the declared table never names. |

---

## What a wrong prediction costs here

Nothing, and that is the point — these exist so the session cannot quietly become
retrospective. **F1 is the only one whose failure stops work**: it is a geometry gate with a
bound of 0 px that the advisor pre-registered in E04 Ruling 10, and it fires *before* any
credit is spent. Every other row is scored in the report and changes nothing about what runs.

**F2 and H1 are the two most likely to be wrong**, for the same reason: both are quantitative
priors carried from other subjects, and this arc's own banked calibration lesson (E12 Ruling
6b) is that **this subject class has no working prior in either direction** — reach on a
winged quadruped landed 7.7 points above the ship and 23.6 below the character after Gate 0's
falsifications had already pushed the estimate the other way.
