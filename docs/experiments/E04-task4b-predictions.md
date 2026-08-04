# E04 Task 4b — backdrop prediction, registered BEFORE the derivation is run

**Executor session, 2026-08-04.** Written before `e04_backdrop.py` has been run once. I have
seen the fixture's twelve materials and assigned each an expected sRGB from its name; I have
**not** computed a single distance.

## What is being derived

S-backdrop: the twins' backdrop is prompted, one word, and it is the only free operand in the
key's `max_channel |pixel − backdrop| > 0.06`. Choose it to **maximise the minimum distance**
from every declared material, weighted toward the dark thin elements (G9 is the exposed one),
avoiding G11's declared blue.

## Predictions

| # | prediction | falsifiable as stated |
|---|---|---|
| **B1** | **No neutral grey can win.** The declared materials span the value range from black tar (~0.15) to pale canvas (~0.79), so every grey sits close to something. The best neutral's minimum distance will be **below 0.25**. | fails if a neutral scores ≥ 0.25 |
| **B2** | **The winner will be saturated**, because the key takes the **max channel**, and a saturated colour can be far from a neutral material in at least one channel while a neutral cannot. | fails if the unconstrained optimum is within ΔE 20 of neutral |
| **B3** | The optimum will sit in the **green–magenta** region — away from the warm register (G1/G2/G4/G5/G10/G12 are all warm) and away from G11's blue and G6's verdigris. | fails if it lands warm or blue |
| **B4** | Weighting toward G9 (dark tar, ~0.17) pushes the backdrop **paler**, not darker. | fails if the weighted optimum is darker than the unweighted |
| **B5** | The minimum distance for the chosen backdrop will exceed **4× the 0.06 cut** (i.e. ≥ 0.24) — comfortably clear for every material, so no declared material sits near the key's threshold. | fails if < 0.24 |

## What I expect to have to report as a tension

A backdrop chosen purely by this metric is likely to be **strongly coloured**, and a strongly
coloured backdrop bleeds into a diffusion image — the model lights the subject with it. So I
expect the honest output to be a **table with a trade**, not a single winner: the metric's
optimum, and the best *low-saturation* option with its cost. **Which to adopt is not mine** —
I will report both with their minimum distances and let the ruling choose.

I am also recording now, before seeing any number, that **these material colours are my
estimates from the fixture's words.** They are the weakest link in the derivation. The
fixture's own instruction is that bands cross-check against the styled target pair once it
exists; the same applies here — this derivation must be re-checked against the pair, and if
the pair's actual materials sit elsewhere, the backdrop follows them, not this table.
