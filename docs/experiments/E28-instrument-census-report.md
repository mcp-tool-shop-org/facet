# E28 — the instrument census. Report at the mid-arc halt.

**Executor, 2026-08-09.** Dispatch:
[E28-instrument-census-kickoff.md](E28-instrument-census-kickoff.md). Predictions:
[E28-predictions.md](E28-predictions.md), committed at `46745af` **before**
`tools/instrument_census.py` existed. Contract:
[measurement-mcp-spec.md](../specs/measurement-mcp-spec.md).

**⛔ THIS IS THE MID-ARC HALT. Task 2 has not started.** The halt is the dispatch's and it
earned itself: the census moves task 2's scope in three places, named in *What this moves*
below. **Task 0 is done** (`c3c7232`). **Task 1 is done and halts here.** **Tasks 2 and 3
are untouched.**

---

## Gates

| gate | state | evidence |
|---|---|---|
| 1 — population verified, not inherited | **HELD** | **99 `.py`, 0 other, 0 subdirectories**, three ways: `Get-ChildItem -File`, `Get-ChildItem -Force`, `git ls-files`. The dispatch's `__pycache__` parenthetical describes a state not present |
| 2 — classifier falsified before its numbers are believed | **HELD** | T41's can-fail legs ran and passed **before** the first census number was read |
| 3 — task 2 does not start before the halt is ruled | **HELD** | not started |
| 4 — `git diff --name-status -- tools/` | **HELD** | `A tools/instrument_census.py`, and nothing else |
| 5 — CI green, run id resolved before written down | **NOT YET RUN** | this commit has not reached CI. Per [E23](E23-ruling.md)'s fabricated-citation law, no identifier is written here |
| 6 — no recorded tree modified | **HELD** | 7,312 files / 17,072,807,610 bytes, measured **four times** — baseline before the census, after it, after the repair, and at the close: **0 added / 0 removed / 0 changed** every time. Byte-identical to E23's and E25's figures |

⚑ **A SEVENTH GATE FIRED AND IS REPORTED AS FIRED, NOT SMOOTHED.**
`test_t41_axis_d_is_idempotent_across_runs` failed on the closing suite run — **1 failed,
734 passed** — because writing this report changed axis D. It was right to fire, it caught
the largest of this arc's four self-references, and **F10 records what it caught, the four
alternatives, and why the adopted one is not a retune.** The axis-D headline is unchanged at
**76**; without the gate it would have been **99 by construction**.

**Suite: 736 passed, 377.86 s, exit 0**, after the repair above. **Task 0's suite run:**
699 passed, 379.80 s, exit 0. T34's self-reference moved the stated suite count four times
across this arc (684 → 699 → 732 → 735 → 736), and every pinned surface moved with it in
the commit that moved the count — which is the property that pin exists to have.

---

## The population, and what one of the counted thing is

Written before counting, in [E28-predictions.md](E28-predictions.md), and repeated in the
instrument's own docstring. **Every one of the 99 `.py` files directly in
`tools/diagnostics/` is a member** — including files with no docstring and files that are
libraries rather than runnable tools. A curated membership is what this arc exists to
replace, so "library rather than tool" is a *result* (axis A false), never an entry
condition.

The census is a committed, re-runnable script — `tools/instrument_census.py` — with its
population under a test (T41, the [E23 Ruling 9](E23-ruling.md) pattern). Outputs:
[`docs/instrument-census.md`](../instrument-census.md) and
[`docs/instrument-census.json`](../instrument-census.json).

---

## What was measured

| axis | measure | count | of |
|---|---|---:|---:|
| **A** | **invocable** — argparse **and** ≥1 `add_argument` **and** a `__main__` guard | **5** | 99 |
| A | — imports `argparse` | 93 | 99 |
| A | — has ≥1 `add_argument` | 93 | 99 |
| A | — **has a `__main__` guard** | **6** | 99 |
| A | — **flag surface** (argparse + `add_argument`, guard not required) | **93** | 99 |
| A | — calls `parse_args()` at module level | 88 | 99 |
| A | — **flag surface but UNGUARDED** | **88** | 99 |
| **B1** | **subject-bound** — module-level literal carrying a recorded-tree marker | **11** | 99 |
| B2 | subject marker in any non-docstring literal | 11 | 99 |
| **C** | has a docstring | 99 | 99 |
| — | files that do not parse | 0 | 99 |
| **D** | **cited** in ≥1 corpus file | **76** | 99 |
| **E** | **anchored** — basename *or* module name as literal text under `tests/` | **46** | 99 |
| E | — basename-with-`.py` only (the stricter read) | 44 | 99 |
| **F** | **import-safe** in all three interpreter modes | **5** | 99 |
| F | — not clean in some mode | **0** | 99 |
| F | — **`n/a`**, property undefined (reason per row) | **94** | 99 |
| **G** | *proposed* to answer one of the spec's eight | *21* | 99 |
| G | *proposed* `none` | *58* | 99 |
| G | *proposed* `ambiguous` | *17* | 99 |
| G | *`no opinion`* | *3* | 99 |

Axis F's 94 `n/a` decompose exactly: **6** with no flag surface, **88** with a flag surface
and no `__main__` guard. No file scored `false`.

---

## Predictions against measurement

| # | predicted | band | measured | |
|---|---:|---|---:|---|
| **P1** invocable | 60 | 45–75 | **5** | **MISS** |
| **P2** subject-bound B1 | 30 | 15–50 | **11** | **MISS** |
| P2b B2 − B1 | 10 | 0–25 | **0** | HIT |
| **P3** cited | 65 | 45–85 | **76** | HIT |
| **P4** anchored | 12 | 3–30 | **46** | **MISS** |
| **P5** import-safe true | 50 | 30–70 | **5** | **MISS** |
| P5b `n/a` | 41 | 25–55 | **94** | **MISS** (declared dependent on P1) |
| P5c false | ~8 | 0–25 | **0** | HIT |
| **P6** mapped to one of the eight | 20 | 8–40 | **21** | HIT |
| P6b ambiguous + no opinion ≥ 10 | ≥10 | — | **20** | HIT |
| **P7** 2a byte-identical | YES | — | — | **NOT RUN** (task 2 is behind the halt) |

### P1 is the sixth consecutive unit miss, and its mechanism is exactly the named one

I predicted **60** and measured **5**. The component I was actually reasoning about —
*"this repo's culture pushes toward re-runnable parameterized instruments"* — is the **flag
surface**, and that measured **93**, which is *above* my band in the other direction.

The three-clause definition was pre-registered before any measurement, so it stands and is
not retuned. But the reasoning attached to it was about flags while the instrument counts
flags **and** a `__main__` guard, and the guard turns out to be near-absent: **6 of 99**.
That is [E23 P4b](E23-ruling.md)'s shape one level over — *reasoned about one property,
measured a conjunction that includes another* — and it is the sixth consecutive arc to miss
on a unit rather than on the work. **The directory's house style is a straight-line
module-level script**, and no amount of thinking about "how disciplined is this repo" would
have produced 5, because the number is not about discipline at all.

**P5 followed P1 by construction and I said so in advance**: the predictions file states
*"`n/a (no CLI)` is not an independent estimate; it is P1's complement"*. One miss, counted
twice, disclosed before the fact.

### P4 missed in the opposite direction, and the mechanism is the one I flagged

I predicted **12**, band 3–30, and wrote that this was *"the row most likely to be wrong,
and the mechanism would be the unit"* — reasoning that this repo prefers globbing to
hand-written lists, so tests would exercise modules without naming them. Measured **46**.
`test_t33_diagnostics_gates.py` **names 42 modules explicitly**. The prediction identified
the right axis of uncertainty and then guessed the wrong side of it.

### P2's secondary prediction landed for a reason worth recording

B2 − B1 = **0**: every subject literal in the directory sits at module level, none inside a
function. That is the same fact as P1's miss seen from another angle — a straight-line
script has no function bodies for a literal to hide in.

---

## Findings

**F1 — THE DIRECTORY'S HOUSE STYLE IS AN UNGUARDED MODULE-LEVEL SCRIPT.** 93 of 99 carry a
flag surface; **88 of those have no `__main__` guard** and 88 call `parse_args()` at module
level. Consequences, in order of how much they matter to the boundary:

- **They cannot be imported without executing.** A server that imported them would run 88
  arc scripts against whatever subjects their constants name.
- **They can still be WRAPPED.** `tools/measure_mcp.py:277–288` invokes instruments as
  **subprocesses under the pinned interpreter**, never by import. So the missing guard does
  not block the spec's surface; it blocks a different thing than the one at issue.
- **Their import-safety is therefore unmeasured, by a deliberate refusal.** Axis F declines
  to probe them because `python <file> --help` runs the module body before argparse sees
  anything. 88 files are `n/a` for a stated safety reason, not scored `false`.

**F2 — ONLY 5 FILES ARE INVOCABLE, AND ALL 5 ARE FROM ONE ARC.** `e10_claim_replay.py`,
`e10_consumers_subject.py`, `e10_offsurface.py`, `e10_offsurface_consumers.py`,
`e10_offsurface_where.py`. The sixth guard-holder, `canny_probe.py`, has a guard and no
argparse. **The invocable class is E10's house style, not the directory's.**

**F3 — ⚠ HALF THE ALREADY-SERVED SURFACE IS OUTSIDE THIS CENSUS'S POPULATION.** Read off
`tools/measure_mcp.py`'s own registry:

| served tool | its instrument | in the census? |
|---|---|---|
| `mesh_stats` | `tools/verify/mesh_stats.py` | **NO** |
| `measure_report` | `tools/verify/gate1_sheet.py` | **NO** |
| `reach_ceiling` | `tools/diagnostics/e08_ceiling.py` | yes |
| `texel_provenance` | `tools/diagnostics/texel_provenance.py` | yes |

The census measured the population the dispatch and the spec's open question 1 both name,
and it measured all of it. **But the boundary question spans at least two directories**, and
axis G's `mesh_stats: —` row is not evidence that no `mesh_stats` instrument exists; it is
evidence that it lives in `tools/verify/` (8 files, uncensused). **A boundary ruled against
these 99 alone would exclude two of the four tools that already work.** This is the census's
own denominator being narrower than the question it serves — reported rather than fixed,
because widening the population is the advisor's call and not an executor's.

**F4 — 23 FILES ARE CITED BY NOTHING IN THE CORPUS.** `build_masks.py`, `canny_probe.py`,
`e04_invar_probe.py`, `e04_ship_cameras.py`, `e04_ship_measure.py`, `e07_score_arm.py`,
`e08_contradiction.py`, `e12_ab_sheet.py`, `e12_canny_derive.py`, `e12_family_mass.py`,
`e12_n_sheet.py`, `e12_pair_sheet.py`, `e12_region_colour.py`, `e12_twin_gate.py`,
`e13_gate1_sheet.py`, `e13_payoff_sheet.py`, `e14_garnet_reproject.py`, `e14_pair_sheet.py`,
`foreshorten_table.py`, `hair_agree.py`, `hair_edge.py`, `head_yaw.py`, `prep_front.py`.

**F5 — THE INTERESTING CELL (D-high, E-zero): 14 files carry numbers a future seat may cite
and no test names them.**

The two that look sharpest are **not** in the cell, and the reason is the axis-E correction
below. `e12_offsurface.py` (cited **16** — the most-cited file in the directory) and
`texel_provenance.py` (cited 12) are both named by tests *without* the `.py`, so both are
anchored under the definition actually registered, and only the strict basename read makes
them look exposed. **That is the correction earning its keep: uncorrected, this finding
would have named the two most load-bearing instruments in the directory as unwatched, and
been wrong about both.**

> ⚠ **Corrected at the ruling seat, 2026-08-09 ([E28-ruling](E28-ruling.md) Ruling 6), with
> the committed instrument output.** Two counts in the paragraph above are interim reads
> from a corpus state that still contained this arc's uncommitted prose: the committed JSON
> has `e12_offsurface.py` cited **14** (raw 17) — a **tie** with `e08_ceiling.py` at 14, not
> the sole most-cited — and `texel_provenance.py` cited **11** (raw 13). And the cell of 14
> below carries an unstated threshold: it is the **cited ≥ 3** slice of the full
> cited>0 ∧ unanchored cell, which holds **36 files** in the committed JSON. The 14 names
> and their per-file counts match the committed output exactly under that threshold; the
> threshold is now stated. *Name the denominator — this repo's oldest defect, found here in
> a report about measuring it.*

The 14 that are genuinely unanchored: `e04_bands.py` (9), `e04_profile_check.py` (8),
`e07_l2_bound.py` (5), `e12_stem_delta.py` (5), `commit_funnel.py`, `e04_backdrop.py`,
`e04_frame_agree.py`, `e04_seam_sources.py`, `e08_bg_separation.py`, `e10_claim_replay.py`,
`e12_make_twin_prompts.py`, `e12_pair_cloud_step.py` (4 each),
`e10_offsurface_consumers.py`, `e12_help_format_scan.py` (3 each). **These are the files
where an edit would change a cited number with nothing to catch it** — which is exactly the
hazard [the closed-ruling law](../../CLAUDE.md) replaced the folklore with.

**F6 — TWO OF THE SPEC'S EIGHT ATTRACT NOTHING HERE, for two different reasons.**
`mesh_stats` attracts nothing because it lives outside the population (F3).
**`anchor_check` attracts nothing because nothing here answers it** — consistent with
[E27 Ruling 4](E27-ruling.md). The dispatch says a candidate would be *a finding, not a
build*: the nearest five are all in the `ambiguous` cell and **none is the anchored-
regression pattern** — `e04_frame_agree.py` ("REPLACEMENT INSTRUMENT — geometry against
geometry, bound 0 px"), `e10_claim_replay.py` and `e04_replay_owner.py` (both re-run shipped
commits on a scratch state), `e12_agree_probe.py` (characterise a fired anchor),
`silhouette_agree.py` (is X the same object as Y). **Reported. Not built.**

**F7 — `mesh_topology` MAY NEED TWO INSTRUMENTS, NOT ONE.** The spec asks it for
non-manifold edges *and where they concentrate*, boundary edges, a dual-definition shell
census, *and* hollow/double-wall detection. Axis G proposes **two** files:
`e14_topology.py` (the dispatch's named one — shells, the facts `mesh_stats` does not print)
and **`e12_nonmanifold.py`** (*"where a reconstruction goes non-manifold, counted AND put on
the picture"*). `e14_atlas_anatomy.py` sits in the ambiguous cell addressing the hollow
double-walled half. **Neither named instrument plainly answers the whole question**, and
task 2's plan wraps only the first.

**F8 — MY OWN AXIS-E IMPLEMENTATION DID NOT MATCH MY OWN PRE-REGISTERED DEFINITION.**
[E28-predictions.md](E28-predictions.md) defines axis E as *"basename **or dotted module
name** as literal text"*. The first implementation matched only `foo.py`, and missed two
files named without the extension — `e12_offsurface` (T40) and `texel_provenance` (T35, T38
and a fixture). Corrected to the registered definition: **46**, with the strict
basename-only read reported beside it at **44**. **The correction makes P4's miss larger**,
which is the only reason it is safe to make one at this point in an arc.

One ambiguity rides with it and is not resolved here: `texel_provenance` is *both* a module
name and one of the spec's eight tool names, so a test naming the tool is indistinguishable
from a test naming the module by this method. Both readings are in the JSON.

**F10 — ⚑ A GATE FIRED ON THE CLOSING SUITE RUN, AND IT CAUGHT THE BIGGEST SELF-REFERENCE
OF THE FOUR.** `test_t41_axis_d_is_idempotent_across_runs` **FAILED**, 734 passed, on the
run taken after this report was written. **51 rows had drifted.** The cause is this
document: a report *about* the census names the files the census found — the uncited ones,
the unanchored ones, the ambiguous ones — and `docs/experiments/` is inside
`record_markdown()`'s set. So committing the report makes **every one of the 99 "cited"**:

| axis D, cited-at-all | |
|---|---:|
| committed census, before this report existed | **76** |
| the same corpus with this report in it | **99** |
| excluding this arc's own documents | **76** |

**The alternatives, named and rejected in writing**, because the boundary in
[CLAUDE.md](../../CLAUDE.md) requires that rather than a quiet repair:

1. **Re-run the census with the report in the corpus** and commit 99/99. **Rejected** — the
   number would be manufactured by the arc's own commentary. That is not a measurement of
   the record's interest in these instruments; it is a measurement of how many filenames I
   typed into a report.
2. **Delete or loosen the idempotency test.** **Rejected** — narrowing a test to make a red
   gate green is forbidden whichever kind of gate fired.
3. **Write a report that names no files.** **Rejected** — the findings *are* the filenames.
4. **Exclude this arc's own documents from axis D.** **Adopted.**

Adopted because it is the rule *already written into this instrument before the gate fired*
— *a derived artifact of this measurement is not evidence about this measurement's subject*
— applied to a member of its class the first pass missed. It passes the test for retuning:
**the headline does not move.** 76 with the exclusion and 76 before the report existed, and
the contaminated 99 is still computed and reported as `cited_raw` beside it rather than
discarded. A later arc that re-censuses adds its own prefix to `SELF_DOC_PREFIXES`, on
purpose, in the commit that writes its report.

The gate is **reported as a fired gate**, not smoothed into a green row: it fired, it was
right, and it is the only reason the axis-D headline is not 100% by construction.

**F9 — THE FIX'S OWN TEST PERTURBED THE MEASUREMENT, AND THAT IS NOW UNDER A TEST.** The
first draft of F8's can-fail leg wrote a real module's basename into its fixture — and T41
is a file under `tests/`, so axis E counted it. The basename-only reading moved **44 → 45
by the test existing.** Rewritten with synthetic names (`zz_alpha_probe`), and pinned:
`test_t41_this_file_does_not_perturb_axis_e` asserts no member is anchored *only* by T41.
Same family as the axis-D self-citation, found the same way, and the third self-reference
this arc had to handle — **an instrument that lives inside its own population needs
checking against itself, every time.**

---

## The hand-verification (EXTERNAL_VERIFIER remediation, owner = this executor)

The classifier would otherwise grade its own output. An **independent method** — plain-text
regex rather than the AST the census uses — re-derived axes A and B across all 99 files.

**2 disagreements out of 396 cells, both resolved in the census's favour:**

| file | cell | text says | AST says | who is right |
|---|---|---|---|---|
| `e08_acceptance.py` | B2 marker | yes | no | **AST** — the marker is in a `#` comment (L56) and a *function* docstring (L130) |
| `silhouette_agree.py` | B2 marker | yes | no | **AST** — a `#` comment (L34) |

A comment is not a string literal, and documentation is not binding — the rule registered in
advance and kept runnable by
`test_t41_axis_b_ignores_a_subject_named_only_in_a_docstring`. **The defect is in the
verifier, not the census.**

**Every one of the 17 `ambiguous` rows was hand-read** against its fuller docstring, as the
dispatch requires. All 17 hold. The clearest confirmations: `e10_offsurface_consumers.py`
asks *"per consumer, does excluding the off-surface 2.5% move your headline number?"* — a
sensitivity question, **not** the offsurface rate; `e13_thin_inputs.py` says of itself
*"Assembles; proposes nothing"* — inputs, not the curve.

**FOUR self-references were checked and three moved a number.** The census lives inside its
own population — its output is a corpus file, its test is a file under `tests/`, and its
*report* is a corpus file too — so it has to be checked against itself on every axis that
reads either set. **This is the arc's dominant finding about its own method**, and three of
the four were caught by instruments rather than by reading:

- **Axis D — real, and it would have destroyed the number.** `docs/instrument-census.md`
  tabulates all 99 filenames and lives under `docs/`, so it is inside `record_markdown()`'s
  set. Left in, axis D reads **99/99** on every run after the first. Measured: **76 before
  the output existed, 99 after.** Excluded by construction, pinned by T41. A headline that
  flips to 100% on a second invocation is not a number.
- **Axis E, first check — clean.** T41 already named two modules in earlier fixtures.
  Measured impact: **zero files anchored only by T41**, because T33 and T40 name them too.
- **Axis E, second check — real, and it was my own repair that caused it** (F9). The
  can-fail leg written *for* the axis-E correction put a real basename in its fixture and
  moved the strict count **44 → 45 by existing**. Rewritten with synthetic names and pinned
  by `test_t41_this_file_does_not_perturb_axis_e`.

- **Axis D again, at arc scale — real, and a fired gate caught it** (F10). Writing *this
  report* made all 99 files cited. Excluded; headline unmoved at 76.

**The first check passing is why the others are worth recording**: a self-reference that
comes back clean once is not a property of the instrument, it is a fact about that moment's
fixtures — and it stopped being true two edits later, then again at the closing run. **Only
one of the four was found by looking; three were found by a check that fired.**

---

## Compensators, discharged

| action | state |
|---|---|
| `tools/instrument_census.py` + its two outputs | added; `git revert` restores, outputs are derived and regenerate |
| running instruments against a recorded tree | **never done.** Axis F probes only the 5 guarded files, with `--help`, and refuses the other 94 |
| recorded trees | manifest **three times** — before the census, after it, and at the close: **0/0/0** each time, 7,312 files, 17,072,807,610 bytes |
| the index DB + certificate | **not touched.** The advisor folds the pair |

---

## What this moves, and what is NOT decided here

**Not decided, by the dispatch and by CLAUDE.md:** the boundary. Axis G is a **proposal**;
`no opinion` is used three times and `ambiguous` seventeen. The advisor rules and the
Director adjusts.

**Three things the census moves in task 2's scope**, which is what the halt was for:

1. **F3 — the population is narrower than the question.** Two of four already-served tools
   are implemented in `tools/verify/`, which no census has measured.
2. **F7 — `mesh_topology` has two candidate instruments**, and the planned wrap names one.
3. **F6 — `anchor_check` has no implementation** and the five nearest are all `ambiguous`.

**Unchanged by the census:** `offsurface_rate`'s bake half exists (`e12_offsurface.py`, and
it is the most-cited file in the directory at 16); the erode / margin-statistic half appears
in **neither** offsurface instrument, exactly as [E27 Ruling 2](E27-ruling.md) measured.

**⛔ HALT. Task 2 does not begin until this is ruled.**
