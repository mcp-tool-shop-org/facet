# E37 — remake the performer: report

**Seat:** executor · **Opened:** 2026-08-15 · **Spend: 0 of 40 cloud jobs.** Nothing has
been submitted. The Stage-B blind bands are unwritten and unsealed, so nothing about the
twin candidates has been seen or set.

The dispatch is [E37-remake-the-performer-kickoff.md](E37-remake-the-performer-kickoff.md).
Reported per stage, as it requires. E36's superseded arms carry nothing into this arc — its
unsealed bands and its planned 0d are stood down, per
[E36-ruling.md](E36-ruling.md) Ruling 1.

---

## Task 0 — mechanics, zero cloud

### 1. Mechanics

| check | result |
|---|---|
| E15 ritual, scratch `--db` | **PASS** — all four legs, exit **0**; seeded question set **19 / 19**; determinism leg **BYTE-IDENTICAL** (12,562,432 bytes, both builds); leg 3 pointers **1,993 checked / 0 dangling**; **37 experiments**, missing none |
| VRAM watchdog | **ADVANCING** on two reads — heartbeat 02:59:27.640 → 02:59:40.679, its *content* timestamp moved with it, and the CSV grew 1,147,884 → 1,148,302 bytes. State `ok`, VRAM **6,498 of 32,607 MiB — 24,702 below the 31,200 ceiling**. Read as movement, never as the starter's exit code |
| manifest **A** `facet_E33` | **HELD** — 116 declared / 116 present, 0/0/0, 835,059,987 bytes; self-reference reported and not counted |
| manifest **B** `facet_E34` | **HELD** — 84 / 84, 0/0/0, 177,563,094 against declared 177,563,094 |
| manifest **C** eight subtrees | **HELD** — 7,312 files / 17,072,807,610 bytes, delta **+0 / +0** |
| manifest **D** `facet_E35` | **HELD** — 335 / 335, 0/0/0, 284,096,148 against declared 284,096,148 |

Manifest C reproduces the recorded per-subtree table to the file: `facet_next` 5,040 ·
`facet_E01` 156 · `facet_E02` 146 · `facet_E05` 129 · `facet_E06` 96 · `facet_E07` 51 ·
`facet_E08` 818 · `saltroad_bake_fix` 876.

**Premise 6 holds at open on all four gates.** The E15 figures differ from E36's recorded
run (12,423,168 bytes / 1,971 pointers) by exactly the two commits landed since — the E36
close and the E37 kickoff — which is what a growing record does.

#### 1a. Every receipt landed outside every protected tree, and the rule is now enforced rather than remembered

The E36 open halt's whole lesson is that a verify receipt must not be written into the root
being verified. Both receipts this task wrote live in `E:\AI\training\facet_E37\task0\`.

⚠ Two of the four gates have no manifest of their own — the eight subtrees are a
count-and-bytes census, and until now that walk has been re-derived inline each arc, which
is the same debt `tree_manifest.py` was committed to end. Gate C is therefore
`task0/e37_gate_c_subtrees.py`, which **calls `tree_manifest.walk` rather than a hand-rolled
`os.walk`**, so its population is defined by the same code that defines gates A/B/D —
including the `__pycache__` exclusion. It carries the receipt-destination guard as a
**hard `raise` checked over every root before the first one is walked**, so the guard cannot
depend on iteration order.

**Proven able to fire**, because a check that cannot fail is not a check:

| probe | result |
|---|---|
| `--out-json` aimed inside `facet_E07` | **ANDON fired**, exit **1**, and `Test-Path` on the target returns **False** — nothing was written into the protected tree |
| `--out-json` aimed at `facet_E37\task0\` | gate ran, **HELD**, exit 0 |

### 2. Premise 1 — the source plate, re-hashed

| | declared at dispatch | measured at this seat | |
|---|---|---|---|
| sha256 | `753383255718db7212b21007a24fce0d9a6a101cb352662459eec690d335e0dc` | identical | **MATCH** |
| bytes | 1,216,363 | 1,216,363 | **MATCH** |

**Premise 1 holds.** `E:\AI\armature\outputs\E07\concepts\00-directors-pick-clay-armature.png`,
mtime 2026-08-11 11:12:09. armature's tree was read and not written.

⚑ **Measured alongside, because Stage A depends on it and the dispatch does not state it:
the plate is 1328×1328, mode RGB — it carries no alpha channel.** By
[E29 Ruling](E29-clay-reconstruction-report.md) the reconstructor's own `pipe.run` resizes
to a 1024 max edge, **runs `rembg` where the input has no alpha**, and square-crops to the
alpha bbox. So every Stage-A candidate is segmented inside the reconstructor before any
geometry exists, and the plate's own framing is not what reaches the model. Recorded now
rather than discovered at a candidate.

### 3. Premise 4 — the three instrument anchors: **PASS, all three**

Premise 4 was carried **ASSUMED**; it is now **MEASURED**. Every comparison is at full
float precision against the stored values, never the console's two-decimal display.

| instrument | file | scope compared | result |
|---|---|---|---|
| **chroma-split / pale** | `facet_E35\diag\r2c_pale_vs_levers.py` | 6 arms × 6 keys + 2 init = **38 values** | **ALL BIT-IDENTICAL** |
| **register** | `facet_E35\diag\t2_register_all.py` | 10 candidates × 5 keys = **50 values** | **ALL BIT-IDENTICAL** |
| **census** | `tools/twin_despeckle.py --mode census` | **37,326 measured leaves** across all three published censuses | **ALL BIT-IDENTICAL** |

The rows the record quotes reproduce exactly: pale ladder **278 / 4.974137425231817** ·
**932 / 12.98626683052641** · **1220 / 19.677933844043622**; init `L_median
76.43347324089892`, `C_median 1.122575874414789`; register `reg_iou 0.9372`,
`median_chroma_Cstar 23.774`, `keyed_px 96217`; census totals **77 / 442 / 27** (s4),
**734 / 3929 / 84** (E2), **1147 / 4962 / 84** (F1).

The **chroma-split column** — the one E37 selects on — is the pale instrument's `C_in`:
recorded arm **23.24614779024321**, which is the published 23.25 at full precision.

#### 3a. The chroma-split instrument was ENUMERATED, not commissioned

[E35 Ruling 2](E35-ruling.md) says *"the detector gains a **chroma-split report column**"*,
and `tools/twin_despeckle.py` contains no such column — the phrase appears nowhere in it.
Read as a missing tool, premise 4 would have named a population member that does not exist
and Stage B would have commissioned one.

It exists. The **chroma-split instrument is the pale instrument**, and the split is the
`C_in` column reading which of the two pale signatures a twin carries — (i) chroma-collapsing
init-bleed against (ii) chroma-preserved lightening, the class the Director rejected. The
E35-F1 and E35-E reports quote it under exactly that name (*"pale C\* (chroma split)"*,
23.25 / 36.30 / 23.24). E36's 0f called the same tool "the pale instrument" and anchored it.
**One tool, two names in the record, no gap.** This is the repo's *enumerate the resource
before commissioning one* law, fired a fifth time and answered by reading.

#### 3b. ⚠ A live hazard in the two E35 instruments, named and worked around

**Both `r2c_pale_vs_levers.py` and `t2_register_all.py` default `--out-json` to
`E:\AI\training\facet_E35\diag` — inside a protected tree.** A flagless anchor run
overwrites a declared file and fires manifest D, which is the E36 open halt reproduced
exactly, one arc later, from the other direction. Every anchor this task ran passed
`--out-json` into `facet_E37\task0\`, and manifest D re-verified **HELD 335/335** afterward.

Recorded, not repaired: it is a default in two closed-arc instruments and the repair is not
this task's. The E36 halt's own still-open item — `tree_manifest.py`'s verify path accepting
an `--out-json` destination inside the root it walks, and T70 having no leg that fires on it
— is the same class and remains open.

#### 3c. The census anchor proves it can fail, in the same run

A comparison over 37,326 leaves that reports 0 differences looks identical to one that
compared nothing. So the census anchor constructs the discriminating case every time it
runs: it re-runs s4 at `--blob-max-px2 35` against a recorded 36 and requires the **same**
comparison to fire.

| | |
|---|---|
| differences detected by the same comparison | **174** |
| probe totals | count **75**, area **432**, largest 27 |
| published totals | count **77**, area **442**, largest 27 |

If that probe ever goes quiet the anchor halts itself. And the census instrument at HEAD is
**byte-identical** to the `tool_sha256` recorded inside all three published files
(`49b99bbc242c12e3509158a56b791ec0b6a5aff765732df72d3acd65e7c55842`), with the env matching
to the patch version (numpy 2.4.6 · scipy 1.17.1 · python 3.13.13) — so the anchor's silence
is the expected outcome and the probe is what makes the silence mean something.

### 4. Premise 7 — the stage-0 clay-ify weights, re-`Test-Path`ed

All three present on disk: `qwen_image_edit_2511_fp8mixed.safetensors` ·
`qwen_2.5_vl_7b_fp8_scaled.safetensors` · `qwen_image_vae.safetensors`. Premise 7 holds.
Nothing in round 1 uses them — concept variants are round 2, at the Director's word only.

---

## ⚠ FINDING — the recorded runner cannot ask Stage A's question

Reported before Stage A runs, because it is a premise of the dispatch rather than a result,
and because the law it lands under is this repo's own: *the eighth member of the
unit/population family is the premise you inherited from your own dispatch.*

Stage A is **six TRELLIS seeds on the source plate as-is**, and premise 2 frames candidates
as coming from *"seed and concept variation, never re-rolls."* Measured at the mechanism:

| | |
|---|---|
| `pipe.run` signature | `run(image, num_samples=1, **seed: int = 42**, …, pipeline_type=None, …)` — `trellis2/pipelines/trellis2_image_to_3d.py:489` |
| how the seed is applied | `torch.manual_seed(seed)` at line 537, immediately before conditioning and all three samplers |
| what the recorded runner passes | `pipe.run(img, pipeline_type=args.ptype)` — `_mesh_character.py:43`. **The seed is never passed** |
| `--seed` on the recorded runner | **absent** — its seven flags are `--image --out --ptype --decimation --texture --remesh --remesh_project` (+ `--probe`) |

**So every reconstruction recorded in this repo ran at seed 42, the library default**, and
the runner Stage A inherits is structurally unable to vary the one thing Stage A varies.

**Enumerated before commissioning**, this repo's most-fired law and its fifth instance in
two sessions — the previous four were `e12_offsurface.py`'s nine flags, a model already on
the rig, `--edge-absolute` already at `project_twins.py:103`, and §3a above:

| candidate runner | seed? |
|---|---|
| `E:\AI-Models\TRELLIS.2-repo\_mesh_character.py` (the recorded one) | **no** — calls `pipe.run` without it |
| `E:\AI\sprite-foundry\3d-prerender\mesh_character.py` (the productized sibling) | **no** — same call, `mesh_character.py:87` |
| `_retexture_character.py` | has `--seed`, but it drives the **texturing** pipeline, not image-to-3D |
| `app.py` / `app_texturing.py` | Gradio seed sliders, GUI-only — and a GUI session produces no recorded parameters |

**Nothing on this rig can ask the question.** This is the branch where enumeration says
*commission*, and the commission is bounded: the seed already exists one layer down, so what
is missing is a runner that passes it.

**The anchor target is exact, not approximate.** [E29 Ruling 5](E29-ruling.md) measured three
reconstructions of one input at one seed **bit-identical through `pipe.run()`** — divergence
begins only inside `to_glb`'s decimation. Both E29 inputs are still on disk at
`E:\AI\facet_scratch\clay_arm\` and both re-hash to their recorded values
(`minotaur_concept.png` 1,693,150 B / `29fc8b87…`; `minotaur_clay.png` 6,240,299 B /
`95f51935…`). So a seed-capable runner at **seed 42** must reproduce E29's recorded raw
counts **to the digit** — 2,081,716 v / 4,229,386 f (concept), 2,208,416 v / 4,430,096 f
(clay) — which tests the new runner's call path against the recorded one at the recorded
seed, with no noise floor needed at that stage.

### The commission, and what it measured

`tools/reconstruct_mesh.py` — the recorded call path value for value, with `seed=` added
and every recorded default passed **explicitly** on the command line (E29's own discipline,
so the pin sits in the invocation rather than in a default a later edit could move). T71
rides the same commit.

**The anchor, run through the tool at HEAD:**

| | |
|---|---|
| `--anchor clay`, seed 42 | **2,208,416 v / 4,430,096 f** |
| E29's recorded clay raw | **2,208,416 v / 4,430,096 f** |
| verdict | **IDENTICAL** — 109 s, OVERALL PEAK 3.4 GB, inside E33's recorded 103–141 s / 3.4 GB band |

The welded GLB reads **9 components** through the served `mesh_stats`, which is E29's
recorded shell count for the clay mesh; faces land 998,507 against E29's 998,988, a
**0.048%** gap sitting inside the measured ±0.27% `to_glb` floor. Raw stage exact, decimation
not — [E29 Ruling 5](E29-ruling.md) reproduced rather than assumed.

⚑ **Three further runs reproduced the same raw counts with three DIFFERENT GLB sha256s**
(36,362,604 / 36,337,020 / 36,612,112 bytes), which is E29 Ruling 5's own finding arriving
again from a new tool: the generative stage is bit-identical and `to_glb`'s decimation is
not. Those three runs were not planned — see the next section.

### ⚠ T71 caught a real defect in the tool, and the way it caught it was a second defect — mine

The decoy leg failed on its first run, and the failure was not the test's:
**`--anchor` overwrote `--image`.** `--anchor clay --image <decoy>` silently discarded the
decoy, read the recorded file, reconstructed it, and reported a **passing** anchor about an
input the caller never named. That is this repo's own recurring shape — *a number that
reproduces exactly can still be measured against the wrong object* — built fresh.

**And because the tool proceeded, three test legs each ran a full 4B reconstruction**
(~105 s, 36 MB of GLB apiece) while reporting only that the return code was 0. A test file
that can reach the model is a harness defect whatever else it proves.

Both repaired, in the same commit:

| defect | repair |
|---|---|
| `--anchor` resolved an ambiguity it should refuse | `resolve_input()` **ANDONs** on `--anchor` + `--image` together, naming the recorded input it would have used. `--image` is no longer `required`; one of the two is |
| the hash check needed a subprocess and a model to prove | factored to `check_anchor_input()`, tested directly against a decoy — no GPU, no subprocess |
| a leg could reach the model at all | every subprocess in T71 is budgeted at **60 s**; loading TRELLIS alone exceeds it, so a leg that ever reaches the model fails loudly instead of quietly spending a GPU |

**T71 went 391 s → 1.91 s**, which is the measurement that the legs no longer touch the
model. 38 tests: the seam proven with a spy pipeline across six seeds, the pre-tool call
shape run through the same assertion to prove that check can fail, both ANDONs firing under
`-O` and `PYTHONOPTIMIZE=1`, and the recorded defaults pinned so moving them is deliberate.

---

## ⚠ FINDING 2 — "mesh-pit shading" does not trace to the measurement it cites

Reported before Stage A screens anything, because Stage A's requirement 3 and its entire pit
screen are built on it.

The dispatch states: *"the pure-black dots are mesh-pit shading, in no texel of atlas or GLB,
unreachable by any texture work,"* citing **E35 task 0a**. Searched across the record, the
phrase **"mesh-pit shading" occurs in exactly two places** — [E36-ruling.md](E36-ruling.md)
line 16 and this arc's kickoff — and both cite task 0a.

**Task 0a does not say it.** Read verbatim, its closing words on this class are:

> **Mechanism: UNMEASURED.** Leading candidate is a UV landing in the atlas's unpainted gap
> (7,585,131 such texels)…  Named, not asserted; settling it needs a UV pass this task did
> not run.

And its own measurement at the six dot locations argues the other way:

| what task 0a measured at all six | value |
|---|---|
| **clay render** (untextured geometry, lit) | **bright, 177–219** |
| twin (the paint) | mid-tone terracotta 123–170, *"dark at none of them"* |
| E33-lit and E34-lit (textured renders) | **dark**, at near-identical values |

**A geometric pit darkens an untextured lit clay render, because that render is nothing but
geometry under a light.** These are bright there. The darkness appears only once the texture
is sampled — which is what task 0a's own leading candidate (a UV landing in the unpainted
gap) predicts, and it is a UV/atlas property rather than a shape property.

What task 0a **did** establish, and which stands: the value exists in no texel of the final
atlas (0 within L1 ≤ 12) nor the GLB's embedded copy, so **no twin-side change can reach
it** — the half of the dispatch's sentence that is measured.

**This is not overturned here and this seat is not ruling on it.** It is reported as an
inherited claim whose citation does not carry it, and it is **measurable for free**: the pit
screen runs the recorded performer mesh as a **positive control before any candidate**, and
refuses to report a zero on a candidate if it does not fire on the mesh whose defect the
Director rejected — *validate a metric against a rejected artifact before building an
experiment on it.* Whatever the control says is the evidence, and it costs no cloud job.

⚠ **What rides on it:** if the class is a UV/atlas-gap artifact rather than geometry, a new
mesh does not by itself remove it — every mesh gets UVs and an atlas with unpainted gaps
from the same `to_glb` — and a clean Stage-A screen would be true and beside the point.
Stated now so the Stage-A sheet is read for what it can show.

---

## Count surfaces and harness state

T71 adds 38 tests. Moved in this commit, in the corrected order (**pin edits → FULL suite →
collect → surfaces → census last**):

| | before | after |
|---|---|---|
| full suite | 1002 | **1040** |
| hermetic | 957 | **995** |
| artifacts gap | 45 | 45 (unmoved) |

All **16 T34-pinned surfaces** moved, plus the **seven translated READMEs** as a digits-only
edit — the E35 Ruling 5 precedent, translations left to the advisor's hands rather than
regenerated at an executor seat.

⚑ **Two surfaces move that no test pins**, found by measuring rather than by the sweep: the
README and SECURITY both state *"two tools of thirty-four open a socket"* and *"the 34
unpublished research scripts."* `tools/` root holds 39 `.py`, four of them published
`py-modules`, so the unpublished population is **35** with this commit's tool and the
socket-opening pair is still exactly two (`restylize_views.py`, `texpass_brush.py`). T34's
sweep keys on test-count vocabulary and cannot see a tool count, so this one is carried by
reading — named here because the next tool added to `tools/` moves it again.

The instrument census was re-emitted last: `corpus_files` 319 → 320, `test_files` 70 → 71,
and axis D +1 each on `e12_offsurface.py` and `tree_manifest.py` — **this report's own
citations**, which is the E28 self-reference family behaving exactly as its idempotency leg
promises. T41's axis-D leg FIRED on the stale census before the re-emit and passes after.

---

## Artifact homes

Everything this task wrote is under `E:\AI\training\facet_E37\task0\`:
`e15_scratch.db` · `e37_open_manifests_ABD.json` · `e37_open_manifest_C.json` ·
`e37_gate_c_subtrees.py` · `e37_0d_pale_rerun.json` · `e37_0d_register_rerun.json` ·
`e37_0d_census_anchor.py` · `e37_0d_{s4,e2,f1}_census_rerun.json` ·
`e37_0d_s4_probe_offbyone.json` · `e37_open_suite.txt`.

**No protected tree was written to.** No cloud job fired. No blind band is written or
sealed.
