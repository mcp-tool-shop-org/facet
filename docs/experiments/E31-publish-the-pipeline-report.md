# E31 report — what it costs to put the pipeline in the package

**Executor, 2026-08-09.** Spec:
[E31-publish-the-pipeline-kickoff.md](E31-publish-the-pipeline-kickoff.md). Predictions:
[E31-predictions.md](E31-predictions.md), committed at `8e21cea` before `python -m build`
was run once and before PyPI was asked anything. The advisor rules at `E31-ruling.md`.

**Nothing was tagged, published, released, or `gh repo edit`ed. No version moved.**

---

## The one-paragraph answer

**The measurement server can go in a wheel, and 8 of 8 served tools return payloads from a
clean install — measured, at the full dependency tier, on Python 3.12.** What it costs is
three things the dispatch did not have numbers for: the package grows from a 58 KB / 2-file
payload to a 506 KB / 114-file payload carrying two generic top-level import names; a clean
install goes from **66.0 MB** of site-packages to **634.6 MB**, of which ~230 MB is
`open3d`'s transitive tree — a web framework and a Jupyter widget stack, declared as hard
requirements; and **`open3d` publishes no distribution at all for Python 3.13 or later**,
while `pyproject.toml` declares `requires-python = ">=3.11"`. **The npm half is a different
answer: size is not its blocker.** The frozen binary is 162,962,583 bytes — 12× inside
GitHub's 2 GB cap — answers `--print-tools` with exit 0, and **cannot run a single
measurement**, because inside a one-file build `sys.executable` is the binary itself and
every instrument is spawned as a subprocess of it.

---

## 1. What this arc changed in the repo

| file | change |
|---|---|
| `.mcp.json` | `facet-measure` declared, pointing at `tools/measure_mcp.py` under the same pinned interpreter as `facet-record` |
| `tests/test_t23_mount_path.py` | its `list(servers) == ["facet-record"]` assertion widened to an exact SET over both servers, parametrized per server, plus a leg that both name one interpreter. 3 legs -> 6 |
| `tests/test_t58..t62` | 48 tests, five files (below) |

**No tool code changed.** `git diff` over `tools/ pyproject.toml package.json bin/` is empty
at the arc's commit. Every shape measured below was built in a **scratch copy of the tree**,
never in the repo, which is why tasks 1-4 could measure both options without adopting either.

---

## 2. The dispatch's claims, re-measured at this seat

*An inherited claim is a hypothesis wearing a fact's clothes — including one the advisor
wrote an hour ago.* All nine reproduce.

| claim | measured | how |
|---|---|---|
| `py-modules = ["facet_index","record_mcp"]`, `measure_mcp` absent | holds | `pyproject.toml:50` |
| no `MANIFEST.in`, no `package-data`, no `packages` | holds | file absent; keys absent |
| the wheel contains exactly two `.py` files | holds — payload is `facet_index.py`, `record_mcp.py`, **58,401 bytes** | built from this tree |
| `measure_mcp.py:139` is `REPO = os.path.dirname(HERE)` | holds, E24's pre-fix expression verbatim | line 139 |
| `record_mcp.py:112` is `REPO = facet_index.REPO` | holds | line 112 |
| instruments run as subprocesses at `REPO/tools/<rel>`, `cwd=REPO` | holds | `measure_mcp.py:309, 323-325` |
| `dependencies = ["mcp>=2.0.0"]` and nothing else | holds | `pyproject.toml:24-26` |
| `bin/facet.js:18` states the binary route's dependency premise | holds | line 16-18 |
| four of eight need `open3d`, four do not | holds — the four that do not are `mesh_stats`, `mesh_topology`, `anchor_check`, `measure_report` | module-level imports of all eight; now pinned in T60 |

**One correction to the dispatch's dependency table.** It lists `anchor_check`'s instrument as
needing `numpy` and `PIL`. Both imports are **inside functions** (`anchor_compare.py:102,
120`), not at module level — and that difference is load-bearing, because an instrument is
invoked as a subprocess: a module-level import decides whether the tool runs at all.
`anchor_check` is the only served tool that returns a payload with **no third-party package
installed whatsoever**. The dispatch's table is right about what the code touches and wrong
about what it requires.

**And one number the dispatch called a floor is not one.** *"357.5 MB installed"* was measured
in `trellis2-env`, which shares its site-packages with the rest of this rig's work. A clean
install of the same five packages is **277.9 MB** without `open3d` and **634.6 MB** with it —
because `open3d` declares `dash>=2.6.0`, `flask>=3.0.0`, `ipywidgets>=8.0.4`, `nbformat>=5.7.0`,
`werkzeug>=3.0.0` and `configargparse` as hard requirements. The dispatch's figure counts
`open3d` at 207.1 MB and none of its tree.

---

## 3. Task 0-PRE — the served surface was unreachable over MCP

**Reproduced.** `.mcp.json` declared one server, `facet-record`; `tools/measure_mcp.py`
appeared in neither it nor `E:\AI\.mcp.json`. E29 Ruling 7 holds exactly as written.

**The one-line fix is not the deliverable, so here is what rode with it.**

`tests/test_t58_measure_mcp_registration.py` starts the **declared arguments as a
subprocess**, initializes an MCP session over stdio, lists the tools, calls `mesh_stats` on
the committed hermetic fixture, and asserts the payload's identity envelope — server name and
version, `tool`, `config_hash`, `metrics_label`, the instrument's declared path, and a
**sha256 that must equal the file on disk**. A second leg drives a refusal over the same wire
and asserts it arrives as `PRECONDITION_MISSING` naming the exact absent input.

```
BEFORE the registration:   4 failed, 1 passed
AFTER  the registration:   5 passed
```

The one that passed before the fix is the **can-fail leg**, which must pass: it proves the
config reader can return `None` for a server nobody declared and does not for one that is
declared. A pass there before the fix is the leg doing its job.

**What is launched, and what is only asserted.** `.mcp.json` names the rig's one pinned
interpreter by absolute path, which does not exist on a CI runner. T58 asserts the
*declaration* (both servers must name the same interpreter — the environment law names exactly
one python) and *runs* with the suite's own `sys.executable` and the declared arguments.
Launching the literal declared command would make the file skip on the gate that fires every
push, which is E24 Ruling 3's own shape.

**`E:\AI\.mcp.json` (the workspace file) is unchanged** — it is outside this repo and outside
this arc. A session that mounts *this repo* reads the repo-root file, which now declares both.

**Over the wire, from the repo, before any packaging change:** `facet-measure 0.4.0`, eight
tools listed, `mesh_stats` returning a payload whose envelope carries
`tools/verify/mesh_stats.py` and its sha256, with the instrument's two WARNING lines surfaced
as `warnings`. The transport half of "serves 8 of 8" is now exercised by a test rather than
by a session's memory of having done it once.

---

## 4. Task 0 — the failing test, and what an installed package does today

### The test failed on arrival, and the failure is below

`pip install facet-mcp` from a wheel built from this tree, into a clean venv on the rig's
Python 3.13, then **a measurement verb — not `--help`**:

```
ModuleNotFoundError: No module named 'measure_mcp'
```

**8 of 8, and at none of the three layers the dispatch names.** The module is not in the
artifact, so there is no call path to reach a resolver with. That is a **layer 0**, upstream
of all three, and it is the honest headline: the three-layer attribution is *undefined* on
today's wheel. To make it measurable the arc built three further tiers in scratch.

### The tiers

| tier | what it is | site-packages | wheel payload |
|---|---|---:|---|
| **T0** | this tree's wheel, unmodified | 66.0 MB | 58,401 B · 2 entries |
| **T1** | + `measure_mcp` in `py-modules`, nothing else | 68.4 MB | 75,581 B · 3 entries |
| **T2** | + `diagnostics/` and `verify/` packaged, instrument path resolved beside the module | — | 502,964 B · 113 entries |
| **T2b** | + `subject_profile` packaged too | 68.4 MB | 505,875 B · 114 entries |
| **LIGHT** | T2b + `numpy scipy trimesh pillow`, **no open3d** (py3.12) | 277.9 MB | — |
| **FULL** | LIGHT + `open3d` (py3.12) | 634.6 MB | — |

### Per served tool, per tier — the answer the dispatch asked for

| served tool | T0 | T1 | T2 | T2b | LIGHT | FULL |
|---|---|---|---|---|---|---|
| `mesh_stats` | layer 0 | layer 1 | layer 3 *(`subject_profile`)* | layer 3 *(numpy)* | **ok** | **ok** |
| `mesh_topology` | layer 0 | layer 1 | layer 3 | layer 3 | **ok** | **ok** |
| `reach_ceiling` | layer 0 | layer 1 | layer 3 | layer 3 | layer 3 *(open3d)* | **ok** |
| `thin_extent_curve` | layer 0 | layer 1 | layer 3 | layer 3 | layer 3 *(open3d)* | **ok** |
| `offsurface_rate` | layer 0 | layer 1 | layer 3 | layer 3 | layer 3 *(open3d)* | **ok** |
| `texel_provenance` | layer 0 | layer 1 | layer 3 | layer 3 | layer 3 *(open3d)* | **ok** |
| `anchor_check` | layer 0 | layer 1 | **ok** | **ok** | **ok** | **ok** |
| `measure_report` *(sheet half)* | layer 0 | layer 1 | layer 3 | layer 3 | **ok** | **ok** |
| *`measure_report` (comparison half)* | layer 0 | **ok** | **ok** | **ok** | **ok** | **ok** |
| **failing, of 8** | **8** | **8** | **7** | **7** | **4** | **0** |

**Layer 1 is attributed by the path the failure names, not by guesswork.** At T1,
`measure_mcp.REPO` is `<venv>\Lib` — the parent of the install root, not the install root —
so the path named is `<venv>\Lib\tools\verify\mesh_stats.py`, **outside the package
entirely**. That is what separates a resolver defect from a missing file, and T59 pins it.

**Two tools survive layers the others do not, and both for reasons nobody had written down:**

- **`measure_report`'s comparison half passes `instrument_rel=None` to `envelope`**, so
  nothing is joined onto `REPO` and no file is hashed. It is the only call that returns a
  payload from an install with the module and *nothing else*. Pinned in T59.
- **`anchor_check` returns a payload with zero third-party packages present**, because
  `anchor_compare.py` imports PIL inside a `try/except Exception` and numpy inside the branch
  that import guards. Pinned in T60.

### The refusal text at each layer, verbatim

```
LAYER 1   message: verify/mesh_stats.py exited 2
          hint:    <venv>\Scripts\python.exe: can't open file
                   '<venv>\Lib\tools\verify\mesh_stats.py': [Errno 2] No such file or directory

LAYER 3   message: verify/mesh_stats.py exited 1
          hint:    File "<venv>\Lib\site-packages\verify\mesh_stats.py", line 44, in <module>
                       import numpy as np
                   ModuleNotFoundError: No module named 'numpy'
```

The refusal's **own message** says only that a script exited N. Everything that identifies the
defect — the absent path, the absent module — reaches the caller **inside the child's stderr
tail**, in the `hint`. It is a structured `ToolError` with a code and an exit code, not a raw
traceback, and the operator can read the cause. It is not a statement of it.

---

## 5. Task 1 — the resolver, and the two shapes

`measure_mcp.py:139` is E24's defect verbatim. **E24's own fix is the wrong remedy**, and the
dispatch's reasoning holds under measurement: `RECORD_MARKERS` keys on the corpus because a
corpus cannot ship, and instruments are code and can.

**Both shapes were built. Neither is chosen here.**

### Shape A — the instruments ship

Built as T2/T2b. The instrument is resolved **beside the module**: `join(HERE, rel)` with a
leading `tools/` stripped. One expression, correct in both worlds — in a checkout `HERE` is
`tools/`, in an install `HERE` is `site-packages`, and both hold the instrument directories.

- **What runs:** everything the dependency tier allows. FULL: 8 of 8. LIGHT: 4 of 8.
- **What refuses:** nothing about *location*. A shape-A install cannot lose an instrument; it
  can only lack a dependency, which lands at layer 3.
- **What its refusal can state exactly:** for the dependency case, *"the instrument
  `verify/mesh_stats.py` needs `numpy`, which this environment does not have; install
  `facet-mcp[measure]` or `facet-mcp[measure-full]`."* Everything in that sentence is
  available at the call site today — the instrument path is in `WRAPPED`, and the missing
  module name is the last line of the child's traceback, which `run_instrument` already
  captures. **Nothing composes it.** The four-of-eight tier is only usable as a product if it
  does.

### Shape B — the instruments do not ship

- **What runs:** the module imports; `measure_report`'s comparison half answers; everything
  else needs a checkout.
- **What refuses:** all seven instrument-bearing tools, from anywhere that is not a checkout.
- **What its refusal can state exactly:** the marker property is *available and exact*. A
  shape-B resolver would ask **does this directory contain the instruments** —
  `tools/verify/mesh_stats.py` and `tools/diagnostics/e14_topology.py` — the property itself,
  not a proxy. And it has E24's key virtue by construction: **measured on the T2 wheel, the
  instruments install as top-level `verify/` and `diagnostics/`, never under a `tools/`
  segment**, so a `tools/verify/...` marker is unsatisfiable from inside an install even in
  the shape that ships them. The refusal can then be E24's, word for word in structure: name
  both candidates, name both markers, name both ways forward.

### A third fact that belongs to whichever shape is chosen

`verify/mesh_stats.py:38-39` inserts `tools/` on `sys.path` and imports **`subject_profile`**,
a repo sibling. Packaging the two instrument directories does **not** ship it: at T2,
`mesh_stats` died on `No module named 'subject_profile'` while every other tool died on
`numpy`. Shipping it as a fourth py-module (T2b) moves `mesh_stats` into the same class as the
rest. **This is a fourth failure class the dispatch's three layers do not name**, and it is
the one a shape-A adoption would meet first.

---

## 6. Task 2 — the dependency declaration

### `open3d`'s support matrix, from the index

`open3d` **0.19.0 is the latest release**, and its wheels are:

| release | cp38 | cp39 | cp310 | cp311 | cp312 | cp313+ |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| 0.19.0 | win/linux/macos | win/linux/macos | win/linux/macos | win/linux/macos | win/linux/macos | **none** |
| 0.18.0 | yes | yes | yes | yes | — | none |

`pyproject.toml` declares `requires-python = ">=3.11"`. On the rig's own Python **3.13**:

```
ERROR: Could not find a version that satisfies the requirement open3d (from versions: none)
ERROR: No matching distribution found for open3d
```

— with and without `--only-binary=:all:`, so there is **no sdist to fall back to either**.
`open3d`'s own metadata says `requires_python >= 3.8`, so pip does not refuse on the version;
it simply finds nothing.

**This is a hard finding and it constrains the answer by itself.** A `[measure]` extras group
that hard-requires `open3d` fails on Python 3.13 and 3.14 — *and 3.13 is the interpreter this
repo's own environment law names*. For contrast, measured in the same sweep: `numpy` 2.5.2 and
`scipy` 1.18.0 publish cp312/cp313/cp314 (numpy also cp315), `pillow` 12.3.0 publishes
cp310-cp315, and `trimesh` is a pure-python `py3-none-any` wheel with no compiled half at all.
**`open3d` is the only one of the five that cannot be had.**

### Does an extras group carry it, and does a tiered split work

Both tiers were installed into clean venvs on Python 3.12 and all eight tools called:

| tier | packages added | site-packages | served, of 8 |
|---|---|---:|---:|
| light | `numpy scipy trimesh pillow` | 277.9 MB | **4** |
| full | + `open3d` | 634.6 MB | **8** |

The light tier's four are `mesh_stats`, `mesh_topology`, `anchor_check`, `measure_report` —
**including `anchor_check`**, the only tool whose whole job is asking whether a recorded output
still reproduces. The dispatch frames this set as the half [E14 Ruling 35](E14-ruling.md)'s
per-profile anchor clause calls; that framing is the advisor's and is not re-derived here — what
is measured is the membership. The split is now pinned in T60, per tool and as a count, so it
cannot drift into a stale claim.

**What the full tier actually installs.** `open3d` declares `dash>=2.6.0`, `flask>=3.0.0`,
`werkzeug>=3.0.0`, `ipywidgets>=8.0.4`, `nbformat>=5.7.0`, `configargparse`, `numpy`. The
resulting venv carries `plotly` (59.9 MB), `dash` (39.6 MB), `jedi` (14.9 MB), `ipython`,
`flask`, `jupyter-core`, `requests`, `certifi` and `jinja2`. **CI's `pip-audit` step audits
the published surface in a clean venv** — a `[measure-full]` extra would put a web framework
and a Jupyter stack inside that audit's population.

### What each of the eight does when its dependency is absent

Seven of eight refuse identically: `INSTRUMENT_FAILED`, exit code 2, with the child's
`ModuleNotFoundError` in the `hint`. Structured, readable, and one step short of a statement
(section 4).

**`anchor_check` does something else, and it is a defect.** With PIL absent it returns
**exit-0 payload** whose pixel tier reads:

```json
"pixel": {"attempted": false,
          "not_attempted_because": "one or both inputs do not decode as images;
                                    the byte tier is what exists for them"}
```

Both inputs are PNGs and both decode as images on any environment with PIL. The `try/except
Exception` at `anchor_compare.py:100-108` swallows the `ModuleNotFoundError` and **attributes
a missing dependency to the caller's files**. `warnings` is empty; the envelope records
nothing. The byte tier's numbers are correct; the *stated cause* is not. A caller reading that
payload would go and check their PNGs.

This is neither a clean refusal nor a traceback — it is a **third thing: a silently narrower
payload with a wrong reason attached**, and it is the strongest argument measured here for
composing dependency refusals at the server rather than leaving them to each instrument.
**Not repaired in this arc** — it is a released instrument, the repair is a behaviour change to
a served payload, and choosing it is the ruling's.

---

## 7. Task 3 — the packaging ruling

### Does packaging break the recorded invocation? No.

`pyproject.toml:43-47` states the design note: `py-modules` was chosen so that making `tools/`
a package would not rewrite the `python tools/<name>.py` invocation every recorded command
cites. **Measured rather than assumed.** `tools/diagnostics/__init__.py` and
`tools/verify/__init__.py` were added to the repo tree, the population run, and both files
then deleted:

| | before | after |
|---|---|---|
| files under the two directories | 108 | 110 *(the two `__init__.py`)* |
| runnable with `--help` | 7 | 7 |
| `--help` exit codes | all 0 | all 0 |
| `compileall` failures | 0 | 0 |
| instrument-invoking tests (T12, T36-T39, T43-T47) | pass | **52 passed, 5 deselected** |

Those 52 include every served tool's real subprocess invocation through `run_instrument`.
**No breakage.** The mechanism: `python path/to/script.py` puts the script's own directory at
`sys.path[0]` whether or not it also holds an `__init__.py`, and packaging changes no import
statement, no `sys.path` insert and no file's location.

The two probe files were removed and their absence is now asserted by T62, so the day
packaging is adopted this file must be edited on purpose.

### The population is small, and that is the interesting part

Only **7 of 108** files under the two directories carry both a `__main__` guard and an
argparse surface. The rest are straight-line module-level scripts — E28's measured house
style — so running one *executes* it, and some of them write. The seven are pinned by name in
T62 rather than by count; a new argparse instrument joins the set by a deliberate edit.

### The second-order cost, measured

Under `package-dir = { "" = "tools" }`, packaging these ships **top-level importable packages
named `diagnostics` and `verify`** into every environment that installs `facet-mcp`. Measured
on the built wheel, it is more than two names:

```
T0    58,401 B     2 payload entries   facet_index.py, record_mcp.py
T2b  505,875 B   114 payload entries   diagnostics(100), verify(10),
                                        facet_index.py, measure_mcp.py,
                                        record_mcp.py, subject_profile.py
```

**100 files under `diagnostics`, of which the served surface uses five.** The rest are this
record's historical one-off instruments. A `packages = [...]` line ships the directory, not
the eight.

**Options, not a choice:**

- **A1** — package both directories as-is: 114 entries, two generic top-level names, 100
  files where 5 are served.
- **A2** — one package with a specific name (`facet_instruments/`), the eight moved or
  re-exported under it: one import name, no generic collision. Costs the recorded invocation
  path a rename, which is what the design note exists to prevent, unless the directories stay
  and the package is built from a subset.
- **A3** — an explicit subset under the existing names (`packages` plus a file filter): the
  eight instruments and `subject_profile` only. Keeps the recorded paths, keeps the generic
  top-level names.
- **B** — do not package; `facet-measure` needs a checkout, and the refusal states so exactly
  (section 5).

---

## 8. Task 4 — the npm half

`bin/facet.js:16-18` states the binary route's precondition: the reason backpropagate
abandoned binaries (torch past GitHub's 2 GB asset cap) *does not apply to a package whose
dependencies are stdlib, sqlite3 and mcp*. Carrying the measurement server voids that
**sentence**. It does not, by itself, void the **conclusion** — those are two claims and only
the first falls to the dependency change.

**Built rather than reasoned about.** PyInstaller 6.22.0 (release.yml's pin), Python 3.12,
one-file, `--collect-all open3d --collect-all trimesh`, both instrument directories added as
data, `measure_mcp.py` as the entry point, release.yml's three excludes:

| platform | size | against the 2 GB cap |
|---|---:|---|
| **win-x64, MEASURED** | **162,962,583 B (162.96 MB)** | 8.2% — clears by 12.3x |
| linux-x64, **DERIVED, not measured** | ~544 MB | ~27% — clears by ~3.7x |

The linux figure is a **derivation and is labelled one**: this rig cannot build it. Its
operands are the compressed wheel bytes at the exact installed versions —
win_amd64 126.2 MB against manylinux 507.4 MB, a **4.02x payload ratio driven almost entirely
by `open3d` (69.2 MB win against 447.7 MB linux, 6.5x)** — applied to the measured Windows
binary's non-payload remainder. **The only honest way to close it is a linux build**, which
the release workflow already has a runner for.

### And the binary cannot measure anything

```
facet-measure.exe --print-tools          -> exit 0, 8 tools listed
facet-measure.exe over stdio, mesh_stats -> REFUSED: verify/mesh_stats.py exited 1
    facet-measure.exe: error: unrecognized arguments:
      C:\Users\...\Temp\tools\verify\mesh_stats.py --glb ...
```

Two facts collide in that line:

1. **`run_instrument` spawns `[sys.executable, tool_path(rel)] + args`**, and inside a
   one-file build `sys.executable` **is the binary**. The server re-invokes its own argparse
   with a script path as an argument. No instrument runs, on any tier, at any size.
2. **`REPO = dirname(HERE)`** in a frozen build is the extraction directory's parent — hence
   `Temp\tools\`. This is the defect `FROZEN` exists to handle at `record_mcp.py:110`, found
   in 2026 by installing a published binary and reading its own banner. `measure_mcp` was
   written later, carries the same expression, and asks the question nowhere.

**`--print-tools` exits 0 through all of it** — the same check that stayed green across four
releases of a broken resolver, green again on a new artifact, before it reached anyone.

T61 pins both source facts as AST walks (E24 Ruling 4 forbids a source-string match) and
records that `release.yml` still freezes `record_mcp.py` only, so none of this is reachable by
a user today.

---

## 9. Predictions, scored

| | prediction | measured | verdict |
|---|---|---|---|
| **P1a** | 8 of 8 fail on today's wheel, at a **layer 0** the dispatch does not name; `ModuleNotFoundError: measure_mcp`; payload is exactly the two modules | 8 of 8, layer 0, that exact exception, payload exactly `facet_index.py` + `record_mcp.py` | **HIT** |
| **P1b** | 7 of 8 fail at layer 1, 1 passes. Band 6-8 | **8 of 8 fail** at layer 1; the passing path is `measure_report`'s comparison half, which is a *second path of a failing tool*, not a ninth tool | **MISS by one, inside band.** The mechanism was predicted exactly and the *unit* was not: I counted a path where the row is a tool |
| **P1b** refusal quality | `INSTRUMENT_FAILED` not a traceback; the path appears only in the child's stderr tail, not in the message. Stated as the row held least confidently | exactly that | **HIT** |
| **P1c** | 6 of 8 fail at layer 3, 2 pass. Band 5-7. `anchor_check` passes degraded via the swallowed PIL import. A fourth failure class exists: `subject_profile` | **7 of 8 fail**, `anchor_check` passes, `subject_profile` is the fourth class and fires exactly where predicted | **MISS by one, inside band**, same unit error as P1b |
| **P1c** precondition | T2 is not measurable without moving the resolver too | correct — built that way and said so | **HIT** |
| **P2** row 1 | `facet-index q/claims/build` from an installed wheel: pass | q -> 0, claims -> 0, build from an empty dir -> **4** with a refusal naming both candidates and both markers | **HIT** |
| **P2** row 2 | the six MCP tools over stdio from a wheel are untested; predicted to pass from a checkout cwd and refuse from elsewhere. *"The row I most expect to be wrong"* | `facet-mcp` over stdio: `facet-record 0.3.1`, six tools, `record_health` -> `SERVING` from the checkout, `REFUSING` / `serving:false` from an empty dir | **HIT** |
| **P3** win-x64 | 165 MB, band 90-400 | **162.96 MB** | **HIT**, 1.3% off |
| **P3** linux-x64 | 200 MB, band 90-500 | derived **~544 MB** | **MISS, above band** |
| **P3** cap | both clear 2 GB by more than 4x | win 12.3x; linux ~3.7x derived | **HIT on win, MISS on linux** (3.7 < 4) |
| **P3** falsifier | named a build that fails outright as the second-most-likely outcome | it built and ran `--print-tools` | — |
| **P4** | NO. cp311 + cp312 at the pinned release, nothing at cp313+. Upper bound 3.12 or 3.13 | NO. 0.19.0 tops out at **cp312**; no sdist; nothing installable on 3.13 | **HIT**, at the low end of the stated band |
| **P5** | NO breakage, binary | no breakage: 7/7 `--help` at 0, compileall clean, 52 instrument-invoking tests pass | **HIT** |
| **P5** second-order | the two generic top-level names are real | real, and larger than predicted: 114 payload entries, 100 files under `diagnostics` | **HIT, understated** |

### The miss, and which law it belongs to

**P1b and P1c are the same error, one level below the one the dispatch warned about.** The
dispatch said *P1 is a conjunction wearing one number* and I split it by clause correctly —
every clause landed. What I got wrong is that **`measure_report` is one tool with two paths**,
and I counted the surviving *path* as a surviving *tool*. The denominator is served tools; the
thing that survives is a call shape. This is the **unit** family's ninth consecutive arc, in
its own new form: not the unit of the metric, not the population, not an unchecked property —
**the unit of the thing that passes**. The band held both times, which is the only reason the
number is still usable.

**P3's linux miss is the "unchecked property" form.** I banded linux above windows on the
general belief that manylinux wheels vendor more. They do — but `open3d` specifically is
**6.5x**, not the ~1.2x the band assumed, and I never checked the one package that dominates
the payload. One index query, before the prediction, would have moved the number.

**P4 was as blind as this arc allowed and hit at the low end**, on the strength of one
sentence of `ci.yml` prose plus the structural observation that `>=3.11` is unbounded above.

---

## 10. Findings nobody asked for

1. **`anchor_check` mislabels a missing dependency as a property of the caller's files**
   (section 6). Exit 0, empty `warnings`, wrong stated cause.
2. **`measure_report`'s comparison half is the only call path that survives every packaging
   layer**, and nothing said so. A change that gave it an instrument would close the one door
   a dependency-free install has, silently. T59 now notices.
3. **`subject_profile` is a fourth failure class** between "the instruments ship" and "the
   instruments run" (section 5).
4. **The frozen binary's `--print-tools` is green while every measurement verb fails**
   (section 8) — E24's exact shape, on a new artifact, before it reached a release.
5. **`open3d`'s hard requirements include `dash`, `flask`, `werkzeug`, `ipywidgets` and
   `nbformat`** — 230 MB of transitive tree that would enter CI's `pip-audit` population with
   a `[measure-full]` extra.
6. **T41's axis-D idempotency leg fails because this report names three instruments** — a
   document that is not about the census, by a seat not thinking about it, moved it anyway.
   Attribution measured by holding the file out and back in (section 11).
7. **The dispatch's 357.5 MB is not a floor for a clean install** — the same five packages
   cost 634.6 MB fresh, because the figure was taken in a shared environment (section 2).

---

## 11. Gates

| gate | evidence | verdict |
|---|---|---|
| **1. task 0's test fails before any fix** | wheel-tier measurement verb: `ModuleNotFoundError: No module named 'measure_mcp'`, 8 of 8. T58 before the registration: **4 failed, 1 passed**; the passing leg is the can-fail leg | **HELD — it failed** |
| **2. no tag, publish, release, `gh repo edit`, metadata change** | none run. Every irreversible command in the vicinity is absent from this session's history | **HELD** |
| **3. `MEASURE_VERSION` does not move; the five declarations stay in agreement** | `MEASURE_VERSION = "0.4.0"` unchanged; `pyproject 0.3.1` = `package.json 0.3.1` = `bin/facet.js 0.3.1` / tag `v0.3.1` = `record_mcp.SERVER_VERSION 0.3.1`. `git diff` over `tools/ pyproject.toml package.json bin/` is **empty** | **HELD** |
| **4. tests ride the commit** | `.mcp.json` changed; T58 rides it, T23 widened in the same commit. T59-T62 port this arc's measurements. 48 new tests + 3 net in T23; every file leads with a can-fail leg | **HELD** |
| **5. CI green, run id resolved before written** | **NOT YET RUN.** Nothing has been pushed at the time of writing, so no run id exists and none is written here | **NOT YET RUN — and expected RED, see gate 6** |
| **6. the count surfaces are the advisor's** | **DRIFT REPORTED, NOTHING TOUCHED.** Collected counts moved **808/768 -> 859/819**. T34 fails on 25 pins across `README.md`, `SHIP_GATE.md`, `site/src/site-config.ts`, `docs/advisor-kickoff.md` and the handbook page. The census — also an advisor surface, also out of scope — drifted on three rows because this report names three instruments. Neither edited, by instruction | **HELD — and it is why gate 5 will be red** |
| **7. the manifest holds** | `7,312 files / 17,072,807,610 bytes` before; `RECHECK before=7312 after=7312 added 0 removed 0 changed 0` after | **HELD** |

### Gate 5 and gate 6 collide, and gate 6 wins by instruction

Adding tests moves `pytest --collect-only`; T34 pins that number against surfaces this
dispatch reserves. **Neither can be green alone** — the same collision E30 reported and
CLAUDE.md ruled on. The advisor reconciles with the true numbers:

```
full       808 -> 859
hermetic   768 -> 819
```

**A correction to this arc's own commit message.** `943d2d5` states the new counts as
`818/778`. **Those numbers were never measured** — they were arithmetic done in the commit
message from a wrong delta, which is precisely the shape this repo forbids in a report and
which has no business in a commit either. The measured values are `859/819`, from
`pytest --collect-only -q` at both tiers. The wrong commit stands with this correction beside
it rather than being amended away.

### The suite

```
baseline, before this arc's tests    25 failed, 743 passed, 40 deselected in 378.94s
final, with them                     26 failed, 793 passed, 40 deselected in 360.06s
collected                            859 full / 819 hermetic
```

**Both runs' failures are enumerated, and neither is a measurement failing.**

- **25 x T34**, both runs — the count drift of section 6 above. In the baseline they were
  caused by this seat creating `test_t58_*.py` *while the run was in flight*, so T34's child
  collector saw a file the parent had not collected. That is E28's self-reference law,
  committed by hand: the check fired correctly on a real inconsistency I had just made.
- **1 x T41**, `test_t41_axis_d_is_idempotent_across_runs`, final run only. **Caused by this
  report.** Its drift list is `['anchor_compare.py', 'e14_topology.py', 'mesh_stats.py']` —
  the three instruments this document names by filename. Attribution measured rather than
  argued: with the report file moved out of the tree the leg **passes**; moved back, it
  **fails**. The census's corpus is `facet_index.record_markdown()`, so any markdown that
  cites an instrument moves axis D, and the committed `docs/instrument-census.json` becomes
  stale the moment it does.

  **Not regenerated.** `docs/instrument-census.json` and `docs/instrument-census.md` are
  named in this dispatch's own out-of-scope list as advisor surfaces, and the advisor seat has
  uncommitted edits to both in this working copy right now. The remedy is one command —
  `python tools/instrument_census.py --committed` — and it is the advisor's to run.

  E28 ruled that *an instrument that lives inside its own population must be checked against
  itself on every axis, each time*. This is that law reaching one step further out: a report
  that is not about the census, written by a seat that was not thinking about the census,
  moved it anyway — because naming a file is a citation whether or not you meant it as one.

### Two live seats

The advisor seat committed `218e410` and `e76c3f8` into this same working copy during this
session, rebuilding `docs/index/facet.db` and editing corpus files under `docs/`. `pytest.ini`
names that race explicitly on the `fold` marker. The baseline suite run was additionally
raced by **this seat**: `tests/test_t58_*.py` was created while it was in flight, so T34's
child collector saw a file the parent had not collected — the self-reference E28 ruled on,
committed again by hand. Both runs' T34 failures are the count drift above; every other test
in both runs passed.

---

## 12. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | every tier is a named wheel built from a named scratch tree, installed into a clean venv by a recorded command; predictions committed at `8e21cea` before the first build; every measured number in this report is reproducible from the tier table and the probe scripts |
| ANDON_AUTHORITY | **3** | gate 1's inverted halt was satisfied by watching the test fail before the fix rather than after; gate 6's collision is reported as a fired condition rather than smoothed into a green row; gate 5 is written `NOT YET RUN` rather than given a plausible id |
| NAMED_COMPENSATORS | **3** | nothing irreversible ran. Undo for the whole arc is `git revert 943d2d5` plus deleting the scratch directory. The two `__init__.py` probe files were written into the repo tree and deleted in the same session, with their absence now asserted by a test. The recorded trees were manifested before and after: 7,312 / 0 / 0 / 0 |
| DECOMPOSE_BY_SECRETS | **3** | four tasks, four things that change independently, and the tiers are built so that each one varies exactly one of them: T0->T1 the module, T1->T2 the instrument packaging and the path expression, T2->T2b one sibling module, T2b->LIGHT->FULL the dependency set |
| UNCERTAINTY_GATED_HUMANS | **3** | tasks 1 and 3 report both shapes with what each can refuse and what its message can state, and choose neither; the `anchor_check` defect is reported and not repaired, because repairing a served payload is a ruling; OQ2's operands are measured and its answer is left open |
| EXTERNAL_VERIFIER | **3** | every tier ran in a different process, a different interpreter, a different Python version in two cases, and a filesystem location that cannot see the checkout. The clean venv is the verifier: it cannot be talked out of a missing module |

---

## 13. What this report does not answer

- **OQ2 — Shape A or Shape B, at what tier.** The operands are all measured (sections 5-7);
  the choice is the ruling's. So is the sub-choice among A1/A2/A3.
- **The linux binary's real size.** Derived at ~544 MB from wheel bytes; only a linux build
  closes it, and `release.yml` already has the runner.
- **Whether `anchor_check`'s degradation should refuse, warn, or stay.** Reported, not
  repaired.
- **Whether a dependency refusal should be composed at the server.** Section 5 says the
  material for it is present at the call site and nothing composes it. That is an observation,
  not a recommendation.
- **The tag.** Steps 7 and 8 are the Director's, gated out by gate 2.

**Halt here.**
