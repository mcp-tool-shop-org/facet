# E10 W2 / W2b / W2c — the element does not land. Three arms, one variable each. HALT.

**Executor session, 2026-08-05.** Run under [E10 Ruling 7](E10-ruling.md), which
pre-registered this halt: *"If W2c also fails, halt: that's a real finding about masked
inpainting over context, and it gets written up as one, full success."* It failed.
Written after the work; **0 credits across all three arms.**

---

## The result

L1 asked for **a weathered tallow-white hull coat below the waterline**. All three arms
returned dark hull planking.

| arm | prompt | what the model saw in the band | painted L\* | ΔL\* vs base | dE median |
|---|---|---|---|---|---|
| **W2** | L1 + the ship's twelve + style tail | the base's dark planking (occupied) | 4.0 | **−3.9** | 5.00 |
| **W2b** | L1 + style tail only, incumbents struck | the base's dark planking (occupied) | 3.9 | **−4.1** | 6.08 |
| **W2c** | L1 + style tail only | **the accepted runs' hole colour, rgb(107,107,107)** | 5.5 | **−1.6** | 5.18 |

Base at the band: L\* 7.1–7.9. A tallow-white coat is an L\* in the seventies or
eighties. **Every arm came back darker than the planking it painted over.**

Striking twelve competing elements from the prompt moved the result by **0.1 L\***
(4.0 → 3.9). Replacing the occupied context with absence moved it by **1.6 L\***
(3.9 → 5.5) — the largest single move, and still the wrong direction from what was asked.

## Each arm changed exactly one thing, and it was proven by diff

Not asserted — the two workflow JSONs were compared field by field before each submission:

```
W2  -> W2b   differing inputs: 1     node 7 CLIPTextEncode.text        ONE VARIABLE
W2b -> W2c   differing inputs: 1     node 9 LoadImage.image            ONE VARIABLE (the render)
```

The mask is byte-identical across all three: re-uploading it returned the **same
content-addressed name** (`943ae871…`) the first arm flew on — a check that could have
failed and did not. And W2b's render reproduced W2's sha exactly (`26B0AE99…`) after a
`--force` re-seed, so the prompt really was the only thing that moved between them.

## W2c's context value is precedent, not a choice

The hole colour was **measured from the accepted asset**, not picked: in E04's stage-1
atlas, **1,963,858 of 1,963,858 hole texels — 100.00% — are rgb(107,107,107)**. That is
exactly what the brush saw at a hole in all six accepted E04 strokes. Choosing white would
have been steering toward the answer; choosing black toward the failure. The precedent had
one value and it was used.

## A measurement error I made and caught

W2c's first band measurement read **L\* 45.2, C\* 0.0, ΔL\* +37.3** and would have looked
like a spectacular success. It was wrong. The measurement defined the layer's texels as
*changed vs the base*, which is correct when the layer state is seeded as a base copy — and
**silently wrong under hole-fill**, where all 98,543 contact texels differ from the base
before a single one is painted. L\* 45.2 / C\* 0.0 *is* rgb(107,107,107); I was measuring
the grey fill.

The honest denominator is what the commit actually wrote — `styled_mask ∩ contact`, 12,836
texels — and against that the number is L\* 5.5. **The same defect is live in
`e10_layer_export.py`**, whose `owned = contact & changed` would have exported an 85,707-texel
grey band as layer content. It was not run after W2c. Flagged, not patched: it is a real
tool defect and it belongs in a ruling, not in a quiet edit at the end of a failing arm.

## What did work, stated separately so the negative does not bury it

Every piece of the layer *mechanism* held under three live generative commits:

- **base-invariance** — `galleon_final.png` byte-identical after all three, asserted inside
  the tool with no skip flag, every time
- **`--restrict`** — 0 texels changed outside the contact mask in every arm
- **invar ANDON** — largest hot component 5 px, 1 px, **0 px** against the 200 bound
- **the two-lane pre-flight** — corroborated the layer lane against the job's state identity
  on every graph build
- **the export contract** — RGBA straight-alpha, dilation ring present, **alpha moved 0 px**,
  composite verified exact as `over`
- **transport** — link topology checked in code each time; **0 credits** across three
  submissions

## What is NOT established

- **Why.** Three candidates are consistent with the data and none is tested: the ControlNet
  inpainting conditions on the render, which carries the dark surround; the band is ~2.3% of
  frame and 1–2% of the figure's height; the LoRA has learned this subject's hull materials
  from a corpus in which hull-foot means dark. Nothing here separates them.
- **Whether a different element would land.** L1 is a pale material asked into the darkest
  region of the asset. A dark boot-top — tarred black, which the Director's open window in
  `E10-LAYER-IDENTITY.md` already names — is the same experiment with the value the model
  keeps returning anyway, and would confound "the element landed" with "nothing changed."
- **Whether the layer mechanism can carry content at all.** It carried *something* three
  times, committed it cleanly and toggled it. What it has not yet carried is content that
  differs from what the base already had.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | three saved workflow JSONs; one-variable proven by field-level diff before each submission; the hole colour measured from the accepted asset with its count |
| ANDON_AUTHORITY | 3 | invar fired-clean three times; base-guard asserted in-tool three times; the halt is the spec's own pre-registered branch, taken rather than extended to a fourth arm |
| NAMED_COMPENSATORS | 3 | 0 credits; every arm's artifacts preserved under `W2_record/`, `W2b_record/`, `W2c_record/`; undo is deleting `e10_layer/` |
| DECOMPOSE_BY_SECRETS | 3 | the layer lane's fixture carried the change in all three arms; no tool constant moved |
| UNCERTAINTY_GATED_HUMANS | 3 | halted at the pre-registered point with three candidate causes named and none asserted |
| EXTERNAL_VERIFIER | 2 | the measurement error was caught by re-deriving the denominator, not by an independent instrument. Not 3: no second party has measured these bands |
