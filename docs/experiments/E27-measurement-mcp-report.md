# E27 — the measurement MCP: executor report

**Executor session, 2026-08-09.** Dispatch:
[E27-measurement-mcp-kickoff.md](E27-measurement-mcp-kickoff.md). Contract:
[docs/specs/measurement-mcp-spec.md](../specs/measurement-mcp-spec.md). This report is the
halt; the advisor rules at `E27-ruling.md`. No tag was cut and no release act performed.

**What was built.** `tools/measure_mcp.py` — a stdio MCP server named `facet-measure`,
version `0.1.0`, serving **the spec's eight tool names exactly**. Four wrap in-scope
instruments as subprocesses under the pinned interpreter; four **refuse with a structured
error naming the finding** that blocks them. Every successful payload carries the identity
envelope (server version, instrument path + file sha256, resolved params, config hash);
`measure_report` refuses to compare payloads whose identity differs, naming the field.
Nothing was moved, nothing re-implemented, no instrument edited.

---

## A live sibling seat shared the working copy — sequenced, not raced

Mid-arc, the 0.3.1 release seat was **live in this same working copy**: its staging grew
between two of my `git status` reads (translations regenerated 02:14, DB rebuilt 02:16,
index staged 02:27 — 58 s before my check). I froze all git activity, watched, and its two
commits landed cleanly (`be8d790` release prep, `9940226` DB/cert pair). My commit lands
**after** both, so no sibling bytes ride in it. E26 Ruling 2's re-measure rule was applied
in the direction it names: every quantity this arc's surfaces assert was re-measured
against the tree as committed. **One residue to flag**: at this halt the v0.3.1 **tag has
not yet been observed** — if the release seat builds its artifacts from the shared tree
*after* this arc's surface updates, the tarball README would carry 684 where the tag
carries 648. The release seat's own publish checklist re-verifies; this line exists so it
re-verifies knowingly.

## Predictions, scored — blindness disclosed per row

Committed at `919ed9c` before any tool was written; the blindness boundary is stated in
that file and held (no instrument source, no `record_mcp.py`, no suite output before the
freeze).

**P1 — hermetic testability: MISS.** Predicted 6 of 8 (band 5–7); **measured 4** —
`mesh_stats`, `reach_ceiling`, `texel_provenance`, `measure_report` all run their primary
measurement path on in-git synthetic fixtures with no FACET_ASSETS. The miss's mechanism:
two of my six (`mesh_topology`, `thin_extent_curve`) turned out to have **no in-scope
instrument at all** — they refuse, so under my own unit ("primary measurement path runs")
they cannot count — and `offsurface_rate` likewise. I predicted `anchor_check` not-hermetic
(right) and `texel_provenance` uncertain (it is hermetic — the one-job synthetic state
works). The prediction failed on scope, not on fixtures: **I predicted testability of tools
whose blocker is that they cannot exist yet.**

**P2 — behaviour `tools/` does not expose: HIT, with the unit ambiguity disclosed.**
Predicted 4 (band 3–5), naming `mesh_topology`, `thin_extent_curve`, `measure_report`,
`anchor_check`. Measured: **3 under the unit's strict reading, 4 under its operational
reading — the unit did not decide the boundary case, which is this repo's five-arc
failure shape appearing again at a smaller scale.** The boundary case is
`offsurface_rate`: `e10_offsurface.py` *is* "a computing module under tools/ outside the
excluded family" (strict: does not count → 3) but it binds its subject as module constants
and cannot be invoked on arbitrary input (operational: counts → 4). Both readings land in
band. Wrong named guess: `measure_report` — `gate1_sheet.py` is parameterized and wraps
cleanly. Missed name: `offsurface_rate`, which I had predicted covered.

**P3 — shared helpers: HIT on the count, mostly wrong on the names.** Predicted ≥2, likely
3 (load-and-weld, envelope builder, camera construction). Measured: **five** helpers shared
by ≥2 of the four live tools — `envelope()` (all 4), `run_instrument()` (all 4),
`_need_file()` (all 4), `warning_lines()` (3), `_sanitize_nan()` (2). Only the envelope
materialized as named. The geometry-side helpers I predicted (weld, cameras) do not exist
in the server **because the server wraps instead of computing** — welding lives inside the
instruments. The bar produced the miss, which is the bar working.

**P4 — tests added: HIT.** Predicted 42 (band 30–55). **Measured 36** collected
(648 → 684): 35 hermetic + 1 artifacts-tier anchor.

**P5 — the shell census: headline HIT, direction call FALSIFIED.** On the pinch fixture
(two boxes sharing exactly one vertex), measured with both instruments run directly:
`mesh_stats` `components` = **1**; `e14_topology` `SHELLS (shared-vertex)` = **1** —
agreement definition-for-definition, exact — and `pieces (manifold-adjacency)` = **2**,
the disagreement the fixture was built to expose. My direction call was wrong twice over:
I predicted `mesh_stats` was the edge-adjacency definition reading 2. It is the **vertex**
definition (its own docstring says so; unread at prediction time, disclosed blind).

**P6 — the baseline: HIT exactly.** Predicted 648 collected, 0 failed, 0 error, blind to
the in-flight run. Measured: **648 passed in 385.16 s, exit 0**, full artifacts tier,
zero failures, zero skips. Split confirmed by collection: 648 total / 640 hermetic /
8 artifacts — the dispatch's numbers reproduce. Stated plainly: the baseline ran on the
tree **as found** — `43a86dd` plus the sibling seat's then-uncommitted 0.3.1 prep.

**P7 — the excluded-family collision: HIT exactly.** Predicted 2 (band 1–3), naming
`mesh_topology` and `thin_extent_curve`. Measured: exactly those two, no third.

Score: 5 hits (one exact-blind, P6), 1 miss (P1), 1 hit-with-disclosed-unit-ambiguity
(P2). **The dispatch's four-arc warning about units was half-heeded: writing the unit
before the number kept every population honest, and the one ambiguity that survived was in
a unit's boundary clause, not its population.**

## The eight tools — what each wraps (gate 3)

| tool | wraps | state |
|---|---|---|
| `mesh_stats` | `tools/verify/mesh_stats.py` | **live** |
| `mesh_topology` | none in scope — `tools/diagnostics/e14_topology.py` is the implementation and is `e14_*` (open question 2); it also crashes on tied extents (finding F1) | **refuses** |
| `reach_ceiling` | `tools/diagnostics/e08_ceiling.py` | **live** |
| `thin_extent_curve` | none in scope — `tools/diagnostics/e12_thin_curve.py` is the implementation and is `e12_*` (open question 2); `e13_thin_inputs.py` answers a different question | **refuses** |
| `offsurface_rate` | none invocable — `tools/diagnostics/e10_offsurface.py` computes it with its subject hardcoded (E04_shipprep paths, `profiles/ship.json`, one job's cam.json); the erode/margin form is `e12_offsurface.py`, excluded | **refuses** |
| `texel_provenance` | `tools/diagnostics/texel_provenance.py` | **live** |
| `anchor_check` | none exists — `tools/diagnostics/e13_anchor_check.py` is a **name collision** (the spiral-law adjacency guard); the anchored-regression pattern lives in the harness's artifacts tier and session procedure | **refuses** |
| `measure_report` | `tools/verify/gate1_sheet.py` (sheet half); the comparison half is the server's own envelope contract, not a measurement | **live** |

**No instrument was re-implemented and no instrument was edited.** The server contains no
measurement arithmetic: its own code is subprocess argv, transcript parsing against pinned
print sites, precondition checks, and the identity envelope.

## The hermetic / artifacts split, measured

- **36 tests added: 35 hermetic, 1 artifacts.** All four live tools' measurement paths run
  hermetically on `tests/fixtures/measure_min/` (21 files, 49,486 bytes, generator
  committed beside the bytes — the E18 D2 pattern; the fixture ADDS a twin, replaces
  nothing).
- **The artifacts tier holds the wrap anchor**: the served `reach_ceiling`, pointed at the
  recorded `facet_next/E12_prep` with the recorded invocation's floors (0.45/0.45),
  reproduces E12's pre-registered stage-1 ceiling **digit for digit** — valid 3,240,510 ·
  head band 1,358,656 · N8 reachable 1,635,304 · 50.46% (E12-task2-report.md §2.2, found
  via `record_query` against the sibling seat's fresh 0.3.1 index). Skips with the named
  path when FACET_ASSETS is absent.
- The four refusing tools have no measurement path to split; their refusal legs are
  hermetic and tested.
- Suite totals: **648 → 684 collected; 640 → 675 hermetic; artifacts 8 → 9.**

## Refusal evidence per tool (gate 2)

Every refusal is a structured error — `code`, `message`, `hint`, `exit_code` (the ruled
registry: 4 = REFUSED, 1 = user error, 2 = runtime) — raised as an MCP error result, with
a can-fail test leg per class:

- `mesh_stats`: absent mesh → `PRECONDITION_MISSING` naming the path (T36).
- `reach_ceiling`: missing prep member → names the exact file (`pos.npy` leg, T37);
  cropless meta → names the missing keys before the instrument can KeyError (T37).
- `texel_provenance`: missing job member → names it (T38); **the sealed-tree gate** — the
  `--render` path writes `claim.npy` into `--state`, so `state` under FACET_ASSETS
  refuses with `SEALED_TREE` naming what would be written (T38). Measured while building:
  the census path is **write-free** (the instrument exits before its `claim.npy` write
  when `--render` is absent), so read-only census of recorded states stays legal.
- `measure_report`: no args / one-sided compare / envelope-less payloads →
  `BAD_ARGUMENT`; **identity mismatch → `MEASUREMENT_MISMATCH` naming the differing
  field** (T39 proves `config_hash` is named on a cube-vs-pinch compare).
- The four unwrapped tools: `NOT_WRAPPED`, exit_code 4, each naming a real file **whose
  existence the test asserts** (T40) — if a later session wraps one or moves an
  instrument, the pin fails and the refusal text is updated consciously.

## The instrument laws, carried in payloads

- **Denominators**: every ratio names numerator and denominator in a `ratios` block, and
  the operands ride in the same payload (`reachable` + `valid_texels`; census counts +
  `valid_texels`; `figure_px` under every dE statistic). T35 asserts no ratio ships
  unnamed.
- **Warnings travel**: instrument WARNING/NOTE lines are surfaced verbatim in
  `measure.warnings` — mesh_stats' not-a-face-readout fired on the sliver fixture and is
  asserted present (T36); e08_ceiling's E14 Ruling 10b bias-vs-wall caveat is asserted
  present (T37).
- **NaN is not a number**: `mesh_stats` returns `curv_var = NaN` on a rect-empty mesh;
  the envelope converts to `null` and names the conversion in `nan_as_null` (T36).
- **Diagnostic vs gate-eligible**: every payload carries `metrics_label: "diagnostic"`
  with the rationale; promotion to gate-eligible is a ruling, and no field exists for a
  verdict.
- **Hue/chroma and circular statistics**: no tool on this surface returns a hue, so the
  laws bind structurally rather than behaviourally this arc.

## Findings

**F1 — `e14_topology.py` crashes on any mesh with tied extents.** Line 184:
`wide = 3 - thin - tall` with `thin = argmin(ext)`, `tall = argmax(ext)`; on equal extents
argmin == argmax and `lo[3]` throws IndexError. Reproduced on the unit cube and the pinch
fixture; every E14 dragon had unequal extents, so it never fired in its own arc. The P5
census printed **before** the crash site, so the measurement stands. Not repaired — the
file is excluded-family and its numbers sit in closed rulings; the refusal text carries
the fact so ruling the family in is done knowingly.

**F2 — `offsurface_rate` has no invocable instrument.** `e10_offsurface.py` computes
exactly the spec's quantity with its subject bound as module constants; parameterising it
is an edit to a tool whose numbers sit in closed rulings — the advisor rules whether that
happens or a fresh instrument is commissioned. The spec's erode/margin form exists only as
`e12_offsurface.py` (excluded).

**F3 — `anchor_check` has no instrument, and the one file named like it is a different
tool.** `e13_anchor_check.py` is the spiral-law painted-adjacency guard. The
anchored-regression pattern the spec wants exists as harness tests (T07–T11) and session
procedure, not as a tool.

**F4 — the census/largest-component gap.** `texel_provenance` reports per-class totals
only; the record's own law wants the total AND the largest connected component for
blob-shaped defect classes (DILATION especially). Computing it in the wrapper would be new
measurement arithmetic — the payload names the gap instead (`measure.notes`, asserted by
T38), and the commission is the ruling seat's.

**F5 — open question 2 is forced, exactly twice.** `mesh_topology` and
`thin_extent_curve` have complete, subject-independent, parameterized implementations that
this arc may not wrap. Both refusals name the question as the Director's. (With F1: ruling
the family in is necessary but not sufficient for `mesh_topology`.)

**F6 — packaging.** `measure_mcp.py` is deliberately NOT in the wheel (`py-modules` is
untouched — it lists `facet_index` and `record_mcp` only, and pyproject was mid-release
under the sibling seat). The measurement server versions itself independently
(`facet-measure 0.1.0`); whether and how it joins a release is the Director's, out of this
arc's scope by the dispatch.

**F7 — the shared-copy interleaving** (top of this report): a live release seat's staging
grew under this session; sequencing rather than racing cost ~20 minutes and zero bytes of
cross-contamination. The tag-timing residue is flagged for the release seat.

## Tests added (T35–T40; T-numbers taken when looked: T01–T13 as files, T14/T15/T15b as
in-file legs, T16, T18–T34 as files; T17 unreferenced — left as a gap, took T35+)

| file | tests | tier |
|---|---|---|
| `test_t35_measure_mcp_surface.py` | 5 | hermetic — the eight-name surface, annotations, envelope, config-hash determinism and parameter-sensitivity, ratio naming |
| `test_t36_measure_mesh_stats.py` | 6 | hermetic — cube 6-island weld demonstration, pinch vertex-census 1, twoshell 2, sheet NaN→null, warning surfacing, refusal |
| `test_t37_measure_reach_ceiling.py` | 6 | 5 hermetic (exact 0→1024 ladder, denominators, bias warning, two refusals) + **1 artifacts (the E12 recorded anchor)** |
| `test_t38_measure_texel_provenance.py` | 5 | hermetic — census sums exactly, write-free census path, sealed-tree refusal, missing-member refusal, largest-CC gap named |
| `test_t39_measure_report.py` | 5 | hermetic — analytic dE identities (576 px, median==mean==p90), denominator naming, same-config compare, mismatch refusal, bad arguments |
| `test_t40_measure_not_wrapped.py` | 9 | hermetic — the four refusals pinned to real files, open-question-2 naming, the F1 crash note, the F2 both-halves note, the F3 collision note, one stdio wire test |

The fixture generator is `tests/fixtures/make_measure_fixture.py`; the committed bytes are
the fixture (byte-equality across library versions not claimed — the selftest_min rule).
Two of my own defects were caught by these tests on their first run: a tuple-shaped
`_sanitize_nan` corrupting every payload value, and a refusal naming
`tools/e13_anchor_check.py` where the file lives under `diagnostics/` — the live-pin
design caught my own wrong pointer immediately.

## Gates

1. **Suite green before and after, full artifacts tier.** BEFORE: measured my own —
   **648 collected / 648 passed / 0 failed, 385.16 s** (tree as found: `43a86dd` + the
   sibling's uncommitted 0.3.1 prep; artifacts tier ran, nothing skipped). AFTER:
   **684 collected / 684 passed / 0 failed, 403.69 s, exit 0** — on the
   surfaces-updated tree, artifacts tier included, nothing skipped.
2. **Refusals**: evidence above; every class has a can-fail leg that runs in CI.
3. **No re-implementation**: the wrap table above; four findings where behaviour is
   missing, zero second implementations.
4. **The four index legs** — BEFORE (session start, scratch build):
   `VERIFY PASSED - all four legs`, 19/19 seeded, byte-identity. AFTER (scratch build on
   the corpus as this report was being finalized): **`VERIFY PASSED - all four legs`,
   byte-identity, 628 rulings / 2,374 prose sections**. `record_markdown()` and every
   line of `facet_index.py` and `record_mcp.py` untouched by this arc (`git diff` empty
   on both). The fold-marked tests re-ran after this report entered the corpus; their
   result is stated in the commit message rather than here, because a claim about a run
   that includes this file cannot precede the file.
5. **CI green, both scanners**: **NOT YET RUN at this report's commit** — the run id and
   verdict are appended in a follow-up commit after the push, per the
   fabricated-citation law: a gate that has not run is written NOT YET RUN, never a
   plausible identifier with a verdict beside it.
6. **No recorded tree modified.** Manifest BEFORE anything ran: **7,312 files,
   17,072,807,610 bytes, 50.0 s** — E22's count and E23's exact byte total reproduce.
   RECHECK at halt, after the artifacts-tier suite run:
   `RECHECK before=7312 after=7312  added 0 removed 0 changed 0 — MANIFEST HELD`.

## What the polish arc gets

Mounted as `facet-measure`, the polish arc can measure each exemplar before and after a
pass with `mesh_stats` / `reach_ceiling` / `texel_provenance`, compose the before/after
comparison with `measure_report` — which will refuse if the two measurements were not
taken by the same instrument configuration, which is the property the arc depends on. The
two refusing geometry tools (`mesh_topology`, `thin_extent_curve`) unblock on open
question 2 the moment the Director rules; wrapping them after a ruling is a small change
inside an already-tested surface (drop-in handler + tests), plus F1's repair for
`mesh_topology` on symmetric meshes.

**Halt.** The advisor rules at `E27-ruling.md`.
