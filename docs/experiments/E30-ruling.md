# E30 — the advisor's ruling

**Ruled 2026-08-09.** Report:
[E30-polish-anchor-gates-report.md](E30-polish-anchor-gates-report.md). Predictions:
[E30-predictions.md](E30-predictions.md). Dispatch:
[E30-polish-anchor-gates-kickoff.md](E30-polish-anchor-gates-kickoff.md).

**The arc is accepted, its halt is ratified as the most valuable thing it produced, and one
of its findings is overturned at this seat before it could be spent.**

---

## Ruling 1 — THE EIGHT ANCHORS ARE ACCEPTED

T50–T57, 11 tests, 250.66 s. Three finalize replays decided at the **byte** tier (atlases
byte-identical, and the galleon's and dragon's sidecars with them), three ceilings and the
dragon's elevated decided at the **value** tier — the elevated payload reproducing *whole*,
both ladder rungs, every float — and the galleon's commit anchor at the byte tier across
four state files at the recorded 31,581 texels.

**No sha256 literal appears in any of them**, and the counts are *loaded from* the recorded
JSON rather than transcribed. That is stricter than T8's literals and it is the right
reading of the dispatch's property 1: a literal is a number someone typed, and it can be
typed to match.

Two process notes worth ratifying. The executor **found and removed a check of its own that
could not fail** in T56 before it landed — this repo's own law, applied to its own work
unprompted. And the galleon's commit pairing was established by a **conservation identity**
(holes lost equals styled gained, exactly, from `bindcheck` to each selftest) rather than by
running anything — a free proof where a run was the obvious move.

## Ruling 2 — THE HALT IS RATIFIED, AND IT IS THE ARC'S MOST VALUABLE OUTPUT

W3's projection does not reproduce: styled **1,718,750** against a recorded **1,653,659**
(+65,091), with holes falling by exactly the same count. The executor halted at gate 5,
characterised the difference, and stopped. Correct on every point.

**And it is characterised the right way round.** The byte tier flagged it; the **pixel tier
confirmed it** — 330,481 differing pixels with the largest connected component only 4.8% of
the differing set, so the difference is **distributed, not concentrated**. That distinguishes
a real acceptance-rule change from the false-halt class that has twice cost this repo a live
halt, and it is the two-tier instrument from [E28](E28-ruling.md) Ruling 14 doing exactly the
job it was commissioned for, on its first use by another seat.

**What this means, stated plainly: a route tool changed under an accepted asset, and nothing
noticed until an anchor was built for it.** That is precisely the condition the Director's
clause exists to detect — *"this is what happens when something like this is neglected"* —
and the clause found it on its first outing. **A negative result is a full success**, and
this one justifies the whole arc.

**The accepted asset is not in question.** W3's GLB was ruled at the Director's eye and
remains accepted. What is now measured is that today's `project_twins` default would not
reproduce its stage-1 projection.

## Ruling 3 — ⚑ "NO FLAG RESTORES THE OLD RULE" IS FALSE. THE COMMISSION IS WITHDRAWN BEFORE IT IS SPENT.

The report states: *"No flag restores the old rule: `texpass_iter` took the same port as an
opt-in mode, `project_twins` took it as a replacement,"* and proposes commissioning
`--edge-mode global`.

**Measured at this seat, in `tools/project_twins.py`:**

```
L103   ap.add_argument("--edge-absolute", action="store_true", ...)
L754   if args.edge_absolute:                  <- selects the pre-A3 path
L797   if not args.edge_absolute:              <- the A3 invariant check is SKIPPED in it
```

**The opt-in already exists and is exactly the one the report says is missing.** The
executor even quoted the comment that names it — line 738's *"in `--edge-absolute` mode"* —
in the course of reading the mechanism, and read past it.

**This is the third instance of one law in a single session**, and the second found inside a
report: *enumerate the resource before commissioning one — including when an executor has
already named it.* Its siblings today were `e12_offsurface.py` (E27 Ruling 2, nine flags
where a fresh instrument was proposed) and Qwen-Image-Edit-2511 (recommended before checking
it was already on the rig — it was). **The shape is always the same and it is always cheap
to check: one grep separates a commission from a flag that exists.**

**Consequently:**

- **No `project_twins` change is commissioned.** Gate 6 holds unbroken and the projection
  lane is not blocked on a tool arc.
- **The remedy is a re-run under the recorded era's flags**, which is anchor work, not tool
  work. `--edge-absolute` is the named candidate; **it is not ruled sufficient**, because
  W3's recorded run also predates other flags that gate the same stage —
  `--mask-keyed`, `--key-corner-median` and `--trust-intersect` are each an era switch on a
  path E08 rebuilt. Which combination reproduces the record is an **empirical question for
  the next seat**, settled by running it, not by me asserting it here.
- **If a flag combination does reproduce W3's recorded numbers, the anchor lands and the
  finding stands anyway** — that the *default* changed is the thing worth knowing, and the
  anchor is what will keep it visible.

## Ruling 4 — T34 IS A SINGLE SCALAR THAT TWO LIVE SEATS BOTH MOVE, AND THAT IS STRUCTURAL

The executor measured the problem exactly and refused to act on it, which was the dispatch's
instruction and the right call:

| tree | total | hermetic |
|---|---:|---:|
| HEAD at its halt | 790 | 761 |
| E30's commit alone | 801 | 761 |
| task 3's commit alone | 797 | 768 |
| **both landed** | **808** | **768** |

**No single number is correct for both seats' commits**, because T34 pins a stated count
against `pytest --collect-only` **of the tree the surfaces sit in**. Two parallel seats
adding tests cannot both be green independently — the second to land is red until someone
reconciles. That is a genuine structural limit of the pin, discovered by running it rather
than reasoned about.

**Resolved at this seat, now that both have landed**: 23 count sites updated to 808 across
eight READMEs, `SHIP_GATE.md`, `docs/advisor-kickoff.md`, `site-config.ts` and
`getting-started.md`, plus the **gap** figure 29 → 40, which the blanket total-replace did
not reach — the artifacts tier grew by E30's eleven, so total − hermetic moved even where
hermetic did not. `SHIP_GATE.md`'s lineage was checked rather than trusted: the historical
chain is intact and additive (`… → 790 → 808`), with only current-state clauses changed.
T34 and the claims sweep are green.

**The rule this earns, and it is the advisor's to carry, not an executor's**: *when two seats
are live, the count surfaces are the advisor's to reconcile after both land.* Neither seat
can be correct alone, so neither should be asked to try. This is why the dispatch reserved
`docs/experiments/README.md` — the reservation was right and was simply drawn one file too
narrow.

## Ruling 5 — P1's MISS IS A NEW SHAPE, AND IT EARNS A LAW

Predicted 11 anchorable, measured 8. **P4 and P5 hit exactly** — 4 not anchorable, on the
count *and* the stated reason; 0 anchors needed the pixel tier to decide.

The executor's own diagnosis is adopted verbatim because it is better than anything I would
have written: *"I checked whether each stage's artifacts exist, and all three projections
have every one. What they lack is an instrument that can still express the recorded rule."*

**Folded to CLAUDE.md: *existence of the operands is not replayability.*** Seventh
consecutive arc to miss on the unit/population family and a genuinely new member of it — the
population was real, every member was real, every member had the *property checked*
(artifacts present), and the prediction still failed because replayability needs a **second**
thing nobody enumerated: a tool that can still be asked the recorded question. Its siblings
in this family — the unit, the population, the unchecked property, the rarest clause of a
conjunction — are all one level away from this one.

P3's headline contradicting its own decomposition two paragraphs below is owned in the report
in place, which is the standard.

## What is NOT ruled here

- **Whether `--edge-absolute` (alone or with the other era flags) reproduces W3's recorded
  projection.** Empirical, next seat, one run per combination.
- **The galleon's and dragon's projections** — not run, correctly, once the lane halted.
- **Any `project_twins` change** — not commissioned, and Ruling 3 is why.
- **The polish work itself.** This arc built gates. Eight of a possible twelve stages across
  three subjects now have them; the four projections do not, and the polish lane for a
  subject opens when its gates do.

## The advisor's record, this ruling

The dispatch reserved `docs/experiments/README.md` from the executor and **should have
reserved the count surfaces too** — that omission is what put a knowingly-red T34 in front of
a seat that had done nothing wrong, and cost it a measurement pass to prove it was not at
fault. Ruling 4 fixes the rule going forward.

Against that: reading `project_twins.py` rather than accepting *"no flag exists"* saved a
tool-change arc on an accepted asset's route tool, which is the most expensive kind of arc
this repo runs.
