# facet

Turning a styled 2D concept into a textured 3D character — with the style applied
**on the asset** in texture space, not painted per view. Runs entirely on local
hardware, with no non-commercial dependency anywhere in the chain.

Named for both halves of the problem: the polygons, and the face they have to hold.

## The route

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

**Where it stands.** Geometry is solved: reconstruction produces real facial structure
given the right framing, and polygon budget allocation works. Texture is improving under
measurement — interpolation is down **68%** and the current asset is *"a lot better"* by the
Director's eye, with two named defects remaining (below). Nothing here is claimed as
finished.

**Form first, style second.** Image-to-3D reconstructors key off shading, silhouette
clarity and unambiguous depth. A heavily stylized sprite — weathered planks, painted
grime, fine rigging — fights the reconstructor, which reads surface noise as geometry
and muddies the form. Feed it a clean, sculpt-like image with the major planes
deliberately exaggerated, and the topology comes back better. The styled twin,
generated alongside the clay from the same control, stays as the colour and identity
reference for the texture stage.

**Frame the face, get a face.** Reconstruct a second time from a head-and-shoulders crop
of the same clay. Measured in [E01](docs/experiments/E01-facial-structure-ceiling.md)
across two characters: the crop puts **3.1–4.5× more polygons** on the head, and the
difference is structural rather than cosmetic. Full-figure input gives a continuous brow
bar over a shallow recess and flat punctured nostrils; the same character from a bust
crop gains separated upper and lower eyelids, a brow furrow, and modelled nostril
cavities. A face is a small fraction of a full-figure frame, and reconstructors spend
their resolution where the pixels are.

**Density where the form is.** Small polygons on the face, larger ones on flat
expanses. Facial structure that survives reconstruction survives every downstream
step, and styling applied to real structure reads naturally instead of sitting on
top of a blob.

**Style on the asset.** The texture atlas is the single accumulating state. The styled
twins are projected onto whatever surface they can see; everything they cannot see is
recorded as an explicit hole map and filled by a masked inpainting brush, one camera
at a time, with already-styled texels never overwritten.

**Twins belong to a mesh, not to a character.** A styled twin is a canny-locked restylize
of a *render of one specific mesh*, so it carries that mesh's silhouette. Measured: A0's
bounding box gives x/z 0.722 against the twin frame's 0.734 and registers to 1.6%; W3
reconstructs the same clay at x/z 0.458 — 38% narrower — and the same twins project the
arms and sword into empty space beside the mesh, collapsing styled coverage from 62% to
22.7%. **Generate twins from the mesh you are about to texture**, every time. It is one
job per view.

**Build the control image; don't hope Canny finds the silhouette.** A clay render is flat
grey on flat grey, so Canny returns 0.84% edge pixels and almost no outer contour — the
ControlNet constrains nothing and the model regenerates the character. Composite the
figure onto a contrasting background *and* union the figure mask's morphological gradient
into the edge map. Measured: control 6,482 → 33,864 px, silhouette IoU **0.290 → 0.777**,
bbox x/y 0.797 → 0.457 against the source's 0.458. `restylize_views.py` does this.

**Prompt per view, or the text overrides the control.** With a correct contour the back
view still came back front-facing at both 0.92 and 0.75 denoise — the control carries
facing (mirrored-front vs back edge-map IoU 0.165), but a prompt asking for "a long red
beard, gold necklace" on every view is an instruction to draw a face, and the text wins.

**Polygons and texels are separate budgets.** `smart_decimate` allocates polygons;
`bake_hero_prep`'s island scaling allocates texels. These do *not* double-subscribe — a
head can hold 84.4% of the faces and only 44.8% of the UV area simultaneously. Any gate
comparing UV area to **face count** is meaningless on a deliberately non-uniform mesh;
compare UV area to **3D surface area**, which is texels per unit of surface.

**Keep the generator's atlas; watch the gutter.** TRELLIS ships xatlas UVs, and
`bake_hero_prep` used to delete them and re-run `smart_project` — which on the same 287k-face
mesh produced **35,070** islands (8 faces each) where the native atlas has **14,010** (20.5
faces each). Native UVs are now the default. Then the gutter: at `island_margin` 0.004 on a
4096 atlas that is 16 px around **every** island, which took packed coverage to 4.01%;
dropping it to 0.001 restored **18.76%**. Raising `angle_limit` to merge islands was tried
and moved the count **0.8%** — `smart_project` splits on UV distortion as well as angle, so
decimation's long thin triangles split whatever the threshold.

**Cull what no camera can see — from the atlas, not from the mesh.** Measured across 46
exterior cameras: **49% of valid atlas texels are never visible from outside** — interior
shells, deep folds, behind a beard, between fingers. The atlas was paying texels for surface
the brush could never reach, then dilating them, then bleeding that into the surface you can
see. Excluding those faces from the UV layout took interpolation down **68%** (2,551,893 →
813,773 dilated texels) and brush coverage from 27% of holes to **52.7%**.

Do this by **excluding faces from the atlas, never by deleting them**. Deletion needs a
perfect gate forever — and the obvious gate does not work: silhouette IoU is structurally
blind to holes punched through visible surface, because the ray behind a removed face still
hits geometry. It returned **1.00000 at all eight cameras** on a mesh with a hole clean
through the torso. Under atlas-exclusion the geometry is never modified, so the failure is
impossible rather than detectable, and a camera you add later sees a flat patch instead of a
hole. The visibility set must also be a **superset of every production camera** — a generic
sphere is not, however dense.

## Status of every tool — measured, not asserted

Nothing here is marked working unless it produced an artifact a human looked at. The
failures are in the repo too, with the reason, because a claim sitting next to
runnable code can be checked in minutes instead of trusted.

Claims that turned out to be wrong are corrected **in place, with the measurement that
overturned them**, rather than quietly deleted — see the `smart_decimate.py` entry below
for a worked example. The evidence trail lives in
[docs/experiments](docs/experiments/): a spec is written before the work, a report after,
and conclusions come last.

### `tools/` — works, load-bearing

| tool | what it does | evidence |
|---|---|---|
| `render_geomaps.py` | position/normal conditioning maps via open3d raycasting | replaces nvdiffrast (non-commercial) at <1/255 MAE on all 6 views |
| `ig2mv_licensefree.py` | six consistent views of one character in one pass | 24 s on an RTX 5090; nvdiffrast's module name is occupied by a tripwire stub that raises if any code path touches it |
| `sr_views.py` | view-space upscale — spandrel (MIT) + RealESRGAN anime6B (BSD-3) | deterministic by construction; ×2 for views, ×4 for face crops |
| `project_twins.py` | projects the styled twins onto the atlas, emits a hole map | 50–62% of the surface styled from two reference images |
| `texpass_iter.py` | emit/commit write-head for progressive texture fill | selftest: styled texels byte-identical (delta 0.000000), holes strictly shrink |
| `texpass_brush.py` | drives local ComfyUI — Qwen + style LoRA + inpainting ControlNet | ~45 s per stroke |
| `texpass_finalize.py` | dilation fill for residual holes | closed 868k texels with zero mean fallback |
| `texpass_loop.ps1` | the whole loop: reset, eight strokes, finalize, render | ~8 min per character, unattended |
| `bake_hero_{prep,fuse,pack}.py` | multi-view baker — depth-tested visibility, per-texel ownership, seam levelling | kills through-projection: a raised sword no longer bakes onto the chest behind it |
| `resample_atlas.py` | nearest-surface texture transfer between topologies | replaces Blender's ray bake, which returned a black atlas when rays were cast from a seam-split mesh |
| `restylize_views.py` | generates a mesh's own twins — builds the control image, saves the exact figure mask beside each twin | silhouette IoU **0.290 → 0.777**; per-view prompts take face detections on the rear view 1 → 0 |
| `cull_unseen.py` | classifies faces by exterior visibility so the atlas can skip them | 47.6% of faces unseen by 46 cameras; interpolation down **68%**; gated on first-hit **depth**, not silhouette |
| `texpass_provenance.py` | replays the commit chain offline to tell you, per texel, whether colour came from a twin, a specific stroke, or dilation | reproduces live commit counts to the texel; settled the blotch question without a GPU |

### `tools/` — unblocked, fix measured

**`smart_decimate.py`** allocates polygon budget by face rect and carries UVs through
the cut, so the existing atlas keeps working with no re-UV and no re-bake. Mechanically
sound and verified: 287k → 150k with UV span intact.

Decimating tore holes and left lace instead of redistributing density. **The cause was
mislabelled in this file until it was measured, and the correction matters more than the
tool.** An earlier version blamed reconstruction — "roughly 8,600 disconnected shells" —
a number inherited from a session record and never checked. Measured in
[E01](docs/experiments/E01-facial-structure-ceiling.md):

| mesh | connected components |
|---|---|
| raw reconstruction (`warrior/mesh.glb`) | **1** |
| four fresh reconstructions | **40–191** (92–98% of faces in one shell) |
| `hero_bake/prep_uv.glb`, `texpass/warrior_texpass.glb` | **285,654** |

Reconstruction returns a connected surface. **Our own UV unwrap and glTF export splits a
vertex at every UV seam**, which with per-triangle islands explodes the mesh into one
shell per face — and decimation was handed that. Collapse decimation merges neighbours;
per-triangle shells have none.

**The fix is local and cheap: weld before decimating** — merge-by-distance now runs
before the decimate modifier, because Blender stores UVs per-loop rather than per-vertex.
Measured on `warrior_texpass.glb`, both arms at `--target 150000` with identical
protection settings, the second reproducing the historical shredded output exactly:

| run | verts in | shells in | faces out | shells out | legs |
|---|---|---|---|---|---|
| `--no-weld` (old behaviour) | 858,562 | 285,654 | 150,000 | **149,528** | shredded to lace |
| welded (default) | 858,562 → 137,607 | 285,654 → **1** | 149,996 | **1** | intact |

The atlas survives the weld: every one of the 287,230 surviving faces kept its exact UVs,
and a textured flat render of the welded 150k mesh differs from the 287k source by a mean
of **0.47/255**. Four zero-area triangles (0.0014%) collapse in the merge — a triangle
whose corners were the same point had no area to lose. The run asserts both facts and
halts if either fails, and `--no-weld` reproduces the old behaviour for comparison.

### `tools/superseded/` — kept because the failure is the lesson

| tool | why it's here |
|---|---|
| `bake_multiview_glb.py` | Averages views instead of assigning ownership. Averaging disagreement **is** ghosting — this is the documented cause of smeared faces, not a tuning miss. Superseded by the ownership baker. |
| `retopo_bake.py` | Retopo → re-UV → bake. Failed twice: the selected-to-active ray bake returned black, and re-UVing a decimated mesh produced 119,776 islands whose packing margins collapsed every island to a sliver — 0.4% atlas coverage. |
| `tint_prime.py` | Statistical colour priming, falsified three ways. Height bands have no horizontal awareness, so arm-versus-torso assignment changes per view. Structural, not tunable — do not retry. |
| `project_prime.py`, `prime_bake_glb.py`, `project_multiview.py`, `facing_atlas.py`, `weight_glb.py` | Earlier projection experiments, superseded by `project_twins.py` + the texture-space loop. |

### `tools/verify/` — how anything gets judged

`head_render.py` and `turn_render.py` are the verification cameras;
`head_crop.py` builds comparison sheets at zoom; `gate_mesh.py` is a mesh QA gate
(character-only — its head/shoulder logic is meaningless on other subjects);
`mesh_stats.py` measures any mesh identically — shell count, face-rect polygon
density, and curvature variance inside the face rect — so two meshes made months
apart by different tools are still comparable.

## Hard-won rules

**Judge textures under FLAT light.** A Blender Workbench STUDIO render is not a texture
readout. Grey chalky facet mosaics are specular highlights on flat-shaded normals and
vanish entirely under `--flat`. Two debugging rounds were spent chasing a render
artifact that was never in the texture. Use `--clay` to judge geometry with no texture
in the way.

**Check the alpha channel before trusting an "is it black?" test.** A fully black RGBA
image with alpha=1 averages exactly 0.25 and sails past a `< 0.005` threshold. That
check shipped a black mesh.

**Blender's RNA references go stale after any `mode_set` round trip.** Reading through
one silently returns zeros — no exception. Re-fetch from `obj.data` after every
edit-mode exit.

**Blender caps meshes at 8 UV layers, and `uv_layers.new()` returns `None` silently at
the cap.** A design needing 9 produces a white export and a long bisect.

**A raised weapon rises above the crown.** Any instrument that finds the head by height
will grab the blade instead. Find the head by projecting a face rect from the front
view.

**Detail overlays mask; it never restores.** No texture pass can add facial structure a
mesh does not have. If the face is crude in clay, it will be crude when painted.

**A gate must test the operation's failure mode, not its success mode.** See the cull
above: silhouette IoU checked "is the silhouette still there" when the risk was "did
anything behind it disappear," and returned a perfect score on a broken mesh.

**A guard that fires on a correct input is worse than no guard.** A centroid checksum
compared Blender's float32 `polygon.center` against trimesh's float64. They agree to
5.6e-8 — which straddles a 5-decimal rounding boundary on thousands of values, so an exact
hash mismatched on a perfectly aligned mask. Compare positions within a tolerance, and size
the tolerance against the thing you are detecting (a one-face shuffle moves a centroid
~0.0029; the noise floor is 5.96e-08).

## Known defects, named

**Stroke seams are not levelled.** Stage 1 applies a low-frequency Gaussian levelling
across projection boundaries. **The brush loop has none** — so every boundary between two
strokes, and between stage 1 and the first stroke, is an unlevelled tonal step. Provenance
replay found the forehead "blotch" on the current asset is exactly this: twin paint below
meeting the overhead stroke above, two blotch pixels in the whole disc, a step rather than a
defect in either source. The architecture called for Poisson seam levelling; it was
implemented in projection and never carried into the loop.

**Dilation still bleeds between unrelated islands.** Down from 75% of hole texels to 33.9%
of the atlas, but dilation-filled texels remain **4.8× enriched** in visible blotches
against a 5% base. Colour crosses the gutter from whichever island the packer placed next
door, and atlas adjacency is not surface adjacency.

**Chart fragmentation is the binding constraint on texel density.** Culling invisible
surface removed 47% of faces but only 34% of charts — because invisible surface is
interleaved *within* charts, so excluding it perforates them rather than freeing them.
Faces-per-chart fell 20.5 → 16.4, bbox fill 42.1% → 36.6%, packed coverage 24.81% → 14.32%.
Net texels landing on visible surface rose ~17% where a naive reading predicts double.

## Licence position

Every stage runs local and commercially clean: SDXL (OpenRAIL++), MV-Adapter (open),
open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy,
trimesh.

Deliberately excluded, with the reason: **nvdiffrast** (non-commercial — enforced here
by a structural tripwire, not by attestation), **Hunyuan3D-Paint** (licence void in the
EU, UK and South Korea), **MVPaint** and **TEXGen** (no licence at all), and
**UltraSharp / SUPIR / StableSR** (non-commercial upscalers).

## Requirements

Blender 5.x, Python 3.11+ with `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`,
`spandrel`, `torch`. A local ComfyUI install is needed only for the inpainting brush.
Developed against an RTX 5090; VRAM headroom matters more than raw speed.
