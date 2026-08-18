# E58 — the A1 twin ring: the first spend, behind the gate, over an anchor

**Advisor spec, 2026-08-18. One executor seat (Sonnet), background. The Director
authorized the spend in one word after approving the A1 mesh sheet; this arc is the
repo's FIRST generation and FIRST credit spend.**

**Pre-registered spend ceiling: 11 generations — 1 anchor + 8 ring views + at most 2
spec-violation re-rolls. The ceiling is absolute for this arc: reaching it halts the
seat whatever the state of the work. `estimate_credits` is reported before every
submission batch.**

Working tree `E:\AI\training\facet_E58\`. Handoff early, current always.

---

## The question

Can A1's eight-view twin ring be generated on Comfy Cloud **behind the canon gate**,
carrying the ratified canon in every prompt, against controls derived from A1's own
approved mesh — with the venue anchored first against the one artifact in this repo
that has a complete recipe?

## What binds (the record, with locators)

- **Twins belong to a mesh. Identity belongs to the prompt** — the twins' ONE job is to
  register to A1's silhouette; every identity element is a ratified phrase or it leaves.
- **The gate is in the spend path or there is no gate** (v0.6.0/0.7.0 arc): E54 measured
  three doors with no canon binding, and `e12_pair_cloud_step` — which authors the paid
  twin graph — is one of them. **No submission happens through an unbound door.**
- **Moving a line to different hardware needs an anchor first** (CLAUDE.md): A1's
  reference embeds its complete recipe (`canon/A1-RECIPE.json`, seed 106, 50 steps,
  cfg 4.0, no active LoRA). Replaying it verbatim on the venue is the anchor. Precedent:
  the last hardware anchor came back non-byte-identical at ΔE 0.84 against a 1.07
  no-response floor and was accepted with the boundary recorded — **read the residual's
  shape, not just its size**: uniform = float kernels, concentrated = structural.
- **Build the control; Canny cannot find a silhouette that is not there.** Controls come
  from the mesh silhouette at a generator-legal frame (**÷16 preferred, ÷8 floor,
  derived from the A1 mesh** — W3's 752 passed by luck; the VAE decodes short on
  illegal widths, E04 Ruling 15).
- **A Comfy Cloud `dry_run` PASS does not prove link sanity** (E04 G7): check link
  topology in code — self-links, dangling targets — and submit saved workflow files
  **verbatim**.
- **Rejecting a spec-violating output is the specification working, not result
  selection**: material not in the spec → reject, ONE re-roll on a new seed, the
  rejected artifact stays in the record with its measurement, a second failure IS the
  result (bounded further by the arc ceiling above).
- **Off-palette gating**: chroma floor before hue; perimeter-normalised boundary
  statistics, never area; report the total AND the largest connected component
  (two-threshold law). Bands: `canon/A1-palette.json`. The bands were derived from the
  reference, the twins are different images — the gate is not a tautology.
- **The compound-occupant observation carries forward**: A1's prompts use the ratified
  compound phrases (e.g. *plum long-vest with fine gold embroidery*) in FRESH
  generations — the class the reference itself proves lands. The W3 add-to-occupied
  question remains separate and untouched.

## Premises — measured vs assumed

MEASURED (this session or the E57 record):
- Canon RATIFIED, census 16/16; mesh APPROVED at the Director's eye; A1-RECIPE complete;
  A1-palette 10 materials; renders + silhouette-bearing clay ring under
  `E:\AI\training\facet_E57\renders\`.
- `CLAUSE_CLASSES` includes `staging`; the gate accepts A1's four staging clauses.
- E54: `e12_pair_cloud_step` authors the paid twin graph and had **no canon binding**.

ASSUMED (the seat verifies before relying):
- The comfy-cloud MCP tools are reachable from the seat's own context (verify with
  ToolSearch early; if unreachable, complete every free stage and HALT at Stage E with
  the submission-ready artifacts enumerated — the advisor submits from the main seat).
- The E12 cloud-step graph is the current submission route (enumerate: it, any saved
  workflows on the account, and `restylize_views.py`'s venue assumptions; report which
  door this arc actually uses BEFORE binding it).
- W3's camera pattern (`v_ext = bbox_z × 1.204`, flat yaw-only ring) transfers to A1
  (verify against `facet_E57` render cams; derive A1's own numbers, do not inherit).

## Stages and gates — order is load-bearing

**Stage A — the venue anchor (spend: 1).**
Replay `canon/A1-RECIPE.json` VERBATIM on Comfy Cloud — same model, sampler, scheduler,
seed 106, steps, cfg, latent size, positive and negative text, no ControlNet, no LoRA.
`estimate_credits` first; link-topology check; submit. Compare the result against
`canon/A1_reference.png`: per-pixel ΔE distribution, its spatial map, and the figure
mask specifically. **Gate A:** pre-registered readings — byte-identical or
uniform-residual ΔE at the 0.84-precedent scale → anchor ACCEPTED, boundary recorded in
every later report; concentrated/structural residual (identity or material moved) →
HALT, the venue does not reproduce the recipe and nothing downstream is comparable.
Record the venue's actual model/version strings from the account catalog beside the
recipe's.

**Stage B — the door is bound (spend: 0).**
Enumerate the submission route (assumed premise above). If the door lacks a canon
binding, bind it: `canon_gate.require_canon` (the resolve path) runs INSIDE the tool
before any graph is authored or any output directory exists, fail-closed, `raise` not
`assert`, no skip flag. Tests ride the same change-set. Then **demonstrate the
refusal**: strip one ratified phrase from a copy of the prompt, run the door, expect
REFUSE with the missing phrase named; restore; run intact, expect pass-through to the
authoring step (dry, no submission). Both transcripts in the report verbatim.

**Stage C — controls from the approved mesh (spend: 0).**
Derive A1's frame from the mesh bbox (record bbox, v_ext derivation, chosen W×H, both
÷16). Render the 8-view silhouette + canny control set from
`facet_E57\mesh\A1_1024_cascade_seed42.glb` through PowerShell/Blender at that frame
(reuse `turn_render` and the recorded control-building route; enumerate before writing
anything new). **Gate C:** bbox-check every control against its silhouette (free check);
sha256 every control byte into the report — controls are contract bytes (E08 precedent).

**Stage D — the A1 profile (spend: 0).**
Author `profiles/a1.json` from the ratified canon: the twin prompt carries every
ratified occupant phrase (N1–N10, the framing clause, the style clauses, the staging
clauses — backdrop, no weapons, no held objects, nothing crossing the silhouette), each
parameter as `{value, why, from}` with `from` citing E57/E58. Negative text from the
recipe. Seeds pinned per view, recorded before submission. Update A1's `CENSUS_ROWS`
pairing from the documented placeholder to `profiles/a1.json`; census + resolve outputs
verbatim in the report; tests move in the same change-set. **The profile is complete
when `canon_gate` resolves A1 against it with zero missing ratified phrases.**

**Stage E — the ring (spend: 8).**
`estimate_credits` for the batch, reported. Submit the 8 views through the bound door,
saved-workflow-verbatim, pinned seeds, one view per job. **Gate E (per view, before any
measurement):** the output frame matches the requested frame exactly (the VAE-rounding
law — a delivered size differing from requested is a HALT for that view, not a crop).

**Stage F — measurement (spend: 0 unless re-roll).**
Per view: registration IoU against the exact silhouette + painted-fraction vs the
mesh's (the twins' one job — report, no invented threshold); off-palette per the law
above; spec-violation check (a material not in the ratified canon → the one-re-roll
law, new seed, rejected artifact kept, ceiling respected). **No quality words.**

**Stage G — the Director's sheet.**
Per view: control | twin | reference, plus the ring beside the E57 clay ring; full-size
per-view PNGs on disk. The sheet decides; the metrics are its appendix.

**Out of scope, named:** painting/projection (texpass — the next arc); canon_bind scope
filling; any W3 work; the compound-occupant restylize test; profile repair for W3's
specimen; any judgment of whether a twin is GOOD.

## Standards compliance

1. **PIN_PER_STEP — 3.** Recipe JSON verbatim for the anchor; pinned seeds per view;
   sha256'd controls; saved-workflow-verbatim submission; venue model strings recorded
   beside recipe strings.
2. **ANDON_AUTHORITY — 2.** Gates A/C/E halt; the Stage B binding is fail-closed inside
   the door (`raise`, no skip flag), demonstrated by a refusal transcript before any
   spend passes it.
3. **NAMED_COMPENSATORS — 2.** Table below. **Spent credits have no compensator** — the
   mitigation is the pre-registered ceiling (11), the estimate-before-submit gate, and
   the Director's recorded authorization; named honestly rather than papered.
4. **DECOMPOSE_BY_SECRETS — 2.** Venue anchoring, door binding, control geometry,
   prompt authoring, and measurement are separate stages communicating through on-disk
   artifacts; the seat measures, the advisor rules, the Director judges.
5. **UNCERTAINTY_GATED_HUMANS — 2.** The Director gated the spend (given, on the
   record); Gate A structural-residual and the ceiling both return to him; the sheet is
   his.
6. **EXTERNAL_VERIFIER — 2.** Deterministic instruments (canon_gate, palette gate, IoU)
   verify the generator's output; the generator never grades itself; the Director's eye
   rules the sheet.

### Compensators

| action | undo | owner |
|---|---|---|
| credits spent (≤11 generations) | **NONE — money is spent.** Ceiling + estimate gate + recorded authorization are the bound | advisor (ceiling), Director (authorization) |
| door-binding edit + tests | `git checkout`/`git revert` by pathspec | advisor |
| `profiles/a1.json`, controls, outputs | new files; delete/revert | advisor |
| CENSUS_ROWS pairing change | revert the pathspec | advisor |
| cloud artifacts on the account | recorded in the report; deletion not required | seat names ids |

## Dispatch record (living)

- 2026-08-18 — spec written; the Director's one-word spend authorization and his mesh
  approval precede it on the session record. Seat dispatched on Sonnet, background,
  this file as charter. E58's status-table row, the `paid_for_by` bound bump to E58,
  and the instrument-census re-run land at THIS arc's fold — the last corpus-touching
  steps before its suite run, per the standing order that fired twice at the E57 fold.
