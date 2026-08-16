# Grok consult #3 — the big delegation

**2026-08-16, facet advisor seat. CONSULT ONLY — no build.** Prior rounds:
`docs/grok-consult-1-brief.md`, `docs/grok-consult-2-brief.md`.

*Everything below the line is the paste block.*

---

# You went 4 for 4. Here is everything that happened after, and a bigger question.

## Your calibration claim, verified at the code that actually ran on this rig

Not the GitHub copy — the installed package, because that is what produced our asset.

`o_voxel/postprocess.py`, `to_glb`:
- `mesh.simplify(...)` at lines 136/149/185, **before** `mesh.uv_unwrap(...)` at line 201 ✓
- `decimation_target: int = 1000000`, documented as a vertex target ✓
- passes `mesh_cluster_threshold_cone_half_angle_rad=np.radians(90.0)`,
  **`mesh_cluster_refine_iterations=0`**, **`mesh_cluster_global_iterations=1`** ✓

And `cumesh/cumesh.py:436-457` confirms your structural point and sharpens it: `compute_charts`
does the cone clustering, then **each cluster is added to xatlas as a separate mesh** —
`xatlas.add_mesh(chart_vertices_i, chart_faces_i)` in a loop — so xatlas runs *inside* each cluster
and can only subdivide it further, never merge across. CuMesh's own signature defaults are
`refine_iterations=100, global_iterations=3`; TRELLIS overrides them to 0 and 1.

**You were right that "xatlas on our mesh class" was the wrong sentence.** That sentence was in our
plan, in our tool's docstring, and in two consult briefs. Everything we built on the xatlas author's
testimony about his segmentation was aimed at a stage we do not run.

## What we measured after that, in order

**1. Your central critique, tested with a picture.** We painted every UV-island rim texel magenta —
**391,188 texels, 16.3% of the painted atlas** — rebuilt the GLB, and rendered it flat-lit beside
the unmodified one.

**116 screen pixels changed.** Out of a figure occupying 151,705 px. A positive control (entire
atlas painted magenta) returned 151,705, so the texture path works and the near-zero is real.

Island rims are **16.3% of the atlas and 0.076% of what the camera sees**. Our headline diagnosis —
17.8% of painted area within one texel of an edge — is essentially invisible. You predicted this:
*"that is confetti under a filter, not the twin but chunky everywhere."* The boundary mechanism is
dead as an explanation of the appearance.

**2. The refinement dial you and I both expected to matter — falsified.** With a control arm.

**3. The real finding, and it is upstream of everything.** Chart clustering returned 2.0
faces/chart under *every* setting, which is what an adjacency-growing algorithm returns when there
is no adjacency. So we measured the geometry directly:

| | shipped mesh | welded @ 1e-6 | closed manifold |
|---|---|---|---|
| vertices | 400,130 | **141,561** | ~143,585 |
| face-adjacency pairs | 177,093 | **427,382** | 430,755 |
| **adjacency completeness** | **41.1%** | **99.2%** | 100% |
| connected components | 146,212 | **271** | 1 |
| single-triangle components | **139,198** | 116 | 0 |
| V − E + F | −60,781 | — | 2 |

**48.4% of the mesh's faces are isolated triangles.** The weld is **lossless** — zero degenerate
faces dropped — and stable across 1e-6 to 1e-4, degrading only at 1e-3. The triangles were
coincident all along and simply never shared vertices.

Cone clustering on the welded mesh: **2,654 charts against 146,462. 55×.**

**4. Where we failed.** We predicted the disconnected mesh would have faceted normals (no averaging
across neighbours) and that this drove `facing^6` ownership flipping triangle-to-triangle. We
clay-rendered welded vs shipped to show it. **The welded render came back MORE faceted**, and the
cause is our own export path destroying normals, not welding. Both meshes carry ~4° normal
deviation in memory. **The prediction failed and the test was confounded. We are reporting it that
way rather than spinning the picture.**

**5. One more thing we found about our own evidence.** The four-candidate sheet the Director
rejected — the one whose verdict was "they all look equally like shit, the rest are the same image"
— was built by taking **one render** and replacing only the flagged pixels per candidate: 813, 537,
615 and 298 pixels respectively, in crops of tens of thousands. They were identical by construction.
His read was literally true and sharper than the sheet's own design allowed for. That sheet was
never evidence about the blend.

## The state of the kill list

Dead or unproven, all measured: blend-composite variants · border-distance weighting (on the wrong
quantity — your correction stands and it is reopened) · camera geometry (blade already 96.35%
reachable against a 99.75% ceiling) · source resolution · premultiplied alpha (0.00e+00 against a
fixture proven able to detect it) · minification aliasing (defect texels are *less* minified) ·
island-rim boundary contamination (116 px) · the defect classifier itself (ten of twelve largest
flagged regions sit on gold that is correctly gold, while the obvious green-on-leather-grip defect
is not flagged at all).

**A week, and every named mechanism is dead. We have one large real defect — the mesh is soup —
with no established link to the appearance.**

---

# THE DELEGATION

Four questions. Take as much room as you need on Q2 and Q3; those are the ones we cannot do from
inside.

## Q1 — Why is the mesh soup?

48.4% isolated triangles, geometrically coincident, welding losslessly. Something in the chain
produced a correct surface that was never welded. Candidates we can distinguish if you tell us the
signature to look for:

- TRELLIS.2's **O-Voxel extraction** emitting per-voxel or per-cell triangles that were never
  stitched;
- its **`mesh.simplify(decimation_target)`** tearing them;
- **our own decimation** (a separate later step, ~300k target, carries UVs through);
- the **glTF export** splitting at UV seams (we think this is only the 400,130 → 335,921 part);
- something in the **`cumesh` round-trip** (`read()`/`init()`).

**What is the cheapest measurement that names the stage?** We can dump vertex/face counts and
adjacency completeness at any point in the chain and re-run the whole thing locally. If you think
the answer is obvious from the numbers above, say which and why.

## Q2 — Design the route, not a fix

Stop assuming our pipeline. Given all of the following, **what should the pipeline be, end to
end?** Name the stages, say what each one owns, and say what you would delete.

- **Deliverable: eight rendered stills** out of Blender. We never ship the mesh. Offline-only
  formats and Blender-only methods are fully acceptable.
- The **twins are good** — smooth, coherent, correctly-modelled paint. The rendered asset at the
  same zoom is not. Good input, degraded output.
- The **mesh is soup that welds losslessly** to a 271-component, 99.2%-adjacent surface.
- The **silhouette is Director-accepted** and we would rather not regenerate geometry.
- No served/cloud path can ingest our mesh at any face count — verified.
- Commercial licence is a hard gate.
- We have locally: Blender 5.2, xatlas, CuMesh, pymeshlab, trimesh, PyTorch/CUDA, an RTX 5090.
- Cross-view consistency is a real requirement — eight independently-beautiful mutually-inconsistent
  stills fail. This is why we build an atlas at all, and it is the thing your camera-projection
  suggestion has to answer.

You sketched a route in consult #1 — camera-project the facing twin as primary plate, fill failures
with a Callieri silhouette weight, optionally one Waechter-style seam level, keep an atlas only if
needed. **Spec it properly.** Where does cross-view consistency get enforced? What is the atlas for,
if anything? What owns identity?

## Q3 — Design the falsification sequence

This is the one we most need and are worst at.

We keep running measurements that cannot discriminate. Give us an **ordered sequence, cheapest
first**, where each step **rules something out** — and say explicitly what each result would mean.
Include the ones that would kill your own Q2 route.

We are good at executing a specified measurement and bad at choosing which one. Assume we will run
exactly what you write, in order, and report the numbers back.

## Q4 — What have we not named?

Every mechanism on the kill list is dead. The mesh is soup but that link is unproven. **What is
still on the table that we have not enumerated at all?**

If your answer is "the appearance is a rendering/colour-management artifact and the asset is closer
to fine than they think," say that — we have not ruled it out, our renderer's own docs warn that a
default render tone-maps through AgX and is not a texture readout, and we do not know whether the
rejected sheets were flat-lit.

## Calibration

Nominate one checkable claim as before. Yours have held four times and each one changed what we
did; the last one rewrote our understanding of our own pipeline. We will verify at primary source
and report the result either way.
