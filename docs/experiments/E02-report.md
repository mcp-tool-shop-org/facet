# E02 — report

**Spec:** [E02-texture-stage-on-sound-inputs.md](E02-texture-stage-on-sound-inputs.md)
**Run:** 2026-08-03, executor session. All local, one RTX 5090.
**Gate 0 ruling:** Director, mid-run — stroke order changed, negatives added, stroke 1 discarded.

Evidence, not argument. No conclusions section: the advisor writes those after the
Director has judged the sheets.

---

## What ran

Every path, pin and threshold below is the one actually used.

| | |
|---|---|
| mesh / prep | `E:\AI\training\facet_E01\tex_W3\prepV2` — W3, TRELLIS.2 `1024_cascade` from `facet_E01/inputs/A0_source_clay.png`, seed 42, `ATTN_BACKEND=sdpa SPARSE_ATTN_BACKEND=sdpa`; welded, decimated to 287,200 faces / 38 shells; atlas 4096, `island_margin` 0.001, 3,147,261 valid texels (18.76%) |
| twins | `facet_E01/tex_W3/twinsF/w3clay_{0,4}.png` + their saved `_mask.png` |
| tools | repo copies at `E:\AI\facet\tools` (not the `saltroad_bake_fix` mirror) |
| brush | local ComfyUI, launched `--reserve-vram 8.0 --disable-smart-memory`; Qwen fp8 + `saltroad_style_v2_lowlr_000001500` @ 0.75 + InstantX Inpainting-ControlNet @ 1.0; euler/simple, 20 steps, cfg 2.5, denoise 1.0, **seed 770700 on all eight strokes** |
| blade policy | `texpass_iter.py --thin-extent 0.03` (see below). No pixel rectangle anywhere in this run. |
| stroke order | `45 → 315 → 135 → 225 → 90 → 270 → 0/+55 → 180/+55` (Director ruling at Gate 0) |
| recipe | [E02-prompts.json](E02-prompts.json) — prompts, order and negative in one version-controlled file |

```
# Stage A
python tools/project_twins.py --prep <prepV2> --front twinsF/w3clay_0.png \
       --back twinsF/w3clay_4.png --out facet_E02/styled_stage1.png

# stage-1 packed GLB (emit needs UVs; the atlas it carries is not read by emit)
blender -b -P tools/bake_hero_pack.py -- --prep-glb <prepV2>/prep_uv.glb \
       --atlas facet_E02/styled_stage1.png --out facet_E02/stage1_W3.glb

# Stage D
tools/texpass_loop.ps1 -Tools E:\AI\facet\tools -Prep <prepV2> -StateDir facet_E02\state \
       -Glb facet_E02\stage1_W3.glb -Stage1Atlas facet_E02\styled_stage1.png \
       -OutDir facet_E02\out -PromptsJson docs/experiments/E02-prompts.json \
       -ThinExtent 0.03 -From 1 -To 8 -SeedState -SkipFinalize

python tools/texpass_finalize.py --state facet_E02\state --prep <prepV2> \
       --out facet_E02\out\atlas_final.png
blender -b -P tools/bake_hero_pack.py -- --prep-glb <prepV2>\prep_uv.glb \
       --atlas facet_E02\out\atlas_final.png --out facet_E02\out\W3_texpass.glb

# Stage E — both assets, identical framing, identical light
blender -b -P tools/verify/turn_render.py -- --glb <asset> --out <dir> --tag flat --flat
blender -b -P tools/verify/head_render.py -- --glb <asset> --out <dir> --tag head --flat
blender -b -P tools/verify/head_render.py -- --glb W3_texpass.glb --out <dir> --tag headclay --clay
```

Wall clock: Stage A 8.5 s · eight strokes 480.6 s (8.0 min, 60.1 s mean, ±0.2 s) ·
finalize ~40 s · pack ~25 s · Stage E renders ~3 min. Brush time was 54 s on every
stroke; the remaining ~6 s is emit + commit.

### Stage C — what the spec asked for is not reachable on this asset

The spec asked for the blade exclusion to be derived from geometry (thin local surface,
sharp normal variation, or a named material). Two probes were written and both failed,
for reasons that are properties of the asset rather than of any threshold. Both are kept
in [`tools/superseded/texpass_thin_mask.py`](../../tools/superseded/texpass_thin_mask.py).

1. **A ray along the surface normal resolves the tessellation, not the body.** Median
   reported thickness **0.00204** against a median mesh edge length of **0.00290** — the
   ray hits a neighbouring triangle, not the far wall. The distribution is far too tight
   to be anatomy (p5 0.00179, p50 0.00204, p75 0.00238) and 95.24% of the surface reads
   "thin" at a 0.02 threshold. Starting the ray at eps 3e-3 recovers real body depth
   (p50 0.0444, p90 0.159) but that start depth is thicker than a blade, so the probe
   stops resolving the only thing it exists to find. Corroborating: **only 37% of
   outward rays escape**, where a figure should be near 100% outside arm-over-torso
   occlusion — the surface is re-entrant at the triangle scale.

2. **There is no interior to test.** `prep_uv.glb` carries **293,099 verts for 287,170
   faces**, because the glTF export splits a vertex at every UV seam. Every island
   boundary is a topological crack and ray parity leaks through it.
   `compute_signed_distance` at the figure's own bounding-box centre — the middle of a
   standing warrior's chest — returns **+0.0019**, i.e. *outside*. Occupancy marching
   inherits the same defect.

   *Director ruling, Gate 0:* this generalises. The exported mesh is not merely
   fragmented, it is not a solid, so **any** future work needing containment, thickness
   or inside/outside must run against the welded mesh before export, never against
   `prep_uv.glb`.

**What was used instead** (Director-ratified at Gate 0): a two-sided **camera-ray**
extent probe, `texpass_iter.py --thin-extent`. Fire the camera's own rays from the front
plane and again from the back plane; `extent = 2D − t_front − t_back`. It needs neither a
surface normal nor an interior, so neither fault above can reach it, and it is
character-independent where the rect never could be. Threshold chosen by sweep at yaw 0:

| threshold | withheld | blade coverage |
|---|---|---|
| 0.010 | 4.5% of figure | outline only, interior open |
| 0.015 | 7.4% | partial |
| 0.020 | 12.5% | fuller grooves still open |
| **0.030** | **18.7%** | **solid** |

Most of the 18.7% is a silhouette rim that `commit` already rejects at `--edge-dist 4.0`.
Its known limit, measured at Gate 0: at yaw 90 the blade is edge-on, so the view ray
passes through its broad dimension and reads thick — only **49.9%** of the sword column
was withheld at that camera. See *Open questions*.

The second historical surgery rect — the "invented medallion" zone at `m[675:785,
365:445]` — was dropped entirely rather than reimplemented, on the grounds that per-view
prompting is the fix for invented content.

---

## The eight prompts

Verbatim from [E02-prompts.json](E02-prompts.json). Palette and material words are
byte-identical across all eight; only anatomy and framing change. Orientation was
measured, not assumed — the sword tip sits at std-frame **X −0.150, Y −0.156**, so the
greatsword is held forward on the character's right; camera yaw *N* here equals
`turn_render` view yaw *N*.

**Negative, identical on all eight strokes:**

> braided belt, plaited belt, woven belt, rope belt, shoulder strap, chest strap, baldric, bandolier, watermark, text, logo, blurry, photo, deformed

The first eight terms are Director-named failures observed at Gate 0. A paired change was
made in the positive spine at the same time: `wide dark brown leather belt with wrapped
straps` → `plain wide dark brown leather belt band`, because "wrapped straps" is a
plausible seed for both the braid and the arm strap, and negating a term the positive
prompt is still asking for is a weaker instrument than not asking for it.

**1 · `y+045_e+00`** (front ¾ from his left)
> three-quarter front view of a bald muscular warrior turned toward his left, full red beard and moustache, heavy bare shoulders and chest, bare left arm ending in a closed fist, small round gold medallion at the front of the belt, dark green ribbed knitted sleeveless tunic, ornate polished gold pauldrons, dark wine-red layered cloth skirt, plain wide dark brown leather belt band, gold-trimmed brown leather bracers, gold knee plates, heavy dark charcoal boots, plain flat grey background, painterly visible brushstrokes, worked matte surface

**2 · `y+315_e+00`** (front ¾ from his right, sword side)
> three-quarter front view of a bald muscular warrior turned toward his right, full red beard and moustache, heavy bare shoulders and chest, right arm raised gripping a leather-wrapped hilt above a gold crossguard, small round gold medallion at the front of the belt, dark green ribbed knitted sleeveless tunic, ornate polished gold pauldrons, dark wine-red layered cloth skirt, plain wide dark brown leather belt band, gold-trimmed brown leather bracers, gold knee plates, heavy dark charcoal boots, plain flat grey background, painterly visible brushstrokes, worked matte surface

**3 · `y+135_e+00`** (back ¾ from his left)
> three-quarter rear view of a bald muscular warrior turned away from the viewer over his left shoulder, back of a bare shaved skull, no face, broad muscular back, high knitted collar and a vertical strap running down the spine, dark green ribbed knitted sleeveless tunic, ornate polished gold pauldrons, dark wine-red layered cloth skirt, plain wide dark brown leather belt band, gold-trimmed brown leather bracers, gold knee plates, heavy dark charcoal boots, plain flat grey background, painterly visible brushstrokes, worked matte surface

**4 · `y+225_e+00`** (back ¾ from his right)
> three-quarter rear view of a bald muscular warrior turned away from the viewer over his right shoulder, back of a bare shaved skull, no face, broad muscular back, raised right arm seen from behind, high knitted collar and a vertical strap running down the spine, dark green ribbed knitted sleeveless tunic, ornate polished gold pauldrons, dark wine-red layered cloth skirt, plain wide dark brown leather belt band, gold-trimmed brown leather bracers, gold knee plates, heavy dark charcoal boots, plain flat grey background, painterly visible brushstrokes, worked matte surface

**5 · `y+090_e+00`** (his left flank)
> side profile of a bald muscular warrior seen from his left flank, facing to the left of frame, red beard seen edge-on along the jaw line, bare muscular left arm hanging at his side ending in a closed fist, dark green ribbed knitted sleeveless tunic, ornate polished gold pauldrons, dark wine-red layered cloth skirt, plain wide dark brown leather belt band, gold-trimmed brown leather bracers, gold knee plates, heavy dark charcoal boots, plain flat grey background, painterly visible brushstrokes, worked matte surface

**6 · `y+270_e+00`** (his right flank, sword side)
> side profile of a bald muscular warrior seen from his right flank, facing to the right of frame, red beard seen edge-on along the jaw line, right arm raised gripping a leather-wrapped hilt above a gold crossguard, dark green ribbed knitted sleeveless tunic, ornate polished gold pauldrons, dark wine-red layered cloth skirt, plain wide dark brown leather belt band, gold-trimmed brown leather bracers, gold knee plates, heavy dark charcoal boots, plain flat grey background, painterly visible brushstrokes, worked matte surface

**7 · `y+000_e+55`** (high front)
> high overhead view looking steeply down on a bald muscular warrior from the front, the bare shaved crown of the skull nearest the camera, the tops and outer curves of two ornate polished gold pauldrons filling the shoulders, tops of the bare arms, chest and skirt strongly foreshortened below, upper surface of the belt, boot tops seen from above, dark green ribbed knitted sleeveless tunic, dark wine-red layered cloth skirt, plain wide dark brown leather belt band, gold-trimmed brown leather bracers, gold knee plates, heavy dark charcoal boots, plain flat grey background, painterly visible brushstrokes, worked matte surface

**8 · `y+180_e+55`** (high back)
> high overhead view looking steeply down on a bald muscular warrior from behind, the bare shaved crown of the skull nearest the camera, no face, the tops and outer curves of two ornate polished gold pauldrons filling the shoulders, upper back and high knitted collar below, vertical strap running down the spine, back of the skirt strongly foreshortened, dark green ribbed knitted sleeveless tunic, ornate polished gold pauldrons, dark wine-red layered cloth skirt, plain wide dark brown leather belt band, gold-trimmed brown leather bracers, gold knee plates, heavy dark charcoal boots, plain flat grey background, painterly visible brushstrokes, worked matte surface

---

## Measurements

### Stage A — the starting point

Reproduced the spec exactly; nothing drifted underneath.

```
styled/REACHABLE  534,188/994,349   = 53.7%
reachable/valid   994,349/3,147,261 = 31.6%
styled/valid      534,188/3,147,261 = 17.0%   (legacy number)
atlas variance 0.01103   holes 2,613,073
```

Write-head selftest after the `emit` edit: styled-texel max delta **0.000000**, holes
strictly shrink.

### Per stroke — holes fall monotonically

| # | job | figure px | withheld thin | hole px offered | texels committed | holes after | wall |
|---|---|---|---|---|---|---|---|
| — | *stage 1* | — | — | — | — | 2,613,073 | 8.5 s |
| 1 | `y+045` | 149,780 | 34,652 (23.1%) | 103,768 | 195,519 | 2,417,554 | 60.4 s |
| 2 | `y+315` | 120,439 | 10,540 (8.8%) | 86,974 | 128,130 | 2,289,424 | 60.1 s |
| 3 | `y+135` | 120,439 | 10,540 (8.8%) | 81,355 | 87,566 | 2,201,858 | 59.9 s |
| 4 | `y+225` | 149,780 | 34,652 (23.1%) | 88,167 | 99,469 | 2,102,389 | 60.2 s |
| 5 | `y+090` | 90,553 | 12,248 (13.5%) | 38,524 | 27,520 | 2,074,869 | 60.1 s |
| 6 | `y+270` | 90,553 | 12,248 (13.5%) | 39,155 | 30,052 | 2,044,817 | 59.9 s |
| 7 | `y+000_e+55` | 108,166 | 13,702 (12.7%) | 49,138 | 94,780 | 1,950,037 | 60.0 s |
| 8 | `y+180_e+55` | 117,176 | 23,564 (20.1%) | 36,661 | 48,147 | 1,901,890 | 60.0 s |

The Gate-0 reorder is visible in column 5: under the discarded order `y+090` opened with
**86,084** hole px offered; arriving fifth it had **38,524**, because 672k texels had
already been committed around it.

### Holes closed by the brush vs by dilation

```
brush     711,183 texels   27.2% of the stage-1 hole set
finalize  1,901,890 texels 72.8%,  138 taking mean fallback
```

Roughly three in four hole texels in the final asset carry dilated colour rather than
paint. That ratio is a property of a two-twin projection on this silhouette, not of the
loop: stage 1 leaves 2.6M holes and eight cameras at `facing-min 0.25` reach 711k of them.

### Final atlas

```
variance (valid texels)        0.03013     (stage 1: 0.01103)
non-black  >2/255              99.22%
           >8/255              97.73%
mean / median luminance        0.202 / 0.154
```

### Head texel density — did the head keep its allocation

```
head UV-area share      0.7669
head 3D-surface share   0.3901
ratio                   1.97x     (1.0 = uniform density)
head faces              231,651 / 287,170 = 80.7%
```

Measured per-face inside the crop rect. `meta.json` records **0.8790** for the same
asset because `bake_hero_prep` measures per-*island* — every union-find island touching
the head rect, including faces that spill outside it. Both numbers describe the same
atlas; neither has drifted.

### The finished asset against the rejected A0

Identical framing, identical FLAT light, `Standard` transform, exposure 0.85.

| | E02 W3 | A0 (rejected) |
|---|---|---|
| dark pixels <0.06, front view | 0.32% of figure | 1.00% |
| dark pixels <0.12 | 8.07% | 11.53% |
| speckle, \|lum − local median\| > 0.10 | 2.93% | 2.43% |
| > 0.15 | 1.31% | 1.18% |
| > 0.25 | 0.34% | 0.30% |
| **blade mean saturation** | **0.477** | **0.117** |
| blade, fraction sat > 0.25 | 81.8% | 7.4% |
| blade, fraction sat > 0.40 | 68.1% | 3.0% |
| blade mean luminance | 0.499 (σ 0.171) | 0.456 (σ 0.215) |

Blade isolated as the tallest connected component above the shoulder line in each front
FLAT render; both are 239 px tall, so the regions are comparable.

### Where the blade's colour comes from

The first hypothesis — dilation bleeding neighbouring colour into an unpainted blade —
does not survive measurement. Blade texels sampled by the yaw-0 view:

```
blade texels                            10,679
  styled by the TWINS (stage 1)          1,808  (16.9%)
  styled after all 8 brush strokes       9,385  (87.9%)
  never painted, took dilation fill      1,294  (12.1%)
  atlas saturation: painted 0.451  |  dilation-filled 0.503
```

**The brush painted the blade, and painted it coloured.** Painted and filled texels are
within 0.05 saturation of each other, so the fill is not the differentiator. The
`--thin-extent` policy is per view, and it withholds the blade only from cameras where
the blade reads thin; at the flanks it reads thick and was offered. The twins reached
only 16.9% of the blade to begin with — a thin prop is where a 0.777-IoU silhouette
registration bites hardest, and the 3.8 px edge erosion consumes most of a ~12 px wide
blade in twin pixels.

### Dilation fill — a measured trade-off, not a defect

`texpass_finalize.py`'s docstring says the fill is "valid-island-constrained", but
`fill = ~grown & (cnt > 0)` is not restricted to `valid`, so growth crosses the 4 px
gutter into neighbouring islands. A/B on this atlas, run as a throwaway outside the repo:

```
hole texels filled                       1,901,890
  differ >2/255 if constrained             679,489  (35.7%)
  differ >16/255                           613,654  (32.3%)
  mean abs difference                        11.81/255
mean-fallback texels: unconstrained 138  |  constrained 590,928
```

Constraining the fill would change a third of all filled texels — but it would also drop
**590,928** texels to flat mean grey, because at 35,070 islands averaging 8 faces each,
31% of hole texels sit in islands containing no styled texel at all. The gutter crossing
is currently the only thing giving those islands any colour.

---

## What failed

- **`tools/texpass_thin_mask.py`, normal-ray thickness probe.** `AssertionError: ANDON:
  thin mask covers 95.2% of the surface at --thin 0.02 — that is a broken derivation, not
  a thin character`. Superseded, not retuned. Command:
  `python tools/texpass_thin_mask.py --prep <prepV2> --out thin.npy --thin 0.02`
- **`o3d ... compute_signed_distance`** as a containment fallback: returns **+0.0019** at
  the figure's own bbox centre. No error raised — it returns a wrong answer silently.
- **First `emit` probe run** exited 1 with no message: `--state` pointed at a directory
  that did not contain `atlas.png`; `texpass_iter` reads state before parsing the job.
  Re-run against the real state directory.
- **`git mv tools/texpass_thin_mask.py tools/superseded/`** → `fatal: not under version
  control`. The file was created in the same session and never staged.
- **Two throwaway measurement scripts** raised before yielding numbers and were rewritten:
  `TypeError: float() argument must be ... not 'open3d...Tensor'` (needs `.numpy()`), and a
  blade locator that keyed the figure on background colour — invalid here, because emit
  renders hole texels at the same 0.42 grey as the background, so it counted 0 blade px
  on W3. Both replaced with geometric masks.
- **Discarded:** stroke 1 of the original order (`y+090`, seed 770700), archived at
  `facet_E02/discarded_gate0/` rather than deleted.

Nothing in the eight-stroke run raised. No ANDON fired during the loop, finalize or pack.

---

## Open questions the data raised

1. **A per-view thinness policy cannot protect a prop end to end.** Thinness is a property
   of the surface, not of a camera. The Director's Gate-0 fix — compute the thin mask per
   view, back-project each to texels, union them, and withhold the union everywhere — was
   deferred out of E02 scope on the grounds that the empirical risk looked low. The
   measured cost of that deferral is a blade at saturation 0.477 against A0's 0.117.

2. **The twins reach 16.9% of the blade.** Even a perfect exclusion leaves a prop with
   almost no projected colour, so it would fall entirely to dilation. Whether thin props
   want a third source — projected-only from a dedicated prop view, or a flat material
   assignment — is undecided.

3. **31% of hole texels live in islands with no styled texel.** This is the island-count
   consequence from E01 surfacing in a new place: at 8 faces per island, an island is
   small enough to fall entirely inside an unstyled region. It makes the gutter crossing
   load-bearing rather than incidental, and it means "constrain the fill to valid" is not
   a free correction.

4. **Three in four hole texels in the final asset are dilated, not painted.** The ratio is
   set by how much surface two twins plus eight cameras at `facing-min 0.25` can reach.
   Whether that is the ceiling of a two-twin route, or an argument for more twins or a
   lower facing threshold, is not answered here.

5. **Garment structure drifted and was not corrected.** Gate 0 named three inventions;
   two (braided belt, shoulder strap) were negated and did not recur. The third — the
   green tunic extending to mid-thigh over the wine-red skirt, where the twins have a
   waist-length tunic — was not in the Director's negative list and persists in the
   finished asset.

6. **The E03 bearing.** E01 established that `project_twins` registers against the mesh
   bbox, so a bust mesh misregisters a full-figure twin ~7×. E02 adds a second constraint
   for any graft: the head-band texel allocation measured here (1.97× density, 76.7% of UV
   area) is a property of `bake_hero_prep` run on *this* silhouette. A grafted head changes
   the crop rect's contents and the 3D surface share underneath it, so the allocation would
   need re-measuring rather than carrying over.
