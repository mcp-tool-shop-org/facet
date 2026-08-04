# E04 Step 0 — HALT on anchor 1c. The gate fired on its own instrument's noise.

**Executor session, 2026-08-04.** Step 0 item 1 (fit-axis) is **implemented and its character
anchors pass**. Its ship anchor **fired**: 0.28% against the spec's ≤ 0.24%. Halting as
dispatched. **Items 2–4 not started**; no measured arm has run.

---

## What was built

`turn_render.py` and `silhouette_masks.py` both gain `--fit-axis {height,width}` and
`--margin`, **in one change**, with the identical warning block at each framing site naming
the other file. `turn_render` now sets `sensor_fit` **explicitly** rather than leaving Blender
to pick the larger axis — which is how height-fit was correct by accident on W3's portrait
frame and silently became width-fit-at-a-height-scale on the galleon's landscape one.

## Anchor 1a/1b — character path, flag unset: **PASS**

| | result |
|---|---|
| `turn_render --flat`, views 4/5/6 vs the banked E08 renders | **0 differing px of 770,048, max channel delta 0** — all three |
| `silhouette_masks`, views 0/4 vs `ARMB/masks/w3clay_*` | **byte-identical** |

⚠ **My first check reported HALT and was wrong, on a unit this repo has already corrected.**
I hashed the PNGs; the renders differ in file bytes and are **pixel-identical**. E08's eightcam
report banked exactly this — *"that run recorded sha b12917a2, re-ran to 6589e61a, and was
pixel-identical to both historical atlases. **File bytes are not pixel values.**"* I used the
retired unit and got a false halt. Corrected before it reached a conclusion; noted because it
is the second time a hash has produced a false alarm here.

## Anchor 1c — ship at 1066×1024, `--fit-axis width`: **FIRED**

| view | silhouette bbox | clay bbox | disagreement |
|---|---|---|---|
| 1 | 716 × 849 | 716 × 851 | 0.24% |
| **7** | 716 × 849 | 718 × 851 | **0.28%** |

**0.28% against the ≤ 0.24% bound. The gate fired and I am not tuning past it.**

### What the 0.28% actually is — measured, not argued

The disagreement is **1–2 px** on ~716–851 px bboxes. Sweeping the clay threshold the anchor
uses, with the silhouette held fixed:

| clay threshold | view 1 (dx, dy) | view 7 (dx, dy) |
|---|---|---|
| 10 | +2, +2 | +2, +2 |
| 26 *(the anchor's)* | 0, **+2** | **+2, +2** |
| 45 | 0, +2 | 0, +2 |
| **70** | **0, 0** | **0, 0** |
| **100** | **0, 0** | **0, 0** |

**At threshold ≥ 70 the clay bbox matches the silhouette exactly — 0 px, both views.** The
registration is exact. What varies is how much **antialiased fringe** the threshold admits.

For scale, the failure this gate exists to catch measured **4.68%** — bbox 717×850 against
751×892, a 34×42 px gap that no threshold closes. This is 0–2 px that closes completely.

## Why I am halting rather than raising the threshold

Three reasons, and the third is the one that matters:

1. **The bound is a single reading of the same noisy statistic.** 0.24% is what *my* square-frame
   measurement happened to return at threshold 26. It was adopted as a bound without a noise
   floor ever being characterised. A pass condition set from one observation of an instrument,
   with no spread, is the failure mode this repo has now paid for four times.
2. **The instrument is a technique this repo retired.** `silhouette_masks.py`'s own docstring:
   *"The mask CANNOT be thresholded off the clay render."* Both 0.24% and 0.28% are readings
   of a keyed clay threshold — the exact method retired for being unreliable — so neither is a
   registration number. The anchor measures its own instrument.
3. **Choosing a threshold now would be retuning while looking at the result it would judge.**
   That is the one move this repo says is always wrong, whatever the reasoning. Threshold 70
   passes; I know that *because I ran the sweep*, which is precisely why I must not adopt it.

## What the advisor is asked to rule on

The instrument, not the number. A registration check that does not key a clay render is
available and cheap — compare the silhouette against the **raycast hit mask** at the same
camera, which is geometry against geometry with no threshold anywhere. If that is the anchor,
it has no fringe and its bound can be 0 px exactly.

**I have not built it**, because specifying the replacement for a gate that just fired on me
is the advisor's call and building it now would be the same retuning by another route.

## State

- Step 0 item 1: **implemented**, character anchors pass, ship anchor halted.
- Step 0 items 2 (cull superset), 3 (emit framing), 4 (profile check): **not started.**
- Arms G7 and T: **not started.** No generation, no spend.
- Code changes are committed and are additive — both flags default to the character
  convention, and the character path is pixel-identical with them unset.
