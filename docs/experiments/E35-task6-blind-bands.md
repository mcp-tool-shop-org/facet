# E35 task 6 — executor blind bands, registered BEFORE the legs run

**Registered 2026-08-14, after reading the Gate R2 amendment and before any leg was
executed.** Zero jobs spent at registration. The amendment pre-registers the
*interpretation maps*; these are my *quantitative* bands under those maps, so a reading
cannot be fitted afterwards.

**Blindness boundary, stated rather than claimed.** I am NOT blind to: the three-row
sheet, the face-compare sheet, the flat/head blotch aggregates I ran before the Director's
correction (whole-figure 100,624 → 90,785 px; head-band 24.48% → 21.18%), and the
selected set's spread (C\* 9.77, L\* 10.14). I am blind to: every leg's output below —
no ownership overlay, no seam measurement, no per-seed twin comparison, no chroma/luminance
decomposition at the blotch, no frequency profile, and **E34's accepted-set spread has not
been measured** (leg 6f's operand does not yet exist).

**My prior, and how it has moved.** I proposed the mixed-seed patchwork mechanism and I
have an interest in it being right. Against it, one thing I can already see without running
a leg: **E34's accepted asset — a single-seed set — also carries a pale cap over the crown**
in the face-compare sheet's middle row. A single-seed asset cannot exhibit mixed-seed
patchwork. That observation moves me off my own proposal before the discriminator runs, and
the bands below reflect it.

---

## 6a — ownership overlay

**Unit:** the fraction of pale-region *boundary* pixels lying within 2 px of an ownership
seam, measured in the render domain after rendering an owner-coloured atlas through the
same camera call.

- **P6a**: that fraction lands **20–45%**. *(Chance is not zero: seams are dense on a
  head. A patchwork reading needs it high; a generation reading low.)*
- **P6a-2**: the largest pale region on the head **spans ≥ 2 owners**.

## 6b — seam-crossing (decisive where it exists)

**Unit:** for pale regions spanning ≥2 owners, the median |ΔL\*| across the seam measured
on matched 5 px strips either side, inside the pale region only.

- **P6b**: the step lands **< 3.0 L\***, i.e. tone continuous — generation-side.
  *(Falsifier: ≥ 5.0 L\*, a visible step, patchwork.)*
- **P6b-2**: for comparison, the same measurement on seams **outside** pale regions lands
  in the same band ± 1.5 L\* — i.e. seams are not generally visible on this asset.

## 6c — same view across seeds

**Unit:** for each blotch-owning view, whether a pale region of ≥ 25 px² occurs within
10 px of the same anatomical location in that view's twin at each of the three seeds.

- **P6c**: pale occurs at the same location in **≥ 2 of 3 seeds** on the blotch-owning
  views — stable across seed, therefore generation-side. *(Falsifier: ≤ 1 of 3, i.e. it
  moves or vanishes with seed.)*

## 6d — chroma vs luminance at the blotch

**Unit:** inside pale regions vs the figure's own register, C\* (circular-safe: chroma is a
magnitude, so a plain median is legitimate; hue is not quoted) and L\*.

- **P6d**: **C\* inside the pale regions is ≥ 30% below the figure median**, and
  **L\* is ≥ 5 above** — the desaturation signature.
- **P6d-2**: hue is **not** quoted anywhere in this leg unless its chroma clears the
  floor (C\* ≥ 8); I expect a material fraction of pale pixels to fall **below** the floor,
  which is itself the finding.

## 6e — frequency profile

**Unit:** median gradient magnitude of L\* on pale-region boundaries, divided by the same
statistic over the figure's other edges.

- **P6e**: the ratio lands **< 1.5** — smooth low-frequency lobes rather than step edges.
  *(Falsifier: ≥ 2.5, step-edged, seam-shaped.)*

## 6f — the spread metric earns or loses its voice

**Unit:** the SAME instrument that produced C\* 9.77 / L\* 10.14 on the selected set, run
over **E34's accepted eight-view twin set** (all seed 770700).

- **P6f**: E34's accepted spread lands **below 6.0 on both axes** — clearly lower than the
  rejected set's 9.77/10.14, so the metric separates accepted from rejected and keeps a
  voice.
- **P6f-2**: **this is the band I most expect to miss.** If E34's spread comes back near
  9–10, the metric does not separate and gates nothing — and I will have spent the
  coherence sheet reporting a number that never had standing. I register that outcome as
  fully expected-possible rather than as a surprise.

## 6g — the twins at the blotch UVs, pre-projection

**Unit:** the full-size sheet; the readable claim is whether pale is present in a **lone**
twin.

- **P6g**: pale **is** visible in at least one individual twin at the blotch location,
  before any projection — therefore not born at assembly.

## Task 7 — consult calibration

- **P7a**: the archive **does** contain at least one byte-identical (inputs + parameters)
  repeat pair, so **zero jobs** are spent. *(View 1's seed-770701 and seed-987654 twins were
  generated in arm 2a and re-used in task 4 without re-submission, so a true repeat may not
  exist; if none does, one job is spent.)*
- **P7b**: the diff is **pixel-identical or a uniform residual at or under ΔE ≈ 0.84** —
  same-seed reasoning stands.

---

**Overall.** Under the amendment's maps, my bands point **generation-side** on 6b, 6c, 6d,
6e and 6g, and equivocal on 6a. That is a reversal of the remedy I proposed two messages
ago, registered here before the evidence, on the strength of one thing already visible:
the single-seed accepted asset carries the same pale crown.
