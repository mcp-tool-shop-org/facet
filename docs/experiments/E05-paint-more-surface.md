# E05 — Why is three quarters of the asset interpolated?

**Status:** SPEC — ready to run
**Author:** advisor session, 2026-08-04, immediately after E02 was rejected
**Priority:** highest. E02 established the texture stage is not sound; this is the
diagnosis. E03 (head graft) and E04 (ship) both wait on it.

---

## 0. The rules

Unchanged from E02 §0 — no verdicts, no memory writes, stop at gates, judge textures under
FLAT and geometry under `--clay`, state predictions before looking. Read
[E02's ruling](E02-ruling-gate1.md) first; this spec assumes it.

## 1. What E02 established

The Director rejected the asset with every input sound. Three complaints, all matching
numbers measured before he looked: floating artifacts (speckle **2.93%**, worse than the
already-rejected A0's 2.43%), a broken blade (saturation **0.477** vs 0.117), bad hands.

Two structural facts underneath:

- **The brush painted 711,183 hole texels; dilation closed 1,901,890.** Three quarters of
  the finished asset is interpolation.
- **31% of hole texels sit in islands with no styled texel at all**, so their only colour
  arrives across the 4 px gutter from whichever island the packer placed beside them. Atlas
  adjacency is not surface adjacency — that is the artifact mechanism.

## 2. The two levers, and why the second is probably bigger

**Lever A — stop discarding the generator's atlas.** `bake_hero_prep.py:80-81` deletes every
existing UV layer and re-runs `smart_project`. Measured on the same 287,170-face mesh:

| unwrap | islands | faces/island |
|---|---|---|
| `smart_project` (current) | 35,070 | 8 |
| xatlas, native, discarded | **14,010** | **20.5** |

2.5× better, free. But note what it is *not*: a hand-unwrapped character has tens of
islands. Neither unwrapper gets near that, which says the **mesh surface is noisy at
triangle scale** — consistent with only 37% of outward rays escaping, i.e. re-entrant
between adjacent faces. Do not expect the unwrapper to fix this alone.

**Lever B — paint more surface.** Eight cameras closed only **27%** of holes. Each stroke
accepts a texel only where it is a hole *and* faces that camera past `--facing-min 0.25`
*and* survives visibility *and* survives edge erosion. Eight narrow acceptance bands with
overlaps leave three quarters unpainted. This is the number that produced the Director's
verdict, and it is independent of how the atlas is cut.

## 3. Arms

Run against the E02 staged W3, changing one thing at a time. Report the metric table for
every arm.

| arm | change | tests |
|---|---|---|
| **U0** | E02 as shipped | baseline (already measured) |
| **U1** | keep native UVs — skip the delete+`smart_project`, scale head islands on the existing layout, repack only if the head scale demands it | Lever A |
| **U2** | U0 cameras ×2 — 12 yaws at 30° instead of 6 at 60°, same two elevations | Lever B |
| **U3** | U0 with `--facing-min` 0.25 → 0.10 | Lever B, cheaper than U2 |
| **U4** | best of U1–U3 combined | do the levers compose |

U2 costs ~6 extra brush strokes (~6 min). U3 costs nothing. Run **U3 first** — it is free
and it isolates whether acceptance width or camera count is the constraint.

## 4. Metrics — every arm, one table

| metric | why |
|---|---|
| islands, faces/island, atlas coverage | Lever A |
| **holes closed by brush vs by dilation** | the headline — this is what must move |
| islands containing zero styled texels (count and % of hole texels) | the artifact mechanism |
| speckle % (>0.10 from local median) vs A0's 2.43% | the Director's first complaint, measured |
| styled/reachable | comparability with E01/E02 |

**The pass condition is not aesthetic.** An arm is interesting if brush-painted share rises
materially above 27% *and* colourless islands fall. Whether that looks better is the
Director's call at Gate 1, not yours.

## 5. Gates

**Gate 0 — after U3 and U1** (both cheap). Report the metric table only, no renders. If
neither moves the brush/dilation ratio, the levers are wrong and we stop rather than
running U2 and U4.

**Gate 1 — the best arm, finished and packed.** FLAT turnaround plus head close-up beside
**both** the E02 asset and A0, same framing and light. Prediction stated first. The
Director's eye is the verdict.

## 6. Out of scope

Remeshing for a cleaner surface. It is the plausible deeper fix — a chart-based unwrapper
cannot make large islands on a surface that is re-entrant at triangle scale — but it is a
geometry change with its own failure mode (the archived note has voxel remesh stair-stepping
at reachable voxel sizes), and it should not be entangled with a texture-coverage
measurement. If U1–U4 all fail, remeshing becomes the next experiment with a clean question.

Also out of scope: E03 head graft, E04 ship, subject P, any change to the mesh.

## 7. Standards compliance

**PIN_PER_STEP 3** — one change per arm against a staged baseline; all inputs already
pinned by E02. **ANDON 3** — Gate 0 halts the expensive arms if the cheap ones do not move
the ratio. **COMPENSATORS skip** — local writes, one commit, `git revert`, owner the
advisor. **DECOMPOSE_BY_SECRETS 3** — Lever A (atlas) and Lever B (coverage) are varied
independently before being combined. **UNCERTAINTY_GATED_HUMANS 3** — Gate 0 is a numeric
gate needing no Director time; Gate 1 is his. **EXTERNAL_VERIFIER 3** — the pass condition
at Gate 0 is numeric and was written before the arms ran; the aesthetic verdict is the
Director's and the comparison is against two assets he has already judged.
