# E36 — Task 0 report: mechanics, the flat init, and the instrument anchors

**Seat:** executor · **Date:** 2026-08-15 · **Spend: 0 of 15 cloud jobs.** Nothing has been
submitted. Blind bands are unwritten and unsealed.

Task 0 as specced in the [E36 amendment](E36-route-arms-kickoff.md): mechanics, then **0d**
(the structural anchor, 1 job), **0e** (the flat-init render, zero cloud), **0f** (instrument
anchors, zero cloud). **0d has NOT been run** — see §5.

---

## 1. Mechanics

| check | result |
|---|---|
| E15 ritual, scratch `--db` | **19 / 19**, all four legs, exit **0**; determinism leg **byte-identity** (12,423,168 bytes, both builds); leg 3 pointers 1,971 checked / 0 dangling |
| VRAM watchdog | **ADVANCING** on two reads — 01:29:57 (998,945 B) → 01:30:21 (999,717 B), status `ok`, VRAM 7,018 of 32,607 MiB, 24,182 below the 31,200 ceiling. Not the starter's exit code |
| manifests A / B / C | **HELD** at open — see [E36-open-manifest-halt.md](E36-open-manifest-halt.md) |
| manifest D | **FIRED**, then **HELD** after the Director's ruling — same document, §8 |

## 2. 0e — the flat-lit init

### 2a. The recorded invocation was not in the record. It is now, and it is proven.

The amendment says *"the recorded invocation (recorded script, recorded frame 352×1024)."*
No such invocation is written anywhere in this repo or the training trees — and this is not
a new gap: **E34's own report says of the sibling call, *"E33's `turn_final` was made by an
invocation this arc never recovered."*** The repo's standing law applies as written — *a
recipe that does not reproduce its output is not a recipe.*

Rather than guess, the invocation was reconstructed and then **anchored against the recorded
artifact before being used for anything**:

```
blender -b -P E:\AI\training\saltroad_bake_fix\tools\turn_render.py --
        --glb E:\AI\training\facet_E33\prep_300k\prep_uv.glb
        --out <dir> --tag <tag> --views 1 --w 352 --h 1024 --clay
```
(`--exposure` 0.85 and `--yaw-offset` 0.0 at their defaults; the `saltroad_bake_fix` copy,
which E33's premise table records as the one used, and which differs from
`tools/verify/turn_render.py` — 279 diff lines, no `--bg`/`--fit-axis`/`--margin`, no
`subject_profile` binding, default `--w 757`.)

Two facts pinned the inputs rather than assumption:

- **Which mesh.** `facet_E34/twin_control/armclay_1_mask.png` is **byte-identical**
  (`2e57a82c…`) to `facet_E33/masks_300k/armclay_1.png`, so the route ran on the **300k**
  prep. `prep_300k/prep_uv.glb` and `performer_300k.glb` are the same file (`2a740e3f…`).
- **Which render.** The reconstruction reproduces `facet_E33/turn_clay_300k/armclay_1.png`.

**Anchor result — the reconstruction against the recorded clay:**

| | |
|---|---|
| pixels differing | **0 of 360,448** (0.000000%) |
| max abs channel delta | **0** |
| alpha differing | 0 · RGB differing 0 |
| file sha256 | `6812d7dd…` recorded vs `fa938a14…` new — **DIFFERENT** |

⚠ **The bytes differ and the pixels do not.** This repo's own law — *a PNG hash mismatch is
not evidence a render changed* — firing live; a byte comparison here would have produced a
false halt on a pixel-perfect reproduction. Third recorded instance.

### 2b. Premise 5 — and two checks that could not fail

Premise 5: *"The flat-lit clay render changes shading only — silhouette byte-equal to the
recorded mask,"* to be proved *"via `silhouette_masks --anchor` (0 differing px)."*

⚠ **That leg cannot fail on this premise.** `silhouette_masks.py` loads `prep_uv.glb` and
raycasts it (`tools/silhouette_masks.py:89`); **the clay render is not an operand.** A
lighting change cannot move its output, so the gate returns 0 whatever the render does. It
is a real check of the mesh and camera convention and it is not a check of premise 5.

⚠ **And my own first replacement was no better.** I compared the two renders' alpha channels
and got 0 differing. Alpha is **255 across the entire frame in both** — `recorded area
360,448 / flat area 360,448`, the whole image — so that comparison was also structurally
incapable of failing. Recorded because the repo's instruction is to ask what a non-zero would
have required, and here nothing would have produced one.

**What is actually true**, tested against the geometry mask (91,415 px, 25.36% of frame):

| | |
|---|---|
| RGB moved inside the raycast mask | **91,415 of 91,415** — the whole figure re-shaded |
| RGB moved outside the mask | **4,279** — the background field itself changed value |
| recorded background | ~`127,127,130`, 193 unique values |
| flat background | ~`154,154,156`, 85 unique values |

The silhouette is identical **by construction** — same GLB, same camera, proven by the §2a
anchor — not because a comparison found it so. Neither render carries an alpha-separated
figure, so there is no silhouette in the file to compare.

### 2c. ⚠ FINDING 1 — `--flat` moves the CONTROL as well as the init

`restylize_views.control_image()` is `max(canny, contour)`. The **contour** term is the
mask's morphological gradient and is pinned. The **canny** term runs `cv2.Canny` on the
render itself, so it is a function of the lighting.

The control path was **anchored first** — the recorded clay + recorded mask rebuild
`facet_E34/twin_control/armclay_1_control.png` at **0 of 360,448 pixels differing**, 13,991
lit px both sides — so the reading of the path is proven before any delta is quoted.

| control, same mask, same parameters | canny px | contour px | control px |
|---|---|---|---|
| recorded STUDIO clay | **7,824** | 10,987 | **13,991** |
| new FLAT clay | **4,702** | 10,987 | **10,987** |

- contour term differing: **0** — pinned, as its docstring promises
- canny term differing: **7,968**
- control total differing: **3,004** = **21.47%** of the recorded control

**Read the flat row: control px 10,987 equals contour px 10,987 exactly.** Under flat light
every canny edge falls inside the contour band and **the canny term contributes nothing** —
the flat control is pure silhouette, carrying no interior edge information at all.

This is the confound law already in CLAUDE.md, at a new site: *"'One variable' is a property
of the dependency graph, not of the parameter you edited… Before running an arm, trace what
the parameter feeds and pin the consumers you did not mean to vary."* Arm 1 as specified
changes **node 9 (intended) and node 10 (not intended)**, and the record already names what a
control carrying nothing does — *gold plates gone, boots to fur, wine-red to green* — which
is the documented identity-loss signature, and it would be inseparable from the init's own
effect.

**Not decided here.** The law's own remedy is to pin the consumer — submit arm 1 with the
**recorded** control (`ae1bab6f…png`, already uploaded), leaving node 9 as the single delta.

### 2d. ⚠ FINDING 2 — the unique-colour guard condemns the recorded baseline, and its remedy does not clear it

The guard: *"below the clean family (~5,000), one lanczos round-trip per the E35-measured
repair."*

| init | unique RGB | after one lanczos round-trip |
|---|---|---|
| **recorded STUDIO init — the route's own baseline** | **2,303** | 3,958 |
| new FLAT init | **107** | **342** |

Two measured problems:

1. **The threshold condemns the artifact that produced the accepted result.** The recorded
   init is 2,303 — below 5,000 — so the guard as written fires on the baseline itself and
   cannot discriminate the new init from the known-good one. The ~5,000 clean family was
   measured on **2509** flat renders, and 2509 is explicitly out of E36's scope; the recorded
   qwen-image route demonstrably runs at 2,303. This is the wrong-population family.
2. **The prescribed repair does not work at this magnitude.** 107 → **342** is still ~15×
   below the threshold it is meant to clear. The round-trip is also not free: it perturbs
   **8,413 px inside** the mask and **13,990 outside**.

Both numbers are reported as the amendment requires. **No disposition taken.**

## 3. 0f — instrument anchors: PASS

Both instruments re-run against every published row and compared at **full float
precision**, not the two-decimal console display.

| instrument | rows | values | result |
|---|---|---|---|
| pale (`r2c_pale_vs_levers.py`) | 3 ladder rungs + init | **20** | **ALL BIT-IDENTICAL** |
| register (`t2_register_all.py`) | 10 candidates | **50** | **ALL BIT-IDENTICAL** |

The three ladder rungs the amendment names reproduce exactly: **278 / 4.974137425231817** ·
**932 / 12.98626683052641** · **1220 / 19.677933844043622**; init `L_median
76.43347324089892`, `C_median 1.122575874414789`. The recorded register row reproduces at
`reg_iou 0.9372`, `median_chroma_Cstar 23.774`, `keyed_px 96217`.

⚠ **One invocation defect, mine, recorded rather than hidden:** the published label
`2d fused K=3` contains `=`, and the instruments' own `LABEL=PATH` parser splits on it, so
the first register run aborted on that row with `OSError` **after** printing nine correct
rows and before writing its JSON. Re-run with the label `2d fused K3` and mapped back in the
comparison. The instrument is not at fault; the row reproduces bit-identically.

## 4. Artifact homes

Under `E:\AI\training\facet_E36\`: `0e_anchor/` (the proving render + a round-trip probe),
`0e_flat/` (the arm-1 init and its round-trip), `0f_anchors/` (both anchor JSONs, the open
manifest receipt, and the three comparison scripts). **Every receipt this session wrote
landed outside all protected trees** — the lesson of the open halt, applied.

## 5. 0d — NOT RUN, and why

0d is arm 2's structural anchor and costs the arc's first job. It is **unaffected by
either finding above** — those are arm-1 (init-side) findings, and arm 2 varies the control
graph.

It is not run because the amendment's order binds: **blind bands are sealed by commit before
anything spends**, and the bands cover all arms. Two of arm 1's specified terms — what its
control is, and what the colour guard binds — do not survive contact with measurement, so
writing bands around arm 1 now would seal predictions about an arm whose definition is
open.

The recorded payload is read and understood; the transform for 0d is known
(`payload_r3_v1.json`, sha256 `5cd0464d…`: node 9 init, node 10 control, node 11
`ControlNetApplyAdvanced` at strength 0.9 / 0.0 / 1.0, node 13 KSampler seed 770700, steps
20, cfg 2.5, euler/simple, denoise 0.92, node 6 shift 3.1 — every value matching the
amendment).

**Halted for the two arm-1 rulings. Zero spent.**
