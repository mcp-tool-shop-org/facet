# E08 — the contradiction test: report

**Executor session, 2026-08-04.** Predictions in
[E08-contradiction-predictions.md](E08-contradiction-predictions.md), committed at `17848b0`
before either arm was submitted, and disclosed as **not blind**.

Both arms run on Comfy Cloud in one batch, so the comparison is **within-cloud** and does not
inherit 0b's hardware-boundary ΔE 0.84.

## Result: the prompt wins. All eight contradicted elements moved.

```
WHOLE FIGURE  SPEC -> CONTRA
  median ΔE  17.09      <- against N11's no-response floor of 1.07
  mean ΔE    23.26
  >2.3  98.6%     >10  61.0%
```

The first number that matters is 17.09 against 1.07. **The model read the phrases.** N11's
failure mode — no perturbation at all — is not what happened here.

### The discriminator was the ratio, and it is 7.4×

| class | n | median ΔE | range |
|---|---|---|---|
| **contra** | 10 | **46.28** | 24.49 – 56.05 |
| coloc | 1 | 47.41 | — |
| **held** (control) | 5 | **6.23** | 5.06 – 6.91 |

Held is not zero — at denoise 0.92 a changed prompt repaints somewhat globally, which was
predicted. But contra sits **7.4×** above it. **Per-element attribution holds.**

**Uniformity check** (required, Amendment 21): held spans 5.06–6.91, a spread of **1.85 across
five regions**. The global component is spread evenly, not piled into one region. Had held's
median come from one region at 20 and four at 2, this table would mean something different.

## Direction, per element — stated before the run

**The metals, gold → silver.** Pre-registered readout: *chroma collapse, not lightness.* That is
exactly what happened — seven of seven onto the neutral axis:

| region | C* SPEC → CONTRA | ΔC* |
|---|---|---|
| N6 medallion | 55.7 → **1.2** | −54.5 |
| N15 crossguard | 49.7 → **1.8** | −47.9 |
| N4 pauldronR | 47.0 → **1.9** | −45.1 |
| N16 pommel | 41.7 → **1.8** | −39.9 |
| N4 pauldronL | 37.0 → **3.2** | −33.8 |
| N12 kneeL | 33.1 → 8.2 | −24.9 |
| N12 kneeR | 33.0 → 8.6 | −24.4 |

RGB confirms it: pauldron `(146,103,29)` gold → `(116,118,121)` grey.

> **Do not read the hue deltas on these rows.** Once chroma collapses to ~2, hue angle is
> undefined and the Δh column is noise — N4 pauldronR's "−164.8°" is an artifact of C* 1.9, not a
> colour rotation. Chroma is the readout. This was pre-registered.

**N2 beard, red → white.** Predicted +L and −C*. Measured L 24.3 → **53.1**, C* 44.1 → **7.2**.
RGB `(109,38,17)` → `(139,124,121)`.

**N3 tunic, green → blue.** Predicted a hue swing to 250–300. Measured h 174.1 → **297.0**, with
chroma *rising* 11.6 → 40.2. RGB `(14,38,32)` → `(9,22,78)`.

## Where I was wrong

**N8 skirt, dark red → black.** I predicted −L and −C*. Chroma collapsed as predicted
(23.9 → 0.7) but **lightness went up, not down**: L 14.7 → **33.8**, RGB `(67,22,27)` →
`(79,80,80)`. "Black" produced a desaturated **mid-grey**. The element responded; my direction
was half wrong.

**The knee plates are the weakest response.** C* 8.2 / 8.6 against ~1.8 for the other five
metals, and on the sheet they read closer to brown leather than to silver. They moved, but least
completely of the seven.

## The co-location correction was right, and the original framing was wrong

The pre-registration set N5/N9/N11 aside as "co-location cases, predicted to drop." **Before the
run** I corrected that: contradicting an element that is *already present* is replacement, not
addition, so co-location does not predict a drop.

**N9 skirt panels, green → grey: ΔE 47.41, C* 40.3 → 9.1.** It responded, right alongside the
contra class. The correction holds and the original prediction would have been wrong.

(N5 and N11 have no measurement region — the sixteen boxes do not map one-to-one onto the sixteen
elements, and N11's forearm plate does not arrive in the baseline anyway, so there was nothing
there to contradict.)

## What this answers

**Identity is in the prompt.** The LoRA, mesh and control did not hold this dwarf's attributes
against a conflicting specification — every named colour and material changed to what was asked
for. **This is not a dwarf generator.**

And the sheet shows the other half of it: **it is still the same dwarf.** Same face, same build,
same pose, same bald head, same brown bracers, same boots. Structure held by mesh and control;
named attributes carried by the prompt. That is the division Amendment 12 asserted, now with a
denominator of eight.

The crop-free hue×chroma panel says it without any box: SPEC carries a large warm high-chroma
mass (gold), CONTRA's has largely migrated to the neutral axis with a new spike at the tunic's
hue.

## Prediction against outcome

| predicted | outcome |
|---|---|
| prompt wins on a majority of eight, ~70% | **8 of 8 responded** |
| metals read as chroma collapse | confirmed, 7/7 |
| beard +L −C\* | confirmed |
| tunic hue → 250–300 | confirmed, 297.0 |
| skirt −L −C\* | **half wrong** — C\* yes, L rose |
| co-location cases respond (my pre-run correction) | confirmed on N9 |
| contra ≫ held | confirmed, 7.4× |

## Files

`CONTRA/spec_vs_contra.png` — SPEC | CONTRA | ΔE heat, plus hue×chroma density for both.
`CONTRA/contra_dE.json` — every number above.
`prompt_id` SPEC `edfcacd8-3c80-4b54-856c-b9a751ece3d8` · CONTRA `67781f49-7b1c-42b9-9596-4e0883a352b7`.
