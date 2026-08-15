# E37 Phase 1 — seeds pre-registered and blind bands, sealed BEFORE the first job

**Seat:** executor · **Written:** 2026-08-15, **before any Phase-1 payload was emitted or
submitted** · **Spend at sealing: 35 of 80.**

Sealed by commit per [Amendment 3](E37-remake-the-performer-kickoff.md) and
[Ruling 18](E37-ruling.md). Nothing below was written after seeing a Phase-1 result: at
sealing **no Phase-1 twin exists**, and every prediction here is blind in the strict sense —
not one arrival has been measured, sampled, or looked at.

---

## The two seeds, pre-registered

| set | seed | why this one |
|---|---|---|
| **A** | **2026081511** | date-derived, so it is arbitrary and auditable rather than picked |
| **B** | **2026081512** | its successor, same construction |

**Both are fresh.** Every numeric token of six digits or more in this arc's record and
artifact tree was enumerated before choosing: `770700 · 770701 · 987654 · 424242 · 20260815 ·
202608151 · 202608153 · 202608156 · 2026081503 · 2026081507 · 20260815007 · 300000` (plus
hashes and measurements). Neither `2026081511` nor `2026081512` appears anywhere in
`docs/` or `facet_E37/`. Checked, not assumed.

## The configuration — uniform on every one of the sixteen view-runs

| field | value | source |
|---|---|---|
| prompt | **v-w1** per-view stems | `E37-twin-prompts-vw1-8view.json`, byte-pinned |
| negative | **v-w1 + the backdrop clause** — `…, dark background, gradient backdrop, studio backdrop` | fixture `facet_E37/registers/vw1n.json`, read through `--negative-from`, **never typed** |
| `cn_strength` | **1.0** (node 11) | `--cn-strength`, ANDON-bounded to the vendor band [0.8, 1.0] |
| controls | the **tuned** canny 0.10 / 0.50 controls | Ruling 5 step 3 |
| frame | **368 × 1024** | Ruling 4 |
| everything else | the recorded recipe — denoise 0.92, steps 20, cfg 2.5, euler/simple, shift 3.1, ControlNet start 0.0 / end 1.0 | byte-preserved from `payload_r3_v1.json` |

Emitted by `e37_fire_seed_sets.py`, which already carries both lever flags — enumerated
before anything was commissioned. Five fields move per payload and the script prints the
full diff against the recorded original and refuses if anything else did.

## ⚠ The lever combination is n = 0

`cn_strength` 1.0 and the backdrop negative clause were measured **one at a time**, on
**one view** (v7), at **one seed**, in the Ruling 16 probe:

| arm | dark count / area | Stage-B key | projection key | sampled bg |
|---|---|---|---|---|
| P1 — seed only, no lever | 72 / 270 | 0.9451 | 0.9144 | 151.1 |
| P2 — + backdrop negative | 71 / 268 | 0.9478 | 0.9196 | **181.4** |
| P3 — + `cn_strength` 1.0 | **50 / 248** | 0.9467 | 0.9106 | 157.6 |

**Their combination has never been run — n = 0, stated here rather than discovered later.**
Nothing in this record says the two compose additively, and every band below is positioned
against **lever-free** baselines for that reason.

## The measured baselines these bands are positioned against

Three **single-seed eight-view** sets exist, all lever-free, from Stage B:

| seed | census total (count / area) | largest | register C\* min–max | **within-set C\* spread** | reg-IoU min |
|---|---|---|---|---|---|
| 770700 | 160 / 887 | 34 | 23.30 – 30.42 | **7.12** | 0.9116 |
| 987654 | 183 / 1075 | 35 | 29.20 – 37.11 | **7.91** | 0.5821 |
| 20260815 | 229 / 1495 | 36 | 32.17 – 38.71 | **6.54** | 0.9422 |

And the **rejected** mixed-seed set, on the identical statistic and the identical
instrument: per-view register C\* of 23.30 · 30.68 · 29.90 · 39.97 · 26.00 · 24.41 · 38.94 ·
29.93 — **within-set spread 16.67**, which is **2.1–2.5× every single-seed set above**. That
is the quantity Phase 1 exists to close, and it is comparable because it is the same column
of the same instrument.

*(The composed-atlas cross-owner C\* spread of 15.90 reported at Stage C is a different
statistic over a different population — owner regions of an atlas, not register regions of a
twin — and is cited nowhere below as a baseline.)*

---

## The predictions — three branches each, UP live, plus the cannot-measure branch

Ruling 15's template clause is carried on every hypothesis: **an arrival can defeat
measurement itself**, and that is a named outcome rather than a gap.

### P1 — within-set register C\* spread

**Prediction: UP. Blind.** Reasoning stated before the result: the spread the mixed set
carried was produced by seed mixing, which is dead here by construction; three lever-free
single-seed sets landed 6.54–7.91 with no set outside that band.

| branch | statement |
|---|---|
| **UP (live)** | **both** sets land within-set C\* spread **≤ 8.00** — inside or at the measured single-seed band |
| FLAT | one or both land **8.00 – 12.00** — wider than any measured single-seed set, still far under the rejected 16.67 |
| DOWN | either set lands **> 12.00** — single-seed construction does not deliver a tight register once both levers are on |
| CANNOT MEASURE | the register instrument refuses a view (the backdrop-invention class, Ruling 15) and the set has no spread |

### P2 — total dark census per set

**Prediction: FLAT. Blind.** Reasoning stated before the result: `cn_strength` 1.0 moved one
view's census 72 → 50 (−31%) at an identical seed, but census across lever-free seeds swings
160 → 229 (+43%) on **seed alone**. Seed variance plausibly swamps a one-view lever effect,
and the combination is n = 0.

| branch | statement |
|---|---|
| **UP (live)** | at least one set totals **< 160** — below every lever-free single-seed set |
| FLAT | both sets total **160 – 229** — inside the lever-free range |
| DOWN | either set totals **> 229** |
| CANNOT MEASURE | a view cannot be censused through its geometry mask |

Largest connected component rides beside the total on every row — total alone must choose
between missing one wrong blob and firing on ordinary speckle. Lever-free largest ran 34–36.

### P3 — both keys clear on all sixteen view-runs

**Prediction: FLAT. Blind.** Reasoning stated before the result: sixteen view-runs against a
route where the projection key has fired at roughly one view in eight (v3 twice, v7 once),
and the Stage-B key cleared a view the projection key then failed. Expecting zero from
sixteen is optimistic even with `cn_strength` 1.0 anchoring.

| branch | statement |
|---|---|
| **UP (live)** | **all sixteen** view-runs clear both keys — Stage-B key and projection key ≥ 0.80 |
| FLAT | **1–2** view-runs fail one key |
| DOWN | **≥ 3** fail, or an entire set is ineligible under the sealed rule |
| CANNOT MEASURE | the register instrument refuses; the projection key is then not run, per the standing refusal |

The projection key is read by running the **full eight-view projection to a scratch `--out`**
per set — the Ruling 12 precedent, local and free, advancing nothing.

### P4 — the backdrop clause holds the field

**Prediction: UP. Blind.** The clause is the direct lever against the failure it was written
for, and P2 measured sampled background 151.1 → 181.4 toward the kept twins' ~196.

| branch | statement |
|---|---|
| **UP (live)** | **zero** view-runs exceed **55%** figure coverage, the failure signature's band (the recorded failure ran 80.30%, every clean arm under 46%) |
| FLAT | 1–2 view-runs land 55 – 70% |
| DOWN | any view-run reaches **≥ 70%**, or the register instrument refuses on backdrop grounds |
| CANNOT MEASURE | coverage is undefined because keying failed for a different reason |

---

## The selection rule — restated from Amendment 3, NOT changed here

> every view clears both keys → **lowest total dark census** → ties broken by **within-set
> C\* spread**.

A third set fires **only if neither censuses clean**. **One mechanical repeat per set** — a
validation failure, a degenerate frame or a corruption signature. **Content defects are NOT
re-rolled**: they are listed per view as they are measured and become Phase 2's masked-repair
inventory. Per-view seed mixing is dead, permanently.

## What would make each of these uninformative

- **P1** if both sets land inside the single-seed band, it confirms single-seed construction
  behaves as the three lever-free sets did and says **nothing about the levers** — which is
  the correct scope, because banding is dead by construction here and not by the levers.
- **P2** the largest confound is seed lottery, which is why the band is positioned against
  the lever-free *range* rather than a point. A set inside 160–229 does not separate lever
  effect from seed draw at n = 2.
- **P3** sixteen view-runs is a small sample against a ~1-in-8 base rate; FLAT and UP are one
  or two events apart and the distinction is weak.
- **P4** the clause and `cn_strength` move together here, so a clean field cannot be
  apportioned between them. Stated in advance rather than claimed afterwards.

## Halt conditions

Per the kickoff, unchanged. A fired gate halts with its numerator and denominator and the
seat reports rather than improvises. The register instrument's refusal is correct behaviour,
not an error. No judgement words in any Phase-1 report.

**Budget:** 16 jobs at the measured ≤ $0.0184/job ≈ $0.30. Spend **35 → 51 of 80** if no
mechanical repeat fires.
