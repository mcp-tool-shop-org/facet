# Working in this repo

This file is about **how to work here**. What is *true* here lives in
[README.md](README.md) (the measured state of every tool) and
[docs/experiments](docs/experiments/) (the evidence trail). Read those for facts; read
this for method.

---

## Why this discipline exists

An earlier arc of this project ran ten sessions in which each session judged its own
output, wrote its conclusions to a shared memory store, and the next session read those
conclusions as established fact. Nothing in the loop was checkable and nothing was gated on
the Director's eye, so errors compounded silently for weeks.

The rules below are not process decorum. Each one was paid for. In the single session that
produced this repo, **six inherited or asserted claims were falsified** — the clay
provenance, the shell count, the facial ceiling, an archived resolution observation, a
coverage baseline, and a pass condition — and every one of them took minutes to overturn
*because it sat next to runnable code*.

---

## The three roles

| role | does | must not |
|---|---|---|
| **Director** (Mike) | sets direction; judges every artifact by eye | — |
| **Advisor** | writes specs, rules on reports, folds findings into the repo | execute, or grade its own rulings |
| **Executor** | runs the spec, measures, reports evidence | decide what results *mean*, or judge quality |

The separation is the point: the session that designs an experiment does not grade its
results, and the session that runs it does not decide their meaning.

## Rules for an executor session

1. **Never judge whether output is good.** Produce measurements and comparison sheets. The
   Director judges. The words *verified, shipped, works, decisive, validated, proven* do not
   belong in a report, a commit message, or a doc.
2. **State a prediction before you look**, and disclose whether it was blind. A hypothesis
   with no prediction cannot be wrong, and one that cannot be wrong teaches nothing.
3. **Stop at every gate. Never improvise past one.** A session that changed a parameter and
   re-ran when a gate fired hit the same gate harder. If a gate fires, report it with its
   evidence and halt.
4. **Do not write to the memory store.** The advisor folds findings into the repo after the
   Director has seen them. The repo is the record.
5. **A negative result is a full success.** Say so plainly and stop, rather than tuning
   toward a number.

## Rules for an advisor session

1. **Rule when the evidence is in; do not predict when it is not.** Deciding is the job.
   Guessing is not — check the advisor's own record below.
2. **Correct in place, with the measurement that overturned the claim.** Never quietly
   delete a wrong statement; the correction is more useful than the original.
3. **Pick a pass-condition unit the experiment cannot move.** Three conditions in this repo
   were mis-specified: two ratios whose denominators moved, then an absolute that broke
   because the experiment *halved the denominator on purpose* — painting 907,825 of 1.7M
   holes read as a "miss" against 923,466 of 3.5M. Ask what the intervention is designed to
   change, then measure something orthogonal to it. Here the honest unit was **dilated texel
   count** (2,551,893 → 813,773, a 68% fall), which cannot be gamed from either side.
4. **Own errors in the commit message.** They are how the next session learns which parts of
   the record to distrust.
5. **Do not end a session the Director has not ended.**

## Rules for everyone

**An inherited claim is a hypothesis wearing a fact's clothes.** Checking one costs minutes;
building on one costs a session. If a spec, README or handoff asserts a number, verify it
before designing around it — including numbers written by the advisor.

**When a number will not move, check the baseline.** The most valuable measurement in this
repo's history came from an executor who stopped chasing a stuck figure and asked whether
the thing it was compared against was real. It was not.

**Bound an expensive arm before spending it.** Compute the ceiling first. One executor
priced a six-stroke experiment at +1.7 points before running it, and skipped it.

**A gate must test the operation's failure mode, not its success mode.** A cull was gated on
silhouette IoU — which is structurally blind to holes punched through *visible* surface,
because the ray behind a removed face still hits geometry. IoU returned 1.00000 on a mesh
with a hole clean through it. The executor noticed the gate could not see its own failure,
added a first-hit depth comparison, and it fired immediately. **Ask what the operation would
look like if it went wrong, then check for that.**

**Prefer eliminating a risk to gating it.** When the same cull was changed from *deleting*
faces to *excluding them from the atlas*, the failure became impossible rather than
detectable — geometry is never modified, so the silhouette cannot change and a future camera
sees flat grey instead of a hole. A guarantee that depends on nobody adding a camera is not a
guarantee.

**Failures stay in the repo, next to the code, with the reason.** `tools/superseded/` is not
an archive; it is the mechanism that stops a falsified approach quietly becoming doctrine
again. Anyone can run those tools and watch them fail the same way.

## Judging artifacts

- **Textures under FLAT light.** A Blender Workbench STUDIO render is not a texture readout —
  grey chalky facet mosaics are specular highlights on flat-shaded normals and vanish under
  `--flat`. Two debugging rounds were lost to this.
- **Geometry under `--clay`.** Texture hides geometry; that confusion caused a whole session
  of misdirected work.
- **At the Director's zoom, not from a contact sheet.** Defects that decide acceptance are
  invisible at thumbnail scale.

## Experiments

Every non-trivial change runs as a numbered experiment in `docs/experiments/`:

```
spec written BEFORE the work  →  report written AFTER  →  advisor ruling LAST
```

A spec carries: the question, hypotheses with predictions, arms varying one thing each,
the metrics, the gates, an explicit out-of-scope section, and a standards-compliance block
scoring the six workflow standards. Amendments are appended in place with dates and reasons
— a spec that hides its own corrections is the thing we are trying to get away from.

## Environment

This is the Robot rig — **drives C and E only. No D:, no F:.** Any `F:/AI/...` path in an
inherited document means `E:/AI/...`.

```
python    E:\AI-Models\trellis2-env\Scripts\python.exe
blender   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
assets    E:\AI\training\facet_E0*\  and  E:\AI\training\saltroad_bake_fix\
```

**Run all Blender work through PowerShell** — Git Bash mangles the paths and every call
fails with `Error: Please select a file`.

**Launch ComfyUI capped:** `--reserve-vram 8.0 --disable-smart-memory`. A bare launch peaks
at the VRAM watchdog's kill ceiling and gets terminated mid-run. This has happened twice.
Cap the consumer; never raise the ceiling.

**argparse eats leading minus signs** — use `--views=-30,0,30`.

**Scripts must create their own output directories.** Two runs died on this.

## Standing technical constraints

These are physics and measured traps, not settings. They are subject-independent and stay in
code rather than in a profile — see [docs/profiles-design.md](docs/profiles-design.md) for
the boundary.

- **Weld before decimating.** An exported glTF splits a vertex at every UV seam; collapse
  decimation on the result tears holes because per-triangle shells have no neighbours.
- **No volumetric predicate on an exported mesh.** It is not a solid — signed distance at the
  centre of a standing figure's chest reads *outside*. Containment, thickness and
  inside/outside must run on the welded mesh, before export.
- **A ray along the surface normal measures the tessellation, not the geometry.**
- **Twins belong to a mesh, not to a character.** Regenerate them for whatever you are about
  to texture.
- **Build the control image; Canny cannot find a silhouette that is not there.**
- **One mask cannot answer two questions** — the mesh silhouette answers *is there surface*,
  the twin's own mask answers *is the paint trustworthy*.
- **Order strokes to spiral outward from already-painted regions**, or the brush composes a
  new character instead of continuing one.

## The advisor's record, for calibration

Kept because a future advisor should know which parts of this repo to distrust. In the
founding session the advisor was wrong about: the shell-soup premise, the clay provenance,
the double-subscribe diagnosis, `--no-head-scale`, the head-pixel multiplier, the halo
hypothesis, `angle_limit` as a lever, deferring the blade fix, and two pass conditions.

The advisor was useful at: ruling once evidence was in, killing options with reasons,
refusing to commission a metric where no honest one existed, and correcting the record in
place.

**Deciding is the job. Predicting is not.**
