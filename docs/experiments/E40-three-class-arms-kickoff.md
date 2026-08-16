# E40 — the three-class arms: three seats, run simultaneously

**Status: DISPATCHED.** Opened 2026-08-16 by the advisor at the Director's word — *"we'll run
experiments on the classes simultaneously through 3 spawned Sonnet sessions, once we've learned
more of the levers involved."* The levers are in:
[E39's three-class study-swarm](../research/E39-three-class-study-swarm.md), 32 findings, every
citation resolved at primary source or listed UNRESOLVED.

Three seats — **A (gold) · B (green) · C (blade)** — run in parallel. Each is a full executor
seat under [CLAUDE.md](../../CLAUDE.md)'s rules. This document is the shared spec; each seat's
section is its own.

---

## What is already settled — no seat re-derives any of this

From [E39](E39-w3-polish-kickoff.md), measured, not assumed:

- **The gold class is `reference`-carried** — 91.05% at an enrichment of **0.99×**, dead on base
  rate. The dilation flood does not carry it.
- **Both gold mechanisms are live, roughly 2:1** — twins disagree **≥ 29.9%** (a firm lower
  bound); a twin hallucinated internally **≤ 70.1%** (a ceiling on the complement, **not** a
  measurement of it).
- **The green class is different** — `brush` **5.49×**, `dilation` **3.34×**.
- **The blade is the one `dilation`-dominant large region**, at a **48.3% plurality**.
- **`dilation` is 26.95% of the written atlas and 4.95% of rendered figure pixels — 0.18×.**
  Quote provenance shares in the space you mean.
- **W3 CANNOT BE RE-BAKED.** No `prep_uv.glb` / `mask.npy` / `pos.npy` / `meta.json` survives —
  verified three times. ⚠ **CORRECTED 2026-08-16 by [E40](E40-three-class-arms-kickoff.md) Seat B, and the correction is the advisor's to own: those four files DO survive**, at `E:\AI\training\facet_E06\C1\prep\` — `mask.npy`, `meta.json`, `nor.npy`, `pos.npy`, `prep_uv.glb`, verified at the advisor's own seat. **The three prior "verifications" searched `facet_E08` only; the prep lives in `facet_E06`. Three searches of the wrong tree is one scope error repeated, not three verifications** — the exact family this record has lost nine arcs to. What is true is narrower and the original claim conflated two stages: regenerating W3's **state** would need new diffusion generation, which is gone; **`finalize` is a deterministic post-process over frozen state and replays byte-identically** — `tests/test_t50_w3_finalize_replay.py` does exactly that pairing (`facet_E08/ARMB/state` + `facet_E06/C1/prep`) and passed live. **So every fill-stage arm runs on W3's own real assets rather than a substitute subject.** W3's **mesh, 26 cameras, 8 aligned twins and `prov_class` maps DO
  survive**, so W3 remains available for *measurement* and unavailable for *re-baking*.
- **The eight twins register to their own export renders at shift (0,0)** under two independent
  objectives. No reprojection or resampling is needed to compare a twin to a render.

## Rules binding all three seats

1. **Task 0 is always ENUMERATION, and it is not optional.** This repo's most-repeated failure is
   commissioning a thing that already exists — `e12_offsurface.py`'s nine flags, a model already
   on the rig, `--edge-absolute` already at `project_twins.py:103`, open3d's cp313 wheel already
   installed. **Before building any arm, list what already exists that could answer it.** One
   `grep` separates a commission from a flag that exists.
2. **Never judge whether output is good.** Measurements and sheets. The Director's eye decides.
   The words *verified, shipped, works, decisive, validated, proven* do not belong in a report.
3. **Predict before you look**, in writing, and disclose whether blind. **Compute what your
   instrument reads when the thing is definitely true and definitely false, and predict inside
   that interval** — E39's seat predicted 75% for a rate whose ceiling was 63.66%.
4. **Stop at every gate. Never improvise past one.**
5. **A negative result is a full success.**
6. **Write `handoff.md` early** in your own output directory and keep it current. Transcripts have
   been lost mid-arc three times, once to a client crash this very session.
7. **Everything from the swarm is a HYPOTHESIS to verify locally, never a fact to adopt.**

## ⚑ Reserved to the advisor — do not touch, all three seats

- **The count surfaces.** T34 pins stated counts against `pytest --collect-only` *of the tree the
  surfaces sit in*, so **three parallel seats adding tests cannot all be green independently** —
  the record already has a two-seat instance. Add your tests; **do not update README.md,
  SHIP_GATE.md, site-config.ts, the handbook, the translated READMEs, or `docs/advisor-kickoff.md`**.
  Report your test count and the advisor reconciles after all three land.
- `docs/experiments/README.md`'s status table · `conventions.json`'s arc span · the index DB/cert
  pair · `docs/instrument-census.json`.
- **Do not `git add -A` and do not commit over a shared index.** Report; the advisor commits by
  pathspec.
- **Accepted assets and manifest-protected trees.** Check a tree's manifest before writing to it,
  and re-verify at close.

## Environment

```
python   E:\AI-Models\trellis2-env\Scripts\python.exe      <- ABSOLUTE, always
blender  "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"   -b -P only, via PowerShell
```
Scripts create their own output dirs. ASCII in tool output. `argparse` eats leading minus signs
(`--views=-30,0,30`). **All three seats are LOCAL and cost ZERO cloud spend** — no generation is
in scope for any of them. ⚠ **The VRAM watchdog was dead at session open**; if any step touches
the GPU, confirm it is alive first.

---

# SEAT A — GOLD: close the bound, then blend by frequency

**The class:** gold across the green tunic, skirt and boot tops. `reference`-carried at base rate.

## A-Task 0 — enumerate

What already exists that projects, blends or re-projects? Include `project_twins.py`'s full flag
surface, `texpass_finalize.py`'s modes, `e11_export_turnaround.py`, and every subject tree under
`E:\AI\training\` carrying **both** a complete prep state *and* multiple twins. Report which are
manifest-protected. **Name what you found before proposing anything new.**

## A-Task 1 — the per-face view vote. Cheap, decisive, and it runs on W3 itself

**This closes E39 Task 2's open side and needs no re-bake.** Task 2 could poll **one** view per
pixel — the view being rendered — which is exactly why (b) came back as a ceiling. The
[MVS-Texturing](https://github.com/nmoehrle/mvs-texturing) method polls **every view that sees the
face**: per face, collect each view's mean projected colour, fit a multivariate Gaussian to the
inliers, score each view by Mahalanobis distance. Their constants: `gauss_rejection_threshold`
6e-3, `minimal_covariance` 5e-4, 10 iterations, `minimal_num_inliers` 4. **BSD 3-Clause — read
the LICENSE yourself before adopting anything from it.**

Everything needed survives for W3: `mesh.glb`, 26 `cam.json`, 8 aligned twins, open3d
`RaycastingScene`. **`prep_uv.glb` is NOT required** — it maps a hit to an atlas texel id, and
this needs a *surface point*.

**The question:** at gold-out-of-place surface points, **is gold the minority or the majority of
the views that can see it?**

- **Minority → mechanism (a)**, the views disagree and the blend resolved it badly.
- **Majority → mechanism (b)**, and MVS-Texturing's own stated assumption — *"the majority see
  the correct color"* — is the thing that has failed here.

**Predict first**, with the floor/ceiling discipline of rule 3. Report the full distribution of
"how many of the N views that see this point call it gold", not just a split.

## A-Task 2 — frequency-split blending, the swarm's best-aimed lever

**Three shipping tools converge on it and two make it the default** — AliceVision
`multiBandNbContrib={1,5,10,0}` over `nbBand=4`; Metashape **`Mosaic`**; RealityCapture
**`Multi-band`**. Gold-on-a-tunic is a **low-frequency** error, and that is the band where these
tools take **5–10 view contributions**, so one hallucinating view is outvoted *in the band where
its error lives* while high-frequency detail still comes from the single best view.

**Arms — one variable each, and the first three are mutually-exclusive blend philosophies:**

| arm | what changes |
|---|---|
| **A0** | current facing-weight blend, full band (the baseline) |
| **A1** | **frequency-split**: decompose into 4 bands, contributions `{1,5,10,0}` |
| **A2** | **hard selection**: facing weight raised toward single-view-per-texel (StableGen's `Weight Exponent`, up to 1000, *"Voronoi-like hard segmentation"*) |
| **A3** | **outlier damping**: A0 plus the A-Task-1 Gaussian, damping factor 0.2 |

⚠ **A1 and A2 pull in opposite directions.** Do not combine them; do not report a combined arm as
a lever. **A3 composes with either.**

**Gate A:** any blend change must be checked for *admitting background* at the reference's painted
boundary — compare newly-admitted texels against the source's own background colour. This repo's
standard widening check.

**Out of scope:** any generation, any ControlNet or model change, SyncMVD and its family
(measured to target only mechanism (a), and its tracker carries no character-mesh report at all).

---

# SEAT B — GREEN: the flood predicate, and a mode that may already exist

**The class:** cloth green on the sword grip and other non-cloth surfaces. `brush` **5.49×**,
`dilation` **3.34×**.

## B-Task 0 — enumerate, and answer one question before anything else

⚑ **Which mode did W3's finalize actually run — the default atlas flood, or `--surface-aware`?**
`texpass_finalize.py` has carried `--surface-aware` since commit `17a9e57` (2026-08-03); W3's
atlas was written **2026-08-04**. An E08 ruling says the surface-aware replacement was *"never
built"*, which **contradicts a flag that existed the day before**. The record is ambiguous and
the advisor will not assert either way.

**This changes what the class is.** `--surface-aware` sources every hole texel from its nearest
painted texel **in 3D** and was measured at a median **0.00253** against the flood's **0.177** — a
70× shrink. **If W3 ran the default flood, the fix may already be a flag we own and never
switched on.** Enumerate before commissioning: that is the law, and it has caught four
commissions in this repo already.

## B-Task 1 — the predicate

`texpass_finalize.py:155` is `fill = ~grown & (cnt > 0)` — **no island constraint**. The record
already falsified adding `& valid` (*"still leaves 53.3% cross-island and strands 174,898 texels
on the mean fallback"*). **`valid` is not `same island`**, and same-island has never been tested.

**Arms:**

| arm | predicate |
|---|---|
| **G0** | current flood (baseline) |
| **G1** | **`--surface-aware`**, if B-Task 0 shows W3-class runs never used it |
| **G2** | **same-island constraint** — the flood may only take colour from the source texel's own island |
| **G3** | **Blender's topology walk**, bounded at 3 polygon steps, mirroring across the real UV seam |

**G3's reference implementation is `texture_margin.cc`** — face index per texel, `grow_dijkstra`
carrying direction back to the owning face, loop adjacency to the neighbour face's UV edge.
Verbatim: *"Looking further than 3 polygons away leads to so much cumulative rounding that it
isn't worth it. So hard-code it to 3."* **No path in it averages an unrelated 2D neighbour.**

⚠ **Two things the swarm found that bound G3.** Blender already **runs this at bake time** in our
pipeline (`bake_hero_prep.py:452`, margin=8, `ADJACENT_FACES`) — so G3 is *moving a technique to
the fill stage*, not importing a new one. And it has an open failure mode of its own: Blender
#119393 (**OPEN**, *"dialates pixels inside uv island"*), #62429 (**OPEN**), and PR #162226
(**OPEN**) listing ~16 defects.

**Every arm MUST report the mean-fallback count.** That is what killed the `& valid` patch —
174,898 stranded texels, 238× the baseline — and a predicate that strands surface is worse than
one that bleeds. **Report total and largest-connected-component**, per this repo's two-threshold
rule.

**Gate B:** the widening check — newly-admitted texels against the source's background colour.
Plus: **do not gate on the direction your invariant already forecloses.** If your predicate
bounds cross-island writes by construction, the live risk is stranding, so gate stranding.

**Out of scope:** the brush stage itself (its 5.49× enrichment is real and is a *separate* arc);
any change to the packer; any re-bake of W3.

---

# SEAT C — BLADE: thin geometry, and why it is not the others

**The class:** a steel blade wearing gold and rust. The **only** `dilation`-dominant large region,
at a **48.3% plurality**, on a figure that is otherwise ~90% projection-carried.

## C-Task 0 — enumerate, then test the mechanism cheaply

**The swarm's mechanism hypothesis, which is the blade agent's synthesis and not a quote:** a thin
blade is **grazing in nearly every view**, so its cosine visibility weight is near zero
everywhere — which is why it falls through to dilation while the torso does not. FlexPainter
(Yan et al. 2025, [arXiv:2506.02620](https://arxiv.org/abs/2506.02620)) names cosine weighting as
unable to *"dynamically adjust"*; Im2SurfTex (Georgiou et al. 2025,
[arXiv:2502.14006](https://arxiv.org/abs/2502.14006)) names backprojection artifacts at rapid
depth change. **Both were confirmed at arXiv for title/authors/year by the advisor; the specific
sentences live in the paper bodies.**

**The cheap test: measure the blade's per-view cosine visibility weight across all 8 twin
cameras, and compare it against the torso's.** If it is near-zero everywhere, the mechanism is
confirmed by measurement rather than by citation. **This runs on W3 with mesh + cameras only.**

⚑ **And upstream concedes the thin case in its own source, which the advisor found and no agent
surfaced.** `texture_margin.cc`'s fallback comment, verbatim: *"not strictly correct, but the
visual difference seems very minimal. **This also catches pixels we missed because of very narrow
polygons.**"* **Blender's topology-aware margin degrades to plain extend on thin geometry.** So
Seat B's G3 will not fix the blade even if it works, and this seat's arms are genuinely separate.

## C-Task 1 — the arms

| arm | lever | provenance |
|---|---|---|
| **C1** | **separate texture set for the sword** — its own atlas, own texel density | the trade's default; 80.lv, *"the high texel density forces you to split the model into independent sets by material ID"*, 120–170 px/cm |
| **C2** | **xatlas `ChartOptions::normalSeamWeight` > 1000** — *"normal seams are fully respected"*, forcing a thin plate's two faces into separate charts | **we already use xatlas**; a flag, not a build |
| **C3** | **per-island dilation cap** as a fraction of that island's own width | this repo's own law — *a global constant must not govern a local feature* — which has now cost three sessions |
| **C4** | **backface exclusion at projection** — reject a texel whose view ray entered through a back face | Substance ships `_ignorebf` per-mesh; Blender #66438, *"go through to the other side"*; #74553, *"Cycles fails to detect when it's hit a back face"* |

**C1 is the one that eliminates rather than gates**, which this repo prefers: a separate atlas
removes the blade from the figure-wide flood **by construction**.

**Gate C:** report, **per structure**, how much of its own area each operation removes. A fixed
erosion once annihilated 100% / 100% / 77.6% of the three thinnest strata. **This is a required
diagnostic and it must not be used as a halt** — it is a perimeter-to-area statistic that swings
±10 points on shape alone.

**Out of scope:** any mesh edit; any change to the reconstructor; the hollow-shell question.

---

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | every arm names one variable and its baseline; subjects are named trees; the swarm's parameter values are quoted with their sources in E39's grounding doc |
| ANDON_AUTHORITY | 3 | Gate A (background admission), Gate B (stranding, aimed deliberately at the direction the invariant does **not** foreclose), Gate C (per-structure area loss, explicitly a diagnostic and explicitly **not** a halt) — all stated before any arm runs |
| NAMED_COMPENSATORS | 2 | no irreversible action in scope: no publish, no push, no external write, no generation spend. Tool edits are additive modes behind flags with defaults unchanged, so an unqualified command reproduces its baseline byte-for-byte — the compensator is reverting the commit, and the advisor holds the index |
| DECOMPOSE_BY_SECRETS | 3 | the three-way split **is** E39's measured finding — three classes, three carriers, three seats — and the shared surfaces that would couple them (count surfaces, status table, span, census) are reserved to the advisor by name |
| UNCERTAINTY_GATED_HUMANS | 2 | each seat halts to the advisor at its Task-0 enumeration and at every gate; the Director sees artifacts, not arms |
| EXTERNAL_VERIFIER | 2 | three seats are different sessions from the advisor that wrote this spec, and each is told the advisor's own hypotheses are candidates to kill — E39 Task 1 killed the advisor's mechanism call on exactly this instruction |

## Amendments

*(appended in place, with dates and reasons)*

### Amendment 1 — the seats were spawned, after the advisor first shelved them (2026-08-16)

**All three seats run as dispatched Sonnet agents, spawned by the advisor**, steered on an open
line, halting to it at Task 0.

They did not start that way, and the reason is worth recording. The advisor wrote this spec and
then delivered **three paste blocks** instead of starting the seats, on a reading of the
Director's *"3 spawned Sonnet sessions"* as three sessions **he** would open. He asked why they
were not already running.

**The standard he ratified this same day answers it**, and the advisor had already followed it
five times in this session — two E39 executor seats and five research agents, all spawned
directly. [CLAUDE.md](../../CLAUDE.md)'s dispatched-seat section says it outright: *"Under this
standard the advisor starts the seat itself, which serves that purpose more directly. The rule
still binds for anything only the Director can begin."* Nothing here was his to begin.

**So this is advisor rule 5's own failure — the shelf — one level up.** That rule exists because
*"a spec sitting in `docs/experiments/` that nobody can start is a shelf, not a deliverable"*, and
a paste block is the remedy **only when the advisor cannot start the thing itself**. Producing
three specs and handing the Director the work of launching them is the same defect the rule was
written against, wearing the rule's own clothes. **The law needed no change; it needed
following.**

*Recorded rather than quietly fixed, because the next advisor inheriting a session where paste
blocks look like the deliverable should see that they usually are not.*
