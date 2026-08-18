# E55 — report: can the plates we already paid for separate element COUNT from element IDENTITY?

**Executor seat, Opus, 2026-08-17. Spec: [E55-density-vs-identity-kickoff.md](E55-density-vs-identity-kickoff.md).**
Zero spend — no generation, no GPU, no cloud. Every number below comes from plates already on
disk. Working tree: `E:\AI\training\facet_E55\`.

---

## The answer, in one paragraph

**No. The corpus cannot separate count from identity as predictors, and the reason is
structural rather than statistical: there is not one element in it whose phrase is held
constant while the count around it varies *and* which is capable of being absent.** Every
element that can be absent changes its own naming somewhere on the ladder, and every element
whose phrase is held is supplied by the mesh, the control or the LoRA in all five arms
regardless of density. What the corpus *can* do is place a **one-sided bound**, and it does:
over a 70% rise in element count (10 → 17), **no element that was present at the low end went
absent at the high end**, while at *constant* count a change of identity moved the same
regions four times as far. The bound closes the "count destroys elements over this range"
direction. It does not close "count has no effect," and it says nothing above 17 elements —
the canon's own target is 19.

---

## 1. The corpus, enumerated

`E:\AI\training\facet_E08\` holds 16 arm directories. Enumerated complete with `find`, **only
three carry `w3clay_0_gen.json`** — the as-generated record — so the spec's "several" is three.

**Six plates exist at camera `w3clay_0` (752×1024). Five are distinct prompts; the sixth is a
replicate.**

| arm | plate | prompt provenance | tier |
|---|---|---|---|
| ARMOUR | `ARMOUR/w3clay_0.png` | `ARMOUR/w3clay_0_gen.json` `prompt` | **as-generated** |
| BRACER | `BRACER/w3clay_0.png` | `BRACER/w3clay_0_gen.json` `prompt` | **as-generated** |
| N11 | `N11/w3clay_0.png` | `N11/w3clay_0_gen.json` `prompt` | **as-generated** |
| SPEC | `SPEC/w3clay_0.png` | `docs/experiments/E08-spec-prompt.json` `w3clay_0` | committed-input |
| CONTRA | `CONTRA/w3clay_0.png` | `docs/experiments/E08-contradiction.json` `w3clay_0` | committed-input |
| ANCHOR | `ANCHOR/cloud_w3clay_0.png` | `docs/experiments/E08-anchor-workflow-api.json` `7.inputs.text` | committed-input |

**What is pinned across all six — sha256-checked, not assumed:**

- mask `8d62983b11a988870cefca6ea3eb6f607e9eea459f09f20aadc4ecfb6e948d5a` (identical in all)
- control `c158af80ef76b8ad7c6b422569bec0b8eb656b55480e05d329762e95e263c6e3` (identical in all)
- seed 770700, steps 20, cfg 2.5, denoise 0.92, lora_w 0.75, cn_strength 0.9
- figure 146,356 px = 19.006% of frame

**So the prompt is the only variable across the ladder.** That is unusually clean and it is why
this arc was worth running at all.

**The three as-generated arms carry their own provenance check.** Each `w3clay_0_gen.json` records an
`output_sha256`, and all three match the plate on disk (`d0220e24…`, `29b027b6…`, `8a26cee5…`).
SPEC and CONTRA have no such record, so their prompts are established from the committed input
they were told to read — a weaker tier, marked as such everywhere below.

### Arms excluded, and why

| excluded | reason |
|---|---|
| **ARMB** (8-view arm) | Its prompts are in `E08-armB-prompts.json`, but it has **no single-camera plate at `w3clay_0`** — its PNGs are sheets, holes maps and turnaround exports. Not comparable to the five, so not used. |
| **A2, A2R, A3, A4, BG, BG2, armA, gate0, LOOK** | Projection / keying / background / inspection arms. None is a prompt arm; several have no generation at all. |
| **ANCHOR as a density rung** | Its prompt is **byte-identical to N11's**. It is the same prompt on different hardware, so it is not a rung — it is used as the instrument's floor, which is the more valuable job. |
| **The second ANCHOR file** | `cloud_w3clay_0_mcptoolshop_lora.png` is **byte-identical** to `cloud_w3clay_0.png` (same sha256). One plate under two names, not two variants. |

### One provenance note the record should carry

`E08-twin-prompts.json` at HEAD holds the **BRACER** prompt in its `w3clay_0` key, while its own
`_armour_note` describes the **ARMOUR** prompt — the file was edited in place for the second
one-term test. Had this arc taken ARMOUR's prompt from that file it would have counted the wrong
prompt for the lowest rung. **Gate A is why it did not.**

---

## 2. Gate B — the element-counting rule, printed in full

Instrument: `tools/diagnostics/e55_prompt_elements.py` (new; tests at
`tests/test_t95_e55_prompt_elements.py`). Manifest: `facet_E55/arms_manifest.json`. Output:
`facet_E55/gateB_element_counts.json`.

```
RULE 1. prompt loaded from a PRIMARY artifact only (as-generated *_gen.json or committed
        input JSON); missing file or key raises, never inferred
RULE 2. split on commas -> prompt surfaces
RULE 3. split each surface on ' with ' -> element phrases
RULE 4. drop phrases on the declared style/framing stop-list
RULE 5. case-insensitive dedupe, first-seen order -> unique elements
        (same definition as canon_worksheet.density unique_elements)

STOP-LIST (12): at three-quarters; in profile; painterly visible brushstrokes;
painterly worked surface; plain flat grey background; plain grey background; seen from
behind; seen from directly behind; seen from the front; seen from the side;
visible brushstrokes; worked matte surface
```

Rule 5 is deliberately `canon_worksheet.density()`'s own definition of `unique_elements`
(distinct prompt-provenance phrases, case-insensitive, first-seen order) so an arm's count is
comparable with the canon's readout.

**Rule 3 exists for a measured reason.** `dark red layered cloth skirt with a leather belt` is a
skirt *and* a belt. A comma-only rule undercounts precisely the low-density arms, which would
have biased the very comparison this arc exists to serve. `test_t95` carries a can-fail leg for
it: under a comma-only implementation the leg returns 2 where it asserts 3, so it fails —
checked by monkeypatching `split_elements` to the identity function, not assumed.

**Stated limitation.** The rule counts a *phrase*, not an *attribute*. `a burly bald warrior` is
one element carrying two attributes; a prompt writing `a burly warrior, a bald head` scores two.
That is a real difference between the two prompts and the rule surfaces it — but it means a
count difference can come from re-phrasing as well as from adding an element, and §6 says
exactly where that bites.

### The density ladder

| arm | prompt surfaces | **unique elements** |
|---|---|---|
| ARMOUR | 11 | **10** |
| BRACER | 12 | **11** |
| N11 | 13 | **12** |
| ANCHOR | 13 | **12** *(replicate of N11)* |
| SPEC | 20 | **17** |
| CONTRA | 20 | **17** |

**The advisor's framing correction is confirmed at its source.** `canon_worksheet readout
--canon canon/w3.surfaces.json` returns `prompt_surfaces 24 / required_checks 25 /
unique_elements 19`. The comparison below uses element counts. **The corpus tops out at 17
against a canon target of 19 — it never reaches canon density.**

---

## 3. Gates

| gate | condition | result | evidence |
|---|---|---|---|
| **A** | every arm's prompt from a primary artifact, never a paraphrase | **HELD** | All six resolved; ARMB excluded for want of a comparable plate rather than a prompt. Gate A is enforced *in code* — `load_prompt` raises on a missing file, missing key or empty value; three `t95` legs pin it. |
| **B** | element count derived by one stated rule applied identically | **HELD** | Rule printed above and in every run's stdout; one code path over all six arms; `gateB_element_counts.json`. |
| **C** | the instrument reproduces a number the record already publishes | **HELD** | Re-ran `e08_contradiction.py` BRACER→N11 **before any new reading**. Whole-figure median ΔE **1.07** (published 1.07); figure **146,356 px / 19.01%**; N10 bracer base **rgb(65,39,26) C\* 18.5 h 50.4** — E53's published forearm figure. All 16 rows match `CONTRA/anchor_bracer_vs_n11.json` to the digit. Two independently published figures reproduced in one run. `facet_E55/gateC_bracer_vs_n11.json`. |
| **D** | writes confined to `facet_E55\` | **HELD** | Plus the three repo files this deliverable requires (this report, the instrument, its test). No `facet_E50`–`E54` tree was read. Nothing committed. |

**No gate fired.** Nothing was re-run with a changed parameter.

---

## 4. The instrument, and its calibration interval

**Reused, not commissioned.** `tools/diagnostics/e08_contradiction.py` already reports per-region
L\*a\*b\*, C\*, chroma-weighted circular-mean hue and CIE76 ΔE, draws its boxes on its sheet, and
intersects every box with the mesh silhouette. `docs/experiments/E08-contradiction-regions.json`
already defines **16 boxes over 14 distinct elements** in this exact camera's pixels, placed
before either image it was built for existed. Nothing about the reading needed a new tool.

Because the mask is byte-identical across all six arms and the boxes are fixed, **the px count in
every box is identical for every arm by construction** — smallest is N6 medallion at 340 px, all
16 clear the instrument's own ≥50 px rule on every arm.

### What the instrument reads when the answer is definitely no, and definitely yes

Both endpoints measured on **this** image family, before any arm was interpreted:

| | pair | Δ elements | whole-figure median ΔE |
|---|---|---|---|
| **FLOOR** — prompt did not change at all | N11 → ANCHOR (same prompt, different hardware) | 0 | **0.84** |
| **CEILING** — prompt changed and was obeyed | SPEC → CONTRA (same count, 11 attributes flipped) | 0 | **17.09** |

**Calibration interval: [0.84, 17.09].** A whole-figure reading outside it could not have been
right at any state of the world.

⚠ **The floor is a hardware floor, not a seed floor.** N11→ANCHOR is local-vs-cloud. The corpus
contains **no same-hardware, same-prompt, different-seed replicate**, so run-to-run variance at
fixed hardware is unmeasured and 0.84 may over- or under-state it. This is the single largest gap
in the arc and it cannot be closed without a generation.

### Presence calibration, for the gold that carries most of the named elements

| | measured on | C\* | hue |
|---|---|---|---|
| gold **definitely present** | N4R, N6, N12L/R, N15, N16 at SPEC, all named gold | **33.0 – 55.7** | **76.4 – 80.2** |
| gold **definitely absent** | the same six surfaces at CONTRA, named silver | **1.2 – 8.6** | undefined (below the chroma floor) |

A 3.8× gap separates the highest absent from the lowest present, on the same surfaces of the same
mesh. **Below C\* ≈ 5 the hue column is not a colour** — CONTRA's silver regions return hues of
238–334° that mean nothing, which is the repo's chroma-floor law behaving exactly as documented.
Hue is quoted below only where chroma supports it.

---

## 5. The measurements

### 5a. Pairwise, whole figure

| pair | Δ elements | median ΔE | position in [0.84, 17.09] |
|---|---|---|---|
| N11 → ANCHOR *(floor)* | 0 | 0.84 | 0% |
| BRACER → N11 | +1 | 1.07 | 1.4% |
| ARMOUR → BRACER | +1 | 1.60 | 4.7% |
| ARMOUR → N11 | +2 | 1.69 | 5.2% |
| N11 → SPEC | +5 | 3.38 | 15.6% |
| **ARMOUR → SPEC** *(widest count change available)* | **+7** | **4.26** | **21.0%** |
| **SPEC → CONTRA** *(identity flipped, count unchanged)* | **0** | **17.09** | **100%** |

**No slope is fitted.** Four distinct densities, one image each, no replication. The points are
reported as points.

The internal control behaves: the `held` class (elements not under test) moves 0.71 → 2.96 across
the count pairs and 6.23 at CONTRA, so some global drift accompanies every change and
per-element attribution is proportionally weaker at the wide end. At CONTRA the contradicted
regions move **7.4×** the held ones; across the count pairs the ratio is 1.8–2.8 against a floor
ratio of 1.4.

### 5b. Per-arm absolute region colour

Nine elements are named in **all five** arms: N1, N2, N3, N4, N7, N8, N12, N13, N14. **Five of
those nine are shown below** — the chromatic ones, since N1/N13/N14 are unassessable (§6) and N7
adds nothing the others do not. **The complete 16-box × 6-arm table is
`facet_E55/per_arm_regions.json`**; the claim in the next paragraph is made against all nine, not
against these five.

| region | ARMOUR 10 | BRACER 11 | N11 12 | SPEC 17 | CONTRA 17 |
|---|---|---|---|---|---|
| N2 beard | C 41.0 h 45.7 | C 42.2 h 47.4 | C 41.6 h 47.9 | C 44.1 h 46.6 | C 7.2 — |
| N3 tunic | C 11.0 h 175.7 | C 11.3 h 176.9 | C 11.6 h 178.4 | C 11.6 h 174.1 | C 40.2 h 297.0 |
| N4 pauldronR | C 38.8 h 79.6 | C 39.9 h 80.4 | C 40.2 h 80.2 | C 47.0 h 79.3 | C 1.9 — |
| N8 skirt red | C 21.6 h 13.5 | C 24.2 h 16.1 | C 23.2 h 15.1 | C 23.9 h 19.8 | C 0.7 — |
| N12 kneeR | C 25.3 h 76.8 | C 27.9 h 78.3 | C 28.3 h 77.9 | C 33.0 h 76.6 | C 8.6 h 71.9 |

**Not one of the nine drops as count rises 10 → 17.** Every chromatic one moves in the *same*
direction — up in chroma — and the largest gains are at the highest density. At CONTRA, at the
*same* count as SPEC, the same regions collapse to the achromatic band.

### 5c. The forearm — the element that never lands

`N10 bracer` box, the only region bearing on N11 (which has no box of its own):

| arm | count | N10 box | reads as |
|---|---|---|---|
| ARMOUR | 10 | C 13.9 h 54.0 | brown **fur cuff** — no bracer, no gold |
| BRACER | 11 | C 18.5 h 50.4 | brown **leather** bracer, no gold trim |
| N11 | 12 | C 19.1 h 50.7 | brown leather bracer, no gold plate |
| SPEC | 17 | C 20.7 h 53.4 | brown leather bracer, no gold plate |
| CONTRA | 17 | C 14.2 h 55.4 | brown leather bracer, no silver plate |

**The forearm never enters the gold band at any density.** C\* 13.9–20.7 sits below the
gold-present floor of 33.0, and hue 50–55° sits outside the gold hue band of 76–80° entirely —
that hue is the family of the scalp (46–48°) and the belt, i.e. skin and leather. N11 is absent
at counts 10, 11, 12, 17 and 17.

**And the same surface shows the opposite behaviour one element over.** Naming the *bracer*
(ARMOUR → BRACER, count 10 → 11) took the box from C\* 13.9 to 18.5 at ΔE 7.55 and replaced fur
with leather — visible on the strip. Naming a gold plate *on top of that bracer* produced ΔE 1.58
against a same-region floor of 0.92. One surface, two elements, adjacent rungs: one landed, one
did not.

---

## 6. The observation table

Unit = *(element, arm)*. **`U` (unassessable) is a real state, not a rounding of "no".**

`L` the declared material is on its surface · `D` named and not on its surface · `U`
unassessable · `(u)` present but **unnamed** in that arm

| element | ARMOUR 10 | BRACER 11 | N11 12 | SPEC 17 | CONTRA 17 | note |
|---|---|---|---|---|---|---|
| N1 bald head | U | U | U | U | U | mesh is bald; the colour test **cannot fail** |
| N2 beard | L | L | L | L | L | CONTRA: named white, landed white |
| N3 tunic | L | L | L | L | L | CONTRA: named blue, landed blue |
| N4 pauldrons ×2 | L | L | L | L | L | CONTRA: named silver, landed silver |
| N5 scrollwork | U | U | U | U | U | **no region exists** — one of only two headroom elements |
| N6 medallion | L (u) | L (u) | L (u) | L | L | present unnamed; ΔE 34.43 when named |
| N7 belt | L | L | L | L | L | |
| N8 skirt | L | L | L | L | L | |
| N9 kilt panels | L (u) | L (u) | L (u) | L | L | present unnamed; ΔE 34.66 when named. CONTRA named *grey*, landed C\* 9.1 — desaturated but above the measured grey band |
| N10 bracers | **D** (u) | **L** | **L** | **L** | **L** | **the only element that changes state on the ladder — and it changes when NAMED, not when count rises** |
| N11 forearm plate | **D** (u) | **D** | **D** | **D** | **D** | colour axis only; the *shape* question is **U** — no region isolates a plate |
| N12 knee plates ×2 | L | L | L | L | L | |
| N13 boots | U | U | U | U | U | dark achromatic named onto dark achromatic geometry — **cannot fail** |
| N14 greatsword | U | U | U | U | U | the control draws the sword; presence **cannot fail** |
| N15 crossguard | L (u) | L (u) | L (u) | L | L | present unnamed; ΔE 18.03 when named |
| N16 pommel | L (u) | L (u) | L (u) | L | L | present unnamed; ΔE 21.98 when named |

### The single sentence this table exists to support

**Zero elements in this corpus hold their phrase constant while the count around them varies
*and* are capable of being absent.** N10 is the only element that ever changes state, and it
changes at the rung where it is first *named* — so its change is attributable to naming, not to
density. Every other assessable element is present in all five arms at every density. That is why
the two factors cannot be separated here, and it is a property of the corpus rather than of the
measurement.

---

## 7. Predictions against outcomes

Pre-registered in `facet_E55/predictions.md` before any plate was opened. **Not blind, and the
disclosure is in that file**: I had read the spec's confound section (which argues one side on
purpose), `SPEC/PREDICTIONS.md` (a prior seat's by-eye presence scoring of the BRACER twin), and
the complete BRACER/N11 anchor table. I was blind to ARMOUR, SPEC, CONTRA and ANCHOR outcomes.

| # | predicted | measured | verdict |
|---|---|---|---|
| **P1** | **NO** separation possible | no separation; all three pre-registered falsifiers checked and **none fired** | **held** |
| P1-F1 | ≥4 of the nine always-named change state ARMOUR→SPEC would falsify | **0** changed | did not fire |
| P1-F2 | ≥4 absences among the lowest arm's own named elements would falsify | **0** | did not fire |
| P1-F3 | a byte-identical phrase present in one arm and absent in another would falsify | **0** | did not fire |
| **P2a** arms | 5 density + 1 replicate | 5 + 1 | **hit** |
| **P2b** regions | 16 boxes / 14 distinct elements | 16 / 14 | **hit** |
| **P2c** px ≥ 50 | 16/16 on every arm | 16/16 | **hit** |
| **P2d** measured cells | **70** (14 × 5) | **70** | **hit** |
| **P2e** headroom elements | band 1–3, point **1** | **1** changes state (N10); **1** constant-absent (N11) | **hit on the number, MISS on the identity** — I named N11 as the headroom element; the element that actually moves is **N10** |
| **P2f** informative cells | band 0–15, point **5** | **5** (N10 × 5 arms) | **hit**, with the caveat above |
| **P3** | 7 generations to settle it | unchanged — see §9 | not testable here |

### Misses, called as misses

1. **P2e named the wrong element.** I predicted the headroom would sit at N11 and it sits at N10.
   The *count* was right for a partly wrong reason, which is worth more as a warning than as a
   hit: N11 turns out to be constant-absent at every density (so it carries no variance at all),
   while N10 is the one element that actually moves. Had I only reported the number, this would
   have looked like a clean hit.

2. **My pre-registered arm counts were 9/10/11/17; Gate B's mechanical rule returns 10/11/12/17.**
   I had counted *canon-named* elements; the rule counts phrases, and `gold necklace` is a phrase
   but not a canon element. **The deltas are identical (+1, +1, +5)** so nothing downstream moves,
   but the absolute numbers in `predictions.md` are one low for the first three arms and the
   report's ladder supersedes them.

3. **A reading I nearly published and the measurement stopped.** From the numbers alone —
   N9 at C\* 11.2–11.8 h 167–170 unnamed, jumping to C\* 40.3 h 141.6 when named, ΔE 34.66 — I
   drafted the conclusion that the prior seat's by-eye "N9 PRESENT" call had been reading tunic
   colour rather than a distinct green panel, which would have overturned a premise of my own
   dispatch. **The strip shows that is wrong.** There is a visibly green pleated panel in all
   three unnamed arms. What naming changed was its *treatment* — dark and pleated becomes flat and
   saturated — not its presence. ΔE is a **response** measure and I read it for a moment as a
   **presence** measure, which is the exact substitution the spec's requirement 2 warns about. The
   advisor's confound statement about N9 stands as written.

---

## 8. Honest n

- **Measured cells: 70** (14 region-elements × 5 arms); 80 counting both boxes of N4 and N12.
- **Cells where an element could in principle register a drop: 55** (11 elements × 5); the other
  four elements (N1, N5, N13, N14) are unassessable in every arm.
- **Elements that ever change presence state across the whole ladder: 1** (N10).
- **Elements holding phrase constant while count varies *and* able to be absent: 0.**
- **Distinct densities: 4** (10, 11, 12, 17). **Images per density: 1.** No seed replication
  anywhere in the corpus.
- **Highest density available: 17. Canon target: 19.** The range above 17 is unmeasured.

**No slope is fitted to any of this.** With four densities at n = 1 and a binary per-cell outcome,
the cited ~8.53%-per-component effect on a continuous inclusion score is not resolvable even in
principle here — over the widest clean span it would predict ~17% of a continuous score, and a
single binary draw cannot show that.

### Which side the evidence closes

Stated before the numbers were read, per the repo's law on bounds:

- **Firmly closed:** *count, over 10 → 17 elements on this subject, did not remove any element
  that was present at 10.* A single absence at the high end would have shown it; there is none.
- **Not closed:** *count has no effect.* The whole-figure ΔE rises monotonically with Δcount
  (1.07 → 1.60 → 1.69 → 3.38 → 4.26), the largest count pair also changes phrasing and vocabulary,
  and nothing here reaches the canon's 19.
- **The comparison is between two ceilings, not two measurements.** ARMOUR→SPEC (4.26) is an
  *upper* bound on count because it also carries a full re-phrasing and five new elements;
  SPEC→CONTRA (17.09) is an *upper* bound on identity because it flips eleven attributes at once.
  Read as such: **the largest count perturbation the corpus can offer moves the figure 21% as far
  as a large identity perturbation at constant count.**

---

## 9. Sheets on disk

All under `E:\AI\training\facet_E55\sheets\`. Strips are cropped from the *same* boxes every
number above was read from, magnified ×5 **NEAREST** so every pixel shown is a native pixel
replicated rather than resampled; `montage.py` composites at `--scale 1` so it does not resample
either. Defects first.

| file | what it shows |
|---|---|
| `strip_N10_bracer.png` | **the one the Director's eye should reach first.** Five arms, the forearm. ARMOUR: brown fur cuff. BRACER: fur replaced by a seamed leather bracer, no gold. N11 / SPEC / CONTRA: same leather, no plate at any density. |
| `strip_N9_skirt_green.png` | Green kilt panel present and pleated in all three unnamed arms; flat and saturated at SPEC; navy at CONTRA where grey was named. |
| `strip_N12_kneeR.png` | Gold knee plate at every density 10 → 17, more saturated at 17; grey-brown at CONTRA where silver was named at the same count. |
| `sheet_density_ARMOUR_vs_SPEC.png` | Widest count change, `e08_contradiction.py --sheet`: labelled boxes, ΔE heat, hue×chroma density. |
| `sheet_identity_SPEC_vs_CONTRA.png` | Identity ceiling at constant count, same panels. |

⚠ `montage.py` prints a per-view brightness spread with a PASS/FAIL verdict. **That verdict is
its turnaround-lighting gate and has no meaning for this comparison** — it is not quoted anywhere
above and should be ignored on these strips.

**Reuse rather than an eighth sheet builder:** the compositing, labelling and readout are
`montage.py`'s; the ΔE sheets are `e08_contradiction.py`'s. `facet_E55/make_strips.py` only
crops.

---

## 10. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every arm's prompt is pulled from a named primary artifact by one code path, with the provenance tier constrained to an enum and a `t95` leg pinning that free text is refused. Control and mask are sha256-checked identical across all six arms; the three as-generated arms' recorded `output_sha256` match their plates on disk. Every command is in `handoff.md`; every output JSON is on disk. |
| ANDON_AUTHORITY | **3** | Four gates, all checked before the readings they protect; Gate C ran before any new number. The new instrument's checks `raise` (`FileNotFoundError` / `KeyError` / `ValueError`), never bare `assert`, so `-O` cannot delete them; the reused `e08_contradiction.py` already raises. |
| NAMED_COMPENSATORS | **3** | No irreversible call exists in this arc — no generation, no publish, no commit, no external write. Writes are confined to `facet_E55\` plus three repo files (this report, the instrument, its test), all uncommitted. Compensator: delete the tree and `git checkout` the three paths. Owner: the advisor. |
| DECOMPOSE_BY_SECRETS | **3** | Four separable pieces with one job each: prompt extraction + counting (`e55_prompt_elements.py`), regional colour (`e08_contradiction.py`, reused unchanged), cropping (`make_strips.py`), compositing (`montage.py`, reused unchanged). The thing that changes — the arm list — is data in `arms_manifest.json`, not code. |
| UNCERTAINTY_GATED_HUMANS | **3** | No pass condition, by the spec's design and this seat's agreement. Numerators and denominators are reported separately, the two ceilings are labelled as ceilings, the unassessable state is carried rather than collapsed, and the eye question is on a strip at the Director's zoom. Whether the canon's 25 stands is left entirely to him. |
| EXTERNAL_VERIFIER | **2** | Gate C forces agreement with two figures produced by different seats with a different instrument, and both reproduced to the digit. Scored **2, not 3**, because no second differently-sourced computation over the same pixels was run — the ΔE and the colour readout come from one code path, so a fault in `to_lab` would move every number here together and nothing in this arc would see it. |

---

## 11. Out of scope

- **Any generation.** Zero spend was a hard constraint; §9's minimal design is priced, not run.
- **Whether the canon should require 25 phrase checks.** The Director's. This arc supplies
  evidence for that decision and takes no position on it.
- **Whether any arm's output is good.** Not this seat's call at any point.
- **`canon_gate.py` and `canon_worksheet.py`.** Not touched — a second builder is live in them.
  `canon_worksheet.py` was *run* read-only for its density readout.
- **The canon schema, and the scope lists.** Untouched.
- **The `facet_E50`–`E54` working trees.** Not read.
- **Run-to-run variance at fixed hardware.** Unmeasured, and the corpus cannot measure it. This
  is the largest gap in the arc.
- **Density above 17 elements**, including the canon's own 19. No plate exists there.

---

## 12. Change-set left uncommitted for the advisor's fold

| path | what |
|---|---|
| `docs/experiments/E55-density-vs-identity-report.md` | this report |
| `tools/diagnostics/e55_prompt_elements.py` | new — Gate B counter, Gate A enforced in code |
| `tests/test_t95_e55_prompt_elements.py` | new — 11 tests, riding the tool in the same change-set |

`t95` was confirmed free by enumerating `tests/` complete at the start of this seat (93
entries, highest `test_t93_canon_worksheet.py`). **`t94` was free at that moment and is now
taken** — `tests/test_t94_fail_closed.py` appeared in the working tree during this session,
which is the outside channel claiming its reservation. No collision: this seat took `t95` and
touched nothing else. Several other paths are modified by live seats (`tools/canon_gate.py`,
`tools/restylize_views.py`, `tests/test_t91`/`t92` among them) and **none was touched here**.

All three new files are LF (`git ls-files --eol` reports `w/lf`; zero CR bytes at the byte
level), so the T6 line-endings pin holds when they are staged.

**T34 count surfaces:** this change-set **adds 1 test file and 11 tests** and touches no count
surface. The surfaces are the advisor's and are stated at 1295 / 1241 / 54; **this seat has
reconciled nothing**, per the standing rule that two live seats cannot both be green
independently.

Working tree `E:\AI\training\facet_E55\`: `handoff.md`, `predictions.md`, `arms_manifest.json`,
`make_strips.py`, `gateB_element_counts.json`, `gateC_bracer_vs_n11.json`, five `pair_*.json`,
`per_arm_regions.json`, `sheets/`.
