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

---

## Session handoff 6 (2026-08-06) — the regeneration under the corrected canon. A decision bundle, not a re-roll.

Serves the holding handoff-5 session (git pull first) or a fresh one — it assumes
nothing not written here or in the reading list.

### Where this stands

Handoff 5 completed all three tasks at 0 credits (`898dea0`) and the Director's eye
came back with a verdict on the staged artifacts: *"What's up with the bones on the
outside of the dragon's legs, bottom of the tail and arms?? This has to be ran
again."* E12 Ruling 12 ruled the mechanism and the fix: the fixture had named five
of eleven elements in the pale-bone family — the literal word "bone" rode the
prompt five times — and the ultra-realistic register renders the word literally:
D2's *bone-tan* on the tail's banded underside and D6's *bone-ivory* blade rows
read as exposed skeleton, and the family pressure invented ivory ridge lines on
the legs (the clay is SMOOTH there — paint, not geometry) and on D1's green wing
fingers, **on both measured seeds**. A same-canon re-roll cannot remove it; the
canon is corrected instead (Ruling 12e): **D2 → pale olive-tan · D6 → charcoal ·
D7 → charcoal**; D4/D5/D10 keep ivory at the head. The register (CONFIRMED, 11a),
the canny pair (0.05/0.10), the backdrop, the frames and the 9d/10i stem split are
all unchanged. **This is the Ruling 10c precedent: a spec change makes a NEW
decision bundle — allowances reset; nothing here is a third roll of anything.**

### You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 11 and 12. 12e is the correction; 12f is THIS dispatch.
canon/DRAGON-IDENTITY.md                   <- D2/D6/D7 corrected in place, old wording preserved
profiles/beast.json                        <- the corrected protective entry; twin_prompts status = REBUILD TO v5
docs/experiments/E12-twin-prompts.json     <- v4 on disk; you rebuild v5
docs/experiments/E12-handoff5-report.md    <- what the last generations measured, incl. the wing-rim artifact
```

Your rules (CLAUDE.md §executor): never judge whether output is good · predictions
blind before looking, blind status disclosed · stop at every gate · no memory-store
writes · a negative result is a full success.

### Environment, standing

Watchdog verified before any local Blender/GPU leg, report either way (restart is
standing authorization: `pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1`;
the ceiling is never raised) · generation cloud-only, full discipline: saved
workflow JSON is the submitted graph · in-code link-topology guard · the no-LoRA
pre-flight (no loader node, never a card at weight 0) · `dry_run` then
`estimate_credits` before any execution · uploads named by content hash · sidecar
at birth · ASCII prints · Blender through PowerShell · output tree: a new
`E:\AI\training\facet_next\E12_repair\repaint_v2\` subdirectory · **read `git log`
before any push; commit with explicit paths only** (the handoff-5 finding) · touch
nothing under E10/E11 artifacts, either accepted asset, or the 00001/00002 trees.

### Blind predictions, before anything runs

Commit a predictions file BEFORE the first rebuild or render, hashed, blind status
stated (this dispatch's seat has seen both prior seeds' outputs — disclose exactly
what, per the handoff-5 form), covering at minimum: do the leg/tail/arm bone reads
leave under the corrected palette · do D1's haunch green and D3's membrane grey
HOLD on the new prompt (a changed prompt re-rolls every landing — regression is a
named branch, not a surprise) · does the wing-rim mouth artifact recur · where
does charcoal land (D6 spines, D7 claws) and does it separate from storm-grey
sheets and slate mouth at the eye's zoom.

### Task 1 — rebuild the prompts file to v5

`tools/diagnostics/e12_make_twin_prompts.py` against the corrected profile entry.
The 9d/10i drop map is unchanged (mouth family off {3,4,5}, horn family off
{3,5}); the headclay_0 key rebuilds from the corrected entry with its own
recorded keeps/drops (15 of 17 terms, D6/D7 dropped). Verify: every stem is a
subsequence-by-whole-comma-terms of the corrected entry; print the per-view term
counts; the file carries version `E12-pair-5`.

### Task 2 — regenerate views 1 and 5

Controls are UNCHANGED — `E12_repair/pair/dragonclay_{1,5}_control.png` derive
from clay + ruled canny + silhouette gradient only; the prompt change does not
touch them. Reuse them; the content-hash upload names give you byte-identity
confirmation free. Seed: **the profile's operating point (770700), both views** —
the bundle is new, the sidecars record the full lineage (770700 rejected pair-v1
register / 770700+770701 re-pair under old palette / this run). One generation per
view, **one bounded re-roll each** on spec-violation grounds only, new seed =
deterministic increment, rejected artifacts stay in the record.

### Task 3 — the sheets, to eyes

Full-size per view: clay | control | styled. The A/B/C progression sheet for view
5 (770700-old-palette | 770701-old-palette | new) and the same regions at zoom
that the Director named: **legs, tail underside, wing arms** at 3×, plus the
wing-rim box at 7× (does the mouth artifact recur), plus HEAD_view1 at 3× and the
membrane field at 3×. No score, no verdict — the E07 class is judged by eye and
the sheets serve the eye.

### Then HALT

Stage: both outputs + sidecars, the sheets and crops, the predictions file scored,
the v5 prompts diff. **All of it to the advisor's eye first, then the Director's.**
His question is one sentence: does this read as the dragon he wants. Handoff 4's
Task 3 (bands + D8 closure) remains acceptance-gated behind that look; the
companion is NOT re-run (Ruling 12f); nothing past the halt runs.

### Do not

Run a third roll within this bundle's allowances · edit any fixture or profile
(advisor's writes) · rebuild or reuse controls at any other canny values · invent
a gate or bound mid-dispatch · arm any structure metric as a gate (Ruling 10d) ·
compare anything to the REJECTED artifacts as baselines (they are evidence) ·
touch thin_extent, the E10/E11 lanes, either accepted asset, or the 00001/00002
artifacts · write to the memory store · end a session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Saved workflows are the submitted graphs; seeds and lineage recorded per sidecar; the v5 prompts file versioned beside its builder; predictions hashed blind before the rebuild |
| ANDON_AUTHORITY | 2 | Watchdog before local legs; topology + no-LoRA guards before every submission; subsequence assertions on every stem; the halt is the Director's eye with the advisor's before it |
| NAMED_COMPENSATORS | 2 | Spend bounded (two generations + two bounded re-rolls max, estimate_credits first); all writes in a new subdirectory; rejected artifacts retained; prompts v4 preserved in git history |
| DECOMPOSE_BY_SECRETS | 3 | The prompt is the only changed input — controls, frames, canny, register, seeds all pinned to recorded values; the canon correction lives in the fixture and reaches the run only through the committed builder |
| UNCERTAINTY_GATED_HUMANS | 3 | The bundle exists because the Director's eye gated the last one; his question is pre-stated; regression branches pre-registered so no outcome needs improvisation |
| EXTERNAL_VERIFIER | 2 | Two generations against one corrected spec, judged by eyes the numbers cannot replace; `skip:` on a second model per the arc's precedent |

### Calibration

The handoff-5 seat's discipline is the standard: the works-perfectly test before
reading any new number, refusals over improvisations, artifacts staged before the
halt. One addition from Ruling 12: **a changed prompt re-rolls every landing** —
treat every element as newly rolled, score the old holds as predictions, and
report regressions as findings rather than surprises.

---

## Session handoff 7 (2026-08-06) — the palette bands against the ACCEPTED pair, and the D8 closure. Comprehensive.

Serves the holding handoff-6 session (git pull first) or a fresh one — it assumes
nothing not written here or in the reading list.

### Where this stands

**THE PAIR IS ACCEPTED** (E12 Ruling 14, the Director: "I accept. Very good!"):
`repaint_v2/target_1_head_seed770700_v5.png` + `target_5_tail_seed770700_v5.png`,
prompts `E12-pair-5`, canny 0.05/0.10, ultra-realistic NO-LoRA register, seed
770700 both views, 0 credits. Acceptance unblocks handoff 4's Task 3, which is
this dispatch. Three deviations were named at acceptance and are accepted AT THE
PAIR, with fixture dispositions landing on THIS task's measurements: **view 1's
foot claws landed ivory** (D7 declares charcoal — the Ruling 13d resemblance
finding), **view 1's cheek/jaw spike fan landed charcoal-brown** (D5 declares
bone-ivory; the crown spikes above it kept... measure, don't assume), and **the
membranes grade** slate-to-pale (ruled a lit-translucency read, 13e). The
suspended handoff-4/5 bands died with the rejected first pair (Ruling 10e);
non-circularity holds — bands derive from the FIXTURE cross-checked against the
ACCEPTED pair, never against the twins they will later gate.

### You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 12-14. 14 is the acceptance; 13d/13e are the deviations.
canon/DRAGON-IDENTITY.md                   <- the eleven elements AS CORRECTED (D2 olive-tan, D6/D7 charcoal)
profiles/beast.json                        <- the corrected protective entry; _still_suspended.palette_bands
E:\AI\training\facet_next\E12_repair\repaint_v2\   <- the accepted pair + sidecar + family instruments
docs/experiments/E04-task4d-report.md      <- the bands precedent (the galleon's derivation form)
docs/experiments/E12-task45-report.md      <- the REJECTED pair's suspended bands (context only, never a source)
docs/experiments/E12-handoff6-report.md    <- the measured landings you will be banding
```

Your rules (CLAUDE.md §executor): never judge whether output is good ·
predictions blind before looking, blind status disclosed · stop at every gate ·
no memory-store writes · a negative result is a full success.

### Environment, standing

No generation and no GPU in this dispatch — it is colour arithmetic on artifacts
already in hand (verify the watchdog anyway if any Blender/render leg becomes
necessary, and report either way; its fourth death and 15:42 restart are Ruling
13a). ASCII prints · scripts create their own output dirs · output tree:
`E:\AI\training\facet_next\E12_repair\bands_v2\` · explicit git paths only ·
touch nothing under E10/E11 artifacts, either accepted asset, or the
00001/00002 trees.

### Blind predictions, before anything runs

Commit a predictions file BEFORE the first measurement, hashed, blind status
stated (disclose exactly what this seat has already seen of the pair), covering
at minimum: does the H1/H4 hue-collapse recur under the new register (the
rejected pair realised eleven materials as ONE 42-degree hue group on 81.6% of
the subject — Ruling 10e banked it register-confounded; this is the test) · the
backdrop's realised separation vs the asked 0.2000 and the rejected pair's
0.2353 · which fixture elements band cleanly vs land contested · where the
ivory-family merge question (D4 / D5-crown / D10) lands · chroma-floor
expectations for the dark elements (charcoal, slate, wine — below a chroma
floor, hue is not a colour).

### Task 1 — the palette bands, derived from the fixture against the accepted pair

Per element D1–D11 of the CORRECTED fixture: locate the element's landed surface
on whichever pair view carries it (say which view and where; the handoff-6
family instruments and boxes are reusable), report the realised triple(s)
(CIELAB D65, the house convention), and propose the band with its chroma floor.
Requirements, each load-bearing:

- **Non-circularity**: bands derive from fixture words cross-checked against the
  PAIR. The twins they will later gate contribute nothing. The rejected pair
  contributes nothing.
- **Contested elements are REPORTED, not banded.** D7 (ivory on view 1, charcoal
  on view 5 — same element, two landings) and D5 (cheek fan charcoal, crown
  measure-first) get their per-view numbers and NO proposed band — the advisor
  rules their dispositions and the ruling pays for the bands. Suspend rather
  than invent; numerator and denominator; stop.
- **D8 eyes and D9 tongue stay below any area floor — no numeric gate on
  either** (the G7 lesson, pre-registered since handoff 2).
- **The forbidden-span arithmetic** over the proposed bands, with the backdrop's
  realised triple and its minimum distance to every band (the 8a/8b line
  re-measured under the accepted register — the derivation promised this
  re-measure at the accepted pair).
- **The H1/H4 collapse re-measure**: hue-group census over the figure on both
  views, the rejected pair's method, so the register confound resolves one way
  or the other.
- **Chroma floors quoted per band** — any hue number carries its chroma or it is
  not quoted (two instruments have been bitten; the rule is standing).
- **The membrane gradient is banded honestly or suspended**: D3 may need a
  lightness RANGE (slate-to-cream) rather than a point band; if the data cannot
  support one band, report the strata and suspend — the 13e ruling anticipated
  exactly this.

### Task 2 — the D8 closure, on the accepted artifact

Ruling 2's named checkpoint, held open through 10g (passed-as-mechanism on a
rejected artifact) — close it on the accepted one: the ember-orange landing on
view 1, px count, largest blob, location against the head region, at zoom, eye
judged. No floor, no gate — the closure is the record that the checkpoint's
question (can the pipeline paint a convincing eye on the measured recess) is
answered on an artifact that stands. Cross-reference the 12g annotation (the
bust-scale companion did NOT paint one under the denser control) so the closure
carries both facts.

### Then HALT

Stage: the per-element table (realised triples, proposed bands, chroma floors),
the contested-element numbers with no bands, the forbidden-span arithmetic, the
collapse census, the D8 closure evidence at zoom, the predictions file scored.
**All of it to the advisor's eye first, then the Director's** if his window is
wanted. The advisor rules the bands into the profile, rules D5/D7 dispositions,
and only then do twins run (handoff 8 — not yours).

### Do not

Band a contested element · arm any threshold the data cannot support (suspend +
report) · touch the twins question or generate anything · compare to the
rejected pair except where a task names it as the confound baseline · edit any
fixture or profile (advisor's writes) · write to the memory store · end a
session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Predictions hashed blind before measurement; every triple carries its box, view and mask provenance; the instruments are the committed handoff-6 pair, re-validated against published figures before new numbers |
| ANDON_AUTHORITY | 2 | Contested elements halt to the ruling rather than being banded; suspension is the specified response to unsupportable thresholds; the halt is the advisor's eye |
| NAMED_COMPENSATORS | 2 | No generation, no spend, no irreversible step; all writes in a new subdirectory + one new report; nothing pre-existing opened for writing |
| DECOMPOSE_BY_SECRETS | 3 | Bands derive fixture-side and are cross-checked pair-side, never twin-side; contested dispositions route to the seat that owns them; the register-confound test is separated from the banding it informs |
| UNCERTAINTY_GATED_HUMANS | 3 | The advisor rules every band and both dispositions before any gate consumes them; D8/D9 stay eye-judged below floors; the Director's window is named |
| EXTERNAL_VERIFIER | 2 | The pair was judged by the Director's eye, not by these instruments; the bands are cross-checked against an artifact the deriving code did not generate. `skip:` on a second model per the arc's precedent |

### Calibration

The handoff-6 seat's standard holds: validate every instrument against a
published figure before reading a new number from it, own method errors in the
report, and state what each measurement returns when nothing is wrong before
reading it. One addition from Ruling 13: where fixture and accepted artifact
disagree, the disagreement IS the deliverable — report it cleanly and leave the
disposition to the ruling. A negative result is a full success.

---

## Session handoff 8 (2026-08-06) — THE TWINS: eight views, the gate validated on the pair first. Comprehensive.

Serves the holding handoff-7 session (git pull first) or a fresh one — it assumes
nothing not written here or in the reading list.

### Where this stands

The pair is ACCEPTED (Ruling 14) and is the subject's generation anchor (the
recipe keys read SPENT, `beast.json _still_suspended.generation_recipe_anchor`).
The bands are RULED (Ruling 15): **warm-olive 85.4–147.3 adopted; blue-violet
suspended** with a pre-registered realised-stratum allowance (273.4–293.4,
pair-realised D3, applied ONLY if the gate's pair-validation demands it); chroma
floor 12.0; D3 is neutral strata, no hue band; D8/D9 below floors, eye-judged;
dark bands match shadow (colour-not-placement). This dispatch generates the
eight `dragonclay` twins the route projects from — **twins belong to THIS mesh**,
their one job is registering to the silhouette they will be projected onto, and
identity rides the stems (v5). Stage 1 is handoff 9, not yours.

### You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 14-15. 15c is the gate's construction; 15k is this dispatch.
profiles/beast.json                        <- bands ruled into _still_suspended.palette_bands; recipe SPENT-anchored
docs/experiments/E12-twin-prompts.json     <- v5 (E12-pair-5): eight dragonclay stems, the ruled per-view drop map
docs/experiments/E12-handoff7-report.md    <- the band table, the strata, the caveats your gate inherits
E:\AI\training\facet_next\E12_pair\clay\   <- the profile-rendered clay views (the pair's controls came from these)
E:\AI\training\facet_next\E12_repair\repaint_v2\   <- the ACCEPTED pair (the gate's calibration artifact)
docs/experiments/E04-twin-run-report.md    <- the ship's twin-run precedent, if present; else the E04 ruling's twin sections
```

Your rules (CLAUDE.md §executor): never judge whether output is good ·
predictions blind before looking, blind status disclosed · stop at every gate ·
no memory-store writes · a negative result is a full success.

### Environment, standing

Watchdog verified before any local Blender/GPU leg, report either way (restart
standing: `pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1`; the ceiling
is never raised; its fourth death and 15:42 restart are Ruling 13a). Cloud
discipline in full: saved workflow JSON is the submitted graph · in-code
link-topology guard · the inverted no-LoRA pre-flight (no loader node ever) ·
`dry_run` then `estimate_credits` before every execution · uploads named by
content hash · sidecar at birth per twin · ASCII prints · Blender through
PowerShell · output tree: `E:\AI\training\facet_next\E12_twins\` · explicit git
paths only · touch nothing under E10/E11 artifacts, either accepted asset, or
the 00001/00002 trees.

### Blind predictions, before anything runs

Commit hashed, blind status disclosed (state exactly what this seat has seen of
the pair and the clay), covering at minimum: the gate's reading on the ACCEPTED
pair per view (does the 15c allowance branch fire?) · per-view registration IoU
range against the pair's precedent (view 1 styled-vs-geometry measured 0.9940;
the twins' construction differs — predict a range, say why) · which stems risk
resemblance-bleed misses (ivory terms ride views {0,1,2,6,7}) · expected
off-palette totals and largest blobs on clean twins (handoff 7's speckle scale
is the prior) · whether any view produces a garment-class invention (the
one-in-eight prior from W3).

### Task 1 — construct the gate; validate it on the pair BEFORE any twin exists

Build the off-palette gate from the RULED bands (warm-olive allowed; chroma
floor 12.0; report total px AND largest connected component per view — the
two-threshold law). **Run it on both accepted-pair views first.**
Pre-registered branches (Ruling 15c, decided before any outcome existed):

- **Quiet on the pair** (speckle-scale totals, no large component) → the gate
  stands as constructed; proceed.
- **Fires on the membrane stratum** (the blue-violet family, view 5's 8.19%) →
  apply the realised-stratum allowance 273.4–293.4, re-validate, report both
  readings; the allowance is then part of the gate and is recorded as
  pair-realised D3, never a fixture band.
- **Fires anywhere else on the pair** → HALT with the evidence. The pair is
  accepted; a gate that flags it is mis-constructed, and that is an instrument
  finding for the advisor.

The gate's clean-baseline numbers on the pair are part of the report whatever
branch fires.

### Task 2 — generate the eight twins

Per view 0–7: control built by the route (`restylize_views.py` — the clay
render composited per the profile's `bg`, ruled canny 0.05/0.10, silhouette
gradient union; the profile supplies every recipe key, now SPENT-anchored),
stem from `E12-twin-prompts.json` v5 by the view's key, **no LoRA node**, seed
per the profile. One generation per view. `estimate_credits` before each
(0-credit expectation, verified not assumed). Sidecar at birth per twin:
provenance + "a twin has one job — register to the mesh; identity rides the
prompt."

### Task 3 — gate, register, sheet

Per twin: the validated gate (total + largest blob; the palette-gate re-roll
precedent applies PER VIEW — one bounded re-roll on a gate firing or a
spec-visible miss, new seed, rejected artifact stays in the record, second
failure is the result) · registration diagnostics against the exact raycast
silhouette (per-view IoU printed; the halt stays suspended at `reg-iou-min
0.0` on this subject — measure, report, the advisor rules whether a beast
bound derives) · bbox diagnostics (vacuous tolerance, printed) · trust-mask ∧
silhouette per the route default. Sheets: per view, clay | control | twin at
full size, plus an 8-view overview, plus crops at any gate firing or
registration outlier. **No verdicts.**

### Then HALT

Stage: eight twins + sidecars, the gate's pair-validation and per-twin
readings, the registration table, the sheets, the predictions file scored.
**All of it to the advisor's eye first, then the Director's.** Stage 1
(projection against the banked 50.46% ceiling) is handoff 9 and runs only
after the advisor rules the twins in.

### Do not

Project anything · run any stroke or texpass step · exceed one bounded re-roll
per view · arm a registration bound (measure and report; the ruling derives or
keeps reporting) · treat the pair as a projection reference (it is the SPEC;
twins are the projection sources) · edit any fixture or profile (advisor's
writes) · compare to the rejected artifacts except as named baselines · touch
thin_extent, the E10/E11 lanes, either accepted asset, or the 00001/00002
trees · write to the memory store · end a session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Saved workflows per view with content-hash input names; seeds and stems recorded per sidecar; predictions hashed blind before the gate exists; the gate's construction cites the ruled band values verbatim |
| ANDON_AUTHORITY | 3 | The gate is validated on an accepted artifact BEFORE it gates anything (a gate that fires on the pair halts as mis-constructed); watchdog before local legs; topology + no-LoRA guards per submission; per-view re-rolls bounded at one; registration halt suspended-not-deleted, diagnostics always printed |
| NAMED_COMPENSATORS | 2 | Spend bounded (eight generations + at most eight re-rolls, estimate_credits first, 0-credit expectation); all writes in a new tree; rejected twins retained in the record; nothing irreversible beyond cloud spend |
| DECOMPOSE_BY_SECRETS | 3 | Twins derive from THIS mesh's clay and silhouettes; identity arrives only through the versioned stems; the gate derives from ruled bands + the pair, never from the twins it gates; every recipe value arrives from the SPENT-anchored profile |
| UNCERTAINTY_GATED_HUMANS | 3 | The halt is the advisor's eye before projection; gate firings and registration outliers surface as evidence, not decisions; the 15c branches were pre-registered by the ruling before any outcome existed |
| EXTERNAL_VERIFIER | 2 | The gate tests twins against a specification derived from an artifact the twins did not produce; registration is measured against geometry the generator does not control. `skip:` on a second model per the arc's precedent |

### Calibration

The handoff-6/7 standard holds: validate every instrument against a published
figure before reading a new number; the works-perfectly test before trusting
any zero; own method errors in the report. Two subject-specific cautions from
the record: **a term can paint a surface it does not name** (Ruling 13d — watch
the ivory-term views' claws and any structure that resembles a named one), and
**the gate cannot see placement** (15d) — a twin can pass every band while
carrying a within-band colour on the wrong structure, which is why the sheets
serve the eye and the eye rules.

---

## Session handoff 9 (2026-08-06) — the wing-skeleton term: v6 stems, regenerate views 0 and 4. Comprehensive.

Serves the holding handoff-8 session (git pull first) or a fresh one — it
assumes nothing not written here or in the reading list.

### Where this stands

The twin run completed (`4864686`, Ruling 17): twins 1 and 5 pixel-identical
to the accepted pair; the view-3 re-roll resolved its achromatic defect at
seed 770701; the resemblance channel resolved (the bleed rides the fangs
term). The Director's eye then found **the wing skeleton painted bone-ivory
on the two wing-spread views (0 and 4)** while the same structures read green
on every folded-wing view. Ruling 17e named the cause — the wing arms and
fingers were D1's surface by fixture assignment but **no prompt term ever
named them**, and the unclaimed bone-shaped structures took the horns' ivory
on exactly the views that present them as a bat-wing skeleton — and the fix:
**`moss-green wing arms and finger struts` now stands in the protective entry
as its own noun phrase**, riding every view. This dispatch rebuilds the stems
to v6 and regenerates ONLY views 0 and 4 under them.

### You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 16-17. 17e is the term; this dispatch is its execution.
profiles/beast.json                        <- the protective entry WITH the wing-skeleton term; twin_prompts: REBUILD TO v6
canon/DRAGON-IDENTITY.md                   <- D1 annotated with the term addition
docs/experiments/E12-twin-prompts.json     <- v5 on disk; you rebuild v6
docs/experiments/E12-handoff8-report.md    <- the twin run's record; the gate + achromatic baselines you re-use
E:\AI\training\facet_next\E12_twins\       <- masks, controls, twins; views 0/4's controls are REUSED as-is
```

Your rules (CLAUDE.md §executor): never judge whether output is good ·
predictions blind before looking, blind status disclosed · stop at every
gate · no memory-store writes · a negative result is a full success.

### Environment, standing

Watchdog verified before any local leg, report either way (restart standing;
the ceiling is never raised). Cloud discipline in full (saved workflows ·
topology guard · no-LoRA pre-flight · `dry_run` + `estimate_credits` per
submission · content-hash uploads · sidecars at birth). ASCII prints ·
output continues in `E:\AI\training\facet_next\E12_twins\` (new files
suffixed `_v6`) · explicit git paths · touch nothing under E10/E11, either
accepted asset, or 00001/00002.

### Blind predictions, before anything runs

Commit hashed, blind status disclosed, covering at minimum: does the wing
skeleton land green on 0 and 4 under the named term · does anything REGRESS
on those views (a changed prompt re-rolls every landing — the Ruling 12f
law; score every element, not just the target) · do the membranes stay in
13e's class · the gate + achromatic readings vs the handoff-8 baselines ·
whether the crown-region ivory mass on view 4 (behind the horns) moves.

### Task 1 — rebuild the prompts to v6

The committed builder against the corrected entry. The new term rides
**every view** (wings are visible from all eight yaws). Drop map unchanged
(mouth off {3,4,5}, horn family off {3,5}); `headclay_0` rebuilds from the
corrected entry with its recorded keeps/drops. Verify: subsequence-by-whole-
comma-terms per stem; the eight v5 `dragonclay` stems differ from v6 by
EXACTLY the one inserted term; version `E12-pair-6`; print per-view term
counts.

### Task 2 — regenerate views 0 and 4 only

Controls and masks REUSED byte-identical from the twin run (the term change
does not touch geometry); content-hash upload names confirm identity free.
Seed 770700 (the operating point — same seed the defective twins ran, so the
term is the only delta per view). One generation per view; each carries its
own single bounded re-roll on spec-violation grounds only. Views
1/2/3B/5/6/7 are NOT regenerated (Ruling 17e: 1 and 5 are pixel-identical to
the accepted pair; the others carry no ruled defect).

### Task 3 — gate, register, sheet

Per new twin: the 16e gate + the 17d achromatic channel, both against the
recorded baselines · registration diagnostics (suspended halt, printed
IoU) · the same-view A|B sheet (v5 twin | v6 twin) full size plus the wing
crops at 3× (arms, fingers, crown region on 4) · sidecars with full lineage
(seed, stem version, superseded v5 twin named). **No verdicts.**

### Then HALT

Stage: both v6 twins + sidecars, A|B sheets + crops, gate/achromatic/
registration tables, predictions scored, the v6 prompts diff. **To the
advisor's eye first, then the Director's.** Stage 1 is handoff 10 and runs
only after the advisor rules the completed twin set in.

### Do not

Regenerate any view but 0 and 4 · exceed one bounded re-roll per view ·
touch the accepted-pair-identical twins 1 and 5 · arm any bound · edit any
fixture or profile (advisor's writes) · write to the memory store · end a
session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | v6 versioned beside its builder with an exact-one-term diff assertion; controls/masks reused by content-hash identity; seeds pinned; predictions hashed blind first |
| ANDON_AUTHORITY | 2 | Watchdog before local legs; both guards per submission; the exact-one-term diff is an ANDON (any other delta halts the rebuild); bounded re-rolls; halt to eyes |
| NAMED_COMPENSATORS | 2 | Two generations + at most two re-rolls, estimate_credits first; v5 twins retained and named superseded in sidecars, never deleted; all writes suffixed _v6 |
| DECOMPOSE_BY_SECRETS | 3 | The term is the only changed input, asserted in code; geometry inputs byte-identical by hash; the fix reaches the run only through the committed builder reading the committed profile |
| UNCERTAINTY_GATED_HUMANS | 3 | The regeneration exists because the Director's eye gated the set; both outcome branches pre-registered in Ruling 17e; regression scoring pre-committed so a fixed wing cannot hide a broken flank |
| EXTERNAL_VERIFIER | 2 | Two generations against one named spec change, judged by eyes; gate + achromatic channels run against baselines derived from artifacts this run did not produce. `skip:` on a second model per precedent |

### Calibration

A changed prompt re-rolls every landing — score the whole view, not the
target. The works-perfectly test: state what the A|B sheet shows if the term
does nothing (v5-identical landings modulo seed-invariant noise — but the
seed is pinned, so a no-op term should reproduce v5 nearly exactly; any
broad change IS the finding). And the handoff-8 standard stands: validate
instruments against recorded baselines before new numbers, own errors in
the report, halt with everything staged.

---

## Session handoff 10 (2026-08-06) — the split term: v7 stems, regenerate view 4 only. Comprehensive.

Serves the holding handoff-9 session (git pull first) or a fresh one — it
assumes nothing not written here or in the reading list.

### Where this stands

Handoff 9 landed the wing-skeleton term in full on view 0 (−66.4%, every strut
green — that twin STANDS) and half on view 4: the arms went green, the finger
struts stayed cream (−29.3%) on the view that presents the wings as the
archetypal bat skeleton. Ruling 18c read the split — the compound phrase's
head noun bound, its second conjunct under-bound — and RULED the fix: the
term splits into **`moss-green wing arms` + `moss-green wing finger struts`**,
each its own noun phrase, every view. The Director ruled the crown question
(18g: D5 stays ivory, judged at Gate 1 on the asset), so this dispatch's
scope is the split term alone. **View 4 is the only regeneration.**

### You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 17-18. 18c is this dispatch; 18g bounds it.
profiles/beast.json                        <- the split-term entry; twin_prompts: REBUILD TO v7
docs/experiments/E12-twin-prompts.json     <- v6 on disk; you rebuild v7
docs/experiments/E12-handoff9-report.md    <- the v6 baselines every v7 number reads against
E:\AI\training\facet_next\E12_twins\       <- masks, controls, twins; view 4's inputs REUSED as-is
```

Your rules (CLAUDE.md §executor): never judge whether output is good ·
predictions blind before looking, blind status disclosed · stop at every
gate · no memory-store writes · a negative result is a full success.

### Environment, standing

Watchdog verified before any local leg, report either way. Full cloud
discipline (saved workflow · topology guard · no-LoRA pre-flight · `dry_run`
+ `estimate_credits` · content-hash uploads · sidecar at birth). ASCII
prints · outputs suffixed `_v7` in the twins tree · explicit git paths ·
touch nothing under E10/E11, either accepted asset, or 00001/00002.

### Blind predictions, before anything runs

Hashed, blind status disclosed, covering at minimum: do the struts land
green under their own noun phrase on view 4 · does anything regress on the
view (score every element — a changed prompt re-rolls every landing) · the
gate + achromatic readings vs the v6 baselines (state the expected
direction: if the struts go green, the gate number should RISE a third
time — pre-register it so the inversion is confirmation, not surprise) ·
whether view 0-class full binding or view-4-class partial binding is the
outcome (the two prior points bound the prediction).

### Task 1 — rebuild the prompts to v7

The committed builder against the split-term entry. ANDON: each v7
`dragonclay` stem differs from v6 by EXACTLY the one-term-to-two-terms
substitution (remove both new terms and what remains is byte-equal to v5's
stem minus nothing — assert the construction, not the intention); drop map
unchanged; `headclay_0` rebuilds with its recorded keeps/drops; version
`E12-pair-7`; per-view term counts printed.

### Task 2 — regenerate view 4 only

Inputs REUSED byte-identical (content-hash names confirm free). Seed
770700 — the term split is the only delta against the v6 run. One
generation; its single bounded re-roll available on spec-violation grounds
only. No other view regenerates.

### Task 3 — gate, register, sheet

The 16e gate + 17d achromatic channel vs the recorded baselines ·
registration diagnostics (suspended halt, printed) · the three-way sheet
v5 | v6 | v7 full size plus the wing crops at 3× (left wing, right wing,
struts) and the crown at 3× (18g's judge-at-asset means the crown is
REPORTED here, not acted on) · sidecar with full lineage. **No verdicts.**

### Then HALT

Stage: the v7 twin + sidecar, the three-way sheet + crops, the tables, the
predictions scored, the v7 prompts diff. **To the advisor's eye first, then
the Director's.** On the advisor ruling the completed set in, stage 1 is
handoff 11 (projection against the banked 50.46% ceiling).

### Do not

Regenerate any view but 4 · exceed its one bounded re-roll · touch twins
0(v6)/1/2/3B/5/6/7 · act on the crown (18g: judged at Gate 1) · arm any
bound · edit any fixture or profile · write to the memory store · end a
session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | v7 versioned with an exact-substitution ANDON against v6 read from git; inputs by content-hash identity; seed pinned; predictions hashed blind first |
| ANDON_AUTHORITY | 2 | Watchdog before local legs; both guards per submission; the stem ANDON halts any unintended delta; one bounded re-roll; halt to eyes |
| NAMED_COMPENSATORS | 2 | One generation + at most one re-roll, estimate_credits first; the v6 view-4 twin retained and named superseded; all writes suffixed _v7 |
| DECOMPOSE_BY_SECRETS | 3 | The split is the only changed input, asserted in code; geometry inputs byte-identical; the fix reaches the run only through the committed builder |
| UNCERTAINTY_GATED_HUMANS | 3 | Scope bounded by the Director's own 18g sentence; both 18c branches pre-registered; regression scoring pre-committed |
| EXTERNAL_VERIFIER | 2 | One generation against one named change, judged by eyes against baselines this run did not produce. `skip:` per precedent |

### Calibration

The works-perfectly test, stated for this dispatch: if the split changes
nothing, v7 reproduces the v6 view-4 twin near-exactly at the pinned seed —
so ANY broad change is signal, and the struts are the register to read
first. Score the whole view; the crown is reported, not judged; a negative
result (struts still cream) is a full success and closes the
positive-naming lever per 18c's pre-registered branch.

---

## Session handoff 11 (2026-08-06) — THE EXEMPLAR REBUILD (v8, all eight) + E13 Gate 0 (the projector's crop cameras, anchored). Comprehensive.

Serves the holding handoff-10 session (git pull first) or a fresh one — it
assumes nothing not written here or in the reading list.

### Where this stands

The Director's directive (Ruling 20): **these sprites are exemplars** — they
feed the E11 training lane, define the method, and will be displayed — so the
texture route runs over whole rather than patching the accumulated set. The
canon is now occupancy-complete (Ruling 20c: the nape crest named its own
term, D6 extended, D5's list explicit, the audit table in the fixture). The
current v5/v6/v7 twins are the E12 measurement record — retained, superseded,
never inputs here. E13 (the detail pass) is specced and amended; its Gate 0
— the projector's crop-camera capability, anchored — is this dispatch's
second leg because it is independent of generation and blocks stage 1.

### You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 19-20. 20b is the directive; 20c the completed canon.
docs/experiments/E13-detail-pass-spec.md   <- the spec + amendment. Gate 0 is YOUR Task 3.
profiles/beast.json                        <- the v8-source entry; twin_prompts: REBUILD TO v8
canon/DRAGON-IDENTITY.md                   <- occupancy-complete; the audit table
docs/experiments/E12-handoff8-report.md    <- the gate/achromatic baselines and twin-run method
E:\AI\training\facet_next\E12_twins\       <- masks + controls (REUSED - geometry unchanged)
```

Your rules (CLAUDE.md §executor) and the standing environment/cloud
discipline are handoff 8's, unchanged (watchdog verified either way ·
saved workflows · topology guard · no-LoRA pre-flight · dry_run +
estimate_credits (the structural-identity proof pattern is ratified) ·
content-hash uploads · sidecars at birth · ASCII prints · explicit git
paths). Output tree: `E:\AI\training\facet_next\E13_twins\`.

### Blind predictions, before anything runs

Hashed, blind status disclosed, covering at minimum: per-view landings of
the three NEW/CHANGED terms (neck spines charcoal at the nape? wing
skeleton green on 0 AND 4 at this seed? spurs?) · whether 770700's
term-resistance recurs on the wing struts (the 20a caveat — pre-register
which views you expect to spend re-rolls on) · gate + achromatic
expectations vs the handoff-8 baselines · registration range · the Gate 0
anchor (must be exactly 0 differing pixels — state it).

### Task 1 — v8 stems

The committed builder against the occupancy-complete entry. ANDON: v8 vs v7
differs by EXACTLY the one inserted term (`charcoal neck spines`) plus the
audit's term substitution if any; subsequence assertions; drop map
re-verified against the renders (the neck spines are silhouette-visible
from every yaw — expect them everywhere); `headclay_0` rebuilds; version
`E12-pair-8`; per-view counts printed.

### Task 2 — the exemplar base coat: all eight views, fresh

Controls and masks REUSED byte-identical (geometry unchanged; hash names
confirm free). Seed 770700 per view (the operating point; the 20a caveat
makes re-roll spends EXPECTED, not surprising — each view carries its one
bounded re-roll on spec-visible grounds, the deterministic increment).
The 16e gate + 17d achromatic channel per twin against the recorded
baselines · registration diagnostics (suspended halt, printed) · per-view
clay | control | twin sheets full size + an eight-view overview + crops at
any firing. The exemplar bar means: **flag anything your eye catches even
if no instrument does** — the record shows the eye leads the instruments
on this subject.

### Task 3 — E13 Gate 0: the projector learns crop cameras, and proves it changed nothing

Extend `project_twins.py` with per-view crop-camera parameters
(`--ortho-scale`, `--centre`, defaulting to the full-figure values the tool
already derives). **The anchor (E13 Gate 0, blocks everything downstream):**
re-run a RECORDED projection through the new parameter path at full-figure
values and require **pixel-identical output** (the E08/E04 anchor
discipline; bytes may differ, pixels may not). Any deviation halts E13 at
zero spend and is a finding. No crop projection runs this session — the
capability is proven, not used.

### Then HALT

Stage: the eight v8 twins + sidecars, sheets, gate/achromatic/registration
tables, the Gate 0 anchor evidence, predictions scored. **To the advisor's
eye first, then the Director's — his bar is the exemplar bar.** On his
acceptance: the E13 crop twins (head region), stage 1 on the allocated
atlas (A2's arithmetic lands with the crop dispatch), and the route.

### Do not

Exceed one bounded re-roll per view · project anything (Gate 0 proves, it
does not use) · touch the E12 measurement-record twins, the accepted pair,
E10/E11 artifacts, or 00001/00002 · arm any bound · edit any fixture or
profile · write to the memory store · end a session the Director has not
ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | v8 versioned with an exact-delta ANDON; inputs by content-hash identity; seeds pinned; the anchor pins the tool extension to a recorded projection; predictions hashed blind first |
| ANDON_AUTHORITY | 3 | Gate 0 halts E13 at zero spend on any pixel deviation; per-twin gates before any acceptance; bounded re-rolls; the eye explicitly deputised to flag past the instruments |
| NAMED_COMPENSATORS | 2 | Eight generations + at most eight re-rolls, estimate_credits first; the tool extension is additive with defaults preserving old behaviour, proven by the anchor; all writes in a new tree |
| DECOMPOSE_BY_SECRETS | 3 | The entry is v8's single source; capability (crop cameras) separated from policy (which crops, later) and from generation; the measurement record never feeds the exemplar run |
| UNCERTAINTY_GATED_HUMANS | 3 | The halt is the Director's exemplar bar with the advisor's eye first; expected re-roll spends pre-registered so spending reads as process, not surprise |
| EXTERNAL_VERIFIER | 2 | The anchor tests new code against old output; twins judged by eyes against a spec they did not generate. `skip:` per precedent |

### Calibration

The handoff-8/10 standard holds. Three subject cautions ride: term binding
is seed-dependent (20a) — a resisted term at 770700 is a re-roll, not a
naming failure; the eye leads the instruments here (three of four
Director-caught defects were invisible to every armed number); and the
exemplar bar is the acceptance bar — a twin that passes every gate and
reads mushy at zoom is a flag, not a pass.

---

## Session handoff 12 (2026-08-06) — the membrane iteration (v9, seven views) + the harmonization instrument. Comprehensive.

Serves the holding handoff-11 session (git pull first) or a fresh one — it
assumes nothing not written here or in the reading list.

### Where this stands

The Director ruled three things on the exemplar set (Rulings 21–22): **view
4-A stands** (the true nape; B stays in the record), **the membranes
iterate once before stage 1** (his sentence — the base coat is their only
paint source), and **cross-view tone consistency is now a named
requirement** ("Not very consistent," views 4|5 — the honest cost of
per-view generation, generalising 17f's watch item from membranes to the
hide). The term is ruled: `leathery storm-grey wing membranes` (22b — the
opacity cue against the measured translucency prior; hue family
unchanged). The tonal answer is ruled as a measured arm: **the
harmonization pass** (22e — deterministic Lab colour-statistics transfer
inside the figure mask toward reference view 1, applied per view before
projection; semantic work stays with the term, tonal work with the
transfer).

### You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E12-ruling.md             <- Rulings 21-22. 22b/22c/22e are this dispatch.
profiles/beast.json                        <- the leathery entry; twin_prompts: REBUILD TO v9
canon/DRAGON-IDENTITY.md                   <- D3's term strengthened, mechanism noted
docs/experiments/E12-handoff11-report.md   <- the v8 baselines every v9 number reads against
E:\AI\training\facet_next\E13_twins\       <- v8 twins + your committed instruments (reused)
```

Your rules (CLAUDE.md §executor), the standing environment and the full
cloud discipline are handoff 11's, unchanged. Output: same tree, `_v9`
suffixes; the harmonization work under `harmonize/`.

### Blind predictions, before anything runs

Hashed, blind status disclosed, covering at minimum: does `leathery` move
the membranes toward neutral grey (per-view membrane-box chroma/hue vs the
v8 readings — state expected direction and rough magnitude) · which views
spend re-rolls (the 21c map: view 3's black limb is EXPECTED at the
operating point) · does any regression appear on the six other changed
views (a changed prompt re-rolls every landing) · harmonization: the
identity test on view 1 (must be exact), and the expected direction of the
figure-mask Lab deltas per view.

### Task 1 — v9 stems

The committed builder + `e12_stem_delta.py` ANDON: v9 differs from v8 by
EXACTLY the one-term substitution, all stems, drop map unchanged,
`headclay_0` rebuilt, version `E12-pair-9`, counts printed.

### Task 2 — regenerate views 0, 1, 2, 3, 5, 6, 7

**View 4 is NOT regenerated** (22c — his sentence chose 4-A; regenerating
it would discard the choice). Inputs reused byte-identical (hash-confirmed
free). Operating-point seed per view; one bounded re-roll each on
spec-visible grounds (view 3's is pre-registered as expected). Per twin:
the 16e gate + 17d achromatic channel + registration via your committed
readout, against the v8 baselines · membrane-box chroma/hue per view (the
question his sentence asked) · per-view clay | control | twin rows and an
eight-row overview (v9 ×7 + v8-A view 4 — the set as it would stand).

### Task 3 — the harmonization instrument, built and validated, NOT adopted

`e13_harmonize.py` (committed, not throwaway): per-view Lab
colour-statistics transfer inside the exact figure mask toward **reference
view 1's v9 twin**, output beside the raw twin, never replacing it.
Requirements: **identity on the reference** (view 1 harmonized toward
itself is byte-identical — the works-perfectly test); the transfer's
operands recorded per view (mean/σ per channel, before and after); a
per-view **raw | harmonized** A/B sheet at full size plus the 4|5-class
pairs the Director's observation was made on; the membrane and hide boxes
re-measured on the harmonized outputs so the tonal move is a number as
well as a look. **Adoption is a ruling, not this session's call** — stage
nothing into the projection inputs.

### Then HALT

Stage: the seven v9 twins + sidecars + re-roll artifacts, the completed-set
overview, the gate/achromatic/registration/membrane tables, the
harmonization A/Bs with their operands, predictions scored. **To the
advisor's eye first, then the Director's** — his two questions are
pre-stated: are the membranes storm-grey now, and does the harmonized set
read as ONE dragon.

### Do not

Regenerate view 4 · exceed one bounded re-roll per view · adopt
harmonization into any projection input · project anything · arm any bound
· edit any fixture or profile · write to the memory store · end a session
the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | v9 exact-delta ANDON against git; inputs by content hash; seeds pinned with expected deviations pre-registered; harmonization operands recorded per view; predictions hashed blind first |
| ANDON_AUTHORITY | 3 | The stem ANDON; both cloud guards per submission; the identity test gates the harmonization instrument before any number is read from it; bounded re-rolls with the expected spend named in advance; halt to eyes |
| NAMED_COMPENSATORS | 3 | 0-credit expectation verified per submission; harmonized outputs land BESIDE raw twins, never replacing them, adoption explicitly reserved to a ruling; view 4-A untouched; all prior artifacts retained |
| DECOMPOSE_BY_SECRETS | 3 | The term change is semantic, the transfer is tonal, and the dispatch keeps them in separate tasks with separate measurements; the reference view is named by ruling, not chosen by the session |
| UNCERTAINTY_GATED_HUMANS | 3 | The round exists on the Director's two sentences; his acceptance questions are pre-stated; the consistency judgement is his eye on the A/B sheets, not a statistic |
| EXTERNAL_VERIFIER | 2 | Twins judged against a spec they did not generate; the transfer validated by an identity test its own code cannot fake; `skip:` per precedent |

### Calibration

The handoff-11 standard holds. The set's acceptance question is now
CROSS-VIEW: after the per-view checks, put the seven v9 twins and view 4-A
side by side and flag tonal disagreement the way the Director's eye would —
the raw|harmonized sheets exist to make that comparison decidable rather
than felt.

---

## Session handoff 13 (2026-08-06) — E13's head-crop twins, A2's arithmetic, and STAGE 1. Comprehensive.

Serves the holding handoff-12 session (git pull first) or a fresh one — it
assumes nothing not written here or in the reading list.

### Where this stands

The base coat is RULED (Ruling 23f): **warm membranes accepted · the
harmonization ADOPTED** — projection consumes the harmonized set (v9 ×6 +
view 3's 770701 cure + view 4-A, all toward reference view 1, operands in
`harmonize/operands.json`, raw twins retained). E13 Gate 0 passed (the
projector's crop-camera path proven at 0 differing pixels). This dispatch
runs the E13 head-crop pass and stage 1 — the route's projection stage —
with the A0/A1 comparison the spec pre-registered, so the Director judges
the detail pass's payoff against evidence.

### You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                  <- how to work here. Read first, follow exactly.
docs/experiments/E13-detail-pass-spec.md   <- THE SPEC. A1/A2, the gates, H3's branches. This dispatch executes it.
docs/experiments/E12-ruling.md             <- Rulings 21-23. 23f is the ruled input set.
profiles/beast.json                        <- every value; the prep bake exists (handoff 2, head-scale 1.0)
docs/experiments/E12-twin-prompts.json     <- v9; crop stems derive per crop with recorded keeps/drops
E:\AI\training\facet_next\E13_twins\       <- the ruled set + harmonize/ + your committed instruments
E:\AI\training\facet_next\E12_prep\        <- prep_uv.glb + the existing 4096 atlas state
E:\AI\training\facet_next\E12_gate0\head_00003.json    <- the head box; the companion's frame derivation precedent
docs/experiments/E12-companion-sidecar.md  <- the crop construction, worked once
```

Your rules (CLAUDE.md §executor), the standing environment and full cloud
discipline are handoff 11's, unchanged. Output: `E13_twins/crops/` for the
crop pass, `E13_stage1/` for projection. Blind predictions first, hashed,
blind status disclosed: A2's ratio (state the expected direction) · crop
twin landings at bust scale (D8/D10/D5 per the companion's precedent) ·
whether crop-twin generation hits the 21c seed-resistance class · stage-1
styled/valid against the 50.46% ceiling (the ship ran 86.4% of its
ceiling; the character 92.8% — state a range and say why) · H3's branch.

### Task 1 — A2's arithmetic, under the pre-registered rule

Measure: head-region atlas texels (the head box's faces → their UV area at
the existing 4096 bake) against the crop twins' pixels landing on them.
**The decision rule, registered here before the number exists**: if the
atlas under-resolves the crop paint (texels-per-crop-pixel < 1.0),
head-scale arms at the value that brings the ratio to ~1.0, **capped at
2.0**, and the prep re-bake runs before stage 1 (the bake's own ANDONs are
the expressibility halt — report and stop if one fires); if the ratio is
already ≥ 1.0, no re-bake, stated with the number. Either way the
arithmetic and the decision print together.

### Task 2 — the head-crop twins (E13 A1)

Yaws **0 and 45**, the companion's construction at the route's cameras:
crop frame from `head_00003.json` padded 1.12 (the recorded derivation),
crop silhouette by direct raycast, control at ruled canny 0.05/0.10, crop
stems derived per crop from the v9 entry with visibility verified against
the crop renders (recorded keeps/drops per the companion precedent; the
neck-spine term stays if the crest enters the crop — verify, don't
assume). Operating seed; one bounded re-roll each (the 21c resistance
class is pre-registered as possible). Per crop twin: the 16e gate + 17d
achromatic + registration at the crop frame (IoU printed; the companion's
0.9940 is the precedent) · **harmonized toward reference view 1 by the
committed transfer** (identity test re-run first; operands recorded) ·
sidecar at birth: projection-source declaration + full lineage.

### Task 3 — STAGE 1, twice: the A0 baseline and the composed run

Both on the Task-1 atlas (re-baked or not, per the rule):

1. **A0 — baseline**: project the eight harmonized full-figure twins,
   standard path, recorded invocation.
2. **A1 — composed**: fresh accumulating state; project the harmonized
   CROP twins FIRST through the proven crop-camera parameters, then the
   eight harmonized full twins. The never-overwrite invariant composes
   them; the crop paint owns what it reaches.

Requirements: **the reach-invariance check** — the ceiling instrument
re-runs and must return 50.46% of 3,240,510 unchanged; any delta HALTS
(wrong camera geometry, not new reach) · styled/valid and
styled/reachable for both runs, read against the ceiling · per-view
acceptance diagnostics · the hole map, saved (the stroke lane derives
from it later) · provenance channels for both runs · **the judging
artifact**: the spec's three-column sheet per head region — clay |
A0 render | A1 render — at the Director's zoom, plus full-figure flat
renders of both runs, plus the provenance panels. No verdicts.

### Then HALT

Stage: A2's arithmetic and decision, both crop twins + sidecars + their
gates, both stage-1 runs' numbers against the ceiling, the hole map, the
three-column sheets and flat renders. **To the advisor's eye first, then
the Director's** — his pre-stated questions: does the detail pass visibly
beat the baseline at his zoom (H3), and do the stage-1 numbers stand
against the ceiling. Strokes remain gated behind the sweep (thin_extent
lands at the stroke-lane ruling); nothing past the halt runs.

### Do not

Project the spec-source companion (its sidecar forbids it) · run any
stroke or texpass_brush step · decide thin_extent · exceed one bounded
re-roll per crop view · adopt A1 over A0 (the ruling adopts; you stage
both) · arm any bound · edit any fixture or profile · write to the memory
store · end a session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Both projection invocations recorded; the A2 rule registered before its number; crop frames from recorded derivations; harmonization operands recorded; predictions hashed blind first |
| ANDON_AUTHORITY | 3 | The reach-invariance check halts on any ceiling delta; the bake's ANDONs are the A2 expressibility halt; identity test before the transfer touches anything; both cloud guards per submission; the halt is eyes on evidence with A0 beside A1 |
| NAMED_COMPENSATORS | 3 | A1 runs on a fresh accumulating state so A0 is never consumed; raw twins and both runs retained; 0-credit expectation verified per submission; the atlas re-bake (if armed) is a new tree, the old bake retained |
| DECOMPOSE_BY_SECRETS | 3 | Capability (crop cameras) exercised under policy (head region, two yaws) decided by ruling; A2's allocation separated from A1's generation; the crop stems derive from the committed entry through the committed builder |
| UNCERTAINTY_GATED_HUMANS | 3 | H3's payoff is the Director's zoom on a pre-registered three-column sheet with the baseline beside it; A2 runs under a rule registered before measurement; both re-rolls bounded and pre-registered |
| EXTERNAL_VERIFIER | 2 | The ceiling instrument independently checks the projector's geometry; provenance channels audit both runs; the payoff is judged by the eye against the baseline. `skip:` per precedent |

### Calibration

The handoff-12 standard holds: pre-register the does-nothing band for
every new number, validate instruments by identity before use, own errors
in the report. Two route cautions: the crop projection is the arc's FIRST
— read the provenance channel before believing coverage moved, and the
three-column sheet is the deliverable his sentence rules on; and the
stage-1 numbers are born on-surface (the subject's off-surface rate is
2.6430% from birth — quote denominators).

---

### Standards compliance (handoff 2)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Every measurement lands beside its derivation JSON; the pair's workflow JSONs saved pre-submission with seeds and params; predictions hashed blind where checkable |
| ANDON_AUTHORITY | 2 | Prep-bake ANDONs pre-stated as halt-not-tune; the sweep's UNDECIDED report is the gate condition for future arms; the pair halt is the Director's fixture window; re-roll bounded at one |
| NAMED_COMPENSATORS | 2 | Cloud spend bounded to two generations (+ at most one re-roll each) with estimate_credits first; all writes in new files/dirs; the one prompts-file write is new; nothing irreversible beyond spend |
| DECOMPOSE_BY_SECRETS | 3 | Every subject value derives from this mesh or this fixture; the tuning constant (edge-ref) explicitly NOT re-derived; the backdrop word flows fixture → derivation → prompts file, never through code |
| UNCERTAINTY_GATED_HUMANS | 3 | The styled-pair halt is the Director's overrule window on the whole authored identity, advisor's eye first; suspended thresholds go to him as numerator/denominator, not invented bounds |
| EXTERNAL_VERIFIER | 2 | The ceiling instrument and the off-surface classifier check the bake from independent code paths; the pair is judged by eyes, not by the generator's own metrics. `skip:` on a second model for the geometry legs, per precedent |
