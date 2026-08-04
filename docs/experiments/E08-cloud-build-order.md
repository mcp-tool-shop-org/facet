# BUILD ORDER — E08 reproduction anchor on Comfy Cloud

**For the Comfy-side agent. Relayed by the Director.**

This is a **reproduction test**, not a creative render. The output is compared byte-for-byte
against a known local result, so **every value below is load-bearing and nothing may be
"improved."** A better-looking image is a failed test.

---

## THE 8 STANDING RULES — these govern everything below

1. **New empty tabs only.** Build in a brand-new empty workflow.
2. **Out of tabs = STOP.** Do not close or reuse an existing tab to make room.
3. **Never delete or rewire a node in a graph you did not create.** There is a stock
   "Unsaved Workflow (2)" open with 10 nodes and a Model Library dialog may be open — leave both
   alone.
4. **Named models are NOT substitutable.** Every filename below is exact. If one is missing, STOP
   and report — do not pick "the closest one."
5. **Exact names, saved.** Save the workflow with the exact name given.
6. **Build only what is listed.** No upscalers, no refiners, no preview nodes, no extra LoRAs, no
   prompt edits.
7. **Report deviations at the TOP of your reply**, before anything else, not buried at the end.
8. **Halt conditions are explicit** — see the last section. Halting is a success, not a failure.

---

## Context you need (one paragraph)

A local RTX 5090 produced this exact image and we recorded its SHA-256. The local rig can no
longer run the job — the staged model set is ~31 GB against a 31.2 GB safety ceiling. We are
moving to Cloud, and before trusting any Cloud number we re-run the **identical** configuration
to see whether Cloud reproduces the local result. That is the whole purpose. **Any deviation in
any parameter voids the test.**

## Save the workflow as

```
E08-anchor-N11
```

---

## The graph — 15 nodes

### Loaders

| # | node | inputs |
|---|---|---|
| 1 | `UNETLoader` | `unet_name` = `qwen_image_fp8_e4m3fn.safetensors` · `weight_dtype` = `default` |
| 2 | `CLIPLoader` | `clip_name` = `qwen_2.5_vl_7b_fp8_scaled.safetensors` · `type` = `qwen_image` · `device` = `default` |
| 3 | `VAELoader` | `vae_name` = `qwen_image_vae.safetensors` |
| 4 | `ControlNetLoader` | `control_net_name` = `Qwen-Image-InstantX-ControlNet-Union.safetensors` |

### LoRA and model sampling

| # | node | inputs |
|---|---|---|
| 5 | `LoraLoaderModelOnly` | `model` ← **node 1** · `lora_name` = `mikeyfrilot__saltroad-lora__saltroad_style_v2_lowlr_000001500.safetensors` · `strength_model` = `0.75` |
| 6 | `ModelSamplingAuraFlow` | `model` ← **node 5** · `shift` = `3.1` |

> **Order is load-bearing:** UNET → LoRA → ModelSamplingAuraFlow. Not UNET → ModelSampling → LoRA.
> **`LoraLoaderModelOnly` is deliberate** — model-only, no CLIP branch. The text encoder was
> frozen during this LoRA's training. Do **not** swap in the regular `LoraLoader`.

### Prompts

| # | node | inputs |
|---|---|---|
| 7 | `CLIPTextEncode` **(POSITIVE)** | `clip` ← node 2 · text below |
| 8 | `CLIPTextEncode` **(NEGATIVE)** | `clip` ← node 2 · text below |

**POSITIVE — paste verbatim, no reordering, no additions:**

```
a burly bald warrior with a long red beard, dark green knitted sleeveless tunic, polished gold pauldrons, gold necklace, dark red layered cloth skirt with a leather belt, brown leather bracers, a gold plate on each outer forearm, gold knee plates, heavy dark boots, holding a massive greatsword, plain grey background, visible brushstrokes, painterly worked surface
```

**NEGATIVE — paste verbatim:**

```
braided belt, plaited belt, woven belt, rope belt, shoulder strap, chest strap, baldric, bandolier, watermark, text, logo, blurry, photo, deformed
```

### Images — both already uploaded to the input folder

| # | node | inputs |
|---|---|---|
| 9 | `LoadImage` **(RENDER)** | `image` = `420a567392d393065b461676cbef04899d7570440ba01f72d7d4729e45de0e1d.png` |
| 10 | `LoadImage` **(CONTROL)** | `image` = `29afb4bdefc04112111d347a52d4c7833be1a703e2dda49dd180ec346bad77b6.png` |

> These are content-addressed names already present in the input folder. **Do not re-upload, do
> not rename.** If the combo box does not list them, type/inject the name anyway — it executes
> fine even when the dropdown does not show it.

### ⚠ The one wiring mistake that silently ruins this

**The RENDER (node 9) becomes the LATENT. The CONTROL (node 10) goes to the ControlNet.**
They are not interchangeable and swapping them produces a plausible-looking image that is a
completely invalid test.

| # | node | inputs |
|---|---|---|
| 11 | `ControlNetApplyAdvanced` | `positive` ← node 7 · `negative` ← node 8 · `control_net` ← node 4 · `image` ← **node 10 (CONTROL)** · `vae` ← node 3 · `strength` = `0.9` · `start_percent` = `0.0` · `end_percent` = `1.0` |
| 12 | `VAEEncode` | `pixels` ← **node 9 (RENDER)** · `vae` ← node 3 |

### Sampler and output

| # | node | inputs |
|---|---|---|
| 13 | `KSampler` | `model` ← node 6 · `seed` = `770700` · `control_after_generate` = **`fixed`** · `steps` = `20` · `cfg` = `2.5` · `sampler_name` = `euler` · `scheduler` = `simple` · `positive` ← **node 11, output 0** · `negative` ← **node 11, output 1** · `latent_image` ← node 12 · `denoise` = `0.92` |
| 14 | `VAEDecode` | `samples` ← node 13 · `vae` ← node 3 |
| 15 | `SaveImage` | `images` ← node 14 · `filename_prefix` = `restylize` |

> **`ControlNetApplyAdvanced` has TWO outputs.** Output 0 → KSampler `positive`, output 1 →
> KSampler `negative`. Wiring output 0 to both is a common slip and breaks the run.
>
> **`control_after_generate` MUST be `fixed`.** On `randomize`/`increment` the seed changes and
> reproduction becomes impossible. This alone would void the test.
>
> **Batch count = 1.** One image.

---

## Known issue you may hit, and what we already saw

The LoRA was imported minutes ago through Model Library → Import from a **private** HF repo. The
dialog reported *"Model successfully imported… loras"* and resolved the name to exactly the
string in node 5. **But it does not yet appear** in `/api/experiment/models/loras`, in the
`Imported` tab list (badge shows 1, list renders empty), or in any node combo.

This partially matches a documented staleness gotcha — imported models are missing from combos
until refreshed, while still executing fine. **We do not know whether the underlying download
completed.** So:

- If the LoRA name is selectable or injectable and the run executes → good, proceed.
- If the run **errors** on the LoRA → that is the answer we need. **STOP and report the exact
  error text.** Do not substitute another LoRA. Do not re-import without saying so.

## What to report back

1. **Deviations first**, at the top — anything you could not set exactly as specified.
2. The **`prompt_id`** of the run.
3. Whether the LoRA node accepted the name, and how (combo listed it / injected it / errored).
4. The output image.
5. Any node where the UI silently changed a value you set (especially `seed`,
   `control_after_generate`, `denoise`, `cfg`, `shift`, `strength`).

## HALT CONDITIONS — stop and report, do not work around

- Any of the five named model files is missing or not selectable → **STOP.**
- The LoRA errors at execution → **STOP**, report the error verbatim.
- You would need to modify, close, or reuse an existing tab or graph → **STOP.**
- Either `LoadImage` name is rejected and cannot be injected → **STOP.**
- A required node class does not exist on this instance → **STOP**, name it. Do not find an
  equivalent.
- The run exceeds the 30-minute workflow cap → **STOP**, report.

**Do not tune anything to make the output look better.** If the image comes back ugly, wrong, or
obviously off-style, that is potentially the correct and useful result. Report it as-is.
