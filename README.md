# facet

Turning a styled 2D concept into a textured 3D character — with the style applied
**on the asset** in texture space, not painted per view. Runs entirely on local
hardware, with no non-commercial dependency anywhere in the chain.

Named for both halves of the problem: the polygons, and the face they have to hold.

## The route

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

**Where it stands.** Geometry is solved: reconstruction produces real facial structure
given the right framing, and polygon budget allocation works.

**Texture is not.** Four experiments improved measurable properties of the texture stage —
the unwrap, the culled surface, the dilation source, the seam levelling — and at
[E07's Gate 1](docs/experiments/E07-ruling-gate1.md) the Director ruled the asset **not
close**. The cause is recorded there and it is a measurement failure, not a tuning one: every
unit those experiments graded on is a **5×5 high-pass statistic**, and the defect that decides
acceptance is a **large region of the wrong material** — a steel blade wearing skin tones, a
boot carrying scattered gold and green. A region like that is smooth inside itself and
registers only its rim. An arm cut dilation source distance **70×** and took speckle below the
reference asset while changing nothing to the eye.

The structural fact underneath it: on the finished asset, **28.4% of texels come from the
styled reference, 37.7% from diffusion invention and 33.9% from interpolation**. Every
experiment up to that point improved *how the other 71.6% is filled*; none reduced it.

**What [E08](docs/experiments/E08-ruling-gate0.md) then established — and this is the part
that generalises.** The reference stage was carrying a defect nobody had measured: the mask
telling the projector *where the surface is* was a keyed clay render missing **a quarter of
the figure**, interior rather than at the rim. Replacing it with the exact raycast silhouette
took reference coverage **28.4% → 39.1%** of valid texels, and **53.8% → 74.2%** of what two
cameras can physically reach, strictly additive, with no diffusion and no GPU.

**Restated after the intersection ([E08 Amendment 27](docs/experiments/E08-ruling-gate0.md)).**
Those A2 figures were measured with the *trust* mask unbounded by the silhouette: paint on no
surface — every twin carries 550–8,991 px of it, and it is connected to the figure — was
setting the edge-distance field and holding erosion off the texels near it. On the current
twins that contaminated 25.3% / 19.6% of the figure's edge distances. Intersecting the trust
mask with the silhouette is now the route default, and its regression was strictly
conservative: **gains exactly zero, zero losses in the two thinnest half-width strata, every
lost texel within 5 px of paint that sat on no surface** (−7,574, measured in
[E08-intersection-regression.md](docs/experiments/E08-intersection-regression.md)). The
standing two-camera baseline is **1,042,794 styled — 43.4% of valid, 82.4% of reachable**.

**Eight cameras are banked** ([E08-eightcam.md](docs/experiments/E08-eightcam.md)):
**1,653,659 styled — 68.8% of valid, 92.9% of reachable** — against a reach of 1,780,546
(74.1% of valid) that matched the ceiling instrument's independently written computation to
the texel. A quarter of the gain came from union acceptance rising with camera count alone
(2.15× redundancy, no test changed) — so **an acceptance rate quoted without its camera count
is not a number** in this repo. A per-view registration halt is armed at IoU < 0.80 against
the exact silhouette, derived from both sides of the measured line (adjudicated twins
0.8329–0.9533; measured failures ≤ 0.578).

**And the architecture is now measured rather than assumed. Twins register; the prompt
carries identity.** Contradict the specification on eight elements — *silver* where gold
arrives unbidden, *black* where wine-red arrives — and the prompt wins **8 of 8**: median ΔE
**46.3** against **6.2** on five held controls, a **7.4×** separation. The LoRA, mesh and
control did not hold the character's attributes against a conflicting spec. **And it is still
the same figure** — face, build, pose, boots. Structure is held by the mesh and control;
named attributes are carried by the prompt. **This is a pipeline, not a one-character
generator.**

**The Director accepted the asset at Gate 1** (2026-08-04, ruled on the GLB at his own zoom
— [E08 Amendment 35](docs/experiments/E08-ruling-gate0.md)). Measured provenance **68.8%
reference / 4.2% brush / 27.0% dilation** against the rejected asset's 28.4 / 37.7 / 33.9 —
reference ×2.42, diffusion invention ×0.11. *⚠ On-surface restatement, 2026-08-06
([E10-offsurface-ruling.md](docs/experiments/E10-offsurface-ruling.md) Ruling 7): W3's bake
carries 2.5840% off-surface texels; excluding them, reach reads 74.30, styled/valid 69.28,
dilation 26.43 — the full table is in
[the report](docs/experiments/E10-offsurface-r4ab-report.md). The on-surface family is the
standing cross-asset family; as-recorded stays beside it.* One region named at his zoom: a hard-edged
blotch on the crown, prior mechanism the documented unlevelled stroke seam (confirmation
dispatched). The post-Gate-1 quality queue demotes to optional polish.

**And the route generalises — E04's galleon is the second accepted asset** (2026-08-05,
"it looks good to me," ruled on the five-column sheets —
[E04-ruling.md](docs/experiments/E04-ruling.md), 28 rulings). The ship ran the character's
route end to end with every subject value drawn from `profiles/ship.json` and
`canon/GALLEON-IDENTITY.md`: eight twins, six strokes, **zero credits across every
generation in the arc**. Measured mix **36.89% reference / 6.87% brush / 56.24% dilation**
— read against the subject's own pre-registered **42.72% stage-1 reach ceiling** (86.4% of
reach, beside the character's 92.8% of 74.1%): a ship hides most of itself from eye level,
and the difference is geometry, not regression. *⚠ Restated 2026-08-05, standing family FLIPPED 2026-08-06
([E10-offsurface-ruling.md](docs/experiments/E10-offsurface-ruling.md) Rulings 1 and 7):
2.4967% of the bake's uv-valid texels carry positions not on the mesh (>1 px). On the
on-surface population the same quantities read **42.25 / 36.68 / 86.8 / 56.44 / 6.89** —
and with W3 now measured too (2.5840%, composition INVERTED: its off-surface population is
paint-depleted where the galleon's is paint-enriched, so three of five W3 headlines move
the opposite way), **the on-surface family is the standing cross-asset family**. The
as-recorded numbers stay beside it everywhere, denominators named. The population itself is
localized: 90.85% on the single outermost ring of the mask, largest blob 33 texels —
measured and bounded, no route change warranted.* The spec's central hypothesis — *no
shared-code edit needed* — was **falsified five times, and that was the payoff**: each
falsification hardened the profile system (the coverage gate and its subject-flag registry
law, the generator-legal frame constraint, two operand corrections found at fixes' second
consumers).

**E10 then closed the same day** ([E10-ruling.md](docs/experiments/E10-ruling.md), 12
rulings, four generations, zero credits): **environment-contact layers** — the Director's
waterline, shipped as **data, not geometry**: the GLB stays whole, `waterline_z` rides in
the profile and manifest (four independent confirmations of the placed line), and the
scene's water hides the underwater body per frame. The arc's law, measured across eight
arms: **inpainting continues an asset; full-frame generation introduces new material;
layers fill by masked projection** — three inpaint attempts at ΔL\* −1.6 to −4.1 against
one full-frame at **+33.4**, one field changed. The layer machinery (second accumulating
state, two-lane profile vocabulary, base-invariance structural and proven under live
fire, straight-alpha RGBA export contract) generalises by construction: snow on boots,
mud on wheels, moss on ruins are the same contact query + layer + law. Both queued
items then ran the same evening — the `pos.npy` off-surface measurement (ruled; the
restatement above, [E10-offsurface-ruling.md](docs/experiments/E10-offsurface-ruling.md))
and the exporter, next.

**E11 ran and was ruled the same day** ([E11-report.md](docs/experiments/E11-report.md),
[E11-ruling.md](docs/experiments/E11-ruling.md)): **accepted assets become training
data.** The dense-turnaround exporter is proven a pure function (two fresh emits
byte-identical on every channel; the beam anchors byte-identical to the recorded
sheets), and both subjects' dense trees — the galleon at 28 cameras with the **native
per-texel owner channel** (the first asset that has one), W3 at 26 with owner honestly
absent — validate through the sdlab lane's own codebase with **zero schema edits**. The
lane's palette gate reproduced the staged manifest's blob digits (1738 / 1495 / 263 px)
from freshly emitted renders through a different implementation. Ruled: the **emit
render generation is the standing export and training input** (the recorded
`renders_flat` are another generator's output no current invocation reproduces — frozen
in the record, superseded for training); a Gate-1 verdict covers the **asset**, renders
are post-verdict derivations by the anchored readout; **flat-only is what facet honestly
exports** — every render ships with its exact silhouette so backgrounds are
augmentation-side, and lighting would be a new renderer with its own anchors.

**E12 — the beast arc — is IN FLIGHT** ([E12-ruling.md](docs/experiments/E12-ruling.md),
Rulings 1–13 so far): the route's third subject class, a **winged dragon**, designated
from three reconstructed candidates on full-size sheets ("3 is the winner"). What Gate 0
measured ([E12-gate0-report.md](docs/experiments/E12-gate0-report.md)) rewrites the
priors: **9–12 welded shells against a character's 40–191 and the ship's 237–512** —
an order of magnitude more connected than anything this repo has reconstructed, every
satellite located (fangs, plus four tail spines on one candidate) — and the **wing
membranes come back as closed slabs that pinch, not sheets that hole** (0–1 boundary
edges of zero length; what breaks watertightness is edges with >2 faces, confined to
trailing rims on two candidates and running through the folded wing's field on the
designated mesh). Reconstruction **does not preserve the concepts' poses**: three
different stances all return as one symmetric wings-spread quadruped. The measurement
pass banked the subject's ceiling (**50.46% of 3,240,510 valid texels at eight
eye-level cameras**), ruled **elevated cameras NONE** (+1.77 points against a
~50-point self-occluded deficit, with the candidate ordering flipping inside
ray-sampling noise), and measured the thin-structure constraint the spec must design
against: **the character's `thin_extent` would withhold a third of the visible animal
and 60% of the wings, and no single global value separates membranes on a subject
where most detail is thin** (mask peaks at 1.78× membrane concentration). The
backdrop was derived, not inherited — and the derivation's payoff is that **W3's
"plain grey background" scores under the key's own 0.06 cut on this subject, bound by
the membranes**: the blade failure's shape pointed at the new surface class. The
first styled pair ran at zero credits — and was **REJECTED at the Director's eye**
([E12 Ruling 10](docs/experiments/E12-ruling.md)): a generic stock dragon wearing the
right silhouette. The rejection bought two rules: **the style register is subject
data** (the saltroad painterly register two subjects earned acceptance under had been
*inherited* by a third it does not fit — the beast now runs ultra-realistic, no LoRA;
the studio plan is [docs/style-registers.md](docs/style-registers.md)), and the
measured cause of the structural loss is the control: the profile's canny pair fires
on 5.2%/2.1% of the figure interior where the same clay carries 15.8%/11.2% at lower
thresholds — the relief never reached the ControlNet, and at denoise 0.92 the interior
was the model's to invent. The re-pair then ran under the ruled register with the canny
pair derived per subject and ruled **0.05/0.10** — the control carries 2.15× the
falsified pair's pixels — still at zero credits, and the Director's verdict is
**register CONFIRMED, pair not yet accepted**
([Ruling 11](docs/experiments/E12-ruling.md)): *"a lot better, but the tongue is
missing and the face could be more defined."* His definition question reopened the
allocation decision by Ruling 2's own re-open clause; the ruled ladder runs
**resolution first** (a head-crop companion generation framed from the measured head
box), **geometry second and only on his sentence** (a bust-crop re-reconstruction
replaces the designated mesh — a Ruling 1 re-open, never a session's arm). Acceptance
now gates on three items in flight as handoff 5: the tongue's geometry answer on the
mesh (Gate 0 saw one on 00001/00002 and not on 00003), view 5's bounded re-roll (the
pale-tan haunch and bone-ivory membranes are spec violations on named elements), and
the companion. Handoff 5 ran all three at 0 credits
([the report](docs/experiments/E12-handoff5-report.md)): **the mesh HAS a tongue** —
main-shell geometry, route-visible; Gate 0's omission-read falsified in one render at
mouth scale — both view-5 misses resolved on the seed alone, and the companion
measured the ladder's resolution rung: muzzle plates, nostrils and tooth rows define
at bust scale while **the eye is geometry-limited** (the clay carries brow plates, no
lens recess; a denser control produced *less* eye than the sparse one — the control
constraining invention rather than enabling it). The Director's eye then caught what
both seeds carry ([Ruling 12](docs/experiments/E12-ruling.md)): the fixture's
pale-bone family — the word "bone" rode the prompt five times — rendering as
**exposed skeleton** on legs, tail underside and wing arms under the realistic
register, a register-family interaction the painterly register never showed at the
galleon's gold density. Canon corrected in place (D2 olive-tan, D6/D7 charcoal;
ivory is now the head's family), and the regeneration is dispatched as a new
decision bundle (handoff 6). The bundle ran at 0 credits and **the bone reads leave
at the worst seed** ([Ruling 13](docs/experiments/E12-ruling.md)): same seed, same
control, prompt only — whole-figure pale-bone mass 28.71% → 7.69%, the rib element
gone, blade rows charcoal, wing arms green. The regeneration also measured the arc's
newest finding: **a colour term appears to reach structures that resemble the one it
names** — `pale ivory fangs` lands on the claws over `charcoal claws` in the same
string, on the view whose stem carries ivory words, while the stem without them
takes charcoal claws at the same seed — so a prompt's colour-family mass bleeds by
structural resemblance, not only by name (labelled hypothesis, two views, one
subject; the drop map's job may be larger than visibility). The pair awaits the
Director's sentence. Every value the subject needs lives in
`profiles/beast.json` and `canon/DRAGON-IDENTITY.md`, and the ones that arrived by
inheritance are being falsified and replaced one measured step at a time — which is
the profile system doing its job.

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

## Status of every tool — measured, not asserted

Nothing here is marked working unless it produced an artifact a human looked at. The
failures are in the repo too, with the reason, because a claim sitting next to
runnable code can be checked in minutes instead of trusted.

Claims that turned out to be wrong are corrected **in place, with the measurement that
overturned them**, rather than quietly deleted — see the `smart_decimate.py` entry below
for a worked example. The evidence trail lives in
[docs/experiments](docs/experiments/): a spec is written before the work, a report after,
and conclusions come last.

### `tools/` — works, load-bearing

| tool | what it does | evidence |
|---|---|---|
| `render_geomaps.py` | position/normal conditioning maps via open3d raycasting | replaces nvdiffrast (non-commercial) at <1/255 MAE on all 6 views |
| `ig2mv_licensefree.py` | six consistent views of one character in one pass | 24 s on an RTX 5090; nvdiffrast's module name is occupied by a tripwire stub that raises if any code path touches it |
| `sr_views.py` | view-space upscale — spandrel (MIT) + RealESRGAN anime6B (BSD-3) | deterministic by construction; ×2 for views, ×4 for face crops |
| `project_twins.py` | projects the styled twins onto the atlas, emits a hole map | N-view since `c469b36`; trust mask ∧ exact silhouette by default (E08 A27) with a registration halt at IoU < 0.80; eight cameras land 68.8% of valid / 92.9% of reachable, anchors pixel-identical back through A2 |
| `texpass_iter.py` | emit/commit write-head for progressive texture fill | selftest: styled texels byte-identical (delta 0.000000), holes strictly shrink |
| `texpass_brush.py` | drives local ComfyUI — Qwen + style LoRA + inpainting ControlNet | ~45 s per stroke |
| `texpass_finalize.py` | dilation fill for residual holes | closed 868k texels with zero mean fallback |
| `texpass_loop.ps1` | the whole loop: reset, eight strokes, finalize, render | ~8 min per character, unattended |
| `bake_hero_{prep,fuse,pack}.py` | multi-view baker — depth-tested visibility, per-texel ownership, seam levelling | kills through-projection: a raised sword no longer bakes onto the chest behind it |
| `resample_atlas.py` | nearest-surface texture transfer between topologies | replaces Blender's ray bake, which returned a black atlas when rays were cast from a seam-split mesh |
| `restylize_views.py` | generates a mesh's own twins — builds the control image, saves the exact figure mask beside each twin | silhouette IoU **0.290 → 0.777**; per-view prompts take face detections on the rear view 1 → 0 |
| `cull_unseen.py` | classifies faces by exterior visibility so the atlas can skip them | 47.6% of faces unseen by 46 cameras; interpolation down **68%**; gated on first-hit **depth**, not silhouette |
| `texpass_provenance.py` | replays the commit chain offline to tell you, per texel, whether colour came from a twin, a specific stroke, or dilation | reproduces live commit counts to the texel; settled the blotch question without a GPU. ⚠ *Corrected 2026-08-05: the replay predates E08 A32 and over-claims +358 commits on the galleon (the missing `fm_e & hit` intersect — [report](docs/experiments/E10-offsurface-consumers-report.md)); the A32-faithful replay is `diagnostics/e10_claim_replay.py`; fix queued for the tool's next use* |
| `e11_export_turnaround.py` | dense-turnaround export — emit-orchestrated flat renders + exact silhouettes + born-indexed class maps + owner slices, per camera, as a sha-linked self-contained tree | export proven a pure function; beam channels byte-anchored to the record; both subjects' trees validate through the sdlab lane 28/28 and 26/26 ([E11-report.md](docs/experiments/E11-report.md)) |
| `e11_manifest.py` | the lane-contract manifest for an export tree | validated by the lane's own codebase on both subjects; the lane's palette gate reproduced the staged manifest's blob digits from fresh renders |

### `tools/` — unblocked, fix measured

**`smart_decimate.py`** allocates polygon budget by face rect and carries UVs through
the cut, so the existing atlas keeps working with no re-UV and no re-bake. Mechanically
sound and verified: 287k → 150k with UV span intact.

Decimating tore holes and left lace instead of redistributing density. **The cause was
mislabelled in this file until it was measured, and the correction matters more than the
tool.** An earlier version blamed reconstruction — "roughly 8,600 disconnected shells" —
a number inherited from a session record and never checked. Measured in
[E01](docs/experiments/E01-facial-structure-ceiling.md):

| mesh | connected components |
|---|---|
| raw reconstruction (`warrior/mesh.glb`) | **1** |
| four fresh reconstructions | **40–191** (92–98% of faces in one shell) |
| `hero_bake/prep_uv.glb`, `texpass/warrior_texpass.glb` | **285,654** |

Reconstruction returns a connected surface. **Our own UV unwrap and glTF export splits a
vertex at every UV seam**, which with per-triangle islands explodes the mesh into one
shell per face — and decimation was handed that. Collapse decimation merges neighbours;
per-triangle shells have none.

**The fix is local and cheap: weld before decimating** — merge-by-distance now runs
before the decimate modifier, because Blender stores UVs per-loop rather than per-vertex.
Measured on `warrior_texpass.glb`, both arms at `--target 150000` with identical
protection settings, the second reproducing the historical shredded output exactly:

| run | verts in | shells in | faces out | shells out | legs |
|---|---|---|---|---|---|
| `--no-weld` (old behaviour) | 858,562 | 285,654 | 150,000 | **149,528** | shredded to lace |
| welded (default) | 858,562 → 137,607 | 285,654 → **1** | 149,996 | **1** | intact |

The atlas survives the weld: every one of the 287,230 surviving faces kept its exact UVs,
and a textured flat render of the welded 150k mesh differs from the 287k source by a mean
of **0.47/255**. Four zero-area triangles (0.0014%) collapse in the merge — a triangle
whose corners were the same point had no area to lose. The run asserts both facts and
halts if either fails, and `--no-weld` reproduces the old behaviour for comparison.

### `tools/superseded/` — kept because the failure is the lesson

| tool | why it's here |
|---|---|
| `bake_multiview_glb.py` | Averages views instead of assigning ownership. Averaging disagreement **is** ghosting — this is the documented cause of smeared faces, not a tuning miss. Superseded by the ownership baker. |
| `retopo_bake.py` | Retopo → re-UV → bake. Failed twice: the selected-to-active ray bake returned black, and re-UVing a decimated mesh produced 119,776 islands whose packing margins collapsed every island to a sliver — 0.4% atlas coverage. |
| `tint_prime.py` | Statistical colour priming, falsified three ways. Height bands have no horizontal awareness, so arm-versus-torso assignment changes per view. Structural, not tunable — do not retry. |
| `project_prime.py`, `prime_bake_glb.py`, `project_multiview.py`, `facing_atlas.py`, `weight_glb.py` | Earlier projection experiments, superseded by `project_twins.py` + the texture-space loop. |

### `tools/verify/` — how anything gets judged

`head_render.py` and `turn_render.py` are the verification cameras;
`head_crop.py` builds comparison sheets at zoom; `gate_mesh.py` is a mesh QA gate
(character-only — its head/shoulder logic is meaningless on other subjects);
`mesh_stats.py` measures any mesh identically — shell count, face-rect polygon
density, and curvature variance inside the face rect — so two meshes made months
apart by different tools are still comparable. `gate0_sheet.py` and `gate1_sheet.py`
build the designation and acceptance sheets (full size, concept beside geometry,
ranking nothing). The E12 arc added per-subject instruments under `tools/diagnostics/`
— frame derivation asking every rendered yaw (`e12_frame.py`), head-region evidence
with the box drawn back onto every view (`e12_head_evidence.py`), non-manifold-edge
location (`e12_nonmanifold.py`), the thin-extent cost curve (`e12_thin_curve.py`),
elevated-camera coverage (`e12_elevated.py`), the subject-flagged off-surface
classifier validated against the ship's ruled number before first use
(`e12_offsurface.py`), and a two-class argparse help linter that gates rather than
informs (`e12_help_format_scan.py` — literal `%` and non-cp1252 glyphs; it found six
sites where a hand-search knew four, one of which could not crash at all).

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

## Known defects, named

**Two thirds of the asset is not the reference.** ⚠ *Corrected in place twice. An earlier
version said the two-view limit was a hardcoded list; fixed —* `project_twins.py` *takes N
views since `c469b36`, anchors pixel-identical. A later version said the acceptance lever was
spent at 82.4%; restated in E08 Amendment 28 — union acceptance is a function of camera
count, and eight cameras reached 92.9% of reachable with no test changed.* The stage-1 state
is now **68.8% of valid referenced at eight cameras** against a 74.1% reach; what fraction of
the *finished* asset the reference covers is Task 3's measurement.

**The blade band takes 0.00% of stage-1 reference — the measured mechanism behind E07's
"the blade carries no reference."** The twin's key excludes the greatsword band in every
measured view: its paint sits *on* the key's threshold (median residual 0.0657 / 0.0645
against the 0.06 cut) because steel on a grey studio backdrop is grey-on-grey — the project's
fifth instance — and the size-5 erosion removes the half that passes. Outside the trust mask
`dist_in` is 0 by definition, so every candidate texel there is rejected: 46,197 / 31,699 on
the current twins, 42,984 / 74,997 in the A2 lineage, **0 accepted in all four rows, in both
arms of the intersection regression** — the intersection neither caused nor repaired it. The
0.06 cut is a global constant governing a local low-contrast feature. At eight cameras the
per-view rate is 0.00% on all eight; the union rescues 55.72% of the band. **On the finished
asset the blade band runs 47–61% dilation against the whole asset's 27%, carrying 30–47%
reference where E07's blade carried none** — the worst-served structure by both measures,
visible as the orange stripe on every provenance panel of the Gate 1 sheet. Measured in
[E08-intersection-regression.md §9a](docs/experiments/E08-intersection-regression.md),
[E08-eightcam.md §5](docs/experiments/E08-eightcam.md) and
[E08-task3-report.md §4](docs/experiments/E08-task3-report.md); the blade arm is specified
after Gate 1 with this as its targeting data.

**⚠ The defect list below was written against high-pass metrics** that
[E07's ruling](docs/experiments/E07-ruling-gate1.md) found blind to the defect that decides
acceptance. Each entry is still measured and still true; none of them is established as the
thing that makes the asset unacceptable.

**Stroke seams are not levelled.** Stage 1 applies a low-frequency Gaussian levelling
across projection boundaries. **The brush loop has none** — so every boundary between two
strokes, and between stage 1 and the first stroke, is an unlevelled tonal step. Provenance
replay found the forehead "blotch" on the current asset is exactly this: twin paint below
meeting the overhead stroke above, two blotch pixels in the whole disc, a step rather than a
defect in either source. The architecture called for Poisson seam levelling; it was
implemented in projection and never carried into the loop. **Located in code:** the levelling
term is `project_twins.py:253-256` and `bake_hero_fuse.py:233-237` (`--seam-sigma 16.0`, its
own docstring calling it *"the multi-band/Poisson role"*); in `texpass_iter.py`, `commit`
writes `a2[hidx] = col` (line 246) and `gaussian_filter` appears only in the selftest's fake
inpaint. **Measured** in [E07 Gate 0](docs/experiments/E07-gate0.md): a provenance boundary
steps **5.5× ordinary texture variation** (median |ΔL| 0.02876 across, 0.00523 within), and
the forehead the Director named is **9.5×**. Dilation boundaries are nearly flat at 1.5–1.75
— dilation blends *from* its neighbour by construction — so the step is a brush-boundary
phenomenon, not an artifact of the denominator.

**Dilation still bleeds between unrelated islands.** Down from 75% of hole texels to 33.9%
of the atlas, but dilation-filled texels remain **4.8× enriched** in visible blotches
against a 5% base. Colour crosses the gutter from whichever island the packer placed next
door, and atlas adjacency is not surface adjacency. **Located in code, and the docstring was
wrong:** `texpass_finalize.py`'s flood predicate is `fill = ~grown & (cnt > 0)` with no
`& valid` — `valid` decides when to stop, never where to write.
[E07 Gate 0](docs/experiments/E07-gate0.md) measured the cost by replaying that flood
carrying a source label: **74.9% of 813,773 dilated texels take their colour from another
island**, from a median **0.177 away on a figure 1.0 tall** — 61 median triangle edges, 18%
of the figure's height.

**The gutter is not the mechanism, and the minimal patch is worse than it looks.** Only
**32.5%** of paths cross an invalid texel; adding the missing `& valid` still leaves 53.3%
cross-island and strands **174,898** texels on the mean fallback, 238× more than now.
`--pack-margin 0.001` does not put a gutter between all charts — 5.73% of 4-adjacent valid
texel pairs are in different islands and touching *directly*, half of them more than 20 edges
apart on the surface. The fix is a surface neighbourhood, not a predicate: nearest painted
texel in 3D sources from a median **0.00253 — below one triangle edge**, a 70× shrink, closer
for 92.4% of the same texels.

**⚠ `bake_hero_fuse.py:257` carries the identical unconstrained flood.** Not on the current
route — the E06 recipe invokes `bake_hero_prep`, `project_twins`, the loop, `finalize` and
`bake_hero_pack`, not `fuse` — and unmeasured. Recorded here so it cannot quietly become
doctrine; it gets the same surface-aware primitive whenever `fuse` returns to the route.

**Chart fragmentation is the binding constraint on texel density.** Culling invisible
surface removed 47% of faces but only 34% of charts — because invisible surface is
interleaved *within* charts, so excluding it perforates them rather than freeing them.
Faces-per-chart fell 20.5 → 16.4, bbox fill 42.1% → 36.6%, packed coverage 24.81% → 14.32%.
Net texels landing on visible surface rose ~17% where a naive reading predicts double.

**Paint lives in big charts; holes live in small ones.** Measured in
[E07 Gate 0](docs/experiments/E07-gate0.md): the island holding a randomly chosen *styled*
texel has a median 1,231 texels (~35×35), the island holding a *dilated* one has 296. So
atlas-space operations are safe exactly where there is already paint and unsafe exactly where
there is not — which is why stage 1's σ=16 levelling draws only 6.8% of its weight
off-island (median) and does no measured harm, while the dilation flood at the same scale
does. Beware the inspection paradox in either direction: the median island holds 88 texels,
but the median *texel* does not live in a median island.

## Licence position

Every stage runs local and commercially clean: SDXL (OpenRAIL++), MV-Adapter (open),
open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy,
trimesh.

Deliberately excluded, with the reason: **nvdiffrast** (non-commercial — enforced here
by a structural tripwire, not by attestation), **Hunyuan3D-Paint** (licence void in the
EU, UK and South Korea), **MVPaint** and **TEXGen** (no licence at all), and
**UltraSharp / SUPIR / StableSR** (non-commercial upscalers).

## Requirements

Blender 5.x, Python 3.11+ with `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`,
`spandrel`, `torch`. A local ComfyUI install is needed only for the inpainting brush.
Developed against an RTX 5090; VRAM headroom matters more than raw speed.
