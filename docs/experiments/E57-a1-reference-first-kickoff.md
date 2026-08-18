# E57 — A1, the reference-first exemplar: canon before geometry

**Advisor spec, 2026-08-17. One executor seat (Sonnet), dispatched as a background agent.
Zero spend: no cloud call, no generation, no GPU beyond local TRELLIS + Blender renders.
Working tree `E:\AI\training\facet_E57\`.**

**Direction (the Director, 2026-08-17, paraphrased):** build a brand new humanoid exemplar
from the beginning with the techniques developed so far, canon solid all the way through.
No weapon — a held object only confuses the profile. The named difference from W3: W3
started as a clay and had no proper reference until after the clay existed, so there was
never an easy way to paint. This one is done right from the start: **reference first.**

---

## The question

Can a humanoid exemplar whose reference, identity and recipe exist BEFORE any geometry
carry ratifiable canon through mesh reconstruction and up to the edge of the first
generation — with provenance COMPLETE at every step, where W3's founding artifacts are
recorded as irreproducible?

## Lineage — what this repairs, with locators

- `canon/MANIFEST.md` records W3's canon pair provenance as **INCOMPLETE**: the exact
  prompts are *not in the repo*, the sampler settings have no record, and the reproduction
  attempt missed (IoU 0.9040 vs 0.9088). The Director ruled to freeze the artifact and stop
  deriving. A1 inverts this: the reference PNG **embeds its own complete recipe**.
- **Twins belong to a mesh. Identity belongs to the prompt** (MANIFEST role change,
  2026-08-04). A1's identity is in a versioned generating prompt from birth; its future
  twins will be regenerated against its own mesh, as the law already requires.
- **E56 Gate A fired** because exactly one subject (W3) carries a per-surface material
  declaration with on-disk assets, and its accepted and defective asset are one file. A1
  becomes the second subject with a `.surfaces.json` and its own asset tree — the
  wrong-material predicate becomes defined on a second, cleaner population.
- The **compound-occupant question** (w3.surfaces.json Q3, OPEN) asks whether one surface
  showing two materials should carry one compound occupant. Observation this arc records
  without testing: A1's generating prompt used the compound form — *"plum long-vest with
  fine gold embroidery"* — and it landed in the reference. That is a **fresh-generation**
  landing. The open W3 question is about **adding to an already-painted surface via
  restylize**; the two cases are distinct and this arc settles neither.

## The subject — measured this session (advisor, 2026-08-17)

| | |
|---|---|
| source file | `C:\Users\mikey\Downloads\Qwen-Image-2512_00021_.png` |
| sha256 | `9417cd6492df34354e5d3f3d7809bf89ddd074f5b1b18725c166a59b97b48dde` |
| frame | 1136 × 1472 RGB — both ÷16, generator-legal by construction |
| embedded | full ComfyUI graph: `prompt` + `workflow` keys present |
| model | `qwen_image_2512_fp8_e4m3fn.safetensors` (UNETLoader) |
| sampler | euler / simple, denoise 1.0, **seed 106** |
| positive prompt | full text extracted; identity clause names ten elements; staging clause forbids weapons, held objects, and anything crossing the silhouette |
| negative prompt | present (CJK text, standard Qwen negative) — extracted to the recipe file by the seat, not hand-transcribed |

**Provenance state: COMPLETE — first subject in this repo whose founding artifact carries
its own recipe.** Replay is untested and is not this arc (a replay would spend; the
artifact is in hand and frozen).

## Premises — measured vs assumed (E29 law: mark which)

MEASURED (this session, tool output on the record):
- PNG size/mode/hash/metadata as tabled above.
- `canon_gate census`: W3 24/24 ratified, binding 0/27; subject registry is
  `CENSUS_ROWS` at `tools/canon_gate.py:907-916`, four-tuples
  (subject, identity, surfaces, profile).
- Record server SERVING, four legs PASSED, corpus 415 files.
- W3 surfaces schema (schema 2) read in full; identity form read in full.

ASSUMED (named, for the seat to verify before relying on):
- A recorded TRELLIS.2 `1024_cascade` driver exists and still runs in
  `E:\AI-Models\trellis2-env` (E01 built W3 with it at seed 42; E29 ran three
  reconstructions). **Enumerate before commissioning: find the recorded driver; do not
  write a new one until the search has failed and the failure is reported.**
- A palette-band derivation instrument exists from the E14/E04/E12 family. Same law:
  enumerate first, report what exists and what it binds as constants.

## Stages and gates

**Stage 0 — provenance freeze (Gate 0).**
Create `E:\AI\training\facet_E57\`. Copy the source PNG to
`facet_E57\reference\A1_reference.png` AND `canon/A1_reference.png` (repo copy — canon
inputs are versioned per MANIFEST precedent). Machine-extract the embedded graph to
`canon/A1-RECIPE.json`: positive text, negative text, model, sampler, scheduler, seed,
denoise, size, source filename, sha256, byte count. **Gate 0 halts if:** sha256 of any
copy mismatches the source, or any recipe field cannot be read from the PNG itself.
Then **diff the advisor's `canon/A1-IDENTITY.md` NAMED phrases against the extracted
positive prompt** — every N-phrase must appear verbatim in the prompt. A mismatch is the
advisor's transcription error: report it, do not fix canon files silently.

**Stage 1 — palette bands (report, no gate).**
Enumerate the E14-family derivation instrument. Derive per-material Lab bands from
`A1_reference.png` for the ten NAMED materials. Laws in force: chroma floor before any
hue is quoted; hue centres are circular statistics; report per-material pixel counts and
the sampled regions on an overlay sheet (the Director must be able to see what was
sampled). Output: `canon/A1-palette.json` + region overlay sheet in the training tree.
The bands DESCRIBE the reference; they gate nothing this arc.

**Stage 2 — mesh (Gates 1 and 2).**
One reconstruction: TRELLIS.2 `1024_cascade`, **seed 42, recorded**, input the frozen
reference copy. Known internals (E29): resize to 1024 max edge, rembg, alpha-bbox crop.
Weld-before-decimate is the recorded route's own behaviour — verify it happened (report
vertex/face counts at each recorded stage the driver exposes). Export GLB into the
training tree.
**Gate 1 (mechanical):** halts on pipe error, empty/degenerate mesh, or rembg visibly
failing to remove the studio backdrop. **This gate does not judge quality.**
**Gate 2 (sanity):** render the 8-view ring (`turn_render`, PowerShell, clay AND flat),
then bbox-check: the figure must occupy a plausible fraction of frame and its
height/width ratio must sit near the reference figure's (report both; halt only on
absurdity — figure touching frame edges, ratio off by more than ~2×). Report mesh_stats
and mesh_topology beside the five-character base rates (largest component 98.2–98.6%);
**do not halt on a base-rate miss — report it.** No inner-wall claims: the nested-wall
leg declines on characters and that stays an open question, not a finding.
Single build, no re-runs: a second run differs ±0.27% faces in `to_glb` decimation
(E29), so no mesh comparison exists this arc and none is to be read.

**Stage 3 — the Director's sheet.**
One sheet: reference | clay renders | flat renders, at sizes his eye can use, plus
full-size per-view PNGs on disk. The sheet is the deliverable; the metrics are its
appendix.

**Out of scope, named:** any generation (twins, restylize, brush — all spend);
`profiles/character.json` repair (left broken on purpose); canon_bind scope filling for
A1 (needs a mesh AND a binding pass — later arc); replaying seed 106 to test recipe
reproducibility (spends); any W3 work, including the compound-occupant generation (the
Director's open item — untouched by this arc); eye/face restoration or any judgment of
whether the mesh is GOOD (the Director's).

## Predictions

The seat states its own predictions in the report BEFORE running Stage 2, each with its
blind status and — per the E39/E40 law — inside the interval its instrument can actually
return. Premise for them: the reference is a single centred figure on a plain backdrop
with nothing crossing the silhouette; the population laws (unit, object counted, rarest
clause) apply. The advisor records here only what is already observed, not predicted:
the ten identity elements are present in the reference to the advisor's eye at full
size; the hands carry ink marks whose painted extent exceeds the phrase
"ink-stained fingertips"; light stubble is painted and unnamed. These are queue items
for the Director, not measurements.

## Registration and tests

The seat adds `("A1", "canon/A1-IDENTITY.md", "canon/a1.surfaces.json",
"profiles/character.json")` to `CENSUS_ROWS`, runs `canon_gate census` and
`canon_gate resolve --subject A1`, and reports both outputs verbatim (ASCII). Tests ride
the commit: whatever suite surface pins the census/subject population moves in the same
fold, and T34's collector counts move with any added test. The seat prepares edits +
tests uncommitted; **the advisor commits by pathspec after review.** Report any reverse-
check warns from `resolve` — legal-clause tuning happens at the fold, pre-ratification.

## Standards compliance

1. **PIN_PER_STEP — 2.** Reference pinned by sha256 + embedded recipe; reconstruction
   seed/params recorded in the spec and report; instruments reused at pinned paths; seat
   model tier named in the dispatch.
2. **ANDON_AUTHORITY — 2.** Gates 0/1/2 halt the seat with evidence; the halt-not-tune
   law binds; any new check that gates an irreversible step must `raise`, never bare
   `assert` (E21 Ruling 2 / E22).
3. **NAMED_COMPENSATORS — 2.** Table below; no irreversible external action exists in
   this arc.
4. **DECOMPOSE_BY_SECRETS — 2.** Canon text (advisor) / measurement (seat) / acceptance
   (Director) never share a hand; stages communicate only through on-disk artifacts.
5. **UNCERTAINTY_GATED_HUMANS — 2.** Five ratification-queue items gate on the Director,
   each framed contrastively; nothing else waits on him.
6. **EXTERNAL_VERIFIER — 2.** The seat (Sonnet) machine-diffs the advisor's (Fable)
   canon transcriptions against the PNG's own bytes with the advisor's reasoning hidden;
   the Director's eye verifies the artifacts. No generator grades its own output.

### Compensators

| action | undo | owner |
|---|---|---|
| files added under `canon/`, `docs/experiments/`, `tools/canon_gate.py` edit | `git checkout -- <path>` pre-commit; `git revert <sha>` post-commit | advisor |
| new tree `E:\AI\training\facet_E57\` | delete the tree; it contains only artifacts derived from the frozen source | seat names, advisor executes |
| repo copy `canon/A1_reference.png` | `git rm`, revert | advisor |
| nothing published, nothing posted, nothing cloud | — | — |

## Ratification queue for the Director (also mirrored in a1.surfaces.json)

- **Q1 — the name.** Subject id drafted **A1**, working name *the archivist* (the
  prompt's own word). Ratify or rename; files follow the id.
- **Q2 — ink extent.** The prompt says *ink-stained fingertips*; the paint carries marks
  across both hands, palms and backs, well past fingertips. You probably expect the
  image to be canon; the identity-in-the-prompt law makes the PHRASE canon, and the
  phrase says fingertips — future generations prompted with it will likely show less ink
  than this reference. Adopt the phrase as-is, or re-word it (a re-word is a canon edit,
  untested until the next generation).
- **Q3 — garment decomposition.** Drafted as ONE garment — the prompt's *plum long-vest*
  — occupying two spatial rows (buttoned torso panel, open skirt below the sash). The
  alternative reading is two garments (outer coat + under-vest). The prompt named one;
  the draft follows the prompt.
- **Q4 — stubble.** Light stubble is painted and appears in no phrase — by the law it is
  arriving by accident and will leave the same way. Name it (the compound form *olive
  skin with light stubble* is a candidate, same untested class as Q3-compound on W3) or
  let it leave.
- **Q5 — the umber word.** The sash phrase says *umber*; the painted sash reads
  olive-gold, and Stage 1's band will record what it measures. The word is the attested
  canon; changing it to match the paint is your call, no action needed to proceed.

## Dispatch record (living)

- 2026-08-17 — spec written; canon drafts (`A1-IDENTITY.md`, `a1.surfaces.json`) written
  by the advisor in the same session; seat dispatched on Sonnet, background, with this
  file as charter. Mid-flight rulings append here.
- 2026-08-17 — **Gate 0 PASSED at the seat** (per `facet_E57\handoff.md`): three sha256
  matches; recipe fully readable, zero unreadable fields; **18/18 canon phrases verbatim**
  in the extracted positive prompt. Two recipe facts surfaced beyond the charter's
  minimum: a Lightning LoRA sits in the graph **INACTIVE** behind a boolean switch
  (238:229=false) — the reference ran the standard branch, 50 steps / cfg 4.0 / no LoRA,
  recorded so nobody conflates "LoRA in the workflow" with "LoRA painted this image";
  and the declared latent width 1140 was **delivered as 1136** = floor(1140/8)×8, the
  generator's own ÷8 rounding — the E04 Ruling 15 mechanism observed from the other side.
- 2026-08-17 — **THE CANON IS RATIFIED — the Director, as drafted.** All 19 rows and all
  five queue positions: A1 *the archivist*; the ink phrase as attested; one garment
  across two rows; stubble unnamed, leaves; the umber word stands. His standing principle
  at ratification, paraphrased: **the quality is made in the edit** — ratification is a
  baseline, not a freeze; a post-ratification canon edit is an ordinary versioned move
  whose test is the next generation. Machine note for future drafts: `canon_gate` reads
  ratification as the ABSENCE of `"ratify": true` on an occupant (`is_unratified`,
  canon_gate.py:335-337) — this draft carried no flags, so the Director's word arriving
  before the first A1 census makes the machine state truthful; **a draft that must read
  as unratified in a census needs the flag on every row until his word.**
- 2026-08-17 — **seat terminated by an API connection loss mid-Stage-1** and resumed on
  the same transcript. Cost: nothing — Stage 0 was on disk (handoff current, report
  skeleton with the Gate 0 row) before the death, which is the E38 discipline doing its
  job. Its last transmitted words carried a genuine enumeration finding, ordered into
  the report at resume so it stops living in a transcript: **`e12_region_colour.py`
  computes its hue centre as a plain linear median on degrees** — the E14 circular-hue
  law names that unsafe near the 0/360 wrap. The instrument is shipped and is NOT to be
  edited this arc; the seat's Stage 1 script (in `facet_E57\`, per charter) computes the
  circular unit-vector mean instead, and the finding is recorded for a later repair arc
  under the cited-instrument discipline.

- 2026-08-17 — **the fold, and the registration ANDON ruled.** The seat completed Stages
  0–3 (Gate 1 PASSED: 990,679 faces, no backdrop contamination; Gate 2 PASSED: ratio 1.240)
  and registration FIRED a real ANDON: `CLAUSE_CLASSES = ("style", "framing")` lacks the
  `staging` class the **ratified** canon uses on four clauses, breaking `census()` for every
  subject — blast radius 3 tests across 2 files, 38 adjacent tests unaffected (seat's
  measurement). **Ruling: widen the enum, not the canon.** The ratified artifact stays
  byte-stable; the tool serves the canon; `staging` names a real third category (the shot —
  backdrop, no weapons, no held objects, clear silhouette — is neither the paint nor the
  subject); and the repair adds capability while removing no coverage, this repo's own
  boundary for a permitted repair. Rejected in writing: re-classing the ratified file
  (edits a ratified artifact to serve a tool's limitation, and misfiles the no-weapon
  direction as style). Implemented at the advisor's hand as part of the fold: enum widened
  with the ANDON message now derived from it, a two-leg can-fail test added
  (staging accepted / unknown class still fires), all three formerly-failing tests green.
  **Non-perturbing anchor:** post-edit census rows for W3 and LONGSWORD are byte-identical
  to the session-start census. A1's row: **10 named, 16/16 occupancy, 16/16 ratified,
  prof_hit 0/10** (the documented placeholder pairing against W3's profile). Count surfaces
  moved in the same change-set: suite 1338→1339 / hermetic 1284→1285 (T34: 51/52 named
  surfaces green on first sweep; the 52nd was README.fr.md's NBSP-separated `1 338`,
  repaired at the byte), experiments 56→57 with the E57 status-table row as the authority.
  **Advisor errors owned:** (1) the spec's "reverse-check warns from resolve" premise is
  measured false — resolve has no such logic; (2) a1.surfaces.json was authored and
  ratified without checking its clause classes against `CLAUSE_CLASSES` — the ANDON that
  fired is that unchecked premise surfacing, one fold late. Two repair items flagged for
  later arcs, not taken here: `e12_region_colour.py`'s linear hue median, and
  `tools/verify/gate_mesh.py` `load_fig()`'s single-corner background sample (the retired
  corner-median shape's last shipping consumer, CLAUDE.md law corrected 3→4 firings).
- 2026-08-18 — **the fold's own two late gates, and the advisor's construction ate one.**
  The full suite behind the fold read `2 failed, 1337 passed` while its recorded exit code
  was 0 — the advisor had built the run as `pytest | tail`, and a pipe exits with its last
  element's code: the shell-chain law, fired at the advisor's own hand, caught only because
  the tally line was read. The two failures were the two designed new-arc steps run late
  rather than skipped: `conventions.json` `laws.paid_for_by` extended `E5[0-6]` → `E5[0-7]`
  (the deliberately bounded pattern; a test forbids wildcarding it), and
  `instrument_census.py --committed` re-run (8 instruments' axis-D citation counts moved
  when the E57 docs joined the corpus). Both files then green in full (112/112). Standing
  order restated for every future fold: the arc-bound bump and the census re-run are the
  LAST corpus-touching steps, BEFORE the suite — running the suite first re-discovers them
  as failures.
- 2026-08-18 — **THE SHEET IS APPROVED at the Director's eye**, the collar specifically
  ruled good. With the canon ratified and the mesh accepted, both Director gates in front
  of the A1 twin arc are open. The twin arc is the first generation and the first spend of
  this repo's credits; it is staged, not dispatched — the spend runs on his word, not by
  default.