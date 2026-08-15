# E36 — the route arms: dual control, the flat init, and the corrector contract

**Seat:** advisor · **Dispatched:** 2026-08-15, at the Director's word ("Why haven't we
tried this?" — the dual-control arm, pointed at directly) · **Grounding:**
[repaint-route-consult5-grounding.md](../research/repaint-route-consult5-grounding.md)
(consult #5, calibration PASSED and generalized) and the E35 record
([E35-ruling.md](E35-ruling.md)) — the measured map every arm here is priced against.
**Halts at:** `E36-route-arms-report.md` per arm sheet · **Tests:** T71+ · **This
dispatch's own commit bumps `laws.paid_for_by` to `E3[0-6]`** — thrice-proven now.

## The question

The recorded route (qwen-image img2img + canny at denoise 0.92 / cn 0.9) is the
class-best measured configuration and the only served route where identity is a
first-class input. Two levers that act on the measured mechanisms — anchoring
suppresses the pale class (R2-c); the dark class is baked-shadow painting (E35
Rulings 2/9) — were never tested in their correct form. **Can either, or both, move
the classes while keeping the man?**

## Why these were never tried — recorded so the reason is not re-derived

Consult #1's depth schedule was validated on the environment line and adopted as
standing THERE, never ported. The E35 grounding did not rank it. The slate's (c) arm
tested a DIFFERENT topology — depth replacing canny at full strength — whose identity
break shadowed the direction; the dual form never failed because it never ran. The
anchoring mechanism that re-ranks it upward was measured only at R2-c.

## The arms — one variable each, view 1, seed 770700, all else the recorded recipe

**Arm 2 first (the Director's pointing), then arm 1; combined only if both help.**

- **ARM 2 — dual control, depth-early + canny.** Depth preprocessor → union apply #1
  (strength 0.80, start 0.0, **end 0.45**) → canny preprocessor → union apply #2
  (strength 0.45, full schedule) → the recorded sampler. Type follows the
  preprocessor (the C-i enumeration); the same union loaded twice. The depth render
  comes from `silhouette_masks --depth` (T69-anchored, 0 differing px against the
  recorded masks). Provenance stated on the sheet: the 0.80/0.0/0.45 schedule is
  consult #1's, validated on environment plates, ported here for its first character
  test. Controls are measured-safe against the quantisation trigger (the slate's (c)
  ran a depth control without corruption; the trigger lives at the edit ENCODE, not
  the control path).
- **ARM 1 — the flat-lit init.** The clay init re-rendered under FLAT light rig-side
  (the repo's own `--flat` convention; recorded invocation, anchored against the
  current init's geometry before the frame is trusted), all else recorded. **Guard
  that binds:** unique-colour count on the new render before submission; below the
  clean family (~5,000), one lanczos round-trip per the E35-measured repair — the
  E01 family law applied to this new consumer.
- **ARM 3 — combined**, only if arms 1 and 2 each help on at least one class without
  breaking the other or the man. Otherwise unspent.

## Hypotheses — three branches each; the sign is stated or admitted unknown

- **H1 pale (arm 2):** DOWN is the mechanism-consistent branch (anchoring suppresses
  the class — our measurement, not testimony). FLAT and **UP are live branches** —
  the slate raised pale on two arms nobody predicted. Executor's blind bands govern.
- **H2 dark (arm 2):** DOWN (depth explains concavities — consult mechanism,
  untested) / FLAT (the 2c precedent: cn changes never moved dark) / UP.
- **H3 dark (arm 1):** DOWN (the init's crevice shading is the amplified signal) /
  FLAT (the prompt-side flat-lighting arm moved dark not at all — weak evidence the
  prior does not need the init's help) / UP.
- **H4 register:** the failure signal for arm 2 is **register C\*** (two anchors can
  starve chroma the way low denoise did), not identity. The register floor ANDON
  binds on every arm.
- **H5 identity:** the Director's eye, on every sheet, at full size. The pale class
  is read by the instrument, never by eye at working zoom (the C3 law).

## Budget — the arithmetic before anything fires

**Ceiling 15 jobs** (≈ $0.27): arms 1+2 = 2 · arm 3 ≤ 1 · the eight-view rebuild on
a Director-picked winner = 8 · contingency 4 (one mechanical repeat per arm, one
re-roll). The rebuild fires only at his word at a sheet. Zero partner-API nodes.

## Alongside, zero cloud — the corrector contract track

The successor's second front (E35 Ruling 11d): a NEW tool contract above the 36 px²
cap, validated against Director-rejected artifacts before any A/B, reaching the
377-texel components the cap excluded by design. Local work; specced separately
before it runs; named here so the arc's frame is complete.

## Compensators — no skip

| irreversible action | compensator | owner |
|---|---|---|
| ≤ 15 cloud jobs | none exists — bounded before spend, per-arm gates, blind bands first | executor |
| writes under `facet_E36\` | remove the tree; re-derivable from recorded scripts | executor |
| repo commits / push | revert by commit, pathspec-scoped | executor / advisor |
| protected trees (E33/E34/E35 + eight subtrees) | prevention: read-only, `tree_manifest` gates at open and close | executor |

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | recorded recipe pinned; arms are single-parameter deltas with sidecars; consult schedule carries its provenance; limit: server-side weights, as always |
| ANDON_AUTHORITY | 3 | register floor raises; unique-colour guard on the new init; manifest gates at open/close; every halt is a hard stop |
| NAMED_COMPENSATORS | 3 | table above; the compensator-less spend bounded before the first job |
| DECOMPOSE_BY_SECRETS | 2 | arms decomposed by mechanism (anchoring vs init-signal); the corrector track separated by cadence |
| UNCERTAINTY_GATED_HUMANS | 3 | the Director's eye at every sheet; the rebuild only at his word; identity is his call by law |
| EXTERNAL_VERIFIER | 2 | consult #5 calibrated at its own nominated claim before this dispatch; the instrument anchors reproduce published rows before any new number; limit: his eye is the identity verifier by design |

## Count surfaces and namespace

Tests take **T71+**. The two-pass order is superseded by the close's correction,
verbatim: **land all pin edits → run the FULL suite to surface unknown pins →
collect → surfaces → census last.** Manifest gates at open and close via
`tree_manifest` (E33 form and E34 form both served). E15 ritual at open: scratch db,
19/19 or stop.
