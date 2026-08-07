# E15 — predictions, registered before the builder exists

Executor session, 2026-08-07. Registered against `530b6bf` before a line of
`tools/facet_index.py` was written.

---

## Disclosure — what was seen before predicting, and what was not

These predictions are **not blind**, and pretending otherwise would be the exact
failure this repo's calibration line exists to prevent. Stated precisely:

**Seen before writing this file** (structural survey; no counting beyond what is
quoted here):

- The `^#{1,6}` heading lists of `E12-ruling.md`, `E04-ruling.md`, `E11-ruling.md`,
  `E10-ruling.md`, `E08-ruling-gate0.md`, `E10-offsurface-ruling.md`, and the four
  gate-1 rulings + `E08-director-canon-ruling.md`.
- A count of bold lettered sub-ruling markers per ruling file: **E12 142, E04 3,
  E10-offsurface 6, every other ruling file 0.**
- The handoff header list: `E04-executor-kickoff.md` carries one *unnumbered*
  "Session handoff" (marked SUPERSEDED) plus 2–5; `E12-executor-kickoff.md`
  carries 2–16.
- `CLAUDE.md`'s heading list and its 48 lines matching `^\*\*`.
- The three profiles' top-level keys, and `beast.json`'s nine tool blocks.
- The `docs/experiments/README.md` experiment table (12 rows).
- The E08 amendment convention: `> ### Amendment N (author, date) — title`,
  inside a blockquote, with Amendment 1 carrying a `⚠` before the word.
- **That all twelve seeded-question anchors exist as real lines.** Checked first,
  deliberately: a gate whose reference is wrong fails honest work.

**Not seen, and genuinely un-run** — everything below is a real prediction: final
row counts per table, artifact and phenomenon extraction (no convention was
inspected for either), which conventions defeat the parser in practice, the
determinism leg, and every FTS result.

---

## P1 — rows per table, order of magnitude

| table | order | predicted range | reasoning |
|---|---|---|---|
| `rulings` | 10² | **250–290** | numbered: E12 28 + E04 28 + E10 12 + E10-offsurface 7 + E11 7 + E08 35 ≈ 117; lettered subs 142 + 3 + 6 = 151 |
| `laws` | 10¹ | **50–70** | 48 bold-lead lines in CLAUDE.md, less ~2 wrapped-paragraph false positives, plus the 10 numbered role rules |
| `experiments` | 10¹ | **15** | E01–E15 exactly; the README table carries only 12 |
| `handoffs` | 10¹ | **18–22** | E12 2–16 (15) + E04 1–5 (5) |
| `artifacts` | 10² | **80–400** | the widest band on the sheet, because **no convention exists for these** — they are paths in prose and in JSON sidecars |
| `phenomena` | 10¹ | **8–20** | named effects; also conventionless |
| `decisions` | 10² | **150–220** | `beast.json` alone carries 64 decided keys across 9 blocks; three profiles |
| `fts` | 10² | ≈ sum of prose rows | derived |

**The two I expect to be wrong about are `artifacts` and `phenomena`**, and the
reason is the same for both: every other table indexes a *convention the record
actually follows*, and these two index a category the record names in prose without
a marker. A wide band is the honest statement, not a hedge.

## P2 — the conventions I expect to defeat the parser

Predicted in advance, so that finding them is confirmation and *not* finding them is
information:

1. **Bold-at-line-start that is not a law.** `CLAUDE.md:141` is
   `**specification**, not against the defect…` — a wrapped continuation of the
   paragraph beginning at 137. A naive `^\*\*` rule mints a phantom law. Predicted
   discriminator: require a blank line before. Predicted phantom count if the
   discriminator is omitted: **2–4**.
2. **Granularity is asymmetric across arcs.** E12 resolves to 142 lettered
   sub-rulings; E04, E10 and E08 resolve only to whole numbered rulings, because
   they sub-divide with `### ` topical subheads instead of letters. The index will
   be **fine-grained for the beast arc and coarse everywhere else**, and no parser
   fixes that — it is a property of the record.
3. **Three ruling documents have no numbered rulings at all.** E01/E02/E06/E07's
   gate-1 rulings and `E08-director-canon-ruling.md` carry ruling-class holdings
   under topical headers (`## The ruling`, `## What is withdrawn`). They cannot
   enter `rulings` by the numbering convention. Predicted: they enter as sections,
   and **any seeded question aimed at them would fail.** None is.
4. **A prose reference that looks like a header.** `E08-ruling-gate0.md:2237` reads
   `> ### Amendment 32's diagnosis is corrected in place` — a `###` line naming an
   amendment that is *not* that amendment's header. Requiring the `(author, date)`
   parenthesis should reject it; predicted duplicate count without that guard: **1**.
5. **Handoff numbers collide across arcs.** E04 handoff 3 and E12 handoff 3 are
   different dispatches, so the key must be arc-scoped. Predicted: E04's *first*
   handoff has no number at all and needs a decision rather than a regex.
6. **E11's rulings continue under a different noun.** Four "Post-ingest addenda N"
   sections are ruling-class and are not called rulings. Predicted: they need an
   explicit second pattern, or E11 undercounts by 4.
7. **Dates are inconsistently placed.** Some ruling headers carry `(2026-08-05)`,
   some `(Director, 2026-08-05)`, some nothing; sub-rulings almost never carry one.
   Predicted: **date is null on the large majority of sub-ruling rows**, inherited
   from the parent where the parent has one.
8. **Sub-rulings have no HTML anchor.** GitHub mints anchors for `#`-headings only;
   a `**25c — …**` bold lead is not one. Predicted resolution: the anchor is the
   *findable literal string* (`Ruling 25c`), and the verifier's dangling-pointer leg
   must search for that literal rather than for a slug.

## P3 — the determinism leg

**Prediction: byte-identity holds, and the `.dump` fallback is not needed.**
Reasoning: SQLite's file header carries no timestamp, and its change counter is a
function of the transaction sequence — which is fixed if the build's traversal and
insert order are fixed. FTS5's index is a deterministic function of insert order.
Named risk that would falsify this: any ordering that depends on dict iteration over
filesystem results, or an `ANALYZE`. Both are avoidable and will be avoided.

Confidence is moderate, not high — this is the prediction I would least mind losing,
because losing it costs one `.dump` comparison, and the fallback was pre-registered
before the first build for exactly that reason.

## P4 — the seeded question set

**Prediction: 10 or 11 of 12 pass on first phrasing.** Named at-risk, in advance:

- **"the backdrop word and why"** — the answer is *two* rows (Ruling 8a plus the 15i
  correction that keeps the word standing on a new anchor). A top-3 window may return
  one and not the other; whether that counts as a pass is a question for the ruling,
  and I will report the rank of *both* rather than declare it.
- **"the galleon's accepted mix"** — `36.89 / 6.87 / 56.24` are decimals inside a
  slash run. FTS5's default tokenizer splits on punctuation, so the query phrasing and
  the indexed form may not agree. Predicted failure mode if it fails: the row is found
  by the words *galleon* and *mix*, not by the digits.

**If a question fails, the finding is the parser's or the schema's — not the
question's.** No seeded question is deleted or re-phrased into passing. Where a
phrasing has to change, the change is reported as a measured fact about FTS
behaviour, with both phrasings quoted.

## P5 — what I expect to be the session's honest boundary

That `artifacts` and `phenomena` deliver materially less than the other six tables,
and that the report's most useful paragraph is the list of holdings the record carries
which **no convention makes machine-findable**. The index's value is bounded by the
record's regularity, and the beast arc is far more regular than the arcs before it.

---

## Standards compliance (this file)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | registered against `530b6bf` before the builder existed; every count band states its arithmetic |
| ANDON_AUTHORITY | 2 | P4 pre-commits to reporting a failed question as a parser finding rather than re-phrasing it into a pass |
| NAMED_COMPENSATORS | 3 | this file is additive; undo is deleting it |
| DECOMPOSE_BY_SECRETS | 2 | predictions separated by table, by convention, and by gate leg, so one being wrong does not implicate the others |
| UNCERTAINTY_GATED_HUMANS | 2 | the disclosure section states exactly which predictions are un-run, so the advisor can discount the rest |
| EXTERNAL_VERIFIER | 3 | the seeded key is the advisor's, authored before this session; the verifier greps the record itself rather than trusting the builder's counts |
