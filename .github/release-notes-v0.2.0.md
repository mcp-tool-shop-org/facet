**The operator contract of the two installed commands.** A behaviour change to a
published CLI, so it takes a minor bump. Scope is what facet actually installs —
`facet-index` and `facet-mcp` — and no other tool in `tools/` is touched. Full
evidence: [E21](https://github.com/mcp-tool-shop-org/facet/blob/main/docs/experiments/E21-cli-contract-report.md).

## Changed

- **Exit codes now mean what the ship gate says they mean.** Measured *before* the
  change, through a subprocess, on twenty rows across both commands: a user error
  exited **2** (argparse's convention) and a runtime error exited **1** (CPython's
  default for an uncaught traceback). **The surface was inverted at both ends, not
  one** — the gate line had named only the argparse half, and the second inversion was
  found by running the matrix rather than by reading the code. Now: `0` ok, `1` user
  error, `2` runtime error.
- **`3` is declared and deliberately unused.** No verb of either command has a
  partial-completion path. `verify` reporting three passing legs and one failing one
  has *completed*, and reports a measured outcome. A code is not populated by
  inventing a path for it to describe.

## Added

- **No raw traceback reaches you without `--debug`.** An unexpected exception now
  leaves as a structured failure naming its cause and the next step. `--debug`
  restores the traceback and changes nothing else — same exit code with and without,
  and the artifact a `build` writes is byte-identical across the pair.
- **`--debug` is confined by test, not by intention.** A gate carries no skip flag, so
  the new flag is checked against that rule: an AST walk pins that the identifier is
  read only in the two functions deciding what gets *printed* after a failure has
  already been decided, and a fired gate still refuses with `--debug` set. The closed
  flag allowlist — the guard that exists to make a new flag expensive — widened by
  exactly one, in writing, with the condition attached.
- **30 new tests**, every code asserted through a subprocess (a console script's exit
  status is a property of a *process*; `main()` returning 2 is a different claim), and
  every code paired with a can-fail leg that must produce a *different* number.

## Unchanged, on purpose

Two outcome classes keep the codes they had, because what they deserve is a ruling and
not an executor's pick: **a failing `verify` leg** — its return value is also the
`verify_exit_code` field of the schema-versioned certificate that `record_health`
serves, so moving it moves a persisted artifact and not just a shell's `$?` — and **a
fired ANDON**. Both are reported with their options and consequences rather than
guessed at. `claims` stays `0` whatever it finds, which was already ruled.

## Not done, and named rather than quietly dropped

**Logging levels are not shipped.** The silent/normal/verbose boundary was reserved for
a ruling *before* it ships, and the census that ruling needs is now measured: of
`verify`'s 35 print sites, **zero are progress chatter** — they are separators, leg
headers, measurements and verdicts — and `facet-mcp` parses `verify`'s stdout to build
its certificate, so a quiet `verify` would break it. That is not a philosophical
objection to suppressing output; it is a live dependency.

## Install

```bash
npx @mcptoolshop/facet          # zero-prerequisite, SHA256-verified binary
pipx install facet-mcp==0.2.0   # or the Python package directly
```

Unchanged from v0.1.x: four accepted assets across four subject classes at zero
credits, a four-leg-verified SQLite+FTS5 index over the whole evidence trail, and the
open defects still named on the front page rather than in a footnote.

## Known, and open

The repo's ANDON gates are bare `assert` statements, which `python -O` and
`PYTHONOPTIMIZE=1` delete silently — measured, dispatched as E22, and **not fixed in
this release**. It does not affect the two installed commands' exit contract above; it
affects the measurement tools in `tools/`. Nothing is claimed corrupted. It is named
here because a release that knows about a defect and does not say so is the thing this
repo exists to avoid.

---

**Compensators:** `gh release delete v0.2.0 --yes` · `git push --delete origin v0.2.0` ·
`git tag -d v0.2.0` · `npm unpublish @mcptoolshop/facet@0.2.0` (72h) or `npm deprecate`
after · PyPI cannot re-upload a version — yank from project settings.
