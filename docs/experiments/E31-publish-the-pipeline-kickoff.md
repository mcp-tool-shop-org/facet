# E31 — what does it cost to put the pipeline in the package?

**Written by the advisor, 2026-08-09**, at the Director's sequencing (*the pipeline on npm,
before `comfy-preflight`*). Halts at `E31-publish-the-pipeline-report.md`; the advisor rules
at `E31-ruling.md`.

---

## The question

`pip install facet-mcp` today gives you a record server that resolves its corpus from the
working directory, and **no measurement server at all**. `npx @mcptoolshop/facet` downloads a
21 MB binary containing the same two modules. The eight tools the measurement server serves —
the thing this repo has spent four arcs building — are **in neither package**.

**This arc does the reversible half.** It measures exactly what an installed package cannot do
today, and makes it able to. **It fires no tag and publishes nothing.** Release-sequence steps
1–6 are the advisor's and are in scope; steps 7 and 8 are the Director's and are out.

## ⚖ THE DIRECTOR'S TWO CLAUSES READ IN TENSION — AND THAT IS AN OPEN QUESTION, NOT A GAP

He asked for **the pipeline on npm, before `comfy-preflight`**. He then said *"we'll keep
working on the measurement tools before we publish."*

The outgoing handoff read the second clause as **overriding**
[E27 Ruling 8](E27-ruling.md) (*"`measure_mcp.py` stays out of the wheel, and that is the
default, not a deferral"*). Read plainly, it does the opposite — *keep working on them
**before** we publish* is that ruling's own position in his own words. **The advisor does not
resolve an ambiguity in the Director's words by choosing the reading that generates more
work.** It goes to him as OQ1.

Either reading leaves this arc's work identical and reversible. What they change is whether
the tag that eventually follows carries the measurement server — which
[E27 Ruling 8](E27-ruling.md)'s own out-of-scope line already assigns to him: *"Whether
`facet-measure` ships — his."*

⚠ **One correction to the handoff's supporting argument, so it is not inherited.** It claimed
R8's reasoning "now favours publishing," because publishing after the polish arc would mean
"the boundary lands inside the very comparison the tool exists to make." **That does not
hold.** `MEASURE_VERSION` has already moved 0.1.0 → 0.3.0 → 0.4.0 across E27 and E28; each bump
is a comparability boundary whether or not PyPI has heard of it, and comparability here is
carried by the **identity envelope** — server version + instrument sha256 + config hash —
that every payload already records, not by publication. Publishing neither creates nor moves
the boundary. R8's actual concern was **freezing an API nobody has exercised on new work**, and
that concern is still live: E29 is its first such consumer and E29 has not run.

## What is already measured — VERIFY ALL OF IT BEFORE DESIGNING AROUND IT

Measured at the advisor's seat, 2026-08-09. *An inherited claim is a hypothesis wearing a
fact's clothes — including one written by the advisor an hour ago.*

| claim | measured | site |
|---|---|---|
| packaged modules | `py-modules = ["facet_index", "record_mcp"]` — **`measure_mcp` absent** | `pyproject.toml:50` |
| instrument packaging | **neither `tools/diagnostics/` nor `tools/verify/` is packaged**; `package-dir = { "" = "tools" }` | `pyproject.toml:48-50` |
| `measure_mcp` resolver | `REPO = os.path.dirname(HERE)` — **the pre-E24 form, verbatim** | `measure_mcp.py:139` |
| `record_mcp` resolver | `REPO = facet_index.REPO` — the two-marker property test | `record_mcp.py:112` |
| how instruments run | **subprocess** at `os.path.join(REPO, "tools", rel)`, `cwd=REPO` | `measure_mcp.py:309, 325` |
| declared dependencies | **`mcp>=2.0.0`, and nothing else** | `pyproject.toml:24-26` |
| instrument dependencies | `numpy`, `scipy`, `trimesh`, `open3d`, `PIL` across the eight | table below |
| their installed size | **357.5 MB** in `trellis2-env` — open3d **207.1**, scipy 99.9, numpy 25.9, PIL 15.7, trimesh 5.4 | `site-packages` |
| npm shape | launcher → GitHub Release binary, SHA256-verified, cached | `bin/facet.js:19-27` |
| the binary's premise | *"a package whose dependencies are stdlib, sqlite3 and mcp"* | `bin/facet.js:18` |

**Per-tool dependency split — a design lever nobody has named:**

| served tool | instrument | numpy | scipy | trimesh | PIL | **open3d** |
|---|---|:-:|:-:|:-:|:-:|:-:|
| `mesh_stats` | `verify/mesh_stats.py` | ● | ● | ● | | |
| `mesh_topology` | `diagnostics/e14_topology.py` | ● | ● | ● | | |
| `measure_report` | `verify/gate1_sheet.py` | ● | | | ● | |
| `anchor_check` | `verify/anchor_compare.py` | ● | ● | | ● | |
| `reach_ceiling` | `diagnostics/e08_ceiling.py` | ● | | ● | | **●** |
| `thin_extent_curve` | `diagnostics/e12_thin_curve.py` | ● | | ● | ● | **●** |
| `offsurface_rate` | `diagnostics/e12_offsurface.py` | ● | | ● | | **●** |
| `texel_provenance` | `diagnostics/texel_provenance.py` | ● | ● | ● | ● | **●** |

**Four of eight need `open3d`; four do not** — and the four that do not include **both anchor
tools**, which is the half [E14 Ruling 35](E14-ruling.md)'s per-profile anchor gate actually
calls.

## ⛔ TASK 0-PRE — THE SERVED SURFACE IS UNREACHABLE OVER MCP. Added by [E29 Ruling 7](E29-ruling.md).

`.mcp.json` declares **one** server, `facet-record`. `tools/measure_mcp.py` is in neither that
file nor `E:\AI\.mcp.json`. **No session can reach the measurement server over MCP as the repo
stands** — E29 had to import the module and unwrap the tool functions in-process to grade its
meshes, which it did correctly and which proved the code path, not the transport.

So **"the measurement server serves 8 of 8" is true of the code path and false of the
transport**, and every surface carrying that phrase needs the qualifier until this lands.

⚠ **The one-line fix is NOT the deliverable, and shipping it alone would repeat this repo's
most expensive habit** — adding a line and declaring it fixed is the same shape as running
`--help` and declaring a wheel good. **The registration ships with a test that starts the
server as a subprocess over stdio, calls a served tool, and asserts a payload comes back with
its identity envelope.** That test is this arc's subject in miniature, which is why it lives
here and not in a ruling commit.

## ⛔ TASK 0 — BUILD THE FAILING TEST FIRST, AND WATCH IT FAIL

**Before any fix.** Build the wheel from this tree, `pip install` it into a **clean venv**, and
run a **measurement verb** — not `--help`. [E24](E24-ruling.md) shipped four releases with a
broken resolver because `--help` was the only wheel check ever run.

⚠ **IT MUST FAIL ON ARRIVAL, AND THE FAILURE IS THE DELIVERABLE.** A test that passes before
any fix has tested nothing — [E30](E30-ruling.md) ratified an executor who **found and removed
a check of its own that could not fail** before it landed, and the silhouette-IoU gate that
returned 1.00000 on a holed mesh is this repo's founding example. **If your test passes on
arrival, HALT**: the test is wrong, not the package.

Report, for each of the eight served tools, **what an installed package does today** — and say
whether it fails at **the resolver**, at **the missing instrument file**, or at **a missing
third-party import**. Those are three different defects and **only the first is E24's.**

## Task 1 — the resolver, and E24's fix is the WRONG remedy here

`measure_mcp.py:139` is E24's defect verbatim. **Do not copy `record_mcp`'s fix into it.**

`RECORD_MARKERS = ("CLAUDE.md", "docs/experiments")` keys on the **corpus**, and
`facet_index.py:110` states in its own comment that *"neither marker can appear in an
install."* That is deliberate: corpus cannot ship. **The measurement server's dependency is the
instruments, which are code and CAN ship.** Copying the corpus resolver would bind the
measurement server to a checkout for a reason that does not apply to it — *test the property,
not a proxy for it*, and the property here is a different one.

Two shapes. **Measure both; choose neither** — that is the ruling's job:

- **Shape A — the instruments ship.** Package `tools/diagnostics/` and `tools/verify/`; resolve
  package-relative. `facet-measure` works from a clean install, no checkout.
- **Shape B — the instruments do not ship.** Apply a marker resolver; `facet-measure` requires a
  checkout exactly as `facet-mcp` does, and the wheel is a launcher for a repo you already have.

For each: what works, what refuses, and **what the refusal message can state exactly** — the
property E24 chose its resolver for.

## Task 2 — the dependency declaration

The package declares `mcp>=2.0.0`. The instruments need five more. Measure:

- **Does an extras group carry it** — `pip install facet-mcp[measure]` — and does a **tiered**
  split work (a light tier without `open3d`, a full tier with), given the 4/4 table above?
- **`open3d`'s actual support matrix against `requires-python = ">=3.11"`.** Measure it from the
  index; do not assume. **If open3d publishes no wheel for a Python the package claims to
  support, that is a hard finding** and it constrains OQ2 by itself.
- **What each of the eight does when its dependency is absent.** A clean refusal through the
  server's own path is a different product from a traceback, and [E23](E23-ruling.md)'s CI gate
  fired on exactly this class — a module-level `cv2` import in a tool no test had ever invoked.

## Task 3 — the packaging ruling

`pyproject.toml:43-47` states the design note in writing: `py-modules` was chosen **so that
making `tools/` a package would not rewrite the `python tools/<name>.py` invocation that every
recorded command in this record cites.** Those commands are citable evidence.

**Measure whether packaging the instruments actually breaks it**, rather than assuming either
way. And name the second-order cost the note does not mention: under
`package-dir = { "" = "tools" }`, adding these would ship **top-level packages named
`diagnostics` and `verify`** — two of the most generic importable names available, installed
into every environment that takes this package. **Report options; do not pick one.**

## Task 4 — the npm half

`bin/facet.js:16-18` states the binary route's precondition in writing: the reason
backpropagate abandoned binaries (torch past GitHub's 2 GB asset cap) *"does not apply to a
package whose dependencies are stdlib, sqlite3 and mcp."* **Shipping the measurement server
voids that sentence.**

Measure it rather than reasoning about it: build the PyInstaller binary **with** the instruments
and their dependencies, and report its size per platform against the 2 GB cap. **357.5 MB
installed is the advisor's floor and is explicitly NOT a prediction of the binary** —
PyInstaller compresses, and also adds a Python runtime. **If it is too big, that is a finding,
not a failure**, and it decides OQ2 by measurement.

## ⚖ Open questions for the Director — do not answer these; the report frames them

- ⚖ **OQ1 — ANSWERED BY THE DIRECTOR, 2026-08-09: `facet-measure` SHIPS.** His words:
  *"facet-measure is what the publish is waiting for. What's the holdup?"* **[E27 Ruling
  8](E27-ruling.md)'s default is overridden by his live word** — which is the only thing that
  could override it, since that ruling's own out-of-scope line reads *"Whether `facet-measure`
  ships — his."* The tension between his two earlier clauses is dissolved in the direction the
  advisor declined to guess: *"we'll keep working on the measurement tools before we publish"*
  means the tools must be **ready**, and readiness is this arc. **The publish is gated on this
  arc completing, not on another experiment.**
  ⚠ **What does NOT follow: a tag.** Steps 7 and 8 remain his (gate 2). This arc makes the
  package able to carry the server; firing the release is a separate word.
- **OQ2 — if it ships: Shape A or Shape B, and at what dependency tier?** Answered by tasks
  1, 2 and 4's measurements, not by preference.

## Predictions — committed BEFORE task 0 runs

Write `E31-predictions.md` and commit it before the first wheel is built. Point estimate, band,
blind disclosure per row. **Name the unit and the denominator before each number.**

- **P1** — of the eight served tools, how many fail from a clean install today, and **at which
  of the three layers** does each fail (resolver / missing file / missing import)?
- **P2** — does `record_mcp`'s **own** wheel-tier *measurement verb* pass today? E24 fixed the
  resolver; nothing has run a **verb** from a clean venv since.
- **P3** — the PyInstaller binary's size with instruments, per platform. State the floor you
  reason from and why it is a floor.
- **P4** — does `open3d` publish a wheel for **every** Python in `requires-python = ">=3.11"`?
- **P5** — does packaging the instruments break **any** recorded `python tools/<name>.py`
  invocation? Binary, with the falsifier stated.

⚠ **EIGHT consecutive arcs have missed on one family** — a unit, a population, an unchecked
property, the rarest clause of a conjunction, or the instrument's continued ability to express
the question. **P1 is a conjunction wearing one number**: a tool fails if *any* of three layers
fails, so predict each layer, then the join — and remember the join tracks the **rarest**
clause, not the salient one. Read those laws in CLAUDE.md before writing a number, and **apply
no calibration haircut**; E23's seat halved an untutored estimate on this repo's own lesson and
moved *away* from the truth.

## Gates

1. **Task 0's test FAILS before any fix.** If it passes on arrival, **HALT** — the test is wrong.
2. **No tag, no publish, no release, no `gh repo edit`, no metadata change.** Steps 7 and 8 of
   the release sequence are the Director's.
3. **`MEASURE_VERSION` does NOT move** — it versions a payload and no payload changes here. The
   five declarations T27 pins stay in agreement and **also do not move**: this arc is not a
   version bump.
4. **Tests ride the commit that touches the code.** A `tools/` change without its tests in the
   same commit is a missing step and you add them unasked. **T58–T62 are reserved for this
   arc** — the namespace has no allocator.
5. **CI green**, run id **resolved** before it is written; `NOT YET RUN` until it is. Never a
   plausible identifier with a verdict beside it.
6. **The count surfaces are the ADVISOR's and are RESERVED** — `README.md`,
   `docs/advisor-kickoff.md`, `site/src/site-config.ts`,
   `site/src/content/docs/handbook/getting-started.md`, and the DB/cert pair. T34 pins a stated
   count against the tree its surfaces sit in, so two live seats cannot both be green
   independently. **Do not touch them**; report any drift and the advisor reconciles.
7. **The manifest holds** — the eight facet subtrees (`facet_next`, `facet_E01/E02/E05/E06/E07/E08`,
   `saltroad_bake_fix`), **7,312 files / 17,072,807,610 bytes**, 0/0/0, before and after. **Not
   the training root** (131,970 files).

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every measured claim carries its file and line; the wheel is built from a named tree and installed into a clean venv, so the tier reproduces from the report alone |
| ANDON_AUTHORITY | 3 | gate 1 is the **inverted** halt this repo had to learn — it fires when a check *passes* too early; gates 2 and 3 halt on any irreversible or version-moving act; gate 6 halts a seat that touches a reserved surface |
| NAMED_COMPENSATORS | 3 | **nothing here is irreversible.** No publish, no tag, no release, no external write. Undo is `git revert` plus deleting a scratch venv and `dist/`. The two irreversible acts in the vicinity — `npm publish`, `gh release create` — are gated OUT by gate 2 and belong to the Director |
| DECOMPOSE_BY_SECRETS | 3 | the four tasks are the four things that change independently: where code resolves paths (1), what the environment must supply (2), how the tree maps to a package (3), how the binary is assembled (4). A change to one does not force a change to another |
| UNCERTAINTY_GATED_HUMANS | 3 | OQ1 and OQ2 route the two genuinely-his decisions to him, framed **contrastively** — the handoff's reading is stated, then the reading that contradicts it, with the evidence for each, per Horvitz/Buçinca |
| EXTERNAL_VERIFIER | 3 | the wheel-tier test runs in a different process, a different interpreter and a different filesystem location from the tree that produced it; **a clean venv cannot see the checkout that masks every defect this arc looks for** |

## Out of scope

- **The tag, the publish, and the GitHub release.** His acts, gated by gate 2.
- **`comfy-preflight`** — ruled STANDALONE, a new org repo, and repo creation is his act.
- **The polish lanes**, and [E14 Ruling 35](E14-ruling.md)'s per-profile anchor clause, which is
  **NOT released** — only its four-tools precondition was.
- **E29** and the archive-to-`D:` arc.
- **Commissioning new instruments**, or changing what any of the eight measures.
- **`docs/experiments/README.md`**, the index pair, and the census — advisor surfaces.

## Environment

```
python    E:\AI-Models\trellis2-env\Scripts\python.exe      <- ABSOLUTE, always
repo      E:\AI\facet
```

- **Bare `python` lacks `open3d` AND `mcp`** — which is **this arc's subject**, not an obstacle
  to it. The clean venv you build for task 0 is *supposed* to lack them; that is the measurement.
- Build the wheel and the venv **in scratch**; nothing enters the repo tree beyond `dist/`.
- CI is paths-gated over `tools/ tests/ pytest.ini .mcp.json .github/workflows/ pyproject.toml
  package.json bin/` — this arc touches several, so expect a run.
- **ASCII prints.** Scripts create their own output directories. `argparse` eats leading minus
  signs (`--views=-30,0,30`).

## Halt

Report at `E31-publish-the-pipeline-report.md`.

- **State predictions before you look**; disclose whether each was blind.
- **Never judge whether output is good.** *Verified, shipped, works, decisive, validated,
  proven* belong nowhere in the report.
- **A negative result is a full success.** If the measurement server cannot honestly ship in a
  wheel, say so plainly with the number that shows it — **that answers OQ1 better than a
  successful build would.**
- **Do not write to the memory store.** Do not end a session the Director has not ended.
