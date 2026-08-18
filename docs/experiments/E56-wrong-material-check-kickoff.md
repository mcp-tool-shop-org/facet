# E56 — is there an honest check for the defect class that actually decides acceptance?

**Dispatched 2026-08-17 by the advisor seat. Opus executor, background, open line.**
This document is the spec. Mid-flight rulings are appended here with dates.

**Opus rather than Sonnet, and the reason is stated:** this seat must *design an instrument
and then try to kill it*. This repo has lost four experiments to metrics that could not
separate an asset the Director accepted from one he rejected, and each looked sound while it
did so.

---

## The defect class, named precisely

**A large region of the wrong material, smooth inside itself, on an otherwise-correct
object.** A steel blade wearing flesh. A boot wearing gold. This is the class that decides
acceptance here, and the repo already knows why every cheap check misses it:

> E07 graded four arms with blotch counts, speckle, a step ratio and a flattening guard —
> **four of the five are 5×5 high-pass statistics, and the fifth is indifferent to where a
> colour lands.** Such a region is smooth inside itself and contributes only its rim to
> every one of those numbers. So an arm took source distance down 70×, mean fallback to zero
> and speckle below A0 — **and the asset was unchanged to the eye.**

Brief #19's research grounding says the same thing from the outside, and it is worth having
because it means this is not a facet-shaped hole:

- **CLIPScore is the weakest metric measured and never ranks top** — Spearman 0.223–0.535
  across compositional categories (Kasaei, Aghayari, Marioriyad et al. 2025,
  arXiv:2509.21227). *Gate-status: existence-verified, groundedness unverified.*
- **Texture/material is the worst-detected attribute class there is** — texture-binding
  accuracy collapses to **23–43%** while colour binding on the same models holds **93–97%**,
  and the best VLM judge reaches only 67.4% human agreement (Hayes, Goldblum, Somepalli et
  al. 2025, arXiv:2512.02161). *Same gate status.*
- **Embedding metrics pool the whole image into one vector**, making them structurally
  insensitive to localized semantic violations (Hartwig, Engel, Sick et al. 2025,
  arXiv:2403.11821).
- **A dedicated search found nothing benchmarking this exact class.** Confirmed gap.

⚠ **Those citations were run through an external citation gate and most returned
`not_addressed`** — the oracle reads title+abstract only, so a figure in a results table
reads as unaddressed. **Treat them as motivation, never as evidence.** If any of them
becomes load-bearing for your design, read the paper.

## The question

**Can an honest automated check separate an asset the Director rejected from one he
accepted, on this class — and if not, say so.**

**Refusing to commission a metric where no honest one exists is a recorded virtue in this
repo**, listed among the things the advisor was useful at. A clean *"no check I can build
discriminates, and here is the evidence"* is a **full success** and is a better outcome than
a number that looks reasonable.

## The validation protocol — this is not optional and it comes FIRST

The repo's own law, and it is the whole method:

> **Validate a metric against a rejected artifact before building an experiment on it.** Take
> something the Director has already turned down, and the region he named, and confirm the
> number fires there. […] A metric that cannot separate an asset he rejected from one he
> accepted is not a metric.

So the order is: **find the rejected artifacts and the named regions first**, then design
against them. Not the reverse. A check designed first and validated second is a check tuned
to pass.

**Where the labelled material is.** Search the record for the Director's own verdicts —
`record_query` is mounted and its pointers are the product. Known anchors to start from,
each of which you must verify rather than trust:

- **E07** — the flesh blade. The Director read the thesis off panel 2: *the blade is flesh
  where the reference is steel*. That is a rejected asset with a named region.
- **E08 Gate 1** — the accepted asset (`facet_E08\ARMB\`). The Director's acceptance is what
  makes it the positive class.
- **known-defects.md** — carries several named, Director-ruled classes with dates, including
  ones ruled *unacceptable* and ones ruled *cosmetic*. The cosmetic/unacceptable split is
  itself a labelled boundary and may be more useful than the accept/reject one.
- **E40 / E49 / E50 / E51** — arms whose sheets he rejected or accepted, several with region
  boxes already transcribed in `tools/s3_sheet_regions.json`.

**Report the label set you assembled, and its size, before any check is scored.** If the
labelled set is too small to discriminate, that is the finding — say it and stop.

## What an honest check may and may not be

- **It may not be a 5×5 high-pass statistic**, or anything whose response to a large smooth
  region is its rim. That family is already falsified for this class.
- **It may not be a global pooled embedding similarity.** Structurally blind here.
- **It must be gated on the quantity of interest, not a proxy for it.** *Is this region the
  wrong material* is the question. *Is this region unusual* is a different question with a
  number attached.
- **Below a chroma floor, hue is not a colour.** Any hue statistic carries its chroma or it
  is not quoted, and a circular statistic is required for hue centres — a garnet family
  straddles the 0/360 wrap and an arithmetic median reported +49.1° where the truth was −8.4°.
- **A material is not a palette band alone.** `palette_gate.py` exists and is the nearest
  prior art; it declares bands from the spec's named materials with a chroma floor and a
  largest-connected-component rule. **Enumerate it before building anything** — and note that
  it answers *is anything outside the declared palette*, which is a related but different
  question from *is this surface wearing the wrong one of the declared materials*.

## What you can now use that E07 could not

The canon is data. `canon/w3.surfaces.json` names, per surface, the material that belongs
there. `tools/canon_gate.py` resolves it, `tools/canon_worksheet.py` can bind surfaces to
per-view region boxes. **The question "is this region the wrong material" is answerable in
principle for the first time**, because for the first time something declares what the right
material *is*.

⚠ **But the binding is thin and you must measure how thin.** The spatial bind exists in the
worksheet; `scopes.views` are declared **empty** by construction, and one region name in
`tools/s3_sheet_regions.json` is the pre-rename `skirt`. Establish what fraction of the
figure you can actually attribute to a named surface before designing a check that assumes
you can.

## Gates — halt and report

- **Gate A — the labels are the Director's, not yours.** Every artifact in the positive and
  negative class traces to a recorded verdict with a locator. **You may not label an artifact
  by eye.** If a class has fewer than two members, **halt** and report the label census.
- **Gate B — the check fires on the rejected artifact at the named region.** If it does not,
  the check is dead, and reporting it dead is the result. Do not tune it and re-run; a
  session that changed a parameter and re-ran hit the same gate harder.
- **Gate C — the check must be shown capable of NOT firing.** Run it on the accepted asset at
  a region the Director did not name. A check that fires everywhere is not a check, and a 0
  that could not have been non-zero is not evidence.
- **Gate D — write only under `E:\AI\training\facet_E56\`.** Every other `facet_E*` tree is
  read-only. Do not read the `facet_E50`–`E55` working trees.

## Predictions

Write `predictions.md` before scoring anything. Cover at minimum:

- **P1** — the size of the labelled set you will assemble, per class, as a band. ⚠ **Thirteen
  consecutive arcs have missed on population-shaped predictions.** Check every member *has*
  the property before predicting how many there are; predict each clause of a conjunction
  separately, because the join tracks the rarest clause.
- **P2** — whether any check you can build separates the classes, with your reason.
- **P3** — what fraction of the figure is attributable to a named canon surface today.

Disclose blindness: you will have read this spec, which argues the refusal branch on purpose.

## Terminus

A report, and a sheet: **reference | asset | provenance | error**, at the Director's zoom,
native pixels, defects first — the cheapest diagnostic in this repo and the one E07 ran four
arms without building. Reuse `tools/evidence.py` or `tools/verify/montage.py`; seven seats
have each written their own sheet builder and an eighth is avoidable.

## Rules that bind this seat

1. **Never judge whether output is good.** *verified, shipped, works, decisive, validated,
   proven* do not belong in the report. You measure; the Director judges.
2. **A negative result is a full success**, and the refusal branch is live here.
3. **Stop at every gate.** Do not change a parameter and re-run.
4. `handoff.md` first, kept current.
5. Do not delegate your core measurement to a child agent.
6. **Do not touch any public surface** — README, README.*.md, CHANGELOG, SHIP_GATE,
   `site/**`, or repo metadata. Those are lead-authored by law. If your work implies a change
   to one, **say so in the report** and the advisor writes it.
7. Do not commit. Do not `git add -A`. No memory-store writes.
8. **Zero spend** — no GPU, no cloud, no generation.
9. Gates `raise`, never a bare `assert`. Tests ride any tool change — **your test file is
   `t97`** (`t96` is the outside channel's; verify before claiming either).
10. Absolute python `E:\AI-Models\trellis2-env\Scripts\python.exe`; `pytest` needs
    `--basetemp=<scratch>`; scripts create their own output dirs.
11. **Read every listing complete.** And on this rig: `grep -c $'\r'` does **not** expand in
    the Bash tool — it counts lines containing the letter *r*. Use `git ls-files --eol`.
    Console is cp1252: keep tool output ASCII or a print will kill a script mid-sweep.
12. **The count surfaces (T34) are the advisor's** — currently 1319 / 1265 / 54. State what
    your change-set assumes and reconcile nothing.

## Out of scope

Any generation. `tools/canon_gate.py` and `tools/canon_worksheet.py` (a second builder is
live in those). The scope lists — filling them is a human walk. Deciding whether an asset is
acceptable; you supply the instrument, or the evidence that none exists.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Every label must trace to a recorded verdict with a locator, and the instrument's inputs are named by path; scored 2 because this dispatch does not pin the executor's own model/prompt hash. |
| ANDON_AUTHORITY | 3 | Four gates. Gate B halts on the check failing to fire where the Director already said the defect is, which is the direction that makes a metric worthless; Gate C halts on the opposite direction. |
| NAMED_COMPENSATORS | 3 | Writes confined to `facet_E56\` plus one repo report. Compensator is delete-the-tree; owner the advisor. No irreversible call. |
| DECOMPOSE_BY_SECRETS | 2 | Label assembly, the check, and the sheet are separable; the module boundary is the seat's. |
| UNCERTAINTY_GATED_HUMANS | 3 | No pass condition. The terminus is a sheet for the Director's eye, and the refusal branch is explicitly available to the seat rather than reserved to the advisor. |
| EXTERNAL_VERIFIER | 3 | The labels come from the Director — a different authority entirely from the seat proposing the check — and Gate C forces the check to be run where he did *not* name a defect. That is a generator/verifier split with the human as the verifier, which is the strongest form available here. |

**No pass condition, by design.** No calibrated threshold exists for "how well must a check
separate," and inventing one while looking at the scores is retuning however principled the
reasoning.
