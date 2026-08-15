# E37 Phase 1 — two single-seed sets: report and HALT

**Seat:** executor · **Written:** 2026-08-15, after both sets landed · **Spend: 51 of 80**
(16 jobs fired, zero mechanical repeats). Bands sealed at
[`7049527`](E37-phase1-bands.md) **before** the first payload was emitted.

**⛔ HALT: a gate FIRED on set B** — the projection key at view 3, `0.7716` against the
`0.80` floor. Reported with its numerator and denominator below; views 4–7 of that set are
UNMEASURED. Nothing is selected here: the executor halts on any firing and the advisor
applies the sealed rule (the Ruling 6 boundary).

---

## 1. What ran

Sixteen jobs, two complete eight-view sets, **zero failures and zero mechanical repeats**.
Uniform on every view: v-w1 · the backdrop negative clause via the `vw1n.json` fixture ·
`cn_strength` **1.0** · the tuned controls · 368 × 1024 · the recorded recipe otherwise.
Emitted by `e37_fire_seed_sets.py` — enumerated before anything was commissioned; it already
carried both lever flags.

The deltas were checked independently of the emitter's own ANDONs: the diff against the
recorded payload is **exactly seven fields** (init, control, seed, prefix, positive, negative,
`cn_strength`) and **16/16** carry both levers and a pre-registered seed. Set B differs from
set A in **exactly** `seed` and `filename_prefix` on all eight views.

Ledger: `phase1/job_ledger.json`, all 16 job ids.

---

## 2. ⚑ A fired gate that was MINE, not the twins'

**The first projection pass halted both sets at view 0** on the background-admission ANDON —
set A at **34.49%** of newly-admitted texels within ΔE 10 of the twin's background, set B at
**5.05%**, both against a **2.0%** limit.

It would have read as a finding about the lever combination. It is not. **I omitted a flag
the recorded chain passes explicitly.**

`--bg-max-pct 2.0` is the tool's default and it is **W3 calibration data that this record has
withdrawn**: E04's ruling sets it to a vacuous **100.0** — *"suspension expressed as a value
the consumer actually receives"* — and
[E34-projection-coverage-report.md:262](E34-projection-coverage-report.md) records the ruled
invocation passing **`--bg-max-pct 100.0` (R-a, the E16 Ruling 4e withdrawal, passed
explicitly)**.

The tell was in the record the whole time: the **rejected** Stage-C projection ran view 0 at
**18.50%** and views 1–7 at 24.56–60.57%, and it completed. A bound that every recorded view
of the accepted chain exceeds by an order of magnitude was never in force.

Caught by asking why a completed recorded run carried numbers a gate says are impossible,
before reporting the firing as a property of the arrivals. Re-run with the recorded
invocation, nothing else changed. **The class: a withdrawn threshold reappearing as a default
when an invocation is written from the flag list instead of from the record.**

*(Set A's first pass also exited 1 on `--out` lacking a `.png` extension — the atlas write,
after all eight registrations were computed and printed. Re-run with a valid path: exit 0.
Recorded so no unexplained exit code sits beside a result.)*

---

## 3. Set A — seed 2026081511

| view | census count / area | largest | Stage-B key | **projection key** | register C\* | coverage |
|---|---|---|---|---|---|---|
| 0 | 25 / 83 | 10 | 0.9633 | 0.9097 | 28.67 | 25.20% |
| 1 | 22 / 149 | 25 | 0.9470 | 0.9211 | 27.44 | 25.25% |
| 2 | 19 / 76 | 18 | 0.9132 | **0.8228** | 35.04 | 15.43% |
| 3 | 13 / 64 | 19 | 0.9254 | 0.8848 | 29.12 | 25.81% |
| 4 | 25 / 124 | 23 | 0.9606 | 0.9063 | 28.26 | 25.28% |
| 5 | 7 / 34 | 10 | 0.9473 | 0.9433 | 29.53 | 25.66% |
| 6 | **46 / 231** | 32 | 0.9408 | 0.9338 | 30.66 | 15.04% |
| 7 | 5 / 48 | 21 | 0.9389 | 0.9470 | 26.71 | 25.65% |

**Census total 162 count / 809 px², largest component 32.**
**Within-set register C\* spread 8.33** (26.71 – 35.04).
**Both keys clear on all eight views**; the register instrument refused none.
Projection to a scratch `--out` completes **exit 0**: styled/REACHABLE
**2,223,745 / 2,268,219 = 98.0%**, atlas variance **0.02580**, holes 194,869.

## 4. Set B — seed 2026081512

| view | census count / area | largest | Stage-B key | **projection key** | register C\* | coverage |
|---|---|---|---|---|---|---|
| 0 | 19 / 72 | 12 | 0.9552 | 0.9034 | 33.54 | 25.61% |
| 1 | 32 / 197 | 31 | 0.9627 | 0.9168 | 33.95 | 25.00% |
| 2 | 29 / 171 | 36 | 0.9627 | 0.8708 | 35.89 | 14.62% |
| 3 | 53 / 260 | 31 | 0.9485 | **0.7716 — FIRED** | 35.41 | 25.25% |
| 4 | 25 / 66 | 16 | 0.9570 | *not run* | 30.97 | 25.62% |
| 5 | 21 / 107 | 16 | 0.9551 | *not run* | 33.03 | 25.40% |
| 6 | 62 / 318 | 30 | 0.9675 | *not run* | 33.67 | 14.57% |
| 7 | 40 / 195 | 31 | 0.9567 | *not run* | 34.24 | 25.19% |

**Census total 281 count / 1386 px², largest component 36.**
**Within-set register C\* spread 4.93** (30.97 – 35.89) — the tighter of the two.
**The Stage-B key clears all eight. The projection key FIRED at view 3: 0.7716 against
0.80**, and the tool's own text is the halt — *"the twin is registered to the wrong place …
do not tune this threshold."* Views 4–7 were never reached and carry **no** projection-key
number; they are written *not run*, never zero.

---

## 5. The bands, scored — two hits, two misses

| | prediction (blind, sealed) | measured | branch |
|---|---|---|---|
| **P1** within-set C\* spread | **UP** — both sets ≤ 8.00 | A **8.33**, B **4.93** | **FLAT — MISS by 0.33 on set A** |
| **P2** total dark census | **FLAT** — both in 160–229 | A **162**, B **281** | **DOWN — MISS** |
| **P3** both keys, 16 view-runs | **FLAT** — 1–2 fail one key | 1 failed (B v3); 4 unmeasured | **FLAT — HIT** |
| **P4** backdrop clause holds field | **UP** — zero views ≥ 55% coverage | max **25.81%** | **UP — HIT** |

**P1's miss is narrow and the reasoning it tested still moved**: single-seed sets ran 6.54 /
7.12 / 7.91 lever-free, and the rejected mixed-seed set measured **16.67** on the identical
column. A 8.33 and B 4.93 both sit far below the mixed set; set A sits 0.33 outside the band I
drew. The band was drawn at the top of the lever-free range and the lever combination is n=0,
so a set landing just outside it is exactly the uncertainty the band existed to expose.

**P2's miss is the one worth banking.** I predicted seed variance would swamp the lever, and
it did — but in the direction I did not price: set B's **281** is above every lever-free set
(160/183/229), and set A's **162** is below all but one. **A 73% census spread between two
seeds under an identical configuration** is larger than the lever-free spread (43%), so the
`cn_strength` 1.0 census gain measured on one view of one seed (72 → 50) does not survive as a
set-level property. Stated as measured, n=2.

**P4 is the clean one.** Every one of the sixteen view-runs keyed under 26% coverage against
the 55% band and the recorded failure's 80.30%. The backdrop-invention class did not
reproduce anywhere.

---

## 6. Content defects — Phase 2's inventory, NOT re-rolled

Per Amendment 3, content defects go to masked repair. Listed per view as observed at full
size on the sheets, set A:

| view | observed |
|---|---|
| 0 | ears read as **detached dark discs** either side of the skull; fingers drawn as dark strokes rather than form |
| 1 | **hard-edged dark wedge across the brow/eye**; torso and upper arms a markedly darker wood than the limbs — a *within-view* tonal split; ear a dark blob |
| 2 | dark blob at the toe; lower legs merge in profile; pale crescent on the skull side |
| 3 | dark disc at the ear; speckle on the forearm and hand |
| 4 | cleanest body; both ears protrude as discs; a pale dot on the left forearm |
| 5 | flat pale disc at the ear |
| 6 | **the nose reads as a hard-edged wedge protruding past the silhouette** — the strongest single defect, and this view carries the set's highest census (46 / 231) |
| 7 | face partially drawn with a hard vertical edge; nose wedge |

**Cross-cutting, and it reproduces a recorded class:** the ear appears as a detached
knob/disc on every view. [Ruling 9](E37-ruling.md) folded the ear-knob observation from two
independent seeds — *"prior-driven, not seed noise"* — and a **third** independent seed shows
it again.

**What the sheets do NOT show: banding.** Walked at full size and at 3× on the head, set A
reads as one wood across all eight views. That is the single-seed construction behaving as
Amendment 3 designed it, and it is the whole point of the phase.

---

## 7. What this seat did not do

- **Selected nothing.** A gate fired; the sealed rule is the advisor's to apply.
- **Re-rolled nothing.** Set B's firing is CONTENT — the job completed and produced a real
  twin whose paint mis-registers — so no repeat fires, per the Ruling 6 boundary.
- **Tuned nothing.** `--bg-max-pct` was corrected to the *recorded* value, not to a passing
  one; `--reg-iou-min` stayed at 0.80 and the tool's own refusal text is quoted above.
- **No third set.** Amendment 3 fires one only if neither censuses clean; that is a reading,
  and readings are not this seat's.
- No protected tree was written to; manifest gates HELD at open (E33 116/116 · E34 84/84 ·
  E35 335/335 · C 7,312 files, delta +0/+0), E15 four legs exit 0, watchdog ADVANCING.

## 8. Artifact homes

`E:\AI\training\facet_E37\phase1\` — `payloads/` (16) · `setA/` · `setB/` · `measA/` ·
`measB/` · `proj_scratch_A/` · `projkey_{A,B}.txt` · `proj_{A,B}.txt` (the mis-invoked pass,
kept as the evidence for §2) · `job_ledger.json` · `e37_phase1_measure.py` ·
`sheet_setA_full.png` · `sheet_setA_head3x.png` · `e15_scratch.db` · `open_manifest_*.json`.
