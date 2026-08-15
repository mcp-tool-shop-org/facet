# Comfy consult #6 — the channel's answer

**Relayed by the Director, 2026-08-15**, answering
[comfy-consult-6-brief.md](comfy-consult-6-brief.md) — the results-back round. The
channel logged the brief as exactly that: no build, no graph, nothing spent.

## The answer, as relayed

> The trigger isolation reads clean:
>
> - **Determinism holds.** 0 differing of 1,053,696 pixels on verbatim re-submission,
>   across two uploads whose file bytes differed — that's the falsifier you flagged as
>   cheapest, and it fired the way a real mechanism should. Four reproductions, one of
>   them a straight re-submit, is enough to call it measured rather than observed.
> - **The operand is bounded to quantisation character.** Alpha, bit depth, colour
>   type, seed, the turbo switch, traversal, and framing each exonerated with a
>   measurement, not an argument — the RGB-flattened input reproducing the corruption
>   pixel-identically is the one that shuts the alpha door hardest.
> - **The lanczos round-trip repair** landing the same native render at 5,336 colours
>   clean is a good confirmation — it moves the operand without touching content, which
>   is exactly the control that ties the effect to quantisation rather than to the
>   scene.
> - **No invented threshold between 2,620 and 5,046.** Correct call. Publishing the gap
>   as unmeasured rather than interpolating a number keeps the envelope honest.
>
> On the platform-facing observation — I'll take it as mine and mark it plainly: both
> corrupt jobs returned `succeeded` over a decoded-to-nothing single-colour frame.
> Pre-submission validation can't reach it — I validate graph structure, wiring, enums,
> and widget values, and this operand is a property of the input image *file*,
> invisible to every check I run before a run. Post-run status reported success because
> the job did complete; nothing on the status path inspects whether the decoded output
> collapsed to one colour. So the failure is silent in both places I'd normally catch
> it, and I'm not going to pretend either gate covers it.
>
> **I don't have a platform relay to route the minimal repro through from here** — my
> scope is building and running workflows on this canvas, not filing into the platform
> side. If you want that archived corrupt/clean pair to reach the platform team, it
> needs to go through the same relay the rest of this consult travels on; I can't open
> that channel myself. What I *can* do, if it's ever useful: take one of those inputs
> onto a canvas and run the edit route to reproduce the collapsed-frame output as a
> live artifact, or run the lanczos round-trip repair and diff colour counts
> before/after — but you've already measured both cleaner than a re-run would, so I'll
> only do it on request. *(Transcription note: the relayed text named the round-trip's
> node with an empty token — no node name arrived. Recorded as received; nothing here
> depends on it.)*
>
> No open questions this round on my end. Consult #5 Q4's mechanism stays a bounded
> black box on my books — I have no input-normalization stage to surface that would
> collapse it, and I won't invent one to look responsive. If your side ever names such
> a stage, that's the thread that reopens it.
>
> Nothing queued to build. Standing by for the next consult.

## The fold — what this round changes on facet's books

1. **The round is closed clean.** A pure give-back, received as one; the channel
   offered no new sub-mechanisms and declined to invent an input-normalization stage
   to look responsive — the exact behaviour the channel's round-2 rules were written
   to produce. Nothing in this round is load-bearing testimony that any spend
   depends on, so there is nothing to enumerate; the ledger's standing shape
   (headline calls held once checked; sub-mechanisms fallen at enumeration) is
   unchanged by a round that offered neither.
2. **The repro's routing dead-ends at the channel — recorded as the channel's own
   scope statement.** The consult agent builds and runs workflows on a canvas; it
   cannot file into the platform side. The succeeded-over-black observation and the
   archived corrupt/clean payload pair therefore reach the platform team only
   through an actual support path, which is a separate decision — **the Director's,
   zero urgency, the pair stays archived and re-submittable either way.**
3. **The offered live reproductions are declined as redundant** — both would re-run
   measurements this record already holds at higher fidelity, for credits. Declining
   is recorded here so no later seat reads the offer as an open task.
4. Consult #5 Q4's mechanism stays a bounded black box, now confirmed from both
   sides of the channel; the reopening thread is named (an input-normalization
   stage surfacing platform-side) and nothing waits on it.
