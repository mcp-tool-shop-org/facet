# E29 ruling — does a clay mesh reconstruct better than a concept mesh?

**Advisor, 2026-08-09.** Report: [E29-clay-reconstruction-report.md](E29-clay-reconstruction-report.md).
Predictions: [E29-predictions.md](E29-predictions.md), committed at `d07a975` before task 0
was attempted. Dispatch: [E29-clay-reconstruction-kickoff.md](E29-clay-reconstruction-kickoff.md).

**Re-measured at this seat before ruling**, because *measure before ruling* and because three
of this report's findings correct documents rather than add to them: E14 Ruling 3's stated
evidence base (read verbatim), E04's banner sentence (read verbatim at `E04-gate0-report.md:47`
and `:66`), the reconstructor's preprocessing (read at source in
`trellis2/pipelines/trellis2_image_to_3d.py`), `e14_topology.py:154`'s conditional, and
`.mcp.json`'s contents. **All five hold as reported.**

---

## Ruling 1 — THE ARC IS ACCEPTED. Gates 1–5 PASS; gate 6 is an honest absence.

Gates 1–5 pass on evidence quoted in the report. Gate 6 is written **`NOT YET RUN`** with no
run id — the fabricated-citation law honoured on its first outing at an executor seat, and
`ci` is paths-gated so a docs-only commit correctly draws no run. **That is the gate working,
not a gap.**

The manifest bracketed the session at **7,312 files / 17,072,807,610 bytes, 0/0/0**, in the
eight facet subtrees — the wording [E28 Ruling 22](E28-ruling.md) corrected, used correctly
here for the first time by an executor.

**The arm's result, stated without a quality word:** the clay mesh returns **9 shells against
82**, **1,461 non-manifold edges against 4,201**, and **3.66% more of the polygon budget
spent** — **73×, 152× and 13.7×** their measured noise floors. Neither mesh is fused to floor,
wall or block on any view.

## Ruling 2 — `ATTN_BACKEND=sdpa` is the fix. The recorded invocation string does NOT change.

One environment variable, **no `pip install`, no code edit, no pinned version moved** — so the
[E23 Ruling 2](E23-ruling.md) argument the dispatch demanded never had to be made, because
nothing was added to `trellis2-env`. 104 s / 3.4 GB sits inside the handbook's recorded
103–141 s / 3.4–5.6 GB band.

**`SPARSE_ATTN_BACKEND=sdpa` is measured inert on this route** and rides in every recorded
invocation in this repo. **It stays.** The executor kept both variables so the invocation
string remains identical to every recorded reconstruction, and that is the right call: this
arc measured inertness on **one route** (`1024_cascade` image-to-3D), and dropping a variable
from every recorded command on one route's evidence trades a citable constant for nothing.
What is now recorded is narrower and true — **the minimal sufficient set is one variable; the
recorded string stays two.**

## Ruling 3 — E04's banner inference is CORRECTED IN PLACE, and E12 carried it forward

[E04's Gate 0 report](E04-gate0-report.md) concluded **"What ran is what the log says, not what
was requested"** from a single `[SPARSE] … Attention backend: flash_attn` line, and annotated
its own invocation `(see §1 — flash_attn is what loaded)`. E12 carried it as P21.

**Measured here: that banner printed on all six runs of this session — in a process where
`flash_attn` is not installed, cannot be imported, and which ran to completion.** A second
banner, `[ATTENTION] Using backend: sdpa`, tracks the dense path and E04 did not quote it.

The line is a **declared preference emitted at import, not a record of execution.** E04's
inference was sound on one banner and is wrong on two. Corrected **additively and dated** at
the report, never by deletion — the correction is more useful than the original. This is the
log-line sibling of *a number that reproduces exactly can still be measured against the wrong
object*: the string reproduced perfectly and described something else.

## Ruling 4 — ⚑ E14 RULING 3's REACH IS NARROWED. The character class is UNMEASURED on this axis — NOT solid.

The most consequential finding in the arc, and the one most easily got wrong in either
direction.

**What the record says.** [E14 Ruling 3](E14-ruling.md) opens *"Every reconstruction this route
has made is a hollow double-walled shell"* — measured **three mutually independent ways**
(ray-crossing counts, cross-section clustering, signed volumes of separable walls) on *"all
three candidates AND two out-of-family controls including the accepted dragon."* Read verbatim
at this seat: **three longswords, a dragon, a galleon. No character.** The character is the
route's founding subject class and it is absent from the evidence base of a claim quantified
over the whole route.

**What E29 measured.** `mesh_topology`'s nested-wall leg **declines to compute** on all five
character-class meshes tested — both arms, a fresh W3 rebuild, and the **recorded W3 and W1
built under the previous attention backend** — because `e14_topology.py:154` requires a second
manifold-adjacency piece larger than 1% of faces and the largest piece runs **98.2–98.6%** on
all five. The longsword the finding was made on split **54/46**.

**What is ruled, in three parts, because the parts are not the same:**

**4a. The universal quantifier is withdrawn and replaced by its evidence base.** The hollow
finding stands **for the classes it was measured on** — prop, beast, vehicle. It is not
withdrawn, weakened or doubted there; three independent methods on five meshes is strong.

**4b. The character class is ruled UNMEASURED on this axis, and a declining precondition is
NOT evidence of solidity.** The executor states this exactly and refuses to convert it, which
is the single best judgment call in the report. An inner wall shredded into hundreds of sub-1%
pieces, or fused to the outer along long contacts, produces **precisely this signature while
still being hollow** — and 800 / 291 / 4,154 pieces is consistent with shredding. Anyone
reading this ruling as "characters are solid" has read it backwards.

**4c. The remedy is to run the other two methods on a character, not to argue about the
first.** E14 measured hollowness three ways; **one** is in `mesh_topology`'s payload.
Ray-crossing counts and cross-section clustering are the instruments that can actually answer
this, and neither is on the served surface. **Commissioned in principle, unscoped here** — a
future arc measures W3 the way E14 measured the longsword. Until then the honest word is
*unmeasured*, and it is written that way in CLAUDE.md.

⚠ **[E14](E14-ruling.md) is a closed ruling and its text is NOT edited** — that would be
revision rather than correction ([E10-off Ruling 1](E10-offsurface-ruling.md)). The narrowing
lands where the law lives: **CLAUDE.md's standing constraint**, folded in this commit, which
previously read *"every TRELLIS.2 `1024_cascade` reconstruction on this route is a hollow
double-walled shell."*

**And the volumetric constraint itself is untouched.** *No volumetric predicate on an exported
mesh* rests on E01's chest-centre reading and on the mesh not being a solid after export —
neither of which this arc bears on. A consumer still meets a shell, and on the character class
it now meets one whose wall structure nobody has measured.

## Ruling 5 — ⚑ THE NOISE FLOOR IS A LAW: the generative stage is deterministic, decimation is not

Three runs, same input, same seed, same parameters: **bit-identical through `pipe.run()`, hole
filling and remeshing** — to the digit — and divergent at `to_glb`'s decimation. Measured
floor: **faces ±2,618 (0.27%), shells ±1, non-manifold edges ±18.**

**Nothing in this record carried a reconstruction noise floor, and every prior single-run mesh
comparison in this repo was made without one.** The studio's standing recollection that
*"TRELLIS is DETERMINISTIC"* ([sprite-motion-golden-3d-path]) is **half right, and the wrong
half is the half a mesh comparison lands in.**

**Ruled into CLAUDE.md as a standing law.** A difference between two single-run meshes is not a
result until it is quoted against a floor measured the same way. E29's own conclusion is safe
because its gaps are 13.7×–152× the floor — but that is a property of this arc, not a licence.

⚠ **This does not retroactively overturn anything, and no prior finding is disturbed on this
ground alone.** What it establishes is that prior single-run comparisons carry an **unmeasured**
floor. Re-litigating one requires measuring its floor, not asserting it was too small.

⚠ **And the executor names its own limit rather than smoothing it:** the floor was measured on
the *control* input across three runs and applied to the arm; no per-arm replicate was run.
Correctly disclosed, and the right call given the margins.

## Ruling 6 — P1's premise was the ADVISOR'S ERROR, written into the dispatch and inherited into a prediction

The dispatch states: *"there is no segmentation stage in front of the reconstructor."* **There
is one, inside it.** Read at source: `pipe.run(..., preprocess_image=True)` resizes to a
1024 max edge, runs a `rembg` model when the input has no alpha, takes the alpha bbox and
**square-crops to the subject**. A dungeon wall filling 100% of the non-figure frame was
removed by the reconstructor's own front door before any geometry was inferred.

**That sentence is mine — the advisor's — and it seeded a prediction that then missed.** The
executor's own post-mortem is right and is the more useful half: *two minutes of reading
`trellis2_image_to_3d.py` would have overturned P1 before it was written.* The repo's law about
inherited claims applies with full force to claims inherited **from the dispatch**, and a
dispatch is the one document an executor has least reason to doubt. **Own it in the fold that
finds it.**

**The same read retires the declared confound by measurement.** Both inputs reach the model at
**700×1024** — byte-identical dimensions, then background-removed and square-cropped — so gate
2 holds on evidence rather than on assertion. What survives is the resampling path alone (the
clay downsampled 2.4× harder), stated rather than dismissed.

## Ruling 7 — the measurement server is unreachable over MCP. The fix belongs to E31, WITH a test.

`.mcp.json` declares one server, `facet-record`. `tools/measure_mcp.py` is in neither that file
nor `E:\AI\.mcp.json`. **No session can reach the measurement server over MCP as the repo
stands.** Verified at this seat.

So the standing phrase **"the measurement server serves 8 of 8"** is true of the *code path* and
false of the *transport*, and every surface carrying it needs that qualifier until the line
lands.

**Routed to [E31](E31-publish-the-pipeline-kickoff.md) as a named task rather than hand-fixed
here**, and the reason is this repo's most expensive habit: adding one line to `.mcp.json` and
declaring it fixed is exactly the shape of running `--help` and declaring a wheel good. **The
fix ships with a test that proves a session can reach a served tool and get a payload back** —
which is E31's whole subject. E31's scope gains it as task 0-pre.

**The executor's substitute was correct and is ratified**: it imported `measure_mcp`, unwrapped
the tool functions and called them in-process. *Same module, same wrapped instrument, same
envelope — the transport differs, the code path does not, and the code path is what the
comparability claim rests on.* Both instrument sha256s are **identical across all five meshes**,
which demonstrates the property rather than asserting it. **This is the server's first use on
new work and the envelope did its job.**

## Ruling 8 — `concept-prep.md`'s background claim is corrected; its form-register half stands

[concept-prep.md](../concept-prep.md) banks background normalisation as *"an unrequested
benefit… One hop fixed the form register **and** the background problem."* Measured here, the
background problem was **already handled downstream** for this pair, by the reconstructor's own
`rembg`. Corrected in place, dated.

⚠ **The form-register half is untouched by this finding** and is what the arm actually measured
— the executor says so explicitly and is right. The clay hop's claim is now narrower and
better-evidenced, not smaller.

## Ruling 9 — the prediction family gains its EIGHTH consecutive member

Seven arcs missed on the unit, the population, an unchecked property, the rarest clause of a
conjunction, and the instrument's continued ability to express the question. E29 adds:
**the premise inherited from your own dispatch.**

P1 and P6 failed the same way — reasoning about a mechanism neither of us had read; P6 blind by
design and therefore informative, P1 inherited and therefore not. **P5 is the miss worth
keeping**: it missed by taking E14 Ruling 3's *"every reconstruction"* at its word without
checking its evidence base, landing on the exact clause the predictions had already flagged as
the one that could fail. **11 HIT, 6 MISS, 1 unscoreable, no band moved.**

**And P4 earns its own line.** It hit every band and was **wrong about what it meant** — it
predicted the row would be *uninformative about the arm*, and the arms differ at **13.7× a
floor that did not exist when the prediction was written**. *Predicting that a row cannot
separate the arms is itself a prediction, and it can miss.* Folded to CLAUDE.md.

## Ruling 10 — WHAT IS NOT RULED HERE, and will not be ruled by a metric

**Whether the clay mesh is better is the Director's, and it is not answered in this document.**
Five sheets reached him at full size under `--clay`, before this arc's first number was written
— gate 4 held by construction. No metric in this arc may answer the acceptance question, and
the report's own §6 says so in its own words: *the 82-against-9 shell gap is consistent with
the ragged sheet geometry, but consistent-with is not identifies.* This repo spent four
experiments on metrics that could not separate an asset he rejected from one he accepted.

**Stage 0's promotion or demotion is therefore still open, and it is his.** What this arc
delivers is the measurement the stage never had: the mesh comes back **structurally different**,
far beyond noise, in the direction of fewer shells and fewer pinches. **Whether that is the
mesh he wants is the question the sheets ask.**

## Ruling 11 — the executor's conduct is the bar, and two calls in particular

**It refused to convert a declining precondition into a solidity claim** (§5.2) — the finding
would have been more impressive stated the other way and would have been wrong.

**It measured a noise floor nobody asked for**, because it noticed that two runs of the same
input produced different meshes and correctly judged that the arm could not be read until it
knew whether the difference was the second variable or run noise. **That is the whole arc's
foundation and it was not in the dispatch.**

It also **re-anchored the backend change against the recorded W3 before believing any arm
result**, applying *moving a line to different hardware needs an anchor first* to a software
move nobody had classified that way — and it came back inside the floor on every quantity.

**And it handled a live-seat collision correctly**: it reported nine dirty files it had not
opened, then **replaced its own inference with the citable commit that proved it** (`dcf9a41`
landing between its two commits), staged only its own two files by explicit path, and touched
nothing else. That is the standing rule working from the executor's side.

## Ruling 12 — CI

`NOT YET RUN`, correctly, at the report. This ruling's commit carries `tools/`-adjacent paths
and will draw a run; the id is resolved **before** it is written anywhere, per the law that a
report may not contain a placeholder shaped like evidence.

---

## Folded in this commit

| where | what |
|---|---|
| `CLAUDE.md` | Ruling 4's narrowing of the hollow finding's reach (character class **unmeasured**, not solid) · Ruling 5's noise-floor law · Ruling 9's eighth prediction-family member and P4's corollary |
| `E04-gate0-report.md` | Ruling 3's dated correction, appended not rewritten |
| `docs/concept-prep.md` | Ruling 8's dated correction |
| `E31-publish-the-pipeline-kickoff.md` | Ruling 7's task 0-pre — `.mcp.json` registration **with a reachability test** |
| `docs/experiments/README.md` | the E29 status row |

## ⚖ DIRECTOR'S RULING, 2026-08-09 — BOTH PATHS ARE KEPT. Stage 0 is an OPTION, not a replacement.

His words on the sheets, closing Ruling 10:

> *"They both are great. The concept makes a more realistic mesh, which is important for more
> detailed sprites. The clay is great in its uniformity. It's clean, and could be better if the
> clay was made to be more detailed. I say keep them both as options, if that's possible."*

**Three things are ruled here and they are not the same.**

**D1 — the arm's result is read as a TRADE, not a ranking.** The concept mesh's 82 shells and
4,201 pinches are the *ragged sheet geometry* the sheet shows at the mane, belt trim and hem —
and that same geometry is **realistic relief that reaches the sprite**. The clay mesh's 9
shells and 1,461 pinches are *uniformity*. Neither number was a quality score and the ruling
declined to make one; the Director read both columns as gains on different axes, which is
what a metric that cannot answer the acceptance question leaves room for. **This is the
fourth time this repo has been right to refuse to grade an artifact with a statistic.**

**D2 — stage 0 is NEITHER promoted NOR demoted. It becomes a per-subject choice.** The route's
first box takes an image; both paths produce one; image-to-3D does not care which. So keeping
both is **possible and cheap**, and the answer to *"if that's possible"* is yes — with **one
cost, named rather than discovered later**: an asset must record **which stage-0 path made
it**, or it cannot be reproduced, and *a recipe that does not reproduce its output is not a
recipe*. That is a provenance field, not an architecture. **Scoped as a follow-up, not done
here** — this ruling does not silently widen into a build.

⚠ **And the identity question the numbers cannot see stays open.** The two meshes differ in
**horn shape, muzzle and brow** — the concept's horns longer and thinner with a sharper taper,
the clay's thicker and shorter. The Director accepted both as meshes; **nothing here rules
that they are the same character**, and [E08's canon ruling](E08-director-canon-ruling.md)
is the standing precedent that identity dominates registration. If the two paths diverge on
canon, that is a canon question for his eye on a *finished* asset, not a geometry question.

**D3 — a direction for stage 0, in his words: *"could be better if the clay was made to be
more detailed."*** The clay hop's own detail level is now a named lever with a stated target.
**Not scoped here**, and it is the natural subject of the next stage-0 arc — E29 measured the
hop as it stands, not as it could be tuned.

## Open, and named rather than left implicit

- ~~Whether the clay mesh is better, and stage 0's promotion~~ — **RULED by the Director above.**
  What remains open is the **canon** question (do the two paths produce the same character), the
  **provenance field** D2 requires, and D3's detail lever.
- **The character class's wall structure** — unmeasured; ray-crossing and cross-section
  clustering commissioned in principle, unscoped (Ruling 4c).
- **How `flash_attn` left `trellis2-env`** between 2026-08-03 and today, with no dist-info
  remnant. Not diagnosed, out of scope, recorded because that interpreter is what the whole
  repo depends on.
- **No per-arm replicate** — the floor was measured on the control and applied to the arm.
