# E44 — The atlas plan

**Written 2026-08-16** by the advisor seat, after consult #11 and a five-agent study swarm.
Full swarm sourcing: [the sampling/rig swarm](../research/E41-E42-sampling-and-rig-study-swarm.md)
and this document's own citations. Consult log: `docs/comfy-consult-8-10-log.txt`,
brief `docs/comfy-consult-11-brief.md`.

> **THE STANDING RULE THIS PLAN IS WRITTEN UNDER (Director, 2026-08-16):** every arc from here
> ends with a picture that can be put beside the current one, or it does not count as done. A
> week of arcs ended in tables and the render never changed.

---

## The diagnosis, and what closes each escape route

W3's atlas has **9,166 UV islands** (14,010 before visible-face culling), **median 102 texels**,
largest 0.79% of painted area, and **17.8% of painted area within one texel of an island edge**.
A prior finding measured **5.73% of 4-adjacent valid texel pairs in different islands, touching
directly** — literal zero gutter.

Four independent routes were checked and each closes a different escape:

| escape route | why it is closed | source |
|---|---|---|
| Tune xatlas's chart weights | **The author says no.** jpcy, issue #91: *"The number of charts isn't supposed to be directly configurable… the ChartOptions weights, maxCost and maxIterations probably shouldn't be in the API so ignore those."* | github.com/jpcy/xatlas issues |
| Blame our parameters rather than the tool | **The author names our mesh class.** Issue #47: *"the mesh segmentation algorithm only really works well on fairly simple meshes with close to planar surfaces… the fallback method I'm using isn't fully implemented and tends to generate a lot of small charts."* Issue #84: *"High-poly models with a lot of curved geometry… tend to give poor results."* TRELLIS.2 + decimation is exactly that class | ibid. |
| Raise the gutter | **Geometrically unsatisfiable at our island size.** Unreal's minimum is 4 texels (BCn block size), Unity's floor 2 texels / default 4. At a ~10×10 median island, protecting even 2–3 mips needs a border approaching the island's own half-width | Wloka, NVIDIA WP-01387-001-v01 (2004); UE + Unity docs |
| Merge the charts we have | **No published method does this.** Both PartUV and UVAtlas re-segment from mesh geometry; nothing merges an existing atlas as a post-process. Blender's `stitch`/`weld` are manual and vertex-scoped | A5 swarm; `uv_pack.cc` |
| Re-unwrap with Blender's `smart_project` | **Already tried here and measurably worse** — 34,783 islands (8.3 faces each) against xatlas's 14,010 (20.5) on this exact mesh. Kept as `--reunwrap`, "the escape hatch, not the route" | `tools/bake_hero_prep.py:75-89` |
| Raise `angle_limit` | **Already tried here** — 1.15→1.5 rad moved island count 0.8% and changed nothing, because smart_project splits on UV *distortion* too and decimation's thin triangles distort at any threshold | `tools/bake_hero_prep.py:43-48` |

**So the island count is set upstream at unwrap time, it cannot be reduced afterwards, it cannot
be padded around, and the tool that produced it is documented as unsuitable for our mesh class.**

## ⚠ The causal gap, stated before the plan rather than after

**Nothing has proven that fixing the atlas fixes the blotchiness.** This is the same gap that
killed the border-distance lever, and it is named here so it cannot be quietly skipped.

What supports the atlas theory: every colour-side lever failed (blend variants, border weighting,
camera geometry, resolution, premultiplied alpha, minification); the defect **survives across two
entirely different colouring processes** — E38's procedural material and the diffusion build —
with **69.2% of surviving marks within 3 px of a mark in the other build**, which is what a
substrate-bound defect looks like.

What does not support it: no one has changed the atlas and looked.

**Therefore the render is the test, and if a coherent atlas does not change the render, the atlas
theory dies with it.** That is a real possible outcome of this plan and it is a full result.

## Two axes, and why we take the cheap one first

- **Axis A — a better unwrapper on the same mesh.** Geometry untouched, so the Director-accepted
  silhouette is preserved by construction and recorded anchors stay valid. `finalize` replays
  byte-identically from frozen state, so a new atlas can be re-projected and re-rendered locally
  with no generation.
- **Axis B — a better mesh.** Retopologise (Quadriflow / Instant Meshes) to a clean quad mesh, then
  unwrap, then bake high-to-low. This is the practitioner canon — *"never texture the raw AI
  mesh"* — but it **changes geometry**, which puts the silhouette and every recorded anchor at
  risk.

**A first.** It is cheaper, it is reversible, and it isolates unwrap quality from mesh quality. If
A succeeds we never spend B's risk. If A fails, its failure is itself the evidence that the mesh
is the problem, which is exactly what B needs to justify itself.

## Phase 0 — the before-picture, and the acceptance artifact

**Nothing else starts until this exists.**

1. Re-render W3 from the current atlas at the Director's zoom, flat-lit (`turn_render.py --flat`)
   and lit, on the four regions from E40's sheet plus the sword.
2. Record the island census as the pre-number, from the same instrument that will measure after.
3. Build the comparison sheet template: **current | candidate**, native pixels, no resampling.

This is the artifact every later phase fills in. It is the deliverable, not a step toward one.

## Phase 1 — re-unwrap, geometry untouched

Two arms, independent, both on a **scratch copy** of the mesh. `E:\AI\training` is not in git.

**Arm U1 — Microsoft UVAtlas.** MIT, archived April 2026, implements Iso-charts (Zhou et al.,
SGP 2004). Exposes **`maxChartNumber`** — a documented soft target, the explicit dial xatlas lacks
— plus `maxStretch`. No Python binding; drive `UVAtlasTool` by subprocess. Zero ML dependency.

**Arm U2 — PartUV.** Wang et al., SIGGRAPH Asia 2025, arXiv:2511.16659. Reports **48.6 average
charts against xatlas's 974.8** at comparable distortion. `pip install partuv`; needs PyTorch/CUDA
and a PartField checkpoint. ⚠ **Its LICENCE text was not retrieved by the swarm — resolve that
before it touches anything shippable.** This is a commercial project.

Measure on each, with the same instrument as Phase 0: island count, median island size, share of
painted area within one texel of an edge, packing efficiency, and UV distortion.

**GATE 1.** If neither arm gets island count below ~500 on our mesh, **halt and report**. That
result says the mesh — not the unwrapper — is the problem, and it is the evidence Phase 3 needs.

## Phase 2 — re-project and RENDER

For whichever arm clears Gate 1: re-run the projection onto the new atlas and re-render the
Phase 0 views. **Put the sheets in front of the Director.**

Supporting lever, cheap, run in the same pass rather than as its own arc: **`--margin-method`.**
Our packer has always run SCALED, whose code derives **one global gutter from the aggregate island
count** and applies it to every island identically (`uv_pack.cc:2111`,
`calc_margin_from_aabb_length_sum`). With far fewer islands, `ADD` or `FRACTION` become usable in
a way they are not today — `FRACTION` is the only mode where `margin` means a fixed share of
output space independent of island population. Both are already flags on `bake_hero_prep.py`.

⚠ **Two different things are called `margin` and their units differ**: `pack_islands` margin is a
UV-space float 0–1; **bake margin is a literal texel count** (`PROP_INT, PROP_PIXEL`). Do not
carry a number from one to the other.

**GATE 2 — the Director's eye.** Not a metric. The whole week's lesson is that every metric we own
failed to separate an asset he rejected from one he would accept.

## Phase 3 — retopology, ONLY if Gate 1 fails

Quadriflow (`bpy.ops.object.quadriflow_remesh`) or Instant Meshes (wjakob, GitHub) to a clean quad
mesh, unwrap that, then bake high-to-low from the current textured mesh
(`bpy.ops.object.bake(use_selected_to_active=True, cage_extrusion=…, max_ray_distance=…)`).

⚠ **Remeshing invalidates the existing UVs by construction** — new faces have no correspondence to
old charts, so the unwrap must follow the remesh, never the reverse. And ⚠ **auto-remesh does not
understand deformation zones**; elbows, knees and faces fold badly without guide loops.

**Pre-registered risk gate:** silhouette and first-hit depth against the current mesh, measured
before anything downstream is built on it. This repo has already learned that silhouette IoU is
blind to holes punched through visible surface — use the depth comparison, not IoU alone.

## Corrections this plan owes the record

1. **The SCALED mechanism we recorded was wrong, and we gave it away.** Consult #10's give-back
   said SCALED "scales the gutter by island size, so small islands get a sub-texel gutter." Read at
   source, there is **no per-island term**: one global margin is computed from the summed
   `sqrt(w·h)` of all islands and applied identically to each. The symptom follows either way; the
   mechanism does not. The Comfy agent banked our version — **correct it in the next brief.**
2. **E40's 74.28% blade never-hit is withdrawn as a coverage claim** (E42's ruling; the same
   instrument reports 97.99% never-hit on the *torso*, which is the best-covered surface on the
   figure).
3. **`facing^6.0` is not baseless** — it matches Meta 3D TextureGen's published α=6, §4.2.1.

## What is deliberately NOT in this plan

- Any generation or cloud spend. Every phase is local. Consult #11 established there is **no served
  path to ingest an off-platform mesh at all** — `Load3D.model_file` is a COMBO with
  `choices:["none"]`, no upload channel at any face count.
- Ptex — the Blender patch never merged, abandoned since ~2015.
- OptCuts — a published baseline clocks it at 35+ hours; we have 287,170 faces.
- Chart-merging post-processes — none exist.
- Vertex colours — ~143.6K vertices against ~935K addressed texels, two orders below a packed
  4096². Kept on the shelf as a fallback *because our deliverable is 8 stills, not a real-time
  asset*, and it is cheap to test-render if Phases 1–3 all fail.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Each arm is a named tool at a pinned version against one frozen mesh; measured by the instrument that produced the Phase 0 baseline. Not 3 — UVAtlas and PartUV are new dependencies with no anchor in this repo yet. |
| ANDON_AUTHORITY | 3 | Gate 1 halts on a pre-registered island-count threshold; Gate 2 is the Director's eye; Phase 3's silhouette/depth check is pre-registered before the arm that would break it exists. |
| NAMED_COMPENSATORS | 3 | All work on scratch copies under `E:\AI\training` (not in git). Compensator for any repo edit: `git checkout -- <path>`, owner = advisor. No irreversible external call in any phase — no publish, no generation, no credit spend. |
| DECOMPOSE_BY_SECRETS | 3 | Axis A (unwrap quality) and Axis B (mesh quality) are separated precisely so a result on one does not confound the other; Gate 1 is the boundary between them. |
| UNCERTAINTY_GATED_HUMANS | 3 | The causal gap is stated **before** the plan rather than discovered inside it, with the dying-hypothesis outcome named as a legitimate result. Gate 2 routes to the Director rather than to a metric. |
| EXTERNAL_VERIFIER | 2 | The swarm's findings were cross-checked against our own repo (which falsified the obvious re-unwrap plan) and against the consult (which independently closed the served route). Not 3 — no second seat re-measures Phase 1's numbers. Remediation: if an arm clears Gate 1, a second seat re-measures the island census before Phase 2 renders. Owner = advisor, at Gate 1. |
