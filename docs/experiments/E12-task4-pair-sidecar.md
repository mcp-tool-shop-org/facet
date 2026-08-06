# The beast's styled target pair — what this is, declared at birth

**Generated 2026-08-06, E12 handoff 3 Task 4.** Two views, on Comfy Cloud, **0 credits**
(`estimate_credits` returned "no paid API nodes found in this workflow" before submission).
**0 re-rolls of the 1 allowed.**

## WHAT THIS PAIR IS, AND IS NOT

**It is a SPECIFICATION SOURCE and a VISUAL TARGET. It is NEVER a projection reference.**

Same prohibition as the galleon's pair and W3's `canon/twin_*`, for the same measured reason:
**twins belong to a mesh, and a twin has exactly one job — register to the silhouette it will
be projected onto.** These two images exist to make the fixture visible and to give the
palette bands something non-circular to cross-check against. They are *not* the twins. When
the beast is textured, `restylize_views` generates its own twins from the mesh it is about to
texture, per view, and those are what `project_twins` consumes. Projecting *these* would be
the A0-vs-W3 error — 62% coverage collapsing to 22.7% because a twin carried a different
mesh's silhouette.

## The backdrop word, and the estimate it supersedes

| | |
|---|---|
| **ruled word** | **`plain lavender-grey background`** — E12 **Ruling 8a**, blue-violet ruled over a metric-equal desaturated green because a green backdrop behind a green-hided animal is what a metric is content with and an eye may not be |
| the estimate it supersedes | `canon/dragon-materials-estimated.json` scored the low-saturation blue-violet at **rgb(121,121,172)**, weighted-min **0.1978**, bound by D4 — one of three hue families spanning 0.009 of score, which is why the metric did not decide and Ruling 8a did |
| **realised on the pair** | **rgb(188,183,202)** — L\* 75.3, C\* **10.44**, h **301.0** |
| asked, for comparison | rgb(121,121,172) — L\* 52.6, C\* **29.58**, h **293.7** |

**The ask→realise transfer is measured and it is not the galleon's.** The galleon asked white
255 and got 173 — pulled *down* toward mid. This asked a mid-value blue-violet and got
something **much lighter and far less chromatic**: L\* 52.6 → 75.3, C\* 29.58 → 10.44, a 65%
chroma loss. **The hue survived** (293.7 → 301.0, a 7.3° rotation, still blue-violet and still
the one family no declared material occupies). So the *word* landed and its *saturation* did
not — the same direction of failure as the galleon's, at a different starting point.

**And unlike the galleon, this is not a regression.** Re-derived against the pair's own
measured clusters: realised **0.2353**, asked 0.2000, W3's inherited grey **0.0745**. The
realised backdrop is better than the one that was asked for and **3.2× better than the grey
Ruling 8b flagged as scoring under the key's own cut**. The galleon's 4d found the opposite
(realised 0.1000 against W3-grey 0.1451); this one holds.

## Provenance

| | |
|---|---|
| mesh | `E12_prep/prep_uv.glb` — the prep bake of `dragon_00003_raw.glb`, Director-designated at E12 Gate 0 (Ruling 1) |
| clay source | `E12_pair/clay/dragonclay_{1,5}.png` — `turn_render --clay --profile beast.json`, **1792 × 1024**, fit-axis **width**, margin 1.204, tag `dragonclay` |
| silhouettes | `E12_pair/masks/dragonclay_{1,5}.png` — `silhouette_masks.py --profile beast.json`, geometry, 26.754% of frame, 490,941 px each |
| **anchor** | `e04_frame_agree` ANCHOR 1c, **0 differing px on both views**, after the Ruling 9a operand repair. Fired at 1 px before it; see `E12-anchor-repair.md` |
| control | `E12_pair/pair/dragonclay_{1,5}_control.png` — `restylize_views --emit-only --masks`, canny + morphological contour from the **exact raycast silhouette**, never a keyed render |
| views | **1 = head-side three-quarter** (head, chest, wing leading edges), **5 = tail-side three-quarter** (tail spines, wing backs, hindquarters). Verified by eye at pre-flight |
| prompt | `docs/experiments/E12-twin-prompts.json` v**E12-pair-2**. **View 1 runs the full eleven-element string; view 5 runs its rear stem** (drops D4 D5 D8 D9 D10 D11) — E12 Ruling 9d, split verified against each view's render |
| LoRA | `mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500.safetensors` — the live card name, byte-identical to `brush_cloud_step.py`'s `CLOUD_LORA` (asserted) |
| recipe | seed **770700**, steps 20, cfg 2.5, denoise 0.92, ControlNet strength 0.9, shift 3.1, euler/simple, LoRA 0.75 — every value the profile's, checked by value in the builder's pre-flight |
| workflows | `E12_pair/pair/workflow_{1,5}.json` — **saved before submission**, with the uploaded cloud names in them, so the saved file *is* the submitted graph |
| uploads | `E12_pair/pair/uploads.json` — local filename → cloud name for all four inputs |
| prompt ids | `1c4e1964-e768-4a2f-8177-a604960bd84e` (view 1), `5a1bfb0f-befb-40a8-b5a6-08647fe3eccc` (view 5) |
| outputs | `target_1_head_three_quarter.png` sha256 `cd8d195e013a10b4…`, `target_5_tail_three_quarter.png` sha256 `95e773f2962e8e91…`, both 1792 × 1024 |
| re-rolls used | **0 of the 1 allowed** |

## ⚠ The submission warning, quoted rather than absorbed

Both `dry_run` and both submissions returned the same `input_validation` warning:

> `Node #5 (LoraLoaderModelOnly): "lora_name" value "mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500.safetensors" was not found in the bundled node index`

**This is the banked E08 Amendment 31 trap, not new information.** `search_models` and the
node's own option list do not see account imports — both return zero for "saltroad" while the
card sits in the library — so *absent from the node list does not mean absent from the
library*, and an API surface is not ground truth for an import. It was submitted anyway on
three grounds: the name is byte-identical to the constant that generated the galleon's
accepted pair and E10's six accepted strokes on this account two days earlier; a **wrong**
name is rejected by the cloud validator at submission (E08 0b: `not in (list of length 144)`),
at zero credits, so the check exists and is free; and the style is judged by eye downstream,
where a styleless output could not hide. Both jobs returned `succeeded`, and the outputs
carry the LoRA's painterly register.

**`dry_run` still does not validate this field**, and that is worth keeping in front of the
next session: its PASS covers node existence and link integrity — it did not catch E04 Arm
G7's self-link either, which is why link topology is checked in
`tools/diagnostics/e12_pair_cloud_step.py` before the JSON is written.

## What this pair does NOT establish

Nothing about whether the route works on a beast. No twin, no atlas, no projection, no bake
has consumed it. The pair exists so Task 5's bands have a non-circular cross-check and so the
Director has his overrule window on the authored identity, made visual.

**And one thing it cannot separate.** View 5 came back with no head anatomy grafted onto the
hindquarters — D8 and D9 measure **0 px** there against 227 and 958 on view 1. That is the
right outcome, but it does **not** isolate the cause: view 5's camera cannot see the head
*and* its stem drops those elements, so the experiment does not distinguish "the stem worked"
from "the geometry hid it". Isolating it needs view 5 generated with the full string — a
second generation, out of this dispatch's scope, and its own arm if a ruling wants it.
