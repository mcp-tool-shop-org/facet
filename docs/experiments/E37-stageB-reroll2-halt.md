# E37 Ruling 14 round 2 — HALT: v7's roll is a RESULT, v3's third roll improves and stays outside

**Seat:** executor · **Date:** 2026-08-15 · **Spend: 30 → 32 of 80** (2 jobs, exactly as
authorized; ceiling raised at the Director's word, Ruling 14 clause 2).

Pre-registration, written **before either payload was emitted and before anything
submitted**: `E:\AI\training\facet_E37\reroll2_preregistration.md`.

---

## 1. What was fired

Seeds from a rule stated before use — **`20260815 * 100 + view`**, the round moved into the
multiplier because round 1's `×10` rule had already burnt `202608153` on v3's second roll.
Ten digits = round 2, nine = round 1, readable from the number alone.

| view | roll | seed | verified against the payload that produced the failing twin |
|---|---|---|---|
| 3 | **third** (his word, clause 3) | **2026081503** | only `13.inputs.seed` + `15.inputs.filename_prefix` moved |
| 7 | **first** | **2026081507** | only `13.inputs.seed` + `15.inputs.filename_prefix` moved |

The check asserts the seed **did** move before asserting nothing else did, so it cannot pass
vacuously. Prompt v-w1, tuned controls, recorded recipe and 368×1024 byte-held.

**Ledger:** probe+confirm 3 · seed sets 24 · re-roll round 1 (v1,v3,v6) 3 · **round 2 (v3,v7)
2** = **32 of 80**.

## 2. ⚠ THE ANDON — v7's roll, and it is a RESULT under clause 3

`t2_register_all.py`, the Stage-B registration key, on `sets/reroll2/twin_v7.png`:

```
ANDON: keyed figure spans the whole frame for ...\sets\reroll2\twin_v7.png
ANDON: register on re-roll v7 failed (exit 1)
```

**The instrument declined to produce a number.** This is the broken-key signature this
record already names — *a figure cannot be 751 px wide in a 752 px frame when the mesh is
388* — and it is the twin's backdrop, not the instrument:

| twin | figure coverage of frame | sampled background |
|---|---|---|
| v7 old 770700 | 45.61% | 196.6 |
| v3 old 770700 | 45.12% | 195.8 |
| v3 roll 2 | 45.70% | 181.3 |
| v3 roll 3 | 30.05% | 189.8 |
| **v7 roll 1 (2026081507)** | **80.30%** | **133.1** |

Measured by `montage.py`'s own figure/background readout. **The prompt asks for a "plain pale
grey background"; this roll painted a darker, gradient studio backdrop** — sampled corner
133.1 against ~190–197 on every other twin in the arc — so a key that separates figure from a
plain field cannot separate this one.

**Its dark census is independently the worst in the arc**, and that number is unaffected by
the backdrop because the census keys off the supplied geometry mask:

| | count | area px² | largest |
|---|---|---|---|
| v7 old 770700 | 24 | 86 | 14 |
| **v7 roll 1** | **138** | **349** | 19 |
| *previous arc worst (v6 at 770700)* | *55* | *252* | *29* |

**Two independent failures on one roll.** Ruling 14 clause 3: *a further failure on either
view is a RESULT — halt, it returns to him.* **Halted.** The projection key was **not**
measured on either arrival: running `project_twins` after this ANDON would be proceeding past
a fired gate, and clause 3 halts rather than continues.

## 3. v3's third roll — measured, improved, still outside

| | reg-IoU (Stage-B key) | register C\* | dark count / area | keyed px |
|---|---|---|---|---|
| v3 old 770700 | 0.9350 | 29.98 | 8 / 49 | 96,148 |
| v3 roll 2 (202608153) | 0.9440 | **46.24** | 34 / 247 | — |
| **v3 roll 3 (2026081503)** | **0.9291** | **39.97** | **15 / 71** | 97,053 |

Its second-roll defects both move toward the kept set — **C\* 46.24 → 39.97** and dark census
**34/247 → 15/71** — and it remains **outside the kept-five C\* range [23.30, 29.90]**.
`within_dE10_of_clay_pct` 0.247, `median_dE_to_clay` 45.135.

⚠ **The baseline is held fixed and this is why.** The guard computes its kept range from
whichever views are not re-rolled, and with v7 now re-rolled that population would have been
`{0,1,2,4,5,6}` instead of round 1's `{0,2,4,5,7}` — **a moving denominator, the family this
record has been bitten by four times.** Every C\* comparison above is against the **round-1**
range 23.30–29.90, stated so no later reader recomputes it from a different set.

## 4. Prediction scorecard — 0 of 3 scorable, and the reason is itself the result

| # | prediction | live branch | measured | |
|---|---|---|---|---|
| P1 | both new views clear the **projection** floor | both ≥ 0.80 | **NOT MEASURABLE** — the Stage-B key ANDONed on v7 before projection was reached | — |
| P2 | both below 6,000 px keyed outside the silhouette | both | **NOT MEASURABLE** — same reason | — |
| P3 | 0 or 1 of the two land inside the kept C\* range | 0 or 1 | v3 outside; **v7 has no C\*** | **partial** |

The pre-registration named the base rate honestly — two of three round-1 fresh rolls were
clean and one was the worst row in the set, making "both clear" ≈ 44% — and what actually
happened is a failure mode none of the three predictions had a branch for: **a roll whose
backdrop stops an instrument from measuring it at all.** Every band assumed a number would
exist. Recorded as the miss it is.

## 5. Mechanics

The wash guard was **parameterized, not forked** (`--rerolls`/`--subdir`/`--out`, round 1 the
default), and the edit is proven non-perturbing: the default invocation reproduces round 1's
`wash_guard.json` **byte-for-byte**. The payload emitter took the round-2 pairs through the
same single code path it took round 1's.

Sheet: `handoff/E37_stageB_reroll2_vs_v0.png` (1104×1213) — v0 beside both arrivals at native
368×1024, with `not measured` written into v7's register cells rather than left blank.
Lineage: `handoff/_reroll2_check.png` (1840×1050) — v3's three rolls and v7's two, at native.

Receipts: `stageB/payloads_reroll2/` (2) · `stageB/sets/reroll2/twin_v{3,7}.png` (sha256
`7b4e29a6e0b89d96…`, `18f399eae8c1c5ec…`) · `handoff/guard2/` · `handoff/e37_wash_guard2.txt`
· `handoff/guard_anchor/` (the non-perturbation anchor). Job ids
`85c39817-4b72-4475-a32f-1973691e232a` (v3) · `7957a85b-1be9-4487-bcc1-680ece233787` (v7).

No protected tree was written to. No atlas exists. **Spend 32 of 80.**
