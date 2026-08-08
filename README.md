<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/facet/readme.png" alt="facet" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/facet/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/facet/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="docs/experiments/"><img src="https://img.shields.io/badge/record-spec%20%E2%86%92%20report%20%E2%86%92%20ruling-8a6f3f" alt="The record"></a>
  <a href="https://mcp-tool-shop-org.github.io/facet/"><img src="https://img.shields.io/badge/landing%20page-live-2ea043" alt="Landing page"></a>
</p>

<p align="center">
  <strong>A styled 2D concept goes in. A textured 3D asset comes out.</strong><br>
  Local hardware end to end · no non-commercial licence anywhere in the chain
</p>

---

The style is applied **on the asset**, in texture space — not painted per view and
stitched together afterwards. Feed the route a form-exaggerated clay concept and it
returns a textured mesh whose colour came from a styled reference of *that* mesh,
with everything the reference could not see filled by a masked inpainting brush and
a surface-aware dilation.

Named for both halves of the problem: the polygons, and the face they have to hold.

## Where it stands

**Four accepted assets, across four subject classes, at zero credits.** Each was ruled
by the Director at his own zoom — on the GLB, or on full-size sheets — not by a metric
clearing a threshold.

| subject | class | accepted | reference / brush / dilation |
|---|---|---|---|
| **Character (W3)** | humanoid | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | vehicle, thin rigging | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | beast, wing membranes | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | prop, near-2D, grey-on-grey | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

Shares are of valid texels, and **they are not comparable across subjects** — a ship
hides most of itself from eye level and an animal hides half. Read each against its own
pre-registered reach ceiling, against which they land **86–93%**: the difference between
the rows is geometry, not regression. [Full numbers, with their
denominators](docs/handbook/subjects.md).

**It is a pipeline, not a one-character generator.** Contradict the specification on
eight named elements and the prompt wins **8 of 8** — median ΔE 46.3 against 6.2 on five
held controls — while the figure stays the same man. Structure is held by the mesh and
control; named attributes ride the prompt.

## The route

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

Stage by stage, with the reasoning for each: **[the handbook](docs/handbook/index.md)**.

## What makes it work

Six findings, each of which cost an experiment and each of which generalises beyond the
subject that produced it. [The long form, with the
measurements](docs/findings.md).

- **Form first, style second.** Reconstructors read surface noise as geometry. A clean
  sculpt-like clay with deliberately exaggerated planes comes back with better topology
  than a stylized sprite does; the styled twin is generated alongside and becomes the
  colour reference.
- **Frame the face, get a face.** A bust crop puts **3.1–4.5×** more polygons on the
  head, and the difference is structural — separated eyelids, a brow furrow, modelled
  nostril cavities — not sharper blur.
- **Twins belong to a mesh, not a character.** Reuse a twin across meshes and coverage
  collapses **62% → 22.7%**, because the arms project into empty space beside the model.
  Generate twins from the mesh you are about to texture, every time.
- **Identity belongs to the prompt.** A canon element not named in the prompt is arriving
  by accident and will leave the same way — measured when gold knee plates turned out to
  be reaching the image only through noise in a broken ControlNet.
- **Ask geometry, not a threshold.** Replacing a keyed mask with the exact raycast
  silhouette moved reference coverage **28.4% → 39.1%** of valid texels — strictly
  additive, no diffusion, no GPU. Corner-median keying has now failed three times here
  and is retired.
- **Cull what no camera can see, from the atlas and never the mesh.** 49% of atlas texels
  are invisible from outside; excluding those faces cut interpolation **68%**. Excluding
  rather than deleting makes the failure impossible instead of merely detectable.

## What is not solved

Named and measured, on the front page rather than in a footnote. [All of them, located in
code](docs/known-defects.md).

- **The blade band takes 0.00% of stage-1 reference** on all eight cameras — steel on a
  grey backdrop sits exactly on the key's own threshold. The union rescues 55.72%.
- **Stroke seams are not levelled.** A provenance boundary steps **5.5×** ordinary texture
  variation; the region the Director named steps **9.5×**.
- **Dilation bleeds between unrelated atlas islands** — 74.9% of dilated texels take their
  colour from another island, from a median 0.177 away on a figure 1.0 tall.
- **Every reconstruction on this route is a hollow double-walled shell**, walls ~two
  voxels. No volumetric predicate is valid on one.

## How this repo is run

The discipline is as much the product as the pipeline is, and it exists for a reason: an
earlier arc ran ten sessions that each judged their own output and wrote conclusions the
next session read as established fact. Nothing in that loop was checkable.

- **Spec before the work, report after, ruling last** — and the session that designs an
  experiment never grades its own results. Twenty experiments are in
  [the record](docs/experiments/).
- **Corrections land in place, beside the measurement that overturned them**, never as
  quiet deletions. Six inherited claims were falsified in the founding session alone, and
  all six are still readable next to what replaced them.
- **Failures stay in the repo with their reason.** [`tools/superseded/`](docs/tools.md)
  is not an archive — anyone can run those tools and watch them fail the same way.
- **A negative result is a full success**, reported and closed rather than tuned toward a
  number.
- **Tests ride the commit that touches the code** — 202 passing at two seats' hands, with
  paths-gated CI on the 194 hermetic ones.
- **The record is queryable.** A SQLite + FTS5 index over the whole trail, verified on
  four legs. It found a ruling count the prose had wrong at three sites, by counting the
  record itself.

## Where everything is

| | |
|---|---|
| **[The handbook](docs/handbook/index.md)** | the guide — the route stage by stage, the subjects, the profile system |
| **[The record](docs/experiments/)** | twenty experiments: spec, report, ruling, and every prediction stated before the measurement |
| **[What the route learned](docs/findings.md)** | the durable findings and the hard-won rules, in full |
| **[Status of every tool](docs/tools.md)** | what works, what is superseded, and the evidence for each |
| **[Known defects](docs/known-defects.md)** | everything not solved, measured and located in code |
| **[The arc, as it happened](docs/arc-history.md)** | the chronological history, corrections intact |
| **[CLAUDE.md](CLAUDE.md)** | how to work here — the roles, the rules, and what each one cost |

## Licence position

Every stage runs local and commercially clean: SDXL (OpenRAIL++), MV-Adapter (open),
open3d (Apache-2.0), spandrel (MIT), RealESRGAN anime6B (BSD-3), Blender, numpy, scipy,
trimesh.

Deliberately excluded, with the reason: **nvdiffrast** (non-commercial — enforced here
by a structural tripwire, not by attestation), **Hunyuan3D-Paint** (licence void in the
EU, UK and South Korea), **MVPaint** and **TEXGen** (no licence at all), and
**UltraSharp / SUPIR / StableSR** (non-commercial upscalers).

## Trust and threat model

facet runs entirely on your own machine — every tool is a script you invoke against
paths you type, so the useful question is not *what permissions does this app request*
but *what do these scripts do to your machine*. Answered by measurement, with every
sweep re-runnable; the full policy is in [SECURITY.md](SECURITY.md):

- **Data touched:** meshes, textures, images and JSON on local disk, at paths you
  pass on the command line. Plus `docs/index/facet.db`, which is *derived* — it holds
  nothing that was not already a file in this repo, and `facet_index.py build`
  regenerates it from scratch.
- **Data NOT touched:** no credentials, ever. Nothing here reads, stores or transmits
  a token, key or password, and none is present in the tree — swept for
  provider-prefixed keys, GitHub PATs, Slack tokens, AWS key ids, private-key blocks,
  bearer tokens and inline `api_key`/`password` assignments, **zero matches**, no
  credential-shaped file tracked.
- **No telemetry.** None collected, none sent. There is no opt-out because there is
  nothing to opt out of.
- **Network egress:** two tools of thirty-four open a socket — `restylize_views.py`
  and `texpass_brush.py` — and both call a ComfyUI HTTP API at `--host`, **default
  `127.0.0.1:8188`**. Nothing else in `tools/` makes a network call.
- **Permissions:** ordinary user. No elevation, no service install, no system-settings
  or registry writes.

Three sharp edges are disclosed rather than claimed away, because a security note that
only lists reassurances is not a threat model: **file operations are not sandboxed**
(a tool writes wherever its arguments say); **absolute local paths are baked into many
tools and docs** — 114 occurrences across 26 files, not secrets but a disclosure of one
machine's layout, and the reason most tools will not run unmodified elsewhere; and
**unexpected failures surface as Python tracebacks**, with no `--debug` gate and no
structured error shape. Deliberate halts are `ANDON:` messages carrying the measurement
that fired them. That is the research-instrument contract, and
[SHIP_GATE.md](SHIP_GATE.md) records exactly when it stops being good enough.

**Support status:** this repo is developed in the open, at one rig, by one director
and a rotating pair of advisor and executor sessions. `main` is the only supported
state. There is no release channel, no backport policy, and no SLA — what there is
instead is the record: every claim sits next to the code that produces it, and
[docs/experiments](docs/experiments/) carries the spec, the report and the ruling for
each one.

## Requirements

Blender 5.x, Python 3.11+ with `numpy`, `scipy`, `trimesh`, `open3d`, `Pillow`,
`spandrel`, `torch`. A local ComfyUI install is needed only for the inpainting brush.
Developed against an RTX 5090; VRAM headroom matters more than raw speed.

CI runs the hermetic subset of the suite on **ubuntu-latest / Python 3.12** with
pinned installs (`.github/workflows/ci.yml`); the artifacts tier needs the recorded
trees under `E:\AI\training`, which are not in git, so CI deselects them by design.
Locally, `python -m pytest` runs all **202** tests and `python -m pytest -m "not artifacts"`
runs the **194** CI reproduces.

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
