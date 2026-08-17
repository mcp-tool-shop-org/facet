# E50 report — the polygon class: is the fill pass the carrier?

Executor seat (Sonnet tier), dispatched 2026-08-17 on
`docs/experiments/E50-polygon-class-overlay-kickoff.md`. Work tree:
`E:\AI\training\facet_E50\` (`handoff.md` kept current throughout; full
step-by-step record there). No repo commits; this report is the only repo
file this seat writes. Python: `E:\AI-Models\trellis2-env\Scripts\python.exe`
throughout — no GPU, no cloud spend, no Blender.

No word below asserts that any result is good, working, or decisive. Every
number is a measurement. Per a coordinator instruction received mid-task,
this report paraphrases the design record in this seat's own words rather
than quoting it — the underlying record (`docs/experiments/E49-finish-and-
cap-kickoff.md`) carries the exact wording if needed.

## 1. The question and the answer, stated first

The E49 dispatch record raised a hypothesis after that arc's renders were
reviewed: this arc's own fill repairs (orphan island fill from source, or
within-island nearest-neighbour fill) might be painting the small flat-
coloured, angular-boundary patches visible in several garment regions. This
seat measured that hypothesis four independent ways. **All four point the
same direction, away from the hypothesis:**

1. Two confirmed real instances of the patch defect (found by direct visual
   inspection, cross-checked against the reference twin image), read
   through the anchored provenance lookup, sit 90.0–99.1% on ordinary
   directly-painted texels (`written`) and 0.9–10.0% on within-island fill
   (`filled`); 0% on orphan fill; 0% on no-view-visible, in both paint modes.
2. A whole-image automated scan (169 total flagged pixels out of 2,028,512
   figure pixels across all 16 view/mode cells, using a detector calibrated
   directly against the E49 dispatch's literal specification) put 100% of
   what it found on `written`, 0% on any fill-derived class.
3. A second, broader automated scan (96,218 flagged pixels, disclosed as
   over-inclusive — see §6) found `filled` barely above its own base rate
   (1.18x) and `orphan_fill` *below* its own base rate (0.27x, i.e.
   under-represented among flagged pixels, not over-represented).
4. The confirmed defect is already present in the pre-E49 baseline render
   (`renders_flat/final_0.png`, rendered from an atlas built before
   `orphan_fill.py` or this arc's erosion-cap repair existed as code). A
   repair cannot be the cause of a defect that predates the repair.

**A negative result for the fill-pass hypothesis, reported as a full
outcome, not a partial one.** The defect's origin sits upstream of this
entire arc, in whatever painted these particular texels during the base
per-texel scatter step (`atlas_from_aovs.py`'s own view-selection), common
to every arc since the source AOV bundle was built — not in either of E49's
two repairs.

## 2. Predictions (written before the real 16 renders were measured — full
text in `predictions.md`)

Blind status: NOT blind to base rates (a necessary partition-completeness
step, computed before the detector ran — disclosed in `predictions.md`) or
to Gate C's calibration (also computed first). Blind to what the detector
would return on the real renders.

| | P1 — detector fires at all | P2 — which class over-represented | P3 — orphan_fill raw count | P4 — no_view_visible hue split | P5 — unmapped |
|---|---|---|---|---|---|
| predicted | YES, ≥1 view/mode | `filled`, enrichment 2x–10x | small (single digits–low tens), NOT a clean negative given predicted instrument blind spot | concentrated in the magenta-hued population, ~0 outside it | ~base rate, no enrichment |
| measured | YES (169px, 4/16 cells) | v1: 0.00x. v2: 1.18x. Direct instances: `filled` share of the 3 confirmed components is 0.9%/10.0%/4.0% against `written` at 99.1%/90.0%/96.0% — `written` dominates every one | v1: 0. v2: 21 (inside the predicted band) | 181/183 = 98.9% magenta-hued (2 non-magenta px total) | **11.58x — the strongest enrichment of any class** |
| result | confirmed | **miss** — measured enrichment is at or below 1x in every quantification, not 2x–10x | inside predicted band, but see §5 — this report's conclusion rests on the (unpredicted) direct-instance check, not on the raw count | confirmed | **miss** — largest enrichment found, opposite of predicted |

Every enrichment prediction was checked against the reachable interval
`[0, 1/base_rate]` before being written (`predictions.md` §"Reachable-
interval check") — none of the measured values in the table above falls
outside what the instrument could in principle return; P2 and P5 are
ordinary misses, not out-of-band predictions.

## 3. Gate A — shapes agree (PASS)

`gate_a_shapes.py` → `gate_a.log`, `gate_a_report.json`. Recomputed from
scratch, not inherited from the E49 report's own account:

- AOV shape `(1024, 752)` int32, C-contiguous, uniform across all 8 views.
  Render shape `(1024, 752, 4)` matches exactly, both modes, all 8 views —
  the `mask.flat[surfid]` lookup this whole seat depends on is shape-legal.
- Atlas resolution 4096×4096 confirmed both modes, matches the prep mask's
  own shape (the formula `row*4096+col` assumes this).
- The 4-way partition (`written` / `filled` / `orphan_fill` /
  `no_view_visible`) over the prep mask's `valid` set is pairwise disjoint
  and exhaustive in ATLAS space, recomputed independently: owner
  1,985,599 / 300,187 / 5,199 / 111,825; blend 1,705,558 / 431,303 /
  132,152 / 133,797 — reproduces the E49 report's own numbers exactly.
- **A premise correction, found here, not inherited**: `surfid != -1` (the
  raycast-based, geometry-only silhouette, copied unchanged from E45 by
  every erosion pass) is a strictly larger set than `aov_eroded/sil.npy`
  (the eroded, painting-visibility silhouette) — 8,542/8,229/6,556/6,329px
  larger per view-group (v0–3), matching E49's own erosion table exactly.
  **The render's actual figure/background boundary is `surfid != -1`, not
  the eroded `sil.npy`** — conflating the two would have measured the wrong
  object for every step downstream. Used `surfid != -1` throughout.

## 4. Gate B — the lookup is anchored

`gate_b_anchor.py` (v1, FIRED) → `gate_b_v2_hue_oracle.py` (v2, PASS).

**v1 (raw-RGB exact-magenta oracle) fired.** Premise: `no_view_visible`
atlas texels are untouched by every paint step (Gate A's partition check
confirms this), so they must still carry the scatter() sentinel
`[255,0,255]` in `atlas_complete.png` (checked true, 0 exceptions, both
modes — a fact about the atlas alone) — so a view pixel whose `surfid`
lands there should render close to magenta. Measured: the CORRECT
row-major convention scored only 0–16.7% exact-magenta agreement
(tolerance ±6) across all 16 view/mode cells; WRONG conventions
(transpose/vflip/hflip) scored similarly low. Gate fired at the
pre-registered 90% floor. Diagnosed before any retry, from direct
evidence: `renders_flat/render_atlas_swap.py` wires the atlas into a
Principled BSDF's Base Color under a Standard view transform — a lit
render, not a raw texel passthrough. A direct sample of 158 predicted
pixels (owner view 0) showed mean RGB (233.8, 41.8, 231.0) — R≈B≫G in
every sample, hue preserved, magnitude/saturation shaded by scene
lighting. v1 compared an unlit texel colour to a lit render pixel-for-
pixel; that is a bug in the test's construction, not evidence about the
lookup.

**v2 (hue+chroma-floor oracle, corrected for the render's documented
shading pipeline): PASS.** Hand-rolled `rgb_to_hsv` self-checked against 5
known colours first (exact). Hue band (±25° around magenta's 300°) and
floors (S≥0.15, V≥0.12) fixed from general colour reasoning before the
wrong-convention numbers were seen. Result: the CORRECT convention scored
96.15–100.00% magenta-hued agreement across all 16 view/mode cells (mean
98.88%); WRONG conventions scored 0.14–6.66% (mean 2.00%). Smallest
per-view margin between the correct convention and any wrong one: 89.49
percentage points. **`mask.flat[surfid[sil]]` (row-major, `sil = surfid !=
-1` guard against the -1-wraps-to-last-element trap) is the anchored
lookup used everywhere after this point.**

## 5. Gate C, the detector, and the mid-course correction

### 5a. v1 — literal specification, synthetic-only calibration: PASSED its
own gate, then found miscalibrated against real content

`detect_patches.py` (local flatness in a 5×5 window + global colour
constancy + `cv2.approxPolyDP` vertex-count angularity) calibrated by
`calibrate_and_gate_c.py` against synthetic flat shapes (a triangle and a
matched-area circle, 2D-painted onto a copy of a real render, zero internal
variance) versus a real textured-negative crop. Two internal corrections
happened before this gate passed (both are in `calibrate_and_gate_c.py`'s
own docstring, left visible rather than silently rewritten): the raw
calibration statistics were first measured over each shape's *whole* drawn
area, which is dominated by edge-contaminated pixels for a shape this
small (53% of a 340px triangle sits within 2px of its own boundary,
measured directly) — fixed to measure true-interior pixels only. The
resulting pass bar ("detect ≥50% of the shape's *total* area") then fired
at 47.1%, which is *above* the shape's own reachable ceiling (its
interior/total ratio) — fixed to gate on true-interior recovery (reached
100%) instead. **Gate C v3 PASS**: thresholds `local_eps=0.0203`,
`global_std_max=0.0070`, `k_max=3`; 100% interior recovery on the synthetic
triangle, 0% on the matched-area circle (angularity alone rejects it,
k=8>3), 0% on a real textured crop, 0% over-fire on a whole unmodified
figure.

Run on the real 16 renders (`cross_tabulate.py`): **169 total pixels
detected out of 2,028,512 figure pixels (0.0083%), all 16 cells combined.
100% of that on `written`. 0% on `filled`, `orphan_fill`, `no_view_visible`,
`unmapped`.** Full per-view table in `cross_tab_report.json`.

### 5b. Before trusting near-total silence as the answer: direct visual
inspection

The E49 sheets the record describes reviewing carry no tabard/skirt/boot
crop rows at all (`s3_sheet_regions.json` only ever had blade/grip boxes),
so this seat cropped the actual `owner_complete_0.png` / `blend_complete_
0.png` files directly at 4–8x zoom. A plainly-visible, small, flat-ish
angular patch of anomalous colour (olive-khaki, plus an adjacent tan/gold
one) was found at the collar/chest seam, bbox roughly y500–524, x300–344 —
compared directly against `aov_eroded/view_0/twin.png` (the reference) at
the same coordinates, which shows clean, uninterrupted tunic fabric with
nothing there (`lookaround/reference_v0_collar.png` vs `lookaround/
owner_v0_collar_compare.png`). This confirms the patch is a genuine
artefact, not an intentional design element.

Measured directly: its true-interior 5×5 colour spread runs mean 8.4–23.7
across its two components — three orders of magnitude above v1's
calibrated `local_eps` of 0.0203. The synthetic calibration shape (flat
2D paint, zero internal variance) did not represent a real patch's own
shading gradient under the same Blender lighting as everything else — the
same failure shape as Gate B v1 (an idealized proxy standing in for a
physically-shaded quantity), found the same way: direct measurement of a
real instance before trusting a synthetic-only calibration.

### 5c. The direct provenance check — the strongest evidence in this report

Bypassing the detector-calibration question entirely: the two confirmed
patch components (349px, 239px, owner mode; a merged 674px component at
the identical UV location in blend mode) were segmented directly (colour
distance from a sampled clean-tunic reference pixel, components ≥100px)
and read through the same anchored lookup as everything else.

| component | mode | area | written | filled | orphan_fill | no_view_visible |
|---|---|---|---|---|---|---|
| collar patch 1 | owner | 349px | 99.1% | 0.9% | 0% | 0% |
| collar patch 2 | owner | 239px | 90.0% | 10.0% | 0% | 0% |
| collar patch (merged) | blend | 674px | 96.0% | 4.0% | 0% | 0% |

Three segmented components (two in owner mode, one merged component at
the identical UV location in blend mode), one consistent answer: the
confirmed real defect sits overwhelmingly on ordinary painted texels, with
a small minority on within-island fill and none on orphan fill.

### 5d. Angularity does not survive real content — measured, not assumed

To check whether the angularity gate (v1) could discriminate a real
angular defect from a real round/organic region (not just a synthetic
one), a specular-highlight blob on the gold pauldron was segmented the
same way as the real patch and run through the same `cv2.approxPolyDP`
routine. It scored k=8 — indistinguishable from the confirmed defect
patches' own k=9 and k=13. An alternative shape statistic (isoperimetric
compactness, `4·π·Area/Perimeter²`) ranked the highlight blob *less*
circular (0.023) than either real defect patch (0.17, 0.26) — a real
specular highlight on curved gold geometry forms an elongated streak, not
a compact blob. Antialiasing and gradient blending erase the crispness
either shape statistic needs at this render's resolution. This is reported
as a measured limitation of the instrument, not silently worked around.

### 5e. v2 — a broader, disclosed-as-over-inclusive automated scan

`detect_patches_v2.py`: colour distance from an 11px-radius per-channel
median-filtered local context, connected component, a 30px mechanical
floor, **no angularity gate** (justified by §5d — none tested
discriminates on real content). `dist_thresh=40` chosen from a measured
sweep against the confirmed real patch versus the textured-negative crop:
27.2% of real-patch pixels exceed it versus 2.8% of ordinary-texture
pixels — not a clean separation (disclosed, not hidden), but a real,
roughly 10x per-pixel enrichment that connected-component + size-floor
turns into a usable, if broad, candidate set.

Run on the real 16 renders (`cross_tabulate_v2.py`):

| class | overlap px | coincidence rate | base rate | enrichment |
|---|---|---|---|---|
| written | 87,018 | 90.44% | 96.996% | 0.93x |
| filled | 2,558 | 2.659% | 2.259% | 1.18x |
| orphan_fill | 21 | 0.022% | 0.0821% | **0.27x** |
| no_view_visible | 183 | 0.190% | 0.0860% | 2.21x (see below) |
| unmapped | 6,438 | 6.691% | 0.5777% | **11.58x** |

Total detected: 96,218 / 2,028,512 px (4.74% of the whole figure,
aggregated across all 16 cells) — this figure is a broad candidate count,
not a defect count; it includes legitimate material-boundary halos and
genuine specular highlights that §5d showed are not shape-separable from
the phenomenon in question.

The `no_view_visible` overlap splits 181/183 (98.9%) magenta-hued by Gate
B v2's own hue+chroma test — the already-documented sentinel artefact
(E49 report §8c), not the flat-colour defect class in question. Only 2
non-magenta pixels, out of 2,028,512 total figure pixels across all 16
cells, coincide with `no_view_visible`.

**`unmapped`** (view pixels whose `surfid` lands on an atlas texel outside
the prep mask's own `valid` region — found while building base rates,
§7 — not one of the classes this dispatch names) shows the strongest
enrichment of any class, 11.58x. A spatial spot-check (view 0) found only
124/1,154 (10.7%) of all `unmapped` pixels sit within 5px of the outer
silhouette rim — the population is concentrated in the figure's interior,
not an antialiasing-at-the-edge artefact. Not investigated further —
outside this dispatch's scope, which is specifically the two fill-repair
classes — but flagged here as a third, previously unnamed candidate
mechanism, measured but not chased.

### 5f. The temporal check — independent of every provenance class above

`E:\AI\training\facet_E08\ARMB\out\renders_flat\final_0.png` is the
pre-E49 baseline render (E47/E48's atlas, rendered before `orphan_fill.py`
or this arc's erosion-cap repair existed as code). At the exact same
collar coordinates, **the same olive-green angular patch is already
present** (`lookaround/shipped_v0_collar_compare.png`). This is a
temporal argument, independent of and stronger than any provenance-class
reading: a repair cannot be the cause of a defect that already existed
before the repair's own code was written. The reference twin image at the
same coordinates is clean (§5b) — so the defect enters the pipeline
between the reference and the first atlas paint step, nowhere near
either of this arc's two repairs.

## 6. Base rates (view-space pixels, not atlas-space texels)

Computed per view per mode (`compute_base_rates.py` → `base_rates.json`)
as an exhaustive 5-class partition, exactly matching the figure pixel
count in every one of the 16 cells (checked, not assumed). Aggregate
across all 16 cells:

| class | figure-pixel share |
|---|---|
| written | 96.996% |
| filled | 2.259% |
| orphan_fill | 0.0821% |
| no_view_visible | 0.0860% |
| unmapped | 0.5777% |

These are RENDER-SPACE shares. They are not comparable to the atlas-space
texel counts in §3 or in the E49 report — a texel is a variable amount of
screen area from view to view (per this repo's own standing law that a
share in one space is not a claim about another).

## 7. A population found while building this partition, not part of the
original hypothesis

Projecting the 4 provenance classes into view space (needed to compute
base rates honestly) initially failed to sum to the figure pixel count —
1,154 of view 0's 146,356 figure pixels were short. Traced directly: those
pixels' `surfid` lands on an atlas texel the prep mask's own `valid` array
does not include. `surfid` is computed by a per-view raycast
(`emit_view_aovs.py`); `valid` is a property of a separate prep-mask
pipeline — the two need not agree everywhere, and measurably do not on
0.39–0.79% of each view's figure. Added as a 5th class, `unmapped`, rather
than silently folded into an existing one; carried through every
downstream measurement in this report (§5e, §6).

## 8. The sheets

`E:\AI\training\facet_E50\sheets\e50_sheet_v00.png` … `v07.png`, one per
view, 2438×3546 each. Per view: owner render | owner provenance overlay
(blue=filled, red=orphan_fill, cyan=no_view_visible, yellow=unmapped) |
owner detected overlay (green=v1 flat+angular, orange=v2-only colour-
anomaly), then the same row for blend mode, then 2x crop rows (render |
provenance | detected) on the confirmed collar patch, a belt/tassel
region, and a boot region — the same fixed pixel box on every view, so a
pose-dependent shift is visible rather than re-centred to hide it.

## 9. Deviations / halts

Two gates fired and were diagnosed before any retry, per the standing
rule against improvising past a fired gate:

- **Gate B v1** (§4) — fired on a test-construction bug (unlit-vs-lit
  colour comparison), not on the lookup. Diagnosed from the render
  script's own shader graph and from direct pixel sampling before
  building v2. v2 passed cleanly and is the anchor used throughout.
- **Gate C** (§5a) — fired twice, both times on this seat's own
  calibration-script construction (edge-contaminated statistics, then a
  pass bar set above the shape's reachable ceiling), never on the
  detector's core arithmetic (confirmed directly: a true-interior pixel of
  the synthetic shape measured local-spread ~4.7e-6, matching expectation
  exactly). Both diagnosed from direct measurement before any parameter
  was retuned toward a desired outcome.

No gate fired on the real 16-render measurement itself. The near-zero v1
result (§5a) was investigated rather than reported as-is (§5b–5f) — not a
fired gate, but the same discipline: a surprising number was checked
against direct evidence before being treated as the answer.

## 10. Artifacts

All under `E:\AI\training\facet_E50\`:

```
handoff.md                       live working record, kept current throughout
predictions.md                   written before the real 16-render run
gate_a_shapes.py, gate_a.log, gate_a_report.json
gate_b_anchor.py, gate_b.log     v1, fired
gate_b_v2_hue_oracle.py, gate_b_v2.log, gate_b_v2_report.json   v2, pass
recon_component_sizes.py, recon_component_sizes.log            calibration sizing recon
compute_base_rates.py, base_rates.log, base_rates.json
detect_patches.py                v1 detector (flatness+angularity)
calibrate_and_gate_c.py, gate_c.log, calibration_report.json, calib_synth_render.png
cross_tabulate.py, cross_tab.log, cross_tab_report.json         v1 real-data run
detect_patches_v2.py             v2 detector (colour-anomaly only)
cross_tabulate_v2.py, cross_tab_v2.log, cross_tab_v2_report.json  v2 real-data run
lookaround/                      reference/shipped/owner/blend comparison crops
sheets/e50_sheet_v00..07.png     the deliverable sheets
```

`git status --short` in the repo confirms this report is the only tracked
change from this seat; nothing else was committed, pushed, or written to
the memory store.
