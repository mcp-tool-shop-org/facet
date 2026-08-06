# E10 Ruling 4 dispatch — pos.npy off-surface consumer measurement: PREDICTIONS

**Executor session, 2026-08-05. Written BEFORE any measurement ran.** Blind status:
these predictions were written after reading the consumer tools' source, the recorded
artifacts (`provenance.json`, `finalize.json`, `run_log.jsonl`, `offsurface.json`, the
stage-1 report) and the E10 rulings — and before computing any new number. No
classification of the off-surface population and no consumer recompute existed when
this file was hashed. The hash is printed in the session log before the first
measurement runs, and the report quotes it.

## The dispatched question (Ruling 4, verbatim scope)

Per consumer, **does excluding the off-surface 2.5% move your headline number** —
read-only, no route tool edited, no accepted number presumed wrong. Blast-radius
order: `e08_ceiling` / `e08_acceptance` → `texpass_finalize` → `project_twins` /
`commit`.

## Definitions, fixed before measuring

- **Off-surface**: distance from the texel's reconstructed canonical position to the
  mesh surface **> 1 image px** (0.0011216247 canonical units — `offsurface.json`'s
  recorded `one_image_px_in_canonical_units`), the population recorded at **2.5065%**
  of 3,111,817 uv-valid texels. The >5 px variant (2.0940%) is reported as a
  diagnostic column, not read against the predictions.
- **Excluding**: off-surface texels are removed from **both numerator and
  denominator**; the headline is recomputed on the remaining (on-surface) population.
- **"Moves"**: a change at the precision the record quotes — 2 decimal places for the
  mix percentages and the ceiling (42.72 / 36.89 / 6.87 / 56.24), 1 dp for 86.4,
  exact integers for texel counts. Integer counts will almost certainly change by
  *some* texels; the deltas are reported and their meaning is the ruling's, not this
  session's.
- **Anchors before any recompute is believed**: (a) restricting the full
  classification to the recorded rng(0) 200,000-sample indices must reproduce
  `offsurface.json`'s digits; (b) the ceiling replica must reproduce **1,329,359**
  reachable; (c) the class reconstruction must reproduce `provenance.json` exactly
  (1,147,959 / 213,852 / 1,750,006, and the six per-stroke counts for the replay).
  A failed anchor is a HALT on that consumer, not a substitute number.

## Predictions

**P0 — composition of the off-surface population** (~78,000 texels): they concentrate
in the class no camera ever painted. Predicted split: **≥ 85% dilation-class**,
**≤ 10% stage-1**, **≤ 5% brush**. Mechanism: the suspected origin is bake
padding/gutter — positions with no surface are unlikely to pass a facing+visibility
raycast toward any camera, so they were never paintable and the flood inherited them.

**P1 — `e08_ceiling` (recorded 42.72%, 1,329,359 / valid).** MOVES UP. Point
**43.4%**, range 43.2–43.6. Mechanism: off-surface texels reach at well below the
population rate (predicted off-surface reach rate 10–25% against 42.72%), so the
denominator shrinks ~2.5% while the numerator loses little.

**P2 — `e08_acceptance` (recorded styled/valid 36.89%, styled/reachable 86.4%).**
styled/valid MOVES UP: point **37.4%**, range 37.2–37.7. styled/reachable: point
**86.6%**, range 86.2–87.0 — direction honestly uncertain (both operands lose
members; the sign depends on whether off-surface *reachable* texels were accepted at
a lower rate than on-surface reachable ones, which nothing recorded answers).

**P3 — `texpass_finalize` (recorded dilation 56.24%, 1,750,006 / valid).** MOVES
DOWN. Point **55.4%**, range 55.1–55.7. Mechanism: P0 — the excluded population is
mostly dilation-class, so dilation loses ~66–75k texels against a denominator loss of
~78k. Scoping fact to carry into the report: the shipped galleon finalize ran
`"mode": "atlas_flood"` — the `pos.npy`-consuming surface-aware branch (line 82) did
not execute on this asset's shipped run; the headline share is still the dispatched
question.

**P4 — `project_twins` (recorded stage-1 1,147,959 = 36.89%).** Count loses
**≤ 8,000 texels (≤ 0.7%)**; share moves UP to point **37.4%** (same range as P2's
first number — same artifact, this consumer's own question). Mechanism: stage-1
acceptance requires facing+visibility+edge+mask; an off-surface position passes that
chain at well below the population rate.

**P5 — `texpass_iter` commit (recorded per-stroke 26,531 / 22,766 / 17,904 / 24,486 /
63,288 / 58,877; brush total 213,852 = 6.87%).** Each stroke loses **< 2.5%** of its
count (below the population rate — the brush paints where emit rendered surface);
brush total loses **≤ 4,000 texels**; share moves UP to **7.00–7.06**, point 7.02.

**P6 — full-bake rate.** The full 3,111,817-texel classification lands within
sampling noise of the recorded sample: **2.51% ± 0.06** for >1 px.

## Pre-registered readings (from the dispatch, restated)

A number moves at its quoted precision → report the delta and halt for the
correction-in-place ruling. Nothing moves → one paragraph in the record and silence
thereafter. Either outcome is a full success; nothing is tuned toward either.
