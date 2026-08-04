# E08 — intersection regression: predictions, recorded before R1 ran

**Executor session, 2026-08-04.** Written after R0 (the no-op anchor) reproduced and
**before `--trust-intersect` was run even once.** Blind with respect to R1: no R1 output of
any kind had been produced when this file was written. R0's diagnostics *were* consulted —
that is the baseline the prediction is made from, and it is the only thing available.

Amendment 26's pre-registered direction is *"more trusted paint at the rim, since erosion is
no longer pushed deep by a phantom boundary."* **I predict the opposite direction, and the
reason is mechanical rather than empirical.** Stating that disagreement here, before the
measurement, is the point of the file.

---

## The mechanism, argued from the operator rather than from the data

`dist_in = distance_transform_edt(fm > 0.5)` returns, at each pixel, the distance to the
nearest pixel **outside** `fm`. Intersecting `fm` with the silhouette can only *remove*
pixels, which can only *add* outside-pixels, which can only make every distance **smaller or
equal**. So

```
dist_in_R1(p)  <=  dist_in_R0(p)      pointwise, everywhere, by construction
```

Acceptance is `d_s >= ed`. If `ed` does not move, a pointwise-smaller `d_s` can only reject
more. **The intersection makes the trust test stricter, not looser.**

This agrees with the halt report's own wording — *"a shadow connected to the figure
**inflates** the distance-to-edge for everything near the ground contact"*. Inflated
distances mean **less** erosion and **more** acceptance in R0. Removing the shadow deflates
them, so R1 erodes deeper there. The phantom boundary was not pushing erosion deep; it was
holding erosion **off**.

The one channel that could push the other way is `fig_w`. In `--edge-absolute` mode
`ed_body = max(2.5, 7.0 x fig_w / 700)`, and `fig_w` is read off the trust mask's columns —
so if the intersection narrows the figure, `ed_body` falls and acceptance loosens globally.
R0 measured `fig_w` raw 385 px (view 0) and 386 px (view 4) against a **388 px** mesh bbox:
the twin is already narrower than the mesh, so the outside paint is not what sets the
extreme columns, and I expect this channel to contribute little or nothing.

## The numbers I am committing to

| quantity | R0 (measured) | R1 (predicted) |
|---|---|---|
| styled | 1,050,368 | **DOWN**, 1,030,000–1,048,000 (a fall of ~5k–20k) |
| styled / valid | 43.7% | 42.9–43.7% |
| styled / reachable | 83.0% | 81.4–83.0% |
| variance | 0.02597 | 0.0256–0.0263 (essentially unmoved) |
| holes | 1,352,442 | up by whatever styled loses |
| `fig_w` view 0 / 4 | 385 / 386 | unchanged, or within a few px |
| `ed_body` | 3.9 px | 3.9 px |
| R1-not-R0 gains | — | **~0**, unless `fig_w` falls |
| R0-not-R1 losses | — | the whole of the delta |

**Magnitude reasoning, so the range is not a hedge.** The removed region is 6,619 px
(view 0) / 5,978 px (view 4) of twin paint, one dominant component each (5,911 / 5,487 px).
`dist_in` only changes within about `ed_body` = 3.9 px of a *newly created* boundary, so the
band that can flip is roughly (the removed component's figure-facing perimeter) x 3.9 px —
order 1,500 twin px per view. At R0's ratio of ~4.2 styled texels per twin figure pixel that
is ~6,000 texels per view, and views 0 and 4 style largely disjoint texels, so ~10,000–15,000
in the union. The stated range brackets that with room either side.

**Where the losses should sit:** in the lowest edge-distance strata (R0 `d_s` just above
3.9 px) and geometrically near the removed component. R0's centroid offsets — `dy +26.7` and
`+32.1 px`, the twin's paint centroid sitting *below* the mesh's on both views — say the
removed mass is low in frame, so **ground contact, boots, the bottom of the skirt**.

## What would falsify what

- **Styled goes UP by more than ~2,000** -> my monotonicity argument is missing a channel.
  The first place to look is `fig_w`: check whether `ed_body` fell.
- **Styled falls by far more than 20,000** -> the outside paint is not a compact band and the
  affected boundary is much longer than R0's component sizes suggest.
- **Variance moves more than ~0.001** -> something other than rim texels changed.
- **Any gain at all with `fig_w` unchanged** -> the implementation is not a pure mask
  intersection, because with `ed` fixed a pointwise-smaller `d_s` cannot admit anything new.
  That last one is a genuine correctness check on my own edit, not a hypothesis about the
  subject.

## What this prediction does not claim

Nothing about whether the intersection is **right**. It is right or wrong on the argument in
Amendment 26 — paint on no surface cannot be asked whether it is trustworthy — and that
argument is untouched by which way the count moves. A correction that costs coverage is still
a correction. **Whether it is adopted is the advisor's ruling and the direction of the delta
is evidence for it, not the decision.**
