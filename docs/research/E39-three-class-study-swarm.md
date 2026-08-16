# E39 — the three-class study-swarm

**Dispatched 2026-08-16 at the Director's word:** *"Send a study swarm studying each of the 3
classes and then we'll run experiments on the classes simultaneously through 3 spawned Sonnet
sessions, once we've learned more of the levers involved. Search for messageboards, etc for
people who have encountered said class. This is the way to solve a problem quickly, by learning
from the trial and errors of other users."*

Written to disk **at dispatch time, before any agent returned**, so the dispatch is the record
rather than a reconstruction. Findings and the verification receipt are appended below as they
land.

Governing doctrine: `memory/research-grounded-advisor-protocol.md` (study-swarm), read at this
seat before the dispatch was written, per its own standing rule.

---

## Why three swarms and not one

[E39 Task 1](../experiments/E39-w3-polish-kickoff.md) split W3's blotchiness into three classes
that had been treated as one defect. They have different carriers, and therefore almost certainly
different fixes:

| class | what it looks like | measured carrier |
|---|---|---|
| **GOLD** | gold across the green tunic, the skirt, the boot tops | **`reference` 91.05%, enrichment 0.99× — base rate.** The twin projection carries it |
| **GREEN** | cloth green down the sword grip and other non-cloth surfaces | **`brush` 5.49×, `dilation` 3.34×**, `reference` down to 68.46% |
| **BLADE** | steel wearing gold and rust; the Director's *"largest single offence"* | the **only** `dilation`-dominant large region, at a **48.3% plurality** — a mixed case |

Aiming one swarm at "W3 is blotchy" would have produced one blurred answer to three questions.

## The Director's method note, and how it reconciles with the protocol

He asked explicitly for **messageboards and other users' trial and error**, not only papers. The
protocol's sourcing standard cautions against citing *"a summary or social thread"* — that
caution is about citing a **thread's summary of a paper**, and it does not apply here. **A
practitioner describing a defect they personally hit, in their own thread or issue, IS the
primary source for that experience.** CLAUDE.md's rule binds identically either way: *resolve
every external citation at its primary source*, which for a forum thread means opening and
reading the thread rather than a search snippet.

This is not a novelty. The last practitioner swarm this repo ran returned, in about twenty
minutes, a merged upstream Blender fix (PR #161752) for a defect three arcs had hunted in the
wrong subsystem.

## The five questions dispatched (one agent each, in parallel, single message)

1. **GOLD — view disagreement vs in-view hallucination.** When independently-generated per-view
   images are projected onto one mesh, what makes a region wear the wrong material? Required to
   distinguish *(a) the views disagree with each other* from *(b) one view hallucinated the wrong
   material internally* — **these need completely different fixes and conflating them is the
   specific error this arc exists to avoid.**
2. **GREEN — chart-constrained padding.** How do practitioners stop dilation/padding pulling
   colour across unrelated UV islands, and what is the toggle actually *called* in Substance,
   Marmoset, xNormal, Blender, Mari? Our flood predicate has no island constraint at all, and the
   one patch the record already falsified (`& valid`) is **not** the same predicate as
   *same-island*.
3. **BLADE — thin hard-surface geometry.** What goes wrong specifically with thin, flat props in
   UV atlasing, baking and projection — and does the trade texture props on a **separate atlas**?
4. **The shipping-tool vocabulary.** Multi-view projection texturing is decades old. What do
   mature tools and photogrammetry pipelines do that we do not, and **what are those features
   named**? A solution we cannot name is one we cannot search for.
5. **Diffusion texture generation in practice.** What do people *actually running* SyncMVD,
   MVPaint, TexPainter, Paint3D, TEXTure, Hunyuan3D, ComfyUI 3D report — failure modes, VRAM,
   mesh requirements, whether it worked on a character — rather than what the papers claim.

Every prompt carried: our measured numbers so agents could search for matching symptoms; the
practitioner-source weighting; **resolve at primary source with `WebFetch` or mark UNRESOLVED**
(with the known `projects.blender.org` 403-to-`/api/v1/` trap named); source + date + direct URL +
one-sentence finding; **name the LEVERS** — the exact setting, the tool, what it changed; a
600-word cap; *specificity over breadth, 6–8 well-sourced findings beat 20 vague gestures*; and
that **everything returned is a hypothesis to verify locally, never a fact to adopt.**

## Verification plan (protocol Step 4), settled BEFORE the findings arrived

Settling this after seeing the findings would be choosing a standard to fit a result.

**Substrate measured on this rig at dispatch time**, not assumed:

- `roleos` — **NOT INSTALLED** (`command not found`). It is the protocol's locked *wrapper*.
- `prism` — **v1.6.0, installed and on PATH.** It is the *engine* the wrapper shells to, and it
  is what performs the deterministic retrieval-oracle existence check and the groundedness lens.
- `ollama` — `mistral-small:24b` and `granite4.1:30b` present: the two decorrelated non-Claude
  families of the protocol's own founding receipt.

**So the verification path is available and the protocol does not halt.** prism is invoked
directly rather than through the absent wrapper; the different-family, reasoning-stripped
requirement is met by construction because the synthesising advisor is `anthropic` and the lens
is `local`.

**One adaptation, and it is forced by the source mix rather than chosen for convenience.** The
protocol's own v1.2.0 lesson records that prism's oracle is **arXiv/Crossref-tuned**, so a dispatch
sourced from RFCs and vendor docs returns most citations `unparsed` — *"NOT fabrication; they're
retrieval-verified out-of-band."* A swarm the Director deliberately pointed at **forum threads and
issue trackers** will return `unparsed` for nearly everything. Therefore:

- academic citations (arXiv/DOI) → prism's oracle, as normal;
- practitioner citations (threads, issues, vendor docs) → **an out-of-band existence audit at this
  seat**: fetch each URL, confirm the page exists and that its content supports the stated
  finding. `unparsed` is **never** read as fabricated, and an unreachable URL is **never** read as
  fabricated either — it is marked CANNOT_CONFIRM and surfaced contrastively rather than kept as
  load-bearing.

## What happens next, and its one precondition

The Director's plan is **three Sonnet executor sessions running the three classes
simultaneously**, once the levers are known. Two constraints on that, both already measured and
neither negotiable:

- **W3 itself cannot be re-baked.** No `prep_uv.glb` / `mask.npy` / `pos.npy` / `meta.json`
  survives — verified three times. Any arm that needs a re-bake needs a *different* subject;
  `facet_E33`, `facet_E37/stageC` and `saltroad_bake_fix` carry complete prep state and are the
  candidates.
- **Three parallel seats collide on the count surfaces.** T34 pins stated counts against
  `pytest --collect-only` *of the tree the surfaces sit in*, so two seats adding tests cannot both
  be green independently — the record already has an instance. **The count surfaces are reserved
  to the advisor** and the dispatches will say so.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | five prompts dispatched in one message, each recorded here in substance; the agent count, word cap and sourcing standard are fixed by the protocol and stated before dispatch |
| ANDON_AUTHORITY | 2 | a citation that cannot be resolved at its primary source is marked UNRESOLVED by the agent and CANNOT_CONFIRM at synthesis, and is barred from the architectural connection rather than silently kept |
| NAMED_COMPENSATORS | 2 | the only irreversible act is spent tokens on five agents, bounded by the agent cap and word cap — the protocol's own named, owner-accepted non-undo. Nothing else here touches the world: no publish, no external write |
| DECOMPOSE_BY_SECRETS | 3 | the decomposition **is** the finding that opened this arc — three classes with three measured carriers, one agent each, plus two cross-cutting agents whose scope is deliberately orthogonal to the class split |
| UNCERTAINTY_GATED_HUMANS | 2 | the Director set the method and gets the levers before the experiments are specced; CANNOT_CONFIRM findings are surfaced contrastively rather than dropped silently |
| EXTERNAL_VERIFIER | 2 | prism v1.6.0 verified present on this rig **before** dispatch, different-family and reasoning-stripped by construction; the out-of-band audit for practitioner URLs is specified above, before any finding arrived. Rises to 3 when the receipt is captured below |

## Research grounding

*(appended when the agents return, one entry per finding, in the protocol's format:
`N. **<finding>.** <source> <date> (<URL>). <implication>.`)*

## Verification receipt

*(appended after Step 4 runs)*
