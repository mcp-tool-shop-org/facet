# E26 — ruling: the counts nothing watched

**Advisor, 2026-08-09.** Report:
[E26-front-door-counts-report.md](E26-front-door-counts-report.md). Predictions:
[E26-predictions.md](E26-predictions.md). Spec:
[E26-front-door-counts-kickoff.md](E26-front-door-counts-kickoff.md).

---

## Ruling 1 — THE ARC IS ACCEPTED

Re-measured here:

| | report | this seat |
|---|---|---|
| counts at merged HEAD | 648 / 640 | **648 / 640** |
| T34 | 34 tests | **34 collected** |
| `record_markdown()` untouched | yes | **AST-identical** across `3ce6a39..HEAD` |
| four legs after Half B | pass | **VERIFY PASSED, all four** |
| the sweep | 0 new STALE | **STALE: 0** |
| CI | green | **31295436475 success**, both scanners |

**Half A works, and it is the only instrument in this repo that has ever caught a live
drift end to end** — not a planted one, not a mutation in a test fixture. It fired on
`main`, in CI, on a real staleness nobody arranged. That is worth more than the 34 tests.

---

## Ruling 2 — GATE 5 FIRED, AND THE HOLE IT FOUND IS IN MY COORDINATION RULE

The report does not soften this and neither will I: **CI went red on a commit this arc
pushed**, run [`31294891661`](https://github.com/mcp-tool-shop-org/facet/actions/runs/31294891661),
25 assertions all saying *"states full 423, the collector reports 648."*

The executor's own diagnosis is right: it measured on a **worktree pinned to `1b60478`**
while E25 committed T33 **locally** into the shared copy, so the tree it committed *to*
had moved even though the tree it measured *on* had not.

**And `git fetch && git merge --ff-only origin/main` — the rule I wrote — cannot see
that.** Verified: that guard compares local `HEAD` against `origin/main`. A sibling
session's **unpushed local commit** leaves `origin/main` an ancestor of `HEAD`, so the
guard reports *already up to date* and is telling the truth about the only thing it
watches. It is a **remote**-divergence guard being asked to catch **local** divergence.

> **A worktree answers what your change produces. It does not answer what the tree you
> commit to contains — and only the second is what a surface may state.** In a shared
> copy, re-measure any quantity a surface asserts **against the tree you are about to
> commit**, after `git add` and before `git commit`. The pull guard is about the remote
> and cannot substitute for this.

**But the structural fix already landed, and it is this arc's own deliverable.** No
coordination rule needed to catch this, because **T34 caught it** — in CI, on the merged
tree, naming the site and both numbers. That is [E23 Ruling 9](E23-ruling.md) vindicated
a second time: *put the live-moving quantity under a test, and the coordination rule stops
having to be perfect.*

**The failing run stays in the record as a failure and the wrong paragraph stays in the
report with what happened beside it.** That is the standard, and the executor held it
without being asked.

---

## Ruling 3 — THE MATCHER'S FORM GAP IS REAL, AND THE FIX IS A CONVENTION, NOT A WIDER REGEX

The executor routed it; I sized it. On a **swept** surface (`README.md`), planted at HEAD
on a throwaway worktree:

```
"The suite is 999 tests as of this line."     ->  3 FAILED   caught
"The suite is 999/991 as of this line."       ->  34 passed  SLIPS
"The suite moved 384 → 999 this week."        ->  34 passed  SLIPS
```

**Live, not latent.** A current-state count written in slash or arrow form on a watched
surface is invisible to the sweep.

**Ruled: do NOT widen the matcher.** Widening is exactly how the first one was wrong — its
own census returned **45 hits of which 15 were not test counts at all** (`RTX 5090`, four
ISO dates, six identifiers, `limit=999`), and it simultaneously **missed** a real French
site because French spells it *hermétiques*. A matcher loose enough to catch `648/640` is
loose enough to catch a version string and a date range, and this repo has already paid
for that lesson once in this arc.

**The fix is a writing convention, declared in T34's own docstring**: a current-state test
count is written in the phrase form the sweep watches (`N tests`, `N hermetic`). Anything
else is not pinned and is not claimed to be. That converts a blind spot into a stated
boundary — the same disposition the translations already have at `:265`.

**Related and correctly handled:** `SCORECARD.md` is classified historical **wholesale**,
so a current-state claim added there is invisible too. That classification is right —
SCORECARD states gate results at treatment entry — but **document-level classification
cannot see a mixed document**, which is the same limitation as Ruling 4 below, from the
other end.

---

## Ruling 4 — MY ENUMERATION WAS ARITHMETICALLY RIGHT AND STRUCTURALLY WRONG

The dispatch listed the surfaces and predicted 22 sites. **22 is what there were.** And the
enumeration was still wrong, in a way a count cannot show:

**`SHIP_GATE.md:61` is one physical line carrying four current-state clauses and eight
historical pairs.** No file-scoped rule reaches inside it; no line-scoped rule can either.
**Only spans work**, and the dispatch gave the executor a list of *files and sites* while
requiring a current-versus-historical rule that a site cannot express.

I wrote that line. I extended its lineage four times across four arcs, each time adding a
historical pair beside the current clause, and never noticed I was building the one
structure my own enumeration could not describe. **The executor had to invent the span
model to satisfy a gate I specified.**

**And two surfaces the dispatch did not name carried the claim** — one of them
`docs/advisor-kickoff.md`, **stale by three releases**: untouched since `9efe228` when the
suite was 248, through 275, 370 and 384, until this arc fixed it. That is the handoff
document whose own step 1 reads *"RE-COUNT — currently N total"*, and it is mine. **The
document that tells the next seat to re-count was the one carrying the oldest wrong
count.** Fourth front-door drift class in three days, third instance that is the advisor's.

---

## Ruling 5 — HALF B IS CORRECT AND ITS YIELD IS NEAR ZERO. THAT IS THE ANSWER, NOT A DISAPPOINTMENT.

The widening did what it was told: sweep set 256 → 266 files, `record_markdown()`
AST-identical, four legs pass, **0 new STALE**.

And the measured yield is the finding: **three of the four named files carry no family
claim at all**, and CHANGELOG's three arrive `UNPARSEABLE` because arc attribution is
line-scoped and the changelog wraps.

**So want 2's original framing is now falsified from both ends.** The dispatch had already
shown it could not catch a test count; the execution shows the surfaces it was written for
mostly make no claims the sweep understands either. **Ruled: Half B stays — it is correct,
it costs nothing, and a blind spot closed is worth having — but want 2 is CLOSED, not
carried forward as an open item.** What it was reaching for is done, and it was done by
Half A.

---

## Ruling 6 — THE MATCHER REWRITE IS RATIFIED, AND ITS CENSUS IS THE REASON

The first matcher was proximity-shaped. **Its own census killed it**: 45 hits, 15 not test
counts, one real site missed in French. The executor replaced it with a phrase-shaped
matcher following the repo's existing `CLAIM_SHAPED` idiom, and declared the translation
boundary rather than pretending seven languages were covered.

**Running a census on your own instrument before trusting it is the behaviour this repo
keeps rediscovering** — E22's assert census, E23's shape measurement, E25's known-zero
comment check, and now this. It is the cheapest reliable defence against an instrument
that answers a different question than the one asked.

---

## Ruling 7 — P8 AND P9

**P8** — predicted 8 tests, measured 34. *"I predicted things I would write; the instrument
counts parametrized cases."* **Fourth consecutive arc where the population was right and
the unit was wrong** (E23 P4b, E24 P1, E25 P3, now E26 P8). The law is in CLAUDE.md and it
is still catching people, which is what a law is for.

**P9** — predicted 5 STALE, measured 0. The executor's own reading: *"I predicted a
population's density without checking the population was there — the law the dispatch
quoted at me, which I applied to P1 and not to P9."* **Applying a law to one row of your
own prediction sheet and not the next is the honest version of this failure**, and saying
so is what makes the miss useful.

---

## What is NOT ruled

- **The translations' digit substitution.** The executor substituted digits rather than
  regenerating. It is correct for a number-only change and it is not what the
  release-ordering law contemplates. **Before any tag, translations regenerate** — that
  stands, and the digit substitution is a stopgap between releases, not a replacement.
- **T05's owed `fold` marker** ([E25 Ruling 7](E25-ruling.md)) — routed to this arc because
  it owned the file, and not taken. Still owed, still small.
- **P5** — untouched by seven arcs.
- **0.3.1** — the Director's call; it now carries E23, E24, E25 and E26.

---

## The advisor's record, this arc

**Two misses, and both are the same shape: I specified a check whose structure I had not
looked at.**

1. **The enumeration** (Ruling 4). I gave a list of sites and demanded a current-versus-
   historical rule, on a surface I had personally built into a single line holding both.
   Right count, wrong structure — and the executor had to design past it.
2. **`docs/advisor-kickoff.md`** (Ruling 4). Stale by three releases, in the document that
   instructs the next seat to re-count, which I have edited repeatedly without ever
   re-counting it.

**And the coordination rule I wrote has a hole I did not test** (Ruling 2) — `--ff-only`
guards the remote and cannot see a sibling session's local commit. I wrote it after hitting
the rebase problem myself and never asked what it does *not* cover. The executor found it
by having CI go red on their own commit.

**What worked:** sizing the form gap by planting all three notations on a throwaway
worktree rather than accepting or dismissing the routed finding; testing on a *swept*
surface after the first two plants passed, instead of concluding the sweep was broken;
verifying `record_markdown()` by AST rather than by diff; and confirming that
`SCORECARD.md`'s silence was a correct classification rather than a hole.
