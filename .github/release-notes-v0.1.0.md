**Four accepted assets, four subject classes, zero credits.**

facet turns a styled 2D concept into a textured 3D asset, with the style applied **on
the asset** in texture space rather than painted per view and stitched. Feed it a
form-exaggerated clay concept and it returns a textured mesh whose colour came from a
styled reference of *that* mesh, with everything the reference could not see filled by
a masked inpainting brush and a surface-aware dilation.

Every stage runs on local hardware, and no non-commercial licence appears anywhere in
the chain.

## Install

The record index ships as an MCP server, so an assistant can query the evidence trail
instead of reading it:

```bash
npx @mcptoolshop/facet            # zero-prerequisite; bootstraps a managed venv
pipx install facet-mcp==0.1.0     # or install the Python package directly
```

Two commands come with it — `facet-mcp` (the stdio MCP server, six tools) and
`facet-index` (`build` / `verify` / `q` / `claims`).

## The four assets

Each was accepted by the Director at his own zoom — on the finished GLB, or on
full-size sheets — never by a metric clearing a threshold.

| subject | class | accepted | reference / brush / dilation |
|---|---|---|---|
| Character (W3) | humanoid | 2026-08-04 | 68.8 / 4.2 / 27.0 |
| Galleon | vehicle, thin rigging | 2026-08-05 | 36.89 / 6.87 / 56.24 |
| Dragon | beast, wing membranes | 2026-08-07 | 44.15 / 3.07 / 52.78 |
| Longsword | prop, near-2D, grey-on-grey | 2026-08-08 | 45.25 / 2.07 / 52.68 |

Shares are of valid texels and **are not comparable across subjects** — a ship hides
most of itself from eye level and an animal hides half. Read each against its own
pre-registered reach ceiling, against which they land 86–93%.

## It is a pipeline, not a one-character generator

Contradict the specification on eight named elements and the prompt wins **8 of 8** —
median ΔE 46.3 against 6.2 on five held controls — while the figure stays the same man.
Structure is held by the mesh and the control; named attributes ride the prompt.

## The record is the product as much as the pipeline is

- **213 tests** at two seats' hands, 205 of them hermetic and reproduced by paths-gated
  CI on every push.
- **A four-leg-verified SQLite + FTS5 index** over the whole evidence trail: byte-identical
  determinism across interpreters, counts checked against independently written greps,
  zero dangling pointers, and a seeded question set that grows with the record. It found
  a ruling count the prose had wrong at three sites, by counting the record itself.
- **Twenty experiments**, each with its predictions written down *before* the measurement,
  and its ruling written by a session that did not run it.

## What this release does NOT assert

This is `0.1.0` deliberately. The texture stage is not finished, and the open defects are
on the front page rather than in a footnote: the blade band takes 0.00% of stage-1
reference on all eight cameras, stroke seams are not levelled, dilation bleeds between
unrelated atlas islands, and every reconstruction on this route is a hollow double-walled
shell. Three testability seams are dispatched and untaken, and the repo's own
highest-value open question — `fit_background` at frame-edge figures — has never been
looked at.

A `1.0.0` would assert a stability this route has not earned. Four accepted assets earn a
first release.

---

**Compensators:** `gh release delete v0.1.0 --yes` · `git push --delete origin v0.1.0` ·
`git tag -d v0.1.0` · `npm unpublish @mcptoolshop/facet@0.1.0` (72h) or `npm deprecate`
after · PyPI releases cannot be re-uploaded at the same version — yank with
`pypi.org` project settings.
