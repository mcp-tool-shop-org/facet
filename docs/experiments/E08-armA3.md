# E08 — Arm A3: the erosion invariant, and what the erosion was actually protecting

**Spec:** [E08-cover-the-figure-with-reference.md](E08-cover-the-figure-with-reference.md) ·
**Amendments 2–3:** [E08-ruling-gate0.md](E08-ruling-gate0.md) · **Arm A2:** [E08-armA2.md](E08-armA2.md)
**Run:** 2026-08-03, executor session. **No diffusion, no GPU.** C1 read-only.
**No A3 atlas was written** — the andon precedes the write, twice.

---

## Reproduction anchors, both intact

| path | result |
|---|---|
| `--mask-keyed --edge-absolute` | sha `b12917a2c7c14c4b` — **byte-identical to C1 stage 1** |
| `--edge-absolute` | **938,718** styled — reproduces A2 exactly |

## The build, and the invariant

`e = min(ed_absolute, --edge-frac × local half-width)`, half-width from `dist_in`'s maximal
inscribed disc, `--edge-frac = 1/3`.

```
front  max e/R = 0.3333    back  0.3333    bound 0.3333    violations 0
```

Now an **implementation assertion**, labelled as one and not promoted: it cannot fail on a
correct build, so by this repo's rule it is a unit test. It catches an operand-order slip or a
bad half-width lookup, nothing else.

## The stratum table — diagnostic, required, never a halt

Area removed by the erosion, per local half-width. This is the row that earned the arm:

| half-width | 1–2px | 2–4px | **4–8px** | 8–16px | 16–32px | 32+px |
|---|---|---|---|---|---|---|
| area (front) | 164 | 730 | 3,528 | 9,417 | 17,193 | 90,702 |
| **shipped (absolute 3.8px)** | **100%** | **100%** | **77.6%** | 37.6% | 22.5% | 4.4% |
| **A3 (invariant)** | **0%** | **0%** | **33.5%** | 33.7% | 22.5% | 4.4% |

The blade lives in the 4–8px stratum: three quarters of it removed by a guard built to delete
a 1–2px rim. The invariant fixes exactly that.

---

## And then the new andon fired, on the direction the invariant does not bound

```
[twins] front: background probe — newly admitted 78,333 texels, median dE 4.9 from
        background rgb (125,126,126); within dE 10 of it 75.13%
        (already-trusted texels: 0.11%)
AssertionError: ANDON: 75.13% of newly-admitted texels sit within dE 10 of the twin's
background, over the 2.0% limit
```

**Amendment 3's placement was right and it caught a real defect on the first live run.**

### The probe is validated in both directions before the finding is claimed

- **It fires on a deliberately loose build.** `--edge-frac 0.02` → 49.45% newly-admitted
  within ΔE 10 of background, against 0.11% for the already-trusted set in the same image.
- **It is not misfiring on grey subject matter.** A3's number came in *higher* than the loose
  run — backwards — so my first hypothesis was that the probe was flagging the blade's own
  steel, which is grey against a grey background. **That hypothesis is falsified.** The twin's
  own paint, measured per region:

| region | median ΔE from background | within ΔE 10 |
|---|---|---|
| blade | **24.80** | 3.2% |
| boots | 35.23 | 0.1% |
| greave | 36.78 | 0.2% |
| tunic | 42.43 | 0.0% |
| beard | 47.51 | 0.0% |

  Nothing the twin paints is near its background. The contamination is real.

---

## What the erosion was actually protecting against

The twin's own keyed figure mask carries background colour — and it is concentrated, by two
orders of magnitude, in exactly the strata the invariant preserves:

| half-width | 1–2px | 2–4px | 4–8px | 8–16px | 16–32px | 32+px |
|---|---|---|---|---|---|---|
| front, share near background | **21.3%** | **16.4%** | 5.0% | 2.0% | 0.3% | 0.1% |
| back | **20.2%** | **15.5%** | 12.0% | 3.3% | 0.0% | 0.0% |

Overall this is only **0.5%** of the front mask and 0.8% of the back — invisible in aggregate,
and 200× enriched in the thinnest structures. It is E01's background-keying failure, alive in
these twins: cast shadow, background gradient and antialiased fringe keyed as figure, and all
of it thin.

**So the absolute erosion was accidentally correct.** It removed 100% of the 1–2px and 2–4px
strata — deleting the contaminated tendrils wholesale, along with the blade. Its *stated*
justification was void (the mesh is fatter than the twin, Arm A). Its *effective* justification
was this, and nobody had measured it.

**The invariant preserves thin structure proportionally, which preserves the blade and the
contamination together.** They live at the same scale, and the invariant is shape-blind: it
cannot tell a blade from a shadow tendril, because half-width is the only thing it reads.

---

## Open for the ruling

1. **A3 as specified cannot separate them.** Anything that keeps thin structure keeps thin
   keying artifacts, unless something distinguishes the two. The background-ΔE probe *is*
   such a discriminator and it is already computed per sample — but moving it from a gate into
   the acceptance rule is a new design, not a re-run, and is not mine to take.
2. **The `--bg-max-pct` quantity is mine and is stated so it can be ruled on.** 2.0%, chosen
   as an order of magnitude above A2's ratified 0.18%. Nothing about this halt is marginal —
   75.13% against 2% — so the threshold is not what decided it.
3. **`--edge-frac` was never what fired** and stays at 1/3.

Front coverage reached **633,518** under the invariant against A2's **555,185** before the
halt. That is a partial and, given the contamination measured above, not a number to bank.

Artifacts: `facet_E08/A3/repro.png` (byte-identical pre-E08 path), `a2repro.png` (A2's config
through the new code). No `styled_stage1.png` — the arm halted.
