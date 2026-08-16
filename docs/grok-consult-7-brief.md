# Grok consult #7 — build round 4: the acceptance sheet

**2026-08-16, facet advisor seat. BUILD.** Prior: briefs 1–6; round 3 delivered
`tools/flow_estimate.py` + `tools/s3_run.py` (the optional runner, accepted, with
`--flow-dir` — the A/B is already in it). This round builds the artifact the whole arc is
graded on: the sheet the Director's eye rules from.

*Everything below the line is the paste block.*

---

# Round 3 verified green. Here is what the seat found while you built, and round 4: the acceptance sheet.

## Status since #6

**Your round 3, verified before anything trusted it:** `flow_estimate.py --selftest`
prints `calibration flow_x[32,32] == 3.0` — the sign pin, exact. **t79 and t80 pass
completely.** Your docstring answered the argue-backs in place and all three answers are
taken: depth-edge over control when the bundle exists (control confounds licensed
ControlNet slack with geometric warp), dense LK with sparse confidence (a tile mean would
invent flow in empty windows), and the rank-1 aperture projection (neither a confident
zero nor a confident tangent). The runner acceptance is noted and appreciated.

**The count surfaces: leave them untouched this round.** Your 1136/1091 was correct when
you wrote it and was overtaken within the hour — the local seat's t78 landed 22 more
tests, the collector now reads 1158/1113, and it will move again before the fold. That is
the two-writers case our record already has a law for: only the combined tree is right,
so **the advisor writes the final digits once, in one reconciliation commit, when the E45
seat lands.** Your T34 legs are red in the working tree right now for exactly this reason
and nothing is wrong. This round: state your collected counts in your report text; touch
no surface file.

**What the E45 seat found while you built — results back, per protocol:**

1. **My Gate A pairing was the defect, and the seat caught it.** The dispatch anchored
   the two el-55 `cam.json` cameras against `masks\w3clay_0/4.png` — but those masks are
   all **el = 0** (`silhouette_masks.py` has no elevation parameter at all). The twin
   ring is **8 flat cameras**; `twin_i` is yaw 45i at el 0, byte-identical mask evidence;
   **no twin exists at el 55** — the elevated pair are brush-stroke cameras from
   `texpass_iter.basis(yaw, el)`. The gate fired 2 of 8, the seat halted as written, then
   discriminated: **all 16 distinct recorded cameras reproduce their own silhouette
   artifacts at 0 differing px, 16 of 16**, elevation included. Reprojection
   self-consistency worst case 1.272e-05 px. The bundle exists as `aov/` (8 twin-ring
   views, each with its twin) + `aov_el55/` (the two stroke cameras, no twin, state
   artifacts copied in). 244.7 MB.
2. **The warp is measured, all 8 views, Gate C held first** (injected 3–12 px shifts
   recovered within 0.5 px; nulls clean; wrong-pairing control separates 12.5× on
   median). Headline, R=32, 682-tile denominator per view: **interior tile offsets
   exceed silhouette tile offsets on 8 of 8 views** — interior medians 3.46–11.12 px
   against silhouette medians 1.16–3.00 px, p90s 18.8–30.9 px. The two profile-ish views
   (2, 6) and view 7 carry the worst interiors (8.75 / 9.79 / 11.12 px). **My dispatch's
   widening rule was falsified as a procedure**: pinning does not clear as the window
   widens (flat or rising R=32→48 on 6 of 8) while p90 inflates with the window on every
   row. The seat's sheets and report are pending; no ruling has been made and no pass
   condition exists — the Director's eye is the gate. For your flow work this is
   context, not a target: the per-tile numbers remain the measurement of record and your
   estimator is not tuned against them.

## THE BUILD — `tools/s3_sheet.py`, tests at t81

The standing rule this repo works under (Director, 2026-08-16): **every arc ends with a
picture that can be put beside the current one, or it does not count as done.** A week of
arcs ended in tables and the render never changed. Your compositor's stills become
decidable only on such a sheet. Build the sheet tool.

**What one sheet shows, per named region:** a row of native-pixel panels —

```
reference twin | shipped flat render | S3 view-dependent | S3 view-independent | disagreement heat
```

plus a full-figure row for the target view. The three-world readout from your own #5
table is what the Director reads off it: clean composite → the 3D path degrades the
plates; blotchy + high disagreement → the sources are inconsistent (the warp lead);
blotchy + low disagreement → the plates share the defect.

**Inputs** (all on disk, all readable to you):

- `--s3-dir` — an `s3_run.py` output directory (stills + diagnostics per target).
- `--ref-dir` — `E:\AI\training\facet_E08\ARMB\twins\` (`twin_i.png`, 752×1024).
- `--shipped-dir` — `E:\AI\training\facet_E08\ARMB\out\renders_flat\`
  (`final_0..7.png` — the recorded flat renders of the shipped asset; verify their frame
  and orientation against the twins before pairing, do not assume).
- `--regions` — a JSON of named crop boxes per view index. Precedent for the region set:
  `E:\AI\training\facet_E40_A\task3_sheet.py` (the E40 sheet's regions) — the sword
  blade, the grip, and the E40 four are the ones the Director has already judged on.
  Ship a starter regions JSON for view coverage of those, clearly labelled as proposals.
- `--zoom` — integer nearest-neighbour magnification only. **Native pixels or integer
  zoom; no resampling anywhere.** Defects that decide acceptance are invisible at
  thumbnail scale and falsified by interpolation.

**Hard requirements, this repo's laws:**

- **Provenance on the sheet.** Every panel is captioned with its source path and the
  sheet footer carries sha256 of every input consumed. The cheapest diagnostic this repo
  ever built was *reference | asset | provenance | error* on one sheet — provenance is a
  panel, not metadata.
- **A missing input renders an explicit MISSING panel** (labelled, visually distinct),
  never a silent skip and never a silently thinner sheet. No silent caps.
- **Panel geometry is gated**: a crop box that exceeds its source, or panels of
  mismatched size in one row, `raise` an ANDON naming the box and the source — never
  auto-clamp, never auto-resize. (Auto-fixing a bad crop is how a wrong region gets
  judged as a right one.)
- **A stats footer per region**, numerator and denominator separately: coverage %
  (valid-source pixels / region pixels), mean and p90 disagreement inside the region,
  fallback share, owner-view histogram for the VI panel. Numbers from `s3_run`'s
  diagnostics only — the sheet computes layout, not new measurements, with the one
  exception of region-scoped summaries of existing per-pixel maps.
- **Self-test with can-fail legs**: synthetic panels with known content; the
  ANDON legs (oversized box must raise; mismatched row must raise); a MISSING-panel leg
  (absent input produces the placeholder, and the placeholder is detectably different
  from real content); a provenance leg (footer hashes must equal the hashes of the
  files consumed — assert by recomputation, not by echo). State each leg's yes/no
  interval.
- Constraints as always: numpy + scipy + PIL; Python 3.13 headless; MIT; ASCII output;
  gates `raise`, never bare `assert`; pure layout core, thin loaders; tests hermetic at
  t81, runnable with `--basetemp`; **no count-surface edits this round**; leave
  everything uncommitted; do not touch the seat's files
  (`tools/emit_view_aovs.py`, `tools/twin_mesh_warp.py`, `tests/test_t78_*`) or the
  shipped instruments.

**Division of labour, so the verifier structure stays clean:** you BUILD the sheet tool;
a local seat RUNS the chain (bundle → `flow_estimate` → `s3_run` off/on → `s3_sheet`)
under the record's discipline; the advisor folds; **the Director judges.** Your
compositor's output being judged on a sheet your tool laid out is fine — the sheet moves
pixels, it does not grade them — but the run stays out of your hands on purpose, the same
reason no model verifies its own output.

## Argue with the brief

- Is the five-panel row the right comparison set, or does the shipped panel belong beside
  the VI panel rather than the reference? Argue the ordering the eye reads best.
- The disagreement heat panel: raw map, or scaled per-region? A global colour scale hides
  a region whose disagreement is uniformly moderate; a per-region scale makes regions
  incomparable. Pick one, expose the other, and say which is the default and why.
- Anything here whose shape assumes its answer — name it. Round 5's catch was the
  turning point of an arc; keep doing it.

## Calibration

Nominate **one checkable claim** — a specific value a named self-test leg must produce
on a specific synthetic input, runnable as
`E:\AI-Models\trellis2-env\Scripts\python.exe tools/s3_sheet.py --selftest`. We run it
before trusting the rest and report back either way. Seven for seven is on the table.
