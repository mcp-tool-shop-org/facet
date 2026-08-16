# Comfy consult #12 — brief: 2D multi-projector existence proof

**From:** the facet advisor seat, 2026-08-16 · **Relay:** the Director carries this
brief to the Comfy Agent and returns its answer · **No generation this round unless
you name a licence-clean local node we do not already have.**

*Everything below the line is the paste block.*

---

## What we need from you

A **local, commercially clean** way to composite our eight painted twins into one
output still **in image space**, using Blender AOVs we will give you (depth, camera
normals, silhouette). No new 3D ingest. No served mesh path. No new generative
model unless you can name its licence and it is unconditionally commercial.

This is an existence proof, not a product. If the 2D composite looks like the twin
and holds together across two adjacent cameras, our 3D atlas/projection path is
the degrader. If it still looks like shit, the twins do not project, and we should
stop blaming the mesh.

## Hard constraints

- **Local first. Commercial licence is a hard gate.** Apache-2.0 / MIT / BSD /
  OpenRAIL++ are fine. Already excluded in this repo, do not propose: nvdiffrast,
  FLUX.1 [dev] / Kontext [dev], Hunyuan3D-Paint, MVPaint, TEXGen, UltraSharp,
  SUPIR, StableSR, any Tencent/Tripo served UV or mesh node, any cloud 3D ingest.
- **pymeshlab is GPL.** Do not tell us to `import pymeshlab` inside a package we
  ship. A standalone MeshLab CLI is a different question; say so if you mean that.
- **Do not generate new twins.** The eight we have are the plates. They are
  smooth, coherent, correctly-modelled. The rendered 3D asset at the same zoom is
  not.
- **Do not design a UV unwrapper or a remesher.** That is our side.
- **Cross-view consistency is required.** Eight independently-beautiful
  mutually-inconsistent stills fail. If your composite is view-dependent, say
  where consistency is lost and what AOV would fix it.

## What we will hand you (we can bake these tonight)

Per camera, same 752×1024 as the twins, same camera matrices:

- the twin (sRGB PNG, the good plate)
- Blender depth AOV (non-normalised camera Z, EXR — not a 0–1 pretty depth)
- Blender camera-space or world-space normals (EXR)
- a binary silhouette / holdout of the figure

Eight cameras: yaw 0/45/90/…/315; yaw 0 and 180 at +55° elevation; the rest at 0.

We can also give you a **facing map** if you would rather we compute
`dot(N, view)` in Blender than in Comfy. Say which.

## What we already killed (do not reopen)

Island-rim bleed (magenta rims, 16.3% of atlas, **116 screen pixels**). Blend
variants (the rejected sheet only rewrote a few hundred flagged pixels; they were
identical by construction). Camera coverage. Source resolution. Premult alpha.
Minification as the differentiator. A "border" weight we computed against
**material ΔE** — that was the wrong Callieri quantity.

**Still open, and this brief is about it:** Callieri's actual border is
distance to **image borders and depth-map discontinuities (silhouette borders)**,
Sobel on the **non-normalised** depth. We have never built that mask.

## Q1 — Can Comfy do this with zero generative weights?

Name the local nodes, in order, for:

1. Sobel (or equivalent) on a non-normalised depth EXR → silhouette-border
   distance / weight. Callieri zeroes the depth discontinuities and the image
   border, then the weight is image-space distance from those zeros.
2. A facing weight from the normal AOV (we used `facing^6` in 3D; we will try
   `^2` and `^4` as well if you can expose the exponent).
3. A reject: if a 2×2 neighbourhood in the twin sits across a depth jump, do
   not bilinear-sample it (or drive its weight to 0).
4. For one output camera: take **that camera's twin as primary**. Where it
   fails (backface, occlusion, border, mixed-depth), fill from the other seven
   twins using the product of facing × border × visibility.
5. Write one 752×1024 still, no atlas, no mesh.

If a node is missing locally, name a **licence-clean** replacement or say
"Blender compositor should do this instead" — we have Blender 5.2 and will
take that answer.

## Q2 — Where does cross-view consistency get enforced in this graph?

If the answer is "it doesn't — each still trusts its own plate," say that
plainly. Then tell us the cheapest extra AOV or extra pass that would make the
same surface point pick the same source view in two adjacent stills (a
view-independent label), still in Comfy or Blender, still local, still clean.

## Q3 — Licence check on anything you name

For every model, custom node pack, or extension: licence string, commercial
yes/no, and whether it is already on this rig's Comfy or would need an install.
If you are not sure, say you are not sure. Do not "probably MIT" a node.

## What a useful answer looks like

A node list we can build, a statement of what the composite cannot prove, and
any licence landmine. Critique the setup if the AOVs as specified cannot carry
Callieri's border. We would rather you refuse a bad graph than invent one.
