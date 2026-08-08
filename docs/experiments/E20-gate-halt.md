# E20 — HALT at the sequencing gate, before any unit was written

**Executor session, 2026-08-08, 11:23-11:31.** The dispatch's own precondition
fired on the first check of the session. Nothing was written into the shared
`tests/` lane; no unit test exists yet.

**Why this file and not `E20-coverage-report.md`:** the dispatch names that path
as the halt destination, but it specifies a *per-tool coverage table* as its
content, and no coverage was produced. Writing it now would either be an empty
report at the reserved path or force the eventual real report to overwrite one.
This repo already has three halt-before-the-work precedents in `E14`
(`handoff7-stroke1-halt`, `handoff7-task2-halt`, `handoff8-step0-halt`), so this
follows that form and leaves `E20-coverage-report.md` unwritten for the coverage
run. **The deviation is named here rather than taken silently.**

---

## 1. The gate

> ⚠ **SHARED COPY — sequencing is load-bearing**: this session fires **after E18
> halts** (both lanes write `tests/` and `conftest.py`; the D2 synthetic-state
> fixture E18 delivers is U3's substrate).
> — `E20-coverage-kickoff.md`

**E18 has not halted, and is writing this session's shared lane right now.**
Three independent legs, all measured:

> ⏱ **Read §1.5 with this section.** Leg 1's tables are the state at 11:23:36 and
> 11:27:07. E18 committed that work at 11:31 and moved on; §1.5 carries the
> correction and the sharper finding it produced. Legs 2 and 3 are unchanged.

### Leg 1 — E18 is live in this working copy

The tree grew new files *between two of this session's own observations*, 3 min
31 s apart. Both listings are `Get-ChildItem E:\AI\facet\tests -Filter *.py`:

| file | LastWriteTime | present at 11:23:36? | present at 11:27:07? |
|---|---|---|---|
| `mcp_support.py` | 11:22:17 | yes (untracked) | yes |
| `test_t19_record_mcp_readonly.py` | 11:22:53 | yes (untracked) | yes |
| `test_t20_record_mcp_certificate.py` | 11:23:41 | **no** | yes (untracked) |
| `test_t21_record_mcp_health.py` | 11:24:49 | **no** | yes (untracked) |
| `test_t22_record_mcp_tools.py` | 11:25:47 | **no** | yes (untracked) |
| **`conftest.py`** | **11:26:01** | tracked, clean | **tracked, ` M` modified** |
| `test_t18_interpreter_precheck.py` | 11:26:06 | tracked, clean | **tracked, ` M` modified** |

The last two rows are the load-bearing ones. `conftest.py` is the exact file the
dispatch names, and it went from clean to uncommitted-modified **65 seconds
before** the second observation. `test_t18_interpreter_precheck.py` — an existing
tracked test — is modified in the same window.

`git status --short` at 11:27:07:

```
 M README.md
 M docs/index/facet.db
 M tests/conftest.py
 M tests/test_t18_interpreter_precheck.py
?? CHANGELOG.md
?? SCORECARD.md
?? SECURITY.md
?? SHIP_GATE.md
?? tests/mcp_support.py
?? tests/test_t19_record_mcp_readonly.py
?? tests/test_t20_record_mcp_certificate.py
?? tests/test_t21_record_mcp_health.py
?? tests/test_t22_record_mcp_tools.py
?? tools/record_mcp.py
```

E18's D1 deliverable `tools/record_mcp.py` (43,691 bytes) is **untracked** — its
work is uncommitted, in-flight, in the same working copy. Its D5 deliverable
(`E18-index-mcp-report.md`, the file that ends in "HALT") **does not exist**.

The mechanism the dispatch warns about is not hypothetical here: two sessions
editing one uncommitted `conftest.py` in one working copy is last-writer-wins,
and neither session would necessarily notice which half survived. U1-U5 all
require new fixtures and conftest additions.

**Test count**, `pytest --collect-only -q` under the trellis2-env python:
**32 committed → 86 collected** in the live tree. All 54 of that growth is
E18's, and none of it is committed.

### Leg 2 — D2 does not exist

`Test-Path E:\AI\facet\tests\fixtures` → **False**.

D2 is E18's deliverable — "a synthetic minimal state (tiny mesh, tiny atlas, tiny
prep — deterministic, committed in-repo)" (`E18-index-mcp-kickoff.md`, line 95) —
and the E20 dispatch names it **U3's substrate**. U3 has no ground to stand on
until it lands.

### Leg 3 — U6's scope is not stable

U6 is specified over "every `assert`/ANDON/refusal in `tools/`".
`tools/record_mcp.py` is in `tools/`, is 43,691 bytes, carries **35 guard-shaped
lines**, and is uncommitted. A U6 list built now is wrong by construction the
moment E18 commits. This is P19 in `E20-predictions.md`, written before this
section.

---

## 1.5 ADDENDUM, 11:31:44 — the tree moved during the halt, and Leg 1 must be corrected in place

Sections 1's tables are the record of what was measured at **11:23:36 and
11:27:07** and are left standing as that record. Between then and 11:31:44, two
commits landed from the parallel lanes:

| commit | lane | what |
|---|---|---|
| `1565e9a` | E19 | Phase 0, the shipcheck gate (CHANGELOG / SCORECARD / SECURITY / SHIP_GATE / README) |
| `12f6381` | E18 | **D1: the record-index MCP server + 55 hermetic tests** |

**Leg 1's collision is now a matter of record rather than a hypothetical.**
`git show --stat 12f6381 -- tests/` :

```
 tests/conftest.py                        |   9 +-
 tests/mcp_support.py                     | 130 ++++++++++++
 tests/test_t18_interpreter_precheck.py   |   3 +
 tests/test_t19_record_mcp_readonly.py    | 252 ++++++++++++++++++++++++
 tests/test_t20_record_mcp_certificate.py | 230 ++++++++++++++++++++++
 tests/test_t21_record_mcp_health.py      | 305 +++++++++++++++++++++++++++++
 tests/test_t22_record_mcp_tools.py       | 326 +++++++++++++++++++++++++++++++
 7 files changed, 1254 insertions(+), 1 deletion(-)
```

E18's D1 **modified `tests/conftest.py` (+9/-1)** — the exact file the gate names.
Had this session added fixtures to `conftest.py` in the 11:23-11:31 window, one of
the two edits would have survived and neither session would have been told which.

**What has changed, measured at 11:31:44:**

- E18's D1 work is **committed**; `tests/` is clean of it. The uncommitted-tree
  hazard of Leg 1 is at rest **for this slice**.
- **E18 is still live and still in `tests/`** — `.mcp.json` and
  `tests/test_t23_mount_path.py` are untracked at 11:31:44. E18 has moved to D4
  (the live mount proof).
- **E18 still has no report.** `docs/experiments/E18*report*` does not exist. The
  dispatch's precondition — "fires after E18 **halts**" — is unsatisfied.
- **D2 still does not exist.** `tests/fixtures/` absent. E18 has delivered D1 and
  moved to D4 with D2 outstanding, so U3's substrate is not merely late — it has
  been passed over in E18's own order.
- Test count: **32 committed at session start → 89 committed at `12f6381` → 90
  collected** in the live tree (the 90th is E18's untracked T23).

**And the collision can now be stated more sharply than the dispatch stated it.**
`tests/fixtures/` **does not exist yet**, and it is simultaneously:

- **D2's home** — "a synthetic minimal state (tiny mesh, tiny atlas, tiny prep),
  deterministic, committed in-repo" (E18 kickoff line 95), and
- **U2's and U5's home** — "a `tests/fixtures/` builder in the D2 pattern"
  (E20 kickoff, Fixtures).

The E20 dispatch says the builder follows "the D2 pattern" — a pattern that does
not exist yet. **Whoever creates that directory first sets its builder pattern,
and the other lane inherits it.** That is a design collision, not a file
collision, and no amount of file-specific `git add` discipline prevents it.

---

## 2. Session-start ritual — measured, PASSED as the tool reports it

Run against a **scratch `--db`**, not the tracked `docs/index/facet.db`. Reason:
`conftest.py` lines 197-199 record that the tracked DB is exactly what a live
session's verify races (E16 report section 2), and a live session is present. The
dispatch's own standing rule says "scratch paths for any DB comparison". The
tracked DB was left untouched; it is ` M` in the status above from another lane,
not from this one.

```
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py build  --db <scratch>
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py verify --db <scratch>
```

| table | rows |
|---|---|
| artifacts | 665 |
| decisions | 225 |
| **experiments** | **20** |
| fts | 3565 |
| handoffs | 31 |
| laws | 71 |
| phenomena | 27 |
| prose_sections | 1999 |
| rulings | 527 |

Verify: **`VERIFY PASSED - all four legs`**, exit 0. Seeded set **19 / 19**, every
target within the top 3. Determinism leg that held: **byte-identity**.
`experiments` reads 20 — E20's kickoff is in the record.

---

## 3. What this session produced

| artifact | status |
|---|---|
| `docs/experiments/E20-predictions.md` | **committed** — 20 rows, blindness disclosed per row, written before any unit's internals were read |
| the read-only guard census (§4) | measured, **provisional** per Leg 3 |
| the coverage baseline (§5) | measured, read-only — **at the 32-test tree**, superseded as a baseline by E18's D1 (89 committed); kept because it is the shape the dispatch was written against |
| the `tests/fixtures/` pattern-ownership finding (§1.5) | measured, and not in either dispatch |
| any file under `tests/` | **none — the gate** |
| `conftest.py` edits | **none — the gate** |
| `tests/fixtures/` | **none — the gate** |

Predictions were written first and committed because the dispatch orders them
first, they must be blind to be worth anything, and they live entirely in the
`docs/experiments/E20-*` lane where nothing collides. Reading and grepping write
nothing.

---

## 4. Provisional guard census — read-only, `tools/` (U6's scope estimate)

**These are grep counts of guard-*shaped lines*, not a deduplicated guard count.**
P17 predicts they overstate distinct fireable guards by roughly 2:1, because this
repo writes an explanatory comment naming an ANDON directly above the code that
raises it. The dedup is U6's actual work and has not been done.

Tracked tools: **33** files, **31** with at least one guard-shaped line.
Totals: `assert` **148** · ANDON mentions **243** · `raise` **23** ·
`sys.exit(` **17** → **431 lines**.

| tool | assert | ANDON | raise | exit | total |
|---|---|---|---|---|---|
| `e11_manifest.py` | 35 | 36 | 2 | 0 | **73** |
| `e11_export_turnaround.py` | 24 | 26 | 2 | 0 | **52** |
| `project_twins.py` | 18 | 23 | 1 | 0 | **42** |
| `bake_hero_prep.py` | 15 | 18 | 1 | 0 | 34 |
| `brush_cloud_step.py` | 9 | 16 | 4 | 0 | 29 |
| `texpass_iter.py` | 9 | 13 | 0 | 1 | 23 |
| `e13_harmonize.py` | 5 | 10 | 3 | 0 | 18 |
| `export_asset_source.py` | 2 | 13 | 0 | 1 | 16 |
| `e10_sea_composite.py` | 0 | 10 | 1 | 4 | 15 |
| `subject_profile.py` | 6 | 7 | 0 | 0 | 13 |
| `texpass_finalize.py` | 4 | 7 | 0 | 0 | 11 |
| `silhouette_masks.py` | 4 | 6 | 0 | 0 | 10 |
| `e10_contact_mask.py` | 0 | 8 | 0 | 1 | 9 |
| `bake_hero_fuse.py` | 4 | 5 | 0 | 0 | 9 |
| `restylize_views.py` | 1 | 4 | 3 | 0 | 8 |
| `e10_waterline_candidates.py` | 0 | 7 | 0 | 1 | 8 |
| `bake_hero_pack.py` | 4 | 4 | 0 | 0 | 8 |
| `palette_gate.py` | 2 | 4 | 0 | 1 | 7 |
| `e10_layer_export.py` | 0 | 6 | 0 | 1 | 7 |
| `cull_unseen.py` | 3 | 4 | 0 | 0 | 7 |
| `texpass_brush.py` | 0 | 2 | 2 | 0 | 4 |
| `resample_atlas.py` | 2 | 2 | 0 | 0 | 4 |
| `facet_index.py` | 1 | 2 | 0 | 1 | 4 |
| `e10_layer_seed.py` | 0 | 3 | 0 | 1 | 4 |
| `smart_decimate.py` | 0 | 2 | 0 | 1 | 3 |
| `e10_w1_coverage.py` | 0 | 2 | 0 | 1 | 3 |
| `e10_toggle_sheet.py` | 0 | 1 | 0 | 2 | 3 |
| `e10_layer_paste.py` | 0 | 2 | 0 | 1 | 3 |
| `normalize_mesh.py` | 0 | 0 | 2 | 0 | 2 |
| `ig2mv_licensefree.py` | 0 | 0 | 2 | 0 | 2 |
| *(untracked, E18's)* `record_mcp.py` | 1 | 18 | 15 | 1 | *35* |

`mask_geometry.py` and `mesh_stats.py` carry **zero** guard-shaped lines by this
grep — worth stating, because two U2/U5 units having no guards at all changes what
U6 can say about them.

---

## 5. Coverage baseline — which tools the 32 committed tests reach at all

By grep over the tracked tests for tool invocations:

| tool | test references | level |
|---|---|---|
| `facet_index` | 18 | subprocess + in-process import (`facet_index_mod`) |
| `texpass_iter` | 6 | subprocess |
| `mesh_stats` | 4 | subprocess |
| `e08_ceiling` | 4 | subprocess |
| `project_twins` | 4 | subprocess |
| `e12_elevated` | 3 | subprocess |
| `texpass_finalize` | 2 | subprocess |
| `e04_registry_sweep` | 1 | subprocess |

**8 of 33 tracked tools are reached by any test**, and every one of them at
whole-tool subprocess level. `mask_geometry.py` — a U2 unit — is reached by
nothing. This is the measured shape of the Director's "32 tests is weak": not
that 32 is a small number, but that the 32 enter through eight front doors and
nothing below them is addressed directly.

---

## 6. What was not done, per unit

| unit | state | reason |
|---|---|---|
| U1 `facet_index` parsers | **not started** | pure-text, hermetic, needs no D2 — blocked only by the shared `tests/` lane |
| U2 `project_twins` core + `mask_geometry` | **not started** | same |
| U3 `texpass_iter` write-head | **blocked twice** | shared lane **and** D2 absent (Leg 2) |
| U4 `texpass_finalize` lookup | **not started** | shared lane |
| U5 `mesh_stats` + frame math | **not started** | shared lane |
| U6 guards audit | **census only** | scope unstable until E18's tool commits (Leg 3) |

U1, U2, U4 and U5 need nothing from E18 except the lane. If E18's work were
committed — or if this session were given a separate working copy — those four
proceed immediately.

---

## 7. The halt

Executor rule 3: *stop at every gate; never improvise past one; if a gate fires,
report it with its evidence and halt.* The gate's stated mechanism ("both lanes
write `tests/` and `conftest.py`") is exactly what was measured, 65 seconds
before the measurement, on the named file.

**Open for the Director and the advisor** — the three dispositions this session
can see, without recommending among the ones that are not its call:

1. **Wait for E18's halt**, then run E20 unchanged against a committed tree. Costs
   wall-clock, changes nothing else. §1.5 makes this cheaper than it looked at
   11:27: E18 commits in slices, so the shared lane clears between them.
2. **Give E20 its own working copy** (a second clone or a worktree). U1, U2, U4, U5
   proceed now; U3 still waits for D2; U6's scope still needs E18's tool. Merging
   two `conftest.py` histories afterwards becomes the new risk, and this session
   does not rule on whether that trade is worth it. **§1.5's `tests/fixtures/`
   finding survives this option** — a worktree isolates the files and not the
   pattern, so two builders would be authored independently and reconciled later.
3. **Re-scope E20** to the units that touch neither `conftest.py` nor `tests/` —
   which is none of them under the current unit list.
4. **Order the fixtures directory explicitly** (added after §1.5, and the cheapest
   of the four if E20 is to run before E18's halt): rule *now* whether `tests/`
   `fixtures/`'s builder is D2's to author or E20's, and have the other lane
   consume it. The dispatch currently points E20 at "the D2 pattern" while E18 has
   passed D2 over to reach D4 — so the pattern's author is undetermined by both
   dispatches, and that is an advisor question rather than a race to `mkdir`.

**Not this session's call, and flagged rather than assumed:** whether
`tools/record_mcp.py` is inside U6's scope (P19). E18's tests are its own lane by
the dispatch's lane rules, but U6's scope sentence says "every `assert`/ANDON/
refusal in `tools/`" without exception. The advisor rules.

Nothing was written to the memory store. No DB was committed. The tracked
`docs/index/facet.db` was not touched by this session.

---

## 8. The Director's disposition, 2026-08-08 (appended after §7 was written)

Both questions in §7 were put to the Director. He ruled:

| question | ruling |
|---|---|
| how E20 proceeds | **Disposition 1 — wait for E18's halt.** Not the partial run this session offered (U1 + inline-fixture probes as new files at T24+, no `conftest.py` edits, no `tests/fixtures/`), and not the worktree. E20 runs unchanged against a committed tree after E18 reports. |
| who authors `tests/fixtures/`'s builder | **Deferred to the advisor's ruling** (`E20-ruling.md`). E20 touches no fixtures directory until then. |

Both rulings are more conservative than the options this session leaned toward,
and both are consistent with the repo's own laws: the executor decides neither the
meaning of a result nor the resolution of a scope question, and a partial run
whose safety rests on "these particular units happen not to need `conftest.py`"
would have put the gate's protection on a property of the current unit list rather
than on the gate.

**E20 is therefore parked, not abandoned.** Its entry state is measured and
committed (§2, §4, §5), its predictions are committed blind (`E20-predictions.md`),
and the two things that must be true before it fires are now written down as
checkable conditions rather than a sequencing sentence:

1. `docs/experiments/E18-index-mcp-report.md` exists (E18 has halted), **and**
2. the `tests/fixtures/` builder's author is ruled in `E20-ruling.md`.

Condition 2 is new — it did not exist in the dispatch, and §1.5 is why.

The session did not end here on its own account; the work halted at the gate and
the Director ruled on the halt.
