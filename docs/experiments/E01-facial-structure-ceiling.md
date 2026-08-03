# E01 — Where is the facial-structure ceiling?

**Status:** AMENDED after Gate 0 — arms not yet run
**Author:** advisor session, 2026-08-04
**Executor:** a fresh session (Sonnet is sufficient; this is measurement, not design)
**Estimated cost:** ~2–3 GPU hours, $0 (all local), one Director review at the end

> ### Amendment 1 (advisor, 2026-08-04, after Gate 0)
>
> The executor passed Gate 0 and returned two findings that change the spec. Both were
> correct; both were errors in the original spec, recorded here rather than quietly
> patched.
>
> **(a) The gate pair was badly chosen — advisor error.** `warrior_texpass.glb` vs
> `warrior_final.glb` differ almost entirely in the legs, and `smart_decimate.py`
> *protects* the face rect (it kept 70,049 → 69,756 faces, 99.6%, while the mesh overall
> went 287,234 → 150,000). Asking a face-rect metric to detect leg shredding could not
> have worked. `components` separated the pair decisively (1 vs 1,516) and that is the
> metric H4 turns on, so **Gate 0 is passed.**
>
> **(b) `face_curvature_var` measures crease density, not facial structure.** The
> executor's clean controls establish the metric is alive — icosphere 5.6e-08, subdivided
> box 2.3e-05, warrior face rect 1.38e-04, four orders of range — but also that an
> equal-size *lower-body* rect on the same mesh scores 3× **higher** than the head. It
> tracks armour edges, boot rims and blades. It is hereby **renamed `crease_density` and
> demoted to advisory.** No replacement scalar is being commissioned: no cheap number
> reliably answers "does this read as a face", which is exactly why this spec puts the
> Director's eye on clay renders as the verdict. A metric that looks authoritative but
> is not would recreate the failure this repo exists to prevent.
>
> **(c) A0 is dropped as a control — advisor error.** `warrior/clay_concept.png`
> (clean-shaven, plate armour, heroic proportions, sword on the viewer's right) and
> `warrior/mesh.glb` (bearded, tunic bulk, dwarf proportions, sword on the left) are
> **different characters**; the mesh matches `twin_front.png`. The original spec assumed
> one produced the other, inherited from an archived note and never verified — the exact
> failure this spec was written to prevent, committed inside the spec itself. No clay
> render of the bearded warrior exists under `E:\AI\training` or `E:\AI\facet`, and A0's
> generation settings are unrecorded.
>
> **Consequences:** **A3 becomes the baseline.** Every arm now derives from
> `clay_concept.png`, so H1 = A1 vs A3, H2 = A2 vs A3, H3 = A4 vs A3. This is better
> internal validity than the original design. The stated cost: results can no longer be
> compared against the shipped asset, only against each other.
>
> **Open question for the Director (do not guess):** the bearded warrior came from Mike's
> own Comfy graph (`mesh_saltroad_warrior_p1_00004` lineage), so its clay input would be
> in Comfy outputs rather than under `E:\AI\training` — which is why the search found
> nothing. If that file exists, A0 becomes valid and reconnects the experiment to the
> shipped asset. If not, proceed without it.

---

## 0. Read this before anything else

**You are not being asked to improve the pipeline. You are being asked to measure
where its quality ceiling actually is.** A negative result is a full success here. If
every arm of this experiment produces the same crude face, that is the finding, and it
is worth more than a hand-tuned improvement, because it redirects everything downstream.

**Three rules that are not negotiable.** Each was paid for in a real session.

1. **You do not judge whether output is good.** You produce measurements and comparison
   sheets. The Director judges. Do not write "verified", "shipped", "works", "decisive",
   or "the approach is validated" anywhere — not in the report, not in a commit message,
   not in a memory file. Write what you ran and what came out.
2. **Do not write to the memory store at all.** The advisor folds findings into the repo
   after the Director has seen them. A previous session's self-assessed notes became
   doctrine for ten subsequent sessions; that loop is closed and stays closed.
3. **Stop and report at every gate below.** If a gate fails, do not improvise a fix and
   continue — report the failure with its evidence and stop. Improvising past a failed
   gate is how three hours got spent on a stale premise.

---

## 1. What is already known (checkable, not asserted)

All of this is verifiable from `github.com/mcp-tool-shop-org/facet` and the artifacts
under `E:\AI\training\saltroad_bake_fix\warrior\`.

**The texture pipeline runs.** `texpass_loop.ps1` takes a styled twin pair plus a mesh
and produces a fully textured character in ~8 minutes: two projections, eight
inpainting strokes, dilation fill. Holes go 1.68M → 868k → 0.

**The output is not good enough.** The Director's verdict on the finished warrior:
clunky, with a ghost image and a white patch on the skull. That verdict stands and is
not up for re-litigation in this experiment.

**Two independent findings point upstream of texture, at geometry:**

- *Structure isn't there to preserve.* Clay renders — geometry only, no texture — show
  the face is crude on the source mesh: eyes are shallow dents, the nose is a wedge, the
  beard is a smooth lump. The brow visible in styled renders is paint on a nearly
  featureless surface. Detail overlays mask; it never restores.
- *Topology blocks density allocation.* `smart_decimate.py` correctly allocates polygon
  budget and carries UVs through the cut, but reconstruction output is roughly 8,600
  disconnected shells. Collapse decimation merges neighbours, and shell soup has no
  neighbours — so it tears holes instead of reallocating. First run the legs vanished;
  second run they shredded.

**One prior measurement worth re-testing rather than trusting:** an earlier session
recorded that generating at `--ptype 512` produced a face with no eyes while
`1024_cascade` did not, at similar polygon counts — suggesting generation resolution,
not polycount, carries facial detail. That is a single unreplicated observation. Treat
it as a hypothesis (H4), not a fact.

---

## 2. The question

**Does the reconstructor's facial output improve when it is given the face at higher
effective resolution — and does any configuration produce a connected surface rather
than shell soup?**

Two dependent variables, both of which gate the studio's route:

- **Facial structure** — does the geometry hold eye sockets, a nose bridge, a mouth line?
- **Topology** — is the output one connected surface, or thousands of shells?

The second matters as much as the first. Facial structure decides whether characters
can carry a close-up; topology decides whether polygon budget allocation is possible at
all.

---

## 3. Hypotheses and predictions

State your prediction before running each arm. A hypothesis with no prediction cannot
be wrong, and one that cannot be wrong teaches nothing.

| id | hypothesis | prediction if TRUE | prediction if FALSE |
|---|---|---|---|
| **H1** | Framing is the lever: the head occupies a small share of a full-figure concept, so the reconstructor spends almost no resolution there | a bust-framed clay input yields visibly deeper eye sockets, a defined nose bridge, a mouth line | bust framing gives the same crude face at larger scale |
| **H2** | Generation resolution is the lever (the `ptype` observation) | `1024_cascade` holds facial features that `512` loses, at matched polycount | both lose them, or both hold them |
| **H3** | Generator choice is the lever | one generator produces materially better facial geometry from an identical input | all three produce comparable faces |
| **H4** | Topology is a property of the generator/settings, not inherent to reconstruction | at least one configuration yields <100 connected components | every configuration yields thousands |

H4 is the highest-value question in this spec. If any configuration produces a connected
surface, `smart_decimate.py` unblocks immediately and polygon budget allocation becomes
available to the whole pipeline.

---

## 4. Build first: `tools/verify/mesh_stats.py`

Before any generation, build the measuring instrument. Comparisons across arms are
worthless unless every mesh is measured identically by the same code.

**Required outputs** (JSON to stdout and to `--out`, plus a human-readable line):

| metric | definition |
|---|---|
| `faces`, `verts` | triangle and vertex count |
| `components` | connected components by shared vertices (this is the shell-soup number) |
| `largest_component_frac` | faces in the largest component / total faces |
| `watertight` | boolean, from `trimesh.is_watertight` |
| `face_rect_faces` | faces whose centroid projects inside the front-view face rect |
| `face_rect_density` | `face_rect_faces` / (rect area as a fraction of the figure's projected area) — polygons per unit of face, the number that actually matters |
| `crease_density` | variance of per-vertex mean curvature within the rect. **Advisory only** — measured 2026-08-04 to track hard edges (armour, boot rims, blades), not facial structure: an equal-size lower-body rect scores 3× higher than the head on the same mesh. Report it; do not conclude from it. |
| `bbox`, `maxabs` | for cross-checking that meshes are comparably normalised |

**Implementation notes.** Use `trimesh` for components and watertightness; reuse the
face-rect projection from `tools/smart_decimate.py` verbatim (do not re-derive it — it
projects from the front view rather than using a height band, because a raised weapon
rises above the crown and height bands grab the blade). Curvature: `trimesh.curvature.
discrete_mean_curvature_measure` with a radius of ~1% of the bounding-box diagonal.

**Report TWO rects for every mesh (amendment 1).** The default
`360,240,700,600` is a **bust** rect — measured to cover head, shoulders and upper
torso: 24% of all faces and 43% of the projected silhouette. Keep it, because prior work
is expressed in it and dropping it breaks comparability. **Add a tightened head-only
rect** — crown to chin, ear to ear — determined empirically: overlay the candidate rect
on a front render, confirm by eye that it frames the head alone, and record the exact
rect in the report. Both rects run through the same code path (`--crop`, no code change).
The tight rect is what H1/H2/H3 are actually about; the wide rect is the bridge to
earlier numbers.

**Gate 0 — the instrument must discriminate before it is trusted.** Run it on two
meshes already on disk that are known to differ:
`warrior\texpass\warrior_texpass.glb` (287k, dense) and
`warrior\smart\warrior_final.glb` (150k, decimated and visibly shredded). If
`components` and `face_curvature_var` do not separate these two, the instrument is
broken — fix it before generating anything. **Report the two rows to the Director and
stop for acknowledgement.**

Commit the tool to `facet` as `tools/verify/mesh_stats.py` with a one-line entry in the
README's verify section. This is a durable repo asset, not scratch work.

---

## 5. The arms

Every arm reconstructs from a **clay** input (form-first — style noise makes the
reconstructor read surface detail as geometry). Hold everything constant except the
named variable.

**Fixed across all arms:** the same source character (the Comfy warrior — clay concept
at `warrior\clay_concept.png`), the same seed where the tool accepts one, the same
post-processing (none — measure raw generator output).

| arm | input | generator | settings | tests |
|---|---|---|---|---|
| ~~**A0**~~ | ~~existing mesh~~ | — | — | **DROPPED, amendment 1** — `mesh.glb` is a different character from `clay_concept.png`; it cannot control for arms fed that input |
| **A1** bust crop | `clay_concept.png` cropped to head-and-shoulders, upscaled to the generator's native input size | TRELLIS.2 | `1024_cascade` | H1 (vs A3) |
| **A2** resolution | `clay_concept.png`, full figure | TRELLIS.2 | `512` | H2 (vs A3) |
| **A3** **BASELINE** | `clay_concept.png`, full figure | TRELLIS.2 | `1024_cascade` | the control every other arm is compared against |
| **A4** generator | `clay_concept.png`, full figure | local TripoSG/TripoSR (MIT) | defaults | H3 (vs A3), H4 |
| **A5** generator + framing | bust crop (same as A1) | local TripoSG/TripoSR | defaults | H1 × H3 interaction |

**Run A3 first** — nothing can be interpreted until the baseline exists.

**On A4/A5:** local Tripo has not been stood up on this rig — the store recorded it as
untested. Standing it up is part of this experiment. It is MIT-licensed and runs local;
this is the licence-clean path and is explicitly not the paid cloud service. If it
cannot be installed in under 30 minutes, **report that and skip A4/A5** rather than
burning the session on environment work. The other arms still answer H1 and H2.

**On the bust crop (A1/A5):** crop the clay concept to head-and-shoulders — roughly the
rect used elsewhere in the pipeline, `360,240,700,600` in 1024-space, expanded ~20% for
margin — then upscale with `tools/sr_views.py` to the generator's expected input size.
The point is that the reconstructor sees a face filling its input rather than a face
occupying 12% of it.

**Gate 1 — after A3 and A1 exist.** Render both as **clay** (`head_render.py --clay`,
geometry only, no texture) at matched zoom, side by side. **Send that sheet to the
Director and stop.** If the two faces are indistinguishable, H1 is likely false and the
remaining arms may not be worth running — that is the Director's call, not yours.

State your prediction for H1 in the message *before* showing the sheet, so a surprise is
visible as a surprise rather than rationalised after the fact.

---

## 6. Measurements and deliverables

For every arm that runs:

1. `mesh_stats.py` JSON, all arms in one table
2. A **clay** head render at matched zoom and framing (`head_render.py --clay --views 0`)
3. A **clay** three-quarter head render (`--views=-30,0,30`) — a face can look adequate
   head-on and collapse at an angle
4. Wall-clock generation time and any failures with their exact error text

**One comparison sheet, all arms, same crop and zoom, clay only.** No textures anywhere
in this experiment — texture hides geometry, which is the entire lesson that produced
this spec.

Keep every mesh. Name them `E01_<arm>_<generator>.glb` under
`E:\AI\training\facet_E01\`. Do not commit meshes to the repo (`.gitignore` excludes
them by design); the report references paths.

---

## 7. Report format

Write `docs/experiments/E01-report.md` in the `facet` repo. Structure:

```
## What ran
  arm | input | generator | settings | wall-clock | mesh path | status

## Measurements
  the mesh_stats table, all arms, one row each

## Hypotheses
  H1 | prediction | measured | supported / not supported / inconclusive
  (one line each, no prose verdicts)

## What failed
  exact errors, exact commands, no interpretation

## Open questions the data raised
```

**"Inconclusive" is a legitimate and expected answer.** Prefer it to a stretched claim.

Do **not** write a conclusions section, a recommendation, or a next-steps plan. The
advisor writes those, after the Director has looked at the sheets. Your report is
evidence, not argument.

---

## 8. Standards compliance

Scored 0–3 per the studio's six workflow standards.

**PIN_PER_STEP — 3.** Every arm names its generator, settings, seed and input path
exactly; the measuring instrument is committed code, so any arm is byte-replayable.

**ANDON_AUTHORITY — 3.** Gate 0 halts on an instrument that cannot discriminate; Gate 1
halts for Director review before the remaining arms; the spec explicitly forbids
improvising past a failed gate.

**NAMED_COMPENSATORS — skip, justified.** No irreversible actions. Every operation is a
local file write under a fresh directory; nothing is published, pushed to a package
registry, deleted, or sent outward. The single repo commit (`mesh_stats.py`) is revertible
with `git revert`, owner: the advisor.

**DECOMPOSE_BY_SECRETS — 3.** The instrument (stable) is built and gate-tested before any
generation (volatile); arms vary exactly one factor each; the report format is fixed
independently of results.

**UNCERTAINTY_GATED_HUMANS — 3.** Two mandatory Director gates, placed at genuine
uncertainty rather than at step counts: after the instrument proves it discriminates,
and after the first two arms reveal whether the effect exists at all. Both gates are
framed contrastively — the executor states its prediction first, so a surprising result
is visible as a surprise.

**EXTERNAL_VERIFIER — 3.** The executor never grades its own output: the Director's eye
is the verdict on facial structure, and `mesh_stats.py` — written before the arms exist
and gate-tested against known-different meshes — is the numeric verifier. The executor
is structurally prevented from being both generator and judge.

---

## 9. Handoff

When the report is written, hand it to the Director, who brings it to the advisor
session. The advisor folds findings into `facet`'s README status table, updates the
blocked-upstream note on `smart_decimate.py` if H4 changed it, and writes the next spec.

**Nothing from this experiment enters the memory store.** The repo is the record.
