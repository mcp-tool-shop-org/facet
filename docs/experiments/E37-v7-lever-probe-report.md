# E37 Ruling 16 — the v7 lever probe: three levers, bands sealed, all three arms measure

**Seat:** executor · **Date:** 2026-08-15 · **Spend: 32 → 35 of 80** (3 jobs, exactly as
authorized). Bands sealed before submission:
`E:\AI\training\facet_E37\v7_lever_probe_preregistration.md`.

---

## 1. What flew

**One fresh seed across all three arms** — `20260815007`, from the standing rule
`20260815 * 1000 + view`, so the round is legible in the digit count (9 = round 1, 10 =
round 2, 11 = round 3). No eleven-digit seed existed anywhere in the record.

| arm | the single named delta | diff against `set770700_v7.json` |
|---|---|---|
| **P1** | none — seed only, the control | `13.inputs.seed`, `15.inputs.filename_prefix` |
| **P2** | negative gains `dark background, gradient backdrop, studio backdrop` | + `8.inputs.text` |
| **P3** | `cn_strength` 0.9 → 1.0 | + `11.inputs.strength` |

**P2's delta was authored in a fixture, never typed into a payload** —
`registers/vw1n.json`, transcribed verbatim from Ruling 16, with the positive prompt
asserted byte-identical to `vw1.json` and the base negative asserted to survive as a prefix.

**The emitter was extended, not forked, and the edit is proven non-perturbing**: re-emitting
the recorded 24 payloads returns **all 24 byte-identical**. Its diff-count ANDON now widens
by exactly one per opt-in delta, so a delta that silently failed to apply lands *below* the
band and halts — the count tests the deltas rather than merely permitting them.

## 2. Every arrival measured — the new branch did not fire

Ruling 15's template clause, first use. **B1's live branch HIT: all three key normally.** The
round-2 roll that defeated the register instrument is not reproduced by any arm.

| arm | figure coverage | sampled bg | Stage-B key | **projection key** | dark count / area | C\* | C_in |
|---|---|---|---|---|---|---|---|
| *v7 old 770700* | *45.61%* | *196.6* | *0.9145* | *0.7989 — FIRED* | *24 / 86* | *24.39* | *24.25* |
| *v7 roll 1 (failed)* | *80.30%* | *133.1* | ***ANDON — no number*** | *not run* | *138 / 349* | *—* | *—* |
| **P1** seed-only | 38.93% | 151.1 | 0.9451 | **0.9144** | 72 / 270 | 29.45 | 23.74 |
| **P2** negative clause | 39.92% | **181.4** | 0.9478 | **0.9196** | 71 / 268 | 29.75 | 17.02 |
| **P3** cn 1.0 | **32.22%** | 157.6 | 0.9467 | **0.9106** | **50 / 248** | 29.93 | 25.58 |

**All three clear both keys.** All three land far under 55% coverage against the failure's
80.30% — **B2's live branch HIT**.

⚠ **And the full eight-view projection completed on all three arms, exit 0, no ANDON** —
which also settles the view that halted Stage C twice: **v3's roll 3 registers at y+135 as
0.9158**, against 0.7547 for roll 2 and 0.8394 for the replaced twin.

## 3. Selection — the sealed rule, applied

A row enters candidacy by measuring at all, clearing both keys, and a census in family; ties
break by **lowest total dark census**. All three qualify, so the tie-break decides:

> **P3 is SELECTED — 50 / 248 against 72 / 270 and 71 / 268.**

**Its delta is named on the sheet, not hidden**: `cn_strength` **0.9 → 1.0**. P3 also carries
the lowest figure coverage of the three (32.22%). Its C\* of 29.93 sits **0.03 outside** the
fixed kept-five range — reported by the wash watch, which gates nothing.

## 4. Bands — 3 of 5, and the two misses are the probe's real content

| band | live branch | measured | |
|---|---|---|---|
| B1 | all three measure | all three measure | **HIT** |
| B2 | all three under 55% coverage | 38.93 / 39.92 / 32.22 | **HIT** |
| **B3** | **P1 alone would have sufficed** | **both levers separate from the control** | **MISS** |
| **B4** | 0 or 1 inside the kept C\* range | **2 inside** (29.45, 29.75; P3 at 29.93 out by 0.03) | **MISS** |
| B5 | best arm's count ≤ 60 | P3 at 50 | **HIT** |

**B3 is the miss worth having.** The band predicted — and said so plainly as "the
uncomfortable prediction" — that a fresh seed alone would fix a seed-lottery failure and the
levers would have nothing left to act on. **Measured, both levers moved something P1 did
not:**

- **P3 (conditioning 1.0)** cut the dark census **72 → 50** and figure coverage
  **38.93% → 32.22%** at an identical seed. The predicted direction — anchoring suppresses
  invention — is the direction measured.
- **P2 (the negative clause)** moved the sampled background **151.1 → 181.4**, toward the
  kept twins' ~196, and returned the best projection key of the three (0.9196). The lever
  aimed at backdrop invention moved the backdrop.

Neither is a large effect and neither is claimed as one; what the probe establishes is that
both levers are **live rather than inert**, measured against their own control at a held
seed, which is the thing no prior run had done. B4's miss is in the reassuring direction:
two arms landed inside a range every previous re-roll had missed.

⚠ **Stated as a limit:** one roll per configuration, so each arm is n = 1 and the differences
above are not separated from roll-to-roll variance. The probe shows a direction, not an
effect size.

## 5. HALT — his eye, then projection with the final eight

Sheet: `handoff/E37_v7_lever_probe_vs_v0.png` (1472×1268) — v0 beside all three arms at
native 368×1024, the selected column marked and **its delta written in words**. Comparison
strip: `handoff/_probe_v7.png` (1840×1050) — the old twin, the failed roll, and the three
arms.

**The final eight would be:** v0 · v1 (re-roll 202608151) · v2 · **v3 (roll 3, 2026081503)**
· v4 · v5 · v6 (re-roll 202608156) · **v7 (P3, 20260815007 + cn 1.0)** — three of eight
carrying a named per-view fork, his eye gating all of it.

Receipts: `stageB/payloads_probe/{P1,P2,P3}/` · `stageB/sets/probe{,P1,P2,P3}/` ·
`registers/vw1n.json` · `handoff/guard_{P1,P2,P3}/` · `stageC/probe_{P1,P2,P3}/run.txt`
(complete captures) · `handoff/_payload_anchor2/` (the 24-payload byte-identity anchor).
Job ids `6dfe9fe4-…` (P1) · `3839c968-…` (P2) · `56828e93-…` (P3).
Twin sha256 `dd244db8294fcb33…` / `9bf216edf82bd2ff…` / `65da3bbd35980410…`.

No protected tree was written to. **Spend 35 of 80.**
