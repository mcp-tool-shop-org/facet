# E70 report — the look that can fail: baked mesh beside its twin

Executor seat (Sonnet), background. Charter: `docs/experiments/E70-baked-look-kickoff.md`
(commit 9246483). Read whole before any work, in order: the charter; `E:\AI\facet\CLAUDE.md`
(already in this session's context verbatim; its "Judging artifacts" section is directly
load-bearing for the sheet); `docs/experiments/E69-whole-figure-withhold-report.md` (which
produced the atlas). Working tree `E:\AI\training\facet_E70\`. Live handoff kept throughout:
`E:\AI\training\facet_E70\handoff.md`.

**ZERO CLOUD SPEND. NO BRUSH.** No comfy-cloud tool was loaded or invoked this session. No
stroke, re-bake, hole-fill, or dilation was performed anywhere. Gate A passes by
construction.

## ⚑ THE RULING THIS REPORT DOES NOT CONTRADICT

E69's ANDON reads **0.00% on 8/8 views**. The withhold predicate and the ANDON's own
re-test share one array and one comparison, so a zero residual is **the code agreeing with
itself**. That is quoted here, once, as **self-consistency** — never as *the bake is good*.
This sheet exists precisely because that number cannot answer whether the bake looks right.
Nothing below treats it otherwise.

## Inputs, verified before use

| input | path | sha256 | status |
|---|---|---|---|
| mesh (E67 Stage 1) | `E:\AI\training\facet_E67\prep\prep_uv.glb` | `b2e0fca72ef56462e01a322095d62e5588ac67aaf6b04a016f45856bbf1bd6c6` | **Gate C** — recorded, re-verified byte-identical after packing |
| atlas (E69 widescope) | `E:\AI\training\facet_E69\bake\atlas_widescope.png` | `66b8602b1e8d1a61e1c536f75730170fdfec3a5292f47de540dad7f2408727f2` | **Gate C** — recorded, re-verified byte-identical after packing |
| twins (8) | `E:\AI\training\facet_A1_accepted_ring\a1_v{0..7}.png` | all 8 match `MANIFEST.json` exactly (`sha256sum` compared byte-for-byte) | **Gate B PASSED** |
| packed GLB (this session's output) | `E:\AI\training\facet_E70\pack\a1_e70_packed.glb` | `8fe0d22c2cc0f8846dc789871187584b961c40c2b5d17dc059e786dab4bd0918` (38,029,352 bytes) | derived, not an input |

**Gate B**, exact evidence: `sha256sum a1_v0..7.png` against `MANIFEST.json`'s recorded
hashes, 8/8 exact match, no discrepancy.

**Gate C**, exact evidence: mesh and atlas hashes recorded *before* `bake_hero_pack.py` ran,
then both files re-hashed *after* packing — identical both times. `bake_hero_pack.py` only
reads `--prep-glb`/`--atlas`; it writes exclusively to `--out`. Neither source file was
re-baked, retouched, or hole-filled — the packer binds the atlas as Principled base colour
verbatim and exports.

**Gate A**: no `mcp__plugin_comfy-cloud_*` tool was loaded via ToolSearch or called at any
point this session.

## Camera / frame convention — sourced, not guessed

`profiles/a1.json`'s own `tools."verify/turn_render.py"` and `tools."silhouette_masks.py"`
blocks (each entry carries `why`/`from`; MEASURED at E58 Stage C from A1's own mesh bbox,
not inherited from W3): `w=576 h=1024 margin=1.204 fit-axis=height views=0..7 step=45.0
yaw-offset=0.0`. Confirmed against the accepted twins themselves before rendering: all 8 are
576×1024 RGB (measured via PIL, this session). This is the **same frame the twins were
generated against** (E58 ring) — cross-checked against `A1_frame.json`
(`render_w=576 render_h=1024 margin=1.204`) and E67 Stage 2's own `--aspect 576,1024`
override on `project_twins.py`.

## The pipeline — every tool reused from the existing codebase, nothing invented

1. **Pack** — `tools/bake_hero_pack.py` (Blender 5.2, `-b -P`, PowerShell). Imports
   `prep_uv.glb`, binds `atlas_widescope.png` as Principled base colour via an Image
   Texture node routed through the mesh's own UV map, packs the image, exports
   `pack\a1_e70_packed.glb`. Exit 0. `logs\stage1_pack_console.txt`.
2. **Render** — `tools/verify/turn_render.py --profile profiles/a1.json --flat` (NOT
   `--clay` — texture must show). Workbench engine, `Standard` view transform, `FLAT`
   light, `color_type=TEXTURE` (CLAUDE.md: *"a Workbench STUDIO render is not a texture
   readout"* — this run is deliberately not that). 8 views written to
   `render\e70bake_{0..7}.png`, 576×1024, exit 0. `logs\stage2_render_console.txt`. Alpha
   channel is uniformly 255 (opaque; the Workbench viewport background is already baked
   into RGB, so RGB was used directly with no compositing step).
3. **Silhouette** — `tools/silhouette_masks.py --prep facet_E67\prep --profile
   profiles/a1.json` (trellis2-env python, no Blender; raycast, not rendered-pixel
   thresholding — this repo's own law, *"where geometry can answer the question, use
   geometry"*). Reads `prep_uv.glb` from the **same, unmodified** prep directory as the
   mesh input; writes new masks only. Exit 0. `logs\stage3_silhouette_console.txt`.
   **Not** run with `--anchor` against E58's `a1sil_*.png`: those masks were raycast on a
   mesh E58 itself describes as *"a byte-identical copy of A1's raw mesh"*, and E69's own
   report records that E67 Stage 1 measurably changed topology (faces −9, boundary_edges
   +16, unwelded verts +4,632) relative to that raw mesh. The anchor's ANDON is a strict
   `diff==0`; using it here would halt this run over a question this arc does not need
   answered. **Cross-checked instead**, softly and non-gating, against E67 Stage 2's own
   printed "mesh sil %" (`project_twins.py`, same prep dir): 8/8 views agree within 0.04
   percentage points (table below).
4. **Crop derivation** — `E:\AI\training\facet_E70\scripts\e70_derive_crops.py` (new,
   one-off, not a repo tool; kept in the training tree, not committed). Derives a HEAD band
   (rows 0–17% of that view's own raycast-measured silhouette height, from `top_row`) and a
   COLLAR/VEST-OPENING band (rows 12–40% of the same) **per view, from that view's own
   mask** — never an inherited pixel rectangle. For each band, the widest measured window
   across all 8 views (+22% padding, 18px floor) becomes **one fixed window size applied to
   every view**, centred on that view's own band centroid. Because every view shares one
   `ortho_scale` (one mesh, one profile), a fixed pixel window is a fixed real-world window
   in every view — genuinely "same zoom," not merely "same crop size." Head window
   215×208px, collar window 517×342px. **16/16 (8 views × 2 bands) unclipped by the
   576×1024 frame.** `logs\stage4_crop_derivation_console.txt`,
   `sheet\crop_boxes.json`.
5. **Sheet** — `E:\AI\training\facet_E70\scripts\e70_build_sheet.py`. Lays out, per view:
   full twin | full mesh render (576×1024 each), then head-crop twin | head-crop mesh |
   collar-crop twin | collar-crop mesh, all crops taken from the identical box for both
   images. Every constituent panel is also saved individually at full/native crop
   resolution in `sheet\crops\` (48 PNGs: 8 views × {twin,mesh} × {full,head,collar}).
   `logs\stage5_sheet_console.txt`.

## Silhouette cross-check (non-gating, informational)

| view | this session's `pct_of_frame` | E67 Stage 2 `mesh sil %` (same prep dir) | diff |
|---|---:|---:|---:|
| 0 | 29.662% | 29.7% | −0.038pp |
| 1 | 27.021% | 27.0% | +0.021pp |
| 2 | 18.123% | 18.1% | +0.023pp |
| 3 | 27.123% | 27.1% | +0.023pp |
| 4 | 29.662% | 29.7% | −0.038pp |
| 5 | 27.021% | 27.0% | +0.021pp |
| 6 | 18.123% | 18.1% | +0.023pp |
| 7 | 27.123% | 27.1% | +0.023pp |

## What the sheet is built to show, and at what zoom

The sheet (`sheet\E70_baked_look_sheet.png`, 1554×12708px, 11,853,716 bytes) is organized as
one section per view (8 sections), each containing:

- **Full twin | full mesh render**, 576×1024 each, native resolution, side by side.
- **Head crop, twin | mesh** — 215×208px window, identical real-world size in every view,
  centred on that view's own raycast-measured head band.
- **Collar/vest-opening crop, twin | mesh** — 517×342px window, same construction.
- The two footer lines, verbatim, once per view section (8 repetitions total in the sheet;
  see "Footer placement" below for how this reading of "every panel" was chosen).

**Mapping to the Director's five named failure modes** (this seat renders and crops so each
would be visible if present; it does not judge whether any occurred):

1. **Seams** — chart-boundary discontinuities can appear anywhere on the body; the full
   576×1024 panels cover the whole figure at native resolution, and the head/collar crops
   add a further ~2.4–2.7× linear zoom specifically where the charter names three of the
   five modes as living.
2. **Through-projection** — a far surface's paint landing on a near one would read as an
   anomalous colour patch inconsistent with the surrounding material; visible in both the
   full panels and the crops at the same zoom levels as above.
3. **Bald crown** — the head band's top edge is `top_row`, i.e. the topmost raycast-hit row
   of that view's own silhouette — the crown sits at the very top of the head crop by
   construction, not by estimation.
4. **Cream-as-wall** — the collar/vest-opening crop is centred on the neck/upper-chest band
   (12–40% of figure height), directly containing the collar and the vest's V-opening where
   the cream shirt is most exposed; the cream sleeves are also visible at full resolution in
   the full panels, adjacent to the flat grey background across a long silhouette edge.
5. **Identity gone** — best judged from the full panel (whole figure, proportions) and the
   head crop (face) together; both are present per view.

## Footer placement — the interpretation used, stated so it can be corrected

The charter's instruction is *"FOOTER, VERBATIM, ON EVERY PANEL."* This seat read "panel" at
the granularity of **one view's comparison block** (full + both crops together), since that
is the unit the charter itself uses elsewhere ("accepted twin | baked mesh... **per view**").
The two lines appear verbatim, unmodified, once under every one of the 8 view sections — not
once per individual image tile (which would be 48 repetitions). If the Director wants it
denser (under each of the 48 individual tiles) or sparser (once for the whole sheet), that is
a one-line change to `scripts\e70_build_sheet.py` and a re-run; nothing else in the pipeline
would need to change.

## Panel content, described factually, per view — uncertainty stated throughout

This seat inspected all 8 view sections at native resolution before writing this section.
Per CLAUDE.md's own law (E64), *"a seat's sentence about its own output is not a
measurement"* — what follows is a description of what is visually present, not a verdict on
whether it is acceptable. Words like *correct/wrong/good/bad/clean* do not appear below.

- **General, all 8 views**: the mesh panel's overall proportions, pose (arms slightly away
  from the body, hands open), garment set (sleeveless plum vest, cream shirt, umber sash,
  dark-green trousers, brown shoes), hair colour/style (dark curly), and skin tone visually
  match the twin panel's in every view. The face in the mesh panel's head crop shows the
  same general hair, facial structure and expression as the twin's head crop in every view.
  This seat does not assess whether identity is preserved — that judgment is the Director's.
- **A vertical lighter/brighter magenta-toned band** is visible down the front-centre of the
  vest in the mesh panel in views 0, 1, and 7 (yaws 0°, 45°, 315° — the front-facing views).
  It is not present at the same location in the twin panel.
- **Pale, near-white patches interrupt the plum vest colour** at: both shoulder blades in
  view 4 (yaw 180°, rear); the upper back/shoulder in view 3 (yaw 135°); the chest-to-hip
  area in view 2 (yaw 90°, profile), where the twin shows a continuous umber sash that does
  not read as a continuous shape in the mesh panel at the same location; and the
  back-of-collar/neck in view 5 (yaw 225°). None of these patches are present at the same
  screen location in the twin panel.
- **The cream shirt sleeves show a mottled/speckled texture** in the mesh panel across most
  views (fine dark flecks scattered on the fabric), more textured than the twin panel's
  comparatively smooth cream sleeve rendering, visible in views 0, 1, 3, 4, 5 particularly.
- **A greyish patch** is visible on the lower trouser leg near the ankle in the mesh panel of
  view 5, not present at the same location in the twin panel.
- **This seat's uncertain, offered-not-measured hypothesis about the pale patches above**:
  this session separately viewed `atlas_widescope.png` directly (in UV/atlas space, at
  1024×1024 downscale from its native 4096×4096) and observed a large tessellated
  grey-triangle pattern interleaved with the painted (coloured) chart regions across the
  used portion of the layout. This grey pattern is visually consistent, in general
  character, with the pale patches this seat is describing in the 3D renders above, and
  E69's own report already measured that "holes" (unpainted texels, fallback-filled) are
  **58.9%** of all valid atlas texels, with the marginal E68→E69 new-hole population
  distributed **26.6% crown / 0.7% / 45.4% middle-fifth (torso) / 7.2% / 20.0% feet** — i.e.
  E69 itself already found holes concentrated in the torso band, not only the crown. This
  seat did **not** perform a pixel-exact correlation (e.g. re-rendering
  `atlas_widescope_holes.png` through the same pack+render path, or overlaying UV
  coordinates) to confirm that the specific patches observed above are specifically hole
  texels rather than, for instance, seam artifacts or something else. Offered as a
  plausible, visually-supported, **unverified** connection to already-measured E69 findings,
  not a new measurement.
- **Head/crown crops, all 8 views**: hair coverage reads as generally continuous in the head
  crop in most views; view 5's head crop shows a lighter patch near the crown/back of the
  head not as pronounced in the twin's head crop at the same location.

## Supplementary measurement (non-gating): shirt/background boundary colour distance

Not the pipeline's own per-texel `dE_bg` statistic (that runs inside `project_twins.py` on
the atlas). This is an ad hoc spot-check on the **rendered pixels**, added because the
charter names "cream-as-wall" as a failure mode this sheet must be able to show, and a
number is more useful to the Director's eye than this seat's impression. sRGB→CIELAB (D65),
reported as `dE76`, uninterpreted — no threshold, no pass/fail, nothing retuned; `--bg-de
10`/`--bg-max-pct 2.0` were not touched anywhere in this session.

- **Background is pixel-identical across all 8 renders**: sRGB `(155, 155, 157)` sampled at
  frame corner `(3,3)` in every view.
- At 3 fixed scanline rows (y=420/470/520) per view, this seat located the first
  non-background run (≥3px, coarse `dE76>20` split, used only to find a boundary column —
  not a quality gate) walking inward from the left frame edge, then sampled `dE76`-to-
  background at 0/1/2/3/6/10px inside that boundary. Across the resulting 24 (view, row)
  locations, values at **+1px inside and beyond overwhelmingly sit in the ~20–52 `dE76`
  range** — clearly separated from the background in the large majority of samples.
  **One located outlier**: view 5, row y=470, column x=152 (6px inside a boundary detected
  at x=146) reads `dE76 = 5.51` — close to the background. This seat did not determine which
  garment structure (sleeve edge, hand, vest hem, or something else) that specific pixel
  belongs to; the scanline method is coarse (fixed rows, not structure-aware) and this is
  reported as a located, uninterpreted number, not a characterisation of the region.
  Full 24-location table: `logs\stage6_bg_spotcheck_console.txt`.

## Out of scope, confirmed untouched

No brush or stroke. No re-baking (the atlas was packed and read, never regenerated). No hole
filling or dilation. `--bg-max-pct` (2.0) and `--bg-de` (10) were not retuned anywhere —
neither appears as a flag in any command this session ran; the `dE76` spot-check above is a
separate, ad hoc, non-gating measurement on rendered pixels, explicitly reported as such and
not fed back into either threshold. E69's ANDON pass is quoted once, as self-consistency
only (above), never as "the bake is good." Binding was not touched and does not gate this
arc. Nothing was regenerated — the mesh, atlas, and twins are the exact files named in the
charter, hash-verified before and after use.

## Testing

No file under `tools/`, `tests/`, or any other tracked path in the git repository was
created, modified, or deleted this session (`git status` below is unchanged from session
start except for this report). The two new scripts (`e70_derive_crops.py`,
`e70_build_sheet.py`) and the supplementary spot-check (`e70_spotcheck_bg.py`) are one-off,
this-arc-only artifacts kept in the training tree
(`E:\AI\training\facet_E70\scripts\`), not the repo — per this repo's own rule, "the commit
that touches the code carries its own tests" applies to code that lands in the repository;
nothing here does, and no commit was made.

## Gates — final states

| gate | status | evidence |
|---|---|---|
| Gate A — no cloud call | **PASSED (by construction)** | no comfy-cloud tool loaded or called this session |
| Gate B — twin sha256 verified against MANIFEST.json | **PASSED** | 8/8 exact match, before any use |
| Gate C — mesh + atlas used unmodified, hashes recorded | **PASSED** | both files re-hashed identical after packing; `bake_hero_pack.py` reads its inputs, never writes to them |

## git status, verbatim

Captured before this report file was written (i.e. the state this session found and leaves,
aside from adding this one file):

```
On branch main
Your branch is ahead of 'origin/main' by 50 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

`git diff --stat` (before this report existed): empty — no tracked file was modified. This
session's only filesystem effect inside `E:\AI\facet` is the addition of this report file,
which will show as untracked until the advisor stages it by pathspec. No `git add`, no `git
commit` was run by this seat.

## Artifact paths

- **The sheet**: `E:\AI\training\facet_E70\sheet\E70_baked_look_sheet.png` (1554×12708,
  11,853,716 bytes)
- Individual full-resolution panels (48 PNGs): `E:\AI\training\facet_E70\sheet\crops\`
  (`v{0..7}_{twin,mesh}_{full,head,collar}.png`)
- Crop-box derivation record: `E:\AI\training\facet_E70\sheet\crop_boxes.json`
- Packed GLB: `E:\AI\training\facet_E70\pack\a1_e70_packed.glb`
- Full-frame renders (identical content to the sheet's mesh-full panels):
  `E:\AI\training\facet_E70\render\e70bake_{0..7}.png`
- Raycast silhouette masks + report: `E:\AI\training\facet_E70\sil\e70sil_{0..7}.png`,
  `E:\AI\training\facet_E70\sil\silhouettes.json`
- Console logs, every stage: `E:\AI\training\facet_E70\logs\stage{1..6}_*_console.txt`
- Scripts (one-off, training-tree, not committed):
  `E:\AI\training\facet_E70\scripts\e70_derive_crops.py`,
  `E:\AI\training\facet_E70\scripts\e70_build_sheet.py`,
  `E:\AI\training\facet_E70\scripts\e70_spotcheck_bg.py`
  (scratchpad originals also left at `C:\Users\mikey\AppData\Local\Temp\claude\
  E--AI-facet\428295a0-ff4d-49f0-b0a2-024d00acf529\scratchpad\`)
- Live handoff: `E:\AI\training\facet_E70\handoff.md`

## Role discipline

No quality judgment is offered anywhere above — "good/bad/correct/wrong/clean/decisive" do
not appear as characterisations of any panel. E69's 0.00%/8-8-PASS result is quoted exactly
once, explicitly as self-consistency, never as evidence the bake looks right. Every gate
(A/B/C) is reported with its own evidence rather than asserted. The crop-box derivation is
disclosed in full (fractions, padding, fixed-window construction) so it can be checked or
overridden rather than trusted. The footer-placement interpretation is stated explicitly,
flagged as a judgment call about layout (not about the asset), and named as trivially
reversible. The one interpretive hypothesis offered (pale patches ~ holes) is labelled
unverified and traced to its supporting-but-not-proving evidence. No memory write was made.
No git commit was made. No child agent was used for core work — the pack, render, silhouette,
crop-derivation, sheet-build, and spot-check stages all ran directly in this seat, each
gated on the previous stage's exit code and, where practical, cross-checked against an
independent prior measurement (E67 Stage 2's silhouette percentages) before being trusted.
The brush does not open on this seat's word; that is the Director's, on the sheet above.
