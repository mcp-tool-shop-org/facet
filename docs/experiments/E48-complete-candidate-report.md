# E48 report — complete candidate renders, the rebuilt-atlas route end to end

Executor seat (Sonnet tier), dispatched 2026-08-16 late at HEAD
`e9e19c56dcccbafd926d24856d0520ec8cf674c6`, immediately after the Director rejected
all four E47 cells ("I don't see any recovered images. They all still look
broken."). Dispatch: `docs/experiments/E48-complete-candidate-kickoff.md`. Full
working record: `E:\AI\training\facet_E48\handoff.md` (kept current through every
step) and `E:\AI\training\facet_E48\predictions.md` (written before step 2 ran).
HEAD did not move during this arc; `git status --short` is clean except for this
file.

No word in this report asserts that any result is good, working, or decisive. Every
number below is a measurement; the sheets under `E:\AI\training\facet_E48\sheets\`
are the artifact for the Director's eye.

## 1. Predictions (written before step 2 ran — full text in predictions.md)

Blind status: blind with respect to every number this arc's own scripts produced —
none existed when `predictions.md` was written. Not blind to two figures already on
record elsewhere, named at the point of use in `predictions.md`: CLAUDE.md's
recorded 100%/100%/77.6% stratum-loss figure for a related-but-different erosion
mask on this mesh, and E47's own coverage/per-texel-delta tables.

| | P1 — erosion loss per half-width band | P2 — zero-written-island count | P2 — sentinel visible, views 0/1/2 | P3 — boundary render delta |
|---|---|---|---|---|
| predicted | 1-2px 60-100% (often unreported); 2-4px 50-100%; 4-8px 25-70%; 8-16px 10-40%; 16-32px 3-20%; 32px+ 0-15% | [1, 500] of 18,915 islands | visible on at least one of the three | substantially larger than E47's flow-on-vs-off deltas; exact metric left TBD, to be decided at step 4/5 |

## 2. What ran

| step | tool | result |
|---|---|---|
| Gate S | `tools/atlas_from_aovs.py --selftest` | `atlas_from_aovs selftest OK  calibration atlas[16,16,0] == 0.5`, exit 0 |
| Gate S | `--anchor --aov facet_E45\aov --prep facet_E06\C1\prep` | `\|bmid\|=0.000e+00 \|v_ext\|=0.000e+00 \|h_ext\|=0.000e+00 valid=2402810`, exit 0 |
| Step 1 | `erode_bundle.py` (training dir) | exit 0, derived bundle written, source hash-confirmed unchanged |
| Step 2 | `atlas_from_aovs.py` × {owner, blend}, flow off | both exit 0 |
| Step 3 | `fill_islands.py` (training dir) | both exit 0, boundary/accounting checks clean |
| Step 4 | `facet_E47\render_atlas_swap.py` (unmodified, reused directly) via Blender `-b -P`, PowerShell | both exit 0, 16 renders |
| Step 5 | `build_sheets_e48.py` (training dir) | exit 0, 8 sheets, no missing panels |
| P3 | `boundary_delta.py` (training dir) | exit 0 |

Gate S matches the recorded precedent exactly (`|bmid|` 0.000e+00, valid-texel count
2,402,810).

## 3. Step 1 — sampling-trust erosion (`erode_bundle.py`)

The A3 rule is copied with citation from `tools/project_twins.py` (not import-safe —
calls `ap.parse_args()` at module level — so copied rather than imported, the E41
pattern): `dist_in = EDT(sil)`; `thick = local_thickness(dist_in)` (imported from
`tools/mask_geometry.py`, which is import-safe and is what `project_twins.py` itself
does — `local_thickness = mask_geometry.local_thickness`); `fig_w` = this view's own
`sil` column-extent bbox width; `esc = fig_w / 700.0`; `ed_body = max(2.5, 7.0*esc)`;
`e_img = min(ed_body, thick/3)`; kept texels are `dist_in >= e_img`.

Two named deviations from `project_twins.py`'s own use of this formula: (1) this
arc erodes `sil` (the AOV bundle's geometric visibility mask), not `fm` (project_
twins' own twin-paint-key ∩ mesh-silhouette trust mask) — the AOV/s3 pipeline has no
twin-paint-key concept, `twin.png` is sampled directly with no separate presence
test; (2) no head/body distinction — `ed_body` applies uniformly across each
view's whole silhouette; porting the front-view head-crop rectangle into each of
the 8 independent camera spaces was not attempted.

The spec's own shorthand for the rule ("min(2.5 px, 0.333 × local half-width)") is
not what the code computes — `ed_body` is `max(2.5, 7.0*esc)`, not a flat 2.5.
Measured per view (table below), `ed_body` runs 2.79-4.17px, i.e. 1.12×-1.67× the
2.5px floor — the `7.0*esc` term is always the larger of the two on this figure, so
the floor never binds at any view; the spec's flat "2.5 px" undercounts `ed_body`
at every one of the 8 views. The literal code is what this arc used; the
discrepancy is reported, not resolved either way.

**Per-view result** (sil px before → after; `ed_body` computed per view from that
view's own `sil` bbox width):

| view | fig_w | ed_body | sil before | sil after | removed | removed % |
|---|---|---|---|---|---|---|
| 0 | 388px | 3.88px | 146,356 | 133,294 | 13,062 | 8.92% |
| 1 | 417px | 4.17px | 149,780 | 134,677 | 15,103 | 10.08% |
| 2 | 279px | 2.79px | 90,553 | 83,997 | 6,556 | 7.24% |
| 3 | 304px | 3.04px | 120,439 | 112,028 | 8,411 | 6.98% |
| 4 | 388px | 3.88px | 146,356 | 133,294 | 13,062 | 8.92% |
| 5 | 417px | 4.17px | 149,780 | 134,677 | 15,103 | 10.08% |
| 6 | 279px | 2.79px | 90,553 | 83,997 | 6,556 | 7.24% |
| 7 | 304px | 3.04px | 120,439 | 112,028 | 8,411 | 6.98% |

Views pair up (0=4, 1=5, 2=6, 3=7) almost exactly in `fig_w` and pixel counts —
checked against a data-duplication bug directly (`sil`/`twin` arrays compared
elementwise between paired views: not equal, `sha256` differs) — consistent with a
roughly bilaterally-symmetric standing figure at paired front/back and
diagonal/diagonal camera angles, not a bundle defect.

**Per-band loss** (`edge_min_struct=50` floor; identical across paired views):

| half-width band | n (view 0/1/2/3) | loss % (view 0/1/2/3) |
|---|---|---|
| 1-2px | 11 / 9 / 24 / 4 | SKIPPED (< 50px) in every view |
| 2-4px | 129 / 92 / 212 / 68 | 0.0% / 0.0% / 0.0% / 0.0% |
| 4-8px | 1,068 / 685 / 1,797 / 485 | 54.4% / 63.8% / 28.6% / 58.1% |
| 8-16px | 5,213 / 4,593 / 15,023 / 6,429 | 41.7% / 43.1% / 19.2% / 32.3% |
| 16-32px | 22,207 / 27,668 / 6,533 / 7,844 | 21.1% / 22.8% / 15.8% / 30.9% |
| 32-infpx | 117,728 / 116,733 / 66,964 / 105,609 | 4.8% / 5.5% / 3.2% / 3.4% |

(Views 4-7 repeat views 0-3's numbers exactly, per the pairing above; full 8-view
table in `aov_eroded/erosion_manifest.json`.)

Loss is **not monotonic** with half-width: the 2-4px band loses 0.0% in every view
(n = 68-212, above the reporting floor) while the next band up, 4-8px, loses the
most of any reported band (28.6-63.8%). Offered as a hypothesis, not confirmed
independently: `local_thickness` assigns a pixel the radius of the largest disc
that *covers* it, which can be centred elsewhere on the mask, so a bridge or
transition pixel (e.g. a wrist, a strap crossing a limb) can inherit a "thicker"
classification from a nearby ridge while its own `dist_in` (distance to its
immediate boundary) stays small — under-supporting the very threshold its band
label implies it should clear.

`E:\AI\training\facet_E45\aov\` hash-confirmed unchanged, 81 files, before === after
(`erode_bundle.py`'s own ANDON, not fired). No view's silhouette went to empty (the
empty-silhouette ANDON did not fire).

## 4. Step 2 — paint (`atlas_from_aovs.py`, flow off, both modes)

| cell | mode | written / valid | pct |
|---|---|---|---|
| atlas_owner_eroded | owner | 1,964,313 / 2,402,810 | 81.76% |
| atlas_blend_eroded | blend | 1,677,233 / 2,402,810 | 69.81% |

Against E47's uneroded equivalents (owner-off 84.39%, blend-off 73.53%): owner
drops 2.63 points (-63,573 texels), blend drops 3.71 points (-89,531 texels) —
smaller in percentage-point terms than the 6.98-10.08% per-view `sil` reduction
from step 1, consistent with atlas coverage aggregating redundant multi-view
contributions (a rim texel lost in one view is not lost from the atlas if another
view still covers it there).

## 5. Step 3 — island-aware fill (`fill_islands.py`)

Islands: `E:\AI\training\facet_E08\ARMB\cache\isl_grid.npy`, shape (4096,4096)
int32, 18,915 island ids. Its valid (>=0) positions are elementwise identical to
`facet_E06\C1\prep\mask.npy`'s own valid mask (2,402,810 texels, exact position
match, not just count) — the same prep Gate S anchors against and
`atlas_from_aovs.py` itself consumes, confirmed by `recon_isl_and_bundle.py` before
any fill ran and re-confirmed at `fill_islands.py`'s own runtime. Producer
identified by grep, as the kickoff asked: identical `build_islands()` in
`tools/diagnostics/e04_blotch.py:189-221` and `tools/diagnostics/e07_gate0.py:
84-116`; `e04_blotch.py:242` is the only `np.save` of the cache. An island is a
UV-chart connected component (union-find over UV-space face adjacency), matching
the spec's "within the same island" reading.

Of the 18,915 island ids, only **11,600 have any texel at all in the 4096 grid**
(`scipy.ndimage.find_objects` returned no bounding box for the other 7,315) — a UV
chart can exist in the mesh's face topology and still rasterise to zero texels at
this resolution. Noted as an observation; not asked for by the spec.

| | owner | blend |
|---|---|---|
| written before fill | 1,964,313 | 1,677,233 |
| unwritten-valid before fill | 438,497 | 725,577 |
| islands: no fill needed | 7,114 | 4,564 |
| islands: filled | 2,683 | 3,411 |
| islands: **zero-written** (unwritten-valid present, no source anywhere in the island) | **1,803** | **3,625** |
| texels filled | 317,081 | 438,224 |
| zero-written-island total area | 121,416px | 287,353px |
| zero-written-island largest | 2,819px (island 11915) | 2,819px (island 11915, same id) |
| remaining sentinel | 121,416 / 2,402,810 = **5.053%** | 287,353 / 2,402,810 = **11.959%** |

The same island (id 11915) is the largest zero-written island in both modes,
consistent with a region no view's facing/visibility test reaches regardless of
mode. The boundary-crossing ANDON (every filled texel's island id compared against
its source texel's island id) checked 317,081 and 438,224 filled texels
respectively; no crossing in either mode. The accounting ANDON (remaining sentinel
must equal zero-written-island total area) held exactly in both modes.

**Against P2's predicted band [1, 500] for the zero-written-island count**: miss in
both modes — owner 1,803 (3.6× the predicted ceiling), blend 3,625 (7.25× the
ceiling). Reported as measured, not adjusted toward the prediction.

## 6. Step 4 — render (`facet_E47\render_atlas_swap.py`, reused unmodified)

Invoked directly by path (sha256
`8529a74de737d825227f5309f7c6e28dd08ac08178f2039ab83da6d2de793edd`, unchanged from
E47) rather than copied, since it is fully parameterised by CLI flags (`--glb
--atlas --out --tag`) and carries no path specific to E47's own run. Both
invocations targeted the shipped `facet_E08\ARMB\out\W3_final.glb` and reported the
same swap line E47's own run reported: `atlas_final (4096,4096) -> atlas_filled.png
(4096,4096) colorspace='sRGB'` — size and colorspace match, no override needed.

16 PNGs written (`renders_owner_complete/owner_complete_{0..7}.png`,
`renders_blend_complete/blend_complete_{0..7}.png`), counted complete (`Get-
ChildItem ... .Count`, not a truncated listing). Spot check, view 1 both sets:
(1024,752,4) uint8, mean≈170, std≈59-60, full 0-255 range.

## 7. Step 5 — the sheet (`build_sheets_e48.py`)

8 sheets, one per view, at `E:\AI\training\facet_E48\sheets\sheet_v00..07.png`:
`reference | shipped | owner-complete | blend-complete`, native 752×1024 panels,
provenance captions with sha256 for every panel. Views 0, 1, 2, 7 additionally
carry region-crop rows at 2× zoom.

Two named resource gaps, stated rather than patched: `tools/s3_sheet_regions.json`
has blade/grip boxes only for views 0, 1, 7 (view 2 has none — view 2's crop row
carries no blade/grip, matching E47's own precedent for its views 2/6 gap); no view
has a "head" region in that file at all. A head box was **derived** (not shipped)
per crop view: the top 22% of that view's own uneroded `sil` vertical extent,
padded 12px, labelled `[DERIVED, not a ruling]` on the sheet exactly as the file's
own `[PROPOSAL]` boxes are labelled.

**Visual description of all 8 sheets** (description, not judgment — the sheets
themselves are the artifact for the Director's eye):

- The `shipped` panel carries no magenta on any view, matching E47's own finding.
- `owner-complete` and `blend-complete` both show small magenta patches at
  full-figure scale on **every one of the 8 views**, concentrated at boot tops /
  lower legs, greave edges, gauntlet/wrist areas, and (views 2 and 5 particularly)
  torso/hip near the tunic seam. `blend-complete` carries visibly more magenta
  than `owner-complete` on most views, consistent with its larger zero-written-
  island area (11.959% vs 5.053% of valid texels).
- Blade crops (views 0, 1, 7): the `reference` and both `-complete` panels show a
  more spatially uniform light grey/silver blade than the `shipped` panel, which
  shows a light-top / dark-bottom split with a brown-toned patch near the guard;
  both `-complete` panels carry a small number of magenta pinpricks on the blade
  itself.
- Grip crops (views 0, 1, 7): both `-complete` panels show a more visible magenta
  patch on the handle than on the blade crop of the same view.
- Head crops (views 0, 1, 2, 7): no visible magenta difference between any of the
  four panels on any of the four views.

**Against P2's "sentinel visible on at least one of views 0/1/2"**: this
undersold the measurement — visible magenta appears on all eight views, both
modes, not on just one of the three named views.

## 8. P3 — boundary-strip render delta (`boundary_delta.py`)

Decided at this step, as `predictions.md` disclosed it would be. Kept to one space
throughout (render pixels, 752×1024) rather than crossing into atlas-texel space —
the practice this repo already holds (a dilation share is not a rendered-pixel
share). Boundary strip per view := `sil & (dist_in <= 8px)` over that view's own
original (uneroded) `sil.npy`, recomputed fresh from `dist_in` (no dependency on
step 1's in-memory arrays) — 8px is a round number above every view's own `ed_body`
(2.79-4.17px), sized to hold the eroded rim with margin. Compared this arc's
eroded-and-filled renders against E47's **uneroded, unfilled**
`renders_owner_off`/`renders_blend_off` cells, mean absolute RGB delta per pixel
(0-1 scale), restricted to the strip.

| | owner | blend |
|---|---|---|
| strip mean, range across 8 views | 0.0286 – 0.0509 | 0.0306 – 0.0517 |
| strip mean, average of 8 views | 0.0394 | 0.0408 |
| whole-silhouette mean, average of 8 views | 0.0176 | 0.0188 |
| strip ÷ whole-silhouette ratio | ≈2.24× | ≈2.17× |

The boundary strip carries roughly 2.2× its own whole-silhouette mean delta in
both modes — the delta concentrates near the original boundary, as the erosion's
own construction implies it should. The strip means are numerically larger than
E47's own flow-on-vs-off atlas-texel co-written means (owner 0.0209, blend
0.0156), but this is **not read as a direct comparison** — the two are measured in
different spaces (render pixels here, atlas texels there) and CLAUDE.md's own
record already treats a cross-space size comparison as invalid without a stated
conversion.

**Scoring note, disclosed plainly**: `predictions.md`'s P3 described a
"coverage-loss fraction of texels moving written-to-sentinel" metric with the
exact form left TBD until this step. The metric actually used — mean absolute
pixel delta in render space — is a different operationalisation from that
description. This is reported as a changed metric choice, not silently
reconciled against the original wording.

## 9. Predictions scored

| prediction | measured | result |
|---|---|---|
| P1 1-2px: 60-100%, often unreported | unreported in all 8 views (n=4-24, below the 50px floor) | consistent with "often unreported"; loss % itself untestable |
| P1 2-4px: 50-100% | 0.0% in all 8 views | miss |
| P1 4-8px: 25-70% | 28.6-63.8% | inside band |
| P1 8-16px: 10-40% | 19.2-43.1% (43.1% on views 1/5 exceeds the ceiling) | mostly inside band, one pair over |
| P1 16-32px: 3-20% | 15.8-30.9% (views 0,1,3,4,5,7 exceed the 20% ceiling; only 2/6 at 15.8% fit) | mostly miss |
| P1 32px+: 0-15% | 3.2-5.5% | inside band |
| P2 zero-written-island count [1,500] | owner 1,803; blend 3,625 | miss, both modes (3.6× / 7.25× the ceiling) |
| P2 sentinel visible on >=1 of views 0/1/2 | visible on all 8 views, both modes | direction correct, magnitude undersold |
| P3 boundary delta "substantially larger" than E47's flow deltas | numerically larger (render-space) than E47's flow deltas (atlas-space) | not scoreable as stated — cross-space; see §8 |

## 10. Deviations / halts

None. Gate S held. No ANDON fired anywhere in the chain: erosion's empty-
silhouette guard, the island-fill boundary-crossing guard (checked on 317,081 and
438,224 filled texels), the island-fill accounting guard, and the render script's
mesh/material/node-count and atlas-size guards all ran clean.

## 11. Artifacts

All under `E:\AI\training\facet_E48\`:

```
handoff.md                              live working record
predictions.md                          written before step 2 ran
recon_isl_and_bundle.py                 isl_grid.npy premise check
erode_bundle.py                         step 1 tool + erosion_manifest.json
aov_eroded/                             derived AOV bundle (sil eroded, all else copied)
atlas_owner_eroded/, atlas_blend_eroded/  atlas.png, owner.npy, weight.npy, manifest.json
fill_islands.py                         step 3 tool
  atlas_{owner,blend}_eroded/atlas_filled.png, filled_mask.npy, fill_manifest.json
  fill_summary.json
renders_owner_complete/, renders_blend_complete/  8 views each, flat
build_sheets_e48.py                     step 5 tool
sheets/sheet_v00..07.png, sheets/manifest.json
boundary_delta.py, boundary_delta.json  P3 tool + numbers
```

`git status --short` in the repo confirms this report is the only change in the
tree; nothing else was committed, pushed, or written to the memory store.
