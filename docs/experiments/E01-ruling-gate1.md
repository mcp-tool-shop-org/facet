# E01 — advisor ruling at Gate 1

**Date:** 2026-08-04 · **Ruling on:** the executor's Gate 1 report (W3, W1, P3, P1)
**Director present:** yes — verdict on the sheet given directly

---

## H1 — SUPPORTED, both subjects

The bust crop puts **3.1–4.5× more polygons** on the head (W3 89,972 → W1 402,427;
P3 31,104 → P1 96,058), and the difference is structural, not cosmetic:

| | full-figure baseline | bust crop |
|---|---|---|
| eyes | continuous brow bar over a shallow recess, no lid structure | separated upper and lower lids around an eyeball form |
| brow | one undifferentiated mass | vertical furrow between the brows |
| nostrils (subject P) | two flat punctures, offset — the Director flagged these unprompted | modelled cavities with wings |

The executor predicted eyelid separation and a brow furrow before the sheet was built,
and disclosed the prediction was not blind. Both mechanisms are independently supported
by the polygon counts, which no one's eye influenced.

**Consequence:** the bust-crop pass is promoted from experiment to route. It is now in
the README as a pipeline stage.

## The experiment's own premise — FALSIFIED

A0 and W3 come from the same clay. A0 is a featureless faceted blob; W3 has a brow, eye
sockets, a nose with nostrils, a moustache and a sculpted beard.

**Reconstruction was never the facial-structure ceiling.** The shipped mesh — whose crude
face motivated this entire experiment, and on which the whole texture pipeline was
built — was a bad generation, not evidence about what reconstruction can do. Every
conclusion drawn from "the face is crude in the clay render" was reasoning from one
defective artifact.

The Director's verdict on the sheet, unprompted: proportions are correct now — the
bearded warrior is no longer collapsed into dwarf proportions as the shipped asset was.
That is an A0-vs-W3 difference at identical input, so it is generator/settings evidence
(H3) obtained for free.

## Shell soup — FALSIFIED, and the fault is ours

| mesh | connected components |
|---|---|
| raw reconstruction (`warrior/mesh.glb`) | 1 |
| four fresh reconstructions | 40–191 (92–98% of faces in one shell) |
| `hero_bake/prep_uv.glb`, `texpass/warrior_texpass.glb` | 285,654 |

The "~8,600 shells" figure in the spec and README was inherited from a session record and
never checked. It is wrong in both directions: reconstruction gives a connected surface,
and our own pipeline produces far worse fragmentation than the number claimed.

Fragmentation appears **after UV unwrap and glTF export**, which splits a vertex at every
UV seam — with per-triangle islands that is one shell per face. `smart_decimate` was then
handed that mesh. Collapse decimation merges neighbours; per-triangle shells have none.
The shredded legs were our export talking, not the generator.

**Ruled fix:** weld before decimating. Blender stores UVs per-loop rather than per-vertex,
so merge-by-distance restores connectivity without disturbing the atlas. Cheap, local,
untested — the next thing to try.

## Remaining arms — ruled

- **W2 (`512`)** — RUN. Cheap (~55 s), closes H2, and directly tests an unreplicated
  archived claim about generation resolution.
- **W4 / W5 (local Tripo)** — DEFER, do not run now. H4 is answered: reconstruction
  already returns connected surfaces, so Tripo's topology argument evaporates. H3's value
  also dropped now that TRELLIS visibly produces real faces. Standing up an untested
  generator is no longer the best use of the next GPU hour.

## What the next hour is worth more on

1. **The weld fix** — unblocks polygon budget allocation, which is the Director's stated
   route.
2. **Re-run the texture pipeline on W1 instead of A0.** Every texture result to date was
   produced on a blob. The pipeline has never been tried on a mesh with a real face, so
   nothing about its output quality has actually been tested.

## Standing correction to how this project reasons

Three claims failed in E01 — the clay provenance, the shell count, and the facial ceiling.
All three were inherited from session records and restated as fact, twice by the advisor
inside a spec written specifically to prevent that. The repo is the countermeasure and it
worked: each was overturned by a measurement that took minutes, because the claim sat next
to runnable code.
