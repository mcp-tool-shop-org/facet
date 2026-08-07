# E15 — the context index, P1: built against the existing record

Executor session, 2026-08-07. Predictions: [E15-predictions.md](E15-predictions.md)
(`763de62`, registered before the builder existed). Spec:
[docs/context-architecture.md](../context-architecture.md). Dispatch:
[E15-context-index-kickoff.md](E15-context-index-kickoff.md).

**Built against `27ecbf7`.** The record moved six commits under this session — see
§7. No generation, no GPU, no credits. No record file was edited.

---

## 1. What was built

| path | what |
|---|---|
| `tools/facet_index.py` | the builder / verifier / query tool — three verbs, 1,554 lines |
| `docs/index/facet.db` | the generated index — one file, ~5.9 MB |

```bash
python tools/facet_index.py build && python tools/facet_index.py verify
```

## 2. Counts per table, against the predicted bands

| table | rows | predicted | |
|---|---|---|---|
| `rulings` | **285** | 250–290 | held |
| `laws` | **69** | 50–70 | held — but only after two parser fixes; the first build gave 49 |
| `experiments` | **15** | 15 | held exactly |
| `handoffs` | **20** | 18–22 | held |
| `artifacts` | **451** | 80–400 | **missed high** |
| `phenomena` | **22** | 8–20 | **missed high**, narrowly |
| `decisions` | **217** | 150–220 | held |
| `fts` | **2,536** | ≈ sum of prose rows | held |

Plus **1,457 prose sections across 159 files** — the reports, halts, predictions,
specs and kickoffs, indexed for FTS with no ontology row of their own. The dispatch
names *report headers* as a parse target and the measurements live there; an index
that finds the ruling but not its evidence is half an index.

*These are the counts with this report present, since the report is part of the
record it indexes. It contributes 14 prose sections and — because §4e quotes the
phantom path `j/inpainted.png` as an example of a phantom — exactly one artifact
row — the self-reference property of §5 demonstrating itself on a path that only ever
existed as an example of a phantom.*

`rulings` decomposes as: E12 30 rulings + 154 lettered sub-rulings + 1 closure ·
E04 29 · E08 35 amendments · E10 12 · E10-offsurface 7 + 6 subs · E11 7 + 4 addenda.

**The two bands I said I would miss are the two I missed** (predictions P1/P5), and
for the predicted reason: every other table indexes a convention the record follows,
while `artifacts` and `phenomena` index categories the record names in prose without
a marker. Their weakness is quantified in §5.

## 3. The verify gate — all four legs pass, exit 0

### Leg 1 — determinism: **byte-identity holds** (P3 confirmed)

Two builds from an unchanged record are byte-identical. The pre-registered `.dump`
fallback was **not needed**. Stronger than the prediction: the DB is byte-identical
**across interpreters** — Python 3.14.5 and 3.13.13 (the trellis env), both on SQLite
3.50.4, produced the same sha256 on every build tested.

*No sha or exact byte count is quoted for the shipped file, and that is deliberate:
this report is part of the record the index covers, so writing the DB's own digest
into it changes the DB and invalidates the digest. Leg 1 tests determinism by
comparing two fresh builds, which needs no fixed point; `git` records the committed
file's hash.*

What makes it hold: an explicit sorted file list, `sorted()` on every traversal, one
transaction for the whole build, a fixed `page_size`, a final `VACUUM`, and no
timestamp or random value written anywhere.

### Leg 2 — counts, against the verifier's own greps

The verifier re-derives every count from the record with patterns written
independently of the parser's constants.

```
E12 numbered rulings         grep   30   db   30   ok
E12 lettered sub-rulings     grep  154   db  154   ok
E12 closure markers          grep    1   db    1   ok
E04 lettered sub-rulings     grep    0   db    0   ok
E10off lettered sub-rulings  grep    6   db    6   ok
E04 numbered rulings         grep   29   db   29   ok
E10 numbered rulings         grep   12   db   12   ok
E11 numbered rulings         grep    7   db    7   ok
E11 post-ingest addenda      grep    4   db    4   ok
E08 amendments               grep   35   db   35   ok
E12 handoffs                 grep   15   db   15   ok
E04 handoffs                 grep    5   db    5   ok
E12 sequence                 ruling 1-28 gaps: none
  ↑ completeness             ABOVE the dispatched bound of 28: [29, 30]
E04 sequence                 ruling 1-28 gaps: none
  ↑ completeness             ABOVE the dispatched bound of 28: [29]
E08 sequence                 amendment 1-35 gaps: none
E11 sequence                 ruling 1-7 gaps: none
E10 sequence                 ruling 1-12 gaps: none
E12 handoffs 1-16            present [2..16]   missing [1]
experiments E01-E15          have 15, missing none
```

**The dispatched sequence bounds were left exactly where they were written.** Both
E04 and E12 carry rulings *above* the bound the dispatch named, and rather than
widen a pre-registered condition after seeing the result, the gate prints a separate
completeness line. Two findings ride on it, §4.

**E12 handoff 1 is genuinely absent** and the gate asserts exactly that: E12's first
dispatch is the kickoff's own `## The task`, never labelled "Session handoff 1". Its
prose is indexed; its handoff row is not, because minting one requires inventing a
mapping the record does not make.

### Leg 3 — pointers: **zero dangling, 1,079 rows checked**

Every row's file exists and its `locator` — the exact string as written in that file
— is findable there.

```
rulings 285 · laws 69 · experiments 15 · handoffs 20 · artifacts 451 ·
phenomena 22 · decisions 217 · fts 2536      dangling 0 everywhere
```

Anchors come in two forms deliberately: `anchor` is the human label a session cites
("Ruling 25c"), `locator` is the findable literal (`**25c `). GitHub mints anchors
for `#`-headings only, so a bold sub-ruling lead has none — predicted (P2 #8) and
implemented.

### Leg 4 — the seeded question set: **14 / 14**

The dispatch's twelve questions, with two split into their two component holdings
(the backdrop word and its 15i correction; the elevated closure at 7a and again at
25b) because each is a separate row and reporting one rank for two answers would
hide which was found.

| question | rank | target |
|---|---|---|
| canny values for the beast | 3 | E12-ruling.md · Ruling 11a |
| which seed resists terms | 2 | E12-ruling.md · Ruling 21c |
| the backdrop word and why | 1 | E12-ruling.md · Ruling 8a |
| the backdrop word's correction | 1 | E12-ruling.md · Ruling 15i |
| thin_extent on the beast | 1 | E12-ruling.md · Ruling 25c |
| why elevated cameras are closed | 1 | E12-ruling.md · Ruling 7a |
| why elevated cameras stay closed | 1 | E12-ruling.md · Ruling 25b |
| the dragon's reach ceiling | 1 | E12-ruling.md · Ruling 6a |
| what happened to the crop pass | 1 | E12-ruling.md · Ruling 24b |
| when the pair was accepted | 1 | E12-ruling.md · Ruling 14 |
| the fifth brush signature | 1 | E12-ruling.md · Ruling 27d |
| what a ruling pays values in | 1 | E12-ruling.md · Ruling 26a |
| the retired keying method | 1 | CLAUDE.md · Corner-median keying has failed three times |
| the galleon's accepted mix | 2 | E04-ruling.md · Ruling 27 (or README / handbook) |

**No question was deleted or re-phrased to pass.** The prediction was 10–11 of 12 on
first phrasing; the first mechanism scored 12/14 and the route to 14/14 is §6.

## 4. Findings about the record — reported, not edited

No record file was touched. Each of these is a report item.

**a. E04 carries a Ruling 29; the prose says 28.** `docs/experiments/README.md` and
`docs/handbook/subjects.md` both say *"28 rulings + the close"*, and
`E04-ruling.md:1760` is `## Ruling 29 — the asset-2 blob-bound halt`. The dispatch
inherited the same figure. E12 likewise stood at 28 when this session began and is
now at 30.

**b. A closure-marker convention exists, once.** `E12-ruling.md:1229` reads
`**18g-CLOSED (Director, 2026-08-06): "Keep ivory, judge on asset."**` — a *closure*
of sub-ruling 18g carrying the Director's own sentence, not a sub-ruling. Measured
across all five ruling documents, the lettered marker is `**<n><letter> <dash>` —
letter, **space**, dash — **151 times of 152**. A dash class tolerating a bare hyphen
swallows `18g-CLOSED` into `18g` and loses one of the two holdings. It is now its own
row with kind `sub-ruling-closure`, and the verifier counts it separately.

**c. Three ruling documents carry no numbered rulings at all** (P2 #3, confirmed).
E01/E02/E06/E07's gate-1 rulings and `E08-director-canon-ruling.md` use topical
headers (`## The ruling`, `## What is withdrawn`). They cannot enter `rulings` by any
numbering convention and are indexed as prose sections instead. **Granularity across
the record is therefore deeply asymmetric** (P2 #2): E12 resolves to 154
sub-rulings, E04/E10/E08 resolve only to whole rulings, and these five resolve only
to sections. No parser fixes that; it is a property of how the arcs were written.

**d. CLAUDE.md's lists carry no blank line between items**, and one item contains a
blank line. Both defeat a blank-line paragraph splitter. Before the fix, **2 of the
10 role rules** were indexed and the four `Judging artifacts` and eight
`Standing technical constraints` bullets were absent entirely; after splitting on
list markers, 8 of 10; after allowing the split anywhere in a block (advisor rule 3
runs to two paragraphs, so rules 4 and 5 sat in a block that no longer began with a
marker), **10 of 10 and 69 laws total**.

**e. The record writes Windows paths with backslashes**, and shell fragments with
variable prefixes (`"$j\inpainted.png"`). Normalising separators into the *locator*
broke eight pointers; the `$` prefix minted a phantom artifact `j/inpainted.png`.
Artifact keys are now separator-normalised while locators stay raw.

**f. `E08-ruling-gate0.md:2237` is a `###` line naming an amendment that is not that
amendment's header** (P2 #4, confirmed): `> ### Amendment 32's diagnosis is corrected
in place`. Requiring the `(author, date)` parenthesis rejects it; the E08 count is
exactly 35 with no gaps.

**g. Three experiments have no README-table row** — E13, E14, E15. They enter from
disk with status `not in the README table`, anchored at their own document's first
heading. E12's table row is also stale (it says "Rulings 1–8"). Reported; not fixed.

**h. Dates: the prediction inverted** (P2 #7). I predicted sub-rulings would mostly
lack a date. Measured: **160 of 160 sub-rulings carry one** (inherited from the
parent header), and it is the **numbered rulings that are the gap — 71 of 85**.

**i. A lettered marker opening a paragraph for a *different* ruling never happens.**
Predicted as a hazard; the skip counter reads **0** across the whole record.

## 5. Where P1 is honestly weak

The boundary of what this delivers, stated plainly because it decides what P2 and P3
are worth.

**`artifacts` is extraction, not parsing.** 449 rows by path shape — 245 renders,
124 data, 36 meshes, 20 arrays, 19 scripts, 5 logs. But **427 of 449 carry no
status** (a status word had to stand in the same paragraph) and **432 of 449 carry no
provenance ruling** (the nearest preceding ruling in the same file — a locality
heuristic, labelled as one). What the table is good for: *where is this file
mentioned, and how often*. What it cannot answer: *was this artifact accepted*.

**`phenomena` is 22 rows read off six different naming verbs** — `banked as` 12,
`is NAMED` 6, and one each of `new law`, `named forward`, `minted`, and
`banked as a measured phenomenon`. The record mints its phenomena out loud but never
the same way twice. A phenomenon named without one of those verbs is invisible here.
The alternative — a hand-kept list — is forbidden by the design, and rightly: the day
it is hand-edited it is wrong by definition.

**`supersedes` / `superseded_by` are all but empty: 2 and 1.** Only explicit
correction verbs aimed at a numbered ruling are linked. The record mostly corrects by
narrative (*"the WORD STANDS, anchored by…"*), which no pattern reads without
guessing. This is the single largest gap between the spec's schema and what P1
delivers, and it is a lower bound by construction rather than a measurement.

**`laws.paid_for_by` reaches 11 of 69.** It captures an experiment id cited in the
law's body; most laws state their cost in prose (*"cost a session"*, *"three
instances now"*) without naming one.

**`rulings.verdict` classifies 82 of 285.** The remaining 203 are rulings whose
holding announces no capitalised verdict — largely sub-rulings that report rather
than decide. Authority splits 30 Director / 255 advisor.

**The index indexes its own dispatch.** `E15-context-index-kickoff.md` quotes every
seeded question verbatim, so it is an exact-phrase match for its own question labels
and takes rank 1 for `q "the fifth brush signature"` and `q "thin_extent on the
beast"` — ahead of Ruling 27d and Ruling 25c. The *content* phrasings the gate uses
return the rulings at rank 1–3, so this is not a gate failure; it is a real property
of a self-referential corpus, and P2's slimming reduces it.

## 6. What `q` does, and how the mechanism was chosen

Two stages: an **exact-phrase best-bet** (capped at 3 slots), then bm25 scaled by the
fraction of query terms the row carries. Stopwords are dropped from stage 2 — measured
on this corpus, `the` appears in **94.9%** of indexed rows, `is` in 77.9%, `not` in
62.2%, so a disjunction carrying them matches nearly everything while the
discriminating term (`galleon` 10.0%, `mix` 1.7%) is one weak signal among many.

Every variant tried, scored on the seeded set. All are generic retrieval mechanisms;
none knows about a specific document.

| mechanism | seeded set |
|---|---|
| bm25 alone, stopwords kept | 12 / 14 |
| bm25 alone, stopwords dropped | 12 / 14 |
| coordination level as primary sort key | **9 / 14 — falsified** |
| title-coverage as primary sort key | **11 / 14 — falsified** |
| bm25 × term coverage | 13 / 14 |
| **exact-phrase-first + bm25 × coverage** | **14 / 14 — adopted** |

The two falsified variants failed for one reason: they discard bm25's length
normalisation, and long prose sections trivially contain every query term.

The last row is worth its own sentence. `THE PAIR IS ACCEPTED` is Ruling 14's title
verbatim, and Ruling 14 has the **highest term frequency in the corpus** for those
words (pair 8, accepted 5) — yet it lost to a 221-character sub-ruling that mentions
them twice each, because its own body is 2,084 characters and bm25 is doing exactly
what it is designed to do. A bag of words cannot separate an acceptance from three
rulings that mention an accepted artifact; the exact phrase can.

**bm25's column weight is inert here.** Title weights of 8, 30 and 100 return
identical rows and identical scores, so the title-vs-body weighting is not the lever
it looks like.

## 7. Two defects that were mine, and one cross-lane event

**a. `classify()` upper-cased the holding before matching verdicts**, which destroyed
the record's own convention. The record shouts a verdict — `THE PAIR IS ACCEPTED`,
`the pair is REJECTED` — while the same word in lower case is an adjective:
*"D9's wine has no cluster on the accepted pair"* accepts nothing. Three rulings were
marked ACCEPTED that accept nothing, and two of them then outranked the actual
acceptance. Fixed by matching case-sensitively. **The prediction I registered for the
verdict/authority schema change — that it would lift Ruling 14 into the top 3 — was
wrong**; the change was independently right and did not move that question.

**b. `_decision_status` scanned the whole `why` string** and so labelled three
*decided* profile values `UNDECIDED`, including `beast.texpass_iter.thin-extent`,
whose `why` reads *"the arc's one deliberately undecided value"* — ruled 0.005 by E12
Ruling 25c. **An index reporting a decided value as undecided is a second authority
contradicting the record, which is the one thing this design exists to prevent.** The
class label is now read only from the head of `why`, which is the profiles' actual
convention (`FIRST-RUN OPERATING POINT at…`, `PROTECTIVE TRANSCRIPTION (…)`,
`SPENT, WITH A BYTE ANCHOR`), and `_still_suspended` is indexed as its own 11 rows
carrying each entry's own disposition. Zero UNDECIDED rows remain.

Both are the same defect class, and it is the one this corpus punishes hardest:
**matching a word in narrative prose and reading it as a status.**

**c. Parent ruling bodies duplicated their sub-rulings' text.** Ruling 4's body ran
3,932 characters including its five children, so a parent competed with its own
sub-rulings and diluted length normalisation for both. Parents now carry only their
own prose.

**d. Cross-lane: six commits landed in this working copy during the session** —
`0ac88fa`, `0966e1a`, `09c4960`, `f882631` (handoff 16), then `9e1b5d2` and
`27ecbf7` (E12 Rulings 29 and 30). **No path collision**: that lane touched
`E12-handoff16-*.md`, `E12-ruling.md`, `e11_export_turnaround.py` and
`e11_manifest.py`; this session touched `tools/facet_index.py`, `docs/index/facet.db`
and its own three documents. Nothing under a handoff-16 path was opened for writing.

It produced a finding worth carrying into P3. **`E12-ruling.md` grew by 107 lines
mid-build, and a seeded question that passed at 2,444 FTS rows missed at 2,475.** The
cause was not the growth itself: the miss exposed that my target list for *the
galleon's accepted mix* named two files when the record states that value in three —
`E04-ruling.md:1658` (Ruling 27), `README.md:85`, and `docs/handbook/subjects.md:31`,
enumerated by grepping the record for paragraphs carrying all of 36.89 / 6.87 /
56.24. The handbook row is the one the index returns. Left file-level, the same gate
had passed on **Ruling 24**, which shares the six query words and carries none of the
digits — *a gate that cannot tell the right row from a coincidence is not testing
anything*, so both loose targets are now pinned to the rows that carry their values.

**The ritual implication: the seeded gate is sensitive to corpus growth**, and it
must be re-run on every fold rather than trusted from the fold before.

## 8. Predictions, scored

| prediction | outcome |
|---|---|
| P1 row bands | 5 of 7 held; `artifacts` (449 vs 80–400) and `phenomena` (22 vs 8–20) missed high — both named in advance as the ones I expected to miss |
| P2 #1 bold-lead phantom | discriminator works — no `specification` law, the real law at CLAUDE.md:137 present |
| P2 #2 asymmetric granularity | confirmed — 154 E12 subs against 0 for E04/E10/E08 |
| P2 #3 three docs with no numbered rulings | confirmed — indexed as prose |
| P2 #4 `Amendment 32's` false header | confirmed — rejected by the `(author, date)` guard |
| P2 #5 handoff numbers collide | confirmed — arc-scoped; E04's first is unnumbered |
| P2 #6 E11 addenda under another noun | confirmed — 4 rows via a second pattern |
| P2 #7 dates sparse on sub-rulings | **inverted** — 160/160 subs have one; 71/85 numbered rulings do |
| P2 #8 no HTML anchor for sub-rulings | confirmed — anchor/locator split |
| P3 byte-identity | **confirmed**, and it holds across two interpreters |
| P4 10–11 of 12 first phrasing | first mechanism 12/14; final 14/14 after four measured mechanism changes |
| P4 `galleon's accepted mix` at risk | **correct** — it was the last question to land, for the predicted reason |
| P5 `artifacts`/`phenomena` weakest | **confirmed** — 427/449 no status, 432/449 no provenance; 22 phenomena from six verbs |
| unpredicted | the `18g-CLOSED` convention; E04's Ruling 29 against the prose's 28; CLAUDE.md's blank-line-free lists; backslash paths; and the two status-from-prose defects in §7 |

## 9. Explicitly not done, each with the reason

- **P2 (slimming the entry documents)** — a separate advisor-led pass measured in
  lines shed. Doing it here couples the index's birth to editing the record it
  indexes.
- **Vector / embedding search** — the spec rules it out; FTS misses get measured
  first, and §5 is that measurement.
- **Editing any record file** — the record is canonical. Every §4 item is a report
  item; zero record files were modified.
- **A hand-maintained anything** — including the tempting hand-kept phenomena list.
  The DB is derived forever.
- **P3 (the standing ritual)** — not this session's work, though §7d hands it a
  requirement: `build` + `verify` on every fold, because the seeded gate moves with
  the corpus.

**One operational note for P3, offered rather than acted on.** The committed DB is
~5.9 MB of binary that is byte-different after every fold, so each fold adds roughly
that much to git history permanently — `.gitignore`'s own premise is *"large and
regenerable"*, and this file is both. The spec rules it in-repo for a good reason
(one `git pull`, no build step for a fresh relief), and that ruling stands; this is
only the cost of it, measured, for the Director's and the advisor's eye when the
ritual is written.

## 10. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the DB is a pure function of the record at a commit — byte-identical across two builds *and* two interpreters; the builder is committed beside it and takes no tuning parameters; predictions registered at `763de62` before it existed |
| ANDON_AUTHORITY | 3 | `verify` exits non-zero on any of four legs and prints the failing evidence; it fired six times during this session (a duplicate key, three dangling-pointer classes, and two seeded misses) and each halt located a real defect — §4b, §4e, §7 |
| NAMED_COMPENSATORS | 3 | exactly one path written (`docs/index/facet.db`); the record is opened read-only; undo is deleting two new files, neither of which any other tool consumes |
| DECOMPOSE_BY_SECRETS | 3 | the parser knows conventions, the schema knows ontology, the verifier knows neither's internals and re-derives every count with its own greps; profiles stay the value registry and markdown stays the authority |
| UNCERTAINTY_GATED_HUMANS | 2 | §4 and §5 stage the parse limitations and the weak tables for the advisor's eye rather than resolving them; the completeness line surfaces the out-of-bound rulings without widening a pre-registered gate |
| EXTERNAL_VERIFIER | 3 | the seeded key is advisor-authored and its targets are record anchors the builder never reads as input; counts come from independent greps; where the key was incomplete (§7d) the completion was enumerated **from the record**, not from what ranked |
