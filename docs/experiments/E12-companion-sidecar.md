# The beast's head-crop COMPANION — what this is, declared at birth

**Generated 2026-08-06, E12 handoff 5 Task 3.** One view, Comfy Cloud, **0 credits**
(`estimate_credits` before submission). **Its single bounded re-roll is UNSPENT.** Job
`succeeded`, zero warnings.

## WHAT THIS IS, VERBATIM PER THE DISPATCH

> **"head-region spec source and definition gate; never a projection reference"**

E12 **Ruling 11b**. The prohibition is the same one the pair's sidecar carries and it is
stronger here, because a bust frame is the most tempting thing in the arc to project:
**twins belong to a mesh, and a twin has exactly one job — register to the silhouette it will
be projected onto.** This image is framed on a sub-box of the mesh at a camera no route tool
renders twins from. Projecting it would be the A0-vs-W3 error with an extra scale factor.
When the beast is textured, `restylize_views` generates its own twins from the mesh it is
about to texture, per view, at the route's own framing.

Its two jobs: give the Director a face at judgeable resolution (the **resolution rung** of
Ruling 11b's allocation ladder), and give the head region a spec source at a scale where
D8/D9/D10/D11 are actually resolvable — at pair scale the cavity is sub-resolvable and
"missing" is not yet a landing verdict.

## The frame — derived and pre-registered before the render existed

| | |
|---|---|
| source box | `head_00003.json` `head_box_blender` = [[−0.10497, −0.50074, 0.01045], [0.08072, −0.30154, 0.20965]], extent **[0.1857, 0.1992, 0.1992]** |
| frame validity | **checked, not assumed** — the box was measured on `dragon_00003_raw.glb` while every route consumer renders `prep_uv.glb`. Both have byte-identical raw-import bboxes, matching the JSON's `mesh_bbox_blender` exactly |
| padding | **1.12** — Gate 0's own head-crop padding, inherited not invented |
| rule | the route's own, `turn_render --fit-axis width`: `ortho_scale = max(size.x, size.y) * margin`, `sensor_fit` HORIZONTAL |
| aspect | **exactly 1.000** — the box's y and z extents are equal to five decimals, so a square frame *falls out of the rule* rather than being chosen |
| **ortho_scale** | **0.223104** = 0.1992 × 1.12 |
| scale | **pixel budget matched to the route's standing frame** (1792 × 1024 = 1,835,008) so the generator stays in the regime the arc has run in: √1,835,008 = 1354.6 |
| **frame** | **1360 × 1360** — both axes ÷16-legal, neither the standing 1024, per the Gate 0 generator-legal law |
| realised budget | 1,849,600 px, **+0.8%** against the standing frame |

**⚠ The ortho_scale is an explicit override, and it is printed as one.** `e12_head_render.py`
computes a yaw-**invariant** span (the horizontal diagonal, 0.305005 here) so a multi-yaw
sheet cannot let the head walk out of frame at 45°. This is a single yaw-0 frame whose scale
was pre-registered from the route's rule before the render existed. Reaching 0.223104 by
solving for `--pad` would have printed a padding of **0.82** and read as under-padding; a
`--ortho-scale` flag was added instead and **both values print at the site**.

**Resolution gained:** the mouth box goes from 222 × 134 px at the pair's view 1 to
**608 × 549 px** here — **11.2× the pixel area**.

## Provenance

| | |
|---|---|
| mesh | `E12_prep/prep_uv.glb` — the prep bake of `dragon_00003_raw.glb`, Director-designated at Gate 0 (Ruling 1) |
| clay | `head_companion/headclay_y+000.png`, copied to `headclay_0.png` so the prompts key matches the input stem — `e12_head_render.py --views 0 --res 1360 --ortho-scale 0.223104 --pad 1.12 --clay`, Workbench conventions `turn_render`'s |
| mask | `head_companion/headclay_mask.png` — a **direct raycast at the crop camera** (`e12_crop_silhouette.py`), NOT an upscaled crop of the full-frame silhouette, which would have handed a 4.1× blocky staircase to the contour term. 1,137,368 px, 61.493% of frame |
| **mask check** | geometry mask vs the render's keyed figure: **bboxes identical at (0, 115, 1359, 1359)**, IoU 0.9575, the 2.6% difference being the known grey-on-grey keying loss. The camera convention is reproduced and *checked*, not asserted |
| control | `headclay_0_control.png` — `restylize_views --emit-only --masks` at the **ruled canny 0.05/0.10**, **108,994 px** (canny 98,546 + contour 17,861) |
| prompt | `docs/experiments/E12-twin-prompts.json` v**E12-pair-4**, key `headclay_0`, **15 of 17 terms** — same builder, same profile entry, same deletion construction as the eight view stems, so the cloud guard's provenance check holds with no skip flag. The eight `dragonclay` stems verified **byte-identical v3 → v4** |
| stem derivation | verified against this render before writing. **KEEPS D3** (both wings enter the crop at the left and right edges — Gate 0's flagged case). **DROPS D6** (dorsal *and tail* spines; the tail is far out of frame and the ivory family is redundantly declared by D4/D5/D10) and **D7** (feet out of frame, no wing-claw spur legible). Subject noun kept — identity rides the prompt, composition is held by the control |
| LoRA | **NONE.** No loader node; 14 nodes, was 15. Pre-flight scans every node for the class family and the card string |
| recipe | seed **770700**, steps 20, cfg 2.5, denoise 0.92, ControlNet 0.9, shift 3.1, euler/simple — every value the profile's, checked by value in pre-flight |
| workflow | `head_companion/workflow_headclay_0.json` — **saved before submission**, with the uploaded cloud names in it |
| uploads | `head_companion/uploads.json` |
| prompt id | `2eb6f163-0de6-47df-ac98-607d41ccd320` |
| output | `companion_y0.png` sha256 `0f549afea07b39bc…`, **1360 × 1360** |
| **registration** | styled figure vs geometry silhouette: **IoU 0.993953**, bboxes **identical**. The halt stays suspended at `reg-iou-min 0.0`, as everywhere on this subject |
| re-rolls used | **0 of the 1 allowed** |

## What it shows, with no verdict attached

Landings at scale are enumerated in [E12-handoff5-report.md](E12-handoff5-report.md) §4. The
two that most need the advisor's and the Director's eyes:

- **D8 did not land as an eye.** A crimson/magenta teardrop with a small orange bead sits in
  the socket region (2,185 px, bbox 913, 604 – 958, 694). The clay there shows overlapping
  brow plates and no lens recess; the control is a thicket of plate edges.
- **D9's form landed and its colour did not.** The tongue — geometry confirmed present and
  visible in Task 1 — is painted in **slate blue-grey**, D11's declared colour, on D9's
  declared surface. At pair scale the swap ran the other way. Two declared elements share one
  cavity and neither reliably owns its surface.

## What this companion does NOT establish

Nothing about whether the route works on a beast — no twin, no atlas, no projection, no bake
has consumed it, and none may. It is not a baseline for anything, it is not comparable to the
rejected first pair, and its eye-region reading rests on **one generation**.
