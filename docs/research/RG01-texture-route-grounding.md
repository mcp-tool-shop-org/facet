# RG01 — Research grounding for the texture route

**Status: ⚠ UNVERIFIED — NOT LOAD-BEARING.** Every citation below is pending the
family-different verification gate. Nothing here may justify an architectural choice until it
clears. Findings are recorded now so the dispatch is auditable, not so they can be used early.

**Dispatched:** 2026-08-05, advisor session, 5 parallel research lanes under the
research-grounded advisor protocol. Fired because E08's recommendation — "more reference
views" — was a single-axis answer to a heavily published problem, which is one of the
protocol's named triggers.

**Cost:** 450,961 subagent tokens, 160 tool calls, under 8 minutes wall clock (parallel).

---

## ⚠ Read this before any number below

**Four of the five lanes ranked methods by FID and KID. The fifth measured what those numbers
are worth against human judgement, and the answer is: very little.** HYPE (Zhou et al. 2019,
arXiv:1904.01121) measured correlation between FID and human perceptual score at **ρ = −0.029,
p = 0.96**; Stein et al. 2023 (arXiv:2306.04675) found none of 17 metrics strongly correlating
with human realism.

So: **mechanism claims from these papers are usable; their FID rankings are not.** SyncMVD's
ablation showing ghosting when synchronisation is removed is a mechanism claim. "SyncMVD beats
Text2Tex by 13 FID" is not a reason to prefer it. This caveat is applied throughout, and it is
the single most important thing the swarm produced — a five-lane dispatch that would otherwise
have ranked our options on a metric with no measured relationship to the Director's eye.

---

## Lane 1 — multi-view consistency

1. **Consensus is formed during denoising, not after it.** Liu, Xie, Liu & Wong 2023
   (arXiv:2311.12891, SyncMVD). Projects the predicted clean latent to UV at every denoising
   step, resolves overlaps, rasterises back — consensus forms early while latents are still
   low-frequency; the ablation without synchronisation reports views "significantly different"
   with severe ghosting. Runs 8 equatorial + 2 elevated cameras, MIT, zero-shot on stock SD1.5
   + ControlNet depth/normalbae. *Implication: our route projects after generation completes,
   which is the configuration its ablation calls the failure case. And its licence and stack
   sit inside our constraints rather than outside them.*
2. **Ownership beats averaging, independently derived.** Cao, Kreis, Fidler, Sharp & Yin 2023
   (arXiv:2310.13772, TexFusion). Explicitly rejects averaging; overlaps resolve by
   quality-based selection from image-space derivatives — the most head-on camera owns the
   texel. *Implication: confirms the rule that put `bake_multiview_glb.py` in `superseded/`.
   Nothing to change; recorded because independent derivation is evidence.*
3. **Synchronisation costs detail, and the cost is priced.** TexFusion users preferred it for
   natural colour 75.58% and fewer artifacts 68.60%, but preferred the *inconsistent* baseline
   for detail **65.12%**. *Implication: consistency machinery is not free, and detail is what
   E09's density axis is about. Do not adopt sync without measuring detail loss.*
4. **Omitting synchronisation is priced too.** Yan, Wu, Lin et al. 2025 (arXiv:2506.02620,
   FlexPainter): ablating view synchronisation costs +9.02 FID; ablating learned UV weighting
   +5.05. *Implication: the tradeoff is real in both directions — see the FID caveat above
   before weighting this.*
5. **More views converge rather than diverge, given ownership gating.** Chen et al. 2023
   (arXiv:2303.11396, Text2Tex): refinement views 0/5/10/15/20 → FID 37.09 / 36.67 / 36.39 /
   35.98 / 35.68, monotone. *Implication: E08's core assumption survives — added references do
   not have to fight each other, provided assignment arbitrates them.*
6. **Position + normal renders give explicit cross-view point correspondence.** Bensadoun et
   al. 2024 (arXiv:2407.02430, Meta 3D TextureGen). 4 views in one joint pass conditioned on
   position and normal renders, 19 s. *Implication: `render_geomaps.py` already produces
   exactly these maps at <1/255 MAE and we feed the ControlNet a canny edge map instead.*
7. **Per-view regional prompts kill Janus artifacts.** Kim, Kang, Choi et al. 2024
   (arXiv:2409.19989, RoCoTex). *Implication: independently confirms E01's per-view prompting
   result, which took back-view face detections 1 → 0.*

## Lane 2 — conditioning the fill

8. **Denoise 1.0 is the documented degenerate case.** Meng et al. 2021 (arXiv:2108.01073,
   SDEdit) sweeps t₀ and recommends **0.3–0.6**, stating that as t₀ → 1.0 the method produces
   random realistic images, "with the extreme case being unconditional image synthesis."
   *Implication: our brush runs at 1.0. The plaited belt is the setting behaving as documented,
   not a tuning miss.*
9. **Per-pixel denoise strength replaces binary masks and post-hoc blending.** Levin & Fried
   2023 (arXiv:2306.00950, Differential Diffusion) — inference-only, maps a continuous change
   map to per-pixel strength; reported to beat alpha, Poisson, Laplace and blurred-mask
   blending on boundary artifacts. *Implication: E07's L2 attacked seams with a Poisson
   membrane after the fact. This says the mechanism belongs in the denoise schedule. If it
   verifies, L2 is withdrawn rather than re-anchored.*
10. **Measured on mesh texturing specifically.** RoCoTex (arXiv:2409.19989) reports Text2Tex's
    constant per-region strength "is not effective" at seam reduction and replaces it with a
    blurred mask plus Differential Diffusion; also reports depth-only ControlNet distorting
    hair, fixed by stacking controls. *Implication: two independent reasons to change our
    canny-only, binary-mask conditioning.*
11. **Exemplar adapters are engineered to discard identity.** Yang et al. 2023
    (arXiv:2211.13227, Paint-by-Example) imposes an information bottleneck — exemplar
    compressed to a single CLIP token — explicitly "to avoid the trivial solution of directly
    copying and pasting the exemplar." Chen et al. 2023 (arXiv:2307.09481, AnyDoor) quantifies:
    CLIP-only conditioning scores DINO **31.5** against DINOv2 + segmentation's **67.8**.
    *Implication: IP-Adapter-class reference conditioning was my obvious next reach and it is
    the wrong tool — it conditions on the embedding that collapses.*
12. **Text contaminates the image condition at the input convolution.** Ju et al. 2024
    (arXiv:2403.06976, BrushNet): prior inpainting UNets fuse noisy latent, masked-image latent
    and mask at the first conv, where "they are collectively influenced by the text embedding";
    BrushNet uses a separate branch with text cross-attention removed. *Implication: a
    mechanism for our measured prompt-overrides-contour failure.*
13. **Our operating point is not benchmarked.** No headline text-guided inpainting benchmark
    publishes a >50%-mask split — EditBench 240 images (arXiv:2212.06909), BrushBench 600,
    neither binned by mask ratio; Blended Latent Diffusion (arXiv:2206.02779) is explicitly
    thin-mask work. We inpaint 50–95% of a view. *Implication: carry this caveat on every
    number in lanes 1–2. They are measured outside our regime.*

## Lane 3 — view selection and order

14. **Assignment is comparative in the published methods, absolute in ours.** Text2Tex
    (arXiv:2303.11396) marks a texel "update" when the current view sees it at **higher
    cosine than any view that already painted it** — relative ranking, not an absolute cutoff.
    TEXTure (Richardson et al. 2023, arXiv:2302.01721) decides its trimap on n_z the same way.
    *Implication: this is the finding that corroborates the E08 Gate 0 ruling. Our absolute
    gate runs BEFORE ownership, so a texel seen obliquely by every camera is discarded by all
    of them instead of being assigned to the one that sees it best.*
15. **The hand-tuned facing threshold is named in the literature as the thing to replace.**
    Im2SurfTex 2025 (arXiv:2502.14006) quotes standard practice as "a hand-tuned threshold
    n_u·v_c > thr to avoid copying colors from obscure views" and replaces it with learned
    attention weighted by normal-to-view angle. *Implication: our `--facing-min 0.45` is that
    threshold, by name.*
16. **~60° is an empirically defensible incidence limit.** Soudarissanane et al. 2011
    (DOI:10.1016/j.isprsjprs.2011.01.005): above 60° incidence angle dominates measurement
    precision. cos 60° = 0.5. *Implication: our 0.45 (≈63°) is a defensible floor value. The
    defect is where the floor sits in the pipeline, not what number it holds.*
17. **Adaptive view selection buys little; ordering and accumulation control buy a lot.**
    Text2Tex's automatic next-best-view over 36 candidates moves FID 37.09 → 35.68; COVER
    (Chen et al. 2026, arXiv:2604.05259) reports 22.12 vs 21.80 PSNR over random selection.
    *Implication: do not build adaptive view selection. Our fixed ladder is fine; spend the
    effort on assignment and order.*
18. **Unseen surface should be propagated in 3D, not in UV.** MVPaint 2024 (arXiv:2411.02336)
    fills unobserved points by kNN over spatial proximity and normal similarity, explicitly
    because "adjacent 3D areas are frequently mapped to non-adjacent 2D regions." *Implication:
    E07's L1 is this technique, independently derived. It was right in kind.*

## Lane 4 — UV space and chart structure

19. **Re-unwrapping is measured on our exact generator's output.** Wang et al. 2025
    (arXiv:2511.16659, PartUV) on 114 **TRELLIS** meshes: xatlas 1541.6 mean / 895 median
    charts → 538.8 / 221.5; seam length 91.2 → 55.9; **area distortion improves** 2.357 →
    1.300; 13.1 s → 41.9 s. SeamCrafter (arXiv:2509.20725) on AI-generated meshes: 135.42
    fragments / 14.75 distortion → 33.72 / 10.63. *Implication: both metrics improve together,
    which refutes the fragmentation-versus-distortion tradeoff I assumed when I parked E09.*
20. **Cheap chart counts are available; cheap low-distortion chart counts are not.** Nuvo
    (arXiv:2312.05283) reaches the lowest chart count measured but the worst area distortion in
    PartUV's table and 2908.8 s per mesh. *Implication: do not chase chart count alone.*
21. **Every working UV-space generator reintroduces 3D adjacency as an explicit channel.**
    Paint3D (arXiv:2312.13913) conditions UV inpainting on a **position map**, each texel
    carrying its 3D coordinate, because fragmentation "complicates the learning of the 3D
    adjacency relationships among the fragments in the UV plane"; TEXGen (arXiv:2411.14740)
    rasterises UV features into a point cloud and back; MV2UV (arXiv:2603.15436) uses UV
    self-attention keyed on XYZ + normal and reports a **50.8 FID improvement on occluded-region
    completion**. *Implication: `bake_hero_prep` writes `pos.npy` — a per-texel 3D position map
    in atlas layout — and we have never fed it to the generator.*
22. **Even the UV-native model normalises the parameterisation first.** TEXGen runs xatlas to
    re-unfold every asset to a single atlas before training. *Implication: a better atlas is
    upstream of every other option here, including the ones that claim to not need one.*

## Lane 5 — metrics

23. **The only human-validated metric for textured meshes was not validated on our defect.**
    Nehmé et al. 2023 (arXiv:2202.02397, Graphics-LPIPS): 3,000 stimuli, 148k scores, 4,513
    participants, PLCC 0.85 / SROCC 0.86 — over geometry and texture *compression* distortions.
    No wrong-material condition in the validation set. *Implication: there is no off-the-shelf
    validated metric for what we are chasing.*
24. **Material plausibility is a measured axis and image metrics are near chance on it.**
    Hi3DEval (arXiv:2508.05609, NeurIPS 2025 D&B), 15,300 assets with 11k material annotations:
    pairwise accuracy against human annotation (chance 0.5) — Material Plausibility CLIP-Score
    **0.640**, Consistency & Artifacts CLIP-Score **0.543**. *Implication: CLIP score was my
    fallback and it is a coin flip on our defect.*
25. **Graphics separated the two error terms in 2020 and we implemented only one.** Andersson
    et al. 2020 (DOI:10.1145/3406183, FLIP) computes a colour-difference term *and* a separate
    edge/feature term, because neither alone covers rendering error. *Implication: E07's five
    units were five feature terms and zero colour terms. E08 Gate 0's ΔE instrument is the
    missing colour term. Report both from here on.*
26. **The formula matters at the magnitude we care about.** JND is ΔE*ab ≈ 2.3 (Mahy, Van
    Eycken & Oosterlinck 1994, Color Res. Appl. 19(2):105–121); measured 50:50 thresholds are
    perceptibility 0.6–1.0 and acceptability 1.8–2.0 ΔE00 (Paravina et al. 2015,
    DOI:10.1111/jerd.12149, adopted into ISO/TR 28642:2016); and CIEDE2000 is fitted to *small*
    differences — for ≥10 CIELAB units the best-performing metric is **HyAB** (Abasi, Tehran &
    Fairchild 2020, DOI:10.1002/col.22451). *Implication: the executor's CIE76 choice is sound
    where CIEDE2000 would not have been; HyAB is the measured upgrade.*
27. **Region-level material error is checkable with off-the-shelf segmenters.** MINC (Bell et
    al. 2015, arXiv:1412.0623) 23 categories, 73.1% per-pixel mean-class accuracy; DMS
    (Upchurch & Niu 2022, arXiv:2207.10614) 46 materials, 0.729 per-pixel. *Implication: "a
    steel blade wearing skin" is a material-label disagreement. A second, independent
    instrument is available.*
28. **Local-window statistics returning "no error" on large errors is documented.** Nilsson &
    Akenine-Möller 2020 (arXiv:2006.13846): SSIM yields values near 1 where error is large.
    *Implication: the E07 failure mode has literature. It was avoidable.*
29. **The gap we fell into is a gap in the field.** MatAtlas (arXiv:2404.02899), the closest
    published work to what we are building, reports **no quantitative material-correctness
    metric at all**. *Implication: worth knowing before assuming a standard instrument exists
    that we simply failed to find.*

---

## Verification status — ⚠ HALTED AND ESCALATED. The oracle was down, and we took it down.

**Run 1, 2026-08-05.** `roleos` is absent on this rig, so the locked path was unavailable;
`prism` is on PATH with Ollama carrying mistral-small:24b, granite4.1:30b and gemma4:31b — the
documented fallback substrate. Ran `prism verify --type citations --caller-family anthropic
--provider ollama --gate` over all 32 citations. Verdict **revise**, exit 10, Ed25519-signed
receipt `kid ed25519-e0963e93294fbb0d`, `reasoning_visibility_mode` stripped, verifier family
`local` — so the family-different and reasoning-stripped requirements held for every lens that
actually ran.

```
existence:  resolved 3 · metadata_mismatch 1 · UNRESOLVABLE 28
verdicts:   accept 1 · revise 1 · escalate 30
details:    arXiv oracle unreachable — ReadTimeout 24, HTTPStatusError 4
            resolved but claim not in title+abstract          1  (c26)
            resolved but no abstract available to ground       1  (c14)
            resolved to a different title than cited: 'FLIP'   1  (c25)
            source supports the claim                          1  (c27)
FABRICATED: 0        REFUSED: 0
```

**28 of 32 were never checked.** The arXiv oracle was unreachable, which the protocol is
explicit must be read as *neither* "citations are fine" *nor* "fabricated". The cause is almost
certainly self-inflicted and is the founding receipt's HTTP-429 lesson at five times the
scale: this rig had just run a 5-lane research swarm — 160 tool calls, most of them arXiv —
and then asked the same IP to resolve 32 identifiers. **Lesson for the next dispatch: leave a
cooldown between the research lanes and the citation gate, or route the oracle differently.**

**What did clear.** The four DOI citations went through Crossref rather than arXiv and all four
resolved:

| id | source | outcome |
|---|---|---|
| **c27** Paravina 2015 | ΔE thresholds, DOI:10.1111/jerd.12149 | **ACCEPT — existence resolved, claim supported** (mistral-small:24b, pass, conf 0.90) |
| c26 Abasi 2020 | HyAB above 10 units, DOI:10.1002/col.22451 | resolved, title exact; claim lives in the body not the abstract → RETRIEVE FULL TEXT |
| c14 Soudarissanane 2011 | 60° incidence, DOI:10.1016/j.isprsjprs.2011.01.005 | resolved, title exact; no abstract available to ground against |
| c25 FLIP 2020 | DOI:10.1145/3406183 | **metadata_mismatch** — Crossref titles it `FLIP`, I cited "FLIP: A Difference Evaluator for Alternating Images". Cosmetic; corrected in place above and eligible for the protocol's correct-once re-verify |

**Consequence, enforced.** Exactly one finding — **26**, the ΔE threshold figures — is verified
and may be load-bearing. **All 28 others remain non-load-bearing** and are removed from any
architectural connection until a re-run resolves them. They are *not* dropped: the protocol
drops only FABRICATED, and nothing was fabricated. This is the CANNOT_CONFIRM class, surfaced
rather than silently kept.

**Contrastive frame for the Director:** you may reasonably have expected the swarm's findings
to be usable after the gate ran. They are not, and the reason is a rate-limited oracle rather
than bad citations — so the correct response is to re-run the gate after a cooldown, not to
discard the research. The one thing this does **not** block is
[E08's Gate 0 ruling](../experiments/E08-ruling-gate0.md), which was deliberately written to
stand on our own measurements and source reading with no citation load-bearing in it.
