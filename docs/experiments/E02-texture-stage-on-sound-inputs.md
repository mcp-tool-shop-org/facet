# E02 — Is the texture stage sound when its inputs are?

**Status:** SPEC — not yet run
**Author:** advisor session, 2026-08-04
**Executor:** a fresh session — this is a production run with gates, not a design task
**Cost:** ~30 min GPU, $0 (all local), two Director gates

---

## 0. Read this before anything else

The Director rejected a textured warrior on 2026-08-03: *clunky, ghost image, white patch
on the skull*. Three independent faults were found afterwards, none of them in the texture
architecture. **All three are now fixed.** This experiment asks the question that has never
actually been asked: with sound geometry, correctly registered twins, and an honest metric,
**does the texture stage produce something the Director would accept?**

A negative result is a full success. If the output is still poor with every input sound,
that redirects the project, and it is worth more than a tuned improvement.

**Five rules, each paid for in a previous session:**

1. **You do not judge whether output is good.** Produce measurements and comparison sheets;
   the Director judges. Never write "verified", "shipped", "works", "decisive" or
   "validated" — not in the report, not in a commit message.
2. **Do not write to the memory store.** The advisor folds findings into the repo after the
   Director has seen them.
3. **Stop at every gate.** Do not improvise past a failed gate. An earlier session changed a
   parameter and re-ran when a gate fired; it hit the same gate harder.
4. **Judge textures under FLAT light, geometry under `--clay`.** A Workbench STUDIO render is
   not a texture readout — grey chalky facet mosaics are specular highlights on flat-shaded
   normals and vanish under `--flat`. Two debugging rounds were lost to this.
5. **State your prediction before you look.** If you have already seen intermediate output,
   say so and weight it accordingly.

---

## 1. What is sound now — the ledger, with measurements

Everything here is checkable from `github.com/mcp-tool-shop-org/facet` and
`E:\AI\training\facet_E01\`.

**Geometry.** `W3` — subject W reconstructed by TRELLIS.2 `1024_cascade` from
`facet_E01/inputs/A0_source_clay.png`, seed 42, `ATTN_BACKEND=sdpa
SPARSE_ATTN_BACKEND=sdpa`. Real facial structure: brow bar with a crease, upper lid edges,
nostril wings, formed mouth cavity, carved beard strands. The rejected A0 mesh, from the
same clay, is a featureless faceted blob.

**Topology.** Welded before decimating: 25,158 shells → 40, decimated to 287,200 faces at
38 shells with exact UVs carried through. The historical shredding was our own glTF export
splitting a vertex at every UV seam (285,654 shells), not the generator.

**Atlas.** `island_margin` 0.001 → **18.76%** coverage (A0 is 20.34%). Head scaling on,
through the corrected gate (UV area vs **3D surface area**, not face count): head UV share
**0.879**.

**Twins.** Generated from W3's own renders — twins belong to a mesh, not a character.
Control image built rather than hoped for: composite onto contrast, then union the figure
mask's morphological gradient into the Canny map. Silhouette IoU **0.777 / 0.789**, bbox
x/y 0.457 / 0.461 against the source's 0.458. Back twin uses a per-view prompt: **0 faces
detected** against a source-back control of 0.

**Projection.** `mesh_mask ∧ erode(twin_mask)` — the mesh silhouette answers *is there
surface here*, the twin's own mask answers *is the paint trustworthy*. Conflating them cost
480k texels. Styled coverage **53.7% of geometrically reachable**, where reachable is
`facing ≥ facing-min ∧ visible` and nothing else, so the ceiling is a true 1.0.

**Registration.** 95.7% of the saved mask lies inside the projected footprint; the 10 px
top-edge gap is the sword tip antialiasing below the keying threshold.

**What has never been tested:** the eight-stroke `texpass` loop on any of this. Every
texture result in this project's history was produced on the A0 blob with A0's twins.

---

## 2. The question

**Run the texture-space loop on sound inputs and put the result in front of the Director
beside the asset he rejected.**

Two outcomes, both valuable:
- **Accepted** → the texture architecture was always sound; three input faults produced the
  rejection. The route is proven end to end and E03 becomes the priority.
- **Rejected** → the texture stage has a defect of its own, now isolated from every
  confound. That is a far better place to debug from than 2026-08-03 was.

---

## 3. Procedure

### Stage A — restate the inputs (no GPU)

Re-run `project_twins.py` on the staged W3 atlas and confirm **53.7% styled / reachable**
and **31.6% reachable / valid**. If either has drifted, something changed underneath —
stop and report rather than proceeding on a moving base.

### Stage B — per-view prompts (the design work of this run)

The first loop used **one prompt for all eight strokes** and the brush invented a corroded
wavy blade and a belt medallion that exists nowhere in the character. A shared prompt is
also what put a face on the back of the head until E01 fixed it per-view.

**Write eight prompts, one per camera.** The rule, not the literal text: *describe what
that camera can see, and omit what it cannot.* A rear camera must not be told about a beard
or a necklace. A raised-elevation camera sees the tops of shoulders and the crown, not the
face. Keep the palette and material words constant across all eight — they are identity;
only the anatomy and framing words change.

Record all eight verbatim in the report. They are the recipe, and the previous run's
recipe was lost because it lived only in a log.

### Stage C — the blade policy

The first run excluded the blade from diffusion via a **hardcoded pixel rectangle** in
`texpass_loop.ps1` (`m[80:580, 385:470] = 0`). That is character-specific and will not
generalise.

Keep the policy — thin hard-surface props take projected colour, never invented content —
but **derive the exclusion from geometry rather than pixels**: exclude hole texels whose
local surface is thin or whose normals vary sharply across a small neighbourhood, or
simply exclude by a named material/region if the mesh supports it. If a principled
derivation is not reachable in this session, **say so and use the pixel rect with a loud
comment** — do not quietly ship a magic rectangle as if it were general.

### Stage D — the loop

`texpass_loop.ps1`, eight strokes: yaws 90, 270, 45, 135, 225, 315 plus elevations
±55 at yaws 0 and 180. Then `texpass_finalize.py`, then `bake_hero_pack.py`.

**ComfyUI must be launched with a VRAM cap** — `--reserve-vram 8.0 --disable-smart-memory`.
Bare launch peaks at the watchdog's kill ceiling and the watchdog will terminate it
mid-run. This has happened twice.

Every brush output is saved seed-stamped. A re-roll must never destroy a prior stroke.

### Stage E — verification renders

- FLAT turnaround, 8 views, `turn_render.py --flat`
- FLAT head close-up, `head_render.py --flat`, at the Director's zoom
- The same two for the **rejected A0 asset** (`warrior/texpass/warrior_texpass.glb`), same
  framing, same light
- A `--clay` head render of W3 for reference, so geometry and texture can be separated by eye

---

## 4. Gates

**Gate 0 — after the first stroke, before committing it.** Send the render / mask /
inpainted triptych. The first loop's opening stroke is where invented content shows up
first. State whether anything appears that is not in the character.

**Gate 1 — the finished asset.** Send the FLAT turnaround and head close-up **beside the
rejected A0 asset at identical framing**. State your prediction first. **The Director's eye
is the verdict** — do not pre-empt it, and do not describe the output as good or bad in the
message that carries it.

---

## 5. Measurements

| what | why |
|---|---|
| styled / reachable, before the loop | the starting point, comparable across meshes |
| holes remaining after each stroke | the loop's progress; should fall monotonically |
| holes closed by `finalize` vs by the brush | how much is real paint vs dilation |
| final atlas variance, non-black fraction | catches a black or uniform atlas |
| head texel density (UV area vs 3D surface area, head rect) | did the head keep its allocation through the whole pipeline |
| wall-clock per stroke, total | cost of the route per character |

---

## 6. Report format

`docs/experiments/E02-report.md`:

```
## What ran            — commands, pins, wall-clock
## The eight prompts   — verbatim
## Measurements        — the table above
## What failed         — exact errors, exact commands, no interpretation
## Open questions the data raised
```

No conclusions section, no recommendation, no next-steps plan. The advisor writes those
after the Director has judged. Your report is evidence, not argument.

---

## 7. Explicitly out of scope

**E03 — the head graft.** E01 established that a bust crop yields materially better facial
geometry (separated eyelids, modelled nostrils) but that a bust mesh cannot ship: it has no
body, and `project_twins` registers against the mesh bbox, so a full-figure twin on a bust
misregisters ~7×. Getting the bust's face onto a full-figure body — graft or detail
transfer — is the next experiment. **Do not start it here.** Note anything E02 reveals that
bears on it.

Also out of scope: the second subject (P), generator comparisons, and any change to the
mesh itself. E02 is one mesh, one question.

---

## 8. Standards compliance

**PIN_PER_STEP — 3.** Mesh, seed, backend, twins, UV parameters, mask construction and
projection thresholds are all pinned by path and value; the eight prompts get recorded
verbatim, closing the gap that lost the previous recipe.

**ANDON_AUTHORITY — 3.** Stage A halts on a drifted baseline; Gate 0 halts on invented
content before seven further strokes are spent; the loop's own asserts halt on a black or
uniform atlas. Improvising past a gate is named as forbidden.

**NAMED_COMPENSATORS — skip, justified.** No irreversible actions: local file writes under a
fresh directory, one repo commit, nothing published or deleted. Undo is `git revert`, owner
the advisor.

**DECOMPOSE_BY_SECRETS — 3.** Prompts (volatile, per-view) are separated from the loop
mechanics (stable); the blade policy is separated from its character-specific
implementation; verification renders are specified independently of results.

**UNCERTAINTY_GATED_HUMANS — 3.** Two Director gates at genuine decision points, not step
counts. Both require a stated prediction first, so a surprise reads as a surprise.

**EXTERNAL_VERIFIER — 3.** The executor never grades its own output. The Director's eye is
the verdict on quality; the numeric checks were written before this run and are geometric
rather than aesthetic. Side-by-side against the rejected asset means the comparison is
against a judgement already made, not against the executor's taste.

---

## 9. Handoff

Report to the Director, who brings it to the advisor. The advisor folds findings into the
README status table, rules on whether the texture architecture is sound, and specs E03.

**Nothing from this experiment enters the memory store. The repo is the record.**
