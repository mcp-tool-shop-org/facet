# E34 report — projection coverage on the performer

**Seat:** executor · **Ran:** 2026-08-13 · **Spec:**
[E34-projection-coverage-kickoff.md](E34-projection-coverage-kickoff.md) ·
**Predictions:** [E34-predictions.md](E34-predictions.md), registered blind before stage 1.

This report carries **no verdicts**. The Director's eye rules the repaired views. Where this
document says a gate "did not fire", that is the arithmetic of a stated condition, not a
judgement about whether the output is good.

---

## 0. Environment and the open gates

| gate | result |
|---|---|
| E15 index ritual, **scratch** `--db` | **19 / 19**, all four legs, `VERIFY PASSED`, exit 0. 34 experiments |
| watchdog heartbeat | **advancing** — `_watchdog_HEARTBEAT` 18:27:46.??? → 18:27:57.770. Checked as movement, not exit code |
| interpreter pre-check (T18) | absolute interpreter reports **0 missing** of the 8 required (`numpy, scipy, PIL, trimesh, open3d, mcp, cv2, record_index`); bare `python` raises `ModuleNotFoundError: open3d`, which is the law's own case |
| manifest A — `facet_E33` | **HELD at open and close**: 117 declared, **0 changed / 0 missing / 0 added** |
| manifest B — eight protected subtrees | **HELD at open and close**: **7,312 files / 17,072,807,610 bytes**, `added 0 removed 0 changed 0` |

`facet_E33`'s file count and the eight subtrees' file count and **byte total** reproduce E23's
recorded figures exactly (E23 recorded 7,312 / 17,072,807,610).

⚠ **One self-reference, reported rather than counted as a change.** `E33_manifest.json`
records **itself** at 14,008 bytes / sha `f8164e25…`; on disk it is **17,991 bytes** /
`18d264c5…`. A manifest cannot contain its own final hash, and E33 §12 lists 91 files while
its delivery line lists 117 — the file was regenerated after its own entry was written. The
other 116 entries match exactly. This is disclosed as an instrument property, not as a tree
delta, and the gate is computed excluding it.

**The protected-subtree manifest is a scratchpad instrument, and that was enumerated before
writing one.** `tools/` has no `tree_manifest.py`; the E23 report records that E22's copy
"lived in that session's scratchpad and is gone". Writing a session-scratch manifest is the
established pattern here, not a commission.

---

## 1. G1 — enumerate before commissioning. All three recovered; **zero commissions**

| item | resolution | status |
|---|---|---|
| the control builder | **`tools/restylize_views.py --emit-only`** | **MEASURED** |
| the prompt builder's eight-view coverage | `tools/diagnostics/e12_make_twin_prompts.py`, `--views` **defaults to `0,1,2,3,4,5,6,7`** | **MEASURED** |
| E33's exact projection invocation | reconstructed and replayed | **MEASURED** |

**The control builder was not obvious and the first two candidates were wrong.**
`e12_canny_derive.py` looks like a control builder and is not — its own docstring says it
"ADOPTS NOTHING and ARMS NO GATE", and it names `restylize_views.control_image` as "the one
place that knows how a control is built". Following that pointer reached `--emit-only`, which
"build[s] and write[s] the control image + exact figure mask per view, then stop[s]".

**Recovered by replay, not by assertion.** E33's control for view 0 was rebuilt from the
recorded clay render and geometry mask:

```
armclay_0_control.png   PIXELS IDENTICAL   sha256 cabfad616b07a259..  byte-equal
armclay_0_mask.png      PIXELS IDENTICAL   sha256 87c4d2aac2d3589e..  byte-equal
```

`cabfad616b07a259…` is the control sha256 **E33 §7 already records** for view 0. The builder
is therefore identified by reproduction rather than by inference.

### 1a. The projection invocation was recovered by arithmetic, then by replay

`project_twins.py` writes **no provenance JSON** of its own invocation, and E33 §14b prints it
elided (`--view 0=… --view 4=…`). Two steps closed it:

**`--aspect` settled by arithmetic before anything ran.** The tool computes
`v_ext = z_extent × margin`, `h_ext = v_ext × AW/AH`. `frame_300k.json` records
`coverage_world` = **w 0.414633 / h 1.206205**, whose ratio is **0.34375 = 352/1024 exactly**;
the argument's default `752,1024` would give 0.734. So E33 ran `--aspect 352,1024 --margin 1.204`.

**Then the whole two-view run was replayed** into a scratch path under `facet_E34\` — E33
untouched — and **every recorded number came back to the digit**:

| quantity | E33 recorded | replay |
|---|---|---|
| valid texels / head band | 2,444,770 / 1,198,542 | identical |
| reg-IoU y+000 / y+180 | 0.8605 / 0.8475 | identical |
| centroid offset | dx +5.5 dy +29.9 / dx +5.8 dy +32.7 | identical |
| erosion cost, y+000 4–8 px | 37.2% | identical |
| background probe y+000 / y+180 | 8,330 @ 9.00% / 15,683 @ 36.58% | identical |
| styled texels | 1,517,278 | identical |
| styled/reachable · styled/valid · reachable/valid | 84.2% · 62.1% · 73.7% | identical |
| holes into finalize | 927,492 | identical |

and `stage1_styled_mask.npy` is **byte-identical**, sha256 `f78e3c53822e97ac…` both sides.
Premise 5's second clause moves from ASSUMED to **MEASURED**.

### 1b. An enumeration discrepancy in the dispatch

The spec says *"the **six** named landmarks"* and names **five**: jaw, temple, shoulder,
ribcage, flank. Recorded here rather than silently resolved; P6 was registered over the five
named, across the six affected views.

---

## 2. Controls for views 1, 2, 3, 5, 6, 7

Built by the G1-located builder, one call, six inputs.

| view | control px | canny | contour | figure mask | frame | mask == geometry silhouette |
|---|---|---|---|---|---|---|
| 1 | 13,991 | 7,824 | **10,987** | 25.4% | 352×1024 | yes, byte-identical |
| 2 | 8,026 | 5,095 | **5,193** | 15.6% | 352×1024 | yes, byte-identical |
| 3 | 13,341 | 7,255 | **10,917** | 25.3% | 352×1024 | yes, byte-identical |
| 5 | 13,345 | 7,186 | **10,987** | 25.4% | 352×1024 | yes, byte-identical |
| 6 | 8,180 | 5,235 | **5,193** | 15.6% | 352×1024 | yes, byte-identical |
| 7 | 13,961 | 7,889 | **10,917** | 25.3% | 352×1024 | yes, byte-identical |

Contour ANDON ≥ 500 px: **lowest is 5,193**, on both profile views. Frames exact. The written
mask is byte-identical to `masks_300k`'s raycast silhouette on every view — geometry, never a
key. The contour ≥ 500 px condition is the **spec's**, not the tool's: `restylize_views.py`
carries only a mask/input count ANDON, so the check was computed here.

---

## 3. Prompts — the byte-exact gate PASSED

```
armclay_0   433 chars   sha256 d8ed1a3968819f13..  vs recorded d8ed1a3968819f13..  BYTE-EXACT
armclay_4   350 chars   sha256 f3dd547267b5721f..  vs recorded f3dd547267b5721f..  BYTE-EXACT
```

`_negative` and `_entry_verbatim` identical; term counts 16 / 13 as recorded. **The machine
reproduces the recorded two, so the six are the same machine's output.**

**The drop map was taken from the record, not chosen.** The three face terms drop on views
**3, 4, 5** — which is what `E12-twin-prompts.json`'s own recorded eight-view map does for its
face-interior terms (mouth interior, tongue, eyes, fangs → views 3,4,5), and what the spec's
own G4 halt signature ("face features on views 3/4/5") describes. Views 0, 1, 2, 6, 7 keep the
full 16-term entry and are asserted byte-equal to it by the builder.

Output: [E34-twin-prompts-r3-8view.json](E34-twin-prompts-r3-8view.json).

---

## 4. Six cloud twins

**Link topology was checked in code before submission — that is the gate.** Per view: every
`[node, slot]` target present, no self-links, no `LoraLoader` and no node 5, node 6 wired to
`["1", 0]`, exactly one `SaveImage`, every node reachable from it, and **no field moved that
was not supposed to move**. The builder loads E33's `payload_r3_v0.json` as the template and
permits only `7.text`, `9.image`, `10.image`, `15.filename_prefix` to differ; anything else is
an error.

```
LINK TOPOLOGY GATE: 0 error(s) across all six graphs
```

Views 1, 2, 6, 7 show **no `7.text` move at all**, because their stems are byte-equal to the
full entry; only 3 and 5 move it. That is the drop map showing up in the payloads.

`dry_run` then returned `status: validated`, **0 warnings** — recorded as corroboration, not
as the gate (E04 Arm G7: a self-referencing link once returned `validated`).

Pinned from the template, not retyped: seed **770700** · steps 20 · cfg 2.5 · denoise 0.92 ·
euler/simple · shift 3.1 · cn_strength 0.9 · `qwen_image_fp8_e4m3fn` /
`qwen_2.5_vl_7b_fp8_scaled` / `qwen_image_vae` / `Qwen-Image-InstantX-ControlNet-Union`.

| view | job id | output blob (cloud) | local sha256 | frame |
|---|---|---|---|---|
| 1 | `4859ea29-b928-4096-a774-90e2bcce2f46` | `053d864435c78a18…` | `94270d00e266b831…` | 352×1024 |
| 2 | `0afccfdb-d32c-4154-afab-45b4c3f0aa4a` | `af76aad561c97ce6…` | `0081f19437703627…` | 352×1024 |
| 3 | `d138286b-d2f5-46c3-9615-084039b70ac8` | `7e86c6bd7db381f4…` | `8e881fc8b46cbccd…` | 352×1024 |
| 5 | `cf9970a8-5651-4e60-a91f-9497e4991852` | `1cf0a74de48882b2…` | `54f7204014c1c436…` | 352×1024 |
| 6 | `01dec11b-f8c4-46ce-82c6-048694df5ee1` | `aab6e776be519ada…` | `b5714aad12a3ef63…` | 352×1024 |
| 7 | `be75af25-7353-4b52-887a-dc9c07c29614` | `9192f91f837f99b9…` | `4f1db149a3c91ddc…` | 352×1024 |

**6 submitted, 0 failed, 0 re-rolls. Ceiling 8; two jobs remain unspent.**

⚠ **E08 gotcha 8 fires a third time, and on a new side.** E33 recorded that the cloud's
returned *input* name is not the local file's sha256. Here the returned **output blob name is
also not the sha256 of the bytes received** (`053d8644…` vs `94270d00…`, all six). Both are
recorded per view in `twin_payloads/submission_manifest.json` so a future byte mismatch is not
attributed to the wrong cause.

**Queue behaviour, recorded because it is a venue property.** The batch sat at
`running 0 / pending 6` for roughly **30 minutes** before executing; the account-wide queue
showed nothing ahead of it. Nothing was resubmitted — a resubmission would have spent ceiling
jobs against a scheduling delay.

### 4a. Credits — the GPU-hours clause is **NOT YET MEASURABLE**, and is not measured at zero

Both reads return **identical totals**: GPU Hours Product **21,768,902.422995 micros**, total
**$76.597931**. The delta is 0.000000 on every line.

**That zero is a window boundary, not a cost.** `get_usage_report`'s period ends at
**2026-08-13T23:00:00Z** on both reads, and the six jobs executed at **~23:12Z** (the
`X-Goog-Date` on the output signed URLs is `20260813T231217Z`). The jobs fall outside the
reporting window entirely. E33's rate implies ~$0.61 for six jobs, which is P7's registered
point estimate; it stands **unverified** here.

⚠ **The attribution caveat is stronger on this arc than on E33's.** At the before-read the
workspace was demonstrably not idle: a **Wan Video** bucket of 3,000,000 micros at 20:00–21:00Z
and a GPU bucket of 1,015,186.709495 micros at 21:00–22:00Z, neither this arc's. E33 recorded
that bucket-delta attribution *cannot prove* exclusivity; here non-exclusivity is **observed**.
Any delta later measured across this window is an **upper bound**, not a measurement.

⚠ **An instrument artifact worth recording:** `granularity=month` returned **zero usage
records** for a period where `hour` and `day` both return $76.597931. The tool's own message
warns this is not a confirmation that nothing was spent. Noted so a future seat does not read
a month-granularity zero as a measurement.

**Partner lines: every line byte-identical across both reads** — consistent with P7's second
clause, and carrying the same caveat, since nothing from this arc has posted at all.

---

## 5. G4 — the twin sheet, walked at full size before projection

Walked as an eight-across strip at **native 352×1024 per panel** (`E34_twin_strip_native.png`,
2816×1024), which is full size for the twins themselves; `E34_twin_sheet.png` carries the
clay | control | twin rows.

**No halt signature fired.**

| signature | measured |
|---|---|
| material / register discontinuity vs R3 | none — all eight read as unglazed terracotta, matte, soft studio light, plain pale grey backdrop. Nothing glazed, wooden, painted or painterly |
| face features on views 3 / 4 / 5 | **none** — views 3 and 5 show the back of the head and an ear; view 4 likewise. The drop map landed |
| keyed bbox ≥ 98% of frame on either axis | **none** — widest is view 0 at **90.9%** of 352 px; tallest is view 6 at **83.9%** of 1024 px |
| any twin not 352×1024 | none — all eight exact |

Views 2 and 6 are proper mirror profiles, both carrying the face (they keep the face terms);
views 1 and 7 are the front three-quarters, also with the face.

### 5a. The registration diagnostic, and its mirror assumption verified first

⚠ **`e14_twin_registration.py` pairs mirrors by ROW POSITION, not by label** — line 117 is a
hard-coded `((0,4),(1,5),(2,6),(3,7))` indexed into `rows`. Its corroboration lines are
therefore valid only when exactly eight twins/masks/labels are passed **in view order**; a
six-row set is E33 §10 defect 2's crash, which is a consequence of this line and not a quirk.
Verified before any of its output was read; all eight were passed in order.

The assumption then held at its design case — opposite views share a silhouette to the pixel:

```
v0 vs v4: sil 91,207 == 91,207    v2 vs v6: sil 56,254 == 56,254
v1 vs v5: sil 91,415 vs 91,416    v3 vs v7: sil 91,082 == 91,082
```

⚠ **A second property of the same tool, recorded:** it binds **no profile at all**
(`ap.parse_args()` with no `subject_profile.bind`), so its printed line *"HALTS SUSPENDED per
prop.json"* is a **hardcoded string**, not a live binding. It also carries no halt arguments,
so it cannot halt regardless. "Suspended halts" is accurate in effect and misleading in
provenance.

Its own `bbox_check` flags **SUSPECT on views 2 and 6** (1.79× / 1.94× of the mesh width).
That is the leg E33 §10 measured unreliable, and it fires precisely on the two narrowest views
— the global-constant-on-a-local-feature shape. Carried as a diagnostic; the frame-fraction
rule above is what was applied.

---

## 6. Projection, fill, pack

`project_twins.py` with **eight** `--view` arguments, every value explicit with provenance:
`--aspect 352,1024` (recovered §1a) · `--step 45.0` · `--margin 1.204` · `--fit-axis height` ·
**`--bg-max-pct 100.0`** (R-a, the E16 Ruling 4e withdrawal, passed explicitly) ·
**`--reg-iou-min 0.80`** (R-b, untouched). Era flags **not used** (R-c).

**Atlas prep was reused, not rebuilt.** `facet_E33\prep_bake\` holds `mask.npy`, `nor.npy`,
`pos.npy`, `prep_uv.glb` and `meta.json` (res 4096, crop 438,44,588,182, head_scale 3.0) — the
same mesh, cull and crop. `project_twins` only reads `--prep`, so E33's directory was pointed
at directly and never written.

### 6a. Registration per view — the gate did NOT fire

| view | class | reg-IoU | twin paint bbox | mesh silhouette bbox | centroid \|d\| |
|---|---|---|---|---|---|
| 0 | pole | 0.8605 | 850 × 317 | 849 × 283 | 30.4 |
| 1 | three-quarter | 0.9196 | 853 × 282 | 849 × 214 | 7.7 |
| 2 | **profile** | **0.9479** | 853 × 138 | 849 × 139 | **1.6** |
| 3 | three-quarter | 0.8835 | 849 × 271 | 849 × 231 | 11.4 |
| 4 | pole | 0.8475 | 850 × 316 | 849 × 283 | 33.2 |
| 5 | three-quarter | 0.9042 | 852 × 226 | 849 × 214 | 12.5 |
| 6 | **profile** | **0.9349** | 852 × 160 | 849 × 139 | **3.4** |
| 7 | three-quarter | 0.8745 | 850 × 290 | 849 × 231 | 25.3 |

**Minimum 0.8475 against a limit of 0.80.** No numerator/denominator halt report is required.

**Views 0 and 4 reproduce their E33 values exactly** — 0.8605 / 0.8475, styled 797,982 /
719,296, erosion 4–8 px 37.2%, probes 8,330 @ 9.00% and 15,683 @ 36.58%. Adding six cameras
perturbed neither recorded view's per-view measurement.

Two **diagnostic NOTEs** (explicitly not halts) fired, on views 1 and 7: keyed twin bbox
exceeds the mesh silhouette by more than 25%, the tool attributing it to a probable cast
shadow that the trust mask no longer reads.

**Background probe, per view, gating nothing** (R-a): newly admitted 8,330 / 5,254 / 2,131 /
4,495 / 15,683 / 6,888 / 5,428 / 2,324 texels at median ΔE 19.6 / 12.0 / 10.4 / 15.0 / 12.8 /
12.6 / 10.1 / 27.7 from the fitted background; within ΔE 10 of it 9.00% / 33.65% / 48.52% /
22.54% / 36.58% / 27.37% / 49.06% / 3.83%. Already-trusted texels within ΔE 10: **0.00% on
every view**.

**Erosion cost by structure half-width** — required in every report of this arm (E08 A3), and
a diagnostic rather than a gate. The thinnest stratum is annihilated or nearly so on the new
views: 4–8 px removes **90.3% (v1), 56.2% (v2), 100.0% (v3), 94.4% (v5), 65.5% (v6), 100.0%
(v7)** — against populations of only 93 / 267 / 84 / 54 / 223 / 61 px. The 8–16 px stratum
runs 18.1–24.9%, 16–32 px 8.9–12.4%, 32+ px 4.4–5.8%.

### 6b. Coverage

| quantity | E33 (2 views) | E34 (8 views) |
|---|---|---|
| valid texels | 2,444,770 | 2,444,770 (unchanged by construction) |
| styled | 1,517,278 | **2,287,542** |
| reachable | 1,801,207 | **2,325,263** |
| **styled / reachable** | 84.2% | **98.4%** |
| **styled / valid** | 62.1% | **93.6%** |
| **reachable / valid** | 73.7% | **95.1%** |
| **holes into finalize** | 927,492 | **157,228** |

⚠ **A stale string in the tool:** the `reachable/valid` line prints *"(what **two** views can
physically reach here)"* regardless of camera count — it read "two views" on an eight-camera
run. Cosmetic, recorded so the printed line is not quoted as a claim about the camera set.

### 6c. Fill — both gates passed, and one unit trap avoided

```
[finalize] filling 157,228 hole texels (surface-aware)
  source distance  median 0.00321 = 1.82 edges   p95 0.01633   max 0.04791
  beyond 5 edges 17.54%   beyond 20 edges 0.333%
  normal disagrees >60deg 26.62%   back-facing 19.94%   (REPORTED, not gated)
```

| gate | limit | measured |
|---|---|---|
| `--max-edge-median` | 3.0 edges | **1.82** |
| `--max-frac-beyond` (share) | 0.05 = 5% | **0.333%** |

E33's margins were 2.974/3.0 (1%) and 1.024%. Both moved further from their limits.

⚠ **`--max-frac-beyond` is a SHARE, and the spec writes it as "5.0".** The argument's default
is `0.05` and the ANDON prints `args.max_frac_beyond * 100`. Passing the spec's literal `5.0`
would have set a **500%** limit and silently disarmed the gate. Checked before passing; `0.05`
was passed.

**`mean fallback 0` is STRUCTURAL in surface-aware mode and is not a pass** (E14 Ruling 31d) —
the tool says so itself, and it is excluded from the gate reading above.

⚠ **The two reported-not-gated normal statistics rose sharply**: normal-disagrees-over-60°
**8.47% → 26.62%**, back-facing **4.96% → 19.94%**. The hole population fell 83%, so what
remains is the harder residue — deep-occlusion surface whose nearest painted source is more
likely to face elsewhere. Reported, per E07 Gate 0.5; nothing here gates on it.

### 6d. Pack

⚠ `bake_hero_pack.py` imports `bpy` and cannot run under the trellis2 interpreter
(`ModuleNotFoundError: No module named 'bpy'`). Run through
`blender -b -P … --` per the environment law.

```
path    E:\AI\training\facet_E34\out\performer_textured_8view.glb
bytes   22,284,208
sha256  ce7930643e573b475737eca676d9118b036d5e131c8b7af66a65b3b7ae0113c5
```

**Brush: NOT RUN** (out of scope). The holes were closed by surface-aware dilation alone, as
in E33 — the difference is that there were 157,228 of them instead of 927,492.

---

## 7. Evidence — the sheet was built before any number in this section

### 7a. A render confound was found and removed before anything was read off the sheet

The first before/after sheet, built from E33's recorded `turn_final` against the new render,
showed the candidate markedly **darker and browner with less visible surface hatching** across
the whole figure — a material-scale difference, not a patch-scale one.

**E33's `turn_final` was made by an invocation this arc never recovered**, so render settings
were an uncontrolled variable in that comparison. Tested in texture space, which is
independent of any render:

| atlas, over the 2,444,770 valid texels | mean RGB | mean luma | std |
|---|---|---|---|
| E33 `atlas_final.png` | 149.62 / 106.52 / 82.33 | **112.82** | 46.13 |
| E34 `atlas_final.png` | 152.43 / 106.92 / 78.83 | **112.73** | 44.16 |

**The two atlases carry the same material** — mean luma differs by 0.09 of 255. The darkening
was the render, not the texture. E33's recorded GLB was then **re-rendered through the
identical `turn_render.py` call** and the comparison rebuilt:

- `E34_before_after_lit.png` — the confounded sheet, kept rather than deleted
- **`E34_before_after_controlled.png`** — E33's GLB and the candidate, same call, six affected views
- `E34_poles_regression.png` — views 0 and 4, same call

### 7b. What the controlled sheet shows

In the BEFORE row the unpainted regions are plainly visible at the recorded landmarks: jaw and
neck and hands on view 1; temple, jaw and knee on view 2; back-of-head and shoulder on view 3;
temple and a large flank/ribcage patch on view 5; temple, jaw and hands on view 6; temple/jaw
and flank on view 7. **In the AFTER row none of them survives.** Material now matches between
the two rows, which is the confound removal working.

Three observations offered as observations, for the Director's eye and not as findings:

1. the AFTER surface reads **smoother**, with less of the fine sculpted hatching visible in the BEFORE;
2. the **brow/eye region on views 1 and 7 is more defined** — those are views whose twins carried the face terms;
3. views 3 and 5 show a **faint vertical tonal boundary** down the back of the head and neck.

### 7c. Texel provenance — total **and** largest 4-connected component

Both runs use the same instrument and the same `--prep`. E33's stage-1 inputs were **copied
out** of the sealed tree first, so nothing wrote to `facet_E33`.

| class | E33 (2 views) | E34 (8 views) | change |
|---|---|---|---|
| TWINS (stage 1), total | 1,517,278 (62.1%) | **2,287,542 (93.6%)** | +50.8% |
| TWINS, largest component | 45,550 | 46,631 | +2.4% |
| **DILATION (never painted), total** | **927,492 (37.9%)** | **157,228 (6.4%)** | **−83.0%** |
| **DILATION, largest component** | **22,457** | **7,390** | **−67.1%** |

Both members of the pair fall, which is what makes the pair readable (E28 Ruling 21): this is
neither one large patch shattered into speckle (total would hold while the component fell) nor
speckle cleared around a surviving patch (the component would hold). The component figure is a
**lower bound** on the surface-contiguous run, because atlas adjacency is not surface
adjacency — the instrument prints that direction itself.

⚠ **A served-surface gap.** `mcp__facet-measure__texel_provenance` **REFUSES** an empty
`order` (`BAD_ARGUMENT: order names no job keys`), while the underlying
`tools/diagnostics/texel_provenance.py` handles it — `order` filters empties and the class
list degrades to TWINS + DILATION. A **brush-not-run** census is exactly this arc's shape and
the E33 arc's before it. The instrument was called directly; the wrapper's guard is recorded
as a gap, not worked around silently.

### 7d. Regression

- **Views 0 and 4 carry no new unpainted patches** (`E34_poles_regression.png`). They do show
  slightly more tonal variation on the torso, which is ownership reassignment to neighbouring
  cameras — reassignment is not loss.
- **The recorded asset is byte-unchanged**: `performer_textured.glb`, **21,588,628 bytes**,
  sha256 **`9e20ea7d800c0ffd2cff101a5e1bcc01fa13c620bbbe3ef05ae23b093547b1aa`** — matching the
  spec's premise 6 exactly, at close.

---

## 8. Predictions against measurements

| # | prediction | band | measured | verdict |
|---|---|---|---|---|
| P1 | reachable / valid | 88–94% | **95.1%** | **MISS, high** |
| P2 | styled / reachable | 85–93% | **98.4%** | **MISS, high** |
| P3 | styled / valid | 76–86% | **93.6%** | **MISS, high** |
| P4 | holes into finalize | 342k–587k | **157,228** | **MISS, low** (derived from P3, declared as such) |
| P5 | profile views 2/6 reg-IoU | 0.70–0.82 | **0.9479 / 0.9349** | **MISS** — and they are the *best* two |
| P5 | gate fires on ≥1 of {2,6}, ~70% confidence | yes | **no** — minimum in set is 0.8475 at a pole | **MISS** |
| P5 | three-quarter views 1/3/5/7 | 0.82–0.87 | 0.9196 / 0.8835 / 0.9042 / 0.8745 | 2 of 4 in band; 1 and 5 above |
| P5 | poles unchanged | 0.8605 / 0.8475 | identical | **HIT** |
| P6 | all five landmark classes lose their patches | — | none survives on the controlled sheet | **HELD** — the Director's eye rules |
| P7 | GPU-hours delta $0.55–$0.72 | — | **NOT MEASURABLE** (window ends 23:00:00Z; jobs ran 23:12Z) | **unresolved, not zero** |
| P7 | every partner line moves by exactly zero | — | all identical | **HELD**, with the caveat above |
| P8 | `dist_median_edges` | 1.6–2.7 | **1.82** | **HIT** |
| P8 | `dist_beyond_pct` | 0.2–0.9 | **0.333** | **HIT** |
| P9 | poles show no new patches; GLB hash unchanged | — | no new patches; `9e20ea7d…` unchanged | **HIT** |
| P10 | DILATION largest component | < 60,000 | **7,390** | **HIT** |

### 8a. Five misses, one mechanism — and it is the registration model

P1–P4 are not four independent misses. They are one quantity seen four ways: how much of the
atlas eight cameras accept. I predicted every one of them **low**, and P5 says why.

I modelled twin↔mesh registration from **the only two views the record had measured** — the
poles, at 0.8605/0.8475, with the twin painted 34 px wider than the mesh and sitting ~30 px
low. I then reasoned that a *fixed pixel* bleed would cost proportionally more on a narrow
profile, and predicted the profiles would register worst and might trip the gate.

Measured, the opposite holds and by a wide margin. At the profiles the twin paints **138 px
against a 139 px mesh** — narrower, not fatter — and the centroid offset collapses from
30.4/33.2 px at the poles to **1.6/3.4 px**. The fatness-and-drop is **a property of the pole
views specifically, not a global generator bleed**, so the six added cameras register *better*
than the two I extrapolated from, less paint is peeled by erosion, and coverage lands far above
every band I set.

**The unit was fine; the population I generalised from was two, and they were the outliers.**
This is the tenth consecutive arc to miss on the unit/population family and a new member of it:
not a mis-specified unit, not an unchecked property, but **a parameter fitted on the only
members that had been measured, when those members were unrepresentative**. The record could
not have told me otherwise — E33 measured exactly two views — but the prediction should have
carried that as its stated exposure rather than treating two poles as the subject's behaviour.
P5's own registered text names the rectangle model as an exposure and does not name this.

The one prediction that came from mechanism rather than extrapolation — P8, that nearer paint
on lateral surface would shorten the fill's search — hit both clauses.

---

## 8b. ⛔ A GATE FIRED — T24, and it was ALREADY RED AT HEAD

The full suite returns **1 failed / 926 passed** (664 s):

```
FAILED tests/test_t24_index_parsers.py::test_t24_paid_for_by_reads_every_arc_the_record_has
E   AssertionError: laws.paid_for_by cannot read 1 of the record's own arcs, so a law
E   citing one is attributed to nobody and nothing says so: E34
```

**The failure list was read complete and counted — exactly 1 — not off a tail.**

### What it is

`facet_index.PAID_RE` is frozen at **`\b(E0[1-9]|E[12]\d|E3[0-3])\b`**. Measured directly:

| arc | readable by `PAID_RE` |
|---|---|
| E32 | yes |
| E33 | yes |
| **E34** | **no** |

`_record_arc_span` derives the record's highest arc from `parse_experiments()` — the authored
status table plus the filesystem — so the moment **E34** entered the record, a law citing E34
became attributable to nobody, and this leg says so. That is the leg working.

### It is NOT this arc's doing, and that was measured rather than assumed

The obvious reading is that this arc's three new documents created E34 and tripped the leg.
**Measured, that is wrong.** With all three of this arc's files moved out and
`git status --porcelain` reporting a **clean tree at HEAD `66baef2`**, the test **still fails**:

```
=== does the test fail at HEAD, with my untracked files hidden? ===
(git status: clean)
FAILED tests/test_t24_index_parsers.py::test_t24_paid_for_by_reads_every_arc_the_record_has
1 failed in 0.11s
```

E34 entered the record at **`73a202c`**, the dispatching commit, which added
`docs/experiments/E34-projection-coverage-kickoff.md` while `PAID_RE` stayed at E33. **The
suite has been red since that commit.** The dispatch's own STATE line reads "Suite baseline
927/887" — the *count* is right (927 collected; 926 + 1 = 927) but it is a count, not a
result, and the red row is not disclosed anywhere in the dispatch.

### Not repaired here, and the reason is the spec's own

The repair is one character — `E3[0-3]` → `E3[0-4]` — and **T24 is already its can-fail
test**: it fails before and would pass after, so a repair commit would not need a new test.
It is still **not this seat's to make**:

- `tools/facet_index.py` is **published tool code** (`facet-index` / `facet-mcp`) and this
  spec commissioned no tool change;
- the spec's own out-of-scope section puts exactly this class — *"repairs to
  `e14_twin_registration.py` or `project_twins.py`'s resurrected default (recorded defects;
  each wants its own commit with tests)"* — in its own commit;
- the executor rule is to stop at a gate and report it with its evidence.

**Named and rejected alternatives** (E23's boundary requires the rejected options be written
down): narrowing T24's arc span to stop at E33 would remove coverage and is refused;
`-k "not t24"` or an xfail marker would smooth a fired gate into a green row and is refused.

⚠ **It will fire again on E35 and on every arc after it.** A one-character bump answers this
firing; it does not answer why a bound over the record's own arcs is a frozen literal that
each new arc must chase. That is the advisor's call, not this seat's.

## 9. Count surfaces — they do NOT move, and that was verified rather than assumed

No tool code and no test code changed this arc; the repo additions are three documents
(predictions, the eight-view prompts JSON, this report).

- `T34.PINS` read with `ast` at apply time: **16 pins across 6 files**, and **every one counts
  a test total** (full / hermetic / gap). None counts documents in `docs/experiments/`.
- `pytest --collect-only` at this tree: **927 tests collected**, matching the dispatch's
  baseline of 927.
- `tests/test_t34_front_door_counts.py`: **50 passed**.
- full suite: **926 passed / 1 failed** — the single failure is the pre-existing T24 red
  documented in §8b, which reproduces on a clean tree at HEAD with this arc's files removed.

**No new tests are required by the studio rule**, because no commit here touches tool code.
Tests T66+ remain unclaimed.

---

## 10. Artifacts

```
E:\AI\training\facet_E34\
  credits_before.json, credits_after.json    the two reads + the window-boundary finding
  twin_control\armclay_{0..7}_{control,mask}.png   six built here; 0/4 copied from E33
  twin_payloads\payload_r3_v{1,2,3,5,6,7}.json + submission_manifest.json
  twins\twin_r3_v{0..7}.png                  six generated; 0/4 copied from E33
  E34_twin_strip_native.png    2816x1024  - THE G4 WALK, native scale
  E34_twin_sheet.png           2116x16736 - clay | control | twin, eight rows
  twin_registration.json                     the diagnostic, eight rows in view order
  texpass\stage1.png + _holes/_styled_mask/_owner/_blend
  state\{atlas,holes}.png + styled_mask.npy  staged for finalize
  out\atlas_final.png, finalize.json
  out\performer_textured_8view.glb           <- THE CANDIDATE, sha256 ce7930643e573b47...
  turn_final\armfinal_{0..7}.png             candidate, default lit, 352x1024
  turn_final_flat\armflat_{0..7}.png         candidate, flat
  turn_e33_rerender\e33re_{0..7}.png         E33's GLB through the IDENTICAL call
  E34_before_after_lit.png                   the CONFOUNDED sheet, kept
  E34_before_after_controlled.png            <- THE SHEET, confound removed
  E34_poles_regression.png
  texel_provenance_{e33,e34}.json
  e33_state_copy\                            E33 stage-1 inputs, copied out to keep E33 read-only
  g1_replay\, g1_control_replay\             the G1 recovery evidence
```

**Compensators.** Every path above is new under `facet_E34\`, so
`rm -r E:\AI\training\facet_E34` undoes the local work; owner = this seat. Repo: three new
documents, `git reset --hard 66baef2`; **nothing pushed**. Cloud: the six jobs' GPU-hours have
**no compensator**, which is why the ceiling was stated before submission and why two of the
eight remain unspent. `facet_E33`, the eight protected subtrees and the recorded GLB were
opened read-only and are manifest-verified unchanged at close.

---

## 11. What the Director is being asked to look at

1. **`E34_before_after_controlled.png` at full size** — six affected views, E33's recorded GLB
   and the candidate rendered through the identical call.
2. **The candidate GLB at his own zoom** —
   `E:\AI\training\facet_E34\out\performer_textured_8view.glb`.
3. `turn_final_flat\` if he wants texture truth under flat light rather than the lit readout.
4. On his word: armature's re-run of its hole survey and RGBA-true turnaround against the
   candidate.

**And one thing needing a ruling rather than an eye:** the T24 red in §8b. It predates this
arc, it fires on every future arc, and its one-character repair touches published tool code
that this spec did not commission.

Open questions this report does not answer, and does not try to: whether the smoother surface
and the fainter hatching are acceptable against R3; whether the faint seam on views 3 and 5
matters; and whether the residual **157,228** dilation-filled texels — down from 927,492, with
the largest single patch at 7,390 — are acceptable as dilation, or whether the arc's evidence
now justifies putting an R3 brush configuration to him as a design decision.
