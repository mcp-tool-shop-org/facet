# Experiments

Each experiment is a spec written by an advisor session, run by a separate executor
session, and judged by the Director. The separation is deliberate: the session that
designs an experiment does not get to grade its own results, and the session that runs
it does not get to decide what the results mean.

**A spec is written before the work. A report is written after. Conclusions come last,
from the advisor, only once the Director has seen the evidence.**

| id | question | status |
|---|---|---|
| [E01](E01-facial-structure-ceiling.md) | Where is the facial-structure ceiling — framing, generation resolution, generator, or reconstruction itself? Does any configuration produce a connected surface rather than shell soup? | **RULED** → [Gate 1 ruling](E01-ruling-gate1.md) |
| E02 | How does the bust crop's facial geometry reach the full-figure mesh — head graft, or detail transfer? | spec pending |

### What E01 established

- **Reconstruction is not the facial ceiling.** The generator's **1024 px input cap** is:
  worked through the preprocessing path, a full-figure clay puts **~138 px** on the head
  and a bust crop of the same clay puts **~439 px** — about **3.2×**.
- **The styled twins are bound to the mesh they were rendered from.** They are a
  derivative of one specific silhouette, not a reusable asset, so twin generation is a
  pipeline stage rather than an input. Any new reconstruction — or head graft — needs
  its own twins.
- **Canny cannot find a silhouette that isn't there.** A Workbench clay render is flat
  grey on flat grey by design, so Canny returns 0.84% edge pixels and almost no outer
  contour — the ControlNet then constrains nothing and the model regenerates the
  character freely. Composite onto a contrasting background *and* union the figure mask's
  morphological gradient into the edge map: silhouette IoU went 0.290 → **0.777**.
  The recipe had been developed against lit concept art and carried to flat renders.
- **Polygons and texels are separate budgets.** `smart_decimate` allocates polygons;
  `bake_hero_prep`'s island scaling allocates texels. A head can hold 84% of the faces and
  45% of the texel area at the same time. A gate comparing UV area to *face count* is
  meaningless on a deliberately non-uniform mesh — compare UV area to **3D surface area**.
- **UV island count drives atlas efficiency, and margins are tuned to it.** Two meshes at
  an identical 287k faces: A0 packs 8,486 islands (34 faces each) into 20.34% of a 4096
  atlas; a decimated mesh packs 35,070 islands (8 faces each) into 4.01%. At a fixed
  16 px gutter, a 4× island count is a silent catastrophe.
- **Framing is a route stage, not a tweak** — 3.1–4.5× head polygons, and the gain is
  separated eyelids, a brow furrow and modelled nostril cavities rather than sharper blur.
- **Shell soup was ours.** Reconstruction returns 1 connected component; our UV unwrap and
  glTF export split it into 285,654. Welding before decimating restores it, verified
  against a control that reproduces the old broken output byte-for-byte.
- **Four inherited claims failed** — the clay provenance, the shell count, the facial
  ceiling, and the strength of an archived resolution observation. An inherited claim is a
  hypothesis wearing a fact's clothes: checking one costs minutes, building on one costs a
  session.

## Why it works this way

An earlier arc of this project ran ten sessions in which each session judged its own
output, wrote its conclusions to a shared memory store, and the next session read those
conclusions as established fact. Errors compounded silently because nothing in the loop
was checkable and nothing was gated on the Director's eye.

The repo is the fix. A claim sitting next to runnable code can be tested in minutes.
A tool marked *superseded* with its failure documented cannot quietly become doctrine,
because anyone can run it and watch it fail the same way.
