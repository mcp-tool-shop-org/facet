# E12 handoff 13 — A2's arithmetic, the head-crop twins, and stage 1

**Executor session, 2026-08-06.** Predictions registered blind in `3d0347d`
([E12-handoff13-predictions.md](E12-handoff13-predictions.md)), git blob `d2b102fa`, written
before A2's arithmetic ran, before a crop frame existed, before either projection ran and
before `project_twins.py` was touched. Blind status was disclosed **per item** in that file —
BLIND / DERIVED / CODE-READ — and the scorecard below keeps the labels.

**0 credits. 3 generations** — two crop twins plus one bounded re-roll. Every job `succeeded`,
zero warnings. Watchdog alive throughout (1,894–1,899 MiB against the 31,200 ceiling).

**Three results carry this report.**

1. **A2's condition fires and the arm is DECLINED, on a collision registered before the
   number existed.** The atlas under-resolves the crop paint by **11.07×**. It also
   under-resolves the *full-figure* paint on the same region, by 1.23× — which the rule did
   not anticipate. And the lever the rule reaches for is not a head lever on this subject:
   `bake_hero_prep` has no head region, only W3's front-view rect, which contains the head box
   entirely and is **4.3× larger than it**.
2. **Two defects in `project_twins` found by reading it before running it, both registered as
   predictions, both fixed and both anchored at 0 differing pixels.** It had **no
   frame-bounds test** — and the crop cameras went on to reject **360,378 and 323,888**
   candidate texels as off-frame, every one of which would otherwise have been sampled at the
   frame border and, tied on facing and processed first, would have **won**. And its frame was
   derived height-fit on a subject that renders width-fit.
3. **Stage 1 ran three times and reach never moved.** 1,635,304 / 3,240,510 = **50.46%** on
   every run. A0 styles **87.5%** of it, A1 **88.6%**, and A1 is **strictly additive** —
   gained 18,060, **lost 0**.

**Look at these before the numbers:** `E13_stage1/sheets/HEAD_y0_3x.png` and `HEAD_y45_3x.png`
(clay | A0 | A1 | provenance, one camera, one crop, one scale — H3's artifact) ·
`E13_twins/gate/crops_residual/CROP1_red_frill_2x.png` (the flagged mass) ·
`E13_stage1/sheets/FULL_A0_A1_y0.png`.

---

## 1. Task 1 — A2's arithmetic, and the decision printed beside it

Full record: [`E13_twins/a2/DECISION.md`](../../../training/facet_next/E13_twins/a2/DECISION.md)
and `allocation.json`. The instrument is a committed tool
([`e13_a2_allocation.py`](../../tools/diagnostics/e13_a2_allocation.py)).

The unit, chosen so neither side can be moved by reframing: **atlas texels per frame pixel over
the same patch of head-box surface** — head-box texels first-hit visible from the camera, over
frame pixels whose first hit lands in that box.

| | yaw 0 | yaw 45 |
|---|---|---|
| head-box texels, first-hit visible | 31,265 | 39,051 |
| **crop** frame px on head (1360², ortho 0.305005) | 346,184 | 431,309 |
| **texels per CROP pixel** | **0.0903** | **0.0905** |
| **route** frame px on head (1792×1024) | 38,365 | 47,834 |
| **texels per ROUTE pixel** | **0.8149** | **0.8164** |

**P1a and P1b held; P1c is falsified and it is the more useful of the two.** I predicted the
route-frame counterpart at 0.9–1.9, centre 1.26 — i.e. that the atlas was roughly matched to
the route frame and the *generation* frame was the whole bottleneck. Measured 0.815: the 4096
bake under-resolves this head region **at both frames**. Allocation and generation-frame are
not alternatives here; the first is a live constraint before the second is applied.

### The decision: DECLINE. Nothing re-baked, no profile touched.

`bake_hero_prep` scales every UV island holding a face whose centroid projects into `--crop`,
a front-view pixel rect. The profile pins W3's `360,240,700,600` and records that it is *"inert
at head-scale 1.0… no beast meaning is claimed for it."* Measured at texel level:

| | texels | |
|---|---|---|
| inside the measured head box | 316,385 | 9.763% of valid |
| inside W3's rect (before island expansion) | 1,358,656 | 41.927% |
| head box **not** in the rect | **0** | the rect *contains* the head |
| rect **not** head box | **1,042,271** | **76.7% of what the lever would scale** |

After island expansion the recorded bake measured the selected set at **51.79% of UV area /
55.00% of faces** (`prep.log`) against the head box's **10.497% of faces**. Projected from that
recorded pre-scale share, the cap buys the head **×1.566** against an **11.07×** shortfall while
cutting the other 45% of the mesh to **×0.392** — and the bake's growth ANDON (`share_area >
0.6215`) **passes at every scale**, so the expressibility halt the dispatch named as the safety
would not have fired. P1f is therefore computed rather than run, and it says the guard was
never going to catch this.

**P1e held.** The spec's own wording for this arm is *"A2 — texel allocation (measured, then
armed or declined)"*. Measured, declined. What a real allocation arm needs is a beast-derived
rect from `head_00003.json`; writing one is a ruling's act, not an executor's, and E12 Ruling 2
ruled ALLOCATION: NONE on Gate 0 evidence.

## 2. Two defects in the projector, found before running it

Both were registered in the predictions file as CODE-READ items **before** the tool was
touched, and both are additive changes whose defaults are the old literals.

### 2a. There was no frame-bounds test, and it is not a small thing (P4b)

`bilinear` **clamps** x and y into the image (`:351–352`), so a texel projecting *outside* a
view's frame was not rejected — it was sampled at the border. On a full-figure frame this is
inert: the 1.204 margin insets the figure ~8% on both axes, and the anchor re-run measured
**0 off-frame candidates on all eight views**. On a head crop the whole body below the neck
lands on the bottom border row, where the neck's own paint sits; those texels carry the *same*
facing weight as the full twin at that yaw and are processed **first**, so they would win.

| crop view | candidates | **rejected as off-frame** | |
|---|---|---|---|
| yaw 0 | 480,442 | **360,378** | 75.0% |
| yaw 45 | 430,062 | **323,888** | 75.3% |

I predicted 10⁴–10⁵. The measurement is 3.6×10⁵ and 3.2×10⁵ — **direction right, magnitude
under-predicted by about 3×**. Without the test, three quarters of each crop camera's
candidates would have been painted with border content and would have owned it.

### 2b. The framing family was never pinned on this consumer (P4c)

E04 Ruling 25 pinned aspect + fit-axis + margin together on three consumers. `project_twins` is
a fourth: `:229` was `v_ext = (bhi[2] - blo[2]) * 1.204`, the margin a literal and no fit-axis
at all — turn_render's HEIGHT mode written longhand. This subject renders **width**-fit.
Measured against the recorded silhouette masks, which is the check that tests the failure mode:

| frame derivation | figure bbox | px | IoU vs the recorded mask |
|---|---|---|---|
| recorded `silhouette_masks` output, view 0 | 152, 85, 1639, 938 | 520,644 | — |
| **width-fit** (`max(size.x,size.y) × margin`) | **152, 85, 1639, 938** | **520,644** | **1.000000** |
| the tool's own height-fit derivation | 154, 87, 1637, 936 | 517,340 | 0.986006 |

Ratio **1.003313** against a predicted 1.00332. Every sample sat up to 0.33% of its distance
from frame centre too far in — 2 px at the figure's own bbox edge. `--fit-axis` and `--margin`
now exist, defaulting to the old literals, and the profile is **not** edited: A0/A1 pass
`--fit-axis width` explicitly and the value is recorded in `run_stage1.ps1`. Pinning it in the
profile is a ruling's call and is named here as the follow-up.

### E13 Gate 0, re-run, and it re-passes at zero

Against handoff 11's `baseline_HEAD_8cam`, the output of the **unmodified** tool:

| anchor | atlas | `_holes` | `_blend` | `_styled_mask` | `_owner` |
|---|---|---|---|---|---|
| **C** — default path through the changed tool | **0** | **0** | **0** | **0** | **0** |
| **D** — framing family passed explicitly at the old literals **plus** all three crop overrides at full-figure values on all eight views | **0** | **0** | **0** | **0** | **0** |

0 of 50,331,648 elements on each image. Recipe: `E13_gate0/anchor_h13.ps1`.

## 3. Task 2 — the two head-crop twins

Sidecar at birth: `E13_twins/crops/sidecar.json`. Frame **1360×1360 at ortho_scale 0.305005** —
`e12_head_render.py`'s **yaw-invariant** span, not the companion's 0.223104, which was an
explicit single-yaw override and would crop the head at 45°. Measured resolution gain over the
route frame, on head-box first-hit pixels rather than computed from extents: **3.00× linear /
9.02× area** (P2a held).

**These are declared PROJECTION SOURCES** — generated at the route's own yaws, through cameras
the projector expresses and Gate 0 anchors. The handoff-5 companion stays forbidden and was
not used.

### The drops are measured, and the companion's do not transfer (P2g, falsified twice)

The companion dropped `charcoal dorsal and tail spines` because *"the tail is far out of
frame"* — true at its tighter frame, false at this one. Raycast per crop, as a share of that
crop's own figure, against handoff 11's accepted floor (D6's dorsal term at 0.043% on route
view 0, KEPT):

| region | crop0 (yaw 0) | crop1 (yaw 45) |
|---|---|---|
| tail quarter, y > 0.25 | **6,607 px · 0.672%** | 0 px |
| dorsal band | 0 px | 0 px |
| **nape crest** | **120,209 px · 12.231%** | **89,326 px · 7.240%** |
| legs / feet | 0 px | 0 px |

So crop0 **keeps** the dorsal/tail term (15.6× the accepted floor) and crop1 drops it; both drop
`charcoal claws`. Term counts **19** and **18** against my predicted 14–17 — falsified. And the
nape clause is falsified in the interesting direction: I predicted it "enters the yaw-45 crop
and is marginal at yaw 0", and yaw 0 measures **12.231%**, the *higher* of the two. The
dispatch asked for this to be verified rather than assumed, and verifying it is what caught it.

`e12_stem_delta.py` gained `--allow-new-stem KEY`, in the same shape as
`--allow-dropmap-change`: a new stem key is a decision, so it must be **named**; a key that
vanishes is still a halt with no flag. v10 passes with the entry unchanged and all nine
predecessor stems byte-equal.

### What landed, and what the gate found

| | crop0 (yaw 0) | crop1 (yaw 45) | crop1 re-roll (770701) |
|---|---|---|---|
| 16e off-palette | 13.71% | 10.87% | **28.77%** |
| largest residual component | 56,274 px (membrane) | 32,723 px (membrane) | **190,825 px** |
| achromatic % / largest CC | 3.70% / 3,972 | 3.68% / 16,942 | 5.55% / 11,952 |
| **registration IoU** | **0.990920** | **0.994727** | 0.914030 |

**P2b held** — D8 landed **as an eye** on both crops, orange with a dark slit, where the
companion's bust-scale attempt produced a crimson teardrop. **P2c held** — D10's tooth rows
resolve as separate teeth. **P2e held on all three clauses.** **P2d is split**: D5 is present
on both crops, but the second clause is falsified — the crown resolves into separate spikes at
this scale rather than reading merged.

### The flagged mass, the re-roll, and why the re-roll is not adopted (P2h falsified)

crop1 at the operating seed carries **22,420 px of scarlet** — `rgb(107,23,23)`, hue 31,
C\* 42.6 — on the cheek-spike array, a surface D5 declares bone-ivory. That is **4.4× the
largest recorded precedent defect** (5,068 px) and it is the pre-registered rejection ground:
*material not in the spec, on a declared surface*. One bounded re-roll spent at 770701, against
my prediction of zero.

**It did not cure.** The frill went green and **190,825 px of pink-mauve** (hue 319) took the
wing membrane — 8.5× the mass it replaced and 38× the largest precedent. Off-palette nearly
tripled and registration fell to 0.914030 with 66,813 px painted outside the silhouette. Per
CLAUDE.md a second failure **is the result rather than a third roll**, and per the Ruling
21c/23d precedent a re-roll is adopted only when it *cures*. The 770700 artifact stands as the
round's yaw-45 twin, **carrying its flagged frill**, and the re-roll is retained beside it.

My named alternative was wrong too: I predicted that if a re-roll fired it would be "an
off-palette blob at a material boundary". It was a coherent mass on a declared surface.

### A new instrument, because the old one refused to answer (P2f)

`e12_twin_readout` fits its background over a **border ring** — E08's correction to
corner-median keying, and right on a full-figure frame. A crop frame has no such guarantee: the
figure reaches the border on both crops (53.1% of frame touching three edges; 66.7% touching
all four), and the tool's own key-health guard fired and declared its IoU unusable — 94.6% and
67.0% of the frame past the key, twin bbox 1359×1359 against a 1359×1172 mesh. **That guard
working is why there is a new file rather than a quoted number.**

[`e13_crop_registration.py`](../../tools/diagnostics/e13_crop_registration.py) fits the
background on pixels the **geometry** says are clean (≥ 24 px outside the silhouette). Geometry
picks the samples; it does not decide the answer — the key is still a threshold on the image
and is free to disagree with the silhouette anywhere. Registration then reads **0.990920 and
0.994727**, against the companion's 0.993953 precedent. **P2f held.**

The same broken key appears inside `project_twins` (IoU 0.5167 / 0.6779 on the crop views).
Those numbers are against a contaminated key on a crop frame and are **not** the registration
of these twins; the halt is vacuous on this subject by ruling, so nothing fired.

### Harmonization (P2i falsified)

The identity test **ran and passed** — 0 differing px, bytes identical; self-test 0 of
1,835,008. It ran on the second invocation: the tool's ANDON fired first because the reference
had not been passed as an image, so the works-perfectly test had not executed. A check that
cannot fail is not a check, and this one refused to be skipped.

Mean L\* corrections toward reference view 1: crop0 **−3.16**, crop1 **−7.35**. I predicted
|Δ| ≤ 3.0. **Both crops sit above the seven-view 4.4 L\* band**, nearer view 4's −9.24 outlier
than to the band — a head crop is dominated by the lit front of the animal, so it reads
brighter than a full figure at the same yaw.

**Also corrected this session:** handoff 12 harmonized view 3 from its **770700** artifact,
because Ruling 23f had not happened yet. 23f adopted the **770701 cure**, so that artifact was
harmonized here by the same identity-tested transfer (`harmonize/operands_v3r.json`) and it is
what stage 1 consumed. The ruled set was otherwise as 23f states.

## 4. Task 3 — stage 1, three runs

Recipe: `E13_stage1/run_stage1.ps1`. The third run is not in the dispatch and is adopted by
nobody: it measures §2b's cost instead of asserting it.

| run | frame | styled | styled / valid | **styled / REACHABLE** | holes |
|---|---|---|---|---|---|
| **A0** baseline | width-fit | 1,430,687 | 44.2% | **87.5%** | 1,809,823 |
| **A1** crop pass | width-fit | 1,448,747 | 44.7% | **88.6%** | 1,791,763 |
| A0L historical | height-fit | 1,432,302 | 44.2% | 87.6% | 1,808,208 |

**The reach-invariance check passes.** `reachable` is **1,635,304 / 3,240,510 = 50.46%** on all
three runs, and the ceiling instrument re-run independently reproduces 1,635,304 at the
profile's ruled floors. **P3a held.**

*One error of mine on the way there, worth recording:* my first ceiling re-run returned 52.72%
and looked like a halt. It was not — I had run the tool at its **default** `--head-facing-min
0.18`, which is W3's value, where the banked number used the profile's ruled **0.45** (Ruling 2,
allocation NONE). Same tool, same prep, wrong argument. Checking the baseline before declaring
the halt is the only reason this is a footnote instead of a false halt.

**P3b held** — 87.5% styled/reachable inside my 78–88%, 44.2% styled/valid inside 39–45%. Both
land at the *top* of their bands: I reasoned this subject would run below the ship's 86.4% and
the character's 92.8% because its mass is thin structure, and it runs between them.

**P3c held, and the swap law does not bite.** A1 − A0 = **+1.1 points**, inside −0.5…+1.5.
CLAUDE.md says characterise what left before banking a net — **nothing left**:

```
A1 vs A0:  gained 18,060   lost 0   net +18,060
```

The eight full views' per-view accepted counts are **identical** between A0 and A1
(370,108 / 340,609 / 214,320 / 319,833 / 375,038 / 332,844 / 228,572 / 348,424). The gain is
mechanism, not luck: erosion is `min(edge_dist × fig_w/edge_ref, ⅓ × local half-width)` in
**frame pixels**, and a crop frame carries ~3× the linear resolution, so the same rule peels
about a third as much *in world terms*. The newly-admitted crop texels are clean against the
twin's own background — 0.11% and 0.48% within ΔE 10, against already-trusted 0.11% / 0.13%.

### Who owns what (P3d held; the part I did not predict is the interesting one)

| owner | texels | in the head box |
|---|---|---|
| **CROP yaw 0** | 39,440 | 9,416 |
| **CROP yaw 45** | 56,801 | 16,695 |
| **crop total** | **96,241** (6.64% of A1 styled) | **26,111** |
| full yaw 0 / 45 (were the head's main owners in A0) | 191,139 / 152,355 | 1,489 / 6,009 |
| full yaw 90 / 180 / 270 / 315 | 118,324 / 213,064 / 127,297 / 202,765 | 17,102 / 14,987 / 17,938 / 20,875 |

96,241 is inside my predicted 40,000–160,000. What I did not predict: **only 26,111 of them are
in the head box** — 24.2% of the crop-owned set, and 24.2% of the head box's 107,675 styled
texels. Two reasons, both measurable: the crop frame at the yaw-invariant span is much wider
than the head box (29.5% / 47.7% of each crop's figure lies outside it in x), and the head is
seen from **all eight** yaws, four of which own more head-box texels than either crop does.

**Head-box coverage barely moves** — A0 106,849 → A1 107,675, **+826**. A1 changed *who owns*
the head, not how much of it is painted. 78,181 texels styled in both runs changed owner.

**A0L vs A0**: +1,615 texels, symmetric difference 26,737 (0.8% of the styled set). The framing
defect is nearly free in *coverage*, which is the point worth stating carefully — coverage
cannot see a registration displacement, so 0.8% is a floor on its cost, not a measure of it.

### The judging artifact

`E13_stage1/sheets/HEAD_y0_{2x,3x}.png` and `HEAD_y45_{2x,3x}.png` — **clay | A0 | A1 |
provenance**, all four at the route camera, cropped to the same rect derived from the measured
head box by the route's own arithmetic, at the Director's zoom. Rendering the clay at the crop
camera and the atlas at the route camera would have put two framings in one sheet and invited
the eye to compare framing instead of paint.

Every texture panel is **FLAT** (`texpass_iter emit`, a raycast of the atlas with no lighting).
The provenance panel is magenta where a crop twin owns the texel, grey where a full-figure twin
does, near-black where nothing painted it. Full-figure flat renders of both runs at five yaws
are `sheets/FULL_A0_A1_y*.png`; the framing pair is `sheets/FRAMING_A0_vs_A0L_y0.png`.

**H3 goes to the eye, and this report attaches no verdict to it.**

## 5. What the eye flags past the instruments

The exemplar bar says flag what no instrument measures.

- **Register drift on the crop twins.** Both read glossier and smoother than the full-figure v9
  set — a CG/toy surface rather than the ultra-realistic scaled hide with sharp scale relief the
  entry asks for. It matters for H3 specifically: if the crop paint is stylistically different
  from the full paint, projecting it first makes a head that does not match its own body, which
  is a **different** failure from mush and would read on the sheet as one.
- **D5 disagrees with itself across the two crops.** At yaw 0 the crown spikes are slate
  blue-grey and the cheek frill green; at yaw 45 the crown is bone-ivory and the frill scarlet.
  One declared element, two yaws, three colours, none of them the declared one on both.
- **D6's neck spines** are pale blue-grey at yaw 0 and ivory at yaw 45; the entry says charcoal.
- **D15 / D9 again.** The mouth interior is dark maroon on both crops where D15 declares dark
  slate — 6,871 px at yaw 0. The same cavity confusion the companion recorded at bust scale.

## 6. Prediction scorecard

| # | class | verdict |
|---|---|---|
| P1a direction < 1.0 | DERIVED | **held** — 0.0903 / 0.0905 |
| P1b 0.08–0.25 | DERIVED | **held**, near the band floor, below my 0.14 centre |
| P1c route ratio 0.9–1.9 | DERIVED | **FALSIFIED** — 0.815; the atlas under-resolves at both frames |
| P1d rule asks for the cap | DERIVED | **held** — 11.07× needs 3.33× linear |
| P1e the lever is not a head lever | CODE-READ | **held** — 76.7% of the rect is not head |
| P1f growth ANDON ~60% to pass | DERIVED | not run; the arithmetic says PASS at every scale |
| P2a 3.0× / 9.0× | DERIVED | **held** — 3.00× / 9.02× measured |
| P2b D8 lands as an eye | BLIND | **held**, on both |
| P2c D10 separate teeth | BLIND | **held** |
| P2d D5 lands / reads merged | BLIND | **split** — lands on both; the merged clause **falsified** |
| P2e gate + achromatic bands | DERIVED | **held**, all three clauses |
| P2f IoU ≥ 0.98 | DERIVED | **held** — 0.9909 / 0.9947, via a new instrument |
| P2g 14–17 terms; nape marginal at yaw 0 | DERIVED | **FALSIFIED** twice — 19/18 terms; nape 12.2% at yaw 0 |
| P2h 0 re-rolls | DERIVED | **FALSIFIED** — 1 spent, and the named alternative was wrong too |
| P2i \|ΔL\*\| ≤ 3.0 | DERIVED | **FALSIFIED** — −3.16 / −7.35 |
| P3a reach unchanged | DERIVED | **held** — 1,635,304 on all three runs |
| P3b 78–88% / 39–45% | DERIVED | **held** — 87.5% / 44.2% |
| P3c −0.5…+1.5 pts | DERIVED | **held** — +1.1, and nothing was lost |
| P3d 40k–160k crop-owned | BLIND | **held** — 96,241 |
| P3e H3's branch | BLIND | **to the Director** — no verdict offered |
| P4a 0 float32 facing diffs at yaw 45 | CODE-READ | **held** — 0 of 3,240,510, weights too |
| P4b off-frame 10⁴–10⁵ | CODE-READ | **held in direction, magnitude under-predicted 3×** |
| P4c ratio 1.00332 | CODE-READ | **held** — 1.003313, IoU 0.986006 vs 1.000000 |

Eleven held, five falsified, one split, one not run, one to the Director.

## 7. What this session does not settle

- **Whether the detail pass earns its keep.** H3 is the sheet at his zoom. The numbers say the
  crop paint reached the head and owns a quarter of it; they cannot say whether it looks better.
- **The scarlet frill.** 22,420 px on a declared surface, and its one bounded re-roll traded it
  for something larger. Whether the crop pass ships with it, escalates, or waits on a different
  lever is a ruling's.
- **Whether `--fit-axis width` is adopted** for `project_twins` and pinned in the profile
  alongside the other three consumers. A0/A1 ran on it and A0L measures the alternative; the
  choice is not mine.
- **A2's real form.** The arithmetic says allocation is a live constraint at both frames. A
  beast-derived head rect would make the lever mean something; writing one reverses Ruling 2.
- **`thin_extent`** — untouched, still the stroke-lane ruling's.

## 8. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions blob-pinned before the first measurement, with blind status per item; A2's rule registered before its number and the collision registered before the measurement; three PowerShell recipes saved (`render_crops.ps1`, `build_v10.ps1`, `run_stage1.ps1`) with their derivations in the header; both crop frames derive from the recorded head box by the recorded rule; every crop-camera override passed at full float precision and echoed by the tool; harmonization operands recorded per view; upload content-hashes recorded |
| ANDON_AUTHORITY | **3** | E13 Gate 0 re-run on both paths at 0 differing elements before any crop projection; the harmonization identity test **fired on this session** for not having been given the reference; `e12_twin_readout`'s key-health guard fired and refused to hand over a registration number, which is why a new instrument exists; `e12_stem_delta` halts on an undeclared new stem key and has no flag for a vanished one; the reach-invariance check verified against an independently re-run ceiling instrument; the new frame-bounds test is inside the tool, not a shell chain |
| NAMED_COMPENSATORS | **3** | 0 credits; 3 generations with `estimate_credits` first; every write under new paths (`E13_twins/crops/`, `E13_stage1/`, `E13_gate0/anchor*_h13*`); no re-bake, so `E12_prep` is byte-untouched; the rejected re-roll retained beside the artifact it did not replace; both tool changes additive with defaults that reproduce every prior anchor, proven not asserted |
| DECOMPOSE_BY_SECRETS | **3** | A2's allocation measured independently of A1's generation; capability (crop cameras, frame bounds, framing family) separated from policy (which crops, which framing) and from the ruling; crop stems derive from the committed entry through the committed builder; the framing fix is a flag, not an edit to a fixture |
| UNCERTAINTY_GATED_HUMANS | **3** | The payoff is a pre-registered four-column sheet with the baseline beside it at his zoom; A2 ran under a rule registered before measurement and its decline rests on a prediction registered before the measurement; the re-roll bounded at one and its failure reported as the result; every falsified prediction reported as falsified, including three of my own derivations and one operating error |
| EXTERNAL_VERIFIER | **2** | The Gate 0 anchor tests new code against output the old path produced; the ceiling instrument checks the projector's reach from an independent code path; registration measured against geometry the generator does not control; the width-fit frame checked against a recorded artifact rather than against my own arithmetic. `skip:` on a second model per the arc's precedent |

---

**Tasks 1–3 complete. HALT.** A2's arithmetic and its decline, both crop twins with their
sidecar and gates, the retained re-roll, three stage-1 runs against an unmoved ceiling, the
hole maps, the ownership decomposition and the four-column sheets go to the **advisor's eye
first, then the Director's**. His two pre-stated questions have evidence: the crop paint
**reaches** the head and owns a quarter of it, reach **did not move**, and whether it *looks*
better is the sheet's to answer. No stroke ran; `thin_extent` is untouched; nothing was adopted.
