# E29 predictions — committed BEFORE the first reconstruction

**Written by the executor, 2026-08-09**, before task 0's fix was attempted and before any
reconstruction ran. The commit that carries this file is the anchor; nothing below was
edited after a result was seen.

---

## Disclosure, per the dispatch

- **Both input images were opened at full size before these predictions were written**, and
  are described below. Looking at an *input* is not looking at a *result* — every prediction
  here is about a mesh that does not exist yet. The alternative was to predict against
  [concept-prep.md](../concept-prep.md)'s prose description of the concept, and this repo's
  standing law is that **an inherited claim is a hypothesis wearing a fact's clothes**. What
  I found is in §2, and it is stronger than the description.
- **P6 is blind in the strict sense.** `trellis2/modules/attention/` was not opened, and
  neither was any TRELLIS.2 source, before P6 was written.
- **The record was read for calibration** — E14 Gate 0's topology table (three longswords),
  E12 Gate 0's stats table (three dragons), and `docs/handbook/subjects.md`'s family table.
  Those are *prior subjects*, and that page's own standing rule is that **a new subject class
  has no working prior**. The minotaur is humanoid×beast, a fifth class beside the four
  recorded. Every band below is widened for that, and the widening is stated rather than
  silently applied.
- **No calibration haircut.** E23's lesson — an executor who halved an untutored estimate on
  this repo's own "densities run 2× high" lesson and moved *away* from the truth — is why
  these numbers are stated as reasoned, with no correction applied for the fact that seven
  consecutive arcs have missed.

## 1. The five prediction laws, applied before any number was written

| law (CLAUDE.md) | how it bites here | what I did |
|---|---|---|
| name the **unit** | "shells" has two definitions that disagree by a factor of hundreds | every row below names the JSON key, its definition, and its denominator |
| check the **population** is real | the two meshes do not exist yet; the population is *two GLBs*, not "the arm" | P4's population is faces **after** `to_glb(decimation_target=1_000_000)`, not the raw pipeline output the script also prints |
| check the **property is defined** for every member | **P5's test is conditional and can decline to compute** — see §4 | P5 is split into clause A (does it compute) and clause B (what it says) |
| a **conjunction** tracks its rarest clause | P5 is a conjunction; so is P6 ("alone") | both predicted clause-by-clause, then the join |
| the **instrument must still express the question** | the reconstructor is broken at HEAD — that is task 0 | P6 predicts the fix, and no other row can be scored until it lands |

## 2. What the inputs actually are — opened, not inherited

Both hashes re-verified at this seat before anything ran:

| role | file | bytes | sha256 (full) | frame |
|---|---|---:|---|---|
| concept | `minotaur_concept.png` | 1,693,150 | `29fc8b87bf9d759541d418ad94d9004499115ced23f3134af754e3b0ab8962d2` | 832×1216 |
| clay | `minotaur_clay.png` | 6,240,299 | `95f519351b31757c2bc6e1c0e67230c05ae92e865fbf569f14b86632e5ef885a` | 1696×2478 |

Both match the dispatch's prefixes. **This arm uses the cloud Nano Banana 2 clay**, not the
ruled local Qwen 4-step floor — the dispatch names that as a real choice, and it is made this
way because that is the artifact already staged and hashed, and because
[concept-prep](../concept-prep.md)'s Gate 0 walk — the pair the Director looked at — is *this*
pair. Running the arm on a clay he has not walked would change two things at once.

**The concept, described from the image:** the minotaur stands in a dungeon. Every non-figure
pixel in the frame is masonry — a coursed stone-block wall fills the entire background from
top edge to floor, and the figure stands on a flagstone floor with visible joints. Both feet
are planted on stone, the forward (frame-left) foot on the edge of a cut step. There is a
large cut stone block at bottom-left directly beneath the lowered fist, and a second block at
bottom-right. **The description in `concept-prep.md` — "stone touching both feet and a
hand-adjacent block" — undersells it**: this is not a figure touching some stone, it is a
figure with no background separation anywhere in the frame. The horn tips run to the top edge.

**The clay, described from the image:** a full maquette on a seamless light-grey sweep, whole
figure inside the frame with margin, no plinth, no base. There is a **soft cast shadow on the
ground under the feet** — which is the exact artifact E14's floor test was built for, so the
clay's fusion risk is not zero, it is a shadow rather than a wall.

### ⚠ A confound that rides with `--image`, declared before the run

The two images are **different frames** — 832×1216 against 1696×2478, 1.01 MPx against
4.20 MPx. Only `--image` differs on the command line, but *"one variable" is a property of the
dependency graph, not of the parameter you edited*. If TRELLIS.2 resizes both to one internal
resolution the confound collapses; if it does not, input resolution rides along with the
register change and the arm cannot apportion between them. **The frame difference is inherent
to the clay hop** (the tool renders at 2K), so it cannot be pinned away without changing what
the hop is — but it is named here, before the run, and the report will state which case holds.

## 3. Predictions

Each row names its unit and denominator first. Bands are 80%-confidence intervals unless
stated. **Blind** = no source or artifact bearing on the answer was opened before writing.

### P1 — does the CONCEPT mesh fuse the figure to the dungeon floor or wall?

**Unit.** `mesh_topology.extremal_slabs["z-min"]`: `area_frac` = surface area of faces whose
centroid sits in the bottom 0.5% of the z extent, over **total surface area of the mesh**;
`axis_facing_frac` = area within that slab whose normal is within 45° of −z, over **that
slab's own area**. Corroborated by `mesh_stats` widest-horizontal / height (character band
0.46–0.72) and by the `--clay` render at the Director's zoom.

**Prediction: YES — the concept mesh comes back with non-figure stone geometry attached to the
figure.** Point estimates: `z-min area_frac` **6%** (band 2–20%) at `axis_facing_frac`
**> 0.85**; widest-horizontal/height **0.95** (band 0.65–1.40), i.e. *outside* the recorded
character band on the high side.

**Falsifier — stated so it can be wrong.** P1 is FALSE if the concept mesh's `z-min` slab
reads `area_frac ≤ 2.0%` (the regime E12's dragon 00001 sat in at 1.021%, which was flat foot
soles and nothing else) **and** the clay render shows no slab, wall or block mass beyond the
figure's own silhouette. Either of those alone failing is not enough; both must hold to
falsify.

*Reasoning, so the mechanism is on the record and not just the number:* there is no
segmentation stage in front of the reconstructor, and the concept has no background to
segment — masonry occupies 100% of the non-figure frame. **Disclosure: informed** (I opened
the image).

### P2 — shells

**Unit.** `mesh_topology.shells` — **shared-vertex** connected components on the welded mesh,
identical by construction to `mesh_stats.vertex_components`. **Not**
`pieces_manifold_adjacency`, which is the shared-manifold-edge quantity and disagrees by
hundreds. Denominator: none, it is a count.

| mesh | point | band |
|---|---:|---|
| concept | **210** | 40 – 900 |
| clay | **55** | 10 – 250 |

**Direction is the real claim: the concept mesh carries more shells than the clay mesh.**
Mechanism: shells count masses not vertex-joined to the body, and the concept supplies
several — a wall plane behind, two cut blocks, floor slabs — plus fur, mane and wet-hair
strands that the clay register deliberately strips. Bands are wide because the recorded
spread is enormous for reasons that are subject-specific (longsword 1 / 331 / 2; dragon
12 / 12 / 9; character 40–191; galleon 237–512) and the handbook's rule is that this quantity
does not interpolate across classes. **Disclosure: informed.**

### P3 — non-manifold edges

**Unit.** `mesh_topology.nonmanifold_edges` — count of unique edges with **more than two**
adjacent faces, welded mesh. Denominator when quoted as a fraction: `edges_unique`.

| mesh | point | band |
|---|---:|---|
| concept | **1,600** | 250 – 12,000 |
| clay | **550** | 100 – 4,000 |

Recorded anchors: longswords 121 / 1,040 / 251 of ~1.42–1.50M unique edges; E12's dragon
00003 carried 7,138, a dense pinch mass through a folded wing. **Direction: the concept mesh
carries more.** Mechanism: non-manifold edges are pinches, and pinches appear where surfaces
meet at thin contact — a figure welded to a floor and a wall has many such contacts, and the
clay's smoothed register has fewer thin structures by construction. **Disclosure: informed.**

### P4 — face and vertex counts at identical decimation

**Unit.** `faces` = triangles of the welded mesh as counted by `mesh_stats` / `mesh_topology`
**after** `o_voxel.postprocess.to_glb(decimation_target=1_000_000)` — *not* the raw
`pipe.run()` count the script also prints. `verts` = welded vertices.

| mesh | faces (point) | faces (band) | verts (point) | verts (band) |
|---|---:|---|---:|---|
| concept | **975,000** | 930,000 – 1,000,000 | **487,000** | 465,000 – 500,000 |
| clay | **970,000** | 930,000 – 1,000,000 | **485,000** | 465,000 – 500,000 |

**The claim is that the decimation target binds on both and the two arms land within 5% of
each other** — i.e. this row is predicted to be *uninformative about the arm*, which is worth
saying out loud because a row that cannot separate the arms should not later be read as
evidence for it. Recorded: longswords 999,474 / 948,328 / 951,850; dragons 965,625 / 966,690 /
986,825 — all just under 1M, all with verts ≈ faces/2 (Euler on a near-closed surface).

**Falsifier.** If either mesh returns well below 930,000 faces, the target did not bind and
the mechanism above was wrong. **Disclosure: informed** (I read `_mesh_character.py` for the
parameter names, which is how the unit above is stated at all).

### P5 — does the hollow / double-wall test fire on both? — A CONJUNCTION, SPLIT

**This row is where the "unchecked property" law bites, and the test is not unconditional.**
`e14_topology.py:154` computes `nested_wall_test` **only if**
`len(pieces) >= 2 and len(pieces[1]) > 0.01 * tot_faces` — otherwise the key is `null` and the
test has not fired, it has *declined to run*. So "does it fire" is two questions.

**Clause A — does it compute at all?** Unit: `nested_wall_test is not null`, which requires
the manifold-adjacency graph to split with a **second piece larger than 1% of total faces**.
Prediction: **YES on both.** Confidence: concept 0.85, clay 0.85.

**Clause B — given it computes, does it read as a nested wall?** Unit: `inner_volume`
**negative** (opposite orientation to the outer) with `material_frac_of_outer` small — thin
walls around a cavity. Prediction: **YES on both.** Confidence: concept 0.90, clay 0.90.

**The join — both clauses, both meshes: 0.85 × 0.90 ≈ 0.75 per mesh.** The clause that can
fail is **A**, not B, and A is the one nothing in the record has ever reported failing —
E14 Ruling 3's route-wide finding is stated about walls, not about the >1% gate that decides
whether the instrument looks for them. A mesh whose inner wall is shredded into many small
pieces, or fused to the outer along a long contact, fails A while still being hollow.

**A negative here is the interesting result**, per the dispatch. **Disclosure: informed** — I
opened `e14_topology.py` to find the conditional, which is exactly the check the law demands
and is the reason this row is two rows.

### P6 — does `ATTN_BACKEND=sdpa` **alone** fix the reconstructor? — BLIND

**Unit.** "Fixed" = `_mesh_character.py` runs to `=== MESH RUN COMPLETE ===` and writes a GLB,
on any input. "Alone" = that environment variable set and **no other**.

**Prediction: NO.** `ATTN_BACKEND=sdpa` alone does **not** suffice; `SPARSE_ATTN_BACKEND=sdpa`
is also required, and the two-variable form works. Confidence **0.65**.

Split into clauses, because "alone" is a conjunction wearing one word:
- **A — the one-variable form fails:** 0.65.
- **B — the two-variable form succeeds:** 0.85.
- **C — no code edit and no `pip install` is needed at all:** 0.80.

*Reasoning:* the traceback names `full_attn.py`, a **dense** attention module. `1024_cascade`
is a sparse-structure pipeline and the studio's recollection carries a second, separately
named variable for the sparse path — a variable that has no reason to exist unless a second
import site is governed by it. **Falsifier:** the one-variable run completing and exporting a
GLB. **Disclosure: BLIND** — no TRELLIS.2 source read before this was written.

## 4. What I am NOT predicting, and why

- **Whether the clay mesh is better.** That is the Director's eye and no number in this arc
  may answer it. Nothing above is a quality claim; P1–P5 say *what differs*.
- **Curvature variance, `face_rect_*`, silhouette area.** `mesh_stats`' front-view rect is
  W3's, authored against a humanoid at the character's framing; E12 declined to quote those
  columns on the dragons for that reason and the same objection holds for a minotaur whose
  front is unestablished. They will be *reported* from the payload, not predicted.
- **Reach ceiling, off-surface, anything downstream of reconstruction.** Out of scope by the
  dispatch — this arm ends at two meshes and a sheet.

## 5. Scoring rule, fixed now

A row is **HIT** if the measured value falls inside its stated band, **MISS** otherwise;
point estimates are reported with their error but do not decide hit/miss. Directional claims
(P2, P3) are scored separately from their bands — a row can hit its direction and miss its
band, and both are reported. Retuning any band after seeing a result is the one move that is
always wrong, and none of these will move.
