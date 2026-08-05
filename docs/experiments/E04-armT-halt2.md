# E04 Arm T — restart sequence: three gates PASS, then three findings. HALT before the batch.

**Executor session, 2026-08-04, after Ruling 13.** The pre-stated restart sequence ran and
**every gate passed to the digit**. Two further findings came out of work beyond the gates, and
a third out of comparing the two profiles. **No twin has been generated. No cloud call was made
this leg. Nothing has been projected. No file outside `docs/` and the training tree was
touched.**

The eight twins are **one command away** — renders, silhouettes, controls and prompts are all
built and clean, predictions are committed blind at `b8245a7`. What stands between here and the
batch is Finding A, and Findings B and C say the advisor's seat is required before projection
regardless.

---

## The restart sequence, as pre-stated in Ruling 13 §"Arm T restarts"

| # | check | result |
|---|---|---|
| 1 | `git pull` | at `b0bf4a7`, Ruling 13 |
| 2 | purity check on the ship profile — restylize row gone, **NO-SUCH-FLAG anywhere → halt** | **PASS** — 16 values / 6 tools, **zero NO-SUCH-FLAG rows**. Eight VALUE-DIFFERS rows (the profile working, per your pre-ruling) and one `cull_unseen.production` *not evaluable* (the checker's known limit on an expression default) |
| 3 | `restylize_views` loads clean | **PASS** — `[profile] ship (ship.json): 0 values applied to restylize_views.py`, no ANDON |
| 4 | one width-fit framing verification, **expect 1 px / 0 px on views 1/7** | **PASS, to the digit** — view 1: 1 px, hit **321,219** vs mask **321,218**, centroid shift (−0.0004, −0.0009); view 7: **0 px**. That is Ruling 11's adjudicated instance reproduced on a fresh invocation from the ratified profile |

The profile now drives the framing on its own: a profile-only `turn_render` + `silhouette_masks`
pair reports `v_ext 1.155008  h_ext 1.202382` — the width-fit numbers, no explicit flag passed.

## Finding A — a nonzero on view 5. Ruling 11's reading two, verbatim.

Ruling 13's gate is views 1/7 and it passed. I then ran the same instrument on the other six,
because all eight are twin cameras:

| view | 0 | **1** | 2 | 3 | 4 | **5** | 6 | **7** |
|---|---|---|---|---|---|---|---|---|
| differing px | 0 | **1** | 0 | 0 | 0 | **2** | 0 | **0** |

**View 5 (yaw 225°) differs by 2 px** — hit 321,216 vs mask 321,218, centroid shift
**(0.0, 0.0017) px**, hit bbox **[716, 849]** identical to mask bbox **[716, 849]**.

I classified the differing pixels rather than leaving the count to speak, using the tool's own
boundary/interior question:

| view | diff px | **on the silhouette boundary** | interior | coordinates |
|---|---|---|---|---|
| 1 | 1 | **1** | 0 | (440, 324) |
| 5 | 2 | **2** | 0 | (609, 346), (367, 360) |

**Every differing pixel is on the boundary. None is interior.** View 5's two are 242 px apart —
scatter, not a contiguous edge segment.

That is **Ruling 11's second pre-registered reading, word for word**: *"A handful of boundary
pixels in uniform scatter → float edge-ordering at the silhouette; report the count and halt
for a ruling, do not tune."* So: reported, and halting. I have not tuned, not chased the
triangle (Ruling 11 declined that), and not adjudicated it — adjudicating is not mine.

Structure worth having, because it is free and it constrains the cause: **views 1 and 5 are the
yaw-45/225 pair**, the axis where `cam_axes`' snap does not apply — Ruling 11's own note,
*"multiples of 45 that are not multiples of 90 keep their irrational components; nothing
anchors them."* The other non-90 pair, views 3 and 7 (135°/315°), both measure **0**. And every
view's mask area is identical to its opposite (321,218 / 318,751 / 290,478 / 198,036), which is
what an orthographic silhouette does — opposite directions give mirrored outlines of equal
area. So the disagreement is +1 on one side of the 45° axis and −2 on its mirror.

For scale, the failure class this anchor hunts measured **4.68%** with a 34 × 42 px bbox gap.
This is 0.0006% with no gap at all and an unmoved centroid.

**The question, in one line:** does view 5's 2 px take the same adjudication as view 1's 1 px,
or does it need something else? Everything downstream is staged either way.

## Finding B — a value "SUSPENDED" in `ship.json` is not disarmed. It silently becomes W3's number.

`subject_profile.bind()` reads **only** `prof["tools"]`. `_gates`, `_still_suspended`,
`_fixtures`, `cameras` and `backdrop` are documentation blocks the loader never touches — and
when a tool has no block it prints *"no block for this tool — defaults unchanged"* and proceeds
on **the tool's own defaults, which are the character's measurements.**

So the suspensions `ship.json` states in prose do not reach the code:

| `ship.json` says | what `project_twins` would actually use | what that number is |
|---|---|---|
| `_gates.reg_iou_min: null` — *"SUSPENDED… run with the halt suspended and REPORT the IoU per view"* | `--reg-iou-min` **0.80** | W3's adjudicated halt, **armed**, on a subject with no distribution |
| `_gates.bbox_tol: null` — SUSPENDED | `--bbox-tol` **0.25** | W3 data |
| `_still_suspended.acceptance` — *"facing floors and the edge-dist family, including edge-ref (700.0 is literally one character's figure width in twin pixels), await twins on this subject"* | `--facing-min` **0.45**, `--edge-dist` **7.0**, `--edge-ref` **700.0**, `--edge-floor` **2.5**, `--head-facing-min` **0.18**, `--head-edge-dist` **3.0** | all W3, including the one the profile itself names as one character's figure width |

And **five tools in `character.json` have no block in `ship.json` at all**:

| tool | ship block | what the ship would inherit |
|---|---|---|
| `bake_hero_prep.py` | **none** | `--crop 360,240,700,600` (W3's **face rect**) and `--head-scale 3.0` — which *is* `_still_suspended.allocation`, *"No privileged region has been chosen… Not decided, not guessed"* |
| `texpass_brush.py` | **none** | `--prompt` defaults to **`"a burly bald warrior with a long red beard, dark green knitted sleeveless tunic, polished gold pauldrons…"`** — the literal W3 identity string. **This is Ruling 2's named accident class, still live, and stage 2 of this experiment is the caller.** |
| `smart_decimate.py` | none | W3's `body-weight`, `pad-frac`, `crop-res` |
| `verify/head_render.py` | none | — explicitly fine: `_gates.head_rect_metrics: false` declares head instruments meaningless here, so absence is a decision |
| `verify/mesh_stats.py` | none | — same; Gate 0 already ran it and recorded its front-view-rect warning as the instrument correctly noticing it is not looking at a character |

**The shape of the finding:** the profile system's ANDON catches a key that names a flag the
tool does not have (Finding 2 of the last halt). It has **no ANDON for the opposite case** — a
flag the tool *does* have, that the profile is silent about, whose default is subject data. The
purity checker compares values that are present; it cannot see values that are absent. Both
instruments are blind in the same direction, and the kickoff's standing rule points straight at
it: *"arm any subject-calibrated threshold on the galleon from character-derived numbers…
derive per subject or suspend and report."* **Suspending in prose does not disarm.**

This does **not** block the twins — `restylize_views` takes zero values from either profile and
its recipe defaults are byte-identical to the pair's anchor (seed 770700 / 20 / 2.5 / 0.92 /
0.9 / 0.75), which is recorded in the twin-prompts file. It blocks **projection**.

## Finding C — the ship's prep bake does not exist, so the H4 ceiling cannot be computed

`E04_shipprep/` contains exactly one file: `prep_uv.glb` (39.9 MB, 2026-08-04 18:24). A
`find` for `meta.json` and `pos.npy` anywhere under `facet_next/` returns **nothing**.

`project_twins.py:160–164` requires `meta.json`, `pos.npy`, `nor.npy` and `mask.npy`.
`e08_ceiling.py:42–52` requires the same four. So:

- **The H4 reach ceiling cannot be computed.** The spec: *"Compute and pre-register the reach
  ceiling (H4) **before** the atlas is read."* I tried; the tool stops on the missing
  `meta.json`. It is not a tool defect — the inputs have never been baked.
- **`project_twins` cannot run at all**, independently of Findings A and B.

Producing them means running `bake_hero_prep.py`, which is Finding B's first row: no ship block,
and its `--crop` / `--head-scale` pair is the `allocation` decision the advisor deliberately
suspended. `--no-head-scale` exists as a flag, and the advisor's own record lists it among the
founding session's wrong calls — so which way it goes on a ship is not a thing I should pick.

Worth stating plainly: **this was always going to need a ruling before projection.** Finding A
is the only thing gating the *twins*; B and C gate what comes after them either way.

---

## What is built and clean, so the batch is one command

All produced this leg, all from the ratified profile with no explicit framing flags:

| artifact | where | state |
|---|---|---|
| 8 clay renders, 1066 × 1024, width-fit | `E04_armT/clay/galleonclay_{0..7}.png` | profile-only |
| 8 exact raycast silhouettes | `E04_armT/masks/` | 18.14% / 26.61% / 29.20% / 29.43% of frame |
| 8 control images + figure masks | `E04_armT/controls/` | `restylize_views --emit-only`, canny + morphological contour off the exact silhouette; figure-mask shares match the silhouettes exactly (26.6 / 29.4 / 18.1 / 29.2) |
| per-view prompts | `docs/experiments/E04-twin-prompts.json` | ratified Ruling 13 |
| palette fixture | `canon/E04-galleon-palette.json` | ratified Ruling 13 |
| **predictions, blind** | `docs/experiments/E04-armT-predictions.md` | committed `b8245a7`, sha256 `9aebbfbb…`, **before any twin of this ship exists** |

Control-image sizes, recorded because they are the first ship numbers of their kind and a later
run should be able to notice a change: canny 23,056–51,501 px, contour 12,822–60,049 px, total
30,396–85,034 px. The two beam views (0, 4) carry the most contour, the two end-on views (2, 6)
the least — which is the silhouette-area ordering, as expected.

## The three questions

1. **View 5's 2 px** — same adjudication as view 1's, or its own investigation? All three
   differing pixels across the eight views are on the boundary, scattered, centroid unmoved,
   bboxes identical. **This is the only thing gating the eight twins.**
2. **Does `ship.json` gain explicit blocks for the suspended acceptance family, or does the run
   pass them on the command line, or does the loader learn to refuse a silent fallback?** As it
   stands `project_twins` on the galleon would arm W3's 0.80 IoU halt and W3's `edge-ref 700.0`
   while `ship.json` says both are suspended. `texpass_brush` would ask the cloud for a bald
   warrior with a red beard.
3. **The prep bake, and with it the `allocation` decision.** No ceiling, no projection, until
   `bake_hero_prep` runs — and its `--crop` / `--head-scale` are the suspended allocation.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every gate result is the pre-stated instrument's own stdout; predictions committed blind before the artifacts they judge; all eight framing digits from one invocation of one tool differing only in `--views` |
| ANDON_AUTHORITY | **3** | Three gates passed and were reported as passing; a fourth measurement fired and was reported and halted on, not adjudicated. Finding B is an ANDON that **does not exist** and is reported as a gap rather than worked around |
| NAMED_COMPENSATORS | **3** | No spend, no generation, no projection, no profile edit. Every write is a new file under `E04_armT/` or `docs/`. Undo = delete them |
| DECOMPOSE_BY_SECRETS | **3** | Finding B is that standard measured: the profile boundary holds for values that are present and is silent for values that are absent, and silence resolves to the other subject's data |
| UNCERTAINTY_GATED_HUMANS | **3** | Three questions, each with its consequence and none with a recommendation where the answer changes what the arm measures; the one gating question is named as the only one gating the twins |
| EXTERNAL_VERIFIER | **2** | The framing check compares two independent implementations of one camera convention and cannot pass by agreeing with itself; Finding B was found by diffing two profiles against the tools' own argument tables, not by reading either profile's prose. `skip:` on a second model |
