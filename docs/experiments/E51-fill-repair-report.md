# E51 report — repainting the fills so the fill pass cannot cross a material edge

Executor seat (Sonnet tier), dispatched 2026-08-17 by the advisor seat. Dispatch:
`docs/experiments/E51-fill-repair-kickoff.md`. Work tree:
`E:\AI\training\facet_E51\` (`handoff.md` kept current through every step,
`predictions.md` written before `fill_repair_e51.py` ran). No GPU, no cloud spend —
every input was already on disk.

No word below asserts that any result is good, working, fixed, or improved. Every
number is a measurement; the sheets under `E:\AI\training\facet_E51\sheets\` are the
artifact for the Director's eye. Per a standing rule received mid-task, this report
paraphrases the Director's own rulings rather than quoting them, and does the same for
every prior document's quoted text it would otherwise have repeated.

**A steering correction received mid-task, load-bearing for how this whole report must
be read, stated here before anything else.** This arc's own dispatch inherited a
hypothesis from the E49 kickoff: that `orphan_fill.py`'s boundary-crossing sample is
what carries the flat-coloured patches the Director named in his review of E49. E50 (a
separate, dedicated diagnosis seat, out of this seat's scope throughout — its own work
tree was never read or touched) finished after this arc's own technical work was
already complete, and measured that premise directly: the patches are NOT carried by
either fill pass. `orphan_fill`'s own population is DEPLETED at the patches (found at
roughly 0.27x the base rate — less likely to be a patch than a random texel, not more),
the within-island fill population sits close to the base rate (roughly 1.18x), and the
patches themselves are found 90-99% on texels the MAIN paint pass wrote — not on the
output of any fill or repair step. E50's own causation finding is stated as decisive: the
same defect is already present in a render built from an atlas that predates
`orphan_fill.py`'s own existence, and a repair cannot cause a defect that predates it.

**Consequence for every claim in this report.** This arc's two arms are not, and are not
framed below as, a repair of the polygon-shapes defect the Director named. They remove a
narrower, independently-justified defect — a texel painted with a colour no view
supports for it — on their own terms, regardless of whether that population turns out to
be the one behind the visually-named patches. E50's own measurement says mostly not.
This seat has no instrument for "the patches" as E50 defines and detects them (out of
scope, and E50's own tree was never read), so nothing below confirms or denies whether
this arc's arms moved them. Where this report's own measurements (Section 6) touch the
same question from a different angle, they are presented as a separate, narrower
measurement using a different instrument, consistent in direction with E50's own finding
but not the same finding — and if any measurement below had come out the other way, that
would contradict E50 and would be reported as a contradiction, not as a success. None
did.

## 0. What this arc changed, in one paragraph

`E:\AI\training\facet_E49\orphan_fill.py` samples a zero-written-island texel from the
best-facing twin using the fully UNERODED silhouette. Because atlas islands at this
mesh's fragmentation are frequently single triangles, a boundary-adjacent sample taken
without erosion CAN reach across a material seam and flat-fill a triangle-sized island
with the neighbouring material's colour — a real, code-level fact about what that one
sampling step is capable of doing, true independent of the front-matter correction
above, which is about what this specific mesh's own patches turned out to be caused by,
not about what the mechanism can do in principle. This arc replaces that one sampling
step with two arms — arm A re-samples using this repo's own capped-eroded silhouette
(the same bundle E49's step 2 already painted against), and arm B gives texels no view
can support under that eroded silhouette a neutral fill derived from nearby
already-painted surface — both gated by `tools/palette_gate.py`'s declared bands, reused
rather than re-rolled. E49's own tree (`facet_E49\`) was read only, never written; this
arc's own output lives entirely under `facet_E51\`.

## 1. Predictions, written before `fill_repair_e51.py` ran (full text: `predictions.md`)

| | stated | measured | result |
|---|---|---|---|
| P1 — owner arm A candidates | exactly 0 (analytic certainty, not a guess — the owner-mode candidate test and E49's own step-2 owner-mode "written" test are the identical predicate against the identical bundle) | 0 / 117,024 (per-view pass count under the eroded sil is `[0,0,0,0,0,0,0,0]`) | **confirmed exactly** |
| P2 — blend arm A candidates | hard upper bound 132,152 (analytic, subset argument); soft band 26,000-118,937 (20%-90% of E49's own blend count, disclosed as uncertain) | 124,763 | **hard bound holds (124,763 < 132,152); soft band missed narrowly on its upper edge** (measured is 94.4% of E49's count, ~5,800 above the band's own edge) |
| P4 — arm A refusal rate | 0%-5% of candidates | blend 0.322% (402/124,763); owner vacuous, 0 candidates | **confirmed (blend); not scored (owner)** |
| P5 — arm B refusal rate | 0%-8% of population | owner 1.804% (2,111/117,024); blend 1.772% (2,502/141,186) | **confirmed, both modes** |
| P6 — final sentinel share of all valid texels | owner 0.5%-4.0%; blend 1.0%-5.0% | owner 0.0879%; blend 0.1209% | **missed, both modes, below the band's own lower edge** (recovery further below E49's own no-view-visible share — 4.65%/5.57% — than the band anticipated) |

**A correction to P2's own analytic argument, found while reconciling the cross-tab
below, not before running anything.** P2's hard upper bound reasoned that "valid under
the eroded sil" implies "valid under the uneroded sil" because `sample_view`'s `tap`
component is monotonic in the silhouette (a smaller silhouette can only fail `tap` more
often). That is true for `tap` alone. It is not rigorously true for the full
`valid = tap & z_ok` predicate, because `z_ok`'s tolerance (`visibility_tau`, via
`_figure_iqr(depth, sil)`) is itself a statistic computed FROM the silhouette in use —
measured directly (`S.visibility_tau` on both bundles, all 8 views): view 5's eroded-sil
tau (0.005566) is measurably LARGER than its uneroded-sil tau (0.005556). This is why
13 blend texels (12 accepted, 1 refused) that E49 recorded as unrecoverable even under
the fully uneroded silhouette (`no_view_visible_mask`) nonetheless produced an arm-A
candidate in this run — out of 133,797 in that population (0.0097%). The hard bound's
own conclusion (124,763 < 132,152) still holds; the argument that was offered for it was
incomplete, and is corrected here rather than left standing.

## 2. What ran

| step | tool | result |
|---|---|---|
| lab_to_srgb self-test | `fill_repair_e51.py`'s own `_selftest_lab_roundtrip` | max abs error 1.035e-14 over 4,096 random colours + 3 anchor points (white/black/grey), exit continues (would `Andon` above 5e-4) |
| Main repair | `fill_repair_e51.py`, both modes | exit 0, no `Andon` fired — Gate A held, Gate B held, both real-`palette_gate.py` cross-checks held |
| Render | `facet_E47\render_atlas_swap.py` (unmodified, reused directly), Blender `-b -P`, PowerShell | both modes exit 0, 16 PNGs (8+8), spot-checked shape (1024,752,4) and mean/std against E49's own `renders_*_complete` and the shipped baseline — consistent to two decimal places (owner mean 141.68 vs E49's own 141.71, shipped 141.19) |
| Sheets | `build_sheets_e51.py` | exit 0, 16 sheets (8 views x 2 modes), no missing panels |
| Cross-tab | `cross_tab_e51.py` | exit 0, population-equality check held (this arc's orphan set is byte-identical to E49's own `orphan_fill_mask \| no_view_visible_mask`, both modes) |

Full logs: `run_fill_repair_e51.log`, `step_render_owner.log`, `step_render_blend.log`,
`step_sheets.log`, `step_cross_tab.log`, all under the work tree.

## 3. The sheet

`reference | shipped | E49-complete | E51-complete`, native 752x1024 per panel,
provenance captions with sha256 per panel, one sheet per view per mode:

```
E:\AI\training\facet_E51\sheets\owner\sheet_owner_v00.png .. v07.png
E:\AI\training\facet_E51\sheets\blend\sheet_blend_v00.png .. v07.png
E:\AI\training\facet_E51\sheets\manifest.json
```

Views 0, 1 and 7 additionally carry 2x-zoom crop rows on the tunic, skirt and
boot-tops regions — found already declared (PROPOSAL, not a ruling) in
`tools/s3_sheet_regions.json`, transcribed there from an earlier contact-sheet pass,
and reused directly rather than re-derived: view 0 gets tunic + skirt, view 1 gets
tunic, view 7 gets boot_tops.

**Descriptive, not evaluative, and not a claim about the Director-named patches.** In
every crop row and every full view checked (0, 7 in both modes, visually inspected in
full at the resolution shown above), the small bright-magenta triangular flecks visible
on `E49-complete` are not visible, at this crop scale, on `E51-complete` in the same
views. This report does not characterise that as an improvement, and per the
front-matter correction above, it is not evidence about the polygon-shapes defect
either way — Section 5's own atlas-space accounting shows these magenta flecks are
overwhelmingly the pre-existing, already-disclosed `no_view_visible` sentinel
population (texels no view could sample even under the fully uneroded silhouette,
never painted by `orphan_fill.py` at all), and E50 measured that population's relation
to the patches independently of anything this seat touched. What this sheet shows is
this arc's own arms' output, at the crop scale a human would judge it at; it is not a
before/after of the defect the Director named. All 16 sheets should be viewed
directly; this report does not attempt to describe all of them in prose.

## 4. Per-arm counts

| | owner | blend |
|---|---|---|
| orphan set (unchanged from E49 steps 2-3) | 117,024 | 265,949 |
| **arm A** — candidates found | 0 | 124,763 |
| arm A — accepted (repainted) | 0 | 124,361 |
| arm A — refused by the palette gate | 0 | 402 |
| **arm B** — population (no eroded-sil sample anywhere) | 117,024 | 141,186 |
| arm B — accepted (filled) | 114,913 | 138,684 |
| arm B — refused by the palette gate | 2,111 | 2,502 |
| arm B — zero chroma-qualified voters among K=25 neighbours (degenerate, literal neutral grey) | 24,121 | 29,224 |
| **final sentinel (this arc)** | **2,111** | **2,904** |

**What became of the refused.** A refused texel is not retried by the other arm and is
not given a fallback guess — it is left exactly as `atlas_filled.png` (E49's own
within-island-fill output, before either arc's own orphan/fill-repair step) already had
it, which for every texel in the orphan set is the pipeline's own `DEFAULT_SENTINEL`
magenta (255,0,255). This is confirmed, not assumed: the cross-tab (Section 5) shows
every "stayed sentinel in both E49 and E51" cell reads a Lab deltaE of exactly 0.0
between old and new, 100% of pixels unchanged.

**External verification of the gate, real tool, both directions.** `tools/palette_gate.py`
itself (unmodified, invoked as a subprocess, `--report-only`) was run against every
accepted and every refused mask, as real PNGs against the real atlas:

| | owner arm B accepted | blend arm A accepted | blend arm B accepted | owner arm B refused | blend arm A refused | blend arm B refused |
|---|---|---|---|---|---|---|
| n | 114,913 | 124,361 | 138,684 | 2,111 | 402 | 2,502 |
| off-palette (real tool) | 83 (0.0722%) | 15 (0.0121%) | 81 (0.0584%) | 2,111 (100.0000%) | 402 (100.0000%) | 2,502 (100.0000%) |
| largest blob | 11px | 2px | 11px | 84px | 57px | 84px |

Every refused mask reads 100.0000% off-palette under the real, unmodified tool — the
refusals are not an artifact of this arc's own in-memory replica of the palette test.
Every accepted mask reads under 0.1% off-palette under the real tool (this arc's own
0.5% andon tolerance for this comparison did not fire) — attributable to uint8 PNG
quantization at texels sitting near a declared band's own edge, not to a disagreement
between the replica and the shipped tool.

## 5. What left, what arrived — atlas space (exact per-texel accounting)

Cross-tabulated against E49's own two saved masks (`orphan_fill_mask.npy`,
`no_view_visible_mask.npy`), which this arc's own orphan set was confirmed identical
to before any cross-tab number is reported (population-equality `Andon`, did not fire).

**Owner** (arm A recovers nothing here, per P1 — the entire orphan set was reclassified
by arm B alone):

| E49's own class (n) | -> arm B accept | -> arm B refuse |
|---|---|---|
| orphan_filled (5,199) | 5,151 (deltaE old-vs-new: median 9.28, mean 13.80) | 48 (deltaE: median 147.12) |
| no_view_visible (111,825) | 109,762 (deltaE: median 124.56 — magenta replaced by real paint) | 2,063 (deltaE 0.0 — stayed magenta) |

**Blend:**

| E49's own class (n) | -> arm A accept | -> arm A refuse | -> arm B accept | -> arm B refuse |
|---|---|---|---|---|
| orphan_filled (132,152) | 124,349 (deltaE: median 0.0, mean 1.68 — 93.4% of these are unchanged to within deltaE 1) | 401 (deltaE: median 135.05 — E49's own colour replaced by magenta) | 7,310 (deltaE: median 10.89) | 92 (deltaE: median 135.45) |
| no_view_visible (133,797) | 12 (deltaE: median 134.52 — magenta replaced by real paint; the P2 correction's anomalous population) | 1 (deltaE 0.0 — stayed magenta; the anomaly's other member) | 131,374 (deltaE: median 124.28) | 2,410 (deltaE 0.0 — stayed magenta) |

Reading this table plainly: of blend's 132,152 orphan-filled texels, 124,349 (94.1%) are
re-sampled by arm A under the stricter eroded silhouette and land within one deltaE
unit of E49's own colour 93.4% of the time (the boundary-crossing risk did not apply to
these — a safe, non-boundary source view existed and both arcs found it). The remaining
5.9% (401 + 7,310 + 92 = 7,803) either lose their eroded-sil sample entirely and fall to
arm B, or are refused outright — this is where a colour actually changes or a texel
loses its paint.

## 6. What left, what arrived — view space (rendered pixels), and this seat's own measurement of the causation question

**Space, stated explicitly, per this repo's own law that a share measured in one space
is not a claim about another.** All counts above are atlas texels. Projected through
`surfid` (per `tools/emit_view_aovs.py`'s own convention, `surfid[y,x] = row*4096+col`)
into each of the 8 rendered views, the same classes occupy a few tens to a few hundred
screen pixels each, against a per-view figure size of 90,553-149,780px:

| view | old: orphan_filled | old: no_view_visible | new: arm_a_accept | new: arm_a_refuse | new: arm_b_accept | new: arm_b_refuse |
|---|---|---|---|---|---|---|
| 0 (owner/blend) | 40 / 61 | 158 / 170 | 0 / 21 | 0 / 0 | 196 / 209 | 2 / 1 |
| 1 (owner/blend) | 51 / 103 | 99 / 107 | 0 / 50 | 0 / 0 | 148 / 158 | 2 / 2 |
| 7 (owner/blend) | 71 / 112 | 124 / 128 | 0 / 39 | 0 / 0 | 195 / 201 | 0 / 0 |

Full 8-view table for both modes: `diag\cross_tab_e51.json`. `figure_px` here is the
geometric figure silhouette (wherever `surfid>=0` — a UV-correspondence fact,
unaffected by which sampling-trust erosion is in force), not the eroded-sil count; the
two answer different questions and are not interchangeable, consistent with the same
law.

**E50's own finding restated plainly (Section 0's front matter carries the full
correction; this is the summary this section builds on).** Measured directly by that
seat's own instrument: `orphan_fill`'s population is depleted at the patches (~0.27x
base rate), the within-island fill population sits near base rate (~1.18x), the patches
themselves read 90-99% on texels the main paint pass wrote, and the same defect is
already present in a pre-`orphan_fill.py` baseline render. This seat has no access to
that instrument (E50's own work tree, out of scope) and does not reproduce, check, or
second-guess it here.

**A separate, narrower measurement this seat did make, using a different instrument,
consistent in direction with E50's own finding but not the same finding and not
offered as confirmation of it.** This arc's own dispatch inherited a hypothesis — from
the E49 kickoff, predating E50's own result — that E49's orphan-fill population is
where a wrong-material colour lives. Measured directly, with the real
`tools/palette_gate.py`, against E49's own `atlas_complete.png`, restricted to exactly
E49's own `orphan_fill_mask`:

| | owner (n=5,199) | blend (n=132,152) |
|---|---|---|
| off-palette (real tool) | 6px (0.12%) | 483px (0.37%) |
| largest blob | 2px | 66px |
| dominant off-palette hue | 110-120deg (100% of the 6px) | 110-120deg (44% of the 483px) |

Both populations sit almost entirely inside the two declared bands already, by this
gate's own two-band test — the gate's `max_offpalette_blob_px=800` bound is not
approached (2px, 66px). This is a different question from E50's own (a global hue-band
test against a declared palette, not a spatial base-rate test against a located defect
class), reaching a similarly unimplicating result by a different route — worth stating
plainly as a second data point, not as proof, and not as this seat's to reconcile
against E50's own numbers. `tools/palette_gate.py`'s own documented limitation is
relevant to why a clean reading here would not settle the question even if this were
the same instrument: it tests colour, not placement, and W3's "warm" band by its own
declaration already covers gold armour pieces (pauldrons, medallion, knees, crossguard,
pommel) alongside skin and leather — a gold-hued sample landing on a boot instead of a
pauldron would pass this specific test while still being the wrong material for that
location. Where genuine off-palette colour does appear in E49's own orphan-fill
population, it clusters at hue 110-120deg — inside the declared gap between the warm
and green bands (105-125deg), the same gap this repo's own palette documentation names
as forbidden by construction.

**Why arm A and arm B are reported regardless of this causation question.** Per the
front matter above, this dispatch's own arms are justified on construction grounds —
each removes a specific way to paint a texel a colour no view supports — independent of
whatever population turns out to carry the visually-named patches. Section 4's counts
and Section 8's gates hold on that basis alone. Locating the visually-named defect
against a placement-sensitive detector was never in this seat's scope
(E51-fill-repair-kickoff.md, "Out of scope") and is not attempted here.

## 7. Final sentinel count

**2,111 owner (0.0879% of all valid texels) + 2,904 blend (0.1209% of all valid
texels), both loudly printed and manifest-recorded, not buried in an aggregate.** Every
one of these is a palette-gate refusal — 0 owner and 402 blend are arm A refusals; 2,111
owner and 2,502 blend are arm B refusals. There is no other source of sentinel in this
arc's own accounting (Gate A/B/accounting `Andon`s all held; the four outcome classes
partition the orphan set exactly, checked in code, both modes).

## 8. Gates

- **Gate A** (arm A must never paint a texel the eroded sil calls invalid) — held, both
  modes. Checked by an independent re-derivation: accepted texels were grouped by their
  own chosen view and `sample_view` was called again, fresh, against that group; `valid`
  was required `True` and the re-sampled colour was required to match the scoring loop's
  own recorded colour to within 1e-6. Zero violations (owner: vacuous, 0 accepted
  texels; blend: 124,361 texels checked).
- **Gate B** (arm B must never run on a texel any view can see) — held, both modes.
  Checked by an independent full re-sample of all 8 views against the arm-B population;
  zero texels came back valid on any view (owner: 117,024 checked; blend: 141,186
  checked).
- **Gate C** (every gate is a `raise`, never a bare `assert`) — held by construction.
  Every check in `fill_repair_e51.py` and `cross_tab_e51.py` that could halt the run
  raises `Andon(ValueError)`; no `assert` appears anywhere in either file.
- **Gate D** (watch the direction the invariant does not bound — texels left unpainted
  or flat-grey) — this is a reporting discipline, not a runtime halt (no calibrated
  threshold for "how much sentinel growth is acceptable" was available to pre-register,
  and inventing one after seeing the result is the one move this repo's own law forbids).
  Satisfied by Sections 4 and 7 above: the final sentinel count is stated per-mode,
  per-arm, and per-cause, not folded into a single aggregate, and Section 5's cross-tab
  specifically surfaces the 48 (owner) + 493 (blend, 401+92) texels where E49 had
  painted something and this arc now paints nothing.

No gate fired anywhere in this arc's own chain.

## 9. Design choices made before writing code (recap; full text in `handoff.md`)

1. **This pipeline has no per-texel material ground truth.** Confirmed by a manual GLB
   JSON-chunk parse of `facet_E08\ARMB\out\W3_final.glb` (no `pygltflib` in this
   environment): exactly 1 mesh primitive, 1 material, 1 image. The only "material"
   concept this codebase has actually built for W3 is the two declared hue bands in
   `docs/experiments/E08-W3-palette.json`.
2. **Arm B's neutral fill**: a KD-tree (3D world position) over all texels painted at
   the moment arm B runs (pre-existing plus this run's own accepted arm-A fills),
   K=25 nearest neighbours, L*/C* as the plain mean over all K (well-defined regardless
   of chroma), hue as the circular mean of unit chromatic vectors over only the
   chroma-qualified voters (C* > 12.0, the palette's own declared floor), reconstructed
   through a newly-written Lab-to-sRGB inverse (round-trip self-tested, max abs error
   1.035e-14) since every other tool in this codebase only ever goes the other
   direction. K=25 is a disclosed, reasoned-not-derived choice; a K-sensitivity
   diagnostic (K=9, K=75 against a 3,000-texel sample, both modes) found gate-verdict
   agreement of 98.0%-98.8% and median Lab deltaE of 0.77-1.70 against the shipped K=25
   result (p90 7.7-10.7 — a smaller tail is more sensitive, expected nearest a material
   seam). This diagnostic did not retune the shipped run.
3. **Known limitation, disclosed not hidden**: Euclidean 3D nearest-neighbour has no
   notion of surface geodesics and can, in principle, reach across a thin gap (opposing
   sides of a closed fist, a tight cloth fold). The palette gate is the backstop for
   this — a neighbourhood straddling the warm/green seam averages toward the declared
   105-125deg gap and should self-flag as refused. Section 6's finding that E49's own
   off-palette contamination clusters at exactly that hue range is consistent with this
   backstop being the relevant one, though this report does not claim it is exercised
   only by seam-straddling cases.
4. **`palette_gate.py`'s `to_lab` is a cited, verbatim copy** (sha256
   `6ecdb307ed23c47afa6f66533ef0cdb36e698d58cb518d8c052e43af7342c544`), not a live
   import — the source module runs `argparse.parse_args()` at module scope, confirmed
   by reading it whole, which makes import unsafe. The palette JSON itself (bands,
   chroma floor) is read live at runtime from `docs/experiments/E08-W3-palette.json`,
   not hand-copied as constants. The real, unmodified CLI is genuinely invoked as a
   subprocess against real PNGs (Section 4) as an external check on the cited-copy
   replica, not a substitute for it.
5. **Crop regions reused, not re-derived** — found already declared in
   `tools/s3_sheet_regions.json` (view 0 tunic + skirt, view 1 tunic, view 7
   boot_tops), the same resource `build_sheets_e49.py` already drew from for its own
   blade/grip rows.

## 10. Out of scope, respected

Twin regeneration: not touched. Generation spend: none (no GPU, no cloud credits used).
The never-seen-surface policy question: not decided here — this report measures, the
Director decides. Canon build-out: not touched. Repo tools: none edited —
`tools/palette_gate.py`, `tools/atlas_from_aovs.py`, `tools/s3_composite.py`,
`tools/s3_run.py`, `tools/s3_sheet.py` were all imported/cited/invoked, never modified.
`E:\AI\training\facet_E4*\`: read only (hash/byte comparisons throughout this report
confirm nothing there was altered by this arc). `E:\AI\training\facet_E50\`: not read,
not touched — a separate seat's own live work tree.

## 11. Standards compliance (scored against what this arc actually did, not the plan)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Every input path is absolute and named; `fill_repair_e51.py` echoes `palette_gate.py`'s sha256, the palette JSON path, K, alpha and relative_jump into its own manifest per mode; the eroded bundle and E49's own atlas dirs are cited by path, read-only. |
| ANDON_AUTHORITY | 3 | Gates A/B/C/D per Section 8; every check is a `raise Andon(ValueError)`, none a bare `assert`; the population-equality check in `cross_tab_e51.py` is the same discipline applied to a diagnostic, not just the main tool. |
| NAMED_COMPENSATORS | 3 | All writes are under `facet_E51\` plus one repo file (this report); compensator is delete-the-tree; owner is the advisor. No irreversible call occurred (no publish, no push, no generation, no edit to a shipped tool). |
| DECOMPOSE_BY_SECRETS | 3 | Run-only seat; arm A, arm B, the gate replica, the real-tool verification, the renderer and the sheet builder are five separate functions/files, each changed independently of the others during development. |
| UNCERTAINTY_GATED_HUMANS | 3 | Terminus is the sheet, for the Director's own eye; the causation question in Section 6 (E50's own finding, and this seat's narrower, consistent-but-separate measurement) is surfaced rather than resolved by this seat, precisely because it bears on a judgment call only he and the advisor make. |
| EXTERNAL_VERIFIER | 3 | The real, unmodified `tools/palette_gate.py` independently re-checked every accepted and refused population this arc produced (Section 4) — not merely a manifest replay, a second, differently-sourced computation over the same pixels, and it was run specifically because this arc's own in-memory replica could not be trusted to grade itself. |

## 12. Artifacts

All under `E:\AI\training\facet_E51\` unless noted:

```
handoff.md                              live working record, written first
predictions.md                          written before fill_repair_e51.py ran
fill_repair_e51.py                      arm A + arm B + gate, both modes
run_fill_repair_e51.log                 full stdout of the main tool
fill_repair_summary.json                combined per-mode manifest
atlas_owner_e51/, atlas_blend_e51/      atlas_complete_e51.png, per-arm masks,
                                          fill_repair_manifest.json,
                                          verify_*.json/.png (real palette_gate.py runs)
renders_owner_e51/, renders_blend_e51/  8 views each, flat, from atlas_complete_e51.png
build_sheets_e51.py                     sheet builder (4 columns, both modes)
sheets/owner/, sheets/blend/            16 sheets + manifest.json
cross_tab_e51.py                        E49-old-class x E51-new-class accounting
diag/                                   E49's own orphan-fill population measured
                                          directly by the real palette_gate.py
                                          (Section 6), cross_tab_e51.json
step_render_owner.log, step_render_blend.log, step_sheets.log, step_cross_tab.log
```

Repo file: `docs/experiments/E51-fill-repair-report.md` (this report) — the only file
this seat wrote inside `E:\AI\facet\`. `git status --short` at report time shows this
as the only tracked change from this seat.
