# E04 — the pre-projection classification: MAJORITY-NOT-RED. Halt for the A23 ruling.

**Executor session, 2026-08-04, after Ruling 17.** The named classification ran exactly as
pre-stated. **View 0's largest off-palette component is 22.2% sub-40° red — majority-not-red —
which is the branch that halts.** Nothing has been projected.

Ruling 17 expected the other branch (*"the numbers already lean here hard"*). They lean that
way on view 2 and not on view 0.

---

## The completed palette table, and the classification

Blue allowed, both bounds null, exact geometry silhouettes. `CC` = largest off-palette
connected component; `red` = sub-40° above the C\* 12 floor, the fixed window whose upper edge
predates this arm.

| view | figure px | off-palette | % | largest CC | CC ∩ red | % of CC | verdict |
|---|---|---|---|---|---|---|---|
| **0** | 293,865 | 12,136 | 4.13% | **4,562** | 1,015 | **22.2%** | **majority-not-red** |
| 1 | 325,009 | 1,276 | 0.39% | 956 | 951 | **99.5%** | majority-red |
| **2** | 200,391 | **14,957** | **7.46%** | 3,113 | 2,730 | **87.7%** | majority-red |
| 3 | 322,680 | 3,302 | 1.02% | 618 | 313 | 50.6% | majority-red |
| 4 | 293,865 | 448 | 0.15% | 132 | 50 | 37.9% | majority-not-red |
| 5 | 325,009 | 2,168 | 0.67% | 528 | 391 | 74.1% | majority-red |
| 6 | 200,391 | 3,202 | 1.60% | 362 | 39 | 10.8% | majority-not-red |
| 7 | 322,680 | 5,613 | 1.74% | **2,002** | **0** | **0.0%** | majority-not-red |

Across all eight largest components: 5,489 of 12,273 = 44.7% red.

**View 2 is the completed row that was missing and it is materially interesting**: 7.46%
off-palette — the highest of the eight — at **87.7% red**, and it is also the view carrying the
most sub-40° red overall (8,433 px). On view 2 the ruling's expectation is exactly right.

## What view 0's component actually is — characterised, not re-cut

| | view 0 | view 7 | view 6 | view 4 |
|---|---|---|---|---|
| size | 4,562 px | 2,002 px | 362 px | 132 px |
| bbox | x 819–933, y 676–755 | x 398–686, **y 896–939** | x 606–641, y 790–821 | x 701–707, y 725–753 |
| median rgb | (106,42,25) | **(56,77,97)** | (43,18,5) | (48,27,20) |
| median hue | **45.1** | **262.6** | 44.5 | 42.3 |
| median C\* | **36.3** | 14.4 | 15.8 | 13.7 |
| median L\* | 26.1 | 31.7 | 8.5 | 12.4 |
| non-red part, hue p10/p50/p90 | **41 / 46 / 49** | 258 / 263 / 266 | 42 / 45 / 48 | 41 / 46 / 49 |

**Two distinct populations are in this column, and only one of them is a garment candidate.**

**View 0's component is unimodal and straddles the classification's own line.** Its non-red
3,547 px run hue **41 → 49** at p10/p90 — a single contiguous warm-red distribution sitting
across the 40° cut, not a second material beside a first. And its chroma separates it from the
tar: **C\* 36.3 against 13.7–15.8** on the views 4 and 6 components, and **L\* 26.1 against
8.5–12.4**. For comparison, Arm G7's measured *arrived* red lids ran **h 41.1–44.9 at C\*
34.3–48.1** — view 0's component sits inside that, and nowhere near the dark tarred wood that
contaminated my Arm G7 window at C\* just over the floor.

**View 7's component is a different thing entirely**: 2,002 px of desaturated blue-grey,
**h 262.6, C\* 14.4**, in a band across the **bottom of the hull** (y 896–939 of a figure
ending at 939) — and **0.0% red**. It sits **10° below the suspended blue band's 273 lower
edge**. That is the one in this table that looks like an unnamed material rather than a
declared one at a window edge.

## The limitation of the pre-stated instrument, reported and NOT worked around

**The sub-40° window's edge falls inside the population it is classifying.** View 0's component
is one unimodal mass centred at h 45 with 80% of its non-red pixels between 41 and 49; the line
at 40 cuts it, and the cut position — not a material boundary — is what produced 22.2%.

I am reporting this and **not re-cutting**. Moving the line to 50 while looking at the result it
would decide is the one move that is always wrong, and the 40° edge was chosen from the pair's
measured warm-band lower edge long before this arm existed. The pre-stated reading fired on the
pre-stated operand; that the operand has a known edge effect on this component is evidence for
the ruling, not licence for me to re-run it differently.

## What this means for the halt, stated as options and not as a recommendation

The pre-stated branch is unambiguous: **majority-not-red → the A23 question opens → halt before
projecting.** Done. What the ruling now has that it did not:

1. **View 0's component is chromatically consistent with G7's landed red** (C\* 36.3, L\* 26.1,
   h 45.1) and inconsistent with the tar (C\* 13.7–15.8, L\* 8.5–12.4) — it reads as the same
   material the classification was asking about, split by a window edge.
2. **View 7's 2,002 px blue-grey band at the hull's waterline is a separate candidate** the
   classification did not name, 0% red, 10° below the suspended blue band.
3. **View 2 completes the table at 7.46% / 87.7% red** — the strongest confirmation of the
   ruling's expected direction, on the view the table had been missing.

If the A23 re-roll applies, it applies to a named view with a named seed, the rejected artifact
stays in the record, and a second failure is the result rather than a third roll.

## What was not done

No projection. No atlas. No re-roll. No threshold moved. `profiles/ship.json`, `canon/` and all
route tools untouched this leg.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The classification ran on the pre-stated operand at the pre-stated line; every number is one measurement over artifacts already on disk |
| ANDON_AUTHORITY | **3** | The halting branch fired against the ruling's stated expectation and is honoured. The instrument's edge effect is reported as evidence, not used as grounds to re-cut |
| NAMED_COMPENSATORS | **3** | No spend, no generation, no writes outside `docs/` and one JSON |
| DECOMPOSE_BY_SECRETS | **3** | The ship's bands, floor and window all came from the fixture; nothing character-derived entered |
| UNCERTAINTY_GATED_HUMANS | **3** | Three findings handed up as evidence with the options left open; the second candidate (view 7) surfaced rather than folded into the first |
| EXTERNAL_VERIFIER | **2** | The chroma/lightness separation between the view-0 component and the tar components is a comparison the classification did not ask for and could have gone either way. `skip:` on a second model |
