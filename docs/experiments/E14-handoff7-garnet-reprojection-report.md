# E14 — the garnet re-projection RAN, and stroke 1 re-entered

**Executor session, 2026-08-08.** Ruling 26 (`9b7c664`), executed per 26e. **The
works-perfectly gate passed pixel-identically; no gate fired; no halt.**

---

## 1. ⚠ THE WORKS-PERFECTLY GATE — PASSED, PIXEL-IDENTICAL

Six **uncorrected** twins through the spine, compared against `stage1b_atlas.png` on the
demoted territory:

```
territory texels          67,904
differing texels          0
max abs channel delta     0
GATE PASSED - PIXEL-IDENTICAL on the territory.
(whole valid set, reported not gated: 0 of 3,661,903 texels differ)
stage1b_atlas.png  sha256 69f61f32a3e2281aff653fb2b740a849
gate atlas.png     sha256 69f61f32a3e2281aff653fb2b740a849
```

**Stronger than the gate required**: the entire atlas is byte-identical, same SHA-256. The
machinery is deterministic on content-identical inputs, as the ruling assumed.

## 2. The corrected M2 run

Twins 1/3/5/7 at the ruled rotations (**+51.80 / +34.47 / +55.45 / +48.01**, asserted against
Ruling 26c/5 before the run), twins **0/4 unrotated** — the *original* files, not my corrected
copies.

**One finding the restriction exists for.** The corrected run's own styled total is
**1,658,221 against stage 1b's 1,656,847 — +1,374 texels, all outside the territory.** The
corrected twins are byte-identical to their inputs outside the stone mask, but `project_twins`
keys each twin's figure from the image itself, so changing the stone's colour moves which
stone-adjacent pixels pass that key (registration IoU moved 0.9337→0.9366 on view 1, and
similarly on 3/5/7). **Without the restriction those 1,374 would have ridden in unnoticed.**

## 3. The restricted write — invariance printed

```
[reproj] territory            67,904 texels
[reproj] of those, HOLES now  67,904   <- THE WRITE SET (territory AND holes)
[reproj] of those, already styled (excluded by construction): 0
[reproj] ASSERTED: no styled texel in the write set; the write set is inside the territory
[reproj] ASSERTED: every texel outside the territory is byte-identical (16,709,312 texels)
[reproj] styled 1,656,847   holes 2,005,056
[reproj] atlas sha256  69f61f32a3e2281aff653fb2  ->  6a9b93e04c696da3802a2de9
[reproj] source sha256 1b2d54b8cb7e0a1deba0ec04
```

**The banked A0's styled count is restored exactly** — 1,588,943 → 1,656,847, the demotion's
dip closed to the texel. The compensator (`e14_demote_garnet.py --undo`) stands unused.

## 4. ⚠ THE 19b-FORM HUE READOUT on the filled territory

| | after | stage 1b |
|---|---|---|
| stone valid / styled | 177,314 / 86,949 (49.0%) | same |
| above C\* 12 | 19,573 (22.5%) | 20,761 |
| **median hue** | **22.5** | 308.6 |
| C\* median | **21.2** | 21.2 |

| band | after | stage 1b |
|---|---|---|
| **wine 0–25 — L5's declared band, garnet** | **57.38%** | 15.04% |
| orange 25–42 | 10.33% | 0.26% |
| gold 42–104 | 7.76% | 12.78% |
| forbidden 104–290 | **5.65%** | 1.41% |
| lavender 290–310 | 0.44% | 21.71% |
| magenta 310–360 | 18.43% | 48.80% |
| **lavender + magenta** | **18.88%** | 70.51% |

### 4b. The 19b ownership partition, on the corrected stone

| owned by | texels | median hue | wine | lav+mag | C\* med |
|---|---|---|---|---|---|
| the GARNET views (0, 4) — **unrotated** | 4,702 | **17.6** | 65.40% | 7.49% | 20.9 |
| the DRIFTED views (1, 3, 5, 7) — **rotated** | 14,871 | **24.2** | 54.85% | 22.48% | 21.3 |
| *stage 1b: drifted-owned* | *16,059* | *322.6* | *0.34%* | *88.97%* | *20.1* |

**The two territories were 305° apart and are now 6.6° apart.** The garnet partition is
untouched to the texel — the ruling's decision not to rotate 0/4 shows here as an exact
no-op.

### 4c. L and C\* on the same 67,904 texels, so no population shift can confuse it

| | before | after |
|---|---|---|
| L\* median | 4.309 | 4.182 |
| **L\* per-texel \|Δ\|** | | **median 0.0882**, p99 17.39, max 61.93 |
| C\* median | 6.241 | 6.109 |
| **circular hue** (above the stage-1b floor, n = 16,059) | **329.16** | **18.39** |
| median ΔE over the territory | | 4.561 (p90 19.998) |

**L is preserved to a median of 0.088 L\* units per texel.** A first reading of §4's tables
suggested L had moved (15.66 vs 16.68) — that was **two different populations**, because the
rotation moved 1,188 texels across the C\* 12 line. Measured on a fixed set it is a no-op, and
the p99/max tails are the blend and levelling mixing corrected paint with unrotated
neighbours, not the transfer.

The territory lands at circular hue **18.39** rather than the reference's 8.18, because the
blend mixes corrected drift paint with the unrotated garnet views' paint. That is the spine
doing its job, and 18.39 sits inside the family (twin 4 reads 16.54, twin 0 33.65).

## 5. ⚠ A DEFECT, LOCATED AND BOUNDED: the forbidden band rose at the collar junction

The forbidden band 104–290 went 292 → 1,106 texels on the stone; orange 25–42 went 54 →
2,022. Located exactly:

| the 1,086 newly-forbidden texels | |
|---|---|
| inside the re-projected territory | **1,086 = 100.0%** |
| z range | **0.4340 – 0.4364** (the stone spans 0.4340 – 0.4993) |
| within 0.010 of the stone mask's BOTTOM edge | **1,086 = 100.0%** |
| their hue BEFORE the rotation | median **76.0**; gold band 42–104 share **100.0%** |

**Every one of them was gold before the rotation.** The geometric stone mask's lower bound
(z ≥ 0.4340) clips the bezel's lower arc where the **gold collar's** paint sits — the
derivation's own §6 rim finding (twin 0's rim at hue 70.9 was the collar's contribution, not
lavender). Rotating gold by +34 to +55° lands it in 104–290, and it is visible at 6× as a
thin green line at the collar junction.

**The palette gate is REPORT-ONLY (Ruling 17), so this reports rather than halts** — 5.65% of
the stone's above-floor set, one structure boundary, fully characterised. The obvious repairs
(raise the mask's lower bound, or exclude gold-band pixels from the rotation) are a ruling's,
not mine.

## 6. The deep-share read, with location

| | after | stage 1b |
|---|---|---|
| lavender-rim band (292–314, C\* > 12) among styled | **19,530 = 1.179%** | 24,513 = 1.479% |
| of those, interior (survive erode-2) | 5,257 = 26.92% | 7,099 = 28.96% |
| all styled that are interior | 32.86% | 32.86% |

| where the band sits | texels | share of the band | of that structure's styled |
|---|---|---|---|
| L5 the stone | **133** | 0.68% | 0.153% |
| L3 pommel collar | 0 | 0.00% | — |
| L4 grip wrap + mid ring | 0 | 0.00% | — |
| L2/L3 the CROSSING | 1,474 | 7.55% | 0.877% |
| **L1 the blade** | **17,923** | **91.77%** | 1.419% |

**On the stone the lavender band fell 5,116 → 133 texels.** What remains is 91.8% blade — the
known rim-mixing class, unrelated to the stone.

## 7. Stroke 1 re-entered (Ruling 25f) — hole-fill only, budget reset

The job mask returned to **8,742 px, +0 / −0 against the pre-demotion mask** — the stone is
out of the stroke's territory exactly as ruled (it was 10,162 with the stone demoted).

| | |
|---|---|
| seed | 770700, budget reset (the spent rolls belonged to the merged spec) |
| pre-flight | **PASS** — five recipe values, the inverted no-LoRA scan (16 nodes, no loader, UNET direct), lane corroboration, prompt provenance |
| link topology | CLEAN — no self-links, no dangling targets |
| `estimate_credits` | **0 credits** |
| prompt_id | `b4fda1e3-f801-4cf5-85db-5bb240af70cd` |
| invariance ANDON | **PASS** — mean 0.049 lv, largest hot component 40 px |

### The eye gate, all watches measured on the 8,742 newly-painted px

| watch | measured | verdict |
|---|---|---|
| **red outside L5** | 132 above-floor px in the wine band: **81.1% on the wrap's own rows**, 18.9% at the collar, **0 on the crossing, 0 on the blade** | **CLEAN** — oxblood owns that band |
| **12e gold** | 1,257 gold-band px, rows p10 145 / median 216 / p90 314 — the collar, mid-ring and boss | **CLEAN** |
| **the fifth signature** | 29.1% of the fill is dark + desaturated, against the emitted context's own **31.8%** | **CLEAN** — less, not more |
| **20b misbinding** | the crossguard at 4× is the same crossguard; no crossguard-like or figurative form anywhere | **CLEAN** |
| **the gem (25f's check)** | unchanged and rendering garnet as context | **CLEAN** |
| forbidden 104–290 | 15 px (1.0% of above-floor) | negligible |

**Committed: 4,344 texels; holes 2,005,056 → 2,000,712.**

### 7b. ⚠ The selftest probe over-estimates a real stroke by 1.75×

Handoff 7's probe measured yaw 0 at **7,591** committed texels; the real stroke committed
**4,344**. The probe fake-inpaints by Gaussian blur, which preserves the figure's own colours
so its keyed figure mask is close to the emitted render's; a real inpaint changes colours at
the rim, shrinking the keyed figure and pushing more texels below `edge-dist 4`.

**So the lane's 69,239-texel achievable set is an upper bound, not a forecast** — the same
denominator discipline as Ruling 22b's reach-vs-paint, arriving one layer further in. Reported
now rather than discovered at HALT 2.

## 8. What has NOT been done

- **Strokes 2–8 have not run.** The dispatch scoped this to the gate, the M2 run, the report
  and stroke 1's re-entry; the ruled order continues `180 → 45 → 225 → 315 → 135 → 90 → 270`
  and HALT 2 comes after it.
- No profile, fixture or palette edit; no memory-store write; no gate armed; no finalize, no
  pack beyond the render GLB.
- The demotion's compensator stands exercised and unused; `state0/` is pristine.
- Zero credits across every submission in this session.

## 9. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The rotations asserted against the ruling before the corrected run; both atlas SHAs recorded either side of the write; the graph saved with its cloud input names so the file is the submitted recipe; prompt_id recorded |
| ANDON_AUTHORITY | **3** | The works-perfectly gate ran first and passed pixel-identically; the restricted write asserts its three invariances before any byte; the commit ANDON untouched; the invariance ANDON passed; my own L-preservation reading was re-measured on a fixed set before it was reported |
| NAMED_COMPENSATORS | **3** | Zero credits; the demotion's compensator exercised and standing; the pre-stroke state copied forward rather than consumed; the corrected twins beside their inputs |
| DECOMPOSE_BY_SECRETS | **3** | The +1,374 keying side-effect separated from the intended change by the restriction and reported; the forbidden-band rise located to one structure boundary and one prior band rather than reported as a total; the deep-share read given with location |
| UNCERTAINTY_GATED_HUMANS | **3** | The forbidden-band defect goes up characterised with its repairs named but not chosen; the probe's 1.75× optimism surfaced now rather than at HALT 2 |
| EXTERNAL_VERIFIER | **2** | The gate compares against the shipped projector's own prior output; the reference is the accepted pair; the watches are measured by band instruments the brush did not write. `skip:` per precedent |

---

## Where this leaves the lane

**The stone is garnet, by arithmetic that cannot touch form** — median hue 308.6 → 22.5, wine
15.04% → 57.38%, lav+mag 70.51% → 18.88%, C\* unchanged, L preserved to 0.088 per texel, every
facet and the bezel intact. The 19b partition that was 305° apart is now 6.6° apart.

**One bounded defect is on the record**: 1,086 texels of gold rotated into the forbidden band
at the stone mask's lower edge, 100% located, report-only by Ruling 17.

**Stroke 1 is committed** with every watch clean and 4,344 texels banked. Seven strokes remain
in the ruled order before HALT 2.
