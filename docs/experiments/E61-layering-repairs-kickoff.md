# E61 — both layering repairs, and the arms that decide between them

**Advisor spec, 2026-08-18. One executor seat (Sonnet), background. Tree
`E:\AI\training\facet_E61\`.**

**Direction (the Director, 2026-08-18, paraphrased):** stop stalling on canon edits to a
character we invented, and stop asking which of two repairs to take — take both and
experiment. The stall was the defect; this arc is the correction.

**Spend: 15 generations (5 arms x 3 seeds).** Not scarcity — design. Seeds 106, 770700,
314159, the same three E60 used, so every arm here is directly comparable to E60's rows.

---

## What already landed before this arc opened (advisor, committed)

Three changes, each with a can-fail leg **proven by reverting the implementation and
watching the leg fail**, then restored:

1. **Spatial prepositions admitted to `STOP`** — `over|under|beneath|above|below|behind|
   beside|across|around|through`. A preposition says where one declared thing sits
   relative to another and cannot introduce an undeclared material; `on` was already
   admitted, so excluding `over` was an inconsistency. It was a load-bearing one: E60's
   composer was barred from the single word the reference's own recipe uses to join the
   garments.
2. **Joint phrases licensed** — `a1.surfaces.json` already declares `vest_shirt` as
   *"plum vest edge against cream shirt"*. A joint IS a layering relationship and its
   phrase is canon exactly as an occupant phrase is; it was simply never licensed, which
   left a composer unable to state a layering the canon already knew. **Licensing is not
   requiring** — the second leg proves a prompt omitting every joint still passes.
3. **A1's vest is declared SLEEVELESS** — N1 is now *"a sleeveless plum long-vest with
   fine gold embroidery"*. E60 measured the cost of leaving it implicit: the composed
   prompt rendered it a full-sleeved coat at 2 of 3 seeds. **W3's precedent is followed —
   the word lives in the garment phrase** — and W3's *other* mechanism (bare `upper_arm`
   + forbidden `sleeve`) is deliberately NOT used, because A1's arms are covered by the
   shirt and forbidding the word would forbid the shirt's own sleeves.

**Non-perturbing anchor:** W3 24/24 and LONGSWORD 5/5 unchanged; A1 census 16/16 ratified,
profile 10/10.

## The question

Which of the two layering repairs — and the sleeveless declaration — actually carries the
garment through a composed prompt? E60 could not tell, because the composer had none of
them.

## Arms — one variable each, all at three seeds

Everything byte-identical to `canon/A1-RECIPE.json` except the positive text.

| arm | text | isolates |
|---|---|---|
| **R** | the recipe verbatim (control + venue re-anchor) | must reproduce `canon/A1_reference.png` at seed 106 or **HALT** |
| **L** | E60's flat comma list, unchanged | E60's incumbent winner, re-run for comparability |
| **P0** | composed prose, **pre-repair canon** (no `sleeveless`, no `over`, no joint) | reproduces E60's failing arm — the baseline the repairs must beat |
| **P1** | composed prose **+ prepositions only** — vest *over* shirt, no joint phrase, no `sleeveless` | does the preposition alone carry it |
| **P2** | composed prose **+ all three repairs** — `sleeveless` phrase, `over`, joint phrase emitted | the full repair |

**P1 vs P2 is the decision.** If P1 already holds the garment, the sleeveless word and the
joint phrase are belt-and-braces rather than load-bearing, and that is worth knowing. If
P1 fails and P2 holds, the declaration is doing the work and the preposition alone was
never enough.

## Gates

- **Gate A** — Arm R seed 106 must reproduce the reference pixel-identically (E58 and E60
  both measured 0 of 1,672,192 differing). A miss halts the arc: something moved.
- **Gate B** — every emitted prompt passes `canon_gate.check_prompt` before submission,
  including all `required: true` clauses. A composer that emits an ungated prompt is a
  defect, not an arm.
- **Gate C** — delivered frame equals requested frame per image (the VAE-rounding law).

## Measurement — narrow on purpose

**The primary readout is the sleeve, because that is the defect the repairs target:** per
image, is the cream shirt sleeve visible on the forearm, and what is N2's hue against
`canon/A1-palette.json` (chroma floor first, circular hue). E60 established the working
range: **63.6–66.8 deg** shift with the sleeve occluded, versus **under 9 deg** when the
sleeve is present. That is a measured separation with both populations known, so it is a
usable instrument here — unlike raw dE-vs-reference, which E60 measured as **confounded by
seed lighting variance** (Arm R's own verbatim text reads "missed" at non-anchor seeds) and
which **must not be used to grade any arm.**

Report per arm per seed. **Rank nothing** — the Director's eye chooses.

## Out of scope

The head-turn / rear-view question (a separate arc; a rear-view arm here would confound the
form comparison); the twin ring; mesh work; painting; adopting `prompt-crafter`.

## Standards compliance

1. **PIN_PER_STEP — 3.** All non-prompt parameters byte-identical from the recipe; the three
   seeds carried from E60 for comparability; every emitted prompt saved beside its image.
2. **ANDON_AUTHORITY — 2.** Gates A/B/C halt; `raise`, never bare `assert`.
3. **NAMED_COMPENSATORS — 2.** Spend has no undo; the bound is the pre-registered design.
   Code and canon revert by pathspec.
4. **DECOMPOSE_BY_SECRETS — 2.** Composition, generation and measurement are separate
   stages over on-disk artifacts.
5. **UNCERTAINTY_GATED_HUMANS — 2.** The arc ranks nothing; the Director's eye decides.
6. **EXTERNAL_VERIFIER — 3.** The sleeve/hue readout is deterministic, external to the
   generator, and carries both calibration populations from E60.

## Predictions

The seat states its own before Stage 2, blind status disclosed, inside the interval the
instrument can return (E60 fixes that interval: ~64-67 deg occluded, under 9 deg present).

**The advisor's, recorded and falsifiable: P1 holds the garment at 3 of 3 seeds and P2
matches it.** Reasoning: E60's failure traced to a missing preposition, and the reference
itself carries sleevelessness on that preposition alone with no `sleeveless` word anywhere.
**If P1 fails, that reasoning is wrong and the declaration is what matters** — which is the
more useful outcome, because a word in canon is portable to every future character and a
preposition is a property of one sentence.
