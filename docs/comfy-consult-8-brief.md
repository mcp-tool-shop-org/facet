# Comfy consult #8 — brief: what generation stack actually builds this character?

**From:** the facet advisor seat, 2026-08-15 · **Relay:** the Director carries this
brief · **No build this round.** Standing rules apply if any later round builds.
This is the landscape question asked plainly, with three days of measured tuition
attached so nothing is re-derived.

## The mission, stated fresh

One canonical character — a jointed wooden artist's mannequin with a painted-on
face — one mesh (ours, clean, Director-picked), and the need: **a textured 3D
asset whose eight-view turnaround is defect-free and reads as one material**, with
identity first-class (the same man every view) and every component
commercial-clean. The consumer binds identity downstream in reference kits,
sprite cells and video start-frames, so "close enough per view" is not the bar —
the composed asset at full zoom is.

## The tuition — what we measured so you don't guess

1. Per-view qwen-image img2img + canny (our recorded route) is the best thing we
   have measured AND structurally incoherent across views: different seeds paint
   different woods (composed L\* medians 34.7–73.6 by view owner); one seed is
   tone-consistent but a content lottery per view; the register prior paints
   dark flecks at every seed and both registers we ran.
2. Masked same-seed repair works mechanically (your SetLatentNoiseMask guidance
   was exact — including that the unmasked region restores to the INIT, which we
   learned the hard way) — and the composed, repaired set **still failed the
   Director's eye**: face features painted on non-face views, repair boundaries
   visible.
3. Your ColorMatch recommendation carried a measured limit we're handing back:
   view-to-view transfer is fine, but region-level matching **washes drawn face
   features while its own metric improves** (ΔE 17.61 → 3.50 as the face faded).
   A metric that improves while the artifact worsens is a recurring theme on
   this subject.
4. Your prior landscape verdict — cross-view coherence from independent per-view
   samples is structural, not a missing config — is now confirmed at the asset
   level, at the Director's eye, at full cost.

## The questions

**Q1 — the untested lever.** `QwenImageDiffsynthControlnet` (the model-patch
reference anchor) is schema-verified on our side and unmeasured on this subject.
What is actually known about its coupling strength for material/identity
consistency across independent generations? Any documented multi-view usage
pattern, or is it single-image lore only? A guess labelled as a guess is fine.

**Q2 — multi-view-native generation.** What is SERVED today that generates N
views of one subject in ONE pass with real cross-view coupling — MV-Adapter
class, any multiview-capable base, or **a video model as the coupling mechanism**
(an orbit/turnaround clip of a provided subject is eight coupled views by
construction; we can extract frames). For each candidate: identity input story
(image ref? mesh conditioning?), license bucket, and whether it can honor our
mesh's silhouette (we hold exact per-view controls and masks).

**Q3 — mesh-native texture, revisited.** Last check (your consult #5), every
served partner texture path was identity-blind by schema — three vendors, zero
reference-image inputs — and the OSS routes we excluded carry their reasons
(Hunyuan3D-Paint license-void in our jurisdictions; MVPaint/TEXGen unlicensed;
nvdiffrast non-commercial). Has ANY of that moved? Any served or newly-listed
mesh-texture route that takes an image identity reference and a commercial-clean
license?

**Q4 — the blunt routing question.** Given all of the above, where would you
route "one canonical character → clean textured 3D asset" on today's served
catalog? Rank your top two or three routes with the identity story, the license
bucket, and the single biggest risk of each. If the honest answer is "the
per-view route you have, plus discipline, is still the best available and the
wall is real," say exactly that — a confirmed wall is worth more to us than a
speculative door.

## Calibration (the channel's own rule)

Nominate ONE checkable claim from your answer — schema-level or catalog-level,
verifiable by a fetch on our side before anything acts on it.

## Give-back

Item 3 above is yours to keep (the region-level ColorMatch wash, measured). Also:
SetLatentNoiseMask's init-restoration behavior confirmed exactly per source at
`samplers.py:637-641`; the one-job-probe pattern caught a composition defect both
our schemas had individually verified — schema verification is not behavioural
verification, which your round-2 rules already implied and our record now
carries as law.
