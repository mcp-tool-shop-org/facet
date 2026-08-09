# E30 predictions — per-profile anchor gates for W3, the galleon and the dragon

**Committed before the first replay.** Nothing in this file was written with a replay result
on disk. The tree manifest was taken first (7,312 files, 17,072,807,610 bytes — E23's count
reproduces exactly); enumeration of the recorded trees is complete; **no tool has been run
against a recorded tree.**

---

## The unit, and the denominator it sits in

**One anchor = one replayable recorded stage meeting all four of T7's properties**: the
recorded artifact's own bytes as the comparand (no sha256 literal in test code), the recorded
tree read in place and written nowhere, the input re-hash leg, and the two markers.

**The denominator is 15**, and it is derived by measurement rather than by subtraction:

- The sword's anchors are **T7–T12**. Six *tests*, but only **five are per-subject shapes** —
  T12 (`mesh_stats`) already runs all four subjects in one test and is not this arc's work.
- The five shapes are: **finalize** (`texpass_finalize`), **ceiling** (`e08_ceiling`),
  **elevated** (`e12_elevated`), **projection** (`project_twins`), **commit**
  (`texpass_iter commit`).
- 5 shapes × 3 subjects (W3, galleon, dragon) = **15 candidate anchors**.

**A wider population exists and is named rather than silently dropped.** Each subject's tree
also carries diagnostic sidecars with recorded outputs — `blade_band_8cam.json`,
`brush_reach.json`, `keyed_outside.json`, `silhouette_agree.json`, `palette_gate*.json`,
`offsurface.json`, `thin_curve.json`, `contact_mask.json`, `w1_coverage.json`,
`layer_export.json` and more. Counting every `.json` under the three subjects' trees gives
145 / 242 / 242, but that count is dominated by per-job `cam.json` route sidecars, which are
inputs rather than gradeable outputs. **This arc scopes to the five sword-shaped route
stages.** That is a declared scope with the remainder enumerated, not a scope obtained by
subtracting one number from another.

⚠ **E27 Ruling 5 applies and was checked before these numbers, not after.** The property
"has a replayable recorded invocation with a recorded output" is **not defined for every
member**: `e12_elevated` is an E12-era instrument, so the two subjects whose arcs predate it
(W3 at E06/E08, the galleon at E04) have **no recorded elevated output at all**. That was
measured — `find` over both trees returns nothing — not assumed.

## Blindness disclosure, per row

The trees have been **enumerated** (which inputs and which recorded outputs exist, and their
sha256s). No tool has been **run**. So:

- **P1, P2, P4 are NOT blind** on artifact existence — I have looked at what is on disk. They
  remain predictions about whether a *recorded invocation* can be recovered for each stage,
  which I have not yet established for any of them.
- **P3 and P5 are BLIND.** No replay has run.

**No calibration haircut is applied to any number below.** E22's P18 halved an untutored
estimate on this repo's own "densities run 2× high" lesson and measured 175 against 4; the
ritual moved the answer away from the truth. These are the numbers I actually believe.

---

## P1 — total anchors buildable across the three subjects

**Point estimate: 11 of 15.  Band: 8–13.**  *(not blind on existence; blind on invocation
recovery)*

*Buildable* means all four T7 properties can be met and the test can be written and run. It
does **not** mean the replay reproduces — that is P3.

Reasoning, per shape:

| shape | W3 | galleon | dragon | buildable |
|---|---|---|---|---|
| finalize | state (647,624 holes) + `facet_E06/C1/prep` → `ARMB/out/atlas_final.png`; **mode not yet recovered** | state (1,750,006 holes = its own `finalize.json`) + `E04_shipprep` → `out/galleon_final.png`; mode `atlas_flood` | `run/state` (1,710,180 = its own `finalize.json`) + `E12_prep` → `run/dragon_final.png`; mode `surface_aware` | **3** |
| ceiling | `facet_E08/gate0/ceiling.json` | `E04_armT72/ceiling/ceiling.json` | `E12_prep/ceiling.json` | **3** |
| elevated | none recorded | none recorded | `E12_prep/elevated.json`, which records its own `glb`/`up_min`/`base_yaws` | **1** |
| projection | 8 twins → `ARMB/stage1_8cam.*` | 8 twins → `E04_armT72/stage1/stage1_8cam.*` | twins → `E13_stage1/A1_stage1.*` | **3** |
| commit | no recorded pre-state | `bindcheck/` (pre + its own job) → `selftest_state/` | no recorded pre-state | **1** |

## P2 — per subject

**Unit as above. Denominator 5 per subject.**

| subject | point | band |
|---|---|---|
| **W3** | **3** of 5 | 2–4 |
| **galleon** | **4** of 5 | 3–5 |
| **dragon** | **4** of 5 | 3–5 |

W3 is the thinnest and the reason is structural, not neglect: its arc is the oldest, it
predates `e12_elevated` entirely, and its stroke lane left no separately-recorded pre-commit
state — `state/atlas.prev.png` carries the previous *atlas* but `holes.png` and
`styled_mask.npy` in that directory are post-commit, so the commit's true input state is not
on disk. The galleon is the richest because its E04 arc recorded a `bindcheck` pre-state
beside its own job, which is exactly T11's shape.

## P3 — how many replays reproduce byte-identically on the first run

**Point estimate: 7 of 11 buildable.  Band: 4–10.**  *(BLIND — no replay has run)*

The split I expect, and why:

- **finalize ×3 — expect all 3.** `texpass_finalize` reads `--state` and writes only
  `--out`/`--json`; T7 has it reproducing across two tool edits already.
- **ceiling ×3 — expect all 3 on the numbers.** T8 established that E16-6's repair collapses
  the settings blocks when the floors are equal, so the *shape* of the recorded JSON will not
  match for the galleon and the dragon (both show the floors-equal signature: their
  "production 0.45/0.18" and "uniform 0.45" blocks carry identical numbers). W3's two blocks
  **differ** (N2 1,265,391 against 1,039,711), so W3's recorded run had genuinely unequal
  floors and needs a different invocation from the other two. Reachable counts should
  reproduce exactly in all three; the block structure will not, for two of them.
- **elevated ×1 — expect it to need `--exact-grid`**, and to reproduce with it. E16-7 changed
  the default grid derivation, and the tool's own help names `--exact-grid` as the way a
  pre-E16 run is reproduced.
- **projection ×3 — expect 0 to 2.** This is where I expect the misses. `project_twins` has
  been repaired *after* every one of these three recorded runs: E16-8 replaced the
  corner-median background reference with the fitted border ring, and E16-10 extracted
  `local_thickness`. T10 works because E16-8 proved byte-identity **on the sword's twins**;
  nothing proves it on these three. A key change that is a no-op on one subject's backdrop
  need not be a no-op on another's.
- **commit ×1 — expect it to reproduce.** T11's shape, and the galleon's `bindcheck` pre-state
  is a genuine snapshot rather than a reconstruction.

## P4 — how many stages are NOT anchorable, and the dominant reason

**Point estimate: 4 of 15.  Band: 2–7.**  *(not blind on existence)*

**The dominant reason is a missing recorded OUTPUT or a missing recorded INPUT STATE — not a
missing invocation.** Split as I expect it:

- **2 — no recorded output exists for the stage at all** (`e12_elevated` on W3 and on the
  galleon). Their arcs predate the instrument.
- **2 — no recorded pre-commit state exists** (W3 and the dragon). `atlas.prev.png` is one
  file of the three a commit needs; `holes.png` and `styled_mask.npy` are overwritten in
  place by the commit that produced them.

## P5 — will any anchor need the pixel tier rather than the byte tier?

**Prediction: NO. 0 of the buildable anchors need the pixel tier to render a correct
verdict.**  *(BLIND)*

Named before looking, as the dispatch asks. **What would make this false:**

1. **A compared artifact that is a RENDER.** Both of this repo's false halts were on Blender
   output, where encoder metadata moves run to run. Every artifact in the 11 above is an
   *atlas* or a *JSON*, written by PIL from a numpy array inside the tool's own process — not
   a render, and not passed through a second encoder.
2. **A recorded artifact that was re-encoded after its run.** The sword's `s1b/atlas.png` is
   exactly this case: E14 Ruling 28d's collar repair rewrote it, which is why T11 compares
   against the sidecar's `atlas_sha256_before` and not the file. If any of these three
   subjects carries a comparable post-hoc rewrite, its anchor needs the same treatment or the
   pixel tier. **I have not checked for one**, and that is the specific way this prediction
   can fail.
3. **A PNG written by a different PIL version than the recorded run's.** This would move the
   bytes of a pixel-identical atlas. The E04 hardware-anchor reading is the shape to look for
   if it happens: a *uniform* residual across every structure is two float kernels; a
   structural difference concentrates.

If the byte tier says DIFFERS anywhere, `tools/verify/anchor_compare.py` decides which tier
rendered the verdict, and the report will say which one it was.

---

## What this file does not predict

- Whether any anchor's failure is a defect in the recorded asset or in the tool that moved
  underneath it. That is a ruling, not a measurement.
- The wider diagnostic-sidecar population named above. It is enumerated, not scored.
- Anything about the sword. T7–T12 exist and re-deriving them is out of scope.
