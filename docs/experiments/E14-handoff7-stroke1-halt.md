# E14 handoff 7 — stroke 1 misbound TWICE. Ruling 24i's HALT branch fires.

**Executor session, 2026-08-08.** Ruling 24l (`311257c`) landed the fixture row; the lane
resumed at stroke 1's graph build and stopped at the branch Ruling 24i pre-registered.

> **24i:** *"THE BRANCH: if the gem region misbinds twice at stroke 1, HALT — the term
> question returns to this ruling's table with both artifacts, the demotion's compensator
> standing ready. Nothing improvises past it."*

**It misbound twice. Nothing committed, nothing improvised, the re-roll is spent, both
artifacts preserved under name. 0 credits, quoted at both submissions.**

---

## 1. THE WALK, in plain words, before any number

**The fixture panel (the identity).** A faceted polyhedral gem: a pointed kite silhouette
with a thin silver bezel outlining its edges, distinct flat facets catching light
separately, the stone near-black at the rim with a deep garnet-red interior and one white
highlight on the upper-left facet.

**The BEFORE panel (the demoted stage-1b context).** The same faceted kite, the same bezel,
the same facet planes — coloured violet with magenta flashes on the left flank. Black
speckles are the demoted hole texels rendering at hole-grey. **The form is right and the
colour is wrong: that is precisely the defect the repaint exists to fix.**

**ROLL 1, seed 770700.** The stone is **no longer faceted**. The kite silhouette has
collapsed into a rounded polygon carrying a thick grey metal rim, and inside it sits a
**flat, smooth disc of solid deep red** — a cabochon in a bezel setting. The colour is
right. The form is gone.

**ROLL 2, seed 770702 (the bounded re-roll).** The same cabochon-in-a-mount recomposition —
a smooth domed oval inside a grey rim, no facets — and the stone has gone back to
**magenta-pink**. Both clauses fail.

**Everything else on the frame is correct in both rolls**: the oxblood wrap, the gold collar
and mid-ring, the blackened iron crossguard, the gold boss, the worn steel blade. The blade
rim's holes filled with continuous steel.

## 2. The measurement, on the stone alone

⚠ **The first cut of this measurement was contaminated and is corrected here rather than
dropped.** I measured the gem watch band (rows 87–158) and it returned median hue 71.5 on
the *fixture* — the gold band — because that row band is the pommel **assembly** and
contains the collar ring. That is handoff 5's own recorded bug arriving in a new form (its
first landmark walked past the collar to the grip neck). The stone is isolated here **by
construction** instead: the pixels the demotion newly added to the job mask ARE the
drifted-owned stone territory, 1,420 px, rows 97–139, cols 95–144.

| panel | median hue | C\* med | L\* med | wine 332–25 | lav+mag 290–332 | above floor |
|---|---|---|---|---|---|---|
| **FIXTURE twin — the identity** | **17.0** | 16.7 | 5.7 | 80.4% | 4.8% | 189 |
| BEFORE — the demoted drift | 316.7 | 18.8 | 8.0 | 58.5% | 32.9% | 258 |
| **ROLL 1 — seed 770700** | **23.7** | 26.4 | 7.5 | 56.6% | **6.2%** | 470 |
| **ROLL 2 — seed 770702** | **323.9** | 29.2 | 21.0 | 73.5% | **26.5%** | 597 |

**Roll 1's colour landed.** Median hue 23.7 sits beside the fixture's 17.0, and
lavender+magenta collapses to 6.2% against the drift's 32.9% and the fixture's 4.8%.

**Roll 2's colour did not.** Median hue 323.9 is back in the drifted range. *(Its 73.5%
"wine" reads high because the band edge is 332 and roll 2's mass sits right on it — the
median is the honest read, and 323.9 is magenta. The percentage and the median disagree in
emphasis and the disagreement is the band edge, not the stone.)*

**The red-outside-L5 watch is CLEAN on both rolls.** Above-floor pixels on the figure
outside the stone *fell* in both rolls (5,018 → 4,662 → 4,566); the wine-band share there is
the oxblood wrap, which owns that band legitimately, and no new red mass appeared on blade,
guard, boss or rings. **The fifth signature is absent** — the filled blade rim is continuous
steel, not dark desaturated crevice fill. **The 20b guard watch is clean** — the crossguard
is unchanged at both seeds, no figurative form.

## 3. What the two rolls say, separated

**(a) The misbind is a FORM misbind and it is seed-independent.** Both seeds recompose the
same way: *a faceted polyhedral gemstone becomes a smooth cabochon in a metal bezel
setting*. The facet planes are MESH-SUPPLIED — they arrive through the control from geometry
— and the inpaint overwrote them at both seeds. This is Ruling 20b's class exactly, at a new
site: **anatomy misbinding seeded by the control's own features.** The gem's kite silhouette
with its thin bright rim matches a *jewel-in-a-ring-setting* template better than it matches
a raw faceted stone, the same way the mid-grip ring's thin horizontal edge matched a
crossguard template better than the true guard's edge-on blob. A control can be obeyed and
still recompose the object when its features resemble the wrong parts — twice now, on the
same subject, at two different structures.

**(b) The term worked, and the colour is still seed-borne.** `a deep red garnet gem pommel`
put deep red on the stone and nowhere else at 770700, and did not at 770702. **The term
change did not remove the seed dependence** — which is Ruling 19b's twin-stage finding
reproducing at the brush stage, on the same seed pair that produced it. 770700 is the garnet
seed at the twin and the red-landing seed at the brush; that is consistent and it
strengthens 19b rather than overturning it.

**(c) The two failures are not the same failure**, and the ruling's table needs both:
roll 1 = form only; roll 2 = form and colour. A third roll is not authorised and none ran.

## 4. What has NOT been done

- **Nothing committed.** `run/state/atlas.png` is **byte-identical** to `state0/atlas.png`
  (`69f61f32a3e2…`); no `atlas.prev.png` exists, which is a commit artifact. The state is
  the demoted state exactly: styled 1,588,943, holes 2,072,960.
- **No third roll.** The one bounded re-roll is spent, on the eye clause, at the ruled seed.
- **Stroke 2 did not launch.** The ruled order stopped at its first gate.
- **Both rejections preserved under name** in `run/rejected/` with their graphs, plus the
  two-roll gate sheet.
- **0 credits**, quoted by `estimate_credits` before each of the two submissions
  (*"0 credits — no paid API nodes found in this workflow"*); GPU/queue time excluded.
- No profile, fixture or palette edit. No memory-store write. No gate armed.

## 5. The two submissions, for the record

| roll | seed | prompt_id | invariance ANDON | eye gate |
|---|---|---|---|---|
| 1 | 770700 | `03f6b148-0bb4-49c4-987a-0541b0adc73d` | **PASS** — mean 0.050 lv, largest hot component 48 px | **REJECTED — form** |
| 2 | 770702 | `836fabfe-083f-4aa9-bf79-20a9be5f839c` | **PASS** — mean 0.054 lv, largest hot component 5 px | **REJECTED — form + colour** |

Both graphs passed the full pre-flight: five recipe values against the cleared block, the
inverted no-LoRA scan (16 nodes, no loader, no card reference, `ModelSamplingAuraFlow`
reading the UNET directly), lane corroboration, prompt/negative provenance. Roll 2's
pre-flight printed the seed deviation loudly as a recorded per-invocation argument, which is
the guard working as written. Link topology checked in code before submission — no
self-links, no dangling targets (the E04 Arm G7 trap).

## 6. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Both submitted workflow JSONs saved before submission and preserved with their rejected artifacts; cloud input names carried into the saved graph so the file IS the submitted recipe (Amendment 30); prompt_ids recorded |
| ANDON_AUTHORITY | **3** | Ruling 24i's pre-registered branch fired and the lane stopped; the invariance ANDON ran on both rolls; the contaminated first measurement was caught and corrected before it was reported; no third roll, no commit, no stroke 2 |
| NAMED_COMPENSATORS | **3** | Nothing irreversible: the atlas is byte-identical to the pre-demotion state and the demotion's compensator is standing, exercised and unused. 0 credits at both submissions |
| DECOMPOSE_BY_SECRETS | **3** | The two failure clauses are separated (form vs colour) and reported as different findings; the stone is isolated by the demotion's own footprint rather than by a row band that contains the collar |
| UNCERTAINTY_GATED_HUMANS | **3** | The walk is stated in plain words before any number; the halt goes up with both artifacts and both readings; nothing about what to do next is decided here |
| EXTERNAL_VERIFIER | **2** | The invariance ANDON is a different tool from the one that generated; the colour measurement uses the band instruments against the fixture panel as its reference, not the brush's own output. `skip:` per precedent |

---

## HALT — stroke 1, two misbinds, the branch fired

`E:\AI\training\facet_next\E14_strokes\run\`:

```
state/                          the DEMOTED state, atlas byte-identical to state0, nothing committed
state/job_y+000_e+00/           render · mask · hit · cam · inpainted_s770700 · inpainted_s770702
graphs/stroke1_y000.json        the roll-1 recipe as submitted
graphs/stroke1_y000_s770702.json the roll-2 recipe as submitted
rejected/                       both rolls, both graphs, the gate sheet
gates/GATE1_gem_6x.png · GATE1_frame.png · GATE1_both_rolls_6x.png
```

**What returns to the ruling's table, with both artifacts:**

1. **⚠ The misbind is FORM, not colour, and it is seed-independent.** The mesh's faceted
   polyhedral gem is recomposed as a cabochon in a bezel at both seeds. Ruling 20b's class at
   a second structure on the same subject — a control obeyed and the object still recomposed,
   because the stone's own silhouette resembles a jewel setting. **The term question is not
   what stroke 1 answered.**

2. **The term itself worked, once.** `a deep red garnet gem pommel` landed deep red on the
   stone and nowhere else at 770700 (median hue 23.7 against the fixture's 17.0, lav+mag 6.2%
   against the drift's 32.9%) and reverted at 770702. **19b's seed finding reproduces at the
   brush stage**; the term change did not remove it.

3. **The demotion is intact and reversible.** Its compensator is exercised and standing; the
   atlas has not moved a byte. Whatever the ruling decides — a different mask, a different
   term, a different camera to open on, or the stone left to a later stage — the state is
   exactly where the ruling put it.
