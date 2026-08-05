# E10 — the sea-occlusion composite: report

**Executor session, 2026-08-05.** Written after the work, against
[predictions written before it](E10-w3-sea-predictions.md). Dispatched by
[Ruling 10](E10-ruling.md).

Tool: [`tools/e10_sea_composite.py`](../../tools/e10_sea_composite.py) · artifacts in
`E:\AI\training\facet_next\E04_stroke\e10_layer\sea\` · record `sea_composite.json`.

**Zero generation. Zero credits. Zero GPU.** No base-asset file was opened for writing; the
beam renders were **reused**, not re-rendered, and P1 records which atlas they came from.

---

## The run

```
[line] waterline_z = -0.43095 (profiles/ship.json, canonical mesh frame)
[rec ] Step 0.2 recorded placed_line_row 896.0021 | rendered beam band 22106 px
[A3] base sha256 before: 65b4c6a3d5fb8df1
[P1 ] toggle/off/atlas.png vs the accepted asset: PIXEL-IDENTICAL (0 px differ)
[A2 ] camera elevation 0.0 - the row-split predicate is exact here
[A1 ] line_row 896.0021 vs Step 0.2's recorded 896.0021 -> delta 0.00e+00 px
[row ] first underwater row 897 (last dry row 896)
[P4 ] silhouette below the line 21821 px vs Step 0.2's rendered band 22106 px (-285, -1.29%)
[sea] G11 blue on the ratified pair: 19407 px | median L* 24.3  C* 34.0  h 286.9 deg
      -> fill rgb(34,56,107)   (a DEMO CHOICE, derived from the fixture)
[sea ] the water hides 21821 px of hull (7.43% of the figure)
[A3 ] base sha256 after:  65b4c6a3d5fb8df1  UNCHANGED
```

| anchor | verdict |
|---|---|
| **A1 — the row** | **PASS.** `line_row` from this render's own `cam.json` equals Step 0.2's recorded row to **0.00e+00 px** — exact in double precision, two tools, two sessions |
| **A2 — elevation** | **PASS.** Camera el 0.0, so the row-split predicate is exact rather than approximate |
| **A3 — the base** | **PASS.** `galleon_final.png` sha256 `65b4c6a3…c492` before **and** after |
| **A4 — chroma** | **PASS.** C\* 34.0 against the fixture's own floor of 12.0 |

---

## Predictions, scored

| # | predicted | measured | verdict | blind? |
|---|---|---|---|---|
| P1 | `toggle/off/atlas.png` pixel-identical to the accepted asset | 0 px differ | **CONFIRMED** | yes |
| P2 | row agrees to < 0.01 px | **0.0000 px** | **CONFIRMED** | **no** — disclosed in the spec |
| P3 | G11 blue median L\* in **[25, 50]** | **24.3** | ❌ **WRONG** | yes |
| P4 | below-line extent within ±5% of 22,106 px | 21,821 (**−285, −1.29%**) | **CONFIRMED** | yes |
| P5 | base sha256 unchanged both ends | unchanged | **CONFIRMED** | yes |

**P3 is a miss and nothing was changed because of it.** I predicted the ship's declared
sea-blue would sit at L\* ≥ 25 and it measures **24.3** — a darker blue than I guessed, by
0.7 of a lightness point. The fill used the **measured** value, not a corrected one; had I
adjusted the colour after seeing it, the derivation would have stopped being a derivation.
The miss is small and it is still a miss.

### A cross-check that landed for free

The water hides **21,821 px = 7.43% of the figure**. `ship.json`'s own `waterline.z.why`
records candidate C as landing *"7.43% of the beam figure below it"* — a number derived in
**E10 Step 0.1, by a different tool, in a different session, from mesh z-fractions rather
than from rendered pixels.** It reproduces here to the digit. That is a **third**
independent confirmation of the placed line, alongside A1's arithmetic and Step 0.2's
raycast band.

---

## What the composite is, and why it is a projection rather than a drawing

**The sea is the opaque half-space `z ≤ waterline_z`, not a zero-thickness surface.** The
distinction is load-bearing and was derived before the tool was written:

Under orthographic projection with a **horizontal** view direction, a zero-thickness
horizontal plane is edge-on — every ray runs parallel to it and never intersects it. **A
rendered infinite water *surface* would occlude nothing at all at the beam camera.** The
half-space has no such degeneracy: a ray at height `z` is inside the water body for every
`z` below the line, so the water's image is exactly the rows below the projected line.

At elevation 0 the up-axis is +Z exactly, so the row is a function of world `z` alone:

```
image row > line_row   ⟺   world z < waterline_z          (exact, elevation 0 only)
```

That equivalence is the whole instrument. **A2 enforces its precondition rather than
trusting it** — and it is the reason the deck views got no sea composite: at elevation 40 a
horizontal plane's image is not a row boundary, so the exact predicate does not exist there.
It *is* expressible as a per-ray depth test against the plane. That is a different
instrument; it is named here and built nowhere.

---

## Measurements of the artifact

| quantity | value |
|---|---|
| first underwater row / last dry row | **897 / 896** |
| sea extent in frame | rows 897–1023 = 127 of 1024 rows (**12.4%** of frame height) |
| hull hidden by the water | **21,821 px**, 7.43% of the 293,865 px figure |
| figure column span | x 91–980 (890 columns) |
| columns whose geometry **reaches** the line | **569 (63.9%)**, contiguous x 333–901 |
| columns that do not | 321, in **two runs**: bow x 91–332 (242) and stern x 902–980 (79) |
| grey gap in those columns | median **145 px**, max **395 px** |
| sea fill | **rgb(34,56,107)** — 19,407 px measured on the ratified pair, median L\* 24.3 / C\* 34.0 / h 286.9° |
| background above the line | flat grey **rgb(107,107,107)** — the render's neutral, unchanged |

The hull meets the water **continuously along its whole mid-length** and rides above it at
bow and stern, which is `ship.json`'s own pre-registered note about the flat plane against a
hull with rocker — *"that is how real waterlines sit and it is not a defect."* The two
non-reaching runs are the columns where the figure's only geometry is bowsprit forward and
gallery overhang aft, sitting a median 145 px above the water with flat grey between.

---

## The finding: 94% of the W2d coat is underwater

Measured on the same beam frame, layer-off against layer-on:

| | px | share |
|---|---|---|
| coat visible on the **dry** render | 9,912 (rows 894–934) | — |
| of it, **above** the line | 567 | **5.72%** |
| of it, **below** the line — hidden by the water | **9,345** | **94.28%** |
| coat visible on the **floating** composite | **567**, rows 894–896 | a 3-row sliver at the line |

**This is structural, not incidental.** The contact mask is *defined* as texels whose
surface sits at `z ≤ waterline_z`, and the coat was painted inside it — so a band confined
to the contact mask is below the water by construction the moment water exists. At full
size the two floating panels are indistinguishable; the sliver reads only at 3×.

**The question this raises is the advisor's, and I am not answering it:** a boot-top on a
real hull *straddles* the waterline — that is what makes it visible when the ship rides
light — while the contact mask stops **at** the line. Whether E10's band should be the
contact mask, or the contact mask grown upward by some hull-derived amount, is a
specification question with a measurable answer, and it is not this session's to decide.

---

## What is NOT established

- **Whether the composite reads as a floating ship.** That is the Director's, through the
  advisor's eye first (Ruling 10, ledger forty-three). Nothing here grades it.
- **Whether flat grey above the line is right.** The background is the render's neutral, not
  a sky or horizon, so the composite is two flat fields with the ship between them. Reported
  as a property; not judged, and not "fixed" — adding a sky would be exactly the taste this
  method excludes.
- **Anything about the deck views.** No sea composite exists at elevation 40 and A2 is why.
- **Whether G11's frieze blue is the right water colour.** It is a **demo choice**, derived
  so no taste entered, recorded as a choice and not as canon. Ruling 10 assigned the water's
  material to the scene.
- **The 1.29% P4 gap's composition.** It is inside the pre-registered band and its three
  candidate causes (the 2,487 off-surface texels the mask excludes, rasterization gaps in
  the rendered mask, the >127 threshold) were named in advance and **not** decomposed here.

## Environment note

The rig's **VRAM watchdog was dead for this session** (heartbeat died 19:36:15, the loop
crashed on a file lock over `_watchdog_HEARTBEAT`). It did not matter here — this task ran
entirely on CPU through numpy and PIL, reused renders rather than raycasting, and touched no
model — but any GPU work this session starts unprotected.

---

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | `waterline_z`, the recorded row, the base hash, the chroma floor and the blue band all read from their files and echoed with sources; the row formula reused from `e10_contact_mask.py:233` rather than retyped; the reused renders identified by the atlas they came from |
| ANDON_AUTHORITY | 3 | four anchors, each with a describable non-zero, all inside the tool; A2 guards a *precondition* the composite's exactness depends on, which is the direction the arithmetic cannot bound |
| NAMED_COMPENSATORS | 3 | writes confined to `e10_layer/sea/`; undo is deleting that directory; the base asset opened read-only and hashed both ends |
| DECOMPOSE_BY_SECRETS | 3 | line in the profile, predicate in the tool, colour in the fixture and labelled a demo choice — three owners, none crossing |
| UNCERTAINTY_GATED_HUMANS | 3 | the session halts here; the sheet reaches the advisor's eye before the Director's; the coat question is stated as a question with no recommendation |
| EXTERNAL_VERIFIER | 3 | the row confirmed three ways — this arithmetic, Step 0.2's raycast band, and Step 0.1's independent 7.43% — the last two from different tools in different sessions |
