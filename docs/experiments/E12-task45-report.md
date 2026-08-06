# E12 handoff 3, Tasks 4 and 5 — the styled target pair, and the bands

**Executor session, 2026-08-05/06.** Predictions pre-registered blind in `75b9a02`
([E12-task45-predictions.md](E12-task45-predictions.md)) before any render, silhouette,
control, submission or clustering existed. This report ranks nothing and recommends nothing.

The session halted once, at `e04_frame_agree`, and resumed on **E12 Ruling 9**
(`5256dea`). The halt and its evidence are [E12-task4-anchor-halt.md](E12-task4-anchor-halt.md);
the repair and both subjects' digits are [E12-anchor-repair.md](E12-anchor-repair.md).

**No credits were spent.** `estimate_credits`: *"0 credits — no paid API nodes found in this
workflow."* **0 re-rolls of the 1 allowed.**

---

## 1. What ran

| leg | result |
|---|---|
| watchdog | **alive** before every GPU/Blender leg and re-checked at each resume — heartbeat ages 0.5–2.1 s, pid 22324, ceiling 31200 MiB. Reported either way per the standing rule |
| clay | `turn_render --clay --profile beast.json`, 8 views at 1792×1024 width-fit. Views 1 and 5 rendered first; the other six later for the 9d verification, written into the same dir so 1 and 5 stayed byte-untouched by construction |
| silhouettes | `silhouette_masks --profile beast.json` — 26.754% of frame, 490,941 px, bbox 1378×854 on **both** views |
| **anchor** | **0 differing px on both views** (post-repair). Fired at 1 px pre-repair |
| controls | `restylize_views --emit-only --masks` — view 1: 50,631 px (canny 36,011 + contour 25,256); view 5: 37,228 px (canny 22,642 + contour 25,256) |
| cloud | two submissions, `succeeded`, outputs 1792×1024 |
| bands | `e04_bands.py` — generalised with `--tag`/`--asked`, **galleon run re-verified byte-identical first** |

`E12_pair/PAIR_SHEET.png` is clay | control | styled for both views, full size. **Look at it
before the numbers.**

## 2. Predictions scored — 8 held, 4 falsified, 1 partial

| # | prediction | outcome |
|---|---|---|
| **F1** | anchor returns 0 px | **FALSIFIED** — 1 px on view 5. The row I called least likely to fire is the one that fired, and it turned out to be an operand mismatch in the gate itself |
| **F2a** | silhouette 20–30% / 22–32% | **held** — 26.754% both |
| **F2b** | view 5 > view 1 | **FALSIFIED, structurally** — *exactly* equal. An orthographic silhouette from `d` and `−d` is the same ray set (Ruling 9b) |
| **F3a** | contour > 20,000 px both | **held** — 25,256 px, and *identical* on both views, which is 9b again in a third instrument |
| **F3b** | Canny exceeds contour on both | **PARTIAL** — holds on view 1 (36,011 > 25,256), **fails on view 5** (22,642 < 25,256). View 5 is dominated by smooth membrane fields; view 1 carries the head, frill and scaled chest |
| **F4** | the `n_contour < 500` ANDON does not fire | **held** |
| **G1** | 9–11 of 11 elements land | **held** — **10 of 11** |
| **G2** | the misses are D8 and/or D9 | **held exactly** — D8 is the only one, at ΔE 57.2 |
| **G3** | the five ivory elements collapse into one cluster | **held** — D4/D5/D6/D7/D10 all → rgb(197,187,142), 4.06% |
| **G4** | realised backdrop less chromatic than asked, still blue-violet | **held** — C\* 29.58 → **10.44** (−65%), h 293.7 → 301.0 |
| **G5** | D3 lands and is a top-three cluster by share | **held** — ΔE 14.2, nearest cluster 11.05%, third largest |
| **G6** | view 5 carries no grafted head anatomy | **held** — D8 and D9 measure **0 px** there against 227 and 958 on view 1. *Cause not isolated — see §5* |
| **G7** | 0 re-rolls | **held** |
| **H1** | forbidden span 180–230° (50–64%) | **FALSIFIED** — **278.1° = 77.3%**, near the galleon's 288°/80.0%, nowhere near the predicted band |
| **H2** | the ivory family's bands merge | **held** — one cluster, one band |
| **H3** | D3 and D11 fall below the C\* 12 floor | **held** — their nearest clusters are C\* 9.6 and C\* 6.2 |
| **H4** | at least one cluster sits outside every declared element | **FALSIFIED** — **zero** clusters exceed ΔE 25 from their nearest declared element; the worst is 23.5 |

**H1 and H4 are the informative failures**, and they fail *together* for one reason (§4).

## 3. The landing table — 10 of 11

Clustered from the pair's actual colours inside the exact silhouette (k-means in Lab, seed
770700, 14 clusters), never from the expectation — so an element *can* fail to appear, and one
did.

| id | element | ΔE | verdict | nearest cluster | share |
|---|---|---|---|---|---|
| D1 | deep moss-green scaled hide | **4.4** | LANDED | rgb(64,79,46) | 13.48% |
| D2 | pale bone-tan ventral plates | 5.3 | LANDED | rgb(197,187,142) | 4.06% |
| D3 | storm-grey wing membranes | 14.2 | LANDED | rgb(104,103,87) | 11.05% |
| D4 | bone-ivory curved horns | 13.1 | LANDED | rgb(197,187,142) | 4.06% |
| D5 | bone-ivory crown and cheek spikes | 13.1 | LANDED | rgb(197,187,142) | 4.06% |
| D6 | bone-ivory dorsal and tail spines | 13.1 | LANDED | rgb(197,187,142) | 4.06% |
| D7 | bone-ivory claws | 13.1 | LANDED | rgb(197,187,142) | 4.06% |
| **D8** | **ember-orange eyes** | **57.2** | **NOT FOUND** | rgb(138,134,88) | 7.04% |
| D9 | a dark wine-red tongue | 23.3 | LANDED | rgb(44,21,35) | 0.50% |
| D10 | pale ivory fangs and tooth rows | 18.1 | LANDED | rgb(197,187,142) | 4.06% |
| D11 | a dark slate mouth interior | 14.6 | LANDED | rgb(79,80,70) | 6.85% |

**The same colour-not-placement caveat the galleon's table carried applies here** and is
sharper: five elements share one cluster. "LANDED" says a colour matching this element is
present on the subject, not that the element is in the right place.

### D8 is the table's blind spot, and it was pre-registered as one

**The cluster table says NOT FOUND. The eye says the eye is there, unambiguously.**

`DRAGON-IDENTITY.md` pre-registered D8 as *"below any area floor … no numeric gate may be
armed on this element; landing verdict belongs to the twins' table, judged by eye at the head
crop"* — the G7 lesson, written before the pair existed. It is exactly right: the eye occupies
**153 px at ΔE < 15 / 282 px at ΔE < 25**, which is **0.03–0.06% of the figure**, against a
cluster floor of 0.4%. A 14-cluster k-means cannot represent it, and no threshold on this
table could be honest about it.

The corroborating measurement, which is not a gate: ember-orange pixels are **100% inside the
head rect**, in a single blob at x 462–494, y 304–323 — a 33 × 20 px region, i.e. one eye,
where the geometry has one eye.

**This is the checkpoint E12 Ruling 2 named for the allocation question** (*"if the pair
paints a convincing ember-orange eye on the measured recess, the question closes"*). The 2×
head crop is `E12_pair/pair/HEAD_view1_2x.png`, staged full size. **The verdict is the
Director's; this report records that the element is present, where, and how large.**

### One observation on D11, offered as data

D11's nearest cluster is rgb(79,80,70) — a near-neutral grey-green at C\* 6.2, below the
chroma floor. On the head crop the mouth interior reads **wine-red**, i.e. D9's register,
not slate. Two declared elements occupy one cavity and the darker/warmer one appears to have
taken it. Whether that matters is not this seat's call.

## 4. The bands — and why H1 and H4 failed together

Measured hues above the inherited C\* 12.0 floor:

```
96, 98, 101, 101, 102, 121, 124, 126, 133, 136, 138        345
└──────────────── one warm-green group ────────────────┘    └ wine ┘
```

| band | measured | proposed (±10° convention) | rests on |
|---|---|---|---|
| **warm-green** | 95.6–137.5 | **85.6–147.5** (61.9°) | 11 clusters, **81.61%** of the figure |
| **wine** | 344.6–344.6 | **334.6–354.6** (20.0°) | **1 cluster, 0.50%** |

| | allowed span | **forbidden span** |
|---|---|---|
| W3 (character) | 0–105, 125–210 | 170° — 47.2% |
| galleon (measured) | 50–100, 273–301 | 288° — 80.0% |
| **beast (measured)** | **85.6–147.5, 334.6–354.6** | **278.1° — 77.3%** |

**H1 predicted 180–230°. Measured 278°.** The prediction assumed that declaring green *and*
red *and* orange *and* ivory would spread the realised hues across a wide arc. It did not:
**eleven declared material names produced one 42°-wide hue group holding 81.6% of the
subject.** Green hide, bone-tan ventral, storm-grey membrane, bone-ivory and pale ivory all
realised inside h 96–138 — one olive family. That is the galleon's own lesson repeating on a
subject that looks nothing like it: *the realised palette is far tighter than the declared
names suggest.*

**H4 is the same fact from the other side.** Every one of the 14 measured clusters sits within
ΔE 25 of a declared element (worst 23.5); **zero clusters are outside the declared table**,
where the galleon had extras. There is no room for an off-palette cluster in a palette this
narrow.

### ⚠ Suspended: the wine band is not proposed as final

It rests on **one cluster holding 0.50%** of the figure — 2,455 px of 490,941 — and that
cluster is the tongue seen through an open jaw on one of the two views. Reported as numerator
and denominator, with the ±10° margin stated as **a convention inherited from the galleon's
table, not a measurement**. The galleon suspended its blue band on 3.69%; this is seven times
thinner. **Derive it when the beast's own twins exist, or run with the wine band wide and
report.** The warm-green band at 81.61% is solid.

### Chroma floors, per the dispatch's question

Two clusters fall **below** the inherited C\* 12.0 floor and carry no hue at all:
rgb(104,103,87) at C\* 9.6 (11.05%) and rgb(79,80,70) at C\* 6.2 (6.85%) — **17.90% of the
figure is below the floor**, and it is the two elements the fixture called neutral on purpose
(D3 membranes, D11 mouth interior). No floor is proposed or moved: 12.0 is W3's, it is named
as inherited, and this subject has no measurement that would justify a different one.

**D8 and D9 carry no numeric gate**, per their pre-registration. D9's band exists only because
it is the sole cluster above the floor in its hue neighbourhood, and it is suspended above.

## 5. What the pair does not settle

- **G6's cause is not isolated.** View 5 shows no grafted head anatomy — but its camera
  cannot see the head *and* its stem drops those elements. The measurement (D8/D9 at 0 px)
  confirms the outcome, not the mechanism. Separating them needs view 5 generated with the
  full string; that is a second generation and its own arm.
- **Nothing about whether the route works on a beast.** No twin, no atlas, no projection.
- **The backdrop's realised value is better than asked, not worse** — 0.2353 against the
  asked 0.2000 and W3's grey at 0.0745, re-derived on the pair's own clusters. The galleon's
  4d found the opposite regression; this one holds, and Ruling 8b's finding that W3's grey
  scores under the key's own cut is corroborated on realised values (0.0745 against a 0.06
  cut is 1.24×, the tightest margin on the asset).

## 6. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The submitted workflow JSONs are on disk with the uploaded cloud names in them, so the saved file *is* the submitted graph; `uploads.json` maps every input; clustering seed 770700; chroma floor named as inherited; every framing value the profile's |
| ANDON_AUTHORITY | **3** | The anchor fired and stopped the run before the control was built and long before submission; nothing was retuned to pass; the builder's pre-flight and topology check leave **no file** on failure, and were proven to fire on all three defect classes before being trusted; the wine band is suspended rather than fixed on 0.50% |
| NAMED_COMPENSATORS | **3** | New files only; two tools edited additively (the anchor keeps its legacy path, `e04_bands` keeps the galleon's defaults and was re-verified byte-identical before use); 0 credits, so no spend to compensate |
| DECOMPOSE_BY_SECRETS | **3** | Two subject constants removed from `e04_bands.py` (the galleon's mask tag and its asked-white backdrop) into flags; every beast value derives from this mesh, this fixture or this pair |
| UNCERTAINTY_GATED_HUMANS | **3** | D8's landing is handed up as *the table cannot see it, the eye can, here is the crop at 2×* rather than resolved; D11's mouth reading offered as data; G6's unisolated cause stated in both the sidecar and here |
| EXTERNAL_VERIFIER | **2** | Clustering derives from the image, so an element can fail — and one did, in exactly the place its own pre-registration said the instrument would be blind. Marked 2 because the anchor's repair **cost** independence (its two derivations are now bit-identical arithmetic), enumerated in its docstring; and `skip:` on a second model, per precedent |

---

**Tasks 4 and 5 complete. HALT per the dispatch.** The pair, the head crop, the sheet, the
bands and this report go to the **advisor's eye first**, then the Director beside the clay —
his overrule window on the whole authored identity, made visual. Open for the ruling: D8's
landing verdict (Ruling 2's named checkpoint), the suspended wine band, D11's mouth reading,
and the fang-shell finding carried in `E12-twin-prompts.json`.
