# E11 — the dense-turnaround exporter: REPORT

**Executor session, 2026-08-05.** Run under
[E11-dense-turnaround-export.md](E11-dense-turnaround-export.md) (handoff 5, Task 2).
No generation anywhere; the base assets were never opened for writing — every write
landed in new directories (`export/turnaround/` under each subject's root) or new
tool files. The spec's own hypothesis table is the pre-registration; nothing below
retunes it.

Tools written:
[`tools/e11_export_turnaround.py`](../../tools/e11_export_turnaround.py) (the exporter —
orchestrates the shipped `texpass_iter emit` as a subprocess; adds exact per-view
products by texel-id raycast) ·
[`tools/e11_manifest.py`](../../tools/e11_manifest.py) (the lane-contract manifest for a
self-contained export tree).

Watchdog standing: reported at session start (dead, heartbeat 13.6h stale) — and **no
GPU render leg exists in this task**: emit and every raycast here are open3d CPU. The
watchdog was not needed and was not restarted by this session. *(⚠ Advisor correction
in place, 2026-08-05 20:51: the watchdog was restarted by the advisor's session at
20:26 — after this session's start, before its E11 leg completed — and measured alive
at 20:51, heartbeat age 0.0 min. The "13.6h" matches no on-disk timestamp and is
recorded as the session-start hook's arithmetic, not a measurement. What stays true
here: this session restarted nothing and ran no GPU leg —
[E10-offsurface-ruling.md](E10-offsurface-ruling.md) Ruling 6.)*

## Hypotheses, scored

| # | hypothesis | verdict | the number |
|---|---|---|---|
| X-H1 | the export is a pure function | **CONFIRMED** | Step 0: two fresh emits byte-identical on all three channels; X2 spot check on W3 byte-identical |
| X-H2 | the shared views reproduce the record | **CONFIRMED (galleon)** | beam render/prov/owner all byte-identical to the recorded sheet renders (`26b0ae99…`/`60f4723f…`/`eb5406ca…`); silhouette byte-identical to Step 0.2's `hit.png`; hit identical across all three channel states |
| X-H3 | indexed conversion is lossless | **CONFIRMED, proven per file** | W3's truecolor provenance atlas (measured: exactly 4 colours) → indexed PLTE round-trip, pixels identical; the galleon's was already proven by the staged export; every born-indexed `prov_class_*.png` re-read and pixel-compared at write |
| X-H4 | the lane ingests without edits | **CONFIRMED, both subjects** | `sdlab asset ingest --dry-run`: galleon dense 28/28 registered, 0 rejected; W3 dense 26/26, 0 rejected; zero schema deviations beyond the recorded Ruling-29 sentinel translation |

## Step 0 — the one-view anchor (HALT on any digit): ALL PASS, first run

Beam view, all channels, against the recorded artifacts. The byte-anchor also
settled the GLB operand question: `prep_uv.glb` reproduces the recorded renders
byte-for-byte, so it is what the record rendered with. The owner display atlas was
proven a pure function of (`view_owner.npy`, claim map): 15 value→colour rows, no
ambiguity, and zero stage-1 texels carry sidecar owner −1.

One dependency carried in: the per-stroke claim map is Task 1's **anchored** replay
(all six strokes exact, A32 hit-intersect included — see
[E10-offsurface-consumers-report.md](E10-offsurface-consumers-report.md)).

## X1 — the galleon, full superset

28 cameras (the profile's `cull_unseen.production`, read at runtime, never
transcribed) × 3 channels, plus per view: exact silhouette, born-indexed
`prov_class` map, `owner_id` slice (int8, −1 unstyled/no-surface), owner-boundary
distance field as `loss_mask` (clip 32 px), admission JSON (class shares inside the
exact silhouette). Reference share runs 82.1–92.5% on the eye-level ring and drops
to 61.2–68.1% on the elevated four — the deck is brush-and-dilation territory,
matching the arc's own coverage measurements.

The self-contained tree `E04_stroke/export/turnaround/` carries sha-verified copies
of mesh, atlas, indexed provenance atlas, `view_owner.npy`, `styled_mask.npy`, and
**all eight clay↔styled-twin pairs** (E04_armT72's ruled generation; the rejected
twin_7 stays in the record under its seed suffix and is not a pair) — item 6's
lossless linkage, activatable retroactively at the lane's ~1k-pair threshold.

Cross-anchor worth naming: the lane's palette gate (a different codebase, JS,
running facet's ported formula) reproduces the staged manifest's measured context
digits on the three sheet cameras — largest blobs **1738 / 1495 / 263 px** — from my
freshly emitted renders. Two implementations, two days, same numbers.

## X2 — W3 re-exported dense: the exporter is not galleon-shaped

Different prep (`facet_E06/C1/prep` — named by `masks/silhouettes.json`'s own
pointer), different profile, different palette, **owner channel honestly absent**
(no owner products emitted, nothing synthesized — the manifest and every admission
JSON say so). 26 cameras (the character's cull superset) × 2 channels + exact
silhouettes + born-indexed class maps + 8 twin pairs (3 with clay counterparts on
disk). Reference share 85.3–95.1% across all views. The lane validates it without
edits.

**Flag for the ruling — two W3 render generations now exist.** The recorded
`out/renders_flat/final_0..7.png` are NOT this emit path's output: my beam render
differs on **all 770,048 pixels (max 193 levels)** while the silhouette is
byte-identical to `masks/w3clay_0.png` (0 px) and the figure count matches
`silhouettes.json` to the pixel (146,356). Same geometry, different renderer or
state — the recorded flat renders came from another generator. **The sdlab fixture
ingested `renders_flat` yesterday; the dense tree renders are emit's.** Which
generation the lane trains on is not this session's call. Nothing was deleted;
both sets stand.

## X3 — lighting variation: enumerated only, nothing built

What it would require: (1) a **new renderer** — emit is an atlas readout with no
shading model, so lighting means Blender (EEVEE/Cycles; Workbench STUDIO is the
documented judging trap) or a shaded raycast, either one a new tool with its own
Step-0 anchors; (2) a **new provenance surface** — light rig identity (HDRI id,
rotation, exposure) pinned per render per PIN_PER_STEP; (3) a **fork in purpose** —
the judging rules require flat (CLAUDE.md: a lit render is not a texture readout),
so lit renders would be training-only artifacts, doubling the render legs;
(4) GPU legs → watchdog discipline.

What the record already covers without it: background variation is **already
augmentation-side** — every render ships with its exact silhouette, so the lane
composites any backdrop without facet re-rendering; the domain-tag caption
mitigation is lane-side (its Phase-0 Q4). The spec's predicted answer stands as the
enumeration's conclusion: **flat-only is what facet honestly exports; lighting is
augmentation-side (or a future lit-renderer arm with its own anchors, if a ruling
ever wants it).** A negative result is a full success; this one was pre-registered
as "probably the answer."

## What is NOT established / gaps named for the ruling

- Which W3 render generation (recorded `renders_flat` vs emit's dense set) the lane
  should train on — and, downstream, whether the sdlab W3 fixture re-ingests.
- The dense manifests reuse the staged manifests' acceptance blocks verbatim (the
  Gate-1 verdicts cover the ASSETS; whether they cover renders made after the
  verdict is a semantics question the ruling owns).
- Which manifest the Director's sdlab paste should use — the staged 3-render one at
  each subject root (untouched) or the dense tree's. Both validate.
- Per-view `owner_id_*.npy` and `admission_*.json` ride undeclared beside the
  declared channels (render-space npy/json are not lane schema 1.x concepts) — the
  Ruling-29 translate-at-the-boundary pattern; the schema item is the lane's to
  take or refuse.
- X1's own beam render was byte-anchored against the record; the other 27 cameras
  have no recorded counterparts to anchor to (they are the dense set's point). Their
  trust rests on X-H1 purity + the anchored beam + the shared code path.

## Standards compliance (this run)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every copy sha256-verified; the camera list read from the profile at runtime; the claim input is the anchored replay; run JSONs record every view's numbers |
| ANDON_AUTHORITY | 3 | Step 0 halted on any digit (none differed); indexed writes self-prove PLTE + pixels; emit failures raise; the W3 render mismatch was REPORTED with pixel evidence, not smoothed |
| NAMED_COMPENSATORS | 3 | all writes under `export/turnaround/` per subject + two tool files; undo is deleting those; base assets never opened for writing (emit reads; states are copies) |
| DECOMPOSE_BY_SECRETS | 3 | the shipped emit renders; the exporter orchestrates; the manifest tool owns the lane contract; the lane validates from its own codebase — the two-sided check neither side can pass alone |
| UNCERTAINTY_GATED_HUMANS | 2 | per the spec: no Director gate in this plumbing; the open choices (render generation, manifest, schema item) are named above for the seats that own them |
| EXTERNAL_VERIFIER | 3 | the lane's validator (different codebase) passed both trees; the beam anchors were against artifacts this session did not produce; the palette-gate digits reproduced across implementations |

**Reported, not ruled. Handoff 5's both tasks are run; the session stays open for
the Director.**
