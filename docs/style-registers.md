# Style registers — the plan (Director's directive, 2026-08-06)

**The directive, in the Director's words:** a dragon should look *ultra realistic and
scary*; *"none at all is better than making the same texture for everything"*; and the
studio needs to **train more LoRAs for varied textures and consolidate the ones it
already has.** This document is that plan. It was occasioned by E12's first styled
pair — rejected at his eye because the saltroad painterly register, which two subjects
earned acceptance under, had been inherited by a third subject it does not fit
([E12-ruling.md](experiments/E12-ruling.md) Ruling 10).

## The rule the rejection bought

**The style register is subject data.** It lives in the fixture's STYLE-SUPPLIED
section (register terms + the LoRA by live card name, or NONE) and is expressed
mechanically in the profile (`lora-w`, the prompt tail). A register arriving by
inheritance is the same accident class as any other undecided subject value — the
profile system's founding lesson, one layer up. No fixture may leave the section
implicit again.

## Register assignments as of this ruling

| subject / class | register | LoRA | status |
|---|---|---|---|
| W3 (Figure) | painterly, visible brushstrokes | `saltroad_style_v2_lowlr_000001500` | earned — accepted asset |
| galleon (Transport) | painterly, worked surface | saltroad, same card | earned — accepted asset |
| dragon (Creature) | **ultra-realistic, menacing** | **NONE** (Ruling 10b) | ruled; the re-pair is its first evidence |
| Architecture / Environment (future) | undecided | undecided | decided per subject when the classes open |

The LOGO-IDENTITY scheme (Figure / Architecture / Creature / Environment / Transport)
is the class map this table grows along — five families, five potential registers.

## Consolidation — the inventory pass (queued studio-side)

The studio holds several trained cards beyond saltroad (rustline for Hesperia's
grounded look, the pirate3d skin card, the sprite-foundry HD line's cards, among
others — **inventory from memory, to be VERIFIED against the account's Model Library,
which is ground truth; API listings are not**). The consolidation deliverable, one
session, sdlab-adjacent:

1. Enumerate every card actually in the library (browser, not API), with provenance:
   base model, training data, the register it produces, where it has been accepted.
2. One page per card in a single registry (sdlab is its natural home — training is
   sdlab's lane); retire duplicates and dead experiments explicitly, nothing silently.
3. Map cards to the five-class register table above; the gaps are the training
   roadmap's demand list.

## Training roadmap — new registers, earned not assumed

New LoRAs train **through the sdlab lane** as its datasets mature — which is exactly
what E11 built: accepted assets become dense, provenance-clean training trees. The
first candidate register is the one today's rejection names: **realistic-creature**.
Its path: the beast runs NO-LoRA first (the model's own realistic prior, constrained
by our geometry and identity prompt); if the register proves out at the Director's
eye but drifts across assets, THAT is the evidence a creature-register LoRA is worth
training, and the accepted creature assets are its dataset. The same logic serves
each future class: **no LoRA until the register drifts; train on accepted assets when
it does.** Nothing trains on rejected artifacts.

## What this changes in facet immediately

- `canon/DRAGON-IDENTITY.md` STYLE-SUPPLIED rewritten (register terms, LoRA NONE).
- `profiles/beast.json`: `lora-w 0.0`; prompt tail carries the register; the canny
  pair is marked falsified-for-subject with the re-pair arm owning its replacement.
- The re-pair dispatch (executor kickoff, Session handoff 4) runs the new register
  with a structure-carrying control.
