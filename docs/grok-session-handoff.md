# Grok session handoff — 2026-08-16 night

Read this before doing anything. The repo is the record. This file is the
next-session start, not a ruling.

Grok experimental memory is **off by default** and was **not running** at the
end of the session that wrote this (config had lost `[memory] enabled`;
`~/.grok/memory/` did not exist). Do not assume prior Grok turns are in
context. Re-check `C:\Users\mikey\.grok\config.toml` for `[memory] enabled =
true`, then type `/memory on` in the TUI prompt box. `--no-memory` still wins.

## Who you are in this tree

Outside consult + build channel. **Ten for ten** nominated calibration claims
held to the digit (or the consult-#10 tree claim). You have repo access:
read, write tools/tests, run the suite, move T34 count surfaces in the same
change-set, leave everything uncommitted for the advisor's fold.

Next Grok test file starts at **t85**.

Do **not** casually modify shipped instruments (`project_twins.py`,
`texpass_*`, `s3_composite.py`). `callieri_border.py` is **1.0.1** (inf-inf
warning repair, byte-identical public arrays, t84). Further edits to it need
the same non-perturbation discipline. Do not touch a seat's in-flight tree
or `docs/experiments/E46-s3-run-report.md` / E49 artifacts as if they were
yours.

## Open the tree

```
cd E:\AI\facet
git log --oneline -3
git status -sb
E:\AI-Models\trellis2-env\Scripts\python.exe tools/facet_index.py verify
```

Python: `E:\AI-Models\trellis2-env\Scripts\python.exe` (absolute, always).
Use `--basetemp=<scratch>` if pytest hits a Windows `pytest-current` symlink
error. Last written collect: **1182 / 1135** (47 artifacts). Re-count before
quoting; T34 pins the surfaces.

HEAD when this was written: `7513ee5` (advisor kickoff + E45-E49 status).
Tag **v0.5.0** is pushed. Working tree was clean.

## What is true (measured)

- **S0 dead.** Colour management is not the look.
- **S1 dead as appearance.** Soup never touched shading.
- **S2 skipped.**
- **Callieri border** is depth-discontinuity + image border, not material dE.
  Built (t76). Warning repair 1.0.1 (t84).
- **Warp is measured, not a finding that grades the look.** Interior tile
  offsets exceed silhouette on 8/8 views (medians 3.46-11.12 px vs 1.16-3.00).
  Gate C held. Twin ring is **8 flat cameras**; no twin exists at el 55.
- **The projector question is closed.** Rebuilt atlas from the per-view
  bundle. Director: E48 a clear step up with room to go further; E49
  accepted, with one new class (colored polygonal shapes).
- **E48** ran flow **off**, both modes, eroded bundle + within-island fill.
  Owner 5.05% / blend 11.96% sentinel (orphan islands). Green on the grip
  survived in both candidates.
- **E49** landed both repairs (orphan fill + erosion cap). Remaining holes
  are surfaces no camera can see (4.65-5.57% valid texels fail the depth
  gate in every flat-ring view). Polygon class is a tagged hypothesis, not
  verified.
- **W3 is the exemplar**, not a character (Director). Sleeveless stands
  (N3 unchanged). No new humanoid. The crux: the canon was never built out.
  ⚠ CORRECTED 2026-08-17: the ARMB twin prompt
  (`facet_E08/ARMB/out/stroke_1_y+090_e+00_workflow.json:181`) carries **16 of
  17** and misses only N17; the **six** is `profiles/character.json`'s brush
  default. grip/gauntlet/greave/hand are still **zero** — because the canon has
  no element for them. W3 surface coverage **20 of 24, 0.833**; the holes are
  both hands and both greaves.

## What Grok built (all folded unless noted)

| module | role | calibration | tests |
|---|---|---|---|
| `tools/callieri_border.py` | Callieri mask + mixed-depth reject + facing | `border_weight[32,32] == 2/3` | T76; 1.0.1 repair T84 |
| `tools/s3_composite.py` | S3 existence proof (VD + VI + disagreement) | `red[16,16] == 0.640625` | T77 |
| `tools/flow_estimate.py` | flow field for the S3 hook | `flow_x[32,32] == 3.0` | T79 |
| `tools/s3_run.py` | load E45 AOV bundle, run S3 | missing `--aov` exits 4 | T80 |
| `tools/s3_sheet.py` | acceptance sheet (layout only) | `crop[0,0] == 200` | T82 |
| `tools/atlas_from_aovs.py` | texel-driven atlas, owner/blend, +/- flow | `atlas[16,16,0] == 0.5` | T83 |

t81 is the E45 warp instrument (not Grok). t78 is the AOV emitter.

## Policy already argued (do not re-litigate unless evidence moves)

- S3-A primary is **target-first** (`primary_mode='facing'` exists).
- S3-B is unsmoothed per-surfid argmax. Waechter / island-owner is a later
  per-island colour offset, not a per-still reassignment.
- Disagreement is not the warp instrument. `flow` is how warp enters S3.
- Twin-vs-control confounds ControlNet slack with geometric warp. Prefer
  depth-edge vs twin-edge when AOVs exist.
- Dense LK, sparse confidence. Do not tune `flow_estimate` against E45
  tile numbers.
- Blend in sRGB. Linear-light is polish.
- Five-panel sheet order: reference | shipped | VD | VI | heat. Heat
  default is global per target.
- Atlas A/B is the **2x2** (owner/blend x flow off/on). Sentinel stays;
  no fill in `atlas_from_aovs` itself.
- Texel Pmid is **not** cam bmid. Decode anchor is mesh-frame vs cams
  inside float32 + P inside the mesh AABB.
- **Flow is not the answer to the Director's three residue regions.**
  E48 residue (green grip, black free hand) is on a flow-off atlas.
- **Do not add a shirt sleeve.** N3 is sleeveless. Name the bare arm and
  the cut (N17 pattern), never a fifth garment (N11 / Amendment 15).
- Masked inpaint is a later, Director-spend lever. UVAtlas / PartUV /
  retopo stay closed.

## Three-world S3 readout

| composite | disagreement | meaning |
|---|---|---|
| clean | low | plates compose; 3D path degrades them |
| blotchy | high | sources inconsistent (warp or plate fight) |
| blotchy | ~0 | plates share the defect; this module cannot see it |

## Adopted next sequence (consult #10 + Director, in the advisor kickoff)

1. Polygon overlay: his three crops vs E49 `orphan_fill_mask.npy` /
   `no_view_visible_mask.npy`. Confirm or kill the polygon class.
2. Never-seen policy to the Director (neutral / brush / accept).
3. Free plate-disagreement measurement on those three regions (E46 maps).
   High -> regen is the right spend. Low -> island-owner compositor first.
4. W3 canon build-out (the crux). Joints named as boundary pairs.
5. Canon-fed twin regen, all eight, this mesh, **on his credit word**.

Seats: Sonnet for execution. Opus only where a seat designs an instrument.
Never omit the model (omitted inherits Fable). Generation is Comfy Cloud
only; Director approves spend.

## Namespace

t76/t77 shipped. t78 emitter. t79 flow. t80 s3_run. t81 warp instrument.
t82 sheet. t83 atlas_from_aovs. t84 callieri 1.0.1. **Next Grok file: t85.**

## Briefs and law

`docs/grok-consult-1-brief.md` ... `docs/grok-consult-10-brief.md`
`docs/experiments/E45-warp-and-aov-kickoff.md` through `E49-finish-and-cap-report.md`
`docs/advisor-kickoff.md` — live advisor paste; recertify counts
`canon/W3-IDENTITY.md` — N1-N17; N17 UNVERIFIED
`CLAUDE.md` — the law book
