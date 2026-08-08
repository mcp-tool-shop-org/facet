# E17 — blind predictions, committed before any port ran

**Executor session, 2026-08-08.** Dispatch:
[E17-harness-kickoff.md](E17-harness-kickoff.md). Written after reading CLAUDE.md,
the E17 dispatch, the E16 kickoff and its closed report, and `git log` — and
**before reading a line of any tool this session will port against**, matching
E16's discipline. Per port: predicted tier, predicted pass state, and a sharper
prediction where I have one. A wrong prediction is a finding.

## Session state at prediction time (it moved under me already)

The dispatch said E16 was live at its final errand. Between my `git pull` and my
first fresh `git status`, **E16-11 committed (`c284693`) and the E16 report
closed (`abe62a9`)** — the tree is clean now. So the dispatch's conditional is
resolved before the first port: **the E16-11 sweep port is IN scope**, with
`c284693` as its anchor; it enters below as T12. E16-5 stays excluded by name
(anchor FAILED, awaiting the ruling). The pre-existing stash (`stash@{0}`,
another seat's) stays untouched per E16-9's ledger.

## Scaffold and environment predictions

- **pytest is absent from the trellis2-env** (it is a model runtime, not a dev
  env) and will be installed; version recorded in the report.
- **No tool edit will be needed anywhere in this session.** The E16 report (§2)
  verified `build --db <other-path>` writes only its declared target. I predict
  `verify` accepts the same `--db`, so T1/T1b can build+verify a scratch DB —
  the `det_a` race and the tracked-DB write both disappear **without the
  scratch-`--out` tool change the dispatch anticipated**. If `verify` turns out
  not to take `--db`, the fallback is the dispatch's in-place shape behind the
  `fold` marker, and the tool change gets proposed in the report rather than
  made. Either way T1/T1b carry the `fold` marker with the race documented.
- All five artifacts-tier recorded trees exist on this rig (E16 replayed every
  one of them today), so locally the artifacts set RUNS — zero skips expected on
  this rig; the skip path is exercised by CI's absence of `E:\AI\training`, and
  every skip prints the exact missing path.

## Per-port predictions

| id | port | predicted tier | predicted state | the sharper prediction, where I have one |
|---|---|---|---|---|
| T1 | build+verify wrapper, PASSED read from position | hermetic (`fold` marker) | PASS | Scratch `--db` makes this genuinely hermetic with no tool change (above). The PASSED line is read as the final summary line of `verify` output at its position — I have not read the tool yet, so its exact form is a port-time fact, not assumed here. |
| T1b | encoding matrix | hermetic (`fold` marker) | PASS both legs | The port forces `PYTHONIOENCODING=cp1252` explicitly rather than relying on the platform default — the recorded crash condition (Ruling 31f) becomes reproducible on ubuntu CI, where the platform default is utf-8 and a "default encoding" leg would silently test nothing. |
| T2 | `texpass_iter` selftest | hermetic | PASS (exit 0) | E16-4 measured it unprofiled and ungated: `PASS`, write-head lossless, 377 texels. |
| T3 | unprofiled `emit` refuses | **hermetic** — the dispatch's open tier call | PASS (exit non-zero, message names the repair) | E16-4 recorded "0 job dirs written — it refuses before any output", so I predict the guard fires before any artifact input is touched, making the test hermetic. Two risks named now: (a) E16-10 recorded that `texpass_iter` **parses argv at import**, so the test must be subprocess-level (the porting rule prefers that anyway); (b) on CI an ImportError would also exit non-zero — the test must assert the guard's own message, not the exit code alone, or it is a check that cannot fail. |
| T4 | discovery + inverse guards (rulings and kickoffs) | hermetic | PASS: discovery covers the current corpus; a synthetic miss FIRES | The miss is injected by E16-9's method — a truncated discovered-list handed to the guard in-process — never a decoy `.md` in the shared tree. Predicts both guards (E15 Ruling 9a's for ruling docs, E16-9's for kickoff handoffs) are callable functions; if import side effects block that, the fallback is a scratch copy of the corpus, and that is a finding about the tool's testability. |
| T5 | claims sweep | hermetic | PASS: exit 0, 0 STALE; synthetic fixtures exercise range-vs-cardinal, starts-at-1, AMBIGUOUS | E16-11 measured `STALE: 0` on this corpus today. The synthetic-fixture half depends on the sweep's parser being reachable apart from the live corpus; I have not read the tool, so the mechanism is a port-time decision reported honestly. |
| T6 | line endings + `.gitattributes` | hermetic | PASS | The native check is `git ls-files --eol`: assert no `w/crlf` (and no `i/crlf`) on files git classifies as text, and `.gitattributes` tracked. E16-2 converted 17 files and pinned `eol=lf`; nothing has reintroduced CRLF since. |
| T7 | finalize replay | artifacts | PASS | Byte-identity asserted against the **recorded artifact's own bytes** (`a0f51101…`), not a literal sha in test code — the recorded file is the anchor. E16-3 replayed it twice today, both byte-identical. |
| T8 | `e08_ceiling` re-derivation | artifacts | PASS — **against E16-6's corrected pair, not the dispatch's** | The E17 dispatch repeats the E16 kickoff's conflation: `51.005%` is NOT an `e08_ceiling` output (it is the 0/45/135/180/225/315 set from two other code paths). The tool's own numbers are N6 = 1,871,948 (51.12%, evenly-spaced six, handoff 2) and N8 = 1,879,807 (51.3342%, thrice-matched). The port anchors on those; porting the dispatch's number as written would manufacture a failure E16-6 already explained. |
| T9 | `e12_elevated` converged reach | artifacts, `slow` (~17 s measured) | PASS within ±0.5 of 53.920 | Sharper: the tool is deterministic on a fixed grid, so on THIS rig I predict the repaired default reproduces E16-7's **53.967% exactly**, not merely within noise. The test's bound stays the dispatched "within ray-sampling noise" (±0.5, E16-7's own pre-registered width); the exact-repro expectation is mine, and its failure would be a finding about determinism, not about reach. |
| T10 | bg-probe report-only projection | artifacts, `slow` | PASS — all five outputs byte-identical | Anchored against the recorded projection outputs on the sword. Risk named: E16-11 just renamed keys in all four profiles; the renamed sites (`brush_cloud_step`, `texpass_iter`) do not include `project_twins`, and E16-11 re-ran the E16-4 and E16-10 anchors after the rename with byte-identity held — so I predict the projector unmoved. If T10 mismatches, `git log` on the profiles first: the record moves under this session. |
| T11 | edge-mode default byte-identity | artifacts | PASS — 4,344 texels, outputs byte-identical; `--edge-mode local` parses | The default was re-verified byte-identical twice today, including once AFTER the profile rename. "Parses" is ported as a real run of the local mode into scratch (exit 0), not an argparse trivia check; its texel count is reported, not asserted — adopting an expectation for an opt-in mode adopted nowhere is not the port's job. |
| T12 | registry sweep end-state (E16-11's port, condition met at `c284693`) | hermetic — predicted; the sweep reads `profiles/` + `tools/`, both in git | PASS against the committed table: beast exit 0 · 85/85 · `_per_invocation 3`; ship exit 0 · 85/85 · 3; prop exit 1 · exactly 1 UNDECIDED (pre-existing `texpass_brush prompt`); character exit 1 · 18 UNDECIDED · `_per_invocation 1` | The exit-1 profiles are pinned AS exit 1 with their exact UNDECIDED counts — the test asserts the recorded end-state, not "sweep passes". If the sweep imports heavy deps to introspect tools, the tier call moves, and that is a wrong-tier finding to report. |

## What would make these wrong

The two live risks are the shared copy (a fold or the MCP spec-session moving
the corpus mid-run — T1/T4/T5/T12 all read it) and the tier calls made before
reading the tools (T3's pre-load claim, T12's hermetic claim, T4/T5's
importability claims). Each is stated above so its failure is legible as a
finding rather than absorbed silently.
