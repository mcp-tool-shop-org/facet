# facet

Turning a styled 2D concept into a textured 3D character — with the style applied
**on the asset** in texture space, not painted per view. Runs entirely on local
hardware, with no non-commercial dependency anywhere in the chain.

Named for both halves of the problem: the polygons, and the face they have to hold.

## The route

```
form-exaggerated clay concept ─┐
styled twin (canny-locked)    ─┴─► image-to-3D ─► density allocation ─► texture-space styling
```

**Form first, style second.** Image-to-3D reconstructors key off shading, silhouette
clarity and unambiguous depth. A heavily stylized sprite — weathered planks, painted
grime, fine rigging — fights the reconstructor, which reads surface noise as geometry
and muddies the form. Feed it a clean, sculpt-like image with the major planes
deliberately exaggerated, and the topology comes back better. The styled twin,
generated alongside the clay from the same control, stays as the colour and identity
reference for the texture stage.

**Density where the form is.** Small polygons on the face, larger ones on flat
expanses. Facial structure that survives reconstruction survives every downstream
step, and styling applied to real structure reads naturally instead of sitting on
top of a blob.

**Style on the asset.** The texture atlas is the single accumulating state. The styled
twins are projected onto whatever surface they can see; everything they cannot see is
recorded as an explicit hole map and filled by a masked inpainting brush, one camera
at a time, with already-styled texels never overwritten.

## Status of every tool — measured, not asserted

Nothing here is marked working unless it produced an artifact a human looked at. The
failures are in the repo too, with the reason, because a claim sitting next to
runnable code can be checked in minutes instead of trusted.

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
| `resample_atlas.py` | nearest-surface texture transfer between topologies | replaces Blender's ray bake, which returned a black atlas on shell-soup meshes |

### `tools/` — works mechanically, blocked upstream

**`smart_decimate.py`** allocates polygon budget by face rect and carries UVs through
the cut, so the existing atlas keeps working with no re-UV and no re-bake. Mechanically
sound and verified: 287k → 150k with UV span intact.

It is nonetheless **blocked**, and the reason matters more than the tool: reconstruction
output is roughly 8,600 disconnected shells, not a connected surface. Collapse
decimation redistributes density by merging neighbours, and shell soup has no
neighbours to merge into — so it tears holes and leaves lace instead of reallocating.
Budget allocation needs a solid surface to operate on. That is a mesh-generation
problem, not a decimation problem.

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
