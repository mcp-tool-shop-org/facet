# E25 — ruling: the last of the deletable gates

**Advisor, 2026-08-09.** Report:
[E25-diagnostics-gates-report.md](E25-diagnostics-gates-report.md). Predictions:
[E25-predictions.md](E25-predictions.md). Spec:
[E25-diagnostics-gates-kickoff.md](E25-diagnostics-gates-kickoff.md).

Ruled with a second arc's uncommitted work in the same tree, so every measurement below
was taken on a **pristine clone of `d908ccc`** or on committed blobs, never on the live
working copy.

---

## Ruling 1 — THE ARC IS ACCEPTED, AND THE CLASS CLOSES EXACTLY

Re-measured here with my own AST walk over `tools/`:

```
ANDON asserts remaining ANYWHERE under tools/ : 1
   tools/superseded/texpass_thin_mask.py        <- the permanently-excluded site
ANDONs that RAISE : AssertionError 278 · SystemExit 44
REMAINING_ELSEWHERE = 1
```

**278 = 87 (E22) + 57 (E23) + 133 (E25) + 1 pre-existing.** Against a pre-E22 census of
**278 ANDON-carrying asserts**, that is the whole class converted but one, and the one is
the one that was ruled never to convert. **Four arcs, and the arithmetic closes on the
first reading** — which after E22's phantom 207 and E23's 192-that-was-191 is worth
saying out loud.

**The pure move, proven with my own instrument** rather than the executor's: each of the
43 files taken as git had it at `1b60478`, the negation rule applied **in the tree**, and
`ast.dump` compared over the whole module —

```
tools/ files changed by E25                          43
  whole-file AST identical to the rule applied       43
  NOT identical                                       0
comment tokens changed (UTF-8 decode, explicit)       0
```

---

## Ruling 2 — GATE 4 IS **BLOCKED**, NOT FAILED, AND THE BLOCKER IS FULLY ATTRIBUTED

The executor wrote `see the CI line below` rather than a verdict it did not have. That is
[E23 Ruling 3](E23-ruling.md) — *a gate that has not run is written `NOT YET RUN`, never a
plausible id with a verdict beside it* — applied by an executor to its own report, and it
is the right call. **Resolved here, because only this seat can.**

**E25's own run never produced a verdict.** Measured:

```
run 31294688455  head 59f9409  04:30:02  CANCELLED
run 31294891661  head d908ccc  04:35:31  FAILURE
ci.yml  concurrency: group ${{ github.workflow }}-${{ github.ref }}
        cancel-in-progress: true
```

Same ref, same workflow, a push 5½ minutes later — **E26's push cancelled E25's run.** Not
a flake and not the executor's doing.

**The run that does contain E25's commit failed, and every failure is another arc's:**

```
25 failed, 614 passed, 1 skipped, 8 deselected
  25 of 25 in tests/test_t34_front_door_counts.py
   0 of 25 in T33, tools/diagnostics/, or tools/verify/
```

Each one says the same thing: a surface states **423** where the collector reports
**648**. That gap *is* E25's 225 new tests, landing correctly, against surfaces that had
not been updated yet — and the update is written and sitting uncommitted in the other
seat's tree.

**So: E25's code is not implicated in a single failing assertion.** The gate is recorded
as **BLOCKED — external, attributed**, and it closes the moment E26 commits the surface
update it already has. Writing `PASS` would be a verdict I cannot support; writing `FAIL`
would be false.

### The law this earns

> **A parallel arc cannot own a CI verdict for its own commit.** With
> `cancel-in-progress: true` — which the studio's Actions rules *require*, and which is
> correct for sequential pushes — a second session's push **cancels the first's run
> before it can produce evidence**. An arc's gate 4 is therefore satisfied by the first
> **completed** run whose tree contains its commit, and the report must name that run
> **and what else was in it**. If that run is red for another arc's reason, the gate is
> **blocked, not failed**, and the arc owes the attribution — a failure count is not a
> verdict until you know whose failures they are.

---

## Ruling 3 — F1 IS CONFIRMED TO THE DIGIT, AND THE MECHANISM IS NOT QUITE WHAT IT SAYS

The executor's proof instrument decoded `git show` output with the platform codec and
mojibaked every em-dash, reporting **10 files** with changed comment tokens *before
anything had been converted*. Unfixed it would have "failed to prove identical" — and by
gate 2 therefore **reverted** — every file containing a non-ASCII character.

**Reproduced here exactly: 10.** And refined, because the account is one step off:

```
comments compared, BOTH sides decoded cp1252   :  0 differ
comments compared, BOTH sides decoded UTF-8    :  0 differ
comments compared, ONE side cp1252, one UTF-8  : 10 differ   <- the real mechanism
files under the scope containing non-ASCII     : 36 of 43
```

**The codec was not the bug. The asymmetry was** — a blob read one way and a working file
read another. A symmetric wrong codec would have compared equal and hidden nothing. That
matters for the next instrument: *decode both sides the same way, and say which way in the
code.*

**How it was caught is the transferable half, and the executor states it plainly: a
number that had to be 0 came back 10.** An instrument with a known-zero case is worth more
than one with only a plausible range, and this arc had one by construction.

---

## Ruling 4 — F2: REVERTING 43 FILES WHOLESALE WAS CORRECT

The first conversion passed 43/43 per-site and formatted multi-line messages in a shape
the 145 already-converted sites do not use. The executor **reverted all 43 and re-ran
against the measured form** instead of patching the difference.

**Ratified, and it is the second time this exact judgement has been made** — E23 did the
same when its rendering diverged from E22's. A patched-to-match file and a
generated-correctly file can be textually identical and still differ in what they prove:
the AST equality holds either way, so only the *procedure* distinguishes them. Re-running
the generator keeps the proof meaning what it says.

---

## Ruling 5 — P3's MISS IS A REACHABILITY UNIT, AND IT IS THE THIRD OF ITS FAMILY

Predicted **46 of 130** fire hermetically; measured **17**. The executor's own diagnosis:
reachability is set by *how many mutually consistent artifacts must exist before a gate*,
not by whether each input format is authorable on its own.

That is E23's P4b and E24's P1 again — **the population was right and the unit was
wrong**, three arcs running. The prediction counted *formats a person could write*; the
instrument counts *states a program can reach*. Upheld as a miss, and the lesson is
already in CLAUDE.md; this is its third instance and the first where the executor named
the unit before I did.

**17 of 130 is not a shortfall to apologise for.** These are one-shot instruments whose
gates sit behind whole recorded trees. E20's refusal is the precedent: the honest list is
short and the reasons are stated.

---

## Ruling 6 — THE OTHER GATES

| gate | verdict |
|---|---|
| 1 · suite before and after | **PASS.** Baseline **384**, measured in-session rather than inherited — the dispatch's 370 predated E24's then-uncommitted T32, exactly as P9 anticipated |
| 2 · whole-file AST equality | **PASS**, and re-proven independently here, 43/43 |
| 3 · scope | **PASS.** Exactly 43 files, all under `diagnostics/` or `verify/`; nothing in E24's or E26's files |
| 5 · tree manifest | **PASS.** 7,312 files, 17,072,807,610 bytes, baseline + 2 rechecks, 0/0/0 |
| 6 · `superseded/` untouched | **PASS**, and **T33 pins it by name**, so the permanent exclusion is now enforced rather than remembered |

Gate 6 deserves the note: [E22 Ruling 4](E22-ruling.md) ruled that site never converted,
and a later sweep reading it as an oversight was the obvious failure mode. It is now a
test.

---

## Ruling 7 — F5: `test_t05_claims_sweep` GETS THE `fold` MARKER

It read `README.*.md` while E26 was writing them, failed in the full suite and passed in
isolation. **It has the same exposure to a live corpus as every `fold`-marked test and no
marker at all**, so its race presents as a plain red test instead of an attributable one —
which is precisely the failure mode [E23 Ruling 10](E23-ruling.md) corrected the marker's
*wording* for, one test away from where the wording lives.

**The marker costs nothing in CI**: the hermetic set runs `-m "not artifacts"`, and `fold`
is not `artifacts`, so the test still runs on every push — the marker only lets a local
session deselect it while a fold is in flight, which is exactly what it is for. It applies
to the corpus-reading tests in that file, not to the synthetic-fixture ones.

**⚑ Not applied from this seat, and the reason is ownership.** `tests/test_t05_claims_sweep.py`
had **five tests added to it by E26 during this same arc** — the scan-set superset, the
front-door reach check, the CHANGELOG split, the classification sweep and the
build-untouched leg. That file changed hands while E25 was running. **The marker lands in
E26's fold**, where the file is already open and its owner can say which tests read the
live corpus; applying it here would be a third seat editing a file a live arc just
extended, which is the exact hazard these coordination rules exist for. Recorded as owed,
with an owner.

## Ruling 8 — F6: A PUSH PUBLISHES THE OTHER ARC'S COMMITS, AND THAT IS CORRECT

E25's push moved origin `3ce6a39..59f9409` and carried E26's predictions commit `1b60478`
with it. **Not a defect.** A push moves a branch; every commit under the tip goes with it,
and `1b60478` was a deliberate, complete commit.

What the coordination rules were missing is the check, not a prohibition:

> **Before pushing on a shared branch, look at what you are about to publish.**
> `git log --oneline origin/main..HEAD` — every commit that is not yours should be another
> arc's *deliberate* commit. If one looks like work in progress, stop and say so; do not
> publish another session's half-finished state, and do not try to push around it.

## Ruling 9 — F7: E22's MANIFEST FIGURE IS WITHDRAWN, AND THE OPEN ITEM CLOSES

E23 flagged E22's **16.3 GB** as an unreconcilable discrepancy it could not attribute.
E25 measured the recorded root independently: **7,312 files / 17,072,807,610 bytes** —
**byte-for-byte identical to E23's**.

Two independent measurements now agree exactly, and neither matches E22's figure
(17,072,807,610 bytes is 15.90 GiB or 17.07 GB; **16.3 is neither**). **The discrepancy is
in E22's number, not in the trees.** E22's 16.3 GB is withdrawn as unreconcilable — the
measured quantity is the file count and the byte total, both of which have now reproduced
twice. **I did not take a third measurement**; two independent agreements to the byte is
the evidence, and it is stated as that rather than as three.

## Ruling 10 — F8 and F9 are already routed correctly

**F8** (`e04_make_brush_prompts.py` does file work before argparse) was named by the
dispatch and confirmed; it is a property of that instrument, not of this conversion, and it
stays open as a small thing anyone may fix.

**F9** (the T-number namespace has no allocator) is [E24](E24-ruling.md)'s finding
reproduced from the other side — E25 took T33 after the dispatch had to be corrected mid-
flight. **Two arcs have now hit it.** The allocator is not worth building for a repo with
one branch and a handful of concurrent seats; **the rule is the fix**: take the next free
number, and say in the report which numbers were taken when you looked.

## What is NOT ruled

- **CI is red at `d908ccc` as this is written**, for 25 T34 assertions that E26 owns and
  has the fix for, uncommitted. *Never leave CI red* is standing, and this is the first
  time it has been left red by a **hand-off boundary** rather than by a defect. It is
  E26's to close and it goes to the Director with this ruling.
- **E25's report is written and uncommitted**, pending gate 4's verdict — which is above.
- The `SystemExit` collision (28 sites, 12 files) stays unresolved by
  [E22 Ruling 5](E22-ruling.md); it is now the whole of what remains of that question.
- **P5** — untouched by six arcs.

## Release

Nothing here is released. 0.3.1 remains the Director's call, and it now carries E23's,
E24's and E25's work.

---

## The advisor's record, this arc

**The miss is a dispatch defect, and it is mine.** E25's coordination table described
**two** arcs in the working copy. I dispatched **E26 into the same tree** while E25 was
live, having written that table myself an hour earlier — and I did not amend it. The
executor found the third arc rather than being told about it, and its report says so. The
disjointness held (E26 touched `facet_index.py` and `tests/`, E25 `diagnostics/` and
`verify/`), so nothing collided — but that was a property of what I happened to scope, not
of anything I checked at the time.

**And the concurrency hazard was foreseeable and I did not foresee it.** I wrote the
`fetch`/`merge --ff-only` rule after hitting the rebase problem myself, and never asked the
next question: what happens to a *CI run* when two sessions push to one branch. Ruling 2's
law is written now, one arc late, at the cost of an executor's gate-4 evidence.

**What worked:** ruling on a pristine clone rather than a tree with two arcs' work in it;
re-proving the pure move with my own instrument instead of accepting 43/43; taking the
failure *census* from CI rather than the failure *count*, which is what made the
attribution unambiguous; and reproducing F1 closely enough to find that its stated
mechanism was one step off.
