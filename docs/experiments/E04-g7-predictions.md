# E04 Arm G7 — predictions, registered BEFORE the generation is submitted

**Executor session, 2026-08-04.** Written before any G7 artifact exists. I have read the pair,
the 4d landing table, Rulings 8–9 and the spec's Arm G7 paragraph. I have **not** run any
measurement on the pair for this arm — not one cluster table, not one pixel count — and the
`after` image does not exist. **Blind: yes**, for every row below.

## The arm, restated as it will run

The pair's **front-view** workflow (`workflow_7_bow_three_quarter.json`, bow three-quarter),
**control image, init image, seed, sampler, steps, cfg, denoise, LoRA and every other token of
the prompt byte-matched**, with exactly one change:

```
red-lined gun port lids   ->   red gun port lids
```

Everything else in the positive prompt stays as it was generated, **including `a verdigris
copper spire on the stern turret`** — G6's Director amendment (Ruling 7) is canon for the
twins, but changing it here would put two variables in a one-variable arm. Noted so it is not
read as an oversight.

## The instrument, pre-registered

**Primary — `e04_bands.py`'s machinery, per image** (the spec names it). k-means in Lab,
`k = 14`, seed 770700, chroma floor C\* 12.0, clustering **only the pixels inside the exact
raycast silhouette** `masks1024/galleonclay_7.png`. Run identically on BEFORE
(`target_7_bow_three_quarter.png`) and AFTER. 4d clustered the two views *together*; this arm
is a single-view A/B, so both sides are re-measured in the same single-view units and 4d's
two-view numbers are quoted only for continuity.

`e04_bands.py`'s own inherited verdict thresholds are used unchanged: **LANDED ΔE ≤ 25**,
NEAR ≤ 40, NOT FOUND > 40. G7's expected colour is `canon/galleon-materials-estimated.json`'s
rgb(150,42,36) — the estimate that was already in the file before this arm was designed.

**The pair's measured element floor**, which the spec makes the pass reading: the smallest
cluster share carrying an element the machinery classes LANDED. On 4d's two-view table that is
**1.56%** (the gold family, G1/G5/G6/G12). The single-view BEFORE run recomputes it in its own
denominator and both are reported.

**Secondary, cluster-independent** — a direct pixel count: silhouette pixels with C\* ≥ 12.0
and hue in [350°,360°) ∪ [0°,50°). The 50° upper edge is **the pair's own measured warm-band
lower edge (62°) minus the 4d band convention's 10°, floored to 50** — derived from data that
existed before this arm, not from its result. Reported for BEFORE and AFTER.

**Placement** — the red set's centroid and bbox against the silhouette bbox, plus a full-size
crop sheet of the gun-port band, BEFORE | AFTER. The landing table's known limit is that it
measures colour, not placement; the crop is what answers placement, and the Director's eye is
what rules on it.

## Predictions

| # | prediction | falsifiable as stated |
|---|---|---|
| **P1** | **Red arrives.** On AFTER, the nearest cluster to rgb(150,42,36) sits at **ΔE ≤ 25** — the machinery's own LANDED threshold. BEFORE measured 34.7 on the two-view table. | fails if ΔE > 25 |
| **P2** | Its share lands in **[1.0%, 6.0%]** of silhouette pixels. Gun ports are small features; a whole-hull red would exceed this and a token blush would fall under it. | fails outside the interval |
| **P3** | It **clears the element floor** — share ≥ 1.56%, so red is not merely detectable but present at the scale at which the gold family was called landed. | fails if share < 1.56% |
| **P4** | **Placement holds:** the red pixels' centroid lies **below the vertical midpoint** of the silhouette bbox, i.e. on the hull rather than in sails or rigging. | fails if the centroid is at or above the midpoint |
| **P5** | **The global repaint stays under E08's eight-element figure:** median ΔE over silhouette pixels *outside* the red set is **< 6.23** (E08's contradiction held-region median at the same denoise 0.92), because one word changed here against eight phrases there. | fails if ≥ 6.23 |
| **P6** | The direct hue-window count goes from **< 500 px on BEFORE** to **> 3,000 px on AFTER**. BEFORE's count is genuinely unmeasured — 4d's "no red anywhere" was the cluster instrument, not a pixel count. | fails on either side |
| **P7** | **No element is knocked out.** The other eleven declared elements keep their BEFORE verdict on AFTER; nothing that landed stops landing because one word moved. | fails if any element's verdict degrades |

## What I expect to have to report either way

The occupancy question is **H1's**, and one generation answers it for this subject only. If red
lands, that is a second instance of the documented mechanism — it is not proof that grammar is
the general lever. If it misses, the spec has already named the alternates (size, occlusion,
the LoRA's warm register) and **the twins run with the head-noun form regardless**, because it
is the correct grammar under the standing rule whatever this measurement says. I will not tune
the phrase and re-run: one generation, and the one-re-roll rule is reserved for a spec-material
violation, which a missing element is not (Rulings 6 and 8, the G6 precedent).

**What I am not measuring:** whether the ship looks better. That is not mine.
