# E34 — predictions, registered BLIND

**Seat:** executor · **Registered:** 2026-08-13, before any E34 artifact was built.

**Blindness, stated precisely.** No E34 control, twin, projection or render exists at the
moment of writing. Two replays ran during G1 enumeration — E33's control build for view 0
and E33's two-view projection — and both reproduce numbers **already published in
[E33-report.md](E33-report.md)** (§7's control sha256, §14b's registration/probe/fill
tables). They recovered *invocations*, not outcomes; nothing below is informed by an
eight-view result, because none has been produced. Each clause is on its own line and
states **what one counted thing is** before it states a number.

---

## The counted things, defined before any number

- **valid texel** — one texel of the 4096×4096 atlas belonging to a packed face. The cull
  parks 151,439 unseen faces on a 10×10 patch, so this is the *packed* population:
  **2,444,770**, fixed for this arc (same mesh, same prep, same cull — `prep_bake/` reused).
  This denominator cannot move, which is why the ratios below hang off it.
- **reachable texel** — a valid texel at least one camera in the set accepts (depth test,
  `--facing-min 0.45` / `--head-facing-min 0.18`, after the A3 edge-distance erosion).
  Reachability is **a property of the camera set**, so it is the quantity the view count
  is designed to move: 1,801,207 (73.7%) at two views.
- **styled texel** — a valid texel actually written from some twin. 1,517,278 at two views.
- **hole** — `valid − styled`, exactly (2,444,770 − 1,517,278 = 927,492 replays to the digit).
  P4 is therefore **not independent** of P3; it is that identity, and is stated as such
  rather than dressed up as a second prediction.
- **reg-IoU** — IoU(twin paint mask, mesh silhouette) in the render frame, per view.
- **view class** — pole (0, 4: recorded), three-quarter (1, 3, 5, 7), profile (2, 6).
  The classes differ in projected figure width: 0.334875 / 0.276081 / 0.164418 world units.

---

## P1 — reachable / valid, at eight cameras

**Band: 88–94%. Point: 91%.** (two-view baseline 73.7% = 1,801,207 / 2,444,770)

Mechanism: the 643,563 texels unreachable at two views are dominated by lateral surface —
the ±90° and ±135° cameras face it directly. What no elevation-0 exterior camera can reach
survives: under-chin, armpit, inner arm, between thighs, crown, soles, hand interiors.
Elevated cameras are closed on this route (E12 Ruling 7a/25b), so that residue is a floor.

## P2 — styled / reachable, at eight cameras

**Band: 85–93%. Point: 89%.** (two-view baseline 84.2%)

Union acceptance means a texel peeled by one camera's edge erosion may be accepted by
another, so the ratio should rise — but erosion still bites at every silhouette edge.
E08's "eight cameras reached 92.9% of reachable" is **W3's subject, not this one**, and is
used as a shape argument, not as a transferred number.

## P3 — styled / valid, at eight cameras

**Band: 76–86%. Point: 81%.** (two-view baseline 62.1%)

This is P1 × P2 (0.91 × 0.89 = 0.81) and is quoted because it is the legacy denominator the
record carries.

## P4 — holes into finalize

**Band: 342,000–587,000. Point: 465,000.** (two-view baseline 927,492)

**Derived, not independent:** `valid × (1 − P3)`. Stated so the report cannot later count
it as a separate hit or miss.

## P5 — per-view reg-IoU, and whether `--reg-iou-min 0.80` fires

- pole views 0, 4 — **unchanged at 0.8605 / 0.8475** (same twins if re-projected; the
  recorded R3 twins are reused in rows 0/4).
- three-quarter views 1, 3, 5, 7 — **band 0.82–0.87**.
- profile views 2, 6 — **band 0.70–0.82**.

**The gate firing on at least one of views 2 / 6: PREDICTED YES, ~70% confidence.**

Reasoning, registered so it can be wrong: the recorded twin is painted **34 px wider** than
the mesh silhouette (317 against 283) and sits ~30 px low. If that bleed is *absolute* — a
diffusion edge overshoot measured in pixels, which is what this repo's own law about fixed
peels versus local feature width predicts — then at the profile views, where the mesh is
only ~139 px wide, the same 34 px costs far more of the union. A rectangle model gives
≈0.73 under the absolute-bleed assumption and ≈0.80 under a proportional one. The absolute
model is the better-motivated of the two, hence the direction of the call.

Per **R-b this is a HALT, not a tune** — if it fires I stop and report numerator and
denominator per view. Predicting the halt does not license passing it.

## P6 — the named landmarks

⚠ **The dispatch says "the six named landmarks" and names five**: jaw, temple, shoulder,
ribcage, flank. Recorded here as an enumeration discrepancy rather than silently resolved;
the prediction below is over the **five named**, across the six affected views (1,2,3,5,6,7).

**Predicted: all five landmark classes lose their unpainted patches.** All five sit on
lateral or antero-lateral surface that the ±45°/±90°/±135° cameras face directly.

**Predicted residual dilation-fill, at deep-occlusion sites only:** under-chin, armpit,
inner arm, between thighs, hand interiors.

*Falsifier, and the one that matters:* a landmark patch surviving eight views is surface no
exterior camera faces, which redirects the remedy to an R3 brush/inpaint question for the
Director rather than to more cameras.

## P7 — cloud spend

**Band: $0.55–$0.72 on the GPU-hours day bucket. Point: $0.61.** (6 jobs × $0.102, E33 §8)

**Partner-API lines: predicted to move by exactly zero**, every line, both reads.

Carries E33's attribution caveat by construction: this is a whole-day-bucket delta across a
window, and exclusivity is not provable from here.

## P8 — the finalize gates

- `dist_median_edges` — **band 1.6–2.7, point 2.2** (limit 3.0; E33 measured 2.974, a 1% margin).
- `dist_beyond_pct` — **band 0.2–0.9, point 0.5** (limit 5.0; E33 measured 1.024).

Mechanism: nearer paint exists on lateral surface, so the search for a source colour ends
sooner. **`mean_fallback` 0 is structural in surface-aware mode and is not a pass**
(E14 Ruling 31d) — it is excluded from this prediction.

## P9 — regression at the poles

**Predicted: views 0 and 4 show no new unpainted patches**, and their styled coverage does
not fall. Ownership may be reassigned to neighbouring cameras where those face the surface
more squarely; reassignment is not loss.

**Predicted: the recorded GLB's sha256 is unchanged** — `9e20ea7d…`, 21,588,628 bytes.

*Falsifier:* a new patch or off-register material on either pole view.

## P10 — largest 4-connected component, dilated class

**Band: under 60,000 texels. Confidence: weak, and stated as weak.**

⚠ **The corresponding E33 number has not been measured**, so this is registered as an
absolute with no baseline behind it. Per this repo's own law — never define a condition as
a fraction of a quantity not yet measured — it is **a diagnostic, not a pass condition**,
and the E33 before-number will be measured at Stage 7 and reported beside it.

---

## What would make me wrong in a way worth reading

The nine-arc failure family here is the **unit / population**: a real-looking number counted
over the wrong object. The exposure in this set is **P1 and P2 sharing the word "reachable"
while it means different things at two cameras and eight** — reachability is defined by the
camera set, so the two-view 73.7% is not a baseline that eight views "improve" so much as a
different measurement of a different set. The valid-texel denominator is pinned precisely
so that at least P3 and P4 stand on ground the experiment cannot move.

The second exposure is **P5's rectangle model**, which treats silhouettes as boxes. Real
figures have limbs; a profile view's arm may occlude the torso and change the union in a way
no rectangle predicts.
