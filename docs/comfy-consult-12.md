# Comfy consult #12 — answer

**Returned 2026-08-16.** Brief: [comfy-consult-12-brief.md](comfy-consult-12-brief.md).
No generation. No new node named. Graph as specified: **refused**.

## Verdict

This Comfy install cannot carry the brief's AOVs.

- No EXR / raw-float loader. Every IMAGE loader decodes 8-bit sRGB. Callieri's
  Sobel on non-normalised camera Z cannot be built here without crushing the
  discontinuities the mask is for.
- Normal-map nodes here *estimate* normals from RGB; they do not read a Blender
  normal EXR.
- No multi-view warp / camera-matrix resample. "Fill from the other seven" has
  nothing to fill from in the output frame.
- No Euclidean distance-transform. Canny can mark zeros; Callieri wants distance
  from those zeros. Mask grow/blur is an approximation.

**Venue correction:** run the existence proof in the **Blender 5.2 compositor**,
which keeps float EXR and can reproject. If we later hand Comfy *pre-aligned*
8-bit PNG stacks + weight masks (reprojection already done), it can do the final
weighted multiply. That narrower graph was offered, not built.

## Consistency

The specified graph does **not** enforce cross-view consistency. Facing/border
are recomputed per output camera. Cheapest fix named: bake a view-independent
surface-ID / object-space-position pass and pick `argmax(facing)` **once** per
ID, in Blender.

## Licence notes (agent, unverified here)

Core Comfy nodes GPL-3.0 (commercial *use* is fine; redistribution is the
question). WAS Suite MIT. Image-Filters pack and essentials: **licence not
stated** — do not ship on a "probably MIT." No new install proposed.

## What a clean 2D result would and would not prove

A Blender-compositor composite proves the twins *blend* under Callieri weights.
It does not prove they *project* onto the mesh. A dirty 2D result is only
informative if the depth/facing/ID passes stayed exact float — which is why
doing it in 8-bit Comfy would have been a false negative against the twins.
