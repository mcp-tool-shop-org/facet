**The measurement server ships.**

Four releases put a record index in the wheel and left the eight measurement tools
behind. `pip install facet-mcp` gave you `facet-index` and `facet-mcp` — and nothing
that measures a mesh, because the wheel held **two `.py` files** while the served tools
invoke their instruments as *subprocesses*. There was nothing to invoke.

It was invisible because this repo **is** the checkout: the tool worked where it was
built and had never been anywhere else.

```
pip install facet-mcp[measure]
```

```
mesh_stats  <a control mesh>   ->  faces 786432, components 1, watertight true
                                   + an identity envelope carrying the instrument's
                                     own sha256
```

Measured from a **clean venv with no checkout on the machine**, by running a verb — never
`--help`, which is how four green pipelines missed the last one.

## Two extras, and what you get depends on your Python

`[measure]` is the tier that resolves on **every** Python this package claims — four
tools, no heavy native dependency. `[measure-full]` adds the four geometry tools, which
need `open3d`.

| your Python | `[measure-full]` gives you |
|---|---|
| **3.11 / 3.12** | **all eight** — `open3d` installs from PyPI |
| **3.13** | four; `mesh_stats` · `mesh_topology` · `measure_report` · `anchor_check` |

`open3d` 0.19.0 is the latest *release* and publishes cp38–cp312 wheels with **no sdist**.
The requirement therefore carries `python_version < "3.13"`, so on 3.13 the install
**succeeds without it** and `reach_ceiling`, `thin_extent_curve`, `offsurface_rate` and
`texel_provenance` exit **`4` REFUSED** naming what they need — instead of the whole
install failing on a resolver error.

**All eight on 3.13** is one documented command, because Open3D ships current cp313 wheels
on its rolling devel channel and a direct URL is legal on a command line even though it
cannot appear in published metadata:

```bash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ Linux's filename is stable; **Windows and macOS devel wheels are `+<sha>`-suffixed** and
move as `main` moves. **That devel build is what this route's own open3d-dependent numbers
were measured against** — a real comparability boundary, since the identity envelope
records the instrument's hash and not its dependency set.

## The defect underneath, which was this project's own, twice

`measure_mcp` carried `REPO = dirname(__file__)`'s parent — in a wheel, `<venv>/Lib`.
That is **v0.3.1's defect verbatim**, in a file written *after* v0.3.1 fixed it
elsewhere. The consumer sweep that found the others could not have caught it, because
the consumer did not exist yet.

The repair is a distinction the first fix never drew:

- **`REPO` answers *where is the corpus*** — the two-marker property test, returning
  `None` rather than guessing.
- **`tool_path` answers *where is the instrument*** — resolved **beside the module**.
  One expression correct in a checkout and an install, because the record markers key on
  a corpus that cannot ship, while instruments are code that does.

The identity envelope now builds its path the same way, because two path expressions for
one file is how a payload comes to certify an instrument that did not run.

## Also in this release

- **The measurement server is reachable over MCP at all.** It was declared in no config,
  so no session could reach it. Registered **with a test** — a subprocess over stdio that
  asserts the payload's instrument sha256 equals the file on disk.
- **A missing dependency is a refusal, not a runtime error** (exit `4`), which is what
  makes a four-of-eight install usable rather than mysterious.
- **The polish arc's eight per-profile anchors** land as permanent tests — and one
  **halted**: a route tool had changed under an already-accepted asset, caught on the
  gate's first outing.
- **A reconstruction noise floor**, which this record did not have. Three runs of one
  input at one seed are bit-identical through remeshing and diverge in decimation:
  faces ±0.27%, shells ±1, non-manifold edges ±18.
- **The hollow-shell finding's reach is narrowed.** Its evidence base is prop, beast and
  vehicle — **no character** — so on the character class the wall structure is ruled
  **unmeasured**, which is not a claim of solidity. Every consumer-facing clause is
  unchanged: a volumetric predicate still meets a shell.

Full detail, with the ruling behind each claim: [CHANGELOG.md](../CHANGELOG.md).

## Compensators

| action | irreversible? | compensator | owner |
|---|---|---|---|
| `npm publish` | **yes** | `npm deprecate @mcptoolshop/facet@0.4.0` and publish a fixed patch; the version stays visible, marked | the publishing session |
| PyPI upload | **yes** | `yank` the release (it stays resolvable for pins, but is not selected for new installs); publish a fixed patch | the publishing session |
| `gh release create` + tag | **yes, in practice** | `gh release delete v0.4.0` and delete the tag; anyone who already fetched the binary keeps it, so treat as one-way | the publishing session |
| the version bump commit | no | `git revert` — five declarations move together and T27 refuses a mismatch | any session |
| the wheel/binary build | no | artifacts are derived; rebuild from the tag | any session |

**The three irreversible rows are the Director's act.** Nothing in the preparation for
this release fired one.
