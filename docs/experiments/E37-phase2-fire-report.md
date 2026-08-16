# E37 Phase 2 — the corrected recipe fires: six repaints land, the lift is repaired, and the local ColorMatch is FALSIFIED

**Seat:** executor · **Written:** 2026-08-15 · **Spend: 52 → 58 of 80** (six jobs; plus one
failed submission that never sampled — §2). Executed under
[Ruling 27](E37-ruling.md).

---

## 1. What ran

| step | result |
|---|---|
| v6 probe under the corrected recipe | **PASS** — `ff846b5c-6495-4fd2-918b-56f52cf5f663`, spend 52 → 53 |
| the remaining five, one batch | **5/5 completed, 0 failed** — spend 53 → 58 |
| local composite + ΔE proof, six views | all six **CHANGED**, none a NO-OP |
| the v0 lift, silhouette-intersected, re-composited at +12 | **off-figure 643 → 0 px** |
| Ruling 27 clause 2 — the local ColorMatch | ⛔ **FALSIFIED — halted, not shipped** (§5) |

Payload diff per job, against the byte-pinned base: **three added nodes** (mask load,
`ImageToMask`, `SetLatentNoiseMask`), **node 9's init clay → the set-A twin**, latent
rerouted, prefix changed. Seed 2026081511, denoise 0.92, `cn_strength` 1.0, prompt, negative
and control all byte-held. **No `ColorMatchV2` in any graph** — asserted by a raising check
in the payload builder.

---

## 2. ⚑ An error of mine, and the server caught it

The first batch submission carried a **control-image hash I typed from a truncated 12-char
prefix in my own earlier console output** rather than reading it from the payload file on
disk. It is exactly the hand-retyped-payload class the record already names (E04 Arm G7,
*"submit saved workflow files verbatim"*).

The job **failed at input download** — `ImageDownloadError`, *"the input file … doesn't
exist"* — so **no sampling ran and no image was produced**. Whether a failed input download
draws credit is not something this seat can measure; it is recorded as an attempt and not
counted as one of the six.

**The repair, applied immediately:** every hash for the real batch was read out of
`phase2fire/payloads/*.json` programmatically and pasted verbatim. **No identifier in this
report was reconstructed from a truncated display.**

---

## 3. The locality gate — Ruling 27's pass condition, on all six

Outside-mask ΔE is the VAE round-trip floor. Compare against job 1 under the defective
recipe, which read **13.369**:

| view | dE inside | **dE outside** | ratio | hottest 0.5% inside mask |
|---|---|---|---|---|
| v1 chest | 3.057 | **0.368** | 8.3× | 99.5% |
| v3 ear | 3.510 | **0.374** | 9.4× | 59.2% |
| v4 ears (union) | 1.967 | **0.394** | 5.0× | 78.0% |
| v5 ear | 8.356 | **0.402** | 20.8× | 85.4% |
| v6 nose (probe) | 2.619 | **0.303** | 8.7× | 36.0% |
| v7 face band | 2.334 | **0.380** | 6.2× | 98.2% |
| *(job 1, defective recipe)* | *24.536* | ***13.369*** | *1.8×* | *0.1%* |

**The falsifier, re-run on the probe:** the correct v6 mask now scores **8.7×**, above all
three wrong-view masks (v5 5.8×, v7 3.4×, v3 1.6×). Under the defective recipe the correct
mask scored **worst** of the four. The ordering inverted, which is the discriminating result.

---

## 4. The ΔE repaint proof ([Ruling 26](E37-ruling.md)), on the DELIVERED set

Measured composite-against-original inside each mask's α > 0.5 core:

| view | core px | ΔE mean | median | p90 | max | > 2 | verdict |
|---|---|---|---|---|---|---|---|
| v0 (lift +12) | 8,602 | 13.02 | 13.27 | 13.66 | 14.17 | 100.0% | **CHANGED** |
| v1 chest | 10,832 | 3.24 | 2.97 | 5.78 | 8.95 | 71.8% | **CHANGED** |
| v2 | — | — | — | — | — | — | untouched, no repair named |
| v3 ear | 2,112 | 4.21 | 2.32 | 10.64 | 37.74 | 54.6% | **CHANGED** |
| v4 ears | 3,808 | 2.34 | 1.29 | 5.47 | 28.62 | 38.6% | **CHANGED** |
| v5 ear | 2,317 | 10.14 | 4.35 | 25.01 | 48.64 | 68.3% | **CHANGED** |
| v6 nose | 1,424 | 3.15 | 1.59 | 7.06 | 33.32 | 44.7% | **CHANGED** |
| v7 band | 6,503 | 2.56 | 2.13 | 4.83 | 14.16 | 54.5% | **CHANGED** |

**No repair is a no-op.** **Zero pixels moved outside any mask** (raising assertion, all
seven). **The held-pixel guarantee verified on the delivered artifact, not merely on the
mask**: v6's held rect (899 px) and v7's (437 px) both read **0 pixels moved, ΔE max
0.0000**.

---

## 5. ⛔ HALTED: Ruling 27 clause 2's local ColorMatch is falsified on this subject

Implemented as ruled — mkl, masked region as target, a 12-px ring of surround as reference,
applied feather-weighted — and its **numbers read like a success**: region-to-surround ΔE
**17.61 → 3.50** on v7, 14.73 → 6.28 on v1, 10.79 → 1.05 on v3.

**Walked at 5×, it destroys the face.** `diag_colormatch_v7band.png`: the masked band washes
to a pale desaturated block, the drawn brows/eye/mouth fade to low contrast, a hard
rectangular seam appears at the mask boundary, and a bluish strip lands on the background.
The pre-match composite in the same sheet is clean.

**Why, measured — the mismatch it corrects does not exist:**

| view | **ORIGINAL** region-vs-surround ΔE | composite region-vs-surround ΔE | delta |
|---|---|---|---|
| v1 chest | 13.14 | 14.73 | +1.59 |
| v3 ear | 10.34 | 10.79 | +0.46 |
| v4 ears | 12.14 | 13.08 | +0.94 |
| v5 ear | 9.71 | 14.62 | **+4.91** |
| v6 nose | 6.97 | 7.67 | +0.70 |
| v7 band | 16.92 | 17.61 | +0.69 |

The untouched originals already sit **9.71–16.92 ΔE from their surround**, and the composites
sit **+0.46 to +4.91** from that — five of six under +1.6. The 17.61 the match was
"correcting" is **the face being a face**, not a repaint defect: these regions contain drawn
features and their surround is plain wood, so they are legitimately different distributions.
Forcing one onto the other fits the features away.

**This is [Ruling 20](E37-ruling.md)'s conflation one layer further down** — there a
dark-speck census could not separate drawn face from defect; here a colour-transfer cannot
separate drawn face from tone error. And it is the repo's metric law firing exactly as
written: a number that says 17.61 → 3.50 while the artifact degrades is not measuring the
thing it is being read for.

**Not shipped, not re-tuned.** The delivered set carries the **composites**. Clause 2 is
reported as fired with its sheet and its table; whether ColorMatch has any remaining role
once the init is correct is the advisor's to rule. The finding this seat can state: **with
node 9's init corrected, the repaint inherits the twin's tone directly, and the step clause 2
existed to perform has no measurable work left to do.**

---

## 6. The v0 lift, repaired by construction

| | support px | off-figure support | backdrop raised | core L\* |
|---|---|---|---|---|
| before (rect mask) | 10,034 | **643** | mean +6.01, max +12.15, a visible +2.30 L\* step | 42.70 → 54.70 |
| **after (∩ silhouette)** | 9,391 | **0** | **+0.00, max +0.00** | 42.57 → **54.59 (+12.03)** |

Off-figure lift is now zero by construction rather than small by measurement, and the ruled
+12 rung still lands (+12.03 on the α = 1.0 core).

---

## 7. Sheets, native, walked at 1:1 at this seat

`sheet_repaired_set_native.png` (2998 × 1050) · `sheet_beforeafter_all.png` (3086 × 2087) ·
`diag_colormatch_v7band.png` · `diag_colormatch_v5ear.png` ·
`sheet_v6_beforeafter_5x.png`.

**Observations from the walk — content, for the Director's eye, no verdict from this seat:**

- **v0** — the face reads lighter; the lift's boundary is discernible as a soft tonal edge across the forehead and jaw. Ears and skull excluded by the mask; drawn features intact.
- **v1** — the dark torso column persists, and the within-view tonal split against the limbs that the phase-1 report named is still present.
- **v3** — the ear changed from a domed knob with a light rim to a flatter, more uniformly dark disc with visible grain. Still reads as a detached disc.
- **v4** — both ears read lighter and sit closer to the skull tone than before.
- **v5** — the largest change in the set. The flat pale disc is **gone**, and what occupies that area now reads as a **drawn eye and brow**. This is a change of feature class, not a cleaner disc, and it is named here rather than counted as a repair.
- **v6** — the wedge softened along its lower edge; it still reads as a hard-edged wedge.
- **v7** — dark brow paint **outside** the held rect is heavier than before. The held rect itself is exactly preserved (0 px, §4), but brow weight is identity-adjacent under Rulings 19–20, so the change is surfaced rather than absorbed.
- Across all eight: **one wood, no banding** — the single-seed construction still holds after six masked repaints.

---

## 8. State

- **Spend 58 of 80.** Six repaints fired and landed; one submission failed at input download without sampling (§2).
- Set A originals are **untouched**; `phase2/masks_v2/` untouched; all writes append-only under `phase2fire/`.
- Manifest gates HELD at open and close; E15 four legs exit 0; watchdog ADVANCING on two reads.
- Nothing tuned, no threshold moved, no gate re-read to make it pass. The one falsified step is reported as falsified.

**What the next ruling decides:** the disposition of clause 2 (the local ColorMatch, whose
job appears to be empty once the init is right), and whether v5's feature-class change and
v7's brow-weight change go to the Director as-is or are re-cut.
