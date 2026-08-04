# E08 — Gate 0

**Spec:** [E08-cover-the-figure-with-reference.md](E08-cover-the-figure-with-reference.md) ·
**Prior ruling:** [E07-ruling-gate1.md](E07-ruling-gate1.md)
**Run:** 2026-08-03, executor session. **No GPU, no diffusion, nothing written to C1.**
**Instruments:** [`e08_ceiling.py`](../../tools/diagnostics/e08_ceiling.py) ·
[`e08_metric_probe.py`](../../tools/diagnostics/e08_metric_probe.py) ·
[`e08_deltaE.py`](../../tools/diagnostics/e08_deltaE.py)

Evidence, not argument.

---

## The spec's source claims, checked first

| claim | verdict |
|---|---|
| `restylize_views.py` takes `--inputs` as an arbitrary list, no two-view assumption | **holds** — `nargs="+"`, and the body loops over what it is given |
| `project_twins.py` hardcodes two in `VIEWS` at 132–137 while its ownership machinery is N-view shaped | **holds** — `best_w`/`owner_c`/`sumW`/`sumWC` all accumulate `for view in VIEWS` |
| `basis(yaw, el)` supplies a correct frame for any yaw | **holds**, and it is now asserted rather than assumed: `e08_ceiling.py` halts unless the generalised `dtc(0°)` and `dtc(180°)` reproduce project_twins' hardcoded `(0,-1,0)` and `(0,1,0)` exactly |
| `project_twins.py` already computes `reachable` | **holds** — line 196, set after facing and depth, before the edge test |
| `ig2mv_licensefree.py` makes six consistent views | **exists**, with a structural licence tripwire on nvdiffrast. Not exercised here |

---

## Half 1 — the geometric ceiling. **PASSES.**

Reachable = facing > threshold ∧ depth-visible, project_twins' own construction, unioned over
equatorial camera ladders on C1's prep. 2,402,810 valid texels.

| cameras | production (body 0.45 / head 0.18) | uniform 0.45 | uniform 0.18 |
|---|---|---|---|
| 2 | 52.66% | 43.27% | 56.69% |
| 4 | 63.78% | 56.68% | 66.53% |
| 6 | 71.15% | 65.48% | 73.08% |
| **8** | **74.10%** | **68.52%** | **76.06%** |
| 12 | 75.90% | 70.36% | 77.72% |
| 8 + 2 elevated | 76.41% | 73.21% | 77.91% |
| 12 + 2 elevated | 77.69% | 74.61% | 79.06% |

**Halt condition was "8 cameras do not clear 60%". Measured 74.10%. The gate passes.**

### Marginal gain, production thresholds, added in turnaround order

```
+yaw   0  ->   709,466   29.53%   (+709,466)
+yaw 180  -> 1,265,391   52.66%   (+555,925)   <- the two shipped twins
+yaw  90  -> 1,384,600   57.62%   (+119,209)
+yaw 270  -> 1,532,567   63.78%   (+147,967)
+yaw  45  -> 1,616,107   67.26%   (+83,540)
+yaw 135  -> 1,652,831   68.79%   (+36,724)
+yaw 225  -> 1,736,237   72.26%   (+83,406)
+yaw 315  -> 1,780,546   74.10%   (+44,309)
```

### The acceptance stage discards nearly half of what the cameras reach

The twins styled **681,212** texels of the **1,265,391** their two cameras can reach — **53.8%**.
The other 46.2% passed facing and depth and were then rejected by the edge-distance and
mask tests. Those tests exist for a measured reason (E01's silhouette-band and
background-keying failures), so this is not a bug.

It is a bound on this spec's own thesis, and it is an **estimate, not a measurement**, because
the rejection rate at a diagonal camera is untested: if 53.8% acceptance holds at eight views,
reference coverage lands near **74.10% × 53.8% ≈ 40%** of valid texels, not 74%. Camera count
raises the ceiling; it does not touch the acceptance rate, and the two multiply.

---

## Half 2 — the metric. **Cannot run as specified. Substituted, and the substitute validates.**

### Hold-one-out at N = 2 has a population of exactly zero

Structural, not a bug. `project_twins` accepts at `facing > 0.45`; front `dtc` is `(0,-1,0)`
and back is `(0,1,0)`, so `facing_front = -N_y` and `facing_back = +N_y` cannot both clear any
positive threshold.

```
twin front reachable   709,466
twin back  reachable   555,925
OVERLAP                      0     <- the hold-one-out population at N=2
```

A texel is comparable only if **two or more** reference cameras pass it:

| cameras | reachable | comparable (≥2) | of reachable |
|---|---|---|---|
| **2** | 1,265,391 | **0** | **0.0%** |
| 4 | 1,532,567 | 496,399 | 32.4% |
| 6 | 1,709,548 | 1,212,727 | 70.9% |
| **8** | 1,780,546 | **1,422,906** | **79.9%** |
| 12 | 1,823,725 | 1,641,032 | 90.0% |

**Hold-one-out is a sound metric for R8 and cannot be validated on C1.** §5 half 2 asks for
both from the same construction, and no camera count satisfies both.

### The substitute, and why it answers §4's actual requirement

§4's requirement is that the instrument fire on the defect before it grades anything. The
nearest computable construction on the rejected asset is **reference agreement**: sample the
finished atlas through a twin camera's own rays and compare against that twin in CIE Lab.
Sampling is straight from the atlas, **not through a Blender render** — the render applies
`exposure 0.85` under the Standard view transform, a nonlinear remap that would land entirely
in ΔE. ΔE is CIE76; **2.3 ≈ JND and >10 ≈ plainly different colour** are external constants.

Where a texel came from the twin, agreement is near-perfect by construction — which is the
metric's null, and it needs to be near zero or the instrument is worthless.

| provenance | front px | median ΔE | >10 | back px | median ΔE | >10 |
|---|---|---|---|---|---|---|
| **TWINS** (this reference) | 58,124 | **0.72** | **0.4%** | 63,817 | **0.67** | **0.2%** |
| BRUSH (invention) | 15,092 | **23.18** | 81.3% | 10,538 | **12.28** | 59.2% |
| DILATION (interpolation) | 3,333 | **18.70** | 65.0% | 10,244 | **14.77** | 55.8% |
| core, facing > 0.45 | 70,153 | 0.89 | 15.6% | 77,193 | 0.81 | 10.7% |
| grazing band | 6,396 | 12.96 | 59.1% | 7,406 | 10.42 | 51.7% |

**The null sits at ΔE 0.7 and non-reference sits 18–32× above it.**

### Does it separate the regions the Director named?

Boxes placed by hand from the diagnostic sheet, then **checked against the reference's own
median colour** rather than trusted — a blade box that is not sitting on steel is a
mis-placed box.

| region (front view) | reference RGB | asset RGB | median ΔE | >10 |
|---|---|---|---|---|
| **blade**, non-reference surface | (123,122,124) *neutral steel* | **(147,97,63)** *flesh* | **32.71** | **92.8%** |
| **forearm R**, non-reference | (80,63,50) | (50,33,18) | **18.53** | 79.6% |
| **greave / thigh**, non-reference | (74,61,49) | (54,36,28) | **14.93** | 70.2% |
| **boots**, non-reference | (56,53,51) | (44,42,41) | **8.84** | 46.3% |
| *CONTROL* beard, whole box | (115,47,27) *red* | (114,47,27) | **0.51** | 1.5% |
| *CONTROL* tunic, whole box | (15,39,32) *green* | (15,39,32) | **0.49** | 0.8% |

**It separates them by 18–65×.** The controls the Director did not name sit at ΔE ≈ 0.5; every
region he did name sits at 8.8–32.7 on its non-reference surface. The blade's numbers are the
sentence *"the blade wears skin tones"* in measured form: neutral steel (123,122,124) replaced
by flesh (147,97,63).

**Halt condition was "if it does not separate the named regions". It separates them.**

### The structural result underneath

Defect severity tracks reference coverage, per region:

| region | non-reference share of box | whole-box median ΔE |
|---|---|---|
| blade | **62%** | **23.17** |
| forearm R | 27% | 0.93 |
| greave / thigh | 21% | 1.09 |
| boots | 33% | 1.44 |
| tunic (control) | **1.2%** | **0.49** |

The blade is the loudest defect because it has almost no reference on it. The tunic is clean
because it is almost entirely reference. That is E08's thesis, measured on the rejected asset
rather than argued — and it is the first instrument in this repo that says so.

---

## Predictions

| # | prediction | outcome |
|---|---|---|
| A1a | rises steeply 2 → 6, flattens by 8 | **CORRECT** — 52.66 → 71.15, then +2.95 to 8 and +1.80 to 12 |
| A1b | most of the gain is the four diagonals | **FALSIFIED** — the two sides add 267,176, the four diagonals 247,979. Half the cameras, more surface |
| A2 | 8 cameras above 80% at facing > 0.45 | **FALSIFIED** — 68.52% at uniform 0.45, 74.10% at production. 12 cameras + 2 elevated at 0.18 still reaches only 79.06% |
| A3 | hold-one-out ΔE separates the named regions on C1 | **the construction is impossible at N=2**; the substituted reference-agreement ΔE separates them by 18–65× |
| A4 | independent views disagree less than the material error they replace | untested — needs R8 |

---

## Gate 0 verdict

**Half 1 passes** — 74.10% against a 60% floor, and A2's 80% is out of reach at any camera
count tested.

**Half 2's specified construction is impossible** and its substitute clears the bar it was
meant to clear. Two things need the advisor rather than the executor:

1. **The substitution needs ratifying or rejecting.** Reference agreement is not hold-one-out;
   it validates that ΔE-in-Lab sees the defect, which is what §4 was for, but the metric R8
   would be graded on is still unvalidated on a rejected asset — and no asset exists that
   could validate it, because hold-one-out needs ≥4 cameras and C1 has 2.
2. **The 40% estimate.** If acceptance stays at 53.8%, eight views buy reference coverage
   around 40% of valid texels, up from 28.4%. That is a real move and it is not "cover the
   figure". Whether the acceptance stage is the second lever — or the first — is a ruling.

Artifacts: `facet_E08/gate0/` — `ceiling.json`, `probe.json`, `dE_front.json`, `dE_back.json`,
and the four-panel sheets `dE_front.png` / `dE_back.png` (reference | asset | provenance | ΔE heat).
