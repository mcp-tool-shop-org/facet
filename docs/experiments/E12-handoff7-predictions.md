# E12 handoff 7 — blind predictions

**Written BEFORE the first measurement of this dispatch**: before any clustering, any hue
census, any backdrop estimate, any per-element ΔE, and before the corrected expected triples
below are compared against anything. Committed first so nothing here can be edited against a
result.

## Blind status — disclosed precisely, because this seat is NOT fresh

This is the holding handoff-6 session. **It generated the accepted pair and has looked at it at
length.** What it has already seen, and is therefore NOT blind to:

- Both accepted outputs at full size, and every crop it built: legs, tail underside, wing arms,
  membranes and wing-rim on view 5; legs, tail underside, wing arms, head, crown spikes and
  cheek fan on view 1; both feet crops; the same-seed A/B and the three-way progression.
- Its own handoff-6 pale-family numbers per region — so the *qualitative* colour of every large
  surface is an observed fact to this seat, not a prediction.
- The **rejected** pair's landing table and bands, read this session from
  [E12-task45-report.md](E12-task45-report.md): warm-green 95.6–137.5 holding **81.61%**, wine
  344.6 holding **0.50%**, forbidden span **278.1° (77.3%)**, below-floor share **17.90%**,
  realised backdrop rgb(188,183,202) scoring **0.2353**, asked rgb(121,121,172), W3's grey
  0.0745. And the galleon's: warm 62–88 / 73.6%, blue 283–301 / 3.69%, forbidden 288° (80.0%).

**What this seat has NOT done and is blind to:** it has never clustered the accepted pair, and
does not know its cluster table, any per-element ΔE, its hue census, its realised backdrop
triple, its below-floor share, or its forbidden span. Every number predicted below is unmeasured
on this artifact.

**Two of the predictions are contaminated by that history and are labelled so** — Q1's
"collapse recurs" and Q3's per-element band/contest split are informed by having seen the
image. They are still registered, because a prediction that is easy is still falsifiable, and
because the *numbers* are not known.

---

## Pre-registered INPUT — the corrected expected triples, estimated from the WORDS

`canon/dragon-materials-estimated.json` carries the **pre-correction** palette for D2, D6 and
D7. The landing table needs an expected triple per element, so three are estimated here in the
same convention that file used — *a plain reading of the fixture's colour word* — and **fixed
before any measurement**, so they cannot be nudged toward whatever the pair turns out to hold.
**No canon or profile file is edited**; the corrected table is written as a NEW file in this
dispatch's output tree and the advisor may fold it wherever it belongs.

| id | fixture word (corrected) | estimated sRGB | L\* | C\* | h |
|---|---|---|---|---|---|
| D2 | `pale olive-tan ventral plates` | **rgb(191,180,133)** | 73.2 | 25.7 | 97.5 |
| D6 | `charcoal dorsal and tail spines` | **rgb(60,60,58)** | 25.3 | 1.3 | *undefined* |
| D7 | `charcoal claws` | **rgb(60,60,58)** | 25.3 | 1.3 | *undefined* |

Reasoning, stated so it can be disputed: *olive-tan* is the old *bone-tan* pulled greener and
slightly darker — ΔE 8.28 from rgb(206,188,154), enough that the two are separable if the pair
distinguishes them. *Charcoal* is read as a plain very dark near-neutral; its hue value of
109.9° is printed nowhere because at C\* 1.3 hue is not a colour. D1, D3, D4, D5, D8, D9, D10,
D11 keep the existing file's triples unchanged.

**A pre-registered LIMIT of the instrument, not a finding:** the charcoal estimate sits
**ΔE 5.86 from D11's slate** rgb(52,56,62). Two declared elements whose expected triples are
that close **cannot be told apart by a nearest-cluster table.** D6/D7 landing correctly and
D11 landing correctly will produce the same row. This is the galleon's *four elements share one
cluster* caveat, sharpened, and it is stated **before** the table is run so that no row is read
as evidence it cannot carry.

---

## The works-perfectly test, before any result is read

**Q1 (collapse).** Recurs → one contiguous hue group above the chroma floor holding most of the
above-floor mass, group width under ~60°. Does not recur → two or more separated groups of
comparable share, or a group wider than ~90°. Different, both observable.

**Q2 (backdrop).** The measurement can return *the backdrop is closer to a material than the
0.06 cut* (a regression, which is what the galleon's 4d found) or *it is several times clear*.
The galleon returned 0.1000 and the rejected beast pair 0.2353 on the same instrument, so it is
known to separate these states.

**Q3 (bands).** An element bands cleanly → a cluster sits near its expected triple, above the
chroma floor, with enough share to fix an edge. It is contested → two views disagree, or its
mass sits below the floor where hue is undefined, or its share is too thin to fix an edge. The
correct output in the second case is **numerator and denominator with no band**, not a band
with a caveat.

**Q4 (D8).** Present → a connected ember-orange blob inside the head region on view 1. Absent →
no such pixels. The rejected pair returned 153 px at ΔE < 15 in one blob at a known location,
so the instrument is known to find one when there is one.

---

## The predictions

### Q1 — the H1/H4 collapse

**P1a — the collapse RECURS** *(contaminated: this seat has seen the pair)*. One contiguous
warm/olive-green group above the C\* 12 floor, **group width ≤ 60°**, holding **≥ 55%** of the
figure. The register changed and the palette changed; the *subject* did not, and a green-hided
animal with a warm-pale belly under a realistic register has no reason to spread.

**P1b — but the above-floor share FALLS, and the below-floor share RISES above 17.90%.**
Predicted below-floor **20–40%** of the figure. Reasoning: the correction replaced two
*chromatic pale* terms with **charcoal**, a near-neutral that must land below the floor if it
landed at all, and it joins D11's slate and D3's near-neutral membranes down there.

**P1c — the forbidden span is ≥ the rejected pair's 278.1°.** Predicted **275–310°**. If the
wine cluster fails to survive the 0.4% cluster floor this time, only one band remains and the
span goes to the top of that range. Named branch: a wider-than-expected single group, or a
third group from the membrane's pale field, would push it down instead.

**P1d — H4 again: 0 or 1 clusters exceed ΔE 25 from every declared element.** The rejected pair
returned zero, the galleon had extras. **Named branch, and it is the one to watch: if one
exceeds, it is the membrane's lit pale-cream trailing field**, because no declared element in
this fixture is a pale cream — D3 is `storm-grey`. That is the 13e gradient showing up in the
cluster table rather than at the eye.

### Q2 — the backdrop, re-measured under the accepted register

**P2a — the realised backdrop is again much lighter and far less chromatic than the asked
rgb(121,121,172).** Predicted **L\* 70–80, C\* 8–14, hue 290–310** — the ask→realise transfer
that Ruling 8's sidecar measured (L\* 52.6 → 75.3, C\* 29.58 → 10.44, hue surviving at 301.0)
is a property of the word and the model, and neither changed.

**P2b — min-distance to the measured clusters lands in 0.20–0.28**, i.e. near the rejected
pair's 0.2353 and **well clear of the 0.06 cut** — no regression of the galleon's kind. The
*direction* against 0.2353 is genuinely uncertain and is not predicted: the pale-bone mass that
used to sit nearest is gone, but the membrane's lit pale field is still there.

**P2c — W3's inherited grey scores under or near the 0.06 cut again**, predicted 0.05–0.09,
corroborating Ruling 8b on a second artifact.

**P2d — a method note registered as a prediction.** `e04_bands.py` estimates the backdrop by
**corner median** (two 8×8 corner patches). CLAUDE.md retires corner-median *keying*; this is
*sampling*, a different use, but it carries the same flat-field assumption. **Both estimates
will be reported** — the corner median, which is what the 0.2353 and 0.1000 figures were
computed with and therefore the only comparable one, and a full outside-silhouette estimate.
**Predicted: they agree within ΔE 3.** If they do not, the recorded figures are measuring a
corner rather than a backdrop and that is a finding.

### Q3 — which elements band, which are contested

*(contaminated on the qualitative split; the numbers are not known)*

| element | predicted |
|---|---|
| **D1** hide | **bands cleanly** — largest or near-largest cluster, ≥ 10% share, above floor |
| **D2** olive-tan | **bands cleanly** — above floor, warm hue, and predicted to land nearer my olive-tan estimate than the superseded bone-tan one. If it lands nearer bone-tan, my estimate was the wrong reading of the word and that is my error, not the pair's |
| **D3** membranes | **SUSPENDED, with strata** — predicted to produce two clusters (a slate upper/leading field and a pale-cream lit trailing field), at least one below the chroma floor. Predicted **no single point band is honest**, exactly as 13e anticipated |
| **D4** horns | bands with the ivory family |
| **D5** crown/cheek | **CONTESTED — no band**, per the dispatch. Predicted the *crown* spikes carry ivory and the *cheek fan* does not; both reported per-region |
| **D6** spines | lands, and **below the chroma floor → no hue band is possible.** L\* and C\* reported instead |
| **D7** claws | **CONTESTED — no band**, per the dispatch. View 1 ivory, view 5 charcoal, both reported |
| **D8** eyes | **no numeric gate**, ever (G7 lesson). Task 2 |
| **D9** tongue | **no numeric gate.** Its cluster predicted to survive at 0.2–0.7% share; if it does, any wine band remains suspendable on one thin cluster, as both predecessors' thin bands were |
| **D10** fangs | bands with the ivory family |
| **D11** slate | **below the chroma floor** again, no hue band |

**P3a — the ivory-family merge question resolves as MERGE.** D4, D5's crown and D10 predicted
to share **one** cluster, as D4/D5/D6/D7/D10 did on the rejected pair. **And the named
consequence, registered before the table exists: view 1's ivory foot claws — the D7 deviation —
will land in that same ivory cluster, so the landing table cannot distinguish the deviation
from a correct D10 landing.** The deviation is only visible in the per-region numbers and at the
eye. Any reader who takes a clean D7 row as evidence the claws are fine has been misled by an
instrument doing what it does.

**P3b — chroma floors.** Charcoal (D6, and D7 on view 5) and slate (D11) predicted **C\* < 12**;
wine (D9) predicted **C\* 12–25**, above the floor; the ivory family predicted **C\* 12–22**,
above it. The floor stays at **12.0, inherited from W3**, and is not moved — this subject has
no measurement that would justify a different one, which was the rejected pair's finding too.

### Q4 — the D8 closure

**P4a — the ember-orange eye is present on view 1**, in **one** connected blob, **100% inside
the head region**, at **100–400 px** at ΔE < 25, i.e. **0.02–0.08% of the figure**.

**P4b — the cluster table returns NOT FOUND for D8 again**, because 0.02–0.08% is below the
0.4% cluster floor. **That is the instrument being blind by construction, pre-registered since
handoff 2, and it must not be read as a miss.** Both facts go in the closure.

**P4c — the closure carries the 12g contradiction rather than resolving it**: this eye landed at
pair scale under the ruled canny, and the bust-scale companion painted **no** eye at ~33× the
pixels under the same dense control. Predicted: nothing measured here explains that, and nothing
should be claimed to.

### Q5 — process

- **P5a** — no generation, no GPU, no credits, no Blender. Watchdog reported if any render leg
  becomes necessary; none is expected.
- **P5b** — **the instrument reproduces its published figures before any new number is read
  from it**: the galleon's warm 62–88 / 73.6%, blue 283–291 / 3.69%, forbidden 288°, and the
  rejected beast pair's warm-green 95.6–137.5 / 81.61%, wine 344.6 / 0.50%, forbidden 278.1°,
  backdrop rgb(188,183,202) at 0.2353. Predicted: **both reproduce exactly.** If either does
  not, no new band is proposed this session and that is the result.

---

## What would make this dispatch a full success while most of the above fails

If the bands cannot be honestly derived — if D3 will not band, if the contested elements
swallow the ivory family, if the collapse leaves the gate with one narrow group and nothing to
separate — then **the deliverable is the suspension**, reported as numerator and denominator,
and the advisor rules with the numbers in hand. Ruling 14 already put the contested dispositions
on this measurement rather than on inference. Inventing a band this data cannot support would be
the one move that is always wrong here, and the fourth mis-specified condition in this repo's
record.
