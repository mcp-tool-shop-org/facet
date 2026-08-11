# E32 report — the armature mark through the route

**Seat:** executor · **Run:** 2026-08-10 · **Spec:**
[E32-armature-mark-through-the-route.md](E32-armature-mark-through-the-route.md) ·
**Predictions:** [E32-gate0-predictions.md](E32-gate0-predictions.md), registered in two
batches, each before the thing it predicts · **Advisor rules after the Director has seen the
sheet.**

Credits spent: **zero**. Every stage ran locally. Nothing was uploaded, published or pushed.

---

## 0. Environment

| item | value |
|---|---|
| watchdog | restarted at session open; prior heartbeat **1 s** old. Re-armed at VRAM 31,200 MiB / RAM 90% / 87 C, x3 @ 2 s |
| VRAM before GPU work | 7,957 / 32,607 MiB |
| reconstruction peak | GEN 3.4 GB · to_glb 2.7 GB · **overall 3.4 GB** — far below the ceiling; it was never approached |
| python | `E:\AI-Models\trellis2-env\Scripts\python.exe` |
| blender | 5.2, `-b -P` headless, driven from PowerShell |
| subject | `E:\AI\training\facet_E32\armature_mark_clay.png`, sha256 `ade49b60…f9a1` — **matches the dispatch, and is byte-identical to `C:\Users\mikey\Downloads\ComfyUI_00122_.png`** (same length, same hash) |

---

## 1. Premises — the four the spec marked, checked

| # | premise | outcome |
|---|---|---|
| 1 | `mesh_character.py` takes `--ptype 1024_cascade` | **holds** |
| 2 | `project_texture.py` is in `3d-prerender/`, not `saltroad_bake_fix/tools/` | **holds — the skill's path is wrong.** Enumerated both directories; `saltroad_bake_fix/tools/` has 33 files and does not contain it |
| 3 | `turn_render.py` is in `saltroad_bake_fix/tools/` | **holds.** ⚠ `facet/tools/verify/turn_render.py` also exists and **differs**; the dispatch's copy was used |
| 4 | `memory/character-turnaround-pipeline.md` — the skill's required reading | **MISSING, confirmed independently.** Searched all of `C:\Users\mikey\.claude\projects` for `*turnaround*`: zero hits. The only `character`-named memory file is `comedic-moods-character-voice-model.md`, unrelated. **It was not read, and nothing here stands on it.** The skill body was the only surviving statement of the procedure |
| 5 | `pipe.run` runs `rembg`; a grey-on-grey plate needs no pre-keying | **holds in outcome, wrong in mechanism — see §2** |
| 6 | the subject is a thin-tube lattice | **holds, measured** |

## 2. Premise 5 corrected: the segmenter is BiRefNet, not `rembg`

Read at `trellis2_image_to_3d.py:127-160` rather than assumed:

```
mode=='RGBA' and not all(alpha==255) -> has_alpha   # OURS: alpha all 255 -> False
scale = min(1, 1024/max(size))       -> LANCZOS 2048 -> 1024
rembg_model(input)                   -> trellis2/pipelines/rembg/BiRefNet.py
bbox = argwhere(alpha > 0.8*255)     -> SQUARE crop about its centre
output = rgb * alpha                 -> PREMULTIPLIED; ground becomes black
```

Three corrections the phrase "runs rembg" hides, each load-bearing:

* **The model is BiRefNet at 1024×1024** (`BiRefNet.py:16`), not the PyPI `rembg`/u2net-at-320.
  The route hands it a 1024 image, so it runs **1:1** with no resampling at its input.
* **The output is premultiplied.** A partially-transparent pixel is darkened toward black,
  not merely masked — thin members lose luminance as well as coverage.
* **The square crop can clip.** `size = max(bbox_w, bbox_h)` with integer halving gave a
  crop of `[264,206,760,702]` against an alpha bbox of `[266,206,758,703]`: the crop's
  bottom edge is **1 px above the figure's**. One pixel of the feet is outside the
  conditioning image. Reported, not repaired.

Our plate is RGBA with alpha **constant 255** (`frac_below_255 = 0.0`), so `has_alpha` is
False and **the segmenter does run**. That is settled by code, not predicted.

## 3. The plate's own geometry

Measured **before any prediction was registered**, as the dispatch directs.

The first measurement was contaminated and is reported because it is the finding. A
two-sided quadratic key on this plate returns **835,526 px at tol 0.06, bbox the full 2048 px
frame width, median width 350 px**. The plate is not a "light grey subject on a grey
gradient": the upper two thirds are a soft light field and **the bottom third is a hard dark
band** (fitted-background luma span **95.82**, top row 136.68 → bottom row 58.19). No
quadratic fits a step edge, so the key returned the band. **No figure number is taken from
it.** `--polarity lighter` does not rescue it either — a step edge drags the ring fit down
until the flat upper field keys as subject too. Both failures are asserted in T64.

The load-bearing mask is therefore **BiRefNet's own** — the route's answer to "where is the
figure", at route scale (1024×1024):

| quantity | value |
|---|---|
| mask area | 26,511 px, **2.53%** of the route frame |
| figure bbox | **493 × 499 px** |
| fill of bbox | **10.78%** — a lattice, not a figure |
| width min / p01 / p05 / p50 / p95 / max | **4 / 6 / 8 / 10 / 26 / 28 px** |
| width band share, 0–4 px | **0.0%** — nothing is thinner than 4 px |
| width band share, 8–16 px | **67.8%** |
| openings at min_area 1 / 16 / 64 / 256 / 1024 | **22 / 22 / 21 / 16 / 2** |

The opening curve is flat from min_area 1 to 16 (**22 at both**): the mask carries **no
speckle**, so the count is a property of the figure and not of a threshold. In plate space
(2048) every width doubles: min 8, p50 20, max 56 px.

An independent cross-check: `project_texture.py` reports `BiRefNet foreground 2.4%` from its
own code path, against the 2.53% above (the two threshold alpha differently, >204 vs >127;
at >204 this instrument reads 2.36%).

---

## 4. Gates

| gate | verdict | evidence |
|---|---|---|
| **L — licence ANDON** | **PASS** | `mesh_character.py … --licence-strict 1` → `licence_guard: nvdiffrast/nvdiffrec blocked (non-commercial licence)` at load, and at the end `LICENCE OK: clean bake path: no nvdiffrast/nvdiffrec loaded this run.` Exit 0. The flag was never disabled |
| **M — mesh sanity** | **reported, not judged** | GLB loads. Mesh extent (Blender xyz) `1.0012 × 0.1772 × 0.9699`; w/h = **1.0324** against the concept figure's 493/499 = **0.9880** — the mesh is **4.5% wider relative to its height** than the plate. Front-view silhouette bbox 878×850 (w/h 1.0329) agrees. **Depth is 17.7% of width**; the profile silhouette is 156 px against the front's 878 (17.8%), which agrees independently |
| **0 — sheet before metrics** | **PASS** | `E:\AI\training\facet_E32\E32_gate0_sheet.png`, 6368×2192, concept beside all 8 clay views. Built **before** any number in §6 was quoted |
| **project_texture `--min-iou`** | **FIRED — HALTED** | see §5 |

## 5. The projection stage HALTED — `--min-iou` fired

```
[img ] armature_mark_clay.png 2048x2048  BiRefNet foreground 2.4%
[cal ] TRELLIS square crop: centre=(1024.0,909.0) side=994.0 px
[rast] 8,174,633 covered texels (48.7% of the atlas)
[cal ] silhouette IoU (body): 0.5831 initial -> 0.5878 refined
[cal ] head box y[422:629]  head IoU before: 0.6275 -> after 0.6411
CALIBRATION FAILED: silhouette IoU 0.5878 < --min-iou 0.8.
```

**Exit 1. No texture was written. The threshold was not lowered and the flag was not
disabled.** Step 3 of the route does not complete on this subject, and steps that depend on
it produce nothing.

The overlay the tool wrote (`proj_debug/calib_silhouette.png`, green = agree, RED = concept
only, BLUE = mesh only) shows the failure is **not** a registration collapse: every member is
green-cored and in the right place, with red and blue as thin opposed fringes along the
tubes. What the number is reacting to is a systematic few-pixel offset on a subject whose
perimeter-to-area ratio is enormous — the mask is 10.8% of its own bbox. On a ~20 px tube, a
3–4 px offset removes a large fraction of the intersection and adds it to the union, on
every member at once.

This is the repo's own law — *normalise a boundary quantity by perimeter, not by area* — in a
new place: **silhouette IoU is an area-normalised agreement score, and it therefore reads a
high-perimeter subject as mis-registered at an offset that would be invisible on a solid
figure.** Reported as a fired gate; whether the metric or the threshold should change on this
subject class is a ruling, not an executor's call.

---

## 6. Predictions against measurements

The mesh side is measured from an **exact raycast silhouette** (`silhouette_masks.py`), never
from a keyed clay render. Both sides are normalised by the figure's **own bbox**, because a
render and a plate are different sizes: widths as a percentage of bbox height, openings above
**0.026% of bbox area** (the plate's own min_area 64 against its 246,007 px bbox).

| # | prediction | band | measured | verdict |
|---|---|---|---|---|
| P4a | segmenter's bbox does not span the frame | < 90% of frame | **48.1%** (493/1024) | **HIT** |
| P4b | mask area, fraction of route frame | 2–8% | **2.53%** (2.36% at alpha>204) | **HIT** |
| P4c | openings surviving segmentation, min_area 64 | ≥ 8 | **21** | **HIT** |
| P4d | thinnest surviving member, route space | 2–5 px | **min 4.0**, p01 **6.0** | **ambiguous — my defect, see below** |
| P1a | crossings come back bridged into webbing | qualitative | **not bridged** — the X-brace, pelvic loops, head cage and foot rings are all open on the sheet | **MISS** |
| P1b | openings preserved, matched relative threshold, against the plate's **21** | **0–6** | **17** (81.0% preserved) | **MISS, far above** |
| P2a | shell count | **5–60** | **212** | **MISS, above** |
| P2b | `mesh_topology` nested-wall leg | **DECLINES** | **it COMPUTED** | **MISS** |
| P3 | front-view p50 width as % of bbox height, against the plate's 2.004% | **2.6–6.0%** (1.3–3.0×) | **2.3529%** (**1.174×**) | **MISS, below band — direction right, magnitude wrong** |

**Four clean misses, one ambiguous, three hits.** The misses are the result.

### P4d was under-specified, and I am not picking the reading that makes it a hit

I wrote "the thinnest surviving member's width" without saying whether that is the minimum or
a low percentile. The minimum is **4.0 px** (inside the 2–5 band); p01 is **6.0** and p05 is
**8.0** (both above it). The same prediction is a hit or a miss depending on a word I did not
write. It is scored **ambiguous**, not hit. This is the repo's recurring unit/operand family
appearing in my own prediction rather than in a dispatch.

### Why P1b and P3 missed — the mechanism I reasoned from does not bound the result

Both predictions came from one piece of arithmetic, stated in advance:
`ss_res` for `1024_cascade` is **32** (`trellis2_image_to_3d.py:541`), the conditioning image
is a square crop tight to the figure, so a p50 **10 px** tube is **0.65 voxels** at 32³ and
the median kept opening is **~1.2 voxels**. A grid that coarse cannot separate them, so I
predicted heavy fusion (0–6 openings) and heavy thickening (1.3–3.0×).

Measured: **17 of 21 openings preserved (81.0%)** and thickening of **1.174×**.

I registered the falsifier for this in advance — *"the arithmetic treats a generative sampler
as a rasterizer… if P1b comes back at or near 22, the lesson is that voxel arithmetic does not
bound a learned occupancy prior, and that is a more useful result than a hit."* That is what
happened. **Occupancy-grid resolution is not an upper bound on the topology a learned sparse-
structure sampler plus a cascaded shape latent will produce.** The cascade refines shape
within occupied voxels, and on this subject that recovered cells the 32³ grid could not have
carried.

The width distribution shifted exactly one band and no further: plate 67.8% in 8–16 px, mesh
74.6% in 16–32 px; raw p50 10 → 20 px across a 1.70× render-scale change (bbox height 499 →
850), which is 1.174× after normalisation. Fill of bbox moved 10.78% → 12.24%. **The
direction I predicted was right and the magnitude was over-predicted by 2.2×–17×.**

### P2b computed, and what it does and does not say

The nested-wall leg **did not decline** — the second manifold-adjacency piece is **25,450
faces = 2.67%** of the mesh, above the 1% floor that makes all five recorded character meshes
decline. It reports:

| | |
|---|---|
| outer / inner faces | 499,256 / 25,450 |
| outer volume | 0.00235083 |
| **inner volume** | **−0.000113198** (negative — the payload's own nested-wall signature) |
| **material_frac_of_outer** | **0.9518** |
| wall gap median | 0.00208604 (**0.208%** of height) |
| boundary edges | **0** — the surface is closed |
| non-manifold edges | 3,582 (**0.251%**) |

So there is an inner surface, enclosing a cavity of **4.8%** of the outer volume. That is not
E14 Ruling 3's "hollow double-walled shell, walls ~two voxels around an empty cavity" — it is
a nearly-solid body with a small internal void. **This is the first subject on this route
where that leg computes at all**, so far as this report's reading of the record goes.

I recorded in advance that a DECLINE would have been uninformative because the leg cannot
distinguish "inner wall shredded below 1%" from "no inner wall exists". A **COMPUTE** does
not carry that ambiguity, but it is one subject in a fourth class and says nothing about the
character class, where the leg still declines.

### P2a: 212 shells

Above my band (5–60) and above the character family's recorded 40–191. Largest shell holds
**57.0%** of faces; 211 satellites. `pieces_manifold_adjacency` is **1,151** — the two
definitions disagree by 5.4×, which is the pinched-surface case `e14_topology`'s own operand
warning exists for. Unwelded components: **32,147**.

⚠ **This is a single-run mesh comparison and its noise floor was not measured here.** E29
Ruling 5 measured ±2,618 faces (0.27%), ±1 shell, ±18 non-manifold edges across three runs of
one input at one seed. My band-miss on P2a is 3.5×, far outside that floor, but the floor
E29 measured was on a different subject class and I did not re-measure it on this one.

---

## 7. The frame the default would have cropped

`turn_render.py`'s default 757×1024 **cut the arms off every view** — the rendered figure
touched both frame edges (bbox x 0…756 in a 757 px frame). This subject is nearly square
(extent 1.0012 × 0.9699) and the portrait default cannot hold it.

`e12_frame.py` derived the frame from this mesh — worst yaw / height = **1.0324** at view 0,
`1024 × 1.0324 = 1057.1` → rounded up to a multiple of 16 → **1072×1024**. Re-rendered there,
the figure sits at x 76…995 with margin on both sides. Every render and silhouette in this
report is at 1072×1024. **The E04 bowsprit trap fired on this subject and the committed
instrument for it already existed.**

---

## 8. Instruments — what was built, and two defects the plate found in them

Two tools and one shared function were added. **Tests ride the commit** (`tests/test_t64_plate_geometry.py`, 24 legs).

* `tools/diagnostics/e32_plate_geometry.py` — a plate's own geometry: bbox, widths via
  `mask_geometry.local_thickness`, enclosed-opening count as a curve against min-area, alpha
  facts. Enumerated first: every existing plate-side instrument in this repo requires a
  mesh-derived mask (`e12_twin_readout --mask`, `silhouette_masks` raycasts, `e14_twin_registration`
  compares to a silhouette), so none can answer a question asked before a mesh exists.
* `tools/diagnostics/e32_route_preprocess.py` — the route's `preprocess_image` transcribed
  from source, emitting the route-scale plate, the segmenter's mask, the premultiplied
  conditioning image and the numbers. It carries one ANDON: if the plate's alpha is
  non-trivial the segmenter never runs, so it raises rather than measuring the other branch
  under this branch's name.
* `mask_geometry.fit_background` — **additive only.** `project_twins.py` calls
  `ap.parse_args` at module level (line 220) and **cannot be imported**, which is why five
  hand-copies of the route's background model already exist in this repo
  (`project_twins:349`, `e12_twin_readout:106`, `e14_twin_registration:48`,
  `gained_bg_check:94`, `e08_registration:86`). Nothing existing was modified; T64 extracts
  `project_twins`' own body with `ast` and asserts the two are **bit-identical**, with a
  companion leg proving that comparison can fail. **The five copies are reported, not fixed.**

**Two defects in my own instrument, both found by the plate within an hour of writing it:**

1. **`bbox_blowout` was a conjunction.** It required *both* dimensions ≥98% of frame. E08's
   own case — "751 px wide in a 752 px frame" — blows out in **one**. It therefore stayed
   silent on the contaminated key at exactly its worst reading: **2048/2048 wide** by
   1673/2048 tall, reported clean. Now fires on either axis and names which. T64 asserts the
   width-only case.
2. **`abs()` in the residual was not free.** A two-sided key cannot express "the subject is
   lighter than the ground", so a dark region is subject. `--polarity` was added; the default
   stays `both` so every number already produced reproduces.

The honest boundary is asserted rather than described: **`--polarity lighter` does not rescue
a hard-edged ground** (11,428 px against a true 800 in the fixture), which is why the
load-bearing path uses `--mask` and the route's own segmenter instead of any key here.

---

## 9. A gate that was already red at HEAD, untouched

`tests/test_t41_instrument_census.py::test_t41_axis_d_is_idempotent_across_runs` **fails on
the clean tree at HEAD `6e85cf9`**, before any change of mine (working tree was clean; I
checked before editing).

Cause, measured: the census's committed axis-D count for `turn_render.py` is **18**; a fresh
read gives **19**. The 19th citing document is
`docs/experiments/E32-armature-mark-through-the-route.md` — **the E32 spec commit itself**.
This is the E28 self-reference family exactly: an arc's own paper contaminating the census
the arc is measured by.

**I have not touched it.** Regenerating the census is a count-surface edit, and my own report
will move the same counts again when it lands.

### Count surfaces — reported first, then reconciled under Ruling 7

At report time these were **named and measured, not edited**, per CLAUDE.md: *"an executor
that reports the collision and touches nothing has done the right thing."* [E32
Ruling 7](E32-ruling.md) then decided the reconciliation and it was carried out in this same
commit, **driven off the tree and never off the list below** — `tests/test_t34*.py`'s own
`PINS` table read at apply time (16 pins across 6 files, plus the separate 8-README digits
leg), `pytest --collect-only` at the combined tree, and
`python tools/instrument_census.py --committed` for the census. The table below is a summary
and was never the authority; two earlier seats hand-listed these surfaces and each missed a
different file.

**The baseline is measured, not assumed.** A detached worktree at HEAD `6e85cf9` was created
and the three count-surface files run there: **1 failed, 101 passed** — the single failure
being the spec commit's own census contamination above. Everything else is green at HEAD.

Working tree, full suite: **31 failed, 884 passed** (697 s). The accounting is complete and
every one of the 30 new failures is a pin firing as designed:

| pin | at HEAD | with this commit | why |
|---|---|---|---|
| `test_t34` — test count, on `README.md` + 7 translations + `SHIP_GATE.md` + site-config + handbook + advisor-kickoff | green | **25 failures** | T64 adds **24** legs |
| `test_t41` — `tools/diagnostics/` population | green, pinned **99** | **101**; 3 failures (population, axis-G judgments, committed JSON) | two tools added |
| `test_t41` — axis-D idempotency | **already red** | still red | the spec commit, §9 above — **not mine** |
| `test_t62` — the runnable population "pinned seven" | green | 1 failure | both new tools are invocable |
| `test_t33` — SystemExit-ANDON population | green, pinned **28 across 12 files** | **30 across 14**; 1 failure | each new tool carries one `raise SystemExit("ANDON: …")` |
| `docs/instrument-census.json` axis-D | stale for `turn_render.py` (18 vs 19) | also stale for this report's citations | |

The T33 movement is worth its own line: that pin found my ANDONs **because they are correctly
formed**. Both are `raise SystemExit("ANDON: …")`, not `assert` — E21 Ruling 2's law, so
neither is deletable by `python -O` or `PYTHONOPTIMIZE=1`.

**Nothing in this list is a regression.** `test_t25_mask_geometry` (33 legs) passes unchanged
across the `mask_geometry` addition, which is the claim that addition had to earn.

### What the reconciliation measured

The collector at the combined tree: **917 full / 877 hermetic / gap 40** (from 891 / 851 / 40).
The census regenerated to **110 rows** from 108 — the two new tools — with **three** axis-D
counts moving, each because a document in this commit cites the instrument:
`turn_render.py` 18 → **21** (the spec, this report, the ruling), `e12_frame.py` 3 → **5**,
`e14_topology.py` 11 → **13**. That regeneration is what clears the gate that was already red
at HEAD.

⚑ **It took two regenerations, and the second one is the lesson.** The census was rebuilt
once, and the axis-D leg went red again on the clean full-suite run — because *this section*,
written after that rebuild, was the first place the report named `e14_topology.py`. Ruling 8
predicted exactly this (*"the report and this ruling will move the same counts again when
they land"*), and it is the E28 self-reference family for the third recorded time. **The
census must be regenerated after every document in the commit is final, not before** — a
derived artifact whose input includes the document describing it has a fixed point, and you
only reach it by writing last and regenerating after. Correcting the integer above is safe
and does not re-trigger it: axis D counts *documents that name a file*, so changing a digit
inside a document that already names it moves nothing.

Both new tools were judged for **axis G** under the census's own stated rule — docstring line 1
plus filename, never the body — and both landed **`none`**: the spec's eight job-shaped tools
have no entry for *measure an input image's geometry* or for *reproduce the reconstructor's
preprocessing*, and a 2D mask's local thickness is not `thin_extent_curve`'s per-view
front-to-back extent of a mesh. Both joined T62's `RUNNABLE` set, which is pinned by name
precisely so that joining it is a deliberate edit: **seven → nine of 110.**

13 surface files were touched, digits only on the seven translated READMEs. **No translation
pass was run** — this is not a release, and the count is the same digits in every language.
`SHIP_GATE.md`'s lineage kept its history rather than overwriting it: `… → 859 → 891 → 917.`

Re-run after reconciliation, the six affected files: **386 passed, 0 failed** — T34, T41, T62,
T33, T25 and T64 together. The 31 failures above are all clear, including the one that was red
before this session began.

---

## 10. Out of scope, and not run

* **Steps 5–7 (facing atlas · per-view restylize · multi-view re-projection): NOT RUN.** The
  spec cut them before the session began, for the two independent reasons in its ⛔ block. The
  `character-turnaround` skill's *"BEFORE RUNNING STEP 6, SAY SO"* instruction was satisfied
  by the spec, in writing, before anything ran. **Nothing in this session ran a per-view job.**
* **Step 3 (texture projection): HALTED at its own gate** (§5). Everything downstream of a
  projected GLB is therefore absent, not skipped by choice.
* `E:\AI\armature` was not touched. `E:\AI\training` was read-only except
  `E:\AI\training\facet_E32\`, which this session created.
* No LoRA, no Comfy Cloud, no upload, **zero credits**.
* The full test suite **RAN** at report time: 31 failed, 884 passed in 697 s. All 31 are
  accounted for in §9 — 1 pre-existing at HEAD, 30 count-surface pins firing as designed, no
  regression — and all 31 are cleared by the Ruling 7 reconciliation carried out in this
  commit.

## 11. Artifacts

```
E:\AI\training\facet_E32\
  armature_mark_clay.png              the plate (input, read-only)
  armature.glb                        36.6 MB - the reconstruction
  recon.log                           run parameters: ptype=1024_cascade remesh=True
                                      decim=1000000, seed 42 (run() default, no flag)
  project.log                         the fired --min-iou gate
  proj_debug\calib_silhouette.png     the overlay behind §5
  preprocess\armature_{route,mask,cond}.png, armature_pre.json
  turn_clay\clay_0..7.png             1072x1024, --clay
  masks\armature_0..7.png             exact raycast silhouettes + silhouettes.json
  plate_geometry.json                 the CONTAMINATED key sweep, kept as evidence
  plate_geometry_routemask.json       the load-bearing plate measurement
  mesh_view0_geometry.json            the mesh front-view measurement
  frame.json                          the derived 1072x1024 frame
  E32_gate0_sheet.png                 6368x2192 - the Gate 0 sheet
```

Compensators: every path above is a new file under `facet_E32\`, so `rm -r
E:\AI\training\facet_E32` undoes the session apart from the plate, which was opened read-only
throughout. Repo changes: two new tools, one additive function, one new test file, two new
docs. Nothing pushed, nothing published.

---

## 12. What the Director is being asked to look at

`E:\AI\training\facet_E32\E32_gate0_sheet.png` at full size — the concept beside eight clay
views. The two questions a number cannot answer: **is this the armature mark**, and does the
17.7%-of-width depth (visible in views 2 and 6, which are 156 px wide against the front's
878) read as a usable object or as a flat relief.

**No judgement word appears in this report about whether the mesh is good.** The measurements
are above; the ruling is the advisor's and the eye is the Director's.
