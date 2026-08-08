# E14 — THE GARNET RE-PROJECTION: the derivation. HALT for the operands ruling.

**Executor session, 2026-08-08.** Ruling 25 (`5e31276`) took the stone off the generation
path; this derives the transfer operands, the per-view stone masks and the projection
mechanism per 25d/25e. **Proposes; adopts nothing. Zero generation, zero credits, nothing
committed.**

---

## 1. ⚠ THE ANCHOR RAN FIRST (25e iv)

Before any operand was proposed: reproduce stage 1b's stone paint from the **recorded**
operands with the **uncorrected** twins — for every demoted texel, sample its recorded owner
view's twin at the recorded projected pixel, and compare against the stage-1b atlas. If a
masked re-projection cannot reproduce the paint it is replacing, nothing it produces is
trustworthy.

```
[frame] h_ext 0.282186  v_ext 1.203993   (stage 1b logged 0.282186 / 1.203993)   asserted
[anchor] demoted territory 67,904 texels — asserted against Ruling 24f
```

| owner view | texels | median ΔE | p90 ΔE | resample hue | atlas hue |
|---|---|---|---|---|---|
| 1 | 16,477 | 1.067 | 4.443 | 317.1 | 315.6 |
| 3 | 18,555 | 0.905 | 4.043 | 333.6 | 334.4 |
| 5 | 17,720 | 1.221 | 3.768 | 315.5 | 313.9 |
| 7 | 15,152 | 0.775 | 2.908 | 327.3 | 326.6 |
| **ALL** | **67,904** | **1.003** | 3.750 | | |

**The recorded-mask resample reproduces the stage-1b stone at median ΔE 1.003** — *smaller
than the step it omits*: handoff 5 measured the facing-weighted-blend → finished-atlas
distance at median ΔE 2.13 on this same stone. The residual is the blend and the σ = 16
levelling, not an error in the mechanism.

## 2. The per-view stone masks — geometry, not a key, not a row band

A pixel is stone if its first-hit point has z ≥ the landmark (0.4340, asserted unchanged).
The row band is retired for this structure (Ruling 25b: it contains the gold collar).

| view | 0 | 1 | 3 | 4 | 5 | 7 | reference (pair v0) |
|---|---|---|---|---|---|---|---|
| figure px | 49,775 | 40,101 | 40,331 | 49,775 | 40,101 | 40,331 | — |
| **stone px** | 1,863 | 1,868 | 1,866 | 1,863 | 1,868 | 1,866 | **1,863** |

The reference is the **accepted pair's view 0** (`PAIR_swordclay_0.png`) under the same
geometric mask — same frame, same landmark, so the operand populations are commensurable by
construction.

## 3. ⚠ TWO SELF-CAUGHT ERRORS IN MY OWN INSTRUMENT, both the same law

**(i) Below a chroma floor, hue is not a colour.** My first draft computed the operands over
the **whole** stone mask and its own output exposed it: the reference read median hue 303.4
at median chroma **3.8**, and the transferred drift views landed at hue **107.7 / 43.2 /
121.4 / 48.9** — green and yellow — with chroma *falling* from ~6.3 to ~3.3. It would have
**desaturated** the stone. Cause: the stone mask is bimodal — 71–85% dark near-achromatic
bezel and facet shadow, 15–28% chromatic body — so a moment transfer over all of it is
dominated by pixels whose hue is undefined.

**(ii) Hue is an angle on a circle.** With the floor applied, the rotation still reported
twin 4 moving **+49.1°** when a garnet stone at 19.6 should move ≈ −5 to reach the reference.
Cause: garnet straddles the 0/360 wrap, so an *arithmetic* median of hue angles is not the
median direction. Every hue centre below is now a **circular mean** — the angle of the summed
unit chromatic vector.

Both were visible only because the instrument printed the *after* state instead of asserting
the transfer had worked. Neither number left the script.

### The population at the ruled floor, with denominators (the D8 lesson, 25e i)

| panel | stone px | above C\* 12 | share | C\* median | circular hue (above floor) |
|---|---|---|---|---|---|
| **REFERENCE — pair view 0** | 1,863 | **277** | 14.9% | 19.87 | **8.18** |
| twin 0 (garnet seed) | 1,863 | 276 | 14.8% | 18.61 | 33.65 |
| twin 4 (garnet seed) | 1,863 | 388 | 20.8% | 20.23 | 16.54 |
| twin 1 (drift) | 1,868 | 521 | 27.9% | 20.57 | 316.39 |
| twin 3 (drift) | 1,866 | 410 | 22.0% | 26.12 | 333.71 |
| twin 5 (drift) | 1,868 | 451 | 24.1% | 16.84 | 312.73 |
| twin 7 (drift) | 1,866 | 397 | 21.3% | 21.03 | 320.17 |

**The chromatic body of the stone is 277–521 px per view.** Named, not hidden in a ratio.

## 4. The three candidate treatments — L preserved in all three

| | what it does | drift views land at | near-no-op on twin 4 |
|---|---|---|---|
| **T1** Reinhard on a,b (mean + σ) | matches both moments | hue 21.0 / 24.2 / 16.1 / 23.5, **C\* moved** | median ΔE 5.948 |
| **T2** mean-only on a,b | matches the first moment | hue 26.7 / **67.7** / 17.3 / **60.1** — unstable | median ΔE 5.064 |
| **T3** hue rotation, C\* and L preserved | **Ruling 25d's own words as arithmetic** | **8.18, residual 0.000 by construction** | **median ΔE 0.760** |

### T3, measured

| view | n > floor | hue before | rotation | hue after | residual | C\* before → after | L\* before → after | median ΔE |
|---|---|---|---|---|---|---|---|---|
| 1 | 521 | 316.39 | **+51.80** | 8.18 | −0.000 | 20.57 → 20.57 | 23.11 → 23.11 | 5.476 |
| 3 | 410 | 333.71 | **+34.47** | 8.18 | −0.000 | 26.12 → 26.12 | 25.21 → 25.21 | 3.712 |
| 5 | 451 | 312.73 | **+55.45** | 8.18 | −0.000 | 16.84 → 16.84 | 23.40 → 23.40 | 4.622 |
| 7 | 397 | 320.17 | **+48.01** | 8.18 | −0.000 | 21.03 → 21.03 | 29.59 → 29.59 | 4.953 |
| 0 (ref seed) | 276 | 33.65 | −25.46 | 8.18 | −0.000 | 18.61 → 18.61 | 9.66 → 9.66 | 2.143 |
| 4 (garnet) | 388 | 16.54 | **−8.36** | 8.18 | +0.000 | 20.23 → 20.23 | 7.21 → 7.21 | **0.760** |

**C\* and L\* are identical before and after in every row** — a rotation cannot move either,
and the columns are printed as the check rather than the claim.

## 5. The near-no-op validation (25e i)

| view | stone px | above floor | rotation | median ΔE | p90 ΔE |
|---|---|---|---|---|---|
| **twin 4** — the other garnet twin, not the reference | 1,863 | 388 | **−8.36°** | **0.760** | 3.006 |
| twin 0 — the reference's seed, a different roll | 1,863 | 276 | −25.46° | 2.143 | 6.727 |
| *for contrast, the four drift views* | | | **+34.5 to +55.5°** | 3.7–5.5 | 16–21 |

**Twin 4 is the honest near-no-op and it passes**: a stone already in the reference's family
moves 8° and 0.760 ΔE. `GARNET_nearnoop_6x.png` shows before/after indistinguishable by eye.

**One thing the validation surfaced that is worth the ruling's attention:** twin 0 and the
reference are *the same view at the same seed* and sit **25° apart** — they are different
rolls. **So the near-no-op floor for this transfer is ~25°, not zero**, and the drift views'
34–55° rotations should be read against that floor, not against 0.

## 6. The rim band, separately (25e iii)

| view | interior px | rim 2 px | int > floor | rim > floor | interior hue | rim hue | Δ |
|---|---|---|---|---|---|---|---|
| 1 | 1,465 | 403 | 328 | 193 | 315.2 | 319.0 | −3.8 |
| 3 | 1,463 | 403 | 240 | 170 | 338.4 | 324.4 | +14.0 |
| 5 | 1,465 | 403 | 266 | 185 | 308.7 | 320.4 | −11.7 |
| 7 | 1,463 | 403 | 267 | 130 | 321.5 | 316.6 | +4.9 |
| **0** | 1,457 | 406 | 206 | 70 | 25.5 | **70.9** | **−45.3** |
| **4** | 1,457 | 406 | 315 | 73 | 11.6 | **58.0** | **−46.4** |

**On the garnet twins the rim sits ~45° off its own interior; on the drift twins ≤ 14°.** The
rim is where backdrop bleed lives and it is present in the reference too — so a reference
population that includes the rim carries the backdrop's contribution into the operand.
Measured both ways; adopted neither. **The operands above use the whole stone mask above the
floor, rim included** — stated plainly because it is a choice the ruling may reverse.

## 7. The projection mechanism — two variants, with the gap measured

Both restrict writes to the demoted stone territory; both leave A32 untouched (the territory
is holes, so the ordinary guard semantics apply unchanged).

| | mechanism | anchor | what it omits |
|---|---|---|---|
| **M1** | recorded-mask resample: each demoted texel takes its **recorded stage-1b owner's** corrected twin at the recorded projected pixel | measured above: reproduces stage 1b at **median ΔE 1.003** | the facing-weighted blend and the σ = 16 levelling — so the stone would carry raw owner colour while every neighbouring texel carries blended, levelled colour |
| **M2** | full re-projection through `project_twins` with the corrected twins, writing only the stone territory | **exact by construction** — run with UNCORRECTED twins it must reproduce `stage1b_atlas.png` pixel-identically, which is the works-perfectly test to run before adoption | nothing; the operand is the shipped spine |

**M2 is the one I propose**, on the route's own law — *prefer eliminating a risk to gating
it*: it makes the stone's treatment identical to every other texel's by construction, so
"does the stone match its neighbours' processing" stops being a question. M1's measurement is
the evidence for why the distinction is not cosmetic: **median ΔE 1.003 of unblended,
unlevelled difference across 67,904 texels.** The choice is the ruling's.

**Invariance conditions I propose for whichever is ruled** (printed, not asserted-in-prose):
styled texels outside the ruled stone mask byte-identical before/after; the write set exactly
the demoted mask ∩ holes; the atlas's own SHA before/after recorded; the compensator named
(restore the stone mask's three channels from `state0/`, the demotion's own inverse, already
exercised).

## 8. What the ruling has to decide

1. **The treatment**: T1 / T2 / **T3**. T3 is 25d's own language as arithmetic and is the
   only one whose near-no-op is a near-no-op.
2. **The operand population**: whole stone mask above the floor (what §4 used), or interior
   only (§6 shows the rim is ~45° off on the garnet references).
3. **Chroma**: T3 preserves each twin's own C\*, so twin 3 lands at C\* 26.1 against the
   reference's 19.9 — the right hue at its own saturation. Whether chroma should also be
   matched is a real operand question and is not answered here.
4. **The hue statistic**: circular mean **unweighted (8.18)** or **chroma-weighted (11.80)**.
   Both are computed; the tables use unweighted.
5. **M1 or M2**, per §7.

## 9. What has NOT been done

- **Zero generation, zero credits.** No cloud call of any kind.
- **Nothing committed, nothing adopted.** The run state is untouched since the stroke-1 halt;
  `run/state/atlas.png` is still byte-identical to `state0/atlas.png`.
- **Corrected twins are written BESIDE, never over** (`garnet/corrected/`), and outside the
  stone mask every pixel is **asserted** byte-identical to its input — a Lab round trip is not
  the identity on 8-bit data, so the untouched region is copied, not reconstructed.
- No profile, fixture or palette edit; no memory-store write; no gate armed. Stroke 2 has not
  launched and stroke 1 has not re-entered.

## 10. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The anchor ran before any operand existed and asserted the frame against stage 1b's logged extents; every operand recorded per view with its population size in JSON; the rotations saved as their own array |
| ANDON_AUTHORITY | **3** | Two errors in my own instrument caught and corrected before proposing — the chroma floor and the circular statistic; the outside-mask byte-identity is asserted, not intended; the demoted count asserted against 24f; the landmark asserted unchanged |
| NAMED_COMPENSATORS | **3** | Nothing irreversible: writes are confined to a new `garnet/` tree; the corrected twins sit beside their inputs; the demotion's compensator remains exercised and unused |
| DECOMPOSE_BY_SECRETS | **3** | Operand population separated from mask (a mask is geometry, a population is chromatic); rim separated from interior; the mechanism's blend/levelling contribution separated from the resample by measurement rather than by assumption |
| UNCERTAINTY_GATED_HUMANS | **3** | Five named decisions go up with both readings and their costs; the ~25° near-no-op floor is surfaced as the denominator the drift rotations should be read against, rather than letting 0 be assumed |
| EXTERNAL_VERIFIER | **2** | The anchor checks the mechanism against the shipped pipeline's own output; the reference is the accepted pair, an artifact this session did not make; the corrected stones are judged by eye at 6×, not by the moments the transfer matches by construction. `skip:` per precedent |

---

## HALT — the operands ruling

`E:\AI\training\facet_next\E14_strokes\garnet\`:

```
garnet_derivation.json          the anchor + masks + the first (superseded) operand pass
garnet_operands.json            the floor-corrected pass, three treatments
garnet_operands_final.json      ⭐ the circular-statistics pass — the operands as proposed
T3_rotations.npy                the six per-view rotations
stone_masks_twinspace.npy       the six geometric stone masks
corrected/TWIN_swordclay_{0,1,3,4,5,7}_garnet.png   T3 applied, beside the inputs
corrected_readout.json          8-bit round-trip check per view
GARNET_corrected_6x.png         ⭐ the four drift stones before/after, beside the identity
GARNET_nearnoop_6x.png          ⭐ the near-no-op controls at 6×
```

**Three things want the eye and five want the ruling:**

1. **The corrected stones at 6×** — the four drift twins land deep garnet-red with **every
   facet, the bezel, the highlight and the shading intact**, because the rotation cannot
   touch L or C\*. This is the property the generation path destroyed twice.

2. **The near-no-op passes** — twin 4 rotates 8.4° and moves ΔE 0.760 over 388 above-floor px
   of 1,863. And it carries its own caveat: twin 0 against the reference is 25° apart at the
   same seed, so **~25° is the floor, not zero**.

3. **The rim is ~45° off its interior on the garnet references** and ≤ 14° on the drift ones —
   the operand population question is not cosmetic.

The five decisions are §8. **The mechanism I propose is M2** — full re-projection through the
spine, whose works-perfectly test (uncorrected twins reproducing `stage1b_atlas.png`
pixel-identically) I have **not** run, because it belongs after the treatment is ruled and
running it now would prejudge which twins go in.
