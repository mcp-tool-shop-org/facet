# Arm B — projection HALTED at the bbox andon on view 6

**Executor session, 2026-08-04.** Eight-camera projection halted before writing an atlas.
The 2-camera control on the same twins and settings completed and is reported below.

## The halt

```
[twins] y+270.0: twin paint bbox 842 x 536   mesh silhouette bbox 848 x 279
AssertionError: ANDON: y+270.0: keyed twin bbox 842x536 exceeds the mesh silhouette's
848x279 by more than 25% — the key is finding the backdrop, not the figure.
```

**Cause: the re-rolled twin_6 painted a cast shadow on the ground**, and the keying reads it as
figure. 8,991 px keyed outside the silhouette, largest component 4,436 px — a thin horizontal
band under the feet. View 2, the same camera from the other side, has 3,772 px and passes.

## I leaned toward "harmless proxy" and the measurement overturned it

My first reading was that the andon was firing where its stated concern did not apply. The
evidence for that looked good: **keyed area 11.93% of frame against the silhouette's 11.76%** —
near-identical. Only the *bbox* was blown. And a shadow outside the silhouette cannot be
projected, because the projection samples texels from geometry, so there is no surface under it.

**That was wrong, and the right measurement says so.** The twin's keyed mask does not only answer
*where is the figure* — it feeds `distance_transform_edt`, which drives the edge erosion. A
shadow **connected** to the figure inflates the distance-to-edge for everything near the ground
contact:

```
keyed mask components: 86,721 / 2,705 / 2,471    (largest overlaps the silhouette 89.6% of itself)

edge-distance INSIDE the silhouette, with shadow vs shadow removed
  changed > 0.5 px   24,896 of 90,553   27.49%
  changed > 2.0 px   19,236             21.24%
  max change         36.22 px
```

**Over a fifth of the figure's texels get a materially different edge distance**, and the
erosion is what decides whether a texel's paint is trusted. The andon caught a real contamination
pathway into the edge test, not a cosmetic bbox blowout.

Same shape as the errors this repo already catalogues: *matching on one statistic (area) while
the operand that matters (the distance transform) diverges.* Area was the wrong object.

## Where that leaves Arm B

The ruling says **no third roll**, and I am not proposing one. The options as I see them, none
chosen:

1. **Project seven**, dropping view 6, and record the coverage cost. The rejected twin_6 stays on
   disk with both its measurements.
2. **Intersect the twin's keyed mask with the mesh silhouette before the distance transform.**
   Paint outside the silhouette is definitionally irrelevant — no surface is there — so this is
   arguably removing a region that cannot legitimately contribute rather than tuning anything.
   **But it changes `dist_in` at the rim for every twin, so it moves A2's 938,718 and needs its
   own regression before it could be used.** Not a mid-arm change to make quietly.
3. Something else.

**This is a ruling, not an executor's call**, and the reason is the same one that made the last
halt right: dropping a camera is not recoverable by measurement afterwards.

## The 2-camera control DID complete, on the same twins and settings

One variable — camera count — because both runs use the new eight-view twins and identical flags
(`--edge-absolute`, fitted keying):

```
2 cameras (views 0 + 4)   styled 1,050,368 / 2,402,810 valid = 43.7%
                          styled / reachable  1,050,368 / 1,265,391 = 83.0%
                          variance 0.02597   holes 1,352,442
```

**Against A2's 938,718 / 39.1% / 74.2%** — but A2 used the *old* twins and corner-median keying,
so this is not a clean camera-count comparison; it is the new twins' two-camera baseline, and it
is the number the eight-camera result must be read against when it exists.

## Artifacts

`ARMB/stage1_2cam.png` + `_holes.png` + `_styled_mask.npy` · `ARMB/keying_diag_2_6.png` (magenta
= keyed outside the silhouette, cyan = silhouette not keyed) · `ARMB/palette_gate_final.json`
(all eight pass the blob bound after the percentage bound's withdrawal).

**No eight-camera atlas written. No third roll. No guard bypassed.**
