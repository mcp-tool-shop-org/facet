# E08 Task 3 step 0 — HALTED at the gained-texel background check

**Executor session, 2026-08-04.** Amendment 28's step 1 is a gate and **it fired.** Steps 2–4
are untouched: no prompt file written, no stroke submitted, no cloud call made, no atlas
consumed.

```
pre-registered bound (project_twins --bg-max-pct, present in that source and reasoned there before this run):  2.0%
gained texels within dE 10 of the twin's background:
    view 1 (y+045)      46 gained    CORNER  8.696%   FITTED  8.696%
    view 5 (y+225)      87 gained    CORNER  3.448%   FITTED  5.747%
    view 6 (y+270)   8,920 gained    CORNER  7.534%   FITTED  2.242%
```

**Every gained set exceeds the bound on at least one background reference.** I am reporting it
with three qualifications that materially change how large the finding is, one of which is a
correction to my own first version of the check.

---

## 1. Two of the three views are 4 and 3 texels

| view | gained | CORNER count within ΔE 10 | FITTED count within ΔE 10 |
|---|---|---|---|
| 1 | 46 | **4** | **4** |
| 5 | 87 | **3** | **5** |
| 6 | 8,920 | 672 | 200 |

A rate over n = 46 cannot be compared to a bound calibrated on A2's 257,506 admitted texels.
Views 1 and 5 moved `fig_w` by 1 and 2 px respectively — `ed` 4.18 → 4.17 and 4.15 → 4.13 — so
their gains are a handful of texels in a 0.01–0.02 px sliver. **View 6 is the only load-bearing
measurement here**, and it is the one where `ed` fell 5.36 → 2.74.

## 2. I used the wrong control first, and correcting it shrinks the anomaly

Amendment 28 specified *"view 2's equivalent 2.75 px band as the normative control."* My first
run used view 2's **whole accepted set**, which is dominated by deep interior. The rim is
intrinsically more background-like than the interior, so that comparison overstated the excess.
Measured properly — the same 2.74–5.36 px depth band on the same-width profile:

| set | n | CORNER within ΔE 10 | FITTED within ΔE 10 |
|---|---|---|---|
| **view 6 GAINED** (2.74–5.36 px by construction) | 8,920 | **7.534%** | **2.242%** |
| view 2 accepted, **same 2.74–5.36 px band** | 37,972 | 0.271% | 0.585% |
| view 2 accepted, deeper than 5.36 px | 288,549 | 0.028% | 0.012% |
| view 6 accepted, deeper than 5.36 px | 235,496 | 1.000% | 0.282% |

The rim band really is dirtier than the interior on both views — view 2: 9.7× (CORNER) and 49×
(FITTED). So the correct control matters, and against it the view-6 anomaly is **27.8× on CORNER
and 3.8× on FITTED**, not the ~30–100× my first comparison implied.

## 3. Three things that complicate the reading, none of which I resolve

**The two background references disagree by 3.4× on the view that carries the weight.** CORNER (the 8×8 corner
median — A2's construction exactly, and what `project_twins`' probe uses) gives 7.534%. FITTED
(the per-pixel quadratic ring fit evaluated at each sample's own position) gives **2.242%**,
barely over the 2.0% bound. On a backdrop with a gradient the fitted field is the better model,
and the gained texels sit low and around the whole figure where a single corner colour is least
representative. **Which reference the bound is stated against was never specified**, and the
answer decides whether this is a 3.8× excess marginally over the bound or a 27.8× one.

**Part of the excess is a property of view 6's twin, not of the band.** View 6's own deep
interior measures 1.000% / 0.282% against view 2's 0.028% / 0.012% — that twin is 36× (CORNER)
and 23× (FITTED) more background-like than view 2's *everywhere*, including surface nobody
disputes. Normalising each view's band against its **own** interior:

```
view 6 band / view 6 interior    7.5x  (CORNER)    7.9x  (FITTED)
view 2 band / view 2 interior    9.7x  (CORNER)   48.8x  (FITTED)
```

**Relative to its own twin, view 6's rim band is proportionally no worse than view 2's — on
both references.** That is the opposite conclusion to the absolute comparison, and I cannot tell
you which framing the rule intends.

**The gains are exactly where the mechanism says, and nowhere else.** All 8,920 lie in
2.74 ≤ d < 5.36 px — 100%, with 0 outside — which is where a gain must live if the only change
is the threshold falling. They are **not local to the shadow**: median 24 px from the nearest
removed pixel, only 8.6% within 5 px. Median height fraction 0.526, 7.1% in the bottom decile;
median local half-width 12 px, 9.7% under 8 px. So this is a **rim band 2.74–5.36 px deep around
the whole figure**, not thin structure and not the ground contact. The `ed` drop is global, so
the gains are global — as expected.

## 4. What this halt is actually about

Two statements are both measured and they pull against each other:

- **The 5.36 px erosion was scaled by a lie.** `fig_w` read 536 px on a figure whose mesh bbox is
  279 px, because the twin painted a cast shadow wider than the profile. The same rule gives
  view 2 — identical width — 2.75 px. Amendment 28 is right that the +6,468 is the removal of
  erosion scaled by a falsehood.
- **The band that erosion was removing is measurably more background-like than the interior**,
  by 7.5–7.9× against view 6's own interior and 3.8–27.8× against view 2's same band.

Both can be true: the erosion depth was derived wrongly *and* the band it happened to remove
contained contamination. That is the shape of *"a guard whose stated reason is wrong may still be
load-bearing for a reason nobody wrote down"* — already in this repo's rules, from the same
erosion.

**Amendment 28 pre-registered the consequence: contaminated → HALT, because it would implicate
width-scaled erosion generally.** The measurement is over the bound on all three views and on at
least one reference each. I halt. Whether the bound applies to CORNER or FITTED, whether an
8,920-texel band at 2.242% is contamination, and whether the fix is A3's local half-width cap
rather than any tuning of `--edge-absolute` — those are rulings, and the last one is already
named in Amendment 28 as a post-Gate-1 candidate arm.

## 5. Two claims in the ruling checked against source, and not acted on

Free to check, and both hold exactly:

**The brush prompt.** `texpass_brush.py:26-30` default:

> a burly bald warrior with a long red beard, dark green knitted sleeveless tunic, polished gold
> pauldrons, **gold necklace**, dark red layered cloth skirt with a leather belt, heavy dark
> boots, holding a massive greatsword, plain grey background, visible brushstrokes, painterly
> worked surface

**"gold necklace" is there** — the term [W3-IDENTITY](../../canon/W3-IDENTITY.md) struck as N6.
Counting against the fixture's sixteen NAMED elements: **8 of 16 present**, one of those being
the struck term, and N7 (the brown leather belt) arrives as *"with a leather belt"* — a modifier
on the skirt rather than its own head noun. **Absent: N5** (gold scrollwork), **N6** (the belt
medallion the necklace displaced), **N9** (green cloth panels), **N10** (bracers), **N11** (gold
forearm plates), **N12** (gold knee plates), **N15** (ornate gold crossguard), **N16** (gold
pommel). The blade's two named gold elements are both missing from the stage that paints the
blade.

**The corner-median licence's premise.** `texpass_iter.py:143` is
`render = np.full((H, W, 3), 0.42, dtype=np.float32)` — a synthetic flat grey, confirmed. The
licence's reasoning holds: on a genuinely flat field the corner median and the fitted ring are
the same estimator. The first-stroke invariance anchor that would test the *compositing*
assumption has not been run, because no stroke has been run.

**Neither was changed.** Writing the fixture prompt file is step 2 and step 1 gated it.

## 6. Artifacts

```
ARMB/gained_bg_check.json          the gate's output
tools/diagnostics/gained_bg_check.py    new — A2's check on an arbitrary gained set, both
                                        background references, with a like-for-like band control
```

`stage1_8cam.png` is **not** consumed and remains exactly as Task 2 wrote it. No cloud call was
made, so nothing was spent.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The gate reads the two Task-2 dumps rather than re-deriving; the bound is the `--bg-max-pct` already in `project_twins` with its own source reasoning, not a number chosen here; A2's converter and estimator copied verbatim for comparability |
| ANDON_AUTHORITY | **3** | The gate fired and the session halted at it. Steps 2–4 untouched, no cloud spend, no atlas consumed. Reported with its evidence rather than tuned past |
| NAMED_COMPENSATORS | **2** | Nothing irreversible attempted. One new JSON written; undo is `rm`. The halt's whole purpose was to precede the irreversible part |
| DECOMPOSE_BY_SECRETS | **2** | The check is a separate tool from the pipeline it judges; the control view is a different view than the one gated |
| UNCERTAINTY_GATED_HUMANS | **3** | Three framings are presented with the measurement that supports each, and the one that reverses the conclusion (band-relative-to-own-interior) is given the same prominence as the one that confirms it. No framing chosen |
| EXTERNAL_VERIFIER | **1** | `skip:` — deterministic measurement. Both inherited claims in the ruling were independently checked against source rather than accepted |

---

**HALTED at step 1.** Nothing adopted, no threshold moved, no prompt written, no stroke run, no
credits spent. The atlas is intact and the three questions above are the ruling's.
