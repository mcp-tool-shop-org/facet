# tree_manifest — the verify-path receipt guard (errand spec)

**Seat:** advisor (spec) → one executor errand · **Written:** 2026-08-15, from the E36
open halt ([E36-open-manifest-halt.md](../experiments/E36-open-manifest-halt.md)) ·
**Runs:** at the Director's word, and **never concurrently with another seat's
test-adding commit** — the errand moves the suite count, so its commit owns the full
T34 surface set, and two seats moving count surfaces at once cannot both be green
(the T34 two-seat lesson).

## The defect, measured at the halt

- The emit path self-guards: [`tree_manifest.py:118`](../../tools/verify/tree_manifest.py)
  excludes its own output file from the walk by construction.
- The verify path does not: lines 226–227 write `--out-json` **after** the walk, to any
  destination — including inside a root this same invocation just verified.
- The instance: the E35 close's manifest-D receipt, written into `facet_E35` eleven
  seconds after the seal it reports HELD — 335 declared / 336 present, the gate FIRED
  at E36's open, the Director ruled the receipt deleted. The instance is repaired; the
  class remains.
- T70's five legs cannot see it: none constructs a receipt written into the verified
  root. Asked in CLAUDE.md's required form — *what would this look like if the code
  were wrong in the specific way this check exists to catch* — this exact
  contamination passes T70 today.

## The change — eliminate the risk, do not gate it

One comparison, **before any walk**: resolve the `--out-json` destination; if it lies
inside any root declared by any manifest in this invocation, **REFUSE** — a
`raise SystemExit` in the tool's own ANDON form (never a bare `assert`; E22), with a
message naming both the destination and the offending root, a non-zero exit distinct
in text from the gate's `MANIFEST GATE: FIRED` path, nothing walked and nothing
written. This makes the contamination impossible rather than detectable — the E06
law, *prefer eliminating a risk to gating it*. The emit path is untouched; it is
already guarded.

## Tests, in the same commit — T70 extended

- **The can-fail leg the halt named:** synthetic tree + manifest; invoke verify with
  `--out-json` **inside** that tree → the tool refuses, exit non-zero, the
  destination file is not created, no walk output is produced.
- **The counterpart:** the same invocation with `--out-json` outside the tree → HELD,
  the receipt written, rows correct.
- **Mode discipline:** the refusal fires under `-O` and `PYTHONOPTIMIZE=1` as well as
  under a normal interpreter (the E22 four-mode form, at minimum both optimize modes).

The suite count moves, so the commit follows the corrected count order in full:
**land pin edits → run the FULL suite to surface unknown pins → collect → surfaces →
census last.**

## The cited-instrument discipline

`tree_manifest.py` is a cited instrument — its numbers sit in the E35 close and the
E36 open halt, and T70 pins its behaviour. The record's rule for editing one: prove
the edit non-perturbing, or carry an anchor that reproduces the cited numbers, **in
the commit that makes the edit**. Both, here:

- every existing T70 leg passes **unmodified** — the walk logic is untouched; the
  change is argument validation ahead of it;
- the four real gates re-run at the closed trees return **HELD with the recorded
  counts** — `facet_E33` 116/116 · `facet_E34` 84/84 · the eight subtrees 7,312 ·
  `facet_E35` 335/335 — receipts written outside every protected tree.

## Predictions, stated before the run

1. All existing T70 legs pass without edits.
2. The four real gates reproduce their recorded counts exactly.
3. The refusal adds no measurable walk time — it precedes the walk.

## Out of scope

The emit path · any manifest re-emission · any protected-tree write · any other
`tools/verify` member · the `json.dump` call's own hygiene (encoding, handle) unless
the guard edit touches that line anyway, in which case the executor reports what it
did rather than deciding silently.

## Compensators

No irreversible action exists in this errand: the change adds a refusal ahead of a
read-only walk; the repo commit reverts by commit, pathspec-scoped. The no-skip rule
is satisfied by there being nothing to compensate — stated, not skipped.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | one commit, tool + tests together; invocation forms in this spec |
| ANDON_AUTHORITY | 3 | the change IS a refusing gate; raises, never assert; textually distinct from FIRED |
| NAMED_COMPENSATORS | 2 | nothing irreversible exists; stated above rather than skipped |
| DECOMPOSE_BY_SECRETS | 2 | verify-path guard only; emit untouched; one file plus its tests |
| UNCERTAINTY_GATED_HUMANS | 2 | fires at the Director's word; scheduling gated on the two-seat count-surface collision |
| EXTERNAL_VERIFIER | 2 | the recorded gate counts are the anchor the edit must reproduce; T70's fixture is the can-fail proof |

## Executor paste block

```
You are an executor session in E:\AI\facet. One errand, one commit.
Read first: docs/specs/tree-manifest-guard-spec.md (this spec, in full) and
docs/experiments/E36-open-manifest-halt.md §4 and §8 (the defect and the ruling).
The work: the verify-path receipt guard exactly as the spec states — the refusal
before any walk, the T70 legs, the cited-instrument anchors (all four real gates
re-run, receipts OUTSIDE every protected tree), the corrected count order for the
suite-count move. Python is E:\AI-Models\trellis2-env\Scripts\python.exe, always.
Halt conditions: any existing T70 leg needs an edit to pass → HALT and report (the
walk was perturbed); any real gate returns other than its recorded count → HALT;
another seat has uncommitted or unpushed test changes in the tree → HALT and report
before touching count surfaces. No judgement words. Report to
docs/specs/tree-manifest-guard-spec.md as an appended report section.
```
