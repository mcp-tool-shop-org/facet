# E35 research grounding — the dark-speck class, five levers

**Study swarm, 2026-08-14, at the Director's word** (*"Let's start with a Sonnet study
swarm focusing on the best 5 levers, 1 agent per lever"*). Five parallel research agents,
one per lever, each under the studio's sourcing standard: named papers with authors,
years, identifiers, one-sentence findings, and named absences where the exact question is
unstudied. Findings are reproduced verbatim below the synthesis; the design implications
are folded into [E35-clean-twins-kickoff.md](../experiments/E35-clean-twins-kickoff.md).

## The synthesis — what the five agree on

1. **The mechanism is the register prior under an over-denoised, near-flat init.**
   SDEdit's own low-information-guide case predicts the regime *by construction*
   (Meng et al. 2021); outline-first/details-later theory (Wang & Vastola 2023;
   Jiralerspong et al. 2025) predicts fine texture commits late and is
   strength-sensitive over a **narrow band** — a knee, not a ramp. ~~The InstantX control
   checkpoint's own documented img2img band is **0.10–0.50**; our 0.92 is 2–9× above it.~~
   **⚑ CORRECTED 2026-08-14: the cited card carries NO img2img denoise band** — finding 8
   falsified at source (three independent fetches across two seats; correction block in
   agent 1's section below). The knee prediction stands on the theory clauses alone.
2. **Conditioning strength hardens what the sampler invents; it does not create it.**
   `conditioning_scale` was never ablated in the ControlNet paper (named absence); the
   Union card's canny examples run at 0.5; the evidenced refinement is **per-step
   scheduling** (full strength early where silhouette locks, released late where texture
   forms) over a flat cut.
3. **Quantization is exonerated by signature.** PTQ failure in diffusion/DiT is global
   or channel/timestep-structured — *no surveyed source names discrete chromatic dots at
   any bit-width*, including two in-the-wild reports on this exact model family. The
   bf16 swap is a necessary-condition discriminator only; the **VAE's precision** is the
   cheaper narrower check; **attention sinks** (Wu & Summa 2026) are the named
   alternative whose signature actually matches seed-fixed small-footprint defects.
4. **Cross-seed median fusion is the principled suppressor — with a measured
   precondition.** Median at K=3–5 is L1-optimal against uncorrelated invention
   (Noise2Noise); production burst practice gates fusion on a per-pixel disagreement
   map (HDR+); naive averaging blurs where seeds disagree structurally (Diffusion
   Mental Averages) — so cross-seed **structural agreement is measured before fusion is
   trusted**, and verifier-gated selection (FK steering) is the upgrade path once a
   speck scorer exists — which the despeckler's detector is.
5. **The despeckler has a canonical shape**: an area-opening detector (one px²
   threshold, byte-identical outside touched footprints — Vincent 1993) cross-checked
   by size-capped LoG (Lindeberg 1998); **classification-gated correction** (switching
   median tradition — census first, touch only flagged pixels); neighborhood fill
   ≤~9 px², exemplar patch-fill above (Criminisi 2004); LaMa verified Apache-2.0 but
   unearned at speckle scale; gates = masked-complement LPIPS ≈ 0 by construction plus
   a no-reference edge-width leak check; refuse bounds keyed to the **figure's** pixel
   count, never the frame — the repo's own global-constant law applied.

---

## Agent 1 — img2img denoising strength and hallucinated high-frequency content

1. SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations — Meng, He, Song, Song, Wu, Zhu, Ermon (ICLR 2021) — arXiv:2108.01073 — On LSUN bedroom/church the realism(KID)/faithfulness(L2) curve has a usable sweet spot at t0∈[0.3,0.6], with guide-deviation bounded ∝σ²(t0) (Prop. 1); critically, for a low-information guide (their own example: an all-white-pixel image) the paper states faithfulness must be sacrificed for realism by choosing a LARGE t0 — the closest published precedent for a near-uniform init.
2. Diffusion Models Generate Images Like Painters: An Analytical Theory of Outline First, Details Later — Wang & Vastola (2023) — arXiv:2303.02490 — Closed-form reverse-ODE analysis: high-variance/large-scale structure commits early in the trajectory, low-variance fine detail commits last, and early noise dominates final content far more than late noise.
3. Shaping Inductive Bias in Diffusion Models through Frequency-Based Noise Control — Jiralerspong, Earnshaw, Hartford, Bengio, Scimeca (2025, ICLR workshop) — arXiv:2502.10236 — Low frequency (color, coarse layout) is set by the initial latent; high frequency is generated last in the trajectory and is comparatively unconstrained by conditioning.
4. Understanding Hallucinations in Diffusion Models through Mode Interpolation — Aithal, Maini, Lipton, Kolter (NeurIPS 2024) — arXiv:2406.09358 — Hallucinated content shows elevated sample-trajectory variance concentrated in the final sampling steps — an independent diagnostic separate from tuning strength.
5. Why DDIM Hallucinates More Than DDPM: A Theoretical Analysis of Reverse Dynamics — Ashiq et al. (ICML 2026) — arXiv:2605.06831 — Deterministic ODE-style samplers can get stuck near mode boundaries past a critical time and hallucinate more than stochastic samplers at matched noise budget; added stochasticity reduces it. Euler/simple (this pipeline) is deterministic.
6. Towards Understanding Text Hallucination of Diffusion Models via Local Generation Bias — Lu, Wang, Lyu, Jiang, Huang, Wang (ICLR 2025) — arXiv:2503.03595 — Denoising networks over-rely on locally-correlated regions when target dimensions are weakly coupled, producing locally-plausible but globally-ungrounded detail.
7. Plug-and-Play Diffusion Features for Text-Driven Image-to-Image Translation — Tumanyan, Geyer, Bagon, Dekel (CVPR 2023) — arXiv:2211.12572 — Spatial features/self-attention injected from early (high-noise) steps carry structure while later steps determine appearance/texture — structure/texture splits by trajectory position, not by one global strength number (measured on a UNet, not MMDiT).
8. Practitioner source, not peer-reviewed: InstantX Qwen-Image-ControlNet-Union model card — https://huggingface.co/InstantX/Qwen-Image-ControlNet-Union — vendor's own recommended img2img denoise range for canny conditioning is ~0.10–0.50; the pipeline's 0.92 sits 2–9x above the checkpoint's own tested range.

   ⚑ **FINDING 8 IS FALSIFIED AT ITS CITED SOURCE (2026-08-14).** The comfy-preflight
   build seat ran Amendment 2's verified-live discipline against this exact URL — two
   independent fetches (rendered page + `raw/main/README.md`), a public search, and the
   sibling Inpainting card — and a third fetch at the facet ruling seat agrees: **the card
   documents `controlnet_conditioning_scale ∈ [0.8, 1.0]` (explicit, all four control
   types), `true_cfg_scale=4.0` and `num_inference_steps=30` as snippet examples, and NO
   img2img denoise or strength range at all.** The 0.10–0.50 figure and the 2–9× framing
   are **withdrawn**; the correction is folded through every consuming surface (the E35
   spec, the status row, comfy-preflight Amendment 2) and relayed to the live E35 seat.
   What survives untouched: findings 1–7, the measured attribution in facet's record, and
   the sweep design — which hunts the knee on theory grounds alone. One NEW vendor fact
   from the same verification: the cn recommendation is **[0.8, 1.0]**, which makes E35
   arm 2c (0.65) a deliberately below-recommendation arm, and puts the recorded 0.9
   INSIDE the vendor band.

Named absence: no paper studies strength thresholds for MMDiT/rectified-flow backbones on flat/low-variance inits. Rectified-flow strength-editing papers (FlowSlider, arXiv:2604.02088; Optimal Transport for Rectified Flow Image Editing, arXiv:2508.02363) show the naive strength knob is non-monotonic and entangled with edit direction in flow models — worse-behaved than DDPM-SDEdit — but give no quantitative curve and never examine flat inits. Treat any [0.3,0.6]-type band as a hypothesis to test on Qwen-Image, not a transferable constant.

Design implications: the flat-guide case predicts the observed regime by construction · findings 2+3 predict a knee — add points between 0.80–0.92 (0.85, 0.88) to locate where speckle breaks vs glides · canny acts on structure (early steps) and is not expected to suppress late-trajectory invention · a stochastic/ancestral sampler at matched strength is a cheap orthogonal arm if low denoise costs register · ~~the vendor's 0.10–0.50 band puts even 0.72 on the high side — don't expect zero invention at 0.72~~ ⚑ withdrawn with finding 8 (correction above); no vendor denoise anchor exists.

## Agent 2 — ControlNet conditioning strength and interior hardening

1. Adding Conditional Control to Text-to-Image Diffusion Models — Zhang, Rao & Agrawala (ICCV 2023) — arXiv:2302.05543 — The source paper has no scalar conditioning_scale ablation at all; its only strength mechanism is CFG Resolution Weighting. The knob this pipeline tunes is a later diffusers-library addition never swept in the original paper — a named absence.
2. Analyzing and Improving the Training Dynamics of Diffusion Models — Karras et al. (CVPR 2024) — arXiv:2312.02696 — Regions where the guided signal changes little accumulate redundant low-frequency correction across steps under strong guidance, producing oversaturation/oversharpening; formalized further in Rethinking Oversaturation in Classifier-Free Guidance via Low Frequency (2026) — arXiv:2506.21452. Flat canny-unconstrained interior is exactly where compounding strength hardens repeatable structure fastest.
3. ControlNet++: Improving Conditional Controls with Efficient Consistency Feedback — Li et al. (ECCV 2024) — arXiv:2404.07987 — Baseline ControlNet has measurable condition-adherence slack even at nominal full strength; some invented content at 0.9 is inherent architecture noise — reducing scale changes the magnitude of hallucination, not the phenomenon.
4. On the Controllability-Fidelity Frontier in Diffusion Editing — Hu, Yi, Davis & Carter (2026) — arXiv:2606.09901 — Spatially-adaptive constraints (tight near control-carrying regions, loose elsewhere) beat a single global weight.
5. T2I-Adapter — Mou et al. (2023) — arXiv:2302.08453 — and IP-Adapter — Ye et al. (2023) — arXiv:2308.06721 — Working precedent that strength-by-location (network depth or timestep) is a real, implementable lever, not just a uniform scalar.
6. ControlNet v1.1 / diffusers control_guidance_start/end (2023) — Documented per-step strength scheduling: full conditioning early where structure locks, released later where fine texture forms — ships as an engineering knob with anecdote behind it, no quantitative strength-vs-artifact ablation found.
7. InstantX/Shakker-Labs — FLUX.1-dev-Controlnet-Union model card (Hugging Face) — Documented canny examples run at 0.5, multi-control per-mode scales as low as 0.2–0.4; the union architecture is expected to underperform single-task ControlNets at matched strength — its own authors implicitly treat ~0.9 as high.

Design implications: no source studied "canny strength vs interior speckle hardening" — the A/B is the first data point on that curve for this pipeline · 0.6–0.7 sits inside the range the Union documentation treats as normal (canny at 0.5), with IoU headroom (0.85–0.95 vs the 0.80 gate) but no quantified curve · prefer scheduling over a flat cut (~0.9 first half of steps, 0.5–0.6 after) if the graph exposes it · measure per view: silhouette IoU plus interior speck density and its cross-seed spatial reproducibility (true hardening implies near-fixed placement at fixed seed) · if specks persist at reduced strength, that favors architecture slack — the fix belongs downstream in the despeckler.

## Agent 3 — fp8/low-bit quantization artifact signatures

1. Q-Diffusion — Li, Liu, Lian, Yang, Dong, Kang, Zhang, Keutzer (2023) — arXiv:2302.04304 — Failure modes at aggressive bit-widths are global texture/structure collapse and FID blowup, not localized point defects.
2. ViDiT-Q — Zhao et al. (2024) — arXiv:2406.02540 — Naive PTQ on DiT backbones degrades to "blurred and unreadable" (whole-image collapse), traced to sensitive layers and timesteps, not any fixed spatial region.
3. PTQ4DiT — Wu, Wang, Shang, Shah, Yan (NeurIPS 2024) — arXiv:2405.16005 — DiT quantization error concentrates in salient channels and timestep-shifting activation distributions — the error's natural axes are channel and time, not image xy-position.
4. SVDQuant — Li et al. (2024) — arXiv:2411.05007 — At W4A4, uncorrected activation-outlier channels drive global quality loss; the failure is channel-structured, not spatially localized.
5. DMQ — Lee et al. (ICCV 2025) — arXiv:2507.12933 — Diffusion PTQ error originates disproportionately in early timesteps and compounds through the trajectory, clustering in specific channels — a time/channel signature, not a pixel one.
6. FP8 vs INT8 characterization — Kuzmin, Van Baalen, Ren, Nagel, Peters, Whatmough (MLSys 2024) — arXiv:2309.14592 — FP8 E4M3-family is more outlier-robust than INT8; the documented INT8 failure mode is detail attenuation, not added chromatic spots. E4M3: range ±448, 3 mantissa bits — coarse but bounded, smoothly-varying rounding, not a mechanism for isolated saturated dots.
7. In-production fp8 bug, same model family — vllm-project/vllm-omni Issue #2728 (2026) — catastrophic fp8 LPIPS regression across Z-Image-Turbo, FLUX.1-dev, and Qwen-Image; the failure signature is whole-image, not dots.
8. Community low-bit report, exact model family — QuantStack/Qwen-Image-Edit-2509-GGUF, HF Discussion #6 — GGUF Q2–Q4 produces ghosting/input duplication traced to two transformer blocks; at Q8/fp8, output is described clean — the one in-the-wild report on this model puts fp8 in the clean bucket and names structured duplication, not chromatic speckle, as the low-bit signature.

Design implications: the literature and both in-the-wild reports converge — PTQ/fp8 failure is global or channel/timestep/block-concentrated, never a scatter of small fixed-position chromatic dots; the consult's ranking is confirmed · the bf16 swap is a necessary-condition test of a two-stage fp8 path (backbone + text encoder — a positive needs staged ablation to localize) · named alternative worth ruling out first: Attention Sinks in Diffusion Transformers — Wu & Summa (2026) — arXiv:2605.09313 — conditioning-dependent positions receiving disproportionate attention mass match a fixed-seed, fixed-position, small-footprint defect better than any quant signature · check the VAE's precision first — production practice keeps VAE decode in bf16/fp16 because VAE-side numeric error is visually disproportionate · if the swap cleanly removes only the dots, that outcome is novel relative to this literature — log it as new evidence, don't treat it as confirming an expected mechanism.

## Agent 4 — multi-seed ensembling / sample fusion

1. EDSR self-ensemble — Lim, Son, Kim, Nah, Lee (CVPRW 2017) — arXiv:1707.02921 — Averaging 8 geometrically-transformed passes improved SR; self-ensembling helps when the task reconstructs one shared target, not free generation.
2. Diffusion Mental Averages — Thawatdamrongkit, Seripanitkarn, Suwajanakorn (2026) — arXiv:2603.29239 — Naive pixel-space averaging of multiple diffusion samples produces blur; sharp fusion needs trajectory alignment, not post-hoc pixel combination.
3. Noise2Noise — Lehtinen et al. (ICML 2018) — arXiv:1803.04189 — Given K independent noisy observations of one clean signal, pointwise mean is L2-optimal and pointwise median is L1-optimal — the basis for cross-seed median converging on shared register content if speckle is independent per seed.
4. Burst photography (HDR+) — Hasinoff et al. (ACM TOG 2016) — DOI:10.1145/2980179.2980254 — Production burst merge computes a spatially-varying robustness weight per tile that downweights frames disagreeing with a reference — fusion gated on disagreement, not uniform.
5. ControlNet — Zhang, Rao, Agrawala (ICCV 2023) — arXiv:2302.05543 — Strong spatial conditioning locks structure while leaving fine texture free to vary — the mechanism that should make structure agree and only speckle disagree across seeds.
6. ControlNet++ — Li et al. (ECCV 2024) — arXiv:2404.07987 — Measured pixel-level adherence is imperfect even under ControlNet, so cross-seed structural disagreement is a real nonzero rate — check it, don't assume it.
7. TEXTure — Richardson et al. (SIGGRAPH 2023) — arXiv:2302.01721 — and SyncMVD — Liu, Xie, Liu, Wong (SIGGRAPH Asia 2023/24) — arXiv:2311.12891 — Neither fuses finished per-view pixels; both route disagreement before pixels exist (trimap zoning; per-step latent sync).
8. FK steering — Singhal et al. (2025) — arXiv:2501.06848 — When a verifier signal exists, particle resampling toward it beats naive best-of-N and blind fusion — verifier-gated selection is the field's preferred multi-sample strategy once a scorer exists.

Design implications: K=3–5 → per-pixel MEDIAN, not mean (rejects one outlier seed; mean needs ~10+ frames with sigma-clip) · compute a per-pixel disagreement map (MAD/stddev across the stack) as a first-class output and gate high-disagreement regions out of auto-fusion · the failure mode to gate on is structural disagreement (fold line, prop edge, material boundary) — that is what turns median fusion into ghosting · measure cross-seed structural agreement on this canny+Qwen setup directly (K seeds, one view, IoU/edge-distance between seeds) before trusting fusion · once the despeckler's detector exists as a scorer, FK-style verifier-gated selection is the documented upgrade path.

## Agent 5 — the despeckler design space

1. Grayscale area openings and closings — L. Vincent (1993), EURASIP Workshop on Mathematical Morphology — An area opening/closing removes every connected component below an area threshold λ (px²) while leaving everything above it byte-identical outside its own footprint; one integer parameter bounds blob size instead of a fixed-radius kernel.
2. Adaptive median filters — H. Hwang, R. Haddad (1995), IEEE TIP 4(4) — Detectors flag a pixel as corrupted only when it falls outside the local min/max of an adaptively grown window; only flagged pixels are ever replaced — correction gated on classification.
3. Switching median filter with boundary discriminative noise detection — P.-E. Ng, K.-K. Ma (2006), IEEE TIP 15(6) — A two-stage classifier sorts each window into clean/corrupted groups via data-adaptive boundaries before any pixel is touched — the closest precedent to a census-then-repair two-phase tool.
4. The Laplacian Pyramid — P. Burt, E. Adelson (1983), IEEE Trans. Comm. 31(4) — Formalizes band-splitting via Gaussian low-pass + subtraction; the split is only valid where the low-pass support exceeds the feature being isolated — an undersized kernel aliases a defect straight into the untouched low band.
5. Exemplar-based inpainting — A. Criminisi, P. Pérez, K. Toyama (2004), IEEE TIP 13(9) — Patch priority combines confidence with an isophote term so the fill front advances along edges first, propagating structure instead of blurring.
6. LaMa — R. Suvorov et al. (WACV 2022) — arXiv:2109.07161 — Licence verified by reading the repo's LICENSE directly: Apache-2.0, commercially usable — but built and evaluated for large structural holes, not 2–6 px speckle.
7. Feature detection with automatic scale selection — T. Lindeberg (1998), IJCV 30(2) — Scale-normalized LoG extrema over a bounded scale range locate a blob and report its diameter in one pass; capping σ to ~1–3 px turns LoG into a size-selective dark-spot detector with size measurement built in.
8. LPIPS — R. Zhang et al. (CVPR 2018) — arXiv:1801.03924 — A calibrated deep-feature distance tracks human judgment of texture change far better than PSNR/SSIM; restricted to the untouched-mask complement it becomes a paired gate a blob-local corrector cannot game.

Design implications: detector = area-opening on a dark-chromatic-deviation map (ΔE from a locally-fit register estimate) cross-checked against σ-capped LoG, reporting count, per-blob px², bbox and largest component, keyed to one px² threshold, never a percentage of frame · corrector = neighborhood/boundary-median fill for ≤~9 px² blobs, Criminisi-style patch fill near the top of the range; LaMa reserved and unearned at this scale · refuse conditions bound total corrected area as a fraction of the FIGURE's own pixels plus a separate per-blob maximum — the global-constant law applied · gate 1: LPIPS on the untouched-mask complement, near zero by construction unless the corrector leaks · gate 2: a no-reference edge-width/local-variance ratio over the same region (Marziliano et al. 2002), catching feather a masked LPIPS could miss.
