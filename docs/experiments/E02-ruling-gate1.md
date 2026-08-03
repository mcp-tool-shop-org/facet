# E02 — advisor ruling at Gate 1

**Date:** 2026-08-04 · **Director's verdict: REJECTED.**
*"Looks like crap. Floating artifacts everywhere. Blade is broken. Hands look bad."*

---

## The question is answered: the texture stage is not sound

E02 existed because every prior texture result was produced on a blob mesh wearing another
silhouette's twins. This run had sound geometry, correctly registered twins, an honest
metric, and a corrected stroke order. **The output was still rejected.**

That is the negative result the spec called a full success, and it is one — the defect is
now isolated from every confound that muddied 2026-08-03.

The Director's three complaints each match a number measured before he looked:

| complaint | measurement |
|---|---|
| floating artifacts everywhere | speckle **2.93%** vs A0's **2.43%** — worse than the already-rejected asset |
| blade is broken | blade saturation **0.477** vs A0's **0.117**; 68.1% of blade above 0.40 |
| hands look bad | thin extremities — lowest twin coverage and highest fill fraction on the model |

## The blade — advisor error, and the cost is now priced

At Gate 0 I deferred the per-view → texel-space union fix for the thin mask, reasoning that
the blade had not been invented at stroke 1. **That was n=1 at a single camera, and the leak
is cumulative.** Across eight strokes:

```
blade texels sampled by the yaw-0 view   10,679
  styled by the twins (stage 1)           1,808  (16.9%)
  styled after all eight strokes          9,385  (87.9%)
  never painted, took dilation fill       1,294  (12.1%)
  atlas saturation: painted 0.451 | filled 0.503
```

Painted and filled texels differ by 0.05 saturation, which kills the dilation hypothesis
outright: **the brush painted the blade, and painted it coloured.** `--thin-extent`
withholds a prop only from cameras where it reads thin; at the flanks it reads thick and was
offered. The deferred fix was the one that would have prevented this.

**Ruled: the texel-space union is no longer deferred.** Thinness is a property of the
surface; compute per view, back-project, union, and withhold in texel space.

## The floating artifacts — mechanism found, and it is structural

Two numbers together explain them:

- **Three in four hole texels are dilated, not painted.** The brush closed 711,183; finalize
  closed 1,901,890.
- **31% of hole texels sit in islands containing no styled texel at all.** Their only colour
  arrives by bleeding across the 4 px gutter into whichever island the packer placed beside
  them.
  > **CORRECTED at E05 Gate 0: the figure is 75.0%, not 31%.** The 31% came from a
  > constrained-fill A/B that was invalid — `bake.margin = 8` against a 4 px gutter means
  > adjacent islands' `valid` regions *overlap*, so an island-constrained fill still leaks,
  > through the bake margin instead of the gutter. It was never island-local. The
  > "constraining it trades artifacts for grey" conclusion below is withdrawn.

**Atlas adjacency is not surface adjacency.** An island holding part of the beard takes
colour from a geometrically unrelated island packed next to it. That is what a floating
artifact is. The executor's A/B confirms the scale: constraining fill to islands changes
**679,489 texels (35.7%)** and sends 590,928 to flat grey — so the gutter crossing is
currently load-bearing, not incidental. Constraining it is not a fix; it trades artifacts
for grey.

## The real finding

**Two twins and eight cameras reach roughly a quarter of the surface with real paint.** The
rest is interpolation across a **35,070-island** atlas whose neighbours are unrelated pieces
of the model. Every symptom the Director named follows from that, and none of them is a
tuning miss.

## Where the next work points — the UV unwrap, not the brush

| mesh | islands | faces per island |
|---|---|---|
| A0 | 8,486 | 34 |
| E02 W3 | 35,070 | 8 |
| a properly unwrapped character | tens | thousands |

`smart_project` produces confetti, and confetti is what makes dilation destructive. With
large, surface-coherent islands: interpolation stays inside a region that belongs together,
coverage per island rises so far fewer islands are colourless, and the gutter stops being
the only source of colour for a third of the surface.

**No parameter changes are proposed on top of this run.** The architecture reaches too little
surface with real paint; tuning the brush cannot repair that.

## Also recorded

- **The third invention persisted and was not negated:** the green tunic runs to mid-thigh
  over the wine-red skirt where the twins have it waist-length. It was absent from the
  negative list. The two that *were* negated — braided belt, shoulder strap — did not recur
  in any of the eight strokes.
- **The stroke reorder worked as predicted.** `y+090` arriving fifth was offered **38,524**
  hole px against **86,084** when the same camera opened the loop.
- **`texpass_finalize`'s docstring is wrong** — it claims the fill is "valid-island-
  constrained"; the code is not. Documented rather than changed, since constraining it is a
  trade, not a correction.
- **Standing constraint from Gate 0, unchanged:** containment, thickness and inside/outside
  queries must run against the welded mesh, never `prep_uv.glb`.
