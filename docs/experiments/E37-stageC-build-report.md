# E37 Stage C — the build, the censuses, and the wash watch: report

**Seat:** executor · **Written:** 2026-08-15 · **Spend: 35 of 80 cloud jobs — unmoved.**
Everything in this document is local and free.

**Why this document did not exist.** Stage C's projection ran at 15:44–15:46, *after*
[Ruling 17](E37-ruling.md)'s commit at 15:40, and the seat that ran it halted on context
before writing it up. Nothing was broken and nothing was lost — every number below was
re-read from the receipts on disk, not inherited from a summary. The dispatch that opened
this seat described the report as a thing to read; **it was not in the tree**, and writing
it is this seat's work. Named here rather than passed over, because a spec that cites a
document nobody can open is the shelf this record exists to avoid.

The build itself is the prior seat's. This seat verified it, measured it, and added what
Stage C still owed: the final censuses, the provenance mix, the wash watch, and the sheets.

---

## 1. The ritual at open

| check | result |
|---|---|
| E15 ritual, scratch `--db` | **PASS** — all four legs, exit **0**; determinism leg **BYTE-IDENTICAL** (12,988,416 bytes, both builds); leg 3 **2,054 pointers checked / 0 dangling**; seeded question set **19 / 19**; **37 experiments**, missing none |
| VRAM watchdog | **ADVANCING** on two reads — heartbeat content 15:53:07.300 → 15:53:59.674, CSV 204,211 → 205,842 bytes. State `ok`, **7,015 of 32,607 MiB — 24,185 below the 31,200 ceiling**. Read as movement, never as the starter's exit code |
| manifest **A** `facet_E33` | **HELD** — 116 declared / 116 present, 0/0/0, 835,059,987 bytes |
| manifest **B** `facet_E34` | **HELD** — 84 / 84, 0/0/0, 177,563,094 against declared 177,563,094 |
| manifest **C** eight subtrees | **HELD** — 7,312 files / 17,072,807,610 bytes, delta **+0 / +0** |
| manifest **D** `facet_E35` | **HELD** — 335 / 335, 0/0/0, 284,096,148 against declared 284,096,148 |

Every receipt landed in `E:\AI\training\facet_E37\close\` — **outside every protected tree**,
gate C's destination guard checked over all twelve roots before the first walk.

The E15 figures differ from this arc's open (12,562,432 bytes / 1,993 pointers) by the
commits landed since, which is what a growing record does.

---

## 2. T72 — the RGBA turnaround tool lands

Commit [`676cab8`](https://github.com/mcp-tool-shop-org/facet/commit/676cab8), pushed,
**CI green — run `31906201987`, 11m49s.**

The tool and its six tests were written by the prior seat and left uncommitted because
landing them takes the corrected order. Run here in full:

| step | result |
|---|---|
| pin edits | tool-count surfaces, below |
| **FULL suite** | **25 failed / 1028 passed**, 807.94 s — all 25 are T34 count sites, the expected shape of a test-adding commit before its surfaces move |
| collect | full **1053**, hermetic **1008**, gap **45** (unmoved) |
| the 16 T34 surfaces | moved across 6 files, plus the digits leg across all 8 READMEs |
| census last | `test_files` **71 → 72**; `corpus_files` unmoved at 330 |
| after | T34 + T41 **91/91**; with T72 **97/97** |

**The counts:** full **1047 → 1053**, hermetic **1002 → 1008**. T72 adds six tests.

### The tool count moved, and a site the previous sweep missed

`tools/` root now holds **40** `.py`, four of them published `py-modules`
(`facet_index`, `record_mcp`, `measure_mcp`, `subject_profile`), so the unpublished
population is **36**. Six English sites moved 35 → 36 — and **a seventh**, `SHIP_GATE.md`
item *"File operations constrained to known directories"*, phrases the same quantity as
*"the 35 research scripts"* and was invisible to the previous sweep's grep, which keyed on
`unpublished` and on the spelled cardinal.

Named rather than quietly fixed: this is the record's own *when you fix a root cause, find
its other consumers* landing on a sweep written one commit earlier. The sweep that found it
was `35 research|36 research|35 tools|36 tools|of thirty`, read complete rather than paged.

### ⚑ Seven translated READMEs carry the tool count at THIRTY-FOUR — NOT fixed here

Stale by two moves now (34 → 35 was missed, 35 → 36 is this commit), and **six of the seven
spell the cardinal in the target language**:

| file | as written | form |
|---|---|---|
| `README.ja.md` | `34個のツールのうち2つ` | digit |
| `README.zh.md` | `two tools of thirty-four` | English, untranslated |
| `README.es.md` | `dos de las treinta y cuatro herramientas` | Spanish |
| `README.fr.md` | `deux des trente-quatre outils` | French |
| `README.hi.md` | `तीस-चार में से दो उपकरण` | Hindi |
| `README.it.md` | `due dei trentaquattro strumenti` | Italian |
| `README.pt-BR.md` | `duas das trinta e quatro ferramentas` | Portuguese |

Writing *thirty-six* into those sentences is a **translation act**, not the digits-only
repair [E35](E35-ruling.md) Ruling 5 permits an executor, so they are reported and left to
the advisor's hands. `README.ja.md:178` additionally carries an untranslated English
fragment. The **test**-count digits in all eight READMEs moved as usual — those are digits.

---

## 3. The build, as it stands

The chain [Ruling 11](E37-ruling.md) corrected, run end to end by the prior seat:

```
perf_300k.glb  ──►  cull_unseen  ──►  bake_hero_prep  ──►  project_twins  ──►  texpass_finalize  ──►  performer_v3.glb
 smart_decimate                                            (the locked 8)      (surface-aware)
 --target 300000
```

`performer_v3.glb` — **23,076,152 bytes**, sha256 `cddc9b02199d39e9…`, on disk and unmoved
by this seat.

### The locked eight, with each view's seed

[Ruling 17](E37-ruling.md)'s set, and the Stage-B register readings that ride it:

| view | yaw | seed | role | Stage-B dark count / area | Stage-B reg-IoU | Stage-B register C\* |
|---|---|---|---|---|---|---|
| 0 | 0° | 770700 | kept | 16 / 157 | 0.9559 | 23.30 |
| 1 | 45° | 202608151 | re-roll | 17 / 69 | 0.9404 | 30.68 |
| 2 | 90° | 770700 | kept | 10 / 50 | 0.9116 | 29.90 |
| 3 | 135° | 2026081503 | roll 3 | 15 / 71 | 0.9291 | 39.97 |
| 4 | 180° | 770700 | kept | 12 / 54 | 0.9463 | 26.00 |
| 5 | 225° | 770700 | kept | 16 / 84 | 0.9354 | 24.41 |
| 6 | 270° | 202608156 | re-roll | 39 / 233 | 0.9592 | 38.94 |
| 7 | 315° | 20260815007 | probe P3, `cn_strength` 1.0 | 50 / 248 | 0.9467 | 29.93 |

Twin totals over the locked eight: **175 count / 966 px²**.

### The projection

| quantity | value |
|---|---|
| atlas | 4096², **valid texels 2,418,614** |
| frame | 368 × 1024, `--fit-axis height --margin 1.204` |
| **styled / REACHABLE** | **2,221,222 / 2,268,219 = 97.9%** |
| styled / valid | 2,221,222 / 2,418,614 = 91.8% *(legacy — the denominator includes texels no camera can see)* |
| reachable / valid | 2,268,219 / 2,418,614 = 93.8% |
| holes before fill | 197,392 |
| atlas variance | 0.03625 → **0.03997** after fill |

**Registration, per view, against its own silhouette** — the projection key, no floor fired:

| view | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| reg-IoU | 0.9091 | 0.8975 | 0.8671 | **0.9158** | 0.9115 | **0.8241** | 0.9283 | 0.9106 |

All eight clear the 0.80 floor. **v3 — the view that halted Stage C twice — sits at 0.9158**,
the third-highest row.

Two views carry the tool's own bbox NOTE (diagnostic, not a halt): **v2** keyed bbox
848×247 against a silhouette 849×129, and **v5** 849×310 against 849×234 — the twin painting
outside the figure's extent, most likely a cast shadow, and the trust mask no longer reads
it. v5 is also the lowest reg-IoU of the eight. Recorded; not chased.

### Both fill gates passed, with their thresholds

`texpass_finalize`, surface-aware mode. The gates are declared in the tool, not inferred:

| gate | threshold | measured | |
|---|---|---|---|
| median source distance | `--max-edge-median` **3.0** median triangle edges | **1.366** | pass |
| share of lookups beyond 20 edges | `--max-frac-beyond` **0.05** | **0.0034** (0.34%) | pass |

Reported beside them, gated by neither: `mean_fallback` **0**, normal disagreement > 60°
**27.93%**, back-facing **20.84%** — the diagnostic [E07](E07-ruling-gate1.md) demoted from
a gate after its proxy inverted on this route's own geometry.

---

## 4. Requirement 4 — the RGBA turnarounds, and the check that could have been fooled

Eight frames written, **none flat-255** (the tool's own end-of-run ANDON). Alpha is the
raycast silhouette copied in, so the composite is exact by construction rather than accurate
to a tolerance.

`silhouettes.json` reports view 0 and 4 at **93,289 px to the digit**, 1/5 at 92,128, 2/6 at
53,705, 3/7 at 91,436. Under an orthographic camera that is an identity — the ray set at yaw
θ and yaw θ+180 is the same set of lines — but **a tool that wrote one mask twice produces
the same agreement**. So the check asked whether each pair is a *mirror* and *not a copy*:

| pair | px | identical? | mirror-identical? | IoU(mirror) | IoU(copy) |
|---|---|---|---|---|---|
| 0/4 | 93,289 / 93,289 | **False** | **True** | 1.000000 | 0.894616 |
| 1/5 | 92,128 / 92,128 | **False** | **True** | 1.000000 | 0.458506 |
| 2/6 | 53,705 / 53,705 | **False** | **True** | 1.000000 | 0.582538 |
| 3/7 | 91,436 / 91,436 | **False** | **True** | 1.000000 | 0.483243 |

Exact mirrors, IoU 1.000000, and copy-IoU as low as 0.46 — the two hypotheses separate
cleanly. The masks are per-view geometry.

The provenance renders were checked against the same masks before going on a sheet:
**zero silhouette pixels fall outside the provenance render's foreground** on all eight
views, with the excess entirely an outward 1-px anti-aliasing rim (+1,285 to +3,001 px). A
misalignment would be two-sided; this is one-sided.

---

## 5. The censuses — both classes

### The dark class, on the eight finished renders

`twin_despeckle --mode census`, at the recorded threshold, **each view against its own
silhouette**:

| view | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | **total** |
|---|---|---|---|---|---|---|---|---|---|
| count | 151 | 202 | 83 | 291 | 154 | 181 | 67 | 193 | **1,322** |
| area px² | 752 | 796 | 429 | 1,067 | 574 | 590 | 281 | 706 | **5,195** |
| largest component | 35 | 32 | 31 | 29 | 30 | 35 | 33 | 31 | **35** |
| % of figure | 0.806 | 0.864 | 0.799 | 1.167 | 0.615 | 0.640 | 0.523 | 0.772 | |

⚠ **This has no baseline in the record.** Nothing in this repo has ever censused a composed
asset's renders — every recorded census is of a *twin*. So the 1,322 / 5,195 px² above is
stated as a numerator and a denominator and **no bound is invented for it**; the twin totals
for the same eight views (175 / 966 px²) measure a **different object** — the paint source,
before projection, fill, geometry and flat-light shading — and are not a baseline either.
The largest component holds at **29–35 px²** across all eight views, well inside the class's
keyed threshold of 36.

### The dark class, on the atlas

**NOT YET RUN.** Started at 16:32 and still executing at the time of writing (450 s CPU,
26.4 GB working set) — the instrument's local-median window is expensive at 4096². It is
written `NOT YET RUN` rather than given a plausible number, and its scale boundary is stated
in advance so nobody compares it to the render row: the keyed threshold is an **absolute**
36 px², and this route paints roughly **8.6 atlas texels per render pixel**, so 36 texels on
the atlas is about 4.2 px² in a render. The atlas census asks a *smaller-featured* question
than the render census; the two are not comparable and the derivation is written here rather
than after the number lands.

### The pale class — measured where it can occur

The pale class is surface the reference could not reach, wearing fill instead of paint. That
population is known exactly: styled (2,221,222) and fill (197,392) partition valid
(2,418,614) with **zero overlap** — checked, not assumed. So the fill is measured against
**the paint it actually touches**, each patch against its own 3-px surround, never against a
global figure statistic.

| | fill | ring (styled, within 3 px) | Δ |
|---|---|---|---|
| L\* median | 50.50 | 57.85 | **−7.35** |
| C\* median | 26.10 | 29.39 | −3.29 |

**In aggregate the fill is DARKER than its surround, not paler** — the class does not
present at whole-asset scale.

**And the total alone would have said the wrong thing.** Two thresholds, per the record's own
rule — 20,426 components, largest 9,876 texels:

| component area | fill L\* | ring L\* | ΔL\* | |
|---|---|---|---|---|
| **9,876** | 56.77 | 40.35 | **+16.43** | paler |
| **7,590** | 72.69 | 48.64 | **+24.05** | paler |
| 4,669 | 50.04 | 39.31 | +10.73 | paler |
| 4,405 | 32.78 | 48.83 | −16.05 | darker |
| 4,053 | 42.93 | 43.48 | −0.55 | — |
| 2,504 | 64.02 | 60.74 | +3.28 | — |

The two largest fill components are **16.4 and 24.1 L\* lighter** than the paint they sit
against, at 0.41% and 0.31% of valid texels. Whether either reads as a patch is the
Director's eye at the sheet; they are located in the provenance panels as magenta.

---

## 6. ⚑ THE WASH WATCH — [Ruling 9](E37-ruling.md)'s question, answered

Ruling 9 carried the wash finding into Stage C **by name**: three arrivals landed above the
kept five's register C\* range, the risk was named as composition-level cross-view tonal
banding, and *"projection's seam-sigma levelling is the mechanism that may absorb it, the
Stage-C sheets and census answer whether it did."* Two outcomes were named in advance. This
is the measurement.

**Method.** The composed atlas is partitioned by its **owner map** — which camera won each
texel — and read on the same axis the Stage-B guard used. Hue is quoted with its chroma and
as a **circular** mean of unit chromatic vectors above a C\* 2.0 floor; the arithmetic mean
of angles has already reported a +49.1° move here where the truth was −8.4°.

| owner | texels | L\* median (p10–p90) | C\* median (p10–p90) | hue (circ) | Stage-B twin C\* |
|---|---|---|---|---|---|
| 0 | 267,298 | 65.05 (44.5–73.9) | **23.63** (19.9–26.6) | 73.6° | 23.30 |
| 1 | 350,002 | **34.69** (25.0–57.9) | 30.23 (23.1–33.8) | 63.1° | 30.68 |
| 2 | 181,560 | 68.66 (54.2–82.2) | 33.40 (25.5–38.0) | 69.3° | 29.90 |
| 3 | 288,848 | 59.13 (44.4–67.0) | **39.54** (34.7–44.6) | 69.6° | 39.97 |
| 4 | 277,475 | 61.48 (48.2–69.3) | 27.16 (24.8–29.6) | 69.9° | 26.00 |
| 5 | 308,202 | 59.81 (42.3–67.3) | 25.64 (21.3–30.2) | 70.4° | 24.41 |
| 6 | 184,862 | **73.60** (58.1–84.4) | 38.99 (27.0–47.0) | 70.6° | 38.94 |
| 7 | 362,975 | 49.03 (32.3–60.4) | 28.57 (23.7–33.3) | 65.7° | 29.93 |

**C\* median spread across owners: 15.90** (23.63 → 39.54).
**L\* median spread across owners: 38.91** (34.69 → 73.60).

**The levelling did not absorb it.** Every owner's composed C\* tracks its own twin's
Stage-B register C\* — 38.94 → 38.99, 39.97 → 39.54, 30.68 → 30.23, 23.30 → 23.63. The two
statistics are over **different populations** (the Stage-B figure is a register region of a
twin; the composed figure is every styled texel that owner won), so the correspondence is an
observation and not an identity — but the spread that entered the projection is the spread
that came out of it.

### The seam, separated from ordinary variation by its own null

A cross-owner step cannot be read alone: the camera that wins a texel is the one facing it,
so an owner boundary falls exactly where the surface turns away — which is where shading
changes anyway. So each pair carries a **null**: the same owner's texels at boundary distance
[0,3) against its own texels at [3,6), the same 3 px of separation at the same place.

| pair | n | cross dE76 | null (same owner) | cross / null |
|---|---|---|---|---|
| 0\|1 | 25,708 | 30.288 | 0.561 | **53.99×** |
| 2\|7 | 202 | 19.083 | 0.814 | 23.44× |
| 5\|6 | 12,567 | 23.401 | 1.147 | 20.40× |
| 0\|7 | 26,476 | 18.354 | 1.224 | 14.99× |
| 6\|7 | 22,757 | **37.039** | 2.587 | 14.32× |
| 1\|2 | 18,519 | **47.088** | 3.625 | 12.99× |
| 1\|3 | 6,841 | 23.884 | 2.165 | 11.03× |
| 3\|4 | 16,417 | 18.425 | 2.450 | 7.52× |
| … | | | | |
| 2\|3 | 10,090 | 5.823 | 5.034 | 1.16× |

**16 pairs read** (12 skipped below a 200-texel floor, reported rather than dropped):
cross dE76 median **18.39**, null median **2.76**, **ratio median 7.37×, max 53.99×**.

The step is not what this atlas does over any 3 px there. It is the seam.

### And it is visible, at the Director's zoom, on the head

`sheet_head_3x_prov.png` puts the candidate head at 3× directly above the provenance render
of the **identical crop**. The tonal band edges sit on the owner edges — the vertical step
down the middle of v0's face, v1's dark band, v7's — so the co-location is shown rather than
asserted.

**Reported, not judged, and not gated.** Ruling 9 put the verdict at the Director's zoom on
the composed asset, and Ruling 15 explicitly left v3's out-of-range C\* for him to veto
there. Nothing here has a threshold.

---

## 7. Provenance mix, and a band that was never sealed

| provenance | texels | % of valid |
|---|---|---|
| **styled** — from the eight twins | 2,221,222 | **91.84%** |
| **fill** — surface-aware | 197,392 | **8.16%** |
| valid | 2,418,614 | |

⚠ **The Stage-C provenance band does not exist.** The kickoff's *Blind bands* section says
the sealed file would carry *"the Stage-C provenance expectation against E34's 98.4%/95.1%
styled/reachable, three branches per hypothesis, the UP branch live."*
[E37-stageB-blind-bands.md](E37-stageB-blind-bands.md) is **Stage-B only** — H1 through H4,
all about twins — and no Stage-C band was ever written or sealed.

So this row has **no pre-registered expectation**, and none is invented now: measuring first
and choosing the bar afterwards is the one move that is always wrong. E34's recorded
**98.4% styled/reachable and 95.1% reachable/valid** are cited as *reference context only* —
they were measured on **a different mesh** (E33's), and reachability is a property of
geometry, so they are not a bar this asset could pass or miss. E37 measures **97.9%** and
**93.8%**. Numerator and denominator, and the Director's eye.

---

## 8. The sheets

Built before the numbers were argued, per the record's own ordering.

| sheet | what it answers | size |
|---|---|---|
| `sheet_ref_cand_prov.png` | reference \| candidate \| provenance, per view, **full size, no downscale** | 1136 × 8472 |
| `sheet_rgba_vs_plate.png` | the RGBA turnaround over a checkerboard beside the approved source plate | 4048 × 1092 |
| `sheet_head_3x.png` | the head at 3×, box **derived per view** from that view's own silhouette | 3522 × 558 |
| `sheet_head_3x_prov.png` | the same head crop with provenance directly beneath it | 3522 × 1092 |

The provenance panel is a **real render of a real GLB** whose texture is the owner map
(`bake_hero_pack` → `turn_render` at the recorded convention), so it is registered to the
candidate by construction rather than by a coordinate guess. Styled texels wear their owning
camera's tint; the fill is magenta.

The head box is derived per view — 130–166 px wide against a fixed 172 px band — never a
pixel rectangle inherited from another subject. The source plate is the Director-approved
round-2 clay, re-hashed at this seat: `a4bcf2501414f769d4164ba910803f6d7882e98747897f5f256be801c75fb3b2`, 1328 × 1328.

---

## 9. What this seat did not do

- **No prediction was made before measuring.** The artifacts existed before this seat opened,
  so a blind band here would have been written with the receipts already on disk. Ruling 9's
  two-outcome fork *was* pre-registered and is resolved above; everything else is reported as
  numerator and denominator with no bar.
- **The atlas dark census is still running** and is written `NOT YET RUN`.
- **Nothing was delivered.** No manifest of `facet_E37`, no read-only pass, no relay to
  armature. Stage D fires on the Director's word and only on it.
- **No protected tree was written to. No cloud job fired.** Spend stands at **35 of 80**.

## 10. Artifact homes

Everything this seat wrote is under `E:\AI\training\facet_E37\close\`:
`e15_scratch.db` · `open_manifest_{E33,E34,E35,C}.json` · `suite_full.txt` ·
`census_before.json` · `e37_stagec_census.py` + `stagec_census.json` ·
`e37_boundary_null.py` + `boundary_null.json` · `e37_pale_class.py` + `pale_class.json` ·
`e37_stagec_sheets.py` · `census_renders.json` · `atlas_valid_mask.png` ·
`provenance_atlas.png` · `provenance.glb` · `turn_prov/` · the four sheets.

## 11. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | every instrument invoked by absolute path with its flags recorded here; the locked eight pinned by seed per view; limit: the sheet scripts live in the arc tree, not under `tools/`, following this arc's own precedent |
| ANDON_AUTHORITY | 3 | the receipt-destination guard `raise`s over all twelve protected roots before the first read; the styled/fill overlap check `raise`s; T72's six ANDONs re-run under `-O` and `PYTHONOPTIMIZE=1`; the atlas census is written `NOT YET RUN` rather than estimated |
| NAMED_COMPENSATORS | 3 | the kickoff's table stands unchanged; this seat's only irreversible acts are one commit (revert by commit, pathspec-scoped) and writes under `facet_E37\close\` (remove the tree; re-derivable from the scripts listed above) |
| DECOMPOSE_BY_SECRETS | 2 | each measurement is its own script with its own operands and its own receipt; the null lives beside the statistic it qualifies rather than inside it |
| UNCERTAINTY_GATED_HUMANS | 3 | the seat halts at Stage D with the sheets on the screen; the wash finding is carried to his eye by Ruling 9's own instruction, not smoothed; no threshold is invented anywhere in this document |
| EXTERNAL_VERIFIER | 2 | the mirror check and the boundary null are both constructed to be able to fail, and both discriminate; identity and acceptance remain the Director's, which is the design |
