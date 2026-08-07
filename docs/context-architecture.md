# Context architecture — the index that lets the repo grow

**The Director's charge (2026-08-07):** organize the record so the repo keeps growing
without taxing a session's context. **The ruling: SQLite + FTS5, one file in-repo,
GENERATED from the markdown record by a committed tool and never hand-edited.** The
markdown stays canonical — corrections in place, prose holdings, the evidence trail —
and the database is a derived, regenerable index over it. A session queries instead of
reading; what it reads after the query is the forty lines the query pointed at, not the
six hundred it would have skimmed.

## Why this type, and not the alternatives

- **The studio already runs this pattern three times**: `repo-knowledge` (FTS5 over
  repo facts), `readouts/model-knowledge/models.db` (SQLite + views + FTS, 119 models,
  retrieval-verified), and the sdlab lane's record store. Proven habits, zero new
  infrastructure, no service, no GPU.
- **Deterministic retrieval.** An FTS query returns exact rows carrying exact
  `file:anchor` pointers. The record's value is precision citation — "Ruling 15c
  pre-registered the allowance branch" — and embeddings retrieve approximately, which
  is the wrong property for a legal record. (Vector search is out of scope; revisit
  only if FTS measurably misses in practice.)
- **One file, versioned, in-repo.** Any session — advisor, executor, a fresh relief —
  reaches it in one Bash call. It travels with `git pull` like everything else.
- **The failure mode is drift, and the design closes it**: the automation-contract
  pattern (generated files are never hand-edited; the generator is committed; every
  fold regenerates; a verifier gates). A DB that could disagree with the record would
  be a second authority — forbidden by construction.

## The schema — the record's actual ontology

| table | rows are | key columns |
|---|---|---|
| `rulings` | every numbered ruling and sub-ruling | arc, number, date, one-line holding, file, anchor, supersedes / superseded_by |
| `laws` | the CLAUDE.md / kickoff law corpus | statement, what it was paid for by, file, anchor |
| `experiments` | E01… | question, status, verdict, spec file, report file |
| `handoffs` | every executor dispatch + halt | number, date, commits, one-line outcome |
| `artifacts` | meshes, pairs, twins, sheets, atlases | path, sha, kind, status (accepted / rejected / superseded / measurement-record), provenance ruling |
| `phenomena` | the named measured effects | name, statement, instances with files (resemblance channel, seed-dependent binding, frame-changes-register, byte-vs-pixel, prose-is-not-registry…) |
| `decisions` | an INDEX over the profiles' registry | subject, tool, key, value, status, ruling — **the profile stays canonical**; this table only makes it searchable |
| `fts` | full-text over all prose columns | — |

## The tool and the ritual

- `tools/facet_index.py build` — parses the record by its own regular conventions
  (numbered ruling headers, law blocks, handoff sections, report headers) into the DB.
  Idempotent; a rebuild from an unchanged record is byte-identical.
- `tools/facet_index.py verify` — the external-verifier pattern: row counts against
  the record's own counts, zero dangling file/anchor pointers, and a seeded
  question set (N questions whose answers are known lines in the record — the index
  must return the right pointer for every one). A build that fails verify does not
  commit.
- **The ritual**: every advisor fold ends `build` + `verify` (the loadout-refresh
  pattern), so the index is never stale by more than the fold that is being written.
- **The context protocol**: kickoffs and CLAUDE.md stop inlining state. CLAUDE.md
  keeps the laws of working; profiles keep the values (they already do); the kickoff
  keeps the live-session pointer and the reading list — and everything else is
  `python tools/facet_index.py q "<term>"`.

## Phases

1. **P1 — build it against the existing record** — ✅ **DONE 2026-08-07**
   ([E15-report.md](experiments/E15-report.md),
   [E15-ruling.md](experiments/E15-ruling.md)): `tools/facet_index.py`
   (build/verify/q) + `docs/index/facet.db`. All four verify legs pass at two
   seats' hands — byte-identity across interpreters, zero dangling over 1,079
   rows, counts against independent greps, 14/14 seeded. The honest boundary is
   E15-report §5; it is P2's worklist.
2. **P2 — slim the entry documents against it**: the kickoff and CLAUDE.md shed
   inlined state that the index now answers; measure the shed (lines
   before/after). QUEUED — advisor-led, the Director's timing. Also reduces the
   measured self-reference (the E15 kickoff outranks answers for its own
   question labels).
3. **P3 — the standing ritual** — ⚖ **RULED 2026-08-07** (E15-ruling Ruling 4):
   **every advisor fold ends `build` + `verify`** — the seeded gate re-runs
   every fold, because it is measured growth-sensitive (a question that passed
   at 2,444 FTS rows missed at 2,475) · **the DB file commits at SESSION
   boundaries**, not every fold — the measured cost (~5.9 MB of
   poorly-delta-ing binary per build) against tonight's fold cadence decides
   the trade; staleness is bounded at one session and freshness is one
   deterministic `build` away · **kickoffs carry
   `python tools/facet_index.py build` right after `git pull`**. The index is a
   derived artifact forever; the day it is hand-edited it is wrong by
   definition.

## What this does not change

The markdown record's authority · corrections-in-place · the profiles as the value
registry · the experiments discipline · anything about how artifacts are judged. The
index is a map of the record, never the record — same law as the handbook.
