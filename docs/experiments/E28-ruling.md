# E28 — the advisor's ruling

**Mid-arc ruling on the census halt, 2026-08-09.** Report:
[E28-instrument-census-report.md](E28-instrument-census-report.md). Predictions:
[E28-predictions.md](E28-predictions.md). Dispatch + Amendment 1:
[E28-instrument-census-kickoff.md](E28-instrument-census-kickoff.md). Contract:
[measurement-mcp-spec.md](../specs/measurement-mcp-spec.md). **The arc is not closed** —
task 2 is green-lit below and this document extends when it reports.

**Every load-bearing claim below was re-measured at this seat rather than read.** Where a
ruling rests on the executor's number, it says so and names the check I ran.

---

## Ruling 1 — TASK 0 IS ACCEPTED

T34's fourth leg pins the experiment count against the status table, and it earned its
place before it was finished: it **fired on two genuinely stale live surfaces the dispatch
had not named** (`site-config.ts` read *"Twenty"*, `docs/advisor-kickoff.md` read *27*,
against a table holding 28) — a stronger discharge of E26's gate 2 than any planted
fixture, because the tree at HEAD was the deliberately-stale input. Its own notation test
then caught a real parser defect on first run: French `vingt-six` fell through to its right
half and read as **6** — a confidently wrong number, worse than declining — and hyphenated
pairs are now all-or-nothing.

The dispatch's own enumeration was wrong in the familiar direction: it named README.md's
two sites, which were *already corrected in the dispatch commit*, and missed the two that
were genuinely stale. **The fourth leg exists precisely because hand-enumeration keeps
doing this**; the leg now watches all swept surfaces mechanically.

## Ruling 2 — THE CENSUS IS ACCEPTED AS AN INSTRUMENT

Re-measured here, not inherited:

| claim | my check | result |
|---|---|---|
| the population | — | gate 1 was the executor's, verified three ways; the count is pinned by T41 |
| `__main__` guards 6 · argparse 93 · module-level `parse_args` 88 | independent `Select-String` greps | **6 / 93 / 88**, to the digit |
| the 5 invocable are all one arc's | grep for guard ∧ `add_argument` | **all five are `e10_*`** — F2 confirmed |
| the census reproduces | full re-run to scratch, JSON diff | **totals equal, 0 of 99 rows differ** — *with this arc's report in the corpus*, which live-tests F10's exclusion at a second seat |
| ambiguous judgments | hand-read 4 of 17 docstrings (`e13_thin_inputs`, `e10_offsurface_consumers`, `e14_atlas_anatomy`, `flagged_identity`) | all four correctly not the eight — *"Assembles; proposes nothing"* is an inputs tool, not the curve |
| F5 cell member | grep `tests/` for `e04_bands` | **0 hits** — unanchored, as stated |
| P4's mechanism (T33 names modules) | name extraction on T33 | the per-file table carries **21 lines × 2 = 42 names** — the report's number; my first grep said 7 and was my own defect (quoted-`.py`-only pattern) |
| suite | full run, this seat | **736 passed, 380.26 s, exit 0** |
| gate 4 | `git diff --name-status 1a2e45c..88a8c26 -- tools/` | **`A tools/instrument_census.py`** and nothing else |
| gate 5, left `NOT YET RUN` by the executor | pushed, then `gh run view` | **[`31324613262`](https://github.com/mcp-tool-shop-org/facet/actions/runs/31324613262)**, `88a8c26`, hermetic job, **success** — resolved before written, per the fabricated-citation law |

The instrument's safety refusal deserves its own sentence: axis F **declines to probe** the
88 unguarded files because `python <file> --help` executes a module body before argparse
sees anything, against whatever subjects its constants name. A census that had scored those
files by running them would have been the E23-class accident — an instrument executing arc
scripts against recorded trees to fill in a table cell. The refusal is the correct shape:
`n/a` with the reason, never a silent `false`, and never a run.

## Ruling 3 — THE BOUNDARY (open question 1, discharged against the census)

**The surface is the spec's eight questions. An instrument is ON the surface iff a served
tool invokes it. Directory membership confers nothing.** The census measured the
population; the boundary is the backing map:

| served tool | backing instrument | home | state |
|---|---|---|---|
| `mesh_stats` | `verify/mesh_stats.py` | verify | serving (E27) |
| `mesh_topology` | `diagnostics/e14_topology.py` | diagnostics | task 2: F1 repair, then wrap |
| `reach_ceiling` | `diagnostics/e08_ceiling.py` | diagnostics | serving (E27) |
| `thin_extent_curve` | `diagnostics/e12_thin_curve.py` | diagnostics | task 2: wrap |
| `offsurface_rate` | `diagnostics/e12_offsurface.py` — **bake half** | diagnostics | task 2: wrap; erode/margin half stays an open commission |
| `texel_provenance` | `diagnostics/texel_provenance.py` | diagnostics | serving (E27); task 3 adds largest-component **in the instrument** |
| `anchor_check` | **none exists** | — | commission stands (E27 Ruling 4, census F6); **not this arc** |
| `measure_report` | `verify/gate1_sheet.py` | verify | serving (E27) |

**Everything else stays off the surface**: the 58 `none`, the 17 `ambiguous`, the 3
`no opinion`, and the *unserved siblings* of served instruments (the five other
`reach_ceiling`-shaped camera tools, the nine arc sheet-builders, `e10_offsurface`,
`e12_nonmanifold`). They are the record's arc-evidence instruments, and a cross-subject
measurement product is exactly where they do not belong. A sibling is **named in a payload's
`notes`** where it adds something the served instrument does not (Ruling 4's case); naming
is not serving.

**The entry rule for the future**: a new instrument enters the surface by a ruling plus a
wrap — never by landing in a directory — with the census's mechanical axes as the entry
checks (a flag surface; no module-level subject literal, axis B1 empty; clean under
subprocess invocation) and **the census re-run in the entering commit**, so the diff shows
exactly what changed about the population.

The three `no opinion` rows stay undecided, and that is the honest state: the boundary is
complete without them because it is defined by the backing map, not by exhausting
judgments.

**This discharges open question 1.** The Director adjusts any line of the map in a
sentence, as always.

## Ruling 4 — F7 IS RESOLVED BY THE INSTRUMENTS' OWN TEXT: `e14_topology` BACKS THE TOOL ALONE

I read both instruments at this seat. `e14_topology.py` computes the non-manifold census
itself — `non-manifold(>2) %d (%.4f%%)` in its print, `nonmanifold_edges` /
`nonmanifold_frac` in its JSON — alongside the boundary triplet, the dual shell census, the
nested-wall test and the cross-sections. Its docstring names the division of labour
directly: *"FOUR QUESTIONS, none of which mesh_stats or e12_nonmanifold.py answers between
them"*, and its standards block states its non-manifold arithmetic is *"independent of
e12_nonmanifold.py's and is meant to agree with it."*

`e12_nonmanifold.py` is the other half by design: the same count computed independently,
plus **every non-manifold edge midpoint projected onto the turnaround renders** — a picture,
on a render set the tool *requires* as input. That is evidence for the eye, which is the
Director's channel, not a payload number.

So: **the served `mesh_topology` wraps `e14_topology.py` alone**, after 2a's tie repair.
`e12_nonmanifold.py` is named in the payload `notes` as the independent concentration
picture — the E27 Ruling 7 pattern, name the gap's instrument rather than compute in the
wrapper. **No agreement test leg is commissioned**: E14 ran both instruments on the same
subjects and their agreement is already in the record; a synthetic agreement leg would add
a second instrument to the wrap's test scope for no new information about the wrap.

## Ruling 5 — F3 IS DISPOSED: THE MAP SPANS HOMES BY CONSTRUCTION, AND THE CENSUS EXTENDS TO MEET IT

The executor's framing is exactly right and the fix has two halves. The *ruling* half is
Ruling 3's principle — the boundary was never a fact about `tools/diagnostics/`, so the two
verify-homed tools were never at risk of exclusion. The *measurement* half is commissioned:
**task 2-pre extends the census to `tools/verify/` (8 files)** — parameterize the
directory, keep the diagnostics default, add the 8 axis-G judgments as a proposal (the
missing-judgment ANDON keeps firing), extend T41's population pin **deliberately in the
same commit**, re-emit both outputs. Then the backing map rests on measurement over both
homes, and the two serving instruments' own hygiene (subject literals, anchoring) is on the
record instead of assumed.

## Ruling 6 — F5 IS CORRECTED IN PLACE, AND THE CELL IS A WATCH-LIST, NOT A WORK QUEUE

Two defects in the report's F5 prose, both found by diffing it against the committed
instrument output, both corrected in the report with a dated note:

- `e12_offsurface` is cited **14** (raw 17), not 16 — **a tie with `e08_ceiling`** for
  most-cited, not the sole leader; `texel_provenance` is **11** (raw 13), not 12. The
  prose numbers were interim reads from a corpus state containing the arc's uncommitted
  drafts — the same contamination class F10 caught, surfacing in prose the gate cannot
  reach.
- "The 14 that are genuinely unanchored" carries an **unstated threshold**: it is the
  cited-**≥ 3** slice of the full cited>0 ∧ unanchored cell, which holds **36 files** in
  the committed JSON. The 14 names and their per-file counts match the committed output
  exactly under that threshold — the list is right, the denominator was unnamed. *Name the
  denominator*, in a report about measuring things, is this repo's oldest lesson refusing
  to stay learned.

Disposition of the cell: **it is the standing watch-list, not a commission.** The anchor
obligation rides any future *edit* to a member — CLAUDE.md's closed-ruling law already
carries the mechanism (*prove the edit non-perturbing, or carry an anchor reproducing the
cited number, in the commit that makes the edit*). Anchoring 36 arc-evidence files nobody
is editing would be coverage theater. F4's 23 uncited files: noted, no action — an
instrument nothing cites constrains nothing. F6 (`anchor_check` has no implementation, five
nearest all ambiguous): the commission stands exactly as E27 left it, unscoped, not this
arc.

## Ruling 7 — THE FIRED GATE IS RATIFIED, AND THE SELF-POPULATION LAW IS FOLDED

`test_t41_axis_d_is_idempotent_across_runs` fired on the closing run — 76 → 99, 51 rows —
because the report names the files the census found, and the report is a corpus file. The
executor's disposition is ratified on every point: the four alternatives are named and
rejected in writing; the adopted exclusion is the rule *already in the instrument before
the gate fired* (`SELF_OUTPUTS`, the same sentence: a derived artifact of this measurement
is not evidence about its subject), applied to a member of its class the first pass missed;
and it passes the retune test — **the headline does not move** (76 before the report
existed, 76 with the exclusion), with the contaminated 99 riding beside as `cited_raw`
rather than discarded. I re-ran the census at this seat with the report in the corpus:
**totals equal, zero rows differ.** The exclusion holds live.

One nuance recorded so a future seat meets it deliberately: the `E28-` prefix exclusion is
**permanent**, so this arc's ruling and report will never count as axis-D citations even
after the arc closes. That is correct — their citations of these instruments are *derived
from the census*, which is exactly the circularity excluded — and any future document that
cites an instrument for its own reasons will do so outside the `E28-` prefix.

**Folded to CLAUDE.md as law**: *an instrument that lives inside its own population must be
checked against itself on every axis, each time — and one clean check is not clearance.*
Four self-references this arc; three moved a number; three were caught by a check firing
rather than by reading. F9's fixture perturbation (44 → 45 by the test existing) and F8's
implementation-vs-registered-definition defect are ratified with the same sentence the
executor used, which is the right one: **a correction adopted mid-arc is safe when it makes
your own miss larger.** Both did.

## Ruling 8 — THE PREDICTION RECORD: THE SIXTH UNIT MISS EARNS THE CONJUNCTION LAW

P1 predicted 60 invocable of 99; measured **5**. The pre-registered definition was a
three-clause conjunction, the reasoning was about one clause (the flag surface, which
measured **93**, *above* band), and the join is governed by the rarest clause (the
`__main__` guard, **6**). The definition was not retuned after the fact, which is why the
miss is legible at all. **Folded to CLAUDE.md**: *a composite definition is governed by its
rarest clause — predict each clause separately, then the join.*

The rest of the record: P4 missed opposite (12 predicted, 46 measured) having **named the
right axis of uncertainty and guessed the wrong side** — T33's per-file table names 42
modules explicitly, verified here; no new law, the unit family already covers it. P2's
secondary (B2 − B1 = 0) landed *with its mechanism* — a straight-line script has no
function bodies for a literal to hide in — which is the same fact as P1's miss from another
angle, and predictions that cohere like that are the point of writing them. P7 stands
untouched behind the halt, which is correct: its discharge is task 2a's deliverable, and
the executor's own note — *"this prediction is the one I am least entitled to"* — is the
right posture toward an inherited conclusion, including one inherited from my ruling.

**The executor's seat: exceptional, and the calibration note is written for the next
dispatch rather than for praise.** Two defects were its own (F8, F9); both were self-caught
by its own instruments, both disclosed with the error's direction stated, both corrected in
the direction that worsened its own score. The predictions file's per-row blindness
declarations and the post-freeze leakage amendment (E25's 43, disclosed, no number moved)
are the house standard now. When this executor declines to do something — judge three
files, build `anchor_check`, retune P1 — that is signal.

## Ruling 9 — TASK 2 IS GREEN-LIT, AS AMENDED

[Kickoff Amendment 1](E28-instrument-census-kickoff.md) carries the scope, appended before
any task-2 work was picked up: **2-pre** (the verify/ census extension, Ruling 5) → **2a**
(the tie repair, with the proof obligation discharged by exhaustive comparison over the
recorded subjects plus a randomized sweep — not by reading the diff, and not by citing
E27 Ruling 3 or P7) → **2b** (three wraps; `mesh_topology` per Ruling 4; `offsurface_rate`
bake half only, gap named in `notes`) → **task 3** unchanged and droppable. T-numbers:
T42+. Everything else in the dispatch stands as written.

---

## Ruling 10 — THE EIGHTH TOOL IS COMMISSIONED, AND ITS HONEST SHAPE IS COMPARE-ONLY

**Appended 2026-08-09, same day, at the Director's word on the 7-of-8 question:** *"I'd
like at least 8 tools, if it could be done honestly. I want control over the art, and the
proper measurements allow for that control. Your call, though, as a tool that's forced is
worse than no tool at all."*

**Ruled: build it. The honesty test passes on three legs, and the shape that passes is
narrower than the spec's sentence implies — that narrowing is the ruling.**

**1. The job is real and its first consumer is already scheduled.** The polish arc's entry
clause — his own binding words at [E14 Ruling 35](E14-ruling.md) — opens every lane with a
per-profile anchor gate: recorded artifacts replayed against the citable tree before any
polish work. That is this tool's question, asked four times before the next arc can start.
And the record carries three instances of the measurement being needed and done by hand:
**two false halts from byte-hashes on pixel-identical renders** (the CLAUDE.md law: file
bytes are not pixel values), and the **hardware-boundary anchor**, where the number (ΔE
0.84 against a pre-registered 1.07 floor) decided less than the residual's *shape* did —
*"uniform across every structure, which is what two float kernels look like."*

**2. An honest decomposition exists: the tool COMPARES; the caller REPLAYS.** The
anchored-regression pattern has two halves. The replay half is a heterogeneous recorded
command per artifact — Blender invocations, projection scripts, brush steps — and a tool
that executes arbitrary recorded recipes is a shell with a safety surface, the exact thing
the census's axis F refused at instrument scale (*probing an unguarded file would execute
it against whatever its constants name*). The comparison half is one question asked
identically every time: **is this re-production the recorded output, and if not, what is
the difference's shape?** That half is instrument-shaped, it is the part every anchor in
this repo currently re-implements ad hoc, and it is what `anchor_check` serves. The payload
states `replay: caller-supplied` so nobody later mistakes the boundary for an omission.

**3. It carries existing laws rather than inventing metrics.** Two-tier identity (bytes,
then pixels — byte-identity labelled gate-eligible **only for artifacts whose bytes are the
contract**, the E08-armB/E04-step-0 class, because encoder metadata moves it on renders);
differing-pixel count **and largest connected component** (the two-thresholds law); residual
magnitude percentiles + ΔE beside them; and shape reported as a **coarse grid of
differing-pixel fractions** — the payload carries the grid, the reader does the reducing,
because collapsing "concentrated vs uniform" to one invented score is where forcing would
begin. Refusals where the comparison is undefined: dimension mismatch, pixel tier on a
non-image — structured, naming what was asked and what exists.

**The bound, in his own words: a tool that's forced is worse than no tool at all.** If the
build reaches for an unprincipled statistic or a magic threshold to fill a payload field,
the executor ships the honest subset or refuses the field — a refusal there is the
specification working, and this ruling says so in advance.

Scope lands as **task 2c** ([kickoff Amendment 2](E28-instrument-census-kickoff.md)): a new
instrument `tools/verify/anchor_compare.py` (subject-independent, so it lives with
`mesh_stats` and `gate1_sheet` in the verify home), wrapped as the served `anchor_check`,
tests riding both commits — including the fixture this repo has owed itself twice:
**a pixel-identical, byte-different PNG pair**, pinning the false-halt class as a can-fail
leg. With 2c, the server reaches **8 of 8 honestly**, and the 7-of-8 question this
document flagged is dissolved rather than answered.

---

## What is NOT ruled here

- **The arc's close** — this document extends when task 2 reports.
- **The erode/margin half of `offsurface_rate`** — open commission, unscoped, unchanged.
- **Whether `facet-measure` ships** — E27 Ruling 8's default holds: not before the polish
  arc has exercised it.
- **The polish arc** — still gated on the four MCP *products* built and test-verified
  (the record index is; the measurement server completes at 2c; `comfy-preflight` awaits
  the Director's repo creation; `fixture-lint` is sdlab-side).

## The advisor's record, this ruling

My first T33 check returned **7** against the report's 42 — a quoted-`.py`-only grep, my
own defect, caught by running a second pattern before doubting the report. *Before trusting
a reading, ask what a passing value would have looked like* — a 7 from a pattern that
cannot see unquoted names was never a refutation. The report's F5 prose defects (Ruling 6)
were found by the same discipline applied in the other direction: diff the prose against
the committed instrument output before adopting either.
