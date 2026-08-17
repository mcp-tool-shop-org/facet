# E49 — finish the candidate: orphan fill from source, erosion at its stated floor

**Written 2026-08-16, night** by the advisor seat, on the Director's direction after E48
(he judged E48 a clear step up with room to go further). One Sonnet executor seat,
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

- 2026-08-16, night — dispatched on the Director's direction to finish it, alongside Grok
  consult #10 (the improvement question).
- 2026-08-16, late night — **three Director rulings recorded** while this seat ran:
  1. **SLEEVELESS STANDS.** *"The reference image is sleeveless, I don't have
     preference."* N3 is unchanged; the armhole smear is tunic paint crossing onto
     unnamed flesh, and the repair is naming the bare arm and the cut — never a
     garment (consult #10's Amendment-15 reading, confirmed).
  2. **W3 IS THE EXEMPLAR, not a character.** He ruled it is not a real character but the
     exemplar for the humanoid. Its job is to prove the humanoid route; identity
     decisions on it need completeness and fidelity to the reference, not taste
     rulings per element.
  3. **THE CRUX, as he named it: the canon was never properly built out.** The audit
     agrees, and every defect region he circled is an unnamed surface or joint. The
     studio constitution's own line — dense canon produces a trainable style, thin
     canon produces noise — measured at twin level.
     ⚠ **The audit's arithmetic is CORRECTED 2026-08-17.** It read "the recorded
     generation prompt names six elements", which welded two files into one claim.
     Measured at the fold: the workflow that generated the twins
     (`facet_E08/ARMB/out/stroke_1_y+090_e+00_workflow.json:181`) carries **16 of 17**,
     missing only N17; the **six** is `profiles/character.json`'s brush default. The
     surviving finding is the sharper one — grip/gauntlet/greave/hand are zero in the
     16-phrase prompt because **the canon has no element for them**, so no prompt could
     have named them. W3 surface coverage measures **20 of 24, 0.833**; the four holes
     are both hands and both greaves.
  Follow-on: the **W3 canon build-out** — the complete named-surface table drafted
  from the reference (own phrase per surface, boundary pairs named, occupancy marked),
  ratified by the Director in one pass, then the twin regeneration from it. The
  durable studio artifact alongside: a humanoid canon completeness checklist in the
  character profile, so the next character starts complete instead of rediscovering
  this. Consult #10's sequencing stands: E49 lands → his three crops re-cut → the
  free per-region disagreement measurement → the canon-fed regen on his credit word.
- 2026-08-16, close of session — **DIRECTOR'S RULING on the E49 sheets: accepted, with
  one new defect class named.** The strongest acceptance signal
  this route has received, with one new defect class: flat-coloured angular patches
  (green/yellow/orange triangles on the tabard and skirt, a gold triangle on the
  boot). **Hypothesis, unverified, checkable in one overlay:** this arc's own fill
  passes are the carrier — atlas islands at this fragmentation are often single mesh
  triangles; the orphan fill painted each flat from a best-facing twin sample taken
  with the UNERODED sil, so a boundary-adjacent sample imports the neighbouring
  material and flat-fills a triangle-sized island with it. The provenance masks
  (`orphan_fill_mask.npy`, `no_view_visible_mask.npy`, per mode, under
  `E:\AI\training\facet_E49\atlas_*_eroded\`) were tagged for exactly this question:
  overlay the Director's crop regions against them; if the shapes sit on filled
  texels, the class is confirmed and the fix is the never-seen-surface POLICY already
  on the decision list — neutral per-material fill instead of twin-sampling at
  boundaries, or eroded-sil sampling with a palette gate for the visible orphans.
  Next session opens here: (1) the overlay confirmation, (2) the policy decision to
  the Director with the crops beside the masks, (3) then the standing sequence
  (disagreement measurement → canon build-out → regen).
