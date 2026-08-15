# E37 round 2 — HALT: the VRAM watchdog fired and killed the local plate edit

**Seat:** executor · **Date:** 2026-08-15 · **Spend: 0 of 40 cloud jobs — nothing has been
submitted to any cloud, and this halt is on a LOCAL job.** No round-2 plate exists.

Round 2 as ruled ([E37-ruling.md](E37-ruling.md) Ruling 1, kickoff Amendment 1): edit the
source plate locally with Qwen-Image-Edit-2511 to smooth, mark-free clay. **Attempt 1 of
the ruling's three was submitted to local ComfyUI and the watchdog killed it mid-run.**
Reported with its evidence and halted per executor rule 3. No parameter was changed and
nothing was re-run.

---

## 1. What fired

`E:\AI\training\_watchdog_KILL.log`, verbatim:

```
04:53:33  WARN(1/3) VRAM 31543MiB>=31200 - holders: python(pid 33176)=25082MiB |
          dwm(pid 6656)=24740MiB | llama-server(pid 16248)=5276MiB | chrome=439MiB | ...
04:53:37  WARN(2/3) VRAM 31522MiB>=31200 - holders: python(pid 33176)=24986MiB | ...
04:53:40  KILL      VRAM 31324MiB>=31200 - holders: python(pid 33176)=24890MiB | ...
04:53:40  ABORT - VRAM 31324MiB>=31200 - killed win python PID(s):
          8388,8832,14184,15640,29944,33176 | wsl[Ubuntu] not running, skipped
```

Three strikes at 2 s intervals, then the abort. The driver returned **exit −1** with no
output because its interpreter was one of the six PIDs killed.

## 2. This is the documented hazard, at a new site

CLAUDE.md's environment section, which was written about the *restylize* graph and applies
here unchanged:

> The restylize graph stages **31,006 MiB** of models against a **31,200 MiB** watchdog
> ceiling on a 32,607 MiB card… **No reserve value fixes that** — because ComfyUI stages to
> fill whatever it sees free. `--reserve-vram` and `--disable-smart-memory` are both
> falsified as levers here. **The ceiling is never raised.**

Measured for this graph: the ComfyUI interpreter reached **25,082 MiB** on its own. The
weights are 19.1 GB (`qwen_image_edit_2511_fp8mixed`) + 8.7 GB
(`qwen_2.5_vl_7b_fp8_scaled`) + 0.2 GB VAE = **28.0 GB**, which the tool's own preamble
recorded as a risk before submission rather than after.

⚑ **And the holder list names something the arc had not accounted for:
`llama-server(pid 16248)=5276MiB`.** A local LLM server is holding **5.3 GB** of this
card, unrelated to this arc, and it is the whole of the ~6.4 GB baseline every VRAM
reading in this session recorded. `dwm=24740MiB` is the compositor's shared-memory
accounting and is not 24 GB of private allocation; the private holders that matter are the
ComfyUI python and llama-server.

## 3. What is NOT damaged — checked, not assumed

| check | result |
|---|---|
| manifest A `facet_E33` | **HELD** 0/0/0 |
| manifest B `facet_E34` | **HELD** 0/0/0 |
| manifest D `facet_E35` | **HELD** 0/0/0 |
| watchdog itself | **ADVANCING** after the kill (04:54:32 → 04:54:36) |
| `facet_E37\round2\` | **empty** — no partial plate, no sidecar |
| cloud spend | **0 of 40**, untouched |

The kill took six python PIDs. Nothing was mid-write to a protected tree, and the gates
confirm it.

## 4. The link topology was validated before submission, and is not implicated

The driver builds the graph from node handles and walks the finished graph for self-links,
dangling targets and non-integer slots before posting — this repo's E04 Arm G7 law applied
locally. It printed `[graph] 11 nodes, link topology validated` and the plate's sha256
verified against premise 1. **The graph is not what failed; the card is.**

## 5. Dispositions — named, none taken

Executor rule 3: report the gate with its evidence and halt. The disposition is not mine.
What each would require, factually:

1. **Free the 5.3 GB `llama-server` and re-run.** ⚠ Named with its own counter-evidence:
   CLAUDE.md records that **freeing 6.5 GB by rebooting made the working set grow 6.1 GB**,
   because ComfyUI stages to fill what it sees. On that measurement this is as likely to
   move the peak as to lower it, and it would spend a run to find out.
2. **Launch ComfyUI with `--lowvram`.** This is a *different mechanism* from the two flags
   the record falsifies: `--reserve-vram` and `--disable-smart-memory` are hints about
   headroom, while `--lowvram` changes residency — weights stay in system RAM and stream
   per block. The record does not speak to it. It is slower and it does not raise the
   ceiling.
3. **Run the edit on Comfy Cloud instead.** Contradicts Ruling 1's "zero cloud" for round 2
   and would spend from the 40-job ceiling, so it needs the Director's word, not mine.
4. **Rule the local edit infeasible on this card** and route round 2's plate work
   differently.

⚠ **I did not raise the ceiling, disable the watchdog, retry with a changed parameter, or
re-run to see if it passes the second time.** The ceiling is never raised, and re-running a
fired gate hoping for a different number is the one move this record calls always wrong.

**Awaiting the ruling. Zero cloud spent; no round-2 plate exists; round 1 stands unchanged
in the record as the measured baseline.**
