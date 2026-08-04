# E08 Task 3 step 3 — pre-flight: the brush graph is portable, and the transport is not

**Executor session, 2026-08-04.** Steps 1 and 2 are done (Branch A banked, fixture prompts
written and mechanically checked). Step 3's free pre-flight is complete. **Nothing has been
submitted and nothing has been spent.** One gap needs naming before the first stroke, because
bridging it changes the recipe rather than a parameter.

---

## 1. The resource, enumerated before building a path to it

Per CLAUDE.md — *before building a path to a resource, enumerate the resource.* The brush is a
**different graph** from restylize (inpainting, not canny-lock), so its dependencies were
enumerated from source and then queried, not assumed from the restylize migration.

| dependency | brush needs | cloud |
|---|---|---|
| diffusion model | `qwen_image_fp8_e4m3fn.safetensors` | present |
| text encoder | `qwen_2.5_vl_7b_fp8_scaled.safetensors` | present |
| VAE | `qwen_image_vae.safetensors` | present |
| **controlnet** | `Qwen-Image-InstantX-ControlNet-**Inpainting**.safetensors` | **present**, exact name |
| **LoRA** | `mikeyfrilot__saltroad-lora__saltroad_style_v2_lowlr_000001500.safetensors` | present (imported; name read off the card, not predicted) |
| **node** | `ControlNetInpaintingAliMamaApply` | **present**, `core` pack, input signature matches the graph exactly |

> **A correction to my own inference, made mid-check.** Reading
> [E08-cloud-migration-state.md](E08-cloud-migration-state.md)'s model table I said the cloud has
> ControlNet-**Union** while the brush needs ControlNet-**Inpainting**, and called it decisive.
> **It is not.** That table enumerated what *restylize* needs; the Inpainting variant is also in
> the catalog, by exact name, and its recommended parameters (steps 20, cfg 2.5, euler, simple)
> match what the brush already passes. The measurement overturned the inference within a minute
> of my stating it — which is the point of querying rather than reasoning from a neighbouring
> document.

**`submit_workflow` with `dry_run: true` on the exact brush graph returned
`status: "validated"`.** One warning, and it is the expected one: the imported LoRA name is not
in the bundled node index — identical to the warning the restylize graph carried before it ran
and landed the 0b anchor at ΔE 0.84. Every `class_type` resolves, every link is sound.

**`estimate_credits`: 0 credits — no paid API nodes.** The graph is entirely OSS models, so the
cost is Creator-plan GPU time, not a per-call purchase. Amendment 28's *"halt on surprises"* is
satisfied: 0 is not a surprise.

**Watchdog: UP.** Heartbeat fresh (15:36), VRAM 7,541 / 32,607 MiB — 23,659 below the 31,200
ceiling. The dispatch's *"watchdog is DOWN, heartbeat stale since 10:41"* is stale; no restart
was needed. Recorded because the dispatch asked for the restart to be reported either way.

## 2. The gap: the brush has no cloud transport

`texpass_brush.py` posts to `http://127.0.0.1:8188` — a **local** ComfyUI — and
`texpass_loop.ps1` calls it per stroke. The standing rule is absolute: *generation runs on Comfy
Cloud, never locally; the ceiling is never raised.* So **the shipped loop cannot run these
strokes as-is**, and Amendment 28's step 3 (*"the cloud graph dry_run + estimate_credits before
any submission"*) assumes a cloud path that does not exist in the code.

Three ways to bridge it, with what each costs:

1. **Hand-drive each stroke through the MCP.** `emit` locally → upload `render.png` + `mask.png`
   → `submit_workflow` → download to the job dir as `inpainted.png` → `commit` locally. Uses the
   pipeline's own `emit`/`commit` **unchanged**, needs no credential, and is the pattern
   [E08-cloud-migration-state.md](E08-cloud-migration-state.md) already proved for the restylize
   anchor. **Cost: `texpass_loop.ps1` is not the thing that ran.** Eight hand-driven iterations
   replace one unattended recipe invocation, so the run is no longer reproducible by re-running
   the loop — PIN_PER_STEP degrades from "one command" to "eight logged calls".
2. **Add a cloud transport to `texpass_brush.py`** via the official API (`cloud.comfy.org`,
   `X-API-Key`), the `comfy_cloud_bridge.py` pattern. Keeps the loop intact and reproducible.
   **Cost: needs an API key entered as a credential, which this session does not handle**, and it
   is a new code path in a route-active tool immediately before the deliverable run.
3. **Run the brush locally.** Refused. The restylize graph stages 31,006 MiB against a 31,200
   ceiling; more to the point, a measured arm on the local rig is a number credited to the wrong
   cause, and the rule has no exception.

**I have not chosen.** (1) is the only one I can execute unaided and it does not touch a measured
parameter — but it silently changes *what the recipe is*, and this repo's own history says a
recipe that does not reproduce its output is not a recipe. That is a ruling, not an executor's
call, and it is the one thing standing between here and eight strokes.

## 3. Bounded before spending: the strokes can reach 26.3% of the holes

*Bound an expensive arm before spending it.* [brush_reach.py](../../tools/diagnostics/brush_reach.py)
applies `texpass_iter`'s own acceptance — `basis(yaw, el)` verbatim, `facing > 0.25` (commit's
floor, not projection's 0.45), plus depth visibility — to the eight-camera hole map.

| stroke camera | sees holes | % of holes | new vs running union |
|---|---|---|---|
| y+090_e+00 | 31,240 | 4.17% | 31,240 |
| y+270_e+00 | 38,930 | 5.20% | 38,930 |
| y+045_e+00 | 48,077 | 6.42% | 27,801 |
| y+135_e+00 | 29,178 | 3.89% | 12,536 |
| y+225_e+00 | 59,012 | 7.88% | 24,015 |
| y+315_e+00 | 35,704 | 4.77% | 7,612 |
| y+000_e+55 | 74,722 | 9.97% | 36,323 |
| y+180_e+55 | 94,484 | 12.61% | 18,942 |

```
holes the eight stroke cameras can reach   197,399 of 749,151 = 26.3%
holes NO stroke camera can reach           551,752            = 73.7%
```

**E06 measured brush coverage at 52.7% of holes. It is now 26.3%** — and the reason is that
stage 1 got better, not worse. The twins have taken 68.8% of valid texels, including everything
an exterior camera sees easily; what remains is surface no eye-level or +55 camera can reach at
all. The brush's *share* falls because its *job* shrank.

### The projected provenance mix, pre-registered as a ceiling

If every stroke commits everything its camera can see — an upper bound, since commit also
applies the emit dilation, `--thin-extent` withholding and the edge-distance guard:

| | projected | E07's rejected asset (measured) | ratio |
|---|---|---|---|
| reference (stage 1) | 1,653,659 — **68.8%** | 28.4% | **×2.42** |
| brush / diffusion invention | ≤ 197,399 — **8.2%** | 37.7% | **×0.22** |
| dilation / interpolation | 551,752 — **23.0%** | 33.9% | **×0.68** |
| non-dilated total | 1,851,058 — 77.0% | 66.1% | ×1.17 |

**Recorded before the strokes run so it is a prediction, not a post-hoc claim.** Whether a
2.42× shift toward reference changes the Director's verdict is Gate 1's question and nothing
here anticipates it — E07 demonstrated a metric moving 70× while the asset was unchanged to the
eye.

**And the dominant residual is now dilation, not invention.** 23.0% of valid texels will be
filled by the flood the README names as still bleeding between unrelated islands — 74.9% of
dilated texels taking colour from another island, median 61 triangle edges away. On this asset
that flood is the largest single provenance class after reference.

## 4. One observation, recorded not acted on

**The brush camera set was designed against a two-camera stage 1.** Six eye-level yaws plus two
at +55, chosen when yaws 0 and 180 were the only styled directions and everything else was hole.
Stage 1 now styles all eight yaws, so the set's rationale — and the spiral order's, which exists
to start adjacent to already-painted regions — is weaker than when either was measured. The
order is byte-identical to the shipped default in the new prompt file, deliberately: changing it
would be a second variable in a run that already carries one (the prompts). Named here as a
post-Gate-1 candidate alongside the blade arm and A3's cap.

## 5. State

```
stage1_8cam.png              Task 3's input, unmodified, Branch A banked
E08-brush-prompts.json       v1.0.0 — 16/16 NAMED elements in all 8 prompts, struck term
                             absent, N7 as a head noun, order byte-identical to the shipped
                             default, negative inherited from Arm B
brush_reach.json             the 26.3% bound
tools/diagnostics/{gained_bg_check,flagged_identity,brush_reach}.py    new
```

Nothing submitted. No credits spent. No local generation. No stroke run, so the corner-median
licence's first-stroke invariance anchor is still untested — it cannot run before a stroke does.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **1** | **The honest score.** The graph, models, LoRA name and every sampler value are pinned and dry-run validated — but the *transport* is unresolved, and option (1) would make the run eight logged calls instead of one recipe invocation. Remediation is the §2 ruling; owner: advisor, before the first stroke |
| ANDON_AUTHORITY | **3** | Stopped at the transport gap rather than improvising a method change; `dry_run` and `estimate_credits` run before any submission as the amendment requires; the arm bounded before spending |
| NAMED_COMPENSATORS | **2** | Nothing irreversible attempted. Cloud spend is bounded and measured at 0 credits; the next irreversible act (uploading inputs, submitting a job) is precisely what this report precedes |
| DECOMPOSE_BY_SECRETS | **2** | Prompt recipe separated into its own versioned file; the reach bound is a separate tool from the loop it bounds; `emit`/`commit` untouched under every option |
| UNCERTAINTY_GATED_HUMANS | **3** | The transport is presented as three options with what each costs and no choice made; the provenance ceiling is stated contrastively against the rejected asset before the run |
| EXTERNAL_VERIFIER | **1** | `skip:` — deterministic. The cloud's own pre-flight validator is an external check on the graph and it passed; my ControlNet-Union inference was overturned by querying rather than by reasoning |

---

**Steps 1 and 2 complete. Step 3's free pre-flight complete. Halted on the transport ruling** —
the graph is portable, the spend is 0 credits, the arm is bounded at 26.3%, and the only
remaining question is whether eight hand-driven MCP calls are an acceptable substitute for the
shipped loop, or whether the loop gets a cloud path first.
