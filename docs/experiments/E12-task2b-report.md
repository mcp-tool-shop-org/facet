# E12 handoff 2, Task 2.3–2.4 — the thin curve and the elevated question

**Executor session, 2026-08-05.** Continues [E12-task2-report.md](E12-task2-report.md)
(2.1 prep bake, 2.2 reach ceiling). Predictions committed blind in `96b59c1`. Split into its
own file because 2.1–2.2 were already committed and ruled on; nothing here revises them.

---

## Task 2.3 — the `thin_extent` cost curve, measured fresh

```
e12_thin_curve.py --glb E12_prep/prep_uv.glb --aspect 1792,1024 --fit-axis width
                  --views 0,45,90,135,180,225,270,315
                  --region-a 0:1120,0,1791,1023 --region-b 90:0,0,1791,1023
```

**What the quantity is, stated because the curve is meaningless otherwise.** `thin_extent` is
not a mesh property. `texpass_iter.emit` fires the emit grid twice — forward from the near
plane, backward from the far plane — and forms `ext = 2D − tF − tB` per **pixel**: the
front-to-back extent of the object along that view ray. Anything with `ext < thin_extent` is
removed from the hole mask and takes projected/dilated colour instead of diffusion. So the
quantity is **per view, screen space, canonical units**, and `e12_thin_curve.py` reproduces
that computation exactly — same canonicalisation, same `D = 2.0`, same `basis()`, same
fit-axis block, same grid — so a value read off this curve means the same thing when
`texpass_iter` receives it.

**On this subject's ruled framing one emit pixel is 6.718107e-04 canonical units**, so the
inherited values are: ship's 0.01 = **14.9 px**, character's 0.03 = **44.7 px**.

**The region is spatial, not a thickness criterion** — selecting the membranes by thinness and
then measuring how much of them is thin is circular and would report ~100% at every value. It
is the half-space laterally outboard of the body (the body spans screen-x 700–1100 at yaw 0),
read off the extent previews and drawn back onto every view for checking. **Its impurity is
known and one-way:** the box contains the wing arm, finger struts and wing claw, which are
thick rods, so their presence can only push the withheld fraction DOWN. Every region number
below is a floor on what the membrane proper loses, never an overstatement.

| `thin_extent` | emit px | **FIGURE withheld** | **WING region withheld** | region / figure |
|---|---|---|---|---|
| **0 — the tool default** | 0.0 | **0.000%** | **0.000%** | — |
| 0.0005 | 0.7 | 0.060% | 0.054% | 0.90 |
| 0.001 | 1.5 | 0.126% | 0.117% | 0.93 |
| 0.002 | 3.0 | 0.311% | 0.282% | 0.91 |
| 0.003 | 4.5 | 0.749% | 0.580% | 0.77 |
| 0.005 | 7.4 | 3.016% | 3.730% | 1.24 |
| 0.0075 | 11.2 | 10.480% | 17.382% | 1.66 |
| **0.01 — the ship's** | 14.9 | **15.304%** | **26.819%** | 1.75 |
| 0.015 | 22.3 | 22.147% | 39.805% | 1.80 |
| 0.02 | 29.8 | 26.595% | 47.499% | 1.79 |
| **0.03 — the character's** | 44.7 | **33.863%** | **60.418%** | 1.78 |
| 0.05 | 74.4 | 46.221% | 73.811% | 1.60 |

**0.0 is on the curve because it is what undecided actually runs.** The tool's own default
disables the guard entirely: nothing is withheld, and every thin structure — membranes,
spines, frill, claws — goes to diffusion.

**The headline is worse than the dispatch's warning.** The warning was that a filament-tuned
value could withhold a third of this subject's membranes. Measured: the **character's 0.03
withholds 60.4% of the wing region and 33.9% of the entire visible animal**; the **ship's
0.01 withholds 26.8% and 15.3%**. Neither inherited value is usable here, and the damage is
not confined to membranes — **at 0.03 a third of the whole beast stops being diffused.**

**And the mask is far less membrane-selective than predicted.** The region/figure ratio peaks
at **1.80×**, never approaching the 3× I predicted. The thin mask is eating tail spines,
frill spikes, claws and thin limb sections alongside the membranes, which is why the figure
column climbs almost as fast as the region column. A single global value cannot separate
"membrane" from "everything else thin on a dragon", because on this subject **most of the
detail is thin**. That is a stronger statement than "0.03 is too big for a membrane", and it
is the one the spec has to design against.

**The knee sits between 0.005 and 0.0075**: 3.7% → 17.4% of the wing region in one step, and
3.0% → 10.5% of the figure. Reported, not adopted.

### The pinch-field comparison — a clean negative

The dispatch asked for the 7,138-edge region against a clean membrane area of the same mesh.
Gate 0 mapped that pinch field onto the **+x** wing, so the identical curve was run on the
**−x** wing as a control:

| `thin_extent` | +x wing (**carries the pinch field**) | −x wing (control) | difference |
|---|---|---|---|
| 0.005 | 3.730% | 3.946% | −0.216 |
| 0.01 | 26.819% | 26.772% | +0.047 |
| 0.03 | **60.418%** | **60.248%** | **+0.170** |
| 0.05 | 73.811% | 73.665% | +0.146 |

**No measurable difference.** The wing carrying 7,138 non-manifold edges behaves like the wing
that does not, everywhere on the curve. The pinch field is a topology defect, not a thin-mask
behaviour difference — which is useful for the spec's arms, because they need not treat it
specially on this axis.

**Boundary, stated so it is not over-read:** the region is a whole-wing half-space, so this
measures *does the wing carrying the pinch field behave differently as a wing*, not *do pinch
texels behave differently from clean membrane texels*. Isolating pinch texels in screen space
would be a different instrument, and the dispatch arms no gate on this.

## Task 2.4 — the elevated-camera question

```
e12_elevated.py --glb E12_prep/prep_uv.glb --fit-axis width
```

Up-facing = face normal z > 0.5 in the canonical frame. Coverage is **first-hit**, the
criterion `cull_unseen` uses, weighted by **area, not face count**.

**Up-facing surface: 250,897 faces, area 0.601444 of 2.269096 — 26.51% of this subject.**

### The measurement is ray-sampling sensitive, and that had to be established first

A face counts as reached only if some ray's first hit lands on it, so a grid coarser than the
tessellation under-counts. Tested before any number was reported:

| ray grid | eye-level eight reach |
|---|---|
| 896 × 512 | 39.286% |
| **1792 × 1024** (the emit frame) | **48.106%** |
| 3584 × 2048 | **49.594%** |

Quadrupling the rays once moved it **+8.8 points**; quadrupling again moved it **+1.5**. The
emit-frame number is therefore *not converged* and the low-resolution one is badly wrong. The
value is approaching roughly **50%** and is quoted that way rather than as 48.106%.

### What the eight already reach, and what elevation buys — at 4× rays

**The eight eye-level cameras reach 49.594% of up-facing area. 50.4% is unreached.**

| candidate | marginal gain | cumulative |
|---|---|---|
| **0/180 @ 40** | **+1.768 pts** | 51.362% |
| 0/180 @ 55 | +1.744 pts | 51.338% |
| 90/270 @ 55 | +1.661 pts | 51.255% |
| top-down (0 @ 90) | +1.194 pts | 50.788% |
| 90/270 @ 40 | +0.975 pts | 50.569% |

Second round on top of the winner: 90/270 @ 55 buys +0.323, everything else less. **After two
elevated pairs, 48.3% of up-facing area is still unreached.**

### The finding: this subject's up-facing surface is SELF-OCCLUDED, not under-viewed

The ship adopted an elevated pair because decks were sky-facing surface no eye-level camera
could see, and elevation bought them. Here elevation buys **1.8 points against a 50-point
deficit**. The unreached half is not waiting for a higher camera — it is the underside of the
folded wing, the surface between wing and body, and the interior of the mouth, none of which
**any exterior camera reaches**. That is `cull_unseen`'s territory, not the camera set's, and
it is why the ship's lever does not transfer.

**And the "winner" is not a real ordering.** At the emit grid `0/180 @ 55` wins by 0.008
points; at 4× rays `0/180 @ 40` wins by 0.024. Both margins sit far inside the sampling
sensitivity the resolution study just measured. **The two candidates are indistinguishable.**

That matters beyond taste, because the E06 superset answer flips with them: `0/180 @ 55` is
**inside** `cull_unseen`'s 26-camera default and needs no union re-issue; `0/180 @ 40` is
**outside** it and forces one. **A union re-issue must not be triggered by a ray-density
artifact.**

**Recommendation withheld, and this is its honest form:** the numbers support *suspending* the
elevated question on this subject rather than adopting any pair — the lever that paid on the
ship does not pay here, and no candidate separates from another by more than noise. The ruling
owns the decision; this report supplies the curve and the sensitivity that bounds it.

## Predictions scored — 2.3 and 2.4

| # | prediction | outcome | measured |
|---|---|---|---|
| Q9 | >50% of membrane area withheld at 0.03 | **held** | 60.418% |
| Q10 | >15% withheld at 0.01 | **held** | 26.819% |
| Q11 | largest value withholding <5% of membrane is below 0.005 | **FALSIFIED, narrowly** | 0.005 itself gives 3.730%; the crossing sits between 0.005 and 0.0075 |
| Q12 | region fraction ≥ 3× the figure fraction at 0.03 | **FALSIFIED** | **1.78×** — and the more useful result: the mask is not membrane-selective, because on a dragon most detail is thin |
| Q13 | the pinch field behaves measurably differently | **FALSIFIED** | +0.17 points at 0.03; the two wings are indistinguishable |
| Q14 | >25% of up-facing area unreached by the eight | **held** | ~50% |
| Q15 | best single addition is an elevated pair, not the top-down | **held** | pairs beat top-down at both densities |
| Q16 | 0/180 @ 55 beats 0/180 @ 40 | **FALSIFIED as worded, INDETERMINATE in fact** | wins at 1792, loses at 3584, both inside noise |
| Q17 | unreached up-facing < 10% after the best pair | **FALSIFIED, badly** | **48.3%** |
| Q18 | adopted camera inside the cull default, no union re-issue | **INDETERMINATE** | the answer flips with ray density — which is itself the finding |

**Task 2 total across both reports: 11 held, 6 falsified, 1 indeterminate, of 18.** The three
most useful entries are all falsifications — Q12 (the mask is not membrane-selective), Q13
(the pinch field is inert on this axis), and Q17 (elevation does not reach what the eight
miss).

## What has NOT run

Tasks 3, 4 and 5. **No generation has run and no credits have been spent.** Task 3 is the
backdrop derivation, Task 4 the two-view styled pair on cloud, Task 5 the palette bands. The
styled-pair halt goes to the advisor's eye first.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Every framing operand, view list, candidate value and region spec lands in the JSON beside the numbers; both wing runs and all three ray densities recorded |
| ANDON_AUTHORITY | 3 | The region tool raises on non-orthogonal views and on a z disagreement past tolerance; the elevated tool raises on a degenerate basis at the pole rather than silently producing a wrong frame |
| NAMED_COMPENSATORS | 3 | Read-only measurement; new instruments and JSONs only; no profile written, no value adopted, no spend |
| DECOMPOSE_BY_SECRETS | 3 | Every number derived from this mesh at this subject's ruled framing; the two inherited `thin_extent` values are quoted only as points on this subject's own curve |
| UNCERTAINTY_GATED_HUMANS | 3 | Nothing adopted. The elevated recommendation is explicitly withheld with the reason — the candidates do not separate by more than measurement noise — rather than resolved by picking the top row |
| EXTERNAL_VERIFIER | 3 | The thin curve was validated against a control region on the same mesh (the −x wing) rather than trusted; the elevated coverage was tested at three ray densities before being quoted, which is what caught both the non-convergence and the winner flip |
