# E61 report — which layering repair carries the garment through a composed prompt

Charter: [E61-layering-repairs-kickoff.md](E61-layering-repairs-kickoff.md), including its
own "Dispatch record (living)" section, appended mid-flight by the advisor from an outside
channel — two steers, the second superseding a wrong worked example in the first. Both are
addressed in this report's Measurement section and in
`E:\AI\training\facet_E61\stage2p5\preflight_design_note.md`.

Working tree: `E:\AI\training\facet_E61\`

No word in this report is `verified`, `shipped`, `works`, `decisive`, `validated`, or
`proven`. Nothing here is ranked. The Director's eye chooses; this report gives him
numbers and pixels.

---

## Stage 0 — composer extensions (spend: 0). COMPLETE.

`tools/canon_compose.py` gained three additive, keyword-only capabilities, all defaulting
to values that reproduce E60's own output byte-for-byte when omitted (measured — see
below, not assumed):

- **`garment_join="and"|"over"`** — wired only into `form="grouped"` (ANDONs otherwise).
  Changes exactly the head-pair connector inside `_join_grouped_garments` from `" and "`
  to `" over "` — the single preposition E60's own failure traced to.
- **`joints=()`** — a tuple of `doc["joints"]` ids to emit as additional trailing
  sentences via the now-licensed (E60 fold) joint phrases. Licensing is not requiring:
  the default emits nothing.
- **`with_occupant_phrase(doc, n_id, phrase)`** — a deep-copied doc with one occupant's
  phrase overridden, used to compose *and* gate-check P0/P1 against A1's pre-repair N1
  text without touching `canon/a1.surfaces.json` on disk (the charter's own words).

**Three new can-fail legs** added to `canon_compose.selftest()`, each proven by checking
both the positive and negative case (the string actually changes / the gate still holds /
the default omits it / an invalid combination or unknown id refuses). `tests/
test_t92_canon_router.py::test_t92_selftest_still_holds` extended in place (+9 lines, 0
new test functions) — same T34-constraint precedent E59/E60 both used.

**Measured, not assumed:**
- `python tools/canon_compose.py --selftest` → exit 0: `selftest PASS
  front/flat/consolidated gated rear drops face anchor in_both=22 canon_only=9
  garment-join-over held joint-emit held occupant-override held`
  (`stage0/selftest_run1.log`). The anchor numbers (22/9) differ from E60's own
  post-correction 23/1 because the canon has moved further since that correction
  (sleeveless N1, 9 licensed joint phrases) — expected drift against the *original*
  recipe text, not a defect.
- `pytest --collect-only -q`: **1342 tests collected**, confirmed via `git stash` to be
  the count **before** any edit this session made (E60's own close recorded 1339; the
  +3 drift landed in a commit between E60's close and this session's start, unrelated to
  this arc) **and unchanged after** both of this session's edits — 0 new pytest items
  added (`stage0/collect_run1.log`, `collect_run2_final.log`).
- Canon-adjacent suite (t87 + t92 + t93): **43/43 PASSED**, both before and after the
  test edit (`stage0/canon_suite_run1.log`, `run2.log`).
- **`tests/test_t34_front_door_counts.py`: 25 FAILED at HEAD**, confirmed via `git stash`
  to be identical with this session's edits stashed away — pre-existing, not caused by
  this arc. Same disposition E59/E60 both recorded for this file: report, do not fix;
  reconciling needs regenerating 7 translated READMEs, outside a Sonnet executor's
  authority (studio translation rule). `stage0/t34_run1.log` has the full list.

---

## The two mid-flight steers, and how the preflight was actually built

Full account: `stage2p5/preflight_design_note.md`. Compressed here.

**Steer 1** (received first): read the sleeve region box, calibrate a preflight against
E60's own 12 images before trusting any threshold; fall back to reporting a
cannot-discriminate finding rather than inventing a cut. **Calibration performed before
steer 2 arrived** (`stage2p5/preflight_calibration.py`, `preflight_calibration.json`):
two candidate signals, tested against two genuinely labeled populations (each image's own
backdrop corners = known background; the sleeve_L/sleeve_R boxes across the reference +
E60's 12 generations = known on-figure, confirmed by direct visual inspection of
`E60_shirt_crop_panel.png` — every one of the 12 cells shows continuous fabric, none shows
the box on backdrop). Distance-to-backdrop-corner **does not separate** (on-figure boxes
read as close as 0.21–0.66 dE from a backdrop corner even on cells confirmed by eye to be
solid fabric — matching `canon/A1-palette.json`'s own documented finding that this
backdrop's hue sits too close to N2's for hue/chroma to discriminate). Local standard
deviation of L\* within the box (texture) **separates cleanly**: backdrop corners read
0.25–0.50 across all 13 known images; every sleeve box (shirt or vest, any of the 13)
reads 13.73–31.02. >27x gap, zero overlap, and neither term of that statistic references
N2's hue, N1's colour, or the backdrop's colour.

**Steer 2** (supersedes steer 1's own worked example): the example "if the box samples
vest fabric, mark it unavailable" was wrong — on E60's 12 frames the forearm never left
the box; what fills it in the four flagged cells is the vest's *own new sleeve*, which is
the defect this arc exists to count, not a measurement failure. Corrected design: three
states, not two — **UNAVAILABLE** (spatial only: box not on a forearm at all; judged
without N2 hue/N1 colour/vest-match, so the readout cannot gate its own availability) /
**AVAILABLE+present** (Δhue < 9°) / **AVAILABLE+occluded** (Δhue in the 63–67° neighbourhood,
or closer in Lab to N1's reference colour than N2's). Both AVAILABLE states vote.
Backdrop-departure keying is explicitly forbidden (it inverts the vote on this image, per
the palette file's own recorded corner distances). Pre-stated expectation: no spatial cut
separates E60's twelve, because none of them is actually off-figure.

**My own local_L\_std signal, built before steer 2 arrived, already satisfied steer 2's
hard constraint** — it never compares to N2 hue, N1 colour, or backdrop colour; it only
asks whether the box holds a textured/painted surface versus a smooth gradient, a question
blind to *which* material is present. Adopted as the axis-1 (spatial) preflight signal,
unchanged by steer 2.

**Final operational design** (`stage3/measure_arms.py`): default AVAILABLE for every row.
`local_L_std` computed and reported for every N2 sleeve sub-region as a diagnostic. A
tripwire at 2.0 (4x the observed backdrop ceiling, >6x below the observed on-figure floor
— a margin, not a validated two-sided cut, since no known off-figure example exists to
validate one against) would flag a row for eye inspection against its own crop before any
UNAVAILABLE verdict; **it did not fire on any of this arc's 15 rows** (below). Axis 2
(present/occluded, AVAILABLE rows only): Δhue < 9° = present; Δhue in 55–75° **or** nearest-
reference-colour test says closer to N1 = occluded; neither = reported as its own
indeterminate case rather than silently bucketed.

---

## Predictions — a disclosed gap, not backfilled

**This executor did not write down its own numeric prediction before Stage 2's
submission**, missing the charter's own requirement ("The seat states its own before
Stage 2, blind status disclosed"). This is the same gap E60's own seat disclosed for
itself, and it is disclosed here rather than backfilled — writing a number now, with
Stage 3's results already in hand, would be hindsight wearing a prediction's clothes,
which this repo's record exists to catch rather than commit.

The charter's own pre-registered prediction, from the advisor, stands as the arc's one
falsifiable prior: *"P1 holds the garment at 3 of 3 seeds and P2 matches it... If P1
fails, [the reasoning] is wrong and the declaration is what matters."* Stage 3's numbers
are reported against it below, as numbers — this executor renders no verdict on it.

---

## Stage 1 — the five arms' text, and Gate B (spend: 0). COMPLETE.

`stage1/build_texts.py`. Arm R: `canon/A1-RECIPE.json` `positive_text`, verbatim. Arm L:
E60's own flat-form text, read out of `graph_L_{106,770700,314159}.json` and confirmed
byte-identical across all three seeds before use (not assumed). Arm P0/P1: composed
against a `with_occupant_phrase`-modified doc carrying A1's pre-repair N1 text. Arm P2:
composed against the live (fully repaired) doc.

**A genuine catch, not a footnote.** The first version of `OLD_N1` guessed `"a plum
long-vest with fine gold embroidery"` (matching N2/N3's leading-article pattern). The
script's own byte-identity assertion against E60's recorded Arm P text (extracted from
`facet_E60/stage2/graphs/graph_P_106.json`) **failed**: E60's actual pre-repair phrase
carried **no leading article at all** — `"plum long-vest with fine gold embroidery"`. The
canon repair that added "sleeveless" evidently also added the leading "a" (`a1.surfaces.
json`'s own note says only *"N1 gains the word SLEEVELESS"*), which is reported here as a
measured finding, not corrected — a canon-authorship question outside this arc's charter.
Corrected, `text_P0` then reproduced E60's own Arm P text **exactly, byte-for-byte**
(asserted in `build_texts.py`, held on re-run — `stage1/run2.log`).

**Gate B**, checked against the doc state honest for what each arm represents:

| arm | checked against | ok | missing | forbidden | unlicensed | replay verdict |
|---|---|---|---|---|---|---|
| R | live canon | False | 3 (N1 sleeveless phrase x2, `stage_head_forward`) | 0 | 1 span | `replay_drift` |
| L | live canon | False | 2 (N1 sleeveless phrase x2) | 0 | 1 span | `replay_drift` |
| P0 | pre-repair (modified) doc | **True** | 0 | 0 | 0 | `replay_match` |
| P1 | pre-repair (modified) doc | **True** | 0 | 0 | 0 | `replay_match` |
| P2 | live canon | **True** | 0 | 0 | 0 | `replay_match` |

R and L are frozen historical text, checked against the *live* canon via both
`check_prompt` (report, not raise) and `report_replay_drift` — `canon_gate.py`'s own
documented tool for exactly this case ("a recorded prompt is a historical object... drift
to name, not a reason to halt a faithful replay"). Both disclose drift because the live
canon now requires "sleeveless" and neither frozen string carries it — disclosed, not
halting, the same disposition E60 gave Arm R. **No arm was halted**: P0 and P1 pass their
own fair check (does the composer's output satisfy the composer's own inputs); P2 passes
the live canon outright, the strongest test available.

Full text of all five arms is in `stage1/text_{R,L,P0,P1,P2}.txt` and printed in
`stage1/run2.log`.

---

## Stage 2 — the spend (15/15). COMPLETE. GATE A PASSED.

`stage2/build_graphs.py` — same base graph E60 used
(`facet_E58/reference/A1_full_graph.json`), same three named deltas (positive text, seed,
`SaveImage` prefix), same per-graph delta assertion and E04 G7 topology check. **15/15
PASS** (`nodes=19 links=22 reachable=19 orphans=0`, every graph — `stage2/run1.log`).

**Pre-submission checks**, both free, both run before the batch: `dry_run` on the R/106
graph → `status=validated, warnings=[]`. `estimate_credits` on the same graph → "0 credits
— no paid API nodes found" (the same disclosed estimator limitation E58–E60 already
named: this workflow bills GPU/queue time, which the estimator does not price).

**Submission: one `submit_batch` call, 15 items, `client_os=windows`.**
`submitted=15 failed=[]`. batch_id and all 15 job_ids recorded in `stage2/spend_record.md`
immediately after submission, before any wait. No `confirm` round-trip was required (0
paid API nodes, same as E60's own experience).

**Completion:** all 15/15 terminal, **0 failed**, via repeated `wait_for_batch` polling.
Downloaded to `gen/` — every one of the 15 files **1136×1472 RGB**, one uniform size
across the batch (`stage2/download_run1.log`), matching `A1_reference.png`'s own
dimensions and E60's own delivered frame exactly.

**GATE A** (charter: "Arm R failing to reproduce `canon/A1_reference.png` at seed 106
HALTS THE ARC"). **PASSED.** `armR_seed106.png` vs `canon/A1_reference.png`, compared
**pixel by pixel**, not file hash (this repo's own law): **0 of 1,672,192 pixels differ in
any channel (0.000000%), max channel delta 0, mean abs channel delta 0.0** —
pixel-identical (`stage2/gate_a_run1.log`). File bytes differ (sha256
`9417cd64...` vs `438cb5f2...`) — PNG encoder metadata only, the documented false-halt
pattern this repo has already named twice.

**GATE C** (charter: "delivered frame equals requested frame per image, the VAE-rounding
law"). **PASSED, read precisely.** The requested latent is 1140×1472 (byte-identical to
the base graph at every graph, per Stage 2's own delta assertion); the delivered frame is
uniformly 1136×1472 across all 15 files. 1140 is not divisible by 8 (1140/8 = 142.5); 1136
is (1136/8 = 142) — the exact documented Qwen-VAE ÷8 rounding this repo's own law names,
not a new or per-image-varying mismatch. What the gate actually protects — that every
generated file shares ONE size, so `canon/A1-palette.json`'s region boxes transfer without
rescaling — holds for all 15.

**A finding neither gate is built to report, so stated here plainly: 9 of the 15 images
are not new evidence.** Billing (`get_billing_activity`) showed R (all 3 seeds), L (all 3
seeds) and P0 (**all 3 seeds**) completing in 0.81–1.45 GPU-seconds each, against
55.7–57.3 GPU-seconds for every P1/P2 job. Checked directly
(`stage3/cross_arc_pixel_check.py`, same pixel-by-pixel method as Gate A, all nine pairs
verified individually — `stage3/cross_arc_run1.log`): **all nine of R/L/P0's E61 images
are pixel-identical to E60's own corresponding files, 0 of 1,672,192 pixels differing, in
every one of the nine cases.** R's text is always the recipe verbatim; L's and P0's text
were built to reproduce E60's own strings exactly (Stage 1). A render cache keyed on
generation parameters (blind to the `SaveImage` filename prefix, which cannot affect
pixels) explains this exactly — the same "measured curiosity" E60's own report flagged for
`armR_seed106` alone, now confirmed at 9 of 15 images and not merely asserted. **This
means only the 6 P1/P2 images are genuinely new pixels this arc generated**; R, L and
P0's rows below reproduce E60's own measurements rather than independently confirming
them, and are reported as such rather than counted as fresh replication.

**Spend, measured** (`get_billing_activity`, job-scoped): the 15 jobs summed to **~346.7
GPU-seconds (~5.78 GPU-minutes) on `rtx_pro_6000`**. Per-job breakdown in
`stage2/spend_record.md`. Comfy Cloud does not report per-job dollar cost; workspace
invoices live at `cloud.comfy.org → settings → workspace`.

---

## Stage 3 — measurement (spend: 0). COMPLETE.

`stage3/measure_arms.py` — region boxes read live from `canon/A1-palette.json`; Lab
transform and dE/hue methodology byte-identical to E60's own (`canon_gate.to_lab`,
`verify_regions`, the circular-hue/chroma-floor discipline). No VLM judges a colour
anywhere in this arc (charter finding 6). Full per-region/per-material table for all 15
images: `stage3/measure_report.json`. The N2 two-axis table alone:
`stage3/n2_two_axis_rows.json`.

**All 10 NAMED materials structurally present in every one of the 15 generations** —
confirmed, not assumed: zero region rows returned `px=0`.

### Axis 1 (spatial availability) — every row

**15 of 15 rows read AVAILABLE. The 2.0 tripwire fired on zero rows** — local_L_std
ranged 12.25–31.02 across all 30 sub-region readings (15 images × sleeve_L/sleeve_R),
nowhere near the 0.25–0.50 backdrop band the calibration measured. No row needed the
eye-check escalation; visual inspection of the full sleeve crop panel (below) independently
confirms every cell holds a forearm, never backdrop.

### Axis 2 (present / occluded), primary readout

| arm | seed | Δhue (deg) | axis2 | dE(N1 ref) | dE(N2 ref) | closer to |
|---|---|---:|---|---:|---:|---|
| R | 106 | 0.0 | present | 50.3 | 8.5 | N2(shirt) |
| R | 770700 | 1.9 | present | 59.2 | 13.2 | N2(shirt) |
| R | 314159 | 3.0 | present | 48.9 | 11.3 | N2(shirt) |
| L | 106 | 8.0 | present | 57.9 | 9.3 | N2(shirt) |
| L | 770700 | 4.9 | present | 65.7 | 17.5 | N2(shirt) |
| L | 314159 | 6.7 | present | 60.3 | 12.0 | N2(shirt) |
| P0 | 106 | 63.7 | **occluded** | 7.8 | 44.3 | N1(vest) |
| P0 | 770700 | 66.8 | **occluded** | 7.6 | 45.8 | N1(vest) |
| P0 | 314159 | 2.7 | present | 59.5 | 12.1 | N2(shirt) |
| P1 | 106 | 6.2 | present | 54.0 | 6.4 | N2(shirt) |
| P1 | 770700 | 3.4 | present | 64.1 | 15.9 | N2(shirt) |
| P1 | 314159 | 4.0 | present | 59.8 | 12.7 | N2(shirt) |
| P2 | 106 | 6.6 | present | 56.4 | 8.2 | N2(shirt) |
| P2 | 770700 | 4.0 | present | 63.8 | 15.4 | N2(shirt) |
| P2 | 314159 | 4.0 | present | 59.2 | 11.5 | N2(shirt) |

Zero rows landed in the indeterminate band (9–55° or 75°+); the hue-band classification and
the nearest-reference-colour classification agree on every one of the 15 rows. P0's two
occluded seeds (106, 770700) and one present seed (314159) reproduce E60's own Arm P
findings exactly, seed for seed — expected, since (Stage 2) those three images are
pixel-identical to E60's own.

**Per-arm summary, full denominator, no ranking:**

| arm | available | present | occluded | indeterminate |
|---|---|---|---|---|
| R | 3 of 3 | 3 | 0 | 0 |
| L | 3 of 3 | 3 | 0 | 0 |
| P0 | 3 of 3 | 1 | 2 | 0 |
| P1 | 3 of 3 | 3 | 0 | 0 |
| P2 | 3 of 3 | 3 | 0 | 0 |

---

## Stage 4 — the sheet

- `stage4/E61_director_sheet.png` — reference | Arm R | Arm L | Arm P0 | Arm P1 | Arm P2,
  one row per seed, full body, labels only.
- `stage4/E61_sleeve_crop_panel.png` — the N2 sleeve_L region crop (expanded), same
  layout, each cell labeled with its measured hue/Δhue and its axis-2 verdict only (no
  ranking language).
- Full-size source PNGs: `gen/arm{R,L,P0,P1,P2}_seed{106,770700,314159}.png` (15 files,
  1136×1472 each).

---

## Premises vs measured

| premise | status |
|---|---|
| P0 (composed against pre-repair canon) reproduces E60's own failing Arm P | measured true — byte-identical text (Stage 1) AND pixel-identical images (Stage 2) |
| `garment_join="over"` and `joints=(...)` are additive and preserve E60's own compose() output when omitted | measured true — collect-only count and canon-adjacent suite unchanged before/after; three new can-fail legs hold |
| The live canon's N1 phrase is "sleeveless" inserted into the pre-repair phrase, nothing else | measured **false** — the repair also added a leading "a" not present in the pre-repair text (caught by a byte-identity assert against E60's own recorded text) |
| Local std of L\* within the sleeve box separates on-figure from backdrop | measured true, with a wide margin (0.25–0.50 vs 13.73–31.02 across 13 known images) — but the calibration corpus contains no negative (off-figure) example, disclosed as a limit rather than papered over |
| Gate C's "requested equals delivered frame" | measured true only under the documented ÷8 VAE-rounding reading (1140 requested → 1136 delivered, uniformly, matching the reference); a literal byte-for-byte reading of "requested" would report a mismatch that is not the gate's actual concern |
| Every E61 image is independent new evidence | measured **false** — 9 of 15 (all of R, all of L, all of P0) are pixel-identical reproductions of E60's own images, not fresh generations |
| The charter's own prediction ("P1 holds the garment at 3 of 3 seeds and P2 matches it") | reported as numbers above; not adjudicated by this executor |

## Gates summary

| gate | result | evidence |
|---|---|---|
| Gate A — Arm R seed 106 reproduces `canon/A1_reference.png` | **PASSED** | 0/1,672,192 pixels differ, Stage 2 |
| Gate B — every emitted prompt passes `canon_gate.check_prompt` against its designated doc state | **PASSED for P0/P1/P2** (the MUST-PASS arms); R/L disclose drift against the live canon via `report_replay_drift`, not halting, matching E60's own Arm R precedent | Stage 1 |
| Gate C — delivered frame equals requested frame, consistently, per the documented ÷8 rounding | **PASSED** | all 15 files 1136×1472, Stage 2 |

No gate fired. No arm halted. No gate was skipped.

## Spend, final tally

15/15 generations spent, ceiling reached exactly, no further submission made or intended.
~346.7 GPU-seconds measured across the 15 jobs (`get_billing_activity`, job-scoped). 9 of
those 15 jobs were near-zero-cost cache hits against E60's own prior generations (Stage 2).
Dollar cost is not exposed per-job by Comfy Cloud; workspace invoices live at
`cloud.comfy.org`.

## Verification re-run at close

- `pytest --collect-only -q`: **1342 tests collected** (pre-existing baseline, confirmed
  unmoved by this arc's own edits via `git stash`).
- Canon-adjacent suite (t87 + t92 + t93): **43/43 PASSED**.
- `python tools/canon_compose.py --selftest`: **exit 0**, all new legs held.
- Full untargeted suite (`pytest -q`, no marker filter, all tiers):
  **26 failed, 1316 passed, 8 warnings, 924.87s** (`stage0/full_suite_run1.log`).

### The 26 full-suite failures, root-caused, not fixed — both classes pre-existing

**25 are `tests/test_t34_front_door_counts.py`** — the collected-item baseline drift
already confirmed via `git stash` (Stage 0, above) to predate this session's own edits.
Every failure states the same shape: a doc surface asserts `1339`/`1285`, the live
collector reports `1342`/`1288` — a uniform +3 drift across every pinned site, landed in
some commit between E60's close and this session's start. Same disposition E59/E60 both
recorded for this class: report, do not fix — reconciling needs regenerating 7 translated
READMEs (`translate-all.mjs README.md --cache-clear`), outside a Sonnet executor's
authority under the studio's translation rule.

**1 is `tests/test_t24_index_parsers.py::test_t24_paid_for_by_reads_every_arc_the_record_
has`** — `AssertionError: laws.paid_for_by cannot read 1 of the record's own arcs...:
E61` / `assert not ['E61']`. The exact mechanism E60's own report already root-caused:
`record_index`'s `PAID_RE` regex is bounded by construction to the highest decade it was
last widened for, and any arc numbered into a new decade fires this leg regardless of
content. E60's report measured the bound stopping at `E5[0-9]` (through E59); some commit
between E60's close and this session widened it far enough to cover E60 itself (the
failure names only `E61`, not `E60`), but naturally not E61, which did not exist when that
widening happened. **Not fixed, on purpose** — `record_index` is a separately installed
package (`E:\AI\record-index\`) outside this repo's own `tools/` tree and this arc's
charter, matching the identical disposition E59 and E60 both already recorded for this
exact test file. Every arc that crosses into a new numeric decade will keep firing this
leg until `record_index`'s bound is widened — the advisor's call, not this executor's.

Neither class is new, and neither traces to anything this arc changed — confirmed by the
Stage 0 `git stash` test for T34, and by the fact that T24's own mechanism is already
fully documented in this repo's history and fires on arc *number* alone, independent of
content.

## git status --short (verbatim, read fresh at fold time — NOT a snapshot from earlier
in this session, per this repo's own established practice for a tree that will not hold
still)

```
 M README.es.md
 M README.fr.md
 M README.hi.md
 M README.it.md
 M README.ja.md
 M README.md
 M README.pt-BR.md
 M README.zh.md
 M SHIP_GATE.md
 M docs/advisor-kickoff.md
 M docs/experiments/README.md
 M docs/index/conventions.json
 M docs/instrument-census.json
 M docs/instrument-census.md
 M site/src/content/docs/handbook/getting-started.md
 M site/src/content/docs/handbook/reference.md
 M site/src/site-config.ts
 M tests/test_t92_canon_router.py
 M tools/canon_compose.py
?? docs/experiments/E61-layering-repairs-report.md
```

**This executor's own four surfaces**: `tools/canon_compose.py`,
`tests/test_t92_canon_router.py`, `docs/experiments/E61-layering-repairs-report.md`
(untracked, this file), and (already at HEAD before this arc opened, not this executor's
edit) the advisor's own kickoff dispatch-record commits.

**Every other modified file above is NOT this executor's edit** — it was not present in
this arc's own git-status checks earlier in the session (Stage 0's collect-only diagnostics
ran against a tree showing only this executor's two files modified) and this executor
touched none of them. The set is exactly `test_t34_front_door_counts.py`'s own pinned
surfaces — `README.md` + its 7 translations, `SHIP_GATE.md`, `site/src/site-config.ts`,
both handbook pages, `docs/advisor-kickoff.md` — strongly suggesting a concurrent session
is actively repairing the T34 collected-count drift this report names above (1339→1342),
matching the "two live sessions share the tree" pattern this repo's own record already
names for `tools/canon_gate.py` during E60. **Not determined here** which session or
whether it is complete — asserting so without checking would be its own unmeasured claim.
`docs/index/conventions.json` and `docs/instrument-census.{json,md}` are similarly
untouched by this executor and unexplained by this report.

`canon/A1-RECIPE.json`, `canon/A1-palette.json`, `canon/a1.surfaces.json`,
`canon/A1_reference.png` — **untouched**. No canon edit was made.

## Working tree — file map

- Report: `E:\AI\facet\docs\experiments\E61-layering-repairs-report.md` (this file)
- Handoff: `E:\AI\training\facet_E61\handoff.md`
- Modified tool: `E:\AI\facet\tools\canon_compose.py`
- Modified test: `E:\AI\facet\tests\test_t92_canon_router.py`
- Stage 0: `stage0\selftest_run1.log`, `collect_run1.log`, `collect_run2_final.log`,
  `canon_suite_run1.log`, `canon_suite_run2.log`, `t34_run1.log`, `full_suite_run1.log`
- Stage 1: `stage1\build_texts.py`, `run1.log` (the OLD_N1 catch), `run2.log`,
  `text_{R,L,P0,P1,P2}.txt`, `stage1_report.json`, `e60_text_extract.log`
- Stage 2: `stage2\build_graphs.py`, `graphs\graph_{R,L,P0,P1,P2}_{106,770700,314159}.json`,
  `graphs\_manifest.json`, `prepare_batch.py`, `batch_items.json`,
  `batch_items_compact.json`, `spend_record.md`, `download_outputs.py`, `download_run1.log`,
  `gate_a.py`, `gate_a_run1.log`
- Stage 2.5: `stage2p5\preflight_calibration.py`, `preflight_calibration.json`, `run1.log`,
  `backdrop_summary.log`, `preflight_design_note.md`
- Stage 3: `stage3\measure_arms.py`, `measure_report.json`, `n2_two_axis_rows.json`,
  `run1.log`, `cross_arc_pixel_check.py`, `cross_arc_run1.log`
- Stage 4: `stage4\build_sheet.py`, `E61_director_sheet.png`, `E61_sleeve_crop_panel.png`,
  `run1.log`
- Generations: `gen\arm{R,L,P0,P1,P2}_seed{106,770700,314159}.png` (15 files),
  `_download_manifest.json`
