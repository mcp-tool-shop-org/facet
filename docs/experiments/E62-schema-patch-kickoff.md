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

**2. The collision law — two branches, and neither is substring.**
A `forbidden` token is illegal on a subject when EITHER branch fires. ⚠ Corrected in
place 2026-08-18: the first landing of this item quoted the sleeve pattern with its
word boundaries mangled by the fold tooling, and specified only the mechanical branch —
which the channel showed leaves A1 unprotected. Both defects were checkable and checked.

**Branch M (mechanical):** the gate's OWN compiled matcher — copy the object at
`canon_gate.py:185`, NEVER a pattern quoted in this or any markdown — fires the
forbidden token inside a licensed phrase of the same subject. This is the W3 case run
in reverse: W3's *"a dark green knitted sleeveless tunic"* plus `forbidden: sleeve` is
LEGAL because the lookahead exempts *sleeveless* — while naive `"sleeve" in phrase` is
True and a substring law would refuse W3's own ratified prompt. NAMED FIXTURE, must
stay green after the patch: the selftest legs at canon_gate.py:1170/:1174
(*"sleeve on a bare arm did not fire"* / *"sleeveless was treated as a sleeve"*).

**Branch D (declared):** the subject's surfaces file carries a `protected_tokens`
declaration — token to reason — and forbidding a protected token refuses. This exists
because A1's protection is NOT derivable from its phrases: measured at spec-correction
time, the SLEEVE matcher fires on NONE of A1's 39 licensed phrases (*"a cream
high-collared shirt"* carries no sleeve token; the cuff joint carries none), so Branch M
alone would ALLOW `forbidden: ["sleeve"]` on A1 — and a later prompt naming the shirt's
real sleeves would then be refused, the exact case this law exists to prevent. The seat
adds to `canon/a1.surfaces.json`:
`"protected_tokens": {"sleeve": "the shirt's sleeves are real surfaces; N2's ratified
phrase under-names them"}` — **DRAFT canon data, marked for the Director's ratification
at the fold**, same standing as the depends_on rows. The declaration is honest, not
derived; the seat must NOT derive protection from surface NAMES (names are not licensed
phrases) and must NOT invent any third mechanism.

Can-fail legs, all proven by reversion: (a) W3 fixture green with Branch M live;
(b) a synthetic subject whose licensed phrase carries a true sleeve token + `forbidden:
sleeve` REFUSES under Branch M; (c) A1 + `forbidden: ["sleeve"]` on any surface REFUSES
under Branch D, and removing the declaration makes leg (c) fail — which is the proof the
protection lives in the data, not in a comment. **Two cases, two reasons, kept distinct:**
W3 may forbid *sleeve* (lookahead exempts its garment; nothing licensed has true
sleeves); A1 may not (its sleeves are real and under-named) — and after this lands the
schema knows both reasons instead of the next advisor having to remember them.

**3. `unavailable` as a measurement convention.** E61's three states, kept exactly — **UNAVAILABLE / AVAILABLE+present / AVAILABLE+occluded** — where UNAVAILABLE is decided by a SPATIAL question only. ⚠ Corrected in place: this item first read 'MEASURED / UNAVAILABLE', two names — and collapsing present and occluded into one MEASURED state is how the defect gets counted as a withhold again. The occluded state IS the finding: the readout may
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
