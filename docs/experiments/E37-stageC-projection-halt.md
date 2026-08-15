# E37 Stage C — HALT: the projection reg-IoU ANDON fired on view 3, the re-rolled twin

**Seat:** executor · **Date:** 2026-08-15 · **Spend: 30 of 40 — unmoved, all local.**
Dispatch: [E37-ruling.md](E37-ruling.md) Ruling 11.

---

## 1. Ruling 11's chain ran clean up to the projection

| step | result |
|---|---|
| `smart_decimate --target 300000 --head-crop 432.8,47.5,591.5,196.3 --crop-res 1024` | **Gate W passed.** 993,795 → **299,986** scene faces; weld 710,959 → 496,644 verts, shells **31,301 → 32**, 46 degenerate faces dropped (0.0046%); every surviving face kept its exact UVs (993,749 checked); face rect protects 160,733/496,644 verts |
| **Ruling 11 step 2 — `maxabs` check** | **crop STANDS.** raw 0.500944555 → decimated 0.500948012, Δ 3.46e-06 (0.00069%). The four corners move **0.0005 / 0.0032 / 0.0005 / 0.0022 px** of a 1024-px frame. No re-derivation |
| **the 17-face loader class, re-checked post-decimate** | **did NOT fire.** trimesh reads **299,976** from the file and **Blender-on-import reads 299,976** — they agree. `smart_decimate`'s 299,986 was its *scene* count; the glTF export dropped 10 (its own "Mesh geometry_0 is not valid" warning). Measured with a fresh Blender import rather than inferred, because declaring the class fired on a scene number would have been a halt on the wrong operand |
| `cull_unseen` on the decimated GLB | **gate did not fire.** 148,062 visible / 299,976 (49.4%); unseen among first-hit **5 faces — 0.0035% by count, 0.0007% by AREA against a 0.50% limit**; worst recession 0.002225 over 2 px; IoU 1.00000 on all eight yaws (reported — the tool is explicit that recession gates and IoU does not) |
| `bake_hero_prep` | **built.** The ANDON that fired last run now passes: *"visible mask lines up with this mesh (max centroid deviation 5.96e-08)"*. Native UVs, no re-unwrap. Islands **13,722**; head islands 5,810; islands holding visible faces 7,619. Head UV-area share **0.6636** against a face-count share of 0.5217 (0.1798 before scaling). Packed UV area **6.37%** of the atlas. 151,914 unseen faces parked on one 10×10-texel patch |

For scale beside the recorded run, **not as a pass condition**: E33's prep reported 13,715 islands, head UV-area share 0.6161, packed 6.87%.

## 2. THE GATE, with its numerator and denominator

`project_twins.py:633`, the registration ANDON, on the eight-view projection of the amended
set:

```
ANDON: y+135.0: IoU(raw twin paint, exact silhouette) 0.7547 is below 0.80
       — the twin is registered to the wrong place. Every adjudicated view measures
       0.8329 or better; every measured registration failure sits at or below 0.578.
       Regenerate the twin against this mesh's control; do not tune this threshold.
```

**View 3 — one of the three re-rolls, seed 202608153.** No threshold was touched, nothing
re-run to get past it, and **no atlas was written**. Views 4–7 are **UNMEASURED**: the halt
stopped the run before them, which is what the gate is for.

| view | source | mesh silhouette | twin paint | reg-IoU | centroid dy | keyed OUTSIDE the silhouette |
|---|---|---|---|---|---|---|
| 0 | kept 770700 | 24.8% of frame | 23.0% | 0.9091 | **−0.1 px** | 956 px (1.10%) |
| 1 | **re-roll** | 24.4% | 24.4% | 0.8975 | **+13.9 px** | 4,790 px (5.22%) |
| 2 | kept 770700 | 14.3% | 15.5% | 0.8671 | **+38.9 px** | 6,331 px (10.84%) |
| **3** | **re-roll** | 24.3% | **29.3%** | **0.7547** | **+42.1 px** | — **FIRED** |
| 4–7 | — | — | — | **NOT RUN** | — | — |

⚠ **My own log was truncated on the first pass** — I piped the run through `tail -45` and lost
view 0's registration line, which is the exact failure this record names as its own family
(*a conclusion read off a truncated listing is not a measurement*). The run was re-executed
with **nothing changed**, captured complete to `stageC/project_run.txt` (52 lines), and
reproduced every figure identically. The table above is from the complete capture.

## 3. What the numbers attribute — measured, not inferred

**The mesh silhouette is not the variable.** `masks8/armwoodclay_3.png` (built on the RAW
mesh) bboxes 850 × 235; `project_twins` raycasts the **decimated, welded, culled** prep and
reports 849 × 234. The silhouette operand survived decimation to a pixel, so the drop is not
the new prep.

**Two instruments, one uniform offset and one outlier.** Stage B's reg-IoU came from
`t2_register_all.py`; this is `project_twins`' own fitted-background key. They differ, and
the difference is flat across three views:

| view | source | Stage B | projection | delta |
|---|---|---|---|---|
| 0 | kept | 0.9559 | 0.9091 | −0.0468 |
| 1 | re-roll | 0.9404 | 0.8975 | −0.0429 |
| 2 | kept | 0.9116 | 0.8671 | −0.0445 |
| **3** | **re-roll** | 0.9440 | **0.7547** | **−0.1893** |

**Views 0/1/2 drop by −0.0447 with a spread of 0.0039 — that is the instrument. View 3 drops
by −0.1893, 4.2× that.** Whatever the instrument change costs every view, view 3 carries an
additional ≈ −0.14 that is view 3's own.

**The signature points at painted background, and the tool says so itself.** `keyed OUTSIDE
the silhouette` runs 956 → 4,790 → 6,331 px across views 0/1/2 and the centroid drifts
downward with it (−0.1 → +13.9 → +38.9 px). At y+090 the tool raised its recorded diagnostic
NOTE: *keyed twin bbox 848×247 exceeds the mesh silhouette's 849×129 by more than 25% … most
likely a cast shadow.* View 3's twin paints **29.3% of frame against a 24.3% silhouette** and
its bbox is 850 × 367 against 849 × 234 — **57% wider than the figure**.

**This coheres with the wash guard rather than contradicting it.** View 3's re-roll was the
arc's largest tonal outlier (C\* 29.98 → **46.24**) and the only view whose dark census got
worse (8/49 → **34/247**). The same seed that removed the lower-back dent produced the most
background-contaminated frame of the eight.

## 4. What is NOT concluded here

The Stage-B and Stage-C reg-IoU numbers are **both valid measurements of different things** —
different keys over the same twin — so the Stage-B figures are not withdrawn and Ruling 8's
selection is not disturbed. What is new is that the projection's own key, on the projection's
own silhouette, reads view 3 below the floor.

**Whether the cause is the re-rolled v3 specifically or something view-3-shaped in the route
is not settled by what has been run.** One diagnostic would attribute it and it is local and
free: **project the REPLACED v3 (`s770700/twin_v3.png`) under byte-identical settings to a
scratch `--out`.** If it clears 0.80, the re-roll is the cause and the remedy is v3's second
roll — which Ruling 8 clause 3 makes a **result that returns to the Director**, not a third
roll. If it also fires, the cause is upstream of both twins.

**That diagnostic is proposed, not executed.** It changes an input after a gate fired, and
this record was paid for by a session that changed something and re-ran. The gate stays at
0.80; nothing proceeds past it either way.

## 5. Mechanics

Watchdog **ADVANCING** on two reads (14:33:22.317 → 14:33:37.372, and 14:45:06 → 14:45:08 at
the second run; VRAM 6,892 of 32,607 MiB). All Blender calls `-b -P` through PowerShell —
three this stage, zero GUI sessions. Every receipt under `facet_E37\stageC\` and
`facet_E37\handoff\`, outside every protected tree. CI `31900743786` green, recorded.

Receipts: `stageC/perf_300k.glb` · `decimate_report.json` · `seen_faces_300k.{npy,json}` ·
`cull_300k.json` · `prep_bake/` (`prep_uv.glb`, `pos.npy`, `nor.npy`, `mask.npy`,
`meta.json`) · `project_run.txt` · `handoff/e37_maxabs_check.{py,txt}` ·
`handoff/e37_blender_facecount.py`.

**No atlas exists. No `performer_v3.glb` exists. Spend 30 of 40.**
