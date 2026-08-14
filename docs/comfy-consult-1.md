# Comfy Agent consult #1 — the answer, and the facet-side calibration

**Relayed by the Director, 2026-08-14**, answering
[comfy-consult-1-brief.md](comfy-consult-1-brief.md). The agent built and ran nothing —
a consult, as briefed. The facet calibration of its checkable claim is appended at the
bottom; read it before acting on the Q3 construction.

---

## Deviations / disagreements — at the top

1. **`MedianFilterImage` is the wrong shape for the Q3 despeckle as-is.** It exposes only
   `images` + `size` (a square kernel). A median at the radius needed to kill a 6 px dot
   (`size` ≥ 5–7) will visibly soften the smooth-matte terracotta register — a global
   filter with no blob gate. It *thins* the class everywhere and drifts the register.
   Flagged rather than endorsed.

2. **No true small-blob-detect + targeted-inpaint node exists in this catalog.** Searched
   by intent and browsed the whole `Image-Filters/*` tree. There is no "detect dark blobs
   under N px → mask → inpaint only those" node. The honest Q3 answer is a
   **frequency-separation** construction, not an off-the-shelf despeckler.

3. **Nothing was built, saved, or run.** A/B rounds are facet's to run under facet's
   spec. All node names below were confirmed against the live catalog in the agent's
   session.

## Q1 — Mechanism, ranked by fit to the measurements

1. **img2img at denoise 0.92 from a near-uniform grey clay source — primary suspect.** A
   denoise this high on a low-variance init gives the sampler almost no image-space
   anchor, so it hallucinates high-frequency structure to satisfy the register prior —
   and "unglazed terracotta / matte / clay" *contains* fine dark mineral flecks. The
   model is rendering plausible terracotta speckle, not failing. Predicts: dots
   content-locked to register and seed, clustering on large smooth fields (matches the
   127/263 counts), chromatic brown (matches the cores). The one-in-six *pure-black*
   specks do **not** fit this — correctly carved out as facet's pipeline-local question.
2. **ControlNet-Union at 0.9 — contributing, not causal.** Canny locks edges and leaves
   interior fill free; at 0.9 it *hardens* invented interior texture into sharp
   repeatable dots. Lowering `cn_strength` softens dot edges but does not remove the
   class (the control never carried the specks).
3. **fp8_e4m3fn quantization — minor, wrong signature.** Quant error is low-amplitude
   and spatially diffuse, not discrete chromatic dots. The fp8→bf16 swap is worth
   running *as a discriminator*, not as the expected fix.
4. **VAE decode artifacts — unlikely.** VAE dot artifacts are typically neutral and
   tile-periodic; these are chromatic and content-placed.
5. **euler/simple @ 20 steps — least likely as a driver.** Adequately converged at
   cfg 2.5; may sharpen what exists, does not manufacture dots.

**Bottom line: the register prior rendered under an over-denoised, near-uniform init,
hardened by strong ControlNet — a content/denoise class, not a quantization or VAE
class.**

## Q2 — Levers, ranked

| # | lever | effect on the class | register-drift risk |
|---|---|---|---|
| 1 | **denoise 0.92 → 0.70–0.78** | removes/strongly thins — starves the mechanism directly; the single highest-leverage knob | **medium** — less restylization; sweep 0.92/0.80/0.72 |
| 2 | **cn_strength 0.9 → 0.6–0.7** | thins (softens dot hardening); pair with #1 | low–medium at canny edges |
| 3 | **fp8 → bf16 base weights** (named-model swap, non-substitutable) | discriminates + possibly thins; if unchanged, quantization is exonerated | low on register; VRAM/latency cost |
| 4 | steps 20 → 28–32 | thins slightly at best | negligible |
| 5 | scheduler simple → `sgm_uniform` (or `karras`) | marginal | negligible |
| 6 | cfg 2.5 → 2.0 | marginal thin | low |
| 7 | VAE variant | no expected effect on this signature | — |
| 8 | negative-prompt speckle terms | **effectively superstition for this family** — weak response to abstract texture negatives; will not reliably remove a content-plausible fleck | low, because low effect |

**Recommended first A/B:** the denoise sweep at fixed everything else; then
cn_strength 0.65 if residual; the bf16 swap reserved as the quant discriminator.

## Q3 — Despeckle-after (the deterministic fallback)

No blob-detect+inpaint node exists. What exists, per the agent (all in
`Image-Filters/image`, pack `ComfyUI-Image-Filters`): `MedianFilterImage` (global —
flagged), `BilateralFilterImage` (edge-preserving, still global), `GuidedFilterImage`,
and **`FrequencySeparate` + `FrequencyCombine`** — separate the twin into low + high
frequency, median/bilateral **only the high band** (where 2–6 px dots live), recombine.
Deterministic, licence-clean, batchable, runs on twins before projection. It removes
dots at the cost of high-frequency micro-detail — acceptable on smooth matte terracotta
*if measured under facet's spec*; it cleans up, it does not diagnose. ⚠ **See the
calibration below before wiring this** — the agent's sketch mis-drew `FrequencySeparate`'s
interface.

## Q4 — What the seed A/B discriminates

- **Dots MOVE on re-roll** (predicted): rules out spatially-fixed mechanisms (VAE grid,
  pipeline stamps, control-locked features); confirms a seed-bound content class — and
  cross-seed averaging across views becomes a real mitigation lever.
- **Dots STAY**: rules out the denoise-hallucination mechanism; points at input- or
  quantization-bound causes — the bf16 swap becomes the decisive test.

The agent ranks this the single most informative bit available, ahead of any spend on
sweeps. Sequence proposed: seed A/B → denoise sweep → +cn 0.65 if residual → bf16 as
discriminator; frequency-separation held as the net.

---

## ⚖ Calibration at the facet seat, 2026-08-14 — the checkable claim, verified live

The agent's claim: *`FrequencySeparate` and `FrequencyCombine` both exist in category
`Image-Filters/image`, each outputting IMAGE; `MedianFilterImage` in the same category
takes exactly `images` (IMAGE) and `size` (INT).*

**Verified against the live catalog via `get_node`, all four names resolving:**

| node | category | verdict |
|---|---|---|
| `FrequencySeparate` | `Image-Filters/image`, pack `ComfyUI-Image-Filters` | **exists, one IMAGE output** — ⚠ see below |
| `FrequencyCombine` | same | **exists** — inputs `high_frequency` + `low_frequency` + `mode` (subtract/divide) + `eps`, one IMAGE output |
| `MedianFilterImage` | same | **exists, inputs exactly `images` (IMAGE) + `size` (INT, 1–1023)** — claim exact |
| `BilateralFilterImage` | same | exists (fallback confirmed): `images` + `size` + `sigma_color` + `sigma_space` |

**One interface imprecision, found by the calibration and material to Q3:**
`FrequencySeparate` does **not** emit low and high bands — it takes **two IMAGE inputs**
(`original` AND `low_frequency`) and outputs the high band alone. The caller must build
the low band first (a blur of the original), so the real wiring is:

```
[twin] ─┬────────────────────────────► FrequencySeparate.original
        └► [blur node → low band] ──┬► FrequencySeparate.low_frequency
                                    │        │ (high band out)
                                    │        ▼
                                    │   MedianFilterImage (size 3–5)
                                    │        │
                                    └──► FrequencyCombine.low_frequency
                                             ▲ high_frequency
                                             ▼
                                     [cleaned twin → projection]
```

One prerequisite node (the blur) that the agent's sketch omitted. The construction
stands; the claim's existence/category/shape clauses all verified. Channel scorecard:
deviations honestly led, one interface detail wrong in a diagram, caught by the
calibration ritual doing its job.
