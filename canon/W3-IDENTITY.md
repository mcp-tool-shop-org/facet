# W3 — identity specification (test fixture)

**Status:** authored by the advisor, 2026-08-04, on the Director's instruction ("this is a test
character, so there is no canon — you should either make canon or stop gating on a test
character. Probably should make canon").

**This is a test fixture, not a shipping character.** Its purpose is to give the pipeline a
**fixed identity target**, because without one "did the element land" has no ground truth and
no mechanism in the route can be tested. Any line here is the Director's to overrule in a
sentence; none of it needs his ratification to proceed.

Read off `canon/twin_front.png` / `twin_back.png` at full size. Those files are the **visual
target the spec was read from** — they are not the projection reference and must not be
projected (see [MANIFEST.md](MANIFEST.md)).

---

## Form

**Every element is its own noun phrase.** This is not style — it is the grammar constraint
measured in [E08 Amendment 13](../docs/experiments/E08-ruling-gate0.md): "gold knee plates"
(head noun, one modifier) landed in full; "gold-trimmed brown leather bracers" (head noun,
stacked compound modifier) landed its head noun and dropped the modifier. Elements expressed as
modifiers on other nouns are unreliable. **The spec below is written to that rule, so the spec
is itself the test of it.**

## NAMED — must appear in the prompt, or it leaves

| # | element | note |
|---|---|---|
| N1 | a bald head | |
| N2 | a long red beard | |
| N3 | a dark green knitted sleeveless tunic | |
| N4 | polished gold pauldrons | |
| N5 | gold scrollwork on the pauldrons | own phrase, not a modifier on N4 |
| N6 | **a gold belt medallion** | **replaces "gold necklace"** — see below |
| N7 | a brown leather belt | |
| N8 | a dark red layered cloth kilt | ⚠ **KILT, not skirt — the Director's ruling 2026-08-17.** The garment is a warrior's kilt and *skirt* was the wrong register for it. Renamed in the phrase, the surface id and N9 |
| N9 | green cloth panels in the kilt | own phrase, not a modifier on N8 |
| N10 | brown leather bracers | measured to land. ⚠ **QUESTIONED 2026-08-17:** plural, and the reference has no bracer on either forearm — the sword arm is bare and the free arm's leather is a wrist cuff belonging to N20's gauntlet |
| N11 | **a gold plate on each outer forearm** | the promoted modifier — **this is the grammar test**. ⚠ **QUESTIONED 2026-08-17, and this may remove it as evidence.** Re-verified at 6–8×: there is **no gold on either forearm**. The single plate sits on the gauntlet over the back of the free hand, and *each* is wrong because the armour is asymmetric. Its measured no-response (median ΔE 1.07, two grammatical forms) has a simpler explanation than co-location — **the generator was asked for something the reference does not contain**. Amendment 15 stands on the knee plates and bracers; N11 stops being its sharpest example |
| N12 | gold knee plates | measured to land |
| N13 | heavy dark boots | present in every arm; kept named rather than assumed |
| N14 | a massive greatsword | |
| N15 | an ornate gold crossguard | own phrase, not a modifier on N14 |
| N16 | a gold pommel | own phrase |
| N17 | **a brown leather-wrapped grip** | **NEW 2026-08-16** — an unoccupied surface, not a promoted modifier. Own phrase, not a modifier on N14. ⚠ UNVERIFIED: predicted to land, must be checked on the next generation |
| N18 | **brown leather gauntlets** | **NEW 2026-08-17, from the Director's own description after the advisor got it wrong twice.** Both hands, the same glove, extending up the arm and running **under** the gold arm brace. Draft 1 called both hands bare and forbade the word *gauntlet*; draft 2 called the armour asymmetric. Both were `twin_front.png` read as a description when it is a straight-on projection - the sword hand is shown **palm-on**. `twin_back.png` shows the brace on both arms and the advisor never opened it until told to |
| N19 | **a brown leather shin guard** | **NEW 2026-08-17, DRAFTED — awaiting the Director's ratification, and the row it fills was mis-named.** There is no bare shin on this figure: the gold knee plate is large and angular, runs knee through upper shin, and its lower point overlaps the boot shaft directly, with brown leather and grey fleece visible behind and beside it. The old `greave` row described a surface that does not exist as a separate thing. Alternative on the table: delete both rows and let N12 own the whole knee-to-boot run — closer to how the reference reads, but it costs the boot-top joint its second operand |

**N17 — the grip, added at the Director's delegation 2026-08-16.** He named the choice as leather
or steel and left it to the advisor. **Leather**, for four reasons, given in the order of how much
they should be trusted:

1. **The surface was unoccupied, and that is why this should land.** Nothing in N1–N16 named the
   grip, so whatever the generator painted there was arriving by accident and would leave the same
   way — it is one of the four regions the Director identified by eye. The measured law is
   co-location, not grammar: a specification determines what occupies a surface and **cannot** add
   a second element to an occupied one, which is why N11's promoted modifier drew ΔE 1.07 and no
   response. N17 occupies an empty surface, so it is the case the law says works.
2. **Brown leather is already twice-landed vocabulary on this character** — N7 the belt and N10 the
   bracers, the latter recorded as *measured to land*. It is the lowest-risk term available.
3. **Historically it is simply what a grip is**: a wooden core wrapped in leather, usually over
   cord. Bare metal grips exist but are late, ceremonial and unpleasant to hold — cold, slippery,
   and they transmit shock into the hand.
4. **Value legibility at sprite scale.** The grip sits between a gold crossguard (N15) and a gold
   pommel (N16). Dark leather gives a strong value break between them; steel between two golds
   reads as one continuous metal mass and the sword loses its articulation at the size these
   assets are actually viewed.

**One argument deliberately NOT used, because it does not decide.** It is tempting to reason from
the day's measurement — defect texels sit sub-pixel from material boundaries, so straddle error
scales with the colour difference across the boundary, so a steel grip beside a steel blade would
produce a *smaller* visible error. But the grip's neighbours are the crossguard and pommel, both
gold; the blade sits on the far side of the crossguard. Steel-vs-gold and leather-vs-gold are both
substantial boundaries, so the argument washes out. It is recorded here so nobody re-derives it and
mistakes it for a reason.

**This is a prediction, not a measurement.** N17 is expected to land because it occupies an empty
surface with vocabulary the model has already landed twice. That expectation is exactly the kind of
inherited claim this repo treats as a hypothesis wearing a fact's clothes — **verify it on the next
generation before building on it**, and if it draws no response the way N11 did, the co-location
law needs re-examining rather than the term needs re-wording.

**N6 — "gold necklace" is struck.** The prompt carried it; there is no necklace at the throat in
the target; there is a belt medallion. A term that misnames an element, and produces the right
thing by accident, is the exact failure the identity-in-the-prompt rule exists to kill. The
Director left the call to the advisor: **the medallion is the element, the necklace term goes.**

**⚠ N11 was the grammar experiment and it DROPPED — measured, not predicted.** Promoting the
trim to its own head noun produced **no change at all**: median ΔE 1.07 over the figure, 1.15 on
the forearm. Not a wrong element — no response to the phrase. The advisor's grammar hypothesis
is not what governs.

**The measured axis is co-location, not grammar** ([Amendment 15](../docs/experiments/E08-ruling-gate0.md)):

> A specification determines what occupies each surface. It cannot add a second element to a
> surface already occupied.

Knee plates and bracers *replaced* what was on their surface and landed, in the same grammatical
form that dropped when *adding*. **N5, N9 and N11 are the three co-location cases in this spec
and are predicted to drop; the other thirteen are predicted to land.** That prediction is
recorded before the full-spec run, and the run is the test of it. **Not to be reworded until it
passes — a spec tuned until it passes is not a spec.**

## MESH-SUPPLIED — arrives through the control from geometry; record the dependency

| element | note |
|---|---|
| stocky proportions, short-limbed and broad | **canon per the Director** (Amendment 12): the mesh's body is the character's body. The target twins' taller, narrower figure is an artifact of a control missing a quarter of the silhouette and is **explicitly not canon**. |
| the silhouette itself | the twin's only job is to register to it |

## STYLE-SUPPLIED — arrives from the LoRA; record so a model change is noticed

| element | note |
|---|---|
| painterly worked surface, visible brushstrokes | currently carried by prompt terms *and* the LoRA; source not yet separated |

## UNDER TEST — not yet filed

| element | why it is not filed |
|---|---|
| fur trim edging the knee plates | ⚠ **2026-08-17: the Director looked at the knees and reports no knee fur - boot and golden knee guards only.** What is at the plate edges is loose wispy painted strands; the advisor read them as a material and that reading is withdrawn. STAYS UNDER TEST, unpromoted. Original note: the clean-control arms produce it **unprompted**, which suggests mesh- or style-supplied. **Not filed until two clean-control arms show it**, per the knee-plate precedent: that armour also looked mesh-supplied and vanished the instant the control was cleaned. Arriving from the mesh through a *noisy* control is not the same as arriving from the mesh. |

---

## What this fixture is for

The pipeline questions it makes testable, none of which need the Director:

1. **Does an element expressed as a head noun land?** (N11, one roll, prediction recorded)
2. **Does a full specification reproduce?** Generate from N1–N16 on a clean control and check
   every element is present. **A spec tuned until it passes is not a spec** — halt and report.
3. **Does Arm B hold identity across eight views?** Each view carries this spec; drift is
   measured against it rather than argued.

His gate is on **pipeline outcomes** — does the mechanism work, and is the finished asset
better. Not on which armour the test dwarf wears.
