# E14 handoff 5 — blind predictions, committed BEFORE the ceiling runs

**Executor session, 2026-08-08.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 19f;
dispatched at [E14-executor-kickoff.md](E14-executor-kickoff.md) "Session handoff 5".

**Blind.** No seven-camera reach has been computed, nothing has been projected, and no stage-1
artifact exists. Everything below is reasoned from the record: the eight-camera ceiling
(`ceiling.json`), the atlas anatomy (`atlas_anatomy.json`), the twin set and its seed split
(handoff-4 report), and the beast's stage 1 as the method precedent.

Written and committed first so it can be scored rather than rationalised.

---

## 0. What I read out of the record before predicting (numbers, not recollections)

| quantity | value | source, verified this session |
|---|---|---|
| valid texels | **3,661,903** | `ceiling.json`, `atlas_anatomy.json` — same number from two files |
| eight-camera reach | **1,879,807 = 51.33%** | `ceiling.json`, all three facing settings identical |
| yaw 90's marginal **at position 3** of the ladder | **101,544** | `ceiling.json` `marginal.yaw90.added` |
| the four diagonals' *combined* marginal after the four cardinals | 14,049 + 8,752 + 18,528 + 10,718 = **52,047** | `ceiling.json` `marginal` |
| islands | **46,496** | Ruling 9c |
| off-surface at birth / erode-2 residue | **11.0875% > 1 px / 0.0085%** | Ruling 9c, `atlas_anatomy.json` |
| unreachable that is inner wall | **93.34%**; outer-wall reach rate **93.98%** | Ruling 10b, `atlas_anatomy.json` |

**Two things about the instruments, checked rather than assumed.** `e08_ceiling` takes
`--sets N` (full equatorial rings) and its `--elev` extras are only unioned for `n >= 8`, so
**it cannot express a seven-camera set** — the ceiling must run through
`e14_atlas_anatomy --views`, which is the dispatch's stated fallback and which carries the
recorded exact cross-check against `e08_ceiling`'s N8. And that file's reach uses a **uniform**
facing floor, which on this subject is the production floor: `ceiling.json`'s three settings
(production 0.45/0.18, uniform 0.45, uniform 0.18) return **identical** numbers at every N, so
the head-band split is inert here and the comparison is like-for-like.

---

## 1. P1 — the seven-camera ceiling, relative to 51.33%

**Prediction: the loss from dropping yaw 90 is FAR smaller than the 101,544 texels / 2.8 points
that Ruling 18c priced from the position-3 marginal. I predict a delta of 0.2–1.2 points —
most likely 0.3–0.9 — putting the seven-camera ceiling at 50.1–51.1% of valid, most likely
50.4–51.0%.**

In texels: **1,835,000–1,875,000 reachable**, against the eight-camera 1,879,807.

**Why, and why this is worth staking rather than inheriting.** 18c's 101,544 is yaw 90's
marginal when it was added **third**, on top of only yaws 0 and 180. That is a
position-dependent number, and the ladder's own later rows say the position matters enormously:
after the four cardinals were in, the four diagonals together bought only 52,047. A surface
whose normal points at yaw 90 passes the facing test from **both** yaw 45 and yaw 135
(cos 45° = 0.707, comfortably above the 0.45 floor), and on a sword's edge-on structures —
quillon ends, blade edge — there is little to occlude the diagonal rays. So most of what yaw 90
uniquely held at position 3 should be recoverable from its neighbours once they are present.

**If I am right, Ruling 18c's cost line needs its number restated** — not its decision, which
rested on two measured failures, but the price tag attached to it. **If I am wrong** and the
delta really is near 2.8 points, that says the edge-on band is genuinely only visible from
yaw 90, which would be a real finding about this subject's thinness and would make view 2's
exclusion more expensive than the ruling recorded.

**The eight-camera 51.33% remains the route-comparable and this run's denominator is the
seven-camera number.** Both get reported; neither is a target (Ruling 10b's bias caveat rides
with both — the shipped 3e-3 bias exceeds this route's ~0.00196 wall floor and is worth
+0.97 points at N8, so the geometric number is 50.36–50.43%).

## 2. P2 — styled / valid, and styled / ceiling

**Prediction: styled/valid lands 38–46%, centred on ~43%. Styled as a share of the
seven-camera ceiling lands 80–92%, centred on ~85%.**

Anchors and the reasoning: the beast banked **44.2% of valid = 87.5% of its 50.46% ceiling** at
stage 1 and went on to acceptance. This subject's ceiling is about the same height, so the
comparable question is what fraction of reach survives the edge test. Two pressures point in
opposite directions and I do not think either dominates:

- **Downward** — this is the route's thinnest subject. `edge-dist 7.0` scales by figure width
  over `edge-ref 700`, and at a 240-px frame the figure spans roughly 142–204 px, so the scaled
  distance falls to ~1.4–2.0 px and is then raised by `edge-floor 2.5`. A 2.5-px peel from each
  side is cheap on a 60–110-px blade and expensive on the quillon ends and the blade's edge
  strata. The A3 invariant bounds it locally, which is exactly why the per-structure area-loss
  report is the number to read.
- **Upward** — 68.6% of this subject's valid texels sit within 2 texels of an island edge
  (46,496 islands). Margin texels inherit their island's interior geometry, so they should pass
  or fail with it rather than being systematically lost.

**Pre-registering the does-nothing band, because this is a new number on a new subject:** if
the projection were doing nothing beyond reach, styled would equal the ceiling; if the edge
test were annihilating thin structure the way the shipped erosion once did (100% / 100% /
77.6% of the three thinnest strata), styled/ceiling would land in the 50s. Anything in the 80s
is the edge test costing what it costs.

## 3. P3 — the gem region's blended composition

The set is split by seed and therefore by gem colour: **views 0 and 4 carry garnet (770700);
views 1, 3, 5, 6, 7 carry the drift (770701)**; view 2 is excluded. Projection is
ownership-not-averaging with `power 6.0`, so each gem texel takes the single view that faces it
best — there is no blending to average the two populations together.

**Prediction, in three parts:**

1. **Source split: 55–80% of gem texels sourced from drifted views, 20–45% from views 0 and 4.**
   Seven cameras at 45° spacing means each owns roughly ±22.5° of a convex knob's angular range;
   two of the seven owners are garnet. Views 0 and 4 should over-perform their 2/7 share because
   the pommel's largest facets face the cardinal directions, which is why I put the garnet floor
   at 20% rather than at 2/7 = 29% and the ceiling at 45%.
2. **Hue composition: lavender + magenta (290–360°) at 40–70% of the gem's above-floor texels;
   wine (0–25°) at 10–30%.**
3. **⚠ The part I most want scored: the projected gem will be VISIBLY PATCHY, not uniformly
   one colour or a smooth gradient.** Garnet facets adjacent to magenta facets, with the seam
   falling on ownership boundaries rather than on the stone's own facet edges. The two source
   populations differ by roughly 65° of hue with nothing between them, and ownership is a hard
   per-texel choice. **If the projected gem instead reads as one coherent stone, my model of
   what the blend does is wrong and Ruling 19b's "measured, not predicted" instinct will have
   been right for a reason I did not anticipate.**

**And the denominator will be small.** I predict the gem region is **5,000–40,000 valid texels**
— 0.1–1.1% of valid. Per the D8 lesson and the dispatch's own warning, that count gets quoted
beside every ratio, and if it comes in at the bottom of that band I will say the ratios are
thin rather than dress them up.

## 4. P4 — per-view marginal ordering and acceptance

**Prediction on marginal contribution, added in turnaround order 0, 1, 3, 4, 5, 6, 7:**

**view 0 largest by a wide margin > view 4 > view 6 > {1, 3, 5, 7}**, with the four diagonals
each **under 40,000 texels** and within a factor of ~2 of each other.

Grounds: at the ceiling pass yaw 0 alone reached 822,951 and yaw 180 743,893, and those two are
views 0 and 4. Yaw 270 (view 6) added 159,372 as the fourth camera. The diagonals added
8,752–18,528 each when they entered last. Turnaround order puts view 1 second, before its
mirror view 4 has been added, so **view 1 should score higher here than its 14,049 ladder
figure** — it enters against only view 0 rather than against four cardinals. That reordering
effect is the same one P1 turns on, and I expect it visible in both places.

**Per-view accepted (committed) texels — a different quantity from marginal, and I predict the
ordering differs from it:** views 0 and 4 each commit **400,000–800,000**; view 6 commits
**60,000–250,000**; each diagonal commits **50,000–250,000**. A diagonal can own texels a
cardinal also reaches whenever it faces them better, so I expect the diagonals' *committed*
counts to be several times their *marginal* counts. If committed ≈ marginal for the diagonals,
the ownership rule is not doing what I think it does.

## 5. P5 — the A3 invariant and the erosion report

**Prediction: zero A3 violations, and that this is uninformative.** The invariant bounds
erosion at `e <= 1/3 x local half-width` by construction, so violations are foreclosed — the
repo has already paid for gating on the direction an invariant forecloses. The informative
number is the **per-structure area loss**, and there I predict **the thinnest strata lose the
largest area fraction, monotonically**, with the thinnest stratum losing **over 40%** of its
area and the blade's body losing **under 10%**.

## 6. P6 — what will not happen

No registration or bbox ANDON (halts are suspended by profile: `reg-iou-min 0.0`,
`bbox-tol 9.99`); view 2's twin does not enter any projection input; nothing generates and no
credits are spent; no pass condition exists to pass or fail.

---

## Standards compliance (this predictions file)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every prediction carries its instrument, its band and its denominator; §0 records the source file for each number the predictions rest on, and the two instrument facts (e08_ceiling cannot express seven cameras; the three facing settings are identical here) were read out of the code and the JSON rather than assumed |
| ANDON_AUTHORITY | **3** | Committed before the ceiling runs, so P1 cannot be tuned to it; P2 pre-registers the does-nothing band and the annihilation band for a number this subject has never produced |
| NAMED_COMPENSATORS | **3** | Creates nothing irreversible; no spend on this dispatch at all |
| DECOMPOSE_BY_SECRETS | **3** | P1 separates the *set-level* loss from the *position-3 marginal* — the same quantity confused across two rulings — and predicts they differ; P4 separates committed from marginal and predicts their orderings differ |
| UNCERTAINTY_GATED_HUMANS | **3** | P3's patchiness claim is stated as the one I most want scored, with what its failure would mean; P1 says explicitly what a wrong answer would imply about view 2's real cost |
| EXTERNAL_VERIFIER | **2** | The ceiling instrument and the projector compute reach on independent code paths and their N8 agreement is on record; the gem readout will use the band instruments rather than the projector's own numbers. `skip:` on a second model, per precedent |
