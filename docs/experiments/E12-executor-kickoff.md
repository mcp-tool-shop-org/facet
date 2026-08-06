# E12 — executor kickoff: the beast at Gate 0

Paste this into a fresh executor session. Written by the advisor, 2026-08-05 evening, at
the close of the two-close day (the galleon accepted at Gate 1, E10's waterline shipped as
data). This dispatch is **Gate 0 only**: three dragon clays become three measured meshes
and three full-size sheets, and the Director designates. The identity fixture, the beast
profile and the spec proper all follow designation — none of them is this session's work.

---

## You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                <- how to work here. Read first, follow exactly.
README.md                                <- measured state of every tool
docs/experiments/E04-gate0-report.md     <- THE PRECEDENT RUN. Its environment findings,
                                            recipe, instrument discipline and sheet form
                                            are this dispatch's template.
E:\AI\training\facet_next\E04_gate0\recon.log   <- the exact recorded invocations
```

**Your rules** (CLAUDE.md, §"Rules for an executor session"): never judge whether output
is good · state a prediction before you look, and say whether it was blind · **stop at
every gate, never improvise past one** · do not write to the memory store · **a negative
result is a full success.**

## Where this stands

Two accepted assets exist (W3 at 68.8% reference; the galleon at 36.89% = 86.4% of its
pre-registered ceiling, zero credits) and E10 closed the same day. **The beast arc is the
new primary**: the first subject with large thin SHEETS (wing membranes), a live
head/allocation question, and filament classes (horns, spikes, tail ridge) on a body that
is neither a humanoid nor a ship.

Three clays are staged at
`E:\AI\training\facet_next\dragon_clay\dragon_clay_p1_{00001,00002,00003}_.png`.
The advisor viewed all three at full size on 2026-08-05:

- **00001** — quadruped forward lean, near-profile head framed by raised wings; the
  largest head relative to frame of the three.
- **00002** — most upright stance, broadest wingspread, biggest paired horns; the
  smallest head relative to frame.
- **00003** — mid-stride walking pose, asymmetric swept wings.

All three: open jaws with teeth and tongue (a real cavity the silhouette sees in
profile), membrane wings with vein ridges, scale relief throughout, horn/spike/claw
filaments, studio-grey gradient backdrop with a ground shadow. All three read **wider
than tall** — expect landscape frames. (Their mtimes read `8/6 00:11` — a UTC stamp from
the staging extraction, ~20:11 local; they are the files this dispatch describes.)

**This dispatch ranks nothing and neither do you.** Which dragon is *the* dragon is an
outcome call and it is the Director's. **Rejecting all three is a legitimate outcome.**

## Environment

- **The watchdog was restarted and verified alive by the advisor at 2026-08-05 20:26**
  after its third hard death (a NEW mechanism: a file lock on its own heartbeat —
  `_watchdog_DEAD` 19:36:15). **Verify it again before the GPU leg and report either
  way** — a status is a measurement, not a fact that survives the afternoon. Restart is
  standing authorization: `pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1`.
  **The ceiling is never raised.**
- **TRELLIS reconstruction runs LOCAL** — the standing exception to cloud-only
  generation; nothing in this dispatch generates. Runner:
  `E:\AI\sprite-foundry\3d-prerender\mesh_character.py`, recipe per the precedent report
  §2 and `recon.log`: `--ptype 1024_cascade`, `HF_HOME=E:\AI-Models\hf-cache`, the
  `PYTHONPATH=E:\AI-Models\TRELLIS.2-repo` repair recorded in the runner. `run()`'s own
  signature default `seed=42` is the seed (the tool exposes no flag) — record it from the
  signature, and **record the backend that LOADED, not the one requested** (E04 measured
  `flash_attn` loading under `ATTN_BACKEND=sdpa`). Precedent cost: 116–141 s and
  4.4–5.6 GB peak VRAM per mesh.
- **A concurrent lane may be live**: the pos.npy off-surface measurement (E10 Ruling 4,
  session handoff 5) — its predictions file
  `docs/experiments/E10-offsurface-consumers-predictions.md` is on disk uncommitted. Do
  not touch that file or anything in its lane.
- Blender through **PowerShell** · `--views=-30,0,30` argparse form · scripts create
  their own output directories · **prints are ASCII-only**.
- Output tree: `E:\AI\training\facet_next\E12_gate0\`.

## Predictions before numbers

Before `mesh_stats` returns anything, pre-state in the report (and say the status was
blind): expected **shell counts** against the measured ranges (character reconstructions
40–191; the ship 237–512, driven by free-floating rigging — a dragon's thin structure is
mostly *attached*, which is the prior to bet on or against) · expected **largest-shell
fraction** · the **membranes' predicted reconstruction form** (sheets / thickened slabs /
holed). A wrong prediction is a full success; it is the calibration the beast profile
inherits.

## The task

1. **Reconstruct all three** → `dragon_00001_raw.glb`, `dragon_00002_raw.glb`,
   `dragon_00003_raw.glb`. Log per-mesh `cmd` / env / wall / peak VRAM / exit in the
   `recon.log` form. A non-zero exit is a report, not a retry with changed parameters.

2. **`mesh_stats.py` on each, with NO `--profile`, on purpose.** No `beast.json` exists;
   the loader's no-profile path is the byte-identity path, and every value measured this
   session is folded into `beast.json` by the advisor after designation. Quote: faces ·
   verts · shells welded and unwelded · largest-shell fraction · watertight · extents
   **with their axes named in the Blender convention** · widest-horizontal / height.
   **Leave the face-rect columns unquoted** (density, curvature, `curv_radius`): the rect
   is W3's, authored against a humanoid at the character's framing, and a raw
   reconstruction's front is unestablished — a dragon *has* a face, but that rect has not
   found it. If the tool prints its front-view-rect warning, quote the warning. The head
   evidence comes from step 3 instead.

3. **Head-region evidence, per mesh — the LIVE allocation question.** E01 measured
   3.1–4.5× polygons mattering on character faces; the ship ruled allocation NONE because
   nothing supported a privileged region; **neither answer is inherited** — the decision
   is made in `beast.json` after designation, from what you measure here. Per mesh:

   - Locate the head **by eye from the clay renders** and record the method and an
     axis-aligned crop box — coordinates plus **the frame they are in** (the same
     Blender-convention frame `mesh_stats` names its extents in; every world quantity
     names its frame). **Never locate a head by height** — horns, raised wing tips and
     tail spines rise above the crown; that is the raised-weapon rule wearing wings.
   - Report: faces inside the box / total (the share) · median face area inside vs
     outside (the density contrast) · and a **full-size head crop render per candidate**
     as its own file, `GATE0_head_0000N.png`.
   - **No verdict attached.** The numbers inform the designation and the profile
     decision that follows it; they do not argue for one here.

4. **Sheets — one per candidate, full size, never a contact sheet.**
   `gate0_sheet.py --concept <clay> --renders <dir> --stats <stats.json>` with eight
   `--clay` views (texture hides geometry; there is no texture here anyway). **The
   render frame is measured per mesh from its own bbox** — the precedent driver's
   discipline; a character default would crop a wingspread the way it would have cut the
   bowsprit. Expect landscape on all three. Round the width to **÷16** (the
   generator-legal law: derive the frame from the mesh, then round to the nearest legal
   width — the ship's Gate 0 frame became its twin frame, so choose as if this one will
   be kept). Record each frame and its derivation. Out:
   `GATE0_candidate_0000N.png`.

5. **HALT — and the report goes to the ADVISOR's eye, not the Director's.** Nothing
   reaches the Director's gate that the advisor has not looked at first (ledger
   forty-three; the looking rule is seat-independent). Stage: three sheets, three head
   crops, three stats JSONs, `recon.log`, and the report at
   `docs/experiments/E12-gate0-report.md`. The report ranks nothing, recommends nothing,
   and offers its observations as data with no verdict attached — the precedent report's
   own form. The advisor looks, then presents. **The Director designates, or rejects all
   three; either is the gate working.**

## What to look at while you are there — priors, labeled (the S3 discipline)

These tell you where to LOOK in the report's observations, not what to tune.

- **Wing membranes** *(measured prior, E07, at sash scale)*: large thin sheets — E07
  measured opposing faces of a sheet thinner than its own tessellation as the closest
  back-facing sources. At Gate 0: report whether each mesh's membranes come back as
  sheets, their apparent thickness on the renders, any holes or fusions.
- **Horns, spikes, tail ridge** *(inferred)*: filament-adjacent thin structure; the
  ship's rigging lessons are the prior. Report survival, truncation or detachment.
- **Scales** *(unread guess, labeled as one)*: report whether relief reconstructs as
  geometry or stays surface detail. Nothing else to do with it at Gate 0.
- **Open jaws** *(all three clays)*: report whether the mouth cavity reconstructs open,
  with teeth, or fuses shut.

## What does NOT run, each with the reason

- **`gate_mesh.py`** — subject instruments are profile decisions; `beast.json` does not
  exist yet, and its absence-of-block will be a recorded decision there after
  designation (ship precedent: `mesh_gate: none`).
- **No second reconstruction from a head crop.** E01's bust-crop move is the allocation
  lever; whether the beast gets it is the profile decision this Gate 0 gathers evidence
  FOR. Spending it now would decide a live question by improvisation, on candidates that
  may be rejected.
- **No decimation, no UV, no atlas, no twins, no texture.** Gate 0 is the route's first
  stage and this dispatch forbids scaffolding past it.
- **No `thin_extent` derivation** — post-designation, on the designated mesh only, with
  the published cost curve (the ship's 0.01 is filament-derived and does not transfer).
- **No threshold armed from character or ship values** — the palette bands, the IoU
  halt, the bbox tolerance are other subjects' data; derive per subject later or
  suspend.
- **No profile writes, no `beast.json` stub, no identity fixture** — the advisor authors
  both from the designated mesh and clay.
- No memory-store writes · do not end a session the Director has not ended.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | `recon.log` per mesh (cmd, env, wall, peak VRAM, exit); seed recorded from the pipeline's own signature; backend recorded as what loaded; stats JSONs beside the sheets |
| ANDON_AUTHORITY | 2 | Watchdog verified before GPU work; non-zero exit halts rather than retunes; the designation halt is the gate; `mesh_stats`' own rect warning is quoted, not suppressed |
| NAMED_COMPENSATORS | 2 | New files only, all under `E12_gate0/` and one new report in `docs/`; nothing pre-existing opened for writing; no publish, no spend, nothing irreversible in scope |
| DECOMPOSE_BY_SECRETS | 3 | Frames derived per mesh, never inherited; character-only columns excluded rather than quoted; subject evidence gathered for a profile that does not exist yet instead of leaking into code defaults |
| UNCERTAINTY_GATED_HUMANS | 3 | The halt IS the designation gate: full-size sheets, head crops at zoom, the advisor's eye before the Director's, no ranking anywhere |
| EXTERNAL_VERIFIER | 2 | `mesh_stats` measures any mesh identically — the instrument that checked the E04 executor's seat checks this one. Gate 0's verifier is the Director's eye on artifacts. `skip:` on a second model — deterministic geometry, per the Gate 0 precedent |

## Calibration

The precedent executor's discipline is the standard: implement the dispatch verbatim
rather than pre-softening it, halt with the artifacts already staged, surface environment
findings (the watchdog's 153 no-op ABORTs came from exactly such a report) rather than
passing over them, and check this dispatch's own inherited numbers — the clay
descriptions, the VRAM precedent, the shell ranges — against source in the same breath
you use them. A negative result, including three meshes not worth designating, is a full
success and is reported as one.

---

## Session handoff 2 (2026-08-05) — the DESIGNATED MESH's measurement pass, 4a–4d analogue. Ends at the styled-pair halt.

Gate 0 is CLOSED by designation: **00003 is the dragon** (E12 Ruling 1 — "3 is the
winner, but they all look great"). The fixture and profile are authored (Ruling 3). A
fresh executor session starts here:

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 1-3. Ruling 2 is the allocation decision.
canon/DRAGON-IDENTITY.md                   <- the eleven elements and the stressor table
profiles/beast.json                        <- every decided value; _still_suspended is YOUR list
docs/experiments/E12-gate0-report.md       <- the designated mesh's measured record
docs/experiments/E04-task4ab-report.md     <- the method precedent for 4a/4b
docs/experiments/E04-coverage-pass.md      <- the coverage forms and decision buckets
```

**The subject:** `E12_gate0/dragon_00003_raw.glb` — its Gate 0 numbers travel with it
(9 shells, satellites = fangs, the 7,138-edge membrane pinch field, the throat crevice,
frame 1792×1024). The crevice and pinch field are **designated-in** (Ruling 1): known
subject facts, not defects to fix.

**Task 1 — the sweep.** Run the registry sweep and coverage pass against
`profiles/beast.json`. Report the UNDECIDED set — expected members: `texpass_iter`'s
absent `thin-extent` (deliberate — it lands in Task 2), the `texpass_brush` block behind
its `_NOT_CLEARED` marker (lifecycle, stays), and whatever the sweep finds that the
advisor's draft missed, which is the sweep doing its job. *(⚠ Corrected by the run,
2026-08-05 — E12 Ruling 5: `_NOT_CLEARED` is one of Ruling 22's recognized decision
forms, so `texpass_brush`'s seven keys count DECIDED and never appear — the marker
working, the dispatch's expectation wrong. The run's actual second member was
`brush_cloud_step --lane`, unreachable from any profile.)* **0 UNDECIDED gates ARMS, not
this dispatch** — your exit condition is the report, with every member dispositioned
(lands-in-this-dispatch / lifecycle-blocked / finding-for-the-ruling).

**Task 2 — 4a analogue: measure the suspended values from the designated mesh.**
Predictions blind before each measurement, hashed where anything is checkable.

1. **Prep bake** at the profile's operating points (head-scale 1.0, res 4096 — the
   Ruling 2 configuration). PRE-STATED READING (beast.json carries it): the bake's
   ANDONs were written for characters; if one fires on this mesh it is an expressibility
   limit — report and HALT, do not tune.
2. **The reach ceiling, pre-registered before any projection** — `e08_ceiling` at the
   profile's ruled floors on the eight eye-level cameras. The ship's 42.72% was
   pre-registered exactly here and every downstream number was read against it. Report
   reach/valid with both operands. **Also classify the bake's `pos.npy` off-surface rate**
   (the E10 Ruling 4 instrument, >1 px threshold, report-only): the property is now a
   known bake artifact class, and this subject's record carries it from birth instead of
   discovering it after acceptance.
3. **`thin_extent`, measured fresh** — extent density on this mesh, the full cost curve
   (fraction of visible area withheld per view per candidate value), and **separately:
   what fraction of the membrane fields each candidate withholds**. A filament-tuned
   value could withhold a third of this subject; the membranes are slabs, not rigging.
   Report the pinch-field's facing/visibility behaviour (the 7,138-edge region against a
   clean membrane area of the same mesh) as diagnostic evidence for the spec's arms — no
   gate arms on it.
4. **The elevated-camera question, measured** — up-facing surface (normal_z > 0.5, area
   not face count) first-hit coverage per candidate set: the eye-level eight alone;
   +0/180 @ 40; +0/180 @ 55; +90/270 @ 40; single top-down as the cheap reference.
   Greedy by marginal gain, the ship's own method. The wing tops and back are this
   subject's decks. If the adopted set leaves the code-default cull superset, flag the
   union re-issue in the report (beast.json's `production` note).

**Task 3 — 4b analogue: the backdrop derivation.** Estimate sRGB per fixture element
(D1–D11 → `canon/dragon-materials-estimated.json`, the galleon pattern — estimates from
the words, superseded the moment the pair exists). Derive the backdrop: maximise the
minimum distance from every declared material, weighted toward **D3 storm-grey
membranes** (the largest near-neutral surface — this subject's danger class) and the
dark small elements; saturated optima disqualified. Show the full table with the minimum
highlighted. **Pre-register the prediction before deriving.** The chosen word goes into
the twin-prompts file you build (fixture prompt + backdrop word, keyed on `dragonclay`
stems) — never silently into the profile's protective prompt entry.

**Task 4 — 4c analogue: the styled target pair, on cloud.** Two views from the fixture
prompt with the derived backdrop word: **view 1 (head-side three-quarter — head, chest,
wing leading edges) and view 5 (tail-side three-quarter — tail spines, wing backs,
hindquarters)**, the identity-dense ends of this subject. Standing cloud discipline in
full: workflow JSON saved before submission · link topology checked in code (a `dry_run`
PASS does not prove link sanity) · `dry_run` · `estimate_credits` · the LoRA by its live
card name (`mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500`; the
browser Model Library is ground truth) · frames generator-legal (1792 is ÷16) · sidecar
at birth: **"specification source and visual target, never a projection reference."**
One generation per view; the palette-gate re-roll precedent applies (one re-roll, new
seed, rejected artifact stays in the record; a second failure is the result).

**Task 5 — 4d analogue: the palette bands.** From the fixture's named materials,
cross-checked against the styled pair — **never against future twins** (non-circularity).
Report the forbidden-span arithmetic, whether the ivory family's bands merge (D4/D5/D6/
D7/D10 — this scheme's gold-family question), and each band's chroma floor. **D8 eyes
and D9 tongue are pre-registered as below any area floor — no numeric gate on either**
(the G7 lesson). Suspend rather than invent any threshold the data cannot support;
report numerator and denominator and stop.

**Then HALT.** The pair and every derivation go to the ADVISOR's eye first, then the
Director beside the clay — his fixture overrule window made visual. The E12 spec proper
follows from the advisor with 4a–4d's numbers in hand.

**Environment, standing:** watchdog verified before any local GPU leg, report either
way (restart is standing authorization; the ceiling is never raised) · generation
cloud-only · Blender through PowerShell · ASCII prints · scripts create their own output
directories · predictions blind before artifacts exist · nothing reaches any eye unviewed
by the seat that sends it.

**Do not:** generate anything beyond the two pair views · project anything · run any
stroke · arm any threshold the data cannot support (suspend + report) · touch the
E10/E11 lane, the 00001/00002 artifacts, or either accepted asset · scaffold past Task 5
· write to the memory store · end a session the Director has not ended.

---

## Session handoff 3 (2026-08-05) — the STYLED TARGET PAIR, then the bands. Fresh session; Tasks 1–3 are banked.

Handoff 2's Tasks 1–3 are complete and ruled: the sweep (`15232fe`, ship at 81/81),
the measurement pass (`9b8f109`, `830c0e4` — ceiling 50.46% banked, elevated ruled
NONE, thin_extent curve banked with its value deferred to the stroke-lane ruling), and
the backdrop derivation (`a3cc6f1`, hue ruled by Ruling 8a). The prior session halted
at the arc's first credit-spending step with its capacity honestly flagged — start
fresh here:

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 1-8. 7d ungates the pair; 8a rules the word.
canon/DRAGON-IDENTITY.md                   <- the eleven elements; S-backdrop RESOLVED
profiles/beast.json                        <- every value; backdrop + prompt now carry the ruled word
canon/dragon-materials-estimated.json      <- the estimates the pair supersedes
docs/experiments/E04-task4c-pair-sidecar.md    <- the sidecar precedent
docs/experiments/E04-task4d-report.md          <- the bands precedent
```

**Task 4 — the styled target pair, on cloud.** Handoff 2's Task 4 text governs; these
are the deltas and the trap:

0. **Build the twin-prompts file first** (`dragonclay` stems, the fixture prompt with
   the ruled `plain lavender-grey background` — byte-equal to `beast.json`'s
   protective prompt entry).
1. **⚠ THE PAIR'S CONTROLS COME FROM PROFILE-RENDERED CLAY VIEWS, NEVER FROM THE
   GATE 0 RENDERS.** Ruling 4a armed this trap: Gate 0 rendered at code-default
   fit-axis HEIGHT and is not a byte-anchor for anything the route does now. Render
   views 1 and 5 under `--profile profiles/beast.json` (width-fit, 1792×1024,
   margin 1.204), silhouettes likewise, controls built from those. Watchdog verified
   before the Blender legs, report either way.
2. Cloud under the full standing discipline (workflow JSON saved before submission ·
   link topology checked in code · `dry_run` · `estimate_credits` · the LoRA by its
   live card name from the browser Model Library). One generation per view; one
   bounded re-roll, new seed, rejected artifact stays in the record; a second failure
   is the result.
3. **Sidecar at birth**: "specification source and visual target, never a projection
   reference" + the ruled backdrop word + the estimated triple it supersedes + the
   Ruling 8a reference.

**Task 5 — the palette bands**, per handoff 2's Task 5 text unchanged (fixture
materials × the pair, non-circular; the ivory-family merge question; chroma floors;
no numeric gate on D8/D9; suspend rather than invent).

**Then HALT.** The pair and the bands go to the ADVISOR's eye first, then the Director
beside the clay — his overrule window on the whole authored identity, made visual.

**Do not:** reuse any Gate 0 render as a control or anchor · exceed the bounded
re-roll · decide the thin_extent value (stroke-lane ruling's property) · touch the
E10/E11 lane, the 00001/00002 artifacts, or either accepted asset · write to the
memory store · end a session the Director has not ended.

---

## Session handoff 4 (2026-08-06) — the RE-PAIR under the ruled register. The control must carry the relief.

The first pair was REJECTED at the Director's eye (E12 Ruling 10: a generic stock
dragon wearing the right silhouette). The style register is now subject data — the
beast runs **ultra-realistic, NO LoRA** (fixture STYLE-SUPPLIED rewritten, `lora-w
0.0`) — and the measured structural deficit owns your first task: at the profile's
canny 0.4/0.8 the control carries 5.20%/2.13% of the figure interior against
15.80%/11.15% at 0.05/0.15. A fresh session starts here:

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 9-10. 10b is the register; 10c is your task.
canon/DRAGON-IDENTITY.md                   <- STYLE-SUPPLIED rewritten; the eleven elements unchanged
profiles/beast.json                        <- lora-w 0.0; prompt tail = the register; canny marked falsified
docs/style-registers.md                    <- why the register changed
docs/experiments/E12-task45-report.md      <- the rejected pair's record (5a91646) - baseline for NOTHING
```

**Task 1 — derive the beast's canny pair, measured.** Blind predictions first. Sweep
the threshold pair on this subject's own profile-rendered clay views (both pair
views at minimum), reporting per candidate: interior edge fraction, and **the
works-perfectly test stated before reading anything** — what a lower pair admits
that is NOT relief (Workbench shading noise, gradient banding on the backdrop,
AA speckle; characterize the admitted set at 5× crops, the A2-check pattern). The
0.05/0.15 point from the rejection measurement is a candidate, not an answer.
Propose the pair with the curve; the advisor rules it into the profile.

**Task 2 — rebuild the controls and re-pair.** Controls from the ruled pair +
the standing silhouette-gradient union; same frames, same discipline as handoff 3
(saved workflows, in-code topology check — your own guard, now self-tested —
dry_run, estimate_credits, sidecar at birth). Prompt: the corrected protective
entry with the register tail; per-view stems per the verified 9d split. **No LoRA
node in the graph** — lora-w 0.0 is not a weight of zero on a loaded card, it is
no card; build the graph without the loader. One generation per view, one bounded
re-roll. **The pair goes to the advisor's eye, then the Director's** — his
question is the register: does it read ultra-realistic and scary.

**Task 3 — only if the pair is accepted:** re-derive the bands against it (the
suspended Task-5 bands died with the rejected pair; non-circularity holds), and
re-confirm D8 on the accepted artifact (Ruling 10g holds it passed-as-mechanism).

**Do not:** compare anything to the rejected pair as a baseline (it is evidence,
not a target) · arm any structure metric as a gate (10d: the structural channel at
a style gate is the eye) · touch thin_extent, the E10/E11 lanes, or either accepted
asset · exceed the bounded re-roll · end a session the Director has not ended.

---

## Session handoff 5 (2026-08-06) — the tongue's geometry, the view-5 re-roll, and the head-crop companion. Comprehensive.

*(An earlier, compressed form of this dispatch was rewritten in full on the
Director's instruction — "make it comprehensive so that there's no room for
misunderstanding." He is right: an executor session starts with no shared context,
and a dispatch that presumes any is a dispatch that invites improvisation. The
compressed form is superseded by this section.)*

Serves either the holding handoff-4 session (git pull first) or a fresh one — it
assumes nothing not written here or in the reading list.

### Where this stands

The re-pair ran under the ruled register (ultra-realistic, NO LoRA, canny
0.05/0.10) at 0 credits, and the Director's verdict is **register CONFIRMED, pair
NOT YET ACCEPTED**: *"It looks a lot better, but the tongue is missing and the face
could be more defined."* Ruling 11 turned that into three work items, and
acceptance — and everything behind it (Task 3's bands re-derivation and the D8
closure) — waits on all three plus the Director's eye. His question about the
humanoid definition technique reopened the allocation question by Ruling 2's own
re-open clause; the ladder is ruled (resolution first, geometry second, the second
step his word only) and **item 3 below is the resolution rung**.

### You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 9, 10, 11. Ruling 11 is THIS dispatch's charter.
canon/DRAGON-IDENTITY.md                   <- the eleven elements; STYLE-SUPPLIED as rewritten by 10b
profiles/beast.json                        <- canny 0.05/0.10 (11a), lora-w 0.0, the protective prompt entry
docs/experiments/E12-twin-prompts.json     <- v3, the ruled per-view stems and the deletion construction
E:\AI\training\facet_next\E12_gate0\head_00003.json    <- the measured head box + its frame convention
E:\AI\training\facet_next\E12_gate0\boxed_00003\       <- the box drawn on all 8 views (checkability)
docs/experiments/E12-gate0-report.md       <- sections 4-6: satellites are INTERIOR geometry; the mouth record
```

Your rules (CLAUDE.md §executor): never judge whether output is good · predictions
blind before looking, blind status disclosed · stop at every gate · no memory-store
writes · a negative result is a full success.

### Environment, standing

- **Watchdog verified before any local GPU/Blender leg, report either way** — a
  status is a measurement, not a fact that survives the afternoon. Restart is
  standing authorization (`pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1`);
  the ceiling is never raised.
- **Cloud discipline, in full:** the saved workflow JSON IS the submitted graph ·
  in-code link-topology guard before submission (yours, self-tested in handoff 4 —
  self-links, dangling targets, clean ANDON prints with no file written) · the
  no-LoRA pre-flight scans every node for the loader class family AND the card
  string (no-LoRA is the absence of a node, never a loaded card at weight zero) ·
  `dry_run` then `estimate_credits` before any execution · uploads named by
  content hash (a matching name is a free byte-identity confirmation) · sidecar at
  birth for every generated artifact · **prints ASCII-only** · Blender through
  PowerShell.
- Output tree: continue the handoff-4 tree; new artifacts in clearly named
  subdirectories (`tongue_check/`, `view5_reroll/`, `head_companion/`).
- A concurrent lane may exist in this working copy — **read `git log` before any
  push**, and touch nothing under the E10/E11 artifacts or either accepted asset.

### Blind predictions, before anything runs

Commit a predictions file BEFORE the first measurement, hashed, blind status
stated, covering at minimum: T1 — tongue present / absent, and if present,
reachable or interior; T2 — do the two named material misses resolve on a seed
change alone; T3 — does the face read defined at bust resolution, and per-element
landing expectations for D8 / D9 / D10 / D11 at that scale. Wrong predictions are
full successes; they are calibration for the allocation ruling that follows.

### Task 1 — the tongue: a geometry question, answered by geometry

**The question, two parts:** does `dragon_00003_raw.glb` carry tongue geometry
inside the mouth cavity — and if it does, is that geometry REACHABLE by any
exterior camera, or is it interior-class like the fangs? (Ruling 10f measured 7 of
8 satellite shells unreachable from all 26 directions; Gate 0 §6 confirmed a
visible tongue on candidates 00001 and 00002 and **did not** on 00003.)

**Mechanics are yours; the requirements are these:** the answer comes from the
mesh, not from any render of a styled artifact — a crop-render into the open mouth
(pick the yaw/elevation that actually sees the cavity; the jaw opens forward and
down) and/or a raycast census of the cavity volume, whichever is decisive. Show
the evidence (a labeled crop or the census numbers), and state the answer in one
line.

**Pre-registered branches — all three are reports, none is yours to act on:**
- **Present and visible** → D9 stands; its landing is judged at the companion's
  scale (Task 3), not before.
- **Present but interior** → D9's declared surface is unreachable by construction,
  the same class as the fangs; the fixture consequence (record D9 as
  unrealizable-at-projection, or merge the cavity's elements) is the advisor's to
  draft and the Director's window to rule.
- **Absent** → same consequence path, with "no geometry" as the ground instead of
  "unreachable geometry."

**You edit no fixture and no profile in any branch.** Report the fact.

### Task 2 — the view-5 re-roll: one seed, nothing else

The pale-tan haunch/shoulder/hindquarter (D1's declared moss-green surface) and
the bone-ivory membranes (D3's declared storm-grey) are spec violations on named
elements — the palette-gate re-roll precedent applies (one re-roll, new seed, the
rejected artifact stays in the record; a second failure is the result).

- **The seed is the ONLY delta.** Same saved workflow JSON, same control, same
  prompt stem, same everything; record both seeds in the sidecar. This SPENDS
  view 5's single re-roll allowance; view 1's remains unspent.
- Full pre-flight discipline applies (topology guard, no-LoRA scan, dry_run,
  estimate_credits) even though the graph is unchanged — the guard runs because it
  is cheap, not because change is expected.
- **Deliverable:** a same-view sheet, old | new, full size, plus the two flagged
  regions at 3× (haunch, membrane field). No score, no verdict — the E07 class is
  judged by eye and the sheet serves the eye.
- **Pre-registered branches:** misses resolve → view-5-v2 is the pair's candidate
  rear view, acceptance judging proceeds on it; misses repeat → **that is the
  result** — no third roll exists, and the finding (a register/element interaction
  the seed does not reach) goes to the advisor as fixture/arm evidence.

### Task 3 — the head-crop companion: the resolution rung of the allocation ladder

**Purpose, stated so the artifact is read right:** the pair's face occupies ~3% of
a full-figure frame — E01's framing physics applied to *generation*. This
companion answers whether the face's softness is resolution starvation or a
geometry limit, gives the head region a spec source, and shows D8/D9/D10/D11 at
judgeable scale for the first time. It is **never a projection reference** — write
that into its sidecar verbatim: *"head-region spec source and definition gate;
never a projection reference"* + the Ruling 11b reference.

**Frame:** derive from `head_00003.json`'s measured world box, padded **1.12**
(Gate 0's own padding), projected under the profile's framing convention, then
rounded **generator-legal on BOTH axes** (the VAE decodes ÷8; prefer ÷16 — the
Gate 0 law, both dimensions this time because neither is the standing 1024).
Record the derivation next to the frame as Gate 0 did.

**Inputs:** a clay render of the head at that frame (the `e12_head_render.py`
lineage is the precedent — same box, same convention), its figure mask (the crop
of the full-frame exact silhouette, or a direct raycast at the crop frame —
whichever you use, say so; the full-frame silhouette is already anchored, and a
crop of anchored geometry needs no new gate — **invent no gate mid-dispatch**),
and the control built exactly as the route builds it: ruled canny 0.05/0.10 on the
clay render ∪ the figure mask's morphological gradient.

**The stem:** derive from the protective prompt entry by the 9d **deletion
construction** (whole comma-terms removed, subsequence assertion) — keep the
elements VISIBLE in the crop, verified against the actual clay render (the
`e12_view_visibility.py` instrument or eye-plus-record; expected keeps: D1 hide,
D2 throat bands, D4 horns, D5 crown/cheek spikes, D8 eyes, D10 fangs/tooth rows,
D11 mouth interior, D9 if Task 1 says visible; expected drops: D3 membranes IF the
wing does not enter the crop — verify, Gate 0 noted membrane passing behind the
skull on this mesh — D6 tail spines, D7 claws). Backdrop word and register terms
stay. **The subject noun stays** (`a winged dragon,`) — identity rides the prompt —
and the named risk is pre-registered: a full-figure noun in a bust frame invites a
whole-body composition; the control is what holds composition (the measured
architecture: structure from control, attributes from prompt). Report the standard
per-view IoU diagnostic against the crop silhouette; the registration halt stays
suspended (0.0) as everywhere on this subject.

**Generation:** one, plus its own single bounded re-roll on spec-violation grounds
only. Full cloud discipline. 0-credit expectation per the arc's record, verified
by `estimate_credits` not assumed.

**Pre-registered readings — the works-perfectly test for the ladder itself:**
- **Face reads defined at bust resolution** → definition was resolution-starved at
  pair scale; the geometry is sufficient; the asset-time answer is the band
  machinery (texel allocation), armed by the advisor at texture stage. No mesh
  change on the table.
- **Face still soft at bust resolution** → the limit is the mesh's own head; the
  bust-crop re-reconstruction question goes to the Director (it replaces the
  designated mesh — a Ruling 1 re-open, his sentence, NOT a session's arm).
- Either way: D8 (the Ruling 2 checkpoint), D9 (with Task 1's geometry answer),
  D10, D11 landings reported at scale, no verdicts attached.

### Then HALT

Stage: the tongue evidence + answer, the view-5 old|new sheet + 3× crops, the
companion + its sidecar + IoU diagnostic, the predictions file scored. **All of it
to the advisor's eye first, then the Director's** (the looking rule,
seat-independent). His questions are pre-stated: does view 5 now wear its declared
materials; does the face define at resolution; what may the mouth hold. Task 3 of
handoff 4 (bands re-derivation + D8 closure) remains acceptance-gated behind that
look — run nothing past the halt.

### Do not

Run a third roll of anything · edit any fixture or profile (advisor's writes) ·
invent a gate or bound mid-dispatch (report and halt instead) · arm any structure
metric as a gate (Ruling 10d: the structural channel at a style gate is the eye) ·
compare anything to the REJECTED first pair as a baseline (it is evidence, not a
target) · touch thin_extent, the E10/E11 lanes, either accepted asset, or the
00001/00002 artifacts · write to the memory store · end a session the Director has
not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Saved workflows are the submitted graphs; seeds recorded old and new; the companion's frame derivation recorded beside the frame; predictions hashed blind before any measurement |
| ANDON_AUTHORITY | 2 | Watchdog before local legs; the topology and no-LoRA guards (both self-tested in handoff 4) run before every submission; the halt is the Director's eye with the advisor's before it; branches pre-registered so no outcome needs improvisation |
| NAMED_COMPENSATORS | 2 | Cloud spend bounded (two generations + one companion re-roll max, estimate_credits first); all writes in new subdirectories of the handoff-4 tree; nothing pre-existing opened for writing; rejected artifacts retained, never deleted |
| DECOMPOSE_BY_SECRETS | 3 | The seed is the only delta in T2; the companion derives every value from recorded artifacts (head box, ruled canny, protective entry) rather than re-deriving; fixture consequences are explicitly routed to the seats that own them |
| UNCERTAINTY_GATED_HUMANS | 3 | All three outcomes halt to eyes, not scores; the allocation ladder's heavy rung is gated on the Director's sentence; the E07 class is presented at full size and 3× because no statistic can see it |
| EXTERNAL_VERIFIER | 2 | The tongue answer is geometry against a styled claim; the re-roll sheet puts two generations against one spec; the companion is judged by the eye the numbers cannot replace. `skip:` on a second model, per the arc's precedent |

### Calibration

The float class is now twice-seen (9a, and handoff 4's bool→float64 promotion):
before trusting any replica or anchor you build, check its arithmetic against the
source's own, in the source's order. The works-perfectly test has earned its keep
twice in two sessions (the iso-luminance artifact; the flat-not-zero null) — state
what every new number returns when nothing is wrong, before reading it. And the
last two sessions' best moments were refusals: no bound proposed while looking at
a result, no third roll, no fixture edit from the executor's seat. Continue.

### Standards compliance (handoff 2)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Every measurement lands beside its derivation JSON; the pair's workflow JSONs saved pre-submission with seeds and params; predictions hashed blind where checkable |
| ANDON_AUTHORITY | 2 | Prep-bake ANDONs pre-stated as halt-not-tune; the sweep's UNDECIDED report is the gate condition for future arms; the pair halt is the Director's fixture window; re-roll bounded at one |
| NAMED_COMPENSATORS | 2 | Cloud spend bounded to two generations (+ at most one re-roll each) with estimate_credits first; all writes in new files/dirs; the one prompts-file write is new; nothing irreversible beyond spend |
| DECOMPOSE_BY_SECRETS | 3 | Every subject value derives from this mesh or this fixture; the tuning constant (edge-ref) explicitly NOT re-derived; the backdrop word flows fixture → derivation → prompts file, never through code |
| UNCERTAINTY_GATED_HUMANS | 3 | The styled-pair halt is the Director's overrule window on the whole authored identity, advisor's eye first; suspended thresholds go to him as numerator/denominator, not invented bounds |
| EXTERNAL_VERIFIER | 2 | The ceiling instrument and the off-surface classifier check the bake from independent code paths; the pair is judged by eyes, not by the generator's own metrics. `skip:` on a second model for the geometry legs, per precedent |
