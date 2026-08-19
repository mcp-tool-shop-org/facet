# E63 — the head probe, on the views that actually turn

**Advisor spec, 2026-08-18. Executor: this session (Grok). Working tree
`E:\AI\training\facet_E63\`.**

**Spend: 4 generations (Arm P and Arm C, on views 3 and 5).** Same two arms E59
chartered, sent to the two frames that carry the defect. E59's two credits bought
no test of this question; this arc is the correction, not a new lever.

**Direction (standing, the Director, 2026-08-18):** the head stays aligned with the
body through the turnaround. He closed identity on the E58 ring. He then told this
seat to stop waiting for another gavel and move the project.

---

## Why this arc exists

E59 Stage 0 stands (`stage_head_forward` is `required: true`). Everything past it
is void. The spec sent the probe to **view 2 (yaw 90°)**. Walked at full size:
that head is already in profile, aligned with the body. The defect is the
**rear-quarter views**:

- `E:\AI\training\facet_E58\ring\a1_ring_v3.png` (yaw 135°) — back to camera,
  head cranked over the shoulder to face the viewer
- `E:\AI\training\facet_E58\ring\a1_ring_v5.png` (yaw 225°) — same class

Re-confirmed by opening both files at the start of this spec. Neither was in
E59's "definitely turned" calibration set. Gate 1's firing is therefore
confounded and is **not** an instrument finding. E59 Arm P and Arm C are not
evidence about the head. Arm C on the wrong view also washed the garment to
pale sage (denoise 0.92 → 0.80 is a badly adverse lever **on that view**; it
is re-tested here because the view was wrong, not because the lever is assumed
safe).

E58's own prompts file put every ratified phrase in every view, including the
face. That is the mechanism of the crank: a rear camera was told about the
smile. This arc does **not** drop face phrases (that is a later per-view
scope job, and A1's `scopes.views` is still empty). It asks the narrower
question E59 actually asked, on the views that can answer it.

## The question

On the two views where the head is cranked toward the camera: does naming the
canon clause in the text straighten it, or does the control need more authority
against denoise?

## What is already known (measured)

- Geometry is not the cause. Mesh head is straight; E57 clay ring is straight
  at every yaw. The generator overrode a correct control.
- Venue is not a variable. E58 / E60 / E61 all reproduced
  `canon/A1_reference.png` pixel-identically at seed 106.
- E58 v3/v5 recorded graphs: seed 770700, `lora_w` 0.75, `cn` 0.9,
  **denoise 0.92**, 576×1024. Positive text is the E58 flat list and does
  **not** contain `head facing straight ahead` (the clause landed after that
  ring). Negative text is the stock Qwen CJK block.
- Do not use the E59 head/torso IoU readout as a verdict. Its calibration
  populations were not distinct.
- **The E58 positive text is now illegal.** `require_canon` refuses it:
  N1 is now `a sleeveless plum long-vest...`, and three required staging
  clauses (arms/hands/feet) plus the head clause are absent. A byte-identical
  E58 splice cannot be submitted. Disclosed, not papered over.

## Arms — one variable between P and C; a disclosed confound vs E58

Base: E58's own `graph_3.json` / `graph_5.json`, loaded verbatim for every
node except the named ones. Controls, seed, LoRA, cn, frame stay.

- **Arm P (today's legal prompt).** Positive text is `canon_compose` flat
  form for A1 (gate-legal, already includes `head facing straight ahead`
  because the clause is `required: true`). Negative text gains the
  CJK-comma complement `looking at the viewer, head turned toward the
  camera`. Denoise stays 0.92. ⚠ Versus the E58 defect this is more than
  one word: sleeveless is in N1, staging clauses are present, the head
  clause is present. The garment join is still a flat list (E61: that
  form holds the sleeve). The confound is named; do not pretend P is a
  one-token splice.
- **Arm C (control authority).** Arm P's text, plus **denoise 0.92 → 0.80**.
  One knob against P. If the head is still cranked under Arm C, the next
  arc raises `cn` strength; do not raise it here.

Every graph passes `canon_gate.require_canon` before it is written. Gate E:
delivered frame equals 576×1024 or that view halts.

## Sheet

For each of v3 and v5, one row:

control | E58 defect | Arm P | Arm C

Head-region crop large enough to rule on, full figure beneath. Native PNGs
untouched on disk. Rank nothing. Do not score plum-going-brown as a result
of this arc; if a panel happens to show it, say so in one sentence and leave
it.

## Out of scope

Per-view prompt drop (empty scopes); raising `cn`; a full eight-view regen;
the ink reading (closed); W3; painting; plum-going-brown as a question
(E58, still waiting, its own arc).

## Predictions

Recorded before any submit, falsifiable on the sheet.

**Advisor: Arm P will not clear the crank.** On a rear-quarter view the
face-toward-viewer prior is the defect itself, not a side effect. Naming
`head facing straight ahead` fights that prior; it is not obvious the
fight wins at denoise 0.92. **Arm C is the arm that can win**, if either
does — more of the (correct, rear-facing) control survives. If P clears
both views, that prediction is wrong and the identity-law reading
(name it and the prior yields) extends to turnaround pose. If both fail,
the next lever is `cn`, not another text splice.

No numeric prediction. The E59 instrument is not available.

## Spend and compensators

| action | undo | owner |
|---|---|---|
| 4 generations | **NONE** | this seat |
| `docs/experiments/E63-*`, bound bump | pathspec revert | this seat |
| tree `E:\AI\training\facet_E63\` | delete | this seat |

`estimate_credits` and `dry_run` before submit, reported. Same workflow
shape as E58/E59: estimator will likely read 0 metered API nodes; that is
not a free-generation claim (GPU-seconds).

## Dispatch record (living)

- 2026-08-18 — spec written after the Director named the stall. Views
  confirmed by opening `a1_ring_v3.png` and `a1_ring_v5.png` at spec time.
  E59 Arm P/C are not in the evidence set.
