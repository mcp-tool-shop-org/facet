# E15 handoff 2 — predictions, registered before the `claims` verb exists

Executor session, 2026-08-07. Registered against `2b57726` before a line of the verb
was written. Dispatch: E15 executor kickoff, Session handoff 2.

---

## Disclosure — what I knew before predicting

Stated precisely, because this is the same seat that ran the hand-sweep last night
and a claim of blindness would be false.

**Known before writing this file:**

- Last night's hand-sweep found **four** stale sites: `advisor-kickoff.md:18` and
  `:57`, `subjects.md:59` and `:62` — reported to the advisor, not edited.
- `2b8a9b9`'s commit message, read just now: the consumed kickoff **gains a
  supersession banner** rather than a rewrite ("the rewrite stays the next
  relief's"), and the handbook's two stale lines were corrected in place
  (`Rulings 1-11 -> 1-30`; `80/81 -> 83/83`) plus a bone-ivory line caught in
  passing.
- The dispatch's own classification rule, which places the advisor kickoff's
  content **below** its banner outside the current-state class.
- That `a4d587a` (E14 Gate 0 predictions) and `2b57726` landed since.

**Not looked at, and genuinely un-run:** the current text of any of the four sites,
any count-claim anywhere on the current record, and every number below.

---

## P1 — how many stale sites remain: **0**

I agree with the advisor's healthy-zero, and by arithmetic rather than faith: two of
the four went out of the current-state class when the banner landed, and the other
two were corrected in place.

**The named risk that would falsify it**, and it is not hypothetical — it is the
growth-sensitivity property this arc already measured at §7d:
`README.md:141` states E12's count as an exact closed range (`Rulings 1–30`). That
line goes stale **the moment E12 gains Ruling 31**, and this arc has added rulings
mid-session twice in twenty-four hours. If the sweep returns non-zero, I predict it
is that line, or its sibling in the experiments table — not a site anyone missed.

Second, smaller risk: the handbook's dragon entry was corrected to `1–30` at
`2b8a9b9`, so it carries the same closed-range fragility.

## P2 — phrasing families the sweep must handle: **4–7**

Predicted shapes, from the ones the record has already shown this seat:

1. `N rulings` — README, handbook
2. `Rulings 1–N` — README's E12 line
3. `Rulings 1–N so far` — the handbook's per-subject entries
4. `N amendments` — E08
5. `N rulings + the close` — E04's handbook entry
6. `handoffs 1–N` — the advisor kickoff's reading list
7. `E01–E15` / `E01-E15` — the experiment span

Prediction: **all seven exist**; the sweep finds at least 4 of them on current-state
documents. The window must span a markdown link (`[E12-ruling.md]`) — last night both
this seat's regex and the advisor's grep failed on exactly that, using `[^.\n]` as
the window and so being unable to cross the `.md` inside the link text. That is the
single most likely way this verb under-reports, and it is why every family found gets
a printed test row rather than a silent match.

## P3 — at least one phrasing is genuinely ambiguous, not merely hard

**Prediction: `N rulings + the close` is unparseable-as-a-count and must be reported
as such rather than resolved.** E04's handbook entry reads `29 rulings + the close`.
Whether that asserts 29 or 30 is a question about what the record means by "the
close", and a sweep that picks one reading and compares against it is inventing a
claim to check. I predict at least this one row prints as **unparseable**, and I
predict the total unparseable count is **1–3**.

## P4 — the DB is untouched: **byte-identical before and after**

`claims` reads the committed DB and re-derives nothing. The verb lives in
`tools/facet_index.py`, which is not itself indexed (the corpus is `.md` under
`docs/` plus `CLAUDE.md` and `README.md`), so editing the tool cannot move the DB.

**Stated so it is not mistaken for a stronger claim than it is:** this session also
writes two `.md` files into `docs/experiments/`, which *are* record files, so a
future `build` will produce a different DB. That is not a violation — it is Ruling
4's session-boundary cadence, under which the committed DB is allowed to trail the
record by one session. I predict the committed DB ends this session **exactly at
HEAD**, and I will restore it if any run dirties it.

## P5 — what the verb will get wrong that I cannot predict away

The classification is by document, and the document list is the dispatch's. A file
that is *neither* a kickoff/spec nor on the current-state list — a new research note,
a style register — has no class. I predict the sweep meets **1–3 such files** and
that the honest handling is a third classification (`unclassified`) printed as such,
not a silent assignment to either side.

---

## Standards compliance (this file)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | registered against `2b57726` before the verb existed; every prediction states its arithmetic |
| ANDON_AUTHORITY | 2 | P3 pre-commits to reporting an ambiguous phrasing as unparseable rather than resolving it to a number |
| NAMED_COMPENSATORS | 3 | additive file; undo is deleting it |
| DECOMPOSE_BY_SECRETS | 2 | predictions separated by count, by phrasing, by ambiguity, by DB effect and by classification gap |
| UNCERTAINTY_GATED_HUMANS | 3 | the disclosure names exactly what this seat already knew, since it is the seat that produced last night's finding |
| EXTERNAL_VERIFIER | 2 | P1 agrees with the advisor's independent healthy-zero and names the one condition that would falsify both |
