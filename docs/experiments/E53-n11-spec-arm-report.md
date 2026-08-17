# E53 — did N11 land in the from-scratch SPEC arm? Report

**Executor session (Sonnet, dispatched background seat), 2026-08-17.** Answers
`docs/experiments/E53-compound-occupant-ruling.md`'s dispatch. Working tree
`E:\AI\training\facet_E53\` (predictions, scripts, crops, JSON receipts, `handoff.md`).
Zero spend — no generation, no cloud call, measurement only.

**Result up front, evidence below: N11 (the gold outer-forearm plate) is ABSENT in
SPEC, on the one forearm the front camera can assess.** The other forearm is not
assessable from this camera in any arm tested, canon included, and is reported as such
rather than forced to a verdict.

---

## 1. Enumeration, and how the image-to-prompt link was established (Gate A)

### What already existed, checked before anything was written

- `E:\AI\training\facet_E08\` subdirectories (complete listing): `A2, A2R, A3, A4,
  ANCHOR, armA, ARMB, ARMOUR, BG, BG2, BRACER, CONTRA, gate0, LOOK, N11, SPEC`, plus two
  top-level Comfy log files.
- `E:\AI\facet\tools\` — complete listing, 176 `.py` files (55 top-level + 102
  `diagnostics/` + 10 `verify/` + 9 `superseded/`; counts sum to 176, cross-checked
  against Glob's own truncation notice rather than trusted at 100/176). No generic
  pixel-bbox crop tool and no generic median-region-colour tool exists. `tools/verify/
  montage.py` (a labelled-images contact-sheet builder) does exist and was **reused**
  for the final sheet rather than rewritten — this repo already has "seven arcs [that]
  have each written their own sheet builder" per its own commit history; an eighth was
  avoidable and is avoided here.
- `tests/` — `test_t92*` and `test_t93*` both absent (Glob, both empty results). Both
  free. **Neither claimed** — no tool code was added to the repo (see §6).

### The "unspecified baseline," named

`facet_E08/SPEC/PREDICTIONS.md` names it directly: *"Scored by eye at full resolution
on the unspecified baseline — the BRACER twin"* → **`E:\AI\training\facet_E08\BRACER\
w3clay_0.png`**. Its own prompt (`BRACER/w3clay_0_gen.json`) names eleven-ish concepts
and uses `"gold-trimmed brown leather bracers"` — a *modifier* form of the N11 idea,
distinct from N11-arm's *head-noun* form (`"a gold plate on each outer forearm"`); both
are the "two different grammatical forms" CLAUDE.md's own law already cites as having
produced no response (ΔE 1.07).

### Gate A — HELD

The dispatch requires confirming (a) the SPEC prompt names N11 and (b) the image
cropped is that prompt's output.

**(a)** `docs/experiments/E08-spec-prompt.json` contains, verbatim: *"...brown leather
bracers, a gold plate on each outer forearm, gold knee plates..."* — confirmed by direct
read, not by memory.

**(b)** This is where the arm's own provenance has a real gap: **`SPEC/` has no
`w3clay_0_gen.json`**, unlike `BRACER/`, `N11/` and `ARMOUR/`, which all do. That gap is
reported, not hidden. The link was established instead by three independent lines of
evidence, run as `e53_gate_a_provenance.py` (receipt: `gate_a_provenance.json`):

1. **Pixel-level.** `SPEC/w3clay_0_control.png` and `SPEC/w3clay_0_mask.png` are
   **sha256-identical** to `BRACER/`, `N11/` and `ARMOUR/`'s own control/mask files
   (`c158af80…`, `8d62983b…`). Same twin, same camera, same registration across all
   four arms — the only thing that differs between them is prompt text. `SPEC/
   w3clay_0.png` itself has its own distinct hash (different pixels, as expected for a
   different prompt) at the same 752×1024 frame.
2. **Textual.** `E08-spec-prompt.json`'s own `_purpose` field ties it to *"Step 2 — the
   full-spec reproduction gate"*; `SPEC/PREDICTIONS.md` independently describes *"Step 2
   asks whether a 16-element spec reproduces its own elements"* in matching terms;
   `CONTRA/PREDICTIONS.md` states outright that `E08-contradiction.json` (CONTRA's own
   prompt) *"is E08-spec-prompt.json with the contradicted adjectives substituted in
   place"*; `E08-contradiction-report.md` cites a specific Comfy prompt_id
   (`edfcacd8-3c80-4b54-856c-b9a751ece3d8`) for "SPEC" as an arm in its own comparison.
3. **Visual, and this is the strongest leg.** SPEC's full image independently shows
   **N9 (green cloth skirt panels)** — the skirt is visibly green fabric under the belt,
   not the plain dark red/maroon of BRACER and N11 — and **N5 (gold scrollwork on the
   pauldrons)** — visible spiral engraving on both pauldrons, absent (smooth) on
   BRACER/N11's pauldrons. Both are *exactly* what the record independently reports
   measuring on "SPEC" (`E08-contradiction-report.md`: *"N9 skirt panels, green → grey:
   ΔE 47.41"*, which requires N9 to have been green in SPEC first; Amendment 16's
   framing of N5 as the open discriminator). A file that were not really SPEC's output
   would have to coincidentally reproduce both of these independently-reported facts.

**Conclusion: Gate A holds.** The provenance sidecar's absence is a genuine, separately
worth-fixing gap in this repo's own "every generation writes a provenance sidecar"
standard, but the link itself is established on independent pixel, textual and visual
grounds and I did not halt.

---

## 2. The reference (opened in full, both files)

`canon/twin_front.png` and `canon/twin_back.png`, both opened whole before anything
else, then zoomed.

- **Front, hanging arm (screen-right, not holding the sword):** shows the brown leather
  cuff **and** a distinct gold, blade-shaped vambrace plate on the outer/lateral edge of
  the forearm, side by side, extending down past the wrist — the "definitely PRESENT"
  exemplar of N10+N11 co-located successfully.
- **Front, sword-gripping arm (screen-left):** the fist on the hilt is entirely bare
  flesh-toned; the forearm above it is foreshortened to almost nothing before the
  pauldron. This is a **direct visual match** to the Director's ratified note —
  *"the front view shows the sword hand palm-on — which is exactly why it registered
  as bare flesh."* Confirmed by looking, not taken on trust.
- **Back view:** the visible gripping wrist there shows a gold band plus a leather wrap
  — confirming both arms canonically carry the combo, from an angle the front camera
  cannot show it on the gripping side.

This matters directly for scope: **the front camera used by the whole BRACER/N11/
ARMOUR/SPEC/CONTRA lineage cannot show N11 on the sword-gripping arm at all — not in
the generated pipeline, and not even in the hand-painted canon reference.** That is a
framing fact, not a pipeline defect, and it bounds what this report can answer (§5).

---

## 3. Predictions against outcome

`predictions.md`, written and saved **before** opening `SPEC/w3clay_0.png`, `N11/
w3clay_0.png`, `BRACER/w3clay_0.png`, `ARMOUR/w3clay_0.png`, `CONTRA/w3clay_0.png`, or
`facet_E08/LOOK/` (whose own filenames — `n11_zoom.png`, `bracer_zoom.png` — telegraph
their content, so they were deliberately left unopened until after predictions were
locked).

**Prediction: ABSENT, confidence ~65%.**

Reasoning given at the time (full text in `predictions.md`): N11's phrase — `"brown
leather bracers, a gold plate on each outer forearm, gold knee plates"` — is **the
identical substring, word for word**, in both `N11/w3clay_0_gen.json`'s prompt (which
measured ΔE 1.07, no response) and `E08-spec-prompt.json`. The only thing that changed
between the N11-alone arm and SPEC is the prompt text *surrounding* that unchanged
clause. I judged the more likely operative mechanism to be "two discrete worn objects
compete for one anatomical slot" (unaffected by how many other phrases exist elsewhere
in the prompt) rather than "patched vs. from-scratch" per se — while holding this at
only 65% because N9, a declared co-location case, **is** measured to have landed in this
same SPEC image (§1.3), which is real counter-evidence and not merely analogical.

**Outcome: ABSENT**, on the one assessable forearm (§4). **Prediction correct.** The
consideration that actually decided it, in hindsight: the exact-substring argument (a
mechanical, unchanged local contest) held; the N9 counter-evidence, while real, did not
generalize, most likely because N9 is a coloured sub-region of one garment rather than a
second discrete object at the same location — exactly the distinction drawn in
`predictions.md` before looking. **No miss to call on the core question.** The only
place the pre-registration undershot the eventual finding is scope: I did not
anticipate, before enumerating the pose, that the *second* forearm would turn out to
have no assessable surface at all (§5) — that is not a wrong prediction so much as an
unasked question, and it is called out here rather than folded silently into "ABSENT."

---

## 4. The instrument: calibration, pauldron non-admission, and the number

**The prior instrument this repo already tried and retired is not re-derived.**
`E08-ruling-gate0.md` (Amendment 15): *"A gold-pixel count over the forearm crop caught
the pauldron edge and read 5.6% / 5.1% against canon's 1.96% — inverting the truth."*
That was a **fraction-above-threshold count over a loose crop**. What follows is
deliberately a different shape: a **single median colour** of a **small, tightly-bounded,
pauldron-checked-clean** box, calibrated against two anchors from the same image
family rather than an invented cutoff.

### Gate B — HELD, checked three independent ways

The crop box used is `N10_BRACER_BOX = (503, 560, 562, 612)` — **not re-derived**, but
taken directly from `facet_E08/CONTRA/anchor_bracer_vs_n11.json`, an existing,
already-cited, already-used record artifact (enumerate-before-commission). The pauldron
box `(462, 430, 525, 495)` comes from the same file.

1. **Arithmetic, at build time.** `e53_forearm_crops.py`'s `gate_b_check()` computes
   pixel-rectangle overlap between the (20px-padded) forearm box and the pauldron box:
   **0 px overlap**, both for the record-sourced screen-right box and the
   mirror-derived screen-left guess. The check is wired as a real `raise SystemExit`
   ANDON, not a bare `assert`, and would have halted the run had either box failed.
2. **The ANDON was demonstrated capable of firing, not merely silent** (this repo's own law:
   *"a check that cannot fail is not a check"*). A deliberately-bad box built to overlap
   the pauldron box was run through the identical `gate_b_check()` function as a
   negative control: `overlap_px=1575, admits_pauldron=True`. The check fires when it
   should. Its silence on the real boxes is therefore evidence, not an artifact of an
   unfalsifiable test.
3. **Visual.** The crops themselves (§ below) show bare bicep skin transitioning
   directly into the leather cuff — no pauldron gold, no pauldron edge, in any of the
   five sampled arms.
4. **Orthogonal, after the fact.** CONTRA's own pauldron desaturates to near-neutral by
   design (gold→silver contradiction; measured here as C\*=1.8, h=272° — matching the
   record's independently-reported silver readout). If the forearm box leaked any
   pauldron pixels, CONTRA's forearm-box reading would be pulled toward that neutral
   value. It is not: CONTRA's forearm box reads C\*=14.2, h=55.4 — squarely inside the
   same leather cluster as the other four arms. This is a check I did not have to build
   on purpose; it fell out of measuring all five arms with the same box.

### Calibration populations, stated before the SPEC number is read

Both anchors measured **on the same images**, via `e53_forearm_colour.py`, using the
`to_lab()` sRGB→CIE-Lab formula copied verbatim from `tools/diagnostics/e08_deltaE.py`
(so the numbers are directly comparable to ones already published in this repo):

- **Methodology cross-check, run before trusting anything downstream:** my own computed
  BRACER numbers for the N10 box match the record's already-published
  `anchor_bracer_vs_n11.json` values **to the last integer** — `rgb_median [65,39,26]`
  vs. published `base_rgb [65,39,26]`; `L 18.6, a 11.7, b 14.3, C 18.5` vs. published
  `18.6, 11.7, 14.3, 18.5`. The independent gold calibration (pauldronR) matches within
  rounding (`C*≈37.3` mine vs. `39.9` published — median vs. mean and a slightly
  different exact box account for the small gap). This is the check that licenses
  trusting the SPEC number below.
- **Definitely-YES (gold):** `pauldronR` box, this image family, C\* ≈ 37–43, h ≈ 78–80°.
- **Definitely-NO (leather):** the `N10` box itself, on **BRACER and N11** — both
  independently confirmed ABSENT by the existing record (ΔE 1.07, Amendment 15) — reads
  C\* ≈ 18.5–19.1, h ≈ 50.7–51.0°.

### The read

| arm | N10-box median RGB | L | a | b | C\* | h° |
|---|---|---|---|---|---|---|
| BRACER (known ABSENT) | 65,39,26 | 18.6 | 11.7 | 14.3 | 18.5 | 50.7 |
| N11 (known ABSENT) | 69,41,28 | 20.0 | 12.0 | 14.8 | 19.1 | 51.0 |
| **SPEC (the question)** | **68,39,24** | **19.1** | **12.0** | **16.6** | **20.5** | **54.1** |
| ARMOUR (no bracer/plate in its own prompt) | 53,33,22 | 14.9 | 8.6 | 10.9 | 13.9 | 51.9 |
| CONTRA (SPEC's colour-swap sibling) | 62,41,30 | 18.9 | 8.1 | 11.7 | 14.2 | 55.4 |
| *gold calibration (pauldronR, same boxes/arms)* | *~129,104,42* | *~47* | *~7* | *~37* | *~37–43* | *~78–80* |

SPEC's forearm-box read (C\*=20.5, h=54.1°) sits inside the same tight cluster as every
other arm's leather reading (C\* 13.9–20.5, h 50.7–55.4°) and nowhere near the gold
calibration (C\* 37–43, h 78–80°). Full JSON: `forearm_colour.json`.

**This is a median colour read, not a threshold-and-count** — deliberately, because a
small box already visually confirmed homogeneous (§ below) does not need a cutoff to
summarise, and a cutoff is exactly the mechanism that inverted the prior instrument.

---

## 5. The crop sheet

`E:\AI\training\facet_E53\crops\E53_forearm_sheet.png` (1500×377, built with
`tools/verify/montage.py`, reused rather than rewritten) — **reference | unspecified
baseline (BRACER) | SPEC | N11 patch (isolated)**, native-pixel forearm crops, defects
first:

- **Reference** (`canon/twin_front.png`, hanging arm): brown leather cuff **and** a
  distinct gold plate on the outer edge, both visible.
- **Unspecified baseline (BRACER):** brown leather cuff only.
- **SPEC (from-scratch, 16 elements):** brown leather cuff only — visually
  indistinguishable in kind from BRACER.
- **N11 patch (isolated, single-phrase addition):** brown leather cuff only, labelled
  explicitly as its own patch operation, not folded into "one variable with SPEC."

`montage.py`'s own built-in brightness-spread gate (designed for turnaround-view
lighting consistency, <1.2×) read 1.24× and printed FAIL on this sheet — **not
applicable here and not treated as a finding**: that gate compares a hand-painted
reference against three AI-rendered clay outputs, an apples-to-oranges brightness
comparison the tool was never built to judge; it is reported for completeness, not
read as a defect.

### What the other forearm (sword-gripping arm) showed

An exploratory crop of the equivalent screen-left region, in both BRACER and SPEC,
shows only the bare fist gripping the ornate gold hilt — no forearm shaft is visible at
all between the pauldron and the fist in this pose, in either arm. This matches the
canon front reference exactly (§2). **This forearm is not assessable for N11 from this
camera, in any arm tested, canon included.** It is reported as an unanswerable question
under this framing, not as a second ABSENT finding — treating "no visible surface" and
"visible surface, no plate" as the same result would be exactly the "test the property,
not a proxy for it" error this repo's law warns against.

### Prior, independently-made crops found in `facet_E08/LOOK/`

`n11_zoom.png` and `bracer_zoom.png` (pre-existing, made by an earlier seat, opened only
**after** predictions were locked) each show a 3-panel reference/generated-arm/
generated-arm comparison. Every generated-arm panel in both — spanning at least the N11
and BRACER arms, and something ARMOUR-like showing fur rather than leather — shows no
gold plate. Independent corroboration of the same pattern, though neither file includes
SPEC itself, which is the gap this report fills.

---

## 6. Standards compliance (0–3, per `workflow_standards.md`'s six)

- **PIN_PER_STEP — 2/3.** Every box, padding, scale, tolerance and hash is a literal in
  the script and is echoed into a JSON receipt (`gate_a_provenance.json`,
  `crops/manifest.json`, `forearm_colour.json`) alongside the number it produced. Not a
  3: there is no pytest-level harness re-running these receipts on demand, only the
  scripts themselves (rerunnable, but not wired to a test runner).
- **ANDON_AUTHORITY — 2/3.** `e53_forearm_crops.py`'s Gate B check is a real `raise
  SystemExit`, not an `assert`, and — per this repo's own "a check that cannot fail is
  not a check" law — was **demonstrated able to fire** with a deliberately-bad negative-control
  box (§4) before being trusted on the real ones. Not a 3: this proof lives in this
  report and a throwaway REPL call, not in a committed, always-run test.
- **NAMED_COMPENSATORS — 2/3.** Every write from all three scripts is additive, into new
  paths under `E:\AI\training\facet_E53\` only. Named compensator: delete that
  directory; owner: whoever next opens this arc (advisor or Director). Not a 3: this is
  stated here and in `handoff.md`, not inside each script's own docstring individually.
- **DECOMPOSE_BY_SECRETS — 2/3.** Three single-purpose scripts
  (`e53_gate_a_provenance.py` for hashing/metadata, `e53_forearm_crops.py` for
  crop-geometry + Gate B, `e53_forearm_colour.py` for the calibrated colour read), each
  independently rerunnable, rather than one monolith. Not a 3: no test suite pins that
  separation against drift.
- **UNCERTAINTY_GATED_HUMANS — 2/3.** The whole task is structured as a stated,
  falsifiable, non-100% prediction (§3) with an explicit "ambiguous, report as such"
  branch pre-registered in `predictions.md`, and this report defers "what it means for
  the co-location law" entirely to the advisor's ruling (§8). Not a 3: no gate actually
  fired, so the contrastive-framing halt-and-ask machinery was never exercised live in
  this arc, only built and (for Gate B) demonstrated capable of firing.
- **EXTERNAL_VERIFIER — 2/3.** The colour instrument's calibration is checked against
  **independently, previously published** numbers in `anchor_bracer_vs_n11.json` (not
  self-referentially defined) and matches to the last integer; the numeric read and the
  native-pixel visual crop sheet are two independently-produced readings that agree.
  Not a 3: this task has no generator/verifier pair in the model sense — the analogy is
  real (two independent methods converging) but not the load-bearing model-family split
  the standard was written for.

No score below 2; no named remediation required by the standard's own rule, though the
gaps above (no pytest harness around these receipts) are named rather than hidden.

---

## 7. Out of scope (explicit)

- **Whether the co-location law survives from-scratch specification in general.** This
  report measures one element (N11) on one surface (forearm) in one arm (SPEC). It does
  not re-litigate N9 (already measured landed, elsewhere in the record) or address N5
  beyond the visual confirmation in §1.3, which was incidental to establishing Gate A.
- **Whether a compound-occupant generation on the forearm is worth spending on.** That
  is the ruling this report's evidence feeds, not a conclusion this report draws. I have
  not judged whether the asset is good, whether the forearm "should" carry a plate as a
  design matter, or what the schema repair in `canon/w3.surfaces.json` should say.
- **The sword-gripping-arm forearm**, beyond reporting that it has no assessable surface
  from this camera in any tested arm (§5). Whether a different camera angle would show
  it is not tested here.
- **`canon/w3.surfaces.json` itself.** Not edited. The ruling document explicitly
  reserves that edit for its own change, with its own tests and the Director's word.
- **Any repo tool commit.** `e53_gate_a_provenance.py`, `e53_forearm_crops.py`,
  `e53_forearm_colour.py` remain in `E:\AI\training\facet_E53\` only. They are not
  copied into `tools/diagnostics/`, not committed, and no `t92`/`t93` test was claimed
  — promoting any of them to permanent instrumentation (with the tests that would then
  be owed) is left to the advisor's fold, not decided here.
- **ANCHOR/ and ARMB/ trees.** Enumerated (top-level file listing only, §1) but not
  opened in depth — they concern earlier registration/reproduction work (0b anchor,
  8-camera stage-1 work) not directly load-bearing for the N11/SPEC question.
- **Committing or staging anything.** No `git add`, no commit. The working tree is left
  as-is for the advisor's fold, per instruction.
- **Any write to a memory store.** None made.

---

## Files

- `E:\AI\training\facet_E53\handoff.md` — live-updated arc record.
- `E:\AI\training\facet_E53\predictions.md` — locked before any arm's pixels were seen.
- `E:\AI\training\facet_E53\e53_gate_a_provenance.py` + `gate_a_provenance.json`.
- `E:\AI\training\facet_E53\e53_forearm_crops.py` + `crops\manifest.json`.
- `E:\AI\training\facet_E53\e53_forearm_colour.py` + `forearm_colour.json`.
- `E:\AI\training\facet_E53\crops\E53_forearm_sheet.png` — the deliverable sheet.
- `E:\AI\training\facet_E53\crops\` — every individual crop (BRACER/N11/SPEC/ARMOUR/
  CONTRA × left/right, both explore and final passes, plus the two reference crops).
