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

### Standards compliance (handoff 2)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Every measurement lands beside its derivation JSON; the pair's workflow JSONs saved pre-submission with seeds and params; predictions hashed blind where checkable |
| ANDON_AUTHORITY | 2 | Prep-bake ANDONs pre-stated as halt-not-tune; the sweep's UNDECIDED report is the gate condition for future arms; the pair halt is the Director's fixture window; re-roll bounded at one |
| NAMED_COMPENSATORS | 2 | Cloud spend bounded to two generations (+ at most one re-roll each) with estimate_credits first; all writes in new files/dirs; the one prompts-file write is new; nothing irreversible beyond spend |
| DECOMPOSE_BY_SECRETS | 3 | Every subject value derives from this mesh or this fixture; the tuning constant (edge-ref) explicitly NOT re-derived; the backdrop word flows fixture → derivation → prompts file, never through code |
| UNCERTAINTY_GATED_HUMANS | 3 | The styled-pair halt is the Director's overrule window on the whole authored identity, advisor's eye first; suspended thresholds go to him as numerator/denominator, not invented bounds |
| EXTERNAL_VERIFIER | 2 | The ceiling instrument and the off-surface classifier check the bake from independent code paths; the pair is judged by eyes, not by the generator's own metrics. `skip:` on a second model for the geometry legs, per precedent |
