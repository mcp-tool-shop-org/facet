# E19 — blind predictions on shipcheck's entry state

**Written 2026-08-08 by the E19 executor, committed before `shipcheck init` or
`shipcheck audit` was run.** Blindness is disclosed **per row**, not claimed
wholesale — the E18 precedent. Some facts were looked up first, because a
prediction made from total ignorance teaches nothing; those are listed below as
facts and are **not** predictions.

---

## Facts established before predicting (NOT predictions)

| # | fact | how |
|---|---|---|
| F1 | Repo root carries `LICENSE`, `README.md`, `CLAUDE.md`, `pytest.ini`, `.gitattributes`, `.gitignore`, `.github/workflows/ci.yml`, and the `canon/ docs/ profiles/ tests/ tools/` trees. It carries **no** `SECURITY.md`, **no** `CHANGELOG.md`, **no** `SHIP_GATE.md`, **no** `SCORECARD.md`, and **no dependency manifest of any kind** — no `package.json`, no `pyproject.toml`, no `requirements.txt`. | `ls -la` |
| F2 | `origin` → `https://github.com/mcp-tool-shop-org/facet.git`, branch `main`, **0 git tags**. | `git remote -v`, `git tag` |
| F3 | `ci.yml` is the repo's only workflow: ubuntu-latest, paths-gated, `workflow_dispatch`, concurrency block, pinned installs, hermetic pytest set. **No dependency-scanning step. No dependabot.** | read the file |
| F4 | `tests/` carries 16 files (E17's 27 tests: 19 hermetic + 8 artifacts); `pytest.ini` present. | `ls tests/` |
| F5 | Claims sweep at entry: **0 STALE**, 2 AMBIGUOUS, 10 UNPARSEABLE. This is the baseline every content phase must return to. | `facet_index.py claims` |
| F6 | No `.mcp.json` on `main` — E18's server is in flight in the other lane and has not landed. | `ls .mcp.json` |
| F7 | The protocol records shipcheck's audit as a **textual checkbox count** that `exit(1)`s on any bare `- [ ]` lacking `SKIP:`, and does not distinguish hard gate A–D from soft gate E. | `full-treatment.md` Phase 0 nuance |

Everything below is written without having run either shipcheck subcommand.

---

## The predictions

### P1 — repo-type detection

`shipcheck init` detects **no `npm` and no `pypi` tag**, because facet has no
manifest of either kind (F1). The uncertain half is whether it detects
**`cli`**: I predict **it does not** — detection almost certainly keys on
manifest files, not on scanning Python source for `argparse`. So I predict the
stamped header carries an **empty or `[all]`-only** tag set.

*If it detects `cli` anyway*, that teaches the detector reads source and not
just manifests — which matters, because it pulls B2/B3/C4/C5/A5/A6 into scope as
applicable rather than SKIP-able.

### P2 — does the checklist shrink to the detected tags?

**No.** I predict the template stamps **all 31 items** with their applicability
tags written inline, and the audit counts every bare line regardless of tag — so
a tag-inapplicable item still has to be hand-written as `SKIP:`. Audit
immediately after init therefore reports **0/31 checked and exits 1**.

*If the template is generated per-type and omits inapplicable lines*, the SKIP
work in Phase 0 roughly halves and the SKIP **reasons stop being visible in the
committed file** — which would be a real loss for this repo, where the reason is
the artifact.

### P3 — how many items are truthfully checkable with **no new files**

**≤ 6**, and I name the four I expect: **A4** (no telemetry — nothing in this
repo phones anywhere), **C1** (README current — it is the measured-state
document by construction), **C3** (LICENSE present; the "repo states support
status" half is the doubtful one), **D1** (verify script — the E17 suite + CI is
the verify story the dispatch names; whether `python -m pytest` satisfies "test +
build + smoke in one command" is the doubtful half).

### P4 — the SKIP set is **12–16 items**

Named, so a miss is legible: **A7, A8** (mcp — no server on `main`, F6), **B4,
B5** (mcp), **B6** (desktop), **B7** (vscode), **C6** (mcp), **C7** (complex —
facet's tools are one-shot scripts, not daemons), **D5, D6, D7** (npm/pypi — the
ruled npm-packaging class: nothing publishes until extraction), **D8** (vsix),
**D9** (desktop), **D4** (automated dependency updates — the org's own rule
forbids dependabot unless requested). That is **14**.

### P5 — A3, secrets

**Zero credentials in source.** But I predict **≥ 1 hardcoded local absolute
path** (`E:\AI\...` / `E:\AI-Models\...`) in `tools/`, which is not a secret and
does not fail A3, but does belong named in the threat model rather than
discovered by a reader. Falsifier: any token-shaped string anywhere in the tree.

### P6 — A2, the README threat model

**Absent** as shipcheck means it. The README's "Licence position" section is a
supply-chain statement, not a threat model — there is nothing about data
touched, data *not* touched, or permissions. This is new writing in Phase 0, and
under Law 1 it is an **addition**, not a rewrite.

### P7 — B1, the structured error shape

**Not met**, and this is the item I predict is the most expensive honest answer
in Phase 0. facet's tools are research instruments that halt with prose
messages; there is no `code`/`message`/`hint` registry anywhere. I further
predict the honest disposition is a **SKIP or an explicit unchecked with a named
reason**, not a retrofit — retrofitting an error contract across ~30 instruments
would touch `tools/`, which is **E18's lane**, and is far outside a treatment's
scope. *A pleasant miss would be finding a structured shape already present.*

### P8 — B2, exit codes

**Partially met.** `facet_index.py verify` returns an int exit code and T18's
interpreter pre-check is a single loud refusal — so the *behaviour* of 0-vs-
nonzero exists. But **0/1/2/3 as a documented registry: absent.**

### P9 — C4, `--help` accuracy

I predict the temptation here is to cite `tools/diagnostics/e12_help_format_scan.py`
as evidence, and that **citing it would be citing a proxy**: that linter gates
help-string *formatting* (literal `%`, non-cp1252 glyphs), not *accuracy*. I
predict C4 has to be checked by hand, scoped to the tools the treatment actually
presents to a reader, and says so in its line.

### P10 — C5, logging levels

**Not met.** facet's tools print measurements to stdout unconditionally, because
in this repo **stdout is the measurement record** — that is the design, not a
gap. I predict the honest disposition is SKIP with exactly that reason.

### P11 — the E section and the GitHub repo's current metadata

All four E items bare at entry. I predict `gh repo view` shows an **empty
description and zero topics** — the repo was pushed without metadata ever being
set. Falsifier: any existing description or topic, which I would then record
verbatim as the compensator's restore value before changing anything.

### P12 — the audit's exit code when Phase 0 is genuinely done

**1**, per F7 — and the binding deliverable is the grep, which I predict returns
**exactly 4 bare lines**, the four E items.

### P13 — the cross-lane hazard

The one hard-gate item whose obvious fix would edit `.github/workflows/ci.yml`
(**E18's lane**) is **D3, dependency scanning in CI**. I predict it does **not**
become a cross-lane want, because facet has no dependency manifest at all (F1) —
there is nothing for a scanner to scan, so D3 SKIPs on its own terms without
touching `ci.yml`. *If instead I find myself wanting a CI edit, that is a FLAG
for the ruling, never an edit.*

### P14 — does `site-theme init` need a root `package.json`?

I predict **no** — it writes a self-contained `site/` tree carrying its own
`package.json`, and facet's manifest-free root survives Phase 2 untouched.
*Falsifier: an error demanding a root manifest.* That would be the session's
sharpest decision point, because adding a root `package.json` would re-open
every npm-class SKIP in P4 and change what facet claims to be.

### P15 — where does "v1.0.0" live?

facet has 0 tags (F2) and **no manifest carrying a version field** (F1). So I
predict the version cannot be "bumped" anywhere: it lands as a **git tag plus a
CHANGELOG heading and nothing else**, and **D2** ("version in manifest matches
git tag") SKIPs on the no-manifest reason rather than being checked. The v1.0.0
proposal is therefore a claim about the *record's* state, not about a package.

---

## What each miss would teach

| miss | lesson |
|---|---|
| P1 wrong (cli detected) | shipcheck's detector reads source, not manifests — six more items are in scope than a manifest-only read predicts |
| P2 wrong (template filters) | SKIP reasons stop being visible in the committed file; this repo would need them written somewhere else, because the reason is the artifact |
| P3 low | the repo is further from the studio's baseline than its record suggests; more Phase-0 writing than the treatment budgets |
| P3 high | the record itself was already doing shipcheck's job — worth naming, since that is the thesis the landing page will make |
| P5 wrong (a token found) | an immediate halt and a security item, not a treatment item |
| P7 wrong (structured shape present) | the error contract arrived through some earlier discipline nobody wrote down — find and name it |
| P13 wrong (CI edit wanted) | the lane boundary is load-bearing here and the want goes to the ruling unedited |
| P14 wrong (root manifest demanded) | the treatment's scaffolding would change what facet *is*; that decision is the Director's, not this session's |
| P15 wrong (a version field exists) | there is a manifest this session did not find, and the npm-class SKIPs need re-deriving against it |
