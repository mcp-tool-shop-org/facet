# E12 handoff 9 — blind predictions

**Written BEFORE anything in this dispatch runs**: before the v6 rebuild, before any upload or
submission, and before this seat has opened view 0 or view 4 at full size. Committed first so
nothing here can be edited against a result.

## Blind status — disclosed precisely, and it is mixed

This is the holding handoff-8 session. **It generated all eight twins.** What it has seen:

- Views 0 and 4 **at contact-sheet scale only** — 896 px wide in `TWINS_OVERVIEW.png`, a 2×
  downsample. At that scale I described view 0 as *"wings spread, ivory horns, orange eyes,
  green hide, olive belly, ivory claws"* and view 4 as *"symmetric, ivory horns visible over
  the back, charcoal claws, wings pale cream with grey."* **I did not identify the wing
  skeleton.** The Director did, from the same set. That is a calibration fact about
  contact-sheet reading and it belongs in the record.
- Their handoff-8 numbers, which I measured: view 0 — off-palette 69,587 px / 13.37%, blob
  12,913, membrane 20.1%, seam 6.1%, shoulder 61.5%, achromatic 55,069 / 10.58% with largest
  component 14,786, registration 0.982525, claw ivory:charcoal 0.51. View 4 — off-palette
  8,733 / 1.68%, blob 1,537, membrane 0.0%, seam 0.0%, **shoulder 99.9%**, achromatic 18,905 /
  3.63% with largest component 1,329, registration 0.986011, claw ratio **0.02**.
- Ruling 17e's account of the mechanism and its two pre-registered branches.

**What this seat has NOT done:** opened either view at full size, looked at any wing crop, or
measured anything about the wing arms and fingers specifically. **The defect I am predicting the
fix for is one I failed to see.**

---

## Pre-registered derivations, fixed before the builder runs

The corrected entry is **18 comma-terms** — `moss-green wing arms and finger struts` inserted at
index 2, immediately after the hide. The drop map is unchanged and names only the mouth family
({3,4,5}) and the horn family ({3,5}); the new term appears in neither, so it rides every view.

| | prediction |
|---|---|
| entry terms | **18** |
| per-view counts | **18 / 18 / 18 / 12 / 14 / 12 / 18 / 18**, `headclay_0` **16** — each exactly one more than v5 |
| full-string views | **0, 1, 2, 6, 7** — unchanged |
| v5 → v6 stem diff | **exactly one inserted term in every stem**, at index 2, with no other difference anywhere. Any other delta is an ANDON and halts the rebuild |
| controls and masks | reused byte-identical; the content-hash upload names must come back as handoff 8's — clay `e436c76c` / `bd620f8d`, control `8356377c` / `460488dc`. A different name means an input I believe unchanged has changed, and that is a halt |

---

## The works-perfectly test, before any result is read

**The seed is pinned at 770700 — the same seed the v5 twins ran.** So a term that does *nothing*
should reproduce v5 nearly exactly, and **any broad change IS the finding**. That is a much
sharper instrument than the usual re-roll comparison, and it cuts both ways: a fixed wing cannot
hide a broken flank, because a broken flank would also have to be a change from v5.

**Lands** → the wing arms and finger struts read moss-green against the membranes on both views,
and the whole-figure ivory mass falls. **Does nothing** → the A|B sheet is v5 modulo nothing, the
ivory mass is within ±10%, and the bat-anatomy prior has overridden a named term, which would be
the first time in this arc that naming a surface failed.

---

## The predictions

### P1 — the skeleton lands green

**P1a — the term claims the structure.** Confidence: **moderate-high**, and the reason is that
Ruling 17e measured the founding law in *both directions on one view*: view 4's wing **claws are
NAMED and stayed charcoal** while its **arm bones were unnamed and went ivory**. The surface was
unoccupied, so naming it should claim it — Amendment 15 forbids adding a second element to an
*occupied* surface, and this one had no owner.

**P1b — quantified, whole-figure ivory mass (ΔE < 20 to the pair's measured ivory cluster
rgb(224,212,169)), inside the geometry silhouette:** predicted to fall by **≥ 40%** on view 0 and
**≥ 40%** on view 4. *Does nothing* → within ±10%.

**P1c — the counterintuitive one, and I am registering it because 17d already recorded the
pattern: THE GATE NUMBER MAY RISE AS THE DEFECT LEAVES.** Ivory sits at h 96.4, **inside** the
adopted warm-olive band (85.4–147.3). D1's greens measure h 119–137 and the band's upper edge is
147.3, so hide green that lands past 147 is **outside** it. Turning a large ivory structure green
therefore moves mass from inside the band to its shoulder. **Predicted: view 0's off-palette
rises above 13.37% and view 4's rises above 1.68%, with the increase dominated by band
shoulder.** If instead both fall, my model of where the wing green lands is wrong.

### P2 — regressions, scored across every element

A changed prompt re-rolls every landing (the Ruling 12f law). Named branches, so none arrives as
a surprise:

- **P2a — the horns and crown keep their ivory.** This is the discriminating regression check:
  the new term is green and sits two positions from `bone-ivory curved horns`. **If the crown
  ivory on view 4 also leaves, the green term is over-claiming**, and the fix has traded one
  unnamed-surface error for a named-surface loss. Predicted: crown/horn ivory **holds**.
- **P2b — view 0's claws stay ivory** (ratio in 0.39–0.77) and **view 4's stay charcoal**
  (≤ 0.05). The fangs term is untouched, so 17c's channel should be unmoved; if the claws change,
  the new term is reaching structures it does not name and the resemblance channel is broader
  than 17c stated.
- **P2c — D2's olive-tan ventral, D6's charcoal spines and D8's eye hold** on both views.
- **P2d — the membranes stay inside 13e's accepted lit-translucency class** — slate through the
  leading fields, cream where the trailing half is lit. Predicted: no orange, no bone-ivory.

### P3 — the achromatic channel (17d, now permanent)

Predicted both views stay inside the accepted pair's own band and well clear of view 3A's
anomaly: **view 0 within 8–14%** (was 10.58%) with largest component **under 20,000** (was
14,786); **view 4 within 2–6%** (was 3.63%) with largest component **under 5,000** (was 1,329).
A new flat-black mass on either view would be the seed-class defect handoff 8 measured, and it
would consume that view's bounded re-roll.

### P4 — registration

Predicted **0.975–0.990** on both, i.e. unchanged from v5's 0.9825 / 0.9860 within noise, because
the control, the mask and the seed are all pinned and only the prompt moves. A registration shift
of more than ±0.005 would mean a prompt term changed the silhouette, which would be a finding
about the control's authority rather than about the wing.

### P5 — process

- **P5a** — the four uploads return handoff 8's content-hash names. Free confirmation.
- **P5b** — **0 credits**, `estimate_credits` before each of the two submissions.
- **P5c** — **0 re-rolls needed.** Confidence: moderate. The likeliest consumer is a new
  achromatic mass of the view-3A kind, which is a seed lottery and unrelated to the term.
- **P5d** — the builder's subsequence assertions pass and the exact-one-term diff holds on all
  eight stems.

---

## What would make this dispatch a full success while P1 fails

If the skeleton comes back ivory under a term that names it moss-green, that is the **more
informative** outcome: it would mean the realistic register's bat-anatomy prior can override an
explicit named term on this structure, which no result in this arc has yet shown — every prior
failure was an *unnamed* surface taking a neighbour's colour. It would move the fix from the
prompt to the arm/fixture layer and it would be the first measured limit on "identity rides the
prompt." Reported plainly, with the anatomy-prior hypothesis attached, and stopped there.
