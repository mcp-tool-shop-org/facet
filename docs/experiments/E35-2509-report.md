# E35 — 2509 pilot, executor report

**Run 2026-08-14 at the Director's word** ([E35-ruling.md §4](E35-ruling.md)). Spec: the
dispatch; bands registered blind and pushed at `e5248ec` **before the graph was built**.

**Two jobs spent, both authorised. Spend 36 → 38 of 45.** The second fired under the
dispatch's own clause — *a second only if the first fails on a mechanical defect rather than
on content* — and the first failure was mechanical.

**The pilot did not produce an image.** Both jobs returned a **pure-black 352×1024 frame,
one unique colour (0,0,0)**, while reporting `succeeded`. Nothing about the two defect
classes was measured, because there is nothing to measure.

---

## 1. The walk

There is no walk. Both outputs are a single colour. The sheet
(`facet_E35\diag\E35_2509_sheet.png`) shows them full size beside the recorded twin with the
clay init and the canny control as provenance, because a sheet with an empty result on it is
still the honest artifact and the Director asked to see the sheet.

**The instruments refuse rather than answering.** `t2_register_all.py` on the black frame
fires its own guard — `ANDON: keyed figure empty` — and returns no row. That is the ring-fit
background estimator declining to read a number off a frame with no figure in it, which is
the behaviour E08's bbox-check discipline exists to produce. No census, pale or register
figure is reported below, and none is invented.

## 2. What was enumerated before building (the dispatch's step 1)

Full JSON of `image_qwen_image_edit_2509`: 4 top-level nodes wrapping the 21-node subgraph
`eba40a3a-f6c5-48ac-b58e-55525d06b373`.

| asked | found |
|---|---|
| **encoder** | two `TextEncodeQwenImageEditPlus` (111 positive, 110 negative), inputs `clip` · `prompt` · optional `vae`/`image1`/`image2`/`image3` — **the advisor's verified schema, confirmed at the node level** |
| **sampler** | one `KSampler`, `euler`/`simple`, **denoise 1.0**, steps and cfg driven through three `ComfySwitchNode`s off a `PrimitiveBoolean` "Enable Lightning LoRA" defaulting **true** (4 steps / cfg 1.0 / Lightning LoRA) vs false (20 / 4.0 / no LoRA) |
| **ControlNet path** | **NONE.** Despite the template's `ControlNet` tag and "ControlNet integration" description, the graph contains no `ControlNetLoader`, no `ControlNetApplyAdvanced`, no type selector |

Three deviations followed, each recorded in the payload sidecar with its reason: the union
path **added** (3 nodes), `FluxKontextImageScale` **removed** (it resizes to Kontext's
preferred set and would have taken the frame away from the mesh that derived it), and the
Lightning LoRA **removed** (a second named-model change against R3's ruled *NO LoRA*).
Steps 20 / cfg 2.5 pinned to the recorded values; denoise left at the template's 1.0 because
the clay enters as an edit reference and 0.92 would re-introduce the pass-through the pilot
exists to test removing.

## 3. What happened, in order

| # | job | prompt_id | payload sha256 | result |
|---|---|---|---|---|
| 1 | 2509 + union ControlNet | `fca935e0-e381-413d-9a25-0f5464559792` | `46fed175daafd658…` | 352×1024, **1 unique colour** |
| 2 | 2509 edit path alone | `bbac66ad-968c-4de7-8558-24ff1c105680` | `b40f341f10ddc58b…` | 352×1024, **1 unique colour** |

`dry_run` returned `validated` with zero warnings on job 1 — **a fourth instance of this
repo's law that a `dry_run` PASS proves nothing about whether a graph works.**

## 4. ⚠ My diagnosis between the two jobs was WRONG, and the measurement says so

After job 1 I diagnosed a **base mismatch**: the InstantX union ControlNet was trained
against Qwen-Image, not the Edit-2509 transformer. The evidence was real and it was gathered
at zero jobs — every served ControlNet template is base-matched
(`image_qwen_image_instantx_controlnet` → Qwen-Image · `image_qwen_Image_2512_controlnet` →
Qwen-Image 2512 with its own `Fun-Controlnet-Union-2602` file · the inpainting, patch and
union-LoRA templates all → Qwen-Image), and **no served template pairs any ControlNet with
`qwen_image_edit_2509`**.

**Job 2 removed the ControlNet and the frame is still pure black.** The diagnosis is
falsified. The catalog observation stands as a fact about the catalog; it was not the cause
of this failure, and I spent the second job on it.

## 5. What is ruled out, what remains — at zero further cost

**Ruled out by measurement:**

- **The union ControlNet.** Job 2 has none and fails identically.
- **The frame.** Both jobs returned exactly **352×1024** — P1 hit. Removing
  `FluxKontextImageScale` did not break the output size; the pipeline ran to completion and
  decoded a correctly-shaped empty frame.
- **A submission or link defect.** Both graphs passed in-code link sanity, a reachability
  check from `SaveImage`, and transcription-equality against the emitted payload before
  submission.

**Remaining candidates, untested, ranked — and a third job is NOT authorised, so they stay
untested here:**

1. **The 352×1024 frame reaching a model that expects Kontext-legal shapes.** This is the
   strongest remaining suspect precisely *because* `FluxKontextImageScale` is in the served
   template at all: the author put it between the input and both the VAEEncode and the
   encoders. 352 px wide is far outside that set. A NaN latent still decodes to a
   correctly-sized black frame, so the size coming back right does not clear this.
2. **cfg 2.5 with `CFGNorm`**, on a model whose sanctioned non-turbo cfg is 4.0.
3. **`weight_dtype: "default"` on the fp8 edit checkpoint** — `qwen_image_edit_2509_fp8mixed`
   is also served and is the obvious alternate.
4. **The negative encoder also receiving `image1`** at cfg > 1 (the template wires it that
   way, but the template also runs at cfg 1.0 by default, where the negative branch barely
   contributes).

## 6. ⚠ The error underneath all of it, and it is mine

**I never anchored the new model before deviating from it.** This repo's own law reads:
*"Moving a line to different hardware needs an anchor first. Reproduce a known output from
its recorded parameters before running anything measured."* A named-model change is that
same move, and the anchor was available for one job: **`run_template image_qwen_image_edit_2509`
as served, on its own input image, unmodified.** That would have established the served graph
produces an image at all, and every later deviation could have been read against it.

Instead job 1 carried **five** changes at once — union path added, Kontext scaler removed,
LoRA/turbo removed, cfg pinned to 2.5, our own frame — and when it came back black there was
no baseline to bisect against. Job 2 could only remove one of the five, and it removed the
wrong one. **Two jobs bought one falsified hypothesis where an anchor-first order would have
bought a working baseline plus one clean bisect.**

The dispatch said "minimal structural delta only." Five simultaneous changes is not that, and
the enumeration I did — which correctly found the missing ControlNet path and the frame
hazard — should have ended in *"therefore anchor first"* rather than *"therefore build all
of it."* Naming what a template lacks is not the same as establishing what it does.

## 7. Bands, scored honestly

Registered at `e5248ec`. **2 hit, 2 missed, 4 unmeasurable.**

| band | predicted | measured | verdict |
|---|---|---|---|
| P1 frame is exactly 352×1024 | yes | **352×1024** both jobs | **HIT** |
| P2a the graph runs at all (0.75) | runs | ran, reported `succeeded` | **HIT, and worthless** — see below |
| P2b the control actually constrains (0.60) | constrains | nothing to constrain | **MISS** — no image |
| P3 pale falls, 80–300, low confidence | falls | — | **UNMEASURABLE** |
| P4 chroma split lands (ii), pale C\* > 15 | (ii) | — | **UNMEASURABLE** |
| P5 dark census 6–16 | falls | — | **UNMEASURABLE** |
| P6 register C\* 15–30 | 15–30 | — | **UNMEASURABLE** |
| P7 identity moves | moves | — | **UNMEASURABLE** |
| P8 cleaner face, different man | — | — | **UNMEASURABLE** |

**P2a is the band worth dwelling on.** I wrote it as *"the graph runs at all (no shape/dtype
refusal)"* and it ran — so by its stated words it hit. But it is a **band that could not
fail in the way it was meant to catch**: the failure mode it was aimed at is "this pairing
does not work," and this pairing does not work *while reporting success*. A prediction about
whether a job errors cannot detect a job that returns garbage with exit 0. That is the same
shape as this repo's IoU-on-a-holed-mesh and dilation-comparison findings, and it is mine:
**before trusting a "runs / does not run" band, ask what a broken run that does not error
would look like.**

The four UNMEASURABLE rows are not misses and are not hits. The pilot never reached the
question they were about.

## 8. What the arc has, and what it does not

**Has:** the served 2509 template enumerated in full and recorded (encoder, sampler,
switch apparatus, the absent ControlNet path, the frame hazard); a versioned pilot emitter
with reachability and forbidden-node checks; the measured fact that this construction returns
black on two variants; the falsified base-mismatch hypothesis; and four ranked untested
candidates with the cheapest anchor named.

**Does not have:** any answer about what 2509 does to the pale or dark classes. The
question the pilot was fired to answer is exactly as open as it was before.

## 9. Artifacts

```
E:\AI\training\facet_E35\
  payloads\make_2509_payload.py                     the emitter, with --no-control
  payloads\payload_p2509_v1.json   + .meta.json     job 1, with the deviation list
  payloads\payload_p2509nc_v1.json + .meta.json     job 2
  twins\twin_p2509_v1.png  twin_p2509nc_v1.png      both black, kept in the record
  diag\E35_2509_sheet.png                           the sheet
docs/experiments/E35-2509-blind-bands.md            registered before the graph existed
```

## 10. HALT

**At the sheet, with two jobs spent and nothing measured.** 38 of 45; seven remain, and by
the ruling the eight-view rebuild does not fit them on any outcome and is not mine to launch.
A third pilot job is not authorised by the dispatch and is not taken.

Rule 5 says a negative result is a full success. **This is a negative result about a
construction, not about 2509** — the difference matters, and the anchor in §6 is what would
tell them apart for one job.
