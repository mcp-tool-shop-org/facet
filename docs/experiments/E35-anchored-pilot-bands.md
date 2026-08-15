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

---

# D1 bands — registered before the discriminator ran

## ⚠ Local enumeration first, which the dispatch's own falsifier branch asks for

Both clay inputs read at the PNG chunk level before any job:

| | A2's input (352×1024) | A3's input (native 672×1568) |
|---|---|---|
| bit depth | 8 | 8 |
| colour type | **6 (RGBA)** | **6 (RGBA)** |
| interlace | 0 | 0 |
| chunk set | IHDR, sRGB, gAMA, cHRM, eXIf, oFFs, pHYs, 7×tEXt, IDAT…, IEND | **identical** |
| alpha | **1 unique value, 255 everywhere** | **1 unique value, 255 everywhere** |

**The two files are structurally identical except for size.** Two consequences, recorded
before D1 spends:

1. **Two of the dispatch's three named fallback candidates are already exonerated** — bit
   depth and PNG colour type are the same in the file that worked and the file that did not.
   Of its list only *upload normalization* survives, joined by content-side candidates the
   list did not name (framing, spatial frequency).
2. **The alpha hypothesis survives only in Ruling 8's exact form** — that the *path* differs,
   the resample stripping a fourth channel the no-op passes through. It is **not** that the
   files differ in alpha: they do not, and the alpha is a constant 255 plane in both, which
   carries no spatial structure that could produce three distinct corruption patterns. D1 is
   still the right discriminator; its clean branch would now be evidence about ComfyUI's
   path, not about our file.

## The bands

**D1-P1 — the flattened input still corrupts.** Odds **0.7**, and I am registering against
the dispatch's leading hypothesis. Reason: the alpha planes are identical and constant in
both files, so for alpha to be the trigger the corruption must come from a channel carrying
no information — possible only as a shape/stride fault, which would be a platform bug rather
than a property of our data. *Falsifier: a clean image, which confirms exactly that and makes
the flatten a permanent step in this route.*

**D1-P2 — the register survives IF the image is clean.** The new term Ruling 8 folded, and
this is its first use: **C\* on the keyed figure ≥ 15**, against A2's terracotta and the
recorded twin's 23.77. *A corrupted return scores this as N/A, not as a fail — the term
exists to separate a mannequin from a rainbow, and it can only speak when there is a figure
to key.*

**D1-P3 — if it corrupts, the signature is a FOURTH distinct one.** A3a streaked
horizontally, A3b streaked and banded across the whole frame, A3c came back a blocky
patchwork. Three inputs at one configuration gave three patterns, so the fault is not
deterministic in the input. *Falsifier: it reproduces one of the three exactly, which would
make the fault deterministic after all and change what the remaining candidates can be.*

**D1-P4 — the flatten does not change one RGB value.** Alpha is 255 everywhere, so
compositing is arithmetically the identity. Asserted locally before upload, not assumed.

---

# E1 bands — the traversal-vs-content discriminator, registered before the job

**At the Director's go**, 2026-08-14. The job I named in the D1 report and did not take.

## The construction

The recorded 352×1024 clay, put through **my local replay of the scaler's transform** —
lanczos ×1.909091 to 672×1955, centre-crop to 1568, top offset 193 — saved as a 672×1568
RGB PNG (colour type 2 read from the IHDR bytes) and submitted through A2's proven config.

**The fork this splits**, and why it is decisive either way: those pixels are content-
equivalent to what `FluxKontextImageScale` produced for A2, but they arrive as a file the
node will **no-op** on (672×1568 is already legal).

- **Clean ⇒ traversal is irrelevant; the pixels are what matter**, and A3's *native render
  content* is the trigger.
- **Corrupted ⇒ traversal is what matters** — content-equivalent pixels behave differently
  depending on whether the node resampled them — which is a platform-side finding and closes
  our side of the question.

⚠ **The replay is content-equivalent, not bit-equivalent.** PIL's lanczos is not ComfyUI's
torch `common_upscale`, so I cannot claim identical pixels to A2's intermediate. That is
sufficient for this fork and insufficient for any stronger claim, and I am saying so before
the result rather than after.

## Measured locally, before the job

| | resampled (E1 input) | native 672 (A3/D1 input) |
|---|---|---|
| mean | 161.5 / 162.0 / 164.2 | 159.1 / 159.4 / 161.7 |
| std | 24.3 / 25.3 / 24.9 | 20.2 / 21.1 / 20.8 |
| unique colours | 5,046 | 2,620 |
| mean \|gradient\| | 2.0762 | **2.2042** |

⚠ **This weakens the softness hypothesis before spending.** I had named "a 1.909× lanczos
upscale is soft and band-limited; a native render is not" as a candidate — measured, the
native is only **1.06×** sharper. The two inputs differ far more in **framing** (the
resampled one is cover-cropped, so the figure fills more of the frame and the head is cut)
and in interpolated colour count than in sharpness.

## The bands

**E1-P1 — it comes back CLEAN.** Odds **0.75**. If content decides and these pixels are
content-equivalent to A2's, this should behave like A2. *Falsifier: corruption, which moves
the finding to the platform and is the more interesting outcome.*

**E1-P2 — the register survives: C\* on the keyed figure ≥ 15** (Ruling 8's term, second
use). Scored N/A if the frame is corrupted, on the instrument's refusal rather than my say-so.

**E1-P3 — if clean, it resembles A2 rather than reproducing it.** Same config, content-
equivalent input, but my lanczos is not the node's, so the pixels differ upstream and 2509 is
deterministic-per-input. *Falsifier: pixel-identity with A2, which would mean my replay is
bit-exact after all — a stronger result than I am claiming.*

**E1-P4 — framing, not sharpness, is the live content candidate**, on the 1.06× gradient
ratio above. Stated as a claim about which candidate survives, not as a prediction about
this job's pixels.

## What I will do on each branch, stated before the result

- **Clean** → the true A3 becomes runnable and I proceed to it under the ruling's D2 terms
  (turbo OFF and stated, 20 steps at the template's non-turbo settings, no ControlNet, no
  seed override), measure the classes at the derived frame, build the sheet, and **HALT for
  the Director's eye**. ≤ 2 further jobs, 47 of 60 at worst.
- **Corrupted** → I stop. The finding is platform-side, there is no measurable configuration
  at our own frame, and inventing a further probe is not mine to do.

---

# E2 bands — interpolation vs framing, registered before the job

## ⚠ First: my E1 branch plan's premise was wrong, and I am not executing it

The E1 bands said *"Clean → the true A3 becomes runnable and I proceed to it."* **That
premise does not hold.** E1 was clean using the **resampled** input, whose framing is the
cover-crop — it does not make a *native-frame* run work, and the head band is still cut
(rows −78…227), so the classes are still not measurable there. Executing the stated plan
mechanically would have run a measurement whose head region is missing the crown, which is
exactly where the pale class lives.

Stating it before adapting, because a branch plan written in advance is worth nothing if I
follow it past a premise that failed.

## What E1 settled

**Traversal is irrelevant; the pixels are what matter.** Content-equivalent pixels arriving
as a file the node no-ops on came back clean (E1-P1 HIT at 0.75, E1-P3 HIT — resembles A2 at
mean |Δ| 1.70 without pixel-identity). So **A3's native render content is the trigger**, and
two candidates remain: the **framing** (native puts more background around the same figure)
or the **interpolation character** (native is flat-shaded and quantised; the scaler's output
is interpolated).

## The construction

The **native** 672×1568 render put through an inverse-then-forward lanczos round-trip
(672×1568 → 352×821 → 672×1568). **Framing untouched, interpolation character acquired.**
One variable, and it is the one that separates the two survivors:

| | unique colours | mean \|grad\| | std | verdict so far |
|---|---|---|---|---|
| resampled (E1 input) | 5,046 | 2.0762 | 24.3 / 25.3 / 24.9 | **CLEAN** |
| native (A3/D1 input) | **2,620** | 2.2042 | 20.2 / 21.1 / 20.8 | **CORRUPT** |
| **native round-tripped (E2)** | **5,336** | 1.8027 | **20.2 / 21.1 / 20.8** | — |

The round-trip sits in the clean family on colour count and in the native family on framing
(std identical to the native's, because the framing is the native's).

## The bands

**E2-P1 — it comes back CLEAN**, odds **0.6**. The colour-count gap (2,620 against ~5,000) is
the largest measured difference between the working and failing inputs, and a heavily
quantised flat-shaded render is the kind of off-distribution input that can produce
degenerate latents. *Falsifier: corruption, which puts **framing** as the trigger and means
no native-framed input works — closing the measurable-frame route entirely.*

**E2-P2 — the register survives: C\* on the keyed figure ≥ 15.** Ruling 8's term, third use.
N/A on the instrument's refusal if corrupted.

**E2-P3 — if clean, the classes become measurable for the first time in this arc.** The
mask at this framing already exists and is verified (`armclay672mask_1.png`, edge deltas
0.22–0.75 px), and the head band is `slice(92,337)` — fully inside the frame, crown
included. *This is the whole point: a clean E2 is the first configuration where the pale and
dark classes can be read at all.*

**E2-P4 — I am NOT predicting the class values here.** The scaled parameters are derived and
recorded, the head band is verified, but a clean E2 is a new population and I have missed the
pale direction 3 of 3 this arc. If E2 is clean I will register the class bands **before**
running the instruments on it, as a separate block, per the rule that a prediction comes
before the number and not with it.

## The branch plan, restated correctly

- **Clean** → register class bands, then measure pale / dark / register / chroma-split at
  the derived frame, build the sheet, **HALT** for the Director's eye. No further jobs.
- **Corrupted** → framing is the trigger, no native-framed input works, and the arc's class
  question cannot be answered at our own frame by this route. I stop and say so.

---

# E2 CLASS bands — registered after seeing the image, BEFORE any instrument ran

**E2 came back clean** (P1 HIT at 0.6, P3 HIT). The trigger is the **interpolation
character**, not the framing: a native render round-tripped through lanczos works, the same
render untouched corrupts. **This is the arc's first configuration where the classes can be
read** — full figure, crown included, at a frame whose mask is already built and verified.

**Blindness limit, stated exactly.** I have looked at the image. I have NOT run the census,
the pale instrument or the register instrument on it. These bands are from the eye and the
construction, and the disclosure is the point: they are *not* blind to the picture, only to
the numbers.

## The configuration being measured

E2 = served template · our native 672×1568 clay, lanczos round-tripped · v-next prompt at
`433.image` · **turbo ON** (4 steps, cfg 1.0, Lightning LoRA) · no ControlNet · no seed
override. ⚠ **Turbo carries a LoRA, and R3 as the Director ruled it says NO LoRA** — so this
measures 2509+Lightning, not 2509. Named as a limit of the reading, not smoothed over.

## Instrument parameters — derived, recorded, unchanged since

Mask `armclay672mask_1.png`; head `slice(92,337)`; census `--blob-max-px2 84 --small-px2 21
--window 23`; pale `--min-area 59 --window 47`. All scaled from the linear 1.53125 / area
2.34473 ratios and nothing else. Baseline for direction only, **not for absolute
comparison**: recorded twin pale 278 / rise 4.97 / dark 16 / 157 px² / C\* 23.77 at 352×1024.

## The bands

**E2-C1 — register survives, C\* ≥ 15.** Ruling 8's term. From the eye the terracotta is
strong. Band **18–32**.

**E2-C2 — dark census RISES above the recorded 16.** Band **18–60**. Reason, and it is a
content reason rather than a defect one: the brows are rendered as **hard black graphic
lines** and the herringbone hatching is far heavier than the recorded twin's, so there is
simply more dark material on this figure. *This is the band I most expect to be argued with,
because a census rise here is not the same defect the arc has been chasing — it is the
prompt's own terms rendered literally.*

**E2-C3 — pale area is LOW, band 0–250, at LOW confidence.** The crown reads evenly toned to
my eye and there is no visible wash. **My pale-direction calls are 0 for 3 this arc**, which
is why the band's floor is 0 and its ceiling still reaches below the recorded 278 rather than
being pinned tight.

**E2-C4 — if pale is non-zero, the chroma split lands (ii)**: pale C\* **above 15**, far from
the clay's 1.12. At denoise 1.0 there is structurally no init to revert toward. N/A if pale
area is 0.

**E2-C5 — reg-IoU ≥ 0.85 against the verified mask.** With no ControlNet the silhouette is
held only by the edit reference, so this measures how faithfully 2509 tracks it. **Reported
as a fidelity number, not as a class metric** (the A3-P8 rule, carried).

**E2-C6 — identity has moved.** Longer face, different nose, different proportions from the
recorded twin. Not measurable; the Director's eye. Registered so it can be wrong.

## After the numbers

Build the sheet, **HALT**. No further jobs. The obvious next single job — **turbo OFF, no
LoRA, R3-compliant, same round-tripped input** — is named for the Director's word and is not
taken on my own initiative.

---

# F1 bands — the un-confounding job, registered before submission

**At the Director's word (Ruling 9).** E2's exact configuration with **turbo OFF**. One job,
46 → 47 of 60.

## The resolved sampler settings, stated before submitting as ordered

Turbo off flips `PrimitiveBoolean` 443, which drives three `ComfySwitchNode`s. Resolved from
the template's own graph, node by node — **not chosen by me**:

| | source in the graph | F1 value | (E2 was) |
|---|---|---|---|
| steps | `PrimitiveInt` 438 via switch 441 `on_false` | **20** | 4 |
| cfg | `PrimitiveFloat` 439 via switch 442 `on_false` | **4.0** | 1.0 |
| model path | switch 440 `on_false` = `UNETLoader` 37 direct | **no LoRA** | Lightning 4-step |
| sampler | `KSampler` widget, unswitched | `euler` | same |
| scheduler | `KSampler` widget, unswitched | `simple` | same |
| denoise | `KSampler` widget, unswitched | `1.0` | same |

cfg 4.0 is **the template's own non-turbo value**, not the recorded route's 2.5. Taking the
model's own sanctioned setting is the smaller deviation; changing it too would put a second
lever in an un-confounding job.

Override: `433.seed_1 = false` — the turbo boolean, whose address is confirmed by A3b, which
took visibly longer at 20 steps.

Everything else byte-unchanged from E2: the round-tripped native input
`0294d3210da93a539cd589bab888fa88e6ff33a9cb7b61cb187905a7c628a14b.png`, the v-next prompt at
`433.image`, no ControlNet, no seed override.

## ⚠ The C3 lesson binds

**No eye-claim about pale appears in these bands.** The last one said the crown read evenly
toned on a figure carrying 3.6× the recorded twin's wash. The pale band below is reasoned
from mechanism and precedent only; **the instrument reads the class, and I do not.**

## The bands

**F1-B1 — register FLOOR: C\* on the keyed figure ≥ 15.** Ruling 8's term as a floor and
nothing more. **The two-sided band is dead** — I invented its upper bound and it is the part
that failed at 37.53. No ceiling is predicted here.

**F1-B2 — pale falls relative to E2's 2,323 px², band 400–2,000.** Reasoning, with no
appeal to the eye: 20 steps at cfg 4.0 converges further than 4 steps at cfg 1.0, and the
class is a *local lightness excursion* — a more converged render has less local contrast
noise. **Confidence LOW and stated: my pale calls are 0 for 4.** *Falsifier: ≥ 2,323, i.e.
Lightning was not contributing to it.*

**F1-B3 — dark census falls sharply relative to E2's 734, band 100–600.** The strongest
reason is content rather than defect: much of E2's 734 is herringbone hatching fragmenting
into components, and a higher-cfg, more converged render draws that hatching *more*
coherently, not less — so I expect fewer, larger components. *Falsifier: a rise, which would
mean cfg 4.0 renders the prompt's hatching term harder still.*

**F1-B4 — chroma split stays signature (ii)**, pale C\* > 15. At denoise 1.0 there is
structurally no init to revert toward. High confidence; N/A if pale area is 0.

**F1-B5 — reg-IoU stays ≥ 0.90.** E2 hit 0.9611 with no ControlNet; the edit reference is
doing that work and turbo is not what holds it.

**F1-B6 — F1 and E2 are visibly different, and F1 is the LESS glossy of the two.** The
Lightning LoRA is a style model; removing it should move the surface toward matte.
*Falsifier: indistinguishable, or F1 glossier.*

**F1-B7 — identity is still not the recorded man.** Neither Lightning nor step count is what
moved it; the model did. Not measurable — the Director's eye, and his call on whether the
identity and register are acceptable is the halt's whole purpose.

## The sheet and the instruments

Three columns — recorded r3 | E2 (Lightning) | F1 (no Lightning) — at full size, **the same
instruments on all three**: `twin_despeckle --mode census`, the pale instrument, and
`t2_register_all`. The recorded column runs at 352×1024 with default parameters and its own
mask; E2 and F1 at 672×1568 with the parameters already derived from the 1.53125 / 2.34473
ratios and the verified `armclay672mask_1.png`. Same code paths, parameterised per frame —
stated so nobody reads three columns as three instruments.
