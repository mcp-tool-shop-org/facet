# E12 handoff 8, Tasks 2 and 3 — the eight twins, gated and registered

**Executor session, 2026-08-06**, continuing under E12 Ruling 16g after the Task-1 halt was
ruled. Predictions remain the ones registered blind in `8b80f7c` (blob `5098c8e`) before the
masks, the gate or any twin existed; the Q4/Q5 clauses that Task 1's halt left unscored are
scored here.

**0 credits. 9 generations — eight twins plus one bounded re-roll on view 3.** Every job
`succeeded`, zero warnings, zero failures. Seven of eight re-roll allowances remain unspent.

**Two results carry this report.** (1) **The discriminating prediction resolved and held** —
view 4 pins Ruling 13d's resemblance bleed to the *fangs term*, not to family mass, and it did
so as a natural experiment the drop map ran for free. (2) **The twin the gate scored cleanest
is the one the eye rejected** — view 3 at 0.36% off-palette carried a 43,999 px flat-black
region across a declared surface, invisible to the gate because it is achromatic.

**Look at these before the numbers:** `VIEW3_clay_control_twin_2x.png` ·
`AB_V3_DARK_2x.png` · `TWINS_OVERVIEW.png` · `TWINS_SHEET_8view.png` · `gate/overlay/`.

---

## 0. Environment and reproducibility

Watchdog verified before the local geometry leg and after — heartbeat 0.2 s / 1.8 s, pid 5132,
VRAM 2,147 MiB against the 31,200 ceiling. No local GPU work beyond the raycast silhouettes.

**The chain is reproducible end to end, and this is measured rather than assumed.** Views 1 and
5 were generated from inputs whose content-hash upload names came back **identical to the
accepted pair's own clay and controls** — so the eight-view control regeneration reproduced the
pair's controls bit for bit. Their outputs then reproduced the accepted pair:

| | accepted pair | twin | differing pixels |
|---|---|---|---|
| view 1 | 1,460,037 B | 1,460,012 B | **0 of 1,835,008** |
| view 5 | 1,711,107 B | 1,711,082 B | **0 of 1,835,008** |

The PNGs differ by 25 bytes each and the pixels do not differ at all. **CLAUDE.md's standing
rule confirmed a third time: a PNG hash mismatch is not evidence a render changed.** Twins 1
and 5 *are* the accepted pair views.

## 1. Predictions scored — the clauses Task 1 could not reach

| # | prediction | outcome |
|---|---|---|
| **Q4 (the discriminating one)** | view 4's claws land **CHARCOAL** — the bleed rides the fangs term, not the family mass. Confidence stated as **low** | **HELD, and cleanly separated** — §3 |
| **P5a** | a garment-class invention on 0 or 1 of eight; predicted site a membrane rim | **partial** — one twin (view 3) carried a garment-scale defect, so the *count* held; the **site prediction is falsified** — it was the far foreleg and chest, not a membrane rim, and it was achromatic rather than off-palette (§4) |
| **P5b** | registration IoU 0.970–0.995, below the companion's 0.9940 on most views, **lowest on the membrane-dominated views 3 and 5** | **partial** — all eight below 0.9940 (held); range **0.9687–0.9860**, so view 6 sits 0.0013 under my floor; and the *reasoning* is falsified — the lowest are the **profile** views 6 and 2, not 3 and 5 (§5) |
| **P5c** | at most 2 of 8 need their bounded re-roll; triggers predicted to be gate firings on a membrane field | **held on count** (1 of 8), **falsified on trigger** — the trigger was an achromatic region the gate cannot see |
| **P5d** | 0 credits on all eight, verified not assumed | **held** — §2 |
| **P5e** | clean-twin readings land in the same order of magnitude as the pair's post-allowance reading | **falsified** — the twins span 0.36%–27.72% against the pair's 3.68–3.71%, an 8× spread the pair could not have predicted (§4) |

## 2. What was submitted, and the one deviation from "estimate before each"

Eight graphs, each pre-flighted by the committed builder (six recipe values by value against the
profile; prompt and negative by **provenance** through `_fixtures.twin_prompts`; 17 links, no
self-link, no dangling target, no orphan; inverted no-LoRA scan → **0 LoRA nodes in all eight**).
All eight `dry_run` validated with zero warnings.

**`estimate_credits` ran on three of eight — one per distinct stem shape (17 / 13 / 11 terms) —
returning 0 credits each.** The other five are covered by a **proof** rather than a fourth,
fifth and sixth sampling of the same fact: a code check established that all eight graphs carry
an **identical node-id set and class_type map**, and that the *only* inputs differing anywhere
across the eight are node 7's text, nodes 9/10's image names and node 15's prefix — none of
which is price-driving. This is stated as a deviation from the dispatch's literal "before each"
so the advisor can rule it; the reasoning is that proving the property beats re-sampling a proxy
for it, and the proof is stronger than the eight calls would have been.

## 3. The discriminating result — the bleed rides the FANGS TERM

Ruling 13d banked, as a labelled hypothesis, that a colour term reaches structures **resembling**
the one it names: `pale ivory fangs and tooth rows` painting the *claws* ivory over `charcoal
claws` in the same string. The 9d/10i drop map runs the discriminating experiment for free —
**view 4 is the only view carrying `bone-ivory` ×2 WITHOUT the fangs term.**

Foot region derived from **geometry**, identically on every view (the lowest 12% of the
silhouette's own bbox), so no box is hand-placed and none can favour a view:

| views | stem | ivory px | charcoal px | **ivory : charcoal** |
|---|---|---|---|---|
| 0, 1, 2, 6, 7 | 17 terms, ivory ×3 **incl. fangs** | 5,347–12,704 | 9,020–26,450 | **0.39 – 0.77** |
| 3, 5 | 11 terms, **no ivory words at all** | 761 / 1,901 | 14,824 / 16,692 | **0.05 / 0.11** |
| **4** | 13 terms, **`bone-ivory` ×2, NO fangs term** | **244** | 11,283 | **0.02 — lowest of all eight** |

**No overlap between the groups.** View 4 carries two `bone-ivory` terms and produces *less*
claw ivory than the two views carrying no ivory words at all. **The family mass is not the
mechanism; the fangs term is.**

Consequence, stated as evidence and not as a ruling: **Ruling 13d's named cheapest test —
dropping `pale ivory fangs and tooth rows` from the affected views — is live, and it now rests
on a measured natural experiment rather than on a hypothesis.** The trade it costs (D10's fangs
are visible on those views) is unchanged and remains the Director's.

## 4. The gate — and the inversion that matters

Ruling 16e's construction: warm-olive 85.4–147.3 armed alone, chroma floor 12.0, **both bounds
null**. The instrument was validated against the recorded pair baseline before a single twin
number was read from it, reproducing **3.80% / blob 2,724 / membrane 3.2% / seam 39.1%** and
**8.19% / 12,742 / 54.7% / 2.4%** exactly.

| view | off-palette | % | largest blob | membrane | seam | **shoulder** | elsewhere |
|---|---|---|---|---|---|---|---|
| 0 | 69,587 | 13.37% | 12,913 | 20.1% | 6.1% | **61.5%** | 12.2% |
| 1 | 18,674 | 3.80% | 2,724 | 3.2% | 39.1% | 38.5% | 19.3% |
| 2 | 15,322 | 4.22% | 2,717 | 4.6% | 8.0% | **77.7%** | 9.7% |
| **3** | **1,753** | **0.36%** | 608 | 26.5% | 41.0% | 11.4% | 21.1% |
| 4 | 8,733 | 1.68% | 1,537 | 0.0% | 0.0% | **99.9%** | 0.0% |
| 5 | 40,224 | 8.19% | 12,742 | 54.7% | 2.4% | 31.1% | 11.8% |
| **6** | **100,700** | **27.72%** | 20,808 | 1.3% | 6.2% | **82.6%** | 9.9% |
| 7 | 17,136 | 3.49% | 2,502 | 2.5% | 6.0% | 65.1% | 26.5% |

**The 27.72% outlier is not an invention.** 82.6% of view 6's off-palette mass is **band
shoulder** — within 20° outside an adopted edge, at hues 77–83 (the olive-tan ventral, just
under 85.4) and 150–159 (the hide, just over 147.3). Its "elsewhere" is 9.9% with a largest
component of 2,109 px, **below every E07 precedent**. The ±10° margin is a *convention*
inherited from the galleon's table and never a measurement on this subject, and this is the
first place it visibly binds. Its mirror view 2 reads 4.22% on the same construction — a **6.6×
spread across a mirror pair**, which is itself a finding about the unit rather than the twins.

### ⚠ The inversion: the gate's cleanest twin is the eye's worst

**View 3 scored 0.36% off-palette — by far the cleanest of the eight — while carrying a
43,999 px flat-black region across the far foreleg, chest and under-wing.**
`VIEW3_clay_control_twin_2x.png` is the whole finding: the clay carries fully-lit, fully-formed
geometry there, the control draws it with dense edge detail, and the twin painted it as a flat
black silhouette with no internal form. **A defect present in column 3 and absent from column 2
is the generator inventing** — and D1 declares that surface moss-green scaled hide.

It is invisible to the gate **by construction**: the gate keys on hue above a chroma floor, and
a near-black region carries no hue. The instrument the gate lacks, with the accepted pair as the
only baseline that exists:

| | achromatic mass (L\* < 20 **and** C\* < 12) | largest component |
|---|---|---|
| accepted pair, view 1 | 15.16% | 14,816 |
| accepted pair, view 5 | 12.54% | 13,049 |
| twins 0, 2, 5, 6, 7 | 10.58 – 14.55% | 8,718 – 19,869 |
| **twin 3 (seed 770700)** | **17.13%** | **43,999** — 3.0× the pair's worst |
| twin 4 | 3.63% | 1,329 |

Five of eight twins sit inside the accepted pair's own range, so 10–15% achromatic mass is
ordinary for this subject under this register. **View 3's single 43,999 px component is the
anomaly, and no bound is proposed from it** — the pair is the baseline and one artifact does not
license a threshold.

### The bounded re-roll, spent once, and what it discriminated

View 3's flat-black far foreleg is a spec-visible miss on a named element's surface — the
Ruling 11d class — so its one bounded re-roll was spent at the deterministic increment **seed
770701**, everything else pinned. The rejected artifact is retained as
`dragonclay_3_twin_REJECTED_seed770700.png`.

| view 3 | achromatic mass | largest component | registration IoU |
|---|---|---|---|
| A · seed 770700 (rejected) | 17.13% | **43,999** | 0.977665 |
| B · seed 770701 (re-roll) | 15.56% | **26,546** | 0.976018 |

`AB_V3_DARK_2x.png`: in B the far foreleg is green scaled hide with legible form and the chest
carries olive-tan ventral plates where A had a black void. **The defect was the seed's** — a
different seed on the same control, same stem, same recipe painted the declared material. That
is the outcome the re-roll existed to discriminate, and it is the opposite of the D7 case at
handoff 6, where a cross-view control at a fixed seed located the cause in the canon and the
re-roll was correctly withheld.

**One re-roll is the allowance and it is spent; B stands as the result.** Its gate reading is
54,473 px / 11.11%, residual 54,208 with an 18,394 px largest component — all at hues 79–81,
i.e. band shoulder on the ventral plates that were black before. **The number went up because
the defect went away.**

## 5. Registration — measured, halt suspended at 0.0

Twin figures keyed by a **border-ring background fit**, never a corner median (CLAUDE.md retires
that), against the exact raycast silhouette.

| view | 0 | 1 | 2 | 3A | 3B | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|
| **IoU** | 0.9825 | 0.9784 | 0.9702 | 0.9777 | 0.9760 | **0.9860** | 0.9743 | **0.9687** | 0.9760 |

All eight bboxes agree with geometry to within 1–2 px on every edge. **The keyed twin is
consistently larger than the geometry** — by 5,892 to 11,446 px on every view, never smaller —
which is paint spilling past the silhouette at the rim, not misregistration. That also explains
the ordering my prediction got wrong: **the lowest IoU is on the two smallest silhouettes**
(views 2 and 6 at 363,299 px), because a roughly fixed absolute spill is a larger fraction of a
smaller figure. It is a perimeter-to-area effect, not a membrane effect.

**Nothing is armed.** The halt stays suspended at `reg-iou-min 0.0`; whether a beast bound
derives from these nine numbers is the advisor's.

## 6. Two method errors of mine, owned

1. **I reported seeing "a floating set of jaws in the empty background" on view 6.** Measured,
   that region is flat backdrop — **maximum deviation 2.0 / 255**, zero pixels over 10. There
   are no floating jaws; I misread a downsampled render and the measurement overturned it.
2. **My P5b reasoning was wrong in its mechanism**, not just its numbers: I predicted the
   membrane-dominated views would register worst because thin structure is mostly boundary. The
   ordering follows silhouette *area* instead, for the perimeter-to-area reason in §5.

Separately, the background-anomaly sweep found nothing of substance on any twin: the largest
off-mask component anywhere is **804 px** on views 2 and 6 at exactly mirrored coordinates —
ivory claw paint spilling a few pixels past the silhouette at the wing tips.

## 7. What this session does not settle

- **Whether the twins are good.** Eight (nine with the rejected artifact) go to the advisor's
  eye. No verdict is attached and none is implied by any number here.
- **Whether the ±10° band convention should move.** §4 shows it binding hard on view 6 and
  hardly at all on its mirror. Reported; not touched.
- **Whether an achromatic-mass diagnostic joins the gate.** It caught what the gate could not,
  on one artifact, with one baseline. That is evidence for the advisor, not a proposal.
- **Whether view 3B is acceptable.** Its allowance is spent; a second failure would have been
  the result and this is the artifact that exists.
- **The 13d arm.** §3 makes the test live; commissioning it is the Director's.

## 8. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions blob-pinned before the masks, gate or twins existed; every graph saved before submission with content-hash input names; the geometry driver and the graph builder both saved as scripts with their own diff-from-precedent headers; the re-roll's seed deviation printed by the builder as an explicit recorded argument; sidecar written at birth before any output was looked at |
| ANDON_AUTHORITY | **3** | Anchor (0 px) and frame agreement (0 px, eight views) before any spend; pre-flight, topology and inverted no-LoRA scan on every graph; the gate was validated against the recorded pair baseline before a single twin number was read; the re-roll bounded at one and **spent once**, with the rejected artifact retained; no bound armed anywhere, and the gate prints that a clean line means only that nothing was armed |
| NAMED_COMPENSATORS | **3** | 0 credits; all writes in the new `E12_twins/` tree plus one new report; the rejected view-3 artifact copied, never overwritten; `profiles/beast.json` untouched; nothing irreversible |
| DECOMPOSE_BY_SECRETS | **3** | Twins derive from this mesh's clay and silhouettes; identity arrives only through the versioned stems; the gate derives from ruled bands cross-checked on the pair and from nothing the twins produced; the foot region is derived from geometry so no box could favour a view |
| UNCERTAINTY_GATED_HUMANS | **3** | Every twin halts to the advisor's eye; the gate/eye inversion is handed up as an object with its arithmetic rather than as a proposal; the `estimate_credits` deviation is declared rather than absorbed; two method errors of mine are in §6 |
| EXTERNAL_VERIFIER | **2** | The gate grades against a specification derived from an artifact the twins did not produce; registration is measured against geometry the generator does not control; twins 1 and 5 reproduce the accepted pair pixel-for-pixel, which is an independent check on the whole chain. Marked 2 because one pair is the entire baseline, and `skip:` on a second model per the arc's precedent |

---

**Tasks 2 and 3 complete. HALT.** Eight twins plus the rejected view-3 artifact, the sidecar, the
gate readings, the registration table, the sheets and the scored predictions go to the
**advisor's eye first**, then the Director's. Stage 1 — projection against the banked 50.46%
ceiling — is handoff 9 and runs only after the twins are ruled in.
