# E37 Phase 3 + 4 — run through to a GLB: `performer_v4.glb`

**Seat:** executor · **Written:** 2026-08-15 · **Spend 58 of 80 — UNMOVED. Zero cloud jobs.**
Run at the Director's instruction *"run the whole process through to a glb without stopping"*,
which supersedes the Phase-3 halt and the Stage-D halt for this pass.

---

## 1. The candidate

| | |
|---|---|
| file | `E:\AI\training\facet_E37\phase2fire\stageD\performer_v4.glb` |
| bytes | **22,562,640** |
| sha256 | `4b7c612251639d1343a9fc15a5fc18246236b2df1bc6e93bdd038565bc33ccfd` |
| triangles | **299,976** — identical to the rejected `performer_v3`; geometry untouched |
| mesh / material / texture | 1 / 1 / 1 |
| generator | Khronos glTF Blender I/O v5.2.39 |

---

## 2. Phase 3 — the rule fired, harmonization ran, and it is NOT in the GLB

The Director's reference view was not given and he asked not to stop, so the rule was
**pre-registered before any number was seen** (`phase2fire/phase3_preregistration.md`):
harmonize if the repaired set's within-set register C\* spread exceeds Phase 1's recorded
**8.33**, against a **mechanical** reference — the view nearest the set median C\*.

**Measured through the same instrument as Phase 1**, repaired set: **spread 8.45**. The rule
fired. Harmonization ran, `mkl`, reference **v0** — *disclosed: v0 and v3 tie at 0.03 from
the median 29.06, separated only by floating-point noise; the tie-break to the lower index
was not pre-registered.* The transform reads **0.00 ΔE on v0 itself**, which is the identity
check.

**One amendment to my own pre-registration, with its reason**: it said whole-view against
whole-view; figure coverage varies **15.05%–25.81%** across these views, so a whole-*frame*
statistic encodes how much backdrop a view has rather than its wood tone. The transform was
scoped to the **figure**. Stated as an amendment rather than absorbed.

**The result, both halves:**

| | repaired | harmonized |
|---|---|---|
| within-set C\* spread | 8.45 | **2.11** |
| census total | 161 / 794 px² | **119 / 597 px²** |
| **drawn-feature contrast, head band, mean** | **25.77** | **21.52** |
| worst view (v6) | 41.83 | **19.13 (−22.71, a 54% loss)** |

**The numbers say it worked; the walk says it fades the face.** Feature contrast — head-band
median L\* minus the darkest 5% mean L\* — falls on five of eight views. And **the census
"improvement" is the same defect wearing a good number**: a dark-speck census and a drawn
face on pale wood are the same colour class ([Ruling 20](E37-ruling.md)), so a transform that
lightens all dark paint reads as −26% census while it is erasing brows.

**So harmonization is measured, reported, kept on disk at
`phase2fire/setA_harmonized/`, and NOT carried into the GLB.** The pre-registered rule
decided *whether to harmonize*; it did not price a cost in an identity-adjacent quantity,
and identity is the Director's, not a metric's. The GLB is projected from the **repaired**
set. If he wants the tighter wood, the single-variable next test is a chroma-only or
wood-masked match that leaves feature luminance alone — named, not run.

---

## 3. Phase 4 — the recorded chain, reproduced with the repaired twins

`perf_300k.glb → prep_bake (reused, not rebuilt) → project_twins → texpass_finalize → pack`

**Projection**, exit 0, the ruled invocation: eight `--view` args · `--step 45.0` ·
`--aspect 368,1024` · `--margin 1.204` · `--fit-axis height` · **`--bg-max-pct 100.0`** (the
E16 Ruling 4e withdrawal, passed explicitly) · **`--reg-iou-min 0.80`** · no era flags.

| quantity | **v4 candidate** | v3 rejected |
|---|---|---|
| **styled / REACHABLE** | **2,223,846 / 2,268,219 = 98.0%** | 2,221,222 / 2,268,219 = 97.9% |
| holes before fill | 194,768 | 197,392 |
| atlas variance, projection | **0.02626** | 0.03625 |
| atlas variance, after fill | **0.02996** | 0.03997 |

**reg-IoU per view — no floor fired:** 0.9097 · 0.9210 · **0.8228** · 0.8848 · 0.9060 ·
0.9435 · 0.9340 · 0.9470. Minimum 0.8228 against 0.80. Two diagnostic NOTEs (v2, v6 — keyed
bbox exceeding the silhouette, attributed to cast shadow), the same pair and the same
character as the recorded build; not halts.

**Fill**, surface-aware, both gates declared in the tool and both passed:

| gate | threshold | measured |
|---|---|---|
| median source distance | 3.0 triangle edges | **1.33** |
| share beyond 20 edges | 0.05 | **0.00346** |

Reported beside them, gated by neither: `mean_fallback` 0 (structural in surface-aware mode),
normal disagreement > 60° 28.08%, back-facing 21.02%.

**RGBA turnarounds** — eight frames, **none flat-255** (the tool's own end-of-run ANDON).
Opaque counts reproduce the recorded silhouettes **to the digit** (93,289 / 92,128 / 53,705 /
91,436), which is the check that the geometry did not move.

---

## 4. The render census, both builds through ONE instrument

| | count | area px² | largest |
|---|---|---|---|
| **v4 candidate** | **847** | **4,259** | 36 |
| v3 rejected | 1,322 | 5,195 | 35 |

Per view (v4): 144 · 116 · 49 · 83 · 100 · 146 · 82 · 127.

---

## 5. The walk, at 3× on the head band — content, no verdict from this seat

Walked at this seat before shipping, candidate against the rejected build side by side
(`diag_v3_vs_v4_head.png`, `sheet_gate0_v4.png`, `sheet_v4_head3x.png`):

- **Vertical seam banding runs down the skull on both builds.** It is a projection artifact at camera-owner boundaries, and the twin-side repairs do not address it. Its *character* differs by view: v0's and v6's hard central face split is reduced in v4; **v4's rear view shows more visible striping than v3's**. Present in both — inherited, not introduced, and not fixed.
- The drawn features read as **embossed relief** on the mesh rather than as flat paint, in both lit and flat renders.
- The **ears read as dark cavities** on the rendered asset, where the twins carry discs.
- The nose reads as a hard wedge in profile (v2, v6), as it does in the twins.

---

## 6. State

- **Spend 58 of 80, unmoved. Phases 3 and 4 are local and free — zero cloud jobs this pass.**
- Set A originals, `phase2/masks_v2/`, and the rejected `performer_v3.glb` are all untouched.
- Manifest gates HELD; every write append-only under `phase2fire/`.
- `prep_bake` was **read, never written** — the same directory the recorded build used.
- Nothing tuned. The one pre-registered rule that fired was followed, its cost measured, and the decision not to carry it into the GLB is stated with the number that drove it.

**The GLB is a candidate, not an acceptance.** Acceptance is the Director's eye at his zoom.
