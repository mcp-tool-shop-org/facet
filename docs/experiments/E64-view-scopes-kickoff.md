# E64 — the scopes fill: a rear camera stops hearing about the smile

**Advisor spec, 2026-08-18. One executor seat (Sonnet), background. Tree
`E:\AI\training\facet_E64\`. Spend: 2 generations (v3 + v5), and they run only after the
Director ratifies the eight scope lists below.**

**The pick this executes (Director-confirmed):** per-view prompts via `scopes.views`,
restoring the E02 law A1 was built without. **cn stays on the shelf** as the named
fallback; it is not this arc.

## The mechanism, confirmed at the Director's own hand

E63's Arm P was composed at `view='front'` **even for yaw 135 and 225**. The composer has
known how to drop face clauses on a rear compose since E60 Stage 0 — that path was never
used, because the gate requires the face phrases at subject scope and a rear prompt could
not be submitted until `scopes.views` exists. **Filling the lists is the missing door, not
a new idea.** W3 never cranked because it was built under E02; A1 cranked in the exact arc
that overrode it. This is reversion to a measured-good state.

## The eight DRAFT scope lists — existing surface ids only, drafted from the E57 clay

The Director walked clay_3 and clay_5 himself and enumerated the rear lists; the advisor's
first draft omitted the hands (both palms are in the clay, N8 is canon) and that omission
is corrected here. **The seat writes these into `canon/a1.surfaces.json` `scopes.views`
marked DRAFT; the Director's word ratifies; the spend waits for it.**

| view | yaw | surfaces in scope |
|---|---|---|
| v0 | 0 | hair, face, eyes, mouth, neck, shirt_collar, vest_torso, vest_skirt, sleeve_L, sleeve_R, sash, trousers, shoe_L, shoe_R, hand_L, hand_R |
| v1 | 45 | same as v0 (front quarter — full face set visible) |
| v2 | 90 | same as v0 (profile — cheek, one eye, lips in profile keep the face set) |
| **v3** | **135** | **hair, vest_torso, vest_skirt, shirt_collar, sleeve_L, sleeve_R, sash, trousers, shoe_L, shoe_R, hand_L, hand_R** |
| v4 | 180 | same as v3 (straight rear) |
| **v5** | **225** | **same as v3** |
| v6 | 270 | same as v2 (profile, mirrored) |
| v7 | 315 | same as v1 (front quarter, mirrored) |

**Not on rear lists, by direction:** face, eyes, mouth, neck (the collar eats it), and
`style_face` — which is a legal_clause and structurally CANNOT appear in a surfaces array
(fence 4 below). Profile views showing a cheek keep the face set; **they are drafted here
for ratification but are NOT probed this arc.**

Route rows (silhouette, proportions, brushwork — mesh/style provenance) are not
spatial-visibility entries and stay out of scope lists; their handling is unchanged from
subject scope.

## Fences (the Director's, verbatim in force)

**1. Existing ids only.** No invented surfaces — no "vest back." The lists above are the
canon's own ids. A list entry that does not resolve as a surface id refuses.

**2. Emit from the scope list — never `compose(view='front')` for a rear camera.** That is
the E63 confound. Can-fail legs, both required: a v3/v5 prompt still containing *a slight
smile* or *curious brown eyes* or *crisp readable facial features* REFUSES; a v0 prompt
missing them still REFUSES (the front view keeps requiring them). `stage_head_forward` and
the arms/hands/feet staging clauses stay `required: true` at every scope — the gate
already checks those globally; leave that alone.

**3. Ratify, then spend.** The two generations are **v3 and v5 only, seed 770700, denoise
0.92, the E58 controls byte-identical, flat form** (E61: no coordinating *and*). One
variable against E63 Arm P: the per-view prompt. Do not raise cn. Do not regenerate the
ring. Profile views get their own lists; they are not this probe.

**4. `style_face` is a legal_clause, not a surface.** The composer omits it on rear views
**because the scope list omits eyes and mouth** — face-clause emission keys off the
scope's face-bearing surfaces — never by naming `style_face` in a surfaces array. Putting
a clause id in a scope list is an ANDON, not an implementation choice.

## Stages

0. **Wiring (free).** `check_prompt` at scope `view:N` requires the ratified
   prompt-provenance occupant phrases of in-scope surfaces plus every `required: true`
   legal clause; the composer emits from the scope list. Fence-2 legs proven by
   reversion. Census byte-identical (scopes are not occupant rows — the E62 lesson:
   occupancy never speaks for these fields). T34 counts move in-change-set if any
   collected test is added.
1. **Draft canon lands (free).** `scopes.views` written as above, marked DRAFT. The seat
   emits the v3 and v5 candidate prompts, records them in the report, and **HALTS at the
   spend gate** until the advisor relays the Director's ratification.
2. **The probe (spend 2, post-ratification).** v3 + v5 as fenced. Gate E stands
   (delivered frame == requested).
3. **The sheet.** Per view: control | E58 defect | E63 Arm P | E64 per-view, head crop at
   the Director's zoom. Beside it the two prompts, so what changed is readable.

## Out of scope, named

cn (the shelf); the full ring; profile-view probes; W3; any canon phrase edit; painting.

## Standards compliance

1. **PIN_PER_STEP — 3.** Seed, denoise, controls, and form all pinned to the E63/E58
   values; one variable moves.
2. **ANDON_AUTHORITY — 2.** Fence legs refuse via `raise`; the spend gate halts the seat
   until ratification is relayed.
3. **NAMED_COMPENSATORS — 2.** Two generations, no undo, gated on the Director's word;
   everything else reverts by pathspec.
4. **DECOMPOSE_BY_SECRETS — 2.** Wiring / canon data / probe / sheet are separable
   stages over on-disk artifacts.
5. **UNCERTAINTY_GATED_HUMANS — 3.** The scope lists are canon and the Director ratifies
   them BEFORE any spend — the gate is his word, structurally ahead of the generations.
6. **EXTERNAL_VERIFIER — 2.** The fence legs and the gate are deterministic; the sheet
   is his eye.
