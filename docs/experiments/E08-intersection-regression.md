# E08 — the intersection regression (Amendment 26)

**Executor session, 2026-08-04.** Task 1 of the intersection dispatch. Both arms ran; the
report stops at **GATE R1**, which is a ruling, not an executor's call.

The question: *does restricting the trust mask to surface that exists change the adopted
2-camera baseline — by how much, where, and in which direction?*

**Answer, in one line: −7,574 styled texels, 43.7% → 43.4% of valid and 83.0% → 82.4% of
reachable, every one of them a loss, none of them in thin structure, all of them within 5 px
of paint that sat on no surface.** Direction, magnitude and location below; the pre-registered
direction in Amendment 26 was the opposite one, and the reason is mechanical.

---

## 1. Gates

| gate | condition | outcome |
|---|---|---|
| **GATE R0** | edited code, flag off, must reproduce the triple to the digit | **PASSES.** Every digit, and pixel-identical to the artifact of record — 0 differing px across atlas, holes and styled mask |
| **GATE R1** | report and STOP; adoption is the advisor's | **HELD.** Nothing adopted, README untouched, no third roll, no view dropped |

## 2. The change, as implemented

`--trust-intersect`, **default off**, in [project_twins.py](../../tools/project_twins.py). With
it on, `fm` becomes `twin_fm ∧ mesh_fm` — the keyed figure intersected with the exact,
undilated raycast silhouette — before every consumer that reads it *as trust*:

| consumer | line (post-edit) | moves with the operand? |
|---|---|---|
| `dist_in = distance_transform_edt(fm > 0.5)` | 484 | yes — the pathway the halt caught |
| `fig_w` from `fm` columns → `esc` → `ed_body`/`ed_head` | 508–515 | yes (measured: it did **not** move here — §5) |
| `e_img` / `med` print | 527–528 | yes, diagnostics |
| `fig = fm > 0.5`, the stratum area-loss table | 544 | **yes — a fourth consumer the dispatch's table did not list.** It is a diagnostic on the trust mask, so it follows the operand; flagged rather than fixed differently |

`twin_fm` survives raw and now carries five printed diagnostics on every view in both
settings of the flag: the bbox pair, IoU(twin, mesh), centroid offset in px, keyed-outside
count, and its largest connected component.

**The bbox halt demotes to a printed warning when the flag is on**, per Amendment 26.

> **One correction to the amendment's stated reason, which does not change its ruling.** The
> amendment says demotion is needed because *"intersection makes the bbox match by
> construction — which would make the andon a check that cannot fail."* Measured: the bbox is
> taken from `twin_fm`, which the intersection does not touch, so the assert **could** still
> fire and is not passing by construction. The demotion is right for the amendment's *first*
> reason — the quantity no longer governs anything downstream, so halting on it would stop
> correct work — and that is what the code comment now says.

The same operand changed in [e08_acceptance.py](../../tools/diagnostics/e08_acceptance.py),
intersecting with the **undilated** sidecar (`raw_mask`), leaving the size-5 `maximum_filter`
as `mask_ok`'s sampling tolerance. Its `--expect-styled` anchor is **scoped to the flag being
off** rather than re-derived, because re-deriving an anchor while looking at the output it
would judge is the move that voided three thresholds already.

## 3. Anchors re-run — four, all exact, three pixel-identical

| anchor | flags | result |
|---|---|---|
| **R0** | `--view 0/4 --edge-absolute`, ARMB twins | 1,050,368 · 43.7% · 83.0% · var 0.02597 · holes 1,352,442. **Pixel-identical to `ARMB/stage1_2cam.png`, `_holes.png`, `_styled_mask.npy` (0 px)** |
| A2 | `--edge-absolute --key-corner-median`, old twins | 938,718 (front 555,185 + back 383,533) · 39.1% · 74.2% · var 0.02182 · holes 1,464,092. **Pixel-identical to `A2/styled_stage1.png` (0 px)** |
| mask-keyed | `--mask-keyed --edge-absolute --key-corner-median` | 681,212 · 28.4% · 53.8% · var 0.01733 · holes 1,721,598. **Pixel-identical to both `A2/repro_stage1.png` and `facet_E06/C1/styled_stage1.png` (0 px)** |
| e08_acceptance | flag off, old twins | `anchor OK`, styled reproduces 681,212 |

**The R0 recipe was recoverable, and this records it** — it was not written down anywhere as
an invocation, only as a description. Reconstructed from the halt report (views 0+4,
`--edge-absolute`, fitted keying, ARMB twins) plus tool defaults, it reproduces byte-for-byte:

```
project_twins.py --prep facet_E06/C1/prep
                 --view 0=facet_E08/ARMB/twins/twin_0.png
                 --view 4=facet_E08/ARMB/twins/twin_4.png
                 --edge-absolute
                 --out facet_E08/ARMB/stage1_2cam.png
```

> **⚠ A correction to the anchor language, which Task 2 will otherwise read wrong.** Commit
> `c469b36` records anchor 2 as *"two-view default == A2: styled 938,718"*, and this dispatch
> repeats it as *"the two-view default lands A2's 938,718 when run with the old twins and flag
> off."* Measured: the **bare** default (no flags) does not land 938,718 — it **halts** at
> A3's background probe, 73.87% of newly-admitted texels within ΔE 10 of background against a
> 2.0% limit. 938,718 needs `--edge-absolute --key-corner-median`. "Default" in that commit
> means the `--front`/`--back` *argument path*, not the absence of flags, which the same commit
> says elsewhere. **The halt is pre-existing, not caused by this edit** — the pre-edit file
> from `git show HEAD:tools/project_twins.py` halts at the identical 73.87%.

## 4. Prediction, recorded and hashed before R1 existed

[E08-intersection-predictions.md](E08-intersection-predictions.md), SHA-256
`9d434a6965b8747ef90ee91e46ce53af2ab6e68ce182b674220923db9a61a5be`, written after R0 and
**before `--trust-intersect` was run once** — no R1 artifact was on disk when the hash was
taken. **Blind with respect to R1.** R0's own diagnostics were consulted; they are the
baseline and the only thing available.

**It predicted the opposite direction to Amendment 26, from the operator rather than from
data.** `distance_transform_edt` of a subset mask is **pointwise ≤** the original, so with the
threshold fixed, intersecting can only reject more. The halt report's own wording says the
shadow *"inflates the distance-to-edge"* — inflated distances mean *less* erosion in R0, so
removing the shadow erodes *deeper*. The phantom boundary was not pushing erosion deep; it was
holding erosion **off**.

| prediction | outcome |
|---|---|
| direction **DOWN** (against the amendment's "up") | **down** |
| styled falls 5,000–20,000 | **−7,574** |
| styled/valid 42.9–43.7% | **43.4%** |
| styled/reachable 81.4–83.0% | **82.4%** |
| variance 0.0256–0.0263 | **0.02587** |
| `fig_w` unchanged, `ed_body` stays 3.9 px | **unchanged; 3.85 / 3.86 px, `ed` arrays byte-identical** |
| gains ≈ 0 | **gains exactly 0, and `dist_in` increased at 0 pixels** |
| losses in the lowest edge-distance strata | **holds** — 53.2% / 43.8% within 1 px of the threshold |
| losses near ground contact | **partly wrong — see §6** |

The zero-gain result was pre-registered as a **correctness check on my own edit**, not a
hypothesis about the subject: with `ed` fixed and a subset mask, a gain would have meant the
implementation was not a pure intersection. It came back 0 in both views and in the union.

## 5. The numbers

### Union

| | R0 (flag off) | R1 (flag on) | delta |
|---|---|---|---|
| styled | 1,050,368 | 1,042,794 | **−7,574** |
| styled / valid (2,402,810) | 43.7% | 43.4% | −0.3 pt |
| styled / reachable (1,265,391) | 83.0% | 82.4% | −0.6 pt |
| reachable | 1,265,391 | 1,265,391 | **0** — the flag does not touch facing or visibility |
| variance | 0.02597 | 0.02587 | −0.00010 |
| holes | 1,352,442 | 1,360,016 | +7,574 |
| **gained (R1 not R0)** | — | — | **0** |
| **lost (R0 not R1)** | — | — | **7,574** |

Per-view losses sum to exactly the union loss (5,399 + 2,175 = 7,574), so **every lost texel
was styled by exactly one view** — none was lost from both, and none was rescued by the other
camera.

### Per view

| | view 0 (yaw 0) | view 4 (yaw 180) |
|---|---|---|
| accepted R0 → R1 | 593,790 → 588,391 (−5,399) | 456,578 → 454,403 (−2,175) |
| gained | 0 | 0 |
| `fig_w` raw / R0 used / R1 used | 385 / 385 / **385** | 386 / 386 / **386** |
| `ed_body` R0 → R1 | 3.85 → 3.85 px, arrays identical | 3.86 → 3.86 px, arrays identical |
| trust mask px R0 → R1 | 140,643 → 134,024 (−6,619) | 140,016 → 134,038 (−5,978) |
| raw bbox twin vs mesh | 858×385 vs 849×388 | 860×386 vs 849×388 |
| **IoU(raw twin_fm, mesh_fm)** | **0.8761** | **0.8799** |
| **centroid offset** | **dx +7.0, dy +26.7 px (\|d\| 27.6)** | **dx −6.9, dy +32.1 px (\|d\| 32.8)** |
| keyed outside the silhouette | 6,619 px | 5,978 px |
| largest connected component | 5,911 px | 5,487 px |
| components | 97 | 57 |

**`fig_w` did not move on either view**, so the whole delta comes through `dist_in` and none
of it through `esc`. The second consumer was live but silent here — worth stating, because on
a view whose off-surface paint *does* set an extreme column it would fire and scale erosion
globally.

### `dist_in` delta inside the silhouette — the view-6 analogue

Denominator is the raycast silhouette, 146,356 px on both views.

| | view 0 | view 4 | *view 6 (from the halt report)* |
|---|---|---|---|
| changed > 0.5 px | 36,982 — **25.27%** | 28,651 — **19.58%** | *24,896 of 90,553 — 27.49%* |
| changed > 2.0 px | 13,646 — **9.32%** | 14,085 — **9.62%** | *19,236 — 21.24%* |
| max change | **17.68 px** | **16.00 px** | *36.22 px* |
| pixels where `dist_in` **increased** | **0** | **0** | — |

**The adopted 2-camera baseline was carrying the same class of contamination that halted view
6.** A quarter and a fifth of the figure's silhouette pixels had a materially different edge
distance under R0, peaking at 17.7 and 16.0 px. Views 0/4 are milder than view 6 above the
2 px band and at the maximum, and comparable at 0.5 px.

The calibration note in the dispatch anticipated *"the front/back pair may carry much less"*
than view 2's 3,772 px. **Measured, they carry more:** 6,619 and 5,978 px, with single
components of 5,911 and 5,487 px against view 6's 4,436.

## 6. Where the losses sit — and the one place my prediction was wrong

**Locality: total.** Every lost sample, both views, sits **within 5 px of a removed pixel** —
median 2.0 px, max 4 px, 100.0% within 5 px. The mechanism is unambiguous.

**Height: not what I predicted.** I predicted the losses would concentrate at ground contact.
Measured, the lost samples' median height fraction is **0.565 / 0.575** (0 = crown, 1 = sole),
with only **21.3% / 35.0%** in the bottom decile. The removed *area* is at the feet — 90.1% /
92.0% of it in the bottom decile, one dominant pool of 5,911 / 5,487 px — but the removed
*pixel set* also contains 96 and 56 smaller components spanning y 400–951 against a silhouette
of y 87–936, and those slivers sit against real surface up the middle of the figure. Each one
takes a local bite out of `dist_in`, and that is where most of the flipped texels come from.
**The shadow pool is the biggest object removed; it is not where most of the cost lands.**

**And the changed-`dist_in` field is not local at all** — median distance from a changed
silhouette pixel to the nearest removed pixel is **26.0 / 25.3 px**, only 9.4% / 9.8% within
5 px, out to 87 px. That is the spread visible on the sheet across pauldrons, skirt and
greaves: interior distance is set by whichever boundary is nearest, so deleting a rim sliver
can move a pixel tens of px away. Those far-field changes are large-to-slightly-less-large and
never cross the 3.85 px threshold, which is why **36,982 pixels changed and only 5,399 texels
flipped.** The two numbers measure different things and the gap between them is the point.

### Losses by edge-distance excess above the threshold

| excess over `ed` in R0 | view 0 | view 4 |
|---|---|---|
| 0.0–0.5 px | 1,642 — 30.4% | 607 — 27.9% |
| 0.5–1.0 px | 1,232 — 22.8% | 346 — 15.9% |
| 1.0–2.0 px | 902 — 16.7% | 254 — 11.7% |
| 2.0–4.0 px | 738 — 13.7% | 252 — 11.6% |
| 4.0+ px | 885 — 16.4% | 716 — 32.9% |

### Losses by local half-width — the thin-structure question

| half-width stratum | view 0 lost / R0-accepted | view 4 lost / R0-accepted |
|---|---|---|
| 0–4 px | **0** / 1,140 — 0.00% | **0** / 105 — 0.00% |
| 4–8 px | **0** / 4,921 — 0.00% | **0** / 4,948 — 0.00% |
| 8–16 px | 215 / 20,895 — 1.03% | 63 / 11,650 — 0.54% |
| 16–32 px | 760 / 38,571 — 1.97% | 426 / 18,720 — 2.28% |
| 32+ px | 4,424 / 528,263 — 0.84% | 1,686 / 421,155 — 0.40% |

**Zero losses in the two thinnest strata on both views.** The blade lives in the 4–8 px
stratum — the structure A3 was built to protect and the historical erosion was removing 71.1%
/ 66.9% of — and the intersection takes nothing from it. The losses are concentrated, in
proportional terms, in the 16–32 px band at ~2%.

## 7. The consistency check: which silhouette object is which

Asked for one line; it produced a finding, so it gets a section.
[silhouette_agree.py](../../tools/diagnostics/silhouette_agree.py) recomputes the silhouette
with `project_twins`' own scene construction, camera convention and snap, and counts differing
pixels against a sidecar.

| sidecar | view 0 | view 4 |
|---|---|---|
| `ARMB/masks/w3clay_{k}.png` | 146,356 vs 146,356 — **0 differing px**, IoU 1.000000 | **0 differing px**, IoU 1.000000 |
| `ARMB/twins/w3clay_{k}_mask.png` | **0 differing px**, IoU 1.000000 | **0 differing px**, IoU 1.000000 |
| `facet_E01/tex_W3/twinsF/w3clay_{k}_mask.png` | 76,549 vs 146,356 — **69,807 differing**, IoU 0.5230 | 84,599 vs 146,356 — **61,757 differing**, IoU 0.5780 |

**The dispatch's check passes: 0 differing pixels for the ARMB sidecars, both views.** The
pipeline and the instrument intersect with the same object *when the instrument is pointed at
ARMB-era twins*.

**They do not when it is pointed at the twins its own anchor uses.** The E01-era `twinsF`
sidecars are the broken keyed clay masks — 76,549 and 84,599 px raw against a 146,356 px
silhouette, entirely contained inside it (`sidecar-not-live` = 0 on both). Running
`e08_acceptance --trust-intersect` on the anchor configuration therefore cuts 52,778 / 41,462
px of *legitimate* paint and collapses styled to **292,448 (−388,764)**. That number measures
a broken sidecar, not the intersection, and is reported here only to size the hazard.

Two consequences, both reported rather than fixed:

- `e08_acceptance --trust-intersect` is only meaningful against twins whose sidecar is the
  exact silhouette. **Which object is authoritative is a ruling**, so nothing was reconciled.
- The instrument **structurally cannot** be pointed at the ARMB twins: it derives its sidecar
  as `<twin stem>_mask.png`, so `twin_0.png` needs `twin_0_mask.png`, and the ARMB layout has
  `twin_0.png` beside `w3clay_0_mask.png`. Enumerated, not changed — one variable.

**A reconciliation, so a number below does not read as a contradiction of the record.** E08
Arm A quotes the saved mask as *"111,602 px of a 146,356 px silhouette"*; measured raw it is
76,549. `maximum_filter(raw, size=5)` gives **exactly 111,602** (and 116,207 on view 4). The
record's figure is the *dilated* mask; both are right about different objects.

**And one error of my own, found by the guard I wrote after making it.** The first run of
`silhouette_agree.py` reported the old sidecar at 10,800 px against a real 76,549, because in a
`twins/` directory `w3clay_0.png` is the **twin**, not the mask, and the script was thresholding
a painted RGB image as a silhouette. Arithmetic that replays perfectly over the wrong operand —
the exact shape this repo catalogues. The script now asserts a mask has ≤ 4 distinct grey
levels, which would have caught it on the first call, and takes an explicit `--suffix`.

## 8. The bbox andon's reach, measured across all eight twins

[keyed_outside.py](../../tools/diagnostics/keyed_outside.py) runs `project_twins`' fitted key
and its raycast silhouette over every ARMB twin — one code path, no projection, no atlas.

**It reproduces the halt report exactly:** view 2 at **3,772 px** and view 6 at **8,991 px**
with a **4,436 px** largest component, all three matching the ad-hoc check that halted the
build. So the numbers in this report are comparable to the numbers in that one.

| view | yaw | keyed | silhouette | outside | largest CC | % keyed | IoU | centroid dy | bbox H ratio | bbox W ratio | bbox andon @ 1.25 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 140,643 | 146,356 | 6,619 | 5,911 | 4.71% | 0.8761 | +26.7 | 1.011 | 0.992 | pass |
| 1 | 45 | 144,097 | 149,780 | 1,517 | 304 | 1.05% | 0.9424 | +6.7 | 1.002 | 1.002 | pass |
| 2 | 90 | 87,255 | 90,553 | 3,772 | 1,266 | 4.32% | 0.8851 | +20.8 | 1.004 | 0.986 | pass |
| 3 | 135 | 115,894 | 120,439 | 550 | 308 | 0.47% | 0.9533 | +6.5 | 0.994 | 0.997 | pass |
| 4 | 180 | 140,016 | 146,356 | 5,978 | 5,487 | 4.27% | 0.8799 | +32.1 | 1.013 | 0.995 | pass |
| 5 | 225 | 144,273 | 149,780 | 5,768 | 4,562 | 4.00% | 0.8904 | +23.1 | 1.002 | 0.995 | pass |
| 6 | 270 | 91,897 | 90,553 | **8,991** | 4,436 | 9.78% | 0.8329 | +37.0 | 0.993 | **1.921** | **HALT** |
| 7 | 315 | 115,755 | 120,439 | 2,539 | 1,985 | 2.19% | 0.9206 | +15.6 | 1.005 | 0.997 | pass |

Three measurements the advisor asked for as a registration baseline, and one that was not
asked for:

- **Every twin carries off-surface paint** — 550 to 8,991 px, never zero — and **every one has
  a positive `dy`**, the paint centroid sitting 6.5 to 37.0 px *below* the mesh's. That is
  systemic, not a `twin_6` defect.
- **IoU(twin, mesh)** runs 0.8329 (view 6) to 0.9533 (view 3). **Centroid \|offset\|** runs
  6.5 to 39.4 px.
- **The bbox andon fired on the narrowest view, not the dirtiest one.** Views 0, 4 and 5 carry
  single off-surface components of 5,911, 5,487 and 4,562 px — the first two **larger** than
  view 6's 4,436 — and all pass at ratios within 1.3% of the mesh. View 6 fails at 1.921 on
  *width* because it is the profile: its figure is 279 px wide, so a shadow band spanning
  536 px blows the ratio, while the same band inside a 388 px front view does not. The test
  measures **extent relative to the figure's own width**, not how much paint is off-surface.
  Offered as evidence for whichever halt replaces it; **arming it is the advisor's.**

## 9. Artifacts

```
ARMB/R0_stage1_2cam.png + _holes.png + _styled_mask.npy   flag off (== stage1_2cam.png, 0 px)
ARMB/R1_stage1_2cam.png + _holes.png + _styled_mask.npy   flag on
ARMB/diag_R0.npz  ARMB/diag_R1.npz                        per-view acceptance internals
ARMB/intersect_delta.json  ARMB/intersect_delta_sheet.png  the decomposition + its sheet
ARMB/intersect_delta_zoom.png                             the sheet's lower half at 2x
ARMB/keyed_outside.json                                   all eight twins, one code path
ARMB/silhouette_agree.json  ARMB/silhouette_agree_OLDtwins.json
ARMB/anchor_A2.png  ARMB/anchor_maskkeyed.png             the two legacy anchors
ARMB/diag_A2.npz                                          A2-era internals, for §9a
```

`ARMB/stage1_2cam.png` and every prior atlas are **untouched**; both arms wrote to new names.
New tools: `silhouette_agree.py`, `keyed_outside.py`, `e08_intersect_delta.py`.

The sheet is *grey = silhouette · magenta = keyed paint on no surface · blue = surface the
twin's key does not cover · yellow = real surface whose edge distance moved > 0.5 px*. The blue
is not this dispatch's subject and is measured in §9a rather than left as an impression.

## 9a. Found while building the sheet — the blade band takes 0% of stage 1's reference

**Not this dispatch's question, unchanged by the flag, and the same in both arms.** Recorded
because building the sheet before the metrics is what surfaced it, and because the quantity is
an order of magnitude larger than the one Task 1 was sent to measure.

The largest single region of mesh surface that the twin's **keyed figure mask does not cover**
is a tall narrow vertical band — the greatsword blade:

| twin set | surface not covered by the key | largest component | its bbox | candidate texels landing there | **accepted** |
|---|---|---|---|---|---|
| ARMB view 0 | 12,332 px — 8.43% of surface, 261 components | 8,415 px (68%) | h 438 × w 63 @ x 207–270 | 46,197 | **0 — 0.00%** |
| ARMB view 4 | 12,318 px — 8.42%, 258 components | 7,328 px (59%) | h 422 × w 50 @ x 490–540 | 31,699 | **0 — 0.00%** |
| A2-era front | 24,727 px — **16.90%**, corner-median key | 10,738 px | h 650 × w 157 @ x 181–338 | 42,984 | **0 — 0.00%** |
| A2-era back | 28,957 px — **19.79%** | 12,356 px | h 445 × w 244 @ x 310–554 | 74,997 | **0 — 0.00%** |

**The mechanism is arithmetic, not statistical.** Outside `fm`, `dist_in` is 0 by definition;
the edge test is `d_s >= ed` with `ed` ≈ 3.85 px; so every texel there is rejected — in R0, in
R1, and in the A2 lineage. Identical in both arms because the blade is outside `twin_fm`
either way, so **the intersection neither caused nor repaired any of this.**

**Why the key excludes it — measured, and it is marginal rather than absent.** Inside the ARMB
blade band, the twin's paint sits *on* the key's threshold: median |residual| against the
fitted background **0.0657 / 0.0645** versus a **0.06** cut, p90 0.1701 / 0.1804, max 0.4444.
**54.5% / 53.2% of the band passes the colour test before the size-5 `minimum_filter`**, and
the erosion then removes the rest, because a 50-px-wide band that is half-speckled cannot
survive a 5×5 minimum. So both stages contribute: the paint is faint against a grey studio
backdrop *and* the erosion finishes it. This is the same physics as *"below a chroma floor, hue
is not a colour"* — the palette gate already measured this sword at C\* 1.6–2.8 — and the
fifth instance of grey-on-grey in this project.

**And the fitted estimator halved it**: 16.90% → 8.43% of surface recovered into the key,
which is [A2R's *"necessary without being contributory"*](E08-armA2R.md) showing up in a third
place.

**What is NOT established here**, and must not be read in: that this is *the* cause of the
Director's E07 blade rejection. E07's asset came from the A2 lineage, E07 Gate 0 recorded the
blade as *carrying no reference at all*, and the acceptance rate in that region measures 0.00%
— but connecting those is a ruling, three of the eight ARMB views are unmeasured for this, and
nothing here was investigated beyond the four rows above.

## 10. Consumers of the root cause — enumeration confirmed, with one addition

`grep -rn "distance_transform_edt" tools/` — the dispatch's table is accurate, and the
`texpass_iter` site is at line **240** within the quoted 236–241 range.

| site | status |
|---|---|
| `project_twins.py:484` (was 404) | **this dispatch** — behind `--trust-intersect` |
| `diagnostics/e08_acceptance.py:160` (was 137) | **this dispatch** — same flag; see §7 for which object it intersects with |
| `texpass_iter.py:240` | ⚠ confirmed: corner-median key (8×8 corners → median → 0.06 → `minimum_filter` 5) on the **brush output**, feeding `distance_transform_edt`, unbounded by any silhouette. **Not touched.** |
| `diagnostics/commit_funnel.py:123` | ⚠ confirmed: the diagnostic twin of the above, identical construction. **Not touched.** |
| `diagnostics/texel_provenance.py:143`, `diagnostics/e07_l2_bound.py:254` | E07-era, **not modified** |
| **`diagnostics/e08_bg_separation.py:104`** | **⚠ NOT IN THE DISPATCH'S TABLE — a sixth live site.** A4's separability instrument keys with a corner median and runs `distance_transform_edt(fm)` unbounded by the silhouette, using it to report how deep the rejected pixels sit. It is a *depth diagnostic* rather than a trust gate, and it is an E08-era instrument rather than an E07 one, so the "do not modify" fence does not obviously cover it. **Not touched; flagged for the ruling.** |

Also not a keyed-mask transform, listed so the enumeration is closed: `project_twins.py:239`
(inside `local_thickness`, operating on the mask's own core) and
`diagnostics/e08_bg_derive.py:84` (a 3-D occupancy transform).

## 11. What this does not settle

Whether the intersection is **adopted**. Amendment 26 pre-registered the decision rule —
*small and in the expected direction → adopt and restate A2; large or wrong direction → halt
and report* — and the measurement splits that rule: **small** (−0.6 points of reachable, 0.7%
of styled texels) but in the **direction opposite** to the one written down. The argument for
the correction is untouched by the sign: paint on no surface cannot be asked whether it is
trustworthy, and a correction that costs coverage is still a correction. **That is a ruling and
it is not the executor's.**

Also unsettled, and not measured here: whether views 1, 3, 5 and 7 behave like 0/4 under the
intersection (Task 2), what the registration halt should be armed on, whether §9a's 0.00%
blade-band acceptance is the E07 defect or merely adjacent to it, and which silhouette object
is authoritative where the E01-era sidecars disagree with the geometry (§7).

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Both arms differ by exactly one flag; the R0 invocation is recorded verbatim above because it was not recorded anywhere before; four anchors re-run, three pixel-identical; the prediction is SHA-256-pinned before R1 existed; `--diag-npz` makes the decomposition replayable without re-running either arm |
| ANDON_AUTHORITY | **3** | GATE R0 passed on the digits *and* on pixels; GATE R1 halts the session pending a ruling; the bbox halt was demoted only where the amendment authorised it and the demotion's stated reason was corrected in place; a pre-existing halt (73.87%) was reproduced on the pre-edit file rather than blamed on the edit |
| NAMED_COMPENSATORS | **2** | No irreversible call in this task. Every write is a new filename; `stage1_2cam.png` and all prior atlases are byte-untouched — undo is `rm` on the `R0_*`/`R1_*`/`anchor_*`/`diag_*` names, owner = this session. No publish, push, release or cloud spend |
| DECOMPOSE_BY_SECRETS | **2** | One operand changed in two files that must agree; `twin_fm`'s diagnostics separated from `fm`'s trust role; E07 instruments fenced and untouched; the new sixth site named rather than folded in |
| UNCERTAINTY_GATED_HUMANS | **3** | The report stops at the ruling with the decision rule's own split stated contrastively — *you pre-registered "up"; it went down, and here is the operator-level reason it had to* — rather than resolving it |
| EXTERNAL_VERIFIER | **1** | `skip:` as the dispatch allows — deterministic geometry replay, no generative output graded by its generator. The nearest thing to an external check is that `keyed_outside.py` reproduces an independently written ad-hoc check's 3,772 / 8,991 / 4,436 exactly |

---

**GATE R1: report and STOP.** Nothing adopted, no README edit, no third roll, no view
dropped, no threshold invented or retuned. Task 2 waits on the ruling and on the registration
halt being armed.
