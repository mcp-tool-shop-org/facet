# E40 — the blend-stage study-swarm (swarm 2)

**Dispatched 2026-08-16** at the Director's word, after [E40](../experiments/E40-three-class-arms-kickoff.md)
closed: *"launch a study swarm to search message boards and the like for solutions."* Five agents,
practitioner-weighted, every citation resolved at primary source or listed UNRESOLVED.

**This swarm's questions were sharper than the first one's because E40 had already located the
defect.** Swarm 1 asked *where is the bleeding coming from*; this one asks *given that it is in
the blend, and given that our views are never independent, what do people do*.

---

## ⚠ Advisor correction, made at the primary source before anything was folded

**Two agents contradicted each other on the single most load-bearing fact in the swarm**, and it
governs the lever the Director is most interested in. The advisor fetched
`src/aliceVision/mesh/Texturing.cpp` from `develop` and read it rather than choosing a report.

Agent 1 wrote: *"`multiBandNbContrib = {1, 5, 10, 0}`: only ONE view contributes the lowest
frequency band — the coarse colour (i.e. material identity) is single-sourced, not averaged."*
**That is inverted.** The code, verbatim at line 405:

> *"Ensure that contribution levels do not contain 0 and are sorted (as each frequency band
> contributes to lower bands)."*

`{1,5,10,0}` has its zero erased → `{1,5,10}`, is sorted, then `std::partial_sum` (line 420) makes
it **`{1, 6, 16}`**. Cameras are sorted by score descending (602) and `nbContribMax` is the
back element, **16** (606). **So the finest band takes 1 camera and the coarsest takes up to 16.**

**RULED: low frequency IS averaged over many views; high frequency comes from one.** Swarm 1's
reading was right, agent 1's clause is wrong, and had it been folded uncorrected the Director
would have been told the opposite of the truth about the lever he had already called out as
worth building. **This is why an external citation is resolved at its source and not adopted from
a report** — including a report this seat commissioned.

**Agent 1's other clause in the same finding is correct and sharp, and survives:** the score is
`area * verticesSupport` — **pure geometry, no photometric term** — so *two agreeing wrong views
both score high*. That is exactly our failure mode, in the reference implementation.

---

## The convergence: NO TOOL BLURS A WHOLE ATLAS

Three agents arrived at this independently and it is the swarm's central result. There are
exactly three strategies in the field, and **our `gaussian_blur_σ16` over a 4096² atlas with
~14,000 islands is the case all three exist to avoid.**

**1. Filter in SOURCE-IMAGE space and write per-triangle — AliceVision.** Verified at source by
the advisor: `Texturing.cpp:663` builds the Laplacian pyramid on **`camImg`, the camera image**,
never on the atlas. Per-triangle texels then sample `pyramidL[band]` at the *source-image*
coordinate and accumulate into per-band atlas buffers.
> **Implication.** The frequency split happens where **adjacency is real**. The atlas only ever
> receives per-triangle writes. Our split happens in the one space where adjacency is a lie.

**2. Confine correction to a narrow seam band — MVS-Texturing.**
`libs/tex/local_seam_leveling.cpp:18` is `#define STRIP_SIZE 20`, commented *"Only alter a small
strip of texture patches originating from input images."* Global levelling runs on **mesh
vertices/edges**; Poisson only inside the strip. Flags `--skip_global_seam_leveling`,
`--skip_local_seam_leveling`. (https://github.com/nmoehrle/mvs-texturing)

**3. Replace the flat kernel with a chart/surface-aware operator — and there is runnable code.**
Prada, Kazhdan, Chuang & Hoppe, *Gradient-domain processing within a texture atlas*, SIGGRAPH
2018 (https://hhoppe.com/proj/atlasfilter/, code at
https://github.com/mkazhdan/TextureSignalProcessing). Named tools: **`TextureFiltering`**
(`--interpolation`, `--modulation`), **`SeamStitcher`**, **`TextureDilation`** (*"dilates the
texture by sampling across the chart seam"*), **`TextureMasking`**. The kernel is replaced by a
multigrid solve on a **texel graph whose topology follows the surface**. Its stitching mask
assigns texels the same colour *"if and only if they are covered by the same chart."*

**Corroborating, from the DCC side:** Adobe's PM states outright that Substance's blur *"has
effect on the 2D view (so only the UV islands), and this is what creates the seams"* — a
12-year-old shipped tool **has no chart-respecting atlas blur**, and a 3D blur is only now *"a
priority for the team."* The paid third-party fix (Action Dawg's *Substance 3D Blur 2.0*) works by
**weighting the kernel by 3D distance through a world-position map** — the direct analogue of what
our σ=16 needs. NVIDIA hit both failure modes in GPU Gems 3 Ch. 14 and fixed them with a
**stretch-correction texture** plus a per-chart partition of unity.

---

## Camera geometry: our set is an inherited default, and it looks nowhere but sideways

**Our 8+2 is literally SyncMVD's default.** `--camera_azims` defaults to the same eight 45°
steps, and `--no_top_cameras` is `store_true` so the two top cameras are **on by default**
(https://raw.githubusercontent.com/LIU-Yuxin/SyncMVD/main/src/configs.py).
> **Implication. We inherited a default and never derived a set.**

**⚑ Nothing in our rig looks UP.** TEXTure runs 8 views but tilts the whole ring to **+30°
elevation** and adds back-high (+60°) *and* **back-low (−60°)**. Hunyuan3D-2.1 builds a 30-camera
candidate pool including a **±20° tier at weight 0.01** as cheap coverage insurance, and a −90°
bottom view. **Every camera we have is at 0° or +55°** — and a held blade's underside is exactly
the surface that set cannot reach. That is a direct, cheap candidate explanation for E40's
**74.28% never-hit**.

**More views is not the answer, and the numbers say so.** MVPaint's own ablation: FID **35.48
(N=4) → 23.45 (N=8) → 25.71 (N=16)** — *"excessive overlap… leads to over-smoothed or blurry
textures."* Its best config is **N=8 with interleaved elevation ±30°** (FID 20.89), *the same
count as ours with the ring broken*. Make-A-Texture plateaus at 6 views (FID 112.14 → 112.18 from
6 → 8), placed on a **Fibonacci lattice**, not a ring. And a practitioner with >1,000 contributing
cameras got *blurry* texture; the vendor fix was **cutting to 100–200**.
> ⚠ **Contested, and the tension is the useful part:** those are **global FID** numbers, and FID
> cannot see a 74%-unpainted blade. StableGen ships the opposite policy — `coverage_target`
> **0.95**, *"stop adding cameras when this fraction of surface area is visible"*, `max_auto_cameras`
> **12**. **Our 74.28% is a coverage number, so StableGen's unit is the one that matches our
> defect.**

**Metashape has the concept we lack: an EFFECTIVE view count.** *Reduce Overlap* selects a minimal
set *"such that each point of rough model is observed from at least N significantly different
angles"* — and **"cameras from single direction count as one."** That is precisely our
100%-within-90° finding, named and operationalised by a shipping tool.

**And the trade's minimum-views rule is not about independence at all:** every surface in *"at
least 2–3 images, taken one straight and two from a slight (10°–15°) angle"* — the safety comes
from **having one near-normal view**, not from independent ones. RealityScan: *"Do not change a
view point more than 30 degrees."* **Ours are 45° apart.**

---

## Material identity: the ID map is a lossy carrier, and USD has the grip answer

**⚠ An ID map read with filtering is NOT a hard boundary**, and this is our defect re-entering
through the fix. Adobe Community, 2026-07-28: an exported ID map is *"pixel-perfect and contains
no bleeding"*, yet Color Selection samples with filtering/wrapping so *"the colour from the
opposite edge bleeds into the generated mask."* Bake, padding and viewport settings did not fix
it. The same failure appears in ComfyUI's Inspire-Pack *Regional Conditioning By Color Mask*,
where some hex codes match and others silently do not (issue #171, unanswered).
> **Implication, and it is a design rule rather than a finding: prefer N binary masks rendered at
> target resolution with NEAREST sampling over one colour-coded image plus a hex lookup.**

**The published version of our idea exists and reports our exact obstacle.** TexPro
(arXiv:2410.15891v2) renders a per-material mask per view directly from the renderer — then finds
*"the object geometry in the images generated by Stable Diffusion is not well aligned with the
rendered images"*, so it transfers the mask onto the generated image with Matcher. **It does not
solve cross-view identity — it assigns each material part to its single most-visible view.**
Anyone claiming per-material consistency across 8 views should be asked how; the published work
declined to.

**A shipping tool already does per-material regional prompting from a 3D mask:** Texturaizer's
*Segment Prompts* panel — `Segment Type = Object / Families / Materials / Collections`, per-segment
Mask Expand / Mask Blur / Conditioning Strength, *"this prompt will replace any existing text
prompt within the boundary of that segment."* ⚖ ComfyUI node pack **GPL-3.0**; the Blender addon
is paid and its terms are **UNRESOLVED**. Its own docs warn segment IDs shift when objects change.

**⚑ THE GRIP HAS A MACHINE ANSWER, and it is a standard we already use.** USD's
**`UsdGeomSubset`** with `familyName == "materialBind"` and `familyType = partition` means *"every
element of the whole geometry appears exactly once in only one of the subsets"*, and
**`UsdGeomSubset::ValidateFamily()`** reports violations of **exclusivity and completeness**.
`unrestricted` is explicitly invalid for materialBind.
> **Implication. A `materialBind` partition plus `ValidateFamily()` is a check that FIRES on an
> unnamed grip** — the canon gap E40 surfaced becomes a gate rather than a thing someone notices.
> The agent searched specifically for a per-character material-manifest practice and **found none
> anywhere**; naming conventions exist and carry no completeness requirement. This is the only
> located mechanism.

⚖ **Licence positions reported as seen, to be verified locally before adoption:** SAMesh wrapper
**MIT** (upstream `gtangg12/samesh` shows **no licence**); StableGen **GPL-3.0**;
ComfyUI-MeshSegmenter **GPL-3.0-or-later**; P3-SAM under a **Tencent community licence void in the
EU, UK and South Korea**; PartField's LICENSE **404s at both paths — UNRESOLVED**.

---

## Two cheap local tests this swarm hands us

**1. Premultiplied alpha.** Iñigo Quílez (https://iquilezles.org/articles/premultipliedalpha/):
filtering non-premultiplied alpha injects a signed colour error `e = x(1-x)(c1·a2 + a1·c2 −
a1·c1 − a2·c2)`, zero at texel centres and **maximal at midpoints**, worst case −c/4. It is
invisible except at alpha transitions — **i.e. exactly at material boundaries.**
> The agent flagged this as one of the two it would test first, and it is nearly free: check
> whether any resample in our projection runs on straight rather than premultiplied alpha.

**2. Whether we average high frequency across views at all.** Metashape's *Mosaic* exists because
*Average* blurs; a practitioner measured Average as **sharper** than a broken Mosaic build, and
Agisoft acknowledged the GPU regression. Our `M + blur(B−M)` may or may not be averaging HF —
reading it as a two-band split says it does not, but that has not been measured.

---

## Coverage gaps, stated

**Reddit and Polycount remain hard-blocked** and were not attempted, per the standing note. Also
unresolved and named in the agents' own lists: Waechter et al. 2014's photo-consistency internals
(Springer auth wall — the `texrecon` flags are resolved, the Mahalanobis detail is **not**
primary-sourced), Metashape's *Reduce Overlap* manual default (the 3–5 figure is a forum post, not
the manual), StableGen's `Discard-Over Angle` default, PartField's licence, and Kazhdan's SIGGRAPH
PDF (fetched at 9.7 MB, no renderer on this rig — findings taken from the project page and code
README, both primary).
