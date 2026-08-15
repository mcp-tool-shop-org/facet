# E37 Stage B — blind bands, sealed BEFORE the first seed set

**Seat:** executor · **Written:** 2026-08-15, before any seed-set job was submitted ·
**Spend at sealing: 3 of 40** (Gate-R probe 2 + confirm 1).

Sealed by commit per the kickoff and [Amendment 2](E37-remake-the-performer-kickoff.md).
Nothing below was written after seeing a seed-set result; the only wood twins in existence
at sealing are the three view-0/view-4 Gate-R images, and where a band is informed by one it
says so.

---

## What is being run

**K = 3 full eight-view sets**, the recorded recipe otherwise byte-held (v-w1, canny-lock
0.9 / 0.0 / 1.0, denoise 0.92, steps 20, cfg 2.5, euler/simple, shift 3.1), on the picked
mesh's **tuned** controls (canny **0.10 / 0.50**, Ruling 5 step 3), frame 368×1024.

| seed | why this one |
|---|---|
| **770700** | the recorded twin seed, and the Gate-R probe's seed — the only wood seed with any evidence at all |
| **987654** | E35's measured-best on the dark class (mean dark area 71.9 px² against 170.4 at 770700) |
| **20260815** | one fresh, chosen as today's date so it is arbitrary and auditable rather than picked |

**Selection rule, pre-registered here and not to be changed after results:** one **GLOBAL**
seed — the lowest **total dark census** across its eight views, subject to **reg-IoU ≥ 0.80
on every view**. Per-view seed mixing is out (it produced the rejected pale wash) and
returns only at the Director's word. **The register floor is SUSPENDED** (Amendment 2): C\*
rides every row as a diagnostic and gates nothing, because no calibrated wood floor exists.

---

## ⚠ The reference context, and why it is not a floor

E35's terracotta seed floor — **dark count 7–26, area 34–139 px²** — is cited as *reference
context only*. Two reasons it cannot be a band here:

1. **Wood expectations are UNMEASURED.** Those numbers were measured on a terracotta
   register at a different material. Nothing in this record says what a wood twin's dark
   census should be.
2. **[Ruling 4](E37-ruling.md)'s frame caveat binds every citation of them.** They were
   measured at **352×1024**; this arc runs at **368×1024**, **+4.5% width**. Every
   *area*-denominated E35 figure is therefore quoted against a frame 4.5% wider, and a
   count is not directly comparable either.

So the bands below are stated as **directions with three branches**, not as thresholds.

---

## The hypotheses, three branches each, UP branch live

### H1 — the dark-speck class on wood, against terracotta

The generator-painted dark specks are the class E35 measured to its floor on terracotta and
could not remove while keeping the man. Wood is a different material with a *lighter* base
value, so a dark speck has more contrast against it.

| branch | statement |
|---|---|
| **UP (live)** | the best seed's total dark census across 8 views lands **above** 8 × 26 = 208 — i.e. worse per view than terracotta's best seed floor |
| FLAT | it lands **within** 8 × [7, 26] = [56, 208] |
| DOWN | it lands **below** 56 |

**Why UP is live, stated before looking:** the detector is contrast-based and wood's base is
lighter than terracotta's, so an identical speck reads *stronger* on wood; and the tuned
control carries **2.09× the interior edge** of the shipped one, which is more painted
structure for the detector to find. Both push the same way. **Disclosure: informed** — I
have seen three wood view-0/view-4 twins, though not a census of any of them.

### H2 — register C\*, diagnostic only

Gate-R measured C\* **21.67 / 24.28 / 23.30** on wood against the recorded terracotta
**23.77**.

| branch | statement |
|---|---|
| **UP (live)** | the winning set's median C\* across 8 views lands **within ±4 of 23** |
| FLAT | it lands 15–19 or 27–31 |
| DOWN | it falls **below 15** — the signature of a revert toward the grey init |

Nothing gates on this. It is here so a collapse is visible rather than discovered later.

### H3 — reg-IoU holds across all eight views

Gate-R: **0.9590** (v0) and **0.9489** (v4), both far above the 0.80 floor.

| branch | statement |
|---|---|
| **UP (live)** | all 24 view-runs land **≥ 0.90** |
| FLAT | all ≥ 0.80, some below 0.90 |
| DOWN | **any** view below 0.80 → the ANDON fires and the arc halts with numerator and denominator |

### H4 — the mole class does not return on the tuned control

The Gate-R confirm removed it at view 0. The other seven views were never tested against it.

| branch | statement |
|---|---|
| **UP (live)** | **zero** detached facial marks on the face-bearing views (0, 1, 7) of the winning set, at the (123,167)-family coordinates |
| FLAT | one such mark on one view |
| DOWN | two or more, or any on view 0 |

⚠ **The residual is known and stated:** canny thresholds could not reach zero fragments —
**5 px and 3 px specks persist at every threshold swept** (0.02–0.40 × 0.30–0.80). The
confirm is evidence they do not paint at that size on **one** view. H4 is the test of
whether that holds across the set.

---

## What would make each of these uninformative

Stated because *a row predicted to be uninformative is still a prediction*: if all three
seeds land inside one branch on every hypothesis, the seeds do not separate on these axes
and the selection rule reduces to a tie-break on total census alone. That is a real
possible outcome and it is not a failure — it would say the wood register is
seed-insensitive on the measured axes, which is itself worth recording.

## Compensator

24 jobs, no undo — bounded before spend by this file, by the pre-registered selection rule
above, and by the reg-IoU ANDON in H3. Budget after the sets: **27 of 40**.
