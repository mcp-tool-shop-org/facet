# E35 — executor predictions, registered BLIND

**Registered 2026-08-14 by the executor seat, after tasks 0 and 1 landed and BEFORE any
cloud job was submitted.** Zero jobs had been run against the E35 budget at the moment
this file was written; the only measurements in hand are task 0's mechanics and task 1's
baseline censuses over already-recorded artifacts.

**Blind?** Partly, and the boundary is stated rather than claimed. Blind to every arm's
outcome — no seed re-roll, no denoise rung, no conditioning change, no fused twin exists.
NOT blind to the baseline: task 1's whole deliverable is the baseline table these arms are
judged against, and the spec orders it before this file. Where a prediction is anchored on
a baseline number, that number is named.

**Why the unit definitions come first.** Nine consecutive arcs in this repo have missed on
the unit/population family — a real population counted in the wrong unit, an unchecked
property, the rarest clause of a conjunction, a premise inherited from the seat's own
dispatch. So every counted thing below is defined before its number, and each clause of a
conjunction gets its own line.

---

## What one counted thing IS

**A SPECK** = one connected component surviving `twin_despeckle.py --mode census` at its
defaults (`blob_max_px2 36`, `dark_dl 12.0`, `de_min 8.0`, `chroma_floor 8.0`, `window 15`)
inside the view's geometry mask. It is *dark-chromatic relative to its own local register*,
*at or below 36 px²*, and *not part of a larger same-colour structure*. It is NOT "a dark
pixel" and NOT "a near-black pixel", both of which count different populations.

**A TWIN CENSUS** = that count on the generated 352x1024 twin. **A FLAT CENSUS** = the same
count on a Blender `--flat` render of the projected asset. **These are different objects and
they do not have the same magnitude** — measured baseline, view 1: twin **16**, flat **102**.
Every band below names which one it is.

**THE BASELINE**, from task 1, at the pinned E33 §7 recipe (seed 770700, denoise 0.92,
cn 0.9):

| unit | view 1 | 8-view total | 8-view range |
|---|---|---|---|
| twin census (E34 r3) | **16** | **202** | 9 – 43 |
| flat census (E34 accepted asset) | **102** | **733** | 70 – 133 |

**SPATIAL REPRODUCIBILITY between two seeds** = the fraction of seed-A specks having any
seed-B speck within 2 px, scored against the *dilated* null (the coverage of seed-B's speck
mask dilated by 2 px over the figure). Reported as an enrichment ratio, because the raw
fraction is meaningless without its chance rate — the error I had to fix in my own
instrument this session.

---

## P1 — arm 2a, the discriminator: do the dots MOVE across seeds?

- **P1a.** The dots **MOVE**. Spatial reproducibility enrichment between any two of the
  three new seeds lands **below 2.0x**. *(Falsifier: >= 3.0x, i.e. placement is seed-fixed,
  which opens R-c and the bf16 swap fires.)*
- **P1b.** Each new seed's **twin census** for view 1 lands in **8–30**. *(Anchored on the
  baseline's 16 and the 8-view range 9–43. Falsifier: any seed outside that band.)*
- **P1c.** The three seeds' twin censuses spread by **no more than 2.5x** between smallest
  and largest.
- **P1d.** Inter-seed **silhouette IoU** (R-b's precondition, structural agreement) lands
  **>= 0.90** — canny locks structure while leaving texture free.

## P2 — arm 2b, the denoise sweep 0.85 / 0.80 / 0.72

- **P2a.** The view-1 twin census **falls monotonically** across 0.92 -> 0.85 -> 0.80 -> 0.72.
  *(Falsifier: any rung above the rung before it by more than the P1c seed spread — because
  a single job per rung cannot separate a small change from seed noise, and P1c measures
  exactly that noise floor. This is the clause I expect to be most fragile.)*
- **P2b.** At **0.72** the view-1 twin census is **<= 60%** of the 0.92 baseline of 16,
  i.e. **<= 9**.
- **P2c.** A **knee** exists: the largest single-rung drop is at least **2x** the smallest.
  *(The grounding predicts a knee, not a ramp; falsifier is a ramp, all drops within 2x.)*
- **P2d.** **Register does not die before the specks do** — reg-IoU against the view's
  control stays **>= 0.80** (E34's untouched gate) at every rung including 0.72.
- **P2e.** But the twins get **visibly less restylized** as denoise falls: the fraction of
  figure pixels within dE 10 of the clay's neutral grey **rises** at every rung, and at 0.72
  it is **at least 2x** its value at 0.92. *(This is the cost H2 names, and the reason Gate R
  is the Director's and not a number's.)*

## P3 — arm 2c, conditioning

- **P3a.** Task 0c measured `start_percent`/`end_percent` PRESENT, so the arm runs in its
  **scheduled** form, not as a flat cut.
- **P3b.** Conditioning change moves the view-1 twin census by **less than the denoise
  knee does** — the grounding says strength hardens what the sampler invents rather than
  creating it. *(Falsifier: conditioning outperforms the best 2b rung.)*
- **P3c.** reg-IoU at the reduced/scheduled conditioning stays **>= 0.80**.

## P4 — arm 2d, the fusion prototype (zero cloud)

- **P4a.** Median-of-3 over 2a's stack cuts the view-1 twin census to **<= 50%** of the
  *best* single seed in that stack. *(Conditional on P1a: median only cancels what moves.)*
- **P4b.** The disagreement map's high-disagreement pixels are **confined to speck scale** —
  the largest connected disagreement component is **<= 200 px²**. *(Falsifier: a larger
  component means structural disagreement, fusion is rejected per R-b, and selection-not-
  fusion is the noted upgrade path.)*

## P5 — the arc's shape, and the one I most expect to be wrong

- **P5a.** **Cloud jobs spent before Gate R: 8–13.** (2a=3, 2b=3–4, 2c=1–2, 2e=0 — I predict
  the conditional arms do NOT fire.)
- **P5b.** **R-c does not fire** — 2a returns a move-outcome, so the bf16 swap never runs.
- **P5c.** **A generation-side fix alone does not reach flat-census 0.** Even at the best
  configuration, the repainted asset's per-view flat census stays **> 0**, because task 0a
  measured a sub-population produced downstream of the texture that no twin-side change can
  touch, and task 1 measured that only **14.3%** of rendered dots have a twin speck at the
  matching pixel (6.13x chance, but 14.3%). **The corrector carries load that the sweep
  cannot.** *(This is a prediction about H5's "~ 0", and it is the one I would most like to
  be wrong about.)*
- **P5d.** The prediction I rate least reliable is **P2a's monotonicity**, for the reason
  named in its falsifier: one job per rung, against a seed-noise floor that P1c measures
  only after the fact. If P2a misses, the miss is a *design* limit of a 3-rung single-shot
  sweep, not a fact about denoise.
