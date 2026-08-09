# E26 — predictions, committed before any source file was opened

**Executor session. Written 2026-08-09** (the session clock reports 2026-08-08; the
dispatch this follows is dated 2026-08-09 — recorded as a discrepancy, not resolved here).

Committed as the session's first act, per the dispatch. Scored in
`E26-front-door-counts-report.md`.

---

## What had been read when these were written

Disclosed so "blind" means something:

- `CLAUDE.md` — method only; states no test count anywhere.
- `docs/experiments/E26-front-door-counts-kickoff.md` — the dispatch. **It supplies a
  baseline of 384, the six-group surface enumeration, the seven `CLAIM_FAMILIES` names,
  `record_markdown()`'s scan set, and the 17-file / 2,768-line candidate sizing.** Every
  row below that leans on one of those is marked SEEDED.
- The session's own memory index line, injected by the harness, which contains the string
  **"suite 370/362"**. This is a stale figure from E23 and it seeds exactly one row (P4).
  Marked SEEDED-MEMORY.
- The studio constitution and memory index, forced by the memory-gate hook before any
  write. Neither states a facet test count.
- `git log --oneline -5`, `git status --short`, `git branch --show-current`.

**Not opened:** `README.md`, any `README.*.md`, `CHANGELOG.md`, `SHIP_GATE.md`,
`SCORECARD.md`, `SECURITY.md`, anything under `site/`, `tools/`, or `tests/`, and both
prior rulings (`E23-ruling.md`, `E24-ruling.md`) named in the paste block — those are read
after this file is committed.

Blindness key: **BLIND** = no artefact bearing on the row was seen. **SEEDED** = the
dispatch supplied a figure I am reproducing or adjusting. **SEEDED-MEMORY** = a harness
memory line supplied it.

---

## The rows

| # | prediction | point | interval | blindness |
|---|---|---|---|---|
| P1 | **Sites** carrying a test-count claim across the dispatch's six enumerated surface groups | **22** | 22–30 | SEEDED |
| P2 | **Additional** front-door surfaces, not in that enumeration, carrying a *current-state* test-count claim | **1** | 0–3 | BLIND |
| P3 | Full-artifacts tier count `pytest --collect-only` reports at HEAD | **384** | 384–392 | SEEDED |
| P4 | Tier gap (full minus base) → base-tier count | **8 → 376** | gap 6–12 | SEEDED-MEMORY |
| P5 | Is any *current-state* claim wrong at HEAD? — and on how many sites | **YES, 14** | 8–22 | BLIND |
| P6 | *Historical* test-count sites inside Half A's scan scope that it must not fire on | **4** | 2–10 | BLIND |
| P7 | Does Half A's own test change the number it pins? | **YES** | — | BLIND |
| P8 | Tests T34 adds to the collected count | **8** | 4–14 | BLIND |
| P9 | New STALE rows Half B's widening produces on its first run | **5** | 0–15 | BLIND |
| P10 | Index verify legs, scratch `--db`, before and after Half B | **19/19 both** | — | SEEDED |
| P11 | Does the current-vs-historical rule turn out ambiguous, i.e. is there a finding for the ruling? | **YES — at `CHANGELOG`'s Unreleased block** | — | BLIND |

---

## Reasoning, per row — so a miss is diagnosable

**P1 — 22 sites.** Arithmetic on the dispatch's own enumeration, in the unit E23's law
demands (**sites, not files**): README 2 + `SHIP_GATE` 2 (item D's verify line, its
lineage) + `site-config.ts` 1 + `getting-started.md` 2 + `reference.md` 1 + seven
translations × 2 = 14. Sum **22**.

The dispatch says *verify, do not inherit*, and I cannot verify before committing this —
so the row is a prediction **about the enumeration's correctness**, not about arithmetic.
Its dominant failure mode is coupled: README and its seven translations move together, so
one extra README site is **eight** extra sites, not one. That is the whole width of the
interval. A README badge, or a scorecard row naming a test total, would do it.

**P2 — 1 extra surface.** `SCORECARD.md` is the likeliest carrier the dispatch did not
list, with `CHANGELOG`'s Unreleased block second. Both are front-door and neither appears
in the six groups. I take **1** rather than 2 because the dispatch's author enumerated
deliberately and the E22 law cuts both ways — the population being under-stated is a real
risk, but so is my inventing members for it.

**P3 — 384.** Straight from the dispatch, so this row is near-worthless as calibration; I
record it only so the report can say whether the dispatch's own number survived contact.
The interval is one-sided upward because E25 is live in this tree and T33 is its
allocation — if any of it has landed, the count only rises.

**P4 — gap of 8.** The only row seeded by memory rather than the dispatch. "370/362" is a
gap of **8** at E23; I predict the artifact-gated set has not changed size since, giving
**376** base against **384** full. This is the row I most expect to lose: two arcs have
added tests since E23 and nothing says they all landed on one side of the tier boundary.

**P5 — YES, 14 wrong.** The dispatch's premise is four drifts in two days, so *nothing is
wrong at HEAD* would be the surprise. I name the **seven translations, two sites each**,
because translated READMEs regenerate on a separate cadence from the source and the
harness memory line calls them stale outright. That makes the prediction sharp: if the
wrong sites turn out to be the site handbook rather than the translations, the row is a
miss even at the right total.

**P6 — 4 historical sites.** Presumes Half A scans the **front door only** — the six
enumerated groups plus `CHANGELOG` — and does *not* scan `docs/experiments/**`, where
scores of reports state suite counts as of their own date. Under that scope: three
`CHANGELOG` released entries carrying a count, plus `SHIP_GATE`'s lineage as one site
holding several numbers. If Half A instead has to scan `docs/**`, this row is off by an
order of magnitude and the scope choice is the finding.

**P7 — YES, and it is the structural trap.** `pytest --collect-only` counts **T34's own
tests**, so the commit that adds Half A moves the very number Half A pins. The test cannot
pass on the tree that introduces it unless every site is bumped by T34's own test count in
that same commit. I predict this bites during the work rather than being designed around
in advance, and that it is the reason the surfaces must be *edited* by this arc rather than
merely audited.

**P8 — 8 tests.** One per enumerated surface group is six; plus one for the
historical-count rule and one for the collector itself. A guess about a design not yet
written.

**P9 — 5 STALE rows.** Repo-wide totals are the movers: `rulings-range`, `handoffs-range`
and `experiment-span` all advance every arc, while a per-experiment cardinal ("E24 has 7
rulings") is correct forever and should stay clean. So I expect the new STALE rows to be
few and to cluster on the range/span families, in `CHANGELOG` and `SCORECARD`. If the
count comes back large, it will be because released `CHANGELOG` entries are being compared
against a present-day index — which is P11 wearing a different hat.

**P10 — 19/19 both.** The paste block states the leg count; gate 4 forbids touching
`record_markdown()`, so an unchanged result is the prediction the gate exists to confirm.
A change here would mean the sweep's scan set is not as separable from the index build as
the dispatch ruled it to be.

**P11 — YES, at Unreleased.** A released `CHANGELOG` entry is unambiguously historical and
`SHIP_GATE`'s lineage is unambiguously historical. The **Unreleased** block is neither: it
is shaped like a released entry and dated like the present, and any count inside it is a
current-state claim wearing a historical entry's clothes. I predict the rule needs a
stated disposition there, and that per the dispatch it goes to the ruling rather than
being decided by me.

---

## Two rows I am declining to predict

- **Whether gate 2 passes** — whether Half A fails behaviourally on a deliberately stale
  surface is a property of code I have not written. Predicting it would be predicting my
  own compliance, which cannot be wrong and so teaches nothing.
- **Whether the arc's surface set is complete** — completeness is not knowable from a
  spec, only from a scan, and the scan is the work.
