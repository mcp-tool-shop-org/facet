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

## Dispatch record (living)

- 2026-08-18 — spec written; three repairs landed and proven-can-fail at the advisor's
  hand (commit 5df9d20); seat dispatched on Sonnet, background.
- 2026-08-18 — **outside-channel ruling folded, mid-flight.** The channel read the E60
  fold beside its own prompt-craft build and called the three repairs **convergence, not
  a merge request** — pcraft independently grew the same three ideas (spatial relations,
  licensed joints, absence-as-a-word). Its brief was ruled on as follows.

  **Verified before acting (the channel's own protocol).** Its checkable claims about
  pcraft are verbatim true at source: `GATE_FAIL=2 / PARTIAL_UNCONFIRMED=3 /
  GATE_UNAVAILABLE=4` in `errors.py`, `Zone.UNAVAILABLE` in the gate, and *"calibrated
  for absence earns required"* literally in its schema. Its claim that **"facet already
  has exit 4" is overstated**: exactly one site (`tools/s3_run.py`, could-not-run refusal)
  carries the pattern — a precedent, not a convention. Reported back as such.

  **ADOPTED NOW, into the running arc (steer sent to the seat):** measurement rows gain an
  explicit **UNAVAILABLE** state behind a calibrated box-preflight — a seed that slides
  the figure so the sleeve box samples vest fabric is *could-not-see*, not a failed arm,
  and an unavailable row does not vote. E59 Gate 1 is the paid-for precedent; the seat's
  preflight calibrates against E60's twelve known images, and if it cannot separate a
  valid box from a slid one on those, it says so rather than inventing a threshold.

  **ADOPTED AS E62, opens when E61's sheet exists — not before:** the schema patch, facet
  spelling only, no pcraft import. (a) `depends_on` edges — after E61 reports, the winning
  layering carrier becomes a **relation row with a parent** in the surfaces file, not more
  prose in N1; P1-vs-P2 is literally "is the preposition a depends_on, or is the adjective
  the atom." (b) The **collision law**: a forbidden token is illegal when it is a substring
  of a licensed occupant phrase — the A1 sleeveless reasoning (forbidding `sleeve` would
  delete the shirt's own sleeves) promoted from an advisor's memory to a schema check.
  W3 keeps its bare-arm mechanism; A1 structurally cannot have it, and the schema will
  know why. (c) Measurement-side `unavailable` made a convention rather than one tool's
  habit. **Not edited now because the seat shares `canon_gate.py` in flight** — the
  two-live-sessions law covers instruments as well as indexes.

  **DECLINED, with the channel in agreement:** pcraft as a dependency (different object:
  it gates atoms against pixels, facet gates phrases against a surface database before
  spend); VLM/CLIP judges (E60 finding 6 stands); a composer learning loop (optimising
  toward a gate metric is how the sleeve happened); pcraft's RGB palette-hist (strictly
  worse than A1-palette's circular-hue/chroma-floor form); OpenPose plates (the control
  is this mesh's own clay; E59 measured the generator overriding a *correct* control);
  identity adapters (the A1 PNG is the identity plate; twins belong to the mesh); the
  cross-family guard (one generation family here).

  **Sequencing accepted as given:** no second prompt-form experiment and no "try pcraft
  on A1" until E61's sheet exists. If P1 and P2 both fail, the next lever is E59's unpaid
  denoise-vs-control question — not a contract question.
