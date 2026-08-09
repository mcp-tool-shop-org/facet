# E28 — the instrument census, and the three tools open question 2 released

**Written by the advisor, 2026-08-09, at the Director's rulings on both open questions.**
Halts twice: **once mid-arc at the census** (task 1), and finally at
`E28-instrument-census-report.md`. The advisor rules at `E28-ruling.md`.

**The spec is [docs/specs/measurement-mcp-spec.md](../specs/measurement-mcp-spec.md) and it
is the contract.** This dispatch does not restate it. Read the spec, then
[E27's ruling](E27-ruling.md), then this.

---

## The question

**Two, and they are sequenced rather than parallel because the Director sequenced them.**

1. Which of `tools/diagnostics/`'s instruments belong on the measurement surface —
   **measured, not curated**?
2. Do the three tools open question 2 just released wrap **without editing** the
   instruments they wrap?

## ⚖ What the Director ruled, 2026-08-09 — both open questions are CLOSED

**Open question 1 — *"Commission the census first."*** The boundary is not set by
curation and is not set blind. This arc measures every file in `tools/diagnostics/`, and
the boundary is ruled against that census afterward. **You do not decide the boundary.**

**Open question 2 — the `e12_*` / `e14_*` family is IN.** Three refusing tools are
released at once: `mesh_topology`, `thin_extent_curve`, `offsurface_rate`.

## ⚠ AND A LAW CHANGED UNDERNEATH THIS ARC — read this before task 2

The Director's second clause was *"Not sure why that closed ruling exists."* **It does
not exist**, and this was measured at the ruling seat rather than reasoned about:

- Searched across **all 25 ruling documents**: **no ruling in this repo forbids editing an
  instrument.** The only `not edited` in a ruling is
  [E10-off Ruling 1](E10-offsurface-ruling.md), whose object is the **ruling document**
  (*"E10-ruling.md is closed and is cited, not edited"*), not the tool.
- The sentence *"rather than edit a shipped instrument whose numbers are cited in a closed
  ruling"* originates in **one executor's docstring explaining its own choice**
  (`e12_offsurface.py:8`). Two documents then cited it as binding at three sites, both in
  the words *"the record already refuses this move."* **The record refuses no such thing.**
- What **is** ruled stays: corrections to a closed ruling are additive, never rewrites
  (E10-off R1); and *an instrument does not change under the session using it*
  ([E12 Ruling 6d/6e](E12-ruling.md) — which **scheduled** two repairs for after the
  handoff rather than forbidding them). Textual and temporal. Neither is a permanent
  prohibition on a tool.
- **The hazard the folklore stood in for is real and is now checkable: a cited number must
  still reproduce from the tool at HEAD.** That is a test, not a taboo.

**What this licenses, and its exact bound.** You may repair `e14_topology.py` (task 2a)
under the discipline this repo applied to 278 sites: **prove the edit non-perturbing, or
carry an anchor reproducing the cited number, in the commit that makes the edit.** It
licenses nothing wider. **Gate 3 still binds absolutely: the server WRAPS and does not
re-implement, and does not edit an instrument to make wrapping easier.** The only
instrument edit in scope is 2a's tie repair, and it is in scope because it fixes a crash,
not because it is convenient.

The full law is now in [CLAUDE.md](../../CLAUDE.md), *a closed ruling freezes its own text,
not the tool that produced its numbers.* The spec and the placement memo are corrected in
place with the measurement, not silently.

---

## Task 0 — T34's fourth leg. Small, first, and it earned its place today.

**The experiment count on the public front door was stale again when this dispatch was
written.** Measured: the status table holds **27** rows and the index's `experiments` table
agrees at **27**; `README.md` said *"twenty-six"* at two sites. Corrected in place in this
fold — to **twenty-eight**, since E28's own row lands with it.

**This is the third instance in 24 hours and the second inside a fix.**
[E27's ruling](E27-ruling.md) caught the front door reading *"twenty-three experiments"*,
corrected it to twenty-six — **and undercounted by one in the very correction**, which is
the same shape as [E26](E26-ruling.md)'s drift landing inside the commit that fixed the
previous drift. A class that re-drifts while being fixed does not need another careful
human; **it needs the mechanism this repo already has and has had vindicated twice**
([E23 Ruling 9](E23-ruling.md)): put the live-moving quantity under a test.

T34 pins **test** counts and cannot see this one. Give it a fourth leg pinning the
**experiment** count: count the status-table rows in `docs/experiments/README.md`, and
assert every prose statement of that count across the swept surfaces agrees.

- ⚠ **The leg must FAIL on a deliberately stale surface before it passes at HEAD** —
  [E26](E26-ruling.md)'s gate 2, which is E24's lesson carried. A leg that has only ever
  been seen passing is not a leg.
- **Do not widen T34's matcher** — [E26 Ruling 3](E26-ruling.md) ruled against it with a
  census: the first proximity-shaped matcher returned 45 hits of which 15 were not counts
  (`RTX 5090`, four ISO dates, `limit=999`) while *missing* a real French `hermétiques`.
  The number here is spelled in **words** on both sites, which is a different matching
  problem from digits — say plainly in the docstring which notations the leg catches and
  which it does not, the writing-convention remedy E26 ruled in place of a regex.
- **The historical-count rule still holds**: a count correct forever in a released
  `CHANGELOG` entry or a `SHIP_GATE` lineage line is not a drift and must not fire.

## Task 1 — THE CENSUS. Halts.

### The population, enumerated rather than derived

`tools/diagnostics/` holds **99 `.py` files and 0 files of any other extension**, measured
at this dispatch (`Get-ChildItem -File`, non-recursive; `__pycache__` is a subdirectory and
is not a member). **Verify this count as your first act rather than inheriting it** — two
arcs in this repo lost their scope to a number nobody re-measured, and *the spec's own
estimate for this directory was "~80."*

### ⚠ Before the first number: say what one of the counted thing IS

The dispatch ritual, and it has kept every population honest for five arcs. Write down, in
the report, before any count:

- What makes a file **an instrument** for this census? Is `__init__.py` a member? A file
  with no docstring? A file that is a library imported by other diagnostics rather than a
  runnable tool?
- **And E27's addition, which is newer and cost that arc its only clean miss:** for each
  axis below, check the property is **defined for every member**. A `bpy`-importing file
  has no defined value for "import-safe under the pinned interpreter" — that is `n/a` with
  a reason, never a silent `false`. A prediction about a real population still fails if it
  assumes a property nobody checked each member for.

### The instrument, not a hand-read

**The census is produced by a committed, re-runnable script — `tools/instrument_census.py`
— not by reading 99 files and typing a table.** A hand-read is what produced "~80". The
script is the deliverable as much as its output is, and it rides with tests (T41).

Axes A–F are **mechanical**: the script measures them and a human does not adjudicate them.

| axis | measured how | why it decides the boundary |
|---|---|---|
| **A — invocable** | `argparse` present · count of `add_argument` · `if __name__ == "__main__"` present | a tool with no flags cannot be pointed at a new subject; this is exactly what made `e10_offsurface` un-wrappable |
| **B — subject-bound** | module-level string literals matching a recorded-tree path (`E:\`, `E:/`, `facet_next`, `facet_E0`, `training`, `saltroad`, `ARMB`) or a named profile; report the literals themselves, not a boolean | the property that separates "an instrument" from "one arc's run" |
| **C — the question** | docstring line 1, verbatim, truncated to one line | the job-shape mapping in axis G reads off this |
| **D — cited** | mentions of the filename across the corpus (`record_markdown()`'s set — do **not** modify that function, [E26](E26-ruling.md) ruled it unchanged) | which files carry numbers a future seat may cite, and therefore which edits owe an anchor |
| **E — anchored** | does any file under `tests/` name this module | whether an edit to it would be *caught*; D-high + E-zero is the interesting cell |
| **F — import-safe** | `--help` exit 0 writing nothing, in three interpreter modes (normal, `-O`, `PYTHONOPTIMIZE=1`) — E25 measured 41 of its 43 | whether it can be tested hermetically at all |

**Axis G is a judgment and is labelled as one.** For each file, which of the spec's **eight**
tool questions it answers, or `none`, or `ambiguous`. **This is a proposal, not a
decision** — the boundary is the advisor's to rule and the Director's to adjust.
*"No opinion" is an acceptable and useful value*; a forced guess is worse than a blank,
because a table of confident `none`s reads as a measurement.

### Output

- `docs/instrument-census.md` — the table, one row per file, plus the axis definitions you
  wrote before counting.
- `docs/instrument-census.json` — the same data, machine-readable, so the next arc diffs
  rather than re-reads.

### Tests — T41 (T40 is taken; the namespace has no allocator)

- **The classifier's can-fail legs**: synthesise a file with a hardcoded recorded-tree path
  and assert axis B flags it; synthesise one with flags and assert axis A finds them; feed
  a `bpy` importer and assert axis F returns `n/a` rather than `false`. **A classifier that
  has never been shown failing is not a classifier** — this repo has caught two checks that
  could not fail (a silhouette IoU that returned 1.00000 on a holed mesh, a dilation
  comparison that returned 0.00% by construction).
- **The population under a test**: pin the count of `.py` files in `tools/diagnostics/`, the
  [E23 Ruling 9](E23-ruling.md) pattern. Moving it must require editing the test on purpose,
  in the commit that moves it.

### ⚠ HALT HERE

Report the census. **Do not proceed to task 2 until the advisor has ruled on it.** The halt
is real work, not ceremony: the census can find an instrument that answers one of the three
tools better than the named one, or an instrument for `anchor_check`, which nobody believes
exists — and **that is exactly how E27's own remedy turned out to be void.** If the census
moves task 2's scope, task 2 must not already have been spent.

---

## ⚖ Amendment 1 — appended 2026-08-09 at the census ruling, before task 2 was picked up

The census halted as dispatched and is **ruled** ([E28-ruling.md](E28-ruling.md), Rulings
1–9). Task 2 is green-lit with three scope adjustments; everything not named here stands
as written below.

1. **Task 2-pre, new and first: extend the census to `tools/verify/` (8 files).** F3
   measured that two of the four serving tools are implemented there, outside task 1's
   population. Parameterize `instrument_census.py`'s directory (diagnostics stays the
   default), add axis-G judgments for the 8 as a *proposal* (the missing-judgment ANDON
   must keep firing), extend T41's population pin **deliberately, in the same commit**,
   and re-emit both outputs. The boundary ruling's backing map then rests on measurement
   over both homes.
2. **`mesh_topology` wraps `e14_topology.py` alone** (Ruling 4). `e12_nonmanifold.py` is
   NOT wrapped: its output is a picture drawn onto a render set it requires as input —
   evidence for the eye, the Director's channel — and its non-manifold *count* is already
   computed independently by `e14_topology`, by both instruments' own design. The served
   payload's `notes` **names it** as the independent concentration picture, the E27
   Ruling 7 pattern. No agreement leg is commissioned: E14 ran both instruments on the
   same subjects and the record already carries their agreement.
3. **The F5 watch-list is output, not work.** The 36-file cited>0 ∧ unanchored cell (see
   the report's dated correction) is the standing watch-list; the anchor obligation rides
   any future **edit** to a member, per CLAUDE.md's closed-ruling law. No wholesale test
   commission.

## Task 2 — THE THREE WRAPS. After the ruling on task 1.

### 2a — `e14_topology.py`'s tie crash (F1), first, because `mesh_topology` needs it

Reproduced at two seats:

```
python tools/diagnostics/e14_topology.py --glb tests/fixtures/measure_min/meshes/cube.glb
  IndexError: index 3 is out of bounds for axis 0 with size 3     (line 187)
```

`thin = argmin(ext)`, `tall = argmax(ext)`, `wide = 3 - thin - tall`; on tied extents
`argmin == argmax`, so `wide == 3`. Every E14 subject had unequal extents, so it never
fired in its own arc.

**The proof obligation, and it is the whole of 2a's difficulty.**
[E27 Ruling 3](E27-ruling.md) ruled this repair provably non-perturbing: *on unequal
extents the expression is arithmetically unchanged.* Discharge that rather than cite it —
**on any mesh with three distinct extents the repaired expression selects the same three
indices as the current one**, shown by exhaustive comparison across the recorded subjects
**plus a randomized sweep over distinct-extent triples**, not by reading the diff. Derive
the repair yourself; the invariant is the specification, not any particular expression.

The test carries the crash as its can-fail leg: the unit cube must raise today and return
three distinct axes after.

### 2b — the three handlers

`mesh_topology` · `thin_extent_curve` · `offsurface_rate`, replacing the `NOT_WRAPPED`
refusals in `tools/measure_mcp.py`.

- **The server wraps. Gate 3 binds.** No measurement arithmetic in the server — that was
  E27's central property and `git diff --name-status` proved it.
- **`offsurface_rate` serves the BAKE half only.** The erode / margin-statistic half the
  spec asks for exists in **neither** offsurface instrument — measured at the E27 ruling
  seat; `--margin` in `e12_offsurface.py` is the *camera framing* margin, a different
  quantity. **Name the gap in the payload's `notes`**, the pattern E27 Ruling 7 ratified.
  Do not compute it.
- **`e12_offsurface.py` requires `--prep` and writes via `--out`** — the out path is a
  scratch path, always.
- **Update the module docstring's refusal list** (`tools/measure_mcp.py`, the block naming
  four refusals) and **T40, which pins those refusals.** T40 moving is correct and
  deliberate; it is not a test being weakened.
- The identity envelope is the contract: every payload carries server version, instrument
  sha256, params and config hash. Three new instruments means three new sha256 pins.

### Tests — T42 onward

Each wrap tested at the served surface, hermetic where possible. **Anchors where a recorded
number exists**: E27's `reach_ceiling` anchor reproduces E12's pre-registered 50.46% digit
for digit and is the model. **Report which of the three can carry an anchor and which
cannot, with the reason** — do not pad the count, and do not skip silently
([E24 Ruling 3](E24-ruling.md): five wheel legs were *skipping* in CI and read as passing).

---

## Task 3 — F4's largest connected component. Droppable.

The record's law is *report the total **and** the largest connected component* — two
thresholds separate one wrong garment from ordinary speckle. `texel_provenance` reports
per-class totals only. [E27 Ruling 7](E27-ruling.md) put this **in the instrument, not the
wrapper**: a `tools/diagnostics/texel_provenance.py` change, pure-move discipline (add an
output, change no existing number), **with the wrapper's `measure.notes` gap-text removed in
the same commit that fills it.**

**If the session is long, halt after task 2 and say so plainly.** A named carry is worth
more than a rushed third task. This is not padding to be completed for the count.

---

## Predictions — committed BEFORE the first measurement

Write `E28-predictions.md` and **commit it before `instrument_census.py` runs once**.
Point estimate **and** a band for each, and **disclose whether each was blind.**

- **P1** — of the 99, how many are invocable (axis A)?
- **P2** — how many are subject-bound (axis B)?
- **P3** — how many are cited in the corpus at all (axis D)?
- **P4** — how many have any test naming them (axis E)?
- **P5** — how many are import-safe in all three modes (axis F)?
- **P6** — how many map to one of the spec's eight questions (axis G)?
- **P7** — behavioural, not a quantity: will 2a's repair be byte-identical on every
  recorded subject? State what would falsify it.

### ⚠ The calibration warning, and it is the sharpest thing in this dispatch

**Five consecutive arcs have missed a prediction on a unit or a population rather than on
the work** — E23 P4b (reasoned about *files*, the instrument measured a *scope*: 4 predicted,
20 measured) · E24 P1 · E25 P3 (a *reachability* unit: 46 predicted, 17 measured) ·
E26 P8 (predicted what it would *write*; the instrument counts parametrized cases: 8 → 34) ·
E27 P1 (the population was real and every member was real, but the prediction assumed a
property none was checked for: 6 → 4).

**Every one of those was a real population measured in the wrong unit, or a real population
with an unchecked property.** Before each number: name the unit, name the denominator, and
check the property is defined for every member. And do **not** apply a calibration haircut —
E22's P18 halved an untutored estimate *on this repo's own "densities run 2× high" lesson*
and measured 175 against a predicted 4. The ritual moved the answer away from the truth and
made the move look like discipline.

---

## Gates

1. **The census's population count is verified, not inherited.** If it is not 99, that is a
   finding and the dispatch was wrong — report it, do not quietly use your number.
2. **The classifier's can-fail legs pass before any census number is believed.** A number
   from an unfalsified classifier is not a measurement.
3. **Task 2 does not start before the task-1 halt is ruled.** Stop at every gate; never
   improvise past one.
4. **Gate 3 (E27's): the server wraps, does not re-implement, and does not edit an
   instrument** — except 2a, which is named, bounded, and carries its proof.
   `git diff --name-status -- tools/` at the close must show **exactly**
   `M tools/measure_mcp.py`, `M tools/diagnostics/e14_topology.py`,
   `A tools/instrument_census.py`, and — only if task 3 runs —
   `M tools/diagnostics/texel_provenance.py`. Anything else is a finding.
5. **CI green**, both scanners, and the run id **resolved before it is written down**
   ([E23](E23-ruling.md)'s fabricated-citation law: a gate that has not run is written
   `NOT YET RUN`, never a plausible identifier with a verdict beside it).
6. **No recorded tree is modified.** sha256-manifest before and after if any tool is pointed
   at one; E23's instrument covers 7,312 files in ~50 s and has held five times.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the census is a committed script under the absolute pinned interpreter, re-runnable and diffable rather than a hand-read; the three wraps extend an identity envelope that already pins server version + instrument sha256 + params + config hash per payload |
| ANDON_AUTHORITY | 3 | the task-1 halt is a hard stop with the advisor between the halves; gates 1–6 above; every ANDON written here `raise`s (the class closed at E25 — 278 sites), and a bare `assert` is either labelled `IMPLEMENTATION:` or is not written |
| NAMED_COMPENSATORS | 3 | table below; nothing here publishes, tags, creates a repo, or writes a registry — the heaviest action is a tracked file edit |
| DECOMPOSE_BY_SECRETS | 3 | axes A/B are precisely the subject-assumption-versus-physics boundary [profiles-design.md](../profiles-design.md) already specifies; the census measures that split across 99 files rather than asserting it |
| UNCERTAINTY_GATED_HUMANS | 3 | the halt gates on uncertainty rather than step count — it exists because the census can move task 2's scope; axis G returns a *proposal* with "no opinion" allowed, and the boundary ruling is reserved to the advisor and the Director |
| EXTERNAL_VERIFIER | 2 | the census's classifier would otherwise grade its own output. **Remediation, owner = this executor:** hand-verify ≥10 rows against the files themselves, including **every** row the classifier marks ambiguous, and report the disagreements. **Second leg, owner = the advisor at the ruling:** re-measure an independent sample, as E27's ruling seat did on nine lines of `argparse` |

### Compensators

| action | irreversible? | compensator | post-rollback state | owner |
|---|---|---|---|---|
| `tools/instrument_census.py` + its two outputs | no | `git revert`; the outputs are derived and regenerate | unchanged | this executor |
| 2a — the `e14_topology.py` repair | no | `git revert`; the proof obligation means a revert restores byte-identical behaviour on every recorded subject | unchanged | this executor |
| 2b — `measure_mcp.py` handlers + T40 | no | `git revert`; the server is not in the wheel ([E27 Ruling 8](E27-ruling.md)) so nothing published moves | refusals restored | this executor |
| task 3 — `texel_provenance.py` | no | `git revert`; pure-move means no existing number changes | unchanged | this executor |
| running any instrument against a recorded tree | **reads only, and must stay that way** | `--out` to scratch **always**; sha256-manifest before/after; a changed file halts the arc | trees byte-identical | this executor |
| the index DB + certificate | — | **not yours.** The advisor rebuilds and commits the pair at the ruling | — | the advisor |

## Out of scope

- **Deciding the boundary.** Task 1 halts; axis G is a proposal.
- **The erode / margin-statistic half of `offsurface_rate`** — commissioned in principle at
  E27, unscoped, and not this arc's.
- **`anchor_check`'s instrument** — a genuine commission either way; if the census finds a
  candidate, that is a *finding*, not a build.
- **Renaming `e13_anchor_check.py`** ([E27 Ruling 4](E27-ruling.md)).
- **`superseded/`'s one remaining `assert`** — pinned by name in T33, ruled never converted.
- **Publishing `facet-measure`** — [E27 Ruling 8](E27-ruling.md): out of the wheel by
  default, not by deferral.
- **`record_markdown()`** — ruled unchanged by [E26](E26-ruling.md).
- **The DB + certificate**, the polish arc, any recorded tree, any closed ruling.

## Environment

```
python    E:\AI-Models\trellis2-env\Scripts\python.exe      <- ABSOLUTE, always
blender   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"   -b -P only
```

- **Bare `python` lacks `open3d` and `mcp`.** T18 refuses the wrong interpreter loudly in
  one line — if you see it, you used the wrong one.
- **Blender work runs through PowerShell.** Git Bash mangles the paths and every call fails
  with `Error: Please select a file`. Blender's own MCP server is a **reference for when you
  are stuck, never a pipeline stage**, and never pointed at `E:\AI\training`.
- **The VRAM watchdog was dead at the previous seat's close and was restarted 2026-08-09
  at this one**, verified by watching the heartbeat file advance rather than by trusting the
  starter's exit code. Nothing in this arc needs the GPU; if that changes, check it first.
- **Scripts create their own output directories.** Two runs have died on this.
- **`argparse` eats leading minus signs** — use `--views=-30,0,30`.
- **ASCII prints.**
- CI is paths-gated over `tools/ tests/ pytest.ini .mcp.json .github/workflows/
  pyproject.toml package.json bin/` — a docs-only commit correctly triggers no run.

### If a second seat is live in this working copy

It has happened twice and both saves were **observational, not mechanical**
([E27 Ruling 9](E27-ruling.md)) — assume nothing is watching for you.

- **File-specific `git add`, always.** Never `git add -A`.
- `git fetch && git merge --ff-only origin/main`, **not** `pull --rebase`.
- ⚠ **That guard watches the REMOTE and cannot see a sibling's local commit**
  ([E26 Ruling 2](E26-ruling.md)). **Re-measure any quantity you assert against the tree you
  are about to commit** — including the census's own population count.
- `cancel-in-progress: true` means a parallel push cancels your CI run; gate 5 is satisfied
  by the first *completed* run whose tree contains your commit, and the report names what
  else was in it.

## Halt

Report at `E28-instrument-census-report.md`. **Two halts**: the census halt mid-arc, and the
close.

- **State a prediction before you look, and disclose whether it was blind.**
- **Never judge whether output is good.** Produce measurements. The words *verified,
  shipped, works, decisive, validated, proven* do not belong in the report, a commit
  message, or a doc.
- **A negative result is a full success.** If the census says the spec's eight are the wrong
  eight, say so plainly. If a wrap cannot be done without editing an instrument, **refuse
  and report** — E27's executor declined to repair an excluded-family tool it had every
  incentive to fix, and that refusal was the right call and is on the record as such.
- **Stop at every gate. Never improvise past one.** A session that changed a parameter and
  re-ran when a gate fired hit the same gate harder.
- **Do not write to the memory store.** The advisor folds findings into the repo. The repo
  is the record.
