# E10 — the sea-occlusion composite: predictions, written before the work

**Executor session, 2026-08-05.** Dispatched by [E10 Ruling 10](E10-ruling.md) — the
Director's verdict on the coat-only toggle was *"How is that supposed to be a waterline?"*,
and Ruling 10's ledger forty-four named why: **a ship reads as floating when the water
*hides* what sits below the line**, and a coat-only toggle leaves the below-water hull fully
visible. This session builds the artifact the float question actually needs.

Nothing is generated. Nothing on the E04 line is touched. No base-asset file is opened for
writing.

---

## The geometry, derived before anything is built

**The sea is modelled as the opaque half-space `z ≤ waterline_z`, not as a zero-thickness
surface.** That distinction decides the whole method, so it is stated first:

Under orthographic projection with a **horizontal** view direction (elevation 0), a
zero-thickness horizontal plane is edge-on — every ray runs parallel to it and never
intersects it. A rendered infinite water *surface* would therefore occlude **nothing** at
the beam camera. The half-space does not have that degeneracy: a ray at height `z` is
inside the water body for every `z < waterline_z`, so the water's image is exactly the set
of rows below the projected line.

And at elevation 0 the row is a function of world `z` **alone** — `e10_contact_mask.py:233`,
reused verbatim rather than re-derived:

```
line_row = (0.5 - (waterline_z - bmid.z) / v_ext) * H - 0.5
```

so **`image row > line_row  ⟺  world z < waterline_z`**, exactly. That equivalence is what
makes the beam composite ortho-exact, and it is **elevation-0 only** — see the scope limit
below.

---

## Predictions

| # | prediction | blind? |
|---|---|---|
| **P1** | `toggle/off/atlas.png` is **pixel-identical (RGB)** to the accepted `out/galleon_final.png`, so reusing the existing beam render is a render of the accepted asset and not of something else | **yes** — not compared |
| **P2** | `line_row` computed from *this render's own* `cam.json` agrees with Step 0.2's recorded `placed_line_row` (896.0021) to **< 0.01 px** | **NO** — disclosed: I read `cam.json` and did this arithmetic by hand before writing this file, and got 896.00 |
| **P3** | G11's sea-blue, measured on the ratified pair inside the declared band (hue 273–301°, C\* ≥ 12.0), has **median L\* between 25 and 50** | **yes** on L\*; the hue range is a property of the selection, not a prediction |
| **P4** | silhouette pixels **strictly below** `line_row` in the beam frame land within **±5%** of Step 0.2's independently-rendered contact band, **22,106 px** | **yes** |
| **P5** | `galleon_final.png` sha256 is `65b4c6a3…c492` before **and after** the run | **yes** on the after-value |

**P4 is the cross-check that can actually fail.** It asks the same question — *how much
hull sits below the line, seen from the beam* — along two paths that share nothing but the
mesh: image-row arithmetic on one side, texel mask → atlas → raycast on the other. The two
are **not** identical by construction (the contact mask excludes 2,487 off-surface texels;
the rendered mask has rasterization gaps; the render is thresholded at >127), so a small
disagreement is expected and **P4 is reported, never gated** — a diagnostic and a gate are
different objects.

---

## Gates

| # | ANDON | what a non-zero would mean |
|---|---|---|
| **A1** | `\|line_row(this cam.json) − 896.0021\| > 0.01 px` → **HALT** | the toggle render is framed differently from the frame Step 0.2 measured in (margin / aspect / state), so the sea would land on the wrong row under an entirely plausible sheet — E10 Ruling 2's failure, one stage later |
| **A2** | `cam.json` elevation ≠ 0.0 → **HALT** | the row-split predicate is exact **only** at elevation 0; at any other elevation a horizontal plane's image is not a row boundary and the composite would be a drawing, not a projection |
| **A3** | `galleon_final.png` sha256 ≠ the recorded anchor, before **or** after → **HALT** | W-H3 violated — the base asset moved |
| **A4** | the derived sea colour's C\* < 12.0 (the palette fixture's own chroma floor) → **HALT and report** | below the floor hue is not a colour, so "sea-blue" would not be a colour claim at all |

Every quantity above is **read from a file, never typed**: `waterline_z` from
`profiles/ship.json`, the recorded row from `e10_contact/contact_mask.json`, the base
sha256 from `e10_layer/layer_state.json`, the chroma floor and the blue band from
`canon/E04-galleon-palette.json`.

---

## The sea colour, and what kind of claim it is

**A demo choice, recorded as one — not canon.** Ruling 10 assigned the water's material to
the scene (RG02 Q3), so nothing here proposes a colour *for the water*. The fill is derived
rather than picked so that no taste enters: it is the median Lab of the pixels on the
**Director-ratified target pair** that fall inside G11's declared blue band — the ship's own
sea-blue, the one blue this subject has ever been measured to carry.

Two properties of that derivation are stated up front. It is **not** a claim that sea water
is this colour. And it is measured on the pair, which is *not* a twin and is not gated by
anything here — the same non-circularity the palette fixture itself keeps.

**No surface treatment is added** — no waves, no gradient, no foam, no transparency. Those
are shader-side per RG02 Q3 and adding them would be exactly the taste this method is built
to exclude. The composite shows the occlusion predicate and nothing else.

---

## Out of scope, pre-registered

- **The deck views (el 40) get no sea composite.** A2 is the reason and it is geometric, not
  budgetary: at elevation 40 a horizontal plane's image is not a row boundary, so the exact
  predicate does not exist there. It *is* expressible as a per-ray depth test against the
  plane, which is a different instrument and is **named here and built nowhere**. The hull
  hiding its own line from 40° is pre-registered three times already.
- Any generation · any write to a base-asset file · rebuilding the boot-top coverage
  (demoted to optional pending the Director's word) · the E04 line · ending a session the
  Director has not ended.

---

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every constant read from its file and echoed with its source; the row formula reused from `e10_contact_mask.py:233` rather than retyped; the reused renders identified by the atlas they were made from (P1) |
| ANDON_AUTHORITY | 3 | four gates, each with a describable non-zero, all inside the tool; A1 and A2 can fire on correct-looking inputs |
| NAMED_COMPENSATORS | 3 | writes only into `e10_layer/sea/`; undo is deleting that directory; the base asset is opened read-only and hashed before and after (A3) |
| DECOMPOSE_BY_SECRETS | 3 | the line is subject data (`ship.json`), the predicate is the tool, the colour is fixture-derived and labelled a demo choice — three owners, no crossing |
| UNCERTAINTY_GATED_HUMANS | 3 | the session halts at the sheet; the advisor looks before the Director does (Ruling 10, ledger forty-three); no grading here |
| EXTERNAL_VERIFIER | 3 | P4 checks the below-line extent along a path that shares only the mesh with the one the composite uses; the row itself is checked against a measurement recorded by a different tool in a different session |
