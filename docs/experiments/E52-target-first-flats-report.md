# E52 report — does the target-first compositor carry the flat class?

**Executor seat, Sonnet, background, 2026-08-17. Dispatched by the advisor seat against
`docs/experiments/E52-target-first-flats-kickoff.md`.** Zero spend: no GPU generation, no
cloud, no credits. Every number below comes from files already on disk. Working tree:
`E:\AI\training\facet_E52\` (uncommitted; not written into any other `facet_E4*`/`facet_E5*`
tree). `handoff.md` in that tree carries the running log with timestamps; this report is
the summary for the advisor's fold.

This report states measurements. It does not state whether the result is good, whether
target-first should ship, or what to do next — that is the advisor's and the Director's.

---

## Gates

All four held. None fired. No parameter was changed and re-run at any gate.

### Gate A — frame correspondence

**HELD.** Dimensions: arm A (`facet_E48/renders_owner_complete/owner_complete_0.png`) and
every one of B/C (`facet_E46/s3_off/t00..t07/{independent,dependent}.png`) are `752x1024`,
matching `tools/s3_sheet_regions.json`'s stated frame. Checked by direct `PIL.Image.size`
read on all 17 files (A plus 8x2), not assumed from a shared-cams claim.

Region correspondence: the `flat_trace.CALIBRATION_BOX` `(y0=490,y1=540,x0=280,x1=360)`,
converted to s3_sheet's `[x0,y0,x1,y1]` convention, was cropped out of A, B(t00), C(t00)
with `s3_sheet.crop_nn` (reused function, not reimplemented) at zoom 6 and viewed. All
three land on the same body structure — the collar/neckline where the tunic meets skin and
the gold pauldron corner. Evidence: `gate_a_sidebyside.png`, `gate_a_crop_*.png`,
`gate_a_wide_*.png` in the E52 tree.

**Disclosure required by the dispatch:** this crop is a qualitative look at C's actual
content, taken before `predictions.md` was written, because Gate A's own text requires
verifying region correspondence "by measurement" across all three arms including C. That
glance is recorded in `predictions.md`'s blindness section. It turned out to be a
**misleading** impression (see P1 below) — the wide, lightly-zoomed crop looked cleaner in
C than the tight, correctly-boxed, higher-zoom measurement later showed. Recorded as a
finding in its own right: a qualitative glance at this zoom level was not a reliable stand-in
for the classifier.

### Gate B — the instrument reproduces its own pinned claim

**HELD**, by two independent routes.

1. `flat_trace.py --selftest` (direct CLI invocation): exit 0, printed
   `owner-twin == (180, 90, 50)  same-xy is not  (E50 olive window: n=115 owner6=97)`.
2. The actual pinned pytest suite, run for real rather than reproduced by hand:
   `pytest tests/test_t89_flat_trace.py -v --basetemp=E:\AI\training\facet_E52\pytest_scratch`
   — **6 passed**, including the real-artifacts-tier
   `test_t89_collar_olive_is_owned_by_view_6`, which reads `facet_E49` (not `facet_E48`;
   see below) read-only.

**A discrepancy surfaced and was resolved, not assumed away.** The E52 dispatch and kickoff
spec name arm A as `facet_E48/renders_owner_complete/owner_complete_0.png`. T89's own
`@pytest.mark.artifacts` leg reads the same-named file under `facet_E49` instead — a
**different, later atlas build** (E49 has `orphan_fill_mask.npy` / `no_view_visible_mask.npy`
that E48 lacks). `gate_b_check.py` ran the pinned check against both directories directly:

| candidate | olive n (box) | owner hist | render sha256 differs from other? | owner.npy sha256 differs? | surfid.npy sha256 differs? |
|---|---|---|---|---|---|
| E48 (dispatch-named arm A) | **115** | `{-1:8, 0:9, 6:97, 7:1}` | yes | yes | no (identical) |
| E49 (T89's own artifacts-leg path) | **115** | `{-1:8, 0:9, 6:97, 7:1}` | yes | yes | no (identical) |

Both give the pinned `n=115`, `owner6=97` exactly, despite the render and atlas `owner.npy`
being byte-different between the two builds (only `surfid.npy` is byte-identical — expected,
since surfid is a function of the mesh/UV layout, not the atlas fill). Two independently
built atlas iterations agree at this anchor region. This arc used the E48 path throughout
(as named by the dispatch) since it reproduces the pinned claim exactly; the E49 agreement is
reported as corroborating evidence, not a substitution.

### Gate C — B and C are one run

**HELD, structurally**, not just from timestamps. `tools/s3_composite.py`'s
`s3_composite()` returns **both** `"dependent"` and `"independent"` colour fields from one
call per target; `tools/s3_run.py`'s `run()` writes both PNGs inside the same loop
iteration from that single call (`s3_run.py:141-142`). `facet_E46/s3_off/manifest.json`
and `provenance.json` show one `s3_run.py` invocation, `primary_mode="target"`, all 8
targets, `alpha=6.0`, `primary_floor=0.05`, one `tool_sha256` pair recorded for
`s3_run.py`/`s3_composite.py`. B and C cannot have come from different invocations by
construction of the code that produced them.

### Gate D — no write outside the E52 tree

**HELD.** Every `Write`/script output in this session targeted
`E:\AI\training\facet_E52\` (including its `sheets_main/`, `sheets_target0_with_A/`, and
`pytest_scratch/` subdirectories). `facet_E50` and `facet_E51` were never read. `git status`
in `E:\AI\facet` before this report was written shows only pre-existing advisor-side
uncommitted state (`docs/advisor-kickoff.md` modified, `docs/experiments/
E53-compound-occupant-ruling.md` untracked) that predates this session, plus this report
file itself, added last. `tools/__pycache__` etc. appeared from importing repo modules at
runtime; confirmed gitignored via `git status --ignored`, not a repo content change.

---

## Calibration

Required before any count is reported. Both populations measured on **arm A only**, per
the spec (the classifier's behaviour is a fixed, deterministic pixel-threshold rule —
`g>90, r>70, b<140, g+10>=r, g>b+15` — so "calibration" here means confirming a chosen
definitely-no region does not itself cross those thresholds, not estimating a fuzzy
model's range).

| population | box (x0,y0,x1,y1) | area | olive n | share |
|---|---|---|---|---|
| **definitely-yes** (T89 anchor) | `[280,490,360,540]` | 4,000 | **115** | 2.875% |
| **definitely-no** ("grip": hand/gold-ring/tunic-sliver, zero overlap with the anchor box, confirmed programmatically) | `[225,555,275,680]` | 6,250 | **28** | 0.448% |
| (secondary, not used as primary) "blade" (steel sword) | `[210,80,330,500]` | 50,400 | 252 | 0.500% | — **overlaps the anchor box by ~500px**, flagged rather than used as the clean no-population |

Separation: definitely-yes reads ~6.4x the definitely-no rate (2.875% vs 0.448%). Neither
"no" candidate reads exactly zero — both sit in the same 0.4-0.5% range this repo's other
arcs have already established as ordinary material-boundary speckle (CLAUDE.md cites a
0.06-0.33% clean baseline and a 5-104px range elsewhere). This is a real but imperfect
separation, reported as such — not rounded up to "clean."

---

## Predictions vs outcomes

Full text in `predictions.md`, written before any `olive_mask()` call on B or C. Two forms
of non-blindness were disclosed there before the fact: (1) Gate A's required crop of C(t00),
and (2) `box_coverage_check.py`'s pre-run of coverage-only metadata (not colour) to bound
the bands. Both are named in `predictions.md`, not discovered after the fact.

### P1 — olive count in C vs B at target 0

- **B band predicted: 20-150.** Measured: **B=38** (lcc=9). Inside band. HIT.
- **C band predicted: 0-30, and directionally < B.** Measured: **C=40** (lcc=25).
  **MISS.** C is not only outside the predicted band, it is **larger than B**
  (delta = +2), which was the pre-registered falsification condition
  ("Falsified if C's count >= B's count"). The (non-blind) visual glance during
  Gate A had suggested the opposite direction; the tight, correctly-boxed
  measurement and the zoomed crop (`region_grid_all8.png`, row t00) both show the
  olive/khaki patch clearly present in C, not reduced, and more contiguous (C's
  largest connected component is 25px vs B's 9px).

### P2 — colour of what replaces the removed pixels, target 0

Pre-registered operationalization: R = pixels olive-in-B and not-olive-in-C (the
"recovered" set); T = a fixed reference population (padded box minus the anchor box minus
olive/skin/gold/near-black, thresholds fixed before running against R).

- **R (recovered): n=17.** Mean RGB in C = `(56.9, 73.4, 46.7)`.
- **T (tunic-like reference): n=62,293.** Mean RGB = `(62.8, 56.5, 40.7)`, std=40.5.
- **RGB distance R-to-T = 18.86** (predicted band: <30 supports "recovered by correct
  tunic paint"). **HIT** on this narrow claim — R sits far closer to the tunic reference
  than to a skin reference (distance 130.2) or a gold reference (distance 135.9).

**But this is half the picture, and an honest report characterises both halves.** The net
delta at t00 (+2) is small only because R (17 "recovered" pixels) is nearly cancelled by
**G = 19 "gained" pixels** — olive-in-C but not olive-in-B — which was not part of the
pre-registered P2 but was measured once the net delta turned out non-zero in the "wrong"
direction (`measure_gained.py`). G's mean colour in C is `(100.1, 113.3, 72.6)` — squarely
olive by the spec. G's mean colour **in B, before**, was `(8.5, 21.2, 15.4)` — near-black,
i.e. **these 19 pixels were uncovered (background) in B and became olive-painted coverage
in C**, not a recolouring of already-painted pixels. This is a different mechanism from R:
R is "C repaints an already-olive B pixel with tunic colour"; G is "C paints olive into a
gap B left uncovered." Both were measured; neither was anticipated in the pre-registered
P2, which asked only about the removed pixels.

### P3 — direction agreement across the 8 targets

- **Predicted: 6-8 of 8 targets show C_olive <= B_olive** (non-increase) in this fixed
  pixel window. Hard falsification line pre-stated: "fewer than 5 of 8."
- **Measured: 5 of 8** (decrease=2, same=3, increase=3). **Below the predicted band**
  (6-8), though not below the separately-stated hard falsification floor (5 is not fewer
  than 5). Reported as a band miss, distinct from the harder falsification criterion,
  rather than rounding it into either "hit" or "falsified."

Per-target table (box area 4,000px throughout):

| target | B olive n (lcc) | C olive n (lcc) | delta (C-B) | direction |
|---|---|---|---|---|
| t00 | 38 (9) | 40 (25) | +2 | increase |
| t01 | 8 (2) | 4 (2) | -4 | decrease |
| t02 | 31 (2) | 25 (3) | -6 | decrease |
| t03 | 0 (0) | 0 (0) | 0 | same |
| t04 | 0 (0) | 0 (0) | 0 | same |
| t05 | 0 (0) | 0 (0) | 0 | same |
| t06 | 23 (5) | 64 (59) | **+41** | increase |
| t07 | 36 (6) | 110 (25) | **+74** | increase |

**Per the spec's own framing, agreement does not poll the region's cause; disagreement at
any one target closes the question for that target specifically.** t06 and t07 close it:
target-first does not uniformly suppress olive/khaki content in this window, and at t06 and
t07 it increases sharply — both in absolute count and in connectedness (t06's largest
connected component grows from 5px to 59px; t07's from 6px to 25px).

A partial mechanistic note, from the same measurement, reported as evidence not
interpretation: t06's target is view 6, the view T89 already identified as the contributor
of the original olive paint at target 0's anchor. At t06, `measure_gained.py` shows the 59
gained pixels' mean colour changed only slightly between B and C (`(109.8,102.5,76.0)` in B
before vs `(104.7,101.7,72.7)` in C) — a small shift across the classifier's threshold
boundary, not a new colour appearing. t07 shows the same small-shift pattern
(`(135.4,123.5,89.4)` before vs `(129.3,122.4,96.8)` after). This differs from t00's G set,
where the colour change was large (near-black to olive) because those pixels went from
uncovered to covered.

---

## Where the sheets are

Two sheets built via `tools/evidence.py sheet` (reused, unmodified) against a local regions
file `E:\AI\training\facet_E52\e52_regions.json` (does not touch the shared
`tools/s3_sheet_regions.json`; documented reasoning is in that file's own `"label"` field).

- **`E:\AI\training\facet_E52\sheets_main\sheet_v00.png` .. `sheet_v07.png`** — one per
  target, columns `reference | B_independent | C_dependent`, FULL-frame row plus the
  `collar_olive` region row at **zoom=1 (true native pixels, no scaling)**, per the spec's
  literal wording ("native pixels, no downscale"). Provenance panel (sha256 + path of every
  file actually read) is baked into each sheet by the tool itself.
- **`E:\AI\training\facet_E52\sheets_target0_with_A\sheet_v00.png`** — target 0 only,
  4 columns `reference | A_owner_complete_NOT_ONE_VARIABLE | B_independent | C_dependent`.
  Arm A is a **literal, non-templated path** (`owner_complete_0.png` only) so it cannot be
  mistaken for per-target arm-A data on other views, matching the spec's "arm A's same
  region on the target-0 sheet only, labelled as the not-one-variable row."

**What did not fit, and what was built instead, disclosed per the spec's own instruction:**
the region row at zoom=1 is technically correct (native pixels, as specified) but is only
50x80px per panel — too small to read at a glance. `build_zoomed_region_grid.py` calls
`s3_sheet.crop_nn` **directly** (the same function the sheet tool calls internally, not a
reimplementation) at zoom=8 for legibility only:

- **`E:\AI\training\facet_E52\region_grid_all8.png`** — all 8 targets, reference|B|C, zoom 8.
- **`E:\AI\training\facet_E52\region_row_t00.png` .. `region_row_t07.png`** — same, per-target.

Additional diagnostic crops from the gate/calibration/P2 work (also in the E52 tree):
`gate_a_sidebyside.png`, `gate_a_crop_*.png`, `gate_a_wide_*.png`, `cal_no_grip_v0.png`,
`cal_no_blade_v0.png`, `p2_R_overlay.png` (R in red over C, t00), `p2_T_overlay.png` (R red
/ T blue over C, t00), `p2_RG_overlay_box.png` (R red / G orange over C, t00, tight box),
`box_t06_B.png`/`box_t06_C.png`/`box_t07_B.png`/`box_t07_C.png`.

---

## Provenance

`E:\AI\training\facet_E52\provenance_manifest.json` — sha256 of all **55** input files this
arc read (0 missing): arm A candidates (both E48 and E49), all 16 B/C files, all 8
coverage.png/owner.npy pairs, the S3 manifest/provenance JSON, all 8 reference twins, and
the 6 repo tool/test files imported or invoked (content-pinned, not just path-pinned).

---

## Standards compliance (this execution, not the dispatch's own pre-score)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every input file used anywhere in this arc is content-pinned by sha256 in `provenance_manifest.json` (55 files, 0 missing), not just path-named. The instrument (`flat_trace.py`) was invoked unmodified via both direct CLI and the actual pinned pytest suite. The sheet tool's own provenance panel independently re-hashes every file it reads. |
| ANDON_AUTHORITY | **2** | Four gates were defined, checked with real evidence, and none fired. Scored 2 not 3 because my own gate-check scripts (`gate_a_check.py`, `gate_b_check.py`) are diagnostic/read-only code that reports and lets me (the executor) decide to halt, not repo tool code with a hard `raise` — appropriate for a measurement arc with no irreversible step, but it means the halt mechanism was never exercised under fire (no gate actually failed to test the halt path). |
| NAMED_COMPENSATORS | **3** | The only writes are under `E:\AI\training\facet_E52\` plus this report file. No irreversible call exists anywhere in this arc — no publish, no push, no generation, no repo-tool edit. Compensator is delete-the-tree (training tree) / revert-the-file (report); owner is the advisor. |
| DECOMPOSE_BY_SECRETS | **3** | Work is split into independently-runnable scripts by concern: `gate_a_check.py` (frame correspondence), `gate_b_check.py` (instrument reproduction), `calibration_check.py` (yes/no populations), `box_coverage_check.py` (coverage denominators), `measure_b_vs_c.py` (P1/P3 core), `measure_gained.py` (P2 symmetric characterisation), `build_zoomed_region_grid.py` (legibility), `provenance_manifest.py` (hashing). None depends on another's internal state; each writes its own named JSON. |
| UNCERTAINTY_GATED_HUMANS | **3** | No pass condition was invented (per the spec's explicit "no pass condition, by design"); the terminus is the sheet plus separated numerator/denominator numbers for the Director's eye. The one genuinely judgment-laden choice in this arc — which region to use as "definitely-no" for calibration — was resolved by measuring both candidates and picking the one with zero box overlap, with the reasoning and both numbers reported, rather than escalated (a methodology choice squarely inside the executor's mandate, not a decision only the Director can make). |
| EXTERNAL_VERIFIER | **2** | `olive_mask()` was invoked unmodified throughout, never re-derived independently. Two forms of partial cross-checking exist: Gate B's pinned claim was reproduced via two independently-built atlas datasets (E48, E49) and via two independent invocation paths (a hand-written script and the actual pinned pytest suite) — both converge. But the core P1/P2/P3 measurement on B and C ran through one classifier, one time, with no differently-sourced second computation over the same pixels. |

---

## Out of scope (named, not silently skipped)

- **Twin regeneration.** Not touched.
- **Any cloud or GPU generation.** None occurred; every measurement is disk-only, confirmed
  by the fact that no network/Comfy/Blender tool was invoked anywhere in this session.
- **`s3_on/` (flow arm).** Exists on disk under `facet_E46`, untouched. Not read.
- **The atlas path and `atlas_from_aovs.py`'s own packing/dilation/orphan-fill.** Not run;
  `atlas_from_aovs` was only imported transitively (by `flat_trace.py`) and never invoked to
  build anything.
- **The compound-occupant question.** Not this arc's; per the spec, it needs the Director's
  word on a spend.
- **Repairing anything.** This arc measured; nothing in `tools/` was edited.
- **`owner_complete_1.png` .. `owner_complete_7.png`.** These exist on disk under
  `facet_E48`/`facet_E49` but were deliberately never treated as "arm A" for targets 1-7,
  per the spec's explicit restriction of arm A to target 0 only. The `sheets_target0_with_A`
  sheet's arm-A column is a literal path, not a `{v}`-templated one, specifically so this
  scoping cannot leak.
- **Full colour characterisation (R/T/skin/gold reference sets) for targets other than 0.**
  P2 was pre-registered for target 0 only. Basic before/after colour stats for t06/t07's
  gained-pixel sets were measured once their deltas turned out to be the largest in the P3
  scan (reported above), but the full R/T/reference-population apparatus built for t00 was
  not re-run per-target — that would be a natural follow-up, not done here.
- **A ΔE/CIE-Lab colour pipeline.** No such pipeline exists in this tree; P2's "close to
  tunic" claim is measured in 0-255 RGB Euclidean distance, named explicitly as a coarser
  proxy in `predictions.md` before it was used.
- **`E:\AI\training\facet_E52\pytest_scratch\`.** pytest's own `--basetemp` working files
  from running `test_t89_flat_trace.py`; not a meaningful arc artifact, listed here so its
  presence in the tree is accounted for rather than unexplained.

---

## Negative-result statement

Per the dispatch's own rule ("a negative result is a full success"): **the measured
evidence at the anchor region does not show target-first suppressing the olive/khaki flat
class.** At target 0 the count went up by 2 (with real churn underneath: 17 pixels
recovered to tunic-like colour, 19 gained from previously-uncovered gaps into olive
coverage). At two of the other seven targets (t06, t07) the count rose sharply (23->64,
36->110), both identified as views whose own contributed paint is close to the olive/khaki
tone. Only two of eight targets (t01, t02) showed a clean decrease. This is reported
plainly, without retuning the box, the threshold, or the calibration population to produce
a friendlier number.
