# E35 — clean twins: executor report

**Seat:** executor · **Run:** 2026-08-14 · **Spec:**
[E35-clean-twins-kickoff.md](E35-clean-twins-kickoff.md) · **Predictions:**
[E35-predictions.md](E35-predictions.md), registered blind after tasks 0–1 and before the
first cloud job · **Grounding:**
[E35-speck-research-grounding.md](../research/E35-speck-research-grounding.md)

**HALTED AT GATE R.** The register is the Director's ruling and the spec makes it a hard
stop. Tasks 3 (corrector), 4 (repaint) and 5 (close) are not run. **This report carries no
verdicts** — no candidate here is called good, better or acceptable.

**Cloud spend: 8 jobs of the 45 ceiling** (2a=3, 2b=3, 2c=2). Zero partner-API nodes. The
conditional arms (2e bf16, stochastic sampler) did **not** fire.

---

## 0. Gates at open, and one that fired

| gate | result |
|---|---|
| E15 index ritual, scratch `--db` | **19/19, VERIFY PASSED — all four legs**, 35 experiments |
| manifest A `facet_E33` | 117 declared / 117 present, **0/0/0** (its known stale self-reference reported, not counted) |
| manifest B `facet_E34` | 84 declared / 84 present, **0/0/0** |
| manifest C eight subtrees | **7,312 files / 17,072,807,610 bytes** — reproduces the recorded figures exactly |
| watchdog heartbeat | **ADVANCING** 14:18:55 → 14:19:53, log ticking ~2 s, `ok`, VRAM 7,186 MiB |
| interpreter | py 3.13.13 · numpy 2.4.6 · scipy 1.17.1 · PIL 12.2.0 (premise 5 holds; no new dependency) |

⚠ **The manifest gate FIRED at open, on my own instrument.** First run: leg B reported
`added 1 (+E34_manifest.json)` → `MANIFEST GATE OPEN: FIRED`. Cause: `E34_manifest.json`
declares `excludes_self: true` and is absent from its own file list by construction; my walk
did not honour the flag. **Nothing about `facet_E34` had changed.** The repair honours the
manifest's declared exclusion — it adds capability and removes no coverage — and before the
repaired leg was trusted a can-fail fixture ran: clean → HELD, intruder file → FIRED,
changed byte → FIRED, removed file → FIRED. Reported here rather than smoothed into a green
row.

---

## 1. Task 0 — mechanics. Every premise closed, one of them by enumeration

### 0a — the parked-face patch is located, sampled, and **exonerated**

From `bake_hero_prep.py:335-343` with E33's recorded invocation (`--res 4096`,
`--unseen-strip` 24.0; 151,439 faces parked):

```
corners UV  (0.010000,0.995605) (0.012441,0.995605) (0.010000,0.998047)
pixels      rows 8..18, cols 40..51        a right triangle, 10 texels a side
visible UVs are scaled  v *= (1-strip)  ->  every visible face lands at rows >= 24
```

| measurement | value |
|---|---|
| patch colour in the final atlas | mean **(144.83, 102.58, 77.25)**, range (139,98,72)–(149,106,80) |
| patch min L1 to the pure-black speck (11,9,8) | **281** |
| route-valid texels inside rows 0..23 | **278** of 2,444,770 (**0.011%**) — the patch plus dilation |
| hole texels' colour | mean **(144.7, 105.3, 80.4)**; **0.00%** within L1 ≤ 12 of the speck |

**Both candidate mechanisms named at the E34 seat carry mid-tone terracotta.** Premise 6
closes: the patch is not the source, and unfilled texels are not either.

### 0a follow-up — the census on the ROUTE's own valid mask

The E34-seat notes named exactly one open follow-up: their operand was the wider prep mask.

| operand | valid | core `max(RGB)<40` | wide `<60` | darkest `max(RGB)` |
|---|---|---|---|---|
| prep mask (E34-seat operand) | 2,730,693 | 1,495 | 18,492 | 25 |
| **route valid (painted ∪ holes)** | **2,444,770** | **1,314** | **16,660** | 25 |
| painted only | 2,287,542 | 738 | 12,725 | 25 |

The operand fix moves core **−12.1%** and wide **−9.9%**.

### 0a remainder — the pure-black sub-population is **not paint at all**

The (11,9,8) sample came from `turn_final_flat\armflat_1.png`, a **render**. Measured
against the geometry mask for that view (91,415 px, 25.36% of frame, bbox rows 87–936 ×
cols 70–284; the render's alpha is uniformly 255 so an alpha test would have returned the
whole frame, and corner-median keying is retired here):

- **6 pixels** within L1 ≤ 12 of the value, **0.0% at the silhouette**, median 8.8 px from
  it, **all 6 surviving a 2 px rim erosion** — interior, not an edge artifact.
- At all six: **clay bright (177–219)**, **twin mid-tone terracotta (max 123–170), dark at
  none of them**, E33-lit and E34-lit dark at near-identical values (the repaint did not
  touch them).
- **The value exists nowhere in the texture.** Final atlas: **0** texels within L1 ≤ 12;
  darkest route-valid texel **(25,8,0)**, min L1 **23**. The GLB's embedded copy censuses
  identically — 0 within L1 ≤ 12, 7,585,131 exactly (0,0,0), 5,855 in 1..39.

**Consequence, load-bearing for this arc:** the sub-population is produced downstream of
the texture, so **no twin-side change can reach it**, and a flat-light census on any
repainted candidate carries it as a floor. **Mechanism: UNMEASURED.** Leading candidate is a
UV landing in the atlas's unpainted gap (7,585,131 such texels) — reaching (11,5,3) from
terracotta needs ~**98.7%** background weight in linear space, which a 2×2 mip blend at an
island edge does not supply but a UV outside an island's dilation margin does. Named, not
asserted; settling it needs a UV pass this task did not run.

### 0b — VAE precision (premise 3): holds, and closes a branch by enumeration

`VAELoader.vae_name = qwen_image_vae.safetensors`, resolving to
`Comfy-Org/Qwen-Image_ComfyUI/split_files/vae/` — **no quantization suffix**, while the same
graph's backbone and text encoder both carry theirs (`qwen_image_fp8_e4m3fn`,
`qwen_2.5_vl_7b_fp8_scaled`). **The VAE is unquantized.** And the catalog offers only two
qwen VAEs (`qwen_image_vae`, `qwen_image_layered_vae`) — **no quantized variant exists to
A/B against**, so the grounding's "a VAE-precision arm outranks the bf16 swap" branch has
**no operand**. Closed by enumerating the resource, not by judgment.

### 0c — the graph's capability surface (premises 2 and 4), verbatim

The recipe's 14-node graph: `UNETLoader · CLIPLoader · VAELoader · ControlNetLoader ·
ModelSamplingAuraFlow · CLIPTextEncode ×2 · LoadImage ×2 · ControlNetApplyAdvanced ·
VAEEncode · KSampler · VAEDecode · SaveImage`.

**Premise 2 — MEASURED, PRESENT.** `ControlNetApplyAdvanced` exposes `start_percent`
(FLOAT 0–1, default 0) and `end_percent` (FLOAT 0–1, default 1) beside `strength` (FLOAT
0–10). The payload runs **0.9 / 0.0 / 1.0**. Arm 2c was therefore **not** forced to a flat
cut.

**Premise 4 — MEASURED, PRESENT.** `KSampler.sampler_name` is a 63-option COMBO on the same
node — a drop-in needing no rewiring — including `euler_ancestral`, `euler_ancestral_cfg_pp`,
`dpm_2_ancestral`, `dpmpp_2s_ancestral`, `dpmpp_sde`, `dpmpp_2m_sde`, `ddpm`,
`res_multistep_ancestral`, `er_sde`, `sa_solver`. `scheduler` offers 11.

**Bearing on R-c:** `UNETLoader.weight_dtype` is `default` with the fp8 carried in the
*file*; `qwen_image_bf16.safetensors` **exists** in the catalog, so the conditional swap had
an operand. The text encoder is *also* fp8, so a backbone-only swap would not have isolated
it. The arm did not fire (see 2a).

---

## 2. Task 1 — the detector. Its first implementation FAILED R-a, and the failure is the useful part

**It fired 153 times on a CLEAN clay control against 104 on the twin the Director rejected**
— backwards, and exactly what R-a exists to catch. Measured cause: it implemented only the
*dark* half of the spec's "dark-**chromatic**" deviation map, so it was reading **geometry
shading**, whose blobs carry median chroma **3.0** against the twin's **54.2**. Absolute
darkness does not separate them (0 clay vs 5 twin blobs below max-RGB 60); **chroma
separates them 25×**.

The floor is derived from two sources that are **not** the twin under test — the class's own
recorded cores, (70–95, 40–60, 15–40) → **C\* 22.7–24.6**, and the control's neutral
Workbench clay at **C\* 0.9** — and sits between them at 8.0. **It was not scanned.** The
same law is already load-bearing in `palette_gate.py`.

**A second defect was worse in kind: the size bound was on the wrong operand.** A local
median is blind *inside* a structure wider than its window, so a planted 20×20 region read
as four 23 px² **corners**, each under a 36 px² threshold. On a twin that would have counted
the corners of every dark garment forever. The bound now applies to the connected
**same-colour structure**, using the tool's existing ΔE unit so no new threshold enters.
An intermediate ring-ΔE discriminator was built, measured (14.8 for corners vs 23.2 for a
speck — a real gap whose cut would have had to be chosen *after* seeing it), and **kept as a
reported diagnostic rather than promoted to a gate**.

**T66 rides the commit:** 25 tests — planted fixtures with exact censuses, every ANDON shown
firing with a companion success, `-O` and `PYTHONOPTIMIZE=1` survival, and R-a's two legs.
**R-a is green:** fires on all six rejected twins, silent on all three clay controls, through
the *same masks* so the separation cannot be a difference in which pixels were looked at.

### The baseline table

| unit | view 1 | 8-view total | range |
|---|---|---|---|
| twin census (E34 r3) | **16** | **202** | 9 – 43 |
| flat census (the accepted asset) | **102** | **733** | 70 – 133 |

⚠ The "14 recorded twins" are **12 distinct** files: E34 reused E33's `twin_r3_v0` and
`twin_r3_v4` byte-for-byte (confirmed by sha256), which is why only six payloads exist.

### The founding premise, re-measured — and it is weaker than the record states

The spec's premise 1 rests on the E34 attribution's line *"at 5 of 6 sampled speck locations
the twin is dark at the matching pixel."* Reproducing that sample this session with the same
code and seed: the six points **de-duplicate to TWO distinct locations**, five of them inside
one 7×9 px cluster — and that cluster measures as a **broadly dark shadow crevice** in the
twin (313/625 px below max-RGB 100 in its own 25×25, dL 3.5), not an isolated dot. The other
point has dL 2.0 and zero dark neighbours. **The premise rested on ~2 independent
observations, one of which is a shadow.**

Measured at scale instead — for all **733** dots detected in the rejected flat renders, what
does the twin carry at the same place:

| tolerance | twin DARK (chance) | twin SPECK (chance) |
|---|---|---|
| **0 px** | 13.0% (6.7%) **×1.92** | 14.3% (2.3%) **×6.13** |
| 1 px | 21.6% (10.0%) ×2.15 | 27.7% (5.6%) ×4.96 |
| 2 px | 28.2% (13.0%) ×2.18 | 36.2% (8.9%) ×4.07 |
| 3 px | 31.6% (15.9%) ×1.99 | 43.0% (12.2%) ×3.52 |
| 5 px | 38.1% (21.8%) ×1.75 | 50.2% (19.2%) ×2.62 |

The enrichment **decays monotonically with tolerance**, which is the signature of real
spatial correspondence rather than coincidence. **The twins are a genuine source and they are
not the only one:** 14.3% of rendered dots have a twin speck at the exact matching pixel.
(My first pass compared a dilated hit rate against an undilated null, which overstates every
tolerance above 0. The null is dilated here.)

---

## 3. Task 2 — the arms

### 2a — seed re-roll ×3 at the pinned recipe (3 jobs; seeds 770701, 424242, 987654)

| seed | census | area px² | reg-IoU | register C\* |
|---|---|---|---|---|
| 770700 (recorded R3) | 16 | 157 | 0.9372 | 23.77 |
| 770701 | 14 | 65 | 0.9442 | 29.00 |
| 424242 | 26 | 139 | 0.9041 | 32.69 |
| **987654** | **7** | **34** | **0.9529** | 25.67 |

**Do the dots move?** At **exact pixel, 5 of 6 seed pairs share ZERO specks**; the sixth
shares 1 of 16. Inter-seed silhouette IoU **0.9814–0.9865**.

⚠ **P1a's metric is WITHDRAWN as mis-specified, not re-derived.** It scored an enrichment
ratio, and with 7–26 specks the chance rate is 0.1–3.5%, so a single coincidental hit yields
"87.9×". The ratio cannot separate *stay* from *luck* at these counts — a pass condition on a
denominator too small to carry it, the family this repo has paid for four times. Per this
repo's own rule I **withdraw it and report numerator and denominator separately** rather than
inventing a replacement while looking at the results it would judge. The raw overlap needs no
threshold to be legible.

**R-c does not fire.** The bf16 swap was conditional on a *stay* outcome and the placements
do not stay.

### 2b — the denoise sweep (3 jobs) — the register dies before the specks do

| denoise | census | area px² | reg-IoU | reverted to init | register C\* |
|---|---|---|---|---|---|
| 0.92 (recorded) | 16 | 157 | 0.9372 | 0.50% | **23.77** |
| 0.85 | 10 | 72 | 0.9478 | 5.01% | **10.00** |
| 0.80 | 12 | 17 | 0.5107 | 36.66% | **3.91** |
| **0.72** | **0** | **0** | 0.4202 | **56.00%** | **1.89** |

**The census reaches zero at 0.72, and the terracotta reaches zero with it.** At full size
the strip is unambiguous: 0.92 is terracotta, 0.85 is pale greige, 0.80 is barely coloured,
0.72 is back to the white-grey clay init. **The specks vanish because the paint vanishes.**
The silhouette and pose survive every rung — the loss is *material identity*, not geometry.

⚠ **P2d fired (min reg-IoU 0.4202), and its instrument is confounded in exactly this
regime.** The figure is keyed by a border-ring background fit, and E01's law is that a grey
figure on a grey ground cannot be found by a threshold — which is what the low rungs are. The
uncontaminated columns are the two beside it: reverted-to-init and register C\*, and both say
the same thing more clearly than reg-IoU does.

### 2c — conditioning (2 jobs), reframed by the mid-arc correction

| arm | census | area px² | reg-IoU | register C\* |
|---|---|---|---|---|
| recorded (strength 0.9, end 1.0) | 16 | 157 | 0.9372 | 23.77 |
| scheduled (0.9, end 0.5) | 22 | 128 | 0.8308 | 24.29 |
| flat 0.65 | 13 | 143 | 0.9064 | 22.40 |

**Both land inside the seed-noise floor** (2a spans 7–26 in count, 34–139 px² in area), so
neither moved the class by more than a re-roll would.

⚑ **The advisor's mid-arc correction is absorbed and it reframes this arm.** The InstantX
card's 0.10–0.50 img2img band — grounding finding 8 — is **falsified at its cited source and
withdrawn**, so the sweep above hunts a knee on **theory grounds alone** (SDEdit's flat-guide
case; outline-first/details-later). The card's actual documented recommendation is
`controlnet_conditioning_scale ∈ [0.8, 1.0]`, which puts the **recorded 0.9 INSIDE the vendor
band** and makes **flat 0.65 a deliberately below-recommendation arm**. The scheduled arm
holds strength inside the band and shortens its reach instead. The correction arrived after
these two jobs were submitted; it changes their framing, not their numbers, and no prediction
was edited.

### 2d — fusion, K=3, zero cloud (T67 rides the commit: 15 tests)

| | census | area px² | register C\* |
|---|---|---|---|
| best single seed (987654) | **7** | **34** | 25.67 |
| median-of-3 fused | 16 | 67 | 29.07 |

**P4a misses in the wrong direction: fusion is worse than the best single seed**, 16 vs 7.
The mechanism is not a defect — a median is a **majority vote**, so it lands near the middle
of its inputs (14/26/7 → 16), not below their minimum. Beating the best member needs
*selection*, which is the grounding's named upgrade path and which the census now makes
possible as a scorer.

**P4b misses and the structural ANDON would have halted:** largest connected disagreement
**35,303 px²** against a 200 px² bound, covering 62.33% of the figure. The diagnostic
underneath: max-deviation across the figure has median **6.70 ΔE**, just above the 6.0
threshold — the seeds differ *mildly everywhere*, and those pixels merge into one blob.
Coverage at other thresholds, reported and **none adopted**: ΔE≥10 → 17.84%, ≥15 → 5.39%,
≥20 → 1.86%, ≥25 → 0.79%. **Per P4b's own pre-registered falsifier, fusion is rejected and
selection-not-fusion is the noted upgrade path.** I do not re-derive the bound.

⚠ T67 caught a real bug in its own tool before any number was quoted: the disagreement map
first used a **median** absolute deviation, which at K=3 with one dissenting seed is
`median([large, 0, 0]) = 0` — blind in exactly the case fusion exists for. It read **zero on
five planted disagreements**. The aggregator is a **max**.

---

## 4. Predictions, scored

| # | prediction | outcome |
|---|---|---|
| P1a | dots move; enrichment < 2.0× | **WITHDRAWN — metric mis-specified** (see 2a). Raw: 5 of 6 pairs share zero specks at exact pixel |
| P1b | each seed's census in 8–30 | **MISS** — 14, 26, **7** (one below band) |
| P1c | seed spread ≤ 2.5× | **MISS** — 26/7 = **3.71×** |
| P1d | inter-seed silhouette IoU ≥ 0.90 | **HIT** — 0.9814–0.9865 |
| P2a | census falls monotonically | **HOLDS under its own falsifier** — count 16/10/12/0 rises once by 1.2×, inside the 3.71× seed floor; area is strictly monotone 157/72/17/0 |
| P2b | 0.72 census ≤ 9 | **HIT** — **0** |
| P2c | a knee: largest drop ≥ 2× smallest | **HIT in area** — drops 85/55/17, ratio 5.0×. In count the sequence is non-monotone and the clause is not readable |
| P2d | reg-IoU ≥ 0.80 at every rung | **FIRED** — min 0.4202; instrument confounded in this regime (see 2b) |
| P2e | near-init fraction rises; 0.72 ≥ 2× 0.92 | **HIT, 55× over** — 0.50→5.01→36.66→56.00%, ratio **111.34×** |
| P3a | scheduled form available | **HIT** — measured in 0c |
| P3b | conditioning moves less than the denoise knee | **HIT** — inside seed noise |
| P3c | reg-IoU ≥ 0.80 for 2c | **HIT** — 0.8308 and 0.9064 |
| P4a | fused ≤ 50% of best single seed | **MISS, wrong direction** — 16 vs 7 |
| P4b | largest disagreement ≤ 200 px² | **MISS** — 35,303 px² |
| P5a | 8–13 jobs before Gate R | **HIT** — **8** |
| P5b | R-c does not fire | **HIT** |
| P5c | generation alone cannot reach flat-census 0 | **not yet testable** — needs task 4 |
| P5d | P2a is the least reliable clause | **partly** — P2a survived its own falsifier; P1b/P1c/P4a/P4b are the misses |

**Six misses, one withdrawal, ten hits.** The withdrawal is mine and is the one worth
carrying: **a ratio whose denominator is 0.1% is not a threshold**, and I wrote it into a
blind prediction file after fixing the same error in a task-1 instrument two hours earlier.

---

## 5. What the arc measured, stated without a verdict

- **At the approved register, only the SEED moved the class.** Seed 987654 carries **7
  specks / 34 px²** against the recorded R3's **16 / 157** — 2.3× fewer, 4.6× less area — at
  **C\* 25.7** against R3's 23.8, one changed integer and nothing else.
- **The denoise lever reaches census 0 and takes the terracotta with it.**
- **Conditioning moved nothing outside seed noise**, in or below the vendor band.
- **Fusion at K=3 does not beat its best member**, and its disagreement gate fires.
- **A twin-side fix has a measured ceiling**: 14.3% of rendered dots have a twin speck at
  the matching pixel, and the pure-black sub-population is not in the twins at all.

**The register ruling and the repaint configuration are the Director's, at Gate R.**

---

## 6. Compensator state at the halt

| action | state |
|---|---|
| cloud spend | **8 jobs** of 45 (≈ $0.14 at the measured $0.018/job). No compensator exists; bounded before spend and under budget |
| writes under `facet_E35\` | twins, payloads, census, diag. Undo = `rm -r E:\AI\training\facet_E35` |
| repo commits | local only. Undo = `git reset --hard 95f6c64` (tasks 0–1) or `f405328` (the advisor's tree) |
| push | **not performed** — the spec puts it at task 5, after the Director's ruling |
| `facet_E33` / `facet_E34` / eight subtrees | **unmoved**; re-verified at close below |

## 7. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every arm emitted through `make_payload.py` with an explicit override dict + base sha256 + payload sha256; both tools write JSON sidecars carrying every threshold, input hash, tool hash and library version |
| ANDON_AUTHORITY | 3 | four ANDONs fired this session and every one is reported with its evidence: the manifest gate, R-a's validation legs, P2d, and the fusion structural bound. None was tuned past |
| NAMED_COMPENSATORS | 3 | table above; the compensator-less cloud spend stayed at 8 of 45 |
| DECOMPOSE_BY_SECRETS | 3 | detection and fusion are separate tools; the census JSON is the interface; `make_payload.py` isolates what varies per arm |
| UNCERTAINTY_GATED_HUMANS | 3 | halted at Gate R with the sheet built at native scale before the metrics were read |
| EXTERNAL_VERIFIER | 3 | the detector validates against **Director-rejected artifacts**, not its author's fixtures; both tools' bugs were caught by their own tests rather than by inspection |

---

# ⚖ GATE R2 — tasks 6 and 7. HALTED for the advisor's mechanism ruling

**Run 2026-08-14 after the Gate R2 amendment.** Blind bands registered before any leg, in
[E35-task6-blind-bands.md](E35-task6-blind-bands.md). **Task 8 not launched.**

**Spend: 33 of 45.** Task 6 cost zero. Task 7 cost one — the archive-first check found no
parameter-identical pair among **34 recorded payloads**, so P7a missed and the one job fired.

## The Gate R ruling, recorded as the gate's outcome

The register HOLDS at the recorded recipe — denoise 0.92, cn_strength 0.9, the approved R3
register unchanged. The repaint configuration was K=3 seeds per view with the recorded seed
among them, census-scored best-of-K **selection** per view. Executed at task 4; its candidate
carries the pale-blotch class the Director caught, which is what Gate R2 exists to explain.

## What the discriminator measured

| leg | measurement | reading under the amendment's map |
|---|---|---|
| **6a** ownership overlay | pale boundary within 2 px of an ownership seam: **1,861 / 5,785 = 32.17%**; **35** pale regions span ≥ 2 owners | equivocal by construction — seams are dense on a head |
| **6b** seam-crossing | \|ΔL\*\| across seams **inside** pale regions **6.089**; **outside** pale regions **9.16** | a step exists — but it is **LARGER away from the blotches**, so seams are stepped generally and pale is **not** seam-defined |
| **6c** same view across seeds | **8 of 8 views** carry pale ≥ 25 px² at **all three seeds**; **87.7%** of pale pixels co-locate across ≥ 2 of 3 seeds within 10 px | **generation-side, stable across seed** |
| **6d** chroma vs luminance | C\* in pale **29.52** vs register **32.61** → drop **9.48%**; L\* **76.54** vs **59.87** → rise **+16.68**; pale px below the C\* 8.0 floor: **0 of 9,276 (0.00%)** | **L\*-dominant at essentially unchanged chroma** — not a desaturation collapse |
| **6e** frequency profile | pale-boundary gradient ÷ other-edge gradient = **0.92** | **smooth low-frequency lobes**, not step edges |
| **6f** the spread metric's own test | E34 **ACCEPTED** set (all seed 770700): C\* **8.42**, L\* **11.54**. E35 rejected set: C\* **9.77**, L\* **10.14** | **DOES NOT SEPARATE** — the accepted asset's L\* spread is *higher* |
| **6g** twins pre-projection | pale visible in **every lone twin, every seed, every view** ([sheet](../../../../E:/AI/training/facet_E35/diag/E35_6g_twins_by_seed.png)) | **not born at assembly** |

## Task 7 — consult calibration

No parameter-identical pair existed in the archive (34 payloads, 34 distinct parameter sets),
so one job re-submitted arm 2a's view-1 / seed-987654 payload verbatim.

**PNG bytes differ. PIXELS ARE IDENTICAL — ΔE 0.0000 mean, median, p95 and max; 0 of 360,448
pixels differ.** The byte difference is encoder metadata, which this repo's law already covers:
a PNG hash mismatch is not evidence a render changed. **Same-seed reasoning stands** on this
Cloud path; no per-job platform entropy was observed.

## Blind bands, scored

**7 hits, 6 misses.** HIT: P6a, P6a-2, P6c, P6d(L\* rise), P6e, P6g, P7b. MISS: P6b, P6b-2,
P6d(C\* drop), P6d-2, P6f, P7a.

**The miss that matters is P6f, and I called it in advance as the one I most expected to
miss.** The spread number — C\* 9.77 / L\* 10.14 — that I printed on the coherence sheet and
that seeded my own mixed-seed proposal **does not separate the accepted asset from the
rejected one**. E34's accepted set carries a *higher* L\* spread. Under the E07 law the metric
has no standing and gates nothing; it is withdrawn as evidence for any mechanism, including
mine.

**P6b missed in the direction that matters too:** I predicted continuity (< 3.0 L\*) and
measured a 6.089 step inside pale regions. But the same measurement away from the blotches
returns **9.16** — so the asset has a pervasive ~9 L\* seam step that is *not* what makes the
blotches, and my P6b-2 (inside ≈ outside) missed by 3.07.

## What the executor reports, without ruling

Two distinct terms are measured and they are not the same object:

1. **A pale wash present in every twin at every seed before any projection** (6c: 8/8 views ×
   3 seeds; 6g: visible in each lone twin; 6e: smooth lobes; 6d: L\*-dominant). No selection
   rule over these twins can remove what all of them carry.
2. **A pervasive mixed-seed seam step of ~9 L\*** (6b), real but *larger away from the
   blotches than inside them*, and whose motivating metric (6f) has just lost its standing.

**My own proposed remedy is not supported by this evidence.** Global-single-seed selection
deletes term 2 by construction and does nothing to term 1, which is where the pale lives.

⚠ **6d does not point the same way as 6c/6g**, and I am not resolving that: its map reads
"L\* shift at modest chroma ⇒ patchwork" while 6c/6g place the class in every lone twin
pre-projection. The two legs measure different stages — 6d the assembled render, 6c/6g the
twins — and the conflict is reported rather than adjudicated. **The advisor rules the
mechanism. Task 8 does not launch until that ruling issues.**

---

# ⚖ GATE R2 — tasks R2-a and R2-b. HALTED at the sheet for the Director's eye

**Zero cloud jobs. Spend unchanged at 33 of 45.** Blind bands in
[E35-R2a-blind-bands.md](E35-R2a-blind-bands.md), registered before the run with an explicit
non-blindness declaration: leg 6c had already printed per-seed pale **area**, so no band was
offered on it.

## R2-a — the anticorrelation, quantified

**The anchor was not a second population.** E34's eight accepted twins **are** the 770700
column (views 0 and 4 are E33's r3 twins, reused byte-for-byte). Enumerated before measuring.

| seed | mean pale area px² | mean pale L\*-rise | mean dark-speck area px² |
|---|---|---|---|
| **987654** | **1065.5** | **14.78** | **71.9** |
| 770701 | 858.1 | 14.75 | 129.0 |
| **770700** (E34 anchor) | **734.5** | **11.67** | **170.4** |

**The ruling's eye is confirmed at the level it was asserted, and only there.**

- Palest-first by area **and** by L\*-rise: **987654 > 770701 > 770700**. Both measures agree.
- Spearman ρ(dark-speck area, pale area) over the **3 seed means**: **−1.000** — perfectly
  monotone.
- Spearman ρ over the **24 individual twins**: **+0.018** — no relationship at all.
- The census-selected twin was also the **pale-maximal** twin on **3 of 8** views.

**So the selection optimised into the pale class through the SEED, not per view.** It chose
987654 — the palest seed on both measures — on 5 of 8 views because that seed carries the
fewest dark specks, while being pale-maximal per view only 3 times.

**Bands: 4 hits, 1 miss.** PR1 (rank agreement) HIT · PR2 (L\*-rise spread 2.0–7.0 → **3.11**)
HIT · PR4 (pale-maximal 2–4 of 8 → **3**) HIT · PR5 (anchor mildest on both) HIT ·
**PR3 MISS** — I predicted ρ −0.75…−0.25 and measured **+0.018**, because I stated the band
over individual twins where the effect lives between seed means. The band was measured at the
wrong level, not falsified.

## R2-b — the candidate, global-770700

Global-770700 selection → corrector (two passes, 1363 → 105 → **27 px²**) → the task-4
projection pipeline unchanged → finalize → pack.

**The projection reproduces the accepted asset exactly.** Registration per view **0.9063 /
0.9196 / 0.9479 / 0.8835 / 0.8475 / 0.9042 / 0.9349 / 0.8745** — E34's recorded table to the
digit; styled **2,287,542**; holes **157,228**; finalize source distance **1.82 edges**,
beyond-20 **0.333%**. Gates green, none fired.

**Candidate:** `facet_E35\r2b\out\performer_textured_clean.glb`.

### ⚠ The finding the Director should have before he looks

| asset | texture core-black | components | largest | flat census |
|---|---|---|---|---|
| E34 ACCEPTED | 1,314 | 57 | 377 | 733 / 4,122 px² |
| **R2-b global-770700** | **1,314** | **57** | **377** | **712 / 3,816 px²** |
| per-view mix (rejected) | 37 | 37 | 1 | 539 / 2,409 px² |

**R2-b's texture dark-class census is identical to E34's.** The corrector did not move it,
and the reason is structural rather than a failure: the atlas core-black class is dominated by
components up to **377 texels**, while the detector is bounded at **36 px²** by construction —
these are not specks and were never in its scope. Wide-dark moves only 16,660 → 16,454.

**The dark-class reduction in the rejected candidate came almost entirely from the SEED, not
from the corrector** (987654 carries 71.9 px² mean dark area against 770700's 170.4). So the
two candidates are a clean trade, now measured:

- **R2-b** — E34's tonal behaviour, no pale wash, and E34's dark texture census.
- **per-view mix** — dark texture census 35× lower, and the pale wash the Director rejected.

**Tonal-behaviour-equivalent to E34's inputs, NOT byte-equivalent** — task 7 found no
parameter-identical pair across the eras (34 payloads, 34 distinct parameter sets), so
equivalence is by seed and recipe, not by reproduction.

**HALTED at the sheet.** The cn ladder (0.7 / 0.6) stays authorized and held; it is the lever
that could move what neither seed choice nor the corrector reached. His word only.
