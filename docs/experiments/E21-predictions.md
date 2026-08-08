# E21 — blind predictions

**Written 2026-08-08 by the executor, BEFORE opening `main()` in either
`tools/facet_index.py` or `tools/record_mcp.py`, and before writing a single
test.** Committed ahead of the work per the dispatch
([E21-cli-contract-kickoff.md](E21-cli-contract-kickoff.md), "Predictions —
committed BEFORE any internals are read").

Blindness is disclosed **per row**, the E19/E20 precedent, with one kind added
because this arc's surface is unusually observable from outside:

- **L** — **LOOKUP**. Measured or read before the row was written. Not a
  prediction, not scoreable as one.
- **P** — **BLIND** on the code the row concerns.
- **S** — **SEMI-BLIND**. Reasoned from an *observed external surface* — a
  `--help` transcript, a `def` signature line, a test fixture constant, a
  protocol constraint — rather than from the implementation. An S row is weaker
  evidence than a P row and is scored in its own band. Claiming "I predicted the
  parser shape" after reading its `--help` output would be a hit bought with a
  lookup.

## What had been read when these were written

- `CLAUDE.md` in full; the E21 dispatch in full.
- `SHIP_GATE.md`: every `- [ ]` line (34, 42-47, 55, 57, 64, 68-69, 94) and the
  five checked `[mcp]`/`[cli]` lines (36, 44, 45, 54, 56).
- The four version declarations, by grep: `pyproject.toml:7`, `package.json:3`,
  `bin/facet.js:23-24`, `tools/record_mcp.py:134` — all `0.1.1`.
- **All of `tests/`** that bears on exit codes: `conftest.py` and
  `mcp_support.py` in full, `test_t13` in full, `test_t06` in full, the
  docstrings of `test_t27` and `test_t28`, and a grep of every `returncode` /
  `exit_code` / `SystemExit` / `sys.exit` occurrence in the suite. **The
  dispatch instructs this explicitly** ("check `tests/` for that before
  predicting"), so every row about an existing test is **L**, not a prediction.
- The *output* of `facet_index.py --help` and of `record_health`, both run at
  session start.
- The top-level `def` / `class` **name-and-line listing** of both tools —
  signature lines only, from `grep -n "^def \|^class "`. No bodies.

**NOT read: `main()` in either file, the argparse construction, `CODES`,
`RecordError`, `_raise`, `run_verify`, `parse_verify`, `build`, `verify`,
`claims`, or any `print` site.**

---

## P0 — the session-start gate (LOOKUP, not a prediction)

| id | statement | kind |
|---|---|---|
| **P0** | The index gate (`build` then `verify`, 19/19, four legs, run against a scratch `--db` because the record mount is live on this working copy) was **not** predicted before being run. It is step one of the session. Its pass is a measurement. | **L** |

Stated because a gate that passes is the easiest thing in a session to
retroactively claim you saw coming.

---

## U1 — the exit-code registry

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P1** | An **uncaught** exception in `facet-index` exits **1** today — CPython's default for an unhandled traceback — not 2. So the current mapping is inverted at *both* ends, not one: user error exits **2** (argparse) and runtime error exits **1** (CPython). SHIP_GATE.md:42 names only the argparse half of the inversion. | **P** | If runtime errors already exit 2, the gate line understated how close the surface already was, and half of U1 is a rename rather than a change. |
| **P2** | `facet_index.py` uses **one flat parser with a `choices`-constrained positional**, not `add_subparsers`. One `error()` override is therefore sufficient; no per-subparser propagation is needed. | **S** | The `--help` transcript shows `{build,verify,q,claims}` as a positional with all four options on the same parser. If subparsers are present anyway, `--help` renders them indistinguishably from choices here and that transcript was not the evidence I took it for. |
| **P3** | `record_mcp.py` likewise has **no subparsers** (`--db`, `--print-tools` only). **Two** `ArgumentParser` subclass sites total across the repo, one per command. | **S** | Weaker than P2: I have this command's surface only from SHIP_GATE.md:54's quoted transcript, not from running it. |
| **P4** | Edited sites **inside `main()`**: **3 in `facet_index.py`** (parser construction, dispatch wrapped, `--debug` added) and **3 in `record_mcp.py`** (the same three). New module-level definitions: **2 per file** (parser subclass + structured-failure printer), possibly folded to 1. **Total: 6 edited sites, 3-4 new definitions, and zero edits outside the two named files.** | **P** | A number materially above this means `main()` does more dispatch work than a 40-line / 17-line body suggests, and the "two commands, one contract" framing was too clean. |
| **P5** | The two files **do not share a new module**. Each carries its own copy of the parser subclass, because `record_mcp.py` is frozen into a standalone binary (T28's subject) and a new cross-file import is a packaging risk that neither T27 nor T28 currently covers. | **P** | If a shared `tools/cli_contract.py` is both correct and safe here, my model of the frozen-binary constraint is over-cautious and the duplication I am about to write was avoidable. |
| **P6** | `facet_index.py verify` exits **1** on a failed leg today. | **S** | `tests/mcp_support.py:47` sets `FAILED_PARSE["exit_code"] = 1`, and that module's own docstring says the dict is "the shape that parse produces". If the live value is not 1, the fixture has been encoding a wrong constant and T20/T21 have been driving the health state machine off it. |
| **P7** | `facet_index.py claims` exits **0** whatever it finds — agreeing with E15 Ruling 9b's binding on `record_claims`, which the dispatch restates as still binding. | **P** | If the CLI verb already exits non-zero on a contradiction while the MCP tool is ruled never to, the two surfaces have been disagreeing about the same measurement. That is a finding, not merely a miss. |
| **P8** | **Nothing partial-succeeds; `3` stays unused.** The one candidate I expect to have to argue is `verify` with 3 of 4 legs passing. I predict the report concludes that is a *measured outcome of a completed run*, not a partial completion, and that **no partial-success path is invented to populate the code**. | **P** | If something genuinely partial-succeeds, the dispatch's own "what is already true" row is falsified — the seventh inherited claim to fall in this repo. |
| **P9** | There is **no exit path distinct to a fired ANDON** in `facet_index.py` today. An ANDON leaves through the same failure exit as any other refusal. | **P** | If ANDONs already carry their own code, U1 question 1 is a naming question rather than a design one. |
| **P10** | Occurrences of the literal token `ANDON` in `tools/facet_index.py`: **5-15**. | **P** (quantity) | Far more means the refusal surface is denser than a 2,042-line tool with four verbs suggested, and "which code does an ANDON deserve" touches more sites than the report will have budgeted. |

---

## U2 — no raw tracebacks without `--debug`

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P11** | An uncaught exception during **serving** in `facet-mcp` never reaches `main()` — the MCP framework catches it and the process stays up, which is what SHIP_GATE.md:44 measured live. U2's top-level handler in `record_mcp.py` therefore guards only the **pre-serve** path (`--print-tools`, `--db` resolution, startup) plus the one path where serving itself returns. **Its blast radius is strictly smaller than `facet_index.py`'s.** | **S** | Reasoned from the gate item plus the stdio-protocol constraint, not from code. If an exception does escape to `main()` during serving, the `[mcp]` "server never crashes on bad input" item is narrower than it reads. |
| **P12** | `--debug` can be made **presentation-only in both commands without touching a single gate**, because no refusal in either file consults a verbosity or debug variable today. **Zero** conditional-on-flag edits inside any refusal or ANDON. | **P** | A non-zero count would mean the E08 A32 no-skip-flag ruling is harder to honour than the dispatch assumes, and `--debug` is not the cheap presentation change it looks like. |

---

## U3 — logging levels

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P13** | `tools/record_mcp.py` contains **8 or fewer** `print(` call sites, and **all** of them sit outside the serving path — in `_print_tools()` and `main()`. Reason: an MCP stdio server that writes to stdout corrupts its own JSON-RPC stream, so the serving path *cannot* print. | **S** | Protocol constraint, not code. If the serving path prints to stdout, either the transport is not what it says or the prints go to stderr, and "stdout is the measurement record" does not transfer to this command at all. |
| **P14** | Consequently **a quiet mode for `facet-mcp` is close to vacuous** — there is almost nothing on stdout to quiet. The honest U3 answer for that command governs a startup banner and little else. | **S** | If `facet-mcp` has real chatter to suppress, U3 is a genuine feature there rather than a formality, and the interesting half of the unit is the one I expected to be trivial. |
| **P15** | `tools/facet_index.py` contains **100-160** `print(` call sites. | **P** (quantity) | The count is the cost of any level-aware emitter. Materially more and "levels govern progress only" stops being a small edit. |
| **P16** | `verify()` (lines 1745-1972, 228 lines) holds **40-70** of them, and **60% or more** of those print a measurement or a refusal rather than progress. | **P** (quantity) | If most of `verify`'s prints are progress, the standing "stdout is the measurement record" reason is weaker than the record claims and a quiet `verify` is affordable after all. |
| **P17** | **NO for `verify`** — a quiet mode cannot be added there without touching lines that print a measurement, because `verify`'s stdout *is* the measurement record (the four legs, the per-table counts, the 19/19, the determinism leg that held). **YES for `build`**, and it costs **about one line in `main()`**. | **L** on the `build` half — `build(db_path, quiet=False)` at line 1125 already carries the keyword, read from the signature listing. **P** on the one-line cost and on the whole `verify` half. | If `verify` can be quieted without touching a measurement line, its prints are already separated by kind and the tension the dispatch asks me to resolve does not exist in the code. |
| **P18** | The boundary the report proposes will be exactly the shape the dispatch calls "likely honest": **levels govern progress and diagnostic chatter; they never govern a measurement, a refusal, or an ANDON.** I predict I find **no** reason to depart from it. | **P** | A miss here is worth more than a hit: it would mean looking at the real print census produced a boundary the advisor had not anticipated, which is the whole reason the executor looks rather than the advisor deciding. |

---

## Existing tests, and what this arc can move

| id | statement | kind |
|---|---|---|
| **P19** | **No existing exit-code assertion moves.** Every one in the suite sits on a success path: `conftest.py:208` (`build` → 0), `test_t13:36` (two concurrent `verify` → 0), `test_t20:239` and `test_t22:194` (`exit_code == 0` read from inside a *tool result body*, not a process exit). `test_t18:66` asserts pytest's own `USAGE_ERROR` from the interpreter probe and `test_t06:19` a git subprocess rc — neither is a facet command. | **L** — measured, not predicted |
| **P20** | **One fixture constant is exposed and no assertion is:** `tests/mcp_support.py:47`, `FAILED_PARSE["exit_code"] = 1`. It cannot fail today because nothing asserts it against a live failing run. If the advisor rules a failing `verify` to 2 or 3, that constant and `parse_verify`'s handling of it both move. **Prediction (P): I leave it untouched and report it as a finding, because U1 question 2 is the advisor's to rule, not mine.** | **L** on the constant; **P** on the outcome |
| **P21** | Assertions on `facet_index` **stdout text** that a default-level change would break: **2-6** across the suite (`test_t13:39`'s `last_nonempty(out) == PASSED_LINE` is one; I expect at least one more in T1). I predict **zero** of them break, because `--quiet` ships opt-in and the default level is unchanged. | **P** (quantity) |

---

## The commit this arc lands

| id | prediction | kind |
|---|---|---|
| **P22** | New test files: **2** (T29, T30). New test functions: **18-30**. At least **6** are can-fail legs whose only job is to prove the discriminating assertion discriminates — a test that cannot fail is this repo's most-repeated defect and the dispatch names it. | **P** |
| **P23** | The version bump is **5 string edits across 4 files**: `pyproject.toml:7`, `package.json:3`, `bin/facet.js:23` (`version`) **and `:24` (`tag`)**, `tools/record_mcp.py:134`. T27 gates the agreement, so a partial bump fails the suite in under a second rather than after a tag is already immutable. | **L** |
| **P24** | CI stays green with **no workflow edit** — the paths gate already covers `tools/**`, `tests/**`, `pyproject.toml`, `package.json`, `bin/**`. | **P** — the dispatch asserts the last three and I have not opened `.github/workflows/ci.yml`; this row predicts the inherited claim holds *and* that the first two are covered |
| **P25** | The arc produces **2-5 findings under the assertion law** — current behaviour that looks wrong and halts into the report rather than being pinned or silently fixed. At least one is the double inversion in P1. | **P** |

---

## Scoring

Each row is scored HIT / MISS / VOID in
[E21-cli-contract-report.md](E21-cli-contract-report.md), with the measurement
that settled it. **L** rows are excluded from the hit rate by construction and
listed separately; **S** rows are scored in their own band. Retuning a
prediction after seeing the result is the one move that is always wrong, and
this file is committed before the first `main()` is opened so that it cannot be.
