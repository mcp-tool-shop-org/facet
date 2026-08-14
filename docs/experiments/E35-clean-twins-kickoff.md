# E35 — clean twins: the dark-speck class, and the control surface it buys

**Seat:** advisor · **Dispatched:** 2026-08-14 · **Priority:** ⚑ TOP — the Director ruled
the dark-speck class unacceptable at his zoom ([known-defects.md](../known-defects.md),
final entry) and set the arc's mandate in his own words: a comprehensive fix, study-swarm
grounded, **the despeckler completely built out — "to the point where this stops being
just a fix and also gives more control over the process."** This arc is that: facet gains
a speck-census instrument, a gated correction stage, and a seed-fusion stage — all
tested — and the performer gets repainted clean.
**Research grounding:** [docs/research/E35-speck-research-grounding.md](../research/E35-speck-research-grounding.md)
— five levers, five agents, named papers and named absences. The spec's arms are built
from it; read it before running anything.
**Halts at:** `E35-clean-twins-report.md` · **Predictions:** `E35-predictions.md`,
registered blind after task 0/1 land and **before any cloud job runs**.

---

## The question

The performer's texture carries generator-painted dark specks — texture truth, in every
twin, invented (the controls are speck-free), surviving re-projection because every twin
carries them. **Can the route produce clean paint — by starving the mechanism at
generation, by cancelling it across seeds, and by a gated despeckle stage — and can
facet measure and control all three, with the repainted performer passing the Director's
eye?**

## What the record establishes (measured, not assumed)

- Attribution ([known-defects](../known-defects.md) final entry; evidence at
  `E:\AI\training\facet_E35\diag\`): specks persist under flat light (texture truth);
  twins carry them (dark at 5 of 6 sampled locations; 127/263 near-black px in sampled
  crops); clay/canny controls carry **0**; the class predates E34 and survives it.
- Atlas census (`diag\atlas_census_notes.md`, operand caveat recorded there): final-atlas
  core-black 1,495 texels / 52 components / largest 377 — **61% on twin-painted texels,
  39% fill-propagated**; wide-dark 18,492 — 79%/21%. The fill *extends* twin dots into
  holes, so **the despeckler's home is the twins, before projection** — clean paint
  starves both classes.
- The recipe under test (E33 §7, byte-pinned): seed 770700 · steps 20 · cfg 2.5 ·
  denoise 0.92 · cn_strength 0.9 · shift 3.1 · euler/simple · 352×1024 · LoRA NONE ·
  the four named models. ~~Grounding headline: the control checkpoint's own documented
  denoise band is **0.10–0.50** — 0.92 is 2–9× above it.~~ **⚑ CORRECTED 2026-08-14:
  the card carries NO denoise band** — the grounding's finding 8 was falsified at its
  source by the comfy-preflight build seat's verified-live check (three independent
  fetches across two seats). The denoise sweep stands on the theory knee (SDEdit
  flat-guide; outline-first/details-later) and this record's own measurements. New
  vendor fact from the same verification: the card recommends
  `controlnet_conditioning_scale ∈ [0.8, 1.0]` — so the recorded 0.9 is IN the vendor
  band and arm 2c (0.65) is a deliberately below-recommendation arm. Run it as specced,
  framed as such.
- Cost: **≈ $0.018/job** measured (E34 Ruling 5). **Ceiling this arc: 45 cloud jobs**
  (≈ $0.85), zero partner-API nodes.

## Premises — measured or assumed (mark the outcome in the report)

| # | premise | status |
|---|---|---|
| 1 | The rejected artifacts for detector validation exist: the eight E34 twins (`facet_E34\twins\`), the six E33 candidates (`facet_E33\twins\`), the clay renders (clean controls) | **MEASURED** (manifested trees; read-only) |
| 2 | The cloud graph's ControlNet node exposes per-step strength scheduling (a `control_guidance_start/end` analog) | **ASSUMED — task 0c verifies via `get_node` on the payload's node types; if absent, arm 2c is a flat cut to 0.65** |
| 3 | The graph's VAE runs unquantized (bf16/fp16) — `qwen_image_vae.safetensors` precision | **ASSUMED — task 0b reads the payload/catalog; if the VAE is quantized, a VAE-precision arm outranks the backbone bf16 swap (grounding, agent 3)** |
| 4 | A stochastic/ancestral sampler is available on the graph's sampler node as a drop-in (the deterministic-euler hallucination lever) | **ASSUMED — task 0c enumerates the sampler node's options; arm 2e is conditional on it** |
| 5 | `scipy`/`numpy`/`PIL` suffice for the detector (area-opening via `ndimage`, LoG via `gaussian_laplace`) on the pinned interpreter — no new dependency | **MEASURED (all three import; T18's surface)** |
| 6 | The parked-face patch's location is derivable from `bake_hero_prep.py` source | **ASSUMED — task 0a; its outcome closes the E34-era pure-black question either way** |
| 7 | facet_E33 (117), facet_E34 (84) manifests verify 0/0/0; the eight protected subtrees verify 7,312 / 0/0/0 | **MEASURED at E34 close; re-verify at open and close** |

## Rulings embedded in this dispatch

**R-a. The detector is the arc's metric, and it validates against rejected artifacts
before any A/B is read.** This repo's law: a metric that cannot separate an asset the
Director rejected from one he accepted is not a metric. The detector must FIRE on the
rejected twins (planted-fixture tests prove exact counts; an artifacts-tier leg proves
it fires on the real rejected twins) and stay quiet on the clay controls. **No A/B
result is quoted until the detector's validation legs are green.**

**R-b. The fusion operator is per-pixel median at K=3 with a first-class disagreement
map, and its adoption is gated on measured cross-seed structural agreement** (grounding,
agent 4: median is L1-optimal against uncorrelated invention; naive fusion blurs where
seeds disagree structurally). Structural agreement is measured from task 2a's stack
(inter-seed silhouette IoU + edge-distance) before any fused twin is trusted.

**R-c. The bf16 swap is conditional, not default.** It runs only if task 2a says the
dots **stay** across seeds (grounding, agent 3: quantization is exonerated by signature;
a stay-outcome opens the quant/attention-sink path and the swap becomes the decisive
test). If it runs, it is a named-model change, called out as such, ≤ 2 jobs.

**R-d. The register is the Director's ruling and is re-gated at his eye.** No recipe
change proceeds to the repaint until he has seen the winning configuration's twins on a
sheet beside the recorded R3 twins. His wood-grain note remains a note.

**R-e. Artifact homes.** Everything this arc writes lands under
`E:\AI\training\facet_E35\` (plus repo tools/tests/docs). `facet_E33\`, `facet_E34\` and
the eight protected subtrees are read-only, manifest-gated at open and close. The
repaint candidate lands as a NEW artifact beside the two recorded ones.

**R-f. Tool shape.** Two tools, decomposed by what changes together:
`tools/twin_despeckle.py` (modes: `census` — read-only report; `clean` — gated write
with sidecar report; the detector is one code path used by both) and
`tools/twin_fuse.py` (median-of-K + disagreement map + agreement metrics). Both are
route-grade: ANDONs `raise`, ASCII prints, create their own output dirs, tests ride
their commits (**T66+**), and each writes a JSON sidecar recording its full parameter
set and per-image census — the control surface the mandate asks for.

## The arc, task by task

**Task 0 — mechanics, zero cloud.** E15 ritual (scratch db, 19/19 or stop); watchdog
heartbeat advancing; interpreter pre-check; manifests (premise 7). Then:
(a) the parked-face patch — locate in `bake_hero_prep.py`, sample its final-atlas
color, settle whether any visible face samples it (the E34 pure-black remainder);
(b) the VAE precision on the cloud graph (premise 3);
(c) the graph's capability surface — scheduling knob, sampler options (premises 2/4) —
via `get_node` on the payload's node types, recorded verbatim in the report.

**Task 1 — the detector, and its validation (local; tests in the same commit).**
`twin_despeckle.py --mode census`: dark-chromatic deviation map (ΔE from a locally-fit
register estimate — reuse the fitted-background family's ring-fit pattern for the
backdrop, a local median field for the figure), area-opening detection keyed to **one
px² threshold** (default spanning the measured 2–6 px class at frame scale),
σ-capped LoG cross-check, census output: count, per-blob px², bboxes, largest
component, corrected-area-as-figure-fraction — JSON + overlay PNG. Tests (T66):
planted synthetic fixtures with exact expected censuses; can-fail legs; `-O` survival;
**the R-a validation legs** — fires on the rejected twins (artifacts tier), quiet on
clay. Then run the census on all 14 recorded twins + the E34 flat renders: **the
baseline table every A/B is judged against.**

**Task 2 — the mechanism A/Bs, one view (view 1), census-judged.** Register
`E35-predictions.md` blind first (each clause its own line; write what one counted
thing IS before the number). Then, cheapest first:
- **2a — seed re-roll ×3** (new seeds, recorded) at the pinned recipe → detector census
  per seed + cross-seed spatial reproducibility of speck placement + inter-seed
  structural agreement (R-b's precondition). **The discriminator: dots move vs stay.**
- **2b — denoise sweep 0.85 / 0.80 / 0.72** (grounding, agent 1: the knee is predicted
  between 0.80–0.92; the 0.92 baseline exists; add 0.88 only if 0.85 ≈ 0.92) → census +
  a register-drift note per rung (full-size look by the executor; the Director's eye
  rules at Gate R).
- **2c — conditioning 0.65** (or the scheduled form if task 0c found the knob) at the
  best 2b rung → census + reg-IoU per the twin-sheet diagnostics.
- **2d — fusion prototype, zero cloud**: `twin_fuse.py` median-of-3 over 2a's stack →
  census on the fused twin + the disagreement map (structural-disagreement gate per
  R-b). Tests ride the commit (T67).
- **2e — conditional arms**: bf16 swap (R-c, only on a 2a stay-outcome, ≤2 jobs);
  stochastic sampler at matched strength (premise 4, only if the denoise knee costs
  register — grounding, agent 1 implication 4).
Budget: 2a=3 · 2b=3–4 · 2c=1–2 · 2e≤4 → **≤ 13 jobs before Gate R.**

**Gate R — the register, at the Director's eye.** The winning configuration's view-1
twin (and its fused variant if 2d survives its gate) on one sheet beside the recorded
R3 twins, full size, with the census numbers beside each panel. **He rules register-hold
and picks the repaint configuration; a halt here is his re-rule, not a failure.**

**Task 3 — the corrector (local; tests in the same commit).** `--mode clean`:
classification-gated correction — neighborhood/boundary-median fill for blobs ≤ ~9 px²,
Criminisi-style patch fill above (grounding, agent 5) — **byte-identical outside flagged
footprints** (the Vincent property, pinned by a test), sidecar report of exactly which
pixels changed, refuse ANDONs: total corrected area > a bounded fraction of the
FIGURE's pixels (not the frame), or any single blob above a per-blob ceiling. Quality
gates as tests: masked-complement LPIPS ≈ 0 by construction is approximated
license-cleanly (report SSIM/variance-ratio on the untouched complement — LPIPS's
torch weight is not earned here; name this deviation in the report) plus the
edge-width leak check. Run on the Gate-R winner's residual census; target: census 0
with gates green.

**Task 4 — the repaint.** Eight views at the Director-picked configuration (×K seeds
per view if fusion won Gate R) → `twin_fuse` (if adopted) → `twin_despeckle --mode
clean` per view (census before/after per view in the report) → the E34 projection
pipeline exactly (eight-view `project_twins` at the recorded invocation, explicit
values with provenance, `--bg-max-pct 100.0` per E34 R-a, `--reg-iou-min 0.80`
untouched/halt-on-fire) → finalize (recorded gates) → pack →
`facet_E35\out\performer_textured_clean.glb`. Evidence: the E34 before/after sheet
form re-rendered through one identical call — E33 | E34 | E35 three-row this time —
plus per-view flat-light census (the acceptance-shaped diagnostic: near-zero specks),
`texel_provenance` with largest-component, poles regression. Budget: ≤ 24 jobs
(8 views × K≤3). **Total arc ceiling stands at 45.**

**Task 5 — close.** Manifests re-run; count surfaces reconciled off `T34.PINS` +
collector at the tree (tools and tests land this arc, so they WILL move — two-pass
order: pin edits first, collect second, surfaces last; census regenerated after all
documents are final); report; pathspec commits; push only with the guard tests green.
**No judgment words.** The Director's eye rules the candidate; anchors for it are
commissioned at the ruling on acceptance, as E34's were.

## Hypotheses (advisor's, qualitative; the executor's blind bands govern scoring)

- **H1**: the dots MOVE across seeds (grounding: content class, agents 1–3). *Falsifier:*
  fixed placement → the quant/attention-sink path opens and R-c fires.
- **H2**: the census falls steeply somewhere in 0.72–0.92 (the knee) while the register
  survives to Gate R at the knee. *Falsifier:* register dies before the specks do →
  generation-side fix is insufficient alone; the corrector carries the load.
- **H3**: median-of-3 cuts the census below the best single seed with the disagreement
  map confined to speck scale. *Falsifier:* structural disagreement (ghosting) → fusion
  rejected, selection-not-fusion noted as the upgrade path.
- **H4**: the corrector reaches census-0 on the winner's residual with byte-identity
  outside flagged footprints and both leak gates green. *Falsifier:* a fired refuse
  ANDON — halt, report, never widen a bound.
- **H5**: the repainted candidate carries per-view flat-light census ≈ 0 and holds the
  register at the Director's zoom. *Falsifier:* his eye.

## Out of scope

The brush stage and its R3 configuration (parked) · the armature re-survey relay (held
until this arc's candidate exists, at the Director's word) · hosted-tier revalidation
(his pricing) · E30's W3 era-flags re-run (unspent) · `anchor_check`/PIL, the identity
envelope's dependency set, archive-to-`D:` (queued) · LaMa or any learned inpainting
(ruled unearned at speckle scale; revisit only on a task-3 failure with the licence
already verified Apache-2.0) · edits to `facet_E33\`/`facet_E34\` or any accepted
asset · attention-sink instrumentation (named alternative, only reachable through a 2a
stay-outcome, and even then it enters through a fresh consult, not this arc).

## Compensators — no skip

| irreversible action | compensator | post-rollback state | owner |
|---|---|---|---|
| ≤ 45 cloud jobs, GPU-hours | **none exists** — bounded before spend: task budgets above, per-arm gates, predictions before the first job | spend stands; rejected outputs stay recorded, unstaged | executor |
| writes under `facet_E35\` | `rm -r E:\AI\training\facet_E35` (diag\ is re-derivable from the recorded trees + scripts) | tree as at open | executor |
| repo commits (local) | `git reset --hard <open-sha>`; pathspec-scoped only | tree at open | executor |
| push | `git revert` by commit | origin restored additively | advisor |
| `facet_E33\`, `facet_E34\`, eight subtrees | prevention: read-only, manifest gates at open + close, halt on delta | n/a | executor |

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | every local stage pinned (tools + flags + sidecar JSONs recording full parameter sets); cloud jobs pinned by payload + job id + hashes; limit: server-side weights, as always on this venue |
| ANDON_AUTHORITY | 3 | the detector/corrector ship with refuse ANDONs that `raise`; every task carries halt conditions; Gate R is a hard stop at the Director's eye |
| NAMED_COMPENSATORS | 3 | table above; the compensator-less cloud spend is bounded per task before the first submission |
| DECOMPOSE_BY_SECRETS | 3 | detector/corrector/fusion decomposed into two tools by change-cadence; subject values explicit (unprofiled, premise-13 form); the census JSON is the stable interface between stages |
| UNCERTAINTY_GATED_HUMANS | 3 | the frame was the Director's own redirect; Gate R gates the register at his eye mid-arc; acceptance is his at close |
| EXTERNAL_VERIFIER | 2 | the research grounding is five independent agents with named sources; the detector validates against Director-rejected artifacts rather than its author's fixtures alone; limit: no different model family grades the twins — his eye decides, by design |

## Count surfaces and namespace

Tests take **T66+**. Tools and tests land, so the count surfaces MOVE — reconcile off
`T34.PINS` read at apply time and `pytest --collect-only` at the combined tree, two-pass
(pin edits → collect → surfaces), census regenerated after every document is final, the
index pair in a terminal commit via `record_build`. **This dispatch's own commit bumps
`laws.paid_for_by` to `E3[0-5]`** — the E34 lesson, applied at birth this time.

---

> ## ⚖ AMENDMENT — GATE R2: the pale-blotch class, the discriminator before the fix (advisor, 2026-08-14)
>
> **What amended.** Task 4's candidate carries **pale blotching across the crown,
> forehead and cheek** at the Director's eye — a LIGHT defect class this arc's detector
> cannot see by construction (it counts dark-chromatic blobs; T66 asserts a brighter
> blob is not a speck). The per-view best-of-K selection mixed three seeds
> (987654 ×5, 770701 ×2, 770700 ×1) where E34's accepted set was uniform at 770700;
> the selected set's cross-view spread — **C\* 9.77, L\* 10.14** — was printed on the
> coherence sheet and passed as context. The executor surfaced its own miss, measured
> the mechanism candidates, proposed a remedy, and held without touching count
> surfaces — correct at every step after the miss. **Consult #3** (the Comfy channel,
> relayed by the Director) rules the seed hypothesis **real but second-order at
> denoise 0.92** — the seed pins where divergence starts, not how much — and names a
> competing **generation-side desaturation class** (the off-distribution InstantX
> union at cn 0.9 failing toward a pale mean exactly where smooth skin gives canny
> nothing to anchor; cfg 2.5 second) **which no seed choice can cure**. The chroma-heavy
> spread and the anatomical localization lean that way; the consult's numbers are
> testimony, not measurement, so the rebuild is **gated on a discriminator, not on a
> re-roll**. The Director's word: *rebuild with a more informed approach instead of
> flailing.*
>
> **Spend arithmetic, before anything fires.** 32 of 45 spent (8 pre-Gate-R + 24 at
> task 4). Remaining: **13**. This amendment budgets: task 7 ≤ 1 · task 8 worst case
> ≤ 11 (2 cn A/B + 1 cfg on the Director's word only + 8 rebuild) → **≤ 12 of 13**.
> Any overage is a halt, his word only.
>
> ### Task 6 — the discriminator (local, ZERO jobs; all inputs already exist)
>
> Interpretation maps pre-registered here so no reading is post-hoc. The executor
> reports each leg; **the advisor rules the mechanism from the report; task 8 does not
> launch until that ruling issues.** The advisor pre-registers **no** mechanism
> prediction — the discriminator's job is to make one unnecessary.
>
> - **6a — ownership overlay.** `texel_provenance` view-ownership boundaries on the
>   head region vs the pale regions at the Director's named locations. *Patchwork ⇒*
>   pale regions piecewise-uniform inside one view's owned region, edges stepping AT
>   seams. *Generation-side ⇒* lobes tracking anatomy, crossing seams unbroken.
> - **6b — seam-crossing (decisive where it exists).** A blotch spanning two ownership
>   regions: tone continuous across the seam ⇒ generation-side; a step at the seam ⇒
>   patchwork.
> - **6c — same view across seeds.** For the views owning blotch UVs, that view's twin
>   at 987654 / 770701 / 770700: blotch at the same anatomical location across seeds ⇒
>   generation-side, stable; moves or vanishes with seed ⇒ seed-driven tone.
> - **6d — chroma vs luminance at the blotch.** Chroma floor honoured, circular means
>   only. Desaturation signature (C\* collapse, L\* rise) ⇒ generation-side;
>   predominantly L\* patch shift at modest chroma ⇒ patchwork.
> - **6e — frequency profile.** Step edges with flat interiors ⇒ seams; smooth
>   low-frequency lobes ⇒ generation.
> - **6f — the spread metric earns or loses its voice.** Measure **E34's accepted
>   eight-view set** with the same instrument that produced 9.77/10.14. If the accepted
>   set's spread is not clearly lower than the rejected set's, the number does not
>   separate accepted from rejected and gates nothing (the E07 law, applied before a
>   threshold exists rather than after). Report both; invent no bound.
> - **6g — the twins at the blotch UVs, pre-projection, full size.** The class that is
>   invisible in every single twin and born at assembly is patchwork; the class carried
>   in a lone twin is generation-side. Sheet, not prose.
>
> ### Task 7 — consult calibration (archive-first; ≤ 1 job)
>
> The consult's checkable claim: same seed + same dims ⇒ same initial noise ⇒
> deterministic output on this Cloud path, IF noise is CPU-side; GPU-side noise breaks
> byte-identity across workers. Archive-first: if any two recorded submissions share
> byte-identical inputs and parameters, diff their outputs — **pixels, not PNG bytes**.
> Else submit ONE existing (view, seed) job a second time, identical payload, and diff.
> *Pre-registered reading:* pixel-identical, or a uniform residual at or under the
> E33-measured cross-hardware float floor (ΔE ≈ 0.84, uniform shape) ⇒ same-seed
> reasoning stands. Structured or localized differences ⇒ per-job platform entropy
> exists, and every same-seed claim in this amendment weakens accordingly — report,
> halt, re-rule.
>
> ### Task 8 — the fix, on the advisor's mechanism ruling; Gate R2 is the Director's eye
>
> Global-single-seed selection is the free baseline on EVERY path (it deletes the
> mixed-seed term by construction). **The seed is 987654** unless the ruling says
> otherwise — census-best (97/575 vs 770700's 202/1363) and per-view winner 5 of 8;
> the consult's confound is recorded: standardizing on E34's 770700 for its tonal luck
> would double the dark-speck load this arc exists to remove.
>
> - **Path P — patchwork dominant.** Global-987654 selection → per-view LAB
>   harmonization to a reference view BEFORE projection (local op, zero jobs;
>   reference = the Gate-R register-ruled view unless the ruling names another), with
>   a guard: named canon materials' chroma centres before/after per view, circular
>   means above the floor, shift bounded and reported → task-3 corrector to census-0 →
>   the E34 projection pipeline exactly as task 4 records it → pack → sheets. The
>   harmonized-vs-unharmonized head rides the SAME sheet so the Director's eye rules
>   the new op, not the advisor's assumption. **Zero cloud jobs.**
> - **Path G — generation-side dominant.** ONE-view A/B at the blotch-owning view,
>   seed 987654, all else pinned at the recorded recipe: **cn_strength 0.9 → 0.7 and
>   0.9 → 0.6** (2 jobs). Full-size sheet — blotch-region crops beside the current
>   twin, register comparison on the same sheet (silhouette + canon chroma). **Gate R2:
>   the Director picks or halts.** The cfg arm (2.5 → 2.0, 1 job) only on his word if
>   cn fails. Then the eight-view rebuild at the winning configuration (8 jobs),
>   selection global-single-seed, corrector, project, pack, sheets. ≤ 11 jobs.
> - **Path M — mixed.** G's lever first, then P's harmonization on the rebuilt set.
>   Same ceiling.
>
> Every path ends in the three-row sheet **plus the head at the Director's zoom beside
> E34's head** — the surface his eye caught both classes on, at the scale he caught
> them.
>
> ### Standing notes folded by this amendment
>
> The executor's earlier global-987654 proposal is Path P's first half — not wrong,
> and not dispatched alone: unswept by the discriminator it risks rebuilding the
> generation-side class straight back to his eye. · No pale-blotch detector is
> commissioned mid-arc — a metric born chasing the defect it grades is the E07 defect;
> the discriminator legs and his eye carry this arc, and the class enters
> `known-defects.md` at the close ruling. · Consult #3 is testimony under the citation
> law: its one checkable claim is exactly task 7; its catalog claims (colour-match
> node families) touch only the next-programme option; **Qwen-Image-Edit 2509 stays
> parked for the next programme** — a base swap re-opens the register ruling and does
> not enter mid-arc. · Task 5 (close) runs last, unchanged, count surfaces reconciled
> as written. · The compensator table stands: harmonization writes live under
> `facet_E35\` (existing row), task-7/8 jobs inside the ≤ 45 ceiling with the
> arithmetic above.

---

> ## ⚖ GATE R2 — THE MECHANISM RULING (advisor, 2026-08-14, on the tasks-6/7 halt report)
>
> **The mechanism is GENERATION-SIDE.** The pale class is carried in the twins before
> any projection — 6g puts it in every lone twin at every seed and my own eye has been
> on that sheet at 3x; 6c makes it seed-stable (87.7% co-location); 6e makes it smooth
> lobes, not step edges; 6b puts the seam steps AWAY from the blotches (9.16 outside vs
> 6.089 inside). No selection rule over these twins can remove what all of them carry.
>
> **6d is adjudicated against its own map, and the map is corrected.** The map's
> dichotomy — *desaturation ⇒ generation-side, L\*-shift-at-modest-chroma ⇒ patchwork* —
> was inherited from consult #3's prototypes, and the measurement falsified the
> prototype, not the mechanism: this stack's generation-side pale is an **L\*-rise wash
> at essentially preserved chroma** (+16.68 L\*, C\* −9.48%, 0 px below the floor), now
> measured. A leg reading the assembled composite under a wrong prototype does not
> outvote legs reading the defect at its birthplace. The corrected signature is
> recorded here for the next map.
>
> **6f: the spread metric is WITHDRAWN.** E34's accepted set carries a *higher* L\*
> spread (11.54) than the rejected set (10.14) — the number fails the E07 bar and gates
> nothing. **And the executor's self-charge is revised accordingly**: "I had the number
> and didn't halt" presumed the number was a valid halt signal; it was not, and could
> not have been known to be either way, because nobody had measured the accepted
> asset's spread until leg 6f built the comparison. The miss that stands is the
> unbuilt comparison, not the missed halt.
>
> **Task 7 is RATIFIED**: pixel-identity (ΔE 0.0000, 0 of 360,448) on a verbatim
> re-submission — this Cloud path is deterministic per payload; the consult's
> certain-half holds; E33's ΔE 0.84 anchor stays attributed to cross-hardware kernels.
> The PNG-bytes-differ half is this repo's own law, applied by the executor unprompted.
>
> **What my eye adds that the binary legs could not carry** (6g sheet, head at 3x):
> the pale class's INTENSITY is seed-graded — **987654 is the palest column across all
> four views; 770700 the darkest and most tonally even; 770701 between**. The
> dark-speck census and the pale wash anticorrelate across seeds — a lighter
> generation carries fewer dark-reading specks — so the per-view census selection was
> optimizing INTO the pale class, and the Director's "much stronger than E34's" has a
> mechanism: E34 was all-770700. Also for his eye at the next sheet: 770700's v2/v7
> twins carry hard graphic line features (brow/mouth/wink), 770701's v7 swooping
> painted lids — register observations, his to weigh.
>
> ### The path, re-routed by the evidence — the zero-job candidate first
>
> **R2-a (zero jobs, runs first):** quantify the eye's observation with the leg-6
> instrument — per-view, per-seed pale measure (area and L\*-rise) across the existing
> 24 twins **plus E34's 8 accepted twins as the baseline anchor**, and report whether
> the census-selected twin was also the pale-maximal twin per view. This replaces my
> assertion with a number and hands the Director the anticorrelation as a measurement.
> Blind bands per the executor's own ritual, registered before the run.
>
> **R2-b (zero jobs): the candidate.** Global-**770700** selection — the seed whose
> class we cannot fix post-hoc is mildest there, and the class we CAN fix is what the
> task-3 corrector exists for — → corrector to census-0 on those eight twins →
> reproject through the task-4 pipeline unchanged → pack → the three-row sheet PLUS
> the head at the Director's zoom beside E34's head. This candidate is E34's tonal
> behaviour with the dark-speck class corrected — the repair this arc set out to
> build, at zero further spend. It is tonal-behaviour-equivalent to E34's inputs, not
> byte-equivalent (task 7 found no parameter-identical pair across the eras; say so
> on the sheet).
>
> **The cn ladder (Path G's 0.7/0.6 A/B) stays AUTHORIZED and HELD.** It is the lever
> that could push the pale wash below even 770700's level, and it re-opens register
> risk; it fires only on the Director's word after his eye rules R2-b's sheet. Budget
> unchanged: 33 of 45 spent; the ladder + rebuild (≤ 10-11) remain inside the ceiling
> if he calls for them.
>
> **The global-987654 proposal is closed**: it would standardize on the palest seed —
> the measured selection defect, made global.
>
> ### The seat's own error record, in the same fold
>
> Commit `63cff76` carries the executor's staged halt artifacts — the tasks-6/7 report
> section and the blind-bands registration — under a comfy-preflight postscript
> message. **The advisor's construction did it**: status, add, commit and push chained
> in one call, so the status that showed the sibling's staged files printed but was
> never read before the commit fired. The kickoff's own ⚠ names this defect verbatim;
> this seat applied it to the sweep and broke it on its own commits, and the same
> shared-copy scoop appears twice more in today's record (`d888baf`, `2c072fa`) — the
> mechanism is now measured three ways in one day. Content unaltered; the blind-bands
> file's pushed SHA still serves its pre-registration; attribution corrected here.
> **From this fold: the advisor's status check, the read of it, and the commit are
> separate calls, always.**
