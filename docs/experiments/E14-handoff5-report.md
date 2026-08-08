# E14 handoff 5 — STAGE 1: the seven twins project. The stage-1 halt.

**Executor session, 2026-08-08.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 19f.
Predictions committed blind in `4a9252d`, before the ceiling ran. The set's record is the
handoff-4 report (`2440e67`); the method precedent is E12's stage 1, cited not restated.

**Nothing is judged here. No pass condition exists** — the ceilings are comparables and the eye
is the gate (the E12 24e form, as the dispatch pins it). **No generation, no credits**;
projection, reach and measurement are local CPU, with one Blender leg for the pack and the
FLAT renders.

**The headline is not the coverage number. It is that Ruling 18c's price for view 2's camera is
overstated 43.8× as a set-level cost, and that the projected gem is a garnet core inside a
magenta shell split exactly on the ownership partition.** Both in sections 1 and 4.

---

## 1. ⚠ THE SEVEN-CAMERA REACH CEILING, pre-registered before any projection

**Which instrument ran, and why.** `e08_ceiling` takes `--sets N` — full equatorial rings —
and its `--elev` extras are only unioned for `n >= 8`. **It cannot express a seven-camera set**,
so the dispatch's stated fallback ran: `e14_atlas_anatomy --views`, which carries the recorded
exact cross-check against `e08_ceiling`'s N8. That cross-check was re-run as this session's
anchor before the seven-camera number was computed:

```
[anat] reachable over 8 yaws at facing-min 0.45: 1,879,807  (51.33% of valid)
[anat] EXTERNAL CHECK: reproduces e08_ceiling's N8 total exactly (1,879,807)
```

`ceiling.json`'s three facing settings (production 0.45/0.18, uniform 0.45, uniform 0.18) return
**identical** numbers at every N on this subject, so the fallback's uniform floor *is* the
production floor here and the comparison is like-for-like. Ray bias stays the shipped 3e-3 for
comparability, with **Ruling 10b's caveat**: that bias exceeds this route's ~0.00196 wall floor
and is worth **+0.97 points** at N8 — the geometric number is 50.36–50.43%, the comparable one
is the shipped default's.

| | cameras | reachable | % of valid |
|---|---|---|---|
| **THIS RUN'S DENOMINATOR** — 0/45/135/180/225/270/315 | **7** | **1,877,487** | **51.27%** |
| the route-comparable — all eight | 8 | 1,879,807 | 51.33% |
| **the delta** | | **2,320** | **0.0634 points** |

### 1b. ⚠ Ruling 18c's price for view 2's camera is 43.8× overstated as a set-level cost

Ruling 18c excluded view 2 and priced it: *"yaw 90's marginal contribution was +101,544 texels
= 2.8 points of valid at the ceiling pass."* **That figure is yaw 90's marginal at LADDER
POSITION 3** — added on top of yaws 0 and 180 only, before either diagonal neighbour existed.
Measured as a set-level loss instead:

| quantity | texels | points of valid |
|---|---|---|
| yaw 90's own reach, alone | 349,108 | 9.53 |
| **of that, reachable by NO other view in the set** | **2,320** | **0.0634** |
| N8 − N7 (same number, computed the other way) | 2,320 | 0.0634 |
| Ruling 18c's carried price | 101,544 | 2.7730 |

**Ratio: 43.8×.** A surface whose normal points at yaw 90 clears the 0.45 facing floor from
both yaw 45 and yaw 135 (cos 45° = 0.707), and on a sword's edge-on structures there is little
to occlude those rays — so the neighbours recover virtually all of it once they are present.

**This does not disturb Ruling 18c's decision**, which rested on two measured generation
failures at yaw 90 and on the brush being the route's mechanism for unreliable coverage.
It corrects the **price tag** attached to that decision: excluding view 2 costs the reach
ceiling **0.06 points, not 2.8**. Both numbers were computed on a path that reproduces the
shipped tool's N8 and N7 exactly, asserted before anything else in that file was reported.

The generalisable form, which is this repo's own law arriving in a new place: **a marginal is a
property of an ordering, not of a camera.** Reading one out of a ladder and carrying it as a
set-level cost is the same error class as a moving denominator.

## 2. The projection — invocation and per-view diagnostics

Seven twins, **views pinned as an explicit per-invocation argument** (`--view IDX=PATH` × 7);
the profile's `views` key is untouched and stays the render/mask consumers'. View 2's twin was
not an input.

```
project_twins.py --profile profiles/prop.json --prep E14_prep
  --view 0=TWIN_swordclay_0.png --view 1=... --view 3=... --view 4=...
  --view 5=... --view 6=... --view 7=...   --out stage1/stage1_atlas.png
[profile] prop (prop.json): 16 values applied to project_twins.py
[twins] frame: --fit-axis height margin 1.204 aspect 240,1024 -> h_ext 0.282186 v_ext 1.203993
[twins] N-VIEW mode: 7 cameras at y+000, y+045, y+135, y+180, y+225, y+270, y+315
```

**Registration, per view, as it ran** (halts suspended by profile — `reg-iou-min 0.0`,
`bbox-tol 9.99` — so these print rather than gate):

| view | yaw | IoU(twin, mesh) | centroid offset | keyed OUTSIDE the silhouette | figure width |
|---|---|---|---|---|---|
| 0 | 0 | 0.8019 | 7.2 px | 10,288 px (17.60%), largest CC 6,040 | 196 → 189 used |
| 1 | 45 | 0.9337 | 1.2 px | 207 px (0.55%) | 136 |
| 3 | 135 | 0.9237 | 2.7 px | 679 px (1.76%) | 135 |
| 4 | 180 | 0.8280 | 15.2 px | 8,554 px (15.05%), largest CC 3,811 | 197 → 190 used |
| 5 | 225 | 0.9251 | 2.0 px | 73 px (0.20%) | 136 |
| 6 | 270 | 0.8746 | 6.4 px | 88 px (0.41%) | 51 |
| 7 | 315 | 0.9132 | 3.6 px | 621 px (1.63%) | 136 |

The two face-on views carry 15–18% of their keyed paint outside the silhouette — the drop
shadow beside a wide quillon span, the same artifact handoff 4 recorded at IoU 0.78–0.80. The
A27 trust-intersect removes it before the distance transform, which is what the "196 → 189
used" column is.

**Erosion by structure — the A3 invariant's per-structure report, which is the number to read**
(the invariant forecloses over-erosion by construction, so *violations* are uninformative; area
loss is not):

| stratum (local half-width) | v0 | v1 | v3 | v4 | v5 | v6 | v7 |
|---|---|---|---|---|---|---|---|
| 2–4 px | — | **0.0%** (56 px) | — | — | — | **0.0%** (55 px) | — |
| 4–8 px | 88.9% | 57.7% | 72.7% | 82.0% | 59.0% | 43.3% | 73.3% |
| 8–16 px | 22.2% | 19.0% | 18.8% | 21.8% | 18.4% | 17.3% | 18.8% |
| 16–32 px | 10.1% | 9.0% | 9.2% | 10.1% | 9.4% | 9.7% | 9.3% |
| 32+ px | 4.6% | 3.6% | 3.1% | 4.5% | 3.8% | — | 2.3% |

Monotone in every view above 4 px, exactly as the cost-runs-inversely-with-width law says.
**The 2–4 px stratum exists on two views only and holds 55–56 px each — at that count the
percentage is not a rate**, and it is quoted with its denominator rather than as a 0%.

## 3. Coverage against BOTH ceilings, and the on-surface family

**Banked, not gated** (the E12 24e form):

| | texels | of valid | of the 7-cam ceiling | of the 8-cam comparable |
|---|---|---|---|---|
| valid | 3,661,903 | 100% | | |
| reach, 7 cameras | 1,877,487 | 51.27% | 100% | |
| **STYLED** | **1,729,017** | **47.22%** | **92.09%** | **91.98%** |
| — the beast at its stage 1 | 1,430,687 | 44.2% | | 87.5% of ITS ceiling |

`project_twins` computed its own reachable set at **1,877,487** — the third independent code
path to that number this session, after the shipped ceiling tool and the marginal script.

**The on-surface family (Ruling 9): a bake-side rate is quoted with its island count and its
erode-2 residue, or it is void.**

- islands **46,496** · off-surface at birth **11.0875%** (> 1 px) · **erode-2 residue 0.0085%**
  · margin ratio **8.3×** (21.83% of atlas valid from 2.62% triangle UV area)

| family | denominator | styled share |
|---|---|---|
| ALL VALID (the legacy family) | 3,661,903 | **47.22%** |
| ON-SURFACE (valid eroded 2 texels) | 1,143,291 (31.22% of valid) | **48.45%** |
| the 2-texel MARGIN RING only | 2,518,612 (68.78% of valid) | **46.66%** |

**The two families differ by 1.79 points.** On a subject where 68.78% of valid texels are
margin ring, the restatement barely moves the number — the ring is painted at essentially the
same rate as the interior, because a margin texel inherits its island's geometry and passes or
fails with it. Reported because Ruling 9's whole point is that the bare rate is meaningless
without this; here the answer is that it costs 1.79 points, and now that is on record for this
subject rather than assumed either way.

## 4. ⚠ THE GEM-REGION READOUT (Ruling 19b)

Ruling 19b ruled the gem drift a seed-borne subject fact, let the mixed set stand, and required
that what the blend does to the projected stone be **measured, not predicted**. It is measured.

**The region, twice, because the first cut contains the collar.** The pommel-assembly band is
the gem watch's own rows (87–158), mapped back into 3D through `project_twins`' own frame
expressions — the projection's arithmetic run backwards, not a second derivation. The **stone
alone** is then isolated by a printed geometric landmark: the first local minimum of the mesh's
cross-sectional x-extent below the stone's widest slice (peak 0.05878 at z 0.4620 → first local
minimum 0.03548 at **z 0.4340**, the next slice rising to 0.03988, which is the collar).

| region | valid texels | styled | above C\* 12 |
|---|---|---|---|
| pommel assembly (rows 87–158) | 232,069 (6.34% of valid) | 113,334 | 43,083 |
| **the stone alone (z ≥ 0.4340)** | **177,314** | **88,902** | **19,227 (21.6%)** |

**The stone's post-projection hue composition — 19,227 above-floor texels:**

| band | texels | share |
|---|---|---|
| **wine 0–25 — L5's declared band, garnet** | 3,121 | **16.23%** |
| gold 42–104 | 2,763 | 14.37% |
| lavender 290–310 | 3,557 | 18.50% |
| **magenta 310–360** | 9,471 | **49.26%** |
| forbidden 104–290 | 288 | 1.50% |

**Median hue 308.9, C\* median 20.4.** Lavender + magenta together: **67.76%.**

**Source split:** **78.58% of the stone's styled texels are owned by the drifted views**
(1, 3, 5, 6, 7), 21.42% by the garnet views (0, 4) — close to the 2-of-7 angular share, with
the garnet views slightly under it.

### 4b. Ownership predicts colour, and the seam is the ownership partition

| the stone's above-floor texels, owned by | texels | median hue | wine 0–25 | lav + mag | C\* median |
|---|---|---|---|---|---|
| **the GARNET views (0, 4)** | 4,700 | **17.6** | **65.36%** | 7.70% | 20.9 |
| **the DRIFTED views (1, 3, 5, 6, 7)** | 14,527 | **322.2** | 0.34% | **87.19%** | 20.1 |

**The two territories are 305° apart in hue and they do not bleed into each other.** The
σ = 16 levelling did not homogenise them: median ΔE between the saved facing-weighted blend and
the finished atlas is **2.13 on the stone against 2.58 across the whole styled figure**, so the
levelling touched the stone *less* than the figure's average.

**What that means in one sentence, stated as structure and not as a verdict: the projected
stone is a garnet core inside a magenta shell, and the boundary between them is the ownership
partition rather than any feature of the stone.** `STAGE1_GEM_6x_tight.png` shows it on views 0
and 4 — the two views whose *own* reference carries a garnet stone — with the provenance panel
beside each: the face-on view owns a narrow central stripe of its own stone and the neighbouring
diagonals own the flanks.

**At 6× it does not read as a patchwork.** Both populations are dark (C\* ≈ 20) and the
transition is soft, so the eye sees one violet stone with a redder core rather than adjacent
garnet and magenta facets. **The numbers and the impression disagree in emphasis, and that
disagreement is exactly what goes to the eye.** The brush stage is Ruling 19b's named repair
owner if the blended stone fails there; nothing is decided here.

## 5. Per-view ownership and marginal contribution

| view | yaw | **committed** (texels it WON) | share of styled | reach marginal, turnaround order | its own reach |
|---|---|---|---|---|---|
| 0 | 0 | 278,678 | 16.12% | **822,951** | 822,951 |
| 1 | 45 | 263,591 | 15.25% | 93,484 | 576,939 |
| 3 | 135 | 264,331 | 15.29% | 457,545 | 519,265 |
| 4 | 180 | 251,327 | 14.54% | 314,889 | 743,893 |
| 5 | 225 | 243,005 | 14.05% | 142,228 | 592,390 |
| 6 | 270 | 145,185 | 8.40% | 35,672 | 473,595 |
| 7 | 315 | **282,900** | 16.36% | **10,718** | 671,237 |

Ownership partitions the styled set exactly (the seven counts sum to 1,729,017; asserted).

**The two columns rank the views almost oppositely, and that is the point.** View 7 committed
the **most** texels of any view while contributing the **least** marginal reach — a 26×
inversion. Marginal reach measures what an ordering had left over when a camera arrived;
committed ownership measures which camera faces a texel best. Neither is "how much this view
mattered", and quoting either alone would mislead. The committed counts are strikingly even —
243k–283k across six views, with only the edge-on view 6 low at 145k.

## 6. Where stage 1 left holes — the brush's territory, sized

| | texels | of valid |
|---|---|---|
| valid but unstyled | 1,932,886 | 52.78% |
| — **reachable** by the seven cameras: **the brush's territory** | **148,470** | **4.05 points** |
| — unreachable: dilation's, at finalize | 1,784,416 | 48.73% |

93.34% of unreachable texels are inner wall (Ruling 10b) — the ceiling is a topology fact on
this subject, so the vast majority of that 48.73% is surface no camera can ever see.

| structure (z band) | valid | styled | styled % | reachable hole |
|---|---|---|---|---|
| L5 the stone | 177,314 | 88,902 | 50.1% | 3,840 |
| L3 pommel collar | 78,130 | 36,927 | 47.3% | 105 |
| L4 grip wrap + mid ring | 214,217 | 103,974 | 48.5% | 2,960 |
| **L2/L3 the CROSSING (guard + boss)** | 452,460 | 172,535 | **38.1%** | **10,095** |
| L1 the blade | 2,739,782 | 1,326,679 | 48.4% | 131,470 |

**The crossing is the worst-covered structure at 38.1%, ten points below every other**, and it
is visible as a black band across the guard in every provenance panel of
`STAGE1_flat_strip.png`. Reported, not diagnosed.

## 7. ⚠ The background probe fired high, could not halt, and the follow-up changes the reading

The projection printed, per view, the share of texels the local-half-width relaxation newly
admits that sit within ΔE 10 of the twin's background: **13.83% and 15.41% on the face-ons,
26.06% / 30.30% / 50.68% / 60.15% on the diagonals, 6.23% edge-on** — against the A2 reference
of 0.18%. `prop.json` sets `bg-max-pct 100.0`, a stated suspension (the quantity is rim mixing
and scales with perimeter), so the ANDON was vacuous by design and nothing halted. That is the
profile working as written; the numbers still had to be looked at.

**Two measurements, and together they resolve it.**

**(a) The probe's background reference is a corner median** — `img[:8,:8]` and `img[:8,-8:]` —
which is the keying method this repo has retired three times, used here as a colour reference
rather than as a mask. These twins carry a corner vignette:

| view | corner median (what the probe uses) | backdrop **beside the figure** | ΔE between them | what the probe reported |
|---|---|---|---|---|
| 0 | (168,149,205) | (165,145,201) | **1.5** | 15.41% |
| 4 | (167,148,207) | (161,141,199) | **2.7** | 13.83% |
| 1 | (110, 93,149) | (141,119,186) | **12.2** | 30.30% |
| 3 | (111, 94,151) | (140,119,184) | **11.1** | 50.68% |
| 5 | (110, 92,146) | (143,122,187) | **13.5** | 26.06% |
| 7 | (110, 94,150) | (141,119,185) | **11.7** | 60.15% |
| 6 | ( 86, 72,114) | (136,119,176) | **21.0** | 6.23% |

**The probe reads low where its reference is right and high where its reference is wrong** on
six of seven views. Its percentage is not the quantity its name claims wherever that ΔE is
large — it is measuring distance from a colour the figure never sits against.

**(b) On the finished atlas, what actually got painted is not background.** Every committed
texel compared to its own owning view's background colour:

| view | committed | within ΔE 10 of background | share | median ΔE |
|---|---|---|---|---|
| 0 | 278,678 | 246 | 0.09% | 54.6 |
| 1 | 263,591 | 1,024 | 0.39% | 36.1 |
| 3 | 264,331 | 1,101 | 0.42% | 42.4 |
| 4 | 251,327 | 144 | 0.06% | 53.3 |
| 5 | 243,005 | 297 | 0.12% | 36.0 |
| 6 | 145,185 | 259 | 0.18% | 27.2 |
| 7 | 282,900 | 2,347 | 0.83% | 40.1 |
| **ALL** | **1,729,017** | **5,418** | **0.31%** | |

**0.31% of the projected asset sits within ΔE 10 of background**, against a probe that reported
up to 60% on candidate samples. The probe measures *candidates the relaxation admits* before
the facing, depth and ownership tests; the atlas is what survives all of them. Both numbers are
true of different populations, and only the second is a statement about the asset.

**For a ruling, not decided here:** the probe's reference is the retired corner median and it
moved a reported percentage by roughly 4× on this subject's vignetted views. That is an errand
candidate beside the `e08_ceiling` bias-vs-wall-floor warning already queued.

## 8. The deep-share diagnostic's atlas-side analogue

**Run, with its scope limit stated rather than the number quoted bare.** Depth-from-silhouette
has no atlas-space meaning, so the honest analogue is whether the band survives an erode-2
interior test:

- lavender-rim band (292–314°, C\* > 12) among styled texels: **19,523 = 1.129% of styled**
- of those, interior (survive erode-2, i.e. not island margin): **4,681 = 23.98%**
- for reference, **32.04%** of all styled texels are interior by the same test

The band is somewhat *more* margin-concentrated than styled texels generally. **This answers
"is the band on island margin", NOT "is it deep inside the figure"** — the twin-side diagnostic
remains the instrument of record, and section 4's readout is where the drifted material is
actually accounted for.

## 9. Predictions scored

| # | prediction | outcome |
|---|---|---|
| **P1** | the seven-camera loss is FAR below 18c's 2.8 points | **HELD, and it is the session's finding** — 0.0634 points, 43.8× below the carried price |
| P1 | delta 0.2–1.2 points; ceiling 50.1–51.1%; reach 1,835,000–1,875,000 | **FALSIFIED — every band.** Measured 0.0634 points, 51.27%, 1,877,487. I got the direction right and was still anchored 3× too close to the inherited number |
| P2 | styled/valid 38–46% | **MISSED high** — 47.22% |
| P2 | styled/ceiling 80–92% | **MISSED, at the edge** — 92.09% |
| **P3** | gem source split 55–80% drifted | **HELD** — 78.58% on the stone, 78.51% on the assembly |
| **P3** | lav+mag 40–70%, wine 10–30% | **HELD** — 67.76% and 16.23% on the stone |
| **P3** | the seam falls on ownership boundaries, not on the stone's features | **HELD, and sharply** — garnet-owned median hue 17.6 / 65.36% wine against drifted-owned 322.2 / 87.19% lav+mag |
| **P3** | it will read VISIBLY PATCHY | **NOT AS STATED.** The mechanism is there in full, but at 6× the stone reads as one violet stone with a redder core. The impression and the numbers disagree in emphasis; the eye rules |
| P3 | the region is 5,000–40,000 texels | **FALSIFIED by 4.4×** — 177,314 (stone) / 232,069 (assembly). Atlas area is not proportional to screen area, and I sized it as if it were |
| **P4** | marginal order 0 > 4 > 6 > {1,3,5,7}, diagonals each under 40,000 | **FALSIFIED** — 0 > **3** > 4 > 5 > 1 > 6 > 7; view 3 added 457,545 |
| P4 | view 1 exceeds its 14,049 ladder figure under turnaround order | **held** — 93,484, 6.7× |
| **P4** | committed and marginal rank the views differently | **HELD emphatically** — view 7 committed the most (282,900) on the least marginal (10,718), a 26× inversion |
| P4 | views 0/4 commit 400k–800k | **MISSED** — 278,678 and 251,327 |
| P5 | monotone area loss, thinnest > 40%, blade body < 10% | **held** on every stratum with a real population; the 2–4 px stratum holds 55–56 px and is quoted with its denominator |
| P6 | no ANDON, no view 2, no generation, no pass condition | **held** |

### Where I was most wrong, and it is one habit twice

**P1 and P4 are the same error.** In P1 I said the ladder's position-3 marginal overstates the
set-level cost — and then predicted a delta 3× larger than the truth, because I anchored on the
number I had just argued was wrong. In P4 I wrote the mechanism down explicitly — *"turnaround
order puts view 1 second, before its mirror has been added, so it should score higher than its
ladder figure"* — and then failed to apply that same sentence to view 3, where the effect is six
times larger and reverses the ordering I predicted. **Both times I identified the right
correction and then under-applied it to my own numbers.** Naming a bias is not the same as
removing it from an estimate.

**And a bug of my own, caught and corrected in place.** My first stone-isolating landmark took
`argmin` over a fixed window after the stone's widest slice, which walked past the collar and
landed on the *grip* neck two structures down — producing a "stone" that was 54% gold. The
profile printed in full is what exposed it (a rise from 0.03548 to 0.03988 between the two
minima). The corrected landmark takes the **first local minimum**, and the wrong number is
recorded here rather than quietly replaced.

## 10. What has NOT been done

- **No pass condition invented, and nothing gated.** Both ceilings are comparables; the eye is
  the gate.
- **Nothing armed, nothing bound.** `reg-iou-min` stays 0.0, `bbox-tol` 9.99, `bg-max-pct`
  100.0, the palette report-only; no IoU bound derived (19e).
- **View 2's twin was not an input to anything.** Its camera appears only in the reach
  arithmetic, labelled, as the excluded delta.
- **No strokes, no finalize, no `thin_extent` decision** (stage 2's, still deferred).
- **No fixture, profile or palette edit. No generation. No memory-store write.**
- **Ruling 18c is not amended by me** — §1b reports the measurement and the correction is the
  advisor's to make.

## 11. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The ceiling pre-registered in its own commit before projection; the full invocation recorded with the profile's applied-value count; the seven-view list an explicit per-invocation argument and never a profile edit; every diagnostic in JSON beside its artifacts; the gem landmark's whole cross-section profile printed, which is what caught its own bug |
| ANDON_AUTHORITY | **3** | The stage-1 halt is the gate. The three suspended halts are named as suspended with the profile's stated reasons rather than read as passes; the background probe's inability to fire is reported as a fact about the profile, not glossed; the ownership partition is asserted to sum to the styled set |
| NAMED_COMPENSATORS | **3** | No spend, no generation. New files only under `E14_prep/stage1/`; the projection is repeatable from committed inputs by the recorded invocation; nothing existing was overwritten |
| DECOMPOSE_BY_SECRETS | **3** | The denominator is derived for THIS camera set rather than inherited (§1); the on-surface family separates ring from interior (§3); the gem is separated from its collar by a geometric landmark (§4); committed is separated from marginal (§5) — four places where an aggregate would have hidden the finding |
| UNCERTAINTY_GATED_HUMANS | **3** | No pass condition invented. Section 4's numbers and the 6× impression are reported as disagreeing in emphasis rather than resolved by me; §1b corrects a price without touching the decision it was attached to; the probe follow-up gives both populations and says which one is a statement about the asset |
| EXTERNAL_VERIFIER | **3** | Three independent code paths agree on the reach set — the shipped ceiling tool, this session's marginal script (which asserts both totals before reporting), and `project_twins`' own reachable count; the gem readout uses the band instruments rather than the projector's numbers; the provenance render checks ownership from the geometry side |

---

## HALT — stage 1 staged

`E:\AI\training\facet_next\E14_prep\stage1\`:

```
stage1_atlas.png            the stage-1 atlas (4096, holes at hole-grey)
stage1_atlas_holes.png      the hole map — stage 2's input
stage1_atlas_styled_mask.npy · stage1_atlas_owner.npy · stage1_atlas_blend.png
stage1_sword.glb            the atlas packed onto prep_uv.glb
stage1_provenance_atlas.png · stage1_prov.glb   ownership as colour, holes black
render/stage1flat_{0,1,3,4,5,6,7}.png      FLAT light + Standard transform
render/stage1prov_{0,1,3,4,5,6,7}.png      the provenance renders
STAGE1_SHEET_{0,1,6}.png    reference | asset | provenance, full size
STAGE1_flat_strip.png       all seven, asset over provenance
STAGE1_GEM_4x.png · STAGE1_GEM_6x_tight.png    Ruling 19b's crops for the eye
reach_N7_ceiling.json · reach_N8_replication.json · reach_marginals.json
stage1_readout.json · gem_stone_readout.json · stage1_holes_by_structure.json
stage1_followups.json · projection.log
```

**Four things want the advisor's eye, and none is mine:**

1. **The asset itself**, at the Director's zoom under FLAT light beside its reference — 47.22%
   of valid, **92.09% of this run's ceiling** against the beast's 87.5% at the same stage. No
   pass condition exists and none was invented.
2. **The gem (§4)** — the projected stone's median hue is **308.9**, 67.76% lavender+magenta,
   16.23% in L5's own declared band, and it is a garnet core inside a magenta shell split on the
   ownership partition. Ruling 19b asked for this measured; it is measured, and what to do about
   it is a ruling with the brush named as the repair owner.
3. **Ruling 18c's price (§1b)** — view 2's camera costs the reach ceiling 0.0634 points, not
   2.77. The decision stands on its own grounds; the number attached to it does not.
4. **The background probe (§7)** — its reference is the retired corner median, wrong by ΔE
   11–21 on the vignetted views, and it reported up to 60% where the finished atlas measures
   0.31%. An errand candidate, and a caution for any future arming of that bound.

The crossing is the worst-covered structure at 38.1% styled with 10,095 reachable holes; the
brush's whole territory is **148,470 reachable-but-unstyled texels = 4.05 points of valid**.
Stage 2's lane derives from the hole map when its ruling opens it.
