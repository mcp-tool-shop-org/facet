# E45 — report: the AOV bundle, and the twin-to-mesh warp measurement

**Written 2026-08-16 by the dispatched executor seat**, after the work, against
`docs/experiments/E45-warp-and-aov-kickoff.md`. Evidence only. This seat does not
decide what any number means; the advisor rules and the Director's eye is the
acceptance gate.

Every number below is attributable to a script on disk. Paths are absolute.

| artifact | path |
|---|---|
| handoff (kept current from before the first measurement) | `E:\AI\training\facet_E45\handoff.md` |
| premise sweep | `E:\AI\training\facet_E45\p0_premises.py` / `p0_premises.json` |
| task 1 predictions (written before the emitter existed) | `E:\AI\training\facet_E45\predictions_task1.md` |
| Gate A matrix | `E:\AI\training\facet_E45\gateA_matrix.py` / `gateA_matrix.json` |
| AOV bundle (8 twin-ring views) | `E:\AI\training\facet_E45\aov\` + `manifest.json`, `cams.json` |
| AOV bundle (2 elevated stroke cameras) | `E:\AI\training\facet_E45\aov_el55\` + `manifest.json`, `state_images.json` |
| task 2 pre-registration + predictions | `E:\AI\training\facet_E45\predictions_task2.md` |
| warp driver | `E:\AI\training\facet_E45\run_warp.py` |
| warp results | `E:\AI\training\facet_E45\warp\warp_report.json`, `warp_arrays.npz` |
| warp analysis | `E:\AI\training\facet_E45\analyse_warp.py` / `warp\warp_analysis.json` |
| sheets | `E:\AI\training\facet_E45\sheets\` (22 files) |
| s3 smoke diagnostic | `E:\AI\training\facet_E45\s3_smoke.py` / `s3_smoke\` |
| new tools (uncommitted) | `E:\AI\facet\tools\emit_view_aovs.py`, `E:\AI\facet\tools\twin_mesh_warp.py` |
| new tests (uncommitted) | `E:\AI\facet\tests\test_t78_emit_view_aovs.py`, `E:\AI\facet\tests\test_t81_twin_mesh_warp.py` |

---

## 0. The two gates, up front

| gate | verdict | evidence |
|---|---|---|
| **Gate A** — the emitter's `sil` against `masks\w3clay_i.png`, at the 8 `cam.json` cameras, compared as pixels | **FIRED, 2 of 8** | 96,024 differing px at `job_y+000_e+55`, 62,116 at `job_y+180_e+55`; 0 on the other six |
| **Gate C** — the warp instrument against constructed truth before any real measurement | **HELD** | 12 invocations, 84 legs; null integer peak wrong on 0 tiles, peak >= 0.999999, every injected shift inside 0.5 px on every in-scope tile |

**The emission the dispatch specified for views 0 and 4 — each `cam.json` camera
carrying `twin_i` — was not performed.** What was emitted instead, and why, is in
section 2.

---

## 1. Premises. Two of the dispatch's four ASSUMED premises are falsified.

The kickoff marks its premises MEASURED or ASSUMED and instructs the seat to verify
the ASSUMED ones. Script: `p0_premises.py`. Output: `p0_premises.json`.

### 1a. The dispatch pairs TWO DIFFERENT CAMERA SETS (the finding Gate A fired on)

`tools/silhouette_masks.py` — the tool that wrote `masks\w3clay_0..7.png` — **has no
elevation parameter at all.** Its ray basis is at :132-136,
`dtc = (sin th, -cos th, 0)`, a pure yaw ring. All eight shipped masks are **el = 0**.

`state\job_y+000_e+55\cam.json` and `job_y+180_e+55\cam.json` say **el = 55.0**.
Those two cameras were written by `tools/texpass_iter.py::emit` through
`basis(yaw_d, el_d)` (:156-164), which does carry elevation.

Measured as pixels, `state\job_*\hit.png` against `masks\w3clay_i.png`:

| job | vs mask | hit px | mask px | differing px | IoU | same sha256 |
|---|---|---|---|---|---|---|
| job_y+000_e+55 | w3clay_0 | 108,166 | 146,356 | **96,024** | 0.452146 | no |
| job_y+045_e+00 | w3clay_1 | 149,780 | 149,780 | 0 | 1.000000 | **yes** |
| job_y+090_e+00 | w3clay_2 | 90,553 | 90,553 | 0 | 1.000000 | **yes** |
| job_y+135_e+00 | w3clay_3 | 120,439 | 120,439 | 0 | 1.000000 | **yes** |
| job_y+180_e+55 | w3clay_4 | 117,176 | 146,356 | **62,116** | 0.618508 | no |
| job_y+225_e+00 | w3clay_5 | 149,780 | 149,780 | 0 | 1.000000 | **yes** |
| job_y+270_e+00 | w3clay_6 | 90,553 | 90,553 | 0 | 1.000000 | **yes** |
| job_y+315_e+00 | w3clay_7 | 120,439 | 120,439 | 0 | 1.000000 | **yes** |

Six of the eight stroke cameras are the twins' cameras and their masks are
byte-identical. Two are not the twins' cameras.

### 1b. Premise A — the twin ↔ yaw mapping. **PINNED**, three independent legs.

1. `twins\w3clay_i_mask.png` is **byte-identical (sha256)** to `masks\w3clay_i.png`
   for all eight i. Two different tools wrote those two directories.
2. `masks\silhouettes.json` maps view i to yaw 45i, with no elevation field, and
   records `anchor_diff_px 0` at views 0 and 4.
3. The six flat `hit.png`s, written by a third tool, reproduce the same index→yaw
   map at 0 differing px.

**`twin_i` is yaw 45i at el 0. No twin exists at el 55**, and the eight twins are
the eight views the Grok brief's input contract requires (`twin` is a mandatory
per-view array there).

### 1c. Premise B — `hit.png` semantics. **SETTLED.**

Raw first-hit raycast mask, undilated (`texpass_iter.py:260`), byte-identical to the
silhouette mask on all six shared cameras.

### 1d. Premise C — **FALSIFIED AS STATED.**

The kickoff assumes `E:\AI\training\facet_E42\check_mesh_match.py` "holds the working
GLB↔state reconciliation." It does not. It compares
`ARMB/export/turnaround/mesh.glb` against `E06/C1/prep/prep_uv.glb` vertex and face
arrays, and on that pair its own first branch reports `same_counts: False` —
400,130 v against 373,462 v, both 287,170 f.

The reconciliation was derived instead from `texpass_iter.py::emit` (:192-266), the
tool that wrote cam.json, and the mesh question was answered directly:

- `W3_final.glb` 400,130 v / 287,170 f; `prep_uv.glb` 373,462 v / 287,170 f.
- **Triangle positions are bit-identical**: `v[f]` compared elementwise, max abs
  diff **0.000e+00**, same face order. The UVs at faces are equal too. The extra
  26,668 vertices are UV-seam splits.
- Canonical `bmid`, `v_ext`, `h_ext` from either mesh match every cam.json to
  **0.000e+00**.

### 1e. Premise D — **REFINED.**

The elevated basis is **not** `bake_hero_fuse.cam_basis(el, az)`. It is
`texpass_iter.basis(yaw, el)`. The two are equivalent under `az = yaw - 90`, but only
the latter is the function that emitted these cameras, and it is the one ported.

---

## 2. Task 1 — the AOV emitter

Tool: `E:\AI\facet\tools\emit_view_aovs.py` v1.0.0 (sha256 in every manifest).
`--selftest` exercises 7 constructions and exits 0.

### 2a. Predictions, then results

`predictions_task1.md` was written after the premise sweep and **before the emitter
existed**. It states what was already measured, so blindness is honest.

| # | prediction | blind? | measured | verdict |
|---|---|---|---|---|
| P1 | Gate A verbatim fires on exactly 2 of 8; 96,024 and 62,116 differing px, 0 elsewhere | **no** (derived from the hit.png comparison) | 96,024 / 62,116 / 0 x 6 | **exact** |
| P2 | every recorded camera reproduces its OWN recorded silhouette at 0 px; confidence 0.70 | **yes** (mesh-soup identity unmeasured when written) | **0 differing px on 16 of 16 cameras** | hit |
| P2 | per-view `sil.sum()` equals silhouettes.json exactly | yes | 146356 / 149780 / 90553 / 120439 x2 | hit |
| P3 | reprojection max error < 1.0e-3 px (band 0-5e-3); dispatch tolerance 0.51 px | yes | worst **1.272e-05 px** over all 16 cameras | hit |
| P4 | surfid valid on > 99.99% of `sil` px | yes | **100.000%** on all 8 views (146,356/146,356 etc.) | hit |
| P5 | join probability ~0.50; the first surprise comes from the mesh-soup clause (a), not the elevated-basis clause (c) | yes | clause (a) held exactly; clause (c) held exactly; **no surprise from either** | the join landed, the reasoning about which clause was riskiest was untested |

Depth-identity residual (analytic `-(P-bmid).dtc` against `t_hit - D`), an in-scope
check on every view: worst **3.886e-16**.

### 2b. Gate A, as written, and the discriminating measurement beside it

`gateA_matrix.py` emits nothing. It casts at every distinct recorded camera and
compares against every recorded silhouette artifact. **No camera parameter is fitted
anywhere; each is read off disk.**

**Gate A as the dispatch wrote it** — the emitter at the 8 `cam.json` cameras, `sil`
against `masks\w3clay_i.png`:

| camera | anchor | differing px | IoU | only-emitted | only-anchor |
|---|---|---|---|---|---|
| camjson_job_y+000_e+55 | masks/w3clay_0.png | **96,024** | 0.452146 | 8,917 | 87,107 |
| camjson_job_y+045_e+00 | masks/w3clay_1.png | 0 | 1.000000 | 0 | 0 |
| camjson_job_y+090_e+00 | masks/w3clay_2.png | 0 | 1.000000 | 0 | 0 |
| camjson_job_y+135_e+00 | masks/w3clay_3.png | 0 | 1.000000 | 0 | 0 |
| camjson_job_y+180_e+55 | masks/w3clay_4.png | **62,116** | 0.618508 | 16,468 | 45,648 |
| camjson_job_y+225_e+00 | masks/w3clay_5.png | 0 | 1.000000 | 0 | 0 |
| camjson_job_y+270_e+00 | masks/w3clay_6.png | 0 | 1.000000 | 0 | 0 |
| camjson_job_y+315_e+00 | masks/w3clay_7.png | 0 | 1.000000 | 0 | 0 |

**VERDICT: FIRED, 2 of 8.** Spatial distribution of the two firing rows — row and
column bboxes and 16-band histograms — is in
`gateA_matrix.json -> gate_a_as_written.differing`, and the difference images are at
`E:\AI\training\facet_E45\diff_camjson_job_y+000_e+55_dispatch.png` and
`diff_camjson_job_y+180_e+55_dispatch.png`. The disagreement is not a rim: it is the
whole upper body, which is what a 55-degree elevation change looks like.

**The discriminating measurement, same pass:** every one of the **16** distinct
recorded cameras reproduces the silhouette artifact **that camera itself produced**,
at **0 differing px, 16 of 16** — the 8 twin-ring cameras against
`masks\w3clay_i.png`, the 6 flat stroke cameras against their own `hit.png`, and
**both el-55 cameras against their own `hit.png`.** The elevated basis is therefore
reproduced exactly against the only elevated silhouettes this route has, which is the
direction the dispatch flagged and which its own Gate A could not test, since no
elevated mask exists in `masks/`.

### 2c. What was emitted, and what was withheld

**Withheld:** the bundle the dispatch specified for views 0 and 4 — an el-55 camera
carrying `twin_0` / `twin_4`. Writing it would have asserted a pairing that the
premise sweep shows does not exist.

**Emitted, `E:\AI\training\facet_E45\aov\` — the 8-view bundle, Gate A live:**
the twin-ring cameras (yaw 45i, el 0), each anchored on `masks\w3clay_i.png` **with
the gate armed inside the emitter**, each returning **0 differing px**, each carrying
its own `twin_i.png`. Six of these eight cameras are bit-identical to the `cam.json`
cameras; the other two are the cameras the dispatch's own Gate A anchor selects.

**Emitted, `E:\AI\training\facet_E45\aov_el55\` — the two elevated stroke cameras**,
anchored on their own `hit.png` (0 differing px each), carrying **no `twin.png`**.
The stroke's own images are copied in as `state_render.png`, `state_inpainted.png`,
`state_mask.png`, `state_thin.png`, `state_hit.png` with sha256s in
`state_images.json`.

Bundle: 244.7 MB, 80 files under `aov/view_*` plus `cams.json` and `manifest.json`.

Per view the bundle carries `depth` (float32, +inf background), `pos` (float32, NaN
background), `normal_world` (float32, NaN background, barycentric-interpolated vertex
normals in the canonical frame), `sil` (bool), `surfid` (int32, `row * 4096 + col`,
-1 background), `weight_border`, `reject`, and `depth_edge` (the last three from
`callieri_border` at `relative_jump = 0.05`), plus `sil.png` and `twin.png`.

| view | yaw | sil px | % frame | surfid unique | front-facing px | depth-edge px | reject in sil | mean weight_border | depth range |
|---|---|---|---|---|---|---|---|---|---|
| view_0 | 0 | 146,356 | 19.006 | 100,250 | 146,130 | 21,745 | 17,700 | 0.3706 | -0.1641..0.1409 |
| view_1 | 45 | 149,780 | 19.451 | 105,023 | 149,518 | 17,667 | 12,610 | 0.4172 | -0.1357..0.1675 |
| view_2 | 90 | 90,553 | 11.759 | 63,137 | 90,305 | 11,102 | 5,421 | 0.4952 | -0.2273..0.2065 |
| view_3 | 135 | 120,439 | 15.640 | 80,129 | 120,101 | 13,552 | 8,872 | 0.3929 | -0.2475..0.2200 |
| view_4 | 180 | 146,356 | 19.006 | 99,001 | 145,993 | 20,148 | 16,509 | 0.4122 | -0.1641..0.1640 |
| view_5 | 225 | 149,780 | 19.451 | 97,648 | 149,412 | 15,342 | 10,180 | 0.4636 | -0.2209..0.1036 |
| view_6 | 270 | 90,553 | 11.759 | 52,824 | 90,345 | 16,051 | 11,402 | 0.3544 | -0.2273..0.2018 |
| view_7 | 315 | 120,439 | 15.640 | 76,521 | 120,175 | 13,989 | 8,628 | 0.3887 | -0.2410..0.2097 |

Identity envelope in `manifest.json`: GLB sha256
`10dddc867b3c743bd958a9cd36312b6c6b96e31825e852551a81629d28f79ce1`, tool sha256,
python 3.13.13, numpy 2.4.6, scipy 1.17.1, PIL 12.2.0, trimesh 4.12.2, **open3d
0.19.0+241aaee**.

### 2d. Tests (T78, uncommitted)

`E:\AI\facet\tests\test_t78_emit_view_aovs.py` — 19 tests, all green.
Renamed from T77 on the advisor's mid-flight steering after Grok Build landed
`tests/test_t77_s3_composite.py` at HEAD.

Legs include: the selftest as a subprocess; basis-vs-`silhouette_masks` agreement
with a can-fail (a one-degree yaw error must not compare equal); **float32 ray-origin
bit-identity between the two constructions** with a can-fail (a 1e-5 perturbation
must break it); the projection contract with a can-fail (a right/up swap); the
reprojection check with a can-fail (a 2% extent error must exceed tolerance);
background sentinels; occlusion; the surfid texel mapping with a can-fail (doubling
the atlas resolution must change the id set); the silhouette gate firing on one
pixel; **the gate firing under `-O` and `PYTHONOPTIMIZE=1`**; and two artifacts-tier
legs that replay a flat recorded camera and **the el-55 camera**, with the anchors'
px counts pinned so a reproduction against a *different* mask cannot pass.

One float detail worth recording: `texpass_iter.basis` and `silhouette_masks`'
construction differ by **exactly the 1e-12 guard epsilon** in float64 (they divide by
`norm + 1e-12` but normalise different vectors). They are bit-identical after the
float32 cast open3d receives, which is the mechanism behind the six byte-identical
`hit.png`/mask pairs, and it is now a test rather than a coincidence.

---

## 3. Task 2 — the twin-to-mesh warp

Tool: `E:\AI\facet\tools\twin_mesh_warp.py` v1.0.0. `--selftest` exercises 7
constructions and exits 0.

**There is no pass condition for task 2 and none was invented.** Distributions,
numerators and denominators separately, controls, and pictures.

### 3a. Pre-registration

`predictions_task2.md` was written after the selftest was green and **before any real
twin was correlated against anything**. Frozen: tile 64, stride 32 (682-tile grid,
31 x 22), radii 16 -> 32 -> 48, blur sigma 1.5, scope floor
`count >= max(8 px, 0.01 x the tile's OWN silhouette area)`, ZNCC with a parabolic
sub-pixel fit, and the sign convention. Both fields are zero-padded by the radius so
the tile grid does not change with the window — a pinning fraction at two radii must
be over the same tiles.

**One disclosure.** A cost probe (`warp_probe_timing.py`, run to bound the arm before
spending it) printed the in-scope count for view 1's silhouette leg — 222 — before
the measurement proper. P7's silhouette band was 90-200, so that band was already
known to have missed high when the measurement ran. No offset was seen.

### 3b. Gate C — HELD

Real twins' edge fields, views 0 and 1, both legs' scope masks, radii 16/32/48 — 12
invocations, each with 1 null leg and 6 injected shifts `(+3,0) (-3,0) (0,+7) (0,-7)
(+12,-5) (-8,+11)`. `gate_c` raises on any miss; reaching the end is the result.

| view | leg | R | in-scope interior tiles | null integer peak wrong | null sub-pixel floor max | null min peak | max inject error |
|---|---|---|---|---|---|---|---|
| 0 | silhouette | 16 | 221 | 0 | 0.2170 px | 1.000000 | 0.2170 px |
| 0 | silhouette | 32 | 209 | 0 | 0.2170 px | 0.999999 | 0.2170 px |
| 0 | silhouette | 48 | 209 | 0 | 0.2170 px | 0.999999 | 0.2170 px |
| 0 | interior | 16 | 220 | 0 | 0.0998 px | 1.000000 | 0.0998 px |
| 0 | interior | 32 | 211 | 0 | 0.0672 px | 0.999999 | 0.0672 px |
| 0 | interior | 48 | 211 | 0 | 0.0672 px | 0.999999 | 0.0672 px |
| 1 | silhouette | 16 | 222 | 0 | 0.1753 px | 1.000000 | 0.1753 px |
| 1 | silhouette | 32 | 210 | 0 | 0.1753 px | 1.000000 | 0.1753 px |
| 1 | silhouette | 48 | 210 | 0 | 0.1753 px | 0.999999 | 0.1753 px |
| 1 | interior | 16 | 206 | 0 | 0.0789 px | 1.000000 | 0.0789 px |
| 1 | interior | 32 | 197 | 0 | 0.0789 px | 0.999999 | 0.0789 px |
| 1 | interior | 48 | 197 | 0 | 0.0789 px | 0.999999 | 0.0789 px |

**A gate of mine fired first and was repaired, and the repair is on the record.** The
first draft set the null tolerance to 1e-9 on the reasoning that a field correlated
against itself has an exactly-zero answer. Run once on the synthetic fixture it FIRED
at **0.018731 px on 35 of 35 tiles**. The integer peak was exactly (0,0) on every
tile and the peak value was 1.0: the residual is the parabolic sub-pixel fit applying
a small correction at the true zero, because a real correlation surface's 3x3
neighbourhood is not symmetric. That is the estimator's own floor, a diagnostic and
not a halt. The repair: the null leg now gates the **integer** peak (exactly zero by
construction) and the peak value, and reuses **the dispatch's own 0.5 px** for the
sub-pixel residual rather than inventing a constant after seeing a result. The
measured floor is reported in the table above — **0.0672 to 0.2170 px on real
twins** — and the reasoning is written into the constant's own comment in the tool.

**What Gate C does and does not establish.** It pins the correlator's origin, the
sign convention, and the sub-pixel estimator's floor, on real twin texture. It does
**not** establish that the cross-modal correspondence is meaningful, because both its
legs correlate the twin field against itself or a shifted copy. The wrong-pairing
control in 3e is what carries that.

### 3c. Predictions, then results

| # | prediction | blind? | measured | verdict |
|---|---|---|---|---|
| P6 | Gate C passes; join ~0.50; if it fires it fires on the injection leg, not the null | yes | **HELD**; the only gate that fired was my own null tolerance, i.e. the opposite leg | join hit, the *reasoning* was wrong about which leg was fragile |
| P7 | silhouette leg in scope 90-200 of 682 (point 130) | yes | **161-222**; 4 of 8 views above band | **missed high on half** |
| P7 | interior leg in scope 80-250 (point 150) | yes | **126-222** | hit |
| P8 | silhouette median \|offset\| 2-6 px (point 3.5) at R=32 | **no** | **1.155-3.001 px**; 7 of 8 views below band | **missed low** |
| P8 | interior median \|offset\| 2-14 px (point 6) at R=32 | no | **3.458-11.124 px** | hit |
| P8 | **interior median > silhouette median on >= 6 of 8 views** (conf 0.75) | no | **8 of 8, at every radius** | hit, stronger than predicted |
| P9 | pinned fraction at R=16: silhouette 2-15%, interior 10-40% | yes | silhouette **5.2-17.4%** (7 of 8 in band), interior **8.2-23.6%** (7 of 8 in band) | mostly hit |
| P9 | pinned fraction at R=32: silhouette < 2%, interior < 10% | yes | silhouette **2.3-8.7%**, interior **5.0-16.4%** | **missed** |
| P9 | pinned fraction at R=48: both < 2%; confidence that 48 clears pinning to 0 = 0.35 | yes | silhouette **1.2-9.6%**, interior **4.1-9.7%**; **never 0** | **missed; the widening rule does not converge** |
| P9 | mean peak: silhouette 0.30-0.60, interior 0.15-0.45 | yes | silhouette **0.729-0.776**, interior **0.503-0.653** | **missed high on both legs** |
| P10 | control mean peak < 0.7x the right pairing | yes | silhouette **0.567x**, interior **0.681x** | hit |
| P10 | control median \|offset\| > 2x the right pairing | yes | silhouette **12.49x**, interior **3.53x** | hit |
| P11 | coherence ratio (neighbour / shuffled) < 0.5 silhouette, < 0.7 interior | yes | silhouette **0.572-0.788**, interior **0.630-0.835** | **missed on both** |
| P12 | cross-modal delta recovery within 1 px: 0.55-0.90 (point 0.75) | yes | **0.959-1.000** | **missed high — and see 3f, the leg is much weaker than its number** |

### 3d. The measurement

Denominator: **682 tiles per view.** Full table for all 8 views x 2 legs x 3 radii is
in `warp\warp_report.json -> measurement`. At R = 32:

| view | leg | in scope | pinned | unpinned | median \|d\| px | p90 \|d\| px | sd dx | sd dy | mean peak | coherence ratio |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | silhouette | 221 | 14 | 207 | 1.424 | 11.93 | 5.563 | 6.825 | 0.7420 | 0.717 |
| 0 | interior | 220 | 12 | 208 | 3.458 | 18.79 | 7.066 | 7.161 | 0.5849 | 0.684 |
| 1 | silhouette | 222 | 16 | 206 | 1.710 | 20.20 | 3.995 | 9.238 | 0.7390 | 0.697 |
| 1 | interior | 206 | 28 | 178 | 3.903 | 23.57 | 7.841 | 9.722 | 0.5737 | 0.748 |
| 2 | silhouette | 161 | 14 | 147 | 3.001 | 27.39 | 7.128 | 11.850 | 0.7292 | 0.788 |
| 2 | interior | 126 | 20 | 106 | 8.751 | 30.89 | 12.386 | 13.004 | 0.6081 | 0.677 |
| 3 | silhouette | 166 | 7 | 159 | 1.573 | 10.18 | 4.724 | 6.719 | 0.7758 | 0.735 |
| 3 | interior | 186 | 28 | 158 | 5.303 | 25.22 | 7.904 | 10.706 | 0.5636 | 0.699 |
| 4 | silhouette | 216 | 11 | 205 | 1.155 | 8.88 | 4.736 | 5.799 | 0.7728 | 0.652 |
| 4 | interior | 222 | 11 | 211 | 3.596 | 19.98 | 6.864 | 8.243 | 0.5951 | 0.730 |
| 5 | silhouette | 218 | 14 | 204 | 1.832 | 23.05 | 7.968 | 7.903 | 0.7601 | 0.611 |
| 5 | interior | 183 | 21 | 162 | 6.032 | 26.22 | 9.803 | 10.295 | 0.5313 | 0.726 |
| 6 | silhouette | 163 | 12 | 151 | 2.184 | 25.36 | 5.010 | 10.683 | 0.7729 | 0.572 |
| 6 | interior | 165 | 27 | 138 | 9.794 | 30.94 | 9.664 | 13.873 | 0.6525 | 0.708 |
| 7 | silhouette | 174 | 4 | 170 | 1.547 | 9.86 | 5.604 | 7.170 | 0.7483 | 0.711 |
| 7 | interior | 177 | 17 | 160 | 11.124 | 28.77 | 11.417 | 12.814 | 0.5030 | 0.749 |

**The global component and the local residual, separately** (R = 16, the least
tail-contaminated window; `warp_analysis.json -> global_vs_local`). The global term
is the per-view median offset vector; the residual is the spread about it.

| view | leg | \|global\| px | residual median px | residual p90 px |
|---|---|---|---|---|
| 0 | silhouette | 0.358 | 1.237 | 6.420 |
| 1 | silhouette | 0.268 | 1.612 | 10.865 |
| 2 | silhouette | 0.059 | 2.102 | 11.035 |
| 3 | silhouette | 0.631 | 1.485 | 5.161 |
| 4 | silhouette | 0.282 | 1.144 | 3.738 |
| 5 | silhouette | 0.168 | 1.662 | 7.593 |
| 6 | silhouette | 0.131 | 1.870 | 11.540 |
| 7 | silhouette | 0.159 | 1.432 | 6.195 |
| 0 | interior | 0.419 | 3.225 | 11.356 |
| 1 | interior | 0.440 | 3.332 | 12.237 |
| 2 | interior | 1.911 | 6.873 | 14.142 |
| 3 | interior | 0.778 | 4.279 | 13.242 |
| 4 | interior | 0.655 | 3.268 | 13.011 |
| 5 | interior | 0.475 | 4.165 | 14.644 |
| 6 | interior | 0.475 | 4.969 | 15.461 |
| 7 | interior | 0.529 | 5.206 | 15.252 |

**Against the 0.439 px boundary scale** (E41's median defect-texel distance to a
material boundary). Numerator and denominator separately; denominator is unpinned
in-scope tiles at R = 16.

| view | leg | denom | > 0.439 px | > 1 px | > 4 px | > 8 px |
|---|---|---|---|---|---|---|
| 0 | silhouette | 198 | 179 | 132 | 27 | 18 |
| 1 | silhouette | 203 | 187 | 146 | 46 | 28 |
| 2 | silhouette | 133 | 123 | 96 | 41 | 21 |
| 3 | silhouette | 154 | 145 | 107 | 20 | 12 |
| 4 | silhouette | 197 | 178 | 112 | 20 | 9 |
| 5 | silhouette | 199 | 185 | 147 | 39 | 20 |
| 6 | silhouette | 141 | 132 | 105 | 38 | 23 |
| 7 | silhouette | 165 | 154 | 119 | 28 | 15 |
| 0 | interior | 202 | 201 | 198 | 84 | 41 |
| 1 | interior | 175 | 172 | 164 | 65 | 32 |
| 2 | interior | 105 | 104 | 104 | 85 | 44 |
| 3 | interior | 147 | 147 | 145 | 82 | 33 |
| 4 | interior | 199 | 196 | 187 | 79 | 43 |
| 5 | interior | 158 | 155 | 151 | 81 | 45 |
| 6 | interior | 126 | 126 | 125 | 81 | 52 |
| 7 | interior | 146 | 146 | 140 | 83 | 53 |

**Peak-stratified** (`warp_analysis.json -> peak_strata`, R = 32): the offsets are
not confined to low-confidence tiles. Median \|offset\| within the highest peak band
(> 0.85) runs **0.95-5.57 px** on the silhouette leg over 50-81 tiles per view, and
**2.96-18.43 px** on the interior leg over 5-18 tiles per view.

### 3e. The controls

**Wrong pairing** — view i's mesh field against view j's twin, j = i+1 and j = i+4,
16 pairs per leg, R = 32:

| leg | right-pairing mean peak | control mean peak | ratio | right median \|d\| | control median \|d\| | ratio |
|---|---|---|---|---|---|---|
| silhouette | 0.7550 | 0.4280 | **0.567** | 1.803 px | 22.529 px | **12.49** |
| interior | 0.5765 | 0.3927 | **0.681** | 6.495 px | 22.939 px | **3.53** |

The instrument separates the right pairing from a wrong one on both legs and on both
statistics.

**Widening does not converge.** Pinned fraction of in-scope tiles, per leg, per
radius, across the 8 views:

| leg | R = 16 | R = 32 | R = 48 |
|---|---|---|---|
| silhouette | 5.2 - 17.4% | 2.3 - 8.7% | **1.2 - 9.6%** |
| interior | 8.2 - 23.6% | 5.0 - 16.4% | **4.1 - 9.7%** |

On 6 of 8 views the silhouette leg's pinned fraction is flat or **rises** from R = 32
to R = 48. Meanwhile the tail inflates with the window on every row — view 1's
silhouette p90 goes 10.66 -> 20.20 -> 32.63 px as R goes 16 -> 32 -> 48, and its
sd dx goes 2.34 -> 4.00 -> 9.05 — while the **median barely moves** (1.572 -> 1.710
-> 1.740). The dispatch's stopping rule ("widen until no tile pins") therefore has no
stopping point on this data.

### 3f. A weakness in my own instrument, found after running it

**The cross-modal delta leg is much weaker than its number.** It reported 95.9-100%
of tiles recovering an injected shift within 1 px. Shifting the *search* field
translates the entire ZNCC surface, so the argmax translates by exactly the shift
**whether or not the peak was a real correspondence**. The leg therefore recovers the
injection from any dominant peak, including a stable artefact. Its ~99% is not
evidence that the twin-to-mesh correspondence is real.

This is measured, not argued: T81 shows the surface-translation identity holding
exactly for an **unrelated noise template** (max \|diff\| under 1e-5, with a can-fail
leg proving a one-pixel-wrong translation does not also match), and shows the same
unrelated template still recovering 67% of the injection through the full delta
pipeline. The gap between 67% and the real data's 99% is the window edge: a
near-random surface lets a value newly entering the shifted window beat the
translated peak, while a dominant real peak is not beaten.

The same limitation applies to Gate C's own injection legs, and is stated in 3b.
**The wrong-pairing control in 3e is the leg that carries the cross-modal evidence.**

**And one property of the pinning signal, pinned as a test.** Pinning detects an
out-of-window peak only while the correlation surface still slopes toward it. On the
synthetic fixture at correlation length ~2 px, a 20 px offset inside an 8 px window
pinned only **15%** of tiles; at correlation length ~6 px it pinned over 50%. So "no
tile pins" does not mean "the window is wide enough", and the peak value is the other
half of that reading. Both are reported per tile.

### 3g. Tests (T81, uncommitted)

`E:\AI\facet\tests\test_t81_twin_mesh_warp.py` — 23 tests, all green. Legs: the
selftest as a subprocess; self-correlation reading exactly zero; five parametrised
injected shifts read back with the declared sign, plus a can-fail proving the
inverted sign does not also satisfy the assertion; the scope floor's locality and its
absolute floor, each with a fixture that fails the other; every tile returned
regardless of scope; pinning detected when the surface slopes **and** the pinned test
that it is not a complete detector; interior-edge extraction; the isoluminant chroma
edge **and** the discriminator showing an L*-only field misses it; Gate C holding;
**Gate C firing** on a field with no information in one axis; Gate C firing under
`-O` and `PYTHONOPTIMIZE=1`; the null-tolerance provenance; and the two legs in 3f.

Two of my own tests failed on first run and both were my authoring errors, not tool
defects: a wrong tile-grid arithmetic (4 vs 9), and a claim about the delta leg that
was stronger than the truth. Both were re-stated to what is measurable and both now
carry can-fail legs.

---

## 4. The pictures

`E:\AI\training\facet_E45\sheets\` — 22 files.

| picture | path |
|---|---|
| per-tile dx / dy / magnitude heatmaps, all 8 views, silhouette leg, R = 16 | `heatmap_silhouette_R16.png` |
| same, interior leg | `heatmap_interior_R16.png` |
| quiver over the twin at **native 752 x 1024**, arrows x8.3, coloured by magnitude | `quiver_view{0..7}_{silhouette,interior}_R16.png` (16 files) |
| mesh interior depth edges over the twin, yaw 45, full frame | `edges_over_twin_view1_yaw45_full.png` |
| the same at the Director's zoom (2x, torso/beard/pauldron/hilt crop) | `edges_over_twin_view1_yaw45_ZOOM2x.png` |
| mesh interior depth edges over the **elevated** camera's painted image, full frame | `edges_over_INPAINTED_job_y000_e55_full.png` |
| the same at 2x | `edges_over_INPAINTED_job_y000_e55_ZOOM2x.png` |

**One deliverable could not be produced as specified.** The dispatch asks for the
interior-edge overlay "mesh edges over twin ... for at least yaw 45 and one elevated
view". **There is no twin at any elevated view** — the same fact Gate A fired on. The
elevated overlay is therefore drawn over `state_inpainted.png`, the brush's own
output at that camera, and is named `edges_over_INPAINTED_*` so it cannot be mistaken
for a twin overlay.

---

## 5. The s3_composite smoke — DIAGNOSTIC, not a measurement

Run on the advisor's zero-obligation offer, after Gate A and the bundle.
`tools/s3_composite.py` and `tests/test_t77_s3_composite.py` were not modified.

The eight view dicts assembled straight from the emitted arrays satisfy
`s3_composite`'s input contract as written; `s3_composite(views, target=1)` returned
in 2.8 s with `dependent` and `independent` (1024, 752, 3) float32, `owner` and
`primary` int16, `disagreement` float32, `coverage` and `fallback` bool, and
`contrib` (8,). Within view 1's silhouette: coverage 0.9845, fallback 0.4139, median
disagreement 0.05349, owner histogram
`{-1: 4010, 0: 35987, 1: 82794, 2: 17627, 3: 5036, 4: 128, 5: 1, 6: 63, 7: 4134}`.
Stills at `E:\AI\training\facet_E45\s3_smoke\`.

**Nothing in this section is evidence about the asset.** It says the bundle loads.

---

## 6. What I did NOT do

- **Did not emit the bundle the dispatch specified for views 0 and 4** (an el-55
  camera carrying `twin_0` / `twin_4`). Gate A fired; the pairing does not exist.
- **Did not tune any camera** to make Gate A pass. Every camera parameter in every
  measurement is read off disk.
- **Did not invent a pass condition for task 2**, and did not filter the headline
  numbers by peak confidence — the peak stratification is an extra column on the same
  tiles.
- **Did not retune** tile size, stride, sigma or the scope floor after seeing a real
  offset. They were frozen in `predictions_task2.md` before the first real
  correlation.
- **Did not measure warp correction.** Out of scope by the dispatch; task 2 measures.
- **Did not commit or push anything.** Every change is uncommitted for the advisor's
  fold.
- **Did not edit the T34 count surfaces or any count-pin test**, and did not touch
  `tools/s3_composite.py`, `tests/test_t77_s3_composite.py`, or the other channel's
  uncommitted `tools/flow_estimate.py`, `tools/s3_run.py`,
  `tests/test_t79_flow_estimate.py`, `tests/test_t80_s3_run.py`.
- **Did not write to the memory store.**
- **Did not run any generation, any cloud call, or any Blender invocation.**
- **Did not characterise the interior leg's larger offsets as good or bad.** The
  pictures are for the Director.

## 7. Counts for the advisor's T34 reconciliation

Collected at land time against the tree as it stands, not quoted from memory
(`pytest --collect-only -q --basetemp=<scratch>`, and again with `-m "not artifacts"`).

**THE TREE MOVED TWICE WHILE THIS WAS BEING WRITTEN, so a single number is not a
fact here — the timestamp is part of the measurement.**

| taken at | full | hermetic | tree also held |
|---|---|---|---|
| during the suite run | 1159 | 1114 | + T79, T80 (another channel, uncommitted) |
| **2026-08-16T15:47:56-04:00, final** | **1166** | **1121** | + T79, T80, **T82** and `tools/s3_sheet.py` (another channel, uncommitted) |

**Neither total is this seat's contribution alone.** This seat adds **42 tests**:
T78 (19) + T81 (23). The seat edited no count surface and no count-pin test, and the
full-suite result in section 8 was taken at the 1159 snapshot.

## 8. Suite state — 27 failed, 1132 passed, 1159 collected (801 s)

Full run, `--basetemp` on scratch (the known Windows PermissionError repair; it adds
capability and removes no coverage).

**25 of the 27 are T34 count-surface rows** — the thirteen pinned surfaces plus the
eight README translations plus the two stale-surface can-fail legs — moved by the
collected count changing. They are the advisor's to reconcile at the fold and were
not touched.

**The other two are red at HEAD independently of this seat, and both trace to the
committed kickoff.** Each was diagnosed rather than assumed:

1. `test_t24_paid_for_by_reads_every_arc_the_record_has`.
   `facet_index.PAID_RE` is `\b(E0[1-9]|E[12]\d|E3\d|E4[0-4])\b` — bounded at **E44**.
   `parse_experiments()` now returns a maximum arc of **E45**, because
   `docs/experiments/E45-warp-and-aov-kickoff.md` is **tracked at HEAD**
   (`git ls-files docs/experiments/E45*` returns exactly that one file; this report is
   untracked and cannot lower the maximum). The test's own docstring says it "is
   deliberately the leg that goes red the first time an arc lands without this
   declaration being edited." Repair: extend `PAID_RE` to E45 in `tools/facet_index.py`.

2. `test_t41_axis_d_is_idempotent_across_runs`.
   Exactly **one** row drifted: `e13_anchor_check.py`, committed count 5, fresh count
   6. The sixth citation is `docs/experiments/E45-warp-and-aov-kickoff.md`, which names
   that module in its premise list. Every one of the six citing files is tracked; none
   is this seat's. Repair: re-run `python tools/instrument_census.py --committed` in
   the commit that moves it.

Both repairs are count/vocabulary surfaces of the same family as T34 and were left
for the fold.

Two DeprecationWarnings in `test_t59` (`'maxsplit' passed as positional`) are
pre-existing and untouched.

### An observation outside this seat's scope

`tools/callieri_border.py` emits two `RuntimeWarning: invalid value encountered in
subtract` at :209 and :214 on every real frame, from `inf - inf` on
background-to-background 4-neighbour pairs. The result is unaffected — the `pair`
mask excludes those pixels and `NaN > thr` is `False` — but the warning appears on
every emitter run. Not repaired here: it is a shipped tool with pinned numbers and no
part of this dispatch.
