# E15 handoff 2 — the stale-claim sweep, as a report-only verb

Executor session, 2026-08-07. Predictions:
[E15-handoff2-predictions.md](E15-handoff2-predictions.md) (`3730add`, registered
before the verb existed). Dispatch: E15 executor kickoff, Session handoff 2.

Run against the record at `2b57726`. **Read-only throughout**: no record file edited,
the build path untouched, the committed DB byte-identical before and after every run
and left exactly at HEAD per Ruling 4's session-boundary cadence.

---

## 1. The result

**`python tools/facet_index.py claims` — 0 STALE. Exit 0.**

Both the advisor's healthy-zero and this seat's P1 are confirmed on the current
record. The sweep reports **18 claim rows** across **5 phrasing families**:

| verdict | class | rows |
|---|---|---|
| `ok` | current-state | 7 |
| `ok` | historical | 1 |
| `AMBIGUOUS` | current-state | 2 |
| `as-of-writing` | historical | 7 |
| `as-of-writing` | unclassified | 1 |
| **`STALE`** | **current-state** | **0** |

Plus **2 AMBIGUOUS** and **4 UNPARSEABLE**, both reported rather than resolved.

The verb never gates. It exits 0 whatever it finds — the diagnostic-vs-gate law
applied at authoring time, as ruled.

## 2. What it checks, and how a row is classified

A **range** claim (`Rulings 1–30`) asserts the highest number; a **cardinal** claim
(`29 rulings`) asserts how many exist. They are compared against different
measurements, because they are different assertions — E12 carries handoffs numbered
to **16** but only **15** of them, since handoff 1 was never labelled, and conflating
the two would manufacture a stale row out of a correct document.

Classification is the steward's own from last night, applied mechanically and printed
with every row:

- **current-state** — README, the handbook, the experiments table, style-registers,
  context-architecture, CLAUDE.md, and the advisor kickoff *above* its supersession
  banner. Must match the measurement.
- **historical** — a kickoff, spec, report, halt or ruling, and the advisor kickoff
  *below* its banner (found at `docs/advisor-kickoff.md:3`). States its counts as of
  writing and is correct as written.
- **unclassified** — on neither list. Printed as such, never assigned. **One file
  meets this**: `docs/profiles-design.md` (P5 predicted 1–3).

Measurements come from the index, not from a second derivation of the record — the
four ratified verify legs already did that derivation, and re-deriving here would be
the second-authority hazard again.

## 3. The two AMBIGUOUS rows — the predicted case, exactly

```
docs/experiments/README.md:21   "29 rulings + the close"
docs/handbook/subjects.md:31    "29 rulings + the close"
```

**`+ the close` makes the assertion unresolvable**: whether it claims 29 or 30
depends on what the record counts "the close" as, and picking a reading would be
inventing a claim to check. Both are reported and neither is resolved to a number
(P3, pre-registered).

Worth stating so the ambiguity is not read as a defect: both sites currently agree
with the measurement on the *29* reading, so nothing is wrong today. What is
unresolved is what they will mean when E04 next moves.

## 4. The four UNPARSEABLE rows — and the finding inside them

```
docs/experiments/E04-executor-kickoff.md:244  "Amendments 1-3"
docs/experiments/E07-report.md:4              "Amendments 1–2"
docs/experiments/README.md:17                 "Amendments 1-2"
docs/experiments/README.md:28                 "285 rulings"  (no measurement for E15)
```

**The first three are one finding: "Amendment" is overloaded in this record.** It
names E08's 35 numbered `> ### Amendment N` blocks — which the index models — *and*
amendments appended to a spec document, which it does not: E04's spec carries 3,
E07's carries 2. An `amendments range` family would have parsed all three and
silently attributed spec amendments to E08's series. **Not having that family is
correct**, and the honest handling is to leave them unparseable and say why.

**The fourth is a hazard for the advisor's eye, not a stale site.**
`docs/experiments/README.md:28` reads `285 rulings` inside E15's table row — that is
*the index's own total row count*, not a count of E15's rulings. The sweep attributes
it to E15 by nearest-arc and then declines, because the index holds no E15 ruling
measurement. It declines for the right reason today. **If finding §5 is ever
addressed it becomes a false STALE** (285 against 7), because no phrasing rule
distinguishes "285 rulings [in the index]" from "285 rulings [of arc E15]". Flagged
now rather than met later.

## 5. A finding the sweep turned up incidentally — and it is about the index

**`docs/experiments/E15-ruling.md` carries 7 numbered rulings and not one of them is
in the index.**

`NUMBERED_RULING_FILES` in `tools/facet_index.py` is an explicit hardcoded list, and
E15's ruling document — written after the builder — is not on it. Every other ruling
document is:

| document | numbered rulings | in the builder's list |
|---|---|---|
| E04-ruling.md | 29 | yes |
| E10-ruling.md | 12 | yes |
| E10-offsurface-ruling.md | 7 | yes |
| E11-ruling.md | 7 | yes |
| E12-ruling.md | 30 | yes |
| **E15-ruling.md** | **7** | **no** |

**The verify gate cannot see this**, and that is the part that matters. Its count
checks are per-file greps against the *same hardcoded list*, so a ruling document
absent from the list is absent from both the parser and its verifier. The gate tests
that no listed file loses a ruling; it cannot test that no file is missing from the
list. That is the repo's own law — *a gate must test the operation's failure mode,
not its success mode* — landing on the instrument written to enforce it.

The list was made explicit deliberately, for determinism: *"explicit and sorted
rather than globbed, so the insert order is a property of this file rather than of a
filesystem."* That reasoning is satisfiable by a **sorted glob**, which is equally
deterministic and cannot silently omit. The trade was made in one direction without
the cost being measured, and this is the cost.

**Not fixed here.** The dispatch is explicit — *"Read-only over the record and the
DB: the build path and the committed DB are untouched"* — so the build path was not
opened. It is a ruling item.

## 6. A defect of mine, found and fixed inside this session

The first `CLAIM_SHAPED` detector flagged **37** unparseable rows. **35 of them were
noise**, and the cause was a distinction I had not made: *a range is only a
count-claim if it starts at 1*. `Rulings 1–30` asserts that thirty exist;
`Rulings 21–23` names three of them and asserts nothing about a total. Corrected, the
bucket falls to 4 — and every one of those 4 is real.

One further correction, from the same run: a document named for an arc governs the
claims it makes without naming one. `E04-executor-kickoff.md:179` writes
`(Rulings 1–12)` with no `E04` token on the line; falling back to the filename's arc
is the record's own convention rather than a guess, and it moved that row out of
unparseable and into a correctly-classified `as-of-writing`.

## 7. The regex lesson from last night, applied

The window spans markdown links. Both this seat's hand-sweep and the advisor's
consumer-grep failed last night for the same reason — a `[^.\n]` window cannot cross
the `.md` inside `[E12-ruling.md]` — and the sites they missed were exactly the ones
where the arc is named only in a link. The families here search the raw line prefix
with no dot-free window, and **every family found on the record prints its site count
and an example**, so a family silently matching nothing is visible rather than
assumed:

```
amendments cardinal   2 site(s)   e.g. docs/experiments/README.md:18
experiment span       1 site(s)   e.g. docs/profiles-design.md:36
handoffs range        1 site(s)   e.g. docs/advisor-kickoff.md:33
rulings cardinal      5 site(s)   e.g. README.md:87
rulings range        10 site(s)   e.g. README.md:141
families with no site on the current record: addenda cardinal, handoffs cardinal
```

Two defined families have no live site. They are reported rather than deleted: a
family with no site today is not evidence the phrasing will not appear tomorrow, and
the printout is what makes its absence checkable.

## 8. Out of scope, as dispatched

**Flag-count claims (`83/83 decided`, `81/81 flags`) are refused.** Those are the
registry sweep's numbers, from `e04_registry_sweep`, not the index's. A checker
asserting them from this instrument would be the second-authority hazard the whole
design exists to prevent — so the sweep does not look at them, and this is stated in
the code rather than left to inference.

The four ratified verify legs are untouched and still pass byte-exact: byte-identity,
zero dangling over 1,079 rows, counts matching the verifier's own greps, 14/14, exit
0. `claims` does not join them.

## 9. Predictions, scored

| prediction | outcome |
|---|---|
| P1 — zero stale sites | **confirmed**, agreeing with the advisor. The named falsifier (README:141's closed range going stale on a 31st E12 ruling) did not fire — E12 stands at 30 |
| P2 — 4–7 phrasing families | **held**: 7 defined, 5 with live sites. One shape I predicted as a family — `Rulings 1–N so far` — is implemented as an *ambiguity modifier* instead, which is the better fit and is stated here rather than quietly reclassified |
| P3 — at least one genuinely ambiguous phrasing | **confirmed, and it is exactly the predicted one**: `+ the close`, 2 sites, reported not resolved |
| P3 — unparseable total 1–3 | **missed**, narrowly: 4 |
| P4 — DB byte-identical | **confirmed** before and after every run; the committed DB ends the session at HEAD |
| P5 — 1–3 unclassified files | **confirmed**: exactly 1, `docs/profiles-design.md` |
| unpredicted | the E15-ruling.md omission (§5), the "Amendment" overload (§4), the `285 rulings` mis-attribution hazard (§4), and my own range-detector defect (§6) |

## 10. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | the verb is committed code with no tuning parameters; its classification rules print with every row; predictions registered at `3730add` before it existed |
| ANDON_AUTHORITY | 2 | report-only by ruling — exits 0 on every path, asserted by running it; stale sites route to the advisor and §5's finding was reported rather than fixed, because the dispatch closed the build path |
| NAMED_COMPENSATORS | 3 | read-only over record and DB, asserted by sha before/after each run; undo is reverting one tool commit |
| DECOMPOSE_BY_SECRETS | 3 | the sweep reads the index's measurements rather than re-deriving them; flag counts refused in code as another instrument's numbers |
| UNCERTAINTY_GATED_HUMANS | 3 | every AMBIGUOUS and UNPARSEABLE row is the advisor's to rule; the `285 rulings` hazard is surfaced before it can fire rather than after |
| EXTERNAL_VERIFIER | 2 | prose checked against measurements the verify legs derive from the record by independent greps. *skip:* a second model, per the arc's precedent |
