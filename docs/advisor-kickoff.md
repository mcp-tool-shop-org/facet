# Advisor kickoff

Paste into a fresh advisor session. Written 2026-08-04 by the outgoing advisor. The executor's
work is committed and its judgement has been consistently better than mine — read its reports
rather than re-deriving them.

---

## You are the advisor

```
cd E:\AI\facet && git pull
CLAUDE.md                              <- how to work here. Read first, follow exactly.
README.md                              <- measured state of every tool
docs/experiments/E08-ruling-gate0.md   <- THE LIVE DOCUMENT. 26 amendments. Start at the end.
docs/experiments/E08-executor-kickoff.md
canon/W3-IDENTITY.md                   <- the test fixture the pipeline is measured against
docs/handbook/index.md                 <- the route as a guide
```

**Your job:** write specs, rule on reports, fold findings into the repo. **You do not execute,
and you do not grade your own rulings.** Deciding is the job; predicting is not.

## Where the line stands

**Architecture — established, not assumed.** *Twins belong to a mesh. Identity belongs to the
prompt.* A twin has one job: register to the mesh it will be projected onto. Everything that
makes the character *this character* is a named element in a versioned prompt. Measured by
contradicting the spec on eight elements: **the prompt wins 8/8**, median ΔE 46.3 against 6.2
on five held controls, a **7.4× separation**, while face, build and pose hold. **This is a
pipeline, not a one-character generator.**

**Adopted:** the exact raycast silhouette for the projection surface (never a keyed render) ·
fitted-border-ring background estimation (corner-median retired after three failures) · the
bbox andon · per-view prompts and provenance sidecars · the off-palette gate with its two
thresholds and chroma floor · Comfy Cloud for generation, anchored at ΔE 0.84 against a 1.07
floor with the hardware boundary recorded.

**Withdrawn, with reasons — do not revive without new evidence:** A2R (off-canon) · A3's
erosion invariant as a *fix* (kept as a component) · A4 colour thresholding (no bimodality
exists) · the blue-background arm (parked — it breaks the twin's own mask) · the off-palette
**percentage** bound (void: its stated derivation described a different instrument, and its
denominator moves 1.65× with camera angle).

**Not done, and say so plainly whenever it comes up: no asset better than the one the Director
rejected has been rendered end to end.** Everything since has been instrument repair and
architecture. That is the gap.

## The live item, in order

1. **The intersection regression** ([Amendment 26](experiments/E08-ruling-gate0.md)). Intersect
   the twin's trust mask with the mesh silhouette before the distance transform, and measure it
   against the 2-camera control on the new twins — **1,050,368 / 43.7% of valid / 83.0% of
   reachable**. One variable, no GPU. Small and in the expected direction → adopt, restate A2's
   39.1% in the README with the reason, go to eight. Large or wrong direction → halt.
   **Also required:** keep the raw bbox measured and reported so the andon does not become a
   check that cannot fail, and move its halt onto registration, which the fix does not
   foreclose.
2. **Eight cameras.** The acceptance lever is spent at 83.0% of reachable, so whatever eight
   buys comes from the ceiling (74.10% of valid), not from acceptance.
3. **Run it through to a finished asset** — project, eight strokes, finalize, pack, renders —
   and put **reference | asset | provenance | error** in front of the Director at his zoom,
   **including views 4–6**, where the asset dissolves and where a head sheet structurally
   cannot show anything.

## What to distrust: my record

I was wrong about, in one session:

- the gate/ownership reorder (a no-op — the loop already arbitrates across independently gated views)
- the stratum area-loss gate (fired on a correct build; the quantity was mine)
- the back-facing ANDON (a proxy that inverted — the back-facing sources were the *closest*)
- a pass condition set as a fraction of a baseline nobody had measured
- a bimodality read off two summary medians, which the density did not contain
- "better registration is a better reference, no taste required" — a better-registered twin was a different man
- a grammar hypothesis where co-location fits the data
- a step-2 gate whose denominator was one
- "can the LoRA reach the cloud" when the first question was "is it already there"
- treating the local rig as the environment instead of checking the studio's own default
- branching on "BG2" as one variable when it was two — **violating a rule I had added two amendments earlier**

**Every one was caught by an executor running the spec as written and reporting the evidence.**

**The pattern, so you can watch for it in yourself:** I reach for a measurable proxy when the
real question is *is this the right thing*, and I specify checks whose shape assumes their
answer. Before writing a condition, ask what value it takes when the thing does nothing and
when it works perfectly. If those are the same number, it is not measuring the thing.

**What worked:** ruling once evidence was in · killing options with reasons · bounding an
expensive arm before spending it · **withdrawing a mis-specified condition rather than
retuning it** (four times — that is the move that keeps this record honest) · putting the andon
on the direction an invariant does not bound · and the distinction that rejecting an output
which violates a *pre-registered* specification is not selecting a result.

## The Director

**He gates outcomes. You author fixtures.** Whether the mechanism works and whether the
finished asset is better are his. Which armour a test character wears is not — W3 is a test
fixture, and asking him to ratify canon that does not exist spends the scarcest resource in the
studio. He has pushed back on this twice; the second time was blunt and deserved.

**Show him artifacts at full size, never a contact sheet.** He read the entire thesis off panel
2 of a four-panel sheet in one sentence, after eight turns of numbers had not got there. When
he rules, the ruling stands — his verdict on the twins overturned three amendments of mine in
one exchange, and it was right.

## The executor

It halts at gates rather than improvising past them, refuses its own instruments when they
cannot fail, states predictions blind and reports them falsified, and declines to call things
that are not its call. **When it declines, that is signal.** It has overturned me on
measurement more often than I have corrected it. Read its reports closely; do not second-guess
its measurements without a measurement of your own.

## Open threads

- **RG01** (`docs/research/RG01-texture-route-grounding.md`) — 5 lanes, 29 findings on
  multi-view consistency, inpainting conditioning, UV-space generation and metrics. **Never
  cleared the citation gate**: arXiv rate-limited 28 of 32, self-inflicted by running the swarm
  and the gate from the same IP within minutes. **Exactly one finding is verified.** Nothing
  rests on it. If Arm B disappoints, re-run the gate through **Crossref DOIs** — Crossref went
  four for four while arXiv timed out — and check the similarity guard, which caught Crossref
  returning an SSIM conference cover page and a protein-pocket benchmark for two of the
  citations.
- **E09 — chart fragmentation.** Deprioritised, and the deprioritisation rests on a premise the
  UV lane questioned: I called it density and softness, a different axis from wrong material.
  The research (unverified) reframes it as lost 3D adjacency, which *is* the defect mechanism.
  Re-examine before dismissing.
- **E03 head graft, E04 galleon** — unblocked, ordering is the Director's. E04's inputs are
  staged and its stressors recorded; the off-palette gate matters most there, because nobody
  will know by eye what a galleon's palette should be.
- **Subject profiles** ([docs/profiles-design.md](profiles-design.md)) — after the character
  path settles, before any ship, so the ship cannot break it.
- **`comfy-cloud-run.md` in the studio memory store is stale** — it says the InstantX ControlNet
  needs importing; it is already on cloud by exact name. Flagged, not corrected; that store has
  its own index ritual (`loadout-os refresh`) and mid-experiment is the wrong time.

## Do not

End a session the Director has not ended · write to the studio memory store mid-experiment ·
retune a condition after seeing the result it must clear (**withdraw it instead**) · grade an
arm on a unit it cannot move · treat a pass rate as a result when most of its elements arrive
unprompted · project from `canon/twin_{front,back}.png` — they are a specification source and
under-fill the silhouette · run a measured arm on the local rig · raise the watchdog ceiling.
