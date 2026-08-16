# E46 — report: the S3 run, stills, sheets, and the flow A/B

**Written 2026-08-16 by the dispatched executor seat** (Sonnet tier), against
`docs/experiments/E46-s3-run-kickoff.md`. Evidence only. This seat does not decide
what any number means; the advisor rules and the Director's eye is the acceptance
gate. Every number below is attributable to a script or manifest on disk. Paths are
absolute. Dispatched at HEAD `46acaee6dc7e175c1a523471e92bdb97e6414cc8`; tree
confirmed clean at the start (`git status --short` empty). At the final check, one
untracked file this seat did not create had appeared —
`tools/callieri_border_repair.diff`, timestamped after this seat's own s3_run/sheet
steps. Its content repairs the `callieri_border.py` RuntimeWarning that E45's report
flagged and left untouched — a different site from the `s3_composite.py:234-235`
warning this report notes in section 4, same family. Read, not touched, not
attributed to this seat's work; consistent with another concurrent seat's
uncommitted output in a tree this dispatch shares.

| artifact | path |
|---|---|
| handoff (kept current from before the first measurement) | `E:\AI\training\facet_E46\handoff.md` |
| predictions (written before step 2 ran) | `E:\AI\training\facet_E46\predictions.md` |
| flow driver + fields | `E:\AI\training\facet_E46\run_flow.py`, `flow\view_0..7\flow.npy` (+confidence.npy, confidence_xy.npy), `flow\manifest.json` |
| S3 off (no flow) | `E:\AI\training\facet_E46\s3_off\t00..t07\`, `manifest.json`, `provenance.json` |
| S3 on (+flow) | `E:\AI\training\facet_E46\s3_on\t00..t07\`, `manifest.json`, `provenance.json` |
| sheets, off arm | `E:\AI\training\facet_E46\sheets_off\sheet_v00..v07.png`, `manifest.json`, `provenance.json` |
| sheets, on arm | `E:\AI\training\facet_E46\sheets_on\sheet_v00..v07.png`, `manifest.json`, `provenance.json` |
| A/B table assembly | `E:\AI\training\facet_E46\ab_table.py` / `ab_table.json` |
| provenance writer | `E:\AI\training\facet_E46\write_provenance.py` |

---

## 0. Gate S — HELD, all three legs

```
python tools/s3_composite.py --selftest
  -> s3_composite selftest OK  calibration red[16,16] == 0.640625      (exit 0)
python tools/flow_estimate.py --selftest
  -> flow_estimate selftest OK  calibration flow_x[32,32] == 3.0       (exit 0)
python tools/s3_sheet.py --selftest
  -> s3_sheet selftest OK  calibration crop[0,0] == 200                (exit 0)
```

All three lines matched the kickoff's required text exactly. No `emit_view_aovs.py
--selftest` run — the bundle exists, per the kickoff, and this seat did not touch
the bundle-producing path.

---

## 1. Reconnaissance, before any tool ran

Full detail in `handoff.md`. Headline findings that shaped every step below:

- `flow_estimate.py` ships **no batch CLI** (`--selftest` only; "functions are the
  API," same convention as `s3_composite.py`). This seat wrote a thin driver
  (`run_flow.py`, not a repo tool) that imports `estimate_flow` directly.
- `s3_run.py`'s `--flow-dir` loader (`tools/s3_run.py:93-97`) reads exactly
  `flow_dir/view_N/flow.npy`, an (H,W,2) array, nothing else — no confidence file.
  Safe unconditionally: `flow_estimate.py`'s own docstring states "Identity (flow 0,
  confidence 0) is the compositor default there," so `flow.npy` is already 0
  wherever unmeasured.
- Mesh-side flow signal: `depth_edge.npy` (bool AOV array; the docstring's stated
  preference "now that the AOV bundle exists"), twin-side: `twin.png`, `pair="edge"`.
  Twin normalised to `[0,1]` to match `depth_edge`'s own `{0,1}` scale —
  `estimate_flow` does not auto-scale its inputs (`to_gray`/`to_edge` apply no
  normalisation), so leaving the twin at `0-255` while `depth_edge` sits at `0/1`
  would make `it = i0 - i1` dominated by the twin's own scale rather than by
  displacement. This is a caller decision, stated here and in `flow/manifest.json`,
  not a tool default.
- `--ref-dir` = `E:\AI\training\facet_E08\ARMB\twins\` (matches the AOV manifest's
  own `image_src` for every view). `--shipped-dir` =
  `E:\AI\training\facet_E08\ARMB\out\renders_flat\` (`final_0..7.png`, 8 files).
- `tools/s3_sheet_regions.json` (shipped, unedited this session) carries named
  regions for views **0, 1, 7 only** — its own `view_map` says so, and its `label`
  field reads verbatim `"PROPOSALS. Not a ruling. Transcribed E40 four plus
  blade/grip for the views those sit on. Verify on the sheet before judging."` This
  seat ran `s3_sheet` with `--views 0,1,2,3,4,5,6,7` (all 8, matching `s3_run`'s 8
  targets) so every view gets a FULL-row sheet; views 0/1/7 additionally get their
  named per-region rows exactly as shipped. This is a CLI argument, not an edit to
  the regions file.
- `s3_run.py`'s and `s3_sheet.py`'s own `manifest.json` carry no tool sha256, no
  package versions, no HEAD commit. This seat wrote a sibling `provenance.json` into
  every output directory with those fields, without touching the tool-native
  `manifest.json` files.
- None of the four tools (`s3_composite`, `s3_run`, `s3_sheet`, `flow_estimate`)
  import open3d — confirmed by reading their imports. Env: python 3.13.13, numpy
  2.4.6, scipy 1.17.1, PIL 12.2.0 (same pinned venv E45 used).
- Instrument interval check, done before predicting (the kickoff's own instruction,
  the E39 trap check): `test_t77_s3_composite.py` pins the disagreement **floor**
  exactly (`fixture_shift_pair`, `<=1e-5`). It does **not** pin a numeric ceiling for
  `fixture_disagree_pair`. `s3_composite.py`'s docstring states the ceiling in prose
  as "1". Reading the unmodified fixture + the unmodified `disagreement_map`
  function directly (same move as E45's `s3_smoke.py`): **the actual computed value
  is `0.7071067690849304` (= sqrt(0.5)), not 1.** Predictions below are calibrated
  against the measured interval `[0, 0.7071]`, not the docstring's prose.

---

## 2. Predictions (written before step 2 ran) — against outcomes

Full text: `predictions.md`. Blind status as stated there: part (a)'s numeric band
was **not blind** (informed by E45's warp numbers and one E45 smoke-run prior for
view 1); part (b) was **not blind** (informed by this seat's own step-1 flow
coverage, read before the prediction was written).

### Part (a): full-frame disagreement p90 (s3_off) — band vs measured

| view | predicted band | measured p90 (s3_off, FULL) | in band? |
|---|---|---|---|
| 1 | [0.05, 0.25] | **0.21598** | yes |
| 2 | [0.08, 0.35] | **0.26983** | yes |
| 7 | [0.08, 0.35] | **0.17770** | yes |

All three landed inside the stated band. **The ranking part of the prediction
missed.** This seat predicted view 7 "likely the highest of the three" (following
E45's `twin_mesh_warp` interior-leg ranking, where view 7's median/p90 px, 11.124 /
28.77, exceeds view 2's 8.751 / 30.89). Measured by `s3_composite`'s disagreement
metric, the ranking is **view 2 (0.270) > view 1 (0.216) > view 7 (0.178)** — view 7
is the *lowest* of the three by this metric, not the highest, and view 1 (E45's
"least warped" of the three) sits in the middle. The two instruments disagree on
relative order between views 2 and 7; both readings are reported, neither
adjudicated here.

The qualitative "world" call (clean/blotchy) was pre-registered as a genuine,
disclosed guess this seat could not verify numerically before looking at a
composite, and per the kickoff, "no metric decides; the Director's eye does" — this
seat has not rendered a verdict on it and the sheets are delivered unjudged, at
native size, for that reading. The disagreement numbers measured above (view 2
highest, view 7 lowest of the three) are offered as the numeric half only.

### Part (b): A/B direction, given step-1 flow coverage

Predicted: flow-on reduces full-frame mean disagreement by roughly **3-15%
relative**, smaller than a full correction would produce, because (1) flow is
identity outside the measured set (~21-27% of silhouette for these 3 views, from
step 1) and (2) flow_estimate's measured magnitude undershoots E45's own interior
warp median on views 2 and 7 specifically. Secondary, more hedged prediction: the
**blade** region (views 1, 7) shows a larger relative reduction than the full frame.

**Measured** (full A/B table in section 5): flow-on reduced disagreement — both mean
and p90 — on **every one of the 8 views and every one of the 10 named regions
measured, with no exception**. Full-frame mean reduction ranged **5.44%-9.21%**,
inside the predicted 3-15% band on all 8 views. Full-frame p90 reduction ranged
**2.47%-6.32%**, also inside band. Two named sub-regions (view 0 skirt, view 1
tunic) fell slightly under the 3% floor on **mean** (2.70%, 2.37%) — both are the
broad fabric regions, not the blade. The secondary blade prediction held on **mean**
for both views 1 and 7 (blade 10.61% / 8.00% vs FULL 5.94% / 5.51% on those views)
and was a near-tie on **p90** for view 7 (blade 3.52% vs FULL 3.47%) while view 1's
blade p90 reduction (7.26%) did exceed its FULL p90 reduction (2.47%).

**Direction was uniform across all 18 measured (view, region) rows: flow-on never
increased disagreement, mean or p90, anywhere measured.** This seat's explicit
hedge — "does not rule out a near-null or locally adverse result in some
sub-region or tile" — did not materialise at the region-and-view granularity this
run measured; a per-tile or per-pixel read could still differ and was not examined
(out of scope, see section 7).

---

## 3. Step 1 — flow fields

`run_flow.py`, `estimate_flow(depth_edge, twin01, sil=sil, pair="edge")`, tool
defaults (window=7, corner_rel=0.15, grad_percentile=75.0). Output:
`flow\view_0..7\{flow.npy, confidence.npy, confidence_xy.npy}`, manifest at
`flow\manifest.json`.

| view | sil px | measured px (confidence>0) | frac of sil | frac of frame | flow magnitude over measured px: median / p90 |
|---|---|---|---|---|---|
| 0 | 146,356 | 27,776 | 0.1898 | 0.0361 | 3.170 / 8.762 |
| 1 | 149,780 | 38,908 | 0.2598 | 0.0505 | 2.459 / 8.603 |
| 2 | 90,553 | 24,813 | 0.2740 | 0.0322 | 1.448 / 6.862 |
| 3 | 120,439 | 29,952 | 0.2487 | 0.0389 | 2.315 / 7.199 |
| 4 | 146,356 | 31,605 | 0.2159 | 0.0410 | 3.040 / 8.546 |
| 5 | 149,780 | 39,332 | 0.2626 | 0.0511 | 2.410 / 10.030 |
| 6 | 90,553 | 14,689 | 0.1622 | 0.0191 | 2.612 / 7.627 |
| 7 | 120,439 | 26,238 | 0.2179 | 0.0341 | 2.446 / 7.070 |

**A negative-leaning result, reported plainly.** Flow was measured (confidence>0)
on 16-27% of each view's silhouette; the remaining 73-84% carries identity flow (0)
by the tool's own construction — no signal on both the depth-edge mask and the
twin's own edges at the 75th-percentile floor, on either or both images. Measured
flow magnitude among the pixels that DO qualify (median 1.4-3.2 px, p90 6.9-10.0 px
across all 8 views) is **smaller** than E45's `twin_mesh_warp` interior-leg
per-tile median (3.5-11.1 px across the 8 views) — most visible on views 2 and 7,
where flow_estimate's median (1.448 / 2.446 px) is well under E45's interior median
(8.751 / 11.124 px). This seat's reading (section 1, predictions.md): a 7 px window
is not sized to capture displacements several times its own radius; this is
reported as a measured gap between two different instruments, not resolved here.

---

## 4. Steps 2-3 — S3 off / on

`s3_run.py --aov E:\AI\training\facet_E45\aov --out ...`, all 8 targets, defaults
(`alpha=6.0`, `primary_floor=0.05`, `primary_mode="target"`); on-arm adds
`--flow-dir E:\AI\training\facet_E46\flow`. One variable. Both exited 0, wrote 8
targets each.

**Observed on every run (off and on), not investigated further (out of scope):**
`RuntimeWarning: invalid value encountered in cast` at `s3_composite.py:234-235`
(`fx = np.floor(px).astype(np.int64)` / `fy = ...`), consistent with a NaN/inf entry
in `px`/`py` for background pixels (the AOV bundle's own manifest states `pos` is
NaN off-silhouette). Exit code was 0 both times; same family as the
`callieri_border.py` warning E45 reported and left untouched.

Per-target headline from each run's own `manifest.json` (`disagreement_mean` is
over `coverage`, not `sil`):

| target | coverage_px off | coverage_px on | fallback_px off | fallback_px on | disagreement_mean off | disagreement_mean on |
|---|---|---|---|---|---|---|
| t00 | 143,491 | 142,043 | 62,360 | 57,182 | 0.079674 | 0.075341 |
| t01 | 147,455 | 145,619 | 61,997 | 57,147 | 0.087461 | 0.082266 |
| t02 | 89,597 | 89,149 | 34,015 | 31,220 | 0.112576 | 0.104644 |
| t03 | 118,868 | 118,186 | 59,497 | 54,459 | 0.074058 | 0.068848 |
| t04 | 143,975 | 142,571 | 55,070 | 50,100 | 0.071799 | 0.065185 |
| t05 | 147,427 | 145,695 | 62,343 | 56,321 | 0.071135 | 0.064943 |
| t06 | 89,328 | 88,955 | 37,503 | 35,465 | 0.087315 | 0.080423 |
| t07 | 118,715 | 117,470 | 64,354 | 59,686 | 0.071550 | 0.067605 |

`coverage_px` (denominator 770,048 = 752x1024 full frame) fell on **all 8** targets
when flow was applied (by 0.60%-1.68% relative) — some previously-valid samples
became invalid once shifted by the flow vector (tap-origin or depth-visibility test
failing at the shifted location). `fallback_px` fell on all 8 as well.

---

## 5. Step 4 — sheets, both arms

`s3_sheet.py --s3-dir ... --ref-dir E:\AI\training\facet_E08\ARMB\twins
--shipped-dir E:\AI\training\facet_E08\ARMB\out\renders_flat --regions
tools\s3_sheet_regions.json --out ... --views 0,1,2,3,4,5,6,7` (zoom default 1,
heat-scale default global). Both arms exited 0, wrote 8 view sheets each, all at
native size (panel `full_hw` = `[1024, 752]` on every view in both manifests).

**No MISSING panel fired anywhere.** Every `consumed` entry in both manifests
carries a real sha256 (reference, shipped, VD, VI, disagreement, coverage,
fallback, owner all present for all 8 views, both arms) — confirmed by reading both
manifests complete (728 lines each) rather than sampling. Sheet PNG dimensions
independently reread and confirmed to match each manifest's stated `height`/`width`
for all 16 files (8 views x 2 arms); pixel standard deviation 61-80 (nonzero,
not blank) on every sheet, checked programmatically, not by eye.

Regions delivered exactly as shipped: view 0 = tunic/skirt/blade/grip, view 1 =
tunic/blade/grip, view 7 = boot_tops/blade/grip, views 2/3/4/5/6 = FULL row only
(the regions JSON has no entries for them). The regions file's `label` field
("PROPOSALS. Not a ruling... Verify on the sheet before judging.") applies to the
blade/grip boxes in all three named views.

Sheet paths: `E:\AI\training\facet_E46\sheets_off\sheet_v00.png` through
`sheet_v07.png`, and the same under `sheets_on\`.

---

## 6. Step 5 — the A/B table (numerators and denominators)

Source: `ab_table.py`, reading only `disagreement.npy` / `coverage.png` /
`fallback.png` / `owner.npy` already written by `s3_run.py`, and the per-region
`stats` blocks `s3_sheet.py` already computed into its own manifests. The FULL row
is `s3_sheet.region_stats` (unmodified, shipped function) called with a
full-frame box — the same reduction the named regions already got, not a new
metric. Full data: `ab_table.json`.

| view | region | area (denom) | d_mean off | d_mean on | d_mean rel chg | d_p90 off | d_p90 on | d_p90 rel chg | cov off / area | cov on / area | fallback off / cov | fallback on / cov |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | FULL | 770,048 | 0.07967 | 0.07534 | -5.44% | 0.19901 | 0.19407 | -2.49% | 143,491 / 770,048 | 142,043 / 770,048 | 62,360 / 143,491 (43.46%) | 57,182 / 142,043 (40.26%) |
| 0 | tunic | 48,400 | 0.07924 | 0.07369 | -7.00% | 0.20992 | 0.19754 | -5.90% | 39,801 / 48,400 | 39,449 / 48,400 | 18,674 / 39,801 (46.92%) | 17,111 / 39,449 (43.37%) |
| 0 | skirt | 32,400 | 0.05487 | 0.05339 | -2.70% | 0.11420 | 0.11059 | -3.16% | 29,423 / 32,400 | 29,379 / 32,400 | 11,264 / 29,423 (38.28%) | 10,898 / 29,379 (37.09%) |
| 0 | blade | 50,400 | 0.13653 | 0.12641 | -7.41% | 0.25405 | 0.24189 | -4.79% | 23,628 / 50,400 | 23,504 / 50,400 | 8,998 / 23,628 (38.08%) | 8,038 / 23,504 (34.20%) |
| 0 | grip | 6,250 | 0.11285 | 0.10171 | -9.87% | 0.23049 | 0.22333 | -3.11% | 4,006 / 6,250 | 3,949 / 6,250 | 1,730 / 4,006 (43.19%) | 1,231 / 3,949 (31.17%) |
| 1 | FULL | 770,048 | 0.08746 | 0.08227 | -5.94% | 0.21598 | 0.21066 | -2.47% | 147,455 / 770,048 | 145,619 / 770,048 | 61,997 / 147,455 (42.04%) | 57,147 / 145,619 (39.24%) |
| 1 | tunic | 48,400 | 0.09245 | 0.09025 | -2.37% | 0.24307 | 0.24205 | -0.42% | 44,198 / 48,400 | 43,758 / 48,400 | 21,594 / 44,198 (48.86%) | 20,551 / 43,758 (46.97%) |
| 1 | blade | 48,400 | 0.16334 | 0.14601 | -10.61% | 0.31470 | 0.29186 | -7.26% | 20,071 / 48,400 | 20,026 / 48,400 | 1,680 / 20,071 (8.37%) | 1,491 / 20,026 (7.45%) |
| 1 | grip | 14,400 | 0.10303 | 0.09193 | -10.78% | 0.22031 | 0.21120 | -4.13% | 7,924 / 14,400 | 7,829 / 14,400 | 3,807 / 7,924 (48.04%) | 3,271 / 7,829 (41.78%) |
| 2 | FULL | 770,048 | 0.11258 | 0.10464 | -7.05% | 0.26983 | 0.25880 | -4.09% | 89,597 / 770,048 | 89,149 / 770,048 | 34,015 / 89,597 (37.96%) | 31,220 / 89,149 (35.02%) |
| 3 | FULL | 770,048 | 0.07406 | 0.06885 | -7.03% | 0.18237 | 0.17271 | -5.30% | 118,868 / 770,048 | 118,186 / 770,048 | 59,497 / 118,868 (50.05%) | 54,459 / 118,186 (46.08%) |
| 4 | FULL | 770,048 | 0.07180 | 0.06518 | -9.21% | 0.16684 | 0.15629 | -6.32% | 143,975 / 770,048 | 142,571 / 770,048 | 55,070 / 143,975 (38.25%) | 50,100 / 142,571 (35.14%) |
| 5 | FULL | 770,048 | 0.07113 | 0.06494 | -8.70% | 0.16594 | 0.15730 | -5.20% | 147,427 / 770,048 | 145,695 / 770,048 | 62,343 / 147,427 (42.29%) | 56,321 / 145,695 (38.66%) |
| 6 | FULL | 770,048 | 0.08732 | 0.08042 | -7.89% | 0.19955 | 0.18837 | -5.60% | 89,328 / 770,048 | 88,955 / 770,048 | 37,503 / 89,328 (41.98%) | 35,465 / 88,955 (39.87%) |
| 7 | FULL | 770,048 | 0.07155 | 0.06760 | -5.51% | 0.17770 | 0.17155 | -3.47% | 118,715 / 770,048 | 117,470 / 770,048 | 64,354 / 118,715 (54.21%) | 59,686 / 117,470 (50.81%) |
| 7 | boot_tops | 19,600 | 0.04891 | 0.04555 | -6.87% | 0.10642 | 0.09901 | -6.97% | 15,295 / 19,600 | 15,128 / 19,600 | 6,013 / 15,295 (39.31%) | 5,498 / 15,128 (36.34%) |
| 7 | blade | 42,000 | 0.09192 | 0.08457 | -8.00% | 0.21082 | 0.20339 | -3.52% | 17,234 / 42,000 | 17,148 / 42,000 | 10,690 / 17,234 (62.03%) | 9,352 / 17,148 (54.54%) |
| 7 | grip | 9,900 | 0.06512 | 0.06288 | -3.45% | 0.17183 | 0.16692 | -2.86% | 9,696 / 9,900 | 9,660 / 9,900 | 6,807 / 9,696 (70.20%) | 6,589 / 9,660 (68.21%) |

18 of 18 rows: disagreement mean and p90 both fell off-to-on. 18 of 18 rows:
coverage fell off-to-on. 18 of 18 rows: fallback share fell off-to-on. No row moved
in the opposite direction on any of the four measured quantities.

---

## 7. What this seat did NOT do

- **Did not judge any composite, sheet, or number as good, clean, blotchy, correct,
  or acceptable.** The words verified/shipped/works/decisive/validated/proven do not
  appear above. The "world" classification (section 2, part a) is explicitly left
  to the Director's eye on the delivered sheets.
- **Did not run `emit_view_aovs.py --selftest`** — did not touch the bundle-producing
  path; the E45 bundle was consumed as-is.
- **Did not edit `tools/s3_sheet_regions.json`.** Ran it exactly as shipped,
  including its own "PROPOSALS, not a ruling" label; only the `--views` CLI argument
  was widened from the file's own default view set (0,1,7) to all 8.
- **Did not tune, retune, or override any tool default** (window, corner_rel,
  grad_percentile in `flow_estimate`; alpha, primary_floor, primary_mode in
  `s3_run`; heat_scale, zoom in `s3_sheet`) after seeing any result. All were
  fixed before step 2 ran and are recorded in each stage's `provenance.json`.
- **Did not investigate the `RuntimeWarning: invalid value encountered in cast`**
  observed on every `s3_run` invocation (section 4). Both runs exited 0; not part
  of this dispatch's scope.
- **Did not resolve the flow_estimate-vs-twin_mesh_warp magnitude gap** on views 2
  and 7 (section 3) beyond stating a measured difference and one candidate
  mechanism (window size vs. displacement magnitude). Not adjudicated here.
- **Did not examine per-tile or per-pixel A/B behaviour** below the (view, region)
  granularity in section 6 — the "no exception, 18 of 18 rows" finding is at that
  granularity only; a finer read could show local counterexamples and was not run.
- **Did not commit, push, or write to the memory store.** `git status --short` in
  `E:\AI\facet` was empty at session start; at the final check it showed this report
  file plus `tools/callieri_border_repair.diff`, a file this seat did not write (see
  the note at the top of this report).
- **Did not edit any tool, test, or count-surface.**
- **Did not delegate any core measurement to a child agent.**
- **Did not run anything GPU-heavy, any generation, or any cloud call.**

---

## 8. Manifests and provenance, by directory

Every directory below carries the tool-native `manifest.json` (as shipped) plus,
where the kickoff's fields weren't already in it, a sibling `provenance.json`
(tool sha256, package versions, HEAD commit, input hashes, parameters) written by
`write_provenance.py`, unmodified after writing:

- `flow\manifest.json` — self-contained (written by `run_flow.py`): estimator tool
  sha256 `9e1c050d6781cfe5433e7b1207b6b957e21475dd215fc18472b11d43b3e97735`, driver
  sha256, HEAD `46acaee6dc7e175c1a523471e92bdb97e6414cc8`, python/numpy/scipy/PIL
  versions, AOV bundle manifest sha256
  `41f3392d430cfed6adf87da3d67eae237d2fb0f635e7543ae0798b64c898f3e3`, per-view input
  file hashes (`depth_edge.npy`, `twin.png`, `sil.npy`).
- `s3_off\manifest.json` (tool-native) + `s3_off\provenance.json`.
- `s3_on\manifest.json` (tool-native) + `s3_on\provenance.json`.
- `sheets_off\manifest.json` (tool-native, includes per-file sha256 of everything
  consumed) + `sheets_off\provenance.json`.
- `sheets_on\manifest.json` (tool-native, same) + `sheets_on\provenance.json`.

`s3_composite.py` sha256 `c79f79998d9d4b78c4fc34dd54ca495e668e5927066a4e9659b460f4
1bc458f2`; `s3_run.py` sha256 `971c6408e5aa055ba7bd0c5992b24529ddef930a5d8e8f87a06a
7097dcf298bd`; `s3_sheet.py` sha256 `61172f284751fd89bbe66d07e746255792220a4d8bb4a2
c3b4b6115493cb4efb`. Env throughout: python 3.13.13, numpy 2.4.6, scipy 1.17.1,
PIL 12.2.0 (no open3d dependency in any of the four tools this arc runs).
