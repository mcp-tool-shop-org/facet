**A patch for a defect that only existed in the artifact you actually download.**

`v0.1.0`'s binary was wrong about your machine. Inside a PyInstaller onefile,
`__file__` lives in a temp extraction directory — so the server resolved its default
index against that, printing `db: C:\Users\…\Temp\docs/index/facet.db` (a path that
cannot exist), and every refusal hint told you to run
`python tools/facet_index.py build` — a command with no `tools/` directory to run it
in, and possibly no Python at all.

## Fixed

- **The default index resolves against the working directory when frozen.** That is
  the honest default: you run `facet` from inside the checkout whose record you want
  served. An explicit `--db` or `$FACET_INDEX_DB` still wins, as before.
- **The refusal hint follows the runtime** — `facet-index build --db <path>` in a
  binary, the source command in a checkout. Every refusal here names the next step,
  and the next step has to be one you can actually take.

## How it was found

Not by CI, which was green. Not by the wheel test, which passed. Not by the console
scripts, which ran. Every one of those exercises the **source checkout**, where the
repo root is the repo and the advice is correct.

It was found by installing the published package and reading what it printed. **A
green pipeline verifies the thing it built, not the thing a user receives.** The new
tests exercise the frozen branch directly rather than trusting that a source-tree run
implies a binary run.

## Install

```bash
npx @mcptoolshop/facet          # zero-prerequisite, SHA256-verified binary
pipx install facet-mcp==0.1.1   # or the Python package directly
```

Unchanged from v0.1.0: four accepted assets across four subject classes at zero
credits, a four-leg-verified SQLite+FTS5 index over the whole evidence trail, and the
open defects still named on the front page rather than in a footnote.

---

**Compensators:** `gh release delete v0.1.1 --yes` · `git push --delete origin v0.1.1` ·
`git tag -d v0.1.1` · `npm unpublish @mcptoolshop/facet@0.1.1` (72h) or `npm deprecate`
after · PyPI cannot re-upload a version — yank from project settings.
