# E06 — report

**Spec:** [E06-cull-the-unseeable.md](E06-cull-the-unseeable.md) · **Ruling:** [E06-ruling-gate1](E06-cull-the-unseeable.md)
**Run:** 2026-08-04, executor session, all local on one RTX 5090.
**Amended mid-run:** Gate 0 ruled *stop deleting faces, exclude them from the atlas.*

Evidence, not argument.

---

## What ran

| | |
|---|---|
| mesh | `facet_E01/tex_W3/W3_287k.glb` — W3, welded, decimated, 287,170 faces, carrying the generator's native xatlas UVs. **Never modified by this experiment.** |
| twins | `facet_E01/tex_W3/twinsF/w3clay_{0,4}.png` + saved masks (unchanged from E02) |
| recipe | [E02-prompts.json](E02-prompts.json) — same eight prompts, same order, same negative, seed 770700, `--thin-extent 0.03`, `--facing-min 0.25`. **The E02 pipeline ran unchanged.** |
| visibility | 46-camera sphere ∪ 26 production cameras (24 yaws at 15° + the two `+55` strokes), 4 samples/face, ∪ rasterisation from the production cameras at 1504 px, 1 ring dilation |

```
python tools/cull_unseen.py --glb facet_E01/tex_W3/W3_287k.glb \
       --out facet_E06/W3_visible.npy --cameras 46 --rings 1 --samples 4

blender -b -P tools/bake_hero_prep.py -- --glb facet_E01/tex_W3/W3_287k.glb \
       --outdir facet_E06/C1/prep --visible-mask facet_E06/W3_visible.npy --pack-margin 0.001

python tools/project_twins.py --prep facet_E06/C1/prep --front twinsF/w3clay_0.png \
       --back twinsF/w3clay_4.png --out facet_E06/C1/styled_stage1.png
blender -b -P tools/bake_hero_pack.py -- --prep-glb facet_E06/C1/prep/prep_uv.glb \
       --atlas facet_E06/C1/styled_stage1.png --out facet_E06/C1/stage1_C1.glb

tools/texpass_loop.ps1 -Tools E:\AI\facet\tools -Prep facet_E06\C1\prep \
       -StateDir facet_E06\C1\state -Glb facet_E06\C1\stage1_C1.glb \
       -Stage1Atlas facet_E06\C1\styled_stage1.png -OutDir facet_E06\C1\out \
       -PromptsJson docs/experiments/E02-prompts.json -ThinExtent 0.03 \
       -CommitFacingMin 0.25 -From 1 -To 8 -SeedState -SkipFinalize

python tools/texpass_finalize.py --state facet_E06\C1\state --prep facet_E06\C1\prep \
       --out facet_E06\C1\out\atlas_final.png
blender -b -P tools/bake_hero_pack.py -- --prep-glb facet_E06\C1\prep\prep_uv.glb \
       --atlas facet_E06\C1\out\atlas_final.png --out facet_E06\C1\out\W3_C1.glb
```

Wall clock: classify 20 s · prep 118 s · stage 1 11 s · eight strokes 481 s · finalize 31 s ·
pack 24 s · Stage E renders 141 s · provenance replay 54 s. **~14.5 min end to end.**

**Adopted from E05, not an arm here.** `bake_hero_prep` no longer discards the generator's
atlas: native UVs are the default and `--reunwrap` is the escape hatch that reproduces the
historical `smart_project` path.

---

## Measurements

### The cull, as a classification

```
faces                287,170   ->   152,096 visible (53.0%),  135,074 unseen
  point test, 46-camera sphere alone      144,454  (50.3%)
  point test, sphere UNION production     145,104  (50.5%)   production adds 650
  raster, 26 production cameras @1504px   127,837  (44.5%)
  UNION of both tests                     145,674  (50.7%)   raster adds 570 the point
                                                             test missed; the point test
                                                             adds 17,837 the raster missed
  + 1 ring dilation                       152,096  (53.0%)
sensitivity: 92-camera sphere             +1.4 points raw over 46
```

Geometry untouched. Unseen faces are parked on one shared 10×10-texel patch in a reserved
strip; the visible set is unwrapped and packed alone.

### The arm table

| metric | **U0** (E02) | **U1** (native UV) | **C1** (culled) |
|---|---|---|---|
| valid texels | 3,147,261 | 4,162,543 | 2,402,810 |
| atlas coverage | 18.76% | 24.81% | 14.32% |
| stage-1 holes | 2,613,073 | 3,475,359 | **1,721,598** |
| **painted by the brush** | 711,183 | **923,466** | 907,825 |
| **closed by dilation** | 1,901,890 | 2,551,893 | **813,773** |
| brush share of holes | 27.2% | 26.6% | **52.7%** |
| colourless islands | 54.6% | 52.7% | **39.0%** |
| their share of hole texels | 75.0% | 60.8% | **50.7%** |
| styled after the loop | 39.6% of valid | 38.7% | **66.1%** |
| exterior-invisible texels | — | 49.8% | **15.0%** |
| speckle >0.10 / >0.15 / >0.25 | 2.93 / 1.31 / 0.34 | 2.61 / 1.03 / 0.19 | 2.64 / 1.07 / 0.23 |
| final atlas variance | 0.03013 | 0.03032 | 0.03607 |

A0 speckle reference: **2.43 / 1.18 / 0.30**.

**Interpolation fell 68%** — 2,551,893 → 813,773 dilated texels.

**Against the spec's absolute pass condition:** exterior-invisible **15.0%**
(360,245 / 2,402,810 = 14.99%) meets `< 15%` by 0.01 points; brush texels **907,825**
misses `> 923,466` by **15,641 (1.7%)**. Recorded as a miss.

### Predicted vs measured

| §3 prediction | outcome |
|---|---|
| roughly double texel density on visible surface | **partial** — ~17% more (U1 3,475,359 × ~50% visible ≈ 1.74M; C1 2,402,810 × 85% ≈ 2.04M) |
| merge charts, islands well below 16,684, faces/island above 17.2 | **FALSIFIED** — see below |
| brush share 27% → 65–70% | **partial** — 52.7% |
| cut colourless islands sharply | **supported** — 54.6% → 39.0%, their hole share 75.0% → 50.7% |

### Charts fragment; they do not merge

```
native charts, ALL faces      14,010  over 287,170 faces = 20.5 faces/chart
native charts, VISIBLE only    9,276  over 152,096 faces = 16.4 faces/chart
chart bbox FILL               42.1%  ->  36.6%
packed atlas coverage         24.81% ->  14.32%
```

Removing 47% of the faces removed only 34% of the charts, so faces-per-chart **fell**. The
mechanism is measurable: invisible surface is interleaved *within* charts, so excluding it
punches holes in them — a chart keeps its outer extent while losing interior area, which is
the bbox-fill drop, and that is why packed coverage went down even though far fewer faces
are packed. This is the cost that ate most of the predicted density gain.

### Blotch provenance — the Director's question, measured

Every texel in the finished asset has exactly one origin. The per-stroke claim is
reconstructed by replaying `texpass_iter.commit`'s filter chain offline from the saved job
directories; the replay reproduces the live commit counts exactly (224,910 / 147,411 /
127,964 / 127,699 / 35,457 / 44,671 / 138,766 / 60,947), which is what makes it usable as
evidence rather than an estimate.

Whole atlas, 2,402,810 valid texels: **TWINS 28.4%**, brush strokes 37.7% combined
(s1 9.4 · s2 6.1 · s3 5.3 · s4 5.3 · s5 1.5 · s6 1.9 · s7 5.8 · s8 2.5), **DILATION 33.9%**.

Head render at the Director zoom — 490,544 figure px, of which 3,533 (0.72%) are blotch
(`|luminance − local median| > 0.10`):

| provenance | share of BLOTCH px | share of CLEAN px | enrichment |
|---|---|---|---|
| **TWINS** | 13.8% | 57.3% | **0.24×** |
| BRUSH, all eight | 62.0% | 37.7% | 1.64× |
| **DILATION** | 24.0% | 5.0% | **4.80×** |

Per region the Director named:

| region | blotch px | provenance of those blotch px |
|---|---|---|
| forehead | **2** | region is 57.1% twins / 36.1% stroke 7 and essentially clean |
| temple (his right) | 106 | stroke 6 **34.9%**, dilation **32.1%**, stroke 7 26.4%, twins 5.7% |
| beard streaks | 39 | stroke 1 35.9%, twins 30.8%, stroke 2 23.1%, dilation 2.6% |
| chest / tunic | 3 | dilation **100%** |

**The twins do not carry that grime.** Twin-painted texels are four times *less* likely to
be blotchy than the surface average; dilation-filled texels are nearly five times *more*
likely, while being only 5% of clean pixels. `twin_front.png` at the matched region and zoom
shows smooth flesh and a clean beard (`facet_E06/PROV_sheet.png`).

Two specifics worth separating from the rest:

- **The forehead "seam" is not a blotch.** Two blotch pixels in the whole disc. It is a
  provenance *boundary* — twin paint below, the `y+000_e+55` overhead stroke above — so it
  is a tonal step where two sources meet, not a defect in either.
- **The temple patch and the tunic specks are dilation**, i.e. colour arriving across the
  gutter from whichever island the packer placed beside them. That is the artifact class
  E02's ruling named, still present at reduced scale.

---

## What failed

- **`cull_unseen.py` v1 deleted faces and was withdrawn at Gate 0.** Silhouette IoU returned
  **1.00000 at all eight cameras** on a mesh with a 0.297 hole clean through it, because the
  ray behind a removed face still hits geometry and the pixel still reads as figure. A
  first-hit depth comparison, added before reporting, fired immediately: 262 px receding at
  yaw 225, 208 px at yaw 135.
- **The visibility camera set was not a superset of the production set.** A 46-camera sphere
  puts 12 yaws at 30° on the equator, so all four diagonal turnaround cameras and both
  elevated strokes were absent — six of ten. 228 faces visible from a production camera were
  culled. Unioning them in costs 0.08% (150,568 vs 150,340) and left **151 px** still
  receding.
- **Point-sampling a face cannot represent partial visibility.** A face half-hidden behind an
  arm is visible, but if none of its four sample origins lands in the exposed sliver it is
  classified unseen. Fixed by unioning with a rasterisation from the production cameras;
  residual fell 151 px → **7 px**.
- **The face-centroid checksum was too brittle to be a guard.** `AssertionError: ANDON:
  face-centroid checksum mismatch … 22dae3da… vs deed453e…` on a *correctly aligned* mask:
  Blender reads float32 `polygon.center` where the mask is built from trimesh float64
  vertices, and the two agree to 5.6e-8 — geometrically nothing, but enough to straddle the
  5-decimal rounding boundary on thousands of values. Replaced with a positional comparison
  against shipped centroids (measured deviation **5.96e-08**; tolerance 1e-4).
- **`trimesh.graph.connected_components(..., node_count=nf)`** →
  `TypeError: unexpected keyword argument 'node_count'` on trimesh 4.12.2; the parameter is
  `nodes`.
- **The recession gate's unit was wrong, and it was changed — the threshold was not.** A
  pixel count at zero is unachievable by construction: the residual **grows** with gate
  resolution (28 faces at 1880 px, 66 at 3008 px), because a finer grid always finds another
  sliver. Area converges, and under UV-exclude a missed face costs a flat patch of exactly
  its own area. Limit 0.5% of visible area; measured **0.155%**.

No ANDON fired during prep, the eight strokes, finalize or pack.

---

## Open questions the data raised

1. **Chart fragmentation is now the binding constraint.** It ate most of the predicted
   density gain, its mechanism is measured (bbox fill 42.1% → 36.6%), and neither unwrapper
   available here gets near a hand-unwrapped character's tens of islands. Not chased in this
   experiment, on the Director's instruction, and it deserves a clean premise of its own.
2. **Dilation is still 33.9% of the atlas and 24.0% of blotch pixels.** It fell 68% in
   absolute terms but remains the most enriched provenance in the defect class. Whether the
   remaining 813,773 dilated texels are reachable by more cameras is bounded by E05: the
   exterior ceiling is ~41% of a hole set, and C1 already commits 52.7% of a hole set that
   culling halved.
3. **Three pass conditions in three experiments have measured the wrong thing** — twice a
   ratio whose denominator moved, once an absolute that penalised halving the denominator on
   purpose. The metric that survived all three framings is **dilated texel count**, which is
   scale-free in the direction that matters.
4. **The `+55` overhead stroke meets twin paint on the forehead with a visible tonal step.**
   It is not a defect in either source, but nothing in the pipeline blends across a
   provenance boundary — stage 1 has a Gaussian levelling term, the brush loop has none.
5. **The unseen faces' shared patch has never been looked at from a camera that can see it.**
   By construction no production camera can, and the classifier's residual is 0.155% of
   visible area. What that patch actually renders as, if a future orbit reaches it, is
   untested.
