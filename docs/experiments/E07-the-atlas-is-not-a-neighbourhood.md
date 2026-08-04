# E07 — The atlas is an index, not a neighbourhood

**Status:** SPEC — ready to run
**Author:** advisor session, 2026-08-05, on E06's report and ruling
**Priority:** highest of the three named defects. E08 (chart fragmentation) waits on it, and
is partly defused by it.

---

## 0. Rules

Unchanged: no verdicts, no memory writes, stop at gates, FLAT for texture and `--clay` for
geometry, predictions before looking. Read [E06's report](E06-report.md) and
[its ruling](E06-ruling-gate1.md) first.

**This spec asserts three code-level facts. Check them before designing around them** — the
advisor asserting them has a poor record, catalogued in [CLAUDE.md](../../CLAUDE.md), and two
of the three are the whole premise of an arm.

> ### Amendment 1 (advisor, 2026-08-05, ruling at Gate 0.5)
>
> Both premises confirmed; neither halt fired. Two things in this spec are wrong and both are
> the advisor's. Modifies **§5** (L2's pass condition) and **§7** (L1's ANDON).
>
> **§7's back-facing ANDON measured a proxy instead of the thing. WITHDRAWN.** The failure
> mode of a surface-aware lookup is *sourcing colour from somewhere else on the figure*. I
> gated on normal disagreement as a stand-in for that. The executor measured the quantity
> itself and the proxy inverts: **the back-facing class is the *closest* class** — 0.77 edges
> median against 1.16 for the agreeing class, 66.7% of it inside a single triangle — and
> **0.00% of any lookup reaches beyond 20 edges**, against 72.2% for the flood that ships
> today. Normal disagreement at sub-triangle range is not a reach across a gap; it is a
> description of a sheet thinner than its own tessellation. And the pipeline **routes the
> blade flank to this operation on purpose** (`--thin-extent`, the policy that thin
> hard-surface props take dilated colour and never invented content), so the gate fired
> hardest on the surface class the design deliberately hands it.
>
> Same move E06 made on the recession gate: *the unit was wrong and was changed; the threshold
> was not.* The gate is **restated on source distance, in median triangle edges** — halt if
> the median exceeds **3 edges** or if more than **5%** of lookups exceed **20 edges**.
> Measured: 0.87 edges and 0.00%, so it passes with room, which is the point — a guard that
> fires on a correct input is worse than no guard. Normal disagreement stays **reported, never
> a halt**.
>
> **The hemisphere variant is rejected, not deferred.** Priced by the executor and strictly
> worse: 1.52× farther, source changed for 13.27% of lookups, and **no answer at all for
> 36.7%** — which is what a thin plate predicts, because the whole local neighbourhood is the
> opposing face. It buys agreement with a proxy the distance measurement supersedes.
>
> **⚠ `edge = 0.00290` is hardcoded** in `texpass_finalize.py` as "median triangle edge, this
> mesh". Harmless while it only scales a printout; **load-bearing the moment the gate is
> stated in edges**. Compute it from the mesh. This is the same family as the blade rectangle
> `texpass_loop.ps1` was rewritten to remove, and E04's galleon is the subject it would break
> on.
>
> **L1 is authorised to run**, gate unit changed, no other parameter touched.
>
> **§5's L2 pass condition was mis-formed. WITHDRAWN, not retuned — fourth in the ledger.**
> "Closes half the distance from its baseline to 1.0" was written before the baseline was
> known, so its difficulty scales with how bad the problem turns out to be: at my predicted
> baseline of 1.5 the bar would have been 1.25, a trivial move; at the measured 5.500 it is
> 3.25, a 41% cut in the step. **A worse baseline should not mean a harder bar.** I have no
> calibrated number for "a seam that is no longer visible", and inventing one now — after
> seeing 5.000 — would be the worst version of this error. Precedent: `project_twins`'
> `assert seen.mean() > 0.30` was **suspended rather than retuned** for exactly this reason.
>
> Replacing it: report the numerator and denominator separately in quanta, as the executor's
> Gate 0 already requires, and let **Gate 1** rule on whether the seam is gone. The numeric
> instrument's remaining job is deciding whether to spend the GPU, and that decision is made
> on mechanism — see Amendment 2.
>
> ### Amendment 2 (advisor, 2026-08-05) — L2's GPU spend is NOT authorised yet
>
> The executor's Gate 0.5 §2 hypothesis is well founded, and it reads out of the source
> without a measurement. `commit` accepts a strict **subset** of the job mask — hole ∧
> `facing > 0.25` ∧ visible ∧ in-mask ∧ edge-distance ([texpass_iter.py:220-242](../../tools/texpass_iter.py)).
> So a provenance boundary in the finished atlas sits at the **facing/visibility frontier**,
> generally interior to the mask contour, while §7 step 2 anchors the membrane's Dirichlet
> condition **at the contour**. The correction decays across the gap before it reaches the
> seam it was built to level. `TWINS|s7` moving 9.500 → 8.250 while `TWINS|s1` did not move at
> all is consistent with an anchor that sometimes lands near the seam and sometimes does not.
>
> **Re-anchor, then re-run the free instrument.** The membrane's boundary is the boundary of
> the **accepted set** — `hidx` after the filter chain, whose view-space `px, py` commit
> already has in hand. Dirichlet **only where the outside neighbour is already styled**;
> natural (unconstrained) elsewhere, because where the neighbour is still a hole there is no
> level to match and forcing one invents a target.
>
> That costs ~2 minutes offline. Spending 15 GPU minutes to measure a mis-anchored membrane
> more expensively is the wrong order, and avoiding exactly that is what §7's bound was
> specified for. **If the re-anchored bound moves substantially, the rerun is authorised on
> the spot. If it moves marginally again, the mechanism is small, we say so plainly, and L2
> is a recorded negative — which is a full success.**

## 1. The premise, at the code level

The texture loop writes colour into the atlas from two places. Neither one knows where a
texel's neighbours are **on the surface**.

**Fact 1 — `texpass_iter.py commit` has no levelling term.** It writes the sampled brush
colour straight in: `a2[hidx] = col` ([texpass_iter.py:249](../../tools/texpass_iter.py)).
`gaussian_filter` appears in that file exactly once, in the selftest's fake-inpaint blur at
line 276. Meanwhile the same masked-Gaussian levelling exists twice elsewhere —
[project_twins.py:253-256](../../tools/project_twins.py) and
[bake_hero_fuse.py:233-237](../../tools/bake_hero_fuse.py), the latter documented as *"the
multi-band/Poisson role"* with `--seam-sigma 16.0`. The operation was built, and it was never
carried into the loop. E06 found the consequence: the forehead is a **provenance boundary**
between twin paint and the `y+000_e+55` stroke, with **2 blotch pixels in the whole disc** —
a tonal step, not a defect in either source.

**Fact 2 — `texpass_finalize.py`'s flood is not island-constrained, despite its docstring
saying it is.** Line 6 claims *"valid-island-constrained"*. The code
([texpass_finalize.py:43](../../tools/texpass_finalize.py)) is:

```python
fill = ~grown & (cnt > 0)      # no  & valid
img[fill] = acc[fill] / cnt[fill][..., None]
grown |= fill
```

`valid` appears only in `todo`, which decides **when to stop**, never **where to write**. So
gutter texels are filled on the first iteration, become sources on the second, and the front
walks across the ~4-texel gutter into the neighbouring island. `todo` going empty does not
stop it either — the loop runs a further 16 steps by design, for mips.

The arithmetic that follows is on measured C1 quantities, not an inference: **39.0% of
islands contain zero painted texels and hold 50.7% of the post-loop hole set.** Against
813,773 dilated texels that is roughly **412,000 texels — ~17% of the valid atlas — whose
colour can only have arrived from a different island.** E06 measured dilated texels at
**4.80× enrichment** in blotch pixels while being 5.0% of clean pixels. The mechanism and the
enrichment are the same object.

**Fact 3, recorded but not acted on — stage 1's levelling is itself atlas-space.** `σ = 16`
on a 4096 atlas draws correction from ~48 texels away, across a 4-texel gutter, on charts
averaging 16.4 faces. It is sourcing across islands too. It shows **no** measured harm — twin
texels are the *cleanest* provenance at **0.24×** enrichment — so it is measured here and
changed nowhere. It is stated because it is the trap waiting for the obvious implementation
of arm L2.

**The unifying statement:** commit never asks for a surface neighbourhood; finalize asks the
atlas, which is an index and not a neighbourhood. Both fixes are local. Neither is a
geometry change.

## 2. The question

**Does giving the loop a surface neighbourhood remove the defect class the Director named?**

Two independent write paths, one missing operation each, measured separately so a null result
on one does not hide a result on the other.

## 3. Predictions — recorded before the run, and blind

Written by the advisor with no measurement beyond E06's tables and the source above.

| # | prediction | arm |
|---|---|---|
| P1 | dilation-provenance blotch pixels **848 → below 400** (E06: 24.0% of 3,533) | L1 |
| P2 | total blotch pixels **3,533 → 2,600–2,900** | L1 |
| P3 | **more than 20%** of nearest-painted lookups source from surface whose normal disagrees by **>60°** — residual holes live in crevices and on the blade flank, where the nearest painted surface is the *opposing wall* | L1 |
| P4 | the cross-provenance step ratio (§5) is **above 1.5** at baseline | Gate 0 |
| P5 | levelling takes that ratio **below 1.2** | L2 |
| P6 | **L2 barely moves the blotch count.** A step is low-frequency; `\|L − median₅\|` is high-pass and tracks straight over it. The forehead disc had two blotch pixels and a visible seam | L2 |
| P7 | L3 ≈ L1 + L2, within noise. The two paths touch disjoint texel sets by construction | L3 |

P6 is stated **because judging L2 on the blotch count would be the fourth mis-specified pass
condition in four experiments.** Each arm is graded on the unit it was built to move; the
units are fixed in §5 before any of it runs.

## 4. Arms

| arm | change | cost | needs GPU |
|---|---|---|---|
| **L0** | C1 as shipped — E06's finished asset | 0 | no |
| **L1** | surface-aware dilation. `texpass_finalize` rebuilt; **replayed from C1's saved state**, brush untouched | ~2 min | no |
| **L2** | commit-time seam levelling, in **view space**. Full loop rerun | ~15 min | yes |
| **L3** | both | ~15 min | yes |

L1 is a strict post-process on a state directory that already exists. It re-runs finalize,
pack and the renders and nothing else — **no reconstruction, no twins, no strokes, no
diffusion.** If it fails, it cost two minutes.

## 5. Metrics, and the unit each arm is graded on

All arms render the **same mesh** from the **same head camera** with the **same framing**.
`hit.sum()` is therefore **490,544 figure pixels in every arm, frozen by construction** —
which is what makes an absolute pixel count safe here where three previous ratios were not.

**Reported for every arm** — the E06 table unchanged: valid texels · atlas coverage · brush
vs dilation split · colourless islands and their hole share · styled/valid · speckle at
0.10/0.15/0.25 against A0's 2.43/1.18/0.30 · final atlas variance · the full
`texel_provenance` enrichment table.

**Grading unit, L1 — absolute blotch pixels at the head zoom, and their provenance split.**
Baseline 3,533 of 490,544, of which 848 are dilation. **Pass: total below 3,100 and
dilation-provenance below 400.**

**Grading unit, L2 — the cross-provenance step ratio.** Defined on the head render, using the
`claim.npy` that `texel_provenance.py` already writes:

> for every 4-adjacent pair of figure pixels, take `|ΔL|`. Partition the pairs by whether the
> two pixels carry the **same** provenance label or **different** labels. The ratio
> `median(|ΔL|)_cross / median(|ΔL|)_within` is the step magnitude in units of the surface's
> own local contrast. **1.0 means a provenance boundary is indistinguishable from ordinary
> texture variation.**

It is honest in both directions: flattening lowers the numerator *and* the denominator, so
smoothing the asset does not flatter it. **Pass: the ratio closes at least half the distance
from its baseline to 1.0** — with the baseline established at Gate 0, and with §6's premise
test deciding whether that condition means anything at all.

**Guard against the failure mode, both arms.** The failure mode of any de-blotching operation
is **flattening**. Fix the pixel set to those that were *clean* in L0 — the same pixels in
every arm, since geometry and camera are frozen — and report `mean(|L − median₅|)` over it.
A correct low-frequency levelling leaves a high-pass statistic untouched. **ANDON: halt if it
falls more than 5%.** Report atlas variance beside it.

## 6. Gate 0 — test both premises before building either fix

**Free. No GPU. Everything below is on disk already.**

1. **Does colour actually cross the gutter?** Instrument the *existing* finalize: carry a
   source-island label beside the colour through the flood. Report the fraction of dilated
   texels whose colour originated in a different island, and the fraction of propagation
   paths that passed through an invalid gutter texel. Also read C1's finalize log for its
   `took mean fallback` count — if it is 0, every colourless island was filled from across
   the gutter and the §1 arithmetic is exact rather than an upper bound.
   **If cross-island import is below 10% of dilated texels, L1's premise is refuted. Halt and
   report.**
2. **Is there a step to level?** Compute the §5 step ratio on the C1 asset from the existing
   `claim.npy` and head render. **If the baseline ratio is below 1.25, L2's premise is
   refuted, the pass condition is meaningless, and L2 is not built. Halt and report.**
3. **Fact 3, measured, changed nowhere.** For a sample of styled texels, what fraction of a
   σ=16 Gaussian's weight falls on texels belonging to a *different* island? Report the
   median. This is information E08 needs; it is not an arm.

## 7. Method

### L1 — surface-aware dilation

`pos.npy` carries the 3D position of every valid texel and `nor.npy` its normal. Both are
already on disk.

1. Build a `cKDTree` over the **painted** texels' 3D positions. Query every remaining hole
   texel for its nearest painted texel and take that colour. ~814k queries against ~1.6M
   points — seconds.
2. **Then** run the existing 16-step dilation into **invalid** texels only, for mips. That
   part was always correct; the bug is that the current code lets those gutter texels become
   sources *during* the fill.
3. **Report the operation's failure mode, not its success mode.** Distribution of
   nearest-painted distance; fraction of lookups whose source normal disagrees by >60° and by
   >90°. A crevice's opposing wall is a plausible source and a strictly better prior than
   "whatever island the packer placed next door"; the *far side of a thin plate* may not be.
   **ANDON: halt if more than 20% of lookups source from a back-facing normal (`n·n' < 0`)**
   and report, rather than silently shipping a hemisphere restriction — that restriction is a
   variant to be measured, not a fix to be assumed.

### L2 — commit-time seam levelling, in view space

**In view space, adjacency is surface adjacency.** That is the whole reason this is not a
copy of stage 1's atlas-space Gaussian — see Fact 3.

At commit, before sampling the edited render:

1. **`emit` must save its depth buffer** (`t_hit`) beside `render.png` and `mask.png`. Small
   addition; needed by step 4.
2. Pair the ring just **outside** the job mask (where `render.png` shows the colour already
   on the surface) with the ring just **inside** it (where `inpainted.png` shows the brush's
   own level). `diff = outside − inside` on that contour.
3. Solve for a correction field `O` over the masked region: `O = diff` on the contour,
   `∇²O = 0` inside. A Jacobi iteration — masked 4-neighbour average holding the ring fixed,
   a few hundred passes at 752×1024 — is a Laplace solve and takes milliseconds. This is the
   membrane form of Poisson seam levelling, in the correct space.
4. **The membrane must not cross a depth discontinuity, and must not leave `hit`.** Without
   the depth constraint an arm's correction leaks onto the chest behind it — the exact class
   of error the ownership baker exists to kill. Use the buffer from step 1.
5. `corrected = inpainted + O`, then sample as now.
6. **Cap `|O|`.** A correction beyond ~0.15 in luminance is not a seam, it is a disagreement,
   and levelling it smears a wrong colour across the region instead of revealing it.
   **Report per stroke how much of the mask hit the cap.** A stroke needing a large correction
   is a stroke that invented, and that is worth knowing on its own.

`commit`'s existing invariants are untouched: only hole texels are written, and the selftest's
`styled texels byte-identical` assertion still holds by construction. **Run the selftest
before the first real stroke.**

### L2's bound, before any GPU is spent

`texel_provenance.py` already replays `commit`'s filter chain exactly from the saved job
directories. Apply the §7 levelling inside that replay to produce a **counterfactual atlas**
— levelled, but using the *original* brush outputs — and compute the step ratio on it. ~1 min.

This is a **bound, not a result**: a true rerun changes each stroke's context and therefore
what the brush paints. But if the counterfactual does not move the ratio, either the
implementation is wrong or the premise is, and the GPU should not be spent. **Halt and report
if it does not move.**

## 8. Gates

**Gate 0 — §6, before either fix is built.** Both premises, numerically. Halt on either.

**Gate 0.5 — L1 complete, and L2's offline bound.** Report both tables. **Halt.** L1 is
cheap enough that a null result there is worth a ruling on its own, and the L2 bound decides
whether the loop rerun happens at all.

**Gate 1 — the finished assets.** Head close-up at the Director's zoom and a FLAT turnaround,
each arm beside **C1**, same framing and light, at his zoom and not from a contact sheet.
Predictions §3 first, then the numbers, then his eye. The Director's verdict is the verdict;
§5 decides only whether the GPU was worth spending.

## 9. Out of scope

**Chart fragmentation and remeshing.** It is the binding constraint on texel density and it
gets E08 with a clean premise. It is *not* entangled here — and note that L1, if it works,
changes what a colourless island costs: today it takes a neighbour's colour, and after L1 it
takes its own surface's. That lowers the price of fragmentation without addressing it.

**Stage 1's atlas-space levelling.** Measured at Gate 0, changed nowhere. Changing it in the
same experiment would confound the loop measurement, and there is no evidence of harm to
chase — twins are the cleanest provenance in the asset.

Also out: E03 head graft, E04 galleon, subject profiles, the unseen faces' shared patch,
widening the camera set, any change to the mesh, the twins, the prompts, the stroke order or
the seed.

## 10. Standards compliance

**PIN_PER_STEP 3** — L1 replays a state directory that already exists, byte-for-byte; L2
reuses E02-prompts.json, seed 770700, the same eight cameras in the same order. Every path is
a parameter.

**ANDON_AUTHORITY 3** — five numeric halts, and each tests a *failure* mode rather than a
success mode: both premises at Gate 0, the back-facing-source fraction on L1, the flattening
guard on both arms, and the offline bound before the GPU.

**NAMED_COMPENSATORS 2** — no irreversible or outward-facing call in the experiment; the only
mutation is an atlas under a state directory. L1 cannot mutate anything, since `finalize`
reads state and writes to `--out`. L2 **must** be seeded into a fresh `facet_E07/L2/state`
from `styled_stage1.png`; C1's state directory is read-only input and must never be passed as
`-StateDir`. Undo = delete `facet_E07/` and re-seed. Owner: the executor session.
*Remediation: the separation is stated here and not asserted by the code — `texpass_loop.ps1`
should refuse a `-StateDir` it did not seed. Next session that touches the loop.*

**DECOMPOSE_BY_SECRETS 3** — the two fixes live in two files that share nothing. L1 touches
only `texpass_finalize.py` and needs no GPU, no brush and no ComfyUI. L2 touches only
`texpass_iter.py`. Either can be shipped, or withdrawn, without the other.

**UNCERTAINTY_GATED_HUMANS 3** — Gate 0 and the L2 bound are numeric and cost the Director
nothing. Gate 1 is his, and is framed contrastively: §3's predictions are recorded first, so
he is shown what was expected against what arrived.

**EXTERNAL_VERIFIER 3** — pass conditions are absolute, pre-registered, and **different per
arm because the arms change different things**. The step ratio is falsifiable in both
directions. The aesthetic verdict belongs to the Director, against an asset he has already
judged.
