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

## Stage A — the control screen: the fork FIRED, and my prediction MISSED

The fork was pre-registered by the advisor at the Director's confirmation, **before the
control was rendered or screened**, and is transcribed with its reasoning in
`facet_E37/stageA_control_fork_preregistration.md`: *fires on the recorded mesh → the
screen gates Stage A; doesn't fire → screen demotes to diagnostic.* Either branch is
CONTENT, so it runs **once** and is not repeated.

**It fired.** The recorded performer geometry, eight views, lit clay against `--flat` clay,
figure bounded by the exact raycast silhouette:

| view | lit blobs | flat blobs | **geometry marks** | largest |
|---|---|---|---|---|
| 0 | 71 | 2 | **71** | 10 px² |
| 1 | 72 | 2 | **72** | 19 px² |
| 2 | 40 | 1 | **38** | 36 px² |
| 3 | 95 | 1 | **94** | 26 px² |
| 4 | 74 | 3 | **74** | 21 px² |
| 5 | 54 | 3 | **54** | 32 px² |
| 6 | 40 | 0 | **40** | 17 px² |
| 7 | 120 | 2 | **119** | 32 px² |
| **total** | 566 | 14 | **562** | **36 px²** |

⚑ **PREDICTION MISS, recorded as one.** This seat predicted **SILENT** (blind to any control
render, reasoning from task 0a's clay-bright measurement) and the control returned 562. The
prediction was wrong; **by the pre-registered rule the screen gates Stage A.**

### But it does not fire WHERE the rejected dots are — and that is a different claim

*A gate must test the operation's failure mode, not a proxy for it.* A lit-versus-flat
asymmetry appears on **any** faceted mesh under a light, so "the screen fires" and "the
screen sees the class the Director rejected" are two claims and only the second makes a
candidate ranking mean what a sheet would be read to mean.

Tested on entirely recorded operands, all four at 352×1024 sharing one camera, nothing
re-rendered: E34's `turn_final_flat/armflat_1.png` (where task 0a found the dots), E33's
recorded studio clay, **E36's flat clay of the same mesh**, and E34's geometry mask.

| | |
|---|---|
| recorded dots reproduced | **6 px** within L1 ≤ 12 of (11,9,8) inside the mask — task 0a's own count, to the digit, so the operand is right |
| locally dark under LIT | 8,514 px |
| locally dark under FLAT | **1 px** |
| lit-only (the screen's quantity) | 8,514 px in **110 components** |
| **recorded dots inside a lit-only mark** | **0 of 6** |
| **recorded dots within 3 px of one** | **0 of 6** |
| per-dot distance to the nearest mark | 20.4 · 4.5 · 5.4 · 16.0 · 24.5 · 23.8 px |
| **null model** — all 91,415 masked px | median **10.0** px, 9.31% at distance 0, 21.50% within 3 px |

**The dots sit farther from the screen's marks than a typical figure pixel does** (median
~18 px against the null's 10.0).

⚠ **Stated with its limits, because six is a small sample.** Under the null, 0-of-6-inside
has probability ≈ 0.56 and 0-of-6-within-3px ≈ 0.23, so this is **not** proof that the dots
avoid the marks. What it is: **no evidence whatever that the screen sees them**, on a test
that would have shown association had there been any.

**Read together with `flat = 1 px`**, the reading is that essentially all local darkness on
a clay render is shading, so the screen's count is a measure of a mesh's own **shading
relief** — a real property, useful for separating candidates, and **not demonstrated to be
the rejected class**. Finding 2's UV-gap candidate survives this test unweakened.

**Nothing is renegotiated.** The fork's rule stands as pre-registered and the screen gates
Stage A. This is recorded so the Stage-A sheet is read for what its ranking is: relief, at
the Director's eye, alongside identity and topology — and *a diagnostic and a gate are
different objects.*

## Stage A — six candidates, measured. **HALT for the Director's pick.**

Seeds pre-registered before any candidate existed
(`facet_E37/stageA_seed_preregistration.md`): 42 (the library default every recorded
reconstruction in this repo ran at), 770700, 987654, 424242, 770701 (the four the record
already names), and 1 (one from outside this record's vocabulary). Each built by
`reconstruct_mesh.py` from the pinned plate, then eight lit clay views, eight `--flat`
views, and eight exact raycast silhouettes.

### The seed moves the geometry — checked, because the ANDON cannot check it

`reconstruct_mesh.py`'s gate proves `pipe.run` *accepts* a seed. It cannot prove the seed
*changes* anything, and if some other source dominated, six candidates would be one mesh in
six files with every downstream number a comparison of a thing with itself.

| seed | raw verts | raw faces | GLB bytes | wall |
|---|---|---|---|---|
| 987654 | 687,457 | 1,381,656 | 36,269,164 | 109.2 s |
| 42 | 704,494 | 1,428,392 | 36,121,852 | 109.5 s |
| 424242 | 705,367 | 1,440,956 | 35,805,112 | 108.4 s |
| 770700 | 722,296 | 1,471,748 | 36,342,412 | 106.7 s |
| 1 | 735,086 | 1,488,292 | 37,653,084 | 108.9 s |
| 770701 | 755,384 | 1,533,380 | 36,955,356 | 109.2 s |

**Six distinct vertex counts, six distinct face counts, six distinct GLB hashes, one
verified source plate** (`image_sha256` identical across all six). Raw-face spread
**10.98%** — 40× the 0.27% `to_glb` floor, and the raw stage is deterministic per seed, so
the spread is seed-driven.

### The two screens, and they agree

| candidate | pit marks | largest | shells | non-man | pieces | sat ≥1% | in/out | gap p95/p5 |
|---|---|---|---|---|---|---|---|---|
| **987654** | **378** | 34 | **4** | **75** | **39** | **1** | **0.939** | **1.16** |
| 1 | 455 | 36 | 62 | 282 | 136 | 11 | 0.320 | 6.63 |
| 770700 | 476 | 32 | 66 | 706 | 273 | 13 | 0.119 | 6.75 |
| 770701 | 510 | 31 | 69 | 505 | 204 | 13 | 0.342 | 4.65 |
| 42 | 525 | 36 | 67 | 542 | 239 | 14 | 0.321 | 2.80 |
| 424242 | 565 | 32 | 51 | 324 | 147 | 13 | 0.341 | 1.31 |
| *CONTROL (old)* | *562* | *36* | *67* | *534* | *218* | *5* | *0.686* | *1.67* |

⚠ **The control row is not comparable on the count columns** and is printed only for the pit
screen's sake: it is the 300k **decimated prep** at 299,956 faces against ~990k raw
candidate faces, and it carries **165 boundary edges** where every candidate has 0 or 1.
Candidate-against-candidate is like-for-like; candidate-against-control is not.

Area-normalising the pit count changes no ranking (987654 563.5 marks/Mpx → 424242 872.9,
control 851.6), and the count correlates weakly with both face count (**r = +0.380**) and
figure area (**r = −0.386**), so it is not a proxy for either.

### Only one candidate's nested-wall reading is actually about a wall

The nested-wall test takes the two largest manifold pieces and asks whether the second is
nested in the first. That is a wall test **only when the second piece is a wall**:

- **987654**: inner/outer **0.939** (near-equal) with gap spread **1.16** (tight, uniform)
  — the signature of a genuine nested wall. `material_frac_of_outer` **13.93%**, so ~86% of
  the enclosed volume is cavity, wall gap **0.204% of height**, `boundary_edges` **0**.
- **every other candidate**: inner/outer **0.119–0.342** with spreads to **6.75** — the
  second piece is the largest *fragment*, and their `material_frac` describes a fragment
  inside a bbox, not a wall. Do not read those numbers as wall thickness.

⚑ **This is the first time the nested-wall leg has computed on a CHARACTER mesh in this
repo.** CLAUDE.md records it *declining* on all five character meshes ever tested, because
it needs a second manifold piece above 1% of faces and the largest ran 98.2–98.6%. On
987654 the second piece is 48.2%, so it ran — and returned a hollow double-walled shell,
which is E14 Ruling 3's finding **measured on this class rather than extrapolated to it**.
The open item CLAUDE.md flags is answered for this one mesh; the ruling is the advisor's.

### ⚠ The thing that must not be read off the topology table alone

**The subject is a jointed artist's mannequin.** On the plate the limbs are physically
separate segments meeting at ball joints. So a reconstruction returning limb segments as
**separate shells may be the faithful structure, and 4 shells may mean the joints were
fused into one continuous surface.** Seed 42's satellites sit in symmetric pairs at
limb-shaped positions and heights (±0.053 at z −0.082, ±0.071 at z −0.329, ±0.137 at
z −0.180, ±0.078 at z −0.484), which is what a segmented arm-and-leg set looks like in a
shell census.

At the torso zoom, all of 42 / 987654 / 770700 render the ball joints visibly. What differs
by eye is surface: **987654 carries visible vertical striation across the chest** where 42
and 770700 read smoother — the topologically cleanest candidate is not the smoothest-
surfaced one. That is a trade, it is exactly the kind of thing a metric cannot rule on, and
it is the Director's.

**No candidate is recommended here, and no pass bar was invented.** *Canon is not a taste
question to be routed around.*

### The sheets

Full size, at `E:\AI\training\facet_E37\stageA\sheets\`:

- `E37_stageA_front_vs_plate.png` — 10624×1354, the source plate beside all six front views
  and the old mesh
- `turn_seed{42,770700,987654,424242,770701,1}.png` and `turn_CONTROL.png` — 6016×1050
  each, eight views at full render resolution. Per-view brightness spread **1.03–1.07×**
  on every one, inside montage's own <1.20× gate, so no view is darkened by the orbiting-
  light bug
- `E37_stageA_torso_zoom.png` — plate against three candidates at 2× on the joint band

**HALT.** The pick is the Director's, on identity first.

### Resolution — **no round-1 pick; resolved to ROUND 2 at the Director's word**

His word, 2026-08-15: **"round 2, wood."** Grounds in [E37-ruling.md](E37-ruling.md)
Rulings 1–2, operational spec in the kickoff's Amendment 1.

**The cause explains this section's own two puzzles at once.** The source plate carries
**generator fingerprint-swirls** — concentric ridge whorls across chest, belly and thighs,
read at his zoom and confirmed at the advisor's read of the plate. The route's founding law
is unchanged — *reconstructors read surface noise as geometry* — so TRELLIS baked the
swirls into every round-1 candidate as **relief**, and all six share one plate. That is
what the chest striation above is, and it is a substantial part of what the pit screen's
378–565 marks are counting on every candidate, control included. **Picking from round 1
would pick the least-swirled swirl.**

It also coheres with the co-location result rather than contradicting it: a screen counting
plate-inherited relief is exactly a screen that would *not* land on the six recorded
pure-black dots. Two independent readings, one mechanism.

**Round 1 is not discarded** — its candidates, screens, sidecars and this section stay in
the record as the measured baseline round 2 is compared against, and the six seeds are
deliberately reused unchanged so the comparison is like-for-like. Spend remains **0 of 40**.

## Round 2 — the plate edit: three attempts, and the Director picks attempt 3

Ruled at [E37-ruling.md](E37-ruling.md) Ruling 1 / kickoff Amendment 1: edit the plate
locally with Qwen-Image-Edit-2511 to smooth, mark-free clay, same man / pose / framing,
up to three attempts, all shown beside the original, **halt at his identity eye before any
reconstruction**. The first submission fired the VRAM gate and its halt, disposition and
resolution are in [E37-round2-vram-halt.md](E37-round2-vram-halt.md).

One prompt across all three attempts; **`denoise` was the only variable**, and the negative
is the recorded clay-ify negative reused verbatim — its first term is already
*"engraved spirals"*, authored in `concept-prep.md` before this defect had a name.

| attempt | denoise | wall | ridge energy inside the figure — median / p95 | swirls at the chest zoom |
|---|---|---|---|---|
| *original plate* | — | — | *0.1571 / 7.8663* | *heavy concentric whorls* |
| 1 | 0.45 | 150 s | 0.1169 / 7.4035 | present, essentially unchanged |
| 2 | 0.65 | 110 s | 0.0962 / 6.5431 | present, slightly reduced |
| **3** | **0.85** | 110 s | **0.0756 / 3.7450** | **gone** |

⚠ The ridge-energy column is a **reported diagnostic and decided nothing** — it cannot
separate a removed swirl from a softened face, which is the exact trade `denoise` governs
and exactly the failure this repo spent four experiments learning (*a metric that cannot
separate an asset he rejected from one he accepted is not a metric*). It is printed because
it moves with the eye here, not because it ruled.

**The Director's word on the sheet: "attempt3 0.85 is the winner. The only one without the
fingerprints."**

### The approved plate, pinned

| | |
|---|---|
| path | `E:\AI\training\facet_E37\round2\e37_attempt3.png` |
| sha256 | `a4bcf2501414f769d4164ba910803f6d7882e98747897f5f256be801c75fb3b2` |
| bytes / frame | 866,642 · **1328×1328 RGB** |
| recipe | Qwen-Image-Edit-2511 fp8mixed · denoise 0.85 · 40 steps · CFG 4.0 · seed 42 · shift 3.1 · euler/simple |
| from | source plate `753383255718…`, verified at submission |

**It carries no alpha, exactly as the original did**, so `rembg` runs inside `pipe.run` for
round 2's candidates on the same terms as round 1's — the comparison stays like-for-like,
which is the whole reason the seed set is unchanged. The full recipe, the validated graph
and both VRAM readings are in `round2/e37_attempt3.json`; attempts 1 and 2 stay in the
record with their own sidecars as the measured rungs either side of it.

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
