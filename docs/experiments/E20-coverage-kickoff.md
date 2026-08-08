# E20 — unit coverage: the tool surface gets tests below the replay level

**Written by the advisor, 2026-08-08, at the Director's word ("32 tests is
weak").** He is right, and this kickoff is the fix rather than the defense: E17
ported the checks that existed — dense end-to-end anchors, and almost nothing
below them. **Most of `tools/` has zero unit coverage.** This session builds it,
prioritized by what is load-bearing, hermetic by construction, under the
tests-ride-the-commit law.

**No numeric test-count target is set, deliberately** — a count is the metric
this repo's own laws warn about (a number that can be satisfied without
measuring the thing). The target is **coverage of the load-bearing surface**:
every tool named below carries its own suite when this session halts, and the
report tables per-tool what is covered and what remains, with reasons.

## You are the executor

```
cd E:\AI\facet && git pull
python tools/facet_index.py build            <- the E15 ritual (seeded set 19)
CLAUDE.md                                    <- read first — the tests law binds
                                                every commit; the instrument laws
                                                bind every assertion
docs/experiments/E17-ruling.md               <- the harness you extend; Ruling 5c
                                                names the control-can-fail law
tests/                                       <- the existing 32; extend, never
                                                duplicate; conftest's patterns
                                                (run_py, the pre-check, need())
                                                are the house style
```

⚠ **SHARED COPY — sequencing is load-bearing**: this session fires **after E18
halts** (both lanes write `tests/` and `conftest.py`; the D2 synthetic-state
fixture E18 delivers is U3's substrate). E19 may run in parallel — its lane is
the presentation surface, no overlap. Standing rules: file-specific adds only;
never commit the DB; trellis2-env python; scratch paths for any DB comparison.

**Blind predictions first, committed** — per module: expected pass state AND
**where a latent defect is most likely** (unit tests on never-unit-tested code
find bugs; predicting where is the calibration).

## The law for what a unit test may assert

A unit test **pins current behavior only where current behavior is anchored or
accepted** (a recorded artifact, a ruled value, a mathematical property). Where
a probe reveals behavior that looks WRONG, the probe's evidence goes to the
report as a FINDING — **no test lands asserting either way until the ruling**,
which then either fixes the tool (change + test in one commit, under the law)
or blesses the behavior (the test pins it). Tests are never tuned to broken
behavior, and broken behavior is never frozen by a well-meaning pin. The
executor decides neither.

## The units, priority order

**U1 — `facet_index`'s parsers** (pure text functions, fixture strings): the
ruling/sub-ruling/closure/handoff heading parsers including the measured marker
convention and its one closure exception; the arc-label derivation (the
E10-offsurface collision law); the status-position law (capitals carry verdicts;
lower-case "accepted" is an adjective); the claims families (range/cardinal/
starts-at-1/AMBIGUOUS — extending T5's fixtures, not duplicating them); the
supersession regexes. These parse a legal record; their edge cases ARE the law.

**U2 — `project_twins`' pure core + `mask_geometry`**: `fit_background`'s
per-pixel sampling on synthetic gradients with known truth (the vignette case —
E16-8's y+270 finding as a fixture); `figure_mask` keying on synthetic images
where the true figure is constructed; `local_thickness` on synthetic shapes of
known width; **the A3 invariant property-tested** — erosion never exceeds a
third of a structure's own half-width, asserted over generated thin/wide/mixed
shapes (E16-10's per-structure table as the oracle shape).

**U3 — the `texpass_iter` write-head, on the D2 synthetic state**: the commit
ANDON's property (styled texels byte-identical across any commit — the A32
invariant as a unit property, violated-by-construction in the can-fail leg);
holes strictly shrink; job-mask derivation from a known hole map; `--edge-mode`
global vs local on synthetic thin structures (the 0-admission-at-thinnest
signature); the emit guard's message contract.

**U4 — `texpass_finalize`'s lookup**: surface-aware nearest-painted-in-3D on a
small synthetic mesh with hand-computable answers; both distance ANDONs FIRED on
constructed violations (the can-fail proofs); the flood path's earned zero vs
surface-aware's structural zero, distinguished in a unit fixture.

**U5 — `mesh_stats` + the frame-derivation math**: fit-axis/margin/aspect on
synthetic meshes built to the four subject classes' geometry (portrait
tip-standing, landscape, near-cube); the T12 warning's boundary (rect_frac at
0.99/1.0/1.01); the welded-vs-unwelded shell census on constructed seams.

**U6 — the guards-can-fail audit, closing Ruling 5c's class**: enumerate every
`assert`/ANDON/refusal in `tools/` (grep, the list in the report); each either
HAS a can-fail test (existing or added here) or is listed with the reason it
cannot be cheaply fired. A guard nobody has seen fire is the class three seats
paid for this week; this item retires it wholesale.

**Fixtures**: synthetic, deterministic, committed (a `tests/fixtures/` builder
in the D2 pattern — generated content is code, so its builder carries its own
test). Everything hermetic; the artifacts tier grows ONLY if a unit genuinely
needs a recorded input, with the reason stated. CI runtime budget: the hermetic
set stays under ~3 minutes; anything slower carries `slow` and the report says
what it costs.

## Explicitly NOT this session

No tool behavior changes except testability seams under the law (tests + anchor,
same commit, proposed in the report if non-trivial). No coverage theater — a
test that asserts a call ran without asserting an outcome is excluded by its own
name in the report. No E18-lane edits (the server's tests are its own), no
E19-lane edits, no profile/canon/fixture/seeded-set edits, no memory-store
writes, no DB commits. Do not end a session the Director has not ended.

## Then HALT

Report at `docs/experiments/E20-coverage-report.md`: the per-tool coverage table
(covered / remaining / reason), the guards audit list, predictions scored,
findings with evidence (per the assertion law above), the full suite output at
the end state, CI green at the advisor's push. The advisor rules at
`E20-ruling.md`.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | fixtures are committed and deterministic; the assertion law pins tests to anchored/accepted behavior only; predictions committed blind per module |
| ANDON_AUTHORITY | 3 | U6 exists to make every guard demonstrably fireable; a suspicious probe HALTS into a finding rather than landing as a pin either way |
| NAMED_COMPENSATORS | 3 | additive files, revertible per commit; any testability seam carries the anchor discipline; no publish, no spend |
| DECOMPOSE_BY_SECRETS | 3 | units follow the tools' own boundaries; fixtures separate from tests; the report separates covered from remaining so the next session inherits a worklist, not a vibe |
| UNCERTAINTY_GATED_HUMANS | 3 | the assertion law routes every wrong-looking behavior to the ruling instead of an executor's judgment call — the fix-or-bless fork is the Director's chain, not the session's |
| EXTERNAL_VERIFIER | 2 | the oracles are synthetic constructions with known answers plus the record's measured tables, not the tools' own outputs; CI re-runs everything clean-room. Scored 2: no different-family verifier reviews the assertions themselves — the advisor's ruling is that check |

## Calibration

The risk on a coverage push is volume-lust: many shallow tests that assert
nothing, hit the count, and freeze bugs in place. The assertion law and U6 are
the guards. A found defect reported with evidence is worth more than fifty
passing pins — a negative result is a full success.
