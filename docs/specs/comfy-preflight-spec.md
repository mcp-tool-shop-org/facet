# Spec 4 — comfy-preflight

**Charter.** Authored by the advisor (spec-author seat), 2026-08-08. **Nothing is built.**

---

## The job

**A gate that runs on a workflow graph in the seconds before it is submitted, and halts
a submission that will spend credits producing a known-wrong result.**

The differentiator is one measured fact, and it is why the product exists at all:

> **A Comfy Cloud `dry_run` PASS does not prove link sanity.** A hand-retyped payload
> with a self-referencing node link — `VAEDecode.samples = ["14", 0]`, the node pointing
> at itself — returned `status: validated`.

The provider's validator answers *is this graph well-formed enough to run*. It does not
answer *is this the graph you meant*. Every check below lives in that gap, and every one
was paid for by a run that got past `dry_run`.

## The checks

| # | check | halts on |
|---|---|---|
| 1 | **Link topology** | a node input referencing its own node; a link to a node id not in the graph; an input the class does not declare |
| 2 | **The inverted register scan** | see below — the load-bearing one |
| 3 | **Recipe-vs-profile agreement, by value** | any parameter reaching the graph that disagrees with the subject profile's declared value |
| 4 | **Graph-saved-is-graph-submitted** | the saved sidecar and the submitted payload differing **as parsed graphs** |
| 5 | **Generator-legal frame** | a width or height the model's VAE cannot decode at |
| 6 | **Estimate before submit** | a missing or unread credit estimate |
| 7 | **Anchor reproduction** | a recorded graph that no longer rebuilds from its recorded inputs — ⚠ **see the flag below; this one may be narrower than it reads** |

> ⚠ **CHECK 7 IS FLAGGED, 2026-08-09, and it is a flag rather than a finding.** The build seat
> raised it and correctly declined to investigate it out of scope: *"it needs the **builder**,
> and the corpus holds outputs, not the scripts that made them."* A graph that "rebuilds from
> its recorded inputs" presupposes something that can rebuild it, and 70 recorded graphs are 70
> **results**. This is the same shape as [E30 Ruling 5](../experiments/E30-ruling.md)'s law —
> *existence of the operands is not replayability; a replay needs a tool that can still be asked
> the recorded question* — arriving in a second repo within the week.
> **Enumerate before dispatching check 7**: find out whether a builder exists, and if it does
> not, the honest check is narrower than the table's wording and the table is what changes.

### Check 2 — the inverted scan, in both directions

The check that names the product's method. When a subject's register declares **no
style adapter**, the claim being asserted is *not* "the weight is 0.0". It is that **no
loader node and no card string exist anywhere in the graph** — asserted by walking every
node and every input, plus the link assertion that the downstream consumer reads directly
from the base model.

*A weight of 0.0 is not a weight of zero on a loaded card; it is no card.*

**And it asserts the mirror image**: a decided positive weight with no loader node is
**silently inert** — the run completes, costs money, and produces base-model output while
every log line says the adapter was requested. That halts too.

This is the shape the studio's own laws demand. *A detector that only reproduces what its
author already noticed is not an instrument* — asking "is the weight right" finds one
failure; asking "does the declared register match the graph's actual construction" finds
both directions. And *a gate must test the operation's failure mode, not its success
mode.*

The proof this is checkable: on one subject the two branches were compared **against each
other** rather than each described alone — the no-adapter graph is 16 nodes, loader nodes
NONE, card references NONE, and the **symmetric difference between the branches is exactly
one node**, the loader and its single link. That is a falsifiable statement about a graph,
and it is what check 2 produces.

### Check 3 — agreement by value, not by default

The parameter reaching the graph must come from **the subject's profile**, and the check
compares against the profile — not against the tool's `DEFAULTS`. This converts a
coincidence of value into agreement by construction.

**And the check carries its own exclusion with the reason in the code**: when a default no
longer reaches the graph at all, comparing it **fires on a correct build**. That is the
exact class of error this repo keeps paying for, and a preflight that halts correct work
gets disabled by the third person who hits it. *Put the andon on the direction the
invariant does not bound.*

### Check 4 — the recipe is the graph, and graphs compare as graphs

**The recipe for a generative step is the submitted workflow JSON** — graph, model names,
seed, sampler values, prompt, inputs. Not the script that built it: a script pins a local
*invocation* while the parameters that matter live in its source. A saved per-step
workflow JSON pins **more** than a loop script did, not less.

So: the exact JSON is **saved before submission**, and the check compares saved against
submitted **as parsed graphs** — node sets, class types, every input, every link —
**because a JSON re-dump can differ in whitespace without a value moving.** Comparing text
produces false halts; comparing parsed graphs produces true ones.

This is also the check with a free test suite: hand-driven runs already produced sidecar
JSONs whose purpose was explicitly to be *the future tool's regression fixtures*. Six
recorded graphs rebuilt identical, node for node, at a later session. **Those fixtures
exist; use them.**

### Check 5 — generator-legal frames

A Qwen VAE downsamples by 8. A width not divisible by 8 **decodes short** — 1066 arrives
as 1064 — putting every output 2 px off its control image and breaking every downstream
pairing. Two frames in the record passed by luck. **Derive the frame from the subject,
then round to the nearest legal width; ÷8 is the floor, prefer ÷16.**

The check is: does every dimension in this graph satisfy the model family's constraint?
It costs microseconds and it caught a defect that corrupted a whole pairing stage.

> ## ⚖ AMENDMENT 1 — check 5 is RE-SPECIFIED (advisor, 2026-08-09)
>
> **Raised by the build seat's §4** ([comfy-preflight-build-halt.md](comfy-preflight-build-halt.md)),
> which measured **zero `width`, `height`, `resolution` or `batch_size` inputs across all 70
> recorded graphs, and no `EmptyLatentImage` anywhere** — every one is img2img, frame inherited
> from the uploaded image. It offered three readings and correctly declined to choose among
> them. All three are partly right and none is the answer alone.
>
> **A is adopted as a rejection.** A check that finds no operand and returns PASS is *a check
> that cannot fail* — this repo's founding example is a silhouette IoU returning 1.00000 on a
> mesh with a hole through it. The naive form is **not adoptable**.
>
> **B is adopted.** `NOT_APPLICABLE` is a distinct third verdict beside PASS and HALT, and it
> **names what it could not see** — *frame-not-in-graph, inherited from `<input>`*. A refusal
> that states its own blind spot is this repo's standard shape.
>
> **C is adopted.** The check keeps full force wherever a dimension **is** declared. This corpus
> has none; other studio lanes generate txt2img graphs that do.
>
> ### ⚑ And the fourth thing, which decides the shape and which none of the three readings names
>
> **The defect check 5 exists for happened UPSTREAM OF THE GRAPH.** [E04 Ruling
> 15](../experiments/E04-ruling.md) records *"the 1066 was derived correctly from the mesh"* —
> `project_twins.py:263-266` computes `h_ext`/`v_ext` from the mesh bbox, and the twin was
> **rendered at that width and uploaded**. The graph never declared 1066; it received an image
> that was already 1066 wide. **So check 5 as this spec words it could not have caught the
> incident that motivates it** — the same family as gating on a proxy, asking about graph
> literals when the property is *the frame the run will actually produce*.
>
> **RULED: check 5's operand is the EFFECTIVE frame, not the declared one.**
>
> | case | operand | verdict |
> |---|---|---|
> | graph declares dimensions | the literals | PASS / HALT (C) |
> | img2img, caller has the input | **the input image's dimensions** | PASS / HALT — a real operand on **70 of 70**, and it would have caught 1066 |
> | neither available | — | `NOT_APPLICABLE`, naming what it could not see (B) |
>
> **The cost, named rather than discovered later:** the signature takes graph + register +
> *optionally* the input's dimensions. That is a parameter, not an architecture, and it fits the
> adoption contract already written below — **the production gate runs in-process on the submit
> path, where the image is in hand by construction**, and the standalone CLI degrades to
> `NOT_APPLICABLE`. That is the development/production split this spec already draws, arriving
> at check 5 on its own.
>
> ⚠ **Still not populated from memory:** the per-family constraint table. Qwen's ÷8 is measured
> here. **Ship Qwen alone and leave every other family declared-absent** — open question 2 is
> unchanged, and an unmeasured entry in that table is worse than a missing one.
>
> ### ⚖ AMENDMENT 1a — ÷8 HALTS, ÷16 ADVISES. The build seat's judgment call is RATIFIED.
>
> Built 2026-08-09, the seat found Amendment 1 did not say whether ÷16 halts, and ruled: **÷8
> is a floor and halts; ÷16 is a preference and advises.** 1064 is ÷8-legal and ÷16-short, so
> it PASSES with a note that says *this is not a halt*.
>
> **Ratified, and the record supports it more strongly than the seat argued.** It reasoned from
> the wording — *"a floor and a preference, not two floors"* — which is correct: the standing
> constraint reads *"÷8 is the Qwen VAE's floor, prefer ÷16."* The stronger ground is
> [E04 Ruling 15](../experiments/E04-ruling.md)'s own rejection of 1064, which rests on
> **three** clauses: *"/8 only, no precedent, and 2 px under the derived aspect."* Only the
> first is the ÷16 preference; **the other two are frame-SELECTION criteria that a preflight
> gate cannot evaluate** — it does not know what aspect was derived from a mesh it never sees,
> nor what precedent a subject carries. A gate that halted on ÷16 would refuse 1064, a width
> that ruling itself classifies as legal-but-not-preferred, and would fire on correct work —
> which is check 3's own exclusion clause arriving at check 5.
>
> **The six declared-absent families are ratified too**, with the reason restated because it is
> the load-bearing half: a test pins that `family="flux"` with `(1066, 1066)` returns
> `NOT_APPLICABLE` **and does not halt**, where Qwen would halt on exactly those numbers.
> Borrowing Qwen's divisor for an unmeasured family would be *inventing a measurement*, and the
> test makes that refusal falsifiable rather than merely stated.

## The home

**Standalone, and transport-independent.** Not a feature inside any one submission path.

**Re-examined under the placement rewrite (2026-08-08) and unchanged** — this is the one
tool of the four whose distribution argument survives intact, and the reason is the
in-process requirement below. The other three lost that argument: an MCP server does not
need to live in its caller's repo, so *mountability* answered them. It does not answer
this one, because a mounted gate beside the submitting process is a transport, not a guard.

The studio submits Comfy work through at least three doors: the official Comfy-Org MCP
plugin (third-party — we cannot add checks inside it), a bespoke cloud bridge script, and
hand-driven submission when a graph is being developed. **A gate that lives inside one
door is absent at the other two**, and the record shows the hand-driven door is exactly
where a retyped payload got past `dry_run`.

So: a small library plus an MCP tool plus a CLI verb, operating on a workflow JSON and a
profile. Any transport calls it. Its natural first callers are the studio's own bridge and
the sessions that hand-drive.

**The rule it enforces on itself:** *the check lives inside the tool that performs the
irreversible step* (E08 Amendment 32). A preflight in a shell chain before a submit is a
transport, not a guard — 47,020 texels were committed after a fired ANDON because a
PowerShell chain walked past a failing exit code. **The adoption contract is therefore
that a caller invokes preflight *in-process* on the submit path, and there is no skip
flag.** A standalone CLI exists for development, not as the production gate.

## What it does NOT do

- **It does not submit.** Nothing here spends a credit. It returns PASS or a structured
  halt; the caller submits.
- **It does not fix a graph.** No rewiring, no auto-inserting a missing loader, no
  rounding a frame for you. It names the defect and the node; a graph that a gate repaired
  is a graph nobody reviewed.
- **It does not judge the output.** It never sees one.
- **It does not evaluate prompts** — whether the terms are right is fixture-lint's job
  ([spec 3](fixture-lint-spec.md)) and the Director's eye.
- **It does not model VRAM or predict fit.** The local ceiling is a measured dead end:
  peak was 31.7–32.0 GB across three runs regardless of the reserve setting or the desktop
  baseline, because the runtime stages to fill whatever it sees free; freeing 6.5 GB made
  the working set grow 6.1 GB. **`--reserve-vram` and `--disable-smart-memory` are
  falsified as levers and the ceiling is never raised.** A preflight offering a fit
  prediction here would be selling a number the record already refuted.
- **It does not replace `dry_run`.** It runs *beside* it. `dry_run` catches what it
  catches; this catches what it demonstrably does not.

## Compensators

| action | irreversible? | compensator | post-rollback state | owner |
|---|---|---|---|---|
| running preflight | no | read-only on the graph and the profile | unchanged | — |
| writing the saved sidecar JSON (check 4) | no | delete it; it is derived from the graph in hand | regenerable | the caller |
| **submitting a graph** | **yes — credits spend, and this is the act being gated** | **cancel the job if it is still queued; otherwise none.** A completed cloud job is billed. The compensator is the gate itself, which is why it must be in-process | credits spent, output discarded | the submitting session |
| npm publish (a later session) | **yes** | `npm deprecate` the version; publish a fixed patch | bad version visible, marked | the publishing session |
| repo creation (a later session) | **yes** | `gh repo delete` same session, or archive | gone or archived | the Director |

**The third row is the whole product.** Submission is the irreversible act with no real
undo, and a preflight is a compensator you run *before* instead of after. That framing
belongs in the README.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | check 4 *is* this standard made mechanical — the submitted graph is the pin, saved before submission, compared as a parsed graph so a whitespace re-dump cannot be mistaken for a change. Check 3 pins parameters to a profile rather than to a tool default |
| ANDON_AUTHORITY | 3 | the whole product is an andon on the one irreversible act in the pipeline; no skip flag; in-process invocation is the adoption contract precisely because a shell chain is a transport, not a guard; check 3 carries an exclusion with its reason so the gate does not fire on correct work and get disabled |
| NAMED_COMPENSATORS | 3 | complete above, and honest about the one action whose compensator is *cancel if still queued, otherwise none* — which is the argument for the tool rather than a gap in it |
| DECOMPOSE_BY_SECRETS | 3 | graph-structural checks (1, 4, 5) know nothing about subjects; register and parameter checks (2, 3) resolve against a profile; the estimate check (6) is transport-side. Three groups changing at three rates, and the transport is deliberately outside all of them |
| UNCERTAINTY_GATED_HUMANS | 3 | it halts and names the node rather than repairing; a human decides. Check 2's mirror direction exists because the silent-inert case produces *no* signal a human could notice, which is exactly where a gate earns its place over a person looking |
| EXTERNAL_VERIFIER | 3 | it is an independent check on a provider's own validator, and it was born from a case where that validator returned `validated` on a self-linked graph. Check 7's anchor fixtures were authored by a different seat for a different purpose and rebuild identical — a regression suite the tool did not write for itself |

## The build bar and the named consumer (E14 Ruling 35)

**Landed mid-session, after this spec's first draft, and it governs.** The Director's
word, 2026-08-08: built and verified properly with tests — **the studio's shipcheck bar,
not a prototype bar** — before the polish arc opens.

**The consumer lands directly on check 2.** The polish arc re-makes the humanoid
**without the style adapter**, for a photo-real look. That is the inverted register scan's
exact case, on a real submission, spending real credits: the claim to assert is not "the
weight is 0.0" but that no loader node and no card string exist anywhere in the graph —
and the mirror direction matters just as much, because a silently inert adapter on any of
the other three exemplars produces base-model output while every log says otherwise.

The arc submits generations for four subjects across two register conditions. **A
preflight whose first production run is a deliberate no-adapter pass on a subject that
previously used one is about as good a first consumer as this tool could be given.**

## Open questions for the Director

1. **Language and package.** TypeScript matches the studio's MCP form and the official
   plugin's ecosystem; Python matches the existing bespoke bridge that would be its first
   caller. My recommendation: **TypeScript**, with the bridge calling the CLI — but if the
   bridge is the only near-term caller, Python is the cheaper honest answer.
2. **Which model families' frame rules ship on day one.** Check 5 needs a per-family
   constraint table. Qwen's ÷8 is measured here; others are not, and **I will not populate
   that table from memory** — each entry needs a measurement or a citation.
3. **Whether the studio's existing bridge adopts it as the gate, or keeps its own
   inline checks.** Adoption is the point; two preflights is worse than one.
