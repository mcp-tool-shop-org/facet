# E56 — report: is there an honest check for the defect class that decides acceptance?

**Executor seat (Opus), 2026-08-17. Spec:
[E56-wrong-material-check-kickoff.md](E56-wrong-material-check-kickoff.md).**
Working tree `E:\AI\training\facet_E56\`. Uncommitted. Zero spend; no GPU, no cloud, no
generation.

**Result in one line: GATE A FIRED, and the reason is that the asset the Director accepted
and the asset he called defective on this class are the same file.** No check was built or
scored. What was measured instead is label-independent: the canon's spatial binding, and
why the nearest prior-art detector cannot answer this question.

---

## 1. Gate A — FIRED. The label census, with a locator per row.

**Only two subjects in the repo carry a per-surface material declaration**:
`canon/w3.surfaces.json` and `canon/longsword.surfaces.json`. The longsword has no tree
under `E:\AI\training\` — [subjects.md:259](../handbook/subjects.md), *"Every E14 artifact
is citable-only"*. So *is this surface wearing the wrong declared material* is answerable
on exactly **one** subject: W3.

W3's Director verdicts on this class. All three have locators; all artifacts are on disk.

| id | artifact | verdict | date | locator |
|---|---|---|---|---|
| **N1** | `facet_E06\C1\renders\flat_0..7.png` | REJECTED — *"The images don't look good."*, and asked which defect drove it, *"all of it — the asset is not close"*. Regions at his zoom: the blade wears skin tones in large blocks; boot and thigh carry scattered gold and green; the forearm has no material identity | 2026-08-05 | [E07-ruling-gate1.md:3](E07-ruling-gate1.md), `:37` |
| **P1** | `facet_E08\ARMB\out\renders_flat\final_0..7.png` | ACCEPTED — *"Very good!!! I'm so happy right now."* And on this class specifically: *"the blade that wore skin tones at E07 reads as steel with a gold crossguard"* | 2026-08-04 | [E08-ruling-gate0.md:2282](E08-ruling-gate0.md) (Amendment 35) |
| **N2** | **the same file as P1** | *"W3 is far from perfect and needs a serious polish."* | 2026-08-16 | [E39-w3-polish-kickoff.md:12](E39-w3-polish-kickoff.md) |

**negative class = 2 · positive class = 1 · and N2 is P1.**

Gate A halts when a class has fewer than two members. **The positive class has one member,
and that member is also a member of the negative class.** Twelve days apart, one artifact,
both labels. An artifact-level accept/reject discriminator on this class would have to be
silent on W3 and fire on W3.

**No other on-disk accepted asset can join the positive class.** `facet_E34`'s performer is
accepted at the Director's eye, and it has **no `.surfaces.json`** — the wrong-material
predicate is undefined for it. That is the *check every member HAS the property* law doing
its job rather than a shortage of assets.

### 1a. The spec's own framing, corrected

The spec reads *"**E08 Gate 1** — the accepted asset (`facet_E08\ARMB\`). The Director's
acceptance is what makes it the positive class."* That is right, and `facet_E08\ARMB\` **is
W3**, the asset of the 2026-08-16 sentence. The spec treats them as separate label sources
in separate bullets. They are one file.

### 1b. A second label authority exists, and it is reported separately rather than merged

The E08 Arm-B twins carry **specification** rejections — recorded, with locators, and not
mine — and both rejected rolls survive beside their replacements:

| class | members | locator |
|---|---|---|
| rejected | `facet_E08\ARMB\twins\twin_2_REJECTED_seed770700.png`, `twin_6_REJECTED_seed770700.png` | [E08-armB-reroll-report.md](E08-armB-reroll-report.md); `tools/palette_gate.py` header |
| accepted | `twin_0..7.png` (8) | same |

This authority has two members in each class. **It is a different authority from the
Director's and the two are not pooled here.** Gate A's heading is *"the labels are the
Director's, not yours"*; a specification verdict is neither. It is recorded so a later seat
can decide whether it is admissible, and the halt stands on the Director census.

### 1c. Transcription chain of the "named regions", stated honestly

The Director's quoted words on 2026-08-16 are **two sentences** — the polish sentence above
and *"do a study-swarm instead of guessing."* The six-bullet enumeration that follows in
[E39-w3-polish-kickoff.md:19-24](E39-w3-polish-kickoff.md) (gold on tunic / skirt / boot
tops; gold and rust-brown on the blade, *"the largest single offence"*; green down the sword
grip; brown-green on hands and right bracer) is introduced by *"The advisor has walked all
of it at native size at this seat"* — **it is the advisor's enumeration under the Director's
sentence.** The seven pixel boxes were then drawn by the E39 seat *"by reading the render at
native size"* — a third hand.

Two inherited characterisations do not survive being opened:

- `facet_E39/gate0_sheets.py:17-18` — *"Names are HIS words from the dispatch."* True of the
  dispatch; the dispatch's bullets are the advisor's walk.
- `facet_E40_C/c0_measure.py:17` — *"the DIRECTOR-VERIFIED crop boxes"*. **Not supported at
  source.** Nothing records the Director verifying those boxes.

---

## 2. What was enumerated before anything was built

The law that has fired three times in this repo in one session. Everything below was read
in full before a line of new code.

| resource | what it asks | why it is not this check |
|---|---|---|
| `tools/palette_gate.py` | is any colour outside the declared palette | **States its own gap in its header:** *"it tests COLOUR, not PLACEMENT. Gold on the boots passes every band while being flatly wrong."* |
| `facet_E39/detector.py` | dE from the image's own local median (window 41 or 121), 8-connected regions ≥ floor | *is this region unusual* — the proxy the spec forbids. *"No provenance is read in this file."* |
| `facet_E39/gate0_recall.py` | pixel within dE 20 of material M **and** local median beyond dE 30 of M | nearest prior art. Placement supplied by **7 hand-drawn boxes**, not by canon. Section 4 measures what its construction costs it. |
| `facet_E40_B/g_material_landing.py` + `material_centres.json` | nearest named material centre in Lab | the **colour half**, done and frozen. No placement half. |
| `facet_E40_C/c0_measure.py` | per-view cosine facing weight | geometry, not material. |
| `tools/evidence.py` (+ `tools/s3_sheet.py`) | column sheets with region rows and sha256 provenance | **reused for the terminus.** No eighth sheet builder was written. |
| `tools/verify/montage.py` | contact sheet at scale 0.5 | not the Director's-zoom form; not used. |

`grep -rln "out of place\|wrong.material" tools/` returns **only** `palette_gate.py` and
`twin_despeckle.py`. **Nothing in `tools/` answers this question.**

---

## 3. P3 — how much of the figure can be attributed to a named canon surface today

Script `p3_binding.py`; JSON `p3_binding.json`.

### 3a. From canon alone: **0.00%**

`canon/w3.surfaces.json` declares 27 surfaces (24 prompt-relevant, RATIFIED by the Director
2026-08-17) and 8 joints. **`scopes.views` is `{}` and `scopes.strokes` is `{}`.** The canon
binds zero pixels to zero surfaces. `surface_at(p)` is undefined for 100.00% of every view.

### 3b. From `tools/s3_sheet_regions.json` — 10 boxes, 3 of 8 views, self-labelled *"PROPOSALS. Not a ruling."*

| view | figure px | strict px | strict % | lenient px | lenient % |
|---|---|---|---|---|---|
| y+000_e+00 | 145,202 | 27,672 | **19.06%** | 82,123 | 56.56% |
| y+045_e+00 | 148,709 | 27,976 | **18.81%** | 72,740 | 48.91% |
| y+090_e+00 | 89,942 | 0 | 0.00% | 0 | 0.00% |
| y+135_e+00 | 119,964 | 0 | 0.00% | 0 | 0.00% |
| y+180_e+00 | 145,771 | 0 | 0.00% | 0 | 0.00% |
| y+225_e+00 | 149,170 | 0 | 0.00% | 0 | 0.00% |
| y+270_e+00 | 90,044 | 0 | 0.00% | 0 | 0.00% |
| y+315_e+00 | 119,595 | 24,484 | **20.47%** | 39,891 | 33.36% |
| **pooled (8)** | **1,008,397** | **80,132** | **7.95%** | 194,754 | 19.31% |

**STRICT** = the region name equals a canon surface `id` exactly. **LENIENT** = plus a
rename table *this script wrote* (`tunic`→`torso`, `skirt`→`kilt`, `boot_tops`→`boot_L/R`).
Supplying that table is providing the binding, not measuring it, so **7.95% is the honest
headline** and 19.31% is what it would be if someone ruled the renames.

**Both numbers are ceilings, not measurements.** The boxes are axis-aligned rectangles, not
surface masks: a box over the tunic also contains arm, rim and background-adjacent pixels.
The true attributable fraction is lower by however much of each box is not its named
surface, and nothing in the repo records that.

### 3c. ⚠ A premise in the spec is wrong

The spec states *"one region name in `tools/s3_sheet_regions.json` is the pre-rename
`skirt`."* Measured: **three of the five distinct region names have no canon surface id** —
`skirt`, **`tunic`** and **`boot_tops`**. Only `blade` and `grip` resolve. `boot_tops`
matches the *joint* ids `boot_top_L/R`, which are not surfaces.

Checked in the reverse direction too: **one id referenced inside `canon/w3.surfaces.json`
is not a surface in that file** — ratification entry Q3 lists `"skirt"` in its `surfaces`
array where the surface is `kilt`.

### 3d. The colour half is also only part-built

The canon carries **21 distinct occupants, 18 of them prompt-provenance**. Frozen Lab
centres exist for **four** material families (gold, green, skin, leather —
`facet_E40_B/material_centres.json`). There is **no centre for steel, for the dark red
kilt, for the dark boots, or for the red beard**. Consequence, visible on the sheet: the
material panel is a forced choice among four, so the steel blade is assigned *green* and the
dark-red kilt *leather*. A material map built on this centre set cannot be read as a
material identification outside those four families.

---

## 4. Why the nearest prior art cannot answer this — measured, label-free

Gate A fired, so nothing below scores a check against a label set. These are properties of
an instrument and of the artifact's geometry, and they hold whatever the verdicts are.

### 4a. Synthetic: the local-median family never sees an interior

`p2_window_blindness.py`. Detector **imported** from `facet_E39/detector.py`, not
reimplemented. A square of gold on a field of green, 512×512, whole frame figure, noiseless
— the most favourable input the detector can be given. The two materials are **dE 66.53**
apart, so any blindness below is not a colour failure.

Calibration first, both directions: **definitely-no returns 0 flagged px** at both windows
and both thresholds; **definitely-yes (blob ≪ window) returns 100.00% recall**.

| window | threshold | recall at width ≤ window/2 | recall at width ≥ 2×window | **interior recall, every row** |
|---|---|---|---|---|
| 41 | dE>12 | 100.0% | 2.6–14.8% | **0.00%** |
| 41 | dE>18 | 100.0% | 1.1–10.8% | **0.00%** |
| 121 | dE>12 | 100.0% | 6.5–11.4% | **0.00%** |
| 121 | dE>18 | 100.0% | 6.1–10.1% | **0.00%** |

Interior = pixels whose entire window lies inside the blob. It is **exactly zero** in every
row where an interior exists — not low, zero. A larger window moves the failure to the
larger radius; it does not remove it. False positives *outside* the blob grow with blob size
(to 5,564 px), so the family also marks correct material on the far side of the boundary.

### 4b. On the real asset: the mechanism is field capture, not width

⚠ **My own predicted mechanism was indexed by the wrong quantity, and measuring caught it.**
I predicted interior recall would collapse *as region width approaches the window*. Measured
(`make_panels.py`, `defect_scale.json`), the largest same-material components inside the
seven named regions have **inscribed widths of 4.0–25.6 px — every one narrower than the
41 px window**. Width does not explain the observed recalls. Width was a geometric proxy;
this repo's own law says test the property.

The property, measured directly (`p2_median_capture.py`): **median capture** — an offending
pixel whose *own local median* has been dragged onto the offending material, so its dE from
its own reference is ~0 and it is invisible whatever the threshold.

| region (window 41) | offender px | captured | cap % | recall \| captured | recall \| NOT captured |
|---|---|---|---|---|---|
| blade_lower | 3,579 | 2,153 | 60.2% | **12.4%** | 79.5% |
| tunic_chest | 2,145 | 1,450 | 67.6% | **11.4%** | 70.9% |
| grip | 2,324 | 1,619 | 69.7% | **18.2%** | 79.9% |
| skirt | 744 | 0 | 0.0% | n/a | 92.6% |
| blade_upper | 183 | 0 | 0.0% | n/a | 97.3% |
| boot_tops | 1,740 | 1 | 0.1% | 0.0% | 31.2% |
| bracer_hand | 1,235 | 14 | 1.1% | 0.0% | 45.6% |
| **pooled** | **11,950** | **5,237** | **43.8%** | | |

Where the field is captured the detector reads 11–18%; where it is not, 71–80%. A
**4–7× gap on the same instrument, same view, same threshold.** At window 121 pooled
capture falls to 13.5% and uncaptured recall rises to 89–99% — so window size does move
this — but the grip stays 61.8% captured even at 121, and `bracer_hand` sits at 43–46%
uncaptured recall at **both** windows, which is a third failure mode this arc did not chase.

### 4c. Gate C direction on the prior art — and this is where it ends

`gate_bc_prior_art.txt`. The detector at `gate0_recall.py`'s own settings (window 41,
dE>18, floor 25) fires on **16.64% of the whole figure in 108 regions**.

| | region | figure px | flagged | density |
|---|---|---|---|---|
| named | blade_lower | 17,020 | 6,852 | 40.26% |
| named | grip | 10,102 | 2,702 | 26.75% |
| named | bracer_hand | 14,263 | 3,048 | 21.37% |
| named | blade_upper | 10,048 | 1,446 | 14.39% |
| named | skirt | 33,159 | 4,408 | 13.29% |
| named | tunic_chest | 29,501 | 3,496 | 11.85% |
| named | boot_tops | 26,415 | 1,996 | 7.56% |
| **control** | **left pauldron — gold on a pauldron, which is what canon declares** | 3,895 | 1,554 | **39.90%** |
| control | right pauldron — same, canon-correct | 1,799 | 319 | 17.73% |
| control | tunic body, clean — green on torso, canon-correct | 4,496 | 43 | 0.96% |

Named: 7.56–40.26%, mean 19.35%. Control: 0.96–39.90%, mean 14.65%.

**A surface wearing exactly the material canon declares for it fires at 39.90% — higher
than five of the seven regions the Director named, and level with the worst of them.** The
two distributions overlap end to end. The instrument responds to *material boundary density*,
and a pauldron has a great deal of boundary.

*(A fourth control box, `scalp_forehead`, contained **0 figure pixels** — the box missed the
head. Its 0.00% is quoted nowhere as evidence: a zero with no denominator is the "a check
that cannot fail" trap, and it is reported here only so the reader knows why three controls
are quoted and not four.)*

### 4d. Gates B and C would both have PASSED, and that is the methodological finding

Read literally against the prior-art detector: **Gate B passes** — it fires on all seven
named regions, none at zero. **Gate C passes** — the synthetic definitely-no returns 0 px,
so it is capable of not firing. **Both gates pass on an instrument that cannot tell a
correct pauldron from a defective blade.** A fire-here / silent-there gate pair is satisfied
by any boundary detector, because the named regions contain boundaries. What separates the
classes is not whether a check fires but whether its response *ranks* the defective above
the correct, and neither gate as written asks that.

---

## 5. Why no check was built, stated as reasoning rather than as a verdict

The predicate is two-place: `material_observed(p) != material_declared(surface_at(p))`.

- The **colour** term exists for 4 of the canon's material families and is frozen.
- The **placement** term, `surface_at(p)`, has exactly three possible sources today:
  1. **canon** — `scopes.views == {}`. Binds nothing.
  2. **the image's own local statistics** — section 4. Cannot rank a correct surface below a
     defective one, and its interior response is zero by construction.
  3. **hand-drawn boxes** — the boxes were drawn by reading the defect. A check whose
     acceptance test is those boxes reproduces what its author already noticed, which this
     repo rules is not an instrument.

There is no fourth source in the repo. Building a check on (3) and scoring it against a
positive class of one artifact — which is also the negative class — would produce a number
with nothing behind it.

**What would change this**, named so it is a route and not a shrug: a binding from mesh
faces (or atlas texels) to canon surface ids, filled once per subject and carried through
the existing raycast that already produces `prov_class` per view. That turns `scopes.views`
from `{}` into data, makes the predicate computable per pixel without any hand-drawn box,
and makes a positive and a negative class constructible *per surface* rather than per
artifact — which is the only level at which W3 can be in both classes without contradiction.
Filling it is a human walk, and the spec puts scope lists out of scope.

---

## 6. Predictions against outcomes

`predictions.md` was written before any scoring, with an explicit disclosure that P1 and P2
were **not blind** (the record had already been read) and P3 was close to blind (box file
read, no pixel measured).

| # | predicted | measured | verdict |
|---|---|---|---|
| P1a C1 verdict-exists | 8 of 8 | 8 | hit |
| P1a C2 locator | 7–8 | 8 | hit (top) |
| P1a C3 on-disk | 4–5 | 5 | hit (top) |
| P1a C4 this-class | 3–4 | **2** | **MISS, below band** |
| P1a join | 2–3 | 2 | hit (bottom) |
| P1a negative / positive | 1–2 / 1–2 | 2 / 1 | hit |
| P1a "Gate A fires", ~70% | fires | **fired** | hit |
| P1b spec-authority negative | exactly 2 | 2 | hit |
| P1b spec-authority positive | 6–8 | 8 | hit (top) |
| P2 refusal | no honest check | refused | hit |
| P2 **mechanism** | interior collapses as region **width** approaches the window | real components are 4.0–25.6 px, **all below** the 41 px window; the property is **field capture**, not width | **MISS on the index** |
| P3a strict, view 0 | 10–20% | 19.06% | hit |
| P3a strict, pooled 8 | 4–9% | 7.95% | hit |
| P3b lenient, view 0 | 35–55% | **56.56%** | **MISS, above band by 1.56 pts** |
| P3b lenient, pooled 8 | 13–22% | 19.31% | hit |
| P3b unresolved region names | 1 (following the spec) | **3** | **MISS — and the spec's premise was wrong** |
| P3b dangling ids inside canon | 0–2 beyond the 1 found by reading | 0 beyond | hit (bottom) |

**Four misses.** Two are worth carrying forward:

- **P2's mechanism** is the fourteenth arc in the unit/population family and a new member of
  it: the population was real, the members all had the property, the conjunction was fine —
  **the index was a geometric proxy for the property**. I reasoned about width because width
  is what the synthetic sweep varies, and the synthetic sweep varies width because a square
  is parameterised by its side. The instrument's failure is a function of *what fraction of
  a pixel's window is the offending material*, which width only approximates. The conclusion
  survived; the stated reason did not, and it was caught by measuring the property directly
  rather than by anyone noticing.
- **P3b's region-name count** is a miss I made **by trusting the dispatch**. The spec said
  one name was unresolved; I predicted one. Three are. That is the eighth-member law —
  *the premise inherited from your own dispatch* — with the executor doing exactly what the
  law says executors do, and a `grep` of five names against 27 ids would have overturned it
  in under a minute.

---

## 7. The sheet

**Built with `tools/evidence.py sheet`** — the existing layer, reusing `s3_sheet`'s crop and
row primitives. No eighth sheet builder was written. Columns are
**reference | asset | provenance | material | error(detector)**; a FULL row then one row per
named region, **ordered defects first** by measured offender mass; every consumed path
carries a sha256 in the sheet's own footer.

| form | path | size |
|---|---|---|
| native pixels (zoom 1) | `E:\AI\training\facet_E56\sheet_native\sheet_v00.png` | 3808 × 3032 |
| the Director's-zoom form (zoom 3, NEAREST — every native pixel preserved) | `E:\AI\training\facet_E56\sheet_zoom3\sheet_v00.png` | 11328 × 7840 |

Both carry `sheet_manifest.json` beside them. The panels are at
`facet_E56\panels\material_y+000_e+00.png` and `detector_y+000_e+00.png`.

**What the error column shows at a glance:** the detector traces material *boundaries* — the
blade's edges, the beard, the gold rims — rather than filling the regions the Director named.
That is section 4's thesis in a picture, and it is the same reading E07's ruling gave of the
high-pass family, one radius up.

**⚠ Read the `material` column with 3d in hand.** It is a forced choice among four frozen
centres; steel and dark-red cloth have none, so the blade renders green and the kilt brown.
It shows what a pixel *reads as* within four families, never whether it belongs.

---

## 8. Files

All under `E:\AI\training\facet_E56\` unless noted. Nothing was written to any other
`facet_E*` tree; `facet_E39` was imported from with `sys.dont_write_bytecode = True` so no
`__pycache__` was created there.

| file | what |
|---|---|
| `handoff.md` | written first, kept current |
| `predictions.md` | written before scoring, blindness disclosed |
| `p3_binding.py` / `.json` / `_stdout.txt` | section 3 |
| `p2_window_blindness.py` / `.json` / `_stdout.txt` | section 4a |
| `make_panels.py` / `defect_scale.json` / `_stdout.txt` | section 4b, panels, regions file |
| `p2_median_capture.py` / `.json` / `_stdout.txt` | section 4b |
| `gate_bc_prior_art.txt` | section 4c |
| `e56_regions.json` | the seven named boxes, defects-first |
| `sheet_native\`, `sheet_zoom3\`, `panels\` | section 7 |
| `docs/experiments/E56-wrong-material-check-report.md` | this file — the only write outside the tree |

**No repo tool was modified, so no test rides this commit.** No `t97` file was created:
the rule is that tests ride a commit that *touches tool code*, and this arc touched none.
`tools/canon_gate.py` and `tools/canon_worksheet.py` were not opened. **T34's count surfaces
(1319 / 1265 / 54) are untouched and this change-set assumes them unchanged**; nothing here
adds or removes a collected test.

**No public surface was touched.** But two implied corrections belong to the advisor, not to
this seat:

1. `docs/known-defects.md` and `docs/handbook/subjects.md` both carry W3 as the accepted
   asset and, separately, as the asset with named wrong-material regions. Neither says the
   two are the same object on the same date-line. Section 1 is the material for that fold.
2. `facet_E40_C/c0_measure.py`'s *"DIRECTOR-VERIFIED crop boxes"* is unsupported (§1c).
   That file is in a read-only tree; the correction is the advisor's to place.

---

## 9. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **2** | every label carries a `file:line` locator; every instrument is named by absolute path; the detector is *imported* from `facet_E39/detector.py` rather than copied, so its version is whatever that file is. Not 3: this seat pins no hash of its own inputs and records no model/prompt for itself. |
| ANDON_AUTHORITY | **3** | Gate A fired and the check-building branch stopped there; it was not routed around. Every new script raises `RuntimeError` on a violated precondition (`p3_binding.py` raises on a frame/box mismatch and on a `view_map` disagreement) — no bare `assert` in any of them. |
| NAMED_COMPENSATORS | **3** | writes confined to `E:\AI\training\facet_E56\` plus one uncommitted repo report. Compensator: delete the tree and `git checkout` the report. Owner: the advisor. No irreversible call; no commit; no `git add`. |
| DECOMPOSE_BY_SECRETS | **2** | census / binding / instrument-property / sheet are four separable scripts that share only frozen JSON inputs. Not 3: `make_panels.py` does two jobs (panels and the defect-scale measurement) because they share one expensive local-median pass. |
| UNCERTAINTY_GATED_HUMANS | **3** | no pass condition was invented. The halt is reported with its census rather than resolved by the seat; the two label authorities are kept separate for the Director and advisor to rule between; the terminus is a sheet for his eye at native pixels. |
| EXTERNAL_VERIFIER | **3** | the labels come from the Director — a different authority from the seat. Section 4c runs the prior-art detector at a surface **canon declares correct**, which is the verifier direction, and it is what ends the arc. The synthetic in 4a is generated independently of any artifact under test. |

---

## 10. Out of scope

- **Any generation.** Zero spend held; no GPU, no cloud, no re-bake.
- **`tools/canon_gate.py` and `tools/canon_worksheet.py`** — a second builder is live in
  them; neither was opened.
- **Filling `scopes.views`** — a human walk, and the route named in §5 rather than taken.
- **Whether W3 is acceptable.** The Director's, and only his.
- **Whether the specification authority (§1b) may stand in for the Director's on this class.**
  An advisor ruling, not a measurement.
- **`bracer_hand`'s third failure mode** (43–46% recall uncaptured at both windows) —
  measured and left open.
- **Re-running `palette_gate.py` on the twins.** Its numbers are recorded; re-deriving them
  while looking at what they would judge is not a measurement this seat should make.
- **The `facet_E50`–`E55` working trees** — not read, per the dispatch.
