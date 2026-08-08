# Placement memo — where each of the four MCP tools lives

**Written by the advisor (spec-author seat), 2026-08-08.
REWRITTEN IN PLACE the same day**, after the Director's live question reopened it.
See §1 — the first version's framing error is recorded rather than replaced.

**This memo decides; it does not build.** Every claim that could be checked was checked
this session, and §7 states the evidence bound on the one claim that carries the most
weight. Every recommendation is the Director's to overrule in a sentence.

---

## The recommendation, per tool

Three candidate homes are enumerated for each: **in facet** · **a standalone package** ·
**the adjacent product**, where one exists.

| tool | in facet | standalone | adjacent | **ruling** |
|---|---|---|---|---|
| record index | ✅ | later, gated | `repo-knowledge` ❌ | **IN FACET** |
| mesh/texture measurement | ✅ | later, gated | a 3D repo ❌ | **IN FACET** |
| fixture-lint | viable | ❌ | `style-dataset-lab` — **argument stands at full strength** | **DIRECTOR'S WORD** — both presented, §3.3 |
| comfy-preflight | ❌ | ✅ | the Comfy plugin — third-party, unreachable | **STANDALONE** |

**⚖ THE DIRECTOR'S WORD (2026-08-08, arriving on this table, verbatim):**

> record index	IN FACET
> measurement	IN FACET
> fixture-sdlab and facet both at full strength
> comfy-preflight	STANDALONE, re-examined and unchanged

**The three ruled rows are RATIFIED as written.** The fixture-lint line restates the
memo's own open form — the pick between sdlab and facet **remains at his word**, and
§3.3 stands as its decision surface. The bar's scope (§5) and the build order were not
addressed in this word and remain open beside it.

---

## 1. The correction — what the first version of this memo got wrong (2026-08-08)

**The first version asked "which new home?" when the first question is "does it need to
leave?"** It framed a binary — a standalone package versus a capability inside
`repo-knowledge` — and never enumerated the home the tools are already in. The Director
asked *"why not put the mcp tools in the facet repo?"* and the binary collapsed: for two
of four tools, the incumbent home is the better answer.

**This is the advisor failure mode already on the record, in a new dress**: *a check whose
shape assumes its answer*. The repo's own law states it in the form that applies exactly
here — **before building a path to a resource, enumerate the resource.** A whole delivery
path was once built for a model already present. This memo built a placement argument for
tools already placed.

Three things the first version got wrong, each recorded because a future session will read
this file and should know which parts to distrust:

1. **The binary itself.** In-facet was never listed as an option.
2. **The distribution argument was mostly wrong.** The first version implied the tools
   must live where their callers live. **An MCP server does not need to be in its caller's
   repo** — a session working in `sprite-foundry` mounts a server that lives in facet. The
   argument survives only for `comfy-preflight`, where a gate must run *in-process* inside
   the submitting tool (§3.4), and it is genuinely decisive there.
3. **A pointer-integrity claim that does not hold, asserted at this seat to the Director
   verbally before it was checked.** I said moving `tools/facet_index.py` would break
   citations the pointer gate proves resolve. **It would not.** `.py` is not in the
   artifact extractor's extension set, so the tool never becomes an artifact row, and a
   ruling's row points at the ruling document, not at the tool. **Leg 3 would not fire.**
   The real cost is smaller and still real: **35 prose citations across ten documents name
   the tool by path**, and a move makes every one of them a pointer a human cannot follow.
   That is a documentation-integrity cost, not a gate failure, and it is stated at its
   true size here.

**What did NOT change:** the case against `repo-knowledge`. That argument was sound and it
is preserved as §4, where it belongs — one leg of the enumeration rather than half of a
false binary.

## 2. The three homes — what each buys and what each costs

| | in facet | standalone package | adjacent product |
|---|---|---|---|
| migration cost | **zero** — the code is already here | a repo, CI, packaging, a full treatment | a port into another codebase's conventions |
| instrument identity | **preserved by construction** — no file moves | a version boundary by definition | a version boundary by definition |
| reachability | mountable by any session; **not** importable in-process by another repo's code | importable and mountable anywhere | in-process inside its host only |
| release cadence | facet's, which is *no* release cadence — it publishes nothing | its own, and it owes semver | the host's |
| shipcheck surface | facet grows tests + CI (§5) | four repos × the full package bar | the host's existing bar |
| the record's citations | **stay resolvable to a human** | 35 prose pointers go stale per moved tool | same |
| adoption by other repos | only via mounting the server | the real answer if adopters exist | only the host's users |

**The asymmetry that decides two of the four tools:** in-facet placement is *reversible* —
extraction later costs a repo and a set of stale prose pointers. Extraction now is
*irreversible in the property that matters*: the instant a measurement tool is ported, its
numbers are a new instrument's numbers by spec 2's own identity law, and every comparison
against a closed ruling needs re-anchoring. **Prefer the reversible order.**

## 3. The rulings

### 3.1 The record index → IN FACET

**The only adopter of the record conventions is this repo.** Measured (§7): across 146
local directories under `E:/AI` and the whole memory store, **11 markdown files carry the
numbered-ruling convention and every one of them is inside facet.** Zero elsewhere.

That single fact reverses the first version's recommendation. Spec 1's §6 — the adoption
contract, conventions declared in config so any repo can adopt them — was written for a
user base of one, and **speculative infrastructure for a user base of one is the
built-vs-filled anti-pattern the studio constitution names by name.**

Three supporting grounds:

- **The CLI already lives here and has been accepted at two seats' hands** (E15 Ruling 1).
  A move buys nothing the mount does not already buy.
- **The polish arc dogfoods it here.** Ruling 35 names the first consumer, and that
  consumer is facet's own sessions across four exemplars. Tool and consumer share a
  working copy.
- **The four-leg verify already runs as facet's standing ritual** (Ruling 4). The gate is
  not something the product has to bring; it is something the repo already does.

**Extraction is not foreclosed — it is gated.** The trigger is explicit and cheap to
detect: *a second repo adopts the conventions.* Spec 1's §6 stays in the spec as the
adoption contract it will be, unbuilt until then, so the extraction is a packaging job
rather than a redesign. **No npm name is needed until that day**, which narrows spec 1's
open question rather than answering it.

### 3.2 The mesh/texture measurement MCP → IN FACET

**The instruments' numbers sit in closed rulings, and a port is a new instrument by this
spec's own identity law.** Spec 2 states the contract: *two assets measured by different
versions of this server are not comparable*, and every payload carries a version and a
config hash so a mismatched comparison refuses. A repo migration plus the refactor it
invites is exactly that mismatch, applied retroactively to four subject classes of banked
numbers.

The record already refuses this move at a smaller scale. `e12_offsurface.py` exists as a
separate file **specifically so a shipped instrument whose numbers are cited in a closed
ruling would not be edited** — its own docstring says so. Extracting the whole family to
another repo is that hazard several orders larger.

**And an in-repo MCP server imports the tools without moving a file.** The server is a new
surface over `tools/verify/` and `tools/diagnostics/` as they stand — no port, no version
boundary, and the Python/`trimesh`/`scipy` grounds from spec 2 now argue *for* staying
rather than for a standalone Python package. The extraction boundary that spec 2 leans on
([profiles-design.md](../profiles-design.md)) is a *code-versus-profile* boundary and is
satisfied inside one repo; it was never a repo boundary.

Same gated trigger: extract when a consumer outside facet needs it **in-process** rather
than over a mount.

### 3.3 fixture-lint → the Director's word, both options at full strength

**This is the one I am not ruling**, because two sound arguments point in opposite
directions and the tie-breaker is a studio-ownership judgment the Director holds.

**The sdlab case (unchanged, and it is strong):** checks 6, 7 and 9 — colour words name
materials, family-word sprawl, register declared per subject — are **checks against a
declared vocabulary inside sdlab, and English heuristics outside it.** sdlab owns the
per-project terminology, rubric and constitution, and the studio constitution *settles*
canon ownership there: `visual-design-bible` was excluded from the map precisely because
sdlab subsumes it. A linter for canon artifacts belongs to whatever owns canon.

**The facet case:** the test corpus is facet's — five fixtures whose catches are already
ruled — and the first two live jobs are facet's polish-arc fixtures (the humanoid's
register change, the sword's activated state). Building it here means the corpus and the
consumer are both in hand on day one; building it in sdlab means reaching into another
repo for every regression case.

**A third shape exists and may be the honest answer:** the *grammar* checks (4, 5) and the
*structure* checks (1, 2, 3) need no vocabulary and could live wherever the tool lives;
only 6, 7 and 9 need sdlab's registry. That is a real seam — and it is also how a tool
ends up half in each repo, which is worse than either. **I flag it; I do not recommend
it.**

My weak lean, stated as weak: **sdlab**, because check 3 — the one that pays for the tool
— is subject-independent and would work anywhere, while the checks that need a registry
cannot be recovered later without the move happening anyway.

### 3.4 comfy-preflight → STANDALONE, unchanged

The one tool whose distribution argument survives §1.2 intact, and it survives because of
E08 Amendment 32: **the check lives inside the tool that performs the irreversible step.**
A preflight invoked over a mount, beside the submitting process, is a transport rather than
a guard — 47,020 texels were committed after a fired ANDON because a shell chain walked
past an exit code.

Its callers are outside facet: the studio's bespoke cloud bridge and the Comfy submission
sessions. The official Comfy-Org plugin is third-party and cannot host our checks. **In
facet, this tool cannot gate the things that spend the money.** Standalone, called
in-process on each submit path.

## 4. Why not `repo-knowledge` — the leg that survives the rewrite

Preserved because it was sound; demoted to one leg of the enumeration, where it belongs.

**4a — The write models are opposed, and merging them re-creates the failure the index
exists to prevent.** `repo-knowledge` is a *curated* store: an `rk note` thesis exists
nowhere else and the DB is rightly its authority. This index's founding ruling is the
opposite — *the day it is hand-edited it is wrong by definition*
([context-architecture.md](../context-architecture.md), and the tool's own docstring in
those words). A DB that could disagree with the record would be **a second authority,
forbidden by construction.** The first note written onto a ruling row produces exactly
that, and nothing notices: `rk fsck` tests that the DB is internally sound, not that it is
a faithful map of a document. This is what the whole facet arc is a reaction to.

**4b — The gate is the product, and `repo-knowledge` has nothing of its shape.** All four
legs at this seat this session:

```
[leg 1] determinism   BYTE-IDENTICAL   both builds
[leg 2] counts        every grep == db; sequence gaps: none
[leg 3] pointers      dangling 0
[leg 4] seeded set    19 / 19 within the top 3
VERIFY PASSED - all four legs
```

`rk fsck` and `rk doctor` are good instruments for what they do and are not this. There is
no determinism contract there — nor should there be, since a DB that syncs from a live
GitHub API cannot be a pure function of anything. **The determinism contract and the
`sync` verb cannot share a home honestly.**

**4c — The non-duplication boundary, which holds under in-facet placement too.**
`repo-knowledge` **never ingests ruling rows** — duplicating them makes two answers to one
question. The seam is a *pointer*: one hand-written `rk note` on facet's entry saying the
repo carries a governed record and how to query it. No sync path, nothing to drift.
*(Unverified: whether `rk`'s note-type enum takes `convention` for this without a schema
change. If not, `general` serves and costs nothing.)*

Verified this session: `@mcptoolshop/repo-knowledge` is **2.1.1** on npm and on disk, with
30 MCP tools. **The banked candidate memory says v1.0.5 and that is stale** — corrected
here because the next session reads that memory too. Nothing in either version of this
memo turned on it.

## 5. The bar consequence — name it now, not live in the build session

Ruling 35 sets the bar: *"BUILT and VERIFIED PROPERLY WITH TESTS — the studio's shipcheck
bar, not a prototype bar."* In-facet placement changes **what that bar means**, and the
build session must not discover it at the time.

**Verified this session: facet has no tests, no CI, no packaging** — no workflows
directory, no test directory, and neither a Node nor a Python package manifest. It is a
public repo in `mcp-tool-shop-org` holding a record, a tool surface, and canon.
*(Named in prose rather than by filename on purpose: citing a manifest filename mints an
artifact row for a file that pointedly does not exist. I predicted that from
`ARTIFACT_KIND` before rebuilding, watched it land, and removed it — the phantom class
named in the index spec's §6, re-committed by me two sections after naming it.)*

So in-facet placement means **facet grows a test suite and a CI workflow for its tool
surface.** That is a real addition to a repo that has neither, and it is the honest cost
of this recommendation. It is also **far cheaper than four full treatments**, and the
difference is worth stating precisely:

| shipcheck item | in facet | as a published package |
|---|---|---|
| tests + verify script + CI green | **required — the new work** | required |
| structured errors, `--help`, threat model, SECURITY.md | required | required |
| v1.0.0 minimum, semver, npm publish | **not applicable — publishes nothing** | required |
| logo, 8 translations, landing page, Starlight handbook | **not applicable** | required |
| CHANGELOG, LICENSE | LICENSE present; CHANGELOG new | required |

**The package-level items attach to a published package.** In-facet tools publish nothing
until extracted, so those rows are not skipped — they are *not yet applicable*, and they
become applicable on the day extraction happens. One CI workflow and one test suite
covering the tool surface satisfies clause 2 of the charter for the two in-facet tools.

**This is the Director's to scope in a sentence** — in particular whether the CI runs on
`push` with paths gated to `tools/**` (the studio's Actions rules cap workflow count and
require paths filters), and whether the test suite covers only the new MCP surface or the
existing instruments too. My recommendation: **paths-gated CI on `tools/**` plus the new
surface's tests only**, because retrofitting tests onto instruments whose numbers are
already banked is a much larger job and is not what clause 2 asks for.

## 6. What changes if the Director overrules — recomputed against this frame

**If the index MCP goes standalone anyway:** spec 1's §6 adoption contract becomes
load-bearing on day one rather than gated, the package name matters (spec 1 §12), and the
35 prose pointers to `tools/facet_index.py` need updating in the same fold that moves it.
The four-leg verify travels intact — it is already external-verifier-shaped. **Nothing in
the spec is invalidated; one section changes from "gated" to "now."**

**If the measurement MCP goes standalone anyway:** the identity law forces an explicit
re-anchoring step — measure the four banked subjects with the extracted server and record
the deltas against the in-repo numbers *before* any new comparison is trusted. That is a
real task with a real cost and it belongs in the extraction spec, not discovered later.

**If either goes into `repo-knowledge`:** §4a is the objection, and the concrete
consequence is that spec 1's read-only-by-construction section stops being a property of
the architecture and becomes **an enforced partition that code has to keep** — derived
tables rejecting every write path, with tests proving it.

**If fixture-lint goes to facet rather than sdlab:** checks 6, 7 and 9 degrade to English
heuristics until a vocabulary source is wired, and the spec should say so at the point the
checks are defined rather than in a footnote.

**If comfy-preflight goes into facet:** it cannot gate the submissions that spend money
(§3.4). This is the one recommendation where I would ask for the reasoning before
proceeding, because the tool's whole value is the in-process placement.

## 7. Evidence state on the one-adopter claim

It carries the most weight in this memo, so it carries its bound explicitly.

**Checked:** every `*.md` file under `E:/AI` — 146 top-level directories, including local
clones of the org's repos — plus the entire canonical memory store, for
`^## Ruling <n>` and `^## Session handoff <n>`. **Result: 11 files, all inside facet.**
The search tool was validated against a known control first (a string present only in
`repo-knowledge`) to prove the path argument was not silently scoping to the working
directory.

**Not checked:** org repos with no local clone. The org holds **87 repos**; I did not
enumerate which are absent from this rig, and I did not clone any to check.

**An earlier attempt at this scan timed out mid-alphabet and its partial output is not
what is reported above** — the numbers here come from the completed run. Recorded because
a partial sweep read as a complete one is how a claim becomes doctrine.

---

## Standards compliance (this memo)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every factual claim names where it was read this session: `npm view`, `gh repo view`/`repo list`, the filesystem checks for CI/tests/packaging, the validated convention scan, the artifact-extension table read from source, and the verify output quoted in §4b |
| ANDON_AUTHORITY | 3 | the memo halted its own first recommendation on the Director's question rather than defending it; §7 refuses to report a timed-out scan as a result; §1.3 retracts a claim this seat had already asserted verbally, at its true size |
| NAMED_COMPENSATORS | 3 | §6 is the compensator table for the decision itself, recomputed per tool, and it names the re-anchoring task that a measurement extraction would owe — the one irreversible-in-practice consequence in the set |
| DECOMPOSE_BY_SECRETS | 3 | the enumeration is by what changes together — migration cost, instrument identity, reachability, release cadence, shipcheck surface — and the ruling differs per tool *because* those axes differ per tool, which is the decomposition doing work rather than decorating |
| UNCERTAINTY_GATED_HUMANS | 3 | one recommendation is deliberately withheld (§3.3) with both cases at full strength and my lean labelled weak; §5 hands the Director a scoping decision framed contrastively; §6 states the cost of overruling before he rules |
| EXTERNAL_VERIFIER | 3 | the search instrument was validated against a control before its result was used; §4b's output is the tool's own verifier rather than my summary; **and the decisive correction in §1 came from the Director, not from this seat** — which is the external verifier working exactly as the separation intends |
