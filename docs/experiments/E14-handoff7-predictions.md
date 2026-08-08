# E14 handoff 7 — blind predictions, committed BEFORE the stroke-lane derivation runs

**Executor session, 2026-08-08.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 23b.
Committed before any hole-map decomposition, camera greedy, adjacency count, garnet-mask
derivation or thin-extent sweep is executed.

## What I have read, and what is therefore NOT blind

Read at the time of writing: `CLAUDE.md`; the handoff-7 dispatch; Rulings 10, 17–23;
`canon/LONGSWORD-IDENTITY.md`; `profiles/prop.json` (`_gates`, `_still_suspended`, the
`tools` blocks); my own [E14-handoff6-report.md](E14-handoff6-report.md), which already
carries the structure-level hole table; E12's handoff-14 stroke-lane dispatch as the method
precedent; and — per CLAUDE.md's standing *read the tool before you run it* —
`tools/texpass_iter.py` and `tools/texpass_brush.py` in full.

**P6 below is NOT a prediction and is disclosed as such**: reading `texpass_iter.py`
surfaced a hard mechanical conflict between the garnet repaint and the commit ANDON. It is
stated here rather than in the report so that it is on the record as *found before the
derivation*, not discovered conveniently at the halt.

Also not blind, because handoff 6 measured them: the brush territory is **210,907**
reachable-but-unstyled texels (5.76 points), of which by structure **blade 186,372 ·
crossing 14,420 · stone 5,581 · grip 4,219 · collar 315**; the stone's styled texels split
**19,045 garnet-owned / 67,904 drifted-owned**, and its above-floor texels **4,702 /
16,059**. Every prediction below is a delta or a structure claim on top of those.

---

## P1 — the hole set's component structure, in two spaces

**Atlas space.** The bake carries 46,496 UV islands, so a surface-continuous ribbon is
shattered into hundreds of atlas islands. I predict the atlas-space component count is
**> 2,000** and the largest single component is **< 5%** of the 210,907. If that holds,
atlas-space components are useless for stroke derivation and camera space is the only
meaningful frame — which is the point of predicting it.

**Camera space, at yaw 270.** Projecting the hole set into the edge-on frame, I predict
**one dominant component running most of the blade's length**, holding **> 50%** of that
frame's hole pixels, with the guard seam a separate smaller component above it.

## P2 — the greedy camera set

Candidates: the eight route yaws at elevation 0. The edge-on cameras are legitimate stroke
cameras even though their *twins* were excluded — Ruling 20b puts the edge-on surfaces in
the brush's territory by construction, and a stroke inpaints into painted neighbourhood
rather than composing from scratch.

| | prediction |
|---|---|
| first camera by marginal coverage | **yaw 270**, covering **35–55%** of the 210,907 |
| second | **yaw 90** (the opposite edge-on face), **15–30%** marginal |
| third / fourth | a diagonal then a face-on; each **< 12%** marginal |
| set size to reach ~75% cumulative | **3–5 cameras** |
| total stroke count including the garnet repaint | **5–8** |

**The two edge-on cameras will lead, and that is the whole shape of this stroke lane** —
handoff 6 measured 88.4% of the paint loss on the blade's edge-on centreline.

## P3 — painted adjacency, the spiral order's guard

The composes-a-new-character law makes adjacency a correctness constraint. The brush's
frames are *not* the twins' frames: the twins opened onto bare clay, the strokes open onto a
painted asset.

| | prediction |
|---|---|
| yaw-270 frame: figure px already painted (not hole) | **60–85%** |
| every stroke frame in the ruled set | **≥ 55% painted** |
| the anchor stroke (highest adjacency) | **yaw 270** — the ribbon is flanked by view 5 and view 7 paint on both sides for its whole length |

If any candidate frame comes in below 55% painted I will report it as a stroke that should
not open there rather than propose it, per the spiral law.

## P4 — the garnet repaint's mask and its cameras

The mask derives from the measured ownership partition (drifted views 1/3/5/7 on the stone),
not from colour — the dispatch is explicit and it is the non-circularity that matters.

| | prediction |
|---|---|
| mask if it is *all* drifted-owned stone styled texels | 67,904 (known, not predicted) |
| mask if restricted to above the C\* 12 floor | 16,059 (known, not predicted) |
| **which I will propose as the target** | **the full 67,904** — a floor-restricted mask leaves the stone's dark facets violet and the eye reads the whole stone, not its chromatic subset |
| yaw 0 sees, of the drifted stone territory | **25–45%** |
| yaw 0 + yaw 180 together | **55–80%** |
| strokes needed to cover ≥ 90% of it | **3** |

## P5 — thin_extent, with the 10d curve in the room

The blade is a plate: faces at yaw 0/180, edges at yaw 90/270. **Ray extent through a plate
is thickness face-on (~0.021) and width edge-on (~0.15–0.2)** — which is the mechanism
behind 10d's measured inversion, and it means the guard barely bites where this lane's
principal strokes live.

| candidate | withheld at yaw 270 (edge-on), % of that frame's hole px | withheld at yaw 0 (face-on) |
|---|---|---|
| 0.005 | **< 4%** | **< 1%** |
| 0.0075 | < 6% | < 2% |
| 0.01 | **2–10%** | **0–3%** |
| 0.021 (the blade's own thickness) | < 15% | **> 40%** |
| 0.03 (the character's) | < 25% | **> 85%** |

**The prediction that decides the value**: every candidate at or below 0.01 withholds under
10% of the brush's own territory, and the cliff is at the blade's own 0.021 where the
face-on strokes lose their subject. I predict I will assemble a case that the honest range
is **0.005–0.01** and that the guard is near-inert on this lane — and I will assemble it,
not decide it (10d defers the value to this ruling, and the ruling is the advisor's).

## P6 — ⚠ NOT A PREDICTION. The garnet repaint cannot run through the ordinary loop.

`texpass_iter.py` commit, line 400:

```python
protected = styled.reshape(-1)
assert not protected[hidx].any(), "ANDON: commit tried to touch styled texels"
```

Commit's candidate set is `(holes > 0.5) & valid`, and it asserts that no candidate is
styled. **There is no flag that skips it** — this is E08 Amendment 32 working exactly as
designed. Ruling 23a's garnet repaint is defined as *the one stroke class painting OVER
styled texels*. The two cannot both hold as written.

I will bring the lawful dispositions to HALT 1 with their costs measured, and adopt none.
The one I expect to propose is a **recorded, deterministic demotion**: a separate,
auditable state operation that sets the ruled garnet mask to `holes = 1, styled = False`
before the stroke runs, leaving the ANDON untouched and unweakened. Note that `emit` builds
`render.png` from `atlas` and `mask.png` from `holes` **independently**, so a demotion can
keep the stone's existing colour visible as shape context while still marking it for
repaint. That is a design fact I read, not a recommendation.

**Predicted cost**: the demotion moves 67,904 texels out of the styled count, and I predict
the strokes recover **70–95%** of them, so the banked A0's 1,656,847 dips before it rises.
Whether that is acceptable is a ruling, not mine.

## P7 — spend

`estimate_credits` per submission, quoted either way. **I predict 0 credits per submission**,
as the route has measured on every prior stroke run. Task 1 spends nothing at all.

## P8 — what will not happen

Nothing generates before HALT 1's ruling lands. No stroke runs out of the ruled order. No
texel outside a stroke's ruled mask changes. No re-roll on any authority but the eye clause,
once. No gate armed. No finalize, no pack. **No fixture, profile or palette edit — the
`_NOT_CLEARED` block is the advisor's to clear, not mine.** No memory-store write.

---

## The one I would bet against myself on

**P2's first-camera coverage.** I am reasoning from handoff 6's 88.4%-blade figure to a
yaw-270 marginal of 35–55%, but reach-at-facing-0.45 and *hole coverage in an emitted frame*
are different questions — commit uses `facing-min 0.25`, a looser floor than the ceiling's
0.45, and the emitted mask is dilated by 9. Last session I priced a camera in reach when the
question was paint and was wrong by 7.4×. The same substitution is available here and I am
naming it before it happens: **the greedy must be computed on the emitted frame's own hole
pixels under commit's own floors, not on the reach masks.** If I catch myself quoting a
reach number as a stroke's coverage, that is the error repeating.
