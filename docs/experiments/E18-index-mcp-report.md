# E18 — the record-index MCP: report

**Executor session, 2026-08-08.** Dispatch:
[E18-index-mcp-kickoff.md](E18-index-mcp-kickoff.md). Contract:
[index-mcp-spec.md](../specs/index-mcp-spec.md). Blind predictions committed
before any server code existed:
[E18-index-mcp-predictions.md](E18-index-mcp-predictions.md) (`c1b8f30`).

**Nothing here is judged.** The advisor rules at `E18-ruling.md`. Zero
generation, zero credits, no GPU. Commits are local and unpushed; the tracked
DB and its new certificate sidecar are uncommitted per the session-boundary
cadence.

---

## 1. Per-deliverable

| # | deliverable | landed | evidence |
|---|---|---|---|
| D1 | the server | `tools/record_mcp.py`, six tools over stdio | `12f6381` + `5c4fa27`; §2 |
| D1 tests | 59 hermetic, in the commits that touch the code | T19/T20/T21/T22/T23 | §6 |
| D2 | the T2 hermetic fixture (E17 Ruling 3d) | `tests/fixtures/selftest_min`, 40,359 bytes | `1b45201`; §5 |
| D3 | CI extended in place | `mcp==2.0.0` pinned, `.mcp.json` in the paths gate | `5c4fa27` |
| D4 | the LIVE dogfood, all three states | fired over the mount path, refusal included | §8 |
| D5 | this report | — | — |

**CI-green is NOT verified here.** Nothing has been pushed; the run id lands at
the advisor's push, per the dispatch.

## 2. The server, against the decisions the kickoff pinned

| pinned | built as pinned? | note |
|---|---|---|
| `tools/record_mcp.py`, single-file, stdio, inside the CI paths gate | yes | 1,020 lines, ASCII bytes |
| the official SDK, verified-then-pinned | yes — **`mcp==2.0.0`** | current release on PyPI at 2026-08-08; pinned in `ci.yml` in the same commit as the first test needing it |
| registered in a repo-root `.mcp.json` | yes | one server, `facet-record`; T23 tests both that it parses and that its command line starts a server |
| six tools, exactly §3's table, with §3's annotations | yes | `readOnlyHint` on the four readers; `destructiveHint: false` on build/verify — read off the wire in §8 |
| the ranking ports untouched (E15 Ruling 3) | yes | `record_query` calls `facet_index.query` and filters after, at the CLI's own over-fetch factor |
| §6's config machinery UNBUILT | yes | the server binds `facet_index` and declares nothing; `_check_conventions` refuses `CONVENTIONS_INVALID` if that module stops carrying what it binds |
| the seeded set stays in `facet_index.py` | yes | untouched, withdrawal history intact; `SEEDED_SET_INVALID` fires if it is emptied or malformed |
| the certificate is a sidecar, never a DB row | yes | `<db>.cert.json`; a test asserts writing it moves **zero bytes** of the DB |
| `record_build` runs the legs and writes the certificate before returning | yes | one act (§3.3 / E15 Ruling 4.1) |
| a `.dump` fallback is reported, never silent | yes | `determinism_leg` is its own certificate field; every run so far held **byte-identity** |
| corpus identity content-derived, not git-derived | yes | sha256 over the text `facet_index.read` returns, per file; an uncommitted edit counts as moved |
| three-state health surface | yes | §8 fires all three |
| no skip flag, permanently | yes | and made **structural**: a test walks `--help` for bypass options and proves four plausible skip env vars change nothing |
| read-only by construction, cheap grep test in CI | yes | AST walk, both directions demonstrated |
| ASCII on every print path; `file:line` last; certificate on every response | yes | tested per clause |

### 2.1 What the SDK turned out to be

**`FastMCP` does not exist in `mcp` 2.0.0.** `mcp.server.fastmcp` is gone; the
high-level decorator server is `mcp.server.mcpserver.MCPServer`, and the wire
objects use snake_case (`is_error`, `server_info`, `read_only_hint`). Tool
annotations are expressible on the decorator, so the spec's §3 table lands
unchanged — P2 held in substance and is falsified on the name.

Refusals leave through one site. The SDK marks an exception-raising tool
`is_error: true` and prefixes the text; the payload is written so both a reader
and a parser get the whole thing:

```
Error executing tool record_query: REFUSED: <message>
  code:      INDEX_VERIFY_FAILED
  message:   ...
  hint:      ...
  retryable: false
{"code": "...", "error": true, "hint": "...", "message": "...", "retryable": false}
```

### 2.2 Function-level vs protocol-level, and why each

The dispatch asked which and why. **The wire is tested at protocol level**
(T22, T23): the annotations, the input-schema plumbing and the `is_error` flag
are produced by the SDK, not by this repo's code, so a function-level test
cannot see any of them. Most of T22 drives `Client(server)` — the same dispatch
a mount drives, without a process spawn. **Two tests spawn the real
subprocess**: one launching the entry point directly, one launching *exactly
what `.mcp.json` says*, because an in-process client cannot prove
`python tools/record_mcp.py` runs at all. **The state machine is tested at
function level** (T21): `health()` returns a value, so its nine refusal paths
and three staleness classes are cheaper and clearer read as values than as
JSON over a socket, and driving all of them through the wire would have bought
coverage of the same SDK plumbing twenty-four more times.

### 2.3 The certificate, as written

35,617 bytes for the live corpus. Keys: `schema`, `written_by`,
`server_version`, `verb`, `verified_utc`, `state`, `determinism_leg`, `legs`,
`failures`, `unattributed_failures`, `andon`, `verify_exit_code`, `db`
(path/bytes/sha256), `counts`, `corpus` (files/id/manifest — 231 files), and
`transcript` (verify's own output, 114 lines, verbatim). Pure ASCII bytes,
LF-terminated.

**Per-leg detail is parsed from verify's transcript, because
`facet_index.verify` returns an int and prints.** The parse is built so it
cannot pass quietly: the VERDICT comes from the single line verify prints once
plus the exit code, and the per-leg routing only refines it. A failure line no
route matches lands in `unattributed` and the state stays FAILED; a missing leg
header, a missing determinism line, a missing verdict, or an exit code that
disagrees with the verdict all produce `state: FAILED` with an `andon` note.
Tested against a real verify run — so a reworded header in `facet_index` fails
loudly here — and against each of those damage shapes.

### 2.4 The health surface's decision order

```
no DB                                  -> INDEX_MISSING          (retryable)
no certificate / unreadable one        -> INDEX_NEVER_VERIFIED   (retryable)
certificate says FAILED                -> INDEX_VERIFY_FAILED    (not retryable)
certificate describes a DIFFERENT DB   -> INDEX_NEVER_VERIFIED   (retryable)
corpus digest moved                    -> SERVING_STALE, banner naming the files
otherwise                              -> SERVING
```

`record_health` never refuses — it is how a caller finds out the others are
refusing. `record_query`, `record_get` and `record_claims` gate; `record_build`
and `record_verify` never gate, because they are the recovery.

## 3. Predictions, scored

| # | prediction | verdict |
|---|---|---|
| P1 | `mcp==2.0.0` installs from wheels, disturbs nothing pinned | **held** — 18 packages, no compiler; the 32-test suite was green immediately after |
| P2 | a decorator server with expressible annotations, `FastMCP`-class | **half falsified** — the API shape held, the NAME did not: `FastMCP` is gone, it is `MCPServer` |
| P3 | installable on CI's 3.12 | **held** — `Requires-Python: >=3.10` |
| P4 | **no edit to `facet_index.py` is needed** | **FALSIFIED** — and it is the session's most useful miss; see §4.5 |
| P5 | the certificate must parse verify's transcript; the parse finds all four headers and both verdict lines first run | **held** |
| P6 | `record_get` is new code; resolves all 19 seeded anchors | **held** — a test walks every seeded target |
| P7 | the read-only guard passes first run and fires on a synthetic corpus write | **falsified on the first half** — it fired on the real source, twice, and both were the guard's own defects; see §4.1 and §4.2 |
| P8 | all three health states reachable in scratch, refusal on absent AND corrupted certificates | **held** — six corruption shapes, all refusing |
| P9 | **the live `.mcp.json` mount is NOT exercisable inside this session** | **held** — confirmed by name lookup: no `mcp__facet-record__*` tool exists in this session. See §8 for what was done instead |
| P10 | fixture needs exactly state/prep/glb; under 100 KB | **held** — 40,359 bytes |
| P11 | the fixture commits > 0 texels and carries > 0 styled texels, first construction | **held** — 512 committed, 512 styled, max delta 0.000000 |
| P12 | 14–20 new hermetic tests; 41–49 total; 1–2 first-run failures | **FALSIFIED, both halves** — 60 new, 92 total, and 5 first-run failures |
| P13 | corpus manifest ≈ 70 ± 10 markdown + 3 JSON | **FALSIFIED** — 231 files (228 markdown + 3 profiles). The estimate came from `PROSE_FILES`, which is the FTS prose list, not the corpus: `record_markdown()` walks all of `docs/` |
| P14 | 0 STALE from `record_claims` | **held** — 0 stale, 2 ambiguous, 10 unparseable, exit 0 |
| P15 | `record_build` under 30 s | **held** — 2.3 s |

## 4. Every first-run failure, in full

Five, four of them caught by the tests and fixture-hygiene of this session and
one by the dogfood. None of them moved a recorded anchor.

### 4.1 The ASCII test fired on this session's own source

`test_t19_source_is_ascii` failed at byte 32,388: the block-boundary regex in
`record_mcp.py` carried literal em and en dashes. The record uses all three
dashes, so the pattern must match all three — the fix is `\u2014\u2013-` as
escapes, so the pattern is unchanged and the source is ASCII bytes. The check
is stricter than §8's "every print path" (it is the whole file) and that is
deliberate: the spec's own words are *"the product ships ASCII from the first
line."*

### 4.2 The read-only guard's first cut was a name match, and over-fired

It flagged `os.path.relpath(cert_path(db), REPO).replace("\\", "/")` inside
`record_build` — a `str` method. Two defects in one: matching the attribute
NAME alone (`replace`, `remove`, `copy`, `mkdir` all exist on builtins), and a
receiver walk that stepped *through* a call to blame `os` for a method called
on its result. Split into ambiguous names (flagged only on a filesystem
receiver) and unambiguous ones (`write_text`, `rmtree`, `copyfile`, … always
flagged), with both directions now pinned: six mutation shapes caught, four
builtin lookalikes not. The scanner's bound is stated in its own docstring
rather than implied — a `Path` bound to a variable and mutated through it would
pass, and the complement is that the only `sqlite3.connect` in the module is
`mode=ro`, proved by a handle that raises on INSERT rather than by the literal.

### 4.3 A `SERVING` pin that fired on correct work

T23's launch test failed once on `state == "SERVING"`. It was right to fail and
the pin was wrong: **three sessions were live in this shared working copy**
(this one, E19's treatment, E20's unit-test arc) and one wrote a document during
the ~2 s the subprocess takes to start, so the corpus legitimately moved and the
server correctly said `SERVING_STALE`. The wire tests now assert *serving*
(not-refusing) and print the state, because their subject is reachability;
staleness keeps its strict tests where the diff is driven from the certificate
side and is deterministic. The two strict state-1 assertions that remain name
the shared-copy cause in their own failure message.

### 4.4 CRLF in the fixture's `meta.json`

Caught by git on the first `add`, not by a test: the generator wrote through the
platform default. `.gitattributes` pins this repo to LF and T6 tests for it.
Fixed at the writer.

### 4.5 The dogfood found a real defect in `facet_index` — P4's falsification

`record_build` after `record_verify` died:

```
REFUSED: build failed: PermissionError: [WinError 32] The process cannot access
the file because it is being used by another process: '...facet.db'
  code: INTERNAL
```

**`facet_index.verify` and `facet_index.claims` each opened a sqlite connection
and never closed it.** Harmless for every caller that had ever existed — a CLI
exits a millisecond after the verb — and fatal for the first long-lived one,
because `build()` begins with `os.remove(db_path)` and Windows refuses to remove
a file any handle still holds. The MCP server is the first caller that keeps the
interpreter alive across two verbs, so it is the first caller that could ever
see this.

Fixed at the root rather than at the consumer (a subprocess or a `gc` nudge in
`record_mcp` would have left it in place for the next composition), and the
second site was found by the repo's own law — *when you fix a root cause, find
its other consumers.*

**Can-fail proved by injection, both directions, before the fix was committed.**
A scratch copy of `facet_index` with ONLY the two new `con.close()` lines
removed:

```
PRE-FIX  verify rc: 0
PRE-FIX  build after verify: PermissionError -> [WinError 32] ...
POST-FIX build after verify: SUCCEEDED (verify rc 0)
```

The riding test runs the sequence a mounted session runs all day — verify,
claims, build, verify, in one interpreter — and asserts PASSED throughout.

## 5. D2 — the hermetic fixture

`tests/fixtures/selftest_min`, **40,359 bytes**, generated and documented by
`tests/fixtures/make_selftest_fixture.py`:

```
mesh_uv.glb                1,584    one flat quad, 4 verts / 2 tris, UV over the atlas
prep/meta.json               176    lo/hi/maxabs of the swizzled bbox
prep/mask.npy             12,416    all figure
prep/pos.npy              12,416    derived ANALYTICALLY from the quad, not baked
prep/nor.npy              12,416    +X, constant
state/atlas.png              122    32x32, two halves
state/holes.png               90    the u >= 0.5 half
state/styled_mask.npy      1,152    the u < 0.5 half
```

`texpass_iter selftest` on it: **committed 512 texels, styled-texel max delta
0.000000, holes 512 -> 0, PASS** — first construction, no second attempt at the
geometry.

**Non-vacuous by assertion, not by hope.** `max delta over pre_styled` is 0 for
free over an empty styled set, and *holes did not shrink* passes when nothing
was committed, so T2b pins both populations. 512 is the whole hole half and is
structural rather than tuned: every hole texel on this quad is visible, faces
the camera at 1.0, and projects far more than `--edge-dist` from the rendered
figure edge — a partial count is a finding, not a tolerance to widen.

Three fixture numbers are load-bearing and say so in the generator: the quad's
Y half-extent is 0.3 rather than 0.5 because `emit` fits the frame to the Z
extent (`h_ext = 0.884`), so a half-unit-wide quad would project past the frame
and the edge guard would measure the crop instead of the figure; **both atlas
halves sit far from the 0.42 background** because `commit` keys its trust mask
with `|edited - bg| > 0.06` and an unpainted hole rendering AT hole-grey is
indistinguishable from background by colour — a hole-grey fixture would have
committed nothing while passing; and pos/nor use `emit`'s exact texel
convention or the fixture would test a shifted mapping.

**T2 is unchanged** and keeps anchoring the real recorded state, which is what
Ruling 3d said the fixture would do.

## 6. The suite

**92 passed, both tiers, 129.38 s**, under
`E:\AI-Models\trellis2-env\Scripts\python.exe`. E17 closed at 32; this session
adds 60.

| file | tests | tier |
|---|---|---|
| test_t01_index_verify.py | 3 | hermetic (fold) |
| test_t02_selftest.py | 2 | 1 artifacts + **1 hermetic (T2b, new)** |
| test_t03_emit_guard.py | 2 | hermetic |
| test_t04_discovery_guards.py | 4 | hermetic |
| test_t05_claims_sweep.py | 2 | hermetic |
| test_t06_line_endings.py | 2 | hermetic |
| test_t07…t12 | 6 | artifacts |
| test_t13_det_race.py | 1 | hermetic (fold) |
| test_t16_registry_sweep.py | 5 | hermetic |
| test_t18_interpreter_precheck.py | 5 | hermetic (+1 assertion, `mcp` in the measured table) |
| **test_t19_record_mcp_readonly.py** | **6** | hermetic |
| **test_t20_record_mcp_certificate.py** | **12** | hermetic (4 fold) |
| **test_t21_record_mcp_health.py** | **24** | hermetic |
| **test_t22_record_mcp_tools.py** | **14** | hermetic |
| **test_t23_mount_path.py** | **3** | 2 hermetic + 1 on-rig |

Zero skips in that run (the recorded trees are present on this rig). Every skip
path still prints its reason; T23's on-rig test skips with the interpreter it
could not find, which is what CI will see.

**The full suite needed two attempts, and the first attempt is a finding rather
than a defect.** Run 1: 3 failed / 89 passed — T1, T13 and T20's real-transcript
leg, all `fold`-marked, all against a corpus that moved under them mid-run
(`VERIFY FAILED - 2 / X artifacts: 10 dangling pointers / X fts: 19 dangling
pointers`, because a concurrent session renamed `docs/brand/facet-logo.png` to
`four-accepted-assets.png` while the 124-second artifacts tier was running). Run
2, immediately after: **92 passed, 0 failed.** This is exactly what `pytest.ini`'s
`fold` marker documents, one scale up: not only leg 1's two builds racing, but a
session-scoped built index going stale against a live tree.

## 7. Environment, recorded

**One change: the SDK install.** E17 recorded zero changes; this is what moved.

```
pip install mcp==2.0.0
  -> mcp 2.0.0, mcp-types 2.0.0, pydantic 2.13.4, pydantic-core 2.46.4,
     annotated-types 0.8.0, typing-inspection 0.4.2, httpx2 2.9.1,
     httpcore2 2.9.1, starlette 1.5.0, sse-starlette 3.4.8, uvicorn 0.52.1,
     python-multipart 0.0.32, pyjwt 2.13.0, cryptography 50.0.0, cffi 2.1.1,
     pycparser 3.0, truststore 0.10.4, opentelemetry-api 1.44.0, pywin32 312
```

Wheels only, no compiler. The pre-existing 32-test suite was re-run immediately
after the install and was green, so nothing the pinned scientific stack depends
on moved. Everything else is as E17 recorded it: Python 3.13.13 locally (CI
3.12), pytest 9.1.1, numpy 2.4.6, scipy 1.17.1, pillow 12.2.0, trimesh 4.12.2,
open3d 0.19.0.

`mcp` joins `conftest`'s measured interpreter table beside `open3d`:
`record_mcp.py` imports it at module level, so a wrong interpreter would
reproduce E17 Ruling 2's partial-green misreading through the stdio test.

## 8. D4 — the live dogfood, all three states, over the mount path

**P9 held: this session cannot mount its own server.** Claude Code reads
`.mcp.json` at session start and this session started before the file existed; a
name lookup for `mcp__facet-record__record_health` returns nothing. Stated in
advance as the deliverable most likely to land half, and it did.

**What was done instead is the same wire, not a substitute for it.** The driver
reads `.mcp.json`, spawns **exactly** the command and args it declares with the
repo as cwd, and speaks MCP over the child's stdio — which is what a mounted
session does. Everything runs against a scratch `--db`; the tracked index is
untouched. The FAILED state is fired by hand-editing the scratch DB and letting
the **real four legs** catch it, not by editing a certificate.

The in-session mount is available to the next session started in this repo, and
`.mcp.json` is committed for it.

```
==============================================================================
E18 D4 - dogfood over the .mcp.json mount path
==============================================================================
command: E:\AI-Models\trellis2-env\Scripts\python.exe
args:    ['tools/record_mcp.py']
cwd:     E:\AI\facet
db:      C:\Users\mikey\AppData\Local\Temp\claude\E--AI-facet\45bdddfd-d0c7-4df4-a673-4e1c484b23b7\scratchpad\dogfood\facet.db   (scratch; the tracked index is untouched)

server:  facet-record v0.0.0
tools:   6
  record_query    readOnlyHint=True  destructiveHint=None
  record_get      readOnlyHint=True  destructiveHint=None
  record_build    readOnlyHint=None  destructiveHint=False
  record_verify   readOnlyHint=None  destructiveHint=False
  record_health   readOnlyHint=True  destructiveHint=None
  record_claims   readOnlyHint=True  destructiveHint=None

------------------------------------------------------------------------------
STATE 3a - REFUSING: there is no index at all
------------------------------------------------------------------------------
  serving:           false
  state:             "REFUSING"
  error:             {"error": true, "code": "INDEX_MISSING", "message": "no index at C:\\Users\\mikey\\AppData\\Local\\Temp\\claude\\E--AI-facet\\45bdddfd-d0c7-4df4-a673-4e1c484b23b7\\scratchpad\\dogfood\\facet.db", "hint": "Run python tools/facet_index.py build   (or call record
  record_query against it:
  is_error: true
  | Error executing tool record_query: REFUSED: no index at C:\Users\mikey\AppData\Local\Temp\claude\E--AI-facet\45bdddfd-d0c7-4df4-a673-4e1c484b23b7\scratchpad\dogfood\facet.db
  |   code:      INDEX_MISSING
  |   message:   no index at C:\Users\mikey\AppData\Local\Temp\claude\E--AI-facet\45bdddfd-d0c7-4df4-a673-4e1c484b23b7\scratchpad\dogfood\facet.db
  |   hint:      Run python tools/facet_index.py build   (or call record_build)
  |   retryable: true
  | {"code": "INDEX_MISSING", "error": true, "hint": "Run python tools/facet_index.py build   (or call record_build)", "message": "no index at C:\\Users\\mikey\\AppData\\Local\\Temp\\claude\\E--AI-facet\\45bdddfd-d0c7-4df4-a673-4e1c484b23b7\\scratchpad\\dogfood\\facet.db", "retryable": true}

------------------------------------------------------------------------------
STATE 3b - REFUSING: a DB somebody produced, with no certificate
------------------------------------------------------------------------------
  (copied the tracked DB in; no certificate beside it)
  serving:           false
  state:             "REFUSING"
  error:             {"error": true, "code": "INDEX_NEVER_VERIFIED", "message": "the index at C:\\Users\\mikey\\AppData\\Local\\Temp\\claude\\E--AI-facet\\45bdddfd-d0c7-4df4-a673-4e1c484b23b7\\scratchpad\\dogfood\\facet.db carries no certificate", "hint": "A DB somebody produced i
  is_error: true
  | Error executing tool record_query: REFUSED: the index at C:\Users\mikey\AppData\Local\Temp\claude\E--AI-facet\45bdddfd-d0c7-4df4-a673-4e1c484b23b7\scratchpad\dogfood\facet.db carries no certificate
  |   code:      INDEX_NEVER_VERIFIED
  |   message:   the index at C:\Users\mikey\AppData\Local\Temp\claude\E--AI-facet\45bdddfd-d0c7-4df4-a673-4e1c484b23b7\scratchpad\dogfood\facet.db carries no certificate
  |   hint:      A DB somebody produced is not a verified DB. Run python tools/facet_index.py build   (or call record_build)
  |   retryable: true
  | {"code": "INDEX_NEVER_VERIFIED", "error": true, "hint": "A DB somebody produced is not a verified DB. Run python tools/facet_index.py build   (or call record_build)", "message": "the index at C:\\Users\\mikey\\AppData\\Local\\Temp\\claude\\E--AI-facet\\45bdddfd-d0c7-4df4-a673-4e1c484b23b7\\scratchpad\\dogfood\\facet.db carries no certificate", "retryable": true}

------------------------------------------------------------------------------
record_build - the E15 ritual as ONE act (build + the four legs)
------------------------------------------------------------------------------
  built:             true
  state:             "PASSED"
  determinism_leg:   "byte-identity"
  legs:              {"0_discovery": "PASSED", "1_determinism": "PASSED", "2_counts": "PASSED", "3_pointers": "PASSED", "4_seeded": "PASSED"}
  counts:            {"rulings": 534, "laws": 71, "experiments": 20, "handoffs": 31, "artifacts": 668, "phenomena": 27, "decisions": 225, "prose_sections": 2024, "fts": 3600}
  corpus_files:      231
  failures:          []
  andon:             []

------------------------------------------------------------------------------
STATE 1 - SERVING: certificate PASSED, corpus unchanged
------------------------------------------------------------------------------
  serving:           true
  state:             "SERVING"
  certificate:       {"state": "PASSED", "verified_utc": "2026-08-08T15:48:23Z", "determinism_leg": "byte-identity", "legs": {"0_discovery": "PASSED", "1_determinism": "PASSED", "2_counts": "PASSED", "3_pointers": "PASSED", "4_seeded": "PASSED"}, "verb": "record_build", "corpus_id
  staleness:         null

  record_query - a SEEDED question, asked in the record's own words
  seeded question: "the hollow finding"
  phrase:          "the hollow finding"
  known target:    docs/experiments/E14-ruling.md :: Ruling 3
    1. Ruling 3                 THE HOLLOW FINDING IS BANKED ROUTE-WIDE (2026- docs/experiments/E14-ruling.md:87
    2. first mentioned in docs/advisor-kickoff.md profiles/prop.json [data/ACCEPTED] 33 mentions docs/advisor-kickoff.md:14
    3. §3 — Task 2.2, the reach ceiling and the off-surface rate §3 — Task 2.2, the reach ceiling and the off-s docs/experiments/E14-handoff2-predictions.md:74
  rank-1 is the known target: True
  certificate on the response: {"state": "PASSED", "verified_utc": "2026-08-08T15:48:23Z", "determinism_leg": "byte-identity", "legs": {"0_discovery": "PASSED", "1_determinism": "PASSED", "2_counts": "PASSED", "3_pointers": "PASSED

  record_get - the rows the query pointed at, from the MARKDOWN
  docs/experiments/E14-ruling.md:87-100  (14 lines, truncated=True)
    | ## Ruling 3 \u2014 THE HOLLOW FINDING IS BANKED ROUTE-WIDE (2026-08-07)
    | 
    | **Every reconstruction this route has made is a hollow double-walled shell** \u2014
    | measured three mutually independent ways (ray-crossing counts, cross-section
    | clustering, signed volumes of separable walls) on all three candidates AND on
    | two out-of-family controls including the accepted dragon; wall thickness sits on
    | a hard floor of 0.00196\u20130.00213 against a ~1.0 bounding box, **almost exactly
    | two voxels of the 1024\xb3 grid** (the voxel arithmetic rides as a labelled
    | hypothesis \u2014 nobody opened the extractor). Invisible for eleven experiments
    | because the route only ever touches visible surface, and the cull excludes the
    | inner wall by construction. **Nothing banked is invalidated** \u2014 no recorded
    | claim asserted solidity, and the standing volumetric-predicate constraint gains
    | its deeper ground: E01's "signed distance at the chest centre reads *outside*"
    | is consistent with the chest centre sitting in the cavity, genuinely outside

  record_claims - report-only, exits 0 whatever it finds
  exit_code:         0
  gates:             false
  summary:           {"stale": 0, "ambiguous": 2, "unparseable": 10}
  stale_rows:        []

------------------------------------------------------------------------------
STATE 3c - REFUSING: the four legs FIRED for real
------------------------------------------------------------------------------
  hand-edited the scratch DB: dropped E16's numbered rulings
  (25 E16 rows before). This is the 'day it is hand-edited it is
   wrong by definition' case, done on purpose, in scratch.
  state:             "FAILED"
  legs:              {"0_discovery": "PASSED", "1_determinism": "PASSED", "2_counts": "FAILED", "3_pointers": "PASSED", "4_seeded": "PASSED"}
  failures:          ["count E16 numbered rulings: grep 7 != db 0", "E16 ruling sequence gaps [1, 2, 3, 4, 5, 6, 7]"]
  determinism_leg:   "byte-identity"
  record_query against a FAILED certificate:
  is_error: true
  | Error executing tool record_query: REFUSED: 2_counts: count E16 numbered rulings: grep 7 != db 0
  |   code:      INDEX_VERIFY_FAILED
  |   message:   2_counts: count E16 numbered rulings: grep 7 != db 0
  |   hint:      Run python tools/facet_index.py build   (or call record_build). If it still fails, the corpus moved something a row points at - the failing rows are in the certificate's transcript.
  |   retryable: false
  | {"code": "INDEX_VERIFY_FAILED", "error": true, "hint": "Run python tools/facet_index.py build   (or call record_build). If it still fails, the corpus moved something a row points at - the failing rows are in the certificate's transcript.", "message": "2_counts: count E16 numbered rulings: grep 7 != db 0", "retryable": false}
  record_health still answers (it is how you find out):
  serving:           false
  state:             "REFUSING"
  error:             {"error": true, "code": "INDEX_VERIFY_FAILED", "message": "2_counts: count E16 numbered rulings: grep 7 != db 0", "hint": "Run python tools/facet_index.py build   (or call record_build). If it still fails, the corpus moved something a row points at - the faili

------------------------------------------------------------------------------
recovery - one command, named in the refusal's own hint
------------------------------------------------------------------------------
  state:             "PASSED"
  determinism_leg:   "byte-identity"
  legs:              {"0_discovery": "PASSED", "1_determinism": "PASSED", "2_counts": "PASSED", "3_pointers": "PASSED", "4_seeded": "PASSED"}

------------------------------------------------------------------------------
STATE 2 - SERVING WITH A STALENESS BANNER: a REAL corpus move
------------------------------------------------------------------------------
  appended one line to docs/experiments/E18-index-mcp-report.md
  (this session's own deliverable - a legitimate corpus move,
   not a falsified certificate)
  serving:           true
  state:             "SERVING_STALE"
  banner: STALE INDEX: the corpus has moved since this index was built - 1 modified (docs/experiments/E18-index-mcp-report.md). Citations below are a faithful map of the OLDER record. Run python tools/facet_index.py build   (or call record_build) to refresh.
  moved:  {"modified": 1, "added": 0, "removed": 0}
  named:  ["docs/experiments/E18-index-mcp-report.md"]

  record_query still SERVES - staleness warns, it does not refuse:
  returned:          2
  state:             "SERVING_STALE"
  note: STALE INDEX: the corpus has moved since this index was built - 1 modified (docs/experiments/E18-index-mcp-report.md). Citations below are a faithful map of the OLDER record. Run python tools/facet_index.py build   (or call record_build) to refresh.

==============================================================================
end of dogfood transcript
==============================================================================
```

Read off that transcript, without interpretation:

- the six tools and their annotations arrive over the wire as §3's table;
- `INDEX_MISSING` and `INDEX_NEVER_VERIFIED` each refuse `record_query` with
  `is_error`, the code, the one fix command, and the machine-readable object;
- `record_build` is one act — build, four legs, certificate — in 231 corpus
  files;
- the seeded question *"the hollow finding"* returns
  `docs/experiments/E14-ruling.md :: Ruling 3` at **rank 1**, and `record_get`
  on that pointer returns fourteen lines of the markdown;
- `record_claims` exits 0 with 0 STALE;
- dropping E16's numbered rulings from the DB makes leg 2 fire for real
  (`count E16 numbered rulings: grep 7 != db 0`), the certificate goes FAILED,
  and every read tool refuses while `record_health` keeps answering;
- one `record_build` recovers it;
- appending one line to this report — a real corpus move by this session's own
  deliverable — puts the surface into `SERVING_STALE` with a banner naming
  `docs/experiments/E18-index-mcp-report.md`, and the query **still serves**.

*(That appended line is not in this file: the stub it was appended to was
replaced by this report. The move it caused is recorded above.)*

## 9. Flags for the advisor — decided by nobody here

1. **`BAD_ARGUMENT` is a tenth code, beyond §5's named minimum.** §5's set names
   failure modes of the index; none of them fits "limit 0" or a typo'd table
   name, and returning an empty result for a typo is worse than saying so.
   Named as an addition rather than folded in silently.
2. **An unreadable certificate routes to `INDEX_NEVER_VERIFIED`**, with a
   message that says "unreadable" rather than "absent". No new code was minted
   for it. Six corruption shapes are tested.
3. **A DB whose sha256 differs from the certificate's refuses.** This is not in
   §5's three-state table. The grounds: a build without its verify is the
   ungated state the E15 ritual closes, and a certificate describing a different
   artifact is no certificate for the one present. It is demonstrable
   (`test_t21_refuses_when_the_db_is_not_the_one_that_was_certified`) and it is
   the ruling's to keep or drop.
4. **The certificate is 35.6 KB** and carries the full verify transcript plus a
   231-entry manifest. It travels with the DB on the DB's cadence. Size and
   contents are the advisor's to accept — the alternative is a bounded
   transcript, at the cost of a `.dump` fallback being visible only in a
   response nobody kept.
5. **`record_claims` gates on health.** §5's table names only `record_query`.
   The reasoning: claims reads the index's measurements, so an untrustworthy
   index makes them untrustworthy. `record_build`/`record_verify`/`record_health`
   never gate.
6. **The certificate carries a fifth leg key, `0_discovery`.** The inverse
   guards (rows from files the glob does not discover) are not one of the four
   legs but produce their own failures; they were given their own bucket rather
   than being forced into leg 2.
7. **§4.2 says the server writes exactly two paths.** It does — but
   `facet_index.verify`'s leg 1 writes two per-process temp DBs beside the
   target and removes them on every path (E16 Ruling 3). Inherited, named here
   rather than left for a reader to find.
8. **`.mcp.json` pins an absolute rig interpreter.** The alternative is bare
   `python`, which on this rig is the exact trap E17 Ruling 2 closed. The cost
   is that the mount is rig-specific; T23 tests the file's shape everywhere and
   launches it only where that interpreter exists.
9. **A lane crossing, disclosed.** The D2 commit (`1b45201`) carries the E19
   session's uncommitted one-line `site/.astro/` addition to `.gitignore`,
   because git stages files rather than hunks and `.gitignore` needed my
   `!tests/fixtures/**` negation. Separately, a first attempt at the
   connection-leak commit swept up E19's two staged brand renames; it was undone
   with `git reset --soft` and re-made pathspec-scoped, and those renames are
   staged in their own lane exactly as they were. Nothing was pushed in between.
10. **The tracked DB and its certificate are both uncommitted**, per the
    session-boundary cadence. They must travel together: a committed DB without
    its certificate refuses, which is by design and will be a fresh clone's first
    experience until the standing kickoff build line runs.
11. **`SERVER_VERSION` is the placeholder `"0.0.0"`.** Nothing publishes, so
    nothing is versioned; a real version attaches on the day extraction happens.
12. **The full-suite race** (§6) is worth a disposition: three `fold` tests
    failed once against a corpus three sessions were writing. No isolation was
    invented here.

## 10. Commits, all local (unpushed)

```
c1b8f30  E18 blind predictions, committed before any server code was written
12f6381  E18 D1: the server + 55 tests (read-only, certificate, health, tools)
5c4fa27  E18 D1b + D3: the mount path and CI, each carrying its test
1b45201  E18 D2: the hermetic selftest fixture + T2b
89ffa23  E18: facet_index's two leaked sqlite connections, fixed at the root
<this>   E18 halts at its report
```

Interleaved in `git log` with E19's and E20's commits — three sessions in one
working copy, which is §6's finding and flag 9's cause.

**HALT.** The advisor rules at `E18-ruling.md`.

## 11. Standards compliance (this session)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the SDK is verified-then-pinned in `ci.yml`; every design decision carries its ruling or spec-section pointer in the code beside it; predictions were committed before any server code existed and are scored against their own text |
| ANDON_AUTHORITY | 3 | the deliverable IS an andon and it was FIRED, not asserted — the refusal ran against a hand-corrupted scratch DB and leg 2 caught it; the transcript parse refuses rather than degrading; the session halted on its own first-run failures five times and reports every one, including the two that were its own guards' defects |
| NAMED_COMPENSATORS | 3 | the two written paths are derived and regenerable (leg 1 guarantees the DB returns byte-identical); corpus writes are impossible by construction, checked by an AST walk with both directions demonstrated; nothing published, nothing spent; the one commit that crossed a lane was undone with `git reset --soft` and re-made scoped |
| DECOMPOSE_BY_SECRETS | 3 | conventions stay in `facet_index`, the seeded key stays in the corpus's own tool, the wire shape lives in the server; §6's config machinery is deliberately unbuilt at the extraction seam; `mcp_support.py` keeps the SDK out of `conftest` so an absent SDK cannot kill collection for tests that do not need it |
| UNCERTAINTY_GATED_HUMANS | 2 | twelve open calls are listed in §9 with their reasoning rather than folded in silently, and every one is one sentence to overrule. Scored 2, not 3: nothing in this session PAUSED for a human — it decided and reported, which is right for an executor seat but is not the standard's strongest form. **skip: none** |
| EXTERNAL_VERIFIER | 3 | the server grades nothing of its own — the verdict is `facet_index`'s four legs, whose leg-2 greps are written independently of the parser and whose seeded key lives outside the server; the read-only property is checked by an AST walk rather than promised; the fixture's twin runs the tool's own selftest; the connection leak was found by the dogfood, i.e. by a consumer, not by the code's author |
