# E50 — the polygon class: is the fill pass the carrier?

**Written 2026-08-17** by the advisor seat, on the Director's open ruling from E49
(he accepted the sheets and named one new defect class). One Sonnet executor
seat, background, working `E:\AI\training\facet_E50\`. **No GPU, no cloud spend** —
every input is on disk.

## The question

E49's kickoff recorded a hypothesis and tagged the masks to test it: this arc's own
fill passes are the carrier of the new flat-coloured angular patches. Atlas islands at
this fragmentation are often single mesh triangles; the orphan fill painted each flat
from a best-facing twin sample taken with the **uneroded** sil, so a boundary-adjacent
sample imports the neighbouring material and flat-fills a triangle-sized island with it.

**The question is whether that is true, and the honest answer includes "no."** If the
patches are not on filled texels the hypothesis dies and the class needs a different
cause. Report that outcome as plainly as the other one.

## What this seat is given — measured, not assumed

The advisor measured each of these this session. They are premises you may build on
without re-deriving, though a Gate below asks you to confirm the shapes:

- `surfid.npy` exists for all 8 views under `E:\AI\training\facet_E49\aov_eroded\view_*\`.
  `tools/emit_view_aovs.py:300-304` computes it as `row * 4096 + col` from the GLB's own
  UVs — **so an atlas-space mask maps into view space by `mask.flat[surfid]`, and no new
  correspondence machinery is needed.** This is the whole instrument.
- The three provenance masks exist per mode at 4096x4096 under
  `E:\AI\training\facet_E49\atlas_owner_eroded\` and `...\atlas_blend_eroded\`:
  `orphan_fill_mask.npy`, `no_view_visible_mask.npy`, `filled_mask.npy`.
- Renders exist at `renders_owner_complete\` and `renders_blend_complete\`; the E49
  sheets at `sheets\sheet_v0*.png` are what the Director looked at.

**Assumed, not measured — treat as claims:** that the atlas is 4096 (confirm from the
mask shape); that the render and AOV rasters share a resolution (confirm); that the
Director's patches sit where the E49 record says (green/yellow/orange on tabard and
skirt, gold on a boot). His words are recorded; the *locations* are recorded prose, not
a measurement. **Do not let them define your detector.**

## The instrument, and the trap it must avoid

**A detector that only reproduces what its author already noticed is not an instrument.**
Write the flat-patch detector against the *specification* of the defect — a connected
region of near-constant colour with an angular boundary, in a painting that is nowhere
else flat — not against the three places the record says to look. Locate patches over
the whole figure on all 8 views in both modes; the Director's named regions are then a
**check that your detector fires where he pointed**, which is a validation of the
instrument, not its input.

Then cross-tabulate patch pixels against provenance class: `orphan_fill`,
`no_view_visible`, ordinary painted.

## Calibration is a deliverable, not a footnote

This repo's most recent losses are all one family: a number read against a rule the
instrument cannot support. Before you report any coincidence rate:

1. **Compute the base rate.** What share of visible figure pixels is orphan-filled in
   each view, mode-by-mode? If orphan fill covers 40% of the figure, "the patches are on
   filled texels" says nothing. The comparison is *rate inside detected patches* against
   *rate over the figure*, and you must state both.
2. **State what the instrument reads when the answer is definitely yes and definitely
   no.** Construct both populations. A decision line outside that interval is not a
   decision line — pre-register where yours sits, before you look.
3. **Two thresholds, always.** Report total patch pixels *and* the largest connected
   component, per class. A total alone must choose between missing the defect and firing
   on speckle.
4. **Predict before you look, and say whether the prediction was blind.** Predict the
   coincidence rate and the base rate separately. A prediction naming a value outside
   what the instrument can return has already failed — compute the reachable interval
   first.

## Gates — halt and report, never improvise past one

- **Gate A (shape).** Mask shape, AOV shape and render shape must agree with each other
  as the lookup requires. A mismatch halts: it means the trees are not the pair this
  dispatch assumes.
- **Gate B (the lookup is real).** Anchor the `mask.flat[surfid]` map before trusting
  it: pick texels of known class, confirm they land where the geometry says. A lookup
  that cannot be wrong has not been tested — construct a case that would fail if the
  index convention (row-major, v-flip) were wrong, and show it fails.
- **Gate C (the detector can fail).** Show the detector returning ~nothing on a surface
  that is not flat-filled, and firing on a synthetic flat patch you insert. A detector
  that fires everywhere or nowhere is not reporting.

## The deliverable

**Build the sheet before the metrics.** Per view, per mode, at the Director's native
zoom: `render | provenance-class overlay | detected-patch overlay`, plus crops at 2x on
the regions where the detector fires hardest **and** on the three the record names.
Defects first; an image is broken if any of it is. Then the numbers.

Also required: whether the two classes differ. `no_view_visible` (surface no camera
sees — 4.65–5.57% of valid texels fail the depth gate in every flat-ring view, a
standing open policy question) and `orphan_fill` (visible surface the erosion orphaned)
have different fixes. If the patches are one class and not the other, that decides which
repair is scoped.

## Out of scope

The repair itself. Twin regeneration. Any generation spend. The never-seen-surface
policy decision — that is the Director's, and this seat's output is what he decides on.
Editing any shipped tool: work in `E:\AI\training\facet_E50\`, and the only repo file
you write is `docs/experiments/E50-polygon-class-overlay-report.md`.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Every input is a named file under a recorded tree; the seat writes a manifest with sha256 per consumed artifact, as E48/E49 did. |
| ANDON_AUTHORITY | 3 | Gates A/B/C halt. Each is a `raise`, never a bare `assert` — E21 Ruling 2 / E22 Ruling 9: `python -O` deletes an assert and the run continues past a fired gate. |
| NAMED_COMPENSATORS | 3 | All writes under `facet_E50\` plus one report doc; compensator is delete-the-tree; owner is the advisor. No irreversible call in scope — no publish, no push, no generation. |
| DECOMPOSE_BY_SECRETS | 3 | Run-only seat; no repo tool changes, so no test-carrying commit is owed. |
| UNCERTAINTY_GATED_HUMANS | 3 | Terminus is the sheet for the Director's eye; the seat renders no verdict on quality. |
| EXTERNAL_VERIFIER | 2 | Manifests make it replayable and the calibration populations are an internal control, but no second seat re-measures. Owner advisor; escalate if the result is close. |

## Rules for this seat

The standing executor set. No quality judgments in any register — not *verified*,
*works*, *decisive*, *validated*, *proven*, and not *better*. Halt at every gate and
report its evidence. A negative result is a full success; say so and stop rather than
tuning toward a number. No commits. `handoff.md` in the work tree **first and kept
current** — two executor transcripts were lost mid-arc and the on-disk state is what
survived. ASCII in tool output. Absolute python:
`E:\AI-Models\trellis2-env\Scripts\python.exe`. Scripts create their own output dirs.
`argparse` eats leading minus signs — use `--flag=-30`.

## Dispatch record

- 2026-08-17, morning — dispatched by the advisor on the Director's E49 ruling, as step
  1 of the sequence the E49 kickoff left standing. The advisor is concurrently repairing
  the v0.5.0 release (five stale version surfaces, one non-hermetic CI test); that work
  touches `bin/facet.js`, `pyproject.toml`, `package.json`, `tools/record_mcp.py`,
  `.github/workflows/ci.yml` and no file this seat writes.
