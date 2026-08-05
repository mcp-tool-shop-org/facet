# E04 stage 2 — the stroke-camera derivation. Report and HALT.

**Executor session, 2026-08-05, on Ruling 23's dispatch.** Nothing has been generated and
no stroke has flown. Deck strokes cited from Task 4a, side strokes derived from the hole
map, the bottom left to dilation as ruled, the spiral order derived from where stage 1 left
paint, the brush fixture landed, `_NOT_CLEARED` lifted with all seven keys decided in one
commit. **The advisor rules the set before anything runs.**

Predictions were hashed and committed blind before the instrument existed —
[E04-stroke-predictions.md](E04-stroke-predictions.md), SHA256
`B78EB03A25DB329A12F2868C54684E6DFAD342C0BA3C08275382585CA4BEBCBA`, commit `ddfbcbb`.
**Three of nine blind predictions survived.** The six that did not are the most useful
part of this report and they are scored in full at the bottom.

**Watchdog: ALIVE**, heartbeat 1 s old, VRAM 1,527 / 32,607 MiB, 29,673 MiB below the
31,200 ceiling, measured 2026-08-04 23:54:45 rather than inherited from the session hook.
Nothing in this leg touched the GPU: it is raycasting and arithmetic.

---

## The instrument, and the anchor it carries

`tools/diagnostics/e04_stroke_cameras.py` walks **`texpass_iter.py commit`'s own funnel in
its own order** — `facing > 0.25`, occlusion, thin-withholding, the 4 px edge trim — rather
than scoring camera sets by first-hit face area the way Task 4a did. That was the right
instrument for *can a camera look into this deck* and the wrong one for *how many hole
texels would this stroke write*: steps 3 and 4 are exactly what a reach calculation misses,
and on a subject with 512 rigging shells they are not small.

Two approximations, stated with their **error direction**, because a number whose error
direction is unknown is not a measurement. The edge trim runs against `emit`'s *geometry*
hit mask where the shipped guard runs against the brush output's keyed mask **intersected
with** that hit mask — a subset, so a nearer boundary and fewer survivors. The 9 px job-mask
dilation is omitted, and it only ever admits more. **Both make every commit count below an
upper bound.**

**The anchor.** A new tool's ray setup — bias, normal offset, normalisation, camera axes —
is an inherited claim until something it did not compute agrees with it:

> eight eye-level yaws at facing 0.45 reach **1,329,359 texels (42.72%)** — byte-equal to
> `e08_ceiling.py`'s pre-registered ceiling, computed by a different tool on a different
> day and printed back from the inside by `project_twins`.

And every one of the stage-1 report's eight figures re-derives from the artifacts exactly —
valid, styled, holes, the three surface classes, hull-foot count, deck styled 24.99%, other
styled 40.05%, hull-foot styled 19.44%. **0 MISMATCH rows.**

Candidates are constrained to `ship.json`'s own `cull_unseen.production` superset, **read
from the profile rather than retyped**, and membership is printed: `candidates outside the
cull superset: NONE`. A camera outside that list would need the superset widened, which is
a ruling and not a derivation.

---

## 1. Deck strokes — the measured pair, cited not re-derived

Per Ruling 23 §1 these are Task 4a's `(0,40)` and `(180,40)`: 30.17% → 49.58% of deck area,
+19.41 points, bow/stern beating beam 49.58 against 41.93, 40° the measured peak across a
30–55° plateau ([E04-task4ab-report.md](E04-task4ab-report.md)). **Not re-derived.** What is
new here is what those two cameras *commit*:

| stroke | commit | new | deck | side | bottom | foot | thin cost | edge cost |
|---|---|---|---|---|---|---|---|---|
| `y+000_e+40` | 110,294 | 110,294 | 73,020 | 36,667 | 607 | **0** | −25.39% | −10.64% |
| `y+180_e+40` | 106,311 | 90,366 | 72,246 | 33,492 | 573 | **0** | −25.12% | −12.34% |
| **union** | **200,660** | | 129,505 | 69,975 | | **0** | | |

- **Deck holes closed: 129,505 of 489,889 = 26.44%. Remaining: 73.56%.**
- **Deck coverage 24.99% → 44.82%**, against Task 4a's 49.58% area prediction — the 4.7-point
  shortfall is the funnel, mostly the thin withholding.
- The pair also closes **69,975 side-class holes** (7.30% of them) as a by-product, which is
  why the side derivation below is scored against a base that already contains them.

**Ruling 23 pre-registered "roughly half the deck's holes remain".** Measured, **73.56%**
remain. The direction was right and the magnitude was optimistic; the deck is worse served
than the pre-registration said, and that is the number Gate 1 should be read against.

## 2. Side strokes — derived from the hole map, greedy on marginal coverage

Base = *stage 1* ∪ *the deck pair* = 1,348,619 texels = 43.34% of valid. A camera set is a
union (Task 4a's own correction), so a camera that reaches surface the base already holds
buys nothing.

### The standalone landscape, and the cleanest single result in this derivation

Side-class holes each candidate would close **against the base**, grouped by where the yaw
sits relative to stage 1's eight cameras:

| candidate group | min | median | max | sum over 8 |
|---|---|---|---|---|
| the **eight stage-1 yaws** (0,45,…,315) | 3,749 | 9,383 | **11,890** | 62,385 |
| the eight **30°-multiples** stage 1 lacks (30,60,120,150,210,240,300,330) | **13,144** | 17,078 | 23,623 | **141,160** |
| the eight **15°-offsets** (15,75,…,345) | 10,047 | 13,263 | 14,669 | 101,066 |

**The two bands do not overlap.** The best stage-1 yaw (11,890) is below the worst
30°-multiple (13,144). Re-standing exactly where a twin stood is the *worst* thing a side
stroke can do — the floor drop 0.45 → 0.25 opens only a 12.2° grazing annulus, and that
annulus is largely what the edge trim then removes (yaw 0 loses **57.94%** of its
after-thin set to the edge trim; yaw 180 loses **62.35%**). This is P3's mechanism as a
measurement rather than an argument.

### The greedy ladder

| pick | camera | side-new | all-new | foot-new | deck-new | cum side holes | styled/valid | hull-foot |
|---|---|---|---|---|---|---|---|---|
| 1 | `y+150_e+00` | 23,623 | 40,759 | 2,078 | 4,096 | 9.76% | 44.65% | 21.21% |
| 2 | `y+030_e+00` | 20,395 | 39,148 | **4,525** | 3,635 | 11.89% | 45.91% | 25.05% |
| 3 | `y+240_e+00` | 16,037 | 31,991 | 233 | 7,259 | 13.56% | 46.93% | 25.25% |
| 4 | `y+300_e+00` | 14,618 | 30,562 | 1,323 | 4,561 | 15.09% | 47.92% | 26.37% |
| 5 | `y+060_e+00` | 14,187 | 24,918 | 197 | 3,483 | 16.57% | 48.72% | 26.54% |
| 6 | `y+120_e+00` | 12,022 | 20,564 | 171 | 2,852 | 17.82% | 49.38% | 26.69% |
| 7 | `y+330_e+00` | 8,828 | 15,750 | 823 | 1,737 | 18.74% | 49.88% | 27.38% |
| 8 | `y+210_e+00` | 7,489 | 13,126 | 217 | 2,211 | 19.52% | 50.31% | 27.57% |

**There is no knee.** Per-stroke gain in points of valid runs 1.31 · 1.26 · 1.02 · 0.99 ·
0.80 · 0.66 · 0.50 · 0.43 — a smooth decay. This repo has paid once for reading a shoulder
as a valley (Task 4a's "antimode" at 0.0090, which was the top of a shoulder), so **no cut
is discovered here and none is invented.** The ladder is the price list; which prefix to
buy is a ruling.

### Why it is flat, MEASURED rather than asserted — and the denominator that makes it read right

A flat ladder has two very different explanations, and picking one by intuition is the move
this repo keeps paying for. So the funnel was unioned across **all 24 eye-level candidates
plus the ruled deck pair**, and every side-class hole attributed to the stage that rejected
it *everywhere*:

| why a side hole is not reachable by any stroke in the candidate list | texels | share of side holes |
|---|---|---|
| never faces any candidate at 0.25 | **0** | 0.00% |
| faces one, **OCCLUDED on every one** | **616,222** | **64.28%** |
| visible somewhere, thin-withheld on every one | 64,395 | 6.72% |
| survives thin, edge-trimmed on every one | 38,804 | 4.05% |
| **REACHABLE by some candidate stroke** | **239,219** | **24.95%** |

**Not one side hole fails the facing test. 64.28% are occluded from every camera in the
list** — behind rigging, inside the waist, under the forecastle, between hull and channel.
So **24.95% of side holes is the ceiling for this candidate set**, exactly as 42.72% was
stage 1's, and the ladder should be read against it:

| prefix | side holes closed | of all side holes | **of the 24.95% ceiling** |
|---|---|---|---|
| deck pair only | 69,975 | 7.30% | **29.25%** |
| n = 2 | 113,993 | 11.89% | **47.65%** |
| n = 4 | 144,648 | 15.09% | **60.47%** |
| n = 6 | 170,857 | 17.82% | **71.42%** |
| n = 8 | 187,174 | 19.52% | **78.24%** |

**The ladder is flat because the reachable side surface is nearly exhausted, not because
the cameras are badly chosen.** Eight side strokes take 78% of everything physically
available to an eye-level stroke, and **all sixteen remaining eye-level candidates together
could add at most 5.43 points** (24.95 − 19.52) of side holes. That is the expensive arm
bounded before it is spent, and it is the strongest argument in this report against ruling
a longer set.

⚠ **This ceiling is the candidate list's, not an absolute.** It is measured over 24 eye-level
yaws plus `(0,40)` and `(180,40)`; an elevated camera unlocks side surface that eye level
cannot see, which is exactly what §6's `y+090_e+40` diagnostic shows (17,067 side-new, and
outside the cull superset).

### What *is* structural: the greedy produced mirror pairs

The ship is bilaterally symmetric about its centreline, and a camera at yaw *y* mirrors to
yaw *180−y*. The greedy's eight picks are exactly the four mirror pairs **(30,150) ·
(240,300) · (60,120) · (210,330)**, and it completed each pair before opening the next —
picks 1-2, 3-4, 5-6, 7-8. That was not designed in; it fell out of marginal coverage, which
is itself evidence the mesh is close to symmetric.

**So the adoptable prefixes are n = 2, 4, 6, 8**, and they are mirror-complete rather than
arbitrary. An odd prefix would paint one flank of a symmetric ship better than the other,
which is a defect an eye catches and no metric here would.

| prefix | strokes total | styled/valid | reference / brush / dilation | hull-foot | side holes closed |
|---|---|---|---|---|---|
| deck pair only | 2 | 43.34% | 36.89 / **6.45** / 56.66 | 19.44% | 7.30% |
| **n = 2** | 4 | 45.91% | 36.89 / **9.02** / 54.09 | 25.05% | 11.89% |
| **n = 4** | 6 | 47.92% | 36.89 / **11.03** / 52.08 | 26.37% | 15.09% |
| **n = 6** | 8 | 49.38% | 36.89 / **12.49** / 50.62 | 26.69% | 17.82% |
| **n = 8** | 10 | 50.31% | 36.89 / **13.42** / 49.69 | 27.57% | 19.52% |

**Read against the character with Ruling 5's caution in the same breath:** the accepted
character asset measured 68.8 / **4.2** / 27.0. This subject's stroke stage buys **6.45 to
13.42 points** of valid — between 1.5× and 3.2× what the character's eight strokes bought —
because the ship's stage-1 reference share is structurally low and there is simply more for
the brush to do. The brush column is the one place where the ship *out-performs* the
character, and it does so for the same geometric reason its reference column under-performs.

### What I propose, and what is not mine

**Proposed: the ruled deck pair + n = 4 side strokes — six strokes total.** Grounds, each
one a measurement or a stated purpose rather than a curve reading:

1. **Mirror-complete** — `(30,150)` and `(240,300)`, both flanks equal.
2. **It buys the waterline rim almost all of what is available.** The foot goes 19.44% →
   26.37% by n = 4; the remaining four strokes add **1.20 more points**. 85% of the entire
   available foot gain sits in the first four picks (see §4).
3. **It takes 60.47% of the measured side-stroke ceiling for four strokes**, where the
   second four take it to 78.24% — 17.8 points of ceiling for another four denoise-1.0
   compositions.
4. Per-stroke gain is ≥ 0.99 points through n = 4 and below it after — stated as a fact
   about the table, **not** as a threshold; the decay is smooth and any prefix is defensible.

**The set size is the advisor's ruling and I am not narrowing it.** The consideration I
cannot weigh: every extra stroke is another **denoise-1.0 composition** on a subject whose
brush behaviour is completely unmeasured — no stroke has ever run on this ship — and E07's
flesh blade reached the Director through exactly this stage. Against that, cloud generations
have cost **0 credits** across 17 submissions this arc. That trade is a judgment, not an
arithmetic. `texpass_loop.ps1 -StopBeforeCommit` already exists as a human gate between
stroke 1 and stroke 2 if the ruling wants the first stroke to inform the rest.

## 3. The hull bottom — no strokes, as ruled, and what that leaves

Ruling 23 §3, not re-opened. **515,329 downward-facing holes.** The proposed set closes
**70,965 of them incidentally (13.77%)** — side and elevated cameras clip the turn of the
bilge — and **444,364 fall to dilation** from hull-adjacent paint, planking continuing
planking. Recorded so Gate 1 reads the bottom as a decision with a number, not an omission.

## 4. The waterline rim — the answer Ruling 23 asked for specifically

**Hull-foot: 117,682 texels (3.78% of valid), 94,805 of them holes, stage-1 styled 19.44%
against 36.89% whole-mesh — 53% of the ship's average rate.**

| | foot styled | foot texels closed |
|---|---|---|
| stage 1 | 19.44% | — |
| **+ the deck pair** | **19.44%** | **0** |
| + n = 2 | 25.05% | 6,602 |
| + n = 4 | 26.37% | 8,156 |
| + n = 6 | 26.69% | 8,532 |
| + n = 8 | 27.57% | 9,568 |

Three things, and two of them are cautions:

1. **The deck pair buys the waterline rim exactly nothing** — 0 texels, both strokes. An
   elevated camera cannot see a hull's foot at all. Whatever serves the rim is a side
   stroke or it is dilation.
2. **The side set buys it +6.9 points at n = 4, +8.1 at n = 8**, and almost all of it comes
   from the four **±30°-from-broadside** yaws (30, 150, 330, 210 → 7,643 of the 9,568 =
   **79.9%**). The beam-adjacent picks buy the foot 171–233 texels each: near nothing.
3. **The rim stays the least-covered region of the mesh, in the same ratio.** 27.57% against
   50.31% whole-mesh is **55% of average** — stage 1's ratio was 53%. The strokes lift the
   foot and the whole ship together; they do not close the gap. **E10's waterline layer will
   still be painting over a base coat roughly half as thick as the ship's average**, which
   is the caution Ruling 19 asked to have carried forward, now with a number.

**An asymmetry, reported as an observation and not a conclusion.** Cameras looking at the
yaw-0 flank find 2.4–2.6× more unpainted hull-foot than their mirror partners — yaw 0:
6,244 against yaw 180: 2,563; 345: 5,899 against 195: 2,368; 330: 5,191 against 210: 1,987.
A mirror-symmetric hull should not do that. The available mechanism is in the stage-1
baseline: **view 0 was the weakest twin of the eight** — IoU 0.8287 (lowest) and 24,151
texels keyed outside the silhouette (8.48%, highest). Whether the asymmetry is that twin or
the mesh is not established here, and the Gate 1 sheet's beam views are where it becomes
visible.

## 5. The spiral order — derived, and nearly inert on this subject

The rule is CLAUDE.md's: *order strokes to spiral outward from already-painted regions, or
the brush composes a new character instead of continuing one.* The quantity it protects is
the **worst-anchored** stroke — E08's failure case was one camera opening at 95% hole and
returning a plaited belt, a strap across the upper arm and a lengthened tunic. So four
candidate orders were **simulated**, accumulating each stroke's commit before scoring the
next, and scored on their minimum:

| order | min anchor | mean | sequence |
|---|---|---|---|
| A greedy-anchor (best-anchored remaining, each turn) | **75.34%** | 81.58% | 300 · 330 · 240 · 210 · 120 · 060 · 030 · 150 · `180@40` · `0@40` |
| **B ring sweep from the best-anchored seed, deck pair last** | **74.90%** | 81.65% | **300 · 330 · 030 · 060 · 120 · 150 · 210 · 240 · `0@40` · `180@40`** |
| C the coverage-greedy order, deck pair first | 64.10% | 82.13% | `0@40` · `180@40` · 150 · 030 · 240 · 300 · 060 · 120 · 330 · 210 |
| D deck pair first, then the ring sweep | 64.10% | 82.15% | `0@40` · `180@40` · 300 · 330 · 030 · 060 · 120 · 150 · 210 · 240 |

**Proposed: order B.** It is the rule as written — outward from the best-anchored camera,
each stroke adjacent in the yaw ring to the last — and it costs 0.44 points of minimum
anchoring against A, which is metric-optimal but **not contiguous** (it jumps 330 → 240 →
210 → 120, skipping the ship). The deck pair goes last in both, because the two elevated
cameras are the least anchored on the mesh (64.10% and 64.06% standalone against 75–86% for
every eye-level candidate) and stroking them after the ring lifts them to 74.9% and 79.3%.

**The honest headline is that the order barely matters here.** Stage 1 painted all eight
yaws, so every candidate camera opens between **64% and 88%** anchored. The character's
disaster case was 95% *hole*. On this subject the spiral is doing very little work, and a
ruling that prefers C or D for its higher mean is not making a mistake — it is trading a
worst case of 64% for a mean of 82.1 against 81.7.

**If the ruling shortens the set, the order re-derives over the ruled subset by the same
rule** — ring sweep from the best-anchored member, deck pair last. At n = 4 that is
`300 · 030 · 150 · 240` … stated as the rule, not as a second table, because the numbers
would have to be re-simulated for whatever prefix is ruled.

## 6. Diagnostics — two cameras in the superset that beat the last side strokes

Reported, never entered into the greedy, because Ruling 23 §1 forbids re-deriving the deck
answer. Measured **against the full proposed set of ten**:

| camera | side-new vs base | **all-new vs the FINAL set** | in the cull superset? |
|---|---|---|---|
| `y+000_e+55` | 12,411 | **27,371** | **yes** |
| `y+180_e+55` | 12,166 | **27,515** | **yes** |
| `y+090_e+40` | 17,067 | 27,062 | no |
| `y+000_e+20` | 13,698 | 19,361 | no |
| `y+090_e+20` | 13,423 | 17,480 | no |
| `y+270_e+40` | 9,625 | 16,080 | no |
| `y+180_e+20` | 11,286 | 15,798 | no |
| `y+270_e+20` | 8,111 | 10,968 | no |

**`(0,55)` and `(180,55)` each add more than twice what the eighth side stroke adds
(27,371 / 27,515 against 13,126), and both are already inside `cull_unseen.production`.**
Task 4a measured the 55° pair at 49.15% deck area against 40°'s 49.58% and adopted 40 as
the peak — which was correct *as a two-camera choice*, and says nothing about 55 as a
**fifth and sixth** camera on top of 40. This is a ruling for the advisor, not a proposal:
it would extend the deck answer that Ruling 23 explicitly closed.

## 7. The brush fixture, and the block lifted

**[E04-brush-prompts.json](E04-brush-prompts.json)** — one **constant identity string** per
stroke, per Ruling 23, transcribed from `E04-twin-prompts.json` by byte-comparing all eight
stems rather than retyped (the generator asserts all eight are one string, and that they are
eight). It carries a key for **every camera in the production superset (28)**, not only the
proposed ten: `brush_cloud_step.py` ANDONs on a missing key at graph time, and because the
constant-string ruling makes every value identical, **a ruled set that differs from the
proposal changes `_order` and no string.** The fixture is therefore closed against whatever
the advisor rules, not against one proposal.

Checked consumable rather than assumed: `brush_cloud_step.py graph` builds a 17-node graph
from it with **no self-links, no dangling targets, no non-terminal orphans**, prompt 439
chars, the live LoRA card `mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500`
@ 0.75. No submission, no dry-run, no credits — the graph was written to the scratchpad.

**No orientation phrase, including on the two elevated strokes.** E08's brush file gave its
+55 cameras "from above"; the ship's twins carry **no orientation vocabulary at all**, so
introducing one at the brush stage would put a word in front of the model that no generation
on this subject has ever carried. If a deck stroke composes something that is not a deck
seen from above, that is the evidence for the phrase and it gets added with the measurement.

**`_NOT_CLEARED` lifted, and the lifecycle ran as Ruling 22 specified.** Removing the marker
reverted seven keys to undecided, `--coverage` fired, and the clearance was paid for by
deciding them in the same commit (`c66ba70`):

```
[chk] ship.json: 56 values checked against 8 tools
[chk] NOT A PURE RELOCATION - 17 mismatches:
[chk]   texpass_brush.py         prompt    source default 'a burly bald warrior...' != 'a gilded lion figurehead...'
[cov] coverage against character.json: 64 reference keys decided, 0 UNDECIDED
[cov] every reference key has an explicit decision in this profile.
```

49 → 56 checked, 16 → 17 mismatch rows, the single new row being the one that should be
there. That count was **declared before the edit** (P10), not read off afterwards.

**One deviation, flagged rather than taken silently.** `negative` is the ship's **own SPENT**
value (`watermark, text, logo, blurry, photo, deformed` — what the ratified pair and all
eight twins ran on) and not the accepted character route's *brush* negative. W3's brush
negative is not W3's restylize negative: it carries eight belt terms — `braided belt,
plaited belt, woven belt, rope belt, shoulder strap, chest strap, baldric, bandolier` —
which `texpass_loop.ps1`'s own header records as failure modes **measured at the brush stage
on that character**. Importing another subject's measurements is Ruling 2's named accident
class. Nothing in this repo calls the negative a recipe key — "recipe" names
seed/steps/cfg/lora-w/cn-strength wherever it appears, including `brush_cloud_step.DEFAULTS`
— and that tool reads the negative from the prompts file beside the prompt. **One line
either way from the advisor.**

Also recorded and **not acted on**: the rejected twin 7 painted 2,002 px of implied water,
and adding a `water` negative term now would be inventing a term from a rejected artifact
before a single stroke has run. Ruling 19 made the waterline a layer.

---

## FINDING — `brush_cloud_step.py` binds no profile, so five of the seven keys never arrive

Generation is cloud-only, so a ship stroke runs through `brush_cloud_step.py`.
`texpass_brush.py` posts to `127.0.0.1:8188` and **will not run on this subject at all**.
And `brush_cloud_step.py` carries no `subject_profile.bind()` — it has its own
`DEFAULTS = {seed 770700, steps 20, cfg 2.5, lora_w 0.75, cn_strength 1.0}` and a hardcoded
`CLOUD_LORA`, and takes the prompt and the negative from the prompts file.

So of the seven keys Ruling 23 just decided: **`prompt` and `negative` reach the graph
through the fixture, and the five recipe numbers reach it through that tool's own
constants.** They agree today because Ruling 23 set them to exactly those values — **by
coincidence of value, not by construction.** A future ruling that moves the ship's brush
recipe off the character's numbers would edit a profile that the graph never reads.

This is armT-halt2's Finding B at a **fourth site**, and it is invisible to both guards:
the purity checker compares values that are present, and `--coverage` compares against
`character.json`, **which has no `brush_cloud_step.py` block either**. It is recorded in the
profile block itself so it cannot be lost, and it is not fixed here — a shared-code change
outside the profile is exactly the primary finding the spec's H2 test is about, and closing
it is a ruling.

## Predictions against measurement — three of nine blind survived

| # | predicted | measured | |
|---|---|---|---|
| P1 | deck pair commits 150k–350k hole texels | **200,660** | **correct** |
| P2 | 50–65% of deck holes remain after the pair | **73.56%** | **FALSIFIED** — worse than predicted |
| P3 | the first side pick is an intermediate yaw | **`y+150`**, and the two bands do not overlap | **correct** |
| P4 | first side pick > 60,000 side-class texels | **23,623** | **FALSIFIED** by 2.5× |
| P5 | 4th pick below 40% of the 1st | **61.9%** | **FALSIFIED** — the ladder is flat, not steep |
| P6 | hull-foot reaches 30–55% | **27.57%** at n=8, 26.37% at n=4 | **FALSIFIED** — below the band |
| P7 | eye-level opens; both deck strokes in the last third | opens `y+300`; deck at 9 and 10 | **correct** |
| P8 | thin costs 5–15% on every candidate | **15.79% – 48.66%** | **FALSIFIED** — badly, on every candidate |
| P9 | edge costs more than thin at yaw 90 and 270 | thin 37.85 / 32.46 vs edge 20.85 / 20.04 | **FALSIFIED** on both |
| P10 | *(declared)* 0 undecided; mismatches 16 → 17 | 0 undecided; 16 → 17; 49 → 56 checked | correct |

**P8 is the one worth naming as a finding rather than an error.** I reasoned from
`ship.json`'s own record that `thin-extent 0.01` withholds "10.20% of visible area on every
view" and predicted a 5–15% band. Two things were wrong with that. The 10.20% is a
**cross-view** figure — area withheld on *every* view, an intersection — and I compared it
to a per-view quantity, which is the wrong operand. And more importantly the denominator is
different in kind: 10.20% is a share of *visible area*, while a stroke's population is
*holes*, and **holes concentrate in exactly the thin structure the policy withholds.** The
rigging is where the paint is missing and it is also what `thin-extent` refuses to paint.
Measured on the hole population the policy costs **a quarter to a half** of what a stroke
could otherwise commit — 48.66% at yaw 15, 46.6% at 165 and 345, 15.79% at 285.

That is the thin policy working as designed (thin hard-surface structure takes projected and
dilated colour, never invented content), and it is a much larger tax on this subject than
anything in the record suggested. It is **not** re-opened here — `thin-extent`'s
structural-thickness replacement is explicitly out of scope in the spec — but the number
belongs in the record, and it means **the rigging will be served by dilation almost however
many strokes are ruled.**

**P4 and P5 failed together, for the one reason I pre-registered as the failure mode that
would matter** — and the prediction file named it in advance: *"If instead they are
occlusion holes … then no eye-level yaw will buy much, every marginal gain will be small
and flat, and the honest output is that the side class is not a stroke problem at all."*

That is what happened, and §2's attribution measures it rather than leaving it as the
explanation that fits: **64.28% of side-class holes are occluded from every camera in the
list, 0% fail the facing test**, and the whole candidate set has a 24.95% ceiling. The
proposed four strokes take 60% of that ceiling and the full eight take 78%. So the flat
ladder is not a badly chosen camera set and it is not a tuning opportunity — it is the
subject, and it was worth being wrong about it in writing first, because the
falsification is what sent me to measure the residual instead of asserting a cause for it.

## What was not done

No generation, no `dry_run`, no `estimate_credits`, no submission, no credits. No stroke,
no finalize, no pack, no Gate 1 sheet. No threshold was invented and no suspended bound was
armed. The hull-bottom question was not re-opened. The `(0,55)`/`(180,55)` diagnostic was
reported and not adopted. The `brush_cloud_step.py` profile gap was recorded and not fixed.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every threshold is a flag whose default is the value `ship.json` carries for the tool it comes from; the candidate list is read out of the profile rather than retyped; predictions hashed and committed at `ddfbcbb` before the instrument existed; the fixture is generated from the profile and the twin file by a script, not hand-authored |
| ANDON_AUTHORITY | **3** | The lifted `_NOT_CLEARED` fired `--coverage` exactly as its lifecycle specifies and was paid for in the same commit; the instrument re-derives eight inherited figures and prints MISMATCH rows rather than absorbing them; the superset-membership check would name any candidate that needed a widening; no cut invented where the ladder shows no knee |
| NAMED_COMPENSATORS | **3** | Nothing irreversible: two new files, one profile edit, git as undo, zero cloud spend. The probe graph was written to the scratchpad and submitted nowhere |
| DECOMPOSE_BY_SECRETS | **3** | Every derived value is this subject's geometry; the one quantity that could not live in the profile — the stroke order, which has no tool flag — is recorded in `_still_suspended` pointing at the fixture that does carry it, rather than forced into a `tools` block where the loader would ANDON on it |
| UNCERTAINTY_GATED_HUMANS | **3** | The set size, the negative, and the `(0,55)` question are each posed with their numbers and left to the ruling; the proposal states which of its three grounds are measurements and which is a reading of a table; the prediction scorecard is at the bottom rather than absent |
| EXTERNAL_VERIFIER | **2** | The instrument reproduces a ceiling computed by a different tool on a different day to the texel, and all eight stage-1 figures exactly — the strongest available check that its geometry is not its author's opinion. `skip:` on a second model: this is deterministic raycasting |

---

## For the ruling, in one place

1. **The set.** Proposed: deck pair + **n = 4** (`y+150, y+030, y+240, y+300`) = six strokes.
   Adoptable mirror-complete alternatives n = 2, 6, 8 with full numbers in §2. No knee exists;
   the choice is a ruling and the trade is coverage against denoise-1.0 invention risk on a
   subject whose brush behaviour is entirely unmeasured.
2. **The order.** Proposed: B, the ring sweep with the deck pair last. Nearly inert here —
   every candidate opens 64–88% anchored against the character's 95%-hole disaster case.
3. **The negative.** The ship's own spent value, a flagged deviation from a literal reading
   of Ruling 23. One line either way.
4. **`(0,55)` and `(180,55)`** each add more than twice what the eighth side stroke adds and
   are already in the cull superset. Reported, not proposed — adopting them re-opens the deck
   answer Ruling 23 closed.
5. **`brush_cloud_step.py` binds no profile.** Finding B at a fourth site, invisible to both
   guards. Recorded in the profile block, not fixed — closing it is shared-code work.
6. **The rigging is dilation's however the set is ruled** — thin-withholding costs 15.79% to
   48.66% of each stroke's otherwise-committable holes, far more than the 10.20% figure in
   the record suggested, because holes concentrate in exactly the structure the policy
   refuses to paint.
