# Concept prep — the clay hop

**Status: a STAGED CANDIDATE with a Gate 0 walk recorded. It is not a route stage, and
nothing in the record depends on it yet.** Built by the Director, 2026-08-09; walked and
designated by the advisor the same day. The experiment that would promote it is **E29**,
queued behind [E28](experiments/E28-instrument-census-kickoff.md)'s close.

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

## Licence — the open item, and the path that closes it

⚠ **The cloud variant's licence is UNVERIFIED and no public claim rests on it.** The Comfy
consult channel called Nano Banana 2 "commercial-safe"; that is an assertion this repo has
not measured, and the studio's model KB structurally cannot settle it — it catalogues open
weights, and this is the chain's first closed-API candidate. **Unlike every licence
currently in the chain, a ToS can change under us where a weights file cannot.** Before any
public licence claim covers a Clay-ify-fed asset, one verification pass against Google's
live Gemini API terms, quoted and dated here.

**A local variant would retire that item entirely, and the licence-correct model is not
either of the two first proposed.** Measured against the studio KB
(`E:\AI\readouts\model-knowledge\models.db`) rather than recalled:

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
