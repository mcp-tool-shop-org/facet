# E08 — advisor ruling at Gate 0

**Date:** 2026-08-05 · **Report:** [E08-gate0.md](E08-gate0.md)

Both halts tested, neither fired. Both open questions ruled. **The arm order changes** — and
it changes on the executor's own arithmetic, not on anything imported.

---

## 1. Half 1 — RATIFIED, and two of my predictions are dead

74.10% against a 60% floor. **A2 falsified**: I predicted above 80% at eight cameras; the
measurement gives 68.52% at uniform 0.45 and 74.10% at production thresholds, and *twelve*
cameras plus two elevated at the loosest threshold still reach only 79.06%. There is no camera
count in the tested range that reaches 80%.

**A1b falsified, and it is actionable.** I predicted the four diagonals carried the gain. The
two **sides** add 267,176 texels; the four diagonals add 247,979. Half the cameras, more
surface. Camera priority is therefore **front → back → the two sides → the diagonals**, and if
a budget ever forces a choice, the diagonals are what gets cut.

## 2. Half 2's substitution — RATIFIED

Hold-one-out at N=2 has a population of exactly zero, and the reason is structural rather than
a bug: `facing_front = −N_y` and `facing_back = +N_y` cannot both clear a positive threshold.
**My §5 asked one construction to do two jobs that no camera count satisfies simultaneously** —
validate on the rejected asset (which has 2 views) and grade R8 (which needs ≥4). That is a
spec error of the same family as the four before it, and the executor found it by construction
rather than by running into it.

Reference agreement is the right substitute because it answers §4's actual requirement: does
the instrument fire on the defect *before* it grades anything. It does, decisively — null at
**ΔE 0.72** where the asset carries its reference, **23.18** on brush, **18.70** on dilation,
and every region the Director named separated from the controls he did not by **18–65×**. The
blade reads the sentence in numbers: neutral steel (123,122,124) → flesh (147,97,63), median
**32.71**.

Three notes on the instrument, all ratifying:

- **Sampling the atlas directly rather than through a Blender render was correct**, and it
  avoided a trap this repo has already paid for twice — `exposure 0.85` under the Standard view
  transform is a nonlinear remap that would have landed entirely inside ΔE.
- **CIE76 is the right formula here and my spec was loose.** I wrote "ΔE in CIE Lab" and later
  worried about CIEDE2000; CIEDE2000 is fitted to *small* differences and misbehaves at the
  magnitude we care about. CIE76 (Euclidean in Lab) is sound at ΔE > 10. A measured-better
  option at this magnitude is **HyAB** — |ΔL*| plus Euclidean Δ(a*,b*) — noted for the next
  build, not required now.
- **This is one half of the instrument, not the whole one.** The colour term is now in place;
  E07's five units were all *feature* terms. Report both from here on and never again only one.

**Standing rule, earned:** the metric-validation halt is what caught this before it graded an
arm. It stays in every spec.

## 3. The ruling that reorders the spec — acceptance is the FIRST lever

The executor asked whether the acceptance stage is the second lever or the first. **It is the
first, and its own arithmetic settles it.**

```
2 cameras reach                  1,265,391   52.66% of valid
2 cameras actually style           681,212   28.36%          <- 53.8% acceptance
8 cameras reach                  1,780,546   74.10%
8 cameras at 53.8% acceptance    ~957,900    ~39.9%   (estimate)
2 cameras at PERFECT acceptance  1,265,391   52.66%
```

**Fixing acceptance on the two twins we already have would buy more reference coverage than
quadrupling the camera count at today's acceptance rate.** 52.66% against ~39.9%. Camera count
raises the ceiling; acceptance decides what fraction of the ceiling is realised; the two
multiply, and we have been pushing only one of them.

**And there is a second, structural finding in our own source.** `project_twins` applies an
**absolute** facing gate *before* ownership is computed:

```python
idx = np.where(facing > fmin)[0]     # absolute cutoff, line 185
...                                   # visibility, edge, mask
take = w > best_w[idx]                # comparative ownership, line 222 — only among survivors
```

A texel seen obliquely by *every* camera is rejected by all of them and falls through to
invention — even though one of those cameras sees it better than the others do. The
comparative rule we already have never gets to arbitrate it, because the absolute rule already
threw it away. **The gate and the ownership rule are in the wrong order.**

> ### ⚠ Amendment 1 (advisor, 2026-08-05) — the mechanism above is FALSIFIED. The conclusion is not.
>
> **The reorder is a no-op, measured.** Comparative ownership is byte-identical to the absolute
> gate at floors 0.45, 0.25 and 0.10. I read the loop as gate-then-arbitrate; it is
> **arbitrate-across-independently-gated-views**. Each view accumulates its own accepted set and
> updates `best_w` separately, so a texel the best-facing view rejects **is already supplied by
> a worse-facing one**. The fallback I said was missing has been in the code the whole time.
> And the facing floor is not the lever either — 0.45 → 0.05 buys **+1.31 points**, toward a
> setting the Director already rejected on other grounds.
>
> **"Acceptance is the first lever" survives** — the executor's own table carries it without my
> mechanism:
>
> | removed | styled | of valid | gain |
> |---|---|---|---|
> | as shipped | 681,212 | 28.35% | — |
> | no EDGE | 892,299 | 37.14% | +211,087 |
> | no MASK | 938,723 | 39.07% | +257,511 |
> | **neither** | **1,265,391** | **52.66%** | **+584,179** |
>
> **The root cause is an E01 fix that never reached its second consumer.** `project_twins`
> treats `*_mask.png` as the mesh silhouette. Against the silhouette its own raycasting scene
> already builds: **146,356 px true against 111,602 used, IoU 0.76**, and only 216 px the other
> way — a near-strict subset. Registration ruled out at shift (0,0). The loss is *interior*: a
> stripe down the whole blade, patches through pauldrons, chest, greaves, boots. `figure_mask`
> keys the **clay** render at tol 0.06, and flat-grey-on-flat-grey is the exact property
> [E01](E01-facial-structure-ceiling.md) identified when Canny returned 0.84% edge pixels.
> **E01 fixed it by compositing onto contrast — for the control-image path only. The mask path
> never got the fix.** One root cause, two consumers, one repaired.
>
> **And a load-bearing comment in the source is wrong.** `project_twins:158-161` justifies
> eroding the twin's mask because "the twin is painted fatter than the mesh (15.8% vs 9.9%,
> IoU 0.777)." Both figures reproduce exactly — **against the wrong objects.** 15.81% is the
> *eroded twin*; 9.94% is the *saved keyed mask*, which is the broken artifact. Measured
> against the true silhouette it is twin **17.43%** against mesh **19.01%**, IoU **0.911** —
> **the mesh is fatter**, with 12,625 px of it outside the twin's paint. The premise that made
> erosion safe is void, and the comment is corrected in place rather than deleted.
>
> **Ruled — do not fix the keying; remove it.** `project_twins` already has the raycasting
> scene. The mesh silhouette is available *exactly*, from geometry, with no threshold, no
> tolerance and no dependence on how the render was lit. That is the repo's own preference for
> eliminating a risk over gating it, and it retires a heuristic that has now produced two
> separate defects.
>
> **The EDGE test is not deleted with it.** E01's background-keying failure is real and
> independent, and this repo already states the rule the bug violated: *one mask cannot answer
> two questions.* The reason it went wrong is that the mask answering **"is there surface
> here"** was never the mesh silhouette — it was a keyed clay render impersonating one. With an
> exact silhouette the two questions finally separate as designed, and the erosion applies only
> to **"is the paint trustworthy"**.
>
> **Arm A2 is authorised:** rebuild stage 1 with the raycast silhouette in place of the keyed
> mask, edge erosion retained against the twin's own paint. Grade on reference coverage against
> 28.35% and on the Gate 0 ΔE instrument. Whether the recovered surface is *good* is the
> Director's at a gate — coverage is not quality, and this repo has confused the two before.
>
> **Two executor self-corrections worth keeping.** The first mask check compared the saved mask
> against its own dilation — an operation that cannot lose a pixel — and returned 0.00%. It was
> reported as *untested*, not as confirmation. That is the same family as E06's silhouette-IoU
> gate, caught one step earlier. And a one-sided rejection band that looked like a registration
> offset was tested by shift search and was not one.

The mechanism claim in the paragraph above was falsified by measurement — see Amendment 1. It
is left in place because the correction is more useful than the original. (A parallel research dispatch has surfaced published
methods that rank views comparatively rather than by absolute cutoff, with a defensible
empirical basis for a ~60° incidence limit — but those citations have **not** cleared the
verification gate and are **not** load-bearing for this ruling. See
[RG01](../research/RG01-texture-route-grounding.md).)

## 4. Consequently: R8 is no longer the first arm

E08's §6 is amended. The arm that runs next needs **no new twins, no diffusion and no GPU**,
because it re-runs stage 1 on the two twins already on disk:

**Arm A — acceptance.** Reorder the gate: compute ownership across all cameras *first*, assign
each texel to the camera that sees it best, and apply rejection only where the best available
camera is genuinely unusable. Separate the three rejection causes that are currently fused —
the facing cutoff, the edge-distance guard, and the twin-mask test — and report what each one
costs in texels. The edge and mask tests exist for measured reasons (E01's silhouette band,
E01's background keying) and are **not** to be removed; the question is how much of the 46.2%
they are rejecting *unnecessarily*, which nobody has measured because the three were never
separated.

Grade it on reference coverage as a share of valid texels — 28.36% today — and on the ΔE
instrument this gate just validated.

**Arm B — R8**, unchanged in intent, after Arm A, because the two multiply and Arm A's
multiplier applies to every camera R8 adds. Running R8 first would spend eight restylize passes
at a 53.8% acceptance rate we already know is the binding term.

**A2 is retired as a target.** "Cover the figure" is not available: 74.10% is the eight-camera
ceiling and ~79% is the ceiling at any count tested. The honest framing of E08's question is
**"raise reference from 28% toward the ceiling"**, and the ceiling is a measured 74%, not 100%.

> ### Amendment 2 (advisor, 2026-08-05) — A2 ratified; my grading instruction was half wrong
>
> **[Arm A2](E08-armA2.md) is ratified and adopted as the default stage-1 path.** 681,212 →
> **938,718** styled, 28.4% → **39.1%** of valid, 53.8% → **74.2%** of reachable, **lost 0** —
> strictly additive, on the two twins already on disk, with no diffusion and no GPU. The
> `--mask-keyed` escape hatch reproduces C1's shipped stage 1 byte-for-byte (`b12917a2c7c14c4b`),
> so every prior arm stays comparable.
>
> The discipline is what makes it adoptable rather than the number: a reproduction anchor
> before the change, a strictly-additive check, a **failure-mode** test aimed at the specific
> way this change could have gone wrong — if the silhouette were too fat, recovered texels
> would carry the twin's background — and then a look at the sheet. Recovered texels sit at
> median **ΔE 38.31** from background grey with **0.18%** within ΔE 10, *cleaner than the
> 681,212 texels that were already trusted* (38.99 / 0.32%). **That background-ΔE probe is now
> the standard check on any change that widens an acceptance mask**, and it is the executor's
> instrument, not mine.
>
> **My §4 grading instruction was half wrong and the executor was right to refuse it.** I said
> grade A2 "on reference coverage against 28.35% *and* on the Gate 0 ΔE instrument." A stage-1
> ΔE grade is **vacuous by construction** — recovered texels carry the twin's own colour, so
> comparing them against that twin returns ~0 whatever the change did. Reference agreement only
> earns its keep on a **finished** asset, where recovered reference has displaced invention and
> interpolation. Corrected: stage-1 arms grade on **coverage plus the background-contamination
> probe**; ΔE grades finished assets only.
>
> ### The blade, and the erosion arm — A3
>
> The blade is still hole, now held by the EDGE test rather than the mask, and the geometry is
> the point: **a ~15 px blade has almost no interior left after 3.8 px of erosion from each
> side.** The erosion is scaled by *global figure width* (`esc = fig_w / edge_ref`) and applied
> to *local* structures, so its cost runs inversely with local feature width. That is the same
> shape as the blade rectangle `texpass_loop.ps1` was rewritten to remove — a global constant
> governing a local feature — and the same shape as E01's silhouette-band erosion, which cost
> 480k texels because a peel near an edge-on region removes far more than the same peel
> elsewhere. Three instances now; it is a pattern, not an incident.
>
> **A3 is authorised, and it is a build with an invariant rather than a tuning pass.** The
> erosion must never remove more than a bounded fraction of a structure's own width, whatever
> that width is. `dist_in` — the distance transform already computed — carries the local
> half-width, so a scale-free criterion is available without new machinery; the construction is
> the executor's call. **Gate it on its failure mode:** per connected structure in the twin
> mask, report the fraction of area the erosion removes, and halt if any structure loses more
> than a stated share. That check would have caught this on the first character.
>
> A3 does **not** delete the erosion. Its stated justification is void (Amendment 1) but the
> failure it was built for — background-grey mixing at the twin's painted boundary, measured as
> white flecks — is real and unaddressed by anything else.
>
> ### The GPU, and why it waits for A3
>
> Not authorised yet, and the reason is the Director's own verdict rather than caution. A2
> raises reference to 39.1% while leaving the blade — **the loudest defect he named** — still
> hole. A loop run now would put an asset in front of him with a flesh-toned blade, which is
> the thing he already rejected, and would spend the GPU to re-answer a question he has
> answered.
>
> Sequencing, and the attribution stays clean: **A2 and A3 are both stage-1 changes and both
> are measurable for free on coverage**, so single-variable attribution happens without a GPU
> at all. One loop run then goes on the combined best configuration, and it is a **Gate 1
> artifact** — its job is to answer the only question the GPU can answer, which is whether the
> Director accepts the asset. It is not an attribution experiment and must not be reported as
> one.
>
> **The executor's scoping is ratified in full:** A2 supports exactly one claim, that reference
> coverage rises 28.4% → 39.1%. Whether the defect goes with the coverage is unanswered.
> Declining to claim more than the arm supports is the behaviour this repo exists to protect.

> ### Amendment 3 (advisor, 2026-08-05) — the stratum gate is WITHDRAWN. It was my quantity.
>
> **The invariant holds exactly.** `e = min(absolute, ⅓ × local half-width)`, max `e/R` =
> **0.3333** against a 0.3333 bound, **zero violations on both views**, both reproduction
> anchors intact. The build is correct.
>
> **The gate fired on it anyway** — 43.8% of the back's 8–16 px stratum against a 40% limit —
> and that is the condition this repo already names: *a guard that fires on a correct input is
> worse than no guard.* **Withdrawn, not retuned.** Retuning a threshold after seeing 43.8%
> would be the one move that is always wrong here.
>
> **The quantity is mine, not the executor's.** Amendment 2 said "per connected structure in
> the twin mask, report the fraction of area the erosion removes, and halt if any structure
> loses more than a stated share." The executor derived the 40% from the bar relation and owned
> that; the deeper error is the quantity I named, and it is wrong in two independent ways:
>
> - **Unimplementable as worded.** "Per connected structure" does not partition a character —
>   the whole front figure is **one component of 121,709 px** because the blade touches the
>   hand, so a blade losing three quarters of its area reads as 12.3%. The executor rejected my
>   wording on measurement and stratified by half-width instead. **That construction is
>   ratified**; it is strictly better and it is what made the diagnosis visible.
> - **It measures shape as much as erosion.** Stratum area-loss is a perimeter-to-area
>   statistic — ragged and tapering structures shed more per unit area — and it is *not*
>   bounded by the invariant that governs `e`. The deviation runs both ways and exceeds the
>   headroom: front 16–32 px lands **10.8 points under** the bar idealisation, back 8–16 px
>   **10.4 points over**. A quantity that swings ±10 points on shape alone cannot carry a halt.
>
> Sixth mis-specified condition in this repo, and this one is shared: the executor picked the
> number, I picked the thing being measured.
>
> ### What replaces it
>
> **1. The stratum table is retained and REQUIRED — as a diagnostic, never a halt.** It is the
> evidence that earned A3 and it belongs in every report of it:
>
> | half-width | 1–2px | 2–4px | **4–8px** | 8–16px | 16–32px | 32+px |
> |---|---|---|---|---|---|---|
> | shipped | **100%** | **100%** | **77.6%** | 37.6% | 22.5% | 4.4% |
> | invariant | 0% | 0% | 33.5% | 33.7% | 22.5% | 4.4% |
>
> Monotone annihilation of thin structure by a distance chosen from the figure's global width.
> The blade is that 4–8 px stratum, and **77.6% of it was removed by a guard built to delete a
> 1–2 px rim.**
>
> **2. `e/R ≤ ⅓` is retained as an implementation assertion, labelled as such.** It verifies
> the code computes what it claims — it can fail on an operand-order slip or a bad half-width
> lookup — but it **cannot fail on a correct build**, so by this repo's own rule it is a unit
> test, not an andon. Do not promote it.
>
> **3. The andon moves to the direction the invariant does not bound.** `e ≤ ⅓R` bounds
> over-erosion *by construction*, which is why a halt there fires on correct work. A3's live
> risk is the opposite one: **loosening an acceptance mask admits background grey at the twin's
> painted boundary** — E01's measured white-fleck failure, which the invariant says nothing
> about. The instrument already exists and is already standard: **the background-ΔE probe** the
> executor built for A2. Halt if newly-admitted texels approach the twin's background colour.
> Same check, same anchor, aimed at the failure that is actually unwatched.
>
> **A3 resumes under that gate.** `--edge-frac` was never what fired and stays at ⅓. Front
> coverage of 633,518 against A2's 555,185 is a partial and stays unreported as a result until
> the back view completes.

## 5. What this does not settle

Whether ~40–53% reference coverage is *enough* for the Director to accept the asset is not a
question any of this answers. The defect-severity table is the closest evidence — the blade at
62% non-reference reads ΔE 23.17, the tunic at 1.2% non-reference reads 0.49 — and it suggests
severity falls with non-reference share rather than switching off at a threshold. Gate 1
remains his.
