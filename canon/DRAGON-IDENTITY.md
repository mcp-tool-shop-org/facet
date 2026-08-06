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
| D2 | pale olive-tan ventral plates | the banded underside: throat rings, chest plates, belly, tail underside. The stepped throat column (S-occlusion) is D2 surface. *⚠ Corrected 2026-08-06 (E12 Ruling 12e, the Director's verdict on the re-roll): was "pale bone-tan" — under the ultra-realistic register the word "bone" on the tail's banded underside rendered as exposed skeleton, on both measured seeds* |
| D3 | storm-grey wing membranes | the sheet fields between the wing fingers, vein relief included. Deliberately cool and neutral against the warm hide — and deliberately NOT the studio-grey of a clay backdrop; the backdrop derivation (S-backdrop) must hold this element furthest of the large surfaces |
| D4 | bone-ivory curved horns | the paired back-swept horns. *⚠ The family note is corrected 2026-08-06 (Ruling 12e): ivory was authored as "this scheme's binding family, as gold was the galleon's" — five of eleven elements — and under the realistic register that family mass painted skeleton down the body on both measured seeds. The ivory family is now the HEAD's (D4, D5, D10); the body wears green, olive-tan and charcoal. The galleon's gold survived at that density under the painterly register; the realistic register renders "bone" literally — a register-family interaction the studio's style plan should carry* |
| D5 | bone-ivory crown and cheek spikes | the frill ring around skull and jaw; its spikes are individually modelled (no satellite shells on this mesh — Gate 0 §4) |
| D6 | charcoal dorsal and tail spines | the ridge from shoulders to tail tip, paired blade rows at the tail. *⚠ Corrected 2026-08-06 (Ruling 12e): was "bone-ivory" — a pale segmented ridge running the whole back and tail read as an exposed spine under the realistic register, both seeds* |
| D7 | charcoal claws | feet and the wing-claw spur at each wing's wrist. *⚠ Corrected 2026-08-06 (Ruling 12e): was "bone-ivory" — same correction; dark claws also cut the prompt's pale-bone family mass from five terms to two, both at the head* |
| D8 | ember-orange eyes | **pre-registered as below any area floor** (the G7 lesson: a pair-derived floor was unreachable by an element this size and was withdrawn). Landing verdict belongs to the twins' table, judged by eye at the head crop; no numeric gate may be armed on this element |
| D9 | a dark wine-red tongue | the studio's wine-red register (W3's skirt); small element, same floor caveat as D8 |
| D10 | pale ivory fangs and tooth rows | the free-standing fang shells are geometry; this element colours them. *⚠ Corrected 2026-08-05 (E12 Ruling 4c): an earlier note said Gate 0 §4 "located every satellite on them" — on the designated mesh, **5 of 8 satellites (384 of 396 faces) are the fangs**; three 4-face micro-fragments sit off the wing/shoulder at x −0.237 / +0.096 / +0.102, y ≈ −0.10..−0.12* |
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

## STYLE-SUPPLIED — the subject's REGISTER; a per-subject decision, never an inheritance

*⚠ Rewritten 2026-08-06 (E12 Ruling 10b, on the Director's rejection of the first
styled pair). As authored this section inherited the saltroad painterly register
("painterly worked surface, visible brushstrokes") from the two accepted subjects —
a style decision nobody made for this subject, arriving by inheritance, which is the
accident class the profile system exists to stop, one layer up. The Director's
directive: a dragon reads **ultra-realistic and scary**, and no LoRA is better than
the same texture on everything.*

| element | note |
|---|---|
| **register: ultra-realistic, menacing** | the Director's words made prompt terms; the model's own realistic-creature prior is WANTED here, constrained by our geometry |
| **LoRA: NONE** | ruled 10b; expressed mechanically as `beast.json` `lora-w: 0.0`. A future creature-register LoRA (see [style-registers.md](../docs/style-registers.md)) replaces this line when one exists and earns it |
| sharp scale relief, harsh directional light | realism-register support terms; the pair re-measures whether they carry |

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
  designated mesh carries **eight satellite shells: five are the fangs (384 of 396
  faces — D10's geometry), three are 4-face micro-fragments off the wing/shoulder**
  *(⚠ corrected 2026-08-05, E12 Ruling 4c — an earlier draft called every satellite a
  fang)*. Pre-registered check wherever weld, decimate or cull runs: **report the
  satellite census before and after.** Losing a fang matters and goes to a ruling;
  losing a micro-fragment is reported, not halted.
- **S-scale-relief** *(unread guess, labeled as one)* — high-frequency overlapping plates
  may interact with the LoRA's register; the styled pair is the first evidence either way.
- **S-occlusion** *(measured at Gate 0, designated-in; REALISED on the accepted pair —
  handoff 8 gate validation, E12 Ruling 16)* — the throat/shoulder crevice and
  the hard-stepped throat bands. Paint cannot fix it; pre-registered so the first person
  to see a dark seam there at a gate reads it as the known geometry, not a new texture
  defect. If it ever matters at the Director's zoom, the fix is geometry-side and is its
  own arm. *Realised form, measured: cool marginal-chroma crevice shadow — median hue
  ~234, C\* ~14.4 (just above the gate's 12.0 floor), ~7,300 px in ~121 components
  (largest 1,342) across both accepted views, tracing the throat/shoulder seam, wing-body
  gap, dorsal-ridge and tail-spine bases, and leg creases. It is occlusion shadow that
  happens to carry a hue, not material: no element names it, no band admits it, and the
  gate REPORTS it rather than firing on it (Ruling 16e) — the stressor doing exactly what
  its pre-registration promised.*
- **S-backdrop** *(RESOLVED — derived at handoff 2 Task 3, hue ruled by E12 Ruling
  8a)* — the word is **`plain lavender-grey background`**: low-saturation blue-violet,
  the one hue family no declared material occupies, ruled over a metric-equal
  desaturated green because a green backdrop behind a green-hided animal is what a
  metric is content with and an eye may not be. **Banked from the derivation: W3's
  inherited grey scores 0.0506 on this subject — under the key's own 0.06 cut — bound
  by D3, the membranes.** The blade failure's shape, pointed at the surface class this
  arc exists to test; neither predecessor's backdrop transfers. *Historical (the
  suspension): derive to maximise the minimum distance from every declared material,
  weighted toward D3 and the dark elements, saturated optima disqualified — the method
  ran exactly so, and D3 bound every optimum without needing a weight.*
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
