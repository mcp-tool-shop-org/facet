# E32 — the armature mark through the route: a thin-tube lattice, a class this route has never measured

**Seat:** executor · **Spec written:** 2026-08-10, before any work · **Advisor rules after the
report** · **Director judges the sheets** · **Credit ceiling: ZERO** — every stage is local.

Subject: `C:\Users\mikey\Downloads\ComfyUI_00122_.png` — a clay render of a wire armature figure,
2048×2048, light grey subject on a grey vertical gradient. It is the `armature` project's brand
mark, so a usable GLB is directly wanted as well as informative.

---

## ⛔ FIRST — two stages are cut, and the reason is a standing verdict, not my preference

The `character-turnaround` skill carries an explicit instruction: *"BEFORE RUNNING STEP 6, SAY
SO… A stage list does not outrank a measured architecture verdict."* It records an incident on
2026-08-02 where an advisor read that verdict, ran eight per-view jobs anyway because a kickoff
said to, and surfaced the conflict only in the wrap-up. **This is me saying so, in the spec,
before anything runs.**

**Steps 5–7 (facing atlas · per-view restylize · multi-view re-projection) are OUT OF SCOPE**,
for two independent reasons, either of which alone would be sufficient:

1. **Step 6 is a measured-wrong architecture.** The Comfy consult's ruling — *"per-view
   generation is the wrong architecture; single-pass multi-view is the fix"* — stands
   unfalsified, and its blocking gate (measure the saltroad LoRA on the Edit-2509 backbone,
   one lever) has not been run. Nothing in this experiment changes that.
2. **Independently, it is irrelevant to this subject.** The restylize half exists to paint a
   *character into house style*: garments named in the prompt, the face preserved by
   `--keep-head 1`, direction clauses, a `face` negative on rear views. **This subject has no
   garment, no face and no identity.** Its final look *is* the clay. Restylizing it would not
   improve a character; it would invent one that does not exist.

The blocked stage and the irrelevant stage are the same stage. That is a clean cut rather than
a compromise, and it is why this experiment can run at all.

**What runs: steps 1–4** — concept plate (already in hand) → TRELLIS.2 mesh → texture projection
→ turnaround render.

## The question

**Does TRELLIS.2 reconstruct a lattice of thin tubes?**

Every reconstruction this route has measured is a solid-ish mass. E14 Ruling 3's hollow
double-walled shell finding rests on **three longswords, a dragon and a galleon** — prop, beast
and vehicle — and E29 Ruling 4 recorded that its own words quantify over more than it measured.
On the character class the wall structure is **unmeasured**, because `mesh_topology`'s
nested-wall leg *declines to compute* on all five character meshes tested.

This subject is a **fourth class and a harder one**: a high-genus lattice of thin tubes with
open loops (the head cage, the torso X-brace, the pelvic loops, ring feet). Nothing in this
repo's evidence base predicts what the reconstructor does with it.

## Premises — marked, and two of them are broken pointers

| # | Premise | Status |
|---|---|---|
| 1 | `mesh_character.py` is the TRELLIS entry point, takes `--ptype 1024_cascade` | **MEASURED** — `E:\AI\sprite-foundry\3d-prerender\mesh_character.py`, args read at spec time |
| 2 | `project_texture.py` exists | **MEASURED, and the skill's path is WRONG.** It is at `E:\AI\sprite-foundry\3d-prerender\project_texture.py`, **not** `saltroad_bake_fix/tools/` as the skill's step 3 states. Enumerated; the tools dir does not contain it |
| 3 | `turn_render.py` is at `E:\AI\training\saltroad_bake_fix\tools\` | **MEASURED** |
| 4 | The skill's required reading, `memory/character-turnaround-pipeline.md` | **MISSING.** Searched the whole memory tree for `*turnaround*` and `*character*`; it does not exist. The skill says to open it *before running the procedure*. **The executor must not pretend to have read it** — record the gap and proceed on the skill body, which is the only surviving statement of the procedure |
| 5 | TRELLIS runs `rembg` internally and square-crops to the alpha bbox, so a grey-on-grey plate needs no pre-keying | **RETRIEVED from E29 Ruling 4**, not re-verified here. **P4 tests it** |
| 6 | The subject is a thin-tube lattice, not a solid figure | **ASSUMED from one look at the image.** The executor measures the subject's own pixel geometry before predicting anything about its reconstruction |

**Premise 5 matters more than it looks.** This plate is exactly the case this repo's law names —
*"a Workbench clay render is flat grey on flat grey, so a threshold cannot find the figure"* —
and corner-median keying is retired after three failures. If `rembg` handles it inside
`pipe.run`, no keying is needed at all and the law is satisfied by construction. If it does not,
**that is a finding, not a reason to hand-roll a key.**

## Gates

- **Gate L (licence) — ANDON.** Run `mesh_character.py` with `--licence-strict`. `licence_guard.py`
  exists because nvdiffrast arrives as collateral of a package `__init__` four levels up from
  anything we ask for. If the guard fires, **report it and halt** — do not disable the flag to
  get a mesh. A mesh obtained by switching off a licence guard is a mesh we cannot use.
- **Gate M (mesh sanity).** The GLB loads, and its bbox is reported against the concept's aspect.
  A reconstruction whose proportions do not match the plate is a failure to report, not to fix.
- **Gate 0 — the sheet before the metrics.** No number is quoted until a
  **concept | mesh (clay) | projected | turnaround contact sheet** exists. This repo ran four
  arms and two gates once before building that sheet; when it finally existed the Director read
  the whole thesis off one panel.

## Predictions — register before looking, state whether blind

Write what one of the counted thing **is** before the number.

- **P1 — fusion.** At the crossings (the torso X-brace, where limbs meet ball joints), does the
  reconstruction keep the tubes separate or bridge them into webbing? Predict which, and predict
  the count of *distinct visible openings* the mesh preserves against the plate's count.
- **P2 — topology.** Predict shell count and whether `mesh_topology`'s nested-wall leg
  **computes at all** on this subject. It declines on characters for want of a second manifold
  piece above 1% of faces; a lattice may or may not give it one. *A row you predict to be
  uninformative is still a prediction and can still miss.*
- **P3 — the thinnest member.** Measure the limb's width in the plate in pixels first, then
  predict whether it survives at `1024_cascade` as a tube or collapses to a ribbon/blob.
- **P4 — the key.** Predict whether `pipe.run`'s internal `rembg` isolates a light-grey figure
  from a grey gradient. Premise 5 says it should; premise 5 is retrieved, not measured here.

## Out of scope

Restylize and everything downstream of it (see the ⛔ block) · any LoRA · Comfy Cloud and any
credit spend · identity and character questions, which this subject cannot answer · rigging ·
and **armature's E02**, which is a separate repo mid-flight and must not be touched.

## Report

Concept-plate measurements first (subject bbox, limb width in px, background gradient range),
then predictions with blind/not-blind stated, then Gate L and Gate M verdicts, then the Gate 0
sheet, then measured values beside predictions. A gate that did not run is written **NOT YET
RUN**. **No judgement words** — the Director decides whether the mesh is good.

## Standards compliance

| Standard | Score | Evidence |
|---|---|---|
| PIN_PER_STEP | **2** | Every stage is a recorded command with explicit args; the plate's sha256 is pinned in the report. Not 3 — no per-run lock file (the pipeline's own open P2). |
| ANDON_AUTHORITY | **2** | Gate L halts on the licence guard, Gate M on proportion mismatch, Gate 0 on order-of-work. Not 3 until one fires here. |
| NAMED_COMPENSATORS | **3** | Every action is a file write to a NEW path; the concept plate and any input mesh are opened read-only. Compensator: `rm <out>.glb` / `rm <render dir>`. **Zero credits, no upload, no publish** — nothing leaves the rig, which is itself the strongest compensator available. |
| DECOMPOSE_BY_SECRETS | **3** | Inherited Parnas-clean seams: mesh generation, projection (hides camera calibration), render (hides lighting/tone). This experiment changes none of them. |
| UNCERTAINTY_GATED_HUMANS | **2** | Gate 0 puts the sheet in front of the Director before any metric is read. Not 3 — no numeric trigger for escalation. |
| EXTERNAL_VERIFIER | **1** | Honestly weak, as the pipeline's own scorecard records: the verifier is the advisor's eye plus geometric measurement, which is a different *kind* of check rather than a different model family. Not remediated here; naming it rather than inflating it. |

**13 / 18.** EXTERNAL_VERIFIER at 1 carries the pipeline's existing P1 remediation and is not
made worse by this experiment.
