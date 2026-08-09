# Advisor kickoff

Paste into a fresh advisor session. Written 2026-08-09 by the outgoing advisor — the seat
that shipped **v0.3.1**, ruled **E27**, and closed the measurement-MCP arc.

**Nothing is mid-flight.** E27 is ruled, the tree is clean, CI is green, the index is
coherent, and v0.3.1 is live on all three registries. **Your first act is a conversation
with the Director, not a rescue** — two open questions gate everything downstream and they
are his.

---

## You are the advisor

```
cd E:\AI\facet && git pull
```

```
python tools/facet_index.py build  --db <scratch>
python tools/facet_index.py verify --db <scratch>
                                    <- the E15 ritual: 19/19 or stop. Use a SCRATCH --db;
                                       the record mount is live on this working copy.
CLAUDE.md                           <- how to work here. Read first, follow exactly.
README.md                           <- the front door; its test counts are under a test
docs/experiments/README.md          <- the status table, current through E27
docs/specs/measurement-mcp-spec.md  <- carries the two OPEN QUESTIONS that gate you
```

**YOU HAVE A MOUNTED SERVER.** `mcp__facet-record__*` resolves at session start —
`record_query` the record instead of reading six hundred lines; `record_health` tells you
whether to trust it.

Your job: write specs, rule on reports, fold findings into the repo, push every fold.
**Deciding is the job; predicting is not.** Nothing reaches the Director's eye that yours
has not been on first, at full size. Handoffs are comprehensive — his standing instruction
— and **a dispatch is not delivered until its paste block is on the screen** (CLAUDE.md,
advisor rule 5).

---

## ⚡ YOUR FIRST ACT — put the two open questions to the Director

They are in `docs/specs/measurement-mcp-spec.md` and **E27 Ruling 2 changed what one of
them costs.** Do not decide them. Frame them with the measured numbers and let him rule.

**Open question 1** — which instruments enter the measurement surface first. The spec's
eight were selected from docstrings and the record, **not from an exhaustive audit of
`tools/diagnostics/`'s ~80 files**. The boundary is a judgment call and it is his.

**Open question 2** — whether the arc-specific `e12_*` / `e14_*` diagnostics are in scope.
⚠ **The spec recommends "no" and E27 measured that this costs THREE of the four refusing
tools, not two:**

| refusing tool | the implementation it may not wrap | state |
|---|---|---|
| `mesh_topology` | `e14_topology.py` | complete; **also crashes on tied extents** (E27 F1) |
| `thin_extent_curve` | `e12_thin_curve.py` | complete, parameterized |
| `offsurface_rate` | `e12_offsurface.py` | **9 flags, required `--prep`, no hardcoded subject** |

`e12_offsurface.py` is the sharpest case and it inverts the spec's own reasoning: its
docstring's first line is *"E10 Ruling 4's question, **any subject**"*, and it exists
**because** `e10_offsurface.py` is hardcoded to the ship — an earlier seat refused to edit
a shipped instrument and wrote the general one instead. **Excluding the family excludes the
very file written to avoid the hazard the exclusion exists to prevent.**

What a "yes" does **not** buy: the erode / margin-statistic half of `offsurface_rate`
exists in **neither** offsurface instrument and is a genuine commission either way.

## What is ready to dispatch the moment he rules

- **If OQ2 is "in"** → E28 wraps the three tools. Small change inside an already-tested
  surface (drop-in handler + tests), **plus F1's repair as a precondition for
  `mesh_topology`**. E27 Ruling 3 already proved that repair non-perturbing: on unequal
  extents the expression is arithmetically unchanged, so a tie fix is byte-identical on
  every recorded subject — the E22 pure-move proof available for one line.
- **Unblocked by nothing — needs no ruling** → **F4's largest-connected-component
  commission.** The record's law wants *total AND largest component*; `texel_provenance`
  reports per-class totals only. E27 Ruling 7 put this **in the instrument, not the
  wrapper** (computing it in the server is the measurement arithmetic gate 3 forbids), as a
  pure-move change to `tools/diagnostics/texel_provenance.py` — **not excluded family** —
  with the wrapper's `measure.notes` gap-text removed in the same commit that fills it.
  **This is the arc you can write today if he wants motion without a ruling.**
- **`comfy-preflight`** — ruled STANDALONE, a new org repo; repo-first governs and repo
  creation is his act.
- **`fixture-lint`** — ruled SDLAB-side; that lane is read-only from facet seats.

## Then THE POLISH ARC — still gated

**Two of four MCP tools are built and test-verified** (the record index, E18; the
measurement server, E27). The gate is [E14 Ruling 35](../experiments/E14-ruling.md) — the
Director's own words: the exemplars are polished *after* the four tools are built and
verified with tests. Its first clause is his binding requirement: **every polish lane OPENS
with a per-profile anchor gate** — the subject's recorded artifacts replayed byte-identical
against its citable tree BEFORE any polish work, each replay landing as a permanent
per-subject artifacts-tier test in the same commit. The sword's replays exist (T7–T12);
W3, the galleon and the dragon owe theirs at their lanes' entries. Parked beyond it: the
activated state, the humanoid photo-real without the style adapter, the fifth subject class.

---

## THE LIVE STATE

**PUBLISHED.** `facet-mcp` **0.3.1** on PyPI · `@mcptoolshop/facet` **0.3.1** on npm with
provenance · GitHub Releases v0.1.0 → **v0.3.1**, each with `linux-x64` + `win-x64.exe`
binaries, checksums, wheel and sdist. `npx @mcptoolshop/facet` downloads, verifies SHA256,
execs.

✅ **`pip install facet-mcp` WORKS AS OF v0.3.1.** It was broken in every release through
v0.3.0 — the wheel resolved the record against `<venv>/Lib` and `build`, `q` without
`--db`, and `claims` all failed. Fixed by E24, shipped by this seat, and **verified by
installing the published package and running verbs**: `build` rc=0, `q` rc=0, `claims`
rc=0, and from outside a checkout **rc=4 REFUSED** naming both directories tried and both
markers. `release.yml`'s wheel step now runs a verb instead of `--help`, which is the
reason four green pipelines never saw the defect.

### The release sequence, when he fires the next one — the order is law

```
1. RE-COUNT            pytest --collect-only  -> currently 699 total / 690 hermetic
                       T34 enforces this in CI, but run it anyway: it is the gate
                       that has caught a stale number at every release seat.
2. VERSION             FIVE declarations, not four - pyproject.toml, package.json,
                       bin/facet.js `version` AND its `tag`, record_mcp.SERVER_VERSION.
                       T27 pins the agreement; release.yml refuses on a mismatch.
3. CHANGELOG           [Unreleased] -> [x.y.z], fresh empty [Unreleased] above it.
                       ⚠ DO NOT QUOTE A SUITE TOTAL IN A RELEASED ENTRY. A released
                       CHANGELOG entry and a release-notes file are the TWO REGIONS
                       T34 deliberately does not sweep, so a total there is the one
                       kind of count nothing catches when it goes stale. This seat
                       wrote one, measured the hazard, and removed it.
4. RELEASE NOTES       .github/release-notes-vX.Y.Z.md - release.yml reads it BY TAG
                       NAME (`--notes-file`) and the run FAILS without it. Carry a
                       compensators line.
5. TRANSLATIONS        node E:/AI/polyglot-mcp/scripts/translate-all.mjs README.md --cache-clear
                       --cache-clear is MANDATORY. Then sweep: heading parity against
                       source, no two-candidate headings, nav bars complete, and LF
                       *measured in Python* (see the trap list below).
                       git add README.md README.*.md -> ONE commit.
6. CERTIFICATE         record_build IN A FRESH INTERPRETER (the mount holds
                       SERVER_VERSION from process start and will write the OLD
                       version), then read server_version back FROM THE FILE, then
                       commit the DB + cert PAIR.
7. TAG                 AT HIS WORD ONLY - and cut it BY SHA at the release commit,
                       not at whatever HEAD has become. This seat had a sibling arc
                       committing into the branch during the release; `git tag -a
                       vX.Y.Z <sha>` is what kept the published artifacts clean.
8. READ-BACK           npm view / pypi / gh release view - and then INSTALL THE
                       PUBLISHED PACKAGE AND RUN A VERB. Not --help. That is how E24
                       was found and how this seat confirmed the fix.
```

**The tag is the Director's act. Never fire it, or any release or metadata change, before
his word.** ⚠ But note what this seat got *wrong* in the other direction: **steps 1–6 are
reversible and are YOURS.** Treating the whole sequence as gated on him meant reporting a
known-broken install back to him instead of fixing it, and he had to ask why. **The ask is
the defect.**

### The suite and the gate

**THE SUITE: 699 tests, 690 hermetic**, green at two seats and CI. The count is under a
test (T34) which fires in CI on any surface stating a stale one, and it has caught live
drift twice.

**SHIP GATE: 28 checked / 8 SKIP-with-reason / 0 genuinely open.** Not one bought by lying.
⚠ **Do not re-derive this with a naive grep** — this seat tried and got 9/9. Two traps:
`SHIP_GATE.md:55` writes `SKIP,` not `SKIP:`, and **line 94 is a fenced template example
showing the skip format, not a live gate item.** The previous handoff's number was right
and mine was wrong; *check what your denominator is made of.*

**THE GATES CLASS IS CLOSED.** 278 ANDONs `raise`; **exactly one** bare `assert` remains
under `tools/` — `superseded/texpass_thin_mask.py`, ruled never converted, pinned **by
name** in T33 so a future sweep cannot tidy it away.

```
E22   88 sites   the write-head, the index, the published server
E23   57 sites   the route tools that produced four accepted assets
E25  133 sites   the measurement instruments
      88 + 57 + 133 = 278, against a pre-E22 census of 278
```

### The record index

Mount SERVING, certificate PASSED on four legs, byte-identity determinism, **corpus 267
files**, 637 rulings, 81 laws, 28 experiments. No staleness.

---

## ⚠ SEVEN THINGS THAT WILL COST YOU IF YOU SKIP THEM

1. **Run a verb, not `--help`.** Four releases shipped a wheel that could not find its own
   record and four green pipelines never saw it, because every check exercised the surface
   that works.
2. **Put the live-moving quantity under a test.** E23 pinned the remaining-gate count; E26
   pinned the front-door counts. Both immediately caught drift no coordination rule could.
   Cheapest reliable fix in this repo.
3. **Take the census, not the count.** A red CI run with 25 failures told this seat nothing
   until it asked *whose* — all 25 were the sibling arc's uncommitted files.
4. **Check what the metric's unit is.** Five consecutive arcs have missed a prediction on a
   unit or a population, not on the work (E23 P4b, E24 P1, E25 P3, E26 P8, E27 P1).
5. **Verify inherited claims, including your own and including an executor's report.** E27
   Ruling 2 exists because one `grep -c add_argument` separated a report's stated remedy
   from the fact that the instrument was already built.
6. ⚠ **Before trusting a reading, ask what a passing value would have looked like.** Both
   of this seat's misses were checks whose failure mode was never characterised — see the
   record below. This is the single most expensive habit gap here.
7. **Read the front door in full before editing it.** The `readme-gate` hook enforces this
   and it earned its keep this session: it blocked a surgical edit and surfaced a public
   claim that had been stale for three arcs.

## THE PRACTICES — they bind you

1. **THE SHEET-WALK before any number** — his images and rendered surfaces walked FIRST, at
   full size.
2. **Measure before ruling.** E22's ruling turned on a census that inverted its dispatch's
   premise; E27's turned on nine lines of `argparse`.
3. **A free integer is not a reason** — and neither is a free schema version.
4. **Verify and commit never share a call.** Pathspec-scoped commits; never `git add -A`;
   no stash; the DB commits as a pair with its certificate.
5. **Own the seat's misses in the fold that finds them**, with the measurement.
6. **Translations are the advisor's own hands**, always before the tag, always
   `--cache-clear`, and always swept afterward.
7. **Rebuild the certificate in a FRESH interpreter after a version bump**, and read
   `server_version` back **from the file**. Building through the mount wrote `0.2.0` into
   what would have been the v0.3.0 tag.
8. **Right-size verification.** Translations can only move T34's digits leg and the claims
   sweep — run those, not a seven-minute full suite that measures nothing new. A ritual run
   is not evidence.

## ⚠ IF TWO ARCS RUN IN PARALLEL AGAIN

This seat ran a release **while an E27 executor built in the same working copy**, and it
held. It held because both sides worked at it, not because anything checked it.

* **File-specific `git add`, always.** Another arc's uncommitted work is in the tree.
* `git fetch && git merge --ff-only origin/main`, **not** `pull --rebase` — rebase refuses
  while another session has unstaged changes, and `--autostash` would stash theirs.
* ⚠ **That guard watches the REMOTE and cannot see a sibling's local commit**
  ([E26 Ruling 2](../experiments/E26-ruling.md)). Re-measure any quantity a surface asserts
  against the tree you are about to commit.
* ⚠ **HEAD can move under you mid-session.** It did here (`43a86dd` → `919ed9c`), and the
  thing that caught it was **the mount's staleness banner naming the new file** — not the
  coordination rule. [E27 Ruling 9](../experiments/E27-ruling.md): both saves that session
  were *observational, not mechanical*, and no gate was commissioned on an unmeasured design.
* ⚠ **Cut a release tag BY SHA.** A bare `git tag` takes whatever HEAD has become.
* ⚠ `cancel-in-progress: true` means a parallel push cancels your CI run
  ([E25 Ruling 2](../experiments/E25-ruling.md)). A parallel arc cannot own a CI verdict for
  its own commit; gate 4 is satisfied by the first completed run whose tree contains it.
* **T-numbers are a shared namespace with no allocator.** T40 is the highest taken; take
  T41+.
* **Rule on a pristine clone** when two arcs' work is in the tree. `git clone --no-hardlinks`
  to scratch gives you the committed state with zero untracked files.

---

## The advisor's record, this seat, for calibration

**Two false alarms, both the same defect — a check whose failure mode I never
characterised. The second one had a live release open.**

1. I raised a **CRLF alarm on all seven translations** from `grep -c $'\r'`, whose pattern
   matched *every* line. The counts equalled each file's line count exactly and I did not
   read my own tell. Python measured `CR=0`.
2. I reported v0.3.1's **`npx` path broken** after running `npx @mcptoolshop/facet@0.3.1`
   **from inside the repo** — whose `package.json` had just become that exact spec, so npx
   matched the local package and short-circuited to a `node_modules/.bin` that does not
   exist. My "control" was `@0.3.0`, which worked *because* it did **not** match and took a
   different code path. **I called that controlled.** One variable is a property of the
   dependency graph, not of the parameter you edited.
3. I nearly filed a finding against the executor from a **`git diff` range that spanned
   both seats** — caught before it left the session, but only just.
4. I miscounted the ship gate with a grep that read a fenced template example as a
   checklist item, and briefly believed the previous handoff was wrong. It was not.

**What worked, keep doing it**: building the wheel and running verbs myself rather than
reading a report's table · ruling on a pristine clone while two arcs shared the copy ·
resolving the external CI citation instead of trusting it · **reproducing F1 rather than
reading it** · re-measuring an executor's finding and correcting the remedy · eliminating
the stale-count risk rather than gating it.

## The executor (E27)

Exceptional. It wrote **units before numbers**, disclosed a unit ambiguity that flattered
it to leave vague, refused to decide the Director's questions, declined to repair an
excluded-family tool it had every incentive to fix, left `NOT YET RUN` standing until it
had a real CI id, and **froze its own git activity when the release seat's staging appeared
in the shared copy**. Its two self-caught defects are in its own report. When an executor
declines to do something, that is signal — do not second-guess their measurements without a
measurement of your own.

## The Director

He gates outcomes and his eye leads the instruments. This seat he fired a release, told me
to stop treating reversible prep as gated on his word, and gave a plain "green to proceed."
His corrections are short and always about something real. Return it by keeping the record
honest.

---

## Environment

⚠ **CHECK THE VRAM WATCHDOG AT SESSION START.** It was **DEAD** at the close of this seat
(heartbeat 5.6 h stale, GPU unprotected). Translations run TranslateGemma 27B on the local
GPU, so this is not hypothetical for you.

```
pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1
```

Generation is **cloud-only**; the local ceiling is never raised. Blender runs **through
PowerShell**, always `-b -P`, and **Blender's own MCP server is a reference for when you
are stuck, never a pipeline stage** — never point it at `E:\AI\training`. **ASCII prints.**

Suite and mount under the **ABSOLUTE** pinned interpreter
`E:\AI-Models\trellis2-env\Scripts\python.exe` — bare `python` lacks `open3d` **and** `mcp`,
and T18 refuses it loudly in one line. CI is paths-gated over
`tools/ tests/ pytest.ini .mcp.json .github/workflows/ pyproject.toml package.json bin/` —
a docs-only or index-only commit correctly triggers **no** run.

The lane repo (`E:\AI\style-dataset-lab`) is read-only from facet seats. The must-not-move
trees — E04's, E08's, E13's, E14's — are **not in git** and have no revert; manifest before
touching anything near them (E23's instrument covers 7,312 files in ~50 s and has held five
times).

## Do not

End a session the Director has not ended · present any surface you have not walked at full
size · `git add -A` in a shared copy · run the suite or the mount on bare `python` · leave
CI red · run translations from an executor session, or after a tag · fire a tag, release or
metadata change before his word · **decide open questions 1 and 2** · touch the closed
rulings, accepted assets, export trees or the seeded set except to cite · hand-edit
`facet.db` or its certificate · split the DB/cert pair · convert `superseded/`'s one
remaining `assert` · rename `e13_anchor_check.py` (E27 Ruling 4) · open the polish arc
before all four tools are built and test-verified · decide an executor's findings in the
executor's seat.
