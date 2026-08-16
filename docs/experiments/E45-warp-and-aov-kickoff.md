# E45 — the twin-to-mesh warp, and the AOV bundle for S3

**Written 2026-08-16** by the advisor seat at the open of the session, before any
measurement. Companion: `docs/grok-consult-5-brief.md` — the S3 existence-proof compositor,
delegated to Grok as build round 2. One dispatched executor seat (Opus tier — task 2 is
instrument design, not instrument running), background, working `E:\AI\training\facet_E45\`.
This document is the dispatch; steering rulings are appended here in place, with dates.

## The two questions

**Q1 — the lead.** Is the twin-to-mesh correspondence locally warped beyond global
registration, at magnitudes that put samples across material boundaries? The prior
measurement (one view, yaw 45, silhouette-based) read global IoU 0.9203 with centroid offset
2.88 × 2.60 px — and per-tile offsets spanning −8..+6 px in x, −8..+8 in y, std 3.71 / 4.09,
with tiles pinned at the ±8 search limit. E41 measured defect texels a median 0.439 px from a
material boundary; a 4–8 px local displacement puts a sample across one. ⚠ **The instrument
that produced those numbers is lost** — it survives nowhere on disk or in git (verified this
session: the numbers exist only in `docs/advisor-kickoff.md`). They are therefore a
hypothesis, not a baseline. The seat re-derives from scratch and treats agreement with them
as a continuity check, never a target.

**Q2 — the substrate.** Per-view G-buffers of the shipped state, so the S3 existence proof
can run the moment Grok's compositor lands, and so Q1's interior-correspondence leg has a
mesh-side signal. One bundle serves both: the depth/normal/position/surface-ID fields the
compositor consumes are exactly the fields the warp instrument needs for its mesh-side edge
maps.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Every emitted artifact carries a manifest: GLB sha256, tool version, open3d version (the identity-envelope law — every open3d number in this repo is against `0.19.0+241aaee`), numpy version, cam.json copies, twin-mapping evidence. Not 3: the new tools have no CI anchor until the fold. |
| ANDON_AUTHORITY | 3 | Gate A halts task 1 before any AOV is emitted; Gate C halts task 2 before any real measurement. Halts `raise`, never bare `assert` (E21 Ruling 2 / E22). |
| NAMED_COMPENSATORS | 3 | All writes are new files under `E:\AI\training\facet_E45\` (not in git) or new files in `tools/` + `tests/` (compensator: `git clean -f <paths>`, owner = advisor). No irreversible external call anywhere in either task — no publish, no generation, no credit spend. |
| DECOMPOSE_BY_SECRETS | 3 | Three modules, three secrets: the emitter owns the state layout and camera conventions; the warp instrument owns the correspondence method; Grok's compositor owns weighting and consistency. The boundary is the array contract in the Grok brief. |
| UNCERTAINTY_GATED_HUMANS | 2 | No warp pass-threshold exists and none is invented — distributions and pictures go to the Director (the suspend-rather-than-invent precedent). Not 3: no mid-task uncertainty trigger beyond the gates. |
| EXTERNAL_VERIFIER | 2 | The compositor is built outside by a different model family against a self-contained brief and ships its own synthetic self-test; the warp instrument validates against constructed truth before touching real twins. Not 3: no second seat re-measures task 2. Remediation: if the warp reads decisive on any view, a second seat re-measures that view before any ruling. Owner = advisor. |

## Premises, marked (the E29 law: say which you measured and which you assumed)

**MEASURED this session, by this advisor:**

- The shipped state is `E:\AI\training\facet_E08\ARMB\` — E44's own scripts read
  `ARMB/out/W3_final.glb` (22,902,332 bytes) as "the shipped mesh".
- `state\` holds exactly 8 job dirs: `job_y+000_e+55, job_y+045_e+00, job_y+090_e+00,
  job_y+135_e+00, job_y+180_e+55, job_y+225_e+00, job_y+270_e+00, job_y+315_e+00`.
- Per-job `cam.json` fields: `{yaw, el, v_ext, h_ext, bmid, W, H}`; the y+000 job reads
  `el 55.0, v_ext 1.1969748723526452, h_ext 0.8790284218839738, bmid ≈ (−0.0008, 0.0022,
  0.0029), W 752, H 1024`.
- `twins\twin_0..7.png` are all 752×1024 RGB; `twin_2` and `twin_6` have
  `_REJECTED_seed770700` siblings. `state\job_*\render.png` is 752×1024 RGB;
  `state\job_*\hit.png` is 752×1024 mode L.
- `masks\` holds `w3clay_0..7.png` + `silhouettes.json` — the shipped silhouette masks;
  `project_twins.py`'s own docstring cites `silhouette_masks.py --anchor, 0 differing px at
  views 0 and 4` against them.
- Flat-ring camera axes: `tools/project_twins.py:416` `cam_axes` — `dtc = (sin θ, −cos θ, 0)`,
  `right = (cos θ, sin θ, 0)`, `up = (0,0,1)`, with the ±1/0 snap that is load-bearing.
  **`cam_axes` is yaw-only — it does not model the two el=55 views.** The general elevated
  basis is `tools/bake_hero_fuse.py:92` `cam_basis(el_d, az_d)`.
- A canonical-frame transform appears at `bake_hero_fuse.py:83`:
  `v = stack([x, −z, y]) / vmax * 0.5` (glTF Y-up → canonical Z-up, maxabs-scaled).
- `tools/callieri_border.py` v1.0.0 public API: `depth_edge_mask(depth, relative_jump=0.05,
  silhouette=None)`, `mixed_depth_reject(...)`, `border_weight(depth, silhouette,
  relative_jump=0.05)`, `facing_weight(normal, exponent, view_dir=(0,0,1))`, plus fixtures
  and a selftest. Depth convention: float32, `+inf` background.
- No tile-offset / correspondence instrument exists anywhere in `tools/` (enumerated:
  the only NCC-adjacent hit is `e13_anchor_check.py`, the spiral-law guard).
- `project_twins.py` is **not import-safe** (argparse + RaycastingScene at module scope);
  the established repo pattern is verbatim copy with citation (E41's fixtures did this).

**ASSUMED — the seat verifies each before building on it:**

- The twin_i ↔ job/yaw mapping. Candidate evidence: `masks\silhouettes.json`,
  `out\run_log.jsonl`, the `w3clay_i_control/mask` pairing in `twins\`, and the stroke
  workflow filenames (`stroke_1_y+090 … stroke_8_y+180_e+55`). Pin it from at least two
  independent sources; a wrong mapping poisons every downstream number.
- `hit.png` semantics (raw raycast silhouette vs something dilated). Diagnostic only —
  Gate A anchors on `masks\w3clay_*.png`, whose provenance is documented.
- That `E:\AI\training\facet_E42\check_mesh_match.py` holds the working GLB↔state
  reconciliation (it was written to check exactly that). Read it before deriving any
  transform; reuse verbatim with citation if it holds.
- That the elevated views' basis is `cam_basis`-style. **Do not trust this by reading** —
  Gate A settles it by reproduction.

## Task 1 — the AOV emitter (`tools/emit_view_aovs.py`, name at seat's discretion)

From `W3_final.glb` + the 8 `cam.json`s, raycast each view on its own pixel grid and emit,
per view, into `E:\AI\training\facet_E45\aov\`:

| array | dtype/shape | contents |
|---|---|---|
| `depth` | float32 (H, W) | `−(P − bmid)·dtc` at first hit; `+inf` at misses |
| `pos` | float32 (H, W, 3) | first-hit position, canonical frame; NaN at misses |
| `normal_world` | float32 (H, W, 3) | barycentric-interpolated vertex normals, unit, canonical frame |
| `sil` | bool (H, W) | first hit exists |
| `surfid` | int32 (H, W) | atlas texel linear index (`v_tex * 4096 + u_tex`) from the GLB's own UVs at the hit; −1 at misses |
| `weight_border` | float32 (H, W) | `callieri_border.border_weight(depth, sil)` |
| `reject` | bool (H, W) | `callieri_border.mixed_depth_reject(depth)` |

plus a copied `twin.png`, a per-view `cam` block `{right, up, dtc, bmid, h_ext, v_ext, W,
H}` in one `cams.json`, and `manifest.json` (hashes + versions + mapping evidence). The
projection contract these must satisfy (identical to the Grok brief, which is the consumer):

```
px = ((P − bmid)·right / h_ext + 0.5) · W − 0.5
py = (0.5 − (P − bmid)·up / v_ext) · H − 0.5
depth(P) = −(P − bmid)·dtc
```

**Gate A (ANDON, halts task 1):** before emitting anything, reproduce the shipped
silhouettes — the emitter's `sil` against `masks\w3clay_i.png`, all 8 views, **compared as
pixels, never as file hashes** (the PNG-hash law). The recorded precedent is 0 differing px
on views 0 and 4. Any nonzero count: report it per view with its spatial distribution and
HALT — do not tune the camera until it passes; the elevated views are exactly where a
flat-ring assumption will surface. `hit.png` comparison is reported as a diagnostic, not
gated.

**Self-consistency check (can-fail by construction on the elevated views):** every valid
`pos` reprojected through its own view's contract must land within 0.51 px of its own pixel
centre; report the max.

**Tests ride the commit:** hermetic tests for basis construction (flat yaws must reproduce
`cam_axes`' snapped literals), the projection round-trip on synthetic geometry, and the
surfid mapping. Run pytest with `--basetemp` on scratch (the known Windows
PermissionError). New test counts are reported for the advisor to reconcile against the T34
pins at fold — the seat does not edit the pins.

## Task 2 — the warp instrument (after task 1's bundle exists)

Per view, two correspondence legs, both per-tile over a search window:

- **Silhouette leg** (the lost measurement, re-derived): per-tile offset between the twin's
  figure/edge band and the mesh silhouette's, masked NCC or phase correlation — seat's
  choice, justified.
- **Interior leg** (the reason silhouette agreement is not enough): mesh-side edge map =
  `depth_edge_mask(depth)` (+ normal-discontinuity creases if useful) — interior occluding
  contours: arm against torso, sword against body. Twin-side = gradient magnitude of the
  twin (luminance and chroma). Per-tile offset where the mesh-side edge density clears a
  floor derived from that tile's own edge count (**no global constant governing a local
  feature**), with the floor and the covered-area fraction reported. The instrument's scope
  is *tiles where both signals exist* — report that population explicitly; it is the object
  counted (the E31 law).

Window: start ±16 px, widen (×2, cap ±48) until no tile pins at the boundary; report the
pinned fraction per window size. Tile size and overlap: seat's choice, pre-registered
before any real measurement, with the yes/no interval stated per leg (what the instrument
reads on a known warp; what it reads on identity).

**Gate C (ANDON, halts task 2):** instrument validation on constructed truth before any
real twin is measured — inject known shifts (3–12 px, both signs, both axes) into a copy of
a real twin and read them back within 0.5 px; a null leg (twin vs itself, render vs itself)
must read ≈ 0 with high peak confidence. If validation fails, halt and report.

**Predictions before looking**, per view AND per leg separately (the conjunction law —
predict each clause, then the join), blind status disclosed. **No pass condition exists.**
Report distributions, spatial coherence (neighbour-tile agreement vs shuffled), pinning
fractions, magnitude vs the 0.439 px boundary-distance scale — numerator and denominator
separately. The one banned move: retuning tile size or floors after seeing real offsets.

**Pictures (the Director's standing rule):** per-view offset heatmaps and a quiver overlay
on the twin at native size; the interior-leg edge overlays (mesh edges over twin) at the
Director's zoom for at least yaw 45 and one elevated view.

## Out of scope

S4–S6, all E44 unwrapper arms (deferred behind S6 by the standing sequence), any
generation or cloud spend, and warp **correction** — the flow hook in Grok's compositor is
where a measured field would eventually be tested, not here. Task 2 measures; it does not
repair.

## Deliverables

`docs/experiments/E45-warp-and-aov-report.md` (seat-written, evidence only, no judging
words), `handoff.md` under the training dir **written early and kept current**, the AOV
bundle + manifest, the warp arrays + sheets, new tools + tests left uncommitted for the
advisor's fold.

## Dispatch record

- 2026-08-16 — dispatched as a background Opus seat at session open, together with Grok
  brief #5. The record server was recertified first (`record_build`, four legs, SERVING) —
  the previous session's final commit had left the served DB one commit stale.
