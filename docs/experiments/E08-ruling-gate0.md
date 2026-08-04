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

> ### Amendment 7 (advisor, 2026-08-04) — the diagnosis is confirmed, and the residual is answerable by measurement rather than taste
>
> **Confirmed, decisively.** Control contour identical at **9,958 px on all four passes**,
> divergence 0.219% / 0.134% confined to the antialiased rim, and gross material relocation
> collapses about tenfold (>ΔE 25: 19.1% → **2.3%** front, 23.2% → **2.1%** back). The
> localiser is the clean part: **BG2-grey matches BG1-blue, not BG1-grey.** Pinning the control
> moved the baseline, so the cause was the control. The executor pre-registered that the grey
> baseline would move and regenerated both sides rather than comparing against the shipped
> twin — which is why this run can say that at all.
>
> Separation survives: min ΔE to the subject gamut **0.35 / 0.40** grey → **58.44 / 64.16**
> blue, both views agreeing. **The background arm's premise is intact.**
>
> ### I looked at the sheet, and it reframes the residual
>
> The executor was right that I had not seen these twins and right to hand it over. Having
> looked: **three of the four agree and the shipped twin is the odd one out — and it is also the
> visibly degraded one.** Its figure sits smaller in frame, its right hand is a smudge, its
> lower legs and boots are vague where the other three are legible.
>
> That is exactly what its control predicts. BG1-grey's control was built from a mask measured
> at **9.9% of frame against a 19.01% truth** — the keying failure A2 fixed on the projection
> side, still governing the generator. A control missing a quarter of the silhouette produces a
> twin painted small and soft. The other three had correct controls, by two independent routes.
>
> **So "the subject repaints" was the wrong frame, and it was mine.** There is no ground truth
> twin; the shipped one is not correct, merely first. The question is not whether BG2 differs
> from it but whether BG2 is a **better reference** — and this repo already established what
> makes one, with numbers.
>
> ### The measurement that decides it, and it is free
>
> **Registration.** E01 established it as load-bearing: silhouette IoU 0.290 → 0.777 was the
> fix, and carrying a mis-registered twin collapsed styled coverage from 62% to 22.7%. So:
>
> **For each of the four twins, report painted-figure fraction and IoU against the exact mesh
> silhouette (19.01%).** No GPU, no diffusion; the machinery exists — the shipped pair was
> already measured at twin 17.43% against mesh 19.01%, IoU 0.911.
>
> **Pre-registered reading, so it cannot be argued after the fact:**
>
> - **BG2 registers better → BG2 is adopted.** Better registration is a better reference by this
>   repo's own established criterion, and no taste is required to say so. The material
>   differences then go to the Director as a *separate* question about canon — gold knee plates
>   against fur wraps is a design call, not a blocker.
> - **BG2 registers worse → the arm dies** and the erosion's cost stands confirmed.
> - **No meaningful difference → it is genuinely the Director's eye**, and he gets the sheet with
>   the residual stated as what it is.
>
> ### One thing this raises that I want measured, not assumed
>
> BG1-grey's control carried **~23,000 px more** than BG2's. Some of that was spurious edges
> from mask holes — but a mask gradient also carries interior crease detail that a pure
> silhouette does not, and the shipped twin's boots match the prompt's "heavy dark boots" where
> the other three do not. **A second accidentally-load-bearing defect is possible here**, in the
> same shape as the erosion. The registration measurement bears on it directly: if the extra
> control was signal, the shipped twin should register *well* despite its broken mask. If it was
> noise, it will not.
>
> `figure_mask` is now retired from every path that governs anything — recorded, and it is the
> quiet result of this whole sequence.

> ### Amendment 8 (advisor, 2026-08-04) — the control is ADOPTED; blue is parked; my branches were mis-specified
>
> **My pre-registration was wrong in the way I had just written a rule against.** Amendment 7
> branched on "BG2" as if it were one thing. It was two — a geometry-derived control and a blue
> background — and *"one variable is a property of the dependency graph, not the parameter you
> edited"* is a rule I added two amendments earlier and then violated in the next
> pre-registration. The executor found the seam and split the result along it. That split is
> ratified and it is the reading that stands.
>
> **The geometry-derived control is ADOPTED.** Grey against grey isolates it — same background,
> same keying difficulty, control the only difference — and BG2-grey wins **5 of 6 cells**,
> with painted fraction closest to the 19.01% truth on both views (18.95 / 19.93 against the
> shipped twin's 17.38 / 17.01) and stability across all three tolerances. The pre-registered
> bar was "registers better → adopted." It does, on the axis that isolates it.
>
> **The extra control was noise, and that question is closed.** BG1-grey carried 3.4× the
> contour and registers *worse* on both views at every tolerance. Interior crease detail would
> have registered at least as well. No second accidentally-load-bearing defect — just a defect.
>
> **Blue is PARKED, not rejected, and the reason has teeth.** The executor refused to quote a
> number because IoU swings **0.61 → 0.92** on threshold alone, and declining to pick 20 because
> it reads well is the behaviour this repo exists to protect. But the limitation is the finding:
> the twin's **own painted mask** is the only remaining answer to *is the paint trustworthy* —
> geometry answers *is there surface*, and `figure_mask` is now retired from that duty — and a
> blue background makes that mask threshold-dependent. **An intervention that breaks an
> instrument the route requires cannot be judged until the instrument is replaced.**
>
> A hypothesis for whoever revives it, recorded and untested: a strongly coloured background
> produces coloured rim light *on the subject*, so the figure's own edge pixels go blue — which
> is the contamination we were removing, returning in a new form.
>
> ### The instrument failure is the most reusable thing here
>
> `figure_mask`'s corner-median key returned painted fractions of **31–76% against a 19.01%
> truth, with a 751 px bounding box in a 752 px frame.** Diffusion paints a lit studio gradient,
> not the flat field the heuristic assumes. **This is the third independent failure of that same
> construction** — A0's painted twin in E01, the grey-on-grey clay render in Arm A, and now the
> generator's own backdrop.
>
> **The fitted-background estimator is adopted as the standard keying**: a quadratic over a
> border ring, which reduces to the corner median on a flat background — which is why the
> shipped twin barely moves and every prior number stays comparable. With mesh-silhouette duty
> already retired to raycasting, the original heuristic is now gone from the pipeline entirely.
>
> **And the bbox sanity check becomes standard.** *A figure cannot be 751 px wide when the mesh
> is 388.* It is free, it tests the instrument's failure mode rather than its success mode, and
> it caught this before a single number was read into.
>
> ### Two consequences to carry forward
>
> **1. The new twins require the new keying.** BG2-grey twins carry diffusion-painted gradient
> backgrounds; the old corner-median key fails on exactly those. Adopting the twins without
> adopting the estimator in `project_twins` would reproduce this failure inside the projection
> stage. They ship together.
>
> **2. The shipped reference cannot be regenerated.** BG1-grey is built exactly as the shipped
> front twin was and does not reproduce it — 17.73 against 17.38%, IoU 0.9040 against 0.9088.
> That elevates the provenance defect filed in Amendment 6 from *inconvenient* to *load-bearing*:
> **every comparison against the shipped asset is a comparison against an artifact we cannot
> recreate.** It is a further argument for adopting BG2-grey's twins as the reference baseline
> going forward, since those are reproducible from a versioned recipe.
>
> ### Next, and it is free
>
> Re-run A2 with the BG2-grey twins and the fitted keying, and report reference coverage against
> A2's 39.1%. **Does a better-registered twin buy more surface?** No GPU, no diffusion — the
> twins exist. State the prediction first.
>
> The material differences — gold knee plates against fur wraps — belong to the *control* half
> and BG2-grey already carries them at the reference background. They go to the Director as a
> canon question when there is a finished asset to look at, not as a blocker now.

> ### Amendment 9 (advisor, 2026-08-04) — the acceptance lever is nearly exhausted; Arm B is re-authorised
>
> **The decomposition is the result, and it is clean.** The estimator alone moves **−0.1
> points**; the entire **+4.0** is the better-registered twin. That is the design working —
> a quadratic border fit reduces to a corner median on a flat field, so nothing prior loses
> comparability.
>
> **And it is the clearest case this repo has produced of a component that is necessary without
> being contributory.** Corner-median keying reads BG2-grey's gradient backdrop at **50.68% of
> frame** against a 19.01% truth, so without the estimator these twins are unusable. Measured in
> isolation it contributes nothing and would have been retired; measured as a precondition it
> enables everything. Recorded as a rule.
>
> **The acceptance lever is nearly spent.** My Gate 0 ruling put two cameras at perfect
> acceptance at 52.66% of valid. A2R is at 43.0% — **81.6% of what two cameras can physically
> reach**, up from 53.8% shipped. There is not much left on this axis.
>
> **So Arm B is re-authorised, and the forward arithmetic is now concrete rather than
> speculative:** eight cameras reach **74.10%** of valid; at A2R's 81.6% acceptance that is
> **~60.5% reference coverage**, against the rejected asset's 28.4%. **A 2.1× change in the
> provenance mix** — which is the thesis, and the first number in this line large enough to
> justify a loop run.
>
> ### Two things gate adoption, and both are free
>
> **1. Characterise the 54,978 lost.** A2 was strictly additive; A2R is not — 148,693 gained
> against 54,978 lost, net +93,715. The executor flagged it rather than burying it under the
> net, which is right, and the net is not the question. **A swap is a win only if what arrived
> is at least as trustworthy as what left**, and nothing yet measures the departed set. Locate
> it: which regions, and were those texels good reference or marginal? Different twin masks
> produce different edge-distance fields, so the loss is probably at boundaries and thin
> structure — which is where the blade lives, and that would matter.
>
> **2. Locate the 2.03%, do not threshold it.** Newly-styled texels sit at 2.03% within ΔE 10
> of background against 0.26–0.28% for the trusted set — about 7× enriched, roughly **3,020
> texels**, 0.29% of the final styled set. **Refusing to pick a threshold after seeing 2.03%
> was correct** and the 2.0% erosion limit belongs to a different population; borrowing it would
> be the seventh mis-specified condition. The answer is not a number, it is a location: if those
> 3,020 sit on the blade or the face it matters, and if they are scattered along the silhouette
> it does not. Same instrument, same cost.
>
> **The guards are ratified.** `reachable` holding at 1,265,391 *exactly* is the right control —
> it takes no twin input, so any movement would have voided the comparison. And the bbox andon
> reading 936×751 on a broken key is the check earning its place a second time.
>
> ### Before Arm B spends GPU, the Director sees the twins
>
> He has not seen them, the executor keeps saying so, and it is the right flag. **Gold knee
> plates against fur wraps is a canon call he can make in seconds, and it gates real spend** —
> if the new reference is wrong for the character, eight restylize passes and a loop run are
> wasted on it.
>
> Put the four-panel twin sheet in front of him framed as **one question about the character,
> not a quality gate**: this is the reference the route will carry, does it read as the man he
> designed. The finished-asset judgement stays where it belongs, at Gate 1.

> ### Amendment 10 (advisor, 2026-08-04) — Director: the shipped twin is the character. My framing is withdrawn.
>
> **Ratified in full.** A2R is off-canon; the geometry-derived control is withdrawn as a
> *twin-generation* path. A2 stands — it never touched the twins, only replaced the projection
> stage's keyed clay mask with the exact mesh silhouette, so it is canon-safe by construction.
> The fitted estimator and the bbox andon stay as no-ops that catch a failure which has now
> happened three times.
>
> **Amendment 7 is falsified, and the falsified line is mine:** *"better registration is a
> better reference by this repo's own established criterion, and no taste is required to say
> so."* It is not a better reference. It is a different man.
>
> **Worse, I had already written the correct rule and then talked myself out of it.** Amendment
> 4's halt said *an arm that improves keying by changing the reference has broken the thing it
> was protecting.* Three amendments later I reframed that same result as a registration
> question — because a measurement was available and I preferred having a number to asking the
> only party who can answer.
>
> **The failure mode has a name and this is its second appearance in two experiments.**
> E07 graded material identity with high-pass statistics; E08 graded character identity with
> IoU. Both times the real question was *is this the right thing* and both times I substituted
> a measurable proxy that was orthogonal to it. **Canon is not a taste question to be avoided —
> it is a ground truth held by the Director, and it is not approximable by a metric.**
>
> ### The architectural correction: a twin is two things, and we only ever modelled one
>
> E01 established *twins belong to a mesh, not to a character* — regenerate them for whatever
> you are about to texture. That is **true for registration and false for identity.** A twin is
> simultaneously:
>
> - a **mesh-bound projection source**, which must match this silhouette, and
> - a **canon identity reference**, which must be this man.
>
> Those were never separated, which is how "regenerate the twins" became a routine step and how
> a registration improvement could quietly replace the character. Every future twin operation
> must state which of the two it is touching.
>
> ### The canon twin's irreproducibility is now the repo's highest-priority defect
>
> The executor is right to flag it hardest. **The asset the whole route exists to carry is a
> file we can copy and cannot recreate** — built identically it does not reproduce (IoU 0.9040
> against 0.9088), and its parameters are not in the repo. That was an inconvenience while it
> was one candidate among several. It is now the canon.
>
> **Ruled: stop treating it as derivable.** Freeze the twin pair as a **canon artifact**,
> version it, and record its provenance as *incomplete* rather than implied — a recipe that
> does not reproduce its output is not a recipe. Do not spend a seed sweep trying to recover
> it: even a match could not be verified as *the* recipe, and the artifact is already in hand.
> `restylize_views.py` still needs per-view prompts from a versioned file so this cannot recur
> for the next character, and that is now a prerequisite rather than a filed nicety.
>
> ### Arm B is re-scoped, not cancelled
>
> It still holds the largest available change — ~55% coverage against 28.4% on A2's canon-safe
> acceptance rate — and it still requires six new twins through a path that has now
> demonstrated it can move the character. There is no metric that gates that, because the thing
> being gated is canon.
>
> **So the Director gates them, one sheet, at full size, accept or reject per twin. Only
> accepted twins project.** That is cheap in his time — he ruled within one exchange of seeing
> these at full size — and it is the only ground truth available. It also fixes the process
> failure the executor named: these were shown as downscaled contact-sheet columns, against
> this repo's own rule about judging at the Director's zoom.
>
> ### Authorised, cheap, and never tried: name the armour
>
> The executor's observation is the best lead on the table. **The gold knee plates are not in
> the prompt** — they came through from the mesh's own knee armour, via the control. So the
> shipped twin's surplus 23,000 px of contour was **noise for registration and signal for
> identity**, which are different properties I conflated in Amendment 8 when I called it "just
> a defect."
>
> Asking for the armour explicitly pins it regardless of control strength, has never been
> tried, and costs one twin. If it works, the identity/registration tension partly dissolves —
> canon comes from the prompt where it can be stated, and the control is free to be clean.
>
> ### Held, correctly
>
> The 54,978-lost and 2.03% location measurements are held. Both were about A2R and A2R is
> withdrawn. Do not run them.

> ### Amendment 11 (advisor, 2026-08-04) — canon is prompt-expressible, and that changes what the ruling implies
>
> **All three ratified.** The freeze, the provenance mechanism, and the armour test. The
> `.gitignore` exception is principled in the repo's own terms — its stated premise is "assets
> are large and regenerable," and *regenerable* is measured false for exactly those two files.
> The sidecar is the first provenance artifact this pipeline has ever produced.
>
> **The armour result is the best single finding of this session.** One phrase, control
> byte-matched at 20,973 px so the term was the only difference, and the plates returned
> correctly placed with the clean control's legibility intact. **It splits Amendment 8 exactly:
> the surplus 23,000 px was noise for registration and signal for identity** — and the signal
> is recoverable by other means. Canon can be stated in the prompt; the control is free to be
> clean; **registration and character are not mutually exclusive.**
>
> **The executor's self-catch is worth more than the predictions were.** They argued the term
> would fail because "heavy dark boots" was in the prompt and had been overridden — then
> checked and found the boots are dark in *every* arm and were never overridden. **An invented
> precedent, reasoned from as if measured.** That is the same failure as an inherited claim,
> except self-inflicted within a single turn, and catching it before reporting is the behaviour
> that makes this record trustworthy.
>
> ### Authorised: the bracer, same one-term fix
>
> Canon has a gold-trimmed leather bracer; both clean-control arms have a fur cuff; the front
> prompt never names bracers though the palette spine does. Cheap, untried, and it is the
> **second data point on whether canon is prompt-expressible in general** rather than lucky once.
>
> ### The proportion question is not a taste call, and it goes to the Director with new evidence
>
> Looking at the canon twin and the armour twin at full size: the difference is larger than
> "stockier." The canon figure reads taller and narrower, with longer legs and a smaller head
> against the body; the armour twin reads short-limbed and broad. Measured, the canon twin
> paints **17.38%** of frame against a mesh silhouette of **19.01%**, where the clean-control
> twins paint 18.95%.
>
> **The load-bearing point: the proportions came from the same defect as the missing knee
> plates.** The canon twin's control was missing a quarter of the silhouette, so the model
> painted freely — and what it painted free of was the mesh's own body. One consequence of that
> defect has just been shown to be a prompt-fixable artifact. Whether the other is, is his call
> and nobody else's, but he should make it knowing the two share a cause.
>
> Three readings, and they lead to different work:
>
> 1. **The proportions are canon.** Then the mesh is not the character's body, and that is a
>    **geometry** finding — reconstruction or E03's head graft — not a texture one. It would
>    reorder the queue.
> 2. **The proportions were the artifact.** Then the armour twin plus a bracer term is the
>    character rendered correctly on the correct body, and the canon PNG becomes a
>    **specification** rather than the reference.
> 3. **Neither cleanly** — he wants something the current route does not produce, which is worth
>    knowing before Arm B generates six more.
>
> **Reading 2 would also dissolve the irreproducibility defect**, which is why it is worth
> putting to him rather than assuming. A specification is reproducible where an artifact is not,
> and Amendment 10's "a twin is two things" tension collapses: identity moves to the prompt, and
> the twin only has to do the registration job. That is now a live hypothesis with one
> confirmation, not a wish.
>
> **Arm B waits on his answer.** Generating six twins is the wrong move while it is unsettled
> which body they should have.

> ### Amendment 12 (Director, 2026-08-04) — the proportions were the artifact. Identity moves to the prompt.
>
> **Ruled: use the mesh's body.** The taller, narrower figure was the model painting free of a
> control missing a quarter of the silhouette — the same defect that lost the knee plates, and
> the plates have already been shown to be prompt-recoverable.
>
> **This resolves the architecture, and it vindicates E01 rather than amending it.** E01's rule
> — *twins belong to a mesh, not to a character; regenerate them for whatever you are about to
> texture* — was right all along. Amendment 10 called it "false for identity"; the correct
> statement is that **identity was never the twin's job to carry.** The complete rule:
>
> > **Twins belong to a mesh. Identity belongs to the prompt.**
>
> The tension I named in Amendment 10 does not need resolving — it dissolves. A twin has one
> job: register to the mesh it will be projected onto. Everything that makes the man *this man*
> is a named element in a versioned prompt.
>
> **And the highest-priority defect dissolves with it.** The canon twin's irreproducibility was
> load-bearing only while the artifact *was* the reference. As a **specification source** it does
> not need to be regenerable — a specification reproduces where an artifact does not. It stays
> frozen and versioned, its role changed rather than its status: **the visual target the spec is
> read off, and no longer the projection reference.** `canon/MANIFEST.md` must record that
> change; it currently describes the file's provenance, not its demotion.
>
> ### Sequence, and the middle step is a gate rather than a formality
>
> **1. Extract the specification.** Enumerate the delta between what the prompt already names —
> green tunic, gold pauldrons, gold necklace, red beard, dark red skirt, leather belt, heavy
> dark boots — and what the canon twin actually shows. Two are known: **gold knee plates**
> (proven) and the **gold-trimmed leather bracer** (authorised, not yet run). Propose the rest;
> the Director ratifies the list, because it is canon.
>
> **2. Verify the specification reproduces — this is the gate.** Generate a twin from the full
> spec on a clean control and check **every named element is present**. Reading 2's entire claim
> is that a specification is reproducible where an artifact is not, and it is untested at more
> than one term. **If the spec does not reproduce its own elements, this ruling's premise fails
> and the artifact reading comes back.** Halt and report rather than adding terms until it
> passes — a spec tuned until it works is not a spec.
>
> **3. Then Arm B.** Six further views, each carrying the ratified spec, each gated by the
> Director at full size per Amendment 10. Not before step 2 clears.
>
> **The bracer test is now step 1's second data point rather than a curiosity** — it is the
> evidence that prompt-expressible canon generalises past one lucky term.

> ### Amendment 13 (advisor, 2026-08-04) — the split is a grammar finding, not a failed premise
>
> **The premise is not falsified.** The element *appeared* — fur became smooth segmented
> leather, decisively, with the control byte-matched and nothing else drifting. What failed is
> **modifier fidelity inside a compound noun phrase**: the head noun landed and the compound
> adjective did not.
>
> Look at the two results together:
>
> | term | shape | outcome |
> |---|---|---|
> | "gold knee plates" | head noun with **one** modifier | **landed in full** |
> | "gold-trimmed brown leather bracers" | head noun with a **stacked compound** modifier | head noun landed, modifier dropped |
>
> That is not "specifications are unreliable." It is a constraint on **how a specification must
> be written**, and if it holds it is worth far more than the bracer — it governs every term in
> the spec and every character after this one.
>
> **Refusing to tune was right and the distinction matters.** Adding "gold bracer plate" and
> re-rolling until it appears is fitting the spec to the outcome. Stating a hypothesis and
> testing it once is not. The hypothesis, derived from the table above rather than from the
> outcome:
>
> > **An element expressed as its own head noun lands. An element expressed as a modifier on
> > another noun is unreliable.**
>
> **Authorised: one test, one prediction, no iteration.** Promote the trim to its own noun
> phrase — a gold plate on the outer forearm as an element, not an adjective on bracers — and
> record the prediction before looking. **Stopping rule: if the promoted phrase also drops it,
> the premise is weaker than Amendment 12 assumed, Arm B waits, and the artifact reading comes
> back onto the table.** One roll either way; do not vary the wording a second time.
>
> ### The spec needs three categories, not one list
>
> D3 exposes it: fur trim edging the knee plates, which **the new twins produce unprompted**. A
> single "named elements" list has nowhere to put that, and the rule *a canon element not named
> in the prompt is arriving by accident* would wrongly condemn it. Something appearing
> consistently across arms without a term is not arriving by accident — it is arriving from the
> **mesh** through the control, or from the **style LoRA**. Those are stable sources; a text term
> is not required, but the dependency must be recorded or a future change to either silently
> removes it.
>
> - **NAMED** — must appear in the prompt; absent it, it leaves.
> - **MESH-SUPPLIED** — arrives through the control from geometry; record it so a mesh change is
>   noticed.
> - **STYLE-SUPPLIED** — arrives from the LoRA; record it so a model change is noticed.
>
> **The knee plates are the cautionary case for this taxonomy**: they *looked* mesh-supplied —
> they came from the mesh's own knee armour — and were lost the moment the control was cleaned.
> Arriving from the mesh through a **noisy** control is not the same as arriving from the mesh.
> Default to NAMED; require evidence across at least two clean-control arms before filing
> anything as supplied.
>
> ### The necklace observation is the sharpest thing in the report
>
> The prompt says "gold necklace"; there is no necklace at the throat in canon; there is a gold
> belt medallion. **A term in the prompt is misnaming a canon element, and the element survives
> by accident** — which is precisely the pattern Amendment 12's rule exists to kill, found by the
> executor one step after the rule was written. Correcting it is not optional polish; it is the
> same class as the knee plates.
>
> ### Corroboration, offered as observation and not as a canon ruling
>
> I have looked at the canon twin at full size. Present in the image: the **gold belt medallion**,
> an **ornate gold crossguard and pommel**, a **green skirt layer** beside the wine-red panel,
> and **scrollwork on the pauldrons**. I see **no necklace at the throat**. Presence is
> observable and I can report it; whether each is *canon* is the Director's, and that question
> goes to him now.
>
> **The MANIFEST demotion is ratified**, including the standing line not to project from the
> canon pair — under-filling the silhouette at 17.38% / 17.01% against 19.01% while showing a
> body that is not the mesh's is exactly why.

> ### Amendment 14 (Director, 2026-08-04) — W3 is a test character. Stop gating on its canon.
>
> **"This is a test character, so there is no canon. You should either make canon or stop gating
> so much on a test character. Probably should make canon."** And: *"we need to focus on making
> the pipeline for future sprites."*
>
> **The frame error is mine and it is the same one he raised earlier in the session.** I spent
> his attention on which armour a test dwarf wears — three questions across two turns — when the
> product is the pipeline and W3 is a fixture. Asking a Director to ratify canon that does not
> exist is not caution; it is offloading a decision I should have made.
>
> **Canon is made, by the advisor, and it is written down:**
> [canon/W3-IDENTITY.md](../../canon/W3-IDENTITY.md). Sixteen NAMED elements in the three
> categories of Amendment 13, every one written as its own head noun so the spec is itself the
> test of the grammar constraint. Any line is his to overrule in a sentence; none needs his
> ratification to proceed.
>
> **The necklace call was left to me and is decided: the medallion is the element, the necklace
> term goes.** A term that misnames an element and produces the right thing by accident is
> exactly what the identity-in-the-prompt rule exists to kill.
>
> ### The gating rule, restated
>
> **The Director gates outcomes. The advisor authors fixtures.** For a test subject, canon is a
> *test fixture* — it exists so "did the element land" has a ground truth, not because the
> warrior matters — and authoring it is advisor work. His attention goes to: **does the mechanism
> work, and is the finished asset better.** Amendment 10's "he gates each twin" stands for a
> *shipping* character and is withdrawn for this one.
>
> **What actually transfers to future sprites** — the product, and the reason this line was worth
> running: identity lives in the prompt, not the twin · elements must be head nouns · the twin's
> only job is registration · surface comes from the raycast silhouette, never a keyed render ·
> background estimation is a fitted border ring, never a corner median · every generation writes
> a provenance sidecar · a recipe that does not reproduce its output is not a recipe. None of
> that is about a dwarf.
>
> ### Next, and nothing here needs him
>
> 1. **N11** — the promoted forearm plate. One roll, prediction recorded, stopping rule stated.
> 2. **The full-spec reproduction gate** — generate from N1–N16 on a clean control; every element
>    present or halt. **A spec tuned until it passes is not a spec.**
> 3. **Arm B** — eight views carrying the spec, drift measured against it rather than argued.

> ### Amendment 15 (advisor, 2026-08-04) — the halt stands; co-location beats my grammar hypothesis
>
> **N11 dropped, the stopping rule fires, and I am not rerolling it.** The grammar hypothesis
> was mine and it is not what is doing the work.
>
> **The sharper measurement is that the model did not respond at all** — median ΔE **1.07** over
> the whole figure, 1.15 on the forearm. Not a wrong element, not a mis-bound attribute: no
> perturbation. Grammar failure predicts *something* moves. Nothing moved. That is evidence
> against my hypothesis and for the executor's.
>
> | element | form | result |
> |---|---|---|
> | gold knee plates | head noun, **replaces** what occupied the surface | landed |
> | brown leather bracers | head noun, **replaces** what occupied the surface | landed |
> | gold trim on the bracer | modifier, **co-located** | dropped |
> | a gold plate on each outer forearm | own head noun, **co-located** | dropped |
>
> **Both grammatical forms land when they replace and drop when they add.** Co-location is the
> better axis, and the executor recorded the pattern *before* the roll rather than after.
>
> ### What "weaker premise" actually means now — and it is not what the stopping rule assumed
>
> Amendment 12 assumed any element could be stated and obtained. That is false, so the stopping
> rule's condition is met and the halt is honoured. But the reason it mattered has changed under
> the Director's Amendment 14 ruling, and the corrected premise is narrower rather than broken:
>
> > **A specification determines what occupies each surface. It cannot add a second element to a
> > surface already occupied.**
>
> **N11 failed because we were patching, and a new sprite is not patched.** Retrofitting a gold
> plate onto a fur cuff that the model has already committed is a different operation from
> specifying a character from scratch, where every element occupies its own surface by
> construction. The pipeline's actual use case is the second one. **So the premise is intact for
> what it is for, and the failure mode is specific to retrofit** — which is itself a pipeline
> finding worth having: *specify from scratch, never patch.*
>
> ### Step 2 is not a reroll, and it is now a sharp test
>
> The full-spec generation was already the gate and it is a *different* operation from N11 — all
> sixteen elements specified simultaneously, nothing added to anything. The executor's reason for
> isolating N11 first has been served, so it is clean to run.
>
> **And the spec has three co-location cases built into it**, which makes it discriminating
> rather than merely confirmatory. Pre-registered:
>
> - **N5** gold scrollwork *on the pauldrons*, **N9** green panels *in the skirt*, **N11** a gold
>   plate *on each outer forearm* — all additions to occupied surfaces. **Predicted to drop.**
> - The remaining thirteen occupy their own surfaces. **Predicted to land.**
>
> **If that pattern holds, co-location is confirmed and is a real, statable pipeline constraint.
> If N5 and N9 land while N11 drops, co-location is wrong too and something narrower is going
> on.** Either result is worth the one generation it costs. Halt and report; **a spec tuned until
> it passes is still not a spec.**
>
> **Arm B stays waiting** on step 2, as sequenced — not on N11.
>
> ### The instrument the executor threw away
>
> A gold-pixel count over the forearm crop caught the pauldron edge and read 5.6% / 5.1% against
> canon's 1.96% — **inverting the truth**, and it would have flattered the reading. It was
> reported as unusable rather than quoted. That is the third self-caught bad instrument in this
> session, after the vacuous dilation check and the invented precedent, and it is the habit that
> makes the rest of the record worth trusting.

> ### Amendment 16 (advisor, 2026-08-04) — my step-2 gate has a denominator of one
>
> **Caught before the number existed, which is what I asked for.** 14–15 of the 16 NAMED
> elements already arrive **unprompted** — the belt medallion, the green skirt panels, the
> ornate crossguard and the gold pommel are all present in an image whose prompt named none of
> them. So "15/16 landed" cannot separate *the specification works* from *the LoRA, mesh and
> control already produce this character.* **The honest unit is: of the elements that were
> absent, how many arrived? — and that denominator is one, possibly two.**
>
> Step 2 still runs, because it tests two real things — regression across sixteen simultaneous
> elements, and N11 under simultaneous specification — but **it is not the specification gate I
> claimed it was**, and its limits go in the report rather than being discovered later.
>
> **N5 is the discriminator and the executor has the sign right:** if scrollwork appears where it
> was absent, that **falsifies** co-location rather than confirming it.
>
> ### The test with a real denominator — and it is the pipeline question
>
> If 14–15 of 16 elements arrive without being named, the question is not *does naming work*. It
> is **does naming matter at all** — and for a future sprite that is not this dwarf, whether the
> LoRA, mesh and control will supply *this dwarf's* attributes regardless of what the prompt
> says. That is the difference between a pipeline and a dwarf generator.
>
> **The contradiction test.** Name an element that **conflicts** with one arriving unprompted —
> *silver pauldrons* where gold arrive unbidden, a *black* skirt where wine-red arrives — and
> measure whether the prompt overrides the supplied attribute.
>
> - **The prompt wins →** identity is in the prompt, Amendment 12's architecture holds, and the
>   route generalises to other characters.
> - **The supplied attribute wins →** identity is in the LoRA and the mesh for those elements,
>   the specification is decorative for them, and **the pipeline produces this dwarf in different
>   clothes.** That would be the most important negative result in this repo, and it is cheap.
>
> Denominator equals however many elements are contradicted, by construction. **This outranks
> Arm B**, which is eight expensive views of a question this answers for one.
>
> ### The blocker
>
> `CLAUDE.md`'s rule is *cap the consumer; never raise the ceiling*, and the executor was right
> that the ceiling is not theirs to move — but it read the rule too narrowly. The launch flags
> are one way to cap a consumer, not the only one, and reducing what a job stages is squarely
> the sanctioned direction. **The ceiling stays at 31,200 MiB. Nothing about it is negotiable.**
>
> Order: try once on a **settled** instance first — the executor's own diagnosis is that the four
> passes that succeeded today ran warm, and the failures competed with ComfyUI-Manager's
> 167-item registry fetch. If it recurs, the rig has a **verified local knowledge base** for
> exactly this (`E:\AI\readouts\model-knowledge\catalog\comfy.md`); consult it rather than
> guessing at flags. One hypothesis worth testing there and **not acting on blind**:
> `--disable-smart-memory` prevents ComfyUI unloading between nodes, so the 7,910 MB text
> encoder may stay resident through sampling when it is no longer needed — which would make the
> cap itself part of the 31 GB.

> ### Amendment 17 (advisor, 2026-08-04) — both environment hypotheses are dead, and the reboot is a confound
>
> The executor ran the ordered protocol and **falsified every hypothesis in it, including both of
> mine.** Recorded here because the diagnosis is now the useful part, not the guesses.
>
> - **Settled instance — falsified.** ComfyUI relaunched, registry fetch fully drained 167/167
>   before a prompt was submitted. The job died at **6/20**, the same point as the three prior
>   attempts. The ComfyUI-Manager fetch was never the cause.
> - **`--disable-smart-memory` — falsified.** Relaunched without it: same place, same phase, same
>   height (31,703 MiB @ 47.6 W against 31,654 @ 54.5 W). The log shows `QwenImageTEModel_ 7910MB
>   Staged` followed straight by `Requested to load QwenImageControlNetModel` **with no unload in
>   between, either way.** My hypothesis and the executor's independent agreement with it were
>   both wrong, and it cost one generation to find out — which is the right price.
>
> **The measurement that replaced them.** Subtract the desktop baseline from each peak and
> ComfyUI's own working set was **24,225** and **24,673 MiB**, against a reserve-derived budget of
> 32,607 − 8,192 = **24,415**. Both runs sat on their budget to within allocator noise.
> `--reserve-vram` was doing exactly what it says — **and that is the problem: it reserves against
> the card's total, not against what is left after the desktop.** The desktop's own 7.0–7.6 GB
> lives *inside* the 8 GB reserve, and the ceiling sits 1,407 MiB below the card total. The breach
> happened at 47–54 W, inside model load, before compute started; compute added ~175 MiB. By the
> rig's own diagnostic that is a **reserve** problem, not a workload-size one.
>
> **`CLAUDE.md`'s launch line is wrong on both halves, and I wrote it.** *"Launch ComfyUI capped:
> `--reserve-vram 8.0 --disable-smart-memory`"* — the flag works *against* the reserve it sits
> beside, since evicting the text encoder is the mechanism `--reserve-vram` depends on; and 8.0 is
> under the line the ceiling requires. The rig's own sanctioned launcher,
> `E:\AI\training\_comfyui_start.ps1`, never passed `--disable-smart-memory` and says so in its
> header. **An inherited claim is a hypothesis wearing a fact's clothes — including one the
> advisor wrote into the standing constraints.** I am not correcting the line to a number yet: E3
> has not run, and writing "10.0" before it is measured would be inventing the replacement.
>
> ### The reboot is a confound, and it points the wrong way
>
> The Director restarted the machine. **The desktop baseline was 7,030–7,604 MiB across the two
> measured failures; it is now 1,150 MiB.** That is ~6.5 GB of headroom that appeared for a reason
> having nothing to do with the fix.
>
> At the current baseline, reserve **8.0** would complete — 24,415 + 1,150 = 25,565, some 5.6 GB
> clear of the ceiling. **So a run at the old setting would now pass, and the pass would mean
> nothing.** It would be credited to a flag change already measured not to work, it would quietly
> become doctrine, and the next run on a warm desktop would fail exactly as before. This is *"one
> variable is a property of the dependency graph, not of the parameter you edited"* arriving from
> outside the experiment entirely.
>
> **Two rulings, both fixed before any number exists:**
>
> 1. **E3 runs at `--reserve-vram 10.0` as pre-registered** — not at 8.0, and not at whatever the
>    fresh baseline would now tolerate. The reserve is sized against the **worst observed baseline
>    (7.6 GB)**, because a setting that only holds on a just-rebooted machine is not a setting.
>    10.0 gives 22,367 + 7,600 = 29,967, still 1.2 GB under the ceiling. E4's cost — streaming from
>    system RAM, slower — is accepted; RAM is at ~31% of 64 GB.
> 2. **Record `nvidia-smi` used-MiB at the moment of launch, in the report.** Every prior
>    environment number in this line is un-attributable without it, which is how a 6.5 GB swing
>    went unnoticed until someone looked for it. It costs one line and it makes the next failure
>    diagnosable.
>
> **E2 stands as the halt condition, and the reboot raises its value rather than lowering it.**
> The anchor must return sha256
> `d0220e244d5ad2015639153188c488e3f3d317933dbd54eb439724fe1f57f93d`. The executor flagged that
> proceeding on a non-reproducing anchor would be an advisor call, so here it is in advance: **do
> not proceed. Halt and report.** Every prior number in this line was taken on the old machine
> state; if the anchor does not reproduce, SPEC and CONTRA are not comparable to BRACER, ARMOUR or
> N11, and no amount of contradiction data is worth measuring against a machine that is not the
> one the baselines came from.

> ### Amendment 18 (advisor, 2026-08-04) — the job does not fit, and local was never the default
>
> **The diagnosis, from E3.** The staged set is 7,910 + 19,483 + 3,372 + 241 = **31,006 MiB**
> against a watchdog ceiling of **31,200 MiB** on a **32,607 MiB** card. Run 3's working set was
> **30,809 MiB** — within ~200 MiB of everything resident at once. **There is no room left for
> activations. This job cannot fit under the ceiling on this card, at these model sizes, at any
> reserve.** It is not a tuning problem and the executor was right to stop walking the lever.
>
> **And the reserve flag is not binding.** Peak was 31.7–32.0 GB across all three runs —
> independent of the reserve *and* of the baseline. Runs 1 and 2 only looked bounded because the
> desktop held ~7 GB, so ~24 GB was all the card had left. **ComfyUI stages to fill what it
> sees**: the reboot freed 6.5 GB and the working set grew 6.1 GB. That inverts the intuition —
> the earlier passes succeeded *because* less VRAM was free.
>
> **Ruled: move to Comfy Cloud, and record that this was the studio's standing default all
> along.** The `comfy-local` skill states it plainly — *local is the fallback; the studio default
> for image generation is Comfy Cloud (RTX 6000 Pro, 96 GB)*. A session was spent fighting a
> constraint we had already decided not to accept. **That is an advisor error of omission** and
> it belongs in the ledger with the other six: I treated the local rig as the environment
> instead of checking what the environment was supposed to be.
>
> ### Two things gate the move, and neither is optional
>
> **1. The first cloud run is an anchor reproduction, not the contradiction test.** Every number
> in this line rests on byte-matched controls and reproducible anchors — that is what makes the
> A2 / N11 / BG2 comparisons mean anything. Memory records Comfy Cloud as *seed-identical to the
> local 5090*, **validated 2026-06-26** — roughly forty days old, which the freshness rule makes
> advisory until re-measured. So: **re-run N11's twin on cloud from its sidecar** (every
> parameter is recorded, the control is byte-matched at 20,973 px) and compare against the local
> output.
>
> - **Reproduces** → the anchor holds, every prior arm stays comparable, and the whole line
>   continues on cloud with 96 GB of headroom.
> - **Does not reproduce** → we have found the comparison boundary before it silently invalidated
>   an arm, and we decide explicitly what remains comparable. That is a result, not a setback.
>
> **2. Check the LoRA delivery path before anything else.** `saltroad_style_v2_lowlr_000001500`
> is a local file. Memory records the cloud bridge's LoRA delivery as **HF-URL-only**, though the
> plugin now exposes `upload_file`. **If the LoRA cannot reach the cloud, none of this runs
> there** — that is a hard blocker and it costs one call to establish. Check it first.
>
> **The ceiling stays at 31,200 MiB regardless.** Nothing here changes it; the point is that we
> stop asking a 32 GB card to hold a 31 GB working set.

> ### Amendment 19 (advisor, 2026-08-04) — Step 0a rulings
>
> **My `upload_file` line was wrong.** Amendment 18 offered it as a possible LoRA path; its
> schema is `.jpg/.jpeg/.png/.webp/.gif` only. There is no API import endpoint, so **the import
> is browser-only however the file reaches HF.** Corrected in place; the executor established it
> rather than inheriting my claim, which is the pattern.
>
> **Keep the LoRA repo private — endorsed, and the reasoning is right.** It is the studio's
> trained visual style, and "public" on HF is not reversible in any meaningful sense once a
> weight file has been fetched. A read token scoped to one private repo is the cheaper risk by a
> wide margin. **Do not make it public to avoid a UI step.**
>
> **Validating the graph before asking for a manual step was the right order.** A free `dry_run`
> returning `validated` — every node class present, links sound, all four base models resolving
> by exact name — means the import is the last unknown rather than the first of several. That
> ordering is worth keeping as a habit for any cloud move.
>
> **The stale memory line is a live-verification win.** `comfy-cloud-run.md` records
> `Qwen-Image-InstantX-ControlNet-Union.safetensors` as still needing an import; it is already
> present on cloud by exact name. The entry is ~40 days old and the freshness rule called it
> correctly. **Flagged for correction in the studio memory store, not corrected mid-experiment**
> — that store has its own index ritual and this is not the session to run it.
>
> ### The upload-naming ambiguity — one free check, if a path exists
>
> The executor was right not to chase it and right to record it: neither returned name matches
> its file's SHA-256, so either the cloud hashes something other than content, **or it
> re-encodes the image — and a re-encode changes the latent, making byte-reproduction impossible
> by construction rather than by drift.**
>
> Those two have very different consequences for reading 0b, and they are separable for free
> **if** the uploaded input can be fetched back: round-trip the render and compare its SHA-256
> to the original. Identical → no re-encode, and a sha mismatch at 0b would be genuine
> hardware drift. Different → re-encode confirmed, byte-reproduction was never available, and
> **0b's ΔE ≤ 1.07 branch becomes the expected path rather than the fallback.**
>
> **If no download path exists, do not build one.** 0b's gate already adjudicates the outcome on
> ΔE against N11's own measured no-response floor; this check only removes an ambiguity about
> *why*, and the ruling does not depend on it.

> ### Amendment 20 (advisor, 2026-08-04) — drive it. This was my call and I let it reach the Director.
>
> **Yes. Take the browser.** The executor's proposed protocol already satisfies the standing rule
> from the earlier Comfy incident — *new empty tabs only, never rewire a graph you did not
> create* — because it opens a **new empty workflow** before clicking Use, so the `LoraLoader`
> drops into nothing. Rule satisfied by construction, not by care. Nothing about this needed the
> Director.
>
> **Run the round-trip in the same authenticated session.** `GET /api/view?filename=…&type=input`
> is the documented endpoint; it answers the re-encode question for free while someone is already
> logged in, and it decides whether 0b's ΔE branch is the expected path or the fallback.
>
> **Do not ask anyone to verify the token first.** Attempt the import. If the token cannot read
> `mikeyfrilot/saltroad-lora`, it fails at download and *that is the measurement* — a distinct
> failure mode from a bad URL, and cheaper to observe than to confirm in advance.
>
> **Halt conditions unchanged:** report deviations at the top, stop on anything unexpected rather
> than clicking through it, and read the **actual** `lora_name` off the node rather than the
> predicted one.
>
> **The pattern, owned:** the Director has now twice had a decision reach him that was mine —
> canon for a test character, and this. Re-checking the browser-only claim before acting on it
> was exactly right, and asking me was reasonable; **the failure was me not answering.** Standing
> correction: when an executor proposes a protocol that already satisfies the governing rule,
> the advisor rules on it and the work proceeds.
> ### Amendment 21 (advisor, 2026-08-04) — 0b passes, and the shape of the residual is what earns it
>
> **Branch 2 fires and the Director accepts. The line continues on cloud, boundary recorded.**
>
> **But the number clearing the bar is the weaker half of the evidence.** ΔE 0.84 against 1.07 is
> a pass; what makes it *the same asset* is the structure of the residual: held controls 0.71
> against contradicted regions 0.98 — **everything moving together** — with the largest single
> region (1.79) being the 340 px medallion, the smallest and noisiest box. Gold holds at chroma
> 40 / hue 80, beard red, tunic green, blade neutral steel.
>
> **Uniform sub-unit drift across every structure is what two float kernels look like. A
> structural difference concentrates.** A future run could clear 1.07 with a residual piled into
> one region and that would *not* be the same asset — the threshold would pass and the reading
> would be wrong. **Standing method from here: when a threshold passes, check whether the
> residual is uniform or concentrated before accepting what it means.** The executor did this
> unprompted; it is now required rather than admirable.
>
> The LoRA loading is the load-bearing confirmation, because it was the first suspect had ΔE
> gone past the floor. Gold at chroma 40 is the style landing, not a coincidence of hue.
>
> ### My error underneath the executor's
>
> The executor did not check the Model Library for an existing copy before building an HF
> delivery path — a repo, an upload, a browser import, all redundant. **That check was missing
> because I specified the wrong one.** Amendment 18 said *check the LoRA delivery path first — if
> the LoRA cannot reach the cloud, nothing runs there.* The first question is not *can it get
> there*; it is **is it already there.** I specified a check whose shape assumed its answer,
> which is the same failure as the registration criterion and the step-2 denominator.
>
> **Standing correction: before building a path to a resource, enumerate the resource.**
>
> ### Worth keeping
>
> Both submits warned that `lora_name` "was not found in the bundled node index" and ran
> correctly anyway — the MCP's catalog lags the cloud, and that warning is not a missing model.
> The Comfy agent's hard UI rejection against a stale 643-option list was **the same staleness in
> a worse failure mode**. A stale index that warns is survivable; a stale index that blocks is
> not.
> ### Amendment 22 (advisor, 2026-08-04) — the prompt wins 8/8. The architecture is confirmed with a real denominator.
>
> **Ratified.** Whole figure ΔE **17.09** against a 1.07 no-response floor; contra median
> **46.28** against held **6.23**, a **7.4×** separation with an internal control. Amendment 12's
> division was a ruling on one Director judgement plus one term. It now has **eight elements and
> a denominator that is not one.**
>
> **Both halves are on the sheet and both matter.** Every named colour and material became what
> was asked for — the LoRA, mesh and control did *not* hold this dwarf's attributes against a
> conflicting spec. **And it is still the same dwarf**: face, build, pose, bald head, bracers,
> boots. Structure held by mesh and control, named attributes carried by the prompt. **This is a
> pipeline, not a dwarf generator.**
>
> ### Three method points, all the executor's, all now standing
>
> **1. The uniformity check applied to the *control* class.** Held spans 5.06–6.91 — spread 1.85
> across five regions, evenly distributed. A median of 6.23 built from one region at 20 and four
> at 2 would have been a different fact wearing the same number. Applying it to the control
> rather than the treatment is the sharper use and it is what makes the 7.4× ratio mean
> attribution rather than coincidence.
>
> **2. The instrument has a floor, and it must be quoted with every future result.** Held is
> **not zero** — denoise 0.92 repaints globally. So attribution rests on the *ratio*, not the
> absolute, and **an element effect below roughly ΔE 6 is indistinguishable from global
> repaint.** That bounds what any contradiction test can detect. Do not read a 4-point move as a
> response.
>
> **3. A hue delta is meaningless below a chroma floor.** At C\* ≈ 2 the hue angle is undefined,
> so pauldronR's "−164.8°" is an artifact of the collapse, not a rotation. The executor flagged
> it rather than letting it into the table as a finding. **Any hue number quoted from this
> pipeline carries its chroma or it does not get quoted.**
>
> ### The two that moved less cleanly — stated, not smoothed
>
> **The skirt is the most informative miss.** "Black" collapsed chroma as predicted (23.9 → 0.7)
> but lightness **rose** (14.7 → 33.8) — desaturated mid-grey, not black. **The model reads a
> colour term as a chroma instruction more reliably than as a lightness one.** That is actionable
> for how specs are written: if you want dark, "black" may not get you dark.
>
> **The knee plates are the weakest metal** — C\* 8.2/8.6 against ~1.8 elsewhere, reading closer
> to brown leather than silver. Two of eight moved less cleanly and one moved the wrong way on
> lightness. That is the boundary of the finding and it belongs in it.
>
> ### The co-location correction was right, and it was made before the run
>
> Contradicting something already present is **replacement, not addition**. N9 responded at ΔE
> 47.41 alongside the contra class; my original "N5/N9/N11 predicted to drop" would have been
> wrong. Corrected pre-registration beats a clean-looking post-hoc reading.
>
> ### Arm B — and the contradiction result changes its shape
>
> **De-risked.** The standing worry was character drift across six new twins. The prompt
> controls named attributes at 7.4×, so **per-view prompts carrying the full spec are the
> mechanism for holding identity across views, not a hope.** Predict accordingly: named elements
> should appear at front-view reliability on every view, and any drift should land in
> *structure* — which is mesh- and control-held — rather than in named attributes.
>
> **And Arm B's deliverable is a finished asset, not a coverage number.** The Director's standing
> verdict is *the asset is not close*, and nothing this session has put a better one in front of
> him. Run it through: twins → project → eight strokes → finalize → pack → renders. The Gate 1
> artifact is **reference | asset | provenance | error at his zoom, including views 4–6**, where
> the asset dissolves and where the head sheet structurally cannot show anything.
## 5. What this does not settle

Whether ~40–53% reference coverage is *enough* for the Director to accept the asset is not a
question any of this answers. The defect-severity table is the closest evidence — the blade at
62% non-reference reads ΔE 23.17, the tunic at 1.2% non-reference reads 0.49 — and it suggests
severity falls with non-reference share rather than switching off at a threshold. Gate 1
remains his.
