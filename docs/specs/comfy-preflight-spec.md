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
   *(Resolved by the build, 2026-08-09: the seat shipped **Python** — console-script
   packaging, suite green in three interpreter modes. OQ1 is closed by reality.)*
2. **Which model families' frame rules ship on day one.** Check 5 needs a per-family
   constraint table. Qwen's ÷8 is measured here; others are not, and **I will not populate
   that table from memory** — each entry needs a measurement or a citation.
3. **Whether the studio's existing bridge adopts it as the gate, or keeps its own
   inline checks.** Adoption is the point; two preflights is worse than one.

---

> ## ⚖ AMENDMENT 2 — the aggregator arc is DISPATCHED, and check 8 joins the table (advisor, 2026-08-14)
>
> **At the Director's word**: the executor launches on the ratified next arc — **the
> `preflight()` aggregator, the CLI verb and the MCP surface** — and the speck arc's
> preflight-shaped lesson folds in as a new check. Checks 3/6/7 remain OUT for the
> standing reasons (no profile fixture; transport-side; needs the builder enumerated).
>
> ### The arc, ratified
>
> 1. **The aggregator** — `preflight(graph, register_profile, input_dims=None)` composing
>    checks 1/2/4/5 (+8 below) into one structured result: per-check findings, verdict
>    merge **HALT > ADVISORY > NOT_APPLICABLE > PASS**, every finding naming its node and
>    its evidence. The composition surface is a check registry, not a hardcoded list —
>    check 8 lands **through** that registry as the proof it extends.
> 2. **The CLI verb** — the development door; follows the repo's own established exit-code
>    and refusal conventions (the executor enumerates them from the built tree, not from
>    this spec).
> 3. **The MCP surface** — stdio, the studio's server form; the tool returns the
>    aggregator's structured result verbatim. The MCP is a *transport* over the same
>    in-process function — the adoption contract is unchanged: **the production gate is
>    the in-process call on the submit path, no skip flag.**
>
> ### Check 8 — the declared-envelope advisory
>
> **Provenance, measured (E33→E35):** the performer's twins were generated at img2img
> denoise **0.92** through a control checkpoint whose own model card documents an
> operating band of **~0.10–0.50** — 2–9× outside it — and nothing on the submit path
> said so. *(⚑ CORRECTED 2026-08-14, Amendment 3: the card documents NO denoise band —
> the cited figure was a research-agent claim falsified at its own source by this
> amendment's verified-live discipline, at the build seat. The provenance's true form:
> the twins were generated at a denoise the vendor gives no guidance on, and nothing
> said even that. Check 8's declared-absence output now says exactly that, on the
> submit path.)* The dark-speck class that followed cost an acceptance, a consult, a five-agent
> research swarm and a repair arc
> ([grounding](../research/E35-speck-research-grounding.md), agent 1 finding 8; facet
> known-defects, final entry). The fact was knowable at submit time. This check puts it
> there.
>
> **The check:** for each model/checkpoint the graph loads, compare the graph's parameter
> values (denoise, conditioning strength, cfg, steps — whatever the entry declares)
> against a **cited envelope table**. Out-of-band → **ADVISORY, never HALT**, the finding
> quoting the value, the band, and the citation. No entry for the checkpoint →
> **NOT_APPLICABLE, naming the checkpoint it could not see** (the Amendment-1 B-shape).
>
> **Why advisory is a ruling, not a softness:** the studio ran 0.92 *deliberately* and
> the Director approved the register produced at it. A documented band is documentation,
> not a gate; a check that halts correct work gets disabled by the third person who hits
> it — check 3's exclusion law arriving at check 8. The advisory's job is to make the
> out-of-band fact **visible at the moment it is cheap**, not to forbid it.
>
> **The data discipline (Amendment 1's, verbatim in force):** the envelope table ships
> with **no entry populated from memory**. Every entry carries its parameter, band,
> source URL and retrieval date, **verified against the live card at build time**. Day
> one ships exactly one checkpoint — `Qwen-Image-InstantX-ControlNet-Union`, img2img
> denoise ~0.10–0.50 per its card — plus any further parameter that card documents,
> verified at the seat, and nothing else. *(⚑ Amendment 3: the card carries no such
> band; what shipped is the band it DOES document —
> `controlnet_conditioning_scale ∈ [0.8, 1.0]` — plus a declared absence for denoise
> that reports the value it cannot judge. RATIFIED.)* ⚠ The E35 grounding also cites a **FLUX**
> Union card (canny examples at 0.5); that is a **different checkpoint** and its numbers
> do not enter a Qwen entry. A test pins that an uncited entry fails; a second pins that
> an absent checkpoint returns NOT_APPLICABLE and does not halt.
>
> **Decompose-by-secrets placement:** check 8 joins the register/parameter group (2, 3)
> — it resolves against declared knowledge, not graph structure — and the envelope table
> is data beside the code, changing at documentation cadence, like check 5's family
> table.
>
> ### What stays out of this fold, with the reason
>
> The despeckler (`twin_despeckle`) and the seed-fusion stage (`twin_fuse`) are **facet
> route tools** — they operate on generated images after the act this gate guards. A
> preflight that touched pixels would be a different product. The fold is the envelope
> fact alone, because that is the part that belongs *before* the spend.

---

> ## ⚖ AMENDMENT 3 — the aggregator arc is RULED AND ACCEPTED; check 8's fired gate is disposed; the citation defect is the advisor's (advisor, 2026-08-14)
>
> **On the build report** (`comfy-preflight docs/build-report-aggregator-and-check-8.md`,
> code at `d8b2bf4`, report at `11b1487`). Verified at this seat before ruling: CI
> `31830549226` resolved — success at `d8b2bf4`, 228 passed **zero skipped** on 3.11 and
> 3.12 in three interpreter modes; the tree pulled and current; and the arc's central
> claim re-verified by a **third independent fetch** of the cited card at this seat,
> agreeing with the build seat's two: `controlnet_conditioning_scale ∈ [0.8, 1.0]`
> explicit for all four control types, `true_cfg_scale=4.0` and `steps=30` as snippet
> examples, **no img2img denoise or strength band anywhere**.
>
> ### The arc is ACCEPTED as built
>
> The aggregator's one-entry-point law (a non-raising twin is a skip flag renamed —
> enforced by parsing the module, which is the right instrument for the absence of a
> function) · the one-raise-carrying-everything composition with per-adapter catches of
> `PreflightHalt` and only `PreflightHalt` · the registry as the extension proof (check 8
> landed through it with no edit to `preflight()`) · PASS-with-declined-clauses printed
> on a passing run (a clause nobody asked is not a clause that passed) · the exit-code
> contract, including its load-bearing pair: **ADVISORY exits 0** so a shell chain cannot
> reinstate the halt this spec removed, and **exit 2 is not exit 1** because nothing
> examined supports no claim · the MCP surface as a byte-identical transport verified as
> a real subprocess · and the four run-found defects, each the
> install-and-run-before-writing discipline paying out. All ratified.
>
> ### The fired gate, disposed: readings A and B are ADOPTED, C is EXECUTED
>
> **A — adopted.** Check 8 as built is CORRECT. A declared absence naming the value it
> cannot judge, with source and retrieval date, is real information on the submit path —
> and inventing a band to judge against would have been the exact defect this table's
> discipline exists to refuse. The check not flagging the 0.92 that motivated it is the
> honest outcome of the world as measured: **the vendor gives no guidance, and now the
> caller is told so at the moment it is cheap.**
>
> **B — adopted as a capability, gated as data.** The envelope table MAY carry
> **studio-measured** entries beside vendor-cited ones — the spec's own discipline
> already says *"each entry needs a measurement or a citation"*, and a measurement with
> a facet-record locator satisfies it. The build-out arc adds the entry KIND (schema +
> tests: a measured entry carries its record citation the way a vendor entry carries its
> URL); **no measured entry ships until the advisor rules one in** — the first candidate
> is E35's denoise sweep once ruled, which would convert facet's own record into the
> documentation the vendor never wrote.
>
> **C — executed, in facet, this fold.** The grounding's finding 8 is corrected at all
> seven sites (the grounding's three, the E35 spec, the status row, this amendment's
> two), each in place beside the original with the three-fetch measurement, and relayed
> to the live E35 seat. **The defect is the advisor's**: a research agent's citation
> became load-bearing across five record surfaces and a dispatch rationale without being
> resolved live — while the same seat WAS resolving the consult's checkable claim and CI
> run ids. The law this folds to: **a citation that becomes load-bearing — entering a
> spec, a defect entry, a data table, or a dispatch rationale — is resolved against its
> live source at fold time**; a research agent's report is testimony, not a resolved
> source. Amendment 2's cited-entries-only discipline is what caught it, one seat late —
> the system working, and the lesson is to run it one seat earlier.
>
> ### Check 5's ÷16 note is PROMOTED to ADVISORY
>
> The build seat flagged the shape mismatch and correctly declined to re-specify a
> ratified check. Ruled now: Amendment 1a's *"PASSES with a note"* predates the verdict
> vocabulary; with `ADVISORY` in the merge order, the ÷16 note IS an advisory and
> carrying it as one is a re-labeling, not a re-specification — ÷8 still halts, ÷16
> still never does, the aggregate verdict for a ÷16-short frame moves PASS → ADVISORY.
> Lands in the build-out arc with tests.
>
> ### And the sibling fact the verification surfaced, recorded so it is not re-derived
>
> The card's explicit `[0.8, 1.0]` cn recommendation means the studio's recorded 0.9 is
> **inside** the vendor band — E35's arm 2c (0.65) is a deliberately below-recommendation
> arm and is framed as such in the corrected E35 spec. `true_cfg_scale=4.0` and
> `steps=30` remain notes, not bands, exactly as the build seat shipped them.

---

> ## ⚖ AMENDMENT 4 — the treatment arc is RULED AND ACCEPTED; the tag outran the sweep; what published, measured (advisor, 2026-08-14)
>
> **On the treatment report** (`comfy-preflight docs/treatment-report.md` at `9f3add0`).
> Verified at this seat before ruling: CI green at the release commit `d888baf`;
> `gh secret list` **empty** (the no-token claim holds); the four version sites agree at
> 1.0.0; logo, landing page and handbook all live at 200; `SHIP_GATE.md` carries the
> hand-corrected tags with the detector's blind spot stated at the top; CHANGELOG's
> `[1.0.0]` entry proper. The arc is **ACCEPTED as built**: the drawn-not-generated mark
> with its constants read off the reference by PIL; the favicon re-drawn after rendering
> at true size caught the hamburger; `verify.py` as the single pinned gate; the pip-audit
> declared-surface fix; §5's defects-found-by-running-things, §5d stated against the
> seat's own instrument discipline; and §9's honest EXTERNAL_VERIFIER markdown. The
> report's §6 also **predicted the exact failure the release then produced** — npm
> masking a trusted-publisher gap as a 404 — which is what a threat model written from
> mechanism looks like.
>
> ### The handback events, measured — the tag outran the sweep
>
> Halt committed 15:57. The Director's web edit 16:00; the executor's header repairs
> 16:07 and 16:10; the outgoing advisor seat closed 16:11. `translate-all.mjs` ran
> ~16:12–16:17 on this rig (TranslateGemma 27B resident; **which hand invoked it is not
> established from any artifact** — the invocation lives in no tree). The release commit
> `d888baf` (16:22) then carried the seven translations **unswept**, tag `v1.0.0` fired
> the workflow, and the sweep this spec's release order assigns to the advisor ran only
> AFTER the tag — at this seat, finding one real defect: **Hindi rendered `÷8 halts.
> ÷16 advises.` as "stop eight times, advise sixteen times"** — an imperative at the
> reader, meaning inverted, the `÷` tokens gone, on check 5's own subject matter. Caught
> by digit-run parity. Also found and repaired: all seven translations lacked the
> PyPI/npm badge pair (generation ran against the badge-less source; the release commit
> re-added the pair per the report's own §5d plan). Dispositions that stand without
> repair: ja's +2/+3 digit surplus is number-word→digit convention; working-copy CRLF is
> `autocrlf` checkout behaviour — the committed blobs measure 0 CRLF, all seven. Repairs
> landed as `0604335` on `main`.
>
> ### What published, and what it contains — measured, not read off config
>
> Run 1 (tag at `d888baf`) failed at the linux binary: PyInstaller's
> `--collect-submodules mcp` imports `mcp.cli`, which `sys.exit(1)`s when typer is
> absent. The executor's root-cause fix (`mcp.server`, with the collection-vs-exclusion
> mechanism in the comment) is exemplary. Run 2 (tag moved to `2c072fa`): both binaries
> built, the GitHub Release cut with assets, **PyPI `comfy-preflight` 1.0.0 LIVE with
> provenance** — then **npm FAILED, E404 on PUT**: the trusted-publisher binding for
> `@mcptoolshop/comfy-preflight` does not exist npm-side. Two facts this seat then
> measured rather than inferred:
>
> 1. **npm packs README variants regardless of the `files` field.** The failed run's own
>    pack listing shows all seven translated READMEs in the tarball against
>    `files: ['bin/', 'README.md', 'LICENSE']`. This seat's first analysis read the
>    config and called the npm artifact translation-free — **falsified within minutes by
>    the tool's own log. That error is this seat's, owned here.** Consequence: the npm
>    artifact is translation-bearing, so it must publish from a tree at or after
>    `0604335`.
> 2. **The PyPI sdist is clean** — downloaded and listed: `README.md` only, no
>    translations; the wheel carries only the package. The live 1.0.0 is unaffected by
>    the Hindi defect. The GitHub Release's binaries and dists are likewise clean; the
>    unswept translations exist only in the `v1.0.0` tag's browse-tree.
>
> One harmless residue, recorded so nobody re-derives alarm: run 2 published a sigstore
> provenance statement (logIndex 2468827143) for the npm tarball that never landed — an
> orphan transparency-log entry, append-only by design.
>
> ### The process finding, and the law it folds to
>
> Nothing on disk distinguishes *translations generated* from *translations swept*. The
> handback word lived in conversation; seven finished-looking files sat in the tree; the
> release commit scooped them and the tag outran the gate. The defect the sweep exists
> to catch was real and present — the system's one miss was ordering, not instruments.
> **The law: translations enter the tree in the ADVISOR's commit, never riding an
> executor's release commit. The sweep's PASS is that commit** — sequencing enforced by
> who commits what, not by memory. This is the same shape as *the check lives inside the
> tool that performs the irreversible step*: the advisor's commit IS the sweep receipt,
> and a release commit that contains no translations cannot ship them unswept.
>
> ### Completion — the one account action, and the fork
>
> Blocking everything: **the Director configures npm's trusted publisher** for
> `@mcptoolshop/comfy-preflight` → repository `mcp-tool-shop-org/comfy-preflight`,
> workflow `release.yml`, environment none — the same binding shape PyPI carries.
> Then the fork:
>
> - **Recommended: v1.0.1 forward.** Bump the four version sites + the launcher's
>   pinned tag, CHANGELOG entry naming the swept translations and the workflow fix, one
>   commit, tag at or after `0604335`, full run. No deletions, no compensators; npm
>   debuts clean at 1.0.1; PyPI keeps a clean 1.0.0 beneath it; the v1.0.0 GitHub
>   Release stands with working binaries.
> - Rejected on content: **re-running the failed job** — it re-packs `2c072fa`'s
>   unswept tree. Rejected on cost: **re-cutting v1.0.0** — three compensator actions
>   on public surfaces (release delete, tag delete, re-tag) to buy version symmetry
>   that a patch buys forward.
>
> ### Open items, routed
>
> §5c (pagefind path stale in the handbook playbook) → the playbook's canonical store
> copy, next consolidation pass. §5e (shipcheck detects `[all] [pypi]` only, blind to
> the npm launcher, console script and MCP server) → an issue on shipcheck's repo when
> its next arc opens. The first `STUDIO_MEASURED` envelope entry → **waits on E35's
> close**, exactly as Amendment 3B ruled; nothing ships into that dict from this arc.
>
> ### ⚑ POSTSCRIPT — the completion, measured (advisor, 2026-08-14, later)
>
> The Director bound npm's trusted publisher and the executor completed **v1.0.0 at its
> own tag** — a `workflow_dispatch` lane taking a tag input, both jobs checking out that
> tag, `skip-existing` on the PyPI step and `--clobber` uploads making a half-published
> release finishable (`362b650`, plus `fb98eb6`) — instead of this amendment's
> recommended v1.0.1. **The deviation is RATIFIED on the measured outcome**: npm 1.0.0
> live under OIDC (`_npmUser: GitHub Actions`, `trustedPublisher` block), and the
> published tarball — downloaded and read at this seat — carries the **repaired** Hindi
> ÷8/÷16 line. The mechanism deserves its plain name: the executor's release-fix commit
> `2c072fa` had scooped this seat's two-minute-old working-tree repair
> (`README.hi.md | 2 ±`) into the tag, so the same shared-copy scoop that nearly shipped
> the corruption at `d888baf` is what shipped the fix at `2c072fa`. **Luck in both
> directions, and this amendment's law — translations enter in the advisor's commit —
> is what replaces it.** Residual, cosmetic: the seven tarball translations lack the
> badge pair (`0604335` is main-only); it heals at the next ordinary release. The
> dispatch lane is ratified with its guard named: a tag-input dispatch can republish an
> old tree by design; the version gate bounds it to tags matching the declared version.
>
> Registry state: `[0.0.0, 1.0.0]` — a placeholder ALSO ran alongside the TP-first
> path; harmless, unnecessary, recorded in the placeholder playbook with the hygiene
> close (**recommend `npm deprecate @mcptoolshop/comfy-preflight@0.0.0`, the Director's
> hand**). The **2FA-and-disallow-tokens flip is now armed**: its condition — a
> successful CI OIDC publish — is met and verified from registry metadata, his hand
> likewise. The executor's two "still open" items were already disposed when its report
> was written: the denoise-band correction executed at seven sites (Amendment 3C), and
> `STUDIO_MEASURED` waits on E35's close (3B, reaffirmed above). shipcheck 27/27 exit 0
> accepted as reported, CI green at `362b650`. **The treatment arc is CLOSED.**
