# E33 predictions — registered before the reconstruction, after the plate

**Seat:** executor · **Registered:** 2026-08-11 · **Spec:**
[E33-the-first-performer-through-the-route.md](E33-the-first-performer-through-the-route.md)

**Blind status, stated per clause below.** The order is the spec's and E32's: the plate's own
geometry is measured **first**, then predictions about what the route does to it. Nothing
about the reconstruction, the render frame, the cull or the twins has been run at the moment
this file is written.

*The law this file is written under:* write what one of the counted thing **is** before the
number; predict each clause of a conjunction separately, and the join tracks the rarest
clause, not the salient one.

---

## 0. NOT a prediction — the segmenter outcome, measured as the first route act

The spec's P0 asked whether BiRefNet isolates this figure. **It ran before this file
existed**, as the spec directs, so it is a measurement and is not scored as a prediction.
Recorded here so a later reader cannot mistake it for a hit:

| quantity | measured |
|---|---|
| `has_alpha` | **false** — the plate is RGB with no alpha channel, so the segmenter branch is taken |
| route scale | 1328 → **1024** (LANCZOS, scale 0.7711) |
| mask area at `alpha > 0.8·255` | **87,092 px = 8.306%** of the route frame |
| mask area at `L > 127` | **88,763 px = 8.465%** |
| alpha bbox | **289 × 876** px, xyxy `[354, 77, 642, 952]` |
| square crop | `[61, 77, 935, 951]`, side **874** |

⚠ **The one-pixel clip E32 measured is present again and is recorded, not repaired.** PIL's
`crop` takes its lower bound exclusive, so a crop of `(61, 77, 935, 951)` covers rows
77–950 while the figure's mask extends to row 951/952. **The bottom row of the feet is
outside the conditioning image.** Same mechanism, same magnitude, different subject.

## 1. NOT a prediction — the plate's own geometry, the denominators everything below uses

Measured from BiRefNet's own mask at route scale, never from a key
(`plate_geometry_routemask.json`):

| quantity | this subject | E32's lattice, for scale |
|---|---|---|
| fill of bbox | **35.06%** | 10.78% |
| figure bbox | **289 × 876** px (w/h **0.3299**) | 493 × 499 (w/h 0.9880) |
| width min / p01 / p05 / p50 / p95 / max | **10 / 18 / 22 / 34 / 104 / 104 px** | 4 / 6 / 8 / 10 / 26 / 28 px |
| width band share 0–8 px | **0.0%** | 0.0% |
| width band share 8–16 px | **0.53%** | 67.8% |
| width band share 16–32 px | **41.20%** | — |
| width band share 32–64 px | **20.51%** | — |
| width band share 64+ px | **37.76%** | — |
| enclosed openings, min_area 1 / 64 / 1024 | **0 / 0 / 0** | 22 / 21 / 2 |
| **p50 width as % of bbox height** | **3.881%** (34 / 876) | 2.004% |

**Premise 11 is now MEASURED: this is a solid figure, not a lattice.** Three separate
signatures say so and they agree — bbox fill 3.25× the lattice's, **zero** enclosed openings
against 22, and 37.76% of its area in members wider than 64 px where the lattice had none
above 28. It remains a **thin-limbed** subject: p05 width 22 px against an 876 px figure
height is 2.5%, and the arms/lower legs sit in the 16–32 px band that holds 41% of the area.

---

## The predictions

### P1 — shell count of the raw reconstruction · **BLIND**

*One shell is one connected component of the exported GLB as `mesh_stats.py` counts them
(unwelded, i.e. the exported-glTF count, and the welded count reported beside it).*

Two precedents pull opposite ways and I am naming both rather than picking the flattering
one. **Toward few:** E29 measured a clay-register input returning **9** shells against the
same subject's concept-image mesh at 82 — and this plate *is* a clay render, matte, on a
seamless field. **Toward many:** E32's thin-tube lattice returned **212**, and this subject's
limbs sit in the same width family; E01's four fresh character reconstructions ran **40–191**.

**Prediction: 5–90 shells (welded), largest-shell fraction 0.88–0.99.**

I am betting on the clay-input mechanism over the thin-limb mechanism, because the thing
E29 measured (fewer shells from a clay register) acts on the whole surface while the thin-limb
mechanism acts only at the wrists and ankles, which are a small share of area here (0.53% of
the mask is under 16 px wide) and were 67.8% of E32's.

**Falsifier named in advance:** if the count comes back above 150, the clay-register effect
does not survive onto a thin-limbed figure and the width band that matters is the 16–32 px
one, not the sub-16 one.

### P2 — `mesh_topology`'s nested-wall leg · **BLIND**

*The leg computes only when a second manifold-adjacency piece exceeds 1% of faces
(`e14_topology.py:154`).*

**Prediction: it DECLINES.** All five recorded character meshes decline, the largest piece
running 98.2–98.6%. E32's lattice is the only recorded COMPUTE, at 2.67%.

**Stated so it cannot be claimed as a virtue later:** a DECLINE is uninformative about
hollowness — it cannot separate *no inner wall* from *an inner wall shredded below 1%* — and
predicting an uninformative row is still a prediction that can miss (E29 P4, which hit every
band and was wrong about what they meant). If it **computes**, this is the second recorded
instance on this route and the first on a humanoid.

### P3 — thickening of the median member · **BLIND**

*The unit is the front-view p50 local width expressed as a percentage of the front-view
figure bbox height, so a render and a plate at different sizes are comparable. The plate's
value is **3.881%**.*

**Prediction: 3.7%–5.0% of bbox height, i.e. 0.95×–1.29× the plate.**

Mechanism: E32 measured **1.174×** on a subject whose median member was 10 px at route scale.
This subject's median member is 34 px — 3.4× wider — so the same absolute voxel-scale
thickening is a smaller relative move. The band's lower bound is below 1.0× deliberately:
`ss_res = 32` occupancy plus a cascade can also *shave* a smooth cylinder rather than only
inflate it, and nothing in the record says the sign is fixed.

**Falsifier:** above 1.29× would mean thickening scales with the subject rather than with the
grid, which is the opposite of the mechanism I am reasoning from.

### P4 — the hands and the ears · **BLIND, qualitative**

*A "separated digit" is a finger or thumb visible as its own protrusion with background
between it and its neighbour, on the front clay render at the derived frame. The plate shows
a thumb clearly separated from a mitten-like finger paddle carrying 2–3 shallow grooves.*

**Prediction: the thumb comes back separated on both hands (2 of 2); the finger grooves come
back as surface relief with no background between them (0 separated fingers); the ears come
back as attached ridges rather than free flaps.**

**Falsifier:** any separated finger falsifies the second clause. This is registered as a
conjunction of three clauses, each scored on its own — E28's lesson, and I am not permitted
to score the join off the salient clause.

### P5 — the derived render frame · **BLIND**

*The frame is `e12_frame.py`'s output at `--h 1024`, `--margin 1.204`, `--round 16`: the worst
yaw's width-over-height across the eight views, rounded up to a multiple of 16.*

**Prediction: width in 336–464 px, i.e. a ratio of 0.33–0.45.** The plate's front aspect is
0.3299 and the worst yaw is not the front — a standing figure's feet and its arm spread put
the widest projection somewhere near a 3/4 view, and depth is unmeasured. **The default
757×1024 is predicted NOT to crop this subject** (the E04 bowsprit trap does not fire here),
because the subject is portrait and narrower than the default — the opposite of E32's case.

**Falsifier:** a derived width above 757 would mean the mesh is wider than its plate implies,
which would be a reconstruction fact worth more than this prediction.

### P6 — the cull's seen fraction · **BLIND**

*`cull_unseen.py` classifies each face by whether any of its 46 exterior cameras sees it.
The counted thing is a **face**, and the quantity is the fraction seen by at least one
camera. W3 measured **47.6% unseen → 52.4% seen**; the tool's ANDON floors are 0.30 / 0.90.*

**Prediction: 0.50–0.80 seen.** Above W3 because this figure has no beard, no folded cloth,
no greatsword held against the body and no fingers to hide between — the geometry that made
half of W3 invisible is absent. Below 0.90 because *if* the reconstruction is double-walled,
the entire inner wall is unseen by construction, and P2 predicts the instrument that would
have told me cannot answer.

**This is a conjunction of two unmeasured things** — self-occlusion (predictable from the
pose) and inner-wall area (not predictable, and P2 says the leg will decline). I am naming
that rather than folding it into one number.

### P7 — the back twin's facing · **BLIND**

*View 4 is the rear camera. Its per-view prompt drops every face term, per E12 Ruling 9d and
E01's measurement that a prompt asking for a face on every view is an instruction to draw
one and the text beats the control.*

**Prediction: all three arms' view-4 twins come back rear-facing (3 of 3).** Registered as
three separate clauses, one per register; a register that comes back front-facing while the
other two do not is a register-interaction finding, not a noise event.

### P8 — the GPU-hours delta · **BLIND, untutored**

*The quantity is `get_usage_report`'s **GPU Hours Product** line, after minus before, over
six executed twin jobs (three registers × two views), Qwen-Image 20 steps at the derived twin
frame, zero partner-API nodes.*

**Prediction: $0.05–$0.60 total for the six.** This band is untutored — I have no per-job
figure from the record, only a 61-day total of $23.409 across an unknown job count, and I am
deliberately not manufacturing a calibration ritual on top of a population I have not
enumerated. **If it lands outside the band, the band was uninformed rather than the run
surprising**, and the useful output is the per-job number for the next spec's ceiling.

---

## What is deliberately NOT predicted

- **Whether any twin is good, or which register is right.** That is canon and it is the
  Director's; no number here approaches it, and a metric that tried would be a different
  question with a number attached.
- **Identity.** Whether the painted figure is *this* mannequin is the Director's eye on the
  Gate 0 sheet at full size.
- **`--min-iou`.** Projection is out of scope, so the registration score is not predicted and
  the gate is `NOT YET RUN`.
