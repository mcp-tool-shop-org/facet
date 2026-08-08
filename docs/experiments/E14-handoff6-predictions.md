# E14 handoff 6 — blind predictions, committed BEFORE the six-camera ceiling runs

**Executor session, 2026-08-08.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 21c.
Committed before `e14_atlas_anatomy` is invoked for N6, before `project_twins` runs, and
before any readout script is executed or read.

**What I have read at the time of writing**: `CLAUDE.md`; the handoff-6 dispatch; Rulings
20 and 21; the whole of [E14-handoff5-report.md](E14-handoff5-report.md) (the seven-run,
which is the *comparison* this session diffs against and is required reading); the
seven-run's `projection.log`. **What I have NOT looked at**: any six-camera number, any
six-run artifact, and the contents of the handoff-5 readout scripts. **These predictions
are blind in that sense and not in any stronger one** — the seven-run's numbers are the
base I am extrapolating from, and every prediction below is stated as a delta against them.

**Handoff 5's own scored lesson is the one I am most at risk of repeating.** That executor
wrote *"the ladder's position-3 marginal overstates the set-level cost"*, was right, and
then predicted a delta 3× larger than the truth because it anchored on the number it had
just argued was wrong. Ruling 20c's carried price for view 6 is **~4.4 points ≈ 161,000
texels**. I am stating below that the true figure is two orders of magnitude smaller, and I
am putting the point estimate where the mechanism says it goes rather than splitting the
difference with the inherited number. If I am wrong it should be recorded as *wrong in the
direction the mechanism predicts*, not as a hedge that survived.

---

## P1 — the SIX-camera ceiling, and v6's exact exclusive price

Cameras 0/45/135/180/225/315 (views 0/1/3/4/5/7). Dropping yaw 270 from the seven-set.

**Mechanism.** A surface whose normal points at yaw 270 clears the 0.45 facing floor from
both yaw 225 and yaw 315 (cos 45° = 0.707 > 0.45). This is the *identical* argument that
made yaw 90's exclusive contribution 2,320 texels in the eight-set, and the structure is
exactly parallel: yaw 270's two diagonal neighbours are both present in N6, and yaw 90's
absence is irrelevant to yaw 270's exclusivity because the two cameras face opposite ways
(cos 180° = −1). What remains exclusive to yaw 270 is therefore **occlusion-limited only** —
surfaces facing near-270 that the 225 and 315 rays cannot reach. On a sword that is the
guard-end undercuts and deep facets, not a large set.

| quantity | band | point estimate |
|---|---|---|
| **N7 − N6** (v6's exclusive price, texels) | 1,000 – 15,000 | **3,500** |
| **N7 − N6** in points of valid | 0.03 – 0.41 | **0.096** |
| **N6** (reachable, texels) | 1,862,000 – 1,876,500 | **1,874,000** |
| **N6** as % of valid | 50.85 – 51.24% | **51.18%** |

**The asymmetry I am pricing in**: view 6's own reach is 473,595 against view 2's 349,108
(1.36×), so I put the point estimate at ~1.5× yaw 90's 2,320 rather than at parity. Ruling
20c's carried ~4.4 points is predicted **FALSIFIED by a factor of ~46**.

**Pre-registered ordering constraint**: N6 < N7 < N8 strictly, and N7 − N6 ≥ 0. If either
fails, the instrument is wrong, not the sword.

**Anchor**: N7 must reproduce at exactly **1,877,487** and N8 at exactly **1,879,807**
before any new number is computed. Predicted to hold to the digit.

## P2 — the six-run's styled count and coverage

View 6 committed 145,185 texels in the seven-run. Removing it, those texels are contested
by the remaining six. Ownership transfer is free — a re-owned texel is still styled. Only
two populations are actually lost: (a) texels geometrically exclusive to view 6 (P1's
~3,500), and (b) texels reachable by a neighbour whose *paint* there is untrusted (eroded,
outside the trust mask). (b) is the part I cannot compute from the seven-run and it is why
this band is wider than P1's.

| quantity | band | point estimate |
|---|---|---|
| **styled** (texels) | 1,720,000 – 1,728,000 | **1,724,500** |
| styled loss vs the seven-run | 1,000 – 9,000 | **4,500** |
| styled / valid | 46.97 – 47.19% | **47.09%** |
| styled / N6 | 91.7 – 92.2% | **92.03%** |
| styled / N8 (the route-comparable) | 91.5 – 91.9% | **91.74%** |

**The ratio barely moves and that is a prediction, not a hedge**: numerator and denominator
lose nearly the same texels, because a texel exclusive to view 6 was almost certainly styled
by view 6. If styled/N6 moves more than 0.5 points in either direction, population (b) is
larger than I think and that is the finding.

## P3 — per-view diagnostics reproduce EXACTLY on the six retained views

The per-view stage of `project_twins` — registration, trust mask, edge distance, the A3
erosion table, the background probe, the per-view styled count — depends on that view's twin
and the profile, **not on which other views are in the set**. So:

- All six retained views' `projection.log` blocks are predicted **byte-identical** to the
  seven-run's, line for line, including the erosion percentages and the probe's dE figures.
- The only lines that may differ are the composite ones: styled total, holes, atlas variance.

**This is the check I most want to fire if it is going to.** A difference in any retained
view's per-view block means a parameter moved that I did not move, and it halts the session.

## P4 — ownership: only view 6's texels move

Ownership among the other six is a per-texel argmax over facing weight and is unaffected by
view 6's presence. The σ = 16 levelling is a colour operation and cannot change an owner.

- **100.00% of non-v6-owned texels keep the same owner.** Predicted exactly, not
  approximately. Any non-zero count here is a finding about order-dependence in the
  projector and is reported as such.
- The 145,185 v6-owned texels redistribute:

| destination | band | point estimate |
|---|---|---|
| re-owned by view 7 (yaw 315) | 30 – 50% | **40%** |
| re-owned by view 5 (yaw 225) | 25 – 45% | **35%** |
| re-owned by views 1 + 3 (yaw 45/135) | 5 – 20% | **12%** |
| re-owned by views 0 + 4 (yaw 0/180) | 3 – 15% | **8%** |
| **newly UNSTYLED** | 0.7 – 6% | **3%** (≈ 4,500 texels) |

View 7 over view 5 because view 7's own reach is larger (671,237 against 592,390).

## P5 — the crossing (L2/L3, guard + boss)

Seven-run: 452,460 valid, 172,535 styled = **38.1%**, 10,095 reachable holes — already the
worst-covered structure by ten points. It is also where Ruling 21c located view 6's
face-dome paint, so it is where v6's exclusion should bite hardest.

| quantity | seven-run | band | point estimate |
|---|---|---|---|
| crossing styled % | 38.1% | 36.5 – 38.0% | **37.3%** |
| crossing reachable hole | 10,095 | 10,300 – 16,000 | **12,500** |
| share of newly-unstyled texels landing in the crossing | — | ≥ 30% | **45%** |

The crossing is 12.4% of valid. Predicting 45% of the newly-unstyled land there is
predicting a **3.6× concentration**, on the mechanism that the guard's yaw-270 end face is
the one surface whose best camera just left.

**Named appearance prediction, for the 4× crossing sheet**: the face-dome's curling hooks
and gold-heavy mass disappear from the guard's yaw-270 face and are replaced by the
diagonals' paint at glancing incidence — predicted to read *flatter and less detailed, but
without the invented figurative motif*. I predict it will look **worse as an image and
right as an object**, and that this tension is what goes to the Director.

## P6 — the gem readout (19b re-run verbatim)

View 6 is a *drifted* (770701) view, and its two angular neighbours 5 and 7 are also
drifted. So v6's stone texels should transfer mostly within the drifted partition and the
composition should barely move.

| quantity | seven-run | band | point estimate |
|---|---|---|---|
| stone valid | 177,314 | unchanged (geometry) | **177,314** |
| stone styled | 88,902 | 88,000 – 88,900 | **88,600** |
| above C\* 12 | 19,227 | 18,900 – 19,300 | **19,150** |
| wine 0–25 share | 16.23% | 15 – 19% | **16.6%** |
| lavender + magenta | 67.76% | 64 – 70% | **67.3%** |
| median hue | 308.9 | 305 – 312 | **308.5** |
| drifted-view source share | 78.58% | 75 – 80% | **78.0%** |

**The prediction that matters: the gem finding is ROBUST to v6's removal** — lav+mag moves
by less than 2 points. If it moves more, view 6 was carrying the stone's colour story and
the Director's pending decision changes shape.

## P7 — the brush's territory

hole = N6 − styled. N6 falls by ~3,500 and styled by ~4,500, so the hole *grows* slightly.

| quantity | seven-run | band | point estimate |
|---|---|---|---|
| reachable-but-unstyled | 148,470 (4.05 pts) | 148,000 – 156,000 | **149,500 (4.08 pts)** |

## P8 — what will not happen

No generation, no credits, no re-roll. View 2's twin and view 6's twin are inputs to
nothing. No seven-run artifact is overwritten — the six-run writes `stage1b_*`. No gate is
armed, no pass condition is invented, no stroke runs, no fixture/profile/palette edit, no
memory-store write. Excluded artifacts are labelled AS EXCLUDED in every sheet (Ruling 20d).

---

## The one number I would bet against myself on

**P1's point estimate.** The mechanism is clean and the parallel to yaw 90 is exact, so the
*shape* of the answer is not in doubt. But 3,500 comes from scaling 2,320 by an own-reach
ratio, and own-reach is not exclusivity — the two are related by occlusion, which I have not
measured. A result anywhere in 1,000–15,000 confirms the mechanism; the point estimate is
the weakest thing on this page and I expect to score it as missed.
