# E28 task-2c predictions — committed before `anchor_compare.py` exists

**Executor, 2026-08-09, the same seat that ran 2-pre/2a/2b.** Required by
[Amendment 2](E28-instrument-census-kickoff.md): task 2c's instrument is commissioned at
[Ruling 10](E28-ruling.md) and the frozen task-2 file
([E28-task2-predictions.md](E28-task2-predictions.md)) does not cover it. Committed before
one line of `tools/verify/anchor_compare.py` is written.

## The blindness boundary — and three rows are DEAD AS FORECASTS, disclosed

- **Read:** Amendment 2 in full (the instrument's specification), Ruling 10's commit
  message, CLAUDE.md's PNG-hash law (*file bytes are not pixel values* — the false-halt
  class this tool's fixture pins), the 2a byte-proof harness's own stdout defect from this
  session (the same class, met live).
- ⚠ **P12, P13 and P14 were VALIDATED IN SCRATCH BEFORE THIS FILE WAS COMMITTED.** While
  the 2a+2b suite ran, this seat drafted the instrument in the scratchpad and ran it: the
  compress-level pair built on the first attempt (13,097 vs 12,420 bytes, pixels equal),
  the two tiers separated on it, and blob-vs-scatter at equal 400-px totals returned LCC
  400 vs 4. **Those three rows are therefore design checks recorded in prediction form and
  are worth nothing as forecasts** — they are kept because their falsifiers and bands were
  written before the runs and the report will score them SEEN, not HIT. Pretending
  otherwise would be the calibration theater the record forbids.
- **Still blind:** P15 (the collector count — the test file does not exist) and P16 (the
  anchor question — the corpus was not grepped for a recorded byte-hash pair before this
  commit).

## P12 — the owed fixture: a pixel-identical, byte-different PNG pair

**Unit:** one *fixture pair* = two PNG files in `tests/fixtures/` whose decoded RGBA arrays
are equal and whose file bytes differ. **Prediction: constructible on the first attempt
(band: 1–2 attempts), via re-encode at a different compression level or an added text
chunk.** Falsifier: PIL normalising the difference away — if `optimize`/`compress_level`
round-trips to identical bytes, the text-chunk route is the fallback and the report says
which built it.

## P13 — the byte tier on the recorded anchors' own class

**Behavioural.** The tool's `byte_identical` is labelled gate-eligible **only** for
artifacts whose bytes are the contract, with the caveat in the payload. **Prediction: the
pixel-identical byte-different fixture reads `byte_identical: false, pixel_identical:
true`** — the false-halt class separated by construction, which two live halts in this
repo's history could not do. Falsifier: any payload where the two tiers cannot disagree.

## P14 — the shape grid separates concentrated from spread

**Unit:** one *separation* = the concentrated synthetic residual (one blob) and the spread
one (scattered noise, same differing-pixel count) producing **different largest-connected-
component values** and **different grid maxima**, with totals equal. **Prediction: HOLDS,
with LCC(blob) ≥ 10× LCC(scatter)** (band ≥ 3×) at equal totals. This is the two-thresholds
law made testable: total alone cannot tell one wrong garment from speckle; the grid and the
component can. Falsifier: a connected-components implementation whose 8- vs 4-connectivity
choice collapses the scatter into one component — the report states which connectivity
shipped and why.

## P15 — how many tests T46 lands with

**Unit:** one collected pytest case in the 2c commit's new test file(s), counted by the
collector (E26 P8's lesson: the instrument counts parametrized cases, not written
functions). **Prediction: 12, band 8–18.** Amendment 2 names six behaviours; parametrization
and refusal legs roughly double it. No calibration haircut.

## P16 — the wrap's anchor question

**Prediction: `anchor_check` CANNOT carry a recorded-number anchor at birth, and the reason
is structural, not a gap:** the instrument is new, so no recorded number was produced by it
— the anchors it *serves* (E08-armB state, E04 step 0) are byte-hashes recorded by other
procedures, and reproducing those is the CALLER's replay act, which Amendment 2 explicitly
keeps out of the tool. The honest test set is fixture-complete and anchor-free, and says so
rather than padding. Falsifier: a recorded byte-hash pair in the corpus that the tool can
re-verify read-only at the served surface — if one exists, that leg gets built and this row
scores MISS.
