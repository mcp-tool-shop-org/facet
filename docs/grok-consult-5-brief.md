# Grok consult #5 — build round 2: the S3 existence proof

**2026-08-16, facet advisor seat. BUILD.** Prior rounds: briefs 1–4; round 4 produced
`tools/callieri_border.py`. Companion dispatch this session:
`docs/experiments/E45-warp-and-aov-kickoff.md` (a local seat is emitting the real-data
bundle and finishing the warp measurement while you build).

*Everything below the line is the paste block.*

---

# Five for five. Your border module is in our tree. Here is S1, a new lead, and the big build.

## Status since #4

**Your calibration claim held — that is five for five.** The self-test printed
`0.6666666666666666` exactly, first run. `callieri_border.py` sits in our tree at v1.0.0
with eleven hermetic tests, all green. Nothing in it was modified.

**S1 is run, and the mesh-soup branch is dead as an appearance mechanism.** We welded the
shipped mesh in Blender (41.1% adjacency → 99.2%, 146k components → 271), let normals come
from restored connectivity, and clay-rendered welded vs shipped: **1,034 px differ out of a
151,705 px figure, max channel delta 3.** Both renders smooth. The GLB carries explicit
vertex normals, so the soup never touched shading. The weld itself remains real and useful
(cone clustering on the welded mesh: 2,654 charts vs 146,462) — it is just not the look.

**S2 we are skipping for now** — with S0 and S1 both negative it is diagnostic-only, per
your own cheapest-first logic.

**A new lead, measured after your plan was written — local twin-to-mesh warp.** Global
registration is fine (IoU 0.9203, centroid offset 2.88 × 2.60 px, so "twins register at
(0,0)" was true and hid this). But per-tile offsets on one view (yaw 45, silhouette-based)
span −8..+6 px in x, −8..+8 in y, std 3.71 / 4.09 — a warp, not a shift — and several tiles
pin at the ±8 search limit, so true offsets are larger. Why it fits where everything else
died: our E41 measurement put defect texels a median **0.439 px** from a material boundary.
A 4–8 px local displacement puts a sample across a material boundary **while depth stays
smooth** — which is precisely the blind spot your own module's docstring declares. It would
explain why blending can't fix it (every view samples the wrong place), why resolution
can't (a sharper twin sampled 6 px off is still wrong), and why the twins look clean while
the asset doesn't. Status: one view, silhouette-only, window-pinned, instrument being
rebuilt — a live hypothesis, not a finding. A seat is finishing it (8 views, wider window,
interior correspondence) while you build.

**Also dead since your plan:** the blend-variant sheet (structurally incapable — each
candidate panel was one render with only 298–813 flagged pixels rewritten; the Director's
"they're all the same image" was literally true).

## THE BUILD — the S3 existence proof, end to end

The question S3 answers: **can the eight plates compose into one consistent surface at
all?** If the composite is clean, the plates are fine and our 3D path degrades them. If it
is blotchy with high cross-view disagreement, the sources are inconsistent (the warp lead
strengthens). If it is blotchy with LOW disagreement, the plates share the defect. Your
module is the instrument that separates those three worlds — which no measurement this
month has managed.

Build **one standalone Python module** (working name `s3_composite.py`) that, given the
8-view bundle below, emits **two stills of any target view plus diagnostics**. Pure
functions of arrays; we wire file I/O on our side.

### The scene and the input contract, exactly

Eight orthographic views of one figure. Real frames are H=1024 rows × W=752 cols; your
self-test may synthesise any size. Canonical world frame, Z up. Figure's largest bbox axis
≈ 0.9969 world units; typical figure occupies ~151,705 of 770,048 px.

Per view `v` (numpy, row-major):

| name | dtype/shape | meaning |
|---|---|---|
| `twin` | float32 (H, W, 3), [0,1] | the painted plate, sRGB |
| `depth` | float32 (H, W) | camera-axis depth of first hit, **+inf background** (your convention from #4) |
| `sil` | bool (H, W) | True where surface exists (raycast, not keying) |
| `pos` | float32 (H, W, 3) | world position of first hit; NaN background |
| `normal_world` | float32 (H, W, 3) | unit world-space surface normal at hit |
| `surfid` | int32 (H, W) | **global surface ID** (atlas texel index), stable across views; −1 background |
| `weight_border` | float32 (H, W) | your `border_weight(depth, sil)`, precomputed by us |
| `reject` | bool (H, W) | your `mixed_depth_reject(depth)`, precomputed by us |
| `flow` | float32 (H, W, 2), optional | additive pixel offset applied when sampling THIS view's twin: sample at `(px + flow_x, py + flow_y)`. Defaults to zeros. **The warp hook** — if the seat's measurement lands, its field goes here, and the A/B (flow off vs on) becomes the warp hypothesis test in composite space. |

Per-view camera dict: `{right, up, dtc, bmid, h_ext, v_ext, W, H}` — unit world vectors
`right`, `up`, `dtc` (direction from scene TO camera), centre `bmid` (3,), full frame
extents `h_ext`, `v_ext` in world units. The projection contract (our emitter guarantees
the AOVs satisfy it; your module must use exactly this):

```
px(P) = ((P − bmid)·right / h_ext + 0.5) · W − 0.5
py(P) = (0.5 − (P − bmid)·up / v_ext) · H − 0.5
depth(P) = −(P − bmid)·dtc
```

Facing of a surface point P with normal n under view v: `n·dtc_v`. Exponent is a module
parameter, default 6.0 (matches Meta 3D TextureGen §4.2.1's α=6, and our shipped
`facing^6.0`); we want 2 and 4 runnable.

Visibility of P in view v: project by the contract; inside frame, `sil_v` true at the
sample, `reject_v` false, and `|depth(P) − depth_v(px, py)| ≤ τ` — **τ must not be a fixed
global constant** (our law: a global constant must not govern a local feature; our sword
blade is ~15 px wide and thin structure is where a fixed τ breaks). Derive it locally —
your `relative_jump` machinery already has the right instincts. State its basis in the
docstring.

### The two stills

**A. View-dependent composite of target view t.** Per-pixel weighted blend across views:
weight = `weight_border` × facing^α × visibility, sampled at the reprojected position (+
flow). **Primary-plate-first**: the highest-facing valid plate leads; the others fill only
where the primary's weight falls below a floor you choose and expose. You spec the exact
policy; write it in the docstring.

**B. View-independent composite of target view t.** ONE global assignment first:
`owner(surfid)` = argmax over views of that surface point's weight, computed once for the
whole surface — then every pixel of ANY target renders its surfid's owner. **The property
this still exists to prove: two different targets agree at every shared surfid by
construction.** Eight independently-beautiful mutually inconsistent stills fail; consistency
is a surface field, not a per-still choice. That sentence is the whole reason S3 exists.

**C. Diagnostics, same call:** per-pixel owner map (int8); per-pixel **disagreement map**
(weighted dispersion of candidate plate colours BEFORE compositing — the number the warp
would inflate, and the discriminator between the three worlds above); coverage/fallback
mask (pixels with no valid source); per-view contribution shares.

We blend in float sRGB because that is the space our shipped pipeline blends in and the
proof must be comparable to it. If you think linear-light changes the proof's *meaning* —
not just its polish — argue it, don't silently switch.

### The self-test, hard requirements (our laws, same as #4)

Synthetic scene with answers known by construction (a textured box or sphere, 3–4 ortho
views, analytic ground truth). Legs, each able to fail:

1. **Reprojection exactness** — view A's plate reprojected into view B recovers ground
   truth within a stated bilinear tolerance.
2. **Occlusion** — a constructed occluder zeroes the hidden plate's contribution; test the
   visible side too.
3. **The consistency theorem** — build plates that deliberately DISAGREE per view; the
   view-independent stills from two different targets must agree at every shared surfid. A
   per-target argmax (the bug class this requirement bans) picks different owners per
   target and fails this leg — that is what makes it a real check. Also assert the
   view-DEPENDENT stills DO differ somewhere on the same fixture, or leg 3 cannot fail.
4. **The warp leg** — inject a known ~6 px local warp into one synthetic plate: the
   disagreement map must fire in the warped region and stay quiet elsewhere; composite with
   the true `flow` handed back must recover the unwarped result within tolerance.
5. State each output's **yes/no interval** — what it reads when the answer is unambiguously
   yes and unambiguously no. We have predicted outside an instrument's range before and it
   cost an arc.

### Constraints

numpy + scipy only (PIL for debug PNGs in the self-test); Python 3.13, headless; MIT
header; pure functions, no I/O in the core, no filesystem assumptions, no hidden state;
ASCII output. **Say in the docstring what this cannot see**: a defect all eight plates
share identically produces zero disagreement and a clean-looking consensus of wrong paint —
this module proves the plates CAN or CANNOT compose, never that they are right.

### Argue with the brief — the protocol's proven use

- Is per-surfid argmax facing the right global field, or should ownership be smoothed over
  the surface (your Waechter seam-level point from #1)? If smoothing, where does it live
  without reintroducing per-still choice?
- Does the disagreement diagnostic subsume the warp seat's instrument in composite space,
  or are they measuring different things? Two levers that are secretly one is a mistake you
  already caught us in once (#4, border vs mixed-depth).
- Anything in the contract above that assumes its own answer — say so. Your critique of
  brief #3 ("the plan only tests unwrappers while calling the causal link unproven") was
  the turning point of that arc.

## Calibration

Same standard, sixth round. Nominate **one checkable claim about your implementation** — a
specific value a named self-test leg must produce on a specific synthetic input — that we
verify by running it before trusting the rest. Yours have held five times, and each one
changed what we did.
