---
title: Getting started
description: What you need on the machine, how a subject enters the route, and the order the stages run in.
sidebar:
  order: 1
---

Every tool in facet is a script you invoke directly, against paths you type. So this
page covers what to have on the machine and the order the stages run in — that is the
whole of the setup.

## What you need

| | |
|---|---|
| **Python** | 3.11+, with `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`, `spandrel`, `torch` |
| **Blender** | 5.x, reachable on `PATH` or by absolute path |
| **GPU** | developed against an RTX 5090. VRAM headroom matters more than raw speed |
| **ComfyUI** | local install, needed **only** for the inpainting brush stage |

Generation runs on metered cloud GPU; geometry and every measurement run locally.

```bash
git clone https://github.com/mcp-tool-shop-org/facet
cd facet
python -m pytest -m "not artifacts"   # the 1121 hermetic tests CI reproduces
```

The full suite is 1166 tests. The 45 it deselects are the *artifacts* tier — they replay
recorded trees that are not in git, so they pass locally and are skipped in CI by
design.

## The order the stages run in

Each stage exists for a measured reason, and
[the handbook's front page](/facet/handbook/) gives the reasoning for every one. This is
the sequence.

1. **A form-exaggerated clay concept.** Sculpt-like, planes deliberately exaggerated, no
   surface noise. Reconstructors read weathered planks and painted grime as *geometry*.
2. **Image-to-3D reconstruction**, plus a styled twin generated from the same control.
   The twin is the colour and identity reference for everything downstream.
3. **Weld, then decimate.** A glTF export splits a vertex at every UV seam, so an
   exported mesh is per-triangle shells; collapse decimation on that tears holes. Merge
   by distance first.
4. **Allocate density** where the form is — and only where a measurement says a region
   earns it. The bust crop is a per-subject decision, not a universal stage.
5. **Cull what no camera can see** — from the *atlas*, never from the mesh. Deletion
   needs a perfect gate forever; exclusion makes the failure impossible.
6. **Generate twins from THIS mesh** and project them. A twin carries the silhouette of
   the mesh it was rendered from, so a twin borrowed from another mesh paints into empty
   space.
7. **Brush the holes**, spiralling outward from already-painted regions so each stroke
   extends an existing character rather than composing a new one.
8. **Finalize** — surface-aware dilation closes what is left, sourcing from the nearest
   painted texel *on the surface* rather than the nearest one in the atlas.

## Before you trust any number you produce

Three habits, each of which this repo paid for:

- **Judge textures under flat light and geometry under clay.** A Workbench STUDIO render
  is not a texture readout — grey chalky facet mosaics are specular highlights on
  flat-shaded normals and vanish under `--flat`. Two debugging rounds were lost to this.
- **Put the asset beside its reference, with its provenance, at full size.** The cheapest
  diagnostic here is a `reference | asset | provenance | error` sheet, and it did not
  exist for the first seven experiments. When it was finally built, the whole thesis was
  readable off one panel.
- **Ask what a wrong answer would look like, then check for that.** A gate written
  against the success mode will pass a broken artifact confidently: a silhouette-IoU
  cull gate returned `1.00000` on a mesh with a hole clean through the torso.

## Reading the record

Every non-trivial change here ran as a numbered experiment, with its predictions written
before the measurement:

```
spec written BEFORE the work  →  report written AFTER  →  advisor ruling LAST
```

Forty-four experiments are in
[docs/experiments](https://github.com/mcp-tool-shop-org/facet/tree/main/docs/experiments).
You do not have to read them linearly — the record is indexed:

```bash
python tools/facet_index.py build      # regenerate the SQLite + FTS5 index
python tools/facet_index.py verify     # four legs, all must pass
python tools/facet_index.py q "blade band"
python tools/facet_index.py claims     # staleness sweep over the current-state docs
```

`q` answers in roughly forty lines what reading the record takes six hundred to answer.
`verify` is the gate: byte-identical determinism across interpreters, counts against
independent greps, zero dangling pointers, and a seeded question set that grows with the
record.
