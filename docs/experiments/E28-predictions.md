# E28 predictions — committed before `instrument_census.py` runs once

**Executor, 2026-08-09.** Drafted in the session scratchpad and moved into
`docs/experiments/` after the baseline suite run completed, because `pytest.ini`'s `fold`
marker forbids corpus writes while the suite is in flight (E23 Ruling 10). The draft was
not edited after the census script was written or run.

---

## The blindness boundary — exactly what was looked at first

- **Read in full:** the E28 dispatch, `docs/specs/measurement-mcp-spec.md`,
  `docs/experiments/E27-ruling.md`, `CLAUDE.md`, `tests/test_t34_front_door_counts.py`,
  `pytest.ini`, `docs/experiments/E27-predictions.md` (first 60 lines, for format).
- **Read in part, for task 0 only:** `docs/experiments/README.md` (the status table's
  first cells), `docs/advisor-kickoff.md` around L120/L161/L185, `SHIP_GATE.md` L61,
  `site/src/site-config.ts` L88–110, `docs/handbook/index.md` L165–173,
  `site/src/content/docs/handbook/{index,getting-started}.md` around their experiment
  mentions, the eight READMEs' record-row lines. **None of this touches
  `tools/diagnostics/`.**
- **Measured before predicting, because gate 1 requires it:** the population —
  `tools/diagnostics/` holds **99 `.py` files and 0 files of any other extension**, three
  ways (`Get-ChildItem -File`, `Get-ChildItem -Force`, `git ls-files`), with **zero
  subdirectories** (the dispatch's parenthetical about `__pycache__` describes a state not
  present).
- **NOT read at draft time:** the source, docstring, or filename list of **any** file in
  `tools/diagnostics/`; any file under `tests/` except `test_t34_front_door_counts.py`;
  `tools/measure_mcp.py`; `tools/instrument_census.py` (it does not exist yet);
  `record_markdown()`'s implementation.
- **Deliberately not looked up:** what E25's "43" was. The dispatch cites *"E25 measured
  41 of its 43"* in the axis F row. **That is a different population whose membership I
  have not measured, and scaling 41/43 onto 99 is precisely the error the last five arcs
  made.** My denominator is 99, named below, and E25's ratio informs none of these numbers.

**Known-in-advance leakage, disclosed:** the dispatch and E27's ruling state facts about
**four** of the 99 files — `e10_offsurface.py` binds its subject as module constants and is
not invocable; `e12_offsurface.py` takes 9 `add_argument` with a required `--prep` and no
hardcoded subject; `e12_thin_curve.py` is "complete, parameterized"; `e14_topology.py` is
complete, takes `--glb`, and crashes on tied extents. Four of ninety-nine are therefore not
blind. Every row below says which.

---

## The unit ritual, applied before every number

Five consecutive arcs missed on a unit or a population, and E27's miss was one level below
both: *a real population whose members were never checked for the property the prediction
assumed.* So each row states **(a) what one of the counted thing is, (b) what the
denominator is made of, and (c) whether the property is defined for every member** —
and where it is not, the row predicts the `n/a` count separately instead of silently
scoring those members `false`.

**No calibration haircut is applied to any number below.** E22's P18 halved an untutored
estimate on this repo's own "densities run 2× high" lesson and measured 175 against a
predicted 4; the ritual moved the answer away from the truth and made the move look like
discipline. Each estimate below is the number I actually believe, stated directly.

---

## The axis definitions, written before counting

These are the census's operative definitions. Where the dispatch's axis table left a
choice, the choice is made here, before any result exists.

**What makes a file a member of this census.** Every one of the 99 `.py` files is a member,
including `__init__.py` if present and including files with no docstring. Membership is
"a `.py` file directly in `tools/diagnostics/`" and nothing else — a curated membership is
the thing this arc exists to stop. Files that turn out to be **libraries imported by other
diagnostics rather than runnable tools** are members that score `false` on axis A, not
non-members; that distinction is a *result*, not an entry condition.

**Axis A — invocable.** `argparse` imported **and** ≥1 `add_argument` **and** an
`if __name__ == "__main__"` guard. All three, because the property being tested is *can
this be pointed at a new subject from a command line*, and any one alone does not deliver
it. Defined for every member (pure source-text). The three components are reported
separately as well, so the boundary can be re-drawn without re-running.

**Axis B — subject-bound.** Two readings, both reported, because they answer different
questions and the strict one is what made `e10_offsurface` un-wrappable:

- **B1 (headline)** — a **module-level** (top-level) string literal containing a
  recorded-tree marker: `E:\`, `E:/`, `facet_next`, `facet_E0`, `training`, `saltroad`,
  `ARMB`. This is the "hardcoded subject constant" reading.
- **B2** — the same markers in **any** string literal in the file, excluding module and
  function docstrings. This catches a subject wired into an argparse `default=`.

The literals themselves are reported, not a boolean (the dispatch's requirement).
Defined for every member.

**Axis C — the question.** Docstring line 1 verbatim, truncated to one line. `n/a` where
the module has no docstring — not an empty string, because "has no docstring" and "has an
empty first line" are different facts.

**Axis D — cited.** The count of **corpus files** (`record_markdown()`'s set, unmodified —
E26 ruled it unchanged) that contain this file's basename. The headline number is *how many
of the 99 have ≥1 citing file*. Defined for every member.

**Axis E — anchored.** Does any file under `tests/` contain this module's basename or
dotted module name **as literal text**. ⚠ **A glob does not name a module.** If a test
enumerates `tools/diagnostics/*.py` by directory walk, the modules it exercises are *not*
named and score `false` here. That is the honest reading of "would an edit to it be
*caught* by name", and it is stated now because it is the axis most likely to be
misread afterwards. Defined for every member.

**Axis F — import-safe.** `--help` exits 0 writing nothing to stderr, under the pinned
interpreter, in three modes (normal, `-O`, `PYTHONOPTIMIZE=1`).

⚠ **This property is NOT defined for every member, and that is E27's exact lesson.**
Three `n/a` classes, each reported with its reason and never scored `false`:

- `n/a (no CLI)` — axis A is false, so there is no `--help` to exit 0. Running the file
  with `--help` would execute its module body, which measures something else entirely.
- `n/a (import blocked)` — the module imports something absent from the pinned interpreter
  (`bpy` is the named case; any ImportError at module scope qualifies). The *environment*
  cannot run the measurement; the module is not thereby unsafe.
- `n/a (timeout)` — the module does work at import that does not terminate promptly.

**Axis G — the job-shape proposal.** Which of the spec's eight tool questions this file
answers, or `none`, or `ambiguous`, or **`no opinion`**. A judgment, labelled as one.
*"No opinion" is a real value and will be used*, because a table of confident `none`s reads
as a measurement and is not one.

---

## P1 — invocable (axis A)

**Unit:** one *invocable file* = one `.py` file in `tools/diagnostics/` satisfying all
three of axis A's clauses. **Denominator: 99** — every `.py` file in that directory,
enumerated, not derived by subtraction. **Property defined for every member:** yes.

**Prediction: 60, band 45–75.**

Reasoning stated so the miss is legible: this repo's culture pushes hard toward re-runnable
parameterized instruments (*"a recipe that does not reproduce its output is not a recipe"*),
but that culture was built over the arcs, and the directory spans the whole history. The
band is wide because I have seen four filenames' worth of evidence and it points both ways
— `e10_offsurface.py` fails all three clauses, `e12_offsurface.py` passes all three, and
they are adjacent arcs.

*Blindness: blind on 97 of 99; `e10_offsurface.py` and `e12_offsurface.py` are known from
E27 Ruling 2, and `e12_thin_curve.py` / `e14_topology.py` are described as parameterized.*

## P2 — subject-bound (axis B1)

**Unit:** one *subject-bound file* = one member with ≥1 **module-level** string literal
carrying a recorded-tree marker. **Denominator: 99.** **Property defined for every
member:** yes.

**Prediction: 30, band 15–50.**

The band is deliberately wide and I want the reason on the record: **B1 and B2 could differ
a lot**, and I do not know which way. A per-arc script that hardcodes `SUBJ = r"E:\..."` at
module scope scores B1; a general tool with `--prep` defaulting to a recorded path scores
only B2. If the directory is mostly the second shape, B1 lands near the bottom of the band
and B2 far above it. **Secondary prediction: B2 − B1 = 10, band 0–25.**

*Blindness: blind on 97 of 99.*

## P3 — cited in the corpus (axis D)

**Unit:** one *cited file* = one member whose basename appears in ≥1 file of
`record_markdown()`'s corpus set. **Denominator: 99.** **Property defined for every
member:** yes.

**Prediction: 65, band 45–85.**

This repo documents what it runs, and a diagnostic that produced a number in a report is
named in that report. The shortfall I expect is internal helpers and superseded one-offs
that never reached a ruling. I have not measured how many corpus files exist, and I am not
predicting the *number of mentions* — the unit is files-of-the-99, not mentions.

*Blindness: blind.*

## P4 — anchored by a test (axis E)

**Unit:** one *anchored file* = one member whose basename or dotted module name appears as
literal text in some file under `tests/`. **Denominator: 99.** **Property defined for
every member:** yes.

**Prediction: 12, band 3–30.**

⚠ **This is the row most likely to be wrong, and the mechanism would be the unit.** This
repo prefers globbing to hand-written lists — `test_t34_front_door_counts.py` says so
explicitly, refusing to hand-list surfaces because *"the surface list is not itself a
hand-written live-moving quantity"*. If `test_t33_diagnostics_gates.py` walks
`tools/diagnostics/` rather than enumerating it, then a great many modules are *exercised*
while **none of them is named**, and this number is near zero. I know T33 pins
`superseded/texpass_thin_mask.py` **by name**, so the count is not zero. I have not opened
T33 and am not going to before this is committed.

*Blindness: blind. T33's existence and byte size are known from a directory listing;
its contents are not.*

## P5 — import-safe in all three modes (axis F)

**Unit:** one *import-safe file* = one member whose `--help` exits 0 writing nothing to
stderr in **all three** interpreter modes. **Denominator: 99**, as the dispatch words it —
so the count of `true`, with `n/a` counted separately and **never** folded into either
side.

⚠ **Property NOT defined for every member** — see the axis F definition above. This is the
row E27's ruling was earned on, so it gets two numbers:

**Prediction: 50 true, band 30–70.**
**Prediction: 41 `n/a`, band 25–55** — dominated by `n/a (no CLI)`, which by construction
is `99 − P1 = 39` if my P1 is right, plus a handful of import-blocked modules
(`bpy`, and whatever else the pinned interpreter lacks). **`n/a (no CLI)` is not an
independent estimate; it is P1's complement**, and I am saying so rather than letting two
of my own numbers look like corroboration.

That leaves **false ≈ 8, band 0–25** — modules with a CLI that misbehave under `-O` or
`PYTHONOPTIMIZE=1`. E22–E25 converted 278 ANDONs to `raise` precisely so optimize mode
would stop deleting them, so I expect this to be small; it is not zero because the axis
also catches anything printed to stderr on `--help`.

*Blindness: blind, and deliberately un-informed by E25's 41/43 (different population).*

## P6 — maps to one of the spec's eight questions (axis G)

**Unit:** one *mapped file* = one member I propose answers one of the spec's eight tool
questions — `mesh_stats`, `mesh_topology`, `reach_ceiling`, `thin_extent_curve`,
`offsurface_rate`, `texel_provenance`, `anchor_check`, `measure_report`. Not `none`, not
`ambiguous`, not `no opinion`. **Denominator: 99.** **Property defined for every member:**
yes, but it is a *judgment*, and its value depends on who is judging — which is why it is a
proposal and why the boundary is not mine to rule.

**Prediction: 20, band 8–40.**

The spec's eight are a curated surface over subject-independent instruments; most of a
99-file diagnostics directory is arc-specific measurement that answers a question nobody
listed. I expect `mesh_stats`, `texel_provenance` and `reach_ceiling` to attract several
files each and `anchor_check` to attract **zero** — E27 Ruling 4 established that the file
*named* `e13_anchor_check.py` is the spiral-law guard, a different question entirely, and
the spec's `anchor_check` pattern exists as harness tests and session procedure rather than
as a tool.

**Sub-prediction, because the dispatch calls it out and it is the interesting cell:
`no opinion` + `ambiguous` ≥ 10.** If that lands at zero, the axis was not being used
honestly.

*Blindness: NOT blind — the spec's eight questions were read in full. Blind on the 99.*

## P7 — behavioural: is 2a's repair byte-identical on every recorded subject?

**Not a quantity.** The claim: **on any mesh whose three std-frame extents are pairwise
distinct, the repaired `(thin, tall, wide)` selection returns the same three indices as the
current expression** — so on every recorded subject the repair changes no output byte.

**Prediction: YES.**

**What would falsify it**, stated before the check:

1. **Any distinct-extent triple** — from the recorded subjects or from a randomized sweep —
   on which the repaired expression selects a different index triple than
   `thin = argmin(ext)`, `tall = argmax(ext)`, `wide = 3 − thin − tall`. One counterexample
   falsifies it outright.
2. **A recorded subject with two equal extents.** On such a subject the *current* code
   raises `IndexError`, so "byte-identical" has no referent: the repair converts a crash
   into output, which is the repair's whole purpose but is **not** a byte-identical
   outcome. If one exists, the honest claim narrows to "byte-identical wherever the current
   code produces bytes at all", and the difference must be reported rather than smoothed.
3. **A subject where the extents are distinct in exact arithmetic but tie in float** —
   which would make the boundary a tolerance question rather than a logical one, and would
   mean the invariant as stated is under-specified.

⚠ **This prediction is the one I am least entitled to.** E27 Ruling 3 already asserts it,
and the dispatch's instruction is explicit: **discharge the obligation rather than cite it**
— exhaustive comparison over the recorded subjects *plus* a randomized sweep over
distinct-extent triples, not by reading the diff. An inherited claim is a hypothesis wearing
a fact's clothes, and this one is wearing a ruling's.

*Blindness: NOT blind — E27 Ruling 3 states the conclusion and the dispatch restates it.
The prediction is therefore worth little; the discharge is the deliverable.*

---

## ⚠ Amendment, appended after the numbers were frozen and before this file was committed

**2026-08-09, same session.** The blindness boundary above says E25's "43" was
*deliberately not looked up*. That was true when the numbers were written and **no number
above has been altered**. It stopped being true afterwards, and a predictions file that
hides its own corrections is the thing this repo exists to get away from, so:

While locating **E25's tree-manifest procedure** — needed for this arc's gate 6, a
different question entirely — I read `E25-diagnostics-gates-report.md` around its
compensators section and incidentally saw its files-changed line: ***"Under `tools/` —
exactly 43, all in scope: `tools/diagnostics/` ×42"***.

**What that leaks, stated plainly so the ruling can discount it:** E25's 43 is a count of
**files it edited**, of which **42 are in `tools/diagnostics/`** — so at least 42 of my 99
carried an ANDON that E25 converted. That bears on **P4** (those 42 are plausibly the ones
`test_t33_diagnostics_gates.py` exercises, though whether it *names* them is exactly the
unit question P4 turns on, and I still have not opened T33) and weakly on **P5** (a file
with a converted gate is a file someone ran). It does **not** touch P1, P2, P3, P6 or P7.

It also confirms the disclaimer's substance: 41/43 was never a ratio about *import-safety
across the whole directory*, so scaling it onto 99 would have been the unit error the last
five arcs made. **The predictions stand as written; this note is the disclosure, not a
revision.**

## What would make this whole set uninteresting

If the census's classifier is not falsified first, every number above is a number from an
unfalsified instrument and none of them means anything (gate 2). The can-fail legs land in
`T41` in the same commit as the classifier, and the classifier's numbers are not to be
believed — by me or by anyone reading this — until those legs have been seen failing on
synthetic input built to fail them.
