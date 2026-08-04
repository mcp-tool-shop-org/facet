# E08 Step 0b — the cloud anchor: report

**Executor session, 2026-08-04.** Predictions in
[E08-0b-predictions.md](E08-0b-predictions.md), recorded before the run and disclosed as **not
blind**.

## Result: BRANCH 2 — sha differs, ΔE below the floor. Accept, with the boundary recorded.

The three branches were pre-registered in the kickoff before any number existed. The middle one
fired.

```
target sha256   d0220e244d5ad2015639153188c488e3f3d317933dbd54eb439724fe1f57f93d
cloud  sha256   72f5aa60c3efdfdd2126c69f3290dba923aff38cea962fb5d102db0c32d51839
                MATCH: False

whole-figure median ΔE   0.84      <-  the gate.  N11's no-response floor is 1.07
whole-figure mean  ΔE    1.06
        >2.3   6.8%      >10  0.2%
figure                   146,356 px (19.01% of frame)
```

**0.84 ≤ 1.07 → accept.** The threshold is N11's own measured whole-figure median when the model
did not respond to a prompt phrase at all — this pipeline's noise level, not a number invented
for this test. Cloud and local differ by less than the pipeline's own floor.

**Every later report in this line must state that its arms span a hardware boundary.** That is
the price of the branch and it was agreed before the number existed.

## The LoRA loaded — and the region table is how we know

This was the failure I pre-registered as the first hypothesis to check if ΔE went past 1.07. It
did not fire, and the per-region data shows why: **every region holds its colour.**

| region | class | LOCAL | CLOUD | ΔE |
|---|---|---|---|---|
| N4 pauldronR | contra | L 43.4 C 40.2 h 80.2 | L 43.0 C 40.0 h 79.4 | 1.12 |
| N2 beard | contra | L 24.1 C 41.6 h 47.9 | L 24.1 C 41.6 h 47.3 | 0.98 |
| N3 tunic | contra | L 12.1 C 11.6 h 178.4 | L 11.7 C 11.6 h 178.0 | 0.82 |
| N14 blade | **held** | L 57.9 C 1.6 h 266.7 | L 58.2 C 1.8 h 267.1 | 0.70 |

Gold stays gold at chroma 40 and hue 80. The beard stays red, the tunic stays green, the blade
stays neutral steel. A LoRA that failed to load strips the style and moves the whole figure by
far more than one ΔE unit.

By class: **held (control) median 0.71 · contra median 0.98 · coloc 0.65.** The controls and the
rest move together. Largest single region is the medallion at 1.79 — and it is the smallest box
at 340 px, so the noisiest. **Uniform sub-unit drift across every structure** is the signature of
floating-point kernel differences across two architectures, not of a structural difference.

Sheet: `ANCHOR/anchor_local_vs_cloud.png` — LOCAL | CLOUD | ΔE heat, plus the crop-free
hue×chroma density for both. Numbers: `ANCHOR/anchor_dE.json`.

## Prediction against outcome

| branch | predicted | fired |
|---|---|---|
| exact sha | ~25% | no |
| sha differs, ΔE ≤ 1.07 | **~70%** | **yes** |
| ΔE > 1.07, halt | ~5% | no |

## Corrections to my own work, and they cost time

**The LoRA was already on Comfy Cloud from the day before.** I did not check, and instead pushed
a fresh copy to `mikeyfrilot/saltroad-lora` and imported it. The run used the one that was
already there:

```
mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500.safetensors
```

**Checking the Model Library for an existing copy costs one call and comes before creating a
delivery path.** The `mikeyfrilot/saltroad-lora` repo I created is redundant and can be deleted.

**I also mis-ordered the two candidate names.** Holding a name that showed `FINISHED` in the
import panel, I submitted the *other* one first on the reasoning that a same-filename model under
a different repo might be a different checkpoint. That reasoning is not wrong in general, but the
Director had the ground truth — same LoRA, uploaded the day before — and one question would have
resolved it before a wasted submit. That job was cancelled before it consumed GPU.

**What held up:** the graph itself. Every one of the fifteen nodes, all five model names and all
the load-bearing wiring — render→latent, control→ControlNet, ControlNet output 0/1 split, UNET →
LoRA → ModelSamplingAuraFlow, `LoraLoaderModelOnly` — ran first time with no correction.

## What the "bundled node index" warning is worth

Both submissions returned `input_validation` warnings that the `lora_name` "was not found in the
bundled node index," and the job ran correctly anyway. The MCP's own schema says local validation
uses a bundled catalog that can lag the cloud. **That warning does not indicate a missing model
and should not be read as one** — the Comfy agent's UI-side rejection against a stale 643-option
list was the same staleness with a harder failure mode.

## State

- `prompt_id` `4aa20f33-9141-46aa-8f4c-52da3614a71b`, completed.
- Output at `ANCHOR/cloud_w3clay_0.png` (595,406 bytes).
- Cancelled job `b8005ce8-77c4-4ddf-85d4-b4102a205421` (wrong LoRA name), no GPU consumed.
- Local rig untouched: ceiling 31,200 MiB, watchdog alive.
