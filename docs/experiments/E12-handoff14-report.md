# E12 handoff 14 — the stroke lane's inputs: hole map, cameras, order, thin_extent, prompts

**Executor session, 2026-08-06.** Predictions registered blind in `27adee3`
([E12-handoff14-predictions.md](E12-handoff14-predictions.md)), git blob `507d792`, written
before the hole map was decomposed, before a candidate camera was scored, before a thin_extent
value was evaluated at the brush level and before a stem was derived.

**Nothing generated, nothing spent, nothing irreversible.** All raycast, hole-map arithmetic
and derivation. Watchdog alive before every Blender-free local leg (VRAM 1,899 MiB against the
31,200 ceiling); no Blender ran — `texpass_iter emit` is the raycast renderer.

**Four results carry this report.**

1. **The Ruling 7 elevated re-open CLOSES, and the check I first wrote for it could not
   fail.** Largest up-facing coherent field in the brush's set is **2,108 texels** (1.03% of
   it), and the population an elevated camera would serve *better* is 3.13–8.67% depending on
   threshold, in components of at most 1,217.
2. **The brush's set is rim, and the sheet shows it** — wing trailing edges, spine rows, claw
   tips, frill tips. But **it is not thin structure**, which is where my own reasoning broke
   and took four predictions with it.
3. **Four strokes close 71.60% of the brush's territory** at the ship's own stopping floor,
   read against both denominators. The greedy is far *steeper* than the ship's, not flatter.
4. **The beast cannot run a stroke through `brush_cloud_step` as it stands** — verified by
   execution, not by reading. The saltroad LoRA loader is unconditional in the model chain.

**Look at these before the numbers:** `E13_stroke/HOLECLASS_sheet.png` (where the brush's
territory actually is) · `E13_stroke/thin_crops/FORBIDS_ladder_y337.png` (what each
thin_extent value forbids, the ship's artifact criterion).

---

## 1. Task 1 — the hole map, decomposed

Committed instrument: [`e13_hole_map.py`](../../tools/diagnostics/e13_hole_map.py). Reach is
**recomputed from geometry** rather than read out of the run being characterised, so the two
agree or the halt fires. They agree exactly.

| | texels | of valid |
|---|---|---|
| valid | 3,240,510 | |
| reach (recomputed; banked 1,635,304) | **1,635,304** | 50.46% |
| A0 styled | 1,430,687 | 44.15% |
| **the BRUSH's set** — reachable, unstyled | **204,617** | 6.31% |
| **DILATION's set** — unreachable at all | **1,605,206** | 49.54% |

204,617 + 1,605,206 = 1,809,823, the ruled hole count, with **no remainder**. **88.7% of holes
are geometry, not misses** — the ship measured 91%.

### Where it is (P1a: the "rim" half held, the "thin" half did not)

`HOLECLASS_sheet.png` at five yaws: the amber traces **wing trailing edges, wing leading edges
and finger struts, the tail and dorsal spine rows, claw tips, frill and horn tips**. It is an
edge map of the animal. The tables say the same thing in numbers — the holed fraction is
almost flat everywhere, which is the signature of a rim process rather than a missed field:

| | brush | holed % of that region's own reach |
|---|---|---|
| head box | 16,271 | 13.22% |
| wing_R box | 32,425 | 10.57% |
| wing_L box | 50,038 | **14.54%** |
| rest | 105,883 | 12.29% |
| up nz>+0.5 | 48,697 | 12.97% |
| side \|nz\|≤0.25 | 47,208 | 11.46% |
| down nz<−0.5 | 52,970 | **16.13%** |

**P1d falsified as stated**: the left wing is the most-holed named region, but the right wing
is the *least* — the wing boxes do not both beat the head. **P1c falsified**: up-facing is
23.80% of the brush set against my predicted 6–14%. I predicted the wrong quantity — my
reasoning was that erosion has no orientation preference, and the *holed fractions* above
(12.97 / 11.46 / 16.13) say exactly that. The share just reflects the mesh's own orientation
mix, which my prediction should never have been about.

**P1b falsified twice, once by 58 texels.** 9,301 components at voxel 3e-3 (~3.5 texel
spacings, quoted because a component count without its adjacency scale is not a number);
largest **25,058** against my predicted "under 25,000" — a miss of 0.23%, and it is a miss.
The second clause is a real miss: I predicted over 60% of the set in components under 1,000
and measured **36.73%**. The set is chunkier than I thought — 77.56% sits in components under
10,000, and the two largest (25,058 and 20,859) are the two wing trailing edges.

### The Ruling 7 re-open check — and the check that could not fail

The first version of this check asked whether elevated cameras add binary coverage of the
brush set. **It returns 100% for the eight eye-level yaws and exactly 0 for every elevated
candidate, and it would do so whatever the geometry looked like**: `reach` is the union of
`seen(yaw, 0, 0.45)`, the stroke floor is 0.25, and the visibility test is the same first-hit
raycast — so eye-level coverage is a superset by construction. A check that cannot fail is not
a check. It is retained in the tool, printed as tautological, and replaced by one that can
fail.

**The real question is whether an elevated camera sees anything *better*** — a grazing camera
paints a stretched sample, which is why commit has a facing floor at all.

| | |
|---|---|
| best eye-level facing over the brush set | median **0.764**, 10th pct **0.503** |
| elevated beats eye-level by >0.10 where eye-level is <0.60 | 17,748 (8.67%), largest component **1,217** |
| elevated beats eye-level by >0.20 where eye-level is <0.60 | 15,256 (7.46%), largest component 1,141 |
| elevated beats eye-level by >0.20 where eye-level is <0.50 | 6,396 (3.13%), largest component **306** |
| up-facing (nz>0.5) brush set | 48,697, largest 3-D component **2,108** |
| **the named falsifier** — up-facing brush inside the wing boxes | 17,398, largest component **2,108** |

**There is no large unpainted up-facing field.** The largest coherent up-facing component is
2,108 texels, an order of magnitude under the 20,000 I pre-registered as the firing threshold,
and the falsifier I named in advance — a big eroded up-facing wing span — does not exist:
inside the wing boxes the up-facing brush set is 17,398 texels whose largest coherent piece is
that same 2,108. Ninety per cent of the brush set is already seen at facing ≥ 0.503 by an
eye-level camera. **The re-open does not fire, answered with numbers in both directions, and
the question is reported to the ruling rather than decided here.**

## 2. Task 2 — the stroke cameras and the order

Committed instrument: [`e13_stroke_cameras.py`](../../tools/diagnostics/e13_stroke_cameras.py).
Closure is modelled as **commit's own acceptance** — facing > 0.25, first-hit visible, in
frame, and ≥ 4 px inside the emit-frame figure — not as "the camera can see it", because on
this subject visibility alone is the tautology above and ranks nothing.

*Ray density (7b): facing and visibility are one ray per texel, so there is no grid to
converge. The edge test uses the shipped emit raster (1792×1024, `--fit-axis width`) itself —
it is the operand, not a sample of a finer one.*

Candidates: sixteen yaws at 22.5°, elevation 0. **The route yaws stay in**, unlike the ship's
derivation which excluded its twin yaws — on this subject the holes *are* the twins' own
erosion rim, and commit's 4 px trim is far tighter than the projector's scaled ~14.9 px.

| pick | yaw | new | cumulative | % of brush set |
|---|---|---|---|---|
| 1 | **337.5** | 52,568 | 52,568 | 25.69% |
| 2 | **180.0** | 43,312 | 95,880 | 46.86% |
| 3 | **45.0** | 30,965 | 126,845 | 61.99% |
| 4 | **292.5** | 19,661 | 146,506 | **71.60%** |
| 5 | 112.5 | 9,992 | 156,498 | 76.48% |
| 8 | 315.0 | 3,228 | 173,063 | 84.58% |
| 16 | 90.0 | 787 | 184,771 | 90.30% |

**The stopping floor, with both denominators quoted** because the ship's absolute does not
transfer on its own: its last accepted pick added 13,126, which is 0.422% of *its* valid
(**13,669** here) or 7.24% of *its* brush set (**14,806** here). **Both give the same answer:
four strokes.**

**P3a is falsified in both clauses and in the interesting direction.** Pick 1 closes 25.69%
where I predicted under 20%, and pick 8 is 6.1% of pick 1 where I predicted above 40%. The
greedy decays **far faster** than the ship's 32.2% over eight picks. My reasoning — "rim
holes are spread so no camera dominates" — was wrong: a rim belongs to a structure, and a
structure's rim is best seen from one direction. **P3b split**: 4 strokes against my 6–10
(falsified), closing 71.60% against my 55–80% (held). **P3d held**: two of the first three
picks (180, 45) are route yaws.

**Pre-registered before any stroke runs, the way the ship pre-registered its deck plateau:**
four strokes leave **58,111** of the brush set unclosed, and even all sixteen candidates leave
**19,846** that no eye-level camera can close under commit's edge rule. Those fall to dilation
at finalize. Four strokes would take stage 1's 44.15% of valid to about **48.67%**; the
sixteen-camera ceiling is **49.85%**.

### The spiral order — a correctness constraint, not a preference

Painted-adjacency recomputed after each simulated stroke (radius 9 px, the profile's
mask-dilate, so the anchor question is asked at the scale the job mask is grown at), best
anchored first — the ship's order A.

| | camera | painted-adjacency | closes |
|---|---|---|---|
| 1 | yaw 292.5 | **92.34%** | 41,374 |
| 2 | yaw 337.5 | 87.93% | 31,864 |
| 3 | yaw 180.0 | 87.72% | 42,345 |
| 4 | yaw 45.0 | 81.87% | 30,923 |

**P3c held on both clauses**: the best anchor is 92.34% (≥ 0.90), above the ship's
80.82–84.74 band, and no camera is anywhere near the 0.70 I named as hole-dominated. **The
greedy order and the ship order are different orders** — greedy is 337.5, 180, 45, 292.5;
the order that would ship is 292.5, 337.5, 180, 45.

## 3. Task 3 — thin_extent's decision inputs, assembled

Committed instrument: [`e13_thin_inputs.py`](../../tools/diagnostics/e13_thin_inputs.py). The
thickness rule is emit's own — two raycasts, `ext = 2D − tF − tB`, thin below the value — on
the same grid, read at each brush texel's own pixel. **A texel counts as withheld only if
every selected camera that could close it withholds it**; anything weaker inflates every
figure.

The wing boxes hold **82,463** of the brush set (40.30%). The four selected strokes can close
**146,506** (71.60%), and both denominators are carried because they answer different
questions.

| candidate | withheld | of brush set | of closable | of WING brush | of non-wing |
|---|---|---|---|---|---|
| global 0 | 0 | 0.00% | 0.00% | 0.00% | 0.00% |
| global 0.003 | 71 | 0.03% | 0.05% | 0.08% | 0.00% |
| global **0.005** | 7,579 | **3.70%** | 5.17% | 5.35% | 2.59% |
| global **0.0075** | 54,266 | **26.52%** | 37.04% | 37.53% | 19.09% |
| global **0.01** | 59,218 | **28.94%** | 40.42% | 42.47% | 19.81% |
| global 0.015 | 64,506 | 31.53% | 44.03% | 45.48% | 22.11% |
| global 0.03 | 78,378 | 38.30% | 53.50% | 52.72% | 28.57% |
| wing-only 0.005 | 4,413 | 2.16% | 3.01% | 5.35% | 0.00% |
| wing-only 0.0075 | 30,945 | 15.12% | 21.12% | 37.53% | 0.00% |
| wing-only **0.01** | 35,019 | **17.11%** | 23.90% | **42.47%** | **0.00%** |
| wing-only 0.03 | 43,475 | 21.25% | 29.67% | 52.72% | 0.00% |

**The knee is between 0.005 and 0.0075** — 3.70% to 26.52% of the brush set — and it sits
exactly where the banked figure-level curve put it (Ruling 7c: knee 0.005–0.0075). Two
independent measurements, different denominators, same knee.

**P4a is falsified on all three bands, and the direction is the finding.** I predicted
0.005 → 25–45%, 0.0075 → 45–65%, 0.01 → 60–80%. Measured 3.70%, 26.52%, 28.94%. My reasoning
was that the brush's set is "selected for thinness" so a thin mask should bite two to three
times harder on it than on the figure; at 0.01 it withholds 28.94% of the brush set against
24.85% of view 0's figure — **essentially the same, not 2–3× more**. The per-camera medians
say why: local thickness at the brush texels each camera closes is 0.0066 / 0.0124 / 0.0173 /
0.0445 canonical units, so most of the brush's territory sits on structure *thicker* than
every candidate. **A rim is at the edge of a structure, not inside a thin one** — and this is
the same wrong assumption that made P1a's "thin structure" clause wrong. One error, four
predictions. **P4b falsified with it**: membrane holes withheld 37.53% / 42.47% at 0.0075 /
0.01 against my predicted >75%.

**P4c is held but partly tautological and is reported as such**: the wing-only family
withholds 0.00% of the non-wing brush set *by construction*, because I defined the candidate
with 0.0 outside the boxes. The substantive part stands on its own — wing-only 0.01 withholds
42.47% of the wing brush set at zero cost elsewhere, so the separation Ruling 7c speculated
about is available and priced.

**P4d held, and it is the artifact criterion the ship used.**
`thin_crops/FORBIDS_ladder_y337.png`, red = forbidden: at **0.005** a hairline rim around the
silhouette plus a few small membrane patches (4.0% of the figure); at **0.0075** whole
membrane panels go red (14.2%); at **0.01** the membrane sheets are almost entirely red
(22.6%). Whole structures, not outlines — exactly as predicted.

**Nothing is proposed.** Ruling 7c reserved this value to the ruling with the wing boxes and
the artifact criterion in the room; both are now in the room.

## 4. Task 4 — the brush prompts draft

`E13_stroke/brush-prompts-DRAFT.json`, version `E13-brush-DRAFT-1`, built by the **committed
builder** from the same v9 profile entry by the same deletion construction, recipe saved as
`build_brush_prompts_draft.ps1`. It is marked DRAFT-FOR-RULING, **referenced by no profile**,
and `_fixtures` gains no `brush_prompts` key this session.

**P5a held on the clause that matters and is falsified on its size.** E04 Ruling 23 set
`brush_prompts` = one constant string per stroke, resting explicitly on *"this subject has no
view-specific anatomy words"*. The beast fails that premise, and the stroke cameras measure it
— mouth-cavity first-hit as a share of each camera's own figure:

| stroke camera | figure px | mouth cavity | crown/horn | feet | tail |
|---|---|---|---|---|---|
| yaw 45.0 | 490,941 | **2.897%** | 4.022% | 22.12% | 9.69% |
| yaw 180.0 | 520,644 | **0.144%** | 3.600% | 13.63% | 10.01% |
| yaw 292.5 | 468,941 | **2.971%** | 4.218% | 28.84% | 9.67% |
| yaw 337.5 | 537,775 | **2.478%** | 3.511% | 16.82% | 8.80% |

**The cut calibrates itself.** Yaw 180 is also route view 4, whose stem handoff 8/11 already
verified against renders and which already drops the mouth family — so 0.144% is a *verified*
drop and 2.478–2.971% are *verified* keeps, and the two interleaved cameras are read against
that line rather than guessed beside it. Crown/horn, feet and tail clear on all four, so the
horn family, `charcoal claws` and `charcoal dorsal and tail spines` stay everywhere. Result:
three stems at 20 terms, one at 16 — a span of **4**, against my predicted "at least 5".

## 5. The recipe keys, enumerated — and the trap re-verified by execution

The dispatch asked for the agreement-by-value trap to be re-verified rather than assumed. It
was, by importing the module and building the graph.

| key | `brush_cloud_step` DEFAULT | accepted route / ruled value | agreement |
|---|---|---|---|
| seed | 770700 | 770700 | by value |
| steps | 20 | 20 | by value |
| cfg | 2.5 | 2.5 | by value |
| **lora-w** | **0.75** | **0.0 (RULED, 10b)** | **DISAGREES** |
| cn-strength | 1.0 | 1.0 (brush stage; the twins run 0.9) | by value |

**P5b held and the reality is worse than I predicted.** `brush_cloud_step.py` binds no
profile. `build_graph` inserts node **5**, `LoraLoaderModelOnly`, with the hardcoded
`mcp-tool-shop__saltroad-style-lora__saltroad_style_v2_lowlr_000001500.safetensors` at
`strength_model = 0.75` — **unconditionally**, and `ModelSamplingAuraFlow` reads `["5", 0]`,
not the UNET. 17 nodes. The beast's twin path builds **14** nodes with no loader at all,
because Ruling 10b's ruled expression is that *"0.0 is not a weight of zero on a loaded card,
it is no card, and the graph is built without the loader."*

So the gap is three-deep, and each layer is measurable:

1. **Today** the pre-flight halts on `_NOT_CLEARED` — `texpass_brush.py`'s block carries only
   the two marker strings and no decided values, so `pv("seed")` raises. The lifecycle working.
2. **After the ruling clears the block at the ruled `lora-w 0.0`**, the pre-flight's check (a)
   — unconditional, no flag — halts on `DEFAULTS['lora_w'] = 0.75` against the profile's 0.0.
3. **Even setting DEFAULTS to 0.0** leaves the saltroad card loaded on this dragon, and the
   pre-flight reads `gr["5"]`, so removing the loader requires touching the guard in the same
   change.

There is no `--lora-w` argument. **This is a capability gap, not a value to choose**, and it
belongs in the clearing ruling beside the keys. **P5c held**: `cn_strength` 1.0 is the brush
stage's own value against the twins' 0.9, the ship's recorded distinction, and it lives in a
tool default rather than anywhere a profile can reach.

## 6. Prediction scorecard

| # | class | verdict |
|---|---|---|
| P1a rim, not fields / thin structure | DERIVED | **split** — rim **held** (the sheet is an edge map); "thin structure" **falsified**, and it took P4a/P4b with it |
| P1b largest <25,000 / >60% under 1,000 | DERIVED | **FALSIFIED** twice — 25,058 (by 58) and 36.73% |
| P1c up-facing 6–14% of brush | DERIVED | **FALSIFIED** — 23.80%; I predicted the wrong quantity |
| P1d wing beats head/body/limbs | BLIND | **FALSIFIED as stated** — wing_L 14.54% first, wing_R 10.57% last |
| P2a re-open closes; no field >20,000 | DERIVED | **held on the field clause** (2,108, 10× under); the coverage clause was mis-specified and could not fail |
| P2b named falsifier (wing up-facing) | DERIVED | **held** — the falsifier does not fire |
| P3a greedy flat | DERIVED | **FALSIFIED** both clauses — 25.69% and 6.1% |
| P3b 6–10 strokes / 55–80% | DERIVED | **split** — 4 strokes (falsified), 71.60% (held) |
| P3c anchor ≥0.90, none <0.70 | DERIVED | **held** — 92.34% and 81.87% |
| P3d route yaws win early picks | CODE-READ | **held** — 180 and 45 in the first three |
| P4a withheld 25/45/60–80% | DERIVED | **FALSIFIED** — 3.70 / 26.52 / 28.94% |
| P4b membrane >75% withheld | DERIVED | **FALSIFIED** — 37.53 / 42.47% |
| P4c region-aware separates | DERIVED | **held, partly tautological by my own candidate design** |
| P4d whole structures, not hairlines | BLIND | **held** — 22.6% of the figure at 0.01, whole panels |
| P5a constant string / span ≥5 | DERIVED | **split** — does not transfer (held); span 4 (falsified) |
| P5b trap still live | CODE-READ | **held, and worse** — the loader is unconditional |
| P5c cn_strength differs by stage | BLIND | **held** |

Seven held, six falsified, four split. The most valuable entry is a falsification: **the
brush's territory is rim on THICK structure**, which is why thin_extent costs it far less than
I derived and why the greedy is steep rather than flat.

## 7. What this session does not settle

- **`thin_extent`.** Assembled, not proposed — Ruling 7c's deferral is honoured. The knee, the
  wing-only family and the forbidden-set crops are all in the room now.
- **The camera set and the order.** Derived and ratifiable, not ratified. Four strokes at the
  ship's floor on both denominators; the spiral order differs from the greedy order.
- **The elevated question.** Reported closed with numbers; Ruling 7's re-open is the ruling's
  to leave shut.
- **The brush lifecycle.** `_NOT_CLEARED` stands untouched. The clearing ruling must decide the
  five recipe keys *and* commission the no-LoRA capability fix, because clearing the block
  alone leaves the pre-flight halting on `lora_w`.
- **Whether any of this looks right.** No stroke exists; nothing was rendered as a finished
  asset. Gate 1's zoom is still downstream.

## 8. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions blob-pinned with blind status per item before the first measurement; every threshold a flag that prints; the component count quoted with its voxel scale; the stopping floor quoted against BOTH the ship's denominators; three PowerShell recipes saved; the draft carries per-stem provenance and its measured cut |
| ANDON_AUTHORITY | **3** | The hole decomposition halts on any remainder and on any disagreement with the banked reach, both of which recomputed exactly; **the Ruling 7 check I first wrote could not fail and was replaced in place with one that can, with the reason in the tool**; the brush lifecycle block left standing; the recipe trap re-verified by execution and found to halt three ways |
| NAMED_COMPENSATORS | **3** | Nothing generated, spent or irreversible; all writes under a new `E13_stroke/` tree plus one file explicitly marked DRAFT and referenced by no profile; A0's state read-only |
| DECOMPOSE_BY_SECRETS | **3** | Cameras derive from the hole map, thin candidates from the banked curve and the wing boxes, prompts from the profile entry through the committed builder — three derivations, three sources, none reaching into another's; closure modelled from commit's rule rather than re-read from stage 1's output |
| UNCERTAINTY_GATED_HUMANS | **3** | The one deliberately undecided value goes up as a table plus artifact crops with no recommendation; the elevated question is answered in both directions and routed rather than decided; every falsified prediction reported as falsified, including the single wrong assumption that cost four of them |
| EXTERNAL_VERIFIER | **2** | Reach recomputed from geometry rather than read from the run it checks, and it matched to the texel; the closure model is commit's rule re-implemented independently; the LoRA trap verified by building the graph rather than by reading the source. `skip:` on a second model per the arc's precedent |

---

**Tasks 1–4 complete. HALT.** The hole decomposition with the Ruling 7 check answered both
ways, the ordered stroke set with its derivation and its pre-registered residual, thin_extent's
assembled inputs with the forbidden-set crops, the prompts draft and the recipe-key enumeration
with its three-deep capability gap go to the **advisor's eye**. No stroke ran, no value was
proposed, `_NOT_CLEARED` stands, and no fixture or profile was edited.
