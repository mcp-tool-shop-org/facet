# E35 — anchored pilot sequence, executor pre-registration

**Registered 2026-08-14 BEFORE A1 was submitted.** Standing at 38 of 60. The sequence
spends ≤ 5. A3's full bands are appended to this file after A2 lands, per the dispatch —
they are the ones that carry the chroma-split column, and they are written only once the
reduced question is known.

---

## ⚠ Enumerated before A1: the template schema's slot defaults are MISALIGNED

`get_template_schema image_qwen_image_edit_2509` returns twelve slots whose `default`
values do not belong to their addresses:

| address | reported default | what that value actually is |
|---|---|---|
| `433.image` | `"Replace the cat with a dalmatian…"` | the **prompt** |
| `433.prompt` | `"qwen_image_edit_2509_fp8_e4m3fn.safetensors"` | the **unet name** |
| `433.lora_name` | `"qwen_2.5_vl_7b_fp8_scaled.safetensors"` | the **clip name** |
| `433.prompt_1` | `"qwen_image_vae.safetensors"` | the **vae name** |
| `433.seed_1` | `true` | the **turbo boolean** |
| `433.unet_name_1` | `"…Lightning-4steps-V1.0-bf16.safetensors"` | the **lightning lora** |
| `433.clip_name_1` | `"randomize"` | the seed's **control_after_generate** |

The shift is systematic — the reported defaults are the subgraph's `proxyWidgets` list read
against the wrong slot order. **Consequence for A2, registered now rather than discovered
after a black frame: a named `slot_override` may not land on the widget its name says.**
A2 therefore verifies its two deltas landed by reading the returned image, and if a
`slot_override` misfires, that is a **mechanical** defect under the one-repeat clause, not a
content result.

**A1 is unaffected: it passes no overrides at all.** That is the point of an anchor.

---

## A1 — the anchor. `run_template image_qwen_image_edit_2509`, nothing overridden

The question is not about our subject. It is: **does the served graph produce an image.**

- **A1-P1 — it produces a non-degenerate image.** Band: **> 1000 unique RGB colours**, and
  not a single-colour frame. *(The two pilot jobs returned exactly 1.)*
- **A1-P2 — the frame is one of Kontext's preferred shapes**, because
  `FluxKontextImageScale` is in the path and the template's own input image feeds it.
  Registered as a **prediction about the mechanism I am about to blame**: if A1 comes back
  at some shape *outside* that set, my leading candidate for the pilot's black frame is
  weakened before A3 is designed.
- **A1-P3 — it runs turbo by default**: 4 steps, cfg 1.0, Lightning LoRA, because
  `PrimitiveBoolean` 443 defaults `true`. Not directly observable in the output, but it sets
  what A2 inherits and is stated so A2's inheritance is not silent.
- **My odds it produces an image: 0.85.** If it does not, the dispatch's own halt applies —
  the failure is platform-side, not ours, and the sequence stops.

## A2 — the template's graph + exactly two deltas

Clay via `image1`, the v-next prompt. **`FluxKontextImageScale` stays and is allowed to
resize.** Turbo default untouched.

- **A2-P1 — it produces a non-degenerate image**, band **> 1000 unique colours**. Odds
  **0.8**, conditional on A1 producing one.
- **A2-P2 — the returned frame is NOT 352×1024.** The scale node will move our
  352×1024 clay to a Kontext shape. This is the whole point of A2 and it is why A2 cannot
  be measured against the recorded twin: **the pale, census and register instruments all
  assume our frame and its mask.** A2 is a mechanical stage; no class number is read from
  it, and I say so before it runs rather than after.
- **A2-P3 — the returned frame is 672×1568**, the most extreme portrait in Kontext's set,
  because our aspect (0.34375) is narrower than anything the table offers (0.4286 is the
  narrowest). *Falsifier: any other shape — which would mean I have the table wrong, and
  A3's frame derivation depends on getting it right.*
- **A2-P4 — the subject survives as a clay mannequin.** At turbo defaults (4 steps, cfg 1.0,
  Lightning LoRA) with the clay as edit reference, I expect a recognisable figure rather
  than a re-imagined scene. Odds **0.7**. Low confidence: the Lightning LoRA is a named model
  nobody here has measured.

## What I am NOT predicting yet

A3's pale, dark census, register and chroma-split bands. They belong to a question that only
exists if A2 produces an image, and the frame they will be measured in is not yet known —
it is derived in A3 from the scale node's own table, enumerated. **Writing them now would be
predicting about a population whose unit I have not yet measured**, which is the family this
repo has missed on for nine consecutive arcs.

## The standing correction I am carrying into this sequence

My last three pale-direction calls missed, and my P2a band in the pilot **could not fail** —
it predicted "the graph runs" against a failure mode that runs and returns nothing. So every
band above is written as a property of the **returned pixels**, not of whether the job
errors. `succeeded` is not evidence here and is not used as any band's falsifier.
