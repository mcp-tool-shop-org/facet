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

## Tooling defects

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

**Disposition: E35 DISPATCHED, 2026-08-14**, at the Director's mandate (comprehensive
fix; the despeckler built out as a route capability) — spec at
[E35-clean-twins-kickoff.md](experiments/E35-clean-twins-kickoff.md), five-agent
research grounding at
[E35-speck-research-grounding.md](research/E35-speck-research-grounding.md). No recipe
change ships without his eye re-gating the register (Gate R — R3 is his ruling); the
span bump to `E3[0-5]` rides the dispatch commit.
