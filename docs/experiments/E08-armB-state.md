# E08 Arm B — state, and a scope finding

**Executor session, 2026-08-04.** Arm B was ratified as a *run*: twins → project → eight
strokes → finalize → pack → renders. **Two of those steps do not exist yet as runnable tools.**
Recording that before spending anything further.

## Done

**Eight clay views rendered** — `facet_E08/ARMB/clay/w3clay_{0..7}.png`, from
`facet_E06/C1/prep/prep_uv.glb` via `turn_render.py --clay --views=0,1,2,3,4,5,6,7`. Local,
free, no GPU. Yaw confirmed: view 0 = 0°, view 4 = 180°, 45° steps.

## I called a halt, and the halt was wrong — the check I used was too strict

I compared file hashes against the shipped renders, got a mismatch, and halted. The pixel
comparison reverses it:

| comparison | pixels |
|---|---|
| `BG/clay_grey/w3clay_0.png` vs my ARMB view 0 | **521 differing of 770,048, max ±1/255**, mean 0.00024 |
| view 4 | 386 differing, max ±1 |

No pixel differs by more than one 8-bit level. That is rasterisation noise, **not a different
mesh or framing** — independently confirmed by size, background `(154,154,157)`, figure fraction
**17.60%** and bbox **390×849 @ y89** all being identical across every render.

**This is the same error I corrected earlier this session and then repeated: file bytes are not
pixel values.** A PNG hash mismatch is not evidence that a render changed. Stating the halt and
then checking was right; reaching for the hash first was not.

**Mitigation, so the question cannot matter:** views 0 and 4 will use the **shipped**
`BG/clay_grey/` files — byte-identical to what the canon twins, N11, ARMOUR, BRACER, SPEC and
CONTRA all consumed — and only the six genuinely new views use the ARMB renders.

## A record discrepancy, found on the way

`BG/clay_grey/w3clay_0.png` and `facet_E01/tex_W3/views/w3clay_0.png` are **pixel-identical**
(0 differing pixels) but have **different file hashes** — `cac49be7d96c35d7` against
`4075a9dce257be2b`. And `E08-armBG.md` claims byte-for-byte reproduction quoting
`4d65b67abae2928f` / `d2c6153be6e1d7ac`, **which match neither file on disk today.** The BG
arm's reproduction claim is true in pixels and false as stated in bytes. Flagged, not corrected
here — it is the advisor's record.

## The scope finding: two tools have to be built, not run

### 1. `project_twins.py` accepts exactly two views

```python
VIEWS = [
    {"name": "front", "path": args.front, "dtc": [0,-1,0], "right": [1,0,0]},
    {"name": "back",  "path": args.back,  "dtc": [0, 1,0], "right": [-1,0,0]},
]
```

Hardcoded pair, explicit camera vectors, and `--front` / `--back` are the only image arguments.
**Arm B's "eight-camera twins" cannot be run against this.**

The change is bounded: everything below `VIEWS` — `best_w`, `owner_c`, `sumW`, `sumWC`,
`reachable`, the whole `for view in VIEWS` body — is already N-general. What is needed is
constructing `VIEWS` from a `--views` argument with `dtc = (sin θ, −cos θ, 0)` and
`right = (cos θ, sin θ, 0)`, which reduces to the existing pair at θ = 0° and 180°.

**Regression anchor exists:** `--mask-keyed` must still reproduce `sha b12917a2c7c14c4b`, and
the two-view default must still land on A2's 938,718 styled texels. Neither is optional.

### 2. Exact-silhouette masks exist for two views only

`restylize_views.py --masks` needs the exact mesh silhouette per view to build the control
image. `BG2/masks/` holds `w3clay_0.png` and `w3clay_4.png` — nothing else.

The mask **cannot** be thresholded off the clay render: measured above, thresholding gives
**17.60%** of frame against the geometry's **19.01%** truth. That is E01's failure, and the
whole reason A2 exists.

`project_twins.py` already computes this silhouette by raycasting, and
`render_geomaps.py` is not a substitute — it uses MV-Adapter framing (768 px, different camera
convention), not `turn_render`'s. So the raycast needs extracting into something that writes a
mask per view.

## What Arm B actually costs, restated honestly

| step | status |
|---|---|
| 8 clay renders | **done**, local |
| 8 exact-silhouette masks | **tool needed** |
| 8 twins | 8 cloud jobs |
| N-view projection → stage-1 atlas | **tool change needed**, with 2 regression anchors |
| 8 brush strokes | 8 cloud jobs |
| finalize + pack + renders | local |
| Gate 1 sheet, reference \| asset \| provenance \| error, **incl. views 4–6** | local |

Two bounded builds and ~16 cloud jobs. That is more than the loop run it was ratified as, and
the difference is worth the Director knowing before it is spent rather than after.

**The ceiling still justifies it:** 74.10% reach × A2's 81.6% acceptance ≈ **55%** reference
coverage against A2's current 39.1%. That arithmetic is unchanged by any of the above.
