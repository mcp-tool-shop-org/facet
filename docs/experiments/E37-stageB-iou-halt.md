# E37 Stage B — HALT: the reg-IoU ANDON fired on seed 987654

**Seat:** executor · **Date:** 2026-08-15 · **Spend: 27 of 40 cloud jobs**, exactly the
bands' figure. All 24 seed-set jobs generated and completed; **nothing further has been
submitted** and no projection has run.

The kickoff's selection clause is explicit: *"reg-IoU ≥ 0.80 (the E34 floor; **a firing
HALTS with numerator and denominator**)"*, and the sealed bands' H3 DOWN branch says the
same. **It fired.** Reported with its evidence and halted per executor rule 3. No parameter
was changed, nothing was re-run, and no seed has been selected.

---

## 1. What fired

**Seed 987654, two of eight views below the 0.80 floor:**

| seed 987654 | reg-IoU | keyed px | geometry mask | |
|---|---|---|---|---|
| view 2 | **0.5821** | 91,559 | 54,993-class profile frame | **FIRED** |
| view 5 | **0.7591** | 120,709 | 96,789-class frame | **FIRED** |
| the other six | 0.9121 – 0.9571 | — | — | pass |

**Numerator and denominator, as the clause requires.** reg-IoU is the intersection-over-
union of the twin's keyed figure against the raycast geometry mask for that view. The two
firing views are the ones whose keyed pixel count is furthest from the geometry's:

- **view 2** is a profile (mask 54,993 px) and the twin keyed **91,559** — the paint covers
  **1.67×** the surface the geometry offers.
- **view 5** keyed **120,709** against a ~96,800 px mask — **1.25×**.

Compare the same two views on the seeds that passed: seed 770700 view 2 keyed **58,472**
against the same 54,993-px profile mask (1.06×), and seed 20260815 view 2 keyed **54,993**
(1.00×). The failure is specific to 987654's paint, not to those camera angles.

## 2. The full board, all three seeds, all 24 views

| seed | total dark count | total area px² | largest | min reg-IoU | median C\* | floor |
|---|---|---|---|---|---|---|
| **770700** | **160** | **887** | 34 | 0.9116 | 29.90 | **OK** |
| 987654 | 183 | 1075 | 35 | **0.5821** | 35.26 | **FIRED** |
| 20260815 | 229 | 1495 | 36 | 0.9422 | 34.36 | OK |

## 3. ⚠ What I did NOT do

My scoring script treated the floor as an **eligibility filter** — it excluded 987654 and
printed "winner: seed 770700". **That is not the ruled behaviour and I am not reporting it
as a result.** The kickoff says a firing *halts*; the selection rule's "subject to
reg-IoU ≥ 0.80" and H3's "any view below 0.80 → the arc halts" are in tension, and
resolving that tension in favour of quietly proceeding would be an executor deciding what a
gate means. The number is recorded above so the ruling has it; it is not a selection.

**No parameter was changed, no seed re-rolled, no job re-submitted.**

## 4. The bands, scored so far — three of four are readable now

Sealed at `1494a0f`; scored here without adjustment.

| band | pre-registered UP branch | measured | verdict |
|---|---|---|---|
| **H1** dark census | total **above 208** (8 × E35's 26) | **160 / 183 / 229** — two of three below 208 | **MISS on the UP branch; lands FLAT** for 770700 and 987654, UP only for 20260815 |
| **H2** register C\* | median within **±4 of 23** | **29.90 / 35.26 / 34.36** — all above 27 | **MISS**, lands in the FLAT band (27–31) for 770700 and outside it for the other two |
| **H3** reg-IoU | all 24 view-runs **≥ 0.90** | 22 of 24 ≥ 0.91; **two below 0.80** | **DOWN branch — the halt** |
| H4 mole class | zero detached facial marks on views 0/1/7 of the winning set | not scorable — no set is selected | **pending the ruling** |

⚑ **H1's UP branch was argued from mechanism and it was wrong.** I predicted wood's lighter
base plus 2.09× the interior edge would push the census up; measured, 770700 and 987654 land
*inside* the terracotta reference band rather than above it. The mechanism reasoning was
plausible and the measurement disagrees — recorded as a miss, not reinterpreted.

⚑ **H2 is a clean miss in a useful direction.** Wood's C\* runs **29.9–35.3** against
terracotta's recorded 23.77 — consistently *higher*, not centred on it. That the register
floor was **suspended** rather than ported is what stopped this from firing a meaningless
halt: a terracotta floor applied to wood would have been a threshold about the wrong
material. *Suspend rather than invent* worked exactly as intended.

## 5. Dispositions — named, none taken

1. **Rule the firing characterised and select from the two eligible seeds** — 770700 wins on
   the sealed rule with 160 against 229. Requires ruling that "subject to the floor" governs
   and H3's halt clause is an eligibility filter, not an arc halt.
2. **Investigate 987654's views 2 and 5 first** — the 1.67× over-key on a profile is a
   measurable defect with a mechanism worth knowing before it is set aside.
3. **Re-roll 987654's two failing views** — mechanical repeat, 2 jobs, taking spend to 29 of
   40. ⚠ The dispatch calls census numbers and register CONTENT, never repeated; whether an
   IoU failure is mechanical or content is exactly the question, and it is not mine.
4. **Halt Stage B and re-dispatch** with the floor's meaning settled.

**Awaiting the ruling. 27 of 40 spent; no seed selected; no projection run; all 24 twins,
their censuses and their per-view registers are in the record.**
