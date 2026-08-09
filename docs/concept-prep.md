# Concept prep — the clay hop

**Status: IN THE PIPELINE as stage 0, LOCAL-FIRST, with two implementations.** Ruled by
the Director 2026-08-09: *"I definitely want it in the pipeline, with the option for the
clayify route if the user doesn't mind the cloud. But I want local-first."* Built and
walked the same day. **Its reconstruction arm is still unmeasured** — whether a clay mesh
beats a concept mesh is **E29**, queued behind
[E28](experiments/E28-instrument-census-kickoff.md)'s close — so the stage is real and its
*benefit* is still a hypothesis. Both statements are true at once and neither is softened.

## The two implementations

| | **DEFAULT — local-first** | **OPTION — cloud** |
|---|---|---|
| model | **Qwen-Image-Edit-2511** (20B MMDiT instruction editor) | Nano Banana 2 (Gemini 3.1 Flash Image) |
| licence | **Apache 2.0** — commercial use unrestricted, no output restrictions | **UNVERIFIED**; a vendor ToS, revisable |
| where it runs | this rig, or cloud — **the licence does not change with the venue** | cloud only |
| weights | already on disk: `diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors` (20.5 GB), `text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors` (9.4 GB), `vae/qwen_image_vae.safetensors` | none — an API |
| front-door claim | **covered** | **not covered** |

**Why the default is not "local only."** Qwen-Image-Edit-2511 is Apache-2.0, so cloud
versus local is an *operational* choice, not a licence one — the same weights and the same
graph, either venue, clean both ways. That is what makes local-first worth having: the
default is never compromised by where it happens to run. **Nothing in this repo claims the
pipeline is local-only, and it must not** — the route's own restylize graph stages 31,006
MiB against a 31,200 MiB ceiling and runs on metered cloud for that reason.

**The cloud option stays offered rather than deprecated.** It works, the Director built it,
and a user who does not mind a cloud API should have it. What it does not get is the
licence claim.

---

## The hop it closes

The route's first box has always read *form-exaggerated clay concept*, and the front door
has promised *a styled 2D concept goes in* since the treatment. **Nothing in this repo ever
made that clay.** Every clay that entered the route arrived by hand — staged from a
Downloads zip, byte-counted on arrival, provenance external ([E14's Gate 0](experiments/E14-ruling.md)
is the worked example, three clays with their sha256s in the status table).

Concept prep is that unowned hop: **an arbitrary styled concept image in, a
form-exaggerated clay maquette out**, ready for image-to-3D.

## What it is

A three-node Comfy Cloud workflow, `73c229b3-267f-442f-8050-4d7090d3202c`
("Clay-ify (image to clay)"): `LoadImage` → `GeminiNanoBanana2` → `SaveImage`. Link
topology checked in code before anything else, per [E04 Ruling](experiments/E04-ruling.md)'s
`dry_run` lesson — no self-links, no dangling targets.

| field | value |
|---|---|
| model alias | `Nano Banana 2 (Gemini 3.1 Flash Image)` |
| seed | 42, fixed |
| resolution / aspect | 2K / `auto` |
| thinking level | HIGH |

**The prompt encodes this repo's own measured findings rather than generic clay-render
language**, which is why it works and is worth reading as a specification:
*exaggerated* and *thick sculpted forms* is [E01](experiments/E01-facial-structure-ceiling.md)'s
form-first finding (reconstructors read surface noise as geometry); *matte warm-grey
monochrome* strips the colour a reconstructor would misread; *keep the subject's overall
pose, silhouette and identity recognizable* preserves the original concept's usability as
the downstream canon reference; *seamless plain light grey studio background* removes the
segmentation fight before it starts.

## Gate 0 — the walk, 2026-08-09

One pair, one seed, one subject. **The Director's images were walked at full size before
any number was taken.**

| role | file | bytes | sha256 | frame |
|---|---|---:|---|---|
| concept | `hellenic_minotaur_D_00001_.png` | 1,693,150 | `29fc8b87bf9d7595…` | 832×1216 |
| clay | `ComfyUI_00068_.png` | 6,240,299 | `95f519351b31757c…` | 1696×2478 |

*Hashed in place. **Staging into the recorded tree is deliberately deferred to E29's
Gate 0** — a sibling arc's compensator gate manifests `E:\AI\training` at 7,312 files and
halts on any delta, so adding two files mid-arc would fire another seat's gate. The hashes
above are the anchor until then.*

**What carried.** The pose wholesale — same raised fist, same lowered clenched fist, same
wide stance with the same leg fore and aft, same torso twist. Both wrist wraps in place.
The belt survives **with its round medallion, and the floral emboss sculpted in relief** —
a small named element surviving a full register translation is the strongest single carry
in the pair. The ragged loincloth keeps its torn hem as modelled drape. And it kept
**human feet**: it did not invent hooves, which is the lazy default for a minotaur and
would have been a silent canon rewrite.

**What drifted** — deviations for the Director's eye, not defects:

- **The face went feral → noble.** The concept's bull is wetter and meaner; the clay reads
  heroic-collectible.
- **The mane mass is gone** — shaggy neck-mane to tidy sculpted locks, and the upper
  silhouette slims at the shoulders. This is the one real silhouette change in the pair.
- **Fur elements smoothed** — fur wrist-wrap to clean bands, fur belt-trim to a plain
  edge. Route-correct rather than lossy: fur-as-geometry is exactly the noise the clay
  register exists to strip, and those elements return **through the prompt** at the twin
  stage. What the swap makes explicit is that *fur cuff* and *fur belt trim* must be named
  in this subject's identity fixture — which the identity law already requires, or they
  arrive by accident.
- **Horns thickened and shortened** — the chunky register doing its job; thin-extent risk
  at the tips goes down.

**Measured, after the looking:**

| property | measurement | why it matters |
|---|---|---|
| colour leak | whole-frame C\* p50 **1.04**, p95 **11.24**, p99.9 **13.15**, max **16.78** | the concept's red loincloth and gold buckle left **no tint**; the clay is warm-neutral throughout. Hue is not quoted at all — every pixel sits below the chroma floor, and below a chroma floor hue is undefined |
| background | border ring L **82.4 / 86.0 / 91.0** (p5/p50/p95), C\* p95 **1.25** | a genuinely seamless achromatic sweep, not a painted studio backdrop — the failure mode that broke keying three times |
| framing | 832×1216 → 1696×2478, ratio **0.6842 → 0.6844** | `aspect: auto` held the concept's ratio |
| plinth | none | the sharpest maquette risk was a sculpting base the reconstructor would faithfully rebuild as part of the figure. It did not appear |

**An unrequested benefit worth naming: background normalisation.** The concept stands in a
dungeon with stone touching both feet; image-to-3D on it would fight segmentation before
doing anything else. The clay hands the reconstructor a pre-segmented studio subject. One
hop fixed the form register *and* the background problem.

**What this pair cannot show, stated plainly:** whether the mesh comes back better. That is
the only question that decides whether this becomes a route stage, and it is E29's.

## Where it sits — concept prep, UPSTREAM of the recorded route boundary

**Ruled by the advisor, 2026-08-09, overrulable in a sentence.** The clay is an *input* to
the recorded route, prepared outside it — exactly the status every prior clay held, now
with better provenance than any of them carried. The route proper still begins at
image-to-3D, and no recorded number moves.

Two collisions this placement resolves honestly instead of quietly:

**Reproducibility.** *Nano Banana 2 (Gemini 3.1 Flash Image)* is a server-side alias the
vendor revs; seed or no seed, **replay is not promised**. As a route stage that would be
disqualifying — *a recipe that does not reproduce its output is not a recipe*. As
concept prep it is the canon-twin precedent exactly: **freeze the artifact, hash it, record
provenance as model-alias + date + seed, incomplete by record.** An accepted clay lands in
the recorded tree with its sha256 and the route runs unchanged.

**The front-door claim.** *Local hardware end to end · no non-commercial licence anywhere
in the chain* stays exactly as true as it was — the boundary it describes is the recorded
route, and this hop is upstream of it. The README and handbook now say so in one sentence
rather than leaving a future reader to discover the gap.

## The local default, measured — and what the prompt was worth

Five renders were reported on the minotaur, 2026-08-09. **Three are honest renders**; two
executed nothing, and the reason is itself the finding (see the wiring note below).

| run | config | C\* p50 | C\* p95 | C\* p99.9 | bg L |
|---|---|---:|---:|---:|---:|
| concept (input) | — | 13.75 | 27.44 | 35.25 | 19.2 |
| cloud Nano Banana 2 | — | 1.04 | 11.24 | 13.15 | 86.0 |
| **Qwen run 1** | first-pass instruction, 40 steps | 1.55 | 22.24 | 25.17 | 83.9 |
| **Qwen run 2 — the ceiling** | + *monochrome / warm-grey* + negatives; no LoRA, 40 steps, CFG 4 | 2.20 | **14.63** | **15.92** | 73.3 |
| **Qwen floor** | same prompt; LoRA on, **4 steps**, CFG 1 | **1.27** | 14.89 | 17.29 | **82.7** |

**Run 1 → run 2 changed the prompt and nothing else** — measured, 99.9996% of pixels
differ, a genuine full re-render. The chroma tail fell **34% at p95 and 37% at p99.9**,
closing two thirds of the distance to the cloud tool. Visually the same edit restored the
belt medallion's floral emboss, removed invented spiral motifs on shoulder and thigh, and
sharpened the muscle planes.

**This confirms a law the record already held** — *a colour term reads as a chroma
instruction more reliably than a lightness one* — and it was the Director's call, made
before the measurement: *"there wasn't much prompt-work done on the example, so I'm sure a
lot of that degradation can be mitigated through proper prompts."*

The prompt that produced run 2 is the working one; it is the Clay-ify prompt with one
clause added — *preserve every existing costume and ornament detail — belt, buckle relief,
wrist wraps, hem shape — rendered as sculpted clay relief* — plus a negative prompt:
*engraved spirals, carved decorative motifs, added ornament, tattoos, painted markings,
colour, saturated hues, glossy or wet surface, plinth, base, pedestal, text, watermark.*
The plinth term is prophylactic: a sculpting base is the one artifact a reconstructor would
faithfully rebuild as anatomy.

### ⚠ A WIDGET IS NOT AN INPUT — the wiring finding, and it cost four exchanges

Two further "runs" were reported as a LoRA ablation and a 4-step test. **Neither executed.**
Measured: the ablation was **pixel-identical** to run 2 with **different file bytes**; the
4-step run was **byte-identical**, the same file. Read from the graph rather than guessed:

- A single boolean, `Enable 4steps LoRA?` (node 168, **false**), drives **three** switches —
  model, steps and CFG. False selects: **LoRA bypassed, steps 40, CFG 4**.
- The KSampler's `model`, `steps` and `cfg` are **all link-driven from those switches**, so
  its own widgets (`steps: 4`, `cfg: 3`) are **dead**. ComfyUI ignores a widget whose input
  carries a link.
- So setting LoRA strength to 0 edited a node on the unselected branch — outside the
  sampler's dependency chain — giving a cache hit with fresh PNG metadata. And setting the
  steps *widget* changed nothing at all, so the identical job returned the identical file.
- **Run 2 was therefore already no-LoRA at 40 steps and CFG 4: the quality ceiling, reached
  without anyone testing for it.** The only control that moves the configuration is node
  168; flipping it true switches all three together to the 4-step speed floor.

**The floor then ran honestly, and it is not the degraded rung the ladder framing
predicted.** New bytes, new pixels — 99.9881% differ from the ceiling at residual p50 29 —
so it is a *different render*, not a softened one. Measured, its median chroma is **lower**
(1.27 against 2.20) and its background is **lighter and cleaner** (L 82.7 / C\* 1.64 against
73.3 / 2.24), landing closer to the cloud reference on both background axes than the
40-step run does. The chroma tail is a wash. The residual concentrates in the head and
horns, which is the region [E01](experiments/E01-facial-structure-ceiling.md) says decides
what the reconstruction can hold.

### ⚖ RULED: the 4-step floor is the configuration. `Enable 4steps LoRA?` = **true**.

**The Director, 2026-08-09**, on seeing the pair: *"node 168 … seems to have the most
contrast, which is needed. That's the winner."* Ruled, and the advisor did not object —
**the contrast claim was then measured and holds on every axis**:

| | figure tonal range (L p5–p95) | figure L sd | figure/bg separation | **interior shading gradient** mean / p90 |
|---|---:|---:|---:|---:|
| cloud Nano Banana 2 | 62.9 | 19.18 | 37.4 | 11.22 / 24.51 |
| ceiling — 40 steps | 61.4 | 19.79 | 26.6 | 9.79 / 23.43 |
| **floor — 4 steps** | **77.0** | **24.05** | **34.7** | **16.56 / 41.15** |

**+25% tonal range, +30% figure/background separation, and +69% interior shading gradient**
(+76% at p90) against the 40-step run — and it beats the cloud tool on interior gradient
while nearly matching its silhouette separation.

**This is not a taste axis for this hop, and that is why the eye was right.** Image-to-3D
infers depth from shading gradients; [E01](experiments/E01-facial-structure-ceiling.md)'s
founding failure was a flat grey-on-grey clay yielding 0.84% Canny edge pixels, so the
ControlNet constrained nothing. More interior gradient is more depth signal. **The eye
selected the property the reconstructor keys off — the property the advisor had not
measured until asked to object.**

⚠ **The cost inside the ruling, recorded because it is not free: at CFG 1 the negative
prompt is inert.** Node 168 true selects CFG 1 through switch 164, and classifier-free
guidance at 1.0 reduces to the conditional branch alone — the negative cancels, and ComfyUI
generally skips the uncond pass outright. So **the plinth and anti-ornament guards are not
armed in the shipped configuration.** The floor render came back clean regardless, which is
evidence about base behaviour rather than about the guard. A plinth is the one artifact a
reconstructor would faithfully rebuild as anatomy, so this is the thing to watch, and the
lever if it ever appears is node 155 — raise the 4-step branch's CFG to ~1.5–2 and the
negatives arm, at the risk Lightning distillations carry above their trained CFG. Untested,
one run, same seed.

**Ceiling and floor both stay in the record.** The ceiling (`14ffd0bd`, 40 steps, CFG 4) is
the armed-negatives configuration and remains available for a clay that needs it.

**The law**: *a widget is not an input* — the same family as *file bytes are not pixel
values*, and diagnosable only by reading the link topology, never the widget values. The
subgraph's outer widgets are stale in the same way: node 170 still shows a background-swap
prompt while the clay prompt is what executes.

## Licence — the open item on the CLOUD option, and the path that closes it

⚠ **The cloud option's licence is UNVERIFIED and no public claim rests on it.** The Comfy
consult channel called Nano Banana 2 "commercial-safe"; that is an assertion this repo has
not measured, and the studio's model KB structurally cannot settle it — it catalogues open
weights, and this is the chain's first closed-API candidate. **Unlike every licence
currently in the chain, a ToS can change under us where a weights file cannot.** Before any
public licence claim covers a Clay-ify-fed asset, one verification pass against Google's
live Gemini API terms, quoted and dated here.

**That item does not block anything, because the default no longer depends on it.** The
licence-correct model was neither of the two first proposed, and the selection was measured
against the studio KB (`E:\AI\readouts\model-knowledge\models.db`) rather than recalled:

| candidate | licence | commercial | verdict |
|---|---|---|---|
| **Qwen-Image-Edit-2511** | **Apache 2.0** | **yes** | **the target.** Instruction-edit, so it keeps the in-place editing that makes the current tool work; VRAM min 6 / rec 24 GB, fits the card; the KB's own note calls it the only top-tier editor that is unconditionally commercial-safe. It is also the stack this studio already runs |
| Qwen-Image-Edit-2509 | Apache-2.0 | yes | fallback, same posture |
| FLUX.1-Kontext [dev] | **FLUX.1 [dev] Non-Commercial** | conditional/no | **excluded.** This repo already excludes `nvdiffrast` on exactly these grounds, by a structural tripwire rather than attestation |
| SDXL + ControlNet + IPAdapter | OpenRAIL++ | yes | licence-clean and already in the chain, but img2img holds the subject less literally than an instruction edit — the weaker fit for a hop whose whole job is *keep pose, silhouette and identity* |

*This is the repo's own law firing a third time this session: **enumerate the resource
before commissioning one.** A binary choice was offered and the right answer sat outside
it.*

## What E29 must measure

1. **Gate 0 — the Director's eye** on concept | clay pairs at full size, several subjects.
   The sheet before the metrics.
2. **The arm that decides it:** image-to-3D on the concept vs. on its clay, everything else
   pinned, graded by the measurement server ([E27](experiments/E27-ruling.md),
   [E28](experiments/E28-ruling.md)) and by the Director's eye at Gate 1. Blind predictions
   first. This would make concept prep the measurement MCP's first consumer outside the
   polish arc.
3. **The local variant**, if built: the same subjects through Qwen-Image-Edit, compared
   against the cloud clays — which also settles the licence item by making it moot.

**A candidate subject is already in hand.** The minotaur is a humanoid×beast hybrid — a
genuinely new class beside the four accepted (humanoid, vehicle, beast, prop). The
alternative worth naming is W3's original concept: running *him* through a front door with
recorded provenance would close the oldest open loop in the repo, since his clay's unknown
provenance was one of the founding session's falsified claims.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | workflow id, model alias, seed, resolution, aspect and thinking level all recorded above, and the graph is saved server-side. **Not 3**: the model alias is server-versioned, so the pin identifies the request and not the weights — which is the reproducibility limit stated in the placement ruling, and the reason this is prep rather than a stage |
| ANDON_AUTHORITY | 2 | the hop cannot silently enter the route: promotion requires E29, and an accepted clay enters the recorded tree only with a hash. **Remediation, owner = E29:** a plinth/colour-leak check as an explicit gate rather than a walked observation |
| NAMED_COMPENSATORS | 3 | the only irreversible-ish act is a cloud generation that spends credits; the compensator is that outputs are curated and unaccepted clays are simply not staged. Nothing is written into the recorded tree by this hop — staging is deferred, and the reason is named |
| DECOMPOSE_BY_SECRETS | 3 | the hop is one subject-independent prompt; everything subject-specific stays where it already lives — the identity fixture and the profile. The fur-element observation is the boundary working as designed |
| UNCERTAINTY_GATED_HUMANS | 3 | the Director's eye is the acceptance gate for every clay, and the walk above is structured as deviations-in-words before measurements |
| EXTERNAL_VERIFIER | 1 | the walk was one seat's eye plus four descriptive statistics on **one pair**. **Remediation, owner = E29:** the reconstruction arm is the external verifier — the mesh either comes back better or it does not, and no amount of looking at the clay answers it |
