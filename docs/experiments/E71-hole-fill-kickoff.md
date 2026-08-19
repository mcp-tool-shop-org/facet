# E71 — fill the holes, then look again

**Advisor spec, 2026-08-19. One executor seat. Tree
`E:\AI\training\facet_E71\`. Spend: 0. Local only.**

**Direction (the Director, 2026-08-19): E70 sheet APPROVED.** Identity
holds, garment set is right, none of the five named failure modes
present at his eye. The brush conversation is open. The first sitting
is a **fill**, not a quality stroke.

## What is already paid

- Atlas: `E:\AI\training\facet_E69\bake\atlas_widescope.png` (do not
  mutate in place).
- Prep: `E:\AI\training\facet_E67\prep\`.
- Holes: 1,468 new texels at vest-front, collar, shoulder, hair
  speckle — the withheld set, sitting where E68/E69 measured them.
- Look construction: E70's sheet (twin | mesh, head + collar crops,
  flat light, footer). Reuse that construction so the two sheets
  compare.

## The fill

`texpass_finalize.py --surface-aware` on a **copy** of the E69 state.

`--surface-aware` is E07 L1: every hole takes its nearest painted
texel **in 3D**. Do not use the default atlas-space flood — that walk
was measured to pull colour from another island (E07 Gate 0: 74.9%).
A1 has no blade; this is not thin-extent. It is neighbour colour
across a 0.0423% hole set.

Write `--out` under this tree. Gate C: the E69 atlas bytes on disk
are unchanged at close.

## The look (the thing that can fail)

Same cameras, same crops, same footer as E70:

*the warm rim light in the twins is still paint; the overlay dots are
still the map.*

Sheet: E70 mesh | E71 filled mesh, plus the accepted twin as the
reference column. Head and collar crops required. Rank nothing.

Failure modes this sheet must be able to show: seams, through-
projection, bald crown, cream-as-wall, identity gone, **plus** fill
bleed (a hole taking the wrong neighbour — vest cream, hair backdrop,
collar plum).

## Out of scope

Brush. Cloud. Retuning 2% / dE 10. Re-bake. Binding. A ring regen.

## Prediction

The pale vest-front band and collar speckle will take neighbouring
plum/cream. If they take wall-grey or the wrong garment, that is
bleed and the fill is rejected; the brush still does not open on
those texels.

## Dispatch record

- 2026-08-19 — spec written on the Director's APPROVED of E70. First
  target is the holes. Stroke-one of the brush loop is not this arc.
