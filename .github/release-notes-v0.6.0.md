**The canon becomes data, and the gate stands in front of the money.**

`canon/W3-IDENTITY.md` specified seventeen elements. The prompt that generated the twins
named sixteen. The profile default that a fresh run would actually use named six. Nothing
connected any of them, so four arcs spent themselves repairing composition downstream of
paint that was wrong at the source.

This release makes that impossible to repeat. The canon is a machine-readable database
keyed on **surface**, and `canon_gate` sits **inside** `restylize_views` and
`texpass_brush`, before the output directory is created. A generation whose prompt does
not cover the ratified canon is refused, and nothing is written.

```
canon_gate 1.0.0  census  (occupancy is not ratification)
subject      named   occupancy   ratified   prof_hit surfaces
W3              19       24/24      24/24       5/19 canon/w3.surfaces.json
GALLEON         13           -          -      11/13 NONE
DRAGON          11           -          -      10/11 NONE
LONGSWORD        5         5/5        5/5        4/5 canon/longsword.surfaces.json
E10-LAYER        1           -          -          - NONE
LOGO             0           -          -          - NONE
```

`prof_hit 5/19` is the specimen, left deliberately broken: the live default is the string
that would be used, and the first run with `--profile character.json` is **supposed** to
halt. Repairing it would delete the evidence.

## Surface, not element — and it is why the holes were findable

An element list cannot show you what is missing. The leather-wrapped grip was absent from
a seventeen-row list and no reading of that list ever revealed it; a human looking at a
picture did. A **surface** list with a nullable occupant makes the hole a row, and W3's
holes turned out to be both hands and both greaves.

Joints are first-class rows between two surfaces, because the missing specification at
every failed region was the **cut** and never a fifth garment. Sleeveless is a bare
occupant plus a forbidden word, not prose. Verification writes a sidecar, so the canon
file can never certify itself.

## Added

- **`tools/canon_gate.py`** — coverage, occupancy, the author-time prompt check, the
  cross-subject census, and a sidecar verifier (t87, t91).
- **`tools/evidence.py`** — the diagnostic layer. Seven arcs had each written their own
  sheet builder and three seats wrote a `surfid` decode in one session; one importable
  surface now emits the provenance classification, the acceptance sheet and the numbers
  with their denominators declared (t90).
- **`tools/flat_trace.py`** — render pixel to atlas texel to contributing view to that
  view's twin (t89).
- **`tools/region_disagreement.py`**, **`tools/boundary_repair.py`**,
  **`tools/unmapped_readout.py`** (t85, t86, t88).

Suite **1182 → 1266**, 1212 hermetic.

## What was measured and did NOT work

Reported because a negative result closed a route rather than leaving it as an untried
option:

- **The flat coloured patches are not a fill artifact.** Orphan fill measures *below* its
  own base rate at them, and the same defect is present in a render built from an atlas
  that predates the repair blamed for it.
- **There is no geometry to snap a material boundary to.** One PBR material on the whole
  mesh, 13,715 atlas islands against sixteen named materials, and a palette that cannot
  separate gold from leather because both are warm. 354 texels of 2.4 million.
- **The magenta is cosmetic.** 0.22% of the figure; a 46x atlas-side reduction moved the
  on-screen count by six pixels.
- **The flats trace to a plate nobody had checked.** The render view's twin is clean; a
  different view owns 97 of 115 defect pixels and its paint is that colour. The patch is a
  scatter artifact and the colour is a real cross-view disagreement on an already-named
  surface — so regenerating twins is **not** justified by "the defect is in the twins".

## Corrections in place

- Two of three Blender citations in the repo's own law book were wrong, resolved one call
  each at `/api/v1/`: **#162226 is open, not merged**, and **#119393 is a single defect,
  not a catalogue**. The correction is load-bearing — the merged fix cannot reach a UV that
  lands in a packer gutter.
- The claim that the generation prompt named six elements welded two files into one false
  sentence. The workflow that made the twins named **sixteen**; the six is the profile
  default.

## Known, and stated rather than implied

The gate checks that the subject prompt contains the ratified canon phrases. **It does not
check paraphrases, per-view stems, unratified drafts, subjects with no surfaces file, or
whether a named material landed on the right surface.** Four subjects have an IDENTITY.md
and no surfaces JSON; generating those files without walking the reference would ship
unwalked lists as if they had been walked, so they are left undone on purpose.

Full detail, with the ruling behind each claim: [CHANGELOG.md](../CHANGELOG.md).

## Compensators

| action | irreversible? | compensator | owner |
|---|---|---|---|
| `npm publish` | **yes** | `npm deprecate @mcptoolshop/facet@0.6.0` and publish a fixed patch; the version stays visible, marked | the publishing session |
| PyPI upload | **yes** | `yank` the release — it stays resolvable for pins but is not selected for new installs — then publish a fixed patch | the publishing session |
| `gh release create` + tag | **yes, in practice** | `gh release delete v0.6.0` and delete the tag; anyone who already fetched a binary keeps it, so treat as one-way | the publishing session |
| the version bump commit | no | `git revert` — five declarations move together and T27 refuses a mismatch | any session |
| the wheel/binary build | no | artifacts are derived; rebuild from the tag | any session |

**The three irreversible rows are the Director's act.**
