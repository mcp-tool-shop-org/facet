# E24 — report: the install that cannot find the record

**Executor, 2026-08-09.** Spec: [E24-installed-paths-kickoff.md](E24-installed-paths-kickoff.md).
Predictions: [E24-predictions.md](E24-predictions.md), committed at `720bae8` **before any
source file was opened**. Fix + tests: `e8b24db`.

This report measures and reports. It does not decide what the results mean; the advisor rules
at `E24-ruling.md`.

---

## 1. The enumeration, re-measured rather than inherited

The dispatch prints **20** `file:line` references under a heading reading *19 `REPO`
consumers*. Both numbers are right and the reconciliation is the one predicted: `facet_index.py:70`
is the definition, so 20 − 1 = 19 consumers.

Measured with `grep -n '\bREPO\b'` on both files:

| file | dispatch | measured | agreement |
|---|---|---|---|
| `facet_index.py` | 70 · 281 · 326 · 345 · 384 · 389 · 398 · 845 · 2072 · 2084 · 2188 | identical, 11 lines | exact |
| `record_mcp.py` | 112 · 119 · 272 · 275 · 312 · 494 · 495 · 890 · 891 | identical, 9 lines | exact |

`record_mcp.py` carries three further mentions of `REPO` at lines **105 / 114 / 115** — all
inside comments, none a consumer. The dispatch's enumeration is exact. **P7 first half: hit.**

**P7 second half also hit, and one instance is load-bearing.** `REPO` occurs outside the two
named files in `tests/conftest.py`, `docs/handbook/sync_to_site.py`, four `tools/e10_*.py`
diagnostics and `tools/export_asset_source.py` — all of them *independent* definitions of a
local name, coupled to nothing here. The two that are coupled:

- `tests/test_t21_record_mcp_health.py:205-206` monkeypatches **both** `record_mcp.REPO` and
  `facet_index.REPO` to an empty directory. This is why `repo()` reads the module global on
  every call instead of capturing it — a captured value would make that test measure nothing.
- **`tests/test_t28_frozen_runtime.py:78` asserts the literal source text**
  `"os.getcwd() if FROZEN else REPO" in SRC`, which is consumer `record_mcp.py:119`. This is
  the constraint-3 collision named at 30% in P4, and it is real: **T28 pins the mechanism of
  one of the 19 consumers, not just its behaviour.** See §5.

No `REPO` consumer outside the two named files needed an edit, so **gate 4 holds** without a
routing.

---

## 2. The defect, reproduced on a wheel built from this tree

Not inherited from the dispatch's read-back of the *published* wheel. Built here with
`python -m build`, installed into a fresh venv, run with the working directory set to this
checkout.

**Sub-prediction inside P5 — MISS.** I predicted `python -m build` was ~60% likely to be
absent from the pinned interpreter. It is present: **build 1.5.0**. Nothing was installed.

The wheel's payload is exactly `facet_index.py`, `record_mcp.py` and `dist-info/`. **No
`CLAUDE.md`, no `docs/`, no data files. P3: hit** on a tree-built wheel, not only on the
published one.

| invocation (cwd = this checkout) | before | after |
|---|---|---|
| `facet-index --help` | exit 0 | exit 0 |
| `facet-mcp --print-tools` | exit 0 | exit 0 |
| the `db:` line it prints | `<venv>\Lib\docs/index/facet.db` | `E:\AI\facet\docs/index/facet.db` |
| `facet-index build --db <scratch>` | **exit 2** `FileNotFoundError: <venv>\Lib\docs\experiments` | exit 0, 9 tables |
| `facet-index claims --db <real index>` | **exit 2** `FileNotFoundError: <venv>\Lib\CLAUDE.md` | exit 0 |
| `facet-index q erosion` (no `--db`) | **exit 2** `unable to open database file` | exit 0, correct rows |
| `facet-index q --db <real index>` | exit 0 | exit 0 |
| `facet-index q` + `$FACET_INDEX_DB` | **exit 2** — the var is not read | exit 0 |
| `record_query`, valid `--db` | REFUSED `CORPUS_NOT_FOUND` under `<venv>\Lib` | rows |
| `record_health` | `REFUSING` / `CORPUS_NOT_FOUND` | `SERVING_STALE` |

And with the working directory **outside any checkout**, after the fix:

| invocation | after |
|---|---|
| `facet-index build` / `claims` / `q` | **exit 4 = REFUSED**, naming both candidates and both markers |
| `facet-index --help`, `facet-mcp --print-tools` | exit 0 |
| `facet-index q --db <real index>` | exit 0 |
| `facet-index q` + `$FACET_INDEX_DB` | exit 0 |
| `record_build` | REFUSED `CORPUS_NOT_FOUND` |

### Two findings the dispatch did not contain

**F1 — `README.md:47` is wrong, and it was written hours ago at the v0.3.0 read-back.** It says
a wheel install *"currently works only for `q` and `claims`, and only with an explicit `--db`."*
Measured: **`claims` does not work** — `FileNotFoundError` on `<venv>/Lib/CLAUDE.md`, exit 2.
Only `q` did. `README.md` is outside the four named files, so this is **routed, not fixed**.
It is the E20-want-2 family again — a front-door claim drifting where no instrument looks —
and this is the fourth instance.

**F2 — `record_build` classified the new refusal as a builder defect.** `RootNotFound` reaching
`record_mcp.py`'s generic wrapper produced code `INTERNAL` with the hint *"This is a defect in
the builder, not in the corpus"*, which is exactly backwards. Found by running the tool, not by
reading it. Fixed in the same commit by catching it above the generic handler; `record_build` is
the only tool that reaches the builder without asking `_corpus_manifest` first.

---

## 3. The resolver as built, and the measurement behind each choice

```python
RECORD_MARKERS = ("CLAUDE.md", "docs/experiments")
def is_record_root(path)          # all markers present
def repo_candidates()             # (os.path.dirname(HERE), os.getcwd())
def resolve_repo(candidates=None) # first candidate that holds, else None
REPO = resolve_repo()
class RootNotFound(Exception)
def repo()                        # REPO, or raise -> run_contract -> EXIT_REFUSED
```

**The marker — measured, not reasoned.** `CLAUDE.md` alone is an ordinary filename. Under
`E:\AI` to depth 3, **26 directories carry one and exactly 1 also carries `docs/experiments`.**
A single-marker resolver binds a working directory that is a different repo entirely and then
fails deeper in — which is the defect being replaced, not a fix for it. Both markers are absent
from the built wheel, so the installed branch cannot key on itself. The reference is taken from
the record's own shape, not from the artifacts being judged.

**The candidate order.** `dirname(HERE)` first, so a source checkout takes the identical branch
it always took and cannot change behaviour; then `os.getcwd()`, which is where an installed
command is run from and is already the documented contract (`record_mcp`'s refusal has said
*"run it from a checkout of the facet repo"* since it was written, and the frozen branch has
resolved against cwd since v0.1.1).

**There is deliberately no walk upward from cwd.** It would let `facet-index` run from a
subdirectory, and it would also reach a *parent* that is a different record. The narrow rule is
the one the refusal message can state exactly. **This is the one design choice I consider
genuinely open** — it is a convenience question, not a correctness one, and it is routed.

**`REPO` is `None` when nothing holds, not a fallback string.** Constraint 2 says refuse; a
plausible-looking value is how `<venv>/Lib` became a banner four releases running, and a
fallback would only move the failure one caller downstream. With `None`, a consumer added
tomorrow that forgets the guard raises `TypeError` at once instead of silently joining onto a
wrong root — the failure is made impossible rather than detectable, which is this repo's stated
preference.

**Where the refusal lives.** `repo()` raises; `run_contract` maps `RootNotFound` to
`EXIT_REFUSED`, beside the fired-gate case. Not an `assert` — E21 Ruling 2 / E22 Ruling 9. It
was measured under `-O` and `PYTHONOPTIMIZE=1` by the suite's existing T30 sweep, which stays
green.

### The per-consumer table

**13 of 19 changed. I predicted 17, band 14–19 — a miss, outside the band.**

| site | verdict | why |
|---|---|---|
| `facet_index` 281, 326, 345, 384, 389, 398, 845, 2072, 2084 | **CHANGED** ×9 | corpus readers; `REPO` → `repo()` |
| `facet_index` 2188 | **CHANGED** | `--db` default was `join(REPO, DB_REL)` at parser-construction time; now `None`, resolved after parse |
| `record_mcp` 119 | **CHANGED** | `REPO or os.getcwd()`, so import survives a null root |
| `record_mcp` 495, 891 | **CHANGED** ×2 | `REPO and …startswith(REPO)` — `None` has no `startswith` |
| `record_mcp` 112 | unchanged | `REPO = facet_index.REPO` still holds; the name stays an attribute, now nullable |
| `record_mcp` 272, 275 | unchanged | the new null guard sits **above** them; they stay load-bearing for a different condition — a root that *exists* but is the wrong tree, which is what T21 monkeypatches |
| `record_mcp` 312 | unchanged | a string inside `REQUIRED_CONVENTIONS`; never a path use |
| `record_mcp` 494, 890 | unchanged | first lines of two-line expressions whose **second** lines took the guard |

**Where the miss came from.** The prediction treated each enumerated line as an independent
edit and reasoned about the *design fork* — (a) route every site through a resolver, ≈19; (b)
constant plus entry guards, ≈4. I built (a) and still got 13, because the fork was not what
governed the count. Six sites survived for four unrelated structural reasons, and two of them
(494, 890) are **line numbers of a statement whose other line changed**. That is E23 Ruling 12
one level further down: I checked the population was real, and did not ask what a *site* is
made of. Under a per-statement unit the answer is the same 13 — the two pairs collapse to two
changed statements — so the miss is not a unit artefact; it is that I predicted the wrong six.

---

## 4. The new tier, and its before/after

`tests/test_t32_installed_wheel.py`, **14 tests**, three groups.

- **the resolver, 5 hermetic legs** — including the can-fail leg first (`resolve_repo` on a
  directory that is not the record returns `None`), `repo()` raising rather than returning, the
  two-marker property, and that `facet_index.DB_ENV == record_mcp.DB_ENV` (one string, two
  modules — T27's pattern).
- **the wheel's geometry, 4 hermetic legs** — the two modules copied into a directory whose
  parent is not the record, then invoked. This is the wheel's defining property at the cost of a
  file copy, and it runs in CI.
- **the real artifact, 5 legs** — a wheel built from this tree, installed into its own venv, and
  then a verb: `q` with no `--db`, `claims`, the refusal outside a checkout asserting **exactly
  4**, the wheel's payload, and `--help` kept as a regression floor.

### Gate 3 — measured at both trees

Run against a `git worktree` at the pre-fix commit:

```
broken tree   13 failed, 1 passed
fixed tree    14 passed
```

The single pass on the broken tree is `test_t32_installed_wheel_help_and_print_tools_still_pass`
— deliberately so. It is the only check `release.yml` ever ran, and it is in the file to make
the point that its being green proved nothing.

**A weakness I found in my own tier, and repaired before committing.** On the first run against
the broken tree, **10 of the 13 failures were `AttributeError` on symbols that did not exist
yet** — the new API being absent, not the shipped artifact misbehaving. A leg that reds a tree
because it imports a new name is not testing the defect. The geometry legs now check the markers
by literal name, and the split became:

| failure mode on the broken tree | before repair | after repair |
|---|---|---|
| behavioural — the pre-fix code did the wrong thing | 3 | **8** |
| `AttributeError` — new symbol absent | 10 | 5 |

The 5 remaining are the resolver's own unit legs, which cannot be written any other way. This is
**P6's stated 10% risk** — the tier failing for the wrong reason — and it materialised; it was
found by looking at *why* each leg failed rather than at the count.

### Hermeticity — the measurement, per the dispatch

| half | hermetic? | measured |
|---|---|---|
| `pip install` of a local wheel | **YES** | `pip install --no-index --no-deps` needs no network, and `facet_index` is stdlib-only so every verb runs without `mcp` |
| `python -m build` | **NO** | it provisions an isolated build env from PyPI. `--no-isolation` **fails**: `pyproject` requires `setuptools>=77`, the pinned env has **70.2.0** |

So the tier is **not fully hermetic and it is not `artifacts`-marked either.** The wheel legs
carry `@pytest.mark.slow` and **skip with a named reason** when `build` is absent or cannot run;
`pytest.ini`'s `-rA` prints it. `artifacts` was rejected because it means *needs the recorded
trees under `FACET_ASSETS`*, which is false here, and using it would have deselected the tier in
CI under a wrong label.

**Consequence, stated rather than smoothed:** `ci.yml` installs no `build`, so **the five wheel
legs SKIP in CI** while the nine hermetic legs run. Adding `build==1.5.0` to `ci.yml` would put
them in CI, and `ci.yml` is **outside the four named files** — so it is routed, not done.

Measured in run `31292129637`, not predicted — `.........sssss`, and the reason printed by `-rA`:

```
SKIPPED [1] tests/test_t32_installed_wheel.py:279: `python -m build` is not installed in
  /opt/hostedtoolcache/Python/3.12.13/x64/bin/python - the wheel tier needs it to produce
  the artifact
```

Five such lines, each naming the interpreter. A silent skip would have been a check that cannot
fail; this one says what is missing and where.

---

## 5. Gate 2 — neither working path regressed

- **T28's five: byte-identical and passing.** `git diff HEAD -- tests/test_t28_frozen_runtime.py`
  is empty; `5 passed in 0.54s`.
- **This constrained the fix rather than merely being satisfied by it.** T28:78 asserts the
  literal `"os.getcwd() if FROZEN else REPO"`, so consumer `record_mcp.py:119` could not become
  `REPO = None`-clean by rewriting that expression. It is now
  `os.getcwd() if FROZEN else REPO or os.getcwd()` — the pinned substring intact, `import`
  surviving a null root. **The `FROZEN` branch is now subsumed by the resolver**: in a binary,
  `dirname(HERE)` is a temp dir that fails the marker test and cwd is tried next, so `REPO`
  already equals cwd. It was **kept, not deleted** — it states the intent at the site and T28
  pins it. **Whether a now-redundant branch should stay is routed.**
- **The source-checkout path is unchanged**: `resolve_repo` accepts the first candidate,
  `dirname(HERE)`, exactly as before; `facet_index.REPO == E:\AI\facet`; build + four-leg verify
  from the checkout pass.

---

## 6. Predictions scored

| # | prediction | measured | verdict |
|---|---|---|---|
| P1 | 17 of 19 consumers change, band 14–19 | **13** | **MISS**, outside the band |
| P2 | no consumer wants a different root; 2 want a DB path; refusal must be deferred | correct, and **3 sites are a third class** — 494/495/890/891 use `REPO` only as a display prefix, which I did not predict | **hit, incomplete** |
| P3 | the marker is absent from a built wheel | payload is exactly the two modules + `dist-info/` | **hit** |
| P4 | T28's five pass unchanged, first attempt (~70%) | they do — **and the 30% risk I named was simultaneously real**: T28 pins consumer 119's source text and constrained the design | **hit**, for a reason I half-predicted |
| P5 | not fully hermetic; `facet-index` half yes, `facet-mcp` half no | correct in shape; the true split is **install-yes / build-no**, not index-yes / mcp-no | **hit, wrong axis** |
| P5b | `python -m build` absent (~60%) | **present**, 1.5.0 | **MISS** |
| P5c | tier marked `artifacts` (~75%) | marked `slow` + self-skipping; `artifacts` rejected as a false label | **MISS** |
| P6 | the tier fails on the broken tree by construction (~90%); 10% risk of failing for the wrong reason | it fails — **and the 10% risk materialised**, 10 of 13 first-run failures were the wrong reason | **hit, with the named risk live** |
| P7 | the enumeration reproduces exactly (~75%) | exact, 20 references, 19 + definition | **hit** |
| P7b | ≥1 `REPO` reference outside the two files (~65%) | many; two are coupled, one constrained the design | **hit** |
| P8 | suite baseline 370 | **370** before, **384** after (+14) | **hit** |
| P9 | 6–9 new tests in one new file (~70%) | **14** in one new file | **miss on count, hit on shape** |

**Four clean misses (P1, P5b, P5c, P9-count), one hit whose named risk fired (P6), one hit on
the wrong axis (P5).** The blind rows did better than the inherited ones on shape and worse on
magnitude: every count I predicted was low except P1, which was high.

---

## 7. Gates

| # | gate | evidence |
|---|---|---|
| 1 | suite green before and after, artifacts tier, baseline 370 | **384 passed in 257.54s** (370 + T32's 14). Baseline 370 reproduced before the edit |
| 2 | T28's five pass unchanged; source-checkout path unchanged | `git diff` on T28 empty; `5 passed`; checkout resolves to itself via candidate 1 |
| 3 | the new tier fails before and passes after | **broken tree 13 failed / 1 passed; fixed tree 14 passed.** The 1 is the `--help` floor, on purpose |
| 4 | no edit outside the four named files | `git diff --numstat HEAD~1 HEAD`: `tools/facet_index.py`, `tools/record_mcp.py`, `.github/workflows/release.yml`, `tests/test_t32_installed_wheel.py`. **Nothing else.** F1 (`README.md`) was routed rather than fixed for this reason |
| 5 | CI green, both scanners | **PASS** — run [`31292129637`](https://github.com/mcp-tool-shop-org/facet/actions/runs/31292129637) on `e8b24db`, `completed / success`. Read at step level: `hermetic set` ✓ · `dependency scan - python` ✓ · `dependency scan - npm` ✓. T32 in CI: **9 passed, 5 skipped**, each skip naming `python -m build` as the missing thing. **No gate fired in this arc** |

---

## 8. `release.yml` — the gate that should have caught this

The step named *"Verify the wheel runs from a clean venv"* ran `--help` and `--print-tools`, and
was green through v0.1.0, v0.1.1, v0.2.0 and v0.3.0 while the package could not find the record.
It now runs: `build --db <scratch>` (the corpus verb that died), `q erosion` with no `--db` (the
DB verb that died), the refusal from `/tmp` **asserting exactly 4** — because a non-zero check
would have passed on the defect, which returned 2 — and the banner's path. The two original
commands stay, in place, as a floor.

**Dry-run, on this rig, against both wheels** (the sequence extracted to a script and run with
the local venvs):

```
against the FIXED wheel     exit 0   "verbs run, the refusal returns 4, and the banner names ..."
against the BROKEN wheel    exit 2   FileNotFoundError: <venv>\Lib\docs\experiments
```

**One leg could not be exercised on this rig**: `case "$db" in "$PWD"/*)` compares with a forward
slash, and on Windows `os.path.join` produces `E:\AI\facet\docs/index/...`. The workflow is
`runs-on: ubuntu-latest`, where the separator is `/`. Every other line ran green locally; that
one is reasoned, not measured. **`release.yml` triggers only on `release: published`, so this
step does not run on a push — it will first execute at the 0.3.1 release.** It is a gate that has
not yet fired in anger, and it is written here as that rather than as a pass.

---

## 9. Findings and open items, routed

1. **F1 — `README.md:47` says `claims` succeeds on a wheel install; it exits 2.** Outside the
   four named files. After this fix both verbs work from a checkout, so the paragraph is stale in
   two directions at once.
2. **F2 — `record_build` mis-classified the refusal as `INTERNAL`.** Fixed in scope; reported
   because it was found by running rather than reading.
3. **Should the resolver walk upward from cwd?** Convenience, not correctness. Not done.
4. **Should the now-subsumed `FROZEN` branch stay at `record_mcp.py:119`?** Kept, because T28
   pins it and it states intent. It is dead weight if the resolver is trusted.
5. **The five wheel legs skip in CI** for want of `build` in `ci.yml`, which is outside the four
   named files.
6. **`CHANGELOG.md` has no E24 entry** — outside the four named files; belongs to the 0.3.1 act.
7. **T28:78's source-text assertion is the only thing standing between this design and a cleaner
   `record_mcp.py:119`.** It did its job — it stopped a silent behaviour change — and it is worth
   noting that it constrains rather than merely observes.

---

## 10. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every number here is a command's output; the wheel is built from this tree, not inherited; the enumeration is re-measured; the broken tree is a `git worktree` at a named commit |
| ANDON_AUTHORITY | 3 | the refusal `raise`s and is mapped to `EXIT_REFUSED` inside the tool, not in a shell chain; gate 3 measured at both trees; the tier's own weakness reported rather than smoothed |
| NAMED_COMPENSATORS | 2 | this arc publishes nothing and touches no recorded tree; the compensator is `git revert e8b24db`. Not 3: **0.3.0 is published with the defect and no compensator un-ships it** |
| DECOMPOSE_BY_SECRETS | 3 | one resolver, three runtimes; the markers, the candidate order and the refusal are separable and separately tested |
| UNCERTAINTY_GATED_HUMANS | 3 | four design choices routed with their consequences rather than picked: the upward walk, the retained `FROZEN` branch, `ci.yml`, and `README.md` |
| EXTERNAL_VERIFIER | 3 | the verifier is a wheel built here, installed into a real venv, running real verbs — and the same sequence run against the pre-fix artifact to show it fails there |

---

## 11. Halt

Stopping here. **0.3.1 is a separate act at the Director's word**, and the advisor rules at
`E24-ruling.md`.
