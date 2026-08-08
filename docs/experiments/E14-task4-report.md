# E14 Task 4 — the styled target pair. HALT: the advisor's eye, then the Director beside the clay.

**Executor session, 2026-08-07.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 11c.
Pre-registration committed in `98af737` ([E14-task4-prereg.md](E14-task4-prereg.md)) before
the twin-prompts file was built, before any control was built through the ruled pair, and
before any submission. Sidecar written at birth:
[E14-task4-pair-sidecar.md](E14-task4-pair-sidecar.md).

**This report judges nothing.** It records what was built, what was measured, one artifact
rejected against a rule written before it existed, and the observations the two decisions in
front of the advisor need. **The Director's gate is on the artifacts, at his zoom, beside the
clay.**

**Cost: 0 credits.** `estimate_credits` returned *"no paid API nodes found in this workflow"*
on all three submissions — the graph is entirely OSS models (Qwen UNET / CLIP / VAE +
InstantX ControlNet-Union), so this is GPU time on the subscription, not metered API spend.
Quoted per submission as the dispatch requires.

---

## 1. The one-string-vs-per-view check — VERIFIED per view, not imported

The profile's note said this subject *appears* to pass the ship's one-string premise and
required verification against the actual renders. Checked at 3× across all eight profile
renders (`ONESTRING_hilt_strip.png`) and at 8× on the crossing
(`ONESTRING_crossing_8x.png`), by eye, this session.

| element | reads on every yaw? | note |
|---|---|---|
| L1 battle-worn steel blade | **yes** | a sliver on 2/6, but present — "slivers of something" |
| L2 blackened iron crossguard | **yes** | quillons seen end-on at 2/6, a compact block, present |
| **L3 gold diamond boss at the crossing** | **NO — absent on views 2 and 6** | it is a plate on the guard **face**; edge-on it is subsumed into the guard's own silhouette. Unambiguous at 8× |
| L4 oxblood leather grip wrap | **yes** | narrower at 2/6, coil turns and collars still read |
| L5 dark garnet gem pommel | **yes** | a faceted polyhedron reads at close to full width from every yaw |

**The premise FAILS on this subject — narrowly: one element, two views.** Four of five see
slivers; the fifth sees nothing of something. The profile's "slivers of everything, not
nothing of something" is right for four elements and wrong for the fifth. Same shape as the
beast's failure (E12 Ruling 9d), far smaller magnitude.

**W1 held exactly**, and the carried Gate-0 flag was half right in a way that mattered. The
flag said views 2/6 render *"the gem and boss"* at near-nothing. Verified: **the boss is
absent; the gem is present on all eight and is one of the clearest elements edge-on.**
Importing the flag would have dropped a term naming an element that IS visible — which is
precisely why the profile said verify rather than import.

The builder was run with one drop:

```
e12_make_twin_prompts.py --profile profiles/prop.json --tag swordclay
    --drop "a gold diamond boss at the crossing:2,6"  --version 1
  swordclay_0  10 terms  FULL (byte-equal to entry)     <- the pair's view
  swordclay_1  10 terms  FULL (byte-equal to entry)     <- the pair's view
  swordclay_2   9 terms
  swordclay_6   9 terms
  all stems asserted ordered subsequences; 6 full-string views byte-equal
```

**L3's collar rings are not dropped** — they are on L3's surface list and ARE visible on 2/6.
The drop removes the term naming the boss, not the gold family.

## 2. The controls, through the ruled pair

```
restylize_views.py --profile profiles/prop.json --emit-only  (12 profile values applied)
```

| view | control px | canny | contour | at 0.40/0.80 (the falsified pair) |
|---|---|---|---|---|
| **0** | **11,322** | **8,695** | 4,776 | 7,885 |
| **1** | **10,710** | **8,230** | 4,516 | 6,883 |

**The canny counts reproduce the ruled ladder row exactly** — 8,695 / 8,230 / 5,580 / 8,400 /
9,509 / 8,508 / 5,230 / 7,870 across all eight views, byte-for-byte the 0.10/0.25 row of the
derivation Ruling 6 ruled on. The control the generator actually received is the one the
ruling saw. Constraint is up **43.6%** on view 0 and **55.6%** on view 1 against the falsified
pair.

## 3. The cloud leg

Graphs built by the committed `e12_pair_cloud_step.py`, **saved to disk before submission**,
each pre-flighted in code:

```
[pre-flight] PASS against prop.json: six recipe values equal the decided block;
             --prompts IS _fixtures.twin_prompts and the graph's strings are that file's;
             17 links resolve, no self-link, no dangling target, no orphan.
[graph]      lora NONE - no loader node in the graph (E12 Ruling 10b);
             ModelSamplingAuraFlow reads the UNET directly
```

**The no-LoRA pre-flight is inverted by construction** — it scans every node for the class
family and for the recorded card name in any input, because a no-LoRA run fails by a LoRA node
*surviving*. Re-verified independently from the saved files by a second code path: 14 nodes,
17 links, **zero LoRA-class nodes, zero LoRA-ish strings**, `ModelSamplingAuraFlow.model` →
`['1', 0]` = `UNETLoader`, on all three graphs.

| submission | prompt_id | seed | estimate | status |
|---|---|---|---|---|
| view 0 | `4ba045dc-183e-49ae-a652-dbc685610471` | 770700 | 0 credits | completed |
| view 1 (rejected) | `6578f588-758e-4ecf-992b-19be172246e0` | 770700 | 0 credits | completed |
| view 1 re-roll | `984952cf-6214-4768-b785-fea48c18a050` | **770701** | 0 credits | completed |

Both outputs are **240×1024**, frame-matched to the control and the render.

## 4. ⚠ The rejected artifact, and the rule it violated

**View 1's first generation put GOLD on the crossguard.** At 4×
(`REJECTED_SHEET_1_seed770700_HILT.png`) the whole crossing — both quillon arms and the
centre — is gold/brass, the boss does not separate from it, and the collar rings are gold too.

**The rule, authored 2026-08-07 before any generation existed** (`canon/LONGSWORD-IDENTITY.md`,
the occupancy audit): L2 owns *"both quillon arms end to end — the stepped chamfered ends
included — and the guard's underside"*, coloured blackened iron, and *"no family word rides
more surfaces than it owns; gold appears once."* On the rejected artifact L3's material
occupies L2's surface.

**Would the rule have been the same whatever came out? Yes** — it is the fixture's own
occupancy table, written at authoring. That is the test this repo uses to separate rejecting a
specification violation from selecting a result, and the profile pre-registers the remedy in
terms: *"term resistance at this seed is a re-roll, not a naming failure"* (E12 Ruling 21c,
carried in `prop.json`'s seed entry).

**One re-roll, new seed 770701, recorded as an explicit deviation by the builder's own
pre-flight. The rejected artifact stays in the record with its sheet, its hilt crop and its
measurement.** A second failure would have been the result; it did not occur. **View 0's
re-roll was not spent.**

**The control is not what failed.** The control panel at 4× carries the boss's diamond outline,
the quillon structure and every wrap coil. The geometry was constrained and the *material*
went elsewhere — the documented mechanism that the text wins on material while the control
wins on form.

## 5. Element landing, by eye at the hilt crop (the D8 lesson: no numeric gate on L5)

| element | **view 0** | **view 1 (re-roll)** | **view 1 (rejected)** |
|---|---|---|---|
| L1 battle-worn steel blade, raised central ridge | **landed** — dark worn steel, ridge and fullers present, wear reads as damage | **landed** — dark steel with surface etching | landed |
| L2 blackened iron crossguard | **landed** — near-black rough cast iron, separated from L1 by VALUE exactly as the fixture designed | **landed** — dark ornate iron | **FAILED — gold** |
| L3 gold diamond boss at the crossing | **landed** — a crisp gold diamond, exactly at the crossing, exactly the control's shape | **landed** — a crisp gold pyramid at the crossing | **absorbed into a gold crossguard** |
| L4 oxblood leather grip wrap | **landed** | **landed** | landed |
| L5 dark garnet gem pommel | **landed** — faceted dark garnet | **landed** — faceted, but reading **magenta-purple** rather than garnet-red | landed |

**⚠ The D6-spur watch-note fired, and it fired both ways.** The fixture put L3's two collar
rings on its surface list with the note that they *"earn their own prompt term only if the
pair mislands them."* Measured:

- **view 0: the rings did NOT land gold** — the pommel collar is dark metal, the mid-grip ring
  is brown/leather.
- **view 1 re-roll: the rings DID land gold.**

**Gold's extent is unstable across views at this recipe** — under-applied on one, correct on
the other, and over-applied to a whole neighbouring element on the rejected roll. That is a
finding for the fixture and it is exactly what the watch-note was pre-registered to catch.
**Reported, not fixed** — the fixture is the advisor's.

## 6. Ruling 7b's two pre-registered checks, measured

### (a) L1's realised lightness AND chroma — the cool-cast question

| artifact | L\* median | **C\* median** | above the C\* 5.0 floor, 3 px eroded | hue of the above-floor set |
|---|---|---|---|---|
| **view 0** (770700) | 23.51 | **2.93** | 10.15% | 295 |
| view 1 **rejected** (770700) | 20.82 | **4.56** | 42.42% | 295 |
| **view 1 re-roll** (770701) | 21.20 | **5.39 — clears the floor** | 51.94% | 295–296 |

**The tail is NOT rim mixing, and that was tested rather than assumed.** Eroding the figure
mask 0 → 3 px moves the above-floor share only 13.88 → 10.15 (view 0) and 44.83 → 42.42
(rejected) and 56.32 → 51.94 (re-roll). Antialiased perimeter pixels on a lavender ground
would have collapsed under erosion, as the bake-margin population did in §2.2c of the
measurement pass. They do not. **There is a weak but real chroma in the blade body, at hue
~295, inside blue-violet's own 225–300 band.**

**So Ruling 7b's named risk materialised — partially, and by degrees.** Below the floor at the
median on view 0; **just above it on the re-roll (5.39 against 5.0)**. Per Ruling 7b this is a
**finding for the palette-bands derivation, and the word is NOT re-chosen on it.** It is not
re-chosen here.

**A correlation offered as data, not as a mechanism claim:** the darker and more saturated the
realised backdrop, the more chroma in the blade (backdrop C\* 33.02 → blade 2.93; 32.61 →
4.56; 37.10 → 5.39). Consistent with bleed; three points is not a demonstration.

### (b) The realised backdrop against the derived estimate

| artifact | realised rgb | L\* | C\* | vs estimate L\* 86.9 / C\* 21.4 |
|---|---|---|---|---|
| view 0 | (171, 151, 208) | 66.02 | 33.02 | **−20.9 L\*, +11.6 C\*** |
| view 1 rejected | (189, 167, 225) | 72.16 | 32.61 | −14.7 L\*, +11.2 C\* |
| view 1 re-roll | (144, 123, 186) | 55.59 | 37.10 | **−31.3 L\*, +15.7 C\*** |

**Two things, both the opposite of the precedent.** The word materialises **darker** than the
derived triple by 15–31 points of L\*, and **more saturated** by 11–16 points of C\* — where
the beast's realised C\* came back *weaker* than derived. And it is not stable: the same word
at two seeds spans 16.6 points of L\*.

### ⚠ (c) The ruled word materialised in the MAGENTA band, not blue-violet

Not asked for, and it falls straight out of (b):

| artifact | realised backdrop hue | band by the derivation's own boundaries | min margin to an occupied family |
|---|---|---|---|
| view 0 | **305.4** | **magenta (300–360)** | 78.9° |
| view 1 rejected | **306.4** | **magenta** | 77.9° |
| view 1 re-roll | **305.1** | **magenta** | 79.2° |

The derivation chose **blue-violet (225–300)** and credited it with **≥123°** from every
occupied hue. `plain lavender background` lands at **~305 on all three artifacts** — five
degrees outside that band — carrying **78–79°** of margin to the wine family instead. Still a
wide margin, and the ruling's other grounds (chroma steel cannot erase; the pre-registration
honoured) are untouched. **A word is not a triple**, and this is the measurement of the gap
between them. Recorded for the palette-bands derivation with everything else in §6.

### (d) Does the ruled backdrop do its job? — the key's own metric on the realised artifacts

| artifact | blade rgb | backdrop rgb | max-channel separation | against the key's 0.06 cut |
|---|---|---|---|---|
| view 0 | (58, 55, 61) | (171, 151, 208) | **0.5765** | **9.6×** |
| view 1 rejected | (51, 49, 55) | (189, 167, 225) | **0.6667** | 11.1× |
| view 1 re-roll | (53, 50, 57) | (144, 123, 186) | **0.5059** | 8.4× |

**The derivation's purpose is achieved on the artifact, by 8–11×** — and by a mechanism the
sensitivity table did not predict. It expected the risk to be steel arriving **bright**
(L\* ≥ 74), collapsing a light backdrop's margin. **Steel arrived dark (L\* 21–24)**, the
opposite direction, so the value gap is wider than derived rather than narrower.

## 7. The drift pre-registration, scored

Committed in `98af737` before the pair existed. **P-D was: D3 live, D1 absent, D2 partial,
D4 absent.**

| # | signature | outcome |
|---|---|---|
| **D1 painterly** | **ABSENT — held.** No brushstroke texture on either view; surfaces read as rendered material. `lora-w 0.0` removing the painterly LoRA entirely is the plausible reason and is not demonstrated here |
| **D2 chrome** | **ABSENT rather than partial — my "partial" was pessimistic.** No blown specular band, no mirror. The blade is matte-to-satin and the wear reads as damage, which is the boundary L1's own note drew. **But the nick scoring is largely gone**, replaced by broader patina and (on the re-roll) etched ornament — relief lost to *smoothing*, not to specular |
| **D3 stylised game metal** | **the one I called live, and I cannot call it cleanly.** No cel-shading, no rim light, no teal tinting — the hard signatures are absent. What is present is an ornamented prop-shot quality, and I do not have a rule that separates that from "ultra-realistic worn steel" |
| **D4 backdrop bleed** | **PARTIALLY PRESENT — falsified.** I predicted absent. §6(a): below the floor at the median on view 0, above it on the re-roll, and not rim mixing |
| **D5 photographic** | **as flagged, I cannot call it.** Both views carry a soft contact shadow and a studio-product quality. I named this the one I expected to be least able to call, and I am not able to call it |

**Two of five as predicted, one falsified, two I named in advance as unfallible by me.** The
useful part of the exercise was not the scoreboard: pre-registering D4 is what made §6(a)'s
erosion test an obvious thing to run rather than a number to report and move past.

## 8. What has NOT been done

- **No third roll.** One generation per view, one bounded re-roll on view 1 only. View 0's
  re-roll is unspent.
- **No profile or fixture edit.** The gold-extent finding (§5), the magenta-band finding
  (§6c) and the cool-cast finding (§6a) are reported; `prop.json` and
  `canon/LONGSWORD-IDENTITY.md` are untouched.
- **The backdrop word and the canny pair were not re-chosen on anything the pair shows.**
  Both are ruled; Ruling 7b forbids the first explicitly.
- **No palette bands derived.** They need this pair as their cross-check and are a later
  ruling's work; the fixture's non-circularity rule stands.
- **No projection, no twins, no strokes, no `thin_extent` value.**
- **No memory-store write.** The repo is the record.

## 9. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | All three graphs saved to disk **before** submission and committed; every prompt_id, seed and estimate recorded; the twin-prompts file records the entry it derived from, the drop map and per-view term counts; every readout lands in a JSON beside its artifact; the rejected artifact keeps its own sheet, hilt crop and measurement under a filename carrying its seed |
| ANDON_AUTHORITY | **3** | The builder's pre-flight is unskippable and both graphs had to pass it before a file existed; the twin-prompts builder asserts every stem is an ordered subsequence and would have written nothing on failure; the re-roll was taken against a rule authored before the artifact, bounded at one, with the rejected artifact preserved; the sheet builder halts if any panel's framing differs |
| NAMED_COMPENSATORS | **2** | **0 credits** on every submission, quoted before each. New files only; two new instruments in `tools/diagnostics/`, three new docs, artifacts under `E14_prep/`. The irreversible act in scope is GPU time on three cloud runs, which has no undo — bounded instead, by the one-re-roll rule and by not spending view 0's. Not 3: cloud uploads of four inputs persist in the account's input store with no compensator named |
| DECOMPOSE_BY_SECRETS | **3** | The one-string check ran against **this** subject's renders rather than importing the carried flag — and the flag was half wrong; the drop is expressed through the builder's deletion construction rather than by retyping a string; the backdrop word flows fixture → derivation → ruling → profile → builder → graph and never through code |
| UNCERTAINTY_GATED_HUMANS | **3** | Nothing is judged. The pair, the rejected artifact, three sheets and three hilt crops at 4× go to the advisor's eye first and the Director's second; the cool-cast finding is routed to the palette-bands derivation exactly as Ruling 7b directs rather than acted on; the gold-extent instability is handed up as a fixture question |
| EXTERNAL_VERIFIER | **3** | The control's canny counts reproduce the ruled ladder row byte-for-byte, so the ruling and the submission are checked against each other; the no-LoRA property was re-verified from the saved files by a second code path; `e14_pair_readout.py`'s sRGB→Lab is asserted against `e14_backdrop_checks.py`'s on the derivation's own triple before any pair number is printed; the chroma tail was tested by erosion rather than reported, using the method that settled the off-surface question earlier in this arc |

---

## HALT — the advisor's eye first, then the Director beside the clay

Staged at `E:\AI\training\facet_next\E14_prep\pair\`:

```
PAIR_swordclay_0.png                     the pair, view 0        (240x1024)
PAIR_swordclay_1.png                     the pair, view 1        (240x1024, re-roll seed 770701)
PAIR_SHEET_0.png · PAIR_SHEET_1.png      REFERENCE | CONTROL | ASSET, full size
PAIR_SHEET_0_HILT.png · _1_HILT.png      the same three panels, hilt at 4x
REJECTED_swordclay_1_seed770700.png      the rejected artifact, preserved
REJECTED_SHEET_1_seed770700{,_HILT}.png  its sheet and hilt crop
readout_view0.json · readout_view1.json · readout_REJECTED_view1_seed770700.json
```

plus `ONESTRING_hilt_strip.png` and `ONESTRING_crossing_8x.png` (the one-string check's
evidence), `cloud/pair_view*.json` (the three submitted graphs), and `control/`.

**Three things want the advisor's ruling, and none is mine:**

1. **The pair itself** — whether these two images are this subject's specification source and
   visual target. The Director's overrule window on the whole authored identity is open on
   them, and the register's first test on steel is what he is looking at.
2. **Gold's unstable extent** (§5) — the rings missed on one view, taken on the other, and a
   whole neighbouring element taken on the rejected roll. The fixture's D6-spur watch-note
   pre-registered exactly this question and it now has an answer to rule on.
3. **The word-versus-triple gap** (§6b, §6c) — `plain lavender background` materialising 15–31
   L\* darker, 11–16 C\* more saturated, and at hue ~305 in the magenta band rather than the
   blue-violet the derivation chose. Ruling 7b routes the cool-cast half of this to the
   palette-bands derivation; the band-membership half is new and has no home yet.
