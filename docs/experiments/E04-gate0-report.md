# E04 Gate 0 — three clays, three meshes. HALT: the Director designates.

**Executor session, 2026-08-04.** All three staged concepts reconstructed locally, welded,
measured, and rendered `--clay` beside their source at full size. **`gate_mesh.py` did not
run**, per the dispatch and `profiles/ship.json`'s `mesh_gate: none`.

**This document ranks nothing.** Which ship is *the* ship is an outcome call and it is the
Director's. Three sheets are in front of him and I am stopping.

---

## 1. Environment, reported before the GPU work rather than after

**The watchdog was stale at session start** — heartbeat 2.77 min against a 15 s threshold,
its log recording *"previous watchdog died hard."* Restarted and verified alive at 0 s
before anything else ran.

**E04 Ruling 4 asked what killed it. The answer is worse than a crash, and it is a real
defect.** `_watchdog_KILL.log` for 2026-08-04 carries **153 ABORT lines**, a continuous burst
from 09:12:44 to 09:17:31 — five minutes of VRAM pinned at **31,851–31,903 MiB against the
31,200 ceiling** — and every one of them ends:

```
ABORT — VRAM 31885MiB>=31200 — wsl[Ubuntu] not running, skipped
```

**The watchdog detected the breach 153 times and killed nothing**, because its kill list is
an allow-list — four named Windows venvs plus one WSL trainer — and whatever held 31.9 GB
was not on it. The mechanism works when it matches (the log holds `killed win python PID(s):
31444,32200` from an earlier date); it simply had no applicable target. Neither
`_watchdog_DEAD` nor `_watchdog_TRIPPED` exists, which is consistent with the documented
hard-kill failure mode: a hard kill cannot write its own sentinel.

**Reported, not fixed** — the watchdog is not in this dispatch's scope and a protection
process is not something to redesign mid-task. It is alive now and Task 3's peak was
**5.6 GB**, nowhere near the ceiling.

**A second environment finding, repaired.** The first reconstruction attempt failed all
three with `ModuleNotFoundError: No module named 'trellis2'`. The package is **not installed
in `trellis2-env`** — it lives at `E:\AI-Models\TRELLIS.2-repo\trellis2` and used to reach
`sys.path` through the retired `trellis-sprite-pipeline` repo, which the studio constitution
records as deleted from the org. The repair is a `PYTHONPATH`, not a version change, and it
is written into the runner with the reason.

**Recorded rather than asserted:** with `ATTN_BACKEND=sdpa` and `SPARSE_ATTN_BACKEND=sdpa`
both set, `trellis2` still reports `Conv backend: flex_gemm; Attention backend: flash_attn`
at import. **What ran is what the log says, not what was requested.** No anchor is harmed —
this is a new subject with nothing to reproduce — but the next session should not read
E02's recorded `sdpa` as describing this run.

## 2. The runs

TRELLIS.2 `1024_cascade`, local, watchdog verified. `mesh_character.py`'s `run()` signature
records `seed: int = 42` as its default and the tool exposes no seed flag, so all three ran
at seed 42 — the same seed E01/E02 recorded for W3.

| candidate | source | out | wall | peak VRAM | exit |
|---|---|---|---|---|---|
| 00004 | `galleon_clay_p1_00004_.png` | `galleon_00004_raw.glb` 40.8 MB | 141 s | 4.4 GB | 0 |
| 00005 | `galleon_clay_p1_00005_.png` | `galleon_00005_raw.glb` 43.2 MB | 125 s | 5.6 GB | 0 |
| 00006 | `galleon_clay_p1_00006_.png` | `galleon_00006_raw.glb` 40.0 MB | 116 s | 4.6 GB | 0 |

```
mesh_character.py --image <clay> --out <glb> --ptype 1024_cascade
  PYTHONPATH=E:\AI-Models\TRELLIS.2-repo  HF_HOME=E:\AI-Models\hf-cache
  ATTN_BACKEND=sdpa  SPARSE_ATTN_BACKEND=sdpa   (see §1 — flash_attn is what loaded)
```

## 3. `mesh_stats` — measured identically on all three

Welding happens inside `mesh_stats` (`merge_vertices(merge_tex=True, merge_norm=True)`),
which also reports the unwelded count beside the real one, so the dispatch's *"weld →
mesh_stats"* is satisfied in-tool rather than by a separate pass.

| | **00004** | **00005** | **00006** |
|---|---|---|---|
| faces | 969,483 | 963,509 | 939,112 |
| verts | 474,154 | 467,823 | 465,569 |
| **shells (welded)** | **237** | **274** | **512** |
| largest shell | 0.8796 | 0.9229 | 0.9285 |
| shells (unwelded) | 39,233 | 52,411 | 31,007 |
| watertight | False | False | False |
| extent (Blender x,y,z) | 0.4672, **1.0017**, 0.8996 | **1.0019**, 0.6022, 0.9208 | **0.9690**, 0.4969, 0.9312 |
| **widest horizontal / height** | **1.114** | **1.088** | **1.041** |

**Not reported, deliberately:** `face_rect_density`, `face_rect_faces`,
`face_curvature_var` and `curv_radius`. Those columns are computed inside a **front-view
face rect** — they measure "is there a face there" and have no referent on a ship.
`profiles/ship.json` records `head_rect_metrics: false` for exactly this reason, and
`mesh_stats` printed its `vertical extent is not the largest — the front-view rect may not
be on the head` warning on all three, which is the character instrument correctly noticing
it is not looking at a character. Quoting a curvature variance here would be the E07 error
in a new costume: a number that cannot mean what its name says.

### Two observations offered as data, with no verdict attached

**Shell counts run 237 / 274 / 512 against a character's 40–191.** E01 measured four fresh
W3-family reconstructions at 40–191 components with 92–98% of faces in the largest shell.
These sit at 237–512 with **88.0 / 92.3 / 92.9%** in the largest. The concepts make the
likely cause visible — standing rigging, stays and yard lines are thin disconnected
filaments, and a reconstructor returns each as its own island. Whether that matters is a
downstream question about welding and decimation, not a quality ranking.

**All three measure wider than tall** — 1.114, 1.088, 1.041 — which is the first *measured*
support for the design note's predicted `fit_axis: width`. It is far less dramatic than the
staged frame's 1.188 suggests, because the masts are nearly as tall as the hull is long.
`profiles/ship.json` is updated with these three measurements; the value itself stays
suspended until one of them is *the* ship.

**The extents are not in a common orientation.** 00004's widest horizontal axis is Blender
**y**; 00005's and 00006's is **x**. The three concepts point their bows different ways, so
"view 0 = front" will not mean the same thing on all three. That is a `--yaw-offset` question
for whichever is designated, and `normalize_mesh.py`'s docstring already argues the camera
should be rotated rather than the mesh (`to_mesh()` destroys authored vertex normals).

## 4. The sheets

One per candidate, **full size, never a contact sheet** — the defects that decide acceptance
in this repo are invisible at thumbnail scale. Source concept on the left at render height,
eight `--clay` views on the right. `--clay` by standing rule: texture hides geometry, and
there is no texture here to hide behind.

```
E:\AI\training\facet_next\E04_gate0\GATE0_candidate_00004.png   7072 x 2192
E:\AI\training\facet_next\E04_gate0\GATE0_candidate_00005.png   6944 x 2192
E:\AI\training\facet_next\E04_gate0\GATE0_candidate_00006.png   6752 x 2192
```

**The render frame is measured, not inherited** — which is the profile work paying off
immediately. `turn_render` fits `ortho_scale = size.z * 1.204` and Blender maps that to the
*larger* render axis, so the character's 752×1024 portrait frame would crop any hull wider
than 0.884× its own height. All three are. The driver measures each mesh's bbox and picks a
frame that contains it: **1152×1024 / 1120×1024 / 1072×1024**. A character default would
have silently cut the bowsprit off every sheet.

## 5. What was NOT done

- **`gate_mesh.py` did not run** on any of the three. Its head-and-shoulder logic is
  meaningless on a ship; `profiles/ship.json` records `mesh_gate: none` as a decision.
- **No decimation, no UV work, no atlas, no twins, no texture.** Gate 0 is the route's first
  stage and the dispatch forbids scaffolding past it.
- **No candidate-calibrated threshold was armed.** The palette bands, the IoU halt and the
  bbox tolerance are W3 data; all three remain suspended in `ship.json` with the reason.
- **No profile value was written from these meshes** beyond recording the three measured
  extents as observations. Framing, cameras and thin-policy land after designation, measured
  from the designated mesh — next dispatch, not this one.

## 6. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every command, env var, wall time, peak VRAM and exit code logged per mesh in `recon.log`; the seed recorded from the pipeline's own signature; the backend recorded as what loaded rather than what was requested |
| ANDON_AUTHORITY | **3** | Halting at the designation gate with three sheets and no recommendation. The watchdog was verified alive before GPU work and its 153 no-op ABORTs are surfaced rather than passed over |
| NAMED_COMPENSATORS | **3** | New files only, all under `facet_next/E04_gate0/`; nothing pre-existing touched; no publish, no spend, no irreversible call |
| DECOMPOSE_BY_SECRETS | **3** | The render frame is derived per mesh instead of inherited, which is Task 2's whole point exercised on its first real subject; the character-only stats columns are named and excluded rather than quietly printed |
| UNCERTAINTY_GATED_HUMANS | **3** | The sheets are the checkpoint, full size, concept beside geometry, with the caption stating that they rank nothing |
| EXTERNAL_VERIFIER | **2** | `mesh_stats` measures any mesh identically and its character-specific warning fired correctly on all three, which is the instrument checking me. Gate 0's verifier is the Director's eye. `skip:` on a second model, as the dispatch allows |

---

**HALT. Three sheets, no ranking, no scaffolding past Gate 0.** After designation the
advisor authors the galleon's identity fixture and the ship profile's measured values follow
from the designated mesh.
