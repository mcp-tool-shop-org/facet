# E14 handoff 6 — the COMPLIANT re-projection: six twins

**Executor session, 2026-08-08.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 21c.
Predictions committed blind in `0c93314`, before the ceiling ran. The comparison is the
seven-run, [E14-handoff5-report.md](E14-handoff5-report.md) (`05b087d`) — a record, not
overwritten by anything here.

**Nothing is judged here. No pass condition exists** — the ceilings are comparables and the
eye is the gate. **No generation, no credits**; ceiling, projection, diff and readouts are
local CPU, with one Blender leg for the pack and the FLAT renders.

---

## 1. ⚠ THE SIX-CAMERA CEILING, pre-registered before any projection

*This section was written and committed before `project_twins` ran.*

Cameras 0/45/135/180/225/315 (views 0/1/3/4/5/7). The instrument is the same fallback the
seven-run used — `e14_atlas_anatomy --views`, because `e08_ceiling --sets N` can only
express full equatorial rings — plus a second file that re-derives the same definition
independently. **Three anchors were asserted before a six-camera number existed:**

```
[reach6] ANCHOR: N8 1,879,807 and N7 1,877,487 reproduce EXACTLY from the same definition
[reach6] ANCHOR: all seven saved per-view reach masks reproduce texel-for-texel
[reach6] ANCHOR: N6 < N7 < N8 holds and N6 is a strict subset of N7
```

The second is new here and is the stronger one: this session's per-yaw reach masks are
compared against the seven-run's saved `reach_per_view.npy` **texel for texel**, not by
total. A definition that drifted between sessions but happened to keep its sum would pass
an anchor on totals and fail this one. Zero differences on all seven.

Ray bias stays the shipped 3e-3 for comparability, with **Ruling 10b's caveat** unchanged:
that bias exceeds this route's ~0.00196 wall floor and is worth +0.97 points at N8.

| | cameras | reachable | % of valid |
|---|---|---|---|
| **THIS RUN'S DENOMINATOR** — 0/45/135/180/225/315 | **6** | **1,867,754** | **51.0050%** |
| the seven-run's denominator — + yaw 270 | 7 | 1,877,487 | 51.2708% |
| the route-comparable — all eight | 8 | 1,879,807 | 51.3342% |

Two independent code paths return 1,867,754: the `e14_atlas_anatomy` invocation and this
session's own reach script, which also asserts that the six-view marginal ladder closes on
N6 exactly.

### 1b. ⚠ View 6's exact exclusive price: 9,733 texels = 0.2658 points

Ruling 20c priced view 6's exclusion at *"~4.4 points"* and Ruling 21b already flagged that
figure as the same ladder-position error class as 18c's 2.8. Measured as a set-level loss:

| quantity | texels | points of valid |
|---|---|---|
| yaw 270's own reach, alone | 473,595 | 12.9330 |
| **of that, reachable by NO other view in the set** | **9,733** | **0.2658** |
| N7 − N6 (same number, computed the other way) | 9,733 | 0.2658 |
| Ruling 20c's carried price, ~4.4 points | ≈ 161,124 | 4.4 |
| for comparison — yaw 90's exclusive (N8 − N7) | 2,320 | 0.0634 |
| both edge-on cameras out (N8 − N6) | 12,053 | 0.3291 |

**Ratio: 16.6× overstated as a set-level cost.** The carried price is retired by
measurement, in the same form 18c's was.

### 1c. ⚠ The two edge-on cameras are NOT the same kind of camera

The seven-run's explanation for yaw 90's small exclusive was angular: *"a surface whose
normal points at yaw 90 clears the 0.45 facing floor from both yaw 45 and yaw 135"*. I
carried that mechanism into the prediction for yaw 270 unchanged. **It is the wrong
mechanism for this camera**, and the instrument says so directly — for each of the 9,733
texels only yaw 270 reaches, the best facing available from the remaining six:

| why the other six miss it | texels | share |
|---|---|---|
| best facing is BELOW the 0.45 floor (the angular story) | 1,818 | **18.7%** |
| best facing CLEARS the floor but **the ray is OCCLUDED** | 7,915 | **81.3%** |

**Median best facing among the exclusive texels is 0.919, maximum 1.000.** These are not
grazing surfaces the diagonals can barely see; they are surfaces the diagonals face nearly
head-on and *cannot reach*, because something is in the way. View 6's exclusive value on
this subject is **occlusion relief, not angle** — which is a different property from view
2's, and it is why yaw 270's price is 4.2× yaw 90's rather than equal to it.

Where that occlusion is, and what it costs in paint rather than in reach, is §4's job.

### 1d. The price law fires again inside this session

The six-view marginal ladder, turnaround order:

| view | yaw | own reach | added | cumulative % |
|---|---|---|---|---|
| 0 | 0 | 822,951 | 822,951 | 22.47% |
| 1 | 45 | 576,939 | 93,484 | 25.03% |
| 3 | 135 | 519,265 | 457,545 | 37.52% |
| 4 | 180 | 743,893 | 314,889 | 46.12% |
| 5 | 225 | 592,390 | 142,228 | 50.00% |
| 7 | 315 | 671,237 | **36,657** | 51.01% |

**View 7's marginal is 36,657 here against 10,718 in the seven-run** — the same camera, the
same subject, the same floor, 3.4× apart, because view 6 no longer arrived before it.
Nothing about view 7 changed. Ruling 21b's law, demonstrated a third time inside the
session that quotes it: *a marginal is a property of an ordering, not of a camera.*

Artifacts: `stage1b_reach_n6.json`, `stage1b_reach_N6_ceiling.json`,
`stage1b_reach_n6.npy`, `stage1b_reach_per_view6.npy`.

---

## 2. The projection — invocation, and the check that six views did not move

Six twins, views pinned as an explicit per-invocation argument (`--view IDX=PATH` × 6); the
profile's `views` key is untouched. **View 2's twin and view 6's twin were inputs to
nothing.** Output is `stage1b_*` throughout — every seven-run artifact still carries its
original timestamp, verified after the run.

```
project_twins.py --profile profiles/prop.json --prep E14_prep
  --view 0=TWIN_swordclay_0.png --view 1=... --view 3=... --view 4=...
  --view 5=... --view 7=...          --out stage1/stage1b_atlas.png
[profile] prop (prop.json): 16 values applied to project_twins.py
[twins] frame: --fit-axis height margin 1.204 aspect 240,1024 -> h_ext 0.282186 v_ext 1.203993
[twins] N-VIEW mode: 6 cameras at y+000, y+045, y+135, y+180, y+225, y+315
```

### 2b. All six retained views reproduce BYTE-IDENTICALLY

The per-view stage depends on that view's twin and the profile, not on which other cameras
are present. Pre-registered as P3 and checked as text, line for line:

```
[logdiff] y+000.0  13 lines  IDENTICAL      [logdiff] y+180.0  13 lines  IDENTICAL
[logdiff] y+045.0  14 lines  IDENTICAL      [logdiff] y+225.0  13 lines  IDENTICAL
[logdiff] y+135.0  13 lines  IDENTICAL      [logdiff] y+315.0  13 lines  IDENTICAL
```

Registration, trust-mask counts, the edge-distance line, **every row of the A3
per-structure erosion table**, and the background probe's dE and percentages are unchanged
to the digit. Nothing moved that this session did not move, and the seven-run's §2 tables
carry over verbatim rather than being re-tabulated here.

## 3. Coverage against all three ceilings — and the number that fell

**Banked, not gated** (the E12 24e form; no pass condition exists):

| | texels | of valid | of the 6-cam ceiling | of the 8-cam comparable |
|---|---|---|---|---|
| valid | 3,661,903 | 100% | | |
| reach, 6 cameras | 1,867,754 | 51.01% | 100% | |
| **STYLED** | **1,656,847** | **45.25%** | **88.71%** | **88.14%** |
| — the seven-run | 1,729,017 | 47.22% | (92.09% of ITS ceiling) | 91.98% |
| — the beast at its stage 1 | 1,430,687 | 44.2% | | 87.5% of ITS ceiling |

**Styled fell by 72,170 texels and the ratio to its own ceiling fell 3.38 points.** That is
§4's subject and it is the session's finding.

**The on-surface family (Ruling 9):**

| family | denominator | styled share | seven-run |
|---|---|---|---|
| ALL VALID (the legacy family) | 3,661,903 | **45.25%** | 47.22% |
| ON-SURFACE (valid eroded 2 texels) | 1,143,291 (31.22%) | **47.61%** | 48.45% |
| the 2-texel MARGIN RING only | 2,518,612 (68.78%) | **44.17%** | 46.66% |

**The two families now differ by 3.44 points against the seven-run's 1.79** — the gap
nearly doubles. The seven-run's reading was that "a margin texel inherits its island's
geometry and passes or fails with it," so the restatement barely moved the number. Losing
the edge-on camera moves the ring 2.49 points and the interior 0.84, because what left was
disproportionately margin. The 1.79 was a property of a camera set, not of the subject.

## 4. ⚠ THE DIFF — where view 6's 145,185 committed texels went

### 4a. The two pre-registered checks

| check | prediction | measured |
|---|---|---|
| texels NOT owned by view 6 that changed owner | exactly 0 of 1,583,832 | **0 (0.000000%)** |
| texels styled in the six-run but not the seven | exactly 0 | **0** |

Ownership among the retained six is independent of view 6's presence, exactly. The
destinations below therefore partition view 6's committed set with nothing left over, and
the asserted identity *loss = styled delta* holds.

### 4b. The destinations

| destination | texels | share of view 6's 145,185 |
|---|---|---|
| re-owned by view 5 (yaw 225) | 36,481 | 25.13% |
| re-owned by view 7 (yaw 315) | 36,023 | 24.81% |
| re-owned by view 4 (yaw 180) | 397 | 0.27% |
| re-owned by view 0 (yaw 0) | 114 | 0.08% |
| re-owned by view 1 (yaw 45) | **0** | 0.00% |
| re-owned by view 3 (yaw 135) | **0** | 0.00% |
| **NEWLY UNSTYLED** | **72,170** | **49.71%** |

Per-view committed, the two runs side by side:

| view | yaw | seven-run | six-run | delta | |
|---|---|---|---|---|---|
| 0 | 0 | 278,678 | 278,792 | +114 | +0.0% |
| 1 | 45 | 263,591 | 263,591 | 0 | — |
| 3 | 135 | 264,331 | 264,331 | 0 | — |
| 4 | 180 | 251,327 | 251,724 | +397 | +0.2% |
| 5 | 225 | 243,005 | **279,486** | +36,481 | **+15.0%** |
| 6 | 270 | 145,185 | 0 | −145,185 | EXCLUDED |
| 7 | 315 | 282,900 | **318,923** | +36,023 | **+12.7%** |
| | | 1,729,017 | 1,656,847 | **−72,170** | |

**Half of the excluded artifact's territory was re-owned and half became holes**, and the
re-owning is almost entirely its two angular neighbours — the two views 45° away. Views 1
and 3, at 135°, took **not one texel**.

### 4c. ⚠ THE HEADLINE — the paint cost is 7.4× the reach cost

| why the 72,170 were lost | texels | share |
|---|---|---|
| no remaining camera can REACH it (the ceiling delta) | 4,136 | **5.73%** |
| reachable, but no remaining camera's PAINT is trusted there | **68,034** | **94.27%** |

| | texels | points of valid |
|---|---|---|
| the reach cost, N7 − N6 (§1b) | 9,733 | 0.2658 |
| **the paint cost, styled(7) − styled(6)** | **72,170** | **1.9708** |
| ratio | **7.4×** | |

**Ruling 21c's premise is falsified by its own instrument.** The ruling ordered the
six-camera ceiling because it "prices v6's exclusion exactly." It prices the *reach*
exclusion exactly — 9,733, three code paths agreeing. It understates the *paint* cost, which
is what an atlas is made of, by 7.4×. A camera contributes a texel only if it both reaches
it and is trusted there, and the trust term is 94% of this camera's contribution.

The reachable-but-untrusted population is not a set of marginal, barely-visible surfaces:

| of the 68,034, how many of the remaining six CAN see them | texels | share |
|---|---|---|
| 1 camera | 16,918 | 24.9% |
| 2 cameras | 51,116 | **75.1%** |

Three quarters are seen by **two** of the six and still go unpainted. Geometry was never the
binding constraint; the A3 edge erosion and the trust intersect are, and they bite where the
subject is thin — which is the whole surface view 6 was facing.

### 4d. The loss by structure — and it is NOT the crossing

| structure (z band) | valid | view 6 owned | LOST | lost / v6-owned | share of loss | concentration |
|---|---|---|---|---|---|---|
| L5 the stone | 177,314 | 15,526 | 1,953 | 12.6% | 2.71% | 0.56× |
| L3 pommel collar | 78,130 | 5,129 | 446 | 8.7% | 0.62% | 0.29× |
| L4 grip wrap + mid ring | 214,217 | 13,630 | 1,545 | 11.3% | 2.14% | 0.37× |
| **L2/L3 the CROSSING** | 452,460 | 10,350 | 4,432 | **42.8%** | **6.14%** | **0.50×** |
| **L1 the blade** | 2,739,782 | **100,550** | **63,794** | **63.4%** | **88.39%** | **1.18×** |

**88.4% of the loss is on the blade.** View 6 was not principally the guard's camera — 69.3%
of everything it owned was blade, and nearly two thirds of that is now hole. The crossing
takes 6.1% of the loss at a concentration of **0.50×, below its share of valid**, against a
pre-registered prediction of ≥30% at 3.6×.

Ruling 21c located view 6's face-dome paint at the guard and ordered the re-projection on
that basis. The paint was there — §5 walks it — but it is a small fraction of what the twin
was carrying. **The atlas consequence of excluding an edge-on camera lands on the edge-on
structure that is longest, not on the one the defect was noticed in.**

## 5. The sheet-walk — the crossing and the blade, before and after, in plain words

Walked at 8–9× on `_walk_yaw270_guard_9x.png` and `_walk_yaw270_guardlow_8x.png`, reference
beside asset, structure by structure, before any of §4's numbers were consulted.

**The excluded twin (view 6), top to bottom.** Wine-red braided grip wrap; a gold collar
ring carrying a band of raised studs; then a rounded grey-brown DOME with a stippled scaly
surface and a horizontal band of rivets around it; two symmetric curling loops hanging off
its left and right flanks like ear-guards; and below the dome a central column bearing two
rounded symmetric masses that read as cheeks or eyes. The clay at this camera has a plain
faceted guard block. This is Ruling 20a's face-helmet, and it is what the AFTER column does
not contain.

**The guard's yaw-270 face — BEFORE (seven twins).** Gold wraps the left and right
shoulders of an octagonal block. The centre is a grey column carrying a soft brown-tan smear
running down its middle and a pale rounded pad near the top-centre; the shading is smooth and
rounded rather than facet-flat.

**The guard's yaw-270 face — AFTER (six twins).** The same octagonal silhouette and the same
gold shoulders. The centre is now hard-divided: light grey on the left, dark charcoal on the
right, meeting at a vertical line, with a thin broken white stripe on the line itself. The
brown-tan smear is gone and the rounded pale pad is gone. It reads flatter and more angular.

**Below the guard, the blade's edge-on centreline — and this is the change nobody predicted.**
In the BEFORE provenance panel a solid **yellow** column (view 6) runs from the guard down the
*entire length* of the blade, flanked by view 5's pink on the left and view 7's blue on the
right. In the AFTER panel the yellow is replaced by a **ragged black column running the blade's
full length** — the two neighbours expanded inward and did not meet. On the asset, the BEFORE
blade carries a soft brown-tan smear at the guard-blade junction and a continuous silvery
left / charcoal right split; the AFTER blade keeps the split and adds a hairline of void down
the centre.

**In one sentence, and it is a description rather than a verdict:** view 6 was the only
camera facing the blade's edge, it owned a continuous ribbon down that edge for the blade's
whole length, and with it excluded that ribbon is a hole for its whole length — while at the
guard, the material with no counterpart in the clay is gone and what replaces it is two
neighbours meeting at a seam.

### 5b. How much each camera's picture actually changed

Pixels inside the figure, not file bytes (CLAUDE.md: a PNG hash mismatch is not evidence a
render changed).

| view | yaw | figure px | changed > ΔE 2 | share | p99 ΔE |
|---|---|---|---|---|---|
| 0 | 0 | 242,266 | 1,473 | 0.61% | 1.15 |
| 1 | 45 | 243,652 | 133 | **0.05%** | 0.75 |
| 3 | 135 | 243,071 | 86 | **0.04%** | 0.74 |
| 4 | 180 | 242,967 | 1,500 | 0.62% | 1.22 |
| 5 | 225 | 244,618 | 6,856 | 2.80% | 16.72 |
| 6 | 270 | 244,960 | **9,499** | **3.88%** | **23.31** |
| 7 | 315 | 243,083 | 6,733 | 2.77% | 17.80 |

Median ΔE is 0.00 at every camera: the change is a small, high-amplitude region, not a
global shift. The two 135°-away views are unchanged to three decimal places, which is the
same fact as their zero re-ownership in §4b, arrived at from the render side.

## 6. The crossing census, and the brush's territory

| | texels | of valid | seven-run |
|---|---|---|---|
| valid but unstyled | 2,005,056 | 54.75% | 1,932,886 / 52.78% |
| — **reachable: the brush's territory** | **210,907** | **5.76 points** | 148,470 / 4.05 points |
| — unreachable: dilation's, at finalize | 1,794,149 | 48.99% | 1,784,416 |

**The brush's territory grows 42%, from 4.05 to 5.76 points of valid.** The reach ceiling
fell by 9,733 while the paint fell by 72,170, so the gap between them — which is exactly the
brush's job — widens by 62,437.

| structure (z band) | valid | styled | styled % | 7-run % | reach hole | 7-run hole |
|---|---|---|---|---|---|---|
| L5 the stone | 177,314 | 86,949 | 49.0% | 50.1% | 5,581 | 3,840 |
| L3 pommel collar | 78,130 | 36,481 | 46.7% | 47.3% | 315 | 105 |
| L4 grip wrap + mid ring | 214,217 | 102,429 | 47.8% | 48.5% | 4,219 | 2,960 |
| **L2/L3 the CROSSING** | 452,460 | 168,103 | **37.2%** | 38.1% | **14,420** | 10,095 |
| L1 the blade | 2,739,782 | 1,262,885 | **46.1%** | 48.4% | **186,372** | 131,470 |

The crossing remains the worst-covered structure and falls 0.9 points; **the blade falls 2.3
points**, the largest structural move in the table, and its reachable hole grows by 54,902.

## 7. ⚠ THE GEM READOUT (Ruling 19b, re-run verbatim)

Same landmark, asserted unchanged (`peak x-extent 0.05878 at z 0.4620; first local minimum
0.03548 at z 0.4340`), same C\* 12 floor, same bands.

| | six-run | seven-run |
|---|---|---|
| stone valid | 177,314 | 177,314 |
| stone styled | 86,949 (49.0%) | 88,902 (50.1%) |
| above C\* 12 | **20,761 (23.9%)** | 19,227 (21.6%) |
| median hue | 308.6 | 308.9 |
| C\* median | 21.2 | 20.4 |

| band | six-run | seven-run |
|---|---|---|
| **wine 0–25 — L5's declared band, garnet** | **15.04%** | 16.23% |
| orange 25–42 | 0.26% | — |
| gold 42–104 | 12.78% | 14.37% |
| forbidden 104–290 | 1.41% | 1.50% |
| lavender 290–310 | 21.71% | 18.50% |
| magenta 310–360 | 48.80% | 49.26% |
| **lavender + magenta** | **70.51%** | 67.76% |

**The stone lost 1,953 styled texels and its above-floor population GREW by 1,534**, because
views 5 and 7 paint the stone at higher chroma than view 6 did (C\* median 20.4 → 21.2).

| the stone's above-floor texels, owned by | texels | median hue | wine | lav + mag | C\* median |
|---|---|---|---|---|---|
| **the GARNET views (0, 4)** | 4,702 | **17.6** | **65.40%** | 7.49% | 20.9 |
| **the DRIFTED views (1, 3, 5, 7)** | 16,059 | **322.6** | 0.29% | **88.97%** | 21.3 |
| — seven-run, garnet | 4,700 | 17.6 | 65.36% | 7.70% | 20.9 |
| — seven-run, drifted | 14,527 | 322.2 | 0.34% | 87.19% | 20.1 |

**The garnet partition is untouched to four texels; the whole change is inside the drifted
one.** Source split 21.90% garnet / 78.10% drifted, against 21.42% / 78.58%.

**And the direction is the one that matters for Ruling 21d: removing view 6 moved the stone
further from garnet, not closer.** Lavender+magenta rises 2.75 points, wine falls 1.19. At 6×
on `STAGE1B_GEM_6x.png` the reading is unchanged from the seven-run's — one coherent violet
stone with a redder core, not a patchwork — beside two references (views 0 and 4) whose own
twins carry a near-black garnet with a red core and a white highlight. **The numbers and the
impression agree about the stone's colour and disagree about its patchiness, exactly as
before.** Nothing is decided here; 21d's three options are unchanged in kind and one of them
now has 2.75 points less room.

## 8. The background probe, on the finished six-run atlas

Ruling 21e's honest asset-level number, re-run because ownership moved:

| view | committed | within ΔE 10 of background | share | seven-run share |
|---|---|---|---|---|
| 0 | 278,792 | 327 | 0.12% | 0.09% |
| 1 | 263,591 | 994 | 0.38% | 0.39% |
| 3 | 264,331 | 1,096 | 0.41% | 0.42% |
| 4 | 251,724 | 145 | 0.06% | 0.06% |
| **5** | 279,486 | 1,105 | **0.40%** | 0.12% |
| **7** | 318,923 | 4,757 | **1.49%** | 0.83% |
| **ALL** | 1,656,847 | **8,424** | **0.51%** | 0.31% |

**The two views that absorbed view 6's territory are the only two whose share moved** — view
5 by 3.3× and view 7 by 1.8×, while the four untouched views move by ≤ 0.03 points. What they
absorbed is more rim-mixed than what they already held, which is what taking over an edge-on
neighbour's surface should look like. The probe's reference is still the retired corner
median (Ruling 21e); this is the asset-side statement, and 0.51% is not a gate.

The lavender-rim band's atlas-side analogue, same scope limit as before (it answers *is the
band on island margin*, not *is it deep inside the figure*): **24,513 = 1.479% of styled**
against the seven-run's 19,523 = 1.129%; interior share 28.96% against 23.98%, with 32.86%
of all styled texels interior by the same test.

## 9. Predictions scored

| # | prediction | outcome |
|---|---|---|
| **P1** | anchors N8 1,879,807 and N7 1,877,487 reproduce; all seven per-view reach masks texel-identical; N6 < N7 < N8 | **HELD**, every one, to the digit |
| **P1** | N7 − N6 in 1,000–15,000 texels | **HELD** — 9,733 |
| P1 | point estimate 3,500 | **missed by 2.8×**, as I said on the page I expected to |
| P1 | N6 in 1,862,000–1,876,500 (50.85–51.24%) | **HELD** — 1,867,754 / 51.0050% |
| P1 | Ruling 20c's ~4.4 points falsified by ~46× | **direction HELD, magnitude wrong** — 16.6×, not 46× |
| **P1** | the mechanism is angular, as it was for yaw 90 | **FALSIFIED, and it is a finding** — 81.3% of the exclusive set is OCCLUSION at a median best facing of 0.919 |
| **P2** | styled 1,720,000–1,728,000; loss 1,000–9,000 | **FALSIFIED by 8×** — 1,656,847, loss 72,170 |
| **P2** | styled/valid 46.97–47.19%; styled/N6 91.7–92.2% | **FALSIFIED** — 45.25% and 88.71% |
| **P2** | *"if styled/N6 moves more than 0.5 points, population (b) is larger than I think and that is the finding"* | **the escape clause FIRED** — it moved 3.38 points and (b) is 94.27% of the loss |
| **P3** | all six retained views byte-identical | **HELD EXACTLY** — every line of every block |
| **P4** | 100.00% of non-v6 texels keep their owner | **HELD EXACTLY** — 0 of 1,583,832 |
| P4 | nothing newly styled | **HELD** — 0 |
| P4 | view 7 30–50%, view 5 25–45% | **7 MISSED (24.81%), 5 held at the edge (25.13%)**; I also predicted 7 > 5 and it is 5 > 7, though by 1.3% |
| **P4** | views 1+3 take 5–20%; views 0+4 take 3–15% | **FALSIFIED** — 0.00% and 0.35% |
| **P4** | newly unstyled 0.7–6% | **FALSIFIED by 8×** — 49.71% |
| **P5** | crossing styled % 36.5–38.0, point 37.3 | **HELD, and the point estimate lands within 0.1** — 37.2% |
| P5 | crossing reachable hole 10,300–16,000 | **HELD** — 14,420 |
| **P5** | ≥30% of the newly-unstyled land in the crossing, at 3.6× concentration | **FALSIFIED** — 6.14% at **0.50×**; 88.4% is on the blade |
| P5 | the guard's face loses the invented motif and reads flatter and less detailed | **held as far as it goes** — but I did not predict a hole would open at the guard's centre, and I did not predict the blade seam at all |
| **P6** | the gem finding is robust; lav+mag moves < 2 points | **FALSIFIED** — 2.75 points, and it moved AWAY from garnet |
| P6 | lav+mag 64–70%; wine 15–19%; median hue 305–312; drifted share 75–80% | 70.51% **missed by 0.51 at the top edge**; 15.04%, 308.6, 78.10% all **held** |
| P6 | stone styled 88,000–88,900; above C\* 12 in 18,900–19,300 | **86,949 missed low; 20,761 FALSIFIED — it went UP** |
| **P7** | brush territory 148,000–156,000 | **FALSIFIED by 35%** — 210,907 |
| P8 | no generation, no re-roll, no overwrite, no gate armed, no fixture edit, no memory write, exclusions labelled in-image | **held** |

### Where I was most wrong, and it is one substitution

**P2, P4's destinations, P5's concentration and P7 are all the same error.** I priced a
camera's contribution in **reach** when the question was **paint**. My prediction page named
the gap explicitly — *"(b) texels reachable by a neighbour whose paint there is untrusted …
is the part I cannot compute from the seven-run"* — and then set every band as though (b)
were a few thousand texels. It is 68,034. **I named the unknown and priced it at zero.**

That is CLAUDE.md's *test the property, not a geometric proxy for it* arriving in a new
place: reach is a proxy for contribution, it fails precisely where the subject is thin, and
the whole surface an edge-on camera faces is thin. It is also the same family as handoff 5's
scored lesson — identify the right correction, then under-apply it to your own numbers — and
it is now two sessions running.

**The one thing the shape of the answer got right** is P3 and P4's exactness: predicting
*exactly 0* twice, and getting exactly 0 twice, is what makes §4b's partition readable at
all. A band would have hidden the fact that views 1 and 3 take nothing.

## 10. What has NOT been done

- **No pass condition invented, and nothing gated.** All three ceilings are comparables; the
  eye is the gate.
- **Nothing armed, nothing bound.** `reg-iou-min` stays 0.0, `bbox-tol` 9.99, `bg-max-pct`
  100.0, the palette report-only.
- **View 2's and view 6's twins were inputs to nothing.** The yaw-270 *camera* is rendered as
  a viewing camera and is labelled in-image as carrying no twin in this run.
- **No seven-run artifact was overwritten** — all 24 retain their original timestamps,
  checked after the run. The six-run writes `stage1b_*` and `render1b/`.
- **No strokes, no finalize, no `thin_extent` decision.** No fixture, profile or palette edit.
  No generation, no credits, no memory-store write.
- **Ruling 21c's premise is reported, not amended.** §4c measures that the ceiling prices the
  reach exclusion and not the paint exclusion; the correction is the advisor's to make.

## 11. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The ceiling pre-registered and committed in its own commit before `project_twins` ran; predictions committed before the ceiling; the six-view list an explicit per-invocation argument, never a profile edit; every readout re-run from handoff 5's own scripts with the three changed lines named in each file's docstring so "verbatim" is checkable rather than asserted |
| ANDON_AUTHORITY | **3** | Three anchors asserted before a six-camera number existed, including a texel-for-texel comparison of all seven saved reach masks that a totals check would have passed; the diff asserts its own partition and that loss equals the styled delta; the gem landmark asserted unchanged between sessions; the render pipeline throws on any non-zero exit rather than continuing |
| NAMED_COMPENSATORS | **3** | No spend, no generation, no irreversible step. New files only (`stage1b_*`, `render1b/`); the seven-run's 24 artifacts verified untouched by timestamp after the run; the whole session is repeatable from committed inputs by the recorded invocation |
| DECOMPOSE_BY_SECRETS | **3** | The denominator is derived for THIS camera set; the loss is decomposed into geometry vs trust (§4c) where the aggregate would have read as a ceiling effect; the loss is decomposed by structure (§4d) where the aggregate would have confirmed the crossing hypothesis instead of overturning it; ownership is separated from marginal reach and both are quoted (21a's law) |
| UNCERTAINTY_GATED_HUMANS | **3** | No pass condition invented. The sheet-walk is stated in plain words before any number (§5) and is labelled as description; the gem's numbers and its 6× impression are reported as agreeing on colour and disagreeing on patchiness rather than resolved here; §4c reports that the ordered instrument answers a different question and leaves the ruling to the advisor |
| EXTERNAL_VERIFIER | **2** | Two independent code paths agree on N6; three anchors tie this session to the seven-run's numbers; the render-side change (§5b) confirms the ownership-side result (§4b) from a different direction — views 1 and 3 are zero in both. `skip:` on a second model family, per this repo's precedent: the arithmetic is deterministic and the disagreement it could surface is already covered by path agreement |

---

## HALT — stage 1b staged

`E:\AI\training\facet_next\E14_prep\stage1\`:

```
stage1b_atlas.png              the six-twin atlas (4096, holes at hole-grey)
stage1b_atlas_holes.png        the hole map — stage 2's input
stage1b_atlas_styled_mask.npy · stage1b_atlas_owner.npy · stage1b_atlas_blend.png
stage1b_sword.glb              the atlas packed onto prep_uv.glb
stage1b_provenance_atlas.png · stage1b_prov.glb
stage1b_lost_atlas.png         GREEN = view 6's texel re-owned, RED = newly unstyled
render1b/stage1bflat_{0,1,3,4,5,6,7}.png   FLAT light
render1b/stage1bprov_{0,1,3,4,5,6,7}.png   the provenance renders
STAGE1B_SHEET_{0,1,3,4,5,7}.png   reference | asset | provenance, full size
STAGE1B_flat_strip.png            all seven cameras, asset over provenance
STAGE1B_CROSSING_4x.png           ⚠ the crossing BEFORE/AFTER, twin panel stamped EXCLUDED
STAGE1B_GEM_6x.png                Ruling 19b's crop for the eye
STAGE1B_OWNERSHIP_DIFF.png        where view 6's territory went, four cameras
_walk_yaw270_guard_9x.png · _walk_yaw270_guardlow_8x.png   the sheet-walk's own crops
stage1b_reach_n6.json · stage1b_reach_N6_ceiling.json · stage1b_reach_n6.npy
stage1b_reach_per_view6.npy · stage1b_lost_mask.npy
stage1b_readout.json · stage1b_gem_stone_readout.json · stage1b_diff.json
stage1b_holes_by_structure.json · stage1b_render_diff.json · stage1b_followups.json
stage1b_projection.log · stage1b_renders.log
```

**Four things want the advisor's eye, and none is mine:**

1. **⚠ The paint cost against the reach cost (§4c).** Excluding view 6 costs the reach
   ceiling 9,733 texels and the atlas **72,170** — 7.4× — because 94.27% of what was lost is
   reachable by a remaining camera whose paint is not trusted there, three quarters of it
   reachable by *two*. Ruling 21c ordered the six-camera ceiling on the premise that it
   prices the exclusion exactly; it prices the reach exclusion exactly. Whether the price law
   (21b) now needs a second clause — *a reach price is not a paint price* — is a ruling.

2. **⚠ The loss is on the blade, not the crossing (§4d).** 88.4% of the 72,170 is the blade's
   edge-on centreline, a continuous ribbon down its whole length that is now a hole for its
   whole length (§5). The crossing takes 6.1% at 0.50× concentration. The defect was noticed
   at the guard; the atlas cost is on the blade, and the brush's territory grows 42% to 5.76
   points of valid because of it.

3. **The gem (§7), for Ruling 21d's still-open decision.** Removing view 6 moved the stone
   **away** from garnet: lav+mag 67.76% → 70.51%, wine 16.23% → 15.04%, with the garnet
   partition untouched to four texels and the whole change inside the drifted one. At 6× it
   still reads as one violet stone with a redder core beside two near-black garnet
   references. 21d's three options stand; the middle one has less room than it did.

4. **The asset itself**, at the Director's zoom under FLAT light beside its reference —
   **45.25% of valid, 88.71% of this run's ceiling** against the beast's 87.5% at the same
   stage, and against the seven-run's 92.09% of a ceiling that included an excluded twin's
   paint. No pass condition exists and none was invented.

Stage 2's lane derives from `stage1b_atlas_holes.png` when its ruling opens it.
