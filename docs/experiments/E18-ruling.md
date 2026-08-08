# E18 — advisor ruling on the record-index MCP build (2026-08-08)

Evidence — what this seat OPENED: the report in full
([E18-index-mcp-report.md](E18-index-mcp-report.md), through its §12), the blind
predictions (`c1b8f30`), the six commits, the D4 dogfood transcript read whole —
and this seat's own hands: **the full suite under the pinned interpreter, 91/92
with `T13` failing ONCE against a corpus E19 was actively writing, then PASSED
alone on the single re-run (2.69 s)** — the report's §6 finding reproduced and
cleared at the ruling's own seat, which is Ruling 2l's disposition exercised
before it was written. The scratch-DB ritual closes this fold below.

## Ruling 1 — the server is ACCEPTED: built as pinned, the andon FIRED, the dogfood earned its keep (2026-08-08)

**1a —** every pinned decision built as pinned (§2's table is ratified; the
SDK's `FastMCP` → `MCPServer` rename absorbed with the spec's shapes intact and
the annotations read off the wire); §6's config machinery unbuilt; the seeded
set untouched with its history.

**1b — the health surface was DEMONSTRATED, not asserted**: the FAILED state
fired by dropping E16's rulings from a scratch DB and letting the real leg 2
catch it (`grep 7 != db 0`); every read tool refused with the code, the one fix
command, and the machine object; `record_health` kept answering; one
`record_build` recovered; the staleness banner fired on a REAL corpus move.
D4's driver — the same wire `.mcp.json` declares, spawned exactly — is ratified
as the honest half P9 pre-stated; **the first true in-session mount belongs to
the next session started in this repo, and E20's re-fire session is named that
consumer.**

**1c —** the certificate design is ratified: transcript-parsed with every
damage shape tested (a parse that cannot pass quietly), a sidecar never a row,
corpus identity content-derived so an uncommitted edit counts.

**1d — the connection-leak fix (`89ffa23`) is RATIFIED at the root**: both
sites, can-fail proved by injection in both directions before the fix was
committed, the riding test running the exact sequence a mounted session runs.
P4's falsification is the arc's most useful miss, and its mechanism enters the
record in the studio law's own words: **a consumer finds what the producer's
own tests cannot** — `verify` and `claims` leaked handles harmlessly for every
one-shot caller that ever existed and fatally for the first long-lived one.

**1e —** the five first-run failures are ratified as disclosed — two of them
the session's own guards' defects, both re-pinned in both directions; the
SERVING pin that fired on correct work re-scoped to reachability with the
strict staleness tests kept where they are deterministic. §12's self-correction
(the verify was read AFTER the report commit; said so rather than amended away)
is the correction discipline at its right form.

**1f —** D2 is ratified: non-vacuous by assertion (512 committed = the whole
hole half, structural, with both populations pinned), the three load-bearing
fixture numbers documented in the generator, the artifacts-tier T2 unchanged.
Predictions 10 held / 5 falsified, the misses informative — including P13's
lesson that the corpus is what `record_markdown()` walks, not what an estimate
remembers.

## Ruling 2 — the twelve flags disposed (2026-08-08)

**2a — flag 1:** `BAD_ARGUMENT` is KEPT — an empty result for a typo'd table is
a wrong answer wearing success; a caller-failure code belongs beside §5's
index-failure codes. The spec gains its dated amendment this fold.

**2b — flag 2:** RATIFIED — unreadable routes to `INDEX_NEVER_VERIFIED` with an
honest message; no new code minted.

**2c — flag 3:** the sha-mismatch refusal is RULED IN — a certificate
describing a different artifact is no certificate for the one present, and this
check is what makes Ruling 2j's pair-commit verifiable rather than a habit.

**2d — flag 4:** the certificate is ACCEPTED as built — its own refusal hint
points into the transcript it carries; evidence nobody kept is not evidence;
35.6 KB rides beside an 8.5 MB DB.

**2e — flag 5:** claims-gates-on-health RATIFIED — `record_claims` reads the
index's measurements, so an untrustworthy index poisons them; build, verify and
health never gate, keeping the recovery path open from every state.

**2f — flag 6:** the `0_discovery` bucket RATIFIED — the inverse guards were
never leg 2's rows; forcing them in would have blurred which instrument fired.

**2g — flag 7:** RECORDED — "exactly two paths" means two persistent artifacts;
leg 1's per-process temps are transient and self-removing (E16 Ruling 3). The
spec amendment carries the clarification.

**2h — flag 8:** the absolute interpreter in `.mcp.json` RATIFIED — T18's
lesson applied one config file over; the rig-specific cost accepted, the shape
tested everywhere and the launch tested where the interpreter exists.

**2i — flag 9:** the crossings are disposed: the one-line `.gitignore` rider is
ACCEPTED as disclosed (both lanes need the entry, and git stages files, not
hunks); the near-sweep of E19's staged renames — undone with `reset --soft`,
re-made pathspec-scoped, nothing pushed between — is RATIFIED as exactly right,
and **the pathspec-scoped commit is named STANDING PRACTICE** for any commit in
a shared copy holding foreign staged or modified files (its third use today,
across two seats).

**2j — flag 10: the DB cadence is AMENDED to a PAIR.** The session-boundary
commit is `record_build` immediately before the boundary, then the DB and its
certificate together — coherent by 2c's own check, refusing if ever split. The
relief carries this forward.

**2k — flag 11:** `SERVER_VERSION 0.0.0` ACCEPTED — versioning attaches at
extraction, consistent with the placement ruling.

**2l — flag 12: the fold-race disposition is RULED — run-then-rerun, no
isolation machinery.** A fold-marked failure against a corpus another live
session is writing re-runs once; a second failure is real. Exercised at this
seat before it was written: T13's single failure under E19's live writes, green
alone in 2.69 s. The quiet tree returns as the lanes land; the marker's
documentation already says what these tests race.

## Ruling 3 — E20 RE-FIRES (2026-08-08)

Both of its parked conditions are met: this report exists, and the fixtures
author was ruled ([E20-ruling.md](E20-ruling.md) Ruling 2). E20 runs unchanged
per the Director's disposition — and its fresh session inherits what no session
has had: **the first true in-session mount of `facet-record`**, since
`.mcp.json` now precedes it. Its relay rides the session reply.

## Ruling 4 — CI closes D3 at this ruling's push (2026-08-08)

This push triggers the workflow on the server and its tests; the run id and
result are recorded in the session reply and stand as D3's closure.

## Standards compliance (this ruling)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the acceptance evidence includes this seat's own full-suite run under the named interpreter and the solo T13 re-run; every disposition cites its flag, section, or commit |
| ANDON_AUTHORITY | 3 | the ruling's central ratification is an andon that FIRED against real leg failures; the one test failure at this seat halted the ruling until reproduced-and-cleared |
| NAMED_COMPENSATORS | 3 | the pair-commit amendment (2j) makes the boundary state self-checking via 2c; the crossings' undo was exercised, not described; nothing published, nothing spent |
| DECOMPOSE_BY_SECRETS | 3 | contract deltas land in the spec as dated amendment, dispositions in this ruling, practice in the standing rules — each where its consumers read |
| UNCERTAINTY_GATED_HUMANS | 2 | all twelve flags arrived undecided and leave decided with one-sentence overrule windows; nothing paused mid-fold for a human beyond the halts the system already has |
| EXTERNAL_VERIFIER | 3 | the suite re-ran at a different seat; CI adds the clean-room third runner at this push; the arc's defining defect was found by a consumer, not the author — the external-verifier pattern at every level it applies |
