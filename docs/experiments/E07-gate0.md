# E07 — Gate 0

**Spec:** [E07-the-atlas-is-not-a-neighbourhood.md](E07-the-atlas-is-not-a-neighbourhood.md)
**Run:** 2026-08-03, executor session. No GPU, no brush, nothing written to C1.
**Instrument:** [`tools/diagnostics/e07_gate0.py`](../../tools/diagnostics/e07_gate0.py)
**Predictions, recorded before any measurement:** `facet_E07/gate0/PREDICTIONS.md` (blind).

Evidence, not argument.

---

## The spec's three facts, checked first

The spec asked to be doubted. All three hold; one line number has drifted.

| fact | verdict |
|---|---|
| **1** — `commit` has no levelling term, writes the sampled colour straight in | **holds.** `a2[hidx] = col` is at [`texpass_iter.py:246`](../../tools/texpass_iter.py:246), not 249. `gaussian_filter` is imported at line 33 and used exactly once, in the selftest's fake-inpaint at line 276 — never in `commit`. |
| **2** — `finalize`'s flood is not island-constrained despite the docstring | **holds exactly.** [`texpass_finalize.py:43`](../../tools/texpass_finalize.py:43) is `fill = ~grown & (cnt > 0)` with no `& valid`; the docstring at line 6 claims "valid-island-constrained". `valid` appears only in `todo` (34), the mean fallback (46, 48) and the variance assert (50) — never in the write predicate. |
| **3** — stage 1's levelling is atlas-space at σ=16 | **holds.** [`project_twins.py:253-256`](../../tools/project_twins.py:253) and [`bake_hero_fuse.py:233-237`](../../tools/bake_hero_fuse.py:233), the latter with `--seam-sigma` defaulting to 16.0. |

**Found while checking, not in the spec:** [`bake_hero_fuse.py:257`](../../tools/bake_hero_fuse.py:257) carries the
*identical* unconstrained flood — `fill = ~grown & (cnt > 0)`, same missing `& valid`. It is a
different stage family and out of scope here, but the defect is not confined to one file.

---

## Premise 1 — does colour actually cross the gutter?

`texpass_finalize`'s flood replayed exactly as shipped, carrying a source-island label, a
source-*texel* index and a gutter flag instead of a colour. Halt condition: cross-island
import below 10% of dilated texels.

```
dilated texels                       813,773
  colour from ANOTHER island         609,168   74.9%     <- halt was at <10%
  path crossed an invalid gutter     264,192   32.5%
  never reached (mean fallback)          734
  foreign-front depth        median 11 texels, p95 35
  islands importing foreign colour     6,568 / 18,915
```

**PREMISE CONFIRMED.** 74.9% against a 10% floor.

### The gutter is not the mechanism, and the minimal fix is worse than it looks

The spec's §1 attributes the import to the missing `& valid` letting the front walk the
gutter. Only **32.5%** of dilated texels have a path through an invalid texel. Running the
same flood *with* `& valid` — the obvious minimal patch — is the counterfactual:

```
constrained flood (& valid):  cross-island 433,475 (53.3%)   via gutter 0
                              unreached   174,898  (21.5%, was 734)
```

Adding the missing predicate removes **less than a third** of the cross-island import, and
strands 174,898 texels with no source at all — 238× more than now — which then take the mean
fallback: a flat average of the whole atlas. Charts do not need a gutter to leak into each
other, because **unrelated charts are directly 4-adjacent in the atlas**:

```
4-adjacent VALID texel pairs                      4,512,993
  in different islands                              258,806   5.73%
    3D separation median 0.06165 = 21.3 median edges, p90 83.4 edges
    within 1 edge (a UV seam, harmless)                42.8%
    beyond 20 edges (genuinely elsewhere)              50.2%
```

`--pack-margin 0.001` does not put a gutter between all charts. Half of the cross-island
adjacency is between surface-distant charts touching directly.

### The physical version of the question, which is stronger

"Different island" is a label question, and it over-counts: two charts meeting at a UV seam
are *continuous on the surface*, and importing colour across that is correct. What makes
dilation a defect is the source being **somewhere else on the figure**. Median triangle
edge is 0.00290 on a figure ~1.0 tall.

| | median | p95 | >5 edges | >20 edges |
|---|---|---|---|---|
| all dilated texels → source | **0.17733** | 0.39150 | 74.4% | 72.2% |
| cross-island subset | 0.22431 | 0.41260 | 97.9% | 96.2% |
| **L1 bound** — nearest painted texel in 3D | **0.00253** | 0.01710 | — | — |

A dilated texel's colour today comes from a median **0.177 away on a figure 1.0 tall** — 18%
of the figure's height. A surface-aware lookup finds paint at a median 0.00253, *below one
triangle edge*: a **70× shrink**, closer for **92.4%** of the same texels.

The 25.1% that stay within their own island are almost all fine (only ~4% of them exceed 5
edges). Atlas dilation is safe inside a chart and catastrophic across one.

---

## Premise 2 — is there a step to level?

Cross-provenance step ratio on the finished C1 head render, from the `claim.npy`
`texel_provenance.py` already wrote. Halt condition: baseline below 1.25.

```
figure 490,544 px   blotch 3,533 px      <- matches E06 exactly; same camera, same render
pairs 977,883       cross-provenance 48,714 (5.0%)
median |dL| within provenance   0.00523
median |dL| across provenance   0.02876
STEP RATIO                      5.500                <- halt was at <1.25
```

**PREMISE CONFIRMED.** 5.500 against a 1.25 floor.

### Controls, chosen before the number was seen

| control | ratio | reading |
|---|---|---|
| island boundary, **same** provenance | 1.500 | the atlas/surface confound is real but small |
| cross-provenance **inside one island** | 4.500 | the step survives with the island confound removed entirely |

| boundary type | pairs | ratio |
|---|---|---|
| s2 \| s7 | 2,022 | **11.750** |
| TWINS \| s7 — *the forehead the Director named* | 5,450 | **9.500** |
| TWINS \| s2 | 6,949 | 7.250 |
| TWINS \| s1 | 14,732 | 4.750 |
| s2 \| DILATION | 2,170 | 3.500 |
| TWINS \| DILATION | 4,821 | 1.750 |
| s7 \| DILATION | 4,159 | 1.500 |

**The internal contrast is the strongest evidence.** Dilation boundaries are nearly flat
(1.50–1.75) — dilation blends *from* its neighbour by construction, so there is no step where
it meets its own source. Brush-vs-brush and brush-vs-twin boundaries run 4.75–11.75. A
denominator artifact would inflate every boundary type equally. It does not.

E06 called the forehead "a tonal step where two sources meet, not a defect in either." That
step is now a number: **9.5× ordinary texture variation.**

### Two things checked that could have made this number a lie

- **Sampling asymmetry.** A cross-provenance pair maps to two different texels by
  construction; a within-provenance pair need not, and 30.5% of them sample the *same* texel,
  which cannot contain a step. Excluding them leaves the denominator unchanged at 0.00523.
  Null — the ratio does not come from magnification.
- **Lighting.** I measured the render's luminance against the atlas texel it samples, found a
  ratio spreading 1.28–1.56, and concluded it was STUDIO-lit — the trap `CLAUDE.md` records.
  **That diagnosis was wrong.** A fresh `--flat` render is **byte-identical** (sha
  `181cc35de7e039c4`), and the spread is Blender's `exposure = 0.85` under the Standard view
  transform, a nonlinear remap of an sRGB texture. My test could not tell a tone curve from
  shading. E06's baseline was already FLAT and the pass condition stands.

### A precision limit the next arm has to respect

The render is 8-bit, so luminance is quantised to 1/765. **The denominator is 4.0 quanta and
the numerator 22.0.** Every ratio above is a small-integer quotient — which is why they land
on multiples of 0.25. The gate verdict is robust (worst-case slop still leaves 4.2 ≫ 1.25),
but the *value* does not carry three digits, and the denominator has almost no room to fall
before hitting the quantisation floor.

**Consequence for L2's pass condition** (`≥ half the distance from 5.500 to 1.0`, i.e.
≤ 3.25): report the numerator and denominator medians separately, not just their quotient. A
ratio that improves because the denominator rose is not a levelled seam.

---

## Fact 3, measured and changed nowhere

Stage 1's own σ=16 atlas-space levelling kernel, at 7,800 sampled styled texels — what share
of its *covered* Gaussian weight lands on a different island:

```
median 6.8%    mean 15.0%    IQR 3.3-18.5%
texels drawing MOST of their correction off-island:  5.5%
```

**Much milder than the spec feared.** The reason is an inspection paradox: a randomly chosen
*island* is small (median 88 texels), but a randomly chosen *texel* lives in a big one.

```
island size, per island   mean 207   median 88     max 18,362   (11,600 hold any texel)
island size at a STYLED  texel   median 1,231  (~35 x 35, vs sigma = 16)
island size at a DILATED texel   median   296
```

That last pair is the sentence connecting both premises: **paint lives in big charts, holes
live in small ones.** Atlas-space operations are safe exactly where there is already paint
and unsafe exactly where there is not. Consistent with E06's finding that twins are the
cleanest provenance at 0.24× enrichment. Measured here, changed nowhere, as the spec directs.

*(Island counts here are over `prep_uv.glb` — 18,915 partitions, 11,600 holding texels, 15.2
faces/island — and are not comparable to E06's "9,276 native charts over visible faces",
which counted charts on the source mesh before `bake_hero_prep` re-packed it.)*

---

## Predictions vs measured

The advisor's §3 P4 (baseline ratio above 1.5) — **correct**, and understated: 5.500.

The executor's, from `PREDICTIONS.md`:

| # | predicted | measured | |
|---|---|---|---|
| E1 | cross-island 55–75% | **74.9%** | correct, top of range |
| E2 | via-gutter within 3 pts of E1 | **32.5% vs 74.9% — 42 pts apart** | **FALSIFIED** |
| E3 | σ=16 foreign weight median 55–80% | **6.8%** | **FALSIFIED** |
| E4 | step ratio 1.15–1.50 | **5.500** | **FALSIFIED** |

Three of four wrong, and the two failure modes are worth recording because they are general:

- **E2** assumed the pack margin separates every chart, so nothing could cross without the
  gutter. Half the cross-island adjacency is charts touching *directly*. I reasoned from the
  parameter rather than measuring the packing.
- **E3** used the per-island mean size (207) where the question asks about the island a
  sampled *texel* sits in (1,231). Inspection paradox, and it inverted the answer.
- **E4** assumed a median over all boundaries would be diluted by innocuous ones. The
  per-boundary table shows why not: the innocuous boundaries are the *dilation* ones, and
  they are only a fifth of the cross-provenance pairs.

---

## Gate 0 verdict

Both halt conditions tested, **neither fired**. Both premises confirmed with room to spare —
74.9% against 10%, and 5.500 against 1.25.

One correction to the spec that does not change either arm: **the gutter is not the dominant
mechanism, so the minimal `& valid` patch is not the fix.** The spec's §7 L1 method is
already surface-aware and is right for a stronger reason than the spec gave.

Proceeding to L1 and to L2's offline bound. Next halt is **Gate 0.5**.
