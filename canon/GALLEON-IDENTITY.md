# GALLEON — identity specification (test fixture)

**Status:** authored by the advisor, 2026-08-04, on the Director's designation of candidate
**00006** ("they look great" → 00006 picked at the Gate 0 designation gate). **This is a test
fixture, not a shipping asset.** Its purpose is a fixed identity target so that "did the
element land" has a ground truth on the route's first non-character subject. Any line here is
the Director's to overrule in a sentence; none of it needs his ratification to proceed.

Form is read off `galleon_clay_p1_00006_.png` and the designated mesh
(`galleon_00006_raw.glb`). **There is no styled visual target yet** — unlike W3, this spec is
authored *forward*: the styled target pair will be generated FROM it, which is the
architecture running in its honest direction (identity enters through the prompt, or it is
arriving by accident).

---

## Form — the grammar rules, inherited as measured

**Every element is its own noun phrase** (E08 Amendment 13: head noun + minimal modifier
lands; stacked compound modifiers drop). **A specification determines what occupies a
surface and cannot add a second element to an occupied surface** (Amendment 15) — elements
below paint surfaces that exist as geometry on the designated mesh; nothing is an addition
onto an occupied surface, and any future edit that becomes one is predicted to drop.

## NAMED — must appear in the prompt, or it leaves

| # | element | note |
|---|---|---|
| G1 | a gilded lion figurehead | gold — the LoRA's proven material on W3 |
| G2 | warm oak-brown hull planking | the dominant hull material |
| G3 | black tarred strakes along the hull | the horizontal wale bands |
| G4 | weathered tan canvas sails | **deliberately warm-toned, not white** — see stressor S1 |
| G5 | gilded scrollwork on the stern castle | carved relief is its own surface (the knee-plate precedent) |
| G6 | a gilded spire on the stern turret | **⚠ AMENDED by the Director, 2026-08-04** ("I love the gold. I approve") — authored as *verdigris copper*; the styled pair arrived gold and he kept it. The spire joins the gold family (G1/G5/G12). The 4d landing table records the history: verdigris asked, gold arrived, Director ruled. |
| G7 | red gun port lids | **⚠ AMENDED to the head-noun form, 2026-08-04** (Ruling 9's grammar, ruled before Arm G7 ran; the twins take this form under both pre-registered branches, and the fixture must match the prompt). History: authored `red-lined` — the only sub-feature modifier of twelve — missed on the pair (no red above the chroma floor, Ruling 8). One byte-matched generation with the head-noun form put red on 3–4 lids (h 66–70 → 41–45, C\* rising, ΔE 16.5–27.3 against a ship median of 0.87) — a real localised **response, not a landing**; the pair-derived floor was withdrawn in Ruling 13 as unreachable by an element this size, and the landing verdict moves to the twins' table. The Director's window on the colour stays open; default is red as authored. |
| G8 | black iron cannon barrels | run out of the ports, per the clay |
| G9 | dark tarred rigging and ratlines | the thin-structure stressor, named so it is not accidental |
| G10 | pale scrubbed deck planking | lighter than G2, still warm |
| G11 | a deep sea-blue frieze band along the bulwarks | **blue is IN-palette on this subject** — W3's off-palette detector colour is a declared material here, which is the palette-as-subject-data principle made concrete |
| G12 | gilded stern-gallery railings | gold again; gold is the binding element across the scheme |
| G13 | gilded masthead finials | **⚠ ADDED post-acceptance, 2026-08-05** (Ruling 28, under the Director's delegation at Gate 1 — "it looks good to me"). Never authored: the twins painted gold at all three mastheads unprompted, first observed on the 1064 frame-discovery batch, flagged through Rulings 17 and 27 as in-spec-material-wrong-place with the Director's window open, and accepted with the asset. Named because an element not named in the prompt is arriving by accident and will leave the same way — naming it is what makes it stay. Joins the gold family (G1/G5/G6/G12). |

## MESH-SUPPLIED — arrives through the control from geometry; record the dependency

| element | note |
|---|---|
| the hull form, sheer and beak-head | the mesh's body is the ship's body |
| three masts, their yards, and the bowsprit | count and rake are geometry |
| the set of the sails | furled/spread state is modelled, not prompted |
| the gun-port count and placement | geometry; G7/G8 colour them, nothing adds or removes one |
| the silhouette itself | the twins' only job is to register to it |

## STYLE-SUPPLIED — arrives from the LoRA; record so a model change is noticed

| element | note |
|---|---|
| painterly worked surface, visible brushstrokes | same source as W3; not yet separated from prompt terms |

## Pre-registered stressors — named before any generation exists

- **S1 — ⚠ CORRECTED IN PLACE (E04 fixture check, 2026-08-04).** As authored this read
  *"pale canvas is the same physics [as the blade] at sail scale"* and claimed G4's tan was
  chosen *"partly for this reason."* **Measured, the physics is inverted:** the key fails at
  the **backdrop's own value**, not at paleness — the blade's failing pixels measure
  rgb(111,113,115) against a backdrop of rgb(114,114,115), and against that mid-grey,
  **white canvas is the furthest candidate of all** (residual 0.5343, 8.9× the 0.06 cut)
  while tan is nearer the danger at 0.3931. Both clear enormously; sail colour is not a
  keying risk in either direction. **G4 stays weathered tan** on its surviving grounds —
  it reads as sailcloth and sits in the style's warm register — a choice with one wrong
  reason and its good ones intact. The advisor conflated two instruments' failure physics:
  the keying's value-distance and the palette gate's chroma floor. Corrected with the
  measurement, per the house rule.
- **S2 — the rigging is the thin-policy stressor, and it is also S1's real heir.** 512
  shells, most of them filaments — and thin structure keys out **4.2–6.8× more often**
  than bulk (≤2 px half-width: 5.68–10.77% against bulk's 1.35–1.58%) because a 1–2 px
  line antialiases toward the backdrop whatever its named colour. **S1 and S2 are one
  failure on this subject, and its element is G9, not G4.** `ship.json`'s `thin_extent`
  is suspended until measured on this mesh.
- **S-backdrop — the twins' backdrop is fixture data and it is the main lever.** The
  backdrop is *prompted*, not rendered — one word — and it is the only free operand in the
  key's `|pixel − backdrop|`. W3's inherited "plain grey background" is **struck as a
  default**; the galleon's backdrop is derived in the E04 dispatch to maximise the minimum
  distance from every declared material above, weighted toward the thin elements' colour
  (G9 is dark, which favours a pale backdrop). The derivation and chosen value are recorded
  there with the G9 enrichment numbers as the baseline they must beat.
- **S3 — nobody knows a galleon's palette by eye.** That is the reason the off-palette gate
  exists (E08 Amendments 23–25) and the reason this table is the gate's source. **Numeric
  bands are NOT declared here** — they derive from these named materials and cross-check
  against the styled target pair once it exists, never against the twins they will gate
  (the non-circularity rule, kept).

## What this fixture is for

1. **Does the route generalise?** Every value the character path needed now comes from
   `profiles/ship.json` or from this fixture; a change required *outside* those two files is
   the finding (profiles-design.md).
2. **Does identity still ride in the prompt on a subject with no face?** G1–G12 against
   contradiction, if E04 needs the test; the W3 result (8/8 at 7.4×) is the prediction.
3. **Does the palette gate carry the judgment the eye cannot?** S3 is the point of the
   whole subject.

The Director's gate is on **pipeline outcomes** — whether the mechanism works on a ship and
whether the finished asset is good. Not on which colours a test galleon wears.
