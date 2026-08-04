# E08 — the armour test: canon can be stated in the prompt

**Amendment 10:** [E08-ruling-gate0.md](E08-ruling-gate0.md) ·
**Canon ruling:** [E08-director-canon-ruling.md](E08-director-canon-ruling.md)
**Run:** 2026-08-04, executor session. **One diffusion pass, 63 s.**
**Prediction, recorded first:** `facet_E08/ARMOUR/PREDICTIONS.md` — blind, and **wrong**.

One term inserted into `restylize_views.py`'s own default prompt — **"gold knee plates"** —
and nothing else altered. Clean geometry-derived control, grey background, seed 770700.

**Control image byte-matched to BG2-grey**: 20,973 px, canny 15,325 + contour 9,958. The
prompt term is the only difference between the two runs.

## Result

**The gold knee plates returned.** Faceted gold plate over the knee, correctly placed, fur
reduced to a trim beneath it, dark boots — and the legibility gain of the clean control is
kept: the hand is a hand, the boots and belt read, the figure fills the frame.

| | canon (shipped) | clean control | clean control + armour term |
|---|---|---|---|
| gold knee plates | yes | **no — fur wraps** | **yes** |
| boots | dark | dark | dark |
| legibility | hand a smudge, lower legs vague | good | good |

## Predictions, and they were wrong in the useful direction

| # | prediction | outcome |
|---|---|---|
| E1 | plates do **not** fully return (~40% they would) | **FALSIFIED** — they returned cleanly |
| E2 | if anything returns it is partial or misplaced — gold as trim or highlight, since the control carries no interior knee contour | **FALSIFIED** — proper plate, correctly placed |
| E3 | boots stay fur | **mis-stated** — the boots were dark in both arms; the *shins* were furred, and the fur is reduced to a trim under the plate |

My reasoning against was that **"heavy dark boots"** was already in the prompt and the clean
control had overridden it. That was the wrong read: the boots were never overridden — they are
dark in every arm — so there was no precedent for prompt terms losing, and I invented one.

## What it decides

**Canon can be stated in language.** The plates were never in any prompt: they came through the
ControlNet from the mesh's own knee armour under a noisy keyed-mask control, and vanished when
the control was cleaned to the exact silhouette. Naming them restores them.

So the tension the canon ruling exposed **largely dissolves**: canon comes from the prompt
where it can be stated, and the control is free to be clean. The registration gain and the
character are not mutually exclusive after all.

It also splits Amendment 8's "the extra control was noise" precisely: the surplus 23,000 px was
**noise for registration and signal for identity** — two properties collapsed into one verdict.
Naming the detail replaces the signal without reimporting the noise.

## Not yet closed

- **The forearm.** Canon has a gold-trimmed brown leather bracer; both clean-control arms have a
  brown fur cuff. The default front prompt never mentions bracers — `E02-prompts.json`'s palette
  spine does (*"gold-trimmed brown leather bracers"*). The same one-term fix is the obvious next
  test and is untried.
- **Proportion.** The clean-control twins read stockier and fill more of the frame than canon.
  That follows from hugging the mesh silhouette, and the mesh is stocky — the canon twin is the
  *less* faithful rendering of the geometry. Whether that matters is the Director's.
- **This is one twin, front only.** The back is untested, and no twin here has been put to the
  Director as a canon proposal.

Artifacts: `facet_E08/ARMOUR/` — `w3clay_0.png`, `w3clay_0_gen.json` (the first provenance
sidecar this pipeline has produced), `PREDICTIONS.md`. Sheets in `facet_E08/LOOK/`.
