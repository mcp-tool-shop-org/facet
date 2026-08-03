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

## Addendum — W2 and the weld fix (same session)

**H2 — supported in direction, archived strength corrected.** W2 (`512`) and W3
(`1024_cascade`) land 0.02% apart in output faces (975,496 vs 975,300), so the comparison
is generation resolution, not budget. `1024_cascade` puts **42% more polygons on the
head** (89,972 vs 63,442). Qualitatively W2 has a soft rounded brow, shallow eye
depressions with no lid edge, and an unformed mouth; W3 has a creased brow bar, upper lid
edges, nostril wings, a formed mouth cavity and carved beard strands.

**The archived claim "`512` produced a face with no eyes" does not replicate.** W2 has
eyes — shallower, without lid definition. Direction confirmed, strength overstated. This
is the fourth inherited claim to fail in E01, after the clay provenance, the shell count
and the facial ceiling.

**The weld fix works — polygon budget allocation is unblocked.** Both arms at
`--target 150000`, identical protection settings:

| run | verts in | shells in | faces out | shells out | legs |
|---|---|---|---|---|---|
| `--no-weld` | 858,562 | 285,654 | 150,000 | 149,528 | shredded to lace |
| welded | 858,562 → 137,607 | 285,654 → **1** | 149,996 | **1** | intact |

Atlas undisturbed: every one of 287,230 surviving faces kept exact UVs; a textured flat
render of the welded 150k mesh differs from the 287k source by a mean of 0.47/255. Four
zero-area triangles (0.0014%) collapse in the merge — a triangle whose corners were one
point had no area to lose. **The `--no-weld` control reproduces the historical shredded
output exactly** (1,516 trimesh components, 102,698 verts, 24,573 KB, matching the
archived `final_report.json`), which is what makes this conclusive rather than suggestive.

## The constraint that E01 actually uncovered

TRELLIS caps input at **1024 px on the long side** (measured). A full-figure clay
therefore puts ~123 px on the head; a bust crop of the same clay puts ~600 px on the same
head. That cap — not reconstruction, not polycount, not the texture stage — is the
facial-structure ceiling this experiment set out to find.

It also means the bust crop's better face cannot ship on its own. `project_twins.py`
registers twins against the mesh bounding box, and a bust mesh (`extent
[1.0009, 0.4214, 0.4529]`, x-dominant) would misregister a full-figure twin by roughly 7×.
A textured bust is not a deliverable.

**So the open question is transfer:** how does the bust's facial geometry reach the
full-figure mesh? Head graft, or detail transfer from bust to full figure. That is E02,
and it is the highest-value unknown remaining.

## Standing correction to how this project reasons

Four claims failed in E01 — the clay provenance, the shell count, the facial ceiling, and
the strength of the `512`-has-no-eyes observation. All four were inherited from session
records and restated as fact, twice by the advisor inside a spec written specifically to
prevent that. The repo is the countermeasure and it worked: each was overturned by a
measurement that took minutes, because the claim sat next to runnable code.

The generalisable form: **an inherited claim is a hypothesis wearing a fact's clothes.**
The cost of checking one is minutes; the cost of building on one is a session.
