# E10 Ruling 4(a) + 4(b) — W3's off-surface measurement, and where the galleon's live: REPORT

**Executor session, 2026-08-06.** Run under [E10 Ruling 4](E10-offsurface-ruling.md)'s
queued dispatch, both items. Read-only over the route: **no route tool edited, no accepted
artifact opened for writing, no accepted number presumed wrong.** Predictions hashed blind
before the first measurement:
[`E10-offsurface-r4ab-predictions.md`](E10-offsurface-r4ab-predictions.md), sha256
`38408839eff743729eb22488d7b203b400afa175322fdfdaea20eaf8aad279cb`, hashed
**2026-08-06 00:30:34**.

New files (diagnostics + one fixture):
[`tools/diagnostics/e10_consumers_subject.py`](../../tools/diagnostics/e10_consumers_subject.py) ·
[`tools/diagnostics/e10_offsurface_where.py`](../../tools/diagnostics/e10_offsurface_where.py) ·
[`docs/experiments/E10-r4a-armb-anchors.json`](E10-r4a-armb-anchors.json).
`e10_offsurface_consumers.py` and `e10_offsurface.py` are **untouched** — their numbers are
cited in a closed ruling, so the subject-flagged carry lives in new files, exactly as
`e12_offsurface.py` carried the bake half.

Measurement outputs, in the repo rather than in either accepted asset's tree (this
session's standing is read-only against both):
[`E10-r4a-armb-offsurface.json`](E10-r4a-armb-offsurface.json) ·
[`E10-r4a-armb-consumers.json`](E10-r4a-armb-consumers.json) ·
[`E10-r4b-galleon-where.json`](E10-r4b-galleon-where.json).

> **⚠ A caveat on every predictions hash in this repo, found while committing this one.**
> The hash above is of the file's bytes as authored — **pure LF**, 140 newlines, 0 CRLF,
> measured. The repo has **no `.gitattributes`** and this rig's `core.autocrlf` is `true`,
> so git stores LF and would hand a **fresh clone CRLF** — where neither this hash nor the
> precedent's would reproduce. In *this* working copy the guarantee holds and is checkable
> both ways: the precedent's recorded `cf16bb55…` still reproduces exactly on
> `E10-offsurface-consumers-predictions.md`, which is also pure LF. So the blind-hash
> mechanism is sound as practised and fragile as stored. **Flagged, not fixed** — adding a
> `.gitattributes` changes how every file in the repo checks out, which is not a read-only
> dispatch's call, and re-hashing the predictions file *after* seeing the results is the
> one move that would be indefensible.

---

## The result in two lines

**Task A — the rate replicates across three subjects and its *class composition* does
not.** W3 measures **2.5840%** off-surface, seated between the ship's 2.5065% and the
beast's 2.6430% — three subjects inside 0.14 points. But **every consumer on W3 moves the
opposite way from the galleon**, because on W3 the off-surface population is concentrated
in *dilation* (4.47%) and depleted in *stage-1* (1.94%) — the exact inverse of the
galleon's finding. **Halted for the ruling on which family becomes standing; nothing here
decides it.**

**Task B — the galleon's off-surface population is a one-texel ring at the UV island
boundary, and it is deep.** 90.85% of it sits on texels 4-adjacent to the mask edge, 91.32%
of *those* are >5 px off the surface, the largest connected component is **33 texels**, and
**no island** is more than 50% affected. Stroke 1's 8.15% is not a composition effect: it
commits a normal share of rim (29.3% against a 23.6% bake-wide) and its rim texels are
off-surface at **27.2%** against 0.86% for stroke 3.

Five of my nine Task-B predictions and three of my six Task-A predictions were falsified.
**The falsifications are the content.**

---

# Task A — W3 / ARMB's own off-surface measurement

## Re-anchoring the instrument before pointing it anywhere new

E12 Ruling 6c made this the standard. `e12_offsurface.py` was run on the ship first:

```
[off] v_ext 1.148544 over H=1024 -> ONE EMIT PIXEL = 1.121625e-03 canonical units
[off] 3,111,817 uv-valid texels, 200,000 sampled (seed 0)
[off] median distance to surface 6.731e-06  (0.0060 px)
[off] OFF-SURFACE (>1 px): 2.5065%   (>5 px): 2.0940%   max 147.4 px
```

Every digit reproduces the ruled ship figure. Only then was it pointed at ARMB.

## The subject, and its pixel unit

ARMB's prep is `facet_E06/C1/prep` (`E08-armB-state.md` line 10;
`E08-intersection-regression.md` line 70). The emit-pixel unit was taken from ARMB's own
`state/job_*/cam.json` — `v_ext` 1.1969748723526452 over `H` 1024 — and **cross-checked
against `texpass_iter`'s own framing rule**, which derives it independently:

| how the unit was obtained | v_ext | one emit px |
|---|---|---|
| supplied from ARMB's `cam.json` | 1.196975 | 1.168921e-03 |
| derived: fit-axis **height**, z extent 0.994165 × margin 1.204 | 1.196975 | 1.168921e-03 |

Identical. Getting this wrong scales every threshold, so it is not inherited on trust.

## Anchors — all passed before any number was believed

| anchor | pins | result |
|---|---|---|
| **A** — the two instruments | the full-bake classification restricted to the rng(0) 200k indices, in the source instrument's own float ordering, reproduces `e12_offsurface.py`'s 2.5745% / 2.2490% / median 2.1073e-08 / max 111.34046 px | **PASS to the recorded digits** |
| **B** — the ceiling | replica at W3's **production** floors (body 0.45 / head 0.18, face rect from `meta.json`) reproduces the recorded reachable count | **PASS: 1,780,546 exactly** |
| **B′** — the head band | the replica's head band, unasked | **1,653,611 — matches `E04-task1-report.md` line 250 exactly** |
| **C** — the classes | stage-1 / brush / dilation / painted from native sidecars reproduce the record | **PASS: 1,653,659 / 101,527 / 647,624 / 1,755,186 exactly** |
| **D** — the stroke splits | three atlas-difference splits against their recorded commits | **1 of 3 PASS** — see below |
| uv-valid | 2,402,810 | **PASS** |

**One anchor fired on my own operand and I fixed the operand, not the anchor.** Anchor A
first halted because I passed the *printed* max (`111.3`) instead of the source JSON's
`111.34045634030718`. The percentages already matched to four decimals; the tolerance was
never touched.

### Anchor D: two of three stroke splits do NOT reproduce, so no exclusion was computed for them

| split | atlas-diff within brush | recorded | verdict |
|---|---|---|---|
| strokes 1–6 | 29,415 | 29,332 | **MISMATCH +83** |
| stroke 7 `y+000_e+55` | 46,981 | 47,020 | **MISMATCH −39** |
| stroke 8 `y+180_e+55` | **25,175** | 25,175 | **PASS** |

The method is not broken and the discrepancy is localised, both measured rather than
argued:

- the three differences **partition the brush class exactly** — union 101,527 = brush
  total, zero brush texels reached by no difference, zero overlap between the 1–6 and 7
  windows;
- the net **+44** is *entirely* the double-count between the stroke-8 window and the
  earlier ones, and it is **exactly** the brush-class difference between
  `out/VOID_post_stroke7_atlas.png` and `state/atlas.prev.png` — two artifacts that both
  stand for the post-stroke-7 state and differ on **316 texels, 44 of them in brush** (4
  landing in the 1–6 window, 40 in the 7 window).

Reported, not diagnosed. Per the tool's own rule, the two unanchored splits get **no**
excluded recomputation.

## The measurement

Full-bake classification, all 2,402,810 uv-valid texels, no sampling. Frames named:
unit-cube `pos` → canonical mesh frame; 1 emit px = 1.168921e-03 canonical units.

```
OFF-SURFACE (>1 px): 62,088 = 2.5840%     (>5 px): 54,303 = 2.2600%     max 111.3 px
```

(The 200k sample estimated 2.5745%; the full count sits inside its sampling noise — the
same relationship the galleon showed, 2.5065 sampled against 2.4967 full.)

### Three subjects, one instrument

| subject | uv-valid | one emit px | **>1 px** | >5 px | >5px share of the population | max |
|---|---|---|---|---|---|---|
| ship (galleon) | 3,111,817 | 1.121625e-03 | **2.4967%** | 2.0813% | 83.4% | 149.3 px |
| **W3 / ARMB** | 2,402,810 | 1.168921e-03 | **2.5840%** | 2.2600% | **87.5%** | 111.3 px |
| beast | 3,240,510 | 6.718107e-04 | **2.6430%** | 2.4395% | 92.3% | 377.6 px |

Total spread across three subjects of very different geometry: **0.1463 points.**

### Per consumer: recorded → excluding the off-surface population

"Excluding" removes off-surface (>1 px) texels from numerator **and** denominator — the
galleon's report's fixed definition, unchanged.

| consumer | headline as recorded | excluded | delta | moves at quoted precision? |
|---|---|---|---|---|
| ceiling reach/valid | 1,780,546 / 2,402,810 = **74.1027%** (quoted 74.1) | 1,739,169 / 2,340,722 = 74.3005% | **+0.1979 pts** | **YES → 74.3** |
| acceptance styled/valid | 1,653,659 / 2,402,810 = **68.8219%** (quoted 68.8) | 1,621,584 / 2,340,722 = 69.2771% | **+0.4552 pts** | **YES → 69.3** |
| acceptance styled/reachable | **92.8737%** (quoted 92.9) | 93.2390% | **+0.3653 pts** | **YES → 93.2** |
| finalize dilation/valid | 647,624 / 2,402,810 = **26.9528%** (quoted 27.0) | 618,675 / 2,340,722 = 26.4309% | **−0.5218 pts** | **YES → 26.4** |
| `project_twins` stage1/valid | same operands as acceptance styled/valid | 69.2771% | +0.4552 pts | YES |
| `texpass_iter` brush/valid | 101,527 / 2,402,810 = **4.2253%** (quoted 4.2) | 100,463 / 2,340,722 = 4.2920% | **+0.0666 pts** | **YES → 4.3** |
| stroke 8 (the one anchored split) | 25,175 | 25,171 | loses 4 = **0.0159%** | — |

### Where W3's off-surface population lives — and it is not where the galleon's lives

| class | off-surface texels | share of the off-surface population | off-surface rate within the class |
|---|---|---|---|
| stage-1 styled | 32,075 | 51.66% | 32,075 / 1,653,659 = **1.9396%** |
| brush | 1,064 | 1.71% | 1,064 / 101,527 = **1.0480%** |
| dilation | 28,949 | 46.63% | 28,949 / 647,624 = **4.4700%** |
| *(reachable)* | *41,377* | *66.64%* | *41,377 / 1,780,546 = **2.3238%*** |

Population baseline **2.5840%**; population reach rate 74.1027%.

**Side by side with the galleon, this is an inversion, not a difference of degree:**

| rate within class | galleon | W3 / ARMB |
|---|---|---|
| stage-1 styled | **3.06%** | **1.94%** |
| brush | 2.27% | 1.05% |
| dilation (never painted) | **2.15%** | **4.47%** |
| population | 2.4967% | 2.5840% |
| reachable | 3.56% | 2.32% |
| off-surface's reach rate ÷ population's | **1.426× — enriched** | **0.899× — depleted** |

On the galleon the painted classes carried the property at a *higher* rate than the
never-painted class. On W3 they carry it at *less than half* the never-painted class's
rate. The two accepted assets disagree about where this population sits.

## Predictions scored — all six were hashed blind

| # | predicted | measured | verdict |
|---|---|---|---|
| **A1** | band 1.8–3.2%, point 2.3%, **direction below both anchors** | **2.5840%** | **band HELD; DIRECTION FALSIFIED** — it lands *between* the two, not below |
| **A2** | ≥80% of the population >5 px | 87.46% | **held** |
| **A3** | stage-1 rate > dilation rate (replication) | 1.94% vs **4.47%** | **FALSIFIED, and inverted** — with it, the ray-clearance reasoning I stated |
| **A4** | off-surface enriched in reachable (>74.10%) | **66.64%** | **FALSIFIED in direction** — depleted, not enriched |
| **A5** | reach ↓, styled/valid ↓, styled/reachable ↑, dilation ↑, brush flat | +0.1979 / +0.4552 / +0.3653 / **−0.5218** / +0.0666 | **4 of 5 FALSIFIED**; only styled/reachable held, and it is 3.7× my size |
| **A6** | no split loses ≥8% | the one anchored split loses **0.0159%**; two splits unanchored | **held on the split that anchored only** — pre-labelled weak, and it stayed weak |

## Task A halts here

Both assets now carry the on-surface family, so **E10 Ruling 2's comparability condition
has its input.** The table the ruling needs, with both assets' denominators named:

| quantity | galleon as-recorded | galleon on-surface | Δ | W3 as-recorded | W3 on-surface | Δ |
|---|---|---|---|---|---|---|
| reach ceiling / valid | 42.72 | 42.25 | **−0.47** | 74.10 | 74.30 | **+0.20** |
| styled / valid | 36.89 | 36.68 | **−0.21** | 68.82 | 69.28 | **+0.46** |
| styled / reachable | 86.4 | 86.8 | +0.4 | 92.87 | 93.24 | +0.37 |
| dilation / valid | 56.24 | 56.44 | **+0.20** | 26.95 | 26.43 | **−0.52** |
| brush / valid | 6.87 | 6.89 | +0.02 | 4.23 | 4.29 | +0.07 |

**Three of five consumers move in opposite directions on the two assets**, and every W3
headline moves at its quoted precision. Which family becomes the standing cross-asset
headline is Ruling 2's question and it is **not decided here**.

---

# Task B — where the galleon's painted off-surface texels live

Population re-derived independently and checked against the recorded count: **77,693
(2.4967%)** — external check PASS, against a JSON this tool did not write.

## The works-perfectly test, restated with the measured value beside it

Every no-defect value below was written down and hashed **before** the measurement.

| measurement | no-defect value (pre-registered) | measured | reading |
|---|---|---|---|
| **B1** rate per rim stratum | **FLAT at 2.4967%** (zero only if the bake is perfect) | 9.62 / 0.18 / 0.44 / 0.44% | not flat — **21.78×** |
| **B2** seam adjacency | on a closed mesh, rim **is** seam; no second number | 17 boundary edges of 1,405,755 = **0.0012%** | closed; B2 is B1 |
| **B3** rate per owning view | **eight equal rates at 3.06%** | 0.28% – 10.07% | **35.42× spread** |
| **B4** modal exact position | modal duplicate 1–2 | off-surface **4**, on-surface **60** | not a default fill |
| **B5** >5 px share per rim stratum | **the same share (83.36%) everywhere** | 91.32 / 4.37 / 3.44 / 9.43% | inverted from my prediction |
| **B6** atlas components | thousands of tiny, largest in the tens | 44,762 components, largest **33**, none ≥100 | it *is* speckle |
| **B7** per-island rate | **every island at 2.4967%** | **0** islands >90%, **0** islands >50% | no island is wholesale wrong |
| **B8** per stroke | **six equal rates at 2.27%** | 0.41% – 8.15% | 19.7× spread |

**The trap the table was built against did not fire.** Reading "the numbers are small" as
"nothing is wrong" would have been the error; the null for B1/B3/B7/B8 is *flat*, and none
of them is flat.

## B1 — island-rim distance

`rim` is the Euclidean distance transform of the uv-valid mask: each valid texel's distance
to the nearest non-valid texel, in **atlas texels**. A valid texel's minimum possible value
is 1.0, reached exactly when it is 4-adjacent to a non-valid texel — so **the `rim≤1`
stratum is precisely the outermost ring of the mask**, and a diagonal-only neighbour falls
into the next stratum.

| stratum | texels | off-surface | **rate** | vs baseline | share of the population |
|---|---|---|---|---|---|
| **rim ≤ 1** (the outer ring) | 733,417 | **70,583** | **9.6239%** | **3.85×** | **90.85%** |
| rim 2–3 | 1,314,685 | 2,427 | 0.1846% | 0.07× | 3.12% |
| rim 4–8 | 893,286 | 3,930 | 0.4399% | 0.18× | 5.06% |
| rim > 8 | 170,429 | 753 | 0.4418% | 0.18× | 0.97% |

Median rim distance: **1.00** off-surface against **2.24** on-surface (no-defect value:
equal, ratio 1.00; measured ratio 0.447).

## B5 — and the ring is the *deep* part

| stratum | off-surface | share of those that are **>5 px** off |
|---|---|---|
| rim ≤ 1 | 70,583 | **91.32%** |
| rim 2–3 | 2,427 | 4.37% |
| rim 4–8 | 3,930 | 3.44% |
| rim > 8 | 753 | 9.43% |

No-defect value: 83.36% in every stratum. **Two populations sit on top of each other** — a
large, far-off ring at the mask boundary, and a small, shallow interior residue of ~0.3%
that is almost entirely sub-5-px.

## B2 — the rim is a seam

The exported mesh carries **757,490** vertices; welded by position it has **465,569** —
glTF splitting at every UV seam, exactly as the standing constraint says. Of 1,405,755
unique welded edges, **17** have a single incident face (**0.0012%**). The mesh is closed
to four decimal places, so **every island rim is a seam** and seam adjacency is
arithmetically B1. There is no second number to report, and that was pre-registered.

## B3 — per stage-1 owning view

| view | stage-1 texels | off-surface | rate | vs baseline | share of the population |
|---|---|---|---|---|---|
| 0 | 160,693 | 5,378 | 3.3468% | 1.34× | 6.92% |
| 1 | 150,558 | 3,223 | 2.1407% | 0.86× | 4.15% |
| 2 | 98,742 | 531 | 0.5378% | 0.22× | 0.68% |
| 3 | 150,053 | 745 | 0.4965% | 0.20× | 0.96% |
| 4 | 158,619 | 451 | **0.2843%** | 0.11× | 0.58% |
| 5 | 142,489 | 1,139 | 0.7994% | 0.32× | 1.47% |
| 6 | 114,589 | 6,359 | 5.5494% | 2.22× | 8.18% |
| **7** | 172,216 | **17,344** | **10.0711%** | **4.03×** | **22.32%** |

Spread **35.42×**. No-defect value: eight equal rates.

## B4 — not a default fill

| population | texels | distinct exact positions | modal duplicate count |
|---|---|---|---|
| off-surface | 77,693 | 77,210 | **4** |
| on-surface *(the null)* | 3,034,124 | 2,172,764 | **60** |

The off-surface positions are *more* unique than the on-surface ones, not less. Nothing
here looks like an unwritten constant.

## B6 / B7 — speckle at boundaries, and no island is wholesale wrong

- **44,762** connected components in the atlas (8-connectivity); largest **33** texels;
  **zero** components ≥ 100; 0.00% of the population in components ≥ 100.
- **21,553** UV islands, median size **75** texels. **Zero** islands are >90% off-surface.
  **Zero** are >50%. The single largest contributor is one 5,068-texel island with 239
  off-surface texels — a **4.716%** rate.

## B8 — why stroke 1 loses 8.15%

Per stroke, on the anchored claim map (all six commits reproduce the record exactly):

| stroke | commits | off-surface | rate | median rim | >5 px share | in islands >50% off |
|---|---|---|---|---|---|---|
| 1 `y+300_e+00` | 26,531 | **2,163** | **8.1527%** | 1.00 | 91.22% | 0.00% |
| 2 `y+030_e+00` | 22,766 | 382 | 1.6779% | 1.00 | 76.18% | 0.00% |
| 3 `y+150_e+00` | 17,904 | 74 | 0.4133% | 2.00 | 37.84% | 0.00% |
| 4 `y+240_e+00` | 24,486 | 230 | 0.9393% | 1.00 | 45.22% | 0.00% |
| 5 `y+000_e+40` | 63,288 | 1,553 | 2.4539% | 1.00 | 78.49% | 0.00% |
| 6 `y+180_e+40` | 58,877 | 447 | 0.7592% | 1.00 | 51.68% | 0.00% |

**The decomposition that answers the dispatch's question.** A stroke's rate can be high
because it *commits more rim* (composition) or because *its rim is worse* (susceptibility).
Splitting it settles that with arithmetic rather than a story:

| stroke | rim ≤ 1 is this much of its commits | off-rate **within** its rim ≤ 1 | off-rate **within** its rim ≥ 2 |
|---|---|---|---|
| 1 `y+300_e+00` | 29.26% | **27.2481%** | 0.2557% |
| 2 `y+030_e+00` | 22.88% | 6.2788% | 0.3132% |
| 3 `y+150_e+00` | 21.41% | **0.8607%** | 0.2914% |
| 4 `y+240_e+00` | 23.48% | 2.3826% | 0.4964% |
| 5 `y+000_e+40` | 22.55% | 9.4948% | 0.4039% |
| 6 `y+180_e+40` | 22.02% | 2.1058% | 0.3790% |
| **whole bake** | **23.57%** | **9.6239%** | **0.2989%** |

Composition spread **1.37×**; susceptibility spread **31.7×**; interior spread **1.94×**.
The same decomposition over the eight views: composition 18.43–29.16% (**1.58×**),
susceptibility 0.31–33.90% (**108.7×**), interior 0.26–0.41% (**1.57×**).

**Stroke 1 does not commit unusually much rim. Its rim texels are off-surface at 27.2%
where stroke 3's are at 0.86%** — and every group's *interior* rate is flat at ~0.3%. The
whole per-view and per-stroke structure lives in the rim stratum and nowhere else.

## Predictions scored — all nine were hashed blind

| # | predicted | measured | verdict |
|---|---|---|---|
| **B1a** | rim≤1 rate ≥ 3× rim>8 rate | **21.78×** | **held**, 7× my size |
| **B1b** | ≥60% of the population at rim ≥ 2 | **9.15%** | **FALSIFIED** — it *is* a rim skirt |
| **B2** | boundary edges < 1% | 0.0012% | **held** |
| **B3** | per-view spread ≥ 2.5× | 35.42× | **held**, 14× my size |
| **B4** | modal exact position < 100 | 4 (null: 60) | **held** |
| **B5** | >5px share ≤70% near rim, ≥90% deep | **91.32% near, 9.43% deep** | **FALSIFIED, and exactly inverted** |
| **B6** | ≥50% in components ≥100, largest ≥1,000 | 0%, largest 33 | **FALSIFIED** |
| **B7** | an island >90% off, holding ≥20% | zero islands >50% | **FALSIFIED** |
| **B8** | ≥50% of stroke 1's off-surface in >50%-off islands | 0.00% | **FALSIFIED** (necessarily, given B7) |

A negative result is a full success. My whole B-series mechanism picture — coherent blobs,
whole bad charts, shallow rim spill plus deep interior errors — is dead in every part. What
the numbers describe instead is the opposite arrangement: a **deep** one-texel ring and a
**shallow** interior residue.

---

## Appendix — the named unread suspect, read AFTER the measurements

Pre-registered in the predictions file: `bake_hero_prep.py` stayed unread until the numbers
were in, so no measurement could be shaped to it. Read now, and reported as **code text,
not as a cause**:

- [`tools/bake_hero_prep.py:439`](../../tools/bake_hero_prep.py#L439) —
  `scene.render.bake.margin = 8`. It is the only margin set on the bake, and
  `bake.margin_type` is not set, so it takes Blender's default.
- [`tools/bake_hero_prep.py:493`](../../tools/bake_hero_prep.py#L493) —
  `for k in ("pos", "nor", "mask"): bake_pass(k)`. The same margin setting is in force for
  all three bakes, including the one that defines which texels are uv-valid.
- [`tools/bake_hero_prep.py:458-467`](../../tools/bake_hero_prep.py#L458) — the `pos` pass
  itself is a Geometry→Position node, subtract `lo`, divide by `size`, emit. Inside a
  triangle it can only produce a point on that triangle, which is what the on-surface
  median of 0.006 px reflects.

**No mechanism is ruled here.** Whether these lines explain the ring is exactly the sort of
claim this repo has been burned by asserting from a plausible reading, and it is the
advisor's to rule with whatever confirming measurement it specifies.

---

## What is NOT established

- **Any mechanism.** Task B measured *where*; it did not establish *why*, and the code read
  above is text rather than a finding.
- **Which denominator family becomes standing.** Ruling 2's condition now has both assets'
  inputs, and that is all this dispatch was asked to produce.
- **Whether any of this is visible in either accepted asset.** Both stand accepted on the
  Director's eye; nothing here re-opens either gate.
- **The 1–6 / 7 stroke boundary on ARMB**, and the 316-texel disagreement between
  `VOID_post_stroke7_atlas.png` and `state/atlas.prev.png` — localised, not diagnosed.
- **Whether the off-surface ring is removable, or should be.** No fix was contemplated, no
  gate armed, no threshold derived from any number above. B1 in particular was barred from
  gating *before* its value was known, and it stays barred: it is a boundary-distance proxy
  of exactly the kind that fails on thin structure.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | predictions hashed before the first measurement (sha + timestamp in the header); every operand a flag or a fixture entry; both pixel units derived and cross-checked with their operands printed; the predictions hash carried inside the output JSON |
| ANDON_AUTHORITY | 3 | six anchor families, each halting its own question; anchor A fired during bring-up on a truncated operand of mine and I corrected the operand rather than the tolerance; two of three stroke splits missed and their exclusions were **not computed**, nothing substituted |
| NAMED_COMPENSATORS | 3 | writes: two new diagnostics, one fixture JSON, two docs, and JSONs in the session scratchpad. Undo = delete them. The shipped instruments cited in closed rulings were not edited; the claim replay wrote only to scratch |
| DECOMPOSE_BY_SECRETS | 3 | Task A and Task B are separate tools with one purpose each; the subject is supplied by flags and the anchors by a versioned fixture, so the record and the recomputation cannot be written by the same hand |
| UNCERTAINTY_GATED_HUMANS | 3 | the standing-family question was pre-registered as *halt, do not decide*, and it halts; A6 was labelled weak and B1 barred from gating before either value was known; no recommendation is made anywhere |
| EXTERNAL_VERIFIER | 3 | every Task-A anchor is an artifact this session did not produce; the instrument was re-anchored on the ship's independently ruled 2.5065% before being pointed at W3; Task B's population was checked against `offsurface_consumers.json`, written by a different tool in a different session; B4's null is the on-surface population rather than an assumption |

**Reported, not ruled. Both tasks halt here for the advisor.**
