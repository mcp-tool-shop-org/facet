# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

**A note on what a version means here.** A version in this file is a claim about
**the state of the record**: which experiments are closed, which assets the Director
has accepted, and what the tools measurably do at that commit. The tag carries it —
there is no manifest to bump. Every entry below points at the ruling that established
it, so a reader can check the claim rather than trust it.

## [Unreleased]

**A gate is never a bare `assert`.** [E22](docs/experiments/E22-gates-report.md)
converted the **88 ruled ANDON gate sites** in five write-path tools plus the two
published console scripts from `assert` to `raise AssertionError`, because `assert`
is a statement the interpreter is licensed to delete: `python -O` and
`PYTHONOPTIMIZE=1` removed them silently and execution continued past them. Measured
before the repair, on the pinned interpreter: the gate never spoke, the write
proceeded, the process exited `0`. That is strictly worse than the shell chain
[E08 Amendment 32] was written for — the chain at least let the ANDON print.

Every conversion is a **pure move**, and that is proved rather than asserted: the AST
of each of the seven files is identical to the negation rule applied to the same file
at the prior commit, over the whole module, and their comment tokens are unchanged.
The three named anchors reproduce — T7's byte-identical atlas replay (its sidecar json
too), the twin-projection anchor, and T26's three fired ANDONs. **No conversion was
reverted.**

**Exit code `4 = REFUSED` lands**, carrying [E21 Ruling 4]: a failing `verify` leg and
a fired ANDON both leave it, off the `1` they shared with a mistyped flag. `verify`'s
value is also the certificate's `verify_exit_code`, and `record_mcp.parse_verify` keys
on `rc != 0` rather than `rc == 1` — verified before the value moved — so the health
state machine is indifferent to which non-zero it is. The test fixture that carried
this as a hardcoded `1` now reads the tool's own constant.

**T30 rides the commit** — 27 cases, 14 functions — asserting that each converted gate
refuses under a normal interpreter **and** under `-O` **and** under
`PYTHONOPTIMIZE=1`, that the write-path gates leave nothing behind when they fire, and
that the `-O` legs are not vacuous (proved on a throwaway script, never on a facet
gate). **No test asserts that `PYTHONOPTIMIZE=1` disables a gate**; that would anchor
the defect. Suite 248 → 275.

**What this does NOT do, measured and reported rather than implied:** E22 converted
the 88 sites its scope ruled. A census taken at the same time found **278 of the 294
asserts in `tools/` carry the ANDON token**, not the 87 the dispatch inherited — so
**192 ANDON-carrying gates outside the five named tools are still bare asserts**, and
**175 of them sit before a write in their own scope**. Those are a finding for the
advisor, not a scope extension taken by an executor.

## [0.2.0] — 2026-08-08

**The operator contract of the two installed commands.** A behaviour change to a
published CLI, so it takes a minor bump. Scope was ruled to what facet actually
installs — `facet-index` and `facet-mcp` — and no other tool in `tools/` is touched.
The full evidence is [E21](docs/experiments/E21-cli-contract-report.md).

### Changed

- **Exit codes now mean what `SHIP_GATE.md` says they mean.** Measured before the
  change, through a subprocess, on twenty rows across both commands: a user error
  exited **2** (argparse's convention) and a runtime error exited **1** (CPython's
  default for an uncaught traceback). **The surface was inverted at both ends, not
  one** — the gate line had named only the argparse half. Now: `0` ok, `1` user
  error, `2` runtime error.
- **`3` is declared and deliberately unused.** No verb of either command has a
  partial-completion path. `verify` reporting three passing legs and one failing one
  has *completed*, and reports a measured outcome. A code is not populated by
  inventing a path for it to describe.

### Added

- **No raw traceback reaches an operator without `--debug`.** An unexpected exception
  now leaves as a structured failure naming its cause and the next step; `--debug`
  restores the traceback and changes nothing else. Proven rather than asserted: same
  exit code with and without, and the artifact a `build` writes is byte-identical
  across the pair.
- **`--debug` is confined by test, not by intention.** E08 Amendment 32 rules that a
  gate carries no skip flag, so the new flag is checked against that: an AST walk
  pins that the identifier is read only in the two functions that decide what gets
  *printed* after a failure has already been decided, and a fired gate still refuses
  with `--debug` set. T21's closed flag allowlist — the guard that exists to make a
  new flag expensive — widened by exactly one, in writing, with the condition
  attached.
- **T29, 30 tests**, every code asserted through a subprocess (a console script's
  exit status is a property of a *process*; `main()` returning 2 is a different
  claim), and every code paired with a can-fail leg that must produce a *different*
  number.

### Unchanged, and unchanged on purpose

Two outcome classes keep the codes they had, because what they *deserve* is a
ruling and not an executor's pick: **a failing `verify` leg** (its return value is
also the `verify_exit_code` field of the schema-versioned certificate that
`record_health` serves — moving it moves a persisted artifact, not just a shell's
`$?`) and **a fired ANDON**. Both are reported for the advisor with their options and
consequences. `claims` stays `0` whatever it finds, which was already ruled at
E15 Ruling 9b.

### Not done, and named rather than quietly dropped

**Logging levels are not shipped.** The dispatch reserved the silent/normal/verbose
boundary for the advisor to rule *before* it ships, and the census that ruling needs
is now measured: of `verify`'s 35 print sites, **zero are progress chatter** — they
are separators, leg headers, measurements and verdicts — and `record_mcp` parses
`verify`'s stdout to build the certificate, so a quiet `verify` would break it. That
is not a philosophical objection to suppressing output; it is a live dependency.

## [0.1.1] — 2026-08-08

**Fixes a defect that only exists in the artifact a user receives.**

`0.1.0`'s binary told operators the wrong thing about their own machine. Inside a
PyInstaller onefile, `__file__` lives in a temp extraction directory, so the server
resolved its default index against that — printing
`db: C:\Users\…\Temp\docs/index/facet.db`, a path that cannot exist — and every
refusal hint said *"run `python tools/facet_index.py build`"*, a command with no
`tools/` directory to run it in and possibly no Python at all.

- **The index default now resolves against the working directory when frozen**, which
  is the honest default: an operator runs `facet` from inside the checkout whose
  record they want served. An explicit `--db` or `$FACET_INDEX_DB` still wins.
- **The refusal hint follows the runtime** — `facet-index build --db <path>` (or the
  env var) in a binary, the source command in a checkout. Every refusal in this repo
  names the next step; the next step has to be one the reader can actually take.

**How it was found, because that is the transferable part.** Not by CI, which was
green; not by the wheel test, which passed; not by the console scripts, which ran.
Every one of those exercises the *source checkout*, where `REPO` is the repo and the
advice is correct. It was found by installing the published package and reading what
it printed. **A green pipeline verifies the thing it built, not the thing a user
receives** — T28 now exercises the frozen branch directly rather than trusting that a
source-tree run implies a binary run.

Also corrected, twice, and the second correction is the useful one: `npx
@mcptoolshop/facet` was reported as broken on Windows, then explained away as registry
propagation. **Both were wrong.** `npx` works from any ordinary directory, on both
versions, exit 0.

It fails in exactly one place — **inside facet's own checkout** — because the repo root
now declares `"bin": {"facet": …}` for the wrapper it publishes. npm resolves the
command against the local project first, that project has no `node_modules`, and the
shell reports `'facet' is not recognized`. A self-reference artifact of testing a
published package from inside the repo that publishes it. No user encounters it.

**The diagnosis took three attempts because the comparison was invalid.** The runs that
worked were from a temp directory and the runs that failed were from the checkout — the
version changed *and* the working directory changed, and the result was read as
version-specific. This repo's own law, committed again: *"one variable" is a property of
the dependency graph, not of the parameter you edited.* The Director found it with a
one-word question after two confident wrong explanations.

**218 tests, 218 passing** — 210 hermetic + 8 artifacts, counted at this commit. The
five new ones are T28, and they exercise the frozen branch directly rather than
inferring it from a source-tree run. *(The v0.1.0 entry below keeps 213/205 — that is
what that release actually shipped, and a blanket count update very nearly rewrote it.
A released version's record states what it was, not what came after.)*

## [0.1.0] — 2026-08-08

Cut at the close of the E19 treatment, at the Director's word. There is no manifest to
bump, so this version exists as a git tag and this heading and nothing else.

**Why 0.1.0 and not 1.0.0.** The Director set the number. It is the honest one: the
extraction gate is open, three testability seams are dispatched and untaken, and the
repo's own highest-value question (P5 — `fit_background` at frame-edge figures) has
never been looked at. A 1.0.0 would assert a stability this route has not earned yet.
What the four accepted assets earn is a *first* release, not a stable one.

### ⚑ Corrected 2026-08-08 at the v0.2.0 seat — these three entries were filed under `[Unreleased]`

They shipped here, in this release, and sat under `[Unreleased]` through **two tags**
before anyone read the section against the tag below it. **The measurement:**
`git show v0.1.0:CHANGELOG.md` puts the `[Unreleased]` heading at line 14 and
`[0.1.0]` at line 40 — so the block was already misfiled *at the moment the tag was
cut*, and this entry's own opening line says the release was "cut at the close of the
E19 treatment," which is exactly the work the block describes. Moved rather than
rewritten; nothing in the wording below is changed. They are restored here because a
released version states what it shipped, and this one was understating itself while a
front-door document told readers a live landing page was unreleased.

- **Presentation surface** (E19 treatment): a landing page, a six-page Starlight
  handbook rendered from the canonical `docs/handbook/`, the clay wordmark logo,
  `SECURITY.md` with a measured threat model, `SHIP_GATE.md`, `SCORECARD.md`, and
  this file.
- **A repo-knowledge entry** — thesis, architecture, conventions, environment traps,
  drift risks and three mapped relationships.
- **The README is a front door, not a changelog** (at the Director's word). It went
  from 867 lines to 208 by **relocating** — never deleting — the chronological arc
  narrative to [docs/arc-history.md](docs/arc-history.md), the durable findings and
  hard-won rules to [docs/findings.md](docs/findings.md), the tool status tables to
  [docs/tools.md](docs/tools.md), and the defect list to
  [docs/known-defects.md](docs/known-defects.md).

  **Nothing measured was lost, and that is audited rather than asserted:** every
  non-blank line of the old README was diffed against the union of its new homes.
  Three lines differ, and all three are the marketing tagline, deliberately rewritten.
  All six ⚠ annotations survive. Corrections stay in place beside the measurements
  that overturned them, exactly as before — they just live one click deeper.

### What v0.1.0 asserts

**Four accepted assets across four subject classes, at zero credits.**

- **W3, the character** — accepted 2026-08-04 at the Director's own zoom
  ([E08 Amendment 35](docs/experiments/E08-ruling-gate0.md)). Mix 68.8% reference /
  4.2% brush / 27.0% dilation against the rejected asset's 28.4 / 37.7 / 33.9.
- **The galleon** — accepted 2026-08-05 ([E04-ruling.md](docs/experiments/E04-ruling.md),
  29 rulings). The first non-character subject; every subject value drawn from
  `profiles/ship.json` and `canon/GALLEON-IDENTITY.md`.
- **The dragon** — accepted 2026-08-07 ([E12-ruling.md](docs/experiments/E12-ruling.md),
  Rulings 1–30). Designation to acceptance in three days; 87.49% of the surface a
  viewer can see is the accepted pair's own paint.
- **The longsword** — accepted 2026-08-08 ([E14-ruling.md](docs/experiments/E14-ruling.md),
  Rulings 1–35). The first portrait-framed subject; the drifted gem returned to
  garnet by arithmetic rather than regeneration.

**The record is instrumented.**

- `tools/facet_index.py` — SQLite+FTS5 over the whole record, verified on four legs
  (byte-identical determinism across interpreters, counts against independent greps,
  zero dangling pointers, a seeded question gate)
  ([E15-ruling.md](docs/experiments/E15-ruling.md)).
- **213 tests, 213 passing at two seats' hands** — 205 hermetic + 8 artifacts — plus the
  repo's first CI workflow, paths-gated and pinned
  (the harness at [E17 Ruling 5](docs/experiments/E17-ruling.md), which closed that arc
  at 32; [E18](docs/experiments/E18-ruling.md) rode 60 more in on the commits that built
  the record-index MCP; [E20](docs/experiments/E20-ruling.md) is adding the unit tier).
  Counted at this commit rather than inherited: `pytest --collect-only` over the
  committed `tests/` returns 213, and 205 with `-m "not artifacts"`. **The lineage is
  27 → 32 → 92 → 202 → 213 in a single day** — E20 closed and was ruled, then the
  extraction's own T27 added eleven more. Re-counted at the tagging commit before the
  tag was cut, per [E19 Ruling 7](docs/experiments/E19-ruling.md); that gate fired five
  times and caught a stale number on every one of them.
- The claims sweep (`facet_index.py claims`) reads **0 STALE** against the record.

**Four dense assets are in the training dataset**, 114 records across five ingests
([E11-ruling.md](docs/experiments/E11-ruling.md),
[E14 Ruling 34](docs/experiments/E14-ruling.md)).

### What v0.1.0 does NOT assert

- That the texture stage is finished. The blade band, the unlevelled stroke seams and
  the cross-island dilation bleed are named, measured and open — see **Known defects,
  named** in the README, which the treatment left standing word for word.
- That any claim in this repo is safe to inherit unchecked. Six inherited claims were
  falsified in the founding session alone; the corrections are kept in place beside
  the measurements that overturned them, which is the point.
