# E12 handoff 6 — blind predictions

**Written BEFORE anything in this dispatch runs**: before the v5 prompts rebuild, before any
upload, before any submission, and before this seat has looked at a single image. Committed
first so nothing here can be edited against a result.

## Blind status — disclosed precisely

This is a **fresh session**. What it has read, and is therefore not blind to:

- `CLAUDE.md`, the handoff-6 dispatch, `docs/experiments/E12-ruling.md` Rulings 11 and 12,
  `canon/DRAGON-IDENTITY.md` as corrected, `profiles/beast.json`'s corrected protective entry,
  `docs/experiments/E12-twin-prompts.json` (v4), `docs/experiments/E12-handoff5-report.md` in
  full, and the opening section of `E12-handoff5-predictions.md`.
- Therefore: the *prose descriptions* of every prior landing — that seed 770700 view 5 wore a
  pale-tan haunch and bone-ivory membranes, that 770701 resolved both, that 273 px of a
  red/pink family sat at the far wing's rim on 770701 against 0 px on 770700, that the
  companion landed D3 orange/rust and painted no eye, and the Director's two verdicts in his
  words.

**What this seat has NOT done and is blind to: it has not opened one PNG.** No pair output, no
re-roll, no companion, no clay render, no control image, no crop, no sheet. Every prior landing
reaches this file as *a sentence someone else wrote*, not as a pixel this seat has seen. That
is a stronger blind position than the handoff-5 seat had, and it is stated so the next reader
can weight these predictions accordingly.

**Scored honestly either way.** Ruling 12's calibration line is the operating instruction: *a
changed prompt re-rolls every landing*. Every element below is treated as newly rolled, the
prior holds are scored as predictions rather than assumed, and each regression is a **named
branch here** so that it arrives as a finding and not as a surprise.

---

## Pre-registered derivations — fixed here so they cannot be tuned afterwards

### The v5 stems, derived by hand from the corrected entry before the builder runs

The corrected entry is 17 comma-terms. The correction **substitutes three terms and adds or
removes none**: D2 `pale bone-tan ventral plates` → `pale olive-tan ventral plates`, D6
`bone-ivory dorsal and tail spines` → `charcoal dorsal and tail spines`, D7 `bone-ivory claws`
→ `charcoal claws`. The 9d/10i drop map names only the mouth family (D8/D9/D10/D11 off
{3,4,5}) and the horn family (D4/D5 off {3,5}) — **none of the three corrected terms appears in
the drop map**, so the `--drop` arguments are byte-identical to handoff 5's.

Predicted, each checkable against the builder's own printout:

| | prediction |
|---|---|
| entry term count | **17**, unchanged |
| per-view counts | **17 / 17 / 17 / 11 / 13 / 11 / 17 / 17**, and `headclay_0` **15** — all identical to v4, because the correction substitutes and never adds or drops |
| full-string views | **0, 1, 2, 6, 7** — unchanged |
| v4 → v5 stem diff | **exactly 3 substituted terms in each of the 8 `dragonclay` stems; exactly 1 (D2 only) in `headclay_0`**, since D6 and D7 are already dropped there |
| **view 5's stem contains zero pale-bone-family words** | **the sharpest prediction in this file.** View 5 drops the mouth family and the horn family, so after the correction its 11 terms are: subject · D1 · D2 olive-tan · D3 storm-grey · D6 charcoal · D7 charcoal · backdrop · four register terms. **No `bone`, no `ivory`, anywhere in the string.** View 1 keeps three head-anchored pale terms (`bone-ivory` ×2, `pale ivory` ×1) |
| the `--extra` companion argument | its v4 dropped-term strings (`bone-ivory dorsal and tail spines`, `bone-ivory claws`) **no longer exist in the corrected entry**, so passing them verbatim **fires the builder's ANDON and writes no file**. Predicted: the corrected strings must be passed instead. If the builder accepts the old strings, the builder is broken and that is the finding |

### The diagnostics, and their bounds, fixed before any image is opened

**These are diagnostics and never gates** (Ruling 10d; the E07 class is judged by eye). No
threshold below decides anything; each is a number reported beside the sheet it belongs to.

- **Pale-bone family**, for the leg / tail-underside / wing-arm question: CIELAB, D65,
  **L\* ≥ 62 and C\* ≤ 20**. **Hue is not quoted for this family** — below a chroma floor hue is
  undefined and reads as a rotation (CLAUDE.md), and a pale near-neutral family is *defined* by
  low chroma, so it is keyed on lightness and chroma jointly and on nothing else.
- **Red/pink family**, for the wing-rim recurrence: **C\* ≥ 12, h 340–30°** — handoff 5's own
  criterion transcribed verbatim, so the recurrence test runs the identical instrument on the
  identical box, **x 1331–1411, y 426–514** (transcribed; the frame is unchanged because the
  control is unchanged).
- **The leg / tail-underside / wing-arm boxes are drawn on the CLAY render**, which is
  byte-identical across every arm compared. A box drawn on geometry cannot favour the old
  palette or the new one; their pixel coordinates go in the report with the clay crop beside
  them.
- **Both the total and the largest connected component are reported** for every family count,
  never the total alone — one wrong garment against ordinary speckle is a two-threshold
  question (CLAUDE.md).

### Free byte-identity checks, called before they are run

The controls and clay renders are reused unchanged, and the cloud names uploads by content
hash. **Predicted: all four uploads return the names already recorded in
`E12_repair/pair/uploads.json`** — `783564fa…` (clay 1), `7501744e…` (control 1), `b6f0739c…`
(clay 5), `94644488…` (control 5). A different name on any of the four means an input this
dispatch believes unchanged has changed, and that is a halt, not a footnote.

**Credits: 0**, with `estimate_credits` returning *"no paid API nodes found in this workflow"*
before each submission, as on every prior run of this graph.

---

## The works-perfectly test, stated before any result is read

For each question: what does the reading look like if the correction **does nothing**, and what
if it **works perfectly**? Where those two are the same number, the instrument is not measuring
the arm and is not used.

**Q1 (the bone reads).** Does nothing → the pale-family mass inside the leg, tail-underside and
wing-arm boxes is indistinguishable from the old-palette output at the same boxes, and the ridge
lines are still visible at 3×. Works perfectly → that mass collapses toward residue and the
ridges are gone to the eye. **Different states, both observable.**

**Q2 (the holds).** Does nothing → view 5's haunch is pale tan and its membranes pale, as at
770700 under the old palette. Works perfectly → moss-green haunch, storm-grey membranes.
Different states. *Note the asymmetry this arm carries: 770700 is the seed that MISSED both on
the old palette, so a hold here is the prompt doing work, not the seed.*

**Q3 (the wing-rim artifact).** Recurs → a non-zero red/pink count in the fixed box with a
connected component of order 100+ px. Absent → order 0–10 px of speckle. Handoff 5 measured
273 px against 0 px in the same box on the same instrument, so the instrument is known to
separate these two states on this subject.

**Q4 (charcoal).** Lands → dark neutral mass on the dorsal ridge, the tail blade rows, the feet
and the wing-wrist spur, distinguishable at 3× from D3's mid storm-grey sheets by lightness.
Fails → those structures wear the hide's green, or a pale residue, or read at the same
lightness as the membranes. Different states.

---

## The predictions

### P1 — the Director's named defect leaves, and the two views leave it differently

**P1a — view 5 clears decisively.** Its v5 stem carries **no pale-bone-family word at all**. The
tail's banded underside renders olive-tan rather than skeletal, the tail blade rows render dark,
and **no ivory ridge lines appear on the legs**. Confidence: high. This is the prediction most
load-bearing on the mechanism Ruling 12e named — if the word was the cause, removing every
instance of it from this view's string must remove the effect from this view.

**P1b — view 1 clears at the limbs, and is where any residue shows.** View 1 keeps three
head-anchored pale terms. Predicted: **no ivory ridge lines on legs or wing fingers**, pale mass
confined to horns, crown spikes and tooth rows. Named branch if wrong: three ivory terms is
still enough family pressure to invent pale ridges on green-declared surfaces, in which case the
mechanism is *density* rather than *the word*, and the correction is partial.

**P1c — the invented ridges are the harder half.** Ruling 12e decomposed the defect into
*declared canon realised* (D2 on the tail, D6 on the blade rows) and *family-pressure invention*
(ivory ridges on smooth leg geometry, ivory on D1-declared wing fingers). The declared half is
removed **by construction** — those two terms no longer say `bone`. The invented half is removed
only if family pressure was the mechanism. Predicted: **both halves leave**, the declared half
at high confidence and the invented half at moderate.

### P2 — the holds, scored as fresh rolls

**P2a — D1's moss-green HOLDS on view 5's haunch, shoulder and near hindquarter**, at seed
770700. Reasoning: the original miss at this exact seed was a *pale* region on a green-declared
surface, the same failure family the correction cuts — the miss and the defect share a
mechanism. Confidence: moderate. **This is a regression branch and not a formality: 770700 is
the seed that produced the miss.**

**P2b — D3's membranes HOLD storm-grey on view 5.** Confidence: low-to-moderate, and **D3 is the
single most likely regression in this dispatch.** It has landed three ways in the record —
bone-ivory at 770700, storm-grey at 770701, orange/rust on the companion — one element with
three landings across two frames and two seeds. If any named element misses here, predicted it
is this one.

**P2c — the head elements on view 1 hold**: D4 horns and D10 tooth rows land pale as they did,
D2's throat bands land (now olive-tan rather than bone-tan). D5's split landing (crown ivory,
cheeks green — recorded on the companion at bust scale) is **not** predicted either way at pair
scale, where it was never separately observed.

### P3 — the wing-rim mouth artifact does NOT recur

At the fixed box on view 5 seed 770700, predicted **< 20 px of the red/pink family, no connected
component above 50 px**. Two reasons: it was absent at 0 px on this seed under the old palette,
and the control — which the executor's labelled hypothesis blamed — is byte-identical here.
**Weak evidence, disclosed as weak**: a changed prompt re-rolls the whole trajectory, so a
seed's prior behaviour under different conditioning does not transfer. If it recurs at 770700
under a new prompt, that materially strengthens the control-cost hypothesis and is the more
interesting outcome.

### P4 — charcoal lands, and the grey family does not collide

**P4a — D6 lands** as a dark neutral segmented ridge from shoulders to tail tip and on the paired
tail blade rows; **D7 lands** on the feet and the wing-wrist spur. Confidence: moderate;
`charcoal` is a common unambiguous colour word with no anatomical referent, which is the property
the correction was chosen for.

**P4b — charcoal separates from D3's storm-grey at 3× by lightness**, and does not need to
separate from D11's slate at all, because the two never share a boundary: the mouth interior is
inside the cavity, and it is dropped from view 5's stem entirely. Predicted: **no collision** on
either view.

**P4c — the named risk, and it is a real one.** The correction does **not** reduce total
colour-family density; it moves mass from the pale family to the grey family. On a full-string
view the pale family goes 5 terms → 3 and the grey family goes 2 terms → **4** (storm-grey,
charcoal, charcoal, slate). If *density* rather than *the word* is the mechanism, the prediction
is a grey invention on green-declared surfaces — a grey wash down the flanks, or the hide reading
desaturated. **Predicted: it does not happen**, because Ruling 12e's measured mechanism was the
word `bone` being rendered *literally as anatomy* under the realistic register, and `charcoal`
has no anatomy to be rendered as. **If a grey invention appears, this prediction is falsified,
the mechanism is density, and that changes the fixture advice for every future
realistic-register subject.**

### P5 — process predictions

- **P5a** — the four uploads return the four recorded content-hash names. Free confirmation.
- **P5b** — 0 credits, both submissions, both `estimate_credits` calls.
- **P5c** — both allowances go unspent: **no re-roll is needed on either view.** Confidence:
  low. This is the prediction most likely to be wrong, and P2b is the likeliest reason.
- **P5d** — the builder's ANDON fires if the companion's old dropped-term strings are passed
  (see the derivation table). A guard proven to fire before it is trusted.
- **P5e** — a finding this seat expects to report rather than fix: **`headclay_0`'s recorded
  rationale for dropping D6 is void under the correction.** v4's note justifies the drop as
  *"the ivory family is already carried by D4/D5/D10, so the shoulder-end spines keep their
  colour by family"* — under the correction D6 is charcoal and is carried by no other term, so
  the shoulder-end spines at the companion's bottom edge now have **no declared colour**. The
  companion is not re-run this dispatch (Ruling 12f), so the stem is built exactly as the
  dispatch instructs and the void rationale is reported to the advisor, not repaired from this
  seat.

---

## What would make this dispatch a full success while every prediction above fails

Stated so this file cannot be read as a target. The dispatch's question is the Director's one
sentence — *does this read as the dragon he wants*. If P1 is falsified and the bone reads
persist under a string with no `bone` in it, that is a **more valuable** measurement than a clean
pass: it moves the mechanism from the word to the register itself, and it is exactly the kind of
falsification this repo exists to produce. A negative result is a full success and is reported
plainly.
