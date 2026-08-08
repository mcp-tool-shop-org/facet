# The mark

`facet-logo.png` is not an invented device. It is **the route's own output**: the
four assets the Director accepted at Gate 1, one per subject class, each cut from
the **exact silhouette** its dense export ships beside it and composited onto a flat
ground.

That is deliberate. The rest of this repo holds every claim to "measured, not
asserted"; a logo drawn to *suggest* what the pipeline can do would be the one
surface where that standard lapsed. This one makes the same claim the README makes,
and a reader can check it.

| quadrant | subject | camera | accepted |
|---|---|---|---|
| top-left | galleon | `y+030_e+00` | [E04 Ruling 29](../experiments/E04-ruling.md) — 2026-08-05 |
| top-right | dragon | `y+045_e+00` | [E12 Ruling 28](../experiments/E12-ruling.md) — 2026-08-07 |
| bottom-left | character (W3) | `y+030_e+00` | [E08 Amendment 35](../experiments/E08-ruling-gate0.md) — 2026-08-04 |
| bottom-right | longsword | `y+000_e+00` | [E14 Ruling 32](../experiments/E14-ruling.md) — 2026-08-08 |

Every generation in all four arcs ran at **zero credits**.

## Rebuilding it

```bash
python docs/brand/make_logo.py --out docs/brand/facet-logo.png
```

Deterministic by construction — fixed sources, fixed cameras, fixed layout, no
sampling and no randomness — so re-running it on the same export trees returns the
same bytes. That matters here for a reason the record paid for: *a recipe that does
not reproduce its output is not a recipe*, learned when the canon twin turned out to
be a file we could copy and could not recreate.

The generator reads the dense turnaround trees under `E:\AI\training`, which are the
recorded artifacts of E04 / E08 / E12 / E14 and are **not in git**. `--root` points
elsewhere if they move. It refuses rather than guesses: a silhouette that does not
match its render's dimensions, or an empty one, halts with an `ANDON:` line.

**Why the silhouette and not a colour key.** Keying was retired in this repo three
times — painted concept art has a gradient and a cast shadow, a clay render is grey
on grey, and a diffusion model paints a lit studio backdrop. The dense export already
ships the raycast silhouette per camera, which answers *is there surface here*
exactly. There was no reason to ask a threshold a question geometry had already
answered.

## Brand-repo copy

The org's canonical home for this file is
`mcp-tool-shop-org/brand/logos/facet/readme.png`. That push is **staged, not fired** —
the mark has not been past the Director's eye yet, and the brand repo is indexed by
`brand manifest` and consumed by other surfaces, so an unjudged asset should not land
there. The command and its compensator are in
[E19-treatment-report.md](../experiments/E19-treatment-report.md); README image URLs
swap from the local path to the brand raw URL in the same one-line change.
