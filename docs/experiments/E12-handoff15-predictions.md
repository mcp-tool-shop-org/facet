# E12 handoff 15 — predictions, registered before the run to Gate 1

**Executor session, 2026-08-07.** Written **before** the no-LoRA path was written, before the
anchor ran, before the sweep re-ran, before any emit, any stroke, any commit, finalize or pack.

**Blind status per item** — BLIND / DERIVED / CODE-READ, as in handoffs 13 and 14. Read to
write this: `CLAUDE.md`, Rulings 7, 24, 25 (a–g), `profiles/beast.json` post-25 (thin-extent
0.005 live, `texpass_brush` cleared), the handoff-14 report, `docs/experiments/
E13-brush-prompts.json`, `E04-ruling.md` Ruling 23, the ship's recorded stroke graph
`E04_stroke/out/stroke_1_y+300_e+00_workflow.json`, and the sources of `brush_cloud_step.py`,
`texpass_iter.py`, `texpass_finalize.py` and `e04_registry_sweep.py`. Nothing has been run.

---

## The arithmetic this run is measured against

Ruled at 24e/25d: valid **3,240,510** · reach **1,635,304** (50.46%) · stage 1 styled
**1,430,687** (**44.15%** of valid, 87.5% of reach) · brush set **204,617** · four strokes
close **146,506** (71.60% of it) · **58,111** to dilation from the brush set · **1,605,206**
unreachable · **19,846** closable by no eye-level camera at all.

The greedy attributed closures in *greedy* order (337.5 → 52,568; 180 → 43,312; 45 → 30,965;
292.5 → 19,661). **The run uses the SPIRAL order**, whose simulated attribution is different
and is what the strokes should be scored against:

| stroke | camera | painted-adjacency | simulated closes |
|---|---|---|---|
| 1 | 292.5 | 92.34% | 41,374 |
| 2 | 337.5 | 87.93% | 31,864 |
| 3 | 180.0 | 87.72% | 42,345 |
| 4 | 45.0 | **81.87%** | 30,923 |

## P1 — step 0 (Task 0)

- **P1a — CODE-READ. The byte-identity anchor HOLDS.** `build_graph` will keep the card
  branch untouched, so the ship's recorded 17-node graph rebuilds exactly:
  node 5 `LoraLoaderModelOnly` at `strength_model 0.75`, node 6 reading `["5", 0]`, seed
  770700 / steps 20 / cfg 2.5, cn 1.0, the two content-hash LoadImage names. If it does not,
  E13 halts before a single stroke.
- **P1b — DERIVED. The sweep returns 0 UNDECIDED, exit 0.** Ruling 25c transcribed the last
  one. Named risk: the sweep may find something *else* undecided that nobody was tracking —
  `texpass_brush`'s block was cleared by a ruling written in prose, and prose is not a
  registry. I give 80% to a clean 0 and 20% to at least one surprise key. **Either outcome
  halts or proceeds by its own rule; I do not tune past it.**
- **P1c — CODE-READ. The no-LoRA graph is 16 nodes, not 14.** The twins' no-LoRA graph is 14
  because it is a different graph (canny ControlNet, no inpainting mask chain). Dropping node
  5 from the brush's 17 leaves **16**, with `ModelSamplingAuraFlow` reading `["1", 0]`.

## P2 — per-stroke closure (Task 1)

- **P2a — DERIVED. Every stroke closes FEWER texels than its simulated attribution**, because
  the simulation modelled commit's geometry (facing, visibility, edge distance) but not its
  content tests: commit also requires the brush's output to actually differ from the render it
  was given, and rejects paint that keys as background. Predicted realised/simulated ratio
  **0.75–0.95** per stroke.
- **P2b — DERIVED. Total closed across four strokes: 110,000–139,000** (75–95% of 146,506),
  i.e. **3.4–4.3 points** of valid.
- **P2c — DERIVED. thin_extent 0.005 withholds 2–6% of each stroke's emit figure.** The ladder
  measured 4.0% of the figure at yaw 337.5; the other three are the same class of silhouette.
  If any stroke's withheld fraction exceeds 10% the guard is not doing what Ruling 25c ruled it
  to do, and that is reportable as a firing rather than as noise.
- **P2d — DERIVED. Painted-adjacency verified at run time will match the simulation within
  ±3 points** on all four. It is recomputed against the *actual* accumulating state, which by
  stroke 2 contains stroke 1's committed paint — the simulation modelled exactly that, so a
  large divergence would mean the simulation's adjacency model is wrong.

## P3 — the register question (the named risk)

- **P3a — BLIND. The brush HOLDS the register on strokes 1–3 and stroke 4 is the exposed
  one.** Grounds: yaw 45 has the lowest anchor (81.87%), and it runs last, so its mask sits
  against three strokes' worth of new paint rather than only stage 1's.
- **P3b — BLIND, and this is the item I most want on the record. What drift would look like,
  named before I see any of it:** (i) a **gloss/CG-smooth** patch where the surrounding paint
  is matte scaled hide — the crop pass's measured signature; (ii) **palette drift into
  undeclared families** — the crop pass produced slate crowns, a rust frill and a 22,420 px
  scarlet mass, so scarlet/pink/slate on a green-declared surface is the specific thing to
  look for; (iii) a **visible seam at the mask boundary**, brush paint meeting stage-1 paint
  with a step in value or hue; (iv) at worst, **a new animal** — the full-denoise failure the
  spiral order exists to prevent, which would show as anatomy that does not continue the
  surrounding structure.
- **P3c — DERIVED. The frame is NOT the risk this time.** The crop pass's drift was measured
  at a bust frame; the strokes run at the route's own 1792×1024. What differs from the twins is
  **denoise 1.0 inside the mask** against the twins' 0.92 over the whole image, so if drift
  appears it should be attributed to full denoise, not to framing — and the check that
  separates them is whether the drift is confined to the mask.
- **P3d — pre-registered procedure, not a prediction: I will look at stroke 1's output before
  running strokes 2–4.** If it shows (i)–(iv), the remaining three do not run and the halt is
  the report.

## P4 — the gates per stroke

- **P4a — DERIVED. 16e off-palette per stroke frame: 4–25%.** The v9 twins ran 4.82–23.91% and
  the stroke frames are the same route frames over largely the same paint.
- **P4b — DERIVED. 17d achromatic 6–17%**, the v9 band (8.36–16.37%) widened slightly because
  a stroke frame is mostly stage-1 paint with a small new region.
- **P4c — DERIVED. The gate cannot isolate the stroke.** Both channels measure the WHOLE
  frame, of which the brush's contribution is ~1–3% of the figure, so a stroke-sized defect is
  below their resolution. **They are reported and they will not decide anything**; the
  same-frame clay | pre | post sheet is what can see a stroke. Registered now so a quiet gate
  is not later read as a pass.
- **P4d — DERIVED. Re-rolls: 0 or 1 of 4 spent.** No seed-resistance map exists for the brush
  lane on this subject, and 770700's known resistances (view 3's limb, view 4's terms) are
  twin-stage facts at different frames.

## P5 — finalize, pack and the mix

- **P5a — DERIVED. Finalize's dilation fills 1,655,000–1,700,000 texels** — the 1,605,206
  unreachable plus whatever the four strokes leave of 58,111. It cannot fill more than valid
  minus painted.
- **P5b — DERIVED. Final mix, quoted against THIS subject's geometry and not another's raw
  mix: styled 44.1% / brush 3.4–4.3% / dilation 51.6–52.5% of valid.** The ship ran
  36.89/6.87/56.24 and the character 68.8/4.2/27.0. This subject sits between them on styled
  and **below both on brush**, and the reason is geometry rather than regression: half of a
  winged quadruped is self-occluded (49.54% of valid is unreachable by any eye-level camera),
  so dilation's share is set by the animal's shape before any tool runs. Reading this subject's
  56% dilation as "worse than the character's 27%" would be the wrong-denominator error the arc
  keeps paying for.
- **P5c — DERIVED. Dilation is the majority provenance of this asset**, and I am registering
  that before the sheet exists so it is not a surprise at Gate 1. The five-column sheet's
  provenance panel will be mostly dilation-coloured, and the honest question at the gate is
  whether that *reads* acceptably, not whether the number is small.

## P6 — Gate 1's sheet

- **P6a — BLIND. The head is where the Director's eye goes first**, and A2's banked finding
  (0.815 texels per full-figure head pixel — the atlas under-resolves the head at the route
  frame) predicts the head reads softest at 3× even though nothing in this run touched it.
- **P6b — BLIND. The wing membranes read as the most-changed region** between stage 1 and the
  final asset, because the brush's territory is their trailing edges and the strokes were
  chosen to reach exactly those.

## What would falsify each

P1a: any byte delta on the card path. P1b: any UNDECIDED. P1c: a node count other than 16.
P2a: any stroke closing MORE than its simulation. P2b: outside 110k–139k. P2c: any stroke
withholding >10%. P2d: adjacency off by >3 points. P3a: drift on strokes 1–3, or none on 4.
P4a/P4b: outside the bands. P4d: 2+ re-rolls. P5a/P5b: outside the ranges.

**No verdicts here and none in the report. Gate 1 is the Director's.**
