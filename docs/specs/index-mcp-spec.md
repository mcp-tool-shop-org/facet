# Spec 1 — the record-index MCP

**Status:** specification, authored by the advisor (spec-author seat) 2026-08-08 at
Gate 1's close on the fourth asset. **Nothing here is built.** Placement is decided in
[placement-memo.md](placement-memo.md) and is the Director's to overrule in a sentence.

**Placement: IN FACET** — ruled in the memo's rewrite, 2026-08-08, after the Director's
question reopened it. **This reverses the first draft of this spec**, which assumed a
standalone package; the reversal is noted here rather than silently applied. The grounds:
facet is the only repo carrying the record conventions (measured — 11 files, all here,
across 146 local directories and the memory store), the CLI already lives here at two
seats' hands, and Ruling 35's named consumer is this repo's own polish arc.

**Tool names:** `record_*`, so the surface reads the same whether or not it is ever
extracted. **No package name is needed yet** — an in-repo server publishes nothing.
Extraction is gated on a second adopter appearing, and §6's adoption contract is written
so that extraction is then a packaging job rather than a redesign.

**What this productizes:** [`tools/facet_index.py`](../../tools/facet_index.py), built
under E15, accepted at two seats (E15 Ruling 1), and run at this seat while writing this
spec: `build` produced 3,399 FTS rows over 476 rulings, 70 laws, 29 handoffs, 219
decisions, 654 artifacts, 27 phenomena and 1,908 prose sections; `verify` returned
**PASSED — all four legs, 19/19 seeded**.

---

## 1. The job

**A session queries the record instead of reading it, and then reads the forty lines the
query pointed at rather than the six hundred it would have skimmed.**

That is the whole product, and it is worth stating why it is not "search your docs".
The corpus is a *governed decision record*: numbered rulings that supersede each other,
laws that were paid for by a named failure, handoffs with outcomes, a value registry
whose entries are DECIDED or UNDECIDED. Retrieval over that corpus has a property
ordinary document search does not need — **the answer is a citation, and a wrong
citation is worse than no answer**, because a session will build on it. Everything below
follows from that.

The differentiator is not the index. It is that **a failing index refuses to answer.**

## 2. What it is NOT

- **Not a writer.** It never edits the corpus. Not to fix a malformed heading, not to
  normalise a date, not ever. Malformed-by-convention text is a *report item*.
- **Not an authority.** The markdown is canonical; the DB is a map. A tool that could
  disagree with the record would be the second authority the design exists to prevent.
- **Not a judge.** It reports what the record says. It does not summarise a ruling into
  a conclusion, rank rulings by importance, or answer "what should we do".
- **Not a portfolio tool.** One repo, one record. Cross-repo questions belong to
  `repo-knowledge`, which must never ingest these rows (memo §4).
- **Not semantic search.** Deterministic FTS was chosen over embeddings *because* the
  record's value is precision citation (`context-architecture.md`). Vector search is out
  of scope; revisit only if FTS is measured to miss in practice.
- **Not a gate on the repo's own work.** `record_claims` is report-only by ruling
  (E15 handoff 2 / Ruling 9b). It never returns a failing exit code.

## 3. The tool surface

Job-shaped, following the studio's reference form (`ollama-intern-mcp` v2.9.1): a tool
is a job someone wants done, not a wrapper on a function. Six tools.

| tool | job | reads | writes | annotation |
|---|---|---|---|---|
| `record_query` | *what did we decide about X, and where is it written* | DB | — | `readOnlyHint` |
| `record_get` | *give me the full text at this anchor* | DB + corpus | — | `readOnlyHint` |
| `record_build` | *make the index current with the working tree* | corpus | the DB + its certificate | `destructiveHint: false` |
| `record_verify` | *is this index trustworthy* | corpus + DB | the certificate | `destructiveHint: false` |
| `record_health` | *what state is the index in right now* | certificate | — | `readOnlyHint` |
| `record_claims` | *which current-state documents disagree with the record* | DB + corpus | — | `readOnlyHint` |

### 3.1 `record_query`

Input: `query` (string, 1–500 chars), `limit` (1–50, default 8), `table` (optional
restriction to one ontology table), `arc` (optional).

Returns ranked rows, each carrying `file`, `line`, `anchor`, `table`, `holding`, and the
rank. **The pointer is the product**; the one-line holding is an aid to choosing among
pointers, never a substitute for reading the row.

The ranking mechanism ports unchanged, and its selection is already ruled (E15 Ruling 3):
a **stage-1 exact adjacent phrase** over the full word run with stopwords kept, then
**stage 2, content words OR'd with bm25 scaled by term coverage**. Both stages ship.
Three variants were scored on the fixed seeded key and two were falsified — coverage as
primary sort key scored 9/14, title-coverage-first 11/14, scaling 13/14, and stage 1
carried it to 14/14. **Do not re-litigate this without re-running the key.**

Two properties are *recorded boundaries*, surfaced in the response rather than engineered
around (E15 Ruling 7): content phrasings return their target at rank 1; **conversational
phrasings surface the evidence documents above the ruling**. The index serves the
record's own vocabulary best, which is the correct bias for a legal record. A client
seeing a report above a ruling is seeing the documented behaviour, and the response says
so in a `notes` field rather than leaving the caller to infer a defect.

### 3.2 `record_get`

Takes a `file` + `anchor` (or `locator`) from a query result and returns the text of that
row's own block, bounded. This exists so the query → read loop never requires the client
to open a 2,000-line document to see forty lines. It reads the **corpus**, not the DB's
copy — the markdown is canonical, so the full text comes from the markdown.

### 3.3 `record_build`

Regenerates the DB from scratch. Never incremental: the DB is a pure function of the
corpus at a commit, and an incremental update is a state machine that can drift.

**`build` runs the verify legs and writes the health certificate before returning.** The
E15 ritual is `build` + `verify` as one act (Ruling 4.1) and separating them in the
product would re-open the gap the ritual closes. A build whose verify fails still writes
the DB — you cannot diagnose a failure you refused to produce — but the certificate
records FAILED, and §5's refusal behaviour follows from the certificate.

### 3.4 `record_verify` — the four legs

The contract, in the order they run:

| leg | what it tests | failure means |
|---|---|---|
| **1 · determinism** | two builds from an unchanged corpus are byte-identical | the build depends on something that is not the record — a set iteration, a timestamp, a filesystem order |
| **2 · counts** | the verifier's **own** greps against the DB's counts, plus sequence-gap and completeness checks | the parser is silently dropping or inventing rows |
| **3 · pointers** | every row's `file` exists and its `locator` is findable in it | a citation the index hands out will not resolve |
| **4 · seeded set** | each seeded question's known target ranks within the top 3 | retrieval regressed — measured growth-sensitive, so this re-runs every time |

Four requirements the implementation inherits, each paid for:

- **Leg 2's greps are written independently of the parser's constants.** In the source
  they are literal patterns in the verifier's own table, not shared regexes. *The parser
  and the verifier must not be one implementation checking itself.* This is the
  EXTERNAL_VERIFIER standard expressed in code, and a refactor that "removes the
  duplication" destroys the leg.
- **Determinism has a pre-registered fallback.** If byte-identity fails, compare
  `.dump` output; SQLite's file header carries a change counter that is an
  implementation detail. The certificate records **which leg held**, because a run that
  fell back to `.dump` is a different (weaker) claim than byte-identity, and the
  difference must be visible without reading the transcript.
- **A `.dump` fallback is not a silent pass.** It is reported as the fallback it is.
- **Pre-registered bounds stay as dispatched.** Sequence checks run to a *dispatched*
  bound; anything the record carries above it prints on a separate completeness line
  rather than widening the condition (E15 Ruling 3c). Widening a bound after seeing what
  is above it is retuning, however principled the reasoning.

**One instruction inherited verbatim from the source, because it is a law about
verifiers:** the completeness line **states only what it measured**. An earlier version
added "← record carries more than the prose claims", which was true when written and
false eight hours later. *A verifier that editorialises about a document it does not
read will eventually lie to every session that runs it.*

### 3.5 `record_health` and `record_claims`

`record_health` returns the certificate: which legs passed, when, against which corpus
revision, which determinism leg held, and the staleness state from §5. Cheap — it reads
one small file.

`record_claims` is the stale-claim sweep: current-state documents (README, the discipline
file, handbook pages) that assert counts the record no longer carries. **It is
report-only by ruling and exits 0 whatever it finds** (E15 handoff 2). Its verdict swings
on phrasing and on document class, and neither may decide an exit code — *a diagnostic
and a gate are different objects.* It reads the index's measurements rather than
re-deriving them, because a second derivation would be a second authority.

Three of its semantics are load-bearing and port unchanged: **a range asserts a MAX and a
cardinal asserts a COUNT** (conflating them manufactures a stale row out of a correct
document); **a range is a count-claim only if it starts at 1** (`Rulings 21–23` names
three of them and asserts nothing about the total); and a modifier that makes an
assertion unresolvable is reported **AMBIGUOUS**, never resolved to a number, because
picking a reading invents a claim to check.

## 4. Read-only by construction

Not a policy. A property of the architecture, and it must survive into the product:

1. **The corpus is opened read-only.** Every read path. There is no write path to a
   markdown file anywhere in the package, and that is a testable claim — an adoption
   test that greps the built artifact for corpus write calls is cheap and belongs in CI.
2. **The server writes exactly two paths**: the DB artifact and its certificate sidecar,
   both under the configured index directory. `record_build` and `record_verify` are the
   only tools that write. Every other tool is `readOnlyHint`.
3. **The seeded set is repo-owned config, never server state.** It lives in the adopting
   repo, in the repo's own file, versioned with the record. A server that carried the
   seeded questions would be grading itself against a key it owns — the seeded set is
   the external verifier, and an external verifier the tool ships is not external.
4. **The certificate is a sidecar, never a DB row.** This follows from leg 1 and is
   worth spelling out because it is the kind of thing an implementer gets wrong once:
   writing the health result into the DB makes the DB no longer a pure function of the
   corpus, and **the determinism leg would fail on its own output**. Certificate goes
   beside the DB, not in it.

## 5. The health surface — how a failing index behaves

This is the differentiator, and it needs three states rather than two.

| certificate state | `record_query` behaviour |
|---|---|
| **PASSED**, corpus unchanged since the build | serves normally |
| **PASSED**, corpus has moved since the build | **serves, with a staleness banner on every response** naming what moved |
| **FAILED**, or **no certificate at all** | **refuses, loudly**, with a structured error naming the failing leg and the one command that fixes it |

**Why staleness warns rather than refuses.** The DB commits at *session* boundaries, not
every fold (E15 Ruling 4.2) — so bounded staleness is the ruled, normal state of a fresh
clone, and a refusal there would fire on correct work. *Put the andon on the direction
the invariant does not bound*: leg 1 bounds "the DB disagrees with itself"; nothing
bounds "the DB is a faithful map of an older record". That direction is watched, and it
is watched by **reporting**, because a diagnostic and a gate are different objects.

**Why no-certificate refuses.** *A gate trusted from the fold before is not a gate* — and
here there is no gate result at all, only a DB someone produced. Refusing is right, and
it is one command to fix.

**Why the failure is loud rather than a flag on the payload.** A caller that must read a
field to discover the answer is untrustworthy will not read it. The refusal is a
structured error in the studio's shape — `code` / `message` / `hint` / `retryable`,
matching `ollama-intern-mcp`'s `ErrorShape`, no raw stacks:

```jsonc
{
  "error": true,
  "code": "INDEX_VERIFY_FAILED",
  "message": "leg 3 (pointers): 4 dangling locators in `rulings`.",
  "hint": "Run record_build. If it still fails, the corpus moved a heading a row points at — the rows are listed in the certificate.",
  "retryable": false
}
```

Named codes, minimum set: `INDEX_VERIFY_FAILED`, `INDEX_NEVER_VERIFIED`,
`INDEX_MISSING`, `CORPUS_NOT_FOUND`, `CONVENTIONS_INVALID`, `SEEDED_SET_INVALID`,
`ANCHOR_NOT_FOUND`, `INTERNAL`.

*⚠ AMENDED 2026-08-08 by the build's ruling ([E18-ruling.md](../experiments/E18-ruling.md)
Ruling 2) — five contract deltas, each argued in the report's §9 and ruled rather
than folded in silently: (i) `BAD_ARGUMENT` joins the codes — a caller-failure
code beside these index-failure codes, because an empty result for a typo'd
argument is a wrong answer wearing success; (ii) `record_claims` ALSO gates on
health (it reads the index's measurements); build/verify/health never gate;
(iii) a DB whose sha does not match its certificate's REFUSES
(`INDEX_NEVER_VERIFIED`) — a certificate describing a different artifact is no
certificate for the one present, and this check makes the DB+certificate
pair-commit cadence verifiable; (iv) the certificate carries a `0_discovery`
bucket beside the four legs — the inverse guards produce their own failures;
(v) §4.2's "exactly two paths" means two persistent artifacts — verify's leg 1
writes per-process temps beside the target and removes them (E16 Ruling 3).*

**There is no skip flag, and adding one is out of scope permanently.** E08 Amendment 32
is the grounds: a check that a scripting accident can separate from the action it gates
is not a gate — 47,020 texels were committed after a fired ANDON because a shell chain
walked past an exit code. *The check lives inside the tool that performs the step.*
Here the step is answering a question, so the check lives in the query path.

## 6. The adoption contract — what a repo must look like

This is the part that makes it a product rather than facet's script. Each convention
below is stated with the ruling that paid for it. **All of it is configurable; none of
it is guessable.** A repo declares its conventions in a versioned JSON config file that
ships in the repo, and the server refuses to run against a repo that has not declared
them (`CONVENTIONS_INVALID`) rather than guessing a pattern. *(The config's filename is
deliberately not fixed here — naming a file that does not exist mints an artifact row in
this repo's own index, which is the phantom-artifact class the record already names.
Caught by running the sweep on this spec; recorded rather than silently avoided.)*

**Under in-facet placement this section is written but NOT BUILT.** facet's own conventions
are the ones the CLI already parses, and a config layer for adopters who do not exist is
the speculative infrastructure the placement memo rules against. §6 stays in the spec as
the contract extraction would honour — so the day a second adopter appears, the work is
packaging rather than redesign. **What ships now is what the CLI already does; what is
specified here is what it must not contradict.**

### 6.1 Discovery — by glob, with the inverse guard

**Ruling documents are discovered by a sorted glob, never by a hardcoded list.** The
list came first and it was written before `E15-ruling.md` existed, so that document's
rulings were invisible to the index — **and invisible to the gate too**, because the
verifier grepped the same list. *A gate must test the operation's failure mode, not its
success mode*, landing on the instrument built to enforce it (E15 Ruling 8b).

Three requirements, all from Ruling 9a:

- **sorted** glob, so insert order is a pure function of filenames, which are in git —
  the determinism the explicit list was protecting is preserved exactly;
- **the discovered list prints in `verify`'s output**, so the glob's own misses are
  visible rather than assumed — *a discovery rule nobody can audit is the hardcoded
  list's defect wearing a different hat*;
- **the inverse guard**: any row whose file the glob does *not* discover fails the run.
  This is the check the old construction could not express, and it was added by an
  executor unbidden. It ships.

**A file that matches the pattern and yields no numbered content is not an error.** It
enters as prose and keeps its prose indexing — *prose exclusion is decided by what a file
actually yielded, not by whether it matched a name.*

**Arc labels are derived by stripping from the convention word onward, never from a
leading identifier.** Keyed on the E-number alone, `E10-offsurface-ruling.md` merges into
`E10` and twelve rulings collide with seven on numbers 1–7 — a primary-key failure, not a
quiet miscount.

### 6.2 Status is read from a convention's position, never matched in prose

**This is the law, and it is the one an implementer is most likely to break** (E15
Ruling 2). Two defects of one class:

- Case-insensitive verdict matching marked three rulings ACCEPTED that accept nothing.
  **The record SHOUTS its verdicts; lower-case "accepted" is an adjective.**
- Whole-field scanning read three DECIDED registry values as UNDECIDED — including one
  whose `why` narrates *"the arc's one deliberately undecided value"* about a value a
  ruling had already decided.

*An index reporting a decided value as undecided is a second authority contradicting the
record — the one thing the design exists to prevent.* Both fixes conform the parser to
the record's conventions (capitals carry verdicts; the head of the `why` field carries
the class label) rather than special-casing documents. **The parser reads the record as
it is; the record is not rewritten to suit the parser.**

### 6.3 The declared conventions

The config declares, per repo, patterns for: ruling headings, lettered sub-rulings,
closure markers, amendments, addenda, handoff headings, the law corpus and its file, the
value registry and its shape, prose corpora, and current-state vs historical document
classes for `record_claims`.

Two are worth stating in the spec because they are measured rather than assumed:

- **The lettered sub-ruling marker is `**<n><letter><SPACE><dash>`** — measured 151 times
  out of 152 across five documents. The single exception is not a sub-ruling but a
  *closure marker* naming the sub-ruling it closes, carrying the Director's own sentence.
  A dash class tolerating a bare hyphen swallows it and loses one of two holdings. **The
  space is required and the suffixed form gets its own pattern and its own row.**
- **A parent ruling's body must not re-index its children's prose.** Including it made
  one ruling a 3,932-character document competing with its own five children and diluting
  bm25's length normalisation for both. The parent keeps only what belongs to it.

### 6.4 The seeded question set — the adoption contract's hardest clause

The seeded set is what makes the index trustworthy, and it has a *process*, not just a
format. All three rules ship as the contract:

1. **Measured entry.** A candidate seed runs report-only through `record_query` FIRST and
   its target must rank ≤ 3 **before** the row enters the gate. Seeds are ruled in from
   measured ranks, never added and then tuned until green.
2. **Targets are pinned to the row that carries the value, not to a file.** Left
   file-level, one seed passed on a ruling that shared six query words and carried none
   of the digits — *a gate that cannot tell the right row from a coincidence is not
   testing anything.* Pinning makes the condition strictly harder and derives it from the
   record.
3. **Withdrawn, never re-crafted.** When the live corpus legitimately outranks a seed,
   the seed is **removed with its history recorded in place** — not re-phrased until it
   passes. Two withdrawals are in the source with their reasons: one whose digits the
   route deliberately propagates per subject (a structural expiry), and one that measured
   rank 2 and missed at the gate minutes later because a live lane had committed fresh
   content that legitimately outranks a generic phrase. **The gate firing on a
   measurement made minutes earlier is the leg working, not a defect.**

The tooling must make the right thing easy: a `record_verify --propose-seed <phrase>`
path that runs a candidate report-only and prints its rank without touching the set, so
measured entry is one command rather than a discipline someone remembers.

### 6.5 Growth sensitivity is the point

A question that passed at 2,444 FTS rows missed at 2,475. **The seeded gate re-runs on
every build** — it is measured growth-sensitive, and a gate trusted from the fold before
is not a gate. This is why §3.3 fuses build and verify.

## 7. Two named boundaries, shipped as documentation rather than engineered around

**Mention-vs-use.** A text sweep cannot tell a phrase *used* from a phrase *mentioned*.
The sweep once fired on a parenthetical quoting a removed phrase — the note documenting
the hazard reproduced the hazard. This is named as the sweep's next improvement and
deliberately **not built**: the collision surface with quotation-heavy correction
discipline is measured-narrow, and a classifier rule added while looking at the row it
would clear earns its place only when the class fires on text that should stay quoted.
Because `record_claims` is report-only by ruling, adding it later is instrument
development, not retuning — *stated now so the distinction is already decided when it
matters* (E15 Ruling 9b).

**Self-reference.** A document that quotes the record's counts as data — a spec, a
predictions file, this file — will surface for queries about those counts. The source
handles it by excluding the index's own arc from the sweep. The product generalises it:
the config declares which paths are *about* the record rather than *of* it. Named,
bounded, and reported — not silently filtered.

## 8. Output requirements

- **ASCII only on every print path.** Not a style preference — a correctness
  requirement, and it fired at this seat while writing this spec: `verify` crashed with
  `UnicodeEncodeError: 'charmap' codec can't encode character '↑'` on a Windows
  console under cp1252, **after legs 1 and 2 had passed**, killing a run that was
  succeeding. A verifier that cannot print its result on the platform it runs on has not
  verified anything. (The repair to facet's own tool is a queued E16 errand and is not
  this spec's business; the *product* ships ASCII from the first line.)
- **`file:line` goes last on a table row**, so a long path is never truncated — the whole
  point of the row is that a human can open the site it names.
- **Every response carries the certificate state.** Not just refusals.

## 9. Compensators

Every irreversible act, its undo, and its owner. **No skips** — this table is
non-negotiable per the studio's workflow standards.

| action | irreversible? | compensator | post-rollback state | owner |
|---|---|---|---|---|
| `record_build` overwrites the DB | no | re-run `record_build` from the corpus | byte-identical DB (leg 1 guarantees it) | the caller |
| `record_build` deletes the DB before rebuilding | recoverable | the DB is a derived artifact; regenerate | identical | the caller |
| `record_verify` writes the certificate | no | re-run; the certificate is derived | identical | the caller |
| **writes to the corpus** | — | **impossible by construction (§4)** — there is no such path | — | — |
| npm publish (a later session) | **yes** | `npm deprecate` the version; publish a fixed patch. Un-publishing is not available past the window | the bad version stays visible, marked | the publishing session |
| `gh release create` (a later session) | **yes** | `gh release delete <tag>` + `git push --delete origin <tag>` | tag and release gone; the commit remains | the publishing session |
| creating the GitHub repo (a later session) | **yes** | `gh repo delete` within the same session, or archive | repo gone or archived | the Director |

The three genuinely irreversible acts all belong to a **later** session. This session
performs none of them.

## 10. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the DB is a pure function of the corpus at a commit; `build` takes no tuning parameters; the ranking mechanism is fixed and its two rejected variants are recorded with their scores so nobody re-tunes it silently; the conventions that govern parsing are versioned in the same repo as the record they parse — which under in-facet placement is true by construction rather than by config |
| ANDON_AUTHORITY | 3 | §5 is an andon on the product's own trustworthiness, with no skip flag by construction (E08 A32); §3.4's inverse guard fails the run on a row from an undiscovered file; a parse the tool cannot do is reported, never papered over |
| NAMED_COMPENSATORS | 3 | §9 is complete, includes the publish-path actions that do not exist yet, and names the two corpus-write compensators as *impossible by construction* rather than as undo procedures |
| DECOMPOSE_BY_SECRETS | 3 | parser knows conventions · schema knows ontology · verifier knows neither's internals and re-derives with its own greps (§3.4, first bullet) · the seeded set is corpus-owned, never server state (§4.3). Four separations, each along an axis that changes independently. In-facet placement does not weaken this: the separations are between *modules*, and were never between repos |
| UNCERTAINTY_GATED_HUMANS | 2 | parse limitations print as findings; §7's two boundaries are surfaced rather than engineered around; the staleness banner tells a caller what it is looking at. Scored 2 rather than 3 because the product has no checkpoint that *pauses* for a human — it reports and continues, which is right for a read tool but is not the standard's strongest form. **Remediation: none proposed** — a query tool that blocks on a human is the wrong shape; the human checkpoint is the Director's ruling on the record, one layer up, and that is where it belongs |
| EXTERNAL_VERIFIER | 3 | the seeded set is authored independently of the builder and lives in the corpus, not the server; leg 2's greps are written independently of the parser's constants and §3.4 forbids the refactor that would merge them; the accepted precedent is a verify run at a *different seat* on a *grown* corpus |

## 11. The build bar and the named consumer (E14 Ruling 35)

**Landed mid-session, after this spec's first draft, and it governs.** The Director's
word, 2026-08-08, charters the polish arc and puts these four tools inside its sequence:

- **The bar is shipcheck, not prototype.** *"BUILT and VERIFIED PROPERLY WITH TESTS —
  the studio's shipcheck bar."* A working prototype does not satisfy clause 2 of the
  charter. **Under in-facet placement the bar's applicable items are tests, a verify
  script, CI green, structured errors and accurate `--help`** — the package-level items
  (v1.0.0, semver, landing page, translations) attach to a published package and are *not
  yet applicable*, not skipped. The memo's §5 carries the item-by-item split.
- **The first consumer is named before the tool is built** — built-vs-filled applied at
  birth. For this tool it is the polish arc's own sessions: every advisor fold and
  executor seat across four exemplars queries the record instead of reading it. That is
  the dogfood, and it is the same loop this spec was written inside.
- **Sequencing is the charter's first clause**: nothing in the polish arc opens until
  these tools pass their tests.

One consequence for this spec specifically: the polish arc will grow the record fast —
four subjects, each producing rulings, reports and predictions. **§6.5's growth
sensitivity stops being a design note and becomes the operating condition**, and the
seeded set's withdrawn-never-recrafted rule (§6.4.3) will be exercised for real. Expect
withdrawals; they are the leg working.

## 12. Open questions for the Director

**Narrowed by the placement ruling.** Three questions that were open in the first draft
are now closed by it: the package name, the package's visibility, and whether §6 ships as
config on day one. An in-repo server publishes nothing and has no package name; facet is
already public; and §6 is written-not-built (§6's closing note).

What remains:

1. **Placement itself** — [the memo](placement-memo.md), §3.1. One sentence overrules it.
2. **The CI and test scope**, which is the real cost of in-facet placement and the memo's
   §5 states it: facet has no tests and no CI today. My recommendation is a **paths-gated
   workflow on `tools/**` plus tests covering only the new MCP surface** — not a
   retrofit onto instruments whose numbers are already banked. Yours to scope in a
   sentence.
3. **Whether `q`'s existing CLI stays** alongside the MCP surface. My recommendation:
   **yes, unchanged.** It is cited 35 times across the record and the kickoff ritual runs
   it; an MCP surface that retires the CLI would break the ritual to gain nothing.
4. **The extraction trigger, confirmed or tightened.** I have it as *a second repo adopts
   the conventions*. If you want a different trigger — a request from another studio lane,
   say — it is cheaper to name it now than to argue it later.
