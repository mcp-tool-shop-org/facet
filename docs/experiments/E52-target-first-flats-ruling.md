# E52 — ruling: target-first does not address the flat class, and my P3 was mis-specified

**Advisor, 2026-08-17**, on `E52-target-first-flats-report.md`. The seat ran the spec as
written, halted at nothing because nothing fired, missed two of three predictions and
called both misses misses. Zero spend.

---

## Ruling 1 — the arm is dead, and it is dead by measurement

The kickoff ranked the target-view-preferring compositor as a free fix on the reasoning
that *"the flats are one view winning a wrap of the chest; preferring the target view
addresses the shape."* **It does not.**

| target | B (global argmax) | C (target-first) | delta |
|---|---|---|---|
| t00 | 38 (lcc 9) | 40 (lcc 25) | **+2** |
| t01 | 8 | 4 | −4 |
| t02 | 31 | 25 | −6 |
| t03 / t04 / t05 | 0 | 0 | 0 |
| t06 | 23 (lcc 5) | **64 (lcc 59)** | **+41** |
| t07 | 36 (lcc 6) | **110 (lcc 25)** | **+74** |

At target 0 the count rose. At two targets it rose sharply, and grew *more connected* —
t06's largest component 5 px → 59 px, which is the direction that makes a patch read as a
patch rather than as speckle. The seat pre-registered *"falsified if C's count ≥ B's
count"* and reported C ≥ B without softening it.

**No further work on this arm.** It is not a threshold question and there is nothing to
tune: the policy was already the shipped default, the comparison was one variable, and the
result went the wrong way on the target the defect was named on.

## Ruling 2 — why it cannot work, which the record already contained in pieces

`flat_trace.py` reported two things about this defect and the kickoff carried only one of
them forward:

> The **angular shape is ownership.** […] The colour is in the contributing twin as a
> different green of **the same named surface (N3)**.

Shape is ownership; **colour is not**. Target-first changes who owns a texel — so it can
change the shape of the patch — but the colour arrives with whichever view wins, and the
olive is view 6's own paint of a surface view 6 is correctly painting. So at **t06, where
target-first means *prefer view 6***, the policy maximises exactly the paint the defect is
made of: 23 → 64.

The seat's own mechanistic note supports this and stays on the right side of its mandate —
at t06 and t07 the gained pixels' mean colour barely moves between arms
(`(109.8,102.5,76.0)` → `(104.7,101.7,72.7)`), i.e. pixels crossing a threshold, not a new
colour appearing. **An ownership policy cannot repair a cross-view colour disagreement on a
correctly-attributed surface.** That is the finding, and it retires the ownership family
for this defect rather than only this one arm of it.

## Ruling 3 — my P3 was mis-specified, and the correct reading is worse for the arm

**The error is mine, in the dispatch.** I specified a direction count over 8 targets
against a **fixed image-space box**. Three rows (t03, t04, t05) read **0 in both arms** and
therefore **cannot exhibit either direction** — they are not agreement, they are absence of
population. The seat honoured the spec exactly and printed the raw table, which is why the
flaw is visible at all.

- **As specified:** 5 of 8 non-increase — a band miss against 6–8.
- **Read honestly:** of the **five targets carrying any population**, **two decreased and
  three increased**, two of those sharply.

Same family as *a check that cannot fail is not a check*, and the same family as the eleven
consecutive unit/population misses: **the population was not checked for the property
before the direction count was defined over it.** Whether those three boxes contain any
figure at all on those views is not measured in the report and I am not inferring it.

**Standing correction for future dispatches: a per-view count over a fixed image-space
window must report, per view, whether the window carries a population — and rows that
cannot move are excluded from the denominator, not counted as agreement.**

## Ruling 4 — the arm-A path in my dispatch was not the one the test pins

I named arm A as `facet_E48\renders_owner_complete\owner_complete_0.png`, taken from a
directory listing. **T89's own artifacts leg reads the same-named file under
`facet_E49`** — a later atlas build whose render and `owner.npy` are byte-different.

The seat found this, ran the pinned check against **both**, and both return `n=115`,
`owner6=97` exactly. **No number in this arc moves**, and two independently built atlases
agreeing at the anchor is a better state than one. But the dispatch should have taken its
anchor path from the test that pins the claim rather than from `find`, and the next
dispatch citing an anchor artifact takes it from the test.

## What holds up

- **Gates.** Four, none fired, each with evidence rather than assertion; Gate C was closed
  *structurally* — one `s3_composite()` call returns both fields and `s3_run.py:141-142`
  writes both PNGs in one loop iteration — which is stronger than the timestamp comparison
  the spec would have accepted.
- **The disclosed non-blindness.** Gate A required looking at C before predictions were
  written; the seat recorded that, and then recorded that the glance **pointed the wrong
  way** against the measurement. That is a finding about this repo's own judging practice
  and it belongs next to *judge at the Director's zoom, not from a contact sheet*: a wide,
  lightly-zoomed look was not a stand-in for the classifier.
- **The symmetric check nobody asked for.** P2 asked only about removed pixels. The seat
  measured the **gained** set as well once the net delta went the wrong way, and found a
  different mechanism — 19 pixels that were *uncovered* in B and became olive-painted
  coverage in C. Without it the +2 at t00 reads as noise; with it, it is 17 recovered
  against 19 gained. *A swap is not a gain until you have looked at what left* — applied by
  the seat, unprompted, in the opposite direction.

## Where this leaves the defect

The flat class is now measured as: **not a fill artifact** (E51), **not in the render
view's own twin** (E50/T89), **not repairable by ownership policy** (this arc), and
**not a material-boundary problem with geometry to snap to** (E49). What remains named
and unexcluded is the one thing flat_trace stated in its docstring — *a real cross-view
colour disagreement on an already-named surface* — which is a **paint** question, not a
compositing one.

**I am not proposing an arm for it in this ruling.** The next move on this defect is the
Director's eye on `region_grid_all8.png` and the t06/t07 rows, because every cheap
compositing hypothesis is now spent and what is left costs a generation.

## Out of scope, respected by the seat

`s3_on/` untouched. No tool edited. No commit. No generation. `facet_E50`/`facet_E51`
never read. Targets 1–7 never given an arm-A column, enforced by a literal rather than
templated path.
