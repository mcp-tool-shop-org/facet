# E12 handoff 15 — the run to Gate 1: four strokes, finalize, pack, the five-column sheet

**Executor session, 2026-08-07.** Predictions registered blind in `1304b9f`
([E12-handoff15-predictions.md](E12-handoff15-predictions.md)), git blob `38775ea`, written
before the no-LoRA path was written and before anything ran. Step 0 halted once on its own
gate and was released by Ruling 26; that halt is
[E12-handoff15-halt.md](E12-handoff15-halt.md) and is not repeated here.

**0 credits. 4 generations, one per stroke, zero re-rolls spent.** Every job `succeeded`,
zero warnings. Watchdog alive before every local leg (1,939 MiB against the 31,200 ceiling).
Stage 1's atlas was **never opened for writing** — the base guard asserted it byte-identical
before each of the four commits, and it still hashes to `050f29fa…`.

**Four results carry this report.**

1. **The gate the texture arms have waited on since handoff 2 is passed: 0 UNDECIDED, exit 0**
   — 83 subject-data flags, 83 decided.
2. **Four strokes committed 99,643 texels and every guard held**, but they closed **48.70%**
   of the brush's territory against the ruling's pre-registered **71.60%** — my closure
   predictions are falsified low across the board, and the cause is measurable.
3. **The register held.** None of the four drift signatures I named in advance appeared. What
   did appear is a fifth I had not registered: **the brush fills crevices dark and
   desaturated** — 2.39× more near-black than the paint it continues, at less than half its
   chroma.
4. **The mix reads two ways and both are true.** Of the whole atlas: 44.15% reference / 3.07%
   brush / 52.78% dilation. **Of the surface a viewer can actually see: 87.49% / 2.86% /
   9.65%.**

**Look at these before the numbers:** `E13_stroke/run/sheets/GATE1_HEAD_y45_3x.png` (the head
at 3× against the accepted pair) · `GATE1_y45.png` · `STROKE1_comp1_3x.png` (the dark-fill
finding).

---

## 0. Step 0 — the gate, passed

```
[sweep] 83 SUBJECT-DATA flags on this route; decided 83  (_not_on_route 3,
[sweep]   _tools_not_on_route 16, value 64)
[sweep] every subject-data flag on this route carries an explicit decision.
SWEEP EXIT CODE = 0
```

Certificate `E13_stroke/run/sweep_after_r26.txt`. The capability and its anchor were delivered
before the halt and are unchanged: all six of the ship's recorded stroke graphs rebuild
identical with the card present, and the no-LoRA branch is 16 nodes differing by exactly the
loader node. **P1a, P1c held; P1b falsified** and its 20% branch was the one that happened.

Every stroke's graph printed the register scan: `decided lora-w 0.0; loader nodes NONE; card
references NONE; 16 nodes`. **No saltroad card was loaded onto this dragon at any point.**

## 1. Task 1 — the four strokes

| # | camera | anchor GATED | (sim) | thin withheld | emit figure / hole | **committed** | (sim) | ratio | invar | 16e | achrom |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 292.5 | **87.96%** | 92.34 | 11,855 · 2.5% | 468,941 / 187,904 | **29,719** | 41,374 | 0.718 | mean .048 cc 111 | 8.03% | 10.60% |
| 2 | 337.5 | **93.24%** | 87.93 | 21,603 · 4.0% | 537,775 / 162,563 | **21,097** | 31,864 | 0.662 | mean .039 cc 46 | 5.36% | 7.57% |
| 3 | 180.0 | **92.02%** | 87.72 | 21,881 · 4.2% | 520,644 / 128,507 | **24,106** | 42,345 | 0.569 | mean .033 cc 18 | 1.10% | 9.76% |
| 4 | 45.0 | **95.03%** | 81.87 | 14,651 · 3.0% | 490,941 / 168,090 | **24,721** | 30,923 | 0.799 | mean .038 cc 21 | 5.05% | 13.99% |

Total **99,643** texels. Holes 1,809,823 → **1,710,180**. Run log: `run/run_log.jsonl`.

**P2c held** — thin-extent 0.005, live for the first time, withheld **2.5–4.2%** of each
stroke's figure, inside my 2–6% band and nowhere near the 10% line I set as "the guard is not
doing what Ruling 25c ruled it to do". The value behaves as the ladder said it would.

**P2a and P2b are falsified low.** Realised/simulated ran **0.569–0.799** against my predicted
0.75–0.95, and the total 99,643 sits under my 110,000–139,000. The cause is not mysterious and
it is not the brush: commit re-applies its own facing, visibility and 4 px edge test to the
brush's output, and the simulation modelled those on the *texel* set while commit applies them
to *bilinear samples of a raster the brush has repainted*. Stroke 3 is the extreme (0.569) and
is also the stroke whose emit hole count was smallest — it had the least to work with after
three strokes had already taken the shared rim.

**P2d falsified, and the falsification was mine to fix mid-run.** I predicted run-time anchors
within ±3 points of the simulation. The first version of the check returned **57.42%** on
stroke 1 against a simulated 92.34% and **halted the run**. That was a false halt on an operand
I had built wrong: `mask.png` is the hole map dilated by mask-dilate, measured at **2.40× the
hole set**, so defining `painted = hit & ~job` subtracts a collar of genuinely painted surface
and the fraction falls by construction. Measured three ways on the same job:

| operand | stroke 1 |
|---|---|
| (A) `hit & ~job mask` — the brush's fixed context | 57.42% |
| **(B) `hit & ~undilated holes` — the simulation's operand, now GATED** | **87.96%** |
| (C) (B) asked of the undilated holes only | 71.13% |

(B) lands 4.38 points under the simulation, the ruling's basis stands, and the tool is
corrected in place with the measurement that overturned it. (A) is now reported and never
gated — no bound for it exists in the record, and inventing one while looking at the number it
would judge is the move that is always wrong. Final anchors: **87.96 / 93.24 / 92.02 / 95.03**,
and **0 px in components touching no paint on all four**.

**The stroke I pre-registered as most exposed was the best-anchored one.** Yaw 45 had the
lowest *simulated* anchor (81.87%) and measured the **highest** at run time (95.03%) — because
by stroke 4 the other three had painted the shared rim it opens against. The spiral order
working, visible in a number.

**P4d held**: 0 re-rolls of 4. **P4b held**: achromatic 7.57–13.99% inside 6–17%. **P4a
marginally falsified**: 16e ran 1.10–8.03% against my 4–25%, with stroke 3 below the floor.
**P4c held and matters** — the gates measure the whole frame, of which the brush's contribution
is 1–3%, so these numbers cannot see a stroke and none of them decided anything. Registered in
advance so a quiet gate is not read as a pass.

*One instrument note, reported not fixed:* `e12_twin_readout`'s key-health column flags the
stroke frames as "GRADED backdrop" with ring and bg both `rgb(107,107,107)`. An emit frame's
backdrop is hole-grey 0.42, not the twins' lavender, so its registration IoU column is not the
twins' quantity on these frames and is not quoted as one.

## 2. The register — held, with a fifth signature I did not register

Pre-registered procedure (P3d): look at stroke 1 before running strokes 2–4. Done, at 3×.

**None of the four named signatures appeared.** No gloss/CG-smooth patch; no palette drift into
undeclared families; no value or hue step at the mask boundary; no anatomy that fails to
continue. Palette, register and identity are carried: same moss-green hide, same pale ventral
plates, same warm membranes, same orange eye, same ivory horns.

**What did appear is a fifth thing, measured rather than only seen** (stroke 1, brush-painted
pixels on surface against stage-1 paint in the same frame):

| | brush | stage 1 | |
|---|---|---|---|
| luma median | 0.306 | 0.381 | |
| below luma 0.08 | **12.77%** | 5.34% | **2.39×** |
| below luma 0.20 | 29.68% | 14.63% | 2.03× |
| chroma median | **0.075** | 0.169 | 0.44× |

**The brush fills crevices with dark, desaturated paint.** Visible at 3× in
`STROKE1_comp1_3x.png`: where the pre-stroke frame had legible frill spikes separated by grey
holes, the post-stroke frame has them merged into a near-black field. Charcoal and dark slate
*are* declared materials, so this is not a family violation — it is a legibility question, and
it is the Director's. My stop condition named (i)–(iv) and none fired, so the run continued;
had I registered "dark fill" in advance it would have been a harder call, and I am recording
that I did not.

## 3. Task 2 — finalize, pack, renders

```
[finalize] filling 1,710,180 hole texels (surface-aware)
[finalize]   median triangle edge 0.00231 (measured on this mesh)
[finalize]   source distance median 0.00212 = 0.92 edges  p95 0.00798  max 0.06672
[finalize]   beyond 5 edges 2.50%   beyond 20 edges 0.021%
[finalize]   normal disagrees >60deg 82.25%  back-facing 78.91%  (REPORTED, not gated)
[finalize] done, 0 texels took mean fallback
```

**P5a marginally falsified**: 1,710,180 against my 1,655,000–1,700,000. The arithmetic was
right and the input was wrong — 1,605,206 unreachable plus 104,974 the strokes left, not the
58,111 the ruling pre-registered at full closure. **The median lookup travels 0.92 triangle
edges** and 0.021% go beyond 20, so dilation is drawing from immediate neighbours almost
everywhere. The two high percentages on the last line are E07 Gate 0.5's recorded diagnostics,
not gates: that normal-disagreement proxy inverted on sheet-like geometry and halted a correct
arm once, which is why it reports.

`bake_hero_pack` → `dragon_hero.glb`, **43.9 MB**. Eight flat route-yaw renders and eight
provenance renders through the same emit path.

### The mix, with both denominators

| | of ALL valid (3,240,510) | of the REACHABLE set (1,635,304) |
|---|---|---|
| **REFERENCE** (stage 1's twins) | 1,430,687 · **44.15%** | 1,430,687 · **87.49%** |
| **BRUSH** (the four strokes) | 99,643 · **3.07%** | 46,736 · **2.86%** |
| **DILATION** (finalize) | 1,710,180 · **52.78%** | 157,881 · **9.65%** |

The ship ran 36.89 / 6.87 / 56.24; the character 68.8 / 4.2 / 27.0. **P5b marginally falsified**
(brush 3.07 against 3.4–4.3; dilation 52.78 against 51.6–52.5), both by the same cause as P2b.

**P5c is falsified in the direction that matters, and it is the number I would put in front of
the Director first.** I predicted the provenance panel would be "mostly dilation-coloured".
It is mostly **green**. Dilation is 52.78% of the *atlas* because this animal hides **49.54%**
of itself from every eye-level camera — under folded wings, in the wing-body gap, inside the
mouth. Of the surface anyone can see, **87.49% is stage-1 reference paint**. Reading 52.78%
against the character's 27% would be the wrong-denominator error this arc keeps paying for.

## 4. Task 3 — Gate 1's five-column sheet

`run/sheets/GATE1_y{0,45,90,135,180,225,270,315}.png` — **reference | asset | provenance |
error | clay**, one camera, one framing, full width, the house form. Reference is the
**accepted pair** at yaws 45 and 225 (Ruling 14's two views) and the harmonized twin
elsewhere, labelled per panel. Asset is FLAT. Provenance is green/amber/violet.

Plus the head at **3×** at yaws 0 and 45: `GATE1_HEAD_y0_3x.png`, `GATE1_HEAD_y45_3x.png`.

Error inside the silhouette, mean levels: **21.77–27.67** across the eight, lowest at yaw 315
and highest at 225. That number carries a caveat that keeps it from being read as a defect
score: the reference is a *lit diffusion render* and the asset is a *flat texture readout*, so
a uniform difference is expected and only its **localisation** is informative.

**P6a held.** The head reads softest at 3× — the frill spikes the clay separates crisply are
merged in the asset — and nothing in this run touched the head. A2's banked finding is the
explanation already on the record: the 4096 atlas carries **0.815 texels per full-figure head
pixel**, so the head is resolution-limited before any stroke. **P6b held**: the wing membranes
and their trailing edges are the most-changed region, which is where the strokes were sent.

## 5. Prediction scorecard

| # | class | verdict |
|---|---|---|
| P1a anchor byte-identical | CODE-READ | **held** — 6 of 6 |
| P1b sweep 0 UNDECIDED (80/20) | DERIVED | **FALSIFIED** at step 0; the named 20% branch |
| P1c no-LoRA graph 16 nodes | CODE-READ | **held** |
| P2a ratio 0.75–0.95 | DERIVED | **FALSIFIED low** — 0.569–0.799 |
| P2b total 110k–139k | DERIVED | **FALSIFIED low** — 99,643 |
| P2c thin withholds 2–6% | DERIVED | **held** — 2.5–4.2% |
| P2d anchor within ±3 pts | DERIVED | **FALSIFIED** — +4.3 to +13.2, after I fixed my own operand |
| P3a register holds 1–3, 4 exposed | BLIND | **held on the register; falsified on which stroke** — 4 was the best-anchored |
| P3b the four drift looks | BLIND | **none appeared**; a fifth, unregistered one did |
| P3c frame is not the risk | DERIVED | **held** — no drift attributable to framing |
| P4a 16e 4–25% | DERIVED | **marginally falsified** — stroke 3 at 1.10% |
| P4b achromatic 6–17% | DERIVED | **held** — 7.57–13.99% |
| P4c gates cannot isolate a stroke | DERIVED | **held**, and they decided nothing |
| P4d 0–1 re-rolls | DERIVED | **held** — 0 of 4 |
| P5a dilation 1.655–1.700M | DERIVED | **marginally falsified** — 1,710,180 |
| P5b mix 44.1 / 3.4–4.3 / 51.6–52.5 | DERIVED | **marginally falsified** — 44.15 / 3.07 / 52.78 |
| P5c dilation is the majority provenance | DERIVED | **FALSIFIED where it counts** — 9.65% of reachable |
| P6a head reads softest | BLIND | **held** |
| P6b membranes most changed | BLIND | **held** |

Nine held, seven falsified, three split. Two of the falsifications are mine as an instrument
author (P2d's operand, P1b's transcription), and both were caught before anything was believed.

## 6. What this session does not settle

- **Gate 1.** Nothing here is a verdict. The sheets are built and the halt is his.
- **The dark crevice fill.** Measured, shown, unregistered in advance, and not adjudicated.
- **The head's softness.** A2's allocation arm is specced and waiting (Ruling 24d); this run
  could not and did not address it.
- **Whether 48.70% closure is enough**, or whether more strokes are worth their spend — the
  greedy's remaining candidates are on the record (handoff 14 §2) and this run did not re-derive
  them.

## 7. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions blob-pinned before the tool was touched; every stroke's workflow saved before submission with content-hash inputs; `run_log.jsonl` carries prompt ids, seeds, node counts, anchors, thin withholding, closures and gates per stroke; three saved recipes; the sweep certificate and anchor log on disk |
| ANDON_AUTHORITY | **3** | The registry gate halted the run at step 0 and stayed halted until a ruling cleared it; the anchor check halted stroke 1 and was **corrected rather than tuned past**, with the measurement that overturned it in the file; the base guard fired inside the commit tool on all four strokes; the invariance check is in-tool and no shell chained it |
| NAMED_COMPENSATORS | **3** | 0 credits, 4 generations, `estimate_credits` first; the accumulating state is a COPY and stage 1's atlas hashes unchanged after all four commits; every job dir retains its render, mask, hit, thin, cam and inpainted; nothing overwritten |
| DECOMPOSE_BY_SECRETS | **3** | The capability was anchored on the other subject's recorded graphs; prompts, order, thin-extent and every recipe key arrived from ruled artifacts through committed tools; the register moved out of a tool constant into the subject's profile |
| UNCERTAINTY_GATED_HUMANS | **3** | The drift risk was pre-registered with its own look AND a stop procedure, and the procedure was executed before strokes 2–4 ran; the mix is quoted against both denominators so the geometry is not mistaken for regression; every falsified prediction is reported as falsified |
| EXTERNAL_VERIFIER | **2** | The palette gate and achromatic channel grade against a specification the brush did not write; the anchor tests new code against the old path's output on a different subject; the five-column sheet puts the asset beside the thing it is meant to look like. `skip:` per precedent |

---

**Tasks 0–3 complete. HALT at GATE 1.** The sweep certificate, the anchor evidence, four
strokes with their guards and gates, finalize and pack, the eight five-column sheets and the
head at 3× are staged. **To the advisor's eye first, then the Director's — Gate 1, at the
exemplar bar.** Nothing past the halt ran; the E11 export lane and any dataset ingest wait on
his verdict.
