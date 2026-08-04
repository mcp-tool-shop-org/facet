# E08 — Cover the figure with reference

**Status:** SPEC — ready to run
**Author:** advisor session, 2026-08-05, on E07's Gate 1 ruling
**Priority:** highest. This replaces chart fragmentation as E08; fragmentation becomes E09 and
waits, because density is a different axis from wrong material in the right shape.

---

## 0. Rules

Unchanged: no verdicts, no memory writes, stop at gates, FLAT for texture and `--clay` for
geometry, predictions before looking. Read [E07's ruling](E07-ruling-gate1.md) first — it
closed a four-experiment line and the reason it closed is the reason this spec is shaped the
way it is.

## 1. Why this, and not another fill experiment

On the asset the Director rejected: **28.4% of texels come from the styled reference, 37.7%
from diffusion invention at denoise 1.0, 33.9% from interpolation.** E02, E05, E06 and E07
each improved how that 71.6% is filled. None reduced it. The failure follows it exactly —
the front views, where the twins reach, hold together; view 5, where they never reach, is
where materials dissolve.

Checked in source: **the two-view limit is a hardcoded list, not a property of the route.**
`restylize_views.py` takes `--inputs` as an arbitrary list and has no two-view assumption.
`project_twins.py` hardcodes two, in `VIEWS` at lines 132–137, while its ownership machinery
(`best_w` / `owner_c` / `sumW` / `sumWC` accumulated `for view in VIEWS`) is already N-view
shaped. `texpass_iter.py`'s `basis(yaw, el)` already computes a correct camera frame for any
yaw. **This is a finding, not a fix, and it is not a claim that more twins fix the asset.**

## 2. The question

**Can the styled reference cover the figure — and if it does, does the defect the Director
rejected go with it?**

Two halves, and the first is free.

## 3. Predictions — recorded before the run

The advisor's record on predictions is poor (see [CLAUDE.md](../../CLAUDE.md)); these are
blind and are recorded so they can be wrong.

| # | prediction |
|---|---|
| A1 | reachable coverage rises steeply from 2 → 6 cameras and flattens by 8 — most of the gain is the four diagonals, because a front/back pair sees no side surface at any facing threshold |
| A2 | 8 cameras reach **above 80%** of valid texels at `facing > 0.45` on the culled mesh. E05's 41% ceiling was measured **before** culling, and culling moved the equivalent brush figure 27% → 52.7% |
| A3 | hold-one-out ΔE on the rejected asset **separates the regions the Director named** — blade, boot, forearm above ΔE 10; the front torso and beard below it. **If it does not, this metric is dead and §5 halts before anything is built** |
| A4 | independently-restylized views disagree at ownership boundaries by less than the material error they replace — i.e. seams between two real references beat invention |

## 4. The metric, and it is validated before it is used

E07 failed because four of its five units were 5×5 high-pass statistics and the defect is a
**large region of the wrong material**, which is smooth inside itself. The replacement has to
fire on region colour, and it needs a ground truth rather than a number I chose.

**Hold-one-out reference agreement.** With N reference views, for each view *v*: build the
atlas from the other N−1, then compare it against what *v* actually sees, over the surface *v*
can see. The reference is the route's own definition of correct, so this has a real ground
truth and a real ceiling.

**Unit: ΔE in CIE Lab**, not luminance. ΔE ≈ 2.3 is a just-noticeable difference and **ΔE > 10
is a plainly different colour to a human** — an external constant, not one derived from this
project. Report the ΔE distribution, the share of surface above 10, and the same split per
region the Director has named.

**Why it cannot be gamed the way the last four were:** smoothing raises disagreement rather
than lowering it, and the denominator is a fixed surface set (the same mesh, the same cameras)
across every arm.

**⚠ Validate it on the rejected asset first — this is now a repo rule and it is the reason
E07 cost four experiments.** Run hold-one-out ΔE on C1 with its existing two twins before
building anything. If it does not light up the blade, the boots and the forearm on an asset
the Director rejected, **it is not a metric and this experiment halts at Gate 0.**

## 5. Gate 0 — both halves free, no GPU, no diffusion

1. **The geometric ceiling.** `project_twins.py` already computes `reachable` — texels a
   camera can see at the facing threshold, depth-tested. Loop it over camera sets of
   **N = 2, 4, 6, 8, 12** on C1's prep and report reachable share of valid texels, at
   `--facing-min` 0.45 and at the head band's 0.18. Pure geometry; the raycasting scene is
   already built. **Halt if 8 cameras do not clear 60%** — a projection route cannot clothe
   this figure from its own renders, that is the finding, and it is worth the whole spec.
2. **The metric's own validation**, §4. **Halt if it does not separate the named regions on
   the rejected asset.**

Report both, halt, and hand back. Neither needs the Director's time.

## 6. Arms — only if Gate 0 passes

| arm | reference views | cost |
|---|---|---|
| **R0** | C1 as shipped, 2 twins — the rejected asset, and the metric's negative control | 0 |
| **R8** | 8 views at the production yaws, via `restylize_views.py` with per-view prompts | ~8 min |

One variable: the number of reference views. Everything downstream runs unchanged — same
prep, same eight strokes in the same order, same seed, same prompts, same finalize.

**`project_twins.py` generalises from two hardcoded views to a yaw list.** Its ownership,
weighted blend and levelling already work for N; `basis()` in `texpass_iter.py` supplies the
frame. The `--front`/`--back` form stays as a two-element default so every prior arm still
reproduces byte-for-byte.

**A third arm is deliberately not specified yet.** Independently-restylized views may disagree
with each other, and `ig2mv_licensefree.py` makes six *consistent* views in 24 s. Whether that
consistency is needed is answered by A4's measurement, not by guessing — so it becomes an arm
only if disagreement at ownership boundaries turns out to exceed the material error it
replaces. Bound it before spending it.

## 7. Gates

**Gate 0 — §5.** Both halts numeric, both free. This is where a bad premise dies cheaply.

**Gate 1 — the Director's eye.** Head close-up and the FLAT turnaround, R8 beside C1, at his
zoom and not from a contact sheet — **including views 4–6**, which is where C1 dissolves and
where the head sheet cannot show anything. Predictions §3 first, then hold-one-out ΔE, then
his verdict. His verdict is the verdict.

## 8. Out of scope

**The brush loop.** If reference coverage rises, the brush's job shrinks on its own; tuning it
in the same experiment would confound the one variable this spec has. **Dilation** — E07's L1
is built, gate-passing and unadopted, and it waits for a route that is worth finalizing.
**Chart fragmentation and remeshing** (now E09) — density and softness, a different axis.
Also out: E03, E04, subject profiles, any change to the mesh, the prompts, the stroke order
or the seed.

## 9. If Gate 0's ceiling comes back low

Then a projection route cannot clothe this figure from renders of itself, and the rethink is
larger than a camera count. **The branch is not specified here** — specifying an unmeasured
branch is the habit that produced four wrong pass conditions — but the measurement is cheap
and it is the fork the whole texture line now turns on.

## 10. Standards compliance

**PIN_PER_STEP 3** — one variable; everything downstream reuses E02-prompts.json, seed 770700,
the same eight cameras in the same order. The two-view default keeps every prior arm
reproducible.

**ANDON_AUTHORITY 3** — two numeric halts at Gate 0, and both test a failure mode: the route
cannot reach the surface, or the instrument cannot see the defect. **The second halt is new to
this repo and is the direct remediation for E07.**

**NAMED_COMPENSATORS 2** — no irreversible or outward-facing call. Writes land under
`facet_E08/`; C1 and its state directory are read-only inputs. Undo = delete `facet_E08/`.
Owner: the executor session. *Remediation unchanged from E07: `texpass_loop.ps1` should refuse
a `-StateDir` it did not seed.*

**DECOMPOSE_BY_SECRETS 3** — the metric, the geometry probe and the projection change are three
separable pieces; the first two are diagnostics that ship regardless of whether R8 runs.

**UNCERTAINTY_GATED_HUMANS 3** — Gate 0 costs the Director nothing. Gate 1 is his, framed
contrastively against an asset he has already rejected, and it puts views 4–6 in front of him
rather than the head sheet that could not show the last arm.

**EXTERNAL_VERIFIER 3** — the pass unit is **ΔE against an external perceptual constant**, not
a threshold derived from this project's own data, and the metric is validated against a
rejected artifact before it grades anything.
