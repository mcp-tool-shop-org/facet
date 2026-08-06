# E12 handoff 2, Task 3 — backdrop prediction, pre-registered before deriving

**Executor session, 2026-08-05.** Committed **before `e04_backdrop.py` runs on this
subject.** `canon/dragon-materials-estimated.json` exists (it is the derivation's input and
had to be authored first) but the derivation has not been run, and no backdrop has been
computed. The dispatch requires the prediction to be pre-registered; this is it.

---

## What the derivation will be handed

Eleven estimated materials. What matters for the metric is how they are distributed in
luminance, so: a **pale cluster** — the ivory family D4/D5/D6/D7 at [222,212,188] and D10 at
[232,226,206], plus D2 pale bone-tan at [206,188,154] — a **mid** pair, D3 storm-grey at
[110,114,120] and D1 moss-green at [70,88,58], and a **dark cluster**, D11 slate [52,56,62]
and D9 wine-red [92,30,36]. One outlier in hue only: D8 ember-orange [214,96,30].

**This palette spans nearly the whole luminance range.** That is the fact the predictions
below turn on, and it is the structural difference from the galleon, whose declared materials
clustered in the warm mid-tones and left white genuinely far away.

## The predictions

| # | prediction | falsified by |
|---|---|---|
| **R1** | The **unconstrained optimum is saturated** — max−min channel > 0.30 — and is therefore **disqualified** by the standing rule that a saturated backdrop bleeds into a diffusion image. No declared material is blue or violet, so the metric will run there. | an unconstrained optimum with saturation ≤ 0.30 |
| **R2** | The best **neutral** backdrop lands in the **mid range, 0.50–0.65** (128–166 of 255) — **not** near black and **not** near white. Both ends are occupied: the ivory family blocks white, D11/D9 block black. | a neutral optimum outside that band |
| **R3** | The material **binding** the neutral optimum is **D3 (storm-grey membranes)** or one of the **ivory family** — the two things a mid-grey sits between. If this holds, the dispatch's concern about D3 is expressed by the derivation itself rather than needing a weight. | any other material binding it |
| **R4** | The neutral optimum's score is **below 0.20** — no neutral is comfortably far from everything on this subject, because the palette spans the full range. For comparison the key's own threshold is 0.06. | ≥ 0.20 |
| **R5** | The recommendation will therefore be a **low-saturation NON-neutral** rather than a pure grey. A mid-grey is uncomfortably close to W3's inherited "plain grey background", which is the documented failure this whole derivation exists to avoid — and a slight tint buys distance in one channel at little diffusion risk. | the best low-saturation option being a pure neutral, or being worse than the neutral |
| **R6** | **The galleon's white will not transfer.** Its score here will be materially worse than the neutral optimum's, because D10's ivory at [232,226,206] sits within 0.19 of white on the max-channel metric before the thin weight, and 0.096 after it. | white scoring at or above the neutral optimum |

## What I am not predicting

- **The chosen word.** The tool proposes; the ruling adopts. What lands in the twin-prompts
  file is a name for a colour, and naming is where an estimate becomes a prompt term.
- **Whether the estimates are right.** They are read off eleven English phrases and are the
  weakest link in the chain; the styled pair supersedes them by the fixture's own
  non-circularity rule.
