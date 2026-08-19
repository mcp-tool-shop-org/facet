# E62 — the schema patch: depends_on, the collision law, unavailable as a convention

**Advisor spec, 2026-08-18. One executor seat (Sonnet), background. Zero spend — this arc
generates nothing. Tree `E:\AI\training\facet_E62\`.**

**Provenance of the design:** the outside channel proposed this patch as the one transfer
from prompt-craft's convergent schema — *"discipline transfers, the runtime stays home"* —
and its first item was then CORRECTED by E61's own measurement before this spec was
written. Nothing here imports pcraft.

---

## The three items

**1. `depends_on` — layering becomes a relation row, and the measured law rides it.**
E61 decided the carrier: P0 (grouped prose joining the two garments with *and*) occluded
the sleeve 2/3; P1 (the one-word swap to *over*) held 3/3; **L (a flat list that never
joins them) also held 3/3.** So the load-bearing fact is NOT "the prompt must contain
over" — requiring it would refuse Arm L, which held. The law is narrower:
**the two occupants of a layered pair must not be coordinated with "and" in grouped
prose.** *Over* keeps them layered; no join never merges them; *and* built one sleeved
coat.

Schema: a surface row (or joint) gains `depends_on: [<parent occupant id>]` —
`vest_torso`/`vest_skirt` depend on N2, spelled as a parented relation, not more prose in
N1. Composer: `canon_compose` consults the edge — for a depends_on pair it may emit
*over* (licensed, 5df9d20) or leave the phrases unjoined; **it may never coordinate them
with "and."** Can-fail legs, all three REQUIRED: (a) a compose that coordinates a depends_on pair
with "and" fails; (b) **a flat list naming vest and shirt as separate noun phrases with
NO preposition passes the gate** — this leg exists so nobody "helpfully" requires the
word and refuses Arm L, which held 3/3; (c) a compose emitting *over* for the pair
passes. *Over* is licensed. *And* between those two occupants is the illegal join.
*Over* is not required.

**2. The collision law.** A `forbidden` token is illegal when the gate's own matching
semantics would fire it against a licensed occupant phrase of the same subject. This
promotes the A1 sleeveless reasoning — forbidding *sleeve* would delete the shirt's own
sleeves — from an advisor's memory to a schema check. ⚠ COLLISION IS A TOKEN RULE, NOT `if needle in haystack`. The matcher already
exists at canon_gate.py:185: `SLEEVE = re.compile(r"sleeve(?!less)", re.I)`.
W3's occupant is *"a dark green knitted sleeveless tunic"* and W3 forbids *sleeve* —
Python `"sleeve" in phrase` is True for that pair, so **a substring collision law
refuses W3's own ratified prompt.** The collision check therefore fires only when the
gate's OWN token matcher (lookahead included) would fire the forbidden token inside a
licensed phrase. NAMED FIXTURE, must stay green after the patch: the existing selftest
legs `"sleeve on a bare arm did not fire"` and `"sleeveless was treated as a sleeve"`
(canon_gate.py:1170/1174, verified verbatim at spec time).

**Two cases, kept distinct — do not collapse them into one comment.** W3: *sleeve* is
forbiddable because the lookahead exempts *sleeveless* and W3 has no true sleeves — the
token fires on nothing licensed. A1: *sleeve* is NOT forbiddable even under the
lookahead, because the shirt's sleeves are REAL sleeves on licensed surfaces — the token
would kill a legitimate occupant. The schema records both reasons.

**3. `unavailable` as a measurement convention.** Three states — MEASURED /
UNAVAILABLE — where UNAVAILABLE is decided by a SPATIAL question only: the readout may
never gate its own availability, and departure-from-backdrop keying is forbidden (the
palette file's own numbers make it an inverter: sleeve_L 8.25 dE from the backdrop
corners at hue 77.5° in the backdrop's neighbourhood). The convention's worked example
is E61's L* texture cut — corners 0.25–0.50 vs sleeve boxes 13.73–31.02, which correctly
withheld nothing on a corpus where every box stayed on an arm. Facet precedent for the
state: `tools/s3_run.py` exits 4 for could-not-run as distinct from failed (one site —
this item makes it a convention). **UNAVAILABLE lives on readout rows and NEVER becomes a fourth `check_prompt`
failure** — it is a measurement convention, not a canon_gate refuse; the authoring gate
is untouched by this item. Deliverable: the convention documented where measurement
tools can cite it, the E61 two-axis row format named as the exemplar, and a schema for
measurement rows that carries the state explicitly.

## Gates

- Non-perturbing anchor: census byte-identical for W3 / LONGSWORD / A1 before and after;
  every existing canon file validates unchanged.
- Every new check that refuses `raise`s — never bare `assert` — and carries a can-fail
  leg proven by reverting the implementation.
- T34: collector counts move in the same change-set as any added test (the E61 fold paid
  for forgetting this at 5df9d20 — do not repeat it).

## Out of scope, named

pcraft as a dependency (different object); any generation (zero spend); the head-turn /
rear-view question (E59's unpaid denoise-vs-control lever, its own arc); plum-going-brown
on E58's side views; L/770700's wrapped vest; VLM judges of any kind.

## Standards compliance

1. **PIN_PER_STEP — 2.** Schema edits + tests in one change-set; anchors pinned.
2. **ANDON_AUTHORITY — 2.** New refusals raise; can-fail proven by reversion.
3. **NAMED_COMPENSATORS — 2.** Zero spend; every edit reverts by pathspec.
4. **DECOMPOSE_BY_SECRETS — 2.** Schema (canon data) / gate (validation) / composer
   (emission) / convention (measurement) land as separable edits.
5. **UNCERTAINTY_GATED_HUMANS — 2.** The depends_on rows for A1 are drafted by the seat
   and reported for the Director's ratification with the fold — canon data is his.
6. **EXTERNAL_VERIFIER — 2.** Deterministic legs; the census anchor is the cross-check.
