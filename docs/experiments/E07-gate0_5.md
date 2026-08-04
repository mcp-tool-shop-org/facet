# E07 — Gate 0.5

**Spec:** [E07-the-atlas-is-not-a-neighbourhood.md](E07-the-atlas-is-not-a-neighbourhood.md) ·
**Gate 0:** [E07-gate0.md](E07-gate0.md)
**Run:** 2026-08-03, executor session, all local. No GPU spent.

Gate 0.5 is an unconditional halt: *"L1 complete, and L2's offline bound. Report both
tables. Halt."* **L1 is not complete — its ANDON fired.** Both tables are below.

**Nothing was mutated.** `facet_E06/C1/` was read-only throughout; `finalize` and the L2
replay both read `--state` and write to `--out`. C1's shipped atlas still hashes
`dcc4a80c5e5d6b44` and its loop atlas `6e9b452d96979982`, both re-verified this session.

---

## L1 — HALTED at the back-facing ANDON

```
python tools/texpass_finalize.py --state facet_E06/C1/state --prep facet_E06/C1/prep \
       --surface-aware --out facet_E07/L1/atlas_final.png
```

```
[finalize] filling 813,773 hole texels (surface-aware)
[finalize]   source distance  median 0.00253  p95 0.01709  max 0.06394  (median edge 0.0029)
[finalize]   beyond  5 edges   7.78%   beyond 20 edges  0.00%
[finalize]   source normal disagrees >60deg 56.58%   BACK-FACING (n.n'<0) 48.67%
AssertionError: ANDON: 48.67% of lookups source from a back-facing normal, over the 20%
limit. Report it; do not add a hemisphere restriction here — that is a variant to be
measured.
```

**48.67% against a 20% limit — 2.4× over.** The assert precedes the save, so no atlas was
written and no L1 arm exists. Per §7 and `CLAUDE.md` rule 3, no parameter was changed and
nothing was re-run.

Two things the spec asked for *did* land before the halt, and they are worth reading:
source distance **median 0.00253 — below one triangle edge**, and **0.00%** of lookups
reaching beyond 20 edges, against the shipped flood's median 0.17733 (61 edges).

### Evidence for the ruling

[`tools/diagnostics/e07_l1_andon.py`](../../tools/diagnostics/e07_l1_andon.py). The spec left
the reading deliberately open — *"a crevice's opposing wall is a plausible source and a
strictly better prior than whatever island the packer placed next door; the far side of a
thin plate may not be."* The measurement separates those two cases.

| nearest painted texel, by normal agreement | share | source distance median | p95 |
|---|---|---|---|
| agrees, >60° (n·n′ > 0.5) | 43.42% | 0.00336 (1.16 edges) | 0.01672 |
| oblique, 0–60° | 7.91% | 0.00500 (1.72 edges) | 0.02573 |
| **back-facing (n·n′ < 0)** | **48.67%** | **0.00223 (0.77 edges)** | 0.01647 |

**The back-facing class is the *closest* class**, and **66.7% of its sources lie within one
triangle edge** (79.5% within two, 92.6% within five). These are not reaches across a gap to
an opposing wall. They are the other side of a surface thinner than its own tessellation —
the blade, cloth, straps — which is the same physical feature at this mesh's resolution.

The variant the spec forbade applying, **priced but not applied**:

```
same-hemisphere restriction (nearest painted texel with n.n' > 0, k=64)
  resolvable within k        63.26%      (298,964 lookups, 36.7%, have NO agreeing
                                          normal among their 64 nearest painted texels)
  distance median            0.00384 (1.32 edges)   vs 0.00253 unrestricted -> 1.52x
  would change the source for 13.27% of lookups
  reference: the SHIPPED atlas flood sources from a median 0.17733 (61 edges)
```

The restriction has **no defined answer for 36.7% of the holes**, which is what a thin plate
predicts: the whole local neighbourhood is the opposing face. Both variants remain ~50–70×
closer than what ships today.

### On the gate itself

The gate did its job — it fired before anything shipped, on a genuine property of the
operation, and it forced the open question into the open rather than letting a hemisphere
restriction slip in unmeasured. Unlike E06's centroid checksum it did not fire on a correct
input; whether 48.67% *is* a defect is exactly the question it was built to raise.

One observation, offered as measurement rather than judgement: **the threshold conflates two
things the data separates.** `n·n′ < 0` is a proxy for "wrong source", but a back-facing
source 0.77 edges away and a back-facing source 20 edges away are different events, and only
the second is what the spec was worried about. On this mesh 0.00% of *any* lookup reaches
beyond 20 edges.

---

## L2 — the offline bound

[`tools/diagnostics/e07_l2_bound.py`](../../tools/diagnostics/e07_l2_bound.py), §7's levelling
applied inside `texel_provenance`'s replay. Depth was never saved by `emit`, so it is
recomputed offline by recasting emit's own rays from `cam.json`.

**Fidelity check first.** The replay with `--no-level` reproduces C1's loop atlas
**byte-identically** (`6e9b452d96979982`), with all eight per-stroke claim counts matching
`provenance.log` exactly. The counterfactual is therefore a counterfactual of the real thing.

| stroke | claimed | \|O\| lum median | p95 | mask at cap |
|---|---|---|---|---|
| 1 y+045_e+00 | 219,966 | 0.0066 | 0.0583 | 0.51% |
| 2 y+315_e+00 | 146,419 | 0.0078 | 0.0779 | 0.83% |
| 3 y+135_e+00 | 124,483 | 0.0118 | 0.0723 | 0.59% |
| 4 y+225_e+00 | 126,930 | 0.0121 | 0.0733 | 0.79% |
| 5 y+090_e+00 | 39,599 | 0.0142 | 0.0895 | 1.70% |
| 6 y+270_e+00 | 44,347 | 0.0172 | 0.0959 | 1.71% |
| 7 y+000_e+55 | 135,397 | 0.0157 | 0.0920 | 1.55% |
| 8 y+180_e+55 | 62,154 | 0.0170 | 0.0900 | 1.41% |

No stroke needed a large correction: under 1.8% of any mask hit the 0.15 cap. By §7 step 6's
reading, no stroke invented at a scale levelling would have smeared.

### The grading unit

| | C1 (L0) | L2 offline bound | |
|---|---|---|---|
| median \|dL\| **within** provenance (denominator) | 0.00523 (4.0 quanta) | **0.00523 (4.0)** | unchanged |
| median \|dL\| **across** provenance (numerator) | 0.02876 (22.0 quanta) | **0.02614 (20.0)** | −9.1% |
| **step ratio** | **5.500** | **5.000** | |
| cross-provenance inside one island | 4.500 | 4.000 | |
| island boundary, same provenance | 1.500 | 1.500 | unchanged |
| TWINS \| s7 — the forehead | 9.500 | 8.250 | |
| TWINS \| s1 | 4.750 | 4.750 | unchanged |
| blotch px at the head zoom | 3,533 | **3,248** | −8.1% |
| speckle >0.10 / >0.15 / >0.25 | 0.72 / 0.28 / 0.05 | 0.66 / 0.25 / 0.04 | |
| final atlas variance | 0.03606 | 0.03497 | |
| holes entering finalize | 813,773 | 822,303 | +8,530 |

**Flattening guard (§5), over the 487,011 head pixels that were clean in L0:**

```
mean |L - median5|   C1 0.005850  ->  L2 bound 0.005813   -0.62%   (ANDON at -5%)
```

**Passes.** The correction removed step without smoothing texture — the denominator did not
move at all, and the high-pass statistic is flat. That is the operation behaving as designed.

### Against the pass condition

§5: *"the ratio closes at least half the distance from its baseline to 1.0."* Baseline 5.500,
so the pass line is **≤ 3.25**. The bound reached **5.000** — it closed **0.5 of the required
2.25**, about 11% of the distance.

§8's halt is narrower: *"Halt and report if it does not move."* **It moved.** So the stated
halt did not fire, and the stated pass condition is far out of reach. Both are true, and the
gap between them is the advisor's to rule on.

### Two things that bear on how conservative this bound is

1. **The counterfactual cannot compound; a rerun would.** Each stroke here is levelled
   against `render.png` from its saved job directory — which was rendered from the
   *unlevelled* atlas. In a true rerun, stroke N+1 emits a view of a surface stroke N already
   levelled, so the seam it inherits is smaller before its own correction applies. This
   bound understates a rerun by an unmeasured amount.
2. **The correction is small relative to the step it targets** — median \|O\| 0.007–0.017
   luminance against a measured cross-provenance step of 0.029. Offered as a hypothesis for
   why, testable and not tested here: the Dirichlet condition is evaluated at the **job-mask
   contour**, whereas a provenance boundary in the finished atlas falls where the
   facing/visibility filter chain divided two strokes' claims — which is not the same locus
   in any one view. If so, the membrane is being anchored somewhere other than where the step
   appears, and that is a design question about L2 rather than a tuning question.

The per-boundary table is consistent with both readings and settles neither: `TWINS|s7` moved
9.500 → 8.250 while `TWINS|s1` did not move at all.

---

## Predictions

| # | prediction | outcome |
|---|---|---|
| P1 | dilation-provenance blotch 848 → below 400 (L1) | **untested** — L1 halted |
| P2 | total blotch 3,533 → 2,600–2,900 (L1) | **untested** — L1 halted |
| P3 | >20% of lookups source from normals disagreeing >60° | **CORRECT, understated** — 56.58% disagree >60°, 48.67% back-facing |
| P4 | baseline step ratio above 1.5 | **CORRECT, understated** — 5.500 |
| P5 | levelling takes the ratio below 1.2 | **FALSIFIED at the bound** — 5.000 |
| P6 | L2 barely moves the blotch count | **SUPPORTED** — −8.1% |
| P7 | L3 ≈ L1 + L2 | **untested** |

P3 deserves a note: the advisor predicted the >60° disagreement as a *reason residual holes
live in crevices*, and named the blade flank. The measurement agrees on the number and points
at a different cause — not crevice walls at a distance, but opposing faces of thin surfaces
at **0.77 edges**.

The executor's own four Gate 0 predictions went 1-for-4; the failures and their causes are
recorded in [E07-gate0.md](E07-gate0.md#predictions-vs-measured).

---

## Open, for the ruling

1. **L1's ANDON.** Is 48.67% back-facing a defect, or a description of a mesh whose plates are
   thinner than their tessellation? The gate as written cannot tell those apart; the data
   above can. If the threshold stands, L1 as specified cannot run at all, and the
   hemisphere variant has no answer for 36.7% of holes.
2. **L2's GPU spend.** The bound moved the ratio 0.5 of a required 2.25, passed the
   flattening guard cleanly, and is conservative by an unmeasured amount. §8's halt did not
   fire; §5's pass condition is not close.
3. **`bake_hero_fuse.py:257` carries the same unconstrained flood** as the finalize defect
   Gate 0 measured. Out of scope for E07, unmeasured, still shipping.

Artifacts: `facet_E07/gate0/` (Gate 0 + PREDICTIONS.md), `facet_E07/L1/andon.json`,
`facet_E07/L2bound/` (counterfactual atlas, GLB, FLAT head render, `l2_bound.json`).
