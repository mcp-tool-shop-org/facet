# E14 handoff 7 — the STROKE LANE, Task 1: the derivation. HALT 1.

**Executor session, 2026-08-08.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 23b.
Predictions committed blind in `a75d5cf`, before any probe ran. *(Corrected in place: this
line first read `c04a629`, the hash the predictions carried in my working tree. The advisor's
relief fold landed between the two commits and the rebase moved mine; `c04a629` is now the
relief commit, so the original line pointed at the wrong object. Ruling 24's evidence line
cites `a75d5cf`, which is the correct one.)*

**Nothing is adopted here. Nothing generated, no credits, no profile edit** — Task 1 is
raycast, write-head probes and derivation. `texpass_brush`'s `_NOT_CLEARED` block is
untouched; the ruling clears it.

**The headline is not the stroke set.** It is that the banked "brush territory" of 210,907
texels is a *ceiling* number and the write-head's own achievable set is **69,239** — a third
instance of Ruling 22b's law, now measured at the brush — and that the spiral order and the
coverage order point at **opposite ends of the subject**.

---

## 1. The instrument, and why it is the tool rather than a model of the tool

Every coverage figure below comes from `texpass_iter selftest`: emit → fake-inpaint by
Gaussian blur → commit. It runs the **real write-head** at the real profile values and
prints exactly how many texels a stroke at that camera would write, with **no generation and
no spend**. It also exercises the invariance ANDON on every probe: *46 probe runs, 46
`styled-texel max delta 0.000000`, 46 PASS.* Nothing in this session is a re-implementation
of commit — my own pre-registered caution was that quoting a reach number as a stroke's
coverage would be last session's error repeating, and `selftest` is the instrument that
makes that impossible.

All probes write into throwaway directories under `E14_strokes/probe/`. `state0/` is a copy
of stage 1b and was never written to.

## 2. ⚠ WHAT THE WRITE-HEAD CAN ACTUALLY DO — the third reach-vs-paint instance

### 2a. The eight-camera union

| population | texels | points of valid |
|---|---|---|
| holes in stage 1b | 2,005,056 | 54.75 |
| **banked "brush territory"** — hole ∧ ceiling-reach at facing **0.45** | **210,907** | 5.759 |
| **write-head achievable** — commit's own chain at facing **0.25**, eight cameras | **69,239** | **1.891** |
| — BOTH: territory the strokes can actually close | 37,271 | 1.018 |
| — territory ONLY: the ceiling reaches it, commit cannot write it | **173,636** | 4.742 |
| — achievable ONLY: commit writes it, the ceiling's floor excludes it | 31,968 | 0.873 |

**Neither set contains the other, and that is the first thing to say.** The territory was
computed at the ceiling's 0.45 facing floor; commit accepts at 0.25. My first draft of this
table printed "closable / territory" per structure and returned **934.9% on the collar** and
185.5% on the crossing — a percentage over 100 of a supposed subset is the denominator
telling you it is not one. Corrected before any number left the script; the partition above
is what replaced it. Fifth moving-denominator instance in this repo, caught by one
impossible percentage, which is what the check is for.

**The strokes close 17.67% of the banked territory** and reach 31,968 texels outside it.

### 2b. Per structure

| structure | holes | territory (0.45) | achievable (0.25) | BOTH | achievable outside territory | % of its territory closable |
|---|---|---|---|---|---|---|
| L5 the stone | 90,365 | 5,581 | 2,694 | 2,499 | 195 | 44.8% |
| L3 pommel collar | 41,649 | 315 | 2,945 | 315 | 2,630 | 100.0% |
| L4 grip wrap + mid ring | 111,788 | 4,219 | 3,486 | 182 | 3,304 | **4.3%** |
| L2/L3 the CROSSING | 284,357 | 14,420 | 26,748 | 6,414 | 20,334 | 44.5% |
| **L1 the blade** | 1,476,897 | **186,372** | 33,366 | 27,861 | 5,505 | **14.9%** |

**The blade — 88.4% of the paint loss and the reason this lane exists — is where the write
head can reach least.** Its territory is 186,372 and the strokes close 27,861 of it.

### 2c. Commit's funnel, and which stage binds

Every stage counted in commit's own order, on the hole set, per camera:

| yaw | facing > 0.25 | visible | in dilated job mask | edge-dist ≥ 4 = **committed** |
|---|---|---|---|---|
| 0 | 882,587 | 111,442 | 43,987 | 7,591 |
| 45 | 782,552 | 85,679 | 42,426 | 10,539 |
| 90 | 686,840 | 33,829 | 28,245 | 14,211 |
| 135 | 767,536 | 57,124 | 43,389 | 7,728 |
| 180 | 878,542 | 100,210 | 44,546 | 6,559 |
| 225 | 829,820 | 125,947 | 46,454 | 8,600 |
| **270** | 783,024 | 124,062 | 66,235 | **27,010** |
| 315 | 854,868 | 136,369 | 59,709 | 9,633 |

Two large losses, and neither is facing. **visible → in-job-mask** roughly halves the set:
`vis` is cast with `bias 3e-3` against walls measured at ~0.00196 (Ruling 10b), so the ray
origin is displaced through its own wall and inner/far-wall texels are called visible while
the frame pixel's first hit is the near wall. **in-job-mask → edge-dist ≥ 4** removes another
59% at yaw 270.

**Frame resolution is falsified as the lever, by measurement.** The obvious hypothesis was
that a 240×1024 job frame cannot address a 4096² atlas. Swept at yaw 270, all
generator-legal and aspect-exact:

| job frame | figure px | hole px | committed |
|---|---|---|---|
| 240 × 1024 | 24,153 | 10,489 | 27,010 |
| 480 × 2048 | 96,921 | 27,287 | 27,612 |
| 720 × 3072 | 217,907 | 49,976 | 28,504 |
| 960 × 4096 | 387,567 | 78,218 | 28,196 |

**16× the pixels buys 4.4%, and the curve turns over.** The frame is not the constraint. The
hypothesis is recorded as falsified rather than dropped.

### 2d. ⚠ The two write-head values that ARE the lever — and they are first-run operating points

`prop.json` marks `texpass_iter`'s `edge-dist 4.0`, `mask-dilate 9` and `facing-min 0.25` as
*"FIRST-RUN OPERATING POINT at the code default; stage 2 has not run on this subject."* They
are what binds. Swept at yaw 270:

| edge-dist | committed | | mask-dilate | committed | | facing-min | committed |
|---|---|---|---|---|---|---|---|
| 0 | **66,235** | | 5 | 21,963 | | 0.10 | 28,708 |
| 1 | 32,318 | | 9 | 27,010 | | 0.18 | 27,965 |
| 2 | 30,760 | | 15 | 31,305 | | 0.25 | 27,010 |
| 3 | 29,104 | | 25 | 33,766 | | 0.45 | 23,238 |
| 4 | 27,010 | | | | | | |
| 6 | 22,384 | | | | | | |

**The cliff is between 0 and 1: requiring any distance at all from the brush's keyed figure
boundary costs 33,917 texels — 51% of the candidates.** On a blade that is ~15 px wide at
this camera, essentially every candidate texel is boundary.

**This is the A3 fix's missing consumer.** `project_twins` had exactly this defect and it was
repaired: a global pixel peel became `min(2.5 px, ⅓ × local half-width)`, because *the cost
of a fixed peel runs inversely with local feature width*. **`texpass_iter`'s commit still
carries the global constant.** CLAUDE.md's *when you fix a root cause, find its other
consumers* — this is the other consumer, found four experiments late. **I have not touched
it.** Reported for the ruling.

An alternative parameter set, run as a full eight-camera chain to price it:

| | eight-camera union |
|---|---|
| profile first-run values (edge-dist 4, mask-dilate 9) | **68,814** |
| edge-dist 1 + mask-dilate 15 | **111,044** (+61%) |

## 3. The candidate cameras, the greedy ladder, and the spiral tension

### 3a. The greedy, on committed texels

| step | camera | marginal committed | cumulative | % of the achievable set |
|---|---|---|---|---|
| 1 | **yaw 270** | **27,010** | 27,010 | 39.3% |
| 2 | **yaw 90** | 14,211 | 41,221 | 59.9% |
| 3 | yaw 45 | 9,560 | 50,781 | 73.8% |
| 4 | yaw 225 | 8,115 | 58,896 | 85.6% |
| 5 | yaw 315 | 4,137 | 63,033 | 91.6% |
| 6 | yaw 135 | 3,789 | 66,822 | 97.1% |
| 7 | yaw 0 | 1,160 | 67,982 | 98.8% |
| 8 | yaw 180 | 832 | 68,814 | 100% |

*(Ordering caveat, stated rather than hidden: steps 4–8 were chained on the round-3 ranking
rather than re-probed at every step, so the individual marginals after step 3 are chain
values. The union is order-independent and is the number that matters. One measured
non-monotonicity: yaw 180 read 6,559 standalone and 6,561 after yaw 270 — +2 texels, from
the previously-committed paint shifting the keyed figure's distance transform at the
boundary. A diagnostic, not a halt.)*

**The two edge-on cameras are 60% of the lane.** Neither has a twin — view 2 excluded at
Ruling 18c, view 6 at Ruling 20a — and Ruling 20b put exactly these surfaces in the brush's
territory by construction. The lane is the shape that ruling predicted.

### 3b. ⚠ The spiral order and the coverage order point opposite ways

The composes-a-new-character law makes painted adjacency a correctness constraint:

| yaw | figure px | hole px | **painted %** | committed | job-mask components | largest |
|---|---|---|---|---|---|---|
| 0 | 49,775 | 8,742 | **82.4%** | 7,591 | 15 | 26.6% |
| 180 | 49,775 | 9,500 | 80.9% | 6,559 | 21 | 22.6% |
| 225 | 40,101 | 10,090 | 74.8% | 8,600 | 17 | 47.2% |
| 45 | 40,101 | 10,422 | 74.0% | 10,539 | 16 | 44.3% |
| 315 | 40,331 | 10,783 | 73.3% | 9,633 | 16 | 45.7% |
| 135 | 40,331 | 10,869 | 73.0% | 7,728 | 14 | 46.6% |
| 90 | 24,153 | 10,081 | 58.3% | 14,211 | 5 | 55.6% |
| **270** | 24,153 | 10,489 | **56.6%** | **27,010** | 7 | **55.6%** |

**The camera that commits the most has the least painted context, and the two that have the
most context commit the least.** yaw 270 commits 3.6× yaw 0 at 26 points less adjacency. The
spiral law says anchor at yaw 0; the coverage says the lane lives at yaw 270. **I am not
resolving that — it is the ruling's.** What I can add is that every candidate frame is above
55% painted, which is a constraint the twins never had (they opened onto bare clay), and
that the yaw-270 job mask is a *single connected ribbon* — 55.6% of that frame's hole pixels
in one component, 90.2% in three — so the brush is not being opened onto scattered speckle.

### 3c. Component structure — atlas space is unusable, and that was worth measuring

| | banked territory, atlas space |
|---|---|
| connected components | **57,332** |
| largest | 1,302 texels = **0.62%** of the set |
| top 10 / top 100 | 3.8% / 11.0% |
| median component | **1 texel** |
| components under 10 texels | 54,566 = 95.2% of components, 56.1% of the set |

The 46,496 UV islands shatter every surface-continuous structure. **Atlas-space components
cannot order a stroke lane**; camera space is the only frame that means anything here.

## 4. thin_extent — the 10d curve, now measured at the brush

Ruling 10d deferred the value to this ruling because *the withheld fraction inverts by view
and no pooled number can judge a candidate on this subject.* The mechanism is the plate:
**ray extent through the blade is its thickness (~0.021) face-on and its width (~0.15–0.2)
edge-on.** Measured at both ends, on committed texels rather than on withheld pixels:

| thin_extent | yaw 270 withheld px | yaw 270 committed | cost | yaw 0 withheld px | yaw 0 committed | cost |
|---|---|---|---|---|---|---|
| 0.0 (off, current) | — | 27,010 | — | — | 7,591 | — |
| 0.005 | 464 (1.9%) | 26,941 | **−0.3%** | 812 (1.6%) | 6,637 | **−12.6%** |
| 0.0075 | 707 (2.9%) | 26,941 | −0.3% | 1,810 (3.6%) | 5,212 | −31.3% |
| 0.01 | 981 (4.1%) | 26,929 | −0.3% | 3,475 (7.0%) | 4,602 | **−39.4%** |
| 0.021 (the blade's own) | 2,721 (11.3%) | 26,476 | −2.0% | 23,715 (47.6%) | 1,356 | **−82.1%** |
| 0.03 (the character's) | 5,757 (23.8%) | 25,154 | −6.9% | 39,033 (78.4%) | 897 | −88.2% |

**The inversion is total.** At the camera that carries 39% of the lane the guard is nearly
free at any candidate; at the face-on cameras 0.01 already costs 39% of a stroke that only
commits 7,591 to begin with. **Assembled, not decided** — 10d's deferral is to the advisor,
and the honest statement of the trade is: *this subject's principal strokes do not need the
guard, and the strokes that would be protected by it are the ones it disarms.*

## 5. ⚠ THE GARNET REPAINT — Ruling 23a, and the wall it meets

### 5a. The mask, from the ownership partition and never from colour

| candidate mask | texels | median hue | above C\* 12 |
|---|---|---|---|
| **ALL drifted-owned stone styled texels** | **67,904** | 322.6 | 16,059 |
| — restricted to above the C\* 12 floor | 16,059 | 322.6 | 16,059 |
| — restricted to lavender+magenta 290–360 | 14,287 | 328.2 | 14,287 |
| for reference: garnet-owned, **the core that stays** | 19,045 | **17.6** | 4,702 |

The stone's landmark (`first local minimum of mesh x-extent, z ≥ 0.4340`) was re-derived and
asserted unchanged. **The mask derives from which camera won each texel, not from what colour
it is** — deriving a repaint mask from the hue it exists to fix would make the stroke's
success a tautology.

### 5b. commit cannot write a styled texel, and the repaint is defined as writing over them

```python
protected = styled.reshape(-1)
assert not protected[hidx].any(), "ANDON: commit tried to touch styled texels"
```

No flag skips it. This is E08 Amendment 32 working as designed, and it is in direct conflict
with Ruling 23a's *"the one stroke class painting OVER styled texels."* **Disclosed in the
predictions commit as found-before-the-derivation, by reading the tool.**

The disposition I bring — **not adopted** — is a **recorded demotion**: a deterministic,
masked, auditable state operation setting the ruled mask to `holes = 1, styled = False`
before the stroke opens, leaving the ANDON untouched and unweakened. It is a state edit, not
a brush write, and its own invariance condition is *exactly the ruled mask changed and
nothing else*. A design fact that bears on it, reported rather than recommended: **`emit`
builds `render.png` from the atlas and `mask.png` from `holes` independently**, so a
demotion can keep the stone's existing colour and facets visible as shape context while
still marking them for repaint.

### 5c. What it costs, and how much comes back

| | texels |
|---|---|
| demoted | 67,904 |
| recovered across all eight strokes | **64,238 = 94.6%** |
| still hole after eight | 3,666 |
| (above-floor mask variant: 16,059 demoted, 15,316 = 95.4% recovered) | |

But the curve is the finding, not the total:

| after stroke | camera | garnet recovered | % |
|---|---|---|---|
| 1 | yaw 0 | 7,605 | 11.2% |
| 2 | yaw 180 | 17,969 | 26.5% |
| 3 | yaw 45 | 28,186 | 41.5% |
| 4 | yaw 315 | 38,702 | 57.0% |
| 5 | yaw 135 | 50,074 | 73.7% |
| 6 | yaw 225 | 60,146 | **88.6%** |
| 7 | yaw 90 | 62,304 | 91.8% |
| 8 | yaw 270 | 64,238 | 94.6% |

**Nearly linear — no camera dominates.** The stone is a faceted polyhedron and each camera's
facing floor plus edge guard admits a narrow band of it. **The garnet repaint is a six-to
eight-stroke job, not a two-stroke job**, and that roughly doubles the lane's stroke count
and its spend. The banked A0's styled count dips from 1,656,847 to 1,588,943 the moment the
demotion runs and only returns above it once the strokes land.

### 5d. The 19b term question, with the evidence Ruling 23a asked for

The question: does the stone's stroke prompt name the hue explicitly — *"deep red garnet"* —
where the fixture and the pair said only *a dark garnet gem pommel*?

**The measured evidence is that the term did not fail.** `E14-twin-prompts.json` v2 carries
byte-identical stems for `swordclay_0` and `swordclay_1`; both contain *a dark garnet gem
pommel*. What differs is the seed:

| | median hue | wine 0–25 | lav+mag |
|---|---|---|---|
| stone texels owned by the **770700** views (0, 4) | **17.6** | 65.40% | 7.49% |
| stone texels owned by the **770701** views (1, 3, 5, 7) | **322.6** | 0.29% | 88.97% |

Same term, 305° apart. Ruling 19b already ruled the drift a seed-borne subject fact, and
this is that ruling's own numbers on the projected asset. **On the twins' evidence, "garnet"
is a material word that IS its colour and it lands** — which is the 12e law's own test.

**The counter-reading, which I think is the stronger one for a stroke and which is why this
goes to the ruling rather than being answered here:** a brush stroke is not a twin. It
inpaints at `cn-strength 1.0` into a neighbourhood that is *currently violet*, and if the
demotion keeps the atlas colour as shape context (5b) then the stroke's strongest local
signal is the very hue it is meant to replace. The twins had no such adversarial context.
**The term did not fail against bare clay; it has never been tested against violet paint.**
That is a different question from the one the twin evidence answers, and the 12e law does
not settle it.

## 6. The proposed stroke set — PROPOSED, adopted nowhere

Every stroke below is a candidate. `texpass_brush`'s `_NOT_CLEARED` block is untouched.

| # | stroke | camera | class | committed | painted % | 20b hazard |
|---|---|---|---|---|---|---|
| A | the blade ribbon, near face | yaw 270 | hole-fill | 27,010 | 56.6% | **HIGH** — edge-on, the guard ring sits in the frame |
| B | the blade ribbon, far face | yaw 90 | hole-fill | 14,211 | 58.3% | **HIGH** — same class, mirror |
| C | diagonal fill | yaw 45 | hole-fill | 9,560 | 74.0% | low |
| D | diagonal fill | yaw 225 | hole-fill | 8,115 | 74.8% | low |
| E | diagonal fill | yaw 315 | hole-fill | 4,137 | 73.3% | low |
| F | diagonal fill | yaw 135 | hole-fill | 3,789 | 73.0% | low |
| G | face-on fill | yaw 0 | hole-fill | 1,160 | 82.4% | none |
| H | face-on fill | yaw 180 | hole-fill | 832 | 80.9% | none |
| **I–P** | **the garnet repaint** | all six/eight | **REPAINT over demoted styled texels** | 64,238 recovered | — | none at the pommel |

**Spiral order** (the composes-a-new-character law): the ordering that satisfies the law is
`0 → 180 → 45 → 225 → 315 → 135 → 90 → 270` — outward from the most-painted frames. **The
ordering that front-loads coverage is its reverse.** The two orders are opposed on this
subject and the ruling picks; I state the law's own order as the one the law implies, and the
coverage cost of following it (the lane's largest stroke opens last, with the most context it
will ever have).

**The 20b hazard, per edge-on stroke.** Ruling 20b's mechanism was *anatomy misbinding seeded
by the control's own features* — the mid-grip ring's thin horizontal edge matched a
crossguard template better than the true guard's edge-on blob. Strokes A and B open at
exactly those cameras. What is different, quantified rather than assumed: **the twins had 0%
painted context and these frames have 56.6% and 58.3%**, and the job mask is 55.6% one
connected ribbon down the blade rather than an open field at the hilt. What a misbind would
look like there, pre-stated: *a crossguard-like or figurative form appearing in the blade
ribbon near the guard, or the guard's edge-on face growing a face/skull motif again* — judged
by eye at 4× on the crossing crop before the next stroke launches.

**Recipe keys, enumerated with their defaults, for the block to earn in one commit:**

| key | tool default | accepted-route value | note |
|---|---|---|---|
| `seed` | 770700 | 770700 (pair primary) / 770701 (re-roll) | per stroke |
| `steps` | 20 | 20 | pair anchor |
| `cfg` | 2.5 | 2.5 | pair anchor |
| `cn-strength` | 1.0 | **1.0 at the brush stage** | profile note |
| `lora-w` | 0.75 | **0.0** — L5's *LoRA: NONE*, the no-LoRA graph path | must be re-verified BY VALUE per stroke; `brush_cloud_step` binds no profile |
| `denoise` | 1.0 (latent-masked) | 1.0 | masked, so only the hole synthesises |
| prompts | — | per-camera stems, §7 | keyed `y+270_e+00` etc. |

## 7. The stroke prompts, and a dispatch item with no consumer

The stems follow E12 Ruling 9d's drop discipline: an element a view cannot see is dropped
from that view's stem. **At stroke scale the drop map is identical to the twin drop map**,
and the reason is mechanical rather than chosen: **`texpass_iter emit` has no crop.** It
frames the whole figure at the profile's aspect every time, so a stroke's frame content is
that view's frame content exactly, and `_drop_map` applies unchanged — the boss term drops at
yaw 90 and yaw 270, the rings term drops nowhere.

**The dispatch's Task 1 item "the crop frame (generator-legal ÷16)" therefore has no consumer
in the current tool.** Raising `--aspect` produces a higher-resolution *full-figure* frame,
not a crop, and §2c measured that it buys 4.4%. The fixture separately forbids crop
generation outright (*"never a crop generation — frame-changes-register, falsified ×3, E12
Ruling 24b"*). Reported as a conflict between the dispatch and the tool, for the ruling.

## 8. Predictions scored

| # | prediction | outcome |
|---|---|---|
| **P1** | atlas-space components > 2,000; largest < 5% | **HELD, by 28×** — 57,332 components, largest 0.62%, median component 1 texel |
| **P1** | at yaw 270 one dominant camera-space component > 50% | **HELD** — 55.6% in one, 90.2% in three |
| **P2** | yaw 270 is the first greedy camera | **HELD** |
| **P2** | it covers 35–55% of the 210,907 | **FALSIFIED** — 27,010 = 12.8%. It is 39.3% of the *achievable* set, which is the honest denominator and is not the one I predicted against |
| P2 | yaw 90 second at 15–30% | **camera HELD**, share falsified on the same denominator (6.7%; 20.6% of achievable) |
| P2 | 3–5 cameras to ~75% cumulative | **HELD** — 3 cameras give 73.8% of the achievable set |
| P2 | 5–8 strokes total | **held for hole-fill; falsified once the garnet repaint is priced** — §5c makes it 14–16 |
| **P3** | yaw 270 frame 60–85% painted | **FALSIFIED, low** — 56.6% |
| P3 | every candidate frame ≥ 55% painted | **HELD**, by 1.6 points at the worst |
| **P3** | the anchor (highest adjacency) is yaw 270 | **FALSIFIED, and backwards** — yaw 270 is the **lowest** at 56.6%; yaw 0 is highest at 82.4%. I reasoned that the ribbon is flanked by paint and forgot that it dominates a narrow frame |
| **P4** | yaw 0 sees 25–45% of the drifted stone territory | **FALSIFIED** — 11.2% |
| **P4** | yaw 0 + 180 give 55–80% | **FALSIFIED** — 26.5% |
| **P4** | 3 strokes cover ≥ 90% of it | **FALSIFIED** — 41.5%; six strokes give 88.6% |
| P4 | propose the full 67,904 rather than the above-floor subset | proposed as predicted; both measured |
| **P5** | the plate mechanism: extent is thickness face-on, width edge-on | **HELD, and it explains 10d's inversion** |
| P5 | at yaw 270, 0.005 withholds < 4% and 0.01 withholds 2–10% of figure px | **HELD** — 1.9% and 4.1% |
| **P5** | every candidate ≤ 0.01 withholds under 10% of the brush's own territory | **HELD edge-on (−0.3%), FALSIFIED face-on (−39.4% at 0.01)** |
| P5 | at yaw 0, 0.005 < 1% and 0.01 in 0–3% of figure px | **missed** — 1.6% and 7.0% |
| **P6** | (not a prediction) the A32 conflict | confirmed in code; the demotion path measured |
| **P6** | the strokes recover 70–95% of a demoted garnet mask | **HELD, at the top edge** — 94.6% |
| P7 | 0 credits | **held** — nothing generated |
| P8 | no adoption, no profile edit, no gate armed, no memory write | **held** |

### Where I was most wrong

**P3's anchor and P4's garnet cameras are the same error in two places: I reasoned about
*where a surface is* and predicted *how much of a frame it occupies*.** The ribbon is flanked
by paint, so I called yaw 270 the highest-adjacency frame — but adjacency is a ratio, and the
ribbon dominates the narrowest frame on the subject, so it is the lowest. The stone is
visible from every camera, so I called two cameras sufficient — but visibility is not
commitment, and each camera's edge guard admits a narrow band of a faceted solid.

**The prediction I got right is the one I wrote the caution for.** P8 pre-registered that
quoting a reach number as a stroke's coverage would repeat last session's 7.4× substitution.
It would have: the reach-derived territory is 210,907 and the write-head's own achievable set
is 69,239, a 3.0× gap in the same direction. Running `selftest` instead of modelling commit
is what kept it out of the numbers — and it also means §2a is the *third* measured instance
of Ruling 22b's law, after the reach-vs-paint gap at the camera and at the twin.

## 9. What has NOT been done

- **Nothing generated. Zero credits.** No cloud submission exists; `estimate_credits` has
  nothing to quote yet and will be quoted per submission in Task 2.
- **Nothing adopted.** `texpass_brush`'s `_NOT_CLEARED` block is byte-unchanged, `thin_extent`
  remains absent from `texpass_iter`'s block, no profile/fixture/palette edit.
- **No tool edit** — the A3 missing-consumer finding (§2d) is reported, not repaired.
- **No stroke run, no finalize, no pack, no gate armed.**
- **stage 1b is untouched**: `state0/` is a copy and every probe wrote into a throwaway
  directory. No memory-store write.

## 10. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions committed before the first probe; every coverage number produced by the shipped write-head at recorded profile values rather than by a model of it; every sweep's full ladder reported with its invocation; the probe tree keeps each run's own job dir, mask, hit and cam.json |
| ANDON_AUTHORITY | **3** | 46 probe runs, 46 invariance-ANDON passes at `max delta 0.000000`; the A32 conflict surfaced *before* the derivation and disclosed in the predictions commit; the impossible 934.9% caught its own denominator before any number was reported; HALT 1 gates all generation |
| NAMED_COMPENSATORS | **3** | Zero spend, nothing irreversible. `state0/` copied from stage 1b and never written; every probe in a throwaway directory; the demotion exists only in probe states and is proposed, not applied |
| DECOMPOSE_BY_SECRETS | **3** | The funnel is decomposed stage by stage rather than reported as a coverage ratio (§2c); the territory/achievable partition is three-way rather than a fraction (§2a); the garnet mask derives from ownership and never from colour; thin_extent is reported per camera because 10d says a pooled number cannot judge it |
| UNCERTAINTY_GATED_HUMANS | **3** | Nothing decided. The spiral-vs-coverage tension, thin_extent's value, the A3 consumer, the demotion, the crop-frame conflict and the 19b term all go up with both readings and their costs; the 19b question is answered with the measurement that says the term did not fail *and* the reason that evidence may not transfer |
| EXTERNAL_VERIFIER | **2** | The write-head checks itself on every probe (the ANDON), and the coverage claims are re-runnable from the staged states by the recorded invocations; the component structure is computed independently of the greedy. `skip:` on a second model per precedent |

---

## HALT 1 — the stroke-lane ruling

`E:\AI\training\facet_next\E14_strokes\`:

```
state0/                       the pre-stroke state, copied from stage 1b, never written
stage1b_sword.glb             the packed asset the probes render
probe/r1|r2|r3/y*/            per-camera standalone + marginal probes, each with its job dir
probe/greedy/                 the eight-camera chained union at the profile's values
probe/alt/                    the same chain at edge-dist 1 + mask-dilate 15
probe/res/ · probe/sw/ · probe/thin/     the frame, write-head and thin_extent sweeps
probe/garnet_full · garnet_abovefloor · gcurve2   the demoted states + the recovery curve
probe/funnel.json · partition.json · components.json · garnet_mask.json
probe/union8_mask.npy · both_mask.npy · garnet_mask_{full,abovefloor}.npy
halt1/HALT1_candidate_frames.png    all eight frames: context over job mask, in-image labels
halt1/HALT1_yaw270_4x.png           the anchor question at 4x
halt1/HALT1_garnet_6x.png           the repaint's target at 6x beside the fixture's word
```

**Six things want the ruling, and none is mine:**

1. **⚠ The write-head's achievable set is 69,239, not 210,907** (§2a) — 1.891 points, not
   5.76. Ruling 22c's territory is a ceiling number; this is the third measured instance of
   22b's own law. **And the blade, which is 88.4% of the loss, is where the write-head reaches
   least: 14.9% of its territory.**

2. **⚠ `edge-dist` is a global pixel constant governing a local feature, and it is the
   binding constraint** (§2d). 0 → 66,235, 1 → 32,318, 4 → 27,010 at yaw 270. `project_twins`
   had this exact defect and it was fixed with a local-half-width bound; **`texpass_iter` is
   the consumer that never got the fix.** Alternative values price the lane at +61%. Whether
   the lane runs at the first-run values, at swept values, or waits for the A3 port is a
   ruling — and the profile marks all three keys as first-run operating points for exactly
   this moment.

3. **⚠ The spiral order and the coverage order are opposed** (§3b). yaw 270 commits 39% of
   the lane at the **lowest** painted adjacency on the subject (56.6%); yaw 0 has the highest
   (82.4%) and commits 1,160. The composes-a-new-character law implies
   `0 → 180 → 45 → 225 → 315 → 135 → 90 → 270`; coverage implies the reverse.

4. **`thin_extent` is assembled** (§4). Edge-on the guard is free at every candidate
   (−0.3% at 0.01); face-on 0.01 costs 39.4% and 0.021 costs 82.1%. The inversion 10d
   predicted is total, and the strokes the guard would protect are the ones it disarms.

5. **⚠ The garnet repaint meets E08 Amendment 32 head-on** (§5b) and needs a recorded
   demotion to run at all — 67,904 texels out of the styled count, 94.6% recovered, but over
   **six to eight strokes, not two** (§5c). It roughly doubles the lane. The 19b term
   question comes with its evidence: the term did not fail on the twins (same stem, 305° apart
   by seed), and it has never been tested against violet paint (§5d).

6. **The dispatch's per-stroke crop frame has no consumer** (§7). `emit` cannot crop; raising
   the aspect is a resolution change worth 4.4%, and the fixture forbids crop generation
   outright. The stroke stems are therefore the twin stems under the same drop map.

**Nothing generates before this ruling lands.**
