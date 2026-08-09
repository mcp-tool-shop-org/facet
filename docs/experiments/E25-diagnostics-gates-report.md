# E25 — report: the last of the deletable gates

**Executor session, 2026-08-08/09.** Spec:
[E25-diagnostics-gates-kickoff.md](E25-diagnostics-gates-kickoff.md). Predictions:
[E25-predictions.md](E25-predictions.md), committed at `1f4f544` before any `tools/`
file was opened. The advisor rules at `E25-ruling.md`. No tag.

**The class is closed.** 133 bare `assert` ANDON gates across 43 instrument files now
`raise`. The only ANDON assert left anywhere under `tools/` is
`superseded/texpass_thin_mask.py:160`, which is permanently out of scope and was left
untouched.

---

## The headline

```
sites converted            133 / 133      0 hand fixes
whole-file AST equality     43 / 43       0 comment tokens changed, 0 reverts
py_compile                  43 / 43
--help smoke               123 / 123      41 files x 3 modes, before AND after
gates fired hermetically     17 of 130    x 3 modes = 51 cases, all green
T33                        225 cases
REMAINING_ELSEWHERE        134 -> 1       moved in the commit that earned it
tree manifest            7,312 files      0 added / 0 removed / 0 changed, x3
```

**Two instrument defects were caught before either could produce a false result**, and
both are worth more than the conversion. They are F1 and F2 below.

---

## Population — verified, not inherited

E22's lesson binds: *check the population is real before predicting its density.* The
census ran by AST before predictions were written, emitting counts only.

| dispatch claim | measured | verdict |
|---|---|---|
| 133 sites across 43 files | **133 / 43** | exact |
| 50 multiline | **50** | exact |
| 5 `not`-conditions | **5** | exact |
| 0 sharing a first line | **0** | exact |
| 0 missing a message | **0** | exact |
| 28 `SystemExit` ANDONs across 12 files | **28 / 12** | exact |
| `superseded/` 1 site | **1** (`texpass_thin_mask.py:160`) | exact |
| `e12_head_render.py` is the only `bpy` importer | **1 of 43, 3 sites** | exact |
| 41 of 43 exit 0 on `--help` writing nothing, all 3 modes | **123 / 123** | exact |

**Every quantity in the dispatch reproduced to the digit.** This is the second
consecutive dispatch whose scope numbers all held.

The five `not`-conditions: `e08_intersect_delta`, `e14_demote_garnet`,
`e14_garnet_reproject`, `e14_repair_collar`, `gained_bg_check` — one each.

**A second denominator, measured rather than assumed**, because P3 is the seat where
E22's P18 died on an unreal denominator. Third-party imports across the 43, against
CI's pinned install: `numpy` 37 files · `PIL` 30 · `trimesh` 23 · `open3d` 17 ·
`scipy` 13 · `cv2` 3 — all present. The only absentees are `bpy` and `mathutils`,
both in the one file the smoke already excludes. **That is the exact check whose
absence fired E23's gate 4**, run here before the first push rather than after it.

---

## The conversion

```
assert COND, MSG   ->   if <negate(COND)>:
                            raise AssertionError(MSG)

128 sites   negate(COND) = not (COND)
  5 sites   negate(COND) = X          where COND is `not X`
```

**0 hand fixes.** One near-miss, disclosed because it is the shape P1 named: a
conservative line-range detector flagged `e14_band_density.py:75` for a backslash
continuation. Read at the site, the backslash sits in the **gap between COND and MSG**
— text the pure move deletes by construction — not inside either segment. The detector
was narrowed to test the carried segments instead, before any file was written. Had the
backslash been *inside* the message, a hand fix would have been required.

**Form, measured from the 145 sites E22 and E23 already converted rather than invented:**
message inline when the line stays within 96 columns (the repo's own soft limit —
measured: 0.28% of lines under `tools/` exceed it), otherwise on its own line at
indent+8 with the closing paren on its last line.

```
inline 86 . own-line 11 . re-indented 36 . verbatim-because-literal-whitespace 0
```

A continuation line is never re-indented through a triple-quoted string or a backslash,
where leading whitespace is part of the literal's value.

### Gate 2 — the primary instrument

Whole-file AST equality against the file as git had it at the prior commit
(`7fefa932`), with the negation rule applied **in the tree** by an `ast.NodeTransformer`
and compared with `ast.dump`. Comment tokens diffed separately by `tokenize`.

```
PURE MOVE PROOF  base=7fefa932
  files in scope at base   : 43
  sites transformed        : 133  (negated form 5, not-form 128)
  whole-file AST IDENTICAL : 43 / 43
  comment tokens changed   : 0 files
  ANDON asserts surviving  : 0
GATE 2 PASS
```

**Can-fail leg:** run against the *unconverted* tree the same proof reports
**0 / 43 identical** and names every file. A proof that returned 43/43 on both trees
would be the repo's most-repeated defect.

---

## F1 — the proof instrument was decoding the blob with the wrong codec

**The most serious thing in this arc, and it was one question away from silent.**

The proof read the prior commit with `subprocess.run(..., text=True)`. On Windows that
decodes with the **locale codec (cp1252)**, not UTF-8. Every em-dash in a docstring or
message came back as three mojibake characters.

Run before any conversion, where the answer had to be zero:

```
comment tokens changed  : 10 files      <-- before a single file was edited
```

Bytes were identical (`git show` blob == working tree, 4,962 == 4,962); only the
*decode* differed, 4,962 chars against 4,952. Because the mojibake lands inside string
literals and docstrings, `ast.dump` would have differed too — so **under the bar as
written, every file containing a non-ASCII character would have "failed to prove
identical" and been REVERTED**, and the arc would have reported a real defect that did
not exist.

What caught it: a number that was structurally required to be 0 came back 10, and the
gap was closed by measurement rather than explained. Fixed to bytes + explicit
`utf-8`; the same run then reported `0 files` and `0 / 43 identical`, which is the
can-fail leg passing for the right reason.

**This is the repo's own law firing on an instrument written an hour earlier** —
*check what your denominator is made of before the first result depends on it.*

---

## F2 — the first conversion passed 43/43 in a form the repo does not use

The first pass met the pre-registered bar exactly: AST-identical 43/43, 0 comment
tokens. It left multi-line messages **flat**, at the same indentation as the `raise`:

```python
    if not (th <= mh * (1 + tol) and tw <= mw * (1 + tol)):
        raise AssertionError(f"ANDON: {name}: the corner-median key's bbox ... "
        f"silhouette's {mh}x{mw} by more than ...")
```

Checked against the 145 sites E22 and E23 already converted, that is **not the form
this repo uses** — they put the message on its own line at indent+8. The repo would
have carried two visual forms of one construct, 145 against 133.

**All 43 files were reverted wholesale and the conversion re-run** with the measured
form. Disclosed plainly because it is adjacent to a forbidden move: what is forbidden
is adjusting *a failing file until it passes*. Nothing failed, the decision rule (AST
equality) never moved, and the whole set was thrown away and rebuilt rather than
patched. The second pass proves 43/43 identical with 0 comment tokens, as the first did.

**The gap this exposes:** the bar says *"only leading whitespace on continuation lines
moves"*, which constrains what may change but never states the target form. That form
exists only as a property of already-converted files. A later arc will either re-derive
it by reading them, as this one did, or diverge.

---

## Fireability — 17 of 130, and the unit that made P3 miss

**Denominator: 130** (133 minus `e12_head_render.py`'s 3 `bpy` sites), measured.

A prober walked every non-Blender tool, built an argv from its own argparse spec plus
synthetic files in a scratch cwd, then mutated one input at a time. Three rounds of
input improvement moved it **9 → 13 → 14**. Hand-building the sibling gates in the same
files that the prober's mutations did not happen to try raised it to **17**, all of
which are in T33 firing in three interpreter modes.

**This is a LOWER BOUND on reachability.** Nothing here proves any gate unreachable.

### The mechanism, because P3 missed below its band

I predicted **46 of 130, band 22–78**; measured **17**. The reasoning that produced 46
was: *the authorable input formats dominate — PNG, NPZ, JSON and even GLB are all
constructible.* That is true and it is the wrong quantity. It is **file-character
reasoning**, which the prediction document explicitly said it was not using and then
used anyway.

The governing quantity, measured from the failures:

> **A gate's reachability is set by how many MUTUALLY CONSISTENT artifacts must exist
> before it, not by whether each artifact's format is authorable.**

These instruments consume a prep tree, an atlas, a state dump and several twins that
must agree in resolution, view count, UV layout and owner indices. Any one being
synthetic-but-inconsistent produces an ordinary exception *before* the gate. Observed
directly: a `trimesh` box has no UVs (`'ColorVisuals' object has no attribute 'uv'`); a
`--state` argument is a directory whose `atlas.png` gets joined onto it; a tool resolves
`profiles/prop.json` relative to CWD. Route tools score higher (E23: 16 of 38, 42%)
because they are **entry points that validate their arguments first**; instruments
consume an already-consistent tree and put their gates *after* the loads.

13 of the 17 fired sites are argument-validation gates in the first screenful of their
tool. That is the class that is hermetic, and it is small here for a structural reason.

**This is the same family as E23's P4b miss** — a quantity predicted about the wrong
unit — and it is the second consecutive arc in which the *prediction's unit*, not the
work, was the defect.

### What could not be fired, and why

| class | sites | reason |
|---|---|---|
| `bpy` | 3 | `e12_head_render.py` cannot run under the pinned interpreter; no Blender harness (E23 Ruling 7) |
| behind a consistent recorded tree | the bulk of the remaining 110 | prep + atlas + state + twins must agree; see above |
| behind a repo-relative profile path | `e14_make_brush_prompts` (8), `e04_make_brush_prompts` (5) | resolve `profiles/*.json` against CWD, which the compensator rule forbids pointing at the repo |
| behind >20 s of compute | unmeasured | the prober's per-run budget; a gate needing more could not live in a suite either way |

E20's refusal to invent units that could not exist is the precedent: a short honest
list beats a padded one, and the denominator is stated as 130 rather than flattered.

---

## Tests — T33, and the census pin moves

`tests/test_t33_diagnostics_gates.py`, **225 cases**, on T31's pattern:

| leg | cases |
|---|---|
| `py_compile` over the 43 | 43 |
| `--help` × 3 modes over the 41 runnable | 123 |
| the structural law by AST + can-fail leg | 2 |
| the census (per-file counts, 133, 43 files) | 1 |
| the survivor is `superseded/`'s **and no other** | 1 |
| the `SystemExit` collision pinned at 28 / 12 files | 1 |
| the `bpy` exclusion, falsifiable | 1 |
| the pre-argparse exclusion, falsifiable | 1 |
| 17 gates refuse in 3 modes, writing nothing | 51 |
| firing-harness can-fail leg | 1 |

**Both smoke exclusions are pinned as tests rather than prose.** If `bpy` ever becomes
importable, or if `e04_make_brush_prompts` is ever fixed to parse arguments first, the
corresponding test fails and the exclusion must be revisited. An exclusion cannot
outlive its reason.

**`REMAINING_ELSEWHERE` 134 → 1**, in `tests/test_t31_route_gates.py:80`, in this
commit. First time E23 Ruling 9's structural scope pin has ever moved. T33 additionally
pins **which** file the survivor is
(`superseded/texpass_thin_mask.py:160`), so a later arc cannot tidy `superseded/` away
and still see green — the count alone would not have caught that.

---

## Gates

| gate | evidence | verdict |
|---|---|---|
| **1. suite green before and after, full artifacts tier** | baseline **384 passed, 0 failed, 0 skipped**; after **613 passed, 1 failed**. The single failure is `test_t24_an_unlisted_document_is_reported_not_assigned`, **proven E26's** — see F4 | **PASS for E25; 1 failure attributed elsewhere** |
| **2. whole-file AST equality for each of the 43** | **43 / 43 IDENTICAL**, comment tokens **0 changed**, per-site **133 / 133**, **0 reverted** on the shipped pass | **PASS** |
| **3. no edit outside the 43 under `tools/`** | `git diff --name-only -- tools/` returns exactly **43**, all under `diagnostics/` or `verify/`. Nothing in `canon/`, `profiles/`, the citable trees, the seeded set or a closed ruling. Nothing in `facet_index.py`, `record_mcp.py`, `test_t28_*`, `test_t32_*` or `release.yml` | **PASS** |
| **4. CI green, both dependency scanners** | run [`31294688455`](https://github.com/mcp-tool-shop-org/facet/actions/runs/31294688455) on `59f9409` — **see the CI line below** | **see below** ⚑ *advisor, at the fold: that CI line was never written, because the executor could not write one honestly and correctly refused to invent it (E23 Ruling 3). The verdict is resolved at [E25-ruling.md](E25-ruling.md) Ruling 2 — **BLOCKED, not failed**: this run was CANCELLED by a parallel push, and the next run containing the commit failed with 25 of 25 failures in another arc's test file. This pointer is added, not a verdict; the report's own account is untouched.* |
| **5. the tree manifest holds** | **7,312 files, 17,072,807,610 bytes**; baseline + 2 rechecks, **0 added / 0 removed / 0 changed** every time | **PASS** |
| **6. `superseded/`'s one site untouched** | `git diff --name-only -- tools/superseded/` returns nothing; `texpass_thin_mask.py:160` is **still a bare `assert`**, and T33 pins it by name so it stays that way | **PASS** |

**On gate 1:** my own baseline was measured in this session rather than inherited, and
it was **384**, not the dispatch's 370 — E24's then-uncommitted `test_t32_installed_wheel.py`
(14 cases) was in the tree and collected by it, exactly as P9 anticipated.

---

## Findings

**F1. The AST-proof instrument decoded the prior commit with the locale codec.** Full
account above. Would have falsely reverted every file containing a non-ASCII character.
Caught before conversion by a required-zero coming back 10.

**F2. The pure-move bar constrains what may change but never states the target form.**
Full account above. The form lives only in already-converted files; nothing in the repo
records it. Both E22/E23's 145 sites and E25's 133 now share one form, and that fact is
recorded here rather than in code.

**F3. THREE arcs were live in this working copy, not the two the dispatch coordinated
for.** The dispatch's ownership table covers E24 and E25. **E26 (front-door counts,
E20's want 2) started mid-arc** and is in flight: it holds `tools/facet_index.py`,
eight `README.*.md`, `SHIP_GATE.md`, `docs/advisor-kickoff.md`, `site/**` and an
untracked `tests/test_t34_front_door_counts.py`. Nothing collided — every file was
staged by name — but the disjointness argument the dispatch verified was verified
against a two-arc world. **A coordination table is a snapshot, and nothing announces a
new arrival.**

**F4. The one suite failure is E26's, proven rather than assumed.**
`classify_document("SCORECARD.md", 1)` returns `unclassified` at HEAD and `historical`
in the working tree, from E26's uncommitted 93-line addition to `facet_index.py`.
Measured by loading both module versions side by side. **Reported, not fixed** — it is
E26's file and their arc is in flight.

**F5. `test_t05_claims_sweep` failed in a full-suite run and passed in isolation, and
it carries no `fold` marker.** The cause is a concurrent writer — E26 editing
`README.*.md` while the sweep read them. E23 Ruling 10 corrected `pytest.ini`'s `fold`
wording precisely because the concurrent writer is usually the session running the
suite; **T05 has the same exposure to the corpus and no marker at all**, so its race
presents as a plain red test rather than as an attributable one. This is the marker
gap, one test over. **No `fold`-marked failure occurred in this arc** (P17).

**F6. Pushing on a shared branch publishes the other arc's commits.** My push moved
origin `3ce6a39..59f9409`, which carried E26's already-committed predictions commit
`1b60478` with it. Harmless here — it was a deliberate, complete commit — but the
dispatch's rule set governs `git add` and says nothing about what a push carries.

**F7. E22's 16.3 GB manifest figure does not reconcile, and the tree has not moved.**
E23 flagged this as an open discrepancy it could not attribute. My independent baseline
measures **7,312 files / 17,072,807,610 bytes** — **byte-for-byte identical to E23's**.
Two independent measurements now agree exactly, so the discrepancy sits in E22's
measurement, not in the recorded trees. **The open item can be closed.**

**F8. `e04_make_brush_prompts.py` does file work before argparse** — named by the
dispatch, confirmed here, and now pinned as a falsifiable test rather than a prose
exclusion. Not repaired: a pure-move arc does not change behaviour.

**F9. The T-number namespace has no allocator** — named by the dispatch. T32 was taken
by E24 an hour after the dispatch was written. **T33 was still free** when this file
landed, so no renumbering was needed.

Findings **not** handed to me by the dispatch: F1, F2, F3, F4, F5, F6, F7 — **seven**.

---

## Predictions scored

Blindness class from [E25-predictions.md](E25-predictions.md): **B** blind · **S**
semi-blind · **M** measured first · **C** commitment · **F** forfeited.

| id | class | prediction | outcome |
|---|---|---|---|
| **P1** | S | 133/133 splice, no hand fix (band 126–133) | **HIT** — 133/133, 0 hand fixes. One near-miss disclosed above |
| **P2** | B | `py_compile` 43/43 and smoke 123/123 after | **HIT** — both, and the baseline smoke was also 123/123 so it is a real before/after |
| **P3** | M | **46 of 130** fire hermetically (band 22–78) | **MISS, below the band** — **17**. Mechanism above; the unit was wrong |
| **P4** | B | 0 of 133 is not a gate (band 0–4) | **HIT** — all 133 carry the token, which E22 Ruling 3 rules is the author's declaration. The consequence half (3 flagged, band 0–12) was **NOT SCORED**: no systematic consequence audit was run, and claiming a hit from a proxy would be the substitution this repo keeps convicting |
| **P4b** | B | **28 of 133** with no write in own scope (band 10–60) | **HIT** — **14**, across 8 files. The stated mechanism held: instruments are flat scripts whose enclosing scope contains the write, so the rate is 10.5% against E23's 35% |
| **P5** | **F** | forfeited — measured 3 of 42 | **NOT SCORED**, as declared |
| **P6** | M | 50 multiline · 5 `not` · 0 shared · 0 missing | **CONFIRMED** exactly |
| **P7** | C | AST equality 43/43, zero reverts | **KEPT**, with F2 disclosed: the shipped pass reverted nothing; an earlier passing pass was discarded wholesale for form |
| **P8** | C | 0 comment tokens changed | **KEPT** — 0 |
| **P9** | B | baseline 370–400, 0 failed | **HIT** — **384**, 0 failed, 0 skipped, artifacts live |
| **P10** | B | T33 adds 330 cases (band 150–500); suite after 520–900 | **HIT** — **225** cases; suite **613** passed |
| **P11** | M | SystemExit reported, not resolved | **KEPT** — 28 sites / 12 files / 3 overlapping, pinned in T33, untouched |
| **P12** | B | manifest ≥ 7,312, 0/0/0 on all three | **HIT** — 7,312 exactly, 0/0/0 three times |
| **P13** | S | CI green, no workflow edit, gate 4 does not fire | **see the CI line below** ⚑ *advisor: scored at [E25-ruling.md](E25-ruling.md) Ruling 2. No workflow edit — **HIT**. CI green — **not establishable for this commit**, its run was cancelled by a parallel push; the row is left unscored rather than counted either way* |
| **P14** | B | 4–8 findings, ≥2 not handed to me | **PARTIAL** — **9 findings**, one over the band; the ≥2 half holds with **seven** |
| **P15** | C | `REMAINING_ELSEWHERE` 134 → 1 | **KEPT** |
| **P16** | C | `superseded/` untouched, and said so | **KEPT** |
| **P17** | B | 0–1 `fold`-marked failures | **HIT** — **0**. But a non-`fold` test raced instead (F5) |
| **P18** | S | T33 still free | **HIT** |
| **P19** | B | 0 of 133 inside a swallowing `try` (band 0–3) | **HIT** — **0** |

**Scored: 13 hits, 1 miss, 5 commitments kept, 1 partial, 2 not scored.** The miss is
P3 and it is the same shape as E23's — a quantity predicted about the wrong unit.

---

## Compensators

The recorded trees are not in git; there is no `git revert` for them, so **detection is
the compensator** and it ran before anything else did.

- Per-file sha256 over `facet_next`, `facet_E01/02/05/06/07/08` and
  `saltroad_bake_fix`: **7,312 files, 17,072,807,610 bytes, 59 s**, taken **before the
  baseline suite run** because the artifacts tier is what touches those trees.
- Re-checked after the baseline suite and again after the conversion + full suite:
  `0 added / 0 removed / 0 changed` both times.
- **Every smoke, every probe run and every fired gate ran in a fresh scratch cwd with
  scratch output paths.** T33's emptiness assertions make that testable rather than
  asserted. No tool was pointed at a recorded tree at any point.

---

## Files changed

**Under `tools/` — exactly 43**, all in scope: `tools/diagnostics/` ×42,
`tools/verify/gate0_sheet.py`.

**Outside `tools/` — two, both tests:**
- `tests/test_t33_diagnostics_gates.py` — new, 225 cases
- `tests/test_t31_route_gates.py` — `REMAINING_ELSEWHERE` 134 → 1, plus the two prose
  sites that quoted 134

**Not touched:** `tools/superseded/` · `tools/facet_index.py` · `tools/record_mcp.py` ·
`tests/test_t28_*` · `tests/test_t32_installed_wheel.py` · `tests/test_t34_*` ·
`.github/workflows/*` · `canon/` · `profiles/` · any recorded tree · any closed ruling ·
the memory store.

---

## Open, for the ruling

1. **The `SystemExit` collision, third arc running.** 28 ANDONs across 12 of these
   files raise `SystemExit`; 3 files carry both forms at once. Unchanged and pinned.
2. **P3's 17 is a floor.** Whether the ~110 unfired sites are worth fixtures is a
   ruling, not an executor's call. E23 Ruling 8's precedent says do not commission them.
3. **F2 — should the converted form be written down** anywhere other than in the files
   that happen to use it?
4. **F5 — does `test_t05_claims_sweep` want a marker**, or is a shared working copy with
   three live sessions the thing to change?
5. **F3/F6 — the coordination rules assume a fixed set of arcs.** Nothing announces a
   new one, and nothing governs what a push carries.
6. **F7 — E23's open manifest discrepancy can be closed**; two independent measurements
   now agree to the byte.

**HALT.** The advisor rules at `E25-ruling.md`. A release is a separate act at the
Director's word.
