# E14 handoff 2 — the designated longsword's measurement pass. HALT before generation.

**Executor session, 2026-08-07.** Predictions committed blind in `d11fd32`
([E14-handoff2-predictions.md](E14-handoff2-predictions.md)) before any instrument touched the
mesh. Task 1's report is separate and already committed (`7876387`,
[E14-task1-sweep.md](E14-task1-sweep.md)).

**This report covers Tasks 2.1–2.5 and Task 3.1–3.2. Task 4 has NOT run and no credits have
been spent.** The dispatch places two advisor halts before any credit-bearing step — the canny
pair and the backdrop word — and this is that halt. Both derivations are **proposed with their
evidence and adopted by nobody here.**

**This document ranks nothing and recommends nothing.** Where it says a prediction was
falsified, that is scoring my own bet, not judging an artifact.

**Watchdog, reported either way as the dispatch requires.** Verified alive immediately before
each GPU leg and after it: heartbeat **1.1 s** before the bake / **2.0 s** after, **1.8 s**
before the renders / **1.5 s** after, all against a 15 s threshold. No `_watchdog_DEAD`, no
`_watchdog_TRIPPED` at any check. VRAM 2,029 → 2,049 MiB against the 31,200 MiB ceiling — the
ceiling was never approached and never raised. **One inherited claim did not survive contact
with the log**: the dispatch says the watchdog was restarted *this morning* after an overnight
death; `_watchdog_KILL.log` carries exactly two entries since 2026-08-06 — `watchdog up` at
2026-08-06 15:42:54 and `watchdog up` at **2026-08-07 20:29:09**, roughly five minutes before
this session's first check — and **no DEAD line for either day** (the most recent is
2026-08-05 19:36:15). A silent death leaves no line, so the death is not contradicted; the
*restart* is timestamped tonight, not this morning. Nothing here depends on it.

---

## 2.1 — the prep bake

```
blender -b -P tools/bake_hero_prep.py -- --glb E14_gate0/longsword_00001_raw.glb
        --outdir E14_prep --profile profiles/prop.json
exit 0   wall 462.9 s   5 profile values applied
```

**No ANDON fired.** Outputs: `pos.npy` / `nor.npy` / `mask.npy` (192 MB each), `meta.json`,
`prep_uv.glb` (35.6 MB). Bake variances 0.050299 / 0.057831 / 0.161115.

| quantity | value |
|---|---|
| faces (Blender) | **999,474 — identical to `mesh_stats`' 999,474, zero difference** |
| head-band faces (W3's crop rect) | **522,860 (52.31%)** |
| islands | **46,496 (21.5 faces/island)** |
| head islands | 24,172 (728,874 faces) |
| head UV-area share / face-count share | 0.7174 / 0.7293 |
| triangle UV area ("packed UV area covers") | **2.62%** |
| **valid texels @ 4096** | **3,661,903 (21.83% of atlas)** |
| head-scale identity | 0.717434943 → 0.717435002, **8.308e-08 relative** against 1.0e-06 — survived |

**The `n_head > 500` ANDON passed, and — as on the beast — the reason matters more than the
pass, but the mechanism is different and I checked it rather than repeating theirs.** On the
dragon the rect was *too big* (it selected most of the animal). Here it is **in the wrong
place**. The crop rect at `crop_res` 1024 and `bound` 0.55 selects a horizontal band running
from **40.55% to 79.22% of height above the tip**. Gate 0's landmark puts the blade shoulder at
69.46%, so the band takes a slab of blade and only the *bottom* of the hilt:

| of the 522,860 band faces | |
|---|---|
| that are **hilt** (above the Gate 0 shoulder) | **39.78%** |
| that are **blade** | **60.22%** |
| **share of the hilt the band actually covers** | **58.79%** — the pommel, the gem and the upper wrap are outside it |

The band is inert at `head-scale 1.0` under Ruling 4 and the scale-preservation assert
confirms the uniform atlas came through `pack_islands` unchanged. **It is recorded because the
ANDON's pass is not evidence the rect found anything**, and `_gates.head_rect_metrics: false`
in the profile is the decision that already covers it.

**A denominator fact that every later percentage in this report is a fraction of.** This
subject bakes **21.83% of the atlas valid from 2.62% of triangle UV area — 8.3×**, against the
ship's 6.16× and the beast's 4.41× (recomputed by one code path this session, §2.2c). The cause
is island count: 46,496 islands here against the beast's 28,870, each paying the same 8-texel
bake margin. **Most of this subject's "valid" texel budget is bake margin, not triangle
interior**, more so than on either prior subject — and §2.2c shows that is not a curiosity.

## 2.2 — the reach ceiling, pre-registered before any projection

```
e08_ceiling.py --prep E14_prep --sets 2,4,6,8,12,24 --facing-min 0.45 --head-facing-min 0.45
```

Floors are the profile's ruled values, `head-facing-min` equal to `facing-min` per Ruling 4.

| cameras (equatorial) | reachable texels | % of valid |
|---|---|---|
| 2 | 1,566,844 | 42.79% |
| 4 | 1,827,760 | 49.91% |
| 6 | 1,871,948 | 51.12% |
| **8 — the stage-1 set** | **1,879,807** | **51.33%** |
| 12 | 1,889,955 | 51.61% |
| 24 | 1,898,982 | 51.86% |

**Valid 3,661,903 · head band 1,894,691 · the pre-registered stage-1 ceiling is 51.33% of valid
at eight eye-level cameras.** Every downstream coverage number on this subject is to be read
against that, the way the ship's 42.72% and the beast's 50.46% were.

Marginal gain in turnaround order: +yaw 0 → 822,951 · +180 → +743,893 · +90 → +101,544 ·
+270 → +159,372 · +45 → +14,049 · +135 → +8,752 · +225 → +18,528 · +315 → +10,718. **The two
face-on cameras carry 83% of the total**; the six others add 17% between them, which is the
portrait geometry showing up in the coverage.

**Ruling 6e's caption caveat, quoted as required.** All three of `e08_ceiling`'s SETTINGS blocks
printed **identical ladders**, because `prop.json` sets `head-facing-min` equal to `facing-min`.
There is **one measurement in that output, not three**, and two of its captions ("head 0.18",
"uniform 0.18") are false. The repair is still in the errand batch. Likewise
`front-back OVERLAP = 0`, which cannot be non-zero at any positive floor.

### 2.2a — the ceiling's mechanism, MEASURED rather than inferred

The prediction that mattered this session (R1) was that Gate 0's hollow finding **bounds** the
ceiling: `e08_ceiling` casts a real first-hit ray, so an inner wall is unreachable by
construction, and 47.85% of this mesh's faces are inner wall. Same size is a coincidence;
identity is a mechanism. A new instrument (`tools/diagnostics/e14_atlas_anatomy.py`) attributes
every sampled valid texel to its nearest triangle and cross-tabs wall against reachability. It
reproduces `e08_ceiling`'s N8 total **exactly** (1,879,807) from an independently written
reachability path, asserted in code.

| | reachable | unreachable | share of valid |
|---|---|---|---|
| **OUTER wall** | 151,612 | 9,706 | 53.77% |
| **INNER wall** | 2,597 | 136,085 | 46.23% |

- **93.98%** of outer-wall texels are reachable.
- **1.87%** of inner-wall texels are.
- **93.34% of everything unreachable is inner wall.**

The manifold partition reproduces Gate 0 on the welded mesh — 3 pieces at 521,134 / 478,288 /
52 faces, signed volumes **+0.001593 / −0.001220** against Gate 0's +0.001603 / −0.001228 on
the raw mesh (the Blender round trip moves the fourth decimal). **The ceiling on this subject is
a topology fact, not a camera-count fact**: 24 cameras reach 51.86%, and the outer wall is
53.77% of the atlas.

**⚠ An error of mine, corrected in place rather than deleted.** The first run of that instrument
computed `face_adjacency` on `prep_uv.glb` **unwelded** and reported **50,586 "manifold-edge
pieces", largest 28,534 faces, 6.63% outer** — which is the UV island distribution wearing a
wall's name, because a Blender glTF round trip splits a vertex at every UV seam. The signed
volumes of open island patches are not a nesting test and the outer/inner labels read off them
were meaningless. Caught by comparing against Gate 0's 3 pieces before any number was reported.
This is the repo's own law in a new costume — *a number that reproduces exactly can still be
measured against the wrong object* — and the instrument now welds first, asserts the face array
is unchanged so the labels still index the raycast's primitives, and carries the reason in a
comment.

### 2.2b — the ray bias exceeds this mesh's wall thickness. Reported, not fixed.

`e08_ceiling`'s `--bias` default is **3e-3**, and this mesh's walls are **0.00196** thick
(Gate 0 §4). The ray origin is `P + N·noffs + dtc·bias`, so on the near face the bias alone
displaces the origin **1.5× the wall thickness** — through the wall it started on. That is why
1.87% of inner-wall texels read reachable. Measured:

| `--bias` | 8-camera reach |
|---|---|
| **3e-3 (the shipped default, and every prior subject's number)** | **51.33%** |
| 1e-3 | 50.56% |
| 5e-4 | 50.43% |
| 2e-4 | 50.36% |

**A 0.97-point overstatement, converging by 5e-4.** The shipped default is what every prior
subject's ceiling was measured with, so **51.33% is the comparable number and is what this
report pre-registers**; 50.4% is what the geometry says. Not changed: it is a shared instrument
whose numbers are cited in closed rulings, and the bias only bites on a subject whose walls are
thinner than it — which, per Gate 0 Ruling 3, is every subject on this route, but only visibly
where the two walls are topologically separable.

### 2.2c — the off-surface rate: the fourth point BREAKS the replication, and locates it

```
e12_offsurface.py --prep E14_prep --aspect 240,1024 --margin 1.204 --fit-axis height
one emit pixel = 1.175774e-03 canonical (fit-axis height: v_ext = z extent 0.999994 x 1.2040)
median distance 1.360e-07 (0.0001 px)   >1 px: 11.0875%   >5 px: 6.7915%   max 64.2 px
```

**11.09% against a 2.50–2.64% replication across three subjects.** The dispatch asked for a
fourth point that "tests the bake-artifact-class reading either way". Before that becomes a
subject property it has to survive the obvious alternative, so the valid mask was eroded and
the rate re-measured — **on this subject and on the beast's and ship's bakes, both still on
disk and neither written by this session**:

| population | **prop** >1px | **beast** >1px | **ship** >1px |
|---|---|---|---|
| all valid (300,000 sampled, seed 0) | **11.104%** | **2.614%** | **2.492%** |
| eroded 2 texels | **0.0085%** | **0.2201%** | **0.3908%** |
| eroded 4 texels | 0.0176% | 0.2694% | 0.5927% |
| eroded 12 texels | 0.0000% | 0.0587% | 0.2051% |
| **the 2-texel ring only** | **16.180%** | **4.500%** | **3.888%** |

**The off-surface population is the bake-margin ring, on all three subjects.** Eroding two
texels drops it by 1300× on the prop, 12× on the beast, 6× on the ship. What replicated at
2.50–2.64% was not a property of position bakes; it was two subjects with similar island-size
distributions, and this subject breaks it by packing 46,496 islands so that **68.6% of its
sampled valid texels are within 2 texels of an island edge** (against the beast's 55.9% and the
ship's 60.1%) *and* its ring is dirtier.

**What this does and does not touch.** E10 Ruling 4's finding was that the ship's off-surface
texels were *painted, not padding* — a question about strokes, which this subject has none of
and which is not re-opened here. What is offered is narrower and measured: **the bake-side rate
is a margin statistic, so it should be read against island count, and a bare percentage across
subjects is comparing atlases, not bakes.**

**A limit on the control, stated so it is not over-read.** The manifold partition separates the
two walls **only on the prop**. On the beast the largest piece holds 962,363 of 986,814 faces
and on the ship 861,420 of 939,104 — both walls inside one piece, because those subjects pinch
far more densely than this one's 121 edges. So §2.2a's wall cross-tab **cannot be run on them**,
and this report makes no claim about whether the hollow bounds their ceilings. Their "inner"
satellites carry signed volumes of ~0.000000 and are small closed shells, not walls; the
83.78% / 28.54% "inner reach" figures in `anatomy_beast.json` / `anatomy_ship.json` are
therefore **not wall statistics and must not be quoted as such.**

## 2.3 — the `thin_extent` cost curve, measured fresh

```
e12_thin_curve.py --glb E14_prep/prep_uv.glb --aspect 240,1024 --margin 1.204
                  --fit-axis height --region-a 0:23,345,216,937 --region-b 90:92,345,147,937
one emit px 1.175774e-03;  0.01 = 8.5 emit px,  0.03 = 25.5 emit px
```

**The region is the BLADE and it was derived, not guessed.** Gate 0's ratified landmark method
(E14 Ruling 2a) put the blade shoulder at 69.46% of height on this mesh; the blade is everything
below it, at full x and y extent. The two orthogonal rects agree on z to 0.0000 of height, and
**the box was drawn back onto every view and looked at** (`thin_preview/ext_y*.png`) — the red
outline runs under the quillons and follows the blade to the tip, excluding guard, wrap and
pommel. Its known impurity is the ricasso flare's lower edge, which can only push the withheld
fraction down.

**Pooled over all eight views:**

| `thin_extent` | emit px | figure withheld | **blade withheld** |
|---|---|---|---|
| **0 — the tool default an undecided profile runs** | 0.0 | **0.000%** | **0.000%** |
| 0.002 | 1.7 | 0.553% | 0.591% |
| **0.005 — the beast's value** | 4.3 | 2.475% | 2.715% |
| **0.01 — the ship's value** | 8.5 | 6.847% | 7.095% |
| 0.02 | 17.0 | 24.966% | 26.407% |
| **0.021 — the blade's own measured thickness** | 17.9 | 27.767% | 29.539% |
| **0.03 — the character's value** | 25.5 | **59.011%** | **63.710%** |
| 0.04 | 34.0 | 81.116% | 85.478% |

**Per view, the blade region — and this is the shape of the answer:**

| `thin_extent` | y0 (face-on) | y45 | **y90 (edge-on)** | y135 | face-on ÷ edge-on |
|---|---|---|---|---|---|
| 0.005 | 1.53% | 3.54% | 2.06% | 3.76% | 0.74× |
| 0.01 | 6.79% | 8.10% | 3.21% | 8.60% | 2.12× |
| 0.015 | 22.01% | 12.58% | 4.16% | 13.34% | 5.29× |
| **0.02** | **46.70%** | 19.10% | **5.38%** | 19.36% | **8.69×** |
| 0.021 | 54.27% | 20.26% | 5.62% | 20.40% | 9.66× |
| 0.03 | **88.37%** | 61.82% | **10.29%** | 63.39% | 8.59× |
| 0.04 | 100.00% | 93.83% | 21.60% | 93.56% | 4.63× |

Views 4/5/6/7 reproduce 0/1/2/3 exactly.

**Three things the curve says, offered as data:**

1. **The transition is centred on the blade's own measured thickness.** Gate 0 measured the
   blade as a hollow box section, total outer-to-outer ~0.0208 at mid-blade, by cross-section
   clustering. This screen-space extent probe puts face-on blade withholding through 50% at
   **0.021**. Two independent measurements on different code paths agreeing on the same
   number.
2. **The character's 0.03 withholds 88% of the blade face-on and 59% of the whole figure.** The
   inherited value is not merely wrong here; it deletes the subject's dominant surface from
   diffusion on the views that carry it.
3. **The withheld fraction is strongly view-dependent, and the direction inverts.** Below
   0.0075 the *edge-on* views withhold more (the blade's own rim); above it the *face-on* views
   withhold vastly more (the blade's thickness). A single value cannot be judged from a pooled
   number on this subject.

**The box-section caveat holds and is visible in the table**: the probe reads outer-to-outer, so
nothing at all responds to the ~0.00196 wall — 0.002 withholds 0.591% of the blade, flat and
empty, not a cliff. **No value is adopted here and no gate arms on any of it.**

## 2.4 — the elevated-camera question, and the 7b law changing the answer

```
e12_elevated.py --glb E14_prep/prep_uv.glb --up-min 0.5 --base 0,45,90,135,180,225,270,315
up-facing (nz > 0.50): 79,308 faces, area 0.026992 of 0.372654 total (7.24%)
```

**Ray density quoted, per the 7b law — and on this subject it is not a footnote, it is the
result.** `e12_elevated` takes its ray grid from `--aspect`, and this subject's frame is 240 px
wide:

| frame | one px | ray cell ÷ mean face | rays per mean face | **eye-level eight reach** | best elevated pair, cumulative |
|---|---|---|---|---|---|
| **240×1024 — the profile frame** | 1.1758e-03 | **3.71×** | **0.27** | **13.851%** | 25.460% (0/180 @ 55) |
| 960×4096 | 2.9394e-04 | 0.23× | 4.32 | **51.526%** | 55.551% (0/180 @ 40) |
| 1440×6144 | 1.9596e-04 | 0.10× | 9.71 | **53.920%** | 55.639% (0/180 @ 40) |

**At the profile frame the grid is 3.7× coarser than the mesh's mean face (3.73e-07), and the
answer is wrong by a factor of 3.9.** Faces smaller than a ray cell are hit only by luck, and
this subject's up-facing faces are exactly the small horizontal steps — coil grooves, nick
scoring, stepped quillon ends. At adequate density the numbers converge (51.5% → 53.9% for 2.25×
more rays; the elevated winner's cumulative moves 0.09 points).

**The converged measurement:**

- Up-facing surface is **7.24% of total area**; the eye-level eight already reach **53.92%** of it.
- The best elevated pair (**0/180 @ 40**) adds **+1.72 points of up-facing area = +0.12 points
  of the figure's total surface area**.
- A second round adds **+0.015 points of up-facing**.
- **E06 superset check**: the round-1 winner at either elevation lies inside `cull_unseen`'s
  26-camera default — **no union re-issue is needed** whichever way this is ruled.

**The symmetric population the instrument does not measure, offered because the question as
posed is one-sided.** This subject carries **76,641 down-facing faces at 7.01% of area** —
within 3% of the up-facing population — the quillon undersides, the guard underside (which the
fixture names as part of L2), and the collar rings' lower faces. No candidate camera set in this
instrument addresses them, and no camera below the horizon exists anywhere on this route.
Measured and reported; **the disposition is the advisor's and I am not proposing one.**

**A prediction I should not have made:** my E3 wrote "the honest disposition is NONE." Whether
the numbers warrant a camera is a decision, not a measurement, and it was not mine to predict.
The numeric half of that prediction is scored in §5; the disposition half is withdrawn as out of
role.

## 2.5 — the mirror check, and half of it turns out to be a tautology

```
silhouette_masks.py --profile prop.json     (from the MESH by raycast, not by keying)
```

| view | yaw | silhouette px | % of frame | bbox |
|---|---|---|---|---|
| **0** | 0° | **49,775** | **20.2535%** | 192×850 |
| 1 | 45° | 40,101 | 16.3171% | 142×850 |
| **2** | 90° | **24,153** | **9.8279%** | 54×850 |
| 3 | 135° | 40,331 | 16.4107% | 142×850 |
| 4 | 180° | 49,775 | 20.2535% | 192×850 |
| 5 | 225° | 40,101 | 16.3171% | 142×850 |
| 6 | 270° | 24,153 | 9.8279% | 54×850 |
| 7 | 315° | 40,331 | 16.4107% | 142×850 |

**Within "mirror pairs": exact to the pixel — and that is a check that cannot fail.** The pairs
that come back identical are (0,4), (1,5), (2,6), (3,7), which are the **opposite-direction**
pairs. Under orthographic projection the silhouette from direction **d** and from **−d** is the
same shape mirrored, so their areas are equal **for any mesh whatsoever**. It carries no
information about this subject's symmetry, and the dispatch's expectation of "near-equality
within mirror pairs" is satisfied by construction rather than by the sword being symmetric.

**The comparison that does carry information is 1 vs 3** (yaw 45 against yaw 135 — related by
the bilateral mirror plane, not by opposition): **40,101 against 40,331, 0.57% apart.** That is
this subject's bilateral symmetry, quantified, and it is the whole of the symmetry evidence in
this table.

**Across mirror pairs: NOT near-equal.** `area(view 0) / area(view 2) = 2.061×`. The dispatch's
parenthetical expected near-equality across pairs too; it does not hold. **Any instrument that
normalises by per-view silhouette area on this subject inherits a denominator that swings 2.06×
between views** — larger than the beast's 1.65×, and the fifth moving-denominator instance in
this repo. The E12 9b/16f caveats apply here in that sharper form.

---

## 3.1 — the canny pair, DERIVED. Proposed to the advisor; adopted by nobody here.

**The replica is anchored to the shipped tool's own digits, with no skip flag.**
`restylize_views.py --emit-only --profile prop.json` (which leaves canny at its 0.4/0.8 defaults,
since the profile deliberately carries no value) printed the control it would build, and
`e12_canny_derive` reproduced **all eight** exactly:

```
[anchor] view 0 at 0.40/0.80: replica 5258 px  recorded 5258 px  MATCH   ... 8 of 8 MATCH
```

**The falsified pair, on this subject's own renders:**

| view | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| control px | 7,885 | 6,883 | 6,009 | 8,475 | 8,277 | 7,095 | 5,571 | 8,280 |
| canny | 5,258 | 4,403 | 3,914 | 5,977 | 5,662 | 4,624 | 3,483 | 5,781 |
| contour | 4,776 | 4,516 | 3,892 | 4,536 | 4,776 | 4,516 | 3,892 | 4,536 |

Note that **contour is mirror-identical and canny is not** — the mask is orthographically
symmetric (§2.5) while the shading is not.

**The ladder** (pooled over eight views; W-columns are the worst view at that rung):

| pair | canny sum | admitted vs REF | W-band | W-flat12 | W-speckle | median admitted component |
|---|---|---|---|---|---|---|
| **0.40/0.80 (the profile's falsified pair)** | **39,102** | — | — | — | — | — |
| 0.30/0.65 | 45,068 | 5,966 | n/a | 0.00% | 13.12% | 4.0 |
| 0.20/0.45 | 53,062 | 13,960 | n/a | 0.00% | 6.59% | 7.0 |
| 0.15/0.35 | 57,505 | 18,403 | n/a | 0.00% | 6.24% | 7.0 |
| 0.12/0.30 | 59,849 | 20,747 | n/a | 0.00% | 6.59% | 7.0 |
| **0.10/0.25** | **62,022** | **22,920** | n/a | **0.05%** | 6.84% | 7.0 |
| 0.08/0.20 | 63,904 | 24,802 | n/a | 0.22% | 6.82% | 6.0 |
| 0.05/0.15 | 66,643 | 27,541 | n/a | 0.37% | 7.01% | 5.0 |
| 0.03/0.09 | 71,112 | 32,010 | 0.82% | 1.80% | 7.44% | 5.0 |
| 0.02/0.06 | 74,675 | 35,573 | 3.92% | **4.39%** | 8.26% | 4.0 |

**W-outside is 0.000% at every one of the 120 rows, and that is a check that cannot fire in this
configuration** — the control composites onto `--bg 0,0,0` through the exact mesh silhouette, so
outside the figure the image is uniform black and Canny has nothing to find. Reported as
structurally zero rather than as a clean result.

### The works-perfectly test, run FIRST as the dispatch requires — and the crops are the gate

**What the shipped pair loses.** `CONTROL_SHEET_0.png` stacks the four candidates full-frame. At
**0.40/0.80 the control is a bare outline** — silhouette, quillon edges, pommel outline and two
blade lines. `CROP_0_hilt-wrap-boss.png` at 5× shows it directly: the wrap's helical turns, the
collar ring and the diamond boss are **almost entirely absent** from the reference set (blue),
and every candidate rung admits them (orange). The interior edge share confirms it — the eroded
interior carrying an edge runs **4.55–11.28%** at 0.40/0.80 against **15.20–20.33%** at
0.10/0.25.

**What the low rungs admit that is NOT relief — the prediction, and where it landed.** I
pre-registered that this subject's flat fields are the blade faces and that the bottom rungs
would put wandering contours down them. `CROP_0_blade-flat-field.png` and
`CROP_0_blade-tip-ridge.png` at 5×:

- **0.02/0.06** — a long broken vertical wander down the middle of the left blade facet, and a
  scatter of short fragments across both facets near the tip, in regions the render shows as
  smooth gradient with no relief. W-flat12 peaks at 4.39% and W-band at 3.92% here.
- **0.05/0.15** — most of the scatter gone; fragments remain at the top of the flat field.
  W-flat12 0.37%.
- **0.10/0.25** — the flat fields are clean. What remains is the central ridge, the fuller line
  and one horizontal nick scar, all visible as relief in the render beside them. W-flat12 0.05%.

**The evidence, assembled, with no pair chosen:**

| | favours a LOWER pair | favours a HIGHER pair |
|---|---|---|
| the wrap's coil relief | absent at 0.40/0.80; fully present from 0.10/0.25 down | — |
| the blade's flat fields | — | wander present at 0.02/0.06 and 0.03/0.09; gone by 0.10/0.25 |
| W-flat12 | — | 4.39% → 1.80% → 0.37% → **0.05%** across 0.02/0.06 → 0.10/0.25 |
| W-band | — | has content only at the two lowest rungs; 3.92% at 0.02/0.06 |
| W-speckle | flat 6–7% across the middle of the ladder | 8.26% at the bottom rung; edge-on views (2, 6) worst at every rung |

**The two crops bracket the same interval from opposite sides**: relief is fully recovered at or
below 0.10/0.25, and flat-field artifact is gone at or above it. **That is what the measurement
says; which pair the route adopts is the advisor's ruling and this session halts here.** Crops
for three candidates and full-frame control sheets for all eight views are staged.

## 3.2 — the backdrop derivation. Proposed to the advisor; the WORD is not chosen here.

Input: `canon/longsword-materials-estimated.json` — five sRGB estimates read off the fixture's
words, the weakest link in the chain and superseded by the styled pair under the fixture's own
non-circularity rule. **L1's slight cool cast is the one estimate that is not purely a guess**:
the repo has measured this material class at C\* 1.6–2.8 at hue 267, so the direction is the
measured class, not a taste call.

**L1 is deliberately NOT flagged thin, and the file says why** — this is the beast's D3 decision
repeated in the same shape. The dispatch asks the derivation to weight toward L1 because S-steel
holds the risk; that concern is *colour proximity of a large surface*, not *antialiasing of a
small one*, and the flag's name describes the latter. Setting it would attach the right weight
for a reason the flag does not describe — the "condition whose stated derivation does not
describe it" failure. So L1 carries weight 1 and its distance is reported at every optimum. A
second L1 fact is recorded rather than encoded: **the blade IS thin in the flag's own sense on
views 2 and 6**, where it is a sliver a few px wide — but the flag is per-element and that
property is per-view.

```
e04_backdrop.py --materials canon/longsword-materials-estimated.json  (grid 26, thin-weight 2.0)
```

| | rgb | L\* | sat | weighted-min | binds (weighted) | raw-min material |
|---|---|---|---|---|---|---|
| metric optimum | (0, 0, 235) | 29.3 | **0.920** | 0.3941 | L3 gold | L1 steel (0.6000) |
| best low-saturation | (214, 214, 255) | 86.9 | 0.160 | **0.3549** | L3 gold | L1 steel (0.3804) |
| best neutral | (255, 255, 255) | 100.0 | 0.000 | **0.3549** | L3 gold | L1 steel (0.4118) |

**The metric optimum is a full-saturation blue and is disqualified** by the standing rule, and
reported because the metric does not know that rule.

**⚠ The derivation as configured optimises against GOLD, not steel.** L1 is the **raw** minimum
at all three optima, but the **weighted** metric is bound by **L3 at every one of them**, because
L3 is thin-weighted 2.0 and gold is the hardest material to escape with a light backdrop. The
dispatch's instruction to weight toward L1 and the metric's actual binding constraint are not
the same thing. Stated plainly because a ruling that reads "L1 binds" off the `<== MINIMUM`
marker would be reading the raw column.

### The occupancy check — CHECKED, not assumed (the 8a/15i lesson)

A chroma floor of C\* 5.0 is applied **before any hue is quoted**, because below the floor a hue
is not a colour:

| element | L\* | C\* | hue | verdict |
|---|---|---|---|---|
| L1 battle-worn steel | 63.1 | **3.0** | **UNDEFINED** | below the floor — occupies NO hue |
| L2 blackened iron | 19.0 | **1.4** | **UNDEFINED** | below the floor — occupies NO hue |
| L3 gold diamond boss | 68.1 | 49.8 | 83.5 | warm yellow |
| L4 oxblood grip wrap | 24.2 | 32.7 | 25.4 | red / wine |
| L5 dark garnet pommel | 24.4 | 44.1 | 24.3 | red / wine |

| hue band | occupied by |
|---|---|
| red / wine (0–40) | L4, L5 |
| orange (40–70) | **UNOCCUPIED** |
| warm yellow (70–105) | L3 |
| green (105–175) | **UNOCCUPIED** |
| cyan (175–225) | **UNOCCUPIED** |
| **blue-violet (225–300)** | **UNOCCUPIED** |
| magenta (300–360) | **UNOCCUPIED** |

**The fixture's pre-registered expectation — "blue-violet is unoccupied" — is CONFIRMED**, and
the check found more than the expectation: **five of seven bands are unoccupied**, because two of
the five elements carry no hue at all. **L1 and L2, the subject's two largest surfaces, cannot be
separated from a backdrop by hue under any choice** — only by lightness. That is S-steel stated
in the derivation's own arithmetic.

### The metric does not choose the hue, and here it barely chooses at all

| family | rgb | L\* | C\* | weighted-min |
|---|---|---|---|---|
| **neutral** | (245, 255, 255) | 99.3 | 3.5 | **0.3549** |
| **blue-violet** | (214, 214, 255) | 86.9 | 21.4 | **0.3549** |
| **cyan** | (214, 255, 255) | 97.3 | 13.7 | **0.3549** |
| **magenta** | (224, 214, 255) | 87.6 | 21.7 | **0.3549** |
| green | (224, 255, 245) | 97.6 | 11.9 | 0.3349 |
| red / wine | (255, 235, 235) | 94.5 | 7.3 | 0.3149 |
| warm yellow | (255, 245, 235) | 97.0 | 6.4 | 0.3149 |
| orange | (255, 235, 224) | 94.2 | 9.1 | 0.2949 |

**Four families tie to four decimal places**, all bound by L3 at the same 0.7098 — the blue-channel
gap to gold. The spread across all eight is 0.0600. As on the beast, **the hue is not decided by
this derivation**; unlike the beast, the top four are not merely close but *identical*.

### The inherited candidates, scored on this subject's own table

| backdrop | weighted-min | raw-min | binds |
|---|---|---|---|
| **W3's mid grey 0.42** | 0.1688 | 0.1996 | L5 |
| **the galleon's white** | **0.3549** | 0.4118 | L3 |
| black | 0.1882 | 0.1882 | L2 |
| **the beast's lavender-grey (121,121,172)** | **0.1255** | 0.1255 | **L1** |

**The most recently ruled backdrop on this route is the worst of the four here**, bound by steel
— which is what "derived per subject, never inherited" looks like when it is measured. And
**the galleon's white does not merely transfer: it *is* the neutral optimum**, tying the best
low-saturation option exactly. That inverts the beast's result, where white scored 0.0961 and
was worse than every derived option.

### ⚠ The sensitivity that the ruling needs, because the estimate is the weak link

L1 is near-achromatic, so a backdrop can only escape it by **lightness** — and L1's lightness is
the single estimate a styled pair is most likely to move, since worn steel under harsh
directional light can come back anywhere. Every other element carries chroma and is separable in
hue as well. Sweeping L1's grey level:

| L1 grey | L1 L\* | white: score / L1 dist | pale blue-violet: score / L1 dist | W3 grey: score / L1 dist |
|---|---|---|---|---|
| 60 | 26.5 | 0.3549 (L3) / 0.765 | 0.3549 (L3) / 0.733 | 0.1688 (L5) / 0.185 |
| 90 | 39.4 | 0.3549 (L3) / 0.647 | 0.3549 (L3) / 0.616 | **0.0671 (L1) / 0.067** |
| 120 | 51.5 | 0.3549 (L3) / 0.529 | 0.3549 (L3) / 0.498 | **0.0820 (L1) / 0.082** |
| **150 — the estimate** | **63.1** | **0.3549 (L3) / 0.412** | **0.3549 (L3) / 0.380** | 0.1688 (L5) / 0.200 |
| 180 | 74.3 | 0.2941 (**L1**) / 0.294 | 0.2627 (**L1**) / 0.263 | 0.1688 (L5) / 0.317 |
| 210 | 85.2 | 0.1765 (**L1**) / 0.176 | 0.1451 (**L1**) / 0.145 | 0.1688 (L5) / 0.435 |
| 235 | 94.0 | **0.0784 (L1) / 0.078** | 0.0941 (**L1**) / 0.094 | 0.1688 (L5) / 0.533 |

Two things fall out, both offered as data:

1. **A light backdrop's advantage is contingent on steel being mid-grey.** From L1 L\* ≈ 74
   upward, steel becomes the binding constraint and the score collapses — at L\* 94 white sits
   at 0.078, a whisker above the key's own 0.06 cut. The estimate is most likely to be wrong in
   exactly that direction.
2. **W3's grey lands nearest the key's cut precisely where steel is mid-grey** (0.067 at L1
   L\* 39, 0.082 at L\* 51) — the grey-on-grey trap arriving on schedule, at the lightness band
   where it was always predicted to.

**No word is chosen here.** The optimum table, the occupancy check, the four-way tie, the
inherited scores and the sensitivity are the evidence; the ruling is the advisor's, and the
fixture's non-circularity rule says the styled pair supersedes this table the moment it exists.

---

## 4. Predictions scored

**Task 1's eight are scored in [E14-task1-sweep.md](E14-task1-sweep.md) §6 (8 of 8 held, with
the caveat that they were predictions about a just-authored file). The thirty below are about a
subject nobody had measured. 19 held, 11 falsified.**

| # | prediction | outcome | measured |
|---|---|---|---|
| Q1 | bake exit 0, no ANDON | **held** | exit 0, 462.9 s |
| Q2 | n_head 250,000–480,000 | **FALSIFIED** | **522,860** — I assumed near-uniform face density along the blade; faces concentrate in the band |
| Q3 | the band is mid-height, not the hilt; misses pommel/gem/upper wrap; ~29% of height of blade | **held, all clauses** | band = 40.55–79.22% of height; 60.22% of its faces are blade; it covers 58.79% of the hilt |
| Q4 | native UVs, no re-unwrap | **held** | as logged |
| Q5 | valid texels 2.7M–3.5M | **FALSIFIED, high** | **3,661,903** — and §2.1 locates it: 46,496 islands make the atlas margin-dominated at 8.3× |
| Q6 | head-scale-1.0 identity passes | **held** | 8.308e-08 relative against 1e-06 |
| Q7 | Blender face count within 50 of `mesh_stats` | **held, stronger** | **exactly equal** (the beast differed by 11) |
| R1 | 8-camera ceiling 40–53%, bounded by the hollow | **held, and the mechanism measured** | **51.33%**; 93.34% of unreachable texels are inner wall |
| R2 | 12 cameras add < 1.5 pts; 24 does not break 53% | **held** | +0.28 pts; 24 → 51.86% |
| R3 | reachable ÷ outer-wall share > 0.85 | **held** | **93.98%** of outer-wall texels reachable |
| R4 | three SETTINGS blocks, one measurement, two false captions | **held** | identical ladders ×3 |
| R5 | front-back OVERLAP = 0, cannot be non-zero | **held** | 0 |
| R6 | off-surface 2.2–3.0% | **FALSIFIED** | **11.0875%** — and §2.2c locates it as bake margin on all three subjects |
| R7 | emit px smaller than the ship's 1.12e−03 | **FALSIFIED — direction wrong** | **1.1758e-03**, *larger*: a height-fit portrait subject spans the full canonical extent |
| T1 | monotone; 0.0 withholds nothing | **held** | 0.000% |
| T2 | 0.03 withholds > 80% of the blade face-on | **held** | **88.37%** |
| T3 | 0.01 withholds < 15%; 0.005 < 6% | **held** | 8.60% / 3.76% worst view |
| T4 | face-on ÷ edge-on blade ratio at 0.02 exceeds 3× | **held, far exceeded** | **8.69×** |
| T5 | nothing responds to the 0.00196 wall | **held** | 0.002 → 0.591%, flat |
| T6 | figure withheld at 0.03 > 45% face-on | **held** | **78.42%** |
| E1 | up-facing area < 3% of total | **FALSIFIED** | **7.24%** |
| E2 | eye-level eight reach > 55% of up-facing | **FALSIFIED at every density** | 13.85% at the profile frame, **53.92%** converged — narrowly under |
| E3 | best elevated camera adds < 1.5 pts of total coverage | **held** (numeric clause) | **+0.12 pts** of total surface at converged density |
| E3b | *"the honest disposition is NONE"* | **WITHDRAWN** | not a measurement and not mine to predict |
| E4 | ray density quoted with every first-hit figure | **held — and it changed the answer** | 0.27 → 4.32 → 9.71 rays per mean face |
| M1 | within-pair areas near-equal | **held, but the check cannot fail** | exact to the pixel; true for any mesh under orthographic projection |
| M1b | 1/3/5/7 within 3% | **held — and this is the real symmetry evidence** | 40,101 vs 40,331, **0.57%** |
| M2 | area(0)/area(2) > 2.5× | **FALSIFIED** | **2.061×** — still the largest denominator swing this route has measured |
| M3 | view 0 largest, 2 or 6 smallest | **held** | 20.25% / 9.83% |
| C1 | contour dominates; canny < 25% of control px | **FALSIFIED** | canny is **66.7%** of view 0's control px — the composite-onto-contrast fix means the clay's relief *does* reach Canny; I imported the pre-fix mechanism |
| C2 | control px rises monotonically as the pair falls | **held** | 39,102 → 74,675 |
| C3 | the bottom rungs' garbage is in the blade's flat fields | **held — seen in two crops** | wander at 0.02/0.06, gone by 0.10/0.25; W-flat12 4.39% → 0.05% |
| C4 | the central ridge survives at mid rungs | **held** | present at 0.10/0.25 with the fuller and a nick scar |
| C5 | the pair is proposed, not adopted | **held** | halting |
| B1 | metric optimum saturated and disqualified | **held** | sat 0.920, rgb(0,0,235) |
| B2 | L1 steel binds the low-saturation optimum | **HALF — and the failing half matters** | L1 binds **raw** at all three optima; **L3 gold binds the weighted metric at all three** |
| B3 | low-sat optimum's L\* more than 25 points from steel's | **FALSIFIED, narrowly** | 86.9 − 63.1 = **23.8** |
| B4 | blue-violet genuinely unoccupied, checked | **held, and exceeded** | confirmed; **five of seven bands** unoccupied, two elements carry no hue at all |
| B5 | hue families span < 0.03 of score | **FALSIFIED as bounded** | green→blue-violet→warm spans **0.0400** — but the top **four** families tie **exactly** |
| B6 | W3 grey and galleon white both score badly | **FALSIFIED on white** | white **is** the neutral optimum at 0.3549; grey 0.1688 |
| W2 | profile renders pixel-identical to Gate 0's | **held exactly** | max |Δ| = 0 on all eight, compared by pixels not bytes |

**Where I was most wrong, and it is one error twice.** Q5 and R6 are the same mistake: I
predicted atlas-level quantities by scaling from the ship and beast without asking what their
**island counts** were. This subject packs 46,496 islands against the beast's 28,870, and both
the valid-texel count and the off-surface rate are dominated by that one number. Both misses
were productive — chasing R6 is what produced §2.2c and overturned a route-wide reading — but
the direction of the error is the same as Gate 0's P8/P9/P25: **pricing the prior instead of
measuring the subject.** Third arc in a row.

**Where a prediction earned its keep.** R1 named a *mechanism* rather than a number, said what
would have to be true for it (the unreachable set must BE the inner wall, not merely resemble
it in size), and the instrument written to test it caught my own bad assumption before any
number was reported. C3 named where to look and the crops showed it there. T4 predicted an
8.69× view dependence at 3× and was under by nearly 3×, in the right direction.

## 5. What has NOT run

- **Task 4 — the styled target pair.** Not started. **No generation, no `estimate_credits`, no
  submission, no credits spent.** The dispatch places a real halt after Task 3 and this is it.
- **The one-string-vs-per-view check (W1/W3-p)** is a Task 4 item and is unscored. The carried
  flag about views 2/6 is **not** imported: the renders are staged, the check runs against them
  at build time, and the crop at `CROP_2_blade-edge-on.png` is the only edge-on look this
  session took.
- **No value was written to any profile or fixture.** `thin_extent`, the canny pair, the
  backdrop word and `cameras.elevated` all remain `_still_suspended`.
- **No gate was armed on anything measured here** — not the thin curve, not the ceiling, not the
  mirror areas, not the W-columns.
- **`e08_ceiling`'s `--bias` default was not changed** (§2.2b) and `e12_offsurface` was not
  edited: shared instruments whose numbers are cited in closed rulings.
- **`e12_elevated`'s ray grid was not changed** — the finding is reported with the arithmetic
  and the convergence, and the fix is a decision about a shared instrument.
- **Nothing in the E12/E13 lane was touched.** No file under `E13_stroke/` or `E13_stage1/` was
  opened; the beast's and ship's prep bakes were **read** for the §2.2c control and not written.
- **No memory-store write.** The repo is the record.

## 6. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Two driver `.ps1` files staged so the GPU legs replay from the record; every invocation, exit code, wall time, VRAM before/after and profile-value count in `prep.log` / `renders.log`; every measurement lands in a JSON beside its artifact (`ceiling.json`, `offsurface.json`, `atlas_anatomy.json`, `thin_curve.json`, `blade_region.json`, `elevated*.json`, `canny_sweep.json`, `backdrop/*.json`); the off-surface pixel unit derived with its operands printed; the blade region derived from Gate 0's landmark by a recorded script rather than by hand |
| ANDON_AUTHORITY | **3** | Watchdog verified before and after both GPU legs; the bake's character-written ANDONs pre-stated as halt-not-tune and reported as passed-**with-reason** rather than passed; the canny replica's eight anchors are a no-skip gate that had to pass before a sweep row was written; the thin-curve region's z-agreement ANDON ran; **this is the dispatch's halt and it is being taken with both derivations unadopted** |
| NAMED_COMPENSATORS | **2** | New files only — three new instruments in `tools/diagnostics/` (per Ruling 2a's ratified practice), one new canon estimates file, artifacts under `E14_prep/`, three new docs. Nothing pre-existing opened for writing. **No spend of any kind.** Undo for the instruments and the estimates file is `git revert`; undo for the artifacts is deleting `E14_prep/`. Not 3: the estimates file is under `canon/`, which is a shipped-fixture directory rather than an experiment tree — declared rather than banked |
| DECOMPOSE_BY_SECRETS | **3** | Every value derives from this mesh or this fixture; the emit-pixel unit and the thin curve's frame come from this subject's ruled framing, not another's `cam.json`; the L1 weighting question answered by *not* overloading a flag whose name describes a different mechanism, and handed up as a named decision instead; `edge-ref` deliberately not re-derived; the beast/ship bakes used only as controls for a method, never as sources of a value |
| UNCERTAINTY_GATED_HUMANS | **3** | Nothing is adopted. The canny pair is presented as an interval bracketed from two sides by two crops, with no pair named; the backdrop is presented as a four-way exact tie plus the sensitivity that decides how much the tie matters, with no word named; the thin curve's value is explicitly left to its own ruling; the elevated disposition is left open **and my own prediction of it withdrawn as out of role** |
| EXTERNAL_VERIFIER | **3** | The canny replica reproduces `restylize_views`' own printed digits on all eight views before any row is trusted; `e14_atlas_anatomy` reproduces `e08_ceiling`'s N8 total exactly from independently written code, asserted in-file; its wall partition reproduces Gate 0's on the welded mesh (3 pieces, signed volumes to the third decimal) — **and the first version's failure to do so is what caught my own error**; the off-surface reading was tested on two bakes this session did not write; the ceiling's bias sensitivity was measured at four values rather than argued; the profile renders were compared to Gate 0's **by pixels, not by file bytes** |

---

## HALT — the advisor's two rulings, then Task 4

Staged at `E:\AI\training\facet_next\E14_prep\`:

```
prep.log · renders.log · E14_prep_bake.ps1 · E14_profile_renders.ps1
pos/nor/mask.npy · meta.json · prep_uv.glb
ceiling.json · offsurface.json · atlas_anatomy.json · anatomy_beast.json · anatomy_ship.json
thin_curve.json · blade_region.json · thin_preview/ext_y*.png   (the region drawn on, checked)
elevated.json · elevated_4x.json · elevated_6x.json
renders/swordclay_*.png · masks/swordclay_*.png + silhouettes.json · control_ref/
canny/CONTROL_SHEET_{0..7}.png · canny/CROP_*.png · canny/canny_sweep.json · canny_ladder.log
backdrop/backdrop.json · backdrop/checks.json
```

New in the repo: `tools/diagnostics/e14_atlas_anatomy.py`, `tools/diagnostics/e14_backdrop_checks.py`,
`canon/longsword-materials-estimated.json`, and this report.

**Two decisions are waiting and neither is mine:**

1. **The canny pair.** The two crops bracket an interval from opposite sides — relief fully
   recovered at or below 0.10/0.25, flat-field artifact gone at or above it. The full-frame
   control sheets for all eight views and the 5× crops for three candidates are staged for the
   eye, which is the gate here.
2. **The backdrop word.** Four hue families tie to four decimal places; the derivation is bound
   by gold rather than by steel; blue-violet is confirmed unoccupied along with four other
   bands; and the whole answer is contingent on L1's estimated lightness in a way §3.2's
   sensitivity table makes explicit.

**Task 4 runs after both land.** Two further items are flagged for the advisor independently of
those rulings: **§2.2c**, which reads a route-wide off-surface claim differently after testing it
on three bakes, and **§2.4's ray-density result**, which changed an elevated-camera answer by a
factor of 3.9 and is a property of a shared instrument on a portrait subject class.
