# E47 report — the atlas 2×2, rendered

Executor seat (Sonnet tier), dispatched 2026-08-16 at HEAD `d8fabb2c7193addb8dd1313e23732a0a91b5c20d`.
Dispatch: `docs/experiments/E47-atlas-ab-kickoff.md`. Full working record:
`E:\AI\training\facet_E47\handoff.md` (kept current through every step) and
`E:\AI\training\facet_E47\predictions.md` (written before step 1 ran).

No word in this report asserts that any result is good, working, or decisive. Every
number below is a measurement; the sheets are the artifact for the Director's eye.

## 1. Predictions (written before step 1 ran — full text in `predictions.md`)

Blind status: **NOT blind.** Grounded in E46's own primary files, re-verified
directly (`flow\manifest.json`, `ab_table.json`), not in the kickoff's paraphrase.
Confirmed for the four mandatory views: flow covers 16.22%–27.40% of silhouette,
median magnitude 1.448–2.612 px.

Committed before any cell ran: the per-texel delta formula (`mean_c |off-on|` over
RGB, read from `atlas.png`'s uint8/255 bytes, over co-written texels only), the
region-selector mechanism (a construction of this seat's own, not spelled out in the
kickoff — reproject each texel's decoded 3D position into the named view's camera via
`s3_composite.project_point`, test half-open box containment), and the instrument's
floor (identical atlases ⇒ delta ≡ 0 exactly, verified from the sampling code, not
assumed) and ceiling reasoning (bounded by affected-fraction × sampled-colour
variance, using E46's own disagreement deltas, 0.007–0.023, as the variance proxy).

| | owner mean / p90 | owner-change share | blend mean / p90 | blade vs grip | owner vs blend magnitude |
|---|---|---|---|---|---|
| predicted band | [0.003,0.03] / [0.01,0.12] | [0.0%,3.0%] | [0.005,0.05] / [0.02,0.20] | blade > grip | blend ≥ owner |

Visibility (Director's-zoom) predictions, per cell: owner/blade "marginal — a subtle
edge shift may be visible"; owner/grip "not clearly visible"; blend/blade "visible —
the most likely of the four cells"; blend/grip "marginal."

## 2. What ran

| step | tool | result |
|---|---|---|
| Gate S | `tools/atlas_from_aovs.py --selftest` | `atlas_from_aovs selftest OK  calibration atlas[16,16,0] == 0.5`, exit 0 |
| Gate S | `--anchor --aov facet_E45\aov --prep facet_E06\C1\prep` | `|bmid|=0.000e+00 |v_ext|=0.000e+00 |h_ext|=0.000e+00 valid=2402810`, exit 0 |
| 4 atlases | `atlas_from_aovs.py` × {owner,blend} × {off,on} | all exit 0 |
| 32 renders | `render_atlas_swap.py` (training dir) via Blender `-b -P`, PowerShell | all exit 0 |
| 5 sheets | `build_sheets.py` (training dir) | all exit 0, no MISSING panels |
| A/B numbers | `ab_analysis.py` (training dir) | exit 0, run twice (region selector refined in place — see §4) |

Gate S matches the recorded precedent exactly (`|bmid|` 0.000e+00, valid-texel count
2,402,810).

**The four atlases** (`atlas_from_aovs.py --aov facet_E45\aov --prep facet_E06\C1\prep`,
alpha=6.0, relative_jump=0.05, sentinel=255,0,255 throughout — manifests verified to
differ ONLY in `mode` and `flow_dir`, programmatically diffed field-by-field, not
eyeballed):

| cell | mode | flow | written / valid | pct |
|---|---|---|---|---|
| atlas_owner_off | owner | off | 2,027,886 / 2,402,810 | 84.39% |
| atlas_owner_on | owner | on | 2,001,843 / 2,402,810 | 83.30% |
| atlas_blend_off | blend | off | 1,766,764 / 2,402,810 | 73.53% |
| atlas_blend_on | blend | on | 1,720,763 / 2,402,810 | 71.61% |

Coverage drops when flow is on, in both modes (owner −26,043 texels / −1.28%
relative; blend −46,001 / −2.60% relative). Mechanism, read from
`s3_composite.sample_view` before this was measured, not after: flow shifts the
sampled position (`sx, sy = px + flow_x, py + flow_y`) **before** the visibility test
(`_tap_origin_valid`, the depth comparison) and before the border-weight sample — an
initial read of the code had this backwards (recorded in `predictions.md`'s
"Mechanism check" section as a correction, not deleted) — so flow can turn a
previously-valid tap invalid, not only move colour. The owner/blend gap present in
BOTH off and on (~11 points) is a separate, pre-existing difference in the two modes'
own "written" definition (blend requires `acc_w>0` strictly; owner's argmax accepts a
valid-but-zero-weight sample) — noted, not chased, out of this arc's scope.

**The renders.** `render_atlas_swap.py` (training dir) imports the shipped
`W3_final.glb` verbatim, ANDONs unless the material graph is exactly 1 mesh / 1
material / 1 `ShaderNodeTexImage` node and the new atlas's pixel size matches the
shipped atlas's — confirmed by `introspect_glb.py` (a dry-run, no-render pass) before
the real script was written: 1 mesh, material `'hero'`, node `'Image Texture'` →
image `'atlas_final'` (4096×4096, sRGB) → Base Color → Material Output. None of the
ANDONs fired across all 4 runs. Camera/lighting parameters are `turn_render.py`'s own
defaults, copied verbatim and cited by line (w=752 h=1024, margin=1.204, exposure=0.85,
bg=0.181/0.181/0.188, FLAT light, Standard transform) — checked against
`profiles/character.json` first: its `verify/turn_render.py` block only sets
`views`/`step`/`w`/`h`, and all four are digit-identical to the tool's own hardcoded
defaults, so the shipped render's exact parameters are reproduced whether or not
`--profile` was used originally. 32 files written (4 cells × 8 views), confirmed
present by a complete directory count (not `head`/`tail`). The shipped comparison
render is consumed as-is from `facet_E08\ARMB\out\renders_flat\final_{0..7}.png` —
never re-rendered.

**The sentinel** (magenta, 255,0,255) appears at unwritten texels in all four cells'
renders, by design — visible on every sheet at shoulder pauldrons, boot tops, and
torso seams, on all four rebuilt atlases, never on the shipped panel (which was built
with dilation/flood/brush machinery this arc's atlas tool's own docstring says it does
not implement: *"No island dilation, no gutter fill, no hole flood, no brush
strokes... this atlas is not a rebuild of the shipped atlas and must not be compared
to it as one"*). Owner's larger written set means less magenta than blend's at the
same view, a mode-driven effect, independent of the flow question.

## 3. The sheets

`sheets\sheet_v00.png`, `sheet_v01.png`, `sheet_v02.png`, `sheet_v06.png`,
`sheet_v07.png` — 5 panels per row (shipped | owner-off | owner-on | blend-off |
blend-on), native pixels at zoom=1 for the FULL row, integer zoom=3 for region crops,
provenance panel (recomputed sha256, not trusted from any manifest) at the foot of
every sheet. Region crop rows (blade, grip) present on views 0, 1, 7 — the only views
`tools/s3_sheet_regions.json` carries boxes for; views 2 and 6 carry the FULL row
only. No box was fabricated for 2 or 6.

`s3_sheet.py`'s own CLI contract does not fit this panel set (5 different roles, no
heat map, no `s3_run` directory tree behind them) — `build_sheets.py` imports its
tested primitives (`crop_array`, `nn_zoom`, `compose_row`, `stack_rows`,
`provenance_panel`, `sha256_file`, `as_rgb_u8`, `load_regions`) as a library rather
than reimplementing them; no repo file was touched.

**"Elevated-content" view resolved as view 0** — this seat's own reading, stated
plainly rather than silently assumed. None of the 8 standard turn views carries a
different camera elevation (`turn_render.py` orbits yaw only; the Gate-S-anchored AOV
bundle is the same flat 8-view set); a true e=55 render was not built. View 0 was
chosen because it is the only view carrying a 4th named region (tunic, skirt) beyond
blade/grip in the shipped regions file — a resource-driven choice, not a
camera-elevation one.

All 5 sheets visually inspected by this seat before writing this report (not merely
generated). Observed, stated as observation rather than judgment: the shipped panel
is clean of magenta on every view; all four rebuilt atlases show visible magenta at
the same locations on every view; owner-off/owner-on look close to each other at
FULL-row scale, as do blend-off/blend-on. On the blade crop (views 1, 7), this seat's
own first read was that owner-on appeared to carry less magenta than owner-off — **the
precise count in §4 contradicts that impression** (coverage drops in every checked
region, never gains). Recorded as a caught discrepancy between a quick visual read and
the measurement, not smoothed over. The sheets are the artifact; this seat's reading
of them is not a substitute for the Director's.

## 4. The A/B numbers

Delta = `mean_c |off − on|` over RGB, uint8/255 (quantization floor: smallest
possible nonzero reading is 1/255 in one channel, delta 0.00131), over co-written
texels (owner ≠ −1 in both off and on).

| mode | co_written | pct of valid (2,402,810) | mean | p90 | frac_nonzero |
|---|---|---|---|---|---|
| owner | 1,966,581 | 81.85% | 0.020860 | 0.057516 | 0.2724 |
| blend | 1,687,679 | 70.24% | 0.015588 | 0.043137 | 0.3941 |

**Owner-change share** (owner ≠ owner, of co-written): **151,088 / 1,966,581 = 7.6828%.**

**Against §1's bands**: owner mean/p90 inside band; blend mean/p90 inside band.
**Owner-change share is a MISS**, above the [0.0%,3.0%] band by more than 2.5×.
**Blend's mean/p90 came out LOWER than owner's, not higher — a second, direction-level
miss**, not just a band width. `frac_nonzero` runs the opposite way (blend 39.41% vs
owner 27.24% of co-written texels carry any nonzero delta) — so blend affects MORE
texels, each by LESS. A hypothesis, not verified independently: blend's weighted
average dilutes one shifted contributing view against several unshifted ones, where
owner's single-winner colour is fully exposed to whichever view it draws from.

**Region table** (visible-refined selector — see below — mean / p90 over co-written,
owner then blend):

| view | region | owner mean/p90 | blend mean/p90 |
|---|---|---|---|
| 0 | blade | 0.0240 / 0.0719 | 0.0177 / 0.0471 |
| 0 | grip | 0.0219 / 0.0758 | 0.0206 / 0.0641 |
| 1 | blade | 0.0340 / 0.1294 | 0.0181 / 0.0418 |
| 1 | grip | 0.0219 / 0.0667 | 0.0178 / 0.0484 |
| 7 | blade | 0.0193 / 0.0405 | 0.0153 / 0.0392 |
| 7 | grip | 0.0131 / 0.0261 | 0.0098 / 0.0222 |

Owner > blend on every one of the 6 rows (same direction as the miss above — a
consistent pattern, not an aggregation artifact). Blade > grip on 5 of 6 rows (view 0
owner is the exception: 0.0240 vs 0.0219, close).

**Region selector, two versions, both kept.** Region boxes are defined in a named
view's 752×1024 pixel frame, not atlas/UV space — reconciling the two is this seat's
own construction (§1). First pass projected each texel's decoded 3D position into the
box's declaring view and tested containment alone (RAW) — counts came back large
(541,838 / 239,277 / 659,124 texels for boxes of comparable pixel area), a signal
reported rather than used as-is: this test is blind to occlusion, so a texel sitting
behind the blade from that camera lands in the same box. Refined by intersecting with
`s3_composite.sample_view(...)["valid"]` for that view (no flow — a fixed geometric
fact, independent of which cell is being scored): visible-in-box counts are
16.6%–54.5% of the raw counts. Only the visible-refined numbers are read as "the
blade/grip region" above; both are in `ab_numbers.json`.

**Per-region coverage (written vs sentinel), off vs on** — added after the sheets
raised a specific, checkable question the co-written delta stats are silent on
(co-written excludes exactly the texels a coverage-pattern change would show):

| view | region | owner off | owner on | owner Δ | blend off | blend on | blend Δ |
|---|---|---|---|---|---|---|---|
| 0 | blade | 100.00% (169,427) | 99.28% (168,211) | −1,216 | 87.32% | 83.49% | −6,495 |
| 0 | grip | 100.00% (18,761) | 98.47% (18,474) | −287 | 90.84% | 88.54% | −432 |
| 1 | blade | 100.00% (130,325) | 99.53% (129,713) | −612 | 87.90% | 81.32% | −8,570 |
| 1 | grip | 100.00% (45,801) | 98.55% (45,137) | −664 | 86.17% | 83.71% | −1,127 |
| 7 | blade | 100.00% (170,790) | 99.31% (169,609) | −1,181 | 91.30% | 88.25% | −5,214 |
| 7 | grip | 100.00% (101,897) | 99.52% (101,405) | −492 | 93.29% | 92.05% | −1,261 |

Denominator is each region's own visible-in-box population (owner-off reads 100.00%
in every row by construction — "visible-in-box" is defined as the same occlusion test
owner's own weight uses when flow is absent). **Coverage drops in every one of the 12
mode×region cells, never gains** — the direction that contradicts this seat's own
blade-crop visual impression in §3. Blend's relative drop is larger than owner's in
blade specifically (0.72/0.47/0.69% vs 4.39/7.48/3.34%); closer in grip
(1.53/1.45/0.48% vs 2.53/2.86/1.33%).

## 5. Gates

Gate S HELD (§2). No other gate is defined in the kickoff for this arc. No gate
fired; nothing was halted.

## 6. Picture paths

```
E:\AI\training\facet_E47\sheets\sheet_v00.png   (view 0, FULL + blade + grip)
E:\AI\training\facet_E47\sheets\sheet_v01.png   (view 1, FULL + blade + grip)
E:\AI\training\facet_E47\sheets\sheet_v02.png   (view 2, FULL only)
E:\AI\training\facet_E47\sheets\sheet_v06.png   (view 6, FULL only)
E:\AI\training\facet_E47\sheets\sheet_v07.png   (view 7, FULL + blade + grip)
E:\AI\training\facet_E47\sheets\manifest.json   (per-sheet provenance, consumed[] with sha256)
```

Atlases: `E:\AI\training\facet_E47\atlas_{owner,blend}_{off,on}\{atlas.png,owner.npy,weight.npy,manifest.json}`
Renders: `E:\AI\training\facet_E47\renders_{owner,blend}_{off,on}\{tag}_{0..7}.png`
A/B numbers: `E:\AI\training\facet_E47\ab_numbers.json`
Scripts (training dir, not repo tools): `ab_analysis.py`, `build_sheets.py`,
`introspect_glb.py`, `render_atlas_swap.py`
Full working record: `E:\AI\training\facet_E47\handoff.md`, `predictions.md`

## 7. What this seat did NOT do

- Did not fabricate blade/grip region boxes for views 2 or 6 — `s3_sheet_regions.json`
  carries none, and the sheets for those views show the FULL row only.
- Did not build a true elevated-elevation (e=55) render — no camera-elevation
  parameter exists in `turn_render.py`'s conventions or in the Gate-S-anchored AOV
  bundle; view 0 stands in for "elevated-content" on the resource-richness reading
  stated in §3, not a certainty.
- Did not compare the rebuilt `atlas.png` outputs to the shipped `atlas_final.png` as
  if they were the same kind of object — `atlas_from_aovs.py`'s own docstring forbids
  this (no dilation/flood/brush machinery is modelled) and the sheets' magenta pattern
  is the visible evidence of that gap, not a defect in this arc's tool.
- Did not resolve the discrepancy between this seat's own blade-crop visual
  impression and the measured coverage direction in §4 — stated as an open,
  caught discrepancy, not investigated further or explained away.
- Did not investigate the owner/blend mode's own ~11-point coverage gap (present in
  both off and on) beyond naming its structural cause (`acc_w>0` vs argmax-accepts-
  zero-weight) — out of this arc's scope.
- Did not commit, push, write to the memory store, or edit any tool, test, or
  count-surface file. The only repo file created is this report.
- Did not judge whether any result is good, working, or decisive, per the executor
  rules — every finding above is stated as a measurement or a prediction scored
  against a band, nothing more.
