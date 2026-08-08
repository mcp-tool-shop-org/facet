# E14 handoff 8 — the collar repair landed and all seven strokes committed. HALT 2.

**Executor session, 2026-08-08.** Ruling 28 (`eac4e19`), executed. **The repair asserted all
three counts and landed; the seven strokes ran in the ruled order; no ANDON fired; no re-roll
spent; 0 credits across seven submissions.** One watch did not read clean on three strokes and
is flagged below rather than cleared.

---

## 1. Step 0 — the collar-junction repair (Ruling 28d)

The union derived and asserted before a byte was written:

```
[repair] CLAUSE P  territory AND edge AND stage-1b gold              1,431
[repair] CLAUSE O  territory AND forbidden-after AND NOT before      1,086
[repair]   of clause O, outside clause P                                 5
[repair] THE RULED MASK  P OR O                                      1,436
[repair] ASSERTED against Ruling 28d: P 1,431 / O 1,086 / union 1,436
[repair] ASSERTED: clause O is identical on the LIVE atlas - no committed stroke touches this
[repair] restored 1,436 texels' atlas colour from state0
[repair] |delta| per texel, 8-bit: median 23  max 68
[repair] ASSERTED: colour changed inside the ruled mask ONLY;
         holes.png and styled_mask.npy BYTE-IDENTICAL (a colour-only operation)
[repair] atlas sha256  fa75204e8bc61627eae43b46  ->  536d86b6826949b826ec7be0
```

**The compensator was exercised before the real op** (`--verify-undo` on a scratch copy: repair
→ undo → all three state files byte-identical), and the real run reproduced the scratch run's
atlas hash exactly. The stroke-1 orthogonality claim is now asserted **inside the tool** rather
than in a report: clause O recomputed on the live atlas is the identical set.

**The line is gone at 6× in all eight views** — `gates/STEP0_collar_repair_before_after.png`,
FLAT light, common crop band, before/after per view. Forbidden-band px inside the junction crop:

| yaw | 0 | 45 | 90 | 135 | 180 | 225 | 270 | 315 |
|---|---|---|---|---|---|---|---|---|
| before | 50 | 56 | 49 | 39 | 62 | 66 | 56 | 37 |
| **after** | **20** | **22** | **13** | **18** | **39** | **41** | **26** | **12** |

The ~20 that remain under both candidates are 28e's forbidden-BEFORE class; not chased.

## 2. ⚠ THE ANCHOR, before any stroke — and what it caught

Stroke 1's job was re-emitted from the recorded state and compared against what is on disk:
**`render.png`, `mask.png`, `hit.png` and `cam.json` all byte-identical.** The first attempt was
NOT identical, and the reason is worth the line: **omitting `--profile` silently emits a
752-wide frame instead of the profile's 240** (`v_ext` identical, `h_ext` and `W` different).
An unprofiled run does not error — it produces a differently-framed job that would have
committed through a different projection than it emitted. The anchor caught it in one command.

## 3. The seven strokes — every watch measured and located

Structures are labelled by **geometry**, not row bands: `e14_stroke_watch.py` raycasts the
job's own camera against the mesh and labels each pixel by the z of the surface it hits, against
a structure map derived once from the mesh's width profile
([E14-longsword-structures.json](E14-longsword-structures.json), placed in `docs/experiments/`
and **not** in `canon/` — a fixture row is the advisor's fold).

| # | yaw | job mask | probe | **committed** | **probe→actual** | red on crossing/blade | gold on blade | forbidden | fifth signature | 20b |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 180 | 9,500 | 6,559 | **4,540** | **0.692** | 0 / 0 | 50 | 4 | 20/20 clean | clean |
| 3 | 45 | 10,115 | 10,539 | **5,236** | **0.497** | 0 / 0 | 8 | 0 | 20/20 clean | clean |
| 4 | 225 | 9,679 | 8,600 | **2,378** | **0.277** | 0 / 0 | 5 | 0 | 20/20 clean | clean |
| 5 | 315 | 10,299 | 9,633 | **4,076** | **0.423** | 0 / 0 | 0 | 8 | ⚠ **2/20, worst +6.3** | clean |
| 6 | 135 | 10,307 | 7,728 | **2,562** | **0.332** | 0 / 0 | 56 | 1 | 19/20, worst +0.4 | clean |
| 7 | 90 | 9,188 | 14,211 | **14,719** | **1.036** | 0 / 0 | 0 | 6 | ⚠ **4/20, worst +8.1** | **clean** |
| 8 | 270 | 9,750 | 27,010 | **38,035** | **1.408** | 0 / 0 | 0 | 8 | ⚠ **0/20, worst +12.6** | **clean** |

**Seven strokes: 71,546 texels. With stroke 1's 4,344: 75,890.** The invariance ANDON passed on
all seven (mean 0.030–0.056 lv, largest hot component ≤ 2 px). `estimate_credits` quoted **0**
before each of the seven; link topology checked in code each time (no self-links, no dangling
targets); every graph saved pre-submission with its cloud input names. The drop map landed: the
boss term is absent at yaw 90 and 270 (10 terms) and present elsewhere (11).

**The stone and the repair are untouched.** Of the 71,546 texels the seven strokes changed,
**0** are in the stone territory and **0** are in the collar-repair mask — measured, not asserted.

## 4. ⚠ THE FIFTH SIGNATURE DID NOT READ CLEAN ON THREE STROKES

Reported as fired, not cleared. On strokes 5, 7 and 8 the fill is more dark+desaturated than the
context at 18, 16 and 20 of 20 (L\*, C\*) cuts. It **survives per-structure decomposition** — at
the L\*<25 / C\*<12 cut, stroke 5 reads +4.7 on the crossing and +3.0 on the blade — so it is not
an artifact of mask composition. At 5× the blade's fuller seams read visibly darker than the
surrounding steel: E12 Ruling 27d's described class exactly.

**The Director ruled at the gate: commit and flag, re-roll unspent** (the alternative — treating
the dispatch's "less-or-equal is clean" as halt authority — would have spent the bounded re-roll
and risked halting the lane at stroke 5 on a watch E12 27d deliberately armed no numeric gate
on). The crops are in `gates/GATE5_y315.png`, `GATE7_y090.png`, `GATE8_y270.png`.

**One instrument note.** Stroke 1's recorded 29.1% / 31.8% does not reproduce at any single cut
in this grid, so the absolute figures here are on a stated definition and are comparable
stroke-to-stroke within this session but **not** to stroke 1's numbers. The relation is what is
comparable, which is why the grid is reported rather than one threshold.

## 5. ⚠ RULING 27d's UPPER BOUND IS FALSIFIED, and the pre-registered falsifier is the one that fired

The predictions committed before stroke 2 said: *"if any stroke exceeds its probe column at all,
Ruling 27d's upper-bound finding is wrong."* **Two did** — stroke 7 at 1.036× and stroke 8 at
**1.408×** — and the eight strokes together committed **75,890 against the 69,239 achievable
set: 109.6%.**

The ratio is not a constant optimism factor: measured **0.277 to 1.408 across eight strokes**,
against the single 1.75× (0.572) point at yaw 0 that the calibration was built on. The two
overshoots are both edge-on and both ran last, which is the mechanism worth a ruling's attention:
the probe fake-inpainted a *sparsely painted* blade, while the real edge-on strokes ran against
a blade six strokes' worth of paint denser, and the keyed figure they emit is correspondingly
larger. **The probe's error changes sign with how much context exists** — it over-estimates a
lightly painted frame and under-estimates a heavily painted one.

## 6. Coverage, both denominators, and the on-surface family (Ruling 9's form)

| | |
|---|---|
| committed this lane (8 strokes) | **75,890** |
| against the achievable set 69,239 | **109.6%** |
| against the territory 210,907 | **36.0%** |
| styled total | **1,732,737** of 3,661,903 valid = **47.32%** (from 1,656,847) |
| islands in the new paint | **19,593** (largest 649, median 1) |
| erode-2 residue of the new paint | 6,593 = **8.7%** |
| **off-surface rate** | **0 texels, 0.0000%** |

The new paint is rim-and-ribbon by construction (median island size 1), which is what the
strokes were dispatched to be and what the 24c dilation argument assumes at finalize.

## 7. The report-only palette gate and the deep-share, with location

**Palette gate** (Ruling 17, report-only, both bounds null), on the eight final views against
their own geometry masks:

| yaw | 0 | 45 | 90 | 135 | 180 | 225 | 270 | 315 |
|---|---|---|---|---|---|---|---|---|
| off-palette px | 341 | 261 | 171 | 210 | 268 | 238 | 153 | 318 |
| % of figure | 0.69 | 0.65 | 0.71 | 0.52 | 0.54 | 0.59 | 0.63 | 0.79 |
| largest blob | 68 | 12 | 10 | 13 | 15 | 19 | 14 | **121** |

Totals sit above the record's 5–104 px clean-view range; the largest blob (121 px, yaw 315) is
two orders below the 4,882 / 5,068 single-blob failures the two-threshold law was written for.

**Deep-share, atlas-wide:** the lavender-rim band is **19,530 texels both before and after the
lane — the seven strokes added exactly zero.** Its share falls 1.179% → **1.127%** on
denominator growth alone. Location shifts: **L1 blade 79.0%** (from 91.8%), **L2 crossing 20.3%**,
L5 stone **133** (unchanged).

⚠ **An instrument discrepancy, unreconciled and flagged rather than smoothed over.** The
re-projection report's "interior (survive erode-2) 5,257 = 26.92%" **does not reproduce with my
erosion**: run on the same pre-lane state, my 3×3 / 2-iteration erosion of the styled mask gives
**1,577 = 8.07%**. On one consistent instrument the figure *rises* across the lane
(1,577 → 3,181; 8.07% → 16.29%), which is the only direction mask growth allows. I checked this
precisely because the cross-session figure moved the wrong way. **The two sessions' erosions are
different instruments and their interior figures are not comparable**; the band's absolute count
reproduces exactly, and that is the number to read.

## 8. The blind predictions, graded

Committed before stroke 2 submitted ([E14-handoff8-predictions.md](E14-handoff8-predictions.md)).

| prediction | outcome |
|---|---|
| per-stroke counts, ~40,400 for the seven | **WRONG** — 71,546, +77% |
| every ratio in 0.35–0.65 | **WRONG** — 5 of 7 outside (0.277, 0.332, 0.692, 1.036, 1.408); only strokes 3 and 5 landed inside |
| the two edge-ons carry the two *lowest* ratios | **WRONG, and inverted** — they carry the two highest |
| any stroke exceeding its probe falsifies 27d's upper bound | **the falsifier fired** — two did |
| **both edge-on strokes 20b CLEAN** | **CORRECT** — the guard's edge-on face is the clay's faceted block; the ribbon is continuous steel; no crossguard-like or figurative form at either face |
| fifth signature below context on all seven, zero firings | **WRONG** — 3 of 7 fired |
| deep-share share 1.05–1.15% | **CORRECT** — 1.127% |
| deep-share absolute 19,800–20,600 | **WRONG** — 19,530, unchanged |
| blade keeps >90% of the band | **WRONG** — 79.0% |
| the stone stays at or below 133 | **CORRECT** — 133 |
| zero credits on all seven | **CORRECT** |
| the invariance ANDON passes on all seven | **CORRECT** |

Four of twelve. The mechanism I got right was the misbind one; the mechanism I got wrong was
that I modelled the probe ratio as a property of the *mask's* rim fraction when it is a property
of how much *context* has been painted — the same class of error the record already names, that
I reasoned about geometry where the answer was in the pipeline's own dependency.

## 9. What has NOT been done

- **No re-roll spent on any stroke.** All seven budgets are intact; no seed but 770700 ran.
- No profile, fixture, palette or ruling edit; no memory-store write; no gate armed.
- No finalize, no pack beyond the walk-set render GLB. Gate 1 is the next dispatch.
- **0 credits** across seven submissions, quoted before each.
- The demotion's compensator and the repair's compensator both stand, exercised and unused.

## 10. The walk set — staged for the advisor, then the Director

```
gates/HALT2_walkset_1_views.png    reference | BEFORE | AFTER | PROVENANCE, all eight views,
                                   native 240x1024 FLAT. Provenance key in-image: grey =
                                   stage-1b paint, MAGENTA = the garnet re-projection (67,904),
                                   CYAN = the collar repair (1,436), YELLOW = stroke 1 (4,344),
                                   GREEN = this session's seven (71,546), black = still holes
gates/HALT2_walkset_2_crops.png    the STONE at 6x beside the fixture (yaw 0/45/180) · the
                                   CROSSING at 4x (four views) · the RIBBON at 4x BOTH FACES,
                                   before|after per face
gates/STEP0_collar_repair_before_after.png    the repair, eight views, 6x
gates/STEP0_collar_repair_candidates.png      the halted candidates (labelled AS SUCH in-image)
gates/GATE2..GATE8_*.png           per-stroke eye gates, each carrying the CLAY reference
run/s2..s8/{atlas,holes,styled_mask,commit.log,watch.json}   the per-stroke state chain
run/graphs/stroke2..8_*.json       the submitted recipes, saved pre-submission
```

**Final SHAs** (`run/s8/`): atlas `34dafd4b57aa5b04df935cfb` · holes `e05e450800dc500f3b2a55d9` ·
styled `322ebdf6b55055da7614e506`. GLB: `run/HALT2_stroked_sword.glb`.

## 11. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The anchor re-emitted stroke 1's job byte-identically before any stroke ran; all three repair counts asserted; every graph saved pre-submission with cloud input names; probe-vs-actual quoted per stroke; the structure map frozen with its derivation |
| ANDON_AUTHORITY | **3** | The repair's count assert ran ahead of any write; the in-tool invariance ANDON passed on all seven with no skip; the commit ANDON untouched; the fifth-signature firing was escalated to the Director at the gate rather than resolved by the executor |
| NAMED_COMPENSATORS | **3** | The repair's compensator exercised on scratch before the real op and reproduced its hash; the per-stroke state chain is a full rollback ladder; 0 credits, quoted seven times |
| DECOMPOSE_BY_SECRETS | **3** | Every watch located to a geometry-defined structure; the fifth signature decomposed per structure before it was read; the deep-share given with location; the probe ratio kept separate from the coverage claim |
| UNCERTAINTY_GATED_HUMANS | **3** | Each stroke gated before the next launched; the one genuinely ambiguous reading went to the Director contrastively (both governing texts quoted, recommendation stated, consequences of each option priced) |
| EXTERNAL_VERIFIER | **2** | The watches, the palette gate and the deep-share are code the brush did not write; the 20b read is against the CLAY render, not memory; the anchor checks the tool against its own recorded output. `skip:` on a second model per precedent |

---

## HALT 2 — the stroked asset is staged

**The lane completed as ruled.** The repair landed on the union with all three counts asserted;
the seven strokes ran in the ruled order 180 → 45 → 225 → 315 → 135 → 90 → 270; both edge-on
strokes came back clean on 20b at 4× against the clay; the stone and the repair were never
touched; 0 credits.

**Three things go up for the ruling, none of them mine to decide:** the fifth signature firing on
three strokes (committed and flagged on the Director's word); Ruling 27d's upper bound falsified
at 109.6% of the achievable set with the ratio's sign flipping with context density; and the
unreconciled erode-2 instrument discrepancy between this session and the last.

**The advisor's sheet-walk first, then the Director. Finalize, pack and Gate 1 are the next
dispatch — not this one's.**
