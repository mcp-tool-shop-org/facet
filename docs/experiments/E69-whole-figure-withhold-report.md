# E69 report — the same write-gate, every face: the ANDON collapses

Executor seat (Sonnet), background. Charter: `docs/experiments/E69-whole-figure-withhold-
kickoff.md` (commit 0a6ca70). Direct predecessor read whole: `docs/experiments/
E68-headband-withhold-report.md`. Classifier instrument read whole, unchanged: `docs/
experiments/E67-contamination-map-report.md`. Working tree `E:\AI\training\facet_E69\`.
Live handoff kept throughout: `E:\AI\training\facet_E69\handoff.md`.

**ZERO CLOUD SPEND.** No comfy-cloud tool was ever loaded or invoked this session. Gate A
passes by construction.

## The rule, as implemented

One new sibling flag, `--bg-withhold-scope {headband,all}` (default `"headband"`), added to
`tools/project_twins.py` (+42/-11 lines, `git diff --stat -- tools/project_twins.py`, 3
hunks). At `headband` (the default), the block computes exactly what E68's own
`--headband-bg-withhold` computed — `hb = headband[idx]` — byte for byte. At `all`, `hb`
widens to every accepted texel on that view (`np.ones(len(idx), dtype=bool)`), so the
SAME predicate E68 wrote — `withhold = hb & (dE_bg < args.bg_de)`, the tool's own existing
`dE_bg` at its own existing window, no new threshold — now applies wherever it fires rather
than only inside the head-band crop. The post-loop diagnostic gained one guarded line
printing a whole-figure pooled hole-cost figure when `scope == "all"`, alongside E68's own
unchanged head-band line. Every new line is guarded by `if args.headband_bg_withhold:`
(unchanged from E68) and, within it, by the scope check; the default path (`--headband-bg-
withhold` omitted entirely) is proven byte-identical to pre-E69 (Gate C, below).

No new threshold was introduced. `--bg-de` and `--bg-max-pct` are unchanged in value and
untouched in the ANDON's own comparison — asserted against the tool's live source text
(Gate B) and printed in every console run below.

## Predictions, logged before touching any code

Full text: `E:\AI\training\facet_E69\logs\predictions.txt`. Five predictions, honestly
split between CODE-DERIVED (read off `project_twins.py`'s own source at current HEAD
before writing this experiment's code) and BLIND.

- **P1 (CODE-DERIVED).** The withhold's `dE_bg < args.bg_de` predicate and the ANDON's own
  re-test (`p_rx = mean(dE_bg[relaxed] < args.bg_de)`) share the identical array and
  comparison. Widening `hb` to all-True makes `p_rx` provably 0.00% on every view — not
  empirically small, exactly zero by construction, since any relaxed texel surviving the
  widened withhold cannot have `dE_bg < bg_de` (it would already be gone).
  **CONFIRMED EXACTLY** — 0.00% on all 8 views, both the single-view test and the full
  joint run.
- **P2 (CODE-DERIVED, contingent on P1).** No other gate in the file depends on
  `dE_bg`/`relaxed`/`headband`, so the joint 8-view run should complete with exit 0 — the
  first joint (non-single-view-swept) run to do so anywhere in the E67/E68/E69 arc.
  **CONFIRMED EXACTLY.**
- **P3 (BLIND).** Whole-figure hole cost in the range 0.1%–1.0% of all valid texels
  (3,500–35,000 texels). **FALSIFIED, on the small side** — measured 1,468 texels
  (0.0423%), roughly 2.4× below the predicted floor.
- **P4 (BLIND).** A "new-territory" population (strict-admitted, non-headband,
  background-colored — texels E67's own map never characterized) of "low hundreds to low
  thousands" pooled view-instances. **CONFIRMED, at the low end** — 115 pooled
  view-instances, collapsing to just 4 unique texels once multi-view redundancy is
  accounted for.
- **P5 (BLIND).** New holes concentrate at particular structures (the charter's own named
  vest opening/collar/sleeve/fingers) rather than spreading uniformly. **CONFIRMED** — see
  the overlay sheet and region breakdown below; the Y-band distribution is sharply
  non-uniform (a near-empty band between two populated ones).

## Gates

| gate | status | evidence |
|---|---|---|
| Gate A — no cloud call | **PASSED (by construction)** | no comfy-cloud tool loaded or called this session |
| Gate B — `bg-de`/`bg-max-pct` byte-unchanged | **PASSED** | asserted against the live source text (below), printed in every console run |
| Gate C — default path byte-identical to pre-E69 | **PASSED** | normalized diff (two known, harmless artifacts only — see below), both the bare-default AND `--headband-bg-withhold`-alone invocations |

**Gate B, printed, per the charter's instruction:**
```
--bg-de default (parsed from live source)      = 10.0
--bg-max-pct default (parsed from live source) = 2.0
```
Both declarations confirmed present, unchanged, and declared exactly once each
(`logs\gateB_threshold_assert.txt`, exit 0). Every console run below prints `dE 10` /
`2.0%` verbatim, corroborating independently.

**Gate C, non-perturbation, proven not eyeballed:** the same two view-0 invocations
(bare default; `--headband-bg-withhold` alone) were captured pre-edit and re-run
post-edit, then diff-asserted equal after normalizing exactly two EXPECTED artifacts: (1)
the first pre-edit capture predates my setting `PYTHONIOENCODING=utf-8`, so its em-dashes
decoded as replacement characters — a capture-method artifact, not a tool-behavior change;
(2) the traceback's `line NNN` reference shifts by the +23 lines this edit inserts above
the unmoved `raise` statement. Every other byte matches exactly, including the ANDON
message text and every printed number (`logs\gateC_nonperturbation_assert.txt`, exit 0).
**Bonus, beyond the charter's minimum:** `--headband-bg-withhold` alone (no scope flag,
i.e. E68's own exact invocation) is ALSO proven unperturbed by this edit — the widening
did not change E68's own already-shipped behavior.

## Provenance (Gate 0, re-verified fresh)

All 8 accepted twins' sha256 match `MANIFEST.json` exactly. The RAW mesh
(`facet_E57\mesh\A1_1024_cascade_seed42.glb`) sha256 matches the recorded `cdf276e794fe...`
prefix exactly. **First draft of this check hashed the wrong file** — `prep_uv.glb`
against the raw mesh's recorded prefix — caught before being trusted: E67's own report
(line 16) names the RAW mesh as what Gate 0 checks, and `prep_uv.glb` is a Stage-1-DERIVED
file, confirmed genuinely different from the raw mesh by E67's own before/after
`mesh_topology` table (faces −9, boundary_edges +16, unwelded verts +4,632) — its earlier
"byte-identical renamed copy" characterization is explicitly OVERTURNED within that same
report. `prep_uv.glb` itself has no directly recorded prior hash; its non-perturbation is
established empirically instead (below), which is a stronger check than a hash match
would have been. `logs\gate0_provenance.txt`.

**`prep_uv.glb` and the whole pipeline confirmed unchanged since E67/E68**, without a
recorded hash for that file: view 0 was re-run bare AND with `--headband-bg-withhold`
alone, at current HEAD before any edit, and BOTH reproduce E67/E68's own recorded console
output exactly — mesh silhouette 29.7%, twin paint 29.7%, IoU 0.9228, relaxed 16,170,
30.29% within dE10 (bare); 4,380/146,546 withheld (2.99%), 4.56% residual
(`--headband-bg-withhold`). `logs\preedit_baseline_v0.txt`, `logs\
preedit_baseline_v0_withhold.txt`.

## THE CENTRAL RESULT — per-view limit comparison, three regimes

**The limit was not touched — `--bg-max-pct` printed 2.0 in every run below. It now PASSES
on all 8 views.**

| view | yaw | OLD % (E67, no withhold) | E68 % (headband-only) | **E69 % (whole-figure)** | limit | E69 verdict |
|---|---|---:|---:|---:|---:|---|
| 0 | 0   | 30.29 | 4.56  | **0.00** | 2.00 | **PASS** |
| 1 | 45  | 37.48 | 7.24  | **0.00** | 2.00 | **PASS** |
| 2 | 90  | 29.19 | 6.91  | **0.00** | 2.00 | **PASS** |
| 3 | 135 | 29.27 | 17.56 | **0.00** | 2.00 | **PASS** |
| 4 | 180 | 28.92 | 10.09 | **0.00** | 2.00 | **PASS** |
| 5 | 225 | 42.88 | 10.45 | **0.00** | 2.00 | **PASS** |
| 6 | 270 | 34.37 | 11.43 | **0.00** | 2.00 | **PASS** |
| 7 | 315 | 47.03 | 21.65 | **0.00** | 2.00 | **PASS** |

**8/8 views PASS** — reversed from E68's 0/8. This is not an empirical trend: it is P1's
structural guarantee, measured on the real tool's own console (single-view test AND the
full 8-view joint run — the first joint invocation to complete in the whole E67/E68/E69
arc, `logs\widescope_joint8_console.txt`, exit 0).

**The mechanism, measured, not inferred.** The withhold's own predicate and the ANDON's
own re-test share the identical `dE_bg` array and the identical `< args.bg_de` comparison
— once `hb` stops gating on head-band membership, any texel that would fail the ANDON's
own residual check is, by that same predicate, already withheld before the ANDON reads
its population. The residual cannot be non-zero without the code contradicting itself.

## Set-identity proofs — what moved, what did not

**(A) Head-band withhold decisions are IDENTICAL between E68 and E69, per texel, all 8
views — exact set comparison, not a count comparison.** E69 cannot touch head-band texels
differently from E68: both regimes test the identical `dE_bg < 10.0` there (E68's own `hb`
was already `True` for every head-band texel). Measured:

| view | E68 headband-withheld set size | E69 headband-withheld set size | SET-IDENTICAL |
|---|---:|---:|---|
| 0 | 4,380 | 4,380 | **True** |
| 1 | 3,607 | 3,607 | **True** |
| 2 | 1,244 | 1,244 | **True** |
| 3 | 652   | 652   | **True** |
| 4 | 2,299 | 2,299 | **True** |
| 5 | 3,861 | 3,861 | **True** |
| 6 | 3,720 | 3,720 | **True** |
| 7 | 2,294 | 2,294 | **True** |

This is why the real joint run's own printed head-band pooled hole cost —
**649,001 / 1,186,538 (54.70%)** — is an EXACT match to E68's own recorded number: widening
scope cannot move a quantity E68 already fully owned. `logs\remap_step2_pooled.txt`.

**(B) E67's own residual-flagged population (the non-hair contamination E68 was forbidden
to touch: 593 class1 + 60 class2 + 5,193 unclassified = 5,846 pooled view-instances) is a
PROVEN SUBSET of E69's withhold, per view, all 8 views — every one of these texels gets
newly withheld, none escape.** Per-view reproduction of E67's own class breakdown, exact:

| view | residual-flagged (non-hb, relaxed, dE<10) | subset of E69 withhold | new-territory (non-hb, strict, dE<10) |
|---|---:|---|---:|
| 0 | 538   | **True** | 0  |
| 1 | 540   | **True** | 12 |
| 2 | 273   | **True** | 0  |
| 3 | 684   | **True** | 17 |
| 4 | 864   | **True** | 63 |
| 5 | 696   | **True** | 0  |
| 6 | 1,217 | **True** | 21 |
| 7 | 1,034 | **True** | 2  |
| **pooled** | **5,846** | **8/8 True** | **115** |

The pooled residual (5,846) reproduces E67/E68's own recorded 593+60+5,193 exactly. The
"new-territory" column — strict-admitted (non-relaxed, i.e. interior, not edge-proximate),
non-headband, background-colored texels — is genuinely new information this session
produced: E67's map never characterized it (it only classified the ANDON's own flagged/
relaxed population), and it is small: 115 pooled view-instances, well inside P4's
predicted low end.

## The reimplementation this measurement runs on — validated before being trusted

`project_twins.py` cannot itself produce a completed E68-regime (headband-only) or
bare-regime pooled atlas: both still halt on every view (E68's own finding, reproduced
here on view 0 as part of Gate 0/pre-edit baselines). Reused, not re-derived: E67's own
already-validated `_raw_results.pkl` (per-view `idx2`/`dE_bg`/`relaxed`/`headband`/`col`/
`bgcol`, 6/6 cross-checks against real console output, 8/8 views, per E67's own report).
Both regimes' withhold arrays were computed from it and validated, BEFORE anything
downstream was trusted, against:
- E68's own recorded per-view numbers, all 8 views, both the withhold count AND the
  residual post-withhold percentage to 6 decimal places — **8/8 exact matches**.
- This session's own real single-view run (view 0, `--bg-withhold-scope all`): 4,918 of
  436,490 (1.13%), 0.00% residual, 431,572 styled — **exact match**.

`logs\remap_step1_validate.txt`. The pooled written/hole computation built on top of this
was THEN cross-validated a second, independent way: its own E69-regime written/holes
totals (1,425,925 / 2,044,423) are an **exact match** to the real 8-view joint run's own
printed numbers, computed via a completely different path (a real completed atlas vs. a
union over 8 independently-loaded per-view arrays).

## Hole cost, honestly — three regimes, whole valid-texel universe (3,470,348)

| regime | written | holes | holes % |
|---|---:|---:|---:|
| BARE (no withhold at all) | 1,430,552 | 2,039,796 | 58.7779% |
| E68 (head-band-only) | 1,427,393 | 2,042,955 | 58.8689% |
| **E69 (whole-figure)** | **1,425,925** | **2,044,423** | **58.9112%** |

**NEW holes, E68 → E69 (the marginal cost of THIS session's widening, specifically):
1,468 texels (0.0423% of all valid texels).**

**NEW holes, BARE → E69 (total cost of both withholds combined): 4,627 texels (0.1333%)**
— exactly E68's own recorded 3,159 (head-band) + this session's 1,468 (non-head-band), by
construction (disjoint populations, arithmetic confirmed: 3,159 + 1,468 = 4,627).

Read plainly: eliminating the ANDON's entire residual population (5,846 pooled
view-instances, the whole non-hair contamination E67 mapped) costs **1,468 actual atlas
texels** — the same multi-view-redundancy absorption E68 found for hair (21,915
instance-eliminations → 3,159 actual holes), now measured for the garment-edge
population. Most withheld (view, texel) pairs are texels at least one of the other 7
cameras still reaches and does not flag.

## Where the new holes sit — by region

Two measured (not invented) spatial signals, both reusing exactly what this codebase
already computes — no colour key, no new calibration, no imported edge-distance constant.
**(1) Y-band, head-to-foot**, generalizing E68's own crown-to-neck-fifths method from the
head-crop to the whole mesh's own Z-extent in std frame (loaded verbatim per
`project_twins.py`'s own P computation, cited lines 236–263). **(2) Distance to the
head-band box**, E68's own already-validated crop-space method, reused unchanged.

| crown-to-foot band | NEW holes, E68→E69 (n=1,468) | NEW holes, BARE→E69 (n=4,627) |
|---|---:|---:|
| top fifth (crown) | 391 (26.6%) | 3,550 (76.7%) |
| 2nd fifth | 10 (0.7%) | 10 (0.2%) |
| middle fifth | 667 (45.4%) | 667 (14.4%) |
| 4th fifth | 106 (7.2%) | 106 (2.3%) |
| bottom fifth (feet) | 294 (20.0%) | 294 (6.4%) |

The BARE→E69 column is dominated by E68's own already-reported crown effect (76.7% top
fifth — E68's report: "the new holes concentrate at the crown at roughly 5× the rate of
the pre-existing baseline"); the E68→E69 column is THIS session's own marginal effect and
reads differently — a near-empty 2nd fifth between a populated top fifth and the largest
single band (middle fifth, 45.4%), plus a real bottom-fifth (feet) contribution (20.0%)
absent from E68's own head-band-scoped accounting entirely, because head-band-scoped
holes cannot occur below the neck by construction.

**Distance to the head-band box** (box diagonal 223.4px, E68's own recorded figure):

| | E68→E69 (n=1,468) | BARE→E69 (n=4,627) |
|---|---|---|
| headband membership | 0.00% (0 of 1,468) | 68.27% (3,159 of 4,627) |
| median distance to box | 406.6px | 0.0px |
| within 5% of box diagonal (11.2px) | 18.94% | 74.28% |
| within 25% of box diagonal (55.9px) | 26.23% | 76.59% |

The typical E68→E69 new hole sits at roughly **1.8× the box's own diagonal** away from
it — genuinely distant from the head, consistent with E68's own suspicion about the
unclassified population ("mostly a different phenomenon from hair spillover") and with
the charter's own visual framing: garment edge, not hair.

**Visual confirmation** (`remap\sheet\E69_widescope_withhold_sheet.png`, all 8 views):
green markers — this session's own new withhold — sit visibly at the vest's V-opening
down the chest, the collar/neckline, both sleeve cuffs, and the fingers/hand outlines on
every view that shows them; charcoal markers — E68's own head-band withhold, unaffected —
sit at the hairline/crown. Read from the image, not judged.

## Mechanism split — what kind of population produces the new holes

Of the 1,468 marginal (E68→E69) new-hole texels: **1,464 (99.7%) were, in at least one
view, part of E67's own already-characterized residual-flagged population** (class1/
class2/unclassified — declared material, true exterior, or unclassified garment edge).
**Only 4 texels (0.3%) trace to genuinely new territory** (strict-admitted, i.e. interior
rather than edge-proximate, never characterized by any prior map). Zero texels are
attributable to neither category (the two are jointly exhaustive of "non-headband,
dE_bg<10" by construction, confirmed). `logs\remap_step3_region.txt`.

**The 4 new-territory texels, individually** (a population small enough to name rather
than summarize): all 4 are accepted in **view 6 only** (yaw 270°) — no other camera
reaches them, so there is no redundancy to absorb the loss. Their `dE_bg` values sit right
at the boundary (9.10, 9.40, 9.46, 9.74 — all within 1.0 of the 10.0 cutoff, not deep
background matches). Their std-frame positions form a short, near-contiguous strip
(x≈−0.114 to −0.115, y≈−0.021, z climbing 0.2333→0.2397 in four small steps) at
y_frac≈0.73 — upper torso, not an extremity, and not head-band. `logs\
remap_step4_newterritory.txt`.

**Reading these two findings together**: the widening's cost is overwhelmingly (99.7%)
"finishing what E67 already mapped" rather than opening a large, previously-invisible
background-contamination problem. The genuinely-new population is four texels, one
camera, borderline dE, and a few tenths of a percent — not the signature of a broadly or
systematically fat silhouette.

## Which pre-registered outcome the measurement lands on

**Outcome 1** ("hole cost stays small AND the leftover set collapses"). Both conditions
measured, not asserted: the ANDON's own residual reads exactly 0.00% on 8/8 views
(complete collapse, not merely under the limit), and the marginal hole cost is 1,468
texels — 0.0423% of all valid texels, well under this session's own pre-registered
0.1%-1.0% band. **Per the charter, this seat does not open "prep can talk about a first
brush" — that is stated as available to the Director, not decided here.**

**Outcome 2's own sub-question, addressed regardless of which outcome numerically
landed, per the charter's instruction.** Is the fatness uniform or concentrated? Measured:
concentrated, not uniform — the Y-band distribution has a near-empty 2nd fifth between two
populated bands, the new holes sit at a median 1.8× the head-band box's own diagonal away
from the head (a genuinely different location, not a spillover gradient), and the visual
overlay places them specifically at garment-edge structures (vest opening, collar, sleeve
cuffs, fingers) rather than spread across open interior fabric. **Nothing measured here
resembles "the silhouette is systematically fat"** — that would predict a large, and
plausibly interior/uniform, new-territory population; what is measured is 115 pooled
view-instances collapsing to 4 actual holes, all borderline-dE, all one camera, all one
small contiguous patch. This is reported as the evidence, not as a ruling on which of the
two outcomes' framings is correct — the Director's eye and the advisor's ruling decide
what it means.

## Testing — the commit that touches the code carries its own tests

`tests/test_t98_bg_withhold_scope.py` (new, untracked), 4 tests, matching the established
T10/T11 pattern (subprocess via `run_py`, `@pytest.mark.artifacts`/`@pytest.mark.slow` for
the three that need the recorded A1 assets, one hermetic source-text check needing
neither): bare-default pinned to the recorded ANDON text; `--headband-bg-withhold` alone
pinned to E68's own recorded numbers (closes E68's own test-coverage gap as a side effect
of covering what this session adds, since both scopes share the same code path up to the
`hb` computation); `--bg-withhold-scope all` asserts P1's structural zero-residual
guarantee strictly (a code-correctness property, not an empirical number) while reporting
— not strictly pinning — its own measured withheld count, matching T11's own precedent for
a not-yet-adopted mode; and a hermetic Gate B assertion ported from this session's own
one-off script into the permanent suite. **All 4 PASS for real, against the actual tool,
22.46s** (`logs\t98_run.txt`).

**Collection-only sweep surfaced a consequence, fixed in this same commit.** Adding 4
tests moved the suite from 1,342 → 1,346 (hermetic 1,288 → 1,289; artifacts-only gap
54 → 57), which — exactly as `test_t34_front_door_counts.py` exists to enforce — broke
every pinned count-surface across the front door: `README.md` (×2 phrase sites + the
8-language digit-check leg), `SHIP_GATE.md` (2 phrase sites + its lineage chain, both the
"now" pair and the terminal element), `site/src/site-config.ts`, two handbook pages, and
`docs/advisor-kickoff.md`. All ten phrase-anchored sites and all 8 READMEs' digit
occurrences were updated in this commit. Two things worth recording about the fix itself:
`README.md`'s edit required the readme-gate hook's full-document read first (satisfied —
no other stale claim found while reading it as a product document); and the French
translation's digits use **U+00A0 (non-breaking space)** as a thousands separator
(`1\xa0342`), not a literal space or comma — a first plain-text grep found "zero"
occurrences there, which was the search being wrong, not a stale file, resolved by
inspecting the actual codepoints before editing rather than trusting the grep's silence.
SHIP_GATE.md's lineage chain gained a new terminal entry (`… → 1342 → 1346.`) rather than
having its history overwritten, per that line's own stated convention. **Re-ran
`test_t34_front_door_counts.py`: 52/52 PASS** (`logs\t34_recheck.txt`, up from 26 failed
/ 26 passed pre-fix, `logs\t34_check.txt`). **Also ran `test_t10_projection.py`** (a
different subject's own byte-identical reproduction test, unrelated to A1) for additional
confidence beyond this session's own Gate C: **PASS, 16.67s** (`logs\t10_run.txt`).

## Out of scope, confirmed untouched

No colour key (none written or considered). `--edge-dist` / W3's 7.0 literal (never
imported, never referenced). `--bg-max-pct` and `--bg-de` (both verified byte-unchanged,
Gate B). E68's head-band withhold (not reverted — proven set-identical, above). Remeshing,
regenerating the ring, starting the brush (none attempted). The palette's region boxes
used spatially (declined for the same reason E67 declined it — no calibration between
`canon/A1-palette.json`'s reference-image-space boxes and the render frame exists or is
invented here).

## Visual evidence

Per-view overlays: `remap\overlays\a1_v{0..7}_e69_widescope_map.png` — charcoal = E68's
own head-band withhold (unaffected, set-identical); green = this session's own marginal
new-withhold. Combined sheet, all 8 views: `remap\sheet\
E69_widescope_withhold_sheet.png` (1170×4186).

> The warm rim light in the twins is still paint.
> The overlay dots are still the map.

## git status, verbatim

```
On branch main
Your branch is ahead of 'origin/main' by 47 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.es.md
	modified:   README.fr.md
	modified:   README.hi.md
	modified:   README.it.md
	modified:   README.ja.md
	modified:   README.md
	modified:   README.pt-BR.md
	modified:   README.zh.md
	modified:   SHIP_GATE.md
	modified:   docs/advisor-kickoff.md
	modified:   site/src/content/docs/handbook/getting-started.md
	modified:   site/src/content/docs/handbook/reference.md
	modified:   site/src/site-config.ts
	modified:   tools/project_twins.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/experiments/E69-whole-figure-withhold-report.md
	tests/test_t98_bg_withhold_scope.py

no changes added to commit (use "git add" and/or "git commit -a")
```

`git diff --stat` (excluding this report and the untracked test file):
```
 README.es.md                                      |  4 +-
 README.fr.md                                      |  4 +-
 README.hi.md                                      |  4 +-
 README.it.md                                      |  4 +-
 README.ja.md                                      |  4 +-
 README.md                                         |  8 ++--
 README.pt-BR.md                                   |  4 +-
 README.zh.md                                      |  4 +-
 SHIP_GATE.md                                      |  2 +-
 docs/advisor-kickoff.md                           |  2 +-
 site/src/content/docs/handbook/getting-started.md |  4 +-
 site/src/content/docs/handbook/reference.md       |  2 +-
 site/src/site-config.ts                           |  2 +-
 tools/project_twins.py                            | 53 ++++++++++++++++++-----
 14 files changed, 66 insertions(+), 35 deletions(-)
```
The 47-commits-ahead state predates this session. No file inside `E:\AI\facet` was
touched this session other than the 14 modified files above, the two new files
(`docs/experiments/E69-whole-figure-withhold-report.md`, `tests/
test_t98_bg_withhold_scope.py`), and this report.

## Artifact paths

- Live handoff: `E:\AI\training\facet_E69\handoff.md`
- Predictions + outcomes: `E:\AI\training\facet_E69\logs\predictions.txt`
- Gate 0: `logs\gate0_provenance.txt`
- Gate B assertion: `logs\gateB_threshold_assert.txt`
- Gate C assertion (normalized diff, not eyeballed): `logs\gateC_nonperturbation_assert.txt`
- Pre-edit baselines: `logs\preedit_baseline_v0.txt`, `logs\preedit_baseline_v0_withhold.txt`
- Post-edit baselines: `logs\postedit_baseline_v0.txt`, `logs\postedit_baseline_v0_withhold.txt`
- Single-view widescope test: `logs\widescope_sweep_v0.txt`
- Full 8-view joint run (real tool, completes, exit 0): `logs\widescope_joint8_console.txt`,
  `bake\atlas_widescope.png` (+ `_holes.png`, `_styled_mask.npy`, `_owner.npy`,
  `_blend.png`), `bake\diag_widescope.npz`
- Reimplementation validation: `logs\remap_step1_validate.txt`,
  `remap\data\step1_withhold_arrays.pkl`
- Pooled hole-cost + set-identity: `logs\remap_step2_pooled.txt`, `remap\data\
  step2_pooled_results.json`, `remap\data\step2_new_holes_e68_to_e69_idx.npy`, `remap\data\
  step2_new_holes_bare_to_e69_idx.npy`
- Region breakdown: `logs\remap_step3_region.txt`, `remap\data\step3_region_summary.json`
- New-territory texel characterization: `logs\remap_step4_newterritory.txt`
- Overlay sheet build: `logs\build_sheet_console.txt`
- Overlays: `remap\overlays\a1_v{0..7}_e69_widescope_map.png`
- Combined sheet: `remap\sheet\E69_widescope_withhold_sheet.png`
- Test run: `logs\t98_run.txt`; T34 pre/post-fix: `logs\t34_check.txt`, `logs\
  t34_recheck.txt`; T10 sanity: `logs\t10_run.txt`; README digit fix: `logs\
  fix_readme_digits.txt`; collection sanity: `logs\collect_only.txt`
- Code diff: `tools/project_twins.py` (uncommitted, in place; `git diff -- tools/
  project_twins.py` for the literal patch)
- New test: `tests/test_t98_bg_withhold_scope.py` (uncommitted, untracked)
- Working scripts (scratchpad copies): `C:\Users\mikey\AppData\Local\Temp\claude\
  E--AI-facet\428295a0-ff4d-49f0-b0a2-024d00acf529\scratchpad\` — `e69_gate0.py`,
  `e69_gateB_assert.py`, `e69_gateC_assert.py`, `e69_step1_validate.py`,
  `e69_step2_pooled.py`, `e69_step3_region.py`, `e69_step4_newterritory.py`,
  `e69_build_sheet.py`, `e69_fix_readme_digits.py`, `e69_inspect_pkl.py`

## Role discipline

No quality judgment is offered anywhere above. The 8/8 pass result and the small marginal
hole cost are reported exactly as measured, with the mechanism traced to the texel and
both thresholds never touched (Gate B). Predictions were logged before any code edit or
new-scope run, split honestly between code-derived and blind, and every one of the five is
stated as confirmed or falsified against what was actually measured — including P3, which
this session's own prediction underestimated the smallness of. Every set-identity claim
is an exact set comparison, not a count comparison. The reimplementation this measurement
depends on was validated against real console output — E68's own recorded numbers on all
8 views, and this session's own fresh single-view and 8-view runs — before any downstream
number was trusted. Which pre-registered outcome the measurement lands on is stated
plainly (outcome 1), and outcome 2's own sub-question is answered anyway, per the
charter's instruction, without treating that answer as a ruling on what should happen
next. "Prep can talk about a first brush" is named as available, not opened — the talking,
per the charter, is the Director's. No memory write was made. No git commit was made
(fourteen files sit modified, two new files sit untracked, for the advisor to fold by
pathspec). No child agent was used for core work — the reimplementation's own validation
gates (8/8 exact matches against E68's recorded numbers, an exact match against this
session's own real single-view AND real 8-view joint run, computed two independent ways)
stand in place of a second seat.
