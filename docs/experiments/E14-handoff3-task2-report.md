# E14 handoff 3, Task 2 — the twin set. HALT 2.

**Executor session, 2026-08-07.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 17f.
Predictions committed blind in `2ce9f64`. Task 1's report and the ruled palette are at
`6c22130` / Ruling 17.

**Nothing is judged here.** Eight twins staged, two bounded re-rolls spent on the eye clause,
one rejected artifact preserved per re-rolled view, every measurement report-only per 17d.
**Cost: 0 credits** — `estimate_credits` returned "no paid API nodes" on all **ten**
submissions; this is GPU time on the subscription, not metered spend.

---

## 1. Stems v2, controls, and the byte-level pre-flight

**Stems v2** built by the committed builder from the profile's LIVE prompt entry (11 terms
after Ruling 13's `gold collar rings`):

```
swordclay_0,1,3,4,5,7  11 terms  FULL (byte-equal to entry)
swordclay_2,6          10 terms  (the boss term dropped)
all stems asserted ordered subsequences; 6 full-string views byte-equal
```

The boss drop is unchanged and re-verified the cheap way: **the eight profile renders are
byte-identical to those the Task-4 two-scale eye check ran on** (SHA-256 recorded in
`twins/control.log`'s companion listing; e.g. `swordclay_0.png` 243,196 B / `3E173A21D8A7AC02`).
The rings term drops on no view — visible on all eight, ratified at Ruling 15a.

**The canny anchor row is a HALT if it drifts. It did not drift:**

| view | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| **canny px** | **8,695** | **8,230** | **5,580** | **8,400** | **9,509** | **8,508** | **5,230** | **7,870** |
| anchor row | 8,695 | 8,230 | 5,580 | 8,400 | 9,509 | 8,508 | 5,230 | 7,870 |

Exact on all eight. Controls for views 0/1 were additionally verified byte-identical to the
accepted pair's own controls, so those two uploads were reused rather than re-minted.

## 2. The cloud leg

Ten submissions, each with its graph **saved to disk and pre-flighted before submission**, each
`estimate_credits` **0 credits**, each carrying the inverted no-LoRA pre-flight:

| view | seed | prompt_id | note |
|---|---|---|---|
| 0 | 770700 | `27eebd06-14d1-470d-a32f-7874d7468be3` | |
| 1 | 770700 | `99cc5977-ef7a-442a-ae45-e4568cca1ce5` | the measured-risk view |
| 2 | 770700 | `6c1e1c19-6f88-4bee-8fd4-b74e342a11fe` | **REJECTED** |
| 2 | **770701** | `5cd3e55c-8104-4482-acee-69fb7bc4cb3b` | re-roll — **second failure, see §4** |
| 3 | 770700 | `f1ee6e8e-f28a-45e9-a568-829dacef9071` | |
| 4 | 770700 | `42d071e1-72e3-4e82-9354-28c66b1a9566` | |
| 5 | 770700 | `75e53f23-5381-4a4a-baf9-8c4da48f6fbe` | |
| 6 | 770700 | `8e024fb5-e6fd-4132-a547-be9db47a9e6d` | **REJECTED** |
| 6 | **770701** | `15a2e817-fb4e-4602-950a-eca6109b4234` | re-roll — clean |
| 7 | 770700 | `cb2b1469-6682-4be1-9708-cb0c0e69588d` | |

**The submissions were transcribed into the tool call, so they were checked back against the
saved graphs afterwards** rather than trusted — render name, control name, prefix, prompt
string (against the fixture file), term count and the whole recipe block, on all eight:
**every field OK, every graph LoRA-free.** CLAUDE.md's rule exists because a hand-retyped
payload once passed `dry_run` with a self-referencing link; this is that rule honoured with a
verification instead of a claim.

## 3. Registration — halts suspended, and the bbox check earning its place

Keyed with a **quadratic background fit over a border ring**, not a corner median (retired,
three failures) — and this subject's realised backdrop is neither flat nor stable, so a single
sample would be the exact failure mode.

**The bbox check fired before any IoU was read**, which is the law working (*a figure cannot be
751 px wide in a 752 px frame when the mesh is 388*):

| view | silhouette px | **first roll** IoU@.06 | bbox vs mesh | **final** IoU@.06 | bbox vs mesh |
|---|---|---|---|---|---|
| 0 | 49,775 | 0.7824 | 1.06× ok | 0.7824 | 1.06× ok |
| 1 | 40,101 | 0.9359 | 1.00× ok | 0.9359 | 1.00× ok |
| **2** | 24,153 | **0.4498** | **3.70× SUSPECT** | **0.8860** | **2.69× still SUSPECT** |
| 3 | 40,331 | 0.9453 | 1.00× ok | 0.9453 | 1.00× ok |
| 4 | 49,775 | 0.8016 | 1.06× ok | 0.8016 | 1.06× ok |
| 5 | 40,101 | 0.9451 | 1.00× ok | 0.9451 | 1.00× ok |
| **6** | 24,153 | **0.5022** | **3.96× SUSPECT** | **0.9300** | **1.07× ok** |
| 7 | 40,331 | 0.9461 | 1.00× ok | 0.9461 | 1.00× ok |

**Spread at tolerance 0.06: 0.7824 (v0) → 0.9461 (v7), 0.1637** on the final set — against
0.4963 before the re-rolls. **No bound is adopted**; `prop.json` keeps `reg-iou-min 0.0` and
`bbox-tol 9.99`, and this spread is the calibration data the twin-set ruling can derive from.
Absolute px sit beside every ratio because this subject's figure area swings 2.061× between
views.

**Mirror corroboration** (Ruling 10c — opposite views share a silhouette by orthographic
construction, so any within-pair difference is the generator, not the geometry): v0/v4 differ
by 0.0192, v1/v5 by 0.0092, v3/v7 by 0.0007. **The generator is highly consistent within a
mirror pair** — which makes v2/v6's divergence (0.4498 vs 0.5022 first roll) a per-roll fact
rather than a geometric one.

**v0 and v4 sit at 0.78–0.80 while every other clean view is at 0.93–0.95.** Their keyed area
exceeds the silhouette by ~13,000 px and their bbox is 1.06× the mesh — the drop shadow beside
a wide face-on quillon span keys in. Reported as a keying artifact rather than a registration
finding, because the bbox is within tolerance and the centroid offsets are small.

## 4. ⚠ THE EYE CLAUSE FIRED ON THE TWO EDGE-ON VIEWS

**What went wrong.** On views 2 and 6 the generator painted a **face-on crossguard — quillon
arms spread wide outside the mesh silhouette** — while the blade column itself followed the
control. The mesh at those yaws presents the quillons end-on as a compact block 54 px wide;
the first rolls painted 200 and 214 px of quillon bar, with a drop shadow to match.

**The pre-registered rule it violates**, authored before any twin existed:
`canon/LONGSWORD-IDENTITY.md`'s MESH-SUPPLIED table — *"the form, stance and silhouette …
the MESH's stance; twins register to it"* — and CLAUDE.md's own line, *"a twin has exactly one
job — register to the silhouette it will be projected onto."* Paint outside the silhouette is
paint on no surface. The rule would have been the same whatever came out.

**One bounded re-roll each, seed 770701, recorded as an explicit deviation by the builder's own
pre-flight. Both rejected artifacts are preserved** with their measurements
(`REJECTED_TWIN_swordclay_{2,6}_seed770700.png`).

- **View 6's re-roll is clean**: IoU 0.5022 → 0.9300, bbox 3.96× → **1.07×, ok**.
- **View 2's re-roll is a SECOND FAILURE at reduced magnitude**: IoU 0.4498 → 0.8860, but the
  phantom crossguard persists at 2.69× the mesh's width. **Per the dispatch, a second failure
  is the RESULT, not a third roll.** No third roll was taken. View 2 stands as generated, with
  the failure recorded.

**A correction to my own first reading, stated because it changes what the finding is.** On
first sight of view 2 I read it as "the generator painted a face-on sword" — a wholesale wrong
pose. The silhouette overlay shows that is wrong: **the blade column registers to the control;
what is added is the crossguard.** The failure is localised, not total, and describing it as
total would have overstated it to the advisor.

**The mechanism, offered as a labelled hypothesis:** the edge-on control carries only
5,580 / 5,230 canny px on a figure 9.83% of frame, and the model's "longsword" prior supplies a
crossguard where a thin control shows none. That is S-thin meeting a weak control — the
fixture's own stressor arriving where it was pre-registered, on the route's thinnest subject.

## 5. The gate, report-only in the admitted configuration (17d)

| twin | figure px | off-palette | % | largest blob | dominant off-band hue |
|---|---|---|---|---|---|
| 0 | 49,775 | 230 | 0.46% | 71 | 100–110 (45%) |
| 1 | 40,101 | 211 | 0.53% | 13 | 320–330 (36%) |
| 2 | 24,153 | 197 | 0.82% | 75 | 320–330 (27%) |
| 3 | 40,331 | 276 | 0.68% | 62 | 310–320 (36%) |
| 4 | 49,775 | 133 | 0.27% | 25 | 320–330 (56%) |
| 5 | 40,101 | 170 | 0.42% | 18 | 320–330 (33%) |
| 6 | 24,153 | 108 | 0.45% | 21 | 30–40 (36%) |
| 7 | 40,331 | 258 | 0.64% | 65 | 320–330 (30%) |

**Both bounds null; nothing here can fail** — the tool's own banner, quoted not suppressed. For
context, the accepted pair measured 106 and 142 px through the same configuration. **The twin
set sits at 108–276 px / 0.27–0.82%**, the same order.

**And the gate is silent about §4 and §6.** Neither the phantom crossguard nor the gold sprawl
is off-palette: both are declared materials in declared bands. This is the colour-not-placement
limit that Ruling 17e banked route-level, now demonstrated on eight more artifacts.

## 6. ⚠ THE STANDING DEPTH DIAGNOSTIC EARNED ITS KEEP ON ITS FIRST RUN

Ruling 17c admitted the lavender-rim band and priced the blindness it buys: the hue count can
no longer see interior backdrop-family arrivals, so **depth watches what hue cannot**. Baseline
class (the accepted pair): 144 px = **0.160%**, unconcentrated, rows 0.13–0.91.

| twin | band px | **deep px** | **deep %** | **largest CC** | row span | reading |
|---|---|---|---|---|---|---|
| 0 | 977 | 109 | 0.219% | 30 | 0.29–0.91 | baseline class |
| 1 | 823 | 117 | 0.292% | 14 | 0.27–0.91 | baseline class |
| **2** | 1,709 | **322** | **1.333%** | **83** | **0.11–0.60** | **⚠ deep AND concentrated** |
| 3 | 441 | 11 | 0.027% | 4 | 0.31–0.91 | baseline class |
| 4 | 1,267 | 99 | 0.199% | 28 | 0.31–0.91 | baseline class |
| 5 | 906 | 62 | 0.155% | 22 | 0.10–0.91 | baseline class |
| **6** | 1,264 | **148** | **0.613%** | 41 | **0.13–0.68** | **⚠ elevated, narrowed** |
| 7 | 582 | 18 | 0.045% | 7 | 0.32–0.91 | baseline class |

**The two views it flags are exactly the two the eye clause caught** — and it flagged them from
a completely different signal. v2 carries 8× the baseline deep share in a component nearly 3×
any other's, and its row span stops at 0.60 where every clean view runs to 0.91. That is the
17c reading condition — *deep AND concentrated* — met on the first set the diagnostic ever ran
on, by an instrument that knows nothing about crossguards.

## 7. ⚠ THE 12e GOLD WATCH — it fires on four of eight, and the pattern is view-systematic

Measured on **L2's own surface**: a horizontal band at the crossing (rows read off the mesh
silhouette's own width maximum), **excluding the central grip column where L3's boss
legitimately sits**. Gold there is gold on a surface outside L3's.

| twin | yaw | arm px | above C\* 12 | **in the gold band** | **gold %** | watch |
|---|---|---|---|---|---|---|
| 0 | 0 | 3,204 | 304 | 0 | **0.0%** | clean |
| **1** | 45 | 2,471 | 2,392 | 2,359 | **95.5%** | **FIRES** |
| 2 | 90 | 1,122 | 337 | 150 | 13.4% | trace |
| **3** | 135 | 2,458 | 2,382 | 2,359 | **96.0%** | **FIRES** |
| 4 | 180 | 3,204 | 340 | 0 | **0.0%** | clean |
| **5** | 225 | 2,471 | 2,339 | 2,311 | **93.5%** | **FIRES** |
| 6 | 270 | 1,122 | 174 | 30 | 2.7% | clean |
| **7** | 315 | 2,458 | 2,343 | 2,293 | **93.3%** | **FIRES** |

**All four diagonal views fire at 93–96%. Both face-on views are at exactly 0.0%.** This is not
a per-view roll: it is a clean function of view geometry, and no prior artifact could have shown
it because the pair only ever generated views 0 and 1.

**View 1 at 770700 is the measured-risk view and it sprawled again.** Ruling 13a pre-registered
the question — does naming the rings redirect the family pressure? — with the rejected pair roll
as its recorded example. **Measured: it does not.** Same view, same seed, now with `gold collar
rings` in the stem, and the crossguard is 95.5% gold.

**The hypothesis, labelled as one:** on face-on views the quillon arms are long and clearly
separated from the boss, and the L2/L3 boundary holds; on diagonal views the arms foreshorten
into a compact mass adjacent to the boss, and gold takes the whole mass. If that is right the
lever is not the prompt at all — it is that two adjacent small structures at this frame scale
cannot be told apart, which is S-hilt-scale rather than 12e family pressure. **Reported, not
acted on. The fixture is the advisor's.**

## 8. The L5 gem watch

**No twin shows the pair's magenta drift.** All eight read dark garnet-red to near-black at the
4× hilt crop — twin 0 and twin 4 clearly garnet, twins 2 and 6 darkest. The pair's view-1
re-roll (median hue 303.9, 37% magenta) is not reproduced anywhere in the set. **The gem is
darker and more consistent across the twin set than across the pair**, and Ruling 17e's watch —
"if the twins widen the gem's spread beyond the band, that is fixture-question territory" —
does **not** fire: the spread narrowed.

## 9. Predictions scored

| # | prediction | outcome |
|---|---|---|
| T1 | stems FULL except 2/6, rings drop nowhere | **held** |
| T2 | canny counts reproduce the anchor row exactly | **held** — all eight |
| T3 | 0 credits every submission | **held** — ten of ten |
| T4 | IoU 0.85–0.95 on face-on/diagonal, materially lower on 2/6, spread ≥ 0.10 | **held on the shape, and the low views were low for a reason I did not predict.** Diagonals 0.935–0.946; 2/6 lowest at 0.450/0.502 first roll. But the face-on views came in at 0.78–0.80, *below* my band, on a keying artifact — and 2/6's shortfall was a phantom crossguard, not the sliver geometry I reasoned from |
| T5 | absolute px reported beside every ratio | **held** |
| T6 | within-pair IoU differences smaller than across-pair | **held** — 0.0007–0.0192 within, 0.164 across |
| **V1** | **the gold sprawl RECURS on view 1 at 770700** | **HELD — 95.5%** |
| V2 | the alternative (naming the rings binds gold) | **falsified as the outcome** — stated in advance so this scores rather than rationalises |
| V3 | one view at one seed cannot settle the mechanism | **held, and superseded** — eight views did settle something the single view could not: the pattern is view-systematic |
| **X1** | **gold watch fires on 1–3 of eight** | **FALSIFIED — 4 of 8**, and the count was the wrong thing to predict; the *pattern* is the finding |
| X2 | the crossguard is the surface it fires on | **held exactly** |
| **X3** | **gem drift on 3 or more of eight** | **FALSIFIED — 0 of 8.** The spread narrowed rather than widened |

**Where I was most wrong: X1 and X3, in the same way.** Both were base-rate guesses extrapolated
from two pair artifacts, and both missed because two views of an eight-view set are not a
sample of it — view 0 and view 1 are one face-on and one diagonal, and the failure turns out to
be *entirely* a face-on/diagonal distinction. Predicting a count when the underlying structure
is categorical is the error, and it is visible only in hindsight because the pair could not have
shown the structure.

## 10. What has NOT been done

- **No third roll on any view.** Two bounded re-rolls spent, both on the eye clause; view 2's
  second failure stands as the result.
- **No threshold armed.** The gate stays report-only per 17d; no IoU bound adopted; `prop.json`
  and the fixture untouched.
- **No projection.** Stage 1 is the next dispatch.
- **The gold finding and the crossguard finding are REPORTED, not acted on** — the fixture is
  the advisor's, and re-choosing terms on what twins show is forbidden (twins are not the pair's
  judges).
- **No memory-store write.**

## 11. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Stems versioned v2 with the builder run recorded and both notes in the file; the canny anchor row checked byte-exact before submission; all ten graphs saved pre-submission with prompt_id and seed; every measurement in JSON beside its artifacts |
| ANDON_AUTHORITY | **3** | The anchor row was a halt condition and was checked first; the bbox check fired before any IoU was read and invalidated two numbers until looked at; the eye clause was the only re-generation authority used; **view 2's second failure was taken as the result rather than rolled again** |
| NAMED_COMPENSATORS | **2** | **0 credits** on all ten submissions, quoted each. New files only under `E14_prep/twins/`; both rejected artifacts preserved with their measurements. Not 3: sixteen cloud uploads persist in the account's input store with no compensator named |
| DECOMPOSE_BY_SECRETS | **3** | Identity flows profile → builder → graph and is never retyped; the gold watch measures L2's own surface with L3's legitimate region excluded by construction, so it cannot fire on a correct boss; the crossguard band is read off the mesh's own width profile rather than guessed |
| UNCERTAINTY_GATED_HUMANS | **3** | Nothing judged, nothing armed. The IoU spread is offered as the calibration data a bound could come from, not as a bound; the gold pattern and its mechanism hypothesis go up labelled; my own overstated first reading of view 2 is corrected in the report rather than quietly fixed |
| EXTERNAL_VERIFIER | **3** | Submissions verified back against the saved graphs on six fields each; registration measured against the raycast silhouette, an independent path from the generator; **the depth diagnostic flagged the same two views as the eye, from an unrelated signal**; the gold watch measured after the eye read it, and agreed |

---

## HALT 2 — the twin set staged

`E:\AI\training\facet_next\E14_prep\twins\`:

```
out/TWIN_swordclay_{0..7}.png              the eight twins (2 and 6 are re-rolls at 770701)
out/REJECTED_TWIN_swordclay_{2,6}_seed770700.png   preserved, with their measurements
TWIN_SHEET_{0..7}.png                      render | control | twin, full size
TWIN_SHEET_{0..7}_HILT.png                 the same three panels, hilt at 4x
TWINSET_strip_with_silhouette.png          all eight with the EXACT silhouette drawn on
TWINSET_hilt_4x_strip.png                  the watches' strip
gate_twins.json · deep_share.json · registration.json · goldwatch.log
overlay/ · control/ · cloud/twin_*.json (ten saved graphs)
```

New instruments: `tools/diagnostics/e14_deep_share.py`,
`tools/diagnostics/e14_twin_registration.py`. Stems: `docs/experiments/E14-twin-prompts.json` v2.

**Four things want the advisor's ruling, and none is mine:**

1. **Twin acceptance** — six views clean, view 6 clean after one re-roll, **view 2 carrying a
   recorded second failure**.
2. **The gold pattern** (§7) — four of eight at 93–96% on L2's surface, entirely on the
   diagonals, with the rings term now in the stem and the pre-registered question answered
   *no*. Fixture territory by the rings precedent.
3. **The edge-on control's weakness** (§4) — whether a subject this thin can be twinned at
   yaws 90/270 from a 5,580-px control at all, or whether that needs its own lever.
4. **Any subject-derived IoU bound** — the spread is 0.7824–0.9461 on the final set, with the
   0.78–0.80 pair being a keying artifact rather than a registration one.

Stage 1 is the next dispatch, against the pre-registered 51.33% ceiling.
