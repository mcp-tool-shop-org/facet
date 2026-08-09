# comfy-preflight — BUILD HALT at gate 1 (repo-first), with the pre-build measurements

**Written by the executor, 2026-08-09.** No code was written. No repo was created. Nothing
was submitted and no credit was spent. Nothing under `E:\AI\training` was modified.

> **⚑ HALT CLEARED the same day.** The Director created
> [mcp-tool-shop-org/comfy-preflight](https://github.com/mcp-tool-shop-org/comfy-preflight)
> and `E:\AI\comfy-preflight`; all five repo-first conditions were then met and the build
> proceeded. **This document is kept as written** — the pre-build measurements in §2–§7 are
> what the build was designed against, and §5 carries a correction earned during the build
> rather than a quiet edit. Build state lives in the new repo's README.

**Why this file exists:** the build halts at gate 1 and the halt is not the whole result.
Everything measurable without the repo was measured, and three findings change what gets
built. Recorded here rather than in a chat log so the seat that builds this does not
re-derive them.

---

## 1. THE HALT — gate 1, repo-first, UNMET

Both conditions checked at this seat:

| # | condition | state |
|---|---|---|
| 1 | `github.com/mcp-tool-shop-org/comfy-preflight` exists | **NO** — `gh repo view` returns `GraphQL: Could not resolve to a Repository` |
| 2 | `E:\AI\comfy-preflight` is a git repo | **NO** — the directory does not exist (`ls -d E:/AI/*preflight*` → no match) |
| 3 | `origin` points at that repo | not reachable — no repo |
| 4 | scaffold commit pushed and visible | not reachable — no repo |
| 5 | `git branch --show-current` is `main` | not reachable — no repo |

**Repo creation is the Director's act.** `gh repo create` was not run. The dispatch's own
words: *ask; do not run it.*

Nothing was scaffolded into an unpushed directory — the dispatch forbids it and
[repo-first.md](../../../.claude/rules/repo-first.md) makes it a hard gate.

## 2. The fixture resource, ENUMERATED before anything is commissioned

The dispatch names four fixture paths and a corpus total. All five claims hold:

| claim | state |
|---|---|
| `docs/experiments/E08-anchor-workflow-api.json` in git | **holds** — 3,161 B, committed at `de95fde` |
| `facet_E08\ARMB\out\stroke_{1..8}_*_workflow.json` — 8 graphs | **holds** — exactly 8 |
| `facet_next\E04_stroke\e10_layer\*_workflow.json` | **holds** — 4 |
| `facet_next\E04_g7\workflow_7_G7_headnoun.json` | **holds** — 3,165 B |
| 69 workflow JSONs under `E:\AI\training` | **holds — exactly 69**, plus the 1 in git = **70** |

All 70 parse as ComfyUI **API format** (`{node_id: {class_type, inputs}}`); 0 unreadable,
0 in the UI export format. Class-type census over the 69 (read-only walk):

```
138 LoadImage           69 UNETLoader      69 KSampler     45 ControlNetApplyAdvanced
138 CLIPTextEncode      69 CLIPLoader      69 VAEDecode    26 LoraLoaderModelOnly
 69 VAEEncode           69 VAELoader       69 SaveImage    24 ControlNetInpaintingAliMamaApply
 69 ModelSamplingAuraFlow  69 ControlNetLoader            24 ImageToMask / SetLatentNoiseMask
```

Split by node count and adapter presence — this is the fixture map for check 2:

| nodes | loader | count | example |
|---|---|---:|---|
| 14 | NONE | 39 | `workflow_headclay_0.json` |
| 15 | YES | 7 | `workflow_7_G7_headnoun.json` |
| 16 | NONE | 4 | `workflow_stroke1_y292.json` |
| 17 | YES | 20 | `stroke_1_y+090_e+00_workflow.json` |

## 3. FINDING 1 — the self-link fixture does not exist on disk, and cannot

The dispatch lists `workflow_7_G7_headnoun.json` as "the G7 case," which reads as *the
broken graph is here*. It is not. That file is the **corrected** graph: 15 nodes, node 14
`VAEDecode.samples = ['13', 0]` → KSampler. Correct.

[E04-g7-report.md:49](../experiments/E04-g7-report.md) says why, and the record is precise:

> my first `dry_run` payload was retyped by hand and contained `VAEDecode.samples = ["14", 0]`
> — a node linking to itself. Pre-flight returned `status: validated`. The submitted graph was
> read from the saved file and checked for self-links and dangling targets in code first;
> **the retyped one was discarded.**

**The corpus contains 0 self-links and 0 dangling links across all 70 graphs.** So check 1
has no naturally-occurring failing fixture anywhere, and gate 4 ("prove each of the 7 fires
on a deliberately broken fixture") must be met by **constructing** the break — mutating node
14's `samples` from `['13', 0]` to `['14', 0]`. That mutation reproduces the recorded
incident exactly, from the graph that was actually in the incident.

**Consequence for the build:** the can-fail fixtures are synthetic by necessity, and they
should be generated *from* the copied-in good fixtures by a documented mutation, not
hand-authored — so the PASS case and the FIRE case differ by exactly the one edit under test.
This also satisfies E28's fixture lesson (use synthetic names, keep the instrument's own
artifacts out of its evidence).

## 4. FINDING 2 — check 5 has NO OPERAND in this corpus, on 69 of 69 graphs

**Measured: zero `width`, `height`, `resolution`, `megapixels` or `batch_size` inputs exist
in any of the 69 graphs.** There is no `EmptyLatentImage` node in the entire corpus.

The class census above says why: every graph is `LoadImage → VAEEncode → KSampler →
VAEDecode → SaveImage`. It is an **img2img** topology throughout — the frame is inherited
from the uploaded image and is never declared in the graph. The 1066→1064 defect the check
exists for happened in the **frame-derivation code upstream of the graph**, not in a graph
literal.

**This is the gate-7 case and it needs the Director's or the advisor's ruling, not mine.**
Check 5 as the spec words it — *does every dimension in this graph satisfy the model
family's constraint* — is answerable only where the graph declares a dimension. On this
corpus it never does. Three readings, and they are not equivalent:

- **A check that finds nothing to check and returns PASS is a check that cannot fail** —
  the exact failure family CLAUDE.md names (silhouette IoU returning 1.00000 on a holed
  mesh). Not adoptable as written.
- **The honest form** reports `frame-not-in-graph, inherited from <input image name>` as a
  distinct third verdict beside PASS and HALT, and refuses to claim it checked a frame it
  never saw.
- **The check retains full force on txt2img graphs**, where `EmptyLatentImage` carries
  literal width/height. The corpus has none, but the studio's other lanes generate them.

I did not choose among these. Per gate 7, the honest subset ships and the missing one is
named; which of the three above is "the honest subset" is a specification decision.

## 5. FINDING 3 — the card-string scan needs a defined vocabulary, or it fires on everything

My first pass scanned for `.safetensors` anywhere in an input and reported **43 graphs** with
"a card string present but no loader node" — the spec's silently-inert direction. **That
figure is a false positive and it is mine.** The matcher hit base-model names:
`qwen_image_fp8_e4m3fn.safetensors`, `qwen_2.5_vl_7b_fp8_scaled.safetensors`,
`qwen_image_vae.safetensors`, `Qwen-Image-InstantX-ControlNet-Union.safetensors`.

Scoped properly, the **actual card surface in the corpus is exactly one input**:

```
26x  LoraLoaderModelOnly.lora_name = mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500.safetensors
```

> **⚠ CORRECTED 2026-08-09, during the build, by a test going red.** The line above says
> "exactly one input" — that part holds, `lora_name` is the only card-bearing input. But the
> **one card** reading is wrong: the corpus carries **two names for one adapter**.
>
> ```
> 26x  mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500.safetensors
>  1x  mikeyfrilot__saltroad-lora__saltroad_style_v2_lowlr_000001500.safetensors
> ```
>
> Same trained weights, different cloud-side namespace prefix from a re-import under another
> account. The figure above came from a walk of the **69** files under `E:\AI\training`; the
> second name is carried by the **70th** graph alone — `E08-anchor-workflow-api.json`, the
> in-git fixture, the first file this seat opened.
>
> **This is the enumerate-the-resource law at small scale, and the mechanism is worth the
> line: a scan that misses one file of seventy reports the wrong cardinality with total
> confidence, and nothing in the output looks partial.** It surfaced when check 2's
> whole-corpus leg halted on `ADAPTER_CARD_MISMATCH` — found by a gate firing, not by
> reading.
>
> Design consequence, already in the shipped check: exact-string comparison against one
> declared card halts a correct build, and the whole basename differs so basename comparison
> does not rescue it. The register takes declared `card_aliases`; equivalence is stated, never
> inferred, because prefix-stripping would also accept a genuinely wrong card whose name
> shared a tail.

**Consequence for the build:** the spec's phrase *"no loader node and no card string exist
anywhere in the graph"* is FALSE on all 43 no-adapter graphs under a naive reading, because
they all reference base-model `.safetensors`. The check needs an operational definition of
*card* — a loader class's card-bearing input, plus a profile-declared adapter vocabulary —
or it halts every correct build on day one, which is the thing check 3's own exclusion clause
warns about. This is a real spec-vs-fixture tension and it is the kind that gets a gate
disabled by the third person who hits it.

## 6. Check 2's mechanism holds on TWO independent pairs, not the one the spec cites

The spec cites one branch comparison. There are two, on different subjects, and both give
the same answer:

| pair | with card | no card | symmetric difference | consumer link |
|---|---|---|---|---|
| E08 ARMB ↔ E13 stroke *(the spec's pair)* | 17 nodes | 16 nodes | **exactly `{"5"}`** | `['5',0]`→loader vs `['1',0]`→UNETLoader |
| E04 G7 ↔ E12 twins *(second, independent)* | 15 nodes | 14 nodes | **exactly `{"5"}`** | `['5',0]`→loader vs `['1',0]`→UNETLoader |

In both, the only differing node is `5 LoraLoaderModelOnly` with
`{model: ['1',0], strength_model: 0.75, lora_name: <the one card>}`, and in both the
no-adapter branch has `ModelSamplingAuraFlow.model` reading **directly from `UNETLoader`**.
That is the spec's link assertion, reproducing on two subjects at two node counts.

[E12-handoff15-halt.md:130](../experiments/E12-handoff15-halt.md) recorded the first pair;
the second is measured here for the first time.

## 7. Open question 3 — ANSWERED WITH EVIDENCE: the bridge has no inline preflight to keep

The spec's third open question is whether the studio's bridge adopts this or keeps its own
inline checks, because *two preflights is worse than one*. Measured at
`E:\AI\sprite-foundry-packs\packages\pirate-raiders-3d\_cloud_sweep\comfy_cloud_bridge.py`
(1,082 lines, read-only):

**It has no link-topology check, no self-link check, no dangling-target check, and no
register scan.** Every `raise CloudError` in it is reactive to an HTTP response —
`node_errors on submit`, poll status, missing outputs. `node_errors` arrives **after** the
submission; the graph was already sent.

So adoption adds a gate that does not exist today rather than creating a second one. There
is no inline preflight to retire.

**And the bridge's CLI defaults are check 2's silently-inert direction, standing in
production:**

```
:1050  --lora-name      default="SaintEloi__pirate3d-lora__pirate3d_v2.safetensors"   <- a real card, always present
:1052  --lora-strength  default=0.0
:269   if lora_name and lora_strength and lora_strength > 0:   <- builds the loader node
```

The default invocation therefore names a real adapter card on the command line and builds
**no loader node**. The bridge's own guard is self-consistent — declining to build a loader
at strength 0.0 is correct — and this is **not a bug report against the bridge.** What is
absent is any assertion tying the *decided register* to the *constructed graph*: a caller
who intends the adapter and omits `--lora-strength` gets a completed run, spent credits, and
base-model output, while the command line and every log line name the card.

That is the case the spec describes as producing *no signal a human could notice*, found in
the named first adopter, before the tool exists.

## 8. What is NOT decided here, and is not mine to decide

- **Repo creation** — the Director's act (gate 1).
- **Language.** The dispatch rules **Python**, and its reasoning was checked: `bin/facet.js`
  is 27 lines and downloads a SHA256-pinned PyInstaller binary, with a stated precondition of
  *stdlib + sqlite3 + mcp* — which comfy-preflight meets (graph JSON + profile JSON, no numpy,
  no open3d). Nothing measured here contradicts the ruling. The Director may override it.
- **Check 5's honest form** — §4's three readings.
- **The card vocabulary** — §5. Where the adapter vocabulary comes from is a specification
  decision, and taking it from the graphs being checked would make the gate a tautology
  (CLAUDE.md: *derive a gate's reference from something other than what it gates*).

## 9. What the build session can start with immediately, once the repo exists

1. Copy the 70 graphs in as fixtures (~3 KB each, ~210 KB total) — **never read
   `E:\AI\training` at test time**; those trees are not in git and have no revert.
2. Generate can-fail fixtures by documented mutation of the copied good ones (§3).
3. Build check 2 first — it has two independent PASS pairs and a precise FIRE shape (§6).
4. Check 1 has 70 PASS fixtures and 0 natural FIRE fixtures; construct the FIRE (§3).
5. Checks 3, 4, 6, 7 need a profile fixture and a saved-sidecar pair; `tools/subject_profile.py`
   in facet is the shape of the profile side and was not read at this seat.
6. Check 5 is blocked on §4's ruling, not on code.

## Standards compliance (this halt)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every number here names its instrument and its scope; the inventory script is one read-only file and its output is quoted rather than summarized |
| ANDON_AUTHORITY | 3 | gate 1 fired and the session stopped at it — no directory scaffolded, no `gh repo create`, no code. §4 halts a check rather than shipping one that cannot fail |
| NAMED_COMPENSATORS | 3 | nothing irreversible was done. This file is the only write outside the scratchpad, and `git checkout` removes it |
| DECOMPOSE_BY_SECRETS | 2 | the findings separate graph-structural facts (§3–§6) from the adopter-specific one (§7); the card-vocabulary question (§5) is the seam that is not yet cut, and §8 says so rather than guessing |
| UNCERTAINTY_GATED_HUMANS | 3 | three decisions routed out rather than taken (§8), each with the reason it is not the executor's; §4 gives three readings and picks none |
| EXTERNAL_VERIFIER | 3 | every dispatch claim was checked against the filesystem and the record rather than accepted — and the one figure this seat produced itself (§5's 43) was overturned by its own follow-up measurement and is reported as an error rather than deleted |
