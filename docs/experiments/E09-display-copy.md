# E09 — the display copy: a web-servable asset that carries its own evidence

**Spec written before the work.** Author: showcase session, 2026-08-04.
**Companion spec:** brand `docs/model-channels-spec.md` — the host side. It defines the
`view.json` schema and the byte budget this experiment must land inside. Neither spec blocks the
other's schedule.

**This experiment does not touch the live E04 line.** The E08 asset is Gate-1 accepted and
frozen; E09 reads it and writes elsewhere. It must not pull the executor off profile extraction →
galleon Gate 0 → the Director's designation.

---

## The question

Can the Gate-1-accepted asset be reduced to something a browser will load, **without losing the
property that makes it worth showing** — that every texel's origin is inspectable?

The display copy is a **derived artifact**. It is not the asset. Its job is to be honest about
what it is and to state, in a number, how far it sits from the thing it depicts.

## Why this is not `gltf-transform simplify`

An exported glTF splits a vertex at every UV seam, and collapse decimation on per-triangle shells
tears holes — a lesson this repo paid a session for. The measured evidence is already in
[README.md](../../README.md): with `--no-weld`, 858,562 → 285,654 → a 150,000 target produced
149,528 faces **"shredded to lace."**

`smart_decimate.py` welds before decimating (merge-by-distance runs before the decimate modifier,
because Blender stores UVs per-loop rather than per-vertex) and carries UV span through the cut.
Its fidelity on this asset is already recorded: **287k → 150k with UV span intact, and a textured
flat render of the welded 150k mesh differs from the 287k source by a mean of 0.47/255**, with
four zero-area triangles (0.0014%) collapsing in the merge.

That is the decimation recipe and the seed of the receipt. E09 does not re-derive it; E09 asks
whether it **survives the two steps the display pipeline adds** — unlit conversion and texture
re-encode — and measures the result.

`--head-crop` is a required argument and is subject-specific. It comes from the W3 entry in
`profiles/character.json`, not from a literal in a script. A global constant must not govern a
local feature.

---

## Predictions, registered before any measurement

**Blindness disclosed per prediction.** P1 and P5 are *not* blind — I have read the prior run's
figures in the README. P2–P4 are blind: no display copy exists and no byte count has been taken.

| # | prediction | blind? | reasoning |
|---|---|---|---|
| **P1** | The welded 150k decimation reproduces its recorded **mean 0.47/255** against the 287k source, ±0.15, on a flat render before any texture re-encode | **no** | the figure is in the README from a prior run on this same asset. What is genuinely open is P1b |
| **P1b** | After unlit conversion and texture re-encode, the combined delta stays **below 2.0/255** | yes | no measurement exists. 2.0 is chosen as roughly 4× the decimation-only figure, allowing the encoder its own budget without absorbing a visible shift |
| **P2** | The flat channel at WebP q≥90, 4096², lands **under 1.5 MB** | yes | painted texture, high entropy — this is the channel most at risk of missing |
| **P3** | Provenance and owner channels compress **losslessly under 1.5 MB** | yes | few distinct colours by construction; PNG should crush them. The source `provenance_atlas.png` is already 664 KB at full resolution |
| **P4** | `asset.glb` with external image URIs lands **under 8 MB** at 150k tris | yes | geometry only; textures do not count against it |
| **P5** | The first-hit depth gate reports **zero hole area** | **no** | `smart_decimate` welds by default and the welded row already shows UV span intact. Run it anyway — the display pipeline adds steps the prior run did not have |

A hypothesis with no prediction cannot be wrong, and one that cannot be wrong teaches nothing.

---

## Arms — one variable

The only genuine comparison here is **decimation target**, and it is forced by brand's byte
budget rather than chosen for taste. 150k was inherited from a run whose purpose was the
pipeline's polygon budget, not a web payload.

| arm | target | varies |
|---|---|---|
| **D0** | 287,170 (no decimation) | control — the accepted asset as-is |
| **D1** | 150,000 | the inherited target |
| **D2** | run only if D1 misses the 8 MB budget | the target, and nothing else |

D2 is **conditional and its threshold is pre-registered**: it runs if and only if D1's
`asset.glb` exceeds 8,388,608 bytes. If D1 lands inside, D2 does not run and the result is D1.
Choosing D2's target after seeing D1's byte count is retuning; the rule for picking it is
declared now — **the largest round target below D1's that projects inside budget by linear
extrapolation on face count**, taken once, not searched.

Everything else — weld distance, head crop, body weight, factor — is held at the profile's
values across all arms.

---

## Metrics

| metric | unit | why this unit |
|---|---|---|
| flat-render delta | mean absolute channel delta /255, display copy vs 287k source, under `--flat` | the same unit the prior decimation run reported, so the numbers are comparable. A STUDIO render is specular highlights on flat-shaded normals, not a texture readout |
| hole area | % of visible surface area that is a first hit from a gate camera on the source but not on the display copy | tests decimation's **failure mode**. Silhouette IoU is structurally blind to holes — it returned 1.00000 on a mesh with a hole clean through it (E06). The instrument is the first-hit depth comparison in `cull_unseen.py`; reuse it, do not rewrite it |
| categorical conformance | count of pixels outside the declared palette, per categorical channel | exact. Any non-zero value is a fabricated class |
| byte counts | bytes, per file | against brand's declared budget |

**Not a metric here: anything judged by eye.** The Director's judgment applies to the *asset*,
and it already has — Gate 1, 2026-08-04. E09 grades a *reduction*, and a reduction is gradeable
on distance from its source. It does not get to re-open acceptance.

---

## Gates

**GATE-HOLE (ANDON).** Any non-zero hole area halts. Decimation's failure mode is torn geometry,
and this is the check that can see it.

**GATE-CAT (ANDON).** Any pixel outside a categorical channel's declared palette halts, measured
on the **served bytes** — after encode, not before. Blending two class colours produces a class
no camera produced. Same defect family as the palette gate; the check is written against the
specification, not against a defect anyone happened to notice.

**GATE-BUDGET (report, not halt).** Byte counts are reported against brand's declared budget. A
miss is a **result**, escalated to the Director with the numbers — not a licence to move the
budget or to reach for lossy compression on a categorical channel.

Three gates, and the first two can fail. If a gate fires, report it with its evidence and halt.

---

## What gets built

1. **`asset.glb`** — welded decimation at the chosen target, `KHR_materials_unlit` set, **image
   URIs external** rather than embedded, so a channel switch is an image fetch and not a model
   reload. `trimesh` does not emit the unlit extension; whatever adds it is a named step in the
   recipe, not an unrecorded post-process.
2. **`ch_flat.webp`** — the finished atlas. Lossy is permitted here.
3. **`ch_provenance.png`** — from the existing provenance atlas. Lossless, nearest-filtered,
   palette declared.
4. **`ch_owner.png`** — from `_owner.npy`, the standing sidecar `project_twins.py` already writes
   ("which VIEW won each texel, int8, −1 where nothing styled it"). Lossless, palette declared.
5. **`view.json`** — filled per brand's schema, including `provenance.recipe` as **exact argv**
   and `provenance.receipt` as the measured P1b number.
6. **A poster** — under 300 KB, from the existing `renders_flat/` set.

### Why the owner channel ships in the first build

E04 Ruling 1 established that an inter-camera ownership seam is **provenance-blind by
construction** — both sides of the edge are the same provenance class, so the instrument that
decided E07 cannot see it. The crown blotch the Director named is exactly that. A viewer with a
provenance channel and no owner channel would show a reader a clean-looking map of a region that
carries a named, measured defect. Shipping both is not scope creep; shipping only one would
misrepresent the asset.

It also doubles as brand's genericity fixture: the fourth channel must arrive by editing
`view.json`, with zero brand code change.

---

## Out of scope

- **Re-opening Gate 1.** The asset is accepted and frozen. E09 reduces it and measures the
  distance; it does not improve, retouch or re-grade it.
- **The galleon.** No E04 asset enters this experiment.
- **Any change to `smart_decimate.py`, `project_twins.py`, or the texture pipeline.** E09 reads
  their outputs. If it needs a change in one of them, that is a finding to report, not a licence
  to edit.
- **Lossy compression on any categorical channel**, at any byte cost.
- **The brand side.** Schema, CLI, route and fixtures are the companion spec's.

---

## Standards compliance

Scored 0–3 against the six workflow standards. Below 2 carries a named remediation.

**1. PIN_PER_STEP — 3.** Every arm's invocation is recorded as exact argv in
`view.json.provenance.recipe`, and the artifact it produced is SHA-256'd by brand. Held constants
are named and sourced from `profiles/character.json` rather than from literals. A display copy is
replayable from its own metadata.

**2. ANDON_AUTHORITY — 3.** Two halting gates, both testing the operation's failure mode rather
than its success mode: GATE-HOLE uses the first-hit depth comparison because IoU is blind to
holes, and GATE-CAT measures served bytes because encoding is where blending happens. Both have a
describable non-zero. The budget deliberately does *not* halt — it is a diagnostic, and promoting
a diagnostic to a halt is an error this repo has already made.

**3. NAMED_COMPENSATORS — 2.** E09 performs no irreversible external action: it reads frozen
inputs and writes new files under a fresh output directory. The irreversible steps (committing
binaries, publishing, releasing) all live on the brand side and are tabled there with owners. Not
3: the compensator for "a bad display copy is already published" is brand's Pages revert, which
this spec inherits rather than rehearses.

**4. DECOMPOSE_BY_SECRETS — 3.** The seam is the point of both specs. Subject vocabulary
(provenance classes, owner indices, camera yaws, captions) lives in `view.json`, authored here;
the mechanism lives in brand. This is the same boundary facet formalised this week as subject
profiles — code holds principles, data holds subject vocabulary.

**5. UNCERTAINTY_GATED_HUMANS — 2.** One gate to the Director, on a budget miss, framed
contrastively: *you probably expect a display copy to just be smaller; if D1 misses the budget the
honest options are a lower polygon target or a smaller texture, not a lossy categorical channel —
and the third is foreclosed by GATE-CAT.* Not 3: the gate is prose here, not a check.

**6. EXTERNAL_VERIFIER — 2.** The receipt is measured by facet's instruments and independently
re-derived by brand as a SHA-256 over the served bytes; GATE-CAT runs on **both** sides, on
different inputs (pre-encode here, served bytes there). Not 3: the same session authored both
sides. The receipt should be reproduced by a session that did not produce it before the number is
quoted anywhere public.
