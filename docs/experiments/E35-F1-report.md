# E35 — F1, the un-confounding job: executor report

**Run 2026-08-14** at the Director's word ([E35-ruling.md §9](E35-ruling.md)). Bands with the
resolved sampler settings registered at `21da62c`, **before submission**, as ordered.
**One job. 46 → 47 of 60.** No mechanical repeat needed.

**The confound is removed and the verdict does not change.** Lightning was inflating every
number; without it 2509 sits far closer to the recorded route on colour — and still runs
**~2.9× worse on both defect classes.**

---

## 1. The three columns, same instruments

`twin_despeckle --mode census`, the pale instrument and `t2_register_all` on all three —
recorded at 352×1024 with default parameters and its own mask, E2 and F1 at 672×1568 with the
parameters derived from the 1.53125 / 2.34473 ratios and the verified `armclay672mask_1.png`.
Same code paths, parameterised per frame.

| | recorded r3 | E2 (Lightning) | **F1 (no Lightning)** |
|---|---|---|---|
| pale area | 278 | 2,323 | **1,890** |
| pale, scale-equivalent | **278** | 991 | **806** |
| pale L\*-rise | 4.97 | 13.29 | **10.90** |
| pale C\* (chroma split) | 23.25 | 36.30 | **23.24** |
| dark count | 16 | 734 | **413** |
| dark, % of figure | **0.1717%** | 1.8334% | **0.4820%** |
| register C\* | 23.77 | 37.53 | **26.99** |
| reg-IoU | 0.9372 | 0.9611 | **0.9311** |

**Removing Lightning moves everything back toward the recorded route.** Dark area falls
**3.8×** (1.8334% → 0.4820%), pale falls 19%, register C\* comes down from an over-saturated
37.53 to **26.99** against the recorded 23.77 — and the pale region's own chroma lands at
**23.24 against the recorded 23.25**, which is agreement to two decimal places on a quantity
neither run was tuned for.

**And the class verdict is unchanged.** Against the recorded route, un-confounded 2509 is
**2.9× worse on pale** (806 scale-equivalent vs 278) and **2.8× worse on dark** (0.4820% vs
0.1717%). Lightning was making it look four to ten times worse than it is; it is still
worse on both.

⚠ **One content caveat carries over and is smaller now.** Part of the dark census is the
prompt's `sculpted thumbprint hatching` term rendered literally — heavy herringbone grooves
in E2, a finer crazed texture in F1. The 3.8× drop is partly that texture becoming finer, not
only fewer defects. The recorded-route comparison (2.8×) carries the same caveat.

## 2. Bands — 6 of 6 measurable HIT

| band | predicted | measured | verdict |
|---|---|---|---|
| B1 register **floor** C\* ≥ 15 | ≥ 15 | **26.99** | **HIT** |
| B2 pale falls vs E2, band 400–2,000 | 400–2,000 | **1,890** | **HIT** |
| B3 dark census falls sharply, band 100–600 | 100–600 | **413** | **HIT** |
| B4 chroma split stays (ii), pale C\* > 15 | (ii) | **23.24** | **HIT** |
| B5 reg-IoU ≥ 0.90 | ≥ 0.90 | **0.9311** | **HIT** |
| B6 F1 differs from E2 and is less glossy | less glossy | it is; C\* 37.53 → 26.99 | **HIT** |
| B7 identity is still not the recorded man | still not | it is not | the Director's eye |

**B2 is my first pale-direction hit in five attempts, and the reason it hit is the reason
the C3 lesson was folded.** The dispatch forbade eye-claims about pale and I reasoned from
mechanism instead — 20 steps at cfg 4.0 converges further than 4 at cfg 1.0, and the class is
a local lightness excursion, so a more converged render carries less of it. That reasoning
was checkable and it held. **The four misses were all made while looking at the picture; the
hit was made while refusing to.**

**B1 as a floor is the whole of what Ruling 8 folded, and it worked.** The two-sided band I
invented last time is dead and stays dead — 26.99 would have sat outside most upper bounds I
would have chosen, and the floor is the part that carries the meaning.

## 3. The sheet

`facet_E35\diag\E35_F1_three_column.png` — three columns at full size with numbers under
each. `E35_F1_heads.png` — the three head bands, **crown included** in all three.

**For the Director's eye**, and not judged here: identity (F1 is a different man from the
recorded twin, as E2 was), the register at C\* 26.99 against the recorded 23.77, and whether
the finer crazed hatching in F1 reads as the prompt's `sculpted thumbprint hatching` or as
noise. **The class numbers carry the class verdict; those three are yours.**

## 4. What the whole 2509 arc now says

- **It works**, at a native frame, given a lanczos round-trip on the input (E1/E2 closed the
  trigger; the mechanism stays open and platform-side).
- **It tracks the edit reference better than the recorded canny route does** — reg-IoU 0.9311
  with **no ControlNet at all**, against 0.9372 with one, and E2 reached 0.9611.
- **It does not fix either defect class. It is ~2.9× worse on both**, un-confounded.
- **It does not preserve identity.**

## 5. Artifacts

```
E:\AI\training\facet_E35\
  twins\twin_F1_nolightning_v1.png
  diag\f1_census.json  f1_pale.json  f1_register.json
  diag\E35_F1_three_column.png  E35_F1_heads.png
```

F1 prompt_id `5e3d11d2-64bb-4c8b-ac17-c9c69a1f2a31`. Resolved settings, read from the
template's own switch nodes before submitting: euler / simple / **20 steps / cfg 4.0** /
denoise 1.0 / **no LoRA**. E2's census reproduced exactly in the same invocation (734 / 3,929
px² / 1.83344%), so the two columns are one measurement, not two.

## 6. HALT

**47 of 60**, thirteen remain. The close ruling follows the sheet either way. No further job
is named: the un-confounding question is answered, and what is left on the sheet is the
Director's judgement rather than another measurement.
