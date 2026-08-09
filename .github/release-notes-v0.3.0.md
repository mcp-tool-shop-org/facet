**The gates stop being deletable.**

`assert` is a statement the interpreter is licensed to remove. `python -O` and
`PYTHONOPTIMIZE=1` delete it silently — and this repo had been using it for the checks
that decide whether an irreversible step proceeds. Measured on one gate before the
repair, on the pinned interpreter:

```
python                      GATE FIRED
python -O                   GATE SILENT, execution continued past it
PYTHONOPTIMIZE=1            GATE SILENT, execution continued past it
```

The gate never spoke, the write proceeded, and the process exited `0`. That is worse
than the shell chain the original rule was written for — a chain at least lets the halt
print before walking past it.

**145 gates now `raise`.** [E22](https://github.com/mcp-tool-shop-org/facet/blob/main/docs/experiments/E22-gates-report.md)
converted 88 across the write-head, the index and the published server;
[E23](https://github.com/mcp-tool-shop-org/facet/blob/main/docs/experiments/E23-route-gates-report.md)
converted 57 more across the twelve route tools that produced four accepted assets. Every
one is a **pure move** — no message reworded, no condition tightened — and that is proved
by whole-file AST equality against the prior commit rather than by anyone reading a diff.
**No conversion was reverted.**

## Changed

- **A new exit code: `4 = REFUSED`.** A fired gate and a failing `verify` leg both leave
  with it — *the tool ran correctly and is telling you not to proceed*, which is neither
  a user error (`1`) nor a runtime error (`2`). `0`/`1`/`2` are unchanged, `3` stays
  reserved and unused. The certificate field and the test fixture now read the tool's own
  constant instead of a hardcoded integer, so they cannot drift apart from it.

## Added

- **Tests that the old construction made impossible.** Each converted gate is asserted to
  refuse under a normal interpreter **and** under `-O` **and** under `PYTHONOPTIMIZE=1`,
  with the write-path gates additionally leaving no artifact when they fire. The suite
  went **248 → 370**. No test asserts that `PYTHONOPTIMIZE=1` disables a gate — that
  would anchor the defect rather than close it.

## Known, and named rather than omitted

**134 ANDON checks are still bare `assert`s** — 132 in `tools/diagnostics/`, one in
`tools/verify/`, and one in `tools/superseded/` that will stay that way on purpose,
because those tools are kept so anyone can run them and watch them fail the same way.
None is in a command this package installs. That count is pinned by a test, so the next
arc's scope cannot drift silently.

One gate was found that **cannot fire at all** — shadowed by an earlier check on the only
path that reaches it. It is kept and annotated rather than deleted, because it is a
precondition on a function's contract and not on today's single call site.

## Install

```bash
npx @mcptoolshop/facet          # zero-prerequisite, SHA256-verified binary
pipx install facet-mcp==0.3.0   # or the Python package directly
```

Unchanged from v0.2.x: four accepted assets across four subject classes at zero credits,
a four-leg-verified SQLite+FTS5 index over the whole evidence trail, and the open defects
still named on the front page rather than in a footnote.

---

**Compensators:** `gh release delete v0.3.0 --yes` · `git push --delete origin v0.3.0` ·
`git tag -d v0.3.0` · `npm unpublish @mcptoolshop/facet@0.3.0` (72h) or `npm deprecate`
after · PyPI cannot re-upload a version — yank from project settings.
