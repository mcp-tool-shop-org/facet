# E22 — blind predictions

**Written 2026-08-08 by the executor, BEFORE opening a single file under `tools/` or
`tests/`.** Committed ahead of the work per the dispatch
([E22-gates-not-asserts-kickoff.md](E22-gates-not-asserts-kickoff.md), "Predictions —
committed BEFORE opening any tool").

Blindness is disclosed **per row**, the E19/E20/E21 precedent, with one kind added
because this arc's central census already exists in prose and can be checked by
arithmetic before any code is read:

- **L** — **LOOKUP**. Measured or read before the row was written. Not a prediction,
  not scoreable as one.
- **P** — **BLIND** on the code the row concerns.
- **S** — **SEMI-BLIND**. Reasoned from an observed external surface — a ruling's
  quoted table, a protocol constraint, a language rule — rather than from the
  implementation. Scored in its own band.
- **D** — **DERIVED**. Arithmetic on numbers already in the record. Not a prediction
  about the world; a check of the record. Excluded from the hit rate, reported
  separately.

## What had been read when these were written

- `CLAUDE.md` in full; the E22 dispatch in full; `docs/experiments/E21-ruling.md` in
  full; `docs/experiments/E21-predictions.md` in full (read for the house format —
  it carries incidental structural facts about two of the seven in-scope files, and
  every row that leans on one is marked **L** or **S** below).
- The **output** of `facet_index.py build` and `facet_index.py verify` against a
  scratch `--db`, run at session start.
- Nothing else. **NOT read: any file under `tools/`, any file under `tests/`,
  `SHIP_GATE.md`, `CHANGELOG.md`, `README.md`, `.github/workflows/`, or any file in
  the four must-not-move trees.**

---

## P0 — the session-start gate (LOOKUP, not a prediction)

| id | statement | kind |
|---|---|---|
| **P0** | The index gate — `build` then `verify` against a scratch `--db` because the record mount is live on this working copy — returned **19/19, all four legs, exit 0**, and the determinism leg that held was byte-identity. It was **not** predicted before being run. Its pass is a measurement. | **L** |

Stated because a gate that passes is the easiest thing in a session to retroactively
claim you saw coming.

---

## U1 — the census, which the dispatch orders verified rather than inherited

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P1** | `tools/` holds **exactly 294** `assert` statements across **exactly 72** files, reproducing the ruling seat's census cell-for-cell. Nothing in `tools/` has moved since E21 except `facet_index.py` and `record_mcp.py`, and E21 added a contract wrapper rather than assertions. | **P** | A drift in either number means the ruling's census was taken against a different tree state than the one E22 converts, and every per-tool number below inherits that drift. |
| **P2** | "**Bare** assert" in the ruling means *a plain `assert` statement*, message or not — not *an assert lacking a message*. Counting only message-less asserts gives a materially smaller number: **60–120**. | **S** | Ruling 2's own sentence — "one bare `assert` gate in a shipped command" — is about construction, not about the message. If 294 turns out to be the message-less count, the assert population in `tools/` is far larger than the arc has budgeted for and the ~207 out-of-scope figure is wrong. |
| **P3** | The five-tool ANDON census reproduces cell-for-cell: **8 / 4 / 15 / 35 / 24** as asserts and **0 / 0 / 1 / 1 / 1** as raises. | **P** | Any cell that moves is the one to distrust in the ruling, and it is the cell whose tool most needs re-reading before conversion. |
| **P4** | Those cells sum to **86, not 87**. The dispatch's "87 ANDON-carrying assert sites" and Ruling 2's "one environment variable removes 87 of them" are an **arithmetic slip of the table they cite** — 8+4+15+35+24 = 86 — not evidence of a site the table omits. The in-scope set is therefore **88**: 86 + `facet_index.py`'s inverse-discovery guard + `record_mcp.py`'s `assert code in CODES`. | **D** on the sum; **P** on "the cells are right and the total is the slip" | If a sixth ANDON assert exists outside the five tools, or one cell is 9 rather than 8, then 87 was right and the table is what is wrong — and I will have corrected the record in the wrong direction. |
| **P5** | The write path — `texpass_iter.py` + `texpass_finalize.py` — is **12 of the 88**, and it is the only part of the set where a fired gate stands between the process and an irreversible write. | **D** | — |

---

## U2 — the 88 sites, and the shape of a pure move

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P6** | **86 of the 86** five-tool ANDON asserts carry a message, and **0** are bare conditions. Reason: the token `ANDON` is what *selected* them, and an `assert` statement has nowhere to carry a token except its message. | **S** (a language argument, not a code reading) | A non-zero bare count means the ruling's census matched on a trailing comment or an adjacent `print`, not on the assert's own message — in which case the selection criterion is looser than "the gate says ANDON" and the scope boundary needs restating before a line is converted. |
| **P7** | The two additional sites split: `facet_index.py`'s inverse-discovery guard **carries a message** containing the token; `record_mcp.py`'s `assert code in CODES` is **message-less**. So **87 of 88 carry a message, 1 does not.** | **P** | If `assert code in CODES` carries a message after all, the one site where I expect to write `raise AssertionError()` with no argument does not exist and the conversion is uniform. |
| **P8** | **Zero** functions anywhere in `tools/` contain an explicit `except AssertionError`. | **P** | A single one is the finding that decides the conversion's exception type, and it outranks my preference in P10. |
| **P9** | **Two** functions catch `AssertionError` *incidentally*, via a broad `except Exception`: E21's `run_contract` wrapper in `facet_index.py` and in `record_mcp.py`. Because `AssertionError` is a subclass of `Exception`, those two already swallow today's asserts exactly as they will swallow tomorrow's raises — **so they are not a behaviour risk; they are the reason the conversion is invisible from outside those two commands.** | **S** (from E21 Ruling 1's description of `run_contract`, not from its code) | If `run_contract` catches something narrower than `Exception`, converting `facet_index.py`'s guard changes what reaches the caller, and the "pure move" claim needs a per-file argument rather than a global one. |
| **P10** | **The conversion form, committed here so it cannot be chosen after seeing a failure:** every site becomes an in-place `if not <cond>: raise AssertionError(<msg>)`, with the condition and message expressions preserved **verbatim, character for character**. **No helper function is introduced**, no `AndonError` subclass, no message reworded, no condition tightened. `raise AssertionError` keeps the exception type identical to what `assert` produces, which the dispatch prefers absent a finding, and is the only form that is a pure move for a caller. | **P** (a commitment, scored on whether I hold to it) | Departing from this form mid-arc — even for a good reason — is the move the dispatch forbids, and the report must name the finding that forced it. |
| **P11** | Between **2 and 4** of the 88 conditions need parenthesising when negated (`if not (a and b)`), and **0** are the classic `assert (cond, msg)` tuple bug — CPython emits a `SyntaxWarning` for that construction, so it would have surfaced long ago. | **P** | A tuple-condition assert is a gate that has never been able to fire, which is the "check that cannot fail" law in its purest form, and it is a finding rather than a conversion. |
| **P12** | At least two of the five tools **import a shared helper module** inside `tools/` — most likely `e11_manifest.py` and `e11_export_turnaround.py`. Between **1 and 3** such shared modules exist. | **P** | *Before building a path to a resource, enumerate the resource* (E21 Ruling 9). If the five tools are five islands, a shared change is impossible; if they share a module, an ANDON I convert in one file may be reached from another, and the anchor set has to cover both callers. |

---

## U3 — the anchors

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P13** | **No anchor fails on the first conversion.** T7's byte-identity replay, T26's three fired ANDONs and the twin-projection anchor all reproduce, and **zero conversions are reverted.** The success path of an `assert` and of `if not: raise` are the same instructions, so no artifact byte can move; the only anchor with an exposed surface is T26, which observes the *failure* path. | **P** | If T7 or the twin-projection anchor moves a byte, something other than the assertion changed — a stray edit, a re-indent, an import — and the conversion is not the pure move it claims. That is a halt, not a fix. |
| **P14** | **T26 fires its three ANDONs in-process** and keys on the exception **type** — `pytest.raises(AssertionError)` or equivalent — not on a subprocess return code. It therefore passes unchanged **only because** P10 keeps the type, and would fail immediately against an `AndonError` subclass. | **P** | If T26 drives `texpass_finalize` as a subprocess and keys on a return code, then the exception type is unobserved by the suite, my main stated reason for preferring `AssertionError` is not load-bearing, and the type choice is free — which the report must say rather than letting P10 look validated. |
| **P15** | Test call sites across `tests/` that expect `AssertionError` **by type**: **4–8**. Three of them are T26's. | **P** (quantity) | Materially more means the suite has been treating `assert` as the repo's refusal contract far more broadly than the write path, and the blast radius of any future type change is wider than E22 measured. |
| **P16** | **Zero files in the four must-not-move trees change** across this arc — sha256-manifested before the first replay and re-checked at the halt, per the compensator note. The four trees are `facet_E04`, `facet_E08`, `facet_E13`, `facet_E14` under `E:\AI\training`, and the manifest covers **more than 2,000 files**. | **P** on the zero and on the file count; **S** on the four paths (from `CLAUDE.md`'s `E:\AI\training\facet_E0*\` line) | A single changed file is the compensator gap firing for real, and the restore has to happen inside this session — there is nothing to restore from in a later one. |
| **P17** | At least one anchor-bearing tool **has no output-path argument**, forcing a scratch replay through an environment variable or a working-directory change rather than a flag. I predict **exactly one** such tool, and that it is `texpass_finalize.py`. | **P** | The dispatch pre-routes this: no output-path argument is *a finding to report*, not a reason to point the replay at the tree. If every tool takes an output path, the compensator gap is smaller than the advisor scored it. |

---

## U4 — the ~207 out-of-scope asserts

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P18** | Of the ~207 non-ANDON asserts, **4** guard an irreversible step — a write into a citable tree, an atlas write, a `git` or network call — and are findings for the ruling rather than conversions. Band **2–6**. | **P** (quantity) | E21's calibration lesson is that this repo's density predictions run **~2× high**; my untutored estimate was 8–12 and I am halving it on that record alone. A number above 12 means the ANDON token is a poor proxy for "guards an irreversible step" and the scope was drawn on the wrong axis — which is a finding that outranks the conversion. |
| **P19** | **Zero** of the ~207 are converted in this arc. The count in the report is a census, not a diff. | **P** | — |

---

## U5 — Q2's exit code, folded in

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P20** | The dispatch's claim that **`parse_verify` keys on `rc != 0`, not `rc == 1`** holds, so moving a failing `verify` from `1` to `4` does not break the health state machine. | **P** — the dispatch asserts it and orders it verified before it is relied on | If `parse_verify` keys on `1`, the certificate's health state silently becomes "healthy" the moment `verify` starts refusing with `4`, and the exit-code change ships a broken artifact. That is a halt. |
| **P21** | `tests/mcp_support.py:47` currently reads `FAILED_PARSE["exit_code"] = 1` and must become `4`. | **L** — read from E21-predictions P20, not measured by me | — |
| **P22** | Code edits required for `4 = REFUSED`: **3–5** sites total, all inside the seven named files — a declared `EXIT_REFUSED = 4` constant, `verify`'s failing return, the fired-ANDON path, and the fixture constant. **No new module.** | **P** (quantity) | More than 5 means the exit value is threaded rather than returned, and E21's F3 understated how far the persisted certificate field reaches. |
| **P23** | The certificate's `verify_exit_code` field changes value **without a schema-version bump**, because the field's name and type are unchanged and only its domain widens. I predict the report *recommends* this and does **not** decide it — the schema is a shipped artifact and its version is the advisor's call. | **P** | — |

---

## U6 — the commit this arc lands

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P24** | **Gate 3's wording needs a reading, and I take the conservative one rather than improvising past it:** "no edit outside the seven named files" governs **tool code**. The dispatch itself requires edits outside those seven — "Tests ride the commit, starting at T30" and "`SHIP_GATE.md`'s B2 line is the gate item this closes" — so the intended set is *seven tool files + `tests/` + the named docs*. I predict I report this reading in the halt rather than treating it as a fired gate, and that **no tool file outside the seven is touched.** | **P** (a commitment) | If the advisor meant gate 3 literally, then T30 cannot be written and the dispatch contradicts itself — which is a finding for the ruling either way. |
| **P25** | New test files: **1** (T30). New test functions: **10–18**. At least **4** are can-fail legs proving the discriminating assertion discriminates. The suite goes **248 → 258–266**. | **P** (quantity) | E21 went 218 → 248 on two files; a comparable number here would mean per-gate tests were written per *site* rather than per *gate*, at 88 sites. |
| **P26** | The `-O` / `PYTHONOPTIMIZE=1` legs run as **subprocesses**, not in-process, because `__debug__` is fixed at interpreter start and cannot be toggled inside a running test. Between **2 and 4** such subprocess invocations of the pinned interpreter, each under 10 s. | **P** | If someone finds an in-process way to test this, my model of `__debug__` is wrong and the test is cheaper than I budgeted. |
| **P27** | The arc produces **3–6 findings** under the assertion law — current behaviour that looks wrong and halts into the report rather than being pinned or silently fixed. At least one concerns the 86/87 discrepancy in P4. | **P** | — |
| **P28** | **CI stays green with no workflow edit**; the paths gate already covers `tools/**` and `tests/**`, and both dependency scanners are indifferent to a control-flow change. | **P** | — |

---

## Scoring

Each row is scored HIT / MISS / VOID in
[E22-gates-report.md](E22-gates-report.md), with the measurement that settled it.
**L** and **D** rows are excluded from the hit rate by construction and listed
separately; **S** rows are scored in their own band.

Retuning a prediction after seeing the result is the one move that is always wrong,
and this file is committed before the first file under `tools/` is opened so that it
cannot be. **P10 in particular is a commitment, not a forecast** — it fixes the
conversion form ahead of the first anchor replay so that a failing anchor cannot be
answered by changing what "pure move" means.
