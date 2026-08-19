# E68 report — the head-band withhold: the amber collapses, the limit still fires

Executor seat (Sonnet), background. Charter: `docs/experiments/E68-headband-withhold-
kickoff.md` (commit a31ccd5). Working tree `E:\AI\training\facet_E68\`. Live handoff
kept throughout: `E:\AI\training\facet_E68\handoff.md`.

**ZERO CLOUD SPEND.** No comfy-cloud tool was ever loaded or invoked this session.
Gate A passes by construction.

## The rule, as implemented

One opt-in flag, `--headband-bg-withhold` (default `False`), added to
`tools/project_twins.py` (+49/-0 lines, 3 additive hunks, `git diff --stat`). On
head-band texels only — `headband[idx]`, the tool's own existing texel-domain array at
line 242, built from `meta.json`'s `crop`/`crop_res` (Stage 1's own head-crop rectangle,
inherited, not re-derived) — a texel is removed from the accepted population if
`dE_bg < args.bg_de` (the tool's own existing default, 10.0, unmodified), computed by
the tool's own existing `fit_background`/`bilinear` pipeline at its existing window.
The filter runs **before** the ANDON's own population is read, so the ANDON's code
(the raise condition and its message) is untouched — only what reaches it changes.
Every new line is guarded by `if args.headband_bg_withhold:`; the default path is
proven byte-identical to pre-E68 (see Gate B / Anchor below).

No new threshold was introduced. `--bg-de` and `--bg-max-pct` are unchanged in value
and untouched in the ANDON's own comparison.

## Predictions, logged before running anything

Full text: `E:\AI\training\facet_E68\logs\predictions.txt`. Four predictions, split
honestly into CODE-DERIVED (read off `classify_contamination.py`'s own source before
writing this experiment's code — not blind) and BLIND (genuine forecasts). Headline:
the structural collapse of class 3 was CODE-DERIVED and confirmed exactly; the
per-view ANDON outcome was BLIND and falsified more strongly than guessed (I predicted
most views would pass; 0/8 did); the hole-cost prediction was BLIND and falsified in
both directions at once, because my own prediction conflated the marginal cost with
the total rate. Full outcomes appended to the predictions file, nothing overwritten.

## Gates

| gate | status | evidence |
|---|---|---|
| Gate A — no cloud call | **PASSED (by construction)** | no comfy-cloud tool loaded or called this session |
| Gate B — `bg-de`/`bg-max-pct` byte-unchanged | **PASSED** | asserted in code (below) and printed; corroborated by both real console runs |
| Gate C — only head-band faces touched | **PASSED** | non-head-band written-texel SET identical, 889,856 == 889,856, exact set comparison |

**Gate B, printed, per the charter's instruction:**
```
bg-de (parsed from tool's own current source default)     = 10.0
bg-max-pct (parsed from tool's own current source default) = 2.0
```
Asserted in code against the tool's live source text (`logs\gateB_threshold_assert.txt`,
exit 0), not merely observed. Both real tool runs below print "dE 10" / "2.0% limit"
verbatim throughout, corroborating the assertion independently.

**Gate B, non-perturbation of the default path (the anchor):** the edited tool, run
with the new flag **omitted**, reproduces E67's Stage 2 view-0 halt exactly: relaxed
16,170, median dE 19.6, twin paint 29.7%/mesh sil 29.7%, IoU 0.9228, "within dE 10 of
it 30.29%", identical `AssertionError` text. `logs\anchor_default_console.txt`. Proven,
not asserted.

**Gate C evidence:** computed as an exact Python `set` comparison (not a count
comparison) of every atlas texel index written by any of the 8 views, restricted to
outside the head band, baseline vs. post-withhold: `{...} == {...}` over 889,856
elements each, `True`. `logs\remap_full.txt`.

## Provenance (Gate 0, re-verified fresh)

All 8 accepted twins' sha256 match `MANIFEST.json` exactly; A1 mesh sha256
`cdf276e794fe...` matches the E67 report's recorded prefix. `logs\gate0_provenance.txt`.

## Why the real tool never produced an atlas either way

The joint 8-view invocation with the new flag halts at view 0's own ANDON (now 4.56%,
down from 30.29%, but still over 2.0%). Since a halt at view 0 prevents observing views
1–7, each view was swept individually — the exact method E67's own Stage 2 used for
the same reason (`logs\withhold_sweep_v{0..7}.txt`). **All 8 exited 1.** No `--diag-npz`
and no atlas was ever produced by the real CLI, in either mode, for the withheld case —
the same structural constraint E67 operated under for the unwithheld case. The
per-view and pooled numbers below are computed by a read-only reimplementation that
directly reuses E67's own already-validated per-view arrays (the pickle
`E:\AI\training\facet_E67\map\data\_raw_results.pkl`), extended with exactly the
withhold predicate the real edit applies, and **hard-validated against the real
edited tool's own console output on 4 numbers × 8 views = 32/32 exact matches** before
anything downstream was trusted (`logs\remap_step0_2.txt`). This is the same method,
same discipline, and literally the same validated data E67's own map used — not a new
instrument.

## THE CENTRAL RESULT — per-view limit comparison

**The limit was not touched. It still fires on all 8 views.**

| view | yaw | OLD % (E67, pre-withhold) | NEW % (post-withhold) | limit | verdict |
|---|---|---:|---:|---:|---|
| 0 | 0   | 30.29 | **4.56**  | 2.00 | FAILS |
| 1 | 45  | 37.48 | **7.24**  | 2.00 | FAILS |
| 2 | 90  | 29.19 | **6.91**  | 2.00 | FAILS |
| 3 | 135 | 29.27 | **17.56** | 2.00 | FAILS |
| 4 | 180 | 28.92 | **10.09** | 2.00 | FAILS |
| 5 | 225 | 42.88 | **10.45** | 2.00 | FAILS |
| 6 | 270 | 34.37 | **11.43** | 2.00 | FAILS |
| 7 | 315 | 47.03 | **21.65** | 2.00 | FAILS |

**0/8 views pass.** Per the charter: this is the result, reported plainly, with the
limit untouched at every step (verified: `--bg-max-pct` default `2.0` unchanged, Gate B).

**The mechanism, measured, not inferred.** The ANDON's percentage is numerator AND
denominator both drawn from the "relaxed" (newly-admitted-by-erosion) population. The
withhold removes hair from both: hair (class 3) is itself almost entirely
relaxed-admitted, so removing it shrinks the denominator by nearly as much as it
shrinks the numerator's hair contribution. The untouched non-hair contamination
(classes 1/2/unclassified — sleeve cuffs, 1px-rounding exterior, and garment-edge
unclassified, none of which the head-band-scoped rule can reach) is left as a **larger
share of a smaller surviving population**. Verified exactly on view 0: relaxed
(denominator) fell 16,170 → 11,810 (−4,360, matching class 3's own view-0 count of
4,360 exactly); the residual numerator is 538 (= 35 class1 + 7 class2 + 496
unclassified, every one of them unchanged) — 538/16,170 = 3.33% under the OLD
denominator, 538/11,810 = **4.56%** under the NEW, smaller one. Verified likewise, to
the texel, on all 8 views (see the class-share table below and `logs\remap_full.txt`).

## Before/after class shares — the amber collapse

Pooled across all 8 views (flagged = every texel that was both relaxed-admitted and
within dE 10 of background — the exact population behind the ANDON's own percentage):

| class | OLD count | OLD % of flagged (27,761) | NEW count | NEW % of flagged (5,846) |
|---|---:|---:|---:|---:|
| class 1 (declared material) | 593 | 2.14% | 593 | 10.15% |
| **class 3 (hair/fringe)** | **21,915** | **78.94%** | **0** | **0.00%** |
| class 2 (true exterior) | 60 | 0.22% | 60 | 1.03% |
| unclassified | 5,193 | 18.71% | 5,193 | 88.83% |

**Class 3's pooled share collapses from 78.94% to 0.00% — exact, complete elimination**,
proven two independent ways: (1) structurally, `headband-in-residual` measures 0 in
every one of the 8 views (a texel cannot survive the withhold AND remain classifiable
as class 3, since class 3 requires headband and the withhold removes every
headband-and-background texel); (2) empirically, the surviving population (classes
1/2/unclassified) is proven **identical as an exact set of texel indices** — not merely
equal in count — to the pre-withhold population, in all 8 views (`SET-IDENTITY check:
True`, sizes matching exactly, `logs\remap_full.txt`). The reproduction step of this
same script first reproduced E67's own pooled 593/21,915/60/5,193 exactly, against
`map\data\summary_table.json`, before the post-withhold numbers were trusted.

Per-view classification reproduced E67's own table exactly (8/8 views, sanity check)
before the post-withhold residual was computed; per-view residual class counts equal
E67's own per-view class1/class2/unclassified counts exactly, with class3 at 0 in
every view. Full per-view table: `remap\data\step3_4_results.json`,
`logs\remap_full.txt`.

**A population the original map never characterized**: the withhold rule has no
"relaxed" qualifier (per the kickoff's own wording), so it also removes a small,
strict-admitted (non-edge-proximate) head-band-background population that was never
part of E67's original "flagged" set at all — **142 texels pooled** (20/0/0/7/31/78/0/6
across views 0–7). Reported for completeness; it does not change the class-share
collapse above, which concerns only the previously-flagged population.

## The hole cost, honestly

| quantity | value |
|---|---:|
| head-band texels (mesh-wide, this crop) | 1,186,538 |
| BASELINE holes (pre-withhold — facing/erosion/reachability alone, no withhold in effect) | 645,842 (54.43%) |
| POST-WITHHOLD holes | 649,001 (54.70%) |
| **NEW holes attributable to the withhold specifically** | **3,159 (0.27% of the head band)** |

Read plainly, in both directions: the head band already carries a very large
pre-existing hole rate (54.43%) from facing/erosion/reachability alone, with no
withhold in effect at all — over half of this crop's texels are never accepted by any
of the 8 cameras regardless of this experiment. Against that baseline, the withhold's
own marginal contribution is small: **0.27 percentage points, 3,159 texels**, despite
eliminating all 21,915 (view,texel)-instance occurrences of class-3 contamination.
The reason the marginal cost is so much smaller than the eliminated-instance count:
most withheld (view, texel) pairs are texels that at least one of the OTHER 7 cameras
still reaches and does not flag as background, so the multi-view redundancy of the
8-camera ring absorbs most of the loss. This crown is not left empty by the withhold
specifically — it was already mostly empty (54.43%) before the withhold existed, and
the withhold's own addition to that is small.

**Per-view withhold counts** (that view's own contribution — a texel withheld here may
still be written by a different view; this is not a per-view hole count of the final,
pooled atlas, which only the pooled figure above represents):

| view | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| withheld (this view) | 4,380 | 3,607 | 1,244 | 652 | 2,299 | 3,861 | 3,720 | 2,294 |
| of head-band-accepted | 146,546 | 147,242 | 150,662 | 142,491 | 138,720 | 147,570 | 148,092 | 145,526 |
| % | 2.99% | 2.45% | 0.83% | 0.46% | 1.66% | 2.62% | 2.51% | 1.58% |

**Where the pooled 3,159 new holes sit**, by crown-to-neck fifth within the head-band
crop (0 = crown/`CY0`, 1 = neck/`CY1`), against the same bands measured on the
pre-existing baseline hole population for comparison:

| crown-to-neck band | NEW holes (n=3,159) | BASELINE holes (n=645,842) |
|---|---:|---:|
| top fifth (crown) | **1,052 (33.3%)** | 42,557 (6.6%) |
| 2nd fifth | 794 (25.1%) | 130,343 (20.2%) |
| middle fifth | 709 (22.4%) | 170,978 (26.5%) |
| 4th fifth | 71 (2.2%) | 154,644 (23.9%) |
| bottom fifth (near neck) | 533 (16.9%) | 147,320 (22.8%) |

**The new holes concentrate at the crown at roughly 5× the rate of the pre-existing
baseline population (33.3% against 6.6%)** — consistent with the kickoff's own stated
mechanism (the painted curls stick out furthest past the raycast mesh line at the
crown, "the left puff most," per E67's first sitting). `logs\remap_step7.txt`,
`remap\data\step7_new_holes_location.json`.

## Unclassified re-examination — stays drawn, re-examined, not absorbed

**Does the withhold reach any of the 18.71% (5,193 pooled) unclassified population?
No — 0 of 5,193, in every view.** Proven two ways: structurally, by the classifier's
own priority order (unclassified is only tested on "not class1, not class3," and class
3 already claims everything inside headband — so unclassified is, by construction,
entirely outside headband and outside the withhold's reach); and empirically, by the
same exact per-view set-identity check used for classes 1/2 above.

**Is it nonetheless "the same phenomenon," hair spilling just outside a hard
rectangle?** Measured by distance from each unclassified pixel to the head-band crop
rectangle, in `project_twins.py`'s own crop-space (the same space `headband[]` itself
is computed in — not a new space invented for this question). The box is
176.0×137.6 crop-space px, diagonal 223.4px.

| quantity | value |
|---|---:|
| pooled unclassified, n | 5,193 |
| min distance to box | 0.0 px |
| **median distance to box** | **306.0 px** |
| mean distance to box | 305.5 px |
| max distance to box | 811.9 px |
| within 5% of box diagonal (11.2px) | 375 (7.22%) |
| within 10% of box diagonal (22.3px) | 712 (13.71%) |
| within 25% of box diagonal (55.9px) | 1,342 (25.84%) |

The typical unclassified pixel sits **further from the head-band box than the box's
own diagonal** — mostly a different phenomenon from hair spillover, consistent with
E67's own visual read of garment-edge contamination (vest/sash hems, trouser seams,
ink-stained fingertips). A real minority sits close: 7.22% within 5% of the box's own
diagonal, and the per-view spread is uneven rather than flat — views 1 and 7 carry
29.5%/21.5% of their own unclassified population within that close band, against
0.0%/0.1% on views 5/6 (`logs\remap_step5.txt`, `remap\data\
step5_unclassified_distance.json`). Reported as measured; no widening or new rule is
proposed or implied.

## Visual evidence

Per-view overlays, E67's own visual format plus one new category (charcoal =
withheld → hole this sitting): `remap\overlays\a1_v{0..7}_e68_withhold_map.png`.
Combined before/after sheet, E67's map directly above E68's map per view, all 8 views:
`remap\sheet\E68_before_after_sheet.png` (2304×4620). Read from the images, not
judged: on every view, the amber ring that traced the hairline in E67's map no longer
appears — the same pixels are now charcoal (withheld) or simply absent (their
position becomes a hole with no marker at all, since a hole carries no colour to
classify). The magenta (unclassified) markers at sleeve cuffs and garment hems are
visually unchanged between the two rows, consistent with the measured set-identity.

## Predictions vs. outcomes, in full

| # | prediction | blind? | outcome |
|---|---|---|---|
| 1 | class3 collapses to ~0%; classes 1/2/unclassified unchanged in absolute count | CODE-DERIVED | CONFIRMED EXACTLY |
| 2 | most views pass the 2.0% limit; view 0 (and maybe view 3) flagged as at-risk of failing | BLIND | FALSIFIED — 0/8 pass, a stronger falsification than guessed; the denominator-shrinkage mechanism was not identified in advance |
| 3 | hole cost in the 15–35% range | BLIND | FALSIFIED in both directions — marginal cost (0.27%) far below the band, total rate (54.70%) far above it; the prediction conflated two different quantities |
| 4a | withhold cannot reach unclassified | CODE-DERIVED | CONFIRMED EXACTLY (0 of 5,193, set-identical) |
| 4b | most unclassified is not hair-adjacent; distance "tens of px" | BLIND (direction), BLIND (magnitude) | CONFIRMED DIRECTIONALLY; magnitude guess wrong by roughly an order of magnitude (306px median vs. "tens of px" guessed) |

Full text with reasoning: `E:\AI\training\facet_E68\logs\predictions.txt`.

## Out of scope, confirmed untouched

Remeshing the hair; regenerating the ring; loosening `--bg-max-pct` or `--bg-de` (both
verified unchanged, Gate B); starting the brush; the palette-aware probe (dead, never
touched); dilation or hole-filling (holes are left and measured, not filled); binding
(not touched, does not gate this).

## git status, verbatim

```
On branch main
Your branch is ahead of 'origin/main' by 44 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   tools/project_twins.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/experiments/E68-headband-withhold-report.md

no changes added to commit (use "git add" and/or "git commit -a")
```

`git diff --stat`: `tools/project_twins.py | 49 +++++++++++++++++++++++++++++++++++++++++++++++++` —
1 file changed, 49 insertions(+), 0 deletions. No file inside `E:\AI\facet` was touched
this session other than `tools/project_twins.py` (modified) and this report itself
(new, untracked). The 44-commits-ahead state predates this session (E67's report/map
were folded between the 39 this session's kickoff inherited and the 44 measured here).

## Artifact paths

- Live handoff: `E:\AI\training\facet_E68\handoff.md`
- Predictions + outcomes: `E:\AI\training\facet_E68\logs\predictions.txt`
- Gate 0: `logs\gate0_provenance.txt`
- Gate B assertion: `logs\gateB_threshold_assert.txt`
- Anchor (default path, non-perturbation proof): `logs\anchor_default_console.txt`
- Withheld run, joint (halts view 0): `logs\withhold_console.txt`
- Withheld run, single-view sweep (all 8, real tool, real ANDON): `logs\
  withhold_sweep_v{0..7}.txt`
- Remap validation + classification + hole cost: `logs\remap_step0_2.txt`,
  `logs\remap_full.txt`, `remap\data\step3_4_results.json`
- Unclassified distance: `logs\remap_step5.txt`, `remap\data\
  step5_unclassified_distance.json`
- New-hole spatial location (crown-to-neck bands): `logs\remap_step7.txt`, `remap\data\
  step7_new_holes_location.json`
- Overlays: `remap\overlays\a1_v{0..7}_e68_withhold_map.png`
- Combined before/after sheet: `remap\sheet\E68_before_after_sheet.png`
- Code diff: `tools/project_twins.py` (uncommitted, in place; `git diff -- tools/
  project_twins.py` for the literal patch)
- Working scripts (scratchpad copies): `C:\Users\mikey\AppData\Local\Temp\claude\
  E--AI-facet\428295a0-ff4d-49f0-b0a2-024d00acf529\scratchpad\` — `e68_gate0.py`,
  `e68_gateB_assert.py`, `e68_remap.py`, `e68_remap_part2.py`, `e68_remap_part3.py`

## Role discipline

No quality judgment is offered anywhere above. The 0/8 pass result is reported exactly
as measured, with the mechanism traced to the texel and the limit never touched — per
charter, a failing result is reported and halted on, not tuned past. Every class-share
and hole-cost number is reported with both its old and new value, not just a
flattering one. Predictions were logged before any computation and the outcomes
section states plainly where each one was wrong, including the two ways the hole-cost
prediction was wrong at once. No memory write was made. No git commit was made
(`tools/project_twins.py` sits modified, uncommitted, for the advisor to fold by
pathspec). No child agent was used for core work — the remap's own validation gate
(32/32 exact matches against the real tool's console, 8/8 classification reproductions
exact against E67's own summary table) stands in place of a second seat.
