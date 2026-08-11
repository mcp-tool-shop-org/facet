# E32 Gate 0 — predictions, registered before the thing each one predicts

**Seat:** executor · **Written:** 2026-08-10 · Spec:
[E32-armature-mark-through-the-route.md](E32-armature-mark-through-the-route.md)

Predictions are registered in two batches because they predict two different things and the
first batch's *operand* is produced by the second thing. Each batch states exactly what had
been seen when it was written. **P4 predicts what the segmenter does, so it is registered
before the segmenter is run. P1–P3 predict what the reconstructor does, and their operands
(opening count, limb width) come from the segmenter's output — so they are registered after
the plate is measured and before TRELLIS is run.**

Subject: `E:\AI\training\facet_E32\armature_mark_clay.png`,
sha256 `ade49b607c6e5872f279bb42f3d78939d03a0a5a167a418567ae7955f6e0f9a1`, 2048×2048 RGBA.

---

## Batch 1 — P4, the key

**Registered:** before any segmenter was run. **Blind to the segmenter's output: YES.**

### What had been seen when this was written

1. The plate at 768 px (a downscale, my own, for composition only). It is a wire-armature
   figure: an oval head cage, a torso X-brace, pelvic loops, outstretched arms with ball
   joints, ring feet. The background is **not** the "grey gradient" the dispatch describes —
   the upper two thirds are a soft light-grey field and the bottom third is a **hard dark
   band**, a floor/horizon, with a step-ish transition.
2. `e32_plate_geometry.py` on the plate: alpha channel **present but constant 255**
   (`frac_below_255 = 0.0`); fitted-background luma span **95.82** (top row mean 136.68,
   bottom row mean 58.19); residual p50 **0.0302**, p99 **0.1836**.
3. That the two-sided key is **contaminated** on this plate — at tol 0.06 it returns
   835,526 px with a bbox of the full 2048 px frame width and a median width of 350 px.
   That is the dark band, not the figure. **No figure quantity is taken from it.**

### The mechanism, read rather than assumed

The spec's premise 5 says `pipe.run` "runs `rembg`". Read at
`trellis2/pipelines/trellis2_image_to_3d.py:127-160`, the actual chain is:

```
mode == 'RGBA' and not np.all(alpha == 255)  ->  has_alpha    # OURS: all 255 -> False
scale = min(1, 1024 / max(size))             ->  LANCZOS resize 2048 -> 1024
rembg_model(input)                           ->  trellis2/pipelines/rembg/BiRefNet.py
bbox = argwhere(alpha > 0.8*255)             ->  SQUARE crop about that bbox
output = rgb * alpha                         ->  PREMULTIPLIED; background becomes black
```

Two corrections to what "runs rembg" implies, both load-bearing for this prediction:

* **The segmenter is BiRefNet at 1024×1024** (`transforms.Resize((1024,1024))`,
  `BiRefNet.py:16`), not the PyPI `rembg`/u2net-at-320 I would otherwise have reasoned
  about. BiRefNet is a high-resolution dichotomous-segmentation model built for fine
  structure. The plate is downscaled to exactly 1024 first, so **the segmenter sees it 1:1**
  — no resampling loss at its input.
* **The output is premultiplied.** A partially-transparent pixel is not merely masked, it is
  *darkened toward black*. Thin members carried at partial alpha lose luminance as well as
  coverage, and the reconstructor never sees the difference between "thin and faint" and
  "dark".

Our plate's alpha is constant 255, so `has_alpha` is False and **the segmenter does run**.
That much is settled by code, not predicted.

### P4 — predictions

| # | Prediction | Band |
|---|---|---|
| P4a | The mask's bbox does **not** span the frame — the dark band is not keyed as subject | bbox width < 90% of frame |
| P4b | The mask's area, as a fraction of the 1024 frame | **2%–8%** |
| P4c | Enclosed openings survive segmentation at min_area 64 (1024-space) | **≥ 8** |
| P4d | The thinnest surviving member's width in the mask, 1024-space | **2–5 px** |

**Reasoning.** P4a/P4b: a single centred salient object on a smooth ground is BiRefNet's
canonical case, and the figure is lighter than every background pixel (subject ≈230 against a
fitted background whose maximum is ≈148). I expect the dark band to be rejected outright —
it is ground, not object, and this is exactly the discrimination a saliency model makes and a
quadratic key cannot. P4b's band comes from the 768 px view: the figure spans roughly half
the frame in each dimension but is a *lattice*, so its fill is low.

P4c/P4d are the ones I hold least confidently and they are where I expect to be wrong. The
ring feet and the hand tubes read at ~2–4 px in the 1024 space, and the premultiply punishes
exactly those. **If a prediction misses here, the mechanism to suspect is the premultiply,
not the segmenter's coverage.**

**Blind:** yes, for all four. Nothing from BiRefNet had been run or read.

---

## Batch 2 — P1, P2, P3, the reconstruction

**Registered:** after the plate measurement, **before `mesh_character.py` was invoked.**
**Blind to any reconstruction output: YES** — no mesh existed on disk when this was written.

### The plate's own geometry, measured — these are the operands

From `e32_plate_geometry.py --mask <segmenter's own mask>`, at **route scale (1024×1024)**,
which is the space the reconstructor operates in. The key is not in this path at all; the mask
is BiRefNet's, i.e. the route's own answer to "where is the figure".

| quantity | value |
|---|---|
| mask area | 26,516 px, **2.53%** of the route frame |
| figure bbox | 493 × 499 px |
| **fill of bbox** | **10.78%** — a lattice, not a figure |
| width min / p01 / p05 / p50 / p95 / max | **4 / 6 / 8 / 10 / 26 / 28 px** |
| width band share 0–4 px | **0.0%** — nothing is thinner than 4 px |
| width band share 8–16 px | 67.8% |
| **openings** at min_area 1 / 16 / 64 / 256 / 1024 | **22 / 22 / 21 / 16 / 2** |
| largest opening areas | 1301, 1206, 911, 888, 888, 721, … |

The opening curve is flat from min_area 1 to 16 (**22 at both**), which says the mask carries
**no speckle at all** — the count is a property of the figure, not of a threshold. In plate
space (2048) every width doubles: min 8, p50 20, max 56 px.

### The mechanism, read rather than assumed

`trellis2_image_to_3d.py:541` —
`ss_res = {'512': 32, '1024': 64, '1024_cascade': 32, '1536_cascade': 32}`.

**`1024_cascade` samples the sparse OCCUPANCY structure at 32³**, then
`sample_shape_slat_cascade` refines shape 512→1024 *within the voxels that structure
occupied*. Occupancy decides topology and the cascade cannot re-open a cell the 32³ grid has
filled. The conditioning image is a square crop tight to the figure's bbox (496×496), so the
figure spans essentially the whole grid:

* a p50 **10 px** tube is 10/496 of the frame = **0.65 voxels** at 32³;
* the thinnest **4 px** member is **0.26 voxels**;
* the median kept opening (~256 px area, ~18 px across) is **~1.2 voxels**;
* the largest opening (1301 px, ~40 px across) is **~2.6 voxels**.

Tubes are sub-voxel and the gaps between them are one to three voxels. That is the whole
basis of P1 and P3 below.

### Units, chosen to be scale-free

A mesh render and a plate are not the same size, so raw pixel widths and raw `min_area`
thresholds are not comparable between them. Both quantities are therefore normalised **by the
figure's own bbox**, which both artifacts have:

* **width** as a percentage of bbox height. Plate p50 = 10/499 = **2.004%**; plate min =
  4/499 = 0.80%.
* **openings** counted above **0.026% of bbox area** (the plate's own min_area 64 against its
  246,007 px bbox), giving the plate **21**.

The mesh side is measured from an **exact raycast silhouette** (`silhouette_masks.py`), never
from a keyed clay render — E01's law, and the same reason the plate side uses BiRefNet.

### P1, P2, P3 — predictions

| # | Prediction | Band |
|---|---|---|
| P1a | Crossings (torso X-brace, ball joints) come back **bridged into webbing**, not as separate tubes | qualitative, judged on the Gate 0 sheet |
| P1b | Openings preserved in the front view, above 0.026% of bbox area, against the plate's **21** | **0–6** |
| P2a | Shell count (`mesh_stats` vertex-components; family table: character 40–191, ship 237–512, dragon 9–12) | **5–60** |
| P2b | `mesh_topology`'s nested-wall leg | **DECLINES to compute** |
| P3 | Front-view p50 width as % of bbox height, against the plate's **2.004%** — i.e. the member **thickens** | **2.6%–6.0%** (1.3×–3.0×) |

**Reasoning, and which of these I hold least confidently.**

P1b and P3 share one mechanism: a 0.65-voxel tube separated by 1.2-voxel gaps cannot be
represented by a 32³ occupancy grid, so I expect the grid to round tubes up to a full voxel
and to close most cells. P3 therefore predicts a *direction* — **thickening, not thinning** —
which is the part that matters; a collapse to ribbons would falsify it as surely as fidelity
would. Only the largest cells (the head cage interior, the two foot rings, the biggest
X-brace triangles) are plausible survivors, which is where P1b's upper bound of 6 comes from.

**P1b is the one I hold least confidently**, and the reason is that the arithmetic above
treats a generative sampler as a rasterizer. The sparse-structure model has learned priors
and the shape latent decodes a continuous field inside each occupied voxel; it may carve
sub-voxel detail the naive count says is impossible. **If P1b comes back at or near 22, the
lesson is that voxel arithmetic does not bound a learned occupancy prior, and that is a more
useful result than a hit.**

P2b predicts a decline for a *different reason* than the character class does: characters
decline because a second manifold piece is shredded below the 1% floor, whereas a sub-voxel
tube has no room for an inner wall at all. **The leg cannot distinguish those two causes**,
so a DECLINE here is uninformative about solidity either way, and I am recording that in
advance rather than reading a decline as evidence of solidity afterwards.

P2a is a wide band and I expect it to be uninformative — but E29's P4 was uninformative *and
wrong*, so it carries a falsifier like the rest.
