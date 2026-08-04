# E08 — Arm A4: HALTED at its own precondition. The subject is not separable from its background.

**Spec:** [E08-cover-the-figure-with-reference.md](E08-cover-the-figure-with-reference.md) ·
**Amendment 4:** [E08-ruling-gate0.md](E08-ruling-gate0.md) · **Arm A3:** [E08-armA3.md](E08-armA3.md)
**Run:** 2026-08-03, executor session. **No diffusion, no GPU. Nothing built.**
**Instrument:** [`e08_bg_separation.py`](../../tools/diagnostics/e08_bg_separation.py)

A4 was to replace the geometric proxy with the property it stands in for: accept on distance
from the twin's own background. Amendment 4 required the threshold to be **derived from the
measured bimodality**, and gated the arm on its own failure mode — *"measure subject-versus-
background separation before applying and halt if there's no gap."*

**That gate fires. There is no gap.** A4 halts before it is built, at zero cost, which is
what the gate was for.

---

## The threshold cannot be derived, because the density has no antimode

ΔE from background over the twin's keyed figure mask, front view, 0–30 in 1.0 steps:

```
  0.2- 5.0      0
  5.2- 6.0      5   ·
  6.2- 7.0     65   #
  8.2- 9.0    193   ####
 10.2-11.0    305   ######
 12.2-13.0    458   #########
 14.2-15.0    587   ############
 16.2-17.0    646   #############
 18.2-19.0  1,030   ######################
 20.2-21.0  1,180   #########################
 22.2-23.0  1,605   ##################################
 24.2-25.0  2,305   #################################################
 26.2-27.0  2,658   #########################################################
 28.2-29.0  2,644   #########################################################
```

**Monotonically rising, start to finish. No antimode anywhere.** The back view has one
shallow dip (395 → 307 → 260 → 285 across ΔE 11–14) that the front does not share, so the
two views do not agree on a location either.

**Where the apparent gap came from.** Amendment 4 cites "the gap between ~10 and ~25", and
that reading is mine as much as the advisor's — it came from comparing two *summary
statistics*: region medians (blade 24.80, tunic 42.43) against the contaminated set's median
(4.9). Two distant medians do not imply a gap in the density between them. Measured, the
populations overlap continuously.

## Otsu is the wrong tool, and its output says so

| view | cut | separability η | class means | rejects | median depth of rejects |
|---|---|---|---|---|---|
| front | 33.63 | 0.661 | 25.8 / 41.6 | 41,194 px | **8.00 px** |
| back | 33.16 | 0.674 | 25.0 / 41.5 | 28,734 px | **9.22 px** |

Otsu maximises between-class variance over the whole distribution. With the contaminated
class at **0.5% of the mask** it finds the dominant split instead — **dark paint against
light paint** — and rejects a third of the figure from its interior. η of 0.66 looks healthy
and is measuring the wrong partition entirely.

## Colour is not a proxy for boundary on this subject

| population | share | median depth into mask | within 2 px of edge |
|---|---|---|---|
| ΔE < 12 (front) | 1.04% | 2.83 px | **47%** |
| ΔE 12–25 (front) | 11.85% | 5.00 px | 26% |
| ΔE < 12 (back) | 1.43% | 2.53 px | **48%** |

Contamination is a boundary phenomenon — that part of the diagnosis holds. But **less than
half of the low-ΔE pixels are at the boundary.** The rest are interior paint that happens to
be dark or neutral. A cut low enough to spare them does not catch the contamination; a cut
high enough to catch it rejects real material from the middle of the figure.

## Restricting to thin structure does not rescue it

Within the 1–4 px half-width strata, where contamination runs 16–21%:

| | front (894 px) | back (1,201 px) |
|---|---|---|
| shape | peak at ΔE 9, then a flat plateau to 25 — **no antimode** | peak at 9, dip at 13, second peak at 21 — weak antimode |
| below ΔE 12 | 27.1% | 22.3% |
| **above ΔE 25** | **16.1%** | **28.1%** |

The two views disagree on whether an antimode exists and where. And even here, 16–28% of thin
pixels are legitimate paint above ΔE 25 — the blade among them — so any cut in the 10–15
region discards a substantial share of exactly the structure A3 set out to save.

---

## What this leaves

1. **A4 as specified is withdrawn by its own gate.** The precondition it was told to check is
   absent, and checking cost one measurement and no build. The gate design was right.
2. **The unspecified arm now has measured support.** Amendment 4 named, and deliberately did
   not specify, rendering the clay against a background no material uses. The reason no gap
   exists here is visible in the numbers: the background is mid-grey (125,126,126) and the
   subject contains mid-grey materials — steel, leather, shadowed cloth — so contamination
   and paint occupy one continuous range. A background outside the subject's gamut would
   *create* the separation that this measurement shows is missing, rather than thresholding a
   distribution that has none. Its cost is also real and unmeasured: the diffusion latent
   comes from the untouched render, so the background reaches the twin and changes it. Still
   its own arm, with its own before/after, as Amendment 4 says.
3. **A2 stands unaffected.** It is ratified, adopted, and independent of everything above.
   A3's invariant is kept and correct; it is a component of an answer, not the answer.
4. **Front's 633,518 stays unbanked.**

Artifacts: `facet_E08/A4/separation.json`, `colour_cut.png` (red = what an Otsu cut would
reject — visibly interior, which is the finding).
