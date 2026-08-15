# E37 Stage C — HALT: the prep ANDON fired on a 17-face loader disagreement

**Seat:** executor · **Date:** 2026-08-15 · **Spend: 30 of 40 — unmoved.** Everything below
is local and free. Dispatch: [E37-ruling.md](E37-ruling.md) Ruling 10.

---

## The gate, with its numerator and denominator

`bake_hero_prep.py:134`, the visible-mask shape guard — the one whose comment says excluding
the wrong faces is *"a failure with no visible symptom until the atlas is already wrong"*:

```
AssertionError: ANDON: visible mask has (993812,) entries for 993,795 faces
                — it was built against a different mesh
```

| | |
|---|---|
| mask entries (`cull_unseen`, trimesh) | **993,812** |
| faces Blender's glTF import sees | **993,795** |
| **gap** | **17 faces — 0.00171% of 993,812** |

The run halted. No parameter was changed, nothing was re-run to get past it, and no atlas
exists.

## What caused it — measured, and it is not what I first suspected

`handoff/e37_facecount_gap.txt`. My leading hypothesis was that Blender's importer drops
degenerate triangles trimesh keeps. **Measured, that is false:**

| | |
|---|---|
| trimesh, `process=False`, unwelded | 993,812 |
| trimesh, **welded** (`merge_vertices`) | **993,812 — the weld moves 0 faces** |
| Blender glTF import | 993,795 |
| repeated-vertex triangles in the welded mesh | **0** |
| zero-area triangles | **0** |
| triangles with area < 1e-12 | **0** |

**There is nothing degenerate to drop, and welding removes nothing.** Two loaders simply
disagree by 17 faces on the same file. Nothing in this record had measured that before.

## The chain omission this exposes, and the mechanism that connects them

Ruling 10 gives Stage C's step 0 as `cull_unseen → bake_hero_prep`. **The recorded chain has
a step in front of both**, and E33 documents it as a gate rather than a convenience —
[E33-the-first-performer-through-the-route.md](E33-the-first-performer-through-the-route.md):

> **W — weld** · inside `smart_decimate.py` · its own asserted invariants on the weld and on
> UV survival. `--no-weld` is not used

and its recipe line: `smart_decimate.py --target 300000 --head-crop 438,44,588,182
--crop-res 1024`, producing the 299,956-face mesh E33's prep then packed.

**The two findings are one mechanism.** `smart_decimate.py` imports through Blender
(`:75`) and **exports a new GLB through Blender** (`:235`). After it runs, the file on disk
is Blender-authored and the two loaders agree on the face list. E33 and E34 never met this
gap because `cull_unseen` always ran on a post-`smart_decimate` GLB. I ran it on the **raw
TRELLIS reconstruction**, which puts a trimesh-counted mask against a Blender-counted mesh.

So the 17 faces are not a defect in either loader to be worked around — they are the symptom
of running the chain one step early, and **the ANDON caught exactly what it was built to
catch.** It is also worth recording plainly that this failure mode is invisible on a
Blender-authored mesh and therefore could not have surfaced until a seat fed the chain a raw
reconstruction.

## What is now known good, and what is void

| artifact | status |
|---|---|
| head world box, `handoff/e37_head_box.json` | **stands** — derived per Ruling 10 from the neck-bounded rects (crown→neck 89–215 front, 87–223 profile), faces-in-box 153,866 / 993,812 = 15.482%, the two views' Z ranges disagreeing by 0.0094 of height |
| projected crop, `handoff/e37_head_crop.json` | **stands** — `432.8,47.5,591.5,196.3` at `--crop-res 1024 --bound 0.55`, this mesh's own `maxabs` **0.500944555**. 158.7 × 148.8 px against E33's 150.0 × 138.0, so inheriting E33's rect would have been wrong by 6–8% in each dimension. A four-corner round-trip ANDON through the inverse projection passes to 1e-9 |
| `stageC/seen_faces.npy` | **VOID as an operand** — built against the raw mesh. Its numbers remain a valid record *of the raw mesh*: 498,880 visible of 993,812 (50.2%), gate at 0.0019% of visible area against a 0.50% limit, worst recession 0.000593 over 0 px, IoU 1.00000 on all eight yaws (reported, not the gate — the tool is explicit that recession gates and IoU does not) |
| `stageC/prep_bake/` | **does not exist** — the halt preceded any write |

⚠ The crop rect was derived against the **raw** mesh's `maxabs`. `smart_decimate` welds and
decimates but does not recentre or rescale, so `maxabs` is expected to carry — **expected, not
measured**, and it is re-checkable for free against the decimated GLB before the crop is used
again.

## Why this returns to the seat above rather than proceeding

The repair is not a parameter change — it is running the recorded chain — so a case could be
made for simply continuing. **One thing in it is a decision I should not take alone:**
`smart_decimate --target`. The tool's default is 120,000; E33 chose **300,000** for its mesh;
this raw mesh is 993,812. That number sets the face count of the asset that gets delivered,
and Ruling 10's step-0 text does not contain it because the step was not in it.

The executor rule is also unambiguous — *stop at every gate, never improvise past one* — and
one arc in this record was paid for by a session that changed something and re-ran.

**The single open question:** `--target` for `smart_decimate` on this mesh. Everything else
in the corrected chain is recorded:

```
cand_s987654.glb (993,812 f)
  -> smart_decimate --target <?> --head-crop 432.8,47.5,591.5,196.3 --crop-res 1024   [Gate W]
  -> cull_unseen  (tool defaults, unprofiled)                                          [Gate C]
  -> bake_hero_prep --res 4096 --crop 432.8,47.5,591.5,196.3 --visible-mask ...
  -> project_twins (8 views, amended set) -> fill -> pack -> performer_v3.glb
```

## Mechanics at this seat

Watchdog **ADVANCING** on two reads (heartbeat 14:33:22.317 → 14:33:37.372; VRAM 7,035 of
32,607 MiB, 24,165 below the ceiling). CI **`31900743786` green** — recorded as Ruling 10
asks. Every receipt under `E:\AI\training\facet_E37\handoff\` and `\stageC\`, outside every
protected tree. Tree clean at `52cdfe3` before this document.

Receipts: `handoff/e37_head_box.json` · `e37_head_crop.json` · `e37_head_crop.txt` ·
`e37_project_head_crop.py` · `e37_facecount_gap.py` · `e37_facecount_gap.txt` ·
`e37_head_rows.py` · `e37_head_rows.txt` · `stageC/seen_faces.{npy,json}` · `stageC/cull.json`.
