# E04 Task 4a + 4b — the ship's measured values and its derived backdrop

**Executor session, 2026-08-04.** Local only, no GPU, no generation. 4b's predictions were
hashed and committed before the derivation ran
([E04-task4b-predictions.md](E04-task4b-predictions.md), SHA256 `3E630442…ED30`).

**Three of five 4b predictions are falsified**, and the answer is simpler than any of them.
**One 4a approach is falsified outright** and reported as such.

---

## 4a — the suspended values, measured from `galleon_00006_raw.glb`

### Framing — and a prediction of mine the measurement corrected

The rotating silhouette's **widest projected width is 0.9987, at yaw 0**, against a height of
0.9598 → **aspect 1.0405, frame 1066 × 1024**.

I built the sweep expecting the bounding box to *understate* the widest view — a box seen at
45° presents its diagonal, which for this bbox would be 1.068. **It does not: the
understatement is 0.00%.** The hull tapers at bow and stern, so the diagonal never
materialises and broadside is genuinely the widest view. The measurement was written because
I thought the box was wrong; it was right, and only measuring showed that.

### Orientation

| end | verts in the outermost slice | beam | reading |
|---|---|---|---|
| **−x** | 2,308 | 0.103 | thin low protrusion → **the bowsprit. Bow.** |
| **+x** | 12,748 | 0.170 | bulky, taller → **the stern castle. Stern.** |

Confirmed by eye: at yaw 0 the spired turret sits image-right, and +x maps to image-right
(right = look × up₀ = +x at yaw 0). So **view 0 = port broadside, view 2 = stern-on, view 6 =
bow-on**, and `--yaw-offset` stays **0.0** — the broadside is a ship's maximum-information
view and rotating buys nothing measurable. Had it needed rotating, the *camera* rotates:
`to_mesh()` destroys authored vertex normals.

### Camera set — measured as unions, which changed the answer

My first pass scored each elevation independently. That answers *"what does one elevation
see"*, a question nobody asked — **a camera set is a union**, and a camera added to a set that
already sees a surface buys nothing. Rescored properly:

| set | cams | deck area seen | gain vs eye8 |
|---|---|---|---|
| eye8 only | 8 | **30.17%** | — |
| eye8 + **pair @ 40 (0/180)** | 10 | **49.58%** | **+19.41** |
| eye8 + character pair @ 55 | 10 | 49.15% | +18.98 |
| eye8 + pair @ 30 | 10 | 49.21% | +19.04 |
| eye8 + **beam** pair @ 40 (90/270) | 10 | 41.93% | +11.76 |
| eye8 + quad @ 40 | 12 | 53.21% | +23.04 |
| eye8 + single top-down (0 @ 90) | 9 | 42.97% | +12.79 |

Three findings:

1. **Eye level reaches only 30% of the decks.** The design note's *"decks need looking into"*
   is now a number, and it is a big one — the elevated pair is worth **+19.41 points** here
   against the crown-and-boot-tops it bought on a character.
2. **Bow/stern beats beam, decisively: 49.58% against 41.93%.** Looking *along* the ship's
   length sees down the decks; looking across the beam is blocked by hull sides and sails.
   Nothing in the character line predicted this — it is a fact about ships.
3. **Elevation is nearly free between 30° and 55°** (49.21 / 49.58 / 49.15 — a 0.43-point
   spread). **40° is adopted as the measured peak rather than by inheriting 55.** The
   character's 55 is not *wrong* here; it is simply not derived.

**A ceiling worth knowing:** deck coverage plateaus near **53% even at twelve cameras**. Half
of this subject's upward-facing surface is unreachable from any exterior camera — it sits
under sails, yards and tops. Dilation and the brush will serve a large share of the deck
however the set is chosen.

### `thin_extent` — one approach falsified, then the character's own method

**FALSIFIED: shell topology does not identify the rigging.** The mesh has 512 shells with
92.85% of faces in the largest, so I used small-shell membership as an *independent*
(non-circular) criterion for "filament". Measured, the 509 small shells have **median extent
0.10975** — chunky interior pieces, not filaments — while the thin population lives in the
**main** shell (p10 = 0.0032). The rigging is attached to the masts and is therefore
topologically part of the hull. Reported rather than quietly dropped; the criterion was
sound in principle and wrong in fact.

**No antimode either.** The density has its thin peak at **0.0015–0.0045**, falls steeply
through 0.0060, and reaches a **plateau** at 0.0090–0.0165 before a secondary bump. My
detector reported an "antimode at 0.0090"; looking at the bins, the dip is ~7% against its
neighbours — **that is the top of a shoulder, not a valley.** This repo has paid once for
reading a shoulder as a gap, and the honest statement is that no cut is *discovered* here.

So the value comes from **the method the character's 0.030 actually came from** — the
smallest value that fills the thin structure solid, judged on the artifact — with three
independent lines agreeing:

| line | reading |
|---|---|
| density peak 0.0015–0.0045 | at this render scale that is **1.3–4 px**, matching rigging diameters |
| rendered thin-masks | **0.005 leaves the rigging patchy; 0.010 is solid** — a rope crossing the ray obliquely presents more extent than its diameter |
| cross-view cost | **10.20%** of visible area withheld on *every* view at 0.010, against **15.25%** at the character's 0.030 |

**`thin_extent = 0.010`**, and the cost curve is published below so it can be moved:

| threshold | 0.004 | 0.005 | 0.006 | 0.008 | **0.010** | 0.015 | 0.020 | **0.030** |
|---|---|---|---|---|---|---|---|---|
| area withheld on **every** view | 5.18% | 7.05% | 8.05% | 9.35% | **10.20%** | 11.71% | 12.89% | **15.25%** |

**Why the character value is visibly wrong here, in one image:** at 0.020–0.030 the **hull's
entire lower rim goes red** in the thin-mask render. That is a large smooth surface caught
because it is *grazing*, not thin. `thin_extent` measures extent **along the view ray**, so a
flat sail seen edge-on and a hull seen at its silhouette both register as thin. On a
greatsword that conflation never fired; on a ship it is everywhere. **The per-view behaviour
may still be correct** — withholding an edge-on surface from diffusion is arguably right, and
the cross-view table is the honest cost because a sail withheld edge-on is still painted
broadside.

## 4b — the backdrop, derived

The key is `max_channel |pixel − backdrop| > 0.06`; the backdrop is prompted and is the only
free operand. Maximising the minimum distance over all twelve declared materials, weighted
2× toward the four thin ones (G3, G8, G9, G12):

| backdrop | raw min | nearest | **thin min** |
|---|---|---|---|
| **W3's inherited mid grey (106,106,107)** | 0.1725 | G6 verdigris | **0.2588** |
| a lighter plain grey (150,150,150) | 0.1804 | G10 deck | 0.3059 |
| **WHITE (255,255,255)** | **0.4275** | G10 deck | **0.7176** |
| metric optimum, saturated blue (0,0,245) | 0.5294 | G11 blue | 0.7765 |

**Adopted: `plain white background`.** It improves the quantity that killed the blade by
**2.5×** over the inherited grey, and the dark thin elements it is chosen for sit furthest of
all — G3 strakes 0.8902, G9 rigging 0.8510, G8 cannon 0.8275.

The unconstrained optimum is saturated blue, beating white by 8%, and is **disqualified
twice**: the fixture requires avoiding G11's declared sea-blue, and a saturated backdrop
bleeds into a diffusion image.

### Predictions against measurement — three falsified

| # | predicted | measured | |
|---|---|---|---|
| B1 | no neutral can win; best neutral < 0.25 | **white scores 0.3588 weighted / 0.4275 raw** | **FALSIFIED** |
| B2 | the winner will be saturated | raw optimum *is* saturated — by 8%, and disqualified; the practical winner is neutral | **half — correct on the metric, misleading as an implication** |
| B3 | optimum in the green–magenta region | **blue** | **FALSIFIED** |
| B4 | thin-weighting pushes the backdrop paler | **no effect at all** — the *unweighted* neutral optimum is also 255 | **FALSIFIED** |
| B5 | min distance ≥ 0.24 | 0.3588 / 0.4275 | **correct** |

The error in B1/B3/B4 is one error: **I reasoned about the metric instead of about the
materials.** Eleven of the twelve declared elements are dark-to-mid; only canvas and deck
planking are pale. White is therefore far from nearly everything by construction, and no
search was needed to see it. My pre-registered tension — that a metric-optimal backdrop would
be unusably coloured — **dissolved rather than resolved**: the answer is a plain neutral word.

## The finding the profile cannot hold

`turn_render` hardcodes `ortho_scale = size.z * 1.204`. **There is no fit-axis knob**, so
"fit to width" cannot be expressed as a profile value at all — the derived margin 1.2528 for a
1066×1024 frame is recorded in `ship.json` but wired nowhere. My Gate 0 driver worked around
it by choosing the render *resolution* so the width fits, which is equivalent and needs no
code change, but the coupling is accidental: `ortho_scale` is computed from `size.z` and
applied to the horizontal axis whenever the frame is landscape.

This is exactly what `profiles-design.md` said to watch for: **a change required outside the
profile is the signal that something in the shared code was never a principle.** Height-fit
is a character assumption baked into a shared tool. Recorded, not fixed — changing it is a
behaviour change on the accepted path and not mine to make unbidden.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | 4b's predictions hashed and committed before the derivation ran; the material table is a versioned file, not literals; every camera, threshold and ray count is an argument |
| ANDON_AUTHORITY | **3** | No threshold emitted where the data does not support one: the "antimode" is reported as a shoulder and the value rests on a stated visual method with its cost curve published |
| NAMED_COMPENSATORS | **3** | New files only; `ship.json` rewritten with git as undo; nothing pre-existing touched; no spend |
| DECOMPOSE_BY_SECRETS | **3** | Every value derived from this subject or its fixture; the one quantity that could not live in the profile is named as the finding rather than forced in |
| UNCERTAINTY_GATED_HUMANS | **3** | The thin threshold is argued from a rendered artifact with its cost curve; the backdrop reports the rejected optimum and why; the weakest link (estimated material colours) is named in the profile itself |
| EXTERNAL_VERIFIER | **2** | The shell-topology criterion was built to be independent of thickness and falsified itself; the union rescoring overturned my own per-elevation table. No second model — `skip:` per the dispatch |

---

**4a and 4b complete. 4c (the styled target pair, on cloud) is next and has not been
started** — no generation has run, no credits estimated, no workflow submitted.
