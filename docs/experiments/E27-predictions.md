# E27 predictions — committed before any tool is written

**Executor, 2026-08-09.** Frozen in the session scratchpad at draft time and moved into
`docs/experiments/` + committed immediately after the baseline suite run completed,
because pytest.ini's `fold` marker forbids corpus writes while the suite is in flight.
The draft was not edited after the baseline output was read; the rows below marked
*blind* were written before that output (or the named source) was seen.

## The blindness boundary — what was looked at before these predictions

- **Read:** the E27 dispatch, `docs/specs/measurement-mcp-spec.md`,
  `docs/specs/placement-memo.md`, CLAUDE.md, `tests/conftest.py`, `pytest.ini`,
  `pyproject.toml` (first 40 lines), `tools/e11_manifest.py` (first 60 lines, while
  locating the manifest instrument — it is the export contract, not the manifest),
  E23 report lines ~445–484 (the manifest instrument's scope and invocation).
- **Listed, filenames only, no source read:** `tools/`, `tools/verify/`,
  `tools/diagnostics/`, `tools/superseded/`, `tests/`, `tests/fixtures/`.
- **Not read at draft time:** the source of any instrument the server would wrap
  (`mesh_stats.py`, `gate_mesh.py`, `e08_ceiling.py`, `e10_offsurface.py`,
  `texel_provenance.py`, `e13_anchor_check.py`, `gate0_sheet.py`, `gate1_sheet.py`, or
  any other `tools/` body), `record_mcp.py` (the pattern to follow), the contents of
  `tests/fixtures/selftest_min/`, and every test body except `conftest.py`.
- **In flight with output unread at draft time:** the baseline suite run.

Per the dispatch's warning (four consecutive arcs missed on a unit, not a population),
**each numbered row states what ONE of the counted thing is before the number.**

---

## P1 — hermetic testability of the eight

**Unit:** one *hermetically testable tool* = one of the spec's eight whose **primary
measurement path** (input in → number out, asserted against a known expected value) runs
in a test with **no FACET_ASSETS** — synthetic fixtures in git only, CI conditions. A
tool whose *refusal leg alone* runs hermetically does **not** count.

**Prediction: 6 of 8, band 5–7.** Expected hermetic: `mesh_stats`, `mesh_topology`,
`reach_ceiling`, `thin_extent_curve`, `offsurface_rate` (a synthetic position map over a
flat quad is constructible), `measure_report` (pure composition). Expected not hermetic:
`anchor_check` — its job is recorded outputs by definition, so its measurement path is
artifacts-tier (its comparison arithmetic may still be exercised hermetically, which does
not count under this unit). The uncertain seventh is `texel_provenance` — hermetic only
if its input state can be synthesized small; if not, 5.

*Blindness: source-blind. Informed by the spec's tool table and the filename listings.*

## P2 — behaviour `tools/` does not currently expose

**Unit:** one *tool needing behaviour `tools/` does not expose* = one of the eight where
at least one spec-named capability of that tool has **no computing module under `tools/`
today outside the excluded `e12_*`/`e14_*` family**. The report will split the two
sub-cases: (a) the only implementation is `e12_*`/`e14_*`-prefixed — the Director's open
question 2 surfaces as a finding; (b) no implementation exists anywhere — a pure finding.

**Prediction: 4 of 8, band 3–5.** Named guesses, from filenames only:
`mesh_topology` (dual-definition shell census + hollow/double-wall detection — the
visible family is `e14_topology.py` and `e12_nonmanifold.py`, both excluded; nothing
else in the listing looks like it), `thin_extent_curve` (`e12_thin_curve.py` is
excluded; `e13_thin_inputs.py` reads as inputs-side), `measure_report`
(`gate0_sheet.py`/`gate1_sheet.py` exist but are likely wired to specific subjects),
`anchor_check` (`e13_anchor_check.py` exists and is in scope, but likely wired to E13's
specific pair). Expected covered: `mesh_stats` (`verify/mesh_stats.py`),
`reach_ceiling` (`e08_ceiling.py`), `offsurface_rate` (`e10_offsurface.py`),
`texel_provenance` (`diagnostics/texel_provenance.py`, unprefixed and in scope).

*Blindness: source-blind, filename-informed.*

## P3 — shared helpers

**Unit:** one *shared helper* = one function or module the built server calls from the
handlers of two or more of the eight tools.

**Prediction: YES — at least 2 distinct shared helpers**, most likely 3:
(1) a load-and-weld mesh canonicalization returning welded and unwelded views (the spec
requires both numbers, and every geometry tool wants it); (2) the payload envelope
builder — server version + measurement-config hash + `diagnostic`/`gate-eligible`
labels, wanted by all eight; (3) camera/view-set construction shared by `reach_ceiling`
and `thin_extent_curve`.

*Blindness: derived from the spec text alone; no server code exists yet.*

## P4 — tests the arc adds

**Unit:** one *test* = one pytest-collected node (test function or parametrized case),
measured as the **collection-count delta** between my measured baseline on main and the
halt commit, same rig, FACET_ASSETS present. Not files, not assert statements.

**Prediction: 42 added, band 30–55.**

*Blindness: blind to `record_mcp`'s test density (T19–T23 bodies unread); informed by
the fact that five T-files cover the six-tool record server.*

## P5 — mesh_stats vs mesh_topology on the shell census

**Operands:** on the pinch fixture (two cubes sharing exactly one vertex, welded),
compare `mesh_stats`'s reported component count(s) against `mesh_topology`'s shell
census under both named definitions.

**Prediction: the two tools agree definition-for-definition** — every component number
`mesh_stats` reports equals `mesh_topology`'s census number under the same named
definition, exactly, on every fixture including the pinch fixture. Direction call:
`mesh_stats`'s primary component count is the **edge-adjacency** definition (so it reads
2 on the pinch fixture, where the vertex-definition census reads 1). The failure this
predicts against: either tool reporting a number matching *neither* named definition.

*Blindness: blind — `mesh_stats.py` source unread at draft time.*

## P6 — my own baseline (gate 1)

**Unit:** pytest's collected count on a clean main at `43a86dd`, this rig, full
artifacts tier (FACET_ASSETS present), pinned interpreter.

**Prediction: 648 collected exactly (dispatch's number; nothing has landed since the
dispatch commit per `git log`), 0 failed, 0 error.** I do not predict the pass/skip
split because I have not measured which artifacts-tier tests skip on this rig.

*Blindness: blind — the run was launched before this draft but its output is unread at
draft time.*

## P7 — the excluded-family collision (own add)

**Unit:** one *collision* = one of the eight whose only existing implementation under
`tools/` is `e12_*`/`e14_*`-prefixed, forcing the Director's open question 2 to surface
in the report as a finding rather than being decided by this session.

**Prediction: YES, 2 collisions, band 1–3** — `mesh_topology` and `thin_extent_curve`.

*Blindness: source-blind, filename-informed.*
