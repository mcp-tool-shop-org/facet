# E49 — finish the candidate: orphan fill from source, erosion at its stated floor

**Written 2026-08-16, night** by the advisor seat, on the Director's direction after E48
(*"This is honestly a lot better, but we can do better."*). One Sonnet executor seat,
background, working `E:\AI\training\facet_E49\`.

## The two repairs (both were the advisor's spec defects in E48)

1. **Orphan islands get paint from the SOURCE, not from neighbours.** E48 left 1,803
   (owner) / 3,625 (blend) islands sentinel because no within-island source existed. The
   repair samples the twins directly: for every texel of a zero-written island, project
   its position into its best-facing view (facing^6 argmax over views where the texel is
   visible by depth test) and sample that twin with the UNERODED sil — these are exactly
   the texels the erosion orphaned, and paint-from-source is not the island-blind
   neighbour flood (the dark-mark mechanism stays dead; state this in the report).
   Orphan-fill texels are tagged in a mask output so their provenance is separable.
2. **Erosion capped at its stated floor.** E48's ed_body ran 2.79–4.17 px against the
   spec's stated 2.5; rebuild the derived bundle with the cap enforced exactly
   (min(2.5, third-of-half-width), no escalation term), report the per-band area cost
   beside E48's table.

Then: repaint both modes (flow off), island fill as E48 (within-island), orphan fill as
above, render all 8 views, and rebuild the E48 sheet set (reference | shipped |
owner-complete | blend-complete + the same crops). The sheet is the deliverable, and
this time complete means zero sentinel in the render or the count reported loudly.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Same manifest discipline as E48; every stage cites the E48 script it derives from. |
| ANDON_AUTHORITY | 3 | Gate S selftest + anchor; cross-island neighbour fill still raises; orphan fill that would sample a view where the texel fails the depth test raises. |
| NAMED_COMPENSATORS | 3 | All writes under the training dir + one report doc; compensator delete; owner advisor. |
| DECOMPOSE_BY_SECRETS | 3 | Run-only seat; no repo tools. |
| UNCERTAINTY_GATED_HUMANS | 3 | Terminus is the sheet for the Director's eye. |
| EXTERNAL_VERIFIER | 2 | Manifests make it replayable; no second seat. Owner advisor. |

## Rules

The standing executor set, unchanged from E48's kickoff: no quality judgments, halt at
gates, negative result is a success, no commits, only repo file is
`docs/experiments/E49-finish-and-cap-report.md`, handoff.md first and current, ASCII,
absolute python, Blender via PowerShell `-b -P` only, manifests everywhere, predictions
before painting (sentinel share after orphan fill — the instrument's floor is 0 and E48
measured 5.05/11.96 without it; predict inside).

## Dispatch record

- 2026-08-16, night — dispatched on the Director's "finish it" direction, alongside Grok
  consult #10 (the improvement question).
