# E67 contamination-map report — second sitting, where the flagged mass sits

Executor seat (Sonnet), background, dispatched directly by the advisor. Subject: the
first sitting's Stage 2 halt (`docs/experiments/E67-a1-paint-prep-report.md`) —
`project_twins.py`'s own background-contamination ANDON fired 8/8 views (28.9%-47.0%
of relaxed-admission texels within dE 10 of background, against a 2.0% limit).
Registration was clean (IoU 0.897-0.963, all 8 views). **This sitting produces ONE
thing: a map of where that flagged mass sits.** ZERO CLOUD. ZERO THRESHOLD CHANGES —
`--bg-de` (10), `--bg-max-pct` (2.0), and every other tool parameter are untouched; the
ANDON is never re-run, hoping for a pass or otherwise. Working tree:
`E:\AI\training\facet_E67\map\`. Live handoff kept throughout, appended to the first
sitting's own file: `E:\AI\training\facet_E67\handoff.md`.

**No ranking, no recommendation, no quality judgment anywhere in this report.** Counts
and shares only. The advisor rules and the Director decides what this means.

## The question, restated precisely

For each of the 8 accepted-twin views, classify every FLAGGED pixel — the exact set
behind the ANDON's own reported percentage, i.e. every atlas texel that is (a) admitted
only by the relaxed/local-half-width erosion cap (`relaxed`, edge-proximate) and (b)
within dE 10 of the twin's own fitted background at its own projected pixel (`dE_bg <
bg_de`) — into exactly one of:

1. **Class 1** — on a declared material that is inside the dE-10 window (N2 cream
   sleeves, N10 mouth; N6 face_skin checked per instruction even though its single
   sampled patch measures dE 24.93, well outside the window).
2. **Class 2** — on true exterior backdrop, outside the figure entirely, decided by
   GEOMETRY only.
3. **Class 3** — on hair / silhouette fringe (the first sitting's second hypothesis).
4. **Unclassified** — none of the above, reported honestly rather than forced.

## Method

### Step 0 — a read-only reimplementation, validated bit-for-bit before anything else

`project_twins.py` cannot be re-run to extract the flagged set: its `--diag-npz` dump
only writes AFTER a view's ANDON-free completion, and every view here fires the ANDON,
so relaxing `--bg-max-pct` to reach that write would be exactly the "retune a parameter
to get past the gate" move this repo's law forbids. Instead, a new, read-only script
(`map_contamination.py`) reproduces the tool's own per-view acceptance chain — facing →
visibility → in-frame → distance-to-trust-mask-boundary → local-half-width-capped
erosion → `inm` (accepted) → `relaxed` (edge-proximate subset) → `dE_bg` (CIE76 distance
to the FITTED, per-pixel background) — stopping exactly where the tool's own ANDON
raise would be (`project_twins.py:864-868`), which simply has no counterpart below.

Every shared piece of logic is either an **import** of a function `project_twins.py`
itself would use (`mask_geometry.local_thickness`, `mask_geometry.fit_background` —
that module's own docstring records both as T64-anchored bit-identical to
`project_twins.py`'s own copies, extracted precisely because `project_twins.py` calls
`ap.parse_args()` at module level and cannot be imported), or a **verbatim, cited copy**
(`srgb_to_lab`, `bilinear`, `cam_axes`, `figure_mask` — character-for-character from
`tools/project_twins.py`, source lines cited in the script). No formula was re-derived.
Every constant is the tool's own argparse default, except `--aspect`, set to `576,1024`
— the exact explicit override the first sitting's own Stage 2 command used.

**Validation gate, hard, before any classification was trusted**: recomputed, for all 8
views, the relaxed-admit count, the percentage within dE 10, the median dE, the
twin-paint %, the mesh-silhouette %, and the registration IoU, and required each to
match the first sitting's own console log exactly.

| view | yaw | relaxed: got / expected | pct within dE10: got / expected | median dE | twin paint% | mesh sil% | IoU |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 16,170 / 16,170 | 30.29 / 30.29 | 19.6/19.6 | 29.7/29.7 | 29.7/29.7 | 0.9228/0.9228 |
| 1 | 45 | 11,065 / 11,065 | 37.48 / 37.48 | 15.4/15.4 | 26.5/26.5 | 27.0/27.0 | 0.9630/0.9630 |
| 2 | 90 | 5,197 / 5,197 | 29.19 / 29.19 | 16.0/16.0 | 19.1/19.1 | 18.1/18.1 | 0.9249/0.9249 |
| 3 | 135 | 4,540 / 4,540 | 29.27 / 29.27 | 13.4/13.4 | 27.0/27.0 | 27.1/27.1 | 0.9501/0.9501 |
| 4 | 180 | 10,831 / 10,831 | 28.92 / 28.92 | 17.0/17.0 | 30.6/30.6 | 29.7/29.7 | 0.9105/0.9105 |
| 5 | 225 | 10,446 / 10,446 | 42.88 / 42.88 | 11.6/11.6 | 27.2/27.2 | 27.0/27.0 | 0.9336/0.9336 |
| 6 | 270 | 14,366 / 14,366 | 34.37 / 34.37 | 17.4/17.4 | 17.3/17.3 | 18.1/18.1 | 0.9522/0.9522 |
| 7 | 315 | 7,063 / 7,063 | 47.03 / 47.03 | 10.9/10.9 | 29.0/29.0 | 27.1/27.1 | 0.8970/0.8970 |

**All 8 views, 6/6 cross-checks each: EXACT MATCH.** Full console:
`map\logs\run1_stdout.txt`. Gate 0 (twin provenance) also re-verified fresh this
sitting: all 8 accepted twins' sha256 match `facet_A1_accepted_ring\MANIFEST.json`
exactly (`map\logs\run1_stdout.txt` lines 1-15). The flagged-pixel set classified below
is bit-identical to the set that fired the ANDON.

### Why the palette's region BOXES are not used spatially — a measured fact, not a new derivation

`canon/A1-palette.json` instructs using its region boxes and bands for class 1 "where
they exist." Checked before writing any classifier: the boxes (`rect_px`/`rect_frac`)
are pixel coordinates in `canon/A1_reference.png`'s own space — confirmed via PIL to be
**1136×1472**, a different aspect ratio than the twin render frame (**576×1024**) or
the clay frame (752×1024). This is not a fresh finding: **E57's own report already
measured the mismatch directly**
(`docs/experiments/E57-a1-reference-first-report.md:605-617`) — a human-read bounding
box on the reference (automated corner-median checks failed on it, the same
four-times-failed method CLAUDE.md names) found the reference's own figure-to-frame
height/width ratio differs from the render's by **1.240x**, and the same report states
plainly at lines 711-712: *"A1's reference... does not share the renders' 752x1024
fixed frame."* No calibration between the reference image and any mesh-rendered frame
exists anywhere in this record, and none is invented here — that would be exactly the
"a global constant must not govern a local feature" / "never invent a box" failure this
repo has paid for repeatedly. **Class 1 therefore uses the palette's LAB BANDS
(`median_rgb255` per region — frame-independent), not its pixel rectangles.**

### Classification, in priority order (per flagged pixel)

1. **Class 1 — nearest-centroid in CIE76 Lab space.** Compare the pixel's dE to the
   LOCAL fitted-background colour (`bgcol` — already computed by the tool's own
   `fit_background` at that exact projected pixel, reused not recomputed) against its
   dE to each candidate declared material's `median_rgb255`
   (`canon/A1-palette.json` → `regions`): `sleeve_L` [154,140,122], `sleeve_R`
   [195,164,133], `mouth` [190,146,100], `face_skin` [114,68,44]. `mouth`/`face_skin`
   are tested ONLY where the pixel sits inside the tool's own `headband` (the SAME
   measured head crop from the first sitting's Gate 1, reused via `meta.json`'s
   `crop`/`crop_res`) — anatomically these features cannot appear elsewhere.
   `sleeve_L`/`sleeve_R` are tested ONLY outside headband. If the closest candidate
   material is closer than local background, the pixel is class 1. This test is
   threshold-free (no invented dE cutoff) — it asks only "closer to a declared material
   or closer to background," which is well-defined and symmetric.
2. **Class 3 — not class 1, and inside `headband`.**
3. **Class 2 — not class 1, not class 3, and OUTSIDE an INDEPENDENT geometry check**:
   E58's own stored raycast silhouette (`facet_E58\controls\sil\a1sil_N.png`, confirmed
   576×1024, pure binary {0,255}, its per-view percentages matching
   `silhouettes.json` and the live-computed `mesh_fm` above to within rounding),
   sampled at NEAREST pixel — deliberately independent of, and stricter than, the live
   bilinearly-sampled `mesh_fm` that the tool's own acceptance criterion (`inm`)
   already required to read `> 0.5` at every flagged pixel's projected location.
4. **Unclassified — everything else.** On-surface per the independent geometry check,
   not in headband, no declared material's colour beats local background. Reported
   honestly rather than absorbed into class 2 (a claim about being outside the figure
   the geometry does not support here) or forced into class 1.

Internal consistency, checked in code for every view: `class1 + class3 + class2 +
unclassified` sums exactly to the flagged count, and each class's share of `relaxed`
sums exactly to the ANDON's own originally-reported percentage (asserted, not just
observed — see `map\logs\run2_classify_stdout.txt`, "check: class shares of relaxed sum
to X% (ANDON's own reported % was X%)" on all 8 lines).

## Results — per-view table, full denominators

Two denominators are reported for each class, because they answer two different
questions: **share of flagged** (the four classes sum to 100% — "of the mass that
fired, where does it sit") and **share of relaxed** (the four classes sum exactly to
the ANDON's own reported percentage — same scale as the original 28.9%-47.0% figures).

| view | yaw | relaxed | flagged (=numerator of the ANDON's %) | class 1 (material) | class 3 (hair/fringe) | class 2 (true exterior) | unclassified |
|---|---|---:|---:|---|---|---|---|
| 0 | 0 | 16,170 | 4,898 (30.29% of relaxed) | 35 — 0.71% of flagged, 0.22% of relaxed | 4,360 — 89.02% of flagged, 26.96% of relaxed | 7 — 0.14% of flagged, 0.04% of relaxed | 496 — 10.13% of flagged, 3.07% of relaxed |
| 1 | 45 | 11,065 | 4,147 (37.48% of relaxed) | 38 — 0.92% of flagged, 0.34% of relaxed | 3,607 — 86.98% of flagged, 32.60% of relaxed | 21 — 0.51% of flagged, 0.19% of relaxed | 481 — 11.60% of flagged, 4.35% of relaxed |
| 2 | 90 | 5,197 | 1,517 (29.19% of relaxed) | 14 — 0.92% of flagged, 0.27% of relaxed | 1,244 — 82.00% of flagged, 23.94% of relaxed | 2 — 0.13% of flagged, 0.04% of relaxed | 257 — 16.94% of flagged, 4.95% of relaxed |
| 3 | 135 | 4,540 | 1,329 (29.27% of relaxed) | 72 — 5.42% of flagged, 1.59% of relaxed | 645 — 48.53% of flagged, 14.21% of relaxed | 1 — 0.08% of flagged, 0.02% of relaxed | 611 — 45.97% of flagged, 13.46% of relaxed |
| 4 | 180 | 10,831 | 3,132 (28.92% of relaxed) | 117 — 3.74% of flagged, 1.08% of relaxed | 2,268 — 72.41% of flagged, 20.94% of relaxed | 1 — 0.03% of flagged, 0.01% of relaxed | 746 — 23.82% of flagged, 6.89% of relaxed |
| 5 | 225 | 10,446 | 4,479 (42.88% of relaxed) | 46 — 1.03% of flagged, 0.44% of relaxed | 3,783 — 84.46% of flagged, 36.21% of relaxed | 4 — 0.09% of flagged, 0.04% of relaxed | 646 — 14.42% of flagged, 6.18% of relaxed |
| 6 | 270 | 14,366 | 4,937 (34.37% of relaxed) | 121 — 2.45% of flagged, 0.84% of relaxed | 3,720 — 75.35% of flagged, 25.89% of relaxed | 9 — 0.18% of flagged, 0.06% of relaxed | 1,087 — 22.02% of flagged, 7.57% of relaxed |
| 7 | 315 | 7,063 | 3,322 (47.03% of relaxed) | 150 — 4.52% of flagged, 2.12% of relaxed | 2,288 — 68.87% of flagged, 32.39% of relaxed | 15 — 0.45% of flagged, 0.21% of relaxed | 869 — 26.16% of flagged, 12.30% of relaxed |

**Grand total, pooled across all 8 views** (flagged = 27,761): class 1 = 593 (2.14%),
class 3 = 21,915 (**78.94%**), class 2 = 60 (**0.22%**), unclassified = 5,193 (18.71%).

### Class 1 breakdown — which material, per view

`mouth` and `face_skin` won **zero** flagged pixels in **every one of the 8 views**.
Every class-1 pixel, in every view, matched `sleeve_L` or `sleeve_R` instead:

| view | sleeve_L | sleeve_R | mouth | face_skin |
|---|---:|---:|---:|---:|
| 0 | 14 | 21 | 0 | 0 |
| 1 | 19 | 19 | 0 | 0 |
| 2 | 5 | 9 | 0 | 0 |
| 3 | 16 | 56 | 0 | 0 |
| 4 | 9 | 108 | 0 | 0 |
| 5 | 21 | 25 | 0 | 0 |
| 6 | 101 | 20 | 0 | 0 |
| 7 | 9 | 141 | 0 | 0 |

Class-1 pixels' median dE-to-matched-material ranges 5.85-8.96 across views; their
median dE-to-local-background ranges 8.49-9.71 (i.e. these pixels sit close to both,
consistently closer to the matched material — see `map\logs\run2_classify_stdout.txt`
for the per-view figures).

### Class 2 — characterized precisely, not just counted

Class 2 measures 1-21 pixels per view, 60 total across all 8 views (0.22% of the
pooled flagged mass). A follow-up measurement (`characterize_class2.py`,
`map\logs\run3_class2char_stdout.txt`) checked, for every one of those 60 pixels, its
distance to the nearest TRUE pixel of the independent E58 silhouette:

| view | class-2 px | distance to independent-silhouette boundary (min / median / max, px) |
|---|---:|---|
| 0 | 7 | 1.00 / 1.00 / 1.00 |
| 1 | 21 | 1.00 / 1.00 / 1.00 |
| 2 | 2 | 1.00 / 1.00 / 1.00 |
| 3 | 1 | 1.00 / 1.00 / 1.00 |
| 4 | 1 | 1.00 / 1.00 / 1.00 |
| 5 | 4 | 1.00 / 1.00 / 1.00 |
| 6 | 9 | 1.00 / 1.00 / 1.00 |
| 7 | 15 | 1.00 / 1.00 / 1.00 |

**Every single class-2 pixel, in every view, sits at exactly 1.00px from the
independent silhouette boundary — never further.** This is consistent with (not proof
of, but exactly what would be expected from) a sub-pixel rounding difference between
the LIVE, bilinearly-sampled `mesh_fm` that every accepted texel's acceptance test
(`inm`) already required to read `> 0.5` at, and the INDEPENDENTLY-stored, nearest-pixel
-sampled E58 silhouette used for this class-2 test — rather than a spatially coherent
exterior region. No pixel classified as class 2 sits 2px or more from that boundary in
any of the 8 views.

## Visual evidence

Per-view overlay images (full size, flagged pixels drawn on the accepted twin,
colour-coded: blue = class 1, amber = class 3, red = class 2, magenta = unclassified):
`map\overlays\a1_v0_contamination_map.png` through `a1_v7_contamination_map.png`.
Combined sheet: `map\sheet\E67_contamination_map_sheet.png` (2304×2302, all 8 views
plus the grand totals).

**Read from the images, not judged**: on every one of the 8 views, the amber
(class-3/headband) markers form a dense, closed ring precisely tracing the boundary
between the mesh's raycast hairline and the twin's own painted curls — directly
matching the first sitting's own visual hypothesis, now with a share attached
(48.5%-89.0% of that view's flagged mass, 78.94% pooled). The sparse blue markers sit
specifically at the sleeve cuffs (wrists), where the cream sleeve fabric's own colour
is close to backdrop — a spatially sensible location for a "declared material inside
the window" match. Magenta (unclassified) markers are visibly scattered along other
garment edges the tested candidate set does not cover — vest/sash hems, trouser
seams, ink-stained fingertips — most visible in view 3's rear three-quarter, which
also has this arc's lowest class-3 share (48.53%) and highest unclassified share
(45.97%) among the 8 views. Red (class 2) markers are not visually distinguishable at
image scale in any view, consistent with the 1-21-pixel counts above.

## Gates

| gate | status | evidence |
|---|---|---|
| Gate 0 (twin provenance) | **PASSED** | all 8 accepted twins' sha256 match `MANIFEST.json` exactly, re-verified fresh this sitting |
| Reproduction/validation gate (this sitting's own, not a charter gate) | **PASSED, 8/8 views, 6/6 cross-checks each** | relaxed count, pct-within-dE10, median dE, twin-paint%, mesh-sil%, IoU all match the first sitting's console log exactly |
| No tool parameter changed | **HELD** | `--bg-de`, `--bg-max-pct`, `--edge-*`, `--facing-min`, etc. all at tool default throughout; `--aspect 576,1024` matches the first sitting's own explicit override, not a new change |
| No cloud call | **PASSED by construction** | no comfy-cloud tool was ever loaded or invoked this sitting |
| Internal consistency (class shares sum to the ANDON's own %) | **PASSED, all 8 views** | asserted in code, not just observed — see `map\logs\run2_classify_stdout.txt` |

## Out of scope, confirmed untouched

Ranking, recommending, or judging any of the above (not done, anywhere). Retuning
`--bg-de`/`--bg-max-pct`/any other parameter to see if a view would pass (not
attempted). Extracting `--diag-npz` by relaxing a threshold (not attempted — the
read-only reimplementation exists specifically because that path was correctly
declined). Reopening the prep/bake stages, the first brush, binding/facesets, W3 — all
untouched, unchanged from the first sitting's own "out of scope" list.

## git status, verbatim

```
On branch main
Your branch is ahead of 'origin/main' by 41 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

This sitting added one file inside the facet repo: this report
(`docs/experiments/E67-contamination-map-report.md`) and the handoff appendix at
`E:\AI\training\facet_E67\handoff.md` (outside the facet repo, in the training tree).
No other file inside `E:\AI\facet` was touched. The 41-commits-ahead state predates
this session (2 commits landed between the first sitting's 39 and this sitting's 41,
from the advisor's own fold of the first sitting's report, visible in `git log`).

## Artifact paths

- Live handoff (both sittings): `E:\AI\training\facet_E67\handoff.md`
- Read-only reimplementation + validation: scratchpad copy at
  `C:\Users\mikey\AppData\Local\Temp\claude\E--AI-facet\428295a0-ff4d-49f0-b0a2-024d00acf529\scratchpad\map_contamination.py`;
  console: `E:\AI\training\facet_E67\map\logs\run1_stdout.txt`,
  `logs\reproduction_console.txt`
- Classification: scratchpad copy at `...\scratchpad\classify_contamination.py`;
  console: `map\logs\run2_classify_stdout.txt`, `logs\classify_console.txt`; data:
  `map\data\summary_table.json`
- Class-2 characterization addendum: scratchpad copy at
  `...\scratchpad\characterize_class2.py`; console/output:
  `map\logs\run3_class2char_stdout.txt`, `logs\class2_characterization.txt`
- Sheet builder: scratchpad copy at `...\scratchpad\build_map_sheet.py`
- Per-view overlays: `E:\AI\training\facet_E67\map\overlays\a1_v{0..7}_contamination_map.png`
- Combined sheet: `E:\AI\training\facet_E67\map\sheet\E67_contamination_map_sheet.png`
- Raw per-view arrays (intermediate, not a deliverable): `map\data\_raw_results.pkl`

## Role discipline

No quality judgment, ranking, or recommendation is offered anywhere above — every
number is reported as a count and a share, against two explicit denominators. Every
intermediate quantity this sitting depended on (the flagged-pixel set itself) was
validated against an independent source (the first sitting's own console log) before
being trusted, with a hard assertion in code rather than a visual approximation. The
class-2 finding (0.22% pooled) was not accepted at face value — it was characterized
further (the 1.00px-from-boundary measurement) before being reported as effectively
negligible, and even that characterization is offered as "consistent with," not
"proof of," a rounding artifact — the alternative (a genuine but vanishingly small
exterior-contamination population) is not ruled out, only bounded. No tool parameter
was changed. No ANDON was re-run. No cloud call was made. No memory write was made. No
git commit was made. No child agent was used for core work. This sitting answers where
the flagged mass sits; it does not decide what should be done about it — the advisor
rules and the Director decides.
