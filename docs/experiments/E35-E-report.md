# E35 — E1/E2, executor report: the 2509 route measured at last

**Run 2026-08-14 at the Director's go.** Bands registered in three blocks, each pushed before
the work it covers: E1 at `41a227a`, E2 at `bc58602`, E2's **class** bands at `3593b1b`
(after seeing the image, before any instrument ran — disclosed as such).

**Two jobs. 44 → 46 of 60.**

**The arc's question is answered.** A working native-framed 2509 configuration exists, and
measured against the recorded twin: **both defect classes are worse**, the register is
stronger, and the silhouette tracks better with no ControlNet at all.

---

## 1. The corruption, closed

| job | input at 672×1568 | result |
|---|---|---|
| A2 | recorded 352 clay, resized **by the node** | clean |
| A3a/b/c, D1 | **native** render | corrupt ×4 |
| **E1** | recorded 352 clay, resized **locally**, node no-ops | **clean** |
| **E2** | **native** render, lanczos round-tripped, node no-ops | **clean** |

- **E1 killed traversal.** Content-equivalent pixels arriving as a file the node no-ops on
  came back clean, so it is not the node's processing that matters — it is the pixels.
- **E2 killed framing.** The native framing, unchanged, with only the interpolation character
  altered, came back clean.

**The trigger is the interpolation character of the input.** The native Workbench render
carries **2,620 unique colours**; every input that worked carries ~5,000+ (E1 5,046, E2
5,336). A flat-shaded, heavily-quantised render is the off-distribution case; one lanczos
round-trip fixes it. Framing, alpha, bit depth, colour type, seed and the turbo switch are
all exonerated, each by a measurement.

⚠ **This is a trigger, not a mechanism.** Why quantisation degenerates the latent is not
established, and no job here could establish it.

## 2. The classes, measured — the arc's first 2509 numbers

Instruments at derived parameters (linear 1.53125 / area 2.34473, from the ratios and nothing
else): mask `armclay672mask_1.png`, head `slice(92,337)` — **crown included** — census
`--blob-max-px2 84 --small-px2 21 --window 23`, pale `--min-area 59 --window 47`. Both
instrument anchors re-verified after their edits.

| | recorded r3 (352×1024) | E2 (672×1568) | like-for-like |
|---|---|---|---|
| pale area | 278 px² | **2,323 px²** | **3.6× worse** (991 scale-equivalent) |
| pale L\*-rise | 4.97 | **13.29** | worse |
| pale C\* (chroma split) | 23.25 | **36.30** | **signature (ii)**, no collapse |
| dark census count | 16 | **734** | — (count does not scale cleanly) |
| dark area as **% of figure** | 0.1717% | **1.8334%** | **10.7× worse** — scale-free |
| register C\* | 23.77 | **37.53** | **stronger** |
| reg-IoU | 0.9372 | **0.9611** | **better, with NO ControlNet** |

**2509 does not fix either class. It makes both worse**, and buys a more saturated register
and better silhouette fidelity from the edit reference alone.

⚠ **Two limits on this reading, both stated in the bands before the numbers.** This is
**2509 + the Lightning LoRA** (turbo default, 4 steps, cfg 1.0) — R3 as the Director ruled it
says **NO LoRA**, so a turbo-off run measures a different thing. And the dark census is
inflated by content: the herringbone hatching is rendered far heavier than the recorded
twin's and its grooves fragment into components. **Some of that 734 is the prompt's own
`sculpted thumbprint hatching` term rendered literally, not the defect class the arc has been
chasing.** The scale-free area fraction (10.7×) carries the same content contamination.

## 3. Bands, scored

**E1** — 2 of 2 hit. P1 clean at 0.75; P3 resembles A2 (mean |Δ| 1.70) without pixel-identity.

**E2 mechanical** — P1 clean at 0.6 (**against framing**, correctly); P3 hit: the classes
became measurable for the first time in the arc.

**E2 class bands** — **2 hit, 3 miss, 1 unmeasurable**:

| band | predicted | measured | verdict |
|---|---|---|---|
| C1 register survives, C\* ≥ 15, band 18–32 | 18–32 | **37.53** | **SPLIT** — the ≥15 clause hit, the band missed high |
| C2 dark census rises, band 18–60 | 18–60 | **734** | **MISS** — direction right, magnitude 12× outside |
| C3 pale is LOW, band 0–250 | 0–250 | **2,323** | **MISS** |
| C4 chroma split lands (ii), pale C\* > 15 | (ii) | **36.30** | **HIT** |
| C5 reg-IoU ≥ 0.85 | ≥ 0.85 | **0.9611** | **HIT** |
| C6 identity has moved | moved | it has | unmeasurable; the Director's eye |

**C3 is my fourth consecutive pale-direction miss, and this one is worse than the other
three.** I was not blind — I had looked at the image and wrote *"the crown reads evenly toned
to my eye and there is no visible wash."* The measurement says 2,323 px², 3.6× the recorded
twin scale-equivalent. **My eye called the class absent on a figure carrying more of it than
anything the arc has measured.** The previous three misses were reasoning errors about
mechanism; this one is a perception error about a defect I have been looking at all day, and
it is the strongest argument yet that the pale class is not reliably visible to me at the
scale I am judging it.

**C1's split is worth its own line.** Ruling 8 folded the register term as a floor — *did the
register survive* — and as a floor it worked perfectly. I then attached a two-sided band to
it and missed high, because I predicted 2509 would hold the register rather than intensify
it. **The term should stay a floor; the band I added was my own invention and it is the part
that failed.**

## 4. Errors and instrument work

- **My E1 branch plan's premise failed and I said so before adapting.** It claimed a clean E1
  makes "the true A3" runnable; it does not — E1 was clean on the *resampled* input, so the
  native frame was still untested and the head band still cropped. Following it mechanically
  would have measured a head region missing the crown, which is where the pale class lives.
- **The register instrument's clay path needed two edits, not one.** I exposed `--clay` and
  the first run still broadcast a 352×1024 array against a 672×1568 one — `clay_lab` loaded
  from the module constant. The shape mismatch raised rather than silently comparing, which
  is the right failure. Anchor re-run after the fix: the recorded rows reproduce.
- **Both parameterised instruments re-anchored** after every edit — the pale instrument's six
  R2-c rows and the register instrument's recorded rows, each to the digit.

## 5. Artifacts

```
E:\AI\training\facet_E35\
  k672\armclay_resampled_1.png     E1 input - local replay of the scaler's transform
  k672\armclay672_1_roundtrip.png  E2 input - native framing, lanczos round-trip
  twins\twin_E1_resampled_v1.png  twin_E2_roundtrip_v1.png
  diag\e2_pale.json  e2_census.json  e2_register.json
  diag\E35_E2_sheet.png  E35_E2_head3x.png
```

E1 `04daafe9-ed4e-4631-a33e-6a54ac1b162f` · E2 `385383de-a75e-4b71-8b57-43ae4fa1f89e`.

## 6. HALT

**46 of 60**, fourteen remain. As pre-registered: no further jobs.

**The one job I would take next, named and not taken:** the same round-tripped input with
**turbo OFF, no LoRA** (20 steps at the template's non-turbo settings) — because R3 rules NO
LoRA and every number above carries one. It would separate 2509 from Lightning and cost one
job. **On the Director's word, not mine.**

The eight-view rebuild still fits the remaining fourteen and is still not mine to launch —
and on these numbers there is no case for it: the route this arc was testing makes both
classes worse.
