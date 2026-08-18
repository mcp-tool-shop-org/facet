# E59 report — the head stays forward: enforce the clause, then probe the hardest view

**Executor seat (Sonnet), background agent. Charter:
[E59-head-forward-kickoff.md](E59-head-forward-kickoff.md). Written as-you-go, uncommitted —
the advisor commits by pathspec after review.**

This document reports measurements only. It does not judge whether any image, mesh, or
control is good — that is the Director's call. Words like verified/shipped/works/decisive/
validated/proven do not appear below in that sense.

**Ceiling: 2 generations, absolute. Stages 0 and 1 are free and both complete before any
submission. Live tally: 0/2 spent so far.**

---

## Stage 0 — the clause becomes enforceable (spend: 0). COMPLETE.

### What changed, in `tools/canon_gate.py`

Before this stage, a `legal_clause` was licensed-but-optional in every case: `licensed_phrases()`
let it occur in a prompt without tripping the reverse/unlicensed check, but nothing required
it to occur, so `canon/a1.surfaces.json`'s `stage_head_forward` clause (already declared
`"required": true` by the advisor before this seat started) had no enforcement mechanism to
bind to.

Added:
- `required_legal_clauses(doc)` — returns `[("clause:<id>", phrase), ...]` for every
  `legal_clause` with `required is True`. Checked at **every scope**, not filtered by
  `scope_ids`: a legal_clause names no surface id, so the surface-id narrowing a view/stroke
  scope uses has no honest way to exempt one, and the property a required clause expresses
  ("the head stays forward") is meant to hold at every view, not just at subject scope.
- Folded into `check_prompt()`: a missing required clause is appended to the same `missing`
  list a missing ratified occupant phrase uses, with `"surface": "clause:<id>"` — same list,
  same ANDON message shape, same `ok = False`. Also added to the `required` phrase counter.
- `_validate_router_fields()`: a `legal_clause`'s `required` key, if present, must be a bool —
  fail-closed validation consistent with the rest of the function (a string `"yes"` refuses at
  load time rather than silently defaulting).
- Unmarked clauses (no `required` key, or `required: false`) are untouched — `required_legal_clauses()`
  returns nothing for them, so they keep exactly today's licensed-but-optional behaviour. This
  adds capability and removes no coverage, per the charter's own instruction.

Fail-closed throughout: the new path `raise`s (`_andon` → `Andon`, a `ValueError` subclass),
never `assert`s, and there is no skip flag — a `required: true` clause cannot be bypassed by
any existing CLI flag (`--no-canon` refuses on any subject with surfaces at all, as before).

### Proof this is a real, can-fail check (CLAUDE.md: "a check that cannot fail is not a check")

Temporarily disabled the new `for cid, ph in required_legal_clauses(doc): ...` loop in
`check_prompt()` (a scratch copy taken first, restored after, byte-diff confirmed identical —
`E:\AI\training\facet_E59\canon_gate.py.bak_verify`), then ran `canon_gate.py --selftest`:

```
ANDON: required-clause fixture: missing required clause did not refuse naming it: {'ok': True,
'missing': [], 'unratified_missing': [], 'forbidden': [], 'unlicensed': [], 'required': 1,
'scope': {'kind': 'subject', 'id': None}}
```

Restored, re-ran `--selftest`, passed, and `diff`'d the restored file against the
pre-verification backup: **byte-identical.**

### Tests, zero new collected pytest items

**Why zero, deliberately.** `tests/test_t34_front_door_counts.py` pins the suite's collected
item count across 8 READMEs, `SHIP_GATE.md`, `site/src/site-config.ts`, and every handbook
page. A new collected test moves that count, which would require regenerating all eight
README translations in the same commit — reserved to advisor/user sessions by the studio's
translation rule, not a Sonnet kickoff session. E58 already established the precedent
(extending `test_t91_census_does_not_invent_surfaces` in place rather than adding a function);
this stage follows it for the same reason.

Two layers, both can-fail, zero new collected items:

1. **In-tool** (`tools/canon_gate.py`, new function `_selftest_required_clause`, called from
   `_selftest_router`, itself called from `selftest()` / `--selftest`): a fresh fixture
   (`legal_clauses`: `bg` unmarked, `pose` required) checks (a) the required clause stripped
   refuses, naming it, and (b) the unmarked clause stripped does **not** refuse. A third check
   confirms a malformed `required: "yes"` (string, not bool) refuses at load time. This is
   exercised on every run of the **already-collected** `test_t92_selftest_still_holds`, which
   now also asserts the printed marker `"required clause held"` is present in `--selftest`'s
   stdout.
2. **Pytest-level** (`tests/test_t92_canon_router.py`, extending
   `test_t92_declared_view_does_not_require_out_of_scope` in place — same function, not a new
   one): the SAME schema-2 synthetic fixture that test already built gained a second
   `legal_clause` (`pose`, `required: true`) alongside its existing unmarked `bg` clause, and
   two new assertions: (a) stripping `pose` refuses at `view:0` scope — a scope that already
   excludes `grip` — demonstrating the clause fires **despite** scope-narrowing being active;
   (b) stripping `bg` (unmarked) still passes.

**Verified directly, not assumed**: `pytest --collect-only -q` reports **1339** both before and
after this stage's edits (confirmed by running it as a standalone command both times, not
inferred from T34 passing). `tests/test_t34_front_door_counts.py` itself: **52/52 passed**
(its own leg 0/1 would have failed loudly had the count moved).

### The non-perturbing anchor on the shared instrument

Ran `canon_gate.py census` and `canon_gate.py resolve --subject A1` **before** touching
`tools/canon_gate.py` and again **after**, full text saved to
`E:\AI\training\facet_E59\census_BEFORE.txt` / `census_AFTER.txt`:

```
$ diff census_BEFORE.txt census_AFTER.txt
(empty — no output)

$ diff resolve_A1_BEFORE.txt resolve_A1_AFTER.txt
(empty — IDENTICAL)
```

**The entire census table is byte-identical, not only W3's and LONGSWORD's rows** — stronger
than the charter asked for. The reason is structural, not luck: `census()` calls `coverage()`
and `occupancy()`/`profile_hits`, none of which call `check_prompt()`; the required-clause
mechanic only changes what `check_prompt()` returns, and `census` never invokes it. W3's own
`legal_clauses` (5 entries: `style_bg`, `style_brush`, `style_paint`, `frame_subject`,
`frame_holding`) carry no `required` key at all (confirmed by reading the file directly,
`canon/w3.surfaces.json:412-443`), and `canon/longsword.surfaces.json` is schema 1 with **zero**
occurrences of the string `legal_clauses` in the whole file (`grep -c` = 0) — so
`required_legal_clauses()` returns `[]` for both subjects by construction, not by luck.

```
W3 row, before: W3              19       24/24      24/24       5/19 canon/w3.surfaces.json
W3 row, after:  W3              19       24/24      24/24       5/19 canon/w3.surfaces.json
LONGSWORD, before: LONGSWORD        5         5/5        5/5        4/5 canon/longsword.surfaces.json
LONGSWORD, after:  LONGSWORD        5         5/5        5/5        4/5 canon/longsword.surfaces.json
```

### A genuine, direct consequence: `profiles/a1.json`'s prompt was stale

Running the full canon-adjacent test set after the edit produced **one failure**:
`test_t91_canon_in_path.py::test_t91_census_does_not_invent_surfaces`, at
`assert a1_chk["ok"], a1_chk` → `{'ok': False, 'missing': [{'surface':
'clause:stage_head_forward', 'phrase': 'head facing straight ahead'}], ...}`.

This is not a bug in Stage 0's enforcement — it is the enforcement working, for real, on a
real production artifact. `profiles/a1.json`'s `tools.restylize_views.py.prompt` was authored
at E58 Stage D (2026-08-18), **one day before** the Director's ruling added
`stage_head_forward` to the canon. The moment the clause became enforced, that prompt stopped
covering its own subject's canon.

**Named alternatives, and why the chosen one is not "tuning a test to pass":**
- Weakening the test's assertion (dropping `a1_chk["ok"]` or accepting `False`) — refused.
  CLAUDE.md: "Narrowing a test to make a red gate green is forbidden whichever kind of gate
  fired."
- Leaving it red and reporting it as a disclosed, out-of-scope consequence (the CRLF-issue
  precedent from E58) — considered and rejected: the CRLF issue was *unrelated* to that
  session's own work; this failure is a *direct, immediate, entirely foreseeable* consequence
  of Stage 0's own stated purpose (make the clause block a prompt that lacks it) landing on a
  real subject's real profile.
- Updating the stale artifact (`profiles/a1.json`'s prompt) to include the phrase — **chosen.**
  This is the same class of edit E58 Stage D itself performed (composing the profile's prompt
  from the ratified canon), re-run because the canon grew one more required element. It
  restores a true fact the test checks for ("the profile's prompt satisfies its own subject's
  canon"), rather than loosening what the test demands.

Appended `, head facing straight ahead` to the prompt's own tail, alongside the other staging
clauses it already carries (`no weapons, no held objects, nothing crossing the body
silhouette`), and updated the field's `why`/`from` provenance to record the edit. Re-ran the
check after the edit:

```
CHECK: {"ok": true, "missing": [], "unratified_missing": [], "forbidden": [], "unlicensed": [],
"required": 17, "scope": {"kind": "subject", "id": null}}
```

`required` moved from 16 to 17 (16 ratified occupant phrases + the 1 new required clause) —
also a hardcoded pin in the same test (`assert a1_chk["required"] == 16`), updated to 17 with
the reasoning recorded inline (matching this file's own established pattern for `W3_NAMED` and
`PROFILE_DEFAULT_HITS`: a canon edit legitimately moves a downstream pinned number, and the fix
is updating the pin to the new true value with the reason recorded, not loosening the check).
`docs/experiments/E58-a1-twin-prompts.json` (the historical record of what E58 actually
**submitted**) was deliberately **not** touched — it stays a faithful record of a prior
generation that predates this ruling.

Re-ran the full canon-adjacent test set after this fix: **94/94 passed**
(`test_t87_canon_gate.py`, `test_t91_canon_in_path.py`, `test_t92_canon_router.py`,
`test_t93_canon_worksheet.py`, `test_t94_fail_closed.py`, `test_t95_e55_prompt_elements.py`,
`test_t96_gen_record.py`, `test_t97_canon_bind.py`).

### Full hermetic suite — 2 failures, both root-caused, neither caused by this stage

`pytest -m "not artifacts"`: **2 failed, 1283 passed, 54 deselected, 8 warnings, 517.06s**
(tally line read directly from the captured log, not through a truncating pipe — the log was
redirected to a file with `set -o pipefail`, and the failing-test list was read with `tail -40`
against the **complete** captured file, not a live-truncated stream).

```
FAILED tests/test_t24_index_parsers.py::test_t24_paid_for_by_reads_every_arc_the_record_has
FAILED tests/test_t41_instrument_census.py::test_t41_axis_d_is_idempotent_across_runs
```

**Neither touches canon_gate/canon_router territory.** Root-caused by bisection (`git stash -u`
to a clean HEAD, then selective file moves) rather than assumed either way:

- **Both PASS against a clean `git stash`'d HEAD** (i.e., neither is a defect already sitting
  in the last commit `b9cd53c`).
- **Both PASS with only the three pre-existing, not-mine, untracked files
  (`docs/experiments/E58-a1-twin-prompts.json`, `E58-a1-twin-ring-report.md`,
  `E59-head-forward-kickoff.md`) moved aside — with every one of this seat's own edits
  (`tools/canon_gate.py`, `tests/test_t91*`, `tests/test_t92*`, `profiles/a1.json`) still
  present and dirty.** This isolates the cause to those three files' mere presence in the
  corpus, not to anything this stage wrote.

**T24** (`laws.paid_for_by cannot read 1 of the record's own arcs... : ['E59']`): matches an
**already-recorded precedent in this repo**, `docs/experiments/E34-projection-coverage-report.md`
section 8b, verbatim mechanism — `facet_index`'s `PAID_RE` (now an export of the installed
`record_index` pip package via `tools/facet_index.py`'s adapter, confirmed by reading that file
in full: it is 168 lines of `BINDING = record_index.bind(...)` / `globals().update(BINDING.exports())`,
zero occurrences of the literal string `PAID`) is a **frozen bound** that does not auto-track
`_record_arc_span()`, which is derived live from `parse_experiments()` — "the authored status
table plus the filesystem." The moment `docs/experiments/E59-head-forward-kickoff.md` exists
on disk, E59 enters the record's span and the frozen regex cannot read it. E34's own report
records the identical firing for E34 and its own disposition: **not repaired by that seat**,
because `tools/facet_index.py` is published tool code, the bound is a one-character fix but
"that is the advisor's call, not this seat's," and "It will fire again on E35 and on every arc
after it" — which it now has, on E59, exactly as predicted. This seat follows the same
disposition for the same stated reasons, one of which — "the executor rule is to stop at a
gate and report it with its evidence" — is this repo's own words for the exact rule this
seat's dispatch also states.

**T41** (`3 file(s) have an axis-D count that no longer reproduces... : ['e12_frame.py',
'e12_pair_cloud_step.py', 'turn_render.py']`): the E28-era self-referential corpus-census class
CLAUDE.md's own law describes at length ("An instrument that lives inside its own population
must be checked against itself on every axis, each time"). `docs/instrument-census.json` is a
**committed** snapshot of how many corpus files cite each instrument by filename; the fresh
re-scan sees `E58-a1-twin-ring-report.md`'s own prose (which discusses `e12_frame.py`'s frame
derivation, `e12_pair_cloud_step.py`'s pre-flight, and `turn_render.py`'s renders at length) as
**new** citations the committed snapshot predates. Not repaired here for the same reasons as
T24: out of Stage 0's chartered scope (no census-tool change was commissioned), and the named
remedy (`python tools/instrument_census.py --committed`) is a corpus-wide re-snapshot, not a
one-line fix scoped to this stage's own files.

**Neither is tuned past, narrowed, or silenced.** Both are reported here, complete, for the
advisor.

### Incidental finding, disclosed rather than claimed as Stage 0 work

The bisection above used `git stash -u` (all tracked + untracked changes) then `git stash pop`
to reach a clean HEAD and back. **Side effect, discovered afterward, not intended**:
`canon/A1-RECIPE.json` and `canon/A1-palette.json` — the two files E58's report named as
carrying a pre-existing CRLF defect (`worktree w/crlf despite .gitattributes declaring
eol=lf`, from `json.dump()` through a plain Windows `open(path, "w")`) — now read **zero**
CRLF bytes and show **empty** `git diff` against HEAD. The stash/pop cycle's own patch
application appears to have renormalized them to the `eol=lf`-declared form already sitting in
the committed blob (content unchanged — `git diff` is empty, not merely small). Confirmed
directly: `test_t06_no_crlf_in_tracked_text_files` now **passes**, where E58 recorded it
failing. This was not a deliberate repair — no one asked for it and Stage 0 did not target
these files — and is recorded here rather than silently enjoyed or silently ignored.

---

## Stage 1 — the head-alignment instrument, calibrated before it is believed (spend: 0). COMPLETE. GATE 1 FIRED.

### Enumerated before writing anything (per CLAUDE.md: "enumerate the resource before commissioning one")

Dispatched a research-only Explore agent over `tools/` (full recursive read, including
`tools/diagnostics/`). Findings, verified at their own primary sources afterward, not taken on
the agent's word alone:

- **No per-region registration/IoU instrument exists anywhere in this repo.** At least six
  independent whole-figure IoU implementations exist (`e08_registration.py`,
  `e13_crop_registration.py`, `e14_twin_registration.py`, `silhouette_agree.py`,
  `keyed_outside.py`, `e13_a2_allocation.py`), all the same one-line `(a&b).sum()/(a|b).sum()`
  pattern, never centralized — none restricted to a sub-region.
- **`figure_bbox_border_ring`** lives at `E:\AI\training\facet_E57\gate2_bbox_check.py` (an
  experiment-local script, not `tools/`) — the exact border-ring bilinear background fit E58
  Stage F already used, imported directly, to key these same ring twins for its own published
  whole-figure IoU table. Reused here rather than reimplemented.
- **`canon_bind.py`** is architecturally the "right" way to get an exact per-surface pixel mask
  (surface ids `hair`/`face`/`eyes`/`mouth`/`neck` are already declared on
  `canon/a1.surfaces.json`), but **A1 is 0% bound** — no `canon/a1.binding.json` exists, and
  authoring one is a nontrivial side-quest this repo's own docstring for the tool does not make
  free. Ruled out for a same-day, free Stage 1 probe.
- **`tools/verify/head_crop.py`** already carries a disclosed convention: `--head-frac`
  defaults to **0.19**, "a head height expressed as a fraction of TOTAL FIGURE HEIGHT, which is
  stable across subjects" (checked at the file directly, `head_crop.py:1-28`, not taken from
  the agent's paraphrase). Reused as the head-band fraction below.
- **No torso-region convention exists anywhere.** This stage's own, disclosed as such.
- **`canon_bind.py`'s `margin_holds()`** (`canon_bind.py:247-267`) is a precedented gate SHAPE
  for exactly this question — "does population A cleanly separate from population B" —
  `gap = min(population_predicted_higher) - max(population_predicted_lower)`, `ok = gap >=
  min_margin`. Reused for Gate 1's separation test below (the shape, not the numbers).

### Self-consistency check, run before trusting the re-implementation

Re-derived `figure_bbox_border_ring`'s keyed mask (the function itself returns only a bbox
summary; the boolean mask is separately recomputed with identical parameters, mirroring E58
Stage F's own inline code exactly) and ran it against E58's own exact silhouettes
(`facet_E58\controls\sil\`) for all 8 ring twins:

```
view 0: recomputed IoU=0.8747  E58 published=0.8747  MATCH
view 1: recomputed IoU=0.9259  E58 published=0.9259  MATCH
view 2: recomputed IoU=0.7453  E58 published=0.7453  MATCH
view 3: recomputed IoU=0.9103  E58 published=0.9103  MATCH
view 4: recomputed IoU=0.8988  E58 published=0.8988  MATCH
view 5: recomputed IoU=0.8794  E58 published=0.8794  MATCH
view 6: recomputed IoU=0.4490  E58 published=0.4490  MATCH
view 7: recomputed IoU=0.8181  E58 published=0.8181  MATCH
ALL VIEWS MATCH E58's PUBLISHED TABLE: True
```

All 8 match E58's already-published Stage F table to 4 decimal places — the re-implementation
is confirmed correct and consistent with the established method before anything region-specific
was built on top of it.

### The disclosed substitution: exact silhouette stands in for "control"

The charter names the aligned population as "E57 clay renders **against their own controls**."
No canny+contour control images were ever built for E57's clay renders (checked directly:
`facet_E57`'s own tree has no `controls\` directory at all — only E58 Stage C built controls,
from E58's own re-render). Rather than spend Stage-1 effort building fresh controls, the exact
raycast silhouette (`silhouette_masks.py`, zero pixel ambiguity, already the tool E58 itself
compared its controls against) is used as the geometric reference throughout, for **both**
populations. This is not an invented substitute: **E58's own Gate C already measured control
geometry and exact-silhouette geometry to coincide within 1-2px of bbox** ("Every control bbox
sits within ~1-2px of its own mask's bbox," `E58-a1-twin-ring-report.md:326`) — so a control
image and the exact silhouette are already established, in this exact repo's own prior work, as
near-interchangeable at the geometry level this instrument operates on.

E57 has no exact silhouette of its own on disk (E58 Stage C built exact silhouettes only at its
own 576x1024 frame). Computed fresh, zero spend, reusing `silhouette_masks.py` unmodified with
its own bare defaults (which already match E57's 752x1024/margin=1.204/fit-axis=height
convention exactly — confirmed by reading `turn_render.py`'s own argparse defaults, the tool
that produced E57's renders with no `--profile` passed) against a byte-identical copy of A1's
mesh (`sha256 cdf276e7...`, confirmed matching E57's and E58's own recorded hash).

### Row-band derivation — self-verified, not hardcoded from exploration

**Measured, not assumed**: `fit-axis=height` + `margin=1.204` on the **same mesh** places the
figure at **identical rows regardless of frame width**. Directly compared E57's (752-wide) and
E58's (576-wide) exact silhouettes' own top/bottom rows, all 8 views each:

```
view  E57(752w) top/bot/h        E58(576w) top/bot/h
0     87/936/850                  87/936/850
1     87/936/850                  87/936/850
2     87/936/850                  87/936/850
3     87/936/850                  87/936/850
4     87/936/850                  87/936/850
5     87/936/850                  87/936/850
6     87/936/850                  87/936/850
7     87/936/850                  87/936/850
```

Identical on **every one of 16 silhouettes measured**, both populations, every yaw — not an
assumption the instrument depends on, a self-verifying gate inside the instrument script itself
(`row_band()` derives the band from view 0 of each population, then asserts every other view
agrees exactly, halting with `ANDON` rather than averaging over disagreement if it does not).

### The instrument

`E:\AI\training\facet_E59\stage1\head_torso_readout.py`. For each candidate image (an E57 clay
render or an E58 ring twin) and its exact silhouette: key the candidate
(`figure_bbox_border_ring`'s border-ring bilinear fit, tol=18.0/ring_px=14/grid=24 — E58 Stage
F's own parameters), compute IoU restricted to a **head band** (rows `[top, top+0.19*height)`
— `tools/verify/head_crop.py`'s own `--head-frac` default, cited at source) and a **torso
band** (rows `[top+0.19*height, top+0.38*height)` — **this script's own convention**, disclosed
as exactly that: no torso fraction exists anywhere else in this repo; chosen as the
equal-sized band immediately adjacent to the head band, so neither region carries an unearned
pixel-count advantage in the comparison). Two normalized readouts, both natural forms of
"against the same statistic on the torso," both computed as a single pre-registered design
decision before any result was seen: `diff = head_iou - torso_iou` and `ratio =
head_iou / torso_iou`.

### Full data

```
--- ALIGNED population (E57 clay renders, head straight by construction) ---
ALIGNED  view 0  whole=0.7808  head=0.7780 (rows 87-248)  torso=0.8568 (rows 248-410)  diff=-0.0788  ratio=0.9080
ALIGNED  view 1  whole=0.7985  head=0.7809 (rows 87-248)  torso=0.8458 (rows 248-410)  diff=-0.0649  ratio=0.9232
ALIGNED  view 2  whole=0.8121  head=0.7904 (rows 87-248)  torso=0.9286 (rows 248-410)  diff=-0.1381  ratio=0.8512
ALIGNED  view 3  whole=0.7612  head=0.7360 (rows 87-248)  torso=0.6831 (rows 248-410)  diff=+0.0529  ratio=1.0774
ALIGNED  view 4  whole=0.8496  head=0.8248 (rows 87-248)  torso=0.8906 (rows 248-410)  diff=-0.0658  ratio=0.9261
ALIGNED  view 5  whole=0.8377  head=0.8032 (rows 87-248)  torso=0.8783 (rows 248-410)  diff=-0.0750  ratio=0.9146
ALIGNED  view 6  whole=0.8199  head=0.8129 (rows 87-248)  torso=0.8265 (rows 248-410)  diff=-0.0136  ratio=0.9836
ALIGNED  view 7  whole=0.8400  head=0.8350 (rows 87-248)  torso=0.8743 (rows 248-410)  diff=-0.0393  ratio=0.9551

--- TURNED population (E58 ring, views the charter named: 45, 90, 270 deg) ---
TURNED   view 1  whole=0.9259  head=0.8377 (rows 87-248)  torso=0.9456 (rows 248-410)  diff=-0.1079  ratio=0.8859
TURNED   view 2  whole=0.7453  head=0.8354 (rows 87-248)  torso=0.8289 (rows 248-410)  diff=+0.0065  ratio=1.0078
TURNED   view 6  whole=0.4490  head=0.8004 (rows 87-248)  torso=0.8569 (rows 248-410)  diff=-0.0565  ratio=0.9340
```

### GATE 1 — FIRED. The readout does not separate the calibration populations.

`canon_bind.py`'s `margin_holds()` shape, direction stated before the gap was computed
(hypothesis: a turned head departs from its control more than the torso does, so `diff` should
read lower for TURNED than for ALIGNED):

```
diff readout:  min(ALIGNED)=-0.1381  max(TURNED)=0.0065  GAP=-0.1446  DOES NOT SEPARATE
ratio readout: min(ALIGNED)=0.8512   max(TURNED)=1.0078   GAP=-0.1566  DOES NOT SEPARATE
```

Both readout forms of the one statistic overlap substantially: ALIGNED diffs range **-0.1381
to +0.0529**; TURNED diffs range **-0.1079 to +0.0065** — almost entirely inside the ALIGNED
range, not below it. **TURNED view 2 — yaw 90, the exact view Stage 2 probes — reads
diff=+0.0065, indistinguishable from several ALIGNED views**, despite the charter naming this
the view where the defect is worst.

**Per the charter's own words, this is the full result: "if the readout does not separate
them, say so plainly and report it as not an instrument — the Director's eye then rules the
probe alone."** No third readout form was tried after these two, and no parameter
(`HEAD_FRAC`, `TORSO_FRAC_HI`, keying `tol`) was retuned after seeing these numbers — either
would be exactly the "tuning toward a number" this repo's law forbids.

### Diagnosis offered, not a retune — two candidate reasons, both structural

1. **A keying-difficulty confound.** Even in the ALIGNED population — geometrically perfect by
   construction — `diff` is negative on 7 of 8 views (head IoU reads lower than torso IoU as a
   *baseline*, not as a signal of misalignment). Hair/curls produce fine, low-contrast
   silhouette boundaries that a smooth bilinear-fit keying method is plausibly worse at
   capturing than the torso's larger, simpler mass — consistent with (though not the same
   defect as) this repo's own documented law that a thin/fine structure is disproportionately
   vulnerable to a method tuned on bulk geometry ("Test the property, not a geometric proxy for
   it… a 1-2 px structure is entirely boundary").
2. **A structural mismatch between the statistic and the property.** Silhouette IoU measures
   **region overlap**, not **orientation**. A head turned toward the camera and a head facing
   away can plausibly occupy a similarly-shaped, similarly-sized silhouette blob — especially
   where hair volume dominates the visible mass over facial features — so region overlap may be
   the wrong *class* of measurement for "which way does the face point," independent of how the
   head/torso split or the keying tolerance are tuned. This reading is offered as a candid
   diagnostic note for the advisor/Director, not as grounds to try a different statistic this
   session — that would be the same forbidden move in different clothes.

### Consequence for Stage 2

Per the charter's own instruction, Stage 3's sheet is unaffected in kind: "The instrument's
readings appear as an appendix beneath, never as a verdict." Gate 1 firing makes this
literal rather than merely procedural — the readout built here is reported alongside Stage 2's
probe images as a diagnostic appendix, and **the Director's eye is the only head verdict this
arc produces.** No numeric prediction is made against this instrument for Stage 2 (a
prediction stated "inside the interval the instrument can return," per the E39/E40 law, would
be close to meaningless here — the instrument's ALIGNED and TURNED intervals already overlap
almost completely, so no number it could return would be strong evidence of anything). The
qualitative prediction (does the head look straight to the eye) is registered instead, below.

---

## Prediction, registered before Stage 2 runs

**Not blind to the advisor's own prediction** — the charter states it explicitly
("Arm P alone straightens the head"), read in full before this seat began. What follows is
this seat's own reasoning, stated as agreement-with-a-mechanism rather than a repetition, plus
one addition the advisor's text does not name.

**This seat's prediction: Arm P (text alone) most likely straightens the head, for the
advisor's stated reason** (denoise 0.92 leaves 92% of the diffusion process free to reinterpret
the latent — close to a fresh generation's creative freedom — and text conditioning is
typically a strong lever over gaze/head-orientation semantics at that freedom level) **and one
additional, mechanistic reason this seat adds**: Stage 1's own measurement found that E58 v2's
(the profile, yaw 90) head-region silhouette barely differs from an aligned head's silhouette
in outer shape (`diff=+0.0065`, indistinguishable from several ALIGNED views) — meaning the
*defect is substantially about internal facial orientation, not outer silhouette*. A
canny+contour control built from a profile-view head is dominated by the outer contour, which
changes little between "facing away" and "facing the camera" in profile — so **the control
itself plausibly carries a weak orientation signal to begin with**. If that reading is right,
Arm C (more control authority via lower denoise) has a real chance of **not** helping much
either, since leaning harder on a control that does not clearly encode orientation would not be
expected to resolve it — a different, and testable, prediction from "if Arm P fails, more
control authority is the fix."

**Stated inside the interval an honest instrument would allow**: since Gate 1 found the
head/torso IoU readout does not separate the calibration populations, **no numeric prediction
is registered against it** — a number stated "inside the interval the instrument can return"
would be nearly meaningless here, because that interval already spans both the aligned and
turned populations almost entirely. The prediction is qualitative only: **Arm P's head reads
as facing forward to the eye; Arm C is not expected to move the outcome much beyond what Arm P
already achieves, win or lose.** The instrument's numbers are still computed and reported on
both arms' outputs, as a diagnostic appendix, exactly as Stage 1 already is — never as the
verdict.

---

## Stage 2 — the probe (spend: 2). Ceiling: 2/2 spent. COMPLETE.

### Arms built from E58's own recorded materials, not reconstructed

Loaded `E:\AI\training\facet_E58\ring\graph_2.json` verbatim (E58's own actually-submitted
view-2 graph) and edited only the named nodes — read directly from the recorded file, not
rebuilt from `docs/experiments/E58-a1-twin-prompts.json` or `profiles/a1.json`, per the
charter's own instruction. A delta check (`E:\AI\training\facet_E59\stage2\build_arms.py`)
confirms programmatically, not by eye, that **only the named nodes differ**:

- **Arm P**: nodes 7 (positive text, `+", head facing straight ahead."` replacing the trailing
  period), 8 (negative text, `+"\uff0c looking at the viewer, head turned toward the camera"`
  appended), 15 (`filename_prefix`, bookkeeping only) differ from the base. Every other node —
  model loaders, ControlNet strength 0.9, seed 770700, steps 20, cfg 2.5, denoise 0.92, LoRA
  weight 0.75, the render/control image references — byte-identical to E58's own graph.
- **Arm C**: identical to Arm P except node 13's `denoise` (0.92 → 0.80) and node 15's prefix.

### Every submission passed the bound canon gate, checked before writing either graph

```
[canon] ARM P: gated=True required=17 missing=[] forbidden=[] unlicensed=[]
[canon] ARM C: gated=True required=17 missing=[] forbidden=[] unlicensed=[]
```

`required` reads 17 (16 ratified occupant phrases + the Stage-0-enforced `stage_head_forward`
clause, now present in both arms' text) — consistent with Stage 0's own `profiles/a1.json`
re-check. Link topology (the E04 G7 check — self-links, dangling targets, orphan
reachability, the same three checks `e12_pair_cloud_step.py` runs on its own authored graphs)
passed on both: `nodes=15 links=18 reachable=15 orphans=0`, matching E58's own recorded ring
graphs exactly.

### `estimate_credits` and `dry_run`, both arms, before any spend

Both graphs: `dry_run` → `{"status":"validated","warnings":[{"code":"input_validation",
"detail":"... lora_name ... was not found in the bundled node index"}],"submitted":false}` —
the same LoRA-catalog warning this repo already documented and resolved (E08 Ruling 31: absent
from the node list does not mean absent from the account's library). `estimate_credits`, both
arms: `"0 credits - no paid API nodes found in this workflow"` — the same reading E58 got on
this workflow shape, flagged for the same reason: this is a local-OSS-model graph billed by
GPU-second on this venue, not a metered API node the estimator can price. **Not a
free-generation claim.**

### Submission

`submit_batch` (both arms as one request, per the tool's own guidance for 2+ independent
generations): `{"submitted":2,"failed":[]}`. `wait_for_batch` returned both `ready` on the
first call (no timeout retries needed). `get_batch_output` returned both signed URLs;
downloaded via PowerShell to `E:\AI\training\facet_E59\stage2\a1_armP_v2.png` (474,700 bytes)
and `a1_armC_v2.png` (493,698 bytes). **Ceiling: 2/2 generations spent. No further spend is
possible or attempted for the remainder of this arc.**

### Gate E — delivered frame == requested frame

```
armP   size=(576, 1024) expected=(576, 1024) OK
armC   size=(576, 1024) expected=(576, 1024) OK
```

**PASSED, both arms.** No VAE-rounding mismatch (576 is div-16-legal by construction, per
E58's own Stage C derivation).

---

## Stage 3 — the sheet

`E:\AI\training\facet_E59\stage2\build_e59_sheet.py` (adapted from E58's own sheet-builder,
same ethic: native full-size files untouched on disk, this PNG an explicitly-downscaled
overview, sha256 provenance footer per panel). Output:
`E:\AI\training\facet_E59\stage2\E59_director_sheet.png` (2374x812) — control | E58 v2 (the
defect) | Arm P | Arm C, head-region crop (rows 60-340 of the 576x1024 frame, upscaled 3x) on
top, full figure beneath for context. Full-size, uncropped originals remain on disk at the
paths named above; the sheet is an overview only.

**What is visible, described plainly — the words verified/shipped/works/decisive/validated/
proven do not apply to what follows, and none of it is a ruling:**

- The **control** (a canny+contour edge map built from A1's own geometry, view 2, yaw 90) shows
  a single, unambiguous profile: one eyebrow/eye-socket contour near the front edge of the
  face, no far-side eye contour, nose and chin in a clean side line.
- **E58 v2 (the defect)**, at the same crop and zoom: both a brow arch and a rounded, more
  fully-drawn eye (visible iris and both lid contours) are present, and the cheek/blush shading
  extends further around the face than the control's profile line does.
- **Arm P**, at the same crop and zoom: the visible eye reads as a narrower, more foreshortened
  shape positioned closer to the front edge of the face, with a sharper, more side-on nose and
  jaw line — closer in outline to the control's profile contour than E58 v2's crop is.
- **Arm C**, at the same crop and zoom: reads similarly to Arm P at the face/eye/nose/jaw —
  narrow foreshortened eye, side-on nose and jaw line. The garment and lower body are
  substantially lower-contrast and less saturated against the grey backdrop than in the other
  three panels (visible directly in the sheet's full-figure row: the vest reads pale sage-green
  and the trousers/boots are only faintly differentiated from the background).

**No claim of "fixed" or "not fixed" is made here or anywhere in this report — that is the
Director's judgment, per role, on the full-size files or the sheet.**

### Appendix — the Stage 1 instrument's readings on all three panels, view 2

**Gate 1 (Stage 1) already found this readout does not separate the calibration populations.
The numbers below are reported for completeness, exactly as the charter specifies ("appears as
an appendix beneath, never as a verdict"), and are not read as evidence of anything on their
own.**

```
E58 v2 (the defect)                 whole=0.7453  head=0.8354  torso=0.8289  diff=+0.0065  ratio=1.0078
Arm P (text only)                   whole=0.8223  head=0.8225  torso=0.8745  diff=-0.0520  ratio=0.9406
Arm C (text + denoise 0.80)         whole=0.2410  head=0.3223  torso=0.2569  diff=+0.0654  ratio=1.2544
```

**Arm C's `whole_iou` (0.2410) is far outside the range measured anywhere else in this entire
arc** (ALIGNED 0.7612-0.8496; TURNED 0.4490-0.9259). Checked against the visual description
above rather than left as a bare number: Arm C's own full-figure crop shows markedly lower
figure-to-background contrast (the pale sage vest and faint lower body noted above), and the
keying method this instrument uses (`figure_bbox_border_ring`, a luminance-threshold border-ring
fit) is measuring exactly that — it classifies a pixel as figure only if it departs from the
fitted background by more than a fixed luminance tolerance, and a low-contrast garment against
a grey backdrop is close to the fitted background by construction. **This reads as a keying
instrument artifact consistent with Stage 1's own named diagnosis (a thin/low-contrast region
is disproportionately vulnerable to a border-ring luminance fit), not evidence about head
position specifically** — the head/eye region itself is comparably high-contrast (skin against
hair, hair against backdrop) in all three panels, and the head-region-only numbers
(head=0.3223 for Arm C vs 0.8225-0.8354 for the other two) move in the same direction as the
whole-figure number, consistent with a global keying effect rather than a head-specific one.
No further reading is offered — this is diagnostic context for whoever looks at the sheet next,
not a substitute for looking at it.

### Predictions and outcomes

| # | prediction | blind? | outcome |
|---|---|---|---|
| P1 (Stage 2, qualitative) | Arm P's head reads as facing forward to the eye; Arm C not expected to move the outcome much beyond Arm P | **Not blind** — read the advisor's own stated prediction in the charter first; this seat's own reasoning added a mechanistic note about the control's plausibly weak orientation signal in profile view | **Reported, not ruled on.** Described above: Arm P's crop shows a narrower, more foreshortened eye and a more side-on nose/jaw than E58 v2's crop, closer to the control's own contour. Arm C's face-region crop reads similarly to Arm P's. Whether this constitutes "facing forward" is the Director's call, not stated here as a result |
| P2 (Gate 1 instrument, numeric) | None registered — the interval an honest instrument could return already spanned both calibration populations almost entirely, so no number was predicted | N/A | N/A — appendix numbers reported above, not read as confirming or denying P1 |
| P3 (Gate E) | Delivered frame equals requested 576x1024 for both arms, per the div-16-legal frame law | Charter's own standing law, applied | **HELD**: 2/2 exact |

---

## Premises vs measured

| premise | source | status | resolution |
|---|---|---|---|
| A1's head is straight on the mesh; E57's clay ring shows it straight at every yaw | charter, citing E57/E58's own prior findings | **INHERITED, not re-measured this arc** | Used as the basis for Stage 1's ALIGNED calibration population without independently re-deriving "is the mesh straight" from scratch — this arc measured E57's clay renders' row-band placement and keying behaviour, not head-straightness itself, which E57/E58 already established |
| E58's Gate A anchor reproduced `canon/A1_reference.png` pixel-identically | charter, citing E58 | **INHERITED, not re-tested** | Not re-run; no venue-anchor question was in this arc's scope |
| E58 ring parameters (seed 770700, lora_w 0.75, cn 0.9, denoise 0.92, 576x1024) | charter | **VERIFIED directly** | Confirmed by reading `facet_E58\ring\graph_2.json` itself, not the charter's prose — the base graph Stage 2 copied from |
| E58's 8 delivered frames all equalled requested | charter, citing E58's own Gate E | **INHERITED, not re-tested** | Not re-run; this arc's own Gate E (armP/armC) was measured fresh, not inherited |
| `canon_gate.require_canon()` checks only the positive prompt | not stated in the charter; this seat's own premise before designing Stage 2's arms | **VERIFIED directly** | Read `tools/diagnostics/e12_pair_cloud_step.py`'s source: `canon_gate.require_canon(pos, ...)` — `neg` never passed |
| `figure_bbox_border_ring` (E58 Stage F's keying method) is directly reusable for a region-restricted readout | charter's implicit premise (names it as available) | **VERIFIED directly** | Re-derivation reproduces E58's own published whole-figure IoU table exactly, all 8 views, before anything region-specific was built on it |
| E57's clay renders have "their own controls" to compare against | charter's literal wording | **MEASURED FALSE, substituted, disclosed** | `facet_E57`'s own tree has no `controls\` directory; E58 Stage C built the only controls that exist, from a different (576-wide) render. Exact silhouette used as the geometric reference for both populations instead, justified by E58's own Gate C measurement that control geometry and exact-silhouette geometry already coincide within 1-2px |
| `head_frac=0.19` is "stable across subjects" | `tools/verify/head_crop.py`'s own docstring | **CITED AT PRIMARY SOURCE, not re-derived** | Read the file directly; used as a disclosed, reused convention, not independently re-measured for A1 |
| E57 (752-wide) and E58 (576-wide) frames place the figure at the same rows | not stated anywhere; this seat's own inference from `fit-axis=height`/`margin=1.204` both being shared | **VERIFIED directly, all 16 silhouettes** | top=87 bot=936 height=850, identical on every one of 8 E57 views and 8 E58 views measured |

---

## Gates summary

| gate | state | evidence |
|---|---|---|
| Stage 0: required-clause can-fail proof | PASSED | selftest disabled/re-enabled, ANDON fired when disabled, byte-identical restore confirmed |
| Stage 0: non-perturbing anchor | PASSED | full `census` table byte-identical before/after (not only W3/LONGSWORD); `resolve --subject A1` identical; T34 52/52 |
| Stage 0: full hermetic suite | 2 failed (T24, T41), both root-caused to pre-existing corpus files via git-stash bisection, NOT this stage's work; 1283 passed, 54 deselected | Full bisection evidence above; T24 matches E34's own recorded precedent exactly |
| GATE 1 (head/torso readout separates the calibration populations) | **FIRED — does not separate** | `gap = min(ALIGNED) - max(TURNED)` is negative for both the diff form (-0.1446) and the ratio form (-0.1566); full 11-view table above. Reported per charter as a full result, not tuned past |
| Stage 2: canon gate on both arms | PASSED | `required=17 missing=[] forbidden=[] unlicensed=[]`, both arms, checked before either graph was written |
| Stage 2: link topology on both arms | PASSED | `nodes=15 links=18 reachable=15 orphans=0`, both arms |
| Stage 2: delta check (only named nodes differ) | PASSED | programmatic diff against the base graph, both arms, asserted in code not eyeballed |
| GATE E (delivered == requested frame) | PASSED | both arms, 576x1024 exact |

---

## Ceiling and spend, final tally

**2 generations allowed. 2 spent. 0 remaining — ceiling reached exactly, as designed.**

| batch | spend | estimate_credits reported | actual result |
|---|---|---|---|
| Arm P + Arm C (one batch) | 2 | "0 credits - no paid API nodes found" both arms (flagged: GPU/queue-time excluded, not a free-generation claim) | 2 jobs via `submit_batch`, `submitted:2 failed:0`, both `ready` on first `wait_for_batch` call, Gate E PASSED both |

---

## git status --short (verbatim, current)

```
 M canon/A1-IDENTITY.md
 M canon/a1.surfaces.json
 M tests/test_t91_canon_in_path.py
 M tests/test_t92_canon_router.py
 M tools/canon_gate.py
?? docs/experiments/E58-a1-twin-prompts.json
?? docs/experiments/E58-a1-twin-ring-report.md
?? docs/experiments/E59-head-forward-kickoff.md
?? docs/experiments/E59-head-forward-report.md
?? profiles/a1.json
```

(Re-run and pasted verbatim at close, replacing an earlier draft of this section that
mis-stated `profiles/a1.json` as tracked-modified — it is untracked, created at E58 and never
committed, and this seat's edit to it does not change that status.)

`canon/A1-IDENTITY.md` and `canon/a1.surfaces.json` are the advisor's own pre-dispatch edits
(the POSE section and the `stage_head_forward` clause), present before this seat began — not
this seat's diff, confirmed by reading them at session start before any tool call touched
them. `tests/test_t91_canon_in_path.py`, `tests/test_t92_canon_router.py`, and
`tools/canon_gate.py` are this seat's Stage 0 work (tracked, modified). `profiles/a1.json` is
untracked (created at E58, never committed) and this seat edited it (Stage 0's prompt fix) —
still untracked, since editing an untracked file does not change its tracked status. The three
other untracked `docs/experiments/` files predate this seat (confirmed by the T24/T41
bisection above); `E59-head-forward-report.md` is this seat's own report, also untracked as of
writing. Nothing committed by this seat, per role — left for the advisor to review and commit
by pathspec.

## Working tree

`E:\AI\training\facet_E59\` — `handoff.md` (kept current through every stage),
`census_BEFORE.txt` / `census_AFTER.txt` / `resolve_A1_BEFORE.txt` / `resolve_A1_AFTER.txt`
(Stage 0 anchor), `canon_gate.py.bak_verify` (the can-fail-proof backup), `stage1\` (row-band
derivation, the keying self-consistency check, `head_torso_readout.py`,
`head_torso_report.json`, E57's freshly-derived exact silhouettes at `sil57\`), `stage2\`
(`build_arms.py`, `graph_armP.json`, `graph_armC.json`, `a1_armP_v2.png`, `a1_armC_v2.png`,
`appendix_readout.py`, `appendix_report.json`, `build_e59_sheet.py`,
`E59_director_sheet.png`, the four `headcrop_*.png` files).

---

*(Report complete through Stage 3. `handoff.md` holds the same close-out, condensed, for the
advisor's continuity.)*
