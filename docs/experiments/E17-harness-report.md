# E17 — the test harness: report

**Executor session, 2026-08-08.** Dispatch:
[E17-harness-kickoff.md](E17-harness-kickoff.md), **amended in place mid-session** by
[E16-ruling.md](E16-ruling.md) Ruling 6 — the amendment landed at `31409d9` while this
session's first artifacts run was executing, and this report covers both the original
twelve ports and the amendment's T12–T15. Blind predictions were committed at `eca32b0`
before any tool was read; they are scored in §4.

**The suite's end state: 27 tests, 27 passed** (19 hermetic, 8 artifacts), full output
quoted in §6. Zero skips on this rig; the skip path demonstrated with printed reasons
in §7. Six commits, all local, listed in §9.

> **⚠ SUPERSEDED IN PART, 2026-08-08** — the ruling landed and assigned this session a
> final leg (T15b, T18). Sections 1–9 stand as written and are the record of the halt;
> the **addendum at §10–12** carries the leg. Current suite end state: **32 tests, 32
> passed** (24 hermetic, 8 artifacts). Flag 5 and the T18 finding are closed there;
> flags 1, 2, 3, 4, 6, 7 were disposed by the ruling itself (§8 keeps the original
> wording so the dispositions can be read against what was flagged).

---

## 1. The record moved under this session, three times

The dispatch warned that this is a shared working copy, and it was, throughout:

1. **Between this session's `git pull` and its first fresh `git status`**, E16-11
   committed (`c284693`) and the E16 report closed (`abe62a9`). The dispatch's
   conditional — "the E16-11 sweep port, only if E16-11 has committed by the time you
   reach it" — was therefore resolved IN before the first port. That port is
   `test_t16_registry_sweep.py` (T16; the predictions doc had called it T12 before the
   amendment claimed that id).
2. **While the first artifacts run was executing**, the advisor ruled E16 (`31409d9`):
   the E17 kickoff gained T12–T15, and three profiles changed in the same commit
   (prop.json's `converged` annotation — prose only, no applied value; character.json's
   `bg-max-pct` withdrawn to a suspension; ship.json's inert duplicate removed). The
   ruling's own fold also re-ran sweeps and verify in this working copy during this
   session's runs. Checked when the two artifacts failures appeared: `git diff` on the
   profiles showed no applied-value change, so neither failure traces to the fold
   (§3 has what they do trace to).
3. **`docs/index/facet.db`** was rebuilt by both seats and stays uncommitted here, per
   the dispatch (advisor-owned, session-boundary cadence).

## 2. Per-test table

| id | source anchor | test node id | tier | predicted | measured |
|---|---|---|---|---|---|
| T1 | the E15 ritual (four-leg verify, seeded 19) | `test_t01_index_verify.py::test_t01_build_and_verify` | hermetic, `fold` | PASS | **PASS** — exit 0, last line `VERIFY PASSED - all four legs` read from its position, `19 / 19`, determinism leg byte-identity, both discovery-corpus audits printed; since T15 also asserts the E16 count legs green |
| T1b | E16-1's anchor (Ruling 31f) | `...::test_t01b_encoding_matrix[utf-8]` / `[cp1252]` | hermetic, `fold` | PASS both | **PASS both** — both encodings forced explicitly (see §5: the rig's ambient `PYTHONIOENCODING` is `utf-8:surrogateescape`, so an inherit-the-default leg would have tested utf-8 twice; the forced matrix is load-bearing on every platform) |
| T2 | the tool's own selftest; E16-4's table | `test_t02_selftest.py::test_t02_selftest_write_head_lossless` | **artifacts** (dispatched hermetic — FINDING, §4) | tier hermetic / state PASS | **PASS** — exit 0, `max delta 0.000000`, last line `[selftest] PASS`, committed 377 = E16-4's recorded count (reported, not asserted) |
| T3 | E16-4's anchor (Ruling 29c) | `test_t03_emit_guard.py::test_t03_unprofiled_emit_refuses` + `::test_t03_control_explicit_aspect_passes_the_guard` | hermetic | PASS, guard fires pre-load | **PASS** — refuses on NONEXISTENT `--state`/`--prep` with the ANDON naming `--profile`/`--aspect`/Ruling 29c, which is the pre-load proof (a post-load guard would FileNotFoundError instead); the control run passes the guard with explicit `--aspect` and fails downstream WITHOUT the ANDON text — the message assertion can discriminate |
| T4 | E16-9; E15 Ruling 9a's inverse guard | `test_t04_discovery_guards.py` (4 tests) | hermetic | PASS; misses FIRE | **PASS** — discovery covers the corpus with the arc labels the derivation must preserve (`E10-offsurface` not merged into `E10`); a truncated ruling-doc list makes in-process `verify` return 1 printing `ROWS FROM UNDISCOVERED FILES` naming the dropped file; `assert_no_undiscovered_handoffs` raises its ANDON on a truncated list naming `E15-context-index-kickoff.md` — E16-9's injection method verbatim, no decoy files in the shared tree |
| T5 | E15 Ruling 8a; E16-9/-11 | `test_t05_claims_sweep.py` (2 tests) | hermetic | PASS; semantics exercised | **PASS** — exit 0 always (exercised WITH a synthetic STALE present), 0 STALE on the current corpus; on monkeypatched synthetic documents over the real scratch DB: range→max vs cardinal→count (E12's own handoffs-1–16-but-15-exist case), `Rulings 21-23` produces neither a row nor an unparseable (starts-at-1), `at least` routes to AMBIGUOUS, the same wrong cardinal is STALE in README.md and as-of-writing in a kickoff path |
| T6 | E16-2 | `test_t06_line_endings.py` (2 tests) | hermetic | PASS | **PASS** — `.gitattributes` tracked with the `* text=auto eol=lf` pin; `git ls-files --eol` shows no `i/crlf`, `w/crlf`, or mixed on any tracked text file, with parse-broke guards (row count, known file present) |
| T7 | E16-3's anchor (Ruling 31d.1) | `test_t07_finalize_replay.py::test_t07_finalize_reproduces_the_recorded_atlas` | artifacts, `slow` | PASS | **PASS** — `atlas_final.png` byte-identical to the recorded artifact (compared file-to-file, no sha literal); the three recorded inputs re-hashed unchanged after the run; `finalize.json` also byte-identical to the recorded one (reported) |
| T8 | E16-6's anchor, thrice-matched — **with its dispatch correction** | `test_t08_ceiling.py::test_t08_n6_n8_exact` | artifacts, `slow` | PASS against N6 = 1,871,948 / N8 = 1,879,807 (NOT the dispatch's 51.005%) | **PASS after an operand correction (§3.2)** — N6 1,871,948 and N8 1,879,807 exact, valid 3,661,903, head band 1,894,691, at the RECORDED floors 0.45/0.45 with the collapse NOTE asserted and the configuration selected via `settings_index` by property, never by caption |
| T9 | E16-7's anchor (Ruling 10a) | `test_t09_elevated.py::test_t09_repaired_default_reaches_the_recorded_value` | artifacts, `slow` | PASS within ±0.5 of 53.920; sharper: exactly 53.967 on this rig | **PASS** — measured **53.967%**, the sharper prediction to the digit; invocation carries E16-7's `--fit-axis height` correction |
| T10 | E16-8's anchor (Ruling 21e) — with its dispatch correction (the probe is NOT report-only; the ANDON is armed only by character.json) | `test_t10_projection.py::test_t10_projection_reproduces_stage1b` | artifacts, `slow` | PASS, five outputs byte-identical | **PASS** — the recorded six-view stage1b invocation (views 0/1/3/4/5/7; y+090 and y+270 were inputs to nothing) reproduces all five outputs byte-identical to the recorded `stage1b_*` artifacts |
| T11 | E16-10's anchor (Ruling 24c) | `test_t11_edge_mode.py` (2 tests) | artifacts | PASS — 4,344 byte-identical; local parses | **PASS after an operand correction (§3.1)** — commit.log reproduced verbatim (trust 32,040, wrote 4,344, holes 2,005,056 → 2,000,712); holes/styled_mask/atlas.prev byte-identical to the recorded s1b; the raw commit atlas matches `collar_repair.json`'s own recorded `atlas_sha256_before` to the last digit; `--edge-mode local` runs and reports **5,675** texels — E16-10's measured number exactly |
| T12 | E16 Ruling 2 (the E16-5 halt, ruled) — amendment | `test_t12_mesh_stats.py::test_t12_honest_warning_condition` | artifacts, `slow` | (post-prediction scope) | **ANCHOR HELD** — before/after JSON identical on all four subjects (every value unchanged); warning states exactly the ruling's pre-stated table: W3 0.680787 silent, galleon 0.327707 silent, beast 0.568773 silent, longsword 1.902512 WARNS; the proxy message gone. Tool edit + test in one commit (`dbe6497`) |
| T13 | E16 Ruling 3 (the twelfth errand) — amendment | `test_t13_det_race.py::test_t13_concurrent_verifies_do_not_collide` | hermetic, `fold` | (post-prediction scope) | **ANCHOR HELD** — per-process temp names; verify PASSED with leg-1 byte-identity before and after the edit; the ruled collision case runs as the test: two simultaneous verifies on the SAME scratch DB both PASS with byte-identity, zero det temps left. Tool edit + test in one commit (`45de927`) |
| T14 | E16 Ruling 4a — amendment | (rides `test_t16_registry_sweep.py`) | hermetic | (post-prediction scope) | **ANCHOR HELD** — before: 85 subject-data flags, value 66; after: **84**, value 65, on all four profiles; beast/ship exit 0 at 84/84, prop exit 1 with exactly its pre-existing 1 UNDECIDED, character exit 1 with 18; `_per_invocation` untouched (3/3/3/1). Sweep edit + the T16 pin moved 85→84 in one commit (`e75f1a8`) |
| T15 | E17 amendment ("if session budget allows") | asserts inside `test_t01` | hermetic | (post-prediction scope) | **HALF-EXECUTED, half deferred with its reason** — the E16 legs are in: greps for 7 numbered rulings + 18 lettered sub-rulings (the fold's own 25 rows) and the sequence bound 1–7, all green inside verify; T1 asserts the legs present-and-ok without pinning counts (grep==db stays verify's own invariant). The E17 half is DEFERRED: no `E17-ruling.md` exists and the E17 kickoff carries no handoff headers, so an E17 leg today would grep a file that is not there — the check-that-cannot-fail class. Commit `7fd4619` |
| T16 | E16-11's anchor, commit `c284693` (condition met before the first port) | `test_t16_registry_sweep.py` (5 tests) | hermetic | PASS against the committed table | **PASS** — asserted at 85 in the base-suite commit, moved to 84 in T14's commit; prop's single undecided named (`texpass_brush prompt`) so a NEW undecided cannot hide behind the count |
| **T15b** | E17 Ruling 3e — **appended 2026-08-08 after the ruling** | asserts inside `test_t01` | hermetic, `fold` | (post-ruling scope) | **ANCHOR HELD** — verify PASSED with `E17 numbered rulings grep 4 db 4 ok`, `E17 lettered sub-rulings grep 10 db 10 ok`, `E17 sequence ruling 1-4 gaps: none`. Counts verified against source **before** the legs were written (§10). Commit `5c81716` |
| **T18** | E17 Ruling 2 — **appended 2026-08-08 after the ruling** | `test_t18_interpreter_precheck.py` (5 tests) | hermetic | (post-ruling scope) | **ANCHOR HELD** — the wrong-interpreter run now exits `USAGE_ERROR` with one refusal naming the missing module, the interpreter run, the law's interpreter and the ruling, having run nothing; the trap reproduced and closed end-to-end (§11). Commit `ac0a1f2` |

## 3. Two first-run failures, both this session's operand errors, both diagnosed from the record

The first artifacts run finished **5 passed / 2 failed** (T8, T11). Per the dispatch,
the failing items halted and were diagnosed before anything was touched; both failures
were this session's own wrong operands, and in both cases the record itself adjudicated
the correction. **No anchor value was changed at any point.** The failing evidence, the
diagnosis chain and the re-run are all below because a report that hides its own first
run is the thing this repo exists to prevent.

### 3.1 T11 — the test pointed at stroke 1-A's abandoned job

First run: `wrote 5,416` against the recorded 4,344, trust mask 31,949 against 32,040 —
with the starting hole count matching exactly. Diagnosis, in order: `git log` first (the
dispatch's rule — the ruling had just landed; its profile diff is prose-only, not the
cause); then the operands. `run/state/atlas.png` is **byte-identical** to
`s1b/atlas.prev.png`, so the input state was right. The job was not:
`run/state/job_y+000_e+00` was emitted at 02:02 from the **post-demotion, pre-garnet**
state (stroke 1-A, abandoned; its `inpainted.png` even reproduces the recorded
diagnostic line to the digit while keying 91 px differently), while **s1b carries its
own job dir**, emitted 02:58–03:01 from the post-garnet state — the one the recorded
commit consumed. With s1b's job: commit.log verbatim, three outputs byte-identical to
the record, and the raw atlas equal to `collar_repair.json`'s recorded
`atlas_sha256_before` (`fa75204e…`) — the recorded `s1b/atlas.png` itself is
post-collar-repair (rewritten 03:42, Ruling 28d), which the sidecar pins from both
sides. A second finding rode along: **E16-10's "all four byte-identical" was
replay-vs-replay across its own tool edit**, not replay-vs-record; the ported test now
asserts strictly more of the record than the errand did.

### 3.2 T8 — the test inferred its invocation from a pre-repair caption

First run: N6 = 1,946,557 against the recorded 1,871,948 (+74,609). The tool's defaults
are floors 0.45/0.18; the recorded run's floors were **both 0.45** — which is exactly
what E16-6 reproduced ("all three SETTINGS blocks identical **while the run's floors
were both 0.45**") and exactly what the recorded `ceiling.json`'s three identical
blocks mean. This session read the recorded json's block captioned
`production (body 0.45 / head 0.18)` and inferred the invocation from it — **the
caption is the pre-repair lie E16-6 repaired**, preserved in a recorded artifact. At
`--head-facing-min 0.45` the repaired tool collapses the three settings to one block
with the NOTE, and N6/N8 land exact. The delta's mechanism is legible: the head band is
1,894,691 texels, and flooring it at 0.18 instead of 0.45 admits +74,609. The ported
test asserts the collapse NOTE and selects the configuration through `settings_index`
by its floors — the tool's own lesson, now also this harness's.

Both corrections are the repo's standing law firing on its newest instrument: *check
what the operands are, not just whether the arithmetic replays* — and its sibling from
the ruling landed the same day, *data is not a literal*.

## 4. Predictions, scored

Committed blind at `eca32b0` before any tool was read. The amendment's T12–T15 arrived
after the predictions and are outside their scope.

| prediction | verdict |
|---|---|
| pytest absent from trellis2-env, install recorded | **FALSIFIED** — pytest 9.1.1 already present; zero environment changes this session (§5) |
| no tool edit needed anywhere; `verify` accepts `--db`, dodging the det race with no tool change | **HELD for the dispatched scope** — `--db` is a global flag consumed by both verbs, exactly as predicted, and none of T1–T11/T16 needed a tool edit. The session then made four tool edits **because the amendment ruled them in** (T12–T15), each with tests in its commit — new scope, not a falsification |
| artifacts set runs with zero skips on this rig; skip path proven by absence | **HELD** — 0 skips in every local run; §7 shows the printed reasons |
| T1/T1b/T3/T4/T5/T6 tiers and pass states | **HELD**, all six — including T3's pre-load claim (proven via nonexistent inputs) and T4/T5's importability claims |
| T2 hermetic | **FALSIFIED — the informative miss.** `--state`/`--prep`/`--glb` are required recorded inputs; the repo tracks no fixture state. The tests-required law commit's words "only the index's four-leg verify and texpass_iter's selftest are re-runnable from a fresh clone" are **half right**: from a fresh clone the selftest cannot run at all. Ported at artifacts tier; whether a small in-repo fixture state should exist is the advisor's call — inventing one was explicitly out of scope |
| T2 pass state | **HELD** — PASS, delta 0.000000, and the committed count reproduced E16-4's 377 |
| T7 | **HELD** |
| T8 anchored on E16-6's corrected pair, not the dispatch's 51.005% | **HELD, and load-bearing** — porting the dispatch's number would have manufactured a failure E16-6 already explained. The first-run invocation error (§3.2) sits beside it: the prediction named the right numbers and this session still reached them wrongly the first time |
| T9 within ±0.5; sharper: exactly 53.967 on this rig | **BOTH HELD** — 53.967% to the digit |
| T10 byte-identical; if it mismatches, git log the profiles first | **HELD** (and the git-log-first move was exercised by T8/T11 instead) |
| T11 byte-identical at default; local parses, count reported not asserted | **HELD after §3.1's operand correction** — and the local mode's 5,675 reproduced E16-10's measured delta exactly |
| T16 (called T12 pre-amendment) hermetic, pinned to the committed table | **HELD** — including the tier call (the sweep is stdlib over repo files) |

Score on the dispatched ports: **11 held, 2 falsified** (pytest-present; T2's tier),
with both falsifications carrying the session's findings — the same shape as E16's
scoring, where the misses were the informative rows.

## 5. Environment, recorded

- **No environment changes.** pytest 9.1.1 was already in the trellis2-env.
- Versions the suite ran under (and CI pins): Python 3.13.13 (CI: 3.12, for open3d
  wheel availability at the pinned release — the one local/CI divergence, named in the
  workflow comment); pytest 9.1.1, numpy 2.4.6, scipy 1.17.1, pillow 12.2.0, trimesh
  4.12.2, open3d 0.19.0 (local build `0.19.0+241aaee`; CI pins the PyPI 0.19.0).
- **The rig's ambient `PYTHONIOENCODING` is `utf-8:surrogateescape`** — discovered when
  the harness's first hermetic run crashed decoding child output (the env value's
  `:errors` suffix was passed to `bytes.decode`; fixed in `conftest.run_py` before any
  port was judged — every first-run red in that run was the harness's own decode, not a
  tool). Consequence worth keeping: on this rig the "default" child encoding is utf-8,
  so T1b's decision to FORCE both encodings explicitly is what makes the cp1252 leg
  real here, not only on ubuntu.

## 6. The full suite, quoted (final run, both tiers)

```
=========================== short test summary info ===========================
PASSED tests/test_t01_index_verify.py::test_t01_build_and_verify
PASSED tests/test_t01_index_verify.py::test_t01b_encoding_matrix[utf-8]
PASSED tests/test_t01_index_verify.py::test_t01b_encoding_matrix[cp1252]
PASSED tests/test_t02_selftest.py::test_t02_selftest_write_head_lossless
PASSED tests/test_t03_emit_guard.py::test_t03_unprofiled_emit_refuses
PASSED tests/test_t03_emit_guard.py::test_t03_control_explicit_aspect_passes_the_guard
PASSED tests/test_t04_discovery_guards.py::test_t04_discovery_covers_the_current_corpus
PASSED tests/test_t04_discovery_guards.py::test_t04_ruling_doc_miss_fails_verify
PASSED tests/test_t04_discovery_guards.py::test_t04_handoff_guard_passes_on_the_real_set
PASSED tests/test_t04_discovery_guards.py::test_t04_handoff_guard_fires_on_a_synthetic_miss
PASSED tests/test_t05_claims_sweep.py::test_t05_current_corpus_zero_stale
PASSED tests/test_t05_claims_sweep.py::test_t05_semantics_on_synthetic_fixtures
PASSED tests/test_t06_line_endings.py::test_t06_gitattributes_present_and_pinning
PASSED tests/test_t06_line_endings.py::test_t06_no_crlf_in_tracked_text_files
PASSED tests/test_t07_finalize_replay.py::test_t07_finalize_reproduces_the_recorded_atlas
PASSED tests/test_t08_ceiling.py::test_t08_n6_n8_exact
PASSED tests/test_t09_elevated.py::test_t09_repaired_default_reaches_the_recorded_value
PASSED tests/test_t10_projection.py::test_t10_projection_reproduces_stage1b
PASSED tests/test_t11_edge_mode.py::test_t11_default_reproduces_stroke1
PASSED tests/test_t11_edge_mode.py::test_t11_local_mode_parses_and_runs
PASSED tests/test_t12_mesh_stats.py::test_t12_honest_warning_condition
PASSED tests/test_t13_det_race.py::test_t13_concurrent_verifies_do_not_collide
PASSED tests/test_t16_registry_sweep.py::test_t12_sweep_end_state[beast]
PASSED tests/test_t16_registry_sweep.py::test_t12_sweep_end_state[character]
PASSED tests/test_t16_registry_sweep.py::test_t12_sweep_end_state[prop]
PASSED tests/test_t16_registry_sweep.py::test_t12_sweep_end_state[ship]
PASSED tests/test_t16_registry_sweep.py::test_t12_prop_remainder_is_the_preexisting_one
======================== 27 passed in 93.44s (0:01:33) ========================
```

Reported values inside that run: T1 determinism leg **byte-identity**; T2 committed
**377** (= E16-4); T7 `finalize.json` **byte-identical** to the recorded one; T8 one
collapsed settings block `production = uniform body-floor = uniform head-floor
(body 0.45 / head 0.45)`; T9 **53.967%**; T11 local mode **5,675**.

The first runs, for the record: hermetic 18/18 in 10.30 s (after the conftest decode
fix; the run before it failed 13 tests on the harness's own `LookupError`); artifacts
first run 5/7 in 70.65 s with the two §3 failures; artifacts re-run 7/7 in 67.93 s.

## 7. Every skip's printed reason (the proof run)

`FACET_ASSETS=E:\no-such-training-root`, artifacts tier only — all eight skip, each
naming the missing root and the remedy; `-rA` keeps these in the summary always:

```
SKIPPED [1] tests\test_t02_selftest.py:25: artifacts tier: recorded-trees root not
  found at E:\no-such-training-root (set FACET_ASSETS; the trees live under
  E:\AI\training on the rig and are not in git, not in CI)
  ... (identical reason from test_t07:25, test_t08:37, test_t09:30, test_t10:34,
       test_t11:56, test_t11:81, test_t12:39)
====================== 8 skipped, 19 deselected in 0.03s ======================
```

A second skip shape exists and is narrower: `need()` skips naming one exact missing
file when the root exists but a recorded input inside it does not.

## 8. Flags for the advisor, decided by nobody here

1. **The CI paths gate is the dispatch's exact three** (`tools/**, tests/**,
   .github/workflows/**`) — `pytest.ini` sits outside it, so a pytest.ini-only change
   would not trigger CI. Widen or accept.
2. **No `pull_request` trigger** — the dispatch named push+dispatch only; the studio
   rules' PR-runs question is left to the ruling.
3. **CI python is 3.12 against the rig's 3.13** (open3d wheels at the pin). CI-green
   verification happens at the advisor's push per the dispatch; the sqlite-FTS5-on-CI
   assumption is verified by the same run.
4. **T2's tier finding** (§4): the law commit's "re-runnable from a fresh clone" claim
   is wrong for the selftest as it stands. If a hermetic selftest is wanted, it needs a
   small in-repo fixture state — a commissioning decision, not an executor improvisation.
5. **T15's E17 half** stays open until `E17-ruling.md` exists (§2 table row).
6. **E16-10's byte-identity anchor form** (§3.1): replay-vs-replay, where this suite
   now anchors replay-vs-record. No action needed — recorded so the next reader knows
   which claim is which.
7. Cosmetic: three commit messages (`e75f1a8`, `7fd4619`, `910a7c5`) carry doubled
   apostrophes from a here-string quoting slip. Content unaffected.

## 9. Commits, all local (unpushed)

| commit | contents |
|---|---|
| `eca32b0` | blind predictions, before any tool read |
| `e8ed958` | Deliverables 1+2: scaffold + the twelve ports (T1–T11, T16 at the pre-T14 pin) |
| `dbe6497` | T12: mesh_stats honest warning + riding test |
| `45de927` | T13: per-process det temps + riding test + marker-text update |
| `e75f1a8` | T14: edge-frac CODE row + the T16 pin 85→84 in the same commit |
| `7fd4619` | T15 (E16 half): count legs + sequence bound + T1's leg assertions |
| `910a7c5` | Deliverable 3: the first CI workflow, hermetic set only |

`docs/index/facet.db` remains uncommitted (advisor-owned). The pre-existing
`stash@{0}` was not touched. No profile, canon, fixture, palette or seeded-set edit;
no memory-store write; no push.

**HALT.** The advisor rules at `E17-ruling.md`.

---

# Addendum — the final leg (2026-08-08, after the ruling)

[E17-ruling.md](E17-ruling.md) accepted the harness (27/27 at two seats) and assigned
this session two last items on the Director's relay: **T15b** (Ruling 3e) and **T18**
(Ruling 2). Both are done and appended to §2's table. **Suite end state: 32 tests, 32
passed** (24 hermetic, 8 artifacts). CI was green on the ruling's push (run
`31263164713`) — the repo's first CI run, and the flag-3 closure.

## 10. T15b — the E17 arc's count legs

The ruling asked for "numbered + lettered as the file parses, sequence bounded 1-4 as
ruled" and told me to verify the parsed counts myself, dispatch text being hypothesis.
Verified three independent ways before a leg was written: my own greps against the file
with the parser's own patterns (4 and 10), the DB queried directly (`ruling` 4 =
`1,2,3,4`; `sub-ruling` 10 = `1a,1b,1c,1d,3a,3b,3c,3d,3e,3f`), and the fold's own
reported figure of 14 rows. All three agree. No closure markers in the file.

**The handoffs leg stays deferred, and that half is now measured rather than
predicted:** the E17 kickoff carries no `## Session handoff` header and the DB holds
zero E17 handoffs, so a handoffs leg would grep a header that does not exist — the same
check-that-cannot-fail reasoning that deferred all of T15's E17 half one commit earlier,
still holding for this one piece of it.

**ANCHOR:** verify PASSED all four legs; new legs `grep 4 == db 4` and
`grep 10 == db 10`; `E17 sequence ruling 1-4 gaps: none`. T1's assertions now cover all
four E16/E17 count legs and both sequence lines, so a leg dropped from `COUNT_CHECKS`
fails the suite instead of waiting for a reader to notice an absence.

## 11. T18 — the interpreter pre-check, and what reproducing the trap corrected

**The trap, reproduced exactly.** I simulated the wrong interpreter with a poisoned
`PYTHONPATH` whose `open3d` raises on import — the same failure shape as an absent one —
and ran the suite as it stood: **7 failed / 20 passed**, the ruling seat's result to the
digit.

**Reproducing it corrected my own arithmetic, which is why it was worth running rather
than reasoning about.** I had counted the open3d-importing tools and got *eight* tests,
not seven (`e12_elevated` imports open3d too, which the ruling's prose does not
enumerate). The eighth is
`test_t03_control_explicit_aspect_passes_the_guard`, and under the broken interpreter it
**PASSED** — for the wrong reason. That control asserts two things: exits non-zero, and
carries no ANDON text. A `ModuleNotFoundError` satisfies both. It is a check that cannot
fail, sitting *inside the control that exists to prove another check can* — and it is
exactly why the count is 7 and not 8.

**Hardened in the same commit**, per the repo's rule that a root cause is fixed at every
consumer rather than only where it was noticed: the control now also asserts the failure
is not an import error and *is* a missing-input error, so it fails downstream of the
guard for the only reason that proves the guard let it through.

**The pre-check.** `conftest.pytest_sessionstart` probes the child interpreter once and,
on any miss, `pytest.exit`s with `USAGE_ERROR`. Design points, each with its reason in
the code:

- **A real import, not `find_spec`** — a present-but-broken install (a DLL that will not
  load) produces the same trap as an absent one, and `find_spec` would call it present.
  Measured cost: ~1.2 s once per session against a 93 s suite.
- **The required set is measured, not assumed** — the module-level third-party imports
  of every tool the suite invokes, transcribed per tool. `facet_index` and
  `e04_registry_sweep` are stdlib-only, which is precisely why a wrong interpreter reads
  as a *partial green*: the twenty that pass are the ones that never needed the
  environment.
- **Strict by choice** — it refuses the whole session rather than only the tests that
  need a mesh library, because under a wrong interpreter "20 passed" is the misreading
  being closed.

**ANCHOR, measured:** the poisoned run now exits `USAGE_ERROR` (4) with one message
naming the missing module, the interpreter actually run, the law's interpreter and the
ruling — **zero tests collected, zero run**.

**Five tests ride the commit**, including the trap end-to-end (a child pytest under the
poisoned PYTHONPATH), the probe's own can-fail proof (it must report an absent name),
and a guard on the guard (a pre-check over an empty module list cannot fail). One
disclosure: the first cut of the "nothing ran" assertion checked `" passed" not in
output` and **failed on its own refusal message**, which quotes "7 failed / 20 passed";
it is now checked structurally on pytest's own report lines. My assertion was wrong, not
the code.

## 12. Commits added by this leg

| commit | contents |
|---|---|
| `5c81716` | T15b: E17 count legs + sequence bound + T1's extended assertions |
| `ac0a1f2` | T18: the interpreter pre-check, its five tests, and the T3 control hardening |

Local and unpushed, as dispatched; `docs/index/facet.db` still uncommitted; the stash
untouched; no profile, canon, fixture, palette or seeded-set edit; no memory-store
write.

**HALT — final.** The advisor folds and pushes.
