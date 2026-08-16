# Grok session handoff — 2026-08-16

> ⚠ **ADVISOR BANNER, added at the reconciliation fold (2026-08-16, later the same
> day):** this handoff was written by the channel between build rounds 3 and 4 and
> several state lines below are already superseded — round 4 shipped (t82; the next
> free number moves with the tree, check `tests/` before taking one), the count
> surfaces are committed at **1166/1121**, the E45 bundle exists and E45 is closed
> (`docs/experiments/E45-warp-and-aov-report.md`), briefs now run to #8, and the
> E46 runner seat owns the S3 run. The policy section and the three-world readout
> below remain the channel's own record and stand as written.

Read this before doing anything. The repo is the record. This file is the
next-session start, not a ruling.

Grok does **not** carry this conversation into a new chat unless
`--experimental-memory` / `[memory] enabled` is on (experimental, off by
default). Do not assume prior Grok turns are in context.

## Who you are in this tree

Outside consult + build channel. Six nominated calibration claims held to
the digit. Folded through `9cbe957` (S3 compositor). Flow estimator and
S3 runner are **uncommitted** in this working tree.

Do **not** modify: `project_twins.py`, `texpass_*`, `callieri_border.py`,
`s3_composite.py`. Do **not** touch in-flight E45 files:
`tools/emit_view_aovs.py`, `tests/test_t78_emit_view_aovs.py`,
`tools/twin_mesh_warp.py`.

Next Grok test file starts at **t81**.

## Open the tree

```
cd E:\AI\facet
git log --oneline -3
git status -sb
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py verify
```

Use `--basetemp=<scratch>` if pytest hits a Windows `pytest-current` symlink
error.

## What is true (measured)

- **S0 dead:** FLAT + Standard vs twin, 6.1/255 mean; both equally wrong.
  Colour management is not the look.
- **S1 dead as appearance:** welded vs shipped clay, 1,034 / 151,705 px,
  max channel delta 3. Soup never touched shading (GLB has explicit
  normals). Weld still useful (2,654 charts vs 146,462).
- **S2 skipped** (diagnostic-only after S0/S1).
- **Blend-variant sheet** was structurally incapable (298–813 px rewritten).
- **Island rims** 16.3% of atlas, 116 screen px. Not the look.
- **Callieri border** we had closed was the wrong quantity (material ΔE).
  Real border is depth-discontinuity + image border. Built.
- **Live lead:** local twin-to-mesh warp. One view, silhouette-only,
  window-pinned, instrument rebuilt as E45. Not a finding yet.

## What Grok built

| module | role | calibration | tests |
|---|---|---|---|
| `tools/callieri_border.py` | Callieri mask + mixed-depth reject + facing | `border_weight[32,32] == 2/3` | T76, folded |
| `tools/s3_composite.py` | S3 existence proof (VD + VI + disagreement) | `red[16,16] == 0.640625` | T77, folded at `9cbe957` |
| `tools/flow_estimate.py` | flow field for the S3 hook | `flow_x[32,32] == 3.0` | T79, **uncommitted** |
| `tools/s3_run.py` | load E45 AOV bundle, run S3 | missing `--aov` exits 4 | T80, **uncommitted** |

Verify the uncommitted estimator before trusting it:

```
E:\AI-Models\trellis2-env\Scripts\python.exe tools/flow_estimate.py --selftest
```

Must print `calibration flow_x[32,32] == 3.0`.

## Policy already argued (do not re-litigate unless evidence moves)

- S3-A primary is **target-first**, not global highest-facing
  (`primary_mode='facing'` exists if they want shipped WTA).
- S3-B is unsmoothed per-surfid argmax. Waechter seam-level is a later
  per-surfid colour offset, not a per-still reassignment.
- Disagreement ≠ warp instrument. `flow` is how warp enters S3.
- Twin-vs-control confounds licensed ControlNet slack with geometric warp.
  Prefer **depth-edge vs twin-edge** when AOVs exist (`pair='edge'`).
- Dense LK, sparse confidence. Do not interpolate into no-signal regions.
- Blend in sRGB (shipped space). Linear-light is polish, not the
  three-world split.

## Three-world S3 readout

| composite | disagreement | meaning |
|---|---|---|
| clean | low | plates compose; 3D path degrades them |
| blotchy | high | sources inconsistent (warp lead) |
| blotchy | ~0 | plates share the defect; this module cannot see it |

## Next work (cheapest first)

1. Advisor folds uncommitted flow estimator + s3_run (and t78 if that seat
   is done). Re-count: collect-only was **1136 / 1091** with t78 **and**
   t79/t80 in the tree. If t78 moved, re-count before pinning T34.
2. When E45 AOV bundle is accepted, run
   `s3_run.py --aov E:\AI\training\facet_E45\aov --out <scratch>`
   **flow off**. That is S3. Label a real-twin flow run a demonstration,
   not a measurement. Do not tune `flow_estimate` against E45 tile numbers.
3. If S3 is blotchy + high disagreement, apply flow only where
   `confidence > 0` and A/B the compositor (flow off vs on).
4. Do not reopen UVAtlas / PartUV / retopo until S3 has failed the eye
   after a measured warp correction.

## Namespace

T-numbers are unique per file. t76/t77 shipped. t78 is the E45 emitter
(in flight). t79 = flow_estimate. t80 = s3_run. Next Grok file: **t81**.

## Briefs

`docs/grok-consult-1-brief.md` … `docs/grok-consult-6-brief.md`
`docs/experiments/E45-warp-and-aov-kickoff.md`
`docs/experiments/E44-the-atlas-plan.md` — diagnostic table partly void
`CLAUDE.md` — the law book
