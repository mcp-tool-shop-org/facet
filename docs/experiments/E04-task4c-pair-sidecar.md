# The galleon's styled target pair — what this is, declared at birth

**Generated 2026-08-04, E04 Task 4c.** Two views, on Comfy Cloud, **0 credits** (no paid API
nodes; `estimate_credits` confirmed before submission).

## WHAT THIS PAIR IS, AND IS NOT

**It is a SPECIFICATION SOURCE and a VISUAL TARGET. It is NEVER a projection reference.**

This is the ship's analogue of W3's `canon/twin_*`, and it carries the same prohibition for
the same measured reason: **twins belong to a mesh, and a twin has exactly one job — register
to the silhouette it will be projected onto.** These two images were generated to make the
fixture visible and to give the palette bands something non-circular to cross-check against.
They are *not* the twins. When E04 textures this ship, `restylize_views` generates its own
twins from the mesh it is about to texture, per view, and those are what `project_twins`
consumes. Projecting *these* would be the A0-vs-W3 error — 62% coverage collapsing to 22.7%
because a twin carried a different mesh's silhouette.

## Provenance

| | |
|---|---|
| mesh | `galleon_00006_raw.glb` — Director-designated at E04 Gate 0 |
| clay source | `E04_task4/clay1024/clay_{1,7}.png`, `turn_render --clay`, **1024 × 1024** |
| control | `E04_task4/pair/clay_{1,7}_control.png` — `restylize_views --emit-only`, canny + morphological contour, built from the **exact raycast silhouette**, never a keyed render |
| silhouettes | `E04_task4/masks1024/galleonclay_{1,7}.png` — `silhouette_masks.py`, geometry |
| views | **7 = bow three-quarter**, **1 = stern three-quarter**. Bow is −x, stern is +x (measured 4a) |
| prompt | all twelve G-elements as own noun phrases + `plain white background` (derived, 4b) + the style tail |
| LoRA | `mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500.safetensors` — the live card name |
| recipe | seed **770700**, steps 20, cfg 2.5, denoise 0.92, ControlNet strength 0.9, shift 3.1, euler/simple |
| workflows | `workflow_1_stern_three_quarter.json`, `workflow_7_bow_three_quarter.json` — **saved before submission** |
| prompt ids | `a808bfac-612b-45f5-a38f-3a6d9968b97a` (view 1), `985f3734-2a31-4351-aa57-e327aabc501c` (view 7) |
| re-rolls used | **0 of the 1 allowed** |

## ⚠ DEVIATION FROM THE DISPATCH, reported at the top where it belongs

The pin said *"use your Gate 0 driver's measured frames"* — **1072 × 1024**. **Measured, that
frame cannot produce a registered control**, so these were generated at **1024 × 1024**.

`turn_render` sets `ortho_scale = size_z × 1.204` and Blender maps `ortho_scale` to the
**larger** render axis, while `silhouette_masks` computes `v_ext = size_z × 1.204` and derives
`h_ext` from it. On a **landscape** frame those disagree by exactly `1.2097 / 1.1556 = 1.0468`.
Measured on this mesh at 1072 × 1024: silhouette bbox **717 × 850** against the clay's
**751 × 892** — the clay figure is **4.7% larger in both axes**, IoU 0.75. A control built from
that pair would canny-lock the model to a silhouette 4.7% off its own render.

At **1024 × 1024** the two agree by construction (neither axis is larger, so both use
`size_z × 1.204`) and empirically: bbox scale **1.0000–1.0024**, y 87–936 against 86–937.
The ship fits with margin 1.157 horizontally and 1.204 vertically.

**This is the deferred `turn_render` fit-axis finding biting its other consumer.** The E04
spec's work item now has a second caller: `silhouette_masks` must move with it, or every
landscape subject silently misregisters. Recorded rather than fixed — changing either tool is
a behaviour change on the accepted character path.

## What this pair does NOT establish

Nothing about whether the route works on a ship. No twin, no atlas, no projection has run.
The pair exists so 4d's bands have a non-circular cross-check and so the Director has his
overrule window on the fixture made visual.
