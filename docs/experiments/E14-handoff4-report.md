# E14 handoff 4 — the diagonal re-roll pass. HALT 3.

**Executor session, 2026-08-07.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 18b/18f.
Predictions committed blind in `86dfda5`, the halt-clause reading in `283a20d`, both before any
graph was built. Task 2's report and Rulings 17/18 are at `3011035` / `080d90f`.

**Nothing is judged here.** Four submissions, one variable, every measurement report-only per
17d. **Cost: 0 credits** — `estimate_credits` returned "no paid API nodes" on all four; this is
GPU time on the subscription, not metered spend.

**The branch resolved to the FIRST exit: all four diagonals landed iron, 0.0% gold on L2's arms
in every case.** Two things moved that nobody asked about, and they are the same thing: **the
L5 gem drifted magenta on all four re-rolls, and that drift is what made the standing depth
diagnostic fire.** Both are in sections 6 and 7 and neither is disposed of here.

---

## 1. Pre-flight — nothing had drifted, and it was checked rather than assumed

The dispatch asserts stems, controls and recipe unchanged, and makes the canny anchor row a
HALT. All three were verified against source before the predictions were written.

| claim | how it was checked | result |
|---|---|---|
| the eight profile renders | SHA-256 + byte length against the digits Task 2 recorded | **unchanged** — view 0 is 243,196 B / `3E173A21D8A7AC02` |
| the controls being reused | **re-derived** all eight from the renders through `restylize_views.py --profile prop.json --emit-only` into a scratch dir, then compared to the on-disk copies **by bytes and by pixels** | **all sixteen artifacts (8 controls + 8 masks) byte-identical AND pixel-identical** |
| **the canny anchor row** | the re-derivation's own printed counts | **exact on all eight** — 8,695 / 8,230 / 5,580 / 8,400 / 9,509 / 8,508 / 5,230 / 7,870 |

The bytes-are-not-pixels law is honoured in the direction it points: bytes agreed *and* pixels
agreed, so neither reading rests on the other. **No drift; the HALT did not fire.**

### 1b. The seed evidence carries a confound, and it was named before the run

Ruling 18b's clearing evidence for 770701 is the accepted pair's view-1 re-roll — **generated
from twin-prompts v1, before the `gold collar rings` term existed** (13b). This dispatch runs
v2. So against the pair's accepted artifact, two things move, not one. Recorded in the
predictions file at §0b, before submission, as the specific way P1 could fail on view 1.
Ruling 13a's measurement is the mitigation (the rings term was inert at 770700), and the
outcome below is consistent with it being inert at 770701 too — but that is now a second
observation, not an assumption.

## 2. The cloud leg — four submissions, one variable, tested on the dependency graph

Each graph built by the committed builder, saved to disk and pre-flighted **before** submission,
each carrying the inverted no-LoRA assertion, each `estimate_credits` **0 credits**:

| view | yaw | seed | prompt_id | credits |
|---|---|---|---|---|
| 1 | 45 | 770701 | `fcd3212d-0d49-4e37-baf8-f1b4a7f82864` | 0 |
| 3 | 135 | 770701 | `065dd235-8790-4b30-8834-48dadc126d4a` | 0 |
| 5 | 225 | 770701 | `a7bdc5bc-253f-4a34-97a1-1350935e0c11` | 0 |
| 7 | 315 | 770701 | `9dfc8bcc-6bb4-439d-bc23-6f63f420c5a1` | 0 |

The builder printed its explicit-deviation line on all four (*"seed 770701 against the profile's
770700 — recorded per-invocation argument, not an undeclared constant"*) and its pre-flight PASS
on all four (six recipe values equal the decided block; `--prompts` IS `_fixtures.twin_prompts`;
17 links resolve, no self-link, no dangling target, no orphan).

**"One variable" was tested, not asserted.** CLAUDE.md's law says the property belongs to the
dependency graph rather than the parameter edited, so each re-roll graph was **diffed field by
field against the graph that produced the same view's first roll**. Only two fields differ on
any of the four: `KSampler.seed` (770700 → 770701) and `SaveImage.filename_prefix` (a new output
name, so the first roll cannot be overwritten). Node set, class types, pin sets, every other
value: identical. And the transcription into the tool call was checked back against the saved
graphs afterwards on seven fields each — **render, control, prefix, prompt, term count, seed and
the whole recipe block: OK on all four, every graph LoRA-free.**

## 3. File discipline (Ruling 18b) — nothing deleted

The four gold first-rolls are preserved as REJECTED artifacts beside the v2/v6 precedent; the
new rolls take the twin names. The move refuses to overwrite an existing REJECTED file.

```
out/REJECTED_TWIN_swordclay_{1,3,5,7}_seed770700.png   the gold rolls, preserved with their measurements
out/REJECTED_TWIN_swordclay_{2,6}_seed770700.png       Task 2's, untouched
out/TWIN_swordclay_{1,3,5,7}.png                       the 770701 re-rolls
out/TWIN_swordclay_{0,2,4,6}.png                       untouched (0/4 at 770700; 2/6 at 770701)
```

All four downloads are **240×1024** — the ruled generator-legal frame — and none is a byte-repeat
of the roll it replaces.

## 4. ⚠ THE 12e GOLD WATCH — the dispatch's central number

**0.0% on all four diagonals. Zero gold pixels on L2's quillon arms.**

| twin | yaw | arm px | above C\* 12 | **gold px** | **gold %** | watch | at 770700 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 3,204 | 304 | 0 | **0.0%** | clean | 0.0% (unchanged) |
| **1** | 45 | 2,471 | **237** | **0** | **0.0%** | **clean** | 95.5% |
| 2 | 90 | 1,122 | 337 | 150 | 13.4% | trace | 13.4% (unchanged) |
| **3** | 135 | 2,458 | **207** | **0** | **0.0%** | **clean** | 96.0% |
| 4 | 180 | 3,204 | 340 | 0 | **0.0%** | clean | 0.0% (unchanged) |
| **5** | 225 | 2,471 | **253** | **0** | **0.0%** | **clean** | 93.5% |
| 6 | 270 | 1,122 | 174 | 30 | 2.7% | clean | 2.7% (unchanged) |
| **7** | 315 | 2,458 | **192** | **0** | **0.0%** | **clean** | 93.3% |

The `above C* 12` column moved with it: **2,339–2,392 → 192–253**, which is the band the clean
face-ons occupy (304 / 340). The chromatic mass on the quillon arms did not merely change hue —
it left.

**A zero is not a check until a non-zero is shown possible.** The same code, in the same run,
was pointed at the four artifacts these replaced: **95.5 / 96.0 / 93.5 / 93.3%, FIRES on all
four**, reproducing Task 2's digits exactly. The instrument fires on this code path today. The
four 0.0% readings are a measurement, not a dead check.

## 5. The eye, at the 4× hilt crops — the authority the re-roll rested on

`DIAGONALS_770700_vs_770701_hilt_4x.png` puts each diagonal's rejected roll above its re-roll at
4×. Read on that sheet, with the per-twin `TWIN_SHEET_{1,3,5,7}_HILT.png` (reference | control |
asset) beside it:

- **The crossguard is blackened iron on all four**, with relief and dark value, and **the gold
  diamond boss sits crisp and separate at the crossing** — L3 on L3's surface, L2 on L2's, which
  is the fixture's occupancy table.
- **The collar rings land gold** on all four (Ruling 13's term doing its own job).
- **The grip is oxblood** on all four.
- The 770700 rolls above them are unmistakable by contrast: one continuous brass mass across the
  whole crossing with the boss absorbed into it.
- **⚠ The guard's MATERIAL converged on the face-ons; its FORM did not.** I first wrote the
  opposite here — that the re-rolls had merely joined a form views 0 and 4 already carried — and
  it was read off a downscaled eight-view strip. Re-read at 6× at the crossing
  (`GUARD_form_6x.png`, built to test that sentence), it is wrong and the correction is the more
  useful statement: the untouched 770700 face-ons carry a dark iron guard with **plain stepped,
  chamfered quillon arms**, which is the clay reference's own form. The 770701 diagonals carry a
  dark iron guard with **scrolled relief along the arms and cusped quillon ends** — ornament that
  is in neither the face-ons, the rejected 770700 diagonals, nor the geometry. So the seed bought
  the right *material* and brought ornament with it.
  **Ruling 18a recorded exactly this character on view 6's 770701 re-roll** ("the ornamental
  crossing recorded as odd but inside the silhouette"). It now appears on all four diagonals at
  the same seed. On the evidence in hand **the ornament tracks the seed, not the view** — stated
  as what the artifacts show, with the disposition left where it belongs.
- **The gem changed, and it is visible without measuring.** See section 6.

## 6. ⚠ THE L5 GEM DRIFTED ON ALL FOUR RE-ROLLS — and the drift travels with the seed

The gem region is read from the mask's own width profile (topmost figure row down to the collar's
first narrowing — the pair-era derivation, unchanged), and only above-floor pixels are quoted.

| artifact | px > floor | p10 | **median hue** | p90 | wine 0–25 | **lav 290–310** | **mag 310–360** |
|---|---|---|---|---|---|---|---|
| **v1 770701 (new)** | 943 | 68.1 | **299.2** | 321.0 | 0.0% | **27.0%** | **24.7%** |
| **v3 770701 (new)** | 863 | 68.4 | 86.2 | 341.6 | 2.9% | **10.4%** | **33.1%** |
| **v5 770701 (new)** | 841 | 62.1 | **298.9** | 313.2 | 1.3% | **35.3%** | **14.7%** |
| **v7 770701 (new)** | 832 | 67.2 | 86.4 | 335.4 | 2.8% | **17.4%** | **25.4%** |
| v1 770700 (replaced) | 782 | 19.5 | 79.4 | 94.3 | 11.4% | 1.3% | 0.6% |
| v3 770700 (replaced) | 728 | 17.3 | 81.8 | 92.1 | 14.4% | 0.0% | 0.5% |
| v5 770700 (replaced) | 642 | 57.0 | 81.7 | 95.7 | 5.1% | 2.0% | 0.6% |
| v7 770700 (replaced) | 778 | 16.6 | 80.7 | 92.3 | 12.9% | 0.0% | 4.5% |
| v0 770700 (face-on, untouched) | 732 | 15.1 | 73.5 | 89.4 | 23.5% | 1.6% | 1.1% |
| v4 770700 (face-on, untouched) | 847 | 11.3 | 72.9 | 310.8 | 24.8% | 1.4% | 10.3% |
| PAIR v1 770701 (the recorded drift) | 636 | 70.3 | **303.9** | 342.0 | 7.4% | 21.9% | 36.9% |
| PAIR v0 770700 (garnet) | 305 | 4.0 | 16.0 | 346.8 | 66.9% | 8.5% | 12.5% |

**The combined lavender + magenta share on the pommel goes from 0.5–4.5% at 770700 to
42.8–51.7% at 770701, on all four views.** Two of the four medians land at 299, within 5° of the
pair's recorded 303.9.

**At 8× (`L5_GEM_8x_strip.png`) the eye reads it without the numbers**: every 770700 roll of this
hilt — the four replaced diagonals, both face-ons, the pair's view 0 — carries a deep garnet-red
stone. Every 770701 roll — the four re-rolls and the pair's view 1 — carries a violet or bright
magenta core. **Six artifacts at 770700 garnet, five at 770701 drifted, zero exceptions.**

**What this means for the set as staged:** the face-on views (0, 4, at 770700) now carry garnet
gems while the four diagonals carry magenta ones. **The set is no longer uniform in L5.** That is
a statement of what is on disk, not a disposition.

**And it is invisible to the gate by construction.** A gem body at hue ~299 sits inside the
**lavender-rim band**, which Ruling 17c admitted explicitly as *"NOT A MATERIAL … backdrop bleed"*.
So a declared material has moved into a band admitted for antialiasing, and the off-palette count
cannot see it. That is the priced 17c blindness with a face nobody predicted: it was priced for
*interior backdrop arrivals*, and what walked through it was **L5 itself**.

**Ruling 17e's watch is therefore live and pointing the other way from Task 2.** Task 2 measured
the gem spread *narrowed* (0 of 8) and the watch did not fire. It fires now. Fixture territory by
the rings precedent — **reported, not acted on.**

## 7. ⚠ THE STANDING DEPTH DIAGNOSTIC FIRED — and what it caught is section 6

Baseline class (the accepted pair, Ruling 17c): 144 px = 0.160%, unconcentrated, rows 0.13–0.91.

| twin | band px | **deep px** | **deep %** | **largest CC** | row span | at 770700 | reading |
|---|---|---|---|---|---|---|---|
| 0 | 977 | 109 | 0.219% | 30 | 0.29–0.91 | (unchanged) | baseline class |
| **1** | 1,890 | **349** | **0.870%** | **198** | **0.09–0.77** | 117 / 0.292% / CC 14 | **⚠ deep AND concentrated** |
| 2 | 1,709 | 322 | 1.333% | 83 | 0.11–0.60 | (unchanged) | ⚠ the recorded v2 failure |
| 3 | 1,521 | 140 | 0.347% | 31 | 0.10–0.90 | 11 / 0.027% / CC 4 | baseline class, 13× its own first roll |
| 4 | 1,267 | 99 | 0.199% | 28 | 0.31–0.91 | (unchanged) | baseline class |
| **5** | 2,138 | **397** | **0.990%** | **124** | **0.09–0.78** | 62 / 0.155% / CC 22 | **⚠ deep AND concentrated** |
| 6 | 1,264 | 148 | 0.613% | 41 | 0.13–0.68 | (unchanged) | ⚠ elevated, narrowed |
| 7 | 1,844 | 224 | 0.555% | 65 | 0.10–0.79 | 18 / 0.045% / CC 7 | elevated, 12× its own first roll |

**v1's largest component is 198 px — 2.4× the 83 that flagged view 2**, the worst artifact this
subject has produced. Two of the four meet 17c's reading condition outright.

**Before that is reported as a backdrop arrival, it was attributed to a region:**

| artifact | deep px | **inside the gem region** | share | largest CC inside the gem? |
|---|---|---|---|---|
| v1 770701 | 349 | **225** | **64.5%** | **YES — the whole 198-px component** |
| v5 770701 | 397 | **244** | **61.5%** | **YES — the whole 124-px component** |
| v3 770701 | 140 | 21 | 15.0% | no |
| v7 770701 | 224 | 71 | 31.7% | no |
| v1/v3/v5/v7 at 770700 | 117 / 11 / 62 / 18 | 6 / 0 / 12 / 0 | 5.1% / 0.0% / 19.4% / 0.0% | no |

`DEEP_LAVENDER_where.png` draws the counted population on the twin itself: on v1 and v5 it is the
gem, plainly. On v3 and v7 the gem holds a third or less and the remainder is thin edge speckle
along the blade — v3's largest component is a 3 × 28 px sliver at rows 0.43–0.46, v7's a 2 × 62 px
sliver at rows 0.45–0.51, both on the blade's flank rather than in any structure.

**So the diagnostic did its job and answered a different question than it was built for.** It was
made to watch interior *backdrop-family* arrivals that hue can no longer see. What it found is a
*declared material* that moved into the same band. The instrument is indifferent to which — and
that indifference is exactly why it caught something the hue count could not.

## 8. Registration — measured, and structurally unable to answer the dispatch's question

| view | sil px | keyed px | **IoU @0.06** | IoU @0.10 | IoU @0.15 | bbox vs mesh | at 770700 |
|---|---|---|---|---|---|---|---|
| 0 | 49,775 | 63,396 | 0.7824 | 0.8154 | 0.8380 | 1.06× ok | 0.7824 (unchanged) |
| **1** | 40,101 | 42,320 | **0.9422** | 0.9544 | 0.9455 | **1.00× ok** | 0.9359 |
| 2 | 24,153 | 25,755 | 0.8860 | 0.8858 | 0.8698 | **2.69× SUSPECT** | 0.8860 (unchanged) |
| **3** | 40,331 | 43,174 | **0.9269** | 0.9431 | 0.9352 | **1.00× ok** | 0.9453 |
| 4 | 49,775 | 61,941 | 0.8016 | 0.8451 | 0.8504 | 1.06× ok | 0.8016 (unchanged) |
| **5** | 40,101 | 41,579 | **0.9557** | 0.9600 | 0.9419 | **1.00× ok** | 0.9451 |
| 6 | 24,153 | 25,300 | 0.9300 | 0.9293 | 0.9114 | 1.07× ok | 0.9300 (unchanged) |
| **7** | 40,331 | 42,661 | **0.9317** | 0.9419 | 0.9237 | **1.00× ok** | 0.9461 |

Set spread at 0.06: **0.7824 (v0) → 0.9557 (v5) = 0.1733** (0.1637 before). Mirror deltas
(Ruling 10c): v0/v4 0.0192, **v1/v5 0.0135**, v2/v6 0.0441, **v3/v7 0.0048**.

**No bound is adopted** — 18d puts that at the set's acceptance, and `prop.json` keeps
`reg-iou-min 0.0` / `bbox-tol 9.99`. Absolute px sit beside every ratio because figure area
swings 2.061× between views.

**The pre-registered point stands and is worth the line: IoU is blind to what this dispatch
tested.** View 1 went from 95.5% gold on its crossguard to 0.0% — a total material change on the
subject's most contested structure — and its IoU moved **+0.0063**. Anyone reading these numbers
as evidence for or against the branch is reading the wrong instrument. Bbox is the one that
earns its place here: 1.00× on all four, the phantom-crossguard failure mode absent.

## 9. The palette gate, report-only in the admitted configuration (17d)

| twin | figure px | off-palette | % | largest blob | dominant off-band hue | at 770700 |
|---|---|---|---|---|---|---|
| 0 | 49,775 | 230 | 0.46% | 71 | 100–110 (45%) | unchanged |
| 1 | 40,101 | 236 | 0.59% | 41 | 310–320 (42%) | 211 / 0.53% / 13 |
| 2 | 24,153 | 197 | 0.82% | 75 | 310–320 (56%) | unchanged |
| 3 | 40,331 | 392 | 0.97% | 84 | 320–330 (47%) | 276 / 0.68% / 62 |
| 4 | 49,775 | 133 | 0.27% | 25 | 320–330 (56%) | unchanged |
| 5 | 40,101 | 298 | 0.74% | 47 | 310–320 (28%) | 170 / 0.42% / 18 |
| 6 | 24,153 | 108 | 0.45% | 21 | 310–320 (39%) | unchanged |
| 7 | 40,331 | 349 | 0.87% | 40 | 310–320 (31%) | 258 / 0.64% / 65 |

**Both bounds null; nothing here can fail** — the tool's own banner, quoted not suppressed. The
accepted pair measures 106 and 142 px through this configuration. The set now sits at
108–392 px / 0.27–0.97%, up from 108–276 / 0.27–0.82%; the four re-rolls all rose (by 25 to 128
px) and their dominant off-band hue moved to 310–320 on three of four — the shoulder just above
the admitted lavender band, consistent with section 6 and not separable from it by this
instrument.

**And the gate is silent about sections 4, 6 and 7.** It could not see the gold sprawl (declared
material, declared band) and it cannot see the gem drift (declared material, *admitted* band).
Two independent demonstrations of colour-not-placement on the same set.

**A record-hygiene note, because it is the kind of thing this repo asks be said out loud:** the
`gate.log` committed at Task 2 disagreed with that report's own table on views 2 and 6 (log 195 /
0.81% / blob 19 and 133 / 0.55% / 15; table 197 / 0.82% / 75 and 108 / 0.45% / 21). This
session's run of the same tool on the same untouched artifacts reproduces the **table** exactly,
so the log was written before those two re-rolls were installed and was stale in the repo. It has
now been overwritten with a current run; the first-roll gold-watch log was renamed rather than
replaced.

## 10. Predictions scored

| # | prediction | outcome |
|---|---|---|
| **P1** | **all four land iron, 0 of 4 sprawl; gold ≤ 3%; above-C\*12 arm counts fall to 150–700; gold px < 150** | **HELD, and tighter than staked** — 0.0% and **exactly zero gold px** on all four; above-C\*12 at 192–253 |
| P1b | the all-four-alike shape (a 2/2 or 3/1 split least likely, under 20%) | **held** — 4/4 |
| P2 | IoU 0.92–0.96 on all four | **held** — 0.9269–0.9557 |
| P2 | within-set spread ≤ 0.02 | **MISSED** — 0.0288 |
| P2 | mirror deltas ≤ 0.010 | **half missed** — v3/v7 0.0048 held, v1/v5 0.0135 did not |
| P2 | bbox `ok`, ratios 0.98–1.05 | **held** — 1.00×/1.01× on all four |
| **P2** | **IoU is structurally blind to the thing being tested** | **held, and it is the useful half** — v1 moved +0.0063 across a 95.5% → 0.0% material change |
| **P3** | **0 of 4 flag; deep 0.02–0.40%, CC < 40, rows reaching ≥ 0.85** | **FALSIFIED on 3 of 4.** v1 0.870% / CC 198 / rows to 0.77; v5 0.990% / 124 / 0.78; v7 0.555% / 65 / 0.79 — out on every clause. v3 (0.347% / 31 / 0.90) held on all three |
| **P4** | **≥ 1 of 4 with gem median above 290°** | **HELD, and beyond the stake** — 2 of 4 above 290 (299.2, 298.9), all 4 with lavender+magenta up ~20× and visibly drifted at 8× |
| P5 | 0 credits on all four | **held** — four of four |
| P6 | the first exit | **held** |

### Where I was most wrong, and it is one error rather than two

**P3 and P4 are the same phenomenon, and I predicted them in adjacent sections without
connecting them.** P4 reasoned that the gem might drift into the magenta-lavender region at this
seed. P3 reasoned that the depth diagnostic would stay quiet because *"a seed change with an
identical control has no mechanism I can name for driving an interior backdrop-family arrival."*
That sentence is true and irrelevant: the gem is not a backdrop arrival, it is deep inside the
figure, and hue 299 is inside the band the diagnostic counts. **If P4 lands, P3 cannot hold** —
the diagnostic had to fire, by arithmetic, and I wrote the two predictions two paragraphs apart
without noticing.

The generalisable form: **I reasoned about the diagnostic by its intended target instead of by
its definition.** The instrument counts *band ∧ deep*, not *backdrop*. Asking "what else is in
this band" was one line of work and I did not do it. That is the same family as the repo's
"write the check against the specification, not against the defect you noticed" — here, read the
check by its predicate, not by its purpose.

Secondary: P2's spread and mirror-delta clauses were guessed off Task 2's within-pair agreement
at a single seed. A different seed is a different draw, and the tightness of one draw is not a
property of the pipeline.

## 11. What has NOT been done

- **No third roll on any view. No 770702. No other seed, no other view.** Four submissions
  exactly, and the halt clause's escalation ban is honoured absolutely.
- **Nothing armed.** The gate stays report-only, both bounds null; **no IoU bound derived** (18d
  puts it at the set's acceptance); `prop.json`, the palette and the fixture are untouched.
- **No disposition on the gem drift or on the guard ornament.** Both go up as findings. The
  fixture is the advisor's, and re-choosing terms on what twins show is forbidden.
- **No projection.** Stage 1 is a later dispatch.
- **No memory-store write.**
- **View 2 is not re-rolled** and is excluded from stage 1 per 18c; its artifact and both its
  measurements stay in the record.

## 12. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Four graphs saved pre-submission with seed and prompt_id; the builder's explicit-deviation line printed on each; the canny anchor row re-derived and checked pixel-exact before anything submitted; every measurement written to JSON beside its artifact; both rejected-artifact sets preserved under name |
| ANDON_AUTHORITY | **3** | The branch reading rule — including the ambiguous trace case — was committed before the numbers existed (`86dfda5`), and so was the halt-clause interpretation (`283a20d`), so neither could be tuned to the result. The file move refuses to overwrite a preserved REJECTED artifact |
| NAMED_COMPENSATORS | **2** | 0 credits on all four, quoted each; new files only; the one overwrite (`gate.log`) is a regenerated measurement whose predecessor was already stale, and the gold-watch log was renamed rather than replaced. Not 3: four more cloud outputs persist in the account's store with no compensator named — Task 2's carried gap, unchanged |
| DECOMPOSE_BY_SECRETS | **3** | Nothing re-derives; the single variable is the seed and that was **tested on the dependency graph** (field-by-field diff against each view's own first-roll graph) rather than asserted. The one remaining difference against the *pair's* artifact — the rings term — is named in §1b rather than glossed |
| UNCERTAINTY_GATED_HUMANS | **3** | Nothing judged, nothing armed. The gem drift and the guard ornament go up as findings with their artifacts; the set's new L5 non-uniformity is stated as what is on disk; my own P3/P4 contradiction is reported as one error rather than split into two misses; and the guard-form sentence I got backwards is corrected in place at §5 with the 6× crop that overturned it rather than quietly rewritten |
| EXTERNAL_VERIFIER | **3** | The gold watch's four zeros were validated **in the same run** against the artifacts they replaced, which fired at 93–96%; registration measures against the raycast silhouette, an independent path from the generator; **the depth diagnostic and the gem watch reached the same finding from unrelated signals** — one counting hue-band pixels by depth, one reading a region's hue median — and the eye at 8× agrees with both. `skip:` on a second model, per precedent |

---

## HALT 3 — the set staged

`E:\AI\training\facet_next\E14_prep\twins\`:

```
out/TWIN_swordclay_{0..7}.png                      1,3,5,7 now at 770701; 0,4 at 770700; 2,6 as Task 2 left them
out/REJECTED_TWIN_swordclay_{1,3,5,7}_seed770700.png   the gold rolls, preserved
out/REJECTED_TWIN_swordclay_{2,6}_seed770700.png       Task 2's, untouched
TWIN_SHEET_{0..7}.png / _HILT.png                  reference | control | asset, full size and hilt 4x
TWINSET_strip_with_silhouette.png                  all eight with the EXACT silhouette drawn on (REBUILT)
TWINSET_hilt_4x_strip.png                          the watches' strip (REBUILT)
DIAGONALS_770700_vs_770701_hilt_4x.png             the dispatch's central comparison, both rolls, 4x
L5_GEM_8x_strip.png                                the gem at 8x: current set, replaced rolls, the pair
DEEP_LAVENDER_where.png                            what the depth diagnostic counted, drawn on the twin
GUARD_form_6x.png                                  the crossing at 6x: face-ons, rejected rolls, re-rolls, clay
gate_twins.json · deep_share.json · registration.json · gate.log · goldwatch.log
goldwatch_firstroll_seed770700.log                 the first-roll watch, preserved
cloud/twin_{1,3,5,7}_reroll.json                   the four saved graphs
```

**The first exit fired.** Seven twins stand for stage 1 — **0, 1, 3, 4, 5, 6, 7** — with view 2
excluded per 18c. Four things want the advisor's eye, and none is mine:

1. **Twin acceptance at the completed set** — the gold occupancy violation is gone from every
   diagonal at 0.0%, verified by an instrument shown firing on the same code path in the same run.
2. **The L5 gem drift (§6)** — four of four re-rolls, a 20× rise in the lavender+magenta share,
   two medians at 299 against the pair's recorded 303.9, and a set that is now non-uniform in L5
   between its face-ons and its diagonals. Ruling 17e's watch fires. **The seed buys an iron
   crossguard and costs a garnet gem** — that trade is the finding, and weighing it is not mine.
3. **The 17c blindness has a second face (§7)** — the admitted rim band now hides a *declared
   material*, not just backdrop bleed, and the depth diagnostic is what saw it. Whether that
   changes the band's status or only its documentation is a ruling.
4. **The guard ornament (§5)** — scrolled relief and cusped quillon ends on all four 770701
   diagonals, present in neither the untouched 770700 face-ons, the rejected 770700 diagonals,
   nor the clay reference; inside the silhouette throughout. Ruling 18a recorded the same
   character on view 6's 770701 re-roll, so on the evidence it **tracks the seed**. Visible in
   every hilt sheet's provenance panel and isolated at 6× in `GUARD_form_6x.png`. My first
   reading of this was wrong in the opposite direction and is corrected in place in §5.

Stage 1 is the next dispatch, against the pre-registered 51.33% ceiling.
