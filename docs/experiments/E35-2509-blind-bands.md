# E35 — 2509 pilot, executor blind bands

**Registered 2026-08-14, after the served template was enumerated and BEFORE the graph was
built or submitted.** Zero pilot jobs had fired when this file was pushed.

---

## ⚠ Enumeration first — three findings, and one contradicts the dispatch's premise

`get_template image_qwen_image_edit_2509`, full JSON, 4 top-level nodes wrapping the
21-node subgraph `eba40a3a-f6c5-48ac-b58e-55525d06b373` ("Image Edit (Qwen 2509)").

**Encoder — as the advisor verified.** Two `TextEncodeQwenImageEditPlus` nodes (111
positive, 110 negative), each taking `clip`, `prompt`, and optional `vae` / `image1` /
`image2` / `image3`. Schema confirmed at the node level: `image1/2/3`, exactly as the
consult claimed and the advisor checked.

**Sampler.** One `KSampler`, `euler` / `simple`, denoise **1.0**, with steps and cfg driven
through three `ComfySwitchNode`s off a `PrimitiveBoolean` "Enable Lightning LoRA"
(**default true**): turbo on → 4 steps / cfg 1.0 / `Qwen-Image-Edit-2509-Lightning-4steps`
LoRA; turbo off → 20 steps / cfg 4.0 / no LoRA. Both models are served.

**⚠ FINDING 1 — the served 2509 template has NO ControlNet path at all.** Its tag and
description say "ControlNet integration"; the graph does not contain `ControlNetLoader`,
`ControlNetApplyAdvanced`, or `SetUnionControlNetType`. The 25 nodes are CFGNorm, VAELoader,
CLIPLoader, UNETLoader, two encoders, ModelSamplingAuraFlow, VAEEncode, VAEDecode,
LoraLoaderModelOnly, FluxKontextImageScale, KSampler, two PrimitiveInt, two PrimitiveFloat,
three ComfySwitchNode, PrimitiveBoolean, two MarkdownNote, LoadImage, SaveImageAdvanced.
**So "canny via the union path" is a structural ADDITION — `ControlNetLoader` +
`ControlNetApplyAdvanced` + a second `LoadImage`, plus rewiring both encoders' conditioning
through it — not a minimal delta to something already present.** Reported rather than
smoothed over; it is still the smallest construction that satisfies the dispatch.

**⚠ FINDING 2 — `FluxKontextImageScale` would take the frame away from us.** Node 117 sits
between the input image and *both* the `VAEEncode` and both encoders, and its own
description is *"resizes the image to one that is more optimal for flux kontext."* Our frame
is **352×1024**, derived in E33 §F and generator-legal (÷16); Kontext's preferred set is
built around 1MP shapes whose most extreme portrait is 672×1568. Leaving that node in means
the frame is **chosen by the node, not derived from the mesh** — the exact thing the dispatch
forbids — and every downstream measurement (the `HEAD = slice(60, 220)` region, the census
mask, reg-IoU against `armclay_1_mask.png`) assumes 352×1024. **It is removed.** The latent
then comes from `VAEEncode` of our own 352×1024 clay, so the output frame is ours. G1 is the
check, and a wrong frame is a mechanical defect under the dispatch's second-job clause.

**FINDING 3 — turbo is OFF, and that is a register decision, not a taste one.** The default
enables a Lightning LoRA, which would be a **second** named-model change in a job called out
as one — and R3 as the Director ruled it (E33 §14b) reads *"unglazed terracotta, matte
sculpted clay, soft studio light, **NO LoRA**."* Turbo off, no LoRA.

**Sampler settings, and why they are the recorded ones.** Steps 20, cfg **2.5**, euler,
simple — not the template's non-turbo cfg 4.0. The template's own note lists "Comfy Original
20 / 2.5" as a sanctioned row, and holding the recorded values keeps the *model* as the
variable instead of compounding it with a sampler change.

**Denoise stays at the template's 1.0, deliberately.** The recorded route's 0.92 exists to
keep some clay latent; here the clay enters as an **edit reference through `image1`**, and
the whole point of the pilot is that the raw-init pass-through is gone. Setting 0.92 would
re-introduce the very mechanism the pilot is testing the removal of.

---

## Blindness limit, declared

**Not blind to:** the recorded view-1 / seed-770700 baseline (pale **278** / rise **4.97** /
dark **16** / **157 px²** / C\* **23.77** / reg-IoU **0.9372**); the clay init head at
**L\* 76.43 / C\* 1.12**; the whole arm slate; the 2b ladder; Ruling 2's two-signature split.
All my own prior work in this arc.

**Not blind to the design** — I enumerated the template and chose the three deviations above.

**Blind to:** every pixel of the pilot. No graph submitted, nothing measured. Also blind to
whether the Qwen-Image InstantX union ControlNet functions at all against a
**Qwen-Image-Edit-2509** base — a different model from the one it was trained for. That is
this pilot's largest mechanical unknown and I could not settle it at zero jobs.

---

## What one counted thing IS — including the new column

**SPECK / TWIN CENSUS / PALE AREA / L\*-RISE / HEAD region**: unchanged from
[E35-armslate-blind-bands.md](E35-armslate-blind-bands.md). One view, 352×1024,
`HEAD = slice(60, 220)`. Not the eight-view mean.

**THE CHROMA-SPLIT COLUMN** (Ruling 2's mandate) is **the pale region's own absolute
C\***, read against two fixed poles: the clay init's **C\* 1.12** and the twin's own register
C\*. Ruling 2's two signatures separate on the *absolute*, not on a ratio:

- **(i) chroma-collapsing march to the init** — pale C\* falls toward 1.12. Measured on the
  2b ladder: **12.45 → 7.16 → 2.82**, alongside reverted-to-init 5.01% → 36.66% → 56.00%.
- **(ii) chroma-preserved chromatic lightening** — pale C\* stays up at register level.
  Measured on every slate arm: **23.0–26.2**, reverted-to-init 0.16–0.45%.

⚠ **A ratio does NOT discriminate these and I am recording that before anyone reaches for
one.** pale C\*/register C\* is 0.98 recorded, 0.98 for (b), and **1.07 / 1.06 / 1.20** down
the ladder — because when the frame reverts, the register collapses *with* the pale. The
split is the absolute figure plus the reverted-to-init percentage; both already come out of
the two instruments, and **no threshold is invented here** — the two measured clusters are
reported and the reader sees which one the pilot lands in.

---

## The bands

**P1 — FRAME. The twin returns exactly 352×1024.** With `FluxKontextImageScale` removed the
latent is a `VAEEncode` of our own frame, so the output size is ours. *Falsifier: any other
size — a mechanical defect, and the one condition under which a second job is authorised.*

**P2 — THE UNION ON A 2509 BASE.** A conjunction, priced clause by clause, because the join
tracks the rarest clause:

| clause | odds | why |
|---|---|---|
| P2a — the graph runs at all (no shape/dtype refusal) | **0.75** | both are Qwen-family with the same VAE and text encoder; the ControlNet was trained against Qwen-Image, not the Edit-2509 transformer |
| P2b — given it runs, the control actually constrains (reg-IoU ≥ 0.85) | **0.60** | a control that loads but does not bind is this repo's recorded failure mode, and its signature is material/identity change rather than hue shift |
| **join** | **≈ 0.45** | **the pilot is a coin flip on mechanics before it is a test of content** |

**P3 — PALE falls, band 80–300, registered at LOW CONFIDENCE.** At denoise 1.0 there is no
raw init latent to survive, so if the class were signature (i) it would be gone. Ruling 2
says the recorded-recipe class is signature (ii) with mechanism OPEN, so this is a genuine
test rather than a foregone one. **The band is deliberately wide because my pale-direction
calls have missed 3 of 3 in this arc** — I predicted falls on (a) and (c) and got 3.4× and
3.8× rises. Saying so before the number rather than after it.

**P4 — CHROMA SPLIT: signature (ii) again, and this one I hold with high confidence.**
Pale C\* lands **above 15** and reverted-to-init **below 2%**. At denoise 1.0 there is
structurally no init to revert toward, so (i) should be impossible. *If this comes back (i),
my model of the pipeline is wrong somewhere I cannot currently see, and that finding would
outrank everything else on the sheet.*

**P5 — DARK census falls but is not eliminated, band 6–16.** Consult #4's testimony
(2509 still owns a shading prior) plus the observation that the class is baked AO painting,
which a different model repaints rather than removes.

**P6 — REGISTER C\* lands 15–30.** Wide: a different base model has a different colour prior
and there is no measurement in this repo to narrow it.

**P7 — IDENTITY MOVES.** Every arm this arc that substantially changed the generation
returned a different man, and this changes the model itself. **Not measurable by anything on
the sheet** — the Director's eye, as always. Registered so the prediction can be wrong.

**P8 — the shape of the result I expect**: a cleaner face on a different man — the same
trade the slate returned, arriving by a new route. If 2509 gives a cleaner face on the
*same* man, that is the outcome that would justify a successor arc, and it is not the one I
am predicting.

---

## The one I most expect to be wrong about

**P3**, and I have said why in the band itself. After that, **P2b** — I have priced "the
control loads but does not bind" at 0.4 on reasoning alone, with no measurement of this
model pair anywhere in the record.
