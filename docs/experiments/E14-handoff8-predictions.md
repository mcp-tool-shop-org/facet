# E14 handoff 8 — the BLIND predictions, committed before any stroke submits

**Executor session, 2026-08-08.** Written and committed **before stroke 2 (yaw 180) — or any
other stroke — was emitted, graphed or submitted.** No stroke of this session's seven has run.

**Disclosure of what is NOT blind.** I have read handoff 7's report, so I know stroke 1's
committed count (4,344) against its probe column (7,591) — the calibration series' first
point, ratio **0.572**. I know each remaining stroke's probe column, quoted in the dispatch. I
have not emitted a job, built a graph or submitted anything for strokes 2–8, and I have not
looked at any frame of theirs.

---

## 1. Per-stroke committed texels, and the probe-vs-actual ratio

The dispatch pre-states the probe columns. Ruling 27d pre-states that actuals undershoot,
with one measured point (0.572 at yaw 0). My model: the ratio is driven by how much of a
stroke's mask is *rim* — the probe's blur fake keeps rim colours, a real inpaint moves them,
and `edge-dist 4` then rejects them. So I predict the ratio falls further where the mask is
thinner (edge-ons, whose mask is almost all boundary) and sits nearer stroke 1's where the
mask carries interior.

| stroke | yaw | probe | predicted committed | predicted ratio |
|---|---|---|---|---|
| 2 | 180 | 6,559 | **3,700** | 0.56 |
| 3 | 45 | 10,539 | **5,800** | 0.55 |
| 4 | 225 | 8,600 | **4,700** | 0.55 |
| 5 | 315 | 9,633 | **5,100** | 0.53 |
| 6 | 135 | 7,728 | **4,100** | 0.53 |
| 7 | 90 | 14,211 | **6,000** | 0.42 |
| 8 | 270 | 27,010 | **11,000** | 0.41 |

**Total for the seven: ~40,400 texels.** With stroke 1's 4,344 that is **~44,700 against the
69,239 achievable set — 64.6%**, and against the 210,907 territory, 21.2%.

Stated as a falsifiable band rather than a point: I expect every ratio in **0.35–0.65**, and I
expect the two edge-on strokes to carry the two *lowest* ratios of the eight. If any diagonal
or face-on lands above 0.70 my rim model is wrong; if any stroke exceeds its probe column at
all, Ruling 27d's upper-bound finding is wrong.

## 2. The two edge-on strokes' 20b outcomes

**Stroke 7 (yaw 90): 20b CLEAN. Stroke 8 (yaw 270): 20b CLEAN.** I predict neither edge-on
stroke misbinds.

Grounds, and I am aware this is the optimistic call on the lane's two riskiest frames: 20b's
two realised instances both fired where the generator had *sparse constraint* — the twin
stage at cn 0.9 on bare clay (the mid-grip ring read as a crossguard), and the stone, a
compact structure whose bright thin rim resembles a jewel setting, sitting in a mask that
covered its whole visible face. The edge-on strokes are the opposite case on both axes: the
ribbon's flanks are **already-painted real steel** (the context constraint Ruling 24e's order
was built to accumulate), the mask is a narrow interior ribbon rather than a whole structure,
and the guard fragments are a separate component. The thing that would falsify me is the one
the record warns about: the guard's edge-on face is exactly the *blob* whose silhouette
matched a template before.

If I am wrong, I predict it fires at **yaw 270 rather than 90**, and as a **crossguard-like
form in the blade ribbon near the guard** rather than a face/skull motif — the mid-blade pale
smears noted at HALT 1 are where a template would find purchase.

## 3. The fifth-signature share

Stroke 1 measured 29.1% of the fill dark+desaturated against the context's own 31.8% — the
against-the-context form, where less-or-equal is clean. I predict **every one of the seven
lands below its own context's share**, in the band **20–34%** absolute, and I predict the two
edge-on strokes sit in the *upper* half of that band (a narrow ribbon inside a dark guard
context has more crevice to fill). A stroke reading *above* its context's share is the
signature firing, and I predict that happens **zero times in seven**.

## 4. Where the deep-share lands after all seven

The post-re-projection reading is 19,530 band texels = 1.179% of styled, 26.92% of them
interior, **91.8% of the band on the blade**. The strokes add ~40,400 styled texels, and they
paint the blade rim and the ribbon — the same structure that owns the band.

I predict the band's **share falls** (the denominator grows and new paint is not lavender)
to **1.05–1.15%**, that its absolute count **rises slightly** to **19,800–20,600**, that the
blade's share of it **stays above 90%**, and that the interior fraction stays within two
points of 26.9%. **The stone stays at or below its current 133 texels** — nothing in this
lane's masks touches it.

## 5. Two calls I will be graded against besides the numbers

- **Zero credits on all seven submissions.** Every submission on this route has quoted 0.
- **The invariance ANDON passes on all seven.** 46 probes plus three real strokes have passed
  it at this recipe; I predict no fired ANDON. A fired one would mean the cloud repainted
  backdrop, which nothing in the recipe has done yet.

---

*Written under the handoff-8 dispatch's requirement that predictions be committed before
stroke 2 submits. Recorded here whatever the lane's fate: the step-0 halt
([E14-handoff8-step0-halt.md](E14-handoff8-step0-halt.md)) may mean these are graded by a
later session rather than this one.*
