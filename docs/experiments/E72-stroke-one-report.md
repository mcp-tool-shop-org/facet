# E72 report — Stage 0: the stroke-one groundwork, zero spend

Executor seat (Sonnet), background. Charter: `docs/experiments/E72-stroke-one-kickoff.md` +
AMENDMENT 1 (read first, per the dispatch's own instruction). Working tree:
`E:\AI\training\facet_E72\`. Live handoff kept throughout: `E:\AI\training\facet_E72\
handoff.md`. Predictions written and committed to disk BEFORE any `emit` ran:
`E:\AI\training\facet_E72\predictions.md`.

**SCOPE: STAGE 0 ONLY, AS DISPATCHED. ZERO CLOUD SPEND.** No comfy-cloud tool was loaded or
invoked. No stroke was emitted for real generation. No workflow JSON was built or submitted.
`canon/a1.surfaces.json` was not edited (the Director ratifies canon). `project_twins.py` was
not run. No threshold was retuned. Nothing was committed to git.

## What this arc cannot do — restated in my own words, per the dispatch's explicit request

The Director ruled (2026-08-19) that the vertical peach banding across A1's face is **view
ownership at UV chart boundaries**: styled texels with different owning cameras
(`project_twins.py:936-939`, winner-take-all). `texpass_iter.py` commits new paint into HOLE
texels only — styled texels are asserted untouched by the tool's own gate, both at `commit()`
and again at `selftest`. **The brush has no mechanism that can reach the banding, and nothing
in this arc changes that.** If a future sheet still shows the bands, that is the expected,
structural outcome — not a defect of anything measured here. Evening the face is explicitly
out of scope for this arc and for stroke one; two candidate remedies exist and are enumerated
in AMENDMENT 1 for a later sitting, not commissioned here.

## ⚠ Two mid-arc corrections received from the coordinator, both attributed, both re-verified
## at source rather than taken on trust — per this repo's own "advisor corrections" convention

**Correction 1** (received after step 2, before any `emit` ran): the dispatch's own literal
`emit`/`selftest`/`brush_cloud_step.py graph` invocations omit `--profile`/`--aspect`
entirely and would have run at the WRONG frame — `tools/texpass_iter.py:133`'s E14 Ruling 29c
ANDON exists to catch exactly a missing `--profile`+`--aspect`, but the correction additionally
flagged that `selftest`'s internal `emit()` call never passes through that ANDON's own
top-level `args.mode == "emit"` guard, so a forgotten frame there would be SILENT, not caught.
Also flagged: `brush_cloud_step.py graph --profile` is `required=True` (`:156`, E04 Ruling
24), confirmed directly by me reading that file's own argparse setup independent of the
correction; and `tools/superseded`-style caution that `e70_build_sheet.py` is not a reusable
tool as the dispatch's Stage-1 sheet section implies.

**Correction 2** (received minutes later, self-superseding one detail of Correction 1): the
coordinator's own first fix said prefer `--profile` as the frame source; a follow-up,
source-verified before I acted on it, corrected that specifically —
`profiles/a1.json` carries **no** `texpass_iter.py` block (until step 7 of this arc), so
`--profile` ALONE would have **silenced** the ANDON (`args.profile is None` becomes `False`)
while the frame silently fell through to the tool's own `--aspect` default (`752,1024`, W3's
portrait frame) — a green gate over the exact wrong-frame failure the gate exists to catch,
reached through a different door than Correction 1 itself proposed.

**Verified, not merely trusted, before treating either correction as satisfied:** every
`emit`/`selftest` call in this session (see the exact argv under each step below) already
passed **both** `--profile profiles\a1.json` **and** explicit `--aspect 576,1024 --fit-axis
height --margin 1.204` on the command line — my own independent decision, made and written
into `handoff.md` before either correction arrived, for the same belt-and-suspenders reason
the corrections later gave in detail. **All 8 step-3 `cam.json` files, plus the `selftest`
job's, were read directly (9 files, not sampled) and every one reads `"W": 576, "H": 1024`.**
No emit or selftest call from this session needed to be voided or re-run.

Independently re-verified rather than relayed on trust: `tools/brush_cloud_step.py`'s `graph`
subparser does declare `--profile` with `required=True` (read directly, matches Correction
1's citation); `E:\AI\training\facet_E70\scripts\e70_build_sheet.py:14` does hardcode
`ROOT = r"E:\AI\training\facet_E70"`, and lines 29-30 do hardcode `MESH_SHA`/`ATLAS_SHA`
literals (checked directly against the file, matches Correction 1's citation on both counts).

This session's own fifth-of-one-shape count (per the coordinator's framing): the CJK
`_negative` transcription bug at step 6, below, which I found and fixed myself rather than
being told about — recorded in `handoff.md` in full, including the console crash the
diagnosis itself triggered (a `repr()` of a CJK string on this rig's cp1252 console —
CLAUDE.md's own documented trap, hit for real, mid-diagnosis, harmlessly since it happened
after the useful comparison output had already printed).

## Step 1 — state directory built (copy, never rename in place)

Copied `E:\AI\training\facet_E69\bake\atlas_widescope.png` /
`atlas_widescope_holes.png` / `atlas_widescope_styled_mask.npy` into
`E:\AI\training\facet_E72\state\` as `atlas.png` / `holes.png` / `styled_mask.npy` (the exact
three names `texpass_iter.py`'s own docstring requires — NOT `_blend.png` or `_owner.npy`,
neither of which the tool reads). Source hashes recorded before the copy and re-verified
identical after ALL other work in this session (Gate C, closed at the end, not just opened):

| file | sha256 | unchanged at close |
|---|---|---|
| `atlas_widescope.png` | `66b8602b...08727f2` | **YES** |
| `atlas_widescope_holes.png` | `63007f6e...80069ac2` | **YES** |
| `atlas_widescope_styled_mask.npy` | `78ccef3d...42fa765d7` | **YES** |

(Full hashes in `E:\AI\training\facet_E72\logs\step1_source_sha256_before.json`; the E69 atlas
hash also matches E70's own recorded value from its report, an independent cross-check.)

## Step 2 — GLB packed

`blender -b -P tools\bake_hero_pack.py -- --prep-glb E:\AI\training\facet_E67\prep\
prep_uv.glb --atlas E:\AI\training\facet_E72\state\atlas.png --out E:\AI\training\
facet_E72\pack\a1_e72_packed.glb` — exit 0. Output: 37,138 KB (~38.0 MB, consistent with
E70's own packed GLB at the same mesh/atlas resolution, 38,029,352 bytes). Console:
`E:\AI\training\facet_E72\logs\step2_pack_console.txt`.

## Step 3 — per-view brush canvas, measured, all 8 yaws

Exact argv, every call (only `--yaw` varies):

```
E:\AI-Models\trellis2-env\Scripts\python.exe E:\AI\facet\tools\texpass_iter.py emit
  --state E:\AI\training\facet_E72\state
  --prep E:\AI\training\facet_E67\prep
  --glb E:\AI\training\facet_E72\pack\a1_e72_packed.glb
  --yaw <0|45|90|135|180|225|270|315> --el 0
  --profile E:\AI\facet\profiles\a1.json
  --aspect 576,1024 --fit-axis height --margin 1.204
```

All 8 exit 0. All 8 `cam.json` files read directly, all read `"W": 576, "H": 1024"`.

| view idx | yaw | figure px (`hit.sum()`) | hole px (`hm.sum()` — the brush canvas) | hole/figure % |
|---:|---:|---:|---:|---:|
| 0 | 0   | 174,952 | 43,747 | 25.00% |
| 1 | 45  | 159,375 | 37,699 | 23.65% |
| 2 | 90  | 106,893 | 17,868 | 16.72% |
| 3 | 135 | 159,976 | 23,346 | 14.59% |
| 4 | 180 | 174,952 | 20,309 | 11.61% |
| 5 | 225 | 159,376 | 23,471 | 14.73% |
| 6 | 270 | 106,893 | 19,174 | 17.94% |
| 7 | 315 | 159,976 | 38,381 | 24.00% |

`hm.sum()` is a **screen-space pixel count** (576x1024 job frame), not an atlas-texel count —
flagged in `predictions.md` before this table existed, per this repo's own law that a share
measured in one space is not a claim about another. Full table, ceiling derivation, and the
P1/P2 predictions-vs-measured writeup: `E:\AI\training\facet_E72\data\
step3_per_view_canvas.md`.

**A real, tool-native cross-check into the OTHER space came for free from step 8**: `selftest`
(below) ran a REAL `commit()` at yaw 0 and reported **9,489 atlas texels actually written**
against that same view's `hm.sum()` of 43,747 screen pixels — a ~4.6x contraction from
screen-space dilated-hole-pixels to actually-committed atlas texels at ONE view, consistent in
direction with (not a re-derivation of) the repo's own W3-measured atlas-vs-rendered-pixel
gap. A full 8-view atlas-texel decomposition (replicating `commit()`'s facing+visibility
selection read-only, without an edited image, for the other 7 views) was considered and NOT
built — named as a possible follow-up rather than commissioned speculatively, since one
concrete, tool-native example of the space gap was already in hand without writing new code
for it.

### P1 — falsified, stated plainly

Predicted band (blind, written before any `emit` ran): **200-20,000 px** per view, computed
inside a correctly-derived ceiling (E70's own measured silhouette percentages, cross-checked
there against `project_twins`'s printed figure to within 0.04pp — that cross-check held here
too: measured `hit.sum()` landed within 17-24 px of the ceiling table on every view). **7 of 8
views measured ABOVE the predicted band** (view 4/yaw180 at 20,309 sits barely over, +309 px;
view 0/yaw0 at 43,747 is more than double the upper bound). The interval-computation method
was sound; the band chosen inside it was not — it was anchored to the GLOBAL
reachable-unwritten ratio (3.93%) as a weak prior, and every measured per-view ratio
(11.6%-25.0%) runs 3-6x that global figure. A hypothesised mechanism (not independently
re-verified): the global 3.93% figure pools ALL 8 views' shared reachable-and-styled texels in
its denominator, while a per-view ratio divides only by that one camera's own visible figure —
structurally different fractions, not the same quantity read at two grains.

### P2 — CONFIRMED

Committed rule (blind, stated before step 3 ran): the view with the fewest hole PIXELS (raw
count) opens the order. **Measured minimum: view 2 (yaw 90), 17,868 px.** Blind guess in
`predictions.md`: "single best guess: view 2 (yaw 90)." Matches. The reasoning behind the
guess (total silhouette area alone) was disclosed as weak at the time and is not retroactively
credited beyond that — it correctly flagged the PAIR of small-silhouette views (90 and 270)
without distinguishing which of the two would measure lower; 270 came second (19,174).

## Step 4 — stroke order derived (NOT inherited from W3)

W3's shipped `_order` starts at two views that were the ONLY painted poles after a 2-view
stage 1, and is stated, in its own fixture's words, as designed to "start adjacent to two
styled poles." **A1 has no such asymmetry** — every one of its 8 eye-level views already
carries real paint from the 8-view twin ring (E58) — so that premise does not transfer, and
A1's silhouette, canvas, and (elevated-camera-free) camera set all differ from W3's besides.

**Rule (pre-committed)**: stroke 1 = fewest raw hole pixels = view 2 (yaw 90), confirmed
above. **Strokes 2-8**: a greedy ring-adjacency walk over step 3's own numbers (at each step,
pick the lowest-hole-count view still adjacent to the placed set) — read as the literal
"spiral outward" the law names, i.e. spatial continuity, not merely ascending count with no
adjacency constraint. **Proposed order: 90, 135, 180, 225, 270, 45, 315, 0.**

**What would have changed the answer, stated as the dispatch requires**: the OTHER defensible
reading of "fewest holes" (pure ascending count, no adjacency constraint) gives **90, 270,
180, 135, 225, 45, 315, 0** — same start, same final two, different middle (270 visited
second instead of fifth). Neither changes stroke 1. A full worst-anchored-stroke simulation
(ship.json's own method: simulate each candidate order, score by the LOWEST
already-painted-fraction any single stroke opens on) was NOT run — named as a real limitation,
not an oversight: it protects strokes 2-8 against a bad worst case, and only stroke 1 spends
this arc. Full derivation, the walk shown step by step, and this section's sourcing:
`E:\AI\training\facet_E72\data\step4_stroke_order_derivation.md`.

**The metric divergence, named rather than resolved by picking after the fact**: ranked by
hole/figure RATIO instead of raw count, the least-holed view is 4 (yaw180, 11.61%), not 2
(yaw90, 16.72%) — the two rankings disagree on the minimum even though they agree on the
worst views (0/315/45). The COMMITTED rule (raw count, stated before this table existed) is
what actually decided stroke one; this is disclosed rather than silently resolved in whichever
direction now looks better.

### P3 — a partial miss, and its cause is traceable to P1's own miss

Predicted (blind): 100-8,000 committed texels, derived as "bounded above by whatever view I
run it against," itself built on P1's (wrong) 200-20,000 band. **Measured: 9,489 committed
texels** — 1,489 above the predicted ceiling (~19% over), a real but modest miss, and directly
attributable to inheriting P1's own underestimate: since the actual `hm` population at yaw 0
was 43,747 (not the 200-20,000 predicted), the commit-eligible subset of it landing at 9,489
(21.7% of that real population, a plausible fraction for facing+visibility+in-job-mask
filtering) is consistent with a correctly-reasoned filter ratio applied to a wrongly-predicted
starting population — a clean, disclosed causal chain, not two independent misses.

## Step 5 — proposed `scopes.strokes`, NOT written into the ratified canon file

Written to `E:\AI\training\facet_E72\data\proposed_scopes_strokes.json` as a diff-ready block
(merges as the value of the existing empty `canon/a1.surfaces.json` `scopes.strokes: {}` key).
Each of the 8 stroke keys' `surfaces` list is **reused verbatim** from the already-ratified
`scopes.views` entry at the same camera position — direct reuse, not a fresh visibility
analysis, since a stroke camera and a twin camera at the same yaw/el are the same physical
camera. Keyed in the `y+NNN_e+00` format `brush_cloud_step.py --key` and `texpass_iter.py`'s
own job-directory naming both use, carrying `order` (from step 4) and
`hole_px_measured` (from step 3) per entry. `canon/a1.surfaces.json` itself was NOT touched —
canon is the Director's to ratify, exactly as `scopes.views` was at E64-E66.

## Step 6 — `E72-a1-brush-prompts.json` authored, verified against live `canon_gate.py`

**Convention followed, and why it is mechanical rather than stylistic** — genuinely
load-bearing, not a style call: `brush_cloud_step.py graph`'s only `canon_gate.require_canon`
call passes no `scope=` kwarg, so it always gates at the default, `scope="subject"`. At
subject scope, `canon_gate.py`'s `unlicensed_residue()` refuses ANY prompt text not built
entirely from this subject's own licensed spans, and `canon/a1.surfaces.json` licenses no
orientation-class `legal_clause` — so **W3's actual brush convention (full spec plus a
per-view "seen from the front" / "in profile" / etc. phrase) would be UNLICENSED RESIDUE on
A1 and would refuse `graph` at Stage 1.** I therefore followed E58's A1-twin convention
instead: the SAME, IDENTICAL, full-19-phrase composed string (reused verbatim from
`profiles/a1.json`'s own `restylize_views.py.prompt` field, the current post-E59/E60 ratified
text) on all 8 keys, unmodified by view.

**Verified directly, not assumed**, via a one-off script against the live `canon_gate.py`
(`E:\AI\training\facet_E72\scripts\verify_prompt.py`,
`E:\AI\training\facet_E72\logs\step6_verify_prompt_console.txt`):

- At `scope="subject"` (what `brush_cloud_step.py` actually gates on): `ok=True, missing=[],
  forbidden=[], unlicensed=[], out_of_scope=[]`. `require_canon()` itself: `gated=True,
  check.ok=True`.
- At `scope="view:N"` for each of the 8 views (**informational only** — nothing in the repo
  currently calls `canon_gate` with a view scope from a real spend site): views 0/1/2/7 pass;
  **views 3/4/5 each fail with 3 `out_of_scope` hits (face/eyes/mouth) and view 6 fails with 2
  (eyes/mouth)** — the exact surfaces those `scopes.views` entries drop. This is a real,
  disclosed tension between what `scopes.views` says a camera can see and what every actual
  brush prompt says regardless of camera, named here rather than silently resolved — resolving
  it (wiring `brush_cloud_step.py` to a per-view scope, or accepting the mismatch permanently)
  is a design decision this arc does not make.

**A transcription bug, caught and fixed before this step was marked done**: the first
hand-typed `_negative` field did not match `canon/A1-RECIPE.json`'s CJK string byte-for-byte
(direct comparison: `False`). Fixed by loading the string programmatically from
`profiles/a1.json` rather than retyping it a second time; re-verified `True` before
proceeding. Full account, including a `repr()`-triggered `UnicodeEncodeError` on this rig's
cp1252 console mid-diagnosis (harmless — it happened after the useful comparison line had
already printed, the documented pattern): `handoff.md`.

## Step 7 — `profiles/a1.json` populated

Added `_fixtures.brush_prompts` (pointing at the new fixture) and `_fixtures.palette`
(pointing at the previously-unreferenced `canon/A1-palette.json`, explicitly noted as
DESCRIPTIVE — `palette_gate.py` cannot execute against it, per E71's own confirmed finding,
independently re-cited here rather than re-tested). Populated `tools["texpass_iter.py"]` (9
keys: `edge-mode`, `edge-frac`, `facing-min`, `edge-dist`, `mask-dilate`, `thin-extent`,
`aspect`, `fit-axis`, `margin` — every entry `value`/`why`/`from`) and
`tools["texpass_brush.py"]` (6 keys: `seed`, `steps`, `cfg`, `lora-w`, `cn-strength`, `prompt`,
`negative`).

**Scope decision, named rather than silently left incomplete**: `bake_hero_prep.py` /
`project_twins.py` / `cull_unseen.py` blocks remain UNPOPULATED. Reasoning, written into the
amended `_out_of_scope_this_profile` note itself: none of those three tools is invoked by E72
(Stage 0 packs the GLB with the separate, profile-blind `bake_hero_pack.py`; the dispatch's
own out-of-scope list forbids re-running `project_twins`), and backfilling
`project_twins.py`'s ~15-key block from imperfect archaeology of prior arcs' invocations risks
exactly the "value arriving by invention rather than measurement" failure this repo's law
forbids. The former blanket note ("A1 has not been baked, painted, projected or culled") was
already stale before this arc — A1 has been all four — and is corrected in place rather than
left contradicting the file it sits in, per the dispatch's own instruction.

**Re-verified after writing, not merely assumed correct**: re-ran the yaw-0 `emit` a THIRD
time, this time passing `--profile profiles\a1.json` **alone**, no explicit frame flags at
all. Console: `[profile] a1 (a1.json): 9 values applied to texpass_iter.py`, then
`174,952 figure px, 43,747 hole px to inpaint` — **byte-identical to every earlier explicit-flag
run of the same view**, and `cam.json` again reads `W=576, H=1024`. This proves the populated
block is both syntactically accepted by `subject_profile.bind()` (no unknown-key ANDON, every
entry's `why`/`from` present) and numerically correct, not merely well-formed.

## Step 8 — `texpass_iter.py selftest` — HARD GATE — **PASSED**

Exact argv, verbatim (per the coordinator's explicit request, and because this is the one call
where the ANDON that would catch a missing frame does not fire — see Correction 2):

```
E:\AI-Models\trellis2-env\Scripts\python.exe E:\AI\facet\tools\texpass_iter.py selftest
  --state E:\AI\training\facet_E72\state
  --prep E:\AI\training\facet_E67\prep
  --glb E:\AI\training\facet_E72\pack\a1_e72_packed.glb
  --yaw 0 --el 0
  --profile E:\AI\facet\profiles\a1.json
  --aspect 576,1024 --fit-axis height --margin 1.204
```

Run at yaw 0 exactly as pre-registered in `predictions.md` (written before step 4 determined
stroke one was actually view 90) — deliberately NOT switched to view 90 after the fact, since
`selftest` is a generic write-head round-trip check, not a rehearsal of stroke one
specifically, and changing which view it ran against after seeing the stroke-order result
would be the same shape of error this repo's law forbids for a pass condition.

```
[profile] a1 (a1.json): 9 values applied to texpass_iter.py
[emit] E:\AI\training\facet_E72\state\selftest_y+000_e+00: 174,952 figure px, 43,747 hole px to inpaint
[commit] diagnostic - outside-figure residual mean 0.000 lv, max 0.0 lv, over-4lv 0 px  (NOT a halt)
[commit] trust mask AND geometry: 163,660 -> 163,660 px (-0 keyed on no surface)
[commit] wrote 9,489 texels; holes 2,044,423 -> 2,034,934
[selftest] styled-texel max delta 0.000000 (must be ~0), committed 9,489
[selftest] PASS - write-head is lossless on styled texels
```

Exit 0. Holes strictly shrank (2,044,423 -> 2,034,934). Styled-texel max delta exactly
0.000000. **The tool's own hard gate passed; Stage 0 did not halt.** This mutates
`E:\AI\training\facet_E72\state`'s atlas/holes/styled_mask (a throwaway copy, backed up
automatically to `atlas.prev.png` by the tool itself) — it does NOT touch the E69 source files,
confirmed by the Gate C re-hash under Step 1 above, taken AFTER this call.

## Gates — final states

| gate | status | evidence |
|---|---|---|
| Gate C — E69 atlas source bytes unchanged at close | **PASS** | 3/3 sha256 identical, before the copy and after every other step this session, including `selftest`'s own commit |
| `selftest` — the Stage-0 hard gate | **PASS** | exit 0; styled-texel max delta 0.000000; holes strictly shrank 2,044,423 -> 2,034,934; full console above |

No gate fired. No HALT was required.

## Out of scope, confirmed untouched

A second stroke (only `selftest`'s own internal round trip touched the state atlas at all).
Elevated cameras (A1 has none; not introduced). Binding. Adopting E71's fill. Re-baking.
Re-running `project_twins.py`. Editing `canon/a1.surfaces.json` or `docs/index/
conventions.json`. Retuning any threshold. Ratifying the stroke scopes (the proposal sits in
the arc tree, not in canon). No comfy-cloud tool was loaded via `ToolSearch` or called at any
point. No workflow JSON was built or submitted.

## Testing

No repo tool code was created or modified this session — `profiles/a1.json` (data) and
`docs/experiments/E72-a1-brush-prompts.json` (a new versioned fixture, not code) are the only
tracked-path changes, plus this report. Per this repo's own "tests ride the commit" rule,
that rule applies to tool code; nothing here is tool code, so no new test is owed. The
scripts in `E:\AI\training\facet_E72\scripts\` (`verify_prompt.py`, `populate_profile.py`) are
one-off, this-arc-only artifacts in the training tree, matching E70/E71's own convention for
non-repo helper scripts.

## git status, verbatim (captured before this report file was written)

```
 M CLAUDE.md
 M docs/advisor-kickoff.md
 M docs/experiments/E72-stroke-one-kickoff.md
 M docs/experiments/README.md
 M docs/instrument-census.json
 M docs/instrument-census.md
 M docs/known-defects.md
 M profiles/a1.json
?? docs/experiments/E72-a1-brush-prompts.json
?? docs/grok-consult-23-brief.md
```

**Everything except `profiles/a1.json` and `docs/experiments/E72-a1-brush-prompts.json` was
already in this state when this session first ran `git status` (not checked at session start
explicitly, but this session never opened or wrote to `CLAUDE.md`, `docs/advisor-kickoff.md`,
`docs/experiments/README.md`, `docs/instrument-census.json`, `docs/instrument-census.md`,
`docs/known-defects.md`, or `docs/grok-consult-23-brief.md` at any point — nor did it touch
`docs/experiments/E72-stroke-one-kickoff.md` beyond reading it at the start).** Consistent
with this repo's own documented concurrency pattern (E71 found `E72-stroke-one-kickoff.md`
itself appearing mid-session from elsewhere), these are almost certainly the coordinating
advisor's own concurrent edits in this same repo. Reported here, per that precedent, so they
are not misattributed to this seat and not investigated or touched by it. **This seat did NOT
run `git add` or `git commit`.** Only `profiles/a1.json` (edited in place) and
`docs/experiments/E72-a1-brush-prompts.json` (new file) are this seat's own repo-tracked
changes; everything else under `E:\AI\training\facet_E72\` is outside git by construction (the
training tree is not a git repo per CLAUDE.md).

## Artifact paths

- Live handoff (kept current throughout, includes the mid-arc corrections in full):
  `E:\AI\training\facet_E72\handoff.md`
- Predictions (written before any run): `E:\AI\training\facet_E72\predictions.md`
- State dir: `E:\AI\training\facet_E72\state\` (`atlas.png`, `holes.png`, `styled_mask.npy`,
  8 `job_y+NNN_e+00\` dirs from step 3, 1 `selftest_y+000_e+00\` dir from step 8,
  `atlas.prev.png` written automatically by `selftest`'s own commit)
- Packed GLB: `E:\AI\training\facet_E72\pack\a1_e72_packed.glb`
- Per-view canvas table + P1/P2 writeup: `E:\AI\training\facet_E72\data\
  step3_per_view_canvas.md`
- Stroke-order derivation + P3 writeup: `E:\AI\training\facet_E72\data\
  step4_stroke_order_derivation.md`
- Proposed `scopes.strokes` (diff-ready, not merged into canon): `E:\AI\training\facet_E72\
  data\proposed_scopes_strokes.json`
- Prompt-verification script + console: `E:\AI\training\facet_E72\scripts\verify_prompt.py`,
  `E:\AI\training\facet_E72\logs\step6_verify_prompt_console.txt`
- Profile-population script: `E:\AI\training\facet_E72\scripts\populate_profile.py`
- All console logs, every step: `E:\AI\training\facet_E72\logs\step{1..8}_*_console.txt`
- Repo files touched (uncommitted): `E:\AI\facet\profiles\a1.json` (edited),
  `E:\AI\facet\docs\experiments\E72-a1-brush-prompts.json` (new)

## The recorded Stage-1 invocation for the next seat (NOT run this arc)

Per Correction 1/3, `brush_cloud_step.py graph` requires `--profile` (E04 Ruling 24,
`required=True`). The corrected, would-be first call, for the record only:

```
E:\AI-Models\trellis2-env\Scripts\python.exe E:\AI\facet\tools\brush_cloud_step.py graph
  --job E:\AI\training\facet_E72\state\job_y+090_e+00
  --key y+090_e+00
  --prompts E:\AI\facet\docs\experiments\E72-a1-brush-prompts.json
  --profile E:\AI\facet\profiles\a1.json
  --subject A1
  --out <path>.json
```

Note the `--job` above points at STEP 3's measurement job (`job_y+090_e+00`), which was
already emitted (non-destructively) this session — Stage 1 may reuse it rather than
re-emitting, or re-emit fresh; both are legitimate, since `emit` never mutates `--state`'s
persistent atlas/holes/styled_mask. `e70_build_sheet.py` is NOT reusable for Stage 1's own
sheet (hardcoded `ROOT`, two-column layout, SHA literals, confirmed directly, cited above) —
a new script is needed there, not a bent copy of that one.

## Role discipline

No quality judgment appears anywhere above — none of this repo's barred words characterize
any measurement. Every prediction (P1, P2, P3) is scored against what was actually measured,
including two disclosed misses (P1's band undershot on 7/8 views; P3 inherited that miss and
landed ~19% over its own derived ceiling) and one confirmation (P2). The metric divergence
found in step 3/4 (raw count vs ratio disagreeing on the minimum) is named, not resolved by
silently picking the one that reads better now — the pre-committed rule is what actually
decided stroke one. The per-view canon-gate tension found in step 6 is reported as a real,
unresolved design question, not smoothed into "it works." Two corrections from the coordinator
are recorded with source lines, re-verified independently rather than relayed on trust, and a
third-party claim inside them (`e70_build_sheet.py`'s hardcoding) was independently
re-confirmed against the file itself rather than repeated unchecked. A transcription bug this
seat made itself (the CJK `_negative` field) is reported in the same terms as the coordinator's
own corrections, not hidden because it was self-caught. `git status` was read before writing
this report and every file this seat did not touch is named as such rather than silently
folded into "the diff." No memory write was made. No git commit was made — `profiles/a1.json`
and the new prompts fixture sit modified/untracked for the advisor to fold by pathspec. No
child agent was used for any core measurement.
