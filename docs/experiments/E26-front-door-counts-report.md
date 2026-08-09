# E26 — the counts nothing watches: report

**Executor session, 2026-08-09.** Spec:
[E26-front-door-counts-kickoff.md](E26-front-door-counts-kickoff.md). Predictions committed
blind as the session's first act: [E26-predictions.md](E26-predictions.md), commit `1b60478`.

Halts here. The advisor rules at `E26-ruling.md`.

---

## The measurement, first

| quantity | at HEAD (`3ce6a39`) | after this arc |
|---|---|---|
| full tier, `pytest --collect-only` | **384** | **423** |
| hermetic tier, `-m "not artifacts"` | **376** | **415** |
| tier gap | 8 | 8 |
| current-state sites stating a count, repo-wide | 23 | 23 |
| of those, **wrong** | **16** | 0 |

The 39 new tests are this arc's own: T34 adds 34, T05 adds 5.

---

## 1. The surfaces, enumerated rather than inherited

The dispatch listed six surface groups and said *verify, do not inherit*. Verified by
scanning every tracked text file outside `tests/`, `tools/` and `docs/experiments/`.

**The dispatch's enumeration is arithmetically right and structurally wrong**, and it is
missing one surface.

### 1a. What the enumerated set actually contains

| surface | dispatch says | measured | numbers |
|---|---|---|---|
| `README.md` | two sites | two sites — L160–161 (bullet), L259–260 (Requirements) | 4 |
| `SHIP_GATE.md` | "item D's verify-script line + its lineage" | **ONE physical line, L61**, carrying **four** current-state clauses and **eight** historical pairs | 4 current + ~20 historical |
| `site/src/site-config.ts` | the card | L116, one site | 2 |
| `…handbook/getting-started.md` | two numbers | L26 (comment), L29 (prose) | 3 — the third is the tier gap |
| `…handbook/reference.md` | one number | L61 | 1 |
| `README.{ja,zh,es,fr,hi,it,pt-BR}.md` | two each | two each, confirmed | 28 |

Counted the dispatch's way — **claim sites** — the enumerated set is **22**, exactly as
predicted, because `SHIP_GATE`'s current clause and its lineage were counted as two.

Counted as **pinnable numeric assertions**, the same set is **19 on the English surfaces
plus 28 in translation**, because three of the enumerated "sites" carry two numbers and
`SHIP_GATE`'s single line carries four current-state values, not two:

```
SHIP_GATE.md:61   "runs the full **423-test** suite"          <- current
                  "runs the **415** hermetic tests"           <- current
                  "... then 370/362, then 384/376, now 423/415 ..."  <- current, INSIDE the lineage
                  "lineage 27 -> ... -> 384 -> 423."          <- current, the terminal element
                  "this line read 32/24, then 92/84, ... 370/362"   <- 8 historical pairs, SAME LINE
```

This is E23's unit law firing again on a fresh instance. *Surfaces carrying the claim*
counts sites; *what a test must pin* counts numbers; and the two differ by more than a
constant, because one line holds four of one and none of the other.

### 1b. One surface the enumeration does not name

**`docs/advisor-kickoff.md`** carries two current-state test-count sites and both were
stale:

```
L43   "1. RE-COUNT   pytest --collect-only  -> currently 248 total / 240 hermetic"
L97   "**THE SUITE: 248 tests, 240 hermetic**, green at two seats and CI."
```

It is not a judgement call that these are current-state: **the repo's own classifier
already says so.** `facet_index.classify_document` treats `docs/advisor-kickoff.md` as
current-state above its supersession banner, and it has no banner, so the whole file is
current-state by the rule that was already in the tree.

### 1c. What was wrong at HEAD

**16 current-state sites**, carrying **32 wrong numbers**:

| surface | sites | stated | truth |
|---|---|---|---|
| seven translations × 2 sites | 14 | 370 / 362 | 384 / 376 |
| `docs/advisor-kickoff.md` L43, L97 | 2 | 248 / 240 | 384 / 376 |

Every English front-door surface was correct at HEAD. The translations were stale by one
release (`370/362` is the v0.3.0 reading); the advisor kickoff was stale by three
(`248/240` predates E22).

### 1d. Surfaces that carry test counts but are historical

Found and left alone: `CHANGELOG.md` (7 shaped hits below the released boundary),
`SCORECARD.md` (2), `.github/release-notes-v0.1.0.md`, `-v0.2.0.md`, `-v0.3.0.md`.
`SECURITY.md` carries none.

---

## 2. Half A — T34

`tests/test_t34_front_door_counts.py`, **34 tests**. Truth is
`pytest --collect-only` in a subprocess, both tiers, parsed from pytest's own summary
line; an unparseable summary raises rather than substituting a guess.

Three legs, because a count can go wrong three ways:

1. **PINS** — 16 anchors over 6 English files, capturing 19 numbers. An anchor that
   matches ≠ 1 time fails as loudly as one reading a wrong number, so a rewritten
   sentence must be re-pinned deliberately.
2. **DIGITS** — each of the 8 READMEs carries the full count twice and the hermetic
   count twice. Language-agnostic; this is the leg that fires on a stale translation,
   and it fires by finding **zero** occurrences.
3. **SWEEP** — every test-count-shaped number on a declared surface must be consumed by
   a pin or sit inside a declared historical region. Otherwise a *new* site exists that
   nothing watches — the failure `SHIP_GATE` item D already records happening at the
   v0.2.0 seat, where the outgoing handoff named four surfaces and missed `SHIP_GATE`
   itself.

### 2a. The matcher was rewritten, and the first version's census is the reason

The first matcher was **proximity-shaped**: a 2–4 digit number within ±90 characters of a
test-word in any of eight languages. Its census over the whole front door:

```
45 hits    29  the stale translation + advisor-kickoff sites   (real)
            1  "T29, 30 tests"                                 (real, a PER-FILE count)
           15  not test counts at all
                 RTX 5090 · a 57-gate-site sentence · four ISO date years
                 · six E/T/A identifiers · limit=999 · "Ruling 35"
 1 MISS    README.fr.md:99 - French spells it "hermetiques", which no
           spelling of herm[e]tic matches
```

A wider window would have found the French site and doubled the false positives. So the
matcher is **phrase-shaped** instead — a number *immediately followed* by
`tests|passing|hermetic|total|collected|deselected|it deselects` — with ISO dates and
letter-prefixed identifiers excluded structurally rather than by threshold.

**And the translations are not swept at all.** Six of the seven false positives were in
them, and no phrase list survives seven languages a generator rewrites. They are covered
by the digits leg, which is what the dispatch specified. This is a **declared boundary**:
a brand-new test-count site invented inside a translation is watched by nothing here.

Final accounting on the swept set: **16 pin anchors matched, 10 historical hits absorbed,
1 declared-not-pinned, 0 unaccounted.**

### 2b. The one hit deliberately not pinned

`SHIP_GATE.md:42` — *"T29, 30 tests"*. A **per-test-file** count, not the suite count. It
is a second class of test-count claim on the front door; E26 pins the suite, so this is
named in `DECLARED_NOT_PINNED` with its reason rather than silently swept up.
`test_t34_every_declared_exemption_is_real` fails if the exemption ever stops matching.

---

## 3. Half B — the widened sweep

`record_markdown()` is **AST-identical** before and after (`ast.dump` SHA `1581685c…` both
sides). The sweep reads a new `sweep_markdown()` — a strict superset.

```
record_markdown   256 files
sweep_markdown    266 files      +10:
     CHANGELOG.md  SHIP_GATE.md  SCORECARD.md  SECURITY.md
     site/src/content/docs/handbook/{getting-started,how-this-repo-is-run,
                                     index,profiles,reference,subjects}.md
```

### 3a. What the widening produced — measured on one corpus, both sweep versions

| | before | after |
|---|---|---|
| claim rows | 37 | **41** |
| **STALE** | **0** | **0** |
| AMBIGUOUS | 2 | 3 |
| UNPARSEABLE | 11 | **14** |

**Zero new STALE rows.** Disposition of every new row:

| new row | disposition |
|---|---|
| `site/…/handbook/subjects.md:18` — amendments cardinal 35 = 35 | **ok.** Agrees with `docs/handbook/subjects.md:9`, so the site sync is current |
| `site/…/handbook/subjects.md:68` — rulings range max 30 = 30 | **ok.** Agrees with its source |
| `site/…/handbook/subjects.md:242` — rulings range max 35 = 35 | **ok.** Agrees with its source |
| `site/…/handbook/subjects.md:40` — "29 rulings + the close" | **AMBIGUOUS**, same as its source at `docs/handbook/subjects.md:31`. The modifier is unresolvable by design |
| `CHANGELOG.md:281` "29 rulings" | **UNPARSEABLE** — *no arc attributable on this line* |
| `CHANGELOG.md:284` "Rulings 1–30" | **UNPARSEABLE** — same |
| `CHANGELOG.md:287` "Rulings 1–35" | **UNPARSEABLE** — same |

### 3b. The widening reached CHANGELOG and could not read it

The three CHANGELOG claims arrive but **none of them is checked**. The sweep attributes an
arc by finding the nearest `E\d\d` *on the same line*, and the changelog wraps:

```
- **The galleon** — accepted 2026-08-05 ([E04-ruling.md](docs/experiments/E04-ruling.md),
  29 rulings). The first non-character subject; ...
   ^ the claim is on the continuation line; the arc is on the line above
```

Extending arc attribution across lines would change attribution for **every file already
swept**, so it is out of Half B's scope and is not attempted. Reported.

### 3c. Three of the four named files contribute nothing

`SHIP_GATE.md`, `SCORECARD.md` and `SECURITY.md` produced **zero rows** — they carry no
ruling / handoff / amendment / experiment claim in any family's phrasing. The widening's
entire yield is the site-handbook mirror plus three unreadable CHANGELOG lines. Their
classifications are declared anyway, because a swept-but-unclassified file can never
produce a STALE row and is watched in appearance only
(`test_t05_every_widened_surface_is_classified`).

### 3d. The current-versus-historical rule, stated

- `CHANGELOG.md` — **split at the first `## [x.y.z]` heading** (L18). Above it is
  `## [Unreleased]`, which is shaped like a released entry and dated like the present, so
  a count there is a current-state claim; from L18 down, an entry states what a version
  shipped and is correct forever.
- `SHIP_GATE.md` — current-state (a live gate document).
- `SECURITY.md` — current-state (a published policy about the tree as it is).
- `SCORECARD.md` — historical (before/after treatment record; its counts are the state at
  treatment entry).
- `site/src/content/docs/` — current-state, joining `docs/handbook/`.

---

## 4. Gates

| gate | verdict | evidence |
|---|---|---|
| 1. suite green before and after, artifacts tier | **PASS** | baseline measured **384**, not the dispatch's stated 384 by luck — same number. After: **423 passed, 0 failed** in 265.60 s on a clean `git worktree` at HEAD + this arc's 17 files, artifacts tier live |
| 2. Half A FAILS on a stale surface, passes at HEAD | **PASS, strong form** | T34 run against HEAD's own unedited surfaces: **25 failed / 9 passed**, and the failure kinds are **50 × AssertionError, 0 × AttributeError / NameError / ImportError**. Every message names a site: *"README.md:160 :: the bullet, full — states full 384, the collector reports 418"*. Also kept runnable in-harness: `test_t34_a_stale_surface_fails_the_pin_leg`, `…_a_stale_translation_fails_the_digits_leg`, `…_a_new_unwatched_site_fails_the_sweep`, each of which first asserts the unmutated mirror passes |
| 3. does not fire on a historical count | **PASS** | 10 shaped hits absorbed by declared historical regions — `CHANGELOG` 7, `SCORECARD` 2, `release-notes-v0.1.0` 1 — with 0 unaccounted. `test_t34_the_sweep_does_not_fire_on_a_historical_count` inserts the same sentence twice: inside a released entry it does **not** fire; above the boundary it **does** |
| 4. `record_markdown()` unchanged, four legs pass | **PASS** | AST hash `1581685c309faedd` identical both sides. Build rows identical (677 / 225 / 26 / 3985 / 31 / 77 / 28 / 2310 / 611). `verify` **19 / 19, all four legs**, before *and* after, on scratch `--db` |
| 5. CI green, both dependency scanners | **NOT YET RUN** — see §7 | written as `NOT YET RUN` rather than with a plausible run id beside a verdict |
| 6. no edit to anything E25 owns | **PASS** | see §5 |

---

## 5. E25 coordination — the disjointness that held, and the one that did not

**Files: disjoint, as the dispatch verified.** Nothing this arc edited is E25's. Its
`tools/diagnostics/*` (43 files), `tools/verify/gate0_sheet.py`,
`tests/test_t31_route_gates.py` and `tests/test_t33_diagnostics_gates.py` are untouched;
every `git add` was file-specific.

**The quantity: NOT disjoint, and it collided mid-session.**

E25 landed `tests/test_t33_diagnostics_gates.py` — **225 tests** — into this shared
working copy while this arc was running. The live tree's collection jumped to **643 / 635**
mid-measurement.

That is not a git conflict and no merge would have caught it. The dispatch's disjointness
table is drawn over **files**, and both arcs are disjoint on files while moving the **same
number**. So every measurement in this report is taken against a **clean `git worktree` at
HEAD plus this arc's own 17 files**, which is the state this arc's commit produces.

**Consequence, stated plainly:** the surfaces are pinned at **423 / 415**. When E25 commits
T33, the collected count becomes **643 / 635** and **T34 will fail on their commit** until
the surfaces move with it. That is the instrument working — the arc was commissioned so a
count cannot move without something noticing, and the first thing it noticed was a live
drift caused by a parallel session. Whichever arc commits second owns the surface update.

**Defect found in E25's files: none.** Their tests were not run in isolation by this seat;
T33 appears green in the shared-tree collection but grading it is not this seat's job.

---

## 6. Findings

**F1 — the enumeration's unit split, again.** A hand-written surface list counts *sites*;
a test pins *numbers*; and `SHIP_GATE.md:61` holds four current-state values and eight
historical pairs in one line, so no line-scoped or file-scoped current/historical rule can
work there. Only spans separate them. This is the fourth instance in the repo of the unit
being the defect rather than the work.

**F2 — a surface the dispatch's list did not have, found by scanning.**
`docs/advisor-kickoff.md` was stale by three releases and is classified current-state by
the repo's *own existing classifier*. The list was not wrong through carelessness — it was
written by hand, and `SHIP_GATE` item D already records a hand-written surface list missing
a surface at the previous release seat. That is now two instances of the same failure, and
it is the argument for the sweep leg rather than for a better list.

**F3 — the lineage is pinned but not discoverable.** T34 pins `SHIP_GATE`'s `now N/M` pair
and its lineage terminal by explicit anchor. The sweep's shaped matcher sees only **2** of
the **22** numbers in that line, because the lineage writes `32/24` and `27 → 32` and the
matcher requires a claim word immediately after the digits. **A new current-state claim
written in `N/M` or `N → M` or `N new tests` form would not be discovered.** Today every
such form sits inside a declared-historical region, so nothing is currently missed. Not
widened after seeing this census — reported for the ruling instead, with the concrete
risk: the lineage is *extended* every time the count moves, and nothing checks that the
previous reading was appended rather than overwritten.

**F4 — the widening reached the changelog and cannot read it** (§3b). Three claims arrive
UNPARSEABLE because arc attribution is line-scoped and the changelog wraps. The widening
delivers less than its file count suggests.

**F5 — three of Half B's four named files carry no family claim at all** (§3c). The
measured yield of the whole widening is one mirrored file's three rows — which do
confirm the `docs/handbook` → `site/` sync is current, a check nothing previously made.

**F6 — a second class of test-count claim exists on the front door**: per-test-file counts
(`T29, 30 tests`; `T30 … 27 cases`; `T31 … 95 cases`). One is on a current-state surface
and is deliberately unpinned (§2b). Whether that class deserves pinning is a scope
question for the ruling.

**F7 — the self-reference is real and it bites more than once.** `--collect-only` counts
T34's own tests, so writing the test moved the number the test pins: 384 → 417 → 418 → 423
across three passes as tests were added to T34 and then to T05. The surfaces had to be
rewritten each time. There is no way to design around it; the discipline is to freeze the
test file, measure once, then write the surfaces.

**F9 — this report is swept by the instrument it reports on.** Quoting the CHANGELOG's
claim text in §3a adds **5 UNPARSEABLE rows** naming this file (14 → 19), each reading
*"no measurement for E26 ruling"*, because the nearest arc resolves to E26 and
`E26-ruling.md` does not exist yet. It is the same self-reference `claims()` already
handles for E15 by skipping `E15-*` documents by filename. Reported rather than fixed: a
second filename skip is a decision about the sweep's contract, and the rows are
UNPARSEABLE, never STALE, so nothing is misreported. **They resolve on their own the
moment the ruling lands.**

**F8 — the translations were updated by digit substitution, not regenerated.** `370 → 423`
and `362 → 415` as standalone tokens, 2 occurrences each, asserted before and after per
file. A full `translate-all.mjs` pass was not run: the release-ordering law puts
translations before a tag, no tag is in scope here, and regenerating seven files would
have produced a prose diff this arc cannot grade. **Whether a regeneration is owed at the
next release seat is a ruling question**, not one this seat settled.

---

## 7. What has not run

**CI.** `.github/workflows/ci.yml` is paths-gated and this arc touches `tests/**` and
`tools/**`, so it will trigger on push. It has **not run at the time of writing** and no
run id exists. Written as `NOT YET RUN` per the law that a report may not contain a
placeholder shaped like evidence.

Two CI-specific risks, named in advance: T34 spawns two `pytest --collect-only`
subprocesses, which CI has never done before; and the digits leg reads all eight READMEs
as UTF-8, which is unremarkable but is the first test to do it.

---

## 8. Predictions, scored

Blindness as disclosed in [E26-predictions.md](E26-predictions.md). **SEEDED** rows are
scored but carry no calibration weight and are marked so.

| # | prediction | point | measured | verdict |
|---|---|---|---|---|
| P1 | sites on the enumerated set | 22 | **22** as sites; **19 + 28 numbers** | **HIT (seeded), composition MISS** |
| P2 | additional surfaces carrying a current-state claim | 1 | **1** — `docs/advisor-kickoff.md` | **HIT on count, MISS on identity** |
| P3 | full tier at HEAD | 384 | **384** | HIT (seeded, worthless) |
| P4 | tier gap → base | 8 → 376 | **8 → 376** | **HIT** (seeded from a stale memory line, and the gap had not moved) |
| P5 | any current claim wrong; how many sites | YES, 14 | **YES, 16** | **mechanism HIT, count MISS** |
| P6 | historical sites Half A must not fire on | 4 | **10** | **MISS** (top edge of the 2–10 interval) |
| P7 | does Half A's test move the number it pins | YES | **YES, three times** | **HIT** |
| P8 | tests T34 adds | 8 | **34** (39 for the arc) | **MISS, badly** |
| P9 | new STALE rows from Half B | 5 | **0** | **MISS** |
| P10 | verify legs before and after | 19/19 both | **19/19 both** | HIT (seeded) |
| P11 | is the current/historical rule ambiguous, and where | YES — at `CHANGELOG` Unreleased | **YES — at `SHIP_GATE.md:61`** | **direction HIT, location MISS** |

**Score on the seven blind rows: 2 clean hits (P7, and P2's count), 2 partial (P5, P11),
3 clean misses (P6, P8, P9).**

### What the misses teach

**P8 — 8 predicted, 34 measured.** The prediction reasoned about *legs*: "one per surface
group, plus two." The instrument counts **parametrized cases**. Sixteen pin anchors and
eight READMEs are 24 collected tests from two functions. This is the E23 unit law a third
time in one session: I predicted the number of *things I would write* and measured the
number of *tests pytest collects*, and parametrization is exactly the transform between
them. A prediction about a test count must be made in the collector's unit.

**P9 — 5 predicted, 0 measured.** The reasoning was sound (repo-wide totals move, per-arc
cardinals do not) and the answer was still wrong, because it assumed the widened files
*contain* the moving families. Three of the four contain no family claim at all, and the
one file that does could not be parsed. **I predicted the density of a population without
checking it was there** — E22's law, which the dispatch quoted at me, and I applied it to
P1 and not to P9.

**P6 — 4 predicted, 10 measured.** Predicted "three CHANGELOG entries plus SHIP_GATE's
lineage" as *sites*; measured as *shaped hits the test must not fire on*, which is the
unit that matters. CHANGELOG alone carries 7.

**P11 — right that a rule would be ambiguous, wrong about where.** `## [Unreleased]` reads
"Nothing yet." and carries no count at all, so the case I predicted does not exist today.
The real ambiguity was one I had no way to see without opening the file: a single line
mixing four current claims with eight historical ones.

---

## 9. Tests added, and what rides this commit

| file | change | tests |
|---|---|---|
| `tests/test_t34_front_door_counts.py` | **new** — Half A entire | +34 |
| `tests/test_t05_claims_sweep.py` | Half B: superset property, the index's non-reach, the CHANGELOG split, classification coverage, and the fts-rows check; the synthetic fixture now patches `sweep_markdown` | +5 |
| `tests/test_t24_index_parsers.py` | `…an_unlisted_document_is_reported_not_assigned` used `SCORECARD.md` as its example of an unlisted file; Half B classified it, so the example moved to `docs/arc-history.md`, which is still unlisted. **The property under test is unchanged and the file count is unchanged** | 0 |

Four of T34's own tests exist only to prove the other legs can fail, each first asserting
that the unmutated mirror passes — a check that cannot fail is not a check.

---

## 10. Files changed

```
tools/facet_index.py                                    sweep_markdown(), classification
tests/test_t34_front_door_counts.py                     new
tests/test_t05_claims_sweep.py                          Half B legs
tests/test_t24_index_parsers.py                         example repointed
README.md  README.{ja,zh,es,fr,hi,it,pt-BR}.md          384/376 -> 423/415
SHIP_GATE.md                                            item D, 4 clauses + lineage extended
docs/advisor-kickoff.md                                 248/240 -> 423/415
site/src/site-config.ts                                 the card
site/src/content/docs/handbook/getting-started.md       comment + prose
site/src/content/docs/handbook/reference.md             comment
```

`CHANGELOG.md` deliberately **not** touched — the release is out of scope and the
`[Unreleased]` block is the advisor's fold.

---

## 11. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every number here is reproducible from a named command on a named tree; the clean-worktree harness is stated so the 643/635 contamination cannot silently enter a later reading |
| ANDON_AUTHORITY | 3 | six gates run; gate 5 reported `NOT YET RUN` rather than assumed; the first matcher's census halted its own design rather than being tuned |
| NAMED_COMPENSATORS | 3 | every change is a tracked file; `git revert` is the undo; the scratch worktree was created and removed; no recorded tree touched |
| DECOMPOSE_BY_SECRETS | 3 | Half A's truth is `pytest`, Half B's is the index; they share no code and `record_markdown()` is AST-identical, which is the decomposition made checkable |
| UNCERTAINTY_GATED_HUMANS | 3 | eight findings routed to the ruling rather than decided here: the matcher's form-blindness (F3), the per-file count class (F6), the translation regeneration (F8), the changelog's line-scoped attribution (F4) |
| EXTERNAL_VERIFIER | 2 | the verifier is `pytest --collect-only` in a subprocess and the index's four legs, neither of which this seat can talk past. skip: no cross-family model; every outcome is an integer comparison |

---

**Halts here.** Nothing is judged good. The advisor rules at `E26-ruling.md`.
