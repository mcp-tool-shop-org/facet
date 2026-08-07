# LONGSWORD — identity specification (test fixture)

**Status:** authored by the advisor, 2026-08-07, on the Director's designation of
candidate **00001** ("00001 is my favorite" — E14 Ruling 1) and his register sentence
("Ultra-realistic, no LoRA"). **This is a test fixture, not a shipping asset.** Its
purpose is a fixed identity target so that "did the element land" has a ground truth
on the route's first prop. Any line here is the Director's to overrule in a sentence;
none of it needs his ratification to proceed.

Form is read off `longsword_clay_p1_00001_.png` and the designated mesh
(`longsword_00001_raw.glb`, 999,474 faces, 1 welded shell, zero boundary edges,
Gate 0 frame 240×1024). **There is no styled visual target yet** — this spec is
authored *forward*: the styled target pair will be generated FROM it, and identity
enters through the prompt or it is arriving by accident.

**Authored under the ruled register, deliberately.** The dragon taught that palette
and register interact (five "bone" terms read literally under realism — E12 Ruling
12e), so every colour word below was chosen with ultra-realism in mind: material
words name materials that ARE their colour (steel, blackened iron, gold, oxblood
leather, garnet), and no family word rides more surfaces than it owns.

---

## Form — the grammar rules, inherited as measured

**Every element is its own noun phrase** (E08 Amendment 13). **A specification
determines what occupies a surface and cannot add a second element to an occupied
surface** (Amendment 15) — every element below paints a surface that exists as
geometry on the designated mesh, each surface is owned by exactly one element, and
any future edit that decorates an occupied surface (an inscription down the blade, a
jewel on the boss) is predicted to drop; to change such a surface, replace its owner
on a named region instead. **Terms are comma-free** (the deletion-construction
grammar — an internal comma shatters a term at the stem builder).

## NAMED — must appear in the prompt, or it leaves

| # | element | note |
|---|---|---|
| L1 | a battle-worn steel blade with a raised central ridge | the dominant surface: both blade faces, both edges, the tip. The mesh's nicks and scoring are geometry; this element colours them — worn steel, not mirror chrome, so the relief reads as damage rather than vanishing into specular. **S-steel owns this element's risk**: near-achromatic, hue-undefined below the chroma floor — the measured E07/W3 class, on home ground |
| L2 | a blackened iron crossguard | both quillon arms end to end — the stepped chamfered ends included — and the guard's underside. Dark against L1's light steel so the two greys separate by VALUE, since below the chroma floor they cannot separate by hue |
| L3 | a gold diamond boss at the crossing | the raised diamond boss, both faces. **Surface list also carries the two collar rings** (pommel collar + mid-grip ring) as gold-family members with a watch note — the D6-spur pattern: they earn their own prompt term only if the pair mislands them. Gold appears ONCE as a term; gilded fittings are physically coherent under realism where the dragon's five bones were not |
| L4 | an oxblood leather grip wrap | the coil wrap, both sections, groove interiors included. Oxblood is the studio's proven wine register (W3's skirt) in a material that IS its colour |
| L5 | a dark garnet gem pommel | the faceted polyhedral gem. Facets are geometry (designated-in with a softer apex — Ruling 1); this element colours them deep garnet-red. Below any area floor by construction at route frames — **the D8 lesson applies: no numeric gate may be armed on this element; landing is judged by eye at the hilt crop** |

## MESH-SUPPLIED — arrives through the control from geometry; record the dependency

| element | note |
|---|---|
| the form, stance and silhouette | tip-standing, bilaterally symmetric, quillon span on one horizontal axis (widest-horizontal 0.2258, the route's first portrait subject) — the MESH's stance; twins register to it |
| the central ridge | full blade length, both faces, legible under `--clay` |
| edge nicks and blade scoring | moderate density, reconstructed as attenuated relief — L1 colours them |
| the wrap's coil relief | lumpy but legible turns with grooves; **the pinch locus** (58.7% of the mesh's 121 non-manifold edges — S-wrap) |
| the two collar rings and the diamond boss | modelled; L3's family |
| the gem's facet planes | modelled, softer apex than siblings — designated-in |
| the tip | free, pointed, a hair of apex rounding at 4× — designated-in |
| **the hollow interior** | the mesh is a double-walled shell, walls ~two voxels (E14 Ruling 3, route-wide) — invisible, culled, never painted; recorded so no downstream consumer assumes a solid |

## STYLE-SUPPLIED — the subject's REGISTER; a per-subject decision, never an inheritance

*Decided at designation day one, per the style-registers law — the Director's
sentence, 2026-08-07: "Ultra-realistic, no LoRA."*

| element | note |
|---|---|
| **register: ultra-realistic** | the Director's words made prompt terms; the model's own realistic-weapon prior is WANTED, constrained by our geometry |
| **LoRA: NONE** | expressed mechanically as `prop.json` `lora-w: 0.0`; the no-LoRA paths exist on both generation stages (restylize since E12 handoff 4; the brush since E13 handoff 15 step 0), each guarded by the inverted pre-flight |
| worn metal, harsh directional light | realism-register support terms; the pair re-measures whether they carry |

## Pre-registered stressors — named before any generation exists, evidence status labeled

- **S-steel** *(measured: E07 Gate 1, E08 §9a, the W3-key derivation, E12's chroma-floor
  law)* — the point of this subject. Steel on a neutral backdrop is the route's
  five-times-measured grey-on-grey trap: paint sitting ON the key's threshold, hue
  undefined below the chroma floor (C\* 1.6–2.8 reading as blue at hue 267), the blade
  band taking 0.00% of stage-1 reference in every measured E07/E08 view. **The backdrop
  derivation must hold L1 furthest of all elements and cannot be any grey.** Declared
  hue occupancy at authoring: steel/iron achromatic · gold warm yellow · oxblood + garnet
  wine-red. **Blue-violet is unoccupied** — the expectation for the derivation,
  pre-registered, checked not assumed (the 8a/15i lesson: occupancy claims go stale).
- **S-thin** *(measured at Gate 0)* — the blade is a **hollow box section**: total
  thickness ~0.0208 at mid-blade, two ~0.00196 walls around a cavity. `thin_extent`
  derives fresh with the published cost curve; the two-sided extent probe reads
  outer-to-outer total (~0.021), not wall thickness, so the hollow does not confuse it —
  stated so nobody discovers it as a surprise. No inherited value transfers (character
  0.03 figure-derived · ship 0.01 filament · beast 0.005 wing-artifact).
- **S-wrap** *(measured at Gate 0)* — the pinch locus is the wrap, not the edges: fine
  relief becomes non-manifold pinching, not density (E14 Ruling 2c). Wherever weld,
  decimate or cull runs: **report the shell census and the wrap band's non-manifold
  count before and after.** One shell at designation; anything that splits or loses
  wrap geometry reports.
- **S-hilt-scale** *(unread guess, labeled as one — the E12 head physics transposed)* —
  at the route frame the hilt (wrap coils, gem facets, boss) occupies roughly 7% of
  frame pixels, the same order as the dragon's head. If the pair's hilt reads soft, the
  measured levers are the per-subject rect in the bake (the A2 arm, specced) — **never a
  crop generation** (frame-changes-register, falsified ×3, E12 Ruling 24b).
- **S-symmetry** *(measured at Gate 0, observational)* — bilateral; the eye-level ring's
  mirror-pair silhouette facts (E12 Rulings 9b/16f) apply with near-identical pairs.
  Any instrument normalising by per-view silhouette area inherits both caveats.
- **S3, kept from the galleon** *(principle, proven twice)* — nobody's eye knows what
  this sword's palette "should" be; it is authored here. The off-palette gate's bands
  derive from these named materials and cross-check against the styled target pair once
  it exists — never against the twins they will gate. Numeric bands are NOT declared in
  this file.

## THE OCCUPANCY AUDIT (2026-08-07, done at authoring — the E12 Ruling 20c pattern, day one)

Every modelled structure enumerated against every element's letter, from the Gate 0
sheets, the hilt crop and the tip crop at zoom, by the advisor. The map, complete:

| structure (modelled, from the clay and mesh) | owner |
|---|---|
| blade faces · both edges · central ridge · nicks and scoring · the tip | L1 |
| both quillon arms · stepped chamfered ends · guard underside | L2 |
| diamond boss, both faces | L3 |
| pommel collar ring · mid-grip collar ring | L3 (surface list; own term only if the pair mislands them) |
| the coil wrap, both sections, groove interiors | L4 |
| the faceted gem | L5 |
| the hollow interior walls | not paintable — never visible; culled by construction |

No other modelled structure was found. Every future element edit re-checks this table
rather than discovering its gap at generation.

## What this fixture is for

1. **Does the route hold its fourth subject class?** Character, ship, beast, now prop —
   every value the route needs comes from `profiles/prop.json` or this fixture; a change
   required *outside* those two files is the finding.
2. **Does steel survive the acceptance chain?** S-steel is the point of the subject: the
   E07 blade failure and the five-times-measured grey-on-grey class finally fight on
   home ground, with the chroma-floor law and the backdrop derivation armed from birth.
3. **Does identity ride in the prompt at five elements?** The smallest element count the
   route has carried — W3 ran 8/8 at 7.4×, the galleon twelve, the dragon eleven. Five
   elements on six surfaces is the compact case.

The Director's gate is on **pipeline outcomes** — whether the mechanism works on a prop
and whether the finished asset is good. Not on which colours a test sword wears.
