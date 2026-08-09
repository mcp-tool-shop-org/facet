# E25 — the last of the deletable gates

**Written by the advisor, 2026-08-08, dispatched at [E22 Ruling 4](E22-ruling.md) and
[E23 Ruling 9](E23-ruling.md).** Halts at `E25-diagnostics-gates-report.md`; the advisor
rules at `E25-ruling.md`.

**⚠ RUNS IN PARALLEL WITH [E24](E24-installed-paths-kickoff.md). Read the coordination
section before you touch anything.**

---

## The question

E22 converted 88 gates and E23 converted 57. **133 ANDON checks are still bare
`assert`s** — every one deleted by `python -O`. They are the measurement instruments:
the sheets, probes and readouts that produced the evidence for four accepted assets.
Does the same pure move close the class?

## Scope — ENUMERATED

```
tools/diagnostics/   132 sites across 42 files
tools/verify/          1 site  across  1 file
                     ---------------------------
  IN SCOPE           133 sites across 43 files
```

**Out, permanently:** `tools/superseded/`'s **1** site. [E22 Ruling 4](E22-ruling.md)
ruled it never converted — those tools are kept precisely so anyone can run them and
watch them fail the same way, and changing how they fail is the one thing that spoils
them. **Leave it, and say in the report that you left it.**

Also out: the 145 already converted · the 15 non-ANDON asserts ([E22 Ruling 3](E22-ruling.md)
read all 15 and ratified the axis) · the 44 ANDONs that already `raise` · anything under
`tools/facet_index.py` or `tools/record_mcp.py` — **those belong to E24 and you may not
touch them.**

**Measured at dispatch — verify, do not inherit:** 50 multiline · **5 `not`-conditions**
(E23 had 0, so the negation rule is *not* uniform here) · 0 sharing a first line · 0
missing a message.

## ⚠ PARALLEL COORDINATION — this is new and it binds

E24 is live in the same working copy. Verified disjoint at dispatch:

| | E24 owns | E25 owns |
|---|---|---|
| tools | `facet_index.py`, `record_mcp.py` | `diagnostics/*` (42), `verify/*` (1) |
| tests | `test_t28_*`, a new installed-wheel tier | `test_t31_route_gates.py` (the census pin), a new file |
| workflows | `release.yml` | none |

**Measured:** no file under `tools/diagnostics/` or `tools/verify/` imports `facet_index`
or `record_mcp`, so there is no runtime coupling either.

Binding rules:

- **File-specific `git add`, always. Never `git add -A`, never `git commit -a`.** The
  other arc's uncommitted work is in this tree; a broad add commits their half-finished
  edit under your message.
- **`git pull --rebase` before every push.** Two sessions push to `main`.
- **Do not run `-m fold` tests while the other arc is mid-run if you can avoid it.**
  [E23 Ruling 10](E23-ruling.md): the concurrent writer can be *another session*, and now
  there genuinely is one. On a `fold` failure apply run-then-rerun once (E18 Ruling 2l)
  and **say in the report that a second session was live**, so the failure is attributable.
- **If you find a defect in E24's files, REPORT IT. Do not fix it.**

## The bar — unchanged, because it has held twice

> **Every conversion is a PURE MOVE.** No behaviour change rides along, no message
> improved in passing, no condition tightened. `COND` and `MSG` keep their source text
> character for character; only leading whitespace on continuation lines moves.

```
assert COND, MSG   ->   if <negate(COND)>:
                            raise AssertionError(MSG)

negate(COND) = X            when COND is `not X`     (5 sites — CHECK EACH)
negate(COND) = not (COND)   otherwise                (128 sites)
```

**`AssertionError`, and the reason is the same as E23's:** `assert cond, msg` raises
`AssertionError(msg)`, so it is the move that changes nothing. **28 ANDONs in this scope
already raise `SystemExit`, across 12 files** — mixed populations again. [E22 Ruling 5](E22-ruling.md)
ruled they stay; `SystemExit` is not deletable by `-O` and does not carry this defect.
**Report the collision, do not resolve it.**

**The primary instrument is whole-file AST equality** against each file as git had it at
the prior commit, with the negation rule applied in the tree. E23's `pure_move_proof.py`
is the pattern. **A file that does not prove identical REVERTS.** Comment tokens diffed
separately.

## Tests ride the commit — T32, and the census pin moves

**Measured at dispatch, so the tier is real rather than hoped for:**

- **`py_compile` on all 43** — hermetic, instant, and it catches what a bad splice
  actually breaks.
- **`--help` subprocess smoke: 41 of the 43 exit 0 writing nothing**, under a normal
  interpreter and `-O` and `PYTHONOPTIMIZE=1`. Two are excluded with measured reasons —
  `diagnostics/e12_head_render.py` (`import bpy`) and
  `diagnostics/e04_make_brush_prompts.py`, which does **file work before argparse** and
  dies on a missing profile path. ⚑ **That second one is a finding in its own right and
  belongs in the report**, not a reason to widen an exclusion quietly.
- **The structural law extended** to the 43, by AST, with a **can-fail leg** that plants
  an ANDON assert and sees it caught.
- **`tests/test_t31_route_gates.py:80`'s `REMAINING_ELSEWHERE = 134` must move.** After
  this arc it is **1** — `superseded/`'s permanently-excluded site. That constant is
  [E23 Ruling 9](E23-ruling.md)'s structural fix for the scope-number defect: it is the
  thing that makes a scope impossible to drift silently, so **move it deliberately, in
  the commit that earns it, and state the new number in the report.**
- **Fire what can be fired.** These are one-shot instruments and most need recorded
  trees. **Measure which fire hermetically on synthetic input, fire those in all three
  modes, and report what could not be fired and why.** E20's refusal to invent units
  that could not exist is the precedent; a short honest list beats a padded one.

**No test may assert that `PYTHONOPTIMIZE=1` disables a gate.** T30 pins the mechanism on
throwaway source; depend on that rather than repeating it.

## Compensators

**These tools mostly READ.** They produce sheets, probes and readouts — but several write
their output beside a recorded tree, and **those trees are not in git**, so there is no
`git revert` for them.

- **Manifest the recorded root before anything runs**, including before the baseline
  suite run. E23's instrument covered 7,312 files in 76 s and held four times. **Re-check
  after the baseline run and at the halt.**
- **Never point one of these tools at a recorded tree.** Every smoke and every fired gate
  runs in a scratch cwd with scratch output paths.
- **Any modification to the recorded trees halts the arc** under gate 3.

## Predictions — committed BEFORE any file under `tools/` is opened

Write and commit `E25-predictions.md` first, blindness disclosed per row. Predict at
least: how many of the 133 the splice handles without a hand fix; whether `py_compile`
and the smoke both pass at every site after conversion; **how many of the 133 fire
hermetically** (a count with a band); whether any of the 133 is not a gate; and how many
of the 42 diagnostics files carry a `SystemExit` ANDON beside an assert one.

**Both prior calibration lessons bind.** E22: *check that the population is real before
you predict its density* — this population is enumerated above, count it. E23: *check
what the metric's unit is* — "fires hermetically" is a property of a **site's inputs**,
not of a file's character.

## Gates

1. **Suite green before and after**, full artifacts tier. Baseline **370** *(E24 may move
   it; re-measure your own baseline and say what it was)*.
2. **Whole-file AST equality for each of the 43.** A file that does not prove identical
   **reverts**. Comment tokens unchanged.
3. **No edit outside the 43 under `tools/`** — and **nothing in E24's two files** — none
   to `canon/`, `profiles/`, the citable trees, the seeded set or a closed ruling.
4. **CI green**, both dependency scanners. If CI fires on the *environment* rather than
   the result, [E23 Ruling 2](E23-ruling.md) governs what you may repair.
5. **The tree manifest holds** — 0 added / 0 removed / 0 changed.
6. **`superseded/`'s one site is untouched**, and the report says so.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | scope enumerated per directory with per-file counts available; shapes, the smoke tier, the `SystemExit` mix and the two smoke exclusions all measured at dispatch and quoted |
| ANDON_AUTHORITY | 3 | six gates; gate 2 is the strong form — a file that does not prove identical **reverts**; gate 6 protects a permanent exclusion from being tidied away |
| NAMED_COMPENSATORS | **2** | the manifest, scratch-cwd rule and halt-on-modification are binding, and the instrument has held four times. Not 3: the recorded trees remain outside git, so the compensator is a restore-from-source that has still never been rehearsed |
| DECOMPOSE_BY_SECRETS | 3 | scope is drawn by *what the tools are for* — instruments, not route — which is also the axis that makes it disjoint from E24; the parallel-ownership table is the same principle applied to two live sessions |
| UNCERTAINTY_GATED_HUMANS | 3 | the `SystemExit` collision, any non-gate site, the smoke exclusions and the fireable set are all routed to the ruling with their consequences |
| EXTERNAL_VERIFIER | 2 | whole-file AST equality against the prior commit, `py_compile`, the three-mode smoke and CI — none of which the converting agent can talk past. skip: no cross-family LLM; every outcome is a byte comparison, an exit code or an AST equality |

## Environment

- Everything under the **absolute** pinned interpreter
  `E:\AI-Models\trellis2-env\Scripts\python.exe`. Bare `python` lacks `open3d` and `mcp`;
  **T18 refuses it loudly in one line.**
- `diagnostics/e12_head_render.py` imports `bpy` — **do not try to run it here**, and run
  any Blender work through PowerShell.
- Shared working copy **with a second live session**: see the coordination section. DB +
  certificate commit as a **pair**, at a session boundary only — **and if E24's seat has
  already folded the pair, do not fold it again.**
- **ASCII prints.** CI is paths-gated over `tools/ tests/ pytest.ini .mcp.json
  .github/workflows/ pyproject.toml package.json bin/`. **Never leave CI red.**

## Halt

`E25-diagnostics-gates-report.md`: predictions scored with blindness disclosed, the
per-file conversion table, the AST proof for all 43, the smoke matrix, which gates fired
and which could not with reasons, the new `REMAINING_ELSEWHERE` value, the manifest
result, findings, tests added, and gates with evidence. **Then stop.** The advisor rules
at `E25-ruling.md`; a release is a separate act at the Director's word.
