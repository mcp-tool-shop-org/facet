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
