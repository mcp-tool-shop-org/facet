# Status of every tool

*Measured, not asserted. Nothing here is marked working unless it produced an
artifact a human looked at. Moved off the [README](../README.md) by the E19
treatment; the content is unchanged.*

---

<!-- Moved out of README.md by the E19 treatment, 2026-08-08, at the Director's
     word ("the readme reads more like a changelog"). NOT rewritten: every line
     below is byte-identical to the README it left, corrections and ⚠ annotations
     intact. The README now links here. -->

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
| `project_twins.py` | projects the styled twins onto the atlas, emits a hole map | N-view since `c469b36`; trust mask ∧ exact silhouette by default (E08 A27) with a registration halt at IoU < 0.80; eight cameras land 68.8% of valid / 92.9% of reachable, anchors pixel-identical back through A2 |
| `texpass_iter.py` | emit/commit write-head for progressive texture fill | selftest: styled texels byte-identical (delta 0.000000), holes strictly shrink |
| `texpass_brush.py` | drives local ComfyUI — Qwen + style LoRA + inpainting ControlNet | ~45 s per stroke |
| `texpass_finalize.py` | dilation fill for residual holes | closed 868k texels with zero mean fallback |
| `texpass_loop.ps1` | the whole loop: reset, eight strokes, finalize, render | ~8 min per character, unattended |
| `bake_hero_{prep,fuse,pack}.py` | multi-view baker — depth-tested visibility, per-texel ownership, seam levelling | kills through-projection: a raised sword no longer bakes onto the chest behind it |
| `resample_atlas.py` | nearest-surface texture transfer between topologies | replaces Blender's ray bake, which returned a black atlas when rays were cast from a seam-split mesh |
| `restylize_views.py` | generates a mesh's own twins — builds the control image, saves the exact figure mask beside each twin | silhouette IoU **0.290 → 0.777**; per-view prompts take face detections on the rear view 1 → 0 |
| `cull_unseen.py` | classifies faces by exterior visibility so the atlas can skip them | 47.6% of faces unseen by 46 cameras; interpolation down **68%**; gated on first-hit **depth**, not silhouette |
| `texpass_provenance.py` | replays the commit chain offline to tell you, per texel, whether colour came from a twin, a specific stroke, or dilation | reproduces live commit counts to the texel; settled the blotch question without a GPU. ⚠ *Corrected 2026-08-05: the replay predates E08 A32 and over-claims +358 commits on the galleon (the missing `fm_e & hit` intersect — [report](docs/experiments/E10-offsurface-consumers-report.md)); the A32-faithful replay is `diagnostics/e10_claim_replay.py`; fix queued for the tool's next use* |
| `e11_export_turnaround.py` | dense-turnaround export — emit-orchestrated flat renders + exact silhouettes + born-indexed class maps + owner slices, per camera, as a sha-linked self-contained tree | export proven a pure function; beam channels byte-anchored to the record; both subjects' trees validate through the sdlab lane 28/28 and 26/26 ([E11-report.md](docs/experiments/E11-report.md)) |
| `e11_manifest.py` | the lane-contract manifest for an export tree | validated by the lane's own codebase on both subjects; the lane's palette gate reproduced the staged manifest's blob digits from fresh renders |

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
apart by different tools are still comparable. `gate0_sheet.py` and `gate1_sheet.py`
build the designation and acceptance sheets (full size, concept beside geometry,
ranking nothing). The E12 arc added per-subject instruments under `tools/diagnostics/`
— frame derivation asking every rendered yaw (`e12_frame.py`), head-region evidence
with the box drawn back onto every view (`e12_head_evidence.py`), non-manifold-edge
location (`e12_nonmanifold.py`), the thin-extent cost curve (`e12_thin_curve.py`),
elevated-camera coverage (`e12_elevated.py`), the subject-flagged off-surface
classifier validated against the ship's ruled number before first use
(`e12_offsurface.py`), and a two-class argparse help linter that gates rather than
informs (`e12_help_format_scan.py` — literal `%` and non-cp1252 glyphs; it found six
sites where a hand-search knew four, one of which could not crash at all).
