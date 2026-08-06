# DRAGON — identity specification (test fixture)

**Status:** authored by the advisor, 2026-08-05, on the Director's designation of candidate
**00003** ("3 is the winner, but they all look great" — E12 Ruling 1). **This is a test
fixture, not a shipping asset.** Its purpose is a fixed identity target so that "did the
element land" has a ground truth on the route's first beast. Any line here is the
Director's to overrule in a sentence; none of it needs his ratification to proceed.

Form is read off `dragon_clay_p1_00003_.png` and the designated mesh
(`dragon_00003_raw.glb`, 986,825 faces, 9 shells, Gate 0 frame 1792×1024). **There is no
styled visual target yet** — this spec is authored *forward*, the galleon's proven
direction: the styled target pair will be generated FROM it, and identity enters through
the prompt or it is arriving by accident.

---

## Form — the grammar rules, inherited as measured

**Every element is its own noun phrase** (E08 Amendment 13: head noun + minimal modifier
lands; stacked compound modifiers drop). **A specification determines what occupies a
surface and cannot add a second element to an occupied surface** (Amendment 15) — every
element below paints a surface that exists as geometry on the designated mesh, each
surface is owned by exactly one element, and **any future edit that decorates an occupied
surface (gold banding on a horn, markings on a membrane) is predicted to drop; to change
such a surface, replace its owner on a named region instead.**

## NAMED — must appear in the prompt, or it leaves

| # | element | note |
|---|---|---|
| D1 | deep moss-green scaled hide | the dominant material: back, flanks, neck top, limbs, tail top, and the wing arms and fingers. Sits in the style's proven green register (W3's tunic band) — the LoRA has painted this family before |
| D2 | pale bone-tan ventral plates | the banded underside: throat rings, chest plates, belly, tail underside. The stepped throat column (S-occlusion) is D2 surface |
| D3 | storm-grey wing membranes | the sheet fields between the wing fingers, vein relief included. Deliberately cool and neutral against the warm hide — and deliberately NOT the studio-grey of a clay backdrop; the backdrop derivation (S-backdrop) must hold this element furthest of the large surfaces |
| D4 | bone-ivory curved horns | the paired back-swept horns. Ivory is this scheme's binding family, as gold was the galleon's |
| D5 | bone-ivory crown and cheek spikes | the frill ring around skull and jaw; its spikes are individually modelled (no satellite shells on this mesh — Gate 0 §4) |
| D6 | bone-ivory dorsal and tail spines | the ridge from shoulders to tail tip, paired blade rows at the tail |
| D7 | bone-ivory claws | feet and the wing-claw spur at each wing's wrist |
| D8 | ember-orange eyes | **pre-registered as below any area floor** (the G7 lesson: a pair-derived floor was unreachable by an element this size and was withdrawn). Landing verdict belongs to the twins' table, judged by eye at the head crop; no numeric gate may be armed on this element |
| D9 | a dark wine-red tongue | the studio's wine-red register (W3's skirt); small element, same floor caveat as D8 |
| D10 | pale ivory fangs and tooth rows | the free-standing fang shells are geometry (Gate 0 §4 located every satellite on them); this element colours them |
| D11 | a dark slate mouth interior | the open cavity behind the teeth |

## MESH-SUPPLIED — arrives through the control from geometry; record the dependency

| element | note |
|---|---|
| the body form, stance and silhouette | symmetric wings-spread quadruped — the MESH's stance, not the concept's (Gate 0 §6: no reconstruction preserved its concept's pose); the twins' only job is to register to it |
| both wing membranes, their finger struts and scalloped trailing rims | closed slabs, not open sheets (0/1 boundary edges, zero length); the folded-side field carries the 7,138-edge pinch region — S-membrane |
| horn, spike, spine and claw count and placement | geometry; D4–D7 colour them, nothing adds or removes one |
| the open jaw, tooth rows and tongue | modelled open with free-standing fangs |
| the scale relief | reconstructs as geometry, legible under `--clay` with no texture (Gate 0 §6) |
| the throat/shoulder crevice and stepped throat bands | designated-in (Ruling 1); paint will render it as a dark seam, and no texture pass can restore geometry it does not have |

## STYLE-SUPPLIED — arrives from the LoRA; record so a model change is noticed

| element | note |
|---|---|
| painterly worked surface, visible brushstrokes | same source as W3 and the galleon; not yet separated from prompt terms |

## Pre-registered stressors — named before any generation exists, evidence status labeled

- **S-membrane** *(measured: E07 at sash scale + Gate 0 on this mesh)* — the new stressor
  class this subject exists to test. Large thin SHEETS: closed slabs 1–2 px at render
  scale (~0.1–0.25% of height; whether that is thickness or shading is not decidable from
  a render — Gate 0 §6). E07 measured opposing faces of a sheet thinner than its own
  tessellation as the *closest* back-facing sources; expect that physics across the whole
  membrane field, worst where the designated mesh pinches (the 7,138-edge folded-side
  field). **Owner seams are expected on the membrane fields** — large smooth surfaces
  under `argmax(facing)`, the E04 Ruling 1 class; the owner channel is native and the
  sheet carries the column. `thin_extent` is per-mesh, the ship's 0.01 is
  filament-derived, and a membrane is not a filament: **measure fresh, publish the cost
  curve, and report what fraction of the membrane the thin mask withholds** — a value
  tuned on rigging could withhold a third of this subject.
- **S-filament** *(inferred from the ship, unmeasured here)* — horns, spikes, spines,
  claws are filament-adjacent; A3's cap (0.0% thin-strata erosion) is the prior. The
  fang shells are the smallest: satellite shells of 4–180 faces that must not be lost by
  any weld, decimate or cull step — pre-registered as a check wherever those run.
- **S-scale-relief** *(unread guess, labeled as one)* — high-frequency overlapping plates
  may interact with the LoRA's register; the styled pair is the first evidence either way.
- **S-occlusion** *(measured at Gate 0, designated-in)* — the throat/shoulder crevice and
  the hard-stepped throat bands. Paint cannot fix it; pre-registered so the first person
  to see a dark seam there at a gate reads it as the known geometry, not a new texture
  defect. If it ever matters at the Director's zoom, the fix is geometry-side and is its
  own arm.
- **S-backdrop** *(suspended — derivation owned by the measurement dispatch)* — the
  twins' backdrop is prompted, one word, the only free operand in the key's
  `|pixel − backdrop|`. Derive it to maximise the minimum distance from every declared
  material above, weighted toward D3 (the largest near-neutral surface) and the dark
  elements (D9, D11) — the galleon's method, its metric-optimum-rejection rule included
  (a saturated backdrop bleeds into a diffusion image). W3's grey and the galleon's white
  are both candidates, neither inherited.
- **S3, kept from the galleon** *(principle, proven there)* — nobody's eye knows what
  this dragon's palette "should" be, because it is authored here. The off-palette gate's
  bands derive from these named materials and cross-check against the styled target pair
  once it exists — **never against the twins they will gate** (non-circularity, kept).
  Numeric bands are NOT declared in this file.

## What this fixture is for

1. **Does the route hold its third subject class?** Character, ship, now beast — every
   value the route needs comes from `profiles/beast.json` or this fixture; a change
   required *outside* those two files is the finding (profiles-design.md).
2. **Do membranes survive the acceptance chain?** S-membrane is the point of the subject:
   sheets are the one surface class neither prior subject carried at scale.
3. **Does identity ride in the prompt on a subject whose every element is organic?** The
   W3 result (8/8 at 7.4×) and the galleon's twelve-element landing are the prediction;
   the ivory family (D4–D7, D10) is this scheme's gold.

The Director's gate is on **pipeline outcomes** — whether the mechanism works on a beast
and whether the finished asset is good. Not on which colours a test dragon wears.
