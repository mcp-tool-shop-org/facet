# E34 ruling — projection coverage on the performer

**Seat:** advisor · **Ruled:** 2026-08-13 · **Spec:**
[E34-projection-coverage-kickoff.md](E34-projection-coverage-kickoff.md) ·
**Predictions:** [E34-predictions.md](E34-predictions.md) ·
**Report:** [E34-projection-coverage-report.md](E34-projection-coverage-report.md), executor
commit `7c39d92` (three files: report, predictions, the eight-view prompt JSON).

This seat did not run the experiment and does not judge the artifact. **The Director's eye
rules the repair, on the sheets and the candidate GLB at his own zoom; this document rules on
what the measurements mean and what the repo does next.** The acceptance question is held
open at the end, deliberately.

## 0. What this seat verified before ruling

Resolved independently against the tree and the instruments' own output files, not against
the report's prose:

| claim | verdict |
|---|---|
| candidate exists, recorded asset untouched | **CONFIRMED** — `performer_textured_8view.glb` sha256 `ce793064…`, 22,284,208 bytes; the recorded `performer_textured.glb` re-hashed at this seat: `9e20ea7d…`, 21,588,628 bytes, byte-unchanged |
| fill headline | **CONFIRMED from `out/finalize.json`** — `hole_texels` 157,228 · `painted_texels` 2,287,542 · `dist_median_edges` 1.822 · `dist_beyond_pct` 0.333 · `mean_fallback` 0 |
| registration diagnostic | **CONFIRMED from `twin_registration.json`** — eight rows in view order, mirror silhouettes exact (91,207 = 91,207 · 56,254 = 56,254 · 91,082 = 91,082); the two `SUSPECT`s are the ratio leg on exactly the two profiles (Ruling 7a) |
| T24 red at HEAD | **REPRODUCED** — fails on `E34` with the executor's message, at a tree containing only pushed commits |
| the failing pattern's site | **RELOCATED one level deeper than the report** — `PAID_RE` greps nowhere in `tools/facet_index.py`; it is built from `docs/index/conventions.json:237` (`laws.paid_for_by`) and re-exported via `BINDING.exports()` (Ruling 3) |
| T41 axis-D | **FIRED AT THIS SEAT** — five files stale, all of them the report's own citations (Ruling 4) |
| the sheets | **WALKED at full size** — `E34_before_after_controlled.png` and `E34_poles_regression.png`; the executor's three observations are all real and visible |
| spend | **RE-READ at ruling time** — the 23:00–24:00Z GPU-hours bucket has posted: **$0.110647**, the only GPU-hours entry in the execution window (Ruling 5) |

## Ruling 1 — Conduct: accepted, and three of its catches were the advisor's defects

The arc ran gate-clean: 6 of the 8-job ceiling, 0 re-rolls, 0 failures, no threshold moved,
both manifests 0/0/0 at open **and** close, and the halt landed at the report with nothing
pushed — exactly the compensator table's assignment.

**G1 is the arc's exemplary work.** All three enumerations recovered with zero commissions,
and the third by the strongest method available: E33's projection invocation was never
written down, so the executor settled `--aspect` **arithmetically** off `frame_300k.json`'s
`coverage_world` ratio (0.34375 = 352/1024 exactly), then **replayed the whole two-view run
and reproduced every recorded number to the digit with `stage1_styled_mask.npy`
byte-identical**. Premise 5 moved from ASSUMED to MEASURED by proof, not by assertion. The
control builder was identified the same way — `restylize_views.py --emit-only` rebuilt E33's
view-0 control to the recorded sha256.

Three catches are owned here as this seat's spec defects:

1. **The `--max-frac-beyond` transcription.** The spec wrote "5.0" where the flag's unit is
   a share — 0.05 *is* the recorded 5%. Passed literally it sets a 500% bound and **silently
   disarms a finalize gate**. The executor read the tool before passing anything. A spec
   that transcribes a rendered percentage into a flag value writes a different gate than the
   recorded one.
2. **"The six named landmarks."** The record names **five** landmarks (jaw, temple,
   shoulder, ribcage, flank) across **six** affected views; the spec conflated the two
   populations. The unit family's smallest member, in the dispatch's own prose.
3. **The missing span bump** — Ruling 3, the largest of the three.

**The render-confound handling is ratified as model behavior.** The first before/after sheet
showed the candidate darker and less hatched — a material-scale claim. E33's `turn_final`
invocation was never recovered, so render settings were an uncontrolled variable; the
executor measured texture space directly (mean luma 112.82 vs 112.73 — same material),
re-rendered **E33's recorded GLB through the identical call**, and rebuilt the comparison.
The confounded sheet stays in the record beside the controlled one. A finding that dissolves
under a controlled re-render was a property of the instrument, not the asset — caught before
it reached anyone's eye as a claim.

## Ruling 2 — The repair, at the measurement level: VERIFIED. Acceptance stays the Director's.

| quantity | E33 (2 views) | E34 (8 views) |
|---|---|---|
| holes into finalize | 927,492 (37.9% of valid) | **157,228 (6.4%)** — −83.0% |
| styled / valid | 62.1% | **93.6%** |
| styled / reachable | 84.2% | **98.4%** (reachable itself 73.7% → 95.1%) |
| DILATION largest 4-connected component | 22,457 | **7,390** |
| finalize source distance, median | 2.974 edges (limit 3.0, margin 1%) | **1.822 edges** |
| beyond 20 edges | 1.024% (limit 5%) | **0.333%** |

Total **and** largest component fell together — [E28 Ruling 21](E28-ruling.md)'s
two-number form doing precisely what it was built for: this is neither one patch shattered
into speckle nor speckle cleared around a surviving patch. The two pole views reproduce
their E33 numbers **to the digit** (reg-IoU 0.8605/0.8475, styled counts, erosion strata,
both background probes) — six added cameras perturbed neither recorded view. `--reg-iou-min
0.80` did not fire anywhere; the minimum across eight views is 0.8475, **at a pole**.

Two diagnostics are placed in context so nobody later reads them as regression signals:
`normal_disagree_gt60` rose 8.47% → 26.62% and back-facing 4.96% → 19.94% — the expected
consequence of adding six oblique cameras, on a quantity [E07](E07-ruling-gate1.md)
classified as a **diagnostic whose proxy inverted**; the gate is the measured source
distance, which improved on both legs.

**What this ruling does not touch:** whether the repaired views are acceptable. The patches
read closed at every named landmark on the controlled sheet at this seat's walk — and this
seat's walk is not the gate. Three observations ride to the Director's eye as observations:
the candidate's surface reads smoother with less of the fine sculpted hatching; the brow/eye
region on views 1/7 is more defined (their twins carried the face terms); a faint vertical
tonal boundary runs down the back of the head and neck on views 3/5.

## Ruling 3 — T24: the dispatch commit's own miss, repaired one level deeper than the report's site

The report attributes the failing pattern to `facet_index.PAID_RE` and proposes a
one-character edit to `tools/facet_index.py`, declining to make it because that is published
tool code. **The attribution is one level too shallow, and the caution was right for a
reason the report could not see.** Measured at this seat: `PAID_RE` appears **nowhere** in
`tools/facet_index.py` as source text. Since the record-index extraction, that module is an
adapter — the regexes arrive at line 60 via `globals().update(BINDING.exports())`, and the
pattern's source is **`docs/index/conventions.json:237`**, the declared field
`laws.paid_for_by`. The executor measured the runtime attribute honestly and named the
attribute's module; *the attribute is a surface, the declaration is the source* — the
sibling of E32's *a name-based search is not an enumeration*, on the read side.

Consequence: the repair is **not** a tool change at all. It is facet's own declared
vocabulary — exactly the class this repo already moves deliberately under a test (T31's
`REMAINING_ELSEWHERE`, T41's census pins), and T24's own docstring says why the bound
exists: *"the second leg below is what makes the next arc's bump a deliberate edit rather
than a silence."* **The defect is that the dispatch commit (`73a202c`, this seat's) created
E34 in the record while the declaration still said E33** — the suite has been red at every
tree containing E34 since, for the arc's whole duration.

**Ruled:** the span is bumped in this ruling's fold (`E3[0-3]` → `E3[0-4]`), T24 goes green,
and the procedure lands in the kickoff where the next dispatching seat will read it: **the
commit that creates E(n) bumps the declared span.** No CLAUDE.md text — the governing law
(*a count under a test moves deliberately in the commit that earns it*) already exists; this
is an instance, not a new law. The executor's report-not-fix was correct under its own
reading and correct under this one: attribution of a red suite is a ruling call either way.

## Ruling 4 — T41: the census was stale at HEAD by the report's own citations

`test_t41_axis_d_is_idempotent_across_runs` fired at this seat: five files' axis-D counts no
longer reproduce — `e12_canny_derive`, `e12_make_twin_prompts`, `e14_twin_registration`,
`texel_provenance`, `turn_render` — **all five are files the E34 report cites.** Third
recorded instance of the arc's-own-paper family ([E28 F10](E28-ruling.md), [E32 Ruling
8](E32-ruling.md)). The mechanism is temporal: the executor's full suite ran **while the
report was being written**, so its T41 pass was true of the tree at collection time and
false of the tree at commit time — [E26](E26-ruling.md)'s law (*a worktree answers what your
change produces, not what the tree you commit to contains*) in temporal form: **a suite run
concurrent with authoring answers the tree at collection, not the tree at commit.**

Remedy standard and executed in this fold: census regenerated by its own tool, T41 green. No
new gate is commissioned — T41 caught it at the next seat, which is the instrument working
as designed. The report's "count surfaces do not move" claim was true of the surfaces it
named (T34's pins, all test counts); the census was the count surface outside its check.

## Ruling 5 — P7 resolved at ruling time, and E33's per-job figure is revised down

The 23:00–24:00Z GPU-hours bucket has posted: **$0.110647** — the only GPU-hours entry in
the window containing the six jobs (~23:12Z), with nothing after it through the report
horizon. Stated in the only honest form: **the arc's six jobs cost at most $0.110647 —
≤ $0.0184/job** ("at most" because same-day workspace non-exclusivity was *observed*, not
merely unprovable, at the executor's before-read).

This revises E33's figure. E33 §8 measured **$0.612951 for six jobs of the identical shape**
as a whole-day-bucket delta and said itself that exclusivity was not proved. Six identical
jobs now measure 5.5× cheaper in a bucket with no competing entry — so E33's $0.102/job was
an **unattributed upper envelope carrying roughly $0.50 of somebody else's work**, exactly
what its caveat warned. **Future specs bound a Qwen 20-step 352×1024 ControlNet job at
~$0.02–0.03 and cite E33's figure only as the envelope it declared itself to be.** The
spec's premise 7 was conservative 5×, in the harmless direction.

## Ruling 6 — Predictions: the self-scoring stands, and the family gains its sharpest member yet

5 miss / 3 hit as scored, no band moved after the fact. The one-mechanism reading is
ratified: P1–P5 all failed through a single fitted parameter — **the twin-registration model
was fitted on the only two views the record had ever measured, and those two (the poles) are
the outliers.** The profiles the model predicted worst (0.70–0.82, ~70% confidence of a gate
firing) are the best-registered views in the set (0.9479 / 0.9349, centroid offsets 1.6 /
3.4 px against 30.4 / 33.2 at the poles); the pole-specific fatness-and-drop was read as a
global generator property. The unit/population family gains the member *a parameter fitted
on the only measured members, when those members are the outliers* — with the P6 corollary
worth its own clause: **the erosion-cost stratum table swings with registration quality**,
so a "recorded baseline" from a pole is not a baseline for a profile.

One bookkeeping note, recorded because it is itself a tiny instance of the family: the
report calls this the *tenth* consecutive arc; [E32 Ruling 5](E32-ruling.md) already claimed
tenth and E33 went unnumbered. The ordinal has drifted — an asserted count whose population
nobody re-enumerated. The member list is the record; the ordinal is retired from use.

P8 (finalize margins, from mechanism rather than extrapolation) hit both clauses. P9 (poles
+ recorded-asset regression) held on both. P10 (largest component < 60,000) hit at 7,390.

## Ruling 7 — Instrument observations, recorded with dispositions

* **(a) The two keys disagree about profile extent.** `e14_twin_registration`'s ring-fit
  key reads the profile twins 250/272 px wide where the projection's own registration reads
  138/160 — 1.8–1.9× — while area-IoU stays ≥ 0.91: stray keyed *extent*, not area. Its
  `SUSPECT` leg fires on exactly the two narrowest views (the global-constant-on-a-local-
  feature shape, as E33 §10 measured). Suspended diagnostic, gates nothing, repair remains
  out of scope. Anyone reading `twin_registration.json` reads bbox columns with this note.
* **(b) The served `texel_provenance` refuses an empty stroke order; its instrument handles
  one.** A strokeless asset is a legitimate route state this record now contains twice (E33's
  delivered asset, E34's candidate). **Commissioned:** the wrapper accepts an explicitly
  empty order, with a can-fail test, in the next commit that opens `measure_mcp.py` — not
  built here, and T-numbers for it come from the namespace then current.
* **(c)** The mirror-corroboration pairing is positional (`rows` by index, `((0,4),(1,5),
  (2,6),(3,7))` at line 117) and was verified at its eight-row design case before any of its
  lines were read — the E33 six-label crash was the off-design case, not a quirk.
* **(d)** E08 gotcha 8, third sighting and first on the **output** side: returned blob names
  are not the sha256 of the bytes received. Recorded so a future byte mismatch is not
  attributed to the wrong cause.

## Ruling 8 — What remains, and the sequence on the Director's word

**Open to his eye, now:** `E34_before_after_controlled.png` and `E34_poles_regression.png`
at full size, and the candidate GLB at his own zoom. The question the report ends on is the
right one: whether **157,228 dilation-filled texels, the largest single patch 7,390**, are
acceptable as dilation — or whether the residue redirects to the R3-brush design question,
which was held out of this arc's scope on purpose.

**On acceptance:** the `facet_E34` tree gains a manifest and protected status; anchor tests
for the candidate are commissioned (the spec's out-of-scope note routed them to this
moment); the status row closes; and armature's re-survey — its hole survey and RGBA-true
turnaround against the candidate — runs **on his word**, at zero credits, as the standing
support offer. A hosted-tier revalidation (an E13-shaped generation at the same landmarks)
remains **his pricing decision and is not assumed**.

**Not touched by this ruling:** the brush stage and its R3 configuration; E30's W3
era-flag re-run (unspent); the queued correctness items (`anchor_check`/PIL, the identity
envelope's dependency set, archive-to-`D:`); every accepted asset.

## This ruling's own error record

Three advisor defects surfaced by this arc, owned above: the `--max-frac-beyond` unit
transcription that would have disarmed a gate (Ruling 1); "the six named landmarks" conflating
views with landmarks (Ruling 1); and the missing span bump that left the suite red for the arc's
duration (Ruling 3). All three were caught by the executor or by an instrument — none by this
seat's own reading — which is the calibration fact worth keeping.

---

# Addendum — ruled 2026-08-13, after the sheets reached the Director

## Ruling 9 — The Director's acceptance closes the arc

**The Director accepted the repair on the controlled before/after sheet and the poles
regression sheet, conditional on the full suite; the condition is met** — the suite is green
at this seat on the folded tree, **927 passed, 0 failed** (657.93 s, exit 0), T24 and T41
included with their repairs. **E34 is CLOSED — ACCEPTED.**

What the acceptance settles and sets in motion:

1. **The accepted artifact** is
   `E:\AI\training\facet_E34\out\performer_textured_8view.glb` (sha256
   `ce7930643e573b475737eca676d9118b036d5e131c8b7af66a65b3b7ae0113c5`, 22,284,208 bytes) —
   the fifth accepted asset on this route, and the first produced as a **repair of
   another**. The E33 recorded asset stays in the record byte-unchanged as the pre-repair
   state; nothing supersedes it as E33's delivery.
2. **`facet_E34` is manifested and protected**: `E34_manifest.json` — **84 files,
   177,563,094 bytes, self-excluded by construction** (E33's manifest records itself at a
   byte size a later regeneration falsified, and the E34 executor had to explain that entry;
   excluding the manifest from its own listing is the E28 self-reference remedy applied at
   write time). The tree is read-only to future arcs and manifest-gated at their open and
   close, beside `facet_E33`.
3. **The residual dilation is accepted for this asset** — 157,228 texels, largest component
   7,390, ruled acceptable by the eye that governs. The R3-brush design question therefore
   **parks** rather than being commissioned; it returns only if a future subject's residue
   fails the same eye.
4. **Candidate anchors are commissioned, T66+** — the finalize replay at the byte tier and
   the recorded values loaded from `finalize.json` (the T50–T57 form), routed to the next
   executor errand; the count surfaces move with them under T34's pins when they land.
5. **armature's re-survey is unlocked** — its hole survey and RGBA-true turnaround against
   the accepted GLB, in armature's seats, at zero credits, on the Director's relay. A
   hosted-tier revalidation remains his pricing decision and is not assumed.

The status row closes with this ruling; the index pair rebuilds in the terminal commit.
