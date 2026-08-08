# E21 — the installed CLI's operator contract

**Written by the advisor, 2026-08-08 (night), at the Director's word.** Dispatched to a
fresh executor session. Halts at `E21-cli-contract-report.md`; the advisor rules at
`E21-ruling.md`.

---

## The question

facet published two console scripts to two registries today. **Does the surface a user
installs honour the operator contract the ship gate asks of an installed command — and
where it cannot, is the reason a measured one rather than an inherited habit?**

Three `[cli]`/`[mcp]` gate items are **UNCHECKED, not skipped**, in
[SHIP_GATE.md](../../SHIP_GATE.md), because they apply and they are not done. They
became applicable the moment `shipcheck init` re-detected `[all] [npm] [mcp] [cli]
[pypi]` after the extraction. This arc closes them or rules them honestly closed-as-
skipped with evidence.

## What is already true — verify, do not assume

Every line below was measured on 2026-08-08. **Re-measure before designing around any
of it** — an inherited claim is a hypothesis wearing a fact's clothes, and this repo has
falsified six of its own in a single session.

| fact | how it was measured |
|---|---|
| `facet-index --help` → 0; `facet-index bogus-verb` → **2** | run against the installed console script in a clean venv |
| `facet-mcp --print-tools` → 0; `facet-mcp --bogus-flag` → **2** | same |
| the 2s are **argparse's** convention, which inverts the gate's 1 = user / 2 = runtime | `parser.error()` calls `sys.exit(2)` |
| nothing in either command partially succeeds | no verb has a partial-completion path |
| the MCP tool surface **already** implements `code`/`message`/`hint`/`retryable` | `RecordError`, validated against a closed `CODES` tuple, one wire site (`_raise`) |
| `record_build` already wraps unexpected exceptions into `INTERNAL` with no traceback | the other five tools rely on the framework envelope |
| an unexpected exception in `facet-index` surfaces a raw traceback | no `--debug` gate exists |
| there are no logging levels anywhere | deliberate, and the reason is in §"the tension" |

## Scope — and the scoping decision is RULED, not the executor's to widen

**In scope: the two published console scripts only** — `facet-mcp` and `facet-index`,
i.e. `tools/record_mcp.py` and `tools/facet_index.py`.

**Out of scope: the other 34 tools in `tools/`, all of `tools/diagnostics/`, and all of
`tools/superseded/`.** They are not published, they are the instruments that produced
four accepted assets, and several write into the must-not-move trees. Retrofitting an
exit-code registry across research scripts would be a large change to accepted-asset
tooling bought for a checkbox. **The `[cli]` tag applies to what facet installs, and
facet installs two commands.** If the executor believes a third file must change, that
is a finding for the ruling, not a scope extension.

## The three units

### U1 — the exit-code registry

Target: `0` ok · `1` user error · `2` runtime error · `3` partial success.

The obvious implementation is an `ArgumentParser` subclass overriding `error()` to exit
`1`, plus a top-level handler mapping unexpected exceptions to `2`. **Both commands must
agree**, and `record_mcp.py` must keep its stdio behaviour intact.

Three questions the executor must **measure and report rather than decide**:

1. **What exit code does a fired ANDON deserve?** A gate firing is the tool *working* —
   it is not a runtime error. It may deserve its own code, or `1`, or to be argued as
   out of the registry's model. E08 Amendment 32 is the governing ruling and it must not
   be weakened. Report the options with their consequences; the advisor rules.
2. **Is `verify` failing a `1`, a `2`, or a `3`?** A failed leg is a *measured outcome*,
   not an error in the tool. `record_claims` is already ruled to **never** return a
   failing code (E15 Ruling 9b / [E15-ruling.md](E15-ruling.md)) — that ruling binds and
   `claims` stays `0` whatever it finds.
3. **Does anything genuinely partial-succeed?** If nothing does, `3` stays unused and the
   report says so. **Do not invent a partial-success path to populate a code.**

### U2 — no raw tracebacks without `--debug`

An unexpected exception must surface as a structured, legible failure naming the next
step; `--debug` restores the traceback.

**The trap, and it is the one that matters:** `--debug` must never become a way to skip a
gate. E08 Amendment 32 exists because a shell chain walked past a fired ANDON and
committed 47,020 texels anyway — the ruled design is that the check lives *inside* the
tool **with no skip flag**. A `--debug` that changes *what runs* rather than *what is
printed* is a regression against a ruling. It affects presentation only.

### U3 — logging levels

Target: silent / normal / verbose / debug, secrets redacted at all levels.

**The tension is real and the executor must resolve it in the report, not paper over
it.** The standing reason for having no levels is that **stdout is the measurement
record** — a tool prints the numbers a report is written from, and suppressing them
behind a level would suppress the evidence. That argument was made for *research
scripts*. It is much weaker for a shipped stdio MCP server, where a quiet mode is
ordinary.

The likely honest shape: **levels govern progress and diagnostic chatter; they never
govern a measurement or a refusal.** A `--quiet` that hides an ANDON is the same defect
as a `--debug` that skips one. Propose the boundary explicitly and name which existing
prints fall on each side; the advisor rules the boundary before it ships.

Nothing sensitive is printed today (A3, swept), so redaction is a property to *state and
test*, not to build.

## The assertion law binds

**A test pins only anchored or accepted behaviour.** Where the current behaviour looks
wrong, that is a **finding for the ruling** — halt into the report, do not pin it and do
not "fix" it silently. Expect findings here: this is the first arc to look hard at a
surface that was never designed as a product.

## Tests ride the commit

A commit that changes tool code carries its tests in the same commit. Name them in the
report. The suite is at **T28**; this arc's tests start at **T29**.

At minimum:

- exit code per (command × outcome class), asserted on the **installed console scripts
  or a subprocess**, not by reading source
- a **can-fail leg** for every code: prove the assertion discriminates, or it is not a
  check. A test that cannot fail is this repo's most-repeated defect
- `--debug` changes only presentation: same exit code, same side effects, traceback
  present in one and absent in the other
- an ANDON still fires and still refuses **at every logging level**, including the
  quietest
- the frozen-binary path (T28's subject) is not regressed

## Gates — halt and report, never improvise past one

1. **Suite green** under the pinned interpreter before and after:
   `E:\AI-Models\trellis2-env\Scripts\python.exe -m pytest tests/`
2. **The MCP surface's structured errors are unchanged.** `BAD_ARGUMENT` on bad input,
   server stays up, `record_health` still answers. If a change to `main()` alters a tool
   result shape, HALT.
3. **The four version declarations still agree** — `pyproject.toml`, `package.json`,
   `bin/facet.js`, `record_mcp.py`'s `SERVER_VERSION`. This arc is a behaviour change to
   a published CLI, so it targets **0.2.0**, and `bin/facet.js` pins the *tag* it fetches
   binaries from as well as the version.
4. **No edit to** `canon/`, `profiles/`, the citable trees, the seeded set, closed
   rulings, or any tool outside the two named in scope.

## Out of scope

The 34 research scripts · `tools/diagnostics/` · `tools/superseded/` · the structured
error shape for `facet-index` beyond what U2 needs · the MCP JSON-schema per-parameter
descriptions (want 9) · extending `record_build`'s unexpected-exception wrapper to the
other five tools (want 10) · the three testability seams ([E20 Ruling 6](E20-ruling.md))
· P5 · anything touching the release workflow beyond a version bump.

## Predictions — committed BEFORE any internals are read

Write `E21-predictions.md` and **commit it before opening `record_mcp.py`'s or
`facet_index.py`'s `main()`**. Disclose per row whether the prediction was blind. A
hypothesis with no prediction cannot be wrong, and one that cannot be wrong teaches
nothing.

Predict at least: how many call sites change per command; whether argparse's `error()`
override is sufficient or whether subparsers need their own; whether any existing test
asserts an exit code that this arc will move (**check `tests/` for that before
predicting**); and whether a quiet mode can be added without touching a single line that
prints a measurement.

**E20's calibration lesson is live and it applies to you:** its three prediction misses
all predicted a defect in a function whose docstring carried the story of a bug it once
had. *A documented past bug is evidence an area is well-guarded, not evidence it is
fragile.* Predict quantities, not negligence.

## Standards compliance (this dispatch)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every fact in "what is already true" names how it was measured; the interpreter, the suite command and the four version sites are pinned literally |
| ANDON_AUTHORITY | 3 | four named halt gates; U1 and U3 both halt into findings rather than deciding; the E08 A32 no-skip-flag ruling is restated as binding on both `--debug` and `--quiet` |
| NAMED_COMPENSATORS | 2 | this arc performs no irreversible act — the release is a separate step at the Director's word. The compensator for a bad behaviour change is `git revert` plus a 0.2.1; scored 2 because stated, not exercised |
| DECOMPOSE_BY_SECRETS | 3 | scope is drawn by *what is published* rather than by directory convenience, and the reason is stated: the unpublished instruments produced the accepted assets |
| UNCERTAINTY_GATED_HUMANS | 3 | the three genuinely uncertain calls (ANDON's code, `verify`'s code, the quiet/measurement boundary) are explicitly the advisor's to rule, with the executor asked to report options and consequences |
| EXTERNAL_VERIFIER | 2 | the harness and CI verify the result, and exit codes are asserted through a subprocess rather than by reading source. skip: no cross-family LLM check — the outcomes here are deterministic integers |

## Environment

- Suite + mount under the **absolute** pinned interpreter
  `E:\AI-Models\trellis2-env\Scripts\python.exe`. Bare `python` lacks `open3d` and `mcp`;
  **T18 refuses it loudly in one line** — if you see that message, you used the wrong one.
- Shared working copy: **file-specific `git add`**, pathspec-scoped commits when foreign
  changes exist, **never `git add -A`**, no stash, and the DB + certificate commit as a
  **pair** at a session boundary only.
- Fold-marked test failures against a live-moving corpus: **run-then-rerun once**
  (E18 Ruling 2l). A second failure is real.
- CI is paths-gated and now includes `pyproject.toml`, `package.json`, `bin/**`. It also
  runs two dependency scanners — **never leave CI red**.

## Halt

Write `E21-cli-contract-report.md`: predictions scored, per-unit outcome, the three
ruled-to-the-advisor questions with options and consequences, findings under the
assertion law, tests added, and gates with their evidence. **Then stop.** The advisor
rules at `E21-ruling.md`; the release, if any, is a separate act at the Director's word.
