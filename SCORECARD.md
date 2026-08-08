# Scorecard

> Score a repo before remediation. Fill this out first, then use SHIP_GATE.md to fix.

**Repo:** `mcp-tool-shop-org/facet`
**Date:** 2026-08-08 (E19 treatment)
**Type tags:** `[all]` — no `[npm]`, no `[pypi]`, no `[cli]`, no `[mcp]`; detected by `shipcheck init` v1.0.7

Scores below are read off the **actual** gate results, not estimated. The
pre-remediation column is the state at the moment `shipcheck init` first ran; the
verbatim entry audit (1 checked / 35 unchecked / 1 skipped, 3%) is recorded in
[E19-treatment-report.md](docs/experiments/E19-treatment-report.md).

## Pre-Remediation Assessment

| Category | Score | Notes |
|----------|-------|-------|
| A. Security | 4/10 | The *substance* was already clean — no credentials anywhere in the tree, no telemetry, network egress confined to a loopback ComfyUI default. The *documentation* was entirely absent: no SECURITY.md, no threat model, and nothing stating the three real sharp edges (unsandboxed file writes, baked absolute paths, raw tracebacks). A reader had no way to know any of it without reading 34 scripts. |
| B. Error Handling | 3/10 | No structured error shape, no exit-code registry, raw Python tracebacks on unexpected failure. Not zero, because the `ANDON:` halt convention is real, load-bearing and ruled (E08 A32: the gate lives inside the tool, no skip flag) — a deliberate halt says what measurement fired it. |
| C. Operator Docs | 6/10 | The README is unusually strong for this axis — a measured-state document with corrections kept in place beside the measurements that overturned them, and `docs/experiments/` carrying spec → report → ruling for every claim. Missing: CHANGELOG, any statement of support status, any runtime/CI version note. |
| D. Shipping Hygiene | 5/10 | The verify story was genuinely there and better than most: 32 tests passing at two seats' hands plus a paths-gated pinned CI workflow (E17). *(Corrected 2026-08-08 at the E19 ruling: this row read "27", inherited from the dispatch's stale premise — the same figure §6a caught and corrected. E17 Ruling 1 closed at 27; Ruling 5 closed the arc at 32, which was the state at treatment entry.)* Everything version-shaped was absent — no manifest, no version field, zero git tags — and no dependency scanning. |
| E. Identity (soft) | 0/10 | Nothing. No logo, no translations, no landing page, no GitHub description, homepage or topics. |
| **Overall** | **18/50** | A repo whose *record* was far ahead of its *presentation*. |

## Key Gaps

1. **Every security fact was true and none of it was written down.** The clean state was
   invisible; so were the three real sharp edges. Both halves needed saying.
2. **No CHANGELOG and no version of any kind** — zero tags, no manifest, nothing a
   reader could anchor "what state is this repo in" to except reading the whole record.
3. **The error contract is a research contract wearing no label.** Not a defect to fix
   in a treatment, but a defect to *disclose* — with the condition under which it stops
   being good enough written down (extraction).
4. **No presentation surface at all.** Four accepted assets across four subject classes
   at zero credits, a four-leg-verified index and a green 32-test suite — and no way for
   anyone to see any of it without reading 775 lines of README.
5. **Dependency posture has no executable check** and no manifest to give one a target.

## Remediation Priority

| Priority | Item | Estimated effort |
|----------|------|-----------------|
| 1 | SECURITY.md + README threat model — write down what is true, including the sharp edges | ~1h |
| 2 | CHANGELOG + the version question in facet's own form (tag + heading, no manifest) | ~30m |
| 3 | Landing page + handbook — the record's story, every claim traced to its ruling | ~3h |
| 4 | GitHub metadata + repo-knowledge entry | ~45m |
| 5 | D3 dependency scanning — flagged to the ruling, cheapest form is `pip-audit` over CI's already-pinned set (E18's lane) | ~15m, not this lane |

## Post-Remediation

| Category | Before | After |
|----------|--------|-------|
| A. Security | 4/10 | 9/10 |
| B. Error Handling | 3/10 | 4/10 |
| C. Operator Docs | 6/10 | 9/10 |
| D. Shipping Hygiene | 5/10 | 6/10 |
| E. Identity (soft) | 0/10 | 8/10 |
| **Overall** | 18/50 | **36/50** |

**Read the two columns honestly.** A went to 9 because the facts were already good and
now they are stated; the residual point is that two posture items are disclosed gaps,
not closed ones. **B moved one point, and only one** — the treatment *documented* the
error contract, it did not improve it; a treatment that claimed otherwise would be
inflating a verdict. D moved one point for the same reason: the verify story was
already real, and the version/manifest/dependency items are ruled out until extraction
rather than solved. E is 8 rather than 10 because translations are staged for the
advisor's own run and the Pages deploy waits on the Director's word.
