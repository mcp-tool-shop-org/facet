# What the route learned

*The durable findings, in full. Each one cost an experiment and each one generalises
beyond the subject that produced it. The [README](../README.md) carries the short
form; this page is the long form with the measurements.*

---

<!-- Moved out of README.md by the E19 treatment, 2026-08-08, at the Director's
     word ("the readme reads more like a changelog"). NOT rewritten: every line
     below is byte-identical to the README it left, corrections and ⚠ annotations
     intact. The README now links here. -->

**Form first, style second.** Image-to-3D reconstructors key off shading, silhouette
clarity and unambiguous depth. A heavily stylized sprite — weathered planks, painted
grime, fine rigging — fights the reconstructor, which reads surface noise as geometry
and muddies the form. Feed it a clean, sculpt-like image with the major planes
deliberately exaggerated, and the topology comes back better. The styled twin,
generated alongside the clay from the same control, stays as the colour and identity
reference for the texture stage.

**Frame the face, get a face.** Reconstruct a second time from a head-and-shoulders crop
of the same clay. Measured in [E01](docs/experiments/E01-facial-structure-ceiling.md)
across two characters: the crop puts **3.1–4.5× more polygons** on the head, and the
difference is structural rather than cosmetic. Full-figure input gives a continuous brow
bar over a shallow recess and flat punctured nostrils; the same character from a bust
crop gains separated upper and lower eyelids, a brow furrow, and modelled nostril
cavities. A face is a small fraction of a full-figure frame, and reconstructors spend
their resolution where the pixels are.

**Density where the form is.** Small polygons on the face, larger ones on flat
expanses. Facial structure that survives reconstruction survives every downstream
step, and styling applied to real structure reads naturally instead of sitting on
top of a blob.

**Style on the asset.** The texture atlas is the single accumulating state. The styled
twins are projected onto whatever surface they can see; everything they cannot see is
recorded as an explicit hole map and filled by a masked inpainting brush, one camera
at a time, with already-styled texels never overwritten.

**Twins belong to a mesh, not to a character.** A styled twin is a canny-locked restylize
of a *render of one specific mesh*, so it carries that mesh's silhouette. Measured: A0's
bounding box gives x/z 0.722 against the twin frame's 0.734 and registers to 1.6%; W3
reconstructs the same clay at x/z 0.458 — 38% narrower — and the same twins project the
arms and sword into empty space beside the mesh, collapsing styled coverage from 62% to
22.7%. **Generate twins from the mesh you are about to texture**, every time. It is one
job per view.

**Identity belongs to the prompt, not to the twin.** The corollary cost a whole experiment. A
twin generated against a control missing a quarter of the silhouette painted a taller, narrower
man than the mesh *and* dropped the character's gold knee plates — and cleaning the control
corrected the proportions while the plates stayed gone. Naming them brought them back: one
phrase, with the control byte-matched at 20,973 px so the term was the only difference. The
armour had only ever reached the image through **noise in a broken ControlNet**. So a twin has
exactly one job — register to the mesh — and everything that makes the man *this man* is a named
element in a versioned prompt. **A canon element not named in the prompt is arriving by accident
and will leave the same way.**

**Build the control image; don't hope Canny finds the silhouette.** A clay render is flat
grey on flat grey, so Canny returns 0.84% edge pixels and almost no outer contour — the
ControlNet constrains nothing and the model regenerates the character. Composite the
figure onto a contrasting background *and* union the figure mask's morphological gradient
into the edge map. Measured: control 6,482 → 33,864 px, silhouette IoU **0.290 → 0.777**,
bbox x/y 0.797 → 0.457 against the source's 0.458. `restylize_views.py` does this.

**Prompt per view, or the text overrides the control.** With a correct contour the back
view still came back front-facing at both 0.92 and 0.75 denoise — the control carries
facing (mirrored-front vs back edge-map IoU 0.165), but a prompt asking for "a long red
beard, gold necklace" on every view is an instruction to draw a face, and the text wins.

**Polygons and texels are separate budgets.** `smart_decimate` allocates polygons;
`bake_hero_prep`'s island scaling allocates texels. These do *not* double-subscribe — a
head can hold 84.4% of the faces and only 44.8% of the UV area simultaneously. Any gate
comparing UV area to **face count** is meaningless on a deliberately non-uniform mesh;
compare UV area to **3D surface area**, which is texels per unit of surface.

**Keep the generator's atlas; watch the gutter.** TRELLIS ships xatlas UVs, and
`bake_hero_prep` used to delete them and re-run `smart_project` — which on the same 287k-face
mesh produced **35,070** islands (8 faces each) where the native atlas has **14,010** (20.5
faces each). Native UVs are now the default. Then the gutter: at `island_margin` 0.004 on a
4096 atlas that is 16 px around **every** island, which took packed coverage to 4.01%;
dropping it to 0.001 restored **18.76%**. Raising `angle_limit` to merge islands was tried
and moved the count **0.8%** — `smart_project` splits on UV distortion as well as angle, so
decimation's long thin triangles split whatever the threshold.

**Cull what no camera can see — from the atlas, not from the mesh.** Measured across 46
exterior cameras: **49% of valid atlas texels are never visible from outside** — interior
shells, deep folds, behind a beard, between fingers. The atlas was paying texels for surface
the brush could never reach, then dilating them, then bleeding that into the surface you can
see. Excluding those faces from the UV layout took interpolation down **68%** (2,551,893 →
813,773 dilated texels) and brush coverage from 27% of holes to **52.7%**.

Do this by **excluding faces from the atlas, never by deleting them**. Deletion needs a
perfect gate forever — and the obvious gate does not work: silhouette IoU is structurally
blind to holes punched through visible surface, because the ray behind a removed face still
hits geometry. It returned **1.00000 at all eight cameras** on a mesh with a hole clean
through the torso. Under atlas-exclusion the geometry is never modified, so the failure is
impossible rather than detectable, and a camera you add later sees a flat patch instead of a
hole. The visibility set must also be a **superset of every production camera** — a generic
sphere is not, however dense.

## Hard-won rules

**Judge textures under FLAT light.** A Blender Workbench STUDIO render is not a texture
readout. Grey chalky facet mosaics are specular highlights on flat-shaded normals and
vanish entirely under `--flat`. Two debugging rounds were spent chasing a render
artifact that was never in the texture. Use `--clay` to judge geometry with no texture
in the way.

**Check the alpha channel before trusting an "is it black?" test.** A fully black RGBA
image with alpha=1 averages exactly 0.25 and sails past a `< 0.005` threshold. That
check shipped a black mesh.

**Blender's RNA references go stale after any `mode_set` round trip.** Reading through
one silently returns zeros — no exception. Re-fetch from `obj.data` after every
edit-mode exit.

**Blender caps meshes at 8 UV layers, and `uv_layers.new()` returns `None` silently at
the cap.** A design needing 9 produces a white export and a long bisect.

**A raised weapon rises above the crown.** Any instrument that finds the head by height
will grab the blade instead. Find the head by projecting a face rect from the front
view.

**Detail overlays mask; it never restores.** No texture pass can add facial structure a
mesh does not have. If the face is crude in clay, it will be crude when painted.

**A gate must test the operation's failure mode, not its success mode.** See the cull
above: silhouette IoU checked "is the silhouette still there" when the risk was "did
anything behind it disappear," and returned a perfect score on a broken mesh.

**A guard that fires on a correct input is worse than no guard.** A centroid checksum
compared Blender's float32 `polygon.center` against trimesh's float64. They agree to
5.6e-8 — which straddles a 5-decimal rounding boundary on thousands of values, so an exact
hash mismatched on a perfectly aligned mask. Compare positions within a tolerance, and size
the tolerance against the thing you are detecting (a one-face shuffle moves a centroid
~0.0029; the noise floor is 5.96e-08).
