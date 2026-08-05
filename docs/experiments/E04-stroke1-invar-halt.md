# E04 stroke 1 — HALT: the invariance ANDON fired, and it is A32's root cause at its second consumer

**Executor session, 2026-08-05.** Ruling 25's sweep ran green, the selftest passed at the
ship frame, stroke 1 (`y+300_e+00`) emitted, uploaded, built, link-checked, dry-ran,
estimated at 0 credits, submitted and returned. **`brush_cloud_step.py invar` HALTED it.**

**Nothing was committed.** `atlas.png`, `holes.png` and `styled_mask.npy` are byte-identical
to the stage-1 seed and no `atlas.prev.png` exists — a commit writes that before it touches
anything, so its absence is the proof the sequence stopped where it should.

```
[invar] outside the dilated figure: 803,683 px
[invar]   |edited - emitted|  mean 0.216  max 106.0  levels (8-bit)
[invar]   pixels over 4 levels: 2,243 (0.279%)  largest connected component 1,515 px
ANDON: the residual outside the figure is CONCENTRATED - largest component 1,515 px
over 4 levels. ... The inpaint is repainting the backdrop ... HALT.
```

---

## What it fired on, measured

The check calls a pixel *outside the figure* when the **emitted render is within 1.5 levels
of 107** — that is, of `0.42` grey. E08 Amendment 32 recorded why that operand is unsound:

> `0.42` is ALSO `project_twins`' `--hole-grey`, so an unpainted HOLE ON REAL SURFACE
> renders at exactly the background value and is **indistinguishable from background by
> colour, by construction**.

A32 fixed that operand **inside `texpass_iter`'s commit**, by intersecting with the geometry
mask `emit` saves as `hit.png`. **`brush_cloud_step.py invar` was not fixed** and still keys
on colour. Measured against `hit.png`:

| | px |
|---|---|
| the check's "outside the figure" set | 803,683 |
| …of which actually **on geometry** | 2,084 (0.26%) |
| **hot** pixels (>4 levels, outside) | 2,243 |
| …of which **on geometry** | **1,999 (89.1%)** |
| …off geometry | 244 |

| the 5 largest hot components | px | on `hit` | in the job mask | in `thin` |
|---|---|---|---|---|
| **cc 17 — the one that halted** | **1,515** | **93%** | **93%** | 0% |
| cc 11 | 342 | 100% | 100% | 0% |
| cc 10 | 82 | 78% | 67% | 11% |
| cc 13 | 71 | 100% | 100% | 0% |
| cc 5 | 63 | 100% | 100% | 0% |

**The component that halted the run is 93% real surface and 93% inside the job mask — holes
the brush was explicitly told to paint.** It is a 182 × 22 px band at x 500–681, y 919–941 of
1072 × 1024: the lowest 10% of the frame, on the hull's foot — the least-covered region on
this subject (19.44% styled) and precisely what a side stroke was dispatched to serve.

`invar_cc1_emitted_edited_hit.png` shows it at full size, *emitted | edited | geometry*: a
ragged grey fringe under the hull in the emitted render, painted dark tarred planking in the
brush output, over geometry that extends exactly that far down.

## The counterfactual, with A32's own operand

Same residual, same bounds, "outside the figure" taken from **geometry** instead of colour:

| | colour operand (shipped) | geometry operand (A32's) |
|---|---|---|
| outside-the-figure set | 803,683 px | 799,733 px |
| mean residual | 0.216 lv | **0.020 lv** |
| max | 106.0 lv | **11.0 lv** |
| pixels over 4 lv | 2,243 | **63** |
| largest connected component | **1,515 px** | **40 px** |
| verdict against the shipped bounds (mean ≤ 1.0, cc < 200) | **HALT** | **PASS** |

The bounds are not the problem and are not touched. **The operand is.**

## This is CLAUDE.md's own rule firing on the repo

> **When you fix a root cause, find its other consumers.** A root cause has as many sites as
> it has callers. Grep for them when you fix one.

A32 had two consumers of the colour proxy. One was fixed on 2026-08-04 — after it produced
a false ANDON that a chained shell then committed past, costing 47,020 texels and a void.
The other is `brush_cloud_step.py invar`, and it has been sitting unfixed since, on a check
that only runs when a stroke flies. This subject's first stroke is the first time it has run
since the fix.

It is also the same shape as **Ruling 25's own finding one leg ago**: `texpass_iter` was the
third frame consumer that a two-consumer fix skipped. Two instances in two legs of *a fix
applied at some of its sites*.

## What I have NOT done

- **Not fixed `invar` and re-run.** A gate fired; *"stop at every gate, never improvise past
  one — a session that changed a parameter and re-ran when a gate fired hit the same gate
  harder."* The evidence above is what the halt report owes, not permission to continue.
- **Not committed stroke 1.** State byte-identical to the seed, no `atlas.prev.png`.
- **Not re-rolled.** Nothing about this output is a content failure; the brush painted the
  hull's foot, which is what it was asked to do.
- **Not touched a bound.** The 1.0-level and 200-px bounds are `brush_cloud_step`'s own and
  stay exactly as they are.

## The artifact is on disk and costs nothing to reuse

`inpainted.png` and its seed-stamped copy `inpainted_s770700.png` are in the job directory,
with `render.png`, `mask.png`, `hit.png`, `thin.png`, `cam.json` and the saved workflow
`out/stroke_1_y+300_e+00_workflow.json`. If the ruling clears it, stroke 1 commits from what
is already downloaded — **no regeneration, no second submission.**

## Cloud record for this leg

One submission. `prompt_id 8ef7d010-89c1-473b-ba74-23b469c6fd7e`, `estimate_credits` **0
credits — no paid API nodes**, `dry_run` `status: validated` with the standing LoRA warning
(*"not found in the bundled node index"* — the documented trap: API surfaces never see
account imports, and this exact card generated all eight twins). Pre-flight guard **PASS**,
link topology checked in code on the saved file: 17 nodes, no self-links, no dangling
targets, no non-terminal orphans.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Workflow JSON saved before submission and link-checked in code; the probe reproduces the check's own two masks exactly before comparing them against geometry |
| ANDON_AUTHORITY | **3** | The gate fired and the run stopped, with the atlas provably untouched. The evidence was gathered *after* halting and changes nothing |
| NAMED_COMPENSATORS | **3** | Nothing to undo — no commit, no profile edit, no tool change. The downloaded artifact is seed-stamped and reusable |
| DECOMPOSE_BY_SECRETS | **2** | Not this halt's axis; the profile is untouched. `skip:` |
| UNCERTAINTY_GATED_HUMANS | **3** | The counterfactual is given in full so the ruling can see what the check says both ways, and the crop is written at full size for the eye rather than described |
| EXTERNAL_VERIFIER | **3** | The check was tested against an operand it does not control — `emit`'s geometry mask, written by a different tool — and the two disagree by 1,515 px against 40 |
