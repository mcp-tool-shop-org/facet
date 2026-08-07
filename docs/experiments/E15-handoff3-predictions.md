# E15 handoff 3 — predictions, registered before the build path is opened

Executor session, 2026-08-07. Registered against `f963a7a` before a line of the
discovery fix was written. Dispatch: E15 kickoff, Session handoff 3 (Ruling 8b).

---

## Disclosure

Known before predicting: that `E15-ruling.md` carried **7** numbered rulings when
measured last session, that the dispatch names its bound as **1–8** (so Ruling 8
landed in `f963a7a`), that Ruling 8 has lettered sub-rulings (the dispatch cites
"8b"), and that the advisor reworded the `285 rulings` row out of the phrasing family
this fold. Not looked at: `E15-ruling.md`'s current text, its sub-ruling count, the
reworded table row, or any number below.

---

## P1 — what the glob discovers

**Prediction: 12 files**, every `docs/experiments/E??-*ruling*.md` — the six that
carry numbered content (E04, E08-gate0, E10, E10-offsurface, E11, E12) plus
`E15-ruling.md`, plus **five that carry none** (E01/E02/E06/E07 gate-1 rulings and
`E08-director-canon-ruling.md`). The five parse to zero rows and must stay indexed as
prose — losing their prose rows would be a regression the row counts would hide.

**The load-bearing check, and it is the one that can go wrong quietly: the glob must
reproduce every existing arc label byte-for-byte.** Deriving the arc from the `E\d\d`
prefix alone would map `E10-offsurface-ruling.md` to `E10` and merge it with
`E10-ruling.md` — twelve rulings and seven rulings sharing numbers 1–7, which is a
primary-key collision, not a silent miscount. Prediction: stripping the filename from
`ruling` onward reproduces `E04`, `E08`, `E10`, `E10-offsurface`, `E11`, `E12`, `E15`
exactly, and yields `E08-director-canon` for the canon ruling — a label that never
appears in a row because that file parses to zero.

## P2 — row deltas

| table | predicted delta | reasoning |
|---|---|---|
| `rulings` | **+10 to +22** | 8 numbered, plus E15's lettered sub-rulings — Rulings 1–7 read as prose paragraphs when I saw them, so I expect subs only under Ruling 8, i.e. 2–14 |
| `prose_sections` | **−6 to −14, i.e. it FALLS** | `E15-ruling.md` is currently indexed as prose sections; becoming a structured ruling document removes them |
| `phenomena` | **+0 to +2** | E15's rulings use naming verbs ("is NAMED AS A LAW", "RATIFIED") |
| `fts` | net of the above, **roughly flat to +10** | rulings up, prose down |
| `laws` `experiments` `handoffs` `artifacts` `decisions` | **0** | none of them reads a ruling document |

The signed prediction that matters is `prose_sections` **falling**. If it rises, the
exclusion is not working and the same text is indexed twice under two identities.

## P3 — the seeded set

**Prediction: 14/14 holds, and 0–3 ranks move by one position.**

Named at risk, in advance: **the fifth brush signature**. `E15-ruling.md` Ruling 7
quotes the exact phrase *"dark desaturated crevice fill → Ruling 27d"* as its own
example. That text is already in the corpus as prose, so it already competes — what
changes is its granularity and its title, which gains `E15 Ruling 7 advisor` tokens.
The effect could go either way, which is why it is named rather than signed.

Second at risk: **what a ruling pays values in** and **when the pair was accepted** —
E15's rulings discuss the gate and the acceptance vocabulary. I predict neither
leaves the top 3.

If any question drops out, that is a finding about a self-describing corpus, not a
licence to re-phrase it.

## P4 — `claims` still reads 0 STALE

**Prediction: 0 STALE holds**, and this run is the reword's test.

The mechanism worth stating: before this fix, `experiments/README.md`'s `285 rulings`
landed in UNPARSEABLE for the right reason — *no measurement for E15 ruling*. **This
fix creates that measurement.** Had the row not been reworded, the same line would
have become a false STALE at 285 against 8. The hazard and its closure are being
tested in the same run, which is the only honest order.

Named risk: any *other* cardinal `N rulings` on a non-E15 file whose nearest
preceding arc token is E15. I predict there is none, and the sweep's UNPARSEABLE
bucket falling from 4 to 3 is what would confirm the reword landed.

## P5 — the completeness line

E15's dispatched bound is 1–8. **Prediction: no completeness line for E15**, because
the record carries exactly 8. E04 and E12 keep theirs (29 and 30 against a bound of
28), unchanged and un-widened.

## P6 — the DB commits with this fold

By construction: the builder change alters what the DB contains, so Ruling 4's
session-boundary cadence takes its one ruled exception. Prediction: the DB grows, and
`verify` leg 1 returns byte-identity on two fresh builds as it has every time.

---

## Standards compliance (this file)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | registered against `f963a7a` before the build path was opened; every delta states its reasoning |
| ANDON_AUTHORITY | 2 | P1 names the primary-key collision the naive arc derivation would cause, so it is caught by design rather than by a crash |
| NAMED_COMPENSATORS | 3 | additive file; undo is deleting it |
| DECOMPOSE_BY_SECRETS | 2 | predictions separated by discovery, row deltas, retrieval, the sweep, the gate and the cadence |
| UNCERTAINTY_GATED_HUMANS | 3 | P3 pre-commits to reporting a dropped question as a finding rather than re-phrasing it |
| EXTERNAL_VERIFIER | 2 | P4 states that the fix creates the measurement that would have fired the hazard, so the reword and the fix are tested against each other in one run |
