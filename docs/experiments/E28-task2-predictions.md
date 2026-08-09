# E28 task-2 predictions — committed before the extended census runs once

**Executor, 2026-08-09, second seat of the arc.** The task-1 file
([E28-predictions.md](E28-predictions.md)) carries P1–P7; this file covers the work
[Amendment 1](E28-instrument-census-kickoff.md) green-lit — the `tools/verify/` extension
(2-pre), the tie repair's sweep (2a), and the anchor question (2b). Committed before
`instrument_census.py` runs against `tools/verify/`, and before any `tools/verify/` or
`e12_*`/`e14_*` source is opened at this seat.

## The blindness boundary — exactly what this seat has seen

- **Read in full:** [E28-ruling.md](E28-ruling.md),
  [Amendment 1](E28-instrument-census-kickoff.md), the task-1 report, CLAUDE.md's two new
  laws, the E15 ritual output.
- **Seen of `tools/verify/` — filenames only, plus fragments of OTHER files that name
  them:** the 8-file directory listing (`gate0_sheet.py`, `gate1_sheet.py`, `gate_mesh.py`,
  `head_crop.py`, `head_render.py`, `mesh_stats.py`, `montage.py`, `turn_render.py`);
  `measure_mcp.py`'s registry lines naming `verify/mesh_stats.py` and
  `verify/gate1_sheet.py` as serving instruments invoked **as subprocesses with flags**;
  the spec's `mesh_stats` row; corpus mentions read in passing across the arc
  (E08: *"`turn_render` gained `--bg`"*; CLAUDE.md: `--views=-30,0,30`; the environment
  note that every Blender call here is `blender -b -P <script>.py -- <args>`, 12 of them).
- **NOT read:** the source of any file under `tools/verify/`; the source of
  `e14_topology.py`, `e12_thin_curve.py`, `e12_offsurface.py`, `e12_nonmanifold.py`,
  `texel_provenance.py` (beyond the dispatch's quoted crash lines); any grep of the record
  for whether the three 2b instruments have recorded outputs — **that check is deliberately
  deferred until after this commit**, because it is precisely what P10 predicts.

## The rituals applied

Per the **conjunction law** (new, folded from this arc's own P1): every composite below is
predicted **clause by clause first, then the join, with the join tracking the rarest
clause**. Per the **self-population law**: this file and the coming report are corpus files
inside `SELF_DOC_PREFIXES` (`docs/experiments/E28-`), so axis D cannot see them —
idempotency is re-verified anyway. **No calibration haircut anywhere.**

---

## P8 — the verify/ census, clause by clause

**Unit:** one `.py` file directly in `tools/verify/`. **Denominator: 8**, to be verified as
the first act of 2-pre, not inherited. **Property defined for every member:** yes for
A/B/C/D/E; axis F carries the same three `n/a` classes as task 1.

| row | clause | prediction | band | reasoning in one line |
|---|---|---:|---|---|
| P8a | imports `argparse` | 7 | 5–8 | `montage`/`head_crop` are the doubt; the rest are flagged tools by record evidence |
| P8b | ≥1 `add_argument` | 7 | 5–8 | rides with P8a |
| P8c | `__main__` guard | 3 | 1–6 | **the rarest clause and the honest uncertainty** — diagnostics measured 6/99, but verify/ is a different, older home whose style I have not seen |
| **P8d** | **invocable (join)** | **3** | **1–6** | governed by P8c, stated as such |
| P8e | module-level `parse_args()` | 4 | 2–7 | the house style seen in diagnostics, hedged for a different home |
| P8f | B1 subject-bound | 0 | 0–2 | two of these serve already; Ruling 3's entry checks name "axis B1 empty" as the serving hygiene |
| P8g | D cited (≥1 corpus file) | 7 | 5–8 | these names saturate the record; `montage` is the doubt |
| P8h | E anchored (either form) | 4 | 2–6 | `mesh_stats` (T12/T36) and `gate1_sheet` (T39) near-certain; the render pair uncertain |
| P8i | F `n/a` (import blocked, `bpy`) | 2 | 1–3 | `turn_render` + `head_render` — the Blender `-b -P` pattern implies module-level `bpy` |
| P8j | F true | 2 | 0–4 | bounded above by P8d minus the bpy pair's overlap with it |
| P8k | G mapped to one of the eight | 2 | 2–3 | `mesh_stats` → `mesh_stats`, `gate1_sheet` → `measure_report`; `gate0_sheet` is the possible third but I expect to judge it `ambiguous` |

*Blindness: source-blind on all 8; informed by the fragments disclosed above, so NOT blind
on `mesh_stats`/`gate1_sheet` having flag surfaces (the server passes them args today).*

## P9 — the tie repair's sweep (2a)

**P7 stands as written in the task-1 file and its discharge is the deliverable.** The
sweep-shaped restatement, so the discharge has its own pre-registered numbers:

- **P9a — zero index-triple mismatches** between the current expression and the repaired
  one over the randomized distinct-extent sweep (N ≥ 10,000 triples). Falsifier: one triple
  where the selected `(thin, tall, wide)` differ.
- **P9b — every recorded subject has three pairwise-distinct extents**, so the crash never
  fires on a recorded subject and byte-identity is checkable on all of them. Falsifier: a
  recorded mesh with a tie — in which case the current tool cannot produce bytes there, the
  claim narrows to "byte-identical wherever the current code produces bytes at all", and
  the narrowing is reported, not smoothed.
- **P9c — the unit cube raises today** (the can-fail leg's precondition; already reproduced
  at two seats, so this is not blind and is worth nothing except as the leg's precondition).

*Blindness: P9a/P9b blind in the only sense left available — the conclusion is inherited
from E27 Ruling 3 and the dispatch quotes the crash mechanism, so what remains mine is the
sweep size, the falsifiers, and P9b, which nobody has measured.*

## P10 — which of the three wraps can carry an anchor (2b)

**Unit:** one *anchor-carrying wrap* = a served tool whose test reproduces, digit for
digit, a number **recorded in the corpus and produced by the same instrument** the wrap
invokes (E27's `reach_ceiling`/50.46% is the model). A number produced by a *sibling*
instrument (`e10_offsurface`'s ship numbers) does not count for `e12_offsurface`'s wrap.
**Denominator: 3.**

**Prediction: 2 of 3, band 1–3.** Named: `mesh_topology` CAN (E14's Gate 0 ran
`e14_topology` on the sword and its numbers sit in E14 documents); `thin_extent_curve` CAN
(the seeded question set itself carries *"thin_extent on the beast"* → E12 Ruling 25c, so a
recorded number exists). `offsurface_rate` CANNOT — predicted reason: the recorded
off-surface headlines are the ship's, produced by `e10_offsurface`, a different instrument;
whether `e12_offsurface` ever produced a recorded number on a recorded subject is exactly
what I have not looked up, and if it did, this row is wrong and the anchor gets built.

*Blindness: NOT blind on the two CANs (both facts were read in passing this arc — the
seeded set and the dispatch). Blind on the CANNOT, which is the only row with information
in it.*

## P11 — the self-population re-check

**Prediction: the extended census is idempotent across a second run at this seat** — zero
row drift with this file and the coming report in the corpus, because `SELF_DOC_PREFIXES`
already covers `docs/experiments/E28-`. Falsifier: any drifted row on the second run.
Stated because the law says one clean check is not clearance — the check runs again, after
the report exists.
