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

---

# A3 bands — registered after A2 landed, before A3 was submitted

**A1 and A2 both produced images. A1-P1/P2 and A2-P1/P2/P3/P4 all HIT** (scored in the
report). The reduced question is now well posed, so A3's bands are written here — the
dispatch's order, and the reason the class bands were withheld until the frame was known.

## The frame, DERIVED not assumed

The dispatch says to take the nearest Kontext-legal portrait frame *from the scale node's own
table, enumerated, never assumed*. The node's implementation is not exposed by `get_node`, so
the table cannot be read — but the node can be **asked**: A2 fed it our own 352×1024 clay and
it returned **672×1568**. That is the node's answer for our aspect, which is stronger evidence
than a table I transcribe. **A3 renders our clay and our mask at 672×1568**, so the scaler
becomes a no-op and the frame is ours by construction rather than by its choice.

Both legs verified before any A3 job:

- **The render invocation is the recorded one** — view 1 re-rendered at 352×1024 through the
  `saltroad_bake_fix` copy of `turn_render.py` matches the recorded `armclay_1.png` at
  **0 differing pixels**. The anchor the pilot skipped, applied to the renderer too.
- **The 672 frame registers to the 352 frame**: vertical is a pure ×1.53125 scale (bbox edge
  deltas **0.22** and **0.75** px), horizontal carries a **computed** +66.50 px centre offset
  — `(672 − 352 × 1.53125) / 2`, from the frames themselves, not fitted — with edge deltas
  **0.31** and **0.62** px. ⚠ My first version of this check predicted a *pure* scale on both
  axes and **FIRED**; the render was right and my model was wrong. Recorded because a check
  that fires and is then read correctly is the point of having it.
- **The head band scales vertically only**: `slice(60,220)` → **`slice(92,337)`**, confirmed
  independently by the fraction of figure it captures — **11.5977%** at 352 vs **11.6012%**
  at 672, 0.0035 points apart.

## ⚠ The unit problem, stated before the numbers exist

**A3's absolute class counts are NOT comparable to the recorded twin's.** Linear ratio
1.53125, **area ratio 2.34473** — and the census's `blob_max_px2 36` is an *absolute* cap, so
a 20 px² speck at 352 becomes 47 px² at 672 and falls *outside* the population the recorded
census counted. Left alone, the same command would measure a different class and report it in
the same column. Derived scalings, from the ratios and nothing else:

| parameter | recorded | at 672×1568 | scales by |
|---|---|---|---|
| census `blob_max_px2` | 36 | **84** | area |
| census `small_px2` | 9 | **21** | area |
| census `window` | 15 | **23** | linear |
| pale `min-area` | 25 | **59** | area |
| pale median window | 31 | **47** | linear |
| pale `head` | 60,220 | **92,337** | linear (vertical) |
| census `dark_dl`, `de_min`, `chroma_floor`; pale `DL`; C\* | — | unchanged | scale-free |

Both readings are reported: **scaled** (the like-for-like population) and **default-param**
(what the flagless command would have said). The scaled one is the comparison; the default one
is there so the size of the trap is visible.

## The two A3 jobs, and the turbo decision stated

The dispatch allows 1–2. Both are taken, and the pair **isolates the Lightning LoRA**:

- **A3a — turbo ON** (4 steps, cfg 1.0, Lightning LoRA): A2's proven configuration, changed
  only by the frame. Minimal deviation from a run that demonstrably works.
- **A3b — turbo OFF** (20 steps, cfg 4.0, no LoRA): R3 as the Director ruled it says **NO
  LoRA**, and the pilot's product is a register measurement, which an unmeasured style LoRA
  would confound. **This is the deviation from the proven baseline and it is A3's mechanical
  risk** — named here, not discovered later. cfg 4.0 is the template's own non-turbo value,
  taken rather than the recorded route's 2.5, because 2509 is a different model and its own
  sanctioned setting is the smaller deviation.

No ControlNet in either: no served pairing exists and the union's declared base is Qwen-Image.

## The bands

**A3-P1 — both jobs produce non-degenerate images**, > 1000 unique colours. Odds **0.9** for
A3a (A2's config, new frame), **0.7** for A3b (unproven config). *A3b coming back black is a
mechanical result about the turbo switch, not about 2509.*

**A3-P2 — pale, scaled, falls below the recorded 278.** Band **60–300** on A3a.
⚠ **Registered at LOW confidence: my pale-direction calls are 0 for 3 this arc.** The reason
to expect a fall is structural rather than empirical — at denoise 1.0 with the clay entering
as a semantic reference there is no raw init latent to survive — and Ruling 2 says the
recorded class is signature (ii), whose mechanism is OPEN, so structure may not decide it.

**A3-P3 — the chroma split lands (ii) again**, pale C\* **above 15**, far from the init's
1.12. Held at **high** confidence: at denoise 1.0 there is structurally no init to revert
toward. *If it lands (i), my model of this pipeline is wrong somewhere I cannot see, and that
outranks every other row on the sheet.*

**A3-P4 — dark census, scaled, falls but is not eliminated.** Band **4–16** components.

**A3-P5 — register C\* lands 15–30**, wide, for a model whose colour prior is unmeasured here.

**A3-P6 — A3a and A3b differ visibly**, and A3b is the **matter** one: no Lightning LoRA
should mean less of A2's gloss. *Falsifier: they are indistinguishable, which would mean the
LoRA contributes nothing at this cfg and the turbo switch is not the lever I think it is.*

**A3-P7 — identity moves on both.** Not measurable; the Director's eye.

**A3-P8 — reg-IoU is NOT reported as a class metric.** With no ControlNet the silhouette is
held only by the edit reference, so reg-IoU measures how faithfully 2509 tracks its reference
— an interesting number, and *not* one of the two classes. Stated so it is not quietly read
as a quality score.
