---
title: Tool reference
description: What each tool does, the evidence for it, and the ones kept precisely because they failed.
sidebar:
  order: 4
---

Nothing below is marked working unless it produced an artifact a human looked at. The
failures are in the repo too, with their reason, because a claim sitting next to
runnable code can be checked in minutes instead of trusted.

The authoritative version of this page, with the full evidence column, is
[docs/tools.md](https://github.com/mcp-tool-shop-org/facet/blob/main/docs/tools.md).

## The route

| tool | what it does |
|---|---|
| `render_geomaps.py` | position/normal conditioning maps via open3d raycasting — replaces nvdiffrast (non-commercial) at <1/255 MAE on all six views |
| `ig2mv_licensefree.py` | six consistent views of one character in one pass, ~24 s on an RTX 5090 |
| `sr_views.py` | view-space upscale — spandrel (MIT) + RealESRGAN anime6B (BSD-3), deterministic by construction |
| `smart_decimate.py` | allocates polygon budget by face rect and carries UVs through the cut — **welds before decimating**, which is the whole fix |
| `cull_unseen.py` | classifies faces by exterior visibility so the atlas can skip them; gated on first-hit **depth**, never on silhouette |
| `restylize_views.py` | generates a mesh's own twins — builds the control image, saves the exact figure mask beside each twin |
| `project_twins.py` | projects the styled twins onto the atlas and emits a hole map; trust mask ∧ exact silhouette, with a registration halt at IoU < 0.80 |
| `texpass_iter.py` | the emit/commit write-head for progressive texture fill — styled texels are byte-identical across a commit, holes strictly shrink |
| `texpass_brush.py` | drives local ComfyUI for the masked inpainting stroke, ~45 s per stroke |
| `texpass_finalize.py` | surface-aware dilation fill for residual holes |
| `bake_hero_{prep,fuse,pack}.py` | multi-view baker — depth-tested visibility, per-texel ownership, seam levelling |
| `e11_export_turnaround.py` | the dense-turnaround export: flat renders, exact silhouettes, class maps and owner slices as a sha-linked tree |
| `facet_index.py` | the record's own index — `build` / `verify` / `q` / `claims` |

## Verification

`turn_render.py` and `head_render.py` are the cameras; `head_crop.py` builds comparison
sheets at zoom; `mesh_stats.py` measures any mesh identically so two meshes made months
apart by different tools stay comparable; `gate0_sheet.py` and `gate1_sheet.py` build
the designation and acceptance sheets at full size, concept beside geometry, **ranking
nothing** — the Director ranks.

`gate_mesh.py` is character-only and its head/shoulder logic is meaningless on other
subjects. Both non-character profiles carry `mesh_gate: none` for exactly that reason.

## Superseded — kept because the failure is the lesson

`tools/superseded/` is not an archive. It is the mechanism that stops a falsified
approach quietly becoming doctrine again: anyone can run these and watch them fail the
same way.

| tool | why it is there |
|---|---|
| `bake_multiview_glb.py` | averages views instead of assigning ownership — and averaging disagreement **is** ghosting. The documented cause of smeared faces, not a tuning miss |
| `retopo_bake.py` | failed twice: the selected-to-active ray bake returned black, and re-UVing a decimated mesh produced 119,776 islands whose packing margins collapsed every island to a sliver |
| `tint_prime.py` | statistical colour priming, falsified three ways. Height bands have no horizontal awareness, so arm-versus-torso assignment changes per view. Structural, not tunable — **do not retry** |
| `project_prime.py`, `facing_atlas.py`, and three others | earlier projection experiments, superseded by `project_twins.py` and the texture-space loop |

## The two commands worth memorising

```bash
python tools/facet_index.py q "<anything>"   # ask the record
python -m pytest -m "not artifacts"          # the 1062 hermetic tests CI runs
```
