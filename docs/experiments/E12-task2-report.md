# E12 handoff 2, Task 2 — the designated mesh's measurements

**Executor session, 2026-08-05.** Predictions committed blind in `96b59c1` before anything
ran. **This report covers 2.1 (prep bake) and 2.2 (reach ceiling + off-surface). 2.3
(thin-extent cost curve) and 2.4 (elevated cameras) are NOT in it and have not been run.**

Watchdog verified immediately before the GPU leg: heartbeat **0.4 s** against a 15 s
threshold, no `_watchdog_DEAD`, no `_watchdog_TRIPPED`, live 2 s samples, **0 ABORTs today**.
Re-read after the bake: alive.

---

## 2.1 — the prep bake

```
blender -b -P tools/bake_hero_prep.py -- --glb E12_gate0/dragon_00003_raw.glb
        --outdir E12_prep --profile profiles/beast.json
exit 0   wall 283.5 s   5 profile values applied
```

**No ANDON fired.** Outputs: `pos.npy` / `nor.npy` / `mask.npy` (201 MB each), `meta.json`,
`prep_uv.glb` (34.3 MB).

| quantity | value |
|---|---|
| faces (Blender) | 986,814 |
| head-band faces (W3's crop rect) | **418,979** (42.5%) |
| islands | 28,870 (34.2 faces/island) |
| head islands | 14,180 (542,699 faces) |
| head UV-area share / face-count share | 0.5179 / 0.5500 |
| triangle UV area ("packed UV area covers") | **4.38%** |
| **valid texels @ 4096** | **3,240,510 (19.31% of atlas)** |
| head-scale identity | 0.517896712 → 0.517896771, rel. 1.151e-07 against 1.0e-06 — **survived** |

**The character's head ANDON did not fire, and the reason matters more than the pass.**
`bake_hero_prep.py:216` asserts `n_head > 500`, written to catch an empty band. On this
subject the band holds **418,979 faces** — W3's crop rect covers 56.88% of this figure's
projected area (Gate 0 stats), so on a dragon it selects most of the animal. **A huge band
is not a right band.** It is inert at `head-scale 1.0` under Ruling 2, and the
scale-preservation assert confirms it: the uniform atlas came through `pack_islands`
unchanged. The ANDON is survivable here by accident of geometry, not because the rect found
a head — which is exactly why `_gates.head_rect_metrics` is `false` in the profile.

**An 11-face discrepancy, recorded rather than chased.** `mesh_stats` reported 986,825 faces
on the welded mesh; Blender's glTF import reports 986,814. 0.0011%. Both numbers are in the
record; nothing downstream in this report depends on the difference.

**4.38% triangle UV area looked alarming and is not — checked against the baseline rather
than reported as a finding.** The number is the sum of triangle areas in UV space, while the
baked mask covers 19.31%, so most of a "valid" texel budget is bake margin around islands
rather than triangle interior. Measured on both subjects by one code path, over all faces:

| subject | faces | triangle UV area | baked valid | ratio | valid texels |
|---|---|---|---|---|---|
| ship (`E04_shipprep`) | 939,104 | 3.01% | 18.55% | **6.16×** | 3,111,817 |
| **beast (`E12_prep`)** | 986,814 | **4.38%** | **19.31%** | **4.41×** | **3,240,510** |

The beast is *better* than the accepted ship on both columns. The ship's prep log was not
preserved, so this is a recomputation of `bake_hero_prep`'s own quantity by this session on
both meshes, not a comparison against a logged number.

## 2.2 — the reach ceiling, pre-registered before any projection

```
e08_ceiling.py --prep E12_prep --sets 2,4,6,8,12 --facing-min 0.45 --head-facing-min 0.45
```

Floors are the profile's ruled values — `head-facing-min` equal to `facing-min` per Ruling 2
(allocation NONE, bands inert).

| cameras (equatorial) | reachable texels | % of valid |
|---|---|---|
| 2 | 954,884 | 29.47% |
| 4 | 1,383,955 | 42.71% |
| 6 | 1,580,597 | 48.78% |
| **8 — the stage-1 set** | **1,635,304** | **50.46%** |
| 12 | 1,697,605 | 52.39% |

**Valid 3,240,510 · head band 1,358,656 · the pre-registered stage-1 ceiling is 50.46% of
valid at eight eye-level cameras.** Every downstream coverage number on this subject is to be
read against that, the way the ship's 42.72% was.

Marginal gain in turnaround order: +yaw 0 → 480,442 · +180 → +474,442 · +90 → +200,664 ·
+270 → +228,407 · +45 → +83,287 · +135 → +51,558 · +225 → +59,844 · +315 → +56,660.

### Two instrument findings, both reported not fixed

**(a) `e08_ceiling` printed one measurement three times, under two wrong labels — and this
configuration is what makes it fire.** The E04 session record flagged this trap; it lands on
the beast by construction, because Ruling 2 set the head floor equal to the body floor.
`e08_ceiling.py:114-116`:

```python
SETTINGS = [("production (body 0.45 / head 0.18)", args.facing_min, args.head_facing_min),
            ("uniform 0.45",                       args.facing_min, args.facing_min),
            ("uniform 0.18",                       args.head_facing_min, args.head_facing_min)]
```

All three labels are hardcoded text. With `--head-facing-min 0.45` the three blocks evaluate
(0.45, 0.45) three times and print identical ladders, while block 1 claims "head 0.18" and
block 3 claims "uniform 0.18". **There is one measurement in that output, not three
confirmations**, and two of its captions are false. Quoted here as one.

**(b) `e08_ceiling`'s "front-back OVERLAP" line cannot be non-zero.** It prints
`front-back OVERLAP = 0 texels — this is the population a hold-one-out comparison at N=2
would have`. For an opposed pair the two tests are `dot(n, d) ≥ f` and `dot(n, −d) ≥ f`;
both can hold only if `f ≤ 0`. Measured rather than argued, on this bake's own normals:

| facing floor | front | back | **both** |
|---|---|---|---|
| 0.45 | 960,809 | 915,087 | **0** |
| 0.18 | 1,368,772 | 1,314,997 | **0** |
| 0.00 | 1,649,476 | 1,591,034 | **0** |

Zero at every floor including 0.00. It is a diagnostic line rather than a gate, so the cost
is low — but by the repo's own law **a check that cannot fail is not a check**, and reading
that zero as a subject property would be an error.

### `pos.npy` off-surface — the E10 Ruling 4 classification

**The shipped instrument cannot run on this subject.** `e10_offsurface.py` hardcodes
`E04_shipprep` / `E04_stroke`, reads `ship.json`'s waterline, and its second half needs an
emitted stroke directory (`job_y+000_e+00/cam.json`, `hit.png`). **The beast has run no
strokes**, so that half has no operands. Rather than edit an instrument whose numbers are
cited in a closed ruling, the bake half was carried into `tools/diagnostics/e12_offsurface.py`
with the subject supplied by flags — same method, same reconstruction
(`(lo + pos*(hi−lo)) * 0.5/maxabs`), same open3d distance query, same fixed-seed sample.

**Validated against the ship's ruled number before being used on the beast:**

| subject | one emit px (canonical) | median distance | **>1 px** | >5 px | max |
|---|---|---|---|---|---|
| ship, via this instrument | 1.121625e-03 | 0.0060 px | **2.5065%** | 2.0940% | 147.4 px |
| ship, **E10 Ruling 4 as ruled** | — | — | **2.5%** | — | — |
| **beast** | 6.718107e-04 | 0.0013 px | **2.6430%** | 2.4395% | 377.6 px |

The reimplementation reproduces the ruled ship figure, so the beast number is measured on a
path with a known anchor. The emit-pixel unit is **derived from this subject's own ruled
framing** (`fit-axis width`, aspect 1792×1024, margin 1.204 → `h_ext` 1.203885, `v_ext`
0.687934), not inherited — getting that wrong would scale every threshold.

**Report-only, per the dispatch.** E10 Ruling 4 established that the ship's off-surface
texels were *painted, not padding*; that half needs a stroke and is not askable here yet.

## 3. Predictions scored — 2.1 and 2.2 only

| # | prediction | outcome | measured |
|---|---|---|---|
| Q1 | bake completes exit 0, no ANDON | **held** | exit 0, 283.5 s |
| Q2 | `n_head > 500` does not fire; n_head > 100,000 | **held** | 418,979 |
| Q3 | native UVs, no re-unwrap | **held** | as logged |
| Q4 | valid texels 2.4M–3.6M | **held on the band, reasoning FALSIFIED** | 3,240,510 — I predicted **lower** than the ship's 3,111,817 and it came in **4.1% higher** |
| Q5 | 8-camera reach 55–72% of valid | **FALSIFIED** | **50.46%** |
| Q6 | 12 cameras add < 3 points over 8 | **held** | +1.93 |
| Q7 | every 8+ set above the ship's 42.72% | **held** | 50.46 / 52.39 |
| Q8 | off-surface 1–6%, ship is the right anchor | **held** | 2.6430% against the ship's 2.5065% |

**Q5 is the calibration entry, and it inverts Gate 0's.** At Gate 0 I anchored four
predictions on the ship and the subject landed an order of magnitude the *character* side.
Here I corrected for that, put the reach band nearer the character — and it landed at
**50.46%**, nearer the ship, only 7.7 points above it and 23.6 below the character. The
honest conclusion is not "anchor on the ship after all": it is that **this subject class has
no working prior in either direction**, and reach on a winged quadruped is not interpolable
from a standing human and a hull. Its own measured 50.46% is now the anchor, and nothing
downstream should be read against a borrowed one.

Q4 records the same lesson in miniature: the band was wide enough to hold, the direction was
wrong, and the direction was the part that came from reasoning about the ship.

## 4. What has NOT run

- **2.3 — the thin-extent cost curve and the membrane fraction.** Not started. The
  measurement's shape is established (`texpass_iter` computes a per-view screen-space
  front-to-back extent `2D − tF − tB` and withholds `ext < thin_extent`), which means the
  membrane fraction needs a **spatial** wing region rather than a thickness criterion, or the
  measurement is circular. Wing boxes will be located by eye and overlaid for checking, as
  the Gate 0 head box was.
- **2.4 — the elevated-camera question.** Not started.
- Tasks 3, 4, 5. No generation has run; no credits spent.

## 5. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Every invocation, exit code, wall time and profile-value count logged in `prep.log`; the off-surface pixel unit derived with its operands printed; JSONs beside every measurement |
| ANDON_AUTHORITY | 3 | Watchdog verified before the GPU leg and after; the bake's character-written ANDONs pre-stated as halt-not-tune and reported as passed-with-reason rather than passed; two instrument defects surfaced rather than worked around |
| NAMED_COMPENSATORS | 3 | New files only, under `E12_prep/` and one new diagnostic; `e10_offsurface.py` deliberately **not** edited because its numbers are cited in a closed ruling; no spend |
| DECOMPOSE_BY_SECRETS | 3 | The off-surface pixel unit derived from this subject's ruled framing rather than read from another subject's `cam.json`; the ceiling run at the profile's own floors |
| UNCERTAINTY_GATED_HUMANS | 2 | No threshold adopted, no value written to any profile; the ceiling is pre-registered before any projection so downstream numbers cannot be read against a moving denominator |
| EXTERNAL_VERIFIER | 3 | The new off-surface instrument was validated against the ship's independently ruled 2.5% before being trusted on the beast; the alarming 4.38% was checked against the ship by recomputation rather than reported as a finding; the overlap claim was measured at three floors rather than argued |
