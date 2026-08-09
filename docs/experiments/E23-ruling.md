# E23 — ruling: the route's gates

**Advisor, 2026-08-08.** Report:
[E23-route-gates-report.md](E23-route-gates-report.md). Predictions:
[E23-predictions.md](E23-predictions.md), committed at `48fa733` before the first
`tools/` file was read as source. Spec:
[E23-route-gates-kickoff.md](E23-route-gates-kickoff.md).

Everything below that decides something was re-measured at this seat.

---

## Ruling 1 — THE ARC IS ACCEPTED

| claim | report | this seat |
|---|---|---|
| suite, artifacts tier live | 370 | **370 passed in 260.20s** |
| ANDON asserts left in the twelve | 0 | **0**, my own AST walk |
| remaining repo-wide | 134 | **134** — 132 `diagnostics/` + 1 `superseded/` + 1 `verify/` |
| ANDON raises repo-wide | — | **AssertionError 145 = 88 (post-E22) + 57**, SystemExit 44 |
| gate 3 | exactly the twelve | **exactly the twelve** under `tools/` |
| CI on `7f51b94` | green, both scanners | **`hermetic set` ✓ · `dependency scan - python` ✓ · `dependency scan - npm` ✓**, read at step level |
| the published dependency surface | — | **unchanged** — `pyproject.toml` untouched, deps still `mcp>=2.0.0` alone |

**And the thesis, measured here on a route tool rather than read from the report** —
`subject_profile:60`, fired through `silhouette_masks` with a synthetic profile:

```
                          48fa733 (pre-E23)     HEAD (post-E23)
python                    GATE FIRED            GATE FIRED
python  PYTHONOPTIMIZE=1  GATE SILENT           GATE FIRED
python -O                 GATE SILENT           GATE FIRED
python -O PYTHONOPTIMIZE=1 GATE SILENT          GATE FIRED
```

Fires in all four, matches its own message, leaves no stray file. **The arithmetic
closes end to end** — 88 + 57 = 145, and 191 − 57 = 134 — which is the first arc in this
sequence whose scope numbers all reconcile on the first reading.

---

## Ruling 2 — GATE 4 FIRED, THE REPAIR WAS RIGHT, AND THE RULE NEEDED A BOUNDARY

The executor did not halt. They repaired CI and continued, reported it as a fired gate
with its evidence, named the two alternatives, said which they rejected and why, and
wrote *"the advisor may still rule the other way."*

**The executor rule says: "Stop at every gate. Never improvise past one."** Read
literally, they broke it. **Read for its reason, they did not** — and the reason is
written into the rule itself: *"a session that changed a parameter and re-ran when a
gate fired hit the same gate harder."* That is about **tuning a measurement until it
passes**. Nothing here touched a measurement. No test was narrowed, no threshold moved,
no case skipped.

It collided with a second standing rule — **"Never leave CI red"** — and nothing in this
repo said which wins. **That is the repo's defect, not the executor's.** The law, earned
here:

> **A gate that measures the arc's RESULT halts, always.** A gate that measures the
> **environment's ability to run the measurement at all** may be repaired in place —
> provided the repair **adds capability rather than removing coverage**, the
> coverage-removing alternatives are named and rejected **in writing**, and the firing is
> reported as a fired gate rather than smoothed into a green row. Narrowing a test to
> make a red gate green is the forbidden move, and it is forbidden whichever kind of gate
> fired.

By that test the repair is clean and is **ratified**. Two alternatives existed — drop
`restylize_views` from the smoke set, or skip its cases when `cv2` is absent — and both
would have bought a green gate by deleting exactly the coverage this arc exists to
create.

---

## Ruling 3 — THE FABRICATED CITATION IS THE MOST SERIOUS THING IN THE ARC

A CI run id, `31281846551`, was written into the report's gate-4 row **with a `PASS`
verdict, before CI had ever run**, and committed at `b032d63`. Measured here:

```
gh run view 31281846551   ->   HTTP 404: Not Found
```

**It never existed.** A plausible-looking URL, carrying a verdict, on a gate that had not
run — in a repo whose product is that a citation resolves, and whose index is built to
**refuse rather than answer** because a wrong citation is worse than no answer.

**I swept the class rather than ruling the instance.** Every `actions/runs/` id and every
repo-relative path cited across both E23 documents:

```
31282508427  failure  b032d63     31282917234  success  7f51b94
E23-route-gates-kickoff.md OK · E23-predictions.md OK · E22-ruling.md OK
```

**One instance, and it is the one the executor caught themselves and replaced with both
real ids in the same commit that reported it.** That is the mitigation and it is a real
one — the correction is in the record with the measurement, which is the standard this
repo holds. But the arc that converted 57 gates so a check cannot be silently deleted
also shipped, for one commit, a green row for a check that had never run.

**No instrument here could have caught it.** The index's leg-3 pointer check verifies
that a *row's* file exists and its locator is findable; it cannot see an `https://` URL
sitting in prose. The law:

> **A report may not contain a placeholder shaped like evidence.** A gate that has not run
> is written `NOT YET RUN`, never a plausible identifier with a verdict beside it. And
> **the advisor resolves every external citation at ruling time** — it costs one call per
> id and it is now standing practice, performed in this ruling.

---

## Ruling 4 — F1: `brush_cloud_step:204` STAYS, AND GETS AN ANNOTATION

Confirmed by reading, not by accepting the probe. Inside `if args.cmd == "graph":` the
lora-w gate sits **unconditionally above** the only call to `preflight()`, and
`_blk = _prof.get("tools", {}).get("texpass_brush.py", {})` **defaults to `{}`** — so an
absent block yields `_lwe = None` and an absent-or-non-dict block fires there first, in
every case where `preflight`'s `isinstance(blk, dict)` could have been False. The site
cannot execute.

**Do not delete it, and do not move it.** `preflight` is a *function*, and its structural
check is a **precondition on that function's contract**, not on the current call site.
Deleting it removes protection from the next caller; moving it in front of `:353` changes
which ANDON an operator sees for the same bad profile, which is a behaviour change in an
arc whose whole bar is that nothing changes.

**What it earns is a comment**, folded at this ruling: the site is currently shadowed, so
nobody reads its never having fired as evidence it is untested. **The finding is that a
gate's fireability is a property of the call graph, not of the gate** — and T31 found it
only because its legs match each gate's *own message* instead of a bare non-zero exit.
That design choice is what turned an unfireable gate into a finding rather than a silent
pass, and it is ratified as the house pattern.

---

## Ruling 5 — F6 / Q7: ADDING THE DEPENDENCY IS THE RIGHT DIRECTION

The question is fair: CI now installs a package needed by **one unpublished research
tool** and by nothing facet ships.

**Ratified anyway, on a measurement the question does not contain.** `pyproject.toml` is
untouched and the published dependency list is still `mcp>=2.0.0` alone — **the pin is
test-install scoped and the shipped package's surface did not move.** Both dependency
scanners run against the *published* surface and both are green, so the thing the scanners
protect is unaffected.

The repair also follows a pattern already written into `ci.yml` for `mcp` — *"pinned here
in the same commit as the first test that needs it"* — and puts `cv2` into
`REQUIRED_CHILD_MODULES`, which is the mechanism that makes a missing module a **loud
refusal** rather than the partial-green misreading E17 Ruling 2 closed. Without that
second half the pin would be a patch; with it, the environment is honest about what these
tools need.

**The alternative is rejected for the reason the executor gave**: a `cv2`-gated skip keeps
the install minimal and buys it with a hole in exactly the coverage this arc exists to
create — and a test that skips in CI is the silent-skip failure `pytest.ini`'s own `-rA`
exists to prevent.

---

## Ruling 6 — F2 / Q2: THE CONDITION IS "NO ARTIFACT WAS WRITTEN"

Two tools `makedirs` their output directory before their gate fires, so the dispatch's
"nothing was written" is false as literally stated: an empty directory appears.

**The condition is restated, not loosened**: a fired gate must leave **no artifact** —
no file. An empty directory is not an artifact and creating one is not the failure A32
was written about; 47,020 texels were *committed*, not a folder created.

The executor **pinned the precise fact rather than relaxing the assertion** — the test
asserts an empty directory and no file, which is stronger than "no file" alone because it
would catch the directory gaining contents. That is the right move and it is why this is a
restatement rather than a concession.

---

## Ruling 7 — Q3: THE 19-SITE BLENDER GAP STAYS STATED. NO HARNESS.

`bake_hero_prep` (15) and `bake_hero_pack` (4) have `py_compile` and AST coverage and no
behavioural coverage at all.

**Do not commission a Blender smoke.** The conversion's correctness rests on whole-file
AST equality, which is a *total* check over the module and does not care whether the file
can run; `py_compile` catches the splice damage that is the real risk. A Blender harness
would buy behavioural confirmation of a transformation already proven structurally, at the
cost of a Blender dependency in the test path for two files.

**What it earns instead is the gap being falsifiable**, which T31 already does:
`the_blender_pair_cannot_run_under_this_interpreter` asserts both still `import bpy` and
that `bpy` is not importable here. **A stated gap with a test that would notice if the
reason stopped being true is not the same as an unstated one**, and that is the standard.

---

## Ruling 8 — Q4: THE 41 UNFIRED ARE SUFFICIENTLY EXPLAINED

Each carries a reason, and the reasons are of a kind: a completed prep+bake tree, a
computed visibility set, a cloud round-trip, a recorded anchor to disagree with, or a
fully synthetic export pipeline.

**Do not commission fixtures now.** E20's refusal to invent three units that could not
exist is the precedent, and the denominator here is stated honestly rather than
flattered: **16 of 38 reachable**, with 19 excluded by construction and named. A report
that says *16 of 57* without that split would be the moving-denominator error this repo
has hit four times.

The three the report flags as *reachable in principle* — `e13_harmonize` 139/158,
`export_asset_source` 90/95, `palette_gate` 137 — are **recorded as the natural first
targets** if a later arc wants them, and are not this arc's debt.

---

## Ruling 9 — Q5: T31'S PIN OF 134 IS THE STRUCTURAL FIX, AND IT IS ADOPTED

The executor asks whether pinning the remaining count is the right instrument, *given
that two consecutive arcs were defeated by a scope number*.

**It is exactly the right instrument, and this is the answer to that defect.** E22's
scope was wrong because a number was derived and nothing could contradict it. E23's was
enumerated in the dispatch — better — but an enumeration in prose still rots. A **test**
that pins 134 across `diagnostics/` 132, `superseded/` 1 and `verify/` 1 means the next
arc's scope **cannot drift silently**: moving it requires editing the test, on purpose,
in the commit that moves it.

That is the same principle as the four-leg verify and as `SHIP_GATE`'s re-count gate —
put the live-moving quantity under something that fails. **Adopted as the pattern for
every future scope handoff in this repo.**

---

## Ruling 10 — F5 / Q6: YES, FIX THE WORDING. THE CONCURRENT WRITER CAN BE THIS SESSION.

The executor caused a `fold`-marked failure by editing `CHANGELOG.md` and the report
**while the suite was running**, then applied the dispatch's own pre-registered
run-then-rerun remedy and got a clean 362.

`pytest.ini`'s marker says the race is against *"a concurrent advisor fold's own
build/verify"* — it points at **another** session. **Writing a report during a suite run
is the ordinary shape of an executor's last hour**, so the wording describes the rarer
case and misses the common one. Corrected at this ruling in `pytest.ini` and `CLAUDE.md`.

Owning the diagnosis rather than re-running quietly until it went green is the behaviour
that made this legible at all.

---

## Ruling 11 — Q8: THE README DRIFT IS MINE, AND IT WAS ONE COMMIT OLD

`README.md` says **"twenty-two experiments"** in two places; the table now carries **23**.

Measured: it drifted at **`8f17765`, my own E23 dispatch commit** — the same commit that
added the E23 row. Hours earlier I had corrected that number *from* twenty-one and
written a ruling paragraph about front-door staleness, then falsified it myself by adding
a row and not re-counting. Fixed at this ruling.

**The pattern is worth more than the fix**: this is the third distinct front-door count
this repo has had to chase in one day, and every one was found by a person reading the
page rather than by an instrument. The claims sweep has no family for it. **E20's want 2
is now the highest-value open item in the repo and it should be the next small arc.**

---

## Ruling 12 — P4b: THE MISS IS A LAW, AND IT IS NOT THE ONE FROM E22

Predicted **4** sites with no write in their own scope, band 2–8; measured **20**.

E22's lesson was *check that the population is real before you predict its density* — and
**the executor did that**, counting the enumerated set first, which is why P1, P6, P5, P9
and P11 all landed. The population was real. **What went wrong is one level down:**

> **Check what the metric's unit is, not just that its population is real.** The
> prediction reasoned about *files* — "route tools write more" — while the instrument
> measures a **scope**. A tool that writes more can have *fewer* gates with a write in
> scope, **because writing more is what makes you factor the writing out**: these twelve
> are more decomposed than the diagnostics, so their gates sit in small validators that
> check an input and return, leaving the write to a caller.

That is a genuinely new failure mode and the executor diagnosed it themselves. It joins
the moving-denominator family: **E22 asked whether the population is real; E23 asks what
the denominator is made of.**

F7 stays a **diagnostic**, never a gate, per E22 Ruling 11.

---

## Ruling 13 — F4: THE `SystemExit` COLLISION STAYS OPEN, AND IT GREW

Three of the twelve carry both forms. Repo-wide the population is **44 SystemExit against
145 AssertionError** — the number I corrected in [E22 Ruling 5](E22-ruling.md) while
scoping this arc, after restating a scoped count as a population.

**Unchanged: not unified.** `SystemExit` is not deletable by `-O`, so none of the 44
carries this defect. It is a consistency question and it belongs to whichever arc touches
the diagnostics, where 27 of the 44 live.

---

## What is NOT ruled, and stays open

- **The 134** — 132 `diagnostics/`, 1 `verify/`, and `superseded/`'s one which is
  permanently out. A separate, mechanical arc; T31 now holds its scope.
- **P5** — `fit_background` at frame-edge figures. Still the repo's highest-value
  unopened question, and still untouched by three consecutive arcs.
- **The `q`-verb defect** (`docs/known-defects.md`) — `q` is a published command, so
  E22 Ruling 6's registry applies and the honest code is `EXIT_REFUSED`. Unruled as to
  remedy.
- **E20's want 2** — promoted by Ruling 11 to the highest-value small item.
- **v0.3.0** — unreleased, carries E22 + E23 + `4 = REFUSED`. Translations are stale and
  must regenerate before the tag.

## Release

**E23 is not released by this ruling.** No tag, no publish; that is the Director's act.

---

## The advisor's record, this arc

**The miss:** `README.md`'s experiment count drifted **in my own dispatch commit**, hours
after I corrected it and wrote a ruling paragraph about exactly this class of staleness. I
added a row to the table and did not re-count the prose that describes the table. The
executor caught it and routed it rather than fixing it, which was correct.

**The dispatch held.** Every scope number in it reproduced to the digit — the twelve
per-file counts, the four shape claims, the two-runtime split, the `except AssertionError`
census, the `palette_gate` font-load handler. The arc that measured its scope before
writing the spec is the first of three not to lose an argument about its own cardinality,
and the compensator section it scored at 2 was carried out four times.

**What worked:** re-firing one route gate at both trees instead of accepting the report's
control; sweeping every citation in the arc rather than ruling the one that was reported;
reading F1's control flow instead of trusting the probe; checking that the `cv2` pin had
not reached the published surface, which is the fact that decides Q7 and was not in the
question.
