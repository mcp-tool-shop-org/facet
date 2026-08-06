# E10 Ruling 4 dispatch — the pos.npy off-surface consumer measurement: REPORT

**Executor session, 2026-08-05.** Run under [E10 Ruling 4](E10-ruling.md)'s queued
dispatch (handoff 5, Task 1). Read-only over the route: no route tool edited, no
accepted artifact opened for writing, no accepted number presumed wrong. Predictions
were hashed blind before any measurement:
[`E10-offsurface-consumers-predictions.md`](E10-offsurface-consumers-predictions.md),
sha256 `cf16bb5552981d44228d95bda9d9d5ca9312b8d0fed94c579856137de35813ee`
(hashed 2026-08-05 20:19:51, before the first classification ran).

Tools written (diagnostics, new files):
[`tools/diagnostics/e10_offsurface_consumers.py`](../../tools/diagnostics/e10_offsurface_consumers.py) ·
[`tools/diagnostics/e10_claim_replay.py`](../../tools/diagnostics/e10_claim_replay.py) ·
artifact `E:\AI\training\facet_next\E04_stroke\e10_contact\offsurface_consumers.json`.

## The result in one line

**Every quoted headline moves at its quoted precision, and four of my six blind
predictions were wrong about the direction — the off-surface 2.5% is not inert
padding; it is disproportionately REACHABLE (3.56% of the reachable set) and PAINTED
(45.3% of the off-surface population is stage-1 styled).** Per the dispatch's
pre-registered reading: deltas reported below, **halted for the correction-in-place
ruling.** Nothing was corrected, tuned, or edited anywhere on the route.

## Anchors, all passed before any number was believed

| anchor | what it pins | result |
|---|---|---|
| A — the recorded sample | full-bake classification, restricted to `offsurface.json`'s rng(0) 200k indices and computed with that tool's own float expression, reproduces 2.5065% / 2.0940% / median 6.7310e-06 / max 147.4324188 px | **PASS, to the recorded digits** |
| B — the ceiling | replica of `e08_ceiling`'s reach at the ship's ruled floors reproduces the recorded reachable count | **PASS: 1,329,359 exactly** |
| C1 — the classes | stage-1 / brush / dilation reconstructed from native sidecars reproduce `provenance.json` | **PASS: 1,147,959 / 213,852 / 1,750,006 exactly** |
| C2 — the strokes | per-stroke replay with the A32 hit-intersect reproduces all six recorded commits | **PASS: 26,531 / 22,766 / 17,904 / 24,486 / 63,288 / 58,877 exactly** |

Three replica corrections were needed to reach those anchors, each with a readable
signature, each moving the replica toward the recorded number (never past it):

1. **`texel_provenance.py`'s replay predates Amendment 32.** Run as shipped against a
   state COPY, it over-claims every stroke (+6/+118/+148/+25/+5/+56, total +358; the
   358 lands in dilation) — the exact signature of the missing `fm_e & hit`
   intersect, since each extra texel is one commit refused as "keyed on no surface."
   The A32-faithful replay (`e10_claim_replay.py`) anchors all six exactly. **The
   shipped route is untouched by this; it is a fidelity note about the diagnostic**,
   flagged for the advisor (its replay reproduces pre-A32 commits, not the ship's).
2. **The ship's ceiling is the uniform-0.45 configuration.** A first replica at W3's
   production split (body 0.45 / head 0.18) reached +67,172 too many — the W3-lineage
   head band's looser floor, which `ship.json` deliberately makes inert
   (`head-facing-min = 0.45`, Ruling 14). At the ship's ruled floors the replica
   lands exactly.
3. **Two float orderings of one conversion live in the codebase.** `e10_offsurface.py`
   computes `(lo + pos*(hi-lo)) * (0.5/maxabs)`; every route consumer computes
   `(pos*(hi-lo) + lo)/maxabs * 0.5`. Additionally, per-point distances wobble in the
   last float digits with query batch composition (~3e-6 px at the sample max — the
   recorded max reproduces exactly when the sample is computed as its own batch, as
   the source tool did). Threshold classifications are insensitive (the 1 px
   threshold is ~10^3 × the wobble); the anchor is computed with the source's own
   arithmetic; the exclusions use the consumers' own.

## The measurement

Full-bake classification (no sampling, all 3,111,817 uv-valid texels; frames named:
unit-cube pos → canonical mesh frame, 1 px = 0.0011216247 canonical units):

```
OFF-SURFACE (>1 px): 77,693 = 2.4967%     (>5 px): 64,767 = 2.0813%     max 149.3 px
```

(The recorded 2.5065% was the 200k sample's estimate of this number; the full count
is inside its sampling noise — prediction P6 confirmed.)

### Per consumer: recorded → excluding the off-surface population

"Excluding" removes off-surface (>1 px) texels from numerator and denominator, per
the predictions doc's fixed definition.

| consumer | headline as recorded | excluded | delta | moves at quoted precision? |
|---|---|---|---|---|
| `e08_ceiling` reach/valid | 1,329,359 / 3,111,817 = **42.7197%** (quoted 42.72) | 1,282,028 / 3,034,124 = 42.2536% | **−0.4661 pts** | **YES → 42.25** |
| `e08_acceptance` styled/valid | 1,147,959 / 3,111,817 = **36.8903%** (quoted 36.89) | 1,112,789 / 3,034,124 = 36.6758% | **−0.2145 pts** | **YES → 36.68** |
| `e08_acceptance` styled/reachable | **86.3543%** (quoted 86.4) | 86.7991% | **+0.4448 pts** | **YES → 86.8** |
| `texpass_finalize` dilation/valid | 1,750,006 / 3,111,817 = **56.2374%** (quoted 56.24) | 1,712,332 / 3,034,124 = 56.4358% | **+0.1984 pts** | **YES → 56.44** |
| `project_twins` stage1/valid | same operands as acceptance styled/valid | 36.6758% | −0.2145 pts | YES |
| `texpass_iter` brush/valid | 213,852 / 3,111,817 = **6.8723%** (quoted 6.87) | 209,003 / 3,034,124 = 6.8884% | **+0.0162 pts** | **YES → 6.89 (last digit)** |

Per-stroke (anchored replay; recorded → excluded, loss):

```
stroke 1  y+300_e+00   26,531 -> 24,368   loses 2,163 = 8.15%   <- the outlier
stroke 2  y+030_e+00   22,766 -> 22,384   loses   382 = 1.68%
stroke 3  y+150_e+00   17,904 -> 17,830   loses    74 = 0.41%
stroke 4  y+240_e+00   24,486 -> 24,256   loses   230 = 0.94%
stroke 5  y+000_e+40   63,288 -> 61,735   loses 1,553 = 2.45%
stroke 6  y+180_e+40   58,877 -> 58,430   loses   447 = 0.76%
```

Scoping fact for `texpass_finalize`: the shipped galleon finalize ran
`"mode": "atlas_flood"` — its `pos.npy`-consuming branch (surface-aware, line 82)
**did not execute on this asset's shipped run**. The 56.24% headline is still the
dispatched question and is answered above; the consumer's pos-reading code path has
not yet run on this subject.

### Where the off-surface population actually lives — the finding

| class | off-surface texels | share of the off-surface population | off-surface rate within the class |
|---|---|---|---|
| stage-1 styled | 35,170 | 45.27% | 35,170 / 1,147,959 = **3.06%** |
| brush | 4,849 | 6.24% | 4,849 / 213,852 = 2.27% |
| dilation | 37,674 | 48.49% | 37,674 / 1,750,006 = **2.15%** |
| *(reachable)* | *47,331* | — | *47,331 / 1,329,359 = **3.56%*** |

Population baseline: 2.4967%. **The painted and reachable classes carry the
off-surface property at a HIGHER rate than the never-painted dilation class.** My
blind P0 predicted ≥85% of the population in dilation on the "inert gutter"
mechanism; measured, less than half is. An off-surface position was no obstacle to
passing facing + visibility + edge + mask on this route — 35,170 texels in the
accepted atlas's stage-1 set carry positions that are not on the geometry.

## Predictions scored (all six were hashed blind)

| # | predicted | measured | verdict |
|---|---|---|---|
| P0 | dilation ≥85% of off-surface population | 48.49% | **FALSIFIED** |
| P1 | ceiling UP to ~43.4 | DOWN to 42.25 | **FALSIFIED in direction** |
| P2 | styled/valid UP to ~37.4; styled/reachable 86.2–87.0 | 36.68 (down); 86.80 | **first FALSIFIED in direction; second inside range** (direction uncertainty was disclosed) |
| P3 | dilation DOWN to ~55.4 | UP to 56.44 | **FALSIFIED in direction** |
| P4 | stage-1 loses ≤8,000 | loses 35,170 | **FALSIFIED, 4.4×** |
| P5 | each stroke loses <2.5% | strokes 1 and 5 lose 8.15% / 2.45% | **FALSIFIED for stroke 1** |
| P6 | full-bake 2.51 ± 0.06 | 2.4967 | confirmed |

A negative result is a full success: the falsifications are the content. The
mechanism I predicted (unreachable padding) is not what this population is.

## What is NOT established (unchanged from the finding, plus one line)

- Where the off-surface positions come from (`bake_hero_prep.py:458` remains the
  unread suspect) — not this dispatch's question.
- Whether any of this is visible in either accepted asset — both stand accepted on
  the Director's eye; nothing here re-opens that gate.
- Whether any correction is warranted anywhere — that is the ruling this report
  halts for, per the dispatch's own pre-registration.
- One denominator note for the record: `E04-h4-ceiling.md` quotes valid = 3,111,832;
  the mask on disk measures 3,111,817 (as `provenance.json` and `offsurface.json`
  record). Both yield 42.72% at 2 dp, so no quoted figure turns on it; the 15-texel
  discrepancy is reported, not diagnosed.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | predictions hashed before measurement (sha in header); every anchor pinned to a recorded artifact; frames named at each conversion; the JSON carries the predictions hash |
| ANDON_AUTHORITY | 3 | four anchors, each halting the tool on miss; two fired during bring-up (sample max, ceiling floors) and the run stopped each time; the classification threshold was never adjusted |
| NAMED_COMPENSATORS | 3 | writes: two new diagnostic files, one JSON in `e10_contact/`, scratch copies outside the repo. Undo = delete them. The shipped state was copied before any replay wrote near it |
| DECOMPOSE_BY_SECRETS | 2 | replay and consumer-measurement are separate files with one purpose each; the claim replay duplicates commit's chain by necessity (reported as such) rather than importing it — the canonical-frame bundle item would remove that duplication |
| UNCERTAINTY_GATED_HUMANS | 3 | the dispatch's pre-registered reading is applied verbatim: numbers moved → deltas reported → halted for the ruling; no recommendation is made |
| EXTERNAL_VERIFIER | 3 | the classification was verified against the recorded sample computed by a different tool; the class reconstruction against `provenance.json`; the replay against the recorded commits — every recompute is checked against an artifact this session did not produce |

**Reported, not ruled. Task 1 halts here for the correction-in-place ruling.**
