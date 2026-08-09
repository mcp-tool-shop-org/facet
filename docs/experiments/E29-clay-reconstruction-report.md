# E29 report — does a clay mesh reconstruct better than a concept mesh?

**Executor session, 2026-08-09.** Dispatch:
[E29-clay-reconstruction-kickoff.md](E29-clay-reconstruction-kickoff.md). Predictions
committed **before** task 0 was attempted, at `d07a975`:
[E29-predictions.md](E29-predictions.md).

**This report does not say whether either mesh is good.** The sheet went to the Director at
gate 4 before a single number was written down here. What follows is what differs.

---

## 0. Gates

| gate | evidence | verdict |
|---|---|---|
| **1. no arm until the fix reconstructs a known input** | three reconstructions of `facet_E01/inputs/A0_source_clay.png` completed, exit 0, before either arm ran | **PASS** |
| **2. one variable** | the two arm command lines differ in `--image` and nothing else (§3). The declared resolution confound **collapses**: the pipeline resizes both inputs to **700×1024** before the model sees them (§3.2) | **PASS** |
| **3. the manifest holds** | BEFORE `7312 files / 17,072,807,610 bytes`; at the close `RECHECK before=7312 after=7312 added 0 removed 0 changed 0`, bytes identical. E23's count and byte total reproduce exactly | **PASS** |
| **4. the sheet reaches the Director before any verdict** | five sheets delivered at full size before this file existed; §6 | **PASS** |
| **5. no `tools/` change** | `git diff --name-status -- tools/` empty. The fix is an environment variable. No `pip install`, no code edit, no version change in `trellis2-env` | **PASS** |
| **6. CI green, run id resolved before written** | **NOT YET RUN.** No run id is written here. See §9 | **NOT YET RUN** |

The E15 index ritual ran at session start against a scratch DB: `VERIFY PASSED - all four
legs`, **19/19** seeded, determinism leg **byte-identity**.

---

## 1. Headline

**The arm ran and the two meshes differ far beyond run noise. Neither is fused to anything.**

| | **CONCEPT mesh** | **CLAY mesh** | run-noise floor (measured, §2.3) |
|---|---:|---:|---|
| faces | 963,072 | **998,985** | ±2,618 (0.27%) |
| verts | 475,554 | 497,872 | ±1,306 |
| **shells** (shared-vertex) | **82** | **9** | **±1** |
| **non-manifold edges** | **4,201** | **1,461** | **±18** |
| non-manifold fraction | 0.002917 | 0.000976 | — |
| boundary edges | 0 | 1 (length 0.0) | — |
| widest-horizontal / height | 0.5522 | 0.5988 | — |
| surface area | 2.4757 | 2.7916 | — |
| UV clusters (from the run log) | 8,370 | 2,480 | — |
| `nested_wall_test` | **NULL — declined** | **NULL — declined** | — |

The three headline gaps are **73×**, **152×** and **13.7×** their own measured noise floors
respectively. They are not run noise.

**Direction, stated plainly and without a quality word attached:** the clay mesh comes back
with **one ninth the shells**, **one third the pinches**, and **3.7% more of the polygon
budget spent** than the concept mesh. Whether that is *better* is the Director's, and §6 is
where it is asked.

---

## 2. Task 0 — the reconstructor. Fixed by one environment variable, and four things fell out.

### 2.1 The failure reproduces, and it is not where the dispatch's summary put it

```
ModuleNotFoundError: No module named 'flash_attn'
  trellis2/models/sparse_structure_flow.py:240   forward
  trellis2/modules/transformer/modulated.py:147  _forward
  trellis2/modules/attention/modules.py:82       forward
  trellis2/modules/attention/full_attn.py:107    import flash_attn
```

Reproduced at this seat on `A0_source_clay.png`, exit 1. The call site is **`full_attn`** —
the *dense* attention module — reached from the sparse-structure stage. That matters for what
follows.

Measured in the environment, before anything was changed:

| fact | measurement |
|---|---|
| `flash_attn` importable | **No** — `importlib.util.find_spec` returns `None` |
| `flash_attn` remnant in site-packages | **None** — no package directory, **no `.dist-info`** |
| interpreter | Python 3.13.13 (built 2026-05-10) |
| torch | 2.10.0+cu130, CUDA 13.0, RTX 5090, available |
| xformers | 0.0.35, present |

`E01_W3_trellis2.glb` carries an mtime of **2026-08-03**, so this route reconstructed on this
rig six days ago. `flash_attn` is gone and left no dist-info behind; **how it left is not
something this session can measure**, and no claim is made about it.

### 2.2 `ATTN_BACKEND=sdpa` **alone** reconstructs. `SPARSE_ATTN_BACKEND` is inert here.

| run | env | exit | wall | peak VRAM | faces out |
|---|---|---|---|---|---:|
| bare | — | **1** | — | — | — |
| **r1** | `ATTN_BACKEND=sdpa` | **0** | 104 s | 3.4 GB | 977,636 |
| **both** | `ATTN_BACKEND=sdpa` + `SPARSE_ATTN_BACKEND=sdpa` | **0** | 105 s | 3.4 GB | 975,018 |
| **r2** | `ATTN_BACKEND=sdpa` (repeat of r1) | **0** | 99 s | 3.4 GB | 975,698 |

104 s / 3.4 GB sits inside the handbook's recorded band (103–141 s, 3.4–5.6 GB). **No
`pip install`, no code edit, no pinned version touched** — the dispatch's condition for an
environment repair is met without having to argue the harder case, because nothing was added.

**`SPARSE_ATTN_BACKEND=sdpa` changes nothing measurable.** Its run is bracketed by the two
runs that omit it (975,018 against 975,698 and 977,636), and every upstream stage is
bit-identical across all three (§2.3). Recorded because every reconstruction invocation in
this repo carries that variable, and on this route it is doing no work.

### 2.3 The generative stage is deterministic. The *simplify* stage is not — and that is a noise floor nothing here had measured.

Three runs, same input, same seed, same parameters:

| stage | r1 | both | r2 |
|---|---|---|---|
| raw `pipe.run()` | 1,512,783 v / 3,050,586 f | **identical** | **identical** |
| after filling holes | 1,512,791 v / 3,050,646 f | **identical** | **identical** |
| after remeshing | 2,911,498 v / 5,828,836 f | **identical** | **identical** |
| **after simplifying** | 487,030 v / **977,636 f** | 485,725 v / **975,018 f** | 486,069 v / **975,698 f** |
| UV clusters | 3,704 | 3,714 | 3,653 |

Everything through remeshing is identical to the digit. The divergence is entirely inside
`o_voxel.postprocess.to_glb`'s decimation. Graded through the served surface, the floor is:

| quantity | min | max | spread | as % of mean |
|---|---:|---:|---:|---:|
| faces | 975,010 | 977,628 | 2,618 | **0.27%** |
| shells | 40 | 41 | **1** | 2.48% |
| non-manifold edges | 1,684 | 1,702 | **18** | 1.06% |

**Every comparison in this report is quoted against this floor.** The studio's recollection
that "TRELLIS is DETERMINISTIC" is half right and the half that is wrong is the half a
mesh comparison lands in.

### 2.4 ⚠ A recorded claim is corrected: the `[SPARSE]` banner is not a readout of what ran

[E04's Gate 0 report §1](E04-gate0-report.md) records that with both variables set, trellis2
"still reports `Conv backend: flex_gemm; Attention backend: flash_attn` at import", and
concludes: **"What ran is what the log says, not what was requested."** E12 carried it forward
as prediction P21.

**Measured here: that banner printed on every one of the six runs in this session — in a
process where `flash_attn` is not installed and cannot be imported, and which ran to
completion.** A second banner, `[ATTENTION] Using backend: sdpa`, is the one that tracks the
dense path, and it is the one E04 did not quote.

So the `[SPARSE]` line is a **declared preference emitted at import**, not a record of
execution. E04's inference was sound given one banner; it is wrong given two. **The repo's own
law fires again — a number that reproduces exactly can still be measured against the wrong
object** — and this is its log-line sibling.

### 2.5 An anchor nobody asked for: the sdpa rebuild reproduces the recorded W3

The recorded `E01_W3_trellis2.glb` was built 2026-08-03 **under flash_attn**. This session
rebuilt it from the same recorded input under sdpa. Both graded through the same instrument:

| | recorded (flash_attn, 08-03) | rebuilt (sdpa, today) | delta |
|---|---:|---:|---|
| faces | 975,300 | 977,628 | +0.24% — **inside the 0.27% floor** |
| verts | 485,564 | 486,727 | +0.24% |
| **shells** | **40** | **40** | **0** |
| largest_shell_frac | 0.983012 | 0.983014 | +2e-6 |
| non-manifold edges | 1,693 | 1,702 | +9 — **inside the ±18 floor** |
| widest/height | 0.4580 | 0.4579 | −0.0001 |

Per the repo's rule that *moving a line to different hardware needs an anchor first*: the
backend change is a move of that kind, and it comes back inside the noise floor on every
quantity. Recorded as an anchor, not as a licence — one subject, one input.

---

## 3. Task 1 — the arm

### 3.1 The invocation, pinned

Both inputs were re-hashed at this seat and compared before use, full sha256 in
[E29-predictions.md](E29-predictions.md); both match the dispatch. **This arm used the cloud
Nano Banana 2 clay**, not the ruled local Qwen 4-step floor — stated as the dispatch requires,
and chosen because it is the pair the Director already walked at
[concept-prep](../concept-prep.md) Gate 0.

```
PYTHONPATH=E:\AI-Models\TRELLIS.2-repo   HF_HOME=E:\AI-Models\hf-cache
ATTN_BACKEND=sdpa   SPARSE_ATTN_BACKEND=sdpa
E:\AI-Models\trellis2-env\Scripts\python.exe _mesh_character.py
    --image <THE ONLY DIFFERENCE>  --out <scratch>.glb
    --ptype 1024_cascade  --remesh 1  --decimation 1000000  --texture 4096
```

`--decimation` and `--texture` were passed **explicitly** at their default values so the pin
sits in the command line rather than in a default that a future edit could move. Both
variables are kept in the env although §2.2 measures the second inert, so the invocation
string stays identical to every recorded reconstruction in this repo.

| arm | wall | peak VRAM | raw | after remesh | after simplify | GLB |
|---|---|---|---|---|---|---|
| **concept** | 102 s | 3.4 GB | 2,081,716 v / 4,229,386 f | 3,880,438 v / 7,776,424 f | 476,675 v / 963,074 f | 39.5 MB |
| **clay** | 107 s | 3.4 GB | 2,208,416 v / 4,430,096 f | 4,328,594 v / 8,662,216 f | 497,978 v / 998,988 f | 36.6 MB |

*(The runner's own simplify line and the graded counts in §1 differ, and the difference is the
weld: faces by **2** (concept) and **3** (clay), vertices by **1,121** and **106**.
`mesh_stats` welds with `merge_vertices(merge_tex=True, merge_norm=True)` before counting, so
§1's numbers are the welded ones and are the numbers quoted throughout.)*

### 3.2 The declared confound collapses — measured, not assumed

The predictions declared a confound before the run: 832×1216 against 1696×2478, 1.01 MPx
against 4.20 MPx, riding along with `--image`. Read from
`trellis2/pipelines/trellis2_image_to_3d.py:137`:

```python
max_size = max(input.size)
scale = min(1, 1024 / max_size)
if scale < 1: input = input.resize(...)
```

- concept 832×1216 → scale 0.8421 → **700 × 1024**
- clay 1696×2478 → scale 0.4132 → **700 × 1024**

**Both inputs reach the model at byte-identical dimensions.** The pipeline then removes the
background (`rembg`, line 147), takes the alpha bbox, and **square-crops to the subject**
(lines 152–158), so framing and aspect are normalized too. What remains of the confound is the
resampling path alone — the clay is downsampled 2.4× harder than the concept — and that is
stated rather than dismissed.

---

## 4. ⚠ Task 2 finding: the measurement server is not registered anywhere a session can reach it

`E:\AI\facet\.mcp.json` declares **one** server, `facet-record`. `tools/measure_mcp.py` is not
in it, and is not in `E:\AI\.mcp.json` either. **No session can reach the measurement server
over MCP as the repo stands.**

Per gate 5, a needed change is a finding and this session did not make it. Instead the served
surface was called **in-process**: `import measure_mcp`, unwrap the tool functions, call them.
Same module, same wrapped instrument, same envelope — the transport differs, the code path
does not, and the code path is what the comparability claim rests on.

**The envelope proves it.** Every payload in this arc:

| | value |
|---|---|
| server | `facet-measure` **0.4.0** |
| `mesh_stats` instrument | `tools/verify/mesh_stats.py` sha256 **`fe146891d97265f5…`** |
| `mesh_topology` instrument | `tools/diagnostics/e14_topology.py` sha256 **`6351135ef6891861…`** |
| metrics label | `diagnostic` — *"promotion to gate-eligible requires asking what else moves it, which is a ruling"* |
| warnings | `[]` on both arms |

Both instrument hashes are **identical across all five meshes measured** (two arms, one fresh
control, two recorded). `config_hash` differs per mesh because it carries the mesh path, which
is correct. This is the first use of the server on new work, and it is the property the server
exists to provide.

---

## 5. Task 2 — what the served surface says

### 5.1 P1's question: is either mesh fused to the dungeon? **No.**

`extremal_slabs`, area of the outermost 0.5% slab as a fraction of **total surface area**, and
the share of that slab's area facing along the axis:

| slab | concept area_frac | concept facing | clay area_frac | clay facing |
|---|---:|---:|---:|---:|
| z-min (underfoot) | **0.2614%** | 0.9999 | **0.3301%** | 0.9978 |
| z-max | 0.0487% | 0.861 | 0.1035% | 0.950 |
| x-min / x-max | 0.0443% / 0.0568% | ~1.0 | 0.0807% / 0.0446% | ~1.0 |
| y-min / y-max | 0.0106% / 0.0218% | ~1.0 | 0.0106% / 0.0130% | ~1.0 |

For scale, the recorded W3 reads **2.4907%** at z-min and W1 **9.5279%**. **The concept mesh
has an order of magnitude less bottom-slab area than the recorded characters**, and nothing
resembling a flat plane on any of the six faces of its box. Widest-horizontal/height is
**0.5522**, sitting inside the recorded character band 0.46–0.72, not outside it.

**Mechanism, and it corrects the dispatch's premise.** The dispatch says "there is no
segmentation stage in front of the reconstructor." **There is one, inside it** —
`pipe.run(..., preprocess_image=True)` runs a `rembg` model and a bbox crop before any
geometry is inferred (§3.2). A dungeon wall filling 100% of the non-figure frame was removed
by the reconstructor's own front door.

This also asks a question of [concept-prep.md](../concept-prep.md), which banks background
normalisation as *"an unrequested benefit… One hop fixed the form register **and** the
background problem."* Measured here, the background problem was **already handled downstream**
for this pair. That is a matter for the ruling, not for this report.

### 5.2 P5's question: the hollow test **declines to compute — on every character-class mesh measured, including two recorded ones**

`e14_topology.py:154` computes `nested_wall_test` **only if** the manifold-adjacency graph has
a second piece larger than **1% of faces**. Otherwise the key is `null`: the test has not
found a mesh solid, it has **declined to run**.

| mesh | pieces | largest | second | second as % of faces | gate 1.00% |
|---|---:|---:|---:|---:|---|
| concept | 800 | 98.580% | 770 | **0.0800%** | DECLINES |
| clay | 247 | 98.592% | 6,292 | **0.6298%** | DECLINES |
| W3 rebuilt (sdpa) | 305 | 98.164% | 2,718 | **0.2780%** | DECLINES |
| **W3 recorded (flash_attn, 08-03)** | 291 | 98.167% | 2,724 | **0.2793%** | DECLINES |
| **W1 recorded** | 4,154 | 94.725% | 2,392 | **0.2571%** | DECLINES |

Compare the longsword 00001, on which the finding was made: two pieces of **521,134 and
478,288** — a 54/46 split. Here the largest piece is **98.2–98.6%** on all five.

**[E14 Ruling 3](E14-ruling.md) says "Every reconstruction this route has made is a hollow
double-walled shell", and its stated evidence base is "all three candidates AND two
out-of-family controls including the accepted dragon"** — three longswords, a dragon, a
galleon. **No character.** The character class is the route's founding subject and it was not
in that evidence base; measured now, this leg of the instrument does not fire on it, on
meshes built under either attention backend.

**What this does NOT establish.** A declining precondition is not a measurement of solidity.
E14 measured hollowness three mutually independent ways; only one of them is in this payload.
An inner wall shredded into hundreds of sub-1% pieces, or fused to the outer along long
contacts, produces exactly this signature while still being hollow — and 800 / 291 / 4,154
pieces is consistent with shredding. **The honest statement is that `mesh_topology`'s
nested-wall leg does not express the hollow question on this subject class**, which is a
statement about instrument reach. Deciding what follows is the advisor's.

### 5.3 Quoted with the caveat E12 attached to the same columns

`face_curvature_var` reads **0.0013975** (concept) against **0.00022967** (clay), a 6.1× gap;
`face_rect_faces` 412,105 against 368,787. [E12's Gate 0 report](E12-gate0-report.md) declined
to quote this family because the front-view rect is W3's, authored against a humanoid at the
character's framing. `mesh_stats` raised **no warning** on either arm here (both are
vertically dominant, unlike the dragons), so its own guard passed — but a minotaur's rect
takes in horns and air that W3's does not. **Reported, not leaned on.**

`components_unwelded` is 32,341 (concept) against 24,310 (clay); the weld law makes the welded
figures (82 / 9) the real ones.

### 5.4 The boundary triplet, which is why the instrument prints three numbers

| | concept | clay | W3 recorded | W1 recorded |
|---|---:|---:|---:|---:|
| boundary edges | **0** | **1** | 2 | 106 |
| boundary total length | 0.0 | **0.0** | 0.0 | — |
| boundary longest edge | 0.0 | **0.0** | 0.0 | — |

The clay mesh's single boundary edge has **length zero**. This is exactly the case the
instrument's docstring separates — *a zero-length boundary edge and a hole's loop are the same
integer and different facts*. There is no open hole in either arm.

---

## 6. Task 3 — the sheet, delivered before this file existed

Five sheets, built from `turn_render.py --clay` at 1128×1536 per view, identical framing
derived per-mesh from its own bbox:

| file | what |
|---|---|
| `E29_sheet_view0.png` | **concept-mesh \| clay-mesh, front, 2328×1656** — the primary |
| `E29_sheet_provenance.png` | input \| mesh, both arms, on one row |
| `E29_sheet_view2.png`, `view4.png` | side and back at full size |
| `E29_sheet_turnaround.png` | 4 views × 2 meshes — **contact scale, labelled supplementary on its own face** |

All under `E:\AI\facet_scratch\E29\sheets\`.

**Described, not graded.** Both meshes are free-standing figures; neither carries floor, wall
or block geometry on any of the four views. Both hold the pose — raised fist, lowered fist,
wide stance, torso twist — and both keep human feet. Differences visible under `--clay`:

- the **concept mesh** carries the mane, the belt trim and the loincloth hem as thin
  ragged sheet geometry — fringes and spikes, most extensive at view 4 where the mane reads as
  a fan of separate thin sheets. A small closed loop of geometry floats above the head, clear
  of the horns, on views 0 and 4.
- the **clay mesh** carries those same elements as compact smooth forms — sculpted locks, a
  plain belt band with the medallion, a scalloped hem.
- the concept mesh's muzzle, brow and nostril carry more modelled relief; the clay mesh's face
  is smoother and its horns are thicker and shorter.

**Which of those is right is not answerable from any number in this report**, and the arc's
whole premise is a geometry-quality claim. The 82-against-9 shell gap and the 4,201-against-
1,461 pinch gap are consistent with the ragged sheet geometry above, but *consistent with* is
not *identifies*, and none of these metrics can separate an asset the Director rejected from
one he accepted.

---

## 7. Predictions, scored against the bands fixed at `d07a975`

Scoring rule as pre-registered: HIT if inside the stated band. **No band was moved.**

| row | predicted | measured | verdict |
|---|---|---|---|
| **P1** fusion — binary | **YES**, z-min area_frac 6% (2–20%), widest/h 0.95 (0.65–1.40) | **NO.** 0.2614%, widest/h 0.5522 | **MISS** — falsifier satisfied on both clauses |
| **P2** shells concept | 210 (40–900) | **82** | **HIT** |
| **P2** shells clay | 55 (10–250) | **9** | **MISS** — one below the band |
| **P2** direction | concept > clay | 82 > 9 | **HIT** |
| **P3** non-manifold concept | 1,600 (250–12,000) | **4,201** | **HIT** |
| **P3** non-manifold clay | 550 (100–4,000) | **1,461** | **HIT** |
| **P3** direction | concept > clay | 4,201 > 1,461 | **HIT** |
| **P4** faces concept | 975,000 (930k–1M) | **963,072** | **HIT** |
| **P4** verts concept | 487,000 (465k–500k) | **475,554** | **HIT** |
| **P4** faces clay | 970,000 (930k–1M) | **998,985** | **HIT** |
| **P4** verts clay | 485,000 (465k–500k) | **497,872** | **HIT** |
| **P4** arms within 5% | yes | 3.66% | **HIT** (but see below) |
| **P5** clause A concept — does the test compute | YES, 0.85 | **NO — declined** | **MISS** |
| **P5** clause A clay | YES, 0.85 | **NO — declined** | **MISS** |
| **P5** clause B | YES, 0.90 | **unscoreable** — the test never ran | — |
| **P6** clause A — one-variable form **fails** | 0.65 | **it succeeds** | **MISS** |
| **P6** clause B — two-variable form succeeds | 0.85 | yes | **HIT** |
| **P6** clause C — no code edit, no install | 0.80 | yes | **HIT** |

**11 HIT, 6 MISS, 1 unscoreable.**

### Where the misses came from, since that is the useful part

**P1 and P6 failed the same way: I reasoned about a mechanism I had not read.** P1 assumed no
segmentation stage because the dispatch said so and I did not check the pipeline; P6 assumed a
sparse import site existed because a second environment variable was named for one. Both were
**blind or near-blind by design**, which is what makes them informative — but the eighth
consecutive arc's lesson writes itself: *the population, the unit, the property, the rarest
clause, the instrument's reach — and now* **the premise you inherited from your own dispatch.**
Two minutes of reading `trellis2_image_to_3d.py` would have overturned P1 before it was
written, and the repo's law already says an inherited claim costs minutes to check and a
session to build on.

**P5 is the miss worth keeping.** It missed because I took E14 Ruling 3's *"every
reconstruction this route has made"* at its word and did not check its evidence base. Its
evidence base excludes the character class. The prediction was wrong about the instrument and
the instrument was the thing worth learning about — this is the dispatch's own "a negative here
would be the interesting result", landing on the clause I had already flagged as the one that
could fail.

**P2's clay miss is a real miss and is reported as one** — 9 against a band floor of 10. I
widened that band for a new subject class and still put the floor one above the answer. The
clay mesh's 9 shells sits below the recorded character band (40–191) entirely, and at the
bottom of the dragon band (9–12).

**P4 hit every band and was wrong about what it meant.** I predicted the row would be
*uninformative about the arm* and said so out loud. The arms differ by 3.66% — **13.7× the
0.27% noise floor I had not yet measured when I wrote that**. The row separates the arms after
all. Predicting a row is uninformative is itself a prediction, and it can miss.

---

## 8. For the advisor

Ordered by how far each reaches beyond this arc.

1. **E04's `[SPARSE]` banner inference is wrong and E12 carried it forward** (§2.4). The
   banner prints `flash_attn` in a process that cannot import it. Two documents assert what
   ran from a line that does not record it.
2. **E14 Ruling 3's "every reconstruction this route has made" was never measured on the
   character class** (§5.2), and `mesh_topology`'s nested-wall leg declines on all five
   character meshes measured here — including the recorded W3 and W1, built under the old
   backend. This is instrument reach, not a solidity claim, and it wants a ruling rather than
   an executor's reading.
3. **The measurement server is unreachable over MCP** (§4). One line in `.mcp.json`.
4. **The reconstructor's decimation stage is non-deterministic** (§2.3) — 0.27% on faces,
   ±1 shell, ±18 pinches. Nothing in the record carries a noise floor for reconstruction, and
   every prior single-run mesh comparison in this repo was made without one.
5. **`SPARSE_ATTN_BACKEND` is inert on this route** (§2.2) yet rides in every recorded
   invocation string.
6. **`concept-prep.md`'s background-normalisation benefit is downstream-redundant for this
   pair** (§5.1) — the reconstructor removes the background itself. The *form-register* half
   of that hop's claim is untouched by this finding and is what §1 and §6 are about.
7. **`flash_attn` left `trellis2-env` between 2026-08-03 and today, with no dist-info
   remnant.** Not diagnosed; out of scope; recorded because the environment is the interpreter
   the whole repo depends on.

### ⚠ A second seat is live in this working tree — reported, nothing touched

The tree was **clean at `99554a5`** when this session verified it at start. At the close,
`git status` reads nine modified files this session did not open —

```
M README.md                    M docs/instrument-census.json
M docs/advisor-kickoff.md      M docs/instrument-census.md
M docs/experiments/README.md   M site/src/content/docs/handbook/getting-started.md
M docs/index/facet.db          M site/src/site-config.ts
M docs/index/facet.db.cert.json
?? docs/experiments/E31-publish-the-pipeline-kickoff.md
```

— and the record index's certificate moved under this session between two reads
(`verified_utc` 20:34:43Z → 20:53:37Z) without this seat invoking `record_build`.

**This session committed only its own two files** (`E29-predictions.md`,
`E29-clay-reconstruction-report.md`), staged by explicit path, never `git add -A`. Per the
standing rule that *when two seats are live, the count surfaces are the advisor's to reconcile
after both land*, nothing else was staged, reverted or reconciled — including
`docs/experiments/README.md`, which an E29 row would ordinarily touch and which this dispatch
puts out of scope anyway.

---

## 9. What was not done, and why

- **CI**: `NOT YET RUN`, and no run id is written. The predictions commit `d07a975` has not
  been pushed. The last `ci` run in the repo is on `feab30b`, and HEAD `99554a5` drew only the
  Pages workflow — `ci` is paths-gated and a docs-only commit does not trigger it. Per the
  fabricated-citation law, that is written as an absence rather than as a plausible identifier
  with a verdict beside it.
- **No second replicate of either arm.** The noise floor was measured on the *control* input
  (three runs) and applied to the arm. A per-arm replicate would be stronger and was not run;
  the gaps are 13.7×–152× the floor, so the conclusion is not close, but this is a real limit
  and it is named rather than smoothed.
- **No `tools/` edit, no `.mcp.json` edit, no memory-store write.**
- **Nothing downstream of reconstruction** — no twins, no projection, no brush, per the
  dispatch's out-of-scope section.
- **No promotion or demotion of stage 0.** That is the ruling's, and the Director's.
- **Zero cloud credits.** Everything here is local.

---

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | both inputs re-hashed at this seat before use; every reconstruction parameter pinned identically and `--decimation`/`--texture` passed explicitly rather than defaulted; predictions committed at `d07a975` before task 0 was attempted; every payload carries server version and instrument sha256, and those hashes are identical across all five meshes |
| ANDON_AUTHORITY | **3** | gate 1 blocked the arm until three reconstructions of a known input completed; the manifest bracketed the session; gate 6 is written `NOT YET RUN` rather than given a plausible id; the P5 result is reported as a declining precondition rather than converted into a solidity claim the payload does not support |
| NAMED_COMPENSATORS | **3** | reconstruction is read-only on its inputs; every output went to `E:\AI\facet_scratch\E29\`; the recorded trees were read in place and manifested before and after at 7,312 / 0 / 0 / 0. Undo = `git revert` plus deleting one scratch tree. No cloud spend, no publish, no install, no recorded-tree write |
| DECOMPOSE_BY_SECRETS | **3** | the subject lives entirely in the two input images; every route constant is identical across both arms; the confound that could have leaked (input frame) was measured and shown to be normalized inside the pipeline rather than assumed away |
| UNCERTAINTY_GATED_HUMANS | **3** | the sheet reached the Director at full size before this file existed, and §6 states in its own words that no metric here answers the acceptance question. The two findings that touch other arcs' rulings are routed to the advisor in §8 rather than resolved here |
| EXTERNAL_VERIFIER | **3** | both arms measured through one code path with the instrument hash proving it; the P5 reading was checked against **two recorded meshes built under the previous attention backend**, which is the control that turned a minotaur observation into a class-wide one; the sdpa rebuild was anchored against the recorded W3 before any arm result was believed |

---

**Halt.** The ruling is the advisor's at `E29-ruling.md`.
