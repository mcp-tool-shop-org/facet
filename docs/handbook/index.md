# The facet handbook

A styled 2D concept goes in; a textured 3D asset comes out. Everything runs on one
local machine plus a metered cloud generation step, and nothing in the chain carries a
non-commercial licence. **Four subject classes have entered the route: a character
(accepted), a galleon (accepted), a dragon (ACCEPTED 2026-08-07 — the third accepted
asset, zero credits across its entire arc), and a longsword (designated, its
measurement pass dispatched)** — each with every subject value in its own profile and
identity fixture, so no subject can break another's path.

This handbook is the guide. [The README](../../README.md) is the measured state of every
tool, and [docs/experiments](../experiments/) is the evidence — every claim here traces to
a numbered experiment you can re-run. If this handbook and a ruling ever disagree, **the
ruling is right and this page has a bug**; corrections land in place, with the
measurement. Maintenance rule (Director, 2026-08-05): the README and this handbook are
updated **as the work moves**, at each ruling fold — translations are deferred until the
repo gets its treatment.

Companion pages: **[Subject profiles](profiles.md)** — the loader, the decision forms,
the registry sweep · **[The subjects](subjects.md)** — the three subjects' numbers, with
their denominators.

---

## What this is for

Making game characters at production quality without a modelling team, on the premise that
a small studio's leverage comes from a pipeline rather than headcount.

**What it is not:** a general 3D texturing tool. It assumes prerendered or
fixed-camera-set delivery, which is what lets it discard surface nobody will ever see. It
assumes you have a style you want carried faithfully rather than invented.

## The route, and why each stage exists

### 1 — Form first, style second

Feed the reconstructor a **clay** image: sculpt-like, planes deliberately exaggerated, no
surface noise. Image-to-3D models key off shading, silhouette clarity and unambiguous
depth; weathered planks and painted grime read as *geometry* and muddy the form.

Generate the **styled twin** at the same time, canny-locked to the same control. That twin
is the colour and identity reference for the whole texture stage.

### 2 — Frame the face, get a face — when the subject earns it

On a character, reconstruct a second time from a head-and-shoulders crop of the same
clay. The generator caps input at 1024 px on the long side, so a full figure puts
roughly **138 px** on the head where a bust crop puts **439 px**. That is the entire
difference between a continuous brow bar over a shallow recess, and separated eyelids
with a brow furrow and modelled nostril cavities. Measured across two characters
([E01](../experiments/E01-facial-structure-ceiling.md)).

Reconstruction is *not* the ceiling on facial quality. Framing is.

**But the crop is an allocation decision, not a universal stage** — it is made per
subject, in the profile, from that subject's own head evidence. The ship ruled
allocation NONE (nothing supported a privileged region); the dragon **also ruled NONE**
([E12 Ruling 2](../experiments/E12-ruling.md)) because its head reconstructs with
legible structure at full figure — separated horns, tooth rows, nostrils at 10.5% of
faces — so the E01 defect the crop exists to fix was not observed. Neither prior
subject's answer transfers; the measurement decides.

### 3 — Weld, then allocate density

Reconstruction returns a connected surface. **A glTF export splits a vertex at every UV
seam**, so a mesh that leaves your pipeline as one shell comes back as hundreds of
thousands. Collapse decimation merges neighbours, and per-triangle shells have none — so
decimating an exported mesh tears it into lace.

Weld first. Then spend polygons where the form is: dense on the face, sparse on flat
expanses. Blender stores UVs per-loop, so welding never disturbs the atlas.

### 4 — Cull what no camera can see

**About half the surface of a reconstructed mesh is not on the outside of it** — interior
shells, deep folds, behind a beard, between fingers. Measured at 49% of atlas texels across
46 exterior cameras ([E05](../experiments/E05-paint-more-surface.md)).

That surface costs three times over: texels in the atlas, holes in the map, and dilation
that bleeds into the parts you can see. Exclude it and interpolation falls **68%**.

**Exclude from the atlas; never delete from the mesh.** Deletion needs a perfect gate
forever, and the obvious gate does not work — see *Judging* below.

### 5 — Twins register. The prompt carries identity.

**This is the division the whole route turns on, and it took an experiment to find.**

A styled twin is a restylize of a render of one specific mesh, so it carries that mesh's
silhouette. Carry it to another mesh and it misregisters: a 38% narrower reconstruction of
the same character dropped styled coverage from 62% to 22.7%. Twin generation is a
**pipeline stage**, not an input.

**A twin has exactly one job: register to the mesh.** Everything that makes the character
*this character* is a named element in a versioned prompt.

That was learned the hard way. A twin generated against a control missing a quarter of the
silhouette painted a taller, narrower body than the mesh *and* silently dropped the
character's gold knee plates — armour that had only ever reached the image through **noise in
a broken ControlNet**. Cleaning the control corrected the proportions and the plates stayed
gone. Naming them brought them back: one phrase, with the control byte-matched, so the term
was the only difference.

**Measured, 8 elements against 5 held controls:** contradict the specification — *silver*
where gold arrives unbidden, *black* where wine-red arrives — and the prompt wins **8 of 8**,
median ΔE 46.3 against 6.2 on the held set, a **7.4×** separation. And it is still the same
figure: face, build, pose, bald head, boots. **Structure is held by the mesh and the control;
named attributes are carried by the prompt.**

**A canon element not named in the prompt is arriving by accident and will leave the same
way.**

Three things make this work:

- **Build the control image from geometry.** A clay render is flat grey on flat grey, so
  Canny finds 0.84% edge pixels and almost no outer contour — the ControlNet constrains
  nothing and the model invents a character. Use the **exact raycast silhouette**; do not key
  the render. A keyed clay mask lost a quarter of the figure interior — a stripe down the
  whole blade, patches through pauldrons and greaves — and the loss was invisible for four
  experiments because nothing compared the mask to the geometry.
- **Specify from scratch; never patch.** A specification determines what *occupies* each
  surface. It cannot add a second element to a surface already occupied — a gold plate asked
  for onto an existing fur cuff produced **no response at all** (ΔE 1.07), in two different
  grammatical forms. Replacement lands; addition does not.
- **Gate every twin against the spec before projecting it.** One view in eight came back with
  a garment the specification does not contain — navy blue where the spec says bare arms, 5,590
  px in a single connected blob, while the same camera from the other side rendered correctly.
  That is a per-view roll, not a prompt error, and no eye should be the detector.

### 6 — Project, brush, fill

The atlas is the single accumulating state.

Project the twins onto whatever surface they can see. Everything they cannot becomes an
explicit **hole map**. Then a masked inpainting brush fills holes one camera at a time,
with already-styled texels never overwritten.

**Order the strokes to spiral outward from painted regions.** The brush runs at full
denoise inside the mask, so hole texels have nothing to preserve — start it at the
worst-anchored camera and it composes a new character rather than continuing yours. Opening
at 95%-hole invented a plaited belt, a shoulder strap and a lengthened tunic.

Residual holes take a dilation fill.

## Judging

- **Textures under FLAT light.** A Workbench STUDIO render is not a texture readout —
  chalky facet mosaics are specular highlights on flat-shaded normals and vanish under
  `--flat`.
- **Geometry under `--clay`.** Texture hides geometry, and that confusion has cost whole
  sessions.
- **At full zoom, never from a contact sheet.** The defects that decide acceptance are
  invisible at thumbnail scale.
- **A gate must test the operation's failure mode.** Silhouette IoU returned a perfect
  1.00000 on a mesh with a hole punched clean through the torso, because the ray behind a
  removed face still hits geometry. Ask what a failure would look like, then check for that.
- **Beside the reference, with provenance.** The cheapest diagnostic here is *reference |
  asset | provenance | error* on one sheet. Four experiments ran without one; when it was
  finally built, the whole thesis was readable off panel 2 in a sentence — the blade is flesh
  where the reference is steel, and the provenance panel shows it carries no reference at all.
- **Validate a metric against a rejected artifact before you build on it.** Four experiments
  were graded on blotch counts, speckle, a step ratio and a flattening guard — **four of the
  five are 5×5 high-pass statistics, and the fifth is indifferent to where a colour lands.**
  The defect that decides acceptance is a *large region of the wrong material*, which is smooth
  inside itself and contributes only its rim to every one of them. One change cut a source
  error 70× and took speckle below the reference asset while a human saw no difference.
- **When a threshold passes, look at the shape of the residual.** A cross-hardware anchor
  cleared its bar at ΔE 0.84 — but what made it *the same asset* was that the residual was
  uniform across every structure (controls 0.71, treated regions 0.98). A structural difference
  concentrates. A run could clear the same bar with the residual piled into one region and the
  reading would be wrong.
- **Know your instrument's floor.** At denoise 0.92 the model repaints globally, so a held
  control sits near ΔE 6, not 0. Attribution rests on the *ratio*. An element effect below the
  floor is indistinguishable from global repaint — and a hue angle below a chroma floor is
  undefined, not a rotation.

## Where the work runs

**Generation runs on Comfy Cloud; geometry and measurement run locally.** This is not a
preference. The restylize graph stages 31,006 MiB of models — text encoder, UNet, ControlNet,
VAE — against a 31,200 MiB watchdog ceiling on a 32,607 MiB card. The working set reached
30,809 MiB with nothing left for activations, and **no reserve value fixes that**: peak was
31.7–32.0 GB across three runs regardless of the reserve *or* the desktop baseline, because
ComfyUI stages to fill whatever it sees free. Freeing 6.5 GB made the working set grow 6.1 GB.

**Cross-boundary work needs an anchor.** Before moving a line to different hardware, reproduce
a known output from its recorded parameters. Ours came back non-byte-identical at ΔE 0.84
against a 1.07 no-response floor — accepted, with the boundary recorded in every later report.

| stage | cost |
|---|---|
| reconstruction (TRELLIS.2 `1024_cascade`) | 103–141 s per mesh, local, 3.4–5.6 GB peak VRAM — measured across six meshes on two subject classes |
| weld + density allocation | seconds, local |
| visibility classification | seconds, local |
| prep bake (4096 atlas) | ~4–5 min, local |
| twins | ~1 min per view, cloud — **zero credits across every E04, E10 and E12/E13 generation** |
| projection, finalize, pack, renders | ~2 min, local |
| brush loop (per stroke) | ~1 min, cloud |
| dense-turnaround export + lane validation | minutes, local CPU |

## Honest limits

- **One twin in eight comes back off-spec** — a garment the specification does not contain,
  from a per-view roll rather than a prompt error. The detector is cheap and belongs in the
  route before projection; the eye is not a detector.
- **A specification cannot add to an occupied surface.** Replacement lands, addition does not.
  Specify a character whole; do not retrofit an element onto a finished generation.
- **A colour term reads as a chroma instruction more reliably than a lightness one.** Asking
  for *black* collapsed chroma as expected and raised lightness — desaturated mid-grey, not
  black.
- **Stroke seams are not levelled.** Projection has a low-frequency levelling term; the
  brush loop does not, so every stroke boundary is a tonal step.
- **Dilation bleeds between unrelated islands** unless the fill is surface-aware — atlas
  adjacency is not surface adjacency. A nearest-painted-texel lookup in 3D sources from under
  one triangle edge where the atlas flood sourced from 61.
- **Chart fragmentation limits texel density.** Culling removed 47% of faces but only 34%
  of charts, because invisible surface is interleaved *within* charts rather than sitting in
  separate ones.
- **⚠ Corrected in place, 2026-08-05 — the sentence below was written before E04 and
  both its predictions landed.** *Original:* "Everything here is calibrated on humanoid
  characters. Ships, monsters and props are untested; the profile design exists so that
  testing them cannot break the character path. The off-spec detector matters most
  there — nobody will know by eye what a galleon's palette should be." *Measured
  since:* the **galleon went through the whole route and was accepted** with every
  subject value drawn from `profiles/ship.json` and its fixture — the central
  hypothesis (*no shared-code edit needed*) was falsified five times and each
  falsification hardened the profile system rather than the subject breaking the
  route; and the off-palette gate did exactly what the sentence predicted, catching a
  garment no eye would have flagged on a subject nobody has priors for. The **dragon**
  is in flight on the same template with its own profile and fixture. What remains
  true: every new subject class arrives with **no working prior** — the beast's reach
  landed interpolable from neither predecessor — so every value is measured on the
  subject, never inherited ([the profile design](../profiles-design.md),
  [Subject profiles](profiles.md)).

## How a new subject enters the route

The template that carried the galleon and now carries the dragon
([E12's kickoff](../experiments/E12-executor-kickoff.md) is the worked current example):

1. **Gate 0 — reconstruct every candidate, measure, sheet, and the Director
   designates.** Three clays → three meshes → `mesh_stats` (no profile — the
   byte-identity path) → full-size sheets beside the sources, ranking nothing.
   Rejecting all candidates is a legitimate outcome. Subject-specific evidence the
   later decisions will need (the beast's head-region measurement) is gathered here so
   the designation is informed and the profile decides from data.
2. **The identity fixture is authored forward** (`canon/<SUBJECT>-IDENTITY.md`): every
   named element its own noun phrase, occupancy-complete, stressors pre-registered
   with their evidence status. The styled target pair is generated FROM it — identity
   enters through the prompt, or it is arriving by accident.
3. **The profile is drafted** (`profiles/<subject>.json`): measured values with their
   derivations, route constants as explicit first-run operating points, suspensions
   expressed mechanically. See [Subject profiles](profiles.md).
4. **The measurement pass** decides everything the draft suspended: the registry
   sweep, the prep bake, the pre-registered reach ceiling, the thin-structure cost
   curve, the camera question, the backdrop derivation — each measured on the
   designated mesh, blind predictions first.
5. **The styled target pair** (two identity-dense views, cloud, bounded re-roll) makes
   the authored identity visual — the Director's overrule window on the whole fixture —
   and the **palette bands** derive from the fixture's materials cross-checked against
   the pair, never against the twins they will later gate.
6. Then the route proper: twins → stage-1 projection → coverage-gated strokes →
   finalize → pack → **Gate 1, the Director's eye on the five-column sheet.**

## Accepted assets become training data

The dense-turnaround exporter ([E11](../experiments/E11-ruling.md)) turns an accepted
asset into a self-contained, sha-linked training tree: per-camera flat renders with
**exact silhouettes**, born-indexed provenance class maps, per-texel owner slices where
the asset has them, and the clay↔styled-twin pairs. The export is a **pure function**
(byte-identical on re-run), the shared views are byte-anchored to the recorded sheets,
and the sdlab lane's own validator ingests every subject **without schema edits** —
**three dense trees are registered in the lane** (galleon 28/28, W3 26/26, and the
dragon 26/26 as of 2026-08-07: **dataset asset #3**, the first manifest born declaring
its subject name, style register, tone-transform provenance and derivation kind under
the lane's 1.3.0 contract, ingested live at zero gap notices). Flat-only is the honest
export: backgrounds are augmentation-side (composite anything behind the exact
silhouette), and lighting would be a new renderer with its own anchors.

**⚠ Durability: the lane holds texture-space channels as sha-verified POINTERS**
(`materialized: false`) into the export trees at
`E:\AI\training\facet_next\E04_stroke\export\turnaround\`,
`E:\AI\training\facet_E08\ARMB\export\turnaround\` and
`E:\AI\training\facet_next\E13_stroke\export\turnaround\` — those directories are
load-bearing for the dataset: do not move them, and back them up as part of it. (The
list is now recorded on the lane's own side too — a dependency only the healthy side
knows about is not a recorded dependency.)

## Licence

Every stage is local and commercially clean: SDXL (OpenRAIL++), MV-Adapter, open3d
(Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Deliberately excluded with the reason: **nvdiffrast** (non-commercial — enforced by a
structural tripwire, not by attestation), **Hunyuan3D-Paint** (licence void in the EU, UK
and South Korea), **MVPaint** and **TEXGen** (no licence), **UltraSharp / SUPIR /
StableSR** (non-commercial upscalers).
