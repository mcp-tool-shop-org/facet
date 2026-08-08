# E21 — the installed CLI's operator contract: report

**Written by the executor, 2026-08-08, after the work.** Spec:
[E21-cli-contract-kickoff.md](E21-cli-contract-kickoff.md). Predictions, committed
before either `main()` was opened: [E21-predictions.md](E21-predictions.md) (commit
`f942d01`). **This report halts here. The advisor rules at `E21-ruling.md`.**

Nothing below judges whether the result is good. Three calls are explicitly the
advisor's and are presented as options with consequences, not as answers.

---

## What was done, in one paragraph

The exit-code registry's two unambiguous classes were implemented on both published
console scripts — **user error `1`**, **runtime error `2`** — and an unexpected
exception no longer reaches an operator as a raw traceback. `3` is declared and
unused, because nothing partial-succeeds. **Two outcome classes were deliberately
left at the codes they already had** — a failing `verify` leg and a fired ANDON —
because what they deserve is questions 1 and 2, and an executor picking a number for
them would be deciding what a result means. **Logging levels were not shipped**: the
dispatch reserved that boundary for the advisor to rule *before* it ships, so the arc
measured the census a ruling needs instead of guessing at one. Version → **0.2.0**.

---

## Gates

| gate | evidence |
|---|---|
| **1. Suite green before and after**, pinned interpreter | **before: `218 passed in 137.84s`**, exit 0. **after: `248 passed in 157.81s`**, exit 0. Command exactly as dispatched: `E:\AI-Models\trellis2-env\Scripts\python.exe -m pytest tests/`. One test failed mid-arc and it was T21's flag allowlist — see F7; it is the only pre-existing test this arc changed. |
| **2. MCP structured errors unchanged** | Fired **live** through a protocol client after the change: `limit=999` → `BAD_ARGUMENT` / *"limit must be between 1 and 50"*; `table="not_a_table"` → `BAD_ARGUMENT` naming all eight tables. Both carry `code`/`message`/`hint`/`retryable`/`error`, no traceback on the wire. **`record_health` answered normally in the same exchange** (`SERVING_STALE`, `serving=true`) and `list_tools` returned the same six tools. No tool result shape changed; `main()`'s edits are confined to argument parsing and the process's own exit. |
| **3. Four version declarations agree** | `pyproject.toml:7`, `package.json:3`, `bin/facet.js:23` + `:24` (`tag: "v0.2.0"`), `tools/record_mcp.py:134` — all **0.2.0**. T27's 11 tests pass, including `test_t27_all_four_version_declarations_agree` and its own can-fail leg. ⚑ **The bump was 7 edits, not the 5 I recorded as a lookup** — `bin/facet.js` also carries the version twice in the comment that documents the asset names it derives. See P23. |
| **4. No edit outside scope** | `git diff --name-only -- tools/` returns exactly **`tools/facet_index.py`** and **`tools/record_mcp.py`**. `canon/`, `profiles/`, the citable trees, the seeded set and every closed ruling are untouched (`git diff --stat` over them is empty). `docs/index/facet.db` and its certificate are **not** modified — the session-start index gate ran against a scratch `--db`, per the shared-copy discipline. |

**Index gate at session start:** `build` + `verify` on a scratch DB — four legs, **19/19** seeded, `VERIFY PASSED`, determinism leg `byte-identity`.

---

## Predictions, scored

25 rows. **L** rows are lookups and are excluded from the rate by construction; **S**
rows scored in their own band.

### P — blind on the code (14 scoreable)

| id | claim | verdict | what settled it |
|---|---|---|---|
| **P1** | uncaught exception exits **1**, so the mapping is inverted at *both* ends | **HIT** | measured, 20 rows: user error 2, runtime 1 **with a raw traceback**. SHIP_GATE.md:42 had named only the argparse half |
| **P4** | ~3 edited sites per `main()`, 2 new defs per file, 6 + 3-4 total, zero edits outside the two files | **MISS** | containment held (only the two tool files). Counts did not: **7 new functions/classes and 6 new constants in `facet_index`, zero new definitions in `record_mcp`** — the asymmetry is P5's miss showing up as a count |
| **P5** | the two files do **not** share a module; each carries its own copy | **MISS, and the instructive one** | `record_mcp` has imported `facet_index` since it was written — it calls `facet_index.verify()` in-process. The shared contract cost **one** definition and **zero** new files. I reasoned about frozen-binary packaging risk for a dependency that was already there and already frozen. *Before building a path to a resource, enumerate the resource* — the repo's own law, and I did not apply it |
| **P7** | `claims` exits 0 whatever it finds | **HIT** | `claims()` has a single `return 0`; its own banner reads *"REPORT-ONLY; always exits 0"* and *"This verb never gates: exit 0"* |
| **P8** | nothing partial-succeeds; `3` unused; `verify`-3-of-4 is the candidate to argue | **HIT** | ten-row sweep returns only {0,1,2}; the candidate was exactly that one and it is argued in Q3 below |
| **P9** | no exit path distinct to a fired ANDON | **HIT** | it was an uncaught `AssertionError` — identical treatment to any crash |
| **P10** | `ANDON` token appears **5-15** times in `facet_index.py` | **MISS** | **2**, and one is a docstring line. I predicted a denser refusal surface than a 2,042-line tool with four verbs has |
| **P12** | `--debug` presentation-only; **zero** conditional-on-flag edits inside any refusal | **HIT** | AST walk: the identifier `debug` is read in exactly two functions, both of which decide what gets *printed* after a failure is already decided. A fired gate still refuses with `--debug` set (tested) |
| **P15** | `facet_index.py` holds **100-160** `print(` sites | **MISS** | **61** |
| **P16** | `verify()` holds 40-70 of them, **≥60%** measurement-or-refusal | **SPLIT** | count **35** (miss). Composition **stronger than predicted**: 19 measurements + 6 refusals = **25/35 = 71.4%**, and the remaining 10 are separators, a banner and leg headers — **zero are progress chatter** |
| **P18** | the proposed boundary is the dispatch's own shape, with no reason to depart | **HIT, with an addition the dispatch did not anticipate** | the boundary holds — and the census shows the set it governs is **nearly empty**, which changes what shipping it would be worth. See U3 |
| **P21** | 2-6 stdout-text assertions on `facet_index`; **zero** break | **SPLIT** | **17** (T01 7, T05 6, T04 2, T13 2) — miss on the count by ~3×. Zero broke: hit, and the reason is that `--quiet` was not shipped and no default moved |
| **P22** | 2 new test files, 18-30 functions, ≥6 can-fail legs | **SPLIT** | **1** file (T29), not 2 — U3 shipping nothing removed the second file's subject. **20 `def test_`, 30 collected** (in band). **6** explicit can-fail legs plus embedded ones: hit |
| **P25** | 2-5 findings under the assertion law | **MISS (over)** | **7**. F2 alone was worth the arc |

**P band, 14 rows: 6 HIT · 5 MISS · 3 SPLIT.** Every one of the five clean misses is a
**quantity** — a count of print sites, a count of ANDON tokens, a count of edited call
sites, a count of findings, and a shared-module prediction that was really a count of
files. Not one is a miss about *behaviour*. E20's lesson was "predict quantities, not
negligence"; this arc predicted quantities and was bad at them, which is the more
useful failure of the two and the one that says my model of this codebase's density
runs about 2× high.

### S — semi-blind, reasoned from an observed external surface (6)

| id | claim | verdict | what settled it |
|---|---|---|---|
| **P2** | `facet_index` is one flat parser with a `choices` positional; one `error()` override suffices | **HIT** | `ap.add_argument("verb", choices=[...])`; no `add_subparsers` anywhere |
| **P3** | `record_mcp` has no subparsers; **two** subclass sites repo-wide | **MISS on the count** | no-subparsers held; **one** `ContractParser`, shared. Same root as P5 |
| **P6** | a failing `verify` leg exits **1** | **HIT** | `verify()` has `return 1` / `return 0`; measured at exit 1 with three rulings deleted from a copy |
| **P11** | a serving exception never reaches `facet-mcp`'s `main()`; smaller blast radius | **HIT** | garbage on stdin → process exits **0**, no traceback; the framework absorbed it |
| **P13** | `record_mcp` has **≤8** `print(` sites, all outside the serving path | **HIT** | **4**, all inside `_print_tools()` |
| **P14** | a quiet mode for `facet-mcp` is near-vacuous | **HIT** | there is nothing on stdout to quiet; see U3 |

**S band: 5 HIT · 1 MISS.** The band is weaker evidence by construction, and it shows: the S rows that hit were reasoned from a *protocol constraint* or a *transcript*, and the one that missed (P3) was a count inferred from a shape.

### L — lookups, not predictions

**P0**, **P17**'s `build` half, **P19**, **P20**'s constant, **P23**.

**P19 held exactly:** no existing exit-code *assertion* moved — all four sit on success paths. **P20 held:** `mcp_support.py:47`'s `FAILED_PARSE["exit_code"] = 1` is untouched and is reported below rather than changed.

⚑ **P23 was recorded as a lookup and it was wrong.** I stated *"5 string edits across 4 files"*, measured by grep. The bump took **7**: `bin/facet.js` carries `0.1.1` twice more, in the comment documenting the asset names — and my grep pattern (`version|VERSION|tag|TAG`) could not match `//   binary:    facet-0.1.1-linux-x64`. **A lookup is supposed to be a measurement, and this one was a measurement of the wrong thing.** It cost nothing here because T27 gates the agreement and the comment is inert, but the lesson is the repo's: *check what your instrument is made of before the first result depends on it.*

---

## U1 — the exit-code registry

### The matrix, measured through a subprocess, before and after

| command | outcome class | before | after |
|---|---|---|---|
| `facet-index` | ok — `--help`, `q`, `q` with no rows, `claims`, a passing `verify`, `build` | **0** | **0** |
| `facet-index` | user error, argparse — unknown verb · no args · unrecognised flag · non-int `--limit` | **2** | **1** |
| `facet-index` | user error, hand-rolled — `q` with no term | **2** | **1** |
| `facet-index` | runtime error — corrupt DB, on `q` / `verify` / `claims` | **1** + raw traceback | **2**, structured, no traceback |
| `facet-index` | **a leg of `verify` failing** | **1** | **1** — *unchanged, question 2* |
| `facet-index` | **a fired ANDON** | **1** + raw traceback | **1**, `GATE_FIRED`, message kept, no traceback — *code unchanged, question 1* |
| `facet-mcp` | ok — `--help`, `--print-tools` | **0** | **0** |
| `facet-mcp` | user error, argparse — unrecognised flag · flag missing its value · stray positional | **2** | **1** |
| `facet-mcp` | garbage on stdin while serving | **0**, process survives | **0**, process survives |

**Before the change, three distinct outcome classes shared exit 1** — a measured
failure, an unexpected crash, and a fired gate — while the operator's own mistakes
sat on 2. **After it, two still share 1**, and that overlap is the direct consequence
of leaving questions 1 and 2 to the advisor. It is named rather than hidden: exit 1
now nominally means *user error*, and two classes that are not user errors are
squatting on it until the ruling moves them.

### Implementation

One shared block in `facet_index.py` (`EXIT_*`, `ContractParser`, `user_error`,
`debug_requested`, `_report_failure`, `run_contract`, `prog_name`), imported by
`record_mcp.py`, which has imported that module since it was written.

Two choices worth stating because they were not obvious:

- **`ContractParser` overrides `error()` and deliberately not `exit()`.** `--help`
  reaches the operator through `exit(0)`; an override there would move a success onto
  a failure code. Measured: every argparse usage failure in both commands routes
  through `error()`, so one override covers the class.
- **`run_contract` wraps `main()` itself, not the `__main__` guard.**
  `[project.scripts]` binds `facet-index = facet_index:main`, so setuptools' generated
  wrapper calls that function directly. A contract in the `if __name__` block would be
  present in a source-tree run and **absent from every installed command** — which is
  the exact surface this arc is about. `main()` is now a two-line entry point and the
  body moved to `_main()`.
- **`prog` is still derived from `argv`, not hardcoded.** A source checkout says
  `facet_index.py`; an installed command says `facet-index`. T28's lesson, applied:
  advice that does not follow the runtime is wrong advice.

---

## U2 — no raw tracebacks without `--debug`

An unexpected exception now leaves as:

```
facet_index.py: RUNTIME_ERROR
  message: file is not a database
  cause:   DatabaseError
  hint:    re-run the same command with --debug for the traceback
```

and a fired gate as `GATE_FIRED`, carrying its own `ANDON:` text and the hint *"this
is a gate refusing, not a defect in the tool. Fix what it names; there is no flag that
skips it."*

**`--debug` is presentation-only, and that is proven three ways rather than asserted:**

1. **Same exit code** with and without, on the identical failing command (2 → 2).
2. **Same side effect** — `build` run under each writes a **byte-identical** artifact.
   (Bytes are the right instrument here specifically: the build is byte-deterministic
   by contract, so the bytes *are* the claim. This is the narrow exception to the
   repo's "a PNG hash mismatch is not evidence" law, and it is exercised as one.)
3. **Confined by AST**, not by intention: the identifier `debug` is read in exactly
   `run_contract` and `_report_failure`, and in no function of `record_mcp` at all.
   That check carries its own can-fail leg, because an AST walk that silently returned
   an empty set would make the guard vacuous.

Plus the behavioural one that matters most: **a fired gate still refuses with
`--debug` set** (`test_t29_debug_does_not_skip_the_gate`). E08 Amendment 32 exists
because a construction that *could* walk past a fired gate did.

---

## U3 — logging levels: not shipped, and the census that a ruling needs

The dispatch's own words are the reason: *"Propose the boundary explicitly and name
which existing prints fall on each side; **the advisor rules the boundary before it
ships.**"* So this unit measured and stopped.

### The census — 61 print sites across both commands

| function | sites | what they are |
|---|---|---|
| `verify()` | **35** | 3 separators · 1 banner · 6 leg headers · **19 measurements** · **6 refusals/verdict**. **Zero progress lines.** |
| `claims()` | 20 | the whole report. Its own banner: *"REPORT-ONLY; always exits 0"* |
| `_main()` (the `q` verb) | 3 | 2 print query results, 1 was the hand-rolled user error (now `user_error`) |
| `build()` | 2 | 1 progress (`[build] <path>`) · 1 the per-table counts |
| `record_mcp._print_tools()` | 4 | the surface listing |
| **`record_mcp`'s serving path** | **0** | — |

### The proposed boundary

**Levels govern progress and diagnostic chatter. They never govern a measurement, a
refusal, or an ANDON.** The dispatch called this the likely honest shape and I found
no reason to depart from it. What the census adds is that **the set it governs is
nearly empty**, and two things it did not anticipate:

- **The objection to a quiet `verify` is now mechanical, not philosophical.**
  `record_mcp.run_verify` calls `facet_index.verify()` **in-process** under
  `contextlib.redirect_stdout` and `parse_verify` is pinned to specific print sites
  (T20 asserts every pattern against a real transcript). **A quiet `verify` breaks the
  certificate.** "stdout is the measurement record" is, for this tool, a live
  dependency of a shipped artifact.
- **A quiet mode for `facet-mcp` governs an empty set.** Its serving path prints
  nothing — a stdio server that writes to stdout corrupts its own JSON-RPC stream — so
  the only candidate is `--print-tools`, which is a verb whose entire purpose is to
  print.

Which leaves `build` as the one verb with a genuine progress line. It **already**
carries a `quiet=` keyword and `record_build` already uses it. Note for the ruling:
`build`'s second print is the per-table **counts**, which the boundary calls a
measurement — but `build()` *returns* those counts, so suppressing the print does not
suppress the measurement. Whether that distinction ("a measurement with another
channel may be quieted") belongs in the boundary is part of what is being ruled.

**Redaction:** stated and testable rather than built. Nothing sensitive is printed by
either command — A3's sweep found zero credential-shaped matches in the tree, and
neither command reads a credential at any level.

---

## The three questions, with options and consequences

### Q1 — what exit code does a fired ANDON deserve?

Currently, and after this arc: **1**, unchanged. **But the measurement raised a prior
question, and it is F2 below: the gate can be switched off from the environment.** A
code assigned to a gate that `PYTHONOPTIMIZE=1` removes is a code for an event that
may not occur. The two are entangled; which to rule first is the advisor's call.

| option | consequence |
|---|---|
| **a. `1`, unchanged** | an ANDON is indistinguishable by exit code from a mistyped flag. A wrapper that treats 1 as *"operator error — fix the arguments and retry"* retries forever against a fired gate |
| **b. `2` (runtime error)** | says the tool broke when the tool worked. Merges the gate with genuine crashes, so *"did the gate fire or did sqlite die"* becomes unanswerable from the code |
| **c. `3` (the reserved code)** | the only free integer in the registry, and *"completed, and refused"* is arguably nearer partial than either error. Cost: the registry's own name for 3 says *partial success*, so `SHIP_GATE.md`'s line would read wrong; and it competes with Q2(c) for the same integer |
| **d. a fifth code (e.g. `4` = gate fired)** | cleanest semantically. Cost: extends the registry past what the ship gate names — a documented deviation from the standard rather than compliance with it |
| **e. `0`** | listed only to be excluded: a gate that exits 0 is E08 Amendment 32's failure mode restated |

### Q2 — is a failing `verify` a 1, a 2, or a 3?

Currently, and after this arc: **1**, unchanged. **A constraint the dispatch did not
have (F3):** `verify()`'s return value is not only a process exit code. `record_mcp`
calls it in-process and writes the value into **`verify_exit_code` of the
schema-versioned certificate** (`facet-record-index-certificate/1`), which
`record_health` serves. Moving it moves a persisted artifact's field.

Mitigating measurement: `parse_verify` keys on `rc != 0` (record_mcp.py:429/432/435),
**not** on `rc == 1`. So the health state machine survives any non-zero choice
unchanged. The cost of moving it is confined to three places: the certificate field's
value on a failing run, the fixture constant `mcp_support.FAILED_PARSE["exit_code"]`,
and any operator script keying on 1.

| option | consequence |
|---|---|
| **a. `1`, unchanged** | shares the user-error code. A caller cannot distinguish *"you typed the wrong flag"* from *"the record's index failed a leg"* — the difference between fix-your-command and **do not trust this index** |
| **b. `2` (runtime error)** | says the tool broke; it did not, it measured. Collides with genuine crashes |
| **c. `3` (partial success)** | the most defensible reading of the registry as written: `verify` completed, ran all four legs, and reports which passed. Cost: populates the code this report otherwise records as unused, changes a certificate field's value, moves one fixture constant — and competes with Q1(c) |
| **d. a dedicated code** | same registry-extension cost as Q1(d) |

`claims` is **not** in this question: E15 Ruling 9b binds it to never return a failing
code, it already exits 0 by construction, and this arc did not touch it.

### Q3 — does anything genuinely partial-succeed?

**No.** A ten-row sweep across both commands returns only {0, 1, 2}, asserted in
`test_t29_the_partial_code_is_declared_and_never_returned` (with a can-fail leg
requiring the sweep to have produced ≥3 distinct classes, so its silence is not empty).

Candidates considered and rejected:

- **`verify` with 3 of 4 legs passing** — it *completed*; a failing leg is a measured
  outcome of a finished run, not a partial completion. (This is a different question
  from Q2(c): the advisor may assign `3` to it as a *code* without agreeing that
  `verify` partially succeeded.)
- **`q` returning fewer rows than `--limit`** — the query completed; there were that
  many rows.
- **`build`** — one transaction by contract. The DB is written or it is not.
- **`claims`** — report-only by ruling.

**No partial-success path was invented to populate the code.** `EXIT_PARTIAL = 3` is
declared, documented as unused, and pinned as never returned.

---

## Findings under the assertion law

Behaviour that looks wrong is reported here, not pinned and not silently fixed.

### F1 — the inversion was two-ended, not one

`SHIP_GATE.md:42` named argparse's `2 = usage error`. Measured: **uncaught exceptions
exited `1` with a raw traceback** — CPython's default — so the registry was inverted at
both ends. Found by running the matrix rather than by reading the gate line. Corrected
in place; both ends now match the registry.

### F2 — the ANDON is a bare `assert`, and an environment variable removes it ⚑

`facet_index.py:186`, the inverse discovery guard, is a bare `assert`. Measured, with a
control, on the same tree:

| run | ANDON fires | exit |
|---|---|---|
| clean tree | no | 0 |
| stray handoff present | **yes** | 1 |
| stray handoff present, `python -O` | **no** | **0** |
| stray handoff present, **`PYTHONOPTIMIZE=1`** | **no** | **0** |

`-O` is an interpreter flag a console-script user never types. **`PYTHONOPTIMIZE=1` is
an environment variable, and it reaches an installed command.** Under it the guard goes
silent, the build **exits 0**, and it writes an index that omits the stray dispatch —
a silently incomplete record with a success code.

**This is E08 Amendment 32's own failure mode landing on the repo's own gate:** a check
that a scripting accident can separate from the action it gates. There the separator
was a PowerShell chain; here it is the interpreter. *A gate that a scripting accident
can separate from the action it gates is not a gate.*

**Not fixed in this arc**, because the assertion law says behaviour that looks wrong
halts into the report. **Not pinned by a test either** — a test asserting
"`PYTHONOPTIMIZE=1` disables the gate" would anchor a defect. The repair is one line
(raise rather than assert). The same construction appears at `record_mcp.py:189`
(`assert code in CODES` inside `RecordError.__init__`); under `-O` an unnamed error
code would pass silently. That one is a developer guard rather than an operator gate,
so its consequence differs, but the construction is identical.

### F3 — `verify()`'s return value is a persisted artifact field

Not only a shell's `$?`. It is written to `verify_exit_code` in `<db>.cert.json`,
schema `facet-record-index-certificate/1`, and served by `record_health`. Bears
directly on Q2, and is the reason this arc did not move it even provisionally.

### F4 — the certificate is built by **parsing `verify`'s stdout**

`run_verify` captures it with `contextlib.redirect_stdout`; `parse_verify` is pinned to
named print sites and T20 asserts each against a real transcript. So for this tool,
*"stdout is the measurement record"* is a **live mechanical dependency of a shipped
artifact**, not only a principle about evidence. Bears on U3.

### F5 — the suite reads `facet_index`'s stdout 17 times

T01 7 · T05 6 · T04 2 · T13 2. A change to the *default* output level would break the
suite; an opt-in flag does not (measured — 248 pass). Bears on U3 and on how any level
scheme must be defaulted.

### F6 — the tracked certificate carries `server_version: "0.0.0"`

`docs/index/facet.db.cert.json`, `verified_utc 2026-08-08T18:40:36Z`, while
`SERVER_VERSION` was `0.1.1` when it was read. `write_certificate` records the
*current* constant (record_mcp.py:482), so the tracked certificate was written before
the extraction attached a real version and has not been regenerated since. A consumer
reading `server_version` from the tracked certificate reads a placeholder.
**Out of scope and not touched** — the DB + certificate commit as a pair at a session
boundary, and this arc does not move them. Named so the next regeneration is known to
be owed.

### F7 — T21's closed flag allowlist widened by exactly one

`test_t21_there_is_no_skip_flag` asserts `opts <= {"--help", "--db", "--print-tools"}`.
It is the guard whose whole purpose is to make a new flag on the refusing command
expensive, and it failed on `--debug` — correctly. **It was the only pre-existing test
this arc changed.** The allowlist admits `--debug` and nothing else, in writing, on a
stated condition, and the same test now *checks* that condition with an AST walk
proving `record_mcp` branches on `--debug` nowhere. Recorded here because widening a
guard to admit one's own change is the move that must never be quiet.

---

## Tests added — they ride this commit

**`tests/test_t29_cli_contract.py`** — 20 functions, **30 collected**, all green.

- **Exit code per (command × outcome class)**, asserted through a **subprocess**. An
  exit code is a property of a *process*; `main()` returning 2 is a different claim
  from the command exiting 2, and setuptools' wrapper is what turns one into the
  other — which is precisely why the contract had to move into `main()`.
- **A can-fail leg for every code.** `..._the_user_code_discriminates`,
  `..._the_runtime_code_discriminates`, `..._user_and_runtime_are_different_codes`
  (which asserts the *identities*, because a test that only checked "they differ"
  would have passed on the inverted surface), `..._the_andon_check_can_fail`,
  `..._the_failing_verify_check_can_fail`, `..._the_debug_confinement_check_can_fail`.
- **`--debug` changes only presentation**: same exit code, byte-identical artifact,
  traceback in one and absent in the other, and confined by AST to two functions.
- **An ANDON still fires and still refuses** — at the only levels that exist (normal
  and `--debug`), and with `--debug` set. What is **not** asserted is its exit
  *integer*, because that is unruled and pinning it would anchor it.
- **A failing `verify`** reports `VERIFY FAILED`, prints its `X` evidence lines, and
  carries no traceback — again without asserting its integer.

**`tests/test_t21_record_mcp_health.py`** — the allowlist widening (F7), plus the new
AST condition attached to it.

**T28's frozen-binary path is not regressed** — its 5 tests pass unchanged, and the
one thing this arc did that could have touched it (`prog`) was deliberately left
argv-derived for exactly T28's reason.

---

## Standards compliance (this arc)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every number here names how it was measured; the interpreter, the suite command, the four version sites and the twenty matrix rows are literal. The measurement scripts are re-runnable and the matrix was run before *and* after |
| ANDON_AUTHORITY | 3 | four gates checked with evidence; U3 halted into a census rather than shipping a boundary the dispatch reserved; two exit codes left unruled rather than picked; F2 halted into a finding rather than being fixed or pinned |
| NAMED_COMPENSATORS | 2 | this arc performs **no irreversible act** — no publish, no tag, no release. Compensator for the behaviour change is `git revert` of this commit plus a 0.2.1; for the version bump, the four sites are gated by T27 and release.yml so a partial revert fails loudly. Scored 2: stated, not exercised |
| DECOMPOSE_BY_SECRETS | 3 | scope held to *what is published*. The contract lives in one module because the two commands already shared one — the decomposition followed the existing dependency rather than inventing a new file |
| UNCERTAINTY_GATED_HUMANS | 3 | the three questions are presented as options with consequences and no recommendation. Q1 additionally names the prior question F2 raised, because ruling a code for a gate that may not fire is the wrong order — that is structure, not a ruling |
| EXTERNAL_VERIFIER | 2 | outcomes are deterministic integers asserted through a subprocess rather than by reading source; the suite and CI verify the result. skip: no cross-family check — there is nothing here for one to grade |

---

## Owed, and named rather than dropped

- **The advisor's three rulings**, and F2's prior question with them.
- **README translations.** `README.md` changed (the threat-model correction and four
  stale counts). The studio rule is that translations run **before** any publish or
  GitHub release so the tag never carries stale ones. This arc performs no release, so
  they are not run here — but **whoever releases 0.2.0 must run them before the tag**,
  not after. `node E:/AI/polyglot-mcp/scripts/translate-all.mjs README.md`.
- **The DB + certificate regeneration** (F6), as a pair, at a session boundary.
- **U3's levels**, blocked on the boundary ruling, not on work.

---

## What this arc did not do

The 34 research scripts · `tools/diagnostics/` · `tools/superseded/` · the
`code`-as-closed-enum and `retryable` halves of the structured shape for `facet-index`
· the MCP JSON-schema per-parameter descriptions (want 9) · `record_build`'s
unexpected-exception wrapper extended to the other five tools (want 10) · the three
testability seams (E20 Ruling 6) · P5 · the release.

**Halt.** The advisor rules at `E21-ruling.md`.
