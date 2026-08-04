# Arm B — the two re-rolls: report, and a threshold I mis-derived

**Executor session, 2026-08-04.** One re-roll each of views 2 and 6 at **seed 770701**,
everything else byte-identical. Rejected twins preserved on disk as
`twin_{2,6}_REJECTED_seed770700.png` per the ruling — evidence, not tidied away.

## The invented garments are gone

| | before (seed 770700) | after (seed 770701) |
|---|---|---|
| **twin_2** off-palette | 5,646 px · 6.24% · **blob 5,068** | 1,073 px · 1.18% · **blob 402** |
| **twin_6** off-palette | 6,206 px · 6.85% · **blob 4,882** | 603 px · 0.67% · **blob 345** |

**The blob bound is the one the palette declaration named as the garment detector** — *"the blob
bound is the one that catches an invented garment"*, written before the re-roll — and **both
re-rolls pass it**, 402 and 345 against a bound of 800. Confirmed by eye at
`ARMB/reroll_offpalette.png`: view 6's blue sleeve is gone, view 2's olive leg mass is gone.
What remains is scattered marks at the gold/green boundary on pauldron scrollwork and skirt
edges.

The dominant off-palette hue on both moved to **110–120°** — the *same band the six passing views
carry*. View 6's blue (290–300°) has no successor.

## But both still fail the percentage bound — and that threshold is mine and it is wrong

```
twin_2  1.18%   twin_6  0.67%    against max_offpalette_pct 0.50%
```

**I derived 0.5% from a wrong prior and I am reporting that rather than changing it.** The
palette JSON says the thresholds were *"set from the seven clean views measuring exactly 0 px,
so any non-zero result is already outside the observed distribution"* and *"an order of magnitude
above nothing."*

**That 0 px came from my ad-hoc blue-only check, not from this gate.** The palette gate's actual
clean-view baseline is **0.06%–0.33%**, so 0.5% is **1.5× the highest clean view**, not an order
of magnitude above nothing. The stated justification does not describe the number.

**I have not touched it.** Retuning a pass condition after seeing the result it would have to
clear is the one move this repo treats as always wrong, and it does not become acceptable because
I am the one who mis-set it.

## And the percentage's denominator moves with the camera

The profile views carry the smallest figure area, so a fraction penalises them for geometry
rather than for paint:

| view | figure px | off-palette px | % |
|---|---|---|---|
| twin_5 (rear ¾) | 149,780 | 462 | 0.31% |
| twin_3 (rear ¾) | 120,439 | 401 | 0.33% |
| **twin_6 (profile)** | **90,553** | **603** | **0.67%** |
| **twin_2 (profile)** | **90,553** | **1,073** | **1.18%** |

**In absolute terms twin_6's 603 px sits beside twin_5's 462 and twin_3's 401.** It fails on the
denominator — a profile has ~60% of a front view's area at a comparable perimeter, so
boundary-scale noise is structurally a larger fraction. This repo has been caught by moving
denominators three times; this is a fourth instance, and it is in an instrument I wrote today.

twin_2 at 1,073 px is genuinely higher in absolute terms — roughly 2.3× the passing views — so it
is not purely a denominator artifact.

## What the ruling says, and why I am not executing it

The ruling: *"If the re-roll also fails, that's the result — project seven and take the coverage
cost. No third roll."* Read literally, both fail, and Arm B projects **six**.

**I am halting instead of projecting six, because the failure may be my instrument rather than
the twins**, and dropping two cameras is not recoverable by measurement afterwards. The facts, so
the call is yours and not mine:

- The bound designed to catch the garment **passes on both**.
- The bound that fails was justified by a baseline that does not exist.
- The remaining off-palette mass is the same hue band and the same scale as on the six views that
  passed.
- One of the two failures is substantially a denominator effect; the other is not.

Three readings are available and I am not choosing between them: project six as ruled; treat the
blob bound as the operative gate and project eight; or re-derive the percentage bound from this
gate's own measured baseline — which would be a *correction of a documented error*, not a retune,
but that distinction is the same one you ruled on for the re-roll and it is yours to draw again.

**Nothing is projected. No third roll. No threshold changed.**

## Artifacts

`ARMB/palette_gate.json` (before) · `ARMB/palette_gate_postreroll.json` (after) ·
`ARMB/reroll_offpalette.png` (before/after overlays) ·
`ARMB/twins/twin_{2,6}_REJECTED_seed770700.png`.
`prompt_id` v2r `1f3928bf-6f8d-47af-939d-820e1cce5ec2` · v6r `2b9171ae-0f2c-41d5-a007-c22c52985b2a`.
