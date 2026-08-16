# Grok consult #1 — brief

**Written 2026-08-16, facet advisor seat. CONSULT ONLY — no build, no code, no implementation.**
We want critique of a diagnosis and a plan, from an outside eye that is not inside our record.

*Everything below the line is the paste block. It is self-contained — Grok has no access to our
repo, our files, or our tooling.*

---

# A texture defect we have failed to fix for a week. Diagnosis and plan attached. Tear into it.

## What you are being asked to do

Read the problem and the plan. Then **argue with them.** We are not looking for encouragement or a
summary of what we said. We have spent a week producing well-reasoned conclusions that turned out
to be wrong, and the specific failure mode has been *elegant reasoning that survives because
nobody outside the frame checks it.* You are the outside.

Concretely useful: a mechanism we have got backwards, a route we have not enumerated, a number we
are misreading, a place the plan will break. If you think the diagnosis is right, say which part
you would still bet against and why.

**Please mark speculation as speculation.** We would rather have "I am not sure, but the shape of
this suggests X" than a confident answer we cannot check. Anything you assert as fact, we will try
to verify at source, and we will tell you what fell.

---

## PART 1 — THE PROBLEM, IN DETAIL

### What we are building

A pipeline that turns one concept image into a textured 3D character plus **eight painted
turnaround views** for a 2.5D JRPG. The subject here is "W3" — a standing dwarf warrior holding a
greatsword.

**A constraint that matters and is unusual: we never ship the mesh.** The deliverable is eight
rendered stills out of Blender. Nothing goes into a real-time engine. So formats and methods that
only work offline, or only work in Blender, are perfectly acceptable to us. Most advice in this
domain assumes a real-time target; ours is not one.

Commercial project — we intend to publish, so licence is a hard gate.

### The pipeline, stage by stage

1. **Concept image** — Qwen-Image diffusion with a house-style LoRA.
2. **Image → 3D** — TRELLIS.2 `1024_cascade`, run locally on an RTX 5090.
3. **Mesh** — TRELLIS's `to_glb`, which decimates. Result **287,170 faces**. Critically, **TRELLIS
   generates the UVs internally using xatlas**, and our decimation step carries those UVs through.
4. **Eight "twins"** — eight painted views of the character generated at 752×1024 with
   Qwen-Image + ControlNet, driven by Blender-authored control images. Cameras at yaw 0/45/90/…/315,
   with yaw 0 and 180 elevated to +55°; the other six at elevation 0. **Eight cameras total.**
5. **Projection into a UV atlas** — our own code, not off-the-shelf. For each atlas texel: raycast
   to find its 3D position, project into each twin that can see it, sample with a **hand-rolled 2×2
   bilinear** lookup, weight each view by `w = facing^6.0` (facing = dot of surface normal with
   direction to camera), then composite. Atlas is **4096×4096**, 2,402,810 valid texels.
6. **The composite is a two-band split**: `styled = M + gaussian_blur_σ16(B − M)`, where `M` is the
   single highest-weighted view's colour per texel (winner-take-all) and `B` is the
   facing-weighted blend of all accepting views. So **high-frequency detail comes from one view
   only; low frequency comes from the blend.** We measured this: impulse-in-M survival 99.94%,
   impulse-in-B survival 0.062%, an asymmetry of 1607×.
7. **Render** eight views in Blender.

### The defect

The Director's words, looking at four candidate variants side by side at native resolution:
**"They all look equally like shit. Only the reference image is clear. The rest are the same image
(blotchy)."**

The twin (the painted source image) is smooth, coherent, correctly-modelled. The rendered asset at
the same zoom is chunky and fragmented — hard-edged colour breakup, scattered wrong-material
patches, gold flecks on green cloth, green smeared down a leather sword grip that is clean brown
in the twin. **Good input, degraded output.**

### What we measured, and what each measurement killed

Everything below is measured on our own asset by our own instruments, mostly by dispatched
executor sessions that were explicitly told to try to kill the hypothesis they were handed.

**Killed — blend variants.** Multi-band, hard-select, and flat facing-weighted alternatives to the
shipped two-band composite. Mean ΔE against reference: shipped 34.24, hard-select 30.91,
multi-band 29.36, flat 26.41. The Director looked at all four at native scale and called them
indistinguishable. **The metric moved; the eye did not.**

**Killed — a border-distance weight term.** The classical multi-view texturing literature
(Callieri et al. 2008) multiplies its blend weight by image-space distance to the nearest material
boundary, because samples near a projected boundary are contaminated. We have no such term. We
found that defect texels sit **5.3× closer** to a material boundary in the twin than clean texels
(median 0.439 px vs 2.333 px). Looked promising. Then we computed the **ceiling**: across all views
that can see each defect texel, what fraction have at least one view with a clean sample? **45.97%
against a null of 100%**, and the owning view is already the best available view **47.53%** of the
time. There is nothing to reallocate to. Killed.

**Killed — camera geometry.** Our rig is 8 cameras and nothing looks down. We built the coverage
ladder: the blade is already **96.35% reachable** against a measured **99.75%** ceiling. Adding a
downward camera buys **+2.11 points**. Breaking the ring to ±30° interleaved (a configuration
published as measurably better) buys nothing here. **Coverage was never the problem.**

**Killed — source resolution.** Rescaling the measured boundary-distance distribution says doubling
the twin frame (752→1504) moves only ~11 points of the affected population and **43.97% still
straddles at 4×**.

**Killed — a premultiplied-vs-straight alpha error in our sampler.** We built a fixture calibrated
against the closed-form error, proved it could detect it, then ran it on the real construction:
**0.00e+00**.

**Killed — minification aliasing.** We have no mip chain and no footprint computation, so we
expected undersampling. Measured: defect texels are **less** minified than clean neighbours
(footprint 0.380 px vs 0.650 px). Real on the route generally, not the differentiator.

**Killed — a whole defect classifier.** We then looked at the twelve largest flagged regions
against canon. **Ten of twelve sit on gold surface that is correctly gold** — the classifier's
window reads the internal light/dark of ornamental scrollwork as "not gold" while standing on
unambiguously gold surface. Meanwhile the obvious visible defect — green smeared on a leather grip
— is **not flagged at all.** So a substantial share of what we have been measuring as "the defect"
was never the defect.

### The measurement that reframed everything

We finally looked at the atlas itself.

- **9,166 separate UV islands** (14,010 before culling faces no camera sees).
- **Median island: 102 texels** — roughly 10×10 pixels.
- Largest single island: **0.79%** of painted area.
- **93% of islands are under 500 texels**, holding 43.6% of painted area.
- **17.8% of painted area lies within ONE texel of an island edge** — and that is a one-texel rim;
  our dilation runs wider.
- A prior measurement: **5.73% of 4-adjacent valid texel pairs are in different islands and
  touching directly** — literal zero gutter.

Rendered, the atlas is confetti: thousands of ~10×10 blobs in a packed grid. Every one has a
boundary. Every boundary gets dilated. Every boundary is a discontinuity where the sampler and the
composite behave differently.

### Why we believe this is the root cause

**The strongest single piece of evidence:** we built a completely different colouring process — a
**procedural material authored directly in UV space**, no diffusion, no per-view sampling, no
projection anywhere. Two of the three defect domains were eliminated *by construction*. Measured
against the old diffusion build on the same mesh and cameras: a cross-view colour-banding problem
vanished, a projection seam vanished — **and the dark-mark defect survived**, halved but not gone,
with **69.2% of surviving marks within 3 px of a mark in the diffusion build.**

Two colouring processes with nothing in common, defects landing in the same places. That is what a
**substrate-bound** defect looks like — it lives in the thing both processes share, which is the
atlas.

### What closes each escape route

- **Tune xatlas's chart parameters.** Its author, in the project's own issue tracker: *"The number
  of charts isn't supposed to be directly configurable. The ChartOptions weights, maxCost and
  maxIterations probably shouldn't be in the API so ignore those."*
- **Blame our settings rather than the tool.** Same author: *"the mesh segmentation algorithm only
  really works well on fairly simple meshes with close to planar surfaces… the fallback method I'm
  using isn't fully implemented and tends to generate a lot of small charts"*, and *"High-poly
  models with a lot of curved geometry tend to give poor results."* TRELLIS.2 output plus
  decimation is exactly that class.
- **Increase the gutter.** Unreal's stated minimum is 4 texels (BC block size), Unity's floor is 2
  with a default of 4. **At a ~10×10 median island this is geometrically unsatisfiable** —
  protecting even two or three mip levels needs a border approaching the island's own half-width.
  We already cut our margin from 0.004 to 0.001 precisely because at this island count the gutter
  was consuming the atlas: packing efficiency went from 4.01% to 18.76%.
- **Merge the charts we have.** No published method merges an existing over-segmented atlas as a
  post-process. Both of the strong re-parameterizers work from mesh geometry, not from an existing
  chart layout. Blender's `stitch` and `weld` are manual and vertex-scoped.
- **Re-unwrap with Blender's Smart UV Project.** Already tried on this exact mesh: **34,783
  islands** (8.3 faces each) against xatlas's **14,010** (20.5). Measurably worse, and it is kept
  in our tool only as a documented escape hatch.
- **Raise the unwrapper's angle threshold.** Already tried: moved island count **0.8%** and changed
  nothing, because Smart Project splits on UV *distortion* as well as angle, and decimation's long
  thin triangles distort at any threshold.

**So: island count is set upstream at unwrap time, cannot be reduced afterwards, cannot be padded
around, and the tool that produced it is documented by its own author as unsuitable for our mesh
class.**

### One correction we owe, because it shows the failure mode

We recorded and propagated a claim that Blender's default `margin_method` (SCALED) "scales the
gutter by island size, so small islands get a sub-texel gutter." Read at source, that is **wrong**.
The code sums `sqrt(w·h)` across *all* islands into one number, multiplies by the margin parameter
and a hardcoded 0.1, and passes **that single float identically to every island.** There is no
per-island term. The symptom follows either way — one absolute gutter is trivial on a large island
and eats a 102-texel one — but the mechanism we published was not the mechanism. It had already
been handed to another consult channel and banked there before we caught it.

---

## PART 2 — THE PLAN, IN DETAIL

### The governing rule

Every arc from here **ends with a picture that can be put beside the current one, or it does not
count as done.** A week of arcs ended in tables and the rendered image never changed once. That is
the actual failure, and it is a process failure rather than an analytical one.

### The causal gap, stated up front

**Nothing has proven that fixing the atlas fixes the blotchiness.** This is the same gap that
killed the border-distance lever above — a strong correlation that turned out to have no lever
behind it. The evidence for the atlas theory is: every colour-side lever failed, and the defect is
substrate-bound across two unrelated colouring processes. The evidence against: **nobody has
changed the atlas and looked.**

So the render is the test, and **if a coherent atlas does not change the render, the atlas theory
dies with it.** That is a legitimate outcome and we have written it down in advance so we cannot
explain it away later.

### Two axes

- **Axis A — a better unwrapper on the same mesh.** Geometry untouched, so the Director-accepted
  silhouette is preserved by construction and our recorded measurement anchors stay valid. Our
  finalize stage replays byte-identically from frozen state, so a new atlas can be re-projected and
  re-rendered locally with no generation and no cost.
- **Axis B — a better mesh.** Retopologise to a clean quad mesh, unwrap that, then bake high-to-low
  from the current textured mesh. This is the practitioner canon — *"never texture the raw AI
  mesh"* — but it **changes geometry**, risking the silhouette and invalidating anchors.

**We chose A first**, because it is cheaper, reversible, and isolates unwrap quality from mesh
quality. If A fails, that failure is itself the evidence B needs.

### Phase 0 — the before-picture

Nothing else starts until this exists. Re-render the current asset at the Director's zoom, both
flat-lit and lit, on the regions he has already named. Record the island census with the same
instrument that will measure after. Build the `current | candidate` comparison sheet at native
pixels.

### Phase 1 — re-unwrap, geometry untouched

Two arms on scratch copies:

- **Microsoft UVAtlas** — MIT licensed, implements the Iso-charts algorithm (Zhou et al., SGP
  2004). Exposes **`maxChartNumber`**, a documented soft target for chart count — the explicit dial
  xatlas is documented as not having — plus a `maxStretch` control. No Python binding; driven as a
  CLI subprocess. Zero ML dependency. Archived April 2026.
- **PartUV** (Wang et al., SIGGRAPH Asia 2025, arXiv:2511.16659) — top-down recursive part
  decomposition that merges regions while keeping each chart's distortion under a threshold.
  Reports **48.6 average charts against xatlas's 974.8** on their benchmark at comparable
  distortion. Pip-installable, needs PyTorch/CUDA plus a model checkpoint. **Its licence terms are
  unresolved and must be settled before it touches anything shippable.**

Measure both: island count, median island size, share of painted area within one texel of an edge,
packing efficiency, UV distortion.

**Gate 1 — if neither arm gets island count below roughly 500 on our mesh, halt and report.** That
result says the mesh, not the unwrapper, is the problem.

### Phase 2 — re-project and render

Re-run the projection onto the new atlas, re-render Phase 0's views, put the sheets in front of the
Director. Also swap the packer's margin method in the same pass — with far fewer islands, the
absolute and fractional gutter modes become usable in a way they are not at 9,166 islands.

**Gate 2 is the Director's eye, not a metric.** Every metric we own failed to separate an asset he
rejected from one he would accept.

### Phase 3 — retopology, only if Gate 1 fails

Quad remesh, unwrap the result, bake high-to-low from the current textured mesh. Pre-registered
risk gate: silhouette **and first-hit depth** against the current mesh before anything downstream
is built on it — we have already learned that silhouette overlap alone is blind to holes punched
through visible surface.

### Explicitly out of scope

No cloud generation (we established there is no path to get our mesh into the served 3D tooling at
all). Ptex (the Blender integration was abandoned unmerged around 2015). OptCuts (a published
baseline clocks it at 35+ hours; we have 287,170 faces). Vertex colours are on the shelf as a
fallback — roughly 143.6K vertices against ~935K currently-addressed texels, two orders below a
packed 4096², but viable *because* we render stills rather than shipping a real-time asset.

---

## PART 3 — WHAT WE WANT FROM YOU

**Q1 — Is the causal chain sound?** We claim 9,166 islands at a 102-texel median, with 17.8% of
area within one texel of an edge, produces the visible blotchiness. Is that mechanically plausible
at these magnitudes? What would you *expect* a render off such an atlas to look like, and does
"chunky, hard-edged colour breakup with scattered wrong-material patches" match? **If you think the
atlas is a real problem but NOT the one producing this specific appearance, that is the single most
valuable thing you could tell us.**

**Q2 — What route have we not enumerated?** We listed what we closed. What is missing from the
list entirely?

**Q3 — Is A-before-B the right order?** Practitioner canon says retopologise first. We deferred it
to protect an accepted silhouette. What does deferring cost us if the mesh is the real answer, and
would you reverse the order?

**Q4 — Look hard at the projection stage itself.** Even granting a perfect atlas: per-texel
raycast, hand-rolled 2×2 bilinear from 8 views, `facing^6` weighting, and a two-band composite
taking all high-frequency detail from a single winner-take-all view. We have measured this stage a
great deal but never asked an outsider whether the **architecture** is right. Winner-take-all high
frequency means every ownership boundary is a hard colour discontinuity in the detail band — is
that defensible? What would you do differently?

**Q5 — Adjacent domains.** Film/VFX and photogrammetry solve texture-from-photographs without
real-time constraints, which is our situation. Given we render eight stills in Blender and never
ship the mesh, is there an approach from those domains that games-oriented advice would not surface?

**Q6 — Where does this plan break?** Name the phase you expect to fail and the reason.

**Calibration.** Please nominate **one specific, checkable claim** — a documented parameter default,
an algorithm's stated behaviour, a paper's reported number — that we can verify at primary source
before acting on anything else you say. We do this with every consult channel: it is how a source
earns weight rather than being given it. We will tell you the result either way.
