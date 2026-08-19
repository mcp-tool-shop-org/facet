# E71 report — the fill, graded on what it could reach, and a mechanism Gate D found

Executor seat (Sonnet), background. Charter: `docs/experiments/E71-hole-fill-kickoff.md`
(original spec, Amendments 1-4, RULING). **The amended spec ran; the original 1,468-texel
fill population was withdrawn before this seat started and was never acted on.** Read whole
before any work: the charter with all four amendments and the ruling; `E:\AI\facet\CLAUDE.md`;
`docs/experiments/E69-whole-figure-withhold-report.md`; `docs/experiments/
E70-baked-look-report.md`. Working tree `E:\AI\training\facet_E71\`. Live handoff kept
throughout: `E:\AI\training\facet_E71\handoff.md`. Predictions written and committed to disk
BEFORE any fill, render, or measurement ran: `E:\AI\training\facet_E71\predictions.md`.

**ZERO SPEND. LOCAL ONLY.** No comfy-cloud tool was loaded or invoked. No cloud call of any
kind. `--max-edge-median`, `--max-frac-beyond`, and the palette gate's bands/floor were never
retuned — where an instrument could not run, it was reported as blocked, not routed around.

## ⚠ Read this before the Arm R column on any sheet in this arc

**44.03% of what Arm R writes (25,689 of its 58,346 filled texels) is the grey(107,107,107)
fallback constant, not paint.** Arm R's clean ANDON readings (median 0.375 edges, both
thresholds passed) do not certify the visible result — the ANDON measures 3D source
distance, and a grey texel one triangle-edge away from another grey texel is a short,
ANDON-legal hop that writes nothing. **Do not read the Arm R column, on this sheet or the
sheet requested below, as a fill that worked.** Full mechanism and reconciliation: "THE
CENTRAL FINDING," below.

## Advisor corrections received mid-arc, attributed, source-checked

The advisor reviewed this report after it was written and issued two corrections to the
RULING this seat executed against. Both are the advisor's corrections to the advisor's own
Amendment 1 and RULING — not this seat's — recorded here per the advisor's instruction, with
the source lines that verify them independently of anything in this report.

1. **The ruling's pre-registered reading of Gate D was wrong.** The ruling stated: *"If the
   two arms' renders differ, `__reachable__` is wrong, and that finding outranks the fill."*
   The advisor's correction: it does not. This seat's own reconciliation (below) closes to
   the texel and shows Arm F carries zero grey(107,107,107) texels anywhere in the valid
   region — the reachability *partition* is not implicated by the Gate D difference; what is
   implicated is which of the two arms' `holes.png` scopings is a sound *source pool* for the
   3D-nearest-neighbour fill. The ruling enumerated one cause for a gate that had two.
2. **The graded/reported arm assignment was backwards.** The RULING graded Arm R and left Arm
   F reported-only. The advisor's correction: Arm F is the sound arm for anything a camera
   can see, because its source pool is real paint only, by construction —
   `tools/texpass_finalize.py:68`, `have = valid & ~holes`, read against Arm F's `holes.png`
   (all 2,044,423 unwritten texels marked as holes) means `have` there is exactly the
   1,425,925 originally-styled texels, never the grey fallback. Arm R's `have` (same line,
   its own narrower `holes.png`) is 3,412,002 texels — the 1,425,925 styled ones **plus** the
   1,986,077 still-grey unreachable ones, which is what let 44.03% of Arm R's fill source
   from grey. Arm R's clean ANDON population is worthless on those 25,689 texels because the
   ANDON cannot distinguish "close to real paint" from "close to another unfilled texel."
   Arm F's own stated defect (a diluted ANDON population, drawing 97% of its lookups from the
   unreachable set) is real — reported, not graded, in this seat's original measurements
   above — but cannot touch the *visible* result, because by definition no camera in the ring
   renders the unreachable texels that dilute it.

Independently confirmed by this seat before this section was written, not taken on the
advisor's word alone: `tools/texpass_finalize.py:68` reads exactly `have = valid & ~holes`
(`sed -n '66,70p' tools/texpass_finalize.py`); `canon/A1-palette.json` has no `allowed_bands`,
`min_chroma`, or `gate` key at its top level (`json.load` + key check, reported above under
"The bleed instrument"). Both match the advisor's citations exactly.

## ⚑ Headline, per the ruling's own pre-committed framing — SEE THE CORRECTION ABOVE

**Gate D fired: 81,452 differing pixels between Arm R's and Arm F's renders, summed over all
8 views (1.726% of the 4,718,592 total rendered pixels).** Not zero. The ruling's own words,
as executed against in real time: *"If the two arms' renders differ, `__reachable__` is
wrong, and that finding outranks the fill."* That framing is left exactly as reported at the
time, below, for the record of what this seat measured against — **but per "Advisor
corrections received mid-arc" above, the advisor has since withdrawn the "`__reachable__` is
wrong" reading itself: this seat's own reconciled mechanism (which the paragraph below
already reported, unprompted, as the more precise account) is now the standing explanation,
not a supplement to a "wrong partition" verdict that turned out not to hold.** The measured
mechanism is not that `__reachable__` misjudges *visibility* (the affected texels are
demonstrably visible — they render, with different colours, at identical screen locations in
both arms) but something else the DATA-only scoping of Arm R's `holes.png` allowed.

## Predictions vs. measured, each disclosed as blind or not

Full text and reasoning, written before anything ran: `E:\AI\training\facet_E71\
predictions.md`.

| # | prediction (band) | blind? | measured | verdict |
|---|---|---|---|---|
| P1 | Arm R median source distance: 0.05-1.5 edges | BLIND | **0.375 edges** | **CONFIRMED**, within band |
| P2a | Arm F median ABOVE Arm R's; Arm F band 0.3-3.0 edges | BLIND | Arm R 0.375, **Arm F 0.974** edges | **CONFIRMED** — direction and band both hold |
| P2b | Arm F `dist_beyond_pct` (beyond 20 edges): 0.5-8% | BLIND | **0.607%** | **CONFIRMED**, within band, near the floor |
| P2c | frac-beyond ANDON more likely to fire than median ANDON | BLIND | median at 32.5% of its ceiling (0.974/3.0); frac-beyond at 12.1% of its ceiling (0.607/5.0) — median is proportionally CLOSER to firing | **FALSIFIED** — neither fired, but the ordering guess was backwards |
| P2d (implicit) | does either of Arm F's ANDONs fire | flagged as open in predictions.md, not itself banded | **Neither fired.** Both arms exit 0. | resolved: NO |
| P3 | Gate D diff pixels: "a few hundred to low tens of thousands," ~0.01-0.5% of 4.7M rendered px | BLIND | **81,452 px, 1.726%** | **FALSIFIED** — above the predicted band in both absolute count and percentage |
| P4 | instrument cannot execute against `canon/A1-palette.json` on any input; `KeyError: 'allowed_bands'` | NOT BLIND (confirmed pre-flight) | Re-run against the real E70/Arm R renders: **same error, same line, exit 1** | **CONFIRMED**, not path-dependent |

**P3's qualitative framing was half right and half wrong, stated plainly rather than
smoothed over.** I predicted a real, nonzero Gate D driven primarily by Blender's texture
minification/bilinear filtering blending across `__reachable__` boundaries. That mechanism
is plausibly still a contributor to the pixel-count-above-texel-count spread (see below), but
it is NOT the dominant driver — the dominant driver is a specific, exactly-reconciled defect
in how Arm R's own fill sourced colour (next section), which I did not anticipate when
writing predictions.md. The direction (nonzero) was right; the size and the primary cause
were both underestimated.

## THE CENTRAL FINDING — why Gate D fired, reconciled exactly

`texpass_finalize.py` was not modified; the scoping is entirely in the `holes.png` each state
directory carries (Amendment 1's own instruction). Arm R's `holes.png` marks only the 58,346
reachable-and-unwritten texels as holes. Every other valid texel — including the 1,986,077
unreachable ones, which still carry the raw `--hole-grey` fallback colour RGB(107,107,107) in
the source atlas (Amendment 2) — is therefore not a hole from the tool's point of view, and
is a legal cKDTree fill *source* for Arm R's 58,346 targets, whether or not it is actually
painted.

Measured directly on `atlas_R.png`, then reconciled against `atlas_F.png` at the identical
58,346 texel locations:

| population (of Arm R's 58,346 targets) | count | share |
|---|---:|---:|
| Arm R found the same real neighbour colour Arm F did | 32,401 | 55.533% |
| **Arm R is still exactly grey(107,107,107) — sourced from an unreachable, unfilled neighbour** | **25,689** | **44.029%** |
| Arm R found a DIFFERENT real (non-grey) colour than Arm F | 256 | 0.439% |
| **total** | **58,346** | **100.000%** |

The 256-texel residual (0.439%) is reported rather than folded into either of the other two
rows: my own pre-registered reasoning (shared-source-pool argument in predictions.md's
corrections section) predicted Arm R and Arm F would agree wherever Arm R's nearest neighbour
was real, and that holds for 55,533 of 55,945 such cases but not all of them — a small,
honestly-reported gap in that reasoning, not zeroed out.

**Whole-atlas reconciliation closes exactly, to the texel, both directions:**

- Arm F: **0** texels remain grey(107,107,107) anywhere in the valid region — consistent with
  its source pool (the 1,425,925 originally-styled texels only) never containing grey.
- Arm R: **2,011,766** texels remain grey — exactly 1,986,077 (the unreachable population,
  untouched by design; not this arm's job) **plus** 25,689 (this finding). `1,986,077 +
  25,689 = 2,011,766`, confirmed by direct count, not arithmetic alone.

**On the Director's own named target, the sharper number:** of the original 1,468 marginal
E68→E69 holes (vest-front/collar/shoulder/hair-speckle — confirmed 100% inside Arm R's
58,346 scope), **474 (32.29%) are still grey(107,107,107) after Arm R's fill; 994 (67.71%)
took a real neighbour colour.** All 1,468 carry `owner=-1` in `atlas_widescope_owner.npy`
(unowned by any camera write, consistent with being holes by definition — this array records
who *wrote* a texel, not who could *see* it, so it does not further localize which of the 8
cameras is involved; not pursued further at this arc's scope). Sampled non-grey outcomes read
as plausible cream/skin-adjacent tones (e.g. RGB(216,205,180), RGB(218,205,181),
RGB(166,125,96)) — described factually, not checked against canon by name, and not a quality
judgment.

**Screen-space, illustrated.** A tight, 4x-scaled crop around Gate D's largest single
connected component in view 0 (2,541 px, bbox y[541:723] x[266:313], the trouser V-front
between the legs) shows a large, flat, uniform grey wedge in the E70 render; in Arm R the
SAME wedge shows the same flat grey through its interior with a mottled, slightly-varied rim
— matching the mechanism exactly: the wedge's deep interior is unreachable (untouched by
either arm), and only its reachable *rim* was in scope for Arm R, where roughly half of that
rim's fills landed on grey rather than paint. A second crop (view 0, left sleeve, 1,414 px
component) shows a diffuse, scattered speckle of single-pixel differences across the cream
sleeve fabric rather than one large blob — consistent with the finer, more distributed part
of the affected population. Both crops: `E:\AI\training\facet_E71\data\
tight_combo_v0_c0.png`, `tight_combo_v0_c1.png` (three panels each: unfilled | Arm R filled |
cyan diff-overlay).

**Gate D per view:**

| view | yaw | diff px | % of frame | in HEAD crop | in COLLAR crop | max channel |Δ| |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 0   | 17,107 | 2.900% | 3,247 (19.0%) | 7,315 (42.8%) | 130 |
| 1 | 45  | 14,231 | 2.413% | 2,244 (15.8%) | 4,327 (30.4%) | 141 |
| 2 | 90  | 6,341  | 1.075% | 1,733 (27.3%) | 2,281 (36.0%) | 124 |
| 3 | 135 | 8,090  | 1.372% | 1,387 (17.1%) | 2,490 (30.8%) | 125 |
| 4 | 180 | 6,846  | 1.161% | 1,178 (17.2%) | 2,135 (31.2%) | 125 |
| 5 | 225 | 8,286  | 1.405% | 1,698 (20.5%) | 2,423 (29.2%) | 124 |
| 6 | 270 | 6,595  | 1.118% | 1,883 (28.6%) | 2,284 (34.6%) | 123 |
| 7 | 315 | 13,956 | 2.366% | 2,530 (18.1%) | 4,420 (31.7%) | 129 |
| **total** | | **81,452** | **1.726%** | | | |

A large share of every view's diff pixels (61.7% for view 0 alone: head+collar) fall inside
the sheet's own head/collar crop windows — the crops the Director will actually look at were,
by construction (they follow the mesh's own silhouette, not chosen to include or exclude
this), already positioned over a substantial fraction of where the two arms disagree.

Per-view diff masks (screen space, white = differs): `E:\AI\training\facet_E71\data\
gateD_diffmask_v{0..7}.png`.

**What the "near-neutral" share of diff pixels shows, and its limit.** 25-33% of each view's
diff pixels are near-neutral in Arm R's own render (max channel − min channel ≤ 3), with a
mean value of ~132-139/255 — consistent with grey(107,107,107) rendering through this
pipeline's exposure (+0.85 stops) and Standard view-transform round-trip (not independently
re-derived to the exact digit; the direction and order of magnitude match). The remaining
67-75% of diff pixels are NOT simply grey-vs-colour at the pixel level; they carry more
saturated tones in both arms' renders. This is consistent with texture minification (the
atlas is 4096×4096, each render is 576×1024, a large downsampling factor, and
`bake_hero_pack.py`'s Image Texture node takes Blender's default bilinear/mip filtering,
never overridden) spreading each grey-sourced atlas texel's influence into a small
neighbourhood of screen pixels beyond its own exact footprint — offered as the same
reasoning predictions.md pre-registered, now understood as a secondary amplifier of the
25,689-texel defect rather than a free-standing cause.

## Gates

| gate | status | evidence |
|---|---|---|
| Gate C — E69 source atlas bytes unchanged at close | **PASS** | sha256 `66b8602b1e8d1a61e1c536f75730170fdfec3a5292f47de540dad7f2408727f2`, identical before state-dir construction and after both finalize runs. Also checked, not required by name: `prep_uv.glb` sha256 unchanged (`b2e0fca7...1bd6c6`). |
| Arm R ANDONs (`--max-edge-median 3.0`, `--max-frac-beyond 0.05`) — ungated by this seat, reported | **Both PASSED.** median 0.375 edges; beyond-20-edges 0.000% | `E:\AI\training\facet_E71\out\report_R.json`, `logs\finalize_R_console.txt` |
| Arm F ANDONs — reported, NOT graded per the ruling | **Both PASSED** (not required to; reported as a statement about atlas topology, per Amendment 1). median 0.974 edges; beyond-20-edges 0.607% | `out\report_F.json`, `logs\finalize_F_console.txt` |
| Gate D — pixel comparison, Arm R vs Arm F renders, 8 views, compared as PIXELS not PNG hashes | **FIRED — 81,452 / 4,718,592 px differ (1.726%)** | `logs\gateD_pixel_compare.txt`, per-view diff masks in `data\` |

No ANDON halted either finalize run; both arms completed and both atlases exist, which is why
Gate D could be measured as literally specified (predictions.md had flagged this as uncertain
— see P2d above).

**On "GRADED" / "ungated" / "reported, NOT graded" above:** those labels are this seat's own
words, executed against the RULING as dispatched, and are left as originally written for the
record. Per "Advisor corrections received mid-arc," the advisor has since ruled the
assignment backwards — Arm R's clean ANDON pass does not certify its visible result (44.03%
of what it writes is the grey constant, invisible to an ANDON measuring 3D source distance
alone), and Arm F's diluted-but-passing ANDON is the sound one for anything a camera renders.
The PASS/FAIL readings in the table are unchanged measurements; which arm's ANDON reading
should be trusted as a proxy for visible quality is the part that flipped.

## The sheet

**Two sheets exist on disk; the second, four-column one is the current deliverable.** The
first (v1, three columns) was this seat's own original construction. The advisor then asked
for a five-column rebuild (A1 reference | twin | E70 | Arm R | Arm F); this seat found the
reference column blocked by a measured frame mismatch and, per the advisor's own contingency
instruction, reported that and built nothing rather than improvise a substitute. The advisor
reviewed the measurement, ruled the reference column an over-specification on their own part,
and **decided the sheet: four columns, reference dropped** — accepted twin | E70 mesh
(unfilled) | Arm R mesh | Arm F mesh. That is v2, built this turn, and is the sheet this
report now points to for the Director's eye. v1 stays on disk and is still described below,
because the reference-column finding it sits beside is a real finding about this sheet's
construction and does not disappear into "we built four columns instead of five."

### v2 — the current sheet: twin | E70 mesh | Arm R mesh | Arm F mesh

`E:\AI\training\facet_E71\sheet\E71_hole_fill_sheet_v2_4col.png` (3074×12726px, 12.84MB).
Same construction as v1 and as E70's own sheet before it: four columns per view — accepted
twin | E70 mesh (unfilled atlas) | Arm R mesh (filled, reachable scope) | Arm F mesh (filled,
full population) — plus one head crop and one collar/vest-opening crop per view, all four
panels cropped identically from the same box. Footer verbatim under every view block:

> The warm rim light in the twins is still paint.
> The overlay dots are still the map.

Same crop boxes as v1, reused verbatim from `E:\AI\training\facet_E70\sheet\crop_boxes.json`
— see the byte-identical silhouette-mask confirmation below, unchanged from v1. 96 individual
full/head/collar crop PNGs (4 sources × 8 views × 3 crop types) live in `sheet\crops_v2\`.
**Rank nothing — none is asserted here or in the sheet's own captions.** The sheet's subtitle
states the Arm R / Arm F asymmetry in the same terms as this report's own top-of-file warning
(Arm R 44.03% grey-sourced; Arm F real-paint-sourced but ANDON-diluted by unreachable texels)
so the column labels themselves do not read as a verdict on either arm.

This seat inspected the assembled sheet's title block and its first view row (`data\
v2_top_check.png`, `data\v2_row0_check.png`) to confirm the layout renders as intended —
four labelled full panels side by side, correct separators, correct crop-box citation in the
row-b caption — before treating the build as complete. It did not re-inspect all 8 views'
content at native resolution beyond what v1's inspection already covered (the underlying
renders are identical to v1's; only the layout changed).

### v1 — the original three-column sheet, unchanged, kept for the record

`E:\AI\training\facet_E71\sheet\E71_hole_fill_sheet.png` (2314×12690px, 12.02MB). Three
columns per view — accepted twin | E70 mesh (unfilled atlas) | Arm R mesh (filled, reachable
scope) — plus one head crop and one collar/vest-opening crop per view, all three panels
cropped identically. Same footer as above.

**Crop boxes reused verbatim from `E:\AI\training\facet_E70\sheet\crop_boxes.json`, not
recomputed.** This is valid, not merely assumed: this session independently re-ran
`silhouette_masks.py` on the same prep/profile and confirmed all 8 resulting masks are
**byte-identical** to E70's own `sil\e70sil_{0..7}.png` — the mesh geometry genuinely did not
change between E70 and E71 (only the atlas texture did), so a crop box derived purely from
silhouette geometry carries over exactly. This confirmation is what v2 also relies on.

48 individual full/head/collar crop PNGs (3 sources × 8 views × 3 crop types) live in
`sheet\crops\`. Rank nothing — none is asserted here.

**Panel content, described factually, per this seat's own inspection of the crops used in the
central finding above** (not a full 8-view pass at native resolution, given the finding's own
quantitative characterization is already precise): the trouser V-front wedge and left-sleeve
speckle described above are directly visible in the individual full-resolution renders; this
seat did not judge whether the difference reads as acceptable at the Director's own zoom on
the full sheet — that is the Director's judgment, not a measurement.

### The reference column — attempted and blocked, with the mechanism

**Kept in the record at the advisor's explicit instruction: this is a real finding about the
sheet construction, not a refusal to be smoothed away.** The advisor's mid-arc message first
asked for a five-column rebuild — A1 reference | accepted twin | E70 mesh | Arm R mesh | Arm
F mesh, same construction, same crops from `crop_boxes.json`, head and collar crops required.
The Arm F column was buildable (its renders already existed, same 576×1024 frame, same
crop-box compatibility as Arm R) and is now in v2 above. **The A1 reference column was not
buildable by the specified method, for a measured reason**, reported at the time rather than
routed around, and the advisor subsequently ruled it an over-specification on their own part
— "I asked for it without checking that `canon/A1_reference.png` could be cropped into the
ortho frame" — and decided v2's four-column construction instead. The measurement below is
unchanged from when it was first reported and stands as the record of why.

`canon/A1_reference.png` is **1136×1472px** (aspect 0.7717); every other column's frame is
**576×1024px** (aspect 0.5625) — the twins, the E70 render, and both this arc's renders all
share one ortho-camera convention (`profiles/a1.json`, one `ortho_scale`, confirmed identical
this session), which is the entire reason a single fixed pixel box is "the same zoom" across
those four columns (E70's own `e70_derive_crops.py` docstring: *"since every view shares the
identical ortho_scale ... a FIXED pixel window size is a fixed real-world window size in
every view"*). The reference image predates that convention and was never rendered through
it — it is a freeform 2D concept image, not an ortho-camera capture of the mesh.

Searched for a recorded pixel-space correspondence between the reference's frame and the
render frame before concluding there is none: `profiles/a1.json` (its `verify/turn_render.py`
and `silhouette_masks.py` blocks are derived from A1's own mesh bounding box, not from the
reference image); `docs/experiments/E57-a1-reference-first-report.md` and `docs/experiments/
E58-a1-twin-ring-report.md` (no frame/crop/margin/scale/registration terms co-occur with
mentions of the reference image); `tools/canon_compose.py` (composes the PROSE that produced
the reference — a text tool, not a spatial one). None establish a mapping. `canon/
A1-palette.json`'s own region boxes (`rect_px`, e.g. hair at `[471, 66, 664, 169]`) ARE
measured on this exact reference image, at E57 Stage 1 — but reusing THOSE would be a
different box, from a different method (hand-placed region boxes, not
`crop_boxes.json`'s raycast-silhouette-derived ones), which is not "same crops from
`crop_boxes.json`" and was not done.

**Proof, not inference — the literal boxes applied to the literal file:**
`crop_boxes.json`'s view-0 head box is `[176, 55, 391, 263]` and its collar box is
`[26, 137, 543, 479]` (pixel coordinates in the 576×1024 frame). Cropped directly out of
`canon/A1_reference.png` at those same pixel coordinates:

- **Head box → flat background.** No part of the head is in the crop at all.
- **Collar box → mostly flat background, with the character's face and one shoulder crammed
  into the box's right edge**, badly off-centre — not a collar/vest-opening crop of anything.

Saved for inspection: `E:\AI\training\facet_E71\data\naive_ref_head_v0.png`, `E:\AI\training\
facet_E71\data\naive_ref_collar_v0.png`. This is the measured reason, not a guess: the two
frames have no calibrated relationship, so the literal instruction ("same crops from
`crop_boxes.json`") cannot be executed on this column, and inventing a rescale/reproject to
make it "work" would be exactly the invented-parameter class of error this repo's own record
already warns against (a half-width, margin, or registration arriving by choice rather than
measurement) — and exactly what "do not improvise a substitute" was written to forbid.

**Also worth naming, since it is a property of the asset independent of any registration
question:** even with a frame-correspondence in hand, the reference is a single front-ish
image — there is no side/rear reference view. A column built the way the other four are would
show the identical reference panel in all 8 view-blocks. Establishing a pixel-space
correspondence between `canon/A1_reference.png` and the ortho render frame — and deciding
what an 8-view sheet should do with a column that cannot vary by view — is a separate job
nobody has done, named here so it is not lost.

**At the time this was first reported, nothing had been rebuilt.** The existing v1 sheet was
left unchanged and this seat stopped, per the advisor's own contingency instruction for
exactly this situation. The advisor then reviewed the measurement and made the call above;
v2, built afterward without the reference column, is the result and is described in full
above.

## The bleed instrument — blocked, not routed around

**`palette_gate.py` cannot execute against `canon/A1-palette.json`, on any input, including
the real E70 and Arm R renders.** Confirmed twice: once at pre-flight (predictions.md, a
throwaway path) and once for real —

```
palette_gate.py --palette canon/A1-palette.json
  --images render/e70bake_0.png render_R/e71R_0.png
  --masks  sil/e71sil_0.png sil/e71sil_0.png
```

exits 1 with

```
KeyError: 'allowed_bands'
```

at `tools/palette_gate.py:75`, before either image is opened. `canon/A1-palette.json` has no
`allowed_bands`, `min_chroma`, or `gate` key — its own `_purpose` field states this is
deliberate: *"it GATES NOTHING this arc (no allowed_bands/gate block in the E04/E12/E14
sense) — per the E57 charter,"* and `_provenance.status` is `"PENDING — Stage 1 is a report,
not a ratification."` **No bands, floor, or gate block were invented to route around this** —
that would be exactly the "values arriving by invention rather than measurement" this repo's
own record already ruled against once this session (Amendment 3, `profiles/a1.json`'s
`project_twins.py` block), and there is no precedent number anywhere in this repo for turning
a material's `hue_centre_deg` + `hue_resultant_length` into a band half-width.

**One fact reported ungated, because it needs only the generic sRGB→Lab transform
`palette_gate.py` itself uses, not the broken palette file:** the sole hole-fallback colour,
RGB(107,107,107), has Lab chroma **C\* = 0.0000** exactly (R=G=B is achromatic by
construction). `canon/A1-palette.json`'s own `_chroma_floor.adopted` is 12.0. So even a
fully repaired, gate-shaped version of this file would never flag a surviving grey-107 patch
as off-palette — a chroma-floored instrument structurally cannot see an achromatic fallback
colour. This instrument, working or not, was never going to be the one that catches "grey
still shows through" (the sheet's question, per Amendment 1's own words: "This does not
replace the eye"); it could in principle catch a wrongly-sourced *chromatic* colour landing
outside the declared palette, but only once repaired.

## Two corrections to the dispatch, found before running anything, reported per the
kickoff's own request

Recorded in full in `predictions.md`; summarized here since they materially shaped this
session's approach.

1. **`texpass_finalize.py` does not read `styled_mask.npy`.** The amendment's `--state`
   construction section says the tool "requires" it. Read at `tools/texpass_finalize.py:
   62-66`: only `atlas.png` and `holes.png` are opened from `--state`. Not a blocker — copied
   into both state dirs anyway, at zero cost — but not an accurate claim as written, and not
   treated as one.
2. **`canon/A1-palette.json` cannot be used with `palette_gate.py` as the amendment
   instructs.** See above. This is the more consequential of the two: it prevented P4 and the
   whole bleed-instrument half of this arc's deliverable from producing a number.

## Out of scope, confirmed untouched

The brush (no stroke, no `restylize_views.py` call). Cloud (no comfy-cloud tool loaded or
invoked). Re-bake (`atlas_widescope.png` never regenerated — Gate C). Binding. Retuning any
threshold (`--max-edge-median`, `--max-frac-beyond` at defaults both runs; no palette bands
invented). Ranking the arms — neither is characterized as better or adopted; this report is a
sheet and a set of numbers, per the ruling. `project_twins.py` was not run. `profiles/a1.json`
was not edited. `docs/index/conventions.json` was not edited. `texpass_finalize.py` was not
modified — the two arms differ only in the `holes.png` each state directory carries, per
Amendment 1's own instruction that the scoping is data, not code.

## Testing

No file under `tools/`, `tests/`, or any other tracked path was created, modified, or
deleted. This is a measurement/data arc, consistent with the kickoff's own framing ("The
scoping in this arc is DATA, not code — you should not need to"); no tool code changed, so no
new test is owed by this repo's "tests ride the commit" rule.

## git status, verbatim

```
On branch main
Your branch is ahead of 'origin/main' by 50 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/experiments/E71-hole-fill-report.md
	docs/experiments/E72-stroke-one-kickoff.md
```

**`docs/experiments/E72-stroke-one-kickoff.md` was not created by this seat.** This session
never wrote anything under `E:\AI\facet` before this report file. Its presence is evidence of
a concurrent session elsewhere in the repo (consistent with this repo's own recorded
concurrency hazards); it is reported here so it is not misattributed, and is otherwise
untouched and not investigated further. This seat's only filesystem effect inside
`E:\AI\facet` is the addition of this one report file. No `git add`, no `git commit` was run.

## Artifact paths

- Live handoff: `E:\AI\training\facet_E71\handoff.md`
- Predictions (written before any run): `E:\AI\training\facet_E71\predictions.md`
- State directories: `state_R\` (atlas.png, holes.png=58,346, styled_mask.npy), `state_F\`
  (atlas.png, holes.png=2,044,423 unmodified, styled_mask.npy)
- State-build script + console: `logs\build_states_console.txt` (script itself was a
  scratchpad file, not retained in the training tree — its asserted invariants are recorded
  in this console log)
- Finalize outputs: `out\atlas_R.png`, `out\atlas_F.png`, `out\report_R.json`, `out\
  report_F.json`; consoles `logs\finalize_R_console.txt`, `logs\finalize_F_console.txt`
- Gate C hashes: `logs\gateC_baseline_sha256.txt`, `logs\gateC_final_sha256.txt`
- Packed GLBs: `pack\a1_e71_R.glb` (39,996 KB), `pack\a1_e71_F.glb` (42,817 KB); consoles
  `logs\pack_R_console.txt`, `logs\pack_F_console.txt`
- Renders (8 views each): `render_R\e71R_{0..7}.png`, `render_F\e71F_{0..7}.png`; consoles
  `logs\render_R_console.txt`, `logs\render_F_console.txt`
- Silhouette masks (byte-identical to E70's): `sil\e71sil_{0..7}.png`, `sil\silhouettes.json`;
  console `logs\silhouette_console.txt`
- Gate D: `logs\gateD_pixel_compare.txt`, `logs\gateD_colour_characterization.txt`, diff masks
  `data\gateD_diffmask_v{0..7}.png`
- Grey-source mechanism: `logs\armR_grey_source_check.txt`, `logs\
  armR_vs_armF_full_reconciliation.txt`, `logs\named1468_grey_check.txt`
- Illustrative crops: `data\tight_combo_v0_c0.png` (trouser V-front, 3-panel), `data\
  tight_combo_v0_c1.png` (left sleeve, 3-panel)
- **The current sheet (v2, four columns, the Director-facing deliverable)**:
  `sheet\E71_hole_fill_sheet_v2_4col.png`; crops `sheet\crops_v2\` (96 PNGs); console `logs\
  build_sheet_v2_console.txt`; layout sanity crops `data\v2_top_check.png`,
  `data\v2_row0_check.png`
- The original sheet (v1, three columns, superseded by v2 but kept on disk):
  `sheet\E71_hole_fill_sheet.png`; crops `sheet\crops\` (72 PNGs); console `logs\
  build_sheet_console.txt`
- palette_gate attempt: `logs\palette_gate_attempt_console.txt`
- Reference-column blocker, proof crops (the finding kept in the record per the advisor's
  instruction): `data\naive_ref_head_v0.png`, `data\naive_ref_collar_v0.png`
  (`crop_boxes.json`'s view-0 boxes applied literally to `canon\A1_reference.png`), `data\
  a1_reference_thumb.png` (whole-image thumbnail for context)
- This report: `docs\experiments\E71-hole-fill-report.md` (uncommitted)

## Role discipline

No quality judgment is offered anywhere above — none of this repo's barred quality words
characterize any panel or arm. Gate D's fired status is reported as the ruling pre-committed
it should be, first and prominently; the more precise mechanism this session measured is
offered alongside that framing, not as a substitute for it, and is stated as a measured,
exactly-reconciled fact (55.533% / 44.029% / 0.439%, closing to the texel both directions on
the whole-atlas count too) rather than as a verdict on whether `__reachable__`, the fill, or
either arm is acceptable. Every one of the four required predictions is scored against what
was actually measured, including two falsifications (P2c's ordering guess, P3's band) stated
as plainly as the confirmations. Neither arm is ranked or recommended for adoption. The
palette-gate blocker was reported rather than routed around by inventing thresholds. Two
dispatch inaccuracies are named with the evidence that found them, per the kickoff's own
request. The two mid-arc advisor corrections are recorded as the advisor's corrections to the
advisor's own ruling, with independent source-line confirmation, not silently merged into
this seat's original measurements as if they had been known from the start. The five-column
sheet rebuild was attempted first, found to have one column blocked by a measured frame
mismatch (proof crops on disk, not an inference), and not built as a partial substitute — per
the advisor's own explicit contingency, that was reported instead and the task stopped there
without deciding a partial scope unilaterally. The advisor then reviewed the measurement,
ruled the reference column an over-specification on their own part, and decided the
four-column construction (v2) directly — that decision, not this seat's own judgment, is why
v2 has the columns it has. The reference-column measurement is kept in the record in full,
at the advisor's explicit instruction, rather than allowed to disappear once a sheet existed.
No memory write was made. No git commit was made — one report file sits untracked for the
advisor to fold by pathspec, alongside an unrelated untracked file this seat did not create.
No child agent was used for core work.
