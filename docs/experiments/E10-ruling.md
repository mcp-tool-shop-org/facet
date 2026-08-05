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
