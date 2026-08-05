# E04 Arm G7 — report: one word, one generation, measured

**Executor session, 2026-08-04.** Predictions in
[E04-g7-predictions.md](E04-g7-predictions.md), committed at `52a887e`
(sha256 `16b781c2…`) **before the AFTER image existed** and before any measurement for this
arm had been run. Blind: yes.

**The headline, stated in the form the spec asked for:** under the pre-registered reading
**red did not arrive above the pair's measured element floor** — the cluster instrument moves
from ΔE 34.3 to 28.3 and stays `NEAR`. Under the eye and the change map, **red arrived on the
gun-port lids and nowhere else**: three-to-four lid squares rotate from ochre-gold to red
(h 66–70 → 41–45, C\* rising) at ΔE 16.5–27.3, against a whole-ship median of **0.87** — below
the documented no-response floor of 1.07. The response is real, it is on the named element, and
it is **an order of magnitude below the floor the pass reading requires**, because the lids are
~0.4% of the silhouette. That third outcome is not one of the spec's two branches; both of its
branches prescribe the same next action, so nothing here blocks Arm T.

---

## 1. The generation — byte-match proven, not asserted

| | |
|---|---|
| workflow saved before submission | `E04_g7/workflow_7_G7_headnoun.json` |
| prompt_id | `5df5ab72-5019-409d-96bb-7721a2fd0cb1` |
| credits | **0** (`estimate_credits`: no paid API nodes) · `dry_run` validated first |
| output | `E04_g7/g7_after_7_bow_three_quarter.png`, sha256 `D804D658…` |
| re-rolls used | **0** |

**The only two fields that differ from `workflow_7_bow_three_quarter.json`**, enumerated by
comparing every node input rather than by inspection:

- node 7 `CLIPTextEncode.text` — `red-lined gun port lids` → `red gun port lids`, 6 characters
  shorter, every other token identical including `a verdigris copper spire on the stern turret`
  (G6's Director amendment is canon for the twins; changing it here would have made this a
  two-variable arm);
- node 15 `SaveImage.filename_prefix` — a terminal node with no downstream consumer, so it
  enters no conditioning, latent or sampler.

**The control and init images are byte-identical to the pair's, and this is measured.** Comfy
Cloud's input store is content-addressed: re-uploading the local `clay_7.png` and
`clay_7_control.png` returned
`fcca48b27c0dc5c1e634069475b2ac1a5b65bbcad720b92aeb03aac02b5436e4.png` and
`c8c4df338c09aa0d142c473d013aac50dfdfe280455ef81baba0846ad9bbb866.png` — **the exact filenames
already written in the pair's saved workflow**. Seed 770700, steps 20, cfg 2.5, denoise 0.92,
ControlNet 0.9, shift 3.1, euler/simple, LoRA `…saltroad_style_v2_lowlr_000001500` @ 0.75 all
unchanged.

**A validator gap, reported because it nearly cost a run:** my first `dry_run` payload was
retyped by hand and contained `VAEDecode.samples = ["14", 0]` — a node linking to itself.
Pre-flight returned `status: validated`. The submitted graph was read from the saved file and
checked for self-links and dangling targets in code first; the retyped one was discarded. **A
dry_run PASS does not prove link sanity.**

## 2. The pre-registered instrument — `e04_bands.py`'s machinery, per image

Same k (14), same seed (770700), same chroma floor (C\* 12.0), same inherited verdicts
(LANDED ≤ 25 / NEAR ≤ 40), clustering only the 318,578 px inside the exact raycast silhouette.
Single-view on both sides, because a shared cluster space would let one image's colours define
the other's bins.

| | BEFORE `red-lined` | AFTER `red` |
|---|---|---|
| **G7 ΔE to nearest cluster** | **34.3 NEAR** | **28.3 NEAR** |
| G7's nearest cluster | rgb(95,62,18) C\* 32.9 **h 71.1** | rgb(121,74,19) C\* 41.3 **h 65.3** |
| that cluster's share | 7.75% | 2.48% |
| element floor (smallest share carrying a LANDED element) | **1.42%** | 1.26% |
| the other eleven elements | **all LANDED** | **all LANDED** |

G7's expected hue is ~28. The nearest cluster moved 6.0 ΔE and 5.8° toward it and stopped a
long way short. **No cluster in AFTER is red.** The k-means is doing what it is built to do:
over 318,578 px at k = 14, the smallest resolvable class is ~1.3k px and a four-lid feature of
~1.4k px sits at that limit, sharing bins with the hull it is painted on.

## 3. The pre-registered secondary — and my window was mis-specified

Pixels with C\* ≥ 12 and hue in [350°,360°) ∪ [0°,50°):

| | BEFORE | AFTER |
|---|---|---|
| total | 5,022 px (1.576%) | 7,068 px (2.219%) |
| components / largest CC | 660 / 904 px | 754 / 1,133 px |

**I set that window's 50° edge from the pair's measured *warm-band* lower edge (62°) minus the
band convention's 10° — a cluster statistic — and then applied it to *pixels*.** The ship's dark
tarred wood sits at hue 40–50 with C\* just over the floor, so the window was never measuring
red; it was measuring warm-and-above-the-floor. The numerator's own breakdown, from the same
unmoved window, shows it:

| hue bin | BEFORE | AFTER |
|---|---|---|
| 350–360 | 0 | 0 |
| 0–10 | 0 | 0 |
| 10–20 | 0 | 0 |
| 20–30 | 5 | **26** |
| 30–40 | 347 | **1,143** |
| 40–50 (the tar) | 4,670 | 5,899 |

**Below 40° — the part of the window that is actually red-leaning — 352 px → 1,169 px, a 3.3×
rise on a window fixed before the run.** That is the non-circular arrival number: 0.37% of the
silhouette. This is the fourth member of this repo's *check what your denominator is made of*
family and the first where I built the instrument myself an hour before it ran.

## 4. Where the word landed — post-hoc localisation, declared as such

`e04_g7_where.py`, ΔE > 10 components, threshold **descriptive: it selects what to print and
gates nothing**. Selecting components by change magnitude makes their own ΔE circular as a
discriminator; what is not circular is *which structures* the largest hue-toward-red movements
sit on, and what they were before.

| rank | px | bbox (x,y w×h) | BEFORE → AFTER | h | C\* | ΔE |
|---|---|---|---|---|---|---|
| 3 | 632 | 602,757 29×29 | rgb(131,79,23) → **rgb(134,35,19)** | 70.2 → **43.8** | 43.2 → 48.1 | 25.8 |
| 4 | 500 | 738,758 29×22 | rgb(125,77,24) → **rgb(120,37,20)** | 69.5 → **41.1** | 41.8 → 45.5 | 27.3 |
| 6 | 267 | 484,770 26×15 | rgb(68,40,14) → **rgb(95,32,15)** | 66.6 → **44.9** | 22.4 → 34.3 | 16.5 |
| 1 | 1,931 | 217,370 141×224 | rgb(196,193,190) → rgb(155,145,135) | 85.4 → 76.7 | 2.0 → 7.4 | 17.5 |
| 2 | 769 | 352,278 57×92 | rgb(191,189,186) → rgb(150,140,128) | 90.0 → 77.5 | 2.3 → 7.8 | 17.6 |
| 5 | 295 | 834,735 14×24 | rgb(199,179,99) → rgb(208,204,184) | 94.0 → 95.6 | 41.5 → **10.5** | 29.4 |

Ranks 3, 4 and 6 are gun-port lids on the upper row: **ochre-gold in, red out, chroma up.**
Ranks 1 and 2 are foresail canvas going a little darker and warmer at chroma 2 — where hue is
not a colour. Rank 5 is on the stern spire, gold losing chroma 41.5 → 10.5.

**Total change over ΔE 10: 5,913 px = 1.86% of the silhouette, in 266 components.**

## 5. What one word did to the rest of the ship

| | |
|---|---|
| median ΔE inside the silhouette | **0.87** |
| median ΔE outside the AFTER red window | **0.87** |
| mean / p90 | 1.61 / 2.95 |
| E08 contradiction, eight phrases changed, held-region median | 6.23 |
| N11 no-response floor | 1.07 |

The median sits **below the no-response floor** while three lid components sit at 16–27. The
ship did not repaint; four squares did.

## 6. A consequence for Arm T, measured while the instrument was open

The 4d bands (warm 50–100 proposed, blue 273–301 suspended) applied per-pixel above C\* 12 —
the palette gate's own arithmetic:

| | off-band px | % of silhouette | components | largest CC |
|---|---|---|---|---|
| BEFORE (**the Director-ratified canon target**) | 5,168 | 1.622% | 705 | 904 |
| AFTER | 7,243 | 2.274% | 796 | 1,133 |

Two things fall out and neither is mine to rule on. **The ratified canon pair itself carries
1.62% off-band material** under its own derived bands — the largest component in both images is
a dark hull shadow at h 45.9 / C\* 13.1, not a garment. And **the arrived red sits at h 41–45,
outside the warm band's 50 edge** — G7 is a declared element whose realised colour has no band,
because the bands were derived from an image in which G7 had not landed.

## 7. Predictions, scored

| # | prediction | outcome |
|---|---|---|
| P1 | red arrives, cluster ΔE ≤ 25 | **FALSE** — 28.3 |
| P2 | red cluster's share in [1.0%, 6.0%] | **not evaluable** — no red cluster formed. The nearest cluster's 2.48% is inside the interval but it is not red |
| P3 | clears the 1.56% element floor | **FALSE** — measured red is 0.37% (hue < 40) to 0.44% (lid components) |
| P4 | red centroid below the silhouette midpoint | **TRUE but weak** — 779.7 against a midpoint of 511.5, on a window I have just shown is dominated by tar |
| P5 | median ΔE outside the red set < 6.23 | **TRUE** — 0.87, and below the 1.07 no-response floor |
| P6 | BEFORE < 500 px, AFTER > 3,000 px | **FALSE / TRUE-for-the-wrong-reason** — 5,022 and 7,068, both dominated by hue-40–50 tar |
| P7 | no element knocked out | **TRUE** — eleven of twelve LANDED on both sides, G7 NEAR on both |

Two clean, one weak, two false, two unevaluable. **P1 and P3 are the arm's own predictions and
both failed**; the mechanism I predicted would produce a landing produced a response instead.

## 8. Artifacts

- `E04_g7/G7_ZOOM_sheet.png` — **BEFORE | AFTER | change map** on the gun-port band, 3× —
  the panel that shows the result. Four squares gold → red, and the change map lighting up on
  those squares alone.
- `E04_g7/G7_FULL_sheet.png` — the same three panels at 1:1 on the whole frame.
- `E04_g7/g7_landing.json`, `g7_where.json`, `red_mask_{before,after}.npy`, `g7_change_dE.npy`
- `tools/diagnostics/e04_g7_landing.py`, `e04_g7_where.py`, `e04_g7_sheet.py`

## 9. What this does not establish

It does not establish that grammar is the lever. One generation on one subject, and the
mechanism's prediction was *landing*, which did not happen. The alternates the spec named are
untouched by this run: **size** is now the leading one on the evidence — the response is
exactly where the phrase points and is bounded by how much of the frame the lids occupy.
Whether an element too small to clear the floor should be read as confirmation, refutation, or
neither, is the advisor's call and the fixture's amendment is the Director's.

It does not establish anything about the twins. Per the spec, **the twins run with the
head-noun form regardless** — that is the same action under both pre-registered branches — and
Arm T proceeds.

## 10. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Workflow saved before submission; both inputs proven byte-identical by content-addressed filenames matching the pair's; every threshold inherited from `e04_bands.py` or derived from data predating the arm; seeds fixed and echoed |
| ANDON_AUTHORITY | **2** | No gate fired and none is claimed to have passed. The pre-registered reading is reported as failed rather than re-cut; the mis-specified window is reported as mis-specified rather than replaced |
| NAMED_COMPENSATORS | **3** | 0 credits, one generation, one re-roll allowance unused. All writes are new files. Undo = delete `E04_g7/` |
| DECOMPOSE_BY_SECRETS | **3** | Every subject value came from the fixture and `ship.json`; no shared-tool constant was touched. The three new scripts are diagnostics, outside the route |
| UNCERTAINTY_GATED_HUMANS | **3** | The sheet is built at the Director's zoom before the metrics are written up; placement is handed to his eye explicitly because the instrument measures colour and not placement; the fixture amendment is left to him |
| EXTERNAL_VERIFIER | **1** | `skip:` — deterministic measurement. The instrument can fail and did: it returned NEAR on an image whose lids are visibly red, and that disagreement is the report's headline rather than a footnote |
