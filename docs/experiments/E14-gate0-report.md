# E14 Gate 0 — three longsword clays, three meshes. HALT: the Director designates.

**Executor session, 2026-08-07.** All three staged concepts reconstructed locally, welded,
measured with no `--profile`, rendered `--clay` beside their source at full size, and given a
hilt-region measurement derived per mesh. **`gate_mesh.py` did not run**, per the dispatch:
subject instruments are profile decisions and `profiles/prop.json` does not exist.

**This document ranks nothing.** Which sword is *the* sword is an outcome call and it is the
Director's. Rejecting all three is a legitimate outcome. Three sheets, three hilt crops and
the numbers below are staged, and I am stopping.

Predictions were committed **blind** in [E14-gate0-predictions.md](E14-gate0-predictions.md)
(`a4d587a`), before any longsword mesh existed. **Seventeen of twenty-five held; eight were
falsified**, and one that held was worded wrongly and is corrected below. §12 scores every one.

**The headline is not about longswords.** The most consequential measurement in this session
is that **every reconstruction this route has made — including the designated, accepted
dragon — is a hollow double-walled shell, not a solid.** It was found while chasing a
sword-specific anomaly, and the control is what turned it into a route-wide fact. §4.

---

## 0. Two deviations from the dispatch, declared before any result

**a. `e14_topology.py` is in `tools/diagnostics/`, not under `E14_gate0/`.** The dispatch's
compensator line says "new files only, all under `E14_gate0/`". E12 made the same call and
argued it: an instrument outside the repo cannot be re-run by the next session from a clone.
That argument was demonstrated rather than asserted this session — three of E12's instruments
(`e12_frame.py`, `e12_head_evidence.py`, `e12_nonmanifold.py`) were reused here unmodified,
which is exactly the benefit. **The compensator's purpose is fully honoured either way**: it
is a new file, and nothing pre-existing was opened for writing anywhere in this session.
Neither E12 deviation was explicitly ruled on, so this is practice, not precedent — the
advisor may want to settle it.

**b. The hilt box was located from a STRUCTURAL LANDMARK, not read by eye off a grid — and
that costs a real check.** The dispatch says "locate the hilt by eye from the clay renders."
I instead scanned each mesh's own x-extent against height, found the **quillon flare** (the
global maximum of horizontal width) and the **blade shoulder** immediately below it (the local
minimum), and took the hilt as everything above that shoulder. The dispatch's *rule* — "do not
locate it by height, the pose is the accident" — is what this obeys: the quillon flare is a
structure, and the height it sits at is read off it rather than assumed.

**The cost, stated plainly.** `e12_head_evidence.py` carries an ANDON that halts when two
independently-read views disagree about the region's Z range. E12's readings disagreed by
1.76% / 0.59% / 0.00% of height — a real cross-check that could have fired. **Mine cannot
fire**: both pixel boxes were projected from one world Z range, so the tool reports 0.0000
disagreement *by construction*. That is a check that cannot fail, and this repo's law says to
name it rather than bank it. **The compensating check is the overlay**: the box was drawn back
onto all eight views of each mesh (`boxed_0000N/`) and looked at, and on all three it contains
pommel, wrap and quillons and excludes the blade below the shoulder.

---

## 1. Environment, reported before the GPU work rather than after

**The watchdog was verified alive immediately before the GPU leg and again after it.** At
session start the heartbeat was **0.0 s old against a 15 s threshold**; at the end of the
session, 2 s. No `_watchdog_DEAD`, no `_watchdog_TRIPPED`, at either check. Heartbeats are
recorded in `recon.log` at start and after each mesh: 02:51:11 → 02:53:53 → 02:56:15 →
02:57:55, i.e. live and advancing across the whole reconstruction window. The newest entry in
`_watchdog_KILL.log` is a `watchdog up` line from 2026-08-06 15:42:54; **nothing fired today**.

**The `trellis2` PYTHONPATH repair from E04 was still required** and is written into the runner
with its reason.

**E12's two-backend refinement reproduced exactly**, on all three meshes:

```
[SPARSE] Conv backend: flex_gemm; Attention backend: flash_attn     <- ignores SPARSE_ATTN_BACKEND
[ATTENTION] Using backend: sdpa                                     <- honours ATTN_BACKEND
```

**The seed is recorded from the pipeline's own printed signature**, not asserted:
`run(image, num_samples: int = 1, seed: int = 42, ...)`. The tool exposes no seed flag, so all
three ran at seed 42.

**One thing the log settles that was previously inferred.** `mesh_character.py` prints
`decim=1000000` on every run. The 900k–1,000k face counts across all twelve reconstructions
this route has made are a **decimation target**, not a subject property — which is what
prediction P3 guessed and is now read directly off the log rather than from the pattern.

**A VRAM baseline difference worth recording.** `nvidia-smi` read **3,739–3,783 MiB** before
and after every mesh, against E12's 1,866–1,896 MiB two days earlier. The desktop baseline on
this rig is ~1.9 GB higher than it was; the reconstruction still peaked at 3.4 GB and never
approached the 31,200 MiB ceiling.

## 2. The runs

TRELLIS.2 `1024_cascade`, local, watchdog verified.

| candidate | source | out | `TOTAL` | shell wall | `OVERALL PEAK` | exit |
|---|---|---|---|---|---|---|
| 00001 | `longsword_clay_p1_00001_.png` | `longsword_00001_raw.glb` 39.2 MB | **135 s** | 161.2 s | **3.4 GB** | 0 |
| 00002 | `longsword_clay_p1_00002_.png` | `longsword_00002_raw.glb` 36.1 MB | **136 s** | 142.0 s | **3.4 GB** | 0 |
| 00003 | `longsword_clay_p1_00003_.png` | `longsword_00003_raw.glb` 36.2 MB | **96 s** | 101.9 s | **3.4 GB** | 0 |

```
mesh_character.py --image <clay> --out <glb> --ptype 1024_cascade
  PYTHONPATH=E:\AI-Models\TRELLIS.2-repo  HF_HOME=E:\AI-Models\hf-cache
  ATTN_BACKEND=sdpa  SPARSE_ATTN_BACKEND=sdpa   (see §1 — only the SPARSE one is ignored)
```

`TOTAL` is the pipeline's own figure, comparable with E04's 116–141 s and E12's 103–135 s. The
shell wall exceeds it by 26 s on the first mesh and ~6 s on the others — a cold model load
(`[load] 69s` on mesh 1), not subject cost. **Peak VRAM was 3.4 GB on all three, the lowest
and flattest the route has recorded**, against the dragon's 3.4–3.8 and the galleon's 4.4–5.6.

## 3. `mesh_stats` — measured identically on all three, **no `--profile`**

No profile was passed, on purpose: `prop.json` does not exist and the no-profile path is
`subject_profile.bind`'s byte-identity path. Welding happens inside `mesh_stats`
(`merge_vertices(merge_tex=True, merge_norm=True)`), which reports the unwelded count beside
the real one.

| | **00001** | **00002** | **00003** |
|---|---|---|---|
| faces | 999,474 | 948,328 | 951,850 |
| verts | 499,609 | 474,308 | 475,704 |
| **shells (welded)** | **1** | **331** | **2** |
| largest shell | **1.000000** | **0.481049** | **0.999973** |
| shells (unwelded) | 46,496 | 43,861 | 40,298 |
| watertight | False | False | False |
| extent (Blender x, y, z) | **0.2262**, 0.0634, 1.0020 | **0.3590**, 0.0868, 1.0020 | **0.2985**, 0.0797, 1.0019 |
| **widest horizontal / height** | **0.2258** | **0.3583** | **0.2980** |

Blender convention, spelled out because every world quantity in this report is in it: **x** and
**y** are the two horizontal axes, **z** is height. The widest horizontal axis is **x** on all
three, and it is the quillon span.

**These are the route's first portrait subjects**, and by a wide margin: character ~0.46–0.72,
galleon 1.04–1.11, dragon 1.61–1.74, longsword **0.226–0.358**.

### ⚠ `mesh_stats` printed NO warning on any of the three, and that silence is a finding

The dispatch anticipated the front-view-rect warning and asked for it to be quoted. **It did
not fire.** Its condition is `vertical extent is not the largest`, and on a sword standing on
its tip the vertical extent **is** the largest — `up_axis_dominant: true` on all three. So the
character instrument did **not** notice it was not looking at a character, where on the ship
and the dragon it did.

The number that would have caught it is in the same JSON: **`rect_frac_of_figure` reads 1.903 /
1.449 / 1.466** — the "face rect" covers 145–190% of the figure's own projected area. A rect
larger than the whole figure cannot be a face.

This is the repo's own law arriving in a new costume — *test the property, not a geometric
proxy for it*. "Is the vertical extent the largest" is a proxy for "is this a character", and a
standing prop passes the proxy. `face_rect_faces`, `face_rect_density`, `face_curvature_var`
and `curv_radius` are therefore **not quoted anywhere in this report**, exactly as the dispatch
requires — but on this subject class that exclusion rests on the dispatch's judgement rather
than on the tool's own warning. Reported, not fixed: changing a shared instrument's warning
condition is not this session's call. (`median_tri_cells` came back 0.257 / 0.264 / 0.253, all
below the tool's 1.5 threshold, so its second warning did not fire either.)

## 4. THE HEADLINE — every reconstruction on this route is a hollow double-walled shell

This was not something the dispatch asked for. It surfaced because 00001's manifold-adjacency
graph split almost exactly in half, which looked like a sword-specific defect; the control is
what turned it into a route-wide fact.

### What was measured

A **ray-crossing count**, subject-independent and implemented directly (trimesh's own
proximity and ray paths need `rtree`, which is not installed on this rig). For 300 rays per
mesh, fired along each mesh's own thinnest axis through points inside its silhouette, count the
surface crossings and record the gaps between consecutive ones. **A solid member gives two
crossings. A hollow one gives four: wall, cavity, wall.**

| mesh | median crossings | rays with ≥4 | **wall gap** median (p5) | cavity median | cavity / wall |
|---|---|---|---|---|---|
| longsword 00001 | 4.0 | 93.8% | **0.00226** (0.00197) | 0.01760 | 7.8× |
| longsword 00002 | 4.0 | 93.3% | **0.00232** (0.00196) | 0.01887 | 8.1× |
| longsword 00003 | 4.0 | 89.6% | **0.00223** (0.00196) | 0.02133 | 9.6× |
| **CONTROL dragon 00003** — *the designated, accepted beast* | 4.0 | 97.1% | **0.00313** (0.00213) | 0.02859 | 9.1× |
| **CONTROL galleon 00004** | 8.0 | 95.0% | **0.00338** (0.00145) | 0.09024 | 26.7× |

The cross-section scan agrees on the swords independently: at every height from 20% to 60% of
the figure, a ray through the blade crosses **four** surfaces in two tight pairs —
00001 at y = −0.01131, −0.00934, +0.00755, +0.00952, i.e. **walls of 0.00197 around a cavity of
0.0169**. Same on 00002 (0.00196) and 00003 (0.00196).

Independently again, on the two swords where the inner wall is a separate manifold piece, the
**signed volumes** settle the nesting: 00001 reads outer **+0.001603** and inner **−0.001228**
— a negative enclosed volume is an inward-facing wall — leaving **0.000375 of material, 23.4%
of the outer envelope**. 00002 reads +0.002465 / −0.001014, material 58.9%.

### What it means, and what it does not

**Hollowness is a property of TRELLIS.2 `1024_cascade` as run here, not of the longsword.** The
dragon shows the same four-crossing double wall. The wall gap's **p5 floor is 0.00196–0.00213
on every mesh measured, including both controls** — a hard floor, not a distribution.
Against a bounding box of ~1.00, one voxel of a 1024³ grid is 0.000977, so **the floor is
almost exactly two voxels**. That is offered as a hypothesis with its arithmetic, not as a
ruling: this session did not open the extractor.

**Two limits on the control, stated so the number is not over-read.** On a shape that is not
slab-like, four crossings can mean *two solid members* rather than *one hollow member* — a ray
through a dragon can hit two limbs. What survives that objection is the **wall gap**: two
separate limbs would be separated by an arbitrary distance, and the measured pairs cluster at
0.002–0.003 with a hard floor. The galleon's median of **8** crossings is the rigging, and its
cavity figure is correspondingly uninterpretable; its wall gap is not.

**What is genuinely sword-specific is not the cavity but how the inner wall ATTACHES.** All
three swords are hollow; they differ in whether the inner wall is topologically joined to the
outer, and that is what §5 is about.

## 5. Topology — boundary, shells, and what 00002's 331 components actually are

| | 00001 | 00002 | 00003 |
|---|---|---|---|
| unique edges | 1,499,090 | 1,421,451 | 1,427,524 |
| **boundary edges (1 adjacent face)** | **0** | **0** | **0** |
| total boundary length | **0.00000000** | **0.00000000** | **0.00000000** |
| **non-manifold edges (>2 faces)** | **121** (0.0081%) | **1,040** (0.0732%) | **251** (0.0176%) |
| shells (shared-vertex, = `mesh_stats`) | 1 | 331 | 2 |
| pieces (shared-manifold-edge) | 3 | 897 | 50 |

**Zero boundary edges on all three.** Not one, not one of zero length — none. **There is no open
sheet and no open puncture anywhere on any of the three**: an open hole in a surface makes a
boundary loop, and there are no boundary edges to make one from. This is the cleanest result of
its kind the route has recorded (E12's dragons carried 1 / 0 / 1, the galleon 23 totalling
0.0175 in length).

### ⚠ "Shells" has two definitions and they disagree by a factor of hundreds

This report's first draft of `e14_topology.py` reported **"3 shells" for 00001, whose shell
count is 1**. It was thrown away rather than published, and the reason is worth recording
because the instrument now carries it in its docstring.

- `mesh_stats.vertex_components` counts components joined by a **shared vertex**. Every shell
  number in the family table — character 40–191, ship 237–512, dragon 9–12 — is that quantity.
- `trimesh.graph.connected_components(m.face_adjacency)` counts components joined by a **shared
  manifold edge**, and that graph *excludes every non-manifold edge*. On 00001 it has exactly
  1,499,090 − 121 rows, and dropping those 121 edges splits the mesh into two pieces of 521,134
  and 478,288 faces that share only 10 vertices.

The two are the outer and inner walls. They are one shell because they touch, and two pieces
because they touch only at 121 pinches. **Both are now computed, named differently, and only
the vertex quantity appears in the stats table.** The repo's law — a number that reproduces
exactly can still be measured against the wrong object — is what caught it.

### 00002's 331 components are its inner wall, in fragments

Enumerated: the largest component holds 456,186 faces (48.1%), and the two largest satellites
are **248,138 faces spanning 0.147 × 0.027 × 0.715 centred on the blade** and **191,672 faces
spanning 0.355 × 0.083 × 0.318 centred on the hilt** — a blade-shaped piece and a hilt-shaped
piece, each spanning its region of the whole subject. They are not detached subject features.
The remaining 328 satellites hold 4.16% of faces between them.

**So on this subject the `shells` column is counting inner-wall fragmentation, not detached
detail** — which is the opposite of what it counted on the galleon, where E04 established from
the concepts that the shells were free-floating rigging. The number means different things on
different subjects, and on 00002 it means the inner wall failed to join up. Whether that
matters downstream is not this session's call.

## 6. The blade as a sheet — this class's stressor

- **No open sheet, no through-hole, on any candidate** — zero boundary edges (§5).
- **The blade is a hollow box section**, not a solid slab: total thickness ~0.0208 / 0.0138 /
  0.0144 at mid-blade, of which two walls of ~0.00196 and a cavity of 0.0169 / 0.0099 / 0.0104.
- **The central ridge survives as legible geometry on all three**, plainly readable under
  `--clay` on view 0 with no texture at all, running the full length of the blade.
- **Apparent thickness on the renders is not decidable as thickness**, and is not quoted as
  such. Edge-on (view 2) each blade reads as a narrow sliver a few pixels wide at native scale;
  whether a given dark band is the slab's thickness or a shading gradient at a silhouette
  cannot be settled from a render, so the thickness figures above come from the mesh, not the
  picture. No `thin_extent` was derived — post-designation, and out of scope by the dispatch.
- **No pinch field in the blade.** E12's 00003 carried a dense non-manifold mass *through the
  field* of a folded wing (7,138 edges, 4.6× its siblings). Nothing of that kind occurs here on
  any candidate: 00002's blade carries **0.1%** of its non-manifold edges, 00001's 17.4%,
  00003's 35.9% of a total of 251 — i.e. about 90 scattered edges, not a mass.

## 7. Fine structure — and the pinch locus, which is not where I looked

### The non-manifold edges are on the GRIP WRAP, not on the cutting edges

Every non-manifold edge midpoint was projected back onto all eight views
(`nonmanifold_0000N/`). On 00002 the picture is unambiguous: a dense red band covering **the
helical wrap**, a scatter on the pommel, a few at the guard, and **a blade that is essentially
clean**.

| | share of non-manifold edges in the wrap band | that band's share of surface area | **enrichment** |
|---|---|---|---|
| 00001 | 58.7% | 17.0% | **3.44×** |
| 00002 | **97.7%** | 25.3% | **3.86×** |
| 00003 | 37.5% | 17.6% | **2.13×** |

**The denominator is named because it is not scale-free.** Non-manifold edges are a curve-like
quantity and surface area is an area-like one, so this enrichment factor is a comparison aid
between regions of one mesh — not a threshold, and not a quantity to gate on. The repo's
moving-denominator law is the reason that sentence is here rather than a bare ratio.

**And the counts order with wrap pitch, not with blade geometry**: 00002 has the finest, tightest
wrap of the three and **1,040** non-manifold edges; 00003's coarser wrap, 251; 00001's, 121.

### What that overturns

I predicted (P9) that the pinches would concentrate along the two cutting edges and the tip —
"a sword's version of the membrane's free rim, the locus where a slab thins to nothing."
**That is wrong, and wrong in an instructive direction.** The pinch locus is not where the
*form* thins; it is where the *relief* is finest. A blunt clay cutting edge is comfortably
above the voxel scale. A helical groove is not.

Offered as a hypothesis with its evidence, for whoever writes `prop.json`: **on this pipeline,
relief finer than the voxel scale does not become denser mesh — it becomes non-manifold
pinching at roughly constant density.** The hilt's density contrast (§9, 1.10–1.14×, the
*lowest* the route has measured) is the other half of the same observation, and P25 predicted
the opposite for the same reason I got P9 wrong.

### At the Director's zoom (`GATE0_hilt_0000N.png`, 4216 × 1446 each)

- **Wrap coils survive as legible helical relief on all three, and not one coil detaches.**
  00001: distinct turns with grooves between them, slightly lumpy, two collar rings. 00002: a
  fine, regular, tightly-pitched helix with roughly thirty individually countable turns — **the
  crispest of the three**. 00003: two wrap sections separated by a middle collar, the upper
  coarser and diagonal, the lower tighter and more regular; the middle collar itself
  reconstructs as an irregular ring of small lumps and is the one region here worth the
  Director's eye at zoom.
- **The gem pommel's facets return as planes with CRISP edges on 00002 and 00003** — clean
  planar faces meeting at sharp arrises, 00003's the chunkiest and best-defined. 00001's are
  readable but softer, with a rounded apex.
- **No quillon detaches on any mesh.** 00001's ends are stepped and chamfered, 00002's flared
  and chamfered, and **00003's curved quillons return as actual points, not blunted.**
- **Edge nicks and blade scoring reconstruct as geometry, attenuated relative to the clay.**
  Heaviest on 00003, where diagonal scoring is plainly legible across the blade field; moderate
  on 00001; on 00002 nearly absent, which matches its clay.
- **Bilateral symmetry**: quillons and blade edges read symmetric on all three renders.
  Observational only — no instrument was commissioned for it, per the dispatch.

## 8. Ground contact and the tip

**No ground or shadow-derived geometry reconstructed on any of the three, and every tip is free
and pointed.**

The z-min slab (the tip end) holds **0.1134% / 0.1019% / 0.0967%** of surface area at **43.8% /
51.7% / 48.2%** axis-facing. The comparison that makes those numbers mean something is E12's:
dragon 00001's z-min slab read **1.021% of area at 93.7% facing straight down**, and that was
flat foot soles resting on the ground plane. These are an order of magnitude less area at half
the axis alignment — the signature of a subject that ends in a point, not one resting on a floor.

At 4× zoom (`_tips_4x.png`) all three come to a defined point standing clear in space, with no
truncation and nothing fused beneath. **One caveat**: the last few pixels of each apex carry a
small rounding rather than a mathematically sharp point — visible at 4×, a fraction of a percent
of figure height, and reported because it is the kind of thing that decides acceptance at zoom.

(The z-max slab — the pommel end — reads 0.1013% / 0.1609% / 0.4377% at 70.7% / 100.0% / 73.9%
axis-facing. The high axis-facing fractions there are the pommel's flat top facet, which is what
the concepts show.)

## 9. Hilt-region evidence — the live allocation question, with no verdict attached

How the region was found, and the ANDON that method disables, are in §0b. Every box was defined
in **that candidate's own render frame**; the frames differ per mesh and these numbers mean
nothing against any other one.

| | **00001** (frame 240×1024) | **00002** (368×1024) | **00003** (320×1024) |
|---|---|---|---|
| quillon flare at z | 0.2355 | 0.2355 | 0.2255 |
| blade shoulder (local min) at z | 0.1954 | 0.1754 | 0.1854 |
| view-0 pixel box (reads world **x**, **z**) | 23,86 – 216,346 | 31,86 – 336,363 | 32,86 – 287,355 |
| view-2 pixel box (reads world **y**, **z**) | 92,86 – 147,346 | 146,86 – 221,363 | 125,86 – 194,355 |
| **hilt box** (Blender xyz), low | −0.11368, −0.03238, 0.19499 | −0.17962, −0.04415, 0.17500 | −0.15018, −0.04059, 0.18439 |
| **hilt box**, high | 0.11370, 0.03242, 0.50130 | 0.17971, 0.04421, 0.50134 | 0.15021, 0.04069, 0.50128 |
| box as share of bbox volume | 31.421% | 33.166% | 32.439% |
| **faces inside / total** | **353,770 / 999,474** | **471,211 / 948,328** | **359,636 / 951,850** |
| **share** | **35.396%** | **49.689%** | **37.783%** |
| median face area **inside** | 3.333e−07 | 4.803e−07 | 4.591e−07 |
| median face area **outside** | 3.783e−07 | 5.411e−07 | 5.060e−07 |
| **density contrast (out / in)** | **1.135×** | **1.127×** | **1.102×** |

**The caveat, stated so the number is not over-read.** Two silhouette rectangles 90° apart bound
a **region of space, not a segmentation**. Anything else occupying the box is counted — here
that includes the top of the blade's ricasso flare where it rises past the shoulder line on
00002 and 00003. Nothing was subtracted for it.

**Why the share is not comparable across subjects and the contrast is.** The dragon's head box
was 1.3–1.8% of its bounding-box volume; these are 31–33%, because a sword's bbox is mostly
empty air around a thin object. The share numbers therefore say more about box geometry than
about allocation. **The contrast does not have that problem, and it is the lowest the route has
measured: 1.102–1.135×, against the dragon head's 1.189–1.323×.**

**What is offered, and what is not.** E01 measured 3.1–4.5× more polygons on a character head
from a bust crop and it mattered; the ship ruled allocation NONE; the beast ruled NONE on its
own head evidence. **No answer is inherited and none is decided here.** The numbers above, and
the §7 observation that this pipeline answers fine relief with pinching rather than with
density, are the evidence `prop.json` gets after designation.

## 10. The frames and the sheets

**The frame is measured per mesh and its derivation is on the record.** Every rendered yaw was
asked for its projected width about the bbox centre, and the width rounded **up to a multiple of
16** — generator-legal, chosen as if the frame will be kept, because the ship's Gate 0 frame
became its twin frame and E04 Ruling 15 cost eight twins at 1066 → 1064.

| | widest **axis** / height | worst of 8 **yaws** | at view | 1024 × ratio | **render** | horiz. margin at worst view |
|---|---|---|---|---|---|---|
| 00001 | 0.225769 | 0.225769 | **0** | 231.2 | **240 × 1024** | 1.2499 |
| 00002 | 0.358284 | 0.358284 | **0** | 366.9 | **368 × 1024** | 1.2077 |
| 00003 | 0.297934 | 0.297934 | **0** | 305.1 | **320 × 1024** | 1.2627 |

**E12's per-yaw extension is correct here and inert here, and that is worth knowing before it is
trusted as a general guard.** On dragon 00002 it caught a 45° view needing 7.46% more than the
axis-only formula. On all three swords the worst yaw **is** view 0 and the two formulas agree to
six decimal places (+0.00%). The reason is structural: the quillon span lies along one horizontal
axis and the depth axis is small, so a 45° view projects the quillon tip at cos 45° = 0.707 of
its axis-view width and a shallow depth axis cannot make up the difference. E04's formula would
have given the identical frame on every candidate.

**An observation about the frame, offered as data with no recommendation.** These are the route's
first portrait frames, and at h = 1024 the derived widths are 240–368 px against the character's
752 and the dragon's 1664–1792. The blade occupies roughly 60–110 px of width in a Gate 0 render.
If this frame is kept as the twin frame — which is what the ship's precedent did — the generator
would be working at that horizontal resolution. Whether that is acceptable is a designation-and-
profile question and it is not decided here; it is flagged because the dispatch asked for the
frame to be chosen as if it will be kept.

One sheet per candidate, **full size, never a contact sheet**. Source concept on the left at
render height across both rows, eight `--clay` views on the right.

```
E:\AI\training\facet_next\E14_gate0\GATE0_candidate_00001.png   2716 x 2192
E:\AI\training\facet_next\E14_gate0\GATE0_candidate_00002.png   3228 x 2192
E:\AI\training\facet_next\E14_gate0\GATE0_candidate_00003.png   3036 x 2192
```

## 11. The dispatch's own inherited numbers, checked against source

Per the calibration note, in the same breath they were used. The full table is in
[E14-gate0-predictions.md](E14-gate0-predictions.md) §0, written before the meshes existed;
repeated here in summary.

| claim | source checked | verdict |
|---|---|---|
| clay byte counts 1,021,466 / 1,029,231 / 1,093,621 | directory listing | **confirmed, all three exactly** |
| character 40–191 shells; ship 237–512; beast 9–12 | `docs/handbook/subjects.md`; `E12-gate0-report.md` §3 | **confirmed** |
| character widest-horizontal/height 0.46–0.72 | `docs/handbook/subjects.md` | **confirmed** |
| "precedent cost 116–141 s and 4.4–5.6 GB" | `E04_gate0/recon.log` | **confirmed — but it is the galleon's**; the nearest precedent (E12, same runner) is 103–135 s / 3.4–3.8 GB, and this session came in at 96–136 s / 3.4 GB |
| `turn_render` maps `ortho_scale` to the vertical under `--fit-axis height` | `turn_render.py:109–111`, `sensor_fit = "VERTICAL"` set explicitly | **confirmed; the portrait case is handled** |
| the three clay descriptions | all three viewed at full size before predictions | **match in substance; three departures recorded** — 00002's quillon span (the most visible separator) is unnamed; 00001 also carries a ricasso flare, so 00003's distinguishing word is "double"; 00003 is not purely near-frontal |
| E12's two-backend refinement | this session's `recon.log`, all three meshes | **reproduced exactly** |
| the ~1M face counts are a subject property | `mesh_character.py` prints `decim=1000000` | **corrected — it is a decimation target** |

One further check, unprompted: the E15 context index was rebuilt at session start
(`python tools/facet_index.py build`, 2,538 FTS rows) and **came back byte-identical to the
committed `docs/index/facet.db`** — `git status` clean. The build is deterministic on an
unchanged record.

## 12. Every prediction, scored

Committed blind in `a4d587a`. **17 held, 8 falsified.**

| # | prediction | outcome | measured |
|---|---|---|---|
| P1 | `TOTAL` 90–140 s | held | 135 / 136 / 96 s |
| P2 | peak VRAM ≤ 4.0 GB | held | 3.4 / 3.4 / 3.4 GB |
| P3 | faces 900k–1,000k | held, **and its reasoning confirmed from source** | 999,474 / 948,328 / 951,850; the log prints `decim=1000000` |
| P4 | welded shells ≤ 8 on all three | **FALSIFIED on 00002** | 1 / **331** / 2 |
| P5 | largest-shell fraction ≥ 0.990 | **FALSIFIED on 00002** | 1.0000 / **0.4810** / 0.99997 |
| P6 | watertight False on all three | held | False ×3 |
| P7 | boundary edges ≤ 5, ~zero length | held, **stronger than predicted** | **0 / 0 / 0**, length exactly 0 |
| P8 | non-manifold fraction inside the dragon's 0.10–0.49% band | **FALSIFIED on all three, all BELOW** | 0.0081 / 0.0732 / 0.0176% |
| P9 | pinches concentrate on the cutting edges and tip | **FALSIFIED — and located** | they concentrate on the **grip wrap**: 3.44 / 3.86 / 2.13× enriched; 00002's blade holds 0.1% |
| P10 | blade a closed, thickened slab; no sheet, hole or boundary loop | **held on every testable clause; the wording "thickened slab" is wrong** | no boundary edge anywhere — but the slab is a **hollow box section**, walls 0.00196 around a 0.0099–0.0169 cavity |
| P11 | central ridge survives as geometry | held | legible under `--clay` on all three |
| P12 | no dragon-pattern pinch field in the blade | held | ~90 scattered edges at worst, no mass |
| P13 | coils legible; zero detached | held | legible on all three; no coil is a separate shell |
| P14 | coil relief weakest on 00002 (finest pitch) | **FALSIFIED** | 00002's is the **crispest** — ~30 individually countable turns |
| P15 | pommel facets readable planes with ROUNDED edges | **FALSIFIED as worded** | crisp arrises on 00002 and 00003; only 00001 is soft |
| P16 | no quillon detaches; 00003's points stay points | held, **both clauses** | none detached; 00003's tips are points |
| P17 | nicks reconstruct, attenuated; most on 00003 | held | 00003 heaviest, 00001 moderate, 00002 near-absent |
| P18 | no ground geometry; tip free and pointed | held, **with a caveat** | z-min slab 0.097–0.113% at 44–52%; apexes carry a small rounding at 4× |
| P19 | widest-horizontal/height in 0.20–0.40 | held | 0.2258 / 0.3583 / 0.2980 |
| P20 | ordering 00002 > 00003 > 00001 | held **exactly** | 0.3583 > 0.2980 > 0.2258 |
| P21 | frames 240–384 px wide | held | 240 / 368 / 320 — 00001 landed on the floor (raw 231.2) |
| P22 | worst yaw is view 0 or 4; ≤ 0.5% over axis-only | held **exactly** | view 0 on all three, **+0.00%** |
| P23 | bilateral symmetry reads on the renders | held (observational) | symmetric on all three |
| P24 | hilt face share 20–45% | **FALSIFIED on 00002** | 35.40 / **49.69** / 37.78% |
| P25 | density contrast 1.2–3.0, at or above the dragon's | **FALSIFIED on all three, all BELOW** | 1.135 / 1.127 / 1.102 |

**Where I was most wrong, and it is one error three times.** P8, P9 and P25 are the same
mistake: I assumed the sword's fine-structure risk lived where the *form* thins, because that is
where the dragon's lived, and I predicted more polygons where the relief is finest for the same
reason. The measured answer is that the pinch locus is the **helical wrap**, that the blade's
blunt cutting edges are comfortably above the voxel scale, and that fine relief buys pinching
rather than density. **This is precisely the error the predictions document opened by promising
to avoid** — pricing the prior instead of the subject — committed in a new place. E12's executor
made it with the ship; I made it with the dragon.

**Where the blind prediction earned its keep.** P22 named a structural reason the frame formula
would come out inert on this subject and it did, to six decimals; P20's ordering came from
looking at three clay images at full size and held exactly; and P4/P5 failed in a way that
*located* something — 00002's 331 components are an inner wall in fragments, which is how §4's
route-wide finding got started.

## 13. What was NOT done, each with the reason

- **`gate_mesh.py` did not run** on any of the three. Subject instruments are profile decisions;
  `profiles/prop.json` does not exist, and its absence-of-block is a decision the advisor records
  there after designation (ship precedent: `mesh_gate: none`).
- **No second reconstruction from a hilt crop.** E01's bust-crop move is the allocation lever and
  whether the prop gets it is the profile decision §9 gathers evidence *for*. Spending it now
  would decide a live question by improvisation, on candidates that may be rejected.
- **No decimation, no UV, no atlas, no twins, no texture.** Gate 0 is the route's first stage.
- **No `thin_extent` derivation and no thickness policy**, despite this session having measured
  wall and cavity figures — post-designation, on the designated mesh only, with the published
  cost curve.
- **No threshold armed from character, ship or beast values.** Palette bands, IoU halts and bbox
  tolerances are other subjects' data.
- **No profile writes, no `prop.json` stub, no identity fixture, no register decision.**
- **`mesh_stats`' warning condition was not changed** despite §3 showing it cannot fire on this
  subject class. Reported, not fixed: it is a shared instrument and a live lane's numbers depend
  on it.
- **Nothing in the E12/E13 lane was touched.** No file under `E13_stroke/`, `E13_stage1/` or any
  handoff-15 report was opened; `git status` was clean of other lanes' work at commit time. The
  only pre-existing repo file this session touched is none — every write was a new file.
- **No memory-store write.** The repo is the record.

## 14. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every command, env var, wall time, VRAM before/after, torch peak and exit code logged per mesh in `recon.log`; seed recorded from the pipeline's own printed signature; both attention backends recorded as what loaded; the decimation target read off the log rather than inferred; every derived frame, hilt box, topology record and non-manifold set written to JSON beside the artifact; two driver `.ps1` files staged so the session replays from the record |
| ANDON_AUTHORITY | **2** | Watchdog verified alive before the GPU leg and re-read after every mesh, with heartbeats in the log; the runner breaks on a non-zero exit rather than retrying with changed parameters; `e12_frame.py`'s frame check ran in the opposite direction from its derivation on all three; the designation halt is the gate. **Not 3, and §0b is why**: my hilt-box method disables `e12_head_evidence.py`'s Z-disagreement ANDON by construction, so one guard that could have fired cannot. Declared rather than banked, with the overlay as the compensating check |
| NAMED_COMPENSATORS | **2** | New files only — all artifacts under `E14_gate0/`, one new instrument, one new report, one new predictions doc. **Nothing pre-existing was opened for writing anywhere in this session.** No publish, no spend, nothing irreversible. One exception declared in §0a (instrument placement) and one stray directory created by a relative `--out` resolving against Blender's cwd (`C:\hilt_00001\`), noticed and removed the same minute; undo for the instrument is `git revert` |
| DECOMPOSE_BY_SECRETS | **3** | Frames derived per mesh and never inherited; the hilt region derived from each mesh's own quillon flare rather than from any other subject's rect; character-only stats columns named and excluded — and the fact that the tool's own warning *failed* to exclude them on this class reported rather than quietly relied on; no value written to any profile; texture-stage steel priors left for the spec and not enacted |
| UNCERTAINTY_GATED_HUMANS | **3** | The halt IS the designation gate: three full-size sheets, three hilt crops at 4216 px, the hilt box drawn back onto all eight views of each mesh, every non-manifold edge drawn onto the geometry that carries it, and a 4× tip crop. No ranking anywhere in the report, the sheets or the tool captions |
| EXTERNAL_VERIFIER | **2** | `mesh_stats` measures any mesh identically and is the instrument that checked the E04 and E12 seats; the boundary and non-manifold arithmetic in `e14_topology.py` is independent of `e12_nonmanifold.py`'s and agrees with it exactly on all three; the vertex-shell count agrees with `mesh_stats` on all three; §4's hollow finding was checked by three mutually independent methods (signed volume, cross-section clustering, ray crossings) and against two out-of-family controls. Gate 0's verifier is the Director's eye on artifacts. `skip:` on a second model — deterministic geometry, per the Gate 0 precedent |

---

**HALT. Three sheets, three hilt crops, three stats JSONs, three frame JSONs, three hilt JSONs,
three topology JSONs, three non-manifold JSONs with their overlay renders, the boxed overlays,
the tip crop, and `recon.log`, all staged at `E:\AI\training\facet_next\E14_gate0\`.** No
ranking, no recommendation, no scaffolding past Gate 0.

To the advisor's eye first, per the looking rule; **the Director designates, or rejects all
three, and either is the gate working.**

**One item is flagged for the advisor independently of designation**: §4's finding is not about
longswords. If it holds under the advisor's reading, it describes the geometry of every asset
this route has shipped, including the accepted galleon and the accepted dragon — and it was
invisible for eleven experiments because nothing had asked a ray how many surfaces it crosses.
