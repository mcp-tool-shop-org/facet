# E31 predictions — committed BEFORE the first wheel is built

**Written by the executor, 2026-08-09**, before `python -m build` was run once, before any
venv was created, and before PyPI was queried for anything. The commit that carries this file
is the anchor; nothing below was edited after a result was seen.

---

## Disclosure — what was read before these numbers were written

Reading the mechanism is required here (E29's law: *read the mechanism you are predicting
about*), so most rows below are **not blind in the strict sense**. What was opened, in order,
before a single number:

| read | which row it informs |
|---|---|
| `pyproject.toml` (all 51 lines) | P1 clause 0, P5 |
| `.mcp.json`, `bin/facet.js` | task 0-pre, P3 |
| `tools/measure_mcp.py` — docstring, `REPO`, `envelope`, `run_instrument`, `measure_report`, `anchor_check`, `WRAPPED`, `_main` | P1, all clauses |
| `tools/record_mcp.py:95-155`, `tools/facet_index.py:85-175` | P2 |
| import lines of all eight instruments, plus `subject_profile.py` | P1 clause 3 |
| `tools/verify/anchor_compare.py:90-135` | P1 clause 3 — the lazy-import branch |
| `tests/test_t32_installed_wheel.py` (all 348 lines) | P2 |
| `.github/workflows/ci.yml`, `release.yml` | P2, P3 |

**Blind rows: P3 and P4.** No PyInstaller build has been run with the instruments, and PyPI
has not been asked anything about `open3d`. P4 is informed by *one sentence of prose* —
`ci.yml`'s comment that the runner pins 3.12 because "the rig runs a local 0.19 build" — and
that prose is itself an inherited claim, unverified at this seat. It is disclosed rather than
leaned on.

**No calibration haircut.** E23's seat halved an untutored estimate on this repo's own
"densities run 2x high" lesson and moved *away* from the truth. Every number below is stated
as reasoned.

---

## 0. The five prediction laws, applied before any number

| law (CLAUDE.md) | how it bites here | what I did |
|---|---|---|
| name the **unit** | "fails" has three readings: raises, returns a narrower payload, or exits non-zero | section 1 defines *fail* as one thing and says which |
| check the **population** is real | "the eight served tools from a clean install" — **there is no such population today**, because the module that defines them is not in the wheel | P1 is split: P1a is today's wheel, P1b/P1c are counterfactual tiers I construct |
| check the **property is defined** for every member | two of the eight do not invoke an instrument on every path (`measure_report` comparison-only; `anchor_check` byte tier) | both predicted separately from the six that always shell out |
| a **conjunction** tracks its rarest clause | P1 is exactly this — a tool fails if *any* layer fails | each layer predicted alone, then the join, and the join read off the rarest clause |
| the **instrument must still express the question** | the three-layer attribution cannot be asked of today's wheel at all | stated as the headline, not smoothed into a layer number |

---

## 1. Definitions, fixed before the measurement

**"Fail"** = the served tool, invoked through the server's own call path with otherwise-valid
arguments (a real subject file supplied by the caller as an absolute path), does **not** return
a payload `dict`. A raised `ToolError`, a raised `MeasureError`, or any unhandled exception is
a fail. A payload that comes back *narrower than it would in the checkout* is **not** a fail —
it is a separate observation and section 4 names it.

**The three layers**, in the order a call meets them:

1. **the resolver** — `measure_mcp.REPO = os.path.dirname(HERE)` (`measure_mcp.py:139`).
   Attributed here when the path the failure names lies **outside the install root**
   (`<venv>\Lib\tools\...`), which is the pre-E24 geometry.
2. **the missing instrument file** — the path named lies **inside the install root**
   (`<venv>\Lib\site-packages\...`) and is simply absent.
3. **a missing third-party import** — the instrument file exists and its subprocess dies with
   `ModuleNotFoundError`.

The discriminator between layers 1 and 2 is *which path the refusal prints*, so the test must
capture that string. Layer 3 cannot be reached until layers 1 and 2 pass.

**Three tiers will be built**, because the three-layer question is undefined on the first:

| tier | what it is |
|---|---|
| **T0** | the wheel as this tree builds it today |
| **T1** | T0 + `measure_mcp` added to `py-modules`, nothing else |
| **T2** | T1 + `diagnostics/` and `verify/` packaged, no dependency added |

---

## 2. P1 — of the eight, how many fail from a clean install, and where

### P1a — T0, today's wheel. **8 of 8 fail.** Band 8-8.

Unit: served tools, of 8. Denominator: the eight names in `measure_mcp.TOOL_ORDER`.

**And none of the three layers is the answer.** `pyproject.toml:50` names two py-modules and
`measure_mcp` is not one of them, so the module is absent from the artifact and there is no
call path to reach a resolver with. The honest layer is a **layer 0 — the module does not
ship**, upstream of all three the dispatch names. I predict the failure mode is
`ModuleNotFoundError: measure_mcp` and that T32's existing assertion (payload ==
`["facet_index.py", "record_mcp.py"]`) reproduces exactly.

*Falsifier:* the built wheel contains `measure_mcp.py`, or any of the eight returns a payload.

### P1b — T1, module ships, nothing else. **7 of 8 fail, all seven at layer 1.** Band 6-8.

Clause by clause, each predicted alone:

| clause | prediction | reasoning |
|---|---|---|
| does the module **import** in a clean venv? | **yes** | it needs `facet_index` (a sibling top-level module, reachable via its own `HERE` insert) and `mcp` (declared). Nothing else at module level. |
| does the **resolver** point somewhere real? | **no**, for all 8 | `dirname(site-packages)` = `<venv>\Lib`; `tool_path()` joins `tools/...` onto it. Pre-E24 geometry, verbatim. |
| how many tools **must** touch that path? | **7 of 8** | six always call `run_instrument`; `measure_report`'s *sheet* half does. `envelope()` also sha256s the instrument file, so even a tool returning early would need it. |
| how many **never** touch it? | **1** | `measure_report(left, right)` with no `sheet` passes `instrument_rel=None` to `envelope`, so `inst` is `None` and no path is joined. Pure stdlib over two caller-supplied dicts. |

**Join: 7 fail, 1 passes.** The join tracks the rarest clause, and the rare clause here is
*does this tool have an instrument to miss* — one member does not, on one of its two paths.

I further predict the seven fail as `INSTRUMENT_FAILED` (a structured `ToolError`) rather than
as a raw traceback, because `run_instrument` reaches the missing file by handing it to a
subprocess that exits 2, and that branch is caught. **The path `<venv>\Lib\tools\...` will
appear only inside the child's stderr tail**, not in the refusal's own message — so the layer
is attributable but the message does not state it. That is a prediction about refusal
*quality*, and it is the one I hold least confidently.

*Falsifier:* any of the seven returning a payload; `measure_report` comparison-only raising;
any failure naming a path inside site-packages.

### P1c — T2, instruments ship, no dependency added. **6 of 8 fail, all six at layer 3.** Band 5-7.

| clause | prediction | reasoning |
|---|---|---|
| does the resolver find them once they ship? | **no — still layer 1 unless the resolver moves too** | T2 as stated puts the files in site-packages while `REPO` still points at `<venv>\Lib`. **I therefore predict T2 is not measurable without the package-relative resolver**, will build it that way, and say so. |
| with the resolver fixed, how many die on imports? | **6** | `numpy` is at module level in seven of the eight instruments; `open3d` in four; `PIL` in `gate1_sheet`. None is installed in a clean venv. |
| `anchor_check` | **passes, degraded** | `anchor_compare.py:100-108` wraps `from PIL import Image` in `try/except Exception`, so a missing PIL is caught and read as "not an image". The byte tier is `hashlib` + `os` only, and the `numpy` import at :120 sits inside the `both_images` branch that never runs. |
| `measure_report` comparison-only | **passes** | unchanged from P1b. |
| `mesh_stats` — a **fourth** failure class | **predicted to exist** | `verify/mesh_stats.py:38-39` inserts `dirname(dirname(__file__))` and does `import subject_profile`. Packaging `diagnostics/` and `verify/` does **not** ship `tools/subject_profile.py`. In an install that insert points at site-packages, so the import resolves *only if* `subject_profile` also ships as a py-module. I predict this gap is real and that naming it is worth more than the count. |

**Join: 6 fail, 2 pass.**

---

## 3. P2 — does `record_mcp`'s own wheel-tier verb pass today?

**Prediction: the verbs that are tested pass; the server's own six tools have never been run
from a wheel, and I predict they pass from a checkout cwd and refuse from outside it.**

The unit matters and the dispatch's phrase is ambiguous, so both readings get a number:

| reading | prediction | basis |
|---|---|---|
| `facet-index q` / `claims` / `build` from an installed wheel | **pass** | T32's five `slow` legs already do exactly this, `ci.yml` pins `build==1.5.0` so they run on every push, and `release.yml`'s verify step runs the same four commands. This is *covered*, not unmeasured. |
| `facet-mcp`'s **six MCP tools**, over stdio, from a wheel | **untested today; predicted to pass from a checkout cwd, exit-code-4 refusal from elsewhere** | no test in the harness starts the installed server and calls a tool. `--print-tools` is a banner and `release.yml` says so in its own comment. The resolver reaches them through `facet_index.REPO`, which E24 fixed — nothing has exercised it. |

Confidence on the second row is **moderate**, and the reason it is not high is precisely
task 0-pre: the same "the code path runs, the transport is unexercised" gap E29 Ruling 7 found
on the measurement server exists here on the record server.

*Falsifier:* any of the six tools raising from an installed `facet-mcp` run inside the
checkout, or returning a payload from outside one.

---

## 4. P3 — the PyInstaller binary with instruments, per platform  *(BLIND)*

**The floor I reason from, and why it is a floor:** the binary that exists today is **21 MB**
(`bin/facet.js:16`). That is a Python runtime plus `mcp` plus two stdlib-only modules, and
nothing this arc adds can make it smaller. **357.5 MB of installed site-packages is not a floor
for the binary** in either direction: PyInstaller deflates each collected file, and it also
adds an interpreter that the 357.5 MB figure does not contain.

| platform | point estimate | band |
|---|---:|---|
| `win-x64` | **165 MB** | 90-400 MB |
| `linux-x64` | **200 MB** | 90-500 MB |

Reasoning: the collected payload is dominated by native extension modules (`open3d` 207.1 MB,
`scipy` 99.9, `numpy` 25.9 on this rig). Native `.pyd`/`.so` deflate at roughly 2-2.5x, pure
Python at 3-4x, so a ~330 MB collection lands near 140 MB, plus the 21 MB base. Linux is banded
higher because manylinux wheels vendor more shared objects than the Windows ones.

**Against GitHub's 2 GB per-asset cap: I predict both platforms clear it by more than 4x.**
The sentence at `bin/facet.js:18` is voided as *stated* — the dependencies stop being "stdlib,
sqlite3 and mcp" — while its *conclusion* (binaries stay viable) survives. Those are two
different claims and only the first is falsified by shipping the server.

*Falsifier:* either binary above 2 GB, or either below 21 MB, or the build failing to produce
one at all — the last being a real possibility, since `open3d` and `trimesh` both load data
files by path at import time and PyInstaller's analysis does not always follow that.

---

## 5. P4 — does `open3d` publish a wheel for every Python in `requires-python = ">=3.11"`?  *(BLIND to the index)*

**Prediction: NO.** Point estimate: `open3d` publishes cp311 and cp312 wheels at its pinned
release and **does not** publish cp313 or later. Band: the upper bound of open3d's support is
**3.12 or 3.13**; I do not predict it reaches 3.14.

Two reasons, and the second is structural. `ci.yml`'s own comment says the runner pins 3.12
rather than the rig's Python because *"the rig runs a local 0.19 build"* — which is what "no
wheel for this Python" looks like from the inside. And `>=3.11` is **unbounded above**, so the
question as asked can only be answered NO by any dependency whose support matrix is finite.
That is not a fact about `open3d`; it is a fact about the constraint, and it holds for `numpy`,
`scipy` and `PIL` too.

*Falsifier:* PyPI shows `open3d` wheels for every cp3XX tag >= 311 that exists.

**If NO, what it constrains.** A `[measure]` extras group that hard-requires `open3d` makes
`pip install facet-mcp[measure]` fail on a Python the package's own `requires-python` says it
supports. The 4/4 split is the lever — the four tools that do not need `open3d` include both
anchor tools.

---

## 6. P5 — does packaging the instruments break any recorded `python tools/<name>.py`?

**Prediction: NO. Binary.**

Reasoning: `python path/to/script.py` puts the *script's own directory* at `sys.path[0]`
whether or not that directory also holds an `__init__.py`. Packaging changes `pyproject.toml`
and adds two `__init__.py` files; it changes no import statement, no `sys.path` insert, and no
file's location. The one cross-directory import among the eight — `mesh_stats.py:38-39`
inserting `tools/` to reach `subject_profile` — computes its path from `__file__` and is
untouched by packaging.

*Falsifier, stated so it can fire:* any invocation that exits 0 on the tree at HEAD and
non-zero after the packaging change, on identical inputs. The population I will run it against:
`--help` on **every** file under `tools/diagnostics/` and `tools/verify/`, plus the full test
suite (which invokes instruments for real), before and after.

**The second-order cost is not a breakage, and I predict it is real:** under
`package-dir = { "" = "tools" }`, packaging these ships **top-level importable packages named
`diagnostics` and `verify`** into every environment that installs `facet-mcp`. I predict both
names are unclaimed as PyPI *distributions* but that the *import* names are generic enough to
shadow a module in a consumer's own tree. That is an option to report, not a breakage to count.

---

## 7. What would make me wrong in a way that matters

- **P1b's count of 1 passing tool rests on one branch** — `measure_report`'s
  `instrument_rel=None`. If `envelope` is reached with a non-`None` value on that path, T1 is
  8/8 and the rarest-clause reasoning was decoration.
- **P1c's `anchor_check` pass rests on a swallowed `ImportError`.** If PIL's absence surfaces
  as something `except Exception` does not catch, or if `measure_mcp` post-processes the
  payload in a way that needs the pixel tier, it fails and P1c is 7.
- **P3's band is wide because I have never built this binary.** A build that fails outright on
  `open3d`'s data files is inside the band as stated and is the outcome I would bet second on.
- **P2's second row is the one I most expect to be wrong**, because it is the row nothing has
  ever run.
