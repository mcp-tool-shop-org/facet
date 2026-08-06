# E10 Ruling 4's queued dispatch — the correction-in-place ruling

**Advisor, 2026-08-05 evening.** Evidence:
[E10-offsurface-consumers-report.md](E10-offsurface-consumers-report.md) — all four
anchors exact to the digit, predictions hashed blind
(`cf16bb55…`, 20:19:51) before the first classification ran, halt observed verbatim.
[E10-ruling.md](E10-ruling.md) is closed and is cited, not edited; this file resolves
its Ruling 4's queued item.

## Ruling 1 — the recorded headlines STAND; the on-surface restatement enters the record beside them

The recorded numbers are not wrong. Each was measured on the population its record
names (uv-valid), the arithmetic reproduces exactly (anchors A–C2), and both Gate-1
acceptances stand on the Director's eye — nothing here re-opens either gate. What the
measurement establishes is that the declared population contains **77,693 texels
(2.4967%) whose positions are not on the geometry** (>1 px, frames named in the
report). The record therefore carries both readings from today, denominators named:

| quantity | as recorded (uv-valid) | on-surface | delta |
|---|---|---|---|
| stage-1 reach ceiling | 42.72 | **42.25** | −0.47 pts |
| styled / valid | 36.89 | **36.68** | −0.21 pts |
| styled / reachable | 86.4 | **86.8** | +0.4 pts |
| dilation / valid | 56.24 | **56.44** | +0.20 pts |
| brush / valid | 6.87 | **6.89** | +0.02 pts |

The README is annotated in place at the galleon's quoting site. The closed E04/E10
rulings are untouched: their numbers were true on their stated operands, and a
correction that rewrites a closed ruling would be revision, not correction.

## Ruling 2 — the as-recorded family remains the standing cross-asset headline

W3's 68.8 / 74.1 / 92.9 were measured on *its* uv-valid population with the
off-surface property unmeasured there. Quoting the galleon on-surface beside W3
as-recorded would compare different denominators — the moving-denominator lesson
applied in advance rather than paid for again. The on-surface family becomes the
standing one **only when both assets carry it** (see Ruling 4a).

## Ruling 3 — the finding is banked; the mechanism stays open and is NOT asserted

Banked as measured: **the off-surface population is painted, not padding.** Stage-1
styled texels carry it at 3.06% and the reachable set at 3.56%, against the
never-painted dilation class at 2.15% (population 2.4967%); 45.27% of the population
is stage-1 styled; **35,170 texels in the accepted atlas's stage-1 set sit on
positions that are not on the geometry**; stroke 1 loses 8.15% of its commits against
0.41–2.45% for the other five. Four of six blind predictions falsified in direction —
the "unreachable gutter" mechanism is dead, and the falsifications are the content.

NOT ruled: any mechanism. `bake_hero_prep.py:458` remains the report's named unread
suspect and remains unread. No route tool changes, no gate arms on these numbers,
nothing is corrected anywhere the measurement did not reach.

## Ruling 4 — the follow-on queue (Director-gated; neither opens unbidden)

- **(a) W3's own off-surface measurement** — the same instrument pointed at ARMB's
  bake: the rate, the exclusion sweep over the same consumers, the class composition.
  CPU-only, cheap, and it completes the pair so Ruling 2's condition can ever be met.
  Queued first.
- **(b) the mechanism measurement** — where the painted off-surface texels live
  (island-rim distance, seam adjacency, per-view structure, and why stroke 1 is the
  outlier), measured before any fix is contemplated. Its spec must state what each
  number returns when nothing is wrong — the works-perfectly test — before any
  threshold rides on it. Queued second.

## Ruling 5 — the diagnostic fidelity note is a correction-in-place

`texel_provenance.py`'s replay predates E08 Amendment 32 and over-claims **+358**
commits on this asset (+6/+118/+148/+25/+5/+56 — the exact signature of the missing
`fm_e & hit` intersect). The README row that said "reproduces live commit counts to
the texel" is corrected in place with this measurement; the A32-faithful replay is
[`tools/diagnostics/e10_claim_replay.py`](../../tools/diagnostics/e10_claim_replay.py).
The fix to `texel_provenance.py` itself is queued for the next session that needs the
tool, with this ruling as its targeting data. The shipped route is untouched — the
tool is an offline diagnostic and nothing on the route consumes its replay.

## Ruling 6 — small discrepancies, disposed

- **E04-h4-ceiling.md quotes valid = 3,111,832; the mask on disk measures 3,111,817**
  (as `provenance.json` and `offsurface.json` record). Annotated in place; both yield
  42.72% at 2 dp, so no quoted figure turns on it. The 15-texel cause is undiagnosed
  and stays that way unless a consumer ever depends on the exact count.
- **The E11 report's environment line** ("watchdog dead, heartbeat 13.6h stale …
  not restarted by this session") is corrected in place with attribution: the advisor
  restarted the watchdog at 20:26 and measured it alive at 20:51 (heartbeat age
  0.0 min). What stays true in the line: that session restarted nothing and ran no
  GPU leg, so nothing was exposed. The "13.6h" matches no on-disk timestamp and is
  recorded as the session-start hook's arithmetic, not a measurement.

## Standards compliance (this ruling)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | every ruled number cites the anchored report; the restatement table names both denominators |
| ANDON_AUTHORITY | 2 | the pre-registered halt was observed by the executor and resolved here rather than tuned past; the follow-on queue is Director-gated |
| NAMED_COMPENSATORS | 2 | corrections are additive annotations with dates; closed rulings untouched; undo is reverting this commit |
| DECOMPOSE_BY_SECRETS | 2 | corrections land at quoting sites; the mechanism question is separated from the correction and queued, not smuggled in |
| UNCERTAINTY_GATED_HUMANS | 3 | both acceptances stand on the Director's eye; the standing-family rule (Ruling 2) waits on a measurement, not an opinion; the queue opens only on his word |
| EXTERNAL_VERIFIER | 2 | the ruling rests on a report whose every recompute was checked against artifacts the measuring session did not produce |
