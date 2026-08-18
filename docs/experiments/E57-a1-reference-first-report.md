# E57 report — A1, the reference-first exemplar

**Executor seat (Sonnet), background agent. Charter:
[E57-a1-reference-first-kickoff.md](E57-a1-reference-first-kickoff.md). Written as-you-go,
uncommitted — the advisor commits by pathspec after review.**

This document reports measurements only. It does not judge whether the mesh, the palette,
or the reference are good — that is the Director's call. Words like verified/shipped/
works/decisive/validated/proven do not appear below in that sense.

---

## Stage 0 — provenance freeze (Gate 0)

### Setup

Working tree created: `E:\AI\training\facet_E57\{reference,mesh,renders,sheets}\`.

Source copied to two destinations:
- `E:\AI\training\facet_E57\reference\A1_reference.png`
- `E:\AI\facet\canon\A1_reference.png`

### sha256 sub-check

```
expected:  9417cd6492df34354e5d3f3d7809bf89ddd074f5b1b18725c166a59b97b48dde  (len=64)

9417cd6492df34354e5d3f3d7809bf89ddd074f5b1b18725c166a59b97b48dde  MATCH  C:\Users\mikey\Downloads\Qwen-Image-2512_00021_.png
9417cd6492df34354e5d3f3d7809bf89ddd074f5b1b18725c166a59b97b48dde  MATCH  E:\AI\training\facet_E57\reference\A1_reference.png
9417cd6492df34354e5d3f3d7809bf89ddd074f5b1b18725c166a59b97b48dde  MATCH  E:\AI\facet\canon\A1_reference.png
```

All three MATCH the pre-registered expected hash. **Sub-check: PASSED.**

### Recipe extraction sub-check

Script: `E:\AI\training\facet_E57\extract_recipe.py` (written this seat — no prior recipe
extractor was searched for because the charter frames this as a fresh machine-extraction
task, not a reuse-first enumeration like Stages 1/2). Reads the PNG's `info['prompt']`
(ComfyUI API-format graph, 19 nodes) via PIL, resolves every KSampler field through
`PrimitiveInt`/`PrimitiveFloat`/`PrimitiveBoolean` and `ComfySwitchNode` hops (this graph
gates `steps`, `cfg`, and the active model loader through one shared boolean switch, node
`238:229`, value `false`), and writes UTF-8 directly to the output file — the console never
receives the CJK negative prompt text (a first attempt at `print()`-through-`>` redirection
died with `UnicodeEncodeError` on this rig's cp1252 console, exactly per the CLAUDE.md
warning; left as `reference\A1_prompt_graph.json`, 0 bytes, as a documented trip-wire and
superseded by the direct-file-write approach).

```
EXTRACT COMPLETE
out_path=E:\AI\facet\canon\A1-RECIPE.json
unreadable_field_count=0
positive_text_len=746
negative_text_len=60
model=qwen_image_2512_fp8_e4m3fn.safetensors
sampler_name=euler
scheduler=simple
seed=106
denoise=1.0
steps=50
cfg=4.0
model_sampling_shift=3.1000000000000005
latent_size=1140x1472
png_size=1136x1472
loras_in_graph=[{'node_id': '238:221', 'lora_name': 'Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors', 'strength_model': 1.0}]
active_model_branch={'branch': 'base_unet_no_lora', 'unet_name': 'qwen_image_2512_fp8_e4m3fn.safetensors'}
```

Exit code 0, `unreadable_field_count=0`. **Sub-check: PASSED** — every charter-named field
(positive text, negative text, model, sampler, scheduler, seed, denoise, size, source
filename, sha256, bytes) resolved from the PNG itself. Output written to
`canon/A1-RECIPE.json` (UTF-8).

**Fields beyond the charter's minimum, captured because the graph exposed them for free:**
`steps`, `cfg`, `model_sampling_shift`, `active_model_branch`, `loras_in_graph`,
`latent_width`/`latent_height` (the *declared* `EmptySD3LatentImage` request size, distinct
from the final PNG size).

### Findings (report only, not gates)

**F1 — the Lightning LoRA is present in the graph but was not active for this generation.**
The graph contains a `LoraLoaderModelOnly` node loading
`Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors` at strength 1.0, but the model
path that actually reaches `ModelSamplingAuraFlow` -> `KSampler` resolves through
`ComfySwitchNode` `238:233` with `switch=false`, which selects `on_false` = the raw
`UNETLoader` output, not the LoRA branch. The same switch gates `steps` (`238:240`:
on_false=50, on_true=4) and `cfg` (`238:243`: on_false=4.0, on_true=1.0) — the on_false
values (50 steps, cfg 4.0, no LoRA) are internally consistent as a "standard" preset, and
the on_true values (4 steps, cfg 1.0, LoRA active) are internally consistent as the
Lightning-fast preset. All three switches read the same upstream boolean
(`PrimitiveBoolean` node `238:229` = `false`), so the resolution is not three independent
guesses — one boolean decided all three simultaneously, and the recorded values are
mutually consistent with a real preset toggle rather than a partial/broken graph.
Recorded in `A1-RECIPE.json.active_model_branch` (`base_unet_no_lora`) and
`loras_in_graph` (present-but-not-proven-active) as two separate fields so a future reader
cannot conflate "the LoRA node exists in the workflow" with "the LoRA painted this image."

**F2 — the declared latent width (1140) is not the final PNG width (1136).**
`EmptySD3LatentImage` requests `width=1140, height=1472`; the delivered PNG is
`1136x1472`. 1136 is divisible by 16 (71 x 16); 1140 is not (1140/16 = 71.25). Arithmetic
consistent with 8x latent-space downsampling rounding: floor(1140/8) = 142,
142*8 = 1136 exactly. This has not been independently confirmed against Qwen/ComfyUI's
internal rounding behavior — it is offered as an observation, not a claim. It does not
affect Gate 0: the charter's "1136 x 1472, both div 16, generator-legal by construction"
describes the delivered image, which is what this arc uses, and that claim measures true
regardless of what the latent node requested.

### Identity-diff sub-check

Script: `E:\AI\training\facet_E57\diff_identity_vs_recipe.py`. Checks every NAMED phrase
(N1-N10, transcribed from `canon/A1-IDENTITY.md`'s table) and every `legal_clauses` phrase
(read live from `canon/a1.surfaces.json`) for verbatim substring membership in
`A1-RECIPE.json`'s `positive_text`.

```
--- NAMED (A1-IDENTITY.md) vs extracted positive_text ---
N1: HIT  phrase='plum long-vest with fine gold embroidery'
N2: HIT  phrase='a cream high-collared shirt'
N3: HIT  phrase='an umber sash'
N4: HIT  phrase='slim dark-green trousers'
N5: HIT  phrase='polished brown shoes'
N6: HIT  phrase='olive skin'
N7: HIT  phrase='tousled dark curls'
N8: HIT  phrase='ink-stained fingertips'
N9: HIT  phrase='curious brown eyes'
N10: HIT  phrase='a slight smile'

--- legal_clauses (a1.surfaces.json) vs extracted positive_text ---
frame_subject: HIT  phrase='A young archivist in his 20s'
style_paint: HIT  phrase='painterly digital art with visible brushwork'
style_palette: HIT  phrase='rich saturated palette'
style_face: HIT  phrase='crisp readable facial features'
stage_bg: HIT  phrase='plain warm pale-grey studio backdrop'
stage_no_weapons: HIT  phrase='no weapons'
stage_no_held: HIT  phrase='no held objects'
stage_clear_sil: HIT  phrase='nothing crossing the body silhouette'

TOTAL CHECKED: 18
HITS: 18
MISSES: 0
```

**Sub-check: PASSED.** 18/18 verbatim hits, zero misses. No correction needed to
`canon/A1-IDENTITY.md` or `canon/a1.surfaces.json`.

### Gate 0 verdict: PASSED

All three sub-checks (sha256, recipe-readability, identity-diff) passed. Nothing halted.
Stage 0 artifacts: `canon/A1_reference.png`, `canon/A1-RECIPE.json`,
`E:\AI\training\facet_E57\reference\A1_reference.png`.

---

## Stage 1 — palette bands

### Mid-flight: canon ratified, session continuity note

**Canon ratified.** The Director ratified A1's canon as drafted, 2026-08-17 — all 19
`a1.surfaces.json` rows and all five ratification-queue positions (Q1 name, Q2 ink extent,
Q3 garment decomposition, Q4 stubble, Q5 umber word), each "as drafted." The advisor updated
`canon/a1.surfaces.json` (top-level `note` field + five `ratification_queue[].status` fields)
and `canon/A1-IDENTITY.md` (status block) to record this. **No occupant phrase changed** —
re-read both files post-update and confirm every N1-N10 phrase and every `legal_clauses`
phrase is byte-identical to the text the Gate 0 diff checked. **The 18/18 Gate 0 identity-diff
result stands; it was not re-run.**

This session's connection dropped mid-response during Stage 1 enumeration (an infrastructure
event, not a gate and not a halt). Resumed on the same transcript; `handoff.md` and this report
were current through Stage 0 at the point of the drop, so nothing was lost — re-anchored from
disk before continuing, per the seat's own standing practice for exactly this failure mode.

### Instrument family enumeration (before writing anything new, per charter)

Searched `tools/` and the `E:\AI\training\facet_E04*`, `facet_E12*`, `facet_E14*` training
trees. **The E04/E12/E14 training trees no longer exist on disk** (`ls -d
E:/AI/training/facet_E14*` etc. all return "No such file or directory"; the surviving
`facet_*` trees are E01, E02, E05-E08, E32 and up — the mid-numbered trees have been cleaned
up over time). This is consistent with the charter's own hedge ("enumerate before
commissioning... do not write a new one until the search has failed and the failure is
reported") — the search's outcome here is "the training-tree copies are gone; the derivation
family survives only in `tools/`."

**What exists in `tools/` and `tools/diagnostics/`:**

| script | role | reused for A1? |
|---|---|---|
| `tools/diagnostics/e04_bands.py` | **THE primary band deriver.** `--pair DIR --masks DIR --materials m.json --out DIR`. K-means clusters (k=14 default, fixed seed 770700) pixels in Lab space *inside an exact silhouette mask*, across one or more named views: builds a landing table (does each declared element's expected RGB have a nearby cluster), derives hue bands from clusters above a chroma floor (default 12.0), re-derives the backdrop against measured colours. Explicitly **generalised in E12** ("GENERALISED 2026-08-06 (E12 Task 5)... A subject constant living in a tool is the class profiles exist to remove") — `--tag`/`--asked` became flags with galleon-preserving defaults. Cited as `measured_by` in both `E04-galleon-palette.json` and `E12-beast-palette.json`. | **No, not directly** — see mismatch below |
| `tools/diagnostics/e14_band_density.py` | Supplement used for the longsword: chroma-density scan to locate a floor antimode/knee (rather than inheriting 12.0 blind), hue-density histogram, and a **placement test** (depth-from-silhouette-boundary) that separates antialiased rim bleed from a genuine deep material at the same hue. Cited in `E14-longsword-palette.json`'s `derived_by`. | Concept reused (chroma-density scan before quoting a floor); code not invoked (needs a silhouette mask + multi-view pair) |
| `tools/diagnostics/e14_band_edges.py` | Supplement used for the longsword: trims a band's contiguous hue span to where per-band density falls below 1% of *that band's own peak* (exists on disk; not opened in full this session — cited in E14's provenance as the third leg, not needed for A1 since Stage 1 derives no band edges this arc, see below). | Not reused (A1 has no edges to trim yet) |
| `tools/diagnostics/e12_region_colour.py` | **Named-region (box) colour readout** — median L*/C*/hue inside a caller-drawn rectangle intersected with a silhouette mask, chroma floor withholds hue, reports the chroma distribution (25/75 percentiles, share under floor). Built for a different question ("is this named region a specific colour") than `e04_bands.py` ("what does the whole figure's palette cluster into"). | **Pattern reused** (region-box + chroma-floor-first + percentile reporting); **one defect found and NOT inherited**, below |
| `tools/palette_gate.py` | The **downstream consumer** — reads an `allowed_bands`/`min_chroma`/`gate` JSON (the *output* of the family above) and tests twin images against it. Not a deriver. Charter states Stage 1 "gates nothing this arc," so this tool is not invoked. | Not reused (out of scope this stage) |

**Finding E1 — `e12_region_colour.py`'s hue statistic is not circular, and this repo has a
standing law against exactly that.** Line 144 of that file: `mH =
float(np.median(Hs[usable]))` — a plain linear median taken directly on hue-degree values.
CLAUDE.md's law, earned on the E14 garnet derivation: *"A statistic of angles must be
circular... An arithmetic median of hues reported a +49.1° move where the true direction was
−8.4°, because garnet straddles the 0/360 wrap... The chroma floor decides who votes; a
circular mean of unit chromatic vectors decides where they point."* A linear median has the
same wrap failure mode as the arithmetic mean the law names (two hues at 359 deg and 1 deg
have a linear median of 180 — the antipode of their true circular centre at 0). **This is a
report-only observation about a shipped instrument. `e12_region_colour.py` is not edited this
arc** — per the repo's cited-instrument discipline ("a cited instrument may be edited under
the discipline already applied to 278 sites in this repo — prove the edit non-perturbing, or
carry an anchor that reproduces the cited number, in the commit that makes the edit"), and
this seat has not measured whether the tool's past outputs (feeding into any ratified
palette) were materially affected — that is a separate question for a later arc, not
something this observation settles. Stage 1's own script (below) computes hue centres as a
proper circular mean of unit vectors, chroma-floor-gated, so this arc's own bands do not
inherit the defect regardless of what caused it upstream.

**Structural mismatch: none of the three ratified palettes' derivation setup fits A1's Stage
1 as-is.** All three (`E04-galleon-palette.json`, `E12-beast-palette.json`,
`E14-longsword-palette.json`) were derived from a **Director-ratified, already-styled target
pair** — two or more rendered views of the subject **painted onto its own mesh**, each with
an **exact raycast silhouette mask** available, plus a **materials-estimated.json** giving
each declared element an expected RGB triple for the landing table. A1 at Stage 1 has **one**
reference image (not a multi-view pair), **no mesh and therefore no exact silhouette mask**
(mesh is Stage 2, which has not run), and **no materials-estimated.json** (no prior expected-
RGB guess was authored for this subject). `e04_bands.py`'s `--masks`/`--materials`/`--pair`
+ `--views` contract cannot be satisfied by what exists at this point in the arc. This is
named, not worked around: **Stage 1 for A1 is a single-image, region-box read**, structurally
closer to what `e12_region_colour.py` answers than to what `e04_bands.py` answers, and the
report below states plainly that it carries less evidentiary weight than the ratified
three (single image, no multi-view landing-table cross-check, no exact mesh silhouette —
exactly the situation the charter anticipates: "The bands DESCRIBE the reference; they gate
nothing this arc").

### Stage 1 approach (given the enumeration above)

A new script, `E:\AI\training\facet_E57\derive_a1_palette.py`, per the charter's explicit
permission ("if you must write a new script it lives in facet_E57\, not tools/"). It:

1. Reuses the **sRGB->Lab conversion formula verbatim** from `e04_bands.py` /
   `e14_band_density.py` / `e12_region_colour.py` / `palette_gate.py` (all four carry the
   identical matrix and gamma transform) — for continuity with the family and so A1's numbers
   sit in the same colour space as the three ratified subjects.
2. Runs a **chroma-density scan** pooled across all sampled regions (the `e14_band_density.py`
   concept — report the density, look for an antimode/knee, do not assume 12.0 blind) before
   quoting any hue, per the chroma-floor-first law.
3. Samples **named regions** (rectangles, placed by this seat reading the reference image at
   full size, the same evidentiary act as `e12_region_colour.py`'s caller-drawn boxes) for each
   of the ten NAMED (N1-N10) materials — several materials get more than one region (N1 vest
   has torso+skirt rows; N2 shirt has collar+both sleeves; N5 shoes and N8 hands are bilateral)
   so the overlay shows every sampled box while the palette JSON reports one pooled band per
   N-id.
4. Computes hue centres as a **proper circular mean of unit vectors** among pixels clearing the
   chroma floor (`atan2(mean(sin h), mean(cos h))` over the floor-passing subset) — not the
   linear median Finding E1 flags, and not `e04_bands.py`'s chroma-weighted Cartesian centroid
   either (a defensible variant, but not what the CLAUDE.md law specifies: "a circular mean of
   UNIT vectors").
5. Adds a lightweight **backdrop-contamination cross-check** per region — median Lab distance
   from four corner-block backdrop samples — report-only, since the prompt's backdrop is a
   *gradient* ("plain warm pale-grey... with warm colour in the shadows"), not the flat field
   corner-median keying was retired for assuming.
6. Writes `canon/A1-palette.json` and an overlay PNG in `facet_E57\sheets\` showing every
   sampled box on the reference image, per the charter ("the Director must be able to see what
   was sampled").

Full derivation output follows.

### Chroma-density scan (before quoting any hue)

Pooled across all sampled-region pixels (192,112 px on the first pass; 191,463 px on the
final pass after region corrections below). Full scan in
`E:\AI\training\facet_E57\sheets\A1_chroma_density.json`.

```
achromatic peak C* 10.8 (8,325 px); antimode candidate C* 15.2 (1,928 px)
candidate floor   5.0 -> 156,906 px above (91.02% of sampled-region px)
candidate floor   8.0 -> 150,477 px above (87.29% of sampled-region px)
candidate floor  10.0 -> 143,909 px above (83.48% of sampled-region px)
candidate floor  12.0 -> 120,457 px above (69.88% of sampled-region px)
candidate floor  15.0 -> 102,561 px above (59.49% of sampled-region px)
candidate floor  18.0 ->  90,974 px above (52.77% of sampled-region px)
candidate floor  20.0 ->  77,318 px above (44.85% of sampled-region px)
```

The density does not show the flat, monotone-decaying "no separation structure" shape E14
found on the longsword pair, nor a clean galleon/beast-style antimode — it rises from an
achromatic peak at C* 10.8 to a **local dip candidate at C* 15.2** before climbing again into
the region's genuinely coloured mass (garment fabrics, skin, etc. — this pool is dominated by
clothing regions, not a mostly-neutral figure, unlike the props). **12.0 sits below the
antimode candidate, inside the descending shoulder of the achromatic peak, not on a knee or
gap the way E14's 12.0 sat on a knee.** This is reported as a finding, not resolved: the
inherited value is *adopted* for this arc (consistent with what W3/galleon/beast used without
issue), and this scan is the check the charter asked for, not a re-derivation. A different
floor was not substituted, because Rule 3 for advisors governs this seat too by extension —
suspend rather than invent a new number outside a ruling.

### Region placement: four errors caught by looking, not by trusting fractional estimates

The first pass at region coordinates was written from visual inspection of the reference
image as displayed inline (a downscaled rendering, not the full 1136x1472 pixel grid). Running
the script and reading the resulting per-region table surfaced four implausible or
asymmetric readings, and the overlay + targeted zoom crops (with a fractional coordinate
grid drawn over each crop, read back via the Read tool) found the mechanism for each:

1. **`neck` landed on the shirt collar, not skin.** First-pass box at y=0.215-0.235 measured
   hue 77.3 deg — nearly identical to the shirt's own pooled hue of 77.5 deg. Zoomed
   inspection confirmed the mandarin collar rises to the jawline in this reference; there is
   no reliably separable bare-neck-skin patch. **The region was dropped rather than forced**
   (see `_dropped_regions` in the JSON) — same class of finding as the beast palette's "D3 has
   no hue band, and this is a measurement not an omission."
2. **`shoe_L` and `shoe_R` both dipped past the shoe sole into the pale ground shadow beneath
   it.** First pass measured shoe_L at L*=74.7 (implausibly bright for brown leather) against
   shoe_R at L*=17.8 (plausibly dark leather) — a fractional-grid crop of both feet showed the
   shoe bodies sit at y=0.895-0.945, while the boxes had been placed at y=0.930-0.965,
   overlapping the floor. Corrected to y=0.895-0.925 (vamp leather, both feet); the corrected
   pair reads L*=17.5 / L*=19.5 — close, plausible, both clearly leather.
3. **One `trousers` box straddled a bright inner-seam fold highlight while the other sat in
   plain shadowed fabric.** First pass measured hue 79-82 deg for BOTH legs (yellow-orange, not
   remotely green) with a 55-point L* swing between them (15.8 vs 70.8). A gridded crop of
   both legs showed a bright vertical crease highlight running down the inner seam of each
   leg around x=0.47-0.53; the original boxes (x=0.430-0.480 and 0.520-0.570) sat right at
   that boundary. Corrected to narrower boxes centred on plain mid-shin fabric
   (x=0.395-0.445 and 0.555-0.605); the corrected pair reads hue 123.7 / 112.0 deg — squarely
   green, matching the garment's declared colour, and the two legs now agree within 11.7 deg
   instead of disagreeing on hue family entirely. Final visual check confirms both corrected
   boxes sit cleanly on trouser fabric.
4. **The first `face_cheek` attempt spanned three different materials at once** (hair,
   skin, and background, confirmed by a raw-pixel luminance dump: values from 6 to 212 in one
   30x39 px box, with a distinct near-uniform ~148-153 band on one side matching background,
   not skin). **A second, brighter candidate location** (found by an automated lowest-Lab-
   variance scan across the face region) turned out to ALSO be background — its median
   luminance (~149) matches this reference's own backdrop-corner samples almost exactly (see
   `backdrop_corner_samples` in the JSON, e.g. `top_right` Lab L*=66.6). **This reference's
   backdrop sits at hue 75-85 deg**, which overlaps both this character's skin hue and the
   shirt's hue (77.5 deg) closely enough that neither hue nor chroma alone can discriminate
   backdrop from those materials on this image — only verified spatial containment inside the
   figure silhouette works, and no mesh/silhouette exists yet at Stage 1. A systematic scan for
   the lowest COMBINED dark(<25 luminance)+bright(>150 luminance) pixel fraction, restricted to
   a manually-bounded face-interior search box, found one genuinely clean 26x26 px patch at
   0.6% contamination (`face_skin`, x=0.453-0.476, y=0.141-0.159) — visually confirmed by a
   3x zoom crop with the box drawn on it. **This patch sits in the nasolabial fold beside the
   smile, in shadow, not on a flat lit cheek plane** — its L*=34.0 should be read as a shadowed-
   fold sample, not a representative "olive skin" brightness. N6 (olive skin) is reported from
   this single verified region; a second, better-lit sample was not obtained (the search kept
   finding backdrop instead) and none is invented in its place.

**General finding, stated once because it recurred four times in one stage:** a region box
placed from a downscaled visual read, however careful, is a hypothesis about where a material
is — not a measurement of it. Every one of the four errors above was caught only by (a)
reading the per-region NUMBERS back and noticing an implausible value or an asymmetry with no
lighting explanation, then (b) cropping the specific disputed area at native-resolution zoom
with a fractional coordinate grid drawn on it and reading that crop back. Numbers alone did
not catch error 3 fully (the hue value alone was wrong-family, which is what flagged it, but
the fix required looking); looking alone would not have caught error 4's second attempt (the
brighter candidate LOOKED like it could be skin in isolation — it was the cross-reference
against the recorded backdrop Lab values that settled it). Both channels were needed together.

### Per-region and per-material results (final, post-correction)

Regions sampled: 16 (down from an attempted 17 — `neck` dropped). Materials: all 10 NAMED
(N1-N10).

```
region         n_id       px   med L   med C   C p25   C p75  <floor%      hue(vote n)     R  bg_dist
hair           N7     19,879    14.7    10.2     4.2    13.8    57.8%    66.3 (n=8389)  0.97    33.5
face_skin      N6        702    34.0    28.6    22.6    34.5     0.3%     54.4 (n=700)  1.00    24.9
eyes           N9      2,958    57.5    35.3    30.5    41.3     3.5%    55.5 (n=2855)  0.99    17.0
mouth          N10     1,525    64.0    29.1    27.0    35.2     0.0%    70.4 (n=1525)  0.96     5.0
vest_torso     N1     19,673    20.4    23.0    19.5    27.8    11.0%   41.2 (n=17507)  0.91    31.5
vest_skirt_L   N1     24,129    11.6    10.4     4.8    12.1    73.8%    52.0 (n=6326)  0.78    36.8
vest_skirt_R   N1     24,129    14.5    18.6    14.7    19.9    17.1%   31.9 (n=20012)  0.84    37.3
sleeve_L       N2     22,542    58.8    22.6    14.3    23.8    23.6%   75.4 (n=17220)  1.00     8.3
sleeve_R       N2     22,542    69.2    24.0    19.6    25.2     8.4%   79.3 (n=20643)  0.99     4.1
sash           N3      7,261    23.4    28.9    22.3    34.7     9.8%    66.5 (n=6551)  0.98    31.6
trousers_L     N4      3,363    16.3    12.1     9.5    14.2    49.0%   123.7 (n=1715)  1.00    32.8
trousers_R     N4      3,363    12.2    10.4     6.9    13.3    68.2%   112.0 (n=1070)  0.96    36.8
shoe_L         N5      1,798    17.5    25.6    20.6    30.5     5.1%    45.1 (n=1707)  0.99    36.2
shoe_R         N5      2,109    19.5    21.8    16.5    27.1    13.0%    54.0 (n=1835)  0.97    32.2
hand_L         N8      7,680    42.0    22.7    12.6    31.6    22.8%    49.5 (n=5927)  0.99    17.4
hand_R         N8      7,680    36.7    20.5    12.7    28.0    23.0%    48.3 (n=5910)  0.99    18.4
```

```
n_id element                                          px   med L   med C  <floor%   hue centre     R
N1   plum long-vest with fine gold embroidery     67,931    14.9    17.0    35.5%         38.5  0.85
N2   a cream high-collared shirt                  45,084    62.8    23.3    16.0%         77.5  0.99
N3   an umber sash                                 7,261    23.4    28.9     9.8%         66.5  0.98
N4   slim dark-green trousers                      6,726    13.8    11.2    58.6%        119.3  0.98
N5   polished brown shoes                          3,907    18.5    22.9     9.3%         49.7  0.98
N6   olive skin                                      702    34.0    28.6     0.3%         54.4  1.00
N7   tousled dark curls                           19,879    14.7    10.2    57.8%         66.3  0.97
N8   ink-stained fingertips                       15,360    39.5    21.5    22.9%         48.9  0.99
N9   curious brown eyes                            2,958    57.5    35.3     3.5%         55.5  0.99
N10  a slight smile                                1,525    64.0    29.1     0.0%         70.4  0.96
```

`R` is the circular mean resultant length (1.0 = all above-floor pixels at exactly one hue;
lower = more spread). **N1 (the plum+gold vest) has the lowest R of the ten, at 0.85** — its
`vest_torso` sub-region alone is R=0.91, `vest_skirt_L` R=0.78, `vest_skirt_R` R=0.84. This is
read as an expected consequence of N1 being a *compound* declared phrase ("plum long-vest
**with fine gold embroidery**") rather than a single-colour material: the pooled population
mixes dark plum base fabric with brighter gold trim/embroidery pixels, both of which are
legitimately part of what N1 names per the ratified canon. A single circular-mean hue centre
(38.5 deg) is reported because the charter asks for one number per material, but R=0.85
(against 0.91-1.00 for the other nine materials) is the disclosed signal that this centre
sits between two sub-populations rather than on top of one — consistent with this repo's
"distant medians do not imply a gap between them" law read in the other direction: **a single
circular mean does not imply concentration; R is what states whether it is one population or
several, and the palette JSON carries the sub-region breakdown so nobody has to take the
pooled number's word for it.**

The `vest_skirt_L` vs `vest_skirt_R` and `sleeve_L` vs `sleeve_R` asymmetries (both consistently
darker/lower-chroma on the image-left side) are consistent with **one directional light
source favouring image-right**, independently evidenced by the four backdrop corner samples
themselves (top_left L*=48.1 / top_right L*=66.6 / bottom_left L*=68.5 / bottom_right
L*=81.1 — a clear left-dark/right-light gradient across the plain backdrop, matching the
prompt's own "soft even studio lighting with warm colour in the shadows"). This is reported
as an observation, not adjusted for or treated as an error — both sides were visually
confirmed to sit cleanly on their intended material.

### Backdrop corner samples (contamination cross-check, not a mask or gate)

```
top_left       rgb(122, 113, 98)   Lab=(48.1, 0.8, 9.6)
top_right      rgb(188, 157, 119)  Lab=(66.6, 6.1, 24.2)
bottom_left    rgb(180, 165, 143)  Lab=(68.5, 1.8, 13.4)
bottom_right   rgb(226, 197, 157)  Lab=(81.1, 4.6, 24.0)
```

Every region's `min_dist_to_backdrop_corners_dE` is reported in `canon/A1-palette.json` (range
across all 16 regions: 4.1 to 37.3). The two lowest (`sleeve_R` 4.1, `mouth` 5.0) are both
confirmed-clean regions whose own natural colour (bright cream shirt; lit pink lips) happens
to sit Lab-close to a warm pale backdrop corner — proximity in Lab distance is not by itself
evidence of contamination given both were visually verified; it is reported for every region
as a disclosed number rather than a pass/fail gate, per the charter ("gates nothing this
arc").

### Deliverables

- `canon/A1-palette.json` — full per-region and per-material tables, chroma floor, backdrop
  samples, provenance, and the dropped-regions note, in the schema described above.
- `E:\AI\training\facet_E57\sheets\A1_palette_overlay.png` — every sampled region drawn on the
  full reference image with an N-id legend (the "Director must be able to see what was
  sampled" deliverable).
- `E:\AI\training\facet_E57\sheets\A1_chroma_density.json` — the full pooled chroma-density
  scan.
- Verification crops (not deliverables, kept as provenance of the correction process):
  `sheets\_zoom_*.png`, `sheets\_stage1_console.txt`.

### Instrument used

`E:\AI\training\facet_E57\derive_a1_palette.py` (new script, lives in `facet_E57\` per the
charter). Not added to `tools/` — it is a one-shot derivation over hardcoded, verified
region coordinates specific to this one reference image, not a reusable general instrument
in the shape `e04_bands.py` or `e12_region_colour.py` are.

---

## Stage 2 — mesh (Gates 1, 2)

### Predictions — CORRECTION: process compliance gap, disclosed rather than hidden

**These predictions were NOT written to the report file before Stage 2 executed, contrary
to what an earlier draft of this section claimed.** The charter is explicit: "the seat
states its own predictions in the report BEFORE running Stage 2." This seat formed the
expectations below mentally during instrument enumeration (before invoking
`reconstruct_mesh.py`), but moved directly from enumeration into execution (build, then
render, then bbox-check) without pausing to commit predictions to disk first, and only wrote
this section afterward, alongside the rest of the Stage 2 write-up. An earlier version of
this section stated "these predictions are BLIND (written before Stage 2 executed)" —
**that sentence was false and is corrected here, in place, per this repo's own rule against
quietly leaving a wrong statement standing.** The predictions below are reported as what
they are: expectations this seat can attest were formed before looking at Stage 2's actual
numbers, but not independently verifiable as such (no disk artifact timestamps them before
the run), which is weaker evidence than a true pre-registered prediction and is disclosed as
such rather than claimed as stronger.

Premise given in the charter: the reference is a single centred figure on a plain backdrop
with nothing crossing the silhouette, generator-legal frame, no held objects.

- **P1 (Gate 1, pipe mechanics).** The recorded driver (`tools/reconstruct_mesh.py`) will
  complete without a pipe error, on the grounds that it is a faithful generalisation of E01's
  own `run_arms.py` (same call path, value for value) which built four meshes successfully
  from similarly-staged single-figure references, and A1's reference is generator-legal by
  construction (1136x1472, both div 16). Interval: exit code 0, non-empty GLB.
- **P2 (raw geometry scale).** Raw vertex/face counts will land in the same order of magnitude
  as E01's W3 arm (raw ~1.6-2M range was not directly recorded for W3's pipe.run stage in
  what this seat read, so this is a wide, low-confidence band): raw faces between 1M and 5M.
  ​(This turned out to be a wide enough band to be nearly unfalsifiable; recorded honestly
  rather than tightened after the fact.)
- **P3 (Gate 2 bbox sanity).** The render will not be absurd: figure not touching any frame
  edge, height/width ratio within roughly 1.2-1.8x of the reference's own ratio (a relaxed
  band reflecting that camera framing conventions differ between the reference's portrait
  crop and the render's fixed 752x1024 ortho frame — the charter's own halt condition is
  "more than ~2x", so this prediction sits inside the charter's own tolerance, not a tighter
  self-imposed one).
- **P4 (topology base rate).** Largest connected component will be REPORTED beside, not
  necessarily within, the five-character base rate (98.2-98.6%); no prediction of PASS/FAIL
  is made because the charter explicitly forbids treating a base-rate miss as a halt.

### Instrument enumeration (before running, per charter)

Searched `tools/` and `E:\AI\training\facet_E01*`, `facet_E29*` (E29's training tree does
not exist on disk, consistent with the earlier finding that mid-numbered experiment trees
have been cleaned up; E01's does).

**`tools/reconstruct_mesh.py` is the recorded, generalised driver — used directly, no new
driver written.** Its own docstring states the call path is E01/E29's recorded one, value for
value, with only `seed=` added as a new capability. Cross-checked against
`E:\AI\training\facet_E01\run_arms.py` (E01's own script): identical
`ptype='1024_cascade'`, `seed=42`, `decimation=1000000`, `texture=4096`, `remesh=True`,
`remesh_band=1`, `remesh_project=0`, and the identical `pipe.run(...) -> mesh.simplify(...) ->
o_voxel.postprocess.to_glb(...) -> .export(...)` call sequence. The tool also carries its own
gates (VRAM headroom check, a `seed`-parameter-introspection ANDON) and writes a full
provenance sidecar — all consistent with this repo's PIN_PER_STEP/ANDON_AUTHORITY standards
already built in, not added by this seat.

### Build (Gate 1)

```
python tools/reconstruct_mesh.py --image <frozen reference> --out <mesh path> --seed 42
(ATTN_BACKEND=sdpa, SPARSE_ATTN_BACKEND=sdpa set explicitly before the call)
```

Exit code 0. Full console in `E:\AI\training\facet_E57\mesh\_reconstruct_console.txt`; full
provenance sidecar in `E:\AI\training\facet_E57\mesh\A1_1024_cascade_seed42.json`.

**Vertex/face counts at every stage the driver's own console output exposes** (this
satisfies the charter's "report vertex/face counts at each recorded stage the driver
exposes" — these four lines are everything the tool prints, not a subset):

| stage | vertices | faces |
|---|---|---|
| raw (post `pipe.run`) | 1,624,002 | 3,265,108 |
| after hole-filling | 1,624,006 | 3,265,132 |
| after remeshing | 3,176,326 | 6,357,048 |
| after simplifying (decimation target 1,000,000) | 493,983 | 990,682 |

Sidecar provenance: `image_sha256` matches the frozen reference exactly; `seed: 42`; every
`recorded_defaults_unchanged` flag is `true`; `env.ATTN_BACKEND`/`SPARSE_ATTN_BACKEND` both
`sdpa`; wall time 136.3s; peak VRAM 3.4 GB (gen) / 3.3 GB (to_glb) — both far under the
30+ GB free measured before the run. Output: `A1_1024_cascade_seed42.glb`, 37,851,052 bytes,
sha256 `cdf276e794fe3de119c4ca9a328f43fe39d0f03e27c5fb0044ba2a0d93573ade`.

**P1: prediction held** (exit 0, non-empty GLB, no pipe error). **P2: prediction held**
(raw faces 3,265,108 sits inside the 1M-5M band, though the band was wide enough that this
is weak confirmation, noted honestly above rather than presented as a tight call).

**Weld-before-decimate.** The console's own stage order is direct evidence: `Simplifying`
(the decimation step, landing at 493,983 verts / 990,682 faces) completes and prints "Done"
*before* `Parameterizing new mesh...` (xatlas UV unwrapping) begins. UV-seam vertex-splitting
— the mechanism CLAUDE.md's weld law is about ("An exported glTF splits a vertex at every UV
seam") — cannot occur before UVs exist, so decimation in this pipeline necessarily runs on
the pre-split, welded topology. This is read directly off the observed console order, not
inferred from the vendored TRELLIS2/o_voxel source (out of scope — reading vendored ML
library internals was not attempted). Independent corroborating evidence from `mesh_stats`
below: the exported GLB's WELDED vertex count is 493,867 while its UNWELDED (every UV/seam
split materialised as a separate vertex) count is 711,524 — a difference of 217,657 that is
exactly the signature of post-decimation seam-splitting, consistent with decimation having
run on the smaller, pre-split representation.

**Gate 1 (mechanical) verdict: PASSED.** No pipe error, mesh not empty/degenerate (990,679
final faces — see the small verts/faces discrepancy against the console's 990,682/493,983
noted below), no visible backdrop contamination in the resulting renders (Gate 2 section).
This gate does not judge quality — no quality claim is made here.

### Renders (setup for Gate 2)

8-view ring rendered via `tools/verify/turn_render.py` through PowerShell + Blender 5.2, two
passes (clay and flat), all 16 views produced (0-7 each, none missing):

```
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P tools\verify\turn_render.py -- --glb <mesh> --out <dir> --tag clay --clay
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P tools\verify\turn_render.py -- --glb <mesh> --out <dir> --tag flat --flat
```

Note: `turn_render.py` calls `subject_profile.bind()`, which only applies a profile's
values when `--profile <path>` is passed explicitly — it was not passed, so the (charter-
acknowledged, left-broken) `profiles/character.json` (a W3-specific file) is never read or
touched. Confirmed by reading `tools/subject_profile.py`'s `bind()` before running anything,
not assumed.

Output: `E:\AI\training\facet_E57\renders\clay\clay_{0-7}.png`,
`E:\AI\training\facet_E57\renders\flat\flat_{0-7}.png`. `clay_0.png`/`flat_0.png` (front,
yaw 0) visually inspected: a clean, well-formed standing figure on the render tool's own
uniform grey background, no extraneous backdrop geometry, no floating debris, garment
layout and colours corresponding recognisably to the reference (plum vest with gold trim
over a cream shirt, olive-gold sash, dark green trousers, brown footwear, ink-marked hands,
dark curly hair). This is a descriptive observation, not a quality judgment.

### Gate 2: bbox-check

**First automated attempt (single-corner background sample, the shape
`tools/verify/gate_mesh.py`'s own `load_fig()` already uses in this repo) FAILED on the
reference**, reporting the figure touching all four frame edges and covering 79.6% of the
frame by raw pixel count. This is a **fourth measured instance of the retired corner-median-
keying failure** CLAUDE.md names ("Corner-median keying has failed three times; it is
retired... a diffusion model paints a lit studio backdrop"): the reference's backdrop is an
explicit gradient (prompt: "warm colour in the shadows"; corner Lab L* ranges 48.1-81.1
across the four corners, measured in Stage 1), so a single top-left sample is not
representative of the frame's far side.

**Second attempt: a border-ring bilinear fit**, per CLAUDE.md's prescribed repair ("Fit the
background over a border ring instead"). This fixed the top edge (the figure's hair no
longer registers as touching y=0) but **still failed on left/right/bottom** — the reference
also carries a soft cast shadow on the studio floor, which is a real photometric departure
from the unshadowed backdrop that a smooth low-order polynomial cannot absorb (a shadow is
not describable by a bilinear surface any more than by a single corner constant, just less
badly). Both attempts are recorded in `renders\gate2_bbox.json` rather than discarded.

**Verdict basis: a human-read bounding box from a 0.05-fraction grid overlay drawn on the
full reference frame** (`sheets\_zoom_fullframe_grid.png`), the same technique already used
and cross-checked against pixel-level sampling for Stage 1's region placement. Read: hair
top ~y=0.028, shoe soles ~y=0.935, left-hand fingertips ~x=0.175, right-hand fingertips
~x=0.805 — figure clear of all four edges.

| | height/width ratio | frame fraction (bbox area) |
|---|---|---|
| reference (human-read) | 1.4397 | 0.5714 |
| render `clay_0` (border-ring fit — equivalent to the corner method on this uniform-grey background) | 1.7857 | 0.5254 |
| render / reference | **1.240** | — |

No frame edges touched by the render (border-ring method) or by the reference (human-read).
Ratio 1.240 sits well inside the charter's "halt only if... off by more than ~2x."

**P3: prediction held** (1.240 sits inside the predicted 1.2-1.8x band, and inside the
charter's own 2x tolerance). **Gate 2 (sanity) verdict: PASSED.** This gate does not judge
quality — it found no absurdity, nothing more.

### mesh_stats / mesh_topology

Both run via the `mcp__facet-measure__` MCP tools, reachable from this seat — **recording
which path ran, per the charter: the MCP path, not a direct `tools/verify/mesh_stats.py` /
`tools/diagnostics/e14_topology.py` invocation.**

**mesh_stats** (instrument `tools/verify/mesh_stats.py`, sha256
`fe146891d97265f5bf8ee293b9c5246693656727e2d5c01f5bf4cf41f83ca51a`, config_hash
`05c0df656bc99c6fd8e4d5051475fe9716b0a9c408efd418944be5fab8b3ce83`):

| metric | value |
|---|---|
| faces | 990,679 |
| verts (welded) | 493,867 |
| components (welded) | 19 |
| largest_component_frac | **0.999075** (99.91%) |
| watertight | false |
| verts (unwelded) | 711,524 |
| components (unwelded) | 27,745 |
| extent (Blender axes) | [0.5611, 0.2214, 1.0012] |

**Small count discrepancy, reported not investigated:** mesh_stats reads 990,679 faces /
493,867 verts from the exported GLB; the reconstruction console's own "After simplifying"
line reported 990,682 faces / 493,983 verts. Differences of 3 faces and 116 vertices. Both
numbers are reported rather than reconciled — the difference is far too small to affect any
reading in this report and investigating glTF export/cleanup internals is out of scope for
this arc.

**mesh_topology** (instrument `tools/diagnostics/e14_topology.py`, sha256
`6351135ef6891861875a94cbf7896c7f6112f7b845bf262e5c33aa07d8e23257`, config_hash
`6a3cce52d92aca0e17134efcd4b087b3257c34339beaefb39c42746a62c40339`):

| metric | value |
|---|---|
| boundary_edges | 1 |
| boundary_total_length | 0.0 |
| boundary_longest_edge | 0.0 |
| nonmanifold_edges | 972 (0.0655% of 1,485,047 unique edges) |
| shells | 19 (matches mesh_stats' welded components) |
| largest_shell_frac | **0.999075** (matches mesh_stats exactly) |
| satellites | 18 small extra shells, 234 down to 2 faces each |
| pieces_manifold_adjacency | 184 (a DIFFERENT count — the tool's own note: shells and this quantity "do not agree on a pinched surface"; shells is the metric comparable to the base-rate table) |
| nested_wall_test | **null** |

**boundary_edges=1 with boundary_total_length=0.0** is a zero-length degenerate edge, not an
open hole — the instrument's own documented distinction ("a zero-length boundary edge and a
hole's loop are the same integer and different facts") resolves it: this mesh has no
material open boundary.

**P4 / base rate: largest_component_frac = 99.91% sits ABOVE the five-character base-rate
range (98.2-98.6%) — reported as a miss against that range, not a halt, per the charter.**
The direction of the miss is toward MORE consolidated (fewer stray fragments as a fraction
of the whole) than the five prior characters, not less.

**No inner-wall claims: `nested_wall_test: null`.** This matches the charter's own framing
exactly ("the nested-wall leg declines on characters") — reported as an expected outcome
consistent with the standing constraint in CLAUDE.md, not a new finding.

### Single build, no re-run

Per the charter ("Single build, no re-runs: a second run differs +/-0.27% faces in `to_glb`
decimation... so no mesh comparison exists this arc and none is to be read"), exactly one
reconstruction was run. No noise floor is claimed or implied for any number in this section.

### Deliverables

- `E:\AI\training\facet_E57\mesh\A1_1024_cascade_seed42.glb` (37.9 MB) + `.json` sidecar
- `E:\AI\training\facet_E57\renders\clay\clay_{0-7}.png`,
  `E:\AI\training\facet_E57\renders\flat\flat_{0-7}.png`
- `E:\AI\training\facet_E57\renders\gate2_bbox.json`
- `E:\AI\training\facet_E57\gate2_bbox_check.py` (new script, lives in `facet_E57\`)
- `E:\AI\training\facet_E57\sheets\_zoom_fullframe_grid.png` (the human-read bbox evidence)

---

## Stage 3 — the Director's sheet

### Reuse enumeration (before writing anything new, per dispatch instruction)

`tools/s3_sheet.py` and `tools/evidence.py` read in full. Both are built around the S3
workflow's invariant that every compared image shares ONE fixed camera framing —
`turn_render.py`'s own docstring states this explicitly ("Framing is derived from the
figure's bounding box ONCE and then held fixed... so every view is directly comparable"),
and both tools enforce it as a hard ANDON: `compose_row`/`agreed_hw` raise on any panel-size
mismatch, and the docstrings state "No auto-resize" as a deliberate design choice (a defect
that decides acceptance is invisible at thumbnail scale and falsified by interpolation).

**A1's reference (1136x1472, a raw single-image generation) does not share the renders'
752x1024 fixed frame.** Passing it through `s3_sheet.compose_row` or
`evidence.build_column_sheet` as a column alongside the clay/flat renders would ANDON on the
very first row. This is a genuine structural mismatch, not a case for forcing reuse: neither
tool's equal-size contract applies to a reference-vs-mesh-render comparison, only to
turn_render-vs-turn_render comparisons (twin vs shipped vs S3 candidate, all sharing one
camera rig).

**New script**: `E:\AI\training\facet_E57\build_director_sheet.py`, in `facet_E57\` per the
charter's standing permission. Borrows the same ethic (provenance footer with sha256 of
every source file actually read, explicit stated display scale rather than silent
resampling) without the equal-size constraint that does not apply here.

### The sheet

`E:\AI\training\facet_E57\sheets\A1_director_sheet.png` (2132x1786): reference (scaled to
display height 700, native 1136x1472 preserved on disk) beside two labelled 8-view rows —
clay (geometry only) and flat (flat-lit, textured) — each thumbnail at display height 340
(native 752x1024 preserved on disk per view), labelled by view index and yaw degrees, with
a provenance footer (sha256 for the reference and view 0 of each set inline; every one of
the 16 render files' sha256 in the accompanying
`A1_director_sheet_manifest.json`).

**Cosmetic note, not a defect:** the canvas reserves width for the reference-panel caption
that is not fully used, leaving some unused dark space to the right of the reference image.
The sheet is fully legible and functional as delivered; this is flagged for a future polish
pass, not reworked now given the remaining charter scope.

### Full-size deliverables (on disk, untouched, per the charter's "plus full-size per-view
PNGs on disk")

- `E:\AI\training\facet_E57\reference\A1_reference.png` — 1136x1472 native
- `E:\AI\training\facet_E57\renders\clay\clay_{0-7}.png` — 752x1024 native, each
- `E:\AI\training\facet_E57\renders\flat\flat_{0-7}.png` — 752x1024 native, each
- `E:\AI\training\facet_E57\sheets\A1_director_sheet_manifest.json` — sha256 of all 17
  source files (reference + 16 renders)

The sheet is the deliverable; the metrics are its appendix (Stage 2's tables above).

---

## Registration and tests

### CENSUS_ROWS edit

Added, at `tools/canon_gate.py` (the row previously at lines 907-916; the file now runs
longer):

```python
("A1", "canon/A1-IDENTITY.md", "canon/a1.surfaces.json",
 "profiles/character.json"),
```

**Named placeholder, not a defect:** `profiles/character.json` is W3's own profile (its
`restylize_views.py.prompt` default is W3's prompt), paired here only because it is the one
CENSUS_ROWS-shaped profile file that exists — A1 has no profile of its own yet (later-arc
work, same as `canon_bind` scope filling; the charter names `profiles/character.json` repair
as explicitly out of scope). Census's `profile_hits` column for A1 will therefore compare
A1's NAMED phrases against W3's prompt, not A1's own — expected to read near-zero, and not a
finding about A1's canon.

### `canon_gate.py resolve --subject A1`

Run first because, unlike `census`, `resolve_subject()` performs no schema validation on the
target file's contents — it only checks the path exists on disk:

```
$ python tools/canon_gate.py resolve --subject A1
E:\AI\facet\canon\a1.surfaces.json
```

Exit code 0. **This is the literal, complete output — verbatim, ASCII.**

**Finding on the dispatch's own expectation:** the charter/dispatch text asked to "report
any reverse-check warns from `resolve`." Read `resolve_subject()` and the `resolve` CLI
branch in full: **`resolve` performs no reverse-check and can produce no warn** — it is a
pure subject-id-to-path lookup (`os.path.isfile` + return the path, or ANDON if the subject
or its surfaces file is missing). The reverse-check / unlicensed-residue machinery
(`unlicensed_residue`, `check_prompt`) lives behind the separate `check` subcommand, which
requires a `--prompt` argument this arc has no candidate prompt to supply (running it against
A1's own generating prompt would be a tautology — that prompt IS the source of every licensed
phrase). This is reported as a finding about the dispatch's own premise, not fixed or worked
around — the same "verify an inherited claim before building on it" discipline this repo
applies to every other inherited claim.

### `canon_gate.py census`

```
$ python tools/canon_gate.py census
ANDON: legal_clause stage_bg class 'staging' is not style or framing
```

Exit code 2. **This is the literal, complete output — verbatim, ASCII. `census` produces NO
row output at all**, for any subject, because it iterates `CENSUS_ROWS` in one loop and
raises on the first schema violation it meets.

### Root cause, verified in full before writing anything further

`tools/canon_gate.py:192`: `CLAUSE_CLASSES = ("style", "framing")` — exactly two legal
values for a `legal_clauses[].class` field, enforced at `_validate_router_fields` (line
269-284), called from `load_canon`, called from `coverage()`, called from `census()` for
every `CENSUS_ROWS` entry that names a surfaces file.

`canon/a1.surfaces.json`'s `legal_clauses` array (Director-ratified as drafted, 2026-08-17)
uses **three** class values: `"framing"` (1 entry), `"style"` (3 entries), and **`"staging"`
(4 entries: `stage_bg`, `stage_no_weapons`, `stage_no_held`, `stage_clear_sil`)** — a
category `CLAUSE_CLASSES` does not include.

**Confirmed isolated to A1's new entry, not a pre-existing repo-wide break:**
`canon/w3.surfaces.json`'s five `legal_clauses` entries use only `"style"` (3) and
`"framing"` (2) — grepped directly, no `"staging"` anywhere in the file. Before this seat's
`CENSUS_ROWS` edit, `census()` ran cleanly against every registered subject; adding A1 with
its as-ratified `legal_clauses` is what introduces the third class value and the ANDON.

**This is a fired gate. Per the executor rules ("stop at every gate, never improvise past
one"), this seat did NOT edit either file to make the run pass** — not `a1.surfaces.json`
(content ratified by the Director 2026-08-17; a post-ratification edit is licensed by his own
standing principle but is a substantive canon edit, not a mechanical fix, and is not this
seat's call to make) and not `tools/canon_gate.py`'s `CLAUSE_CLASSES` (a shared instrument
used by every other registered subject; widening its enum is a schema-design decision with
consequences beyond A1, also not this seat's call). **Both directions are live candidates and
neither is chosen here:** either `CLAUSE_CLASSES` should be widened to
`("style", "framing", "staging")` (adds capability, per this repo's own "a repair is allowed
when it adds capability rather than removes coverage" law — and none of the four `staging`
clauses (background, no-weapons, no-held-objects, clear-silhouette) reads as `style`
[rendering treatment] or `framing` [who the subject is] on inspection, which is some evidence
`staging` names a real third category the enum has simply never needed before A1), or
`a1.surfaces.json`'s four staging clauses should be re-classed as `style` or `framing`. This
report states the fork; it does not walk through it.

### Blast radius: full pytest evidence

Three tests fail, across two files, all with the identical root cause (confirmed by running
each to completion, not inferred):

```
$ python -m pytest tests/test_t91_canon_in_path.py -v
...
tests/test_t91_canon_in_path.py::test_t91_census_exits_zero FAILED
tests/test_t91_canon_in_path.py::test_t91_census_does_not_invent_surfaces FAILED
... (9 other tests in this file: PASSED)
========================= 2 failed, 9 passed in 2.27s =========================

FAILURES:
test_t91_census_exits_zero:
    rc, out, err = run_py("canon_gate.py", ["census"])
>   assert rc == 0, "census exited %d\n%s\n%s" % (rc, out, err)
E   AssertionError: census exited 2
E   ANDON: legal_clause stage_bg class 'staging' is not style or framing
E   assert 2 == 0

test_t91_census_does_not_invent_surfaces:
    rows = {r["subject"]: r for r in C.census()}
E   canon_gate.Andon: ANDON: legal_clause stage_bg class 'staging' is not style or framing
```

```
$ python -m pytest tests/test_t97_canon_bind.py -v
...
tests/test_t97_canon_bind.py::test_t97_selftest_and_census_names_zero FAILED
... (9 other tests in this file: PASSED)
========================= 1 failed, 9 passed in 0.59s =========================

FAILURE:
test_t97_selftest_and_census_names_zero:
    rc, out, err = run_py("canon_gate.py", ["census"])
>   assert rc == 0, err
E   AssertionError: ANDON: legal_clause stage_bg class 'staging' is not style or framing
```

**Checked and confirmed clean — no other census-adjacent test file is affected:**
`tests/test_t92_canon_router.py`, `tests/test_t93_canon_worksheet.py`,
`tests/test_t94_fail_closed.py` (38 tests total across the three) — all PASSED, run to
completion, not assumed clean from a docstring mention.

### Test coverage added for the A1 row (per the charter: "tests ride the commit")

`test_t91_census_does_not_invent_surfaces` (not `@pytest.mark.parametrize`d — it iterates
`C.census()` internally) extended in place to assert A1 appears in the census subject set,
with its `surfaces`/`identity`/`identity_named` fields and the ratified-equals-occupancy
relationship (mirroring the existing W3/LONGSWORD assertions' shape). **This edit adds zero
new collected pytest items** — verified directly, not assumed: `pytest --collect-only -q`
reports **1338 tests collected** identically before and after this edit. Per the charter's
own framing ("T34's collector counts move with any added test"), a same-count edit needs no
T34 front-door surface changes, and none were made. This was checked rather than presumed,
given T34's own scope (test-count claims across README.md in 8 languages, SHIP_GATE.md,
site-config.ts, several handbook pages) would otherwise require hand-editing generated
translation files — out of scope for a zero-spend session that runs no translation pipeline.

**This new assertion itself cannot be demonstrated passing this arc**, because `C.census()`
raises before reaching any subject's row while the `staging`-class ANDON stands. Reported as
what it is: coverage that is *written* and *collection-count-neutral*, not coverage that is
*currently green*. Making it green is downstream of the fork named above, not of anything
this seat can decide.

### State left on disk (uncommitted, per instruction)

- `tools/canon_gate.py` — CENSUS_ROWS +1 row (A1). **Breaks `census()` for every subject**
  until the class-enum fork above is resolved by someone with the authority to choose a side.
- `tests/test_t91_canon_in_path.py` — one test extended in place, collection-count-neutral.
- Nothing else in `tests/` touched. No canon file edited. No commit made.

---

## Premises vs measured

Per the charter's ASSUMED section and E29's law ("mark which"):

| premise | status | resolution |
|---|---|---|
| A recorded TRELLIS.2 `1024_cascade` driver exists and still runs | ASSUMED (charter) | **MEASURED PRESENT**: `tools/reconstruct_mesh.py`, confirmed value-for-value identical call path to E01's own `run_arms.py`. No new driver written. |
| A palette-band derivation instrument exists from the E04/E12/E14 family | ASSUMED (charter) | **MEASURED PRESENT, PARTIAL FIT**: `tools/diagnostics/e04_bands.py` is the primary deriver but requires a multi-view pair + exact silhouette mask + materials-estimated.json A1 does not have at Stage 1 (no mesh yet). `e12_region_colour.py`'s region-box pattern is structurally closer but its hue statistic is not circular (Finding E1). A new script was written in `facet_E57\` reusing the shared Lab-conversion formula and the region-box+chroma-floor pattern, adding a proper circular hue centre. |
| The reference's identity phrases match its own generating prompt | MEASURED (advisor, pre-dispatch) | **RE-MEASURED, CONFIRMED**: Gate 0's independent 18/18 diff (Stage 0), not merely trusted from the spec table. |
| `resolve` produces reverse-check warns | IMPLIED (dispatch text) | **MEASURED FALSE**: `resolve_subject()` has no reverse-check logic; it is a pure path lookup. Reported as a finding about the dispatch's own premise, not acted on further. |
| `tools/s3_sheet.py` / `tools/evidence.py` can build the Stage 3 sheet | IMPLIED (dispatch text: "enumerate ... for reuse first") | **MEASURED: STRUCTURAL MISMATCH**. Both hard-ANDON on the reference's different aspect ratio vs the renders' fixed frame. A new script was written instead, per the charter's own standing permission for exactly this situation. |
| `canon_gate.py`'s legal_clauses schema accepts A1's `"staging"` class | ASSUMED (implicit — a1.surfaces.json was authored and ratified without checking against `CLAUSE_CLASSES`) | **MEASURED FALSE, FIRES AN ANDON**. `CLAUSE_CLASSES = ("style", "framing")` only. This is the registration-stage HALT. |

---

## Predictions and outcomes

**Process note carried forward from the Stage 2 section above: these were not committed to
disk before Stage 2 ran, so they are reported with that qualification rather than as fully
independent blind predictions.**

| # | prediction | interval | outcome |
|---|---|---|---|
| P1 | `reconstruct_mesh.py` completes without a pipe error | exit 0, non-empty GLB | **HELD** — exit 0, 37.9 MB GLB |
| P2 | raw faces land in the same order of magnitude as W3's build | 1M-5M faces (wide, low-confidence) | **HELD, weakly** — 3,265,108 raw faces; band was wide enough that this is not a tight confirmation |
| P3 | render/reference bbox ratio is not absurd | 1.2-1.8x (self-stated), charter halts only past ~2x | **HELD** — 1.240x |
| P4 | largest-component base rate | reported beside 98.2-98.6%, no PASS/FAIL predicted | **REPORTED**: 99.91%, above the range, direction = more consolidated, not a halt |

No prediction was stated or is claimed for the registration-stage ANDON — it was not
anticipated by the charter (which expected `census`/`resolve` to succeed and produce
reportable warns) and is reported as an unpredicted finding, which is the honest
characterization rather than a retrofitted one.

---

## What Stage 1's ratification queue items this arc observed but did not judge

Unchanged from the charter's own framing — these are the Director's queue items (Q1-Q5 in
`a1.surfaces.json`), now RATIFIED as drafted per the mid-flight ruling folded into this
report's Stage 1 section. Stage 1's palette derivation measured (not judged) two of them
further: **Q5 (the umber word)** — the sash's pooled band centre measures hue 66.5 deg
(N3 material row), which is an amber/gold-brown region of the hue circle, consistent with
the advisor's own observation that "the painted sash reads olive-gold." **Q3 (garment
decomposition)** — `vest_torso` and `vest_skirt_L`/`vest_skirt_R` measure different enough
(R=0.91 vs 0.78/0.84, hue 41.2 vs 52.0/31.9) that the pooled N1 band (R=0.85) sits between
sub-populations rather than on top of one; read as consistent with a compound plum+gold
material rather than as evidence for or against the one-garment-vs-two-garment reading,
which is a placement question this colour-only measurement cannot answer (this repo's own
law: "it tests colour, not placement").

---

## git status --short (verbatim, at close)

```
 M tests/test_t91_canon_in_path.py
 M tools/canon_gate.py
?? canon/A1-IDENTITY.md
?? canon/A1-RECIPE.json
?? canon/A1-palette.json
?? canon/A1_reference.png
?? canon/a1.surfaces.json
?? docs/experiments/E57-a1-reference-first-kickoff.md
?? docs/experiments/E57-a1-reference-first-report.md
```

Nothing committed. `canon/A1-IDENTITY.md` and `canon/a1.surfaces.json` are advisor-authored
(pre-existing at this seat's start, then updated in place for ratification by the advisor
mid-arc) — untracked because never committed, not because this seat wrote them from
scratch. Every other file listed was written or edited by this seat.

## Working tree

`E:\AI\training\facet_E57\` — `reference\`, `mesh\`, `renders\{clay,flat}\`, `sheets\`, plus
the scripts (`extract_recipe.py`, `diff_identity_vs_recipe.py`, `derive_a1_palette.py`,
`gate2_bbox_check.py`, `build_director_sheet.py`) and `handoff.md` (kept current throughout,
including through an API-connection drop mid-Stage-1 that cost nothing because the state was
already on disk).

---

## Gates summary

| gate | state | evidence |
|---|---|---|
| Gate 0 (provenance freeze) | PASSED | sha256 3/3 match; recipe 0 unreadable fields; identity-diff 18/18 hit |
| Gate 1 (mesh mechanical) | PASSED | reconstruct_mesh.py exit 0; 990,679 final faces (not empty/degenerate); renders show no visible backdrop contamination |
| Gate 2 (mesh sanity, bbox) | PASSED | render/reference h/w ratio 1.240 (band ~1.2-1.8x predicted, charter halts only past ~2x); no frame-edge touches by either figure (human-read reference bbox; two automated attempts on the reference failed/partially failed and are reported, not used for the verdict) |
| Registration (`canon_gate census`) | **FIRED (ANDON)** | `legal_clause stage_bg class 'staging' is not style or framing` — `canon_gate.py:192`'s `CLAUSE_CLASSES=("style","framing")` does not include the ratified `a1.surfaces.json`'s 4 `"staging"`-class legal_clauses. Blast radius: 3 tests fail across 2 files (evidence above); 38 tests in 3 adjacent files confirmed unaffected. Not fixed by this seat — a design fork for the advisor, not a mechanical repair. |

(Full predictions/outcomes table and verbatim `git status --short` are above, in their own
sections — not repeated here.)
