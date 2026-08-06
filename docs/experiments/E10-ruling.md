# E10 — the ruling document

Advisor rulings for the E10 arc, in the E04 pattern: rulings appended in place with dates
and reasons, corrections in place with the measurement that overturned them. The spec is
[E10-environment-contact-layers.md](E10-environment-contact-layers.md); the research
record is [RG02](../research/RG02-environment-contact-layers.md); the charter is
[E04-ruling.md](E04-ruling.md) Ruling 19.

---

## Ruling 1 (advisor, 2026-08-05) — RG02 is RATIFIED, the negative-finding trigger fired as designed, and the six collisions are decided. The spec amends before Step 0 exists — which is the cheapest correction there is.

### The research record and its gate

**RG02 is ratified: 11 of 11 DOIs independently re-resolved against Crossref** — the
citation gate that lost 28 of 32 on RG01 lost none, because the executor ran it rather
than trusting the agents that produced the citations, spot-checked the first return
before the others landed, and the one title discrepancy (Lu et al., published
*"Scalable…"* vs preprint *"Efficient…"*) was disclosed by its own agent before the gate
looked. The agents' honesty about weak sources (community-only BC7 claim; no
version-anchored UE page) is what the gate exists to produce. **The spec's
pre-registered negative-finding trigger fired on Q3 exactly as written** — *"if the
standard answer is shader-side, the layer's content may be simpler than painted water"*
— and the executor halted before Step 0 instead of building the architecture the
research had just undermined.

### The six collisions, decided

1. **The layer's content is the STATIC BOOT-TOP** — the painted band at the designed
   waterline, its own paint, fixed in hull coordinates, the half Q3 found precedented as
   art. **The foam-white lap line is STRUCK from W2's prompt**: dynamic wetting and foam
   are computed shader-side in every shipped source RG02 could read (Sea of Thieves'
   depth-buffer foam, Horizon's water-side vertex colour, AC3's runtime gunnel probes),
   and they belong to the *water's* material, not the hull's skin. Where UV-space art
   enters wetting at all it encodes **susceptibility, not appearance** (Lagarde's
   porosity × runtime WetLevel; Lekner & Dorf's wet darkening as a multiplier) — that
   path is recorded as the engine-side future if wet darkening is ever wanted, and it is
   not this arm.
2. **The commit mechanic is the MASKED PASTE — the spec's dichotomy had a third member,
   and it is the one the pipeline already implements.** The diff is dead twice over
   (Smith & Blinn: three equations, four unknowns even with the base known; PIE-Bench:
   a full-frame edit drifts outside its own mask at 17.87 dB, and the VAE round-trip
   alone is 24.7 dB) — but `texpass_iter` never diffed a frame; it commits inside a
   mask. The agent that raised this caveat against its own conclusion is why Phase 0
   was worth running.
3. **Alpha comes from the geometry, not the model.** With the foam gone shader-side,
   the boot-top's top edge is a painted line — a hard edge — and the contact mask IS
   the correct alpha. No model-generated alpha in v1; LayerDiffuse's
   rim-good/interior-bad asymmetry is banked as the gate-direction lesson (a boundary-
   quality gate would watch the direction generation is already good at — the andon
   belongs on the unwatched direction) and becomes moot for this arm by construction.
4. **The file contract is adopted as Q2 found it:** 8-bit **straight-alpha** RGBA PNG on
   the existing UV1, RGB in sRGB, alpha linear, never premultiplied; Godot
   `BaseMaterial3D` detail slot with `detail_enabled` as the runtime per-scene toggle;
   UE's compile-time static switch costs one material instance per state and is
   recorded as the asymmetry it is. sdlab's `encoding: "rgba"` is already legal —
   Ruling 19's "a layer channel role is a schema entry" holds, checked against code.
5. **The missing authoring step joins the spec as a gated export step:** colour
   dilated outward under transparent texels before export — the only mip-bleed
   mitigation available in both engines, and Godot documents no alpha-coverage mip
   preservation at all (a clean negative). The step carries its own check: the dilated
   ring exists and the alpha channel is untouched by it.
6. **`waterline_z` and W-H1 stand untouched** — every reading (boot-top, shader cutoff,
   porosity mask) needs the same number from the same eye. Step 0.1 is confirmed as the
   one item no ruling could have wasted, which is what made it safe to hold everything
   else.

### Ledger thirty-nine — mine, caught by the executor's sha discipline

E10's W-H3 and the handoff both named `atlas_final.png` — **W3's atlas filename, carried
across subjects by the advisor** in the very spec whose calibration section quotes the
enumerate-before-asserting correction. The accepted atlas is
**`E04_stroke\out\galleon_final.png`**, sha256 `65b4c6a3d5fb…`, and the spec is corrected
in place (Amendment 1). The base-invariance gate hashes the file that exists.

### Step 0 is CLEARED, and the watchdog needs no word from anyone

The kickoff's standing instruction already covers it — *verify the watchdog before any
local GPU step; restart only if stale; report either way*. **Restart it and proceed to
Step 0.1**: derive the candidate lines from the mesh (hull lower extent + the founding
exemplar's band top projected to z), render them, and the Director places the line in one
sentence. The exemplar's role is clarified by decision 1: it validates the band's
**geometry** (W-H1 unchanged — the model painted contact exactly where contact lives);
it is no longer a colour or content target, because what it painted was the dynamic half
that now belongs to the shader. Then Step 0.2–0.4 and the arms, per the amended spec.
The blob-bound halt is ruled in [E04-ruling.md](E04-ruling.md) Ruling 29 — the sentinel
translation at the export boundary; canon's null stands.

---

## Ruling 2 (advisor, 2026-08-05) — Task 1 CLOSED; the cam.json frame trap goes to the bundle as an exported function; the ladder goes to the Director

**Task 1 is closed better than ruled:** the sentinel **derived from the atlas's own
dimensions** rather than typed as a literal — it stays "the whole atlas" if the atlas
ever changes size, and a real derived integer in canon would pass through untouched.
That is the ruling's intent implemented one step more honestly than the ruling wrote it.
Manifest validates, canon's `null` intact, ingest untouched — the sdlab session's go is
now purely the Director's paste.

**Step 0.1's ANDON caught the fourth transcription.** `texpass_iter.load_scene()`
re-axes Y-up→Z-up and normalises by max-abs before any ray is cast — **every world
quantity in every `cam.json` this pipeline has ever written lives in that frame**, and
nothing outside the code says so. A consumer reading one against the raw GLB puts every
z on the wrong row while producing an entirely plausible sheet — which is precisely what
the projection check that could fail was built to catch, and it caught it at 206 px
before any number was believed. **Bundle item, named as proposed: one exported canonical
mesh-frame function, not a fifth transcription** — it joins the fit-axis three-copy
family it extends. The 0.34 px landing after the fix, the record's two exemplar
statistics reconciled to the digit (2,272 total vs 2,002 largest-CC, both bboxes now
labelled), and the sheet-legibility self-catch (an unreadable ladder rebuilt before it
reached the eye it was for) are endorsed as run.

**The ladder is ratified as built** — C at the exemplar's own band top, independently
landing at 7.43% of the figure against Ruling 20's "lower 7%" from the other direction;
A and B as a ruler, not thresholds; the 5% ticks so any sentence carries into a number.
**The gate is the Director's. Step 0.2 builds the mask the moment his sentence lands.**

---

## Ruling 3 (advisor, 2026-08-05) — THE WATERLINE IS PLACED: C. Step 0.2 is cleared.

**The Director's word: "I agree. C is the winner."** One sentence, exactly as the gate
was designed — the ship sits deep, properly loaded, at the line the model itself painted
when it did it uninvited.

**`waterline_z = −0.43095`, and the frame is named in the same breath as the value** —
the canonical mesh frame of `texpass_iter.load_scene()` (Y-up→Z-up re-axed, max-abs
normalised), which is Ruling 2's trap applied as discipline on the first value written
since it was named. Lands in `ship.json` with the full provenance: the Director's
placement on the candidate sheet; candidate C derived from the founding exemplar's band
top; cross-checked at 7.43% of the beam figure below it against Ruling 20's
independently-measured "lower 7% of figure."

**Step 0.2 is cleared:** the contact mask at the placed line, with the spec's anchors —
byte-stable across two runs, mask ⊆ silhouette exactly. Then Step 0.3 (the layer state,
base-invariance by construction against `galleon_final.png` at its recorded sha) and
Step 0.4 (the layer palette fixture, boot-top edition per Amendment 1), then Arm W1
measures the mask against the exemplar's band — W-H1's ≥90% prediction is still blind
and stays that way until the mask exists. **The next gate that needs anyone's word is
W3's toggle sheet, and the word is the Director's: does the ship float.**

---

## Ruling 4 (advisor, 2026-08-05) — anchor C's form is withdrawn on its own control (ledger forty); the mask gains the on-surface intersection; the route-wide inheritance becomes a bounded measurement, not a panic

### The halt is ratified, and the control is the star

The decomposition is exactly what a fired gate should produce: two populations, not one
number — 37.4% rim at ≤1 px, 62.6% **not on the mesh at all** at median 46 px — and the
decisive instrument was **the mesh's own vertices run through the anchor's exact check:
99.4506%, every miss exactly 1.00 px.** That is the works-perfectly test, run by the
executor against the advisor's anchor, and it returns the verdict: **the anchor cannot
be passed by the geometry it validates.** Also endorsed by name: the frame check *first*
(`pos.npy` is a **third** frame — unit-cube per-axis against meta lo/hi — anchored at
1.2e-06 / 5.9e-05 before a single number was believed, Ruling 2's trap applied as
reflex); the diagnostic kept out of the fired gate — *"adding a diagnostic to a gate
after watching it fire is how a gate quietly becomes whatever passes"* goes in the
record beside A32; and the consumer grep done before being asked.

**Ledger forty.** The spec's anchor line — *"mask ⊆ silhouette, exactly"* — specified a
containment property in a form (rounded-pixel membership in a binary mask) whose
correct-input score is structurally below 100%: a projected boundary point rounds one
pixel out, and the contact band hugs the boundary by construction. The works-perfectly
family, fourth member, written into the spec whose calibration section quotes the rule.

### Anchor C, replaced — derived from both sides of the line, the Ruling 16 shape

The property is containment; the honest form is **distance, not membership**: every
contact-mask texel's projection lands **within 1.5 px of the silhouette mask**. The
derivation owns both sides: the correct-input side is the rasterization rim quantum,
**exactly 1.00 px** (the control's every miss); the failure side is the off-mesh
population at **median 46 px, max 144**. 1.5 px sits above the rim quantum and 30×
below the signal median. Neither side is the fired number's to move — one is
rasterization arithmetic, the other is the defect the anchor exists to catch.

### Finding 2: the mask gains the on-surface intersection NOW; the route inherits a question, not a verdict

**E10-scoped, ruled:** the contact mask intersects with an on-surface predicate —
positions farther than **5 px** from the mesh are excluded (the executor's own measured
reporting cut; the separation is 0.006 px clean median against 46 px off-median, four
orders). This is **E08 A27 one layer down, applied at the mask's birth and scoped to the
layer machinery**: the trust question is only askable where surface exists, and paint on
no surface is the exact failure the layer must not inherit into its first texel.

**Route-wide, ruled as a measurement and not a fix:** 2.5065% of the bake's uv-valid
texels carry off-surface positions and five consumers inherit the unmeasured property.
The executor's restraint is adopted whole — **no accepted number is claimed wrong**, and
both accepted assets passed the gate that actually rules here, the Director's eye on
artifacts. The dispatch, queued **after Arm W1** (read-only, one session, no route
change without its own ruling): per consumer, does excluding the off-surface 2.5% move
your headline number — priority by blast radius: `e08_ceiling`/`e08_acceptance` (the
quoted figures) → `texpass_finalize` (56.24% of the accepted atlas) → `project_twins`/
`commit` (the acceptance stage). Corrections in place with the measurement if any number
moves; silence in the record if none does.

**The bundle item widens:** the exported canonical-frame module now covers **all three
frames** — raw GLB, canonical mesh frame, and `pos.npy`'s unit-cube — one module, the
transforms and their documentation, replacing every per-tool transcription.

### Sequence

Re-anchor Step 0.2: A and B stand as passed; **C in its replaced form** over the
intersected mask; D runs. Pre-stated: if C still fails after both corrections, that is a
new finding and a halt — nothing else gets tuned. Then Step 0.3 (layer state), Step 0.4
(boot-top palette fixture), Arm W1 — whose ≥90% prediction stays blind. The next word
anyone needs remains the Director's, on W3's toggle.

---

## Ruling 5 (advisor, 2026-08-05) — Steps 0.2 and 0.3 RATIFIED; the boot-top fixture is authored; the beam is pre-registered as the toggle's legible view

### The re-anchor: ratified, with the two numbers that matter named

**1.414 is adjudicated as arithmetic, not defect** — √2 is the Euclidean distance
transform's diagonal-neighbour quantum, which is exactly why Ruling 4 set the bound at
1.5: above the rim quantum, thirty times under the signal. And **the control-match is
the correction's proof**: strictly-inside 99.4327% against the mesh's own vertices at
99.4506% — *the mask scores what the geometry scores*, which the withdrawn form was
structurally unable to report. Anchor D's first run (0 px outside the silhouette on all
three cameras, band top within 1 px of the placed line, through an independent path) is
the cross-check the family needed. 2,487 off-surface texels excluded at the birth of the
mask — A27 one layer down, working.

### Step 0.3: the best kind of invariant, and the proof that costs nothing was run anyway

**Base-invariance turned out structural** — `commit` writes only into `--state`, so the
accepted atlas is never opened for writing at all. That is CLAUDE.md's own preference
order realised: *prefer eliminating a risk to gating it* — and the `--base-guard` then
proves what the construction guarantees, no skip flag, demonstrated able to fail before
being trusted. **The regression proof is the leg's best move**: all six shipped commits
re-run through the *modified* tool, final atlas byte-identical, every per-stroke count
equal, every sidecar and both base assets sha-identical. The change is neutral on the
shipped path — proven, not asserted, which is what touching the tool that made both
accepted assets required.

### The boot-top fixture, authored (Step 0.4's content — the executor lands the file)

One element, its own noun phrase, the Amendment-1 grammar:

> **L1 — a weathered tallow-white hull coat below the waterline** — the period "white
> stuff," its top edge forming the painted line at the placed waterline.

Grounds: it is what the static half of a period waterline *is*; its pale warm register
sits **inside the ship's existing warm band** (no new palette band needed — the layer
fixture declares the warm band's pale end, report-only, bounds null per the standing
pattern); and it **contrasts with the dark foot planking** (the re-roll's tar at h 43,
L\* ~10), which is what makes W3's toggle legible — the experiment's own gate favours a
coat the eye can see arrive and leave. The founding exemplar's blue-grey is explicitly
NOT the target (Amendment 1: it painted the dynamic half). **The Director's one-sentence
window is open as always** — if he wants tarred black below the line, or a black
boot-top stripe above the coat, either is an authoring sentence; default is the
tallow-white coat. W2's prompt takes the element phrase verbatim.

### Pre-registered for W3, so a panel is not misread

**The hull hides its own waterline from 40° of elevation** — the band renders 22,106 px
from the beam and only 789 / 770 px from the deck pair. The beam view is where the
toggle is legible and where the Director's eye should rule; the deck panels showing
almost no band is geometry, not a layer failure, and it is priced here before any
generation exists.

### Sequence

Layer-state seed (alpha from the contact mask at export, per Ruling 1 decision 3 — not
carried through painting) → the fixture file lands as authored above → **Arm W1**, the
≥90% prediction still blind → W2, one authored stroke, **beam view** (the visibility
observation confirms the spec's own choice) → W3's toggle to the Director.

---

## Ruling 6 (advisor, 2026-08-05) — W-H1 CONFIRMED at 100.00% blind; the pre-flight found E10's primary finding: the profile was single-lane. The second lane is ruled in.

### W-H1: CONFIRMED, and it is the experiment's foundational claim landing

Pre-registered ≥90%, genuinely blind, measured: **100.00% of the exemplar's largest
component, 99.96% of its total — one pixel of 2,272 outside.** Every pixel the model
painted freehand — uninvited, on a rejected twin, killed by one seed increment — falls
inside the band a plane through the Director's placed line cuts out of the geometry.
**Contact is geometry's job**; the model's freehand water was evidence of *where*, and
the plane recovers the where exactly. The anchor that makes the number meaningful is
endorsed by name: emitted silhouettes byte-identical to the exact clay masks on all
eight views, so exemplar and render are provably the same picture; mirror-pair extents
agreeing to 5–7 px. The colour disclaimer stands as written — extent only, per decision
6; nothing here endorses blue-grey.

### Steps 0.3 and 0.4: ratified as landed

Re-seed byte-identical, base sha unchanged. Both canon fixtures landed as authored —
and **the palette fixture's chroma-floor note is endorsed as the W3-blade lesson
pre-applied**: a tallow coat is low-chroma by construction, so runs report the
below-floor share rather than letting the gate count a pale coat as off-palette. The
staged W2 design — the layer rendering as the ship (atlas copied from the accepted
base for context and registration) with the only paintable region the geometric band —
is the right shape: the brush sees a ship, and geometry decides where paint may land.

### The pre-flight halt: the guard is RIGHT, and the finding is E10's primary one

The check refused a generative step on a prompt file the subject never declared — which
is precisely what Ruling 24 built it for — and in refusing, it measured the boundary:
**the profile's vocabulary was single-lane.** One `brush_prompts` slot per subject; E10
introduces a second content lane over the same subject; the galleon now legitimately
owns two prompt fixtures and the profile can name one. That is the
DECOMPOSE_BY_SECRETS test firing one level up from where E04 fired it, and it is
recorded as a primary finding, not a defect: the profile design predates the existence
of layers. The executor's refusal to edit either the decided value or the no-skip
gate's definition of legal *while holding a run they wanted to fly* is endorsed by
name — that restraint is the whole reason the gate still means something.

**The ruling:**

1. **`_fixtures.layer_prompts` joins `ship.json`** (this ruling's commit): path
   `docs/experiments/E10-layer-prompts.json`, with why and from. Two lanes, two
   declared homes, one subject.
2. **The pre-flight learns lanes EXPLICITLY, never by inference:** `brush_cloud_step`
   gains `--lane {base,layer}`, **defaulting to base** — the character and E04 paths
   are unchanged by construction. The lane→fixture mapping is fixed in the tool
   (base → `brush_prompts`, layer → `layer_prompts`); the check fires against the
   mapped key **always, no skip flag in either lane**. A guard that infers its own
   jurisdiction from a path can be steered; the lane is a declared input.
3. **The declaration is corroborated against the job**: the pre-flight asserts the job
   directory's state identity matches the declared lane — the emit sidecar already
   carries it, so a mis-declared lane halts on data in hand, not on trust.

### Sequence

Profile edit lands (this commit) → `--lane` lands with its two-lane check and the
corroboration → pre-flight green on `--lane layer` → **W2 flies: one authored stroke,
the beam, L1 as the only variable** → commit under restrict + base-guard → **W3's
toggle sheets → the Director: does the ship float.**

---

## Ruling 7 (advisor, 2026-08-05) — the MECHANISM is confirmed under real fire; W-H2 is FALSE as run, the record predicted it, and ledger forty-one is mine. W2b is cleared now.

### What the run proved — every infrastructure claim of E10, at once

**W-H3 and the whole machine are CONFIRMED**: base `galleon_final.png` byte-identical
through a real generative commit with the guard asserting *inside the tool* · `--restrict`
exact (0 texels outside the contact mask) · alpha from geometry (moved 0 px) · the
dilation ring flooded under transparent texels · the composite verified exact as `over` ·
invar on the geometry operand at 5 px against the 200 bound · 0 credits, full transport
discipline, the invented-negative caught and corrected to the spent string **before**
anything flew (the one-variable rule applied to one's own fixture — endorsed by name).
The toggle visibility numbers land exactly on Ruling 5's pre-registration. **The layer
system works. What failed is one prompt's content, and the two must not be conflated.**

### W-H2: FALSE as run — and ledger forty-one is the reason it was predictable

The band came back **darker than the hull it painted over** (L\* 4.0 against the base's
7.9, hue 55.8 — the tar family), and the chroma guard fired *right for the wrong reason*,
exactly as the executor put it: 81.38% below the floor because the coat is nearly black,
not because it is white. **The house grammar predicted this and neither the fixture's
author nor the ruling that ratified the prompt carried the prediction into the arm — the
author was me, twice.** A15's law: *a specification cannot add a second element to an
occupied surface.* The render the model saw showed the band fully occupied by accepted
dark planking; L1 was an **addition onto occupied surface** — the W3 fur-cuff's ΔE 1.07
class, G7's class — and the sharpest fact is already in E04's record: **stroke 1 painted
this exact region dark tarred planking with this exact ship string, and was accepted for
it.** The string plus the context both name dark; L1 arrived as the thirteenth voice.
**Ledger forty-one, the same form as ledger twenty-three one seat over**: the fixture's
own Form section predicts additions drop, and L1 was an addition the moment the layer
seeded from the painted base.

### W2b, ruled and CLEARED — one variable, the lane's own rule applied

**The layer lane's prompt fixture becomes L1 + the style tail + the backdrop — the
incumbent ship materials are struck from the layer lane.** The per-view rule, applied at
lane scope: *describe what THIS stroke paints* — and the layer paints one element. The
lane split makes this principled rather than convenient: **each lane's prompt carries
that lane's identity** — the ship's twelve elements ride the base lane, the coat rides
the layer lane; the render and control carry the ship's context without the text
re-arguing for the incumbents. One decided object changes (the lane's fixture, updated
in place with the history); graph, seed discipline, mask, transport all held constant;
0 credits.

**Pre-registered readings:** the coat arrives (band L\* rises decisively above the
base's 7.9, above-floor share flips majority, hue stays warm-pale) → W-H2 confirms on
the second run and **W3's toggle goes to the Director**. Still dark → **W2c**: the band
rendered as HOLE in the emit (unoccupied — the brush's entire successful history is
painting absence), W2b's prompt held constant — the render-side lever, one variable
again. If W2c also fails, halt: the arm has a real finding about masked inpainting over
context, and it gets written up as one.

### The Director's gate is deferred, not skipped

The sheets exist and the measurement already answers them — there is nothing new for
the ship to float on, and his eye is for outcomes, not for confirming a ΔE table. The
toggle goes to him when a candidate coat exists. The executor's closing sentence is the
right shape of a negative result and is kept: *reported, not diagnosed.*

---

## Ruling 8 (advisor, 2026-08-05) — three arms falsify W-H2 in brush mode with clean attribution; the finding is named; the next arm rides the mode the record already measured. Ledger forty-two is mine.

### The ladder is ratified as the cleanest attribution work of either arc

One variable per arm, **proven by field-level diff before submission** (W2→W2b: node
7's text only; W2b→W2c: node 9's image only); the mask byte-identical across all three
arms **proven by the content-addressed name**, not inferred; W2c's hole colour
**measured, not chosen** — 1,963,858 of 1,963,858 accepted hole texels at
rgb(107,107,107), so white would have steered toward the answer and grey is the
precedent. And the self-caught measurement error is endorsed by name: the +37.3
"triumph" that was **the fill, not the paint** — a denominator correct under base-copy
seeding and silently wrong under hole-fill, caught before it was believed, with the same
defect then **flagged in `e10_layer_export.py` and not patched** — *"a real tool defect
belongs in a ruling, not a quiet edit at the end of a failing arm"* is exactly where
that line belongs.

**The export defect is ruled fixed here:** the owned set is `contact ∩ styled_mask` —
what the commit actually wrote — never `changed vs base`. Anchor: W2's export re-run
under the fixed predicate must reproduce its recorded output byte-identically (under
base-copy seeding the two predicates coincide, so the fix is behaviour-preserving where
it already ran and correct where it hasn't).

### The finding, named — and it is a finding about objectives, not a defect

| arm | prompt | context | painted L\* | ΔL\* |
|---|---|---|---|---|
| W2 | L1 + twelve | occupied | 4.0 | −3.9 |
| W2b | L1 only | occupied | 3.9 | −4.1 |
| W2c | L1 only | hole grey | 5.5 | −1.6 |

Target: L\* in the seventies. Striking twelve competing elements moved 0.1; replacing
occupied context with absence moved 1.6 — the largest lever, still the wrong direction.
**The brush is built to continue an asset — anchoring, context, consistency are its
design goals — and the layer's coat demands departure from context. Three arms measured
the tool doing its designed job on the wrong objective.** The three mechanism candidates
(surround conditioning, 2.3% frame share, the LoRA's dark register) stay recorded as
untested: the next arm does not need the why, and diagnosing a mode we are leaving is
spend without a consumer.

### Ledger forty-two — the record held the answer while I specced the question

**The repo already measured where new materials win: full-frame twin generation, where
the prompt beat incumbent materials 8 of 8 at 7.4× separation** (the E08 contradiction
test) — and where G7's red and G13's unprompted gold actually arrived. I routed the
layer's content through the brush — the mode with zero such evidence and an opposite
objective — for two rulings, with the contradiction result quoted in my own E04 close.
The pivot below is a return to the measured mechanism, not an invention.

### W2d, ruled and CLEARED: the layer's content comes from a twin, projected under the mask

1. **One beam twin with L1 appended to the ship string** — own noun phrase, the standing
   grammar, everything else byte-held to the twin recipe. The full-frame mode paints the
   hull's foot *fresh*, so L1 competes as an occupant, not an addition.
2. **Measure the landing first** — the band's colour in the twin, the existing table
   machinery, before anything projects. Bounded: **two generation tries** (seed
   increment second), then halt — a no-land after two is a finding about L1 as an
   element, and the re-authoring window (tarred black coat, pale boot-top line — the
   prior-compatible alternatives) is the Director's, presented with the evidence.
3. **If landed: project the band only** — the projection machinery pointed at the layer
   state under the contact-mask restriction, base untouched by construction, trust ∧
   geometry as everywhere. Any expressibility gap this needs is a primary finding under
   the standing test, reported not improvised.
4. Then the fixed export → composite → **the toggle to the Director**.

0 credits expected throughout; every transport discipline standing. The mechanism
already survived three live fires — this arm changes only where the paint comes from.

---

## Ruling 9 (advisor, 2026-08-05) — W2d LANDED on the first try. W-H2 CONFIRMS in the measured mode; the contrast is the proof; the toggle goes to the Director.

### The landing, and why the contrast matters more than the success

One field against E04's accepted twin_0 — node 7's text, proven by diff, both inputs
proven byte-identical by content-addressed name. **Band L\* 13.8 → 47.1 (+33.4), the
whole figure at ΔE median 4.34** — the ship survived and the change concentrated where
it was asked for. **The diagnosis is confirmed by the contrast, not merely the
success**: same element, same words, same seed, same LoRA — inpainting three ways
returned −3.9 / −4.1 / −1.6, and full-frame returned **+33.4**. The mode was the
variable all along. **W-H2 CONFIRMS as restated by Ruling 8**: one authored generation
produced a waterline where eight rolled twins produced zero — in the mode where the
prompt is measured to win. Banked for every future layer and for E10's close: **new
materials enter through full-frame generation and reach the layer by masked
projection; inpainting continues, it does not introduce.**

### The rest of the leg, ratified

The projection path taken through the right tool's contract (`project_twins --view 0=`,
unchanged), the paste under the contact mask with the guard inside the tool — 6,564
texels, one beam view's physical share, **223,872 projected texels outside the band
discarded, not banked**. The export predicate fixed exactly as ruled with its anchor
run — `predicate_disagreement 0` on the path where the predicates must coincide,
*checked, not reasoned*. Base byte-identical through projection and paste; ring
present; alpha 0 px; composite exact; the toggle's per-view visibility landing on
Ruling 5's pre-registration a third time. In the layer: ΔL\* +41.4 at hue 97.7, 86.68%
of above-floor texels inside the warm-pale band the fixture declared **before any of
this ran** — the non-circular gate doing its job on the first content it ever judged.

### To the Director, with the two flags carried honestly

The toggle sheets go to his eye with the executor's flags attached, not smoothed: **the
coat covers 6.7% of the band** — one view's share; seven cameras' worth of coat is
unbuilt, so this is the beam's proof of mechanism, not the finished waterline — and
**the top edge runs ragged in places at 3×**. His gate is the one W-H4 pre-registered:
*does she float.* His readings, pre-stated so one sentence suffices: **yes** → the
full-coverage build is the follow-on (remaining views through the same twin→project
path, then the finished toggle); **no, because of the raggedness or the colour** → the
edge treatment and the coat's register are the next arm's variables, with his words as
the targeting data; **no, wrong idea** → the layer stays a proven mechanism awaiting a
better element, and E10 closes on its architecture findings — which are already worth
the arc.

---

## Ruling 10 (advisor, 2026-08-05) — the Director's verdict: IT DOES NOT READ. Two ledger entries are mine, and the second is the finding: the gate was aimed at an artifact that cannot pass it at perfection.

**The Director, on the toggle: "How is that supposed to be a waterline? I'm confused
right now, do you not see that?"** Recorded as the verdict it is. And on looking — for
the first time, which is the first entry — the advisor agrees: the layer-on panel reads
as a ship with a cream-painted bottom, fully visible, on grey. Not a floating ship.

**Ledger forty-three: the advisor presented a gate artifact unviewed.** E07's founding
lesson — *build the sheet before the metrics, and look* — violated at the advisor's own
seat: the toggle went to the Director's eye carrying measurements (+33.4 L\*, all true)
in place of a look. The Director's question — *"do you not see that?"* — had the honest
answer *no, I had not looked.* The rule was always subject-independent; it is now
seat-independent too.

**Ledger forty-four, the works-perfectly test at ARM level: W-H4's artifact class
cannot produce a floating ship at perfect execution.** A ship reads as floating when
the water *hides* what sits below the line — that is what floating looks like. The
coat-only toggle paints the below-water hull pale and **leaves it fully visible**: more
of what should be hidden, highlighted. A perfect boot-top on a waterless render is a
dry ship with a painted bottom. **RG02's Q3 had already assigned the water to the
scene** — *the dynamic band is computed shader-side; the meeting line belongs to the
water's material* — and the advisor pointed the float question at the hull-side half
anyway, one ruling after ratifying that research.

### The correction: the float question gets the artifact it actually needs

**The sea-occlusion composite, dispatched now:** at the ortho beam view, the placed
plane's projection is exact — every pixel below the waterline's projected row is
underwater. A sea surface rendered (or composited) at `waterline_z`, occluding the hull
below it, IS the "does she float" picture — **zero generation, minutes of work, and the
contact machinery already built is precisely the engine contract**: `waterline_z` +
the below-line predicate are what a game's water plane consumes to do this per-frame.
The demo goes back to the Director's eye as the true W-H4 artifact.

### What stands, unbowed by the miss

Every mechanism finding survives untouched: base-invariance under live fire · the
two-lane profile vocabulary · alpha-from-geometry and the export contract · the
inpainting-continues / full-frame-introduces law with its 8-arm evidence · the placed
`waterline_z` and the contact mask, which are exactly the scene-side inputs the true
demo consumes. **The boot-top coat demotes to an optional hull detail** — real
shipyard practice, visible in dry dock or heel, the Director's to want or not once
the true float demo is in front of him; its one-view ragged state builds out only if
wanted.

---

## Ruling 11 (advisor, 2026-08-05) — the composite is RATIFIED and the advisor has looked at it; the product contract is stated in the Director's own terms; the coat's submersion is the spec correction it implies

### The Director's question, answered as the ruling's first duty

*"Should we be seeing the actual water? I thought we were just hiding the bit that
would be in the water, not adding the water itself. How would this even work as a
glb?"* — **his instinct is the architecture.** Nothing adds water to the asset, ever.
The composite's blue is a stand-in for the game's own sea, drawn in a demo picture so
an eye can judge the placed line. **The product contract, stated plainly: the GLB ships
whole — bottom included, painted — plus one number, `waterline_z`, in the profile and
the asset manifest.** The engine's water surface sits at that height and hides
everything below it by ordinary depth testing, per scene, per frame, for free. The
bottom stays in the GLB for the same reason E06 excluded faces from the atlas instead
of deleting them: a dry dock, a beaching, a heavy heel — some camera may someday see
it, and a scene's water must never be baked into an asset. Hiding is the scene's job;
the asset's job is to carry the line.

### The composite, ratified — and looked at, per ledger forty-three

All four anchors hold, including the line row reproduced at 0.00 px across two tools
and two sessions, and **the placed line's third independent confirmation** (7.43% of
the beam figure below it, pixels agreeing with mesh z-fractions). P3's miss is
recorded as the executor reported it — the fill used the measured value, not a
corrected one. **The advisor's own read of the sheet, on the record:** she contacts
the water continuously over 63.9% of her length; bow and stern ride above it as a real
hull's overhangs do — the grey between them and the sea is *air above the waterplane*,
correct at a view where the sea surface is edge-on and shows as a single row. The
presentation is two flat fields — a naval-architecture diagram, stark by construction,
recorded as a property; the in-engine version inherits waves, sky and perspective from
the scene. Whether she floats is the Director's sentence, and this time the sheet
reaches him with the advisor's eyes already on it.

### The coat's submersion — the finding becomes the spec correction, parked with its owner

**94.28% of the W2d coat sits underwater by construction**: the contact mask is
`z ≤ waterline_z` and a band confined to it is submerged the moment water exists — a
real boot-top *straddles* the line. Ruled: if the boot-top is ever built out, **its
band is the placed line grown upward by a hull-derived height** (a fraction of
freeboard, derived not guessed), its own small spec amendment at that time. The coat
stays parked as an optional detail pending the Director's word after the float demo —
nothing builds unbidden.

### Infra, flagged to its owner

The watchdog died by a **new mechanism** — the loop crashed on a file lock over its
own heartbeat file — the third hard death of the arc. Flagged to the watchdog-robustness
thread outside this repo (E04 Ruling 2's task owner); the standing restart authorization
covers any session needing the GPU; this leg was CPU-only throughout.

---

## Ruling 12 (advisor, 2026-08-05) — "THAT LOOKS ABOUT RIGHT." W-H4 confirms against a photograph of a real galleon. E10 CLOSES.

**The Director ruled the float demo against a reference photograph of a real galleon
under way** — his words: *"that looks about right."* The photo is the ruling's free
cross-check: the real ship shows contact amidships, bow and stern riding above, and
foam breaking at the line — the sitting-depth half is what E10 built, and the
foam-and-wake half is exactly where RG02's research put it: the scene's water, computed
per frame. The placed line now carries four confirmations — the exemplar's band, the
mesh z-fraction, the pixel measurement, and the Director's eye against reality.

### The hypotheses, scored at close

| # | verdict | the number |
|---|---|---|
| W-H1 | **CONFIRMED, blind** | the geometric band contains 100.00% of the exemplar's largest component, 99.96% of its total — contact is geometry's job |
| W-H2 | **falsified in brush mode, confirmed in twin mode — the law is the finding** | −3.9 / −4.1 / −1.6 across three inpaint arms; **+33.4** full-frame, one field changed. *Inpainting continues; full-frame introduces; layers fill by masked projection* |
| W-H3 | **CONFIRMED under live fire** | base byte-identical through four generative commits and two projections, asserted inside the tools, zero violations |
| W-H4 | **CONFIRMED in the Director's sentence** | "that looks about right," ruled against a real galleon |

### What ships — the contract, in the Director's own terms

The GLB, whole — bottom included, painted — plus **one number** (`waterline_z`, in the
profile and the asset manifest) the scene's water consumes to hide the underwater body
per frame. Optionally: the layer PNG (straight-alpha RGBA on UV1, the Q2 contract) for
anything the hull wears at the line. Nothing about water ever enters the asset. **The
generalisation the Director asked for on day one is banked as the pattern**: a contact
query + a layer state + the introduce-by-full-frame/fill-by-projection law — snow on
boots, mud on wheels, moss on ruins are the same three pieces with a different query.

### Parked and queued at close, none opened

The boot-top coat (if ever built: the band **straddles** the line by a hull-derived
height — Ruling 11) · the deck-view occlusion's depth-test form (named, unbuilt) ·
**Ruling 4's `pos.npy` off-surface consumer measurement — the next facet dispatch
candidate** (read-only, queued since the mask's birth) · the shared-code bundle, now
seven items · the sdlab asset-2 ingest, staged and validated, awaiting the Director's
paste in that lane.

**E10's cost: four generations, zero credits, one day.** The ledger closes the arc at
forty-four entries — six of them E10's, and every one of the six was caught by an
executor or a control before it cost an outcome. The arc began with the Director
saying *"the data that we'd learn from making that work could be applied to other
models in the future"* — that sentence is now a measured law, a schema, and a number
riding in a manifest.
