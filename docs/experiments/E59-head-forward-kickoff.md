# E59 — the head stays forward: enforce the clause, then probe the hardest view

**Advisor spec, 2026-08-18. One executor seat (Sonnet), background. Working tree
`E:\AI\training\facet_E59\`.**

**Spend ceiling: 2 generations — the balance the Director authorized for the twin work and
E58 held unspent. Absolute; reaching it halts the seat.** Stages 0 and 1 are free and both
precede any submission.

**Direction (the Director, 2026-08-18, paraphrased):** the head must look straight forward
as canon — in the E58 ring it turns toward the camera as the body rotates, and it should
stay straight throughout. He separately ruled the ring's identity close enough to the
reference (the twins are this man; that question is closed) and corrected the advisor for
over-weighting the ink reading (a minor register difference, not a work item — do not
re-raise it).

---

## The question

Does expressing the head direction in the text conditioning straighten it, or does the
control need more authority against denoise? Measured on the view where the defect is
worst, with the prompt-only arm separated from the control-authority arm.

## What is already known (measured, not assumed)

- **The geometry is not the cause.** A1's head is straight on the mesh by construction
  (built from a front-facing reference) and the E57 clay ring shows it straight at every
  yaw. **The generator overrode a correct control** — so the levers are the text
  conditioning and the control's authority, not the mesh.
- **The venue is not a variable.** E58's Gate A anchor came back pixel-identical to
  `canon/A1_reference.png` (0 of 1,672,192 pixels differing, ΔE 0.0000). A difference in an
  output is a difference in the inputs.
- E58 ring parameters: seed 770700, `lora_w` 0.75, `cn` 0.9, **denoise 0.92**, 576×1024,
  8 views, delivered frame == requested frame on all 8.
- A second E58 defect is NOT this arc's subject and stays open: the plum long-vest returns
  brown on v1/v2/v6 and the gold embroidery is largely absent. **Do not tune for it, do not
  grade it, and do not let an arm's success or failure on the head be read as evidence
  about the garment.** Report what the probe images happen to show and nothing more.

## Stages

**Stage 0 — the clause becomes enforceable (free).**
`canon/a1.surfaces.json` now declares `stage_head_forward` with **`"required": true`**.
Today a `legal_clause` is *licensed but optional*, so a staging clause can silently drop
out of a prompt and the gate stays quiet — which would make this canon decorative.
Implement enforcement in `tools/canon_gate.py`: a legal_clause marked `required: true`
**must occur** in the checked prompt, and its absence refuses exactly the way a missing
ratified occupant phrase does. Unmarked clauses keep today's licensing behaviour
unchanged — this adds capability and removes no coverage.
Tests ride the same change-set, and the leg must be able to fail: assert the refusal fires
on a prompt with the clause stripped, AND assert an unmarked clause still does not require
occurrence (or the change silently makes every staging clause mandatory across W3 too).
Report `canon_gate census` and `resolve --subject A1` verbatim, and confirm **W3's and
LONGSWORD's rows are unchanged** — a non-perturbing anchor for a shared instrument.

**Stage 1 — the head-alignment instrument, calibrated before it is believed (free).**
The question is *does the head follow its control as well as the body does*. Build a
readout restricted to the head region and normalised against the same statistic on the
torso, so a whole-figure registration difference cannot masquerade as a head result.
**Both calibration populations are required before any number is quoted:**
- *definitely aligned* — the E57 clay renders against their own controls (the head is
  straight by construction);
- *definitely turned* — E58's ring views the advisor named (v1 45°, v2 90°, v6 270°).
**Gate 1:** if the readout does not separate those two populations, say so plainly and
**report it as not an instrument** — the Director's eye then rules the probe alone. That is
a full result, not a failure; do not tune the readout until it separates.

**Stage 2 — the probe (spend 2, and the ceiling ends the arc).**
View **2 (yaw 90°, the profile)** — the hardest case for this defect, so a fix that works
here works everywhere. `estimate_credits` before submitting, reported. Everything not named
below is byte-identical to E58's v2 submission: same control, same seed, same LoRA weight,
same frame.
- **Arm P (prompt only)** — add the canon clause to the positive text and its complement to
  the negative (*looking at the viewer / head turned toward the camera*). Prompt and
  negative are ONE intervention — expressing head direction in text conditioning — and are
  stated as one arm on purpose.
- **Arm C (control authority)** — Arm P's text, plus **denoise 0.92 → 0.80** and nothing
  else. One knob. If the head is still turned under Arm C, the next arc raises `cn`
  strength; do not raise it here.
Every submission passes the bound canon gate. Gate E from E58 stands: delivered frame must
equal requested frame or that view halts.

**Stage 3 — the sheet.**
control | E58 v2 (the defect) | Arm P | Arm C, at the Director's zoom, with the head region
shown large enough to rule on. Full-size PNGs on disk. The instrument's readings appear as
an appendix beneath, never as a verdict.

**Out of scope, named:** the garment/embroidery defect; any full-ring re-generation (that
is a later arc with its own ceiling and its own authorization); the ink reading (the
Director closed it); painting/projection; W3.

## Predictions

The seat states its own before Stage 2 runs, blind status disclosed, each inside the
interval its instrument can return — and per the E39/E40 law, compute what the head readout
returns on the *definitely aligned* and *definitely turned* populations FIRST, then predict
inside that interval.

The advisor's own, recorded before the fact and falsifiable: **Arm P alone straightens the
head.** Reasoning — denoise 0.92 leaves the model most of its prior, and the
face-toward-viewer prior is one of the strongest in portrait generation, but nothing in
E58's conditioning ever *asked* for a head direction; an unasked-for property arriving by
prior is exactly the class this repo's identity law says a named phrase recovers (the gold
knee plates precedent, where naming restored what only noise had been supplying). If Arm P
fails and Arm C succeeds, that law's scope is narrower than stated and the finding is worth
more than the fix.

## Standards compliance

1. **PIN_PER_STEP — 3.** Byte-identical control and seed carried from E58; one named knob
   per arm; every parameter recorded before submission.
2. **ANDON_AUTHORITY — 2.** Gate 1 (instrument fails to separate) and Gate E (frame) halt;
   the enforcement built in Stage 0 refuses fail-closed and `raise`s, never `assert`.
3. **NAMED_COMPENSATORS — 2.** Table below; spent credits have no undo, which is why the
   ceiling is 2 and Stage 2 runs last.
4. **DECOMPOSE_BY_SECRETS — 2.** Enforcement, instrument, and generation are separate
   stages over on-disk artifacts; the seat measures, the advisor rules, the Director judges.
5. **UNCERTAINTY_GATED_HUMANS — 2.** The head verdict is his eye by construction; the
   instrument is explicitly demoted to an appendix.
6. **EXTERNAL_VERIFIER — 2.** The gate and the alignment readout are deterministic and
   external to the generator; no model grades its own output.

### Compensators

| action | undo | owner |
|---|---|---|
| 2 generations | **NONE — spent is spent.** The ceiling and the free-stages-first ordering are the bound | advisor |
| `canon_gate.py` enforcement + tests | `git checkout`/`git revert` by pathspec | advisor |
| new tree `E:\AI\training\facet_E59\` | delete; derived artifacts only | advisor |

## Dispatch record (living)

- 2026-08-18 — spec written on the Director's three corrections (head forward as canon;
  identity accepted; ink de-weighted). The canon edit landed first: `stage_head_forward`
  added to `a1.surfaces.json` with `required: true`, and a POSE section added to
  `A1-IDENTITY.md` recording that **a single front-on plate cannot teach a turnaround
  property** — the first A1 canon element the reference could not supply, and the honest
  boundary of the reference-first method rather than a defect in it.

- 2026-08-18, AFTER THE SEAT CLOSED — ⚠ **THE PROBE WAS SENT TO A VIEW THAT DOES NOT
  CARRY THE DEFECT. The spec is wrong and the arc's two credits bought no test of its own
  question.** The advisor's error, found by walking the images the seat produced.

  **The measurement that overturns it.** The spec asserted view 2 (yaw 90°) was *"the
  hardest case for this defect"* and named v1/v2/v6 as the *definitely turned* calibration
  population. Read at full size: **v2's head is in profile, aligned with the body — there
  is no defect in the baseline**, visible directly in the seat's own Stage 3 sheet where
  E58 v2 and Arm P sit side by side with the same profile head. The defect is in the
  **rear-facing views**: `a1_ring_v3.png` (yaw 135°) and `a1_ring_v5.png` (yaw 225°) both
  show the back turned to camera with the head cranked over the shoulder to face the
  viewer. Neither was in the population the spec named.

  **Two consequences, and the second is the one that matters.**
  1. Arms P and C tested a fix on a view with nothing to fix. Neither arm can speak to the
     head question, and no reading of them may be entered as evidence about it.
  2. **Gate 1's firing is CONFOUNDED and must not be recorded as an instrument finding.**
     The seat was told to calibrate *definitely turned* on v1/v2/v6; at least v2 belongs in
     the *aligned* class, so the two populations were not distinct and **no instrument
     could have separated them.** The seat's own offered explanation — that silhouette IoU
     may be structurally wrong for an orientation defect — is plausible and **remains
     untested**; the seat behaved correctly throughout, halting at the gate and declining
     to tune, and the defect is upstream in this document.

  **The law it violates is already written here, twice.** *A real population whose members
  you never checked for the property still breaks the prediction*, and the advisor's own
  recorded failure shape: *specifying a check whose form assumes its answer*. The spec
  named a population by reasoning about geometry (a profile is the hardest angle) instead
  of opening eight PNGs — the free step, skipped, in the same session that had just written
  *enumerate the resource before commissioning one* into two other documents.

  **What the spend did buy, stated as the diagnostic it is rather than the test it was
  meant to be.** Arm C (denoise 0.92 → 0.80) is a large, visibly adverse change: the image
  washes out and the garment moves to a pale sage. Lowering denoise as the control-authority
  lever therefore costs colour heavily, which is worth knowing before the next arc reaches
  for it. Arm P left an already-correct view undisturbed — a weak negative control,
  recorded as weak.

  **Standing correction for the next arc: walk all eight views at full size and record, per
  view, whether the head is aligned and whether the garment is plum, BEFORE any arm is
  designed.** That enumeration is free and it is the step whose absence voided this arc.
