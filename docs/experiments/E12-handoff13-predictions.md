# E12 handoff 13 — predictions, registered before the work

**Executor session, 2026-08-06.** Written **before** any measurement of this dispatch: before
A2's arithmetic ran, before a crop frame was rendered, before a crop twin existed, before
either stage-1 projection ran, and before `project_twins.py` was touched.

**Blind status, disclosed per item.** Three classes appear below and they are labelled:

- **BLIND** — no recorded number bears on it; a guess with a reason.
- **DERIVED** — computed from numbers already in the repo (the head box JSON, the prep
  bake's own meta and log, the companion sidecar, `ceiling.json`, `offsurface.json`). Not
  blind, and saying so is the point: a derived prediction that misses is a *stronger* finding
  than a blind one that misses, because the derivation is on the page and can be audited.
- **CODE-READ** — read off the source of a tool I am about to run, before running it. These
  are predictions about the *construction*, and three of them below say the construction is
  wrong in a way no run in this arc has yet exercised.

What I have read to write this: `CLAUDE.md`, the E13 spec, Rulings 21–23f, handoff 11's and
handoff 12's reports, `profiles/beast.json`, `E12_prep/{meta.json,prep.log,ceiling.json,
offsurface.json}`, `E12_gate0/head_00003.json`, the companion sidecar, and the sources of
`project_twins.py`, `bake_hero_prep.py`, `e12_head_render.py`, `e12_crop_silhouette.py`,
`turn_render.py` and `e12_pair_cloud_step.py`. I have run exactly one thing: a five-line float
check on `cam_axes` (P4a), whose result is quoted below because it decides what I build.

---

## P1 — A2's arithmetic (Task 1)

The unit: **atlas texels per crop-twin pixel, over the same patch of surface** — head-box
surface the crop camera can actually see, counted as (a) valid atlas texels whose 3-D position
lies inside `head_box_blender` and which are first-hit visible from the crop camera, against
(b) crop-frame pixels whose first hit lies inside that box. Both sides measure the same
physical surface, so neither side can be moved by reframing alone.

- **P1a — DERIVED. Direction: the atlas UNDER-resolves the crop paint.** Ratio < 1.0.
  Head surface-area share ≈ 103,591 × 1.9437e-6 / (103,591 × 1.9437e-6 + 883,234 × 2.3505e-6)
  = **8.84%** of the mesh (`head_00003.json`'s own face counts and mean face areas), against a
  crop frame that spends 100% of 1,849,600 px on a box covering ~33% of its area.
- **P1b — DERIVED. Magnitude: 0.08 – 0.25, centre ~0.14.** Visible head surface ≈ 0.06 world²
  → ≈ 85,000 atlas texels at 3,240,510 texels / 2.277 world²; crop pixels on head ≈ 0.0306
  world² projected / 0.305² frame × 1,849,600 ≈ 609,000.
- **P1c — DERIVED. The full-figure counterpart of the same ratio is 0.9 – 1.9, centre ~1.26.**
  The load-bearing companion number, registered because it decides what A2 *means*: if the
  atlas is roughly matched to the route frame and badly under-matched to the crop frame, the
  4096 bake was never the bottleneck — the generation frame was — and A2 is a consequence of
  A1 rather than an independent arm.
- **P1d — DERIVED. The rule fires and asks for the cap.** 1/0.14 ≈ 7× the texel density is
  2.67× linear, above the registered cap, so the rule as written arms `head-scale 2.0`.
- **P1e — CODE-READ, and I expect to report this rather than execute it.**
  `bake_hero_prep.py` has no head *region*; it has `--crop`, a **front-view pixel rect**, and
  it scales every UV island containing any face whose centroid projects into that rect. The
  profile pins that rect at `360,240,700,600` — W3's face rect, kept explicitly inert at
  head-scale 1.0 and carrying, in the profile's own words, "no beast meaning". The existing
  bake already measured what it selects on this mesh: **418,979 / 986,814 faces in the band,
  542,699 faces in the head islands, 51.79% of UV area** (`prep.log`, `meta.json`). The
  measured head box is **103,591 faces, 10.497%**. The lever the rule reaches for therefore
  selects **5.2× more faces than the head** and over half the mesh's texel budget. Predicted:
  arming `head-scale 2.0` against that rect does not put texels on the head — it rescales half
  the mesh and re-normalises in `pack_islands` — so the honest report is *the rule's premise is
  false on this subject*, not a re-bake. Correcting it means writing a beast head rect into the
  profile, which this dispatch forbids and which is a ruling's to make.
- **P1f — DERIVED, secondary.** If the re-bake is armed anyway, `bake_hero_prep`'s own growth
  ANDON (`share_area > share_area_pre × 1.2`, i.e. > 0.6215 from 0.5179) is close to a coin
  flip at head-scale 2.0 with 55% of faces already in the band. I give it **60% to pass**,
  which means a 40% chance the expressibility halt fires. Either outcome is reportable.

## P2 — the crop twins (Task 2)

Frame, pre-registered before the render exists: the **yaw-invariant span** the companion
sidecar records (horizontal diagonal of the head box, 0.272333, × pad 1.12 ≈ **0.305013**,
`e12_head_render.py`'s default derivation) used for **both** yaws so the two crops share one
scale, at **1360 × 1360** — the companion's pixel budget and its ÷16-legal frame. The
companion's own 0.223104 was a single-yaw override and does not survive to a two-yaw set: at
45° the head box's horizontal span is 0.272 and 0.223 would crop it.

- **P2a — DERIVED. Resolution gained over the route frame: 2.99× linear, 8.97× area.** The
  head box's 0.1992 vertical extent spans 888 px at the crop against 297 px in the 1792 × 1024
  route frame. (The companion's headline 11.2× was against the *pair's* mouth box at a tighter
  single-yaw scale; it does not transfer and I am not quoting it as if it did.)
- **P2b — BLIND. D8 (ember-orange eyes) lands as an eye on at least one of the two crops**,
  ≥ 500 px of ember-orange in the socket. Reason: the companion's crimson teardrop was v4 stems
  at a *tighter* frame, and Ruling 15h closed D8 on the accepted pair at a 193 px slit-pupil
  iris — so the element is known to be able to land. 60/40.
- **P2c — BLIND. D10 (pale ivory fangs and tooth rows) resolves as separate teeth on the yaw-0
  crop** rather than as a pale band. 70/30.
- **P2d — BLIND. D5 (bone-ivory crown and cheek spikes) lands on both crops**, and the
  merged-lobe read the Director banked at 18g is *still* legible as merged at this scale rather
  than resolving into separate spikes. 60/40 on the second clause.
- **P2e — DERIVED from the v9 set. Gate and channel bands.** 16e off-palette **5 – 30%** (v9
  full-figure ran 4.82 – 23.91%); 17d achromatic **3 – 15%**, below the full-figure
  8.36 – 16.37% band because the head carries the green/ivory/orange families and not the
  charcoal limb mass; largest achromatic connected component **< 20,000 px**.
- **P2f — DERIVED. Registration IoU at the crop frame ≥ 0.98 on both** (the spec's H2; the
  companion measured 0.993953). Band 0.980 – 0.996.
- **P2g — DERIVED. Stem derivation.** The v9 entry carries 20 terms. Predicted: the yaw-0 crop
  keeps **14 – 17**, the yaw-45 crop the same or one fewer. D6's *dorsal and tail* term and D7
  (claws/feet) drop on both — the companion's recorded drops. **The neck spines are the term to
  verify, not assume**: the nape crest sits at the box's lower rear, and I predict it **enters
  the yaw-45 crop and is marginal at yaw 0**. D3 (membranes) is the companion's flagged case —
  both wings entered its crop at the edges — and I predict it enters **both** crops at the
  wider span.
- **P2h — DERIVED. Seed resistance: 0 of 2 re-rolls spent.** Ruling 21c's map names view 4 (two
  terms) and view 3 (a deterministic flat-black limb) at seed 770700. Neither yaw 0 nor yaw 45
  is in it, across four stem generations. Named alternative so this falsifies usefully: if a
  re-roll does fire, I predict the ground is an **off-palette blob at a material boundary**,
  not a term failing to bind.
- **P2i — DERIVED. Harmonization moves these crops less than it moved view 4.** The transfer's
  mean L\* correction toward reference view 1 lands at **|Δ| ≤ 3.0** on both, inside the
  seven-view 4.4 L\* band rather than near view 4's −9.24, because a head crop is dominated by
  the same green/ivory families the reference is.

## P3 — stage 1 (Task 3)

- **P3a — DERIVED. Reach is invariant; the ceiling instrument returns 1,635,304 / 3,240,510 =
  50.46%, unchanged.** `project_twins` sets `reachable` from facing + visibility **before** any
  frame test (`:633`), so a crop camera at a yaw the eight already contain marks exactly the
  texels that yaw already marked. If this moves, the crop camera geometry is wrong — which is
  what the check is for.
- **P3b — DERIVED. A0 styled/reachable 78 – 88%, centre ~83%; styled/valid 39 – 45%.** Below
  both precedents (ship 86.4%, character 92.8%), and the *why* is registered rather than a
  split difference: this subject's mass is thin structure — the thin-mask curve peaks at
  **1.78× membrane concentration** and withholds 15.3% of the visible figure at 0.01 — and the
  A3 invariant still removes up to a third of the area of the thinnest strata. Both precedents
  were thicker subjects.
- **P3c — DERIVED. A1 − A0 in styled/reachable: −0.5 to +1.5 points, centre +0.1.** The crop
  cameras re-see reachable surface; A1 is a *swap of ownership*, not a coverage gain. Per
  CLAUDE.md's swap law I will characterise what left, not bank the net.
- **P3d — BLIND. The crop twins own 40,000 – 160,000 texels in A1** (1.5 – 6% of A1's styled
  set), concentrated in the head box, read off `_owner.npy` rather than inferred.
- **P3e — BLIND, H3's branch: the POSITIVE branch, sub-proportionally.** The head reads visibly
  crisper at the Director's zoom, but by far less than 9× — because if P1b holds the atlas is
  the binding constraint at ~0.14 texels per crop pixel, so most of the crop's extra resolution
  has nowhere to land. Consequence registered now so it cannot be chosen later: **if the sheet
  shows little or no gain, the honest reading is P1b's, not H1's** — the mush would be an
  allocation limit rather than a generation limit, which is the spec's own pre-registered
  negative branch with the allocation lever named as the primary arm.

## P4 — three construction predictions, from reading the code before running it

These matter most on the record, because each says something is wrong that no run in this arc
has exercised.

- **P4a — CODE-READ, already checked and quoted. Two cameras at the same yaw can be tied
  exactly only at multiples of 90°.** Ownership is `take = w > best_w[idx]`, strictly greater,
  so an equal-weight later view never overwrites — that is the never-overwrite invariant the
  dispatch composes with, and it needs the two weights to be *equal*. `--view IDX=PATH` derives
  yaw as `IDX × step` and no index may repeat, so a crop camera at yaw 0 must be addressed as
  index 8 (360°) and yaw 45 as index 9 (405°). Measured: `cam_axes(360)` is **bit-identical**
  to `cam_axes(0)` (the snap at `:375` is load-bearing and covers it), and `cam_axes(405)`
  **differs from `cam_axes(45)` by 2 ULP** — the irrational components are not snapped.
  **Prediction: it does not matter**, because `facing = (N @ dtc).astype(np.float32)` at `:620`
  quantises to float32, and a 2.2e-16 relative gap straddles a float32 boundary with
  probability ≈ 3.7e-9 per texel — expected flips over ~10⁶ contested texels ≈ **0.004**. I
  predict **0 differing float32 facings** at yaw 45, and will measure it rather than argue it.
- **P4b — CODE-READ. `project_twins` has no frame-bounds test, and that makes crop projection
  wrong.** `bilinear` **clamps** x and y into the frame (`:351–352`), so a texel whose
  projection falls *outside* a crop frame is sampled at the frame's border instead of being
  rejected. On the full-figure path this is inert — the frame contains the mesh by construction
  — which is why four experiments never saw it. On a head crop the body below the neck clamps
  onto the bottom border, where the neck's own paint sits; those texels carry the same facing
  weight as the full twin at that yaw **and are processed first**, so they would win.
  Predicted: without a bounds test the yaw-0 crop paints on the order of **10⁴ – 10⁵ texels
  outside the head box** with border colour. Consequence registered in advance: I will add the
  bounds test, prove it inert on the default path by re-running the recorded E13 Gate 0 anchor
  for **0 differing pixels**, and report the out-of-frame count per view as the diagnostic that
  shows the fix was needed.
- **P4c — CODE-READ. `project_twins` derives its frame height-fit while this subject renders
  width-fit, so the projection's frame is ~0.33% larger than the twins'.** `:229` is
  `v_ext = (bhi[2] - blo[2]) * 1.204` with the margin hardcoded and no `--fit-axis`; the profile
  pins `turn_render --fit-axis width`, which sets `ortho_scale = max(size.x, size.y) × margin`
  (`turn_render.py:113`). Predicted **h_ext 1.207877 against the render's 1.203884, ratio
  1.00332** — every sample displaced outward by up to 0.33% of its distance from frame centre,
  ≈ **3.0 px at the horizontal edge, 1.7 px at the vertical**. This is the framing-family law
  (E04 Ruling 25) with a **fourth consumer nobody pinned**. Registered consequences: it is
  **pre-existing and shared by A0 and A1**, so the H3 comparison survives it; it is **not mine
  to fix in this dispatch** (it moves stage 1's registration and needs a ruling); and I predict
  the measured render-vs-projection silhouette bbox disagreement confirms it at ~0.33% rather
  than at 0.

## What would falsify each

P1: a ratio ≥ 1.0 kills P1a–P1e outright and the rule says no re-bake. P2h: any re-roll spend.
P3a: any movement in reach at all. P3c: a swing outside ±1.5 points either way. P4a: any
non-zero float32 facing difference at yaw 45. P4b: an out-of-frame count of 0. P4c: a measured
bbox agreement at 1.000.

**No verdicts in this file, and none in the report that follows it.** The Director judges the
sheet; this session measures.
