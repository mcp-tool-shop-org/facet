# E15 — executor kickoff: the context index (P1). Infra-class; no generation, no GPU.

**Fired by the Director's sequencing word** (2026-08-07: *"We'll fire the database
kickoff once the beast profile is complete"* — Ruling 28 completed it). The design is
**already ruled and committed**: [docs/context-architecture.md](../context-architecture.md)
is the spec — SQLite + FTS5, one file in-repo, GENERATED from the markdown record by a
committed tool, verify-gated, never hand-edited; **the record stays canonical**. This
dispatch builds P1 against the existing record. P2 (slimming the entry documents) and
P3 (the standing ritual) are explicitly NOT this session's work.

**Sequencing:** launches after handoff 16 (the dense export) lands, in the shared
working copy — serial by the advisor's recommendation, the Director's word overrides.
Touch nothing under any handoff-16 path if overlap occurs; stop and report on any
cross-lane collision.

---

## You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                          <- how to work here. Read first, follow exactly.
docs/context-architecture.md       <- THE SPEC. Schema table, tool contract, ritual. Build to it.
docs/experiments/                  <- the corpus: rulings, reports, specs, kickoffs
profiles/*.json                    <- the decisions table's source (the profile stays canonical)
README.md, docs/handbook/          <- prose corpora for FTS
```

Your rules are unchanged (CLAUDE.md §executor). This session writes exactly three
things: `tools/facet_index.py`, `docs/index/facet.db` (generated), and its report.
**It edits no record file** — a builder that "fixes" a source document while parsing
it has failed; malformed-by-convention text is a REPORT item, never an edit.

## Deliverables

1. **`tools/facet_index.py`** with three verbs, per the spec:
   - `build` — parse the record by its own conventions (numbered ruling headers and
     lettered sub-rulings, handoff sections, report headers, the law corpus in
     CLAUDE.md, artifact mentions with status, the named phenomena, the profiles'
     decided keys) into the spec's eight tables. Deterministic: fresh DB each build,
     fixed traversal and insert order, no timestamps, no randomness.
   - `verify` — the external-verifier gate (below). Non-zero exit on any failure.
   - `q "<term>"` — FTS query returning rows as `file:anchor · one-line holding`,
     the forty-lines-not-six-hundred contract.
2. **`docs/index/facet.db`** — built and verified, committed. One file.
3. **The report** at `docs/experiments/E15-report.md`: counts per table, the verify
   transcript, the seeded-question results, and every parsing limitation stated
   plainly (what the conventions could not capture is a finding, not a footnote).

## The verify gate — all four legs, exit non-zero on any failure

1. **Determinism**: two builds from the unchanged record are **byte-identical**.
   *Pre-registered fallback, decided now so it is not retuned later*: if SQLite's
   file header defeats byte-identity (change counters are an implementation
   detail), the gate falls back to `.dump` byte-identity — logical determinism —
   and the report states which leg held. One of the two MUST hold.
2. **Counts against the record's own numbering**: rulings per arc cross-checked
   against a header grep the verifier runs itself (E12 numbers 1–28 with lettered
   subs; E04 1–28; E11's rulings + 4 addenda; E08's 35 amendments); handoffs 1–16;
   experiments E01–E15. A parser that silently drops a ruling fails here.
3. **Zero dangling pointers**: every row's `file` exists and its `anchor` is
   findable in that file.
4. **The seeded question set** — the index must return the right pointer for every
   one. Advisor-authored, answers known before the builder exists (the gate's
   reference derives from the record, not from what the builder happens to parse):

   | question | must return (file · anchor) |
   |---|---|
   | canny values for the beast | E12-ruling.md · Ruling 11a (0.05/0.10 ratified) |
   | which seed resists terms | E12-ruling.md · Ruling 21c (the seed×view map) |
   | the backdrop word and why | E12-ruling.md · Ruling 8a + the 15i correction |
   | thin_extent on the beast | E12-ruling.md · Ruling 25c (0.005, artifact criterion) |
   | why elevated cameras are closed | E12-ruling.md · Rulings 7a + 25b (the 20,000 falsifier) |
   | the dragon's reach ceiling | E12-ruling.md · Ruling 6a (50.46% of 3,240,510) |
   | what happened to the crop pass | E12-ruling.md · Ruling 24b (frame-changes-register ×3; capability banked) |
   | when the pair was accepted | E12-ruling.md · Ruling 14 |
   | the fifth brush signature | E12-ruling.md · Ruling 27d (dark desaturated crevice fill) |
   | what a ruling pays values in | E12-ruling.md · Ruling 26a (registry entries, not prose) |
   | the retired keying method | CLAUDE.md · corner-median keying, three failures |
   | the galleon's accepted mix | E04-ruling.md / README · 36.89/6.87/56.24 = 86.4% of 42.72 |

   A right answer = the target row within the top 3 returns for the question's
   natural FTS phrasing. Report hits per question; **12/12 gates**; a miss is a
   parser/schema finding to fix and re-verify, never a question to delete.

## Predictions before building

Pre-state blind: rows per table (order of magnitude) · which record conventions
you expect the parser to fail on (the corpus was written for humans; some of it
will resist — predict where) · whether byte-identity or `.dump`-identity will be
the determinism leg that holds.

## Out of scope, each with the reason

- **P2 (slimming kickoffs/CLAUDE.md)** — a separate advisor-led pass measured in
  lines shed; doing it here couples the index's birth to editing the record it
  indexes.
- **Vector/embedding search** — the spec rules it out; FTS misses get measured
  first.
- **Editing any record file** — the record is canonical; parse findings are
  report items.
- **A hand-maintained anything** — the DB is derived forever; the day it is
  hand-edited it is wrong by definition (the spec's own words).
- No generation, no GPU, no memory-store writes · do not end a session the
  Director has not ended.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | The builder is committed code; the DB regenerates from the record deterministically; the seeded set is authored before the builder exists |
| ANDON_AUTHORITY | 3 | `verify` exits non-zero on any of four legs and a failed build does not commit; 12/12 on the seeded set gates the deliverable; malformed conventions halt to the report, never to an edit |
| NAMED_COMPENSATORS | 3 | The record is read-only to this session; the DB and tool are new files; undo is deleting two paths |
| DECOMPOSE_BY_SECRETS | 3 | The index maps the record and never becomes it — profiles stay the value registry, markdown stays the authority; the parser knows conventions, the schema knows ontology, the verifier knows neither's internals |
| UNCERTAINTY_GATED_HUMANS | 2 | The halt stages the verify transcript and seeded results for the advisor's eye; parsing limitations surface as findings for a ruling |
| EXTERNAL_VERIFIER | 3 | The verifier checks counts against its own independent grep of the record and answers against an advisor-authored key the builder never sees as input |

## Calibration

The corpus this parses was written across four arcs by many sessions — expect
convention drift and report it honestly. A seeded question that needs its phrasing
tuned to pass is a finding about FTS behaviour worth recording; a builder that
special-cases one document to pass verify is the failure mode this repo exists to
prevent. Negative results — conventions that cannot be parsed, questions FTS
cannot serve — are full successes, reported as the boundary of what P1 honestly
delivers.

---

## Session handoff 2 (2026-08-07) — the stale-claim sweep: a report-only verb

For the P1 steward session (it has full context; citations replace restatement).
Ruled in by the advisor on the steward's own proposal, after the class fired
three times in one night: E04's "28 rulings" at three sites (E15 Ruling 5), the
verifier's own completeness line (`6962946`), and the handbook's four stale
lines including one self-contradiction inside a single file (`2b8a9b9`).

### The deliverable

`python tools/facet_index.py claims` — a **separate verb, report-only, never a
gate**. The four ratified verify legs stay byte-exact as ruled (E15 Ruling 3);
this does not join them. The diagnostic-vs-gate law is the grounds: a
prose-claims sweep swings on phrasing and document class, which is exactly what
must not decide an exit code. Its output is for the advisor's eye; stale sites
are RULING items, never edits from that seat.

### What it checks

Every count-claim in **current-state documents** against the measured tables:
per-arc ruling counts, handoff counts, the experiment count. The
historical/current classification is the steward's own from tonight, applied
mechanically and printed with each row: a kickoff or spec states its counts
as-of-writing (historical-correct); a current-state document (README, handbook,
experiments table, style-registers, context-architecture, CLAUDE.md, the
advisor kickoff ABOVE its supersession banner) must match the measurement.
Output per site: `file:line · claims · measured · classification`. The healthy
state is zero stale rows.

**Out of scope, stated**: flag-count claims ("83/83 decided") — those are the
registry sweep's numbers, not the index's; a checker asserting them from the
wrong instrument would be the second-authority hazard again. Phrasings the
sweep cannot parse are REPORTED as unparseable, not guessed.

### Constraints

Read-only over the record and the DB — the build path and the committed DB are
untouched (byte-identity before/after asserted in the report). The regex lesson
from tonight rides the spec: the window must span markdown links
(`[E12-ruling.md]`), and every phrasing family found gets a test row. Blind
predictions first (how many stale sites remain on the current record — the
advisor believes zero after `2b8a9b9`; a non-zero result is a finding, not a
failure). HALT with the sweep's output on the current record, to the advisor's
eye.

### Standards compliance (this handoff)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | the verb is committed code; its classification rules are printed with every row; predictions registered blind |
| ANDON_AUTHORITY | 2 | report-only BY RULING — the diagnostic-vs-gate law applied at authoring time, not discovered later; stale sites route to the advisor |
| NAMED_COMPENSATORS | 3 | read-only everywhere; the DB byte-identity asserted; undo is reverting one tool commit |
| DECOMPOSE_BY_SECRETS | 3 | the sweep reads the index's measurements rather than re-deriving them; flag counts explicitly refused as another instrument's numbers |
| UNCERTAINTY_GATED_HUMANS | 3 | the healthy-zero prediction is falsifiable; every stale row is the advisor's to rule, never the tool's to fix |
| EXTERNAL_VERIFIER | 2 | the sweep checks prose against measurements derived from the record by independent greps; `skip:` on a second model per the arc's precedent |

---

## Session handoff 3 (2026-08-07) — the discovery fix: E15 Ruling 8b, exactly and only

For the same steward session. The read-only constraint on the build path is
LIFTED for this one change; everything else in handoff 2's constraints stands.

**The change** (ruled at [E15-ruling.md](E15-ruling.md) Ruling 8b):

1. `NUMBERED_RULING_FILES` becomes a **sorted glob** over the ruling-document
   naming convention — state the pattern in the code with its reasoning, and
   confirm it discovers exactly the current six plus `E15-ruling.md` (a
   pattern-matched file with no numbered rulings, like
   `E08-director-canon-ruling.md`, parses to zero rows harmlessly — say so).
2. `verify` **prints the discovered list** — a glob's own misses become
   visible rather than assumed.
3. **E15 joins the count leg**: its own grep, sequence check, and the
   completeness-line convention (bound as of this dispatch: rulings 1–8).
4. Full gate re-run + `claims` re-run. Expected: the four legs pass with
   E15's rulings now counted; the seeded set holds (report any rank
   movement — the corpus grows by E15's ruling rows); **claims still reads
   0 STALE** — the 285-hazard row was reworded out of the family at
   `docs/experiments/README.md` this fold, and your re-run is its test.
5. The DB changes by construction (new rows). **Commit it with the fold — and
   the exception is RULED here, not assumed**: Ruling 4's session-boundary
   cadence gains its one exception — when a builder change alters what the DB
   contains, the committed DB moves with the builder, because otherwise HEAD
   carries a builder and a DB that disagree, which is the two-authorities
   hazard in miniature.

Blind predictions first (row deltas; whether any seeded rank moves). HALT
with the gate transcript. This closes the steward's arc.
