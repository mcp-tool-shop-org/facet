# E15 handoff 3 — the discovery fix: ruling documents are found, not listed

Executor session, 2026-08-07. Predictions:
[E15-handoff3-predictions.md](E15-handoff3-predictions.md) (`ea356d5`, registered
before the build path was opened). Dispatch: E15 kickoff, Session handoff 3
(Ruling 8b). Built against `f963a7a`.

**The gate passes: byte-identity, zero dangling over 1,093 rows, every count against
the verifier's own greps, 14/14 seeded, exit 0.** `claims` returns **1 STALE**, which
falsifies a prediction and is §5.

---

## 1. The change

`NUMBERED_RULING_FILES` and `AMENDMENT_FILES` are gone. Ruling documents are
discovered by a sorted glob — `^E\d\d-.*ruling.*\.md$` over `docs/experiments/` —
and `verify` prints what it found:

```
[corpus] ruling documents discovered by the sorted glob
  E01-ruling-gate1.md            arc E01                 0 rows — prose only
  E02-ruling-gate1.md            arc E02                 0 rows — prose only
  E04-ruling.md                  arc E04                29 rows
  E06-ruling-gate1.md            arc E06                 0 rows — prose only
  E07-ruling-gate1.md            arc E07                 0 rows — prose only
  E08-director-canon-ruling.md   arc E08-director-canon  0 rows — prose only
  E08-ruling-gate0.md            arc E08                35 rows
  E10-offsurface-ruling.md       arc E10-offsurface      13 rows
  E10-ruling.md                  arc E10                12 rows
  E11-ruling.md                  arc E11                11 rows
  E12-ruling.md                  arc E12               185 rows
  E15-ruling.md                  arc E15                13 rows
  12 documents matched ^E\d\d-.*ruling.*\.md$
```

Determinism is preserved by sorting: the insert order is a pure function of the
filenames, which are in git. The list was explicit *for* determinism, and the sorted
glob buys the same property without the silent-omission cost.

A guard rides beside it: any ruling row whose file the glob does **not** discover
fails the run. That is the inverse check the old construction could not express.

**E15 joins the count leg** — its own grep (8 numbered, 5 lettered), its own sequence
check at the dispatched bound of 1–8, no gaps, and no completeness line because the
record carries exactly 8 (P5 confirmed).

## 2. The check that could have gone wrong quietly

The arc label is derived by stripping the filename from `ruling` onward, **not** from
the leading E-number. Keyed on the E-number, `E10-offsurface-ruling.md` maps to `E10`
and merges with `E10-ruling.md` — twelve rulings and seven rulings colliding on
numbers 1–7, which is a primary-key failure rather than a quiet miscount. Named in
P1 before the code was written; the derivation reproduces every label the hardcoded
list carried, byte for byte:

```
E04 · E08 · E10 · E10-offsurface · E11 · E12 · E15
```

`E08-director-canon` appears in the discovery printout and in no row, because that
document parses to zero — which is the honest way for a pattern-matched file with no
numbered content to behave.

## 3. Prose exclusion is decided by yield, not by name

The glob matches five documents carrying no numbered rulings. Excluding those from
the prose corpus on a *name* match would have deleted their prose rows outright — a
regression no ruling count could show. Exclusion is therefore computed from what each
file actually yielded. Measured after the change, all five keep their prose:

```
E01-ruling-gate1.md 9 · E02 7 · E06 7 · E07 7 · E08-director-canon-ruling.md 7
```

And `E15-ruling.md` reads **13 ruling rows, 0 prose rows** — indexed once, under one
identity.

## 4. Row deltas, measured in isolation

The build's raw numbers move for two reasons at once — the fix, and three documents
this session wrote — so the fix was measured on **one** record by building the prose
corpus with and without the exclusion:

| quantity | delta |
|---|---|
| ruling rows added by `E15-ruling.md` | **+13** (8 numbered, 5 lettered) |
| prose sections removed | **−2** |
| net FTS effect of the fix alone | **+11** |

**P2's prose prediction (−6 to −14) is falsified, and the reason is worth keeping:**
`parse_prose` already skipped `## Ruling N` sections through its `owned_hdr` rule,
even in files outside the structured set. So `E15-ruling.md` was only ever
contributing its preamble and its standards block — two rows. The double-indexing the
exclusion exists to prevent was already prevented by a different mechanism, and the
exclusion is belt-and-braces for the preamble. Worth knowing before anyone prices
that mechanism's removal.

Whole-index totals after the fold, with this report present in the corpus it
describes: rulings **298**, laws 69, experiments 15, handoffs 20, artifacts 451,
phenomena 23, decisions 217, prose sections 1,506 — FTS **2,599**.

## 5. The 285 hazard fired — the prediction is falsified, and the mechanism was right

**`claims` returns 1 STALE:**

```
docs/experiments/README.md:28  claims count 285, record has count 8  [rulings cardinal]
```

P4 predicted **0 STALE**. It is falsified. What is *not* falsified is the mechanism I
named last session — *"this fix creates the measurement that would have fired the
hazard"* — which is exactly what happened.

**The reword did land.** `f963a7a` changed `285 rulings · 69 laws · 217 decisions`
into `Index contents at acceptance: ruling rows 285 · law rows 69 · decision rows
217`, which no phrasing family matches. The row fires on the *parenthetical that
explains the change*, which quotes the removed phrase verbatim:

> *phrased as row counts deliberately — E15 handoff 2 flagged that **"285 rulings"**
> inside this row would read as an arc-E15 count-claim and go falsely STALE once
> E15's own rulings enter the index*

**The note documenting the hazard reproduces the hazard.** This is the same class the
P1 report already recorded at §2, where quoting `j/inpainted.png` as an example of a
phantom path minted that phantom as an artifact row. A sweep that reads text cannot
distinguish a phrase **used** from a phrase **mentioned**.

**Not fixed here, and the reason is the discipline rather than the scope.** A rule
that "a count-claim inside quotation marks is a mention, not an assertion" is
general, cheap, and one I would write the same way whatever document triggered it —
but adding it *after* watching it fire is the retuning move, and the choice is also a
prose question (whether the parenthetical should quote the phrase at all) that
belongs to the seat that owns the record. Both options are on the table and neither
is this seat's to take:

1. rewrite the parenthetical so it does not quote the literal phrase; or
2. add mention-vs-use to the sweep, ruled rather than slipped in.

**My own calibration failure, stated plainly:** I predicted 0 STALE because the
dispatch said the row *"was reworded out of the phrasing family"*, and I predicted
from that sentence instead of checking it. That is this repo's founding law —
an inherited claim is a hypothesis wearing a fact's clothes — and I fell for it in
the one place a prediction is supposed to be my own.

The rest of `claims` is unchanged: **2 AMBIGUOUS** (`29 rulings + the close`, at two
sites, still unresolved by design) and **UNPARSEABLE falls 4 → 3**, which is the half
of P4 that held — the 285 row left that bucket by acquiring a measurement, exactly as
predicted. The three that remain are the "Amendment" overload recorded in handoff 2.

## 6. The seeded set did not move at all

**14/14, and every rank identical to the pre-fix run** — including *the fifth brush
signature*, which P3 named at risk because `E15-ruling.md` Ruling 7 quotes the exact
phrase *"dark desaturated crevice fill"* as its own example.

| question | rank |
|---|---|
| canny values for the beast | 3 |
| which seed resists terms | 2 |
| the galleon's accepted mix | 2 |
| the other eleven | 1 |

P3 predicted 0–3 ranks moving; **0 moved**. The corpus gained 13 ruling rows about
the index itself and the exact-phrase stage still put every ruling above its
commentary — the granularity change (per-ruling rows replacing two prose sections)
did not cost precision.

## 7. The DB commits with this fold — under the ruled exception

The builder change alters what the DB contains: 285 → **298** ruling rows. Ruling 4's
session-boundary cadence takes its one exception, ruled in this dispatch and not
assumed here — a HEAD carrying a builder and a DB that disagree is the two-authorities
hazard in miniature. Leg 1 returns byte-identity on two fresh builds, as it has every
run.

## 8. Predictions, scored

| prediction | outcome |
|---|---|
| P1 — 12 discovered, 5 yielding nothing, arc labels reproduced byte-for-byte | **confirmed on all three**, including the primary-key collision avoided by design rather than by crash |
| P2 — rulings +10 to +22 | **held**: +13 |
| P2 — prose_sections falls 6–14 | **falsified**: falls 2, because `owned_hdr` already prevented most of the double-indexing (§4) |
| P2 — phenomena +0 to +2 | **held**: +1 |
| P3 — 14/14 holds, 0–3 ranks move | **held**, at the strong end: 0 moved |
| P4 — 0 STALE | **FALSIFIED**: 1 STALE, on a quoted mention. The named mechanism was right and the outcome wrong, because I predicted from the dispatch's sentence instead of checking it |
| P4 — UNPARSEABLE falls 4 → 3 | **held** |
| P5 — no completeness line for E15 | **held**: 1–8, no gaps, nothing above the bound |
| P6 — DB grows, byte-identity holds | **held** |

## 9. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | discovery is a pure function of filenames in git; the discovered list prints in every verify transcript; predictions registered at `ea356d5` before the build path was opened |
| ANDON_AUTHORITY | 3 | the four legs re-run and pass; a new guard fails the run on any ruling row from an undiscovered file — the inverse check the old construction could not express; the fired STALE row is reported, not silenced |
| NAMED_COMPENSATORS | 3 | two paths written (builder, DB) and the DB moves *with* the builder under the ruled exception; undo is reverting one fold |
| DECOMPOSE_BY_SECRETS | 3 | discovery knows the naming convention, the parser knows the header conventions, prose exclusion knows only what each file yielded, and the verifier still greps the record for itself |
| UNCERTAINTY_GATED_HUMANS | 3 | §5 hands the advisor two named options and takes neither, because one of them is a prose decision and both would be retuning after the fact |
| EXTERNAL_VERIFIER | 3 | E15's counts are checked by the verifier's own greps against a document the builder now discovers rather than is told about; the seeded key is unchanged and still advisor-authored |
