# E19 — the full treatment: facet becomes a presentable studio repo without rewriting its record

**Written by the advisor, 2026-08-08, at the Director's word** — the treatment he
named hours earlier ("we haven't done a full treatment or versioned it"), fired now
that the repo has what the protocol gates on: a green 27-test suite and CI (E17).
**The protocol files are the spec; this kickoff adds only facet's overlays.** The
advisor has checked full-treatment.md's standards-compliance block (present, scored,
every sub-2 carrying a named remediation — the 2026-06-01 audit's state); the
session does not re-audit it.

## You are the executor

```
cd E:\AI\facet && git pull
python tools/facet_index.py build                <- the E15 ritual (seeded set 19)
CLAUDE.md                                        <- read first, follow exactly
C:/Users/mikey/.claude/projects/F--AI/memory/full-treatment.md      <- THE PROTOCOL,
C:/Users/mikey/.claude/projects/F--AI/memory/handbook-playbook.md      read all three
C:/Users/mikey/.claude/projects/F--AI/memory/shipcheck.md              END TO END
README.md + docs/experiments/README.md           <- the measured state you are
                                                    presenting, not rewriting
```

⚠ **SHARED WORKING COPY — up to two other sessions may be live** (E18 building the
record-index MCP; E17's final leg). Standing rules: file-specific `git add` only,
never `-A`; never commit `docs/index/facet.db`; no stash; the det_a race is fixed
(T13) but the courtesy stands — scratch paths for any DB comparison. **Lanes:**
E18 owns `tools/`, `tests/`, `ci.yml`, `.mcp.json`. E19 owns README, `site/`,
handbook content, SECURITY/CHANGELOG, GitHub metadata, the repo-knowledge entry —
and MAY add the Pages deploy workflow as its own file (the repo's second and last;
the studio's two-workflow cap lands exactly). A want in the other lane is FLAGGED
for the ruling, never edited.

**Blind predictions first, committed**: shipcheck's audit state at entry (which
hard gates pass, which items are structurally inapplicable), before running it.

## The two laws this kickoff exists to enforce

**1 — THE RECORD IS NOT REWRITTEN.** This repo's README is a measured-state legal
document: corrections-in-place, ⚠ annotations, falsified claims kept beside their
overturning measurements. The treatment ADDS marketing surface — logo, badges,
nav, a short plain-language intro — and deletes NOT ONE measured claim, correction,
or annotation. The marketing voice lives in the NEW surfaces (landing page,
handbook), where every claim must trace to the record: four accepted assets across
four subject classes at zero credits, a 27-test suite, CI green, the four-leg
verified index. That story is strong exactly as measured — no verdict inflation,
no rounding up. Any protocol step that would rewrite or trim the record is taken
as SKIP-with-reason and flagged for the ruling. The claims sweep runs after every
content phase and must read 0 STALE.

**2 — PUBLIC SURFACES ARE LEAD-AUTHORED** (the protocol's own law, earned
2026-06-20): README, landing page, handbook pages, CHANGELOG, metadata — this
session writes them itself. **No subagent touches any public surface.**

## The phases, with facet's overlays

**Phase 0 — shipcheck, the gate**, exactly as the protocol writes it (init →
SHIP_GATE → audit; mind the recorded exit-code nuance — the audit counts
checkboxes). Facet overlays: the repo publishes nothing and has no package
manifest — the npm-packaging class of items is **SKIP with the reason cited**
(the placement memo's §5 split and the Director's ruled extraction gate), never
silently unchecked. SECURITY.md, CHANGELOG.md, LICENSE-check, threat-model note,
structured-error and docs gates apply as written. The verify story is the E17
suite + CI — reference them; do not build a parallel verify script.

**Phases 1–5 as the protocol orders them**, with: the logo/brand asset per the
protocol's brand-repo flow; README polish per Law 1 above; the landing page via
site-theme and the handbook via the playbook — content sourced from the record
(the route diagram, the four assets, the instruments, the MCP tools' state AS THE
RECORD HOLDS IT at write time — in-flight is written as in-flight); GitHub
metadata (description + topics) staged with the current values recorded for the
compensator; **Phase 5's repo-knowledge entry is NEVER skipped** — facet enters
the studio DB with a thesis the scan output supports.

**Phase 6 — translations are STAGED, not run.** The standing rule: executor
sessions defer; **the advisor runs `translate-all.mjs` at the fold**, and the
release-ordering law holds — translations land BEFORE any tag or release, in the
same commit family as the README they translate.

**Phase 7 — publish actions are STAGED, not fired.** Draft the CHANGELOG entry
and release notes; stage the version question in its facet form — **the
Director's own word named versioning, so the proposal is a `v1.0.0` git tag +
GitHub release at treatment close** (no npm — nothing publishes until
extraction). The tag, the release, and the Pages enablement fire **only on the
Director's word after the ruling**, translations first, compensators per the
protocol's table. The held-publish note applies as written: every reversible
phase RUNS in full — do not shrink the treatment because publishing waits.

## Then HALT

Report at `docs/experiments/E19-treatment-report.md`: the shipcheck audit output
verbatim (before and after), predictions scored, the per-phase table with every
SKIP's reason, the claims sweep at 0 STALE, preview paths/screenshots for every
new surface (the advisor's eye walks them at full size, then the Director's), the
staged release package (CHANGELOG, notes, tag proposal), and any cross-lane wants.
Commits stay local for the advisor's fold. **The advisor rules at
`E19-ruling.md`; the Director's word fires the tag, the release, and Pages.**

## Explicitly NOT this session

No npm publish, ever (extraction-gated, ruled). No edits to `docs/experiments/*`
(this kickoff and your report excepted), `canon/`, `profiles/`, `tools/`,
`tests/`, `ci.yml`, `.mcp.json`, the citable trees, or the seeded set. No record
rewrites per Law 1. No subagents on public surfaces per Law 2. No translations
run in-session. No tag, release, or Pages deploy fired. No memory-store writes
(the advisor updates the studio memory after the ruling). Do not end a session
the Director has not ended.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | the protocol's own PIN remediation (treatment.lock) is P2 and not yet landed — inherited honestly rather than papered; this dispatch pins what it can: the protocol files read end-to-end, blind predictions committed, every SKIP carrying its written reason |
| ANDON_AUTHORITY | 3 | shipcheck is a hard entry gate; the claims sweep at 0 STALE gates every content phase; Law 1 converts record-rewrite into a halt-and-flag, not a judgment call |
| NAMED_COMPENSATORS | 3 | the protocol's compensator table governs (checked present, owners named); all irreversible actions (tag/release/Pages/metadata) are STAGED for the Director's word, none fired in-session |
| DECOMPOSE_BY_SECRETS | 3 | lane separation by change cadence: E18 owns the tool surface, E19 owns the presentation surface; record vs marketing split by Law 1 — measured claims live in the record, voice lives in the new surfaces |
| UNCERTAINTY_GATED_HUMANS | 3 | the two eyes are in the loop by construction — the advisor walks every surface at full size, the Director fires every irreversible act; the version proposal is contrastively staged, one sentence to overrule |
| EXTERNAL_VERIFIER | 2 | the claims sweep and shipcheck audit are instruments outside this session's authorship; the protocol's own EXTERNAL_VERIFIER remediation (different-family checks) is P1 upstream and not this session's to build. skip: inherited, named |

## Calibration

The treatment's named failure modes, both already paid for elsewhere: shrinking
the work because publishing is held (run every reversible phase), and marketing
drift (a landing page claiming what the record does not). The second is this
repo's cardinal sin — when in doubt, quote the record and link the ruling. A
SKIP with a reason is a full success; an unmarked checkbox is not.
