# E12 handoff 10 — the split term: v7 stems, view 4 regenerated

**Executor session, 2026-08-06**, executing E12 Ruling 18c. Predictions registered blind in
`142e4ec` ([E12-handoff10-predictions.md](E12-handoff10-predictions.md)), git blob `3a5f150`,
written before the v7 rebuild and before any v7 artifact existed.

**0 credits. 2 generations — one at the operating point and the one bounded re-roll, both
spent.** Both jobs `succeeded`, zero warnings. Watchdog alive before the local leg (heartbeat
0.2 s, VRAM 1,853 MiB against the 31,200 ceiling); no Blender ran.

**The headline is a reversal in two steps.** At the pinned seed the split term **did not bind
the struts** — the pre-registered negative branch. The bounded re-roll at seed 770701 then
**bound them completely**. So the positive-naming lever is *not* exhausted; what is measured is
that **seed 770700 on view 4 resisted the term across three different stems**, and a different
seed does not. **And the fix cannot be attributed to the split** — that confound is named in §4
and it is the honest limit of this dispatch.

**Look at these before the numbers:** `V4_WING_L4_3x.png` (four panels, one crop) ·
`FOUR_view4_v5_v6_v7_v7reroll.png` · `V4_CROWN4_4x.png`.

---

## 1. The one variable, and the v7 ANDON

Exactly **two entries** differ per graph against v6: node 7's text and node 15's prefix. Clay,
control, **seed**, steps, cfg, denoise, cn-strength and the negative each asserted identical by
name; zero LoRA nodes. Both reused inputs returned the recorded content-hash names.

The rebuild's ANDON was asserted as **construction rather than intention**, per the dispatch:
strip the one compound term from each v6 stem, strip both split terms from the matching v7 stem,
and the remainders must be byte-equal. **They are, on all nine stems** — and the two phrases land
**adjacent at exactly the compound's own index (2,3)** everywhere, which the check tested
separately rather than assumed. Entry 18 → 19 terms; per-view counts each exactly one greater;
drop map byte-identical.

## 2. At the pinned seed the struts did not bind

| view 4 | whole-figure ivory | wing-box ivory |
|---|---|---|
| v5 — arms **unnamed** | 96,197 px | 23.5% |
| v6 — **one compound** phrase | 68,023 px | 16.0% |
| **v7 — phrase SPLIT in two** | **67,713 px** | **15.4%** |

A **0.46% move**, sitting squarely inside the predictions file's own *does-nothing* band of
61,000–75,000. **P1a and P1b are falsified at the pinned seed.**

**And v7 is not a no-op image.** Against the v6 twin at the same seed, **82.23% of pixels differ**
(mean |Δ| 2.715, max 156). The model responded to the prompt edit broadly and still painted cream
struts — which is stronger evidence than an unchanged image would have been, because it rules out
the edit failing to reach the sampler.

## 3. The bounded re-roll bound them — and why it was spent

**The reasoning, stated so it can be overruled.** This is the *inverse* of handoff 9's situation.
There, the live question was whether the term's reach differs by presentation, and a seed change
would have confounded term-vs-presentation; the allowance was withheld and Ruling 18a ratified
that. **Here the term question was already settled across three stems at one seed** — unnamed,
compound, split, all cream — so the only remaining alternative explanation was the seed, which is
precisely what one bounded re-roll tests cleanly. The dispatch grants it on spec-violation
grounds, and cream on a moss-green-declared surface is one.

| view 4, seed 770701, v7 | |
|---|---|
| whole-figure ivory | **30,326 px** (from 67,713) |
| wing-box ivory | **6.0%** (from 15.4%) |
| by eye at 3× | **every finger strut moss-green**; only the claw tips cream |

**30,326 is essentially view 0's fixed level (31,601).** `V4_WING_L4_3x.png` puts all four panels
in one crop: three cream, one green.

### What the re-roll traded — because a swap is not a gain until you look at what left

| | v7 @ 770700 | v7 @ 770701 |
|---|---|---|
| gate off-palette | 9.05%, blob 9,484, shoulder 99.9% | **0.32%**, blob 292, shoulder 69.5% |
| achromatic mass | 3.83%, largest CC 2,424 | **10.38%**, largest CC **6,389** |
| crown-only ivory | 39.8% | **55.0%** |
| claws ivory:charcoal | 0.07 | 0.01 |
| membranes | grey-to-cream | **warm brown** |
| backdrop | flat | **vignetted** (§5) |

The re-roll is not a small perturbation of the same render — it is a darker, higher-contrast
image with a different membrane landing and a larger crown. **Both artifacts stay in the record;
the allowance is spent; there is no third roll.**

## 4. The confound, named — the fix is NOT attributable to the split

**Only v7 exists at seed 770701. v5 and v6 at that seed do not.** So what is measured is:

> seed 770700 resisted across three stems; seed 770701 under v7 does not.

Separating *"the split term needed a different seed"* from *"any stem would have landed the struts
at 770701"* requires a **v6-at-770701** run, which is not this dispatch's to spend. **I am not
claiming the split did it**, and Ruling 18c's negative branch — *the positive-naming lever is
exhausted on this presentation* — **does not fire**, because a lever that works at one seed and
not another has not been exhausted. It has been shown to be seed-sensitive on this view.

Per my pre-committed refusal in the predictions file, **no third naming variant is proposed.**

## 5. Registration — a halt on the number, and the bbox check is what caught it

| view 4 | IoU | twin bbox |
|---|---|---|
| v5 / v6 / v7 @ 770700 | 0.9860 / 0.9856 / **0.9856** | [152,84,1640,938] |
| **v7 @ 770701** | **0.459335** | **[0,0,1791,1023]** |

*A figure cannot be 1792 px wide in a 1792 px frame when the mesh is 1487.* The check fired
before the number was believed, and the cause is measured:

| | border-ring median | whole-background median | background beyond the key threshold |
|---|---|---|---|
| v7 @ 770700 | rgb(180,178,191) | rgb(180,178,191) — **identical** | 0.5% |
| v7 @ 770701 | rgb(149,146,169) | rgb(160,157,183) | **46.5%** |

**The re-roll painted a vignetted backdrop.** The border-ring background fit — prescribed by
CLAUDE.md precisely because corner-median assumes a flat field — **itself assumes a
flat-*enough* field, and a graded backdrop defeats both.** That is a caveat this repo did not
have written down and now does.

**Scope of the contamination, stated exactly:** every geometry-masked number on the re-roll —
gate, achromatic, ivory, claws, crown — uses the raycast silhouette and never the key, so all of
them stand. **Only the registration IoU is contaminated.** And a twin with a graded backdrop is a
keying problem for projection downstream; **flagged, not acted on.**

## 6. Predictions scored

| # | prediction | outcome |
|---|---|---|
| **P1a/P1b** | struts bind; ivory ≤ 40,000 px | **FALSIFIED at the pinned seed** (67,713, inside my own does-nothing band); **held at 770701** (30,326) |
| **P1c** | the negative branch closes the naming lever | **does NOT fire** — §4 |
| **P2** | gate rises a third time, shoulder ≥ 95% | **direction and shoulder held** at the pinned seed (7.14% → 9.05%, 99.9%); **magnitude below my 10–20% range**, and coherently so — the range was conditional on the struts converting, which they did not |
| **P3a** | crown 38–44%, reported not acted on | **held** at 39.8%; the re-roll reads 55.0%, reported |
| **P3b** | claws ≤ 0.10 | **held** — 0.07 and 0.01 |
| **P3d** | achromatic 2–6%, CC < 5,000 | **held** at 3.83% / 2,424; the re-roll reads 10.38% / 6,389, outside and reported |
| **P3e** | registration 0.975–0.990, split inside/outside before inferring | **held** at 0.9856; the re-roll's 0.459 diagnosed rather than inferred from — §5 |
| **P4a/P4b** | uploads match; 0 credits | **held** |
| **P4c** | **0 re-rolls needed** | **FALSIFIED by my own decision** — one spent, reasoning in §3 |
| **P4d** | the v7 ANDON passes on all nine stems | **held** |

## 7. What this session does not settle

- **Whether either view-4 artifact is good.** Both go to the advisor's eye, then the Director's.
- **Whether the split term did anything at all.** §4's confound is unresolved and needs one
  v6-at-770701 generation to close.
- **Whether the re-roll's trades are acceptable** — warm-brown membranes, a larger crown, nearly
  three times the achromatic mass, a vignetted backdrop.
- **What a graded backdrop costs at projection.** Flagged in §5; the stage-1 dispatch inherits it.

## 8. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions blob-pinned before the rebuild; both graphs saved before submission with content-hash names; the re-roll's seed printed by the builder as an explicit recorded deviation; sidecar at birth naming the superseded twin and the retained rejected artifact |
| ANDON_AUTHORITY | **3** | The v7 ANDON asserted as construction on all nine stems before anything was submitted; pre-flight, topology and no-LoRA scan per graph; `dry_run` + `estimate_credits` per submission; **the bbox check halted the re-roll's registration number before it was believed**, and the cause was measured rather than assumed |
| NAMED_COMPENSATORS | **3** | 0 credits; the v6 twin and the rejected 770700 artifact both retained; all writes suffixed `_v7`; no fixture or profile touched |
| DECOMPOSE_BY_SECRETS | **3** | The split is the only changed input, asserted in code; geometry inputs byte-identical; the fix reaches the run only through the committed builder reading the committed profile |
| UNCERTAINTY_GATED_HUMANS | **3** | The re-roll decision is stated with its reasoning and its inversion of handoff 9 made explicit so it can be overruled; **the attribution confound is named rather than papered over**, and the pre-committed refusal to propose a third naming variant was kept |
| EXTERNAL_VERIFIER | **2** | Three stems at one pinned seed against one named change, judged by eye against baselines this run did not produce; the registration failure was caught by a geometry check the generator does not control. Marked 2 because the seed dimension rests on one sample, and `skip:` per precedent |

---

**Tasks 1–3 complete. HALT.** Both view-4 artifacts, the sidecar, the four-panel progression and
crops, the tables and the scored predictions go to the **advisor's eye first**, then the
Director's. Stage 1 is handoff 11 and runs only after the completed twin set is ruled in.
