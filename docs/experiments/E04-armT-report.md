# E04 Arm T — the twin baseline. Eight twins measured. HALT for the ruling.

**Executor session, 2026-08-04, after Ruling 16.** The chain that had been open for three
sessions is closed: the tolerance landed, **the bake completed**, **the H4 ceiling is
pre-registered**, the frame regenerated at 1072, **the twins came back at the right size**, and
the full baseline is measured. **Nothing has been projected.** This is the spec's twin-baseline
halt.

Predictions committed blind at `b8245a7` before any twin of this ship existed. Two rows —
G7-landed and masthead-gold — were **demoted to declared priors** by Ruling 15 because I
observed them on the 1064 batch; they are scored as priors below, not as blind hits.

---

## The frame ruling worked

| | |
|---|---|
| twins returned | **1072 × 1024, all eight** — matching their masks exactly |
| the 1064 defect | gone. `1072 = 16 × 67`; the VAE had nothing to round |
| batch | 8/8 ready, **0 failed, 0 credits, 0 re-rolls** |
| workflows | saved before submission, link-checked in code; 16 upload names asserted distinct and disjoint |

## Bake and ceiling receipts

**Bake:** guard passed at **1.225e-07 relative against the ruled 1.0e-06**;
`meta.json`/`pos.npy`/`nor.npy`/`mask.npy`/`prep_uv.glb` written at res 4096, `head_scale 1.0`,
uniform atlas, `head_uv_area_share 0.24318870902061462`.

**H4 ceiling, pre-registered** ([E04-h4-ceiling.md](E04-h4-ceiling.md), committed before the
batch): **42.72%** of valid texels — 1,329,359 of 3,111,832 — is the most stage 1 can reach
from the eight twin cameras at the ruled facing floor. The character's reach is 74.1%. **Stage-1
share must be read against 42.72%, not 100%.**

## ⚠ An instrument error of mine, caught before the number was believed

My first registration pass reported **IoU 0.632** on the broadside views. That was **my
morphology, not the ship**: I had run `binary_fill_holes` on the keyed figure, and a rigged
ship is *porous* — fill_holes swallows every patch of background enclosed by shrouds, ratlines
and yards, giving 464,282 px of "figure" against a 293,865 px silhouette, **+58%**.

Checked on all eight views before reporting:

| figure definition | IoU range |
|---|---|
| raw key (adopted) | **0.8442 – 0.9565** |
| + closing | 0.8434 – 0.9604 (moves < 0.005; dropped) |
| + fill_holes | 0.6320 – 0.9389 ← the artifact |

The tool now uses the raw key with the reason written beside it. **A collapse that large on
two views and not the other six is a shape story, and shape stories deserve an operand check.**

## REGISTRATION — reportable now that the frame matches

| view | sil px | twin px | **IoU** | centroid dx, dy | bbox sil → twin |
|---|---|---|---|---|---|
| 0 broadside | 293,865 | 328,463 | **0.84420** | −6.73, −12.53 | 890×856 → 891×862 |
| 1 | 325,009 | 338,436 | **0.92565** | +1.68, −2.59 | 721×856 → 723×863 |
| 2 stern-on | 200,391 | 204,249 | **0.95297** | +0.14, −1.43 | 456×856 → 457×860 |
| 3 | 322,680 | 335,957 | **0.91588** | −1.61, −5.62 | 721×856 → 723×860 |
| 4 broadside | 293,865 | 330,229 | **0.86276** | +6.23, −11.32 | 890×856 → 893×859 |
| 5 | 325,009 | 340,858 | **0.92953** | −0.02, −4.61 | 721×856 → 723×860 |
| 6 bow-on | 200,391 | 204,327 | **0.95649** | +0.06, −1.13 | 456×856 → 457×860 |
| 7 | 322,680 | 339,518 | **0.92990** | −1.11, −4.33 | 721×856 → 723×863 |

**Range 0.8442 – 0.9565, against W3's adjudicated 0.8329 – 0.9533.** The halt is suspended
(`reg-iou-min 0.0`), so this is a baseline and not a verdict.

Two structures worth the ruling's eye, neither a judgment:

- **Every centroid dy is negative** (−1.1 to −12.5 px): the painted figure sits systematically
  *above* its silhouette, and the offset scales with how much rigging the view presents.
- **The two broadside views are the worst-registered pair** (0.844, 0.863) and the two end-on
  views the best (0.953, 0.956) — **the exact opposite of prediction T10**, which said the
  end-on views would be worst because they present the least area. They present the least
  *rigging*, and rigging is where the twin over-paints.

## LANDING, RED, WATCH — no bound anywhere

| view | landed/12 | G7 ΔE | G7 | red < 40° px | key margin % | thin/bulk key-out % | enrichment |
|---|---|---|---|---|---|---|---|
| 0 | **11** | **21.6** | **LANDED** | **6,438** | 3.059 | 4.91 / 2.72 | 1.81× |
| 1 | 10 | 30.6 | NEAR | 953 | 1.875 | 5.71 / 1.58 | 3.61× |
| 2 | **11** | **22.0** | **LANDED** | **8,433** | 1.469 | 8.74 / 1.10 | 7.95× |
| 3 | 10 | 31.3 | NEAR | 1,134 | 2.423 | 7.66 / 2.02 | 3.79× |
| 4 | 10 | 34.4 | NEAR | **55** | 1.636 | 7.05 / 0.66 | 10.68× |
| 5 | 10 | 33.8 | NEAR | 1,378 | 1.303 | 5.72 / 0.96 | 5.96× |
| 6 | 10 | 33.9 | NEAR | 246 | 1.264 | 11.98 / 0.71 | 16.87× |
| 7 | 10 | 32.0 | NEAR | 1,807 | 1.118 | 4.95 / 0.82 | 6.04× |

**G7 lands on two views of eight** — the port broadside and the stern-on — at ΔE 21.6 and 22.0,
against the pair's 34.7 and Arm G7's 28.3. And the asymmetry is the striking number:
**view 0 (port broadside) carries 6,438 sub-40° red pixels; view 4 (starboard broadside)
carries 55.** Same ship, mirrored camera, same prompt, same seed. That is the per-view-roll
signature E08's blue sleeve had, with an element that is *supposed* to be there.

**Thin enrichment (S2, element G9) reproduces and then some:** 3.6× to 16.9× on seven of eight
views, median ~6×, against W3's 4.2–6.8×. The one exception is view 0 at 1.81×, which is also
the view with the highest bulk key-out (2.72%).

**Key margin 1.118% – 3.059%**, against the ratified pair's 1.48% and the accepted character's
1.77–2.45%.

## ⚠ Ruling 8's banked watch item is live

The pale near-neutral cluster — below the chroma floor, invisible to the palette gate:

| view | rgb | share % | max-channel distance to the realised backdrop |
|---|---|---|---|
| 0 | (176,173,167) | 6.38 | 0.0627 |
| 1 | (168,165,159) | 4.43 | 0.0706 |
| 2 | (156,148,141) | 4.31 | 0.1098 |
| **3** | (173,171,168) | 4.59 | **0.0471** |
| 4 | (173,169,162) | 5.00 | 0.0941 |
| 5 | (164,159,156) | 4.17 | 0.0902 |
| 6 | (157,151,146) | 3.41 | 0.0902 |
| 7 | (162,159,149) | 3.69 | 0.1020 |

**The key cut is 0.06.** View 3's pale cluster sits at **0.0471 — under the cut** — and view 0's
at 0.0627, just over. On those views a pale-painted region is at or inside the keying
threshold, which is exactly the failure Ruling 8 banked this cluster to watch for. Reported;
not acted on.

## PALETTE GATE — both bounds null, shipped instrument, exact silhouettes

Blue allowed. **All eight "within the declared palette"** under the vacuous blob bound, which
is a statement about a bound that cannot fire, not about the twins — read the numerators:

| view | figure px | off-palette | % | largest CC | dominant off-palette |
|---|---|---|---|---|---|
| 0 | 293,865 | 12,136 | 4.13% | 4,562 | — |
| 3 | 322,680 | 3,302 | 1.02% | 618 | h 40–50 (44%), rgb(97,43,31) |
| 4 | 293,865 | 448 | 0.15% | 132 | h 40–50 (82%), rgb(48,25,17) |
| 5 | 325,009 | 2,168 | 0.67% | 528 | h 30–40 (52%), rgb(81,24,16) |
| 6 | 200,391 | 3,202 | 1.60% | 362 | h 40–50 (92%), rgb(43,19,5) |
| 7 | 322,680 | 5,613 | 1.74% | 2,002 | h 260–270 (29%), rgb(58,28,19) |

**View 0 is the outlier: 4.13% with a 4,562 px largest component.** For scale, E08's *invented
navy sleeve* measured 6.17% with a 4,882 px blob — and view 0 is also the view carrying 6,438
px of newly-arrived red. Whether that component **is** the red gun-port lids sitting outside a
warm band derived from an image where G7 had not landed — the gap the palette fixture already
records as *"G7 has no band"* — is the question, and it is not mine to answer.

## Predictions, scored

| # | prediction | outcome |
|---|---|---|
| T1 | median landed ≥ 11 of 12 | **FALSE** — median 10; landed 11 on two views, 10 on six |
| T2 | G7 clears ΔE ≤ 25 on ≥ 5 of 8 | **FALSE** — 2 of 8. I said I expected to lose this one |
| T3 | red > 500 px on views 0,1,4,5,7 and < 500 on 2,6 | **FALSE, and inverted** — view 2 has the *most* red (8,433) and view 4 the least (55) |
| T4 | off-band share in [0.8%, 3.5%] on the median view | **TRUE** — median 1.67% |
| T5 | largest off-band CC < 2,000 px on all eight | **FALSE** — view 0 at 4,562, view 7 at 2,002 |
| T6 | IoU ≥ 0.90 on all eight | **FALSE** — 0.844 and 0.863 on the broadsides; 6 of 8 clear it |
| T7 | key margin < 1.77% on every view | **FALSE** — views 0 (3.06%) and 3 (2.42%) exceed it; 6 of 8 clear it |
| T8 | thin enrichment ≥ 3× on the median view | **TRUE** — median ~6× |
| T9 | the pale cluster sets the tightest margin | **TRUE**, and tighter than expected — under the cut on view 3 |
| T10 | views 2 and 6 are the worst-registered pair | **FALSE, and inverted** — they are the *best* |
| prior | G7 lands (declared, from the 1064 batch) | holds on 2 of 8 views |
| prior | masthead gold (declared) | not re-measured; placement is the Director's |

**Three of ten clean, two inverted.** T3 and T10 were not merely wrong but backwards, and both
were wrong for the same reason: **I reasoned from projected area and the subject answers by
rigging.** Rigging is where the twin over-paints, where thin structure keys out, and — on the
end-on views — where there is least of it.

## What is NOT in this report

No projection, no atlas, no stage-1 share. No verdict on any number: every gate this arm could
carry is suspended by the spec and by `ship.json`, and the one rejection rule that needs no
baseline — material not in the spec — has no trigger here, since nothing arrived that the
fixture does not name.

## Artifacts

`E04_armT72/twins/twin_{0..7}.png` · `workflows/` · `clay/` · `masks/` · `controls/` ·
`twin_baseline.json` · `palette_blue_allowed.json` · `ceiling/` ·
`tools/diagnostics/e04_twin_baseline.py`

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Workflows saved before submission and link-checked; upload names asserted distinct; ceiling committed before the batch; every threshold inherited or ruled |
| ANDON_AUTHORITY | **3** | The bake guard and the frame anchor both ran as ruled; the arm halts here for the ruling rather than projecting; no bound was invented for any suspended gate |
| NAMED_COMPENSATORS | **3** | 0 credits, 0 re-rolls of the 1 allowed; the 1064 batch preserved as the frame-discovery record; all writes new files |
| DECOMPOSE_BY_SECRETS | **3** | Every subject value came from `ship.json` or the fixture; the two shared-code edits this arc needed are both ruled Finding-1-class and both recorded |
| UNCERTAINTY_GATED_HUMANS | **3** | Ten predictions scored including five failures and two inversions; the view-0 off-palette component is posed as a question rather than classified |
| EXTERNAL_VERIFIER | **2** | The registration artifact was caught by comparing three independent figure definitions against the same geometry — the instrument disagreeing with itself is what surfaced it. `skip:` on a second model |
