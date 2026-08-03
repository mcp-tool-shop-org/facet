# E05 — Gate 0

**Run:** 2026-08-04, executor session. Arms U3 and U1, per [the spec](E05-paint-more-surface.md) §5.
**Halt:** neither cheap arm met the pass condition. U2 and U4 were not started.

Evidence only. The advisor rules.

---

## The metric table

All three arms measured by one tool, [`tools/diagnostics/texpass_metrics.py`](../../tools/diagnostics/texpass_metrics.py),
so they are comparable by construction. U0 is E02 as shipped, re-measured through the same
tool rather than quoted.

| metric | **U0** (E02) | **U3** (`facing-min` 0.10) | **U1** (native xatlas UVs) |
|---|---|---|---|
| islands | 34,783 | 34,783 | **16,684** |
| faces / island | 8.3 | 8.3 | **17.2** |
| atlas coverage | 18.76% | 18.76% | **24.81%** |
| valid texels | 3,147,261 | 3,147,261 | 4,162,543 |
| stage-1 holes | 2,613,073 | 2,613,073 | 3,475,359 |
| **closed by brush** | **711,183 (27.2%)** | **750,348 (28.7%)** | **923,466 (26.6%)** |
| closed by dilation | 1,901,890 (72.8%) | 1,862,725 (71.3%) | 2,551,893 (73.4%) |
| colourless islands | 14,132 / 25,878 (54.6%) | 13,850 / 25,878 (53.5%) | 8,031 / 15,228 (52.7%) |
| **hole texels in colourless islands** | **75.0%** | **74.9%** | **60.8%** |
| styled / valid after loop | 39.6% | 40.8% | 38.7% |
| styled / reachable (stage 1) | 53.7% | 53.7% | 53.6% |
| speckle > 0.10 | 2.93% | 2.86% | **2.61%** |
| speckle > 0.15 | 1.31% | 1.28% | **1.03%** |
| speckle > 0.25 | 0.34% | 0.33% | **0.19%** |

A0 reference for speckle: **2.43 / 1.18 / 0.30**.

**Against the spec's pass condition** — *brush-painted share rises materially above 27%
**and** colourless islands fall*:

- **U3** — brush share 27.2% → 28.7% (+1.5 pp), colourless islands 54.6% → 53.5%. Does not pass.
- **U1** — brush share 27.2% → **26.6%**, i.e. it fell. Does not pass.

§5 says halt in that case, so U2 and U4 were not run.

### What U1 did move, even though it failed the stated condition

Recorded because the two clauses of the pass condition came apart. U1 did not touch the
brush/dilation ratio, but it moved the artifact mechanism and the Director's own complaint:

- hole texels in colourless islands **75.0% → 60.8%** (−14.2 pp)
- speckle below A0 at two of three thresholds (1.03 vs 1.18, 0.19 vs 0.30), where U0 was
  worse than A0 at all three
- islands 34,783 → 16,684, atlas coverage 18.76% → 24.81%, and it is free

### A correction to a number in the E02 ruling

The ruling puts hole texels in colourless islands at **31%**. That figure came from the
constrained-fill A/B (590,928 mean-fallback texels). Measured directly, it is **75.0%**.

The gap is `bake.margin = 8`: the baked `valid` mask extends 8 px past each island's
triangles, and the gutter is 4 px, so **adjacent islands' valid regions overlap**. An
island-constrained fill therefore still leaks — it just leaks through the bake margin
instead of the gutter. The 31% figure describes islands whose margin-dilated region touches
no styled texel; 75.0% describes islands containing no styled texel. Both are true of the
same atlas; the second is the one the artifact mechanism is about.

---

## Why neither lever moved the ratio

### The commit funnel — visibility is the constraint, not acceptance

[`tools/diagnostics/commit_funnel.py`](../../tools/diagnostics/commit_funnel.py) replays
commit's five tests on one job and counts survivors. Stroke 1 (`y+045`), against the
stage-1 hole set:

| stage | U0 (`facing-min` 0.25) | U3 (`facing-min` 0.10) |
|---|---|---|
| 0 hole ∧ valid | 2,613,073 | 2,613,073 |
| 1 facing test | 1,013,253 (−61.2%) | 1,173,512 (−55.1%) |
| 2 **visible from this camera** | **349,761 (−65.5%)** | **388,868 (−66.9%)** |
| 3 inside the job mask | 261,957 (−25.1%) | 282,409 (−27.4%) |
| 4 edge distance → committed | 195,519 (−25.4%) | 205,225 (−27.3%) |
| survival | 7.5% | 7.9% |

Widening acceptance added **160,259** texels at stage 1 and only **9,706** reached the
atlas — a **6% pass-through**. Texels that barely face a camera are overwhelmingly also
occluded or near the silhouette, so the tests downstream take back what the widening
gave. Visibility is the dominant filter at either setting.

### The occlusion is mid-scale, not micro-noise and not only pose

For the facing-passing hole texels at `y+045`, distance from the texel to whatever blocks it:

```
p10 0.00234   p25 0.00892   p50 0.03068   p75 0.07755   p90 0.11877
blocker within 1 median edge length (0.0029):   11.7% of blocked
blocker within 3 edge lengths      (0.0087):   24.4%
blocker within 10 edge lengths     (0.0290):   48.9%
```

Raising the ray's normal offset 16× (0.0015 → 0.024) lifts visibility only 34.5% → 45.8%,
so micro-scale self-occlusion is real but modest. The median blocker sits at **3% of figure
height** — folds, crevices, the gap behind the beard, between fingers. A camera cannot see
into a closed fold no matter where it is placed.

### The exterior ceiling — what U2 could ever buy

Fraction of the stage-1 hole set reachable by *any* camera in a set (facing > 0.25, visibility tested):

| camera set | reach |
|---|---|
| E02's 8 cameras | 894,309 (**34.2%**) |
| **U2's 14 cameras** (12 yaws at 30° + 2 elevations) | 938,595 (**35.9%**) |
| 46-camera sphere | 1,045,532 (40.0%) |
| 46-camera sphere, facing > 0 | 1,071,915 (**41.0%**) — the exterior ceiling |

U2 buys **+1.7 percentage points of reach** for six extra strokes, and no camera-based
scheme of any size passes ~41%. E02 already commits 27.2% against a 34.2% reach, so the
remaining headroom at these cameras is the job-mask and edge-distance tests, not coverage.

### Half the atlas is surface no camera can see

Over **all** valid texels, not just holes:

```
valid texels                            3,147,261
visible from ANY of 46 exterior cameras 1,606,103 = 51.0%
never visible from outside              1,541,158 = 49.0%
outward-ray escape (the E02 measure)                36.5%
```

The two independent measures agree in direction and scale. Roughly half of what the atlas
is spending texels on is not on the outside of the model.

---

## What ran

```
# U3 — one change from U0
tools/texpass_loop.ps1 ... -CommitFacingMin 0.10 -From 1 -To 8 -SeedState -SkipFinalize
# U1 — one change from U0
blender -b -P tools/bake_hero_prep.py -- --glb facet_E01/tex_W3/W3_287k.glb \
        --outdir facet_E05/U1/prep --keep-uvs --pack-margin 0.001
python tools/project_twins.py --prep facet_E05/U1/prep --front twinsF/w3clay_0.png \
        --back twinsF/w3clay_4.png --out facet_E05/U1/styled_stage1.png
tools/texpass_loop.ps1 ... -Prep facet_E05\U1\prep -From 1 -To 8 -SeedState -SkipFinalize
```

Both arms: same twins, same prompts, same order, same seed 770700, same `--thin-extent 0.03`,
then `texpass_finalize` + `bake_hero_pack` + one FLAT front render. Loop wall clock 8.0 min
per arm; U1 adds ~2 min for prep and stage 1. No ANDON fired in either arm.

**Artifacts:** `E:\AI\training\facet_E05\{U1,U3}\out\` (atlas + GLB), `metrics\{U0,U3,U1}.json`,
`logs\`.

**New in the repo:** `--keep-uvs` on `bake_hero_prep.py` (default off, U0 path byte-unchanged);
`-CommitFacingMin` on `texpass_loop.ps1` (defaults to the E02 value);
`tools/diagnostics/texpass_metrics.py`; `tools/diagnostics/commit_funnel.py`.

---

## Open questions the data raised

1. **The pass condition's two clauses came apart.** U1 lowered colourless-island hole texels
   by 14.2 points and put speckle below A0 at two thresholds while the brush ratio *fell*.
   Whether "more real paint" or "interpolation that stays inside a coherent region" is the
   thing that matters is a judgement the numbers do not make.

2. **The exterior ceiling is ~41% and E02 reaches 27%.** Whether the remaining 14 points are
   worth pursuing through the job-mask and edge-distance tests, or whether ~41% is simply too
   low a ceiling to build a texture route on, is the fork this gate exposes.

3. **Half the atlas is interior surface.** This is the spec's out-of-scope hypothesis arriving
   with a number attached: 49% of valid texels are invisible from outside, and the 37% outward-ray
   escape figure from E02 says the same thing a different way. It also explains the unwrapper
   result without appeal to the unwrapper — charts cannot be large on a surface that is half
   interior, which is why xatlas at 20.5 faces/island and `smart_project` at 8.3 are both far
   from a hand-unwrapped character's tens of islands.

4. **U1 is free and its own path is untested downstream.** It was measured only at Gate 0
   metrics; no finished asset was rendered beyond the single FLAT front view the speckle
   number needed.
