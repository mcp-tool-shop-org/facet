# E47 — the atlas 2×2, rendered

**Written 2026-08-16** by the advisor seat, at the fold that closed E46 and landed Grok
rounds 5–6. One dispatched executor seat (Sonnet tier — execution of built instruments),
background, working `E:\AI\training\facet_E47\`. This document is the dispatch; steering
rulings are appended in place.

## The question

E46 answered in image space: flow-on reduced cross-view disagreement on **18 of 18
measured (view, region) rows, zero exceptions**. The Director's standing rule is that an
arc ends with a picture beside the current one — and the current one is a **render of the
atlas**. This arc rebuilds W3's atlas from the bundle in the full 2×2
(`--mode owner|blend` × flow off/on), renders all four beside the shipped render, and
puts the sheets in front of the Director. Grok's round-5 argument, accepted: owner hides
disagreement by construction, so the four cells discriminate four different things —
winner-colour movement (owner off/on), mix cleanup (blend off/on), WTA-vs-mix share
(owner vs blend at off), and post-correction convergence (owner vs blend at on).

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Committed tools at a stated HEAD; every output dir carries a manifest (input hashes, tool sha256s, numpy/open3d versions, parameters, HEAD). The flow fields are CONSUMED from `E:\AI\training\facet_E46\flow\` with their manifest — never regenerated. |
| ANDON_AUTHORITY | 3 | Gate S selftest lines read before anything runs; the tool's own `--anchor` run against real data before any paint; the tool's internal ANDONs stay armed. |
| NAMED_COMPENSATORS | 3 | All writes under `E:\AI\training\facet_E47\` + one report doc. No irreversible external call. Compensator: delete the output tree; owner = advisor. |
| DECOMPOSE_BY_SECRETS | 3 | Build (Grok) / run (this seat) / fold (advisor) / judgment (Director), four hands. The seat adds NO repo files except the report; glue scripts live in the training dir. |
| UNCERTAINTY_GATED_HUMANS | 3 | No threshold anywhere; the terminus is sheets for the Director's eye. |
| EXTERNAL_VERIFIER | 2 | Builder does not run; runner does not judge. Not 3: no second seat re-runs. Remediation: manifests make every cell replayable in one command; a spot re-run is the check if anything reads oddly. Owner = advisor. |

## The chain

0. **Gate S (ANDON):** `atlas_from_aovs.py --selftest` must print
   `calibration atlas[16,16,0] == 0.5`; then its real-data anchor:
   `--anchor --aov E:\AI\training\facet_E45\aov --prep E:\AI\training\facet_E06\C1\prep`
   must report |bmid| at 0.000e+00 and the valid-texel count (recorded precedent:
   2,402,810). Any other output: halt and report.
1. **The four atlases.** `atlas_from_aovs` × {owner, blend} × {no flow,
   `--flow-dir E:\AI\training\facet_E46\flow`}. Same command otherwise — the manifests
   must differ ONLY in mode and flow-dir. Report per cell: coverage (written / valid,
   numerator and denominator), sentinel share.
2. **The renders.** Swap each atlas into the shipped GLB and render flat — the recorded
   precedent for atlas-swapped rendering is `E:\AI\training\facet_E42\render_blade_mask_atlas.py`
   (read it; reuse its mechanism with citation). Render the 8 turn views flat
   (`turn_render.py --flat` conventions), plus the shipped render for the same views
   from `E:\AI\training\facet_E08\ARMB\out\renders_flat\final_i.png` (recorded — do not
   re-render the shipped asset; consume the recorded artifacts).
   ⚠ Blender through PowerShell only, `-b -P` only. The sentinel (magenta) will show on
   unwritten texels in ALL four cells equally — that is by design; say so in the report.
3. **The sheets.** Per view (at minimum views 1, 2, 6, 7 and one elevated-content view
   if legible): `shipped | owner-off | owner-on | blend-off | blend-on`, native pixels
   or integer zoom, provenance captions, plus blade/grip crops at the Director's zoom
   (region boxes from `tools/s3_sheet_regions.json` — labelled PROPOSALS there; carry
   the label). Use `s3_sheet.py` if its contract fits the panel set; otherwise a
   minimal composer in the training dir — never a new repo tool.
4. **The A/B numbers**, from the atlases directly: per-texel |Δ| between off and on per
   mode (mean/p90 over co-written texels, numerator and denominator), share of texels
   whose owner changed (owner mode), per-region summaries for the blade and grip boxes.

## Predictions (the seat's own, written before step 1 runs, blind status disclosed)

Per cell of the 2×2: whether the off→on render difference is visible at the Director's
zoom on the blade and grip, with a band on per-texel |Δ| p90 — conditioned on E46's
measured flow coverage (16–27% of silhouette) and magnitudes (median 1.4–3.2 px). State
what the instrument reads if flow changes nothing (identical atlases, |Δ| = 0) and if it
changes everything it can reach (bounded by flow coverage × sampled-colour variance) —
predict inside that interval.

## Rules (standing executor set)

Never judge quality; halt at any fired gate; a negative result is a full success; no
commits, no memory writes, no tool or test or count-surface edits; the ONLY repo file
you create is `docs/experiments/E47-atlas-ab-report.md`; `handoff.md` under the training
dir first and current; ASCII; absolute python `E:\AI-Models\trellis2-env\Scripts\python.exe`;
scripts create their own output dirs; read listings complete; manifests everywhere.

## Deliverables

The report, the handoff, four atlas dirs + renders + sheets with manifests. The sheets
are the arc's artifact — the Director's eye is the gate, and no metric substitutes.

## Dispatch record

- 2026-08-16 — dispatched at the E46/rounds-5-6 fold.
- 2026-08-16, late — seat landed; report folded at `8093833`; Gate S held; two
  prediction misses reported (flow-on drops coverage 12/12 cells; blend moves more
  texels at smaller magnitude).
- 2026-08-16, close — **DIRECTOR'S RULING: all four cells REJECTED.** His words: He could see no recovered imagery in any of them. The advisor's walk had
  reported interior-material recovery with boundary residue and called blend-off "the
  closest thing to the reference this pipeline has ever rendered" — **that sentence was
  a quality grade, which is not the advisor's call, and it is withdrawn.** What stands
  measured: the rebuilt atlases differ from the shipped one in the direction of the
  reference *inside material regions*, and every cell is covered in unfilled-sentinel
  lace and patch seams at boundaries — a diagnostic, not a candidate. An image is
  broken if any of it is. Follow-on: E48 produces a COMPLETE candidate render (trust
  erosion + island-aware fill + whole-figure render) so the next artifact judged is an
  asset, not an A/B instrument. If E48 also fails the Director's eye, this route is
  dead at his word and the from-scratch question reopens with the advisor arguing
  neither side.
