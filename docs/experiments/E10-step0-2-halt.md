# E10 Step 0.2 — the contact mask is built; anchor C FIRED. Two findings, neither ruled.

**Executor session, 2026-08-05.** Run under [E10 Ruling 3](E10-ruling.md), which cleared
Step 0.2 at the placed line. Written after the work. **The gate fired and I stopped there.**
Nothing was retuned.

Tool: [`tools/e10_contact_mask.py`](../../tools/e10_contact_mask.py) · diagnostic:
[`tools/diagnostics/e10_offsurface.py`](../../tools/diagnostics/e10_offsurface.py) ·
artifacts in `E:\AI\training\facet_next\E04_stroke\e10_contact\`.

---

## The run

```
[line] waterline_z = -0.43095 (profiles/ship.json, canonical mesh frame)
[A] texel z [-0.479557, +0.480133] vs mesh z [-0.479558, +0.480192]  (d_lo 1.17e-06, d_hi 5.93e-05)
[mask] 101030 contact texels of 3111817 uv-valid (3.247%)
[B] recomputed from a fresh read: identical
[B] contact_mask.npy sha256 0ad15bd3cfadfbd717baa306c16bfeee895f6672adf4c7b6004d0e50484097c9
[C] 98.5222% of 101030 projected contact texels land inside the exact silhouette
    projected rows 896.0-939.3; the placed line is row 896.0
ANDON C: contact texels project outside the figure. HALT.
```

| anchor | verdict |
|---|---|
| **A — frame** | **PASS.** `pos.npy` reconstructs the mesh's canonical z to 1.17e-06 / 5.93e-05 |
| **B — stability** | **PASS.** Pure function of (mesh, plane); recomputed from a fresh read, identical |
| **C — projection ⊆ silhouette** | **FIRED.** 98.5222% against the anchor's 99.99% |
| **D — end-to-end render** | **not reached** |

The mask's vertical placement is exactly right: projected rows run 896.0–939.3, from the
placed line to the keel, and the band is 3.247% of the uv-valid atlas.

## A third frame, found on the way in

`pos.npy` is in **neither** of the two frames Ruling 2 named. It is the canonical frame's
permuted-but-unnormalised bbox (`meta.lo/hi`) remapped **per-axis into the unit cube** —
its values are in [0,1], not world units. So the pipeline carries **three** things called
"position": the GLB's own Y-up coordinates, the canonical `load_scene()` frame that every
`cam.json` speaks, and the bake's unit cube. The conversion is anchored (A) rather than
assumed, and documented at the top of the tool.

## Why C fired — decomposed, because a failure's signature names its cause

1,493 texels project outside the exact silhouette. They are **two populations**, not one:

| population | count | share | distance to the mesh surface |
|---|---|---|---|
| on the surface, at the silhouette rim | 558 | 37.4% | ≤ 1 px |
| **not on the mesh surface at all** | **935** | **62.6%** | median **46 px**, max **144 px** |

### Finding 1 — the anchor cannot be passed by the geometry it validates

The control that decides this: run **the mesh's own vertices** below the placed line
through anchor C's exact check.

```
[control] 20387 vertices, 99.4506% inside, 112 outside, every miss at 1.00 px
```

Rounding a projected position to the nearest pixel centre and testing membership in a
**binary** raycast mask puts boundary points one pixel out. The geometry the anchor exists
to validate scores **99.4506%** against a **99.99%** bar. The threshold is unreachable in
principle for a structure that hugs the silhouette — which the contact band, at the hull's
foot, does by construction.

This is the repo's own gate lesson arriving again: *before promoting a number to a halt,
ask what else moves it besides the thing you are watching.* Reported, **not retuned** —
re-deriving a threshold while looking at the result it would judge is the one move that is
always wrong.

### Finding 2 — 2.5% of the prep bake's uv-valid texels are not on the mesh

The larger population is not about the anchor at all. Measured across the whole bake
(200,000-texel sample, distance via the same raycasting scene the pipeline uses):

```
[bake] 3111817 uv-valid texels, 200000 sampled
       median distance to surface 6.73e-06 (0.006 px)
       OFF-SURFACE (>1 px): 2.5065%   (>5 px): 2.0940%   max 147.4 px
```

The bulk of the bake is exactly on the surface — median 0.006 px. But **2.51% of uv-valid
texels carry a position that is not on the geometry**, and 2.09% are more than 5 px off.
The contact mask's own rate is 2.6477%, i.e. it **does not concentrate the defect** — it
inherits the bake's.

`mask.npy` says these texels are uv-valid; `pos.npy` gives them a position; nothing on the
route has ever asked whether that position is on the mesh. This is the same family as E08
A27 — *paint on no surface* — one layer down: **a coordinate for a texel that has no
surface to have a coordinate on.**

## When you fix a root cause, find its other consumers

`pos.npy` + `mask.npy` are read by **the shipped route itself**, not only by diagnostics:

| consumer | role |
|---|---|
| `project_twins.py:162` | stage 1 — the multi-view projection |
| `texpass_iter.py:239` | `commit` — every brush stroke |
| `texpass_finalize.py:82` | the flood that filled 56.24% of the accepted atlas |
| `resample_atlas.py:35`, `bake_hero_fuse.py:62` | atlas resample / fuse |
| `e08_ceiling.py:48`, `e08_acceptance.py:86` | **the 42.72% ceiling and the acceptance figures** |
| `e04_stroke_cameras.py:120`, `brush_reach.py:40`, `commit_funnel.py:57` | the stroke derivation |
| `texel_provenance.py:72`, `texpass_metrics.py:118`, `e04_blotch.py:152`, `e04_seam_sources.py:67`, `e07_gate0.py:128`, `e07_l1_andon.py:41`, `e07_l2_bound.py:78`, `texpass_thin_mask.py:109` | diagnostics |

**I am not claiming any of those numbers is wrong.** Most of them use `pos.npy` for
nearest-neighbour queries in texel space, where a 2.5% off-surface population may cost
nothing, or may cost something small and bounded. What I can say is that **the property has
never been measured**, it is inherited by everything on the list, and whether it matters at
any given site is a question with a cheap measurable answer per site. That enumeration is
for the advisor to prioritise, not for this session to start.

## What is NOT established

- **Where the off-surface texels come from.** UV gutter/dilation padding in the bake is the
  obvious suspect and it is *not* verified here; `bake_hero_prep.py:458` is where the map is
  written and nobody has read it against this question.
- **Whether the accepted galleon or W3 is affected in any visible way.** Both are Gate-1
  accepted on the Director's eye, and nothing here re-opens that.
- **Anchor D.** The end-to-end render check — the one that would catch a wrong axis or a UV
  mismatch — never ran, so the mask is *anchored on frame and stability only*.

## What the ruling faces

Two independent questions, stated without a recommendation:

1. **The anchor's form.** It tests rounded-pixel membership in a binary mask, and its
   control scores 99.4506%. Restating it against the property it means to test — *does the
   contact mask reach beyond the surface* — is a different check from the one written.
2. **The off-surface population.** E08 A27's precedent is on the record: intersect the mask
   with where surface exists before using it. Whether E10 adopts that, and whether the
   finding travels to the consumer list above, is a ruling with a scope much wider than
   this step.

## Standards compliance (this step)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | `waterline_z` and its frame read from `profiles/ship.json`, never typed; the mask's sha256 recorded; the unit-cube conversion documented and anchored |
| ANDON_AUTHORITY | 3 | four anchors, each with a describable non-zero; C fired and the run stopped inside the tool. The diagnostic was written as a **separate file** so the fired gate is untouched — adding a diagnostic to a gate after watching it fire is how a gate becomes whatever passes |
| NAMED_COMPENSATORS | 3 | writes only into `e10_contact/`; undo is deleting it; the accepted base asset is neither written nor read |
| DECOMPOSE_BY_SECRETS | 3 | the line is subject data in the profile, the mechanism is in the tool, the frame convention is named at both ends |
| UNCERTAINTY_GATED_HUMANS | 3 | halted with both questions stated, the control that prices the first, and no recommendation |
| EXTERNAL_VERIFIER | 3 | the failing anchor was diagnosed against an independent object — the mesh's own vertices — rather than against the mask that failed it |
