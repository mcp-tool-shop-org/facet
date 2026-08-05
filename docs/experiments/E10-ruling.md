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
