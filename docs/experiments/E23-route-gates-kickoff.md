# E23 — the route's gates, and the ones no test has ever run

**Written by the advisor, 2026-08-08, dispatched at [E22 Ruling 4](E22-ruling.md).**
Halts at `E23-route-gates-report.md`; the advisor rules at `E23-ruling.md`.

---

## The question

E22 converted the 88 ruled gate sites and left **191 ANDON-carrying asserts** that
`python -O` still deletes. **57 of them are in route tools** — the twelve scripts that
produced four accepted assets. Does the same pure move hold there, on files that
**no test has ever executed**?

## Scope — ENUMERATED, not derived

**Two consecutive arcs have had a scope-number defect, and both came from arithmetic
rather than measurement** (E22 Ruling 2 and Ruling 4). So this dispatch carries the
enumeration itself. Verify it; do not inherit it.

```
tools/ TOP LEVEL, asserts whose message carries the ANDON token:

  bake_hero_prep.py        15   ⚠ BLENDER      brush_cloud_step.py       9
  subject_profile.py        6                  e13_harmonize.py          5
  bake_hero_fuse.py         4                  bake_hero_pack.py         4   ⚠ BLENDER
  silhouette_masks.py       4                  cull_unseen.py            3
  export_asset_source.py    2                  palette_gate.py           2
  resample_atlas.py         2                  restylize_views.py        1

  TOTAL 57 sites across 12 files
```

**In:** those 57 sites. **Out:** everything else — the 132 `diagnostics/` sites, the one
in `superseded/` (**never**, by E22 Ruling 4 — those tools are kept so they fail the same
way), the one in `verify/`, the 15 non-ANDON asserts, and the 44 ANDONs that already
`raise`.

**A site that turns out not to be a gate is a finding for the ruling, not a scope
reduction.** A site outside the 57 that turns out to be one is the same. Do not adjust
the boundary; report it.

## The bar — unchanged from E22, because it worked

> **Every conversion is a PURE MOVE.** No behaviour change rides along, no message
> improved in passing, no condition tightened. `COND` and `MSG` keep their source text
> character for character; only leading whitespace on continuation lines moves.

```
assert COND, MSG   ->   if not (COND):
                            raise AssertionError(MSG)
```

**`AssertionError`, and here is why it is not automatic.** In E22 the type was forced —
`facet_index.run_contract` catches it specifically. **Measured for E23: there is exactly
one `except AssertionError` in all of `tools/` (`facet_index.py:216`), and none of these
twelve files is `facet_index`.** So nothing forces the type here. It stays
`AssertionError` anyway, because `assert cond, msg` raises `AssertionError(msg)` and
**the pure move is the one that changes nothing** — matching a file's existing
`SystemExit` style would be a behaviour change wearing a consistency argument.

**Measured shapes, so no one re-derives them:** 31 of the 57 are multiline · **0 are
`not`-conditions** (E22 had 3, so the negation rule is uniform here) · 0 share their
first line with another statement · 0 lack a message. The splice is safe by line range —
**verify that before relying on it.**

## ⚠ What is different from E22, and it is the whole difficulty

**Zero of the twelve files are reached by any test.** Measured: no file under `tests/`
mentions any of them. E22's safety came from T7's byte-identity replay, T10 and T26's
three fired ANDONs. **E23 has no behavioural net at all.** That is not a reason to
lower the bar; it is the reason the AST proof carries the whole load and the tests
this arc owes are not optional.

**And the twelve are not one runtime:**

| | files | sites | can the pinned interpreter run it? |
|---|---|---|---|
| pinned-interpreter tools | **10** | **38** | yes — `--help` exits 0 writing nothing, measured on all ten |
| **Blender tools** | **2** | **19** | **no** — `bake_hero_prep` and `bake_hero_pack` `import bpy`; `--help` dies at the import |

**11 of the 12 are SCRIPTS, not modules** — they execute at import, and three
(`bake_hero_pack`, `silhouette_masks`, `resample_atlas`) have **zero function
definitions**. E20 met this exact wall and refused to restructure accepted-asset tooling;
that refusal stands. **Do not import these files in a test.** It runs the tool.

## Tests ride the commit — T31, and what is honestly reachable

The tests-ride-the-commit law binds: twelve tool files change, so tests for them land in
the same commit. What is reachable was measured before it was asked for.

1. **`py_compile` on all 12** — hermetic, needs no `bpy`, instant, and it catches the
   real risk of a mechanical rewrite: a splice that breaks indentation or syntax.
   **Measured now: 12/12 compile clean**, so this is a genuine before/after.
2. **`--help` subprocess smoke on the 10 non-Blender tools**, under a normal
   interpreter **and** `-O` **and** `PYTHONOPTIMIZE=1`: exit 0, and **the scratch cwd is
   still empty afterward**. Measured on all ten today. This proves the module still
   parses and reaches argparse after the splice.
3. **The structural law extended** — no ANDON gate in the twelve is an `assert`, by AST,
   with a **can-fail leg** that plants one and sees it caught.
4. **Fire what can be fired.** Some gates take synthetic input cheaply (`palette_gate`
   takes images; `subject_profile` takes JSON). **Measure which are reachable
   hermetically and fire those in all three modes, asserting nothing was written.**
   For the rest, **report what could not be fired and why** — E20's refusal to invent
   three units that could not exist is the precedent, and it was that arc's largest
   deliverable.

**No test may assert that `PYTHONOPTIMIZE=1` disables a gate.** That anchors the defect.
The one place the mechanism is pinned is on throwaway source, as T30 already does.

**The two Blender files get 1 and 3 only, and that gap is stated in the report rather
than papered over.** If a Blender-runtime smoke is cheap, it is artifacts-tier and
optional; do not build a Blender harness for this arc.

## ⚠ Compensators — the same gap as E22, and these tools are worse

E22 scored `NAMED_COMPENSATORS` at **1** and the row earned it. **It is worse here.**
E22's seven files were largely measurement and index tooling; **these twelve are the
route** — they bake, cull, resample, project and export into `E:\AI\training`, and
**those trees are not in git.** There is no `git revert` for them.

Binding, and gates rather than suggestions:

- **Manifest the recorded root BEFORE anything runs** — including before the baseline
  suite run, because the artifacts tier touches those trees. E22's run was 7,312 files
  / 16.3 GB / 76 s; reuse its instrument. **Re-check after the baseline run and at the
  halt.**
- **Never point one of these tools at a recorded tree.** Every smoke and every fired
  gate runs in a scratch cwd with scratch output paths. `tests/conftest.py`'s
  `copy_state()` already implements this discipline — E22 found it predated the
  request.
- **Any modification to the recorded trees halts the arc**, under gate 3.

## Predictions — committed BEFORE any file under `tools/` is opened

Write and commit `E23-predictions.md` first, disclosing blindness per row. Predict at
least:

1. How many of the 57 sites the splice-by-line-range handles without a hand fix.
2. Whether `py_compile` and the `--help` smoke both pass at every site after conversion —
   and if you predict yes, say what a no would look like.
3. **How many of the 57 gates you can fire hermetically** on synthetic input. State it as
   a count with a band.
4. Whether any of the 57 is not a gate at all.
5. Whether any of the twelve files carries a handler that would newly catch the raise.
   *(Measured for you at dispatch: one broad `except Exception` exists among the twelve,
   in `palette_gate.py:189`, and it wraps a **font load**, not a gate. Verify it.)*

**The calibration lesson from E22 is binding: check that the population is real before
you predict its density.** P18 predicted 4 against a measured 175 because it estimated a
property of a class that did not exist. Every number above is a property of an enumerated
set — count the set first.

## Gates

1. **Suite green before and after**, full artifacts tier, under the pinned interpreter.
   Baseline is **275**.
2. **Whole-file AST equality** for each of the twelve, against that file **as git had it
   at the prior commit**, with the negation rule applied in the tree — E22's
   `pure_move_proof.py`. **A file that does not prove identical reverts.** Comment tokens
   diffed separately and unchanged.
3. **No edit outside the twelve** under `tools/`, and none to `canon/`, `profiles/`, the
   citable trees, the seeded set, or a closed ruling. Tests and the docs this dispatch
   names are expected — E22's F3 read gate 3 as governing tool code and that reading is
   ratified here explicitly, so no one has to re-derive it.
4. **CI green**, both dependency scanners.
5. **The tree manifest holds** — 0 added, 0 removed, 0 changed, checked three times.

## Out of scope

The 132 `diagnostics/` sites · `superseded/`'s one, permanently · `verify/`'s one · the
15 non-ANDON asserts · unifying `SystemExit` (E22 Ruling 5; **44 sites repo-wide**, three
of them inside E23's own target files — report the collision, do not resolve it) ·
extending `4 = REFUSED` to these tools (E22 Ruling 6 ruled no) · restructuring any script
into a module · P5 · the measurement MCP · **the release**.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the scope is **enumerated per file**, not derived; the conversion rule, the interpreter, the baseline suite number and the three smoke modes are literal; the Environment block below is present at dispatch rather than amended in later |
| ANDON_AUTHORITY | 3 | five gates; gate 2 is the strong form — **a file that does not prove identical REVERTS**; the arc halts at a report and decides nothing |
| NAMED_COMPENSATORS | **2** | the manifest, the scratch-cwd rule and the halt-on-modification are binding and the instrument exists and has held three times. Not 3: **the trees are still not in git**, so the compensator is a restore-from-source and not a revert, and no rehearsal of that restore has ever been performed |
| DECOMPOSE_BY_SECRETS | 3 | scope split by **what changes together**: route tools vs diagnostics vs superseded, then again by **runtime** (pinned interpreter vs Blender), because those two groups can be tested in entirely different ways |
| UNCERTAINTY_GATED_HUMANS | 3 | the genuinely open calls are pre-routed to the ruling — a site that is not a gate, a gate outside the 57, the `SystemExit` collision in three target files — and none is an executor's to settle |
| EXTERNAL_VERIFIER | 2 | the verifier is whole-file AST equality against the prior commit plus `py_compile`, the three-mode smoke and CI — none of which the converting agent can talk past. skip: no cross-family LLM; every outcome is a byte comparison, an exit code or an AST equality |

## Environment

- Everything under the **absolute** pinned interpreter
  `E:\AI-Models\trellis2-env\Scripts\python.exe`. Bare `python` lacks `open3d` and `mcp`;
  **T18 refuses it loudly in one line.**
- **`bake_hero_prep` and `bake_hero_pack` are Blender scripts** — do not try to run them
  under the pinned interpreter, and run any Blender work **through PowerShell**.
- Shared working copy: file-specific `git add`, pathspec-scoped commits, **never
  `git add -A`**, no stash. The DB and its certificate commit as a **pair**, at a session
  boundary only.
- Fold-marked failures against a live corpus: **run-then-rerun once** (E18 Ruling 2l).
- **ASCII prints.** CI is paths-gated over `tools/ tests/ pytest.ini .mcp.json
  .github/workflows/ pyproject.toml package.json bin/`. **Never leave CI red.**

## Halt

`E23-route-gates-report.md`: predictions scored with blindness disclosed, the per-file
conversion table, the AST proof for all twelve, the smoke matrix, **which gates could be
fired and which could not, with reasons**, the manifest result, findings, tests added,
and gates with their evidence. **Then stop.** The advisor rules at `E23-ruling.md`; a
release is a separate act at the Director's word.
