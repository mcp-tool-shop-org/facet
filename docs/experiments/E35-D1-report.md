# E35 — D1 corruption discriminator, executor report

**Run 2026-08-14** at the Director's word ([E35-ruling.md §8](E35-ruling.md)). Bands and the
local enumeration registered at `413bb92`, **before** the job. **One job. 43 → 44 of 60.**

**D1 is not clean, so D2 does not fire.** The dispatch conditions D2 on a clean D1; it is
off, no repeat is taken (D1's return is the discriminator answering, not a mechanical
defect), and the arc halts here.

**The result is stronger than "still corrupted."** D1's output is **pixel-identical to
A3c** — 0 differing pixels of 1,053,696 — while the two files' sha256 differ.

---

## 1. What the enumeration settled before the job

Both clay inputs read at the PNG chunk level: identical bit depth (8), identical colour type
(**6, RGBA — both of them**), identical interlace, identical chunk set, and **all-opaque
alpha in both, one unique value, 255 everywhere**. The two files are structurally identical
except size.

That killed two of the dispatch's own three fallback candidates before spending — **bit depth
and PNG colour type are the same in the file that worked and the file that did not** — and
narrowed the alpha hypothesis to Ruling 8's exact form: the *path*, not the file.

## 2. What the job settled

| | |
|---|---|
| **Alpha — EXONERATED, decisively** | Not merely "still corrupted": the RGB-flattened input produced **exactly the same pixels** as the RGBA one. The fourth channel changed nothing anywhere in the pipeline, so it cannot be stripped-or-passed by any path |
| **The fault is DETERMINISTIC** | Same input content + same config → pixel-identical output. The three distinct A3 signatures came from three distinct *configs* (seed 770700 / turbo-on, seed 770700 / turbo-off, default seed / turbo-on), not from a nondeterministic platform fault |
| **Bit depth, colour type** | exonerated locally, above |
| **Seed** | exonerated by A3c vs A3a |
| **Turbo / Lightning LoRA** | exonerated by A3b vs A3a — both corrupt |

**What remains is the image content itself.** A2's input traversed
`FluxKontextImageScale`'s real resample (352×1024 → ×1.909091 → centre-crop); A3's and D1's
hit it at no-op. The difference between the two is therefore either **what the resample does
to the pixels** (a 1.909× lanczos upscale is soft and band-limited; a native render is not)
or **the framing** (our native 672 render puts more background around the same figure,
because `h_ext` grows with the frame while the figure does not).

⚠ **The decisive next discriminator is one job and is NOT taken here**, because it is not
authorised: replay the scaler's transform **locally** on the recorded 352×1024 clay — the
same arithmetic already verified for the mask at IoU 0.9531 — save it as a 672×1568 PNG, and
submit that. **Clean ⇒ the trigger is the native render's content** and a locally-resampled
input is the route's fix. **Corrupted ⇒ the trigger is that the pixels did not pass through
the node itself**, which is a platform-side finding and closes our side of it. Either branch
ends the question; it is on the Director's word, not mine.

## 3. Bands, scored

| band | predicted | measured | verdict |
|---|---|---|---|
| **D1-P1** flattened input still corrupts (0.7, **against the dispatch's leading hypothesis**) | corrupts | corrupts | **HIT** |
| **D1-P2** register survives if clean — C\* on the keyed figure ≥ 15 | — | **N/A**, as pre-registered | **N/A** |
| **D1-P3** if it corrupts, a FOURTH distinct signature | new signature | **reproduces A3c exactly** | **MISS** |
| **D1-P4** the flatten changes no RGB value | identity | max \|Δ\| **0** | **HIT** |

**D1-P1 is the one I want on the record as a hit, and it is not a victory lap.** I registered
at 0.7 *against* the ruling's leading hypothesis, with the reason stated: a constant 255 plane
carries no spatial structure, so for alpha to be the trigger the corruption would have to come
from a channel with no information in it. That reasoning held.

**D1-P3 is the informative miss.** I predicted a fourth distinct signature on the grounds that
"three inputs at one configuration gave three patterns, so the fault is not deterministic."
That sentence was wrong twice over: they were not one configuration — they were three — and
the fault *is* deterministic. **The band was built on a mis-stated population, which is the
family this repo keeps paying for**, and it caught me one level below where I have been
watching: not the unit, not the members, but *which variable I had actually held fixed across
them*. I had the run log and still summarised it wrong.

**D1-P2 scored N/A on the instrument's evidence, not on my say-so.** `t2_register_all.py`
refused D1 with `ANDON: keyed figure spans the whole frame` — the bbox-check declining to read
a number off a frame where the background estimator found figure everywhere. Ruling 8's new
register-survived term therefore gets its first exercise as a **refusal**, which is the
correct behaviour and the reason the term was folded: *non-degenerate* could not have
separated this frame from a mannequin, and the keyed-figure guard can.

## 4. This repo's own law, running in reverse

*"A PNG hash mismatch is not evidence a render changed — file bytes are not pixel values."*
Twice this law has produced a false halt on identical renders. Here the same fact ran the
other way and produced the finding: **the sha256s differ and the pixels do not.** Had I
compared bytes I would have reported "D1 differs from A3c" and drawn the opposite conclusion
about alpha.

```
D1  sha256 acb9651307f4b4da9d4eb2f0bbc9be15bd0cdc01dbac2fbb027b2ca7f995e932
A3c sha256 8dff8e54c94e824946594a20f22287e6f75599821e8f9c4a35ae8296ec6b2517
differing pixels: 0 of 1,053,696
```

## 5. Artifacts

```
E:\AI\training\facet_E35\
  k672\armclay672_1_rgb.png        the flattened input; colour type 2 read from the IHDR
                                   bytes, RGB byte-identical to the RGBA source
  twins\twin_D1_rgbflat_v1.png     pixel-identical to twin_A3c_noseed_v1.png
  diag\E35_D1_discriminator_sheet.png
docs/experiments/E35-anchored-pilot-bands.md   D1 section, pushed before the job
```

D1 prompt_id `c6f1240a-6f20-4c88-8c0c-3e7f5c4df44e`.

## 6. HALT

**44 of 60. D2 is off by its own condition.** Sixteen jobs remain; the eight-view rebuild
still fits them and is still not mine to launch — and there is nothing to rebuild from: A2
remains the only clean 2509 result on our subject and it sits in a frame that crops the head
band.

The arc's 2509 question is unchanged and its *cause* list is four items shorter. One
authorised job — the locally-resampled input in §2 — would close the remaining fork in either
direction.
