# E3 + E2 — predictions, recorded before the launch

**NOT BLIND, and the disclosure matters here.** I wrote Amendment 17 in this same session while
acting as advisor, before the Director moved me to executor. I have the full environment
diagnosis, both falsified hypotheses and the reserve arithmetic in context. These predictions
are made with all of it in hand and should be discounted accordingly.

## What is being run

The reproduction anchor: N11's exact configuration, recovered from `N11/w3clay_0_gen.json`.
Every generation parameter in that sidecar is `restylize_views.py`'s default, so the invocation
is inputs + masks + prompts file and nothing else.

```
input   BG/clay_grey/w3clay_0.png   sha256 cac49be7d96c...
mask    BG2/masks/w3clay_0.png
prompts docs/experiments/E08-grammar-test.json
seed 770700  steps 20  cfg 2.5  denoise 0.92  lora_w 0.75  cn_strength 0.9
canny 0.4/0.8  bg 0,0,0  contour_width 3  tol 0.06  erode 5
```

**Two launch changes at once** against the run that produced the anchor: `--reserve-vram`
8.0 → 10.0, and `--disable-smart-memory` is gone. Amendment 17 accepts that — it is a
reproduction check, not an attribution experiment.

## E3 — does the job complete?

**Predicted: yes, and I hold it near-certain.** Budget becomes 32,607 − 10,240 = 22,367 MiB;
against a launch baseline of ~1,150 MiB that is a peak near 23.5 GB, some 7.7 GB under the
31,200 ceiling.

**⚠ And that prediction is nearly worthless as evidence for the setting, which I want on the
record before the number exists rather than after.** The desktop baseline was 7,030–7,604 MiB
when the failures were measured and is ~1,150 MiB now. At today's baseline the job completes at
reserve 8.0 too — the setting that was already measured not to work. **So a completion today is
over-determined: it cannot separate "10.0 fixed it" from "the reboot fixed it."**

This does not change what I run. Amendment 17 picked 10.0 from the worst-baseline arithmetic
(22,367 + 7,600 = 29,967, 1.2 GB under), and that reasoning stands on its own without today's
run. But the run is not a test of it, and I will report it as such rather than let a green
result read as confirmation. **The discriminating test needs a warm desktop, and I am not
going to manufacture one.**

## E4 — is it slower?

**Predicted: yes.** 22,367 MiB does not hold UNet 19,483 + ControlNet 3,372 + VAE 241 = 23,096
resident, so something streams from system RAM. I will report wall-clock against N11's run for
whatever it is worth, noting the machine was rebooted between them, so that comparison is
confounded too.

## E2 — does the anchor reproduce byte-for-byte? THE HALT CONDITION

Target: `d0220e244d5ad2015639153188c488e3f3d317933dbd54eb439724fe1f57f93d`

**Predicted: it reproduces — but I hold this at ~75%, below the previous executor's 85%.**

For: seed, sampler, steps, cfg and the control image are all identical, and the control is
deterministic from unchanged inputs. Memory management decides where weights live, not what the
sampler computes.

Against, and this is why lower rather than higher: **two launch changes instead of one**, and at
reserve 10.0 the model set demonstrably *cannot* stay resident (23,096 needed against a 22,367
budget), so streaming is now guaranteed rather than merely possible. The previous run's 8.0 left
open the possibility that nothing actually moved. Weights are fp8 with a manual cast to
bfloat16; I have no measurement on this stack saying an offload path preserves cast order, and
I am not going to assume one.

**If E2 fails I halt and report. That is already ruled (Amendment 17) and it is not mine to
reconsider at the moment the number appears.** A non-reproducing anchor means SPEC and CONTRA
are not comparable to BRACER, ARMOUR or N11, and the contradiction test measured against a
different machine answers nothing.

## Recorded at launch, per Amendment 17's second ruling

`nvidia-smi` used-MiB at the moment of launch goes in the report. Every prior environment number
in this line is un-attributable without it.
