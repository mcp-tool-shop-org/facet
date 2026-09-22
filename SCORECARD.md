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

---

## Re-score at v0.8.1 — 2026-09-22

The section above is the E19 record and stays as written. This is a fresh read, **not a
revision of it**: eight releases have landed since, and three of the five rows moved for
reasons that are in the record rather than in a judgement call.

`npx @mcptoolshop/shipcheck audit` at this commit: **28 checked / 0 unchecked / 9 skipped,
100%.** Every skip carries a written reason and a re-open condition.

| Category | E19 (2026-08-08) | v0.8.1 | what moved it |
|----------|------------------|--------|---------------|
| A. Security | 9/10 | 9/10 | unchanged, and the residual point is the same one — two posture items are **disclosed** gaps (unsandboxed file writes, baked absolute paths), not closed ones |
| B. Error Handling | 4/10 | **8/10** | E21 gave the two installed commands a structured failure shape and an exit-code registry; E22 added **`4` REFUSED** for a fired gate; E22/E23/E25 converted **278** ANDON sites from `assert` to `raise`, closing a class that `python -O` could delete silently |
| C. Operator Docs | 9/10 | 9/10 | unchanged. A CHANGELOG, a support-status statement and a runtime/CI note all landed; the residual point is that the research scripts outside the two published commands still surface raw tracebacks |
| D. Shipping Hygiene | 6/10 | **9/10** | nine tags, four version declarations gated against the tag by `release.yml`, a published npm launcher and a PyPI wheel, and a 1376-test suite with 1319 hermetic tests in paths-gated CI |
| E. Identity (soft) | 8/10 | **10/10** | logo, seven translations, landing page, Starlight handbook with a working pagefind index, GitHub description, homepage and twelve topics — all live |
| **Overall** | 36/50 | **45/50** | |

**The five points that are missing are real and each is named.** A and C are each held at
9 by a disclosed gap rather than an unknown one, and B is held at 8 because the contract is
closed for `facet-index` and `facet-mcp` and **not** for the ~100 research instruments under
`tools/`, which are a research-instrument surface by design and say so.

**What this scorecard does not measure:** whether the assets are good. That is the
Director's eye, and no row here approximates it.
