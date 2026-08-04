# E04 Task 4d — the landing table, the bands, and the backdrop re-derived on realised values

**Executor session, 2026-08-04.** Local only, no generation. Measured against the
**Director-approved** styled target pair and never against twins that do not exist
(non-circularity, kept). `G6` read as **gold** throughout, per Ruling 7.

**Two results reverse what was expected**: the galleon's palette gate comes out **stronger**
than the character's, not weaker — and the **realised backdrop is worse than the grey it
replaced**, because white did not land.

---

## 1. Method, and what it can return that a sample disc cannot

Elements are located by **clustering the pair's actual colours inside the exact silhouette**
(k-means in Lab, fixed seed 770700, 14 clusters), then asking per declared element whether any
cluster sits near its expected colour. Hand-placed sample discs were rejected: a disc I
position by eye measures *where I think an element is*. The cluster table measures **what is
actually there**, and it can return *"nothing like this element is present"* — which a disc
cannot.

## 2. The landing table — 11 of 12 landed, 1 did not

| id | element | ΔE to nearest cluster | verdict | nearest cluster | share |
|---|---|---|---|---|---|
| G1 | gilded lion figurehead | 5.8 | **LANDED** | rgb(179,141,49) | 1.56% |
| G2 | warm oak-brown hull planking | 8.2 | **LANDED** | rgb(128,105,65) | 15.93% |
| G3 | black tarred strakes | 8.7 | **LANDED** | rgb(44,25,13) | 9.67% |
| G4 | weathered tan canvas sails | 4.4 | **LANDED** | rgb(197,174,127) | 8.33% |
| G5 | gilded stern scrollwork | 5.8 | **LANDED** | rgb(179,141,49) | 1.56% |
| **G6** | **gilded spire** *(amended)* | **5.8** | **LANDED** | rgb(179,141,49) | 1.56% |
| **G7** | **red-lined gun port lids** | **34.7** | **⚠ NEAR — did not land as red** | rgb(92,60,22) | 9.25% |
| G8 | black iron cannon barrels | 13.9 | **LANDED** | rgb(44,25,13) | 9.67% |
| G9 | dark tarred rigging/ratlines | 9.6 | **LANDED** | rgb(44,25,13) | 9.67% |
| G10 | pale scrubbed deck planking | 9.1 | **LANDED** | rgb(197,174,127) | 8.33% |
| G11 | deep sea-blue frieze band | 14.5 | **LANDED** | rgb(35,46,74) | 2.14% |
| G12 | gilded stern-gallery railings | 5.8 | **LANDED** | rgb(179,141,49) | 1.56% |

**G7 is the miss.** Its nearest cluster is a warm brown at ΔE 34.7 — **there is no red
anywhere on this ship above the chroma floor.** The measured hues run 62–88 and 283–291;
G7's expected hue is ~28. The red lining did not arrive.

**Same classification as G6's before the Director ruled: an element that did not land, not
off-palette material** — nothing arrived that is outside the spec, a named element simply
failed to appear. No re-roll trigger under the stated rule. His to overrule or keep.

### The limit of this table, stated plainly

**Four elements share one cluster** (G1/G5/G6/G12 → the gold) and **three share another**
(G3/G8/G9 → the dark). That is expected — they are declared as the same materials — but it
means **"LANDED" says a colour matching this element is present on the ship, not that the
element is in the right place.** The fixture already says this of the gate itself: *"It tests
COLOUR, not placement. Gold on the boots would pass every band while being flatly wrong."*
The same caveat governs this table. Placement is the Director's eye, and he has seen it.

## 3. The bands — and the gate comes out STRONGER than the character's

Measured hues of every cluster above the inherited **C\* 12.0** floor:

```
62, 69, 77, 77, 82, 86, 87, 88        283, 291
└──────── one warm group ────────┘    └─ blue ─┘
```

Two contiguous groups, split by a 195° gap. With a symmetric ±10° margin:

| band | measured | proposed | rests on |
|---|---|---|---|
| **warm** | 62–88 | **50–100** | 8 clusters, **73.6%** of the ship |
| **blue** | 283–291 | **273–301** | 2 clusters, **3.69%** of the ship |

| | allowed span | **forbidden span** |
|---|---|---|
| **W3 (character)** | 0–105, 125–210 | **170° — 47.2%** |
| **galleon (measured)** | 50–100, 273–301 | **288° — 80.0%** |

**This reverses my Task-1-era estimate.** I costed admitting blue at ~120° forbidden (33.3%)
and warned the gate would lose a third of its reach on the one subject where it carries the
judgment no eye can. Measured, the galleon's forbidden span is **288° against W3's 170°** —
**the ship's gate is markedly stronger than the character's.** Two reasons, and only one was
foreseeable: the Director's G6 amendment removed verdigris, and — the part I got wrong — the
ship's realised palette is far **tighter** than its twelve declared names suggest. Twelve
material names produced **two hue groups**, because gold, oak, tan, deck and tar are all one
warm family.

### ⚠ Suspend: the blue band is thin, and it is not proposed as final

The blue band rests on **two clusters totalling 3.69%** of the silhouette. That is enough to
say blue is present and where it sits; it is **not** enough to fix a band edge. Reported as
numerator and denominator — 283° and 291°, 2.14% + 1.55% — with the ±10° margin stated as a
*convention, not a measurement*. **Derive it properly when the ship's own twins exist**, or
run with the blue band wide and report. The warm band at 73.6% of the ship is solid.

### G6/G11 merge — the question is dissolved, not answered

It was asked because verdigris (green-cyan) and sea-blue could sit adjacent. **G6 is gold
now**, so verdigris is not a declared material at all: measured, G6's cluster sits at **h 87**
inside the warm band, 196° from G11's 283. **No merge is possible.** The Director's amendment
answered a question the measurement was commissioned to settle.

## 4. The backdrop, re-derived on realised values — and this is a regression

4b computed every distance against **expected** material colours and an **asked** backdrop.
Both operands were wrong. Re-run against the **measured** clusters and the **realised**
backdrop:

| backdrop | min distance to measured clusters | vs the 0.06 cut |
|---|---|---|
| **realised on the pair — rgb(173,173,173)** | **0.1000** | 1.67× |
| asked (white, 255) | 0.2471 | 4.12× |
| W3's inherited grey (106,106,107) | 0.1451 | 2.42× |

**The realised backdrop is worse than the grey it was chosen to replace — 0.1000 against
0.1451.** The derivation was directionally right (white is still best of the three at 0.2471),
but the prompt delivered **rgb(173) of an asked 255**, and the attenuated result landed near a
pale material the expected-colour table did not contain: a **near-neutral pale cluster at
rgb(198,195,192), 4.62% of the ship, C\* 2.2**, sitting **0.098** from the realised backdrop.

**That cluster is the tightest margin on the asset and it is the thing to watch.** It is
1.63× the cut — clear, but by the least of anything measured, and it is invisible to the
palette gate because it sits below the chroma floor.

**Two corrections to 4b's record, both mine to have caused:**

1. **Distances were computed against a backdrop that did not arrive.** Every figure in 4b's
   table assumed 255. The asked-vs-realised gap Ruling 6 banked is not a footnote here — it
   moved the answer from "2.5× better than grey" to "worse than grey".
2. **The expected-material table had no near-neutral pale entry**, so the cluster that now
   sets the minimum was not in the derivation at all. The measured table has fourteen
   clusters against twelve declared names; the extras are real surface.

**Not proposed here:** a stronger backdrop word. Choosing one while looking at the result it
would be judged against is exactly the retuning this repo forbids. The measurement is
reported; the next backdrop decision belongs to the spec, with Ruling 5's loop bound applying
to realised values.

## 5. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Fixed clustering seed 770700; chroma floor inherited from W3's fixture rather than chosen; every input a path |
| ANDON_AUTHORITY | **3** | The blue band is **suspended** with numerator and denominator rather than fixed on 3.69% of the ship; no backdrop word is proposed while looking at the result it would be judged against |
| NAMED_COMPENSATORS | **3** | Read-only on the pair; new files only; no spend |
| DECOMPOSE_BY_SECRETS | **3** | Bands derived from this subject's measured colours; the one inherited constant (chroma floor) is named as inherited |
| UNCERTAINTY_GATED_HUMANS | **3** | The landing table's colour-not-placement limit is stated in the table's own section; G7's miss is classified and handed up rather than re-rolled |
| EXTERNAL_VERIFIER | **2** | Clustering derives from the image, not the expectation, so an element *can* fail — and one did. The re-derivation overturned my own 4b conclusion. `skip:` on a second model |

---

**4d complete. HALT per the dispatch.** G7 is the open question for the Director, the blue
band is suspended pending the ship's own twins, and the backdrop's realised-value regression
is on the record for the E04 spec.
