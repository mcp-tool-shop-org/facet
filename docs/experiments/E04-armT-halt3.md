# E04 Arm T — the eight twins exist. Two ANDONs fired. HALT.

**Executor session, 2026-08-04, after Ruling 14.** All three restart gates passed to the
digit. **The eight twins were generated — 8/8, 0 failed, 0 credits, 0 re-rolls.** Then two
in-tool ANDONs fired: the bake's, exactly where Ruling 14 pre-stated it would, and the shipped
palette gate's shape check, on the arm's own artifacts.

**The headline is the second one: `ship.json`'s measured frame width 1066 is not a legal
diffusion width.** All eight twins came back **1064 × 1024** against 1066 × 1024 controls,
clay and silhouettes. Every twin↔silhouette pairing is refused, which is why **no registration
IoU is reported** — that is precisely the quantity this defect corrupts.

Predictions committed blind at `b8245a7` before any twin existed. **The predictions are not
scored in this document**, because the measurements that would score them need the pairing the
ANDON refuses.

---

## The restart gates — all PASS

| gate | result |
|---|---|
| purity check on the grown ship profile | **PASS** — 26 values / 8 tools, **zero NO-SUCH-FLAG rows**. Thirteen VALUE-DIFFERS (the profile working) + the known `cull_unseen.production` *not evaluable* |
| `restylize_views` loads clean | **PASS** — `0 values applied`, no ANDON |
| width-fit framing verification, views 1/7 | **PASS, to the digit** — 1 px / 0 px, hit 321,219 vs mask 321,218 |

## The generation — clean, and recorded

| | |
|---|---|
| batch | 8 items, `submit_batch`, **8 ready / 0 failed** |
| credits | **0** — `estimate_credits` 0, `dry_run` validated first |
| re-rolls | **0** |
| workflows | `E04_armT/workflows/twin_{0..7}.json`, **saved before submission** and link-checked in code for self-links and dangling targets (the Arm G7 lesson — a hand-retyped graph with `VAEDecode.samples=["14",0]` had passed `dry_run`) |
| inputs | 16 uploads, **all 16 returned distinct content-addressed names** — asserted, so no two views can share an input |
| recipe | seed 770700 · steps 20 · cfg 2.5 · denoise 0.92 · CN 0.9 · shift 3.1 · euler/simple · LoRA @ 0.75 — the pair's anchor, unchanged |
| prompt | identical across all eight, asserted; G6 gilded (Ruling 7), G7 head-noun (Ruling 9) |

## ANDON 1 — the bake. Exactly the case Ruling 14 pre-stated.

```
AssertionError: ANDON: head islands did not keep their x1 scale through pack_islands
(0.2432 -> 0.2432)
```

`bake_hero_prep.py:381` — `assert share_area > share_area_pre * 1.2`.

**At the ruled `head-scale: 1.0` this assertion cannot pass, by construction.** Scaling by 1.0
is the identity, so `share_area == share_area_pre` *exactly*, and the guard demands ≥ 20%
growth. It encodes "head-scale is always > 1" — a character assumption — and **allocation NONE
is unreachable through this branch.**

The other branch is no escape and I did not try it: `--no-head-scale` asserts
`share_area > share_3d`, i.e. *"the input already puts extra texels on the head."* **Both
branches require a privileged region to exist.** A uniform atlas — Ruling 14's ruled allocation
— is not expressible either way. Finding-1 class, as pre-stated: halt, don't tune.

Measured on the ship before it fired, and worth keeping:

| quantity | value |
|---|---|
| head-band faces (W3's crop rect on ship geometry, inert by design) | 203,908 / 939,104 |
| islands total / head islands | 31,007 (30.3 faces each) / 5,403 (257,974 faces) |
| head UV-area share, before and after ×1 scaling | **0.2432 → 0.2432** |
| head face-count share | 0.2747 |
| packed UV coverage of the atlas | 3.01% |
| native UVs | used as-is, no re-unwrap |

**Consequence, unchanged from the last halt but now with the guard named:** no prep bake → no
`meta.json`/`pos.npy`/`nor.npy`/`mask.npy` → **the H4 reach ceiling still cannot be computed**,
and `project_twins` still cannot run.

## ANDON 2 — the frame. 1066 is not a legal diffusion width.

```
AssertionError: ANDON: mask (1024, 1066) vs image (1024, 1064) for .../twin_0.png
```

Fired by the shipped `palette_gate.py:116` on the first pairing it was handed.

**All eight twins are 1064 × 1024. All eight controls, clay renders and silhouettes are
1066 × 1024.** Unanimous, no exceptions.

**Mechanism, arithmetic and checkable:**

| width | ÷ 8 | ÷ 16 | where it is used |
|---|---|---|---|
| **1066** | **133.25 — NOT divisible** | 66.625 — no | `ship.json` `verify/turn_render.py.w`, measured from the mesh aspect |
| 1064 | 133 — divisible | 66.5 — no | **what came back** |
| **1072** | 134 — divisible | **67 — divisible** | the Gate 0 driver's own frame (the 4c sidecar: *"the pin said 1072 × 1024"*) |
| 1024 | 128 | 64 | the pair, via Ruling 6's deviation |
| 752 | 94 | 47 | W3 |

The Qwen VAE downsamples by 8. A 1066-wide image encodes to `floor(1066/8) = 133` latent
columns and decodes to `133 × 8 = 1064`. **W3's 752 and the pair's 1024 are both divisible by
8, which is why four experiments never met this** — and the pair specifically dodged it,
because Ruling 6's ratified deviation put it at 1024 × 1024. E04 is the first time this
subject's *measured* frame has been through the generator, and it does not survive it.

`ship.json`'s `w: 1066` is derived correctly — `0.99866 / 0.95975 = 1.04054`, `1024 × 1.04054 =
1066` — and is nonetheless **not expressible through the generator**. A profile value that the
geometry demands and the diffusion stack cannot accept.

### What I could NOT establish, reported as unresolved rather than forced

**Whether the 2 px was a crop or a rescale.** I tried and the test is confounded:

| view | mask bbox w | twin bbox w | if rescale | if crop |
|---|---|---|---|---|
| 0 | 886 | 887 | 884.3 | 886 |
| 1 | 717 | 722 | 715.7 | 717 |
| 2 | 454 | 458 | 453.1 | 454 |
| 4 | 886 | 885 | 884.3 | 886 |

The twin's painted figure exceeds the mesh silhouette by **+3 to +6 px** (mean edge deltas
−3.12 left, +0.75 right) — paint spill larger than the 2 px in question. And the decisive
constraint: **the figure sits ≥ 90 px from the right frame edge on every view** (margins 90,
170, 306, 179, 90, 179, 306, 170), so whichever way the pipeline handled it, **no figure
content was lost** and the question is not observable from these artifacts. I am not reaching
for a third instrument to force an answer to a question the data cannot settle.

### Why no registration number appears in this report

Registration IoU and centroid are **boundary** measurements, and the defect is a frame-edge
mismatch. A ≤ 1 px alignment uncertainty that is negligible for a region's colour statistics is
not negligible for the number T6 predicted to four significant figures. Reporting it would be
measuring the defect and calling it registration. It is withheld, not lost — it re-measures in
minutes once the frame is ruled.

## The one screen that needs no pairing, and therefore no ruling

The pre-registered rejection rule — **material not in the spec** — needs no baseline and no
silhouette. Run against each twin's own border-ring-keyed figure (geometry is unusable here;
the key was bbox-checked against the mesh silhouette first — +3 to +6 px spill, no runaway).
**Both gate bounds are `null`. Nothing below passes or fails.**

| view | figure px | blue **allowed** off-band | % | largest CC | blue **excluded** off-band | % | largest CC |
|---|---|---|---|---|---|---|---|
| 0 | 457,567 | 2,116 | 0.46% | 323 | 8,873 | 1.94% | 6,757 |
| 1 | 361,386 | 1,360 | 0.38% | 1,129 | 6,773 | 1.87% | 4,595 |
| **2** | 211,677 | **11,875** | **5.61%** | 1,686 | 16,246 | 7.67% | 9,406 |
| 3 | 360,829 | 3,455 | 0.96% | 863 | 4,248 | 1.18% | 1,685 |
| 4 | 456,682 | 8,615 | 1.89% | 2,123 | **8,615** | 1.89% | 2,123 |
| 5 | 360,590 | 3,779 | 1.05% | 399 | 4,574 | 1.27% | 739 |
| 6 | 210,898 | 2,065 | 0.98% | 564 | 4,272 | 2.03% | 825 |
| 7 | 361,139 | 2,085 | 0.58% | 181 | 2,457 | 0.68% | 276 |

Two things the numbers say that are worth the advisor's eye, neither a verdict:

- **View 2 (stern-on) carries 5.61% off-band with blue allowed — roughly 3× any other view.**
  For scale, E08's invented sleeve measured 6.17%. **But its largest component is 1,686 px
  against that sleeve's 4,882** — so this is diffuse, not one garment. That is exactly the
  separation the two-number discipline exists to make, and it is making it.
- **View 4 is the only view where allowing blue changes nothing** (8,615 both ways) — zero
  pixels in the 273–301 band. Blue is present on the other seven (372–6,757 px). On a subject
  whose blue band is **suspended on a 3.69% denominator**, a view with no blue at all is the
  kind of datum the suspension anticipated.

## Looked at, at full size — observations, not judgments

- **G7 landed on the broadside.** View 0 shows a row of **red gun port lids** framing each
  cannon along the hull, plainly. Recorded because Arm G7's cluster instrument returned `NEAR`
  at ΔE 28.3 on a three-quarter view of the same subject, and this is the head-noun form at
  broadside scale.
- **All three mastheads terminate in gold spires.** The fixture declares **one** gilded spire,
  on the stern turret (G6). Gold on three mastheads is in-spec material in a place the fixture
  did not put it — the same classification Ruling 6 gave G6's original miss, so **no re-roll
  trigger** under the stated rule. A placement observation for the Director, whose window it is.
- **The backdrop realised grey again**, visibly ~rgb(175) against an asked `plain white` —
  consistent with Ruling 6's banked asked-vs-realised gap.

## Artifacts

`E04_armT/twins/twin_{0..7}.png` · `workflows/twin_{0..7}.json` · `clay/` · `masks/` ·
`controls/` · job ids and per-view sha256 in the sidecar.

## The questions

1. **The frame.** `w: 1066` is geometrically derived and diffusion-illegal. **1072 is divisible
   by 16 and was this subject's Gate 0 frame already**; 1064 is divisible by 8 only. Changing
   `w` changes the framing derivation and re-runs the anchor; the eight twins regenerate on any
   answer that is not 1064. Not mine — it moves a measured profile value.
2. **The bake guard.** Allocation NONE cannot pass either branch of
   `bake_hero_prep.py`'s post-pack assertion. Step-0-class code work, or a third branch, or
   something else.
3. **Does anything else in the route assume a frame divisible by 8?** I have not swept for it,
   and I am not going to guess: the same question that produced this halt should be asked once,
   mechanically, across every tool that names a width.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Workflows saved before submission and link-checked in code; 16 upload names asserted distinct; every gate result is the pre-stated instrument's own stdout |
| ANDON_AUTHORITY | **3** | Two ANDONs fired and neither was worked around. The bake's alternate branch was identified and **not tried**. The palette gate's shape check was not satisfied by resizing an artifact. Registration is withheld rather than reported from corrupted operands |
| NAMED_COMPENSATORS | **3** | 0 credits, 0 re-rolls of the 1 allowed. Canon fixture untouched — the vacuous blob bound the tool required lives in a scratchpad copy, never in `canon/`. All writes new files |
| DECOMPOSE_BY_SECRETS | **3** | The frame finding is the boundary test again: a correctly derived subject value that shared code cannot accept |
| UNCERTAINTY_GATED_HUMANS | **3** | Three questions as choices; the crop-vs-rescale question reported as **unresolved** rather than answered by a confounded instrument; placement observations handed to the Director rather than classified |
| EXTERNAL_VERIFIER | **2** | Both ANDONs are in tools this session did not write, asserting against artifacts their authors never saw. `skip:` on a second model |
