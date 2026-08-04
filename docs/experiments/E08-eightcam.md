# E08 Task 2 — eight cameras

**Executor session, 2026-08-04.** Amendment 27's four steps executed in order. No gate fired;
the registration halt was armed and did not trip. Report and stop.

```
2 cameras (adopted)   styled 1,042,794 / 2,402,810 valid = 43.4%   of reachable 82.4%
8 cameras             styled 1,653,659 / 2,402,810 valid = 68.8%   of reachable 92.9%
                      reachable 1,780,546 = 74.1% of valid   variance 0.03687   holes 749,151
```

**+610,865 styled texels, +25.4 points of valid.** Reach came in at **exactly 1,780,546** — the
number `e08_ceiling.py` computed independently in [E08 Gate 0](E08-gate0.md), to the texel.

---

## 1. Steps 1–3, and the anchors re-run

| step | done | evidence |
|---|---|---|
| 1. `--trust-intersect` default **on**, `--no-trust-intersect` added | yes | R0 recipe + negation flag is **pixel-identical** to `ARMB/stage1_2cam.png` (0 px, atlas + holes + styled mask). The new bare default lands the adopted 1,042,794 / 43.4% / 82.4% |
| 2. registration halt armed at IoU < 0.80; IoU + centroid print every view | yes | did not fire on any of the eight (min 0.8329, view 6). Bbox assert removed; it printed its diagnostic NOTE on exactly one view, 6 |
| 3. `e08_acceptance` sidecar guard + explicit mask argument | yes | guard **halts** on the E01-era sidecar (69,807 px differing) and passes on an exact silhouette (0 px). `--front-mask`/`--back-mask` added |

**Anchors re-run this task — five, four pixel-identical:**

| anchor | invocation | result |
|---|---|---|
| R0 / 2-cam | `--view 0/4 --edge-absolute --no-trust-intersect` | 1,050,368 · 0.02597 · 1,352,442 — **0 differing px** vs `stage1_2cam.png` |
| adopted 2-cam | `--view 0/4 --edge-absolute` | 1,042,794 · 43.4% · 82.4% · 0.02587 · 1,360,016 |
| A2 | `--edge-absolute --key-corner-median --no-trust-intersect` | 938,718 · 0.02182 · 1,464,092 — **0 differing px** vs `A2/styled_stage1.png` |
| mask-keyed | `--mask-keyed --edge-absolute --key-corner-median --no-trust-intersect` | 681,212 · 0.01733 · 1,721,598 — **0 differing px** vs *both* `A2/repro_stage1.png` and `facet_E06/C1/styled_stage1.png` |
| `e08_acceptance` | flag off, E01 twins | `anchor OK`, 681,212 |

**Every pre-Amendment-27 recipe now needs `--no-trust-intersect` added.** Stated as pixel
comparisons rather than as a file hash, per the N-view commit's own correction — that run
recorded `sha b12917a2c7c14c4b`, re-ran to `6589e61a`, and was pixel-identical to both
historical atlases. **File bytes are not pixel values.**

## 2. Prediction: direction right, magnitude wrong

[E08-eightcam-predictions.md](E08-eightcam-predictions.md), SHA-256
`c45bd8438f965d963788ef946324f6c09b9d08c09804a70a8ae839e0641fc27d`, hashed with no
eight-camera artifact on disk. **Blind.**

| prediction | measured | verdict |
|---|---|---|
| reachable within ±1% of 1,780,546 | **1,780,546 exactly** | **hit**, and two independently written instruments agree to the texel |
| acceptance 82–86% | **92.9%** | **missed high** — outside my band by 6.9 points |
| styled 1,460,000–1,530,000 | **1,653,659** | **missed high**, past my own 1,560,000 falsification line |
| styled/valid 60.8–63.7% | **68.8%** | missed high |
| holes ~873,000–943,000 | **749,151** | missed low, consistently |
| variance 0.026–0.031 | **0.03687** | missed high |
| registration ANDON does not fire | did not fire | hit |
| exactly one bbox NOTE, view 6 | exactly one, view 6 | hit |
| no relaxation on any view | none on any view | hit |
| blade band 0.00% accepted, all eight | **0.00% on all eight** | hit |

**My falsification procedure said "check reach first, because that is the inherited number."**
Reach was exact, so the miss is entirely in acceptance. The *direction* argument I gave was
right and the mechanism was right — more cameras give each texel more independent chances, and
`w > best_w` means a rejecting view cannot veto an accepting one — but I wrote that the
counterforce (newly-reachable texels sit at rims and in thin structure) would "roughly cancel,
with the monotone effect slightly ahead." **The monotone effect dominated: +10.5 points.** The
counterforce is either much weaker than I judged or absent.

### The "acceptance lever is spent" claim, measured

The dispatch and Amendment 9 say *the acceptance lever is spent at 83.0% — eight buys from the
ceiling, not from acceptance.* Decomposing the 1.586× rise in styled texels:

```
reach       1,265,391 -> 1,780,546   x1.4071
acceptance      82.4% ->     92.9%   x1.1274
product                              x1.5864     actual x1.5858
log share:  reach 74.0%   acceptance 26.0%
```

**Eight cameras bought from both, and about a quarter of the gain came from acceptance** — with
no acceptance test changed, no threshold touched, no flag moved. Two readings, and they are
compatible:

- **The instruction stands and is vindicated.** *Do not grade eight on an acceptance rate* is
  exactly right, because the rate is not a property of the pipeline — it is a **function of
  camera count**. 82.4% and 92.9% describe the same tests.
- **The claim behind it is about a different lever.** "Spent" was measured on *loosening the
  tests* (the facing-floor ladder, the edge distance), and that remains untested here. Nothing
  in this run loosened anything. So the claim is not falsified — but "83.0%" cannot be quoted as
  a ceiling on acceptance, because acceptance reached 92.9% without any lever being pulled.

For the record, [Arm B's prediction B3](E08-armB-predictions.md) forecast **~55%** of valid from
74.10% reach × 81.6% A2-era acceptance. Measured **68.8%** — B3 undershot by 13.8 points, and
its own caveat named the reason (*"eight overlapping cameras may accept differently"*).

## 3. Per view

| view | yaw | silhouette | keyed outside | largest CC | IoU | centroid dy | `fig_w` raw→used | `ed_body` | styled |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 146,356 | 6,619 | 5,911 | 0.8761 | +26.7 | 385 → 385 | 3.85 | 588,391 |
| 1 | 45 | 149,780 | 1,517 | 304 | 0.9424 | +6.7 | 418 → **417** | 4.17 | 596,642 |
| 2 | 90 | 90,553 | 3,772 | 1,266 | 0.8851 | +20.8 | 275 → 275 | 2.75 | 329,451 |
| 3 | 135 | 120,439 | 550 | 308 | **0.9533** | +6.5 | 303 → 303 | 3.03 | 423,328 |
| 4 | 180 | 146,356 | 5,978 | 5,487 | 0.8799 | +32.1 | 386 → 386 | 3.86 | 454,403 |
| 5 | 225 | 149,780 | 5,768 | 4,562 | 0.8904 | +23.1 | 415 → **413** | 4.13 | 459,291 |
| 6 | 270 | 90,553 | **8,991** | 4,436 | **0.8329** | **+37.0** | 536 → **274** | **2.74** | 265,708 |
| 7 | 315 | 120,439 | 2,539 | 1,985 | 0.9206 | +15.6 | 303 → 303 | 3.03 | 434,192 |

Per-view styled sums to 3,551,406 against a union of 1,653,659 — **2.15× redundancy**, which is
where the acceptance rise comes from.

## 4. The intersection on eight cameras — and view 6 goes the other way

Amendment 27 adopted the intersection on the views-0/4 pair, where `fig_w` **did not move** and
the `ed` arrays were byte-identical. On the full eight, `fig_w` moves on **three** views, and on
view 6 it moves **49%** (536 → 274). Run as a single-variable pair:

```
8 cameras, --no-trust-intersect   styled 1,663,572   69.2% of valid   93.4% of reachable   var 0.03693   holes 739,238
8 cameras, adopted default        styled 1,653,659   68.8%            92.9%                var 0.03687   holes 749,151
                                  net -9,913 (0.60% of styled)   gained 2,983   lost 12,896
```

| view | `ed_body` noTI → TI | styled noTI → TI | delta | gained | lost |
|---|---|---|---|---|---|
| 0 | 3.85 → 3.85 *(identical)* | 593,790 → 588,391 | −5,399 | **0** | 5,399 |
| 1 | 4.18 → 4.17 | 605,499 → 596,642 | −8,857 | 46 | 8,903 |
| 2 | 2.75 → 2.75 *(identical)* | 335,140 → 329,451 | −5,689 | **0** | 5,689 |
| 3 | 3.03 → 3.03 *(identical)* | 424,992 → 423,328 | −1,664 | **0** | 1,664 |
| 4 | 3.86 → 3.86 *(identical)* | 456,578 → 454,403 | −2,175 | **0** | 2,175 |
| 5 | 4.15 → 4.13 | 468,078 → 459,291 | −8,787 | 87 | 8,874 |
| **6** | **5.36 → 2.74** | 259,240 → **265,708** | **+6,468** | **8,920** | 2,452 |
| 7 | 3.03 → 3.03 *(identical)* | 437,900 → 434,192 | −3,708 | **0** | 3,708 |

**The monotonicity argument from the R1 prediction holds exactly, and its precondition is
visible in the data.** On all five views where `ed` is byte-identical, gains are **exactly
zero** — a subset mask with a fixed threshold cannot admit anything new. Gains occur on, and
only on, the three views where `fig_w` shifted. `dist_in` increased at **0 pixels on all eight**.

**View 6 is the exception class and it is the view that caused the halt.** Its cast shadow spans
536 px against a 279 px profile figure, so pre-adoption `esc = fig_w / 700` scaled the erosion
to **5.36 px on a 274-px-wide figure** — nearly double what the same rule gives the corrected
width. The intersection removes the shadow, `fig_w` falls to 274, `ed_body` falls to 2.74, and
the erosion *loosens*. So on view 6 the change is a net **+6,468**, not a cost.

Two things follow, both for the ruling rather than for me:

- **Amendment 27's evidence base did not cover this case.** The adoption was justified on a
  pair where `ed` could not move; on the halting view it moves by half. That is not an argument
  against the adoption — 536 px was the shadow's lie and the mesh bbox is 279 — but the change
  is a *tightening* on five views and a *loosening* on one, which the two-camera measurement
  could not show.
- **`--edge-absolute` scaling erosion by global figure width is the repo's named pattern again.**
  A global constant governing a local feature: one twin's cast shadow doubled the erosion across
  that entire view. Fourth instance. Not touched here — one variable.

### `dist_in` corruption per view, and it does not track the keyed-outside count

| view | keyed outside px (rank) | changed > 0.5 px | > 2.0 px | max change |
|---|---|---|---|---|
| 0 | 6,619 (2) | 25.27% | 9.32% | 17.68 px |
| 1 | 1,517 (7) | **38.24%** | **26.48%** | **40.61 px** |
| 2 | 3,772 (5) | **41.81%** | **29.13%** | **43.64 px** |
| 3 | 550 (8) | 21.06% | 11.74% | 6.00 px |
| 4 | 5,978 (3) | 19.58% | 9.62% | 16.00 px |
| 5 | 5,768 (4) | 31.59% | 21.85% | 17.72 px |
| 6 | 8,991 (1) | 27.49% | 21.24% | 36.22 px |
| 7 | 2,539 (6) | 19.51% | 7.32% | 11.00 px |

**Pearson r between keyed-outside px and the fraction of `dist_in` materially changed is
−0.073.** No relationship. View 2 has the fifth-largest off-surface count and the **worst**
corruption on both measures; view 1 is seventh by count and second by corruption; view 4 is
third by count and seventh by corruption. **How much off-surface paint there is does not predict
how much damage it does** — what matters is whether a removed pixel was the *nearest boundary*
to real surface. So `keyed_outside_px` is a twin-quality diagnostic and not a proxy for
contamination, and the bbox andon — which is one step further removed again — was measuring a
third thing.

Every lost sample on every view sits within **5 px of a removed pixel** (median 2.0, max 4).

## 5. The blade band across all eight (Amendment 27 §9a)

Per view, the largest connected region of mesh surface the twin's key does **not** cover:

| view | yaw | uncovered | % of surface | comps | largest band | band bbox | candidates | **accepted** |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 12,332 | 8.43% | 261 | 8,415 | 438 × 63 | 46,197 | **0 — 0.00%** |
| 1 | 45 | 7,200 | 4.81% | 223 | 3,175 | 341 × 53 | 19,248 | **0 — 0.00%** |
| 2 | 90 | 7,070 | 7.81% | 117 | 2,853 | 404 × 47 | 19,937 | **0 — 0.00%** |
| 3 | 135 | 5,095 | 4.23% | 192 | 1,306 | 250 × 44 | 3,790 | **0 — 0.00%** |
| 4 | 180 | 12,318 | 8.42% | 258 | 7,328 | 422 × 50 | 31,699 | **0 — 0.00%** |
| 5 | 225 | 11,275 | 7.53% | 156 | 6,082 | 443 × 82 | 30,548 | **0 — 0.00%** |
| 6 | 270 | 7,647 | 8.44% | 60 | 4,110 | 443 × 74 | 14,136 | **0 — 0.00%** |
| 7 | 315 | 7,223 | 6.00% | 246 | 1,369 | 304 × 44 | 4,094 | **0 — 0.00%** |

**0 of 169,649 across all eight views.** The mechanism is arithmetic and it holds without
exception: outside `fm`, `dist_in` is 0, and the edge test needs 2.74–4.17 px. The prediction
held on every view.

### The union — the number I said I could not guess

A per-view rate cannot answer whether the finished atlas has a painted blade, because a texel
excluded head-on may be picked up by a camera that keys it better. Asked properly:

```
texels landing in SOME view's excluded band:   114,209
of those, styled by SOME camera:                63,640 = 55.72%
left with no reference at all:                  50,569 = 44.28%
```

**Eight cameras rescue 55.72% of the band and leave 50,569 texels with no reference.** That is
the answer to the question I recorded as the one most worth having and least guessable — the
band is *partly* recoverable by camera count, and partly not. Whether 50,569 unreferenced texels
under the blade matters is Gate 1's.

**Not established:** that this is the cause of E07's blade verdict. E07's asset came from the A2
lineage; this measures the ARMB eight. The mechanism is the same and measured in both.

## 6. Artifacts

```
ARMB/stage1_8cam.png + _holes.png + _styled_mask.npy      the eight-camera atlas (adopted default)
ARMB/stage1_8cam_noTI.png + ...                           pre-adoption operand, for §4
ARMB/diag_8cam.npz  ARMB/diag_8cam_noTI.npz               per-view internals
ARMB/intersect_delta_8cam.json + .png                     8-panel decomposition sheet
ARMB/delta_8cam_v0_v6.png                                 views 0 and 6 side by side
ARMB/blade_band_8cam.json                                 §5
ARMB/step1_noTI.png  step1_default.png  step1_anchorA2.png  step1_anchorMK.png
```

Every prior atlas is byte-untouched. New tool: `blade_band.py`.

Sheet legend: *grey = silhouette · magenta = keyed paint on no surface · blue = surface the
twin's key does not cover · yellow = real surface whose edge distance moved > 0.5 px*. On view
6's panel the magenta band visibly extends well past the profile figure's width, which is the
1.921 bbox ratio and the 536 px `fig_w`.

## 7. Three corrections to my own work this session

- **I put `⚠` inside a `print` three times** — U+26A0 is not in cp1252 and raises
  `UnicodeEncodeError` on a Windows console. Fixed in all three files, and now written in a
  comment so the fourth does not happen. Comments and docstrings keep the glyph; they never
  reach stdout.
- **`e08_intersect_delta`'s gain warning conflated two cases.** It printed *"GAINED N samples
  with ed identical (False)"* — technically accurate, unreadable, and it told the reader to
  "investigate before reading any other number" in the one case where the number is already
  explained. A gain with `ed` fixed is an implementation fault; a gain with `ed` moved is the
  `fig_w` channel doing its job. Now two distinct messages.
- **The instrument had no guard on its key, only on its silhouette.** Pointed at the ARMB twins,
  `e08_acceptance`'s corner-median `figure_mask` returns **465,363 px — 60.4% of frame against a
  19.01% truth** (the documented 31–76% diffusion-backdrop failure), and it reported 1,063,039
  styled texels off it before I noticed. Amendment 27 §7 specified a guard on the *sidecar*; the
  broken operand was the *key*. Both now guarded — the repo's standing bbox-check rule, which
  this instrument did not have — and the key stays corner-median deliberately, because its
  anchor is *of* that key. **Verifying one operand says nothing about the other.**

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Five anchors re-run, four pixel-identical; every legacy recipe's new flag recorded; the 8-cam pair differs by exactly one flag; prediction SHA-256-pinned before the artifact existed |
| ANDON_AUTHORITY | **3** | Registration halt armed and exercised (did not fire, min 0.8329); bbox demoted to a NOTE and it printed on exactly the view it should; the instrument's new sidecar guard **halts** on a broken mask rather than reporting off it; a second guard added on the operand the amendment did not name |
| NAMED_COMPENSATORS | **2** | No irreversible call. All writes are new filenames; every prior atlas byte-untouched; undo is `rm` on `stage1_8cam*`, `step1_*`, `diag_8cam*`, owner = this session. No cloud spend, publish or push |
| DECOMPOSE_BY_SECRETS | **2** | Route default separated from legacy reproduction by one flag; the instrument's two operands guarded separately; E07-era and A4 instruments untouched behind the fence |
| UNCERTAINTY_GATED_HUMANS | **3** | Reports and stops. The three places the evidence complicates a ruling — the acceptance-lever claim, view 6's sign flip, the 50,569 unreferenced blade texels — are stated as open with both readings, not resolved |
| EXTERNAL_VERIFIER | **1** | `skip:` per the dispatch — deterministic geometry. The nearest external check is real and it passed: reach 1,780,546 matches `e08_ceiling.py`'s independently written computation exactly |

---

**Task 2 reported. Task 3 waits on the ruling** — the acceptance-lever restatement, whether
view 6's sign flip changes anything about the adoption, and whether the blade band gets an arm
before or after Gate 1. Nothing adopted here, no threshold moved, no view dropped, no third
roll.
