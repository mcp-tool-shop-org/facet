# E17 — the test harness: the record's run-once checks become a persistent suite

**Written by the advisor, 2026-08-08, at the Director's word — the session that starts
making tests.** Same-day context: the tests-ride-the-commit law entered CLAUDE.md
(`eccc827`) after the Director surfaced the deviation ("I assumed you were making tests
these past few days as we were building"). This repo has verified continuously — anchors,
in-tool invariance ANDONs, byte-replays, the four-leg index verify — but run-once and
recorded in reports: from a fresh clone exactly two checks re-run
(`facet_index.py verify`; `texpass_iter.py selftest`). **This session builds `tests/` +
CI and PORTS the existing checks into it.** It invents no new coverage, builds no MCP
servers, and retrofits nothing.

## You are the executor

```
cd E:\AI\facet && git pull
python tools/facet_index.py build          <- the E15 ritual (the seeded set is 19)
CLAUDE.md                                  <- read first, follow exactly — including the
                                              NEW tests-ride-the-commit law (this session
                                              runs under it)
docs/experiments/E16-errands-report.md     <- the anchors you are porting live here;
                                              VERIFY each against source before porting
                                              (dispatch text is hypothesis; report text too)
docs/experiments/E16-errands-kickoff.md    <- the anchor definitions as dispatched
```

⚠ **THIS IS A SHARED WORKING COPY AND E16 IS LIVE** at its final errand (E16-11, the
`_per_invocation` migration — it touches ALL FOUR PROFILES and their readers). Rules,
absolute: **file-specific `git add` only, never `-A`**; `profiles/`, `canon/`, the seeded
set, and E16's report/dispatch are OFF LIMITS to this session; concurrent verifies race
on the fixed determinism scratch (`facet.db.det_a`) — a PermissionError there is another
session's verify: retry once, flag it, never force; an index lock or staged files you did
not stage → stop and report; if an anchor mismatches on a file E16 just committed,
`git log` first — the record moves under you (it moved under two seats today). **Never
commit `docs/index/facet.db`** (session-boundary cadence, advisor-owned).

**Blind predictions first, committed**: per port — its tier (hermetic vs artifacts) and
expected pass state. A wrong prediction is a finding.

## Deliverable 1 — the scaffold

`tests/` + `conftest.py` + `pytest.ini`, with markers `artifacts` (needs the recorded
trees under `E:\AI\training\` — NOT in git, NOT in CI) and `slow`. `conftest` discovers
the artifact root from `FACET_ASSETS` (default `E:\AI\training`), and **every skip prints
its reason** — a silent skip is a check that cannot fail. pytest installs into the
trellis2-env if absent; the install is recorded in the report. **ASCII on every print
path** (the repo's law; E16-1 is why it is a law).

## Deliverable 2 — the seed suite (every test names its source)

| test | source | tier |
|---|---|---|
| T1 — build+verify wrapper: exit 0; the PASSED line read from its position, never matched in prose | the E15 ritual | hermetic* |
| T1b — encoding matrix: verify passes under default cp1252 AND `PYTHONIOENCODING=utf-8` | E16-1's anchor | hermetic* |
| T2 — `texpass_iter` selftest: exit 0 (styled byte-identical, delta 0.000000) | the tool's own selftest | hermetic |
| T3 — unprofiled `emit` refuses loudly, exits non-zero, message names the repair | E16-4's anchor | hermetic if the guard fires pre-load — verify that |
| T4 — ruling-doc discovery: the glob finds the current corpus; a synthetic undiscovered-file miss in scratch FAILS the run | E16-9; E15 Ruling 9a's inverse guard | hermetic |
| T5 — claims sweep: exits 0 always; 0 STALE on the current corpus; range-vs-cardinal, starts-at-1, and AMBIGUOUS semantics exercised on synthetic fixtures | E15 Ruling 8a; E16-9 | hermetic |
| T6 — line endings: no CRLF in tracked text files; `.gitattributes` present | E16-2 | hermetic |
| T7 — finalize replay: `atlas_final.png` byte-identical on the sword's recorded `run/final` inputs | E16-3's anchor | artifacts |
| T8 — `e08_ceiling` re-derivation: N6/N8 exact against 51.005% / 51.3342% | E16-6's anchor (thrice-matched) | artifacts |
| T9 — `e12_elevated` converged reach: the sword's 53.92% within ray-sampling noise | E16-7's anchor | artifacts |
| T10 — the bg-probe is report-only: projection outputs byte-identical on a recorded twin | E16-8's anchor | artifacts |
| T11 — edge-mode default byte-identity: stroke 1's recorded commit (4,344 texels) reproduced at `global`; `--edge-mode local` parses | E16-10's anchor | artifacts |

\* T1/T1b rebuild the derived DB in place and race `det_a` with live sessions — in CI
(fresh clone, no siblings) they are clean; locally they carry a `fold` marker and run
serially. If a scratch `--out` for the builder is the better shape, that is a TOOL
CHANGE: it carries its own tests in the same commit AND an anchor (default-path DB
byte-identical) — the new law and the E16 anchor discipline both apply. Propose it in
the report if it is not trivial.

**EXCLUDED, by name**: the E16-5 `mesh_stats` port — its anchor FAILED as dispatched and
awaits the advisor's ruling at the batch halt; it ports on that ruling, not before. The
E16-11 sweep port — only if E16-11 has committed by the time you reach it, with its
commit as the anchor.

**Porting rule**: prefer subprocess-level tests over restructuring tools for
importability. A test that needs a tool edit to exist gets the edit proposed in the
report, or made under the law (tests + anchor, same commit) — never silently.

### ⚠ AMENDED 2026-08-08 — E16 is RULED ([E16-ruling.md](E16-ruling.md)); four additions

- **T12 — the E16-5 repair, ruled at E16 Ruling 2**: `mesh_stats` warns on
  `rect_frac_of_figure > 1` and on nothing else (the proxy leg goes; the
  subject-class question lives in the profiles). ANCHOR, pre-stated by the ruling
  from measured values: every VALUE unchanged; W3 silent (0.680787); galleon
  silent (0.327707); beast silent (0.568773); the sword WARNS (1.902512). The
  warning's test rides the same commit.
- **T13 — the det_a race, ruled at E16 Ruling 3**: leg 1's temp paths become
  per-process unique (same directory). ANCHOR: leg 1 byte-identity unchanged on a
  quiet tree; the fixed-path collision impossible by construction. Test in the
  same commit.
- **T14 — the CODE_ROWS row, ruled at E16 Ruling 4a**: `texpass_iter`'s
  `edge-frac` enters the sweep's section-6 transcription as CODE (A3's derived
  law), matching `project_twins`' row verbatim; `edge-mode` stays SUBJECT-DATA.
  ANCHOR: the four profile sweeps' decided counts move only as this
  classification predicts, before/after quoted.
- **T15 — E16 and E17 arcs enter verify's count legs** with their own greps,
  sequence checks and completeness lines (the E15 Ruling 8b pattern) — if session
  budget allows, else the next errand window.
- **The E16-11 exclusion is LIFTED**: its port's anchor is commit `c284693`.
  The E16-5 exclusion above is superseded by T12's ruled specification.

## Deliverable 3 — CI

`.github/workflows/ci.yml` — the repo's FIRST workflow; the studio Actions rules bind:
`ubuntu-latest` only; `on.push.paths: [tools/**, tests/**, .github/workflows/**]` plus
`workflow_dispatch`; the required concurrency block; pinned minimal installs; **the
hermetic set only** (`-m "not artifacts"`). CI-green verification happens at the
advisor's push and lands in the ruling.

## Deliverable 4 — the report, then HALT

`docs/experiments/E17-harness-report.md`: the per-test table (source anchor → test node
id → tier → predicted vs measured), predictions scored, environment changes recorded,
every skip's printed reason shown, the full suite output quoted. Commits stay local
unless the advisor's fold has taken them. **HALT. The advisor rules at `E17-ruling.md`.**

## Explicitly NOT this session

No MCP servers (the index-MCP build is the NEXT session, on the E16 ruling, per Ruling
35's sequence). No new unit coverage over instrument internals (the polish arc's commits
carry that under the law, tool by tool as each is touched). No E16-5 port. No
profile/canon/fixture/palette/seeded-set edits. No memory-store writes. No packaging, no
versioning. Do not end a session the Director has not ended.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every port names its source anchor and recorded artifact; predictions committed blind before work; CI pins its installs |
| ANDON_AUTHORITY | 3 | a port whose expected pass FAILS is a finding — halt that item and report (E16-5 is the same-day precedent); T4 proves the inverse guard can fail before its green is trusted |
| NAMED_COMPENSATORS | 3 | all work is additive files, revertible per commit; any tool edit carries the anchor discipline; no publish, no spend |
| DECOMPOSE_BY_SECRETS | 3 | hermetic/artifacts tiers split by what each test needs; tests separate from tools; CI knows paths only |
| UNCERTAINTY_GATED_HUMANS | 2 | tier calls and tool-edit proposals go to the report for the ruling rather than being decided silently; skip: none — the open calls are named where they arise |
| EXTERNAL_VERIFIER | 3 | the suite is ports of checks authored by OTHER seats for OTHER purposes (E16's anchors, E15's gate, the selftest); CI is an independent runner on a clean clone |

## Calibration

The risk is green-lust. A port whose expected pass fails has FOUND something — halt that
item, report it, and never tune a test until it passes. The mirror risk is a check that
cannot fail: prove each guard-test fires on a synthetic miss before trusting its green.
A negative result is a full success.
