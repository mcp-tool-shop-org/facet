# E48 — a complete candidate render, or this route is done

**Written 2026-08-16, late** by the advisor seat, immediately after the Director rejected
all four E47 cells (*"I don't see any recovered images. They all still look broken."*).
One dispatched executor seat (Sonnet), background, working `E:\AI\training\facet_E48\`.

## The question, and the stakes

E47 rendered diagnostics: no fill, sentinel lace on every boundary, patch seams. The
Director judges assets, and he is right that a diagnostic is not one. This arc produces
**complete candidate renders** — the rebuilt-atlas route finished end to end — so the next
artifact his eye rules on is an actual asset. **Pre-registered stop condition: if these
fail his eye, the rebuilt-atlas route is DEAD at his word** — no further polish arcs on
it; the from-scratch question reopens.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Committed tools at stated HEAD; every stage manifested (hashes, versions, parameters); derived inputs recorded as derivations, never mutations of the E45 bundle. |
| ANDON_AUTHORITY | 3 | Gate S selftest lines; the anchor run; erosion bounded by the shipped A3 rule (min(2.5 px, 1/3 local half-width)) with per-structure removal reported; fill confined by the island grid with an ANDON if any fill crosses an island boundary. |
| NAMED_COMPENSATORS | 3 | All writes under `E:\AI\training\facet_E48\` + one report doc. Compensator: delete the tree; owner = advisor. |
| DECOMPOSE_BY_SECRETS | 3 | Build/run/fold/judge separation unchanged; the seat creates no repo tools. |
| UNCERTAINTY_GATED_HUMANS | 3 | The terminus is two complete renders beside the shipped one and the reference; the stop condition is pre-registered above, before any result exists. |
| EXTERNAL_VERIFIER | 2 | Runner ≠ builder ≠ judge. Not 3: no second seat re-runs; manifests make every stage replayable. Owner = advisor. |

## The chain

0. **Gate S:** `atlas_from_aovs.py --selftest` prints `calibration atlas[16,16,0] == 0.5`;
   anchor run reports |bmid| 0.000e+00, valid 2,402,810. Else halt.
1. **Sampling-trust erosion (the boundary class).** E46/E47's boundary residue is twin
   edge-bleed: anti-aliased twin edge pixels and warp-displaced paint sampled at
   occlusion boundaries. The shipped route killed this with the A3 erosion —
   `edge-dist = min(2.5 px, 0.333 × local half-width)` (the exact rule is in
   `tools/project_twins.py`; not import-safe — copy the erosion with citation, the E41
   pattern). Build a DERIVED aov dir under the training tree: copies/links of the E45
   bundle per view with `sil` (and therefore the weights) eroded by that rule.
   **Report per view and per structure-width band how much area the erosion removed**
   (the A3 stratum discipline — thin structures are where a fixed peel kills; the local
   half-width cap is the guard). Do not touch `E:\AI\training\facet_E45\aov\`.
2. **Paint both modes, flow off only** (E46/E47 measured flow as a trim; one variable
   fewer): `atlas_from_aovs --mode owner` and `--mode blend` over the derived bundle.
3. **Island-aware fill.** Fill unwritten valid texels by nearest written texel WITHIN
   the same island — the island labels are recorded at
   `E:\AI\training\facet_E08\ARMB\cache\isl_grid.npy` (verify its shape/semantics
   against its producer before use; it is an ASSUMED premise). An island with zero
   written texels gets the island's nearest-island... NO — it stays sentinel and is
   REPORTED (count + total area + largest); never fill across an island boundary
   (ANDON if the implementation would). The island-blind flood is the documented
   dark-mark mechanism; within-island nearest-valid is the bounded form.
4. **Render complete.** Both filled atlases into the shipped GLB (the E47 seat's
   render mechanism — read its scripts under `E:\AI\training\facet_E47\`, reuse with
   citation), all 8 views, flat. PowerShell, `-b -P` only.
5. **The sheet.** Per view: `reference twin | shipped | owner-complete | blend-complete`,
   native pixels, provenance captions, plus blade/grip/head crops at 2× for views 0, 1,
   2, 7. This sheet is the deliverable.

## Predictions (seat's own, before step 2, blind status disclosed)

Per view 0/1/2: whether any sentinel remains visible at full-figure scale after fill
(with the zero-written-island count as the mechanism); the erosion's area cost per
thin-band; and a band on |render Δ| between eroded and E47's uneroded cells at the
boundary strips. State each instrument's reading at nothing-changed and at
maximum-effect first; predict inside.

## Rules

The standing executor set: no quality judgments anywhere; halt at fired gates; negative
result is a full success; no commits, no memory writes, no tool/test/count-surface
edits; only repo file is `docs/experiments/E48-complete-candidate-report.md`; handoff.md
first and current; ASCII; absolute python; manifests everywhere; read listings complete.

## Dispatch record

- 2026-08-16, late — dispatched immediately after the E47 rejection, with the stop
  condition pre-registered above.
