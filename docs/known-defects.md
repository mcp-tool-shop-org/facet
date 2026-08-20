# Known defects, named

*Everything the route does not do well, measured and located in code. It stays
written down because a defect nobody wrote down becomes doctrine. The
[README](../README.md) carries the short list; this page is the full one.*

---

<!-- Moved out of README.md by the E19 treatment, 2026-08-08, at the Director's
     word ("the readme reads more like a changelog"). NOT rewritten: every line
     below is byte-identical to the README it left, corrections and ⚠ annotations
     intact. The README now links here. -->

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
[E08-intersection-regression.md §9a](experiments/E08-intersection-regression.md),
[E08-eightcam.md §5](experiments/E08-eightcam.md) and
[E08-task3-report.md §4](experiments/E08-task3-report.md); the blade arm is specified
after Gate 1 with this as its targeting data.

**⚠ The defect list below was written against high-pass metrics** that
[E07's ruling](experiments/E07-ruling-gate1.md) found blind to the defect that decides
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
inpaint. **Measured** in [E07 Gate 0](experiments/E07-gate0.md): a provenance boundary
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
[E07 Gate 0](experiments/E07-gate0.md) measured the cost by replaying that flood
carrying a source label: **74.9% of 813,773 dilated texels take their colour from another
island**, from a median **0.177 away on a figure 1.0 tall** — 61 median triangle edges, 18%
of the figure's height.

⚠ **AMENDED 2026-08-16 ([E39](experiments/E39-w3-polish-kickoff.md) Task 1) — this entry was
read for a whole arc as the explanation of W3's blotchiness, and it is not.** Two separate
corrections, and the second is the larger:

**1. Every number above is in ATLAS TEXELS; the defect is judged in RENDERED PIXELS, and for
`dilation` the two differ by 5.4×.** Measured on W3's own `provenance_atlas_indexed.png` beside
its 26 exported views:

| class | % of the **written** atlas | % of **rendered** figure px | render ÷ atlas |
|---|---|---|---|
| `reference` | 68.82% | 92.31% | 1.34× |
| `brush` | 4.23% | 2.74% | 0.65× |
| `dilation` | **26.95%** | **4.95%** | **0.18×** |

Written texels total 14.32% of the atlas, reproducing E07 Gate 0's packed coverage exactly, and
*"68.8% of valid referenced"* reproduces to the digit at 68.82%. **The atlas share overstates
what any camera sees by 5.4×** — dilation lives in gutters and in small islands, and *"paint
lives in big charts, holes live in small ones"* (below) is why: the same inspection paradox that
makes a dilated texel's island small makes it cheap in screen space. **A provenance share quoted
in atlas texels is not a claim about the asset's appearance.** Tenth consecutive arc lost to the
unit/population family, and the first where the mis-united number was the *advisor's* own
reasoning basis.

**2. `33.9% of the atlas` matches no denominator on this artifact** — the measured shares are
26.95% of the written atlas and 3.86% of all texels. The figure is left in place, unrepaired,
because its object is not identified: it may be a different arm's state, and re-deriving it while
looking at the numbers that would judge it is retuning. **It is withdrawn as a citable quantity**
until someone measures it with its object named. The same caution attaches to `813,773`: W3's own
atlas carries **647,624** dilation texels, and E07 Gate 0's figure was measured on E06's C1 state
— **two objects, one number, which is exactly the defect [E38's ruling](experiments/E38-ruling.md)
adopted the object/methodology ledger against.** Neither is asserted wrong here; both are
asserted *unattributed*.

**3. The mechanism claim itself does not survive contact with the defect the Director named.**
`dilation` IS enriched in wrong-material regions — 1.76× / 1.92× / 2.22× at three thresholds,
ranking stable — and it is **capped far below what could carry them**: 9.52% of detected-region
pixels, **4.27%** of the area of regions ≥300 px, and **11 regions against `reference`'s 369**.
On the tight, specification-defined population, **gold out of place is 91.05% `reference` at an
enrichment of 0.99× — dead on base rate**. The gold on the tunic, skirt, boots and blade arrives
through the **twin projection**, not through the flood. **Green out of place is a different
class and keeps this entry alive**: `brush` 5.49× and `dilation` 3.34×, `reference` down to
68.46% — and the blade is the one `dilation`-dominant large region, at a 48.3% plurality.
**So: this defect is real, it is where this entry says it is, and it is not the one that decides
acceptance.** The 4.8×-enrichment sentence above rests on a **speckle** measure, and CLAUDE.md's
own law holds that a 5×5 high-pass statistic is structurally blind to a large region of the wrong
material — which is what a gold blob on a green tunic is.

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
[E07 Gate 0](experiments/E07-gate0.md): the island holding a randomly chosen *styled*
texel has a median 1,231 texels (~35×35), the island holding a *dilated* one has 296. So
atlas-space operations are safe exactly where there is already paint and unsafe exactly where
there is not — which is why stage 1's σ=16 levelling draws only 6.8% of its weight
off-island (median) and does no measured harm, while the dilation flood at the same scale
does. Beware the inspection paradox in either direction: the median island holds 88 texels,
but the median *texel* does not live in a median island.

---


## Vertical peach banding across A1's face — view ownership at chart boundaries (Director, 2026-08-19)

**The twin's face is one continuous wash; the bake is cut into vertical strips of different
peach.** Ruled by the Director on the E70/E71 head crop. **It is not dirt, and it is not the
cream-vs-grey hole class** — those are the separate RGB(107) patches in hair, collar and vest.

**Mechanism, ruled by the Director and confirmed at source before this entry was written.**
`tools/project_twins.py:936-939` is winner-take-all, not averaging:

```
take = w > best_w[idx]
best_w[idx[take]] = w[take]
owner_c[idx[take]]  = col[take]
owner_i[idx[take]]  = _view_i
```

One camera wins each texel outright, by facing weight. A1's face is seen by the front view and
the two 45° quarters, **and those twins do not agree on skin value** — the front is flatter and
cooler, the quarters warmer and more modelled. Wherever two UV charts on the face are owned by
different cameras, the disagreement lands as a hard step. **The bands are island boundaries.**

Measured, on the accepted ring's own head crops: across-view skin spread **R 13.0 / G 13.9 /
B 18.3** (max−min of per-view mean skin RGB). That is the size of the step available at any
ownership boundary, and it is a property of eight independent generations rather than of any
defect in one of them.

**What the evidence is, and what it is not.** The measurement here is the **twin-beside-mesh
pair at the Director's zoom** — the twin's face continuous, the bake's cut into strips. An
advisor's column-step statistic over a small crop is a weak instrument for this and was
withdrawn as such: it separated the two images by 19 steps against 30, which is not what a
reader of the pair sees. Same for a warm-pixel skin mask written the same minute, which
selected 30,123 px in the twin against 7,703 in the bake — different populations, so its
colour delta measured the mask.

**This is not caused by the hole fill and E71's arms do not touch it.** Arm F's render carries
the identical banding. It is baked into the stage-1 atlas.

**⚠ The scope of E70's approval, stated so the record does not overstate it.** The Director
approved E70 on **identity and the garment set** — recognisably the same man, plum vest, cream
sleeves, umber sash, green trousers, brown shoes, crown not bald, shirt not backdrop grey. The
banding **was already present on that sheet's `v0_mesh_head.png`** and the approval did not
cover it. **It is a real fail of "seamless face"** and it stands as an open defect on an
approved artifact — the two are not in conflict, and the record must not read the approval as
covering a property nobody graded.

**The brush cannot fix it, and this is structural rather than a matter of effort.**
`texpass_iter.py` commits edited pixels into **HOLE texels only; styled texels are never
overwritten**. The bands are styled texels. So:

| what you see | cause | can a brush stroke touch it? |
|---|---|---|
| vertical peach bands on cheeks and forehead | styled texels, different owners | **No** — commit writes holes only; styled is frozen |
| grey patches in hair, collar, vest | RGB(107) holes | **Yes** — that is the brush canvas |

**Two candidate remedies, both NEW DOCTRINE and neither in scope for stroke one** (Director,
2026-08-19): let the front view own the whole head band; or a seam-blend that is **allowed to
rewrite styled skin**, which no stage in this route may currently do.

**Enumerated for whoever runs that sitting, so it is not commissioned twice:** the tool
**already computes a weighted average alongside the winner** — `sumW` / `sumWC` at
`project_twins.py:934-935` — and **the blended atlas is already on disk**,
`E:\AI\training\facet_E69\bake\atlas_widescope_blend.png`, written by the same run that
produced the approved `atlas_widescope.png`. Whether it reads better is a look question and it
is free to render. That is not a claim that it fixes the banding; it is a claim that the
artifact exists and nobody has put it in front of the Director.

## Tooling defects

### `texpass_iter selftest` writes REAL texels into the state it is gating (E72, 2026-08-19)

**The gate that protects a paid generation leaves permanent residue in the directory it
guards.** `selftest` emits, fake-inpaints by local blur, and **runs a real `commit()`** - by
design, because that is how it proves styled texels stay byte-identical and holes strictly
shrink. But the texels it writes are indistinguishable from real paint afterwards: E72's
Stage 0 selftest left **9,489 yaw-0 texels marked permanently STYLED** in the shared
`state/` directory, so the "pristine E69 bake" the Stage 1 stroke was about to emit against
was not pristine.

**Found before it could touch a number**, by the Stage 1 seat rather than by a check - it
noticed while preparing to emit, reset `atlas.png` / `holes.png` / `styled_mask.npy` from
sha256-verified E69 copies, **disclosed the reset in `predictions.md` before running
anything**, and then re-emitted yaw 90 to prove the reset was inert: 106,893 figure px /
17,868 hole px, reproducing Stage 0's numbers exactly.

**Why it matters beyond one arc.** The residue is silent, it is in the *shared* state dir, and
it accumulates - a lane resuming across sessions would emit against a mixture of real paint
and blur-fill with nothing anywhere saying so. The gate's own honesty is what creates it:
`commit` is the only way to test `commit`.

**Director's ruling, 2026-08-19: before stroke two, `selftest` gets its own directory. It is
NOT to be "fixed" by committing those texels.** The residue is not paint and must not be
promoted to paint to make the problem go away.


*Added 2026-08-08 at the v0.2.0 release read-back. The route's defects are above; this
section is for the instruments themselves, which are now published products and so have
users who are not this repo.*

**`facet-index q` answers from an index that does not exist, and its answer is
indistinguishable from a real one.** Pointed at any path with no database —
`facet-index q "the hollow finding" --db ./nope.db` — the verb **creates a 0-byte file**
and prints `(no rows)`, **exit 0**. The term used in that measurement is one of the
seeded set, a question whose target the four-leg verify requires to rank **1**. So the
strongest possible query returns the same output as a genuine miss, and the operator has
no way to tell "the record has nothing on this" from "there is no record here."

**The mechanism, located:** [`tools/facet_index.py:2194`](../tools/facet_index.py) opens
with a bare `sqlite3.connect(args.db)` — which *creates* a missing file rather than
failing — and consults neither the file's existence nor the health certificate. `query()`
then swallows the consequence: both of its `except sqlite3.OperationalError` handlers —
[`:1876`](../tools/facet_index.py) whose body at `:1877` is `pass`, and
[`:1884`](../tools/facet_index.py) whose body at `:1885` is `return out[:limit]` — were
written to tolerate a **malformed FTS5 MATCH expression from user input**, and
`no such table: fts` is the same exception class. Three distinct
conditions — bad query syntax, no index at all, and nothing matched — collapse into one
output and one exit code.

**This is the repo's own law, and the guard's stated reason is not the reason it fires.**
An error handler written for a narrow condition catches a structural one by accident; the
result is an answer that cannot be distinguished from its own failure, which is the
sibling of *a check that cannot fail is not a check* and of the silhouette IoU that
returned 1.00000 on a holed mesh.

**It contradicts the surface built beside it.** The MCP server's `record_query` refuses
when the index is not verified, on the stated principle that **a wrong citation is worse
than no answer**. Two surfaces over the same index disagree about whether to answer from
an unusable one, and the CLI is the one a shell script will call.

**Reachable without a `--db` flag.** The default resolves against the working directory,
so the published binary run anywhere outside a checkout takes exactly this path — the
same class v0.1.1 fixed for the server, still open on the CLI.

**Not a v0.2.0 regression, and the release's own contract holds.** All three declared
codes were measured on the *published* artifact at the read-back: `--print-tools` → 0,
`--no-such-flag` → 1, and `verify` against this very empty database → **2**, with a
structured refusal and a `--debug` hint. `verify` gets it right; `q` does not.

**Disposition: unruled, and deliberately not fixed in the seat that found it.** The
honest code is a refusal, which points at E22's incoming `4 = REFUSED` — but E22's scope
is ruled narrow, and quietly widening a dispatched spec is the move this repo forbids.
It goes to the Director as a finding with its measurement, not into a spec by the hand
that noticed it.

**The `pip` / `pipx` install cannot find the record at all — only the `npx` binary can.**
Found at the v0.3.0 release read-back, by installing the published wheel and running more
than `--help`. `facet_index.py` ships as a **top-level py-module**, so on a wheel install
`__file__` is `<venv>/Lib/site-packages/facet_index.py` and
[`facet_index.py:69-70`](../tools/facet_index.py) computes
`REPO = dirname(dirname(__file__))` = **`<venv>/Lib`**. Every corpus and default-DB path
is then resolved under a directory that holds neither. Measured on the published 0.3.0
wheel, with the working directory set to a real facet checkout:

| surface | result |
|---|---|
| `facet-index --help` · `facet-mcp --print-tools` | **work** — and these are exactly what `release.yml`'s wheel test runs |
| the `db:` line `--print-tools` prints | `<venv>\Lib\docs/index/facet.db` — **a path that cannot exist** |
| `facet-index build` | `RUNTIME_ERROR` — *cannot find `<venv>\Lib\docs\experiments`* |
| `facet-index q` with no `--db` | `RUNTIME_ERROR` — *unable to open database file* |
| `facet-index q --db <a real index>` | **works**, exit 0, correct rows |
| `record_get`, even with a valid `--db` | `REFUSED: no record corpus under <venv>\Lib` |

**Not a v0.3.0 regression — measured, not assumed.** The published **0.2.0** wheel fails
identically (`REPO` = its own `<venv>\Lib`), so this has been true since the extraction.
**The `npx` path is unaffected**: v0.1.1 fixed the *frozen* branch to resolve against the
working directory, and `npx @mcptoolshop/facet` still downloads, verifies SHA256 and
prints a correct `db:` line. Only the *wheel* branch was left behind.

**Why nothing caught it, which is the transferable part — and it is the same lesson for
the third time.** `release.yml`'s own step is *"Verify the wheel runs from a clean venv"*,
and it runs `facet-index --help` and `facet-mcp --print-tools`. **Neither touches the
corpus or the database.** T27/T28 pin packaging shape and the frozen branch. Every check
exercises the surface that works. *A green pipeline verifies the thing it built, not the
thing a user receives* — and this time the artifact was installed and a **verb** was run,
which is what the earlier statement of the law did not quite say.

**Second, separate defect on the same read-back: `$FACET_INDEX_DB` is honoured by
`facet-mcp` and NOT by `facet-index`.** `DB_ENV` is defined in
[`record_mcp.py:138`](../tools/record_mcp.py) and has no counterpart in `facet_index.py`,
but [README](../README.md)'s Install section says *"Point **either** at an index with
`--db` or `$FACET_INDEX_DB`."* Measured: the env var leaves `facet-index q` at
`RUNTIME_ERROR`, while `--db` on the same invocation returns rows.

**Disposition: unruled, and not fixed by the seat that found it.** The repair is a
behaviour change to the path resolution of two published commands — it wants a spec,
committed predictions and tests riding the commit, not a hotfix from the advisor's chair.
The README's Install section is corrected in the meantime, because a front door that
tells operators to run a command which cannot work is a false claim, and correcting a
document is not a behaviour change.

**An unprofiled run resurrects a withdrawn threshold.** `project_twins.py:93` carries a
`--bg-max-pct` default of **2.0** — the pre-withdrawal value.
[E16 Ruling 4e](experiments/E16-ruling.md) withdrew that condition to the expressed
suspension (100.0) because its stated derivation was measured against the retired
corner-median reference — but the withdrawal landed **only in `profiles/character.json`**,
so every unprofiled run re-arms a condition a ruling retired. Fired live on E33's first
projection (9.00% against the resurrected 2.0 limit, exit 1, nothing written); the run was
repeated at the ruled suspension value passed explicitly with its provenance
([E33 §14b](experiments/E33-report.md)), and E34's dispatch rules that the withdrawal
governs unprofiled runs. **Disposition: unruled as a tool change, and not fixed by the
seats that found it** — moving a route-tool default is a behaviour change wanting its own
spec, prediction and test; a default that contradicts a ruling is recorded here so it
cannot quietly become doctrine.

---

## Texture-projection holes on the performer — ruled TOP PRIORITY by the Director, 2026-08-13

**The unpainted patches on the E33 performer's texture are now the studio's
highest-priority facet defect.** Six of the performer's eight turnaround views carry
unpainted texture-projection patches (jaw, temple, shoulder, ribcage, flank; the front
and back views measure clean). armature measured them twice on 2026-08-13 — flat-alpha
survey, then an RGBA-true re-render that proved they are texture truth, not render
artifacts (they re-color under different lighting and persist) — and then watched them
**propagate into hosted-tier generations**: the E13 identity probe carried the patches
into generated output at the same landmarks. The Director ruled the character holds and
the composed route proves its lever, which makes the holes the named confound on every
identity read downstream: **a faithful hole and an identity failure are not separable
by looking at the patch.**

Evidence, cross-repo: the per-view hole survey (old set beside RGBA-true re-render) at
`E:\AI\armature-S03\outputs\S03\survey\`; propagation sheets at
`E:\AI\armature-E13\outputs\E13\sheets\`; the rulings in armature's
`docs/dispatches/S03-ruling.md` (R3–R4) and its E13 record. The asset:
`E:\AI\training\facet_E33\out\performer_textured.glb` (sha256 `9e20ea7d…`); the
affected views `facet_E33/turn_final/armfinal_1,2,3,5,6,7`.

The repair is this repo's projection-coverage arc — armature documents and consumes,
never edits. It enters through facet's own method: a spec, committed predictions, tests
riding the commit. **Priority set by the Director's word, 2026-08-13.**

**⚖ REPAIRED AND ACCEPTED — [E34](experiments/E34-ruling.md), 2026-08-13.** Eight-view
projection in the approved register: holes 927,492 → 157,228, the patches closed at
every named landmark, accepted at the Director's eye with the suite green (927/0). The
candidate is the record's fifth accepted asset; the recorded E33 asset stays
byte-unchanged as the pre-repair state. **A second, distinct defect class on the same
asset was then ruled unacceptable at his zoom — the dark-speck class, next entry.**

---

## The dark-speck class on the performer — ruled unacceptable by the Director, 2026-08-14

**Scattered dark brown-to-black speckles — 2–6 px dots at the 352×1024 frame scale,
reading as sharp dark triangles at zoom — across the performer's textured surface.** A
second defect class, distinct from the unpainted patches E34 repaired. Found at the
Director's zoom after E34's acceptance and ruled unacceptable the same day. It is
visible on the accepted sheets, and neither the E34 report's observations nor the E34
ruling named it — owned at the ruling seat as that walk's miss.

**Measured attribution (E34 ruling seat, 2026-08-14; strips, per-pixel samples and the
script staged at `E:\AI\training\facet_E35\diag\`):**

- **Texture truth, not shading.** The specks persist under FLAT light. Near-black
  counts, torso/legs crops: lit 3,233 / 2,039 px (dominated by legitimate joint
  shading) against flat **18 / 20 px** — the flat residue is the baked dot cores.
- **In the generated twins.** Every sampled view carries dark dots on the figure —
  127 / 263 near-black px per crop, cores ~(70–95, 40–60, 15–40) — and at **5 of 6
  sampled speck locations the twin is dark at the matching pixel**.
- **The controls are clean.** The clay renders carry **0** near-black px: the canny
  transmits no speck features. The generator invents the dots.
- **Predates and survives E34.** The 2-view and 8-view textures carry the class at
  near-identical values at the same locations (e.g. (59,52,49) in both) — every twin
  carries it, so re-projecting from more views multiplies its sources.
- **A minority sub-population is not twin paint.** ~1 of 6 sampled specks is pure-black
  (11,9,8) at a texel whose view twin is mid-tone — candidate pipeline-local mechanisms
  (the 10×10 parked-face patch, unfilled texels), **UNMEASURED**, task 0 of the repair
  arc.

**The Comfy consult** ([brief](comfy-consult-1-brief.md) → [answer](comfy-consult-1.md))
ranks the mechanism: **the register prior rendered under an over-denoised (0.92)
near-uniform grey init, hardened by ControlNet at 0.9** — the model painting plausible
terracotta mineral flecks — with fp8 quantization and VAE decode ranked against this
signature. Discriminators, cheapest first: a seed re-roll A/B (dots move = seed-bound
content class, and cross-seed averaging becomes a lever; dots stay = input/quant-bound,
the bf16 swap decides), then a denoise sweep 0.92/0.80/0.72, then cn_strength 0.65. A
frequency-separation despeckle on the twins is the deterministic fallback — its four
nodes verified against the live catalog at the facet seat, with one interface
imprecision found and recorded in the answer's calibration section.

---

## The canny brow-fragmentation artifact — control-side, riding an accepted asset (found 2026-08-15, E37 Gate-R)

Canny on the studio-lit clay render fragments the brow ridge where its specular
highlight fades: instead of one continuous brow edge, the control carries a broken
line plus a detached speck cluster, and ControlNet at 0.9 renders the cluster
literally as a dark facial mark. Measured at E37's Gate-R probe: the wood twin's
29 px blob at (123,167) sits exactly on a seven-fragment cluster in the control;
the clay geometry carries no feature there — nearest dark feature is the brow
itself, 9.4 px away. **The accepted E34 performer carries the same artifact at
(124,166) at 81 px, nearly 3× larger** — present since E34, camouflaged by
terracotta (a mole-coloured speck on terracotta reads as terracotta), surfaced by
pale wood. Control-side, not prompt-side: prompt iteration cannot move it. The
canny thresholds (`--canny-low 0.4 --canny-high 0.8`) are defaults never tuned on
this subject and are the named lever; flat light is not an answer — E36 measured
that flat collapses the control to pure contour, losing every interior edge with
the artifact. Repair specced at [E37 Ruling 5](experiments/E37-ruling.md) (local
threshold iteration, brow continuity verified on the control image, one confirm
job); the E34 attribution rides the next armature relay so S07's panels read that
forehead mark as a control artifact, not paint intent.

---

**Disposition: E35 DISPATCHED, 2026-08-14**, at the Director's mandate (comprehensive
fix; the despeckler built out as a route capability) — spec at
[E35-clean-twins-kickoff.md](experiments/E35-clean-twins-kickoff.md), five-agent
research grounding at
[E35-speck-research-grounding.md](research/E35-speck-research-grounding.md). No recipe
change ships without his eye re-gating the register (Gate R — R3 is his ruling); the
span bump to `E3[0-5]` rides the dispatch commit.

**⚖ E35 CLOSED (2026-08-15 → [E35-ruling.md](experiments/E35-ruling.md), Rulings
1–11); the class is measured to its floor and STANDS.** Five directions closed by
measurement — the seed frontier is one-dimensional, cn weakening raises the pale
class, denoise kills the register before either class, no slate lever moves the dark
class while keeping the man, and 2509 is class-worse at both its configurations —
and **no repaint candidate was produced**: the recorded route remains the class-best
measured configuration and its best-measured candidate (R2-b) stands rejected at the
Director's eye. The dark class is baked-shadow painting, 57 components to 377 px² on
the accepted asset — above the corrector's 36 px² cap **by design**; the successor
corrector contract (E36's second front) is the named path to those components. The
pale class resolved into TWO signatures — chroma-collapsing init-bleed (mechanism
established; anchoring suppresses it) and chroma-preserved lightening (the rejected
class; mechanism open) — and is read by the chroma-split instrument, not by eye at
working zoom.

**The attribution above, reconciled — two instruments, two operands, both standing.**
This entry's "5 of 6 sampled speck locations" line was re-measured at scale in the
E35 report and weakened in place: the six sample points de-duplicate to two distinct
locations, one of them a broad shadow crevice rather than a dot. The honest pair of
numbers, and why they do not contradict: the **final-atlas census** attributes the
atlas's dark *texels* to their painting source — core-black **61% twin-painted / 39%
fill-propagated** (wide-dark 79% / 21%) — answering *who painted what the atlas
holds*; the **render-dot co-occurrence** asks of each *rendered dot* whether the twin
carries a detector-grade speck at the exact matching pixel — **14.3%, against 2.3%
chance, ×6.13**, decaying monotonically with tolerance, the signature of real spatial
correspondence. A dark texel is twin-painted whenever a twin sourced it, speck or
broad shading alike, so the census's 61–79% and the co-occurrence's 14.3% measure
different operands and both stand: **the twins are a genuine source and they are not
the only one.**

---

## Atlas texels that are never painted — the class that survived every route change (E38, 2026-08-16)

**Some visible mesh surface maps to atlas space no bake ever writes, so it renders as the
image's untouched default fill, which is black.** Found in [E38](experiments/E38-material-route-kickoff.md)
by replacing the entire colouring process — a procedural wood material authored directly in
UV space, no diffusion anywhere — and watching the dark-mark class **survive**: 847 → 425
marks, with **69.2% of them within 3px of a mark in the diffusion-textured build**, across two
colouring processes with nothing in common. That co-location is what moved the class out of
the generator, where three arcs had hunted it, and into the shared atlas substrate.

**Split by a criterion chosen before looking, with a perfect null:**

| population | share of mark pixels | signature |
|---|---|---|
| **A** | **57.94% / 60.34%** | UV lands outside any triangle's UV footprint; **100.00%** read atlas RGB exactly **(0,0,0)**. Null: **0.00%** |
| **B** | 42.06% / 39.66% | atlas is clean at the exact nearest texel; boundary-distance median **1.414** against the null's **2.828** |

Both were then confirmed by **intervention rather than inference**: refilling the atlas
background with magenta left **0%** of A dark, and shifted **100%** of B at median ΔE 66–67
*while nothing at B's own nearest texel changed*.

⚠ **B's independence is challenged and under test.** B may be render-time bleed sourcing
*from* A's black texels rather than a separate mechanism — B fell 49–61% under an arm that
touched no packing parameter at all. If that holds, this is one mechanism with a halo, not two.

**The mechanism is named by Blender's own developers.**
[PR #161752, *"Bake: Conservative rasterization for texture bake"*](https://projects.blender.org/blender/blender/pulls/161752),
**merged**, commits 2026-07-27/28 — resolved at the tracker's API because the HTML 403s:

> *"Blender can miss small, thin or long triangles during the texture bake as texel center
> sampling is used to determine which triangles overlap texture pixels. So, if a triangle does
> not overlap texel center, it will be empty."*

That is Population A exactly. **Blender 5.2.0 LTS (build 2026-07-14) predates the fix**, so
every asset this route has produced was baked without conservative rasterization.

**Located in code, and both sites are defaults nobody chose.**
[`bake_hero_prep.py:319`](../tools/bake_hero_prep.py) calls
`bpy.ops.uv.pack_islands(margin=args.pack_margin)` passing **only** `margin` — so
`margin_method` has silently been Blender's default **`SCALED`** on every build this project
has ever made, and SCALED multiplies the gutter *by island size* on an atlas whose median
island is ~117 texels. The repo's own [E07 Gate 0](experiments/E07-gate0.md) already measured
the consequence and never connected it: **5.73% of 4-adjacent valid texel pairs are in
different islands and touching directly.** Separately, `bake_hero_prep.py:452` sets
`scene.render.bake.margin = 8` and passes neither `margin_type` nor `use_clear`, inheriting
`ADJACENT_FACES` and `use_clear=True` from the scene mirror.

**`ADJACENT_FACES` is itself defective, per Blender's own tracker.**
[#119393](https://projects.blender.org/blender/blender/issues/119393) is **open** and
*Confirmed* — a 4.0.2 regression against 3.6.8 — and
[PR #162226](https://projects.blender.org/blender/blender/pulls/162226) (open, 2026-08-01)
catalogues ~16 concrete defects in the underlying fill search, including bounds checking that
compares y against the image *width*. Measured here: switching that one setting to `EXTEND`
cut the remaining marks a further 52–56%.

**⚠ This is E05's defect, and it survived the fix that was thought to close it.**
`bake_hero_prep.py`'s own `--reunwrap` help text has carried the finding the whole time —
*"at 8 faces an island is small enough to be entirely unpainted, and 54.6% of them were."*
**That is Population A.** E05 identified the mechanism, adopting native xatlas UVs reduced it,
and the record treated the matter as settled. Apples to apples, E38's layout (13,722 islands /
21.9 faces) is **normal for this route** against W3's 14,010 / 20.5 — so the class is a
property of **every asset this route has produced**. *Measured on E38's subject;
**UNMEASURED** on W3, the galleon, the dragon and the longsword. Naming the exposure is
honest; quantifying it there without measuring it there would not be.*

**Measured levers, all local and free.** Population A against its 766-pixel baseline:
`margin_method='ADD'` **−91.5%** at unchanged resolution, with atlas utilisation rising
6.37% → **24.10%**; atlas resolution 4096 → 8192 **−92.7%**, at 4× the texture memory;
`margin_type='EXTEND'` on top of ADD **−95.95% cumulative**. Raising the *nominal* margin while
leaving the method at SCALED is catastrophic — utilisation collapses to 0.52% and the census
worsens 25× — which is the same diagnosis from the other side.

**Measured to a conclusion, 2026-08-16.** Population A against its 766-pixel baseline, all at
4096 unless noted:

| arm | Population A | Population B |
|---|---|---|
| A0 — stock 5.2 | 766 | 556 |
| A1 `margin_method='ADD'` | 65 | 323 |
| A4 `--res 8192` | 56 | — |
| A1+A7 (`margin_type='EXTEND'`) | 31 | — |
| A1+A7+A6' (bake `margin` 16) | **4** | 279 |
| **A11 — Blender 5.3 alpha, STOCK settings** | **0** | **165** |
| A11 + all three levers | 0 | **257** — *worse* |

**Two answers, neither displacing the other.** On 5.2 today the three levers are right. On 5.3
**change nothing** — they were compensating for a Blender defect and turn net-negative once it
is gone, because tight packing carries its own independent cost on Population B. **5.2 remains
the route**; the 5.3 alpha is an instrument.

**Population B is INDEPENDENT of A**, closed by intervention rather than by geometry: the
magenta refill moved 100% of B at A0 and **0.0%** of B at A11, median ΔE exactly 0.0. An earlier
geometric criterion claimed to settle this and was **withdrawn** — its 1–2 texel window tested
*bilinear* reach while B's nearest unpainted neighbour sat 7–8 texels away, inside a *mip*
kernel. The advisor's mis-scoped radius; the interventional test is what closed it.

**⚠ AND THE SCOPE CORRECTION THAT MATTERS MOST, at the Director's word 2026-08-16:** *"let's not
over focus on the black artifacts. W3 is far from perfect and needs a serious polish."* He is
right. This class measures **0.578% of W3's figure pixels and renders zero black there**. What is
visibly wrong with W3 is **blotchiness across every material** — gold on tunic, skirt, boots and
blade; green on the sword grip; brown-green smears on hands and bracers — which is the
**cross-island bleed** entry above, at 74.9%. An entire arc was spent on a countable class while
the dominant visible defect sat in this same document, measured, treated as a footnote. That is
this repo's own recorded failure — *a metric that cannot separate an asset he rejected from one
he accepted is not a metric* — committed again in a new costume.

**Disposition: E38 RUNNING; nothing here is adopted.** Population B and the cross-island bleed
above are plausibly one class at two sites — a render-time *read* and a bake-time *write* — and
**that is unconfirmed and is the live question.**
