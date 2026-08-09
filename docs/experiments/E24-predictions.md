# E24 — predictions

**Executor, 2026-08-08.** Committed **before any source file was opened.** At the moment this
file was written the session had read, in this order: `CLAUDE.md`,
[E24-installed-paths-kickoff.md](E24-installed-paths-kickoff.md), [E23-ruling.md](E23-ruling.md),
and had run `facet_index.py build` / `verify` against a scratch DB (19/19, four legs). No file
under `tools/`, `tests/` or `.github/` had been read as source; the only knowledge of their
contents is the dispatch's own enumeration, which is itself **unverified at this point** and is
one of the things predicted below.

**Blindness is disclosed per row.** Three grades:

- **BLIND** — nothing about this was looked at; reasoned from the dispatch's prose alone.
- **INHERITED** — the dispatch asserts it and I am predicting it reproduces. Not blind, and not
  evidence either: an inherited claim is a hypothesis wearing a fact's clothes.
- **SIGHTED** — measured before writing. **There are no SIGHTED rows in this file.**

---

## The unit, declared before the numbers

E23's only clean miss was a prediction whose *population* was real and whose *unit* was not the
one the instrument measures. So the units are declared first, and the ones with a second
plausible reading carry both.

| quantity | the unit I commit to | the other reading, and why I rejected it |
|---|---|---|
| "consumers that change" | **an enumerated `file:line` site whose line text differs in the final diff** | *Sites whose behaviour changes* is the other reading, and its answer is **19 of 19 by construction** — the root's value moves, so every consumer's behaviour moves. A prediction that cannot be wrong teaches nothing. The textual unit can be wrong, so it is the one I commit to. |
| "the 19" | **consumers, excluding the definition.** The dispatch prints **20** `file:line` references under the heading *19 `REPO` consumers*; `facet_index.py:70` is labelled *(the definition)*, so 20 − 1 = 19 reconciles. | Counting the definition as a consumer gives 20 and makes the dispatch's own headline wrong by one. I predict the 19/20 split above is the intended reading, and I will report the count both ways. |
| "hermetic" | **the tier completes with no network available — build *and* install** | "no network at install time only" would let `python -m build`'s isolated build env download `setuptools` and still be called hermetic. That is the looser reading and I am not using it. |
| "T28's five pass unchanged" | **the five test functions' source is byte-identical AND they pass** | "they pass" alone would be satisfied by editing them until they do, which is the forbidden move. |

---

## The five the spec names

### P1 — how many of the 19 consumers change

**Prediction: 17 of 19.** Band **14–19**. **BLIND.**

Counted over the enumerated set rather than estimated as a density, per E23 Ruling 12:

| site | change? | reasoning (blind) |
|---|---|---|
| `facet_index.py` 281, 326, 345, 384, 389, 398, 845 | **7 × yes** | corpus-path readers. If the root can be *unresolved*, each needs a legible refusal rather than a `join(None, …)` TypeError. |
| `facet_index.py` 2072, 2084 | **2 × yes** | CLI plumbing near the verbs; same guard requirement. |
| `facet_index.py` 2188 (the `--db` default) | **yes** | today it defaults to a path that on a wheel **cannot exist**. That default has to become absent, not fabricated. |
| `record_mcp.py` 112 (re-export) | **yes** | it re-exports the thing being redefined. |
| `record_mcp.py` 119 (`DB_DEFAULT`) | **yes** | same defect as 2188, other module. |
| `record_mcp.py` 272, 275 | **2 × yes** | this is the marker check the hypothesis wants promoted into the resolver; promoting it edits it. |
| `record_mcp.py` 312, 494, 495, 890, 891 | **3 of 5 yes** | corpus readers; I expect a minority to sit inside a scope that has already refused. |

**The fork that decides this number, stated before I know which way it goes.** Two designs
satisfy the three ruled constraints and differ by an order of magnitude:

- **(a) route every site through a resolver call** that raises `4 = REFUSED` — ≈19 of 19 change.
- **(b) keep a module-level constant and add refusal guards at verb entry points** — ≈4 of 19
  change, and the risk moves to *finding every entry point*, which is the failure mode the
  enumeration exists to prevent.

I predict **(a)**, at ~65%, and 17 is where that lands. If it comes back ≈4, my miss is that I
read *"a root cause has as many sites as it has callers"* as a claim about the diff when it is a
claim about the **search**.

### P2 — does any consumer want a different root than the others?

**Prediction: NO for the corpus root — all 19 want the same one. But the set is not homogeneous:
2 of the 19 (`facet_index.py:2188`, `record_mcp.py:119`) want a *derived DB path*, not a corpus
root, and they must be able to end up unset while the corpus root refuses.** **BLIND.**
Confidence on NO-different-root ~85%.

**The consequence I predict falls out of that split:** a wheel user running
`facet-index q --db <a real index>` must still work — the dispatch's own table records it
working today — and `q` needs no corpus. So **the refusal cannot fire at import time**, or
`q --db` and `--help` die with it. Confidence that deferred refusal is forced: ~80%. If this is
wrong, the resolver is far simpler than P1 assumes and P1 goes with it.

### P3 — is the marker present in a built wheel?

**Prediction: NO. `CLAUDE.md` is absent from the wheel; the wheel carries `facet_index.py`,
`record_mcp.py`, two console scripts and `dist-info/`, and nothing else.** **INHERITED** — the
dispatch measured this on the **published** 0.3.0 wheel and told me not to re-derive it, then
told me to verify it anyway. I am predicting it reproduces on a wheel **built from this tree**,
which is a different object from the published one and is the one the new tier will actually
test against. Confidence ~92%; the 8% is `pyproject.toml` having gained a data-file rule since
0.3.0 was cut.

### P4 — do T28's five frozen tests pass unchanged on the first attempt?

**Prediction: YES.** Confidence ~70%. **BLIND.**

The frozen branch is selected by a different predicate than the wheel branch, and the fix adds
a candidate search rather than removing that predicate. **The 30%, named:** those five may pin
the *mechanism* rather than the behaviour — monkeypatching a module-level `REPO`, or asserting
the literal `dirname(dirname(__file__))` shape — in which case design (a) breaks them by
construction and **constraint 3 forces design (b)**. This is the row most likely to change the
shape of the whole fix, and it would take P1 down with it.

### P5 — can the new installed-wheel tier be hermetic?

**Prediction: NO under the declared unit (no network for build *and* install). Partially:
hermetic for the `facet-index` half, not for the `facet-mcp` half.** **BLIND.**

`python -m build` provisions an isolated build environment from PyPI unless `--no-isolation`;
`pip install <local wheel>` resolves `mcp>=2.0.0` from the network unless `--no-deps`, and with
`--no-deps` the venv has no `mcp`, so a `facet-mcp` verb cannot run in it. A wheelhouse or
`--find-links` pointed at the pinned env's own `mcp` is the way out and I predict I will need
one.

**Sub-prediction, separable: `python -m build` is NOT present in the pinned interpreter** —
~60% absent. If absent I report it and do not install it silently, per the dispatch.

**Predicted tier marking: `artifacts`, not the hermetic set.** Confidence ~75%.

---

## Four more, on record because they can be wrong

### P6 — does the new tier fail on the broken tree? (gate 3)

**Prediction: YES, by construction rather than by luck** — the verb will be one the dispatch
already measured as `RUNTIME_ERROR` on the published wheel. Confidence ~90%. **BLIND as to which
verb; INHERITED as to the failure.** The 10% is the tier failing on the broken tree for the
**wrong reason** — venv plumbing rather than root resolution — which would make it a gate that
passes while proving nothing. I will have to separate those two failures explicitly, and I
predict I will need a distinguishing assertion on the error text rather than on the exit code
alone.

### P7 — does the 19-consumer enumeration verify?

**Prediction: it reproduces exactly in the two named files — 20 line references, 19 consumers
plus the definition, none missing and none stale.** Confidence ~75%. **BLIND.** For it: E23's
ruling records that every scope number in that dispatch reproduced to the digit. Against it: the
two arcs before that were both defeated by a scope number, and this enumeration was produced
during a release read-back rather than a scoping pass.

**Separately: I predict ≥1 `REPO` reference exists OUTSIDE the two named files** — most likely
in `tests/`, plausibly under `tools/diagnostics/`. Confidence ~65%. That would not contradict
the enumeration, which is scoped to the two files, but it is exactly the *find its other
consumers* case, and it decides whether **gate 4** (no edit outside the four named files) can
hold. Per the dispatch, that is a report-and-route, not an executor's pick.

### P8 — the suite baseline

**Prediction: 370 reproduces, artifacts tier, before any edit.** **INHERITED** — from the
dispatch and from E23's ruling, which measured 370 at that seat. Confidence ~85%; the 15% is the
fold commits since E23 having moved it.

### P9 — tests added by this arc

**Prediction: 6–9 new test functions in one new file** (a T32 for the installed-wheel tier),
plus a can-fail leg for the resolver and a `$FACET_INDEX_DB`-through-subprocess leg that may
land in the existing CLI-contract file rather than the new one. **BLIND.** Confidence on "one
new file" ~70%.

---

## What would make me wrong in a way worth recording

Ranked by how much it would change the arc:

1. **P4 goes NO** — T28 pins the mechanism, constraint 3 forces design (b), and P1 collapses
   from 17 to ~4. One prediction overturning another is the shape to watch for here.
2. **P2's deferred-refusal consequence is wrong** — if refusal *can* fire at import time without
   killing `q --db`, the resolver is much simpler than P1 assumes.
3. **P7's second half hits** — a `REPO` consumer outside the two named files puts gate 4 and the
   scope in tension, and that is a routing, not a fix.
