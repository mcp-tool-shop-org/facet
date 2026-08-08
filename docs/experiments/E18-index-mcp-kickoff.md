# E18 — the record-index MCP: spec 1 becomes a running server, in facet

**Written by the advisor, 2026-08-08 — Ruling 35's step 2, open as of the E17
ruling.** The chain that authorizes this: the spec landed and was ruled
([index-mcp-spec.md](../specs/index-mcp-spec.md)); the Director placed it IN FACET
in his own words ([placement-memo.md](../specs/placement-memo.md), the Director's-
word block); the harness exists and is green at two seats and CI
([E17-ruling.md](E17-ruling.md)). Zero generation, zero credits, no GPU. **This
session builds and tests; it publishes nothing, creates no repo, bumps no
version** — the package-level items are not applicable until extraction, by the
memo's §5 split and the Director's word.

## You are the executor

```
cd E:\AI\facet && git pull
python tools/facet_index.py build            <- the E15 ritual (seeded set 19)
CLAUDE.md                                    <- read first — the tests-ride-the-commit
                                                law binds every commit here
docs/specs/index-mcp-spec.md                 <- THE CONTRACT. Read END TO END; §3-§8
                                                are the build's spec, not suggestions
docs/specs/placement-memo.md                 <- the Director's word + §5 (what "the
                                                bar" means in facet)
docs/experiments/E17-ruling.md               <- the harness you are extending;
                                                Ruling 3d commissions D2 here
docs/experiments/E17-harness-report.md       <- §5 environment (interpreter, pins,
                                                the ambient-encoding trap)
```

⚠ **SHARED WORKING COPY.** The E17 session may still be landing its final leg
(T15b + T18 — conftest and facet_index may change under you; `git log` before
diagnosing any surprise). Standing rules, absolute: file-specific `git add` only,
never `-A`; never commit `docs/index/facet.db` (advisor-owned cadence); no in-repo
DB sha is an anchor (scratch paths only); no stash; profiles/canon/fixtures/seeded
set untouched. **Run under the trellis2-env python** (`E:\AI-Models\trellis2-env\
Scripts\python.exe`) — the E17 ruling's own miss is the warning.

**Blind predictions first, committed** — per deliverable, expected shape and pass
state. A wrong prediction is a finding.

## The decisions this kickoff PINS (build these; do not re-derive them)

1. **Home and form**: `tools/record_mcp.py` — a single-file Python MCP server over
   stdio, the repo's single-file tool idiom, inside the CI paths gate. The official
   Python `mcp` SDK: **verify the current release yourself, pin it** in the report
   and in `ci.yml`'s pip line (same commit as the first test that needs it). The
   server registers in a repo-root `.mcp.json` so any Claude session in this repo
   mounts it — that file IS the polish arc's consumption path.
2. **Six tools, exactly the spec's §3 table**: `record_query`, `record_get`,
   `record_build`, `record_verify`, `record_health`, `record_claims` — with the
   spec's annotations (`readOnlyHint` on the four readers; `destructiveHint: false`
   on build/verify). The tool surface wraps `facet_index.py`'s existing verbs;
   prefer importing its functions over shelling out where the module allows, but
   **the ranking mechanism ports untouched** (E15 Ruling 3 — re-litigating it
   requires re-running the seeded key, and that is not this session).
3. **§6's config machinery stays UNBUILT** — the memo's own ruling: the adoption
   contract is written so extraction is "a packaging job rather than a redesign,"
   unbuilt until a second adopter exists. The server binds this repo's conventions
   directly; **the seeded set stays inside `facet_index.py`** with its withdrawal
   history intact (repo-owned is satisfied — the tool is in the repo).
4. **The certificate is a sidecar**: `docs/index/facet.db.cert.json`, never a DB
   row (leg 1 would fail on its own output — the spec's §4.4). `record_build` runs
   the verify legs and writes it before returning (§3.3: build and verify are one
   act); `record_verify` rewrites it. It records which legs passed, when, **which
   determinism leg held** (byte-identity vs the `.dump` fallback — a fallback is
   reported, never silent), and the corpus identity. It commits on the DB's own
   cadence — a committed DB travels with its certificate, or a fresh clone's
   server refuses until the standing kickoff build line runs.
5. **The three-state health surface, DEMONSTRATED not asserted** (§5): certificate
   PASSED + corpus unchanged → serves; PASSED + corpus moved → serves with a
   staleness banner **naming what moved**; FAILED or absent → **refuses loudly**
   with the structured error (`code` / `message` / `hint` / `retryable`, the
   studio's ErrorShape; the §5 minimum code set). Corpus identity is
   **content-derived, not git-state-derived** — an uncommitted edit counts as
   moved. **There is no skip flag, and adding one is out of scope permanently**
   (E08 A32; the check lives in the query path).
6. **Read-only by construction, with the cheap test in CI** (§4.1): the corpus is
   opened read-only on every path; the server writes exactly two files (DB +
   certificate); and a hermetic test greps the server source for corpus-write
   calls so the property is checked, not promised.
7. **Output requirements** (§8): ASCII on every print path; every response carries
   the certificate state, not just refusals; `file:line` last on table rows.

## Deliverables

**D1 — the server**, in commit slices that each carry their tests (the law):
hermetic tier, running against scratch `--db` copies per the harness's own T1
pattern. Protocol-level tests where the SDK's client makes them cheap;
function-level otherwise — say which and why in the report. The tests must
include: each error code reachable and shaped; the refusal firing on a corrupted
scratch certificate AND on an absent one; the staleness banner naming a moved
file; `record_get` returning corpus text (not the DB copy), bounded;
`record_claims` returning rows with exit-0 semantics preserved.

**D2 — the T2 hermetic fixture (E17 Ruling 3d's commission)**: a synthetic
minimal state (tiny mesh, tiny atlas, tiny prep — deterministic, committed
in-repo, a few KB; `.gitattributes` already marks the binary types) so
`texpass_iter selftest` gains a **hermetic twin test that runs in CI**. The
artifacts-tier T2 keeps anchoring the REAL recorded state — the fixture adds,
replaces nothing.

**D3 — CI extended in place**: the pip line gains the pinned `mcp` SDK in the
same commit as the first test needing it; the hermetic set (now including D1's
tests and D2's twin) green in CI at the advisor's push — the run id lands in the
ruling.

**D4 — the LIVE dogfood proof**: the server mounted through `.mcp.json` and
exercised in a real session — `record_query` answering at least one seeded
question with its pointer, `record_get` returning the rows it pointed at,
`record_health` read in all three states. The transcript rides the report. A
health surface whose refusal has never fired is a check that cannot fail —
fire it on purpose, in scratch, and show it.

**D5 — the report**: `docs/experiments/E18-index-mcp-report.md` — per-deliverable
table, predictions scored, environment changes recorded (the SDK install is one;
E17 recorded zero, so say what changed), the full suite output (old tests AND
new — 27+ passing under the trellis2-env python), the dogfood transcript. Commits
stay local for the advisor's fold. **HALT. The advisor rules at `E18-ruling.md`.**

## Explicitly NOT this session

No publish, no repo creation, no version bump, no landing page, no translations
(not applicable until extraction — the Director's word). No §6 config machinery.
No seeded-set moves or edits. No corpus writes anywhere, including "fixing" a
malformed heading the parser reports. No measurement-MCP work (second in the
ruled order; its own session). No re-litigating the ranking. No memory-store
writes. Do not end a session the Director has not ended.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every design decision is pinned above with its ruling pointer; the SDK version is verified-then-pinned; commits are sliced with their tests |
| ANDON_AUTHORITY | 3 | the deliverable IS an andon (the refusing health surface), and D4 requires firing it rather than asserting it; no skip flag by construction |
| NAMED_COMPENSATORS | 3 | all work is additive files revertible per commit; the two written artifacts (DB, cert) are derived and regenerable; nothing publishes, nothing spends |
| DECOMPOSE_BY_SECRETS | 3 | server binds conventions it does not own (facet_index carries them); the seeded key stays external to the server; config machinery deliberately unbuilt at the extraction seam |
| UNCERTAINTY_GATED_HUMANS | 2 | protocol-vs-function test choices and any SDK-forced deviation from the spec's shapes go to the report for the ruling, named; skip: none — the open calls are listed where they arise |
| EXTERNAL_VERIFIER | 3 | the server's health claims are checked by the harness (a different instrument), CI (a clean-room third runner), and D4's live mount (a real consumer) — three verifiers none of which is the server grading itself |

## Calibration

Two named risks. **Scope-lust**: §6's config, a second adopter's needs, the
measurement MCP — all adjacent, all out. The spec is generous; build exactly it.
**Demo-theater**: a health surface asserted in prose but never fired. D4 exists
because the refusal and the banner must be SEEN failing and recovering, in
scratch, in the transcript. A negative result is a full success.
