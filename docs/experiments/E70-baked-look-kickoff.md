# E70 — the look that can fail: baked mesh beside its twin

**Advisor spec, 2026-08-19. One executor seat (Sonnet), background. Tree
`E:\AI\training\facet_E70\`. ZERO CLOUD. NO BRUSH. Free.**

**Direction (the Director, 2026-08-19, paraphrased):** pack the prep mesh with the widescope
atlas, render the eight E58 cameras, and put the accepted twin beside the baked mesh at the
same zoom and crop. The halt lifts for a look, not for a brush. If the sheet fails, the
brush does not open; if it holds at his eye, then stroke one is discussed.

## ⚑ THE RULING THAT MUST STAY IN THE SPEC

E69's ANDON reads **0.00% on 8/8 views** and the 2% limit passes 8/8. **The withhold
predicate and the ANDON's re-test share one array and one comparison, so a zero residual is
the code agreeing with itself.** Quote it as **self-consistency**. **Never** quote it as
*the bake is good*. This arc exists precisely because that number cannot answer the question.

**What is load-bearing from E69**, and all of it survives: 1,468 new holes at **0.0423%**;
**99.7%** of them the garment-edge set finally becoming holes; **four** genuinely new texels;
**the silhouette is not systematically fat**.

## Inputs

| | |
|---|---|
| mesh | `prep_uv.glb` (E67 Stage 1) |
| atlas | `E:\AI\training\facet_E69\bake\atlas_widescope.png` |
| cameras | the eight E58 ring cameras — the same ones the twins were generated against |
| twins | `E:\AI\training\facet_A1_accepted_ring\` — verify sha256 against MANIFEST.json first |

## The work

Pack mesh + atlas, render all eight cameras, build the sheet: **accepted twin | baked mesh,
same zoom, same crop, per view.** Full-size PNGs on disk beside it.

**Render textures under FLAT light** — a Workbench STUDIO render is not a texture readout and
two debugging rounds were lost to that. Blender only through PowerShell.

## What the sheet must be able to show — the Director's five, named so the seat cannot miss one

The sheet is built so each of these would be **visible if present**. The seat does not judge
whether any occurred; it renders honestly at a zoom where they *could* be seen, and describes
panel content factually with uncertainty stated (E64's law: a seat's sentence about its own
output is not a measurement).

1. **Seams** — chart boundaries showing as visible discontinuities.
2. **Through-projection** — paint from a far surface landing on a near one.
3. **Bald crown** — E69's holes concentrate at the crown by construction; this is where they
   read.
4. **Cream-as-wall** — the shirt taking backdrop grey, the collision E67 measured at 4.12 dE.
5. **Identity gone** — the man not being this man.

Include at least one **head crop** and one **collar/vest-opening crop** per view at the
Director's zoom, since three of the five live there.

## ⚑ FOOTER — verbatim, on every panel

> The warm rim light in the twins is still paint.
> The overlay dots are still the map.

## Gates

- **Gate A** — no cloud call.
- **Gate B** — twin sha256 verified against the manifest before use.
- **Gate C** — the atlas and mesh are used unmodified; hashes recorded. Re-baking, retouching
  or filling holes is out of scope and a halt.

## Out of scope, named

Any brush or stroke; re-baking; hole filling or dilation; retuning `bg-max-pct` (2.0) or
`bg-de` (10); treating E69's ANDON pass as an answer; binding, which still does not gate
this; regenerating anything.

## Standards compliance

1. **PIN_PER_STEP — 3.** Mesh, atlas, cameras and twins pinned by hash; nothing regenerated.
2. **ANDON_AUTHORITY — 2.** Gates A/B/C halt; a failing look is a reported result and closes
   the brush.
3. **NAMED_COMPENSATORS — 2.** Zero spend; new tree; repo edits by pathspec.
4. **DECOMPOSE_BY_SECRETS — 2.** Pack / render / sheet separable over on-disk artifacts.
5. **UNCERTAINTY_GATED_HUMANS — 3.** The whole arc is a look for the Director; the brush is
   gated on it and the seat cannot open it.
6. **EXTERNAL_VERIFIER — 3.** The verifier here is the Director's eye on an artifact that
   **can fail** — deliberately replacing a ratio that could not.
