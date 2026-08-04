# E08 Task 2 — eight cameras: predictions, recorded before the run

**Executor session, 2026-08-04.** Written after Amendment 27's steps 1–3 landed and their
anchors re-ran, and **before the eight-camera projection was run once.** Blind with respect to
it: no eight-camera atlas or diagnostic existed on disk when this file was hashed. Per
Amendment 27's standing method — *when a prediction can be hashed before the artifact exists,
hash it.*

## What is being read against what

The one variable is **camera count**: 2 → 8, same twins, same flags (`--edge-absolute`,
fitted key, intersection now default-on), same mesh, same prep.

Baseline, the adopted 2-camera figure from Amendment 27:

```
styled 1,042,794 / 2,402,810 valid = 43.4%      reachable 1,265,391 = 52.7% of valid
styled / reachable = 82.4%       variance 0.02587      holes 1,360,016
```

**The acceptance lever is spent; eight buys from the ceiling.** So the prediction is built as
*reachable × acceptance*, and the two factors are predicted separately because they can fail
separately.

## Checking the ceiling rather than inheriting it

[E08 Gate 0](E08-gate0.md) measured 8-camera reach at **1,780,546 texels = 74.10% of valid**,
from `e08_ceiling.py`. This run reports `reachable/valid` directly, so it **tests** that number
rather than assuming it. The two tools could disagree if `e08_ceiling` used a different head-band
facing floor; I have not read it, deliberately, so this stays a real test.

**Predicted: reachable within ±1% of 1,780,546 (74.10% of valid).** An exact match is agreement
between two independently written instruments; a large miss means one of them is wrong about the
facing floor and the ceiling arithmetic in four documents needs restating.

## The numbers I am committing to

| quantity | 2-camera baseline | 8-camera prediction |
|---|---|---|
| reachable | 1,265,391 (52.7%) | **~1,780,546 — 73.4–74.8% of valid** |
| styled / reachable (acceptance) | 82.4% | **82–86%** — flat to slightly up |
| **styled** | 1,042,794 | **1,460,000–1,530,000** |
| **styled / valid** | 43.4% | **60.8–63.7%**, central ~61% |
| holes (= valid − styled) | 1,360,016 | **~873,000–943,000** |
| variance | 0.02587 | **0.026–0.031**, up |
| registration ANDON (IoU < 0.80) | — | **does not fire.** Min measured IoU is view 6's 0.8329 |
| bbox NOTE (diagnostic) | none on 0/4 | **exactly one, view 6** (width ratio 1.921) |
| background probe | no relaxation | **no relaxation on any view** — `--edge-absolute` makes `ed == e_abs_s`, so the relaxed set is empty by construction |

**Why acceptance flat-to-up rather than down.** A texel is *reachable* if any view sees it
front-facing and unoccluded, and *styled* if some view additionally passes edge+mask. Adding
views gives each texel more independent chances to pass, and `project_twins` accumulates per
view with `w > best_w`, so a view that rejects cannot veto one that accepts. That is a
monotone argument for acceptance rising. Against it: the newly-reachable texels are ones only
oblique cameras can see, so they sit disproportionately near rims and in thin structure where
the edge test bites hardest. I expect those to roughly cancel, with the monotone effect
slightly ahead — hence 82–86% rather than a symmetric band.

**Why not the 55% that justified this arm.** [E08 Arm B's prediction B3](E08-armB-predictions.md)
said ~55% of valid, from 74.10% reach × **81.6%** acceptance measured in the A2 era. Acceptance
is now 82.4% on these twins, so the same arithmetic gives ~61%. If the result lands near 55%
rather than 61%, acceptance fell to ~74% and the "spent lever" framing needs revisiting.

## The blade band (Amendment 27 §9a), predicted across all eight

Measured on views 0 and 4: **0 of 46,197 and 0 of 31,699** candidate texels landing on the band
of surface the twin's key excludes were accepted, in both arms.

**Predicted: 0.00% accepted on all eight views.** The mechanism is arithmetic, not statistical —
outside `fm`, `dist_in` is 0 by definition, and the edge test needs ≥ 3.85 px. A nonzero
acceptance anywhere would mean the band is not actually outside `fm` on that view, which would
be worth knowing.

**Predicted: the band shrinks on the profile views (2 and 6)** where the blade is seen edge-on
and projects to fewer pixels, and stays comparable on the three-quarter views. I have no
prediction for whether the *union* over eight cameras leaves the blade unpainted — a view that
sees the blade broadside might key it better if the local contrast against the backdrop happens
to be higher there. **That is the number I am least able to guess and the one most worth having.**

## What would falsify what

- **styled below 1,400,000** → acceptance fell below ~79%; the oblique views' texels are harder
  than I allowed and the "lever is spent" reading needs the acceptance rate broken out per view.
- **styled above 1,560,000** → either reach beats 74.10% or acceptance beats 86%; check reach
  first, because that is the inherited number.
- **reachable off 1,780,546 by more than 1%** → the two instruments disagree about the facing
  floor. Report; do not reconcile.
- **the registration ANDON fires** → my reading of its calibration is wrong, or a twin moved on
  disk since `keyed_outside.py` measured it. Halt and report; do not touch the threshold.
- **any blade-band acceptance above 0%** → the band is not outside `fm` on that view and §9a's
  mechanism is view-dependent.

## What this prediction does not claim

Nothing about whether the asset is better. Coverage is not quality; E07 demonstrated that a
metric can move 70× while the asset is unchanged to the eye. **Gate 1 is the Director's** and
Task 3 exists to put an artifact in front of him.
