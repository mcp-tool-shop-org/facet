# Grok build #17 — wire the gate, or we ship two things nothing calls

**2026-08-17, facet advisor seat. FINAL BUILD of the session.** Sixteen briefs, sixteen
chips held. A release follows this fold.

*Everything below the line is the paste block.*

---

# Sixteen for sixteen. Last build before the release. `canon_gate.py` exists and nothing calls it — which is the exact defect this whole session was about, one layer up.

## The shape we keep repeating

`canon/W3-IDENTITY.md` specified seventeen elements. The generation prompt named sixteen.
Nothing connected them, so nobody noticed for weeks — the canon was a document a human
read.

We fixed that by making the canon data. **And now `canon_gate.py` is a tool nobody
invokes.** A gate that is not in the path is a document again. If this ships as-is, the
release contains a canon database and a diagnostic layer that no pipeline stage calls,
and the next arc rediscovers the same gap.

You already named the obstacle when you declined to touch it: **T31 pins
`restylize_views.py` at line 197.** That refusal was right. Solve it rather than route
around it.

## What to build

Tests at **t91** — t89 is `flat_trace`, t90 is `evidence`; I mis-assigned t89 last round
and you caught it.

**1. The gate is in the path.** A generation whose prompt does not cover the subject's
canon is refused **before the call is made**, not audited afterwards. Where that attaches
is yours to decide — `restylize_views`, a wrapper the route calls, or the profile load.
State what you chose and why the alternatives lose.

**2. Ratification state is not coverage.** W3 now reads coverage **1.0000, 24/24** — but
four of those rows (`hand_L`, `hand_R`, `greave_L`, `greave_R`) were drafted off the
reference by an advisor and carry `ratify: true`, awaiting the Director. **A gate that
treats drafted as ratified is lying to the person paying for the generation.** Decide how
the gate reports and whether it refuses, warns, or passes on an unratified row — and say
which, because getting this wrong in either direction is a real failure: refusing blocks
work on a route that has produced four accepted assets, and passing silently spends his
credits on a canon he never saw.

**3. A coverage readout across every subject.** Five subjects have IDENTITY.md; two have
surface files. Report what each one's canon covers and what its recorded prompt covered,
so the number is a fact rather than a W3 anecdote. **This lands in the README and the
handbook immediately after your fold**, so it needs to be a number that survives being
quoted.

## Argue

1. **Check the prompt, or DERIVE it?** Checking catches a thin prompt. Deriving the prompt
   from the canon makes a thin prompt unrepresentable — the stronger form, and the one that
   would have made 16-of-19 impossible instead of merely detectable. What does deriving
   cost, and what does it take away from an author who has a reason to phrase something
   differently?
2. **Refuse or warn?** Every ANDON in this repo halts. But this one sits in front of a
   human's money and a route with four accepted assets behind it. Is halting right here, or
   is this the case for a different verdict — and if you invent one, what stops it becoming
   a checkbox everyone passes?
3. **What about the four subjects with no surface file?** The galleon, dragon and longsword
   have IDENTITY.md and no surfaces JSON. Does the gate refuse to run, run degraded, or is
   generating the missing files part of this build? Enumerate before you commission — the
   longsword file already exists and you wrote it.
4. **Does the profile default get repaired, or left as evidence?** It names 6 of 19. It is
   the live default that a generation would actually use. Fixing it silently would delete
   the specimen; leaving it broken ships a default that fails your own new gate on first
   contact. Pick, and say what the other option costs.
5. **Anything unnamed.** Six rounds running you have cut a brief down and been right.

## This one ships, so it is different

A release follows this fold, and the README and handbook get rewritten from it. Prefer the
change that is **stable and legible over the change that is clever**. If some part of this
is better left for the next session, say so and leave it — an honest partial that ships is
worth more than a complete one that destabilises a release.

State plainly what the gate does **not** cover, because that sentence is going on the front
page.

## Constraints

No GPU, no cloud generation, **no credits** — this build is the gate in front of the spend,
not the spend. Read `E:\AI\training\facet_E*\`; write to none of them. Change-set
uncommitted for the advisor's fold. Gates `raise`, never a bare `assert`. Tests ride the
commit; a test that cannot fail is not a test.

⚠ **The canon files are dirty from another seat** — `canon/W3-IDENTITY.md`,
`canon/w3.surfaces.json`, `tools/canon_gate.py`, `tests/test_t87_canon_gate.py` carry the
N18/N19 draft and the ratification queue, with `W3_NAMED` moved 17 → 19 on purpose. Build
on that state; do not revert it.

Counts: the tree with t89 and t90 present collects **1252 / 1198 / 54**. State what your
change-set assumes; reconcile nothing you did not move.

## Calibration

Nominate **one checkable claim** we verify by running it before anything trusts the rest.
Sixteen for sixteen, and a round where the chip loses is still reported.
