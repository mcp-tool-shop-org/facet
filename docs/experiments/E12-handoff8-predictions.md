# E12 handoff 8 — blind predictions

**Written BEFORE anything in this dispatch runs**: before the eight masks, before the frame
gate, before any control, before the palette JSON exists, before the gate has been pointed at
the accepted pair, and before a single twin exists anywhere. Committed first so nothing here
can be edited against a result.

## Blind status — disclosed precisely

This is the holding handoff-7 session, and it is **deeply non-blind to the pair**: it generated
both accepted views, built every handoff-6 crop of them, ran the handoff-7 clustering, and
knows the full cluster table, the band arithmetic and the strata by heart. It has also read
Ruling 15 including the 15c branch structure.

**What it has NOT seen and cannot have seen:**

- **Any twin. None exist** — this dispatch creates the first eight.
- Clay views **0, 2, 3, 4, 6, 7** — this seat has looked at `dragonclay_5` only.
- Silhouette masks for views 0, 3, 6, 7 (they are not on disk).
- Any control image for any view.
- **The gate's actual reading on the pair.** The cluster table is known; a *per-pixel* hue
  census under a band with a chroma floor is a different measurement and has never been run
  on this subject.

**So the P1 family below is informed** — I can see roughly where it must land from the cluster
table — **and everything about the twins is genuinely unknown.** Labelled accordingly.

---

## Q1 — the gate on the accepted pair, and which 15c branch fires

**P1a — the gate as constructed FIRES on the pair, on the membrane stratum. Branch 2.**
*(informed by the cluster table, not by any per-pixel run.)* The adopted band is warm-olive
85.4–147.3 with a C\* 12.0 floor. Of the pair's eight above-floor clusters, seven sit inside
that band and one does not: **rgb(74,79,97), h 283.4, C\* 12.9, 4.52% of the figure** — 8.19%
of view 5, 0.85% of view 1. That cluster is a large contiguous membrane field, so it cannot
present as speckle.

Quantified, so it can be wrong:

| | predicted off-palette, band as adopted | predicted largest blob |
|---|---|---|
| **view 5** | **6–14% of figure** | **> 10,000 px** |
| **view 1** | **0.5–4% of figure** | 500–8,000 px |

**P1b — after the realised-stratum allowance (273.4–293.4) the reading falls but does NOT go
to zero.** The cluster's *median* hue is 283.4; per-pixel hue spreads either side of a median,
and the allowance is only ±10° around a single point. Predicted post-allowance: **view 5 falls
to 0.5–4%, view 1 below 1%**, with the residual sitting at the stratum's edges rather than in
one field. **If the allowance takes either view to a flat 0, my model of the spread is wrong.**

**P1c — no OTHER firing on the pair.** No third hue family should appear above the floor: the
cluster table has none, and 40.25% of the figure carries no quotable hue at all. **If anything
fires outside the blue-violet family, that is the 15c halt branch and this dispatch stops
there with the evidence** — I predict it does not.

**P1d — the backdrop is not measured by the gate at all**, because the gate masks to the
geometry silhouette. Its h 297.8 is outside the allowance either way; stated so nobody reads
the 4.4° margin as a gate quantity. It is not one.

## Q2 — the instrument defect I expect to hit first

**P2a — `palette_gate.py` will RAISE on the galleon's own palette file.** Line 83 is
`MAXBLOB = int(PAL["gate"]["max_offpalette_blob_px"])`, and `canon/E04-galleon-palette.json`
sets that key to **`null` on purpose** ("both bounds are null ON PURPOSE"). `int(None)` is a
TypeError. The tool has a null path for `max_offpalette_pct` and **none for the blob bound**,
so it cannot read the precedent file this subject's palette is modelled on.

Predicted response if it fires: **prove the defect, then fix it in the shape the null-pct path
already has** — a null bound reports and gates nothing — **with the defect recorded in the
tool**, which is the practice Ruling 11e ratified. Not a new threshold, not a guessed number.
**If it does not raise, I have misread the code and will say so.**

**P2b — both beast gate bounds are written null**, per the galleon precedent and CLAUDE.md's
withdrawal rule. The percentage bound stays withdrawn (its denominator moves with camera angle;
figure area is fixed at 26.754% on this subject's eight views by the mirror-symmetry fact, but
the withdrawal reasoning is not about this subject). The blob bound has **no clean baseline
until these twins exist**, so inventing one now would be the fourth mis-specified condition in
this repo. Runs use `--report-only`; the gate reports numerator and denominator and the advisor
derives a bound later, from a baseline measured *before* the arm it judges.

## Q3 — the geometry legs

- **P3a — `silhouette_masks --anchor` on views 1 and 5 returns 0 differing px** against the
  masks already on disk, IoU 1.000000. The handoff-4 driver recorded exactly that; this is a
  re-check of a published figure before new masks are trusted.
- **P3b — all eight silhouettes measure 26.754% of frame, 490,941 px**, and the bboxes of view
  *v* and view *v+4* are exact mirrors. Reason, established at Ruling 9b: an orthographic
  silhouette from **d** and **−d** is the same ray set on this mesh, so the eight views are
  four mirror pairs. **If any view breaks 490,941 the mesh is not what the record says it is.**
- **P3c — frame agreement returns 0 differing px on all eight views** (bound 0, the ANCHOR 1c
  gate). A non-zero is a halt before any credit is spent.
- **P3d — control pixel counts:** views 1 and 5 reproduce **108,887** and **88,717 px**
  exactly, because the same tool at the same ruled canny on the same clay and mask is a
  deterministic function. The other six land in **60,000–130,000 px**, with the head-bearing
  views higher than the membrane-dominated ones (the 9d/F3b finding: view 1's Canny exceeded
  its contour, view 5's did not).

## Q4 — resemblance-bleed, per view, from the stems

Ruling 13d: **a colour term reaches structures that resemble the one it names.** The measured
instance is `pale ivory fangs and tooth rows` painting the *claws* ivory over `charcoal claws`
in the same string. The drop map puts the mouth family (incl. D10 fangs) off **{3,4,5}** and
the horn family off **{3,5}**. So:

| views | ivory words in the stem | predicted claws |
|---|---|---|
| **0, 1, 2, 6, 7** | `bone-ivory` ×2 + `pale ivory fangs and tooth rows` | **IVORY — the bleed recurs** |
| **4** | `bone-ivory` ×2, **no `pale ivory fangs`** | **CHARCOAL** — the resemblance source is the *fangs* term specifically |
| **3, 5** | none | **CHARCOAL** |

**View 4 is the discriminating case and it is the one to watch.** If view 4's claws come back
ivory, the bleed is driven by the *family mass* (`bone-ivory` ×2 is enough) rather than by the
fangs term, and Ruling 13d's named cheapest test — dropping the fangs term — would not fix it.
If view 4's claws come back charcoal, the fangs term is the source and that test is live.

**Predicted: view 4 lands CHARCOAL**, i.e. the fangs term is the source. Confidence: low. This
is the single most informative prediction in this file and I expect it to be the one that
teaches something either way.

## Q5 — the twins themselves

- **P5a — a garment-class invention appears on 0 or 1 of the eight.** W3's prior is one in
  eight; this subject has produced one such artifact in the record (the wing-rim serrations
  reading as a gaping mouth, 1 occurrence in 3 view-5 generations, handoff 5). **If one
  appears, the predicted site is a membrane trailing rim or the wing-body gap**, not a body
  surface — those are where the dense control draws structure the stem never named.
- **P5b — registration IoU lands in 0.970–0.995 per view**, and **below the companion's
  0.9940** on most views. Reason the constructions differ: the companion was a bust crop where
  the figure fills 61% of a square frame with a compact perimeter, while these are full-figure
  views whose silhouette includes membrane trailing edges, tail spines and claws — thin
  structure is almost all boundary, and a keying error there costs proportionally more IoU.
  **Predicted lowest on the membrane-dominated views (3 and 5), highest on the head-bearing
  ones.**
- **P5c — at most 2 of 8 need their bounded re-roll**, and I predict the triggers are gate
  firings on a membrane field rather than spec-visible material misses.
- **P5d — 0 credits on all eight**, `estimate_credits` verified before each rather than
  assumed.
- **P5e — the eight clean-twin off-palette readings land in the same order of magnitude as the
  accepted pair's post-allowance reading**, because the pair IS this subject's baseline and
  there is no other. Stated so that no twin is called dirty against a number from a different
  subject: **W3's 5–104 px clean scale and the galleon's 5,168 px / 1.622% are other subjects'
  data and are not this gate's baseline.**

## Q6 — what the gate cannot do, restated before it produces a number

Ruling 15d and the galleon's caveat: **the gate tests colour, not placement.** On this subject
that bites twice over — the ivory family is one cluster covering three declared elements plus a
known per-view deviation, and both dark bands are colour matches to *shadow*. **A twin can pass
every band while wearing a legal colour on the wrong structure.** Predicted consequence, stated
now: **if view 4's claws come back ivory, the gate will not flag it** — ivory sits at h 96.4,
squarely inside the adopted band. The sheets serve the eye and the eye rules.

---

## What would make this dispatch a full success while most of the above fails

If the gate fires on the pair somewhere the 15c branches did not anticipate, this session
**halts with the evidence and generates nothing** — and that is a full success, because a gate
that flags an accepted artifact is mis-constructed and finding that out before eight
generations is exactly what validating on the pair first is for. Equally, if the twins come
back with a per-view landing pattern that contradicts Q4's table, the resemblance mechanism is
not what Ruling 13d banked and the fixture consequence changes. A negative result is reported
plainly and stops.
