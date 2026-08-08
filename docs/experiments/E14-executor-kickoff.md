# E14 — executor kickoff: the prop at Gate 0

**⚠ DEFERRED BY THE DIRECTOR'S SEQUENCING WORD (2026-08-07, hours after authoring —
supersedes this dispatch's launch and concurrency rulings):** *"Let's wait until the
database is developed before we move on to another profile, so that the data doesn't
accumulate too much. We'll fire the database kickoff once the beast profile is
complete."* This dispatch does NOT launch until, in order: **(1)** the beast profile
completes (E12/E13 Gate 1 ruled, its on-acceptance items landed), **(2)** the
context-architecture P1 index is built and verify-gated
([context-architecture.md](../context-architecture.md)). The clays stay staged; the
dispatch body below is unchanged and launches as written when its turn comes.

**⚡ BOTH CONDITIONS MET, 2026-08-07** ([E15-ruling.md](E15-ruling.md) Ruling 1):
the beast profile completed at E12 Ruling 28 (Gate 1 accepted; export and ingest
landed at Rulings 29–30), and the P1 index is built and verify-gated at two
seats' hands. **This dispatch is LAUNCHABLE on the Director's paste.** One line
joins the executor's first commands, per the E15 ritual:
`python tools/facet_index.py build` after `git pull`.

Paste this into a fresh executor session. Written by the advisor, 2026-08-07, at the
incoming seat's first fold, while the E12/E13 handoff-15 session runs the dragon's
strokes toward Gate 1. This dispatch is **Gate 0 only**: three longsword clays become
three measured meshes and three full-size sheets, and the Director designates. The
identity fixture (`canon/LONGSWORD-IDENTITY.md`), the prop profile (`profiles/prop.json`),
the register decision and the spec proper all follow designation — none of them is this
session's work.

**Class ruling, carried from the relief (2026-08-07):** the profile class is **`prop`** —
not "assets" (too generic), not "sword" (profiles name classes; fixtures name subjects:
character / ship / beast / prop). This is the route's fourth subject class.

**Concurrency ruling (advisor, this dispatch):** this session MAY run while the
handoff-15 stroke session is live. Grounds: TRELLIS's measured peak is 4.4–5.6 GB
against ~29 GB of current headroom under the watchdog; the stroke lane's generation is
cloud-side; the file lanes are disjoint. The guard: **touch nothing under
`E:\AI\training\facet_next\E13_stroke\`, `E13_stage1\`, or any handoff-15 report file**,
and if `git pull` or any commit meets the other lane mid-write (index lock, staged files
you did not stage), stop and report rather than improvise. The Director launches this
whenever he chooses; his word is the schedule.

---

## You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                <- how to work here. Read first, follow exactly.
README.md                                <- measured state of every tool
docs/experiments/E04-gate0-report.md     <- THE PRECEDENT RUN: environment findings,
                                            recipe, instrument discipline, sheet form.
docs/experiments/E12-gate0-report.md     <- the nearest-subject precedent: same runner,
                                            same sheet form, per-mesh frame derivation
                                            on a non-character subject.
docs/style-registers.md                  <- the class table; the prop row is UNDECIDED
                                            on purpose and stays that way this session.
E:\AI\training\facet_next\E04_gate0\recon.log   <- the exact recorded invocations
```

**Your rules** (CLAUDE.md, §"Rules for an executor session"): never judge whether output
is good · state a prediction before you look, and say whether it was blind · **stop at
every gate, never improvise past one** · do not write to the memory store · **a negative
result is a full success.**

## Where this stands

Two accepted assets exist (W3; the galleon at zero credits) and the beast is at its
Gate 1 halt in a concurrent session. **The prop arc is the fourth subject class**, and
the first whose dominant surface is a *near-2D thin slab at figure scale*: the E12
membranes were the subject's stressor; here the sheet **is** the subject. Also new:
high bilateral symmetry, hard planar facets (the gem pommel), and a helical fine
structure (the grip wrap). The E07 blade lessons — steel's chroma floor, grey-on-grey
keying, the blade band's dilation starvation — finally fight on home ground; those are
**texture-stage priors recorded for the spec, not Gate 0 work**.

Three clays are staged at
`E:\AI\training\facet_next\longsword_clay\longsword_clay_p1_{00001,00002,00003}_.png`
(staged 2026-08-07 by the advisor from `Downloads\comfy-export-2026-08-07-2c1adf8d.zip`;
byte counts 1,021,466 / 1,029,231 / 1,093,621 verified against the zip entries). The
advisor viewed all three at full size on 2026-08-07:

- **00001** — broad slab blade with a strong continuous central ridge; straight quillons
  with stepped, flared ends; rope-wrapped grip; faceted polyhedral gem pommel; nick
  marks along both edges; near-frontal presentation.
- **00002** — the slimmest blade of the three; quillons taper to soft down-swept flares;
  the tightest coil wrap; the smallest, roundest gem pommel; slight three-quarter
  presentation with visible depth toward the tip.
- **00003** — stepped ricasso shoulders giving the silhouette a double flare below the
  guard; curved quillons ending in points; the chunkiest faceted pommel; the heaviest
  nick scoring across the blade field; near-frontal presentation.

All three: a single object standing on its tip over a soft ground shadow, studio-grey
gradient backdrop, monochrome clay. All three read **taller than wide — expect portrait
frames, the route's first** (the character sat at 0.46–0.72 widest-horizontal/height; a
sword will sit far below that).

**This dispatch ranks nothing and neither do you.** Which sword is *the* sword is an
outcome call and it is the Director's. **Rejecting all three is a legitimate outcome.**

## Environment

- **Verify the watchdog before the GPU leg and report either way** — a status is a
  measurement, not a fact that survives the afternoon. Restart is standing
  authorization: `pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1`. **The
  ceiling is never raised.**
- **TRELLIS reconstruction runs LOCAL** — the standing exception to cloud-only
  generation; nothing in this dispatch generates. Runner:
  `E:\AI\sprite-foundry\3d-prerender\mesh_character.py`, recipe per the E04 precedent
  report §2 and `recon.log`: `--ptype 1024_cascade`, `HF_HOME=E:\AI-Models\hf-cache`,
  the `PYTHONPATH=E:\AI-Models\TRELLIS.2-repo` repair recorded in the runner. `run()`'s
  own signature default `seed=42` is the seed (the tool exposes no flag) — record it
  from the signature, and **record the backend that LOADED, not the one requested**
  (E04 measured `flash_attn` loading under `ATTN_BACKEND=sdpa`). Precedent cost:
  116–141 s and 4.4–5.6 GB peak VRAM per mesh.
- Blender through **PowerShell** · `--views=-30,0,30` argparse form · scripts create
  their own output directories · **prints are ASCII-only**.
- Output tree: `E:\AI\training\facet_next\E14_gate0\`.

## Predictions before numbers

Before `mesh_stats` returns anything, pre-state in the report (and say the status was
blind): expected **shell counts** against the measured family — character 40–191, ship
237–512 (free-floating rigging), beast 9–12 (thin structure attached) — a single rigid
object with a wrapped grip is the prior to bet on or against · expected **largest-shell
fraction** · the **blade's predicted reconstruction form** (closed thin slab per the
membrane precedent / thickened / holed) · **wrap-coil survival** (distinct coils vs a
fused cylinder) · watertightness. A wrong prediction is a full success; it is the
calibration the prop profile inherits.

## The task

1. **Reconstruct all three** → `longsword_00001_raw.glb`, `longsword_00002_raw.glb`,
   `longsword_00003_raw.glb`. Log per-mesh `cmd` / env / wall / peak VRAM / exit in the
   `recon.log` form. A non-zero exit is a report, not a retry with changed parameters.

2. **`mesh_stats.py` on each, with NO `--profile`, on purpose.** No `prop.json` exists;
   the loader's no-profile path is the byte-identity path, and every value measured this
   session is folded into `prop.json` by the advisor after designation. Quote: faces ·
   verts · shells welded and unwelded · largest-shell fraction · watertight · extents
   **with their axes named in the Blender convention** · widest-horizontal / height
   (expect well under 1). **Leave the face-rect columns unquoted** (density, curvature,
   `curv_radius`): the rect is W3's, authored against a humanoid — a sword has no face.
   If the tool prints its front-view-rect warning, quote the warning.

3. **Hilt-region evidence, per mesh — the allocation question's evidence, prop form.**
   E01 measured 3.1–4.5× polygons mattering on character faces; the ship ruled
   allocation NONE; the beast ruled NONE on its own head evidence; **no answer is
   inherited** — the decision is made in `prop.json` after designation, from what you
   measure here. The hilt (pommel + wrap + quillons) is this subject's detail-dense
   region against a large plain blade expanse. Per mesh:

   - Locate the hilt **by eye from the clay renders** and record the method and an
     axis-aligned crop box — coordinates plus **the frame they are in** (the same
     Blender-convention frame `mesh_stats` names its extents in). **Do not locate it by
     height**, even though a tip-standing sword happens to put the hilt at the top —
     the pose is the accident the raised-weapon rule warns about, worn upside down.
   - Report: faces inside the box / total (the share) · median face area inside vs
     outside (the density contrast) · and a **full-size hilt crop render per candidate**
     as its own file, `GATE0_hilt_0000N.png`.
   - **No verdict attached.** The numbers inform the designation and the profile
     decision that follows it; they do not argue for one here.

4. **Sheets — one per candidate, full size, never a contact sheet.**
   `gate0_sheet.py --concept <clay> --renders <dir> --stats <stats.json>` with eight
   `--clay` views (texture hides geometry; there is no texture here anyway). **The
   render frame is measured per mesh from its own bbox across its rendered yaws** — the
   worst yaw is contained by construction; an inherited frame is the accident class
   whether or not it happens to fit. Expect portrait on all three; edge-on yaws will
   render the blade as a sliver a few pixels wide — **that is the subject, not a
   defect**; report it, don't fix it. Round to generator-legal — **÷16 on both axes
   when neither is 1024** — and choose as if the frame will be kept (the ship's Gate 0
   frame became its twin frame). Record each frame and its derivation. Out:
   `GATE0_candidate_0000N.png`.

5. **HALT — and the report goes to the ADVISOR's eye, not the Director's.** Nothing
   reaches the Director's gate that the advisor has not looked at first. Stage: three
   sheets, three hilt crops, three stats JSONs, `recon.log`, and the report at
   `docs/experiments/E14-gate0-report.md`. The report ranks nothing, recommends
   nothing, and offers its observations as data with no verdict attached — the
   precedent reports' own form. The advisor looks, then presents. **The Director
   designates, or rejects all three; either is the gate working.**

## What to look at while you are there — priors, labeled (the S3 discipline)

These tell you where to LOOK in the report's observations, not what to tune.

- **The blade as a sheet** *(measured family prior: E07 at sash scale, E12 on the
  membranes)*: the family precedent is closed slabs that pinch, not sheets that hole.
  Report each blade's reconstructed form, apparent thickness on the renders (thickness
  vs shading is not decidable from a render — say so if it isn't), pinches, holes, and
  whether the central ridge survives as geometry.
- **Edge nicks and blade scoring** *(unread guess, labeled as one)*: report whether
  they reconstruct as geometry or vanish into surface.
- **The wrap coils** *(inferred — filament-adjacent; the ship's rigging lessons are
  the prior)*: distinct helical coils vs fusion into a cylinder; any detached shells.
- **The gem pommel facets** *(unread guess)*: hard planar facets with crisp edges —
  report whether the planes come back flat and the edges sharp, or rounded.
- **Quillon tips** *(inferred)*: pointed extremities — truncation, rounding, or
  detachment.
- **The tip contact and ground shadow** *(this subject's own)*: every clay stands ON
  its tip over a soft floor shadow. Report whether any floor or shadow-derived
  geometry reconstructs, and whether the tip returns free and pointed.
- **Bilateral symmetry** *(observational at Gate 0)*: report whether left/right
  quillons and blade edges read symmetric on the renders. No instrument is
  commissioned for it this session.

## What does NOT run, each with the reason

- **`gate_mesh.py`** — character-only; its head/shoulder logic is meaningless here,
  and the prop profile's absence-of-block will be a recorded decision after
  designation (ship precedent: `mesh_gate: none`).
- **No second reconstruction from a hilt crop.** E01's bust-crop move is the
  allocation lever; whether the prop gets it is the profile decision this Gate 0
  gathers evidence FOR. Spending it now would decide a live question by improvisation,
  on candidates that may be rejected.
- **No decimation, no UV, no atlas, no twins, no texture.** Gate 0 is the route's
  first stage and this dispatch forbids scaffolding past it.
- **No `thin_extent` derivation** — post-designation, on the designated mesh only,
  with the published cost curve. No inherited value transfers: the character's 0.03 is
  figure-derived, the ship's 0.01 filament-derived, the beast's 0.005 derived on the
  artifact criterion against wings — **a blade is none of those**.
- **No thresholds armed from character, ship or beast values** — palette bands, IoU
  halts, bbox tolerances are other subjects' data; derive per subject later or
  suspend.
- **No profile writes, no `prop.json` stub, no identity fixture, no register
  decision** — the advisor authors the fixture and profile from the designated mesh
  and clay; the register row is decided at designation day one, at the Director's
  word, per the style-registers table. The occupancy audit (the E12 Ruling 20c
  pattern) runs at fixture authoring, before any generation — day one, not after the
  third unnamed-surface catch.
- No memory-store writes · do not end a session the Director has not ended.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | `recon.log` per mesh (cmd, env, wall, peak VRAM, exit); seed recorded from the pipeline's own signature; backend recorded as what loaded; stats JSONs beside the sheets |
| ANDON_AUTHORITY | 2 | Watchdog verified before GPU work; non-zero exit halts rather than retunes; the designation halt is the gate; `mesh_stats`' own rect warning is quoted, not suppressed; the concurrency guard stops on any cross-lane collision |
| NAMED_COMPENSATORS | 2 | New files only, all under `E14_gate0/` and one new report in `docs/`; nothing pre-existing opened for writing; no publish, no spend, nothing irreversible in scope |
| DECOMPOSE_BY_SECRETS | 3 | Frames derived per mesh, never inherited; character-only columns excluded rather than quoted; subject evidence gathered for a profile that does not exist yet instead of leaking into code defaults; texture-stage steel priors recorded for the spec, not enacted at Gate 0 |
| UNCERTAINTY_GATED_HUMANS | 3 | The halt IS the designation gate: full-size sheets, hilt crops at zoom, the advisor's eye before the Director's, no ranking anywhere; the register decision is explicitly reserved to the Director at designation |
| EXTERNAL_VERIFIER | 2 | `mesh_stats` measures any mesh identically — the instrument that checked the E04 and E12 seats checks this one. Gate 0's verifier is the Director's eye on artifacts. `skip:` on a second model — deterministic geometry, per the Gate 0 precedent |

## Calibration

The E12 Gate-0 executor's discipline is the standard: implement the dispatch verbatim
rather than pre-softening it, halt with the artifacts already staged, surface
environment findings rather than passing over them, and check this dispatch's own
inherited numbers — the clay descriptions, the VRAM precedent, the shell ranges —
against source in the same breath you use them. A negative result, including three
meshes not worth designating, is a full success and is reported as one.

---

## Session handoff 2 (2026-08-07) — the DESIGNATED MESH's measurement pass. Ends at the styled-pair halt. Comprehensive.

Gate 0 is CLOSED by designation: **00001 is the longsword** (E14 Ruling 1, "00001
is my favorite"). The register is ruled day one (Ruling 5a: **ultra-realistic, no
LoRA** — his sentence). The fixture and profile are authored (Ruling 5b/5c). A
fresh executor session starts here:

```
cd E:\AI\facet && git pull
python tools/facet_index.py build       <- the E15 ritual: query the tip, not the last commit
CLAUDE.md                               <- how to work here. Read first, follow exactly.
docs/experiments/E14-ruling.md          <- Rulings 1-5. Ruling 4 is allocation; Ruling 3 is the hollow finding.
canon/LONGSWORD-IDENTITY.md             <- the five elements, the occupancy audit, the stressor table
profiles/prop.json                      <- every decided value; _still_suspended is YOUR list
docs/experiments/E14-gate0-report.md    <- the designated mesh's measured record
docs/experiments/E12-executor-kickoff.md   <- Session handoff 2 there is the METHOD PRECEDENT
                                            (the beast's measurement pass); this dispatch is
                                            its analogue and cites rather than restates
```

**The subject:** `E14_gate0/longsword_00001_raw.glb` — its Gate 0 numbers travel
with it (1 welded shell, zero boundary edges, 121 non-manifold edges with the wrap
as the pinch locus, hollow box-section blade, frame 240×1024 height-fit). The
softer pommel apex and lumpier wrap are **designated-in** (Ruling 1): known subject
facts, not defects to fix.

**Your rules and environment are unchanged** (CLAUDE.md §executor; watchdog
verified before any GPU leg, report either way; generation cloud-only with
`estimate_credits` per submission; ASCII prints; explicit git paths; output
`E:\AI\training\facet_next\E14_prep\`). Blind predictions first, hashed, blind
status disclosed — per task below.

### Task 1 — the sweep

Registry sweep + coverage pass against `profiles/prop.json`. Report the UNDECIDED
set with every member dispositioned (lands-in-this-dispatch /
lifecycle-blocked / finding-for-the-ruling). **Expected members, pre-stated**:
`texpass_iter.thin-extent` (deliberate — its curve is Task 2, its value is a later
ruling), `restylize_views.canny-low`/`canny-high` (deliberate — the per-subject
derivation is Task 3, the 10c/11a law), and whatever the sweep finds that this
draft missed, which is the sweep doing its job. The `_NOT_CLEARED` brush marker
and the `_not_on_route` forms count DECIDED (the recognized forms). **0 UNDECIDED
gates ARMS, not this dispatch** — your exit condition is the report.

### Task 2 — measure the suspended values from the designated mesh

1. **Prep bake** at the profile's operating points (head-scale 1.0, res 4096).
   PRE-STATED READING: the bake's ANDONs were written for characters; if one fires
   on this mesh it is an expressibility limit — report and HALT, do not tune.
2. **The reach ceiling, pre-registered before any projection** — `e08_ceiling` at
   the profile's floors on the eight eye-level cameras (quote Ruling 6e's caption
   caveat beside any output of that tool — its repair is still in the errand
   batch). Report reach/valid with both operands. **Also classify the bake's
   `pos.npy` off-surface rate** (`e12_offsurface`, the validated instrument,
   report-only): the rate has replicated 2.50–2.64% across three subjects; a
   fourth point tests the bake-artifact-class reading either way.
3. **`thin_extent`, measured fresh** — the full cost curve (fraction of visible
   figure withheld per candidate value), and **separately: what fraction of the
   BLADE each candidate withholds** — the blade is this subject's membrane-analog
   and its whole point. The box-section caveat is in the profile's suspension
   note: the probe reads outer-to-outer (~0.021), not walls. No gate arms on any
   of it; the value is decided at its own ruling.
4. **The elevated-camera question, measured** — up-facing surface (normal_z >
   0.5, area not face count) first-hit coverage per candidate set, greedy by
   marginal gain, **ray density quoted** (the 7b law). The prior to bet on or
   against is in `cameras.elevated`: the z-max slab measured 0.10% of surface at
   Gate 0, so NONE is likely — and the beast's lesson is that this class has no
   working prior until measured.
5. **The mirror check, cheap and new** — this subject is bilaterally symmetric:
   report per-view silhouette areas across the eight (the E12 9b/16f caveats
   predict near-equality within AND across mirror pairs here). One table; any
   instrument that later normalises by view area inherits it.

### Task 3 — the two derivations, in order

1. **The canny pair, derived per subject** (the 10c/11a law — the accepted
   route's 0.4/0.8 was falsified on grey-on-grey clay, and this clay is the same
   class): the rung ladder on the designated clay's own renders, **works-perfectly
   test FIRST** (what does the lower pair admit that is NOT relief — the beast's
   ladder found wandering iso-luminance contours in flat fields at the bottom
   rungs; this subject's flat fields are the blade faces). Report control px per
   rung per view with crops. **The pair is proposed with the evidence and RULED
   by the advisor before any generation consumes it** — the beast's executor
   halted exactly there and was right to.
2. **The backdrop derivation** (the S3 method): maximise the minimum distance
   from every declared material, saturated optima disqualified, weighted toward
   L1 — **S-steel holds the risk: the result cannot be any grey**, and the
   fixture's blue-violet-unoccupied expectation is CHECKED at derivation, not
   assumed (the 8a/15i lesson). Report the optimum table; **the WORD is chosen
   at the ruling**, never by the metric alone.

### Task 4 — the styled target pair, after the two rulings land

Twin-prompts file built by the committed builder from the fixture + the ruled
backdrop word (the one-string-vs-per-view check runs against the actual renders
at build time — this subject may be the first since the ship to pass the
one-string premise; verify, don't import). Controls from PROFILE-rendered clay
views (never Gate 0 renders — the 4a law). **Views 0 and 1** (face-on carries
all five elements; the three-quarter adds depth cues; on a bilaterally symmetric
subject the rear family mirrors the front and buys no identity — state the check
that confirmed it). Full cloud discipline, `estimate_credits`, one generation
per view, one bounded re-roll each, the no-LoRA pre-flight on every submission.
**HALT with the pair staged: the advisor's eye first, then the Director beside
the clay** — his fixture overrule window made visual, the register's first test
on steel.

### Do not

Generate before Task 3's two rulings land (the halt after Task 3 is a REAL halt
— the advisor rules the canny pair and the backdrop word, then Task 4 runs) ·
run any measured arm locally (TRELLIS excepted, none needed here) · touch
thin-extent's value or arm any gate on Task 2's curves · edit any fixture or
profile · write to the memory store · end a session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Every measurement lands beside its derivation JSON; predictions hashed blind where checkable; the pair's workflows saved pre-submission with seeds and params |
| ANDON_AUTHORITY | 3 | Prep-bake ANDONs pre-stated as halt-not-tune; the sweep's UNDECIDED report is the gate condition for future arms; TWO mid-dispatch halts to the advisor (canny pair, backdrop word) before any credit-bearing step; the pair halt is the Director's window |
| NAMED_COMPENSATORS | 2 | Cloud spend bounded to two generations (+ at most one re-roll each) with estimate_credits first; all writes in new files/dirs under E14_prep; nothing irreversible beyond spend |
| DECOMPOSE_BY_SECRETS | 3 | Every subject value derives from this mesh or this fixture; the tuning constant (edge-ref) explicitly NOT re-derived; the backdrop word flows fixture → derivation → ruling → prompts file, never through code |
| UNCERTAINTY_GATED_HUMANS | 3 | The styled-pair halt is the Director's overrule window on the whole authored identity, advisor's eye first; both derivations go to rulings as evidence, not as decisions |
| EXTERNAL_VERIFIER | 2 | The ceiling instrument and the off-surface classifier check the bake from independent code paths; the pair is judged by eyes, not by the generator's metrics. `skip:` on a second model for the geometry legs, per precedent |

### Calibration

The handoff-16 and E14-Gate-0 standard holds. Named risks: **S-steel is live at
every step** — the clay is grey-on-grey (the canny ladder's home case), the
backdrop derivation must escape grey entirely, and at generation the register's
realism prior meets near-achromatic steel for the first time (pre-register what
a register drift would look like on metal before the pair runs). The hilt at ~7%
of frame pixels is S-hilt-scale — if the pair's hilt reads soft, that is the
E12 head physics arriving on schedule, recorded not tuned. And the mirror facts
mean view-pair comparisons are cheap corroboration everywhere — use them.

---

## Session handoff 3 (2026-08-07) — the palette bands and the twin set. TWO advisor halts. Comprehensive.

**Authorised by [E14-ruling.md](E14-ruling.md) Ruling 16** — the pair is
ACCEPTED (the Director: "I agree with view 0 being the best. I love it. You
have my acceptance."), the recipe anchor is converted, and the route proceeds:
**bands → twins → stage 1**. This dispatch is the bands and the twins; stage 1
is the NEXT dispatch, after the twin-set ruling. A fresh executor session
starts here:

```
cd E:\AI\facet && git pull
python tools/facet_index.py build        <- the E15 ritual: query the tip
CLAUDE.md                                <- read first, follow exactly
docs/experiments/E14-ruling.md           <- Rulings 1-16. 6/7 are your ruled values; 12-16 are
                                            the pair record, the rings term, the realised-value
                                            corrections, and your authorisation (16b)
canon/LONGSWORD-IDENTITY.md              <- the fixture: L3 now carries TWO terms (Ruling 13)
profiles/prop.json                       <- every decided value; the prompt entry is the LIVE
                                            v2 source; generation_recipe_anchor is the anchor
docs/experiments/E14-task4-report.md     <- the pair's record: realised values in section 6
docs/experiments/E14-task4-pair-sidecar.md
docs/experiments/E12-executor-kickoff.md <- handoff 8 there is the METHOD PRECEDENT (the
                                            beast's twins); this dispatch cites, not restates
```

**Your rules and environment are unchanged** (CLAUDE.md §executor). Generation
cloud-only, `estimate_credits` per submission, graphs saved to disk and
pre-flighted before submission, the inverted no-LoRA pre-flight on every
graph. No local GPU leg is expected (the renders, masks and controls exist);
if any Blender invocation becomes necessary, the watchdog is verified before
it, reported either way. Output: `E:\AI\training\facet_next\E14_prep\bands\`
and `E14_prep\twins\`. ASCII prints. **Blind predictions first, committed
before any derivation runs, blind status disclosed** — they must cover at
minimum: the wine-merge question, where the gate's chroma floor lands
relative to L1's realised 5.39 cast, the backdrop band's position, the twins'
per-view IoU spread, the view-1-at-770700 outcome, and the gold-watch firing
count.

### Task 1 — the palette bands, derived and VALIDATED, then HALT for the ruling

Derive the off-palette gate's bands **from the fixture's named materials,
cross-checked against the ACCEPTED PAIR — never against the twins they will
gate** (non-circularity, kept from the galleon). The realised values are in
the room (task4 report §6): use the PAIR's measured colours, not the
superseded estimates file.

Pre-registered structure, from the profile's suspension note and the fixture
— verify each against the pair rather than assuming:

1. **L1 steel and L2 iron carry NO hue bands, by design** — they sit below
   any honest chroma floor and separate by VALUE; the achromatic channel
   (E12 17d's permanent member) is their instrument. **The floor itself is
   derived from the separation structure of the pair's realised values —
   never chosen to put L1's 5.39 cast on either side of it.** Where the
   floor lands relative to that cast is a RESULT, reported with the
   derivation (the beast's realised backdrop sat under its gate's floor and
   was hue-neutral under the gate's own rule — the 15i mechanism; this
   subject's answer is measured, not inherited).
2. **The band candidates**: gold (warm, ~L3's measured 83.5) and the wine
   family (oxblood 25.4 + garnet 24.3 — likely ONE merged band, the
   D4/D5/D10 precedent; report both merged and split forms with the
   between-band density so the ruling can see whether a cut exists — never
   claim a gap without plotting the density between).
3. **The backdrop band is NEW TERRITORY on this subject**: the realised
   backdrop is hue ~305 at C\* 32.6–37.1 — far ABOVE any floor, so unlike
   the beast's it is NOT hue-neutral, and its band is carved deliberately.
   Its proximity to L1's realised cast (~295, ten degrees away) is the
   derivation's hardest question: report the density between 290 and 310 on
   the pair's figure pixels vs backdrop pixels before proposing any
   boundary.
4. **The dark-rows caveat (15j) bites on blackened iron exactly as it bit on
   charcoal** — dark bands are colour-matches to shadow; colour-not-placement
   rides beside the bands in the profile block when they land.
5. **Every bound obeys the perimeter law** (normalise boundary quantities by
   perimeter, not area) **and the two-thresholds law** (report total AND
   largest connected component).

**Validation before proposal** (the S3 discipline — validate against known
artifacts): the gate as drafted must (a) PASS both accepted pair views, (b)
be run on the REJECTED 770700 artifact and its behaviour REPORTED — note the
rejection was occupancy (gold on the wrong surface), which colour-not-
placement cannot see; whether the gate fires on it for any other reason is
data about the gate, stated plainly either way. **HALT 1: the derivation, the
density plots, the validation table and a proposed band set go to the
advisor. The bands and the gate's disposition (armed with bounded re-roll
authority vs report-only, per band) are RULED before any twin generates.**

### Task 2 — the twin set, after the bands ruling lands

1. **Stems v2 by the committed builder** — it reads the profile's LIVE prompt
   entry (Ruling 13's rings term included) and re-verifies the one-string
   drop against the renders:
   `e12_make_twin_prompts.py --profile profiles/prop.json --tag swordclay
   --drop "a gold diamond boss at the crossing:2,6" --version 2`.
   Views 0–7; expect FULL stems everywhere except 2/6 (one drop); the rings
   term drops nowhere (visible on all eight — verified at Task 4).
2. **Controls**: re-emit through the profile (`--emit-only`) and verify the
   canny counts against the anchor row — 8,695 / 8,230 / 5,580 / 8,400 /
   9,509 / 8,508 / 5,230 / 7,870. Any drift is a HALT, not a re-derivation.
3. **Eight twins at the pair-anchored recipe** — profile values, seed 770700
   per view, one generation per view. **One bounded re-roll per failing
   view** (new seed, +1 per attempt), where "failing" means: a ruled-armed
   band fires, or a pre-registered fixture rule is violated by eye (the
   occupancy class — the pair's own precedent). The rejected artifact stays
   in the record with its measurement, and a second failure on any view is
   the RESULT, not a third roll.
4. **Pre-registered watches, judged by eye at 4× hilt crops per twin**: the
   12e gold-family-pressure watch (gold on ANY surface outside L3's boss +
   rings is the signature; the rejected 770700 is its recorded example) ·
   view 1 at 770700 is the measured-risk view (same seed that sprawled on
   the pair; the stems have since gained the rings term — either outcome is
   one data point on whether naming the rings redirects the pressure,
   recorded not tuned) · L5's gem-hue drift (garnet vs magenta — the pair's
   internal drift, watched per twin).
5. **Per-view registration diagnostics** with the halts suspended as the
   profile expresses (reg-iou-min 0.0, bbox-tol 9.99): IoU per view against
   the exact raycast silhouette, computed and printed; the across-pair area
   swing is 2.061× on this subject (Ruling 10c) — any per-view-area
   normalisation inherits it; report absolute px counts beside any ratio.
   This subject derives its own IoU bound from its own twins' spread at the
   ruling, or keeps reporting — never inherits W3's 0.80.
6. **Sheets**: per twin, full size — render | control | twin — plus the 4×
   hilt crop. Never a contact sheet alone.

**HALT 2: the twin set staged** — eight twins (plus any bounded re-rolls,
rejected artifacts preserved), the registration table, the gate results per
the ruling's disposition, the watch findings, and the sheets. **The advisor's
eye first, then the Director.** The twin-set ruling decides: twin acceptance,
any subject-derived IoU bound, and dispatches stage 1 against the
pre-registered 51.33% ceiling.

### Do not

Generate any twin before HALT 1's bands ruling lands · arm any threshold the
ruling has not armed · re-choose the backdrop word or canny pair on anything
a twin shows (both RULED; twins are not the pair's judges) · project anything
(stage 1 is the next dispatch) · touch `thin_extent`'s value, the head-rect
arm, or the activated state (parked, 16c) · edit any fixture or profile (the
gold watch and gem drift are REPORTED; the fixture is the advisor's) · write
to the memory store · end a session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Stems versioned (v2) with the builder re-run recorded; the canny anchor row is a byte-level pre-flight; every twin's graph saved pre-submission with prompt_id + seed; band derivation lands in JSON beside its density plots |
| ANDON_AUTHORITY | 3 | TWO advisor halts (the bands ruling before any generation; the twin set before any projection); canny-count drift halts; the bounded re-roll rule is the only re-generation authority and a second failure is the result |
| NAMED_COMPENSATORS | 2 | Cloud spend bounded to 8 generations + at most 8 bounded re-rolls, estimate_credits each (expected 0 on the OSS graph — quote anyway); all writes in new files under E14_prep/bands and E14_prep/twins; rejected artifacts preserved, never deleted |
| DECOMPOSE_BY_SECRETS | 3 | Bands derive from fixture materials × the accepted pair, never the twins they gate; the floor derived from separation structure, never from where L1's cast falls; stems carry identity through the profile's live entry, never retyped |
| UNCERTAINTY_GATED_HUMANS | 3 | The bands' disposition (armed vs report-only, per band) is the advisor's ruling with density plots in the room; twin acceptance and any derived IoU bound are the twin-set ruling's; the gold watch and gem drift go up as findings |
| EXTERNAL_VERIFIER | 2 | The gate is validated against artifacts it did not derive from (the pair) and exercised on a known-rejected artifact before ruling; registration is measured against the raycast silhouette, an independent code path from the generator; `skip:` on a second model for the derivation legs, per precedent |

### Calibration

The Task-4 standard holds — verify inherited claims against source in the
same breath you use them (the last two dispatches' carried flags each broke
half-wrong). Named risks: **the 295-vs-305 proximity** (L1's realised cast
ten degrees from the realised backdrop hue) is the bands derivation's hardest
cut and may honestly have no clean boundary — a suspension with the density
plotted is a full success; **the gold watch** is live on every twin; and the
mirror-pair facts make view-pair comparisons cheap corroboration on all
eight — use them.

---

## Session handoff 4 (2026-08-07) — the diagonal re-roll pass. Four submissions, one branch each. Ends at the set's halt.

**Authorised by [E14-ruling.md](E14-ruling.md) Ruling 18** — the twin-set
ruling at HALT 2. The Director has seen the first-roll set; the gold pattern
is ruled SEED-CONDITIONAL on the pair's own evidence (770700 convicted on a
diagonal by the pair's rejected roll; 770701 cleared on the same view by its
accepted re-roll), and the eye clause's bounded re-roll authority applies to
the four diagonals. This dispatch is surgical: **four submissions, nothing
else generates.** A fresh executor session starts here:

```
cd E:\AI\facet && git pull
python tools/facet_index.py build          <- the E15 ritual
CLAUDE.md                                  <- read first, follow exactly
docs/experiments/E14-ruling.md             <- Rulings 17-18 are your authorisation and
                                              your branch conditions. Read both fully.
docs/experiments/E14-handoff3-task1-report.md   <- the bands (RULED per Ruling 17)
docs/experiments/E14-task4-report.md            <- the pair's seed evidence (section 4)
canon/E14-longsword-palette.json           <- the gate config: admitted rim band,
                                              report-only, deep-share standing
profiles/prop.json                         <- every decided value; nothing here changes
```

**Your rules and environment are unchanged** (CLAUDE.md §executor; cloud-only;
`estimate_credits` per submission, quote the 0-credit expectation either way;
graphs saved to disk and pre-flighted before submission; the inverted no-LoRA
pre-flight on all four; ASCII prints). No local GPU leg is expected — the
controls, masks and stems all exist and none regenerates. **Blind predictions
first, committed before any submission**: per-diagonal sprawl outcome at
770701, the IoU range the re-rolls land in, deep-share behaviour, and the gem.

### The task

1. **Re-roll views 1, 3, 5, 7 at seed 770701** — stems v2 unchanged, controls
   unchanged (verify the canny anchor row byte-identical before submitting;
   drift is a HALT), recipe otherwise the profile's. One generation per view,
   saved and pre-flighted first, `estimate_credits` each.
2. **File discipline**: the four gold first-rolls are REJECTED artifacts under
   Ruling 18b — rename to `REJECTED_TWIN_swordclay_N_seed770700.png` beside
   the v2/v6 precedent; the new rolls become `TWIN_swordclay_N.png`. Nothing
   is deleted.
3. **Measure the finished set exactly as Task 2 did**: registration IoU + bbox
   per the purpose-built tool on the four new twins; the gate report-only in
   the admitted configuration with the deep-share diagnostic; the gold watch
   QUANTIFIED per view (the 93–96% metric re-run — its landing on the re-rolls
   is the dispatch's central number); the L5 gem watch; full-size sheets, 4×
   hilt crops, and the final-set strip rebuilt (the one the Director saw was
   first-roll era; the rebuilt strip is what goes up).
4. **The branch, pre-stated — one of two exits, no third**:
   - **All four land iron** → the set completes: seven accepted twins
     (0, 1, 3, 4, 5, 6, 7) with view 2 EXCLUDED per Ruling 18c. HALT with
     the set staged for the advisor's eye, then the Director's.
   - **ANY diagonal sprawls gold again at 770701** → **THE RESULT. HALT
     IMMEDIATELY** — no further submissions on any view, not 770702, nothing.
     Report what landed and what sprawled with the quantified watch; the
     recipe/fixture question goes to the ruling with systematic evidence in
     hand. A second failure is the result, exactly as view 2's was.

### Do not

Re-roll views 0, 2, 4, or 6 (0/4 accepted; 6's re-roll accepted; 2 is the
recorded result, excluded per 18c) · submit anything beyond the four · arm
any gate or derive any IoU bound (the bound derives at the set's acceptance,
not here) · project anything · edit any fixture, profile, or the palette ·
write to the memory store · end a session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Four graphs saved pre-submission with prompt_id + seed; the anchor-row byte check before anything submits; every measurement lands in JSON beside its artifact; rejected artifacts renamed, never deleted |
| ANDON_AUTHORITY | 3 | The branch is binary and pre-stated: any sprawl at 770701 halts the dispatch cold with no third roll anywhere — the second failure IS the result, the v2 precedent applied set-wide |
| NAMED_COMPENSATORS | 3 | Spend bounded to exactly four submissions at expected 0 credits, quoted each; new files only; nothing irreversible beyond GPU time |
| DECOMPOSE_BY_SECRETS | 3 | Nothing re-derives: stems, controls, bands, recipe all stand as ruled; the single variable is the seed, and it moves to a value the pair's own accepted artifact proved |
| UNCERTAINTY_GATED_HUMANS | 3 | Both exits end at a human gate: the completed set to the advisor's eye then the Director's, or the sprawl evidence to a ruling; no disposition is made here |
| EXTERNAL_VERIFIER | 2 | The registration tool and the gate check the generator from independent code paths; the gold watch is the quantified check on the ruling's own seed hypothesis — if 18b is wrong, this dispatch is what proves it. `skip:` on a second model, per precedent |

### Calibration

One variable moves. The dispatch exists to test Ruling 18b's seed hypothesis
against four fresh diagonals, and **a sprawl at 770701 is not a failed
dispatch — it is the measurement succeeding at falsifying the ruling**, which
is worth more than a lucky pass. Say which happened plainly. The gold watch's
per-view numbers are the evidence either way; the eye confirms at the 4×
crops. Zero credits expected; quote it anyway.

---

## Session handoff 5 (2026-08-07) — STAGE 1: the twins project. Ends at the stage-1 halt.

**⚠ AMENDED BEFORE LAUNCH (2026-08-08, [Ruling 20](E14-ruling.md)) — SIX
twins, not seven.** The Director's eye caught what Ruling 19 missed: view
6's re-roll carries a face-bearing mass at the crossing (the v2
death's-head's sibling) and is EXCLUDED on identity. Everywhere this
dispatch says seven, read SIX: **views 0 and 4 at 770700; views 1/3/5/7 at
770701; views 2 AND 6 excluded** (Rulings 18c and 20a). The projection view
list is `0,1,3,4,5,7`. The ceiling leg pre-registers the **SIX-camera**
reach, quoting the eight-camera 51.33% as the route-comparable and both
excluded cameras' marginals (~2.8 and ~4.4 points) as the labelled delta.
Any sheet or strip you build labels excluded artifacts AS EXCLUDED, in the
image (Ruling 20d's standing practice).

**Authorised by [E14-ruling.md](E14-ruling.md) Ruling 19f as amended by
Ruling 20c.** Everything projects at the profile's ruled values; nothing
generates, nothing spends. A fresh executor session starts here:

```
cd E:\AI\facet && git pull
python tools/facet_index.py build          <- the E15 ritual
CLAUDE.md                                  <- read first, follow exactly
docs/experiments/E14-ruling.md             <- Rulings 17-19. 19f is your authorisation;
                                              19b's gem readout and 19e's bbox law are yours
profiles/prop.json                         <- project_twins' ruled values; the framing family
docs/experiments/E14-handoff4-report.md    <- the set's record and the seed split
docs/experiments/E12-executor-kickoff.md   <- the beast's stage-1 handoff is the METHOD
                                              PRECEDENT; cite, don't restate
```

**Your rules and environment are unchanged** (CLAUDE.md §executor). No
generation, no credits; projection and measurement are local CPU. If any
Blender leg becomes necessary, the watchdog is verified before it, reported
either way. Output: `E:\AI\training\facet_next\E14_prep\stage1\`. **Blind
predictions first, committed before the ceiling runs**: the seven-camera
ceiling's landing relative to 51.33%, styled/valid, the gem region's blended
composition, per-view acceptance ordering.

### The task, in pinned order

1. **Pre-register the SEVEN-camera reach ceiling BEFORE any projection** (the
   moving-denominator law): first-hit reach at the profile's floors over
   cameras 0/45/135/180/225/270/315 — the shipped `e08_ceiling` if it takes a
   camera list, else `e14_atlas_anatomy`'s reachability path (it reproduced
   N8 exactly; state which ran). Ray bias stays the shipped default for
   comparability, with Ruling 10b's caveat quoted beside the number. Report
   it WITH the eight-camera 51.33% (the route-comparable) and the delta.
2. **Project the seven twins** through `project_twins.py` at the profile's
   ruled values, views pinned per-invocation to `0,1,3,4,5,6,7` (the
   explicit-deviation line printed — the profile's views key stays the
   render/mask consumers'). Per-view registration diagnostics print as they
   run; the A3 invariant's per-structure erosion reporting stays on.
3. **The stage-1 report**: styled/valid against BOTH ceilings (the E12 24e
   form — banked, not gated); the on-surface family per Ruling 9 (island
   count 46,496 and erode-2 residue beside any off-surface rate); per-view
   marginal contributions in turnaround order; dilation and edge diagnostics
   per the route's standard; **the GEM-REGION READOUT** (Ruling 19b: the gem
   texels' post-projection hue composition — garnet vs drifted shares, with
   an atlas-space crop and a rendered crop for the eye); the deep-share
   diagnostic's atlas-side analogue if the tooling permits, else stated as
   not-run.
4. **Sheets**: the atlas under FLAT light (the Workbench-STUDIO trap is the
   founding lesson); reference | rendered-asset panels at views 0, 1 and 6;
   the gem crop at 4×. Full size, never a contact sheet alone.
5. **HALT — stage 1 staged** for the advisor's eye, then the Director's.
   **No pass condition exists**: the ceilings are comparables, the eye is
   the gate.

### Do not

Generate anything · re-roll anything · include view 2's twin in any
projection input (its camera may still appear in reach arithmetic as the
excluded delta, labelled) · arm any gate or derive any bound · run strokes,
finalize, or touch `thin_extent`'s value (stage 2's, still deferred) · edit
any fixture, profile, or the palette · write to the memory store · end a
session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | The ceiling pre-registered before projection in its own commit; every invocation logged with its printed diagnostics; the seven-view list an explicit per-invocation argument, never a profile edit |
| ANDON_AUTHORITY | 3 | The stage-1 halt is the gate; the A3 invariant and bbox diagnostics print live; any tool ANDON is a halt-not-tune per standing rule |
| NAMED_COMPENSATORS | 3 | No spend, no generation; new files only under E14_prep/stage1; projection is repeatable from committed inputs |
| DECOMPOSE_BY_SECRETS | 3 | The denominator derived for THIS run's camera set rather than inherited from the eight-camera number; per-view contributions reported so no aggregate hides a view's failure |
| UNCERTAINTY_GATED_HUMANS | 3 | No pass condition invented — the E12 24e form; the gem readout goes to the eye with crops; the halt is the advisor's then the Director's |
| EXTERNAL_VERIFIER | 2 | The ceiling and the projector compute reach on independent code paths (their N8 agreement is on record); the gem readout uses the band instruments, not the projector's own numbers. `skip:` on a second model, per precedent |

### Calibration

The route's first prop projection. Named risks: the blade's thin strata are
where erosion physics bite (the A3 invariant reports per structure — read
it); view 2's absence will show as a reach hole at yaw 90 (expected,
priced at ~2.8 points, labelled not discovered); the gem region is SMALL —
if the readout's denominators are tiny, say so plainly rather than quoting
ratios alone (the D8 lesson lives here too). The 51.33% is the comparable,
not the target: a stage-1 number is what it is, and the beast banked 87.5%
of ITS ceiling on the way to acceptance.

---

## Session handoff 6 (2026-08-08) — the COMPLIANT re-projection: six twins. Surgical.

**Authorised by [E14-ruling.md](E14-ruling.md) Ruling 21c.** The seven-twin
stage-1 run (handoff 5) launched before Ruling 20's amendment and is the
measured COMPARISON; the banked A0 must be the RULED set — **six twins,
view 6's face-dome paint out**. Local CPU only; no generation, no credits.
A fresh executor session starts here:

```
cd E:\AI\facet && git pull
python tools/facet_index.py build          <- the E15 ritual
CLAUDE.md                                  <- read first, follow exactly
docs/experiments/E14-ruling.md             <- Rulings 20-21; 21c is your authorisation
docs/experiments/E14-handoff5-report.md    <- the seven-run you are diffing against
```

**Blind predictions first** (the six-camera ceiling's landing; v6's exact
exclusive cost; the crossing's styled % without v6; the diff's largest
region). Then in pinned order:

1. **Pre-register the SIX-camera ceiling** (cameras 0/45/135/180/225/315)
   through the anatomy path, after reproducing the seven-run's 1,877,487
   anchor. Quote all three: N6, N7, the 51.33% route-comparable. **N7 − N6
   is v6's exact exclusive price** — Ruling 21b's correction of 20c's ~4.4,
   measured.
2. **Project the six twins** (`--view` × 6, view 6's twin NOT an input),
   same profile values, out to `stage1/stage1b_atlas.png` — a NEW file; the
   seven-run atlas is a record and is not overwritten.
3. **Re-run the readouts**: coverage vs all three ceilings; the gem readout
   (the stone's numbers shift with v6's texels gone — 19b's readout re-run
   verbatim); the crossing census; the brush-territory sizing.
4. **THE DIFF**: per-texel ownership diff seven-run vs six-run — where did
   v6's 145,185 committed texels go (re-owned by which views vs newly
   unstyled), and the crossing's before/after at 4× with the change stated
   in plain words. This characterises exactly what the excluded artifact
   was contributing.
5. **Sheets**: the walk set — reference | asset | provenance per view, the
   gem at 6×, the crossing at 4× — **excluded artifacts labelled AS
   EXCLUDED in-image** (Ruling 20d). HALT with stage 1b staged for the
   advisor's sheet-walk, then the Director.

**Do not**: generate · re-roll · include view 2 or view 6 in any projection
input · overwrite any seven-run artifact · arm any gate · run strokes or
finalize · edit fixtures, profiles, or the palette · write to the memory
store · end a session the Director has not ended.

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | The ceiling pre-registered in its own commit before projection; new files only; the diff lands beside both atlases |
| ANDON_AUTHORITY | 3 | The halt is the gate; the anchor reproduction before any new number |
| NAMED_COMPENSATORS | 3 | No spend; nothing overwritten; the seven-run preserved as the comparison |
| DECOMPOSE_BY_SECRETS | 3 | The six-camera denominator derived for this set; v6's price measured, not inherited from a ladder column |
| UNCERTAINTY_GATED_HUMANS | 3 | No pass condition; the gem re-readout and crossing diff go to eyes |
| EXTERNAL_VERIFIER | 2 | Anchor reproduction against the seven-run's three-path number; the diff is its own check — ownership must repartition exactly. `skip:` on a second model, per precedent |

Calibration: one input leaves; everything else is pinned. The finding to
report plainly is what v6 was actually worth — its exclusive texels, the
crossing's drop, and where the brush's territory grew.

---

## Session handoff 7 (2026-08-08) — the STROKE LANE. Two advisor halts. Ends with the stroked asset staged.

**Authorised by [E14-ruling.md](E14-ruling.md) Ruling 23** — the Director's
gem word is GARNET (the fixture holds; the stone's drifted colour is stroke
territory), and the ship's `_NOT_CLEARED` lifecycle opens for its third
subject: nothing in `texpass_brush`'s block carries a value until HALT 1's
stroke-lane ruling. A fresh executor session starts here:

```
cd E:\AI\facet && git pull
python tools/facet_index.py build          <- the E15 ritual
CLAUDE.md                                  <- read first, follow exactly
docs/experiments/E14-ruling.md             <- Rulings 17-23. 23b is your authorisation;
                                              20b is the misbinding hazard you carry
canon/LONGSWORD-IDENTITY.md                <- L5 GARNET HOLDS - the identity you paint toward
profiles/prop.json                         <- texpass_brush is _NOT_CLEARED until HALT 1;
                                              texpass_iter's thin-extent is decided AT HALT 1
docs/experiments/E14-handoff6-report.md    <- the banked A0 and the hole map's shape
E14_prep/stage1/stage1b_holes_by_structure.json + stage1b_followups.json
docs/experiments/E12-executor-kickoff.md   <- the beast's stroke lane is the METHOD
                                              PRECEDENT; cite, don't restate
```

**Your rules and environment are unchanged** (CLAUDE.md §executor).
Generation cloud-only through `brush_cloud_step.py` (binds NO profile — its
agreement with the ruled recipe is BY VALUE, re-verified per stroke; the
no-LoRA graph path since E13, the inverted pre-flight on every submission);
`estimate_credits` per submission, quoted either way; the invariance ANDON
lives IN the tool and no shell chain gates a commit (E08 A32; Ruling 21g).
Output: `E:\AI\training\facet_next\E14_strokes\`. **Blind predictions
first, committed before the derivation runs.**

### Task 1 — derive the stroke lane from the hole map, then HALT 1

From `stage1b`'s hole map and the banked territory (5.76 points +
the garnet repaint), derive and PROPOSE — adopt nothing:

1. **The stroke set**: candidate strokes covering, at minimum — the blade's
   edge-on centreline ribbon (both faces of it), the unclosed v5/v7 guard
   seam and crossing holes, and **the garnet repaint** (the stone's
   drifted territory — the one stroke class painting OVER styled texels;
   its mask derives from the 19b readout's drifted-ownership partition,
   printed). Per stroke: the hole/target mask, the camera (yaw/el from the
   job key, per-stroke), the crop frame (generator-legal ÷16), and the
   spiral order FROM ALREADY-PAINTED REGIONS — the composes-a-new-character
   law is the reason and is cited on the ordering itself.
2. **The stroke prompts**: derived from the fixture per stroke (the stems
   name what the stroke's frame contains — the per-view drop discipline
   applies at stroke scale). **THE 19b QUESTION IS POSED WITH EVIDENCE**:
   whether the stone's stroke names the hue explicitly ("deep red garnet")
   — bring the pair's and twins' measured hue behaviour to the ruling; the
   12e law decides the grammar there.
3. **The recipe keys**: proposed per the E13 precedent (cn-strength 1.0 at
   the brush stage per the profile's note; steps/cfg/denoise/seed per
   stroke), with `thin_extent`'s candidate value STATED against the 10d
   curve (the guard serves stage 2; the value is ruled at HALT 1 with the
   curve and the blade's per-view inversion in the room — a pooled number
   cannot judge it).
4. **The edge-on hazard, pre-registered per stroke**: any stroke whose
   frame is edge-on or near-edge-on carries Ruling 20b's misbinding risk —
   state per stroke what constraint its control actually carries (the
   painted neighbourhood is stronger context than the twins had; say how
   much of each frame is already-painted vs hole), and pre-state what a
   misbind would look like there.
5. **HALT 1 — the stroke-lane ruling**: the set, order, prompts, cameras,
   recipe keys and thin-extent value go to the advisor with the masks and
   frames staged as images. `texpass_brush`'s `_NOT_CLEARED` block earns
   its ruled values there; nothing generates before the ruling lands.

### Task 2 — the strokes, after the ruling

One stroke at a time, in the ruled spiral order: graph saved and
pre-flighted before submission (`estimate_credits` each), the stroke
applied through the tool's own invariance ANDON (byte-level: texels
outside the stroke's ruled mask do not change — the tool halts itself, no
skip flag), the fifth-signature watch (dark desaturated crevice fill) and
the 20b watch judged BY EYE at 4× per stroke before the next launches,
one bounded re-roll per stroke on the eye clause only, every rejected
stroke preserved under name. **HALT 2 — the stroked asset staged**: the
walk set (reference | before | after | provenance per stroke region, the
stone at 6× beside the fixture's word, the ribbon at 4×), excluded and
rejected artifacts labelled in-image, the gate report-only in the admitted
configuration with the deep-share diagnostic, coverage restated against
the banked A0. The advisor's sheet-walk first, then the Director.
Finalize, pack and Gate 1 are the NEXT dispatch.

### Do not

Generate before HALT 1's ruling lands · run any stroke out of the ruled
order · touch texels outside a stroke's ruled mask (the in-tool ANDON is
the guard; a fired ANDON is a report, not a retry) · re-roll on any
authority but the eye clause, once · arm any gate · run finalize or pack ·
edit any fixture, profile, or the palette (HALT 1's ruling makes the
profile edits — the advisor's fold, not yours) · write to the memory
store · end a session the Director has not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Every stroke's mask, frame, camera, prompt, seed and graph land beside its artifacts before submission; the derivation's masks staged as images at HALT 1; per-stroke logs |
| ANDON_AUTHORITY | 3 | TWO advisor halts; the invariance ANDON in-tool with no skip flag (A32); per-stroke eye gates before the next stroke launches; a fired ANDON halts the lane |
| NAMED_COMPENSATORS | 2 | Cloud spend bounded to the ruled stroke count + one bounded re-roll each, estimate_credits quoted; every rejected stroke preserved; the pre-stroke atlas is never overwritten — each stroke writes forward |
| DECOMPOSE_BY_SECRETS | 3 | Strokes derive from THIS subject's hole map and fixture; the brush tool binds no profile and agreement is re-verified by value per stroke; the garnet mask derives from the measured ownership partition, not from colour |
| UNCERTAINTY_GATED_HUMANS | 3 | The stroke-lane ruling gates all generation; per-stroke eye gates; the stone judged at 6× beside the fixture's word; HALT 2 ends at the Director |
| EXTERNAL_VERIFIER | 2 | The invariance ANDON checks the tool from inside; the gate and deep-share diagnostic check colour from independent code; the walk sheets check identity by eye. `skip:` on a second model, per precedent |

### Calibration

The route's first prop strokes, and the first stroke class that paints
OVER styled texels (the garnet repaint) — say plainly per stroke what was
hole-fill and what was repaint. The edge-on strokes are where 20b lives:
the painted neighbourhood is your constraint advantage over the twins;
quantify it per frame rather than assuming it. A stroke that fails twice
is the result. Zero credits expected; quote it anyway.

---

## Session handoff 8 (2026-08-08) — the SEVEN REMAINING STROKES to HALT 2. One repair first. Comprehensive.

**Authorised by [E14-ruling.md](E14-ruling.md) Ruling 27f.** Where the lane
stands: the garnet re-projection RAN (works-perfectly gate pixel-identical,
whole-atlas SHA; the stone is garnet — median hue 308.6 → 22.5, L preserved
to 0.088, the 305°-apart partition now 6.6°; styled restored to 1,656,847
exactly) and **stroke 1 is committed** (4,344 texels, every watch measured
clean). One located defect awaits its ruled repair (step 0 below). Seven
strokes remain. A fresh executor session starts here:

```
cd E:\AI\facet && git pull
python tools/facet_index.py build          <- the E15 ritual
CLAUDE.md                                  <- read first, follow exactly. TWO NEW LAWS
                                              since your predecessor: the circular-statistics
                                              law and the chroma-floor sibling note.
docs/experiments/E14-ruling.md             <- Rulings 24-27 are THE LANE'S LAW. Read all
                                              four fully: 24 (the stroke-lane ruling + 24l),
                                              25 (the stone off the generation path),
                                              26 (the re-projection operands),
                                              27 (the repair you run + your authorisation)
profiles/prop.json                         <- texpass_brush's cleared block: order, seed,
                                              re-roll law, prompts path, garnet_reprojection,
                                              demotion record; texpass_iter thin-extent 0.0
docs/experiments/E14-handoff7-garnet-reprojection-report.md   <- the state you inherit
docs/experiments/E14-handoff7-stroke1-halt.md                 <- the misbind record (20b's
                                              second structure; why the stone is not yours)
docs/experiments/E14-brush-prompts.json    <- stems v3, the _order array, the drop map
E:\AI\training\facet_next\E14_strokes\run\ <- the LIVE run state. state/ is current
                                              (post-reprojection, post-stroke-1); state0/
                                              is the pristine A0 and the compensators' source
```

**Your rules and environment are unchanged** (CLAUDE.md §executor).
Generation cloud-only through `brush_cloud_step.py` (binds NO profile —
agreement BY VALUE per stroke against the cleared block; the inverted
no-LoRA pre-flight on every submission; graphs saved with cloud input
names so the file IS the submitted recipe — A30; link topology checked in
code); `estimate_credits` per submission, quoted either way (expect 0 —
quote anyway); the invariance ANDON lives IN the tool, no skip flag, and
no shell chain gates a commit (A32; 21g). ASCII prints. **Blind
predictions first, committed before stroke 2 submits**: per-stroke
committed-texel counts (the probe columns are known — predict the
probe-vs-actual ratio per stroke against 27d's 1.75× first point), the
two edge-on strokes' 20b outcomes, the fifth-signature share range, and
where the deep-share lands after all seven.

### Step 0 — the collar-junction repair (Ruling 27c), before any stroke

**⚠ AMENDED IN PLACE by [Ruling 28](E14-ruling.md) (2026-08-08) — the
count assert FIRED as armed: 27c's predicate yields 1,431 where the
ruling asserted 1,086 (an outcome set's count attached to a descriptive
predicate — this seat's error, 28b). The ruled mask is now THE UNION,
count asserted 1,436**: (territory ∩ z ≤ bottom-edge + 0.010 ∩ stage-1b
gold 42–104 above C\* 12) ∪ (territory ∩ forbidden-after ∩
¬forbidden-before) — both legs re-derived, all three counts asserted
(1,431 / 1,086 / 1,436; any other number HALTS). **And the path sketch
below was wrong (28b-ii): the LIVE state is `run/s1b/`, not `run/state/`
— `state/` is the pre-stroke-1 checkpoint; verify by SHA as the step-0
session did.** The rest of the step stands as written:

The re-projection rotated the GOLD COLLAR's paint (the stone mask's
lower bound clips the bezel arc) toward green — the deep end crossed
into the forbidden band (the visible line at the collar junction), the
shallow end shifted within the gold band. Restore the ruled union's
atlas values from `state0/`, invariance printed (exactly the union
changed; both atlas SHAs recorded), the pre-repair values saved beside
as the op's NAMED COMPENSATOR. The op lives in `tools/diagnostics/`
(the 2a practice). Verify the green line is gone at 6× on one rendered
view; stage the before/after crop in your report.

### The seven strokes — one at a time, in the ruled order

`180 → 45 → 225 → 315 → 135 → 90 → 270` (Ruling 24e; the `_order` array
in the stems file). Per stroke, in pinned order:

1. **Emit** the job at the profile frame; record the job mask px and the
   painted % of figure.
2. **Graph** built from the cleared block's values (seed 770700, steps
   20, cfg 2.5, cn-strength 1.0, denoise 1.0 latent-masked, lora-w 0.0
   re-verified BY VALUE), stems v3 by the job key, saved pre-submission
   with cloud input names; pre-flight (five values, the inverted no-LoRA
   scan, lane corroboration, prompt/negative provenance, link topology).
3. **`estimate_credits`**, quoted; **submit**; invariance ANDON.
4. **The eye gate — every watch MEASURED on the newly-painted pixels,
   never asserted** (the 27e form): red-outside-L5 (wine-band px with
   their row locations — the wrap owns its rows; crossing and blade must
   read zero) · 12e gold (gold-band px located to collar/ring/boss rows)
   · the fifth signature (dark+desaturated share of the fill AGAINST THE
   CONTEXT'S OWN SHARE — less-or-equal is clean) · **20b at 4× on the
   crossing crop** (LOW on 180/45/225/315/135; **HIGH on 90/270** — the
   pre-stated misbind signature: a crossguard-like or figurative form in
   the blade ribbon near the guard, or the guard's edge-on face growing
   a face/skull motif; the stone's cabochon recomposition is this class'
   second instance — read the crop against the CLAY reference, not from
   memory) · the gem unchanged and rendering garnet as context ·
   deep-share beside the totals, with location. **The gate passes before
   the next stroke launches.**
5. **Commit** through the tool's own ANDON; record committed texels and
   **quote probe-vs-actual** (the probe column: 180 → 6,559 · 45 → 10,539
   · 225 → 8,600 · 315 → 9,633 · 135 → 7,728 · 90 → 14,211 · 270 →
   27,010; Ruling 27d pre-states actuals will undershoot — the ratio is
   the calibration series, not a failure).

**The re-roll law** (Rulings 24h/24i as amended by 25f): one bounded
re-roll per stroke, at **770702**, on the eye clause only; the rejected
artifact preserved under name with its graph; **a second failure on any
stroke is THE RESULT — halt the lane with the evidence; no third roll
anywhere, no stroke out of order.**

### HALT 2 — the stroked asset staged

After stroke 270's gate: build the walk set — **reference | before |
after | provenance per stroke region**, the stone at 6× beside the
fixture's word, the ribbon at 4× (both faces), the crossing at 4× —
excluded and rejected artifacts labelled AS SUCH in-image (20d).
Restate: coverage against BOTH denominators (the 210,907 territory and
the 69,239 achievable-as-upper-bound, with the demotion dip and the 27d
calibration stated and the per-stroke probe-vs-actual table); the
on-surface family per Ruling 9's form (island count 46,496 + erode-2
residue beside any off-surface rate); the gate report-only in the
admitted configuration with the deep-share diagnostic and its location
read; the final SHAs. **The advisor's sheet-walk first, then the
Director. Finalize, pack and Gate 1 are the NEXT dispatch — not yours.**

### Do not

Run any stroke before step 0's repair lands and its count asserts ·
generate out of the ruled order · touch texels outside a stroke's job
mask (the in-tool ANDON is the guard; a fired ANDON is a report, not a
retry) · re-roll on any authority but the eye clause, once, at 770702 ·
roll a third seed at anything · arm any gate · run finalize or pack ·
touch the stone (it is styled; the ANDON forbids it and the identity is
banked) · edit any fixture, profile, or the palette (a fixture row is
the advisor's fold — your predecessor's halt at exactly this line was
correct) · write to the memory store · end a session the Director has
not ended.

### Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Step 0's mask re-derived by recorded predicate with its count asserted; every stroke's graph saved pre-submission with cloud input names and prompt_id; probe-vs-actual quoted per stroke; blind predictions committed before stroke 2 |
| ANDON_AUTHORITY | 3 | The repair count-assert halts on any surprise; per-stroke eye gates before the next launches; the in-tool invariance ANDON with no skip flag; a second failure halts the lane; HALT 2 gates finalize |
| NAMED_COMPENSATORS | 3 | The repair saves its pre-state as its own inverse; the demotion's compensator stands; every rejection preserved; spend bounded to seven submissions + bounded re-rolls at expected 0 credits, quoted each |
| DECOMPOSE_BY_SECRETS | 3 | Strokes read the cleared block by value; the stems by job key; the watches measured per structure with locations, never as bare totals; the calibration series kept separate from the coverage claim |
| UNCERTAINTY_GATED_HUMANS | 3 | Every stroke gated by eye before the next; both HALT-2 denominators pre-stated with the calibration so no number surprises; the walk set ends at the advisor then the Director |
| EXTERNAL_VERIFIER | 2 | The invariance ANDON and band instruments check the generator from independent code; the walk sheets check identity against the clay reference. `skip:` on a second model per precedent |

### Calibration

Your predecessor's session is the standard: the anchor before the
operands, two self-caught instrument errors that never left the script,
a fired gate honoured at the exact line the record predicted, and every
watch measured rather than asserted. Named risks: **the two edge-on
strokes are the lane's highest-risk and they run LAST by design** — the
painted context is your constraint advantage over the twins (quantify
it per frame: the ribbon's flanks are real steel now); the probe's
1.75× optimism means small committed counts are EXPECTED — report them
against the ratio, not against hope. A negative result, including an
edge-on stroke that fails twice, is a full success and is reported as
one. Zero credits expected; quote it anyway.
