# E13 — the detail pass: crop twins as projection sources

**Spec, written before the work** (advisor, 2026-08-06, on the Director's direction —
E12 Ruling 19). The beast's intricate structures — horns, crown and cheek frill, wing
finger struts, fangs — diverge from the clay at twin scale because a full-figure frame
gives the whole head ~1.6% of its pixels. The companion measured the cure without
being allowed to be it: at 11.2× the pixel area, the same mouth went from mush to
legible plates — and its sidecar rightly forbids projecting an artifact generated at a
non-route camera under a spec-source declaration. This experiment makes the mechanism
route-legal: **crop-framed twins, generated at the route's own yaws under
projection-source declarations, projected FIRST so their paint owns the detail texels.**

The Director's sentence that opens it: *"We should be treating the bones like we do
the humanoid's face, so that the intricate details don't get rendered into mush."*

## The question

Does a crop-framed twin, projected through a crop camera, deliver measurably and
visibly crisper detail-region texture than the full-figure twins alone — without
disturbing registration, the never-overwrite invariant, or any anchored number?

## Hypotheses, with predictions stated before any run

- **H1 — capability.** `project_twins` extended with crop-camera parameters
  (`--ortho-scale`, `--centre`, per-view) reproduces a known full-frame projection
  **pixel-identical** when invoked through the new path at full-frame values.
  *Predicted: holds — the parameters default to the values the tool already derives.
  If this fails, nothing downstream runs.*
- **H2 — registration.** A head-crop twin registers to the crop silhouette at the
  companion's precedent level (its styled-vs-geometry IoU measured 0.993953).
  *Predicted: IoU ≥ 0.98 at the crop frame; the registration halt stays suspended and
  the number is reported.*
- **H3 — the payoff.** On the head-region texels, the crop-projected atlas carries
  visibly crisper horn/crown/fang detail than stage 1's full-figure paint at the
  Director's zoom, and the texel-level provenance shows the crop twin owning the
  region. *Predicted: the difference is legible at 3× the way the companion's muzzle
  plates were — and if it is NOT, that is a full-success negative: the mush would be
  survivable resolution loss in projection, not generation, and the texel-allocation
  lever (head-scale) becomes the primary arm instead.*

## Arms

- **A0 — baseline**: stage 1 as planned, eight full-figure twins, no crop pass.
  Exists by construction; costs nothing.
- **A1 — the head-crop pass**: crop twins at the head box (`head_00003.json`, padded
  1.12, the companion's frame derivation) for the yaws where the head carries detail
  the route must keep — **yaw 0 and yaw 45 first** (the front-family, where D8/D10
  and both horns present; view 315 joins if the first two prove). Crop silhouette by
  direct raycast at the crop camera (`e12_crop_silhouette.py`, proven); control at
  the ruled canny 0.05/0.10 (companion construction, proven); stems by the deletion
  construction with per-crop visibility verification (`headclay_0`'s precedent, drop
  map re-verified per yaw). Projected BEFORE the full-figure eight.
- **A2 — texel allocation** (measured, then armed or declined): `bake_hero_prep
  head-scale > 1.0`. The value derives from the measured gap between the crop paint's
  resolution and the head region's current texel density — reported as arithmetic
  before any re-bake, with the re-bake's downstream cost (a new atlas invalidates
  nothing yet — stage 1 has not run) stated beside it. If armed, it lands before
  stage 1 so the whole route runs on the allocated atlas.

## Metrics and gates

- **Gate 0 (ANDON, blocks everything): the H1 anchor.** The extended projector,
  invoked through the new parameter path at full-frame values, reproduces a recorded
  projection pixel-identical. Any deviation halts the experiment at zero spend.
- **Gate 1 (per crop twin, before projection):** the 16e palette gate + 17d
  achromatic channel against the pair baselines; registration IoU reported; the
  bounded re-roll precedent applies per crop view.
- **The judging artifact:** a three-column sheet per region — clay crop | stage-1-only
  texture render | crop-pass texture render — at the Director's zoom, with the
  provenance panel showing per-texel ownership. **The eye rules the payoff (10d);
  no numeric structure gate is commissioned** — the metrics report, the sheet decides.
- Coverage accounting: crop projection must not change reach (the crop cameras re-see
  eye-level-reachable surface). The ceiling instrument re-run confirms 50.46% of
  3,240,510 unchanged; any delta is a halt (it would mean the crop camera geometry is
  wrong, not that reach improved).

## Out of scope

Wing-strut or claw crop passes (they join only if the head pass proves and the
Director asks); any elevated camera (Ruling 7 stands); any change to the eight-view
base coat, the accepted pair, the bands, or the stems beyond per-crop visibility
stems; the allocation ladder's geometry rung (his sentence only); the brush stage.

## Standards compliance (this spec)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Every crop frame derives from the recorded head box by the recorded rule; the anchor gate pins the tool extension to a recorded projection; seeds/stems/controls per sidecar as throughout the arc |
| ANDON_AUTHORITY | 3 | Gate 0 halts the whole experiment on any anchor deviation at zero spend; per-twin gates before projection; the reach-invariance check halts on any ceiling delta; the payoff is judged at the Director's eye, not passed by a statistic |
| NAMED_COMPENSATORS | 2 | Crop projection runs on a copied atlas state until ruled in (the accumulating state is a file; the compensator is not consuming it); generations bounded with estimate_credits first; nothing pre-existing modified |
| DECOMPOSE_BY_SECRETS | 3 | The capability (crop cameras) is separated from the policy (which regions, which yaws); the allocation arm (A2) is measured independently of the generation arm (A1); stems derive per crop from the committed builder |
| UNCERTAINTY_GATED_HUMANS | 3 | Opened by the Director's sentence; the payoff gate IS his zoom on the three-column sheet; A2 arms only on reported arithmetic; H3's negative branch is pre-registered as a full success with its consequence named |
| EXTERNAL_VERIFIER | 2 | The anchor tests the new code path against output the old path produced; the payoff is judged by the eye the numbers cannot replace. `skip:` on a second model per the arc's precedent |
