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
| N8 | a dark red layered cloth skirt | |
| N9 | green cloth panels in the skirt | own phrase, not a modifier on N8 |
| N10 | brown leather bracers | measured to land |
| N11 | **a gold plate on each outer forearm** | the promoted modifier — **this is the grammar test** |
| N12 | gold knee plates | measured to land |
| N13 | heavy dark boots | present in every arm; kept named rather than assumed |
| N14 | a massive greatsword | |
| N15 | an ornate gold crossguard | own phrase, not a modifier on N14 |
| N16 | a gold pommel | own phrase |

**N6 — "gold necklace" is struck.** The prompt carried it; there is no necklace at the throat in
the target; there is a belt medallion. A term that misnames an element, and produces the right
thing by accident, is the exact failure the identity-in-the-prompt rule exists to kill. The
Director left the call to the advisor: **the medallion is the element, the necklace term goes.**

**N11 is the live experiment.** Predicted before running: promoting the trim from a compound
modifier to its own head noun makes it land. **One roll. If it drops again, the specification
premise is weaker than [Amendment 12](../docs/experiments/E08-ruling-gate0.md) assumed, Arm B
waits, and this is reported rather than reworded.**

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
| fur trim edging the knee plates | the clean-control arms produce it **unprompted**, which suggests mesh- or style-supplied. **Not filed until two clean-control arms show it**, per the knee-plate precedent: that armour also looked mesh-supplied and vanished the instant the control was cleaned. Arriving from the mesh through a *noisy* control is not the same as arriving from the mesh. |

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
