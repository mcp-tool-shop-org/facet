# E28 — task 3. `texel_provenance`'s largest connected component, in the instrument.

**Executor, 2026-08-09, the third seat of the arc.** Dispatch:
[E28-instrument-census-kickoff.md](E28-instrument-census-kickoff.md) Task 3. Contract:
[E27 Ruling 7](E27-ruling.md) and [E28 Ruling 17](E28-ruling.md), which named this the arc's
last open item. Predictions:
[E28-task3-predictions.md](E28-task3-predictions.md) (`0fe123f`, committed before the
instrument was touched and before the population was enumerated).

**Task 3 is done.** The instrument reports each class's largest connected component beside
its total; the wrapper's gap-text is gone in the same commit that filled it; the change is
insert-only on stdout and byte-identical on both file outputs.

---

## Gates

| gate | state | evidence |
|---|---|---|
| 4 — allowed diff under `tools/` | **HELD** | `git diff --name-status -- tools/` is exactly `M tools/diagnostics/texel_provenance.py` and `M tools/measure_mcp.py`. `instrument_census.py` is **not** modified — the census is re-*run*, and its outputs live under `docs/`, outside this gate |
| 5 — CI | **NOT YET RUN** — no identifier is written here ([E23](E23-ruling.md)'s fabricated-citation law). The push is the advisor's |
| 6 — no recorded tree modified | **HELD** | 7,312 files / 17,072,807,610 bytes; **0 added / 0 removed / 0 changed**, baseline and close, across 18 instrument runs against the recorded trees plus the artifacts tier of four suite runs (two complete, two stopped early). Scope corrected — see F14 |
| the pure-move condition | **HELD** | insert-only on 9 of 9 recorded triples plus the fixture; `--out-json` and `claim.npy` byte-identical |

**Suite: 797 passed / 493.88 s / exit 0**, measured on a `git archive HEAD` of exactly the
tree being committed with this seat's four files copied in — **not** in the shared working
copy, where a live sibling seat's eight untracked test files are collected and would inflate
every count this commit pins (F19). 790 → 797 is T47's seven cases.

⚠ **One methodological catch, recorded because it would waste the next seat's hour.** The
archive is not a git repository, so `T06`'s two legs fail there with
`fatal: not a git repository` — they shell out to `git ls-files`. That is the *method*
failing, not the tree: both pass in the working copy, and after `git init && git add -A` in
the archive the run is **797 / 797 / 0 failed** with no exclusion and no deselection. The
number above is that run. An archive used as a test tree needs a `.git` before the count
means anything.

---

## What landed

**In the instrument** — `tools/diagnostics/texel_provenance.py`, **+47 / −5, net +42** (238 →
280 lines):

- The class list is hoisted to a name (`CLASSES`) and the existing census loop iterates it
  instead of an inline expression. The expression itself is **moved verbatim**, which is why
  the census block's output is provably untouched rather than merely believed to be.
- **The five removed lines are those two relocations and nothing else**: the `scipy.ndimage`
  import, widened to two lines to bring in `label`, and the four-line inline class-list
  expression that is now `CLASSES`. Said precisely because "pure move" is the claim under
  test, and a diff that removes five lines while claiming to remove none would be the
  report's own defect.
- A largest-connected-component block prints after the census and **before the `--render`
  early exit**, so it rides the write-free path — the one the server wraps.
- **4-connectivity, atlas space, over `class AND valid`** — the same mask the totals use, or
  the pair would describe two different sets.
- The caveat rides the output, the docstring and the payload: **atlas adjacency is not
  surface adjacency**, so UV seams split one surface region into several atlas components and
  each figure is a **LOWER BOUND** on that class's largest surface-contiguous run. A large
  value means one region for certain; a small one does not rule it out. Surface-connected
  components are a different and more expensive measurement, and neither the instrument nor
  the wrapper computes one.

**In the wrapper** — `tools/measure_mcp.py`:

- Three pinned patterns parse the block into `census.twins_largest_component`,
  `census.dilation_largest_component` and `largest_component` inside each stroke row. **No
  arithmetic** — gate 3 holds; the server reads numbers the instrument printed.
- A second `INSTRUMENT_FAILED` refusal fires if the census parses but its component block
  does not: the two are printed together, so a half-parse means the print shape moved.
- The gap note is **deleted**, replaced by the atlas-adjacency caveat and the
  no-surface-components disclaimer.
- `ratios` gains `*_largest_component` naming **the class's own total** as the denominator,
  not `valid_texels` — one region versus speckle is a within-class question.
- `MEASURE_VERSION` 0.3.0 → **0.4.0**. The two earlier bumps marked the surface while no
  serving tool's payload changed; **this one is a serving tool's payload changing.** It is
  additive — every existing key keeps its name and its value — but a caller that pinned the
  shape is entitled to see the version move, which is what the envelope is for.

---

## The pure-move proof

Whole-stream byte identity is impossible when the task is to add an output, and naming it as
the bar would have been a pass condition the experiment is built to break. The condition was
registered before any measurement:

> **INSERT-ONLY on stdout** — every pre-change line present, byte-identical, in order, with
> the new block the only addition — **and BYTE-IDENTICAL on `--out-json`.**

Checked with `difflib` opcodes accepting only `equal` and `insert`; a `replace` or `delete` is
a violation. That is a check rather than a filter that could hide a modification by
construction — a line-marker filter would have been the latter.

| leg | result |
|---|---|
| 9 runnable recorded triples, pre-change byte copy vs HEAD, identical arguments | **INSERT-ONLY on 9 of 9**, +15 lines each, 0 violations, rc 0/0 |
| the fixture's `--render` path (the only path that emits JSON) | **INSERT-ONLY**, +8 lines |
| `--out-json` bytes | **IDENTICAL** — `b28191ad…cbcaa4` both sides |
| `claim.npy` bytes | **IDENTICAL** — `d1fb327e…0e55da` both sides |
| return codes and harness arguments | unmoved on every subject |

E28 2a's trap was designed in: both versions receive the **same** `--state` and `--out-json`,
because that harness produced a false `DIFFERS` from a tool printing its own argument back.

### And the anchors the closed-ruling law asks for

CLAUDE.md's law on editing a cited instrument is *prove the edit non-perturbing, **or** carry
an anchor reproducing the cited number, in the commit that makes the edit.* This commit
carries both halves, and the anchors were not sought — they fell out of the enumeration:

| cited number | where it is cited | measured at HEAD |
|---|---|---|
| dilated texel count **2,551,893** | CLAUDE.md, *"the honest unit was dilated texel count (2,551,893 → 813,773, a 68% fall)"* | **2,551,893** — E05-U1, DILATION total |
| dilated texel count **813,773** | same sentence, the after-state | **813,773** — E06-C1, DILATION total |

Both endpoints of that pair reproduce to the digit from the tool at HEAD. `facet_E06/C1/prep`
is also the one prep the record names in a `--prep` invocation anywhere in `docs/`, so that
pairing is the record's own, not this seat's guess.

---

## The population, and where the prediction broke

P17 asked how many recorded subjects exist. Measured clause by clause first, as the
conjunction law requires:

| clause | predicted | measured |
|---|---:|---:|
| a — a complete prep (5 files) | 6 | **11** |
| b — a stage-1 atlas with **both** siblings | 2 | **48** |
| c — a state with >=1 complete job | 2 | **19** |
| **join — runnable (prep, state, stage1) triples** | **2** | **9**, over 4 distinct states |

**The clause I named in advance as rarest was the most abundant by 24x.** The reasoning —
"only an arc that ran stage 1 and then brushed leaves a styled mask beside an atlas" — was
true and useless: every *variant* of such an arc saves one, so E08 alone contributes 14
atlases. The join is not governed by any clause count here; it is governed by a constraint I
never enumerated at all — **whether a prep exists in the same arc as the state**.

The join rule, stated so it can be argued with: adjacency first (a prep from one arc is not a
subject with another arc's state), then the instrument's own shape preconditions. Order is the
record's spiral (`docs/experiments/E14-brush-prompts.json`'s `_order`) applied by yaw so each
state's actual elevation suffixes are preserved. **Only E06-C1 is claimed as a historically
recorded pairing** (the `--prep` citation plus the reproduced 813,773); the other eight are
runnable triples, which is what the proof needs and all it claims.

---

## Findings for the ruling

**F14 — the inherited manifest figure describes a tree 18x smaller than the one the dispatch
names, and both numbers are right about different objects.** `E:\AI\training` holds
**131,970 files / 122,439,162,519 bytes** — python environments (`chatterbox-env`,
`unsloth-env`, `sd-scripts`), LoRA datasets, and the **live VRAM watchdog's own log and
heartbeat**, which are written continuously. The inherited **7,312 files /
17,072,807,610 bytes** is `E:\AI\training\{facet_*, saltroad_bake_fix}`, and **both figures
reproduce to the digit** for that subset. The conflation has a cause worth recording: the
server's `DEFAULT_ASSETS` *is* `E:\AI\training`, so the sealed **root** (what
`SEALED_TREE` refuses under) and the manifested **trees** (what 0/0/0 is asserted about) are
two different objects wearing one path. A future seat that manifests the literal root will
get a non-zero `changed` from the watchdog and read it as a violation.

**F15 — the repo's most-cited brush state cannot be replayed from the record.**
`facet_E08\ARMB\state` holds 8 complete jobs, and **`facet_E08` contains no prep file at
all** — no `meta.json`, no `mask.npy`, no `prep_uv.glb` — nor does `facet_E02`. Measured, not
assumed: a walk for any of the five prep members under either arc returns nothing. And no
`--prep` invocation naming an E08 prep exists anywhere in `docs/`; the only one the corpus
carries is `facet_E06/C1/prep`. E08/ARMB is therefore excluded from the proof set with its
reason, rather than paired by guess.

**F16 — the declared 4-connectivity was unfalsifiable until a falsification run said so.**
Six legs were written and passing. Patching `label(m2)` to 8-connectivity left **all six
green**: the fixture's two DILATION bands do not touch even diagonally, and the stripe
variant's columns sit two apart. The instrument declared 4-connectivity in its print block,
its docstring **and** the served payload, and nothing could catch that declaration going
false. A seventh leg — a main-diagonal styled mask, 32 texels that are pairwise diagonal
neighbours and nothing else — now pins it: **1 under 4-connectivity, 32 under 8**, at an
identical total. It passes at HEAD and fires under the patch. Found by running a
falsification, not by reading one.

**F17 — E10 Ruling 5's queued repair of this instrument is still queued, and every number in
the new block inherits the defect.** That ruling measured `texel_provenance.py`'s replay as
predating E08 Amendment 32 and **over-claiming +358 commits** on the asset it examined
(+6/+118/+148/+25/+5/+56, the signature of a missing `fm_e & hit` intersect), and queued the
fix "for the next session that needs the tool." This is that session, and **I did not run
it**: repairing the replay changes existing numbers, which is the exact inverse of the
pure-move discipline task 3 was commissioned under. The consequence is worth stating plainly
rather than leaving implicit — the per-stroke totals are slightly too large and DILATION
slightly too small, so the components I added are measured on a marginally wrong partition.
**I did not add that caveat to the payload either**: it is a property of the whole census,
which has served since E27 without naming it, and attaching it only beside the new number
would misattribute the defect. Whether the served notes should carry it is a ruling, not an
executor's edit.

**F18 — the fixture's `--render` path had never been executed by anything.** T38 passes
`render=` only to assert the `SEALED_TREE` refusal, which fires *before* the instrument runs,
so the JSON-emitting half of the tool was untested at the fixture. Running it needs
`--res 32`; at the default 1024 it dies on `operands could not be broadcast together with
shapes (32,32) (1024,1024)`, because the head camera builds an R x R ray grid and the fixture's
stand-in render is 32 x 32. That is the instrument behaving as documented, not a defect — but
the JSON byte-identity leg of this proof is the first time that code path has run here.

**F19 — a live sibling seat's untracked files perturb the census, and the census was emitted
around them.** E30 is writing `tests/test_t50_*` through `test_t57_*` into this working copy
(three when this seat first looked, eight an hour later). They are untracked, and they move
axis E's `anchored_in` lists on rows this seat does not own — `e08_ceiling.py`,
`e12_elevated.py`, `anchor_compare.py`. Committing that census would have published a claim
that **cannot reproduce from my own commit**, because those files are not in it. Measured
rather than reasoned about: emitted in place, `anchored_in` moved on **4 rows**; emitted from
a `git archive HEAD` of exactly the tree being committed with my four files copied in, it
moves on **1** — `texel_provenance.py`, gaining T47, which is the only movement this seat
owns. The archive emission is the committed one. E30's *documents* are already committed and
do move axis D legitimately (see P22).

**And the archive is why the front-door bump is honest too.** The collector reports
**797 / 768 / 29** (full / hermetic / gap) for my tree — +7, exactly T47's cases — measured
in the archive, not in the shared copy where E30's eight untracked files would have inflated
it. T34's fifteen pinned sites and all eight READMEs' digit legs are bumped **in this
commit**, which is the property working rather than a chore: `SHIP_GATE.md`'s lineage gains
`→ 797`, `docs/advisor-kickoff.md`'s two lines move, and the seven translations carry the
digits. ⚠ **This number is shared with the live E30 seat.** When their tests land the count
moves again and every one of these surfaces moves with it; the pin makes that mechanical, not
optional. `docs/experiments/README.md` was not touched — it is the advisor's this arc.

---

## The census, re-emitted under Ruling 3's entry rule

`texel_provenance.py` is a counted file, so the census re-runs in this commit. It is the same
`--committed` invocation; `tools/instrument_census.py` is **not** edited.

| what moved | rows | why |
|---|---:|---|
| `lines` | 1 | `texel_provenance.py` 238 → 280, the +42 this change adds |
| `anchored_in` | 1 | `texel_provenance.py` gains `tests/test_t47_measure_texel_component.py` |
| `cited_count` (**the headline**) | 2 | `anchor_compare.py` 1 → 3, `texel_provenance.py` 11 → 12 — **not this seat's documents**; see P22 |
| `cited_count_raw` | 10 | this arc's papers ride in the raw reading by design, so the contamination stays visible |
| `corpus_files` / `…before_self_exclusion` / `test_files` | — | 265 → 267 / 272 → 277 / 48 → **49** |
| the axis-A, axis-B, axis-C, axis-F and axis-G readings for every row | **0** | no flag added, no subject literal added, docstring line 1 untouched, no guard added |

**Idempotency, checked rather than assumed** (the arc's own law — *one clean check is not
clearance*): emitted twice into the same tree with the report present in the corpus, the two
JSON files are **byte-identical**. `anchored` (the axis-E boolean) moved on **0** rows, and
the population pin is untouched at 99 + 9.

---

## Predictions, scored

| # | predicted | measured | |
|---|---|---|---|
| **P17** | 2 subjects, band 1–5 | **9** | **MISS above band**; clause analysis above |
| **P18** | pure-move HOLDS | **HELD** | insert-only 9/9 + fixture; both file outputs byte-identical |
| **P19a** | LCC(TWINS) 512 | **512** | HIT exact |
| **P19b** | LCC(DILATION) 160, band 120–160 | **80** | **MISS below band** |
| **P19c** | LCC(BRUSH s1) 352, band 300–352 | **352** | HIT exact |
| **P20** | separation 16x, band >=8x | **16x** (512 vs 32) | HIT exact |
| **P21** | 6 collected cases, band 4–10 | **7** | band HIT, point +1 — see below |
| **P22** | 0 rows move on headline `cited_count` | **2** | **MISS** |
| **P23** | 0 rows move on axis-E `anchored` | **0** | HIT |
| **P24** | LCC(DILATION)/class <5%, band 0.5–20% | **0.8%** | HIT |

**P19b is the useful miss.** I reasoned that the unclaimed set is a rim and that "a rim is
connected". It is **two disjoint bands of 80**, so the fixture's DILATION is the one class
whose total and component disagree — which is what makes the parse-independence leg able to
fail at all. The wrong prediction produced the better fixture.

**P21 moved because of F16, and it moved against me.** Six was the specified set and six was
what I wrote; the seventh leg exists because a falsification run showed the connectivity
declaration was unpinnable. Disclosed rather than quietly re-scored: the addition came after
seeing a result, and it makes my own point estimate worse.

**P22 is a new shape of this repo's oldest failure and is worth the ruling's attention.** I
predicted **0 rows** would move on the headline axis-D count, reasoning that Ruling 7's
`E28-` exclusion is permanent and covers both documents I add. **That reasoning is correct
and the prediction was still wrong.** `cited_count` moved on two rows — `anchor_compare.py`
1 → 3 and `texel_provenance.py` 11 → 12 — because the advisor's
`docs/experiments/E30-polish-anchor-gates-kickoff.md` is committed, is not `E28-` prefixed,
and cites both. **I predicted a property of my own contribution and the instrument measures a
property of the tree.** The unit was real, the population was real, every member was real —
and the quantity was not mine alone to move. Seventh consecutive arc on this family, and the
first where the miss came from a *co-tenant* rather than from a denominator.

**P24, the number the task exists to produce.** Across the 9 subjects, DILATION's largest
component runs **0.6% – 5.4%** of its class: the class is seam-rim dominated, as predicted.
The counterpart is what the law was for — the SaltRoad hero subjects carry a **single
43,000-texel unpainted region** inside an 800k–950k class, which a total alone cannot
distinguish from the same 43k spread over ten thousand rims.

| subject | DILATION total | largest component | of class |
|---|---:|---:|---:|
| E05-U1 | 2,551,893 | 20,317 | 0.8% |
| E05-U3 | 2,548,203 | 20,321 | 0.8% |
| E06-C1 | 813,773 | 14,863 | 1.8% |
| SR-hero-partial | 788,953 | 42,896 | 5.4% |
| SR-hero-v2 | 955,098 | 43,760 | 4.6% |
| SR-hero-v3 | 867,577 | 43,613 | 5.0% |
| SR-smart-partial | 55,032 | 331 | 0.6% |
| SR-smart-v2 | 57,959 | 344 | 0.6% |
| SR-smart-v3 | 56,988 | 344 | 0.6% |

Per-stroke on E06-C1 the spread is wider — strokes 7 and 8 sit at 16.6% and 12.3% against
3.0–6.6% for strokes 1–6 — and TWINS, the largest class, is the **least** concentrated at
1.7%. Reported, not interpreted: what any of it means about an asset is the Director's.

---

## Tests

**T47** (`tests/test_t47_measure_texel_component.py`), 7 collected cases, all through the
served surface because E27 Ruling 7 put the measurement in the instrument:

- the three fixture anchors — TWINS **512 of 512**, BRUSH **352 of 352**, DILATION **80 of
  160**;
- the invariant: no component exceeds its class, and a class is non-empty exactly when its
  component is;
- **the can-fail leg** — a stripe variant holding TWINS at 512 and cutting the component to
  32, the two-thresholds law in one pair: a count-only census cannot tell those two atlases
  apart;
- **the connectivity leg** (F16) — a diagonal chain, 1 under 4-connectivity;
- parse independence, on DILATION because it is the only fixture class whose two numbers
  differ;
- the gap note gone and the caveat present;
- the ratio naming the class as its denominator.

**T38's gap-note leg moved deliberately, in the commit that filled the gap.** It asserted the
payload *named* the missing measurement; asserting a disclaimer after the measurement exists
pins a stale claim. It now asserts the pairing — no total on this surface is reported without
its component beside it — and T47 owns the values.

**Falsification runs, both against the in-tree file, both reverted from a byte copy whose
sha256 was re-read after each:**

| patch | result |
|---|---|
| A — report the class total instead of its largest component | **3 of 7 legs FIRE** — exactly the three that measure the value; the invariant, notes and ratio legs correctly stay green |
| B — 8-connectivity | **0 of 6 fired** (F16), and **1 of 7 fires** after the connectivity leg was added |

---

## Compensators, discharged

| action | state |
|---|---|
| the instrument + wrapper edits | tracked file edits; `git revert` restores both, and the pure-move proof means a revert restores insert-identical behaviour |
| the two falsification patches | reverted from a byte copy taken before the first edit; sha256 `070b1e2d…bba778` equal to the pre-edit copy after each |
| 18 instrument runs against the recorded trees | census path only — it writes nothing (T38 pins this); `--render` ran only on scratch copies; manifest 0/0/0 at the close |
| the census re-emit | derived output; re-runnable with `--committed` |
| the index DB + certificate | untouched; the advisor folds the pair |

**Two seats share this working copy.** E30's untracked tests were never staged (file-scoped
`git add` throughout, and F19 explains what that was not sufficient for on its own). Nothing
of E30's is in this commit; `docs/experiments/README.md` was not touched — it is the
advisor's this arc.

---

## Withdrawn from this seat's scope, stated plainly

- **E10 Ruling 5's A32 replay repair** (F17) — it changes existing numbers, and task 3 is a
  pure move. Still queued, now with this seat's reason for not taking it.
- **The A32 caveat in the served notes** — a ruling, not an executor's edit (F17).
- **Surface-connected components** — a different, more expensive measurement over the mesh
  graph, not what E27 Ruling 7 commissioned, and inventing it here would be the forcing
  [Ruling 10](E28-ruling.md) ruled against. Named as a limitation in the payload instead.
- **The erode/margin half of `offsurface_rate`** — open commission, unchanged.
- **The index DB and certificate**, `docs/experiments/README.md`, anything of E30's.

⛔ **Halting at the report.** The push and the ruling are the advisor's.
