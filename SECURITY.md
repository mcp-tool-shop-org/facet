# Security Policy

## What facet is, for the purposes of this policy

facet is a set of local Python instruments that turn a styled 2D concept into a
textured 3D asset, plus the measured record of every experiment that built them.
Every tool is invoked as `python tools/<name>.py` against paths the operator types,
and nothing in the chain runs off this machine.

That shapes the whole policy below: the attack surface is the surface of *running
these scripts on your own machine against your own files*, and this document's job
is to say exactly what they do.

## Supported versions

| Version | Supported |
|---------|-----------|
| `main` | Yes — the record is the product; `main` is the only supported state |

`main` carries the current state of every instrument and the evidence behind it.
`v0.1.0` is cut at the close of the E19 treatment — see [CHANGELOG.md](CHANGELOG.md)
for what it marks and what it deliberately does not.

## Reporting a vulnerability

Email: **64996768+mcp-tool-shop@users.noreply.github.com**

Include:

- Description of the vulnerability
- Steps to reproduce
- The commit sha affected
- Potential impact

### Response timeline

| Action | Target |
|--------|--------|
| Acknowledge report | 48 hours |
| Assess severity | 7 days |
| Release fix | 30 days |

## Threat model — measured, not asserted

The same standard the rest of this repo runs under applies here: every claim below
was checked against the tree rather than assumed. The commands are given so you can
re-run them.

### Data touched

- **Meshes, textures, images and JSON on local disk**, at paths the operator passes
  on the command line. The tools read and write freely inside whatever directory
  you name.
- **`docs/index/facet.db`** — a SQLite+FTS5 index *derived* from the repo's own
  markdown. `tools/facet_index.py build` regenerates it from scratch; it holds no
  input that did not come from files already in this repo.

### Data NOT touched

- **No credentials of any kind.** The tools do not read, store, or transmit
  tokens, keys, or passwords, and none are present in the tree — swept for
  provider-prefixed keys, `github_pat_`/`ghp_`, Slack tokens, AWS access-key ids,
  private-key blocks, bearer tokens, and inline `api_key`/`password` assignments:
  **zero matches**. No `.env`, `.pem` or credential-shaped file is tracked.
- **No telemetry, analytics, crash reporting, or usage counting.** None is
  collected, and none is sent. There is no opt-out because there is nothing to opt
  out of.

### Network egress

Two tools of thirty-five make network calls, and both call the **same local
endpoint**:

| tool | what it calls |
|---|---|
| `tools/restylize_views.py` | a ComfyUI HTTP API at `--host`, **default `127.0.0.1:8188`** |
| `tools/texpass_brush.py` | the same ComfyUI HTTP API, same default |

Nothing else in `tools/` opens a socket. Both hosts are operator-supplied, so
pointing them at a remote ComfyUI is possible and is your decision — the default is
loopback and the repo never changes it for you.

Image *generation* for the experiments runs on Comfy Cloud, invoked by the operator
outside these scripts. No credential for that service lives in this repo.

### Permissions required

Ordinary user permissions. No elevation, no service installation, no registry or
system-settings writes, no scheduled tasks. The tools need read/write on the
directories you point them at, a GPU for the generation and reconstruction stages,
and Blender on `PATH` (or its absolute path) for the render and mesh stages.

### Known sharp edges, disclosed rather than claimed away

- **File operations are not sandboxed.** There is no allow-list of directories and
  no confinement — a tool writes wherever its arguments say. Treat these as scripts
  you are running deliberately, not as a hardened CLI. Point them at scratch trees.
- **Absolute local paths are baked into many tools and docs** (`E:\AI\...`,
  `E:\AI-Models\...` — 114 occurrences across 26 files). They are not secrets, but
  they do disclose one machine's directory layout, and they mean most tools will
  not run unmodified on another rig.
- **Unexpected failures surface as Python tracebacks — in the 35 unpublished
  research scripts.** ⚑ **Corrected at 0.2.0**, and the narrowing is the point:
  the two commands facet actually installs, `facet-index` and `facet-mcp`, no
  longer do this. An unexpected exception leaves them as a structured failure
  (`message` / `cause` / `hint`) and `--debug` restores the traceback; a fired
  gate leaves as `GATE_FIRED` carrying its own `ANDON:` text. Measured before and
  after through a subprocess — [E21](docs/experiments/E21-cli-contract-report.md),
  T29. Everything under `tools/` that is *not* one of those two still prints a raw
  traceback and still carries no `--debug`, deliberately: that is the
  research-instrument contract, and retrofitting an error registry across the
  instruments that produced four accepted assets is a large change to
  accepted-asset tooling bought for a checkbox.
- **No `--allow-*` escape hatches, by ruling.** Where a tool performs an
  irreversible step, the gate lives *inside* that tool with no skip flag — the
  practice earned in E08 Amendment 32, after a shell chain walked past a fired
  gate and committed 47,020 texels anyway. An opt-in override flag would be a
  regression against that ruling, not an improvement.

## Scope

In scope: the tools in `tools/`, the index in `tools/facet_index.py`, the test
suite in `tests/`, and the CI workflow.

Out of scope: the third-party models and runtimes the pipeline invokes (ComfyUI,
Blender, TRELLIS.2, SDXL, open3d, spandrel, RealESRGAN). Their licence positions
are stated in the README; their security is theirs.
