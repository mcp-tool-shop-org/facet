# E14 handoff 2 — predictions, committed BEFORE any measurement

**Executor session, 2026-08-07.** Written and committed before the sweep ran, before the
bake ran, before any instrument touched `longsword_00001_raw.glb` in this session.

**Blind status, stated per group rather than claimed wholesale:**

- **Tasks 1, 2, 3 predictions are BLIND to their own results** — no instrument in this
  session has produced a number yet.
- They are **NOT blind to the repo's record**. Gate 0's measurements
  ([E14-gate0-report.md](E14-gate0-report.md)) are in hand and are the basis of several
  predictions below; where a prediction is arithmetic on a Gate 0 number rather than a
  guess about an unmeasured quantity, it says so. E12's Task 3 report made exactly this
  distinction and it is worth keeping: *the scoreboard is the same number in both cases
  and does not mean the same thing.*
- Several predictions below are **derived from instrument source read this session**
  (`e08_ceiling.py`, `bake_hero_prep.py`, `e12_thin_curve.py`, `turn_render.py`,
  `restylize_views.py`). Reading the instrument is not measuring the subject, but it does
  make those predictions cheap — flagged **[src]** where it applies.

---

## §0 — The dispatch's own inherited claims, checked against source in the same breath

| claim (source) | checked against | verdict |
|---|---|---|
| watchdog "restarted this morning after an overnight death" (kickoff) | `_watchdog_KILL.log`, `_watchdog_HEARTBEAT` | **partially contradicted — below** |
| designated mesh: 1 welded shell, 0 boundary edges, 121 non-manifold, frame 240×1024 | `E14-gate0-report.md` §3/§5/§10, `stats_00001.json`, `frame_00001.json` | to verify in the report |
| blade hollow box section, total ~0.0208, walls ~0.00196 | `E14-gate0-report.md` §4/§6 | to verify in the report |
| off-surface "has replicated 2.50–2.64% across three subjects" | `E12-task2-report.md` carries ship 2.5065% and beast 2.6430% — **two**; the third subject's figure is not in that table | to locate, or report unlocated |
| "Gate 0 renders show views 2/6 rendering the gem and boss at near-nothing edge-on" (carried flag) | the actual renders, per view, at the profile frame | **to verify, not import** — §9 |

**The watchdog claim, measured now rather than accepted.** Verified alive before any GPU
work and reported either way as the dispatch requires: heartbeat file **1.5 s old** against
the 15 s threshold, no `_watchdog_DEAD`, no `_watchdog_TRIPPED`, live 2 s samples in
`_watchdog_log.csv`, VRAM 2,045–2,058 MiB against the 31,200 MiB ceiling. **But the log does
not say what the dispatch says.** `_watchdog_KILL.log` holds exactly two entries since
2026-08-06: `watchdog up` at **2026-08-06 15:42:54** and `watchdog up` at **2026-08-07
20:29:09** — the latter roughly five minutes before this session's first check, i.e. *this
evening*, not this morning. **No DEAD line exists for 2026-08-06 or 2026-08-07**; the most
recent is 2026-08-05 19:36:15. A silent death (hard kill, the loop never reaching its own
handler) is consistent with an unlogged overnight death, so the *death* is not contradicted —
but the *restart* the dispatch places this morning is timestamped tonight, and the Gate 0
session's own heartbeats at 02:51–02:57 today show it alive after any overnight window.
Recorded as a discrepancy in an inherited claim; nothing in this session depends on it.

---

## §1 — Task 1, the sweep

| # | prediction |
|---|---|
| **S1** | Both instruments exit **non-zero** — each is an ANDON that fires on any undecided flag, and `prop.json`'s own `_status` says it has not been swept. |
| **S2** | `texpass_iter.py --thin-extent` is in the UNDECIDED set. Deliberate; `_still_suspended.thin_extent` names it. |
| **S3** | `restylize_views.py --canny-low` **and** `--canny-high` are both in the UNDECIDED set — two members, not one. Both flags exist with defaults 0.4 / 0.8 and neither appears in `prop.json`'s `restylize_views` block. [src] |
| **S4** | `brush_cloud_step.py --lane` does **NOT** appear. `prop.json` carries the `_not_on_route` per-invocation block E12 Ruling 5c/6d minted for exactly this, and `_not_on_route` is a recognized decision form. **The prediction I am least sure of**: the E12 sweep counted `lane` UNDECIDED on all three profiles *before* that block existed, and whether the sweep accepts `prop.json`'s **dict-shaped** `_not_on_route` as it accepts `texpass_iter`'s is a code fact I chose not to check. |
| **S5** | Total UNDECIDED = **3** (S2 + S3's two). Band if S4 is wrong: 4. |
| **S6** | The coverage pass reports **NOT A PURE RELOCATION** with **12–22** mismatches — the beast's was 17, and this profile's deviations are the same families (frame, tag, allocation, suspensions, the protective prompt). |
| **S7** | `cull_unseen production` is **26 cameras, byte-identical to the tool default, no narrowing**, and the static checker reports it `not evaluable` (a computed expression), so it is checked by hand. |
| **S8** | No `bake_hero_prep` flag appears UNDECIDED despite `island-margin`, `pack-margin`, `angle-limit` and `bound` being absent from `prop.json` — the classification table should call those CODE, not SUBJECT-DATA. **Low confidence**; I have not read the table. |

## §2 — Task 2.1, the prep bake

| # | prediction |
|---|---|
| **Q1** | Bake completes **exit 0** with no ANDON fired. |
| **Q2** | `assert n_head > 500` does **not** fire, and n_head lands in **250,000–480,000**. Arithmetic, not a guess [src]: the crop rect at `crop_res` 1024 and `bound` 0.55 selects `z_std ∈ [−0.0945, +0.2922]` — a **mid-height band**, ≈38.7% of the figure's height, running from ~40% to ~79% of height above the tip. The sword's whole x range (±0.113 canonical) sits inside the rect's x span [360,700], so the band is decided by height alone. Against Gate 0's hilt share (35.4% of faces in the top 30.6% of height) that band should hold ≈38% of faces. |
| **Q3** | **The band is not the hilt, and the ANDON's pass says nothing about allocation.** Its top edge is z_std 0.2922 while the Gate 0 hilt runs z_std ≈0.195 → ≈0.501, so the band takes the *guard and lower wrap*, **misses the pommel, the gem and the upper wrap entirely**, and takes ~29% of height's worth of blade. Same shape as the beast's finding (*a huge band is not a right band*), different mechanism: there the rect was too big, here it is in the wrong place. |
| **Q4** | Native UVs kept, no re-unwrap. |
| **Q5** | Valid texels @ 4096 land in **2.7M–3.5M** (16–21% of the 16.78M atlas), the same order as ship 3,111,817 and beast 3,240,510. Face counts sit within 6% across the three subjects. |
| **Q6** | The head-scale-1.0 identity clause passes within its 1e-6 relative tolerance. |
| **Q7** | Blender's imported face count differs from `mesh_stats`' 999,474 by **fewer than 50 faces** (the beast's discrepancy was 11). |

## §3 — Task 2.2, the reach ceiling and the off-surface rate

**The load-bearing prediction of this session, and it is a consequence of Gate 0's headline.**

| # | prediction |
|---|---|
| **R1** | **The eight-camera ceiling is bounded above by roughly 52% of valid, by the hollow finding**, and I predict it lands in **40–53%**. [src + Gate 0 arithmetic] `e08_ceiling` does a real first-hit raycast (`out[idx[~np.isfinite(t)]] = True`), so the **inner wall is unreachable by construction**. Gate 0's manifold-piece split on this mesh is 521,134 outer / 478,288 inner faces — **47.85% of faces are inner wall** — and if UV area tracks face count the reachable ceiling cannot exceed ~52.15% however many cameras are added. |
| **R2** | Following from R1: **the 12-camera row adds under 1.5 points over the 8-camera row**, and even a 24-camera row would not break 53%. The saturation is not a camera-count fact on this subject; it is a topology fact. |
| **R3** | Within the outer wall, eight equatorial cameras at facing-min 0.45 reach **most** of it — reachable ÷ (outer-wall share of valid) > **0.85**. A blade's dominant normals are ±y (dot 1.0 to views 0 and 4), the wrap is a cylinder covered around, and the residue is up/down-facing surface needing `nz > 0.893` to fail every equatorial camera. |
| **R4** | `e08_ceiling`'s three SETTINGS blocks print **one measurement three times under two false captions**, exactly as Ruling 6e recorded, because `prop.json` sets `head-facing-min` equal to `facing-min`. Quoted once, with the caveat. [src] |
| **R5** | `front-back OVERLAP = 0` again, and again it is a line that cannot be non-zero at any positive floor. [src] |
| **R6** | Off-surface rate lands in **2.2–3.0%** at the >1 px threshold. I expect the property to replicate rather than break, which makes this a weak prediction and a strong test — a miss here is the more informative outcome. |
| **R7** | The emit-pixel unit derives from **this** subject's framing (fit-axis **height**, aspect 240×1024, margin 1.204). Direction predicted: **smaller than the ship's 1.12e−03 and within 2× of the beast's 6.72e−04**. |

## §4 — Task 2.3, the thin_extent cost curve

`ext = 2D − tF − tB` is a **per-view screen-space front-to-back extent in canonical units**
[src], and the canonicalisation `(x,−z,y)/vmax*0.5` is the one Gate 0's thickness figures were
already quoted in — so the blade's **0.0208 outer-to-outer** is directly comparable to a
candidate value.

| # | prediction |
|---|---|
| **T1** | The curve is monotone non-decreasing in withheld fraction, and **0.0 withholds exactly nothing** (the disabled guard, and a curve point). |
| **T2** | **The character's 0.03 withholds the blade almost entirely on the face-on views** — blade-region withheld fraction > **0.80** at views 0 and 4 — because 0.03 exceeds the blade's own 0.0208 front-to-back extent. |
| **T3** | **The ship's 0.01 withholds under 15% of the blade region**, and **the beast's 0.005 under 6%**. |
| **T4** | **The withheld fraction is strongly view-dependent, and this is the finding to look for.** Edge-on (views 2, 6) the blade's front-to-back extent is its *width* (~0.06–0.11), not its thickness, so at every candidate below 0.03 the edge-on views withhold **far less** of the blade than the face-on views. Face-on ÷ edge-on blade-withheld ratio at 0.02 exceeds **3×**. |
| **T5** | The box-section caveat holds: the probe reads **outer-to-outer**, so nothing in the curve responds to the ~0.00196 wall. The 0.002 region of the curve is flat and empty, not a wall-thickness cliff. |
| **T6** | Withheld fraction of the **whole visible figure** at 0.03 exceeds **0.45** on views 0/4 — the blade is most of what this subject shows face-on. |

## §5 — Task 2.4, the elevated cameras

| # | prediction |
|---|---|
| **E1** | Up-facing surface (normal_z > 0.5, **area**) is under **3%** of total surface area. Gate 0 measured the z-max slab at 0.1013% of area, but that is a *height* slab, not a normal criterion — quillon tops and the guard's upper faces are up-facing at mid-height and are not in it, so the normal-criterion number should be several times larger and still small. |
| **E2** | The eye-level eight already reach **> 55%** of that up-facing area (a 45°-inclined normal still gives dot 0.707 to an equatorial camera, clearing facing-min 0.45). |
| **E3** | The best single elevated camera adds **under 1.5 points** of total coverage, and the honest disposition is **NONE**. Stated as the prior to bet against, per the profile — the beast's lesson is that this class has no working prior until measured, so **E3 is the prediction most worth being wrong about.** |
| **E4** | Ray density is quoted with every first-hit figure (the 7b law), or the number is not reported. |

## §6 — Task 2.5, the mirror check

**A direct prediction against the dispatch's own parenthetical, stated plainly so whichever
way it falls is legible.** The dispatch writes that the E12 9b/16f caveats *"predict
near-equality within AND across mirror pairs here."*

| # | prediction |
|---|---|
| **M1** | **Within** mirror pairs: near-equal, agreed. Views 0/4 within **2%** of each other; 2/6 within 2%; and 1/3/5/7 all within 3% of each other — the subject carries **two** mirror planes (the blade's own face plane, and the left/right plane through the quillons), so the diagonals form one family of four rather than two pairs of two. |
| **M2** | **Across** mirror pairs: **NOT near-equal, and not close.** `area(view 0) / area(view 2) > 2.5`. Face-on the blade shows 60–110 px of width against a few px edge-on over ~70% of the frame's height, and no hilt structure makes that up. **If M2 holds, any instrument normalising by per-view silhouette area on this subject inherits a denominator swinging more than 2.5× between views** — a sharper version of the beast's 1.65×, and the fifth moving-denominator instance in this repo. |
| **M3** | View 0 carries the **largest** silhouette area of the eight; view 2 or 6 the smallest. |

## §7 — Task 3.1, the canny pair

| # | prediction |
|---|---|
| **C1** | At the falsified 0.4/0.8 pair on this clay, **contour dominates control px and Canny contributes under 25% of the total** — the same grey-on-grey mechanism that produced 6,482 px on a Workbench render. |
| **C2** | Control px rises monotonically as the pair falls. |
| **C3** | **The works-perfectly test finds its garbage in the blade faces.** The beast's ladder found wandering iso-luminance contours in flat fields at the bottom rungs; this subject's flat fields are the two blade faces — large, smooth, lit by a single gradient. The lowest rungs admit long wandering contours *down the blade face parallel to the central ridge* that are not relief. |
| **C4** | The central ridge **is** relief and appears at mid rungs on face-on views — the discriminating structure the ladder should keep. |
| **C5** | The pair is **proposed, not adopted.** This session halts and the advisor rules it. |

## §8 — Task 3.2, the backdrop

| # | prediction |
|---|---|
| **B1** | The unconstrained metric optimum is **saturated (> 0.30)** and disqualified by the standing rule, reported anyway. |
| **B2** | **L1 steel binds the low-saturation optimum.** It is the largest surface, near-achromatic, and an achromatic material sits at the centre of the chroma circle where nothing escapes it except by lightness. |
| **B3** | Following from B2: **the low-saturation optimum is far from steel in L\***, not in hue — its L\* differs from steel's by more than **25 points**, and the derivation's real content is a *value* decision wearing a hue decision's clothes. |
| **B4** | **Blue-violet is genuinely unoccupied** on the declared five: steel and blackened iron sit below any chroma floor (hue undefined, not blue), gold is warm yellow, oxblood and garnet are wine-red. Checked, not assumed — and the check applies a chroma floor to every element before any hue is quoted. |
| **B5** | As on the beast, **the metric will not separate the hue families** — the top low-saturation candidates across green / blue-violet / warm span under **0.03** of weighted-min score. The word is the ruling's. |
| **B6** | **W3's mid grey and the galleon's white both score badly, and the grey scores worse** — the exact five-times-measured trap the fixture names, with the largest near-neutral surface being the blade itself. |

## §9 — Task 4, the one-string premise

| # | prediction |
|---|---|
| **W1** | The carried flag is **directionally right, and its wording is what I expect to fail.** Views 2 and 6 are edge-on; the gem pommel and the diamond boss are *not* equally at risk there — the gem is a roughly isotropic polyhedron reading at close to full width from every yaw, while the **boss** is a diamond plate on the guard *face* and is the element that genuinely goes near-nothing edge-on. Predicted: **gem present on all eight views; the boss the one element at risk on 2/6.** |
| **W2** | The profile-rendered views will be **pixel-identical** to the Gate 0 renders except for filename tag. [src] Gate 0 rendered at `--w 240 --h 1024 --clay` with every other flag defaulted, and `turn_render`'s defaults are `fit-axis height`, `margin 1.204`, `step 45`, `yaw-offset 0` — exactly what `prop.json` pins. The 4a law still requires the fresh profile render (the tag is a real dependency and Gate 0 is not a byte-anchor), but the *pixels* should match, and I will **compare pixels, not file bytes** (a PNG hash mismatch is not evidence a render changed). |
| **W3-p** | Therefore **the one-string premise passes on this subject** — the first since the ship — but on a narrower argument than the profile's note gives: not "slivers of everything" but "four of five elements read at every yaw, and the fifth is a boss whose worst view still carries its silhouette." Stated as the thing to check, not the conclusion. |

---

## What I expect to be most wrong about

**S4 and E3, for opposite reasons.** S4 is a code fact I chose to predict rather than check —
the cheap kind of wrong. E3 is the kind this repo keeps paying for: I am predicting NONE on
the elevated cameras because the prior says NONE and the profile says NONE, while the profile
entry *itself* records that this class has no working prior until measured. If E3 is wrong it
will be because a tip-standing sword's **quillon tops and stepped guard ends** are a larger
up-facing population than a z-slab measurement suggested — which is exactly the shape of the
P9/P25 error the Gate 0 session made, assuming the risk lives where the *form* suggests rather
than where the structure actually is.

**R1 is the prediction I most want scored.** If the ceiling does **not** land near 52%, then
either UV area does not track face count on this mesh or the hollow does not partition the
atlas the way Gate 0's face split implies — and both are findings larger than this session's
task list.
