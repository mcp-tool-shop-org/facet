# E04 stage 1 — HALT on view 0. The background ANDON fired on a character-derived bound.

**Executor session, 2026-08-04, after Ruling 20.** Projection started, profile-driven, all
eight twins. **It halted inside `project_twins` on the first view.** Nothing was written; no
atlas exists.

```
AssertionError: ANDON: 19.06% of newly-admitted texels sit within dE 10 of the twin's
background, over the 2.0% limit — the relaxed acceptance is projecting background onto the mesh.
```

**The bound is W3 data and `ship.json` does not carry it.** `--bg-max-pct 2.0` and `--bg-de
10.0` are absent from the ship's `project_twins` block, so the tool took its own defaults —
**the third instance of Finding B's class** (a flag the tool has, that the profile is silent
about, whose default is the character's number). My own note stands: the purity checker
compares values that are *present* and cannot see values that are *absent*.

---

## What the 19.06% is — measured, not argued

The guard asks *is the relaxed acceptance projecting background onto the mesh*. On this subject
the answer needs one more question, because **the ship declares two pale near-neutral
materials** — G10 pale scrubbed deck planking and G4 weathered tan canvas — and Ruling 8
already banked the pale cluster as the tightest key margin on the asset.

So: of the pixels inside the exact silhouette within ΔE 10 of the realised backdrop
rgb(183,183,183), **where are they?**

| view | near-bg px | % of silhouette | median distance to silhouette edge | share > 20 px from edge |
|---|---|---|---|---|
| 0 | 14,121 | 4.81% | **4.1 px** | 16.9% |
| 1 | 8,945 | 2.75% | 5.0 px | 7.4% |
| 2 | 3,039 | 1.52% | 4.0 px | 0.2% |
| 3 | 10,889 | 3.37% | 4.0 px | 8.9% |
| 4 | 10,939 | 3.72% | 1.4 px | 0.0% |
| 5 | 6,890 | 2.12% | 3.6 px | 16.9% |
| 6 | 2,525 | 1.26% | 2.2 px | 0.0% |
| 7 | 13,294 | 4.12% | 2.0 px | 7.5% |
| **the Director-ratified canon pair** | **10,374** | **3.26%** | **2.0 px** | **0.8%** |

**It is a rim population.** Median 1.4–5.0 px from the silhouette boundary on every view, with
0–17% more than 20 px in. That is the antialiased edge where painted figure meets a light
backdrop — and this subject has an enormous perimeter, because 512 of its shells are rigging.

**And the ship's own ratified canon measures 3.26% by the identical test**, at median 2.0 px,
sitting inside the twins' 1.26–4.81% range. The twins are not anomalous against the artifact
the Director approved.

**This is the perimeter-not-area lesson arriving through a third door.** The bound is a
*fraction of newly-admitted texels*; the quantity it bounds scales with **perimeter**; and this
subject's perimeter-to-area ratio is unlike anything the 2.0% was measured on.

## Not tuned past, and not re-derived

I have not raised the bound, disabled the guard, or added `bg-max-pct` to `ship.json`. The
number would be chosen while looking at the result it judges, which is the one move that is
always wrong — and the honest alternatives are genuinely different (derive per subject from a
clean baseline; normalise by perimeter; gate on the *interior* fraction rather than the total;
or suspend it as the spec suspends the others). That is a ruling.

## What view 0 reported before it stopped — the diagnostics are real and worth keeping

| | |
|---|---|
| atlas | 4096, **valid texels 3,111,817** (the ceiling's denominator, matching) |
| registration, tool's own | IoU(twin, mesh) **0.8287**, centroid dx +0.3 dy +7.7 px — measured against the tool's **dilated sidecar**, which it says so itself; my 0.84420 is against the exact silhouette |
| keyed outside the silhouette | 24,151 px, largest component 1,357 px (8.48% of keyed paint) |
| trust mask | 260,567 of 284,718 raw; fig_w raw 883 → used 881 px |
| edge-dist | min(8.8 px, ⅓ × local half-width); median local cap 19.7 px |
| background probe | 114,949 newly admitted, **median ΔE 31.5** from background; 19.06% within ΔE 10 (already-trusted texels: **0.01%**) |

**A3's cap is doing exactly what it was built to do**, and this is the first ship evidence of it:

| structure half-width | texels | removed by erosion |
|---|---|---|
| 1–2 px | 4,284 | **0.0%** |
| 2–4 px | 12,074 | **0.0%** |
| 4–8 px | 14,698 | 28.1% |
| 8–16 px | 35,423 | 33.4% |
| 16–32 px | 43,207 | 36.2% |
| 32+ px | 150,881 | 10.8% |

The two thinnest strata lose **nothing**. The shipped erosion that A3 replaced annihilated
100% / 100% / 77.6% of the three thinnest strata on the character. On a subject whose declared
stressor **is** its thin structure (S2, element G9), that guard is holding.

Also worth the ruling's eye: the newly-admitted set's **median ΔE from background is 31.5**, and
the already-trusted texels sit at **0.01%** within ΔE 10. The relaxation is not indiscriminate;
the disagreement is entirely about the rim.

## The question

**`bg-max-pct` on this subject.** The A23-style options, none chosen here: derive per subject
from a clean baseline measured before the arm it judges · normalise by perimeter rather than by
admitted-texel count · gate on the interior fraction (the >20 px column above, 0.0–16.9%)
rather than the total · or suspend it as the spec suspends `reg-iou-min` and `bbox-tol`, with
the numbers reported per view.

Whichever way it goes, **`bg-de` and `bg-max-pct` should join `ship.json`'s `project_twins`
block explicitly** — even at the tool's own values — so the next reader sees a decision rather
than a silence.

## What was not done

No atlas, no owner sidecar, no stage-1 share, no hole map. Nothing was written by the
projection. No profile, fixture or tool edit this leg.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The run is one profile-driven invocation; every diagnostic quoted is the tool's own stdout |
| ANDON_AUTHORITY | **3** | An in-tool ANDON fired and was neither raised, disabled nor routed around; the halt is the deliverable |
| NAMED_COMPENSATORS | **3** | Nothing written, nothing spent; no undo needed |
| DECOMPOSE_BY_SECRETS | **3** | The finding *is* the standard: a subject-calibrated bound the profile was silent about, inherited from the character — third instance, and the first to fire |
| UNCERTAINTY_GATED_HUMANS | **3** | Four named options with the measurement that distinguishes them, and no recommendation |
| EXTERNAL_VERIFIER | **2** | The rim-vs-interior test could have gone either way, and the ratified canon pair — an artifact this arm did not produce and cannot influence — was measured by the identical instrument as the control. `skip:` on a second model |
