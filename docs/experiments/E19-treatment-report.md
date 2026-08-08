# E19 — the full treatment: report

**Executor session, 2026-08-08.** Halts here for the advisor's ruling at
`E19-ruling.md`. Commits are local; nothing is pushed, tagged, released or
deployed. Predictions were committed at `7aab88a` **before** `shipcheck init` ran.

---

## 1. What the session did, in one paragraph

facet now has a presentation surface: a threat model, a security policy, a
changelog, a scorecard, a filled ship gate, a logo, a landing page, a six-page
Starlight handbook rendered from the canonical one, a repo-knowledge entry, and a
README that is 208 lines instead of 867. **No measured claim, correction or ⚠
annotation was deleted** — and that is audited mechanically rather than asserted
(§4). The session also found **four stale or blind things it was not looking for**,
three of them in the instruments this treatment was supposed to lean on (§6).

## 2. The shipcheck audit, verbatim

### Entry — immediately after `shipcheck init`, nothing filled

```
shipcheck audit

Checked:   1
Unchecked: 35
Skipped:   1
Pass rate: 3%

Remaining gaps:
  ○ `[all]` SECURITY.md exists (report email, supported versions, response timeline)
  ○ `[all]` README includes threat model paragraph (data touched, data NOT touched,
  ○ `[all]` No secrets, tokens, or credentials in source or diagnostics output
  ○ `[all]` No telemetry by default — state it explicitly even if obvious
  ○ `[cli|mcp|desktop]` Dangerous actions (kill, delete, restart) require explicit `
  ○ `[cli|mcp|desktop]` File operations constrained to known directories
  ○ `[mcp]` Network egress off by default
  ○ `[mcp]` Stack traces never exposed — structured error results only
  ○ `[all]` Errors follow the Structured Error Shape: `code`, `message`, `hint`, `ca
  ○ `[cli]` Exit codes: 0 ok · 1 user error · 2 runtime error · 3 partial success
  ...and 25 more

35 item(s) still need attention.

EXIT=1
```

`shipcheck init` reported **`Detected tags: [all]`** — no `npm`, no `pypi`, no
`cli`, no `mcp`.

### Exit — every A–D line answered

```
shipcheck audit

Checked:   11
Unchecked: 2
Skipped:   24
Pass rate: 85%

Remaining gaps:
  ○ `[all]` **STAGED, not skipped** — translations run locally via `translate-all.mj
  ○ `[all]` **STAGED, not skipped** — the exact `gh repo edit` command, the proposed

2 item(s) still need attention.

EXIT=1
```

**Exit 1 is the correct outcome**, per the protocol's recorded nuance: the audit is
a textual checkbox count and both remaining lines are soft-gate E items deliberately
held for someone else's hands (the advisor runs translations; the Director fires
Pages, and the metadata's homepage field is meaningless until he does).

**A denominator note.** The audit counts **37** lines where the gate has **35** —
it also counts the two example checkboxes inside the template's own "Checking off"
and "Skipping" fenced blocks. Every repo in the org therefore carries a permanent
+1 checked / +1 skipped from the template. Left alone rather than edited, because
editing the examples to flatter the count is precisely the move this repo forbids.

### The binding Phase-0 grep

```
$ grep -nE '^- \[ \]' SHIP_GATE.md | grep -v 'SKIP:'
69:- [ ] `[all]` Logo in README header
70:- [ ] `[all]` Translations (polyglot-mcp, 8 languages)
71:- [ ] `[org]` Landing page (@mcptoolshop/site-theme)
72:- [ ] `[all]` GitHub repo metadata: description, homepage, topics
```

Exactly four, all soft-gate E. **P12 held to the line.**

### Executed gates, not attested

| gate | result |
|---|---|
| **H — `shipcheck pack`** | `no publishable packages found`, **exit 0**. This is the npm-class SKIPs' evidence rather than my word for them |
| **G — `shipcheck front-door`** | skips gracefully: needs `@mcptoolshop/site-theme >= 2.0.0`, and the current published version is **1.7.0**. Re-checked after Phase 2 installed site-theme — still unavailable. **Not a pass; an unavailable check** |
| **F — `shipcheck dogfood`** | not run. facet has no dogfood-lab record and is not a dogfood-swarm subject |

## 3. Predictions, scored

15 predictions, blindness disclosed per row, committed before either subcommand ran.

| # | prediction | outcome |
|---|---|---|
| P1 | detector returns no `npm`/`pypi`, and **not** `cli` either — an `[all]`-only tag set | **HELD** — `Detected tags: [all]` |
| P2 | checklist does **not** shrink to detected tags; all items stamped; 0/31 at entry, exit 1 | **HELD in substance, one number wrong.** No filtering — `[mcp]`, `[vsix]`, `[desktop]` lines all present under `[all]`. But the live template has **35** items, not the 31 in `shipcheck.md`. The memory file's inventory is stale |
| P3 | ≤ 6 items truthfully checkable with no new files; named A4, C1, C3, D1 | **HELD** — 5 (A3, A4, C1, C3, D1). Four of five named; A3 was the one I did not |
| P4 | SKIP set is 12–16 items; 14 named | **MISSED — 23 SKIPs.** All 14 named held. The 9 I under-counted are the `[cli]` family (A5, A6, B2, B3, C4, C5) plus B1, D2, D3 — I had treated the CLI items as probably-applicable. The lesson P3's row named applies: more of this gate is structurally inapplicable than a manifest-only read predicts |
| P5 | zero credentials; ≥ 1 hardcoded absolute path in `tools/` | **HELD both halves** — zero matches on the full sweep; **114** absolute-path occurrences across 26 files, now disclosed rather than found by a reader |
| P6 | README threat model absent | **HELD** — written in Phase 0 as an addition |
| P7 | B1 structured error shape absent; honest disposition is a named SKIP, not a retrofit | **HELD** — the convention is `raise SystemExit("ANDON: …")` with the measurement that fired it; no `code`/`message`/`hint` anywhere |
| P8 | exit codes partially met; no 0/1/2/3 registry | **HELD** — `sys.exit(main())` gives 0-vs-nonzero; no registry |
| P9 | citing `e12_help_format_scan.py` for C4 would be citing a proxy | **HELD** — it gates help-string *formatting*, not accuracy. C4 SKIPs and says so |
| P10 | no logging levels; stdout **is** the measurement record | **HELD** |
| P11 | GitHub description empty and zero topics | **SPLIT.** Topics zero ✔, homepage empty ✔, **description already set** ✘. Per the row's own falsifier clause it is recorded verbatim in §8 before anything changes |
| P12 | audit exits 1 at Phase 0's end; grep returns exactly 4 bare E lines | **HELD exactly** |
| P13 | D3 needs no `ci.yml` edit — no manifest means no graph to scan | **HELD.** Named the cheapest executed alternative for the ruling anyway (§7) rather than editing another lane |
| P14 | `site-theme init` needs no root `package.json` | **HELD** — self-contained `site/` tree; facet's manifest-free root survived, so no npm-class SKIP re-opened |
| P15 | v1.0.0 has no manifest to live in — tag + CHANGELOG heading only; D2 SKIPs | **HELD** |

**13 held, 1 split, 1 missed.** The miss (P4) and the split (P11) both landed where
their own "what this would teach" rows said they would, which is the point of
writing those rows.

## 4. Law 1, audited mechanically

The Director redirected mid-session: *"the readme reads more like a changelog and
less like a readme. Let's sell the product and put most of what's on the readme
somewhere more appropriate. Translated the readme as it is would take forever."*

His word is above the dispatch, and it does not conflict with Law 1 — it
**relocates** rather than deletes, which is Law 1's substance exactly. So the
question became checkable: *did anything get lost in the move?*

```python
old = git show HEAD:README.md          # 758 non-blank lines
new = README.md ∪ arc-history ∪ findings ∪ tools ∪ known-defects
lost = [l for l in old if l.strip() and l not in new]
```

```
old README lines (non-blank): 758
LOST lines (present in old README, absent from every new file): 3
  L13   Turning a styled 2D concept into a textured 3D character — with the style applied
  L14   **on the asset** in texture space, not painted per view. Runs entirely on local
  L15   hardware, with no non-commercial dependency anywhere in the chain.
```

**Three lines, and all three are the marketing tagline I deliberately rewrote.**
Zero measured claims, zero corrections, zero ⚠ annotations lost — 6 in the old file,
all 6 present, 11 across the new set. The same check run after Phase 1 returned
**72 insertions, 1 deletion**, the deletion being the redundant `# facet` h1 the
protocol itself says to remove once the logo carries the product name.

This check is cheap and it is now the session's standing instrument rather than a
promise made once.

### Where the record went

| new file | lines | what |
|---|---|---|
| `docs/arc-history.md` | 446 | the chronological narrative, E07 → E15, corrections intact |
| `docs/findings.md` | 137 | the durable findings + the hard-won rules |
| `docs/tools.md` | 111 | status of every tool, including `superseded/` |
| `docs/known-defects.md` | 101 | everything not solved |

README: **867 → 208 lines.** Translatable, which the 867-line version was not — the
Director's stated reason.

## 5. Per-phase table

| phase | state | notes |
|---|---|---|
| **0 — shipcheck** | done | 3% → 85%. Every A–D line checked with evidence or SKIP-ed **with its reason and its re-open condition** |
| **1a — logo** | done, **by the Director** | He chose and pushed the clay **FACET** wordmark to `brand/logos/facet/readme.png` mid-session; verified live, HTTP 200. My generated four-asset composite is superseded as a logo and **kept as a showcase sheet** (`docs/brand/four-accepted-assets.png`) with its provenance corrected in place — it was claiming to be the logo, and after his push that claim was false |
| **1b–e — README** | done | Logo, three badges, footer, `# facet` h1 removed. **No "Landing Page: live" badge** — it would point at a 404 until Pages fires, which is the drift the dispatch names as this repo's cardinal sin. Staged as a one-line addition landing *with* Pages |
| **2 — landing page** | done | `site-theme init` v1.7.0; base `/facet`; builds clean; walked at desktop width |
| **3 — handbook** | done | **The handbook already existed** (the Director pointed at it). `docs/handbook/` stays the one copy; `docs/handbook/sync_to_site.py` renders it into Starlight. Six pages: three synced, three hand-authored |
| **4 — metadata** | **STAGED** | Commands, proposed values and pre-treatment restore values in §8 |
| **4 — review** | done | Link-checked every new and edited doc: 58 broken links found and fixed (all from the relocation), 0 remaining |
| **5 — repo-knowledge** | done | Never skipped, per the dispatch. `sync-dogfood` then `scan`; 8 notes, 3 relationships, 13 docs indexed |
| **6 — translations** | **STAGED** | Executor sessions defer; the advisor runs them at the fold, **before** any tag, per the release-ordering law |
| **7 — publish** | **STAGED** | Tag, release, Pages — all await the Director's word after the ruling |

### Every SKIP, with its reason class

23 SKIPs. They fall into four families, and each line in `SHIP_GATE.md` carries its
own **re-open condition** — a SKIP whose condition is unwritten is how a falsified
approach quietly becomes doctrine.

| family | items | reason |
|---|---|---|
| **nothing publishes until extraction** (ruled) | D5, D6, D7, D2 | no manifest, no package, nothing to pack. D5 is **executed** by Gate H, not attested |
| **no installed command surface** | A5, A6, B1, B2, B3, C4, C5 | facet is invoked as `python tools/<name>.py`. Each discloses the measured reality rather than hiding behind the tag — A5 additionally notes an `--allow-*` flag would be a **regression** against E08 A32, which put the gate inside the tool with no skip flag |
| **no MCP server on `main` at audit time** | A7, A8, B4, B5, C6 | E18 was in flight in the other lane. ⚑ **These re-open the moment E18's server lands, which it now has** — see §7 |
| **not that kind of artifact** | B6, B7, C7, D8, D9, D3, D4 | not a desktop app, VS Code extension, or daemon. D3/D4: no dependency manifest exists for a scanner or dependabot to read, and the org's own rule forbids dependabot unless requested |

## 6. What the session found that it was not looking for

Four, and three are in instruments this treatment was told to lean on.

**6a — the dispatch's own premise was stale.** This kickoff and the E19 row both say
*"the 27-test suite."* That was E17 **Ruling 1**. **Ruling 5** closed the arc at
**32/32** hours later, and `pytest --collect-only` over the committed `tests/`
returns **32** (24 hermetic + 8 artifacts). Every new surface carries 32, counted at
this commit. ⚑ `docs/experiments/README.md:30` still reads *"27 tests, 27 passed …
(19 hermetic + 8 artifacts)"* and is now stale against Ruling 5 — **out of this lane,
flagged not edited.**

**6b — the claims sweep cannot see this treatment's surfaces.** Law 1 gates on
`claims` reading 0 STALE after every content phase. But `claims()` iterates
`record_markdown()` = `CLAUDE.md` + `README.md` + `docs/**.md`. **`CHANGELOG.md`,
`SECURITY.md`, `SHIP_GATE.md`, `SCORECARD.md` and the entire `site/` tree are outside
it.** The gate's blind spot is exactly where Law 1's marketing surface lives.
Compensated by hand meanwhile — every count claim written on a new surface was
verified against the index directly (E04 29, E12 max 30, E14 max 35, confirmed by
query, not by trust). ⚑ The naive fix is wrong: `record_markdown()` also drives
artifact and phenomenon extraction, so widening it would pollute those tables. The
sweep needs its own list.

**6c — the sweep is structurally blind to prose status, second instance.** Its claim
families are ruling / handoff / amendment **counts**. `docs/handbook/index.md` still
described the longsword as *"pair ACCEPTED … its stroke lane dispatched"*, written
before E14 Ruling 32 accepted the finished GLB **the same day**, and said *"the three
subjects' numbers"* where there are four. Corrected in place with the ⚠ annotation
(handbook content is this lane). The record already named this class once — *the arc
outran its row and the sweep cannot see prose staleness.* It has now happened twice.
**Keeping a status current is a duty, not a gate.**

**6d — relocation moves claims out of the gated class.** The four new `docs/*.md`
files classify as **`unclassified`** rather than `historical`, because
`facet_index.py`'s `CURRENT_STATE` / `HISTORICAL_DIRS` lists are literal. `historical`
is the *correct* class for an arc history — it states its counts as of each fold,
which is exactly what `HISTORICAL_DIRS` exists for. ⚑ One-line fix, in E18/E20's
lane, named not touched. Fail-safe meanwhile: unclassified rows **report** rather than
gate, so nothing silently passes.

### And two things the eye caught that no gate would have

- **Section subtitles are not rendered via `set:html`** — only `hero.description` is.
  `<em>` and `<strong>` shipped as literal tags on the landing page's assets table.
  Rewritten as plain prose.
- **Hero `previews` collapse newlines**, so a two-line command ran together into one
  unreadable string. Each preview is now a single short line. Code-cards *do* preserve
  newlines (verified on the licence block), so the fix is scoped.

Both were invisible in the build output and obvious in the browser. This is the
repo's own *look at it, at full size* rule doing its job on a marketing surface.

### A guard that fired on its own correct output

`sync_to_site.py`'s stray-link ANDON ran **after** the link rewrites, so it flagged
the rewrites' own output (`../profiles/`) and halted a correct run. Fixed by scanning
the **source** for links no rule handles. That is this repo's own law — *a guard that
fires on a correct input is worse than no guard* — caught within an hour of writing
the guard.

## 7. Cross-lane wants — flagged, never edited

| # | want | lane | note |
|---|---|---|---|
| 1 | `docs/experiments/README.md:30` says 27 tests; Ruling 5 closed at 32 | advisor | §6a |
| 2 | the claims sweep needs its own file list, separate from `record_markdown()`, covering root-level `CHANGELOG/SECURITY/SHIP_GATE/SCORECARD` and `site/` | E18 / E20 (`tools/`) | §6b. Do **not** widen `record_markdown()` — it feeds artifact/phenomenon extraction |
| 3 | add the four relocated docs to `HISTORICAL_DIRS` (or an equivalent) | E18 / E20 (`tools/`) | §6d |
| 4 | **A7/A8/B4/B5/C6 re-open now that E18's server has landed.** `tools/record_mcp.py` is on `main`; those five `[mcp]` lines were SKIP-ed against a `main` that did not have it | E18 + advisor | The SKIPs carry the re-open condition in writing; someone must actually re-run them |
| 5 | D3 dependency scanning, if the ruling wants it executed rather than skipped: a `pip-audit` step over the versions `ci.yml` already pins | E18 (`ci.yml`) | one step; P13 held, so this is optional, not owed |
| 6 | `site-theme handbook`'s `secondaryCta` patch produces **invalid TypeScript** when the existing href is a template literal | upstream `site-theme` | repaired by hand here; the org invariant is preserved |
| 7 | the handbook playbook's halt criterion names `dist/_pagefind/`; current Starlight emits `dist/pagefind/` | upstream playbook | the index builds; the documented path is stale |
| 8 | `shipcheck.md` records the gate as **31 items**; the live v1.0.7 template has **35** | upstream memory | §3 P2 |

## 8. The staged release package

Nothing below has been fired.

### 8a — GitHub metadata

**Pre-treatment values, recorded for the compensator (measured 2026-08-08):**

```
description  "Styled 2D concept to textured 3D character: form-first reconstruction,
              polygon budget allocation, texture-space styling. Local and licence-clean."
homepageUrl  ""        (empty)
topics       none
```

**Proposed:**

```bash
gh repo edit mcp-tool-shop-org/facet \
  --description "A styled 2D concept becomes a textured 3D asset — style applied on the asset in texture space. Four accepted subject classes, local and licence-clean." \
  --homepage "https://mcp-tool-shop-org.github.io/facet/"

gh repo edit mcp-tool-shop-org/facet \
  --add-topic 3d --add-topic texturing --add-topic game-assets \
  --add-topic blender --add-topic python --add-topic diffusion \
  --add-topic comfyui --add-topic trellis --add-topic pipeline
```

**Compensator:** restore the description verbatim from the block above, clear the
homepage with `--homepage ""`, and `--remove-topic <t>` for each of the nine.
Owner: advisor. Window: forever.

**Held because** the homepage field points at a Pages URL that 404s until the deploy
fires. It should go in the same breath as Pages, not before.

### 8b — Translations (advisor runs; before any tag)

```bash
node E:/AI/polyglot-mcp/scripts/translate-all.mjs E:/AI/facet/README.md
```

Then `git add README.md README.*.md` and commit **together**. The release-ordering
law is the reason: a tag is immutable, so translations must land in the same commit
family as the README they translate or the tagged commit carries stale ones forever.

The README is now **208 lines** rather than 867, which is the Director's stated
reason for the restructure.

### 8c — v1.0.0

`CHANGELOG.md` carries the proposed entry, and it states **what the version asserts
and what it does not**. There is no manifest to bump (P15): the version lives as a
git tag and that heading, and the CHANGELOG says so rather than implying a package.

```bash
git tag -a v1.0.0 -m "facet v1.0.0 — four accepted assets across four subject classes"
git push origin main
git push origin v1.0.0
gh release create v1.0.0 --title "facet v1.0.0" --notes-file <notes>
```

**Draft release notes:**

> **Four accepted assets, four subject classes, zero credits.**
>
> facet turns a styled 2D concept into a textured 3D asset, with the style applied on
> the asset in texture space rather than painted per view. This tag marks the state of
> the record, not a package — nothing here publishes until the ruled extraction gate.
>
> - **The character** (2026-08-04), **the galleon** (2026-08-05), **the dragon**
>   (2026-08-07) and **the longsword** (2026-08-08), each ruled at the Director's own
>   zoom on the finished GLB or full-size sheets.
> - **A pipeline, not a one-character generator** — contradict the specification on
>   eight named elements and the prompt wins 8 of 8.
> - **32 tests** at two seats' hands, paths-gated CI, and a four-leg-verified SQLite
>   index over the whole evidence trail.
> - **What is not solved is on the front page**: the blade band, the unlevelled stroke
>   seams, the cross-island dilation bleed, the hollow double-walled shells.
>
> Compensators: `gh release delete v1.0.0 --yes`, `git push --delete origin v1.0.0`,
> `git tag -d v1.0.0`.

### 8d — GitHub Pages

`.github/workflows/pages.yml` is committed — the repo's **second and last** workflow,
so the studio's two-workflow cap lands exactly. Enablement is manual and irreversible
enough to need his word:

> Repo → Settings → Pages → Source → **GitHub Actions**, then push any change to `site/`.

**Compensator:** set Pages source back to None, or `git revert` the offending commit
and let the workflow redeploy the prior state. CDN cache may serve stale content for
up to ~10 minutes.

## 9. Preview paths for the advisor's eye

Built locally and walked at desktop width. Rebuild and serve with:

```bash
cd site && npm install && npm run build && npm run preview
```

| surface | path |
|---|---|
| Landing page | `site/dist/index.html` → `/facet/` |
| Handbook home | `site/dist/handbook/index.html` |
| Getting started | `site/dist/handbook/getting-started/index.html` |
| The subjects *(synced)* | `site/dist/handbook/subjects/index.html` |
| Subject profiles *(synced)* | `site/dist/handbook/profiles/index.html` |
| Tool reference | `site/dist/handbook/reference/index.html` |
| How this repo is run | `site/dist/handbook/how-this-repo-is-run/index.html` |
| Search index | `site/dist/pagefind/` |
| The logo, live | `https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/facet/readme.png` |
| The showcase sheet | `docs/brand/four-accepted-assets.png` |

The advisor's eye is owed the landing page and all six handbook pages at full size,
then the Director's.

## 10. Gates, at every content phase

| after phase | claims sweep |
|---|---|
| entry (baseline) | **0 STALE**, 2 AMBIGUOUS, 10 UNPARSEABLE |
| Phase 0 | **0 STALE**, 2, 10 |
| Phase 1 | **0 STALE**, 2, 10 |
| Phases 2–3 | **0 STALE**, 2, 10 |

The two AMBIGUOUS and ten UNPARSEABLE rows are unchanged from entry — this session
introduced none. **Read §6b before reading this table as reassurance:** the sweep
could not see four of the five root-level surfaces this session created, so 0 STALE
is a true statement about a smaller set than it appears to cover.

Other gates: handbook drift `sync_to_site.py --check` → clean; `site npm run build` →
7 pages, pagefind index built; link check over every new and edited doc → 0 broken.

## 11. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | tool versions recorded where they mattered (`shipcheck` 1.0.7, `site-theme` 1.7.0, the pinned `ci.yml` install set); the protocol's own `treatment.lock` remediation is P2 upstream and inherited honestly rather than papered over |
| ANDON_AUTHORITY | 3 | shipcheck was a real entry gate; the claims sweep ran after every content phase; the sync script's own ANDON fired, was found to fire on correct input, and was **fixed rather than loosened** |
| NAMED_COMPENSATORS | 3 | every irreversible act is staged with its command **and** its undo, and the pre-treatment metadata values are recorded verbatim before anything changes (§8a). Nothing irreversible was fired in-session |
| DECOMPOSE_BY_SECRETS | 3 | the lane held under pressure — four cross-lane wants were flagged and none edited. The handbook is generated from one source rather than duplicated, for a stated secrets reason: the source is inside the claims sweep and the rendered copy is not |
| UNCERTAINTY_GATED_HUMANS | 3 | the one genuinely blocking uncertainty — pushing an unjudged logo to the org's indexed brand registry — went to the Director rather than being resolved by assumption, and he answered by choosing a different mark entirely |
| EXTERNAL_VERIFIER | 2 | shipcheck's audit and Gate H, the claims sweep, and the link check are all outside this session's authorship. Gate G, the one true front-door verifier, is **unavailable** (needs site-theme ≥ 2.0.0, published is 1.7.0) — recorded as unavailable, not as a pass. skip: the protocol's different-family remediation is P1 upstream |

## 12. What this session did not do

No push, no tag, no release, no Pages deploy, no `gh repo edit`, no npm publish
(extraction-gated, ruled), no translations run in-session, no memory-store writes, no
subagent on any public surface, and no edit to `tools/`, `tests/`, `ci.yml`,
`.mcp.json`, `canon/`, `profiles/`, the citable trees, the seeded set, or any file
under `docs/experiments/` other than this report and the predictions.

`docs/index/facet.db` is left uncommitted per the session-boundary cadence.

**Halting here for the ruling.**
