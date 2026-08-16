# Advisor kickoff

Paste into a fresh advisor session. **Rewritten 2026-08-16** at the close of the session that ran
E41–E44, two study swarms, four Grok consults and two Comfy consults.

**Read the calibration section before you trust a ruling here.** The seat that wrote this was wrong
about seven separate mechanisms in one day, most killed within an hour of being announced. What
held was the structure and the outside channels, not the seat.

---

> # ⚑ THE DEFECT IS NOT WHERE THIS FILE USED TO SAY IT WAS
>
> The previous banner read *"THE DEFECT IS IN THE BLEND. THAT IS SETTLED."* **It is not in the
> blend.** Blend variants are dead, and the sheet that "settled" it was structurally incapable of
> separating them — each candidate panel was the shipped render with only a few hundred flagged
> pixels rewritten.
>
> **Cornered as of this close: the defect is in the TEXTURE or the PROJECTOR.** Geometry, atlas
> boundaries, camera coverage, resolution and colour management are each dead on a measurement or
> a picture.
>
> **The strongest live lead is LOCAL TWIN-TO-MESH WARP** — measured, one view, unfinished.

## Your first move

```
cd E:\AI\facet && git pull
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py verify   <- 19/19 or stop
CLAUDE.md                                    <- the law book, read it whole
docs/grok-consult-3-brief.md                 <- the S0-S6 falsification sequence we are running
docs/experiments/E44-the-atlas-plan.md       <- ⚠ its diagnostic table is PARTLY VOID, see below
docs/comfy-consult-8-10-log.txt              <- consults 8-10, filed late
```

Two mounted servers: `mcp__facet-record__*`, `mcp__facet-measure__*`. `record_health` first.

⚠ **`pytest` may die with `PermissionError` on `pytest-current`** — a Windows temp-symlink issue,
not a test failure. Repair with `--basetemp=<scratch>`; it adds capability and removes no coverage.

## THE LIVE STATE

| | |
|---|---|
| HEAD | re-measure — `git log --oneline -1` |
| suite | **THE SUITE: 1107 tests, 1062 hermetic.** RE-COUNT before quoting — `pytest --collect-only -q` and again with `-m "not artifacts"`, currently 1107 total / 1062 hermetic. T34 pins ~14 surfaces off the collector and they all move in the same commit |
| the record | index recertified this session after **30 commits stale** — VERIFY PASSED, four legs, byte-identity, over 44 experiments. No staleness findings at the declaration leg |
| CI | verify at open |
| spend | **zero cloud credits, two sessions running.** Everything below is local |

## ⚖ THE DIRECTOR'S DECISIONS — all three now closed

1. **Which blend candidate** — **NONE.** His words: *"They all look equally like shit. Only the
   reference image is clear. The rest are the same image (blotchy)."* He was more right than the
   sheet's own authors: the four panels differed by 813/537/615/298 pixels in crops of tens of
   thousands. **They were identical by construction.**
2. **What the sword grip is made of** — **LEATHER**, delegated to the advisor, now `canon/
   W3-IDENTITY.md` **N17**, marked UNVERIFIED because it is predicted to land, not measured to.
3. **Whether the blend stage gets built** — moot. The blend is not the defect.

## ⚑ THE GROK CHANNEL — new this session, and the best instrument we have

**Grok Build runs code.** Not only a reasoner — it has an execution environment, so its test
results are real runs. Verify them here anyway; that is the protocol, not a slight.

**FIVE FOR FIVE on nominated calibration claims, and every one changed what we did:**

| # | claim | what it cost us |
|---|---|---|
| 1 | Callieri's border is **depth discontinuity**, not material boundary | reopened a lever we had closed |
| 2 | PartUV's Trellis row is 568.7/233.5, not the Common Shapes 48.6/974.8 we cited | our Gate 1 was a coin flip set from the wrong column |
| 3 | Open3D/UVAtlas completes **39.5%** on Trellis meshes | killed an arm before we ran it |
| 4 | `to_glb` passes `refine_iterations=0`; segmentation is **CuMesh cone clustering, not xatlas** | **voided three rows of our own diagnostic table** |
| 5 | its own selftest prints `0.6666666666666666` | its build landed correct on first run |

**THE PROTOCOL — carry it forward exactly:**

- **Every brief ends with "nominate one checkable claim."** Verify at primary source before
  weighting anything else, and report the result back either way. This is how a channel earns
  weight instead of being given it.
- **Resolve citations in the installed package**, not a GitHub tab. Claim 4 was verified in
  `o_voxel/postprocess.py` on this rig because that is the code that ran.
- **Hand it your candidates labelled as candidates and tell it to argue.** Its central critique —
  *"the brief already says the causal link is unproven, then writes a plan that only tests
  unwrappers; that is the hole"* — was correct and was the turning point of the session.
- **Give results back, including when its chip loses.** S0 was its call and its own hypothesis
  died on it. Telling it so is worth more than another question.
- **It can be delegated BUILDS.** `tools/callieri_border.py` is its work: MIT, numpy+scipy, pure
  functions, self-test, eleven hermetic tests, and it satisfied this repo's global-constant law by
  construction rather than by comment.
- Briefs live in `docs/grok-consult-N-brief.md`. ⚠ CORRECTED 2026-08-16 (consult #5 fold):
  this line used to say *"It has no repo access — every brief is self-contained"* and that
  is **false** — the Director's word, and the measurement: Grok Build read the tree, wrote
  `tools/s3_composite.py` + `tests/test_t77_s3_composite.py`, ran the suite, and updated
  all thirteen T34 count surfaces in its own change-set (verified on disk to the digit:
  selftest value, 61 passed, 1107/1062). The advisor repeated the false line twice before
  his correction landed — the inherited-claim law, on the advisor's own document. Briefs
  stay self-contained as good practice, not as a constraint; Grok leaves its work
  uncommitted for the advisor's fold, like any dispatched seat.

## WHAT DIED THIS SESSION, each on a measurement or a picture

| killed | how |
|---|---|
| **Colour management / view transform** | S0. Asset rendered FLAT + Standard, no AgX, still badly wrong vs twin. A/B differ 6.1/255; the gap to the twin is the whole material |
| **Mesh soup → the appearance** | S1. Welded in Blender, normals from restored connectivity, vs shipped: **1,034 px differ, max channel 3**. Both smooth. Soup never touched shading because the GLB carries explicit vertex normals |
| **Island-rim boundary contamination** | Repainted **16.3% of the atlas** magenta → **116 screen pixels** changed. Positive control returned 151,705, so the near-zero is real |
| **Blend-composite variants** | The sheet could not separate them; the metric moved 8 points while the eye saw nothing |
| **Camera geometry** | Blade already **96.35%** reachable against a measured **99.75%** ceiling; a downward camera buys 2.11 |
| **Source resolution** | 2× reaches ~15% of the affected population; 43.97% still straddles at 4× |
| **Premultiplied alpha** | 0.00e+00 against a fixture proven able to detect the error |
| **Minification aliasing** | Defect texels are **less** minified than clean neighbours, 0.380 vs 0.650 px |
| **The defect classifier itself** | Ten of twelve largest flagged regions sit on gold that is **correctly gold**; the visible green-on-leather-grip defect is **not flagged at all** |
| **E40's 74.28% blade never-hit** | Withdrawn as a coverage claim. Same instrument reports **97.99%** never-hit on the **torso** — the best-covered surface on the figure |
| **"TRELLIS ships xatlas UVs"** | False, and it sat in this repo's own tool docstring since E05. It is CuMesh cone clustering; xatlas only subdivides inside a cluster somebody else cut |
| **CuMesh refinement as a chart-count dial** | Welded+refined gives 4,505 charts vs 2,654 unrefined. TRELLIS's fast-path settings are better. Caught only by the control arm |

## WHAT IS TRUE AND MEASURED

**The mesh is triangle soup and it welds losslessly.** 41.1% adjacency completeness, **139,014
single-triangle components**, V−E+F = −60,781. Welding at 1e-6 (stable to 1e-4, zero degenerate
faces) gives **99.2% adjacency, 271 components, 141,561 verts** — the manifold expectation.
Reproduced independently in numpy and in Blender.

**Welding collapses chart count 55×** — 146,462 → 2,654 cone clusters. So **weld before any new
unwrap**; clustering has no adjacency to grow through otherwise. **Do not expect it to fix the
look** — S1 says it will not.

**The shipped rig is 8 cameras, not 8+2.** Yaw 0 and 180 at **+55° instead of flat**. Three
independent sources. The rig is therefore *already partially ring-broken*.

**The atlas has 9,166 islands, median 102 texels**, 17.8% of painted area within one texel of an
edge — **and that is an atlas share, not a screen claim.** It renders as 0.076% of the figure.

**`facing^6.0` is not baseless** — it matches Meta 3D TextureGen §4.2.1's published α=6.

**`tools/callieri_border.py` exists now** (Grok's build, MIT). Four surfaces: `border_weight`
(true Euclidean distance transform), `depth_edge_mask` exposed separately so the discontinuity set
can be looked at, `mixed_depth_reject` as a distinct 2×2 gate, `facing_weight` with the exponent
parameterised. Its own stated limit: **wrong paint where depth is locally smooth is invisible to
it.**

## ⚠ THE STRONGEST LIVE LEAD — unfinished, hand it to a seat

**Local twin-to-mesh warp.** Measured on **one view only** (yaw 45), silhouette-based:

- Global registration is fine and the record's "twins register at shift (0,0)" is **true** —
  IoU **0.9203**, centroid offset 2.88 × 2.60 px.
- **Per-tile offsets range −8 to +6 in x and −8 to +8 in y, std 3.71 / 4.09**, around a mean near
  zero. A uniform shift would show near-zero spread. **This is a warp, and the global number hides
  it completely.**
- Several tiles **pin at the ±8 search limit**, so true offsets are larger than the window.

**Why it fits where nothing else did:** E41 measured defect texels a median **0.439 px** from a
material boundary. A 4–8 px local displacement puts those samples across it. That explains why
blending cannot fix it (every view samples the wrong place), why resolution cannot (a sharper twin
sampled 6 px off is still wrong), why coverage is irrelevant, and why the twin looks clean while
the asset does not.

**Before anyone believes it:** widen the window until offsets stop pinning · all eight views ·
silhouette agreement is blind to slip *inside* the figure, so an interior correspondence check is
required · and ControlNet is not a calibrated camera, so this is a plausible mechanism, not a
proven one.

## THE PLAN — Grok's S0–S6 sequence

Ordered cheapest-first, each step **rules something out**. Written by Grok in consult #3 because we
were good at executing measurements and bad at choosing which one.

| step | what | status |
|---|---|---|
| **S0** | flat/Standard vs Studio/AgX vs the twin | ✅ **RUN** — colour management dead |
| **S1** | soup vs welded clay, normals from welded connectivity | ✅ **RUN** — soup is not the appearance |
| **S2** | the A–E stage dump: which stage makes the soup | not run — diagnostic only |
| **S3** | existence proof in the **Blender compositor**: can the plates blend? Two stills — view-dependent, and view-independent via argmax-facing per surface ID | not run — **`callieri_border.py` now exists for it** |
| **S4** | Callieri border + mixed-depth reject on the current projector; look at green-on-grip | not run |
| **S5** | Arm A — vertex colours on the welded mesh, 8 stills | not run |
| **S6** | Arm B — unwrap the welded mesh (~2,654 charts), project, render | not run |

**Do not run UVAtlas, PartUV, or a quad remesh until S6 has failed.** They change the variable that
has not been isolated.

## ▶ START HERE NEXT SESSION — delegate a bigger build to Grok

**The build: the S3 existence proof, end to end.** It is the biggest thing on the board, it is the
step that discriminates *"the plates are fine and our 3D path degrades them"* from *"the plates do
not project"*, and Grok has specified its shape twice and already built its hardest component.

Ask for a runnable module that, given per-camera twin + non-normalised depth + camera normals +
silhouette + camera matrices:

1. **reprojects any twin into any camera's frame** — the piece **Comfy cannot do** (no
   camera-matrix warp exists there, verified consult #12);
2. composites with `callieri_border` weights × facing × visibility, primary-plate-first;
3. emits **both** stills — view-dependent, and view-independent via a single global argmax-facing
   per surface ID;
4. ships a synthetic self-test and nominates a calibration number, same protocol.

**Give it the constraint that kills the naive version:** eight independently-beautiful mutually
inconsistent stills fail. Consistency is a **surface field**, not a per-still choice.

We supply the AOVs, and we may not need Blender's compositor for them: `silhouette_masks.py`
exists, prep emits `pos.npy`/`nor.npy`, `cam.json` carries verified matrices, `project_twins`
already raycasts, and `_owner.npy` is already a global per-texel view label — the surface ID the
consistency fix needs. **Enumerate before commissioning.**

## HARD-BLOCKED

`polycount.com` · `reddit.com` · `docs.blender.org` · `marmoset.co` · `web.archive.org`.
`projects.blender.org` answers at `/api/v1/`. **Do not open the Browser pane — it crashed the
client twice.** Comfy Cloud has **no channel to ingest an off-platform mesh at any face count**
(`Load3D.model_file` is a COMBO with `choices:["none"]`) and no float-EXR loader, so it cannot be
the AOV venue.

Local licences, checked on disk: ComfyUI-GGUF Apache-2.0 · Trellis2 MIT · **KJNodes GPL-3.0** ·
**Manager GPL-3.0**. Image-Filters/essentials are **not installed here** — that flag was about the
Cloud install. xatlas MIT, CuMesh MIT, trimesh MIT. **pymeshlab is GPL — never import it into
anything shipped.**

## THIS SEAT'S RECORD — read before trusting its rulings

**Seven mechanisms announced then killed, most within the hour:** minification aliasing ·
island-rim contamination · the CuMesh refinement dial · soup-causes-faceted-normals · the atlas as
the deciding defect · a re-unwrap plan our own tool had already tried and recorded as worse · and a
Comfy consult numbered #9 when #10 had already run.

**Three recurring shapes, all this repo's own named laws, all violated by the seat that quotes
them:**

- **An atlas share is not a screen claim.** Quoted at the Director in the morning; committed by
  lunch with the 17.8% rim figure.
- **Read the listing complete.** Numbered a consult from a `docs/` directory that stops at 8.
- **Corner-median keying is retired.** Reached for it anyway on a twin with a gradient backdrop
  and keyed 62.7% of the frame as figure.

**What held:** the calibration protocol, dispatched seats that killed the advisor's premises four
separate times, the control arm that caught the refinement dial, positive controls before believing
a near-zero, and every fold committed and pushed.

**And the process failure the Director named directly, which matters more than any of the above:**
this seat repeatedly ended a turn *announcing* work instead of doing it — four times — and let the
advisor role shrink to delegation while the tree sat uncommitted for hours. *"That's lazy and the
source of a lot of my headaches."* **Do the work in the turn. Keep the tree clean as you go.**

**Deciding is the job. Predicting is not. Announcing is not either.**

## Environment

```
python   E:\AI-Models\trellis2-env\Scripts\python.exe      <- ABSOLUTE, always
blender  "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"   -b -P only
assets   E:\AI\training\facet_E0*\  facet_E4*\
```

⚠ **The VRAM watchdog was DEAD for most of this session** and was never restarted. Check before any
GPU work: `pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1`.

Scripts create their own output dirs. ASCII in tool output. `argparse` eats leading minus signs.
Generation is cloud-only and nothing in the plan needs it.

## Do not

End a session the Director has not ended · announce work instead of doing it · leave the tree dirty
across turns · present a surface you have not walked at native size · `git add -A` · quote an
external claim before resolving it at its primary source · treat a countable proxy as the question
when his eye is the question · re-derive anything in WHAT DIED.
