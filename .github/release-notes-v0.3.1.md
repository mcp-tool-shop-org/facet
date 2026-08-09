**The install that could not find the record.**

Every released version through v0.3.0 shipped a wheel whose two commands could not
locate the corpus they exist to serve. v0.3.0's own release notes named the defect at
publication — this is the arc that fixes it.

```
facet-index build          FAILED   resolved the record against <venv>/Lib
facet-index q <term>       FAILED   without an explicit --db
facet-index claims         FAILED   (v0.3.0's notes said this one worked; it did not)
```

**The root is now resolved by TESTING FOR THE RECORD** rather than by assuming a
location. From inside a checkout both commands find it. From anywhere else they exit
**`4` REFUSED**, naming both directories they tried and both markers they looked for —
a refusal instead of a wrong answer, which is the same rule the index MCP already
served under. Measured on a wheel built from `main` and installed into a clean venv.

`$FACET_INDEX_DB` is read by **both** commands now, and it selects which *index*,
never which *corpus*.

## Why four green releases shipped it

Every check exercised `--help`. `release.yml`'s wheel step said *verify the wheel runs
from a clean venv* and ran the one surface that needs no record — so the one thing the
package exists to do was the one thing nothing tried. **That step now runs a verb**, and
CI runs the artifacts tier it had been silently skipping.

## Changed

- **The deletable-gate class closes.** The last **133** ANDON sites across **43** files
  — the measurement instruments — now `raise` instead of `assert`, after v0.3.0's 88 and
  57. **278 converted in total.** Exactly **one** bare ANDON `assert` remains anywhere
  under `tools/`: `superseded/texpass_thin_mask.py`, permanently out of scope because
  those tools are kept so anyone can run them and watch them fail the same way. It is
  pinned **by name** so a future sweep cannot tidy it away.

  **None of the 133 is in this package** — the wheel ships `facet_index` and
  `record_mcp` only. This is an internal change, and the patch bump is not concealing a
  published behaviour change.

- **28 ANDONs that already `raise SystemExit`** across 12 files are unchanged and
  pinned. `SystemExit` survives `-O`, so none of them carried the defect.

## Added

- **The front door's counts are under a test.** It fails CI on any watched surface
  stating a stale count, and it caught a real drift on its first run that no
  coordination rule had seen. The matcher is phrase-shaped rather than proximity-shaped
  — a ±90-character window returned 45 hits of which six were not test counts at all.

*No suite total is quoted in these notes.* It is a live-moving number and a published
release note is a region the front-door count test deliberately does not sweep — so a
total written here is the one kind of count nothing catches when it goes stale.

## Install

```bash
npx @mcptoolshop/facet          # zero-prerequisite, SHA256-verified binary
pip install facet-mcp==0.3.1    # fixed in this version; run it from inside a checkout
```

Unchanged from v0.3.x: four accepted assets across four subject classes at zero credits,
a four-leg-verified SQLite+FTS5 index over the whole evidence trail, and open defects
named on the front page rather than in a footnote.

---

**Compensators:** `gh release delete v0.3.1 --yes` · `git push --delete origin v0.3.1` ·
`git tag -d v0.3.1` · `npm unpublish @mcptoolshop/facet@0.3.1` (72h) or `npm deprecate`
after · PyPI cannot re-upload a version — yank from project settings.
