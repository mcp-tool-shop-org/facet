---
title: How this repo is run
description: Three roles, a spec-report-ruling loop, and why every one of these rules was paid for rather than chosen.
sidebar:
  order: 5
---

This page is about **method**, not about the pipeline. It is here because the method is
load-bearing: an earlier arc of this project ran ten sessions in which each session
judged its own output, wrote its conclusions to a shared memory store, and the next
session read those conclusions as established fact. Nothing in that loop was checkable
and nothing was gated on the Director's eye, so errors compounded silently for weeks.

Every rule below was paid for. In the single session that produced this repository,
**six inherited or asserted claims were falsified** — and every one of them took minutes
to overturn *because it sat next to runnable code*.

## Three roles, deliberately separated

| role | does | must not |
|---|---|---|
| **Director** | sets direction; judges every artifact by eye | — |
| **Advisor** | writes specs, rules on reports, folds findings into the repo | execute, or grade its own rulings |
| **Executor** | runs the spec, measures, reports evidence | decide what results *mean*, or judge quality |

The separation is the whole point: **the session that designs an experiment does not
grade its results, and the session that runs it does not decide their meaning.**

## The loop

```
spec written BEFORE the work  →  report written AFTER  →  advisor ruling LAST
```

A spec carries the question, hypotheses **with predictions**, arms varying one thing
each, the metrics, the gates, an explicit out-of-scope section, and a standards
compliance block. Amendments are appended in place with dates and reasons — a spec that
hides its own corrections is the thing this repo is trying to get away from.

## The rules that cost the most

**An inherited claim is a hypothesis wearing a fact's clothes.** Checking one costs
minutes; building on one costs a session. If a spec, README or handoff asserts a number,
verify it before designing around it — *including numbers written by the advisor*.

**State a prediction before you look**, and disclose whether it was blind. A hypothesis
with no prediction cannot be wrong, and one that cannot be wrong teaches nothing.

**Stop at every gate; never improvise past one.** A session that changed a parameter and
re-ran when a gate fired hit the same gate harder.

**A negative result is a full success.** Say so plainly and stop, rather than tuning
toward a number.

**Correct in place, with the measurement that overturned the claim.** Never quietly
delete a wrong statement — the correction is more useful than the original.

**A check that cannot fail is not a check.** Before trusting a zero, ask what a non-zero
would have required. A cull gate returned `1.00000` on a mesh with a hole clean through
the torso, because silhouette IoU is structurally blind to holes behind visible surface.

**When you fix a root cause, find its other consumers.** One fix corrected the control-image
path and left the *same function on the same render* still losing a quarter of the
silhouette elsewhere. A root cause has as many sites as it has callers.

**A global constant must not govern a local feature.** Three instances, each costing a
session: a rectangle measured on one silhouette applied to a mesh 38% narrower; an
erosion tuned on a wide figure eating 480k texels where the surface turns edge-on; an
edge-distance scaled by global figure width leaving a 15 px blade with no interior.

**Canon is not a taste question to be routed around.** When the real question is *is this
the right thing*, a measurable proxy is not a conservative substitute for asking — it is
a different question with a number attached. Ask, and show the artifact at full size.

**A gate that a scripting accident can separate from the action it gates is not a gate.**
An invariance halt fired on stroke 7 and the commit ran anyway, because the check and the
commit were chained in one shell call that walked past the failing exit code. The check
lives *inside* the tool that performs the irreversible step, with no skip flag.

## Judging artifacts

- **Textures under flat light** — a Workbench STUDIO render is not a texture readout.
- **Geometry under clay** — texture hides geometry.
- **At the Director's zoom, never from a contact sheet** — the defects that decide
  acceptance are invisible at thumbnail scale.
- **Beside the reference, with provenance.** The cheapest diagnostic in this repo is a
  `reference | asset | provenance | error` sheet on one page. Build it *before* the
  metrics, not after them: a number tells you a region is wrong; the sheet tells you what
  it was supposed to be, which is the part that decides what to do next.

## The advisor's record, kept for calibration

A future advisor should know which parts of this repo to distrust. In the founding
session the advisor was wrong about the shell-soup premise, the clay provenance, the
double-subscribe diagnosis, the head-pixel multiplier, the halo hypothesis, and two pass
conditions. In a later experiment it was wrong about two of its own gates — one measuring
a proxy that inverted and halted a correct arm, one defining a pass condition as a
fraction of a baseline nobody had measured. Both were caught by an executor who ran them
as written and reported the evidence rather than tuning past them.

The advisor was useful at: ruling once evidence was in, killing options with reasons,
refusing to commission a metric where no honest one existed, bounding an expensive arm
before spending it, and correcting the record in place.

**Deciding is the job. Predicting is not.**

The full version of this page, with every rule and what it cost, is
[CLAUDE.md](https://github.com/mcp-tool-shop-org/facet/blob/main/CLAUDE.md) in the repo
root.
