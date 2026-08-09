# E27 — the measurement MCP

**Written by the advisor, 2026-08-09, at the close of the gates arc.** Halts at
`E27-measurement-mcp-report.md`; the advisor rules at `E27-ruling.md`.

**The spec is [docs/specs/measurement-mcp-spec.md](../specs/measurement-mcp-spec.md) and it
is the contract.** This dispatch does not restate it. It adds facet's overlays, the bar,
and what has changed under the spec since it was written.

---

## The question

Spec 2's eight job-shaped tools become a running server, **in facet**
([placement-memo.md](../specs/placement-memo.md), ruled in the Director's own words).
Does the measurement surface hold as one instrument — the same numbers for the same mesh,
from any caller?

## Why this arc, and why now

**It is the last thing standing between here and the polish arc.** [E14 Ruling 35](E14-ruling.md)
is the Director's word: *"We're going to polish all of the exemplars from each profile
after the MCP tools have been built and verified properly with tests."* Four tools were
ruled; **one is built** (the record index, E18, now shipped as `facet-mcp` on PyPI and
`@mcptoolshop/facet` on npm). This is the second, and it is the one the polish arc
actually consumes.

**Its first consumer is the best one it could have**: four accepted exemplars across four
subject classes, each measured **before and after** a polish pass by the same instrument.
Instrument identity stops being a README claim and becomes what the arc depends on.

## What has changed under the spec since it was written — verify, do not inherit

- **The build bar is the studio's, not a prototype's** (E14 Ruling 35). Shipcheck-grade,
  with tests. `record_mcp.py` is the worked example of what that looks like here.
- **Open question 3 is CLOSED** and the spec says so: `ai-eyes-mcp` is seven image-grading
  tools, this server measures geometry and texels, **disjoint by measurement**. The one
  adjacency is `measure_report`'s sheet — if a sheet is ever *graded*, call `image_compare`,
  do not reimplement it.
- **Open questions 1 and 2 are the Director's** — which instruments enter the surface
  first, and whether arc-specific `e12_*`/`e14_*` diagnostics are in scope (the spec
  recommends **no**). **Do not decide them.** If the build forces the question, report it.
- **Every ANDON in `tools/` now raises** (E22, E23, E25 — 278 of them). Any gate you write
  in this server `raise`s; a bare `assert` is a developer sanity check labelled
  `IMPLEMENTATION:` or it is not written.
- **Exit codes are ruled**: `0` ok · `1` user error · `2` runtime error · `4` REFUSED for
  a fired gate or a refusal. `3` is reserved and unused. If this server ships a console
  script, it carries that registry.
- **The wheel path is fixed** (E24): the root resolves by **testing for the record**, and
  refuses with `4` when no candidate holds. If this server resolves any path, it uses
  `facet_index`'s resolver rather than inventing a second one.

## The bar

**This is a build, not a conversion — the pure-move bar does not apply.** What applies is
the bar `record_mcp` set and passed:

1. **Job-shaped tools.** A tool answers a question someone has, not "run script X". The
   spec's eight names are the contract; their *signatures* are yours to derive.
2. **The server wraps; it does not re-implement.** The instruments live in `tools/`. If a
   tool needs behaviour that is not there, **that is a finding**, not a licence to write a
   second implementation of a measurement the record already cites.
3. **A refusal is better than a wrong number.** The index MCP refuses to answer from an
   unverified index because a wrong citation is worse than none. **A measurement server
   inherits that squarely**: an instrument that cannot establish its precondition refuses
   with `4` and names what is missing.
4. **Tests ride the commit.** Every tool you add carries tests in the same commit. The
   studio rule, and this repo's own since E17.

## ⚠ The instrument laws the spec carries are not decoration

The spec's *"instrument laws"* section is the reason this server exists rather than a
directory of scripts. Read it as binding. The ones that have cost this repo the most:

- **A denominator is named or the number is not quoted.** Four moving-denominator
  incidents are in the record.
- **A hue carries its chroma; a statistic of angles is circular.**
- **Bbox-check a keyed mask against the geometry before reading a number from it.**
- **A global constant must not govern a local feature** — derive per structure or bound it
  as a fraction of that structure's own width.
- **Report the total AND the largest connected component.**

If a tool cannot honour one of these on some input, **it refuses on that input**. It does
not return a number with a caveat in prose nobody reads.

## Tests ride the commit — and the fixture question is the arc's real work

`record_mcp` had a corpus to serve. **This server needs meshes**, and the recorded trees
are **not in git** and are the thing three rulings had executors sha256-manifest 7,312
files to protect.

- **Synthetic fixtures first.** E18's D2 built a hermetic fixture for the write-head
  (`tests/fixtures/selftest_min`, one flat quad) precisely so a test could run in CI. That
  is the pattern. A cube, a sheet, a two-shell blob and a deliberately non-manifold mesh
  will exercise most of the surface.
- **The artifacts tier is for anchors.** Where a tool must reproduce a recorded number,
  that is an `artifacts`-marked test reading `FACET_ASSETS`, skipping with a printed reason
  when absent — never a silent skip.
- **Measure which tools can be tested hermetically and report the split.** E23's 16-of-38
  and E25's 17-of-130 are the precedent: a short honest list beats a padded one, and
  E20's refusal to invent units that could not exist was that arc's largest deliverable.
- **Take T35+.** T-numbers are a shared namespace with no allocator; take the next free
  number and say which were taken when you looked.

## Predictions — committed BEFORE any tool is written

`E27-predictions.md` first, blindness disclosed per row. Predict at least: how many of the
eight tools can be tested **hermetically** (a count with a band); how many need behaviour
`tools/` does not currently expose; whether any two of the eight want the same helper;
how many tests the arc adds; and whether `mesh_stats` and `mesh_topology` agree on the
shell census on a mesh where the two definitions differ.

**Four consecutive arcs have missed on a UNIT, not a population** (E23 P4b, E24 P1, E25 P3,
E26 P8). Before each number, write down what one of the thing you are counting *is*.

## Gates

1. **Suite green before and after**, full artifacts tier. **Measure your own baseline and
   state it** — it was 648 at dispatch and two arcs have moved it in a day.
2. **Every tool refuses rather than guessing** when its precondition fails, exits `4`, and
   names what is missing. A can-fail leg per refusal.
3. **No instrument is re-implemented.** For each of the eight, name the `tools/` module it
   wraps — or report that none exists.
4. **The four index legs still pass** and `record_markdown()` is untouched: this server
   shares a repo with the record index and must not disturb it.
5. **CI green**, both dependency scanners. If a gate fires on the *environment* rather than
   the result, [E23 Ruling 2](E23-ruling.md) governs what you may repair.
6. **No recorded tree is modified.** Manifest before, re-check at the halt. E23's
   instrument covered 7,312 files in 76 s and has held four times.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the spec is the contract and is named rather than restated; the six things that changed under it since it was written are enumerated with their rulings; the fixture pattern is pinned to E18's D2 by path |
| ANDON_AUTHORITY | 3 | six gates; gate 2 makes refusal the tested behaviour rather than an aspiration; gate 3 makes re-implementation a halt |
| NAMED_COMPENSATORS | **2** | this arc adds a server and tests and touches no recorded tree, so `git revert` is a real undo. Not 3: it *reads* the recorded trees for its anchors, and those remain outside git with a restore-from-source that has still never been rehearsed |
| DECOMPOSE_BY_SECRETS | 3 | the server wraps, the instruments stay in `tools/`, the conventions stay in `facet_index` — the same split `record_mcp` proved, and gate 3 enforces it |
| UNCERTAINTY_GATED_HUMANS | 3 | the spec's open questions 1 and 2 are explicitly the Director's and the dispatch forbids deciding them; the hermetic/artifacts split is reported rather than assumed |
| EXTERNAL_VERIFIER | 2 | anchors against recorded numbers, the four index legs, CI. skip: no cross-family LLM — every outcome is a number compared to a recorded number |

## Out of scope

`comfy-preflight` (ruled **standalone**, a new org repo under the repo-first rule) ·
`fixture-lint` (ruled **sdlab-side**) · the polish arc itself · the release · P5 · the
`SystemExit` collision · anything under `tools/diagnostics/e12_*` or `e14_*` unless the
Director rules them in.

## Environment

- Everything under the **absolute** pinned interpreter
  `E:\AI-Models\trellis2-env\Scripts\python.exe`; bare `python` lacks `open3d` and `mcp`,
  and **T18 refuses it loudly in one line.**
- Blender work runs **through PowerShell**. **Blender's own MCP server is a reference for
  when you are stuck, never a pipeline stage** — see CLAUDE.md's Environment section for
  why, and do not point it at `E:\AI\training`.
- Shared working copy: file-specific `git add`, **never `git add -A`**, no stash. Before
  pushing, `git fetch origin && git merge --ff-only origin/main` — and note
  [E26 Ruling 2](E26-ruling.md): that guard watches the **remote** and cannot see a sibling
  session's local commit, so **re-measure any quantity a surface asserts against the tree
  you are about to commit.**
- **ASCII prints.** CI is paths-gated. **Never leave CI red.**

## Halt

`E27-measurement-mcp-report.md`: predictions scored with blindness disclosed, the eight
tools with the module each wraps, the hermetic/artifacts split with reasons, refusal
evidence per tool, the index legs before and after, the manifest result, findings, tests
added, and gates with evidence. **Then stop.** The advisor rules at `E27-ruling.md`; a
release is a separate act at the Director's word.
