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

Columns: **accepted twin | pre-stroke mesh | post-stroke mesh**, at matched zoom and
crop, head and collar crops required. **Rank nothing.**

⚠ **The `A1 reference` column originally specified here is WITHDRAWN, and E71 is why.**
That arc's seat measured it: `canon/A1_reference.png` is 1136x1472 against this route's
576x1024 calibrated ortho frame, and **no recorded correspondence between those spaces
exists** in `profiles/a1.json`, the E57/E58 reports or `canon_compose.py`. Applying E70's
literal crop boxes to the reference yields an empty-background head crop and a badly
misregistered collar crop, both saved as proof artifacts under `facet_E71\data\`.
Establishing that correspondence is a separate pre-registered job nobody has done. The
accepted twin is the registered comparison and it shares the frame.

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

---

## ⚠ AMENDMENT 1 — 2026-08-19 — what stroke one CANNOT do, ruled before it runs

The Director ruled the vertical peach banding across A1's face on the E70/E71 head crop:
it is **view ownership at UV chart boundaries**, styled texels with different owning
cameras — not dirt, and not the cream-vs-grey hole class. Confirmed at source before this
amendment: `project_twins.py:936-939` is winner-take-all (`take = w > best_w[idx]`), the
face is seen by the front view and the two 45° quarters, and those twins disagree on skin
value by **R 13.0 / G 13.9 / B 18.3** across the accepted ring. Full entry in
[known-defects](../known-defects.md).

**E72 will not erase the stripes, and the reason is structural rather than a matter of
effort.** `texpass_iter.py` commits into **HOLE texels only; styled texels are never
overwritten.** The bands are styled.

| what you see on the crop | cause | can stroke one touch it? |
|---|---|---|
| vertical peach bands, cheeks and forehead | styled texels, different owners | **No** — styled is frozen |
| grey patches in hair, collar, vest | RGB(107) holes | **Yes** — that is the brush canvas |

**So the sheet this arc produces must not be read as a face fix, and the report must say so
in its own words.** If the bands are still there afterwards, that is the expected outcome and
not a failure of the stroke.

**Stroke one answers exactly one question**, and the arc is graded on it alone: *does the
brush continue this man into the holes, or compose a new one?*

**Out of scope, added:** evening the face. Both candidate remedies — letting the front view
own the whole head band, or a seam-blend **allowed to rewrite styled skin**, which no stage
in this route may currently do — are **new doctrine for a later sitting**, not this one.

**Enumerated for that sitting so it is not commissioned twice:** the tool already computes a
weighted average alongside the winner (`sumW` / `sumWC`, `project_twins.py:934-935`), and the
blended atlas is **already on disk** at
`E:\AI\training\facet_E69\bake\atlas_widescope_blend.png`, written by the same run that
produced the approved `atlas_widescope.png`. Whether it reads better is a look question and it
is free to render. That is not a claim that it fixes the banding — only that the artifact
exists and nobody has put it in front of the Director.

---

## ⚠ AMENDMENT 2 — 2026-08-19 — the invocations in Stage 0 and Stage 1 CANNOT RUN as written

Found by the **outside channel** ([consult #23](../grok-consult-23-brief.md)) while the Stage 0
seat was executing this spec. Verified at source before the seat was steered. The defect is the
advisor's, and so is the correction that followed it.

**Stage 0 step 3 and Stage 1 step 1 invoke `texpass_iter.py emit` with no frame.**

    texpass_iter.py:133
    if args.mode == "emit" and args.profile is None and not _aspect_explicit:
        ANDON: `emit` needs a frame it was given, not one it guessed.

That is E14 Ruling 29c living in the tool. Its default `--aspect` is **752,1024** — W3's
portrait framing. **A1's measured frame is 576,1024.** The prop's own frame is 240x1024, so
the silent default that earned this guard was **3.1x too wide**, committing through a different
projection than the one that lit it, with no error anywhere.

**⚠ The trap inside the trap: `selftest` skips this ANDON.** The refusal is narrowed to
`mode == "emit"` deliberately — `commit` reads W/H out of the emitted `cam.json` and gating it
would fire on correct work. So **Stage 0's hard gate, the thing standing between this arc and a
paid generation, would pass on W3's frame while the real stroke ran on A1's.** A green gate that
never saw the thing it gates.

**⚠ And `--profile` does NOT close it — the advisor's first correction re-armed the trap.**

    texpass_iter.py:132   _aspect_explicit = any(a == "--aspect" or a.startswith("--aspect=") for a in _argv)
    texpass_iter.py:142   W, H = (int(x) for x in args.aspect.split(","))

Passing `--profile` makes `args.profile is None` **false**, so the ANDON goes quiet; the frame
is then read from `args.aspect`, which `bind()` overwrites **only if the profile carries a block
for THIS tool**. `profiles/a1.json`'s `tools` keys are exactly
`['verify/turn_render.py', 'silhouette_masks.py', 'restylize_views.py']` — **no
`texpass_iter.py`**, and its `576,1024` sits on `silhouette_masks`, which `bind()` never reads
here. The documented cure silently re-opens the documented defect, on exactly the subject whose
profile is incomplete. **That law is now in CLAUDE.md; E14's guard is NOT retuned in this arc**
(Director, 2026-08-19).

### The corrected invocations — binding

1. **`--aspect 576,1024` explicitly on EVERY `emit`, and on `selftest`.** Not `--profile` as the
   frame source. `--aspect` is the only flag that sets the frame here today.
2. **`--profile` is required for `brush_cloud_step.py graph`** (`:156`, `required=True`, E04
   Ruling 24, no skip) — where it is identity and provenance, **not a frame**. Stage 1 step 2 as
   originally written never builds a graph.
3. If Stage 0 step 7 populates a `texpass_iter.py` block in `profiles/a1.json`, `aspect` goes in
   it with `value`/`why`/`from` — and **the live invocations still pass `--aspect` explicitly
   this arc** rather than trusting a block written the same hour.
4. **The verbatim argv of every `emit` and of the `selftest` is reported**, not described. Any
   emit or selftest already run unframed is **void** and is declared rather than quietly re-run
   over.

### And `e70_build_sheet.py` is not reusable — the spec's claim was wrong

`E:\AI\training\facet_E70\scripts\e70_build_sheet.py:14` is `ROOT = r"E:\AI\training\facet_E70"`,
hardcoded, laying out **two** columns and carrying SHA literals. A three-column E72 sheet is a
**new script**, not a reuse. Say so plainly rather than bending that one.

### Why this is recorded at length rather than quietly fixed

These are the **fourth and fifth** defects of one shape the advisor shipped in this session —
naming a tool and not opening it — after three that a Sonnet seat caught in E71. The first three
cost a seat's time; these two were caught **before** anything was spent, by a channel the
advisor had not opened all session. A future reader deciding how much to trust these two specs
should weigh that: **E71's Amendments 1-4 and this file's Stage 0/1 invocations were written by
a seat that named tools without opening them.**

---

## ⚠ AMENDMENT 3 — 2026-08-19 — the debt strokes 2–8 do NOT get a free ride on

**Director, 2026-08-19: stroke one runs with the prompt string as drafted. The recut is
refused for this sitting, and the debt is recorded rather than carried silently.**

### Why the string stands at yaw 90

`head facing straight ahead` is the **body-relative staging clause**, not *look at the
camera*. It is this repo's own wording for the anti-crank direction — E66's kickoff states
the defect as *the head turns toward the camera when it should stay straight ahead*. At yaw
90 a body-relative "straight ahead" **is** the profile, so the clause does not fight the
silhouette. Measured: the eight keys carry **one distinct prompt string**, so the clause is
uniform and body-relative rather than per-view and camera-relative.

Recutting the set for a camera-relative "in profile" phrase is **refused this sitting** and
the reason is mechanical, not stylistic: `brush_cloud_step.py:407` gates at
`scope="subject"`, and **A1 licenses no orientation clause**, so a per-view orientation
phrase would land as **unlicensed residue**. And the yaw-90 mask is hair fringe, collar,
vest opening and a shoe — **not a blank face** — so the clause is acting as an anti-crank
instruction on those texels rather than as a fight with the view.

### ⚠ THE DEBT — it binds strokes 2 through 8, and it is unresolved

**The same single prompt string names `eyes`, a smile, and `face` on the REAR cameras.**
The seat measured this and disclosed it rather than resolving it (report §step 6,
`logs\step6_verify_prompt_console.txt`), and the measurement is informational **only because
nothing in the repo currently calls `canon_gate` with a view scope from a real spend site**:

| scope | result |
|---|---|
| `scope="subject"` — **what `brush_cloud_step.py` actually gates on** | `ok=True`, missing/forbidden/unlicensed/out_of_scope all empty |
| `scope="view:0/1/2/7"` | **pass** |
| `scope="view:3"`, `"view:4"`, `"view:5"` | **FAIL — 3 `out_of_scope` hits each: `face`, `eyes`, `mouth`** |
| `scope="view:6"` | **FAIL — 2 `out_of_scope` hits: `eyes`, `mouth`** |

Those are exactly the surfaces each `scopes.views` entry drops. **This is the E58/E63
mechanism, disclosed and unresolved.**

**Stroke one is yaw 90, and view:2 PASSES. That is the whole reason it may run.**

**Strokes 2–8 do not get a free ride on this file** (Director, 2026-08-19). Before any of
them is spent, one of two things is decided and written down:

1. wire `brush_cloud_step.py` to a **per-view** scope, so the gate the record already knows
   how to compute is the gate that actually guards the spend; or
2. accept the subject-scope mismatch **permanently and in writing**, with the reason.

Neither is decided here, and **neither may be decided by a seat mid-spend.** A stroke on any
of views 3/4/5/6 with this file and no decision is a spend against a prompt the record can
already show is out of scope for that camera.

---

## AMENDMENT 4 — 2026-08-19 — stroke one is TAKEN and ACCEPTED, and three things are ruled with it

**The Director, 2026-08-19, on the Stage 1 sheet: CONTINUED. Same man. Stroke one is taken.**

The pale triangle at the vest collar-to-shoulder went plum and the seam reads as **one
garment, not a new one**. Hem and shoe ticks are the same class. Head, hair, profile and the
peach bands are unchanged — as they must be, styled and frozen. **It did not invent a face,
turn the head, or paint a second vest.**

The arc's single question is answered: **the brush continued this man into the holes.**

### The three rulings that ride with the acceptance

1. ⚠ **`selftest` gets its own directory before stroke two — and is NOT to be "fixed" by
   committing its texels.** The gate that protects the spend performs a real `commit()` and
   left **9,489 yaw-0 texels permanently marked STYLED** in the shared `state/` dir. The
   Stage 1 seat caught it before spending, reset from sha256-verified E69 copies, disclosed
   the reset in `predictions.md` **before it could touch a number**, and proved the reset
   inert by re-emitting yaw 90 to Stage 0's exact figures. Full entry in
   [known-defects](../known-defects.md). **Blur-fill is not paint and must not be promoted to
   paint to make the problem go away.**

2. ⚠ **The thin grey gap at the vest-hem/trouser junction STAYS A HOLE.** Present pre-stroke
   and post-stroke; the stroke did not close it. **Left alone deliberately** — it is not a
   defect to be chased in this arc.

3. ⚠ **Strokes 2–8 remain blocked on the Amendment 3 debt, and `brush_cloud_step.py` is NOT to
   be wired to a per-view scope in the afterglow of a pass.** One stroke passing at
   `scope="view:2"` is not evidence about views 3/4/5/6, which the record can already show
   fail. That debt is decided in the clear, in its own sitting, or accepted permanently in
   writing — **and neither by a seat mid-spend.**

### What Stage 1 measured

| | |
|---|---|
| generations | **one**, submitted once, completed once — no retry, no second seed |
| `invar` ANDON | **PASS** — mean 0.014 lv, largest hot component **0 px** outside the figure across 472,318 px tested; uniform sub-unit is the codec boundary, not a repainted backdrop |
| `commit` | **PASS** — **3,585 texels** written, holes **2,044,423 → 2,040,838**, no ANDON fired |
| E69 source atlas | sha256 `66b8602b…`, **byte-identical to E70's Gate C record** |
| P4 residual shape | **confirmed**, at the clean end of its band |
| P5 texels closed | **confirmed** — 3,585, inside both the 1,000–9,000 band and the 2,500–4,500 central guess |
| P6 continuity | **the seat refused to score it** and handed it to the Director's eye with factual sheet evidence — the role boundary working |

Both gates were run as **separate calls with each exit code read individually**, per E08
stroke 7's law. The seat also reported two operational hiccups it caught without damage: a
Bash `cp` blocked by the session's permission classifier, and an unquoted backslash path that
exited 2 before touching any state.
