# E46 — the S3 run: stills, sheets, and the flow A/B

**Written 2026-08-16** by the advisor seat, after E45 landed. One dispatched executor seat
(Sonnet tier — this is execution of built instruments, not instrument design), background,
working `E:\AI\training\facet_E46\`. This document is the dispatch; steering rulings are
appended in place.

## The question

What do the eight plates compose into? E45's bundle exists; Grok's chain exists
(`s3_composite` → `s3_run` → `s3_sheet`, with `flow_estimate` for the A/B). This arc runs
it and puts the pictures in front of the Director. The three-world readout is the point:
clean composite → the 3D path degrades the plates; blotchy + high disagreement → the
sources are inconsistent (the warp lead); blotchy + low disagreement → the plates share
the defect. **No metric decides; the Director's eye does.**

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Every stage consumes committed tools at a stated HEAD, records tool sha256 + open3d/numpy versions + input hashes in a manifest per output dir; the bundle it consumes carries its own manifest (E45). |
| ANDON_AUTHORITY | 3 | Gate S: each tool's selftest runs first and its known line is read (`0.640625` / `flow_x[32,32] == 3.0` / `crop[0,0] == 200`); any mismatch halts. The tools' own internal ANDONs (crop geometry, MISSING panels) stay armed. |
| NAMED_COMPENSATORS | 3 | All writes under `E:\AI\training\facet_E46\` (not in git) + one report doc. No irreversible external call. Compensator: delete the output dirs; owner = advisor. |
| DECOMPOSE_BY_SECRETS | 3 | The seat runs; it edits no tool. Build (Grok), run (this seat), fold (advisor), judgment (Director) stay four hands. |
| UNCERTAINTY_GATED_HUMANS | 3 | The run's terminus is sheets for the Director's eye; no threshold is invented anywhere; the A/B's meaning is ruled by the advisor only after his look. |
| EXTERNAL_VERIFIER | 2 | The chain's builder (Grok) does not run it; the runner does not judge it. Not 3: no second seat re-runs the chain. Remediation: the manifests make any stage replayable one command at a time; a spot re-run of one target is the check if anything reads oddly. Owner = advisor. |

## The chain, in order

0. **Gate S (ANDON, halts everything):** run the three selftests and read their lines —
   `s3_composite.py --selftest` must print `calibration red[16,16] == 0.640625`;
   `flow_estimate.py --selftest` must print `calibration flow_x[32,32] == 3.0`;
   `s3_sheet.py --selftest` must print `calibration crop[0,0] == 200`. Any other output:
   halt and report. Also `emit_view_aovs.py --selftest` if you touch the bundle-producing
   path at all (you should not — the bundle exists).
1. **Flow fields.** `flow_estimate` on the 8 view pairs, mesh-side = depth-edge (its own
   docstring's preference now that the bundle exists), twin-side = the bundle's twins.
   Read the tool's `--help` and docstring for the CLI; read `s3_run.py`'s `--flow-dir`
   loader to match the on-disk layout it expects — **enumerate, never assume**. Output:
   `E:\AI\training\facet_E46\flow\`. Report per view: measured-pixel fraction (confidence
   above the tool's stated floor), flow magnitude distribution over measured pixels —
   numerator and denominator separately.
2. **S3 off.** `s3_run --aov E:\AI\training\facet_E45\aov --out ...\s3_off`, all 8
   targets, defaults (`alpha 6.0`, `primary_mode target`).
3. **S3 on.** Same, plus `--flow-dir ...\flow` → `...\s3_on`. **One variable.**
4. **Sheets, both arms.** `s3_sheet` with the shipped regions file
   (`tools/s3_sheet_regions.json` — its blade/grip boxes are labelled PROPOSALS; use as
   shipped, note the label in the report) over `s3_off` → `sheets_off\` and `s3_on` →
   `sheets_on\`. Heat scale: the tool's default (global per target).
5. **The A/B table.** Per region and per view, from the runs' own diagnostics only:
   disagreement mean/p90 off vs on, coverage off vs on, fallback share off vs on. No new
   measurement; numerators and denominators.

## Predictions (the seat writes its own, before step 2 runs)

Per the executor rules: before looking at any composite, state — blind status disclosed —
(a) which of the three worlds each of views 1, 2 and 7 lands in (view 2 and 7 carry the
worst measured interior warp, 8.75 / 11.12 px median; view 1 the least), with a band on
regional disagreement p90; (b) the A/B direction: whether flow-on reduces disagreement in
the high-warp regions, and by roughly what fraction, given `flow_estimate`'s measured-
pixel coverage from step 1. A prediction the instrument cannot return is the E39 trap —
compute the disagreement map's value on an identical-plates fixture and a
maximally-inconsistent fixture first if unsure of the interval (both exist in
`test_t77_s3_composite.py`'s fixtures; read, don't rebuild).

## Rules (the standing executor set)

Never judge quality — the words verified/works/decisive/proven do not appear. Halt at any
fired gate. No commits, no memory writes, no tool edits, no count-surface edits. ASCII;
absolute python path `E:\AI-Models\trellis2-env\Scripts\python.exe`; scripts create their
own output dirs; `--basetemp` on scratch for any pytest. `handoff.md` under
`E:\AI\training\facet_E46\` written first and kept current. A negative result — a chain
stage that refuses, a flow field that measures almost nowhere — is a full success,
reported plainly.

## Deliverables

`docs/experiments/E46-s3-run-report.md` (evidence only; the A/B table; the predictions
against outcomes; every number attributable to a manifest), `handoff.md`, and the output
tree `flow\ s3_off\ s3_on\ sheets_off\ sheets_on\` with manifests. The sheets are the
arc's artifact — native size, ready to put beside the shipped render.

## Dispatch record

- 2026-08-16 — dispatched at the reconciliation fold, immediately after E45 landed and
  Grok rounds 3–4 were verified and folded.
