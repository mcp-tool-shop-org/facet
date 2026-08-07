# E14 Gate 0 — predictions, committed BLIND

**Executor session, 2026-08-07.** Written and committed **before any longsword mesh exists**
— no reconstruction has been run, `mesh_stats` has returned nothing, and no render has been
made. The only longsword artifacts I have looked at are the three staged clay concepts, at
full size, which are the source and not a result.

Every number below can be wrong. A wrong prediction is a full success: it is the calibration
`profiles/prop.json` inherits, and two of E12's most useful predictions were failures, because
they *located* where the subject departed from the prior.

**The standing rule I am deliberately obeying, and where it cuts against me.**
`docs/handbook/subjects.md` records it plainly: *"Subject properties do not interpolate — the
dragon's shells and reach landed outside any band the two priors suggest, in opposite
directions, and the arc's standing rule is that a new subject class has no working prior."*
E12's executor was most wrong exactly where it priced the *prior* (the ship) instead of the
*subject*. So every prediction below reasons from **what a longsword is** — one rigid object, a
thin slab with two edges that taper to nothing, a helical wrap, a faceted polyhedron — and
quotes the measured family only as a scale against which to state the answer.

---

## 0. The dispatch's inherited claims, checked against source before use

Per the calibration note, in the same breath as using them.

| claim in the dispatch | source checked | verdict |
|---|---|---|
| clay byte counts 1,021,466 / 1,029,231 / 1,093,621 | directory listing of the staged clays | **confirmed, all three exactly** |
| character 40–191 shells; ship 237–512; beast 9–12 | `docs/handbook/subjects.md` calibration table; `E12-gate0-report.md` §3 | **confirmed** |
| character widest-horizontal / height 0.46–0.72 | `docs/handbook/subjects.md` calibration table | **confirmed** |
| "Precedent cost: 116–141 s and 4.4–5.6 GB peak VRAM per mesh" | `E04_gate0/recon.log` — TOTAL 141 / 125 / 116 s, OVERALL PEAK 4.4 / 5.6 / 4.6 GB | **confirmed — but it is the galleon's, and not the nearest precedent** |
| — the nearest precedent, same runner, two days earlier | `E12_gate0/recon.log` — TOTAL 135 / 106 / 103 s, OVERALL PEAK 3.8 / 3.7 / 3.4 GB | **the dragon is cheaper on both axes than the figure the dispatch quotes** |
| `turn_render` maps `ortho_scale` to the vertical under `--fit-axis height` | `turn_render.py:109–111` — `sensor_fit = "VERTICAL"` set explicitly, `ortho_scale = size.z * margin` | **confirmed; the portrait case is handled, not a latent landscape assumption** |

**The three clay descriptions, checked at full size against the dispatch's wording.** All three
match in substance. Three departures worth recording, because these descriptions are what a
later reader will use to tell the candidates apart:

- **00002's quillons are the longest-span of the three by a clear margin** — nearly straight
  horizontal arms reaching far wider than either other candidate. The dispatch describes their
  *ends* ("taper to soft down-swept flares", accurate) but not their span, which is the most
  visible thing separating 00002 from the other two at a glance.
- **00001 also carries a flared ricasso shoulder below the guard**, which the dispatch
  attributes distinctively to 00003. 00003's remains genuinely distinctive — it is a *double*
  flare (out, step in, out again into a second wider shoulder, then taper); 00001's is a single
  flare. The distinguishing word is "double", not "flare".
- **00003 is not purely near-frontal** — a side plane of the blade is visible down its right
  edge, so it carries some three-quarter rotation. Less than 00002's, but not zero.

Two things observed on the clays and named nowhere: **the pommel sits on a distinct collar ring
above the wrap on 00003**, and all three blades carry a **hollow-ground section** — a raised
central ridge with concave bevels falling away to each edge.

---

## 1. Cost

| # | prediction |
|---|---|
| **P1** | pipeline `TOTAL` **90–140 s** on all three |
| **P2** | `OVERALL PEAK` VRAM **≤ 4.0 GB** on all three — at or below the dragon band's top, below every galleon |
| **P3** | faces **900k–1,000k** on all three |

P3 is low-information and is stated so it is on the record as *not* evidence about swords: nine
prior reconstructions landed 939k–987k, which reads as a pipeline face budget rather than a
subject property. It fails only if this subject escapes that budget, which would itself be the
finding.

Reasoning for P2: the two measured subjects order themselves by structural complexity rather
than by size — the galleon's rigging cost 4.4–5.6 GB, the dragon's connected body 3.4–3.8. A
longsword is the simplest solid the route has attempted. If P2 fails upward, complexity is not
what drives the peak and my model of the pipeline is wrong.

## 2. Topology

| # | prediction |
|---|---|
| **P4** | **welded shells ≤ 8 on all three** — below the beast's floor of 9, making this the most connected subject the route has reconstructed |
| **P5** | largest-shell fraction **≥ 0.990** on all three |
| **P6** | `watertight` **False** on all three |
| **P7** | and the mechanism is **non-manifold edges (>2 faces), not open boundary**: boundary edges **≤ 5** per mesh, total boundary length ~0 |
| **P8** | non-manifold edge fraction lands **inside the dragon's measured 0.10–0.49% band** on all three |
| **P9** | those edges **concentrate along the two cutting edges and the tip** — a sword's version of the membrane's free rim, and the locus where a slab thins to nothing |

P4 is the prediction I most expect to be interesting rather than right. A longsword has no
free-floating structure at all: the wrap is on the grip, the quillons are on the guard, the
pommel is on the tang. The dragon's 9–12 came with satellites that were *teeth* — small
free-standing detail features — and a sword has fewer such features, so the count should fall
further. **The live risk is the grip wrap:** if the reconstructor cuts the inter-coil grooves
deeply enough, individual coils could return as separate rings and the count could jump into the
tens. If P4 fails, that is the first place to look, and locating the satellites is worth more
than the count.

P6 commits to False, matching all nine prior reconstructions. Stating the alternative so the
prediction is informative either way: this is the simplest closed solid the route has
reconstructed, so **`True` on any of the three would be the route's first**, and would say the
non-manifold defects seen everywhere else are a function of subject complexity rather than of
the pipeline.

## 3. The blade as a sheet — this class's stressor

| # | prediction |
|---|---|
| **P10** | the blade returns as a **closed, thickened slab** — no open sheet, no through-hole, no boundary loop anywhere in the blade |
| **P11** | the **central ridge survives as legible geometry** on all three under `--clay` |
| **P12** | **no pinch-through in the blade *field***, as distinct from at its edges — 00003's dragon-pattern "dense mass of non-manifold edges through the field of the folded wing" does not recur here on any candidate |

Reasoning, and the measurement that separates P10 from its alternative: E12 established that a
membrane thinner than the voxel grid fails by **pinching** (two faces meeting along one edge)
rather than by holing, and that an open sheet is decidable from the mesh alone — an open sheet
carries a boundary loop around its perimeter, a closed slab carries none. The dragon's free
membrane rim measured **0.1–0.25% of figure height**. This blade, read off 00002's three-quarter
view where its side plane is visible, is on the order of **1.5–2% of height** thick — roughly an
order of magnitude fatter than the structure that pinched. So the blade *field* should be safe
by a wide margin, and the risk migrates to the **cutting edges**, which is what P8 and P9 are
about.

## 4. Fine structure

| # | prediction |
|---|---|
| **P13** | wrap coils survive as **legible helical relief** on all three, and **zero coils detach** as separate shells |
| **P14** | coil relief is **weakest on 00002**, which carries the finest pitch |
| **P15** | the gem pommel's facets return as **readable planes with ROUNDED edges** rather than crisp ones |
| **P16** | **no quillon detaches** on any mesh, and **00003's pointed tips return as points, not blunted** |
| **P17** | edge nicks and blade scoring **reconstruct as geometry, attenuated** relative to the clay; the most surviving relief is on 00003, which carries the heaviest scoring |

P16 bets *with* the dragon precedent rather than against it: E12 predicted blunting somewhere and
was falsified — horns came back "full, sharp, attached", tips "fine and sharp". Quillon points
are smaller than horns, so this is the same bet at a harder scale, and losing it locates a size
threshold rather than merely being wrong.

## 5. Ground contact and tip

| # | prediction |
|---|---|
| **P18** | **no ground or shadow-derived geometry** on any of the three, and the **tip returns free and pointed** — not truncated flat at the contact, not fused to a floor patch |

Every clay stands on its tip over a soft cast shadow. The precedent is E12's z-min slab check,
which found flat foot soles where a dragon's feet were planted and no floor anywhere. A sword's
contact is a single point rather than a sole, so there is even less for a floor to key off — but
a truncated tip is the specific failure to look for, and it would be visible on the sheet.

## 6. Proportion and framing — the route's first portrait

| # | prediction |
|---|---|
| **P19** | widest-horizontal / height in **0.20–0.40** on all three, i.e. **below the character's 0.46 floor** — the route's first portrait subject |
| **P20** | ordering on that ratio: **00002 > 00003 > 00001** |
| **P21** | derived render frames **240–384 px wide** at h = 1024, portrait on all three |
| **P22** | the **worst yaw is an axis-aligned view (0 or 4)** on all three, and the worst-yaw ratio exceeds the axis-only ratio by **≤ 0.5%** |

P19 and P20 come from eyeballing the quillon span against total height on the three clays at
full size — roughly 0.25 / 0.35 / 0.27 — and are labelled as an eyeball estimate, not a
measurement.

P22 is the reverse of the dragon's finding and is the sharper of the two claims. On dragon 00002
the frame needed **7.46% more** than the axis-only formula, because its wingspan and tail sweep
were nearly equal and about 45° apart. A sword is the opposite shape: the quillon span lies
along one horizontal axis and the depth axis is small, so a 45° view projects the quillon tip at
`cos 45° = 0.707` of its axis-view width and a shallow depth axis cannot make up the difference.
**Every 45° view should come out narrower than view 0**, which would make E12's per-yaw extension
correct but *inert* on this subject — worth knowing before it is trusted as a general guard.

## 7. Symmetry

| # | prediction |
|---|---|
| **P23** | quillons and blade edges read **bilaterally symmetric** on all three renders |

Observational only; no instrument is commissioned for it this session. The candidate at risk is
00002, whose clay carries the most three-quarter rotation.

## 8. Hilt-region evidence

| # | prediction |
|---|---|
| **P24** | hilt face share **20–45%** of total faces on all three |
| **P25** | density contrast (median face area **outside / inside**) **> 1.0**, in the range **1.2–3.0** — at or above the dragon head's measured 1.19–1.32× |

The hilt box will occupy a far larger share of the bounding box than the dragon's head did
(1.3–1.8% of bbox volume), because a sword's bbox is mostly empty air around a thin object. So
the *share* numbers are not comparable across subjects and only the *contrast* is. P25 predicts
at or above the dragon's band because a helical wrap groove and a faceted polyhedron are finer
relief than dragon scales.

---

## What these predictions are not

They rank nothing. Which sword is *the* sword is an outcome call and it is the Director's, and
rejecting all three is a legitimate outcome. Nothing above is a pass condition, a gate or a
threshold — no number here can halt anything, and none is written into any profile.
