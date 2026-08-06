# E12 handoff 4, Task 1 — the beast's canny pair, derived

**Executor session, 2026-08-06.** Predictions pre-registered blind in `d347744`
([E12-task1-canny-predictions.md](E12-task1-canny-predictions.md)) — the grid, the four
views, the erosion depths, the interior definition and the works-perfectly test all fixed
before a single Canny ran. This report ranks nothing and recommends nothing beyond the
proposal the dispatch explicitly asks for, and it says which half of that proposal is
derived and which half is a judgement.

**Nothing was generated. No credits were spent. No profile value was written.**

Artifacts: `E12_repair/sweep/` (`canny_sweep.json`, `CONTROL_SHEET_{1,5}.png`, six 5× crops)
and `E12_repair/crops/`. **Look at `CONTROL_SHEET_1.png` before the numbers.**

---

## 0. Environment

| leg | result |
|---|---|
| watchdog | **alive**, verified before the geometry leg and reported either way — heartbeat age 0.1–1.1 s, pid 22324, VRAM 2,134 MiB against the 31,200 MiB ceiling. No `_watchdog_DEAD` present |
| silhouettes | `silhouette_masks --profile beast.json --views 1,2,4,5` into a **fresh** directory, so `E12_pair/masks/` was never opened for writing |
| clay renders | **reused, not re-rendered** — `E12_pair/clay/` are the handoff-3 profile-rendered views (width-fit, 1792×1024, margin 1.204). Reusing them makes the sweep measure exactly the renders the re-pair's controls will be built from, and leaves the previous session's artifacts byte-untouched |

## 1. The ANDON fired, and the anchor was the thing that fired it

The tool's first act is to reproduce `restylize_views.py`'s own recorded Canny counts at the
profile's pair before any sweep row is written. **It did not.**

| view | replica, first construction | recorded by `restylize_views` | |
|---|---|---|---|
| 1 | 35,992 | 36,011 | −19 |
| 5 | 22,658 | 22,642 | +16 |

Nothing was swept. The mechanism was isolated before anything was changed: the replica kept
the figure mask as a **bool** array, which is the obvious way to write it and is
arithmetically identical on paper. `1.0 - fm` on a bool array promotes to **float64**, so the
composite and its `.mean(axis=-1)` ran at double precision, and ~19 px per view landed on the
other side of the `uint8` truncation and then on the other side of a Canny threshold.
`control_image` writes `.astype(np.float32)`.

Measured both ways, in one run, before the fix:

```
view 1  bool   (mine)   comp.dtype float64  canny 35992   want 36011  no
view 1  float32 (source) comp.dtype float32  canny 36011   want 36011  MATCH
view 5  bool   (mine)   comp.dtype float64  canny 22658   want 22642  no
view 5  float32 (source) comp.dtype float32  canny 22642   want 22642  MATCH
```

**This is an operand repair, not a retune**, and the retune test passes: the fix was "use the
source's dtype chain," which would have been the fix whatever number came out — no threshold
was moved to reach 36,011. **Second instance of this exact class in two sessions** (E12
Ruling 9a was a normalisation that cancels mathematically and not in float32). The standing
rule caught it both times and is quoted in the tool's docstring at the site:
*an anchor is computed with the source's own arithmetic, not with arithmetic equivalent to it.*

## 2. Predictions scored — 4 held, 4 falsified, 1 partial

| # | prediction | outcome |
|---|---|---|
| **C1** | replica reproduces 36,011 / 22,642 exactly | **FALSIFIED** on first construction (§1); exact after the operand repair |
| **C1b** | silhouette re-render byte-identical to `E12_pair/masks/` | **held** — 0 differing px, IoU 1.000000, on both anchored views, by the tool's own `--anchor` |
| **C2** | the four inherited numbers reproduce within ±1.0 point | **held** — worst deviation **0.154 points** (view 5 at 0.05/0.15: 11.304 vs 11.15). See §3 |
| **C3** | monotonic, no adjacent rung differing by >1.5× | **held** — monotonic on all four views; max adjacent ratio **1.358** (view 2). **No knee exists** |
| **C4** | W-outside = 0 at every candidate | **held** — **0 absolute px across all 64 rows.** The composite forecloses backdrop banding by construction; the dispatch's naming of it as a risk is misattributed |
| **C5** | W-band ≥15% at 0.02/0.06 | **FALSIFIED** — 1.34–2.82%. And the instrument was blind to a real artifact (§4) |
| **C6** | W-speckle higher at 0.05/0.15 than 0.20/0.45 on every view, and <25% | **PARTIAL** — falsified on view 5 (4.20% vs 4.40%); held on 1/2/4; the <25% clause held everywhere (worst 6.40%) |
| **C7** | view 4 ratio > view 5; view 2 ratio smallest | **FALSIFIED**, both blind clauses. Measured ordering **v1 3.08 < v2 3.71 < v4 4.97 < v5 5.17** |
| **C8** | moving `high` changes the fraction by <half the change from moving `low` | **FALSIFIED, and it is the session's most useful miss** (§5) |
| **C9** | the proposal lands in 0.05–0.12 low | **held** — 0.05 (§6) |

## 3. The inherited four are corroborated by an independent construction

E12 Ruling 10c's numbers were measured by a previous seat with an instrument that is **not in
the repo** — no script, no JSON, no stated definition of "figure interior." This session
built its own definition from scratch (exact silhouette, eroded 5 px) and got:

| | claimed | measured | Δ |
|---|---|---|---|
| 0.4/0.8, view 1 | 5.20% | **5.131%** | −0.069 |
| 0.4/0.8, view 5 | 2.13% | **2.187%** | +0.057 |
| 0.05/0.15, view 1 | 15.80% | **15.826%** | +0.026 |
| 0.05/0.15, view 5 | 11.15% | **11.304%** | +0.154 |

**The ruling's numbers stand**, and the 3.0×/5.2× multiples it quotes reproduce (3.08×/5.17×).

The erosion depth is not doing the work. On view 1 the headline moves by **≤ 0.09 points**
across erosion 3 / 5 / 9:

```
0.40/0.80   e3  5.175%   e5  5.131%   e9  5.143%
0.05/0.15   e3 15.829%   e5 15.826%   e9 15.745%
```

## 4. The works-perfectly test — what a lower pair admits that is NOT relief

**The pre-registered statistic failed and the eye caught what it missed. Both are reported.**

W-band (Sobel |Gx|+|Gy| ≤ 8 at the admitted pixel) said the bottom rung was clean: 1.34–2.82%
at 0.02/0.06. Then the 5× crop of a **smooth membrane field** on view 5 showed a whole
population of wandering closed contours with no counterpart in the render — iso-luminance
bands in an almost-flat gradient — present at 0.02/0.06 and **gone at 0.05/0.15**.

W-band could not see them because it asks about the gradient **at** the pixel, which Canny's
own low threshold bounds from below; those pixels clear the bar (2–4 LSB steps). Only their
**neighbourhood** gives them away. So a second instrument was added, with its reason recorded
in the tool rather than hidden — **W-flat**, the fraction of admitted pixels whose local 15×15
grey range is ≤ 12 (edges found where the neighbourhood has no contrast to carry one):

| pair | W-flat12 %, v1 / v2 / v4 / v5 |
|---|---|
| 0.02/0.06 | **1.19 / 1.20 / 3.97 / 3.58** |
| 0.03/0.09 | 0.25 / 0.42 / 1.31 / 0.93 |
| **0.05/0.15** | **0.01 / 0.12 / 0.18 / 0.09** |
| 0.08/0.20 | 0.00 / 0.01 / 0.03 / 0.01 |
| 0.10/0.25 and below | 0.00 everywhere |

The instrument locates the phenomenon where the geometry says it should be: **the artifact is
3–4× worse on views 4 and 5**, the membrane-dominated views with the large smooth fields, than
on the head-bearing views 1 and 2. That agreement is what makes it worth reporting; it is not
a gate.

**This is E07's lesson arriving in a new instrument, and Ruling 10d's point from the other
side:** a per-pixel statistic cannot separate what a look separates. The crops decided this,
the number followed, and the order is recorded because it is the reverse of the order the
predictions assumed.

The other two channels, for completeness: **W-outside = 0 absolute pixels on all 64 rows** —
`control_image` composites onto uniform `bg 0,0,0`, so no edge can exist on the backdrop at
any threshold. **W-speckle** is non-monotonic: it falls from 9.9% at 0.02/0.06 to a minimum
of 4.2% around 0.12/0.30 and rises again to 13.4% at 0.30/0.65, because as the admitted set
shrinks it becomes mostly fragments.

## 5. `high` is the lever. `low` is nearly inert — and that inverts the arm

C8 predicted `high` was the weaker threshold. Measured on view 1:

```
low fixed at 0.05, high 0.10 -> 0.30 :  17.842%  ->  12.632%     -5.210 points
high fixed at 0.20, low 0.05 -> 0.10 :  14.576%  ->  14.041%     -0.535 points
```

**`high` moves the interior edge fraction about ten times as much as `low` does.** The reason
is the subject: on grey-on-grey Workbench clay almost all relief is *weak* edge, so what
decides whether a scale row reaches the control is whether hysteresis lets a weak chain
survive — which is `high`'s job — not whether a seed exists, which is `low`'s.

The consequence for the derivation is structural rather than a matter of taste:

- **`low` is not a structure control on this subject. It is the artifact control.** It buys
  almost no relief and it is the only threshold that moves W-flat.
- **`high` is the structure control, and no instrument in this session bounds it.** W-outside
  and W-flat are flat in `high`; W-speckle trades against it monotonically with no knee (C3).

## 6. The proposal — and which half of it is derived

### `canny-low = 0.05` — **DERIVED**

It is the lowest grid value at which the flat-field artifact is measured absent (W-flat12
≤ 0.18% on every view, against 0.93–1.31% at 0.03 and 1.19–3.97% at 0.02) **and** confirmed
absent by eye at 5× on the smooth membrane field. Below it the pair admits non-relief. Above
it there is nothing left to buy — the artifact is already gone at 0.05, and raising `low`
further costs structure for no measured artifact benefit.

### `canny-high = 0.15` — **PROPOSED, NOT DERIVED. This is the advisor's to rule.**

No instrument in this session bounds `high`. Its measured trade is structure against speckle,
monotone in both directions, with no cut point anywhere on the ladder. Stating that plainly
rather than manufacturing a derivation is this repo's own rule about thresholds the data
cannot support. Three grounds are offered for 0.15 specifically, all of them judgement:

1. It is the highest-structure candidate at the derived `low` floor whose speckle stays below
   the next rung up in structure — 6.4% against 0.05/0.10's 8.2% on view 1.
2. It keeps the ~1:3 `low`:`high` ratio class the source recipe used.
3. It is the point Ruling 10c already measured, so the ruling's numbers and this session's
   describe the same candidate.

### The trade table the ruling chooses on

`x` = multiple of the profile's 0.4/0.8 interior fraction, per view v1 / v2 / v4 / v5.

| pair (int) | interior e5 % | × vs profile | W-flat12 % (artifact) | W-speckle % |
|---|---|---|---|---|
| 0.02/0.06 (5/15) | 20.44/21.48/16.35/16.98 | 4.0/4.7/7.9/7.8 | **1.19/1.20/3.97/3.58** | 9.9/8.5/8.4/8.1 |
| 0.03/0.09 (7/22) | 18.58/19.48/13.46/14.15 | 3.6/4.3/6.5/6.5 | 0.25/0.42/1.31/0.93 | 8.3/6.8/6.7/6.4 |
| 0.05/0.10 (12/25) | 17.84/18.75/12.49/13.30 | 3.5/4.1/6.1/6.1 | 0.04/0.16/0.42/0.37 | 8.2/6.6/6.6/6.2 |
| **0.05/0.15 (12/38)** | **15.83/16.96/10.25/11.30** | **3.1/3.7/5.0/5.2** | **0.01/0.12/0.18/0.09** | **6.4/4.9/4.8/4.2** |
| 0.05/0.20 (12/51) | 14.58/15.75/8.94/10.00 | 2.8/3.4/4.3/4.6 | 0.02/0.07/0.20/0.10 | 5.3/4.0/4.0/3.5 |
| 0.08/0.20 (20/51) | 14.28/15.19/8.54/9.46 | 2.8/3.3/4.1/4.3 | 0.00/0.01/0.03/0.01 | 5.4/4.2/4.2/3.7 |
| 0.10/0.25 (25/63) | 13.16/13.87/7.38/8.17 | 2.6/3.0/3.6/3.7 | 0.00/0.00/0.00/0.00 | 4.7/3.6/3.7/3.5 |
| 0.12/0.30 (30/76) | 12.01/12.52/6.26/7.03 | 2.3/2.7/3.0/3.2 | 0.00/0.00/0.00/0.00 | 4.2/3.3/3.8/3.4 |
| 0.40/0.80 (102/204) | 5.13/4.58/2.06/2.19 | 1.0 | — | — |

**The named alternative, if the advisor weights the residual artifact above the residual
structure: 0.08/0.20.** It costs ~10% of the admitted structure and cuts W-flat12 by 6–18×.
At 0.05/0.15 the residual artifact is 0.18% of 41,041 admitted pixels on the worst view — **74
pixels** — so the absolute quantity being traded is small in both directions.

## 7. What the eye sees, which is the gate here (Ruling 10d)

`CONTROL_SHEET_1.png`, full frame, three panels — **this is the report's real finding**:

- At the profile's **0.4/0.8** the control is a colouring-book outline: silhouette, a handful
  of the strongest creases, and **empty wings**. At denoise 0.92 everything inside that
  outline is the model's to invent.
- At **0.05/0.15** the control carries wing-membrane veins, the ventral banding, the scaled
  flank, the frill, the dorsal spine row and the tail scales — the animal's actual surface.
- At **0.08/0.20** the same picture, slightly thinner in the finest vein tracery.

The two decisive 5× crops:

- `CROP_5_backspines*.png` — the profile's pair catches **only the two spine silhouettes**;
  the whole scale-relief field beside them reaches the control as nothing. 0.05/0.15 outlines
  individual scale plates; by 0.10/0.25 a visible part of that field has broken up.
- `CROP_5_membrane*.png` — the smooth field. At 0.02/0.06 the wandering non-relief contours
  are plain. At 0.05/0.15, 0.08/0.20 and 0.10/0.25 only the real vein ridge is traced. There
  is **no blue at all** in this crop: 0.4/0.8 finds nothing in a membrane field.

## 8. What this task does not settle

- **Nothing about whether a denser control produces a better dragon.** That is the re-pair's
  question and it is the Director's eye, not a number here. No structure metric is armed as a
  gate (Ruling 10d).
- **Whether a denser control over-constrains at cn-strength 0.9.** Not measurable from a clay
  render; it needs a generation, and this session did not run one.
- **`high` has no measured bound**, per §5–6. If the advisor wants one, the instrument that
  would produce it does not exist in this session's evidence and inventing it while looking at
  these results is the move this repo forbids.
- **The negative prompt still carries `photo`** against a register now ruled ultra-realistic —
  flagged in the predictions file *before* any measurement so it is on the record blind, and
  not changed here: it is a decided profile value, profile writes are the advisor's, and it
  would be a third variable in a run that already changes the register and the control.

## 9. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Grid, views, erosion depths, interior definition and the works-perfectly test all pre-registered in a commit that precedes the first Canny; all 64 rows plus the gradient comb land in `canny_sweep.json` beside the sheets; the anchor digits are arguments, recorded in the JSON |
| ANDON_AUTHORITY | **3** | The anchor **fired**, halted the sweep before a single row was written, and the mismatch was diagnosed rather than tuned past; there is no skip flag; the repair is an operand conformance whose retune test is stated and passes |
| NAMED_COMPENSATORS | **3** | New files only, all under `E12_repair/` and two new docs; silhouettes written to a fresh directory so `E12_pair/` was never opened for writing; clay renders reused read-only; no generation, no spend, nothing irreversible in scope |
| DECOMPOSE_BY_SECRETS | **3** | No subject constant baked into the tool — tag, views, crops, composite background, cuts and anchors are all arguments; the derived value is proposed, not written, because profile writes are the advisor's (Ruling 9e) |
| UNCERTAINTY_GATED_HUMANS | **3** | The proposal is split into a derived half and a judgement half and says which is which; the trade table and a named alternative go up rather than a single number; `high`'s absence of a bound is stated instead of filled |
| EXTERNAL_VERIFIER | **2** | The anchor checks this instrument against the tool it replicates, from digits that tool printed in a previous session — and it caught a real defect on first use. Marked 2 rather than 3 because the replica is now bit-identical arithmetic to its source, so it can no longer catch a bug the two share; and `skip:` on a second model, per precedent |

---

**Task 1 complete. HALT at the ruling gate.** `canny-low = 0.05` is derived; `canny-high` is
the advisor's to rule from §6's table. Task 2 spends credits on a control built from that
pair, so it does not begin on an unruled threshold.
