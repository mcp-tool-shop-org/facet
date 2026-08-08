# Known defects, named

*Everything the route does not do well, measured and located in code. It stays
written down because a defect nobody wrote down becomes doctrine. The
[README](../README.md) carries the short list; this page is the full one.*

---

<!-- Moved out of README.md by the E19 treatment, 2026-08-08, at the Director's
     word ("the readme reads more like a changelog"). NOT rewritten: every line
     below is byte-identical to the README it left, corrections and ⚠ annotations
     intact. The README now links here. -->

## Known defects, named

**Two thirds of the asset is not the reference.** ⚠ *Corrected in place twice. An earlier
version said the two-view limit was a hardcoded list; fixed —* `project_twins.py` *takes N
views since `c469b36`, anchors pixel-identical. A later version said the acceptance lever was
spent at 82.4%; restated in E08 Amendment 28 — union acceptance is a function of camera
count, and eight cameras reached 92.9% of reachable with no test changed.* The stage-1 state
is now **68.8% of valid referenced at eight cameras** against a 74.1% reach; what fraction of
the *finished* asset the reference covers is Task 3's measurement.

**The blade band takes 0.00% of stage-1 reference — the measured mechanism behind E07's
"the blade carries no reference."** The twin's key excludes the greatsword band in every
measured view: its paint sits *on* the key's threshold (median residual 0.0657 / 0.0645
against the 0.06 cut) because steel on a grey studio backdrop is grey-on-grey — the project's
fifth instance — and the size-5 erosion removes the half that passes. Outside the trust mask
`dist_in` is 0 by definition, so every candidate texel there is rejected: 46,197 / 31,699 on
the current twins, 42,984 / 74,997 in the A2 lineage, **0 accepted in all four rows, in both
arms of the intersection regression** — the intersection neither caused nor repaired it. The
0.06 cut is a global constant governing a local low-contrast feature. At eight cameras the
per-view rate is 0.00% on all eight; the union rescues 55.72% of the band. **On the finished
asset the blade band runs 47–61% dilation against the whole asset's 27%, carrying 30–47%
reference where E07's blade carried none** — the worst-served structure by both measures,
visible as the orange stripe on every provenance panel of the Gate 1 sheet. Measured in
[E08-intersection-regression.md §9a](experiments/E08-intersection-regression.md),
[E08-eightcam.md §5](experiments/E08-eightcam.md) and
[E08-task3-report.md §4](experiments/E08-task3-report.md); the blade arm is specified
after Gate 1 with this as its targeting data.

**⚠ The defect list below was written against high-pass metrics** that
[E07's ruling](experiments/E07-ruling-gate1.md) found blind to the defect that decides
acceptance. Each entry is still measured and still true; none of them is established as the
thing that makes the asset unacceptable.

**Stroke seams are not levelled.** Stage 1 applies a low-frequency Gaussian levelling
across projection boundaries. **The brush loop has none** — so every boundary between two
strokes, and between stage 1 and the first stroke, is an unlevelled tonal step. Provenance
replay found the forehead "blotch" on the current asset is exactly this: twin paint below
meeting the overhead stroke above, two blotch pixels in the whole disc, a step rather than a
defect in either source. The architecture called for Poisson seam levelling; it was
implemented in projection and never carried into the loop. **Located in code:** the levelling
term is `project_twins.py:253-256` and `bake_hero_fuse.py:233-237` (`--seam-sigma 16.0`, its
own docstring calling it *"the multi-band/Poisson role"*); in `texpass_iter.py`, `commit`
writes `a2[hidx] = col` (line 246) and `gaussian_filter` appears only in the selftest's fake
inpaint. **Measured** in [E07 Gate 0](experiments/E07-gate0.md): a provenance boundary
steps **5.5× ordinary texture variation** (median |ΔL| 0.02876 across, 0.00523 within), and
the forehead the Director named is **9.5×**. Dilation boundaries are nearly flat at 1.5–1.75
— dilation blends *from* its neighbour by construction — so the step is a brush-boundary
phenomenon, not an artifact of the denominator.

**Dilation still bleeds between unrelated islands.** Down from 75% of hole texels to 33.9%
of the atlas, but dilation-filled texels remain **4.8× enriched** in visible blotches
against a 5% base. Colour crosses the gutter from whichever island the packer placed next
door, and atlas adjacency is not surface adjacency. **Located in code, and the docstring was
wrong:** `texpass_finalize.py`'s flood predicate is `fill = ~grown & (cnt > 0)` with no
`& valid` — `valid` decides when to stop, never where to write.
[E07 Gate 0](experiments/E07-gate0.md) measured the cost by replaying that flood
carrying a source label: **74.9% of 813,773 dilated texels take their colour from another
island**, from a median **0.177 away on a figure 1.0 tall** — 61 median triangle edges, 18%
of the figure's height.

**The gutter is not the mechanism, and the minimal patch is worse than it looks.** Only
**32.5%** of paths cross an invalid texel; adding the missing `& valid` still leaves 53.3%
cross-island and strands **174,898** texels on the mean fallback, 238× more than now.
`--pack-margin 0.001` does not put a gutter between all charts — 5.73% of 4-adjacent valid
texel pairs are in different islands and touching *directly*, half of them more than 20 edges
apart on the surface. The fix is a surface neighbourhood, not a predicate: nearest painted
texel in 3D sources from a median **0.00253 — below one triangle edge**, a 70× shrink, closer
for 92.4% of the same texels.

**⚠ `bake_hero_fuse.py:257` carries the identical unconstrained flood.** Not on the current
route — the E06 recipe invokes `bake_hero_prep`, `project_twins`, the loop, `finalize` and
`bake_hero_pack`, not `fuse` — and unmeasured. Recorded here so it cannot quietly become
doctrine; it gets the same surface-aware primitive whenever `fuse` returns to the route.

**Chart fragmentation is the binding constraint on texel density.** Culling invisible
surface removed 47% of faces but only 34% of charts — because invisible surface is
interleaved *within* charts, so excluding it perforates them rather than freeing them.
Faces-per-chart fell 20.5 → 16.4, bbox fill 42.1% → 36.6%, packed coverage 24.81% → 14.32%.
Net texels landing on visible surface rose ~17% where a naive reading predicts double.

**Paint lives in big charts; holes live in small ones.** Measured in
[E07 Gate 0](experiments/E07-gate0.md): the island holding a randomly chosen *styled*
texel has a median 1,231 texels (~35×35), the island holding a *dilated* one has 296. So
atlas-space operations are safe exactly where there is already paint and unsafe exactly where
there is not — which is why stage 1's σ=16 levelling draws only 6.8% of its weight
off-island (median) and does no measured harm, while the dilation flood at the same scale
does. Beware the inspection paradox in either direction: the median island holds 88 texels,
but the median *texel* does not live in a median island.
