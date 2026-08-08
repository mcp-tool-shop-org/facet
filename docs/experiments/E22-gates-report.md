# E22 — report: the gates an environment variable deletes

**Executor session, 2026-08-08.** Spec:
[E22-gates-not-asserts-kickoff.md](E22-gates-not-asserts-kickoff.md). Predictions
committed at `a729e6e` **before the first file under `tools/` was opened**:
[E22-predictions.md](E22-predictions.md). Work committed at `f878b8b`.

This report measures and reports. It does not decide what the results mean; the
advisor rules at `E22-ruling.md`.

---

## The short version

The conversion did what the dispatch asked and the anchors held on the first
attempt. **The dispatch's scope premise did not survive being measured.**

- **88 sites converted**, pure move, proved by whole-file AST equality rather than
  by my reading of the diff. **Zero reverted.**
- **All three named anchors reproduce** — T7 byte-identical (sidecar json too),
  the twin-projection anchor, T26's three fired ANDONs.
- **Suite 248 → 275**, artifacts tier included, zero skips. **CI green.**
- The four must-not-move trees — **7,312 files, sha256-manifested before the first
  replay** — are byte-unmoved at the halt.
- **`4 = REFUSED` lands** for both classes E21 Ruling 4 named.
- **THE FINDING: `tools/` holds 278 ANDON-carrying asserts, not 87.** The
  "~207 non-ANDON asserts" the scope excluded as "developer sanity checks" is a
  population that does not exist — **192 of them carry the ANDON token**, and
  **175 sit before a write in their own scope.** F1 below.

---

## Gate 0 — the session-start index gate

`build` then `verify` against a scratch `--db`, because the record mount is live
on this working copy.

```
[leg 4] the seeded question set - target within the top 3     19 / 19
determinism leg that held: byte-identity
VERIFY PASSED - all four legs                                 exit 0
```

Re-run after the work, against a fresh scratch DB: **`VERIFY PASSED`, exit 0,
byte-identity**, with `prose_sections` 2147 → 2157 (this arc's two documents).

---

## The census — verified, not inherited

The dispatch ordered this measured. It was, by AST walk over all 150 `.py` files
under `tools/` (`assert_census.py`, run before any file was opened for editing).

| claim in the dispatch | measured | verdict |
|---|---|---|
| `tools/` — 294 bare asserts across 72 files | **294 asserts, 72 files carrying ≥1** | **reproduces exactly** |
| `texpass_iter.py` ANDON asserts | **8** | reproduces |
| `texpass_finalize.py` | **4** | reproduces |
| `project_twins.py` | **15** (+1 as raise) | reproduces |
| `e11_manifest.py` | **35** (+1 as raise) | reproduces |
| `e11_export_turnaround.py` | **24** (+1 as raise) | reproduces |
| **"the 87 ANDON-carrying assert sites in the five tools"** | **86** | **the table sums to 86; 87 is an arithmetic slip** |
| "the ~207 non-ANDON asserts … developer sanity checks" | **16 non-ANDON asserts exist in all of `tools/`** | **F1 — falsified** |

Every per-tool cell the ruling seat published reproduces to the digit. The two
totals derived from them do not.

**The in-scope set is 88**: 86 + `facet_index.py:343` + `record_mcp.py:189`.

---

## F1 — THE SCOPE'S EXCLUSION CLAUSE DESCRIBES A POPULATION THAT DOES NOT EXIST

This is the finding of the arc and it is reported, not acted on.

```
asserts in tools/                                    294
  carrying the ANDON token in their own message      278
  carrying no ANDON token at all                      16
```

The dispatch computed its out-of-scope class as `294 − 87 = 207` and characterised
it as *"developer sanity checks; converting them wholesale is a large diff across
accepted-asset tooling for no gate."* Measured, that class is **16 asserts**, not
207. The other **192 are ANDON-carrying gates in 57 files** the scope never named:

```
bake_hero_prep.py 15 · diagnostics/e14_repair_collar.py 13 · brush_cloud_step.py 9
diagnostics/e14_make_brush_prompts.py 8 · diagnostics/e04_blotch.py 7
diagnostics/e14_demote_garnet.py 7 · subject_profile.py 6 · silhouette_masks.py 4
cull_unseen.py 3 · resample_atlas.py 2 · palette_gate.py 2 · export_asset_source.py 2
… 57 files total
```

**Every one of them is deleted by `PYTHONOPTIMIZE=1`, exactly as the 86 were.**

### F1b — and 175 of them stand between the process and a write

Measured by a static walk (`irreversible.py`): for each out-of-scope assert,
whether its own scope later executes an unambiguous write.

```
out-of-scope asserts followed by a write in the same scope   187
  carrying the ANDON token                                   175
  not carrying it                                             12
                                                    across    61 files
```

**What this measures, stated before the number is used:** "later" is *source
order within the scope*, not execution order, so a loop or an early return can
make it over- or under-count. The write set was **tightened after a hand-check**
of the first pass, which had counted `ndarray.copy()` and `str.replace()` as
writes; `fh.write()`, `.copy()` and bare `run()` are now dropped even though some
really are writes, so **175 under-counts on purpose**. It is a diagnostic, not a
gate — which of these writes nobody can undo is the advisor's call, so the three
closest sites are named in full:

```python
# tools/bake_hero_prep.py:488-489
assert float(px_.var()) > 1e-8 or kind == "mask", f"ANDON: {kind} bake is uniform"
np.save(os.path.join(args.outdir, f"{kind}.npy"), px_)

# tools/resample_atlas.py:94-95
assert nonblack > 0.25, "ANDON: transferred atlas is mostly black"
Image.fromarray(img).save(args.out)

# tools/silhouette_masks.py:160-165
assert diff == 0, (
    f"ANDON: view {idx} does not reproduce its anchor — {diff:,} differing px, "
    f"IoU {inter / union:.6f}. The camera convention is wrong; every twin built "
    f"on these masks would be misregistered. Fix before generating anything.")
...
with open(os.path.join(args.out, "silhouettes.json"), "w") as fh:
```

The third one's own message says **"Fix before generating anything."** Under `-O`
it does not say it, and the generation proceeds.

**Not converted.** The dispatch pre-routed this exactly — *"if one turns out to
guard an irreversible step, that is a finding for the ruling, not a scope
extension"* — and 175 is not one, so the routing holds all the harder. The
ruled 88 were converted and this is reported.

---

## The conversion

### The rule, fixed in the predictions before any file was opened

```
assert COND, MSG   ->   if <negate(COND)>:
                            raise AssertionError(MSG)

negate(COND) = X              when COND is `not X`   (3 sites)
negate(COND) = not (COND)     otherwise             (85 sites)
```

`COND` and `MSG` keep their source text character for character. No helper
function, no `AndonError` subclass, no message reworded, no condition tightened.
**Only leading whitespace on the message's continuation lines moves**, by the +4
the new nesting requires.

**`AssertionError` was not a preference.** `facet_index.run_contract` catches that
type specifically (`facet_index.py:208`) and routes it to the `GATE_FIRED` branch;
any other type lands in the generic runtime handler with a different message and a
different code. P8 predicted zero such handlers in `tools/`; there is exactly one,
and it is the one that makes the type mandatory.

### Per-file table

| file | sites | diff (+/−) | shape notes |
|---|---|---|---|
| `tools/texpass_iter.py` | **8** | +27 / −19 | 1 `not`-condition, 5 multiline |
| `tools/texpass_finalize.py` | **4** | +13 / −8 | 2 multiline; the write-head's distance gates |
| `tools/project_twins.py` | **15** | +39 / −25 | 4 multiline |
| `tools/e11_manifest.py` | **35** | +103 / −68 | 20 multiline, indents to 16 |
| `tools/e11_export_turnaround.py` | **24** | +72 / −44 | 1 `not`-condition, 11 multiline |
| `tools/facet_index.py` | **1** | +48 / −29 | the inverse-discovery guard, `not`-condition; the rest of the diff is the exit-code block |
| `tools/record_mcp.py` | **1** | +2 / −1 | `assert code in CODES`, non-ANDON |
| **total** | **88** | | 43 multiline, 3 `not`-conditions |

**0 sites shared a line with another statement, 0 carried a trailing statement,
0 lacked a message.** The splice was therefore safe by line range — measured
before it was attempted, not assumed.

### The pure-move proof

Two independent checks, neither of which is my reading of the diff.

1. **Per site** (`convert.py --check`): the produced statement is an `If` whose
   body is a single `raise AssertionError(...)` with exactly one argument;
   `ast.dump(arg) == ast.dump(old.msg)` and the test matches the negation rule.
   **88/88 OK.**
2. **Whole file** (`pure_move_proof.py`, written separately from the splicer):
   take each file *as git has it at the prior commit*, apply the negation rule to
   its in-scope `Assert` nodes **in the tree**, and compare `ast.dump` of the
   entire module against the file on disk.

```
texpass_iter.py            sites=8    whole-file AST: IDENTICAL to the rule applied at HEAD
texpass_finalize.py        sites=4    whole-file AST: IDENTICAL to the rule applied at HEAD
project_twins.py           sites=15   whole-file AST: IDENTICAL to the rule applied at HEAD
e11_manifest.py            sites=35   whole-file AST: IDENTICAL to the rule applied at HEAD
e11_export_turnaround.py   sites=24   whole-file AST: IDENTICAL to the rule applied at HEAD
facet_index.py             sites=1    whole-file AST: IDENTICAL to the rule applied at HEAD
record_mcp.py              sites=1    whole-file AST: IDENTICAL to the rule applied at HEAD

PURE MOVE: 7 of 7 files prove identical-except-the-rule
```

Check 2 is total: it would catch a stray edit anywhere in the file, not only at a
site. Comments are not in an AST, so they were diffed separately by token:

```
texpass_iter 93 · texpass_finalize 24 · project_twins 252 · e11_manifest 80
e11_export_turnaround 97 · facet_index 335 · record_mcp 132     ALL IDENTICAL
comment lines changed: 0
```

**Neither proof can be a standing test.** Both need the pre-conversion tree, and
after the commit `HEAD` *is* the converted state — a re-run would be a tautology.
What was portable was ported: T30 pins the durable half (no ANDON gate in these
seven files is an `assert`; the exception-type census; the ANDON message counts).

---

## Gate 2 — the anchors

Run after the conversion, before anything else was touched.

| anchor | result |
|---|---|
| **T7** `test_t07_finalize_reproduces_the_recorded_atlas` | **PASSED** — `atlas_final.png` byte-identical to the recorded artifact; the three recorded inputs re-hash unchanged; and its reported-not-asserted line printed **`T7 finalize.json vs recorded: byte-identical`** |
| **twin projection** `test_t10_projection_reproduces_stage1b` | **PASSED** |
| **T26** — three fired ANDONs + 5 siblings | **8/8 PASSED** |

`11 passed in 46.04s`. **No anchor failed; no conversion was reverted.**

**Why T26 survived, measured rather than assumed** (this is P14's correction):
T26 drives `texpass_finalize` **as a subprocess** and keys on `rc != 0` plus the
ANDON text on stderr — **not** on the exception type. So the type was unobserved
by that anchor, and my stated main reason for keeping `AssertionError` was not
what saved T26. The reason the type is nonetheless mandatory is `run_contract`,
which is a different site in a different file. The prediction was right for the
wrong reason and the report says so rather than banking the hit.

---

## Gate 1 — the suite

Full run under the pinned interpreter, artifacts tier included, both before and
after.

```
BEFORE   248 passed in 155.83s     0 failed, 0 skipped
AFTER    275 passed in 171.25s     0 failed, 0 skipped
HERMETIC (as CI runs it)   267 passed, 8 deselected in 82.60s
```

The artifacts tier ran on both sides — the recorded trees are present on this
rig, so nothing skipped and the anchors were live rather than absent.

---

## The compensator gate

The dispatch scored NAMED_COMPENSATORS at **1** and made detection mandatory.
Carried out in full, and it is the row that most deserved the score.

- **Manifest taken BEFORE the first replay** — before even the baseline suite run,
  because the artifacts tier is the thing that touches those trees. Per-file
  sha256 over the whole recorded root, not only the four named trees: `facet_next`
  (5,040 files), `facet_E01/02/05/06/07/08` (1,396), `saltroad_bake_fix` (876) =
  **7,312 files, 16.3 GB, 76 s**.
- **Re-checked twice**: after the baseline suite run, and at the halt.

```
RECHECK  before=7312 after=7312     added 0   removed 0   changed 0
MANIFEST HELD - no file in the recorded trees moved
```

Two corrections to the note's own premises, reported because they change how the
row should be scored next time:

1. **The four trees are not where the note implies.** There is no `facet_E04`,
   `facet_E13` or `facet_E14` under `E:\AI\training`. E04's, E13's and E14's trees
   are **subdirectories of `facet_next`** (`E04_*` ×17, `E13_*` ×4, `E14_*` ×3);
   only E08's is a top-level `facet_E08`. **P16 MISS** on the paths.
2. **P17 MISS, and the gap is smaller than scored.** The prediction was that at
   least one anchor-bearing tool has no output-path argument, forcing a replay at
   the tree. False: `texpass_finalize` takes `--out` and `--json`, and
   `tests/conftest.py` already implements the discipline the note asks for —
   `copy_state()` copies every mutable file to scratch, with a docstring that says
   *"recorded trees are READ, never written"*, and T7 re-hashes its inputs
   afterward. **The harness had the compensator before the dispatch asked for
   one.** What it did not have is the manifest over the *whole* tree, which is
   what would catch a write to a file no test names.

---

## Q2's exit code — `4 = REFUSED`

Carried per E21 Ruling 4. **5 code sites**, all inside the seven named files
plus the fixture, no new module:

| site | change |
|---|---|
| `facet_index.py` constants | `EXIT_ANDON_UNRULED = 1` → **`EXIT_REFUSED = 4`**, with the ruling's reasoning in place of the "unruled" note |
| `facet_index.py` `run_contract` | the `GATE_FIRED` branch returns `EXIT_REFUSED` |
| `facet_index.py` `verify()` | the failing return `1` → `EXIT_REFUSED`; the passing `0` → `EXIT_OK` |
| `tests/mcp_support.py` | `FAILED_PARSE["exit_code"]` → `facet_index.EXIT_REFUSED`; `PASSED_PARSE` → `EXIT_OK` |
| `tests/test_t04_discovery_guards.py:44` | `rc == 1` → `rc == m.EXIT_REFUSED` |

**The claim the dispatch ordered verified before it was relied on:**
`record_mcp.parse_verify` keys on **`rc != 0`** (`record_mcp.py:429`) and
**`rc == 0`** (`:432`), never on `rc == 1`. **Verified — the health state machine
is indifferent to which non-zero code arrives.** P20 HIT.

**One hardening beyond the literal carry, declared rather than slipped in.** E21's
F3 named `FAILED_PARSE["exit_code"] = 1` as "a fixture constant" that nothing
compared against a live run. Re-typing `4` there would have reproduced exactly the
defect that let it be wrong. It now reads `facet_index.EXIT_REFUSED`, so the
fixture cannot disagree with the command it stands in for. **This is more than the
dispatch asked for and is flagged for the ruling.**

**Not decided by this seat:** the certificate's schema version. The field's name
and type are unchanged and only its domain widens, so a bump looks unnecessary —
but the schema is a shipped artifact and its version is the advisor's call. P23.

**Left alone, and named:** `tests/test_t16_registry_sweep.py:75`'s `assert rc == 1`
is `diagnostics/e04_registry_sweep.py`'s own contract, not the CLI registry — a
different tool, outside the seven. It stays at `1`.

---

## F2 — an ANDON has two exception types in this repo

Caught by a T30 test I wrote too broadly, which failed on first run and was
**corrected to describe what is there rather than what I assumed**.

Three ANDONs were **already raises** before E22 and they raise **`SystemExit`**:

```
tools/project_twins.py:281            raise SystemExit(f"ANDON: --{name} view index {k!r} is not an integer")
tools/e11_manifest.py:267             raise SystemExit(f"ANDON: {path} differs from what this tool would assemble …")
tools/e11_export_turnaround.py:108    raise SystemExit(f"ANDON: emit failed for yaw {yaw} el {el} in {state_dir}")
```

These are E21's "as raise" column (0/0/1/1/1), **byte-untouched by E22** — the
diff contains no `SystemExit` line. They are not the defect this arc exists to
fix: `raise SystemExit` is not deletable by `-O`. But it means *"a fired ANDON"*
is not one exception class, and `SystemExit` would not be caught by
`run_contract`'s fired-gate branch if one of these ever moved into a shipped
command. **Reported, not unified** — a pure move does not include normalising a
type nobody ruled.

---

## F3 — gate 3's wording needs a reading, and I took the conservative one

Gate 3 says *"no edit outside the seven named files."* The dispatch itself
requires two edits outside them: *"Tests ride the commit, starting at T30"* and
*"`SHIP_GATE.md`'s B2 line is the gate item this closes."* Read literally, the
gate forbids its own instructions.

**Taken as governing tool code**, which is the only reading under which the
dispatch is self-consistent. **No tool file outside the seven was touched** —
`git diff --name-only HEAD~1 -- tools/` returns exactly the seven. Everything
else edited is `tests/` or a named doc, itemised below. Reported rather than
improvised past. P24.

**Files edited outside `tools/`, every one:**

| file | why |
|---|---|
| `tests/test_t30_gates_survive_optimize.py` | new; the dispatch names it |
| `tests/mcp_support.py` | E21 F3's fixture constant |
| `tests/test_t04_discovery_guards.py` | asserted the old `1` |
| `tests/test_t29_cli_contract.py` | **prose only, no assertion moved** — its docstring said both classes "are E21's open questions"; they are ruled. Its `!= OK` assertions were correct before the ruling and stay correct after, so they are deliberately left as a second, weaker witness that does not depend on the constant's value |
| `SHIP_GATE.md` | the B2 line, which the dispatch names |
| `CHANGELOG.md` | **`[Unreleased]` only.** The `[0.2.0]` section states what that tag shipped and was accurate when written; a shipped release entry is not rewritten |

---

## Tests that ride the commit — T30

`tests/test_t30_gates_survive_optimize.py`, **27 cases from 14 functions**,
`27 passed in 19.46s`. Subprocess-based, because `__debug__` is fixed at
interpreter start and cannot be toggled in-process — so an in-process version of
this test cannot exist. **P26 HIT.**

| test | modes | what it pins |
|---|---|---|
| `the_optimize_legs_are_not_vacuous` | all 3 | **the can-fail leg that makes the whole file mean something** — on a throwaway script the test writes, a bare `assert` halts a normal interpreter and does not halt under `-O`/`PYTHONOPTIMIZE=1`. Never on a facet gate |
| `finalize_source_distance_gate_refuses_in_every_mode` | ×3 | refuses, says `ANDON`, **and `out_png` does not exist** |
| `finalize_beyond_edges_gate_refuses_in_every_mode` | ×3 | same, second distance gate |
| `finalize_uniform_atlas_gate_refuses_in_every_mode` | ×3 | third gate, fired by **constructing the input it catches** rather than moving a bound — so this leg depends on no tunable |
| `finalize_clean_run_is_silent_in_every_mode` | ×3 | **can-fail leg** — inside the bounds, the same command in the same mode succeeds and writes |
| `index_discovery_gate_refuses_in_every_mode` | ×3 | the one gate in a published console script exits **`REFUSED`** and prints `GATE_FIRED` |
| `index_discovery_gate_can_fail_in_every_mode` | ×3 | **can-fail leg** — no stray file, builds, exit 0 |
| `a_failing_verify_exits_refused` | — | the ruled integer |
| `the_refused_code_discriminates` | — | **can-fail leg + the discrimination pair**; `4 ∉ {0,1,2,3}` |
| `the_certificate_field_and_the_fixture_agree_with_the_tool` | — | E21 F3 closed |
| `no_converted_file_still_gates_with_an_assert` | — | the standing law, AST-checked over the seven |
| `the_structural_check_can_fail` | — | **can-fail leg** — the walk finds a *planted* ANDON assert and ignores a non-ANDON one |
| `the_andon_exception_types_are_the_ones_e22_measured` | — | both populations (85+1 `AssertionError`, 3 `SystemExit`) |
| `run_contract_still_keys_on_assertionerror` | — | and that its handler **precedes** the broad one |
| `the_conversion_left_no_orphan_message` | — | the per-file ANDON message census |

**5 can-fail legs.** **No test asserts that `PYTHONOPTIMIZE=1` disables a gate** —
E21 refused to pin that and it was right; the one test that touches the mechanism
does so on throwaway source and pins a property of CPython, so that the tests of
facet's own gates can be believed rather than passing vacuously.

`test_t30_no_converted_file_still_gates_with_an_assert` is **deliberately scoped to
the seven files**, with the reason in its docstring: pinning the other 192 would
fail on work nobody has been asked to do.

---

## Gates

| gate | evidence | verdict |
|---|---|---|
| **1. suite green before and after, full artifacts tier** | 248 → **275**, 0 failed, 0 skipped, artifacts live | **PASS** |
| **2. every named anchor reproduces byte-for-byte** | T7 byte-identical (+ its json), T10 passed, T26 8/8; **0 reversions** | **PASS** |
| **3. no edit outside the seven named files** | `git diff --name-only HEAD~1 -- tools/` = exactly the seven; nothing in `canon/`, `profiles/`, the citable trees, the seeded set or a closed ruling; the wording itself is F3 | **PASS**, on the reading in F3 |
| **4. CI green including both dependency scanners** | run [`31279280312`](https://github.com/mcp-tool-shop-org/facet/actions/runs/31279280312) on `f878b8b`, `hermetic in 3m6s` — `hermetic set` ✓, `dependency scan - python (published surface)` ✓, `dependency scan - npm (published surface)` ✓. **No workflow edit** (P28) | **PASS** |

Plus the compensator gate: **manifest held, 7,312 files, 0 changed.**

---

## Predictions scored

**23 scoreable rows** (P1–P28 less L/D rows). Blindness was disclosed per row and
is not re-litigated here.

### Blind (P) — 13 hit / 5 miss

| id | claim | outcome |
|---|---|---|
| P1 | 294 asserts across 72 files reproduces | **HIT** |
| P3 | the five cells reproduce 8/4/15/35/24 and 0/0/1/1/1 | **HIT** |
| P8 | zero `except AssertionError` in `tools/` | **MISS** — exactly one, `facet_index.py:208`, and it is the one that makes the exception type mandatory |
| P10 | the conversion form, held to | **HIT** (a commitment; held at all 88 sites) |
| P11 | 2–4 conditions need parenthesising; 0 tuple-condition asserts | **SPLIT** — 0 tuple bugs (**hit**); 85 of 88 took `not (…)`, so the "2–4" was a misreading of my own rule (**miss**) |
| P12 | ≥2 of the five tools import a shared helper | **MISS** — the five are five islands; no shared module |
| P13 | no anchor fails; zero conversions reverted | **HIT** |
| P14 | T26 fires in-process and keys on the exception type | **MISS** — subprocess, keys on `rc != 0` and stderr text |
| P16 | zero files in the trees change | **HIT** on the zero; **MISS** on the four paths (no `facet_E04/13/14` exists) |
| P17 | exactly one anchor tool lacks an output-path argument | **MISS** — none does; the harness already had the discipline |
| **P18** | **4 out-of-scope asserts guard an irreversible step (band 2–6)** | **MISS, by ~44×** — see below |
| P19 | zero of the out-of-scope set converted | **HIT** |
| P20 | `parse_verify` keys on `rc != 0` | **HIT** |
| P22 | 3–5 exit-code sites, no new module | **HIT** — 5, no new module |
| P24 | gate 3 read as governing tool code, reported not improvised | **HIT** |
| P25 | 1 new test file, 10–18 functions, suite 258–266 | **SPLIT** — 1 file (**hit**), 14 functions (**hit**), suite **275** (**miss**, above the band) |
| P26 | the `-O` legs run as subprocesses | **HIT** |
| P27 | 3–6 findings, one about 86/87 | **HIT** — 3 findings, F1 is the 86/87 one |
| P28 | CI green with no workflow edit | **HIT** (no workflow edit; CI result below) |

### Semi-blind (S) — 3 hit / 1 miss

| id | claim | outcome |
|---|---|---|
| P2 | "bare assert" means construction, not a missing message | **HIT** — 292 of 294 carry a message, so the 294 cannot be the message-less count |
| P6 | 86/86 five-tool ANDON asserts carry a message | **HIT** — and the reasoning was right: the token lives in the message, 0 in comments |
| P7 | `facet_index`'s guard has a message, `record_mcp`'s does not | **MISS** on the second half — `assert code in CODES, "unnamed error code: %s" % code`. **88 of 88 carry a message** |
| P9 | two functions catch `AssertionError` incidentally via `except Exception` | **HIT** — `facet_index.py:221`, `record_mcp.py:880`; and the deliberate narrow handler P8 missed sits above the first |

### The instructive miss — P18

I predicted **4**, band 2–6. Measured **175**.

The prediction file records the reasoning verbatim: *"my untutored estimate was
8–12 and I am halving it on that record alone"*, citing E21's calibration lesson
that this repo's density predictions run ~2× high. **Applying a calibration
correction to a number I had no business estimating made it worse, not better.**
The 8–12 was already wrong by an order of magnitude; halving it moved away from
the truth and dressed the move up as discipline.

The deeper error is the one worth carrying: I predicted a *density* when the
question was a *definition*. I assumed the dispatch's "~207 non-ANDON asserts"
named a real class and asked how many of its members were dangerous. The class
did not exist. **A quantity predicted about a mis-specified population cannot be
right, and the calibration ritual gave me a way to feel careful while being
wrong about the thing underneath.** E20's lesson was *predict quantities, not
negligence*; this arc's is **check that the population is real before you predict
its density.**

---

## What this arc did not do

- **Did not convert the 192 out-of-scope ANDON asserts.** Scope was ruled narrow
  and F1 is routed to the ruling, which is what the dispatch says to do with it.
- **Did not unify `SystemExit` and `AssertionError`** (F2).
- **Did not decide the certificate's schema version** (P23).
- **Did not touch** U3's logging flag, the three testability seams, P5, the
  measurement MCP, or the release. No tag, no publish.
- **Did not write to the memory store.**

## Open for the ruling

1. **F1 / F1b** — 192 ANDON gates outside the scope, 175 of them before a write.
   Convert them, and if so in what unit of work? Or is the ANDON token the wrong
   axis, and the real scope *"every assert that guards an irreversible step"*?
2. **F2** — should an ANDON have one exception type?
3. Does `4 = REFUSED` extend to the **research tools**, which have no
   `run_contract` and today exit `1` with a traceback when a gate fires? E21
   Ruling 4 was written about the exit-code registry of the two published
   commands; E22 did not extend it on its own authority.
4. The `mcp_support` hardening (constant instead of literal) — beyond the literal
   carry, declared above.
5. The certificate's schema version (P23).

---

## Appendix — commands

```
tools/facet_index.py build|verify --db <scratch>      gate 0, before and after
python -m pytest -q                                   248 -> 275
python -m pytest -q -m "not artifacts"                267 passed, 8 deselected (as CI runs it)
tree_manifest.py write|check                          7,312 files, 3 runs, 0 changed
assert_census.py                                      294 / 72 / 278 / 16
convert.py [--apply]                                  88 sites, per-site AST proof
pure_move_proof.py                                    whole-file AST proof vs the prior commit
comment_diff.py                                       0 comment tokens changed
irreversible.py                                       175 ANDON asserts before a write, 61 files
```

Instruments live in the session scratchpad, not the repo: they are one-shot
proofs that need the pre-conversion tree, and the repo's rule is that
**re-runnable** anchors get ported into the harness. The re-runnable half is T30.
