# The facet handbook

A styled 2D concept goes in; a textured 3D character comes out. Everything runs on one
local machine, and nothing in the chain carries a non-commercial licence.

This handbook is the guide. [The README](../../README.md) is the measured state of every
tool, and [docs/experiments](../experiments/) is the evidence — every claim here traces to
a numbered experiment you can re-run.

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

### 2 — Frame the face, get a face

Reconstruct a second time from a head-and-shoulders crop of the same clay.

The generator caps input at 1024 px on the long side, so a full figure puts roughly **138
px** on the head where a bust crop puts **439 px**. That is the entire difference between a
continuous brow bar over a shallow recess, and separated eyelids with a brow furrow and
modelled nostril cavities. Measured across two characters ([E01](../experiments/E01-facial-structure-ceiling.md)).

Reconstruction is *not* the ceiling on facial quality. Framing is.

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

## Cost

Per character, on an RTX 5090, all local:

| stage | cost |
|---|---|
| reconstruction | ~20 s per arm |
| weld + density allocation | seconds |
| visibility classification | seconds |
| twins (2 views) | ~2 min |
| brush loop (8 strokes) | ~8 min |
| finalize + pack + renders | ~2 min |

## Honest limits

- **Stroke seams are not levelled.** Projection has a low-frequency levelling term; the
  brush loop does not, so every stroke boundary is a tonal step.
- **Dilation still bleeds between unrelated islands** — atlas adjacency is not surface
  adjacency, and filled texels remain 4.8× enriched in visible blotches.
- **Chart fragmentation limits texel density.** Culling removed 47% of faces but only 34%
  of charts, because invisible surface is interleaved *within* charts rather than sitting in
  separate ones.
- **Everything here is calibrated on humanoid characters.** Ships, monsters and props are
  untested; [the profile design](../profiles-design.md) exists so that testing them cannot
  break the character path.

## Licence

Every stage is local and commercially clean: SDXL (OpenRAIL++), MV-Adapter, open3d
(Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy, trimesh.

Deliberately excluded with the reason: **nvdiffrast** (non-commercial — enforced by a
structural tripwire, not by attestation), **Hunyuan3D-Paint** (licence void in the EU, UK
and South Korea), **MVPaint** and **TEXGen** (no licence), **UltraSharp / SUPIR /
StableSR** (non-commercial upscalers).
