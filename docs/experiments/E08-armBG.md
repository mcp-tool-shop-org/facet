# E08 — background arm: the separation appears, and the reference repaints. HALTED.

**Spec:** [E08-cover-the-figure-with-reference.md](E08-cover-the-figure-with-reference.md) ·
**Amendment 5:** [E08-ruling-gate0.md](E08-ruling-gate0.md) · **Arm A4:** [E08-armA4.md](E08-armA4.md)
**Run:** 2026-08-03, executor session. **GPU: 4 diffusion passes, ~3.5 min.**
**Predictions, recorded before any twin was generated:** `facet_E08/BG/PREDICTIONS.md` — blind,
and **all three falsified.**

---

## The pin, and the one place it could not be taken literally

**The back twin's original prompt is not in the repo.** `E02-prompts.json` holds the eight
brush strokes, not the two twin cameras; `restylize_views.py` has a single front-flavoured
`--prompt` default; E02's report states the back used a different one.

So the A/B was generated on **both sides** with the same pinned prompt per view, rather than
comparing a new blue twin against the shipped grey one. That satisfies "vary only the render
background" exactly — comparing against the shipped twin would have varied the prompt too.
The back prompt is reconstructed from `E02-prompts.json`'s stated `_rule` with `_palette_spine`
byte-identical, and is used identically on both sides, so it cannot confound the comparison.

**Render side pinned exactly:** re-rendering the clay at the default background reproduces the
shipped `views/w3clay_0.png` and `w3clay_4.png` **byte-for-byte** (sha `4d65b67abae2928f`,
`d2c6153be6e1d7ac`). `turn_render.py` gained `--bg`; its default is unchanged, so every prior
render still reproduces.

## Requirement 1 — the colour, derived

Subject gamut harvested from both twins inside eroded figure masks, 198,001 Lab samples;
occupancy grid at 2 ΔE/cell; every realisable sRGB colour read off the distance transform.

```
DERIVED   rgb (0, 0, 255)      minimum dE to the subject gamut  123.31
CURRENT   rgb (125,126,126)    minimum dE to the subject gamut    6.00
```

Runner-ups are all blue-violet — (82,0,255) at 118.68, (173,0,255) at 108.35 — which is what a
warm subject (skin, gold, red beard, brown leather) plus a green tunic implies.

**6.00 is below the ΔE 10 "plainly different colour" line.** That is A4's failure stated as one
number: the background was inside the subject's gamut, so there was nothing to threshold.

## Requirement 3 — the separation appears, and both views agree

| view | background | output background rgb | **min ΔE to subject gamut** |
|---|---|---|---|
| front | grey | (122,122,122) | **0.00** |
| front | **blue** | (1,14,111) | **54.15** |
| back | grey | (110,110,112) | **0.20** |
| back | **blue** | (2,14,127) | **61.05** |

The baseline background is *literally inside* the gamut — minimum distance 0.00 and 0.20.
Under blue it clears to 54–61, and the two views agree in direction and magnitude, which is
the agreement A4 could not produce.

**Predictions B1 and B2 falsified.** I expected the prompt to win: it still says *"plain grey
background"* on both sides, and at denoise 0.92 I expected the twin to come back grey.
It did not — output ΔE to blue 71.2 / 62.5 against ΔE to grey 77.1 / 83.2. The render
background beat an explicit prompt term.

Side effect, measured and worth its own line: the clay's keyed figure mask went **9.9% → 18.1%**
of frame against a true silhouette of **19.01%**. The blue background fixes E01's keying failure
at its source. A2 already replaced that mask with geometry, so nothing depends on it — but it
confirms the mechanism outright.

## Requirement 2 — the subject repaints. **The halt fires.**

ΔE between the grey-background twin and the blue-background twin, inside the exact raycast
mesh silhouette, eroded 9 px so no background fringe enters:

| view | px | median ΔE | mean | p95 | >10 | >25 |
|---|---|---|---|---|---|---|
| front | 126,822 | **14.30** | 16.78 | 38.84 | **69.9%** | 19.1% |
| back | 126,822 | **11.41** | 16.86 | 48.17 | **56.1%** | 23.2% |

**Prediction B3 falsified** — I expected the subject to hold, because the clay's figure pixels
are byte-identical between arms.

And it is not a hue shift. Looking at `facet_E08/BG/repaint_compare.png`, the changes are at
material level, on the exact terms the prompt held byte-identical in `_palette_spine`:

| prompt asked for | grey background | blue background |
|---|---|---|
| "gold knee plates" | present | **gone** |
| "heavy dark charcoal boots" | dark charcoal | **brown fur** |
| "dark wine-red layered cloth skirt" | wine-red | **green with a red centre panel** |

The figure also carries blue rim-light, and the background is rendered as a lit studio
gradient rather than the flat field it was given. **The background change overrode identity
terms the prompt pinned.**

### One thing this run cannot separate

The control image changed too — contour 33,026 → 9,699 px — because it is built from the keyed
clay mask, and the mask got correct. So "control construction" is pinned as *code* but not as
*output*. Part of the repaint may be the better contour rather than blue bleeding into the
latent, and this run cannot apportion it. Both are downstream of the single varied input.

---

## The result, which was pre-registered

Amendment 4 stated the reading in advance: *"If the subject does repaint, the honest position
is that this twin's keying isn't separable — the contaminated band goes to stage 2 as hole,
which is what the absolute erosion already does at the blade's cost, and we'd then know that
cost is necessary rather than accidental."*

**That is the outcome.** The separation is real and reachable; the price is the reference, and
the reference is what the whole route is for. So:

- **The absolute erosion's cost at the blade is necessary, not accidental.** It was doing a job
  nobody had written down (A3), and no cheaper way of doing that job has survived: not the
  half-width invariant (A3 — shape-blind), not a colour cut (A4 — no bimodality), not a
  background outside the gamut (here — separates, but repaints the reference).
- **A2 stands and is unaffected**, 28.4% → 39.1% reference coverage.
- **A3's invariant is kept and correct** as a component.
- **Front's 633,518 stays unbanked.**

Artifacts: `facet_E08/BG/` — `derive.json`, `PREDICTIONS.md`, `clay_grey/`, `clay_blue/`,
`twins_grey/`, `twins_blue/`, `repaint_compare.png`, and the three pinned prompt files.
