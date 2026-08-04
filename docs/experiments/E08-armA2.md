# E08 — Arm A2: stage 1 rebuilt on the raycast silhouette

**Spec:** [E08-cover-the-figure-with-reference.md](E08-cover-the-figure-with-reference.md) ·
**Ruling + Amendment 1:** [E08-ruling-gate0.md](E08-ruling-gate0.md) ·
**Arm A:** [E08-armA.md](E08-armA.md)
**Run:** 2026-08-03, executor session. **No diffusion, no GPU.** C1 read-only.

The change: `project_twins` answers *is there real surface here* from **geometry** — a raycast
of the view against the mesh it is already carrying in a raycasting scene — instead of from
`figure_mask` thresholding the clay render. `--mask-keyed` reproduces the historical path.
The edge erosion against the twin's **own paint** is retained; it answers the other question.

---

## Reproduction anchor

```
project_twins.py --mask-keyed ...   ->  sha b12917a2c7c14c4b
facet_E06/C1/styled_stage1.png      ->  sha b12917a2c7c14c4b     BYTE-IDENTICAL
```

Every arm before this one still reproduces exactly.

## Result

| | **shipped** (keyed mask) | **A2** (raycast silhouette) |
|---|---|---|
| mask used, front / back | 14.49% / 15.09% of frame | **19.01% / 19.01%** |
| styled, front | 391,407 | **555,185** |
| styled, back | 289,805 | **383,533** |
| **styled texels** | **681,212** | **938,718** |
| **styled / valid** | **28.4%** | **39.1%** |
| **styled / reachable** | **53.8%** | **74.2%** |
| holes into stage 2 | 1,721,598 | **1,464,092** |
| stage-1 atlas variance | 0.01733 | 0.02182 |

**+257,506 texels of reference**, from the two twins already on disk, with no diffusion and no
GPU. Arm A's counterfactual predicted 938,723; the rebuild landed on **938,718**, a difference
of 5 texels from bilinear-versus-exact rasterisation in the replica.

**`lost 0`.** No previously-styled texel was dropped — the change is strictly additive, so
nothing that was already trusted was traded away for the gain.

## The failure mode, checked

If the silhouette were too fat, recovered texels would sample the twin's **background** rather
than the figure. The twin background is a flat grey, RGB (126,126,126) front and (124,124,124)
back, so a contaminated texel would sit near ΔE 0 from it.

| | median ΔE from background | within ΔE 10 of it |
|---|---|---|
| **recovered** texels (257,506) | **38.31** | **0.18%** |
| previously-styled texels (681,212) | 38.99 | 0.32% |

The recovered set is **cleaner on this test than the set that was already trusted**. Confirmed
by eye at `facet_E08/A2/A2_stage1_compare.png` — the recovered surface carries skin on the
arms, green on the tunic, red on the skirt and gold on the pauldrons.

## What is still hole, and why it moved

The blade is still largely unstyled. It is no longer the mask holding it back — the silhouette
now contains the whole blade — but the **EDGE test**, which erodes against the twin's own
painted figure, and a blade only ~15 px wide in the twin has little interior left after a
3.8 px erosion from each side. That is the other 211,087 texels Arm A separated, and its
stated justification is void: the mesh is fatter than the twin (19.01% vs 17.43%), so eroding
the twin's mask *does* reach the mesh boundary. **Not touched here** — one variable.

---

## What this does not show

**Coverage is not quality.** This is a stage-1 atlas: the recovered texels carry the twin's
own colour by construction, so a ΔE comparison against that twin is near-zero by definition
and grades nothing. The ΔE instrument earns its keep on a **finished** asset, where recovered
reference displaces brush invention and interpolation — and that needs the eight-stroke loop,
which is GPU and is not authorised here.

So the claim this arm supports is exactly one: **reference coverage rises 28.4% → 39.1%**.
Whether the defect the Director rejected goes with it is E08's §2 question and is unanswered.

Artifacts: `facet_E08/A2/` — `styled_stage1.png` + `_holes.png` + `_styled_mask.npy`,
`repro_stage1.png` (the byte-identical historical path), `A2_stage1_compare.png`
(twin | shipped | A2, front and back).
