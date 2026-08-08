# E16 — the errand batch: eleven queued repairs, each with an anchored regression

**Written by the advisor, 2026-08-08, at the window Ruling 30b deferred and Ruling
33f opened** — Gate 1 accepted on the fourth asset, dataset asset #4 staged, no
live lane anywhere. Every item below was found by a ruling and queued rather than
fixed mid-arc; each carries its finding's pointer. **The discipline: one errand,
one commit, one anchor** — a recorded output reproduced BEFORE the change, the
change applied, the output re-checked (byte-identical where the change is
print/guard-only; delta REPORTED with mechanism where behavior legitimately
moves). No route semantics change except the one flagged opt-in.

## You are the executor

```
cd E:\AI\facet && git pull
python tools/facet_index.py build          <- the E15 ritual (the seeded set is 19)
CLAUDE.md                                  <- read first, follow exactly
docs/experiments/E14-ruling.md             <- Rulings 29c/31d/31f/24c/21e/10a/10b/2d
                                              are the findings you are repairing
docs/experiments/E12-ruling.md             <- Ruling 6d (the _per_invocation form);
                                              cite via q, don't reread the arc
```

Blind predictions first, committed: per-errand, the anchor's expected outcome
(byte-identical vs reported-delta) — a wrong prediction is a finding.

## The errands, in order (safest first)

**E16-1 — `facet_index.py` verify ASCII repair** (Ruling 31f). The `↑` on the
completeness branch crashes under cp1252. Replace with ASCII; ASCII-audit every
print in the tool while there. ANCHOR: verify passes 19/19 before and after
under BOTH `PYTHONIOENCODING=utf-8` and default cp1252; the DB byte-identical.

**E16-2 — `.gitattributes` LF pin** (the CRLF warnings on every commit). Pin
text types to LF; mark `*.db`, `*.png`, `*.npy`, `*.glb` binary; renormalize in
the same commit (`git add --renormalize .`). ANCHOR: `git status` quiet after a
touch-and-restore of README.md; build + verify byte-identity holds after
renormalization.

**E16-3 — `texpass_finalize.py` surface-aware print** (Ruling 31d). In
surface-aware mode, replace "0 texels took mean fallback" with a line stating
the count is structural in this mode (`grown = valid.copy()`); the atlas-flood
path keeps its real count. ANCHOR: replay finalize on the sword's recorded
`run/final` inputs — `atlas_final.png` byte-identical (a print cannot move
bytes; assert it).

**E16-4 — `texpass_iter.py` emit-profile guard** (Ruling 29c). Unprofiled emit
silently produces a 752-wide W3-default frame. Repair: `emit` requires
`--profile` or an explicit `--frame`, else refuses loudly. Grep every caller
first; any legacy invocation gains its explicit frame in the same commit.
ANCHOR: a profile-bound emit of the sword's yaw-0 job byte-identical
(render/mask/hit/cam); an unprofiled call now exits non-zero with the message.

**E16-5 — `mesh_stats.py` silent-warning repair** (Ruling 2d). The
front-view-rect warning uses a proxy a tip-standing prop passes;
`rect_frac_of_figure > 1` is the honest condition sitting unused in the same
JSON. Fire the warning on the honest condition. ANCHOR: run on all four
subjects' meshes — every VALUE unchanged; W3/galleon/beast warning state
unchanged; the sword NOW warns. All four outputs in the report.

**E16-6 — `e08_ceiling` caption + bias warning** (Rulings 6e / 10b). Repair the
caption per 6e's caveat, and print a warning when `--bias` exceeds the route's
wall floor (~0.00196 — near-face origins displace through their own wall;
10b measured +0.97 points). ANCHOR: re-derive the sword's N6 and N8 — exact
against the recorded 51.005% / 51.3342% (the handoff-9 re-derivation already
matched; match it again).

**E16-7 — `e12_elevated` ray-grid floor** (Ruling 10a). Derive the grid from
rays-per-mean-face with the ratio printed; refuse or warn at ratio ≳ 1 (the
sharpened 7b law: a figure at that ratio is not converged — the sword's answer
was wrong 3.9× before the ladder). ANCHOR: reproduce the sword's converged
53.92% up-facing reach within ray-sampling noise at the repaired default.

**E16-8 — the bg-probe's corner-median reference** (Ruling 21e — the retired
method's LAST live consumer, inside `project_twins`). Replace the probe's
colour reference with the fitted border-ring background (the route's standard).
The probe is REPORT-ONLY: ANCHOR — projection outputs byte-identical on a
recorded twin (the probe must not touch commits); report old-vs-new probe
percentages on the sword's twins (the ΔE 11–21 reference error should
collapse).

**E16-9 — kickoff-glob discovery for HANDOFF_FILES** (the claims sweep's
hardcoded list — E15 Ruling 8b's own class, one list over). Sorted glob + the
inverse guard (a parsed row from an undiscovered file fails the run), the
discovered list printed. ANCHOR: the sweep returns the same rows on the current
corpus before and after; the guard demonstrated by a synthetic miss in scratch.

**E16-10 — `texpass_iter` edge-dist A3-port, AS AN OPT-IN FLAG** (Ruling 24c —
the A3 fix's missing consumer; NOT a lane lever). Implement
`--edge-mode local` = `min(edge-dist, ⅓ × local half-width)`; **default
`global` preserves current behavior byte-identically**. The next subject's
stroke-lane ruling opts in or not with its own evidence. ANCHOR: a recorded
stroke commit (stroke 1's 4,344 texels) reproduced byte-identically at the
default; the local mode's delta on the same job REPORTED with per-structure
numbers, adopted nowhere.

**E16-11 — the `_per_invocation` migration** (E12 Ruling 6d's minted fifth
form). Rename `_not_on_route` → `_per_invocation` across ALL FOUR profiles and
every reader (grep consumers first; the registry sweep's recognized-forms list
updates in the same commit). ONE commit, all profiles together — the batch's
one multi-file move. ANCHOR: build + verify PASSED; the sweep returns 0 STALE /
0 new UNDECIDED on all four profiles.

## Explicitly NOT this batch

The **e11 galleon/W3 re-emit** stays queued — it updates committed manifests
the lane holds pointers into and wants ingest coordination with the Director;
it promotes if a training split is cut. **No fixture, canon, palette, or
seeded-set edit. No route-semantics change beyond E16-10's opt-in flag.**
No memory-store write. Do not end a session the Director has not ended.

## Then HALT

Report at `docs/experiments/E16-errands-report.md`: the per-errand table
(finding → change → anchor result → commit), predictions scored, every anchor's
evidence. Build + verify in their own calls, PASSED read, the commits pushed…
by the advisor's fold if you leave them local. The advisor rules at
`E16-ruling.md`.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | One errand one commit; every anchor a recorded artifact reproduced before the change; predictions committed first |
| ANDON_AUTHORITY | 3 | Anchors halt on unexplained deltas; E16-4/-7 ADD refusals; nothing tunes past a mismatch |
| NAMED_COMPENSATORS | 3 | Every change revertible per-commit; renormalization isolated; no publish, no spend |
| DECOMPOSE_BY_SECRETS | 3 | Print/guard changes separated from the one behavior change (flagged opt-in); the migration all-profiles-together so no profile half-moves |
| UNCERTAINTY_GATED_HUMANS | 2 | The batch is queued housekeeping the rulings already decided; the one open trade (E16-10's local mode) is explicitly adopted nowhere |
| EXTERNAL_VERIFIER | 2 | The index's four-leg verify gates the batch's end state; anchors are recorded artifacts, not the tools' own claims. `skip:` per precedent |

## Calibration

Eleven small repairs, and the risk is boredom-shaped: the trap is fixing two
things in one commit, or "improving" something no ruling queued. The anchors
are the discipline — a repair whose anchor fails has found something; halt and
report it rather than making the anchor pass. A negative result is a full
success.
