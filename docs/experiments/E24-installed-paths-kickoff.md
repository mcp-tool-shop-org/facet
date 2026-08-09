# E24 — the install that cannot find the record

**Written by the advisor, 2026-08-08, dispatched at the v0.3.0 release read-back.**
Halts at `E24-installed-paths-report.md`; the advisor rules at `E24-ruling.md`.
Targets **0.3.1** — a defect fix, no new capability.

---

## The question

`pip install facet-mcp` gives you two commands that **cannot find the record**. Can the
root be resolved so that a source checkout, a frozen binary and a wheel install all work
— without breaking either of the two paths that work today?

## What was measured at the read-back — verify it, do not inherit it

The published **0.3.0** wheel, with the working directory set to a real facet checkout:

```
facet-index --help  ·  facet-mcp --print-tools    WORK   <- exactly what release.yml runs
the db: line --print-tools prints                 <venv>\Lib\docs/index/facet.db - cannot exist
facet-index build                                 RUNTIME_ERROR, no <venv>\Lib\docs\experiments
facet-index q   (no --db)                         RUNTIME_ERROR, unable to open database file
facet-index q --db <a real index>                 WORKS, exit 0, correct rows
record_get, even with a valid --db                REFUSED: no record corpus under <venv>\Lib
```

**Mechanism, located.** `facet_index.py` ships as a **top-level py-module**, so on a
wheel install `__file__` is `<venv>/Lib/site-packages/facet_index.py` and
`facet_index.py:69-70` computes `REPO = dirname(dirname(__file__))` = **`<venv>/Lib`**.

**Not a v0.3.0 regression:** the published 0.2.0 wheel fails identically under its own
`<venv>/Lib`. **The `npx` binary is unaffected** — v0.1.1 fixed the *frozen* branch and
left the *wheel* branch behind.

**Second defect, same read-back.** `$FACET_INDEX_DB` is honoured by `facet-mcp`
(`record_mcp.py:138`) and has **no counterpart in `facet_index.py`**, while the README
said *"point either at an index with `--db` or `$FACET_INDEX_DB`."* The README is already
corrected; the code is not.

## Scope — ENUMERATED

**19 `REPO` consumers**, measured, and a root cause has as many sites as it has callers:

```
facet_index.py   :70 (the definition) · 281 · 326 · 345 · 384 · 389 · 398 · 845
                 · 2072 · 2084 · 2188 (the CLI's --db default)
record_mcp.py    :112 (re-export) · 119 (DB_DEFAULT) · 272 · 275 · 312 · 494 · 495
                 · 890 · 891
```

**In:** the root resolution and its consumers, `facet_index`'s `--db` default, and
`$FACET_INDEX_DB` support in `facet_index`. **Files:** `tools/facet_index.py`,
`tools/record_mcp.py`, `tests/`, `.github/workflows/release.yml`.

**Out:** a corpus-selecting env var or flag — that is a **new surface** and needs a
ruling, not an executor's pick · the 134 remaining ANDON asserts · P5 · the measurement
MCP · the tag.

## ⚠ Three constraints that are rulings, not preferences

**1. `$FACET_INDEX_DB` selects WHICH DERIVED DB, NEVER WHICH CORPUS.** That is the
existing design, stated at `record_mcp.py:136-137`. **Do not repurpose it as the corpus
root** to make this easier. Extending it to `facet_index` is in scope precisely because
it stays a DB selector there too.

**2. A resolver that cannot find a corpus MUST REFUSE.** Never silently resolve to a
directory that does not contain one — that is how a wrong path became a plausible-looking
banner in the first place. The refusal already has a code: **`4 = REFUSED`** (E22, E23),
and `record_mcp.py:272-275` already refuses with a legible message. **Extend that
behaviour; do not invent a fallback that guesses.**

**3. Neither working path may regress.** The source checkout and the frozen binary both
work today and **T28 pins the frozen branch in five tests**. Those tests pass unchanged,
or the change is wrong.

## The design hypothesis — measure it, do not obey it

`FROZEN` is a **proxy** for *"REPO is not a real root"*. It was the right fix for the
case it was written for and it is blind to the wheel case, which is neither frozen nor a
checkout. This repo's own law is **test the property, not a geometric proxy for it** —
and the property is *does this directory actually contain the record*. The codebase
already has that test: `record_mcp.py:272` checks
`os.path.exists(os.path.join(REPO, "CLAUDE.md"))`.

So the hypothesis is: **resolve the root by checking candidates for a marker, in a
declared order, and refuse if none holds.** The executor measures whether that is
sufficient, what the marker should be, and what the candidate order is. **Report the
options with their consequences; the advisor rules any that are genuinely open.**

⚑ **A caution earned three times in this repo:** whatever the marker is, it must not be
a file that exists in a *published wheel*. **Measured at dispatch so you do not have to
re-derive it — verify it anyway:** the published 0.3.0 wheel installs exactly
`facet_index.py`, `record_mcp.py`, two console scripts and `dist-info/`. **No
`CLAUDE.md`, no `docs/`, no data files of any kind.** So the marker `record_mcp.py:272`
already uses is safe by construction: it is present in every checkout and can never be
present in an install. That is a reason to keep it, not a reason to skip checking it.

## Tests ride the commit — and the missing tier is the point

**T28 has five tests for the frozen branch and ZERO for the installed-wheel branch.**
That hole is why this shipped in four consecutive releases.

- **The new tier: build a wheel, install it into a temp venv, and run a VERB.** Not
  `--help`, not `--print-tools` — those are exactly what has been green throughout. A
  verb that touches the corpus and a verb that touches the DB.
- Whether that tier is hermetic or `artifacts`-marked is the executor's measurement to
  report: it needs `python -m build` and a network-free `pip install` of a local wheel.
  **If it cannot be hermetic, say so with the reason** rather than making it pass by
  narrowing it.
- **T28's five frozen tests run unchanged.**
- A **can-fail leg** for the resolver: prove it refuses when no candidate holds.
- `$FACET_INDEX_DB` on `facet-index`, asserted through a subprocess.

**`release.yml`'s wheel step must run a verb.** It currently reads:

```
/tmp/verify/bin/facet-index --help > /dev/null
/tmp/verify/bin/facet-mcp --print-tools > /dev/null
```

That step is named *"Verify the wheel runs from a clean venv"* and it is the gate that
should have caught this. **Make it run what a user runs.**

## Predictions — committed BEFORE any source file is opened

Write and commit `E24-predictions.md` first, disclosing blindness per row. Predict at
least: how many of the 19 `REPO` consumers need to change; whether any consumer wants a
*different* root than the others; whether the marker you expect to use is present in a
built wheel; whether T28's five pass unchanged on the first attempt; and whether the new
tier can be hermetic.

**E23's lesson binds: check what the metric's unit is, not just that its population is
real.** "How many consumers change" is a property of an enumerated set of 19 — count
before you estimate.

## Gates

1. **Suite green before and after**, full artifacts tier. Baseline **370**.
2. **T28's five frozen tests pass unchanged**, and the source-checkout path is
   unchanged — verified by running the suite from the checkout as now.
3. **The new installed-wheel tier fails before the fix and passes after.** A tier that
   passes on the broken tree is not testing this.
4. **No edit outside the four named files.**
5. **CI green**, both dependency scanners.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the 19 consumers are enumerated by line; the measured failure table is literal; the baseline suite number, the marker precedent and the exact `release.yml` lines are quoted |
| ANDON_AUTHORITY | 3 | five gates; gate 3 is the strong form — **a tier that passes on the broken tree is not testing this**; the arc halts at a report |
| NAMED_COMPENSATORS | **2** | this arc touches no recorded tree and publishes nothing, so the compensator is `git revert` plus a 0.3.2 — real, and stated. Not 3: **0.3.0 is already published with the defect**, and no compensator un-ships it; the README and the release body are corrected instead, which is mitigation and not undo |
| DECOMPOSE_BY_SECRETS | 3 | scope is drawn by *what resolves a path* rather than by file; the three runtimes (checkout / frozen / wheel) are the axis, and they are what changes together |
| UNCERTAINTY_GATED_HUMANS | 3 | the design hypothesis is explicitly *measure it, do not obey it*; the marker choice, the candidate order and the hermeticity of the new tier are routed to the ruling with their consequences |
| EXTERNAL_VERIFIER | 3 | the verifier is **an actual wheel installed into an actual venv running an actual verb** — the one check none of the four green releases performed. CI runs it too |

## Environment

- Everything under the **absolute** pinned interpreter
  `E:\AI-Models\trellis2-env\Scripts\python.exe`. Bare `python` lacks `open3d` and `mcp`;
  **T18 refuses it loudly in one line.**
- Building a wheel needs `python -m build`; if it is absent, **report that rather than
  installing tooling into the pinned environment without saying so.**
- Shared working copy: file-specific `git add`, pathspec-scoped commits, **never
  `git add -A`**, no stash. DB + certificate commit as a **pair**, session boundary only.
- **ASCII prints.** CI is paths-gated; `.github/workflows/**` is inside the gate, so a
  workflow edit triggers it. **Never leave CI red** — and if a gate fires because the
  environment cannot run the measurement, [E23 Ruling 2](E23-ruling.md) governs what you
  may repair and what you must halt on.
- ⚠ **Do not edit `.github/release-notes-v0.3.0.md`** — it is the published body of a cut
  release and already carries its post-publication correction.

## Halt

`E24-installed-paths-report.md`: predictions scored with blindness disclosed, the
resolver as built with the measurement behind each choice, the per-consumer table, the
before/after of the new tier, T28's five re-run, findings, tests added, and gates with
evidence. **Then stop.** The advisor rules at `E24-ruling.md`; **0.3.1 is a separate act
at the Director's word.**
