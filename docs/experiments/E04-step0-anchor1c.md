# E04 Step 0 anchor 1c, on the replacement instrument — 1 px. HALT for a ruling.

**Executor session, 2026-08-04.** Built `tools/diagnostics/e04_frame_agree.py` as Ruling 10
specified: `silhouette_masks`' raycast against a raycast cast under `turn_render`'s own camera
parameters. Same mesh, same triangles, same frame — **geometry against geometry, no threshold
anywhere**. Bound 0 px, pre-registered by the advisor, not chosen here.

## Result

| subject | frame | fit-axis | view | differing px |
|---|---|---|---|---|
| **galleon 00006** | 1066 × 1024 | width | **1** | **1** |
| galleon 00006 | 1066 × 1024 | width | 7 | **0** |
| **W3 (control)** | 752 × 1024 | height | 0 | **0** |
| W3 (control) | 752 × 1024 | height | 4 | **0** |

**Worst 1 px against a bound of 0. Halting, per the pre-registered reading.**

## Which of the three readings this is — decided by the numbers, not by preference

Ruling 10 pre-stated three: 0 px passes · a handful of boundary pixels in uniform scatter is
float edge-ordering, *report and halt* · a structural offset is the gate's real prey.

**This is unambiguously the second.** View 1: hit 321,219 against mask 321,218 — **one pixel**,
0.0003% of the figure.

| evidence | value | reading |
|---|---|---|
| centroid shift | **(−0.0004, −0.0009) px** | no displacement — a structural offset moves the centroid |
| hit bbox vs mask bbox | **716 × 849 vs 716 × 849** | identical to the pixel on both axes |
| the other view | **0 px** | a convention error would hit both views |
| the character control | **0 px on both views** | the instrument can return 0, and does |

For scale, the failure this anchor exists to catch measured **4.68%** — a 34 × 42 px bbox gap.
This is one pixel with the bboxes identical and the centroid stationary to four decimal places:
a single boundary ray landing on the far side of a triangle edge in one implementation and the
near side in the other.

**The control matters most.** A check that returned "close enough" on everything would be the
gate that cannot fail — this repo's own named trap. It returns **exactly 0** on both character
views, so 1 px on one ship view is a real, if tiny, disagreement rather than a tolerance.

## What I am not doing

**Not tuning.** No bound of 1, no `>= 1` allowance, no rounding. The advisor's instruction for
this reading is *"report the count, halt for a ruling, do not tune"*, and the reason I refused
threshold 70 on the withdrawn anchor applies unchanged: I now know what value would pass, and
that is exactly why I must not pick it.

**Not chasing the pixel either.** Identifying which triangle edge it sits on would take
minutes, and it would be work aimed at making a fired gate go away. If the ruling wants it
located, that is a different instruction.

## State

- Step 0 item 1 (fit-axis): implemented; **character anchors pass with 0 differing pixels on
  renders, masks, and now the geometry check**; ship anchor at 1 px awaiting a ruling.
- Items 2 (cull superset), 3 (emit framing), 4 (profile check): **not started.**
- Arms G7 and T: **not started.** No generation, no spend.
