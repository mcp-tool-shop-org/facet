# E12 handoff 10 — blind predictions

**Written BEFORE anything in this dispatch runs**: before the v7 rebuild, before any upload or
submission, and before any v7 artifact exists. Committed first so nothing here can be edited
against a result.

## Blind status — disclosed precisely

This is the holding handoff-9 session. **It generated the v6 twins and has seen view 4 at full
size**, including `AB_view4_v5_v6.png` and the wing and crown crops at 3×. So view 4's v6
landing is an observed fact to this seat and not a prediction: **arms green, finger struts
cream, crown ivory, wing claws charcoal, membranes grey-to-cream.**

I also hold every v6 number I measured, and they are the baselines this dispatch reads against:

| view 4, v6 | value |
|---|---|
| whole-figure ivory mass | 68,023 px (v5 was 96,197) |
| gate off-palette | 7.14%, blob 9,392, shoulder **99.6%**, membrane 0.2%, seam 0.0% |
| achromatic mass | 3.74%, largest component 2,848 |
| registration IoU | 0.985585 |
| claws ivory:charcoal | 0.07 (ivory 675, charcoal 9,724) |
| crown-only box | 41.0% ivory |

**What does not exist and cannot have been seen: any v7 artifact.** The prediction is about one
noun-phrase split on one view.

---

## Pre-registered derivations

The split-term entry is **19 comma-terms** — `moss-green wing arms and finger struts` replaced by
`moss-green wing arms` + `moss-green wing finger struts` at indices 2 and 3. The drop map is
unchanged and names neither.

| | prediction |
|---|---|
| entry terms | **19** |
| per-view counts | **19 / 19 / 19 / 13 / 15 / 13 / 19 / 19**, `headclay_0` **17** — each exactly one more than v6 |
| full-string views | **0, 1, 2, 6, 7** — unchanged |
| the ANDON | remove **both** new terms from a v7 stem and remove the **one** compound term from the matching v6 stem; the two remainders must be **byte-equal**. That asserts the construction rather than my intention, per the dispatch |
| inputs | clay `bd620f8d` and control `460488dc` must return as handoff 8/9's names. A different name is a halt |

## The works-perfectly test

**The seed is pinned at 770700**, the same seed v6 ran. If the split changes nothing, v7
reproduces the v6 view-4 twin near-exactly — so **any broad change is signal**, and the finger
struts are the register to read first.

**Lands** → the struts read moss-green like the arms, and the whole-figure ivory mass falls
toward view 0's v6 value of 31,601 px. **Does nothing** → ivory mass within ±10% of 68,023 and
the struts still cream at 3×.

---

## The predictions

### P1 — the struts land green; view 0-class FULL binding

**P1a — predicted: full binding.** Confidence **moderate**. The reasoning is the head-noun
account Ruling 18c ruled on: in v6 the compound phrase's head noun (`wing arms`) bound and its
second conjunct under-bound. Giving the struts their own noun phrase is exactly the construction
that has worked every time in this arc — `charcoal claws` is its own phrase and bound on view 4
while the unnamed arms beside it did not. Amendment 15 permits naming an *unoccupied* surface,
and the struts' cream is a neighbour's colour rather than a declared owner.

**Against it, and this is why confidence is only moderate:** view 4 is the archetypal bat-skeleton
presentation, its stem still carries two `bone-ivory` terms, and it is the one place the anatomy
prior has already beaten a term once.

**P1b — quantified: whole-figure ivory mass 68,023 → ≤ 40,000 px** (a ≥ 40% fall). *Does
nothing* → within ±10% of 68,023, i.e. 61,000–75,000.

**P1c — the branch, pre-registered by 18c and restated here so neither outcome is improvised:**
struts green → the twin set completes. Struts still cream → **the positive-naming lever is
exhausted on this presentation**, and the decision goes to the Director with 18c's two named
options (a subject-level negative term earned the W3 way, or accepting cream struts as the rear
presentation's realised form). **I will not propose a third naming variant** — that would be
tuning a term against the artifact it is judged on.

### P2 — the gate rises a THIRD time, and I am registering it as confirmation

Ivory sits at h 96.4, **inside** the adopted warm-olive band; the hide's deeper greens land past
its 147.3 edge, in the shoulder. So converting a large ivory structure to green moves mass from
inside the band to outside it. This happened on view 3's re-roll (0.36% → 11.11%) and on both v6
views (13.37% → 18.78%, 1.68% → 7.14%).

**Predicted: view 4's gate rises from 7.14% to 10–20%, with shoulder ≥ 95% of the off-palette.**
Registered now so that a third inversion reads as confirmation of a known mechanism rather than
as a surprise — and so that a *fall* would be the informative outcome instead.

### P3 — regressions, scored across every element

- **P3a — the crown holds at ~41%** on the crown-only box (777,216)–(953,388). **Reported, not
  acted on**: Ruling 18g sends D5 to Gate 1 on the asset. Predicted 38–44%.
- **P3b — the claws stay charcoal**, ratio ≤ 0.10 (v6 was 0.07).
- **P3c — the membranes stay grey-to-cream** on this view. View 0's v6 warm-tan trailing field is
  a different view's landing and is not predicted here.
- **P3d — achromatic mass 2–6% with largest component under 5,000** (v6: 3.74% / 2,848).
- **P3e — registration 0.975–0.990** (v6: 0.9856). **And per Ruling 18e's banked caveat, if it
  shifts materially I check the inside/outside split of the newly-keyed pixels before inferring
  anything about the silhouette** — my own ±0.005 inference rule was falsified last session and
  is not reused.

### P4 — process

- **P4a** — both uploads return the recorded content-hash names.
- **P4b** — **0 credits**, `estimate_credits` before the submission.
- **P4c** — **0 re-rolls needed.** Confidence moderate; the likeliest consumer is an achromatic
  mass of the view-3A kind, which is a seed lottery unrelated to the term.
- **P4d** — the v7 ANDON passes on all nine stems.

---

## What would make this dispatch a full success while P1 fails

If the struts come back cream under their own noun phrase, that is a **clean negative and a full
success**: it closes the positive-naming lever on this presentation with two data points
(compound term, split term) on one view at one pinned seed, and it hands the Director a bounded
choice rather than an open question. It would also sharpen the arc's founding law — *identity
rides the prompt* — with its first measured boundary: **a named surface can still lose to a
strong enough anatomical prior on the presentation that most invokes it.** Reported plainly and
stopped there.
