# E33 — the first performer through the route: a solid-limbed clay mannequin, and a register the Director has not chosen

**Seat:** executor · **Spec written:** 2026-08-11, before any route work · **Advisor rules
after the report** · **Director judges the sheet and rules the register** ·
**Commissioning spec:** `E:\AI\armature\docs\dispatches\F01-the-first-performer.md`
(armature advisor, 2026-08-11) · **Runs under facet's CLAUDE.md, not armature's.**

Subject: `E:\AI\armature\outputs\E07\concepts\00-directors-pick-clay-armature.png` —
sha256 `753383255718DB7212B21007A24FCE0D9A6A101CB352662459EEC690D335E0DC`, 1,216,363 bytes,
1328×1328, RGB. Director-generated on Comfy Cloud (Qwen-Image 2512) and picked by him from
six candidates. **The image is the contract; its generation parameters were not recorded,
the pinned file is.** Copied read-only to `E:\AI\training\facet_E33\armature_performer_clay.png`
(hash re-verified byte-identical after the copy — recorded in §0 of the report).

`E:\AI\armature` is READ-ONLY for this seat. Nothing here writes into it.

---

## The question

**Does facet's character route carry a solid-limbed clay mannequin from concept to a
styled-twin ruling — and what is this subject's mask geometry?**

E32 put the *armature mark* (a thin-tube lattice, fill of bbox **10.78%**) through steps
1–4 of this route and its projection stage halted at `--min-iou`. This subject is the mark's
nearest living relative in silhouette family — long thin limbs, ball joints, a readable face
— and its **class is the open question**: a solid mannequin and a lattice are different
objects to a reconstructor and to an area-normalised registration score. E32's own ruling
says the character class remains **UNMEASURED** on the nested-wall axis, and F01 names the
character class as facet's explicitly-unmeasured subject class.

## ⛔ Scope, stated first — two order corrections from the commissioning seat

1. **The deliverable is on the way to the route's STYLED output.** Clay is the *entry*
   stage of this route, never the destination — F01's gate A4 was corrected by the Director
   on 2026-08-11 to read *"the styled twin's colour and material variety survive
   projection."* Nothing in this run treats the clay mesh as the product.
2. **This run STOPS at twin candidates**, for the Director's register ruling. **No
   projection, no brush, no fill.** Everything after the twin stage is out of scope and is
   absent rather than skipped by preference.

**What runs:** image-to-3D → weld → density allocation → cull → styled twin candidates from
THIS mesh → Gate-0 sheet → STOP.

**Deliverables are unrigged.** Rigging is armature's E07, a different repo.

## The venue ruling, inherited and recorded

**Dispatcher, 2026-08-11, recorded in F01:** the twin stage runs on **Comfy Cloud**. The
LOCAL restylize graph is VRAM-falsified — it stages **31,006 MiB** against a **31,200 MiB**
ceiling that is never raised, and `--reserve-vram` / `--disable-smart-memory` are both
falsified levers (facet CLAUDE.md, Environment). It is not attempted here.

**Cloud enters at the twin stage ONLY.** If any other step appears to need cloud or a paid
API, that is a **Gate V halt**: stop and report, do not route around it.

## Premises — every one marked

*The law this table exists for: an inherited claim is a hypothesis wearing a fact's clothes,
and it binds hardest on the premises of one's own dispatch (E29 Ruling 4).*

| # | premise | status |
|---|---|---|
| 1 | The input file is the Director's pick at the stated hash and size | **MEASURED** — `Get-FileHash` at spec time, both at source and after the copy: `75338325…E0DC`, 1,216,363 bytes. Match |
| 2 | `mesh_character.py` is the TRELLIS.2 entry point, takes `--ptype 1024_cascade` and `--licence-strict 1`; the licence guard exits non-zero | **MEASURED** — args read from source at `E:\AI\sprite-foundry\3d-prerender\mesh_character.py:9-25` at spec time |
| 3 | `turn_render.py` is at `E:\AI\training\saltroad_bake_fix\tools\`, default frame 757×1024 | **MEASURED** — args read at source. ⚠ E32 recorded a second, DIFFERING copy at `facet/tools/verify/turn_render.py`; the `saltroad_bake_fix` copy is used here, as E32 used it |
| 4 | `e12_frame.py` derives the render frame per mesh and rounds to a multiple of 16 | **MEASURED** — args read at source; E32 used it to replace a default that cropped its subject's arms |
| 5 | `e32_route_preprocess.py` + `e32_plate_geometry.py --mask` measure a plate's own geometry at route scale | **MEASURED** — both present, args read at source |
| 6 | The route's segmenter is **BiRefNet at 1024×1024**, run inside `pipe.run` when the plate carries no alpha; output premultiplied; square crop about the alpha bbox can clip by a pixel | **MEASURED BY E32, RETRIEVED HERE** (E32 §2, upheld at E32 Ruling 6, which retired the phrase *"pipe.run runs rembg"*). Our plate is **RGB with no alpha channel at all**, so the no-alpha branch is taken. **P0 re-tests the outcome on this plate**, not the mechanism |
| 7 | `--min-iou 0.80` in `project_texture.py` fired at **0.5878** on E32's lattice and the halt was **UPHELD**; the threshold does not move | **MEASURED BY E32, RETRIEVED** (E32 §5; E32 Ruling 4a/4b). **Projection is out of scope here**, so the precedent is recorded and not exercised |
| 8 | The four Qwen base models the twin graph names are on Comfy Cloud by exact name | **MEASURED** — `search_models` exact-name at spec time returned 1 row each for `qwen_image_fp8_e4m3fn.safetensors`, `qwen_2.5_vl_7b_fp8_scaled.safetensors`, `qwen_image_vae.safetensors`, `Qwen-Image-InstantX-ControlNet-Union.safetensors` |
| 9 | The **saltroad LoRA is on Comfy Cloud** | **MEASURED FALSE — see §"The LoRA is not there".** `search_models` returns **0 rows** for `q="saltroad"` `type="lora"` and **0 rows** for `q="mikeyfrilot"`. The same probe returns exactly one row for each base model above, so the query form is precise |
| 10 | Comfy Cloud generation on this workspace is free | **MEASURED FALSE.** `get_usage_report` shows a live, metered **GPU Hours Product** line — **$23.409** over the 61 days to 2026-08-11 and **$2.881** already accrued in today's bucket at spec time. facet's *"zero credits across E04/E10/E12/E13"* is about **partner-API credits**, and it does not extend to GPU hours. **This spec therefore states a job ceiling, not a zero** |
| 11 | The subject is a **solid-limbed** mannequin (as against E32's lattice) | **ASSUMED, from one look at the plate.** §"First route act" converts it to MEASURED before any prediction about the reconstruction is registered |
| 12 | The style register for this subject is **UNDECIDED** and is the Director's canon call | **MEASURED** — `docs/style-registers.md` lists no row for this subject or class, and its founding law is *"no class inherits another's register"*. F01 gate A4's correction says the same thing in the commissioning seat's words |
| 13 | The subject class is **new** — a mannequin/mascot, not W3's warrior | **ASSUMED.** Consequence taken now rather than argued later: **every route stage runs UNPROFILED** (`subject_profile.bind` with no `--profile` leaves every default untouched — read at source, `tools/subject_profile.py:96`), with each needed value passed explicitly and its provenance recorded. E12's Gate 0 set this precedent for a new subject |
| 14 | facet `main` is at `c0031c1`, one commit ahead of `origin`, tree clean, and **must not be pushed** (`pyproject` pins `record-index>=0.1.0`, which is not on PyPI; a push turns CI red) | **MEASURED** — `git log`, `git status --porcelain` (empty), `git rev-list --left-right --count origin/main...HEAD` → `0 1`. Commits land LOCALLY; the pin is not touched |
| 15 | The VRAM watchdog guards GPU work at 31,200 MiB | **MEASURED at session open** — `_watchdog_start.ps1` reported a live 1 s heartbeat, stopped it and re-armed: `kill@ VRAM 31200 MiB / RAM 90% / temp 87C, x3 @ 2s`. **The ceiling is never raised** |

## The LoRA is not there, and that is a measurement rather than an obstacle to route around

`saltroad_style_v2_lowlr_000001500.safetensors` is the card behind facet's **painterly**
register. E08 recorded three outstanding steps to get it onto Comfy Cloud: an HF **read**
token entered into Comfy Cloud → Settings → Secrets, a browser-only Model Library import,
and a read-back of the resulting `lora_name`. **All three are Director actions** — one is a
credential action and one is an account-configuration action; neither is this seat's to
perform, and neither is attempted.

⚠ **The honest bound on this measurement:** `search_models` indexes the catalog, and E08
recorded that an un-imported LoRA name produces a *warning* rather than a failure at
`dry_run`, so a catalog miss is strong evidence and not a proof of absence from a private
Model Library. The spec's response is to **not stake an arm on it**: every arm below runs
**LoRA-free**, and the painterly register is reached through prompt terms with that fact
labelled on the sheet. If the Director wants the saltroad card itself judged, that is a
separate submission after the import, and the two are not conflated.

## Licence — what enters, and nothing new does

**No non-commercially-licensed model, weight, LoRA, preprocessor or code dependency enters
this experiment.** Every model named below is already in facet's verified chain:

| item | role | licence position | source of the row |
|---|---|---|---|
| TRELLIS.2 `1024_cascade` via `mesh_character.py --bake clean` | image-to-3D | clean bake path; **nvdiffrast is BLOCKED at load** by `licence_guard.py` and `--licence-strict 1` exits non-zero if it was reached | facet README licence position; E32 Gate L |
| `qwen_image_fp8_e4m3fn` + `qwen_2.5_vl_7b_fp8_scaled` + `qwen_image_vae` | twin generation | the twin graph facet has run since E08 | E08 cloud migration state |
| `Qwen-Image-InstantX-ControlNet-Union` | twin control | same graph, same arc | E08 cloud migration state |
| Blender 5.2, numpy, scipy, trimesh, open3d, Pillow, OpenCV | render + measurement | facet README licence position | — |

**Excluded, restated because the guard is structural rather than attested:** `nvdiffrast`
(non-commercial), `Hunyuan3D-Paint`, `MVPaint`, `TEXGen`, `UltraSharp/SUPIR/StableSR`.
**No new licence row is introduced by this experiment**, so no new licence check is opened.

⚠ **One boundary carried forward rather than claimed away:** the concept plate itself was
made on a closed cloud API by the Director. That is the same position `docs/concept-prep.md`
records for the clay hop — upstream of the recorded route, with the artifact frozen and
hashed. No licence claim in this report covers the plate's provenance.

## Credit ceiling — stated before the first submission, itemised per arm

Premise 10 measured GPU Hours as a live metered product, so *zero* is not available as a
ceiling and is not claimed.

| arm | submissions | node classes | partner-API nodes |
|---|---|---|---|
| R1 ultra-realistic | 2 (views 0, 4) | Qwen UNET + CLIP + VAE + ControlNet Union + KSampler | **none** |
| R2 painterly (prompt-only, LoRA absent) | 2 (views 0, 4) | identical | **none** |
| R3 clay-native | 2 (views 0, 4) | identical | **none** |
| probes | ≤ 2 `dry_run` (no GPU, no job) + ≤ 1 live probe if a dry_run cannot settle a name | — | **none** |

**Ceiling: 8 executed cloud jobs, zero partner-API nodes, zero partner credits.** A ninth is
a halt, not a judgement call. `submit_workflow`'s spend gate cannot fire on these graphs
because they contain no paid API node; that is the arm-level bound, and the GPU-hours delta
is measured by taking `get_usage_report` **before and after** and quoting the difference.

**Why two views and not eight.** A twin set is eight views, and eight *per register* before
the register is chosen would be 24 jobs to answer a question the front view carries. Views
**0 (front)** and **4 (back)** are E08's own canon pair, and the back view is the one that
tests the per-view prompt rule (a face term on a rear camera is an instruction to draw a
face — E01, measured). The full eight-view twin set is generated **after** the ruling, from
the chosen register, in a later run. *Bound an expensive arm before spending it.*

## Arms — each varies exactly one thing

Everything is pinned across arms: the mesh, the render, the exact silhouette mask, the
constructed control image (byte-identical across arms by construction — it is built once and
reused), seed **770700**, steps **20**, cfg **2.5**, denoise **0.92**, `cn-strength` **0.9**,
`shift` 3.1, `euler`/`simple`, and the frame. **The only difference between arms is the
register clause of the prompt**, plus the negative that travels with it.

The identity half of every prompt is the same string, and it names what the plate actually
carries — *the identity law: a canon element not named in the prompt is arriving by accident
and will leave the same way.* Named elements: a slender jointed mannequin, ball-and-socket
shoulders / elbows / wrists / hips / knees / ankles, a smooth bald head with a simple
readable face (drawn brows, closed lidded eyes, a small smile), small ears, sculpted
thumbprint hatching on torso and limbs, empty open hands, simple rounded feet, plain pale
background.

| arm | register clause | LoRA | why this arm is on the sheet |
|---|---|---|---|
| **R1** | *ultra-realistic, matte fired clay, harsh directional light* | **NONE** | the earned NO-LoRA register (prop and beast classes, `docs/style-registers.md`) |
| **R2** | *painterly, visible brushstrokes, worked surface* | **NONE — labelled** | the terms of the earned painterly register, reached without its card (premise 9) |
| **R3** | *unglazed terracotta, matte sculpted clay, soft studio light* | **NONE** | the subject's **own** material. ⚠ **Not a row in `style-registers.md`** — offered because this subject is made of clay and a clay mascot painted as clay is a real option, not because any precedent supports it. Labelled on the sheet as unearned |

**This spec ranks nothing and neither does the report.** Which register is *the* register is
canon, and canon is the Director's. **Rejecting all three is a legitimate outcome** and is
stated here so it cannot be read as failure later.

## First route act — the class measurement, before any prediction

`e32_route_preprocess.py --image <plate>` then `e32_plate_geometry.py --image <route plate>
--mask <segmenter mask>`, which converts premise 11 from ASSUMED to MEASURED and gives the
denominators every later normalisation needs: mask area as a fraction of the route frame,
figure bbox, **fill of bbox**, the local-thickness width distribution, and the enclosed-
opening curve against min-area.

**Predictions are registered only after this runs**, in
`docs/experiments/E33-predictions.md`, each marked blind or not — the E32 order exactly.
No prediction about the reconstruction may be written before the plate's own geometry is on
paper.

## Gates

Every gate below either lives inside the tool that performs the irreversible step and
`raise`s, or is an order-of-work gate on this seat. **A fired gate is reported with its
evidence and the run HALTS. No parameter is changed and re-run to get past one.**

| gate | where it lives | what fires it |
|---|---|---|
| **L — licence ANDON** | inside `mesh_character.py`, `--licence-strict 1` | non-commercial code (nvdiffrast/nvdiffrec) reached on a run claiming a clean bake. Non-zero exit. **The flag is never disabled to obtain a mesh** |
| **M — mesh sanity** | this seat | the GLB loads; extents and w/h reported against the plate's figure aspect. **Reported, not judged** — a proportion mismatch is a finding, not a thing to fix |
| **F — frame derivation** | `e12_frame.py` | the render frame is derived from THIS mesh and rounded to ÷16. E32's subject was cropped by the 757×1024 default; a default frame is not used here. ÷8 is the generator-legal floor, ÷16 preferred |
| **W — weld** | inside `smart_decimate.py` | its own asserted invariants on the weld and on UV survival. `--no-weld` is not used |
| **C — cull ANDON** | inside `cull_unseen.py` | `--min-seen` / `--max-seen` floors on the fraction of faces any exterior camera sees, and its recession / missed-area bounds. Run at **tool defaults, unprofiled**, and the measured fraction is reported whether or not it fires |
| **T — twin contour ANDON** | inside `restylize_views.py` | `raise SystemExit` when the figure mask produces under 500 px of contour — keying failed. The exact mesh silhouette is supplied via `--masks`, so this gate is watching the supply, not the key |
| **V — venue** | this seat | any step other than the twin stage appearing to need cloud or a paid API |
| **X — credit** | this seat | a ninth executed cloud job, or any paid partner-API node appearing in a submitted graph |
| **0 — the sheet before the metrics** | this seat | **no number is quoted in the report until a `control \| mesh renders \| twin candidates \| provenance` sheet exists.** facet ran four arms and two gates once before building that sheet; when it finally existed the Director read the whole thesis off one panel |

**Not exercised here, recorded so its absence is not read as a pass:** `project_texture.py`'s
`--min-iou 0.80`. Projection is out of scope; that gate is **NOT RUN**.

## What the report must contain

Plate measurements first · predictions with blind/not-blind stated · Gate L, M, F, W, C, T
verdicts with evidence · the Gate 0 sheet path · then measured values beside predictions ·
the twin submissions with model ids, full payloads, seeds and control-input hashes · the
GPU-hours delta as a before/after difference · and a compensator line. **A gate that has not
run is written `NOT YET RUN`, never a plausible identifier with a verdict beside it.**

**No judgement words.** *Verified, works, proven, decisive, validated, shipped* do not
appear. The Director decides whether the mesh and the twins are what he wants; this seat
measures.

## Out of scope

Projection (`project_texture.py`, `project_twins.py`) · the inpainting brush · finalize/fill
· rigging and any armature-side work · the eight-view twin set · any LoRA · any partner API ·
`E:\AI\armature` (read-only) · the memory store (an executor does not write to it) ·
**pushing facet** (premise 14) · and re-litigating E32's `--min-iou` threshold, which is a
ruled matter and not this seat's.

---

## Amendment 1 — the density-allocation values, 2026-08-11, before the stage ran

The spec as written named the stage and not its numbers. `smart_decimate.py` takes a
**required** `--head-crop` and a `--target`, and neither can be inherited: the face rect is
"the single most subject-specific value in the pipeline" (`profiles/character.json`) and
`mesh_stats.py` itself **warned** that its default W3 rect covers **1.005×** this figure's
whole silhouette, so it cannot be measuring a face here. Both values are declared here,
before the stage ran, with their derivation:

| value | setting | derivation |
|---|---|---|
| `--head-crop` | **`438,44,588,182`** at `--crop-res 1024` | **DERIVED, not chosen.** Located **by eye** on two orthogonal `--clay` renders of this mesh (view 0 `108,84,245,207`; view 2 `114,85,222,210`, 352×1024, y from top), converted to one world box by `e12_head_evidence.py` — the committed instrument, found by enumeration rather than commissioned — then projected into `smart_decimate`'s own frame by its formula at `smart_decimate.py:192-193` with this mesh's `maxabs` 0.500952 and `--bound` 0.55. **Never by height**, per the raised-weapon rule |
| `--target` | **300,000** faces | **DECLARED, not measured.** F01 gate A3 asks for 200k–1.2M triangles; the raw reconstruction is 990,552 with a head/body median-face-area contrast of **1.016** — i.e. no allocation at all. 300,000 sits mid-band and leaves the protected head a real multiple under `--factor 3.0`. This is subject data with no profile to live in yet; it is recorded as a declared value so a later profile inherits a number that was written down rather than one that arrived by silence |
| everything else | tool defaults | `--factor 3.0`, `--body-weight 0.8`, `--pad-frac 1.5`, `--bound 0.55`, `--weld-dist 1e-5`, weld **on** (`--no-weld` is not used) |

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **2** | every stage is a recorded command with explicit args; the plate's sha256 is pinned; each cloud submission records model names, full payload, seed and control-input hashes. **Not 3** — no per-run lock file, the pipeline's own open P2, and the cloud side pins model *names* rather than weight hashes |
| ANDON_AUTHORITY | **3** | five of the nine gates live **inside** the tool performing the step and `raise` (L, W, C, T, and `e32_route_preprocess`'s alpha ANDON); E22/E23/E25 converted 278 sites in this repo from `assert` to `raise` precisely so `python -O` cannot delete them. The seat-level gates (M, F, V, X, 0) are order-of-work gates and are named as such rather than dressed as tool gates |
| NAMED_COMPENSATORS | **3** | **local:** every write is a new file under `E:\AI\training\facet_E33\`; compensator `rm -r E:\AI\training\facet_E33`, owner = this seat. The plate, `E:\AI\armature` and `E:\AI\facet`'s tree outside `docs/experiments/` are opened read-only. **cloud:** a submitted job's GPU-hours **have no compensator** — that is why the ceiling is stated before the first submission and why the arms are two views rather than eight. **repo:** commits are local and unpushed; compensator `git reset --hard c0031c1`, owner = this seat, and **no push means no irreversible publish exists to undo** |
| DECOMPOSE_BY_SECRETS | **3** | inherited Parnas-clean seams, unchanged by this experiment: reconstruction, weld/allocation, visibility classification, control construction (`restylize_views.py --emit-only` is exactly this standard — the one place that knows how to build a control, kept from being duplicated in a cloud submitter), and generation. What varies with the subject goes on the command line, not into the tools |
| UNCERTAINTY_GATED_HUMANS | **3** | the run **stops** at the twin candidates for a decision no measurement can make (which register is canon), and Gate 0 puts the sheet in front of the Director before any metric is read. The register arms are presented contrastively and unranked, with R3 labelled as having no precedent |
| EXTERNAL_VERIFIER | **1** | honestly weak, as this pipeline's scorecard has recorded since E32: the verifier is a different *kind* of check (geometric measurement + the Director's eye), not a different model family with the generator's reasoning hidden. **Not remediated here; named rather than inflated.** It carries the pipeline's existing P1 remediation and is not made worse by this experiment |

**16 / 18.** EXTERNAL_VERIFIER at 1 is the standing gap; every other score is argued from a
mechanism in this spec rather than from intent.
