# E07 — advisor ruling at Gate 1

**Date:** 2026-08-05 · **Director's verdict:** *"The images don't look good."* Asked which
defect was driving it, he took **"all of it — the asset is not close"** and ruled the texture
line stopped for a rethink.

---

## The ruling

**E07 closes. Neither arm is adopted, and no further arm is specified on the fill.**

L1 did exactly what it was built to do. Source distance fell 70× (0.17733 → 0.00253, 61
median triangle edges → 0.87), mean fallback went 734 → 0, speckle landed at or below A0 on
all three thresholds, and 10% of turnaround figure pixels moved, concentrated on views 4–6
where dilation carries the surface. **That is not a case for it.** Its Gate 1 failed and its
pre-registered head-zoom condition failed. An arm that improves four numbers and changes
nothing the Director can see has taught us about the numbers.

L2's GPU stays unauthorised, and the instruction conflict the executor correctly refused to
resolve — Amendment 2's *"authorised on substantial movement"* against §5's flattening ANDON —
is **moot**. Both sides of it optimise a step ratio, and a step ratio cannot see the defect.

## Why every number moved and the asset did not

Look at what E07 measured:

| unit | construction |
|---|---|
| blotch count | `\|L − median₅\| > 0.10` — a 5×5 high-pass |
| speckle | the same construction |
| step ratio | median `\|ΔL\|` over 4-adjacent pixel *pairs* |
| flattening guard | `mean(\|L − median₅\|)` |
| atlas variance | global, and indifferent to *where* a colour lands |

Four of the five are high-frequency. The fifth cannot distinguish steel-coloured steel from
skin-coloured steel. Now look at the asset at the Director's zoom: **the blade wears skin
tones in large blocks, the boot and thigh carry scattered gold and green, the forearm has no
material identity.** A large region of the wrong material is *smooth inside itself* and
contributes only its rim to every one of those statistics.

**The instrument was blind to the defect, and nobody checked.** Three experiments were
instrumented around the word *blotch* because E06 recorded the Director saying *"blotches on
his face (that may be warpaint or dirt texture)"* — and a high-pass detector was built for it
without ever confirming the detector fires on what he was pointing at. That is the advisor's
error, and it is a more expensive one than the four gate and pass-condition mistakes before
it, because those were caught by their own experiments and this one survived four.

## The structural read, which is what the verdict is really about

Provenance on the finished C1 asset, measured in E06:

```
TWINS      28.4%      the styled reference, carried faithfully
BRUSH      37.7%      diffusion invention at denoise 1.0 inside the mask
DILATION   33.9%      interpolation
```

**71.6% of the shipped asset is not the reference.** E02, E05, E06 and E07 each improved
*how that 71.6% is filled* — better unwrap, culled surface, surface-aware sources, levelled
seams. **Not one of them reduced it.** And the failure follows it exactly: the front views,
where the twins reach, hold together; view 5 — back three-quarter, where twins never reach —
is where materials dissolve. The executor's own turnaround table says the same thing from the
other side, with views 4–6 moving hardest under a dilation change.

An asset two thirds composed of invention and interpolation does not become the reference by
interpolating better.

## The two-view limit is a hardcoded list, not a property of the route

Checked in source this session, because it decides whether the above is a wall or a lever:

- **`restylize_views.py` takes `--inputs` as an arbitrary list.** It loops over the renders it
  is given, builds each one's control image, restylizes canny-locked, and saves the registered
  figure mask beside each. There is no two-view assumption in it. It was *run* with two.
- **`project_twins.py` hardcodes two** — the `VIEWS` list at lines 132–137, with `--front` and
  `--back` as required arguments.
- Its ownership machinery is **already N-view shaped**: `best_w` / `owner_c` / `sumW` / `sumWC`
  accumulate over `for view in VIEWS`, with `facing^power` ownership and a weighted blend,
  which is why averaging was rejected in the first place.
- And the consistency objection has a tool already in the repo answering it:
  **`ig2mv_licensefree.py` — six consistent views of one character in one pass, 24 s.**

So the single biggest structural fact about this route traces to a two-element list in one
file. That is a finding, not a fix, and it is **not** a claim that more twins will make the
asset acceptable.

## What runs next — a measurement, not an arm

**One free geometric computation decides whether the lever is real**, and it needs no
diffusion, no GPU and no new tool: `project_twins.py` already reports `reachable`, the texels
a camera set can physically see at the projection facing threshold. Compute it on C1's prep
for **N = 2, 4, 6, 8** restylize cameras and report styled-reachable coverage against the
current 28.4%.

E05 measured the analogous ceiling for *brush* cameras on the **uncut** mesh — 8 cameras
reached 34.2% of the hole set, 46 cameras 41.0%. That ceiling moved once culling left the
atlas (C1's brush share is 52.7% from the same eight), so **the twin-projection ceiling on a
culled mesh is unmeasured**, and it is the number that decides this.

- If eight views take reference coverage from 28.4% to most of the surface, the reference /
  invention ratio is the whole question and everything after it is downstream.
- If it plateaus near 40%, then a projection route cannot clothe this figure from its own
  renders, we know that for the cost of one geometry pass, and the rethink is a real rethink
  rather than another fill experiment.

**Explicitly not proposed:** another arm on the fill, another de-blotching metric, or E08's
remeshing. E08 addresses texel density — softness and lack of detail — which is a different
axis from wrong material in the right shape, and chasing it now would repeat this experiment's
mistake at a larger scale.

## Before any metric is used to gate an experiment again

**Validate the instrument against a known-bad artifact first.** Take an asset the Director has
already rejected, and the specific region he named, and confirm the metric fires there. A
metric that does not separate an asset he rejected from one he accepted is not a metric, and
running four experiments on one costs more than every gate error in this repo combined.
