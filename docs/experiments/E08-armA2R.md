# E08 — A2 re-run: does a better-registered twin buy more surface?

**Amendment 8:** [E08-ruling-gate0.md](E08-ruling-gate0.md) ·
**Registration:** [E08-registration.md](E08-registration.md) · **A2:** [E08-armA2.md](E08-armA2.md)
**Run:** 2026-08-04, executor session. **No GPU.**
**Prediction, recorded first:** `facet_E08/A2R/PREDICTIONS.md` — blind, and all three held.

Two things ship together, as ruled: the **BG2-grey twins** replace the shipped pair, and
`project_twins`' twin-paint keying moves to the **fitted-background estimator**. The erosion
stays absolute (`--edge-absolute`), matching A2, so the comparison has one moving part.

**Reproduction anchor:** `--mask-keyed --edge-absolute --key-corner-median` still produces C1's
stage 1 **byte-for-byte**. Three legacy flags now, each earned.

---

## The result

| | styled texels | of valid | **of reachable** | holes into stage 2 |
|---|---|---|---|---|
| shipped (C1) | 681,212 | 28.4% | 53.8% | 1,721,598 |
| A2 (geometry mesh mask) | 938,718 | 39.1% | 74.2% | 1,464,092 |
| **A2R** | **1,032,433** | **43.0%** | **81.6%** | **1,370,377** |

Ceiling is 52.66% of valid — what two cameras can physically reach. **81.6% of it is now
carried by reference**, against 53.8% at the start of E08.

## The gain is the twins, not the keying — decomposed rather than asserted

| arm | twins | keying | styled | of valid |
|---|---|---|---|---|
| A2 | shipped | corner-median | 938,718 | 39.1% |
| **A2R-a** | **shipped** | **fitted** | 936,441 | 39.0% |
| **A2R** | **BG2-grey** | **fitted** | **1,032,433** | **43.0%** |

**The estimator alone moves nothing** — −2,277 texels, −0.1 points. That is the design working:
it reduces to a corner median on a flat background, so no prior arm loses comparability. **The
entire +4.0 points is the better-registered twin.**

The keying is still load-bearing, but as an *enabler* rather than a contributor: BG2-grey
carries a diffusion-painted gradient backdrop, and corner-median keying on it returned 50.68%
of frame. Without the estimator these twins are unusable.

Twin paint accepted, eroded, front / back: **15.7% / 15.2% → 17.1% / 18.2%** of frame, against
a 19.01% silhouette. The better-registered twin simply reaches closer to the mesh, so the same
3.8 px erosion rejects less.

## Guards

- **`reachable` invariant held at 1,265,391 exactly.** It is facing ∧ depth on the mesh with no
  twin input; had it moved, the comparison would have been void.
- **The bbox andon passed and is now standard**: twin paint 843 × 385 and 859 × 386 against a
  mesh silhouette bbox of 849 × 388 — within 1.2%. The same check reads 936 × 751 on a broken
  key, which is how the registration failure was caught before any number was believed.

## The background probe — the standard check, and it is not free of cost

| set | styled | median ΔE from the twin background | within ΔE 10 |
|---|---|---|---|
| A2 | 938,718 | 38.45 | **0.28%** |
| A2R-a | 936,441 | 38.47 | **0.26%** |
| A2R | 1,032,433 | 37.63 | **0.52%** |
| **A2 → A2R newly styled** | 148,693 | 32.72 | **2.03%** |

**A2R is not strictly additive**: 148,693 texels newly styled, **54,978 lost**, net +93,715.
Different twins paint different regions, so A2's `lost 0` property does not carry.

And the newly-styled set sits at **2.03%** within ΔE 10 of background against the trusted
set's 0.26–0.28% — roughly 7× enriched, small in absolute terms, and at the same magnitude as
the 2.0% limit already written for the erosion probe in a different population. Reported, not
ruled on: no threshold has been set for this population, and setting one after seeing 2.03%
is the move the ledger exists to prevent.

## Predictions

| # | prediction | outcome |
|---|---|---|
| D1 | styled 39.1% → 40.5–43%, i.e. 975,000–1,035,000 | **CORRECT** — 1,032,433 = 43.0%, top of range |
| D2 | the gain sits in the edge test; ceiling unchanged at 52.66% | **CORRECT** — reachable exactly 1,265,391 |
| D3 | the bbox guard passes, within ~1% | **CORRECT** — within 1.2% |

---

## Open

1. **The 2.03%.** Whether a sevenfold enrichment of background-adjacent texels in the newly
   styled set is acceptable, and what population the standard probe should gate on.
2. **The 54,978 lost texels** — surface A2 carried and A2R does not. Not characterised here.
3. **The Director has still not seen these twins**, and the material differences (gold knee
   plates against fur wraps) remain a canon question rather than a measurement.

Artifacts: `facet_E08/A2R/` — `PREDICTIONS.md`, `styled_stage1.png` (+ holes, styled mask),
`a_shipped_fitted.png` (the estimator-only control), `repro.png` (byte-identical legacy path).
