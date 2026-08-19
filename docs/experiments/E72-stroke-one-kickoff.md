# E72 — stroke one

**Advisor spec, 2026-08-19. One executor seat. Tree `E:\AI\training\facet_E72\`.
Stage 0 is FREE and local. Stage 1 is ONE cloud generation — the first brush
stroke on A1, green-lit by the Director 2026-08-19.**

## The question

Does the brush *continue* this character into its holes, or does it compose a new
one? That is the only question stroke one answers, and it is answered at the
Director's eye on a sheet, not by a number.

## What the brush actually does — read this before planning

`texpass_iter.py` states it in its own docstring: **commit writes edited pixels into
HOLE texels only; styled texels are never overwritten.** The holes are the brush's
canvas. That has three consequences this spec is built around:

1. **E72 and E71 Arm R target the SAME population** — reachable-unwritten texels.
   They are **alternatives, not stages**: E71 smears a real 3D neighbour into a
   hole, E72 synthesises new paint there. Both are measured; the Director judges.
   Neither is adopted by running.
2. **Nothing is destructive, and it must stay that way.** E71 works in its own tree
   under a Gate C that asserts the E69 atlas bytes are unchanged. **E72 does the
   same**: build a state directory by COPYING E69's widescope output; never mutate
   it in place. If both arcs keep that discipline the approved artifact is
   untouched whatever happens.
3. **A1's atlas is 58.91% holes** (2,044,423 of 3,470,348 valid) — far more than
   W3's loop faced at this stage — but **97.1% of that is unreachable by any camera
   in the ring**. The brush only ever sees what a view projects, so the real canvas
   is a per-view subset of the 58,346 reachable-unwritten. **Measure it before
   spending; do not assume it.**

## What A1 does not have yet

Measured, not inferred, by reading `profiles/a1.json` and `canon/a1.surfaces.json`:

| needed | state |
|---|---|
| `_fixtures.brush_prompts` | **ABSENT** (W3's profile has one; A1's does not) |
| `_fixtures.palette` | **ABSENT** — `canon/A1-palette.json` exists and is unreferenced |
| `profiles/a1.json` texpass tool blocks | **UNPOPULATED**, by that file's own note |
| `canon/a1.surfaces.json` `scopes.strokes` | **`{}`** — the slot is ratified, the contents are not |
| elevated cameras | **none, and out of scope** — A1's `cameras` block declares eight eye-level yaws and states no elevated-camera question has been asked or measured. W3's stroke order ends with two `e+55` keys; **A1's cannot.** |

`profiles/a1.json`'s own note says the texpass blocks are unpopulated because the
values "would be arriving by invention rather than measurement." **That condition no
longer holds** — A1 has been projected and baked — and the Director ruled at E71 that
the seat which runs the route populates it. **This is that seat.**

## Stage 0 — FREE, and it gates the spend

Zero generations. Every step local.

1. **Build the state directory.** Copy `facet_E69\bake\atlas_widescope*.png` /
   `*_styled_mask.npy` into `facet_E72\state\` under the names
   `texpass_iter` requires (`atlas.png`, `holes.png`, `styled_mask.npy`).
   **Copy, never rename in place.**
2. **Pack the GLB** with `tools/bake_hero_pack.py`, exactly as E70 did.
3. **Measure the per-view brush canvas.** Run `texpass_iter.py emit` for each of the
   eight eye-level yaws and record, per view, how many hole texels its projected
   (dilated) mask actually covers. This is the input to the stroke order and it is
   the number that says whether the brush has anything to do at all in a given view.
   **Report all eight; do not read a conclusion off the first one.**
4. **Derive the stroke order from that measurement.** CLAUDE.md: *order strokes to
   spiral outward from already-painted regions, or the brush composes a new
   character instead of continuing one.* W3's `_order` starts at the two profiles.
   **Do not inherit it** — a global constant must not govern a local feature, and
   A1's silhouette, canvas and camera set all differ. Derive, state the derivation,
   and say what would have changed the answer.
5. **Author the proposed `scopes.strokes`** for `canon/a1.surfaces.json`, honouring
   the eight **already-ratified** `scopes.views` entries — those are the mechanism
   that cleared the head-crank at E65/E66 and they are canon. Write the proposal to
   the arc tree as a diff-ready block; **do not edit the ratified canon file.**
6. **Author `docs/experiments/E72-a1-brush-prompts.json`** in the shape
   `brush_cloud_step.py` requires: per-key prompt strings, an `_order` array, a
   shared `_negative`, plus the documentation keys that record why each decision was
   made. **Every ratified element must be named** — if a canon element is not in the
   prompt it arrives by accident and leaves the same way. Note that E58's A1 twin
   prompts deliberately deviated from W3's per-view-drop convention and disclosed it;
   say which convention you follow here and why.
7. **Populate `profiles/a1.json`** — `_fixtures.brush_prompts`, `_fixtures.palette`,
   and the texpass tool blocks — each entry carrying `value` / `why` / `from` in the
   file's existing style, **every value from a measurement with its source named.**
   Amend the stale `_out_of_scope_this_profile` note in the same change rather than
   leaving it contradicting the file it sits in.
8. ⚠ **`texpass_iter.py selftest`** — emit, fake-inpaint by local blur, commit,
   assert styled texels byte-identical and holes strictly shrink. **The tool's own
   docstring says to run this before any real brush. It is a HARD GATE on the
   spend.** If it fails, report it and HALT; the stroke does not run.

**Stage 0 ends with an artifact for the Director**: the proposed stroke scopes, the
prompts file, the per-view canvas table, and the selftest result. **Canon is his** —
the view scopes were ratified at his eye and the stroke scopes are the same class of
object.

## Stage 1 — THE SPEND. One stroke. Not two.

1. `texpass_iter.py emit --state ... --prep ... --glb ... --yaw <k> --el 0` for the
   FIRST key of the derived order.
2. `brush_cloud_step.py graph --job DIR --key <k> --prompts docs/experiments/E72-a1-brush-prompts.json --out J.json`
   — **the saved workflow JSON is the recipe**, written before anything is
   submitted (E08 Amendment 30). It carries a provenance check that `--prompts` IS
   the file the profile's `_fixtures.brush_prompts` names, so step 7 above must
   land first.
3. **Submit through the Comfy Cloud MCP.** Generation does not run on this rig.
4. ⚠ `brush_cloud_step.py invar` — **the first-stroke invariance ANDON.** Is the
   returned image unchanged OUTSIDE the figure? Read the residual's SHAPE: uniform
   sub-unit is the codec boundary and proceeds; **CONCENTRATED is a repainted
   backdrop and HALTS.** A structural difference concentrates; two float kernels do
   not.
5. `texpass_iter.py commit` — its own invariants are the gate: styled texels
   byte-identical, holes strictly shrink.

⚠ **The gate lives inside the tool that performs the irreversible step. Never chain
a check and a commit in one shell call** — E08's stroke 7 committed 47,020 texels
after a fired ANDON because a PowerShell chain walked past a non-zero exit, and it
produced a pass-shaped log entry for a failed condition. Run them as separate
calls and read each exit code.

## The sheet

E70's construction, reused: `bake_hero_pack.py` → `turn_render --flat` →
`silhouette_masks.py` → E70's `e70_build_sheet.py` and `crop_boxes.json`.

Columns: **A1 reference | accepted twin | pre-stroke mesh | post-stroke mesh**, at
matched zoom and crop, head and collar crops required. **Rank nothing.**

Failure modes the sheet must be able to show: the brush composing a *different*
character in the stroked region; a seam at the stroke boundary; the stroke taking
backdrop grey; identity drift in face or hair; and the hole filling with something
no canon row names.

**Required verbatim in the footer:** the warm rim light in the twins is still paint;
the overlay dots are still the map.

## Predictions — written BEFORE anything runs

Each with a stated band, each disclosing whether it was blind.

- **P1** — the per-view brush canvas (hole texels under the projected mask) for each
  of the eight yaws. State the band before running emit. ⚠ **Check the interval your
  instrument can return**: what does this read when a view sees no holes, and when it
  sees all of them? A prediction outside that interval could not have been right.
- **P2** — which view the derived order puts first, and why, stated before the
  measurement that decides it.
- **P3** — the selftest's hole-shrink magnitude.
- **P4** — the invariance residual's shape (uniform or concentrated), and what each
  outcome would mean, stated before the stroke returns.

## Out of scope

A second stroke. Elevated cameras. Binding. Adopting E71's fill. Re-baking.
Re-running `project_twins`. Editing `conventions.json`. Retuning any threshold.
Ratifying the stroke scopes — **that is the Director's**.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The recipe is the saved workflow JSON, written to disk before submission (E08 Amendment 30), with the prompt from a versioned file as the only per-stroke variable. Seed, steps, cfg, LoRA weight and ControlNet strength are all explicit tool defaults recorded in that JSON. |
| ANDON_AUTHORITY | **3** | Three halts, none of them optional: `texpass_iter selftest` gates the whole spend; `brush_cloud_step invar` halts on a concentrated residual; `commit`'s own invariants halt on a styled-texel change or a non-shrinking hole map. The spec forbids the shell-chain construction that defeated one of these at E08 stroke 7. |
| NAMED_COMPENSATORS | **3** | Every write lands under `E:\AI\training\facet_E72\`. Compensator: `Remove-Item -Recurse E:\AI\training\facet_E72\`, owner the executor seat. The E69 atlas is copied, never mutated. The one irreversible external act is the cloud submission, whose compensator is that it writes nothing back — the returned image is inert until `commit` runs locally, and `commit` is separately gated. |
| DECOMPOSE_BY_SECRETS | **3** | `brush_cloud_step` splits deliberately into graph / invar / log so the recipe, the gate and the audit trail each change for their own reason; the write-head (`texpass_iter`) is separate from the generator; canon lives in `a1.surfaces.json`, prompts in a versioned fixture, and subject values in the profile. |
| UNCERTAINTY_GATED_HUMANS | **3** | Two checkpoints, both gated on uncertainty rather than step count: the Director ratifies the stroke scopes because canon is ground truth he holds and no metric approximates it, and he judges the sheet because *is this still the same man* is not a measurable question. |
| EXTERNAL_VERIFIER | **2** | The invariance ANDON reads the returned image against the submitted one — the generator does not grade itself — and `palette_gate`'s bands come from `canon/A1-palette.json`, derived at E57 and never fit to this question. Not 3: the write-head and the emit step are one codebase, so `selftest` is a self-check and is reported as one. |

## Dispatch record

- 2026-08-19 — spec written after the Director green-lit stroke one. Stage 0 is
  free and gates the spend. The brush-canvas measurement, the stroke order, the
  stroke scopes and the profile population are all Stage 0 because **none of them
  should be decided while looking at a generation that has already been paid for.**
