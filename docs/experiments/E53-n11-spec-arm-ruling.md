# E53 — ruling: co-location survives, its own discriminator was mis-specified, and the compound occupant was already tried

**Advisor, 2026-08-17**, on `E53-n11-spec-arm-report.md`. Zero spend. The seat predicted
ABSENT at ~65% before opening a pixel, said so with its reasoning, and was right.

---

## Ruling 1 — N11 is absent from the from-scratch SPEC arm

| arm | N10-box C\* | h° | |
|---|---|---|---|
| BRACER (known absent) | 18.5 | 50.7 | |
| N11 (known absent) | 19.1 | 51.0 | |
| **SPEC (the question)** | **20.5** | **54.1** | leather cluster |
| gold calibration (pauldronR) | 37–43 | 78–80 | not close |

**Co-location survives from-scratch specification.** The blocked-addition class is *not*
merely an artifact of patching, which was the branch that would have made the repair free.

What licenses the number: the seat's own recomputation of BRACER matches the record's
published `anchor_bracer_vs_n11.json` **to the last integer** (`[65,39,26]`, L 18.6, a 11.7,
b 14.3, C 18.5), so its instrument is calibrated against a figure it did not produce. And it
did not re-derive the instrument that failed here before — it used a *median colour over a
tight box* rather than the *fraction-above-threshold over a loose crop* that caught the
pauldron edge and inverted the truth in Amendment 15.

**Gate B was demonstrated able to fire** — a deliberately-bad box run through the same check
returned `overlap_px=1575, admits_pauldron=True`. A 0 that has been shown capable of being
non-zero is evidence; this repo has been burned twice by 0s that could not have been anything
else.

## Ruling 2 — the pre-registered discriminator fired, and it was mis-specified

E08 pre-registered (`E08-ruling-gate0.md:1051-1053`):

> **If N5 and N9 land while N11 drops, co-location is wrong too and something narrower is
> going on.**

N9 landed. N11 dropped. **The stated conclusion does not follow, because N9 was never a test
of the rule.** Amendment 16 measured that the green skirt panels *arrive unprompted* — they
are in the base distribution for this figure — and this seat confirmed them visually in SPEC
while establishing Gate A. **An element that would have appeared anyway cannot demonstrate
that a specification added it.** Its landing has the same reading whether the rule holds or
not, which is this repo's own instrument-range law applied to a discriminator instead of a
metric.

Read against elements that actually had headroom, the record is consistent:

| operation | in base already? | outcome |
|---|---|---|
| gold knee plates **replace** fur | no | **landed fully** |
| brown leather bracers **replace** fur cuff | no | **landed** |
| green panels **added** beside the kilt | **yes** | "landed" — uninformative |
| gold plate **added** beside the bracers | no | **dropped** (1.07 patched, absent from scratch) |
| gold trim **added** within the bracers | no | **dropped** (the split, below) |

**Amendment 15 stands, and N9 was never evidence against it.** The correction is to the
discriminator, not to the law.

## Ruling 3 — the compound occupant on the forearm was already tried, and it split

This is the one that decides the spend, and it was one file away the whole time.

`E:\AI\training\facet_E08\BRACER\w3clay_0_gen.json` contains, verbatim:

> …dark red layered cloth skirt with a leather belt, **gold-trimmed brown leather bracers**,
> gold knee plates…

That **is** a compound occupant — one noun phrase, one surface, two materials. Its measured
result is in `E08-canon-spec-proposal.md:18`:

> **SPLIT** — "brown leather" landed (fur cuff → smooth segmented leather); **"gold-trimmed"
> did not**.

and the same document names the shape in its own words: *"A compound term — material plus
trim — delivered its head noun and dropped its modifier."*

So on the forearm, three forms are now measured, and the surface with the only real headroom
in the whole specification has refused all three:

1. `gold-trimmed brown leather bracers` — compound, premodifier → **split**
2. `a gold plate on each outer forearm` beside `brown leather bracers` → **dropped**, patched
   *and* from scratch
3. `brown leather bracers` alone → lands

**The spend stays refused.** The only form nobody has run is a postmodifier —
*"brown leather bracers with a gold outer plate"* — and reaching for it means re-running the
grammar hypothesis Amendment 15 already killed by measurement:

> The grammar hypothesis was mine and it is not what is doing the work. […] **Both
> grammatical forms land when they replace and drop when they add.**

A third grammatical form is a third draw from a distribution the record has sampled twice and
found flat. That is not an experiment; it is a reroll with a syntax tree attached.

## What is open, stated as a candidate and not as a finding

The axis may not be *occupied surface* at all. Every element that landed either replaced its
surface's occupant or was already in the base distribution; every element that dropped was a
**new** thing asked for beside an existing one. Whether the operative variable is *occupancy*
or *base rate* is not settled by anything in this record, and I am not proposing an arm for it
— the honest test needs a subject where the two come apart, and W3 is not that subject.

Recorded here so the next seat inherits the question rather than the assumption.

## Consequences for the canon schema

`canon/w3.surfaces.json`'s three `blocked_additions` rows are now differently supported and
the file should say so — **as its own change, with its own tests and the Director's word**,
not as a side effect of this ruling:

- **N11** — `"measured drop, median dE 1.07"`. Now *also* measured absent under from-scratch
  simultaneous specification (this arc). Strengthened.
- **N5** — `"predicted to drop"`. Still unmeasured; it has no measurement region. Unchanged.
- **N9** — `"predicted to drop"`. **The prediction is void rather than confirmed or
  refuted**: N9 arrives unprompted, so this row was never testable as written. The honest
  edit is not "landed" — it is that the row is not a blocked addition at all, because the
  surface it names was never unoccupied by it.

## What the report did that the dispatch did not ask for

- **It named the scope bound instead of burying it.** The sword-gripping forearm has *no
  assessable surface from this camera in any arm tested, canon reference included*. It
  reported that as unanswerable rather than folding it into a second ABSENT — *test the
  property, not a proxy for it*, applied by the seat to its own headline.
- **It found a real provenance gap and reported it.** `SPEC/` has no `w3clay_0_gen.json`
  where `BRACER/`, `N11/` and `ARMOUR/` all do. It held Gate A on three independent lines
  instead — byte-identical control/mask across all four arms, a textual chain, and the
  visual presence of N9 and N5 exactly where the record independently reports measuring
  them. **The missing sidecar is a live defect in this repo's own standard** and is now on
  the record as one.
- **An orthogonal check fell out of the design.** CONTRA's pauldron is desaturated by
  construction, so a forearm box leaking pauldron pixels would drag CONTRA's forearm reading
  toward neutral. It does not — C\* 14.2, h 55.4, inside the leather cluster. A second
  independent proof of non-admission that nobody had to build.

## Out of scope, respected

No generation. Nothing committed by the seat. `canon/w3.surfaces.json` untouched. No repo
tool added, and **neither `t92` nor `t93` was claimed** — both remain free.
