# E14 handoff 9 — finalize, pack, and the Gate 1 staging

**Executor session, 2026-08-08.** Ruling 30 (`35ca345`), executed. **Finalize ran at exit 0
with both ANDONs passing; the pack produced `longsword_hero.glb`; the Gate 1 sheets are staged.
No generation, no credits, no re-derivation. `run/s8/` was never opened for writing and its
three SHAs are byte-identical at session end.**

Two instrument errors were caught inside this session and neither reached a number below.
Both are reported in §7 rather than deleted, because both are the same family the record
already names.

---

## 1. What ran — the invocation, quoted in full

```
# step 1, after copying run/s8/ -> run/final/ (three SHAs verified identical both sides)
python tools/texpass_finalize.py --state E:\AI\training\facet_next\E14_strokes\run\final ^
       --prep E:\AI\training\facet_next\E14_prep ^
       --out  ...\run\final\atlas_final.png --surface-aware ^
       --json ...\run\final\finalize.json
#   ANDON defaults, unchanged and unpassed: --max-edge-median 3.0
#                                            --beyond-edges 20.0  --max-frac-beyond 0.05
# exit 0, wall 20.2 s

# step 3
blender -b -P tools\bake_hero_pack.py -- --prep-glb ...\E14_prep\prep_uv.glb ^
        --atlas ...\run\final\atlas_final.png --out ...\run\final\longsword_hero.glb
# exit 0, wall 4.5 s

# step 4 renders, x8 yaws x2 channels, --profile BOUND ON EVERY EMIT (Ruling 29c's trap)
python tools\texpass_iter.py emit --state <rstate> --prep ...\E14_prep ^
       --glb ...\prep_uv.glb --yaw <Y> --el 0 --profile profiles\prop.json
```

The `texpass_finalize` values above are the ones the advisor's Gate-1 fold puts into the
profile's registry: **`surface-aware` ON, `max-edge-median 3.0`, `beyond-edges 20.0`,
`max-frac-beyond 0.05`** — all defaults, none overridden. The beast's finalize ran the same
mode and the same three ANDON values.

**Watchdog, verified twice and reported either way**: at session start, alive, 1955/32607 MiB,
29,245 below the 31,200 ceiling; again immediately before the Blender leg, alive, 2003/32607,
29,197 below. No GPU work in this dispatch beyond Blender's headless import/export.

## 2. The dispatch's first caveat — checked, and it is STALE

The dispatch carried *"E07 found `texpass_finalize.py`'s triangle-edge length HARDCODED from
one mesh."* **The repair already landed and the tool measures per mesh at run time**
([`texpass_finalize.py:98-106`](../../tools/texpass_finalize.py)), loading `prep_uv.glb` from
`--prep`. [E04-profile-extraction.md](E04-profile-extraction.md) had already flagged the seed
list as stale on this exact item; source and record agree.

Measured independently anyway — my own walk, not the tool's print:

| | value |
|---|---|
| tool's printed median edge | **0.00098** |
| my per-face-edge median (same definition, my code) | **0.000980** |
| my UNIQUE-edge median (a different definition) | **0.000979** |
| one voxel of a 1024 grid over a 1.0 span | **0.000977** |
| `meta["maxabs"]` vs the mesh's `max\|v\|` | **0.501006126 both — identical** |

The last row is the one that makes the unit real: positions and edges are normalised by the
same scalar, so a distance quoted in edges is in one space. And the median triangle edge **is
the voxel pitch** to three significant figures, which is the marching-cubes mechanism showing
through. The dragon's edge is 0.002307 — **this mesh's triangles are 2.35x smaller.**

## 3. Step 1 — FINALIZE

```
[finalize] filling 1,929,166 hole texels (surface-aware)
[finalize]   median triangle edge 0.00098  (measured on this mesh)
[finalize]   source distance  median 0.00200 = 2.04 edges   p95 0.00626   max 0.03218
[finalize]   beyond 5 edges  6.80%   beyond 20 edges 0.054%
[finalize]   normal disagrees >60deg 90.43%   back-facing 86.44%   (REPORTED, not gated)
[finalize] done, 0 texels took mean fallback
[finalize] wrote atlas_final.png  var 0.03410
```

**Texels closed: 1,929,166** — and the two state files agreed exactly about which they were:
`valid & holes` = 1,929,166, `valid & styled` = 1,732,737, with **zero** texels in either
disagreement direction and zero of either mask outside `valid`.

### 3.1 The distribution, beside the dragon's — and what the comparison actually says

| | this subject | the dragon | |
|---|---|---|---|
| median source distance, **absolute** | **0.001996** | 0.002115 | **5.6% closer** |
| median source distance, **in edges** | **2.037** | 0.917 | 2.2x further |
| p95 | 0.006255 | 0.007975 | closer |
| max | 0.032175 | 0.066724 | closer |
| beyond 5 edges | 6.80% | 2.50% | |
| beyond 20 edges (ANDON at 5%) | **0.054%** | 0.021% | both far inside |
| normal disagrees >60 deg | 90.43% | 82.25% | reported, never gated |
| back-facing | 86.44% | 78.91% | reported, never gated |

**The two subjects source colour from the same absolute distance and differ only in the unit.**
Every absolute percentile on this asset is *closer* than the dragon's; the ratio is larger
because the denominator — this mesh's triangle edge — is 2.35x smaller. Reading 2.04 against
0.92 as "twice as far" would be the wrong-unit error one level down from the one the dispatch
warned about.

The mechanism is the hollow shell, and it is measured: 92.8% of unreachable texels are inner
wall (`stage1b_reach_N6_ceiling.json`'s cross-tab), and an inner-wall texel's nearest paint is
the outer wall across a two-voxel cavity. That is also why the two normal-disagreement
diagnostics are high on both subjects and why E07 Gate 0.5 withdrew them as gates.

### 3.2 ⚠ The mean-fallback ANDON the dispatch named CANNOT FIRE

The dispatch asked for the mean-fallback count with *"a nonzero is a FINDING, located per
structure."* **In `--surface-aware` mode the count is 0 by construction.**
`texpass_finalize.py:135` sets `grown = valid.copy()` before the dilation loop; `left` at
line 154 is `(valid & ~grown).sum()`, and `grown` only ever grows. `left == 0` on every
surface-aware run regardless of the atlas, the mesh, or how badly the lookup went. The
galleon's 112 came from the **atlas-flood** path, where `grown = have.copy()` and the number
means something.

So the reported 0 is not a quality signal, and neither was the dragon's. *A check that cannot
fail is not a check.* The quantity that carries this mode's failure is the source-distance
distribution above, which is gated (`--max-edge-median`, `--max-frac-beyond`) and which
passed at 2.04 against 3.0 and 0.054% against 5%.

### 3.3 The cross-island flood defect — measured, with the lane's mitigating fact tested

**98.16% of the 1,929,166 lookups take colour from a different atlas component.** That number
needs its operands or it is alarming for the wrong reason:

| | |
|---|---|
| atlas components, 4-connectivity | **31,887** |
| atlas components, 8-connectivity | 31,883 |
| cross-island lookups | 1,893,700 = **98.16%** |
| their distance, median | **0.00200 = 2.04 edges** |
| same-island lookups, median | 0.00135 = 1.38 edges |
| E07's measurement of the **atlas-flood** path on E06's C1 | 74.9% cross-island, **median 0.177** |

The defect E07 named is colour walking through the gutter into a geometrically unrelated
island **0.177 away on a figure 1.0 tall**. Here the cross-island lookups sit at **0.00200** —
**89x closer**. On an atlas shattered into 31,887 components averaging 115 texels each, the
opposing wall of a two-voxel-thick blade is virtually always a different component, so the
cross-island *flag* is answering a question about UV packing, not about surface distance. The
lane's mitigating fact holds where it is measurable: only **0.054%** of lookups travel beyond
20 edges, and 97.3% of those are cross-island.

**⚠ A recorded number does not mean what it has been used to mean.** The route quotes
**46,496 islands** for this subject (Ruling 9c, and the dispatch repeats it). Its source is
[E14-gate0-report.md](E14-gate0-report.md) line 121, **`shells (unwelded)`** — a property of
the *mesh* (a vertex split at every UV seam), not a count of atlas-space components. The
atlas-space count is **31,887**. Neither number is wrong; they measure different objects, and
"islands" has been carrying both. Cross-island is an atlas-space question, so 31,887 is the
denominator used above. Ruling 29g's instrument-pinning lesson, one level over.

### 3.4 Per structure — the geometry-derived bands, the blade first

Bands from [E14-longsword-structures.json](E14-longsword-structures.json) (mesh-z, derived
from the width profile — **not** the coarser bands in `stage1b_holes_by_structure.json`, which
partition differently; the two are not comparable row for row).

| structure | valid | reference | brush | dilation | **dilation %** | src median | cross-isl |
|---|---|---|---|---|---|---|---|
| **L1 blade** | 2,542,416 | 1,178,416 | 39,192 | 1,324,808 | **52.11%** | 2.02 e | 98.3% |
| L2 crossing | 590,807 | 224,291 | 28,145 | 338,371 | **57.27%** | 2.06 e | 97.0% |
| L5 stone | 177,314 | 86,949 | 2,047 | 88,318 | **49.81%** | 2.06 e | 98.4% |
| L4 grip lower | 137,214 | 66,291 | 81 | 70,842 | 51.63% | 2.08 e | 99.6% |
| L4 grip upper | 102,546 | 53,975 | 45 | 48,526 | 47.32% | 2.09 e | 100.0% |
| L3 mid ring | 57,150 | 23,312 | 3,453 | 30,385 | 53.17% | 2.18 e | 97.0% |
| L3 collar | 54,456 | 23,613 | 2,927 | 27,916 | 51.26% | 2.25 e | 98.3% |

Every valid texel falls in exactly one band (0 outside). **The blade's dilation share is
52.11%, inside W3's blade band of 47–61%** — the named comparable. Its source distance is the
lowest of the seven structures (2.02 edges), which is the rim-and-ribbon design's claim
holding where it was made.

### 3.5 The stone is untouched — asserted, not assumed

All 1,732,737 styled texels compared byte-for-byte before and after finalize: **0 moved.**
Finalize writes only into `valid & holes` (line 69), so the garnet stone, the 1,436 collar
repair texels and all eight strokes are byte-identical. Located, too: **the garnet
re-projection's 66,468 texels and the repair's 1,436 are 100% inside `L5_stone`** — zero in any
other structure, measured.

## 4. Step 2 — the provenance accounting

Every class count was asserted against the record before it was used; the five classes plus
dilation partition all 3,661,903 valid texels exactly.

### 4.1 The mix, both denominator families

| | texels | **% of valid** | in N8 (1,879,807) | **% of N8** | in N6 (1,867,754) | **% of N6** |
|---|---|---|---|---|---|---|
| **REFERENCE** | 1,656,847 | **45.246** | 1,656,847 | **88.139** | 1,656,847 | **88.708** |
| — stage-1b projection | 1,588,943 | 43.391 | 1,588,943 | 84.527 | 1,588,943 | 85.072 |
| — **THE STONE**, its own sub-class | 67,904 | 1.854 | 67,904 | 3.612 | 67,904 | 3.636 |
| **BRUSH** (8 strokes) | 75,890 | **2.072** | 52,485 | **2.792** | 50,089 | **2.682** |
| **DILATION** (finalize) | 1,929,166 | **52.682** | 170,475 | **9.069** | 160,818 | **8.610** |

Both reachable columns are **intersected**, not bare ratios. Two facts fall out of that:

- **Reference is entirely inside both reachable sets** (1,656,847 of 1,656,847), so its bare
  and intersected numbers coincide. `project_twins` and the ceiling floor at the same 0.45.
- **Brush is not**: 23,405 of 75,890 stroke texels (30.8%) sit outside N8, because the brush
  commits at `facing-min 0.25`. That is the profile's own three-way funnel, measured. The
  dragon's report quoted reference as a bare ratio and brush as an intersection; this one
  states which is which.

**Both ceilings re-derived from `project_twins`' definition and asserted: N8 = 1,879,807 and
N6 = 1,867,754, EXACT against the recorded 51.3342% and 51.005%** — an independent code path
agreeing with a recorded number.

**The comparables, stated so no number is read against the wrong asset:**

| | reference | brush | dilation |
|---|---|---|---|
| W3 (character) | 68.8 | 4.2 | 27.0 |
| the galleon | 36.89 | 6.87 | 56.24 |
| the dragon | 44.15 | 3.07 | 52.78 |
| **the longsword** | **45.25** | **2.07** | **52.68** |

This subject lands within 1.1 points of the dragon on every class. Both are hollow
double-walled shells with ~51% of the atlas reachable, and reachability is what sets the
dilation share.

**The stone's provenance, kept separate as Ruling 30 requires:** 67,904 texels = 66,468
garnet re-projection (projected reference paint, hue/chroma corrected at the recorded
operands, Rulings 25–26) + 1,436 collar repair (restored from `state0`, Ruling 28d). It is
reference-provenance, never brush, and it is 1.854% of valid / 3.61% of N8.

### 4.2 The on-surface family, Ruling 9's form — with a class breakdown that is new

As recorded: **11.0875% >1 px** (`offsurface.json`) / **11.1037%** on the anatomy tool's own
300k sample · **46,496 UV islands** (the mesh property, §3.3) · **erode-2 residue 0.0085%**.
Finalize does not touch the bake, and it re-measures identically.

Measured this session, per provenance class (300k sampled each, same instrument):

| population | >1 px | >5 px |
|---|---|---|
| ALL VALID (the bake) | 11.1037% | 6.8370% |
| STYLED at HALT 2 (reference + brush) | **7.1163%** | 4.2307% |
| DILATION (what finalize filled) | **14.7597%** | 9.1760% |

The margin population concentrates in the dilation class, which is what the bake-margin
reading predicts: the styled set is what cameras could reach — outer wall, well-formed
surface — and the residue is inner wall and island margins. **This is a denominator change,
not a regression:** HALT 2's recorded "off-surface 0 texels, 0.0000%" is a different quantity
(committed paint landing off-surface), and after finalize every valid texel is painted, so
the painted set's margin rate becomes the bake's own. The two do not belong in one column.

### 4.3 What anyone actually SEES — the rendered provenance

The atlas mix says what the asset is made of. This says what a camera returns, inside the
exact raycast silhouette:

| yaw | figure px | reference | stone | brush | dilation | boundary blend |
|---|---|---|---|---|---|---|
| 0 | 49,775 | 92.37% | 2.01% | 0.98% | 1.53% | 3.11% |
| 45 | 40,101 | 89.11% | 2.99% | 1.81% | 2.05% | 4.03% |
| 90 | 24,153 | 81.68% | 6.38% | 3.61% | 2.22% | 6.11% |
| 135 | 40,331 | 88.37% | 2.93% | 2.04% | 2.37% | 4.30% |
| 180 | 49,775 | 92.27% | 1.96% | 0.84% | 1.87% | 3.06% |
| 225 | 40,101 | 88.87% | 2.97% | 1.54% | 2.34% | 4.28% |
| 270 | 24,153 | 81.13% | 6.45% | 3.21% | 2.37% | 6.84% |
| 315 | 40,331 | 88.33% | 3.03% | 1.91% | 2.20% | 4.52% |
| **pooled** | 308,720 | **88.71%** | **3.20%** | **1.78%** | **2.08%** | 4.23% |

**Dilation is 52.68% of the atlas and 2.08% of the visible surface.** The "boundary blend"
column is the provenance render's own resampling — class colours interpolate at class
boundaries — and it is largest on the two edge-on views, where a 54 px figure is almost
entirely boundary. The mirror pairs agree to two decimals throughout (0/180, 45/225,
90/270, 135/315), which is the bilateral-symmetry fact behaving.

## 5. Step 3 — PACK

`longsword_hero.glb`, **49.6 MB** (50,827 KB), sha256 `ab62bb4bd753f2cef4db74d0`. Atlas
variance 0.03410, well over the 0.001 ANDON. The dragon's hero GLB was 43.9 MB; the smoke
render is the eight-yaw turn set in §6, which proves the GLB's atlas loads and reads.

## 6. Step 4 — the Gate 1 staging

All under `run/final/gate1/`, full size, FLAT light throughout, **no verdicts on any sheet**.
The house form ran as the handoff-8 walk-set builder's form rather than `gate1_sheet.py`:
that tool's five columns assume a per-view reference exists, and views 2 and 6 have no
accepted twin. Both carry an **EXCLUDED placard naming the ruling**, in-image, per Ruling 20d.

| sheet | what it carries |
|---|---|
| `GATE1_y{000..315}.png` (8) | **clay \| finished asset \| provenance \| accepted twin \| error**, native 240x1024 |
| `GATE1_turnset.png` | the eight finished views at native frame |
| `GATE1_turnset_beside_clay.png` | clay \| finished, per yaw, all eight |
| `GATE1_HILT_4x.png` | pommel through crossing, 4x, eight yaws, clay \| asset |
| `GATE1_STONE_6x.png` | L5 at 6x, eight yaws, clay \| asset \| provenance |
| `GATE1_CROSSING_4x.png` | L2 at 4x, eight yaws, clay \| asset \| provenance |
| `GATE1_RIBBON_4x.png` | both edge-on faces, 4x, clay \| BEFORE \| AFTER \| provenance |
| `GATE1_FIFTH_SIGNATURE_5x.png` | yaws 315 / 90 / 270 at 5x, clay \| BEFORE \| AFTER |
| `longsword_hero.glb` | staged for the Director's own zoom |

The provenance legend is drawn as **colour chips**, not colour words, because the route's
dilation violet (150,90,150) and this lane's garnet magenta (220,60,220) are close enough at
display scale that I misread one for the other while checking a sheet. Neither colour was
changed — the violet is the convention across three subjects and the magenta is the key the
Director was shown at HALT 2. Measured to settle it: **garnet-magenta appears only in rows
88–141 of the rendered frame on every view**, and there is none at the crossing.

## 7. ⚠ Two instrument errors, caught in-session, neither reaching a number above

Both were found by the same cheap move — *an inherited or measured figure moved a direction
the mechanism forbids* (Ruling 29g), where the mechanism is that finalize only ever adds
colour and cannot make an asset darker in a place it did not touch.

**(a) A detector whose threshold rode on the intervention.** My first speckle instrument
scored "darker than the local 5x5 median, where that median exceeds 0.15". Before finalize the
holes are a flat mid-grey and the local median sits low, so the detector stays quiet; after,
the holes carry paint, the median rises, and the same isolated dark pixels start firing. It
reported speckle **rising 220 -> 1,596**. The moving-denominator family, inside an instrument
written an hour earlier.

**(b) An inherited comparison column from another session's render path.** Replacing it with
an absolute threshold still said darkness rose (9,182 -> 21,276), so I anchored the BEFORE
column instead of trusting it: re-emitted `run/s8` through the same tool, same profile, same
cameras, and pixel-compared against handoff 8's `run/render_final/`. **Every one of 245,760
pixels differs** — background 154 against 107, figure mean ~25 levels brighter, RGBA against
RGB. The HALT-2 walk set was rendered through a different path. It is not wrong, and the
Director's acceptance of it stands; it is simply not pixel-comparable to this session's
renders, so it cannot be a BEFORE column. (Per the repo's own law, the PNG hash mismatch
alone proved nothing — the pixel comparison did.)

I re-rendered `run/s8` through the identical path at all eight yaws (`run/final/render_before/`)
and every before/after panel and number in this report uses that. **Anyone comparing the
HALT-2 sheets against these Gate-1 sheets should expect a global brightness difference that
is the render path, not the asset.**

### 7.1 With the instruments fixed — what finalize did to the residual speckle

Ruling 29a named "scattered dark hole-speckle across guard and blade awaiting finalize's
dilation". Measured on the corrected pair:

| | before | after |
|---|---|---|
| pixels under luma 0.08 inside the silhouette, pooled | 21,378 (6.92%) | **21,276 (6.89%)** |
| INVALID-texel samples inside the silhouette (state-independent) | 2,489 = 0.81% of figure px | same |
| their mean luma | **0.0741** | **0.1431** |
| atlas texels outside `valid`, pure black | **100.00%** | **28.40%** |

**The speckle's source is the gutter, and finalize's 16-step tail closed 71.6% of it.** The
s8 atlas carried pure black in every one of its 13,115,313 invalid texels; after finalize
71.6% carry neighbouring colour, and the gutter samples the camera returns are twice as
bright. What remains is beyond 16 steps of the valid boundary.

The dark population that is *not* gutter is the subject: of the 21,276 dark pixels in the
finished asset, **53.0% are stage-1b reference paint and 31.3% are the garnet stone**, against
5.6% gutter, 2.4% brush and **0.7% dilation**. This subject's accepted steel is L\* 21–24
(Ruling 14) and its stone is a deep garnet.

The fill itself is arithmetically clean: the hole texels carried a **uniform 0.4196 luma**
placeholder (mean = median, zero pure black) and now carry mean 0.2630 / median 0.2070,
against the styled sources they drew from at mean 0.2573 / median 0.2062. **The filled texels
inherited the paint's own distribution.** Every view's rendered figure darkens by 0.093–0.104
mean luma, which is that placeholder grey leaving.

## 8. The blind predictions, graded

Committed before finalize ran ([E14-handoff9-predictions.md](E14-handoff9-predictions.md),
`1643249`), blind status disclosed per item.

| # | prediction | outcome |
|---|---|---|
| P0 | the hardcoded-edge caveat is stale; the tool measures per mesh | **CORRECT** — and re-measured independently, three definitions agreeing |
| P1 | 1,929,166 closed; holes and styled agree | **CORRECT** — zero disagreement either direction (not blind: arithmetic) |
| P2 | edge 0.0008–0.0013, ~half the dragon's | **CORRECT** — 0.000980, 42.5% of the dragon's; and it is the voxel pitch |
| P3 | absolute 0.0015–0.0030; **1.2–2.6 edges, above the dragon's 0.92** | **CORRECT** — 0.001996 and **2.037 edges**, with the absolute distance landing 5.6% closer than the dragon's exactly as the shell mechanism said |
| P3 | beyond 5 edges 2–8%; beyond 20 below 0.5%; back-facing 65–88% | **CORRECT** — 6.80%, 0.054%, 86.44% |
| P3 | normal disagrees >60 deg 70–90% | **FALSIFIED, marginally** — 90.43% |
| P4 | mean fallback 0, and the ANDON cannot fire | **CORRECT** — structural, not earned (not blind: a code read) |
| P5 | mix of valid 45.245 / 2.073 / 52.682 | **CORRECT** — 45.246 / 2.072 / 52.682 (not blind: arithmetic) |
| P5 | reference 86–89% of reachable | **CORRECT** — 88.14% of N8, 88.71% of N6 |
| P5 | brush 2.4–3.7% of reachable | **CORRECT** — 2.79% / 2.68% |
| P5 | dilation 8–11% of reachable | **CORRECT** — 9.07% / 8.61% |
| P6 | **blade dilation 51–56%** | **CORRECT** — 52.11%, inside W3's 47–61% band |
| P6 | crossing 57–64% · stone 46–53% · collar 48–56% | **CORRECT** — 57.27% · 49.81% · 51.26% and 53.17% |
| P6 | grip 48–55% | **SPLIT** — lower 51.63% correct, **upper 47.32% falsified** just below |
| P7 | the bake's off-surface family re-measures identically | **CORRECT** — 11.1037% / 46,496 / 0.0085% |
| P8 | GLB 40–46 MB | **FALSIFIED** — **49.6 MB**; a fully-filled atlas compresses worse than a hole-heavy one, which I did not price |
| P8 | atlas variance 0.02–0.06 | **CORRECT** — 0.03410 |

Fourteen correct, three falsified (two marginal), on a dispatch whose calibration named unit
errors and silent defaults as the risks. The prediction worth keeping is P3's: it was made
from a mechanism — same voxel grid, same shell, smaller triangles — and both halves landed,
the absolute distance *and* the direction of the ratio.

## 9. What has NOT been done

- **No generation, no cloud call, no credits.** No such call exists in this dispatch.
- `run/s8/` was never opened for writing; its three SHAs are byte-identical at session end
  (`34dafd4b57aa5b04df935cfb` / `e05e450800dc500f3b2a55d9` / `322ebdf6b55055da7614e506`).
- **No errand-batch repair run** — the window is deferred past Gate 1 (Ruling 30b). The two
  errand items this session touched evidence for (the `emit` profile guard, the A3 port) were
  left alone; the emit trap was handled by binding `--profile` on all 24 emits and asserting
  the 240x1024 frame afterwards.
- No fixture, profile, palette, ruling or tool edited. No gate armed. No value re-derived.
- No memory-store write.
- Nothing on any sheet judges the asset.

## 10. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | State copied forward with three SHAs verified both sides and re-verified at session end; the finalize invocation quoted in full with every ANDON value; blind predictions committed in their own commit before the run; the edge constant verified three ways before any distance was quoted; every emit carries `--profile` and every frame asserted 240x1024 |
| ANDON_AUTHORITY | **3** | Both finalize ANDONs left at their defaults and passed on their own (2.04 vs 3.0; 0.054% vs 5%); the stone's untouchability asserted by byte comparison, not claimed; the provenance partition asserted class-by-class and as a partition before use; the mean-fallback ANDON reported as unable to fire rather than quoted as a pass |
| NAMED_COMPENSATORS | **3** | No spend, no generation, nothing irreversible; `s8` preserved as the rollback point and proven unchanged; every output written to new paths under `run/final/`; every prior compensator standing |
| DECOMPOSE_BY_SECRETS | **3** | The mix reported per structure over geometry-derived bands with the stone as its own provenance sub-class; both denominator families with intersections rather than bare ratios, and the funnel that separates them measured; all four subjects' mixes stated so no number is read against the wrong asset |
| UNCERTAINTY_GATED_HUMANS | **3** | The sheets carry no verdicts; the fifth-signature class goes to the eye on the finished asset after dilation exactly as 29a/30a routed it, with the clay's crease geometry beside it; excluded artifacts labelled in-image; the halt ends at the advisor then the Director beside the clay |
| EXTERNAL_VERIFIER | **3** | The finalize lookup was REPLAYED independently and reproduces `atlas_final.png` byte-for-byte on all 1,929,166 filled texels; both reachability ceilings re-derived from `project_twins`' definition and matched the record exactly; the BEFORE column anchored by re-emission and pixel comparison rather than trusted; the edge length measured by two definitions of my own beside the tool's |

## 11. ⚠ The index verify — legs 1–3 PASS, leg 4 is 19/20, and THIS SESSION'S DOCUMENTS CAUSED IT

The E15 ritual ran (`build` then `verify`) after the report was written. Legs 1–3 hold:
determinism **byte-identical** at 8,093,696 bytes over two builds; all 17 count checks `ok`
(E14 now 30 numbered rulings / 123 lettered / 8 handoffs); every pointer resolves.

**Leg 4 — the seeded question set — regressed from 20/20 to 19/20**, and the miss is mine:

```
the galleon's accepted mix   MISS
   expected: E04-ruling.md Ruling 27 | README.md The route | handbook The galleon
   got 1. E14-handoff9-predictions.md : P5 - the final mix          [prose]
   got 2. E14-handoff9-report.md      : 4.1 The mix, both denominator families
   got 3. E08-task3-step3-preflight.md
```

**The cause is the dispatch's own instruction.** Ruling 30's step 2 requires the comparables
restated in the report — *"the galleon 36.89 / 6.87 / 56.24"* — precisely so nobody reaches
for them elsewhere. Doing that put two fresh documents above the canonical source on an FTS
query seeded on exactly those numbers. **A route that restates its comparables in every
subject's report will out-rank their canonical home once per subject**, so this is structural
and it will fire again on subject five, not a one-off.

**I have not touched it.** The seeded questions live in `facet_index.py`, which this dispatch
forbids editing, and re-choosing a question after seeing which document displaced it is
retuning a condition against the result it judges — the one move the record calls always
wrong. Editing my own report to lose a ranking contest would be the same move wearing
different clothes, and would delete content the dispatch ordered. The disposition is the
advisor's: pin the seeded question to its canonical locator, weight canonicality over
recency, or accept comparables-bearing reports as legitimate answers.

**A second, separate finding in the same tool**: `verify` **crashes** under the default
Windows console encoding — `UnicodeEncodeError: 'charmap' codec can't encode '↑'` at
[`facet_index.py:1770`](../../tools/facet_index.py), a `↑` in the completeness-branch print.
It only fires when a sequence runs ABOVE its dispatched bound, which E12 and E14 now both do
(E12 `[29, 30]`, E04 `[29]`). `PYTHONIOENCODING=utf-8` is the workaround used above. This is
the repo's own ASCII-prints rule broken inside its own verifier, on a branch that stayed cold
until the arcs outgrew their bounds — errand-batch class, and the errand window is deferred
past Gate 1 (Ruling 30b), so it is reported and left alone.

## 12. What goes up for the ruling, none of it mine to decide

1. **The finished asset at Gate 1** — the sword beside the Director's clay, all eight yaws.
2. **The flagged fifth-signature class on the finished asset after dilation**, as Rulings
   29a/30a routed it, at 5x on the three strokes whose watch fired.
3. **The "46,496 islands" label carrying two different objects** (§3.3) — a mesh shell count
   used as an atlas component count; the atlas-space number is 31,887.
4. **The mean-fallback ANDON that cannot fire in surface-aware mode** (§3.2) — a route-wide
   fact about a check three subjects have now quoted as a pass.
5. **The HALT-2 walk set and the Gate-1 sheets are not pixel-comparable** (§7b) — different
   render paths, a global brightness difference that is not the asset.
6. **The seeded-question regression this session caused** (§11) — structural, will recur per
   subject, and its disposition is an index-design call.
7. **`facet_index.py verify` crashes on its own non-ASCII print** (§11) on a branch that only
   fires once an arc runs above its dispatched bound — which two arcs now do.

---

## HALT — the finished longsword is staged

Finalize ran at the accepted route's recorded invocation with both ANDONs passing on their
own defaults; the stone and every styled texel are byte-identical; the pack produced
`longsword_hero.glb` at 49.6 MB; the Gate 1 sheets are full size under FLAT light with no
verdicts on them.

**The advisor's sheet-walk first, then the Director beside the clay.** Nothing past this halt
runs — the E11 dense export, the lane ingest and the activated state each wait on his sentence,
and the errand window stays deferred until Gate 1 is ruled.
