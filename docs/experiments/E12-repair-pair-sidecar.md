# The beast's RE-PAIR — what this is, declared at birth

**Generated 2026-08-06, E12 handoff 4 Task 2.** Two views on Comfy Cloud, **0 credits**
(`estimate_credits`: *"0 credits — no paid API nodes found in this workflow"*, before
submission). **0 re-rolls of the 1 allowed.** Both jobs `succeeded` with **zero warnings**.

## WHAT THIS PAIR IS, AND IS NOT

**It is a SPECIFICATION SOURCE and a VISUAL TARGET. It is NEVER a projection reference.**

Unchanged from the first pair's sidecar and for the same measured reason: **twins belong to a
mesh, and a twin has exactly one job — register to the silhouette it will be projected onto.**
These two images exist to make the fixture visible and to give the palette bands something
non-circular to cross-check against. They are *not* the twins. When the beast is textured,
`restylize_views` generates its own twins from the mesh it is about to texture, per view.
Projecting *these* would be the A0-vs-W3 error — 62% coverage collapsing to 22.7% because a
twin carried a different mesh's silhouette.

**And it is not a comparison against the rejected pair.** E12 Ruling 10c: the re-pair runs as
a DECISION bundle (new register + derived control), not an experiment against a rejected
baseline. Nothing here is measured against `E12_pair/`.

## The two things that changed, and nothing else

| | rejected pair (5a91646) | **this pair** | authority |
|---|---|---|---|
| **style register** | saltroad painterly LoRA @ 0.75 | **ultra-realistic, menacing — NO LoRA** | Director, E12 Ruling 10b |
| **canny pair** | 0.4 / 0.8 (102/204) | **0.05 / 0.10 (12/25)** | Director's ruling on Task 1's derived curve |
| clay renders | — | **byte-identical, reused** | cloud upload names are content hashes and both returned the SAME names handoff 3 uploaded |
| silhouettes | — | **byte-identical**, 0 differing px, IoU 1.000000 | `silhouette_masks --anchor` |
| seed / steps / cfg / denoise / cn | 770700 / 20 / 2.5 / 0.92 / 0.9 | **identical** | the profile's, checked by value in pre-flight |
| negative | `watermark, text, logo, blurry, photo, deformed` | **identical** | Director ruled it unchanged this run — see the flag below |

**NO LoRA is the ABSENCE OF A NODE, not a weight of zero.** `e12_pair_cloud_step.py` reads
`lora-w: 0.0` from the profile and omits the loader entirely; `ModelSamplingAuraFlow` reads
the UNET directly. The graph is **14 nodes, was 15**. The pre-flight **inverts** for this case
and scans every node for the LoRA class family and for the card name in any input — gating the
failure mode (a loader surviving) rather than the success mode. That guard was self-tested by
injecting a `LoraLoaderModelOnly` at strength 0.0 into a copy: it fired on both the class name
and the card string, exit 1, no file written.

**Corroboration that the removal took:** both `dry_run`s and both submissions returned **zero
warnings**. The rejected pair's runs all carried
`Node #5 (LoraLoaderModelOnly): "lora_name" ... was not found in the bundled node index`
(the banked E08 A31 trap). There is no node 5 now, and the warning is gone with it.

## The control, and why it is the arm

`E12-task1-canny-report.md` is the derivation. In one line: at the profile's inherited
0.4/0.8 the control was a **colouring-book outline** — silhouette plus a handful of the
strongest creases, **empty wings** — and at denoise 0.92 everything inside it was the model's
to invent.

| view | control at 0.4/0.8 | **control at 0.05/0.10** |
|---|---|---|
| 1 | 50,631 px (canny 36,011 + contour 25,256) | **108,887 px (canny 94,269 + contour 25,256)** |
| 5 | 37,228 px (canny 22,642 + contour 25,256) | **88,717 px (canny 74,131 + contour 25,256)** |

Interior edge fraction (silhouette eroded 5 px) rises **3.5× / 6.1×** on views 1 / 5.
The contour term is unchanged by construction — it is the mask's morphological gradient and
does not depend on a threshold.

**`canny-low = 0.05` is DERIVED**: the lowest grid value at which the flat-field artifact is
measured absent (W-flat12 ≤ 0.18% against 1.19–3.97% at 0.02) and confirmed absent by eye at
5× on a smooth membrane field. **`canny-high = 0.10` is the Director's ruling** on the trade
table — no instrument in Task 1 bounds `high`, and the report says so rather than inventing a
derivation. It arrives as an **explicit flag override**, printed as a recorded deviation:
`profiles/beast.json` still carries 0.4/0.8 marked FALSIFIED with the replacement owned by
this arm. **The profile write is the advisor's** (Ruling 9e).

## Provenance

| | |
|---|---|
| mesh | `E12_prep/prep_uv.glb` — the prep bake of `dragon_00003_raw.glb`, Director-designated at E12 Gate 0 (Ruling 1) |
| clay source | `E12_pair/clay/dragonclay_{1,5}.png` — `turn_render --clay --profile beast.json`, **1792 × 1024**, fit-axis **width**, margin 1.204, tag `dragonclay`. **Reused read-only**; that directory was never opened for writing |
| silhouettes | `E12_repair/masks/dragonclay_{1,5}.png` — `silhouette_masks --profile beast.json`, 26.754% of frame, 490,941 px each, **anchored byte-identical** to `E12_pair/masks/` |
| **anchor** | `e04_frame_agree` ANCHOR 1c, **0 differing px on both views**, run BEFORE the controls and before any upload. The legacy unconformed construction is printed beside it (1 px on view 5) and is not gated — E12 Ruling 9a/10h |
| control | `E12_repair/pair/dragonclay_{1,5}_control.png` — `restylize_views --emit-only --masks`, canny 0.05/0.10 + morphological contour from the **exact raycast silhouette**, never a keyed render |
| views | **1 = head-side three-quarter** (head, chest, wing leading edges), **5 = tail-side three-quarter** (tail spines, wing backs, hindquarters) |
| prompt | `docs/experiments/E12-twin-prompts.json` v**E12-pair-3**, built by `e12_make_twin_prompts.py` — every stem DERIVED from `beast.json`'s prompt entry by deleting whole comma-terms, asserted an ordered subsequence, five full-string views asserted byte-equal. **View 1 runs the full 17-term string; view 5 runs its rear stem (11 terms** — drops D4 D5 D8 D9 D10 D11), the split ruled at 9d and corrected by measurement at 10i |
| LoRA | **NONE.** No loader node in either graph |
| recipe | seed **770700**, steps 20, cfg 2.5, denoise 0.92, ControlNet strength 0.9, shift 3.1, euler/simple — every value the profile's, checked by value in pre-flight |
| workflows | `E12_repair/pair/workflow_{1,5}.json` — **saved before submission**, with the uploaded cloud names in them, so the saved file *is* the submitted graph |
| uploads | `E12_repair/pair/uploads.json` — local → cloud for all four inputs |
| prompt ids | `5390e51b-5762-4306-a7c5-bf828ec2a6f7` (view 1), `2bab19d7-bcfa-4602-8add-c290ed863421` (view 5) |
| outputs | `target_1_head_three_quarter.png` sha256 `aa386e3f718e6ad8…`, `target_5_tail_three_quarter.png` sha256 `53074e84fefd6602…`, both **1792 × 1024** |
| re-rolls used | **0 of the 1 allowed** |

## ⚠ Flagged BEFORE any measurement existed, and unchanged by the Director's ruling

`beast.json`'s negative is `watermark, text, logo, blurry, photo, deformed` — a FIRST-RUN
OPERATING POINT inherited from two subjects that ran a **painterly** register. The beast's
register is now **ultra-realistic**, and that negative asks the sampler to move *away from*
`photo`. This was recorded in `E12-task1-canny-predictions.md` before any Canny had run, so
it is on the record blind rather than as an after-the-fact explanation.

**The Director ruled it unchanged for this run**, on the ground that the re-pair then changes
exactly two things (register + control) and stays attributable. If the register does not land
at his eye, `photo` is the named next suspect with its own arm.

## What this pair does NOT establish

Nothing about whether the route works on a beast. No twin, no atlas, no projection, no bake
has consumed it. The pair exists so the Director has his overrule window on the authored
identity in its ruled register, made visual — and, if he accepts it, so the palette bands
have a non-circular cross-check (the suspended Task-5 bands died with the rejected pair).

**And the same thing it could not separate before, it still cannot.** View 5 shows no grafted
head anatomy — but its camera cannot see the head *and* its stem drops those elements.
Isolating "the stem worked" from "the geometry hid it" needs view 5 generated with the full
string: a second generation, out of this dispatch's scope, and its own arm if a ruling wants
it.
