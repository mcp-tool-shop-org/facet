# E12 handoff 8 — HALT at the gate's pair-validation. No twin was generated.

**Executor session, 2026-08-06.** Predictions registered blind in `8b80f7c`
([E12-handoff8-predictions.md](E12-handoff8-predictions.md)), git blob `5098c8e`, written
before the masks, the frame gate, any control, the palette JSON, and before the gate had ever
been pointed at anything.

**Ruling 15c's third branch fired. The dispatch halts here, as that branch instructs.**
The palette gate as constructed flags the **accepted** pair on a population the branch structure
did not anticipate — and it is not the membrane stratum the allowance exists for. Per the
dispatch: *"Fires anywhere else on the pair → HALT with the evidence. The pair is accepted; a
gate that flags it is mis-constructed, and that is an instrument finding for the advisor."*

**0 credits. 0 generations. Nothing was submitted.** The eight masks, the frame-agreement gate
and the eight controls are built and staged, so whatever the ruling decides starts from them
rather than from scratch.

**Look at these before the numbers:** `gate_validation/VIEW1_offpalette_asconstructed.png` ·
`gate_validation/VIEW5_offpalette_asconstructed.png` (magenta = off-palette; cyan = inside the
suspended allowance).

---

## 0. Environment

| leg | result |
|---|---|
| watchdog | **alive** before the local geometry legs and re-checked after — heartbeat 0.2 s at start, 1.8 s at finish, pid 5132, VRAM 2,147 MiB against the 31,200 ceiling. No `_watchdog_DEAD` |
| GPU | one local Blender/raycast leg (eight silhouettes); no cloud submission, no credits |
| working copy | clean at session start; **explicit git paths only** |

## 1. The instrument defect, pre-registered and then proven

**P2a held exactly.** `palette_gate.py` line 83 read
`MAXBLOB = int(PAL["gate"]["max_offpalette_blob_px"])`, and `canon/E04-galleon-palette.json`
sets that key to `null` **on purpose** — *"both bounds are null ON PURPOSE… this subject has no
baseline until its own twins exist."* Pointed at its own precedent file, the tool raised:

```
TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

**The tool could not read the file its own precedent wrote**, and any subject arriving at the
gate before its twins exist hit a traceback instead of a measurement.

Repaired in the shape the `MAXPCT` path already had — **a null bound reports and gates nothing**
— with the defect and its meaning recorded in the tool body rather than silently fixed (Ruling
11e's practice). No number was invented. Then checked both ways, because **a check that cannot
fail is not a check**:

| | result |
|---|---|
| galleon palette, both bounds null | **runs**, exit 0 — 5,201 px / 1.62% / largest blob 727 on view 1 |
| same file with a blob bound of 1 armed | **`ANDON`, exit 1** — the guard still fires |

The repaired tool also now prints a loud line when both bounds are null: *this run is a
MEASUREMENT, not a gate; a zero-failure line means only that no bound was armed.* That line is
why the `ok` verdicts below must not be read as passes.

## 2. The geometry legs — every gate passed

| leg | result |
|---|---|
| **anchor** (P3a) | **0 differing px, IoU 1.000000** on views 1 and 5 against the masks the accepted pair was built from. The new eight-view mask set does not move an input the arc rests on |
| **frame agreement** (P3c) | **0 differing px on all eight views**, bound 0. *(The ungated legacy construction reads 0/0/0/1/0/1/0/4 — the Ruling 9a operand repair is what moves it, as recorded)* |
| **controls** (P3d) | views 1 and 5 reproduce **108,887** and **88,717 px** to the digit; the other six land 83,317–108,724, inside the predicted 60k–130k |

**P3b is falsified, and the error is mine.** I predicted all eight silhouettes at 490,941 px.
Measured, they are **four mirror pairs at four different sizes**:

| views | px | % of frame |
|---|---|---|
| 0, 4 | 520,644 | 28.373% |
| 1, 5 | 490,941 | 26.754% |
| 2, 6 | 363,299 | 19.798% |
| 3, 7 | 490,436 / 490,4**37** | 26.727% |

The *reason* I gave (Ruling 9b — an orthographic silhouette from **d** and **−d** is the same
ray set) was right and the mirror structure holds exactly on 0/4, 1/5 and 2/6. **I
over-generalised the constant from the one pair I had seen.** One measured detail worth the
record: **3 and 7 differ by 1 px**, and the ungated legacy construction put them 4 px apart —
the only pair that is not bit-exact.

## 3. Task 1 — the gate, and the branch that fired

### Construction

Built from the ruled bands into `canon/E12-beast-palette.json` — a **pure transcription**, the
same act that produced `canon/E04-galleon-palette.json` in the Arm T session. `profiles/beast.json`
was **not** edited; wiring `_fixtures.palette` is the advisor's write.

**One construction decision worth stating, because it would otherwise have pre-empted the branch
it was supposed to test.** `palette_gate.py` consumes **every** entry in `allowed_bands` and does
not read the `status` field. Listing the suspended blue-violet stratum there would have **silently
armed it**, and Ruling 15c's whole point is that the allowance applies *only if the pair-validation
demands it*. So the gate as constructed is **warm-olive alone**, and the stratum is recorded in a
key the tool does not read.

### The reading on the accepted pair

Both bounds null, `--report-only` — a measurement, not a gate.

| view | allowance **withheld** | allowance **applied** |
|---|---|---|
| **1** (head three-quarter) | **18,674 px · 3.80% · blob 2,724** | 18,080 px · 3.68% · blob 2,724 |
| **5** (tail three-quarter) | **40,224 px · 8.19% · blob 12,742** | 18,238 px · 3.71% · blob 3,968 |

**P1a held on all four of its numbers** — view 5 predicted 6–14% with a blob over 10,000
(measured 8.19%, 12,742); view 1 predicted 0.5–4% with a blob 500–8,000 (measured 3.80%, 2,724).

### Which branch — decomposed, because "dominant hue bin" cannot answer it

The gate's own dominant-bin line reports 12% of view 1's mass in one bin. That is not enough to
identify a population, so the off-palette mass was decomposed against the two structures the
branches name:

| | band shoulders (within 20° of an adopted edge) | inside the suspended allowance | **elsewhere** |
|---|---|---|---|
| **view 1** | 38.5% | **3.2%** | **58.3%**, median hue **234.0** |
| **view 5** | 31.1% | **54.7%** | 14.3%, median hue 294.3 |

**View 5 is branch 2 cleanly.** More than half its off-palette mass is the membrane stratum the
allowance was written for, and its "elsewhere" at median 294.3 is that same stratum's upper
skirt, 0.9° past the allowance edge. Applying the allowance takes it 8.19% → 3.71%.

**View 1 is not.** Only **3.2%** of its mass sits inside the allowance; applying it moves the
reading by **0.12 points** (3.80% → 3.68%) and does not touch the largest blob at all. The
majority sits at **median hue 234** — 87° from the adopted band's nearest edge and 49° from the
allowance's. **That is the branch-3 condition, and this session halts on it.**

## 4. What the flagged population actually is

Characterised rather than merely counted, since the ruling needs the object and not the number:

| | view 1 | view 5 |
|---|---|---|
| off-band mass at hue 190–270 | **7,293 px · 1.486% of figure** | 978 px · 0.199% |
| connected components | **121** (largest 1,342 / 1,174 / 1,047) | 114 (largest 104 / 80 / 63) |
| median colour | **rgb(26,65,76)** · L\* 25.4 · C\* 14.4 · h 234.9 | rgb(71,89,109) · L\* 37.2 · C\* 13.6 · h 264.3 |
| within 2 units of the inherited C\* 12.0 floor | **43.7%** | 58.7% |

**Spatially it traces occlusion crevices, on both views.** On view 1 the overlay marks the
throat/shoulder crevice, the wing-body gap, the base of the dorsal ridge, the roots of the tail
spines and the leg creases. On view 5 the same signature runs along the spine bases and the
wing struts' shadow sides, where it is dwarfed by the membrane stratum. **It is many small dark
seams, not one region** — 121 components for 7,293 px.

**This is S-occlusion**, pre-registered in `canon/DRAGON-IDENTITY.md` before any generation
existed: *"the throat/shoulder crevice and the hard-stepped throat bands… paint will render it
as a dark seam, and no texture pass can restore geometry it does not have."* The fixture
anticipated the seam. **What no one anticipated is that the seam would carry a hue, and that the
hue would be cool.**

## 5. Three candidate diagnoses, none of them ruled here

Stated as alternatives with their arithmetic, because choosing one is the advisor's and choosing
it *while looking at the artifact it would judge* is the move this repo forbids.

1. **The chroma floor is too low for this subject.** 12.0 is W3's, inherited unchanged through
   the galleon and **never derived here**. 43.7% of view 1's flagged mass sits within 2 units of
   it. But raising it is not free, and the cost is measured:

   | floor | removes of the flagged population | **also drops of the figure's own IN-BAND mass** |
   |---|---|---|
   | 13 | 24.7% | — |
   | **14** | 43.7% | **32,305 px = 6.58% of figure** |
   | 16 | 68.4% | 78,276 px = 15.94% |
   | 18 | 84.0% | 142,118 px = 28.95% |

   A floor that removes even half the seam population takes a sixth of the subject's declared
   colour below the line with it.

2. **A cluster-derived palette structurally cannot represent a diffuse population.** The bands
   come from a 14-cluster k-means with a 0.4% floor — **3,927 px**. This population is 7,293 px
   spread over **121 components**, none larger than 1,342. It can never form a cluster, so it
   could never have entered the band table, and it was invisible to every handoff-7 measurement.
   **The per-pixel gate and the cluster table are different instruments at different resolutions,
   and this is the first place they disagree.**

3. **The fixture has no element for it.** Eleven elements name surfaces; none names a seam. D3 is
   `storm-grey`, D11 `dark slate` — both neutral by declaration and both measured below the floor.
   A cool dark seam is not any of them, and it is not "material the specification never named" in
   the sense the gate was built to catch either. **S-occlusion was declared as geometry, not as a
   material** — and the gate only knows materials.

**No floor is moved, no band is widened, and no word is changed in this report.** Withdrawing or
re-deriving either is the ruling's, from a baseline measured before the arm it judges.

## 6. Predictions scored

| # | prediction | outcome |
|---|---|---|
| **P1a** | gate fires on the pair; view 5 6–14% blob > 10,000; view 1 0.5–4% blob 500–8,000 | **held on all four numbers** |
| **P1b** | the allowance drops both views but not to zero | **held for view 5** (8.19% → 3.71%); **falsified for view 1** — predicted below 1%, measured 3.68%, because the allowance is nearly irrelevant there |
| **P1c** | **no other firing on the pair** | **FALSIFIED — and it is the halt.** 58.3% of view 1's mass is a third population at median hue 234 |
| **P1d** | the gate never measures the backdrop | **held** — it masks to the geometry silhouette |
| **P2a** | `palette_gate.py` raises `TypeError` on a null blob bound | **held exactly**, proven on the galleon's published file |
| **P2b** | both beast bounds written null, `--report-only` | **held** |
| **P3a** | anchor 0 differing px on views 1 and 5 | **held** — IoU 1.000000 |
| **P3b** | all eight silhouettes 490,941 px in mirror pairs | **falsified in its constant, held in its reason** — four mirror pairs at four sizes; my over-generalisation |
| **P3c** | frame agreement 0 px on all eight | **held** |
| **P3d** | views 1 and 5 reproduce 108,887 / 88,717; others 60k–130k | **held on both clauses** |
| **Q4, Q5** | resemblance-bleed per view; registration; garment-class invention; re-rolls | **NOT TESTED — no twin exists.** They stand unscored for the re-dispatch |

**The discriminating prediction (view 4's claws) was not reached.** It stays live and unspent.

## 7. What this session does not settle

- **Whether the gate is mis-constructed, and if so where.** Three candidates in §5, none ruled.
- **Everything about the twins.** None exists. Q4 and Q5 are unscored.
- **Whether the allowance should be adopted for view 5.** It works there — 8.19% → 3.71% — but
  adopting half a gate while the other half halts is a ruling, not a session's call.

## 8. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions hashed and blob-pinned before the masks, the gate and the palette file existed; the geometry driver saved as `E12_twins/E12_twins_geom.ps1` with its own diff-from-handoff-4 header; the palette file is a transcription citing the ruled values and their report; every reading carries its band, floor, view and mask |
| ANDON_AUTHORITY | **3** | **The dispatch halted at a pre-registered branch rather than improvising past it** — nothing was submitted, no floor was moved, no band widened; the instrument defect was proven before it was fixed and the guard re-proven to fire afterwards; the suspended band was kept out of `allowed_bands` so it could not silently arm the branch it was meant to test; anchor and frame-agreement gates run before any spend |
| NAMED_COMPENSATORS | **3** | 0 credits and 0 generations, so nothing irreversible occurred; all writes in the new `E12_twins/` tree plus one new canon transcription and one report; `profiles/beast.json` untouched; the one tool edit is additive and preserves the armed-bound path, proven by test |
| DECOMPOSE_BY_SECRETS | **3** | Masks and controls derive from this mesh; the gate derives from ruled bands cross-checked on the accepted pair and from nothing the twins would produce; the canny arrives from the profile now that Ruling 11a ratified it, so silence is correct where a flag was previously the deviation |
| UNCERTAINTY_GATED_HUMANS | **3** | The halt hands the advisor an object rather than a number — three candidate diagnoses with their costed arithmetic and no choice made among them; the floor's cost table is reported precisely so that raising it cannot look free |
| EXTERNAL_VERIFIER | **2** | The gate was validated against an artifact the Director accepted and the gate's authors did not generate, which is what caught this; the tool's repair was checked in both directions. Marked 2 because one pair is the whole calibration set, and `skip:` on a second model per the arc's precedent |

---

**HALT at Task 1, branch 3, with nothing generated.** The pair-validation, the overlays, the
decomposition, the floor cost table and the scored predictions go to the **advisor's eye**. Tasks
2 and 3 (the eight twins, the per-twin gate and registration) did not run and are not partially
done — the masks and controls they need are staged and complete. **This is what validating the
gate on the pair first is for: the alternative was eight generations judged by an instrument
that flags an accepted artifact.**
