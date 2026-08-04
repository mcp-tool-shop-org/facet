# E08 N11 — the grammar test. **It dropped. Stopping rule fires.**

**Amendment 13:** [E08-ruling-gate0.md](E08-ruling-gate0.md) · **Canon:** [W3-IDENTITY.md](../../canon/W3-IDENTITY.md)
**Run:** 2026-08-04, executor session. One diffusion pass, 54 s.
**Prediction, recorded first:** `facet_E08/N11/PREDICTIONS.md` — blind. **Wrong**, and so was the
advisor's.

## The test

Exactly one edit against the bracer run's prompt, everything else byte-identical:

```
- gold-trimmed brown leather bracers                                    (modifier form)
+ brown leather bracers, a gold plate on each outer forearm             (head-noun form)
```

Control image byte-matched at 20,973 px (canny 15,325 + contour 9,958), seed 770700.
Deliberately **not** the full 16-element spec — that would have grown the prompt by five terms
and confounded the grammar change with competition for attention.

## Result: no plate, and no measurable change at all

The forearm is indistinguishable from the modifier form. Promoting the element to its own head
noun did not make it land.

| | median ΔE | mean | >10 |
|---|---|---|---|
| whole figure, modifier vs head-noun | **1.07** | 1.44 | 0.4% |
| forearm region only | **1.15** | 1.68 | 1.5% |

**The added phrase had essentially no effect on the image.** This is stronger than "the plate
did not appear" — the model did not respond to the phrase at all.

*A gold-pixel count over the forearm crop is reported in the log and is **not usable as
evidence**: the crop box catches the gold pauldron edge, so it reads 5.6% / 5.1% on the new arms
against 1.96% on canon, which inverts the truth. The ΔE and the eye are the evidence.*

## What fires

**Amendment 13's stopping rule, as written:** *"If the promoted phrase also drops it, the
premise is weaker than Amendment 12 assumed, Arm B waits, and the artifact reading comes back
onto the table. One roll either way."*

- **Arm B waits.**
- **The specification premise is weaker than assumed.** Two of three named elements now fail to
  reproduce: the bracer's gold trim as a modifier, and the same element as its own head noun.
- **The grammar constraint is not rescued by this test**, and is not refuted by it either — it
  predicted this element would land, and it did not.

## The distinction that was written down first, and is not a rewording

`PREDICTIONS.md`, before the roll:

> *"The knee plates replaced what was there, and this does not. Fur gave way to plate on the
> knee — one element per surface. Here the model must layer a gold plate ON brown leather that
> the same prompt also asks for, on the same body part. Two elements competing for one surface
> is not what the armour test demonstrated, and the grammar constraint says nothing about it."*

That remains the live alternative: **co-located elements may be the hard case, independent of
grammar.** Per the stopping rule it is a *future* test and is **not** run here. Rerolling
variations until the plate appears is fitting the spec to the outcome.

## Where the ledger stands on prompt-expressible canon

| element | form | result |
|---|---|---|
| gold knee plates | head noun, replaces what was there | **landed in full** |
| brown leather bracers | head noun, replaces what was there | **landed** |
| gold trim on the bracer | modifier on another noun | dropped |
| a gold plate on each outer forearm | own head noun, **co-located** with an element already named | **dropped** |

Every element that **replaced** what occupied its surface landed. Every attempt to **add a
second element to an occupied surface** dropped, in both grammatical forms. That pattern is
consistent with the data and is offered as a hypothesis, not a finding — it rests on two
positives and two negatives.

## Unchanged

The canon pair stays frozen and demoted to specification source. `W3-IDENTITY.md` stands as
authored, with **N11 now measured as not landing** rather than predicted to land. A2 stands at
28.4% → 39.1%. Nothing here touches the projection path.
