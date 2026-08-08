# E14 handoff 3 — predictions, committed BEFORE any derivation runs

**Executor session, 2026-08-07.** Written and committed before `e04_bands.py` ran, before any
palette JSON existed, before any twin generated. Authorised by
[E14-ruling.md](E14-ruling.md) Ruling 16b via the handoff-3 dispatch.

**Blind status, stated per group rather than claimed wholesale:**

- **Blind to every derivation and every twin in this session** — nothing has been run.
- **NOT blind to the accepted pair.** I generated and measured it in the previous session
  ([E14-task4-report.md](E14-task4-report.md) §6), so the realised values below are in hand:
  L1 C\* 2.93 / 4.56 / 5.39, backdrop hue ~305 at C\* 32.6–37.1, blade L\* 21–24. Predictions
  that are **arithmetic on numbers I already hold** are marked **[held]**; predictions about
  quantities nobody has measured are unmarked and are the real bets.
- **NOT blind to the two artifacts' appearance** — I looked at both pair views and the rejected
  roll at 4× last session, including the gem's magenta drift on view 1's re-roll.
- Predictions about **instrument behaviour** read from source this session are marked **[src]**.

---

## §1 — The wine-merge question

The profile's suspension note expects one merged wine band (oxblood + garnet, the D4/D5/D10
precedent). The estimates had them 1.1° apart (25.4 vs 24.3) — but the estimates are formally
superseded (Ruling 14b) and the pair is the source.

| # | prediction |
|---|---|
| **W1** | **The merge question does NOT have one answer across the pair, and that is the finding.** On view 0 the gem read garnet-red and on view 1's re-roll it read **magenta-purple with a pink glint** — I saw both at 4×. So oxblood and garnet should sit close on view 0 and far apart on view 1. |
| **W2** | Quantified: **on view 0 the two wine clusters sit within 20° of each other; on view 1 they sit more than 40° apart**, with the gem the one that moved. |
| **W3** | Therefore a single merged wine band derived from **both** views must span **> 50°**, or the gem must be reported as its own suspended band. **I predict the honest output is a merged band that is uncomfortably wide, reported with its width as the cost** — not a clean two-band split. |
| **W4** | The mechanism I will look for, stated so it is not invented afterwards: the gem's drift direction (toward ~300) is *toward the realised backdrop's hue*, not away from it. If that holds, the gem's "drift" and L1's "cast" are the same phenomenon at different strengths. **Offered as the hypothesis to test, not as a claim.** |

## §2 — Where the derived chroma floor lands, relative to L1's 5.39 cast

The dispatch is explicit that the floor derives from **separation structure**, never from where
the cast falls, and that where it lands is a **result**.

| # | prediction |
|---|---|
| **F1** | **The separation structure has a wide empty gap and the floor lands inside it.** The declared materials split into two chroma populations with nothing between them: steel and iron below C\* ~6 (measured 2.93–5.39 and, for iron, expected lower still), and gold + the wine family above C\* ~25. **I predict a derived floor in the range 8–20.** |
| **F2** | **Following from F1: L1's 5.39 cast falls BELOW the floor**, so steel stays hue-neutral under the gate's own rule and the fixture's "L1/L2 carry no hue bands" claim survives its own measurement. This is the beast's 15i mechanism repeating on a different subject. |
| **F3** | I predict the gap between the two populations is **wider than 15 points of C\***, so the floor's exact value inside it changes nothing measurable — which is the property that makes F2 robust rather than lucky. **If F1/F2 fail it will be because iron or the dark wrap sits mid-gap**, and that is the case worth looking for. |
| **F4** | The inherited floor is **12.0** on both W3 and the galleon [src: `canon/E04-galleon-palette.json`]. I predict a derived floor lands near it — **within ±6 of 12.0** — and that the honest report says so rather than presenting a re-derivation as a discovery. |

## §3 — The backdrop band

**The mechanism first, because it decides what the band is for.** `palette_gate.py` measures
only **inside the exact mesh silhouette** [src]. So the backdrop cannot enter the gate as
background — it enters as **antialiased rim pixels inside the mask**, carrying backdrop colour.
On the beast the backdrop sat below the floor and never reached the hue gate; here it is at
C\* 32.6–37.1, far above any floor, so those rim pixels WILL read as a real hue.

| # | prediction |
|---|---|
| **B1** | **A backdrop band centred near 305 is needed, and what it exists to admit is rim mixing, not a declared material.** That makes it categorically different from gold and wine, and I predict the derivation has to say so explicitly or the band looks like a fifth material. |
| **B2** | **The quantity it admits scales with PERIMETER, and this subject is the route's thinnest** — proportionally more perimeter than any prior subject. So the rim population here should be a **larger share of the figure** than on the ship or beast. |
| **B3** | **THE HARD ONE — I predict there is NO clean antimode between 290 and 310**, and that the honest output is a **SUSPENSION** of that boundary with the density plotted. Reason: L1's cast at ~295 and the backdrop rim at ~305 are plausibly *the same physical phenomenon at different mixing fractions* — a continuum, not two populations. The repo has been burned exactly here before (distant medians read as a gap that the density showed was monotone). **A suspension with the density plotted is the outcome I expect and the dispatch names it a full success.** |
| **B4** | If a cut IS found, I predict it will not survive the two-view check — i.e. views 0 and 1 will disagree about where it sits by more than 5°, because their realised backdrops differ by 16.6 L\* and their blade casts by 2.5 C\*. |

## §4 — The gate's validation

| # | prediction |
|---|---|
| **G1** | **Both accepted pair views PASS** the gate as drafted. They must, or the bands were derived wrong — this is close to a tautology (the bands come from these images) and I state it as such rather than as a result. The informative part is the *margin*, not the pass. |
| **G2** | **The rejected 770700 artifact also PASSES**, or fires only trivially. Its defect was **occupancy** — gold on the wrong surface — and gold is a declared material in a declared band. Colour-not-placement is structurally blind to it. **A pass here is the gate's documented limitation being demonstrated, not a gate failure**, and it should be reported as the limitation working exactly as the docstring says. |
| **G3** | Following from G2: **this subject cannot validate its gate against a known-bad artifact**, because the only known-bad artifact it has is bad in the one way the gate cannot see. I predict that is the honest conclusion and that no substitute is manufactured. |

## §5 — The twin set

| # | prediction |
|---|---|
| **T1** | Stems v2: **FULL on all views except 2 and 6** (one drop each, the boss term); the rings term drops nowhere. [held: verified visible on all eight at Task 4] |
| **T2** | **The canny counts reproduce the anchor row exactly** — 8,695 / 8,230 / 5,580 / 8,400 / 9,509 / 8,508 / 5,230 / 7,870. Nothing upstream has changed; a drift would mean something moved that should not have. [src + held] |
| **T3** | `estimate_credits` returns **0 credits** on every submission (OSS graph, no paid API nodes). [held] |
| **T4** | **Per-view IoU against the raycast silhouette: 0.85–0.95 on the face-on and diagonal views, and MATERIALLY LOWER on views 2 and 6** — I predict edge-on IoU below 0.85, and the lowest of the eight. Mechanism: the blade is a sliver ~10 px wide edge-on, so a one-pixel boundary error costs a large IoU fraction there and almost nothing face-on. **Spread across the eight ≥ 0.10.** |
| **T5** | **Report absolute px beside every ratio** — the across-pair area swing is 2.061× on this subject (Ruling 10c), so an IoU spread is partly a denominator artifact. Predicting the reporting form, not a value. |
| **T6** | **Mirror corroboration**: views 0/4, 1/5, 2/6, 3/7 have identical silhouette areas by orthographic construction (Ruling 10c retired that as a check), so any IoU difference within those pairs is entirely the generator, not the geometry. I predict within-pair IoU differences smaller than across-pair ones. |

## §6 — View 1 at seed 770700: does naming the rings redirect the gold pressure?

This is the measured-risk view — the same seed and view that sprawled gold onto the crossguard
on the pair, now generated with a stem that names gold **twice**.

| # | prediction |
|---|---|
| **V1** | **I predict the gold sprawl RECURS.** The 12e mechanism is family pressure: a family word's reach scales with how many surfaces it claims, and the stem now claims two instead of one. Adding a second gold mention should *increase* the family's pull, not bind it. |
| **V2** | **The alternative, stated so either outcome is legible rather than rationalised afterwards**: naming the rings gives gold a specific second home adjacent to the boss, and it binds there instead of spreading to the guard. If V1 is wrong, this is why, and it would be a genuinely useful finding — it would mean the D6-spur remedy (name the unclaimed surface) also *contains* family pressure rather than merely labelling it. |
| **V3** | Either way this is **one data point on one view at one seed** and cannot settle the mechanism. I predict the report says so. |

## §7 — The gold watch, across all eight twins

| # | prediction |
|---|---|
| **X1** | **The gold watch fires on 1–3 of the eight twins.** Base rate: one of three pair-class artifacts sprawled (the rejected roll). |
| **X2** | **The crossguard is the surface it fires on**, when it fires — it is gold's nearest large neighbour to the boss, and it is the recorded example. |
| **X3** | **The gem-hue drift watch fires more often than the gold watch** — I saw it on one of two accepted views already, so I predict **3 or more** of the eight show the gem reading magenta rather than garnet. |

---

## What I expect to be most wrong about

**B3 and V1**, and for different reasons worth separating.

**B3** is the one I most want to be wrong about, because a clean antimode at 290–310 would make
the backdrop band derivable rather than suspended. I predict no antimode because the physics
says these are one population, and because this repo has already paid once for reading two
medians as a gap without plotting the density between them. If a cut does exist I will have
under-called the data.

**V1** is a genuine coin-flip dressed as a mechanism. I am predicting the sprawl recurs because
that is what the 12e family-pressure reading implies, but the D6-spur remedy was adopted at
Ruling 13 on the opposite intuition, and the advisor's reading may simply be right. I have
stated both directions above so that whichever way it lands, the report scores a prediction
rather than discovers a rationale.

**And one I expect to hold for an uninteresting reason:** G1. The bands are derived from the
pair, so the pair passing is near-tautological. The number worth reading there is the margin, and
I have deliberately not predicted it.
