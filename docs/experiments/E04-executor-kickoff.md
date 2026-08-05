# E04 — executor kickoff: the road to the galleon

Paste this into a fresh executor session. Written by the advisor, 2026-08-04, the evening
Gate 1 accepted the E08 asset. Three tasks in strict order: a small confirmation on the
accepted asset, the profile extraction that protects it, then the galleon's Gate 0.

---

## You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                <- how to work here. Read first, follow exactly.
docs/experiments/E08-ruling-gate0.md     <- the closed E08 record; Amendments 30–35 at minimum
docs/experiments/E08-task3-report.md     <- the accepted asset's provenance and artifacts
docs/profiles-design.md                  <- Task 2's spec, agreed with the Director
README.md                                <- measured state of every tool
```

**Your rules** (CLAUDE.md, §"Rules for an executor session"): never judge whether output is
good · state a prediction before you look, and say whether it was blind · **stop at every
gate, never improvise past one** · do not write to the memory store · **a negative result is
a full success.**

## Where this stands

- **GATE 1: ACCEPTED** (Director, 2026-08-04, on the GLB at his own zoom). The E08 line is
  closed as the accepted character texture route. Measured mix 68.8% reference / 4.2% brush /
  27.0% dilation. The post-Gate-1 quality queue (dilation flood, blade band, A3's cap) is
  **optional polish, not remediation** — do not run any of it unbidden.
- **One region named at his zoom:** a hard-edged blotch on the crown/side of the head.
  Task 1 confirms its mechanism. **The fix does not run in this dispatch** — whether and when
  is the Director's call once the mechanism is confirmed.
- **Next milestone:** E04, the galleon — three clay concepts staged at
  `E:\AI\training\facet_next\galleon_clay\` (2026-08-03). Per the Director's own directive
  the **profile extraction runs first**, so the ship never has a reason to touch a character
  default.

## Environment

- **Verify the watchdog before any local GPU step; restart only if stale**
  (`pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1`), and report either way. A
  status is a measurement, not a fact that survives the afternoon.
- Mesh reconstruction (TRELLIS) runs **locally** per E01 precedent, watchdog verified.
  Any **diffusion generation runs on Comfy Cloud** — and the LoRA gotcha is standing: the
  API surfaces never see account imports; the browser Model Library is ground truth. The
  live card is `mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500`.
- Blender through **PowerShell** · `--views=-30,0,30` argparse form · scripts create their
  own output directories · **prints are ASCII-only** (four crashes last session; the lint is
  queued, the habit starts now).

---

## Task 1 — the crown blotch: confirm the mechanism, change nothing

**The prior, pre-registered by the advisor (Amendment 35):** the documented unlevelled
stroke-seam defect — E07's forehead blotch measured as a provenance-boundary step of 9.5×
ordinary variation with two anomalous pixels in the whole disc; stage 1 levels seams, the
brush loop never did, and the crown is where grazing stage-1 paint, both elevated strokes,
and dilation meet. **Alternates, so the check is not written to its answer:** per-island
tonal offsets (chart fragmentation), dilation patches.

**The measurement** (all local, no GPU): a paired crop at the named angle — asset | provenance
— from `W3_final.glb` / `W3_prov.glb`, plus the E07 Gate 0 boundary instrument on the blotch
region: median |ΔL| **across** provenance/island boundaries against **within**-region
variation, and whether the patch edges align with those boundaries.

- **Aligned and stepped** → the known defect, confirmed. Record it in the report with the
  step ratio; the levelling arm's file gets the measurement as its targeting data. Proceed
  to Task 2.
- **Not aligned** → the prior is wrong. Report and stop; that is a ruling.

## Task 2 — extract the character profile. The classification IS the deliverable.

[profiles-design.md](../profiles-design.md) is the spec; read it in full. The Director's
words are its charter: *"create profiles so that we don't break the humanoid character
pipeline to make the ship."*

**The work:** every constant in the route-active tools declares itself —

- **goes in `profiles/character.json`** → it was a subject assumption all along, and it
  carries its `why` and its provenance (which experiment measured it);
- **stays in the code** → it is a real principle, and the classification table says why.

Seed list from the record (enumerate beyond it — grep every numeric constant in route-active
tools): framing 752×1024/fit-height/1.204 · face-rect allocation and head scale ·
`thin_extent 0.030` (sized to the greatsword) · `edge_ref 700` · `edge_dist 4.0` and the
head variants · facing floors 0.45/0.25 and `head_facing_min` · `bbox_tol` · the camera set
and spiral order · the elevated pair · **the palette file and chroma floor 12.0 and blob
bound 800** (measured on W3's materials — subject data, not physics) · **the registration
halt IoU 0.80** (derived from W3's twins and failures — a new subject derives its own or
suspends) · `texpass_finalize`'s hardcoded triangle-edge length (E07 flagged it; per-mesh) ·
the brush prompt file reference. Borderline cases go in the table with the argument, not
silently either way. `--hole-grey 0.42 ≡ background` is a **design collision, not a
profile value** — record it in the table, change nothing.

**GATES, pre-registered:**

1. **Byte-identity.** After the refactor, with the character profile loaded: the 8-camera
   projection reproduces `stage1_8cam.png` **pixel-identically**, `e08_acceptance` lands its
   anchor, and one `emit` reproduces its saved render byte-identically. The profile is a
   pure relocation — zero behaviour change on the accepted path. Any digit differs → HALT.
2. **Completeness.** Every constant in route-active tools appears in exactly one column of
   the classification table. A constant in neither is the finding, not an oversight to tidy.

Deliverables: `profiles/character.json` · `profiles/ship.json` **drafted** from the design
note's stressor table (aspect measured from the staged clay, not assumed) · the
classification table in `docs/experiments/E04-profile-extraction.md` · loader wired into the
route tools.

## Task 3 — E04 Gate 0: three clays, three meshes, the Director designates

The route's first stage, run on all three staged concepts so the Director's designation is
informed rather than blind (E01: reconstruction quality depends on the clay's own
qualities — form first):

1. **Reconstruct all three** (`galleon_clay_p1_{00004,00005,00006}.png` → TRELLIS, local,
   watchdog verified) → weld → `mesh_stats.py` on each (shell count, density; it measures
   any mesh identically). **`gate_mesh.py` does not run** — its head/shoulder logic is
   meaningless on a ship, and the ship profile records `mesh_gate: none`.
2. **Renders for the eye:** `--clay` turnarounds of each mesh beside its source concept, at
   full size — one sheet per candidate, never a contact sheet.
3. **HALT: the Director designates the galleon.** Which ship is *the* ship is an outcome
   call and it is his. Present the three sheets and stop.

**After designation (next dispatch, not this one):** the advisor authors the galleon's
identity fixture — named materials → palette bands, non-circular, cross-checked against a
different image than the twins it will gate — because on this subject **the off-palette
gate carries the weight nobody's eye can: no one knows by sight what a galleon's palette
should be.** Camera set, framing and thin-policy land in `profiles/ship.json` measured from
the designated mesh. Then E04's spec proper.

## Task 4 — the ship's measured values, its styled target, and its bands. DISPATCHED after designation (Rulings 3–4).

The Director designated **00006**. The fixture is
[GALLEON-IDENTITY.md](../../canon/GALLEON-IDENTITY.md) — read it *as corrected* (S1 was
inverted and rewritten in place; S-backdrop is new). Strict order:

**4a — measure `ship.json`'s suspended values from `galleon_00006_raw.glb`.** Framing
(width-fit, margin measured not inherited — your Gate 0 driver already did this once);
the declared **front** and `--yaw-offset` (rotate the camera, never the mesh); the camera
set — eye-level yaws plus the elevation question the design note flags: **decks need
looking into**, so derive candidate elevations from the mesh's deck visibility (what
fraction of upward-facing surface each elevation reaches — measurable by raycast, no
generation) and record the chosen set with its coverage numbers; `thin_extent` measured
from the rigging's actual widths (G9 is the element — S2's numbers are the baseline).
Every value lands in `ship.json` with its `why` and provenance, per the profile discipline.

**4b — derive the backdrop** (S-backdrop): maximise the minimum distance from every
declared material's expected colour, weighted toward the dark thin elements, avoiding
G11's declared blue. Show the derivation as a table — every declared material, its
distance to the chosen backdrop, the minimum highlighted — and the G9 enrichment numbers
(5.68–10.77% thin vs 1.35–1.58% bulk on W3) as the baseline the choice must beat when
twins exist. Pre-register the prediction before any generation.

**4c — the styled target pair, on cloud.** Two views (front three-quarter and stern
three-quarter — the stern castle and figurehead are the identity-dense ends), generated
FROM the fixture prompt (all twelve G-elements, own noun phrases, the derived backdrop
word) with the standing recipe discipline: workflow JSON saved before submission, seed
and params recorded, `dry_run` + `estimate_credits` first, the LoRA by its live card name.
**This pair is the ship's `canon/twin_*` analogue: a specification source and visual
target, never a projection reference** — write that into its sidecar at birth. One
generation per view; if an output violates the fixture (material not in the spec), the
palette-gate re-roll precedent applies: one re-roll, new seed, rejected artifact stays in
the record; a second failure is the result.

**4d — derive the palette bands** from the fixture's named materials, cross-checked
against the styled target pair (never against future twins — non-circularity, kept).
Report the forbidden-span arithmetic (the ~120° estimate made real), whether G6 and G11's
bands merge, and each band's chroma floor. **Suspend rather than invent** any threshold
the data cannot support — report numerator and denominator and stop.

**Then HALT.** The styled target pair goes to the Director beside the clay (his overrule
window on the fixture made visual), and the E04 spec proper follows from the advisor with
4a–4d's numbers in hand.

## Session handoff (2026-08-04, evening) — start at Arm G7 ⚠ SUPERSEDED by Session handoff 2 below (Arms G7 and T are complete and ruled)

Tasks 1–4 and the spec's Step 0 are **complete and ruled** (Rulings 1–12). A fresh
executor session starts here:

```
cd E:\AI\facet && git pull
CLAUDE.md                                          <- how to work here
docs/experiments/E04-the-galleon-through-the-route.md   <- THE SPEC. Your document.
docs/experiments/E04-ruling.md                     <- Rulings 8–12 at minimum
profiles/ship.json  ·  canon/GALLEON-IDENTITY.md   <- every subject value
```

State: Step 0's four anchors all pass (Ruling 12) — the tools are ready. The
Director-ratified styled pair and its workflow JSONs are in the Task 4c artifacts; the
live LoRA card is `mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500`
(the browser Model Library is ground truth for imports, never the API list). Cloud
discipline standing: workflow JSON saved before submission · `dry_run` ·
`estimate_credits` · sidecars · predictions hashed blind before artifacts exist.

**Arm G7 first** — one byte-matched generation, `red gun port lids`, lid clusters before
and after. **Then Arm T** — ten twins to the spec's twin-baseline halt: measure, report,
and the advisor rules before anything projects. Verify the watchdog before local GPU work;
generation is cloud-only; the halts that remain are the spec's own.

## Do not

Run the seam-levelling fix, or any post-Gate-1 polish arm, unbidden · touch a
character-profile value while building the ship profile (the point of the exercise) · arm
any subject-calibrated threshold on the galleon from character-derived numbers — the palette
bands, the IoU halt, the bbox tolerance are W3 data; derive per subject or suspend and
report · run `gate_mesh.py` on a ship · scaffold past Gate 0 (Tasks 1–3) or past Task 4d ·
write to the studio memory store · end a session the Director has not ended.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Task 2's gate is pixel-identity against three recorded anchors; Task 3 reconstructions record seeds/params per mesh; Task 1 reads existing artifacts only |
| ANDON_AUTHORITY | 2 | Three pre-registered halts: mechanism-not-aligned, byte-identity failure, and the Director's designation gate. In-tool guards from E08 carry over unchanged |
| NAMED_COMPENSATORS | 2 | Task 2 is a refactor with a byte-identity proof and git as undo; Task 3 writes only new files; no publish, no spend beyond local reconstruction; nothing irreversible in scope |
| DECOMPOSE_BY_SECRETS | 3 | The task IS the decomposition: subject data separates from principles, with the boundary argued line by line in the classification table |
| UNCERTAINTY_GATED_HUMANS | 3 | The designation halt gates on the Director's eye with full-size sheets; the blotch fix explicitly waits on his call; borderline classifications carry arguments, not defaults |
| EXTERNAL_VERIFIER | 1 | `skip:` — deterministic refactor and geometry; the byte-identity anchors are the check. Gate 0's verifier is the Director's eye, shown artifacts rather than arguments |

## Calibration

The advisor's ledger is at eighteen entries and the pattern to watch is unchanged: checks
whose shape assumes their answer, and predictions about operands (especially distance
transforms) instead of decisions on their measurements. The executor discipline that closed
E08 — halting at gates, refusing instruments that cannot fail, hashing predictions before
artifacts exist, checking inherited claims against source in the same breath — is the
standard. The last session's report falsified a banked amendment with one measurement and
surfaced it at the top. Do that.

---

## Session handoff 2 (2026-08-04, late) — start at the STROKE-CAMERA DERIVATION

Stage 1 is COMPLETE and RATIFIED (Ruling 23): **36.89% of valid = 86.4% of the
pre-registered 42.72% ceiling**, atlas + native owner + blend sidecars written, coverage
at 0 undecided, purity clean, eight adjudicated twins in the set and nine in the record.
A fresh executor session starts here:

```
cd E:\AI\facet && git pull
CLAUDE.md                                               <- how to work here
docs/experiments/E04-the-galleon-through-the-route.md   <- THE SPEC, Amendments 1-3
docs/experiments/E04-ruling.md                          <- Rulings 17-23 at minimum; 23 is YOUR DISPATCH
profiles/ship.json                                      <- every value now DECIDED (64/0 coverage)
docs/experiments/E04-stage1-report.md                   <- the hole map you derive from
docs/experiments/E04-coverage-pass.md                   <- the decision forms and buckets
```

**Your task is Ruling 23's stroke dispatch, in order:**

1. **Deck strokes = the measured elevated pair** (0/180 @ 40) — cite Task 4a, do not
   re-derive. Pre-registered: the deck plateaus ~53%, so ~half its holes remain after the
   pair and fall to dilation.
2. **Side strokes: derive from the hole map 4a-style** — per candidate yaw, raycast the
   side-class hole coverage, greedy by marginal gain. Report the table and your proposed
   set, including **specifically what it buys the waterline rim** (19.44% styled — E10's
   layer needs a painted base there).
3. **NO hull-bottom strokes** — ruled (Ruling 23 §3, reasoning on the record); bottom
   holes fall to dilation. The Director's window is open; yours is not.
4. **The spiral order is subject data** — derive it from where stage 1 left paint
   (`_still_suspended`'s own note).
5. **`brush_prompts` = the twin constant string per stroke** (ruled; the twin file's
   argument transfers whole). Land the fixture beside the derivation;
   `_fixtures.brush_prompts` closes.
6. **Lift `_NOT_CLEARED` per Ruling 22's lifecycle**: coverage firing on the reverted
   `texpass_brush` keys IS the procedure — decide every key in the same commit (prompt
   from the fixture; recipe keys as FIRST-RUN OPERATING POINTS at the accepted character
   route's values), coverage back to 0, purity green.
7. **HALT: the derivation report.** The advisor rules the stroke set before any stroke
   flies. Then: strokes (cloud, per-stroke sidecars, in-tool gates unchanged) → finalize
   → pack → renders → **the five-column Gate 1 sheet** (reference | asset | provenance |
   owner | error), both elevated cameras and a beam view, textures under `--flat`, full
   size, never a contact sheet.

**Environment, standing:** verify the watchdog before any local GPU step and report
either way · generation is cloud-only (workflow JSON saved before submission,
link-checked in code — a `dry_run` PASS does not prove link sanity · `dry_run` ·
`estimate_credits` · the LoRA by its live card name) · Blender through PowerShell ·
ASCII-only prints · predictions hashed blind before artifacts exist where anything is
measurable.

**Pre-registered expectations, so numbers are not misread at the sheet:** the ship's
provenance mix reads against the 42.72% ceiling, never against the character's 68.8/4.2/
27.0 raw (Ruling 5: geometry is not a regression) · owner seams are EXPECTED on hull and
sails, with a named likely site at view-7 boundaries (Ruling 20 — its tar runs darker; the
owner channel shows it) · H3 measures with `e04_blotch.py`'s instrument on the two largest
smooth surfaces · an acceptance rate quoted without its camera count is not a number.

**Do not:** invent a bound for anything suspended (report numerator and denominator and
halt) · run any polish arm unbidden · touch the character path · re-open the withdrawn
bottom question · write to the studio memory store · end a session the Director has not
ended.
