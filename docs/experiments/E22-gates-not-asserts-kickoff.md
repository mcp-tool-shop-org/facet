# E22 — the gates an environment variable deletes

**Written by the advisor, 2026-08-08 (night), dispatched at [E21 Ruling 2](E21-ruling.md).**
Halts at `E22-gates-report.md`; the advisor rules at `E22-ruling.md`.

---

## The question

**The repo's ANDONs are bare `assert`s.** Does converting them to raises preserve every
anchored behaviour *exactly*, and does the write path then refuse under `-O` as it does
without it?

## What was measured at the ruling seat — verify it, do not inherit it

```
tools/                            294 bare asserts across 72 files
```

Gates carrying the `ANDON` token, by construction:

| tool | ANDON as `assert` | as `raise` |
|---|---|---|
| `tools/texpass_iter.py` — **the write-head** | **8** | **0** |
| `tools/texpass_finalize.py` | **4** | **0** |
| `tools/project_twins.py` | **15** | 1 |
| `tools/e11_manifest.py` | **35** | 1 |
| `tools/e11_export_turnaround.py` | **24** | 1 |

Control, on the pinned interpreter, three ways:

```
NORMAL           : gate fired -> ANDON: gate fired
python -O        : gate SILENT, execution continued past it
PYTHONOPTIMIZE=1 : gate SILENT, execution continued past it
```

**E08 Amendment 32** was earned when a PowerShell chain walked past a fired ANDON and
committed 47,020 texels; the repair moved the check *inside the tool*. One environment
variable removes 87 of those checks — including every ANDON in `texpass_finalize` that
E20's T26 fired to prove it *"refuses before writing the atlas."* **Strictly worse than
the original defect:** the shell chain at least let the ANDON print; under `-O` the gate
never speaks, the write proceeds, and the process exits `0`.

**Severity, honestly:** nobody sets `PYTHONOPTIMIZE` in this repo's recorded commands and
**no artifact is claimed corrupted**. A32's test is *separability*, not probability.

## Scope — RULED, and narrow

**In:** the **87 ANDON-carrying assert sites** in the five tools above, plus
`facet_index.py`'s inverse-discovery guard and `record_mcp.py`'s `assert code in CODES`.

**Out:** the **~207 non-ANDON asserts.** They are developer sanity checks; converting
them wholesale is a large diff across accepted-asset tooling for no gate. **Do not touch
them** — if one turns out to guard an irreversible step, that is a finding for the
ruling, not a scope extension.

## The bar — this is the whole difficulty

These tools produced four accepted assets and several write into the must-not-move trees
(E04's, E08's, E13's, E14's).

> **Every conversion is a PURE MOVE.** No behaviour change rides along, no message is
> improved in passing, no condition is tightened. **An anchor that does not reproduce
> byte-for-byte REVERTS the conversion — it is never adjusted until it passes.**

Anchors that must reproduce exactly: **T7's byte-identity replay**, **T26's three fired
ANDONs**, and the **twin-projection anchor**. Run them before and after; a diff in either
direction is a halt.

**A raise is not automatically equivalent to an assert.** `assert cond, msg` raises
`AssertionError(msg)`; callers that catch `AssertionError` — or tests that assert on it —
change behaviour if you raise something else. **Measure what catches these before
converting**, and prefer the conversion that keeps the exception type unless a finding
says otherwise.

## Tests ride the commit, starting at T30

The shape is fixed, and it is the test the current construction makes *impossible*:

- **each converted gate fires under a normal interpreter AND under `-O` and
  `PYTHONOPTIMIZE=1`** — the repair is exactly what makes this writable
- a **can-fail leg** per gate: prove the assertion discriminates
- the write-path gates additionally assert **nothing was written** when they fire
- **no test asserts that `PYTHONOPTIMIZE=1` disables a gate.** E21 was right to refuse
  that: it would anchor the defect

## Fold in: Q2's exit code

[E21 Ruling 4](E21-ruling.md) ruled a failing `verify` off `1` and onto **`4 = REFUSED`**
— *"the tool ran correctly and is telling you not to proceed."* A fired ANDON takes **the
same `4`** once it is a raise (Ruling 3 unblocks here). Carry E21's F3 consequences:
`verify()`'s value is also the `verify_exit_code` field of the schema-versioned
certificate `record_health` serves, and `mcp_support.FAILED_PARSE["exit_code"]` is a
fixture constant. `parse_verify` keys on `rc != 0`, not `rc == 1`, so the health state
machine survives — **verify that claim before relying on it.**

`SHIP_GATE.md`'s B2 line is the gate item this closes.

## Predictions — committed BEFORE opening any tool

Write and commit `E22-predictions.md` first. Predict at least: how many of the 87 sites
carry a message vs. a bare condition; how many are inside a function that already
catches `AssertionError`; whether any anchor fails on the first conversion; and how many
of the ~207 non-ANDON asserts turn out to guard an irreversible step (**a quantity, and
E21's calibration lesson is that this repo's density predictions run ~2× high**).

## Standards compliance (this dispatch)

**⚑ Amendment 1, 2026-08-08, added by the incoming advisor before any executor opened
this spec.** The dispatch shipped without this block and without an Environment section.
Every sibling kickoff E17–E21 carries both; this one carried neither, and the standing
rule is that missing compliance halts a session rather than being noticed later. Scored
against the spec **as amended** — what the amendment itself added is named in the row.

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the control is pinned three ways (normal / `-O` / `PYTHONOPTIMIZE=1`), the per-tool ANDON counts are given as numbers to re-derive rather than trust, and three anchors are named literally. **The amendment added the Environment block below** — the absolute interpreter, the shared-copy git discipline, run-then-rerun — which the dispatch had left implicit |
| ANDON_AUTHORITY | 3 | this experiment *is* andon authority: it exists because 87 gates are deletable by an env var. Gate 2 is the strong form — an anchor that does not reproduce **reverts the conversion**, it is never adjusted until it passes — and the arc halts at a report rather than deciding its own meaning |
| NAMED_COMPENSATORS | **1** | **the weakest row, and it is a real gap, not a formality.** See the compensator note below: this arc replays anchors through tools that write into the must-not-move trees, and **those trees are not in git**, so `git revert` is not a compensator for them. Remediation is written below and is binding on the executor; owner: advisor, this dispatch |
| DECOMPOSE_BY_SECRETS | 3 | scope is drawn by *what carries the ANDON token*, not by file or directory convenience, and the ~207 non-ANDON asserts are excluded with the reason stated — a large diff across accepted-asset tooling for no gate |
| UNCERTAINTY_GATED_HUMANS | 3 | the genuinely uncertain call is pre-routed: a non-ANDON assert that turns out to guard an irreversible step is "a finding for the ruling, not a scope extension." Predictions are committed before any tool is opened, and the calibration note ("this repo's density predictions run ~2× high") frames the ask contrastively |
| EXTERNAL_VERIFIER | 2 | the verifier is not the converting agent's own judgment but three byte-level anchors, the full artifacts tier and CI — none of which the agent can talk its way past. skip: no cross-family LLM check, because every outcome here is a byte comparison or an exit code, and a second model has nothing to add to `==` |

### ⚑ The compensator gap, stated because scoring it 1 obliges naming it

The anchors replay through tools that write into **E04's, E08's, E13's and E14's trees**,
and those trees live under `FACET_ASSETS` (`E:\AI\training`) — **they are not in git.**
For every other file in this arc the compensator is `git revert`; for those trees there
is no revert, because there is no committed prior state to return to. A single bad write
during an anchor replay is unrecoverable by any mechanism this repo currently has.

Binding on the executor, and this is a gate not a suggestion:

- **Replay anchors to a scratch output path**, never over the recorded tree. Where a tool
  has no output-path argument, that is a finding to report — not a reason to point it at
  the tree.
- **Before the first replay, record the tree's state** (per-file sha256 manifest of the
  four trees) and **re-check it at the halt**. The compensator for an unexpected write is
  a restore from that manifest's source, and the owner is the executor within the session
  that wrote it — a cross-session restore has nothing to restore from.
- Any anchor replay that modifies a must-not-move tree **halts the arc** under gate 3,
  which already forbids the edit; this row makes the *detection* mandatory rather than
  assumed.

## Environment

- Suite and any tool invocation under the **absolute** pinned interpreter
  `E:\AI-Models\trellis2-env\Scripts\python.exe`. Bare `python` lacks `open3d` **and**
  `mcp`, and **T18 refuses it loudly in one line** — if you see that message, you used
  the wrong interpreter.
- Blender work runs **through PowerShell**; Git Bash mangles the paths.
- Shared working copy: **file-specific `git add`**, pathspec-scoped commits, **never
  `git add -A`**, no stash. The DB and its certificate commit as a **pair**, at a session
  boundary only.
- Fold-marked test failures against a live-moving corpus: **run-then-rerun once**
  (E18 Ruling 2l). A second failure is real.
- **ASCII prints.** CI is paths-gated over `tools/ tests/ pytest.ini .mcp.json
  .github/workflows/ pyproject.toml package.json bin/` and runs two dependency scanners.
  **Never leave CI red.**

## Gates

1. **Suite green before and after** under the pinned interpreter, and **the full
   artifacts tier**, not just hermetic — the anchors live there.
2. **Every named anchor reproduces byte-for-byte.** A failure reverts.
3. **No edit outside the seven named files**, and none to `canon/`, `profiles/`, the
   citable trees, the seeded set or closed rulings.
4. **CI green**, including both dependency scanners.

## Out of scope

The ~207 non-ANDON asserts · U3's logging flag (ruled SKIP at E21 Ruling 6) · the three
testability seams (E20 Ruling 6) · P5 · the measurement MCP · the release.

## Halt

`E22-gates-report.md`: predictions scored, per-site conversion table, anchor evidence
before and after, findings under the assertion law, tests added, gates with evidence.
**Then stop.** A release, if any, is a separate act at the Director's word.
