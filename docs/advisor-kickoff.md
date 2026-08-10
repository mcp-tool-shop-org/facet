# Advisor kickoff

Paste into a fresh advisor session. **Written 2026-08-10 by the outgoing advisor** — the seat
that ruled **E29** and **E31**, ruled comfy-preflight's first two builds, fixed the packaging
defect E31 found, and **shipped v0.4.0**.

**Rewritten from measurement, not edited.** Every number below was re-measured at the close.
[E26 Ruling 4](experiments/E26-ruling.md) caught a predecessor stale by three releases — on
the very document whose step 1 reads *RE-COUNT* — so nothing here is carried forward unchecked.

**Nothing is mid-flight.** Tree clean at `1e30db3`, **0 ahead of origin**, tag `v0.4.0`
pushed, CI and Pages green, index coherent, no seat running.

---

## You are the advisor

```
cd E:\AI\facet && git pull
```

```
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py build  --db <scratch>
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py verify --db <scratch>
                                     <- the E15 ritual: 19/19 or stop. SCRATCH --db;
                                        the record mount is live on this working copy.

CLAUDE.md                            <- how to work here. Follow exactly. The prediction
                                        family is now NINE members and it is still what
                                        keeps biting.
README.md                            <- the front door; its counts are under a test
docs/experiments/README.md           <- the status table, current through E31
docs/concept-prep.md                 <- stage 0: what it IS and what it has NOT been
                                        shown to do. Both, unsoftened.
```

**YOU HAVE TWO MOUNTED SERVERS NOW.** `mcp__facet-record__*` and — new since v0.4.0 —
`mcp__facet-measure__*`, eight tools. `record_health` tells you whether to trust the first.
The measurement server was reachable by **no session at all** until E29 Ruling 7; if it is
missing from your tool list, check `.mcp.json` before concluding anything.

Your job: write specs, rule on reports, fold findings into the repo, **push every fold**.
**Deciding is the job; predicting is not.** Nothing reaches the Director's eye that yours has
not been on first, at full size. **A dispatch is not delivered until its paste block is on the
screen** (advisor rule 5) — and that includes the arcs listed below.

---

## ⚡ YOUR FIRST ACT

**Nothing is broken and no conversation is owed.** v0.4.0 shipped clean. Two correctness items
are **ruled, commissioned and unscoped** — they are the natural next arc, and the first one
gates his polish lanes:

1. ⛔ **`anchor_check` PASSES SILENTLY WITHOUT PIL, and it is the polish arc's entry gate.**
   `tools/verify/anchor_compare.py:101-106` imports PIL **inside** the `try`, and
   `except Exception` catches `ModuleNotFoundError` identically to a decode failure. Without
   PIL it reports *"one or both inputs do not decode as images"*, blames the caller's PNGs,
   degrades to **byte tier only** and **exits 0**. Byte-tier-only is the exact configuration
   that produced two false halts here — it is why [E28 Ruling 14](experiments/E28-ruling.md)
   built the pixel tier, and [E30](experiments/E30-ruling.md)'s W3 halt was *confirmed* by
   that tier. **Ruled** ([E31 Ruling 5](experiments/E31-ruling.md)): a missing dependency is
   an environment **refusal**, exit `4`, not a per-input decode result — with a test that
   installs without PIL. ⚠ It does not bite on this rig (PIL 12.2.0 present) and has touched
   no recorded number.

2. **The identity envelope records no dependency set** ([E31 Ruling 3b](experiments/E31-ruling.md)),
   and this stopped being theoretical during the release: **four of the eight instruments need
   `open3d`, every open3d-dependent number here was measured against `0.19.0+241aaee`, and the
   devel channel moved to `+63e30be` while we worked.** The envelope carries server version,
   instrument sha256 and config hash — *and nothing about what the instrument imported*.
   Nothing recorded is withdrawn; a comparability component is named.

3. **THE ARCHIVE-TO-`D:` ARC — still unwritten**, and it is the one queued arc that never got
   a spec. Scope measured below.

## THE LIVE STATE — every figure re-measured at the close

| | |
|---|---|
| HEAD | `1e30db3`, working tree **clean**, **0** ahead of origin, tag `v0.4.0` on it |
| CI | **green** — [`31347712983`](https://github.com/mcp-tool-shop-org/facet/actions/runs/31347712983) on `main`; the Release run [`31348324862`](https://github.com/mcp-tool-shop-org/facet/actions/runs/31348324862) succeeded on all three jobs |
| suite | **THE SUITE: 891 tests, 851 hermetic** (40 artifacts), green at two seats and CI. ⚠ That phrasing is **pinned by T34** — preserve its shape if you rewrite this row |
| highest T-number | **T63.** Take T64+ |
| published | `facet-mcp` **0.4.0** (PyPI) · `@mcptoolshop/facet` **0.4.0** (npm, provenance) · Release `v0.4.0` with both binaries, checksums, wheel, sdist |
| `pip install` | **works, and now carries the measurement server** — verified by installing the *published* package and running a measurement verb, not `--help` |
| measurement server | **`facet-measure` 0.4.0, serving 8 of 8** from a checkout; **4 of 8 from a clean install on 3.13**, 8 of 8 on 3.11/3.12. `MEASURE_VERSION` is INDEPENDENT of the package version and not in T27's set |
| ship gate | **28 checked / 8 SKIP-with-reason / 0 genuinely open** |
| gates class | **closed.** 278 ANDONs `raise`; **exactly one** bare `assert` remains under `tools/` — `superseded/texpass_thin_mask.py`, ruled never converted, pinned **by name** in T33 |

### The record index

Mount SERVING, certificate PASSED on five legs, byte-identity determinism.
The record holds 31 experiments. No staleness. **Every other count lives in the ritual's own
output and in `record_health` — read them there, not here.** *(This line once quoted corpus,
ruling and law totals; they went stale within a day, twice, because nothing sweeps this file
for them and every fold moves them. **The experiment count stays because T34's fourth leg
pins this exact sentence.** Preserve the sentence shape when you edit this file.)*

### The arcs

**E27, E28, E29, E30 and E31 are all ruled and closed.** Four accepted assets unchanged.

⚖ **Director's rulings, 2026-08-09/10:** **both reconstruction paths are KEPT** — *"they both
are great… keep them both as options"*; the concept mesh gives realistic relief for detailed
sprites, the clay gives uniformity, and **stage 0 is a per-subject choice, not a replacement**
([E29 Ruling D1–D3](experiments/E29-ruling.md)). His named lever for the next stage-0 arc is
in his own words: *"could be better if the clay was made to be more detailed."*
⚠ **Its cost, scoped and NOT built:** an asset must record **which stage-0 path made it**, or
it cannot be reproduced. That is a provenance field, not an architecture.
⚠ **And the canon question is OPEN**: the two meshes differ in **horn shape, muzzle and brow**.
He accepted both *as meshes*; nothing says they are the same character, and
[E08's canon ruling](experiments/E08-director-canon-ruling.md) is the standing precedent that
identity dominates registration.

**⛔ THE OPEN FINDING THAT MATTERS MOST IS STILL E30's.** W3's projection does not reproduce —
styled **1,718,750** against a recorded **1,653,659** — because `project_twins`' erosion was
rebuilt under E08 A3. The remedy is **ruled**: a **re-run under the recorded era's flags, not
a tool change.** `--edge-absolute` exists at `project_twins.py:103`; `--mask-keyed`,
`--key-corner-median` and `--trust-intersect` are the other era switches on that path. Which
combination reproduces is empirical and unspent.

## What is queued, with scope already measured

**THE ARCHIVE-TO-`D:` ARC.** ⚡ **`D:` is a real drive** — external, label `AI-BACKUP`,
~3,472 GB free. **Treat presence as a per-session fact** (`Test-Path D:\`) and never make a
live pipeline path depend on an external drive being mounted.

- `E:\AI\training` is **114 GB**, of which **15.9 GB is facet's protected record** — exactly
  the eight subtrees, **7,312 files / 17,072,807,610 bytes**. The other ~98 GB is every other
  studio project's training material.
- **The design, and "fallback" has a precise meaning:** copy → **verify by per-file sha256** →
  only then remove. Never move-then-check. **The index lives on `E:`**, because an unplugged
  `D:` must still tell you what is on it. And the tool must be **structurally unable to reach
  the eight facet subtrees** — a refusal list asserted before any move, with a test proving it
  refuses. *Prefer eliminating a risk to gating it.*
- **Waiting on his call:** ~38 GB of LoRA checkpoint sets and a 23 GB `output` directory.

**`comfy-preflight` — LIVE, IN ITS OWN REPO, AND AHEAD OF SCHEDULE.**
[mcp-tool-shop-org/comfy-preflight](https://github.com/mcp-tool-shop-org/comfy-preflight)
(PUBLIC, `main`). **Checks 1, 2, 4 and 5 are built**, with its own suite green in all three
interpreter modes — *count deliberately not quoted here: it is that repo's number, and T34's
sweep correctly refuses a bare test count on this page that could be misread as facet's.*
The spec lives here at [docs/specs/comfy-preflight-spec.md](specs/comfy-preflight-spec.md)
with **Amendment 1 and 1a** — check 5 re-specified (its operand is the **effective** frame, not
the declared one, because the 1066→1064 defect happened *upstream of the graph*) and ÷8-halts /
÷16-advises ratified.
**Its next arc is NOT checks 3/6/7**: check 3 has no profile fixture, check 7 needs enumeration
first (it needs the *builder*, and the corpus holds outputs), and check 6 is transport-side.
**It is the `preflight()` aggregator, the MCP surface and the CLI** — the adoption contract *is*
the product (in-process on the submit path, no skip flag), and three built checks nothing can
call is a shelf.

**THE POLISH LANES.** [E14 Ruling 35](experiments/E14-ruling.md)'s four-tools precondition is
**RELEASED**. ⚠ **Its per-profile anchor CLAUSE is NOT released**: every polish lane opens with
a per-profile anchor gate, each replay landing as a permanent artifacts-tier test in the same
commit. **A subject's lane opens when its gates do**, and W3's projection gate is the open one
— and item 1 above is that gate's own instrument.

## The release sequence, when he fires one — the order is law

```
1. RE-COUNT      pytest --collect-only  -> currently 891 total / 851 hermetic
                 ⚠ RESERVE COUNT SURFACES BY NAMING T34's PINS TABLE, NEVER BY
                 TRANSCRIBING IT. It holds SIXTEEN pins across SIX files, plus a
                 separate leg over the SEVEN translated READMEs. Two seats in a row
                 hand-listed it and each missed a different file.
2. VERSION       FIVE declarations - pyproject.toml, package.json, bin/facet.js
                 `version` AND its `tag`, record_mcp.SERVER_VERSION. T27 pins the
                 agreement; release.yml refuses on a mismatch.
                 ⚠ measure_mcp.MEASURE_VERSION is INDEPENDENT and NOT in that set.
                 It sits at 0.4.0 and the package now does too - a COINCIDENCE.
3. CHANGELOG     [Unreleased] -> [x.y.z], fresh empty [Unreleased] above.
                 ⚠ NEVER quote a suite total in a released entry or a release-notes
                 file - the TWO regions T34 deliberately does not sweep.
4. RELEASE NOTES .github/release-notes-vX.Y.Z.md - release.yml reads it BY TAG NAME
                 and the run FAILS without it. Carry a compensators line.
5. TRANSLATIONS  node E:/AI/polyglot-mcp/scripts/translate-all.mjs README.md
                 --cache-clear   (MANDATORY). RUN IT ONCE, AFTER THE CONTENT IS
                 FINAL - a mid-run README edit wastes the whole pass.
                 ⚠ THEN SWEEP, AND THE SWEEP CATCHES REAL DEFECTS: heading parity,
                 NO TWO-CANDIDATE HEADINGS (v0.4.0 had THREE - the model emitted
                 "X? / Y?" rather than choosing, twice in Italian, once in Hindi),
                 nav bars complete, any bare URL intact, LF measured IN PYTHON.
                 git add README.md README.*.md -> ONE commit.
6. THREE DERIVED ARTIFACTS, and THE ORDER MATTERS:
                 (a) the CENSUS FIRST - `instrument_census.py --committed`. ⚠ NOT
                     --skip-probe, which wipes axis F. It is machine-emitted from
                     whatever is on disk, so it cannot be hand-reconciled and it
                     belongs in the same reservation as the count surfaces.
                 (b) THEN the DB + certificate - record_build IN A FRESH INTERPRETER
                     (the mount holds SERVER_VERSION from process start and will
                     write the OLD one), then read server_version back FROM THE
                     FILE, then commit the pair.
                     ⚠ `docs/instrument-census.md` IS IN THE CORPUS, so emitting it
                     after the index leaves the index stale. record_health catches
                     it; do it in this order and it never arises.
                 (c) the count surfaces.
7. TAG           AT HIS WORD ONLY, and cut it BY SHA at the release commit.
                 ⚠ release.yml fires on `push: tags: ['v*']`, NOT on
                 `release: published` - a Release made with GITHUB_TOKEN does not
                 fire that event, which silently skipped PyPI on xrpl-lab v1.7.1.
                 SO PUSHING THE TAG IS THE WHOLE ACTION; the workflow cuts the
                 Release itself. He is on PowerShell 5.1 - `&&` is a parser error,
                 give him two commands.
8. READ-BACK     ⚠ QUERY THE INDEX THE CONSUMER READS. At v0.4.0 this seat read
                 PyPI three ways and got three answers: the aggregate
                 /pypi/<name>/json said the OLD version (cached), pip said "no
                 matching distribution" (its own cache), and the SIMPLE INDEX -
                 https://pypi.org/simple/<name>/ with the JSON Accept header - was
                 authoritative and correct. Go there first, or just
                 `pip install --no-cache-dir`. THEN INSTALL THE PUBLISHED PACKAGE
                 AND RUN A VERB. Not --help. And test `npx` from OUTSIDE a checkout.
```

**The tag and the publish are his. Steps 1–6 are reversible and are YOURS.**

## ⚠ WHAT WILL COST YOU

1. **Run a verb, not `--help`.** Four releases shipped a wheel that could not find its own
   record while four green pipelines checked the surface that worked.
2. ⚠ **A DEPENDENCY MISSING FROM PyPI FOR THIS RIG'S PYTHON IS NOT UNAVAILABLE — CHECK THE
   PROJECT'S NIGHTLY/DEVEL CHANNEL.** This seat wrote *"there is nothing installable for
   Python 3.13"* into a pyproject comment, a runtime refusal and a ruling — **having read the
   `main-devel` URL in that same session.** `open3d` publishes 8 cp313 wheels there and this
   rig runs one. **"Cannot declare" ≠ "cannot install"**: a direct URL is legal on a pip
   command line and banned only in published metadata; the remedy is a documented install line
   plus a PEP 508 marker. **The Director has raised this repeatedly.** It is in the memory
   store now.
3. ⚠ **`pathlib.write_text()` translates `\n` to `\r\n` on Windows.** It put CRLF into 13
   tracked files in one pass. Write **bytes** when editing tracked text programmatically; T06
   catches it, but after the fact.
4. **Reserve count surfaces from `T34.PINS`, never by transcribing a failure list.** A failure
   list shows what is *currently stale*; the table shows what is *watched*.
5. **Verify inherited claims — including your own rulings.** This seat's Ruling 3a was
   over-strong and was corrected before release, at the Director's question.
6. **Before trusting a reading, ask what a passing value would have looked like.**
7. **Read the front door in full before editing it.** The `readme-gate` hook enforces it — and
   at v0.4.0 the README did not mention the headline feature until it was rewritten.

## THE PRACTICES — they bind you

1. **THE SHEET-WALK before any number** — his images and rendered surfaces walked FIRST, at
   full size, before any metric is quoted.
2. **Measure before ruling.** Every ruling this seat made that reached beyond its arc was
   re-checked at source first, and three of them corrected the report.
3. **Verify and commit never share a call.** Pathspec-scoped commits; never `git add -A`; no
   stash; the DB commits as a pair with its certificate.
4. **Own the seat's misses in the fold that finds them**, with the measurement.
5. **Translations are the advisor's own hands**, always before the tag, always
   `--cache-clear`, always swept afterward.
6. **Right-size verification** — but run the **full suite** before a ruling that accepts an arc.
7. **A gate that pins the pre-change state is a gift, not an obstacle.** v0.4.0 moved five of
   them (T59, T62, T32, T41, the census ANDON) and **two had left instructions in their own
   docstrings** for whoever made the change. Read the docstring before editing the assertion.

## ⚠ IF TWO SEATS RUN IN PARALLEL

* **File-scoped `git add`, always — and diff each file before staging it.**
* `git fetch && git merge --ff-only origin/main`, **not** `pull --rebase`.
* ⚠ **Derived artifacts are why a fold goes narrow.** The census is machine-emitted from
  whatever is on disk, so with a sibling's uncommitted work in the tree it encodes *their*
  work into *your* commit. Measured at v0.4.0: a re-emit moved axis E only (test_files 57 → 61,
  all from a sibling's uncommitted tests) and axis D not at all — so the census was reverted
  rather than committed. **Check which axis moved before you commit one.**
* **Rule on a pristine clone** when two seats' work is in the tree. `git clone --no-hardlinks`
  to scratch and run the gates there; the local red may be the other seat.
* **Allocate T-numbers in the dispatch.** The namespace has no allocator.

---

## The advisor's record, this seat — for calibration

**The errors clustered in one place: I was too quick to declare something impossible, and
twice I did it with the disproving evidence already on my screen.**

1. ⚑ **The nightly-build miss** (trap 2 above) — the worst of them, because the Director had to
   raise it himself and had raised it before.
2. ⚑ **Ruling 7's own figure was transcribed from a failure list** — "nine pins across five
   files" against a true sixteen across six — *inside the ruling that forbids exactly that.*
3. **I added two `__init__.py` files that were unnecessary and fired the census's
   duplicate-basename ANDON**, then nearly banked a false "setuptools synthesizes them" result
   from a stale build cache. Caught because the synthesized files were the exact byte size of
   my own docstrings.
4. **I put CRLF into 13 tracked files** with `write_text()` (trap 3).
5. **I read PyPI three ways and narrated each swing** instead of going to the simple index.
6. **My E29 dispatch asserted there was no segmentation stage in front of the reconstructor.**
   There is one, inside it. That premise seeded a prediction that then missed.

**What worked, keep doing it**: reading source instead of accepting a report — it corrected
three claims that reached beyond their arcs · demonstrating rather than asserting (a clean venv
and a verb settled every packaging question that argument could not) · owning misses in the
fold that found them · **stopping at a fired ANDON and looking for the cheaper path**, which is
how the `__init__.py` route got replaced by no route at all.

## The executors

**All four were exceptional.** E29's seat **measured a noise floor nobody asked for**, because
it noticed two runs of one input differed and judged the arm unreadable until it knew why —
that became the arc's foundation and a standing law. It also **refused to convert a declining
precondition into a solidity claim**, which would have been more impressive and wrong. E31's
seat **built six wheels and six clean venvs** where the dispatch asked for one, and **found the
frozen binary's `sys.executable` defect by running a measurement rather than a banner.**
comfy-preflight's seat **halted correctly at repo-first** and produced its whole pre-build
measurement set anyway. **When an executor declines to do something, that is signal.**

## The Director

He gates outcomes and his eye leads the instruments. This seat's best work came from his
questions: *"so we only got 4 of the measurement tools to work?"* surfaced that I had
overstated a limit, and *"is there a nightly build for Python 3.13?"* corrected a ruling before
it shipped. **When he asks a question about a claim, re-measure the claim — do not explain
it.** His corrections are short and always about something real.

---

## Environment

⚠ **CHECK THE VRAM WATCHDOG AT SESSION START** — and verify the heartbeat **advancing**, not
the starter's exit code.

```
pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1
```

```
python    E:\AI-Models\trellis2-env\Scripts\python.exe      <- ABSOLUTE, always
blender   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"   -b -P only
drives    C: (system) · D: (external AI-BACKUP, ~3,472 GB free) · E: (AI workspace)
```

- **Bare `python` lacks `open3d` AND `mcp`.** T18 refuses the wrong interpreter in one line.
- ⚠ **`trellis2-env`'s `open3d` is `0.19.0+241aaee`, a cp313 DEV wheel** from Open3D's
  `main-devel` channel — the channel has since moved to `+63e30be`. Four served instruments
  need it, and the identity envelope does not record it.
- ⚠ **`trellis2-env`'s setuptools predates PEP 639**, so `pip wheel . --no-build-isolation`
  fails on `project.license`. Build with isolation (the default).
- **The reconstructor needs `ATTN_BACKEND=sdpa`** — measured, one variable, no install.
  `SPARSE_ATTN_BACKEND` is **inert on this route** but stays in the recorded string.
- **Generation is cloud-only; the local ceiling is never raised.** Blender through PowerShell,
  always `-b -P`.
- ⚠ **MANIFEST THE EIGHT FACET SUBTREES, NOT THE TRAINING ROOT** — `facet_next`,
  `facet_E01/E02/E05/E06/E07/E08`, `saltroad_bake_fix` = **7,312 files /
  17,072,807,610 bytes**. The root holds 131,970 ([E28 Ruling 22](experiments/E28-ruling.md)).
- **The recorded trees are not in git and have no revert.**
- **Scripts create their own output directories.** `argparse` eats leading minus signs
  (`--views=-30,0,30`). **ASCII prints.**
- CI is paths-gated over `tools/ tests/ pytest.ini .mcp.json .github/workflows/ pyproject.toml
  package.json bin/` — a docs-only commit correctly triggers **no** run.
- ⚠ **A `grep -c $'\r'` CRLF alarm on the translations is a FALSE POSITIVE.** Measure line
  endings in Python.
- ⚠ **`npx @mcptoolshop/facet` run from INSIDE the repo short-circuits to the local package**
  and looks fine. Test that path from outside a checkout.

## Do not

End a session the Director has not ended · present any surface you have not walked at full
size · **do work he did not ask for** · **verify his present-tense statements about his own
rig** · `git add -A` in a shared copy · run the suite or the mount on bare `python` · leave CI
red · run translations from an executor session, or after a tag · fire a tag, release or
metadata change before his word · touch the closed rulings, accepted assets, export trees or
the seeded set except to cite · hand-edit `facet.db` or its certificate · split the DB/cert
pair · convert `superseded/`'s one remaining `assert` · rename `e13_anchor_check.py`
(E27 Ruling 4) · **treat E14 Ruling 35's per-profile anchor CLAUSE as released — only its
four-tools precondition was** · decide an executor's findings in the executor's seat.
