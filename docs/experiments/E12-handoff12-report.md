# E12 handoff 12 — the membrane iteration (v9) and the harmonization instrument

**Executor session, 2026-08-06.** Predictions registered blind in `2924a09`
([E12-handoff12-predictions.md](E12-handoff12-predictions.md)), git blob `a91ba51e`, written
before the v9 rebuild, before any v9 artifact existed and before `e13_harmonize.py` existed.

**0 credits. 8 generations — seven twins plus one bounded re-roll.** Every job `succeeded`,
zero failures, zero warnings. Six re-roll allowances unspent. Watchdog alive (VRAM 1,914 MiB
against the 31,200 ceiling); no Blender ran.

**The round's question was his, and the answer is no.**

> **`leathery` did not make the membranes storm-grey.** Seed-matched against v8, the membrane
> box's median chroma moves by a mean of **0.94 points** across the seven views — inside the
> **2.0 does-nothing band I registered before running it**. P2a is falsified by my own
> pre-registered threshold, and the direction is wrong besides: chroma *rose* on four of seven.

**And the edit was not inert** — 77.6% to 100% of pixels differ from the v8 twins at the pinned
seed. The model responded broadly to the prompt change and the membranes stayed warm, which is
stronger evidence than an unchanged image would have been.

**Look at these before the numbers:** `ab_mem0/AB_membrane_right_2x.png` (the whole finding in
one crop) · `PAIR_4v5_raw_vs_harmonized.png` (his own comparison, before and after) ·
`SET_raw_over_harmonized.png`.

---

## 1. Task 1 — the v9 stems, the arc's first substitution

Entry stays at **20 terms**; `storm-grey wing membranes` → `leathery storm-grey wing membranes`
at index 5. Because this is a substitution rather than an insertion, every per-view count is
**identical** to v8's rather than one greater — 20/20/20/14/16/14/20/20, companion 18. Drop map
byte-identical.

`e12_stem_delta.py` gained a `--substituted OLD=>NEW` mode for exactly this: the insertion
assertion cannot express an in-place change, because neither spelling is new-or-gone on its own.
It also asserts the **old spelling survives nowhere**, which an insertion check would walk past.
Run against v8 read out of git with no `--allow-dropmap-change`: **PASS on all nine stems.**
**P1a and P1b held.**

## 2. Task 2 — the membrane question, measured

Seed-matched, presented-wing box, masked to the exact silhouette. *(View 3's v8 column is its
**770700** artifact, not the adopted 770701 one — comparing against the re-roll would have
credited the term with a seed's work, and it briefly did: the naive comparison showed +8.8 and
the seed-matched one shows −0.4.)*

| view | v8 C\* | **v9 C\*** | Δ | v8 hue | **v9 hue** | Δ hue |
|---|---|---|---|---|---|---|
| 0 | 19.8 | 20.4 | **+0.6** | 87.6 | 97.3 | +9.7 |
| 1 | 26.0 | 27.3 | **+1.3** | 108.2 | 107.4 | −0.8 |
| 2 | 22.8 | 22.1 | **−0.7** | 127.9 | 127.4 | −0.5 |
| 3 | 32.4 | 32.0 | **−0.4** | 123.5 | 123.4 | −0.1 |
| 5 | 20.5 | 20.8 | **+0.3** | 121.2 | 123.8 | +2.6 |
| 6 | 24.9 | 23.9 | **−1.0** | 129.9 | 133.4 | +3.5 |
| 7 | 18.6 | 20.9 | **+2.3** | 128.0 | 132.1 | +4.1 |

**Mean absolute chroma move: 0.94 points.** Storm-grey is a neutral; nothing here is one.

- **P2a — FALSIFIED**, by the band P2b registered in advance.
- **P2c — HELD.** No membrane hue moved more than 9.7°, well under the 25° bound. 22b left the
  hue family alone and the result confirms it stayed left alone.

### The mechanism, read off the crop rather than the number

`ab_mem0/AB_membrane_right_2x.png` at 2×: the v9 membrane is **more opaque and more solid**,
with clearer wrinkle folds and less of v8's washed backlit look — and it is **more saturated
tan**. The opacity cue did contest the translucency prior. It also named a *material*, and the
material `leathery` names is tanned hide, which is warm brown.

**So the two halves of the term are pulling against each other on hue.** That is the finding, and
it is not what the word was expected to do. Relief supports it weakly and honestly: high-frequency
energy inside the membrane box moved −1.0% to +4.7%, up on five of seven — real but small.

**Both branches of P2a's pre-registered alternative are therefore partly right and neither is
clean**: the cue was not spent purely on relief, and it did not free `storm-grey` to govern.

## 3. The rest of the set — stable, which is the useful part

| view | gate % (v8 → v9) | achromatic % | largest CC | reg IoU | backdrop |
|---|---|---|---|---|---|
| 0 | 22.45 → 23.91 | 12.70 | 13,094 | 0.957463 | flat |
| 1 | 9.18 → 10.53 | 14.21 | 14,319 | 0.961112 | flat |
| 2 | 6.11 → 4.82 | 14.81 | 12,419 | 0.956764 | flat |
| **3** | 0.89 → 4.20 | 16.37 | **42,567** | 0.966628 | flat |
| 5 | 3.40 → 4.10 | 8.36 | 12,076 | 0.966503 | flat |
| 6 | 22.68 → 23.75 | 12.45 | 17,245 | 0.953315 | flat |
| 7 | 4.82 → 7.29 | 11.51 | 22,327 | 0.969264 | flat |

**P2e held on three clauses and is marginally falsified on the fourth.** The gate moved on all
seven; nape charcoal held on views 0 and 7 (+1.5 and +0.9 points against a ±8 bound);
whole-figure pale stayed within ±30% on six of seven — **view 3 moved +31.6%** (3,955 → 5,203
px), just outside, and it is reported as outside rather than rounded in.

**P2f held on both clauses**: registration 0.9533–0.9693, inside 0.950–0.985, and **0 of seven**
graded backdrops. **P2g held**: 0 credits, all sixteen reused inputs at their recorded hashes.

That stability is worth stating plainly: a term change that moved 78–100% of every image left
every other measured landing within a couple of points. The membrane failure is cleanly isolated.

## 4. View 3's bounded re-roll — the third reproduction

**P2d held.** One spend of seven, on the view named near-certain. The flat-black limb returned at
770700 for a **third independent stem generation**:

| view 3, achromatic largest CC | at 770700 | at 770701 |
|---|---|---|
| handoff 8 (v5 stems) | 43,999 | 26,546 |
| handoff 11 (v8 stems) | 41,985 | 28,057 |
| **handoff 12 (v9 stems)** | **42,567** | **28,749** |

Three stem versions, one seed, one defect, one cure, all within ±2,200 px. Ruling 21c's
best-evidenced entry now has three points. The re-roll also drops the membrane box's chroma
32.0 → 21.2 — a seed effect, not the term's, and named here so it is not misread as one.

## 5. Task 3 — the harmonization instrument

**P3a held, and the guard fired on its author first.** The first version wrote the reference
through PIL and compared **file sha256**; it raised the ANDON on a pass that was pixel-perfect,
because PIL's PNG encoder does not reproduce the cloud encoder's bytes. *File bytes are not
pixel values* — CLAUDE.md's standing rule, third instance in this repo, and this time it caught
the person writing the instrument. Corrected to copy the file verbatim **and** assert on pixels,
so both properties hold honestly rather than one standing in for the other.

| check | result |
|---|---|
| reference harmonized toward itself | **0 differing px**, bytes identical |
| **self-test — the reference through the FULL arithmetic path, no short circuit** | **0 of 1,835,008 px differ, max channel delta 0/255** |

The self-test is stronger than P3a claimed: I predicted a Lab round trip would cost a few
least-significant bits and it costs none on this data, so the short circuit is not load-bearing
and no harmonized view carries round-trip residual.

**P3b — FALSIFIED, and the reason is mine.** I predicted post-transfer moments would match the
reference to within 0.01. Measured: **0.18–0.36**. The transfer's arithmetic *is* exact; I
measured the moments after quantising to 8-bit, and uint8 rounding moves a mean by ~0.2 L\*
units. The prediction described the float arithmetic and the measurement described the file.

**P3c held, and it is the session's second real finding.**

| view | mean L\* before | correction toward the reference |
|---|---|---|
| 2 | 35.44 | +2.90 |
| 0 | 36.29 | +2.05 |
| **1 (reference)** | **38.33** | — |
| 7 | 38.54 | −0.21 |
| 5 | 39.50 | −1.17 |
| 6 | 39.69 | −1.35 |
| 3 | 39.80 | −1.47 |
| **4 (v8-A)** | **47.57** | **−9.24** |

Seven views sit in a **4.4 L\*** band. **View 4 sits 7.8 L\* above all of them**, and the total
spread is **12.13** against my predicted ≥8.0. The Director made his "not very consistent"
observation on **views 4 and 5** — the two extremes of that spread, 8.07 L\* apart. His eye went
straight to the largest tonal disagreement in the set.

**P3d held on its stated clause and found the overreach it was written to find.** Harmonized
membrane hue moved 3.4°–11.7° — under the 20° bound — and the membranes stayed warm on every
view: the transfer unified tone and did not fix a colour family, exactly as 22e says it cannot.
**One exception, reported not ruled:** view 4's membrane chroma fell 15.2 → **11.6**, crossing
the gate's chroma floor, with 53.8% of its box now below it. That is not the instrument fixing
D3 — it is the −9.24 correction desaturating the set's one outlier far enough that its already
least-warm membranes cross a threshold. It is the class of thing P3d exists to surface.

**P3e held.** Nothing adopted; harmonized files land in their own directory; view 4-A untouched.

## 6. What this session does not settle

- **Whether the membranes are acceptable.** They are not storm-grey. Whether that matters at his
  bar, and whether the escalation arm (reference-image conditioning, 22e) is now warranted, is
  his and the advisor's — the word lever has had its one iteration and it did not land.
- **Whether harmonization is adopted.** Reserved to a ruling (22e). The 4|5 pair is the artifact.
- **Whether view 4-A should stay** now that it is measured as the set's tonal outlier by 7.8 L\*.
  His sentence chose it on the nape, before this number existed. Harmonization brings it into the
  set without regenerating it — which is an argument *for* the pass, and the advisor's to weigh.
- **Which view-3 artifact stands.** Both are in the record with their measurements.
- **The crown and the three-charcoal-terms watch item.** Unchanged from handoff 11; not re-opened.

## 7. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions blob-pinned before the rebuild and before the instrument existed; all eight graphs written to disk before submission with content-hash names; the re-roll seed printed as a recorded deviation; `build_v9.ps1` saved with its diff-from-v8 header and the pre-change membrane measurement in the note; every harmonization operand (mean and sigma per channel, before and after, per view) recorded in `operands.json` |
| ANDON_AUTHORITY | **3** | The substitution ANDON against git on nine stems; pre-flight, topology and no-LoRA scan per graph; **the harmonization identity test halted the run before a single number could be read, and it halted its own author** — the correction is in the file with the reason; the view-4 exclusion is enforced in the driver with its own throw rather than left to a retyped loop |
| NAMED_COMPENSATORS | **3** | 0 credits; harmonized outputs land in a separate directory and replace nothing; view 4-A never regenerated; the 770700 view-3 artifact retained beside its re-roll; all prior artifacts intact |
| DECOMPOSE_BY_SECRETS | **3** | Semantic work (the term) and tonal work (the transfer) kept in separate tasks with separate measurements, exactly as 22e separates them; the reference view is named by ruling, not chosen by this session; the membrane instrument derives its boxes from geometry, not from the images it measures |
| UNCERTAINTY_GATED_HUMANS | **3** | The does-nothing band was registered before the run and it is what falsifies the round's own hypothesis; his two acceptance questions are answered as measurements plus artifacts, not as verdicts; the view-4 tonal-outlier finding is handed up beside the sentence it complicates rather than acted on |
| EXTERNAL_VERIFIER | **2** | The identity test is a property the tool's arithmetic cannot fake and it fired against its author; the membrane instrument grades colour against a declaration written before the images existed; registration measured against geometry the generator does not control. `skip:` on a second model per the arc's precedent |

---

**Tasks 1–3 complete. HALT.** The seven v9 twins, view 3's re-roll and its retained artifact, the
harmonized set with its operands, the membrane tables, the gate/achromatic/registration tables,
the A|B crops and the 4|5 pair go to the **advisor's eye first, then the Director's**. His two
questions have answers: **the membranes are not storm-grey**, and **the harmonized set is
measurably one dragon where the raw set is not** — but whether it *reads* as one is his.
