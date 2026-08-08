# E14 handoff 9 — predictions, committed before finalize runs

**Executor session, 2026-08-08.** Written after reading the dispatch, the rulings, the
handoff-8 report, the profile and `texpass_finalize.py`'s source — and **before any
finalize, pack or render leg has run.** Nothing in `run/final/` exists yet; `run/s8/`
has been read (SHA verified `34dafd4b57aa5b04df935cfb…`) and not opened for writing.

**Blind status is disclosed per prediction.** Two of the eight are not blind and say so:
one is arithmetic on recorded state, one is a code read. Calling those "predictions"
would be the thing this repo exists to stop.

---

## P0 — the inherited claim the dispatch told me to check, checked first

The dispatch carries: *"Verify the source-distance unit before quoting it — E07 found
`texpass_finalize.py`'s triangle-edge length HARDCODED from one mesh."*

**That claim is STALE, and the repair already landed.**
[`texpass_finalize.py:98-106`](../../tools/texpass_finalize.py) loads `prep_uv.glb` from
`--prep` at run time and takes the median over all three edges of every face, in the same
normalisation every consumer uses (`v = [x, -z, y] / max|v| * 0.5`). There is no constant.
The record already says so — [E04-profile-extraction.md](E04-profile-extraction.md) lines
176–178 flagged the seed list as stale on exactly this item — and the source agrees with
the record.

**I will still measure this mesh's median edge independently** (my own walk over
`prep_uv.glb`, not the tool's print) and report both numbers. Two independent numbers
agreeing is the check; the tool printing a number is not.

## P1 — the closed-texel count · **NOT BLIND (arithmetic on recorded state)**

`need = valid & holes`. From `run/s8/commit.log` (holes 1,929,166 after stroke 8) and the
ceiling record (valid 3,661,903): **1,929,166**, and 3,661,903 − 1,732,737 = 1,929,166
closes exactly.

What is genuinely open, and what I am actually predicting: **that `holes.png` and
`styled_mask.npy` agree about the same texel set on the valid mask.** They are separate
files written by separate code paths. If `(valid & holes).sum()` returns anything other
than 1,929,166, the two state files disagree and that is a finding, not a rounding.

## P2 — this mesh's median triangle edge · **BLIND**

**0.0008 – 0.0013, centre 0.0011.** Two independent routes to it:

- **Area / face count.** 999,474 faces (`reach_N8_replication.json`). The normalised sword
  is about 1.0 x 0.23 x 0.06; as a double-walled shell its two walls give a surface area I
  estimate at 0.4–0.5. Equilateral-equivalent edge = sqrt(A/F / 0.433) ~ 0.0010.
- **Voxel scale.** TRELLIS `1024_cascade` over a bbox whose longest axis normalises to 1.0
  gives one voxel ~ 0.00098, and marching-cubes triangles run ~0.5–1.0 voxel.

The dragon's was **0.00231** — I predict this mesh comes back roughly **half** that,
because the two meshes carry a similar face budget over very different surface areas.

## P3 — source-distance median, in triangle edges · **BLIND**

**Absolute: 0.0015 – 0.0030. In edges: 1.2 – 2.6, centre ~1.8 — ABOVE the dragon's
0.92**, and this is a mechanism prediction rather than a hedge:

The hole population is dominated by the **inner wall** of the hollow shell (1,794,149 of
2,005,056 stage-1b holes unreachable; 92.8% of unreachable texels are inner wall, per
`stage1b_reach_N6_ceiling.json`'s cross-tab). An inner-wall texel's nearest painted texel
in 3D is the outer wall directly across the cavity — **about 2 voxels, about 0.002 in
absolute terms, the same absolute separation as the dragon's**, because both meshes
normalise to a 1.0 longest span and both were reconstructed on the same 1024 grid. So the
absolute distance should sit close to the dragon's 0.00212 while the *ratio* rises,
because this mesh's edge is smaller.

**The ANDON sits at 3.0 edges.** If the median lands above it the tool halts, and that is
a report with its evidence — not a flag change, not a re-run at a looser bound.

Also pre-stated: **beyond 5 edges 2–8%** (dragon 2.50%); **beyond 20 edges below 0.5%**
(dragon 0.021%; ANDON at 5%); **normal disagrees >60 deg 70–90%** and **back-facing
65–88%** (dragon 82.25 / 78.91) — the last two are E07 Gate 0.5's reported diagnostics,
never gates, and on a double-walled shell they are *expected* high, because the nearest
surface to an inner-wall texel is the opposing wall.

## P4 — the mean-fallback count · **NOT BLIND, and the ANDON on it cannot fire**

The dispatch says *"the mean-fallback count (the dragon's was ZERO — predict against it)"*
and *"a nonzero is a FINDING, located per structure."*

**In `--surface-aware` mode the count is 0 by construction and cannot be anything else.**
`texpass_finalize.py` line 135 sets `grown = valid.copy()` before the dilation loop, and
`left` at line 154 is `(valid & ~grown).sum()` where `grown` only ever grows. So
`left == 0` on every surface-aware run, regardless of the atlas, the mesh, or how badly
the lookup went. The galleon's 112 came from the **atlas-flood** path, where
`grown = have.copy()` and the count means something.

**Prediction: 0 — and it carries no information.** *A check that cannot fail is not a
check* (CLAUDE.md). The dragon's zero was structural, not earned. The quantity that
actually carries this operation's failure mode in this mode is the source-distance
distribution (P3), which is where I will look.

## P5 — the final mix · **the valid-denominator row is arithmetic; the reachable row is BLIND**

**Of ALL valid (3,661,903) — NOT BLIND, this is addition:**

| | texels | % of valid |
|---|---|---|
| REFERENCE (stage-1b projection) | 1,656,847 | **45.245** |
| BRUSH (8 strokes) | 75,890 | **2.073** |
| DILATION (finalize) | 1,929,166 | **52.682** |

Comparables, stated so nothing is read against the wrong asset: W3 68.8 / 4.2 / 27.0 ·
galleon 36.89 / 6.87 / 56.24 · dragon 44.15 / 3.07 / 52.78. **This subject should land
almost on top of the dragon** — both are hollow double-walled shells with about 51% of the
atlas reachable, and reachability is what sets the dilation share.

**Of the REACHABLE set — BLIND**, because the class counts are *not* subsets of it: the
brush commits at `facing-min 0.25` while the ceiling floors at 0.45, so the partition is
three-way (the profile's own funnel note). Predicted against N6 = 1,867,754:

- reference within N6: **1,600,000 – 1,660,000 → 86 – 89%**
- brush within N6: **45,000 – 70,000 → 2.4 – 3.7%**
- dilation within N6: the remainder, **8 – 11%**

I will report intersected counts and bare ratios separately where they differ, and say
which is which. The dragon's report quoted reference as a bare ratio and brush as an
intersection; I am not repeating that silently.

## P6 — the per-structure table, the blade especially · **BLIND**

Structures per [E14-longsword-structures.json](E14-longsword-structures.json) —
geometry-derived z bands, not row bands.

| structure | valid | predicted dilation share |
|---|---|---|
| **L1 blade** | 2,739,782 | **51 – 56%** — inside W3's blade band of 47–61%, the named comparable |
| L2 crossing | 452,460 | 57 – 64% (styled only 37.2% at A0, the lowest band) |
| L5 stone | 177,314 | 46 – 53% |
| L4 grip | 214,217 | 48 – 55% |
| L3 collar | 78,130 | 48 – 56% |

The blade is the one that matters: it is the subject, and its dilation share is where the
E08 blade-band history says to look.

## P7 — the off-surface family, Ruling 9's form · **NOT BLIND (quoting the record, then re-measuring)**

Ruling 9a: a bake-side off-surface rate is quoted **with its island count and its erode-2
residue** or it is void. This subject's recorded numbers (Ruling 9c, `offsurface.json`):
**11.0875% >1 px · 46,496 islands · erode-2 residue 0.0085%**. The rate is a property of
the *bake*, which finalize does not touch, so it should re-measure identically.

Separately, the **painted** off-surface count at HALT 2 was **0 texels / 0.0000%**.
Prediction: **still 0 after finalize** — but this is a different quantity from the bake
rate and the two will not sit in one column.

## P8 — pack · **BLIND**

`longsword_hero.glb` at **40 – 46 MB** (dragon 43.9 MB; this subject's stroke GLB is
41.8 MB and the atlas grows no pixels at finalize, only colour). Atlas variance well over
the 0.001 ANDON — **0.02 – 0.06**.

---

## What would make me wrong in a way worth knowing

The prediction I most expect to break is **P3's ratio**, and the two ways it breaks say
different things. If the median lands *below* 0.92 edges, my edge estimate is too small
and P2 is wrong with it. If it lands *far above* 2.6 — or trips the 3.0 ANDON — then the
holes are not dominated by across-the-cavity lookups, colour is coming from somewhere else
on the figure, and that is the defect class this gate exists for: a halt, not a number to
explain away.

**Second: P6's blade share.** The lane's design (Ruling 24c) declined a wider commit mask
on the grounds that *"the withheld rim closes by finalize dilation from the strokes' own
paint at sub-triangle-edge distance."* If the blade's dilation sources turn out to travel
far, that argument is retrospectively weaker — a finding for the ruling, not something to
smooth over in a sheet.
