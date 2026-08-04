# E06 — advisor ruling at Gate 1

**Date:** 2026-08-04 · **Director's verdict:** *"This is a lot better, but there are blotches
on his face (that may be warpaint or dirt texture). Sword is better. Hand also has a blotch
that may be intentional."*

---

## The result

Culling exterior-invisible surface from the atlas works. The blade — the loudest defect at
E02 — is fixed by the Director's eye. The remaining question is not whether the blotches are
bad but **what they are**, which is measurable rather than aesthetic.

| metric | U0 (E02) | U1 (native UV) | **C1 (cull)** |
|---|---|---|---|
| brush closed | 711,183 (27.2%) | 923,466 (26.6%) | 907,825 (**52.7%**) |
| **dilated** | 1,901,890 | 2,551,893 | **813,773** |
| colourless islands | 54.6% | 52.7% | **39.0%** |
| their share of hole texels | 75.0% | 60.8% | **50.7%** |
| styled after loop | 39.6% of valid | 38.7% | **66.1%** |
| exterior-invisible texels | — | 49.8% | **15.0%** |
| speckle .10 / .15 / .25 | 2.93 / 1.31 / 0.34 | 2.61 / 1.03 / 0.19 | 2.64 / 1.07 / 0.23 |

A0 reference: 2.43 / 1.18 / 0.30.

## The pass condition was mis-specified — third time, and in the opposite direction

The executor reported a miss rather than rounding, which was correct. The condition was
wrong, and it is the advisor's.

An absolute was chosen to escape a moving denominator — and then C1 **halved the denominator
on purpose**, which was the entire point of the experiment. Painting 907,825 of 1,721,598
holes is not worse than painting 923,466 of 3,475,359; it is twice as good.

**The unit that cannot lie from either side is dilated texel count: 2,551,893 → 813,773, a
68% fall.** Three mis-specified conditions across three experiments is a pattern, now
recorded in `CLAUDE.md`: ask what the intervention is designed to change, then measure
something orthogonal to it.

## One prediction falsified, and it costs most of the predicted gain

**Charts fragment under culling; they do not merge.** 47% of faces removed, only 34% of
charts, so faces-per-chart *fell* (20.5 → 16.4), bbox fill fell 42.1% → 36.6%, and packed
coverage fell 24.81% → 14.32%. The mechanism: invisible surface is interleaved *within*
charts, so excluding it punches holes in them — a chart keeps its outer extent while losing
interior area.

Working the arithmetic through, texels landing on visible surface:

- U1: 3,475,359 valid × ~50% visible ≈ **1.74M**
- C1: 2,402,810 valid × 85% visible ≈ **2.04M**

**~17% more, against an advisor prediction of "roughly double."** Chart fragmentation ate
the rest. §3 pre-registered this outcome as itself the finding, and it is: **the atlas
layout, not the visibility of the surface, is now the binding constraint on texel density.**

## The gate unit change is ratified

Changing the recession gate's *unit* rather than its *threshold* was correct, and the
reasoning is the proof: a pixel count at zero is unachievable by construction when the
residual **grows** with gate resolution (28 faces at 1880 px, 66 at 3008 px). That is a
finite-sampling asymptote. Area converges, and under UV-exclude a missed face costs a flat
patch of exactly its own area, so area is the unit with meaning. 0.155% against a 0.5% limit.

## Three defects the depth gate caught, all real

1. **The visibility set was not a superset of the production set** — 228 faces visible from a
   production camera were culled.
2. **Point sampling cannot represent partial visibility** — a face half-hidden behind an arm
   is visible, but if no sample origin lands in the exposed sliver it reads unseen. Fixed by
   unioning with a rasterisation from the production cameras, which *is* the operational
   definition of visibility.
3. **The executor's own centroid checksum was too brittle to be a guard** — Blender's float32
   `polygon.center` and trimesh's float64 agree to 5.6e-8, which straddles a 5-decimal
   rounding boundary on thousands of values, so an exact hash mismatched on a perfectly
   aligned mask. **A guard that fires on a correct input is worse than no guard.**

## Open: the blotches

Three provenances are possible and they mean entirely different things — twins (style,
canon), brush (invention, like the belt braid), or dilation (defect). Provenance is tracked
per texel, so this is one measurement, not an opinion. Pending.
