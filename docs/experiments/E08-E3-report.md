# E08 — E3 report: the reserve is not the lever, and I halted

**Executor session, 2026-08-04.** Predictions in
`E:\AI\training\facet_E08\ANCHOR\PREDICTIONS-E3.md`, recorded before the launch and **disclosed
as not blind** — I wrote Amendment 17 earlier in this same session while acting as advisor, so I
had the full environment diagnosis in hand.

## ⚠ E3 IS FALSIFIED

**Prediction E3:** *"At `--reserve-vram 10.0` the job completes. Budget becomes 32,607 − 10,240 =
22,367 MiB; plus a 7.6 GB baseline that is 29,967 total, ~1.2 GB under the ceiling."*

**Measured: peak 31,953 MiB, killed by the watchdog at 02:39:28.** The job did not complete. E2
was never reached, so the reproduction anchor is **untested** — neither passed nor failed.

```
launch baseline (nvidia-smi, 02:37:43)   1,144 MiB     <- Amendment 17's second ruling
ComfyUI ready                            1,634 MiB
peak                                    31,953 MiB
kill                                     02:39:28
```

## The climb, and its signature

Monotonic, ~47 s, **entirely at 40–56 W**. 571 W appears only in the kill sample. By the rig's
own diagnostic this is model load, before compute — the same phase as every prior failure.

| time | power | VRAM |
|---|---|---|
| 02:38:50 | 56.1 W | 5,121 MiB |
| 02:39:04 | 49.6 W | 18,110 MiB |
| 02:39:15 | 50.7 W | 25,790 MiB |
| 02:39:21 | 46.9 W | 30,240 MiB |
| **02:39:23** | **47.2 W** | **31,712 MiB — WARN(1/3)** |
| 02:39:26 | 47.7 W | 31,953 MiB — WARN(2/3) |
| 02:39:28 | 571.2 W | 31,953 MiB — **KILL** |

**It does not plateau at any budget. It climbs until the watchdog stops it.**

## The number that kills the reserve theory

```
ComfyUI working set  =  31,953 - 1,144  =  30,809 MiB
budget from reserve  =  32,607 - 10,240 =  22,367 MiB
                                            --------
                                over by     8,442 MiB
```

**`--reserve-vram` did not bound the working set.** 30,809 MiB is within ~200 MiB of the full
staged set the ComfyUI logs name for this workload — TE 7,910 + UNet 19,483 + ControlNet 3,372 +
VAE 241 = 31,006. Everything was staged, and a 10 GB reserve evicted nothing.

## This also retro-falsifies the inference that produced E3

Amendment 17 recorded, from the previous executor's two runs, that *"both runs sat on ComfyUI's
reserve-derived budget, to within allocator noise"* and concluded `--reserve-vram` was working as
documented. Placed beside run 3, that reading does not hold:

| run | reserve | desktop baseline | peak | ComfyUI working set | budget from reserve |
|---|---|---|---|---|---|
| 1 | 8.0 (+`--disable-smart-memory`) | 7,604 | 31,829 | 24,225 | 24,415 |
| 2 | 8.0 | 7,030 | 31,703 | 24,673 | 24,415 |
| **3** | **10.0** | **1,144** | **31,953** | **30,809** | **22,367** |

**The peak is ~31.7–32.0 GB in all three runs — independent of the reserve and independent of the
baseline.** Runs 1 and 2 appeared bounded by their budget because the desktop was occupying ~7 GB,
so ~24 GB was all the card had left to give. The agreement between working set and budget was a
coincidence of the baseline, not evidence the reserve was binding. **Raising the reserve by 2 GB
while the baseline fell by 6.5 GB let the working set grow by 6.1 GB.**

This is the repo's own rule arriving from a new direction: *a number that reproduces exactly can
still be measured against the wrong object.* Two runs agreeing with a budget did not mean the
budget caused them.

**The reboot did not help. It made the failure larger** — more free VRAM, more staged, same kill.

## What did reproduce

The control image came back identical to N11's sidecar: **20,973 px total, canny 15,325, contour
9,958**, figure mask 19.0% of frame. Deterministic across the reboot and both launch changes. The
control half of E2's reproduction question is intact; the sampler half is untested.

## I am halting here

`CLAUDE.md`: *"Stop at every gate. Never improvise past one. A session that changed a parameter
and re-ran when a gate fired hit the same gate harder."*

The obvious next move is reserve 12.0, and **I am not making it.** Run 3 is evidence that the
reserve does not govern this workload's working set at all, so walking it upward is walking a
lever the measurement says is disconnected — and each attempt costs a watchdog kill. A reserve
large enough to matter by subtraction alone would be ~14 GB against a 22 GB requirement, which is
not a tuning step, it is a different hypothesis.

**Unexplained, reported and not acted on:** each model logs `prepared for dynamic VRAM loading,
N MB Staged`, and the staging appears to fill available VRAM rather than respect the reserve.
Whether that is the flag failing on this node set, an interaction with the ControlNet path, or
expected behaviour I have mis-read is not something this run can distinguish, and I have no
measurement that separates them.

**Gap in this run's evidence:** `_comfyui_start.ps1` launches hidden with no redirect, so there is
no ComfyUI log for run 3 — the staged-set figures above are carried from runs 1 and 2. Capturing
stdout on the next launch would cost nothing and would show whether the staging lines differ.

## State left behind

- **Watchdog: alive**, heartbeat 2 s, ceiling untouched at 31,200 MiB. It fired correctly on all
  three breaches. `_watchdog_TRIPPED` holds the 02:39:28 record; `_watchdog_start.ps1` clears it.
- **ComfyUI: down** (killed).
- **`ANCHOR/`**: control + mask written, **no output image**. The anchor did not run.
- Nothing tuned, no parameter changed after seeing a number.
