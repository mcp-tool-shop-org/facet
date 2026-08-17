# Grok build #19 — the prompt studio, and the density problem the router just exposed

**2026-08-17, facet advisor seat.** Eighteen briefs, eighteen chips held. #18 landed the
canon router; its chip was verified by running it before this brief was written.

This round carries a **research grounding** section: five parallel research agents, ~45
retrieved findings, synthesized here with identifiers so every architectural choice below
traces to evidence rather than to an advisor's taste. Findings are cited as `F<n>` in the
architecture section. Citations are gated before they connect to architecture; anything the
gate could not confirm is marked and is **not** load-bearing.

*Everything below the line is the paste block.*

---

# Eighteen for eighteen. The router works — and the literature says the thing it enforces may be physically too dense to render.

## What #18 established, verified by running it

`canon_gate` is a router: resolve, cover both directions, scope, schema 1+2, and a gate in
front of the cloud spend path. The chip reproduced exactly — a covering W3 prompt returns
`missing: 0, ok: True`; the same string with `gold necklace` appended returns
`missing: 0, unlicensed: [{'span': 'gold necklace'}], ok: False`. The forward direction is
fully satisfied and the reverse fires alone, which is the only case that discriminates.

Counts reconciled by the advisor, as reserved: **1283 / 1229 / 54**. Your change-set's
assumption was right to the test.

## Research grounding — the empirical floor for this round

Retrieved, not recalled. Where a source could not be confirmed it is named as unconfirmed
and is not used.

### ⚑ Verification status — read this before trusting any F-number

Every citation below was run through an external citation gate: a deterministic arXiv/Crossref
retrieval oracle plus a different-model-family groundedness lens, with this seat's reasoning
stripped. **The gate fired twice.** First `verifier_unreachable` (0 checked — reported as a
fired gate, repaired by configuring signing, which adds capability rather than removing
coverage). Then, on the real run: **27 citations checked, verdict `revise` — 5 supported,
17 not-addressed-in-abstract, 3 contradicted, 2 oracle-unreachable.**

What those verdicts mean here, stated honestly rather than smoothed:

- **`contradicted` → WITHDRAWN.** F15 and F16 are struck below and are **not** load-bearing.
  One of them was the sole evidence for a prohibition in the *foreclosed* list; that entry is
  struck too.
- **`not_addressed` is NOT fabrication.** The oracle reads title + abstract only, so a figure
  that lives in a results table reads as unaddressed. This is the documented behaviour of this
  runner, not a defect in the finding — but it does mean **17 of these are existence-verified
  and groundedness-unverified**, and a claim you intend to build on should be read at source.
- **`2 unreachable`** — arXiv returned an HTTP error for arXiv:2403.11821 and arXiv:2605.27463.
  Unreachable is never read as "fine" and never as "fabricated."
- **6 findings cite multiple sources and only the first was checked** (F14, F19, F20, F21, F22,
  F37). That is a formatting defect of mine — one finding, one source is the rule and I broke
  it — so their second and third citations are unverified.

Receipt: `docs/grok-consult-19-brief.citation-receipt.json`.

### The prompt is a budget, and the budget is measured in ELEMENTS, not tokens

**F1. Each additional prompt component costs ~8.53% of mean Components-Inclusion-Score, with
image quality falling alongside it (Inception Score −15.91%, FID +9.62%).** Foong, Kotyan,
Mao & Vargas 2023 (arXiv:2311.13620). Their tested range tops out well below our 17–24
element prompts; **nothing retrieved measures a ceiling anywhere near that density.**

**F2. Binding ONE attribute to ONE object already fails close to half the time.**
T2I-CompBench++ single-object colour binding tops out at 0.5879 for SDXL (SD v2 0.5065, SD
v1.4 0.3765). Huang, Sun, Xie, Li & Liu 2023 (arXiv:2307.06350).

**F3. At TWO objects, the strongest model still fails most of the time.** GenEval's
two-object colour-attribution task: DALL-E 3 scores 0.45, SDXL 0.23, SD 2.1 0.17. Ghosh,
Hajishirzi & Schmidt 2023 (arXiv:2310.11513).

**F4. Prompt-component ORDER has no statistically significant effect on which components
appear.** Components-Inclusion-Score 0.664 original vs 0.678 shuffled; χ²(996, N=175,918) =
1006.76, **p = .399**, for up to 8 components. Foong et al. 2023 (arXiv:2311.13620).
⚠ This contradicts the studio's own inherited belief that front-loading is "influence
optimization." That belief is now **suspended** in our knowledge store, not replaced.

**F5. A separate 2025 result DOES measure positional bias — but in retrieval, not
generation.** Moving a matching segment from position 0 to position 2 dropped Long-CLIP's
Urban-1K accuracy 0.582 → 0.485. Wu & Albreiki 2025 (arXiv:2511.11216). **F4 and F5 are not
in conflict; they answer different questions**, and conflating them is how a studio ships a
front-loading feature that does nothing.

### The encoder's declared limit is not its useful limit

**F6. CLIP ViT-L/14 is hard-fixed at 77 tokens (75 content + BOS/EOS) and overflow is
TAIL-truncated.** OpenAI, `clip/clip.py` (https://github.com/openai/CLIP/blob/main/clip/clip.py)
— `truncate=True` slices `tokens[:context_length]` and force-writes EOT as the final element;
`truncate=False` raises. Primary source is code, not a paper.

**F7. CLIP's EFFECTIVE reading length is ~20 tokens.** On long-caption retrieval, R@1 growth
flattens past 20 tokens — "the true effective length of CLIP is no more than 20." Zhang,
Zhang, Dong, Zang & Wang 2024 (arXiv:2403.15378).

**F8. Our own stack's encoder is not CLIP, so F7 may not transfer.** Qwen-Image's text
encoder is Qwen2.5-VL-7B-Instruct; Diffusers' documented pipeline default is
`max_sequence_length=512` while `encode_prompt`'s own default is 1024
(https://huggingface.co/docs/diffusers/main/api/pipelines/qwenimage). **The effective length
for OUR encoder is unmeasured by anyone.**

**F9. No primary source exists for a CLIP-BPE characters-per-token ratio.** The familiar ~4
chars/token is OpenAI's guidance for its **GPT-family** tokenizers, a different vocabulary.
**The studio must tokenize, never estimate.**

**F10. A live padding defect in the Qwen-Image Diffusers path** — embeddings pad to the
batch's shortest prompt rather than the declared max (huggingface/diffusers#12075). We
generate on Comfy Cloud rather than local Diffusers, so **whether this touches us is an open
question, not a finding.**

### The mechanism nearest our co-location result — and the honest gap

**F11. Attention-map OVERLAP is the isolated cause of an entity vanishing COMPLETELY rather
than rendering weakly.** Tested against two rival causes (low attention intensity, diffuse
spread). Marioriyad, Banayeeanzade, Abbasi, Rohban & Baghshah 2024 (arXiv:2410.20972). **When
two nouns compete for one region, the loser can be a hard zero, not a fade** — which is the
shape of our ΔE 1.07 no-response.

**F12. The field's standard taxonomy separates "catastrophic neglect" (a subject is dropped
entirely) from "incorrect attribute binding" (an attribute attaches to the wrong subject).**
Chefer, Alaluf, Vinker, Wolf & Cohen-Or 2023 (arXiv:2301.13826). **Our co-location result is
neglect of the added element, not blending** — which is the correct name for it and we did
not have one.

**F13. ⚑ Co-location is NOT a named phenomenon in the retrievable literature.** A dedicated
search for a complete, near-zero perturbation when a new element is requested for a region
already filled by a named incumbent — across two grammatical forms, same null result — found
nothing. The nearest mechanisms (F11, and cross-attention dilution) describe competition
between two **prompt-native** entities, not one entity's request being absorbed by an
**already-established incumbent**. This is a clean gap: our result is a candidate for
something the field has not isolated, not a failure to find it.

### The model that drives it: size is not the lever

**F14. Production systems disclose the rewrite rather than performing it silently.** DALL-E
3's API runs a rewrite over every prompt and returns it as `revised_prompt`. Betker et al.,
OpenAI 2023 (https://cdn.openai.com/papers/dall-e-3.pdf). **The closest existing precedent
for "propose, never silently admit."**

**F15. ⛔ WITHDRAWN FROM LOAD-BEARING USE — the citation gate contradicted it.** The research
agent reported Llama-3 rewriters at 3B / 8B / 70B scoring win rates of 0.499 / 0.506 / 0.510
("weak scaling") from arXiv:2510.12041. The gate returned **contradicted**, and the abstract,
fetched directly, does **not** contain those numbers — its stated conclusion runs the other
way: *"prompt rewriting is an effective, scalable, and practical model-agnostic strategy."*
The numbers may well sit in a table in the body, **but nobody here has read the body**, so
this does not connect to architecture. *You probably expected a "size doesn't matter" finding
here; I pulled it because the oracle contradicted it at the abstract. Override it by reading
the paper's scaling table.*

**F16. ⛔ WITHDRAWN FROM LOAD-BEARING USE — same source, same verdict.** The reported
aesthetics-reward trade (aesthetics 0.476 → 0.818 while alignment fell 0.561 → 0.424) is
**unconfirmed** for the same reason. This is the one that stings: it was the whole evidence
for forbidding an aesthetics-tuned rewriter, and **a prohibition resting on an unverified
number is worse than no prohibition**, because it looks grounded. The concern is still
*plausible* — it is the classic reward-shaping failure — but it is now a hypothesis, not a
finding, and the brief treats it as one.

**F17. Task-tuning, not scale, is what moves adherence — and it is not uniform.** A 7B CoT
rewriter, RL-trained against an alignment reward, lifts prompt-following +5.1% average and up
to +17.3% on relational reasoning — but improves only **20 of 24** categories. PromptEnhancer
/ Hunyuan 2025 (arXiv:2509.04545).

**F18. The vendor closest to this exact task picked the small end of its own range.**
Qwen-Image-2.0's prompt enhancer is built on Qwen3.5-9B via SFT+GRPO, not a 27B+ model
(arXiv:2605.10730), while Qwen3.8-27B dense shipped 2026-08-12/14
(https://github.com/QwenLM/Qwen3.8).

**F19. ⚑ The FORMAT INSTRUCTION does the damage, not the decoding constraint.**
Format-requesting instructions cause most of the accuracy loss before any grammar constraint
applies; generating freely and reformatting afterwards recovers most of it. "The Format Tax"
2026 (arXiv:2604.03616); "Capacity, Not Format" 2026 (arXiv:2606.09410) — constrained models
lose 28–36 points, and even a frontier model drops 96.2% → 91.0% on AIME under forced JSON.
**Reason in prose; extract deterministically in a separate pass.**

**F20. Small models can be right and unusable at the same time.** Three 7–9B models reached
85% GSM8K accuracy with **0%** output-format accuracy under naive JSON prompting; grammar-
constrained engines reach up to 96% schema compliance. JSONSchemaBench 2025
(arXiv:2501.10868); "When Correct Isn't Usable" 2026 (arXiv:2605.02363).

**F21. Self-verification does not close with scale; the 2025 result closest to solving it
uses external ENSEMBLES.** Stechly, Valmeekam & Kambhampati 2024/ICLR 2025 (arXiv:2402.08115);
Weaver, NeurIPS 2025 (arXiv:2506.18203) reaches o3-mini-level accuracy by ensembling multiple
distinct weak judges around a Llama-3.3-70B generator. **Reinforces "no model inside a gate,"
and specifies the shape of the exception: a different model, ensembled, never the generator.**

### Modes: what the HCI evidence actually supports, and what it warns about

**F22. Structured fields beat a free-text box, measured three ways.** A subject/style template
beat discursive language on predictability across 5,493 generations (Liu & Chilton 2022, DOI
10.1145/3491102.3501825); a structured refinement UI beat free text on image-match (SSIM
0.648 vs 0.479) and frustration (p<0.01) (PromptCharm, arXiv:2403.04014); a staged structured
pipeline produced 2× more usable outputs (Opal, arXiv:2204.09007).

**F23. Real expert practice is small deltas on ONE long prompt, not fresh composition.** In
2.2M+ logged prompts: median **3–5 terms changed** between consecutive prompts, ~10–14 prompts
per session, prompts 20–30 terms long, and near-zero reuse of others' prompts (0.94%). Xie,
Pan, Ma, Jie & Mei 2023 (arXiv:2303.04587). **The advanced tier's core loop is fast
small-delta re-editing, not a compose-from-scratch wizard.**

**F24. Making the user commit their own answer BEFORE seeing the AI's cut over-reliance on
wrong suggestions from 64% to 48% and raised accuracy 8% → 27% — and users disliked it.**
Buçinca, Malaya & Gajos 2021, N=199 (arXiv:2102.09692).

**F25. Seeing AI images during ideation NARROWED the human's own idea space** — fewer ideas,
less variety, lower originality than an unassisted baseline. Wadinambiarachchi, Kelly, Pareek,
Zhou & Velloso 2024, N=60 (DOI 10.1145/3613904.3642919).

**F26. Contrastive framing improves later judgment but NOT in-the-moment reliance.** 47% vs
39% vs 32% (d=0.35) on independent decisions afterward; **58% vs 58% — no difference** — on
following a wrong suggestion in the moment. Buçinca, Swaroop, Paluch, Doshi-Velez & Gajos
2024, N=628 (arXiv:2410.04253). **Contrastive framing is a teaching device, not a verifier.**

**F27. Expert de-skilling from routine AI assistance is measured in WEEKS.** Endoscopists'
unassisted polyp-detection fell 28.4% → 22.4% within three months (Budzyń et al. 2025, PMID
40816301); after one ~10-minute assisted session, unassisted solve rates fell 0.89 → 0.76
(d=−0.42) with higher give-up rates (Liu et al. 2026, N=1,222, arXiv:2604.04721).

**F28. An LLM assist that SUGGESTS AND CLUSTERS keywords lowered cognitive load** versus a
standard tool. Promptify, Brade, Wang, Sousa, Oore & Grossman 2023 (arXiv:2304.09337, N=14).
**This — not auto-writing the prompt — is the shape the evidence supports for an assist tier.**

**F29. There is NO published evaluation of a three-tier quick/advanced/AI prompt UI.** The
mapping is proposed (Prompt Middleware, arXiv:2307.01142) with comparative evaluation stated
as future work. **We are not implementing a validated pattern; we are building one.**

### Provenance and evaluation

**F30. A seed does not replay a generation.** HF's own reproducibility docs state results "may
not be reproducible between CPU and GPU executions, even when using identical seeds," and warn
against expecting similar results across GPU hardware or PyTorch versions
(https://huggingface.co/docs/diffusers/main/en/using-diffusers/reproducibility). **The minimal
replay unit is seed + generator device + checkpoint + scheduler + steps + library + hardware.**

**F31. Three independent vendors converged on IMMUTABLE VERSION + MOVABLE ALIAS.** MLflow's
registered prompt is immutable with mutable aliases; LangSmith gives each push a content hash
independent of environment tags; Weave's `weave.publish` creates an immutable ref. **Convergent
design across competitors is the load-bearing signal, not one vendor's opinion.**

**F32. DSPy's own docs state its save captures only "learned state" and does NOT preserve
dataset version, seeds, model/provider, or package versions — those "must be recorded
separately"** (https://dspy.ai/getting-started/saving-and-loading/). The framework closest to
this problem names the gap we must close ourselves.

**F33. ⚑ CLIPScore is the WEAKEST metric measured and never ranks top.** Spearman 0.223–0.535
across compositional categories, against 0.520–0.734 for ImageReward; and no metric holds
strong correlation across all categories. Kasaei, Aghayari, Marioriyad et al. 2025
(arXiv:2509.21227).

**F34. ⚑ TEXTURE/MATERIAL is the worst-detected attribute class there is.** Texture-binding
accuracy collapses to **23–43%** while colour binding on the same models holds **93–97%**; the
best VLM judge reaches only 67.4% human agreement. Hayes, Goldblum, Somepalli et al. 2025
(arXiv:2512.02161).

**F35. Embedding metrics pool the whole image into one vector, making them structurally
insensitive to localized semantic violations.** Hartwig, Engel, Sick et al. 2025
(arXiv:2403.11821). **This is the mechanistic reason a small internally-smooth wrong-material
region barely moves a global similarity score** — the exact defect class that decides
acceptance here.

**F36. Nothing off-the-shelf benchmarks our failure class.** A dedicated search for a large,
internally-smooth, wrong-material region on an otherwise-correct object found only
wrong-texture-from-generation benchmarks, not a localized swap. **Confirmed gap; build
in-house or do not claim it.**

**F37. Naive paired tests are invalid for generative A/B once paraphrases are included; a
permutation test stays valid.** Helm & Priebe 2026 (arXiv:2605.27463). And
n ≈ 8/(Δ/s)² at α=.05/power=.8 sizes a run from a small pilot's measured variance
(Krishnamachari 2026, arXiv:2605.00428).

## What the evidence FORECLOSES — do not build these

1. **A front-loading / reordering feature.** F4: p = .399. Ordering is not a lever, and our
   own store said it was.
2. **A CLIPScore gate, or any single-metric quality gate.** F33, F35, F36. This repo already
   refuses to commission a metric where no honest one exists; the literature now says why.
3. ~~**A rewriter tuned on aesthetics or human preference.**~~ **REMOVED FROM THIS LIST** —
   F16 was withdrawn by the citation gate. The concern is real and untested; treat it as a
   question to answer, not a rule to follow. **This entry is left visible rather than deleted
   so the next reader can see that a forbidding instruction was written on an unverified
   number and then pulled.**
4. **A model that emits the schema.** F19, F20. Reason in prose; extract deterministically.
5. **An assist tier that writes the prompt.** F25, F28. Suggest and cluster; do not compose.
6. **Any claim that a seed replays a generation.** F30.

## The architecture this implies

**A. The studio's primary budget is ELEMENT COUNT, and the router just made it visible.**
F1/F2/F3 say a prompt naming 24 elements is far outside any measured regime, and F1 puts a
concrete price on each one. Meanwhile `canon_gate` now REQUIRES 25 phrases for W3 at subject
scope. **Those two facts are in tension and the tension is the finding of this round.** The
studio must show, at authoring time, both the token count (F6/F9, tokenized not estimated)
and the **element count against the evidence** — with the honest note that our encoder's
effective length is unmeasured (F8).

**B. `scopes` is not a gate convenience — it is the mechanism that keeps each prompt inside a
renderable density.** This is the strongest architectural consequence in the round. #18 built
`scopes.views` and `scopes.strokes` empty, and per-view scoping now has an evidence-backed
reason to exist beyond checking: **it is how 24 elements become several prompts that each sit
where binding still works** (F1, F2, F3, F11).

**C. Name our defect correctly: catastrophic neglect, not misbinding** (F12), with attention
overlap as the nearest measured mechanism (F11). And **record that co-location is unnamed in
the literature** (F13) — that is a claim worth making carefully and worth making.

**D. Any model in the studio proposes, discloses, and never admits.** `revised_prompt` as the
precedent (F14); task-tuning rather than scale is the lever, and it is not uniform — 20 of 24
categories (F17); the vendor closest to this task shipped a 9B enhancer with a 27B available
(F18); the verifier is a different model, **ensembled**, never the generator (F21).
⚠ **The size question is now OPEN, not settled** — F15 was the "scale buys nothing" evidence
and the gate withdrew it. Do not read F18 as a size ruling; one vendor's choice is a data
point, not a measurement.

**E. Modes, as the evidence actually supports them:**
- **quick** = structured fields, not a text box (F22)
- **advanced** = fast small-delta re-editing of one long structured prompt (F23)
- **assist** = suggest-and-cluster, shown only AFTER the author's own first pass (F24, F25,
  F28), with contrastive framing understood as a teaching device rather than a safeguard (F26)
- **and the from-scratch path stays in active use**, because de-skilling showed up in weeks
  (F27)
- **say plainly that no three-tier prompt UI has ever been evaluated** (F29)

**F. Provenance: immutable version + movable alias** (F31), pinning far more than the prompt
string (F30, F32), hashing LoRA **weights only** — Civitai's whole-file hash meant identical
weights could hash differently (civitai/civitai#742).

## What to build this round — and argue the scope

My call, and it is a call: **#19 is the WORKSHEET, as promised, plus the element-count
readout from finding A.** The worksheet's schema is now proven by a consumer, which was the
whole reason for the split. The readout rides with it because the worksheet is where a human
decides how many elements a surface list will demand, and shipping the authoring tool without
the density number would be building the thing that causes the problem F1 describes.

Everything else above is architecture for later rounds, deliberately. **If that is the wrong
half, say so.** Seven rounds running you have cut a brief down and been right.

The worksheet, per #18's own boundary statement: kind templates, occupant filling,
IDENTITY→surfaces emission, spatial box binding. Its hard constraint stands — **structurally
incapable of filling an occupant**, and tested for it.

## Argue

1. **The density tension in A is the real question.** If the canon requires 25 phrases and the
   evidence prices each additional element at ~8.5% inclusion, is the canon gate enforcing a
   prompt that cannot render? Or is F1's measurement inapplicable to our regime — different
   model, ControlNet-conditioned, a LoRA that already knows this character? **Both readings are
   live and I am not ruling.** What would settle it without spending credits?
2. **Does the worksheet declare scopes, or only surfaces?** If B is right, the per-view
   surface-id list is as load-bearing as the occupant list, and a worksheet that emits only
   surfaces has emitted half the canon. But you argued in #18 that a human declares scope per
   subject per view — which makes it worksheet work by construction. Is scope declaration in
   this round or the next?
3. **F13 says co-location is unnamed in the literature.** Do we record that as a repo finding,
   and if so what would it take to state it responsibly — given our evidence is one character,
   one surface, three grammatical forms?
4. **F8: our encoder's effective length is unmeasured by anyone.** Is that a cheap local
   measurement, or does it need generation? If cheap, it is the highest-value free number
   available to this project right now.
5. **Anything unnamed.** Seven rounds running.

## Constraints

No GPU, no cloud generation, **no credits**. Read `E:\AI\training\facet_E*\`; write to none of
them. Change-set uncommitted for the advisor's fold. Gates `raise`, never a bare `assert`;
`IMPLEMENTATION:`-labelled asserts are allowed and must say why. Tests ride the commit.

**Next free test file is `t93`.** t92 is yours from #18.

⚠ **A second seat is live in this tree** repairing the index's arc-number parser (E52/E53
unreadable), the t87 artifacts pin (14 ≠ 16), and producing a spend-site census. It is fenced
OFF `tools/canon_gate.py`, `canon/*.surfaces.json`, `canon/*IDENTITY.md` and every
`README*.md` — those are yours. It writes `docs/experiments/E54-router-landing-zone-report.md`.
**Count surfaces are at 1283 / 1229 / 54 as of this brief**; state what your change-set assumes
and reconcile nothing you did not move.

## Calibration

Nominate **one checkable claim** we verify by running it before anything trusts the rest.
Eighteen for eighteen, and a round where the chip loses is still reported.
