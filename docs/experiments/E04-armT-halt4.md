# E04 Arm T — the bake guard is fixed and fired; the 1072 anchor fired. HALT, twice.

**Executor session, 2026-08-04, after Ruling 15.** Both fixes were made and both produced a
halt at a **pre-stated** branch. **No batch was resubmitted. Nothing was projected. No
tolerance was chosen.**

Two results, and the first is the one that matters more:

1. **The bake guard, implemented exactly as ruled, falsifies the ruling's own premise.** Ruling
   15 specified `share_area == share_area_pre` *"which you measured exact."* I had measured
   them equal **to four decimal places**, said so, and implemented the ruled condition verbatim
   rather than pre-softening it. It fired: the two shares differ by **exactly 2 float32 ULPs**.
2. **The new eight-view anchor row at 1072 is `(0, 3, 0, 1, 0, 1, 0, 2)`** — pre-stated halt,
   bound still 0.

---

## Fix 1 — the scale-aware bake guard, and what it measured

Implemented at `bake_hero_prep.py:378-408`, three branches:

| `head_scale` | clause | rationale |
|---|---|---|
| **> 1.0** | the original growth assert, **statements byte-identical** | the character path at 3.0. The diff shows only `else:` → `elif args.head_scale > 1.0:`; the assert body does not appear in the diff at all, so the character path is unchanged **by construction**, not by re-measurement |
| **== 1.0** | `assert share_area == share_area_pre` — the identity must survive `pack_islands` | allocation NONE. The guard verifies what was *requested*: at ×1 the request is "change nothing" |
| **< 1.0** | raises, explicitly "not specified" | a de-allocating scale has no ruled condition. Refusing beats inventing a symmetric clause — an unspecified guard that silently passes is how a value gets treated as configured while checking nothing |

**It fired on the identity clause:**

```
ANDON: head-scale 1.0 asks for the identity and pack_islands did not preserve it —
share_area 0.24318870902061462 vs share_area_pre 0.24318867921829224,
delta 2.9802322387695312e-08. HALT: report these digits, do not choose a tolerance.
```

| quantity | value |
|---|---|
| `share_area` (after pack) | `0.24318870902061462` |
| `share_area_pre` (before scaling) | `0.24318867921829224` |
| delta | `2.9802322387695312e-08` |
| **delta as a power of two** | **exactly 2⁻²⁵** |
| float32 ULP at 0.24319 | `1.4901161193847656e-08` |
| **delta in float32 ULPs** | **exactly 2.000** |
| relative delta | 1.225 × 10⁻⁷ |
| agreement | **7 significant figures** |

**The identity survived to within two float32 ULPs.** Blender stores UVs as float32 and both
shares are read back through `foreach_get` into float32 arrays; `pack_islands` may apply a
global uniform scale, which cancels in a ratio but not in the last bits.

**I am not choosing the tolerance.** The condition was ruled, implemented verbatim, and
measured; a bit-exact equality on a float32 round-trip is one to two bits too strict, and
picking `2 ULP` or `1e-7` now — while looking at the number the choice would judge — is the
one move that is always wrong. The digits above are the evidence for a ruling.

**My four-decimal reading is what the ruling inherited.** I reported `0.2432 → 0.2432` from the
tool's own `%.4f` print and flagged at the time that this was not bit-equality. The premise
travelled as *measured exact*; it was measured to 4 dp. Recorded so the next reader knows which
part of Ruling 15 rested on a print format.

**Consequence unchanged:** no prep bake → no `meta.json`/`pos.npy`/`nor.npy`/`mask.npy` → the
H4 reach ceiling still cannot be computed and `project_twins` still cannot run. This is the
third session with that chain open and it is one ruled tolerance from closing.

## Fix 2 — the frame at 1072, and the anchor row

All three profile sites read 1072 (`turn_render.w`, `silhouette_masks.aspect`,
`project_twins.aspect`). Renders and masks regenerate **from the profile alone**, no explicit
flags: `v_ext 1.148544  h_ext 1.202382`.

**Two things independently confirmed before the gate ran**, both cheap and both worth banking:

| check | result |
|---|---|
| **pixels square at 1072?** | `h_ext/W = 0.001121625`, `v_ext/H = 0.001121625` — **equal to 9 dp**. 1066 was square too. The 6 px is margin slack, exactly as ruled — **no anisotropy, no distortion** |
| **figure scale shift** | `1072/1066 = 1.00563` → **+0.56%**, independently reproducing Ruling 15's own `thin-extent` figure from a different direction |

Silhouettes at 1072: 18.26% / 26.77% / 29.40% / 29.61% of frame, bboxes 456×856, 890×856,
721×856.

### The pre-stated gate, and it fired

```
[agree] view 0: 0 px      view 4: 0 px
[agree] view 1: 3 px      view 5: 1 px
[agree] view 2: 0 px      view 6: 0 px
[agree] view 3: 1 px      view 7: 2 px
ANCHOR 1c (geometry vs geometry, bound 0 px): worst 3 px -> *** HALT ***
```

**Row: `(0, 3, 0, 1, 0, 1, 0, 2)`** — 7 differing px against **2,484,048** summed silhouette
pixels, **0.00028%**.

The structure is clean and it names the mechanism:

- **All four axis views (0°, 90°, 180°, 270°) are exactly 0.** These are where `cam_axes`' snap
  applies — Ruling 11's own note that components within 1e-12 of 0 or ±1 are snapped exact.
- **All four diagonal views (45°, 135°, 225°, 315°) are nonzero.** These keep their irrational
  components; nothing anchors them.
- **Centroids unmoved** — max |shift| 0.0011 px, where a structural offset must move it.
- **bboxes identical on both axes in all four**: hit 720×855 vs mask 720×855.

For scale, the prey this anchor hunts measured **4.68%** with a 34 × 42 px bbox gap.

### The one pixel that is not in Ruling 11's readings, characterised

6 of 7 differing pixels are on the silhouette boundary. **One is interior** — view 1, (435,352),
in a region **94.7% filled**, i.e. solid surface rather than lattice.

I first assumed the interior one was (628,470) and **checked instead of asserting**; it is not
— that pixel is 4-adjacent to empty in a 73%-filled rigging lattice and classifies as boundary.
The interior pixel is (435,352), and its neighbourhood explains it:

```
13x13, . empty  # surface      LEFT = turn_render-convention raycast   RIGHT = silhouette_masks
   #############    #############
   ##.##########    ##.##########
   #.###########    #.###########
   .############    .############
   #############    #############
   #############    #############
   ######.######    #############   <- the disagreement
   #############    #############
   #####.#######    #####.#######
   #############    #############
   ####.########    ####.########
   ####.########    ####.########
   ###.#########    ###.#########
```

**Both implementations produce isolated 1-px pinholes through solid surface here — 8 of them in
the raycast's 13×13 window against the mask's 7 — and they disagree about one.** That is a ray
threading a triangle-edge coincidence in the *interior* of a dense tessellation, which is the
same mechanism as the boundary pixels with the coincidence in a different place. It is not a
structural offset and it is not an outer-rim effect; it is a **tessellation pinhole**, and
Ruling 11's three readings do not have a name for it.

### 1072 against 1066, for the ruling

| frame | row | worst | total px | boundary / interior |
|---|---|---|---|---|
| 1066 | (0,1,0,0,0,2,0,0) | 2 | 3 | 3 / 0 |
| **1072** | **(0,3,0,1,0,1,0,2)** | **3** | **7** | **6 / 1** |

1072 is slightly noisier. It is also divisible by 16, is this subject's own Gate 0 frame, and
is the ruled frame for reasons that have nothing to do with this row — I am reporting the
comparison, not arguing from it.

## Step 6, run anyway for the handoff

Purity check on the 1072 profile: **26 values / 8 tools, zero NO-SUCH-FLAG rows.** All fourteen
rows are VALUE-DIFFERS plus the known `cull_unseen.production` *not evaluable*. The advisor's
three-site edit binds cleanly.

## What was NOT done

The batch was **not** resubmitted — the anchor is step 5 and it fired at step 5. The eight 1064
twins stay on disk as the frame-discovery record per Ruling 15. Nothing projected. No tolerance
chosen, on either halt. `profiles/ship.json` untouched by me this leg.

## The two questions

1. **The bake identity tolerance.** Exact float32 equality across a `pack_islands` round-trip is
   1–2 bits too strict; measured delta is exactly 2 ULPs, 1.2 × 10⁻⁷ relative. A ruled tolerance
   — or a ruled change of operand, e.g. comparing in float32 rather than float64 — closes the
   bake, the ceiling and the projection chain in one.
2. **The 1072 anchor row `(0,3,0,1,0,1,0,2)`,** with its axis/diagonal split, unmoved centroids,
   identical bboxes, and one interior tessellation pinhole that is a new mechanism for this
   gate rather than a new magnitude.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The guard is three explicit branches keyed on the requested value; the character path is unchanged by construction and the diff proves it; every anchor digit is the pre-stated instrument's stdout |
| ANDON_AUTHORITY | **3** | Two pre-stated halts, both honoured. The ruled condition was implemented **verbatim rather than pre-softened**, which is why it could falsify its own premise. No tolerance chosen while looking at the number it would judge |
| NAMED_COMPENSATORS | **3** | No spend, no batch, no projection. One code edit, additive branches, git as undo; the 1064 record preserved |
| DECOMPOSE_BY_SECRETS | **3** | The `< 1.0` branch refuses rather than inventing an unruled clause — the same discipline that produced the finding |
| UNCERTAINTY_GATED_HUMANS | **3** | Both halts hand up digits, not recommendations; the interior pixel is characterised rather than classified into a reading that does not fit it |
| EXTERNAL_VERIFIER | **2** | The anchor compares two independent implementations of one convention; the square-pixel and +0.56% checks reproduce the advisor's own numbers from a different direction. `skip:` on a second model |
