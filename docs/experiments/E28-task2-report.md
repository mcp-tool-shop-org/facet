# E28 — task 2 (2-pre · 2a · 2b · 2c). Report at the close.

**Executor, 2026-08-09, the second seat of the arc.** Dispatch:
[E28-instrument-census-kickoff.md](E28-instrument-census-kickoff.md), Amendments 1 and 2.
Ruling to date: [E28-ruling.md](E28-ruling.md) (Rulings 1–10). Predictions:
[E28-task2-predictions.md](E28-task2-predictions.md) (`d4aa87f`, before the extended
census ran) and [E28-task2c-predictions.md](E28-task2c-predictions.md) (`c976c4f`, before
`anchor_compare.py` entered the tree — with three rows declared dead as forecasts in the
file itself).

**Tasks 2-pre, 2a, 2b and 2c are done. Task 3 is the named carry** — not run, per
Amendment 2's own sentence that a clean halt beats a rushed instrument, at the end of a
session that had already run task 0, task 1, and the four task-2 stages.

---

## Gates

| gate | state | evidence |
|---|---|---|
| 4 — allowed diff under `tools/` | **HELD, with 2c's ruled addition** | across this seat's commits: `M tools/instrument_census.py` (2-pre + 2c census re-run), `M tools/diagnostics/e14_topology.py` (2a), `M tools/measure_mcp.py` (2b + 2c), `A tools/verify/anchor_compare.py` (2c, entered by Ruling 10 + Ruling 3's entry rule). `texel_provenance.py` untouched — task 3 did not run |
| 5 — CI | **NOT YET RUN** at this writing; no identifier is written here (E23's law) |
| 6 — no recorded tree modified | **HELD** | 7,312 files / 17,072,807,610 bytes; manifested at the 2a baseline, after the byte-proof, and at the close: **0 added / 0 removed / 0 changed** every time |
| the census halt (gate 3) | **HELD** | task 2 started only after [E28-ruling.md](E28-ruling.md) landed |

**Suites at this seat:** 782 passed / 457.03 s / exit 0 at the 2a+2b state; **790 passed /
437.62 s / exit 0** at the close, after 2c. Both scanners ride CI, not this table.

---

## 2-pre — the census reaches `tools/verify/`

Population verified first: **8 `.py`, 0 other, 0 subdirs, 8 git-tracked** (now 9 — see 2c).
The directory is parameterized (`--dir`, repeatable; diagnostics stays the default) and the
committed outputs are emitted with `--committed`, pinned by T41 so a partial re-emit cannot
land silently. A filename shared across homes is an ANDON (axes D/E/G key on the filename).

**The measurement: the two instruments serving at E27 —`mesh_stats.py` and
`gate1_sheet.py` — are themselves unguarded module-level scripts.** Task 1's house-style
finding extends to the serving surface, and the server's subprocess invocation is why it
works. Only `gate_mesh.py` carries a `__main__` guard in the whole home (1 of 8; the only
axis-F `true`). B1 = 0 across all 8: the verify home is subject-clean, exactly the property
Ruling 3's entry checks name.

### P8 scored, clause by clause (the conjunction law's first outing)

| row | predicted | band | measured | |
|---|---:|---|---:|---|
| P8a argparse | 7 | 5–8 | **8** | band HIT, point −1 |
| P8b add_argument | 7 | 5–8 | **8** | band HIT |
| P8c `__main__` guard (the named rarest clause) | 3 | 1–6 | **1** | band HIT |
| **P8d invocable (join)** | 3 | 1–6 | **1** | **band HIT — the join tracked the rarest clause, as the law says** |
| P8e module-level `parse_args` | 4 | 2–7 | **7** | band HIT, top edge |
| P8f B1 subject-bound | 0 | 0–2 | **0** | HIT exact |
| P8g cited | 7 | 5–8 | **7** | HIT exact (`montage.py` is the uncited one) |
| P8h anchored | 4 | 2–6 | **4** | HIT exact |
| P8i bpy-blocked | 2 | 1–3 | **NOT MEASURED** | see below |
| P8j F true | 2 | 0–4 | **1** | band HIT |
| P8k G mapped | 2 | 2–3 | **4** | **MISS above band** |

**P8i is the E27 shape, caught by the instrument's own discipline instead of scored:** the
two predicted `bpy` importers (`turn_render`, `head_render`) are unguarded, so axis F never
probes them and the import-blocked path is unreachable for them. A prediction about a
property the instrument does not evaluate for those members — `n/a`, not a hit or a miss.

**P8k's miss is the forgetting of my own precedent's breadth:** task 1 mapped nine
diagnostics sheet-builders to `measure_report`; judged under the same rule, three verify
sheet tools joined them (`gate0_sheet`, `gate1_sheet`, `head_crop`) plus `mesh_stats` = 4.
The prediction reasoned about two and the rule I had already applied produced four.

**P11 held:** second `--committed` run at this seat, totals equal, **0 of 107 rows
drifted**, with this arc's papers in the corpus.

---

## 2a — the tie repair, and the proof discharged rather than cited

The crash reproduced at this seat before anything was touched (third seat to reproduce it).
**The derivation sharpened the obligation:** `argmin == argmax` exactly when
`min(ext) == max(ext)` — first-of-min and first-of-max can only coincide if the values do —
so the crash class is **all-equal extents only, and two-way ties never crashed.** A repair
that changed two-way-tie selection would be a behaviour change wearing a crash fix's
clothes, which rules out the argsort form. The repair is a guard:
`if thin == tall: thin, tall = 0, 2`, dead on every input the old code returned on.

**The proof (T42, 27 tests + the byte run):**

| leg | result |
|---|---|
| randomized sweep, 10,000 distinct-extent triples + all 6 permutations of (1,2,3) | old == new selection, **0 mismatches** |
| 6,000 two-way-tie triples | old does not crash; old == new, **0 mismatches** |
| all-equal class | old raises IndexError; new returns a permutation |
| tool conformance, 5 synthetic GLBs through the SHIPPED file | tool == swept expression on the extents the tool measures |
| **byte level, 17 recorded subjects** (3 gate-0 raws × 3 arcs, 4 preps, the 4 accepted finals) | pre-repair tool (byte copy taken before the edit) vs repaired tool: **stdout and JSON BYTE-IDENTICAL on 17 of 17**, rc 0/0 |
| P9b — every recorded subject has three pairwise-distinct extents | **HELD**, pinned as a permanent artifacts leg |

**P7 / P9a: HELD.** P9c held trivially (not blind, said so).

**The proof harness produced one false DIFFERS first, and it is the arc's cleanest
self-caught defect:** the first run passed different `--out` paths to the two tools, and
the one differing stdout line was `[topo] wrote <path>` — the tool printing the harness's
own argument back. Fixed by giving both runs the same path. A differing byte the harness
injected is not a differing behaviour — the E15 PNG-hash law, met again in stdout, at the
seat that was about to build the tool that separates exactly that class.

---

## 2b — three wraps; the server serves 7 of 8, then 8 of 8 (2c)

`mesh_topology` wraps `e14_topology.py` **alone**, with `e12_nonmanifold.py` named in the
payload notes (Ruling 4's disposition, carried structurally — T43 asserts the note).
`thin_extent_curve` wraps `e12_thin_curve.py`; `--preview` is deliberately not exposed
(artifacts for the eye, not payload numbers). `offsurface_rate` wraps `e12_offsurface.py`
**bake half only**, the erode/margin gap named in the payload notes and not computed.
`MEASURE_VERSION` 0.1.0 → 0.2.0 (surface 4→7) → 0.3.0 (2c, 7→8): the identity law is the
reason — `measure_report` refuses cross-version comparison, so two surfaces must not share
a number. **T40's pin moved twice, deliberately, in those commits.**

### P10 — the anchors: predicted 2 of 3, measured **3 of 3**. Band held, the blind row fell.

| wrap | recorded source | the digits reproduced at the served surface |
|---|---|---|
| `mesh_topology` | E14 gate-0, `longsword_00001` | shells **1** · boundary **0** / **0.0** · non-manifold **121** (0.0081%) |
| `thin_extent_curve` | E12 task 2b, the dragon, exact recorded invocation | one_px **6.718107e-04** · 0.01 → **15.304% / 26.819%** · 0.03 → **33.863% / 60.418%** |
| `offsurface_rate` | E12 task 2, the dragon, instrument defaults | **2.6430%** >1px · **2.4395%** >5px · max **377.6 px** · **3,240,510** uv-valid |

The CANNOT row's reasoning — "the recorded off-surface headlines are the ship's, produced
by `e10_offsurface`" — was falsified by **E12-task2's own validated table**, which recorded
fresh numbers from `e12_offsurface` itself on both subjects, ship (2.5065% against E10
Ruling 4's ruled 2.5%) and beast. The record had the anchor. *Enumerate the resource before
predicting its absence* — the same law, met at the prediction layer.

**Two anchor-precision findings, both mine, both corrected in the direction that hurt:**

- **T44's first run failed on a half boundary of my own construction**: the payload stores
  4 decimals (26.8195), the report printed 3 from the raw (26.819), and `round(26.8195, 3)`
  is 26.82. The pin is now the payload's own 4-dp values, each documented as printing to
  the recorded digits.
- **T45's first quad assertion demanded `median == 0.0` exactly** and failed on 2.98e-08 of
  float32 kernel residue — my test inventing a precision the instrument never claimed. The
  bound is 1e-3 px with the reason in the test.

Hermetic can-fail pairs ride each wrap: the quad prep reads 0.0 off-surface and its
meta-shifted twin reads **100.0**; the curve's endpoints pin 0 → 0% and huge → 100%; the
fixture ladder pins one defect class per mesh (two shells, non-manifold, open sheet with
boundary *length*).

---

## 2c — the eighth tool, at the Director's word

[Ruling 10](E28-ruling.md) commissioned it compare-only; Amendment 2 specified it; the
predictions addendum was committed first with **three rows declared dead as forecasts in
the file itself** — the instrument was drafted and validated in scratch while the 2a+2b
suite ran, before the addendum could be committed, and pretending those rows were blind
would be calibration theater. They score **SEEN**: the compress-level pair built on the
first attempt (P12), the tiers separated on it (P13), and blob-vs-scatter at equal 400-px
totals returned **LCC 400 vs 4** — a 100× separation against the ≥3× band (P14).

**The live rows:**

- **P15 (blind): predicted 12 tests, band 8–18; measured 9.** Band HIT, point −3 — fewer,
  not more: the six specified behaviours landed as eight tests plus one self-validating
  fixture leg, and the parametrization I predicted did not materialise because the
  refusal legs are single cases.
- **P16 (blind): HELD.** `anchor_check` carries no recorded-number anchor at birth, and
  the reason is structural: nothing this instrument produced is in the record, and the
  byte-hashes the record does carry (E08-armB state, E04 step 0) are single-artifact
  hashes whose *re-production* is the caller's replay act — the exact boundary Ruling 10
  drew. The test set is fixture-complete and anchor-free, and says so.

**What landed:** `tools/verify/anchor_compare.py` (compare-only; byte tier always with the
gate-eligibility caveat IN the payload; pixel tier with differing count/fraction, largest
connected component, |Δ| and Lab ΔE diagnostics, and the shape carried as an N×N grid,
never reduced); the served `anchor_check` wrap (envelope, `replay: caller-supplied`, the
e13 collision migrated into the served notes); **the owed fixture** — a pixel-identical,
byte-different PNG pair (7,406 vs 7,028 bytes, pixels equal), self-validating in T46 so a
regenerated pair that lost either property fails loudly.

**The instrument passed Ruling 3's entry checks in its entering commit**: flag surface (4
flags), `__main__` guard, B1 empty, axis F `true` in all three modes, axis G
`anchor_check` — the first file that question has ever attracted — and the census re-ran
`--committed` with T41's verify pin moved 8 → 9 deliberately.

**Two of my own test defects, self-caught by first runs:** the "no uniformity score" leg
grepped the payload for the *word* and fired on the note explaining why no such score
exists — a check written against the token rather than the specification, this repo's own
law; rewritten to scan keys. And a ratio assertion used the unqualified key where the wrap
follows the house style (`pixel.differing_fraction`).

---

## Findings for the ruling

**F11 — the serving surface's own hygiene is now measured, and it is the house style.**
`mesh_stats.py` and `gate1_sheet.py` serve today as unguarded module-level scripts (2-pre).
Nothing breaks — the server subprocesses — but axis F cannot probe them, so their
import-safety is structurally unmeasurable without adding guards, which is an instrument
edit nobody has commissioned. Stated, not proposed.

**F12 — a fifth front-door drift instance, in a phrasing the sweep structurally cannot
see.** `site/src/content/docs/handbook/getting-started.md` read *"Twenty of them are in
docs/experiments"* against a record of 28 — the count separated from its noun by three
words, invisible to the line-scoped phrase sweep by declared boundary. Found by a person
editing the file for the suite count; rephrased INTO the pinned form and pinned
(EXPERIMENT_PINS gained the site). The writing-convention remedy, applied at its fifth
instance.

**F13 — the T34 suite-count self-reference cost four bump rounds this seat** (736 → 782 →
789 → 790), the last +1 being the new experiment pin itself adding one parametrized test.
Every pinned surface moved in the commit that moved the count, which is the property
working — and the mechanical bump script that served three rounds produced two derivation
errors when regex-derived from itself, both caught by its own exact-count refusal. The
fourth round was hand-edited.

**Withdrawn from this seat's scope, stated plainly:** task 3 (`texel_provenance` largest
component — the named carry); the erode/margin half of `offsurface_rate` (open commission,
unchanged); anything touching the index DB or certificate (the advisor's).

---

## Compensators, discharged

| action | state |
|---|---|
| all four task-2 stages | tracked file edits; `git revert` restores each |
| the byte-proof + anchors against recorded trees | reads only; `--out` to scratch/tempfiles throughout; manifests 0/0/0 at baseline, mid, close |
| the fixture pair | two committed PNGs, self-validating in T46 |
| the index DB + certificate | untouched; the advisor folds the pair |

**Two seats shared this working copy throughout.** The advisor's fold (`a3e85db`) swept my
uncommitted README.md and advisor-kickoff count bumps into its commit — named in my 2a+2b
commit message rather than left to be discovered; HEAD moved under this seat twice
(Ruling 10's pair, the concept-prep fold) and both times the response was re-measure, then
sequence after. Both coordination saves were observational, which is E27 Ruling 9's
standing caveat, now instanced at a third pair of seats.

⛔ **Halting here. Task 3 is the named carry. The ruling extends in place.**
