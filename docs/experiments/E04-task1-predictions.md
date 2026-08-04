# E04 Task 1 — predictions, recorded BEFORE any measurement

**Executor session, 2026-08-04.** Written before opening a single render, provenance panel,
atlas or JSON from the accepted asset in this session. **Blind** in that sense; *not* blind to
the advisor's pre-registered prior (Amendment 35), which the kickoff states in full, nor to the
E07 Gate 0 numbers, which are in the repo. Both are declared below so the disclosure is honest
rather than flattering.

## What I already know, and therefore cannot claim as blind

- Amendment 35's prior: the unlevelled stroke-seam defect. Alternates offered: per-island tonal
  offsets (chart fragmentation), dilation patches.
- E07 Gate 0 measured, on a *different* asset (E07's C1) and a *different* region (the
  forehead): whole-figure cross-provenance step ratio **5.500**, the named forehead **9.500**,
  dilation boundaries **1.50-1.75**, same-provenance island boundaries **1.500**,
  cross-provenance-inside-one-island **4.500**.
- The accepted asset's global mix: 68.8% reference / 4.2% brush / 27.0% dilation.
- Strokes 7 and 8 are the two elevated cameras (y+000_e+55, y+180_e+55) and delivered 72,116 of
  101,527 brush texels - 71% of all brush paint.
- I have **not** looked at where the blotch is, what its provenance composition is, or any
  render of the head.

## Predictions

| # | prediction | falsifiable as stated |
|---|---|---|
| **P1** | The blotch region is **not** provenance-uniform: it contains at least two provenance classes, and at least 15% of its area is a class other than its majority class. | fails if >=85% one class |
| **P2** | The dominant *cross-provenance* boundary inside the blotch involves a **brush stroke** - i.e. one side of the modal boundary pair is s7 or s8, not TWINS\|DILATION. | fails if the modal pair is TWINS\|DILATION or DILATION-only |
| **P3** | The blotch region's **cross-provenance step ratio >= 3.0** (median \|dL\| across provenance boundaries / median \|dL\| within a provenance region). Point estimate **6-11**, bracketing E07's forehead 9.5. | fails if < 3.0 |
| **P4** | **Alignment:** >= 50% of the blotch's own perimeter pixels lie within 2 px of a provenance boundary. | fails if < 50% |
| **P5** | **The island/chart alternate is not the mechanism:** same-provenance *island* boundary ratio inside the region <= 2.0, i.e. well below P3's cross-provenance ratio. | fails if island ratio >= P3's ratio |
| **P6** | **The dilation alternate is not the mechanism:** dilation-adjacent boundaries in the region are the *flattest* class present (consistent with E07's 1.50-1.75), so dilation patches do not explain a hard edge. | fails if a DILATION-involving pair is the steepest class |
| **P7** | Dilation share **inside the crown blotch region exceeds** the asset-wide 27%. | fails if <= 27% |
| **P8** | Stage-1/TWINS share inside the region is **below** the asset-wide 68.8% (the crown grazes every horizontal camera). | fails if >= 68.8% |

## The composite call

**P2 + P3 + P4 all hold -> the advisor's prior is confirmed** (a stepped, aligned provenance
seam involving a brush stroke).
**P4 fails -> not aligned -> report and stop.** That is the kickoff's ruling branch and I will
take it without tuning the alignment tolerance.

## What would make me say the prior is wrong even if the numbers pass

If the blotch's perimeter aligns with **island** boundaries rather than provenance boundaries
(P5 inverted), the mechanism is chart fragmentation, not seam levelling - a different fix. I
will report the two alignment fractions side by side rather than only the one the prior wants.

## Instrument risk I am naming in advance

The E07 instrument measures |dL| on an 8-bit render; its denominator was **4.0 quanta**. Any
ratio here is a small-integer quotient and does not carry three digits. I will report the
numerator and denominator medians separately, per E07's own consequence note, so a ratio that
moved because the denominator rose is visible as such.

## Locating the region is not measuring it

I have to *find* the crown blotch before I can measure it, and that requires looking at a
render. The sequence is: this file is written and hashed first; then I locate the region by eye
and record its pixel extent; then the instrument runs. No prediction above is edited after the
region is located.
