# E08 — executor kickoff: the intersection regression, then eight

Paste this into a fresh executor session. Written by the advisor, 2026-08-04. This file
previously carried the contradiction-test dispatch; those tasks are complete and ruled
(Amendments 20–26), and that version lives in git history. This dispatch supersedes it.

---

## You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                                     <- how to work here. Read first, follow exactly.
docs/experiments/E08-ruling-gate0.md          <- the live ruling; Amendments 23–26 at minimum
docs/experiments/E08-armB-projection-halt.md  <- the halt this dispatch answers
docs/experiments/E08-armB-state.md            <- the Arm B build record and its anchors
canon/W3-IDENTITY.md                          <- the fixture
README.md                                     <- measured state of every tool
```

**Your rules** (CLAUDE.md, §"Rules for an executor session"): never judge whether output is
good · state a prediction before you look, and say whether it was blind · **stop at every
gate, never improvise past one** · do not write to the memory store · **a negative result is
a full success.**

The previous executor halted at the bbox andon, overturned its own "harmless proxy" reading
with a measurement, and declined to make a call that was not its to make. That is the
behaviour this repo runs on, not an obstacle to it.

## Where this stands

- **The architecture is measured.** The prompt wins 8/8 contradicted elements, median ΔE 46.3
  against 6.2 held, a 7.4× separation. Twins register; identity rides in the prompt.
- **Eight twins exist** (`ARMB/`), views 2 and 6 re-rolled once under the pre-registered
  palette rule, both clearing the blob bound (402 / 345 against 800). The percentage bound is
  **withdrawn** (Amendment 25) — its stated derivation described a different instrument.
  **Ruled: project eight.** twin_2 is flagged (distributed off-palette, uncharacterised) and
  projects anyway; Gate 1 is where that gets judged.
- **Eight-camera projection halted at the bbox andon on view 6** — the re-rolled twin painted
  a cast shadow, connected to the figure, and the keyed mask feeds `distance_transform_edt`:
  27.49% of the figure's texels get an edge distance changed > 0.5 px, 21.24% > 2 px, max
  36.22 px. The andon caught a real contamination pathway, not a cosmetic bbox blowout.
- **Amendment 26 ruled the fix:** intersect the twin's trust mask with the mesh silhouette
  before the distance transform. Paint outside the silhouette is on no surface at all; asking
  whether it is trustworthy is a category error. **A correction, not a tune — but it moves
  `dist_in` at the rim for every twin, so it is its own measured change.** That regression is
  Task 1.
- **The gap, stated plainly:** no asset better than the one the Director rejected has been
  rendered end to end. Everything since has been instrument repair and architecture.

## Environment — read before any tool call

- **The VRAM watchdog is DOWN** (heartbeat stale since 2026-08-04 10:41). Tasks 1 and 2 are
  CPU-only measurement and may proceed. **Before any local GPU step** (including Blender
  renders in Task 3): `pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1`, and report
  the restart in your log.
- **Generation runs on Comfy Cloud, never locally.** The ceiling stays at 31,200 MiB. A
  measured arm on the local rig is a number credited to the wrong cause.
- Blender through **PowerShell** (Git Bash mangles paths) · `--views=-30,0,30` form for
  argparse · scripts create their own output directories.

---

## Task 1 — the intersection regression

**The question:** does restricting the trust mask to surface that exists change the adopted
2-camera baseline — by how much, where, and in which direction?

### The change, pinned

One operand changes: the twin's trust mask becomes `twin_fm ∧ mesh_fm` — the keyed figure
intersected with the **exact, undilated** raycast silhouette — everywhere it is consumed *as
trust*. Its consumers in [project_twins.py](../../tools/project_twins.py) are:

| consumer | line | note |
|---|---|---|
| `dist_in = distance_transform_edt(fm > 0.5)` | 404 | the edge-erosion field — the pathway the halt caught |
| `fig_w` from `fm` columns | 423–424 | scales `ed_body`/`ed_head` via `esc` — a shadow inflates erosion **globally** in `--edge-absolute` mode |
| `e_img` / median prints | 437–438 | diagnostics; move with the operand |

The raw `twin_fm` **survives as a diagnostic**: the bbox report and the keyed-outside counts
are measured on it, per Amendment 26.

- Implement behind a flag (suggest `--trust-intersect`), **default off**.
- **The same operand changes in the instrument**,
  [e08_acceptance.py](../../tools/diagnostics/e08_acceptance.py): its `fm` (line 137's
  distance transform and the `fig_w` below it) intersects with the **undilated** sidecar mask
  (already loaded as `raw_mask`, line 147). The `maximum_filter` size-5 dilation stays what it
  is — a sampling tolerance for `mask_ok`, a different question. If the instrument and the
  pipeline intersect with different silhouette objects, the regression measures nothing.
- **Consistency check, one line:** count differing pixels between `project_twins`' live
  raycast `mesh_fm` and the sidecar mask, views 0 and 4. Expect 0. If nonzero, **report it and
  do not reconcile silently** — which object is authoritative is a ruling.
- **The bbox andon, per Amendment 26:** with the flag on, the raw bbox is still measured and
  printed every view; the `assert` demotes to a printed warning (intersection makes the
  asserted quantity pass by construction, and a check that cannot fail is not a check). Print,
  always and per view: **IoU(raw `twin_fm`, `mesh_fm`) and centroid offset in px.** Those are
  the registration baseline. **The halt that replaces the bbox assert is armed by the advisor
  from your report — not by you, and not in this run.**

### Arms

**R0 — the no-op anchor.** The edited code, flag **off**, replaying the exact invocation that
produced `ARMB/stage1_2cam.png` (views 0+4, `--edge-absolute`, fitted keying, the ARMB twins
— parameters as recorded in the halt report and the run's own sidecars; if the full invocation
turns out not to be recorded anywhere, **that is a deviation to report** — a recipe that does
not reproduce its output is not a recipe). Must reproduce, to the digit:

```
styled 1,050,368 / 2,402,810 valid = 43.7%
styled / reachable 1,050,368 / 1,265,391 = 83.0%
variance 0.02597   holes 1,352,442
```

**GATE R0: any digit differs → HALT.** R0 is not bureaucratic — it proves the flag edit is a
true no-op when off. If it fails, the code path moved under you and nothing downstream is
comparable.

**R1 — the fix.** Flag **on**, everything else byte-identical. One variable, no GPU, minutes.

**Before running R1, state your prediction** — direction and rough magnitude of the triple's
move — and mark it blind. Amendment 26's pre-registered direction: *more trusted paint at the
rim, since erosion is no longer pushed deep by a phantom boundary.*

**Calibration note, so a null is not misread:** views 0+4's outside-silhouette paint is
unmeasured (view 2 carries 3,772 px, view 6 8,991 — the front/back pair may carry much less).
A near-null R1 delta means **the fix does not break the adopted baseline**, which is exactly
what this regression exists to establish before eight cameras — where view 6's repair is
already measured at 27.49% of figure texels. Report what is; do not chase a large number.

### Report — `docs/experiments/E08-intersection-regression.md`

Per arm and per view:

- the triple, variance, holes
- keyed-outside-silhouette px and largest connected component (raw `twin_fm ∧ ¬mesh_fm`)
- `fig_w` raw vs intersected; the raw bbox; IoU and centroid offset (the registration baseline)
- **gain/loss decomposition:** texels styled in R1-not-R0 and R0-not-R1, counts per view, with
  a location characterisation (edge-distance strata suffice). *A swap is not a gain until you
  have looked at what left.*
- `dist_in` delta stats inside the silhouette for views 0 and 4 — the analogue of the view-6
  27.49% / 21.24% / 36.22 measurement.

**GATE R1: report and STOP.** Adoption is a ruling (Amendment 26: small and expected → adopt
and restate A2 in the README with the reason; large or wrong direction → halt). Do not edit
the README yourself; the advisor folds after the ruling.

### Out of scope for Task 1

- `texpass_iter.py`'s commit guard (below) — enumerated, not fixed. One variable.
- The E07-era diagnostics (below) — historical instruments; they must keep reproducing E07.
- The palette gate, the prompts, the spec, anything cloud.

## Consumers of the same root cause — enumerate, do not fix here

Per CLAUDE.md: *when you fix a root cause, find its other consumers.* Keyed-mask distance
transforms in this repo:

| site | status |
|---|---|
| `project_twins.py:404` | **this dispatch** |
| `diagnostics/e08_acceptance.py:137` | **this dispatch** — instrument must match pipeline |
| `texpass_iter.py:236–241` | ⚠ the brush commit guard keys the **brush output** with a **corner-median** (8×8 corners → median → 0.06 threshold) and feeds `distance_transform_edt`, unbounded by the silhouette. Corner-median keying is **retired after three failures** — this is a fourth live site, on a different image class (the brush's own composite). **Not touched in this run.** Confirm the enumeration in your report; the advisor rules when the brush stage is next touched. |
| `diagnostics/commit_funnel.py:123` | diagnostic twin of the above; same note |
| `diagnostics/texel_provenance.py:143`, `diagnostics/e07_l2_bound.py:254` | E07-era instruments — **do not modify**; they exist to reproduce E07's numbers |
| `diagnostics/e08_bg_separation.py:104` | ⚠ found by the Task 1 report (missed by this dispatch's grep — advisor's miss, owned in Amendment 27): A4's separability instrument, corner-median key + unbounded EDT. A4 is withdrawn; the tool reproduces its record. **Fenced with the E07 instruments — do not modify.** |

## Task 2 — eight cameras. CLEARED by Amendment 27; step 0 first.

Task 1 is ruled: **the intersection is ADOPTED as the route default** (Amendment 27 — read
it in full before step 0; it also owns the direction clause as mis-derived, so do not treat
"down" as a failed prediction). Step 0, in order:

1. Flip `--trust-intersect` default **on**; add `--no-trust-intersect`; re-run the R0 recipe
   once with the negation flag — must stay pixel-identical. The A2 and mask-keyed anchor
   recipes gain the explicit negation flag in their recorded invocations. ⚠ Anchor language
   corrected by the Task 1 report: A2's 938,718 needs `--edge-absolute --key-corner-median`
   (the bare default halts at A3's pre-existing 73.87% background probe — known state of a
   withdrawn arm, not a defect to fix).
2. **Arm the registration halt** in `project_twins.py`, per view, active alongside the
   intersection: **HALT if IoU(raw `twin_fm`, exact silhouette) < 0.80.** Derivation is in
   Amendment 27 (adjudicated views 0.8329–0.9533; measured failures ≤ 0.578). It cannot fire
   on the current eight — they are its calibration set; its jurisdiction is future twins.
   IoU and centroid offset print every view; the raw bbox pair stays a printed diagnostic
   with its assert demoted.
3. `e08_acceptance`: when the flag is on, verify the sidecar against the live raycast
   (0 differing px, `silhouette_agree.py` is the check) and halt otherwise; give the mask
   stem an explicit argument so the instrument can point at the ARMB layout.

Then the projection:

- All eight twins, including the re-rolled twin_2 and twin_6 (Amendments 25–27: no third
  roll, view 6 is not dropped, twin_2 carries its flag to Gate 1).
- Read against **1,042,794 / 43.4% / 82.4%** (the R1 baseline — not R0's 43.7/83.0) and the
  **74.10%-of-valid** ceiling, which the flag does not touch (reachable moved 0). **The
  acceptance lever is spent — eight buys from the ceiling, not from acceptance. Do not grade
  eight on an acceptance rate.** *(⚠ Corrected by the Task 2 measurement, restated in
  Amendment 28: acceptance rose 82.4% → 92.9% with no test changed — union acceptance is a
  function of camera count. The instruction stands; the "spent at 83.0%" phrasing does not.)*
- **Add the blade-band table**: per view, all eight cameras, candidate texels landing in the
  band the key excludes and how many are accepted (§9a's measurement generalised). This is
  reporting for the post-Gate-1 blade arm, not a change to make now.
- CPU only. State which anchors you re-ran.

## Task 3 — through to a finished asset. CLEARED by Amendment 28; step 0 in order.

Projection is done (`stage1_8cam.png`, 68.8% of valid). What remains: strokes → finalize →
pack → renders → the Gate 1 sheet. The Director's standing verdict is *the asset is not
close*, and nothing yet has put a better one in front of him. This is the step that does, or
reports why not. **Read Amendment 28 in full first** — it carries the three rulings this
section depends on.

Step 0, in order — each is a gate:

1. **The gained-texel background check** (A28 Ruling 2). The 9,053 texels the intersection
   admitted on views 6/5/1 get A2's admitted-texel check — median ΔE against the view's
   fitted background, fraction within ΔE 10 — with view 2's equivalent 2.75 px band as the
   normative control. Clean → `stage1_8cam.png` is this task's input. Contaminated → **HALT**
   (it would implicate the width-scaled erosion generally).
2. **Stroke prompts to the fixture** (A28 Ruling 3). `texpass_brush.py`'s default prompt is
   stale and carries the struck "gold necklace" — it does not run. Build a versioned stroke
   prompt from W3's NAMED elements verbatim (N6 is the belt medallion; N14–N16 name the
   greatsword, crossguard, pommel — the brush paints the 50,569 unreferenced blade texels, so
   this is the blade's honest test), with per-view facing handling per the E01 rule, recorded
   per stroke in sidecars.
3. **First-stroke anchors.** (a) Outside-figure invariance: max |edited − emitted| outside
   the dilated figure mask ≈ 0 — this is the licence for the commit guard's corner-median on
   its flat synthetic backdrop (A28's owed `texpass_iter` ruling: guard unchanged for this
   run; modernisation is a post-Gate-1 regression). Materially nonzero → **HALT**. (b) Cloud:
   the brush is a *different graph* (inpainting) — enumerate what is already on cloud,
   `dry_run` first (free), `estimate_credits` before submitting, halt on surprises.
4. **Watchdog restart before any local render step** (see Environment).

Then run it through. Deliverable: **reference | asset | provenance | error at the Director's
zoom, views 4–6 included** — and **the blade's provenance called out explicitly**, so the
unreferenced band is visible as provenance rather than discovered as a surprise. **Build the
sheet before the metrics.** Textures under `--flat`, geometry under `--clay`. Report the
finished asset's reference/diffusion/interpolation split beside E06's 28.4/37.7/33.9.

## Do not

Judge or adopt — report and stop at each gate · retune or invent a threshold after seeing a
result (withdrawing is the only legal move, and it is the advisor's) · third-roll any twin ·
drop view 6 · fix `texpass_iter`'s keying in this run · modify E07 diagnostics · project from
`canon/twin_{front,back}.png` · write to the studio memory store · run a measured arm on the
local rig · raise the watchdog ceiling · end a session the Director has not ended.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | R0 replays a recorded invocation byte-for-byte; the flag is the single delta; sidecars and flags recorded per run |
| ANDON_AUTHORITY | 2 | Gate R0 halts on any digit; Gate R1 halts pending ruling; the registration halt is being re-armed on the direction the invariant does not bound |
| NAMED_COMPENSATORS | 2 | Tasks 1–2 write only regenerable local artifacts (prior atlas preserved; `atlas.prev.png` pattern). Task 3's cloud spend is irreversible-by-nature: bounded, not compensated — `dry_run` + `estimate_credits` before submit, halt on surprise. No publish/push/release in scope. |
| DECOMPOSE_BY_SECRETS | 2 | Executor measures, advisor rules, Director gates; sites grouped by the one shared operand; instruments that must not change are fenced |
| UNCERTAINTY_GATED_HUMANS | 2 | Adoption gates on the advisor ruling with a pre-registered decision rule; Gate 1 gates on the Director's eye; the calibration note pre-frames the likely-null contrastively |
| EXTERNAL_VERIFIER | 1 | `skip:` for Task 1 — deterministic geometry replay, no generative output is graded by its generator. For Task 3 the verifier is the Director's eye on the sheet, with artifacts shown rather than argued. |

## Calibration

The advisor's errors are catalogued in the ruling and in CLAUDE.md's record — including, this
session, a check whose shape assumed its answer and a two-variable "one-variable" arm. **Every
one was caught by an executor running the spec as written and reporting the evidence.** The
previous executor's self-overturn on the "harmless proxy" reading — measured, not argued — is
the standard. Do that.
