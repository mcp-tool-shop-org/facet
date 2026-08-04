# E08 — Arm A: what each acceptance test costs

**Spec:** [E08-cover-the-figure-with-reference.md](E08-cover-the-figure-with-reference.md) ·
**Ruling that ordered this arm:** [E08-ruling-gate0.md](E08-ruling-gate0.md) ·
**Gate 0:** [E08-gate0.md](E08-gate0.md)
**Run:** 2026-08-03, executor session. **No twins, no diffusion, no GPU. No atlas written.**
**Instrument:** [`e08_acceptance.py`](../../tools/diagnostics/e08_acceptance.py)

**Verification anchor:** the replica of `project_twins`' acceptance reproduces E06's measured
TWINS provenance — **681,212** texels — exactly, and the tool asserts it. Every number below
rests on that.

---

## 1. The reorder premise is falsified

The ruling: the absolute facing gate at line 185 runs before the comparative ownership rule
at line 222, so *"a texel seen obliquely by every camera gets discarded by all of them
instead of assigned to the one that sees it best."*

Tested by construction at three floors — accept-then-own against own-then-accept:

| floor | absolute gate | comparative ownership | identical |
|---|---|---|---|
| 0.45 | 681,212 | 681,212 | **yes** |
| 0.25 | 700,758 | 700,758 | **yes** |
| 0.10 | 710,391 | 710,391 | **yes** |

**It is a no-op**, and the reason is in the loop: `project_twins` accumulates each view's
accepted set *independently* and then takes `w > best_w`. A texel the best-facing view
rejects is **already** supplied by a worse-facing one. The fallback the reorder was meant to
add is present in the shipped code.

## 2. And the facing floor is not the lever either

With the edge and mask tests still applied, dropping the body floor all the way to 0.05:

| body floor | 0.45 | 0.35 | 0.25 | 0.18 | 0.10 | 0.05 |
|---|---|---|---|---|---|---|
| styled | 681,212 | 692,090 | 700,758 | 706,023 | 710,391 | 712,588 |
| % of valid | 28.35% | 28.80% | 29.16% | 29.38% | 29.57% | 29.66% |
| acceptance rate | 53.8% | 53.1% | 52.3% | 51.8% | 51.2% | 50.8% |

**+31,376 texels, +1.31 points, for a nine-fold reduction in the threshold** — and toward
the setting the Director already rejected (streak bands on skull sides and sword, 2026-08-04).
The facing gate is not where the 46.2% goes.

---

## 3. Where it does go

Production floors (body 0.45 / head 0.18):

| | reachable | accepted | lost | EDGE only | MASK only | both |
|---|---|---|---|---|---|---|
| front | 709,466 | 391,407 | 318,059 (44.8%) | 98,406 | **163,783** | 55,870 |
| back | 555,925 | 289,805 | 266,120 (47.9%) | **112,681** | 93,728 | 59,711 |
| **union** | **1,265,391** | **681,212** | **584,179 (46.2%)** | | | |

Counterfactual coverage, one test removed at a time:

| | styled | % of valid | vs shipped |
|---|---|---|---|
| as shipped | 681,212 | 28.35% | — |
| no EDGE test | 892,299 | 37.14% | **+211,087** |
| no MASK test | 938,723 | 39.07% | **+257,511** |
| neither test | 1,265,391 | 52.66% | +584,179 |

These are coverage counts from the acceptance replica, **not rebuilt assets**. Whether
recovered texels look right is not measured here.

---

## 4. The MASK test rejects because the mask is missing a quarter of the figure

`project_twins` treats `*_mask.png` as the mesh silhouette. It is not. Measured against the
silhouette itself, which the raycasting scene already in the tool produces for free:

| | front | back |
|---|---|---|
| **true mesh silhouette** (raycast) | **146,356 px** | 146,356 px |
| mask as used (saved, un-eroded) | 111,602 | 116,207 |
| **mesh NOT in the mask** | **34,970** | **30,348** |
| mask not on the mesh | 216 | 199 |
| IoU | 0.7599 | 0.7916 |

The mask is a near-strict **subset** of the silhouette, short by ~24%. Registration is not
the cause — a ±12 px search puts the best IoU at shift **(0,0)** front and **(1,0)** back.

**And the loss is interior, not a rim** (`facet_E08/armA/mask_vs_mesh.png`): a dense stripe
down the entire length of the blade, and patches through the pauldrons, chest, greave plates,
boots and skirt — following shading boundaries.

The mechanism is already in this repo's own record. `figure_mask` keys the **clay render**
against its corner-median background at `tol 0.06`, and `CLAUDE.md` states the property that
breaks: *"A Workbench clay render is flat grey on flat grey by design."* E01 hit this exact
wall with Canny, which returned 0.84% edge pixels, and fixed it by compositing onto a
contrasting background before keying. **The mask path never received the same fix.**

The silhouette is available exactly, for free, from the raycasting scene `project_twins`
already builds — and by `CLAUDE.md`'s own rule a depth-visible texel projects inside it by
definition, so after the visibility test the check is close to a no-op.

---

## 5. A documented claim is wrong, and the EDGE test rests on it

`project_twins` lines 158–161 justify eroding the twin's mask:

> *"The twin is painted fatter than the mesh (measured 15.8% of frame against 9.9%, IoU 0.777),
> so eroding the TWIN's mask never reaches the mesh boundary while still excluding background."*

Both numbers reproduce exactly — against the wrong objects:

| quantity | % of frame | what E01 called it |
|---|---|---|
| twin painted figure, **eroded** | **15.81%** | "twin … 15.8%" ✓ |
| **saved keyed mask**, raw | **9.94%** | "the mesh … 9.9%" ✗ |
| **true mesh silhouette** | **19.01%** | never measured |
| twin painted figure, un-eroded | 17.43% | — |

The comparison was **twin against mask**, not twin against mesh. Against the silhouette:

```
twin 17.43%   vs   MESH 19.01%      IoU 0.911  (not 0.777)
mesh silhouette falling OUTSIDE the twin's painted figure:  12,625 px
```

**The mesh is fatter than the twin, not the other way round.** So eroding the twin's mask
*does* reach the mesh boundary, and the premise that made the EDGE test safe is void. That
test costs 211,087 texels.

Verified by eye before reporting (`facet_E08/armA/silhouette_check.png`): the raycast
silhouette outline hugs the painted twin — sword, pauldrons, skirt, greaves, boots, open hand
— so the silhouette is correct and registered, and the discrepancy is the mask's.

---

## 6. Two corrections to my own instruments

- **A vacuous guard, caught and replaced.** My first version of the mask check compared the
  saved mask against *its own dilation*, which cannot lose a pixel by construction and
  returned 0.00% at both views. I reported it as untested rather than as confirmation, and
  replaced it with the comparison against the raycast silhouette. Same failure family as
  E06's silhouette-IoU gate: a check that could not see its own failure.
- **A hypothesis dropped on measurement.** The one-sided red band in the rejection overlay
  suggested a registration offset. The shift search found none.

---

## What Arm A did not do

No arm was built. `project_twins` is unmodified, C1 is untouched, and §4 of the ruling asked
for costs in texels, which is what is above. Rebuilding stage 1 with a raycast silhouette in
place of the keyed mask is the obvious next step and it is **not** taken here — the ΔE
instrument from Gate 0 can grade it, and whether the recovered surface is *good* is the
Director's call at a gate.

Artifacts: `facet_E08/armA/` — `acceptance.json`, `rejections.png` (twin | mask | rejections,
per view), `mask_vs_mesh.png`, `silhouette_check.png`.
