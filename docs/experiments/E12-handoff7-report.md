# E12 handoff 7 — the palette bands against the accepted pair, and the D8 closure

**Executor session, 2026-08-06.** Predictions registered blind in `a22a949`
([E12-handoff7-predictions.md](E12-handoff7-predictions.md)), git blob `a76a128`, written
before any clustering, hue census, backdrop estimate or per-element ΔE existed. This report
proposes one band, **suspends the other**, bands no contested element, and attaches no verdict.

**No generation, no GPU, no Blender, no credits** — colour arithmetic on artifacts already in
hand. Watchdog not required by any leg; checked anyway for the record: **alive, heartbeat 2.0 s,
VRAM 2,207 MiB against the 31,200 ceiling.**

**Two headline findings for the ruling.** (1) **Ruling 8a's stated ground is stale on the
accepted artifact**: blue-violet is no longer "the one hue family no declared material
occupies" — a D3 membrane stratum realises there, and it is the pair's entire second band.
(2) **The pooled landing table reports a clean `LANDED` for D7** while one of its two views
carries the accepted deviation — which was **pre-registered before the table was run**.

**Look at these before the numbers:** `bands_v2/D8_CLOSURE_eye_8x.png` ·
`bands_v2/bands-proposed.json` · the accepted pair itself.

---

## 0. The instrument, checked before any new number was read from it

`e04_bands.py` was re-run on **both** artifacts whose figures are already published, on their
recorded command lines:

| run | published | measured now |
|---|---|---|
| **galleon** (E04 Task 4d) | hues 62,69,77,77,82,86,87,88 \| 283,291 · bands 62–88, 283–291 · G7 ΔE 34.7 NEAR · G11 ΔE 14.5 / 2.14% · backdrop 0.1000 / asked 0.2471 / W3 0.1451 | **every figure identical** |
| **beast, REJECTED pair** (Task 4/5) | hues 96,98,101,101,102,121,124,126,133,136,138 \| 345 · bands 96–138, 345–345 · D1 ΔE 4.4 / 13.48% · D8 ΔE 57.2 NOT FOUND · D9 ΔE 23.3 / 0.50% · backdrop rgb(188,183,202) 0.2353 / asked 0.2000 / W3 0.0745 | **every figure identical** |

**P5b held.** One incidental correction to the record: the galleon's run consumes
`E04_task4/masks1024/`, not `masks/` — the 1072-wide masks raise an IndexError against a
1024-wide pair. The recorded numbers were always the 1024 ones; only the path was ambiguous.

## 1. Predictions scored — 13 held, 4 falsified, 1 outside its stated range

| # | prediction | outcome |
|---|---|---|
| **P1a** | collapse recurs: one group ≤ 60° wide holding ≥ 55% | **held, narrowly** — 95.4–137.3, **41.9° wide, 55.23%**. Held by 0.23 points |
| **P1b** | below-floor share rises above 17.90%, predicted 20–40% | **FALSIFIED ON THE LETTER** — **40.25%**, 0.25 points above my stated ceiling. Direction and mechanism right; the range was wrong |
| **P1c** | forbidden span ≥ 278.1°, predicted 275–310° | **held** — **278.1° (77.2%)** |
| **P1d** | 0 or 1 clusters exceed ΔE 25 from every declared element | **held** — **zero**, worst 19.7. The named branch (the membrane's pale field) did not fire; it sits second-worst at 18.3 |
| **P2a** | realised backdrop L\* 70–80, C\* 8–14, h 290–310 | **held on all three** — rgb(177,174,194), **L\* 71.8, C\* 11.0, h 297.8** |
| **P2b** | min-distance to clusters 0.20–0.28 | **FALSIFIED** — **0.1843**, below the range and below the rejected pair's 0.2353 |
| **P2c** | W3's grey scores 0.05–0.09 | **FALSIFIED** — **0.0314**, less than half the floor of my range, and now well **under** the key's 0.06 cut where the rejected pair had it 1.24× over |
| **P2d** | corner median and outside-silhouette estimates agree within ΔE 3 | **held decisively** — **ΔE 0.38** |
| **P3-D2** | the pair lands nearer my olive-tan reading than the superseded bone-tan | **held** — ΔE **7.92** against **9.96**, and to different clusters |
| **P3-D3** | D3 suspends with strata; no single point band is honest | **held, and more strongly than predicted** — §4 |
| **P3-D6/D11** | charcoal and slate land below the chroma floor | **held** — C\* 5.0 and C\* 6.5 |
| **P3-D9** | D9's cluster survives at 0.2–0.7% share | **FALSIFIED** — **no wine cluster exists** on the accepted pair; ΔE 32.7, `NEAR`, assigned to the dark slate |
| **P3a** | the ivory family merges | **held** — D4/D5/D10 all → rgb(224,212,169), 3.69% |
| **P3a-consequence** | view 1's deviant ivory claws land in that ivory cluster | **held, and the consequence is worse than I stated** — §5 |
| **P4a** | D8: 100–400 px at ΔE < 25, one blob, 100% inside the head region | **held on every clause** — **193 px, 0.0393%, one blob, 100%** |
| **P4b** | the cluster table returns NOT FOUND for D8 | **held** — ΔE 58.4, against a cluster floor 20× the eye's size |
| **P4c** | the closure carries the 12g contradiction without resolving it | **held** — §6 |
| **P5a/P5b** | no generation/GPU/credits; the instrument reproduces | **held** — §0 |

### The one prediction I registered as a LIMIT, and it was wrong

I pre-registered that the charcoal estimate sitting ΔE 5.86 from D11's slate meant the two
**could not be told apart** by a nearest-cluster table. **Measured, the assignment is not a coin
flip:**

| element | assigned | runner-up | margin |
|---|---|---|---|
| D6 charcoal | rgb(61,70,65) ΔE **5.64** | rgb(42,45,53) ΔE 10.48 | 4.84 |
| D11 slate | rgb(42,45,53) ΔE **5.74** | rgb(61,70,65) ΔE 9.23 | 3.49 |

My limit was too pessimistic and the measurement says so. **A different and worse caveat
replaces it**, and it is not about colour distance at all: **71.7% of D11's assigned cluster
sits on view 5** — whose camera cannot see the head and whose stem drops the entire mouth
family. Its 5.95% share is shadow, not mouth interior. The same holds for D6/D7's cluster at
8.73%, which is far more area than spines and claws occupy. **Both dark rows are colour matches
to shadow.** That is the galleon's colour-not-placement caveat, and on this subject it is
sharper than the merge problem I predicted.

## 2. What is actually on the accepted pair — 14 clusters, pooled over both views

Inside the exact geometry silhouette, 490,941 px per view, k-means in Lab, seed 770700.

| share | rgb | L\* | C\* | h | nearest declared | ΔE |
|---|---|---|---|---|---|---|
| 11.79% | (85,91,66) | 37.9 | 15.7 | 119.0 | D1 | 6.4 |
| 9.61% | (58,68,46) | 27.2 | 14.9 | 124.9 | D1 | 9.7 |
| 9.26% | (130,126,95) | 52.2 | 18.1 | 101.5 | D1 | **19.7** ← worst |
| 8.81% | (32,44,29) | 16.0 | 10.9 | — | D6 | 13.4 |
| 8.73% | (61,70,65) | 28.8 | 5.0 | — | D6 | 5.6 |
| 7.98% | (173,162,125) | 66.8 | 21.0 | 95.4 | D2 | 7.9 |
| 6.73% | (48,85,38) | 31.7 | 31.6 | 135.6 | D1 | 12.2 |
| 6.51% | (14,18,15) | 5.3 | 1.1 | — | D11 | 18.6 |
| 6.18% | (84,119,77) | 47.1 | 28.1 | 137.3 | D1 | 14.6 |
| 5.95% | (42,45,53) | 18.2 | 6.5 | — | D11 | 5.7 |
| 5.91% | (156,162,142) | 65.7 | 10.4 | — | D2 | 18.3 |
| **4.52%** | **(74,79,97)** | 34.2 | **12.9** | **283.4** | D11 | 14.0 |
| 4.34% | (109,113,115) | 47.8 | 1.3 | — | D3 | **3.1** ← tightest |
| 3.69% | (224,212,169) | 86.1 | 21.6 | 96.4 | D4 | 8.6 |

Hue is printed only where C\* ≥ 12.0; six clusters carry none. **40.25% of the figure is below
the chroma floor**, against 17.90% on the rejected pair — the correction traded two chromatic
pale terms for charcoal, a near-neutral, and it joined slate and the membranes down there.

**The floor stays at 12.0, inherited from W3, and is not moved.** This subject still has no
measurement that would justify a different one, which was the rejected pair's finding too.

## 3. The bands — one proposed, one SUSPENDED

Above-floor hues, pooled: **95, 96, 102, 119, 125, 136, 137 | 283**.

| band | measured | proposed | width | rests on |
|---|---|---|---|---|
| **warm-olive** | 95.4–137.3 | **85.4–147.3** | 61.9° | **7 clusters, 55.23%** of the figure — D1, D2 and the ivory family |
| **blue-violet** | 283.4–283.4 | *(273.4–293.4)* | 20.0° | **1 cluster, 4.52%** — **SUSPENDED, not proposed** |

The ±10° margin is a **convention inherited from the galleon's table, not a measurement**.

### ⚠ Why the second band is suspended — three reasons, any one sufficient

1. **One cluster cannot fix a band edge.** The galleon suspended its blue on 2 clusters /
   3.69%; the rejected beast pair suspended its wine on 1 cluster / 0.50%. This is the same
   shape and gets the same answer: numerator and denominator, no edge.
2. **Its nearest declared element is a placement impossibility.** D11 at ΔE 14.0 — the *mouth
   interior* — while **71.7%** of the cluster's mass sits on view 5, which cannot see the head.
3. **By location it is a D3 membrane stratum** (7.3% of view 5's membrane box), and D3's own
   best landing is a *different* cluster, below the floor. Arming this band would give 20° of
   forbidden span to a stratum no declared element names.

**Cost of the choice, stated both ways:** forbidden span **278.1° (77.2%)** with the band armed,
**298.1° (82.8%)** without it. The advisor rules; nothing is armed here.

### Forbidden-span arithmetic

| | allowed | **forbidden** |
|---|---|---|
| W3 (character) | 0–105, 125–210 | 170° — 47.2% |
| galleon (measured) | 50–100, 273–301 | 288° — 80.0% |
| beast, **rejected** pair | 85.6–147.5, 334.6–354.6 | 278.1° — 77.3% |
| beast, **accepted** pair | 85.4–147.3, 273.4–293.4 | **278.1° — 77.2%** |

**The equality with the rejected pair is construction, not meaning, and should not be read as
one.** Both are one ~42° group plus one single-cluster point band, each widened by the same
±10°: (41.9 + 20) + 20 = 81.9° allowed either way. **The second band is a different colour on
each pair** — wine at 344.6 on the rejected, blue-violet at 283.4 on the accepted.

### Per-view census

| | warm-olive group | blue-violet | below floor |
|---|---|---|---|
| **view 1** | 95.4–137.3, 6 clusters, **64.13%** | 0.85% | 35.02% |
| **view 5** | 95.4–137.3, 7 clusters, **46.33%** | **8.19%** | 45.49% |

**H1/H4, the register confound, resolved.** Ruling 10e banked the rejected pair's collapse —
eleven declared materials as one 42° hue group on 81.6% — as *register-confounded*. Under a
different register (no LoRA, ultra-realistic) and a corrected palette, **the collapse recurs**:
one 41.9° group. The group's *share* falls (81.61% → 55.23%), but only because mass moved
**below the chroma floor**, not because it spread across the hue circle. **The register was not
the cause.** The cause is the one the galleon found first — a realised palette far tighter than
its declared names suggest. Third subject, third time.

**H4 a third time: zero clusters outside the declared table**, worst 19.7. The galleon had
extras; neither beast pair does.

## 4. D3 — suspended, with its strata

**D3's own best landing is the tightest in the entire table — ΔE 3.1 — and it sits at C\* 1.3,
far below the chroma floor.** The membrane fields carry at least four strata:

| stratum | rgb | L\* | C\* | h | in view 5's membrane box |
|---|---|---|---|---|---|
| lit trailing field | (156,162,142) | 65.7 | 10.4 | — | 19.0% |
| storm-grey (D3's landing) | (109,113,115) | 47.8 | 1.3 | — | 10.1% |
| deep shadow | (42,45,53) | 18.2 | 6.5 | — | 8.6% |
| **blue-violet** | (74,79,97) | 34.2 | **12.9** | **283.4** | 7.3% |

**Only one of the four is above the floor, and it is the one that produced the suspended band.**
**No hue band for D3 is possible** — its mass carries no quotable hue. The honest output is the
lightness range **L\* 18.2 – 65.7 at C\* ≤ 12.9**, reported as strata rather than proposed as a
band. E12 Ruling 13e anticipated exactly this and it is what the data does.

## 5. The pre-registered consequence — and it is worse than I stated

I registered, before the table existed: *view 1's ivory foot claws will land in the ivory
cluster, so the landing table cannot distinguish the deviation from a correct D10 landing.*

**Measured, in view 1, ivory-cluster occupancy by box:**

| box | figure px | ivory-cluster px | share |
|---|---|---|---|
| **FEET** — D7 declares **charcoal** | 21,709 | **3,887** | **17.91%** |
| HORNS — D4 declares ivory | 4,587 | 1,748 | 38.11% |
| MOUTH/FANGS — D10 declares ivory | 29,767 | 3,074 | 10.33% |

The claws sit in the ivory family's cluster at a higher share than the fangs do. **And the
consequence runs further than I predicted**: the pooled table's D7 row reads **`LANDED`, ΔE
5.6** — against the *charcoal* cluster, which exists because **view 5's** claws are charcoal.
So the two-view table hands D7 a clean pass while one of its two views carries the deviation the
Director accepted at Ruling 14. **A reader taking that row as evidence the claws are fine has
been misled by an instrument doing exactly what it does.** D5 and D7 are reported per-view with
**no band**, per the dispatch.

## 6. Task 2 — the D8 closure, on the accepted artifact

Ruling 2's named checkpoint, held open through 10g on a rejected artifact. Closed here on one
that stands.

| threshold | px | % of figure | blobs | largest | bbox | inside the head box |
|---|---|---|---|---|---|---|
| ΔE < 15 | 98 | 0.0200% | 2 | 96 | (434,335)–(454,347) | **100%** |
| **ΔE < 25** | **193** | **0.0393%** | **1** | **193** | **(434,334)–(455,348)** | **100%** |
| ΔE < 40 | 231 | 0.0471% | 1 | 231 | (434,334)–(455,348) | **100%** |

One blob, **22 × 15 px**, entirely inside the head region, where the geometry has one eye.
`bands_v2/D8_CLOSURE_eye_8x.png` is that region at 8×: an ember-orange iris with a **vertical
slit pupil**, on a scaled brow, nostril below-left, tooth rows below. **The eye is judged by the
eye, and the verdict is the Director's** — this report records that the element is present,
where, how large, and what shape.

**Three facts the closure carries together, because none of them is complete alone:**

1. **The cluster table says NOT FOUND at ΔE 58.4.** The 14-cluster floor is 0.4% = **3,927 px**;
   the eye is **193 px**, twenty times below it. That is the instrument being blind by
   construction, **pre-registered in `DRAGON-IDENTITY.md` since before any pair existed**, and
   it is not a miss.
2. **It is smaller than the rejected pair's.** That pair measured 153 px at ΔE < 15 / **282 px**
   at ΔE < 25, in a 33 × 20 blob; this one is 98 / **193**, 22 × 15. The eye landed on both
   registers, smaller on the accepted one.
3. **Ruling 12g's contradiction stands unresolved, and nothing here explains it.** The
   bust-scale companion — ~33× the pixels, the same dense control — painted **no** eye at all,
   and the clay at that socket shows overlapping brow plates with no lens recess. A pair-scale
   eye at 193 px and a bust-scale absence at 33× the resolution are both measured facts. **This
   closure does not reconcile them and does not claim to.**

## 7. The backdrop, re-measured under the accepted register

| | rgb | L\* | C\* | h | min-dist to measured clusters |
|---|---|---|---|---|---|
| asked (the ruled word) | (121,121,172) | 52.6 | 29.58 | 293.7 | 0.1608 |
| **realised, corner median** | **(177,174,194)** | **71.8** | **11.0** | **297.8** | **0.1843** |
| realised, outside-silhouette median | (177,173,193) | 71.4 | 11.0 | 298.7 | — |
| W3's inherited grey | (106,106,107) | — | — | — | **0.0314** |

**The method check first (P2d).** `e04_bands` samples the backdrop by **corner median**, which
carries the flat-field assumption CLAUDE.md retired for *keying*. Both estimates are reported —
the corner median because it is the only figure comparable to the recorded 0.2353 and 0.1000,
and a full outside-silhouette median beside it. **They agree to ΔE 0.38.** The recorded figures
are measurements of a backdrop, not of a corner.

**The ask→realise transfer repeats exactly.** L\* 52.6 → 71.8, C\* 29.58 → **11.0** (−63%), hue
surviving at 297.8. The word lands and its saturation does not — the same direction, and nearly
the same magnitude, as the rejected pair's −65%.

**Two margins moved, both worse, and both bound by something new:**

- **Realised backdrop: 0.2353 → 0.1843.** Bound by the **ivory cluster** rgb(224,212,169) at
  3.69% — the horns, crown and fangs, and view 1's deviant claws.
- **W3's inherited grey: 0.0745 → 0.0314.** Bound by rgb(109,113,115) at C\* 1.3, 4.34% —
  **D3's storm-grey**, the tightest landing in the table. It was 1.24× *over* the key's 0.06
  cut on the rejected pair; it is now **1.9× under it**. **Ruling 8b is corroborated far more
  strongly on the accepted artifact than it was on the rejected one**, and by exactly the
  element the backdrop derivation said would bind — *"D3 bound EVERY optimum."*

### ⚠ Ruling 8a's stated ground is stale

Ruling 8a chose `plain lavender-grey` because blue-violet is **"the one hue family no declared
material occupies."** On the accepted pair, **a D3 membrane stratum occupies it** — h 283.4,
C\* 12.9, 4.52% of the figure, 8.19% of view 5 — and it is the pair's entire second band. The
realised backdrop sits at h 297.8, **4.4° outside** that band's would-be upper edge of 293.4.

**The softening fact, in the same breath: the realised backdrop's C\* is 11.0, below the gate's
own 12.0 floor.** Under the gate's rule the backdrop carries **no hue at all**, so a hue-band
collision with it is not evaluable. **The premise is stale; the arithmetic is not yet broken.**

**No replacement backdrop word is proposed here.** Choosing one while looking at the result it
would be judged against is the retuning this repo forbids, and the galleon's 4d refused the
same move for the same reason. The measurement is reported; the word is the advisor's.

## 8. What this session does not settle

- **Whether the bands are right.** One is proposed, one suspended, two elements unbanded by
  instruction. The advisor rules them into `profiles/beast.json`; nothing was written there.
- **D5's and D7's dispositions.** Reported per-view with numbers and no bands, per Ruling 14.
- **Whether the second band should ever be armed**, and what the backdrop word becomes. Both
  reported with their arithmetic; neither decided.
- **Why D9's wine survived clustering on the rejected pair and not on the accepted one.** One
  measurement each; no arm exists to separate scale from register from seed.
- **The 12g eye contradiction**, §6.3.

## 9. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions hashed and blob-pinned before the first measurement; the three corrected expected triples fixed in that same commit so they could not be nudged toward the result; clustering seed 770700 and the chroma floor named as inherited; every triple carries its box, view, mask and share |
| ANDON_AUTHORITY | **3** | The instrument reproduced two published runs exactly before a new number was read from it; the second band is **suspended** with numerator and denominator rather than armed on one cluster; D3 is reported as strata rather than forced into a point band; no backdrop word is proposed while looking at the result it would be judged against; contested elements halt to the ruling unbanded |
| NAMED_COMPENSATORS | **3** | No generation, no spend, no irreversible step; all writes in the new `bands_v2/` subdirectory plus one new report; `canon/` and `profiles/` opened read-only, and the corrected materials table written as a NEW file in the output tree rather than as an edit to a canon file |
| DECOMPOSE_BY_SECRETS | **3** | Bands derive fixture-side and cross-check pair-side; the twins they will gate contributed nothing and none exist; the register-confound census is separated from the banding it informs; the one inherited constant (C\* 12.0) is named as inherited and not moved |
| UNCERTAINTY_GATED_HUMANS | **3** | Every band, both dispositions and the backdrop word go to the ruling; D8 and D9 stay below any floor and eye-judged; the pre-registered limit that turned out **wrong** is scored as wrong in §1 rather than quietly dropped; the 12g contradiction is carried unresolved |
| EXTERNAL_VERIFIER | **2** | The clustering derives from the image and not the expectation, so an element can fail — and D9 did; the pair was judged by the Director's eye, not by these instruments. Marked 2 because every number rests on one pair, and `skip:` on a second model per the arc's precedent |

---

**Both tasks complete. HALT.** The proposed band, the suspended one with its arithmetic, the
contested elements' per-view numbers, the collapse census, the backdrop re-measure and the D8
closure go to the **advisor's eye first**, then the Director's if his window is wanted. Twins
are handoff 8 and are not this session's.
