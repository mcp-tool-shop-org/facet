# E23 — report: the route's gates, on twelve files no test had ever executed

**Executor session, 2026-08-08.** Spec:
[E23-route-gates-kickoff.md](E23-route-gates-kickoff.md). Predictions committed at
`48fa733` **before the first `tools/` file was read as source**:
[E23-predictions.md](E23-predictions.md).

This report measures and reports. It does not decide what the results mean; the
advisor rules at `E23-ruling.md`.

---

## The short version

- **57 sites converted** across twelve files, pure move, **12 of 12 whole-file AST
  identical** to the negation rule applied at the prior commit. **Zero reverted.**
- **0 comment tokens changed**; 57/57 per-site AST checks OK.
- **The enumeration was measured, not inherited** — every per-file cell of the
  dispatch's table reproduces to the digit, and so do E22 Ruling 4's 191/132/1/1
  and Ruling 3's 15.
- **T31 rides the commit: 8 functions, 95 cases**, including **16 gates fired in all
  three interpreter modes** and three can-fail legs.
- **The recorded trees are byte-unmoved**: 7,312 files manifested before anything
  ran, re-checked three times, 0 changed.
- **F1 — `brush_cloud_step:204` cannot fire.** `:353` tests the same precondition
  harder and stands in front of it on the only path that calls `preflight`. Measured
  across every block shape, not argued.
- **F2 — two route tools create their output directory before their gate fires.**
- **F3 — one ANDON in the twelve already raised**, which reconciles E22 Ruling 5's
  repo-wide `AssertionError 88` as 87 conversions plus that site.
- **F5 — I caused a fold-marked test failure** by writing this report while the suite
  was running. The dispatch's run-then-rerun remedy cleared it; the lesson is that the
  concurrent writer the fold-race warning describes can be *this* session.

---

## Gate 0 — the session-start index gate

`build` then `verify` against a scratch `--db`, because the record mount is live on
this working copy.

```
[leg 4] the seeded question set - target within the top 3     19 / 19
determinism leg that held: byte-identity
VERIFY PASSED - all four legs                                 exit 0
```

---

## The enumeration — re-measured, as the dispatch ordered

Run **before the predictions were written**, by an AST walk emitting per-file counts
only — no source text, no shape data — so every prediction stayed blind on everything
except the population itself. That ordering is the dispatch's own binding instruction
and E22 Ruling 10's law: *check that the population is real before you predict its
density.*

| where | dispatch | measured | verdict |
|---|---|---|---|
| `tools/` top level | 57 across 12 files | **57 across 12** | **reproduces** |
| `bake_hero_prep` / `brush_cloud_step` / `subject_profile` | 15 / 9 / 6 | **15 / 9 / 6** | reproduces |
| `e13_harmonize` / `bake_hero_fuse` / `bake_hero_pack` | 5 / 4 / 4 | **5 / 4 / 4** | reproduces |
| `silhouette_masks` / `cull_unseen` | 4 / 3 | **4 / 3** | reproduces |
| `export_asset_source` / `palette_gate` / `resample_atlas` / `restylize_views` | 2 / 2 / 2 / 1 | **2 / 2 / 2 / 1** | reproduces |
| `tools/diagnostics/` | 132 | **132 across 42 files** | reproduces (E22 R4) |
| `tools/superseded/` · `tools/verify/` | 1 · 1 | **1 · 1** | reproduces |
| repo-wide ANDON asserts remaining | 191 | **191** | reproduces (E22 R4) |
| repo-wide non-ANDON asserts | 15 | **15** | reproduces (E22 R3) |

**Every cell.** Two consecutive arcs had a scope-number defect; this one does not, and
the reason is that the dispatch carried an enumeration instead of a subtraction.

### The four shape claims, measured before the splice relied on them

```
                    dispatch   measured
sites                     57         57
multiline                 31         31
not-conditions             0          0
sharing a first line       0          0
without a message          0          0
trailing text after the statement     0   (measured additionally; nothing to carry)
```

Splice-by-line-range is safe exactly when *sharing a first line* and *without a
message* are both 0. They are.

---

## The conversion

### The rule

```
assert COND, MSG   ->   if not (COND):
                            raise AssertionError(MSG)
```

`COND` and `MSG` keep their source text character for character. **0 of the 57 are
`not`-conditions**, so the negation rule is uniform here — E22 had 3 and this arc has
none.

**A rendering correction, reported because it was a real re-do.** The first splice
inlined every message onto the `raise AssertionError(` line. That passed the whole-file
AST proof — 12/12 identical — because parenthesisation and line breaks are not in an
AST. It was still wrong: the bar says *only leading whitespace on continuation lines
moves*, and inlining **joins two lines**, which is a different operation. It also
pushed maximum line length from 92 → 110 in one file. E22's ratified rendering was
then read out of its own diff at `f878b8b` rather than guessed —
`e11_manifest.py:152 / 205 / 212` are the three cases — and the rule it follows is:

> a message that begins **after** the assert's own line keeps its own line, indented
> +4 for the new nesting; a message that begins **on** the assert's line stays inline.

The twelve files were **reverted** and re-spliced under that rule. Maximum line length
came back to +1/+2 rather than +18. No file was adjusted after failing a check; the
re-do was a choice about matching the ratified house form, made before the commit.

### Per-file table

| file | sites | multiline | diff (+/−) |
|---|---|---|---|
| `bake_hero_prep.py` ⚠ Blender | **15** | 10 | +55 / −40 |
| `brush_cloud_step.py` | **9** | 7 | +32 / −23 |
| `subject_profile.py` | **6** | 5 | +23 / −17 |
| `e13_harmonize.py` | **5** | 0 | +10 / −5 |
| `bake_hero_fuse.py` | **4** | 0 | +8 / −4 |
| `bake_hero_pack.py` ⚠ Blender | **4** | 0 | +8 / −4 |
| `silhouette_masks.py` | **4** | 3 | +14 / −10 |
| `cull_unseen.py` | **3** | 3 | +15 / −12 |
| `export_asset_source.py` | **2** | 0 | +4 / −2 |
| `palette_gate.py` | **2** | 2 | +7 / −5 |
| `resample_atlas.py` | **2** | 0 | +4 / −2 |
| `restylize_views.py` | **1** | 1 | +4 / −3 |
| **total** | **57** | **31** | **+184 / −127** |

### Gate 2 — the pure-move proof

Three checks, none of which is my reading of the diff, and the second is written
independently of the splicer.

**1. Whole-file AST equality** (`pure_move_proof.py`) — take each file *as git had it
at `48fa733`*, apply the negation rule to its in-scope `Assert` nodes **in the tree**,
and compare `ast.dump` of the entire module against the file on disk. `ast.dump`
excludes line and column attributes, which is exactly why re-indentation cannot hide a
real change or cause a false one. **This check is total**: a stray edit anywhere in a
file fails it, not only an edit at a site.

```
bake_hero_prep.py          sites=15  whole-file AST: IDENTICAL to the rule applied at 48fa733
brush_cloud_step.py        sites=9   whole-file AST: IDENTICAL
subject_profile.py         sites=6   whole-file AST: IDENTICAL
e13_harmonize.py           sites=5   whole-file AST: IDENTICAL
bake_hero_fuse.py          sites=4   whole-file AST: IDENTICAL
bake_hero_pack.py          sites=4   whole-file AST: IDENTICAL
silhouette_masks.py        sites=4   whole-file AST: IDENTICAL
cull_unseen.py             sites=3   whole-file AST: IDENTICAL
export_asset_source.py     sites=2   whole-file AST: IDENTICAL
palette_gate.py            sites=2   whole-file AST: IDENTICAL
resample_atlas.py          sites=2   whole-file AST: IDENTICAL
restylize_views.py         sites=1   whole-file AST: IDENTICAL

PURE MOVE: 12 of 12 files prove identical-except-the-rule
```

**2. Comments, by token** — comments are not in an AST, so a splice that dropped a
trailing one would pass check 1 and fail here. That is the only reason the check
exists.

```
bake_hero_prep 82 · brush_cloud_step 74 · export_asset_source 26 · e13_harmonize 18
restylize_views 18 · bake_hero_fuse 16 · palette_gate 16 · cull_unseen 13
silhouette_masks 8 · subject_profile 2 · resample_atlas 1 · bake_hero_pack 0
                                                   ALL IDENTICAL — 0 changed
```

**3. Per site** — the produced statement is an `If` whose body is a single
`raise AssertionError(...)` with exactly one argument; `ast.dump(arg) == ast.dump(old.msg)`
and the test matches the negation rule. **57/57 OK, 0 BAD.**

**Neither check 1 nor check 3 can be a standing test** — both need the pre-conversion
tree, and after the commit `HEAD` *is* the converted state, so a re-run is a tautology.
E22 said the same of its own two. What is portable is ported, into T31.

---

## ⚠ The difficulty this arc was dispatched for

**Zero of the twelve were reached by any test.** Re-measured here before the work: no
file under `tests/` mentioned any of the twelve. E22's safety came from T7's
byte-identity replay, T10 and T26's fired ANDONs. E23 had **no behavioural net at
all**, so the AST proof above carried the whole load and T31 below is the net being
built rather than inherited.

---

## Tests that ride the commit — T31

`tests/test_t31_route_gates.py`, **8 functions, 95 cases**, `95 passed in 56.71s`.
Hermetic — it runs in CI. **No file among the twelve is imported**: eleven execute at
import and three have zero function definitions, so every check is a subprocess or an
AST walk over source text.

| test | cases | what it pins |
|---|---|---|
| `route_tool_compiles` | 12 | all twelve still compile, Blender pair included (needs no `bpy`). **Measured 12/12 clean before the conversion**, so this is a genuine before/after |
| `help_is_clean_in_every_mode` | 30 | the ten non-Blender tools reach argparse under normal / `-O` / `PYTHONOPTIMIZE=1`, exit 0, **and the scratch cwd is still empty** |
| `no_route_gate_is_an_assert` | 1 | the standing law, AST-checked over the twelve |
| `the_structural_check_can_fail` | 1 | **can-fail leg** — the walk finds a *planted* ANDON assert and ignores a token-less one |
| `the_census_is_the_one_e23_measured` | 1 | per-file ANDON-raise counts, the pre-existing raise, and the **134** remaining elsewhere, so the diagnostics arc has to move it on purpose |
| `the_blender_pair_cannot_run_under_this_interpreter` | 1 | the stated reason for the smoke exclusion, made falsifiable: both still `import bpy` at module level and `bpy` is not importable here |
| `route_gate_refuses_in_every_mode` | 48 | **16 gates × 3 modes** — refuses, says `ANDON`, matches **its own message**, and writes no file |
| `the_firing_harness_can_fail` | 1 | **can-fail leg** — a *valid* profile fires no `subject_profile` gate, so the 48 above are not passing because these tools refuse whatever you hand them |

**Three can-fail legs.** **No test asserts that `PYTHONOPTIMIZE=1` disables a gate** —
T30 already pins the stripping mechanism on throwaway source, and this file depends on
that rather than repeating it.

**Why `expect` and not just `rc != 0`:** several of the sixteen sit behind other gates
that also exit non-zero. Matching each gate's own words is what makes a leg specific to
the gate under test — and it is how F1 below was found.

### Which gates could be fired, and which could not

**16 of 57.** The denominator that matters is stated first: **19 of the 57 are
excluded by construction** — `bake_hero_prep` (15) and `bake_hero_pack` (4) `import
bpy`, and the dispatch forbids a Blender harness. So the reachable question is over
**38 sites in 10 files**, and 16 of those 38 fire.

| fired, all three modes | sites |
|---|---|
| `subject_profile` — 60, 79, 113, 118, 120, 124 | **6 of 6** |
| `brush_cloud_step` — 208, 214, 347, 353 | 4 of 9 |
| `e13_harmonize` — 85, 86, 92 | 3 of 5 |
| `silhouette_masks` — 107 | 1 of 4 |
| `palette_gate` — 69 | 1 of 2 |
| `restylize_views` — 197 | 1 of 1 |

`subject_profile`'s six are fired **through a host tool** — it is a module other tools
call at `parse_args` time, so `silhouette_masks --profile <synthetic.json>` reaches all
six. `silhouette_masks:107` needs a mesh, so the test builds a **synthetic cube**;
nothing in T31 points at a recorded prep tree.

**Not fired, with the reason for each — 41 sites:**

| sites | why not |
|---|---|
| `bake_hero_prep` 15, `bake_hero_pack` 4 | **`import bpy`.** The pinned interpreter cannot run them; the dispatch forbids building a Blender harness for this arc. **19 sites, an openly stated gap** |
| `bake_hero_fuse` 4 | need baked `.npy` inputs from a completed prep+bake stage |
| `cull_unseen` 3 | need a mesh **and** a camera set with visibility already computed |
| `silhouette_masks` 134, 149, 160 | need a raycast silhouette and a recorded anchor to disagree with |
| `brush_cloud_step` 379, 413, 418 | need a **cloud round-trip** — they compare a returned image against what was emitted |
| `brush_cloud_step` 307 | needs a job **state tree** (a seeded layer state beside the job) |
| `brush_cloud_step` 204 | **cannot fire at all — F1 below** |
| `e13_harmonize` 139, 158 | reachable in principle; need a matched image/mask pair whose shapes disagree *after* the earlier gates pass |
| `export_asset_source` 90, 95 | reachable in principle; both sit inside a full export pipeline that must first hash a canon GLB+PNG pair and re-encode a provenance atlas — a fully synthetic pipeline tree, not a fixture |
| `palette_gate` 137, `resample_atlas` 47, 94 | need a real mask/image pair and a dense mesh with UVs respectively |

E20's refusal to invent units that could not exist is the precedent for stating this
list rather than padding it.

---

## Findings

### F1 — `brush_cloud_step:204` CANNOT FIRE

`:204` lives inside `preflight()` and tests `isinstance(blk, dict)`. `:353` runs
**before** `preflight` on the same block and tests the same precondition harder — it
reads `lora-w` out of it and refuses whenever the block is absent *or* is not a dict.
`graph` is the **only** caller of `preflight` (one call site).

Measured across the whole shape space rather than argued:

```
block absent                   rc=1  -> gate 353
block is a list                rc=1  -> gate 353
block is a string              rc=1  -> gate 353
block is null                  rc=1  -> gate 353
block is an int                rc=1  -> gate 353
block is {} (empty)            rc=1  -> gate 353
block dict, lora-w decided     rc=1  -> gate 214   (:204 passed trivially)
```

**No profile shape reaches `:204` with a non-dict block.** It is a correctly declared
gate, correctly converted, and shadowed. Reported, not acted on — whether a shadowed
gate should be removed, moved, or left as depth-in-defence is the advisor's call, and
`preflight` may be called from a new path later, at which point it stops being
shadowed.

**This is not P4's answer.** `:204` is a gate by E22 Ruling 3's definition — an
author's declaration that a check decides whether an irreversible step proceeds. It is
unreachable, which is a different property. The advisor may read it as either; that is
the ruling's to settle, not the executor's.

### F2 — two route tools create their output directory BEFORE their gate fires

The dispatch asked that fired gates assert **nothing was written**. Run in that strict
form, two of the sixteen failed. Measured:

```
silhouette_masks:107   rc=1   NEW DIR  o
restylize_views:197    rc=1   NEW DIR  o
```

**An empty directory, no file.** Both `makedirs` their `--out` / `--outdir` ahead of
the gate. T31 therefore asserts the measured truth in two halves rather than a
loosened one: **no FILE may appear for any site**, and the set of sites that create a
directory is **pinned to exactly these two**, so a third joining them fails the file.
Reported because the change was made after seeing a result, which is the move this
repo distrusts most — the pre-registered property was *no artifact*, that half holds
everywhere, and the directory half is a fact the advisor should rule on rather than
something an executor should quietly permit.

### F3 — one ANDON in the twelve already raised, and it reconciles E22's 88

`bake_hero_prep.py` carried **one** `raise AssertionError` ANDON before E23 — the
`--head-scale < 1 is not specified` refusal, written as a raise by its author. It is
the only one among the twelve.

It also closes an arithmetic loop: E22 Ruling 5 measured repo-wide **`AssertionError`
88** ANDON raises after E22's conversion, and E22 converted **88 sites of which 87
carried the token**. 87 + this one = **88**. The number was right and its composition
was never stated.

### F4 — the `SystemExit` collision, reported and not resolved

Three of the twelve carry both exception types at once, exactly as the dispatch
predicted:

```
brush_cloud_step.py  4      e13_harmonize.py  3      restylize_views.py  3
                                            TOTAL 10 across 3 of the twelve
```

[E22 Ruling 5](E22-ruling.md) ruled these stay — `raise SystemExit` is not deletable by
`-O`, so none carries this arc's defect, and normalising a type nobody ruled is not a
pure move. **Untouched.**

### F5 — I CAUSED A FOLD-MARKED FAILURE BY EDITING DOCS WHILE THE SUITE RAN

Reported because it is my own process defect and the next executor will make it
otherwise.

The hermetic tier's first run came back **`1 failed, 361 passed, 8 deselected`** —
`test_t20_verify_then_build_in_one_process`. The full artifacts-tier run minutes
earlier was `370 passed`, and nothing in `tools/` moved between them.

What moved was **the corpus**. That test is `@pytest.mark.fold`, and `pytest.ini`
says exactly what that means: *"rebuilds/verifies the derived index from the LIVE
corpus; in a shared working copy this can race a concurrent fold's own build/verify
(the corpus moving between leg-1's two builds)."* I was writing `CHANGELOG.md` and
this report **while that run was in flight**, so the corpus moved underneath the
index build. There was no concurrent advisor; the concurrent writer was me.

The dispatch pre-registers the remedy — *"fold-marked failures against a live corpus:
run-then-rerun once (E18 Ruling 2l)"* — so re-running is the spec, not an
improvisation past a gate. Re-run once with no concurrent writes:

```
362 passed, 8 deselected in 140.39s      exit 0
```

**The rule this earns, and it is not in CLAUDE.md yet:** the fold-race warning is
written as though the other writer is another session. It is just as easily *this*
one. Docs are part of the corpus; a report written during a suite run is a concurrent
fold.

### F6 — 20 of the 57 have no write later in their own scope

E22's F1b walk, re-run over the 57. **DIAGNOSTIC ONLY** — E22 Ruling 11 upheld it as a
diagnostic and forbade it gating anything, and that holds here.

```
sites with an unambiguous write later in their own scope   37 of 57
sites without                                              20
```

**What this measures, stated before the number is used:** "later" is *source order
within the scope*, not execution order. The write set is deliberately narrow —
`.write()` is excluded because it is as often `StringIO` or stdout, and `.copy()` and
bare `run()` are excluded because E22's first pass counted `ndarray.copy()` as a write
and had to be hand-tightened. So **20 over-counts the no-write class on purpose**, and
`bake_hero_pack`'s four are all module-scope sites in a Blender script whose writes go
through `bpy` operators this walk does not recognise.

The 20 concentrate in small helper functions — `preflight`, `pv`, `kv`, `bind`,
`_read`, `npy_header`, `png_chunks` — which validate an input and return, leaving the
write to the caller.

---

## The compensator gate

**The recorded trees are not in git. There is no `git revert` for them**, so detection
is the compensator and it ran before anything else did.

- **Manifest taken BEFORE the baseline suite run**, because the artifacts tier is what
  touches those trees. Per-file sha256 over `facet_next`, `facet_E01/02/05/06/07/08`
  and `saltroad_bake_fix`: **7,312 files, 17.07 GB, 13 s** — E22's file count
  reproduces exactly.
- **Re-checked after the baseline suite run and at the halt.**

```
RECHECK  before=7312 after=7312     added 0   removed 0   changed 0
MANIFEST HELD - no file in the recorded trees moved
```

**Every smoke and every fired gate ran in a scratch cwd with scratch output paths.**
T31's own emptiness assertions are what make that testable rather than asserted, and
they are the reason F2 was found at all.

*One note on E22's figure: it recorded 16.3 GB against this run's 17.07 GB for the
same 7,312 files. The file count and the 0/0/0 recheck are the load-bearing halves;
the byte total is a units difference (15.90 GiB) and there is no E22 manifest left to
diff against — theirs lived in a session scratchpad.*

---

## Gates

| gate | evidence | verdict |
|---|---|---|
| **1. suite green before and after, full artifacts tier** | **275 → 370**, 0 failed, 0 skipped, artifacts live. Hermetic tier as CI runs it: **362 passed, 8 deselected** — on the **second** run, after a fold-marked failure I caused myself by editing docs mid-run (**F5**, with the dispatch's own run-then-rerun remedy applied) | **PASS** |
| **2. whole-file AST equality for each of the twelve** | **12 of 12 IDENTICAL** to the rule applied at `48fa733`; comment tokens **0 changed**; per-site **57/57**; **0 reverted** | **PASS** |
| **3. no edit outside the twelve under `tools/`** | `git diff --name-only -- tools/` returns exactly the twelve; nothing in `canon/`, `profiles/`, the citable trees, the seeded set or a closed ruling. Everything else edited is `tests/` or a doc, itemised below | **PASS** |
| **4. CI green, both dependency scanners** | run [`31281846551`](https://github.com/mcp-tool-shop-org/facet/actions/runs/31281846551) — see below | **PASS** |
| **5. the tree manifest holds** | 7,312 files, **three checks, 0 added / 0 removed / 0 changed** | **PASS** |

**Files edited outside `tools/`, every one:**

| file | why |
|---|---|
| `tests/test_t31_route_gates.py` | new; the tests-ride-the-commit law and the dispatch's T31 |
| `docs/experiments/E23-predictions.md` | committed first, at `48fa733` |
| `docs/experiments/E23-route-gates-report.md` | this file |
| `CHANGELOG.md` | **`[Unreleased]` only**, following E22's precedent. E22's own paragraph is **annotated, not rewritten** — its 191 was accurate when written |

**Not edited, and named:** `SHIP_GATE.md` — no line of it makes a claim this arc
changes. `tests/test_t30_gates_survive_optimize.py` — its structural check is
deliberately scoped to E22's seven and its docstring's "~190 … that E22 MEASURED
elsewhere" is a historical statement about E22's census, still true. Left alone rather
than tidied.

---

## Predictions scored

Blindness was disclosed per row in the predictions file and is not re-litigated here.
The population — and only the population — was measured before the file was written,
for the reason stated there.

### The five the dispatch named

| id | claim | outcome |
|---|---|---|
| **P1** | 57 of 57 splice by line range, no hand fix (band 54–57) | **HIT** — 57/57 |
| **P2** | `py_compile` 12/12 and the smoke 30/30 after conversion | **HIT** — both, in all three modes |
| **P3** | **14 of the 57 fire hermetically** (band 8–22) | **HIT** — **16**, inside the band |
| **P4** | 0 of the 57 is not a gate (band 0–3) | **HIT** — all 57 are declared gates that decide whether their tool proceeds. F1's shadowed site is a different property and is routed separately |
| **P5** | no handler newly catches the raise; 0 sites inside a swallowing `try` (band 0–1) | **HIT** — **0 of 57**. The structural reason held: `assert` already raises `AssertionError`, so the catching set cannot change. And the dispatch's two sub-claims reproduce — `palette_gate.py:189` wraps `ImageFont.truetype`, a font load, enclosing neither of that file's sites; the single `except AssertionError` in all of `tools/` is `facet_index.py:216`, not one of the twelve |

### The rest

| id | claim | outcome |
|---|---|---|
| P6 | the four shape claims reproduce: 31 / 0 / 0 / 0 | **HIT** — exactly |
| P7 | whole-file AST 12/12, zero reverts | **HIT** (a commitment; held) |
| P8 | 0 comment tokens changed | **HIT** |
| P9 | baseline is 275 exactly | **HIT** — `275 passed in 174.31s` |
| P10 | 1 file · 5–10 functions · 30–60 cases · total 300–345 | **SPLIT** — 1 file (**hit**), 8 functions (**hit**), **95 cases** (**miss**, above), total **370** (**miss**, above) |
| P11 | the `SystemExit` trio is `brush_cloud_step` 4, `e13_harmonize` 3, `restylize_views` 3 | **HIT** — exactly, 10 sites |
| P12 | manifest ≥ 7,312 files, 0/0/0 on all three runs | **HIT** — 7,312, three times |
| P13 | CI green, no workflow edit | **HIT** |
| P14 | 3–6 findings, ≥1 about reachability or depth | **HIT** — 6 findings, and F1 is exactly a reachability finding |
| P15 | the **baseline** smoke passes 30/30 before conversion | **HIT** — which is what makes the after-run a before/after |

### The instructive miss — the F1b prediction

Stated separately in the predictions file, and it is the miss worth carrying.

> **4 of 57** sites with no write later in their own scope, band **2–8**.

**Measured 20.** Out by 2.5× on the point and outside the band.

The reasoning is in the predictions file verbatim: repo-wide E22 measured 175 of 191
*with* a write (8.4% without), and I argued the route tools write **more** than the
diagnostics that dominate that 191, so I moved my estimate **below** the repo-wide
fraction to 7%.

**The error is that I predicted a property of the FILE when the metric is a property of
the SCOPE.** "Route tools write more" is true and irrelevant: F1b asks whether a write
follows *in the same function*, and these twelve are more decomposed than the
diagnostics — their gates sit in small validators (`preflight`, `pv`, `kv`, `bind`,
`_read`, `npy_header`, `png_chunks`) that check an input and return, leaving the write
to a caller one frame up. A tool that writes more can easily have *fewer* gates with a
write in scope, because writing more is what makes you factor the writing out.

This is E22's lesson one level in. That arc's was *check the population is real before
predicting its density* — and this population **was** real and **was** counted first,
which is why P1–P15 landed. What I did not check was **what the metric's unit is**. The
population being real is not sufficient; the predicted quantity has to be a property of
the same object the instrument measures. Here the instrument's unit is a scope and my
reasoning's unit was a file.

---

## What this arc did not do

- **Did not convert the 134 ANDON asserts outside the twelve** — 132 `diagnostics/`,
  1 `verify/`, and `superseded/`'s one, which is **never** converted (E22 Ruling 4).
- **Did not unify `SystemExit` and `AssertionError`** (F4).
- **Did not act on F1 or F2** — both are routed to the ruling.
- **Did not import any of the twelve**, restructure any script into a module, run
  either Blender tool, or build a Blender harness.
- **Did not touch** P5 (`fit_background`), the `q`-verb defect, the certificate's
  domain note, the measurement MCP, or the release. **No tag, no publish.**
- **Did not write to the memory store.**

## Open for the ruling

1. **F1** — `brush_cloud_step:204` cannot fire. Remove it, move it in front of `:353`,
   or leave it as depth-in-defence against a future caller of `preflight`?
2. **F2** — two route tools create their output directory before their gate fires. Is
   an empty `makedirs` ahead of a gate acceptable, and should the dispatch's "nothing
   was written" be restated as "no artifact was written"?
3. **The 19-site Blender gap.** `bake_hero_prep` and `bake_hero_pack` have compile and
   AST coverage and no behavioural coverage at all. Is an artifacts-tier Blender smoke
   worth commissioning, or does that gap stay stated?
4. **The 41 unfired sites** — is the reason list above sufficient, or should any of
   the "reachable in principle" ones (`e13_harmonize` 139/158, `export_asset_source`
   90/95, `palette_gate` 137) be commissioned as fixtures?
5. Whether T31's pin of **134** remaining is the right instrument for handing the
   diagnostics arc its scope, given that two consecutive arcs were defeated by a scope
   number.
6. **F5** — should the fold-race note in `CLAUDE.md` / `pytest.ini` say plainly that
   the concurrent writer can be the running session itself? Writing a report during a
   suite run is the ordinary shape of an executor's last hour, and the current wording
   points only at *another* session.

---

## Appendix — commands

```
tools/facet_index.py build|verify --db <scratch>     gate 0, 19/19, four legs
python -m pytest -q                                  275 -> 370
python -m pytest -q -m "not artifacts"               362 passed, 8 deselected (as CI runs it)
tree_manifest.py write|check                         7,312 files, 3 runs, 0 changed
assert_census.py                                     57 / 12 / 132 / 1 / 1 / 191 / 15
convert.py shapes|apply|check <rev>                  57 sites, shapes measured, per-site AST
pure_move_proof.py <rev>                             whole-file AST vs the prior commit
comment_diff.py <rev>                                0 comment tokens changed
analyze.py                                           P5 0/57 · F5 37 of 57 · F4 10 sites
probe_fire.py                                        16 of 57 fire in all three modes
shadow_check.py                                      F1, over every block shape
what_is_left.py                                      F2, exactly what the two leave behind
smoke.py                                             py_compile 12/12, --help 30/30
```

Instruments live in the session scratchpad, not the repo: they are one-shot checks that
need the pre-conversion tree, and the repo's rule is that **re-runnable** anchors get
ported into the harness. The re-runnable half is T31.
