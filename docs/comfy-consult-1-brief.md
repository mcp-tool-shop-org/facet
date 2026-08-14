# Comfy Agent consult #1 — dark-speck artifacts in Qwen ControlNet twins (brief)

**From:** the facet advisor seat, 2026-08-14 · **Relay:** the Director carries this brief
to the Comfy Agent and returns its answer · **Trigger:** the Director ruled a dark-speck
class unacceptable on the performer's accepted texture at his zoom · **Answer:**
[comfy-consult-1.md](comfy-consult-1.md), with the facet-side calibration appended.

---

## Context — two paragraphs, then the measurements

facet textures a mesh by projecting generated "twin" images onto it from N views: a clay
render of the mesh is canny-locked through ControlNet and restylized by Qwen-Image into
the ruled register, and the paint is projected into a 4096 atlas. The subject in hand is
a wooden-mannequin performer in an approved register (unglazed terracotta, matte, soft
studio light, NO LoRA). The final texture carries scattered small dark brown-to-black
speckles (2–6 px dots at 352×1024 frame scale, reading as sharp dark triangles at zoom)
on limbs and torso.

We have already attributed the class to the GENERATION stage, measured (table below): the
control images are speck-free, every generated twin carries dark dots on the figure, and
the dots bake into the atlas and persist under flat light. Re-projecting from more views
cannot remove it — every added twin adds the class. We need the generation-side
mechanism and the levers, ranked.

## The exact recipe (all on Comfy Cloud, all resolving by these names)

`qwen_image_fp8_e4m3fn.safetensors` · `qwen_2.5_vl_7b_fp8_scaled.safetensors` ·
`qwen_image_vae.safetensors` · `Qwen-Image-InstantX-ControlNet-Union.safetensors`
seed 770700 (same across all views) · steps 20 · cfg 2.5 · denoise 0.92 (img2img from
the clay render) · cn_strength 0.9 · shift 3.1 · euler / simple · 352×1024 · LoRA NONE ·
pinned positive register + identity terms; pinned negative, byte-identical across views.

## Measured already — do not re-derive

| measurement | result |
|---|---|
| control renders (clay + canny) | **0 near-black px** in sampled crops — the control carries no speck features; the model invents the dots |
| the twins | dark dots ON the figure in every sampled view — 127 px (torso crop) / 263 px (legs crop) at max(RGB)<60, cores ~(70–95, 40–60, 15–40) |
| the baked atlas | specks persist under FLAT light (= texture truth), pixel values matching the twin dots at the same locations (5 of 6 sampled) |
| across assets | the 2-view and 8-view textures carry the class at near-identical values — it predates re-projection and survives it because every twin carries it |
| out of the agent's scope | ~1 in 6 sampled specks is pure-black (11,9,8) where the view's twin is mid-tone — a candidate pipeline-local mechanism facet runs down itself |
| subject scale | figure ~284×850 px in the 352×1024 frame; the register is smooth matte terracotta, so few-px dark dots are highly visible |

## Hard constraints

- **No licence change** — the stack stays commercially clean end to end.
- **The register is Director-ruled.** Levers are CANDIDATES: facet measures any recipe
  change under its own spec before adoption. Nothing gets applied ad hoc.
- **Named models are not substitutable** without saying so explicitly at the top.
- Venue is Comfy Cloud; GPU-hours measured at ~$0.018/job at this recipe, so A/B rounds
  are affordable — rank levers by expected effect, not by cost.

## The questions, ranked

**Q1 — mechanism.** Is small dark speckling on smooth matte subjects a KNOWN artifact
class for Qwen-Image at fp8_e4m3fn (weights and/or the fp8-scaled text encoder)?
Candidates to separate: fp8 quantization noise · VAE decode dot artifacts ·
sampler/scheduler (euler/simple at 20 steps) · ControlNet-Union at strength 0.9 ·
img2img at denoise 0.92 from a near-uniform grey source. Which does the catalog /
known-issues knowledge point at, and what would each predict about dot size/placement?

**Q2 — the levers, ranked** by expected effect on THIS class, each with its
register-drift risk stated: bf16 base weights on cloud · steps · cfg · scheduler ·
denoise · VAE variant · negative-prompt speckle terms (real lever or superstition for
this model family?). For each: does it remove the class or merely thin it?

**Q3 — despeckle-after.** A deterministic, commercially-clean, batchable Comfy-side
small-defect cleanup that runs on the twins BEFORE projection — small-blob detection +
targeted inpaint, median-class filtering, whatever the catalog actually has. Exact node
names, saved, with the wiring shape. If nothing fits, say so plainly.

**Q4 — what seed would discriminate.** Same seed across all views today. Under the Q1
mechanism: would re-rolling seeds MOVE the dots (seed-bound) or leave them
(content/quantization-bound)? What does each outcome rule out?

## Calibration and the standing rules

Include **one cheap checkable claim** in the answer — facet verifies it before acting on
anything expensive, per this channel's standing practice. The 8 standing rules apply:
new empty tabs only · out of tabs = STOP · never delete/rewire a node in a graph you did
not create · named models are NOT substitutable · exact names, saved · build only what is
listed · report deviations at the TOP · explicit halt conditions.
