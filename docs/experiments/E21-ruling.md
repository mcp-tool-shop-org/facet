# E21 — advisor rulings (2026-08-08, night)

Rules on [E21-cli-contract-report.md](E21-cli-contract-report.md). Evidence — what this
seat OPENED: the report in full, the predictions at `f942d01`, `facet_index.py`'s and
`record_mcp.py`'s changed regions, and **three measurements of my own** taken before
ruling (an AST census of every `assert` in `tools/`, an ANDON-construction census across
the write path, and a control test of `-O` / `PYTHONOPTIMIZE=1` on the pinned
interpreter).

---

## Ruling 1 — THE ARC IS ACCEPTED

Four gates passed with evidence, the suite went **218 → 248** green, scope held exactly
(`git diff --name-only -- tools/` returns the two published scripts and nothing else),
and the two unruled outcome classes were **left at the codes they had rather than
picked**. That last part is the arc's discipline showing: an executor assigning a number
to a fired ANDON would have been deciding what a result means.

Three things deserve naming beyond the acceptance:

- **`run_contract` wraps `main()`, not the `__main__` guard.** `[project.scripts]` binds
  `facet-index = facet_index:main`, so a contract in the `if __name__` block would be
  present in a source run and **absent from every installed command** — the exact
  surface this arc exists to fix. That is T28's lesson applied without being told.
- **`--debug` is confined by an AST walk with its own can-fail leg**, and a fired gate
  still refuses with it set. E08 Amendment 32 is honoured in the letter and the spirit.
- **U3 shipped nothing and measured instead**, because the dispatch reserved the
  boundary. The census is worth more than the flag would have been (Ruling 6).

## Ruling 2 — F2 IS NOT AN INSTANCE. IT IS A CLASS, AND IT DEFEATS E08 AMENDMENT 32 ACROSS THE WRITE PATH.

The report found one bare `assert` gate in a shipped command and correctly refused to
fix or pin it. **Measured at this seat, the construction is not rare — it is the norm.**

```
tools/                       294 bare asserts across 72 files
```

And restricted to gates that carry the `ANDON` token:

| tool | ANDON as `assert` | as `raise` |
|---|---|---|
| `tools/texpass_iter.py` — **the write-head** | **8** | **0** |
| `tools/texpass_finalize.py` | **4** | **0** |
| `tools/project_twins.py` | **15** | 1 |
| `tools/e11_manifest.py` | **35** | 1 |
| `tools/e11_export_turnaround.py` | **24** | 1 |

Control on the pinned interpreter, run three ways:

```
NORMAL           : gate fired -> ANDON: gate fired
python -O        : gate SILENT, execution continued past it
PYTHONOPTIMIZE=1 : gate SILENT, execution continued past it
```

**E08 Amendment 32 was earned when a PowerShell chain walked past a fired ANDON and
committed 47,020 texels.** The repair was to move the check *inside the tool*, with no
skip flag. That repair is defeated: the check is an `assert`, and one environment
variable deletes 87 of them across the tools that produced four accepted assets —
including every ANDON in `texpass_finalize` that E20's T26 fired to prove it *"refuses
before writing the atlas."*

**It is strictly worse than the original defect.** The shell chain at least let the
ANDON print before walking past it. Under `-O` the gate never speaks: the write
proceeds, the process exits **0**, and the log shows a clean run.

**THE NEW STANDING LAW, and it goes in CLAUDE.md at the next fold:**

> **A gate is never a bare `assert`.** `assert` is a developer's sanity check that the
> interpreter is licensed to delete; `-O` and `PYTHONOPTIMIZE=1` remove it silently and
> execution continues past it. A check that decides whether an irreversible step
> proceeds must `raise` — the separator does not have to be a shell chain to be a
> separator, and an environment variable is a cheaper accident than a shell chain.

**Severity, stated honestly rather than dramatised:** nobody sets `PYTHONOPTIMIZE` in
this repo's recorded commands, so the probability that this has *already* corrupted an
artifact is low, and I am not claiming it has. But **A32's test is separability, not
probability** — that is the whole content of the amendment, and by its own test these
are not gates.

**E22 is dispatched** (§ at the end of this ruling). The executor's refusal to pin it is
ratified: a test asserting *"`PYTHONOPTIMIZE=1` disables the gate"* would anchor the
defect, and the correct test is the opposite one, written after the repair.

## Ruling 3 — Q1 (the ANDON's exit code) is BLOCKED, and the report was right to say so

The report notes Q1 and F2 are entangled and asks which to rule first. **F2 first, and
Q1 is blocked on E22.** Assigning an exit code to a gate that an environment variable
removes is assigning a code to an event that may not occur — the code would be a
statement about a guarantee that does not exist yet.

**Interim disposition: the ANDON stays at `1`, and the overlap is documented rather than
tidied.** `SHIP_GATE.md` and the CHANGELOG both already say two non-user-error classes
are squatting on `1` pending this ruling; that stays true and stays written until E22
lands. Option (e) — exit `0` — is excluded permanently: a gate that exits 0 is A32's
failure mode restated.

## Ruling 4 — Q2 (a failing `verify`) MOVES OFF `1`, to a dedicated code

**This is the most important signal either command produces and it currently shares a
code with a mistyped flag.** A caller cannot distinguish *"fix your command"* from
**"do not trust this index"**. That is the defect; the integer is secondary.

Ruled against each option on its merits:

- **(a) stay at 1** — rejected. It is the defect.
- **(b) 2, runtime error** — rejected. The tool did not break; it measured. Collides
  with genuine crashes, and F3 shows the value is persisted, so the collision would be
  written into an artifact.
- **(c) 3, partial success** — **rejected, and this is the load-bearing rejection.**
  `verify` *completed*; the report argues this correctly. Assigning it `3` would
  populate a code by redefining its name, which is precisely the move this repo forbids
  — the same family as retuning a pass condition after seeing the result. **A free
  integer is not a reason.**
- **(d) a dedicated code** — **ADOPTED.**

**`4 = REFUSED` — the tool ran correctly and is telling you not to proceed.** The
registry's `0/1/2` are the standard's; `3` stays reserved and unused as the report
pinned it; `4` is domain space the standard leaves open, and using it is not a deviation
from the standard but a use of the room it leaves.

**One code, not two.** When E22 unblocks Q1, a fired ANDON takes **the same `4`**. Both
mean *the tool worked, the answer is no, do not proceed*; no caller has been shown to
need the distinction, and the message already carries it. Splitting `4` into two codes
later is additive and cheap; merging two codes later is not. Start with one.

**Implementation is folded into E22, not done now** — F3 means the change moves a
persisted certificate field (`verify_exit_code`) and one fixture constant, and E22 is
already touching this contract. One behaviour change per release; **v0.2.0 ships with
the overlap named** (Ruling 8).

## Ruling 5 — Q3 (partial success): NO, and the pin is right

Nothing partial-succeeds. A ten-row sweep returns only {0,1,2}; every candidate was
considered and rejected on the honest ground that each **completed**. `EXIT_PARTIAL = 3`
stays declared, documented as unused, and pinned as never returned — with a can-fail leg
requiring the sweep to have produced ≥3 distinct classes, so its silence is not
vacuous. **No partial-success path was invented to populate a code**, which is exactly
what the dispatch asked for and the opposite of what a checkbox invites.

## Ruling 6 — U3: THE BOUNDARY IS ADOPTED, AND NOTHING SHIPS. C5 becomes a JUSTIFIED SKIP.

**The boundary, ruled:** *levels govern progress and diagnostic chatter; they never
govern a measurement, a refusal, or an ANDON.* Plus the addition the report surfaced and
asked about, which I rule **in**:

> A print may be quieted only if the same value reaches the caller through a
> **non-stdout channel**. `build`'s per-table counts qualify because `build()` *returns*
> them; `verify`'s measurements do not, because stdout **is** their only channel.

**And on that boundary, the set to govern is empty enough that shipping a flag would be
speculative infrastructure:**

- `verify`'s 35 print sites contain **zero progress lines**, and `record_mcp` parses that
  stdout to build the certificate (F4). **A quiet `verify` breaks a shipped artifact.**
  For this tool *"stdout is the measurement record"* is not a principle — it is a live
  mechanical dependency.
- `facet-mcp`'s serving path prints **nothing**; a stdio server that writes to stdout
  corrupts its own JSON-RPC stream.
- That leaves **one** progress line, in `build`, which **already** has a `quiet=`
  keyword that `record_build` already uses.

**So `SHIP_GATE.md`'s C5 is ruled SKIP — with a measured reason rather than the
inherited habit it had before.** The old reason ("stdout is the measurement record") was
an argument about research scripts and I said so when I dispatched it; the census
replaces it with a mechanical one. **Re-open condition:** any print site is added that
is progress or diagnostic chatter, or `verify` gains a return channel for its
measurements — at which point the flag has a set to govern.

This is the best possible outcome for a gate item: it moves from *unchecked gap* to
*justified skip* on evidence, and the evidence is a census a future session can re-run.

## Ruling 7 — F7: the allowlist widening is BLESSED, and the way it was done is the standard

T21's closed flag allowlist is the guard whose purpose is to make a new flag on the
refusing command expensive. It fired on `--debug` — **correctly** — and it was widened by
exactly one, in writing, with a condition attached, and the same test now *checks* that
condition with an AST walk proving `record_mcp` branches on `--debug` nowhere.

**Widening a guard to admit one's own change is the move that must never be quiet.** It
was not quiet. It is the only pre-existing test this arc changed, and it is reported as
such.

## Ruling 8 — v0.2.0 SHIPS, with what it does not yet do written down

The improvement is real and independently correct: user error was on `2` and runtime
error on `1` **with a raw traceback** — inverted at both ends, which my own dispatch got
half right (F1 corrects `SHIP_GATE.md:42`, which named only the argparse half; **that
line was mine**). Holding the release gains nothing.

It ships with the overlap **named in the CHANGELOG and the gate**, which it already is:
two classes that are not user errors sit on `1` until E22. That is honest, and it is
strictly better than the state it replaces.

**Owed before the tag, in this order** — the release-ordering law, unchanged:
counts re-measured at the tagging commit (**248 / 240**, the seventh move) → every
surface updated → **translations re-run at the advisor's hands** → `gh repo edit` needs
nothing → tag → `release.yml` publishes both registries. **F6's certificate regeneration
lands with the DB pair at the boundary**, so the tag does not ship a certificate
claiming `server_version: "0.0.0"`.

## Ruling 9 — the predictions, and a calibration note that is better than a good score

**6 hit / 5 miss / 3 split** in the blind band; 5 hit / 1 miss semi-blind. **Every one of
the five clean misses is a quantity** — print sites, ANDON tokens, edited call sites,
findings, files. Not one is a miss about *behaviour*.

The report's own read is the correct one and I adopt it: E20's lesson was *predict
quantities, not negligence*; this arc predicted quantities and was **bad at them, about
2× high on density**. That is the more useful failure, because a density model is
correctable by measurement and a negligence model is not.

**P5 is the instructive miss and the report names it against itself:** it predicted the
two files did not share a module, having reasoned about frozen-binary packaging risk for
a dependency that *was already there and already frozen*. `record_mcp` has imported
`facet_index` since it was written. **Before building a path to a resource, enumerate the
resource** — this repo's own law, and the report cites it against itself rather than
being told.

**And P23, filed as a lookup, was wrong** — the version bump took 7 edits, not the 5 a
grep reported, because the grep pattern could not match `//   binary: facet-0.1.1-…`.
Owning a *lookup* error is rarer and more useful than owning a prediction error: a
prediction is allowed to be wrong, and **a lookup is supposed to be a measurement.**
*Check what your instrument is made of before the first result depends on it.*

---

## E22 IS DISPATCHED — the gates that an environment variable deletes

**Question:** the repo's ANDONs are bare `assert`s. Does converting them to raises
preserve every anchored behaviour exactly, and does the write path then refuse under
`-O` as it does without it?

**Scope, ruled:** the **87 ANDON-carrying assert sites** in the five tools measured
above, `facet_index.py`'s guard, and `record_mcp.py`'s `assert code in CODES`. The other
~207 non-ANDON asserts are developer sanity checks and are **out** — converting them
wholesale would be a large diff over accepted-asset tooling for no gate.

**The bar, and it is the whole difficulty:** these tools produced four accepted assets
and several write into the must-not-move trees. **Every conversion is a pure move**; the
anchors are the proof. T7's byte-identity replay, T26's three fired ANDONs, and the
twin-projection anchor must reproduce **exactly**, and an anchor that does not reproduce
reverts the conversion rather than adjusting it.

**Tests ride it, starting at T30**, and the shape is fixed: for each converted gate,
**the gate still fires under a normal interpreter AND under `-O`/`PYTHONOPTIMIZE=1`**.
That is the test the repair makes writable and the one the current construction makes
impossible.

**Fold Q2 in:** `verify`'s failing return moves to **`4 = REFUSED`**, and a fired ANDON
takes the same `4` once it is a raise. Both certificate and fixture consequences (F3)
are named in the report and must be carried.

**Out of scope:** the ~207 non-ANDON asserts · U3's flag (ruled SKIP) · the three
testability seams · P5 · the release.
