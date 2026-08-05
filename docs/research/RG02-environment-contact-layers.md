# RG02 — environment-contact layers: research grounding for E10 Phase 0

**Status: CITATIONS VERIFIED. FINDINGS NOT RULED.** Executor session, 2026-08-05, running
[E10](../experiments/E10-environment-contact-layers.md)'s Phase 0 as written: three
questions, parallel agents, Crossref-first citation gate. This is a research record. It
reports what the sources say and where they collide with the spec. **It decides nothing** —
Phase 0's whole purpose is to reach the advisor before the architecture locks, and two of
the three answers are the kind the spec pre-registered as reasons to change it.

## The citation gate, run independently of the agents that cited

RG01 is marked UNVERIFIED to this day because 28 of its 32 citations died to arXiv
rate-limiting from one IP in one window (Ruling 1's standing correction). This dispatch put
Crossref first and every academic citation was then **re-resolved by this session against
`api.crossref.org`, not trusted from the agent that produced it** — a different process
reading the registry, which is the cheap half of EXTERNAL_VERIFIER.

**11 of 11 DOIs resolved, title and authors matching the claim.**

| DOI | resolved as |
|---|---|
| `10.1145/237170.237263` | Smith, Blinn — *Blue screen matting* — SIGGRAPH 1996 |
| `10.1145/800031.808606` | Porter, Duff — *Compositing digital images* — SIGGRAPH 1984 |
| `10.1109/CVPR52734.2025.02164` | Wang, Cao, Yu — *Towards Enhanced Image Inpainting…* — CVPR 2025 |
| `10.1145/3658150` | Zhang, Agrawala — *Transparent Image Layer Diffusion using Latent Transparency* — ACM TOG 2024 |
| `10.1109/ICCV51701.2025.01393` | Dai, Li, Zhou — *Trans-Adapter…* — ICCV 2025 |
| `10.1016/j.patcog.2025.112972` | Lu, Lu, Huang — *Scalable portrait matte creation…* — Pattern Recognition 2026 |
| `10.1145/3203185` | Yuksel — *Alpha Distribution for Alpha Testing* — PACMCGIT 2018 |
| `10.1145/3214745.3214820` | Ang, Catling, Ciardi, Kozin — *The technical art of Sea of Thieves* — SIGGRAPH 2018 Talks |
| `10.1364/ao.27.001278` | Lekner, Dorf — *Why some things are darker when wet* — Applied Optics 1988 |
| `10.1007/978-3-7091-6809-7_24` | Jensen, Legakis, Dorsey — *Rendering of Wet Materials* — Rendering Techniques '99 |
| `10.1145/2897839.2927409` | Kryachko — *Sea surface visualization in World of Warships* — SIGGRAPH 2016 Talks |

One discrepancy was **disclosed by the agent before I checked it**: Lu et al.'s published
title is *"Scalable portrait matte creation…"* where the preprint (arXiv:2501.16147) reads
*"Efficient…"*. Crossref confirms the published form. Disclosed, not papered over.

Sources that are **not** literature are labelled as such below and carry no DOI: engine
documentation (`[DOC]`), industry talks and slide decks (`[TALK]`), studio blogs and artist
interviews (`[COMMUNITY]`). Documentation asserting a mechanism is **documented, not
measured**, and is not upgraded by being quoted here. Three sources were unreadable behind
paywalls (Kryachko's body; the Atlas GDC 2019 and Black Flag GDC 2014 talks) and **no
technique is attributed to them**.

---

## Q1 — layered/decomposed generation: what commits into the layer

**Decides:** Arm W2's commit mechanics — (a) generate the layer directly with alpha, versus
(b) generate a full-frame edit and recover the layer by diffing against the base.

**The answer is against (b)-as-diff, and the strongest half is arithmetic rather than
empirical.**

1. **Smith & Blinn 1996, *Blue screen matting*** — with the backing colour *known*,
   `edit = αF + (1−α)·base` is still **three equations in four unknowns**; an exact solve
   needs a second known backing or a channel constraint. A diff must assume α = 1 wherever
   it is non-zero — and that assumption fails exactly where a waterline is fractional.
2. **Porter & Duff 1984** — `over` and premultiplied alpha are the form in which
   compositing and filtering are linear. Corollary for (b): `edit − base = α(F − base)` is
   a *premultiplied difference*, not a colour; compositing it back with straight-alpha
   semantics is a second error stacked on the first.
3. **Ju et al. 2024, PIE-Bench** (ICLR proceedings; no Crossref DOI found) — 700 images,
   human-annotated masks: background preservation **outside** the mask is PSNR **17.87 dB**
   for DDIM inversion + Prompt-to-Prompt, **27.22 dB** after their fix. A full-frame edit
   does not leave the untouched region alone.
4. **Wang et al. 2025 (ASUKA, CVPR)** — the VAE "not only noticeably degrades high-frequency
   details but also shifts in colors"; Gradient@edge 63.844 → 47.753 (MISATO 512²). Error
   concentrates at the mask boundary.
5. **Podell et al. 2023 (SDXL)** [UNVERIFIED: no Crossref DOI] — encode→decode round trip
   alone is PSNR **24.7 dB** on COCO2017 val 256². A no-op generation already returns pixels
   ~24.7 dB from its input, so any diff threshold must clear the autoencoder before it means
   anything.
6. **Zhang & Agrawala 2024 (LayerDiffuse, TOG)** — RGBA-native generation trained on ~1M
   transparent layer pairs; users preferred its output over SD+matting pipelines at
   **97.1 ± 1.9%**. Supports (a) — but this is a *preference* number, and the paper reports
   no PSNR/FID for the transparent-VAE round trip and no numeric alpha accuracy.
7. **Dai et al. 2025 (Trans-Adapter, ICCV)** — the masked-generation-into-a-layer case
   exactly: composite→inpaint→matte "struggles to preserve transparency consistency" with
   "jagged edges along transparency boundaries." AEQ 0.9872 vs 0.9828/0.9859; LPIPS 0.0434
   vs 0.0461/0.0453. Supports (a), but the margins are ~0.4 pt and ~6%.
8. **Lu et al. 2026 (Pattern Recognition)** — LayerDiffuse's mattes show "fine alpha along
   edges but significant errors in regions of absolute foreground or background."

**The finding this session did not expect, and the one with teeth:** #8 says RGBA-native
alpha is reliable **at the rim and unreliable in the interior** — the opposite of the
assumed failure mode. A layer gate written on boundary quality would watch the direction the
generation is *good* at. That is this repo's own lesson — *put the andon on the direction
the invariant does not bound* — arriving from outside it.

**The caveat that keeps (b) alive, raised by the agent against its own conclusion:** nothing
here shows a masked edit cannot be made exactly base-preserving outside the mask **by
pixel-space paste**. Findings 3–5 measure what *unconstrained* editors do. facet's
`texpass_brush`/`texpass_iter` commit is already a masked paste, not a frame diff, so the
variant actually on the table — call it (b′) — inherits only findings 1, 4 and 5's *in-mask*
consequences. **The spec's dichotomy has a third member, and it is the one the pipeline
already implements.**

---

## Q2 — the layer's file contract in Godot 4 and UE5

**Decides:** the layer's file contract and its E09/sdlab channel role. Everything here is
`[DOC]` unless marked otherwise — documented, not measured.

**The contract, as the documentation gives it:**

- **Pixel format** — 8-bit RGBA PNG, same dimensions and same UV space (UV1) as the base
  atlas. UE's `srgb` flag "can only be used with 8-bit and compressed formats," so a 16-bit
  or float layer silently forfeits it.
- **Alpha convention** — **straight/unassociated, linear**. PNG 3rd Ed. (W3C Rec., 24 June
  2025) §4.3: "Gamma correction is not applied to the alpha channel… Alpha samples… represent
  a linear fraction of full opacity"; §6.2: "The color values in a pixel are not
  premultiplied." Godot's `process/premult_alpha` stays **off** (it pairs only with
  `BLEND_MODE_PREMULT_ALPHA`).
- **Colour space** — RGB sRGB in both; Godot plain sRGB import, UE `srgb = true`.
- **Consumption** — Godot `BaseMaterial3D`'s detail slot: `detail_albedo`'s alpha is used as
  a mask "even when the material is opaque," `detail_uv_layer` selects UV1/UV2. The base
  material stays `TRANSPARENCY_DISABLED`; **the per-scene toggle is the runtime boolean
  `detail_enabled`**, not a second draw pass.
- **The toggle is asymmetric between engines.** UE's `StaticSwitchParameter` "cannot change
  at runtime; it can only be set in the Material Instance Editor," so per-scene switching
  costs one material instance per state there, against Godot's runtime bool.
- **Mips** — generate. UE's `do_scale_mips_for_alpha_coverage` is an **alpha-test** remedy
  (Castaño 2010 [COMMUNITY]; peer-reviewed successor Yuksel 2018 [VERIFIED]) and is the wrong
  tool for an alpha-**blended** band; the contract should state it off. **Godot documents no
  alpha-coverage mip preservation at all** — a clean negative; `Mipmaps > Limit` is
  documented as "currently not implemented and has no effect."
- **⚠ A load-bearing authoring step the spec does not currently name: colour must be dilated
  outward under transparent texels before export.** It is the only mitigation available in
  *both* engines. Godot can also do it at import (`process/fix_alpha_border`); UE names no
  dilation feature. Whichever is used must be recorded, because it is a property of the
  written file.
- **Compression** — the file must carry real alpha at import or Godot selects BC1 (1-bit
  alpha); a soft band wants `compress/high_quality` (BPTC). The parallel BC7 claim for UE is
  `[COMMUNITY]` only — no version-anchored UE 5.x compression page was retrievable.

**On the sdlab channel role**, checked against the code rather than inferred: Ruling 19
predicted "a `layer` channel role is a schema entry, not a rebuild." `lib/asset-source.js`
accepts `encoding: "rgba"` for a texture-space channel and maps it to PNG colour type 6.
So an RGBA layer is expressible in schema 1.0.0 **today**, with no schema change — the
prediction holds.

---

## Q3 — waterline practice: ⚠ THE NEGATIVE FINDING THE SPEC ASKED FOR

**Decides:** whether the layer's *content* should be painted water at all. The spec's own
trigger: *"if the standard answer is shader-side, the layer's content may be simpler than
painted water and the spec should know before generating any."* **That trigger has fired.**

**Two different things have been conflated under one word.**

- **The static band is genuinely painted art.** The real-world *boot top* is "a specifically
  painted line featured on the hull… that signifies the designed waterline," in a zone
  "alternately wet and dry," in its own paint [COMMUNITY: trade glossary]. Fixed in hull
  coordinates, independent of the live sea.
- **The dynamic wet/foam band is computed per frame, shader-side, in every shipped source
  that could be read.** Sea of Thieves generates foam "around objects that intersect the
  water surface within a camera centered window using **depth buffer comparisons**," then
  blends that mask "with artist-authored textures" — art that lives in the **water's**
  material [VERIFIED 10.1145/3214745.3214820]. Horizon Forbidden West passes foam location,
  relative height and deformation strength "through the **vertex color**" of the water
  [TALK: SIGGRAPH 2022 Advances]. Assassin's Creed III measures hull–water contact at runtime
  with depth probes along the gunnel that "sense how far up the side the waves were rising"
  [TALK/interview].
- **Where UV-space art does enter wetting, it encodes susceptibility, not appearance.**
  Lagarde's shipped decomposition (Dontnod, *Remember Me*) is a per-texel **porosity** map
  times a runtime `WetLevel`: `Diffuse *= lerp(1.0, factor, WetLevel)` with
  `factor = lerp(1, 0.2, Porosity)` [COMMUNITY: studio blog]. The physics agrees that this
  is a multiplier and not a repaint: darkening comes from a water film raising total internal
  reflection [VERIFIED 10.1364/ao.27.001278], and the canonical model is a water layer over
  the material [VERIFIED 10.1007/978-3-7091-6809-7_24].

**No published case was found of a studio authoring a waterline or wet band into a separate
toggleable texture layer on a hull.** The nearest shipped-adjacent practice is a
material-layer blend driven by a vertex-colour mask [COMMUNITY: artist interview, not a
shipped title]. The agent's own confidence: high on the shader-side answer (four independent
sources), **moderate on the negative — absence of publication is not absence of practice.**

---

## Where this collides with the spec as written

Named, with the spec's own line quoted. **None of these is decided here.**

| # | spec text | what the research says | status |
|---|---|---|---|
| C1 | Step 0.4 and Arm W2's prompt: *"deep sea-blue-grey wash, **foam-white lap line**"* | foam belongs to the water's material and is generated from a depth/intersection test; no source paints it into the contacted object's UVs (Q3.2, Q3.3) | **collision** — the foam half of the prompt has no shipped precedent in this position |
| C2 | Arm W2: masked generation committed into the layer, mechanics left to Phase 0 | (b)-as-diff is unsound by arithmetic (Q1.1–1.2) and noisy by measurement (Q1.3–1.5); (a) is production-grade but graded on preference; **(b′) masked paste — what facet already does — is a third option the spec does not list** | **the dichotomy is incomplete** |
| C3 | Step 0.3: the layer state's emit/commit discipline | the written file needs colour dilated under transparent texels, or it bleeds at mip boundaries in both engines (Q2) | **a required step the spec does not name** |
| C4 | W-H4: *"the Director… can say in one sentence whether the ship floats"* | what reads as floating in shipped work is the **water's** foam at the intersection, not paint on the hull (Q3.2, Q3.3) | **the premise is challenged** — a layer-on/layer-off toggle with no water surface in frame may not be able to answer it either way |
| C5 | Metrics: *"the layer's own provenance… the mask is the gate"* | RGBA-native alpha errs in the **interior**, not at the rim (Q1.8) — a boundary-shaped gate watches the wrong direction | **gate direction** |
| C6 | W-H1: the contact mask is geometry's job | untouched. A plane-intersection band at a placed `waterline_z` is required by **every** reading — painted boot-top, shader height threshold, or porosity mask | **survives intact** |

**`waterline_z` is invariant to all three readings.** A boot-top band, a world-space shader
cutoff and a porosity mask all need the same number, placed by the same eye. Step 0.1 —
*the Director places the line on a candidate render* — is therefore the one Step 0 item that
cannot be wasted by whatever the ruling decides.

## What is NOT established

- **No source measures diff-recovery of a layer from a full-frame edit.** Q1.1 is an
  impossibility result; Q1.3–1.5 are drift measurements on unconstrained editors. This
  licenses *"(b) is unvalidated and has a known ambiguity"*, **not** *"(b) fails"* — and it
  says nothing at all about (b′).
- **No source measures RGBA-native diffusion in texture/UV space, on water content, or under
  a projection consumer.** All Q1 evidence is natural-image or portrait.
- **No engine page quantifies the waterline case.** Q2 is documentation end to end; the
  band's behaviour at mip 3–5 on this atlas is unmeasured, and measuring it is cheap.
- **No shipped title was confirmed doing a world-space-height wet band on a ship hull
  specifically**, and whether Sea of Thieves' or Black Flag's hull textures carry a painted
  boot-top stripe is visually plausible but unsourced.
- **Nobody publishes the separate-toggleable-layer comparison at all.** That licenses
  *"nobody publishes this"*, not *"it is wrong"* — and the Director's charter for E10 was
  explicitly that the mechanism generalises beyond water (snow on boots, mud on wheels, moss
  on ruins), none of which have a shader-side sea to be computed against.
