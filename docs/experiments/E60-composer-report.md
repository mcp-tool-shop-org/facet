# E60 report — the composer: canon → prompt → reference

Charter: [E60-composer-kickoff.md](E60-composer-kickoff.md)
Working tree: `E:\AI\training\facet_E60\`

No word in this report is `verified`, `shipped`, `works`, `decisive`, `validated`, or
`proven`. Nothing here is ranked. The Director's eye chooses the reference; this report
gives him numbers and pixels.

---

## Stage 0 — the composer (spend: 0). COMPLETE.

`tools/canon_compose.py`, new file. `canon` (occupant phrases + `legal_clauses`) → prompt,
in three forms:

- **`grouped`** (Arm P) — framing → staging → style → identity, garments joined
  `"G1 and G2, G3, G4 and G5"` (first two and-bound, the rest a comma list with a final
  `and`), features the same shape.
- **`flat`** (Arm L) — the established E58/`profiles/a1.json` convention: framing, then
  every phrase joined with a bare comma, N-id numeric order, pose clauses last (matching
  how that string actually grew — E59 Stage 0 appended them to an already-written flat
  list).
- **`consolidated`** (Arm G) — identical to `grouped` except the garment span is
  `"G1 with G2 with G3 with G4 and G5"` — zero internal commas, one unbroken noun phrase.
  Only the garment span differs from `grouped`; features are untouched, per the charter's
  own scoping ("Arm G — composed prose with the **garment** consolidated").

**The hard constraint found while building it, not assumed from the charter.**
`canon_gate.check_prompt`'s reverse check (`unlicensed_residue`) strips every licensed
phrase, then punctuation, then a **fixed stopword list**:
`a|an|the|with|and|or|of|on|in|at|to|for|from|by|as|his|her|its|their|this|that|each`.
The reference's own recipe text joins the vest and shirt with **"over"**, and "over" is
not in that list — `canon/A1-IDENTITY.md` already documents that the raw recipe fails the
gate for exactly this reason. So "join related garments with prepositions" (the charter's
own words) can only draw on the stop-list prepositions above; `_join_grouped_garments`
and `_join_consolidated_garments` in `canon_compose.py` are built from that closed set on
purpose, and the module docstring says so.

**View argument.** `canon/A1-IDENTITY.md`'s POSE section: *"only the front view shows the
face frontally."* Mechanised as binary — face-bearing content (eyes N9, mouth/smile N10,
the `style_face` legal clause) is emitted only at yaw 0. A1's canon declares **no view
scopes** (`scopes.views` is `{}`), so `canon_gate.check_prompt(scope="view:N")` ANDONs for
any N on this subject; Gate 1 is therefore only exercised, and only claimed to hold, at
the front view — the only view Stage 2 ever spends against. The rear-view can-fail leg
checks the composed **text** directly rather than through the gate, and the tool's
docstring says so rather than overclaiming gate coverage it doesn't have.

**Tests.** T34 (`tests/test_t34_front_door_counts.py`) pins exact pytest collected-item
counts against 15 doc surfaces across 8 languages; any delta fails every pin
simultaneously, and full reconciliation needs regenerating 7 translated READMEs — outside
a Sonnet executor's authority (studio translation rule). Followed E59's exact precedent:
substantive coverage lives in `canon_compose.selftest()` (in-tool, ANDON-raising — front/
flat/consolidated all pass the gate; a rear-view compose demonstrably drops face-bearing
phrases and *nothing else*; the front view is confirmed to still carry them, so the leg
cannot pass by a composer that dropped face content everywhere; the anchor diff is
non-degenerate). `tests/test_t92_canon_router.py::test_t92_selftest_still_holds` extended
in place (+12 lines, 0 new test functions) to also run `canon_compose.py --selftest` and
assert its three headline strings.

**Measured counts, not asserted:** `pytest --collect-only -q` — **1339 tests collected
before AND after** (unchanged). T34 re-run standalone: **52/52 PASSED**. The canon-adjacent
suite (t87 canon_gate + t92 canon_router + t93 canon_worksheet) re-run: **40/40 PASSED**.

`python tools/canon_compose.py --selftest` — exit 0, first run:
```
selftest PASS  front/flat/consolidated gated  rear drops face  anchor in_both=21 canon_only=3
```

---

## Stage 1 — the anchor (spend: 0). COMPLETE. GATE 1 PASSED.

`python tools/canon_compose.py anchor --canon canon/a1.surfaces.json --recipe
canon/A1-RECIPE.json --view front`

Composed (front, `grouped`):
> A young archivist in his 20s. Head facing straight ahead, arms slightly away from the
> body, hands empty and open and feet planted and visible. Plain warm pale-grey studio
> backdrop. No weapons, no held objects and nothing crossing the body silhouette.
> Painterly digital art with visible brushwork, rich saturated palette, crisp readable
> facial features and realistic stylized proportions. Plum long-vest with fine gold
> embroidery and a cream high-collared shirt, an umber sash, slim dark-green trousers and
> polished brown shoes; olive skin, tousled dark curls, ink-stained fingertips, curious
> brown eyes and a slight smile.

**Gate 1: `ok=True missing=[] forbidden=[] unlicensed=[]`.** PASSED.

**Three-way diff — not a byte match, not tuned toward one; reuses `canon_gate.licensed_
phrases` / `_present` / `unlicensed_residue` directly rather than a bespoke text diff.**

- **In both (21):** all 10 NAMED phrases, `frame_subject`, `style_paint`, `style_palette`,
  `style_face`, `stage_bg`, `stage_no_weapons`, `visible brushwork` (subsumed inside
  `style_paint`'s longer phrase), `realistic stylized proportions`.
- **Canon-only, raw instrument output (3), then corrected by hand-verification:** the raw
  `_present()` sweep reports `head facing straight ahead`, `no held objects`, `nothing
  crossing the body silhouette` as absent from the recipe text. **Two of these three are a
  measured negation-window artifact**, not a real absence: `_present()`'s 24-char
  look-back for `no|not|without|lacking` fires on an **adjacent** "no X" phrase — searching
  for `no held objects` in `"...features, no weapons, no held objects, nothing crossing..."`
  finds it at a position whose 24-char window is `"l features, no weapons, "`, which
  contains "no" from the *neighbouring* clause and is misread as a negator. Confirmed by
  direct substring check: both phrases **are** textually present in the recipe. The one
  **genuine** canon-only phrase is `head facing straight ahead` — correctly so, since it is
  the Director's 2026-08-18 post-hoc ruling and could not have been in the 2026-08-17
  recipe.

  > ### ⚠ Advisor correction appended 2026-08-18, after the fold — the instrument was
  > repaired and these numbers moved.
  >
  > **The 21/3 above was accurate when measured and is now stale.** The seat diagnosed the
  > artifact correctly and hand-corrected around it; the underlying defect has since been
  > **fixed in the instrument** rather than in the reading. `canon_gate._present` now cuts
  > its negation look-back at the nearest clause boundary (`_neg_window`, `CLAUSE_END`),
  > authored in a concurrent session the Director started from a flagged chip — **not this
  > seat's work and not the advisor's.**
  >
  > **Re-measured against the repaired instrument: `in_both=23`, `canon_only=1`.** The two
  > phantom absences are gone and the single genuine canon-only phrase — `head facing
  > straight ahead` — is exactly the one the seat identified by hand. **The hand-correction
  > was right, and it is no longer needed.**
  >
  > The repair carries a declared trade-off rather than a hidden one: a *distributive*
  > negator (*"without a sword, a shield"*) now reads its second item as present. That form
  > was never reliably handled — the flat window only reached it when the intervening items
  > happened to fit inside 24 characters, which is a property of item lengths rather than a
  > design — and the direction kept is the one a gate cares about: the old failure was a
  > false **refusal** of a prompt carrying its required phrase; the new one is a false accept
  > of a form the corpus does not contain. It is asserted in the test and stated in the
  > docstring.
  >
  > **No live gate verdict moved.** `check_prompt` was run over every `canon/*.surfaces.json`
  > against every recipe text before and after: byte-identical results. A1's only refusal
  > remains `stage_head_forward`, which is a genuine absence.
  >
  > Appended rather than rewritten, per this repo's rule that a correction is more useful
  > than the original — and flagged for this ruling by the chip session itself, which
  > declined to edit another seat's report and routed the call here instead. That was the
  > right boundary.
- **Recipe-only (canon debt, reported not fixed — "a canon edit is the Director's"):** one
  residue span, `"full body character concept single figure centered standing relaxed
  pose facing camera soft even studio lighting warm colour shadows over"`. Decomposes into:
  framing/staging boilerplate never captured as a legal clause (*"full-body character
  concept, single figure centered"*); the view-specific pose phrase A1-IDENTITY.md already
  documents as a **deliberate** exclusion (*"standing in a relaxed A-pose facing the
  camera"* — "facing the camera" must never enter a non-front prompt); a lighting
  description with no legal-clause home (*"soft even studio lighting with warm colour in
  the shadows"*); and the illegal connector `"over"`. Not touched.

**Content divergence from the historical E58 flat string, disclosed:** `canon_compose`'s
`flat` form includes `realistic stylized proportions` (mesh-provenance, licensed) in all
three composed forms so that Arms P/L/G differ **only** in joining, not in content set —
the literal historical E58/`profiles/a1.json` string omits this phrase. This is a
deliberate choice for a clean single-variable comparison across the three composer forms,
not a reproduction of the frozen E58 bytes.

---

## Predictions — registered before Stage 2

**A disclosed process gap, not backfilled.** The charter requires: *"The seat states its
own before Stage 2, blind status disclosed, each inside the interval its instrument can
return."* This executor did **not** write down explicit numeric predictions between
finishing Stage 1 and submitting Stage 2. Writing predictions now, after Stage 3's results
are in hand, would not be a prediction — it would be dressed-up hindsight, which this
repo's own record exists to catch, not commit. This gap is reported plainly rather than
patched.

The charter's own pre-registered prediction, from the advisor, stands as the arc's one
falsifiable prior: *"Arm P beats Arm L on colour landing, and Arm R beats or ties Arm P...
If Arm P loses to Arm R, the composer is not adopted."* Stage 3's numbers are reported
against it below, as numbers — not as a verdict on the prediction, which is the advisor's
call to render, not this executor's.

---

## Stage 2 — the spend (12/12). COMPLETE. GATE 2 PASSED.

**Third seed pinned 2026-08-18, before any Stage 2 artifact existed: 314159** (digits of
pi — arbitrary, documented). The three seeds: 106 (A1's own reference seed), 770700
(studio shared twin-generation seed, E08 lineage), 314159 (this pin).

**Graphs.** Built from `facet_E58/reference/A1_full_graph.json`, the actual runnable
txt2img graph that produced `canon/A1_reference.png` (not `A1-RECIPE.json`, which is a
machine-extracted *summary*, not a graph) — loaded verbatim, only three fields edited per
graph: node `238:227` positive text, node `238:230.seed`, node `60.filename_prefix`.
Everything else (model, sampler, scheduler, steps, cfg, negative text, latent size
1140×1472, the LoRA-off switch) stays byte-identical to the base, confirmed by an explicit
per-graph delta check (`assert` over every node not in the three named ids) in
`facet_E60/stage2/build_graphs.py`.

- **Arm R** — the recipe's `positive_text`, verbatim. Checked against `canon_gate` for the
  record (not gated — not composer output): **EXPECTED FAILURE**, printed not raised
  (`missing=[stage_head_forward]`, `unlicensed=["full body character concept ... over"]`),
  matching Stage 1's own anchor finding exactly.
- **Arms P/L/G** — `canon_compose.compose(view="front", form=...)`. All three:
  `canon_gate.require_canon(subject="A1")` → **`ok=True` for every one**, checked once per
  arm (text is seed-independent) before any graph was written.

Local link-topology check (E04 G7 law — a dry_run PASS does not by itself prove link
sanity; self-links, dangling targets, orphan reachability from SaveImage) on all 12 built
graphs: **PASS, nodes=19 links=22 reachable=19 orphans=0, every time.**

**Pre-submission checks, both free, both run before the batch:**
- `dry_run` on the shared graph shape → `status=validated, warnings=[]`.
- `estimate_credits` on the same graph → `"0 credits — no paid API nodes found"` — the
  same disclosed **estimator limitation** E58/E59 already named: this workflow bills GPU
  time, which the estimator does not price, not a claim of free generation.

**Submission: one `submit_batch` call, 12 items, `client_os=windows`.**
`submitted=12 failed=[]`. batch_id and all 12 job_ids recorded in
`E:\AI\training\facet_E60\handoff.md` immediately after submission, before any wait —
"on-disk state is the record."

**Completion:** all 12/12 terminal, **0 failed**, via repeated `wait_for_batch` polling.
Downloaded to `E:\AI\training\facet_E60\gen\` — every one of the 12 files **1136×1472
RGB**, matching `A1_reference.png`'s own dimensions exactly (VAE rounding is consistent
across the whole batch, so `A1-palette.json`'s pixel region boxes transfer without
rescaling).

**GATE 2 (charter: "Arm R failing to reproduce `canon/A1_reference.png` at seed 106 HALTS
THE ARC"). PASSED.** `armR_seed106.png` vs `canon/A1_reference.png`, compared **pixel by
pixel**, not by file hash — this repo's own law: *"A PNG hash mismatch is not evidence a
render changed."* **0 of 1,672,192 pixels differ in any channel (0.000000%), max channel
delta 0, mean abs channel delta 0.0 — pixel-identical.** File bytes differ (sha256
`9417cd64...` vs `92d9cbcc...`) — PNG encoder metadata only, the documented false-halt
pattern this repo has already named twice. The venue re-anchor holds.

**Spend, measured (not the estimator's "0 credits" reading).** Per-job GPU seconds from
`get_billing_activity` (job-scoped, unlike the workspace-wide usage report, which cannot
isolate this arc's spend from concurrent activity): the 12 jobs summed to **~552.9
GPU-seconds (~9.2 GPU-minutes) on `rtx_pro_6000`**, ranging 47.98–55.74 s per job except
`armR_seed106` at **1.73 s** — a measured curiosity (armR/106 is a byte-for-byte resubmit
of a previously-generated graph+seed pair; whether Comfy Cloud's cache explains the near-
zero compute time is not something this arc's instruments can confirm, and is reported as
an observation, not a claim). Comfy Cloud does not report per-job dollar cost (tool's own
message: *"Per-job DOLLAR cost is not something Comfy Cloud reports today — pricing is
rated at invoice level"*); dollar figures live at `cloud.comfy.org → settings → workspace`.

---

## Stage 3 — measurement (spend: 0). COMPLETE.

`facet_E60/stage3/measure_arms.py` — region boxes read **live** from
`canon/A1-palette.json` (never retyped); `canon_gate.to_lab` (byte-identical to
`derive_a1_palette.py`'s own copy) for the Lab transform; the same circular-hue-mean /
chroma-floor (12.0) methodology `derive_a1_palette.py` used for the reference itself,
ported not reinvented; `canon_gate.verify_regions`'s established `DE_LANDED=2.3` /
`DE_MISSED=10.0` thresholds for the landed/missed/uncertain classification. No VLM judges
a colour anywhere in this arc (charter finding 6).

**All 10 NAMED elements are structurally present in every one of the 12 generations** —
confirmed, not assumed: zero region rows returned `px=0`, and every material's pixel count
is identical across all 12 files (the region boxes are geometrically fixed and every file
shares one canvas size).

**Two disclosed limits of this measurement, stated before the numbers, not after:**
1. Region boxes were hand-placed **once**, on the reference's own pose. They are **not**
   re-placed per generated image. Seed/arm variation can shift the figure enough that a
   box samples the wrong material — Stage 4's crop panel shows this happening.
2. Raw dE-vs-reference is **not** a clean "in-band" signal by itself. Measured directly:
   **Arm R at seeds 770700/314159 — the verbatim recipe text, unchanged — already reads
   `missed` (dE 7–36) on most materials**, because dE conflates ordinary seed-to-seed
   lighting/exposure variance with genuine material-family shifts. Circular hue delta from
   the reference (gated by the same 12.0 chroma floor — a reading below floor is flagged
   `[LOW-CHROMA: hue unreliable]` and should not be read as a colour) separates these two
   sources far better, and is reported alongside dE for exactly that reason.

### Per-generation material verdicts (dE-vs-reference; `armR_seed106` is the pixel-identical
anchor and reads 10/10 landed by construction — degenerate, not informative)

| image | landed | missed | uncertain |
|---|---|---|---|
| armR_seed106 | 10 | 0 | 0 *(pixel-identical to reference; see Gate 2)* |
| armR_seed770700 | 0 | 6 | 4 |
| armR_seed314159 | 0 | 9 | 1 |
| armP_seed106 | 0 | 5 | 5 |
| armP_seed770700 | 0 | 9 | 1 |
| armP_seed314159 | 0 | 10 | 0 |
| armL_seed106 | 0 | 8 | 2 |
| armL_seed770700 | 0 | 10 | 0 |
| armL_seed314159 | 0 | 10 | 0 |
| armG_seed106 | 0 | 6 | 4 |
| armG_seed770700 | 0 | 9 | 1 |
| armG_seed314159 | 0 | 10 | 0 |

Full per-material dE/hue/chroma table for all 12 × 10 = 120 rows:
`facet_E60/stage3/hue_delta_rows.json` (and the console table in
`facet_E60/stage3/hue_delta_analysis.py`'s own run).

### Circular hue delta from reference, mean/median per arm

Seeds 770700 + 314159 only (the two seeds every arm shares with no self-comparison; Arm R
carries no pixel-identical row here):

| arm | n | mean Δhue° | median Δhue° |
|---|---|---|---|
| R | 20 | 6.24 | 4.95 |
| P | 20 | 8.70 | 4.55 |
| L | 20 | 8.35 | 6.35 |
| G | 20 | 8.12 | 3.95 |

### The one large, chroma-valid signal: N2 (cream high-collared shirt)

| arm | seed | dE | hue measured | hue Δ from ref (77.5°) | chroma (meas/ref) |
|---|---|---|---|---|---|
| R | 770700 | 13.6 | 75.6 | 1.9 | 24.4 / 23.3 |
| R | 314159 | 14.2 | 74.5 | 3.0 | 26.1 / 23.3 |
| P | 106 | 43.2 | 13.8 | **63.7** | 14.2 / 23.3 |
| P | 770700 | 45.5 | 10.7 | **66.8** | 13.3 / 23.3 |
| P | 314159 | 16.1 | 80.2 | 2.7 | 22.5 / 23.3 |
| L | 106 | 17.9 | 85.5 | 8.0 | 18.4 / 23.3 |
| L | 770700 | 18.5 | 82.4 | 4.9 | 22.2 / 23.3 |
| L | 314159 | 18.5 | 84.2 | 6.7 | 20.3 / 23.3 |
| G | 106 | 42.6 | 13.9 | **63.6** | 14.9 / 23.3 |
| G | 770700 | 45.2 | 11.8 | **65.7** | 13.8 / 23.3 |
| G | 314159 | 15.9 | 80.6 | 3.1 | 22.6 / 23.3 |

Every chroma reading above clears the 12.0 floor — none of these hue readings are floor
artifacts. **Arm P and Arm G, at seeds 106 and 770700 only, read a hue ~64–67° from the
reference's cream (a shift toward warmer, more saturated territory); Arm P and Arm G at
seed 314159, and Arm L and Arm R at every seed, read within 9° of the reference.**

**Stage 4's crop panel (below) shows what the number is reading.** In those four cells
(P/106, P/770700, G/106, G/770700), the vest/coat renders full-sleeved, covering the arm
to the wrist; the reference, Arm R, and Arm L all render the vest sleeveless with the
cream shirt sleeve visible from roughly the elbow. At seed 314159 all four arms render the
vest sleeveless. **Two explanations are consistent with the measured pattern and this
arc's instruments do not distinguish them:**
(a) the composed grouped-prose form — shared by Arms P and G, which differ from each other
only in how garments are joined — biases the model toward a different vest silhouette than
the flat list or the original recipe's "over"-joined phrasing; or
(b) the fixed `sleeve_L` region box, placed once on the reference's own sleeve position,
samples vest fabric rather than shirt fabric whenever the vest renders full-sleeved,
independent of any colour-attribute effect on the shirt token itself.
Distinguishing them would need a fresh per-image region placement or segmentation, which
this arc did not build. Both readings are worth naming against the charter's own research
grounding: (a) is the shape finding 2 (Zarei et al., attribute-embedding leak between
grammatically bound entities) predicts; (b) is a measurement-methodology artifact this
report's own Stage 3 preamble flagged as a limit before the number was seen.

---

## Stage 4 — the sheet

- `facet_E60/stage4/E60_director_sheet.png` — reference | Arm R | Arm P | Arm L | Arm G,
  one row per seed, full body, labels only (no ranking, no quality language).
- `facet_E60/stage4/E60_shirt_crop_panel.png` — the N2 region crop (expanded), same
  layout, each cell labeled with its measured dE and hue delta only.
- Full-size source PNGs: `facet_E60/gen/arm{R,P,L,G}_seed{106,770700,314159}.png` (12
  files, 1136×1472 each).

---

## Premises vs measured

| premise | status |
|---|---|
| "over" (the recipe's garment connector) fails `canon_gate`'s reverse check | measured true — confirmed via Stage 0's own dry-composition and Stage 1's residue span |
| A1's canon has no declared view scopes, so Gate 1 cannot be exercised at non-front views | measured true — read directly from `canon/a1.surfaces.json`'s `scopes.views: {}` |
| `facet_E58/reference/A1_full_graph.json` is the graph that produced the reference | measured true via Gate 2 (pixel-identical reproduction at seed 106) |
| Region boxes transfer from the reference to all 12 generations without rescaling | measured true — every generated file is 1136×1472, matching the reference exactly |
| Raw dE-vs-reference is a clean "in-band" signal | measured **false** — Arm R at non-anchor seeds already reads mostly "missed" on unchanged text |
| The charter's own prediction ("Arm P beats Arm L on colour landing, Arm R beats or ties Arm P") | reported as numbers above (hue-delta table, N2 table); not adjudicated by this executor |

## Gates summary

| gate | result | evidence |
|---|---|---|
| Gate 1 — composed front-view prompt passes `canon_gate` | **PASSED** | `ok=True missing=[] forbidden=[] unlicensed=[]`, Stage 1 |
| Gate 2 — Arm R seed 106 reproduces `canon/A1_reference.png` | **PASSED** | 0/1,672,192 pixels differ, max channel delta 0, Stage 2 |

No gate fired. No gate was skipped.

## Spend, final tally

12/12 generations spent, ceiling reached exactly, no further submission made or intended.
~552.9 GPU-seconds measured across the 12 jobs (`get_billing_activity`, job-scoped).
Dollar cost is not exposed per-job by Comfy Cloud; workspace invoices live at
`cloud.comfy.org`.

## Verification re-run at close

- `pytest --collect-only -q`: **1339 tests collected** (unchanged from Stage 0's baseline).
- `tests/test_t34_front_door_counts.py`: **52/52 PASSED**.
- `tests/test_t87_canon_gate.py` + `test_t92_canon_router.py` + `test_t93_canon_worksheet.py`:
  **40/40 PASSED**.
- `python tools/canon_compose.py --selftest`: **exit 0**.
- Full untargeted suite (`pytest -q`, no marker filter, all tiers including `artifacts`):
  **1 failed, 1338 passed, 8 warnings, 906.21s**.

### The one full-suite failure, root-caused, not fixed

`tests/test_t24_index_parsers.py::test_t24_paid_for_by_reads_every_arc_the_record_has`.
Its own assertion names the cause exactly: `AssertionError: laws.paid_for_by cannot read 1
of the record's own arcs... : E60` / `assert not ['E60']`. Root-caused (not guessed):
`facet_index_mod.PAID_RE` — the regex this leg checks can recognise "paid for by EXX" for
every arc number up to the record's own highest — resolves to
`\b(E0[1-9]|E[1-4]\d|E5[0-9])\b`, exported from `tools/facet_index.py`'s `import
record_index`, and the pattern itself is compiled at
`E:\AI\record-index\record_index\conventions.py:162` from a `laws.paid_for_by` config
value. **This is bounded at E59 and stops one short of E60 by construction** — `E5[0-9]`
covers the 50s decade; there is no `E6[0-9]` term. The leg's own `_record_arc_span` helper
computes "the highest experiment number the record itself carries" by parsing the
filesystem, so **any** E60-numbered file in `docs/experiments/` — this report or the
advisor's own kickoff — pushes the span to 60 and the leg fires, regardless of content.

**Not fixed, on purpose.** The regex lives in `record_index`, a separately installed
package (`E:\AI\record-index\`) outside this repo's own `tools/` tree and this arc's
charter — editing it is a package change with its own release lifecycle, not a
composer-arc edit. This is also **not a new class of finding**: E59's own handoff records
the identical disposition for this identical test file — *"T24 matches E34's own recorded
precedent exactly (report don't fix, advisor's call)"* — reached independently here by
root-causing the assertion rather than by citing that precedent first. Every arc that
crosses into a new numeric decade (E49→E50 before it, E59→E60 here) will fire this leg
until `record_index`'s bound is widened; that is the advisor's call, not this executor's.

## git status --short (verbatim, current — the snapshot at this session's own close)

```
 M tests/test_t92_canon_router.py
?? docs/experiments/E60-composer-kickoff.md
?? docs/experiments/E60-composer-report.md
?? tools/canon_compose.py
```

`canon/A1-RECIPE.json`, `canon/A1-palette.json`, `canon/a1.surfaces.json`,
`canon/A1_reference.png` — **untouched**. No canon edit was made; the anchor's canon debt
is reported, not repaired, per the charter's own instruction.

**A concurrent session touched `tools/canon_gate.py` and `tests/test_t87_canon_gate.py`
during this one, not this executor — observed transiently, gone by the close-of-session
snapshot above, reported because it happened, not because it is this arc's work.**
Mid-session, `git status --short` briefly showed both files modified; `git diff` showed a
fix for exactly the negation-window finding this report's own Stage 1 section names — its
comments cited "E60 Stage 1, reproduced" verbatim — cutting `_present()`'s look-back at
the nearest clause boundary instead of a flat 24-character window, plus a regression test
extended into the already-collected `test_t87_negation_does_not_count_as_coverage`
(collect-only re-confirmed **1339**, unchanged, while the diff was present). This
executor had separately flagged the identical finding via `spawn_task` (`task_54aed787`,
"Fix negation-window false-negative in canon_gate._present"); attempting to withdraw it
at close returned *"already started by the user"* — the Director started that chip
himself during this session. By the time of the final status check above, both files no
longer appeared as modified — committed or stashed by that other session, not determined
here, since this executor neither touched those files nor the mechanism that changed
their status, and asserting which without checking would be exactly the kind of
unmeasured claim this repo's own rules warn against. Full diff text, as observed, stays
in the session transcript rather than being reproduced twice in this file. This session's
own full-suite tally (see above) reflects whichever version of `canon_gate.py` `pytest`
had already imported into `sys.modules` before that edit reached disk — Python does not
hot-reload a module underneath a running process — so the tally is internally consistent
even though the file it measured briefly differed from the file sitting on disk at this
report's own close.

**Unstable at close, not chased further:** re-checked three times in this session's
final minutes, `tools/canon_gate.py` and `tests/test_t87_canon_gate.py`'s git status
fluctuated between modified and clean — a concurrent session actively iterating in this
same shared tree, not a single edit this report can pin to one final diff. The right
response to a target that will not hold still is the one this repo's own advisor practice
already uses: read git status fresh at fold time rather than trust a prior snapshot for
those two files. This executor's own four surfaces — `canon_compose.py`, this report, the
`test_t92_canon_router.py` edit, and the advisor's pre-existing kickoff file — held stable
throughout and are what this arc itself delivers.

## Working tree — file map

- Report: `E:\AI\facet\docs\experiments\E60-composer-report.md` (this file)
- Handoff: `E:\AI\training\facet_E60\handoff.md`
- New tool: `E:\AI\facet\tools\canon_compose.py`
- Modified test: `E:\AI\facet\tests\test_t92_canon_router.py`
- Stage 2: `facet_E60\stage2\build_graphs.py`, `graphs\graph_{R,P,L,G}_{106,770700,314159}.json`,
  `graphs\_manifest.json`, `batch_items.json`, `download_outputs.py`
- Stage 3: `facet_E60\stage3\measure_arms.py`, `measure_report.json`,
  `hue_delta_analysis.py`, `hue_delta_rows.json`
- Stage 4: `facet_E60\stage4\build_sheet.py`, `E60_director_sheet.png`,
  `E60_shirt_crop_panel.png`
- Generations: `facet_E60\gen\arm{R,P,L,G}_seed{106,770700,314159}.png` (12 files),
  `_download_manifest.json`
