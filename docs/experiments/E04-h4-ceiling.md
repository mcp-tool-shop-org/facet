# E04 — H4's reach ceiling, PRE-REGISTERED before any projection

**Executor session, 2026-08-04.** The spec requires this computed and pre-registered **before
the atlas is read**. It is committed here before the 1072 twin batch is submitted and long
before any projection. Pure geometry — no diffusion, no twin, no atlas. A camera that does not
exist yet reaches exactly as much surface as one that does.

Measured on `E04_shipprep` — the prep bake that completed this session once Ruling 16's
tolerance landed. Camera set: the ship profile's **eight eye-level yaws** (Ruling 13: eight,
not ten). Acceptance thresholds from `profiles/ship.json`'s ruled `project_twins` block:
`facing-min 0.45`, `head-facing-min 0.45` (the head band is inert on this subject by Ruling 14
— no ship surface gets looser treatment).

## THE PRE-REGISTERED CEILING

> **42.72% of valid texels** — 1,329,359 of 3,111,832 — is the most that stage 1 can reach on
> this subject from the eight twin cameras at the ruled facing floor.

*⚠ Annotated 2026-08-05 (E10 Ruling 4's measurement): the valid mask on disk measures
**3,111,817** — as `provenance.json` and `offsurface.json` both record — against the
3,111,832 quoted above. Both denominators yield 42.72% at 2 dp, so no quoted figure turns on
the 15-texel difference; the cause is undiagnosed and stays that way unless a consumer ever
depends on the exact count
([E10-offsurface-ruling.md](E10-offsurface-ruling.md) Ruling 6).*

**Stage-1 share cannot exceed this number.** Any measured share is a fraction of it, and the
honest denominator for reading the finished asset is this ceiling, not 100%.

## The ladder, and what it says about H4

| camera set | texels | % of valid |
|---|---|---|
| 2 (front/back) | 646,842 | 20.79% |
| 4 | 926,889 | 29.79% |
| 6 | 1,201,035 | 38.60% |
| **8 — the twin set** | **1,329,359** | **42.72%** |
| 12 | 1,446,520 | 46.48% |
| 8 + the elevated pair | 1,509,005 | 48.49% |
| 12 + the elevated pair | 1,605,776 | 51.60% |

Marginal gain per camera, in turnaround order: +337,165 · +309,677 · +127,552 · +152,495 ·
+114,710 · +91,143 · +110,674 · +85,943. **The eighth camera still buys 85,943 texels (2.8
points)** — this set is not at its plateau, and four more cameras would buy only 3.8 more
points.

**H4 stated the ship's reference share runs structurally lower than the character's.** The
character's reach is **74.1%** (Ruling 5). The ship's is **42.72%** — **31.4 points lower**,
and that is geometry, not a pipeline regression. Ruling 5 banked the expectation; this is its
number.

## How much of the gap is the facing floor, and how much is the subject

Same eight cameras, same prep, floor varied:

| facing floor | texels | % of valid | |
|---|---|---|---|
| **0.45** — ruled production | 1,329,359 | **42.72%** | the pre-registered ceiling |
| 0.18 — the character's head value | 1,586,292 | 50.98% | +8.3 points |
| 0.00 — pure visibility, no floor at all | 1,737,764 | 55.84% | +13.1 points |

**Even with no facing floor whatsoever, eight eye-level cameras reach only 55.84%.** So of the
57.3 points this subject cannot reach at production settings, **44.2 are geometry** — surface
no exterior eye-level camera sees at any obliquity — and 13.1 are the facing floor. That is
consistent with `ship.json`'s own banked note that deck coverage plateaus near 53% because
roughly half the upward-facing surface sits under sails, yards and tops.

## ⚠ A reporting trap in the instrument, found and reported

`e08_ceiling.py` prints **three settings blocks** — `production (body X / head Y)`,
`uniform 0.45`, `uniform 0.18`. With this subject's arguments **all three returned identical
numbers**, which reads like three independent confirmations and is one measurement printed
three times: the third block computes `(args.head_facing_min, args.head_facing_min)`, and the
ship passes `head-facing-min 0.45`, so its label **`uniform 0.18` is hardcoded text, not the
value used**. The second block is a duplicate of the first for the same reason — the ship's
head band is inert by ruling.

Verified rather than assumed: re-run with `--facing-min 0.18 --head-facing-min 0.18` and the
number moves to 50.98%, and at 0.0 to 55.84%. **The tool is not broken and the ceiling is not
wrong** — but a row whose label misdescribes the value it used is the same family as a profile
key that does not reach its tool, and it goes in the work-item bundle as a one-line fix.

## Also recorded

**Front/back overlap is 0 texels.** At N=2 the yaw-0 and yaw-180 twins share no texel at all on
this subject. Not load-bearing for the eight, but it is the population a hold-one-out
comparison at N=2 would have had, and it is empty.

## What this does not establish

Nothing about what stage 1 will *actually* paint — only what it can physically reach. The
measured share, the dilation and brush split, and whether any of it is good are downstream of
the twin-baseline halt and of the Director's eye.

Artifacts: `E04_armT72/ceiling/ceiling.json`, `ceiling_f018.json`, `ceiling_f000.json`.
