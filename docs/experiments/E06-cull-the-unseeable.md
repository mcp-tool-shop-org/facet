# E06 — Cull what cannot be seen

**Status:** SPEC — ready to run
**Author:** advisor session, 2026-08-04, on E05's Gate 0
**Priority:** highest. This is the diagnosis E05 produced.

---

## 0. Rules

Unchanged: no verdicts, no memory writes, stop at gates, FLAT for texture and `--clay` for
geometry, predictions before looking. Read [E05's Gate 0](E05-gate0.md) and
[E02's ruling](E02-ruling-gate1.md) first.

## 1. What E05 established

**49% of valid atlas texels are never visible from any of 46 exterior cameras.** Half the
surface the atlas pays for is not on the outside of the model.

Consequences, all measured:

| | |
|---|---|
| 8 cameras reach | 34.2% of the stage-1 hole set |
| 14 cameras reach | 35.9% — U2 was worth +1.7 points for six strokes |
| 46 cameras, no facing limit | **41.0%** — the exterior ceiling |
| commit funnel: visibility drops | **65.5%** of everything passing the facing test |
| widening facing 0.25 → 0.10 | +160,259 texels at stage 1, **9,706** reached the atlas |
| occlusion scale | median blocker **0.031** (3% of figure height); only 11.7% within one edge length |

The occlusion is **mid-scale** — folds, crevices, behind the beard, between fingers,
interior shells — not triangle-scale noise. And it explains the unwrapper result without
appealing to the unwrapper: charts cannot be large on a surface that is half interior.

**Adopted from E05, not an arm here:** native xatlas UVs (`--native-uv`). 923,466 texels
painted against 711,183, colourless-island hole texels down 14.2 points, speckle below A0
at two of three thresholds. `bake_hero_prep` must stop discarding the generator's atlas.

## 2. The question

**Does culling exterior-invisible faces before unwrapping fix coverage, atlas efficiency and
the artifact mechanism together?**

For a prerendered 2.5D deliverable, exterior visibility is the only visibility there is. A
face no camera can ever see is surface the pipeline pays for three times — texels in the
atlas, a hole in the map, and a dilation that bleeds into its neighbours.

## 3. Predictions — recorded before the run

Removing ~half the faces should:

- **roughly double** effective texel density on visible surface at the same atlas size
- **merge charts**, because the fragmenting interleaved invisible geometry is gone —
  expect islands well below U1's 16,684 and faces/island well above 17.2
- take brush share from 27% of holes to **65–70%**, because the unreachable half leaves the
  hole set entirely
- cut colourless islands sharply — an island is currently colourless largely *because* it is
  invisible

If islands do **not** merge after culling, the fragmentation has a second cause and that is
itself the finding.

> ### Amendment 1 (advisor, 2026-08-04, on Gate 0)
>
> **The gate as specified was blind to the operation's failure mode — advisor error.** I made
> silhouette IoU the load-bearing check on an operation whose defining risk is holes punched
> through *visible* surface. IoU cannot see that: the ray behind a removed face still hits
> geometry, so the pixel still reads as figure. On a mesh with a **0.297 hole clean through
> it**, IoU returned **1.00000 at all eight cameras**.
>
> The executor noticed before reporting, added a **first-hit depth** comparison, and it fired
> immediately — 262 px receding at yaw 225, 208 px at yaw 135. **Depth comparison is the gate
> from now on.** General form, now a repo rule: *a gate must test the operation's failure
> mode, not its success mode.*
>
> **Cause, measured:** a generic 46-camera sphere puts 12 yaws at 30° on the equator and
> therefore misses **six of the ten production cameras** — all four diagonals and both
> elevated. 228 faces visible from a production camera were culled; the ring dilation rescued
> 85 of 313. Union costs 0.08% (150,568 vs 150,340).
>
> **RULED — stop deleting faces; exclude them from the atlas instead.** The union fixes
> *this* camera set, but any future orbit reopens the same class of hole, and a guarantee that
> depends on nobody adding a camera is not a guarantee. Instead:
>
> - compute the visible set as now, **union'd with every production camera**
> - unwrap and pack **only** the visible faces
> - collapse unseen faces' UVs to a single shared texel
> - **never modify the geometry**
>
> Same benefit — texel density doubles on visible surface, and charts are computed on the
> visible subset, which is where 16,684 → 10,842 came from — with the risk eliminated rather
> than managed: the silhouette cannot change, a hole is structurally impossible, and a future
> camera sees flat grey instead of through the torso.
>
> **§4.3's "delete, then re-weld" is withdrawn.** The executor was right not to weld: trimesh
> stores UVs per-vertex where Blender stores them per-loop, so welding there endangers the
> native atlas adopted in E05. Under UV-exclude the mesh is untouched and the question
> dissolves.
>
> **Halting was correct** even though the remedy looked trivial — that is exactly the
> condition under which an earlier session improvised and hit the same gate harder.

## 4. Method

**Build `tools/cull_unseen.py`.** Input the welded, decimated mesh **before** any UV work.

1. **Visibility by exterior sampling.** Cast rays inward from a sphere of N cameras (start
   at 46, the E05 set; report sensitivity at 92). A face is *seen* if any ray's first hit
   lands on it.
2. **Dilate the seen set by one ring** before deleting. A face visible only through a narrow
   aperture may be missed by a finite camera sample; keeping its neighbours costs little and
   protects against sampling error. Report how many faces the ring adds.
3. **Delete unseen faces**, then re-weld. Export.
4. **ANDONs:** halt if the seen fraction is above 0.9 (the cull is doing nothing and the
   visibility test is wrong) or below 0.3 (it is eating real surface); halt if the silhouette
   from the eight production cameras changes by more than 1% IoU against the uncut mesh —
   **that is the load-bearing check**, since culling must be invisible from outside by
   definition.

**Then re-run the E02 pipeline unchanged** on the culled mesh with `--native-uv`: prep,
twins, `project_twins`, the eight strokes in spiral order, finalize, pack.

## 5. Arms

| arm | mesh | tests |
|---|---|---|
| **C0** | U1 (uncut, native UVs) | baseline — already measured at E05 Gate 0 |
| **C1** | culled, native UVs | the question |
| **C2** | culled, native UVs, 46-camera visibility recomputed *after* cull | does culling reveal surface that was previously shadowed by geometry now gone |

C2 is cheap and worth knowing: interior shells may have been occluding real exterior
surface.

## 6. Metrics — the E05 Gate 0 table, unchanged

islands · faces/island · atlas coverage · **holes closed by brush vs dilation** ·
colourless islands and their share of hole texels · speckle at 0.10/0.15/0.25 against A0's
2.43/1.18/0.30 · styled/reachable.

**Plus, new and specific to this experiment:** faces before/after cull, seen fraction,
ring-dilation additions, silhouette IoU against the uncut mesh from all eight production
cameras, and the **exterior-invisible texel fraction re-measured after culling** — that is
the number E05 put at 49%, and it should approach zero.

**Pass condition, stated as an absolute so it cannot move with a denominator** (the E05
error): **brush-painted texels must exceed U1's 923,466** *and* exterior-invisible texel
fraction must fall below 15%.

## 7. Gates

**Gate 0 — after the cull, before any texturing.** Report faces removed, seen fraction, and
silhouette IoU from all eight cameras. **If IoU moves more than 1% anywhere, halt** — the
cull is removing surface that shows.

**Gate 1 — the finished asset.** FLAT turnaround and head close-up beside **the E02 asset
and A0**, same framing and light. Prediction first. The Director's eye is the verdict.

## 8. Out of scope

Remeshing. If culling does not merge charts, remeshing becomes the next question with a
clean premise — but it is a geometry rewrite and must not be entangled with a cull
measurement. Also out: E03 head graft, E04 ship, subject P.

## 9. Standards compliance

**PIN_PER_STEP 3** — one change against a measured baseline; the E02 pipeline runs unchanged
downstream. **ANDON 3** — three numeric halts on the cull itself, and the silhouette-IoU
check is a direct test of the operation's defining property. **COMPENSATORS skip** — local
writes on a copy; the uncut mesh is never modified. **DECOMPOSE_BY_SECRETS 3** — the cull is
a standalone tool with its own gate, ahead of and independent of the texture stage.
**UNCERTAINTY_GATED_HUMANS 3** — Gate 0 is numeric and needs no Director time; Gate 1 is his.
**EXTERNAL_VERIFIER 3** — pass condition is absolute, numeric, and written before the run;
the aesthetic verdict is the Director's, against two assets he has already judged.
