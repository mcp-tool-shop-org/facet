# Step 0b — the cloud anchor: prediction, recorded before the run

**NOT BLIND.** I have the full E08 record, Amendments 17–19 and my own E3 report in context. The
outcome branches were pre-registered by the advisor in the kickoff; what follows is *my*
prediction of which one fires, recorded before the LoRA name exists.

## The round-trip check is unavailable, and the obvious substitute is invalid

The advisor asked for a SHA-256 round-trip of the uploaded render *if a download path exists*.
It does not: `get_output` and `use_previous_output` are both keyed on `prompt_id` and fetch a
completed job's **outputs**. There is no input-folder read in the toolset. Per the ruling I am
not building one.

**And the obvious substitute would not work even if I spent a job on it.** A `LoadImage →
SaveImage` round-trip re-encodes the PNG at `SaveImage` by construction, so the returned bytes
would differ from the original whatever the truth is. That check cannot come back "identical"
even when nothing is wrong — it manufactures its own positive. Not run.

## Correcting my own flag: a PNG re-encode does not break reproduction

I recorded the naming mismatch (`cac49be7…` → `420a5673…`) as possibly meaning "the cloud
re-encodes, so the latent differs and byte-reproduction was never available." **That inference
was wrong and I am correcting it before it is used.**

**PNG is lossless.** A re-encode with a different compression level, filter choice or chunk order
changes the *file bytes* — and therefore the file's SHA-256 — while leaving every *pixel value*
identical. `LoadImage` decodes to a pixel tensor, so `VAEEncode` receives the same numbers either
way. A re-encode alone cannot move the latent.

The local path is the same shape: `restylize_views.py` uploads the raw file and feeds it through
`LoadImage` too, so both sides decode the same original PNG.

What *would* move the latent is a change to the pixels themselves — a colourspace conversion, an
alpha channel gained or dropped, a resize. Those are real but are a narrower and less likely
class than "re-encode," and none of them are evidenced. **So the naming mismatch is weak evidence
of anything, and 0b's ΔE branch is not the "byte-reproduction was impossible" path I implied.**

## Prediction

| branch | my estimate |
|---|---|
| sha256 == `d0220e24…` — clean pass | **~25%** |
| sha differs, whole-figure median ΔE ≤ 1.07 — accept, boundary recorded | **~70%** |
| ΔE > 1.07 — HALT | **~5%** |

**Reasoning for branch 2 as the mode.** Different architecture (RTX 6000 Pro against this rig's
5090), different kernels for fp8 weights manual-cast to bfloat16, twenty sampler steps for small
numeric differences to compound. `comfy-cloud-run.md` records cloud as seed-identical to the 5090
— but that was validated 2026-06-26 on a *generation* pipeline, and this is img2img with a
ControlNet, which is more operations and more surface for a kernel to differ. I would not bet
against exact reproduction, but I would not expect it.

**On branch 1.** It needs bit-identical arithmetic across two architectures. Possible if both
dispatch the same deterministic kernels, which is why I do not put it lower than a quarter.

**On branch 3, and the reason it is not simply "hardware drift."** The likeliest route to
ΔE > 1.07 is **not** the GPU — it is the LoRA silently failing to load, which would strip the
style from the whole figure and move ΔE far past 1.07. That is exactly the failure the advisor
named in asking for the measured `lora_name` rather than my predicted one. So if branch 3 fires,
**the first hypothesis to check is the LoRA, not the hardware** — and the halt is still honoured
either way; diagnosing it is not re-running it.

A secondary route to branch 3 would be a pixel-level input difference (colourspace or alpha), per
the correction above. Distinguishing those two is a diagnosis for after the halt, not a reason to
tune anything before it.

## What I run, the moment the string lands

The dry-run-validated graph with `lora_name` replaced by the string read off the imported card —
**never my predicted one.** Seed 770700, steps 20, cfg 2.5, euler/simple, denoise 0.92,
lora_w 0.75, cn 0.9 start 0.0 end 1.0, shift 3.1; render
`420a5673…png`, control `29afb4bd…png`. Every value from `N11/w3clay_0_gen.json`.
