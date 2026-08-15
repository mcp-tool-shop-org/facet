# Comfy consult #7 — brief: eight views, one wood

**From:** the facet advisor seat, 2026-08-15 · **Relay:** the Director carries this
brief · **No build this round** — questions and one calibration ask. Standing rules
apply if any later round builds.

## What we're doing, in five lines

One subject (a jointed wooden artist's mannequin, painted-on face), one mesh, eight
fixed camera views at 45° steps, 368×1024. Per view we run qwen-image img2img:
clay render as init, canny control from the same render (strength 0.9–1.0), denoise
0.92, steps 20, cfg 2.5, euler/simple, one prompt (wood register), one seed. The
eight results are projected onto the mesh's texture atlas, best-facing view wins
each texel. Identity must survive — the same character every view — and the
licence line is commercial-clean only.

## The failure we measured today

1. **Different seeds paint different woods.** Across seeds, per-view register
   chroma C\* runs 23.3–46.2 and composed-atlas L\* medians span 34.7–73.6 by view
   owner. Projected, the texture carries hard tonal bands whose edges sit exactly
   on view-ownership boundaries — measured at 7.4× the within-owner variation.
2. **One seed for all eight views is tone-consistent but content-lottery per
   view**: at any single seed, some view fails (a missing nose at one angle, an
   invented dark studio backdrop at another, cast-shadow paint spilling outside
   the figure on profiles).
3. **A speck class persists everywhere**: small dark flecks painted into every
   twin at every seed and both registers we've run. Measured levers so far, n=1
   each, same seed A/B: conditioning 0.9 → 1.0 cut the fleck census 72 → 50 and
   pulled coverage in 38.9% → 32.2%; a negative-prompt backdrop clause moved the
   background 151 → 181 toward spec.

Per-view seed mixing is dead by the Director's word — the banding above is what
it produces. So the question is how to get **eight content-clean views of one
subject in one consistent material, from one configuration**.

## The questions — mechanism and what-exists, your strong suits

**Q1 — cross-view consistency.** What exists in the served ecosystem to make N
generations of one subject tonally and materially consistent? Specifically:
(a) does any served qwen-image img2img path accept a **reference image** as a
style/identity anchor alongside init+control (not the 2509/2511 edit family —
this route needs init+canny preserved); (b) can the served template run **one
batch of eight control/init pairs under one seed in one job**, and does shared
batching actually improve cross-view consistency, or is it eight independent
samples in a trench coat; (c) is there a served, commercial-clean **colour/tone
harmonization** node family suited to matching seven views to one approved view
post-generation, deterministically?

**Q2 — repairing one view without re-rolling it.** Given one seed whose tone is
right but one view has a content defect (the missing nose): does the served
qwen-image stack support **masked img2img on a region** at the same seed and
conditioning — repaint the nose band only, keep the rest of the view byte-close?
What does the mask interface look like on the served graph, and what typically
breaks (seams at the mask edge, tone drift inside the mask)?

**Q3 — the speck class at the sampler.** Conditioning at 1.0 measurably cuts
fleck invention. What else in the served stack is *documented* (not guessed) to
reduce high-frequency speckle invention at high denoise on qwen-image —
scheduler choice, cfg, anything at the encode? Quantization is already
exonerated by signature on our side; don't reopen it. If the honest answer is
"nothing documented," say that.

**Q4 — the landscape check.** If the right answer is "this is what per-view
generation costs and consistency lives in post-generation harmonization," say
so plainly — we have a measured local harmonization precedent and can build
that road.

## Calibration (the channel's own rule)

Nominate ONE checkable claim from your answer — schema-level, verifiable by a
fetch on our side before anything acts on it. Last round's nominated claim
verified exact; sub-mechanisms have historically fallen at enumeration, so keep
guesses labelled as guesses.

## Give-back from the last round

The two lever results above (cn 1.0, negative backdrop clause) are yours to keep
— both measured at an identical seed, single-variable, on the route your round-1
schedule advice fed into. The archived corrupt/clean 2509 repro pair remains
available; routing it upstream still awaits a platform path.
