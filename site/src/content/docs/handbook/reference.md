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

## The composition chain (E45–E49, 2026-08-16)

The seven tools that closed the projector question — the eight plates compose, and the
rebuilt atlas renders cleared the Director's acceptance bar for the first time on this
route. Five of the seven were built by an outside review channel (nominated calibration
claims have held **twenty-one for twenty-one**, each verified here by running it before
anything trusted the build).

| tool | what it does |
|---|---|
| `emit_view_aovs.py` | per-view G-buffers of a recorded state (depth, world pos/normal, surface id, callieri weights) — anchored by pixel-exact reproduction of the recorded silhouettes, 16/16 cameras at 0 px |
| `callieri_border.py` | border weight, depth-edge mask, mixed-depth reject, facing weight — v1.0.1, warning-silenced, byte-identity proven |
| `s3_composite.py` | the existence-proof compositor: view-dependent and view-independent stills, per-pixel disagreement, coverage, a flow hook |
| `flow_estimate.py` | dense LK twin-to-mesh flow with sparse per-component confidence — the aperture problem is refused, not hallucinated |
| `s3_run.py` | runs the compositor over a bundle, all targets, flow A/B via `--flow-dir` |
| `s3_sheet.py` | native-pixel acceptance sheets — provenance as a panel, MISSING made explicit, crop geometry gated |
| `twin_mesh_warp.py` | per-tile twin↔mesh correspondence, silhouette and interior legs, validated on injected shifts before any real measurement |
| `atlas_from_aovs.py` | texel-driven atlas rebuild from a bundle — owner/blend modes, flow off/on, sentinel-honest coverage |

## The canon gate (2026-08-17)

The identity specification named seventeen elements. The workflow that generated the
twins named sixteen. The profile default a fresh run would use names six. Nothing
connected them, so four arcs repaired composition downstream of paint that was wrong at
the source.

**SURFACE is the row.** An element list cannot show you what is missing — the
leather-wrapped grip was absent from a seventeen-row list and no reading of that list
ever revealed it. A surface list with a nullable occupant makes the hole a row.

| tool | what it does |
|---|---|
| `canon_gate.py` | the **router**: resolve a subject to its canon, cover a prompt in both directions, carry a scope, census every subject, verify via a sidecar. Runs **inside** every tool that authors a generation, before the output directory is created |
| `canon_worksheet.py` | the **authoring half**: kind templates so a hole is a row, IDENTITY → inventory, joints as pairs to confirm, per-view scope slots, spatial bind, and the density readout. Structurally cannot fill an occupant |
| `canon/<subject>.surfaces.json` | the database: surfaces with occupants, joints as first-class rows between two surfaces, blocked additions recorded rather than installed |
| `evidence.py` | the diagnostic layer — provenance classification, the acceptance sheet, and the numbers with their denominators and space declared |
| `flat_trace.py` | render pixel → atlas texel → contributing view → that view's twin |

```bash
python tools/canon_gate.py census
python tools/canon_gate.py check --subject W3 --prompt "..."
python tools/canon_gate.py check --canon canon/w3.surfaces.json --prompt "..." --scope subject
```

### Fail-closed, and why the escape is census-backed

A tool that authors a spend and is given no canon **refuses** rather than proceeding
quietly. The previous shape was `if args.canon:` — so omitting a flag walked past the gate
in silence, and the shipped PowerShell driver did exactly that.

```bash
# no canon and no escape -> ANDON, and --outdir is never created
python tools/restylize_views.py --emit-only --inputs IN --outdir OUT --prompt "..."

# the escape names a subject the census knows has an IDENTITY and no surfaces
python tools/restylize_views.py ... --no-canon --subject GALLEON   # proceeds, announces
python tools/restylize_views.py ... --no-canon --subject W3        # REFUSED: W3 has surfaces
```

Requiring a census subject is what stops the escape becoming a checkbox: wearing it means a
deliberate edit of the census, and you cannot invent a subject that has no IDENTITY.

### Both directions

Checking that the prompt **contains** the canon finds a thin prompt. Checking that
everything in the prompt **is** canon finds a phrase naming something the subject does not
have. Schema 2 declares the legal non-surface clauses (style, framing) so the reverse check
does not fire on `plain grey background`; schema 1 files stay one-directional by design, so
adding the reverse could not make an older subject start refusing its own style words.

**What it does not cover, stated rather than left to be discovered:** paraphrases and
synonyms — semantic matching would put a model inside a gate — per-view stems until a view
scope is declared, unratified drafts, subjects with no surfaces file, or whether a named
material landed on the right surface. Scope slots exist with empty surface lists: filling
them is a human walk, same as filling occupants. Four subjects have an IDENTITY.md and no
surfaces JSON — left undone rather than generated without walking the reference.

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
python -m pytest -m "not artifacts"          # the 1284 hermetic tests CI runs
```
