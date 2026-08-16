# Study swarm — sampling, view weighting, and camera rig

**Run 2026-08-16** at the Director's explicit trigger. Five parallel Sonnet research agents,
one per question, under `memory/research-grounded-advisor-protocol.md`. Every agent was required
to open primary sources, return author / year / title / URL plus a one-sentence finding in its
own words, and mark **UNRESOLVED** rather than report from a search snippet.

**Read the correction at the top of §0 before using anything here.** Two agents contradicted
each other on the exact constant our route ships, and the advisor resolved it at the primary
source rather than folding either version.

---

## §0 The contradiction, and its resolution

**Agent Q2** (classical photogrammetry texturing) returned: *no published system uses a cosine
power greater than 1*. **Agent Q3** (diffusion texturing) returned: *Meta 3D TextureGen uses
`cos^6`*. Our route ships `w = np.power(facing[idx], args.power)` with power **6.0**
(`tools/project_twins.py:873`), so the disagreement was directly about our own constant.

**Resolved by the advisor at the primary source.** Meta 3D TextureGen, §4.2.1
(https://arxiv.org/html/2407.02430v1), verbatim: *"We use n=4, as the number of generated views
and **α=6** for all of our experiments."*

**Both agents were right inside their own literature.** The disagreement was scope, not error:
the classical MVS-texturing literature (2007–2014) carries no cosine power above 1; the diffusion
texturing literature (2023–2026) does. This is the second consecutive swarm in which two agents
contradicted each other and the primary source settled it — the first was AliceVision's band
ordering. **An agent's report is testimony, not a resolved source.**

⚠ **This corrects the advisor.** In the session that ran this swarm the advisor told the Director
that `facing^6.0` "has no basis in the literature." That is **false**: it matches a shipping
system's published constant exactly. The honest statement is that our exponent is *inherited and
undocumented*, and happens to coincide with Meta 3D TextureGen's α — **with the caveat that they
use it over n=4 views and we use it over 8+2.**

---

## §1 What shipping tools expose, and what they weight by

`multiBandNbContrib` band ordering, **settled from `Texturing.cpp` source rather than paraphrase**:
`pyramidL[0]` is the finest level, and the loop's `contrib` index runs over *all* sorted cameras
without resetting, so `{1,5,10,0}` is a vector of **cumulative band boundaries**, not per-band
counts. Camera rank 0 (the single best) paints band 0; ranks 1–4 reach band 1; ranks 5–9 reach
band 2. **Best views paint fine detail; weaker views only ever reach coarse bands.**

| tool | exact parameter | default | mechanism |
|---|---|---|---|
| AliceVision | `nbBand` | `4` | Laplacian-pyramid levels |
| AliceVision | `multiBandNbContrib` | `{1,5,10,0}` | cumulative band-boundary counts (above) |
| AliceVision | `useScore` | `true` | `false` → uniform weight `1.0f` per contributing triangle |
| AliceVision | `bestScoreThreshold` | `0.1` | drop cameras scoring `< 0.1 ×` the best |
| AliceVision | `angleHardThreshold` | `90.0°` | drop camera beyond this normal/view angle; `0.0` disables |
| Metashape | `BlendingMode` | Mosaic (UI) | Mosaic = one best source per texel + low-frequency seam blending, explicitly *"does not mix image details between overlapping photos"* |
| RealityCapture | Coloring Method | Multi-band | frequency-split, joined after |
| Blender bake | `margin_type` | `ADJACENT_FACES` (since 3.1) | samples across the UV seam from the neighbour island |

**AliceVision's published weight, verbatim from source:**
`const double score = area * double(verticesSupport)` — projected triangle area in that camera's
image, times how many of the triangle's three vertices that camera sees. **There is no angle term
at all.**

## §2 View weighting in the classical literature

- **Lempitsky & Ivanov, CVPR 2007**, DOI 10.1109/CVPR.2007.383078 — founding MRF formulation.
  Data cost `w_i^j = sin²φ + α`, a **sine-squared obliquity penalty, not a cosine power**, with a
  per-edge seam-visibility term. Hard winner-take-all labelling via α-expansion. They report that
  swapping the data term for border-distance or colour-median *"tended to give similar results"* —
  **the data term's shape barely matters once a seam term exists.**
- **Waechter, Moehrle & Goesele, ECCV 2014**, DOI 10.1007/978-3-319-10602-1_54 — states plainly
  that an angle-only data term *"is insufficient… as it chooses images regardless of proximity,
  resolution or out-of-focus blur"*, and **explicitly rejects a bare angle weight**. Adds a
  photo-consistency outlier rejection over per-view mean colours.
- **Gal et al., CGF 2010**, DOI 10.1111/j.1467-8659.2009.01617.x — data term is integrated image
  **gradient magnitude**; foreshortening enters only implicitly through projected area. No cosine
  factor anywhere. Frames blending itself as the problem: *"ghosting and blurring artifacts when
  textures are geometrically misaligned."*
- **Callieri et al., C&G 32(4), 2008**, DOI 10.1016/j.cag.2008.05.004 — the field's one true
  continuous per-texel blender, and the closest published analogue to our weight. Three masks
  combined **by product** specifically to preserve minima: angle = plain cosine, **power 1**;
  depth ∝ 1/depth² (a geometric argument, not a tuned constant); and a **border mask = image-space
  distance to the nearest border or silhouette discontinuity.**
- **Allène, Pons & Keriven, ICPR 2008**, DOI 10.1109/ICPR.2008.4761913 — rejects heuristic
  angle/distance combinations for `E_detail = -Σ area(...)`: **pure footprint, zero angle term.**

**Synthesis:** the dominant modern practice is **winner-take-all label selection plus seam
repair**; full per-texel soft blending is the minority approach and is explicitly blamed in this
literature for ghosting and blur wherever geometry or registration is imperfect. **Every system
here that is not pure winner-take-all carries a footprint/resolution term. Our weight is angle
alone.**

## §3 Correlated views — the gap in the field

Our measured situation: 100% of multi-camera defect faces span ≤ 90°, median 45°; adjacent
cameras under near-identical control **fail together**.

**No system reviewed models or measures correlated failure across adjacent views.** They either
reconcile post-hoc by a geometric heuristic assuming per-view independence, or synchronise latents
during denoising to force early agreement — which suppresses visible seams while saying nothing
about whether the agreed content is *correct*.

⚑ **The one inconsistency metric that exists measures agreement, not correctness.** SyncMVD's
3D-consistency score is mean pairwise CLIP cosine over rendered views — **it would score a
hallucination that every adjacent camera agrees on as maximally consistent.** That is our exact
failure mode, and it is unaddressed anywhere reviewed.

Rig and mechanism, per system: TEXTure (arXiv:2302.01721) sequential trimap, 8 equatorial + 2;
Text2Tex (2303.11396) generation-mask states + greedy next-best-view; SyncMVD (2311.12891) latent
UV-blend each denoising step with weight `cosθ^α`, α scheduled low→high, 8 @ 45° + 2 elevated;
MVPaint (2411.02336) image-space fuse `T′=Σcos(v,n)·Tᵢ`; Paint3D (2312.13913) earlier-view-wins;
FlashTex (2402.13251) 4 reference views + SDS; **TexFusion (2310.13772) — a dedicated 3-ring,
24-camera rig for human characters, the most explicit character treatment found**; Meta 3D
TextureGen (2407.02430) incidence-weighted blend at α=6 over 4 views, coverage gaps handed to a
**dedicated UV-inpainting network**.

A 2026 survey carves out **"3D Humans Texturization" as its own taxonomy section** — the field
treats character texturing as a specialised sub-problem, not a routine eval case.

**Correlated-error literature outside texturing:** Covariance Intersection (Julier & Uhlmann,
Proc. ACC 1997, pp. 2369–2373) is sensor fusion's standard answer to unknown cross-sensor
correlation, producing a fused estimate that never claims more confidence than worst-case
correlation permits. Kuncheva & Whitaker (*Machine Learning* 51(2):181–207, 2003,
DOI 10.1023/A:1022859003006) is the classic result that **ensemble gain shrinks as pairwise
member-error correlation rises** — the formal version of our 90°-span finding. No texturing system
uses anything like either.

## §4 Sampling — the mechanism that fits the defect

Our route sub-samples with a hand-rolled 2×2 `bilinear` (`project_twins.py:399-413`), no mip
chain, no footprint, no anisotropic filter.

- **Heckbert 1989**, *Fundamentals of Texture Mapping and Image Warping* (CMU MS thesis) §3.1 —
  point-sampling images containing high frequencies produces *"objectionable moire patterns…
  called texture aliasing."* §3.5.8–9 fixes it with a resampling filter whose texture-space
  footprint is the reconstruction filter warped by **the local Jacobian** of the map.
- **Greene & Heckbert 1986**, IEEE CG&A 6(6):21–27 — the Elliptical Weighted Average filter,
  built explicitly because *"point sampling… will cause aliasing."*
- **Williams 1983**, *Pyramidal Parametrics* (SIGGRAPH) — *"sampling high-resolution data at
  larger sample intervals invites aliasing."*
- **McCormack et al., Feline** (WRL 99/1) — even mip-mapped trilinear *"severely blurs"* under
  anisotropy, because treating a screen-space footprint as square in texture space is wrong.
  **With no mip chain we get neither that blur nor a correct ellipse — just raw aliasing.**

⚑ **AliceVision ships the identical shortcut**, read directly from source: per-texel colour comes
from plain bilinear `getInterpolateColor`, with **no footprint, mip or pyramid anywhere in the
sampling path**. Its only pyramid is multi-band blending on the *output* atlas. **Its defence
against minification is view selection — `score = area * verticesSupport`, preferring close and
fronto-parallel cameras — not filtering.**

**Predicted signature** (inferred by the agent, not stated in any source, and flagged as such):
unfiltered undersampling is **high-variance noise, not a systematic shift** — mip/trilinear blur
softens edges, point-like sampling *scatters*. Across views this should read as **per-view speckle
at a material boundary.**

**Premultiplied alpha**, the second suspect: Porter & Duff 1984, *Compositing Digital Images* —
un-premultiplied interpolation is a different, wrong operation rather than an approximation. Error
is **zero wherever alpha is constant over the footprint**, confined to footprints spanning an alpha
transition, sign pulling toward whatever RGB sits in transparent texels. **Real but conditional:
dormant if source sampling touches only opaque interior pixels.**

## §5 Camera rigs — one prior verified, one falsified

| system | views | azimuths | elevations | source |
|---|---|---|---|---|
| SyncMVD | 10 | 8 × 45° | 0° × 8 + 2 elevated (° unstated) | arXiv:2311.12891 |
| **MVPaint (best)** | 8 | 45° spacing | **interleaved ±30°** | 2411.02336 Table S2 |
| TEXTure | 10 | 8 equatorial + 2 | init θ = **+60°**; top/bottom ° unstated | 2302.01721 §3.1 |
| Hunyuan3D-2 | 6 | 0,90,180,270,0,180 | 0,0,0,0,**+90,−90** | `hy3dgen/texgen/pipelines.py` |
| Meta 3D TextureGen | 4 | 0,90,180,270 | fixed +20° | 2407.02430 |
| FlashTex (best) | 4 | front/back/L/R | equator | 2402.13251 Table 5 |

- ✅ **MVPaint VERIFIED exactly.** Table S2: N=8/φ=0° → FID **23.45**; N=16/φ=0° → **25.71**;
  best cell N=8 interleaved ±30° → **20.89** (also beating N=16/±30°'s 21.58). Authors attribute
  the N=16 decline to over-smoothing from excessive view overlap. **Breaking the ring buys ~11% at
  equal view count; adding views costs.**
- ❌ **TEXTure's "back-low view at −60°" is FALSIFIED.** §3.1 states 8 viewpoints plus two
  top/bottom — a 10-view rig shaped like SyncMVD's and like ours. The only concrete elevation is
  the *initial* viewpoint at **+60°, positive**. This claim appeared in `docs/advisor-kickoff.md`
  and must be corrected there.
- ✅ **Hunyuan3D-2's −90° camera is real**, verified in `Hunyuan3DTexGenConfig` — but
  `candidate_view_weights=[1,0.1,0.5,0.1,0.05,0.05]` trusts it at **0.05**, ~20× less than front.
- **Downward-facing surfaces are conceded, not placement-solved.** Meta 3D TextureGen hands
  "unpainted areas" to a second-stage inpainting network; Text2Tex's next-best-view is confined to
  36 predefined **non-below-horizon** viewpoints. Hunyuan3D-2 is the sole system with an actual
  −90° camera and still downweights it near zero.
- **No published never-hit statistic exists** to compare our 74.28% against.

---

## What this changes in the record

1. **`facing^6.0` is not baseless** — matches Meta 3D TextureGen's α=6 (§0). The advisor's
   contrary statement is corrected above.
2. **`docs/advisor-kickoff.md`'s TEXTure −60° claim is falsified** (§5) and needs correcting in
   place.
3. **Our route has the aliasing shortcut *and* lacks the compensating mechanism.** AliceVision
   shares our plain-bilinear sampler but defends with a **footprint-based view score**; Callieri's
   soft blend carries **depth and border-distance** terms. Our weight is angle alone
   (`project_twins.py:873`). This is a sourced mechanism for blotchiness — **it is a hypothesis
   for E41 to test locally, not a finding.**
4. **Our rig is the flat-ring configuration MVPaint measured as worse** — bounded by E42 before
   any generation spend.

## Hard-blocked in this environment

`polycount.com` · `reddit.com` · `docs.blender.org` · `marmoset.co` · `web.archive.org` — all
403 to agents and advisor alike. `projects.blender.org` answers at `/api/v1/`. The Browser pane
must not be opened in this workspace. **The two largest practitioner boards for this domain are
unreachable, and that is a real gap in this swarm as in the two before it.**

## UNRESOLVED — carried forward rather than guessed

- Blinn, *Fun with Premultiplied Alpha*, IEEE CG&A 16(5) 1996 — Xplore returned HTTP 418.
- AliceVision: what happens to cameras beyond `nbContribMax` when `multiBandNbContrib.back()==0`
  (the shipped default) — literal code gives `nbContribMax=0`, which would make the loop body never
  execute. **Flagged rather than guessed; worth resolving, since it governs the default path.**
- SyncMVD's exact top-camera elevation in degrees — repo config paths 404'd.
- Text2Tex / Paint3D actual axis-aligned angle values; FlashTex's top/bottom elevations.
- Hunyuan3D 2.1/2.5 camera config (only 2.0 checked).
- Metashape / RealityCapture weighting formulae — neither vendor publishes algorithmic detail.
- Whether **any** paper in this literature distinguishes *material/identity hallucination* from
  the geometric Janus problem they all target. No source found makes the distinction, which reads
  as an unaddressed gap rather than a measured absence.
