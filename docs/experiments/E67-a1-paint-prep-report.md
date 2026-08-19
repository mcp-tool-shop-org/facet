# E67 report — A1 paint prep: unwrap, bake, and the face crop measured on this subject

Executor seat (Sonnet), background. Charter: `docs/experiments/E67-a1-paint-prep-kickoff.md`
(commit 69e799c). Working tree `E:\AI\training\facet_E67\`. Live handoff kept throughout:
`E:\AI\training\facet_E67\handoff.md`. This report restates its findings in the kickoff's
requested shape; the handoff is the fuller, chronological record.

**ZERO CLOUD SPEND.** No comfy-cloud tool was ever loaded or invoked this session. Gate 2
(no cloud call) passes by construction — there is nothing to disclose because nothing was
called.

## Premises vs measured

| premise (from the kickoff / inherited) | measured | verdict |
|---|---|---|
| A1's mesh is `E:\AI\training\facet_E57\mesh\A1_1024_cascade_seed42.glb`, 990,679 faces, sha256 `cdf276e7...` | sha256 matches exactly; faces = 990,679 (trimesh) | CONFIRMED |
| The 8 accepted twins match `MANIFEST.json`'s sha256 | all 8 match, byte for byte | CONFIRMED |
| "A1's front clay is 752×1024" (kickoff's own words) | `clay_0.png` is genuinely 752×1024 (RGBA) | CONFIRMED (the dimension is right) |
| ...and by implication, that this is A1's own frame | **FALSE, per two independent prior handoffs (E57, E58) and `turn_render.py`'s own source**: 752×1024 is a W3-era literal default, used because E57 called the render tool with no `--profile`; E58 explicitly built a corrected, A1-bbox-derived frame at 576×1024 and called the 752-wide one "W3's inherited... by accident" | **OVERTURNED — see "Major finding" below** |
| "cameras: the E58 ring's recorded `cam.json` per view" | **No literal `cam.json` exists anywhere in `facet_E58\`.** Closest artifact is `controls\A1_frame.json` (the bbox-derived frame, not per-view extrinsics). Read as: "the turn_render.py camera CONVENTION E58 used," not a file to load. | Clarified, not falsified — a naming gap, not a wrong premise |
| `prep_uv.glb` (E58) implies A1's mesh has no UV unwrap | **FALSE.** `prep_uv.glb` is a byte-identical renamed copy of the raw mesh (confirmed by hash) — that only means bake_hero_prep.py was never RUN on A1, not that no UVs exist. Direct glTF parse shows the raw mesh already carries a real `TEXCOORD_0` (711,524 entries, var 0.0846) from its OWN reconstruction pipeline's xatlas parameterization step (console log: "Parameterizing new mesh..." at line 27, confirmed to run AFTER "After simplifying" at line 25) | OVERTURNED — see Stage 1 |
| "weld before decimating" needs doing in this arc | Already satisfied upstream, inside `reconstruct_mesh.py`'s own pipeline (decimation at line 25 precedes UV-parameterization at line 27) — no NEW decimation happens in E67, so the hazard the law warns about does not apply to any operation performed here | Constraint respected; not re-derived from scratch, its prior satisfaction verified |
| W3's thin-extent `0.03` might be needed | Not invoked. No thin-structure threshold was needed for provenance, unwrap, or the bake's own (unmodified, default) edge-erosion parameters. **Reported per the kickoff's own instruction: not needed this sitting, not carried forward.** | N/A — correctly not used |

## The face-rect derivation, in full

**Method, decided and logged before running anything** (`logs\gate1_prediction.txt`):
crown-to-neck-pinch via a cross-sectional width(z) scan on the mesh's own vertices, not an
eyeballed fraction and not W3's rect.

1. Blender-space vertices via the exact `GLTF_TO_BLENDER` remap `tools/diagnostics/
   e12_frame.py` uses (`[[1,0,0],[0,0,-1],[0,1,0]]`). **Cross-checked against
   `A1_frame.json`'s independently-recorded bbox before trusting anything downstream**: my
   computed bbox matched to 6 decimal places on all three axes.
2. 400 horizontal bands from crown (`hi.z`) to sole (`lo.z`); per band, the X-extent
   (min-to-max) of vertices whose Z falls in that band, lightly smoothed (5-band moving
   average).
3. Neck-pinch = the first genuine local minimum in that width(z) profile after the width
   has grown from the crown, confirmed by a subsequent regrowth into the shoulders (not
   just any dip — the rule requires grow-then-recede-then-regrow, checked band by band).
   **Found at band 45, z=+0.386481, 11.37% down from the crown** — inside the
   pre-registered 8–16% prediction band.
4. Head 3D box (raw, no padding): X=[-0.093213, 0.062004], Z=[0.386481, 0.500367],
   97,460 vertices in that slab.
5. Padded +15% of the head's own raw height on all four sides (a fraction of the
   structure's own extent, matching this repo's established law for bounding a local
   quantity — not a fixed pixel or world-unit constant): X=[-0.110296, 0.079087],
   Z=[0.369398, 0.517450].
6. Projected into three frames, each via the formula its own consumer already uses (not
   re-derived): `project_twins.py`'s own pixel-projection expressions for the two render
   frames, `bake_hero_prep.py`'s own `std`/`crop_res` normalization for the operational
   `--crop` argument.

**Results:**

| frame | formula source | rect (x0, y0, x1, y1) |
|---|---|---|
| `clay_0.png`, 752×1024 (the kickoff's pinned overlay target) | `project_twins.py` `view_frame` | (282.8, 71.7, 443.7, 197.5) |
| corrected A1 frame, 576×1024 (E58/E65/the twins' actual frame) | same | (194.8, 71.7, 355.7, 197.5) |
| `bake_hero_prep.py`'s own crop_res=1024 square frame (bound=0.55) — **the one actually passed as `--crop`** | `bake_hero_prep.py` `std`/`crop_res` | (409.5, 31.1, 585.5, 168.7) |

**Two independent cross-checks, not assumed:**

- The 752-frame and 576-frame rects differ by EXACTLY (752−576)/2 = 88.000 px horizontally
  (both edges) and 0.000 px vertically — confirming, by direct measurement rather than by
  reading the source and trusting it, that `turn_render.py`'s height-fit convention places
  a subject identically on the vertical axis regardless of canvas width.
- The unpadded crown (`hi.z`) projects to y=86.1 and the sole (`lo.z`) to y=936.9 in the
  576-frame — matching E65's own, independently-measured **exact raycast silhouette**
  y-extent of **[87, 936]** (quoted verbatim from E65's handoff) to within 1 px on both
  ends, via a completely different method (my direct vertex projection vs. E65's raycast).

**Visual sanity check, required before trusting the numbers further**: the rect was drawn
and viewed on three separate images — the pinned `clay_0.png`, E58's corrected clay, and
the actual accepted twin v0 (painted). All three show the rectangle cleanly framing A1's
head, hairline to chin, with a small even margin, not clipping the jaw and not catching a
shoulder. Files: `sheet\overlay_clay0_752x1024.png`, `sheet\overlay_a1clay0_576x1024.png`,
`sheet\overlay_twin_v0_576x1024.png`.

**Gate 1 verdict: PASSED.** The rect was measured from A1's own mesh geometry, matches
independently-recorded numbers it was never fit to, and visually frames the correct feature
on three different images including the accepted twin itself. It did NOT arrive from
another subject.

## Predictions and outcomes

| # | prediction (logged before looking) | outcome |
|---|---|---|
| Gate 1 P1 | Crown sits at the exact bbox top (no weapon, nothing raised) | CONFIRMED — crown_z used directly as `hi.z` |
| Gate 1 P2 | Neck-pinch falls 8–16% down from the crown | CONFIRMED — 11.37% |
| Gate 1 P3 | `bake_hero_prep`-frame rect will not resemble W3's (360,240,700,600); CY0 should sit close to a small value | CONFIRMED — (409.5, 31.1, 585.5, 168.7); CY0=31.1 vs W3's 240 |
| Gate 1 P4 | The 752-frame and 576-frame rects relate by a fixed, computable offset (constant horizontal shift, zero vertical) | CONFIRMED EXACTLY — 88.000 px / 0.000 px, measured not assumed |
| Stage 2 P1 | All 8 views clear the registration IoU ANDON (≥0.80) | CONFIRMED — 0.897–0.963, all 8 |
| Stage 2 P2 (explicitly weak/low-confidence) | reachable/valid ≈60–90%, styled/reachable ≈70–95% | **NOT REACHED** — the run halts before printing these summary ratios (they are computed once, after the per-view loop, and no view ever exits that loop cleanly) |
| Stage 2 P3 | Background-contamination probe passes at every view (≤2.0%) | **FALSIFIED, 8/8 views** — 28.9%–47.0%, all 14×–24× over the limit |
| Stage 2 P4 | No "empty mask" ANDON | CONFIRMED (that specific ANDON never fired; a different one did) |

Prediction 3 was wrong at every one of 8 views, by a wide and consistent margin. This is
reported plainly, per the executor rule that a negative/falsified prediction is exactly as
reportable as a confirmed one.

## Stage 1 — weld/unwrap prep

Command: `blender -b -P tools\bake_hero_prep.py -- --glb A1_1024_cascade_seed42.glb --outdir
facet_E67\prep --crop 409.5,31.1,585.5,168.7` (native UVs kept, no `--reunwrap`; every other
flag at tool default; no `--profile` — none exists for A1 on this tool, matching every
prior A1 Blender-tool invocation in this record). Exit 0.

**Enumerated first** (four prior instances of "enumerate the resource before commissioning
one" already in this record): read `project_twins.py`, `texpass_*`, and the E06 prep tree
(`facet_E06\C1\prep\`) before writing anything. `bake_hero_prep.py` (Stage 1) and
`project_twins.py` (Stage 2) are exactly the recorded route's existing tools for this job;
nothing new was commissioned.

**Major finding, verified not assumed, before running Stage 1**: the raw mesh already
carries a real xatlas UV unwrap from its own reconstruction. Console log
(`facet_E57\mesh\_reconstruct_console.txt`, stage lines only): "After simplifying: 493,983
vertices, 990,682 faces" (line 25) precedes "Parameterizing new mesh..." (line 27, xatlas,
2,712 clusters). Direct glTF binary parse of the shipped GLB confirms `TEXCOORD_0` present:
711,524 entries (matches POSITION count exactly), range [0,0]–[0.9996,0.9996], variance
0.0846 (far above `bake_hero_prep.py`'s own "uniform/no UVs" floor of 1e-6). Per the tool's
own docstring, native UVs are the E05-established, measured-better default
("TRELLIS ships xatlas UVs and smart_decimate carries them through the cut... Native UVs are
now the default; [`--reunwrap`] is the escape hatch, not the route").

**Chart/island counts** (tool's own printed diagnostics): 27,745 islands total (35.7
faces/island average); head-band 139,603/990,670 faces by direct per-face crop test,
5,080 islands / 153,125 faces by whole-island inclusion; head UV-area share 10.39% before
the ×3 scale, 51.08% after (face-count share 15.46%, unchanged throughout, as expected —
only UV area was scaled). Packed UV area covers 5.20% of the 4096 atlas — lower than a
precedent the tool's own docstring cites (18.76% at the same margin), though that
precedent's island-count regime is not confirmed to match this mesh's; reported as
measured, not chased with a margin retune.

**Non-manifold/degenerate geometry — same-instrument before/after** (`mesh_topology`, sha256
unchanged `6351135ef6...`, raw mesh vs. `prep_uv.glb`):

| metric | raw (E57 mesh) | prep_uv.glb | changed? |
|---|---|---|---|
| faces | 990,679 | 990,670 | −9 (0.0009%) |
| boundary_edges | 1 | 17 | **+16** |
| boundary_total_length | 0.0 | 0.0105797 | **+0.0106** (world units; mesh is ~1.0 tall) |
| nonmanifold_edges | 972 | 972 | unchanged |
| shells / largest_shell_frac | 19 / 0.999075 | 19 / 0.999075 | unchanged |
| nested_wall_test | null | null | unchanged |
| pieces_manifold_adjacency | 184 (largest 988,302) | 184 (largest 988,302) | unchanged |
| surface_area | 2.1187747 | 2.11877408 | unchanged to displayed precision |
| verts_unwelded | 711,524 | 716,156 | **+4,632 (+0.65%)** |

Read plainly: the continuous 3D surface is unchanged (surface_area, bbox, nonmanifold_edges,
shells, nested_wall_test all identical). The boundary-edge and unwelded-vertex counts moved,
confined to index-level vertex splitting — plausibly (stated as a hypothesis, not verified
by a seam-graph diff) because Blender 5.2's own glTF exporter splits vertices at UV/attribute
seams somewhat more aggressively than the original pipeline's exporter did. Disclosed per
"report exactly what was modified and why," even though no geometry edit was intended.

**Cross-instrument confirmation**: `mesh_stats` (separate script, sha256 `fe146891d9...`),
run with the derived crop explicitly passed, independently counts `face_rect_faces: 139603`
— an exact match to `bake_hero_prep.py`'s own printed head-band count. (A first `mesh_stats`
call was made without passing the crop and silently used the tool's own default —
`"360,240,700,600"`, W3's rect — for its face-rect diagnostics; caught before it entered
this report and re-run correctly; the wrong-default numbers are not used anywhere above.)

## Stage 2 — the bake: HALTED, 8/8 views, same ANDON

Command: `project_twins.py --prep facet_E67\prep --view 0=a1_v0.png ... --view 7=a1_v7.png
--aspect 576,1024 --out facet_E67\bake\atlas.png`. **`--aspect 576,1024` is an explicit
override of the tool's own default (`752,1024` — a W3 literal, per `turn_render.py`'s own
`--w` default and its stated reason).** This is the operational form of the kickoff's "do
not inherit W3's numbers" instruction, found by reading the tool's source rather than by
being told a second time; leaving `--aspect` at its default would have silently
reintroduced the forbidden constant into the bake's own camera geometry.

First run (all 8 views in declared order) halted at view 0. A pure-diagnostic sweep (same
parameters throughout, nothing retuned) then tested every remaining view individually, to
learn scope rather than to force a pass:

| view | yaw | mesh sil % | twin paint % | IoU | centroid \|d\| px | shadow note? | relaxed-admit % within dE10 (limit 2.0%) | median dE |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 29.7 | 29.7 | 0.9228 | 17.5 | no | **30.29** | 19.6 |
| 1 | 45 | 27.0 | 26.5 | 0.9630 | 2.0 | no | **37.48** | 15.4 |
| 2 | 90 | 18.1 | 19.1 | 0.9249 | 25.2 | yes | **29.19** | 16.0 |
| 3 | 135 | 27.1 | 27.0 | 0.9501 | 8.5 | yes | **29.27** | 13.4 |
| 4 | 180 | 29.7 | 30.6 | 0.9105 | 23.3 | no | **28.92** | 17.0 |
| 5 | 225 | 27.0 | 27.2 | 0.9336 | 15.8 | yes | **42.88** | 11.6 |
| 6 | 270 | 18.1 | 17.3 | 0.9522 | **0.5** | no | **34.37** | 17.4 |
| 7 | 315 | 27.1 | 29.0 | 0.8970 | 36.9 | yes | **47.03** | 10.9 |

**8/8 views fire, all 14×–24× over the 2.0% limit.** All 8 registration IoUs individually
clear the tool's own separate 0.80 ANDON with room. **View 6 has near-perfect registration
(IoU 0.9522, centroid offset 0.5 px) and still fires at 34.37%** — this rules out gross
twin-vs-mesh misregistration as the sole or primary mechanism (the worst offender by
registration, view 7 at |d|=36.9px, is also the worst by contamination at 47.03%, but view
1 fires nearly as hard, 37.48%, with |d|=2.0px — the two do not track together cleanly).
4/8 views (2, 3, 5, 7) also carry the tool's own separately-demoted diagnostic note about a
keyed twin bbox exceeding the mesh silhouette by >25%, "most likely a cast shadow" — a
different, already non-halting observation. Median dE across all 8 views (10.9–19.6) sits
just above the probe's own dE-10 classification threshold, consistent with a genuinely
large population of near-background texels rather than a handful of outliers.

**Pure-look diagnostic, no tool parameter touched**: E58's own exact raycast silhouette
(`facet_E58\controls\sil\a1sil_{0,6}.png`, the same mesh+camera the ring's controls are
pinned to) drawn as a contour directly on the accepted twins, front (v0) and profile (v6).
On both, the body silhouette (torso, sleeves, sash, trousers, shoes) tracks the mesh
contour tightly, matching the high measured IoU. **At the hair, on both views, the mesh's
contour sits visibly inside the twin's painted curls** — offered as a well-evidenced
HYPOTHESIS for the ANDON's mechanism (hair is exactly the kind of thin, irregular structure
the relaxed edge-distance cap applies to, and it sits inside this run's own head-band with
looser facing/edge criteria), **not a confirmed root cause** — no per-texel spatial
decomposition was run. That would need `--diag-npz`, which this tool only writes AFTER its
per-view loop completes without an ANDON; extracting it here would require relaxing
`--bg-max-pct`, which is exactly the "retune a parameter to get past the gate" move the law
forbids, so it was not attempted. Files: `sheet\silhouette_check_v0.png`,
`sheet\silhouette_check_v6.png`.

**No atlas was produced. No parameter was changed to force a pass.**

## Stage 3 — the sheet: PARTIAL

`sheet\E67_sheet.png` (1872×3666, full size on disk). Panel 1 (measured face rect on
clay_0) and panel 2 (UV layout with chart boundaries) are real and complete. Panels 3
(baked atlas) and 4 (baked mesh render beside the accepted twin) are honestly marked NOT
AVAILABLE — Stage 2 never produced an atlas to show or render. Two bonus panels (the
silhouette-check overlays) are included, clearly labelled as diagnostic evidence for the
Stage 2 halt rather than as the four requested panels.

The UV-layout script itself had one bug, found and fixed before the image was trusted: it
initially read the exported `prep_uv.glb`'s raw `POSITION` values directly (glTF's own
Y-up convention) without applying the same glTF-to-Blender remap `e12_frame.py` uses —
`bake_hero_prep.py` gets this remap for free via Blender's own glTF importer, but a
standalone script reading the exported file directly does not. This returned 0 head faces
against Stage 1's own printed 139,603. Fixed and re-verified against both the known bbox
(exact match) and the exact head-face count (139,603, exact match) before the image was
used.

## Gates — summary

| gate | status | evidence |
|---|---|---|
| Gate 0 — provenance | **PASSED** | mesh sha256 exact match; all 8 twin sha256 exact match; face count 990,679 matches the ratified figure |
| Gate 1 — face rect measured, not inherited | **PASSED** | crown-to-neck-pinch geometry, 3-way visual confirmation, 2 independent numeric cross-checks |
| Gate 2 — no cloud call | **PASSED (by construction)** | no comfy-cloud tool loaded or called this session |
| `project_twins.py`'s own registration IoU ANDON (≥0.80) | PASSED, all 8 views | 0.897–0.963 |
| `project_twins.py`'s own background-contamination ANDON (≤2.0%) | **FIRED, all 8 views** | 28.9%–47.0%; see Stage 2 table |

## Out-of-scope items, confirmed untouched

Any generation or cloud call (none made); the first brush (waits on the Director's look,
and now additionally waits on Stage 2's halt being resolved); binding/facesets (not
touched); reopening twins for the clay-ridge at v6's chest seam (not touched); W3 (read
only for its forbidden constants, never used as a value source).

## git status, verbatim

```
On branch main
Your branch is ahead of 'origin/main' by 39 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

The 39-commits-ahead state predates this session (nothing here added a commit). This
session touched nothing inside `E:\AI\facet` itself; every output lives under
`E:\AI\training\facet_E67\`.

## Artifact paths

- Live handoff: `E:\AI\training\facet_E67\handoff.md`
- Gate 0: `E:\AI\training\facet_E67\logs\gate0_report.txt`
- Gate 1: `E:\AI\training\facet_E67\logs\gate1_prediction.txt`,
  `logs\gate1_head_region.txt`, `logs\gate1_result.json`, `logs\gate1_uv_check.txt`
- Stage 1: `E:\AI\training\facet_E67\prep\` (`pos.npy`, `nor.npy`, `mask.npy`, `meta.json`,
  `prep_uv.glb`), `logs\stage1_bake_hero_prep_console.txt`
- Stage 2: `logs\stage2_prediction.txt`, `logs\stage2_bake_console.txt` (view 0 halt),
  `logs\stage2_diag_views1-7_console.txt` (view 1 halt), `logs\stage2_diag_v{2..7}_console.txt`
  (views 2–7 individually)
- Sheet: `E:\AI\training\facet_E67\sheet\E67_sheet.png` (assembled),
  `overlay_clay0_752x1024.png`, `overlay_a1clay0_576x1024.png`,
  `overlay_twin_v0_576x1024.png`, `uv_layout.png`, `silhouette_check_v0.png`,
  `silhouette_check_v6.png`
- Working scripts (copies): `C:\Users\mikey\AppData\Local\Temp\claude\E--AI-facet\
  428295a0-ff4d-49f0-b0a2-024d00acf529\scratchpad\` — `gate0_provenance.py`, `check_uv.py`,
  `gate1_head_region.py`, `gate1_draw_overlay.py`, `silhouette_overlay.py`,
  `build_uv_layout.py`, `build_sheet.py`

## Role discipline

No quality judgment is offered anywhere above. Every gate is reported PASSED, FIRED, or (in
one case, the summary coverage ratios) NOT REACHED — never "good," "clean," or "ready."
Predictions were logged before each measured stage, including one (Stage 2 P2) explicitly
disclosed as low-confidence in advance, and one (Stage 2 P3) that was wrong at all 8 views
and is reported exactly that plainly. No memory write was made. No git commit was made. No
child agent was used for core work. The Director's eye still gates the first brush — this
arc did not reach the point where that question is even askable, because Stage 2 halted
first.
