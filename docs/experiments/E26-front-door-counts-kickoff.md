# E26 — the counts nothing watches

**Written by the advisor, 2026-08-09, dispatched from [E20](E20-ruling.md)'s want 2 —
and RESHAPED by measuring it first.** Halts at `E26-front-door-counts-report.md`; the
advisor rules at `E26-ruling.md`.

**⚠ May run in parallel with [E25](E25-diagnostics-gates-kickoff.md). Read the
coordination section.**

---

## The question

The repo's stated test count has drifted on its public surfaces **four times in two
days**, once inside the very commit that fixed the previous drift. Every one was caught
by a person reading the page. What should watch it?

## ⚠ WANT 2, AS WRITTEN, WOULD NOT HAVE CAUGHT ANY OF THEM

E20's want 2 says *"the claims sweep still cannot see `CHANGELOG`/`SECURITY`/`SHIP_GATE`/
`SCORECARD`/`site/`."* That is true. **It is also not the defect.** Measured before this
was written:

```
claims() scans        record_markdown()  =  CLAUDE.md + README.md + docs/**.md
                      -> CHANGELOG, SHIP_GATE, SCORECARD, SECURITY, site/, README.*.md
                         are all invisible to it.                        CONFIRMED

CLAIM_FAMILIES        rulings-range · rulings-cardinal · amendments-cardinal
                      · addenda-cardinal · handoffs-range · handoffs-cardinal
                      · experiment-span
                      -> ZERO families mention tests.                    MEASURED

measurements(con)     reads ONLY the index: rulings, amendments, addenda, handoffs,
                      experiments.
                      -> A TEST COUNT IS NOT IN THE INDEX AND CANNOT BE, because the
                         index is a pure function of the CORPUS MARKDOWN and the test
                         count is a property of tests/.                  STRUCTURAL
```

**So widening the scan set catches nothing for a test count**, and the sweep cannot be
given a test-count family without a source of truth it does not have. An arc that only
widened the sweep would deliver a change that reports nothing new about the thing that
broke four times.

**The shape that works is already ratified in this repo.** [E23 Ruling 9](E23-ruling.md)
put a live-moving quantity — the remaining ANDON count — **under a test**, and that is
adopted as the pattern for exactly this: *a count under a test cannot drift silently,
because moving it requires editing the test on purpose.*

## The arc, in two separable halves

### Half A — the one that has bitten. Do this first.

**A hermetic test that pins every stated test count on every surface against the count
`pytest` actually collects.**

Surfaces that carry the claim today, measured at dispatch — **verify, do not inherit:**

```
README.md                                            two sites (a bullet, and Requirements)
SHIP_GATE.md                                         item D's verify-script line + its lineage
site/src/site-config.ts                              the "Tests ride the commit" card
site/src/content/docs/handbook/getting-started.md    two numbers
site/src/content/docs/handbook/reference.md          one number
README.{ja,zh,es,fr,hi,it,pt-BR}.md                  two each, digits only
```

**The truth is `pytest --collect-only`**, both tiers. How the test obtains it without
recursing into itself is the executor's to measure and report — a subprocess is the
obvious route and it is what T29/T30/T31 already do for exit codes and gates.

**Rule it must not break:** a *historical* count is not a drift. `CHANGELOG`'s released
entries state what a version shipped and are correct forever; `SHIP_GATE`'s lineage is a
list of past values on purpose. **The test pins current-state claims and must not fire on
a released entry** — which means it needs a stated rule for telling them apart, and that
rule is a finding for the ruling if it turns out to be ambiguous.

### Half B — the original want 2, now correctly scoped.

**Widen the SWEEP's scan set** so ruling/handoff/amendment/experiment counts stated on
`CHANGELOG.md`, `SHIP_GATE.md`, `SCORECARD.md`, `SECURITY.md` and the site handbook are
checked against the index the way `docs/**` already is.

**⚠ RULED, so the executor does not have to discover it:** `record_markdown()` feeds
**both** the index build **and** the sweep. **Do not extend `record_markdown()`.** Give
the sweep its own scan set. Measured reason: the candidates are **17 files / 2,768 lines
against a 254-file / 62,161-line corpus**, and **seven of them are non-English
translations** — putting that into an FTS5 index tuned for English moves prose rows, fts
rows and, most importantly, **the seeded set's rankings, which leg 4 gates on**. Risking
legs 1, 2 and 4 to improve a *report* is a bad trade, and the narrow change gets the same
result.

**The translations are bounded OUT of Half B** — the families match English phrasings and
a Japanese ruling-count claim is a different problem. Half A covers them, because digits
are digits. Say so in the report rather than silently skipping them.

## Predictions — committed BEFORE any source file is opened

`E26-predictions.md` first, blindness disclosed per row. Predict at least: how many
surfaces carry a test-count claim (a property of an **enumerated** set — count it); how
many *historical* counts Half A must not fire on; whether any surface's claim is currently
wrong at HEAD; and how many new STALE rows Half B's widening produces on the first run.

**Both calibration laws bind.** E22: *check the population is real.* E23: *check the
metric's unit* — "surfaces carrying the claim" counts **sites**, not files, and README
alone has two.

## Gates

1. **Suite green before and after**, full artifacts tier. Baseline **384** *(E25 may move
   it — measure your own and say what it was)*.
2. **Half A's test FAILS on a deliberately stale surface** and passes at HEAD. A test that
   passes on a broken tree is not testing this — E24's gate 3, and its tier had to be
   repaired for exactly this reason.
3. **Half A does not fire on a historical count.** Demonstrate against `CHANGELOG`'s
   released entries and `SHIP_GATE`'s lineage.
4. **`record_markdown()` is unchanged**, and the four verify legs still pass — run
   `build` + `verify` against a scratch `--db` before and after and report both.
5. **CI green**, both dependency scanners. If CI fires on the environment rather than the
   result, [E23 Ruling 2](E23-ruling.md) governs.
6. **No edit to anything E25 owns** (below).

## ⚠ Parallel coordination

E25 may be live in this working copy. Verified disjoint at dispatch:

| | E25 owns | E26 owns |
|---|---|---|
| tools | `diagnostics/*`, `verify/*` | `facet_index.py` (Half B only) |
| tests | `test_t31_route_gates.py`, **T33** | **T34+** |

- **File-specific `git add`, always. Never `git add -A`** — the other arc's uncommitted
  work is in this tree.
- **`git fetch origin && git merge --ff-only origin/main` before every push**, *not*
  `pull --rebase`: rebase refuses outright while another session has unstaged changes, and
  `--autostash` would stash **their** work. A non-fast-forward means disjointness broke —
  **halt and report.**
- **T-numbers are a shared namespace and nothing allocates them** (E25's dispatch found
  this the hard way when T32 was taken mid-arc). **Take T34; if it is taken, take the next
  free number and say so** rather than renumbering anyone.
- A defect found in E25's files is **reported, not fixed**.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the sweep's scan set, its seven families, `measurements()`'s sources and the corpus sizing are all measured and quoted; the surfaces carrying the claim are enumerated |
| ANDON_AUTHORITY | 3 | six gates; gate 2 is the strong form (fail on a stale tree first), gate 4 protects the four verify legs from a reporting change |
| NAMED_COMPENSATORS | 3 | every file this arc touches is in git and `git revert` is a real undo; **no recorded tree is touched at all**, which is why this scores above the last three arcs rather than beside them |
| DECOMPOSE_BY_SECRETS | 3 | the arc is split by **source of truth** — Half A's truth is `pytest`, Half B's is the index — which is also why one is a test and the other is a sweep change |
| UNCERTAINTY_GATED_HUMANS | 3 | the current-vs-historical rule, the translations boundary and any ambiguity in what counts as a current-state claim are pre-routed to the ruling |
| EXTERNAL_VERIFIER | 2 | the verifier is `pytest --collect-only` in a subprocess and the index's own four legs — neither of which the author can talk past. skip: no cross-family LLM; every outcome is an integer comparison |

## Out of scope

Extending `record_markdown()` (ruled above) · adding non-English family patterns · the
132-site diagnostics conversion (E25's) · T28's two assertions ([E24 Ruling 4](E24-ruling.md),
a separate small arc) · P5 · **the release**.

## Environment

- Everything under the **absolute** pinned interpreter
  `E:\AI-Models\trellis2-env\Scripts\python.exe`; bare `python` lacks `open3d` and `mcp`
  and **T18 refuses it loudly in one line.**
- Shared working copy, possibly with a second live session — see coordination. DB +
  certificate commit as a **pair**, at a session boundary only, and **not at all if E25's
  seat has already folded it.**
- **ASCII prints.** CI is paths-gated. **Never leave CI red.**

## Halt

`E26-front-door-counts-report.md`: predictions scored with blindness disclosed, the
enumerated surfaces and which were wrong at HEAD, Half A's test with its stale-tree
evidence and its historical-count evidence, Half B's new STALE rows with a disposition for
each, the four legs before and after, findings, tests added, gates with evidence.
**Then stop.** The advisor rules at `E26-ruling.md`.
