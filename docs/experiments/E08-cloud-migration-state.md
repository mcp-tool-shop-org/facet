# E08 — Step 0 cloud migration: measured state

**Executor session, 2026-08-04.** Everything below is measured or read off a tool response.
Nothing here is a judgement about whether the migration is a good idea — Amendment 18 ruled that.

## 0a. LoRA delivery — RESOLVED, with two corrections to the ruling's premises

**The import list is one file, not two.** All four base models are on Comfy Cloud **by exact
name**, confirmed via `search_models`:

| file | type | cloud |
|---|---|---|
| `qwen_image_fp8_e4m3fn.safetensors` | diffusion_model | present |
| `qwen_2.5_vl_7b_fp8_scaled.safetensors` | text_encoder | present |
| `qwen_image_vae.safetensors` | vae | present |
| `Qwen-Image-InstantX-ControlNet-Union.safetensors` | controlnet | **present** |
| `saltroad_style_v2_lowlr_000001500.safetensors` | lora | **absent — the only import** |

**Correction 1.** `comfy-cloud-run.md` (2026-06-26) records the InstantX ControlNet Union as
still needing an import alongside the LoRA. It is in the catalog now. That memory line is stale;
the freshness rule called it right at ~40 days.

**Correction 2.** Amendment 18 read the plugin's `upload_file` as a possible LoRA path. Its
schema is **`.jpg/.jpeg/.png/.webp/.gif` only** — it cannot carry a `.safetensors`. Combined with
`comfy-cloud-run.md`'s note that the official API has no import endpoint (verified against
`docs.comfy.org/development/cloud/api-reference`), **model import is browser-only regardless of
how the file reaches HF.**

### Delivered to HuggingFace

Director's direction: *"use it through huggingface."*

```
repo    mikeyfrilot/saltroad-lora     PRIVATE
file    saltroad_style_v2_lowlr_000001500.safetensors
bytes   295,144,520
commit  ae98e936960635570f7b85845f18c276f286f678
```

Private, deliberately: the LoRA is the studio's trained visual style. Filename kept identical to
the local one so the imported name is predictable.

The cached HF token turned out to be a **Write** token — not the read-token trap
`comfy-cloud-run.md` gotcha #2 warns about. The upload itself was run by the Director; the
permission classifier blocked it from this session twice.

## 0a-remaining — what is still outstanding, and why it is not mine

1. **A `mikeyfrilot` HF *read* token in Comfy Cloud → Settings → Secrets.** The existing secret is
   for `SaintEloi` (per `comfy-cloud-run.md`), which cannot read a private `mikeyfrilot` repo.
   Entering a token is a credential action and is not something this session does.
2. **Model Library → Import → the HF blob URL → type LoRA.** Browser-only, per correction 2.
3. **Read back the real `lora_name`.** Predicted
   `mikeyfrilot__saltroad-lora__saltroad_style_v2_lowlr_000001500.safetensors` from the
   `<owner>__<repo>__<file>` pattern in `comfy-cloud-run.md`, **but predicted is not measured** —
   the string must be read off the imported card, not assumed.

## The graph is portable — validated, free, no spend

`submit_workflow` with `dry_run: true` returned **`status: "validated"`** for the full
`restylize_views.py` graph rebuilt in API format. Every `class_type` exists on cloud —
`UNETLoader`, `CLIPLoader`, `VAELoader`, `ControlNetLoader`, `LoraLoaderModelOnly`,
`ModelSamplingAuraFlow`, `CLIPTextEncode`, `LoadImage`, `ControlNetApplyAdvanced`, `VAEEncode`,
`KSampler`, `VAEDecode`, `SaveImage` — links are sound and all four base model names resolve.

The **only** warning was the LoRA name not being in the bundled index, which is expected for an
un-imported model and is the browser-combo staleness `comfy-cloud-run.md` gotcha #3 documents as
running fine headless.

## Inputs uploaded, and byte-matched to N11 first

The control image is **byte-identical across N11, BRACER and the local E3 run**, and the render
matches the `input_sha256` in N11's sidecar:

```
c158af80ef76b8ad…   w3clay_0_control.png    N11 == BRACER == ANCHOR
cac49be7d96c35d7…   w3clay_0.png            == N11 sidecar input_sha256
```

Uploaded to the cloud input folder:

```
render   420a567392d393065b461676cbef04899d7570440ba01f72d7d4729e45de0e1d.png
control  29afb4bdefc04112111d347a52d4c7833be1a703e2dda49dd180ec346bad77b6.png
```

**⚠ Flagged unknown, not chased.** `comfy-cloud-run.md` gotcha #8 says the cloud content-addresses
an upload to its SHA-256, but neither returned name equals the local file's SHA-256
(`cac49be7…` → `420a5673…`). Either the cloud hashes something other than the file bytes, or it
re-encodes the image. **If it re-encodes, the latent differs and the anchor cannot reproduce
byte-for-byte.** This does not need resolving before the run: Step 0b's gate already covers it —
a re-encode surfaces as a sha mismatch and is then adjudicated on ΔE against N11's own 1.07
no-response floor. Recording it so a mismatch is not later attributed to the wrong cause.

## Ready to run the moment the LoRA name exists

Graph, seed 770700, steps 20, cfg 2.5, euler/simple, denoise 0.92, lora_w 0.75, cn 0.9
start 0.0 end 1.0, shift 3.1 — every value from `N11/w3clay_0_gen.json`. Target sha256
`d0220e244d5ad2015639153188c488e3f3d317933dbd54eb439724fe1f57f93d`.
