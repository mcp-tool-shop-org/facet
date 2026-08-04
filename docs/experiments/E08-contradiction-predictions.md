# The contradiction test — predictions, before either image exists

**NOT BLIND.** Full E08 record in context, including my own 0b report. Recorded before the SPEC
and CONTRA arms are submitted.

## What is being asked

If 14–15 of 16 named elements arrive *unprompted*, does naming matter at all? Name attributes
that **conflict** with what the route supplies and see which one the image carries.

- **Prompt wins** → identity is in the prompt, the route generalises to other characters.
- **Supplied attribute wins** → identity lives in the LoRA and mesh, the specification is
  decorative, and the pipeline produces this dwarf in different clothes.

Two arms, one variable: `E08-spec-prompt.json` (baseline) and `E08-contradiction.json` (the same
prompt with eight adjectives substituted in place). Same render, control, mask, seed 770700 and
sampler settings. Both run on cloud, so both sit on the same side of the hardware boundary — the
comparison is within-cloud and does not inherit 0b's ΔE 0.84.

## Prediction: the prompt wins on a majority. ~70%.

**The reasoning, and it is a consequence of the co-location constraint rather than a new guess.**
Every contradiction here is a **replacement** of the attribute occupying a surface, not an
addition to an occupied one. Amendment 15's constraint says replacement is exactly the operation
that works — "gold knee plates" and "brown leather bracers" both landed by replacing their
occupant. So the constraint, taken seriously, predicts these land.

Denoise is 0.92, so the latent contributes little and prompt + LoRA dominate. Colour is the most
promptable attribute there is.

**Against, and why not higher than 70%:** the LoRA is a style LoRA trained on saltroad canon. If
it encodes *this dwarf has gold armour* strongly enough, it can fight the prompt. "Arrives
unprompted" and "resists contradiction" are different claims — that is the whole point of the
test — but they are correlated, and I have no measurement separating them yet.

### Per-element, with the direction stated

| element | change | predicted signature |
|---|---|---|
| N4/N6/N12/N15/N16 metals | gold → silver | **ΔC\* strongly negative.** Gold sits at C\* 27–40, h 78–90. Silver is the neutral axis: C\* < 10 at any hue. Chroma collapse is the readout, not lightness. |
| N2 beard | red → white | **ΔL strongly positive** (L 24 → 60+) **and ΔC\* strongly negative** (C\* 42 → <10). |
| N3 tunic | green → blue | **Hue swing**, ~178 → ~250–300. Lightness roughly held. |
| N8 skirt | dark red → black | **ΔL negative** (13.5 → <8), **ΔC\* negative** (23 → <5). |

### The three co-location cases, reported outside the denominator

**And the framing needs one correction I want on the record before the run.** These were set
aside as "co-location cases," but contradicting an element that is *already present* is
replacement, not addition — so the co-location constraint does **not** predict they drop:

- **N5 scrollwork** and **N9 skirt panels** both arrive in the unprompted baseline. Contradicting
  them is replacement. **I predict they respond**, like the counted eight.
- **N11 forearm plate** does *not* arrive — it is the element with headroom. There is nothing on
  that surface to contradict, so **its region measures nothing** and cannot be read either way.

That is why they sit outside the denominator, and the pre-registration was right to put them
there — but for N5 and N9 the reason is bookkeeping, not a different prediction.

### The five held elements — the internal control

N1 scalp, N7 belt, N10 bracers, N13 boots, N14 blade are not contradicted. At denoise 0.92 a
changed prompt repaints somewhat globally, so I expect held ΔE **above 0b's 0.71** — but the
discriminator is the **ratio**:

- **contra ≫ held** → per-element attribution holds, the prompt is doing the work.
- **contra ≈ held** → the image repainted globally and no per-element claim is supportable,
  whichever way the colours went.

## The uniformity check is required, not optional

Per Amendment 21: a summary statistic clearing a threshold is not the finding — **the shape of
the residual is.** For the held class specifically I will report whether movement is spread
across all five or piled into one, because held movement concentrated in a single region is a
different fact from held movement spread evenly, and the class median hides both.

## What would make me halt

A spec tuned until it passes is not a spec. One roll per arm. If the result is ambiguous I report
it ambiguous rather than rewording either prompt.
