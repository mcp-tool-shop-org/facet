# Advisor kickoff

Paste into a fresh advisor session. Written 2026-08-09 by the outgoing advisor, at the
close of **THE GATES ARC**: the seat that shipped **v0.2.0 and v0.3.0**, ruled **E22
through E26**, and closed the class that started as one bare `assert` in a report.

**Nothing is mid-flight. Both parallel arcs are ruled, CI is green, the tree is clean.**
Your first act is a dispatch, not a rescue.

## You are the advisor

```
cd E:\AI\facet && git pull
python tools/facet_index.py build --db <scratch> && python tools/facet_index.py verify --db <scratch>
                                    <- the E15 ritual: 19/19 or stop. Use a SCRATCH --db;
                                       the record mount is live on this working copy.
CLAUDE.md                           <- how to work here. Read first, follow exactly.
README.md                           <- the front door; its counts are under a test now
docs/experiments/README.md          <- the status table, current through E26
docs/experiments/E27-*              <- YOUR FIRST DISPATCH, written and ready to paste
```

**YOU HAVE A MOUNTED SERVER.** `mcp__facet-record__*` resolves at session start —
`record_query` the record instead of reading six hundred lines; `record_health` tells you
whether to trust it.

Your job: write specs, rule on reports, fold findings into the repo, push every fold.
**Deciding is the job; predicting is not.** Nothing reaches the Director's eye that yours
has not been on first, at full size. Handoffs are comprehensive — his standing
instruction — and **a dispatch is not delivered until its paste block is on the screen**
(CLAUDE.md, advisor rule 5; he had to ask twice before that line existed).

---

## ⚡ YOUR FIRST ACT — dispatch E27, the measurement MCP

It is written: [E27-measurement-mcp-kickoff.md](experiments/E27-measurement-mcp-kickoff.md),
with its paste block at the bottom of this file. **It is the last thing standing between
here and the polish arc**, which is the Director's named next milestone.

Four MCP tools were ruled ([placement-memo.md](specs/placement-memo.md), his words).
**One is built:** the record index (E18), now shipped on two registries. E27 is the
second, and the one the polish arc actually consumes.

```
index MCP        BUILT + SHIPPED    tools/record_mcp.py -> facet-mcp, @mcptoolshop/facet
measurement MCP  SPEC'D, UNBUILT    docs/specs/measurement-mcp-spec.md   <- E27
comfy-preflight  SPEC'D             ruled STANDALONE - a new org repo, repo-first governs
fixture-lint     SPEC'D             ruled SDLAB-side - coordinate with that lane
```

**Then THE POLISH ARC**, and clause 1 is the Director's binding requirement in his own
words: *"We're going to basically have to verify everything when we get to the polish
pass, one profile at a time."* Every polish lane OPENS with a per-profile anchor gate —
the subject's recorded artifacts replayed byte-identical against its citable tree BEFORE
any polish work, each replay landing as a permanent per-subject artifacts-tier test in the
same commit. **The sword's replays exist (T7–T12); W3, the galleon and the dragon owe
theirs at their lanes' entries.** Parked beyond it: the activated state, the humanoid
photo-real without the style adapter, the fifth subject class.

## THE LIVE STATE

**PUBLISHED.** `facet-mcp` **0.3.0** on PyPI · `@mcptoolshop/facet` **0.3.0** on npm with
provenance · GitHub Releases v0.1.0 → v0.3.0, each with `linux-x64` + `win-x64.exe`
binaries, checksums, wheel and sdist. `npx @mcptoolshop/facet` downloads, **verifies
SHA256**, execs.

⚠ **`pip install facet-mcp` is broken in every RELEASED version and fixed on `main`** —
E24 found it by running a *verb* instead of `--help`. **0.3.1 is unreleased and carries
that fix**, plus E23's, E25's and E26's work. The README says so on the front page.

### The 0.3.1 sequence, when he fires it — the order is law

```
1. RE-COUNT            pytest --collect-only  -> currently 648 total / 640 hermetic
                       T34 now enforces this in CI, but run it anyway: it is the gate
                       that has caught a stale number at every release seat.
2. VERSION             FIVE declarations, not four - pyproject.toml, package.json,
                       bin/facet.js `version` AND its `tag`, record_mcp.SERVER_VERSION.
                       T27 pins the agreement; release.yml refuses on a mismatch.
3. CHANGELOG           [Unreleased] -> [0.3.1], fresh empty [Unreleased] above it.
4. RELEASE NOTES       .github/release-notes-v0.3.1.md - release.yml reads it BY TAG NAME
                       and the run FAILS without it. Carry a compensators line.
5. TRANSLATIONS        node E:/AI/polyglot-mcp/scripts/translate-all.mjs README.md --cache-clear
                       --cache-clear is MANDATORY; then sweep the two-candidate headings
                       and check LF. git add README.md README.*.md -> ONE commit.
6. CERTIFICATE         record_build IN A FRESH INTERPRETER (the mount holds SERVER_VERSION
                       from process start and will write the OLD version), then read
                       server_version back FROM THE FILE, then commit the DB + cert PAIR.
7. TAG                 at his word only. release.yml then builds both binaries, cuts the
                       Release with checksums + wheel + sdist, publishes PyPI and npm.
8. READ-BACK           npm view / pypi / gh release view - and then INSTALL THE PUBLISHED
                       PACKAGE AND RUN A VERB. Not --help. That is how E24 was found.
```

**The tag is the Director's act.** Never fire it, or any release or metadata change,
before his word.

**THE SUITE: 648 tests, 640 hermetic**, green at two seats and CI. **The count is under a
test now** (T34) — it fires in CI on any surface stating a stale one, and it has already
caught a live drift nobody staged.

**SHIP GATE: 28 checked / 8 SKIP-with-reason / 0 genuinely open.** Not one bought by lying.

**THE GATES CLASS IS CLOSED.** 278 ANDONs raise; **one bare `assert` remains anywhere
under `tools/`** — `superseded/texpass_thin_mask.py`, ruled never converted, now pinned by
name in T33 so a future sweep cannot tidy it away.

```
E22   88 sites   the write-head, the index, the published server
E23   57 sites   the route tools that produced four accepted assets
E25  133 sites   the measurement instruments
      87 + 57 + 133 + 1 pre-existing = 278, against a pre-E22 census of 278
```

## ⚠ FIVE THINGS THIS SEAT LEARNED THAT WILL COST YOU IF YOU SKIP THEM

1. **Run a verb, not `--help`.** Four releases shipped a wheel that could not find its own
   record and four green pipelines never saw it, because every check exercised the surface
   that works. `release.yml`'s step is literally *"verify the wheel runs from a clean
   venv"* — and it ran `--help`.
2. **Put the live-moving quantity under a test.** E23 pinned the remaining-gate count; E26
   pinned the front-door counts. Both immediately caught drift no coordination rule could.
   **This is the repo's most reliable fix and it is cheap.**
3. **Take the census, not the count.** A red CI run with 25 failures told me nothing until
   I asked *whose* — all 25 were another arc's, and a blocked gate resolved on that fact.
4. **Check what the metric's unit is.** Four consecutive arcs missed a prediction on a
   unit, not a population (E23 P4b, E24 P1, E25 P3, E26 P8).
5. **Verify inherited claims, including your own.** Six of this seat's numbers were wrong
   and every one fell to a two-call measurement.

## THE PRACTICES — they bind you

1. **THE SHEET-WALK before any number**; his images and rendered surfaces walked FIRST, at
   full size.
2. **Measure before ruling.** E22's ruling turned on a census of two tool calls that
   inverted its dispatch's premise.
3. **A free integer is not a reason** — and neither is a free schema version.
4. **Verify and commit never share a call.** Pathspec-scoped commits; **never `git add
   -A`**; no stash; the DB commits as a **pair** with its certificate.
5. **Own the seat's misses in the fold that finds them**, with the measurement.
6. **Translations are the advisor's own hands, always before the tag**, always
   `--cache-clear`, and always sweep the two-candidate headings afterward.
7. **Rebuild the certificate in a FRESH interpreter after a version bump.** The mounted
   server holds `SERVER_VERSION` from process start; building through it wrote `0.2.0`
   into what would have been the v0.3.0 tag, and only reading the file back caught it.

## ⚠ IF TWO ARCS EVER RUN IN PARALLEL AGAIN

This seat ran three in one working copy. It worked — but because the disjointness happened
to hold, not because anything checked it.

- **File-specific `git add`, always.** Another arc's uncommitted work is in the tree.
- **`git fetch && git merge --ff-only origin/main`, not `pull --rebase`** — rebase refuses
  outright while another session has unstaged changes, and `--autostash` would stash
  *theirs*.
- ⚠ **That guard watches the REMOTE and cannot see a sibling's local commit**
  ([E26 Ruling 2](experiments/E26-ruling.md)). **Re-measure any quantity a surface asserts
  against the tree you are about to commit.**
- ⚠ **`cancel-in-progress: true` means a parallel push cancels your CI run**
  ([E25 Ruling 2](experiments/E25-ruling.md)). A parallel arc cannot own a CI verdict for
  its own commit: gate 4 is satisfied by the first *completed* run whose tree contains it,
  naming what else was in it. A red run for another arc's reason is **blocked, not failed.**
- **T-numbers are a shared namespace with no allocator.** T32 was claimed mid-dispatch.
- **Disjointness must be MEASURED.** I told the Director two arcs shared no files and was
  wrong — the claims sweep and the path resolver live in one file.

## The advisor's record this seat, for calibration

**The misses, worst first.** **I asserted disjointness without checking it** and offered
the Director a parallel pair that shares `facet_index.py`. **`docs/advisor-kickoff.md` —
this file — was stale by three releases**, the document whose own step 1 says RE-COUNT.
**My E26 enumeration was arithmetically right and structurally wrong**: `SHIP_GATE.md:61`
is one physical line carrying four current-state clauses and eight historical pairs, a line
I built that way, and I handed an executor a list of *sites* while demanding a rule a site
cannot express. **I wrote `README.md:47` claiming a broken wheel worked for `q` and
`claims` having run only `q`.** **My coordination rule had a hole I never tested.** **I
restated a scoped count as a population** inside the ruling convicting a dispatch of that
move. **A shell chain nearly skipped a commit** because `grep -c` returning 0 exits 1.

**What worked, keep doing.** Building a wheel and running verbs myself rather than reading
a report's table · ruling on a pristine clone when two arcs' work was in the tree ·
re-proving a pure move with my own instrument · taking failure *censuses* · sizing a routed
finding by planting all three notations rather than accepting or dismissing it · closing an
open spec question with one look at a mounted server.

## The executors

Exceptional, all four. E22 measured a census that inverted its own dispatch. E23 caught its
tier reddening for the wrong reason and repaired it before committing. E25's proof
instrument reported 10 where 0 was required and it noticed. **E25 and E26 both refused to
write a CI verdict they did not have**, and left `NOT YET RUN` standing. **When an executor
declines to do something, that is signal.** Do not second-guess their measurements without
a measurement of your own.

## The Director

He gates outcomes and his eye leads the instruments. This seat he fired three releases,
ruled Blender's MCP a reference and not a pipeline stage, and told me to stop making him
ask for paste blocks. **His corrections are short and always about something real.** He
also said thank you. Return it by keeping the record honest.

## Environment

Watchdog standing. Generation cloud-only. Blender through PowerShell — **and Blender's own
MCP server is a reference for when you are stuck, never a pipeline stage; never point it at
`E:\AI\training`** (CLAUDE.md, Environment). ASCII prints. **Suite and mount under the
ABSOLUTE pinned interpreter** `E:\AI-Models\trellis2-env\Scripts\python.exe` — bare
`python` lacks `open3d` AND `mcp`, and **T18 refuses it loudly in one line**. CI is
paths-gated over `tools/ tests/ pytest.ini .mcp.json .github/workflows/ pyproject.toml
package.json bin/`. The lane repo (`E:\AI\style-dataset-lab`) is read-only from facet
seats. The must-not-move trees — E04's, E08's, E13's, E14's — are **not in git and have no
revert**; manifest before touching anything near them.

## Do not

End a session the Director has not ended · present any surface you have not walked at full
size · `git add -A` in this shared copy · run the suite or the mount on bare `python` ·
leave CI red · run translations from an executor session, or after a tag · fire a tag,
release or metadata change before his word · touch the closed rulings, accepted assets,
export trees or the seeded set except to cite · hand-edit `facet.db` or its certificate ·
split the DB/cert pair · convert `superseded/`'s one remaining `assert` · open the polish
arc before all four tools are built and test-verified · decide an executor's findings in
the executor's seat.

---

## PASTE BLOCK — E27, the measurement MCP

```
cd E:\AI\facet
git fetch origin && git merge --ff-only origin/main
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py build --db <scratch>
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py verify --db <scratch>
                                     <- 19/19 or stop. Scratch --db: the mount is live.

CLAUDE.md                            <- how to work here. Read first, follow exactly.
docs/experiments/E27-measurement-mcp-kickoff.md   <- YOUR DISPATCH.
docs/specs/measurement-mcp-spec.md   <- THE CONTRACT. The dispatch does not restate it.
docs/specs/placement-memo.md         <- why this lives in facet, in the Director's words.

YOU ARE THE EXECUTOR. You measure and report; you do not decide what results mean.

FIRST ACT, before writing any tool: commit E27-predictions.md, blindness disclosed per row.
⚠ FOUR CONSECUTIVE ARCS MISSED ON A UNIT, NOT A POPULATION. Before each number, write
  down what ONE of the thing you are counting is.

THE BAR - this is a BUILD, not a conversion, so the pure-move bar does not apply:
  - Job-shaped tools. A tool answers a question, not "run script X".
  - THE SERVER WRAPS; IT DOES NOT RE-IMPLEMENT. Instruments live in tools/. If one needs
    behaviour that is not there, that is a FINDING - not a licence to write a second
    implementation of a measurement the record already cites. (Gate 3.)
  - A REFUSAL IS BETTER THAN A WRONG NUMBER. An instrument that cannot establish its
    precondition exits 4 = REFUSED and names what is missing, with a can-fail leg.
  - Tests ride the commit. Take T35+ (the T-number namespace has no allocator).

⚠ THE SPEC'S INSTRUMENT LAWS ARE BINDING, NOT DECORATION. Name the denominator. A hue
  carries its chroma. A statistic of angles is circular. Bbox-check a keyed mask against
  the geometry. Report the total AND the largest connected component. If a tool cannot
  honour one of these on some input, IT REFUSES ON THAT INPUT.

⚠ OPEN QUESTIONS 1 AND 2 IN THE SPEC ARE THE DIRECTOR'S. Do not decide them. Q3 is
  already CLOSED (ai-eyes-mcp is disjoint, measured).

⚠ FIXTURES ARE THE REAL WORK. The recorded trees are NOT in git and have no revert.
  Synthetic first - E18's tests/fixtures/selftest_min is the pattern. Anchors go in the
  artifacts tier. MEASURE which tools can be tested hermetically and REPORT THE SPLIT;
  E20's refusal to invent units that could not exist was that arc's largest deliverable.
  Manifest the recorded root before anything runs, re-check at the halt.

Halts at E27-measurement-mcp-report.md. The advisor rules at E27-ruling.md. No tag.
```
