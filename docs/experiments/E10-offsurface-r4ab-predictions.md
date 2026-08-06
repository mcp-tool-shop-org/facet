# E10 Ruling 4(a) + 4(b) — predictions, hashed BLIND

**Executor session, 2026-08-06.** Written and hashed **before any measurement ran** on
either subject for this dispatch. Nothing in this file was informed by a number produced
this session. `bake_hero_prep.py` — the report's named unread suspect — is **deliberately
still unread at the moment of hashing**, so no measurement here is shaped to a mechanism I
already knew. It will be read only after the numbers are in, and reported as *code read*,
never as a ruling.

Disclosure of what I did read first, since it bounds "blind":
[the E10 ruling](E10-offsurface-ruling.md),
[the galleon's consumers report](E10-offsurface-consumers-report.md), the tools
`e10_offsurface.py` / `e10_offsurface_consumers.py` / `e12_offsurface.py` /
`e10_claim_replay.py` / `e08_ceiling.py`, and the recorded W3 headlines in
`E08-gate0.md`, `E08-eightcam.md`, `E04-task1-report.md`, `docs/handbook/subjects.md`.
Those supply the anchors. **None of them contains W3's off-surface rate, which nothing has
ever measured.**

---

## Task A — W3 / ARMB's own off-surface measurement

### The subject, pinned before running

| operand | value |
|---|---|
| prep bake | `E:\AI\training\facet_E06\C1\prep` (E08 armB's prep — `E08-armB-state.md` line 10, `E08-intersection-regression.md` line 70) |
| emit-pixel unit | from ARMB's own `state/job_*/cam.json`: `v_ext` 1.1969748723526452 over `H` 1024 → **1.168921e-03** canonical units (all eight jobs carry the identical framing; checked) |
| stage-1 sidecar | `facet_E08/ARMB/stage1_8cam_styled_mask.npy` |
| final sidecar | `facet_E08/ARMB/state/styled_mask.npy` |
| ceiling floors | **production split, body 0.45 / head 0.18** with the face rect from `meta.json` — W3's ruled configuration, unlike the ship's uniform 0.45 |

### Anchors that must reproduce before any recompute is believed

| anchor | must equal | source |
|---|---|---|
| uv-valid texels | 2,402,810 | `E08-gate0.md` |
| 8-camera reachable | 1,780,546 (74.10%) | `E08-gate0.md`, `E08-eightcam.md` |
| stage-1 styled | 1,653,659 (68.8%) | `E08-eightcam.md` |
| brush total | 101,527 (4.2%) | `E04-task1-report.md` |
| dilation | 647,624 (27.0%) | `E04-task1-report.md` |
| stroke 8 | 25,175 | `E04-task1-report.md` |
| stroke 7 | 47,020 | `ARMB/out/run_log.jsonl` |
| strokes 1–6 | 29,332 (= 76,352 − 47,020) | two records, cross-consistent |
| the two instruments agree | `e12_offsurface.py`'s rng(0) 200k sample must equal the consumer tool's full-bake classification restricted to the same indices, to the recorded digits | the pattern E12 Ruling 6c made standard |
| the ship, re-validated | `e12_offsurface.py` on `E04_shipprep` must return **2.5065%** again | E12 Ruling 6c |

A missed anchor halts that question and is reported. Nothing is substituted.

### Predictions

The dispatch names the licensed prior: **ship 2.5065%, beast 2.6430%**, legitimate here
because E12 Ruling 6b banked the off-surface rate as a *bake artifact class, not a subject
property*. Two subjects 0.14 points apart. W3 is the third.

| # | prediction | falsified if |
|---|---|---|
| **A1** | W3's >1 px rate lands in **1.8%–3.2%**, point estimate **2.3%**, and I call the **direction below both anchors** — W3's prep puts `head_scale` 3.0 and 89.5% of UV area on one compact smooth region, against a hull's rigging and a beast's wings | outside [1.8, 3.2]; direction wrong if ≥ 2.5065 |
| **A2** | ≥ 80% of W3's off-surface population is **>5 px** off, not sub-pixel spill (ship 83.5%, beast 92.3%) | < 80% |
| **A3** | The galleon's headline finding **replicates in direction**: stage-1's off-surface rate exceeds dilation's. Reasoning, stated so it can be wrong: the visibility test casts a ray from the baked position and accepts when it hits nothing — a position floating off the surface has a clearer ray, so off-surface texels should be *over*-admitted, not stranded in dilation. Point: stage-1 ≈ 1.3× dilation | stage-1 rate ≤ dilation rate |
| **A4** | Off-surface texels are enriched in the **reachable** set: their reach rate exceeds the population's 74.10%. The enrichment ratio is arithmetically capped at 1.35 here, so it **must compress** against the galleon's 1.426 — that compression is not evidence of anything. Point: ~85%, ratio ~1.15 | off-surface reach rate ≤ 74.10% |
| **A5** | Consumer deltas, direction and rough size: reach/valid **falls** ~0.25 pts (74.10 → ~73.85); styled/valid **falls** ~0.15 (68.8 → ~68.65); styled/reachable **rises** ~0.1 (92.9 → ~93.0); dilation/valid **rises** ~0.2 (27.0 → ~27.2); brush/valid **flat** within ±0.05 | any named direction wrong |
| **A6** | **No** W3 stroke split loses ≥ 8% of its commits — the galleon's stroke-1 outlier does not replicate here. Held loosely: only three splits are recoverable without a replay (1–6 / 7 / 8), so a single bad stroke inside 1–6 could hide | any split ≥ 8% |

**A6 is deliberately weak and says so.** Reporting it as strong would be the mistake.

### What Task A does NOT decide

Which family — as-recorded or on-surface — becomes the standing cross-asset headline.
That is E10 Ruling 2's condition, and it is the Director's and the advisor's. This task
**completes the condition's input** and halts.

---

## Task B — the mechanism, on the galleon's bake

### The works-perfectly test, stated for every number BEFORE any of them is read

This is the part that has to come first. A number whose no-defect value I have not written
down cannot be read as evidence of anything.

| measurement | what it returns when **nothing is wrong** | what it returns when the defect is **present** |
|---|---|---|
| **B1 — off-surface rate per island-rim-distance stratum** (EDT of the uv-valid mask; strata 0–1, 2–3, 4–8, >8 texels) | Perfect bake: the population is empty, every stratum reads 0, and the statistic is undefined rather than small. Defective bake whose cause is *unrelated to rims*: the curve is **FLAT** — every stratum reads the population's 2.4967% | a curve **rising toward the rim** |
| **B2 — seam adjacency** | glTF splits a vertex at every UV seam, so on a closed mesh **every island rim IS a seam** and B2 is arithmetically B1, not a second number. If the welded mesh has boundary edges, rim splits into seam-rim and boundary-rim and both are reported. Perfect: nothing to report. Unrelated cause: identical flat curve | seam-rim rate ≠ boundary-rim rate |
| **B3 — off-surface rate per stage-1 owning view** (`stage1_8cam_owner.npy`, 8 views) | Perfect: eight zeros. Unrelated cause: **eight equal rates**, each the stage-1 class rate of 3.06% | spread across views |
| **B4 — modal exact position** (how many off-surface texels share a byte-identical baked position) | Perfect or unrelated cause: the modal count is **1 or 2** — coincidence only | a single exact position held by thousands ⇒ an unwritten-default fill |
| **B5 — surface-distance magnitude joint with rim distance** | Perfect: empty. Unrelated cause: the >5 px share is the **same** in every rim stratum | near-rim shallow, deep-interior far ⇒ two mechanisms superposed |
| **B6 — connected components of the off-surface set in the atlas** | Perfect: none. Unrelated cause / true speckle: **thousands of tiny components**, largest in the tens | a few large coherent blobs |
| **B7 — per-island off-surface rate** (label the uv-valid mask; rate within each island) | Perfect: every island 0. Unrelated cause: **every island ≈ 2.4967%**, no island near 0% or 100% | a subset of islands at ~100% |
| **B8 — stroke 1 vs strokes 2–6** | Perfect: all six lose 0. Unrelated cause: all six lose the brush class rate, **2.27% each** | the recorded 8.15% against 0.41–2.45% — already known, so B8's *new* content is the characterisation, never the rate |

**The trap this table exists to avoid:** B1, B3, B7 and B8 are all rate-per-stratum
measurements, and a rate-per-stratum measurement on a defect-free artifact is *flat, not
zero*. Reading "the numbers are small" as "nothing is wrong" would be the error. Flatness
is the null; shape is the signal.

**And one measurement is barred from gating by construction:** B1's strata are defined by
distance to a boundary, which is the exact proxy this repo already paid a session for
(*"test the property, not a geometric proxy for it"* — a 1–2 texel structure is entirely
rim). B1 is reported as a diagnostic. It cannot become a threshold, and this file says so
before its value is known.

### Predictions

| # | prediction | falsified if |
|---|---|---|
| **B1a** | The rate curve is **not flat**: rate at rim-distance ≤ 1 is ≥ **3×** the rate at rim-distance > 8 | ratio < 1.5 |
| **B1b** | And yet the rim does **not explain** the population: ≥ **60%** of off-surface texels sit at rim-distance ≥ 2 | < 60% |
| **B2** | The welded prep mesh is effectively closed — boundary edges < **1%** of edges — so rim = seam and no second number exists | ≥ 1% |
| **B3** | Per-view rates vary by ≥ **2.5×** between the highest and lowest of the eight | max/min < 2.5 |
| **B4** | **Not** a constant fill: the modal exact position is shared by < **100** texels | any single exact position ≥ 1,000 texels |
| **B5** | Near-rim off-surface texels are **shallow** and deep-interior ones are **far**: >5 px share ≤ **70%** at rim ≤ 1, and ≥ **90%** at rim > 8 | either bound missed |
| **B6** | Coherent, not speckle: ≥ **50%** of the population in components ≥ 100 texels, largest component ≥ **1,000** texels | either bound missed |
| **B7** | At least one island is > **90%** off-surface, and such islands hold ≥ **20%** of the population | no island > 90%, or < 20% |
| **B8** | Stroke 1's excess is an **island** effect, not a rim effect: ≥ **50%** of its 2,163 off-surface commits fall in islands whose own off-surface rate is > 50% | < 50% |

B1a and B1b are deliberately in tension. If both hold, the reading is *rim-enriched but not
rim-explained*, and that is a finding rather than a hedge. If B1a holds and B1b fails, it is
a rim skirt. If B1a fails, the rim is not in it at all.

### Out of scope, explicitly

No fix. No gate. No route tool edited. No threshold derived from any number here. Nothing
is decided about whether either accepted asset is affected — both stand on the Director's
eye and nothing in this dispatch re-opens that. `bake_hero_prep.py` is read only after the
measurements land, and what it says is reported as text, not as a cause.

---

## Standards compliance (this predictions file)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every operand of both subjects pinned by path and value before running; the emit-pixel unit written out with its derivation; this file hashed before the first measurement |
| ANDON_AUTHORITY | 3 | ten Task-A anchors, each halting its own question on a miss; the ship re-validated before the instrument is pointed anywhere new |
| NAMED_COMPENSATORS | 3 | writes are new diagnostic files plus JSON under scratch and `e10_contact/`; undo is deleting them; no accepted artifact opened for writing |
| DECOMPOSE_BY_SECRETS | 2 | Task A and Task B are separate tools with one purpose each; Task A's subject is supplied by flags rather than hardcoded, so the ship's cited instrument is never edited |
| UNCERTAINTY_GATED_HUMANS | 3 | the standing-family question is pre-registered as *halt, do not decide*; A6 is labelled weak before its value is known; B1 is barred from gating before its value is known |
| EXTERNAL_VERIFIER | 3 | every Task-A anchor is an artifact this session did not produce; the two off-surface instruments cross-check each other on the same rng(0) sample |
