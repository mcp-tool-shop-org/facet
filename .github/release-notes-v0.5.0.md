**The plates compose, and the projector question closes.**

The shipped atlas route was destroying paint that the eight per-view plates agree on.
Rebuilt from the per-view bundle under border × facing × visibility weights, the renders
cleared the Director's acceptance bar for the first time on this route — twice, across
two arcs, with one defect class left open and named.

One session ran five arcs (E45–E49), two dispatched executor seats and three runner
seats, and six build rounds through an outside review channel whose nominated
calibration claims held **ten for ten** — every one verified here by running it before
anything trusted it. **Zero cloud credits were spent.**

## Added

**The S3 chain, seven tools.**

| tool | what it does |
|---|---|
| `emit_view_aovs.py` | per-view G-buffers of the shipped state, anchored by pixel-exact reproduction of the recorded silhouettes — 16/16 cameras at 0 px |
| `s3_composite.py` | the existence-proof compositor: view-dependent and view-independent stills, disagreement diagnostics, a flow hook |
| `flow_estimate.py` | dense Lucas–Kanade with sparse per-component confidence, and the aperture problem handled rather than hallucinated |
| `s3_run.py` | the bundle runner, flow A/B built in |
| `s3_sheet.py` + regions | native-pixel acceptance sheets carrying provenance as a panel |
| `atlas_from_aovs.py` | texel-driven atlas rebuild, owner/blend × flow off/on |
| `twin_mesh_warp.py` | the per-tile correspondence instrument, validated on constructed truth before any real measurement |

Tests t77–t84; the suite grew **1098 → 1182** (1135 hermetic), with the thirteen T34
count surfaces moved in the same commits.

**The warp is measured.** Interior tile offsets exceed silhouette offsets on **8 of 8
views** — medians 3.46–11.12 px against 1.16–3.00 — and wrong-pairing controls separate
12.5×, so the instrument discriminates. The twin ring turned out to be **eight flat
cameras**; the elevated pair are brush cameras and no twin exists at elevation, which
retired a premise the record had carried.

**Flow-corrected compositing reduces cross-view disagreement on 18 of 18 measured rows** —
directionally uniform, but magnitude only a trim (1.4–3.2 px median at 16–27% coverage).
The lever was the projection policy itself, not the correspondence.

## Changed

- **`callieri_border.py` 1.0.0 → 1.0.1** — the inf−inf RuntimeWarnings silenced by masked
  subtraction, proven byte-identical across all four public surfaces on an inf-background
  fixture **and** a real frame, with the warning provocation demonstrated against the old
  form and the T76 calibration pin untouched.
- **`docs/index/conventions.json` `paid_for_by`** marched E4[0-4] → E50 as arcs landed.
  Its andon fired three times in one day — each firing a designed leg doing its job — and
  earned a standing order now in the record: the arc bound and the instrument census
  re-run are the **last** corpus-touching steps of every fold.

## Fixed in this release

**v0.5.0 was tagged once and published nothing.** The tag went onto a tree that still
declared `0.4.0` in every site the release gate compares, so the gate refused and no
Release was cut — while the session handoff recorded the publish as successful. The gate
exits at its first check, so its annotation named one file when four declarations plus
the server version were stale.

Also repaired: the hermetic CI job checked out at depth 1, while `t84`'s diff leg reads a
historical blob with `git cat-file`. It passed on the development rig, where the full
history is present, and failed on the runner — a check hermetic with respect to training
assets and not with respect to clone depth. Now `fetch-depth: 0`, with the two
coverage-removing alternatives named and rejected in the workflow file itself.

## Known, named, and staged

- The fill-pass **polygon class** — flat-coloured angular patches on the accepted-grade
  sheets, the one open ruling against them. Hypothesis tagged in provenance masks; a
  repair arc is running.
- **Never-seen surface** — 4.65–5.57% of valid texels fail the depth gate in every
  flat-ring view. That is a policy decision, not a bug.
- **The canon build-out**, identified as the crux: the recorded generation prompt names
  six elements, and several surfaces the defects sit on are named zero times.

Full detail, with the ruling behind each claim: [CHANGELOG.md](../CHANGELOG.md).

## Compensators

| action | irreversible? | compensator | owner |
|---|---|---|---|
| `npm publish` | **yes** | `npm deprecate @mcptoolshop/facet@0.5.0` and publish a fixed patch; the version stays visible, marked | the publishing session |
| PyPI upload | **yes** | `yank` the release — it stays resolvable for pins but is not selected for new installs — then publish a fixed patch | the publishing session |
| `gh release create` + tag | **yes, in practice** | `gh release delete v0.5.0` and delete the tag; anyone who already fetched a binary keeps it, so treat as one-way | the publishing session |
| the version bump commit | no | `git revert` — five declarations move together and T27 refuses a mismatch | any session |
| the wheel/binary build | no | artifacts are derived; rebuild from the tag | any session |

**The three irreversible rows are the Director's act.** The tag move that fired this
release was his.
