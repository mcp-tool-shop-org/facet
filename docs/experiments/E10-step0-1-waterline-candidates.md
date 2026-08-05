# E10 Step 0.1 — `waterline_z` candidates: the ladder is drawn, the line is not placed

**Executor session, 2026-08-05.** Run under [E10 Ruling 1](E10-ruling.md), which cleared
Step 0 and confirmed this item as the one no outcome of that ruling could waste. Written
after the work. **No line is chosen here.** The Director places it in one sentence.

Artifacts, in `E:\AI\training\facet_next\E04_stroke\e10_step0\`:
`STEP0_waterline_candidates.png` (full, with a 5% ruler) ·
`STEP0_waterline_candidates_ZOOM.png` (hull foot, 5×) · `waterline_candidates.json`.
Tool: [`tools/e10_waterline_candidates.py`](../../tools/e10_waterline_candidates.py).

---

## The ANDON fired on the first run, and it caught a real trap

The tool checks its own projection before using it: project the mesh's z extremes to image
rows and compare against the render's own raycast silhouette. First run:

```
[proj] mesh z_max -> row 290.24 (silhouette top 84, d=206.24)
ANDON: the projection disagrees with the raycast silhouette by more than 2 px. HALT.
```

**206 px.** The cause is not a formula slip — it is a shared convention with no
documentation outside the file that owns it. `texpass_iter.load_scene()` does not raycast
the GLB's own coordinates:

```python
vmax = np.abs(v).max()
v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / vmax * 0.5
```

It **re-axes Y-up → Z-up and normalises by max-abs**. Every world quantity in every
`cam.json` this pipeline has ever written is in *that* frame, not the file's. Reading a
`cam.json` against the raw GLB silently puts every z on the wrong row while producing a
sheet that looks entirely plausible.

Applying the same transform reproduces the beam camera's operands **exactly**:

| operand | recomputed | `cam.json` | delta |
|---|---|---|---|
| `bmid` (all three axes) | `[0.0006720531666543073, -4.863785143496835e-05, 0.00031705981776916636]` | identical | **0.0** |
| `h_ext` | 1.2023816959746965 | identical | **0.0** |

and the projection check then lands at **0.34 px** on both ends against an 855-row
silhouette.

**This is the fourth copy of a convention that must agree.** `texpass_iter.py`'s own header
already warns that the fit-axis block has three copies — `turn_render.py`,
`silhouette_masks.py`, and itself — and that all three must agree. The normalise-and-re-axis
step is a *fourth* thing any new consumer of a `cam.json` must replicate, and nothing
outside `texpass_iter.py` says so. It is now replicated in
`e10_waterline_candidates.load_emit_frame()` with the source named and the check that
proves it. **Flagged for the shared-code bundle in Ruling 28's queue** — this belongs
beside the registry rebuild and the frame-legality assert, as one exported function rather
than a fifth transcription.

## The founding exemplar, re-measured — and the record's two numbers reconcile

The record carries **two different counts** for the same band: the E10 spec says *2,002 px,
x 398–686*, and Ruling 20 says *2,272 px*. Re-measured from the artifact
(`twin_7_REJECTED_seed770700.png`, chroma > 12.0, hue 240–273°, inside the exact
silhouette `masks/galleonclay_7.png`):

```
band 2272 px in 17 components (largest 2002) | rows 896-939 | x 398-786
bbox of the largest component: x 398-686, y 896-939
median L* 31.5  C* 14.2  hue 262.2
```

**Both numbers are right and they measure different things.** 2,272 is the total; 2,002 is
the largest connected component, and *its* bbox is the x 398–686 the spec quotes. The
apparent discrepancy dissolves — and the measurement reproduces both figures to the digit
along with the record's `h 262.6, C* 14.4, L* 31.7` (here 262.2 / 14.2 / 31.5, median
against the record's statistic). Nothing is corrected; the record was consistent, and it
now says which statistic is which.

Per Ruling 1 decision 6, this exemplar validates the band's **geometry** only. It is not a
colour or content target — what it painted is the dynamic half that now belongs to the
shader.

## The measured anchors and the ladder

Frame: the emit frame described above. **A z with no frame is not a coordinate**, so every
number below carries one.

| quantity | value |
|---|---|
| hull lower extent (keel), `z_min` | **−0.47956** |
| mesh z span (keel → masthead) | 0.95975 |
| exemplar band top → z | **−0.43095** (row 896) |
| exemplar band bottom → z | −0.47918 (row 939) |
| span between the two anchors | 0.04861 — **5.06% of the hull's z-span** |

`prep_uv.glb` and the accepted `galleon_final.glb` occupy the **identical** z range
(disagreement 0.0), so the candidates are equally valid against the shipped asset.

| line | z | % of hull z-span | image row | % of the beam figure below it |
|---|---|---|---|---|
| **A** | −0.46335 | 1.69% | 924.9 | 2.31% |
| **B** | −0.44715 | 3.38% | 910.4 | 4.79% |
| **C** | −0.43095 | 5.06% | 896.0 | **7.43%** |

**The fractions are a ruler, not thresholds.** A and B are 1/3 and 2/3 of the measured span
between the two anchors the spec names; C *is* the exemplar's band top. Nothing here was
derived from an outcome.

One consistency worth noting: C puts **7.43%** of the beam silhouette below it, and Ruling
20's exact-band check was defined on the *"lower 7% of figure"*. The two land on the same
place from different directions.

## What the sheet shows, described and not judged

**The ladder is compressed.** Because the exemplar painted only at the hull's foot, the
whole keel→C span is 5.06% of the ship's height, so A, B and C sit **14 px apart** in a
1024-row frame. Text on the lines collided into an unreadable smear on the first sheet —
a defect in this tool, fixed by moving the labels to a legend and adding a **ruler ticked
every 5% of hull z-span** so any answer is expressible, not only the three lines.

Where they fall, as description: **C** sits at the transition from the hull's dark lower
planking to the lighter mid-hull. **B** crosses the dark bottom planking. **A** sits near
the base of the hull's curve. Because the hull has rocker, a horizontal z-plane meets it at
mid-length while bow and stern rise above all three.

## What is needed

**One sentence from the Director**: pick a line, or move it — *"a bit above C"*, *"at the
10% tick"*, *"where the dark planking starts"* are all answers this sheet can carry into a
number. It then lands in `profiles/ship.json` with its why and provenance, and Step 0.2
builds the contact mask against it.

## Standards compliance (this step)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every number read from `cam.json`, the mesh, or the exemplar; the frame convention is replicated with its source named and proven equal to the camera's own operands; fractions stated in the output and the JSON |
| ANDON_AUTHORITY | 3 | the projection check halted the first run at 206 px and passed the second at 0.34 px — a check that demonstrably can fail; a second halt guards the exemplar measurement returning nothing where the record says a band exists |
| NAMED_COMPENSATORS | 3 | writes only into `e10_step0/`; undo is deleting that directory; the accepted asset is read, never opened for writing |
| DECOMPOSE_BY_SECRETS | 2 | the two anchors are the spec's; the subject's chroma floor comes from canon. Not 3: the 1/3–2/3 ruler lives in the tool rather than in a profile, which is correct only because it is not a value anything downstream consumes |
| UNCERTAINTY_GATED_HUMANS | 3 | the whole step is one uncertainty gated on one sentence, with a ruler so the answer need not be one of the three offered |
| EXTERNAL_VERIFIER | 3 | the tool grades nothing; the frame convention was verified against an artifact written by a different tool on a different day, and the exemplar measurement against two independently recorded figures |
