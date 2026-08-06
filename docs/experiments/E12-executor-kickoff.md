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
