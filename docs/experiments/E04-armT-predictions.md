# E04 Arm T — predictions, registered BEFORE any twin exists

**Executor session, 2026-08-04.** Written after Ruling 13 unblocked Arm T and after the
restart-sequence gates ran, and **before a single twin has been generated** — no cloud call
for Arm T has been made, and none will be until the two open rulings close. **Blind: yes**,
for every row. I have seen: the eight clay renders, the eight exact silhouettes, the framing
table, the ratified pair, and Arm G7's measurements. I have seen **no twin of this ship**,
because none exists.

## What Arm T measures, per the spec

Eight eye-level twins (Ruling 13: eight, not ten), generated from the ratified profile's
frame with per-view prompts from [E04-twin-prompts.json](E04-twin-prompts.json), then
**measured and reported with no numeric pass bound** — palette totals and largest CC per view,
registration IoU and centroid per view, and the watch items. The advisor rules before anything
projects.

## The baselines these predictions are made against — all pre-existing, none from a twin

| quantity | value | source |
|---|---|---|
| silhouette share of frame, 8 views | 18.14% / 26.61% / 29.20% / 29.43% | this session's masks, 1066×1024 |
| the ratified pair through the ship's own bands | 5,168 px = **1.622%**, 705 components, largest CC **904 px** | E04 Arm G7 report §6 |
| W3's clean twins through W3's bands | 0.06%–0.33%, largest CC ≤ 800 px bound | E08 armB |
| key margin on the ratified pair | **1.48%** of silhouette at or under the cut | Ruling 8 |
| W3's accepted twins' key margin | 1.77%–2.45% | Ruling 8 |
| thin enrichment on W3 | ≤2 px half-width keys out **5.68–10.77%** against bulk **1.35–1.58%** | fixture S2 |
| landing on the ratified pair | 11 of 12, G7 the miss at ΔE 34.7 | Task 4d |
| G7 after the head-noun form, one view | ΔE 28.3, sub-40° hue population 352 → 1,169 px | Arm G7 |

## Predictions

| # | prediction | falsifiable as stated |
|---|---|---|
| **T1** | **The landing table reproduces the pair's, ±1 element.** Across eight views, the median count of the twelve elements at ΔE ≤ 25 is **11 or 12**. H5's prediction, restated per-view. | fails if the median lands ≤ 10 |
| **T2** | **G7 lands on more views than it misses** — the head-noun form clears ΔE ≤ 25 on **≥ 5 of 8** views. This is the arm's bet against Arm G7's own result, and I expect to lose it: the lids are ~0.4–0.5% of silhouette and the cluster instrument could not resolve them on the one view where red demonstrably arrived. Stated at ≥ 5 anyway rather than hedged, because a prediction I expect to lose is still a prediction. | fails at ≤ 4 |
| **T3** | **The sub-40° red population rises on every view that shows the gun-port band** — views 0, 1, 4, 5, 7 (broadside and three-quarters) each exceed **500 px**, and the two bow/stern-on views (2, 6) fall below it because the ports are edge-on. | fails if the ordering breaks either way |
| **T4** | **Off-palette totals land in the ratified pair's neighbourhood, not W3's.** Per-view off-band share sits in **[0.8%, 3.5%]** — above W3's 0.06–0.33% clean range, because this subject's dark tarred wood sits at hue 40–50 with chroma just over the floor and its own ratified canon measures 1.622%. | fails outside the interval on the median view |
| **T5** | **No twin carries an invented garment.** Largest off-band connected component stays **under 2,000 px** on all eight views — the ratified pair's own largest is 904 px (a hull shadow), and E08's invented sleeve was 4,882. | fails if any view exceeds it |
| **T6** | **Registration is tighter than W3's**, because these controls are built from exact raycast silhouettes at a frame derived from this mesh's own aspect: **IoU ≥ 0.90 on all eight views**, against W3's adjudicated 0.8329–0.9533. | fails if any view falls below 0.90 |
| **T7** | **The key margin beats the accepted character's on every view** — silhouette pixels at or under the key cut stay **below 1.77%** (W3's best accepted view), because the backdrop word is the derived `plain white` and the pair measured 1.48%. | fails on any view |
| **T8** | **Thin enrichment reproduces on this subject and G9 is where it lands.** Rigging/thin strata key out at **≥ 3× the bulk rate** on the median view — the fixture's S2, whose W3 figure is 4.2–6.8×. | fails below 3× |
| **T9** | **The pale near-neutral cluster is the tightest margin on every view**, as it was on the pair (rgb 198,195,192, C\* 2.2, 0.098 from the realised backdrop) — i.e. it, and not any declared material, sets the minimum distance to the backdrop. | fails if a declared material sets the minimum on the median view |
| **T10** | **The two bow/stern-on views (2, 6) are the worst-registered pair**, because they present the least area (18.14% of frame against 29.43%) and the most self-occlusion along the hull's length. | fails if either is not in the bottom two by IoU |

## What I will NOT do

Tune a prompt and re-generate. The one pre-registered rejection rule needs no baseline —
**material not in the spec, one re-roll, new seed, the rejected artifact stays in the record**
— and an element that fails to *land* is not that (the G6 and G7 precedents, Rulings 6 and 8).

Read a number as a pass or a fail. Every gate in this arm is suspended by the spec and by
`ship.json` (`reg_iou_min: null`, `bbox_tol: null`, both palette bounds `null`). I report
numerator and denominator and stop.

Project anything. The twin-baseline halt is before projection, and the H4 reach ceiling that
must be pre-registered before it **cannot currently be computed** — see the halt report.
