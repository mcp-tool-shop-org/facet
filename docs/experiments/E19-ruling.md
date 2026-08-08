# E19 — the full treatment: ruling

**Advisor session, 2026-08-08 (night).** Rules on
[E19-treatment-report.md](E19-treatment-report.md). The report halted correctly:
nothing pushed, tagged, released or deployed by that session, every irreversible
staged with its compensator.

**The sheet-walk ran first, before any number in this ruling** — the practice binds
and it earned its keep again. Opened at full size, on the **live deployed site**
rather than local `dist/`: the landing page (`/facet/`) and all six handbook pages
(`handbook/`, `getting-started/`, `subjects/`, `profiles/`, `reference/`,
`how-this-repo-is-run/`), plus `README.md` and the relocation targets in source.

---

## Ruling 1 — THE TREATMENT IS ACCEPTED. The release is HELD on one repair.

The work is accepted on its substance. Shipcheck 3% → 85% with every A–D line
answered by evidence or by a SKIP carrying its own re-open condition; the README
relocation audited mechanically rather than asserted; the landing page and handbook
built, deployed and now walked; predictions committed before the subcommands ran and
scored honestly at 13 held / 1 split / 1 missed.

**Both of the session's own eye-caught defects are confirmed fixed on the live
surface.** Text extraction over the deployed landing page returns no literal `<em>`
or `<strong>` anywhere, and the three hero previews render as single readable lines.
Those were invisible in build output and would have shipped; the report's own
insistence on looking at it is why they did not.

**What the release is held on is Ruling 2**, and it is not a defect in this session's
work.

## Ruling 2 — THE TEST COUNT IS STALE ON THE LIVE PUBLIC FRONT DOOR. It blocks the tag.

The landing page says, right now, to anyone who loads it:

> **32 tests** passing at two seats' hands

The measured suite at this commit, under the pinned interpreter:

```
E:\AI-Models\trellis2-env\Scripts\python.exe -m pytest tests/ --collect-only -q
  at this session's open   -> 92 tests collected  (84 hermetic + 8 artifacts)
  at this fold's own gate  -> 202 tests collected (194 hermetic + 8 artifacts)
```

**202 total · 194 hermetic · 8 artifacts**, and the two readings above are four hours
apart in the same session — see the amendment at Ruling 7, which is the more important
half of this finding. The live site asserts **32** and **24**.

### This is not E19's error, and naming it correctly is the point

E19 wrote 32 when 32 was true, and said so explicitly — *"Counted at this commit
rather than inherited."* It went stale **the same day**, because E18 landed 60 tests
in the parallel lane. The surfaces carrying the number sit **outside the claims
sweep's file set**, which is the report's own §6b.

So §6b is not a theoretical blind spot. **It has already produced a false public
claim, within hours of being described.** That is the finding, and it is worth more
than the repair.

### Every site, with its correct value

The truth differs by site, because two of these are **historical** statements that
should say what was true *when they describe*, not 92. A find-and-replace would be
wrong here.

| file:line | reads | ruled value | class |
|---|---|---|---|
| `README.md:120` | 32 passing | **202** | live + about to be translated |
| `README.md:201–202` | all **32** / the **24** | **202** / **194** | same |
| `site/src/site-config.ts:116` | 32 tests passing | **202** | LIVE on the landing page |
| `site/…/handbook/getting-started.md:27` | the 24 hermetic | **194** | LIVE |
| `site/…/handbook/getting-started.md:30` | full suite is 32 | **202** | LIVE |
| `site/…/handbook/reference.md:61` | the 24 hermetic | **194** | LIVE |
| `CHANGELOG.md:69` | 32, 32 passing, 24 + 8 | **202 · 194 + 8** | frozen by the tag |
| `SHIP_GATE.md:57` (D1) | 32-test / 24 hermetic | **202 / 194** | gate record |
| `SCORECARD.md:21, 35` | 27 tests | **32** | historical — pre-remediation state |
| `docs/experiments/README.md:30` | 27 tests, 27 passed | **32** | historical — E17's end state |

`SCORECARD.md` is the one genuine miss in the session's own hands: §6a caught the
dispatch's stale "27" and corrected the premise, then 27 still stands twice in the
scorecard. That is this repo's own law — **when you fix a root cause, find its other
consumers** — and the fix is one grep. Named small because it is small.

### The ordering consequence, which is why this blocks

`README.md` carries the stale count twice and is the file the translations translate.
Fire them now and the number is wrong in eight languages, and then the **immutable
tag** freezes it. The release-ordering law exists for exactly this. **The repair lands
before the translations, in the same commit family as the README they translate.**

## Ruling 3 — PAGES IS LIVE. Three of the report's staged premises are void.

Measured: `https://mcp-tool-shop-org.github.io/facet/` returns **HTTP 200**, and the
"Deploy site to GitHub Pages" workflow is green at run `31266198261`. The report's §8d
("enablement is manual and irreversible enough to need his word") described the world
before that run.

1. **§8d is complete, not staged.** Pages needs no further word; it is deployed and
   serving.
2. **§8a's stated blocker is void.** The `gh repo edit` was *"held because the homepage
   field points at a Pages URL that 404s until the deploy fires."* It does not 404. The
   command still awaits the Director's word — it is an irreversible on a public
   surface — but its stated reason for being held has cleared.
3. **The "Landing Page: live" badge condition has fired.** §5 staged it as a one-line
   addition landing *with* Pages. Pages landed. It goes in with the Ruling 2 repair,
   before translations.

**And a governance change nobody has written down: a push touching `site/` is now a
deploy.** Before that run it was inert. The repo's standing practice is *push every
fold*; that practice now publishes to the public front door on any fold touching
`site/`. Recorded here so the next seat does not discover it by surprise.

## Ruling 4 — THE FIVE RE-OPENED `[mcp]` GATES, RE-RUN RATHER THAN RE-ASSERTED

A7/A8/B4/B5/C6 were SKIP-ed against a `main` with no MCP server. `tools/record_mcp.py`
is on `main`. The SKIPs carried their re-open condition in writing, so they re-open;
someone had to actually run them, and this seat did.

| item | contract | disposition | evidence |
|---|---|---|---|
| **A7** | Network egress off by default | **CHECK** | `record_mcp.py` imports no `socket`, `requests`, `urllib` or `http.client`; zero network calls in 868 lines. The transport is stdio. Egress is not "off by default" — it is absent |
| **B4** | Tool errors return structured results — server never crashes on bad input | **CHECK — fired live at this seat** | Two independent bad inputs through the mounted server: `limit=999` → `BAD_ARGUMENT` / *"limit must be between 1 and 50"* / hint; `table="not_a_table"` → `BAD_ARGUMENT` naming all eight valid tables. Both carry `code`/`message`/`hint`/`retryable`. **The server stayed up** — `record_health` answered normally in the same exchange |
| **B5** | State/config corruption degrades gracefully (stale data over crash) | **CHECK** | `health()`'s contract is *"Never raises — it returns the refusal instead"*, and the surface carries a literal `SERVING_STALE` state that serves the older record behind a banner naming the fix command. E18's dogfood fired this for real on a hand-corrupted DB: every read tool refused with its code, health kept answering, one `record_build` recovered |
| **C6** | All tools documented with description + parameters | **CHECK, with a noted boundary** | All six tools carry a description, and each documents its parameters with meaning and range in that description. The **JSON schema** carries no per-field `description` keys — the docs are in the prose a caller reads, not machine-readable per-parameter. Checked on substance; the schema gap is want 9 |
| **A8** | Stack traces never exposed — structured error results only | **CHECK, bounded — and the bound is stated** | Every deliberate refusal leaves through one site (`_raise`), so the wire shape has one implementation; measured twice above with no traceback. `record_build` additionally wraps *unexpected* exceptions into `INTERNAL` with the class name and message and no traceback. **The other five tools have no such wrapper** and rely on the framework's own error envelope for a genuinely unexpected exception. That is a real residual, not a pass by assumption — want 10 |

Four checks are unqualified. A8 and C6 are checked on substance with their residuals
written down rather than smoothed over, which is the form this repo requires of a
SKIP and should equally require of a check.

**`SHIP_GATE.md` moves 11 → 16 checked, 24 → 19 skipped.** The audit still exits 1 on
the two soft-gate E lines, which remains the correct outcome.

## Ruling 5 — THE CROSS-LANE WANTS, DISPOSED

| # | want | disposition |
|---|---|---|
| 1 | `docs/experiments/README.md:30` says 27 tests | **MINE, done in this fold** — corrected to 32, E17's end state at Ruling 5. Not 92: the row describes E17 |
| 2 | the claims sweep needs its own file list covering the root-level surfaces and `site/` | **ADOPTED into E20's lane.** Ruling 2 is the argument: the blind spot has now produced a false public claim. `record_markdown()` is **not** to be widened — it feeds artifact and phenomenon extraction. A separate presentation-surface list, gated, with tests riding the commit |
| 3 | add the four relocated docs to `HISTORICAL_DIRS` | **ADOPTED into E20's lane.** `historical` is the correct class for an arc history; unclassified rows report rather than gate, so nothing silently passed meanwhile |
| 4 | A7/A8/B4/B5/C6 re-open | **DONE — Ruling 4** |
| 5 | D3 `pip-audit` over `ci.yml`'s pinned versions | **DECLINED, with the reason.** P13 held: no manifest means no graph. A scanner over an inline install list reports on the CI runner's environment, not on facet's dependency posture. The SKIP's re-open condition (extraction) is the honest trigger. Buying it now buys a green check that measures the wrong object |
| 6 | `site-theme handbook`'s `secondaryCta` patch emits invalid TypeScript | **UPSTREAM**, repaired by hand here; org invariant preserved. File against `@mcptoolshop/site-theme` |
| 7 | handbook playbook names `dist/_pagefind/`; Starlight emits `dist/pagefind/` | **UPSTREAM**, playbook memory correction |
| 8 | `shipcheck.md` records 31 items; live v1.0.7 template has 35 | **UPSTREAM**, memory correction. The +1/+1 template-example miscount in §3 stays unedited — editing the examples to flatter the count is the move this repo forbids, and the report was right to leave it |
| 9 | *(new)* MCP tool JSON schemas carry no per-parameter `description` | E20's lane, with C6's note |
| 10 | *(new)* extend `record_build`'s unexpected-exception wrapper to the other five tools | E20's lane. Tests ride it: one injected failure per tool, both directions |
| 11 | *(new)* `handbook/reference.md`'s tool table predates `record_mcp.py` and does not list it | E20's lane or the next treatment fold |

## Ruling 6 — PREDICTIONS AND STANDARDS, ACCEPTED AS SCORED

13 held / 1 split / 1 missed, committed at `7aab88a` before `shipcheck init` ran, with
blindness disclosed per row. **P4 (23 SKIPs against a predicted 12–16) and P11 (the
description was already set) are the two informative rows**, and both landed where
their own "what this would teach" clauses said they would. P11's falsifier clause was
honoured exactly: the pre-existing value is recorded verbatim in §8a before anything
changes, which is what makes the compensator real.

Standards block accepted as scored. The EXTERNAL_VERIFIER 2 is honest — Gate G, the
one true front-door verifier, is **unavailable** (needs `site-theme` ≥ 2.0.0; published
is 1.7.0) and is recorded as unavailable rather than as a pass. That is the correct
handling of a check that cannot run.

## Ruling 7 — THE RELEASE ORDER, WITH THE REPAIR INSERTED

Nothing below fires without the Director's word. The order is law, not preference —
the tag is immutable.

```
0.  THE REPAIR   (this seat, before his word: Ruling 2 + the badge)
    -- counts corrected at all ten sites, site rebuilt, suite + sweep green
0b. E20 CLOSES AND IS RULED    -- see the amendment; the tag must not freeze a
                                  count an open arc is still moving
0c. RE-COUNT                   -- one --collect-only; every surface must match
0d. NPM NAME RESERVED          -- @mcptoolshop/facet at 0.0.0, from a sibling dir
                                  OUTSIDE this repo (see the second amendment)
1.  gh repo edit               -- description + homepage + 9 topics (compensator 8a)
2.  THE TRANSLATIONS           -- advisor's own hands, translate-all.mjs
                                  git add README.md README.*.md  -> ONE commit
3.  git tag -a v0.1.0 + push + gh release create
4.  Pages                      -- ALREADY LIVE (Ruling 3); redeploys on the push
```

**A pre-tag gate, standing from here:** the test count is **re-counted at the tagging
commit** and must match every surface before the tag fires. Ruling 2's whole cause was
a count that was true when written and false when read; a tag freezes it forever. One
`--collect-only` is the cost.

**AMENDED 2026-08-08, before this ruling was committed — the gate justified itself
inside the session that wrote it.** Ruling 2 corrected ten sites from 32/24 to 92/84,
measured at this session's open. Running the suite as the fold's own gate returned
**202 passed**, and `git log` showed HEAD had moved to `ef29d2d` — E20 committing its
unit tier to `main` underneath this seat. Re-measured: **202 total · 194 hermetic · 8
artifacts.** All ten sites now carry 202/194.

So the lineage is **27 → 32 → 92 → 202 in a single day**, and the number went stale
*twice*: once between E19's commit and this ruling, and once **between this ruling's
correction and its own commit**. That is not carelessness at either seat. It is what a
count does when it is written onto a marketing surface while a lane is actively adding
tests — **a moving denominator, the fifth instance in this repo**, and the first found
in a document being written to fix the previous four.

**Two consequences, both binding:**

1. **The tag does not fire while E20 is live.** Sequence: E20 closes and is ruled →
   re-count → *then* steps 1–3 above. Cutting v1.0.0 mid-arc freezes a number E20 will
   move again within hours, into a release that cannot be edited.
2. **The count on every surface is provisional until that re-count**, and each site now
   says so. A figure that three arcs can move is not a fact a front door should assert
   without its commit.

The honest read of Ruling 2 is therefore sharper than it was first written: the defect
was never "someone wrote a wrong number." It is that **the presentation surfaces carry
live-moving quantities with no gate**, which is exactly want 2 — and want 2 has now
earned priority over everything else in E20's lane.

### AMENDED AGAIN 2026-08-08 — the Director set the version, and added a step

**The tag is `v0.1.0`, not `v1.0.0`** (his word: *"Make sure it's released at v0.1"*;
`v0.1` maps to `v0.1.0` because semver takes three parts and npm rejects two). This
**overrides the studio's standing shipcheck rule** — *"repos at v0.x MUST be promoted
to v1.0.0 — never patch-bump a pre-1.0 version"* — and the override is recorded here
rather than left to be discovered as a rule violation. His live word outranks the
standing rule by the stated authority order.

It is also the more honest number, and the CHANGELOG now says why in its own words:
the extraction gate is open, three seams are dispatched and untaken, and P5 has never
been looked at. **1.0.0 would assert a stability this route has not earned.** Four
accepted assets earn a *first* release, not a stable one.

**Step 0d is new, and its placement outside the repo is the load-bearing part.** The
name `@mcptoolshop/facet` is reserved by a `0.0.0` placeholder published from
`E:/AI/facet-placeholder/` — a sibling directory, **never inside this repo**. The
playbook's primary path is TP-first, and it was **not** taken here for two measured
reasons: it requires `release.yml` (a *third* workflow against the studio's max-2 cap
that E19 landed exactly at `ci.yml` + `pages.yml`), and it requires a root
`package.json` — which would flip shipcheck's Gate H off *"no publishable packages
found"* and **re-open the npm-class SKIPs D5/D6/D7**, the precise thing P14 held
because facet's root stayed manifest-free. A name reservation should not re-open a
packaging gate. The fallback path costs one user-run publish and changes nothing in
the repo.

**The draft release notes in §8c say "32 tests" and must not ship that.** Corrected to
92 at step 3; the four-accepted-assets claim in those notes holds.

---

## What this ruling did not do

No push, no tag, no release, no `gh repo edit`, no translations, no metadata change,
no memory-store write. No edit to `tools/`, `tests/`, `ci.yml`, `.mcp.json`, `canon/`,
`profiles/`, the citable trees, the seeded set, or the closed rulings. The DB is left
to the session-boundary pair cadence.

## The advisor's own record, this seat

The kickoff I inherited asserted *"Pages ALREADY DEPLOYS GREEN"* while the report it
pointed me at staged Pages as unfired. Both could not be true. Checking cost one
request and resolved it (Ruling 3) — **an inherited claim is a hypothesis wearing a
fact's clothes**, and this one was written by the previous advisor.

I also corrected that kickoff's stated sequence. It reads *sheet-walk → his word →
gh-edit → translations → tag*. There is a repair between the walk and his word, and it
is there **because** the walk found it. The sequence was right about order and wrong
about completeness.

One instrument error of my own, caught and named: checking a blank landing-page frame,
I first asked *"which elements in view are hidden?"* and got zero — a number equally
consistent with "all visible" and "nothing is there at all." That is this repo's
**a check that cannot fail is not a check**, committed by the advisor inside the very
session that quotes the law. The second question — *what is in view* — returned 60
elements including the assets table, and the black frame was a capture artifact in the
browser pane, not a defect on the page. The cost was two requests; the lesson is that
the law applies to diagnostics, not only to gates.
