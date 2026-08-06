# E12 handoff 11 — the exemplar rebuild (v8, all eight) and E13 Gate 0

**Executor session, 2026-08-06.** Predictions registered blind in `4723129`
([E12-handoff11-predictions.md](E12-handoff11-predictions.md)), git blob `427182f3`, written
before the v8 rebuild, before the nape check, before any v8 artifact existed and before
`project_twins.py` was touched.

**0 credits. 10 generations — eight twins plus two bounded re-rolls.** Every job `succeeded`,
zero failures, zero warnings. Six re-roll allowances remain unspent. Watchdog alive before the
local legs (heartbeat 2 s, VRAM 1,884 MiB against the 31,200 ceiling) — no Blender ran; the
local work is raycast and image measurement.

**Three results carry this report.**

1. **E13 Gate 0 PASSES at exactly 0 differing pixels**, in two directions, on five artifacts.
   E13 is unblocked at zero spend.
2. **Ruling 20a's seed-binding phenomenon reproduced, and it is not specific to one term.** On
   view 4, seed 770700 left the finger struts cream for a **fourth** stem, and 770701 bound them
   again (whole-figure pale 83,353 → 29,352 px, reproducing handoff 10's 67,713 → 30,326 on a
   different stem version). At the same seed the *neck-spine* term also binds far harder
   (nape charcoal 12.75% → 41.86%). One seed resists two different terms on one view.
3. **The set moved coherently in the declared direction and my eye was wrong about why.** I read
   view 1's limbs as "gone charcoal-black, a regression". Measured, the charcoal **area** in that
   view's limb band *fell* 54.81% → 40.59% with the largest component down 75,589 → 25,702. What
   changed is chroma, not area: the dark went neutral (C\* 9.3 → 4.0). §6 owns it.

**Look at these before the numbers:** `SHEET_v8_clay_control_twin.png` (eight rows, clay |
control | twin, full size — the artifact the acceptance rules on) · `ab_v4r/AB_wings_and_nape_2x.png`
· `ab_v3r/AB_shoulder_and_limbs_2x.png` · `ab_v1/AB_head_3x.png`.

---

## 0. Environment and the one input check that matters

All **sixteen** reused inputs — eight clay renders, eight controls — were re-uploaded and every
one returned handoff 8's recorded content-hash name. Geometry did not change, so this is the
check that nothing moved rather than the assumption that nothing did. **P2h held in full**;
`estimate_credits` returned 0 on each distinct stem shape.

## 1. Task 1 — the v8 stems, and the drop map verified rather than assumed

Entry **19 → 20 terms**; `charcoal neck spines` at index 8. The exact-delta ANDON is a
**committed tool** this time ([`e12_stem_delta.py`](../../tools/diagnostics/e12_stem_delta.py))
rather than the throwaway scripts handoffs 9 and 10 used, and it reads v7 out of **git**, not out
of a working copy this session wrote. It passed on all nine stems with no
`--allow-dropmap-change`: strip the one term and what remains is byte-equal to v7.

Per-view counts **20 / 20 / 20 / 14 / 16 / 14 / 20 / 20**, companion **18** — exactly P1b.

**P1c is the one that needed work.** The new term names the nape crest, and views 3 and 5 hide
the whole head behind the near wing (Ruling 10i). A second committed tool
([`e12_region_crops.py`](../../tools/diagnostics/e12_region_crops.py)) carries a world box into
the render frame by the route's own arithmetic, narrows it to a midline up-facing ridge, and
emits both a number and a crop:

| view | 0 | 1 | 2 | **3** | 4 | **5** | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| nape crest first-hit, % of figure | 0.611 | 0.982 | 1.897 | **0.627** | 2.280 | **0.638** | 1.930 | 1.007 |

**The control settles it.** D6's *other* term — `charcoal dorsal and tail spines`, which has
ridden all eight views since v1 — measures **0.043% on view 0**, fourteen times below the nape's
own floor. By the standard this element is already accepted under, the crest clears everywhere.
Confirmed by eye at 3×: on views 3 and 5 a nape spike stands clear above the near wing and the
shoulder-end row is open. **No drop added; P1c held.**

**P1d held and is reported, not decided:** `headclay_0`'s recorded drop list does not name the
new term, so the companion keeps it — which gives the shoulder-end crest at that frame's bottom
edge a declared colour for the first time and closes the standing `_companion_rationale_VOID`
flag as a side effect of the deletion construction. Not submitted.

## 2. Task 3 — E13 Gate 0, run first because it blocks E13

Run in **two** directions against the recorded eight-camera projection, whose five artifacts are
byte-identical to each other:

| anchor | atlas | `_holes` | `_blend` | `_styled_mask` | `_owner` |
|---|---|---|---|---|---|
| **baseline** — unmodified HEAD, *before* the change | 0 | 0 | 0 | 0 | 0 |
| **A** — extended tool, default path | 0 | 0 | 0 | 0 | 0 |
| **B** — extended tool, **new parameter path**, all three overrides passed explicitly at full-figure values on all eight views | **0** | **0** | **0** | **0** | **0** |

0 of 16,777,216 elements differing on each, and byte-identical besides. **P3a, P3b and P3c all
held.** Anchor B is the one the dispatch asks for — A alone would only prove the refactor is
inert on the branch that hands back the globals untouched. Nothing was projected (P3d).

`--crop-aspect` is a **third** parameter beyond the two the spec names, declared rather than
smuggled: the measured head-crop companion is 1360×1360 against a 1792×1024 route frame, so
ortho-scale and centre alone cannot express a crop camera. Default = the global `--aspect`.

## 3. Task 2 — the palette gate, against the recorded baselines

| view | figure px | off-palette | % | largest blob | membrane | seam | residual | res-blob | **baseline %** |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 520,644 | 116,862 | **22.45%** | 23,778 | 4.8% | 0.4% | 110,895 | 23,778 | 13.37 |
| 1 | 490,941 | 45,057 | **9.18%** | 9,445 | 6.1% | 12.4% | 36,722 | 8,912 | 3.80 |
| 2 | 363,299 | 22,185 | **6.11%** | 2,692 | 4.5% | 4.3% | 20,225 | 2,692 | 4.22 |
| 3 | 490,436 | 4,383 | **0.89%** | 694 | 4.1% | 37.4% | 2,566 | 602 | 0.36 |
| 4 | 520,644 | 30,351 | **5.83%** | 2,089 | 0.2% | 0.0% | 30,300 | 2,089 | 1.68 |
| 5 | 490,941 | 16,687 | **3.40%** | 3,487 | 49.4% | 5.0% | 7,597 | 786 | 8.19 |
| 6 | 363,299 | 82,397 | **22.68%** | 23,757 | 2.2% | 5.6% | 75,962 | 23,757 | 27.72 |
| 7 | 490,437 | 23,649 | **4.82%** | 2,716 | 6.3% | 3.7% | 21,286 | 2,716 | 3.49 |

**P2d held on three clauses and is falsified on the fourth.** Six of eight rose (predicted ≥ 5);
view 6 stays above 20% (22.68%); the median of the eight is **5.97%**, inside my 4–12%. The
residual largest component sits below the E07 precedents on **5** of 8 — I predicted at least 6.
**No bound is armed; nothing here passed or failed.**

## 4. The channels the gate is blind to

Both measured by a third committed tool
([`e12_twin_readout.py`](../../tools/diagnostics/e12_twin_readout.py)), for the same reason —
handoffs 8, 9 and 10 each measured these with scripts nobody kept.

| view | achromatic % | largest CC | reg IoU | twin bbox | mesh bbox | key |
|---|---|---|---|---|---|---|
| 0 | 11.89 | 15,185 | 0.957898 | 1485×857 | 1487×853 | flat |
| 1 | 14.17 | 13,909 | 0.961780 | 1371×848 | 1377×853 | flat |
| 2 | 14.38 | 12,784 | 0.957369 | 1481×845 | 1485×853 | flat |
| **3** | 15.61 | **41,985** | 0.967117 | 1307×847 | 1313×853 | flat |
| 4 | 4.48 | 2,689 | 0.970228 | 1484×849 | 1487×853 | flat |
| 5 | 7.40 | 7,730 | 0.966620 | 1371×850 | 1377×853 | flat |
| 6 | 11.56 | 16,928 | **0.953767** | 1481×851 | 1485×853 | flat |
| 7 | 9.98 | 20,691 | 0.969088 | 1308×849 | 1313×853 | flat |

Accepted-pair baseline: 15.16% / CC 14,816 and 12.54% / CC 13,049. **P2e held on the range and
on view 4 as the low outlier; the < 25,000 CC clause held on 7 of 8** — view 3's 41,985 is the
exception and it is §5.

**P2f: registration 0.953767–0.970228 — falsified by 0.0012 at the bottom.** I predicted
0.955–0.990 and view 6 sits just under. The separate clause held: **0 of the eight base twins
paints a graded backdrop**; every key is flat and every IoU usable. (One re-roll does — §5.)

**P2g held.** Views 1 and 5 no longer reproduce the accepted pair; whole-figure pale alone moves
37,450 → 16,722 and 37,736 → 22,983 px. The directive working, not a defect.

## 5. The two bounded re-rolls, and what each one traded

**View 3 — spent, and it reproduces handoff 8 exactly.** The 770700 twin carries a **41,985 px
flat-black region** across the far foreleg and the shoulder under the near wing, on a surface D1
declares moss-green. Handoff 8 measured **43,999 px** on this same view at this same seed under
the *v5* stems and cured it at 770701. Two stem versions, one seed, same defect: the canon
explanation is disfavoured because 770701 has now produced a clean limb twice.

| view 3 | achromatic | largest CC | nape charcoal | whole-figure pale |
|---|---|---|---|---|
| A · 770700 (retained) | 15.61% | **41,985** | 5.92% | 3,955 px |
| B · 770701 | 14.53% | **28,057** | 16.97% | 2,699 px |

At 2× the far foreleg is green scaled hide with legible form where A was a black void.

**View 4 — spent, and the trade is not small.** Cream finger struts on a moss-green-declared
surface, the **fourth** stem at 770700 to leave them cream.

| view 4 | whole-figure pale | nape charcoal | achromatic | largest CC | backdrop |
|---|---|---|---|---|---|
| A · 770700 (retained) | 83,353 px (16.01%) | 12.75% / CC 2,264 | 4.48% | 2,689 | flat |
| B · 770701 | **29,352 px (5.64%)** | **41.86%** / CC 14,778 | 11.42% | 8,417 | **GRADED** |

**A swap is not a gain until you have looked at what left.** At 2× (`ab_v4r/AB_wings_and_nape_2x.png`)
A's nape is a row of **discrete charcoal cones** matching the clay's modelled spikes; B's is a
**broad continuous grey vertebral slab**. The charcoal number rose 3.3× and the structure got
mushier — which is the Director's own Ruling 20 sentence pointing the other way. B's backdrop is
graded (ring rgb(151,148,172) against background rgb(158,156,182)), the handoff-10 hazard
reproducing on this same view at this same seed; its bbox did **not** blow out (1485×849 against
1487×853) so IoU 0.977549 is usable, but a graded backdrop is a projection keying hazard.

**Which view-4 artifact stands is not decided here.** A is spec-correct at the nape and
spec-wrong at the struts; B is the reverse.

**P2c held on count** (2 of 8, predicted 1–3) **and on one of its two named views** — view 4 was
named near-certain and spent; view 3 I predicted at ≈60/40 *not* to recur, and it recurred.

## 6. Two errors of mine, both caught by measurement

1. **I read view 1's limbs as "gone charcoal-black — a regression".** Measured on a
   geometry-derived limb band (lowest 35% of each view's own silhouette bbox, same rule
   everywhere), the charcoal **area** *fell*: 54.81% → 40.59%, largest component 75,589 →
   25,702. Across the eight the area fell on 5 views and rose on 3. What actually changed is
   **chroma** — the median C\* inside the dark family fell on 6 of 8 views (view 1: 9.3 → 4.0).
   The dark went neutral rather than growing. My eye read "more black" from a chroma change and
   called it an area change.
2. **I thought view 6 carried a floating set of jaws in the empty background.** The off-mask
   sweep gives a largest off-figure component of **450 px** at [1025,485,1048,516] — beside the
   figure, not out in the field — and the crop at 3× is flat backdrop.
   **This is the identical false positive a previous executor made on this exact view**
   (handoff 8 §6). Twice now, same view, same illusion: worth the record.

One real off-mask finding survives: **view 0 paints a ground shadow**, an 11,526 px component at
[651,901,1295,948] below the feet. The trust intersection handles it; flagged for projection.

## 7. What the terms did, measured

Nape crest region, pale and charcoal, v8 against each view's predecessor. **View 4 is the only
clean single-term attribution in the set** (its predecessor v7-at-770700 differs by the neck term
alone) and it presents the nape best of the eight (2.280% first-hit):

| view 4 nape | pale | charcoal |
|---|---|---|
| v7 @ 770700 | 28.64% | 9.29% |
| **v8 @ 770700** | 28.82% | **12.75%** |

Pale flat, charcoal **+37% relative**, from the one inserted term. Views 0 and 7 move the same
way (charcoal +13.1 and +4.7 points, pale −7.6 and −9.8). Views 1, 2 and 6 move the other way —
**and their attribution is confounded**: they gained *three* terms against their v5 predecessors,
not one. Views 3 and 5 are unreadable on this channel because the nape rect there is mostly wing.

Whole-figure pale fell on 7 of 8 views (−17% to −83%); view 4 is flat at −0.6%, which is the
struts refusing to convert at 770700.

## 8. What this session does not settle

- **Whether any twin is good.** Ten artifacts go to the advisor's eye, then the Director's. No
  verdict is attached and none is implied by any number here.
- **Which view-4 artifact stands.** §5.
- **Whether the crown is landing.** D5 declares bone-ivory crown and cheek spikes; on views 0, 1
  and 2 the frill reads charcoal at 3×, and it read charcoal at v5 too — this is Ruling 18g's
  open question, now with the head-box pale mass falling on 7 of 8 views. Reported, not acted on.
- **Whether the membranes are landing.** D3 declares storm-grey; they read warm tan or
  yellow-green on most views. Standing, unmeasured against a bound, flagged.
- **Whether three charcoal terms are now too many.** The chroma finding in §6 is the mirror shape
  of Ruling 12e's five pale-bone terms. One session's measurement is not a canon change.
- **Whether the ±10° band convention should move.** Views 0 and 6 are shoulder-dominated again.

## 9. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions blob-pinned before the rebuild, the nape check and the tool edit; all ten graphs written to disk before submission with content-hash input names; the re-roll seeds printed by the builder as recorded deviations; the builder invocation saved as `build_v8.ps1` with its diff-from-v7 header; sidecar written at birth before any output was looked at; the Gate 0 anchor pins the tool extension to a recorded projection |
| ANDON_AUTHORITY | **3** | Gate 0 run in two directions **before** any crop projection was contemplated, and the baseline established before the change rather than after; the stem ANDON asserted as construction on nine stems against git; pre-flight, topology and inverted no-LoRA scan on every graph; the bbox/grading check flagged view 4's re-roll backdrop; the eye was deputised past the instruments and did flag past them — in both directions, including twice at its own expense (§6) |
| NAMED_COMPENSATORS | **3** | 0 credits; every write under a NEW `E13_twins/` tree; both 770700 artifacts retained beside their re-rolls; the E12 measurement-record twins, the accepted pair and E10/E11 untouched; the tool extension is additive with defaults preserving old behaviour, **proven** by the anchor rather than asserted |
| DECOMPOSE_BY_SECRETS | **3** | The occupancy-complete entry is v8's single source and reaches the run only through the committed builder; capability (crop cameras) separated from policy (which crops) and from generation; the drop-map decision rests on a geometry measurement with its own control, not on the term it would justify |
| UNCERTAINTY_GATED_HUMANS | **3** | Every artifact halts to the advisor's eye; both re-rolls stated with their grounds and their trades so they can be overruled; view 4's swap is presented as a swap and not banked as a gain; the `dry_run`/`estimate_credits` sampling deviation is declared rather than absorbed |
| EXTERNAL_VERIFIER | **2** | The anchor tests new code against output the old path produced; registration is measured against geometry the generator does not control; twins judged against a specification written before they existed. Marked 2 because the achromatic channel still has one pair as its entire baseline, and `skip:` on a second model per the arc's precedent |

---

**Tasks 1–3 complete. HALT.** The eight v8 twins, the two re-rolls and both retained 770700
artifacts, the sidecar, the eight-row clay | control | twin sheet, the A|B sheets and crops, the
gate / achromatic / registration / family tables, the Gate 0 anchor evidence and the scored
predictions go to the **advisor's eye first**, then the Director's — whose bar is the exemplar
bar. E13 is unblocked at zero spend: Gate 0 passed, and nothing has been projected.
