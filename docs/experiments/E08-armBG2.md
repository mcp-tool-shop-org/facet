# E08 — BG2: hold the control constant, vary only the latent background

**Spec:** [E08-cover-the-figure-with-reference.md](E08-cover-the-figure-with-reference.md) ·
**Amendment 6:** [E08-ruling-gate0.md](E08-ruling-gate0.md) · **BG1:** [E08-armBG.md](E08-armBG.md)
**Run:** 2026-08-03, executor session. **GPU: 4 diffusion passes, ~3.5 min.**
**Prediction, recorded before generation:** `facet_E08/BG2/PREDICTIONS.md` — blind.

The change: `restylize_views.control_image()` takes the figure mask from the **exact raycast
mesh silhouette** (`--masks`) instead of keying it off the render. Same move A2 made for the
projection path, and it retires `figure_mask` from the last place it governed anything.

---

## The control is now pinned, and the number says so

| view | contour px | canny px | control divergence between arms |
|---|---|---|---|
| front | **9,958 both arms** | 15,325 / 15,329 | 46 px = **0.219%** of lit |
| back | **9,958 both arms** | 13,029 / 13,025 | 25 px = **0.134%** of lit |

The contour term is **identical by construction** — same mesh, same camera. Only Canny moves,
and only where the antialiased rim blends against a different background. Figure mask 19.0% on
all four passes, against a true silhouette of 19.01%.

Against BG1, where the mask was keyed: contour **33,026 (grey) vs 9,699 (blue)**.

## The repaint largely goes with the control

ΔE between the grey-background and blue-background twins, inside the exact silhouette eroded
9 px:

| view | | median ΔE | mean | p95 | >10 | **>25** |
|---|---|---|---|---|---|---|
| front | BG1 (keyed control) | 14.30 | 16.78 | 38.84 | 69.9% | **19.1%** |
| front | **BG2 (pinned control)** | **8.19** | 9.63 | 22.09 | **38.3%** | **2.3%** |
| back | BG1 | 11.41 | 16.86 | 48.17 | 56.1% | **23.2%** |
| back | **BG2** | **6.06** | 7.60 | 19.14 | **21.9%** | **2.1%** |

**The share above ΔE 25 — gross material change — collapses from ~20% to ~2%, roughly tenfold.**
Median falls to below the ΔE 10 "plainly different colour" line on both views.

### What the eye adds, and it is the decisive part

`facet_E08/BG2/bg2_compare.png`, columns *BG1 grey | BG1 blue | BG2 grey | BG2 blue*:

- **BG2 grey and BG2 blue carry the same materials.** Brown fur boot wraps in both, wine-red
  skirt panel in both, gold pauldrons in both, no gold knee plates in either. The differences
  read as tone and rim light.
- **BG2 grey does not match BG1 grey — it matches BG1 *blue*.** BG1 grey had gold knee plates
  and dark charcoal boots; BG2 grey has fur wraps and no knee plates, like BG1 blue.

That second line is the finding. **Changing the control moved the baseline**, which localises
BG1's material relocation to the control rather than to the background. My pre-registration
warned this would happen and that the new grey twin must not be compared against the old one;
it happened, and it is why the comparison had to be regenerated on both sides.

## Separation survives the change

| view | grey | blue |
|---|---|---|
| front | min ΔE to gamut **0.35** | **58.44** |
| back | **0.40** | **64.16** |

Both views agree, and the baseline background remains effectively inside the subject's own
gamut.

## Predictions

| # | prediction | outcome |
|---|---|---|
| C1 | repaint reduces substantially, median lands in 6–11 | **CORRECT** — 8.19 and 6.06 |
| C2 | some drift survives; rim-light is latent bleed no control governs | **SUPPORTED** — 38.3% / 21.9% still above ΔE 10, and it reads as tone |
| C3 | control images differ by under 2% of lit pixels | **CORRECT, and conservative** — 0.219% / 0.134% |

First run this arm where my predictions held. They were predicting *against* the advisor's
cleaner outcome, and the advisor's mechanism is the one the data supports.

---

## Where this lands against Amendment 6's decision rule

Amendment 6 pre-registered two branches: *still repaints* → arm dead and the erosion's cost
confirmed necessary; *doesn't* → colour separation, a correct keyed mask, and the blade.

**The measurement is between them, and that is reported rather than resolved.** Gross material
relocation is gone — the ΔE > 25 share falls ~10× to about 2%, and the two arms carry the same
materials by eye. A tonal difference remains: median ΔE 8.19 / 6.06, below the ΔE 10 line, with
38.3% / 21.9% of the silhouette above it.

What is not in dispute: **most of BG1's repaint was the control, not the background**, and the
control is now pinned to geometry with 0.13–0.22% divergence between arms.

Whether a residual tonal shift of that size disqualifies the reference is a judgement about the
reference, and the Director has not seen these twins. `bg2_compare.png` is the artifact.

Unchanged: A2 stands at 28.4% → 39.1%. A3's invariant is kept as a component. Front's 633,518
stays unbanked.

Artifacts: `facet_E08/BG2/` — `PREDICTIONS.md`, `masks/`, `twins_grey/`, `twins_blue/`,
`bg2_compare.png`.
