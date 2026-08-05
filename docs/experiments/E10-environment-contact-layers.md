# E10 — environment-contact layers: the waterline as authored state

**Spec written before the work.** Advisor, 2026-08-05, under [Ruling 19](E04-ruling.md)'s
charter — the Director's own words: *"I want to be able to add the waterline like a
layer... The data that we'd learn from making that work could be applied to other models
in the future."* The founding exemplar is on disk and seed-reproducible: the rejected
view-7 twin (seed 770700) that painted 2,002 px of implied water at the hull's foot —
h 262.6, C\* 14.4, L\* 31.7, x 398–686, y 896–939 — eliminated by one seed increment,
which is the measured proof that **spontaneous contact is a roll, and anything that's a
roll can't be a feature until it's authored** (the executor's sentence, kept as this
spec's thesis).

## The question

**Can environment-contact content live in a separate accumulating layer — authored,
masked by geometry, provenance-tracked, toggleable — without touching one byte of the
accepted base asset?** The waterline is the first instance; the mechanism (contact mask +
layer state + compositing contract) is the product. Snow on boots, mud on wheels, moss on
ruins are the same shape with a different contact query, named here and tested nowhere.

## Phase 0 — research grounding, dispatched before architecture locks

Three questions, parallel agents, **Crossref-first citation gate** (Ruling 1's standing
correction — RG01 lost 28 of 32 citations to arXiv rate-limiting from one IP in one
window). Source standard: author + year + title + URL + one-sentence finding; 6–8
well-sourced findings beat 20 gestures.

1. **Layered/decomposed generation** — what is measured about diffusion inpainting into
   an alpha-carrying overlay vs diffing a full-frame edit against its base? This decides
   Arm W2's commit mechanics (direct layer generation vs base-composite-diff).
2. **Decal/detail-layer compositing conventions in engines** — the Godot/UE contract a
   layer atlas must satisfy (blend modes, sRGB/linear, mip behaviour at alpha edges).
   This decides the layer's file contract and the E09/sdlab channel role.
3. **Waterline/wet-band rendering practice** — how shipped games treat hull wetting and
   waterlines (texture band vs shader vs geometry); if the standard answer is
   shader-side, the layer's *content* may be simpler than painted water and the spec
   should know before generating any.

A negative finding — "diff-commit is unmeasured/unsound at this scale" — is a full
success: it changes the architecture before it exists.

## Hypotheses, predictions first

| # | hypothesis | prediction | blind? |
|---|---|---|---|
| W-H1 | the contact mask is geometry's job | a raycast band at the placed `waterline_z` covers ≥90% of the founding exemplar's observed band (the rejected twin's 2,002 px, y 896–939) on the matching view | yes — the mask does not exist |
| W-H2 | authored beats rolled | one masked generation into the band produces a waterline on the target view where the 1072 batch produced zero on eight | yes |
| W-H3 | the base is untouchable by construction | base `atlas_final.png` byte-identical through every layer operation, enforced in-tool, zero exceptions | yes — but designed-true; the gate proves the construction, the prediction is 0 violations |
| W-H4 | the composite reads | the Director, shown toggle renders (layer on / layer off) at his zoom, can say in one sentence whether the ship floats | his eye; not a metric |

## Step 0 — tool work, each item anchored (no generation until all pass)

1. **`waterline_z` is fixture data and the Director places it.** One render, three
   candidate lines drawn at measured z-fractions of the hull, one sentence from him picks
   (or moves) the line. Lands in `ship.json` with why + provenance. **His eye is the
   gate; the candidates are derived from the mesh** (hull lower extent + the founding
   exemplar's band top, projected to z — the exemplar is validation data, not the
   answer).
2. **The contact mask**: raycast texels whose surface z sits below `waterline_z` — the
   exact-silhouette family, no keying. Anchor: the mask is a pure function of mesh +
   plane (byte-stable across two runs); its per-view projection is checked against the
   exact silhouette (mask ⊆ silhouette, exactly).
3. **The layer state**: `texpass_iter` gains a layer mode — a second state directory
   (RGBA, transparent base) with the same emit/commit discipline and the same in-tool
   gates. **The base-invariance gate is BY CONSTRUCTION, then verified anyway**: the
   layer path never opens the base atlas for writing, and every layer commit asserts the
   base's bytes unchanged (hash recorded at layer-state seed; E08 A32's lesson — the
   check lives inside the tool, no skip flag). Anchor: a layer no-op leaves base and
   layer byte-identical; the character path is untouched by construction (no character
   invocation passes layer flags).
4. **The layer palette fixture** — authored forward like the galleon's: the sea family,
   seeded from the founding exemplar's measured colour (h 262.6, C\* 14.4) and the
   fixture words (*deep sea-blue-grey wash, foam-white lap line*), bounds null,
   report-only — first-run baselines, the E04 pattern verbatim.

## Arms — one variable each

- **Arm W1 (no generation): the mask.** Build the contact mask at the placed line;
  measure its per-view band against the founding exemplar's band (W-H1's number).
  Report band extent per view, texel count, and the mask ∩ silhouette check.
- **Arm W2: one authored stroke into the layer.** The beam view first (largest band).
  Masked generation, cloud, standing discipline (workflow saved, link-checked, dry_run,
  estimate_credits, pre-flight guard). Commit into the LAYER state under the geometry
  invar. Gates: base bytes unchanged (halt), layer palette report-only, invar at the
  standing bounds. The prompt names the water (*a deep sea-blue-grey waterline wash along
  the hull's foot, foam-white lap line*) — identity in the prompt, layer edition.
- **Arm W3: the composite and the toggle.** Renders at the three ruled sheet cameras,
  layer on / layer off, full size, beside each other. **Gate 1 of E10 is the Director's
  eye on the toggle pair** — does the ship float. His sentence closes the arm.

## Metrics

W-H1's coverage fraction · the layer's own provenance (all texels stroke-class inside
the mask, zero outside — the mask is the gate) · base-invariance violations (must be 0)
· per-view layer palette report · the toggle sheet.

## Gates

Step 0 anchors (byte-identity, halt on any digit) · base-invariance in-tool, no skip ·
the mask ⊆ silhouette check · palette report-only (no bounds — no baseline exists) ·
suspend rather than invent everywhere else · Gate 1 is the Director's.

## Out of scope

Training on layer data (the sdlab lane holds until assets pool) · any second contact
type (snow/mud/moss — the class is named, one instance is tested) · engine integration
beyond the file-contract note Phase 0 Q2 produces · reviving the hull-foot stroke arm
(queued in polish; W2 measures whether the layer reads over the current 24.41% base
before anyone strokes it) · touching the accepted galleon base asset in any way.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Step 0 anchors byte-identity; workflows saved before submission; the founding exemplar is seed-pinned validation data |
| ANDON_AUTHORITY | 2 | Base-invariance halts in-tool with no skip flag; palette and coverage report-and-halt for rulings rather than invent bounds |
| NAMED_COMPENSATORS | 2 | The layer is additive by construction — undo is delete the layer state; base asset never opened for writing; cloud spend bounded by dry_run + estimate per submission |
| DECOMPOSE_BY_SECRETS | 3 | The experiment IS the boundary: contact geometry in the profile (`waterline_z`), mechanism in tools, water identity in the prompt and layer fixture — a change required outside those is a primary finding, E04's test inherited |
| UNCERTAINTY_GATED_HUMANS | 3 | The Director places the waterline (Step 0.1) and rules the toggle (W3) — both one-sentence gates on his eye, at his zoom |
| EXTERNAL_VERIFIER | 1 | `skip:` — deterministic geometry and byte checks; the verifier of record is the Director on the toggle pair, the one question no metric answers |

## The advisor's record, for this spec

Priors carry status: the founding exemplar's band is *measured*; the mask-covers-band
prediction is *inferred from geometry*; the engine-contract question is *unread* until
Phase 0 returns. The advisor has closed thirty-eight ledger entries; the standing
corrections that bind this spec: name every operand's kind, enumerate before asserting
coverage, the consumer-grep is part of any fold, and a check's failure mode is examined
before the check is adopted. When a number disagrees with this spec, trust the number,
report it, and halt for the ruling.
