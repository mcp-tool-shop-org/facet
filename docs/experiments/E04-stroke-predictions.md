# E04 stage 2 — stroke-camera predictions, registered BEFORE the derivation runs

**Executor session, 2026-08-05 (early).** Written before `e04_stroke_cameras.py` exists as
a file. I have read `ship.json`, the stage-1 report's hole map, `texpass_iter.py`'s commit
path and Ruling 23. I have **not** cast a single ray in this session, and no derivation
artifact exists.

**Blind status: BLIND on P1–P9.** P10 is a *declared prior* rather than blind — it is
arithmetic over a profile edit I have already scoped, and I state it so the arithmetic is
checkable rather than asserted afterwards.

---

## The instrument these predictions are about

For a candidate stroke camera `(yaw, el)`, a hole texel is **commit-reachable** when it
passes what `texpass_iter.py commit` actually tests, in that order:

1. `facing = N . dtc > 0.25` — `ship.json` `texpass_iter.facing-min`;
2. **unoccluded** — a ray from the texel toward the camera escapes;
3. **not thin-withheld** — the figure's extent *along the view ray through that texel* is
   at or above `thin-extent 0.01`, because `emit` removes thin pixels from the job mask
   (`hm = hm & ~thin`) and `commit` requires `injob`;
4. **not edge-trimmed** — the texel's projected pixel sits at least `edge-dist 4.0` px
   from the boundary of the rendered figure mask.

Step 4 is modelled against `emit`'s **geometry** hit mask; the shipped guard runs on the
brush output's keyed mask *intersected with* that same hit mask, which is a subset — so my
step-4 survivor set is an **upper bound**. Steps omitted entirely: the 9 px job-mask
dilation (which only ever admits more), and whether the brush paints anything plausible.

Camera candidates are constrained to `ship.json`'s `cull_unseen.production` superset — the
24 yaws at 15 deg, elevation 0, plus `(0,40) (180,40) (0,55) (180,55)`. A camera outside
that list would need the superset widened, which is a ruling, not a derivation.

**Deck strokes are not derived** — Ruling 23 fixes them at the Task 4a pair `(0,40)` and
`(180,40)`.

---

## Predictions

| # | prediction | falsifiable as stated |
|---|---|---|
| **P1** | The two ruled deck strokes together commit-reach between **150,000 and 350,000** hole texels (union, all surface classes). | fails outside that band |
| **P2** | After those two strokes, between **50% and 65%** of the 489,889 upward-facing holes remain unpainted. Ruling 23 pre-registered "roughly half"; this is that claim made numeric. | fails outside that band |
| **P3** | The greedy's **first side pick is an intermediate yaw** — one of the sixteen 15 deg-grid yaws that is *not* a stage-1 camera. Reason: stage 1 already took the well-facing surface at 0/45/.../315, so a repeat yaw can only harvest the 12.2 deg grazing annulus the floor drop 0.45 -> 0.25 opens. | fails if the first pick is in {0,45,90,135,180,225,270,315} |
| **P4** | That first side stroke's marginal gain on **side-class holes** exceeds **60,000** texels. | fails below 60,000 |
| **P5** | Decay is steep: the **4th** side stroke's marginal gain is **below 40%** of the 1st's. | fails at or above 40% |
| **P6** | The proposed side set takes hull-foot ("waterline rim", lowest 7% of the mesh) styled coverage from **19.44%** to between **30% and 55%**. | fails outside that band |
| **P7** | In the derived spiral order the **first stroke is an eye-level camera**, and **both elevated deck strokes fall in the last third** of the order — because the deck is this subject's least-painted class (24.99% against 40.05%) and the spiral runs outward from paint. | fails if a deck stroke opens, or if either lands outside the last third |
| **P8** | Thin-withholding costs between **5% and 15%** of each camera's otherwise-committable hole texels, on **every** candidate — the hole-texel analogue of the 10.20%-of-visible-area figure `ship.json` records for `thin-extent 0.01`. | fails if any candidate falls outside that band |
| **P9** | The 4 px edge trim costs **more** than thin-withholding on the two **end-on** cameras (yaw 90 and 270), whose silhouettes are smallest and therefore most boundary. | fails if thin costs more on either |
| **P10** | *(declared, not blind)* After lifting `_NOT_CLEARED` and deciding all seven `texpass_brush` keys, `--coverage` returns **0 UNDECIDED** and the `[chk]` mismatch list grows by **exactly one row** — `texpass_brush.py prompt` — from 16 to 17. The other six ship values equal the tool's own source defaults digit for digit. | fails at any other count |

## Two things I expect to have to report as findings, stated now

**`brush_cloud_step.py` does not bind a profile.** It carries its own
`DEFAULTS = {"seed": 770700, "steps": 20, "cfg": 2.5, "lora_w": 0.75, "cn_strength": 1.0}`
and a hardcoded `CLOUD_LORA`, and it takes the prompt and the negative from the prompts
file. Generation is cloud-only, so **the ship's strokes run through this tool, not through
`texpass_brush.py`** — which means the profile keys Ruling 23 is about reach the graph for
`prompt`/`negative` (via the fixture) and **not at all** for the five recipe numbers. On
this subject the numbers coincide, so nothing misbehaves; the mechanism is Finding-B's
exactly, and `brush_cloud_step.py` is absent from `character.json`, so `--coverage` cannot
see it.

**The negative is not obviously a "recipe key at the character route's values".** W3's
*brush* negative is not W3's *restylize* negative — it carries eight earned belt terms
(`braided belt, plaited belt, ... baldric, bandolier`) measured at the brush stage on that
character. Transcribing those onto a galleon is Ruling 2's accident class. I expect to
propose the ship's **own spent** negative instead and to flag the deviation rather than
pick silently.

## What would make me wrong in a way that matters

P3 and P4 both assume the residual side-class holes are *obliquity* holes — surface the
eight stage-1 cameras saw too edge-on. If instead they are **occlusion** holes — surface
behind rigging, inside the waist, under the forecastle — then no eye-level yaw will buy
much, every marginal gain will be small and flat, and the honest output is that the side
class is not a stroke problem at all. I would rather report that than tune toward a set.
