# Advisor kickoff

Paste into a fresh advisor session. **Written 2026-08-16 by the outgoing advisor** — the seat
that opened E38, the material route, and ran it from dispatch to the Director's redirect.

**Read the calibration section before you trust a ruling in this document.** This seat was
wrong about a mechanism **seven times in one session**. Dispatched executor seats caught five
of them, a measurement killed one, one came back PARTIAL. What held was structure. That ratio
is the argument *for* the working system below, not against it — but it is also why you should
treat this seat's mechanism claims as candidates and its process rules as earned.

---

> # ⚑ E38 IS RUNNING. THE ROUTE QUESTION IS ANSWERED; THE POLISH QUESTION IS OPEN.
>
> **The Director's live direction, 2026-08-16, in his words:** *"let's not over focus on the
> black artifacts. W3 is far from perfect and needs a serious polish."* And on how to proceed:
> ***"do a study-swarm instead of guessing."***
>
> He is right and this seat had over-indexed. The atlas-coverage class E38 solved measures
> **0.578% of W3's figure pixels and renders zero black** there. What is actually wrong with W3
> is **blotchiness across every material** — gold on the tunic, skirt, boots and blade; green on
> the sword grip and pauldron edges; brown-green smears on hands and bracers. **Walk
> `E:\AI\training\facet_E08\ARMB\out\renders_flat\final_0.png` at full size before you do
> anything.** It is unmistakable and no metric in this repo was pointing at it.
>
> **The mechanism is already in this record and was treated as a footnote for a whole arc:**
> atlas adjacency is not surface adjacency, and **74.9% of dilation-filled texels take colour
> from a different island**, median 18% of the figure's height away across the surface
> (E07 Gate 0). W3 is 27% dilation by provenance and our most fragmented asset at ~10
> faces/island.

## You are the advisor

```
cd E:\AI\facet && git pull
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py build  --db <scratch>
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py verify --db <scratch>
                                     <- the E15 ritual: 19/19 or stop. SCRATCH --db.
CLAUDE.md                            <- the law book. READ THE DISPATCHED-SEAT SECTION.
README.md                            <- the front door
docs/experiments/E38-material-route-kickoff.md   <- the live arc's spec
docs/known-defects.md                <- "Atlas texels that are never painted" is E38's
docs/experiments/E37-ruling.md       <- the prior arc's law
```

Two mounted servers: `mcp__facet-record__*`, `mcp__facet-measure__*`. `record_health` first.
Watchdog: heartbeat ADVANCING on two reads.

## THE WORKING SYSTEM — the Director asked explicitly that this be carried forward

**1. You spawn your own executors and steer them on an open line.** Codified in CLAUDE.md
("How an experiment is actually run"). The Director is out of the loop by default. Corrections
land inside the same arc instead of at a session boundary. Its costs are in that section:
on-disk state early · the dispatch IS the spec · an executor never delegates its own
measurement · `git status` before every fold.

**2. Research swarms are standard, not exceptional.** Also in CLAUDE.md. Four parallel agents
against the practitioner literature found, in ~20 minutes, a **merged upstream Blender fix**
for 58% of a defect three arcs had hunted in the wrong subsystem. Do it early.

**3. Resolve every external citation at its primary source.** `projects.blender.org` 403s to a
plain fetch and answers at `/api/v1/`. The gap between a search snippet and the issue body was
the gap between "matches our config" and "a different defect in the same setting."

**4. Everything from outside is a hypothesis to verify locally** — consults, forums, papers,
and this document.

**5. Hand executors your candidates labelled as candidates, and tell them to kill yours as hard
as their own.** They will. That is the whole value.

## THE LIVE STATE — measured at the close

| | |
|---|---|
| HEAD | re-measure at your open — `git log --oneline -1`; it moves inside a session |
| working tree | check `git status` **before every fold**; seats work uncommitted in a tree you also write to |
| suite | **THE SUITE: 1072 tests, 1027 hermetic.** **RE-COUNT before quoting** — `pytest --collect-only -q` and the same with `-m "not artifacts"`, currently 1072 total / 1027 hermetic. T34 pins every surface off the collector, and every one of them changes in the *same* commit |
| the record | the index rebuilds and verifies **19/19** over 40 experiments. No staleness findings at the declaration leg |
| highest T | **T74** (landed) |
| accepted assets | five — W3, galleon, dragon, longsword, the E34 performer (reopened) |
| protected trees | manifests **HELD byte-identical before and after** the catalogue survey |

## WHAT E38 ESTABLISHED — do not re-derive any of this

**The material route works.** A procedural material authored directly in UV space removed
**two** E37 classes *by construction*: the four-woods cross-view incoherence, and the projection
seam (confirmed an owner boundary at **zero-pixel** separation).

**The dark-mark class was never in the generator.** It survived total replacement of the
colouring process with **69.2% of marks within 3px** of a diffusion-build mark. The bisect split
it: **Population A** (57.94%, UV outside any triangle's footprint, **100.00%** reading exact
`(0,0,0)`, null **0.00%**) and **Population B** (42.06%, atlas clean at its own texel,
boundary-distance **1.414** against a **2.828** null). **Both confirmed by intervention** via a
magenta atlas refill, not by inference.

**Population A is Blender's own bug, fixed upstream.**
[PR #161752](https://projects.blender.org/blender/blender/pulls/161752), **merged**: *"if a
triangle does not overlap texel center, it will be empty."* Our 5.2.0 LTS build (2026-07-14)
predates it.

| arm (4096 unless noted) | Pop A | Pop B |
|---|---|---|
| A0 stock 5.2 | 766 | 556 |
| A1 `margin_method='ADD'` | 65 | 323 |
| A4 `--res 8192` | 56 | — |
| A1+A7 (`margin_type='EXTEND'`) | 31 | — |
| A1+A7+A6' (bake `margin` 16) | **4** | 279 |
| **A11 — Blender 5.3 alpha, STOCK settings** | **0** | **165** |
| A11 + all three levers | 0 | **257** — worse |

**The finding, and nobody picks a winner:** on 5.2 today the three levers are right; on 5.3
**change nothing** — they were compensating for a Blender bug and turn net-negative once it is
gone. **5.2 remains the route.** 5.3 alpha is an instrument only, at
`E:\AI-Models\blender-5.3.0-alpha\...\blender.exe`.

**Population B is INDEPENDENT**, closed by intervention: the magenta refill moved 100% of B at
A0 and **0.0%** at A11, median ΔE exactly 0.0. Not a halo of A.

**⚠ B is very likely the same root as what is wrecking W3** — cross-island bleed, one site over:
B is a render-time *read*; E07's 74.9% is a bake-time *write*. **Nobody has confirmed they are
one class at two sites. Cheap, live, high-value.**

**Back-catalogue survey** (all four accepted assets, read-only, manifests held): pooled
figure-pixel outside-valid rate — longsword **0.808%** > W3 **0.578%** > dragon **0.065%** >
galleon **0.000000%**. Whether it renders black does **not** generalise: W3 **0%** all views,
dragon 3.71–7.25%, longsword **39.70–51.40%**. The galleon's zero is *unseen*, not absent —
23,260 black background texels these eight cameras never sample. **W3 cannot be re-baked: no
`prep_uv.glb`/`mask.npy`/`pos.npy`/`meta.json` survives.** Verified twice.

## IN FLIGHT AT THE CLOSE — check these before planning anything

1. **A10** (xatlas `padding`, on A11, judged on Population B) — sheets landed `02:00`,
   `phase2-report.md` updated `02:04`. **UNRULED.** Read it first.
2. **A study-swarm, four agents. TWO LANDED BEFORE THE CLOSE AND THEY CONVERGE — read this.**
   Two more (UV-atlas fill / cross-island bleed, and material segmentation / low-contrast
   masking) were still out; **look for them before assuming they did not land.**

   **The convergent finding, from two independent agents:** the blotchiness is **upstream of
   the blend and post-hoc blending cannot fix it**. Classical multi-view texturing assumes N
   *photographs of one physically consistent object* disagreeing only **photometrically**. Our
   twins are independently diffusion-sampled and disagree about **material identity** — gold vs
   cloth — which is a different kind of disagreement, and multi-band/graph-cut remedies were
   built for the first kind. The literature's answer is to **synchronise views during denoising**
   so they cannot diverge, rather than to blend better afterwards (SyncMVD
   [arXiv:2311.12891](https://arxiv.org/abs/2311.12891), MVPaint, TexPainter; survey: *Advances
   in Neural 3D Mesh Texturing*, CGF/Eurographics STAR 2026, [arXiv:2606.00137](https://arxiv.org/abs/2606.00137)).

   **⚖ SyncMVD is MIT, and I verified the LICENSE file myself** — *"MIT License, Copyright (c)
   2023 LIU-Yuxin"*, fetched directly, not inferred from the paper. It is the named originator
   of synchronised multi-view diffusion and the one method that is simultaneously the fix for
   our exact symptom **and** commercially clean. MVPaint is the stronger successor and is
   licence-blocked. Also verified permissive: Paint3D (Apache 2.0), FlashTex (Apache 2.0),
   Material Anything (MIT), TRELLIS/TRELLIS.2 (MIT — already ours). Verified excluded: Text2Tex
   (CC BY-NC-SA), Hunyuan3D-Paint (regionally void). Everything else in that brief is
   **UNVERIFIED** and must not be adopted on an assumed licence.

   **And two standard passes this route simply does not have** (Waechter et al. ECCV 2014;
   Lempitsky & Ivanov CVPR 2007): a **global colour harmonisation** across the atlas, then a
   **local gradient-domain correction confined to the seams**. Our dilation fill is neither. The
   literature also selects **one source view per face by graph cut** rather than blending by
   facing weight — explicitly to avoid the ghosting that averaging two misregistered "correct"
   views produces. Both are testable arms against the blotchiness.

   **The third brief landed too, and it gives the concrete fix for our OWN route** — worth
   having whether or not the generation side ever changes. TEXTure and Text2Tex already maintain
   a per-texel **keep / refine / generate** trimap over the atlas, which is architecturally the
   same object as this repo's graded mask. **Adding a material-ID channel to it — so a texel can
   only ever be filled from same-material neighbours — is a precedented extension, not an
   invention**, and it attacks cross-island bleed at its definition rather than its symptoms.
   The material IDs are obtainable from the views we already render: segment each rendered view
   (SAM2, **Apache-2.0, LICENSE fetched directly**) and fuse the labels onto the atlas beside the
   colour, the standard multi-view fusion pattern (Kundu et al., ECCV 2020). Also licence-verified
   there: SAMPart3D **MIT**, Point-SAM **MIT**, BiRefNet **MIT**, MODNet **Apache-2.0** *(that one
   corrects a secondary source that claimed CC-BY-NC-SA — read the LICENSE, not the summary)*;
   PartField is **NVIDIA non-commercial**, CGAL's shape-diameter segmentation is **GPL**.
   And it independently confirms this repo's own law: TEXTure and Text2Tex **never matte their
   painted views** — the mask comes from depth rendered from the known mesh at the known camera.

   **⚑ ALL FOUR LANDED. The fourth one's closing question is the single most actionable thing in
   the swarm, and it is nearly free to answer.** *"Does the pipeline's dilation have any
   per-island mask at all, or is it a global flood across the whole packed atlas? If the latter,
   the fix may be much closer to turning on a mode that already exists than to implementing
   geodesic fill."* **Our own known-defects page already answers it:** `texpass_finalize.py`'s
   predicate is `fill = ~grown & (cnt > 0)` **with no island constraint** — *"`valid` decides when
   to stop, never where to write."* ⚠ **CORRECTED 2026-08-16, at the primary source, by the seat
   that inherited this paragraph and repeated it.** This line said *"Adobe's own docs describe our
   exact defect as the documented behaviour of unconstrained padding: it 'stretch[es] a pixel until
   it reaches another UV island.'"* **That reads the sentence backwards.** Fetched and read directly,
   the sentence sits under *"Infinite padding generation"* and describes the island as a **wall that
   halts the stretch**, not as a source colour is pulled from — Substance's dilation is
   island-bounded **by construction**, which is the opposite of our defect rather than a description
   of it. **The correction strengthens the case it was cited for**: the mature tools stop at island
   boundaries and we do not. And the toggle is real and now named in three tools — Substance
   `UV Padding: 2D/UV Space Neighbor` vs `3D Space Neighbor`, Blender `Margin Type: EXTEND` vs
   `ADJACENT_FACES`, Mari `Bleed Patch Edges`.

   **And here is the precise gap nobody has closed.** The record already tested adding `& valid`
   and found it insufficient — *"still leaves 53.3% cross-island and strands 174,898 texels on the
   mean fallback."* But **`valid` is not `same island`**. A texel can be valid and belong to a
   different chart. **Nobody has ever tested constraining the flood to the source texel's OWN
   island.** That is a different predicate from the one the record falsified, it is the one every
   DCC tool ships, and it is a small local change to a tool we own. Start there before anything
   architectural. (The literature's more radical answer, worth knowing: Purnomo et al. SGP 2004
   build atlases *seamless by construction*, and would flag 28,000 islands at ~10 faces as the
   real problem before touching the fill at all.)

## THE QUEUE

1. **W3's polish** — the Director's live direction, informed by the swarm. Not specced.
2. **The E38 ruling and fold** — the arc has a spec and a status row, no ruling.
3. **Commit the executor's `bake_hero_prep.py` + T74** behind its anchor.
4. Translations sweep (seven READMEs, stale tool count, further drifted this session).
5. Tree-manifest guard spec · the resurrected `--bg-max-pct 2.0` default · E34 candidate
   anchors · six errands.

## The Director's open decisions — surface, never re-decide

1. **What a "serious polish" of W3 means at his eye.** He named blotchiness; the fix depends on
   the swarm.
2. **The back-catalogue re-bake** — greenlit *conditionally on the fix eliminating the class*.
   It does. But W3 cannot be re-baked at all, and the longsword is the only asset carrying
   visible black. Bring him numbers, not a plan.
3. The E34 formal disposition · the pure-black dot routing · hosted-tier revalidation.

## This seat's record — read before trusting its rulings

**Seven wrong mechanism calls in one session:** the parked-face hypothesis · an invented
1.0-texel² threshold · a bake margin read from the API instead of the call site that overrides
it · the `--reunwrap` arm, built on a `grep` line that truncated mid-sentence · an island-count
comparison between two different mesh states · a B-independence criterion whose radius tested
bilinear when mipmapping was the live mechanism · and **the framing error the Director had to
correct: chasing a countable class instead of looking at the asset.**

Five were caught by dispatched executors. **They are one shape** — asserting a located default,
a partial reading, or a convenient proxy as a measured fact. What held: the route decision, the
bisect design, the ordering that put cheap measurements before expensive ones, the gates, and
every fold pushed.

**Deciding is the job. Predicting is not.** This session is the strongest evidence for that line
the repo has produced.

## Environment

```
python    E:\AI-Models\trellis2-env\Scripts\python.exe      <- ABSOLUTE, always
blender   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"   -b -P only
blender   E:\AI-Models\blender-5.3.0-alpha\...\blender.exe  <- INSTRUMENT ONLY, not the route
assets    E:\AI\training\facet_E0*\  facet_E3*\
```

Blender through PowerShell. Scripts create their own output dirs. ASCII in tool output.
`argparse` eats leading minus signs. Generation is cloud-only; all of E38 was local and free.

## Do not

End a session the Director has not ended · present a surface you have not walked at native size
at your own seat · `git add -A`, or commit over a shared index (`git status` first, every
time) · let an executor delegate its own measurement to a child · quote an external claim before
resolving it at its primary source · **treat a countable proxy as the question when the
Director's eye is the question** · run the suite or the mount on bare python · leave CI red ·
touch closed rulings, accepted assets or protected trees except to cite · split the DB/cert
pair · re-derive anything under "WHAT E38 ESTABLISHED".
