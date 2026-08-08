# E18 — blind predictions, committed before any server code was written

Written by the executor 2026-08-08, from the dispatch
([E18-index-mcp-kickoff.md](E18-index-mcp-kickoff.md)), the contract
([index-mcp-spec.md](../specs/index-mcp-spec.md)), the placement memo, the E17
ruling, and a read of `tools/facet_index.py`, `tools/texpass_iter.py` and the
existing harness. **No line of `tools/record_mcp.py` exists yet; no fixture has
been generated; the `mcp` SDK is not installed.**

**Blindness is disclosed per row, not claimed wholesale.** Two facts were looked
up before this file was written and are therefore NOT predictions: the current
`mcp` release on PyPI (`pip index versions mcp` -> 2.0.0 latest, nothing
installed in the trellis2-env), and the shape of `facet_index`'s public
functions (read from source). Everything below is stated before the thing it
predicts was attempted.

| # | prediction | blind? |
|---|---|---|
| P1 | `mcp==2.0.0` installs into the trellis2-env (Python 3.13.13) from wheels, no compiler, and does not disturb the pinned numpy/scipy/pillow/trimesh/open3d set the suite depends on | yes |
| P2 | the 2.0.0 SDK still exposes a decorator-based high-level server (`FastMCP`-class) and tool **annotations** (`readOnlyHint`, `destructiveHint`) are expressible there without dropping to the low-level `Server` API | yes |
| P3 | the same pin is installable on CI's Python 3.12 (the SDK's `requires-python` floor is <= 3.10) | yes |
| P4 | **no edit to `tools/facet_index.py` is needed** for any of the six tools; the server imports `build`, `verify`, `query`, `claims`, `SEEDED`, `record_markdown`, `PROFILE_FILES` and adds nothing to that module | partly — the source was read, the attempt was not made |
| P5 | `facet_index.verify()` returns only an int and prints its legs, so the certificate's per-leg state must be **parsed from verify's own transcript**; the parse will find all four leg headers and both verdict lines on the live corpus first run | partly — same |
| P6 | `record_get` has no existing implementation to wrap: bounding a row's own block from `locator` + `line` + the next heading / bold lead is new code, and it will resolve **all 19 seeded targets' anchors** on the live corpus | yes |
| P7 | the read-only guard (AST over `record_mcp.py`) passes first run, and fires on a synthetic source carrying a corpus write — both directions demonstrated | yes |
| P8 | the three health states are all reachable in scratch: PASSED-current, PASSED-stale (banner names the moved file), and refusal on **both** an absent and a corrupted certificate | yes |
| P9 | **the live `.mcp.json` mount will NOT be exercisable inside this session** — Claude Code reads `.mcp.json` at session start and this session started before the file existed. The protocol-level proof will be produced with the SDK's own stdio client (the same wire a mount speaks), and the in-session mount is available to the next session started in this repo. Called out now as the deliverable most likely to land half | yes |
| P10 | the T2 hermetic fixture needs exactly `state/{atlas.png,holes.png,styled_mask.npy}`, `prep/{meta.json,mask.npy}` and a UV-bearing GLB — nothing else from the recorded trees — and lands **under 100 KB total** | partly — the tool's module-level loads were read; the size is blind |
| P11 | the fixture's selftest run **commits > 0 texels and carries > 0 styled texels** on first construction — i.e. the hermetic twin is non-vacuous without a second attempt at the geometry | yes |
| P12 | new hermetic tests: **14–20**; whole-suite total after this session **41–49**; and **1–2 first-run failures** among them, mine rather than the record's | yes |
| P13 | the corpus manifest covers **70 +/- 10 markdown files + 3 profile JSONs** | yes |
| P14 | `record_claims` reports **0 STALE** rows against the corpus as it stands at this session's start | yes |
| P15 | wall time for `record_build` (one build plus verify's own two, plus the four legs) is **under 30 s** on this rig | yes |

## What would make each miss informative

- **P2 falsified** -> the annotations ride the low-level API and the report says
  so; the spec's §3 table is unchanged either way.
- **P5 falsified** -> either verify grew structure (it had none at this commit)
  or the transcript parse is fragile. A fragile parse must fail LOUDLY
  (certificate FAILED, health refuses), never pass silently, and that direction
  is the one the tests pin.
- **P9 held** -> D4 lands as a protocol transcript plus a committed mount path,
  and the mounted-session half is named as the next session's rather than
  asserted as done.
- **P11 falsified** -> the fixture is a check that cannot fail and must be
  rebuilt until the write head is actually exercised, or reported as blocked.
- **P14 falsified** -> a STALE row is a finding for the advisor, never an edit
  here: the corpus is not written by this session for any reason.

## Out of scope, restated so a later reader does not have to infer it

No publish, no repo, no version bump, no landing page, no §6 config machinery,
no seeded-set edits, no corpus writes, no measurement-MCP work, no re-litigating
the ranking, no memory-store writes.
