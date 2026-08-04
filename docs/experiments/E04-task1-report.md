# E04 Task 1 — the crown blotch. HALT: the advisor's prior is falsified.

**Executor session, 2026-08-04.** Local only, no GPU, no generation, nothing on the asset
changed. Predictions registered and hashed before any artifact was opened
([E04-task1-predictions.md](E04-task1-predictions.md), SHA256 `BB9A3B78…ED87`; the
source-test block appended before it ran, `A96B1F9C…7356`).

**The kickoff's branch:** *"Not aligned → the prior is wrong. Report and stop; that is a
ruling."* **It is not aligned. I am stopping here.** Tasks 2 and 3 are untouched.

**No judgement of the asset appears in this document.** Gate 1 is accepted and closed; this
identifies a mechanism, and whether it is worth anything is the Director's.

---

## 1. The ruling, in one paragraph

The Director named a hard-edged patch on the crown and side of the head. The advisor's
pre-registered prior was the documented **unlevelled stroke-seam defect** — a provenance
boundary where *"grazing stage-1 paint, both elevated strokes, and dilation meet."*
Measured, that junction is not there: the crown region is **94.8–98.7% stage-1 reference
and 0.0% dilation**, and **0.0%** of its strong luminance steps lie within 2 px of a
provenance boundary on any view that sees it.

The edge is real and it is on a boundary — a different one. It is a **stage-1 inter-camera
ownership seam**, entirely *inside* the reference class. `project_twins` gives each texel
the colour of the accepted view with the largest facing; the crown is split roughly in half
between the **yaw-090** twin and the **yaw-135** twin, and those two twins paint the scalp
**ΔE 17.97** apart on surface both cameras see properly. A provenance map cannot see this,
because every texel on both sides of the line is class TWINS.

## 2. What was measured, and how the claim map was built

The provenance map is **exact and involves no replay**. Stage 1's saved styled mask, the
post-stroke hole map, the final styled mask, and `atlas.png` against `atlas.prev.png` for
stroke 8. It is asserted against the run's own recorded counts before anything reads it:

| class | measured | E08 Task 3 report |
|---|---|---|
| TWINS (stage 1) | 1,653,659 | 1,653,659 |
| BRUSH strokes 1–7 | 76,352 | — |
| BRUSH stroke 8 | 25,175 | 25,175 |
| BRUSH total | 101,527 | 101,527 |
| DILATION | 647,624 | 647,624 |
| sum | **2,402,810 = valid, no overlap** | 2,402,810 |

Two further checks it did not need to pass and did: every class maps **1:1 onto a single
colour** in the run's own `provenance_atlas.png` with zero leakage, and stroke 8 recovered
from `atlas.prev` lands **entirely** inside the brush class.

Stage-1 ownership is reconstructed the same way — `w = facing^power` and `argmax` is
invariant under a monotone power, so the power never has to be guessed. It covers exactly
1,653,659 texels, asserted equal to the stage-1 set.

**Luminance is sampled from the atlas at the hit texel, not from a Blender render.** E07
recorded that its own denominator was 4.0 quanta of 1/765 under `exposure 0.85` and the
Standard view transform. Sampling the atlas removes the tone curve and pairs every
luminance with the exact texel it came from. **The cost is that ratios below are not
numerically comparable to E07's 5.500 / 9.500** — numerator and denominator are reported
separately so that is visible rather than implied.

## 3. The result — whole head camera, no region chosen by me

Five cameras, the head-crop camera at each. Step ratio = median |ΔL| across a boundary over
median |ΔL| within, different-texel denominator (E07's correction, carried).

| camera | provenance ratio | **stage-1 camera seam** | island (chart) |
|---|---|---|---|
| yaw 090 | 16.000 (1,721 cross) | **18.200** (9,553 cross) | 2.250 |
| yaw 045 | 12.600 (2,876) | **15.750** (13,449) | 2.000 |
| yaw 135 | 9.200 (5,109) | **19.200** (16,757) | 2.750 |
| yaw 270 | 17.500 (1,386) | **19.333** (9,406) | 3.000 |
| yaw 000 el 55 | 21.000 (15,833) | **18.667** (19,831) | 1.667 |

Both boundary types carry a step. The separation is in **how much of the head each one
accounts for** — ownership boundaries outnumber provenance boundaries 3.3–6.8× on the four
horizontal cameras — and in the exclusive breakdown below, which is the deciding statistic
because "near a provenance boundary" and "near an ownership boundary" are not exclusive and
have very different base rates.

**Of the strong luminance steps (|ΔL − median₅| > 0.10, E07's inherited `--blotch`), which
boundary explains them alone:**

| camera | **owner only** | **claim only** | both | neither |
|---|---|---|---|---|
| yaw 090 | 65.6% | **0.0%** | 25.1% | 9.3% |
| yaw 045 | 64.2% | **1.1%** | 30.6% | 4.1% |
| yaw 135 | 65.7% | **0.1%** | 21.8% | 12.4% |
| yaw 270 | 77.8% | **0.0%** | 17.5% | 4.7% |
| yaw 000 el 55 | 43.5% | **1.3%** | 47.0% | 8.2% |

**Claim-only is 0.0–1.3% on every camera.** Not one strong step on this head is explained by
a provenance boundary that is not also an ownership boundary.

The chart-fragmentation alternate is measured and is not the mechanism: island ratio
1.667–3.000 against the seam's 15.75–19.33. The dilation alternate is measured and is not
the mechanism: `TWINS|DILATION` ratios 2.2–6.2 and `BRUSH|DILATION` 0.8–1.0 — the flattest
classes present, reproducing E07's 1.50–1.75 finding that dilation blends from its
neighbour by construction.

### The null control

"90% of strong steps are within 2 px of an ownership boundary" is only evidence if it would
not also be true of a boundary set with the same density somewhere else. The owner boundary
map displaced 8 px diagonally — same curves, same length, wrong location:

| region | owner | **NULL (owner + 8 px)** |
|---|---|---|
| crown ROI, yaw 135 | 100.0% | **4.7%** |
| crown ROI, yaw 000 el 55 | 96.3% | 48.1% |
| whole camera, yaw 135 | 87.5% | 38.2% |
| whole camera, yaw 270 | 95.3% | **51.0%** |

On the region at issue the null collapses. **At whole-camera scale it does not collapse
cleanly** — yaw 270's null retains 51.0% against a 9.8% base rate, because ownership curves
are locally parallel and an 8 px shift often lands on a neighbouring one. Reported as the
limitation it is; the ROI figure is the one that separates.

## 4. The Director's region

The crown ROI was drawn **by me, by eye, on the yaw-090 camera, after seeing the panels** —
so it is not blind, and §3's whole-camera numbers, which involve no region choice, are the
primary evidence. The ROI is a *surface* region: a disc drawn once, converted to its 2,851
texels, and applied as "texel in that set" on every view, so "the crown" is the same patch
of scalp from yaw 090 and from yaw 135.

| camera | px | TWINS | BRUSH | DILATION | owners |
|---|---|---|---|---|---|
| yaw 090 | 42,664 | **96.5%** | 3.6% | **0.0%** | y090 20,758 · y135 19,407 · y180 1,003 |
| yaw 045 | 16,541 | **98.7%** | 1.3% | **0.0%** | y090 12,691 · y135 3,632 |
| yaw 135 | 48,105 | **94.8%** | 5.2% | **0.0%** | y090 16,673 · y135 25,363 · y180 3,565 |
| yaw 000 el 55 | 18,707 | 71.8% | 28.2% | **0.0%** | y090 5,791 · y135 6,552 · y180 1,089 |

**Alignment inside the ROI, at E07's inherited operating point:**

| camera | owner | claim | island | NULL |
|---|---|---|---|---|
| yaw 090 | 97.4% | **0.0%** | 10.5% | — |
| yaw 135 | 100.0% | **0.0%** | 9.3% | 4.7% |
| yaw 000 el 55 | 96.3% | **0.0%** | 85.2% | 48.1% |

**The step in the atlas, between the two owners' median scalp colours:**

| camera | side A | side B | ΔE |
|---|---|---|---|
| yaw 090 | y090 rgb(194,141,121) L\*63.3 | y135 rgb(192,161,151) L\*68.7 | **13.14** |
| yaw 045 | y090 rgb(195,143,122) L\*63.9 | y135 rgb(190,160,150) L\*68.2 | **12.92** |
| yaw 135 | y135 rgb(193,162,152) L\*69.1 | y090 rgb(193,140,119) L\*62.9 | **13.83** |
| yaw 000 el 55 | y135 rgb(188,155,145) L\*66.7 | y090 rgb(206,154,134) L\*68.0 | **10.32** |

The two halves of one bald scalp differ by **5–6 L\*** and, more visibly, in saturation —
one side is warm and saturated, the other pink and desaturated.

## 5. The source test — and my prediction S1 is FALSIFIED as stated

The ownership boundary is where the pipeline *switches source*. That is not yet proof the
**sources** are what differ: the scalp could genuinely change colour along that line and the
boundary would be coincidence. S1/S2 were registered before this ran.

**S1 predicted** each twin would move across the seam line by **under half** the between-twin
ΔE. Measured over the ROI:

| | rgb | L\* |
|---|---|---|
| twin_2 (yaw 090) on the side **it** owns | (200,146,124) | 65.2 |
| twin_2 on the side twin_3 owns | (158,108,88) | **50.4** |
| twin_3 (yaw 135) on the side twin_2 owns | (186,150,140) | 65.1 |
| twin_3 on the side **it** owns | (196,167,157) | 70.6 |

Between-twin ΔE on the same texels **15.66**; twin_2 moves **14.78** across the line,
twin_3 **6.29**. S1 required both under 7.83. **twin_2 fails it, so S1 is falsified as
written.**

**And the reason is my operand, not the mechanism — the same error class this repo keeps
paying for.** A texel on the far side of the seam is, *by the definition of the seam*, one
twin_2 sees at a lower angle: ownership is `argmax(facing)`, so crossing the line means the
other camera faces it better. Sampling twin_2 there reads **shading**, and it reads it dark
— L\* 65.2 → 50.4. I asked "does twin_2 change across the line" over texels twin_2 can
barely see. *A number that reproduces exactly can still be measured against the wrong
object.*

Restricting to the fair set — the 1,906 of 2,851 texels **both** cameras see above
`project_twins`' own `--facing-min` 0.45 (inherited, not chosen here):

```
twin_2  rgb(174, 122, 102)  L*56.0        twin_3  rgb(192, 161, 152)  L*68.6
THE TWO SOURCES DISAGREE BY dE 17.97      per-texel median 17.56, p90 32.00
within the fair set: twin_2 moves 15.87 across the line, twin_3 moves 6.61
```

**The restriction does not rescue S1 either** — twin_2 still moves 15.87. So the honest
statement is narrower than S1 wanted and is the one the evidence supports:

> The two twins **disagree about the scalp by ΔE 17.97** on surface both see above the
> pipeline's own facing floor, per-texel median 17.56. twin_2 additionally carries a strong
> shading gradient across this region, so its own variation cannot be separated from the
> disagreement by this measurement. **What is established is that the sources differ by more
> than the step that reaches the atlas (17.97 against 10.3–13.8); what is not established is
> how much of twin_2's variation is shading and how much is content.**

That separation is measurable — it needs the ownership map `M` and the facing-weighted blend
`B` that `project_twins` computes and does not save — and it is **not** measured here.

## 6. The prior's defect is real on this asset; it is just not here

`TWINS|BRUSH` boundaries carry ratios of **12.6, 15.4, 18.3, 18.75, 19.0, 24.7, 26.0, 27.0,
31.4** across the five cameras — the documented unlevelled stroke seam, measured, large, and
present. It is concentrated where the brush painted: the elevated camera, which is the only
one whose ROI carries meaningful brush paint (28.2%), is also the only one where `claim`
reaches 48.3% of strong steps at whole-camera scale.

**The crown is not where the brush painted.** It is 94.8–98.7% stage-1 reference on every
horizontal view and 0.0% dilation on all four. The prior named the right defect and the
wrong region.

## 7. Predictions against measurement

| # | predicted | measured | |
|---|---|---|---|
| P1 | region not provenance-uniform; ≥15% a second class | 94.8–98.7% one class | **FALSIFIED** |
| P2 | modal cross-provenance boundary involves a brush stroke | no cross-provenance boundary in the region at all | **FALSIFIED** |
| P3 | region cross-provenance step ratio ≥ 3.0, point 6–11 | not evaluable — too few cross-provenance pairs in the ROI | **VOID** |
| P4 | ≥50% of patch perimeter within 2 px of a provenance boundary | **0.0%** on all three views | **FALSIFIED** |
| P5 | island ratio ≤ 2.0 and below the provenance ratio | 1.667–3.000, far below the seam's 15.75–19.33 | **correct in direction**, 3.000 exceeds the stated 2.0 |
| P6 | dilation-adjacent boundaries the flattest class | 0.8–6.2, flattest present | **correct** |
| P7 | ROI dilation share above the asset-wide 27% | **0.0%** | **FALSIFIED** |
| P8 | ROI stage-1 share below the asset-wide 68.8% | 94.8–98.7% | **FALSIFIED** |
| S1 | each twin moves < half the between-twin ΔE across the line | twin_2 moves 14.78 / 15.87 | **FALSIFIED** |

**Six of nine wrong, and the composite call went to its stopping branch.** P1/P7/P8 all
failed the same way and for one reason: I reasoned that the crown must be poorly covered by
stage 1 because it grazes every horizontal camera, and never checked that `--head-facing-min`
is **0.18** against the body's 0.45, with `--head-edge-dist` 3.0 against 7.0 — looser floors
added precisely so the head band would not go to the brush. Measured rather than inferred,
after the predictions failed:

```
head band              1,653,611 of 2,402,810 valid texels   68.8%
crown ROI inside it    2,851 of 2,851                       100.0%
stage-1 coverage   inside the head band  72.9%
                   outside               59.8%
                   on the crown ROI      89.2%
```

**The head is the best-covered region on the asset, not the worst.** An inherited constant I
did not read, three predictions built on the guess.

⚠ *One coincidence, flagged so nobody builds on it: the head band holds 1,653,611 texels and
stage 1 styled 1,653,659 — 0.003% apart. They are different sets, not the same one. Stage 1
covers 72.9% of the band and 59.8% outside it; the totals merely land in the same place.*

## 8. Faults of mine in this run

1. **S1 measured against the wrong operand** — pooled texels including ones the sampled twin
   can barely see. Caught by the sign of the result (L\* 50.4 is shading, not scalp), fixed
   with an inherited floor rather than a chosen one, and the corrected test **still** does
   not rescue the prediction, which is reported rather than softened.
2. **Predicted the crown's coverage from geometry instead of reading `--head-facing-min`.**
   Three falsified predictions from one unchecked constant, in a repo whose first rule is
   that an inherited claim is a hypothesis wearing a fact's clothes.
3. **Shadowed `n` inside `align()`**, so the reported region size printed the operating-point
   count for one run. Cosmetic, caught, fixed; no statistic was affected.
4. **Two crashes from variable shadowing** (`cb` as both a boundary mask and a colour array)
   and one from casting the ROI as per-view pixel discs rather than a surface region — the
   latter would have measured a *different patch of head* on every camera had it not been
   caught by the yaw-270 ROI collapsing to 12 px.

## 9. Environment

Watchdog was **STALE on session start** (heartbeat 2.77 min against a 15 s threshold, last
17:09:24) — reported, restarted with `_watchdog_start.ps1`, verified alive at heartbeat 0 s,
VRAM 6,488/32,607 MiB. It logged *"previous watchdog died hard."* No GPU work ran in this
task; the restart was done before anything else because Task 3 needs it.

## 10. Artifacts

```
tools/diagnostics/e04_blotch.py          the boundary instrument (new)
tools/diagnostics/e04_seam_sources.py    the source test (new)
E:\AI\training\facet_next\E04_task1_head\
  E04_task1_sheet.png        asset | provenance | owner | overlay, two views, at zoom
  e04_blotch.json            every number above
  seam_sources.json          the source test
  {asset,prov,owner,overlay,highpass}_y*.png     per-camera panels
  roi_crown_texels.npy       the 2,851-texel region, so the ROI is reproducible
E:\AI\training\facet_E08\ARMB\out\renders_prov\prov_{0,1,2,3,7}.png   (new, --flat)
E:\AI\training\facet_E08\ARMB\cache\isl_grid.npy                      island partition
```

Nothing in `state/` or `out/` that existed before this session was modified.

## 11. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions hashed and committed before any artifact was opened, twice. Every path and camera is an argument; the claim map asserts against the run's four recorded counts before anything reads it; camera basis and projection math copied from `texpass_iter`/`project_twins` with the source lines cited |
| ANDON_AUTHORITY | **3** | The pre-registered branch fired and I stopped at it with Tasks 2 and 3 untouched. Five in-tool assertions guard the claim map and the ownership reconstruction |
| NAMED_COMPENSATORS | **3** | Read-only on every pre-existing artifact. New files only, all under `facet_next/` and two new tools; git is the undo and nothing irreversible was in scope |
| DECOMPOSE_BY_SECRETS | **2** | Three partitions separated so each mechanism is tested against the other two; the source test is its own tool rather than a flag on the first |
| UNCERTAINTY_GATED_HUMANS | **3** | The sheet carries the artifact at zoom, built before the report. Every threshold is inherited (`--blotch` 0.10, `--facing-min` 0.45) or reported as a curve; the one region I chose by eye is flagged as non-blind with ROI-free numbers given first |
| EXTERNAL_VERIFIER | **2** | The null control and the fair-set restriction each overturned a reading of mine; the claim map was cross-checked against an artifact built by a different session with a different method. No second model was involved — `skip:` on that clause, as the dispatch allows |

---

**HALT. The prior is falsified and the branch says stop.** The mechanism found is named,
measured, and has its own limits recorded. Whether it is worth an arm — and whether Tasks 2
and 3 proceed from here — is not mine.
