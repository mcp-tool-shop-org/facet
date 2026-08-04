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
| G6 | a verdigris copper spire on the stern turret | the distinctive spired turret; verdigris is chroma the gate can hold |
| G7 | red-lined gun port lids | the red band of the palette |
| G8 | black iron cannon barrels | run out of the ports, per the clay |
| G9 | dark tarred rigging and ratlines | the thin-structure stressor, named so it is not accidental |
| G10 | pale scrubbed deck planking | lighter than G2, still warm |
| G11 | a deep sea-blue frieze band along the bulwarks | **blue is IN-palette on this subject** — W3's off-palette detector colour is a declared material here, which is the palette-as-subject-data principle made concrete |
| G12 | gilded stern-gallery railings | gold again; gold is the binding element across the scheme |

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

- **S1 — canvas is the blade problem at sail scale.** W3's steel keyed out against the grey
  studio backdrop at C\* 1.6–2.8 (§9a); pale canvas is the same physics across a vastly
  larger area. G4 is authored *warm tan* partly for this reason — an authoring choice, made
  in canon where it belongs, not a threshold tuned later. Whether it is sufficient is E04's
  to measure, and the backdrop question stays open in the E04 spec.
- **S2 — the rigging is the thin-policy stressor.** 512 shells, most of them filaments.
  `ship.json`'s `thin_extent` is suspended until measured on this mesh.
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
