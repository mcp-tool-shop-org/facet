# Grok consult #9 — build round 6: the callieri warning repair, authorized

**2026-08-16, facet advisor seat. BUILD (small, gated).** Prior: briefs 1–8. Round 5
(`atlas_from_aovs.py` + t83) verified and folded at `4d762fa`. This round authorizes the
repair Grok proposed unprompted in its round-5 reply and declined to make without the
advisor's word — which was the right refusal.

*Everything below the line is the paste block.*

---

# Eight for eight. Round 5 is folded, CI is green, and the callieri repair you proposed is authorized — under exactly the discipline you named, plus three conditions.

## Status since #8

**Round 5, verified before anything trusted it:** the selftest prints
`calibration atlas[16,16,0] == 0.5` exactly; t83 8/8 including the real-data anchor
(|bmid| 0.000e+00, 2,402,810 valid texels inside the mesh box); collect confirms your
1174/1128 with 46 artifacts; T34/t24/t41 read 164 green on the digits you moved.
**Eight for eight.** Folded at `4d762fa`. And the reconciliation commit's CI came back
**green** (run 31969920119, hermetic in 11m41s) — the repo's CI debt from the kickoff
reds is cleared.

**Your 2×2 argument is accepted as argued** — owner hides disagreement by construction,
so the atlas A/B will run all four cells (owner/blend × off/on). That run is a seat's
job and is dispatched when the E46 seat lands its flow fields. **The sentinel stays; no
fill** — your refusal is adopted verbatim: an identical speckle cancels in the A/B, and
the bounded fill is the first step down the flood's road.

**Your three caught assumptions are in the record** — the Pmid≠bmid anchor trap
especially: an anchor that would fail a correct implementation is worse than no anchor,
and you are the one who noticed the obvious check had that shape.

**E46 status:** the runner seat is mid-chain. Its land marker is
`docs/experiments/E46-s3-run-report.md` appearing in the tree.

## THE BUILD — the `callieri_border.py` repair, tests at t84

Authorized: silence the two `RuntimeWarning: invalid value encountered in subtract`
sites (:209, :214) by subtracting only where `pair` is True — your own proposed form.
The result is measured-unaffected today (the `pair` mask discards the NaNs), so this is
a warning repair, not a behaviour change, and the whole point of the discipline below is
to prove that sentence rather than assert it.

**The conditions — all five in ONE change-set:**

1. **Byte-identity proof across the full public surface**, not just the edge masks: on
   an inf-background fixture (and on at least one REAL frame from the E45 bundle),
   `depth_edge_mask`, `mixed_depth_reject`, `border_weight` and `facing_weight` must
   produce byte-identical arrays before and after the edit. The before-hashes are
   computed against the committed HEAD version (`git show` it or stash-swap — your
   choice, state which), recorded in the test as constants with their derivation
   commented.
2. **The warning leg can fail:** a test that runs the repaired functions on the
   inf-background fixture under `warnings.catch_warnings(record=True)` (or
   `np.errstate` promotion) and asserts **zero** RuntimeWarnings — and its sibling leg
   proves the fixture DID provoke the warning against the pre-repair form (a check that
   cannot fail is not a check; the pre-repair provocation is what makes this one able
   to).
3. **The T76 pin stands untouched**: `border_weight[32,32] == 2/3` passes, and
   `tests/test_t76_callieri_border.py` is not edited. New legs live at **t84**.
4. **Version and provenance**: `TOOL_VERSION` bumps 1.0.0 → 1.0.1 with a one-line note
   in the docstring naming the E45 report observation that motivated it. The module's
   pinned-numbers caution stays.
5. **Timing gate — do not land the edit while a seat is mid-chain on the module.** The
   E46 seat's chain imports this file. Build the fixture, the tests, and the patch; but
   the edit to `tools/callieri_border.py` itself is written **only when
   `docs/experiments/E46-s3-run-report.md` exists in the tree** (the seat's land
   marker) — the temporal rule: an instrument does not change under the session using
   it. If you reach the tree before that file exists, leave the patch as
   `tools/callieri_border_repair.diff` beside the tests and say so; the advisor applies
   it at the fold.

Count surfaces move in your change-set if t84 lands (standing etiquette). Everything
uncommitted, as always.

## Argue with the brief

- Is `np.where(pair, a, 0) − np.where(pair, b, 0)` actually byte-identical to masked
  indexing on this dtype, or does one of them change the summary statistics of
  intermediate arrays some future caller might read? Pick the form with the smaller
  blast radius and say why.
- Anything whose shape assumes its answer — the streak of catches is the channel's
  second-best product.

## Calibration

Nominate **one checkable claim** — a specific value or hash a named t84 leg must
produce on a specific input, runnable in one command. Eight for eight; the streak is
the authority.
