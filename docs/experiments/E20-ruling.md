# E20 — advisor rulings (2026-08-08; the arc's end ruling lands here later)

Evidence — what this seat OPENED: the gate-halt file in full
([E20-gate-halt.md](E20-gate-halt.md), through its §8), the blind predictions
([E20-predictions.md](E20-predictions.md), 20 rows, blindness disclosed per row),
the copy's live state at this fold (E18's D2 slice STAGED — the fixture builder
and T2's hermetic twin in the index, uncommitted; E19 at Phase 2, `site/` and the
Pages workflow untracked), and the two E20 commits' contents.

## Ruling 1 — the gate-park is RATIFIED; the Director's dispositions govern (2026-08-08)

The session fired its own sequencing gate on the first check, measured all three
legs rather than asserting them (the tree growing between its own listings;
`conftest.py` clean → modified 65 seconds before the second observation; the
collision becoming record when E18's `12f6381` modified the exact named file),
corrected its own Leg 1 **in place with a dated addendum** while the tree moved
under it, wrote nothing into the shared lane, and delivered everything that
collides with nothing: the blind predictions, the scratch-DB ritual, the guard
census, the coverage baseline. The halt-file-path deviation
(`E20-gate-halt.md`, not the dispatched report path) is ratified with its named
precedent — the dispatched path is specified to carry a coverage table, and no
coverage exists. The Director's §8 dispositions are the governing word: E20
waits for E18's halt; the partial run and the worktree were rightly declined
(a partial run's safety would have rested on a property of the current unit
list, not on the gate).

## Ruling 2 — `tests/fixtures/` authorship is RULED: E18 authors the pattern; E20 extends it (§8's condition 2, SATISFIED) (2026-08-08)

**D2 was always E18's dispatched deliverable, and E18 is landing it as ruled** —
its D2 slice (the fixture builder plus T2's hermetic twin) is staged in this
working copy at this fold. The ruling closes the race by assignment: **E18
authors `tests/fixtures/` and its builder pattern.** E20, when it fires, adds
its **own builder files beside E18's**, consuming the pattern; it edits neither
E18's builder nor `conftest.py`'s fixture plumbing except through this arc's
end ruling. The §1.5 finding — a design collision no file discipline prevents —
is banked with the halt as the reason sequencing gates name *artifacts*, not
just files: "the D2 pattern" was a dangling pointer until D2 existed, and a
dispatch that points one lane at another lane's unbuilt pattern owes the gate
E20's kickoff carried. E20's re-fire now has **one condition**:
`E18-index-mcp-report.md` exists.

## Ruling 3 — U6's scope includes `record_mcp.py`, and the audit CITES rather than re-proves (the §7 flagged question) (2026-08-08)

The scope sentence — every `assert`/ANDON/refusal in `tools/` — admits no
exception, and the server will be committed record by E18's halt. But U6's job
is the **census of fireability**, not re-authorship: per guard, the audit names
**the existing test that fires it** (E18's own error-surface tests count fully),
and only a guard no test fires gets U6's can-fail treatment or its written
reason. The lane rule survives intact: E20 writes no tests against E18's server;
it indexes the ones E18 wrote.

## Ruling 4 — the entry measurements are BANKED; three predictions are WATCHED (2026-08-08)

**4a — the coverage baseline is the measured shape of "32 tests is weak"** and
enters the record as E20's founding measurement: 8 of 33 tracked tools reached
by any test, every one at whole-tool subprocess level, `mask_geometry` — a
shared implementation two tools import — reached by nothing. Not that 32 is
small; that the 32 enter through eight front doors with nothing below them.

> ⚠ **CORRECTED IN PLACE 2026-08-08 at Ruling 10, by E20's own report (§2, §4,
> F4) — the denominator was wrong.** `tools/` holds **150** python files, not 33:
> the census scanned `tools/*.py` only and missed `tools/verify/` and
> `tools/diagnostics/` entirely, which is also how it missed that `mesh_stats.py`
> lives at `tools/verify/mesh_stats.py`. The *shape* of the finding survives
> untouched and is if anything sharper — the qualitative claim was that coverage
> enters through a handful of whole-tool front doors with nothing below them, and
> a larger denominator strengthens it. But **the ratio "8 of 33" was never a
> measurement of what it claimed to measure** and must not be requoted. Read 4a
> for its shape, not its fraction.

**4b — the guard census is U6's entry table** as provisional (431 guard-shaped
lines across 33 tools; the ~2:1 comment-inflation dedup is U6's actual work
— ⚠ **measured at Ruling 10: 431 grep-shaped lines against 204 AST sites over
the same files = 2.11:1**, so the provisional table was inflated exactly as
flagged, and the real top-level total is 204 of a 409-site tree),
with the two zero-guard units named: `mask_geometry` and `mesh_stats` carry no
guards at all, which changes what U6 can say about them and is itself a
finding-shaped fact for the arc.

**4c — three predictions are WATCHED, adjudicated only at the arc's end**: P12
(a triangle-edge scale remnant in finalize's unit — which would contradict the
recorded repair and therefore matters in either direction), P5
(`fit_background` unguarded where a figure touches the frame edge — invisible
on every fixture that floats clear), P17 (the census dedup ratio). No number
moves on a prediction.

## Standards compliance (this ruling)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every ruling cites the halt file's section, the commit, or this fold's own observation of the staged tree |
| ANDON_AUTHORITY | 3 | the ruling ratifies a gate that fired before any work, and converts the sequencing sentence into one checkable re-fire condition |
| NAMED_COMPENSATORS | 2 | dispositions are assignments and citations, revertible per commit; nothing irreversible occurs. Scored 2: stated, none exercised |
| DECOMPOSE_BY_SECRETS | 3 | the pattern's ownership follows the deliverable that was always its owner; the audit cites across lanes instead of crossing them |
| UNCERTAINTY_GATED_HUMANS | 3 | the Director's §8 word is recorded as governing; the one question deferred to this seat is answered with the race closed by assignment, one sentence to overrule |
| EXTERNAL_VERIFIER | 2 | the banked baseline and census are the session's read-only measurements against the tracked tree, reproducible by grep; the watched predictions await the arc's own instruments |

---

# The arc's end ruling (2026-08-08, night — the second advisor seat)

Rules on [E20-coverage-report.md](E20-coverage-report.md). Evidence — what this
seat OPENED: the coverage report in full, `E20-ruling.md`'s Rulings 1–4 as
written, `tools/record_mcp.py`'s error surface and health contract, the live
suite under the pinned interpreter (**202 passed, 140.04 s**), and the mounted
server's own responses at this seat's hands.

## Ruling 5 — THE COVERAGE ARC IS ACCEPTED, and its largest finding is not a test

110 tests in three new files, no conftest edit, no tool behavior changed, zero
seams taken unilaterally, ASCII throughout, hermetic tier at 47.01 s against a
~3-minute bound. The suite goes **92 → 202**; tools reached go 8 → 10; guard
sites demonstrably fired go **9 → 17**.

**But the deliverable that matters most is the refusal.** Asked for six units,
the session measured that **three of them cannot exist** — and rather than
inventing something callable or restructuring accepted-asset tooling on its own
authority, it produced the AST evidence, proposed three seams, and said *"the
executor does not decide whether to take them."* That is the separation of roles
working exactly as designed, and it is worth more than the three units would
have been.

**No coverage theater** is verified, not asserted: every test asserts an outcome,
and the two negative-only tests exist as the other half of a can-fail pair and
say so. The `chr()` detail is the session at its best — a first pass converted
the dash constants to `"--"`, which would have left **every dash test passing
while testing nothing**, since the dash class is one character and a two-hyphen
stand-in matches on its first. A weakened test that still passes is worse than a
failing one, and catching that in your own work is the hard version.

## Ruling 6 — ALL THREE SEAMS ARE TAKEN. Order by risk; every one carries its anchor.

The seams are the arc's unblocking move and the reason U2b/U4/U5 are empty. They
are taken in this order, **one commit each, tests riding it, the named anchor
re-run in the same commit**:

| # | seam | anchor that proves nothing moved | risk |
|---|---|---|---|
| **3** | `tools/verify/mesh_stats.py` — `main()` guard only; `measure(path, label)` is already a function and is unreachable solely because import runs the pipeline | T12's subprocess warning test, unchanged | lowest — a guard, not a move |
| **1** | `project_twins.py` — move `figure_mask` and `fit_background` into `mask_geometry.py`, beside `local_thickness` | the twin-projection anchor, re-run across the extraction | low — **the precedent is exact and already blessed**: `local_thickness` was extracted to that same module for E16-10 for this same reason |
| **2** | `texpass_finalize.py` — wrap the body in `main()` behind a `__main__` guard; lift the lookup into a function taking arrays | **T7's byte-identity anchor** | highest, and the anchor is strongest — the tool has zero function defs, so this is the largest structural move in the set |

**Why take them at all**, stated so the reasoning is checkable rather than
assumed: these are not refactors for taste. Three units the Director asked for
are undeliverable without them, and one of those units carries **P5** — the only
unresolved prediction with a named failure mode nobody has ever looked for
(`fit_background` where a figure touches the frame edge, invisible on every
fixture that floats clear). A tool that cannot be called cannot be tested below
its front door, and "the 202 enter through ten front doors" is the same finding
4a made about 32 and eight.

**The bound, absolute:** each seam is a *pure move*. No behavior change rides
along, no signature is improved in passing, and if an anchor does not reproduce
byte-for-byte the seam is reverted and reported, not adjusted until it passes.
The must-not-move trees are E04's, E08's, E13's and E14's, and these tools
produce them — the anchors are exactly what stands between a seam and those
trees.

## Ruling 7 — U6's SCOPE IS RULED: the audit is about 212 of the 409 sites

The report refused to narrow this unilaterally and reported the strata
separately so it could be ruled. Ruled:

| stratum | sites | in scope? | reason |
|---|---|---|---|
| `tools/*.py` | 204 | **YES** — the audit | the route-active surface; 15 fired (7.4%) |
| `tools/verify/` | 8 | **YES** | these are the measurement instruments; a verifier whose guards cannot fire is the exact object this repo distrusts |
| `tools/diagnostics/` | 186 | **NO, with a re-open condition** | 65 one-shot research instruments. E19 treated the class as out of scope for a different gate and was right. **Re-opens per file** the moment a diagnostic becomes route-active or a ruling cites its output as evidence |
| `tools/superseded/` | 11 | **NO, permanently — and this one is a principle** | these are kept **because they fail**. A can-fail test there would assert that a falsified approach still fails *in a particular way*, which converts "anyone can run those tools and watch them fail" into a **maintained contract on our own dead ends** — and a maintained contract is a thing that must be kept green. The failure is documented in prose and reproducible by running the tool; that is the mechanism, and a test would weaken it by making the repo responsible for the shape of its own falsified approaches |

**The audit is therefore 212 sites, 15 fired, and the priority is the report's
own:** the `e11` pair first (`e11_manifest.py` 37 guards / 0 fired,
`e11_export_turnaround.py` 26 / 1 — **63 sites, one fired**, in two ~50 KB
export-path tools), then `project_twins.py` (19 / 0). This is a program across
sessions, not a session; it is dispatched in strata, not as a number to reach.

**The census method is adopted with its stated bound.** AST for guard sites, an
18-character sliding window over each guard's own message for firedness — a
**lower bound**, because a test that fires a guard without quoting its message is
invisible to it. The detector's first cut asked the question backwards and
**undercounted its own author's tests 2 of 3**; that it was found, fixed and
reported rather than quietly replaced is the reason the number is usable at all.

## Ruling 8 — THE FOUR FINDINGS, DISPOSED (fix-or-bless, per the assertion law)

**F1 — `github_slug`: RETIRE it.** Zero callers in `tools/` or `tests/`, and it
makes an external claim about GitHub's anchor algorithm that could not be
verified offline. Verifying it would buy a maintained commitment to another
project's undocumented behavior for a function nobody calls. Delete it in the
same commit as its removal-justifying grep; if an anchor generator is ever
needed, it is written then, against a rendered anchor, by a caller that exists.
*A function whose correctness cannot be checked and whose absence cannot be
noticed is not an asset.*

**F2 — `texpass_iter:437`'s comment: FIX the comment, change no code.** The
measurement stands (`local_thickness` returns nonzero off-mask within `r` of a
core, pinned by T25), the fix stands, the recorded 38,041-vs-4,344 stands. Only
the stated *mechanism* is narrower than the comment implies — the
admit-everything failure needs background **far** from any core, not merely
off-mask. Correct it in place with T25 cited, per the corrections-in-place law.

**F3 — the silent `tools/call`: E18's lane, and I name the likely cause rather
than leave it a mystery.** The probable explanation is protocol, not defect: MCP
requires the client to send the `notifications/initialized` message after
`initialize` before calling tools, and a hand-rolled client that skips it leaves
a correct server waiting. **That is a hypothesis, not a ruling** — it is checkable
in one run and E18's lane checks it. If confirmed, the disposition is a
documentation line, not a code change, and the report's instinct still holds:
a call that can neither answer nor refuse is the same family as a check that
cannot fail, so if the server *can* detect the case it should refuse with a code.

**F4 — the halt report's census was wrong in scope and kind: BLESSED, and it
cost a prior ruling.** Reported against its own instrument rather than quietly
replaced, which is the standard. It falsifies Ruling 4a's denominator — corrected
in place above. **The lesson is the one this repo keeps paying for: check what
your denominator is made of before the first result depends on it.** `tools/*.py`
was a glob someone typed, and it silently defined the population for a founding
measurement and a banked census.

## Ruling 9 — THE WATCHED PREDICTIONS, ADJUDICATED

Ruling 4c armed three. No number moved on any of them; here is their disposal.

**P12 — FALSIFIED, and it is the good kind.** The triangle-edge scale remnant
does not exist: the edge length is **measured per mesh**, the tool prints
"(measured on this mesh)", and the rescale test returned 1.00000 twice because
L103 normalizes by `max|component|` — which is *required*, since the gate is a
ratio and both operands must share a frame. **The recorded E07 repair holds.**
4c said this mattered in either direction and it did: a falsification here is a
confirmation of the record, and the executor correctly identified the wrong
premise as **its own**, then found the lever that does test per-mesh-ness
(tessellation), which passes.

**P5 — UNSETTLED, and it is now the highest-value open question in the repo.**
`fit_background` is unreachable, so the border-ring contamination question at
frame-edge figures has still never been looked at. It survives as the named
target of seam 1 and is the single reason seam 1 outranks seam 2 in Ruling 6.

**P17 — HIT to the decimal.** 431 grep-shaped lines against 204 AST sites over
the same files = **2.11:1** against a predicted ~2:1. This retroactively
justifies the method switch: the provisional census in 4b was inflated by
comment text, and any future guard count in this repo is an AST count or it is
not a count.

## Ruling 10 — A NEW STANDING LAW, earned by the calibration lesson

The report's own calibration read is the most transferable thing in it, and it
becomes law:

> **A documented past bug is evidence an area is well-guarded, not evidence it is
> fragile.** E20's three prediction misses — P2, P3, P12 — all predicted a defect
> in a function whose docstring carries the story of the bug it once had. The
> record's own scar tissue read as live risk. The predictions that landed (P8,
> P17, P18) were about **quantities**, not about whether someone had been
> careless. Predict magnitudes; do not predict negligence where the record shows
> a fix.

This sits beside the repo's existing calibration laws and is the first one earned
from a *prediction* pattern rather than from a measurement error.

## Ruling 11 — THE MOUNT PREMISE WAS WRONG, and the seat it named is now closed

The dispatch told E20 it was *"the FIRST session in this repo with the true
in-session mount."* Measured false, and the measurement is clean: `.mcp.json`'s
mtime is **11:30:42** against a session that started ~11:23, because the re-fire
arrived as a new turn in the *same continuous parked session*, and MCP servers
mount at session start. **The dispatch's error was mine to inherit** — it assumed
a fresh session where the Director's park had created a resumed one, which is a
premise nobody checked because it looked like a scheduling detail.

The session's response is the right one and is adopted as practice: rather than
fall back to reading, it drove the **same `MCPServer` instance through the SDK
`Client`**, exactly as `tests/mcp_support.py` does — the server's own dispatch,
schema validation and error wrapping, minus the literal wire. `record_health`
then earned its keep in five minutes by catching a **DB/certificate drift across
the session boundary** with the exact fix in its hint, and one `record_build`
recovered it in 3.17 s.

**The open seat is closed at this seat.** This advisor session is the first with
the true in-session mount: `mcp__facet-record__*` resolved at start, and the
server answered live here — `record_health` returned `SERVING`/`PASSED` with
byte-identity and 19/19, and two deliberate bad inputs returned structured
`BAD_ARGUMENT` refusals while the server stayed up (E19 Ruling 4's B4 evidence).
The record was queried, not read, exactly as the instrument was built for.

## Ruling 12 — THE TAG IS UNBLOCKED, with the re-count standing

[E19 Ruling 7](E19-ruling.md)'s amendment held v1.0.0 until E20 closed, because
the suite moved 92 → 202 *inside* the E19 ruling session and a release cannot be
edited. **That condition is now satisfied:** E20 has halted at its report and is
ruled here.

**The seams and the U6 program do NOT block the tag.** A tag marks the state of
the record at a commit; it is not a promise of quiescence, and waiting for an
open program would defer v1.0.0 indefinitely. Seam work and the can-fail program
land after it, in v1.0.1+.

**What stands is the gate, not the wait:** one `--collect-only` at the tagging
commit, and every surface must match before the tag fires. At this ruling the
figure is **202 total / 194 hermetic / 8 artifacts**, and all ten surfaces carry
it.

## What this ruling did not do

No seam taken (they are dispatched, not executed here — this seat rules, it does
not execute). No tool, test, `conftest.py`, `ci.yml` or fixture edited. No tag,
release, translation or metadata change. No memory-store write. E20's report and
predictions untouched.

## Standards compliance (the end ruling)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every ruling cites the report's section, a measured figure, or this seat's own live tool call; the seams carry named anchors per commit |
| ANDON_AUTHORITY | 3 | the arc's central act was a refusal to write three units that cannot exist, honoured rather than worked around; F4 is a halt turned on the session's own instrument |
| NAMED_COMPENSATORS | 3 | each seam's compensator is its anchor: an anchor that does not reproduce byte-for-byte reverts the seam rather than adjusting it. Ruling 8's F1 retirement is one revertible commit |
| DECOMPOSE_BY_SECRETS | 3 | Ruling 7 partitions 409 sites by *why they exist* — route-active, verifier, research, falsified — not by directory convenience, and the superseded exclusion is argued from what those files are for |
| UNCERTAINTY_GATED_HUMANS | 3 | the three questions the executor refused to decide (seams, U6 scope, findings) are decided here with reasons; F3 is explicitly labelled hypothesis-not-ruling so the next seat can falsify it |
| EXTERNAL_VERIFIER | 3 | the report's numbers were re-measured at this seat under the pinned interpreter (202 passed) and the server's error surface was fired here rather than read; the census method's own undercount is disclosed and its bound stated |
