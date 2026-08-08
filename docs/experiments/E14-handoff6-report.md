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
