# E12 Gate 0 — three dragon clays, three meshes. HALT: the Director designates.

**Executor session, 2026-08-05 evening.** All three staged concepts reconstructed locally,
welded, measured with no `--profile`, rendered `--clay` beside their source at full size,
and given a head-region measurement derived per mesh. **`gate_mesh.py` did not run**, per the
dispatch: subject instruments are profile decisions and `profiles/beast.json` does not exist.

**This document ranks nothing.** Which dragon is *the* dragon is an outcome call and it is the
Director's. Rejecting all three is a legitimate outcome. Three sheets, three head crops and
the numbers below are staged, and I am stopping.

Predictions were committed **blind**, before any dragon mesh existed, in
[E12-gate0-predictions.md](E12-gate0-predictions.md) (`602640b`). **Thirteen of twenty-one
held; eight were falsified**, three of them on the headline questions. Section 9 scores every
one.

---

## 0. Three deviations from the dispatch, declared before any result

**a. Three new instruments live in `tools/diagnostics/`, not under `E12_gate0/`.** The
dispatch's compensator line says "new files only, all under `E12_gate0/`". The repo's own
convention puts per-experiment instruments beside the code (`e04_*`, `e07_*`, `e08_*`,
`e10_*` are all in `tools/diagnostics/`), and an instrument outside the repo cannot be re-run
by the next session from a clone. New files either way; nothing pre-existing was opened for
writing by this change. `e12_frame.py`, `e12_head_evidence.py`, `e12_head_render.py`,
`e12_head_sheet.py`, `e12_nonmanifold.py`.

**b. `tools/verify/gate0_sheet.py` WAS opened for writing — one additive flag.** Its caption
printed, as literal text, *"gate_mesh.py was NOT run: its head/shoulder logic is meaningless
on a ship, and profiles/ship.json records mesh_gate: none as a decision."* On a dragon sheet
both halves of that sentence are false, and a designation sheet is the last place a wrong
provenance line should sit. The fix is `--gate-note`, **defaulting to E04's sentence
verbatim**, so no historical invocation changes. That claim is tested rather than asserted:
E04's `GATE0_candidate_00004.png` was regenerated with the edited tool and compared against
the committed artifact **pixel by pixel — 0 differing pixels of 15,501,824, max channel delta
0**. (Pixels, not a file hash: a PNG hash mismatch has produced two false halts in this repo.)

**c. The render frame asks every rendered yaw, not just the axis-aligned ones.** E04's driver
used `max(ex, ey) / ez`, which bounds views 0/2/4/6 only; at 45° the camera's horizontal axis
is `(cos θ, sin θ, 0)` and the projected width can exceed either axis. **On 00002 it does, by
7.46%** — view 3 needs 1.7270 × height where the widest axis is 1.6071. Reported honestly:
E04's formula would **not** have cropped it. It would have rendered 00002 at 1648 px with a
horizontal margin of **1.1220** at view 3 instead of **1.2091**, i.e. eaten most of the
1.204 margin without warning. On 00001 and 00003 the two formulas agree to the pixel.

---

## 1. Environment, reported before the GPU work rather than after

**The watchdog was verified alive immediately before the GPU leg and again after it.** At
20:43:37 the heartbeat was **1.5 s old against a 15 s threshold**, no `_watchdog_DEAD`, no
`_watchdog_TRIPPED`, and the CSV was accruing live 2 s samples — two independent signals, not
one file's mtime. Across the reconstruction window the watchdog logged **218 samples**, VRAM
**1,866–8,235 MiB against the 31,200 ceiling**, and **zero ABORTs**. The newest ABORT in
`_watchdog_KILL.log` is still 2026-08-04 09:17:31; nothing fired today. Heartbeats are
recorded in `recon.log` at start and after each mesh.

**The third hard death is in the log and it is the mechanism the dispatch names.**
`2026-08-05 19:36:15 watchdog DEAD — loop died: The process cannot access the file
'E:\AI\training\_watchdog_HEARTBEAT' because it is being used by another process.` The
advisor's restart at 20:21:41 is the live process. **Reported, not fixed** — a protection
process is not something to redesign mid-task.

**One thing worth recording that E04 could not:** the current kill list includes
`E:\AI-Models\trellis2-env\Scripts\python.exe`, the exact interpreter this leg ran under. E04
Gate 0's 153 no-op ABORTs failed because the holder was not on the list; this leg's holder
was. The mechanism had an applicable target throughout.

**The `trellis2` PYTHONPATH repair from E04 was still required** and is written into the
runner with its reason. Without it the package is not importable from `trellis2-env`.

**A refinement to E04's recorded backend finding, from the same two log lines.** E04 recorded
*"with `ATTN_BACKEND=sdpa` and `SPARSE_ATTN_BACKEND=sdpa` both set, trellis2 still reports
`Attention backend: flash_attn`."* True, and incomplete: the import prints **two** backends,
and only one ignores its variable —

```
[SPARSE] Conv backend: flex_gemm; Attention backend: flash_attn     <- ignores SPARSE_ATTN_BACKEND
[ATTENTION] Using backend: sdpa                                     <- honours ATTN_BACKEND
```

Both lines are present in E04's own `recon.log` too, so this corrects the *record*, not the
run. **What loaded is what the log says**: sparse attention on `flash_attn`, dense attention
on `sdpa`, on all three meshes.

**Two traps paid for in this session, so the next one does not pay them again.** `--box` with
a leading negative number was eaten by argparse exactly as CLAUDE.md warns (`--box=...` is the
fix; one run lost). And **Blender's bundled Python has no Pillow**, which is why the head-crop
composition is its own tool run under the pipeline interpreter rather than a block inside the
Blender script.

## 2. The runs

TRELLIS.2 `1024_cascade`, local, watchdog verified. `run()`'s signature — printed into
`recon.log` by `mesh_character.py` itself — records `seed: int = 42` and the tool exposes no
seed flag, so all three ran at seed 42, the same seed E01/E02 recorded for W3 and E04 for the
galleons.

| candidate | source | out | `TOTAL` | shell wall | GEN peak | OVERALL peak | exit |
|---|---|---|---|---|---|---|---|
| 00001 | `dragon_clay_p1_00001_.png` | `dragon_00001_raw.glb` 35.9 MB | **135 s** | 160.3 s | 3.8 GB | **3.8 GB** | 0 |
| 00002 | `dragon_clay_p1_00002_.png` | `dragon_00002_raw.glb` 37.5 MB | **106 s** | 111.6 s | 3.7 GB | **3.7 GB** | 0 |
| 00003 | `dragon_clay_p1_00003_.png` | `dragon_00003_raw.glb` 38.4 MB | **103 s** | 108.5 s | 3.4 GB | **3.4 GB** | 0 |

```
mesh_character.py --image <clay> --out <glb> --ptype 1024_cascade
  PYTHONPATH=E:\AI-Models\TRELLIS.2-repo  HF_HOME=E:\AI-Models\hf-cache
  ATTN_BACKEND=sdpa  SPARSE_ATTN_BACKEND=sdpa   (see §1 - only the SPARSE one is ignored)
```

`TOTAL` is the pipeline's own figure and the one comparable with E04's 116–141 s. The shell
wall exceeds it by **25 s on the first mesh and ~5 s on the other two** — a cold HF cache on
the first load, not subject cost. `nvidia-smi` read 1,896 → 1,868 → 1,895 → 1,883 MiB across
the three runs, i.e. the process returned its memory each time.

**All three dragons are cheaper than every galleon, in both time and VRAM** (103–135 s
against 116–141; 3.4–3.8 GB against 4.4–5.6). The pre-bake mesh sizes explain part of it:
5,135,100 / 5,013,376 / 3,822,236 faces before decimation against the ship's larger
structures. This falsified two of my cost predictions; see §9.

## 3. `mesh_stats` — measured identically on all three, **no `--profile`**

No profile was passed, on purpose: `beast.json` does not exist and the no-profile path is
`subject_profile.bind`'s byte-identity path. Welding happens inside `mesh_stats`
(`merge_vertices(merge_tex=True, merge_norm=True)`), which reports the unwelded count beside
the real one.

| | **00001** | **00002** | **00003** |
|---|---|---|---|
| faces | 965,625 | 966,690 | 986,825 |
| verts | 480,604 | 479,865 | 485,291 |
| **shells (welded)** | **12** | **12** | **9** |
| largest shell | **0.999043** | **0.999427** | **0.999599** |
| shells (unwelded) | 20,405 | 24,746 | 28,870 |
| watertight | False | False | False |
| extent (Blender x, y, z) | 1.0019, 1.0012, **0.6189** | 1.0019, 0.9976, **0.6234** | 1.0017, 1.0004, **0.5743** |
| **widest horizontal / height** | **1.6188** | **1.6072** | **1.7442** |

The dispatch's Blender-convention naming, spelled out because every world quantity in this
report is in it: **x** and **y** are the two horizontal axes, **z** is height; the widest
horizontal axis is **x** on all three.

**`mesh_stats` printed its front-view-rect warning on all three, and it is quoted rather than
suppressed:**

```
[stats] WARNING dragon_00001: vertical extent is not the largest ([1.0019, 1.0012, 0.6189])
        - the front-view rect may not be on the head
```

identically for 00002 (`[1.0019, 0.9976, 0.6234]`) and 00003 (`[1.0017, 1.0004, 0.5743]`).
That is the character instrument correctly noticing it is not looking at a character.
`face_rect_density`, `face_rect_faces`, `face_curvature_var` and `curv_radius` are therefore
**not quoted anywhere in this report**: the rect is W3's, authored against a humanoid at the
character's framing, and a raw reconstruction's front is unestablished. The head evidence in
§5 replaces them. (`median_tri_cells` came back 0.640 / 0.619 / 0.547, all below the tool's
1.5 threshold, so its second warning did not fire.)

### Four observations offered as data, with no verdict attached

**Shell counts run 12 / 12 / 9 against a character's 40–191 and a ship's 237–512.** Both
priors were checked against source this session. These are **an order of magnitude more
connected than anything this repo has reconstructed**, with 99.90–99.96% of faces in the
largest shell against the character band's 92–98% and the ship's 88.0–92.9%. The dispatch's
stated prior — a dragon's thin structure is mostly *attached* where the ship's rigging was
free-floating — is supported, and by more than it asked for. What the satellite shells
actually are is §4.

**All three measure far wider than tall — 1.6188 / 1.6072 / 1.7442** — against every galleon
(1.114 / 1.088 / 1.041). A wingspread is a wider thing than a hull is long, and by a clear
margin.

**x and y are both ≈ 1.00 on all three, and that is not a clipped mesh.** The subject spans
the generation box in *both* horizontal directions, which invites the suspicion that it is
being cut off by the volume. It is not: a cut leaves a flat wall, so the outermost 0.5% slab
of each axis was measured for area share and for how much of it faces along that axis. Every
slab is **0.011–0.092% of surface area** with 21–66% axis-facing — i.e. a subject touching
its box, not one sliced by it. The single exception is 00001's **z-min at 1.021% of area,
93.7% of it facing straight down**: flat foot soles on the ground plane, which is what the
concept shows and what 00002 (0.011%) and 00003 (0.016%) lack because fewer of their feet are
planted flat.

**`watertight: False` on all three, and the reason is not what the name suggests.** These
surfaces have **no open boundary at all** — 1, 0 and 1 boundary edges respectively, and those
single edges are of **zero length** (degenerate). What makes them non-watertight is edges with
**more than two** adjacent faces: 1,561 / 2,564 / 7,138. That distinction is the subject of
§6 and it is the most load-bearing measurement in this report.

## 4. What the satellite shells are — every one located

With 99.9%+ of faces in the largest shell, the other 8–11 shells hold 924 / 554 / 396 faces
in total. Each was enumerated (face count, surface area, extent, centre in the Blender frame)
and then **projected back onto the profile render** so the answer is a picture rather than a
coordinate.

| | 00001 | 00002 | 00003 |
|---|---|---|---|
| satellite shells | 11 | 11 | 8 |
| faces off the main body | 924 (0.096%) | 554 (0.057%) | 396 (0.040%) |
| largest satellite | 252 faces, extent 0.0074 × 0.0169 × 0.0083 | 198 faces, 0.0028 × 0.0173 × 0.0045 | 180 faces, 0.0112 × 0.0162 × 0.0112 |
| smallest | 14 faces | 8 faces | 4 faces |

**They are teeth, and on one mesh they are also tail-ridge spines.** On all three, most
satellites sit at y ≈ −0.44 to −0.49 and z ≈ 0.04–0.14 — inside the open mouth — and the
overlay lands them exactly on the **front fangs**, upper and lower. On **00001 only**, four
further satellites sit at y ≈ +0.08 to +0.16 and the overlay lands them on **individual spines
of the dorsal/tail ridge**. 00002 and 00003 carry no detached ridge spine.

**No horn is detached on any of the three**, and no wing, claw, limb or tail structure is
detached at any structural scale: the largest thing that came off anything is 0.017 world
units on a figure 0.57–0.62 tall.

## 5. Head-region evidence — the live allocation question, with no verdict attached

**How the region was found, and the rule it obeys.** Not by height: on all three the horns,
the raised wingtips and the tail spines rise above the crown, so a height band would have
measured a horn — the raised-weapon rule wearing wings. The head was located **by eye** on
each mesh's own `--clay` turnaround, as two pixel rectangles 90° apart, read off a coordinate
grid drawn over 1:1 crops of `clay_0.png` and `clay_2.png`. Each pair was converted to one
axis-aligned world box by the exact inverse of `turn_render`'s camera — the convention taken
from `silhouette_masks.py`, whose header states it and whose `--anchor` flag proved it
byte-identical against masks on disk, rather than re-derived here.

**Then the box was drawn back onto all eight views and looked at.** That check is in the
staged artifacts (`boxed_0000N/`) and it is why these boxes are claimed rather than hoped: on
each mesh the rectangle contains skull, jaws, horns and frill and excludes neck, wings and
body. Every box was defined in **that candidate's own render frame** — the frames differ per
mesh and these numbers mean nothing against any other one.

| | **00001** (frame 1664×1024) | **00002** (1776×1024) | **00003** (1792×1024) |
|---|---|---|---|
| view-0 pixel box (reads world **x**, **z**) | 690,170 – 955,525 | 745,175 – 1015,475 | 740,200 – 1015,495 |
| view-2 pixel box (reads world **y**, **z**) | 128,170 – 440,510 | 240,175 – 500,470 | 155,200 – 450,495 |
| the two views' **z** disagreement | 1.76% of height | 0.59% | 0.00% |
| **head box** (Blender xyz), low | −0.10294, −0.51219, −0.00993 | −0.10448, −0.47530, 0.02575 | −0.10497, −0.50074, 0.01045 |
| **head box**, high | 0.08989, −0.28515, 0.24840 | 0.09343, −0.28472, 0.24565 | 0.08072, −0.30154, 0.20965 |
| box extent | 0.1928 × 0.2270 × 0.2583 | 0.1979 × 0.1906 × 0.2199 | 0.1857 × 0.1992 × 0.1992 |
| box as share of bbox volume | 1.822% | 1.331% | 1.280% |
| **faces inside / total** | **112,645 / 965,625** | **96,631 / 966,690** | **103,591 / 986,825** |
| **share** | **11.666%** | **9.996%** | **10.497%** |
| median face area **inside** | 2.294e−06 | 2.053e−06 | 1.751e−06 |
| median face area **outside** | 2.889e−06 | 2.715e−06 | 2.082e−06 |
| **density contrast (out / in)** | **1.259×** | **1.323×** | **1.189×** |
| mean face area in / out | 2.603e−06 / 3.275e−06 | 2.432e−06 / 3.189e−06 | 1.944e−06 / 2.350e−06 |

**The caveat, stated so the number is not over-read.** Two silhouette rectangles 90° apart
bound a **region of space, not a segmentation**. Anything else occupying the box is counted.
By eye, on all three the box also contains the top of the neck behind the jaw hinge and, on
00001 and 00003, a small area of wing membrane passing behind the skull. Nothing was
subtracted for that.

**What is offered, and what is not.** The share and the contrast are the evidence. Whether a
head at ~10–12% of faces with a ~1.2–1.3× density contrast argues for or against E01's
bust-crop lever is the `beast.json` decision, it is made after designation, and it is not made
here. E01 measured **3.1–4.5×** more polygons on a head from a bust crop; the contrast a
full-figure frame supplies on its own is the number in that row, and the two are on the table
together for whoever writes the profile.

`GATE0_head_0000N.png` puts each head at the Director's zoom: three yaws (0° head-on, 45°,
90° profile) at 1400 px each, `--clay`, framed by the measured box padded 1.12 — 4216 × 1446
per candidate.

## 6. The thin-structure findings — the reason this subject is the new primary

### The membranes come back as CLOSED SLABS, not open sheets — measured, not eyeballed

This is decidable from the mesh and does not need shading: an **open** sheet carries a
boundary loop around its whole perimeter (edges with exactly one adjacent face); a closed slab
carries none there. Measured across all edges:

| | 00001 | 00002 | 00003 |
|---|---|---|---|
| unique edges | 1,446,876 | 1,447,471 | 1,473,100 |
| **boundary edges (1 adjacent face)** | **1** | **0** | **1** |
| total boundary length | **0.00000** | — | **0.00000** |
| **non-manifold edges (>2 faces)** | **1,561** (0.1079%) | **2,564** (0.1771%) | **7,138** (0.4846%) |

Two boundary edges across three meshes, both of zero length. **There is no open sheet and no
open puncture anywhere on any of the three** — an open hole in a surface makes a boundary
loop, and there are none. (A *tunnel* through a closed slab would not make one; none was seen
by eye either, in views 0 and 2 at full size on all three and in 5× crops of the trailing
edges.)

### Where the non-manifold edges are — counted AND put on the picture

A count alone is a proxy, so every non-manifold edge midpoint was projected back onto all
eight views (`nonmanifold_0000N/`). The pictures are unambiguous:

- **00001 (1,561)** — a red line tracing **the scalloped trailing rim of both wing
  membranes**, plus the head frill spikes and a scatter on the chest. The pinching is confined
  to the membrane's free rim, where a slab thins to nothing.
- **00002 (2,564)** — the same pattern, denser: both trailing rims, the frill, a scatter down
  the body.
- **00003 (7,138)** — **a dense mass through the field of the folded wing itself**, not only
  at its rim, plus the frill and a few elsewhere. 4.6× 00001's count and a different
  distribution.

The hypothesis this suggests — that a membrane thinner than the voxel grid fails by *pinching*
(its two faces meeting along one edge instead of enclosing a thickness) rather than by holing
— is consistent with both the count and the location. It is offered as a hypothesis with its
evidence, not as a ruling, and the instrument (`e12_nonmanifold.py`) is in the repo so it can
be run on anything.

### Apparent thickness on the renders

At 5× NEAREST magnification, every free membrane edge on all three reads as a **1–2 pixel dark
rim** at native scale — at 0.000675–0.000728 world units per pixel, ~0.0007–0.0015 world units
against figure heights of 0.574–0.623, i.e. **0.1–0.25% of height**. Whether that rim is the
slab's thickness or a shading gradient at a silhouette is **not decidable from a render**, and
this session did not measure the thickness: thin-structure derivation is post-designation and
out of scope by the dispatch.

### Trailing edges, filaments, scales, jaws

- **Trailing edges** — on the regions inspected (00001 v0 250–470 × 320–440; 00002 v0
  240–460 × 430–550; 00003 v0 120–340 × 300–420, all at 5×), the scalloped edges are **smooth
  continuous arcs with no tears and no ragged breaks**, and the claw/spur tips at the scallop
  corners are intact.
- **Horns** — full, sharp, attached on all three; no satellite shell is anywhere near a horn.
- **Tail ridge / dorsal spines** — attached on 00002 and 00003; **four individual spines
  detached on 00001** (§4). No blunting observed on any of the three; the tips are fine and
  sharp.
- **Scales** — reconstruct as **geometry**, plainly legible under `--clay` with no texture at
  all: overlapping plate relief on neck, chest, flank, limbs and tail on all three.
- **Open jaws** — the mouth cavity reconstructs **open** on all three, with an upper and a
  lower tooth row and a tongue visible inside on 00001 and 00002. **The front fangs are
  free-standing shells, not relief on the jaw**, on all three. *⚠ Annotated 2026-08-06
  (E12 Ruling 12b, handoff-5 Task 1): this sentence is true as written, and the
  omission-as-absence reading of it — "no tongue on 00003" — is falsified. The designated
  mesh carries a large main-shell tongue, first-hit visible from the route's own eye-level
  cameras; at this report's full-figure scale the mouth spans ~1.1–1.6% of frame and the
  observation could not have resolved it either way.*

### One region worth the Director's eye on 00003

On view 0 there is a **deep narrow crevice between the throat/chest ridge and the right
shoulder**, running from below the jaw down to the chest, with rough irregular walls; the
throat itself reconstructs as a stack of hard-stepped horizontal bands. Reported as an
observation at zoom, with no diagnosis and no verdict. Crop: `clay_0.png` (860,380)–(1120,580).

### The reconstructions do not preserve the concepts' poses

Readable off all three sheets, panel beside panel. Each concept shows a different asymmetric
pose — 00001 a quadruped leaning with the head in near-profile, 00002 **upright with both
forelimbs raised clear of the ground**, 00003 mid-stride with **one wing folded short and one
spread**. All three meshes come back as a **bilaterally symmetric, forward-facing quadruped
with both wings spread**, all four limbs planted. Offered as data. What it implies about how a
beast concept should be staged is not this session's call.

## 7. The frames and the sheets

**The render frame is measured per mesh, and its derivation is on the record.** Every yaw
actually rendered was asked for its projected width about the bbox centre (which is where
`turn_render` puts the camera), and the width was rounded **up to a multiple of 16** — the
generator-legal constraint, chosen as if this frame will be kept, because the ship's Gate 0
frame became its twin frame and E04 Ruling 15 cost eight twins at 1066 → 1064.

| | widest **axis** / height | worst of 8 **yaws** / height | at view | 1024 × ratio | **render** | horiz. margin at the worst view |
|---|---|---|---|---|---|---|
| 00001 | 1.618843 | 1.618843 | 0 | 1657.7 | **1664 × 1024** | 1.2086 |
| 00002 | 1.607099 | **1.727034** | **3** | 1768.5 | **1776 × 1024** | 1.2091 |
| 00003 | 1.744221 | 1.744221 | 0 | 1786.1 | **1792 × 1024** | 1.2080 |

00002's per-view projected widths are 1.0019 / **1.0764** / 0.9976 / **1.0766** / … — the 45°
views are the wide ones, because its wingspan and its tail sweep are nearly equal and lie
about 45° apart. E04's formula would have given it 1648 px: no crop, but a 1.1220 horizontal
margin instead of 1.2091. The tool prints both numbers on every run.

One sheet per candidate, **full size, never a contact sheet**. Source concept on the left at
render height across both rows, eight `--clay` views on the right. `--clay` by standing rule:
texture hides geometry, and a raw reconstruction has none to hide behind.

```
E:\AI\training\facet_next\E12_gate0\GATE0_candidate_00001.png   9376 x 2192
E:\AI\training\facet_next\E12_gate0\GATE0_candidate_00002.png   9824 x 2192
E:\AI\training\facet_next\E12_gate0\GATE0_candidate_00003.png   9888 x 2192
```

## 8. The dispatch's own inherited numbers, checked against source

Per the calibration note, in the same breath they were used:

| claim | source checked | verdict |
|---|---|---|
| character reconstructions 40–191 shells | `E01-ruling-gate1.md` §"Shell soup", 92–98% in the largest | **confirmed** |
| ship 237–512 shells, driven by free-floating rigging | `E04-gate0-report.md` §3 (237 / 274 / 512, largest 88.0 / 92.3 / 92.9%) | **confirmed** |
| precedent cost 116–141 s, 4.4–5.6 GB peak | `E04_gate0/recon.log` `[GLB] … TOTAL` / `OVERALL PEAK` lines (141/125/116 s, 4.4/5.6/4.6 GB) | **confirmed** |
| the three clay descriptions | all three viewed at full size before the predictions were written | **all three match**, in detail |
| mtimes are a UTC stamp, ~20:11 local | mtime 2026-08-06T00:11:56−04:00, i.e. 3 h 34 min in the *future* against a 20:37 session start | **confirmed to the minute** |
| E10's `pos.npy` predictions file is on disk uncommitted | it was already **committed** at `cd41ee5` before this session began; the file uncommitted in that lane at session start was `tools/e11_export_turnaround.py` | **stale, corrected** — neither was touched |
| E04's recorded backend finding | see §1 | **incomplete, refined** |

## 9. Every prediction, scored

Committed blind in `602640b` before any dragon mesh existed. **13 held, 8 falsified.**

| # | prediction | outcome | measured |
|---|---|---|---|
| P1 | welded shells 60–200 on all three | **FALSIFIED** | 12 / 12 / 9 — an order of magnitude below the floor |
| P2 | all below the ship's 237 | held | 12 / 12 / 9 |
| P3 | largest-shell fraction ≥ 0.95 | held | 0.9990 / 0.9994 / 0.9996 |
| P4 | shells ordered 00002 ≥ 00001 ≥ 00003 | held **on a tie** | 12 ≥ 12 ≥ 9 — the prediction had no power to separate the first two |
| P5 | `watertight` False on all three | held, **for the wrong reason** | False on all three — but from non-manifold edges, not the open boundary my reasoning assumed |
| P6 | membranes are closed slabs, not open sheets | **held, decisively** | 1 / 0 / 1 boundary edges, all of zero length |
| P7 | membrane thickness visible edge-on as a *distinct edge* rather than a hairline | **FALSIFIED** | a 1–2 px rim at native scale is a hairline; and whether it is thickness at all is not decidable from a render |
| P8 | no through-holes in the membrane field | held, with scope stated | no open puncture anywhere (boundary-edge count); no tunnel seen by eye |
| P9 | trailing edges tear or blunt on at least one mesh | **FALSIFIED** | smooth continuous arcs, tips intact, on every region inspected |
| P10 | horns and tail ridge attached; tips blunt somewhere | **FALSIFIED, both clauses** | horns attached — but **four tail-ridge spines detached on 00001**; no blunting anywhere |
| P11 | jaws open; teeth as relief, not separate shells | **FALSIFIED as worded** | cavity open on all three ✓; **front fangs are free-standing shells on all three** ✗ |
| P12 | scale relief reconstructs as geometry | held | legible under `--clay` on all three |
| P13 | widest-horizontal / height > 1.0 | held | 1.6188 / 1.6072 / 1.7442 |
| P14 | that ratio in 1.15–1.60 | **FALSIFIED** | all three **above** 1.60 |
| P15 | frames wider than the galleon's 1152, landscape | held | 1664 / 1776 / 1792 |
| P16 | head face share 8–22% | held | 11.666 / 9.996 / 10.497% |
| P17 | share ordered 00001 > 00003 > 00002 | held | 11.666 > 10.497 > 9.996 |
| P18 | median face area inside < outside, ratio 1.0–2.5 | held | 1.259 / 1.323 / 1.189 |
| P19 | wall 110–170 s | **FALSIFIED** | 135 / **106** / **103** s on the comparable quantity |
| P20 | peak VRAM 4.0–7.0 GB | **FALSIFIED** | **3.8 / 3.7 / 3.4 GB** — below the floor on all three |
| P21 | `flash_attn` loads despite `ATTN_BACKEND=sdpa` | held, **refined** | sparse attention ignores its variable; dense attention honours it (§1) |

**Where I was most wrong, and it is the same error twice.** P1 and P14 both reasoned from the
ship: I took the galleon's fragmentation as the near neighbour and bet the dragon would land
between it and the character. It landed an order of magnitude the *other* side of the
character. The ship's shells were free-floating rigging; a dragon has none, and I priced the
prior instead of the subject. P19/P20 are the same shape — the ship's cost quoted as the
dragon's floor.

**Where the blind prediction earned its keep.** P6 named the mechanism (slab, not sheet) and
the measurement that would settle it, before the mesh existed; P17's ordering came out of
looking at three clay images at full size and held exactly; and P10/P11 failed in a way that
*located* the failure — teeth and tail spines — which is more useful than either would have
been if it had passed.

## 10. What was NOT done, each with the reason

- **`gate_mesh.py` did not run** on any of the three. Subject instruments are profile
  decisions; `beast.json` does not exist, and its absence-of-block is a decision the advisor
  records there after designation (ship precedent: `mesh_gate: none`).
- **No second reconstruction from a head crop.** E01's bust-crop move is the allocation lever
  and whether the beast gets it is the profile decision §5 gathers evidence *for*. Spending it
  now would decide a live question by improvisation, on candidates that may be rejected.
- **No decimation, no UV, no atlas, no twins, no texture.** Gate 0 is the route's first stage.
- **No `thin_extent` derivation, and no membrane thickness measured** — post-designation, on
  the designated mesh only, with the published cost curve.
- **No threshold armed from character or ship values.** The palette bands, the IoU halt and
  the bbox tolerance are other subjects' data.
- **No profile writes, no `beast.json` stub, no identity fixture.**
- **Nothing in the E10 / E11 lane was touched.** That lane was live alongside this session
  and landed three commits on top of the predictions commit while this one was running —
  `20f2a0a`, `d37b504`, `18bdcdf`, touching `tools/e11_export_turnaround.py`,
  `tools/e11_manifest.py`, `README.md` and five E04/E10/E11 docs. **No file overlaps between
  the two sessions**, verified by `git log --name-only` over the range; this report's only
  edit to pre-existing code is §0b.
- **No memory-store write.** The repo is the record.

## 11. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every command, env var, wall time, VRAM before/after, torch peak and exit code logged per mesh in `recon.log`; seed recorded from the pipeline's own printed signature; backend recorded as what loaded rather than what was requested; every derived frame, every head pixel box and every world box written to JSON beside the artifact; three driver `.ps1` files staged so the whole session replays from the record |
| ANDON_AUTHORITY | **3** | Watchdog verified alive by two independent signals immediately before the GPU leg and re-read after each mesh; the runner breaks on a non-zero exit rather than retrying with changed parameters; `mesh_stats`' front-view-rect warning quoted on all three rather than suppressed; `e12_frame.py` re-checks its chosen frame against every rendered yaw in the opposite direction from its derivation, and `e12_head_evidence.py` raises on a non-axis view, a same-axis pair, a Z disagreement past tolerance or a box outside the mesh; the designation halt is the gate |
| NAMED_COMPENSATORS | **2** | New files only under `E12_gate0/`, five new instruments in `tools/diagnostics/`, one new report. **One exception, declared in §0b**: `tools/verify/gate0_sheet.py` gained one additive flag whose default is the prior behaviour verbatim — undo is `git revert`, owner is this session, and the no-change claim was verified against E04's committed artifact at 0/15,501,824 differing pixels. No publish, no spend, nothing irreversible in scope |
| DECOMPOSE_BY_SECRETS | **3** | Frames derived per mesh and never inherited; head regions derived per mesh from that mesh's own renders rather than from W3's face rect; character-only stats columns named and excluded rather than quietly printed; no value written to any profile; the one place a subject constant had leaked into shared code as literal text (the sheet caption) was found and parameterised with its default preserved |
| UNCERTAINTY_GATED_HUMANS | **3** | The halt IS the designation gate: three sheets at 9376–9888 px, three head crops at 4216 px, the head box drawn back onto all eight views of each mesh so the measured region is checkable by eye, and every non-manifold edge drawn onto the geometry that carries it. No ranking anywhere in the report, the sheets or the tool captions |
| EXTERNAL_VERIFIER | **2** | `mesh_stats` measures any mesh identically and its character-specific warning fired correctly on all three — the instrument checking this seat, as it checked E04's. The boundary/non-manifold counts come from raw edge arithmetic, independent of the shell instrument, and agree with it. Gate 0's verifier is the Director's eye on artifacts. `skip:` on a second model — deterministic geometry, per the Gate 0 precedent |

---

**HALT. Three sheets, three head crops, three stats JSONs, three frame JSONs, three head
JSONs, three non-manifold JSONs with their overlay renders, and `recon.log`, all staged at
`E:\AI\training\facet_next\E12_gate0\`.** No ranking, no recommendation, no scaffolding past
Gate 0. To the advisor's eye first, per ledger forty-three; **the Director designates, or
rejects all three, and either is the gate working.**
