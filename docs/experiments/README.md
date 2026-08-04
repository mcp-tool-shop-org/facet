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
| [E02](E02-texture-stage-on-sound-inputs.md) | Is the texture stage sound when its inputs are? Every texture result in this project was produced on a blob mesh with twins belonging to a different silhouette. | **RULED — answer is NO** → [Gate 1 ruling](E02-ruling-gate1.md). Director rejected with every input sound. Two twins + eight cameras paint only ~25% of the surface; the rest is interpolated across a 35,070-island atlas where neighbours are unrelated pieces of the model. Next target is the UV unwrap, not the brush. |
| [E05](E05-paint-more-surface.md) | Why is three quarters of the asset interpolated rather than painted? | **RULED** → [Gate 0](E05-gate0.md). Neither lever moved it. **49% of valid atlas texels are never visible from any of 46 exterior cameras** — half the surface the atlas pays for is not on the outside of the model. Native xatlas UVs adopted permanently |
| [E06](E06-cull-the-unseeable.md) | Does culling exterior-invisible faces before unwrapping fix coverage, atlas efficiency and the artifact mechanism together? | **RULED** → [report](E06-report.md), [Gate 1 ruling](E06-ruling-gate1.md). Culling works and the blade is fixed by the Director's eye. Interpolation fell **68%** (2,551,893 → 813,773 dilated texels), brush share 27% → **52.7%**. Two predictions falsified: density rose ~17% not 2×, because **charts fragment under culling rather than merging**. Atlas layout is now the binding constraint |
| [E07](E07-the-atlas-is-not-a-neighbourhood.md) | The loop writes colour from two places and neither knows where a texel's neighbours are *on the surface*. Does giving it one remove the defect class the Director named? | **SPEC — highest priority.** Commit has no levelling term; finalize's flood is not island-constrained despite its docstring. E08 waits on it and is partly defused by it |
| E08 | Chart fragmentation — the binding constraint on texel density. Culling removed 47% of faces but only 34% of charts. Remeshing is the untested candidate. | needs a clean premise of its own; do not entangle with a texture measurement |
| E03 | How does the bust crop's facial geometry reach the full-figure mesh — head graft, or detail transfer? | unblocked (E02 ruled). Ordering against E04 is the Director's call; neither depends on the other |
| E04 | Does the route hold on a **non-character subject**? A galleon: landscape framing, no face to anchor density on, and thin rigging everywhere. | inputs staged; ordering against E03 is the Director's call |

**E04 inputs staged** — `E:\AI\training\facet_next\galleon_clay\`, three form-first clay
variants at 1216×1024 (sha256 `59c25940075dca93`, `80263b1551d5fd7b`, `bb8da35402cf2a10`).
Known stressors, recorded before the spec is written: the pipeline's framing is
portrait-shaped throughout (`turn_render` 752×1024, `project_twins` deriving `h_ext` from
`v_ext × 752/1024`, `ortho_scale` on the larger dimension) and a ship is wider than tall —
the same class of break the bust mesh caused; `smart_decimate` allocates density by *face*
rect and a galleon has none; the thin-extent probe will fire on the entire rig, which may
be correct or may withhold most of the subject; and `gate_mesh.py` is character-only and
must not be run on it.

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
- **The gutter, not the island count, ate the atlas.** Two meshes at an identical 287k
  faces: A0 packs 8,486 islands (34 faces each) into 20.34% of a 4096 atlas; a decimated
  mesh packs 35,070 islands (8 faces each) into 4.01%. Dropping `island_margin`
  0.004 → 0.001 took it **4.01% → 18.76%**. Raising `angle_limit` 1.15 → 1.50 moved island
  count by **0.8%** and bought nothing — `smart_project` splits on UV distortion, not angle
  alone, and decimation's long thin triangles distort regardless of the threshold. The
  advisor predicted the opposite; the margin was the entire gain.
- **Atlas packing and styled coverage are independent.** Valid texels rose 4.7× and styled
  texels rose 5.4× — the ratio barely moved, falsifying the "most valid texels are
  bake-margin halo" hypothesis.
- **⚠ The coverage baseline was contaminated, and the floor built on it was void.**
  `figure_mask` keys A0's twin over its own background: **30.2% and 32.3% of the bottom
  corners** register as figure, where a centred standing figure cannot reach. A0's twin is
  painted concept art with a background gradient and a cast shadow, and a flat top-corner
  median at tol 0.06 keys a third of the lower background as paintable surface. The
  clinching arithmetic: A0 styles **81–100% of its geometrically orientable texels** against
  a two-view ceiling of 61.5% — a number brushing an unreachable ceiling is a broken
  measurement, not a good result. Measure **`styled / geometrically-reachable`**, which has
  a true ceiling of 1.0 and is comparable across silhouettes; and take the mask from the
  render the twin was restylized from, where it is exact and registered by construction,
  rather than re-keying the twin heuristically.
- **Consequence for shipped work:** the warrior the Director rejected has background grey
  projected into its atlas, and a contaminated mask also disables the edge guard meant to
  keep silhouette pixels out. Three independent faults in that asset — poor geometry, twins
  never registered to it, background baked into the texture. None of them the texture
  architecture.
- **Prompt per view.** A shared prompt asking for "a long red beard, gold necklace" on every
  view overrode a correct ControlNet contour and put a face on the back of the head at both
  0.92 and 0.75 denoise. Per-view prompting fixed it outright — face detections 1 → 0
  against a source-back control of 0, with silhouette held at IoU 0.784.
- **⚠ The exported mesh is not a solid — no volumetric predicate works on it.**
  `prep_uv.glb` carries **293,099 verts for 287,170 faces**: the glTF export splits a vertex
  at every UV seam, so every island boundary is a topological crack. `compute_signed_distance`
  at the figure's own bbox centre — the middle of a standing warrior's chest — returns
  **+0.0019**, i.e. *outside*. Ray parity leaks, containment is meaningless, and only **37%**
  of outward rays escape. Any query needing thickness, containment or inside/outside must run
  against the **welded mesh before export**. Related trap: a ray cast along the surface normal
  measures the *tessellation*, not the geometry — median reported thickness 0.00204 against a
  median edge length of 0.00290 is a sub-triangle hit on a neighbouring face.
- **Thinness is a property of the surface, not of a camera.** A two-sided camera-ray extent
  probe (`extent = 2D − t_front − t_back`) needs neither normal nor interior, so it survives
  the above — but it reads a blade as *thick* when the blade is edge-on to that camera, and
  withheld only 49.9% of the sword column at yaw 90. The general form is to compute the thin
  mask per view, back-project to texels, and **union across views**.
- **A masked inpainting brush invents when it is starved of context.** At denoise 1.0 hole
  texels have nothing to preserve, so the model anchors only on prompt and contour. At yaw 90,
  95% of the figure is hole — the worst-anchored camera in the set, furthest from both styled
  poles — and the brush returned a plaited rope belt where the twins have a flat leather band,
  a shoulder strap over bare flesh, and a tunic extended from waist to mid-thigh. **Order the
  strokes to spiral outward from the styled poles** (45 → 315 → 135 → 225 → 90 → 270), so each
  stroke extends an existing character rather than composing a new one, and each commit
  anchors the next.
- **One mask cannot answer two questions.** *Is there real surface here* is answered by the
  mesh silhouette, un-eroded — a visible texel always projects inside it, by definition.
  *Is the paint here trustworthy* is answered by the twin's own painted figure, eroded.
  Conflating them and eroding the mesh mask cost **480k texels**: near the silhouette the
  surface turns edge-on and enormous numbers of texels foreshorten into a thin band, so
  peeling a few pixels off it removes far more than the same peel anywhere else. The bug was
  invisible under the old heuristic mask, which keyed *wider* than the mesh so erosion ate
  background instead of surface. `mesh_mask ∧ erode(twin_mask)` took styled coverage
  **23.8% → 53.7%** of reachable with the denominator unchanged.
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
