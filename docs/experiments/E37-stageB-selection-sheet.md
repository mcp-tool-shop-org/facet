# E37 Stage B — the selection sheet for the ruled set (seed 770700)

**Seat:** executor — a NEW seat, taken mid-arc at `5b8e9ce`; the prior seat retired on
context, not on a defect · **Date:** 2026-08-15 · **Spend: 27 of 40 cloud jobs —
UNCHANGED. This stage submitted nothing and costs nothing.**

[Ruling 6](E37-ruling.md) selected seed 770700 and named what comes next: *"the selected
set's sheet — all eight views at full size beside the source plate, head band at 3×, the
per-view reg-IoU and census table riding — then his word gates Stage C."* This is that
sheet, with the ritual that preceded it and the observations that ride it.

**No number in this document was re-measured.** Every census, register and reg-IoU figure
is cited from `stageB/selection.json`, the artifact the prior seat wrote and Ruling 6 ruled
on. What this seat measured is listed separately in §1 and §5, and is measurement *about
the record*, not a re-run of it.

---

## 0. The handoff ritual — all gates HELD

| gate | result |
|---|---|
| working tree at open | **clean** — the prior seat left nothing uncommitted; 25 commits ahead of `origin/main` |
| E15 ritual, scratch `--db` | **PASS** — all four legs, exit **0**; seeded set **19 / 19**; determinism leg **BYTE-IDENTICAL** (12,763,136 bytes, both builds); leg 3 **2,012 pointers / 0 dangling**; **37 experiments**, missing none |
| VRAM watchdog | **ADVANCING** on two reads — heartbeat `07:15:51.582` → `07:16:22.329`, CSV 1,501,637 → 1,501,919 bytes, last row's own timestamp moving with it. State `ok`, VRAM **6,424 of 32,607 MiB — 24,776 below the 31,200 ceiling** |
| manifest **A** `facet_E33` | **HELD** — 116 / 116, 0/0/0, 835,059,987 bytes; self-reference reported, not counted |
| manifest **B** `facet_E34` | **HELD** — 84 / 84, 0/0/0, 177,563,094 against declared |
| manifest **C** eight subtrees | **HELD** — 7,312 files / 17,072,807,610 bytes, delta **+0 / +0**, per-subtree table reproduced to the file |
| manifest **D** `facet_E35` | **HELD** — 335 / 335, 0/0/0, 284,096,148 against declared |
| premise 1, source plate re-hashed | **MATCH** — `753383255718db72…`, 1,216,363 bytes, 1328×1328 RGB |

**Every receipt landed outside every protected tree**, in `E:\AI\training\facet_E37\handoff\`
— the E36 open halt's rule, and the reason gates A/B/D were run with an explicit
`--out-json` rather than a default (task 0 §3b's still-live hazard: two E35 instruments
default their output *into* `facet_E35`).

The E15 figures differ from the prior seat's open run (12,562,432 bytes / 1,993 pointers)
by exactly the commits landed since — the Stage-B halt and Ruling 6. That is what a growing
record does.

⚠ **`E:\AI\training\_watchdog_TRIPPED` is present and dated `2026-08-15 05:18:32`.** It is
the *recorded* round-2 kill already documented in
[E37-round2-vram-halt.md](E37-round2-vram-halt.md) — a historical marker, not a live
firing. The heartbeat has advanced 1h58m past it and the state column reads `ok`.

## 1. What this seat verified rather than inherited

| claim inherited from the handoff | measured here |
|---|---|
| the selected set's eight twins are on disk | **8 / 8 present**, `sets/s770700/twin_v{0..7}.png` |
| frame is 368×1024 (Ruling 4) | **all eight are 368×1024 RGB** — checked as a hard `raise` inside the sheet builder, not a comment |
| the source plate is armature's, read-only, `75338325…` | **re-hashed to the full 64 hex digits**, matches |
| the round-2 approved plate is `a4bcf250…` (Ruling 3) | **re-hashed**, matches; 866,642 bytes, 1328×1328 RGB |
| the prompt is v-w1 via the register fixture, never typed | `facet_E37/registers/vw1.json` present; **no prompt text was typed at this seat** |

### 1a. The wrong-object family, checked before a number was read off the sheet

`selection.json`'s `figure_px` pairs up **exactly** across three of four view pairs —
v0 = v4 = 93,264 · v2 = v6 = 53,715 · v3 = v7 = 91,371 — while v1/v5 differ by 1
(92,134 / 92,135). Exact equality over ninety-three thousand pixels is not what
near-symmetry produces, and this arc has already had one firing of this family (Ruling 5:
view 4's reg-IoU first measured against view 0's silhouette). Two readings fit — a genuinely
mirror-symmetric silhouette, or a mask serving two views — so it was checked rather than
assumed.

**It clears.** Eight views, eight distinct mask files, eight distinct sha256s, and every
view's `figure_px` equals its own mask's pixel count to the pixel:

| | v0 | v1 | v2 | v3 | v4 | v5 | v6 | v7 |
|---|---|---|---|---|---|---|---|---|
| mask sha256[:8] | `482bbf51` | `9447960d` | `c7f610df` | `9e31ef50` | `5135cd8f` | `a454e46a` | `38470af2` | `3f92bf0a` |
| mask px | 93,264 | 92,134 | 53,715 | 91,371 | 93,264 | 92,135 | 53,715 | 91,371 |
| bbox cols | 37–330 | 78–312 | 119–248 | 75–309 | 37–330 | 55–289 | 119–248 | 58–292 |

The mechanism is visible in the bboxes: **v3 spans cols 75–309 and v7 spans 58–292 — the
same 234-px width, mirrored, not the same file.** Bilateral symmetry gives equal areas at
mirrored yaws; a reused operand would have given equal *hashes*. It gave neither.

Receipt: `handoff/e37_mask_pairing_check.txt`.

## 2. The sheet, and the three choices it makes

`handoff/E37_stageB_selection_s770700_fullsize.png` — **5600 × 1406**.

**1. Nothing is resampled.** The twins sit at native 368×1024 and the plates at native
1328×1328, vertically centred on one 1328-tall canvas. `montage.py` was *not* used here and
the reason is in its own code: it resizes every panel to the first image's dimensions
(`montage.py:63-68`), which on a 368×1024 twin beside a 1328-wide plate is a 3.6×
horizontal stretch — a distortion the eye reads as the twin's own proportions. The tool is
right for the same-shape case it was built for and wrong for this one. Layout is done in
`handoff/e37_selection_sheet.py`; `head_crop.py` is used unmodified for the head band,
because its head-band location is figure-relative and needs no such change.

**2. Both plates ride.** The kickoff's premise-1 plate (`75338325…`, armature's tree) is the
identity reference; the round-2 approved plate (`a4bcf250…`) is what the picked mesh was
actually reconstructed from. Showing one without the other hides half the provenance.

**3. The numbers are cited, never re-measured.** The builder reads `selection.json` and
computes no census and no IoU. It carries four `raise`-form ANDONs — receipt destination
inside any protected tree, either plate's hash off its recorded value, a missing view, a
frame that is not 368×1024 — none of them an `assert`, per E21 Ruling 2.

Companion sheets, same directory:

- `E37_stageB_selection_s770700_head3x.png` — **8304 × 806**, both plates + all eight views,
  head band at **3×**, band located by `head_crop.py --auto` from each figure's own mask.
- `E37_stageB_s770700_browzoom6x.png` — **3978 × 674**, views 0 / 1 / 7 at **6×** over the
  brow region, the locus §4 scores.

## 3. The per-view table — cited from `selection.json`

| view | dark count | dark area px² | largest | reg-IoU | C\* | keyed px | figure px |
|---|---|---|---|---|---|---|---|
| 0 | 16 | 157 | 34 | 0.9559 | 23.30 | 95,948 | 93,264 |
| 1 | 19 | 155 | 25 | 0.9523 | 30.26 | 95,141 | 92,134 |
| 2 | 10 | 50 | 19 | **0.9116** | 29.90 | 58,472 | 53,715 |
| 3 | 8 | 49 | 17 | 0.9350 | 29.98 | 96,148 | 91,371 |
| 4 | 12 | 54 | 15 | 0.9463 | 26.00 | 97,291 | 93,264 |
| 5 | 16 | 84 | 15 | 0.9354 | 24.41 | 96,782 | 92,135 |
| 6 | **55** | **252** | 29 | **0.9627** | 30.42 | 54,932 | 53,715 |
| 7 | 24 | 86 | 14 | 0.9145 | 24.39 | 98,443 | 91,371 |
| **total** | **160** | **887** | **34** | min **0.9116** | median **29.90** | — | — |

Counts and areas sum to the ruled totals exactly (160, 887). **reg-IoU floor 0.80: every
view clears it**, minimum 0.9116 at view 2. **C\* is SUSPENDED** (Amendment 2) — it rides
as a diagnostic and gates nothing, and Ruling 6 already folded the reason: wood runs
29.9–35.3 against terracotta's 23.77, so a ported terracotta floor would have been a
threshold about the wrong material.

**One row carries a third of the set.** View 6 holds **55 of the 160** dark marks and
**252 of the 887 px²**, on the smallest figure of the eight (53,715 px — a profile). The
other profile, view 2, is the *lowest* row at 10 / 50. Reported, not explained: this seat
ran no investigation, and none is dispatched.

## 4. Band H4 — its blocker cleared, scored from the record

The halt doc left H4 *"not scorable — no set is selected → pending the ruling."* Ruling 6
selected the set, so the blocker is gone. H4's text, sealed at `1494a0f` **before any
seed-set job fired**:

> **UP** zero detached facial marks on the face-bearing views (0, 1, 7) of the winning set,
> at the (123,167)-family coordinates · **FLAT** one such mark on one view · **DOWN** two or
> more, or any on view 0

**No detector was run and no region was invented.** The blobs are filtered out of
`sets/s770700/census.json`, which carries a `bbox` and `centroid` for every one; the brow
boxes are lifted verbatim from the prior seat's own `task0/e37_canny_sweep.py:36-37`
(BROW_L rows 112–142 / cols 138–182, BROW_R rows 112–142 / cols 186–216), authored to find
the defect before this band existed.

| view | blobs, whole view | in the BROW boxes | in the head band (rows 66–264) |
|---|---|---|---|
| 0 | 16 | **0** | 4 — largest 7 px² |
| 1 | 19 | **1** — 3 px² at (y 139.7, x 144.7) | 8 — largest **25 px²** at bbox [167,143,182,146] |
| 7 | 24 | **0** | 10 — largest 3 px² |
| | | **1 mark, on one view, none on view 0** | |

**As worded, that is the FLAT branch**: one such mark, on one view, and none on view 0. The
mark is inside BROW_L but sits ~17 rows below and ~22 cols left of the recorded
(123,167) mole, and at 3 px² against the probe's 29 px. Both facts ride; neither is
adjudicated here.

⚠ **A declared limit, because a check that cannot fail is not a check.** The census caps a
blob at `blob_max_px2 = 36`. **A mark larger than that is absent from this list by
construction** — and E34's forehead artifact, the one Ruling 5 traced to the control, is
**81 px**. So this scoring can see a probe-sized mark and *cannot* see an E34-sized one.
That is precisely why the 6× brow zoom rides beside it: the band's numbers bound the small
class, and the Director's eye is the instrument for the large one.

Receipts: `handoff/e37_h4_scoring.txt`, `handoff/e37_h4_from_record.py`.

## 5. What the sheet shows at full size — observations, not judgements

Recorded because the sheet exists to be read, and because a defect that decides acceptance
is invisible at contact-sheet scale. **None of this is a verdict; all of it is the
Director's.**

1. **The face is painted on views 0, 1, 2, 6 and 7; views 3, 4 and 5 carry a bare head**
   with ears. The two profiles disagree in kind: view 2's face reads as a drawn profile,
   view 6's carries a heavy dark brow and a dark curved stroke.
2. **Brow stroke weight varies across the set.** View 0's brows are fine and light; views 6
   and 7 carry markedly thicker, darker brows. View 6 is also the 55 / 252 census row in §3
   — the heaviest strokes and the highest dark census are the same view.
3. **View 1's face is asymmetric and partial** against view 0's: one brow (rendered as a
   hatched patch rather than a drawn line), one eye, and a vertical double-line down the
   nose region — the 25 px² blob at rows 167–182, cols 143–146 in §4's table. View 0 at the
   same zoom carries two brows, two lidded eyes, a nose and a closed smile.
4. **View 2 reads warmer and more saturated** than the other seven at full size. Its
   C\* is 29.90 — mid-range for the set — so the register diagnostic already on the sheet
   does not single it out. **No new metric was commissioned for this**; it is an eye
   observation and the eye that rules on it is his.

## 6. HALT — the Director's word gates Stage C

> ⚠ **ANSWERED, same day — this section's forecast of what came next is superseded and is
> left standing rather than rewritten.** His word at this sheet was **"v1 is missing a nose ·
> v6 has a line across the face · v3 has a dent in the lower back"** — the set does NOT
> proceed unamended ([E37-ruling.md](E37-ruling.md) Ruling 8; Ruling 7 folded a partial
> word as an acceptance and is corrected in place there). Stage C did not fire. What fired
> instead is a per-view re-roll of exactly those three views, reported in
> [E37-stageB-reroll-report.md](E37-stageB-reroll-report.md).
>
> **Two of his three defects are in §5 below and one is not.** §5 flagged v1's partial face
> and v6's mark concentration — the same two views he named. **It did not flag v3, because
> it never looked at the lower back**: §5's observations run over faces and head bands,
> which is where the sheet's 3× and 6× zooms pointed. The v2 warmth it did flag drew no
> ruling. Recorded because an executor's hit rate on his eye is worth knowing, and because
> the miss has a stateable cause — the zooms decided what got looked at.

Nothing beyond this sheet has run. No projection, no fill, no turnaround, no cloud job.
Spend stands at **27 of 40**.

**What his word gates:** Stage C as the kickoff dispatches it — E34's proven eight-view
projection on the selected set (local, zero cloud), surface-aware fill, RGBA-true
turnarounds (requirement 4 — real alpha from the raycast silhouette masks, named new work
because this route's turn renders measure flat-255), final census in both classes,
provenance mix, and the full-size sheets. Then Stage D: his acceptance at his zoom, the
`facet_E37` manifest self-excluded, the delivery GLB + sha256 + ruling + accepted-with
observations, and the relay to armature carrying path and hash.

## Artifact homes

All under `E:\AI\training\facet_E37\handoff\` — outside every protected tree:

`E37_stageB_selection_s770700_fullsize.png` · `E37_stageB_selection_s770700_head3x.png` ·
`E37_stageB_s770700_browzoom6x.png` · `_head3x_A.png` · `_head3x_B.png` ·
`e37_selection_sheet.py` · `e37_h4_from_record.py` · `e37_h4_scoring.txt` ·
`e37_mask_pairing_check.py` · `e37_mask_pairing_check.txt` · `e37_probe_sheets.py` ·
`e37_probe_census.py` · `e15_scratch.db` · `e15_verify.txt` ·
`e37_close_manifest_{E33,E34,E35}.json` · `e37_close_manifest_C.json` ·
`e37_close_suite.txt`.

No protected tree was written to. No cloud job fired. No sealed band was edited.
