# E04 — the galleon through the accepted route

**Spec written before the work.** Advisor, 2026-08-04, on Task 4's measured numbers
([E04-ruling.md](E04-ruling.md) Rulings 1–9). Executor executes; gates halt; the Director
judges at Gate 1. The derivations behind every value here live in the Task 4 reports —
this spec cites them rather than restating them.

## The question

**Does the accepted character route generalise?** Concretely: the galleon runs the route
the warrior proved — twins from its own mesh → geometry-bounded projection → fixture-
prompted strokes → finalize → Gate 1 sheet — with every subject value drawn from
`profiles/ship.json` and `canon/GALLEON-IDENTITY.md`. **A change required anywhere outside
those two files is a primary finding** (`profiles-design.md`'s test), whatever else the run
produces.

## Hypotheses, predictions first

| # | hypothesis | prediction | blind? |
|---|---|---|---|
| H1 | the occupancy mechanism explains G7 | `red gun port lids` (head-noun form) **lands** where "red-lined" missed, control byte-matched | yes |
| H2 | the route generalises | no shared-code edit needed beyond Step 0's named items | yes |
| H3 | owner seams appear on the ship (Ruling 1's prediction) | visible owner-boundary steps on large smooth hull/sail surfaces, measurable with `e04_blotch.py`'s instrument | yes |
| H4 | reference share runs structurally lower than the character's | stage-1 share lands **well under** the warrior's 68.8% of valid; the 53% deck plateau and 10-camera reach set the ceiling — compute the exact reach ceiling *before* projection and pre-register it then | partially — the plateau is known, the ceiling number is not |
| H5 | identity rides in the prompt on a faceless subject | the landing table on the twins reproduces the pair's 11/12-or-better | yes |

## Step 0 — tool work, each item anchored (no measured arm runs until all pass)

1. **Fit-axis**: `turn_render` gains `--fit-axis {height,width}` defaulting to height, and
   `silhouette_masks` derives its extent from the **same convention in the same change** —
   the two move together or landscape subjects silently misregister (Ruling 6). Anchors:
   character-path renders and masks **byte-identical** with the flag unset; the ship's
   1066×1024 frame renders with mask agreement ≤ the 0.24% the square frame measured.
2. **Cull superset**: `cull_unseen --production` grows the ship's elevated ±40 bow/stern
   pairs. The superset must cover every production camera (E06 rule). Anchor: the
   character's cull output unchanged (its cameras were already covered).
3. **Emit framing**: `texpass_iter emit` takes its frame from the profile rather than the
   752×1024 convention. Anchor: character emit byte-identical with profile loaded.
4. **Profile check**: `e04_profile_check.py` passes across all tools after the edits.

## Arm G7 — the occupancy test (one generation, then the fixture updates)

The pair's front-view workflow, **control and seed byte-matched**, one change: G7's phrase
becomes `red gun port lids`. Measure the lid clusters before/after (`e04_bands.py`
machinery). Pre-registered readings: red arrives above the pair's measured element floor →
H1 confirmed, the fixture amends G7 to the head-noun form with the measurement; no
response → H1 unconfirmed here, the cause list (size, occlusion, warm register) goes to
the record, and **the twins run with the head-noun form regardless** — it is the correct
grammar under the standing rule either way.

## Arm T — twins, projection, strokes, asset

- **Twins**: the profile's 10 cameras (eye-8 + bow/stern @40). Per-view prompts from the
  fixture (G7 head-noun form), backdrop `plain white` (Ruling 8's default — overrulable
  only by a measurement). Controls from exact silhouettes at the profile frame.
- **Gates on the twins — first-run baselines, so: measure, report, and the advisor rules
  before projection.** Palette gate runs with the ship's two bands (blue suspended,
  reported beside): per-view off-palette totals and largest CC reported with **no numeric
  pass bound** — the W3 bounds are W3 data. Registration: IoU + centroid reported per
  view; the halt arms only after this baseline exists (Ruling 2's pattern). The one
  pre-registered rejection rule that needs no baseline: **material not in the spec, one
  re-roll, new seed, rejected artifact stays in the record** (E08 A23).
- **Watch items reported per view**: the pale near-neutral cluster's key margin (Ruling
  8); sail and rigging key-out rates (S1-corrected physics — thin enrichment is the
  number to watch, G9 its element).
- **Projection**: `project_twins`, trust∧geometry default, owner + blend sidecars standing.
  Compute and pre-register the reach ceiling (H4) before the atlas is read.
- **Strokes**: stroke cameras derived from the hole map the way 4a derived view cameras —
  measured, not inherited; the character's spiral is subject data. Cloud, per-stroke
  sidecars, the in-tool gates unchanged.
- **Finalize → pack → renders → the Gate 1 sheet**: reference | asset | provenance |
  **owner** | error — five columns now; Ruling 1 made the owner channel part of honest
  presentation. Views must include both elevated cameras and a beam view. Textures under
  `--flat`, geometry under `--clay`, full size, never a contact sheet.

## Metrics

Stage-1 share of valid and of the pre-registered reach ceiling (H4's units) · the landing
table on twins (H5) · owner-seam boundary statistics on the two largest smooth surfaces
(H3, `e04_blotch.py`) · per-view palette totals + largest CC · the watch items · provenance
mix on the finished asset beside the warrior's 68.8 / 4.2 / 27.0 **with the ceiling
difference stated in the same breath** (Ruling 5: geometry is not a regression).

## Gates

Step 0 anchors (byte-identity, halt on any digit) · the spec-material rejection rule with
its one-re-roll bound · the in-tool commit gates (corner assert, trust∧geometry) ·
**suspend rather than invent** for every threshold this subject has no baseline for —
report numerator and denominator and stop for a ruling. Gate 1 is the Director's, on the
sheet, at his zoom.

## Out of scope

The seam-levelling and owner-seam fix arms (polish queue, post-Gate-1) · E03 head graft ·
E09/brand (separate line) · any palette-gate numeric bound for the ship · `thin_extent`'s
structural-thickness replacement (named limitation, its own arm) · re-opening any
withdrawn arm.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Step 0 anchors byte-identity on the character path; every generation saves its workflow JSON before submission; profile + fixture pin every subject value; stroke and twin sidecars standing |
| ANDON_AUTHORITY | 2 | Step 0 halts on any anchor digit; first-run gates deliberately report-and-halt for rulings rather than invent bounds; in-tool gates carry from E08 A32 |
| NAMED_COMPENSATORS | 2 | Cloud spend bounded by dry_run + estimate_credits per submission with the one-re-roll rule; all writes new files; rejected artifacts stay in the record; no publish/release in scope |
| DECOMPOSE_BY_SECRETS | 3 | The experiment IS the boundary test: subject data in profile + fixture, principles in code, and H2 scores the split by whether the run needed to cross it |
| UNCERTAINTY_GATED_HUMANS | 3 | Twin baseline halt before projection; Gate 1 on the Director's eye with the five-column sheet; expectations pre-registered so a structurally lower number cannot be misread as regression |
| EXTERNAL_VERIFIER | 1 | `skip:` — deterministic geometry and measurement; the verifier of record is the Director at Gate 1, shown artifacts, with the owner channel ensuring the sheet cannot hide the defect class provenance is blind to |

## The advisor's record, for this spec

Priors in this spec carry their status: H3 is *inferred from Ruling 1's mechanism*, H4's
plateau is *measured*, H1 is *inferred from two instances*. The advisor has been wrong
about this subject's physics once already (S1, inverted) and about two costings the
measurements reversed. When a number disagrees with this spec, trust the number, report
it, and halt for the ruling.
