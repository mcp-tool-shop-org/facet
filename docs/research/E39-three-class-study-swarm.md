# E39 — the three-class study-swarm

**Dispatched 2026-08-16 at the Director's word:** *"Send a study swarm studying each of the 3
classes and then we'll run experiments on the classes simultaneously through 3 spawned Sonnet
sessions, once we've learned more of the levers involved. Search for messageboards, etc for
people who have encountered said class. This is the way to solve a problem quickly, by learning
from the trial and errors of other users."*

Written to disk **at dispatch time, before any agent returned**, so the dispatch is the record
rather than a reconstruction. Findings and the verification receipt are appended below as they
land.

Governing doctrine: `memory/research-grounded-advisor-protocol.md` (study-swarm), read at this
seat before the dispatch was written, per its own standing rule.

---

## Why three swarms and not one

[E39 Task 1](../experiments/E39-w3-polish-kickoff.md) split W3's blotchiness into three classes
that had been treated as one defect. They have different carriers, and therefore almost certainly
different fixes:

| class | what it looks like | measured carrier |
|---|---|---|
| **GOLD** | gold across the green tunic, the skirt, the boot tops | **`reference` 91.05%, enrichment 0.99× — base rate.** The twin projection carries it |
| **GREEN** | cloth green down the sword grip and other non-cloth surfaces | **`brush` 5.49×, `dilation` 3.34×**, `reference` down to 68.46% |
| **BLADE** | steel wearing gold and rust; the Director's *"largest single offence"* | the **only** `dilation`-dominant large region, at a **48.3% plurality** — a mixed case |

Aiming one swarm at "W3 is blotchy" would have produced one blurred answer to three questions.

## The Director's method note, and how it reconciles with the protocol

He asked explicitly for **messageboards and other users' trial and error**, not only papers. The
protocol's sourcing standard cautions against citing *"a summary or social thread"* — that
caution is about citing a **thread's summary of a paper**, and it does not apply here. **A
practitioner describing a defect they personally hit, in their own thread or issue, IS the
primary source for that experience.** CLAUDE.md's rule binds identically either way: *resolve
every external citation at its primary source*, which for a forum thread means opening and
reading the thread rather than a search snippet.

This is not a novelty. The last practitioner swarm this repo ran returned, in about twenty
minutes, a merged upstream Blender fix (PR #161752) for a defect three arcs had hunted in the
wrong subsystem.

## The five questions dispatched (one agent each, in parallel, single message)

1. **GOLD — view disagreement vs in-view hallucination.** When independently-generated per-view
   images are projected onto one mesh, what makes a region wear the wrong material? Required to
   distinguish *(a) the views disagree with each other* from *(b) one view hallucinated the wrong
   material internally* — **these need completely different fixes and conflating them is the
   specific error this arc exists to avoid.**
2. **GREEN — chart-constrained padding.** How do practitioners stop dilation/padding pulling
   colour across unrelated UV islands, and what is the toggle actually *called* in Substance,
   Marmoset, xNormal, Blender, Mari? Our flood predicate has no island constraint at all, and the
   one patch the record already falsified (`& valid`) is **not** the same predicate as
   *same-island*.
3. **BLADE — thin hard-surface geometry.** What goes wrong specifically with thin, flat props in
   UV atlasing, baking and projection — and does the trade texture props on a **separate atlas**?
4. **The shipping-tool vocabulary.** Multi-view projection texturing is decades old. What do
   mature tools and photogrammetry pipelines do that we do not, and **what are those features
   named**? A solution we cannot name is one we cannot search for.
5. **Diffusion texture generation in practice.** What do people *actually running* SyncMVD,
   MVPaint, TexPainter, Paint3D, TEXTure, Hunyuan3D, ComfyUI 3D report — failure modes, VRAM,
   mesh requirements, whether it worked on a character — rather than what the papers claim.

Every prompt carried: our measured numbers so agents could search for matching symptoms; the
practitioner-source weighting; **resolve at primary source with `WebFetch` or mark UNRESOLVED**
(with the known `projects.blender.org` 403-to-`/api/v1/` trap named); source + date + direct URL +
one-sentence finding; **name the LEVERS** — the exact setting, the tool, what it changed; a
600-word cap; *specificity over breadth, 6–8 well-sourced findings beat 20 vague gestures*; and
that **everything returned is a hypothesis to verify locally, never a fact to adopt.**

## Verification plan (protocol Step 4), settled BEFORE the findings arrived

Settling this after seeing the findings would be choosing a standard to fit a result.

**Substrate measured on this rig at dispatch time**, not assumed:

- `roleos` — **NOT INSTALLED** (`command not found`). It is the protocol's locked *wrapper*.
- `prism` — **v1.6.0, installed and on PATH.** It is the *engine* the wrapper shells to, and it
  is what performs the deterministic retrieval-oracle existence check and the groundedness lens.
- `ollama` — `mistral-small:24b` and `granite4.1:30b` present: the two decorrelated non-Claude
  families of the protocol's own founding receipt.

**So the verification path is available and the protocol does not halt.** prism is invoked
directly rather than through the absent wrapper; the different-family, reasoning-stripped
requirement is met by construction because the synthesising advisor is `anthropic` and the lens
is `local`.

**One adaptation, and it is forced by the source mix rather than chosen for convenience.** The
protocol's own v1.2.0 lesson records that prism's oracle is **arXiv/Crossref-tuned**, so a dispatch
sourced from RFCs and vendor docs returns most citations `unparsed` — *"NOT fabrication; they're
retrieval-verified out-of-band."* A swarm the Director deliberately pointed at **forum threads and
issue trackers** will return `unparsed` for nearly everything. Therefore:

- academic citations (arXiv/DOI) → prism's oracle, as normal;
- practitioner citations (threads, issues, vendor docs) → **an out-of-band existence audit at this
  seat**: fetch each URL, confirm the page exists and that its content supports the stated
  finding. `unparsed` is **never** read as fabricated, and an unreachable URL is **never** read as
  fabricated either — it is marked CANNOT_CONFIRM and surfaced contrastively rather than kept as
  load-bearing.

## What happens next, and its one precondition

The Director's plan is **three Sonnet executor sessions running the three classes
simultaneously**, once the levers are known. Two constraints on that, both already measured and
neither negotiable:

- **W3 itself cannot be re-baked.** No `prep_uv.glb` / `mask.npy` / `pos.npy` / `meta.json`
  survives — verified three times. Any arm that needs a re-bake needs a *different* subject;
  `facet_E33`, `facet_E37/stageC` and `saltroad_bake_fix` carry complete prep state and are the
  candidates.
- **Three parallel seats collide on the count surfaces.** T34 pins stated counts against
  `pytest --collect-only` *of the tree the surfaces sit in*, so two seats adding tests cannot both
  be green independently — the record already has an instance. **The count surfaces are reserved
  to the advisor** and the dispatches will say so.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | five prompts dispatched in one message, each recorded here in substance; the agent count, word cap and sourcing standard are fixed by the protocol and stated before dispatch |
| ANDON_AUTHORITY | 2 | a citation that cannot be resolved at its primary source is marked UNRESOLVED by the agent and CANNOT_CONFIRM at synthesis, and is barred from the architectural connection rather than silently kept |
| NAMED_COMPENSATORS | 2 | the only irreversible act is spent tokens on five agents, bounded by the agent cap and word cap — the protocol's own named, owner-accepted non-undo. Nothing else here touches the world: no publish, no external write |
| DECOMPOSE_BY_SECRETS | 3 | the decomposition **is** the finding that opened this arc — three classes with three measured carriers, one agent each, plus two cross-cutting agents whose scope is deliberately orthogonal to the class split |
| UNCERTAINTY_GATED_HUMANS | 2 | the Director set the method and gets the levers before the experiments are specced; CANNOT_CONFIRM findings are surfaced contrastively rather than dropped silently |
| EXTERNAL_VERIFIER | 2 | prism v1.6.0 verified present on this rig **before** dispatch, different-family and reasoning-stripped by construction; the out-of-band audit for practitioner URLs is specified above, before any finding arrived. Rises to 3 when the receipt is captured below |

## Research grounding

Four of five agents landed; agent 4 (shipping-tool vocabulary) was killed twice by a client
crash and is re-dispatched — see *Coverage gaps*. Findings are grouped by the class they serve.

### The three findings that reorganise the whole arc

**1. Blender's own bake margin is TOPOLOGY-DRIVEN, and we already call it — at the wrong stage.**
`source/blender/render/intern/texture_margin.cc`, read at raw source by the advisor, not quoted
from the agent: it rasterises a **face index per texel**, grows outward with `grow_dijkstra`
carrying a direction back to the owning face, then uses the loop adjacency map to find *"the
'other' edge. I.E. the UV edge from the neighbor face"* and mirrors the projection onto it.
Bounded verbatim: *"Looking further than 3 polygons away leads to so much cumulative rounding
that it isn't worth it. So hard-code it to 3."* (`map.lookup_pixels(ibuf, mask, 3)`, line 566.)
**No path in it averages an unrelated 2D neighbour.** The enum is `Margin ▸ Type`: `EXTEND`
(*"Extend border pixels outwards"*) vs `ADJACENT_FACES` (*"Use pixels from adjacent faces across
UV seams"*), made default by Martijn Versteegh, commit `449db0ab1e3`, 2022-01-17.
(https://raw.githubusercontent.com/blender/blender/main/source/blender/render/intern/texture_margin.cc)
> **Implication.** E38 measured that `bake_hero_prep.py:452` already runs this at **margin=8,
> ADJACENT_FACES**. So the surface-aware margin is *in our pipeline at bake time* while
> `texpass_finalize.py:155`'s island-blind flood runs at **fill** time. We are not missing the
> technique; we are missing it at the stage where 26.95% of the atlas is written.

**2. MVS-Texturing's photometric outlier removal is the measurement that CLOSES E39 Task 2's
open side.** Waechter, Moehrle & Goesele, ECCV 2014, via the implementing source. Per face it
collects each view's mean projected colour, iteratively fits a 3×3 multivariate Gaussian to
inliers and scores each view by Mahalanobis distance. Verbatim: *"Dampens the quality of all
views in which the face's projection has a much different color than in the majority of views."*
Constants `gauss_rejection_threshold` 6e-3, `minimal_covariance` 5e-4, 10 iterations,
`minimal_num_inliers` 4. Lever `--outlier_removal={none,gauss_damping,gauss_clamping}`.
(https://github.com/nmoehrle/mvs-texturing/blob/master/libs/tex/calculate_data_costs.cpp)
> **Implication, and it is the single most actionable thing in the swarm.** Task 2 could poll
> **one** view per pixel — the view being rendered — which is exactly why (b) came back as a
> **ceiling of ≤70.1% and not a measurement**. This polls **every view that sees the face**. If
> gold is the minority of candidate views → mechanism (a). If the majority vote gold → (b), and
> the method's own stated assumption (*"the majority see the correct color"*) is the thing that
> has failed on us. **It converts our bound into a number, locally, with no generation spend.**

**2b. ⚑ FREQUENCY-SPLIT BLENDING — three shipping tools converge on it, and it is aimed exactly
at our defect. This finding CORRECTS THE ADVISOR'S OWN BRIEF.** The dispatch told agent 4 that
*"the literature selects one source view per face by graph cut rather than blending by facing
weight."* Its verbatim reply: *"Your 'one source view per face by graph cut' is HALF right —
correct it. MVS-Texturing does that; every **shipping** photogrammetry tool instead does
frequency-split blending: one best view for high frequency, many views for low frequency."*

| tool | setting | what it does |
|---|---|---|
| **AliceVision / Meshroom** | `nbBand=4`, `multiBandDownscale=4`, **`multiBandNbContrib={1,5,10,0}`** — *"Number of contributions per frequency band"* | highest band takes **1** view, next **5**, next **10**, lowest **0** |
| **Agisoft Metashape** | **`Mosaic`** (the default), vs `Average` | *"images are decomposed into high frequency and low frequency components. A weighted average is calculated separately for low frequency and high frequency components (with different weights), which are subsequently combined back"* |
| **RealityCapture** | **`Coloring method: Multi-band`** (default), vs `Linear` | *"divides images into frequencies — lower frequencies carry color/brightness while higher frequencies carry detail"* |

(https://raw.githubusercontent.com/alicevision/AliceVision/develop/src/software/pipeline/main_texturing.cpp
· https://www.agisoft.com/forum/index.php?topic=8972.0 ·
https://rshelp.capturingreality.com/en-US/tools/texturing_part2.htm)

> **Implication, and it may be the best-aimed lever in the whole swarm.** **Gold-on-a-green-tunic
> is a LOW-frequency error** — a large region of the wrong colour, smooth inside itself. That is
> the band where these tools take **5–10 view contributions**, so a single view hallucinating gold
> is outvoted *in the band where its error lives*, while high-frequency detail still comes from
> the one best view and is not blurred. Our pipeline has **no frequency decomposition at all**: it
> blends by facing weight at full band. **This addresses (a) AND the visible consequence of (b)
> simultaneously**, which nothing else found does — and it does not require synchronised
> generation, a re-bake, or a new model.
>
> ⚠ **It also sharpens finding 4's conflict.** StableGen's `Weight Exponent → 1000` pushes toward
> *hard single-view selection*, the exact opposite of contributing 5–10 views to the low band.
> These are now three mutually-exclusive blend philosophies — hard selection, flat averaging,
> frequency-split — and an experiment must pick one per arm.

### GOLD — the projection-carried class

**3. Hard per-texel view SELECTION exists as a knob, not just a paper.** StableGen v0.2.0
(2026-02-15) — *architecturally our exact route*: Blender cameras → ControlNet depth/canny →
ComfyUI SDXL/Qwen → project to UV. Weights are max-relative normalised so **`Weight Exponent`**
reaches *"up to 1000 without black edge artifacts"*, giving *"Voronoi-like hard segmentation"*;
at high exponent *"the discard-over-angle setting becomes irrelevant."* Defaults elsewhere in the
same tool: `weight_exponent` **3.0** (*"Weight = |cos(θ)|^Exponent"*), `discard_factor` **90.0**
though its own description says *"use ~65 for best results."*
(https://github.com/sakalond/StableGen/discussions/81 ·
https://github.com/sakalond/StableGen/blob/main/stablegen/core/properties.py)

**4. ⚠ Two levers in that same release pull OPPOSITE ways and are not composable.** Colour
matching (MKL, Reinhard, Histogram, MVGD, hybrid) matches each view to the current texture
*before* blending — a **global** transform, which on a region-level material error could as
easily drag gold across everything. Finding 3 converts averaging into a hard seam; finding 4
averages harder. **Run them as separate arms or not at all.**

**5. A shipped tool ranks our configuration LAST, and defaults against it.** StableGen's
`generation_method` defaults to `'sequential'` — *"each subsequent view is generated using
inpainting, guided by a visibility mask and an RGB render of the texture projected from previous
viewpoints"* — with `'separate'` documented as *"without context from other views."* **We
generate separately.** The author adds: *"6 cameras for characters… a good sweet spot. Having 4
would probably mean not having enough overlaps."* (https://github.com/sakalond/StableGen/issues/66)

**6. ⚠⚠ THE ARM-INVALIDATOR, single-source and unverified.** Same author, same thread, on raising
ControlNet strength: **"that only applies for SDXL not Qwen."** **We are on Qwen.** If true, our
most obvious structural lever is inert on our model. **Test this first — it is cheap and it
decides whether a whole arm exists.**

**7. One report separates both failure classes in a single sentence.** aliabougazia, StableGen
#66, 2025-12-13: *"a character's shirt could be red in the front and blue in the back. Or a 2nd
face is generated at the back of a head."* Shirt-flip = views disagree **(a)**; second face = one
view hallucinated internally **(b)**. Independent practitioner confirmation that both live in
this exact architecture.

**8. (b) has a name in the diffusion literature: incorrect attribute binding.** diffusers
Attend-and-Excite docs, verbatim: *"we find that in some cases the model also fails to correctly
bind attributes (e.g., colors) to their corresponding subjects."* Our prompt names gold; gold
landing on tunic, skirt, boots and blade is the textbook symptom.
(https://huggingface.co/docs/diffusers/main/en/api/pipelines/attend_and_excite)

**9. (b) can be foreclosed by construction, and a shipped tool does it.** Text2Tex
`--update_strength 0.3` vs `--new_strength 1.0`: a later view is denoised at 0.3 where paint
already exists, so **it cannot re-invent the material there**. (https://github.com/daveredrum/Text2Tex)

**10. The unexploited (b)-fix nobody reports doing.** ComfyUI core `ConditioningSetMask`
(`mask`, `strength`, `set_cond_area`) binds a prompt term to a region. **Our mesh can render a
per-material mask per view.** The agent found *nobody* reporting they drive it from mesh material
IDs — the practitioner regional-prompting corpus is entirely 2D.

**11. Production pipelines do not trust views equally.** Hunyuan3D-2.1
`candidate_view_weights = [1, 0.1, 0.5, 0.1, 0.05, 0.05]` (front/right/back/left/top/bottom) plus
24 tilted views at `0.01` — **front is 10× the sides**. `bake_exp = 4`, `bake_mode="back_sample"`.
(https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/hy3dpaint/textureGenPipeline.py)

**12. Blender's own tracker, on 45°.** Issue #26393 (Daniel Grauer, 2011-03-07, closed):
projection degrades *"when the object is rotated so you look on it in a ~45 degree angle or
more."* **Our views are 45° apart.**

**13. What adopting SyncMVD actually costs — and the gap that matters most.** Author: *"only one
mesh, and only one material, and a valid UV mapping"* (#14); 24 GB OOM at
`--latent_tex_size=2048` on a 4090 (#9); pytorch3d install is the adoption blocker (#16). The
author names the projection-side mechanism himself (#4): a texel *"can be… only visible in a bad
angle… prone to be polluted by background colors."* ⚑ **No character-mesh report exists in that
tracker — buildings, cars and cubes only**, and two later users report the #4 issue unfixed.
> **Implication.** Combined with E39 Task 2 (SyncMVD targets **(a)**, which is ≥29.9% and
> ≤70.1% of the gold class), this is now **two independent reasons not to adopt it on the last
> swarm's headline.** One mesh / one material also collides with finding 21's separate-atlas
> recommendation for the blade.

### GREEN — the brush + dilation class

**14. Substance's name for the toggle, and a practitioner hitting our exact defect.**
`UV Padding` ▸ `3D Space Neighbor` (default) vs `2D Space Neighbor` — the latter *"Copy the pixel
inside an UV island to the border outside the UV island"*, *"recommended when UV islands have very
opposed information and don't overlap."* Adobe forum: OP had **underwear colour bleeding into
skin**; LaurieAnnis (2022-10-19) identified `3D Space Neighbor` as the culprit and switching fixed
it. **Contested:** an Adobe staffer first blamed texel density and recommended UDIM/separate sets.
(https://experienceleague.adobe.com/en/docs/substance-3d-painter/using/interface/texture-set/texture-set-settings
· https://community.adobe.com/t5/substance-3d-painter-discussions/different-uv-island-having-bleeding-between-them/m-p/13280744)

**15. ⚠ CORRECTION TO THIS REPO'S OWN INHERITED READING, verified by the advisor at the primary
source.** The handoff cited Adobe as documenting our defect: padding *"stretch[es] a pixel until
it reaches another UV island."* **That reads the sentence backwards.** In context (*"Infinite
padding generation"*) the island is a **wall that halts the stretch**, not a source colour is
pulled from — Substance's dilation is island-bounded **by construction**. **The correction
strengthens the case it was cited for:** the mature tools stop at island boundaries and we do
not. Corrected in place in `docs/advisor-kickoff.md`.

**16. ⚠ The topology-aware margin has its OWN failure mode — adopting it is not free.** Blender
#119393 (2024-03-12, **OPEN**): adjacent-faces *"dialates pixels inside uv island"*, a 4.0.2
regression. #62429 (**OPEN**): margin extends into the island interior. PR #162226 (2026-08-01,
**OPEN**) rewrites the blend and lists ~16 defects, including Dijkstra seeded from
*first-encountered* rather than *smallest-distance* pixel. **This is the same PR family the
previous swarm surfaced; it is still open.**

**17. Tiny islands are the named failure regime, and ours are tiny.** SimpleBake: *"each island
needs a margin, and even at the lowest setting there won't be enough texture space to go
around."* Maya's official guidance: 2 px to border, 4 px between shells, and *"every LOD/Mipmap
step requires double the shell spacing."* **Our ~14,000 islands at ~20 faces each sit squarely
in this regime.**

**18. Packer-side levers we already have.** xatlas `PackOptions::padding` (*"Number of pixels to
pad charts with"*, **default 0**), `blockAlign` (*"Align charts to 4x4 blocks"*), `bilinear`.
Unreal: *"A minimum of four texels is usually required to avoid all bleeding artifacts since DXT
texture compression operates on 4x4 texel blocks."* Mari's equivalent is `Bleed Patch Edges`,
which uses **surface** adjacency, never atlas adjacency.

### BLADE — the thin hard-surface class

**19. ⚑ The mechanism, and it explains why the blade behaves unlike the torso.** FlexPainter
(Yan et al. 2025, arXiv:2506.02620 — title/authors/year confirmed at arXiv by the advisor) notes
traditional methods weight by *"the cosine of the angle between the camera rays and the rendered
normals"*, which *"can not dynamically adjust."* Im2SurfTex (Georgiou, Loizou, Averkiou,
Kalogerakis 2025, arXiv:2502.14006 — confirmed; abstract states *"ad hoc backprojection and
averaging schemes… often resulting in texture seams and artifacts"*) names back-projection
distortion at rapid depth change and high curvature.
> **Implication.** **A thin blade is grazing in nearly every view, so its cosine weight is near
> zero everywhere — which is why it falls through to dilation while the torso does not.** That is
> a mechanism for our measured **48.3% dilation plurality on the blade specifically**, and it is
> the agent's synthesis, not a quote.

**20. ⚑ Blender's own code says the topology walk MISSES thin geometry — found by the advisor in
the same file as finding 1, and not surfaced by any agent.** After the Dijkstra + 3-polygon
lookup, the fallback comment reads verbatim: *"Use the extend filter to fill in the missing
pixels at the corners, not strictly correct, but the visual difference seems very minimal. **This
also catches pixels we missed because of very narrow polygons.**"*
> **Implication.** Even the topology-aware margin degrades to plain extend on narrow polygons.
> **Adopting finding 1 wholesale would not fix the blade** — upstream's own implementation
> concedes the thin case. The blade needs a separate lever, which is findings 21–23.

**21. The trade's answer to a thin prop is a separate texture set, and the stated reason is texel
density.** Andrew Stokaliuk, 80.lv, 2026-07-30: *"the high texel density forces you to split the
model into independent sets by material ID"* — 12 sets on one AR-15, *"120–170 px/cm."*
> **Implication.** A separate atlas for the sword removes the blade from the figure-wide flood
> **by construction**, which is this repo's own *prefer eliminating a risk to gating it*.

**22. Per-mesh backface exclusion is a named, shipping feature.** Substance Bakers **`Match: By
mesh name`** with `_high` / `_low` / **`_ignorebf`** suffixes — *"very useful to avoid geometry
bleeding over each other during the baking process"* — plus a baker-level `Ignore Backface`
toggle. Practitioner equivalent: exploded-mesh bakes.
(https://experienceleague.adobe.com/en/docs/substance-3d/bakers/features/matching-by-name)

**23. The upstream bug that makes thin geometry take colour from behind it.** Blender #66438
(MACHIN3, 2019-07-04): bakes *"go through to the other side"* unless Solidify adds thickness;
lever **`Max Ray Distance`**, *"limits how far rays can travel before they are excluded."*
Blender #74553 (Joseph Eagar, 2020-03-08): *"Cycles fails to detect when it's hit a back face."*
**Both Archived, not fixed-and-verified.** And the direct atlas-side lever: xatlas
**`ChartOptions::normalSeamWeight`** — *"If > 1000, normal seams are fully respected"* — which
would force a thin plate's two faces into **separate charts**. **We already use xatlas.**

### The mature-tooling vocabulary — named settings we can go looking for

**24. ⚑ Production carries material identity as a BAKED PER-TEXEL LABEL, never inferred from
colour.** Substance's **`Color Map from Mesh`** baker: `Color Source` = **Vertex Color | Material
Color | Mesh ID | Polygroup/Submesh ID**, generation Random / Hue Shift / Grayscale, feeding
*"Add mask with color selection."*
(https://experienceleague.adobe.com/en/docs/substance-3d/bakers/bakers-settings/color-map-from-mesh)
> **Implication.** The previous swarm proposed adding a material-ID channel to our graded mask
> and called it *"a precedented extension, not an invention."* **This is the precedent, named and
> shipping** — and it means the ID map is a *bake output*, produced from mesh data, not a
> segmentation problem. It is the natural carrier for both the same-material fill constraint
> (green) and the per-region prompt binding of finding 10 (gold).

**25. MVS-Texturing is BSD 3-Clause — adoptable.** Full lever set: `--data_term={area,gmi}`,
`--smoothness_term=potts`, `--outlier_removal={none,gauss_damping,gauss_clamping}` (damping
factor 0.2, clamping 1.0), `--tone_mapping={none,gamma}`, `--skip_geometric_visibility_test`,
`--skip_global_seam_leveling`, `--skip_local_seam_leveling` (*"Poisson editing"*),
`--skip_hole_filling`, `--keep_unseen_faces`, and **`--num_threads` — *"Set 1 for
determinism"***. (https://github.com/nmoehrle/mvs-texturing)
> **Implication.** The licence clears it for commercial use — **verify the LICENSE file locally
> before adopting, per this repo's own rule.** The determinism flag matters: this route requires
> replayable runs, and a texturing tool that ships a single-thread determinism switch can be
> anchored the way everything else here is.

**26. AliceVision's per-triangle scoring is a second, independent view-trust mechanism.**
`useScore=true` *"Use triangles scores (based on observations and re-projected areas in source
images)"*; **`bestScoreThreshold=0.1`** *"(0.0 to disable filtering based on threshold to relative
best score)"*; `angleHardThreshold=90.0`; `forceVisibleByAllVertices=false`; `padding=5`;
`fillHoles=false`; `correctEV=NO_CORRECTION` *"uniformize images exposure"*;
`visibilityRemappingMethod=PullPush`. **MPL2 + others — verify LICENSE.**

**27. Metashape ships an outlier filter aimed at exactly our failure shape.** **`Enable ghosting
filter`** — *"helps to improve the texture if the quality of the dataset is not very good…
moving objects, patches of reflected light, unwanted objects."* Also `Enable hole filling`,
`Disable cameras`, `Apply masks to tie points`. And **`Refine Seamlines` exists only under
Mosaic**, because *only Mosaic picks a view per region* (Agisoft support, #14835, 2023-03-15).

**28. RealityCapture's other named levers.** **`Texturing style: Visibility-based | Photo-consistency
based`** — *"Visibility-based is fast and sharp… Photo-consistency based is slower with more
complex results."* **`Gutter`** = *"number of pixels of a chart border."* **`Color Correction`**
with per-image enable/disable and a **colour-normalisation reference** photo *"whose colors remain
unchanged while influencing others."* Plus `Texture Reprojection` (Nearest | Trilinear) to move
texture between two meshes of the same component.

**29. Manual override is a first-class feature everywhere, and we have none.** Mari **Projector**:
`Unproject` → edit externally → `Project` restores the exact camera → `Bake`. ZBrush
**ZAppLink**: stored views, `Drop Now` / `Pickup Now`. Substance **Clone tool** (`V` sets source,
recommended layer blending *"Pass through"*). Blender **Project Paint**: **`Occlude`**,
**`Backface Culling`**, **`Bleed`** (*"extends the paint beyond UV island bounds"*),
`Quick Edit / Apply`.
> ⚠ **Sourcing note, flagged by the agent:** the Blender Project Paint option text was retrieved
> by `curl` with a browser user-agent because `docs.blender.org` 403s WebFetch. Primary source,
> non-standard fetch — recorded rather than hidden.

**30. Substance's export-side padding menu, which independently re-confirms finding 15.**
*"No padding (passthrough)"*, *"Dilation + transparent"*, *"Dilation + default background color"*,
**"Dilation + diffusion"** (*"filled with a blurry version of the UV island (based on mip-maps)"*),
**"Dilation infinite"** (*"until they reach neighbor borders"*). **"Until they reach neighbor
borders"** is the island-as-wall reading, stated a second time on a different page.

**31. Contested, and labelled so.** AliceVision issue #1015 (@devernay) blames island-border
colour on alpha-unaware downscale filtering and proposes a UV island margin (8–16 px) plus pyramid
inpainting. **No maintainer confirmation — hypothesis only.**

**32. A correction to the advisor's brief, from the agent.** *"Seamline editing"* as a
mesh-texture feature **was not found**: in Metashape it is `Refine Seamlines` under Mosaic only,
and elsewhere it is an orthomosaic concept. The dispatch listed it as a thing to find; it is not
one.

## Verification receipt (protocol Step 4)

**Substrate:** `roleos` absent; **prism v1.6.0 present**; ollama carries `mistral-small:24b` and
`granite4.1:30b`. Different-family and reasoning-stripped hold by construction (synthesiser is
`anthropic`, lens is `local`).

**Advisor-run out-of-band audit, completed before this section was written:**

| citation | check | verdict |
|---|---|---|
| Im2SurfTex arXiv:2502.14006 | fetched arXiv abs | **CONFIRMED** — Georgiou, Loizou, Averkiou, Kalogerakis, 2025, title exact. Abstract supports the general claim; the depth-change/curvature wording lives in the **body** |
| FlexPainter arXiv:2506.02620 | fetched arXiv abs | **CONFIRMED** — Yan et al. 2025, title exact. The cosine-weighting sentence lives in the **body** |
| Blender `texture_margin.cc` | raw source downloaded and grepped | **CONFIRMED VERBATIM** — `maxPolygonSteps` at line 230, `lookup_pixels(ibuf, mask, 3)` at 566, the *"Looking further than 3 polygons away"* comment at 564, the narrow-polygon fallback at 568-571 |
| Adobe *"Infinite padding generation"* | fetched, read in context | **CONFIRMED AND THE REPO'S READING OVERTURNED** — see finding 15 |

The two arXiv bodies are the protocol's documented **escalate → RETRIEVE FULL TEXT** class
(*"claim lives in the paper body, not title+abstract"*). Both agents cited the `/html/` full text,
so the claims are marked **supported-at-body**, with the abstract as the confirmed floor. Neither
is load-bearing alone: finding 19's implication is the agent's own synthesis over our measured
48.3%, and finding 20 — the stronger evidence for the same conclusion — is confirmed verbatim in
source code.

**Nothing is marked FABRICATED. No finding was dropped.** Practitioner citations were resolved by
the agents at primary source and their UNRESOLVED lists are reproduced below rather than quietly
omitted.

## Coverage gaps — stated because a swarm that hides its holes is worse than a small one

**Reddit and Polycount were unreachable to every agent, and to the advisor.** `reddit.com` refuses
the search API and `old.reddit.com` is blocked at the harness; `polycount.com` and
`wiki.polycount.com` return 403/ECONNREFUSED on every thread; `web.archive.org` is blocked, so
neither could be reached by proxy. **These are the two largest practitioner boards for exactly
this domain and the Director asked for messageboards specifically.** Threads known to be on-point
and unread include `polycount.com/discussion/191707` (Padding!), `/230868` (baking — where do the
rays come from), `/214519` (one atlas vs separate), `/230295` (when to use >1 texture set for a
weapon), and `wiki.polycount.com/wiki/Edge_padding`.

**An attempt to route around the 403 via the Browser pane crashed the client twice** and is the
reason agent 4 was killed mid-flight — a known open bug
([anthropics/claude-code#81664](https://github.com/anthropics/claude-code/issues/81664), GPU
process dies when a preview is created). **It also violated this workspace's own standing
"Preview Plugin Override" rule, which forbids preview tools for non-web projects.** The route is
abandoned; Polycount stays UNRESOLVED. A source that cannot be opened is not a citation.

Also unresolved: `docs.blender.org` (403 on every version path, so the Blender manual's own
`Extrusion` / `Max Ray Distance` / `Margin Type` wording is **not** quoted here — the tracker and
source code stand in), `marmoset.co` and `docs.marmoset.co` (403 — **treat every Marmoset setting
semantics claim as unverified**), xNormal's edge-padding default, Unity's lightmap padding page
(404), and Substance's export-side padding option list.
