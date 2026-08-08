# E23 — predictions, committed before any file under `tools/` was opened

**Executor session, 2026-08-08.** Spec:
[E23-route-gates-kickoff.md](E23-route-gates-kickoff.md). This file is committed
**before the first `tools/` file is read as source**, and it is scored in
`E23-route-gates-report.md`.

---

## What I knew when I wrote this, stated exactly

The dispatch's closing instruction is binding and it changes the order of work:
*"check that the population is real before you predict its density … every quantity
you are asked for is a property of an ENUMERATED set. Count it first."* E22's P18
missed by ~44× because it predicted a property of a class that did not exist. So the
population was **measured first**, by a script that emits per-file **counts only** —
no source text, no shape data — precisely so that the predictions below stay blind on
every property except cardinality.

**Measured before writing this file** (`assert_census.py`, cardinality only):

```
tools/ TOP LEVEL      ANDON 57 across 12 files      non-ANDON 4
tools/diagnostics/    ANDON 132 across 42 files     non-ANDON 2
tools/superseded/     ANDON 1                       non-ANDON 6
tools/verify/         ANDON 1                       non-ANDON 3
REPO-WIDE tools/      ANDON 191 · non-ANDON 15 · 150 .py files
```

Every per-file cell of the dispatch's table reproduces exactly: `bake_hero_prep` 15,
`brush_cloud_step` 9, `subject_profile` 6, `e13_harmonize` 5, `bake_hero_fuse` 4,
`bake_hero_pack` 4, `silhouette_masks` 4, `cull_unseen` 3, `export_asset_source` 2,
`palette_gate` 2, `resample_atlas` 2, `restylize_views` 1. **The 57 is verified, not
inherited**, and so are E22 Ruling 4's 191/132/1/1 and Ruling 3's 15.

**Handed to me by the dispatch, so no row below is blind on these** — 31 of 57
multiline · 0 `not`-conditions · 0 sharing a first line · 0 without a message · 10
pinned-interpreter files (38 sites) vs 2 Blender files (19 sites) · 11 of 12 execute
at import · 3 have zero function definitions · one `except AssertionError` in all of
`tools/` at `facet_index.py:216` · one broad `except Exception` among the twelve at
`palette_gate.py:189` wrapping a font load · E22 Ruling 5's 44 repo-wide `SystemExit`
ANDONs with 3 of the twelve carrying both forms.

**Not known to me at this commit:** any source line of any of the 57 sites; where in
its file's control flow each site sits; what inputs each tool takes beyond the two the
dispatch names (`palette_gate` images, `subject_profile` JSON) and the two whose text
E22's report quotes (`resample_atlas:94`, `silhouette_masks:160`); which files import
what.

Blindness per row below: **B** = blind, **S** = semi-blind (leans on something the
dispatch or E22's report handed me, named in the row), **C** = a commitment rather
than a forecast, **M** = the population was measured first, as described above.

---

## The five the dispatch names

| id | class | prediction |
|---|---|---|
| **P1** | S | **57 of 57 sites splice by line range with no hand fix.** Band **54–57**. Leans on the dispatch's four shape claims, which I have not yet verified; E22 hit 88/88 with the same four properties holding. |
| **P2** | B | **Yes to both**, at every site: `py_compile` **12/12** after conversion, and the `--help` smoke **10 files × 3 modes = 30/30** exit 0 with the scratch cwd still empty. |
| **P3** | M | **14 of the 57 gates can be fired hermetically.** Band **8–22**. |
| **P4** | B | **No — 0 of the 57 is not a gate.** Band 0–3. |
| **P5** | S | **No handler newly catches the raise — 0 sites.** And 0 of the 57 sit lexically inside a `try` whose handler would catch `AssertionError` or `Exception`. Band 0–1. |

### P1 — what a hand fix would look like

A line-range splice fails where the range is not the whole statement or carries
something that is not the statement. The forms I expect if the number comes back below
57: a **trailing comment** on the site's last line (deleted by the splice, and it would
surface as a non-zero comment-token diff rather than as a syntax error); a **backslash
continuation**; a message whose implicit string concatenation carries an interior
comment; or a site whose closing paren shares a line with the next statement. The
dispatch's "0 share their first line" does not by itself exclude the *last* line.

### P2 — what a "no" would look like, since I predicted yes

**`py_compile`:** an `IndentationError` or `SyntaxError` on one named file, from a
continuation line re-indented by the wrong amount or a dropped closing paren. It would
be caught before anything else runs and would name its file and line.

**The `--help` smoke:** three distinct shapes, and they are not equally likely.
1. A **non-zero exit** — the realistic cause is an exception at *import*, because 11
   of the 12 execute at import, so a splice that re-parented a statement out of a
   function into module scope raises `NameError`/`IndentationError` there rather than
   at the gate.
2. **Exit 0 but the scratch cwd is not empty** — the tool wrote something on the
   `--help` path. That would be a pre-existing property, not something the conversion
   could introduce, so it would fire identically on the baseline run; I predict the
   baseline is clean on all ten.
3. A **mode-dependent** failure — passing normally and failing under `-O`. The
   conversion cannot cause this on the `--help` path (no gate is on it), so if it
   appears it is a finding about the file, not about the splice.

### P3 — the reasoning, because this is E22 P18's seat

**19 of the 57 are excluded by construction, not by difficulty.** `bake_hero_prep` (15)
and `bake_hero_pack` (4) `import bpy`; the dispatch forbids a Blender harness. So the
firable set is a **property of 38 sites in 10 files**, and that is the denominator I am
predicting against — stating it because P18's error was predicting against a
denominator that did not exist.

Of those 38, four tools are named as taking constructible input: `palette_gate` 2 and
`subject_profile` 6 (the dispatch), `resample_atlas` 2 and `e13_harmonize` 5 (images,
inferred from E22's quoted `resample_atlas:94` and the tool names) = **15 sites**. Not
all 15 will be reachable — a gate sitting behind a cloud call, a GPU render or an
`open3d` step is not hermetic at any price — and some of the remaining 23 sites in
`bake_hero_fuse`, `brush_cloud_step`, `silhouette_masks`, `cull_unseen`,
`export_asset_source` and `restylize_views` will be cheap early input-shape checks.

**What I have not measured and am therefore genuinely uncertain about: the depth of
each site in its file's control flow.** That is the whole variance, and it is why the
band is wide in both directions rather than tight around the point. 14/38 is 37%.

### P4 — and the separate quantity that is easy to confuse with it

All 57 carry the token by construction, so "not a gate" can only mean an ANDON whose
failure decides nothing irreversible: an unreachable site, or one in a path whose only
output is stdout. E22 Ruling 3 found the taxonomy maintained rather than accidental, so
I predict **0**.

**Distinct, and predicted separately:** the count of the 57 with **no write later in
their own scope** by E22's F1b walk. Repo-wide that was 175 of 191 (8.4% without). The
route tools write *more* than the diagnostics that dominate the 191, so I predict
**4 of 57**, band **2–8** — not 0, because argument-validation gates that precede a
function's return rather than its write do exist.

### P5 — why the structural answer is no

**`assert cond, msg` already raises `AssertionError(msg)`.** A handler that catches
`AssertionError` or `Exception` therefore catches the fired gate *today*, before any
conversion. The converted form raises the identical type, so under a normal interpreter
**no handler can newly catch anything** — the set of handlers that catch it is unchanged
by construction. The only new catching happens **under `-O`**, where the assert did not
fire at all and now does; that is the arc's entire purpose and not a defect.

So the useful form of this question is the one I predict at 0 with band 0–1: **does any
of the 57 sit inside a `try` that swallows it** — a gate whose halt its own file eats.
If one exists it is a finding for the ruling, not something to fix here. I also predict
`palette_gate.py:189`'s broad `except Exception` **wraps a font load and encloses none
of that file's 2 sites**, exactly as the dispatch states.

---

## The rest, so the report has something to score

| id | class | prediction |
|---|---|---|
| **P6** | S | The dispatch's four shape claims reproduce exactly: **31 multiline · 0 `not`-conditions · 0 shared first lines · 0 missing messages.** |
| **P7** | C | **Whole-file AST equality 12 of 12, zero reverts.** A commitment: a file that does not prove identical reverts rather than being adjusted. |
| **P8** | C | **0 comment tokens changed** across the twelve. |
| **P9** | B | Gate 1 baseline is **275** exactly, 0 failed, 0 skipped, artifacts tier live. |
| **P10** | B | Suite after: **1 new test file**, **5–10 test functions**, **30–60 cases**; total in the band **300–345**. |
| **P11** | B | The three E23 target files carrying `SystemExit` ANDONs are **`brush_cloud_step` (4), `e13_harmonize` (3), `restylize_views` (3)** = 10 sites, from E22 Ruling 5's concentration list. Reported as a collision, not resolved. |
| **P12** | B | Manifest: **≥ 7,312 files**, and the recheck holds at **0 added / 0 removed / 0 changed** on all three runs. |
| **P13** | B | **CI green, no workflow edit.** |
| **P14** | B | **3–6 findings** in the report, and **at least one** concerns a site's reachability or its depth rather than the splice. |
| **P15** | B | The `--help` **baseline** smoke passes 30/30 before conversion, so the after-run is a genuine before/after rather than a first measurement. |

---

## What this session will not do

Convert anything outside the 57 · touch `superseded/` · unify `SystemExit` · restructure
a script into a module · import any of the twelve in a test · run either Blender tool ·
build a Blender harness · write to the memory store · tag or publish.
