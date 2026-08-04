# E08 — Arm A3: the erosion invariant, HALTED at its own gate

**Spec:** [E08-cover-the-figure-with-reference.md](E08-cover-the-figure-with-reference.md) ·
**Amendment 2:** [E08-ruling-gate0.md](E08-ruling-gate0.md) · **Arm A2:** [E08-armA2.md](E08-armA2.md)
**Run:** 2026-08-03, executor session. **No diffusion, no GPU.** C1 read-only.
**No A3 atlas was written** — the assert precedes the write.

---

## Reproduction anchors, both intact

| path | result |
|---|---|
| `--mask-keyed --edge-absolute` | sha `b12917a2c7c14c4b` — **byte-identical to C1 stage 1** |
| `--edge-absolute` (A2's config) | **938,718** styled — reproduces A2 exactly |

Reproducing any pre-E08 arm now needs **both** flags, and that is in the `--edge-absolute`
help text.

## The build

The erosion is no longer an absolute distance scaled by the figure's *global* width. The
invariant: **never remove more than a bounded fraction of a structure's own width.**
`dist_in` already carries it — the maximal inscribed disc covering a pixel is that pixel's
local half-width — so `e = min(ed_absolute, --edge-frac × R)` with `--edge-frac = 1/3`.

**The invariant is satisfied exactly:**

```
front   max e/R = 0.3333   bound 0.3333   violations 0
back    max e/R = 0.3333   bound 0.3333   violations 0
```

## The gate fires on the known-bad configuration

Validated before being trusted, against the erosion that shipped — area removed per
half-width stratum, front view:

| half-width | 1–2px | 2–4px | 4–8px | 8–16px | 16–32px | 32+px |
|---|---|---|---|---|---|---|
| area | 164 | 730 | 3,528 | 9,417 | 17,193 | 90,702 |
| **shipped (absolute 3.8px)** | **100%** | **100%** | **77.6%** | 37.6% | 22.5% | 4.4% |
| **A3 (invariant)** | **0%** | **0%** | **33.5%** | 33.7% | 22.5% | 4.4% |

Monotone annihilation of thin structure by a distance chosen from the figure's global width
— the diagnosis, measured. The blade sits in 4–8px: **77.6% of it removed** by a guard built
to delete a 1–2px mixed rim.

## And then it fired on A3

```
AssertionError: ANDON: the edge erosion removes 43.8% of the 8-16px half-width stratum
(4,821px), over the 40% limit — that is deleting a structure, not its rim.
```

Reported and halted. No parameter changed, no re-run.

**The invariant is not violated; my threshold was mis-derived.** I set 0.40 from the bar
relation — a bar of half-width `R` eroded by `e` loses exactly `e/R` of its area, so
`--edge-frac = 1/3` should cost 33.3% — and added headroom for raggedness. The measured
deviation from that idealisation runs in **both** directions and is larger than the headroom:

| stratum | area removed | bar prediction | excess |
|---|---|---|---|
| front 4–8px | 33.5% | 33.3% | +0.2 |
| front 8–16px | 33.7% | 33.3% | +0.4 |
| front 16–32px | 22.5% | 33.3% | **−10.8** |
| back 4–8px | 29.8% | 33.3% | −3.6 |
| **back 8–16px** | **43.8%** | 33.3% | **+10.4** |
| back 16–32px | 20.6% | 33.3% | −12.7 |

A tapering or ragged structure has more perimeter per unit area than a bar, so more of it
lies within `e` of an edge; a compact one has less. Stratum area-loss is a **shape**
statistic, and it is not bounded by the invariant that governs `e`. Setting a threshold on it
from the bar idealisation was the error — the fifth mis-specified pass condition in this
repo, and it is the executor's this time.

**Not retuned.** Picking a number now, after seeing 43.8%, is precisely the move the ledger
exists to prevent.

## A second self-correction inside this arm

The first version of this gate measured **per connected component**, as Amendment 2 worded
it. It was rejected on measurement, not on taste: the twin's whole front figure is **one
component of 121,709 px**, because the blade touches the hand gripping it, so the blade
losing three-quarters of its area read as **12.3% overall**. Connectivity cannot separate a
blade from the body holding it. Thickness can, and thickness is the unit the invariant is
already stated in.

## What is measured, and what is not

Front-view coverage reached **633,518** styled texels under the invariant, against A2's
**555,185** — but the run halted on the back view, so **there is no A3 total and no A3
atlas**. That number is a partial, not a result.

## Open for the ruling

1. **The threshold.** `e/R ≤ 1/3` holds by construction and is checkable for free. Whether a
   *stratum area-loss* gate should exist at all — given it measures shape as much as
   erosion — or whether the invariant check is the honest gate, is not mine to decide.
2. **`--edge-frac` itself is untouched at 1/3** and was never the thing that fired.

Artifacts: `facet_E08/A3/repro.png` (byte-identical pre-E08 path), `a2repro.png` (A2's config
through the new code). No `styled_stage1.png` — the arm halted.
