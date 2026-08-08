# Spec 3 — fixture-lint

**Charter.** Authored by the advisor (spec-author seat), 2026-08-08. **Nothing is built.**

---

## The job

**Validate an identity specification before anything is generated from it.**

An identity fixture is the document that says what a subject *is* — every element, the
surface it owns, the words that carry it into a prompt. It is the only thing standing
between "the model painted a character" and "the model painted *this* character.

The rule the whole lint serves: **if a canon element is not named in the prompt, it is
arriving by accident and will leave the same way.** That was learned expensively — a
registration improvement silently replaced a character, because identity was riding in an
artifact nobody had declared was carrying it. The proof it can ride elsewhere is one
phrase: naming the gold knee plates restored armour that had only ever reached the image
through a noisy ControlNet, with the control byte-matched so the term was the only
difference.

Today every check below lives in prose, in a discipline document, applied by whoever
remembers. The lint makes them mechanical.

## The checks

Each is a rule the record paid for. Severities: **error** (generation will produce a
known-wrong result), **warning** (a measured hazard), **note** (declare-or-explain).

| # | check | severity | what it catches |
|---|---|---|---|
| 1 | **Occupancy completeness** — every modelled structure appears in the audit table | error | the gap discovered at generation instead of at authoring |
| 2 | **Single ownership** — each surface is owned by exactly one element | error | two elements fighting for one surface |
| 3 | **No decoration of an occupied surface** | error | the silent no-op: a spec determines what *occupies* a surface and cannot add a second element to one already occupied |
| 4 | **Every element is its own noun phrase** | error | elements that dissolve into a neighbour's phrase |
| 5 | **Terms are comma-free** | error | an internal comma shatters a term at the stem builder |
| 6 | **Colour words name materials that ARE their colour** | warning | palette/register interaction — literal reads under a realism register |
| 7 | **Family-word sprawl** — no family word rides more surfaces than it owns | warning | the measured gold-sprawl class |
| 8 | **Declared hue occupancy present, and marked checked-not-assumed** | warning | occupancy claims go stale |
| 9 | **Register declared, per subject, not inherited** | note | a register arriving by inheritance instead of by decision |
| 10 | **Stressors carry an evidence label** — measured / principle / unread guess | note | a guess wearing a measurement's clothes |
| 11 | **Mesh-supplied elements recorded as dependencies** | note | assuming geometry that the control must actually supply |
| 12 | **No numeric gate armed on a below-floor element** | warning | gating an element that is below any area floor by construction |

**Check 3 is the one that pays for the tool.** Asking for a gold plate onto an existing
fur cuff produced **no response at all** — ΔE 1.07, in two different grammatical forms —
where elements that *replaced* their surface's occupant landed in full. It is a silent
failure: nothing errors, the image comes back, and the element is simply absent. A lint
catches it in one second; a generation run catches it after the credits are spent, if
anyone happens to look at that surface.

**Check 1 is the one that generalises.** A single observation about one structure being
unowned generalised into an occupancy audit "done once and completely" — the pattern that
then caught the prop's gaps *on authoring day one*, before a single image existed.

## The test corpus

This lint has an unusual advantage: **its regression corpus already exists as history, and
its expected outcomes are already ruled.** Fixtures and their known catches, all in the
facet record:

- **the beast** — the occupancy audit's origin; an unowned structure found by eye, then
  the audit done completely
- **the prop** — the audit run at authoring, day one, and a term **earned** at the pair
  when a watch-note fired: one element's second surface was mislanding on one view, so it
  became its own noun phrase
- **the rejected artifact** — a generation carrying material not in the spec; the
  recorded example of family sprawl, kept in the record with its measurement
- **the ship and the character** — two more fixtures, different element counts (twelve and
  eight against the prop's five)

Every one of those is a test case where the expected output is a ruling, not an opinion.
**Build the corpus from the record before writing the first check** — the outcomes are
pre-registered by history, which is as close to a blind test as a lint gets.

## The home — the one placement the advisor does not rule

**⚖ RULED (Director, 2026-08-08): SDLAB — Option A below is the home.** Option B and
the split-shape flag stay in place as the record of the decision surface he ruled on.

**Two sound arguments point in opposite directions, and the tie-breaker is a
studio-ownership judgment the Director holds.** Both are stated at full strength. This
was the only one of the four tools left open; the other three are ruled in
[the memo](placement-memo.md).

### Option A — inside `style-dataset-lab`, as an `sdlab` verb

**sdlab already owns the per-project canon system** — constitution, lanes, rubric,
terminology, art contracts. The studio constitution records that this ownership is
*settled*: `visual-design-bible` was excluded from the map **because** sdlab subsumes it.
An identity fixture is a canon artifact, so a linter for identity fixtures belongs to
whatever owns canon, and something already does.

**And it buys the thing nowhere else can:** sdlab knows the project's declared vocabulary.
**Checks 6, 7 and 9 are checks against a registry inside sdlab and English heuristics
outside it** — that is the difference between "this colour word is off-register for this
project" and "this word looks like a colour to me."

*(Constitution records sdlab at v3.3.0, verified 2026-07-07 — **over 30 days old, so
advisory under the freshness rule.** The version does not affect the argument; the home
does not move on a version bump. Confirm before the build session, not before this spec.)*

### Option B — in facet, beside the record that paid for every check

**The test corpus is here** — five fixtures whose catches are already ruled, which is this
lint's whole claim to an external verifier. **And the first two live jobs are here**: the
humanoid's register re-authoring and the sword's activated state, both named by Ruling 35.
Built in facet, corpus and consumer are in hand on day one. Built in sdlab, every
regression case reaches into another repo.

### What I would do, and how weakly I hold it

**Weak lean: Option A, sdlab.** Grounds: **check 3 — the one that pays for the tool — is
subject-independent and works anywhere**, so facet's corpus advantage is a build-time
convenience rather than a capability. The registry-dependent checks are the opposite:
6, 7 and 9 **cannot be recovered later without the move happening anyway**, so building in
facet means either shipping them degraded or doing the migration eventually.

**A third shape exists and I am flagging it rather than recommending it:** split the tool —
grammar (4, 5) and structure (1, 2, 3) checks need no vocabulary and could live anywhere;
only 6, 7 and 9 need the registry. That is a real seam, and it is also **how a tool ends up
half in each repo, which is worse than either option.**

## What it does NOT do

- **It does not judge whether the identity is good.** Whether this is the right character
  is the Director's, and no metric approximates it. The lint checks that the specification
  is *well-formed and complete*, never that it is *right*.
- **It does not write to a fixture.** No autofix, no "add the missing row for you". A
  fixture is canon; a linter that edits canon is a second author. It reports and points.
- **It does not generate anything**, and it does not call a model. Every check above is
  deterministic text and structure analysis over a declared vocabulary.
- **It does not enumerate the mesh's structures for you.** Check 1 verifies that the audit
  table is *complete against a declared structure list*; producing that list is a human
  act with the geometry in front of them, and pretending otherwise would let the lint
  certify an audit against its own guess.
- **It does not gate generation by default.** It exits non-zero on errors so a caller
  *can* gate; arming it is the pipeline's decision.

## Compensators

| action | irreversible? | compensator | post-rollback state | owner |
|---|---|---|---|---|
| linting a fixture | no | read-only on every fixture — no undo needed | unchanged | — |
| writing a lint report | no | delete it; derived from the fixture | regenerable | the caller |
| **autofix / fixture edits** | — | **not implemented, and out of scope permanently** (see above) | — | — |
| an sdlab release carrying this verb (Option A, later session) | **yes** | `npm deprecate` the version; publish a fixed patch | bad version visible, marked | the publishing session |
| in-facet placement (Option B) | no | publishes nothing; the row above does not fire | — | — |

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every check cites the rule and the record site that paid for it; the lint is deterministic text analysis with no model call, so a run is replayable from the fixture and the project vocabulary alone |
| ANDON_AUTHORITY | 2 | errors exit non-zero so a pipeline can halt on a malformed fixture before spending credits. Scored 2 rather than 3 because arming the halt is the caller's decision and the lint cannot enforce being run. **Remediation: whichever host is ruled wires it into the pre-generation path so the check lives inside the tool that spends the money — owner: the build session** (E08 A32: a check a shell chain can walk past is not a gate). Note this favours Option A slightly — sdlab *has* a pre-generation path to wire into; facet's generation runs through the route's own tools |
| NAMED_COMPENSATORS | 3 | complete above; the strongest entry is that the destructive path (autofix) is refused rather than compensated |
| DECOMPOSE_BY_SECRETS | 3 | grammar checks (4, 5) are subject-independent and live in the linter; vocabulary checks (6, 7, 9) resolve against the project's own registry; structure checks (1, 2, 3) resolve against the fixture's declared structure list. Three groups, three change rates, three homes |
| UNCERTAINTY_GATED_HUMANS | 3 | the lint refuses to enumerate structures for the human (check 1's boundary) rather than guessing and certifying its guess; severities separate "will produce a known-wrong result" from "declare or explain", so a human is asked only where the answer is theirs |
| EXTERNAL_VERIFIER | 3 | the regression corpus is history with pre-registered outcomes — five fixtures whose catches were ruled by a different seat, at a different time, for a different purpose. A lint graded against rulings it did not author is the strongest external verifier available to a linter |

## The build bar and the named consumer (E14 Ruling 35)

**Landed mid-session, after this spec's first draft, and it governs.** The Director's
word, 2026-08-08: built and verified properly with tests — **the studio's shipcheck bar,
not a prototype bar** — before the polish arc opens.

**This lint's first consumer is unusually well matched to it.** Two of the polish arc's
named upgrades are fixture events, not generation events:

- **The humanoid re-made photo-real without the style adapter** is a *register* change,
  and the register-is-subject-data law means its fixture is re-authored at that arc's
  designation moment rather than inheriting. A re-authored fixture is exactly what checks
  6, 7 and 9 exist for — and it is the first one authored after the checks exist.
- **The sword's activated state** adds an element to a fixture whose occupancy audit is
  already complete and closed. That is **check 3's hardest live case**: an element that
  decorates an occupied surface is predicted to drop, and an element that *replaces* its
  surface's occupant lands. The lint gets to fire on that distinction before the credits
  are spent rather than after.

The lint therefore ships with two real jobs waiting, on fixtures whose prior state is
already in the record. That is built-vs-filled applied at birth.

## Open questions for the Director

1. **THE HOME — sdlab or facet.** The open one, both cases above at full strength, my lean
   weak and toward sdlab. **This is the only placement of the four still unruled**, and it
   is the one question in this spec whose answer changes what gets built.
2. **Verb or MCP tool or both.** sdlab is a CLI; the studio's canon work runs through
   Claude sessions. My recommendation is **both** — the check is the same, the surface is
   cheap — but it doubles the docs surface.
3. **Does check 1 require a machine-readable structure list?** Today the structure list is
   a markdown table authored by eye. Requiring JSON makes the check exact and adds an
   authoring burden to every fixture. My recommendation: **accept the markdown table,
   parse it by its column convention** — the index spec's whole §6 argues that parsing a
   record's own conventions beats making authors serve the parser.
