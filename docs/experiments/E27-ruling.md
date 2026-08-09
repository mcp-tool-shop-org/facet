# E27 — the advisor's ruling

**Ruled 2026-08-09.** Report: [E27-measurement-mcp-report.md](E27-measurement-mcp-report.md).
Predictions: [E27-predictions.md](E27-predictions.md). Dispatch:
[E27-measurement-mcp-kickoff.md](E27-measurement-mcp-kickoff.md). Contract:
[measurement-mcp-spec.md](../specs/measurement-mcp-spec.md).

**Every load-bearing claim below was re-measured at this seat rather than read.** Where a
ruling rests on the executor's number, it says so and names the check I ran.

---

## Ruling 1 — THE ARC IS ACCEPTED

The measurement MCP exists, serves the spec's eight names exactly, wraps four instruments,
refuses four with structured errors, and carries the identity envelope the spec makes its
central contract.

Re-measured here, not inherited:

| claim | my check | result |
|---|---|---|
| suite green after | full run, this seat | **684 passed, 405.83 s, exit 0** |
| gate 3 — no instrument re-implemented **or edited** | `git diff --name-status 9940226..b5a8c0f -- tools/` | **`A tools/measure_mcp.py`** and nothing else |
| `facet_index` / `record_mcp` untouched | same range, path-scoped | empty diff |
| CI citation (E23's fabricated-citation law) | `gh run view 31299692852` | real, `a30fea2`, success, **both scanner steps green** |
| the recorded anchor | read the cited source and ran the test | E12-task2-report.md lines 32/76/79 carry 3,240,510 · 1,358,656 · 1,635,304 · 50.46%; the test asserts all four |
| the anchor is not a silent skip | `pytest -rs` on T37 | **6 passed, zero skips** |
| count surfaces are digit-only | diff of all eight surfaces | digit-only, lineage correctly extended |

The anchor deserves its own line. It calls the **served** tool against the recorded
`facet_next/E12_prep` with E12's own floors, pins the instrument path, and carries a
non-vacuous guard (`twin_front + twin_back > 0`). E12's 50.46% was **pre-registered and
falsified Q5 against itself**, so it is a real anchor rather than a number fitted after the
fact. *The wrap is proven not to change the instrument, which is the one thing it exists
not to do.*

Two of the executor's own defects were caught by its own tests on first run, and it said
so. That is the harness earning its place in the same commit.

---

## Ruling 2 — OPEN QUESTION 2 FORCES **THREE** TOOLS, NOT TWO, AND THE THIRD ONE'S INSTRUMENT IS ALREADY BUILT

**F5 undercounts and F2's remedy framing is wrong.** Measured at this seat:

```
e12_offsurface.py   9 add_argument, --prep REQUIRED, --aspect --margin --fit-axis
                    --v-ext --sample --seed --out.   NO hardcoded subject.
```

Its own docstring, first line: *"Does a prep bake's position map lie ON the mesh? E10
Ruling 4's question, **any subject**."* And immediately after: *"WHY THIS FILE EXISTS AND
WHY IT IS NOT `e10_offsurface.py`"* — because e10 is hardcoded to the ship, and *"rather
than edit a shipped instrument whose numbers are cited in a closed ruling, this carries
the bake half … with the subject supplied by flags."*

So `offsurface_rate`'s core question **already has a complete, parameterized,
subject-independent instrument**, written by an earlier seat for precisely the reason F2
identifies. It is blocked by exactly one thing: it is `e12_*`, and open question 2 is the
Director's.

The report named `e12_offsurface` as "the erode/margin form … excluded" and stopped there.
One `grep -c add_argument` separates that sentence from this ruling. **This is the repo's
own law — *before building a path to a resource, enumerate the resource* — and it is
recorded as the advisor's recurring failure shape, so finding it in an executor's report
is a correction, not a demerit.** The executor's core observation (e10 is not invocable) is
exactly right; only the remedy was mis-framed.

**What the commission actually is, now narrowed.** The spec asks `offsurface_rate` for the
bake question *"with the erode test, reported as a margin statistic."* Measured: `erode`
appears in **neither** offsurface instrument (e10 nor e12); `--margin` in e12 is the
*camera framing* margin, a different quantity entirely. So:

- the **bake half** — commission **nothing**, it exists, gated on OQ2 alone;
- the **erode / margin-statistic half** — a genuine commission, and a much smaller one
  than "parameterise e10 or write a fresh instrument."

**Consequence for the Director's question.** Ruling the `e12_*`/`e14_*` family in moves
**three** of the four refusing tools, not two. That materially changes the trade the
question asks him to make, and it is why this ruling re-measured rather than restating F5.

---

## Ruling 3 — F1 IS CONFIRMED AT THIS SEAT, AND ITS REPAIR IS PROVABLY NON-PERTURBING

Reproduced independently, not read:

```
python tools/diagnostics/e14_topology.py --glb tests/fixtures/measure_min/meshes/cube.glb
  [topo]   SHELLS (shared-vertex, = mesh_stats) 1 | largest 1.000000 | satellites 0
  IndexError: index 3 is out of bounds for axis 0 with size 3     (line 187)
```

`thin = argmin(ext)`, `tall = argmax(ext)`, `wide = 3 - thin - tall`; on tied extents
argmin == argmax, so `wide == 3`. Every E14 subject had unequal extents, so it never fired
in its own arc.

**Not repaired in this arc — correct.** But the repair is cheaper and safer than the report
implies, and that is worth ruling now so the next seat does not re-derive it: **on unequal
extents the expression is arithmetically unchanged**, so a tie-handling repair is provably
byte-identical on every recorded subject — the same pure-move proof E22 used for its 88
conversions, available here for one line. When OQ2 is ruled in, the repair is a
precondition for `mesh_topology` and it is a small, provable change.

The same run corroborates **P5 for free**: the tool prints
`SHELLS (shared-vertex, = mesh_stats)` — its own output states the definitional agreement
the executor measured, and it prints *before* the crash site, so the census stands.

---

## Ruling 4 — F3 IS CONFIRMED; THE COLLISION IS DOCUMENTED, NOT RENAMED

`tools/diagnostics/e13_anchor_check.py` opens: *"E13 — the SPIRAL LAW's guard, run before a
brush opens on a job."* It is the painted-adjacency instrument. It is **not** the
anchored-regression pattern the spec's `anchor_check` names.

**The file is not renamed.** Its numbers are cited in closed rulings and its name appears
in the record; renaming it to tidy a collision would break citations to fix a cosmetic
problem. **The spec's tool keeps the name `anchor_check`** — it is the right name for the
job — and the collision is carried where a future session will actually hit it: in the
refusal text, which already names the real file and is pinned by a test that asserts that
file exists (T40). That pin is the part that matters; if anyone moves either file, the test
fails and the text is updated deliberately.

Folded into the spec by this ruling so the next reader meets it before the code does.

---

## Ruling 5 — P1's MISS IS THE FIFTH CONSECUTIVE UNIT/POPULATION MISS, AND ITS SHAPE IS NEW

Predicted 6 of 8 hermetic (band 5–7), measured 4. The executor's own diagnosis is right and
I adopt it: *"I predicted testability of tools whose blocker is that they cannot exist yet."*

The four prior instances (E23 P4b, E24 P1, E25 P3, E26 P8) were about a **denominator's
unit** or a **population's membership**. This one is a level below both and has not appeared
before: the population was real — the eight names are the spec's contract — and each member
was real. What was not real was an **implicit property** the prediction attributed to every
member: *that each one has an instrument to be hermetic about.*

**The law this earns**, folded to CLAUDE.md: *a prediction about members of a real
population still fails if it assumes a property none of them was checked for. Before
predicting how a set behaves, check that the behaviour is defined for every member.* The
dispatch's ritual — write what one of the counted thing **is** before the number — kept
every population honest and is why the miss is legible at all. It did not ask what one of
them **has**.

---

## Ruling 6 — P2's DISCLOSED UNIT AMBIGUITY: THE OPERATIONAL READING GOVERNS, AND THE SCORE DOES NOT MOVE

The executor disclosed that its own unit did not decide the boundary case
(`offsurface_rate`), and reported **both** readings — 3 strict, 4 operational — noting both
land in band. Disclosing rather than picking the flattering one is exactly right.

**The operational reading governs from here**: an instrument that exists but cannot be
invoked on arbitrary input does **not** expose the behaviour, so it counts as behaviour
`tools/` does not expose. The unit's purpose is to tell a builder what they must build; a
module whose subject is three hardcoded absolute paths tells them nothing.

**This changes no score.** Both readings were in band before I chose, so this is resolving
an ambiguity for future arcs, not retuning a condition after seeing its result — the one
move that is always wrong. Stated explicitly because the distinction is the whole of the
rule.

---

## Ruling 7 — F4's LARGEST-COMPONENT GAP IS COMMISSIONED, AND IT BELONGS IN THE INSTRUMENT

The record's law is *report the total **and** the largest connected component* — two
thresholds separate one wrong garment from ordinary speckle. `texel_provenance` reports
per-class totals only.

**Naming the gap in the payload rather than computing it was the correct call**, and gate 3
is why: computing a connected-component census in the wrapper is new measurement
arithmetic in a server whose entire contract is that it contains none.

**The commission goes to the instrument, not the wrapper**, and it is its own arc — a
`tools/diagnostics/texel_provenance.py` change under the pure-move discipline (add an
output, change no existing number), with the wrapper's `measure.notes` gap-text removed in
the same commit that fills it. Not this arc's work and not the wrapper's.

---

## Ruling 8 — F6: `measure_mcp.py` STAYS OUT OF THE WHEEL, AND THAT IS THE DEFAULT, NOT A DEFERRAL

`py-modules` lists `facet_index` and `record_mcp`; the measurement server versions itself
independently at `facet-measure 0.1.0`. Correct, and it stays that way until the Director
rules otherwise.

The reason is the spec's own: **instrument identity is the product**. The moment
`facet-measure` is published, its version boundary becomes a comparability boundary for
every number it has produced — and it has produced exactly one recorded anchor so far.
Shipping it before the polish arc has used it would freeze a surface nobody has exercised
against real work. Publishing is a decision to make **after** four exemplars have been
measured before-and-after, not before.

---

## Ruling 9 — THE TWO SEATS HELD, AND THE COORDINATION HOLE IS NOW MEASURED FROM BOTH SIDES

E26 Ruling 2 found that `--ff-only` watches the remote and cannot see a sibling's local
commit. This arc ran that risk live, in both directions, and both seats handled it:

- the executor **froze git activity** when the release seat's staging appeared, sequenced
  after it, and said so in its report and its commit message;
- the release seat used file-scoped adds only, and **had HEAD move under it mid-session**
  (`43a86dd` → `919ed9c`) — caught not by the coordination rule but by the mount's
  staleness banner naming `E27-predictions.md`.

**Both saves were observational, not mechanical.** One seat watched a directory; the other
was told by an unrelated health surface. Neither is a mechanism, and the next pair may not
be watching.

**What this ruling can honestly say**: the hole is real, it is now instanced twice, and the
remedy is *not* a wider `--ff-only`. It is that **a quantity a surface asserts must be
re-measured against the tree being committed** — which both seats did, and which is why
nothing broke. That rule already exists in CLAUDE.md; this arc is its second confirmation
and the first from both sides at once. No new mechanism is commissioned, because I do not
have a measured design for one and inventing a gate here would be the shape of error this
repo names most often.

The tag's cleanliness is a fact rather than a hope: `v0.3.1` sits at `9940226`, and
`git merge-base --is-ancestor v0.3.1 HEAD` confirms E27's commits landed **after** it. The
published artifacts contain no in-flight work.

---

## What is NOT ruled

- **Open question 1** (which instruments enter the surface first) and **open question 2**
  (whether `e12_*`/`e14_*` are in scope) — **the Director's**, untouched by this ruling
  except to correct the count: OQ2 moves **three** tools, not two (Ruling 2).
- **Whether `facet-measure` ships** — his, and Ruling 8 says why the default is "not yet."
- **The erode/margin-statistic half of `offsurface_rate`** — commissioned in principle,
  unscoped here.
- **The polish arc** — its entry gate is unchanged and is his clause: every lane opens with
  a per-profile anchor gate before any polish work.

## Release

**Nothing here is released.** `v0.3.1` shipped from this seat before E27 landed and does
not contain it. `measure_mcp.py` is not in the wheel (Ruling 8). The next release is the
Director's act as always.

---

## The advisor's record, this arc

**Two false alarms, both the same defect, and the second one cost real time.**

1. I raised a CRLF alarm on all seven regenerated translations from `grep -c $'\r'`, whose
   pattern matched **every** line. The counts (153, 153, 174 …) equalled each file's line
   count exactly and I did not read my own tell. Python measured `CR=0`; the files were LF
   throughout and the guarded rewrite never fired.
2. I reported the v0.3.1 `npx` path **broken** after `npx @mcptoolshop/facet@0.3.1` failed
   — having run it **from inside the repo**, whose `package.json` had just become
   `@mcptoolshop/facet@0.3.1`, so npx matched the local package and short-circuited to a
   `node_modules/.bin` that does not exist. Worse, I called the comparison controlled: my
   "control" was `@0.3.0`, which worked *because* it did **not** match the local version and
   therefore took a different code path. **One variable is a property of the dependency
   graph, not of the parameter you edited** — this repo's own law, and I broke it while
   holding a live release open.

Both are the same shape as the errors this repo keeps recording: *a check whose failure
mode was never characterised*. The remedy is the one already written down — before trusting
a reading, ask what a passing value would have looked like.

**What went right at this seat**: building the wheel and running verbs rather than reading
a table; ruling on a pristine clone while two arcs shared the copy; resolving the external
citation instead of trusting it; reproducing F1 rather than reading it; and catching my own
wrong `git diff` range before it became a finding against the executor.

**The executor**: exceptional. It wrote units before numbers, disclosed a unit ambiguity
that flattered it to leave vague, refused to decide the Director's questions, declined to
repair an excluded-family tool it had every incentive to fix, and left the CI row
`NOT YET RUN` until it had a real id. When it declines to do something, that is signal.
