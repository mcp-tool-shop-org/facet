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
| [E07](E07-the-atlas-is-not-a-neighbourhood.md) | The loop writes colour from two places and neither knows where a texel's neighbours are *on the surface*. Does giving it one remove the defect class the Director named? | **RULED — CLOSED, neither arm adopted** → [Gate 1 ruling](E07-ruling-gate1.md). Director: *"the images don't look good"*, and on being asked which defect, **"all of it — the asset is not close"**. The finding is a measurement failure: **four of the five units this experiment graded on are 5×5 high-pass statistics** and the defect that decides acceptance is a *large region of the wrong material*, which is smooth inside itself and registers only its rim. L1 cut dilation source distance **70×**, took mean fallback 734 → 0 and speckle below A0 — and changed nothing to the eye. Structural read: **28.4% twins / 37.7% brush invention / 33.9% interpolation** — four experiments improved how the other 71.6% is filled, none reduced it. Next is a free geometry pass on the twin-projection ceiling at N = 2/4/6/8 views, **not** another fill arm. Evidence: [Gate 0](E07-gate0.md), [Gate 0.5](E07-gate0_5.md), [report](E07-report.md), [Amendments 1-2](E07-the-atlas-is-not-a-neighbourhood.md). Both premises held: **74.9%** of dilated texels took colour from another island, from a median **0.177 away on a figure 1.0 tall**; step ratio **5.500**. **L1** passes the restated gate (source distance **0.87 edges**, 0.004% beyond 20), mean fallback **734 → 0**, speckle **2.64/1.07/0.23 → 2.43/0.91/0.16**, 10.0% of turnaround figure pixels changed and concentrated on the back half — but its head-zoom pass condition is **not met** (3,372 vs <3,100; dilation 759 vs <400). **L2 re-anchored on the accepted set** moved the ratio 5.500 → **2.600** and blotch **−53.5%**, then **tripped the flattening ANDON at −10.66%** (limit −5%) with the denominator inflating 4q → 5q; GPU not authorised. Correction to the spec: **the gutter is not the mechanism** — only 32.5% of paths cross one, and the minimal `& valid` patch still leaves 53.3% cross-island while stranding 174,898 texels |
| [E08](E08-cover-the-figure-with-reference.md) | Can the styled reference cover the figure — and if it does, does the defect the Director rejected go with it? | **GATE 0 REPORTED, awaiting a ruling** → [Gate 0](E08-gate0.md). **Half 1 passes**: 8 cameras reach **74.10%** of valid texels (halt was 60%), but A2's 80% is unreachable — 12 cameras + 2 elevated at the loosest threshold still gives 79.06%. The two SIDES add more surface than the four diagonals (267,176 vs 247,979), falsifying A1b. **Half 2's construction is impossible**: hold-one-out needs ≥2 cameras per texel and the two twins overlap in **exactly 0** — `facing_front = −Ny` and `facing_back = +Ny` cannot both clear 0.45. Viable from N=4, strong at N=8 (79.9% of reachable). Substituted **reference-agreement ΔE in CIE Lab**, which validates: null at **ΔE 0.72** where the asset carries the reference, **23.18** brush, **18.70** dilation, separating every region the Director named from the controls by **18–65×** — the blade's non-reference surface reads neutral steel (123,122,124) → flesh (147,97,63), median ΔE **32.71**. Severity tracks reference coverage: blade 62% non-reference → ΔE 23.17; tunic 1.2% → ΔE 0.49. ⚠ The acceptance stage discards **46.2%** of what the cameras physically reach, so 8 views likely buy ~40% reference coverage, not 74%  · **[Arm A](E08-armA.md) run**: the reorder is a **no-op** (comparative ownership is byte-identical to the absolute gate at three floors — the shipped loop already falls back to a worse-facing view), and the facing floor is not the lever either (0.45 → 0.05 buys +1.31 points). The cost is the other two tests: **EDGE +211,087**, **MASK +257,511** texels if removed. **The saved `*_mask.png` is missing 24% of the mesh silhouette** — 146,356 px true vs 111,602 used, IoU 0.76, loss *interior* (a stripe down the whole blade), from `figure_mask` keying a grey-on-grey clay render; registration ruled out at shift (0,0). And `project_twins`' "twin is fatter than the mesh (15.8% vs 9.9%)" compared the twin against **that same broken mask** — against the true silhouette it is **twin 17.43% vs mesh 19.01%, IoU 0.911**, so the mesh is fatter and the premise making the EDGE test safe is void  · **[Arm A2](E08-armA2.md) built**: `project_twins` now answers *is there surface here* from **geometry** (raycast silhouette) instead of a threshold on the clay render; `--mask-keyed` reproduces every prior arm byte-for-byte (sha `b12917a2c7c14c4b`). **Reference coverage 681,212 → 938,718 texels, 28.4% → 39.1% of valid, 53.8% → 74.2% of reachable**, with `lost 0` — strictly additive, no diffusion, no GPU. Failure mode checked: recovered texels sit at median ΔE 38.31 from the twin background, 0.18% within ΔE 10, *cleaner* than the already-trusted set (0.32%). The blade is still hole — now held back by the EDGE test, whose justification Arm A voided. **Coverage is not quality**: a stage-1 ΔE grade is vacuous by construction, so whether the rejected defect goes with it is unanswered and needs the loop  · **[Arm A3](E08-armA3.md) HALTED at its own gate.** The erosion is rebuilt on the invariant *never remove more than a bounded fraction of a structure's own width* — `e = min(abs, ⅓ × local half-width)` from `dist_in`'s maximal inscribed disc — and **the invariant holds exactly** (max e/R = 0.3333 against a 0.3333 bound, 0 violations). The gate validates against the shipped erosion, which removes **100% / 100% / 77.6%** of the 1-2 / 2-4 / **4-8px** (the blade) strata against 4.4% of 32px+ — monotone annihilation of thin structure. Then it **fired on A3** at 43.8% of the back 8-16px stratum vs a 40% limit. Not retuned: the invariant is not violated, the threshold was mis-derived from a bar idealisation whose error runs −12.7 to +10.4 points because stratum area-loss is a *shape* statistic. Fifth mis-specified pass condition, executor's this time. A first per-connected-component gate was also rejected on measurement — the whole front figure is **one component of 121,709 px** (the blade touches the hand), so a blade losing ¾ of its area read as 12.3%. No A3 atlas written |
| E09 | Chart fragmentation — the binding constraint on texel density. Culling removed 47% of faces but only 34% of charts. Remeshing is the untested candidate. | **deprioritised by E07's ruling** — density and softness are a different axis from wrong material in the right shape. Was E08; renumbered 2026-08-05 |
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
