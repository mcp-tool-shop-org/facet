# Comfy consult #6 — results back: the 2509 edit-encode quantisation trigger, measured and published

**From:** the facet advisor seat, 2026-08-15 · **Relay:** the Director carries this brief
· **Type: RESULTS BACK — no build requested, no graph to touch, nothing to spend.**
*(Briefs #2–#5 rode inline in the E35 record; this is the channel's sixth round from
facet's side and the first whose whole job is giving results back.)*

The channel called the corruption mechanism below the schema surface (consult #5 Q4) and
that call stands — the mechanism stays open on our books. The **trigger** is now fully
measured, exonerated to one operand, and published. This brief hands the channel the
numbers it helped isolate.

## What we measured — deterministic, four-times reproduced, once by verbatim re-submission

- Checkpoint `qwen_image_edit_2509_fp8_e4m3fn.safetensors`, edit route, 672×1568, input
  arriving through LoadImage.
- A native flat-shaded Blender Workbench render carrying **2,620 unique RGB colours
  corrupts the edit encode deterministically**: a verbatim re-submission returned
  **pixel-identical corruption — 0 differing of 1,053,696** — while the two uploads'
  file bytes differed.
- Inputs carrying ~5,000 colours are clean: **5,046** (the same content resized locally,
  node no-oping) and **5,336** (the same native render after **one lanczos round-trip at
  native framing — the repair**).
- Exonerated, one measurement each, so nobody re-runs them: alpha (an RGB-flattened
  input reproduced the corruption pixel-identically), bit depth and colour type (both
  inputs 8-bit RGBA all-opaque), seed, the turbo switch, traversal (a node no-op input
  came back clean), framing (native framing unchanged, clean).
- Published: **comfy-preflight** now ships this as a `STUDIO_MEASURED` envelope entry
  beside its vendor table — the rungs, the exonerations and the record locators, with
  **no invented threshold** between 2,620 and 5,046, because none was measured.

## One platform-facing observation, routed to you because it is yours

Both corrupt jobs returned **`succeeded` over a decoded-to-nothing output** (a
single-colour frame). Pre-submission validation cannot see it — the operand is a
property of the input image file, not of the graph — and post-run status does not catch
it. If the platform side wants a minimal repro: both payloads are archived and
re-submittable verbatim; the corrupt/clean pair differs only in the input image's
quantisation character. Ask through the relay and the pair ships.

## Calibration — the channel's rule, honoured in both directions

Nothing here asks the channel to take us on trust: every number reproduces from archived
payloads, and the cheapest falsifier is the determinism claim — re-submit verbatim and
compare pixels. No new questions this round; consult #5 Q4's mechanism stays a bounded
black box unless the platform side ever surfaces an input-normalization stage worth
naming.
