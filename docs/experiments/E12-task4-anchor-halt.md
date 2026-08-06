# E12 handoff 3, Task 4.1 — ANCHOR 1c FIRED. Halt before the pair.

**Executor session, 2026-08-05.** `e04_frame_agree.py` halted at **1 differing px on view 5**
against its bound of 0. **Nothing was submitted. No credits were spent. No control image
exists** — the gate fires before `restylize_views --emit-only` in the driver, so it stopped
the run at the step it was placed to stop.

Reporting and halting per the executor rule (*"stop at every gate, never improvise past
one"*) **and** per the gate's own pre-registered readings, which send this case to a halt by
name.

---

## 1. What ran, and what it returned

```
E12_pair_geom.ps1   watchdog -> clay render -> silhouettes -> ANCHOR 1c -> (controls, NOT REACHED)
```

Watchdog **alive** before the GPU leg — heartbeat `2026-08-05T23:47:30.9035241-04:00`, age
1.9 s, pid 22324, ceiling 31200 MiB; VRAM 1984 MiB before, 1986 after. Reported either way
per the standing rule.

| leg | command | result |
|---|---|---|
| clay | `turn_render.py --glb prep_uv.glb --out clay --views 1,5 --clay --profile beast.json` | exit 0, 3.9 s. 8 profile values applied. `dragonclay_{1,5}.png` at 1792×1024 |
| silhouettes | `silhouette_masks.py --prep E12_prep --out masks --views 1,5 --profile beast.json` | exit 0, 2.0 s. 6 profile values applied. 726,671 verts / 986,814 tris; `v_ext 0.687934`, `h_ext 1.203885` |
| **anchor** | `e04_frame_agree.py --glb prep_uv.glb --masks masks --tag dragonclay --views 1,5 --aspect 1792,1024 --fit-axis width --margin 1.204` | **exit 2 — HALT** |
| controls | `restylize_views.py --emit-only …` | **NOT REACHED** |

```
[agree] fit-axis width  ortho_scale 1.206072  ->  h_ext 1.206072  v_ext 0.689184  frame 1792x1024
[agree] view 1: differing 0 px   (hit 490941, mask 490941)
[agree] view 5: differing 1 px   (hit 490942, mask 490941)  centroid shift [-0.0007, -0.0]
                                  hit bbox [1377, 853] vs mask [1377, 853]
[agree] ANCHOR 1c (geometry vs geometry, bound 0 px): worst 1 px -> *** HALT ***
```

**The GLB operand is `E12_prep/prep_uv.glb`**, not the raw reconstruction — `silhouette_masks`
reads `prep_uv.glb` by construction, and the precedent settled it on the other side too
(E08 armB rendered the character's turnaround from `prep_uv.glb`; E11 re-confirmed it
reproduces the recorded renders). The two meshes carry the same bbox to the digit and differ
by 3,477 verts / 11 faces — the seam splits from UV packing and the recorded 11-face
Blender/trimesh discrepancy (E12 Ruling 6f).

## 2. Which pre-registered reading this is — measured, not argued

E04 Ruling 10 wrote three readings into the tool's own docstring **before** any of them
occurred:

| reading | prescribed action |
|---|---|
| 0 px | anchor passes |
| **a few boundary px, uniform scatter** | **float edge-ordering at the silhouette; report and halt** |
| a structural offset | the gate's real prey; the fit-axis change needs review |

`tools/diagnostics/e12_agree_probe.py` (new, this session) decides between the lower two. It
grades nothing and lifts nothing — the gate's exit code stands whichever way it lands. Its
hypothesis was stated in its docstring before it ran: **the two implementations are not the
same arithmetic on the same numbers.**

```
silhouette_masks.py   normalises  v -> [x,-z,y] / max|v| * 0.5,  casts from -look * 2.0
e04_frame_agree.py    does NOT normalise,                        casts from -look * radius (3.005)
```

That is a uniform scale of **0.998186307466** which the mesh *and* the ray grid both carry,
so it cancels mathematically — and it does not cancel in float32, because the ray origins are
built at a different magnitude and round differently. (It is visible in the two tools'
printed extents: `h_ext 1.203885` against `1.206072`, whose ratio is exactly that scale.)

**Measured:**

| construction | view 1 | view 5 |
|---|---|---|
| the gate's own (unnormalised, ray-back 3.005) | 0 px | **1 px** |
| the same code on the **normalised** mesh (ray-back 2.0) | **0 px** | **0 px** |

The single disagreeing pixel is at **(x 636, y 498)**, and the probe measures it **touching
the silhouette rim** — 1 of 1 touching, 0 interior. Centroid shift −0.0007 px. Both bboxes
identical at 1377 × 853.

**Reading: this is the second row.** The disagreement lives in the gate's own third
construction, at one grazing-angle rim pixel, and vanishes when the two constructions are
made arithmetically identical. It is **not** a framing difference between `turn_render` and
`silhouette_masks`.

**That does not lift the halt, and I am not proposing that it should.** The prescribed action
for this row is *report and halt*, written by the advisor before the case existed.

## 3. The visual evidence — `E12_pair/AGREE_overlay.png`, full size

The geometry silhouette's rim drawn in red on the profile clay render, both views, at
1792×1024 each. The rim tracks the membrane scallops, every tail spine, the frill, the claws
and the wing-wrist spurs. The one disagreeing pixel is marked with a green cross on view 5.
**Look at it before ruling** — it is the artifact the metric is a number about.

Measured on those renders:

| | view 1 | view 5 |
|---|---|---|
| silhouette | 26.754% of frame, 490,941 px | 26.754% of frame, 490,941 px |
| bbox | 1378 × 854, x 182–1559, y 85–938 | 1378 × 854, x 232–1609, y 85–938 |
| rim | 12,649 px | 12,649 px |
| h-margin / v-margin | 1.3004 / 1.1991 | 1.3004 / 1.1991 |

The horizontal margin is **1.300, not the pinned 1.204**, and that is correct rather than
wrong: the frame was fitted to the **worst yaw (view 0, projected width 1.001721)** and these
two views project 0.960782, so they sit inside it with room to spare. The vertical margin
measures 1.1991 against 1.204 — sub-pixel bbox discretisation on a figure that spans
essentially the whole height extent (0.574746 measured against the mesh's 0.574309).

## 4. A structural fact this turned up, and it is not a defect

**Views 1 and 5 have byte-identical silhouette area and identical bbox dimensions, with the
bbox mirrored about the frame centre** — 182–1559 against 232–1609, and 1792 − 1 − 1559 = 232
exactly. That is not a coincidence and not a bug:

> **An orthographic silhouette from direction `d` and from `−d` is the same set of rays.** A
> ray along a line hits the mesh from one end iff it hits from the other, so opposed cameras
> return the same hit set, mirrored by the flipped right-vector.

So the eight eye-level cameras produce **four distinct silhouettes**, each appearing twice
mirrored: 0↔4, 1↔5, 2↔6, 3↔7. It was sitting in plain sight in `frame_00003.json`'s
`projected_width_per_view` (0 = 4, 1 = 5, 2 = 6, 3 = 7) and I read that file at pre-flight
without understanding it.

**Consequence, flagged not ruled:** anything that reasons about *silhouette* coverage per
view on this subject is counting four things, not eight. The **first-hit** coverage figures
(the 50.46% ceiling, the elevated-camera measurements) are unaffected — those ask *which
surface* is hit, and opposed cameras hit opposite faces. The relevant risk is narrower: a
future instrument that used silhouette area as a per-view weight would double-count.

## 5. Predictions scored — what is decidable now

| # | prediction | outcome |
|---|---|---|
| **F1** | `e04_frame_agree` returns 0 px on both views — PASS | **FALSIFIED.** 1 px on view 5, HALT. The gate I called the least likely to fire is the one that fired |
| **F2a** | silhouette 20–30% (view 1) and 22–32% (view 5) | **held** — 26.754% on both |
| **F2b** | **view 5 > view 1** | **FALSIFIED, and structurally so** — they are *exactly* equal, for the reason in §4. The prediction assumed the two views present different membrane area; orthographic opposition makes that impossible |
| F3 | contour > 20,000 px, Canny > contour | **NOT RUN** — the gate fired first |
| F4 | the `n_contour < 500` ANDON does not fire | **NOT RUN** |
| G1–G7, H1–H4 | the pair and the bands | **NOT RUN** — nothing generated |

Two falsifications of five decidable rows, and F2b is the more useful of them: it is a
property of the camera set this arc has been reasoning about for two sessions.

## 6. What the advisor is being asked to rule

Stated as a question, not a recommendation — the executor does not decide what a result
means.

1. **Does the 1 px lift, and on what grounds?** The prescribed action for this reading is
   *report and halt*, and that is what happened. Whether "float edge-ordering at one rim
   pixel, which goes to 0 when the two constructions are made arithmetically identical"
   clears the pair to run is the ruling's call, not this session's.
2. **Is the gate's bound pinned to the wrong thing?** Its docstring says it "compares two
   independent implementations of one convention and cannot pass by agreeing with itself" —
   true, and the measurement shows the price: at a bound of 0 px it is also asserting
   **float32 determinism across two constructions that are not arithmetically identical**,
   which is a stronger claim than "the framing agrees". This subject has 12,649 rim px per
   view against the galleon's smaller frame and simpler rim. **Reported as an instrument
   finding; not fixed, not re-tuned, and no threshold proposed** — proposing a bound while
   looking at the result it would judge is the retuning this repo forbids.
3. **Nothing else in the dispatch is reachable.** Tasks 4.2, 4.3 and 5 are all downstream of
   the control image, which is downstream of this gate.

## 7. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | `E12_pair_geom.ps1` is the run: every command, exit code, wall time and VRAM reading logged to `E12_pair/geom.log`; both profile bindings echoed with their value counts; the probe takes the same flags as the gate |
| ANDON_AUTHORITY | 3 | The gate fired and the run stopped **inside the driver**, before the control was built and before any submission — the check sits ahead of the irreversible step rather than beside it. No parameter was changed and nothing was re-run for a pass |
| NAMED_COMPENSATORS | 3 | New files only, all under `E12_pair/` plus one new diagnostic and two new docs. Undo = delete them. No spend, nothing irreversible attempted |
| DECOMPOSE_BY_SECRETS | 3 | Every framing value came from `beast.json`; the GLB operand decided from precedent and stated; no character or ship constant entered |
| UNCERTAINTY_GATED_HUMANS | 3 | The halt is handed up as a question with both readings measured and neither adopted; the overlay is staged full-size so the ruling is made on the artifact, not on the number |
| EXTERNAL_VERIFIER | 3 | Three independent constructions of one convention — `silhouette_masks`, the gate, and the probe's normalised re-derivation — and the probe *can* return "structural", which would have confirmed the gate rather than explained it |

---

**HALT.** Task 4.0 is banked (`75b9a02`). Task 4.1's clay renders, silhouettes and overlay
are staged at `E:\AI\training\facet_next\E12_pair\`. **No image was generated, no workflow was
built, no credit was spent.** The pair, the sidecar and the bands wait on the ruling.
