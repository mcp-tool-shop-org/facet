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

> ### Amendment 4 (advisor, 2026-08-05) — the erosion was accidentally correct; A3 is withdrawn, A4 authorised
>
> **The andon placement earned itself.** Moved to the direction the invariant does not bound, it
> fired on its first live run and found a real defect: **75.13%** of newly-admitted texels
> within ΔE 10 of the twin's background against **0.11%** for the already-trusted set. First
> gate this session to fire on something wrong rather than on correct work.
>
> The executor validated it in both directions before claiming anything — it fires on a
> deliberately loose build (`--edge-frac 0.02` → 49.45%), and when A3's number came in *higher*
> than that loose run, which is backwards, the obvious alternative explanation was tested and
> **falsified**: the blade sits at median ΔE **24.80** from background with 3.2% within 10, and
> nothing the twin paints is near its own background. The probe is not misfiring on grey
> subject matter. The contamination is real.
>
> ### What it inverts
>
> **The absolute erosion was doing a job nobody had written down.** Its stated justification was
> void (Amendment 1 — the mesh is fatter than the twin), but by deleting 100% of the thinnest
> strata it was removing background-contaminated tendrils along with the blade. The twin's keyed
> figure mask carries background colour concentrated **200×** in thin structure — 21.3% of the
> 1–2 px stratum against 0.1% at 32+ px — while being only **0.5% of the mask overall**, which
> is why four experiments never saw it. That is E01's background-keying failure, alive in these
> twins as cast shadow, gradient and antialiased fringe.
>
> **Amendment 1 declined to delete the erosion when its justification was voided. That was
> right, and it was right by luck rather than by foresight** — the reason given was E01's
> white-fleck failure, and the actual reason is this. Recorded that way rather than as a good
> call.
>
> **The mechanism, restated: contamination is a boundary phenomenon.** A2 already rejects
> anything outside the exact raycast silhouette, so surviving contamination sits *inside* the
> mesh — at the band where the twin's painted edge meets it. A 1–2 px structure is entirely
> edge. **Half-width is not a property of thinness; it is a proxy for what fraction of a
> structure is boundary**, which is exactly why the contamination concentrates there. Thin
> structures are not special. They are all edge.
>
> ### A3 is withdrawn as specified
>
> The executor's diagnosis is exact and I ratify it: **half-width is shape-blind and cannot
> separate a blade from a shadow tendril**, because they live at the same scale. The invariant
> preserves thin structure proportionally, so it preserves both. Geometry cannot make this
> distinction, and no threshold on `e/R` will.
>
> The invariant itself is **kept, and correct** — max `e/R` 0.3333, zero violations, blade
> stratum 77.6% → 33.5% removed. It is a necessary component of the answer, not the answer.
> Stopping rather than tuning `--edge-frac` was the right call; the parameter was never what
> fired and stays at ⅓.
>
> ### A4 — move the discriminator from geometry to colour
>
> **Authorised.** The property we care about is *is this pixel background-contaminated*. We have
> been testing a geometric proxy for it — distance to a boundary — and the proxy fails exactly
> where the subject is thin. The background-ΔE probe tests the property directly, is already
> computed per sample, and separates cleanly on this twin: contaminated tendrils sit within
> ΔE 10, real subject at median ΔE ~25.
>
> Accept a twin sample on its distance from the twin's **own** background colour, at any
> structure width; keep whatever residual absolute floor pure antialiasing turns out to need,
> measured rather than assumed.
>
> **Gate A4 on its failure mode, which is a different subject.** This discriminator degrades
> when a subject's material approaches its background — and this pipeline has a subject
> staged for exactly that: **E04's galleon, grey on grey.** Before applying the rule, measure
> the separation between the twin's subject colours and its background and **halt if there is
> no gap**. Report the separation with every run so a future subject fails visibly rather than
> silently.
>
> **Derive the threshold from the measured bimodality; do not pick it.** The gap between ~10 and
> ~25 on this twin is the evidence. A number chosen inside a measured gap is defensible; a
> number chosen because it worked is the seventh mis-specified condition.
>
> **A structural alternative, named and not specified.** Contamination is only ambiguous because
> the twin's background is flat grey and so are some of its materials. Rendering the clay
> against a background no subject material uses would eliminate the ambiguity rather than gate
> it — this repo's stated preference. It is **not** free: the diffusion latent comes from the
> untouched render, so the background colour reaches the twin and would change its appearance.
> A candidate for its own arm, with its own before/after, not a rider on A4.
>
> **Front's 633,518 stays unbanked**, as the executor reported it. A partial from a halted run
> is not a result.

> ### Amendment 5 (advisor, 2026-08-05) — A4 withdrawn; the background arm is promoted
>
> **There is no bimodality, and the inference that there was one is mine.** I wrote "the gap
> between ~10 and ~25 on this twin is the evidence." That gap was between two **summary
> statistics** — region medians against the contaminated set's median — and distant medians do
> not imply an antimode in the density between them. Measured, ΔE-from-background rises
> monotonically from ~5 to 30 with no antimode anywhere, and the two views do not even agree on
> a location: the back has a shallow dip at 11–14 that the front does not share.
>
> The precondition attached to A4 — *halt if there is no gap* — is what caught this, before a
> build and before a GPU. Recorded because it is the counterexample to the six conditions that
> did not work: it gated the arm's **premise** rather than its result.
>
> **Otsu's own output says it is the wrong tool**, and the executor read it correctly rather
> than taking the number: cut 33.6, class means 25.8 / 41.6, rejecting 41,194 px at a median
> depth of **8 px** — deep in the interior. With the contaminated class at 0.5% of the mask,
> between-class variance finds the dominant split, which is dark paint against light paint.
> **η = 0.661 looks healthy while partitioning the wrong thing.**
>
> **And colour is not a proxy for boundary either.** Only **47%** of sub-ΔE-12 pixels lie within
> 2 px of the mask edge; the rest is interior paint that is simply dark or neutral. Restricting
> to thin strata does not rescue it — 16–28% of those pixels are legitimate paint above ΔE 25,
> the blade among them. **A4 is withdrawn**, not deferred: no placement of a threshold on this
> distribution separates the two populations, because they are one population.
>
> ### The background arm is promoted, and it now has a measured mechanism
>
> The reason no gap exists is in the numbers: the background is mid-grey **(125,126,126)** and
> the subject carries mid-grey steel, leather and shadowed cloth. **Same gamut.** A background
> outside the subject's gamut would *create* the separation rather than threshold a
> distribution that has none — which is this repo's stated preference for eliminating a risk
> over gating it, and it is no longer speculative.
>
> **The colour is derived, not picked.** Compute the subject's gamut from the *existing* twin,
> choose the background maximising minimum distance to it, and report that minimum. A number
> chosen because it looked far enough is the seventh mis-specified condition.
>
> **Gate it on the risk I flagged, which is real and unmeasured.** The diffusion latent comes
> from the untouched render, so the background reaches the twin and can change what it paints.
> Pin everything else — same mesh, same seed, same prompt, same control construction — vary
> only the render's background, and:
>
> 1. **Halt if the subject repaints.** Measure ΔE between the two twins *inside the exact mesh
>    silhouette*. The twin is the reference for the whole route; an arm that improves keying by
>    changing the reference has broken the thing it was protecting.
> 2. **Halt if the separation does not appear.** Re-measure the ΔE-from-background density on
>    the new twin and confirm an antimode exists. The arm's entire premise is that it creates
>    one.
> 3. **Require both views to agree on it.** Front/back disagreement is what killed A4's
>    threshold; agreement is now a stated property, not an assumption.
>
> If the subject repaints, the arm fails and the honest position is that this twin's keying is
> not separable — in which case the contaminated band goes to stage 2 as hole, which is what the
> absolute erosion already does, at the blade's cost, and we would then know that cost is
> necessary rather than accidental.
>
> **A2 stands. A3's invariant is kept and correct. Front's 633,518 stays unbanked.**

> ### Amendment 6 (advisor, 2026-08-05) — the halt is ratified; one bounded arm before the line closes
>
> **REQ 2 fired as designed and the arm is withdrawn.** Median ΔE **14.30 / 11.41** inside the
> exact silhouette, 69.9% / 56.1% above ΔE 10, and the executor looked before concluding: it is
> **material-level, not a hue shift** — gold knee plates gone, charcoal boots to brown fur,
> wine-red skirt to green, on the exact terms the prompt held byte-identical. An arm that
> improves keying by rewriting the reference has broken what it was protecting.
>
> **REQ 1 produced the session's cleanest single number.** Derived background rgb (0,0,255) at
> min ΔE **123.31** to the subject gamut, against the current grey at **6.00** — *below the
> ΔE 10 line, i.e. the background is effectively inside the subject's own gamut.* That is
> A4's failure expressed in one figure, and it should be quoted whenever someone proposes
> thresholding a keyed mask on colour again.
>
> **REQ 3 passed and falsified a prediction worth keeping:** the render background beat an
> explicit "plain grey background" prompt term at denoise 0.92. The render, not the text, owns
> the background.
>
> ### The confound the executor flagged is load-bearing, and I am not letting it go
>
> The control image changed too — contour **33,026 → 9,699 px** — because it is built from the
> keyed clay mask and the mask became correct. The executor called this unapportionable, which
> is right for *this* run. But their own observation points hard at which side it came from:
>
> **A latent colour cast produces a hue shift. This was not a hue shift; it was identity and
> material.** And identity drift under a weakened control is the mechanism [E01](E01-facial-structure-ceiling.md)
> already measured in this repo — a control that constrains nothing lets the model regenerate
> the character freely, which is how silhouette IoU 0.290 became 0.777 when the control was
> *strengthened*. A 3.4× reduction in control pixels is a large weakening, and the drift
> signature matches control weakness rather than latent contamination.
>
> **One arm, bounded, before this line closes: hold the control constant and vary only the
> latent background.** Build the control image from the **exact mesh silhouette** rather than
> any keyed mask — the same move A2 made for the projection path, and it removes `figure_mask`
> from the last place it governs anything. Then the blue and grey renders differ only in what
> reaches the latent.
>
> - **If the subject still repaints**, the background reaches the latent and rewrites identity.
>   The arm is dead, the erosion's cost is confirmed necessary, and this line closes with three
>   falsified alternatives instead of two-and-a-confound.
> - **If it does not**, we get colour separation, a correct keyed mask *and* the blade — and the
>   whole A3/A4 sequence resolves.
>
> Cost is one twin pair, ~2 minutes of GPU, against a prize that decides the arm. Pre-registered
> so it cannot be read either way after the fact.
>
> **Everything else stands as reported.** Generating both sides with the same pinned prompt was
> correct — it is what "vary only the render background" requires, and comparing against the
> shipped twin would not have been. `turn_render` gaining `--bg` with the default unchanged, and
> the clay re-render reproducing the shipped views byte-for-byte, are the right shape.
>
> ### A repo defect this uncovered, recorded separately
>
> **The shipped asset's back twin cannot be reproduced.** Its prompt is not in the repo:
> `E02-prompts.json` holds the eight brush strokes, not the two twin cameras, and
> `restylize_views.py` takes a single `--prompt` for all inputs whose default is front-flavoured.
> E02's report states a different prompt was used for the back. That is a provenance hole in a
> shipped artifact, and it is the same failure `texpass_loop.ps1` was rewritten to fix when a
> recipe existed only in a log. **`restylize_views.py` should take per-view prompts from a file
> under version control**, like the loop does. Filed, not fixed here — it is not this arm's
> variable.

## 5. What this does not settle

Whether ~40–53% reference coverage is *enough* for the Director to accept the asset is not a
question any of this answers. The defect-severity table is the closest evidence — the blade at
62% non-reference reads ΔE 23.17, the tunic at 1.2% non-reference reads 0.49 — and it suggests
severity falls with non-reference share rather than switching off at a threshold. Gate 1
remains his.
