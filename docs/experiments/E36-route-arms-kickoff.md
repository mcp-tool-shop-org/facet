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

---

> ## ⚖ AMENDMENT — the execution spec this kickoff shipped without (advisor, 2026-08-15)
>
> The Director ruled the first executor handoff the weakest this seat has made, and
> he was right: it compressed what the record already holds, ordered a structural
> graph change with no anchor — the error class Ruling 6 folded hours earlier — and
> described a topology that contradicts the recorded pipeline. This amendment is the
> repair. Everything below supersedes the thin arm descriptions above where they
> conflict.

## Premises — measured or assumed (mark the outcome in the report)

| # | premise | status |
|---|---|---|
| 1 | The recorded view-1 payload is reproducible from the archive and the platform is pixel-deterministic on a verbatim payload | **MEASURED** (E35 task 7: ΔE 0.0000 on 360,448 px) |
| 2 | A `ControlNetApplyAdvanced` at strength 0.0 is a conditioning no-op, so the rewired dual graph at depth-strength 0 reproduces the recorded twin | **ASSUMED — task 0d proves it; this IS the structural anchor, and arm 2 does not run until it holds** |
| 3 | The authored view-1 depth map exists and is mask-consistent | **MEASURED** (`facet_E35\depth\armclay_1_depth.png`, T69-anchored: 0 differing px vs the recorded masks; `_depth_far.png` variant also on disk) |
| 4 | The depth map's head band occupies 110–179 of 254 levels (near-limb blowout compresses head relief) | **MEASURED at the slate — carried as a known property, not tuned; the `_far` variant is a contingency at the Director's word only** |
| 5 | The flat-lit clay render changes shading only — silhouette byte-equal to the recorded mask | **ASSUMED — task 0e proves it via `silhouette_masks --anchor` (0 differing px) before any upload** |
| 6 | The pale/register instruments reproduce every published R2-c and register row before measuring anything new | **ASSUMED — task 0f; the G5/G5b anchor forms are built and were green at the close** |
| 7 | `facet_E33/E34/E35` + the eight subtrees verify 0/0/0 via `tree_manifest` | **MEASURED at the E35 close; re-verify at open and close** |

## The baseline and the floors — the numbers every band is set against

| | view-1 recorded (seed 770700, R3 prompt) |
|---|---|
| pale area / L\*-rise | **278 px² / 4.97** |
| dark census / area | **16 / 157 px²** |
| register C\* | **23.77** |
| reg-IoU | **0.9372** |
| **seed-noise floor (2a, 3 seeds)** | **count 7–26 · area 34–139 px²** — a result inside the floor is a re-roll, not a signal; every band states its position relative to the floor |
| pale-region chroma, recorded | 23.25 (the chroma-split column reads signature, not just magnitude) |

## ⚠ The prompt ruling that binds every arm

The arms run **the RECORDED R3 prompt** (`E34-twin-prompts-r3-8view.json`, armclay_1 —
sixteen terms ending *"…unglazed terracotta, matte sculpted clay, soft studio
light"*). The r3L probe ("flat even lighting") **edits a ruled register term and is
the Director's to veto** — its own file says so — and Ruling 1's "adopted into
prompt v-next" overstepped: adoption awaits his ratification, surfaced in the
advisor handoff. One lever per arm means the prompt does not move while the control
or the init does. r3L's measured numbers (pale 226/4.09, dark flat) stand in the
record as the term's own evidence when he rules.

## The arc, task by task

**Task 0 — mechanics, zero cloud.** E15 ritual (scratch db, 19/19 or stop);
watchdog heartbeat ADVANCING (two reads, not the starter's exit code); manifests
(premise 7). Then:
- **0d — THE STRUCTURAL ANCHOR (1 job).** Emit the dual-control payload **from the
  recorded payload by structural transform in code — never retyped** (the prompts
  file's own discipline): add one `LoadImage` (the depth map) and one
  `ControlNetApplyAdvanced` chained ahead of the recorded canny apply, conditioning
  rewired through both. Link-sanity in code (self-links, dangling targets — the E04
  G7 law: a `dry_run` PASS proves nothing). Submit at **depth strength 0.0**, all
  else byte-recorded. **Gate: pixel-identical to the recorded twin, or a uniform
  residual at the E33 float floor (ΔE ≈ 0.84, uniform shape).** Structured
  difference ⇒ the rewire itself perturbs ⇒ HALT, report, arm 2 never fires.
- **0e — the flat-init render, zero cloud.** `silhouette_masks`-gated re-render of
  view-1 clay under `--flat` at the recorded invocation (recorded script, recorded
  frame 352×1024). Gates: `--anchor` 0 differing px against the recorded mask
  (geometry unchanged, shading only), then the **unique-colour count** — below the
  clean family (~5,000), one lanczos round-trip (the E35-measured repair), and the
  round-tripped file's mask re-anchored. Both numbers in the report.
- **0f — instrument anchors.** The pale instrument and `t2_register_all.py
  --twins` reproduce every published R2-c row (278/4.97 · 932/12.99 · 1220/19.68 ·
  the three ladder rungs) and the register rows **to the digit** before any arm is
  measured. A failed anchor halts the arc, not the instrument.

**Task 1 — ARM 2, dual control (1 job).** The 0d graph with depth strength
**0.80, start 0.0, end 0.45** (consult #1's schedule, environment-validated,
provenance stated on the sheet) · canny apply at **0.45, full schedule** (the
recorded canny control image, locally built as always — nothing cloud-side
preprocesses anything) · seed 770700 · denoise 0.92 · steps 20 · cfg 2.5 · shift
3.1 · euler/simple · 352×1024 · R3 prompt · no LoRA. Depth control =
`armclay_1_depth.png` as uploaded input. Blind bands sealed in a commit BEFORE
submission, three branches per hypothesis with the UP branch live, every numeric
band stating its position against the seed floor.

**Task 2 — ARM 1, the flat init (1 job).** The recorded graph unmodified; the only
delta is the 0e init. Same band discipline.

**Task 3 — ARM 3, combined (≤1 job).** Only if arms 1 and 2 each improved at least
one class without worsening the other, breaking the register floor, or losing the
man. The pre-registered rule is code, not judgement — write it in the bands file
before task 1 runs.

**Task 4 — sheets and the halt.** Per arm: full-size sheet beside the recorded
twin + the head band at 3x (the surface his eye reads); columns carry pale
(area, L\*-rise, **chroma-split signature**), dark (census, area, % of figure),
register C\*, reg-IoU. The pale class is read by instrument only — no eye-claims
at working zoom (the C3 law). **HALT at each sheet for the Director's eye.**
Identity and register are his; the class numbers carry the class verdict.

**Mechanical vs content, defined here so no seat re-litigates it:** validation
failures, black/degenerate frames, and corruption signatures are MECHANICAL — one
repeat per arm. Class numbers, register values, and identity are CONTENT — never
repeated, whatever they say.

## Artifact homes and report conventions

Everything lands under `E:\AI\training\facet_E36\` (+ repo tools/tests/docs);
`facet_E33/E34/E35` and the eight subtrees are read-only behind `tree_manifest`.
The report is `E36-route-arms-report.md`; bands are
`E36-route-arms-blind-bands.md`, sealed by commit SHA before the first job and
scored hit/miss/mixed in the report. Payload sidecars record full parameter sets
per job. No judgement words anywhere. Spend ledger per job in the report.

## Out of scope

The corrector-contract track (its own spec, local) · the r3L prompt ratification
(the Director's) · the `_depth_far` variant (contingency, his word) · any
8-view rebuild (his word at a sheet) · Qwen-Image-Edit-2509 in any form (closed
worse by E35) · partner texture nodes (closed identity-blind by schema) · edits to
any protected tree or accepted asset.

## Budget — REVISED by this amendment

**Ceiling 15**: 0d anchor 1 · arm 2 = 1 · arm 1 = 1 · arm 3 ≤ 1 · the eight-view
rebuild on a Director-picked winner = 8 · contingency 3 (one mechanical repeat per
arm). The anchor is not optional and not contingency — it is the first job of the
arc, and Ruling 6 is why.
