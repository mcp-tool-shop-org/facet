# E24 — ruling: the install that could not find the record

**Advisor, 2026-08-09.** Report:
[E24-installed-paths-report.md](E24-installed-paths-report.md). Predictions:
[E24-predictions.md](E24-predictions.md), committed at `720bae8` before any source file
was opened. Spec: [E24-installed-paths-kickoff.md](E24-installed-paths-kickoff.md).

Ruled while [E25](E25-diagnostics-gates-kickoff.md) runs in parallel; nothing here
touches a file E25 owns.

---

## Ruling 1 — THE ARC IS ACCEPTED

Re-measured at this seat, on a wheel **I built from this tree** rather than on the
report's word:

| | report | this seat |
|---|---|---|
| suite | 384 | **384 passed in 261.17s**, 0 skipped on the rig |
| T28's five | byte-identical, pass | **untouched** (`git diff` empty), **5 passed** |
| scope | four named files | **exactly four** in `e8b24db` |
| CI on `e8b24db` | green, both scanners | **success**, both scanners at step level |

**And the fix itself, from a wheel installed into a clean venv:**

```
cwd = the checkout        q -> 0 with correct rows · claims -> 0 · banner reads
                          db: E:\AI\facet\docs/index/facet.db      (was <venv>\Lib\...)

cwd = an empty dir        q -> 4 · claims -> 4 · build -> 4
                          message names BOTH candidates and BOTH markers
                          hint names both ways forward
                          facet-mcp --print-tools -> 0   (the working path, unregressed)
```

**Exactly `4`**, which is constraint 2 met rather than approximated. Four releases shipped
a wheel that could not find its own record; it can now, and when it cannot it says so.

---

## Ruling 2 — THE RESOLVER IS RATIFIED, INCLUDING THE PART THAT WAS LEFT OUT

The property is asked directly — *does this directory contain the record* — instead of
`FROZEN`, which named a **runtime** and was a proxy for it. That is this repo's own law
applied to a fix rather than a gate, and it is the right shape.

**Two markers, and the second is load-bearing.** Re-measured here, and the number is
worth reading carefully: on this rig, directories carrying `CLAUDE.md` number **14** at
one level under `E:\AI` and **62** recursively — the report's 26 is a third scan depth.
**That number is depth-dependent and should not be quoted as a property.** The half that
matters is not: at *every* depth I tried, **exactly one** directory also carries
`docs/experiments`, and it is `E:\AI\facet`. A single-marker resolver would bind some
other repo and fail deeper in. Two markers is correct, and the reason survives the count
being fuzzy.

**No walk-up from cwd — RATIFIED, on the executor's reasoning.** A walk-up would resolve
from a subdirectory of a checkout, which is a benefit, but it can also reach a *different*
record's root, and it makes the refusal message a list instead of a statement. **Adding a
walk-up later is additive and safe; removing one later is a behaviour change.** Prefer the
narrow rule and re-open when an operator actually hits it — not before.

---

## Ruling 3 — CI MUST RUN THE TIER. IT IS SKIPPING, AND THAT IS THE DEFECT'S OWN SHAPE.

The report routes this and it is the most important thing in the arc after the fix.
Measured at this seat from the CI log:

```
370 passed, 6 skipped, 8 deselected
  5 skips: tests/test_t32_installed_wheel.py — `python -m build` is not installed
  1 skip:  the pre-existing mount tier
```

**The tier built to catch this defect class does not run on the gate that fires every
push.** It is not a silent skip — the reason prints, `-rA` sees to that, and the executor
reported it rather than letting a green tick stand for coverage. But a check that is
present on one rig and absent from CI is the same shape as the defect it was written for:
*every check exercised the surface that works.*

**RULED: `build` is pinned in `ci.yml`, in this fold.** It is one line, it follows the
pattern `ci.yml`'s own comment already prescribes for `mcp` and `cv2` — *"pinned in the
same commit as the first test that needs it"* — and [E23 Ruling 2](E23-ruling.md) already
ratified adding a dependency rather than narrowing a test. The alternative is a tier that
exists to be read about.

Applied and verified by watching CI, not by asserting it.

---

## Ruling 4 — T28 PINS SOURCE TEXT, AND THAT IS WHY THE DESIGN IS SHAPED THIS WAY

The executor's first finding, raised before any code was written, and it is correct.
`tests/test_t28_frozen_runtime.py:78`:

```python
assert "os.getcwd() if FROZEN else REPO" in SRC
```

That is a **literal source-string match**. It pins an *implementation*, not a behaviour —
so when the resolver subsumed the `FROZEN` branch, the branch could not be removed without
breaking a test that constraint 3 forbade breaking. **A test asserting source text forced
a design.**

**`FROZEN` stays at `record_mcp.py:119` for now**, subsumed and harmless, stating intent at
the site. What is ruled is the general form, and it goes to CLAUDE.md:

> **Pin a structural property with an AST walk, never with a source-string match.** This
> repo already does the former in four places — the `--debug` confinement, the flag
> allowlist, the converted-gate structure. A string match is the outlier, and it survives
> nothing: rename a variable and it fails on correct code; keep the string and it passes
> on broken code. It cannot tell you the property still holds, only that the characters
> are still there.

And beside it, in the same file, `test_t28:76`:

```python
assert "Temp" not in pathlib.Path(frozen_default).parts[:2] or True   # documentation
```

**`or True`. The assertion cannot fail.** It is labelled, which is the honest half — and
[E22 Ruling 3](E22-ruling.md) established that an author's declaration is what separates a
sanity check from a gate. But this one lives in a *test file*, where the entire contract is
that a failure means something. **Converting both is a small, well-scoped arc**; it is not
E25's, and it is not urgent enough to interrupt anything.

---

## Ruling 5 — THE README LINE IS MINE, AND IT WAS WRONG WHEN I WROTE IT

The report's second new finding: `README.md:47` said a wheel install *"works only for `q`
and `claims`"*. **`claims` did not work** — it died on `<venv>/Lib/CLAUDE.md`, exit 2.

I wrote that line hours earlier at the v0.3.0 read-back, from a measurement I took of `q`
and then **generalised to `claims` without running it**. That is the same move I have
convicted two dispatches of in two days: a quantity asserted about a class after measuring
one member.

It is now wrong a second way — the fix landed, so on `main` both verbs work. **Corrected
in this fold to describe the released state and the fixed state separately**, because
v0.3.0 is what a user gets today and `main` is what 0.3.1 will carry. Fourth front-door
drift in this class in two days, and the second of them mine.

---

## Ruling 6 — THE TIER'S OWN WEAKNESS WAS CAUGHT BY THE EXECUTOR, AND THE CATCH IS THE POINT

First run against the pre-fix tree: 13 of 14 failed — **but 10 failed with `AttributeError`
on symbols that did not exist yet.** The tier was reddening the old tree because the *new
API was absent*, not because the artifact misbehaved. A gate that fails for the wrong
reason passes for the wrong reason too.

They found it, said so, and repaired it before committing: behavioural failures went
**3 → 8**. That is the difference between a tier and a formality, and it is exactly what
gate 3 was written to force. **Ratified.**

The one leg that passes on the broken tree is the `--help` leg, deliberately kept — *it is
precisely what stayed green through four releases*, and a tier that no longer contains it
would lose the record of how the defect hid.

---

## Ruling 7 — P1's MISS IS E23's LAW ONE LEVEL FURTHER DOWN

Predicted **17 of 19** consumers changing, band 14–19; measured **13**. Outside the band.

The instructive part is what the six survivors are: two of them (`:494`, `:890`) are line
numbers of a **statement whose other line changed** — so "did this consumer change" depends
on whether you count *statements* or *lines*, and the enumeration was given in lines.
E23's lesson was *check what the metric's unit is*; this is that lesson applied to the
prediction rather than to the instrument. **The population was right and the unit was
ambiguous** — which is a subtler failure than E23's and worth carrying.

---

## What is NOT ruled

- **Converting T28's two assertions** (Ruling 4) — a small arc, unscheduled.
- **`release.yml`'s new verb sequence has never fired in anger.** It runs only on
  `release: published`. Dry-run on the rig: exit 0 on the fixed wheel, **exit 2 on the
  broken one**. It proves out at the next tag, and the next tag is the Director's.
- **P5** — still the repo's highest-value unopened question, now untouched by five arcs.
- **E20's want 2** — queued behind this arc, which owned the files it needs.

## Release

**0.3.1 is not cut by this ruling.** The fix is on `main`; the tag is the Director's act.
Everything a release needs is already true — 384 green, CI green, four version declarations
still agreeing at 0.3.0 and needing a patch bump, and the release notes template proven by
dry-run.

---

## The advisor's record, this arc

**The miss:** `README.md:47`, Ruling 5 — I measured `q` on the broken wheel and wrote a
sentence about `q` **and `claims`**, having run one of them. The executor ran the other and
it exited 2. A dispatch I wrote the same day convicts two prior arcs of exactly this shape.

**The dispatch held.** Every enumerated number reproduced — 19 consumers plus the
definition, the wheel's contents, the marker's absence from an install, the two-runtime
split. The three constraints ruled in the dispatch did real work: constraint 1 kept the env
var a DB selector, constraint 2 produced an exact `4`, and **constraint 3 is what surfaced
T28's source-text pin** — a finding that would not exist if the dispatch had said "don't
break things" instead of naming the five tests.

**What worked:** building a wheel myself and running the verbs rather than reading the
report's table; checking that the refusal returns exactly `4` rather than merely non-zero;
re-measuring the marker count at two depths and reporting that the count is depth-dependent
while the conclusion is not; reading the CI log for the skip rather than trusting a green
tick.
