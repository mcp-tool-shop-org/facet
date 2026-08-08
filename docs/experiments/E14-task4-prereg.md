# E14 Task 4 — pre-registration, written BEFORE the pair exists

**Executor session, 2026-08-07.** Written and committed before the twin-prompts file was
built, before any control was built through the ruled pair, and before any submission. Task 4
was authorised at [E14-ruling.md](E14-ruling.md) Ruling 11c; the dispatch's calibration note
makes this pre-registration the executor's.

**Blind status, stated precisely rather than claimed:**

- **§1 (register drift on metal) is fully blind.** No styled image of this longsword exists.
  Nothing in this repo has generated on this subject. Not one credit has been spent on it.
- **§2 (the one-string check) is NOT fully blind, and here is exactly what I have seen**:
  `swordclay_0.png` at full size (this session), a 5× crop of the blade *only* on view 2
  (`CROP_2_blade-edge-on.png` — blade field, no hilt), and the four canny crops on view 0. I
  have **not** looked at views 1, 2, 3, 5, 6, 7 at full size this session, and have not opened
  the Gate 0 sheets. The prediction being scored (W1) was committed blind in `d11fd32` before
  any of that.
- **§3 (what the pair costs and how it can fail procedurally) is blind** in the sense that
  nothing has been submitted.

---

## 1. What a register drift on metal would look like — named before the artifact exists

The register is the Director's sentence: **ultra-realistic, LoRA NONE** (Ruling 5a). This is
the route's first test of that register on a **near-achromatic** subject, and the failure modes
of realism-on-metal are not the failure modes the route has already learned to see on hide,
timber or cloth. Named now so that "it looks fine" and "it drifted" cannot be decided after the
fact.

**The eye is the gate. Every number below is support, and none of it is a gate** — this repo's
own law is that a metric which cannot separate a rejected asset from an accepted one is not a
metric, and no such metric exists for this yet (the pair *is* the first artifact).

### D1 — painterly drift (the W3 register arriving uninvited)

**What it looks like:** visible brushstroke texture on the blade faces; the flat fields reading
as *worked surface* rather than as ground metal; edges gaining a drawn quality.

**Why it is the first candidate:** the code default prompt this profile protectively overrides
literally ends `visible brushstrokes, painterly worked surface` (E04 Ruling 22's named accident
class), and the whole accepted route was generated under that register. If any of it leaks
through the checkpoint's own prior, the blade is where it will show, because the blade is the
largest smooth field.

**Support, not gate:** high-frequency energy inside the blade region above what the clay's own
relief explains.

### D2 — chrome drift (the fixture's own named boundary, crossed)

**What it looks like:** the blade becomes a mirror — a hard blown highlight band with the nicks
and scoring **vanishing into specular** instead of reading as damage.

**Why it is pre-registered:** L1's note names this boundary in the fixture itself — *"worn
steel, not mirror chrome, so the relief reads as damage rather than vanishing into specular."*
It is the one drift the fixture predicted at authoring.

**Support:** a bimodal or clipped blade histogram; the count of pixels at or near 255 inside
the blade region; loss of the nick scoring that Gate 0 measured as reconstructed geometry and
that the control at 0.10/0.25 now carries as constraint.

### D3 — stylised-game-metal drift

**What it looks like:** cel-like hard-edged specular bands, rim lighting the geometry does not
carry, saturated tinting of the steel (teal/blue "fantasy steel"), a graphic bevel on the
quillons.

**Why:** "longsword" is a heavily stylised token in any image model's prior, and this is the
first subject on the route whose *noun* pulls that hard toward game art. The realism terms are
the counterweight and this is the test of whether they hold.

**Support:** L1's realised chroma (see D4 — the two are separable by hue, not by magnitude
alone).

### D4 — backdrop bleed onto achromatic steel ⚠ ALREADY PRE-REGISTERED AT RULING 7b

**What it looks like:** the blade takes a lavender cast — steel arriving **above** the C\* 5.0
chroma floor **inside blue-violet's own band**.

**This is not my pre-registration to make; Ruling 7b made it**, and it is repeated here so it
is measured in the same pass as the rest: *"L1's realised lightness AND chroma are measured —
the named risk is cool-cast materialisation… if it does, that is a finding reported with the
pair and owned by the palette-bands derivation — the word is not re-chosen while looking at the
artifact it would judge."*

**Measured at the pair:** L1's realised L\* and C\* and, if above the floor, its hue against
blue-violet's 225–300 band. **The word is not re-chosen on this result.** I record it and stop.

### D5 — the photographic boundary

**What it looks like:** a photographed prop — depth-of-field falloff, lens bloom, a studio
product shot.

**Why it is worth naming and why it is the weakest of the five:** the negative carries `photo`,
so the recipe already asserts a distinction between *ultra-realistic* and *photographic*. I do
not know where that line sits for this checkpoint and I am not confident this is separable by
eye from a good outcome. Named as the one I expect to be least able to call.

### What is NOT drift, and must not be reported as such

- **The softer gem apex and the lumpier wrap** are **designated-in** (Ruling 1) — subject facts
  the Director designated on, not defects.
- **A blade reading dark against a pale lavender ground.** That is the derivation working: the
  backdrop was chosen to sit far from steel, and value separation is the entire mechanism by
  which it does so on an achromatic material.
- **Edge-on views rendering the blade as a sliver.** That is the subject (Gate 0 §6).
- **Any element landing imperfectly at 240 px of frame width.** S-hilt-scale pre-registers the
  hilt at roughly 7% of frame pixels; if the hilt reads soft that is the E12 head physics
  arriving on schedule, **recorded and not tuned**, and the measured lever if it ever bites is
  bake-side, never a crop generation (frame-changes-register, falsified ×3).

### The prediction I will be scored on

**P-D:** I expect **D3 (stylised game metal)** to be the live one and **D1 (painterly)** to be
absent, because `lora-w 0.0` removes the route's painterly LoRA entirely and the register terms
are explicit, while nothing in the recipe opposes the model's own "longsword" prior except the
word *ultra-realistic*. I expect **D2 (chrome)** to be partially present — some specular
flattening on the flat fields — because `battle-worn` is a weaker steering term than `mirror`
is an attractor. I expect **D4** to be **absent** (steel arriving below the C\* 5 floor), which
is the outcome Ruling 7b's check would call clean.

---

## 2. The one-string-vs-per-view check — what I am about to test, and against what

The profile's `_fixtures.twin_prompts` note says this subject *appears* to pass the ship's
one-string premise (E04 Ruling 23) and requires verification per view against the actual
renders. The carried Gate-0 flag is that **views 2/6 render the gem and boss at near-nothing
edge-on**.

**The check, defined before it runs:** for each of the eight profile renders, does each of the
five named elements present a surface a generator could paint? An element **fails** a view when
that view shows *nothing of* it — not when it shows *little of* it, which is the distinction
the profile's own note draws ("slivers of everything, not nothing of something").

**W1, committed blind in `d11fd32`:** *"gem present on all eight views; the boss the one
element at risk on 2/6"* — on the grounds that a faceted polyhedron is roughly isotropic while
a diamond plate on the guard **face** is not.

**What I do with either answer:** one string if every element reads on every view; per-view
stems built by the same deletion construction if not (the builder's `--drop TERM:views` form,
which is how the beast's failure was expressed). **The premise is checked, never imported** —
this is E12 Ruling 9d's lesson, where the beast failed the premise six elements deep.

## 3. Cloud discipline, restated as the conditions this session holds itself to

Nothing here is new; it is written down so a departure is visible rather than convenient.

- **Generation is cloud-only.** Nothing measured runs locally (TRELLIS excepted, and none is
  needed).
- **`estimate_credits` before every submission**, quoted in the report.
- **The no-LoRA pre-flight on every submission** — `lora-w 0.0` is the Director's ruled
  register expressed mechanically, and the guarded path exists on both stages.
- **Workflow JSON saved before submission; link topology checked in code** — a `dry_run` PASS
  does not prove link sanity (E04 Arm G7 returned `status: validated` on a self-referencing
  link).
- **Frames generator-legal**: 240×1024, both axes ÷16.
- **One generation per view, one bounded re-roll each.** New seed on a re-roll; **the rejected
  artifact stays in the record with its measurement**; a second failure is the result, not a
  third roll. A re-roll is only legitimate against a **pre-registered** specification violation
  — rejecting an output that violates a spec written before it existed is not selecting a
  result, and the test is whether the rule would have been the same whatever came out.
- **Sidecar at birth**: *specification source and visual target, never a projection reference.*
- **HALT with the pair staged** — the advisor's eye, then the Director beside the clay. Nothing
  reaches the Director ungated.

## 4. What this session will NOT do

- Generate any view other than 0 and 1.
- Project anything, run any stroke, or touch `thin_extent`'s value.
- Derive the palette bands (they need the pair to exist first, and are non-circular by rule).
- **Re-choose the backdrop word or the canny pair on anything the pair shows.** Both are ruled;
  retuning a decision after seeing its result is the one move that is always wrong.
- Edit any profile or fixture, write to the memory store, or end a session the Director has not
  ended.
