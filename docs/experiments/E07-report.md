# E07 — report: L1 built, L2's re-anchored bound halted

**Spec:** [E07-the-atlas-is-not-a-neighbourhood.md](E07-the-atlas-is-not-a-neighbourhood.md)
(Amendments 1–2) · **Gate 0:** [E07-gate0.md](E07-gate0.md) ·
**Gate 0.5:** [E07-gate0_5.md](E07-gate0_5.md)
**Run:** 2026-08-03, executor session, all local. **No GPU spent.**

Evidence, not argument.

`facet_E06/C1/` was read-only throughout. Its shipped atlas still hashes `dcc4a80c5e5d6b44`
and its loop atlas `6e9b452d96979982`, both re-verified after every stage below.

---

## What ran

```
# Amendment 1: gate restated on source distance; edge computed from the mesh
python tools/texpass_finalize.py --state facet_E06/C1/state --prep facet_E06/C1/prep \
       --surface-aware --out facet_E07/L1/atlas_final.png
blender -b -P tools/bake_hero_pack.py -- --prep-glb .../prep_uv.glb \
       --atlas facet_E07/L1/atlas_final.png --out facet_E07/L1/W3_L1.glb
blender -b -P tools/verify/head_render.py -- --glb ... --tag headflat --views=0 --flat
blender -b -P tools/verify/turn_render.py -- --glb ... --tag flat --flat

# Amendment 2: membrane re-anchored on the accepted set
python tools/diagnostics/e07_l2_bound.py --anchor accepted ... --out facet_E07/L2bound_acc
```

---

## L1 — the gate passes on the restated unit

`edge` is now measured from `prep_uv.glb` rather than hardcoded — all three edges of every
triangle, median **0.00290**, which is the value the repo already records, so nothing that
depends on it shifts.

```
[finalize] median triangle edge 0.00290  (measured on this mesh)
[finalize] source distance  median 0.00253 = 0.87 edges   p95 0.01709   max 0.06394
[finalize] beyond 5 edges 7.80%   beyond 20 edges 0.004%
[finalize] normal disagrees >60deg 56.58%   back-facing 48.67%  (REPORTED, not gated)
[finalize] done, 0 texels took mean fallback
```

| gate | limit | measured |
|---|---|---|
| median source distance | ≤ 3 edges | **0.87** |
| share beyond 20 edges | ≤ 5% | **0.004%** |

Mean fallback **734 → 0**: every hole texel now has a surface source, where the shipped
flood left 734 taking a flat average of the whole atlas.

### The arm table

| | **L0** (C1 as shipped) | **L1** |
|---|---|---|
| islands · faces/island · coverage | 18,916 · 15.2 · 14.32% | *identical — L1 does not touch the loop* |
| holes 1,721,598 → | 813,773 | identical |
| brush closed / dilation closed | 907,825 (52.7%) / 813,773 | identical |
| colourless islands | 4,528/11,600 (39.0%), 412,775 hole texels | identical |
| styled after loop | 1,589,037 = 66.1% of valid | identical |
| **source distance, median** | **0.17733 (61 edges)** | **0.00253 (0.87 edges)** |
| **mean fallback** | 734 | **0** |
| final atlas variance | 0.03607 | **0.03994** |
| speckle >0.10 / >0.15 / >0.25 (flat_0) | 2.64 / 1.07 / 0.23 | **2.43 / 0.91 / 0.16** |

A0 speckle reference: **2.43 / 1.18 / 0.30**. L1 sits at A0 on the loosest threshold and
below it on both tighter ones.

### At the Director's head zoom

| | L0 | L1 |
|---|---|---|
| blotch px of 490,544 | 3,533 (0.72%) | **3,372 (0.69%)** |
| DILATION share of blotch | 24.0% | 22.5% |
| DILATION blotch px | 848 | **759** |
| DILATION enrichment | 4.77× | **4.46×** |
| TWINS enrichment | 0.24× | 0.24× |
| step ratio | 5.500 | 5.500 *(unchanged by construction — L1 is post-loop)* |
| flattening guard | — | **+0.97%** (ANDON at −5%) |
| head speckle >0.10 / >0.15 / >0.25 | 0.72 / 0.28 / 0.05 | 0.69 / 0.26 / 0.05 |

**§5's L1 pass condition is NOT met.** It asked for total blotch below **3,100** and
dilation-provenance blotch below **400**; measured **3,372** and **759**. P1 (dilation below
400) and P2 (total 2,600–2,900) are both falsified at the head zoom.

### Where L1 actually acts

The head is where dilation is scarcest — 5.0% of its clean pixels — so the head zoom cannot
show much of an operation that rewrites 813,773 dilated texels. Across all eight FLAT
turnaround views, figure pixels changing by more than 2/255:

| view | 0 | 1 | 2 | 3 | **4** | **5** | **6** | 7 |
|---|---|---|---|---|---|---|---|---|
| changed | 6.4% | 8.3% | 10.6% | 6.4% | **12.9%** | **15.4%** | **13.0%** | 7.2% |
| mean delta /255 | 2.40 | 3.07 | 3.97 | 3.17 | **8.71** | **10.82** | **9.53** | 3.37 |

**10.0% of figure pixels over the eight views**, concentrated on views 4–6 — the back half,
where the twins never reached and dilation carried the surface. Front views move a third as
much. That is the operation acting where the measurement says it should.

**Director's Gate 1 artifacts.** `facet_E07/GATE1_head_L0_vs_L1.png` (2072×1064, both heads
at full render resolution, no downscale), `facet_E07/L1/flat_0..7.png` FLAT turnaround,
`facet_E07/L1/W3_L1.glb`.

---

## L2 — re-anchored, and the flattening ANDON fired

Amendment 2's re-anchor is implemented as `--anchor accepted`: the membrane's domain is the
**accepted set** rasterised into view space through a per-pixel texel map, Dirichlet only
where the outside neighbour is already styled, natural elsewhere. The filter chain now runs
on the *original* brush output, so the accepted set — and the claim map — stay
**byte-identical to C1's**, isolating the correction as the only variable. The `--no-level`
replay still reproduces C1's loop atlas byte-for-byte.

| stroke | accepted | domain px | anchored | \|O\| lum median | p95 | at cap |
|---|---|---|---|---|---|---|
| 1 y+045_e+00 | 224,910 | 45,963 | 14.8% | 0.0638 | 0.1422 | 7.08% |
| 2 y+315_e+00 | 147,411 | 35,335 | 10.4% | 0.0335 | 0.1371 | 5.62% |
| 3 y+135_e+00 | 127,964 | 30,488 | 15.0% | 0.0493 | 0.1405 | 5.72% |
| 4 y+225_e+00 | 127,699 | 36,131 | 17.8% | 0.0826 | 0.1498 | 8.79% |
| 5 y+090_e+00 | 35,457 | 7,675 | 20.4% | 0.0459 | 0.1482 | 9.06% |
| 6 y+270_e+00 | 44,671 | 9,254 | 20.3% | 0.0667 | 0.1500 | 12.43% |
| 7 y+000_e+55 | 138,766 | 16,581 | 20.2% | 0.0612 | 0.1484 | 11.84% |
| 8 y+180_e+55 | 60,947 | 10,026 | 25.4% | 0.0706 | 0.1500 | 11.57% |

Against the contour anchor: **corrections ~5× larger** (median 0.007–0.017 → 0.034–0.083) and
**cap hits ~7× more often** (0.5–1.7% → 5.6–12.4%). Amendment 2's diagnosis is supported —
the contour anchor's correction was decaying before it reached the seam.

### The outcome, and the halt

| | L0 | L2 contour | **L2 accepted** |
|---|---|---|---|
| step ratio | 5.500 | 5.000 | **2.600** |
| numerator (cross-provenance) | 0.02876 (22q) | 0.02614 (20q) | **0.01699 (13q)** |
| **denominator (within-provenance)** | 0.00523 (4q) | 0.00523 (4q) | **0.00654 (5q)** |
| island boundary, same provenance | 0.00784 | 0.00784 | **0.00784** |
| blotch px | 3,533 | 3,248 | **1,643 (−53.5%)** |
| final atlas variance | 0.03607 | 0.03498 | **0.02998 (−16.9%)** |
| **flattening guard** | — | −0.62% | **−10.66%** |

**ANDON: the flattening guard fell 10.66%, against §5's −5% halt.** Reported and halted; no
parameter changed, no re-run. The guard's own sanity case passes — scoring L0 against itself
returns +0.00%, and L1 returns +0.97%.

**The denominator moved, which is what I flagged at Gate 0.5.** Within-provenance neighbour
contrast rose 0.00523 → 0.00654 (**+25%**), so part of the ratio's improvement is the
denominator inflating rather than the seam levelling. Decomposed:

- numerator alone: 22q → **13q**, a 41% fall — that part is real
- **holding the denominator at its baseline 4q, the ratio would be 3.250** rather than 2.600

The island-boundary numerator is **unchanged at 0.00784** across all three arms, so whatever
moved, it was not island-boundary contrast.

Three independent signals point the same way and are offered as mechanism, not verdict: the
guard fell 10.66%, atlas variance fell 16.9%, and 5.6–12.4% of the domain is clipped at the
0.15 cap — a clipped field has a hard edge where it transitions from clipped to unclipped,
which would raise 1-pixel contrast while lowering a 5×5 median residual. That is consistent
with the denominator rising and the guard falling at the same time, but it is not tested.

### The instruction conflict, unresolved by me

Amendment 2: *"If the re-anchored bound moves substantially, the rerun is authorised on the
spot."* It moved substantially — 5.500 → 2.600, blotch −53.5%, past the withdrawn 3.25 bar.

§5: *"ANDON: halt if it falls more than 5%."* It fell 10.66%.

Both conditions are met. Choosing between a standing ANDON and a conditional authorisation is
a ruling, so **the GPU run is not authorised by this session** and nothing was tuned toward
the guard.

---

## Predictions

| # | prediction | outcome |
|---|---|---|
| P1 | dilation blotch 848 → below 400 (L1) | **FALSIFIED** — 759 |
| P2 | total blotch 3,533 → 2,600–2,900 (L1) | **FALSIFIED** — 3,372 |
| P3 | >20% of lookups disagree >60° | **CORRECT, understated** — 56.58% |
| P4 | baseline ratio above 1.5 | **CORRECT, understated** — 5.500 |
| P5 | levelling takes the ratio below 1.2 | **FALSIFIED at both bounds** — 5.000 contour, 2.600 accepted |
| P6 | L2 barely moves the blotch count | **FALSIFIED at the accepted anchor** — −53.5% (supported at the contour anchor, −8.1%) |
| P7 | L3 ≈ L1 + L2 | **untested** |

P6 flipping between the two anchors is the clearest single piece of evidence that the anchor
was the load-bearing choice, not the levelling operation itself.

---

## Open

1. **L1 is built and awaits the Director's eye.** Its pre-registered head-zoom pass condition
   is not met; its gate, its speckle, its source distance and its turnaround delta all move.
   Gate 1 is his.
2. **L2's conflict above.** If the guard is to stand, the cap is the first suspect and the
   membrane's magnitude the second — both untested, and tuning either is a new arm, not a
   re-run of this one.
3. **`bake_hero_fuse.py:257`** still carries the same unconstrained flood Gate 0 measured.
   Unchanged, out of scope, still shipping.
