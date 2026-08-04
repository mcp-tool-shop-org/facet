# E08 — registration: does the twin sit where the mesh is?

**Amendment 7:** [E08-ruling-gate0.md](E08-ruling-gate0.md) · **BG2:** [E08-armBG2.md](E08-armBG2.md)
**Run:** 2026-08-04, executor session. **No GPU.**
**Instrument:** [`e08_registration.py`](../../tools/diagnostics/e08_registration.py)

E01 made this the criterion: silhouette IoU 0.290 → 0.777 was the fix, and carrying a
mis-registered twin collapsed styled coverage 62% → 22.7%. Truth is the exact raycast
silhouette at **19.01% of frame, bbox 849 × 388**.

---

## The instrument failed first, loudly, and was fixed before anything was read from it

The corner-median key — `figure_mask`'s construction, used everywhere in this pipeline —
returned painted fractions of **31–76%** against a 19.01% truth, with figure bounding boxes
**751 px wide in a 752 px frame**. A figure cannot be 751 px wide when the mesh is 388.

Diffusion paints a **lit studio gradient**, not the flat field it was given, so a single
corner median is the wrong background model and every pixel far from a corner exceeds
tolerance. Replaced with a per-channel quadratic surface fitted over a border ring the figure
cannot reach. It reduces to the corner median when the background really is flat, which is
why the shipped twin's numbers barely move (17.43% → 17.38%, IoU 0.9107 → 0.9088).

## The clean comparison — grey against grey

Same background, so keying difficulty is identical and **the control is the only difference**.

**View 0** (truth 19.01%)

| twin | painted % | IoU @.06 | IoU @.04 | IoU @.10 | bbox h × w |
|---|---|---|---|---|---|
| shipped | 17.38 | 0.9088 | 0.9229 | 0.8818 | 843 × 384 |
| BG1-grey (keyed control) | 17.73 | 0.9040 | 0.9017 | 0.8848 | 851 × 384 |
| **BG2-grey (geometry control)** | **18.95** | **0.9314** | **0.9357** | **0.9070** | 851 × 389 |

**View 4**

| twin | painted % | IoU @.06 | IoU @.04 | IoU @.10 | bbox h × w |
|---|---|---|---|---|---|
| shipped | 17.01 | 0.8900 | 0.9071 | 0.8620 | 838 × 386 |
| BG1-grey | 18.27 | 0.8638 | 0.8685 | 0.8523 | 858 × 385 |
| **BG2-grey** | **19.93** | **0.9222** | 0.8988 | **0.9261** | 866 × 390 |

**BG2-grey registers best on five of six cells, and its painted fraction is closest to the
19.01% truth on both views** — 18.95 and 19.93 against the shipped twin's 17.38 and 17.01,
which are both undersized. The ranking is stable across tolerance, so it is not a keying
artifact.

## The second question, answered: the extra control was noise

BG1-grey's control carried **33,026 px of contour against BG2's 9,958** — 3.4× more. If that
surplus had been interior crease detail, BG1-grey should register at least as well.

**It registers worse, on both views, at every tolerance.** The surplus was spurious edges from
a mask that held 111,602 px of a 146,356 px silhouette. Not a second accidentally-load-bearing
defect — just a defect.

## The blue twins cannot be measured this way, and that is itself a finding

A quadratic fit does not capture their background, and the answer moves with the threshold:

| | ΔE>8 | ΔE>12 | ΔE>20 |
|---|---|---|---|
| BG1-blue IoU (cubic fit) | 0.6124 | 0.7674 | 0.9183 |
| BG2-blue IoU (cubic fit) | 0.6047 | 0.7190 | 0.8658 |

IoU swings 0.61 → 0.92 on threshold alone, where the grey twins hold 0.90–0.93 across their
range. **Picking ΔE 20 because it produces a clean number is the move this repo exists to
prevent**, so no blue registration figure is reported.

The limitation is decision-relevant on its own: `project_twins`' edge test needs the twin's
**own painted-figure mask** — the "is the paint trustworthy" question, which geometry cannot
answer — and on a blue-background twin that mask is threshold-dependent.

---

## Against the pre-registered branches

Amendment 7 pre-registered: *BG2 registers better → adopted; worse → arm dies; no difference →
the Director's eye.*

**The result splits along a seam the branches did not have, because BG2 changed two things:**

1. **The geometry-derived control — measured, and it registers better.** BG2-grey against
   BG1-grey isolates it exactly, and it wins on both views at every tolerance, with painted
   fraction moving toward truth. By the pre-registered criterion this is adopted, and no taste
   is required.
2. **The blue background — not decidable on registration.** Its figure mask is not robustly
   extractable, so the criterion cannot be applied to it.

So the arm's *first* half clears the bar and the *second* half is undecided on this axis. The
material differences the Director would be ruling on — gold knee plates against fur wraps —
belong to the first half, since BG2-grey already carries them at the reference background.

## One reproducibility observation

BG1-grey is built exactly as the shipped front twin was — same clay, same default prompt, same
seed, same keyed-mask control — and does not reproduce it: painted 17.73 vs 17.38, IoU 0.9040
vs 0.9088. Close, not identical. Consistent with the defect already filed: the shipped twins'
generation parameters are not fully recorded in the repo.

Artifacts: `facet_E08/BG2/registration.json`.
