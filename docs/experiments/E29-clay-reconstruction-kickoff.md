# E29 — does a clay mesh reconstruct better than a concept mesh?

**Written by the advisor, 2026-08-09**, at the Director's sequencing (*"Let's start task
three, then E29"*). Halts at `E29-clay-reconstruction-report.md`; the advisor rules at
`E29-ruling.md`.

---

## The question

**Stage 0 exists. Its benefit does not.** [concept-prep.md](../concept-prep.md) records a
clay hop that is in the pipeline, local-first, with a measured prompt effect and a chosen
configuration — and **nothing in the record says the mesh comes back better.** That is the
only question that justifies the stage, and it has never been asked.

**One arm, one variable:** image-to-3D on a **concept** image versus on the **clay** derived
from it, everything else pinned.

**Its first consumer is the measurement server**, which now serves 8 of 8
([E28](E28-ruling.md)). This is the first arc to use it on new work rather than on recorded
anchors — `mesh_stats` and `mesh_topology` grade both meshes through one code path, which is
the property that server exists to provide.

## ⛔ TASK 0 — THE RECONSTRUCTOR IS BROKEN ON THIS RIG. FIX IT FIRST, AND MEASURE THE FIX.

Reproduced at the advisor's seat, 2026-08-09:

```
python _mesh_character.py --image <clay>.png --out <scratch>.glb --ptype 1024_cascade --remesh 1
  ...model loads, pipeline starts...
  File "trellis2\modules\attention\full_attn.py", line 107, in scaled_dot_product_attention
    import flash_attn
ModuleNotFoundError: No module named 'flash_attn'
```

The model loaded and the pipeline began — this fails **inside attention**, not at import.
Meanwhile [the handbook](../handbook/index.md) records reconstruction at *103–141 s per
mesh, 3.4–5.6 GB peak VRAM, measured across six meshes on two subject classes*, so this
route demonstrably ran on this rig. **Something changed, or those runs used a different
backend.**

**The hypothesis, offered to be measured and not obeyed:** the studio's sprite line records
the TRELLIS.2 invocation as `ATTN_BACKEND=sdpa SPARSE_ATTN_BACKEND=sdpa`, which routes
around flash-attn entirely. **That is a recollection from another lane's memory, not a
measurement here.** Test it; if it works, record it as the invocation; if it does not,
report what you find and **halt** rather than installing packages into a pinned environment.

⚠ **`E:\AI-Models\trellis2-env` is the interpreter the whole repo depends on.** Do not
`pip install` into it to chase this. An environment repair that adds capability is
permitted under [E23 Ruling 2](E23-ruling.md); one that changes a pinned version under four
accepted assets is not, and the difference must be argued in the report before it is made.

**Gate: no reconstruction runs until one known input reconstructs.** Prove the fix on any
subject before spending the arm.

## Task 1 — the arm

**Both inputs are already staged**, hashed, at `E:\AI\facet_scratch\clay_arm\`:

| role | file | sha256 | frame |
|---|---|---|---|
| concept | `minotaur_concept.png` | `29fc8b87bf9d7595…` | 832×1216 |
| clay | `minotaur_clay.png` | `95f519351b31757c…` | 1696×2478 |

⚠ **Verify both hashes before use.** And note the clay in scratch is the **cloud Nano Banana
2** render, not the ruled local Qwen floor — [concept-prep](../concept-prep.md) records
both. **Which clay this arm uses is a real choice**: state it, and if you use the Qwen floor
instead, hash it into the record first.

**Pin everything but the image.** Same `--ptype 1024_cascade`, same `--remesh`, same
decimation and texture size, same interpreter. `--image` is the only difference, and the
report says so explicitly.

⚠ **Outputs go to scratch, never to `E:\AI\training`.** Manifest the **eight facet
subtrees** — `facet_next`, `facet_E01/E02/E05/E06/E07/E08`, `saltroad_bake_fix` — at
**7,312 files / 17,072,807,610 bytes**, 0/0/0, before and after. **Not the training root**:
[E28 Ruling 22](E28-ruling.md) measured that the root holds 131,970 files and that every
dispatch since E22 has worded this wrong.

## Task 2 — grade them, through the server

Run **both** meshes through the served surface, not the scripts directly, so the instrument
identity is the point rather than an assumption:

- **`mesh_stats`** — components welded **and** unwelded, curvature variance, bbox and
  std-frame extents, projected silhouette area.
- **`mesh_topology`** — non-manifold edges and where they concentrate, boundary edges, the
  **dual-definition** shell census, hollow/double-wall detection. Quote both shell
  definitions; they do not agree and the disagreement is the finding on a pinched mesh.
- Record the **identity envelope** from each payload (server version, instrument sha256,
  config hash). Two meshes measured by one code path is this arc's whole claim to
  comparability.

**What to expect and why it is not a prediction:** the concept has stone touching both feet
and a hand-adjacent block, and there is no segmentation stage in front of the reconstructor.

## ⚠ Task 3 — THE SHEET, AND IT COMES BEFORE THE VERDICT

**Build `concept-mesh | clay-mesh` clay renders at the Director's zoom, side by side, and
put them in front of him before any number decides anything.** Geometry is judged under
`--clay` (texture hides geometry; that confusion cost a whole session), at full size, never
from a contact sheet.

**No metric in this arc may answer "is the clay mesh better."** That is an artifact
judgment and it is his. The numbers say *what differs*; his eye says *which is right*. This
repo spent four experiments on metrics that could not separate an asset he rejected from one
he accepted, and stage 0's whole premise is a geometry-quality claim.

## Predictions — committed BEFORE the first reconstruction

Write `E29-predictions.md` and commit it before task 1 runs. Point estimate, band, blind
disclosure per row. **Name the unit and the denominator before each number.**

- **P1** — will the concept mesh fuse the figure to the dungeon floor or wall? Binary, with
  the falsifier stated.
- **P2** — shells (vertex-joined) for each mesh. Two numbers, and say which definition.
- **P3** — non-manifold edge count for each.
- **P4** — face/vertex counts for each at identical decimation.
- **P5** — behavioural: will `mesh_topology`'s hollow/double-wall test fire on both? (E14
  Ruling 3 says every `1024_cascade` reconstruction on this route is a hollow double-walled
  shell — so a *negative* here would be the interesting result.)
- **P6** — task 0: does `ATTN_BACKEND=sdpa` alone fix the reconstructor?

⚠ **Seven consecutive arcs have missed on a unit, a population, an unchecked property, the
rarest clause of a conjunction, or the instrument's continued ability to express the
question.** Read those five laws in CLAUDE.md before writing a number, and **apply no
calibration haircut**.

## Gates

1. **No arm runs until task 0's fix reconstructs a known input.**
2. **One variable.** If anything but `--image` differs between the two runs, the comparison
   is void and the report says so.
3. **The manifest holds** — eight facet subtrees, 7,312 / 0/0/0, before and after.
4. **The sheet reaches the Director before any verdict is written.**
5. **No `tools/` change.** A needed change is a finding. If task 0's fix is an environment
   variable it is not a tool change; if it is a code edit, **halt and report**.
6. **CI green**, run id resolved before written; `NOT YET RUN` until it is.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | both inputs hashed in the dispatch; every reconstruction parameter pinned and identical but one; both payloads carry the server's identity envelope |
| ANDON_AUTHORITY | 3 | gate 1 blocks the arm on an unproven fix; gate 2 voids the comparison on a second variable; gate 5 halts on a code edit; the manifest halts on any tree delta |
| NAMED_COMPENSATORS | 3 | reconstruction is read-only on its inputs and writes only to scratch — `git revert` plus deleting a scratch tree is the whole undo. No cloud spend, no publish, no recorded-tree write |
| DECOMPOSE_BY_SECRETS | 3 | the subject lives entirely in the two input images; every route constant is pinned identically across both arms, so nothing subject-specific enters the code path |
| UNCERTAINTY_GATED_HUMANS | 3 | gate 4 routes the verdict to the Director's eye by construction, and the dispatch forbids any metric from answering the acceptance question |
| EXTERNAL_VERIFIER | 3 | the measurement server is a different code path from the reconstructor, and both meshes go through **one** instrument — the comparability property the server exists to provide, used here on new work for the first time |

## Out of scope

- **Anything downstream of reconstruction** — no twins, no projection, no brush. This arm
  ends at two meshes and a sheet.
- **Promoting or demoting stage 0** — that is the ruling's job, and the Director's.
- **The publish**, `comfy-preflight`, and the polish lanes.
- **Editing `tools/`**, the index pair, the census, or `docs/experiments/README.md`.

## Environment

```
python    E:\AI-Models\trellis2-env\Scripts\python.exe      <- ABSOLUTE, always
trellis   E:\AI-Models\TRELLIS.2-repo\_mesh_character.py    <- --image --out --ptype --remesh
inputs    E:\AI\facet_scratch\clay_arm\{minotaur_concept,minotaur_clay}.png
```

- **The VRAM watchdog is alive** (restarted 2026-08-09, heartbeat verified). Reconstruction
  is local and measured at 3.4–5.6 GB peak — well under the ceiling, but check it is up.
- **Generation is cloud-only and this arc generates nothing.** Zero credits.
- Blender through PowerShell, `-b -P` only. **ASCII prints.** Scripts create their own
  output directories. `argparse` eats leading minus signs.

## Halt

Report at `E29-clay-reconstruction-report.md`.

- **State predictions before you look**; disclose whether each was blind.
- **Never judge whether output is good.** *Verified, shipped, works, decisive, validated,
  proven* belong nowhere in the report.
- **A negative result is a full success.** If the clay mesh is no better, that is the
  answer, and it retires a stage rather than embarrassing anyone. **If the concept mesh is
  better, say that plainly** — it is the more valuable finding of the two.
- **Do not write to the memory store.**
