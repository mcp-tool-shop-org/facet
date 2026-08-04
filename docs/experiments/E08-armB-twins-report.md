# Arm B — the eight twins: report

**Executor session, 2026-08-04.** Predictions in
[E08-armB-predictions.md](E08-armB-predictions.md), committed at `542de7f` before submission.
All eight generated in one cloud batch, 8/8 completed, 0 failed.

## B4 HOLDS — no face on the rear views

I deliberately did **not** view-gate the beard out of the rear prompts, and pre-registered that a
face appearing on views 3/4/5 would falsify B4 and be **my** fault rather than the control's.

**It did not happen.** Views 3, 4 and 5 show the back of a bald head with beard mass visible past
the jaw where a real bearded figure would show it. Every twin matches its own clay render's
orientation — checked side by side at
`ARMB/clay_vs_twin_odd.png`, not off a contact sheet.

The reasoning behind the choice holds up: E01's face-on-the-back-of-the-head came from a control
that carried no contour, and an exact-silhouette control at IoU 1.000000 locks orientation
without needing the prompt to be filtered.

**A correction to my own reading along the way:** from the contact sheet I judged view 7 to be a
rear view when its prompt said "seen from the front," and started to treat it as a convention
error. At proper zoom against its clay, **view 7 is a front three-quarter and matches its clay
exactly.** The contact sheet was the wrong instrument for the question — which is the repo's own
rule about the Director's zoom, arriving from the diagnostic side.

## B1 IS FALSIFIED — on one view of eight

**View 6 (+270 profile) has a navy blue sleeve.** The specification says *"a dark green knitted
**sleeveless** tunic"* and bare arms with brown leather bracers. Blue appears nowhere in the
specification at all.

```
BLUE inside the figure mask   (C* > 12, hue 240-320 deg)
view   figure px    BLUE px   % figure   largest connected blob
   0     146,356          0      0.00%          0
   1     149,780          0      0.00%          0
   2      90,553          0      0.00%          0
   3     120,439          0      0.00%          0
   4     146,356          0      0.00%          0
   5     149,780          0      0.00%          0
   6      90,553      5,590      6.17%      4,882      <-
   7     120,439          0      0.00%          0
```

**Seven of eight are at exactly zero.** View 6 is 5,590 px, and **4,882 of them are one connected
blob** — a single garment, not scattered speckle.

**And view 2 is the same camera from the other side.** Same prompt, same spec, same settings,
mirrored geometry — and it renders bare skin and a brown bracer, correctly. So the cause is not
the prompt and not the specification: it is a per-view roll on one camera.

This is exactly the defect class E07 established the old metrics cannot see — *a large region of
the wrong material*, smooth inside itself, contributing only its rim to any high-pass statistic.
It is visible instantly at `ARMB/profiles_zoom.png` and would be invisible in a blotch count.

## Standing against the predictions

| # | prediction | outcome |
|---|---|---|
| B1 | named elements at front-view reliability on every view | **falsified — 7 of 8**. View 6's sleeveless tunic gained a sleeve. |
| B4 | no frontal detail on rear views despite the ungated spec | **holds** |
| B2 | drift lands in structure, not named attributes | **not yet testable** — needs the projection |
| B3 | reference coverage ~55% of valid | **not yet run** |

## The decision this reaches, which is not mine

Projecting all eight twins paints **that blue sleeve onto the mesh**. The options are:

1. **Project all eight as they are** and carry a known 6.17% contamination on one camera into the
   atlas, recorded.
2. **Re-roll view 6** on a different seed.
3. **Project seven**, dropping view 6, and accept whatever coverage that costs.

**I am not choosing.** Option 2 in particular is selecting a result after seeing it, which is the
move this repo treats as always wrong — but "re-roll a view that produced an off-spec garment" is
arguably production practice rather than tuning a pass condition, and that distinction is a
ruling, not an executor's call.

Nothing has been projected. The twins are on disk at `ARMB/twins/twin_{0..7}.png`.

## Artifacts

`ARMB/twins_sheet.png` — all eight · `ARMB/profiles_zoom.png` — views 2 and 6 at torso scale,
where the sleeve is unmissable · `ARMB/clay_vs_twin_odd.png` — orientation check against clay.
`prompt_id`s in the batch: `21519a7d…` `579e3bfc…` `6401ba8b…` `18413250…` `11edc3ad…`
`bbe2e967…` `9f1950ed…` `5a4b956a…`.
