# E35 R2-a — executor blind bands

**Registered 2026-08-14, after the Gate R2 mechanism ruling and before the R2-a run.**

## ⚠ Blindness limit, declared rather than claimed

**I am NOT blind to per-seed pale AREA.** Leg 6c already printed it per view per seed, and
that table is in my context. Summing it is arithmetic on a number I have seen, so any
"prediction" about which seed is palest by area would be a recitation. Declared here so the
band below cannot be read as a blind hit.

**I am also not blind to one enumeration fact:** the ruling asks for "E34's 8 accepted twins
as the baseline anchor." Those files **are** the 770700 column of leg 6c — E34's accepted set
is seed 770700 on every view (views 0 and 4 are E33's r3 twins, reused byte-for-byte). The
anchor is not a second population; it is the same object under another name, and R2-a will
say so rather than present it as an independent measurement.

**I am blind to:** L\*-rise per seed (never computed — 6d measured it only on the assembled
render, pooled across views), the anticorrelation between the dark-speck census and the pale
measure, and whether the census-selected twin was the pale-maximal twin per view.

## The bands

**PALE MEASURE, defined before use:** the leg-6 definition unchanged — connected components
of figure pixels whose L\* exceeds a 31 px local median by ≥ 6.0, area ≥ 25 px², head region
rows 60–220. Two numbers per (view, seed): **area px²** and **L\*-rise** = median L\* inside
pale minus median L\* of the rest of the figure.

- **PR1 — L\* rise ranks with area.** Mean L\*-rise orders **987654 > 770701 > 770700**, the
  same order as area. *(Falsifier: any other ordering — which would mean the two pale
  measures disagree and the ruling's "palest seed" needs saying in one unit only.)*
- **PR2 — the gap is modest in L\*.** The spread in mean L\*-rise between the palest and
  darkest seed lands **2.0–7.0 L\***. *(A wash the Director called "much stronger than E34's"
  should be visible but is not a 20-point shift; if it exceeds 7.0 the class is bigger than
  I have been treating it as.)*
- **PR3 — anticorrelation is real but loose.** Across the 24 (view, seed) twins, Spearman ρ
  between dark-speck census area and pale area lands in **−0.75 … −0.25**. *(Falsifier
  either way: ρ > −0.15 means the ruling's anticorrelation is not carried by these 24
  points; ρ < −0.85 means it is near-deterministic and selection was almost purely a pale
  knob.)*
- **PR4 — the selected twin was pale-maximal on a MINORITY of views: 2–4 of 8.** The
  selection rule minimised dark-speck area, and the anticorrelation is loose (PR3), so it
  should have landed on the palest candidate often but not usually. *(This is the clause I
  expect to be most informative: if it comes back 7–8 of 8 the selection was effectively a
  pale-maximiser; if 0–1 the ruling's mechanism does not run through my selection rule at
  all.)*
- **PR5 — E34's anchor is the mildest column on both measures**, consistent with the ruling's
  eye and with 770700 being the recommended global seed.
