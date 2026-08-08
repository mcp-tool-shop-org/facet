# Brand assets

## The logo — the clay wordmark

The canonical mark lives in the org's brand registry at
`mcp-tool-shop-org/brand/logos/facet/readme.png` (1344×1024), and the README
references it there. It is the word **FACET** sculpted in clay.

That is the right mark for this repo, and the reason is structural rather than
decorative: **the route begins with a form-exaggerated clay concept.** Everything
downstream — the reconstruction, the twins, the projection, the brush — exists to
carry that clay into a textured asset. A clay wordmark says what the first stage is,
in the material the first stage is made of.

*Chosen and pushed by the Director, 2026-08-08.*

## The four-accepted-assets sheet

`four-accepted-assets.png` is **not the logo**. It is a showcase sheet, and it is the
route's own output rather than an illustration of it: the four assets the Director
accepted at Gate 1, one per subject class, each cut from the **exact silhouette** its
dense export ships beside it and composited onto a flat ground.

| quadrant | subject | camera | accepted |
|---|---|---|---|
| top-left | galleon | `y+030_e+00` | [E04 Ruling 29](../experiments/E04-ruling.md) — 2026-08-05 |
| top-right | dragon | `y+045_e+00` | [E12 Ruling 28](../experiments/E12-ruling.md) — 2026-08-07 |
| bottom-left | character (W3) | `y+030_e+00` | [E08 Amendment 35](../experiments/E08-ruling-gate0.md) — 2026-08-04 |
| bottom-right | longsword | `y+000_e+00` | [E14 Ruling 32](../experiments/E14-ruling.md) — 2026-08-08 |

Every generation in all four arcs ran at **zero credits**.

It carries a wordmark of its own because it was authored as a logo candidate before
the clay mark landed. That history stays recorded here rather than tidied away, in
the same spirit as `tools/superseded/` — and the sheet is kept because it has a real
job that is not the logo's job: **showing what the route produced, checkably.**

### Rebuilding it

```bash
python docs/brand/make_asset_sheet.py --out docs/brand/four-accepted-assets.png
```

Deterministic by construction — fixed sources, fixed cameras, fixed layout, no
sampling and no randomness — so re-running it on the same export trees returns the
same bytes. That matters here for a reason the record paid for: *a recipe that does
not reproduce its output is not a recipe*, learned when the canon twin turned out to
be a file we could copy and could not recreate.

The generator reads the dense turnaround trees under `E:\AI\training`, which are the
recorded artifacts of E04 / E08 / E12 / E14 and are **not in git**. `--root` points
elsewhere if they move. It refuses rather than guesses: a silhouette that does not
match its render's dimensions, and an empty silhouette, both halt with an `ANDON:`
line.

**Why the silhouette and not a colour key.** Keying was retired in this repo three
times — painted concept art has a gradient and a cast shadow, a clay render is grey
on grey, and a diffusion model paints a lit studio backdrop. The dense export already
ships the raycast silhouette per camera, which answers *is there surface here*
exactly. There was no reason to ask a threshold a question geometry had already
answered.
