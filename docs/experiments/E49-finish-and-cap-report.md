# E49 report — finish the candidate: orphan fill from source, erosion at its stated floor

Executor seat (Sonnet tier), dispatched 2026-08-16 night at HEAD
`acac4aa7472d062286b8d6ac00227458b1eed224`, on the Director's direction to finish it
after E48, which he judged a clear step up with room to go further.
Dispatch: `docs/experiments/E49-finish-and-cap-kickoff.md`. Full working
record: `E:\AI\training\facet_E49\handoff.md` (kept current through every
step) and `E:\AI\training\facet_E49\predictions.md` (written before step 1
ran). **git HEAD moved during this run**, to `bf7662e4909daa6cdfe6105cbc11b5ae9970ad11`
— `git status --short` is clean (nothing of this seat's landed outside the
training dir before this report), and the diff between the two HEADs touches
only the E49 kickoff's own "Dispatch record" section (21 lines appended,
recording three Director rulings from a parallel consult track and
confirming this arc's completion is a prerequisite for follow-on canon work)
plus an unrelated `docs/index/facet.db` refresh — no change to this arc's
"two repairs" / "Rules" / "Standards compliance" sections. This report is
written against HEAD bf7662e4.

No word below asserts that any result is good, working, or decisive. Every
number is a measurement; the sheets under `E:\AI\training\facet_E49\sheets\`
are the artifact for the Director's eye.

## 1. Predictions (written before step 1 ran — full text in predictions.md)

Blind status: blind with respect to every number this arc's own scripts
would produce (none existed when `predictions.md` was written). Not blind to
E48's own recorded numbers (its per-band table, its 5.053%/11.959%
pre-orphan-fill sentinel shares, its island-11915 observation), named at the
point of use in `predictions.md`.

| | P1 — erosion per-band loss at the flat 2.5px floor | P2 — remaining-sentinel share after orphan fill |
|---|---|---|
| predicted | 2-4px: EXACT match to E48 (analytic certainty); 4-8px/8-16px/16-32px/32+px: per-view-group bands derived from an approximate proportionality heuristic, disclosed as approximate | owner: 0.05%-1.5% of valid (2,400-36,000 texels); blend: 0.15%-3.0% of valid (3,600-72,000 texels); no-view-visible count == the remaining-sentinel count |

## 2. What ran

| step | tool | result |
|---|---|---|
| Gate S | `tools/atlas_from_aovs.py --selftest` | `atlas_from_aovs selftest OK  calibration atlas[16,16,0] == 0.5`, exit 0 |
| Gate S | `--anchor --aov facet_E45\aov --prep facet_E06\C1\prep` | `\|bmid\|=0.000e+00 \|v_ext\|=0.000e+00 \|h_ext\|=0.000e+00 valid=2402810`, exit 0 |
| (extra) | `s3_composite.py --selftest`, `s3_sheet.py --selftest` | both OK, exit 0 (not a required gate — an extra confidence check on two modules this arc's new tools import and rely on) |
| Step 1 | `erode_bundle_capped.py` (training dir) — repair 2 | exit 0, derived bundle written, E45 source hash-confirmed unchanged |
| Step 2 | `atlas_from_aovs.py` × {owner, blend}, flow off | both exit 0 |
| Step 3 | `fill_islands_e49.py` (training dir, E48's algorithm re-pointed) | both exit 0, boundary/accounting checks clean |
| Step 4 | `orphan_fill.py` (training dir) — repair 1, new | both exit 0, accounting checks clean |
| Step 5 | `facet_E47\render_atlas_swap.py` (unmodified, reused directly) via Blender `-b -P`, PowerShell, atlas = `atlas_complete.png` | both exit 0, 16 renders |
| Step 6 | `build_sheets_e49.py` (training dir) | exit 0, 8 sheets, no missing panels |

Gate S matches E48's recorded precedent exactly (`|bmid|` 0.000e+00,
valid-texel count 2,402,810).

## 3. Step 1 — erosion at its stated floor (repair 2, `erode_bundle_capped.py`)

E48's own `ed_body` was `max(edge_floor=2.5, edge_dist=7.0*esc)`, measured
2.79-4.17px per view (an escalation term). This repair removes that term
entirely: `ed_body = 2.5` (flat), `e_img = min(ed_body, edge_frac*thick)`
otherwise unchanged in form. `esc`/`edge_dist`/`edge_ref` are still computed
and reported for context but no longer feed `ed_body`. Cited from E48's
`erode_bundle.py` (sha256 `27fa5bb8f56fd71e21e5b191861816efeec5212285766210ffbba689f8e88200`)
for structure; the one formula change is the whole of this repair.

**Analytic consequence, checked before any data ran (predictions.md):**
since `2.5 < 2.79` (E48's own smallest `ed_body`), the new `e_img` is `<=`
E48's everywhere, with EXACT equality wherever `thick/3 <= 2.5`, i.e.
`thick <= 7.5px` — view-independent. This makes the 2-4px band's loss% a
mathematical certainty to reproduce E48's own number exactly, not a genuine
prediction; it is scored anyway in §9.

**Per-view result** (sil px before → after; `ed_body` is now flat 2.5px in
every view, was 2.79-4.17px in E48):

| view | fig_w | ed_body (E49 / E48) | sil before → after | removed | removed % (E49 / E48) |
|---|---|---|---|---|---|
| 0 | 388px | 2.50 / 3.88px | 146,356 → 137,814 | 8,542 | 5.84% / 8.92% |
| 1 | 417px | 2.50 / 4.17px | 149,780 → 141,551 | 8,229 | 5.49% / 10.08% |
| 2 | 279px | 2.50 / 2.79px | 90,553 → 83,997 | 6,556 | 7.24% / 7.24% |
| 3 | 304px | 2.50 / 3.04px | 120,439 → 114,110 | 6,329 | 5.25% / 6.98% |
| 4-7 | (mirror 0-3) | | | | |

View 2 (and its pair, view 6) show **zero change** from E48 — its own old
`ed_body` (2.79px) was already the closest to the new flat floor.

**Per-band loss, E49 vs E48** (`edge_min_struct=50` floor; identical across
paired views; full 8-view table in `aov_eroded/erosion_manifest.json`,
carrying both arcs' numbers side by side, computed by the same script, not
hand-copied):

| band | v0/v4 (E49 / E48) | v1/v5 (E49 / E48) | v2/v6 (E49 / E48) | v3/v7 (E49 / E48) |
|---|---|---|---|---|
| 1-2px | SKIPPED (n<50), both | SKIPPED (n<50), both | SKIPPED (n<50), both | SKIPPED (n<50), both |
| 2-4px | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% |
| 4-8px | 54.40% / 54.40% | 63.80% / 63.80% | 28.60% / 28.60% | 58.14% / 58.14% |
| 8-16px | 30.60% / 41.68% | 29.13% / 43.09% | 19.18% / 19.18% | 24.61% / 32.32% |
| 16-32px | 14.15% / 21.14% | 12.42% / 22.79% | 15.84% / 15.84% | 23.75% / 30.90% |
| 32-infpx | 2.74% / 4.77% | 2.59% / 5.47% | 3.17% / 3.17% | 2.46% / 3.43% |

The 2-4px AND 4-8px bands reproduce E48's own numbers exactly in every view
(not just similarly — bit-for-bit identical percentages). 8-16px and 16-32px
show meaningful drops on views 0/1/3 (and their pairs) and zero change on
view 2/6. No band's loss went to zero and no band's loss increased in any
view.

`E:\AI\training\facet_E45\aov\` hash-confirmed unchanged, 81 files, before
=== after (`erode_bundle_capped.py`'s own ANDON, not fired). No view's
silhouette went to empty (the empty-silhouette ANDON did not fire).

## 4. Step 2 — paint (`atlas_from_aovs.py`, flow off, both modes)

| cell | mode | written / valid | pct | vs E48 | vs E47 (uneroded) |
|---|---|---|---|---|---|
| atlas_owner_eroded | owner | 1,985,599 / 2,402,810 | 82.63% | +0.87pt (81.76%) | −1.76pt (84.39%) |
| atlas_blend_eroded | blend | 1,705,558 / 2,402,810 | 70.98% | +1.17pt (69.81%) | −2.55pt (73.53%) |

Both sit between E48's more-eroded coverage and E47's uneroded coverage, as
expected from a smaller erosion cap.

## 5. Step 3 — within-island fill (`fill_islands_e49.py`, E48's algorithm re-pointed)

Same algorithm as E48's `fill_islands.py` (cited by sha256
`6558296bad30a8fd64fc10b7c81c3b384c2be003d92f94ede995976999bfdd18`,
recorded in `fill_islands_e49.py`'s own manifest field
`cites_e48_fill_islands_py_sha256`), re-pointed at this arc's own
`atlas_{owner,blend}_eroded`. Same islands source
(`facet_E08\ARMB\cache\isl_grid.npy`, 18,915 ids, 11,600 with a bbox at this
resolution — unchanged, this arc did not re-derive it), same premise
cross-check at runtime (not just inherited from E48's recon).

| | owner | blend |
|---|---|---|
| written before fill (step 2) | 1,985,599 | 1,705,558 |
| unwritten-valid before fill | 417,211 | 697,252 |
| islands: no fill needed | 7,208 | 4,639 |
| islands: filled | 2,647 | 3,490 |
| islands: **zero-written** | **1,745** | **3,471** |
| texels filled | 300,187 | 431,303 |
| zero-written-island total area | 117,024px | 265,949px |
| zero-written-island largest | 2,819px (island 11915) | 2,819px (island 11915, same id) |
| remaining sentinel (pre-orphan-fill) | 117,024 / 2,402,810 = **4.870%** | 265,949 / 2,402,810 = **11.068%** |
| E48's equivalent (different erosion, no orphan fill existed) | 5.053% | 11.959% |

Boundary-crossing ANDON checked 300,187 (owner) / 431,303 (blend) filled
texels — none crossed. Accounting ANDON (remaining sentinel must equal
zero-written-island total area) held exactly in both modes. The largest
zero-written island is again id 11915 (2,819px) in BOTH modes — same id, same
size as E48 found, unaffected by the lighter erosion cap, consistent with a
region no view's visibility test reaches regardless of erosion depth or mode.

## 6. Step 4 — orphan fill (repair 1, `orphan_fill.py`, new)

**Mechanism, per the kickoff verbatim.** For every texel of a zero-written
island (the "orphan set" — exactly step 3's remaining-sentinel set): project
into all 8 views using the position/normal already decoded for the atlas,
score each view by `facing^6` (`S.facing_of`, `exponent=S.DEFAULT_ALPHA=6.0`)
among the views where `S.sample_view` (imported, not reimplemented) reports
`valid = tap & z_ok` under the **ORIGINAL E45 UNERODED bundle** (loaded
directly via `s3_run.load_bundle(facet_E45/aov)`, no `--flow-dir` — this is
not an approximation of "uneroded," it IS the uneroded bundle, since erosion
in this repo only ever touches `sil.npy` and copies every other per-view
file unchanged from this same E45 source). Argmax wins; its twin colour is
sampled and written. A texel passing visibility in NO view stays sentinel.

**Never fills from neighbouring texels — eliminated by construction, not
merely avoided.** `orphan_fill.py` contains no atlas-space distance
transform and no atlas-space neighbour lookup anywhere; the existing atlas
array is read only as the base canvas to paste newly-sourced colour onto,
never as a colour source. Every written colour originates from one of the 8
views' own `twin` array via `sample_view`'s bilinear sample. The island-blind
flood — the documented dark-mark mechanism — stays dead; this tool does not
implement anything resembling it, even restricted to one island.

**Measured, and this arc's prediction MISSED substantially:**

| | owner | blend |
|---|---|---|
| orphan set (= step 3's remaining sentinel) | 117,024 (4.870% of valid) | 265,949 (11.068% of valid) |
| orphan-filled | 5,199 (4.44% of orphan set) | 132,152 (49.69% of orphan set) |
| **NO-VIEW-VISIBLE (final sentinel, counted loudly)** | **111,825 (95.56% of orphan set, 4.6539% of ALL valid texels)** | **133,797 (50.31% of orphan set, 5.5684% of ALL valid texels)** |
| predicted band (of all valid) | 0.05%-1.5% | 0.15%-3.0% |
| result | **MISS — measured 4.65%, >3x the predicted ceiling** | **MISS — measured 5.57%, ~1.9x the predicted ceiling** |

Orphan fill still helps relative to no-orphan-fill-at-all — owner
4.870%→4.654%, blend 11.068%→5.568% — but nowhere near the near-total
recovery the prediction reasoned toward.

**Mechanism for the miss, offered as a hypothesis consistent with the
numbers, not independently confirmed further.** The prediction's central
assumption — that most zero-written-island texels are erosion-BOUNDARY
artifacts, recoverable by relaxing `sil` alone — looks wrong for OWNER mode
specifically. `sample_view`'s `valid = tap & z_ok` has two independent
gates: `tap` (which erosion affects, through `sil`) and `z_ok` (the
depth/occlusion test, which erosion never touches — identical whether `sil`
is eroded or not). For an owner-mode texel to be zero-written, all 8 views,
spaced 45 degrees apart, must fail `tap & z_ok` under the ERODED sil —
already the loosest owner bar (any one valid sample suffices for "written").
Relaxing to the fully uneroded `sil` only rescues the ones whose failure was
specifically a `tap`/sil-boundary matter; a texel failing `z_ok` in all 8
views (self-occlusion the camera rig cannot reach from any of the 8 fixed
angles — candidates named by shape, not confirmed per-texel: underside of a
foot, inside a closed fist, deep between overlapping cloth folds) is
untouched by this repair, in any mode, by construction. 95.56% of owner's
orphan set behaves exactly like that population.

Blend's much higher 49.69% recovery is a DIFFERENT mechanism, not a
rebuttal of the above: blend's own "written" bar is strictly harder than
owner's (`acc_w > 0`, not "any valid sample" — `atlas_from_aovs.py:238-245`),
so blend's pre-orphan-fill unwritten set contains texels that already pass
`tap & z_ok` in the eroded bundle (i.e. ARE geometrically visible) but were
excluded from blend's "written" tally because every passing view's
`border*facing^alpha` weight rounded to ~0 (grazing/edge-on incidence).
`owner.npy` (loaded identically by `fill_islands_e49.py` and this tool) was
re-checked against `atlas_from_aovs.scatter()`'s own `keep = painted["written"]`
gate to confirm this is not a code inconsistency — it is not; each mode's
`owner.npy` correctly encodes that mode's own written bar. Orphan fill's
facing^6-ALONE selection (no weight floor, the kickoff's own literal wording)
trivially recovers these already-visible-but-zero-weight texels, which is
why blend recovers roughly 10x owner's rate. The SELECTION formula
(facing^6 alone vs the main pipeline's border-weighted score) has NO effect
on the no-view-visible COUNT — that count is fixed entirely by
`samp["valid"]`, before either scoring formula is applied — so the miss is
not an artifact of which scoring rule the kickoff specified.

Per-view diagnostic (owner): PASS (valid under uneroded sil, pre-argmax) =
`[379, 633, 3359, 1101, 470, 901, 384, 657]`; WON (argmax winner) =
`[173, 444, 2712, 297, 200, 517, 283, 573]` — view index 2 alone won over
half of owner's 5,199 recoveries. Blend per-view WON:
`[26164, 23952, 19822, 15471, 9491, 21996, 4149, 11107]`. Full manifests:
`atlas_{owner,blend}_eroded/orphan_fill_manifest.json`,
`orphan_fill_summary.json`.

Accounting: `orphan_filled + no_view_visible == orphan set` held exactly in
both modes (own ANDON, did not fire). `orphan_fill_mask` never overlaps
`filled_mask` or `written` (own ANDON, did not fire).

## 7. Step 5 — render (`facet_E47\render_atlas_swap.py`, reused unmodified)

Invoked directly by path (sha256
`8529a74de737d825227f5309f7c6e28dd08ac08178f2039ab83da6d2de793edd`, unchanged
from E47/E48) via Blender `-b -P`, through PowerShell. Both invocations
targeted the shipped `facet_E08\ARMB\out\W3_final.glb` with `--atlas` pointed
at `atlas_complete.png` (the orphan-filled atlas, not `atlas_filled.png`).
Both runs reported the same swap line as E47/E48's own runs: `atlas_final
(4096,4096) -> atlas_complete.png (4096,4096) colorspace='sRGB'`.

16 PNGs written (`renders_owner_complete/owner_complete_{0..7}.png`,
`renders_blend_complete/blend_complete_{0..7}.png`), counted complete
(`Get-ChildItem ... .Count`, not a truncated listing: 8 + 8). Spot check,
view 1 both sets: (1024,752,4) uint8, mean≈170.0, std≈59.3-59.8, full 0-255
range — matches E48's own spot-check pattern closely.

## 8. Step 6 — the sheet (`build_sheets_e49.py`)

8 sheets, one per view, at `E:\AI\training\facet_E49\sheets\sheet_v00..07.png`:
`reference | shipped | owner-complete | blend-complete`, native 752×1024
panels, provenance captions with sha256 for every panel. Views 0, 1, 2, 7
additionally carry region-crop rows at 2x zoom.

### 8a. The head-crop box — two rows, both shown

The kickoff's literal words: *"derive the head box from the figure's top
quarter of the eroded sil instead"* (of E48's top-22%-of-uneroded-sil rule,
stated to have caught the blade tip). Before implementing, this session
verified — by cropping and visually reading the actual `twin.png` content,
not by silhouette-shape inference alone — that on this mesh the topmost
silhouette point is the raised sword's tip, and the silhouette from there is
a single, near-constant-width (~47-50px on view 0) column all the way to
32.2% of the full vertical extent. A crop of exactly that top-25% band is
pure blade (confirmed visually on views 0 and 7). The head only appears as a
separate, wider silhouette mass starting at 32.2% down (also confirmed
visually — unambiguously the character's bald head and red beard on both
views checked). Since 32.2% > 25%, and since this arc's own (smaller)
erosion cap does not meaningfully shrink a 47-50px-wide shaft (the same
`e_img` arithmetic used in §3 puts a shaft that wide in the `ed_body`-bound,
small-constant-rim regime — thin structures near the tip taper are not what
gets thinned by this rule), swapping only the fraction (0.22→0.25) and the
sil source (uneroded→this arc's own eroded) cannot fix the underlying issue
on this mesh — it is not a sil-erosion question.

So this tool computes and shows BOTH, on the sheet, captioned with their own
derivation text (the same transparency convention this repo already uses for
`[PROPOSAL]` and `[DERIVED, not a ruling]` boxes):

- **head-literal** — the kickoff's literal wording, E48's algorithm
  unchanged in shape (top-N%-of-full-vertical-extent, x-extent from that
  band), with the two literal parameter changes applied (0.22→0.25,
  sil source → this arc's own eroded `aov_eroded/view_N/sil.npy`). Measured
  to still be blade shaft on every view with a crop row checked (0, 2, 7 —
  view 4 carries no crop rows, it is not a CROP_VIEW; visual inspection of
  the actual rendered sheet panels, not just the box coordinates).
- **head-corrected** — an evidence-based rule, this session's own addition,
  NOT the kickoff's literal wording (named as a deviation): scans past the
  initial tip taper for either a second silhouette run or a marked widening
  of the single run (>1.4x the shaft's own steady near-top width), ending at
  the first point the silhouette re-merges into a mass wider than 0.55x that
  view's own `fig_w` (full torso/shoulders), bounded to a 10%-22%-of-full-
  height band. Measured to show the actual head (bald head, red beard,
  visible identically across reference/shipped/owner-complete/blend-complete)
  on every view with a crop row checked (0, 2, 7 — view 4 carries no crop
  rows, it is not a CROP_VIEW).

Both boxes and their derivation parameters (`y0`, `y1_full`/`y_start`,
`y_end`, `base_w`, `fig_w`) are written to `sheets/manifest.json` per view,
exactly as auditable as E48's own derivation was.

### 8b. Region gaps, stated not patched

`s3_sheet_regions.json` has blade/grip boxes only for views 0, 1, 7 (view 2
has none — same gap E47/E48 both flagged, matching precedent, not
fabricated).

### 8c. Visual description of the sheets checked (description, not judgment)

Views 0, 2, 4, 7 visually inspected in full (all panels, all rows) as part
of verifying the head-box fix; the remaining views (1, 3, 5, 6) inspected via
their manifest entries (no missing panels, correct region-row counts) but
not opened at full resolution.

- The `shipped` panel carries no magenta on any view checked, matching
  E47/E48's own finding.
- `owner-complete` and `blend-complete` both show small magenta patches at
  full-figure scale, concentrated at boot tops/lower legs, greave edges,
  gauntlet/wrist areas, and torso/hip near the tunic seam — the same
  character and location E48 described, visibly present but not absent
  (this arc's own no-view-visible sentinel is a nonzero 4.65%/5.57% of
  valid texels, not the "zero sentinel" the kickoff named as one success
  condition — reported plainly in §6, not smoothed over here).
- `head-literal` crop rows: pure blade content on every view checked,
  matching the pre-registered expectation from §8a's visual recon.
- `head-corrected` crop rows: the character's actual head, consistent across
  all four panels on every view checked.
- Blade crops (views 0, 1, 7): visually similar in character to E48's own
  description (the `shipped` panel shows a light-top/dark-bottom split with
  a brown-toned patch near the guard; `reference` and both `-complete`
  panels show a more spatially uniform light grey/silver blade).

## 9. Predictions scored

| prediction | measured | result |
|---|---|---|
| P1 2-4px: EXACT match to E48 (analytic) | EXACT match, all 8 views | confirmed |
| P1 4-8px: v0 45-64%, v1 55-64%, v2 20-29%, v3 50-58% | v0=54.40%, v1=63.80%, v2=28.60%, v3=58.14% | 3/4 inside; v3 miss by 0.14pp |
| P1 8-16px: v0 20-35%, v1 20-35%, v2 8-18%, v3 15-28% | v0=30.60%, v1=29.13%, v2=19.18%, v3=24.61% | 3/4 inside; v2 miss by 1.18pp |
| P1 16-32px: v0 12-24%, v1 13-25%, v2 8-16%, v3 18-28% | v0=14.15%, v1=12.42%, v2=15.84%, v3=23.75% | 3/4 inside; v1 miss by 0.58pp (below floor) |
| P1 32-infpx: v0 2.0-4.0%, v1 2.5-4.5%, v2 1.5-3.0%, v3 1.8-3.2% | v0=2.74%, v1=2.59%, v2=3.17%, v3=2.46% | 3/4 inside; v2 miss by 0.17pp |
| P2 owner remaining-sentinel: 0.05%-1.5% of valid | 4.6539% | **miss, 3.1x the ceiling** |
| P2 blend remaining-sentinel: 0.15%-3.0% of valid | 5.5684% | **miss, 1.9x the ceiling** |

P1's exact-match band scored perfectly (as it was a derived certainty, not a
genuine prediction). P1's magnitude bands, disclosed as an approximate
proportionality heuristic, landed inside on 16 of 20 testable band/view
combinations; all 4 misses were narrow (0.14-1.18 percentage points past the
stated edge). P2 missed substantially in both modes — reported in full in
§6, including the mechanism hypothesis for why the prediction's reasoning
was wrong, not just its number.

## 10. Deviations / halts

None halted. Gate S held. No ANDON fired anywhere in the chain: erosion's
empty-silhouette guard and its two IMPLEMENTATION assertions (e_img bound,
flat-floor bound), the island-fill boundary-crossing guard, the island-fill
accounting guard, the orphan-fill accounting guard, the orphan-fill overlap
guards, and the render script's mesh/material/node-count and atlas-size
guards all ran clean.

Named, disclosed deviations (none silent):
- Repair 2's `ed_body` is a flat 2.5px, a stated departure from
  `project_twins.py`'s own escalated formula, per the kickoff's explicit ask.
- Orphan fill's selection score is `facing^6` alone (no border weight),
  a stated departure from the main pipeline's own `border*facing^alpha`
  weight, per the kickoff's literal wording.
- The head-corrected crop row is a stated departure from the kickoff's
  literal "top quarter of the eroded sil" wording — both are shown on the
  sheet, neither silently substituted for the other (§8a).

## 11. Artifacts

All under `E:\AI\training\facet_E49\`:

```
handoff.md                              live working record
predictions.md                          written before step 1 ran
erode_bundle_capped.py                  step 1 tool (repair 2) + erosion_manifest.json
aov_eroded/                             derived AOV bundle (sil eroded at flat 2.5px, all else copied)
atlas_owner_eroded/, atlas_blend_eroded/
  atlas.png, owner.npy, weight.npy, manifest.json       step 2 (paint)
  atlas_filled.png, filled_mask.npy, fill_manifest.json step 3 (within-island fill)
  atlas_complete.png, orphan_fill_mask.npy,
  no_view_visible_mask.npy, orphan_fill_manifest.json   step 4 (orphan fill, repair 1)
fill_islands_e49.py                     step 3 tool
fill_summary.json                       step 3 combined summary
orphan_fill.py                          step 4 tool (repair 1, new)
orphan_fill_summary.json                step 4 combined summary
renders_owner_complete/, renders_blend_complete/        8 views each, flat, from atlas_complete.png
build_sheets_e49.py                     step 6 tool (two head-box rules)
sheets/sheet_v00..07.png, sheets/manifest.json
step1_erode_capped.log .. step5_sheets.log              full stdout of every step
```

`git status --short` in the repo confirms this report is the only tracked
change; nothing else was committed, pushed, or written to the memory store.
HEAD moved once during this run for reasons unrelated to this arc (§ above,
front matter) — this report and all measurements are against the training
directory only, unaffected by that move.
