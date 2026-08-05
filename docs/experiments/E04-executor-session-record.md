# E04 — executor session record, 2026-08-04 evening → 2026-08-05

**Closing at the context boundary, on the Director's offer and with the advisor's dispatch
already written** (Session handoff 2, `c6cc919`). Stopping here rather than starting the
stroke derivation is the precedent Ruling 12 endorsed by name: *a run you cannot see through
is worse than a clean halt at a passed anchor set.* **Nothing is half-done. The working tree is
clean.**

This file is the executor's record — what ran, what fired, and the traps a fresh session would
otherwise pay for again. The *dispatch* is in the kickoff; the *rulings* are in
`E04-ruling.md`. Neither needs repeating here.

---

## Where it got to

**The galleon is painted.** Stage 1: **1,147,959 of 3,111,817 valid texels = 36.89%**, which is
**86.4% of the pre-registered 42.72% ceiling**. Owner and blend sidecars native. Ratified,
Ruling 23.

Arms completed this session: **G7** (one byte-matched generation) · **T** (eight twins, one
A23 re-roll, full baseline) · **stage 1 projection**. Plus the ship's prep bake, the H4
ceiling, and the profile brought to **coverage 0 undecided**.

## Nine halts, and what each one bought

Every one fired on a gate or a discipline this repo already had. None was improvised past.

| # | halt | what it caught |
|---|---|---|
| 1 | Arm T, pre-flight | H2 falsified — elevated twins need elevation in three shared tools |
| 2 | " | `restylize_views.aspect` — a dead profile key; in-tool ANDON on load |
| 3 | " | profile missing `fit-axis`; would have rendered in the un-adjudicated mode |
| 4 | 1072 anchor | a nonzero row, and one **interior tessellation pinhole** Ruling 11's readings didn't name |
| 5 | bake guard | a growth assert the identity can never satisfy at `head-scale 1.0` |
| 6 | bake identity | strict equality off by **exactly 2 float32 ULPs** — falsified the ruling's own "measured: exact" |
| 7 | classification | majority-**not**-red, against the ruling's expectation |
| 8 | A23 re-roll | row changed materially; the accepted set was no longer the set that would project |
| 9 | `project_twins` bg probe | **W3's 2.0% bound**, inherited by silence, halting every ship view forever |

Halt 9 is the one that closed a class rather than an instance: it produced `--coverage`, which
found **41 more keys** inheriting the character's numbers by silence.

## Traps I paid for — do not pay again

- **`binary_fill_holes` on a porous subject destroys registration.** It reported IoU **0.632**
  where the raw key reads **0.844** — rigging encloses background and the fill swallows it. A
  collapse on two views and not six is a *shape* story. Check the operand.
- **A `dry_run` PASS does not prove link sanity.** A hand-retyped graph with
  `VAEDecode.samples = ["14",0]` — a node linking to itself — returned `status: validated`.
  Every workflow since is read from its saved file and link-checked in code.
- **Signed GCS URLs must be used verbatim.** Reconstructing one without
  `response-content-disposition` returns 403; the signature covers it. Two attempts lost.
- **`e08_ceiling.py` prints three settings blocks and the third's label is hardcoded text.**
  With `head-facing-min` equal to `facing-min` all three return identical numbers, which reads
  like three confirmations and is one measurement printed three times. Verified by re-running
  at a genuinely different floor. One-line fix, queued.
- **`palette_gate.py` accepts `null` for `max_offpalette_pct` but requires an int for
  `max_offpalette_blob_px`** — so it cannot express the spec's "no numeric pass bound". The
  workaround here was a **scratchpad copy** with a vacuous 10⁹, canon untouched, and the
  verdict column discarded as meaningless. Queued.
- **`1066` is not a legal diffusion width.** Any frame fed to the Qwen VAE must be divisible by
  8 (16 preferred). Derive from the mesh, then round to a generator-legal width — now a
  CLAUDE.md standing constraint.

## Artifacts, by directory

| path | what it is |
|---|---|
| `E04_armT72/` | **the live set** — clay, masks, controls, twins, workflows, stage1/, ceiling/ |
| `E04_armT72/twins/twin_7_REJECTED_seed770700.png` | the A23 rejection **and E10's founding exemplar** — 2,002 px of implied water, h 262.6, C\* 14.4 |
| `E04_armT/` | the **1064-frame record** — the frame-discovery batch, preserved per Ruling 15 |
| `E04_armT_diag/` | height-vs-width framing diagnostics |
| `E04_g7/` | Arm G7 — sheets, sidecar, measurements |
| `E04_shipprep/` | the prep bake — `meta`/`pos`/`nor`/`mask`/`prep_uv.glb`, res 4096, uniform atlas |

Cloud: 17 generations total this session (1 G7 + 8 + 8 + 1 re-roll, minus the 8 superseded),
**0 credits throughout**, **1 re-roll of 1 allowed, spent.**

## New instruments left in the repo

`e04_g7_landing.py` · `e04_g7_where.py` · `e04_g7_sheet.py` · `e04_twin_baseline.py` ·
`e04_profile_check.py --coverage` · the scale-aware branch in `bake_hero_prep.py`.

## Standing rhythm for the next session

Watchdog before every local GPU step — it went stale once mid-session and the check is two
seconds. Cloud discipline unchanged: workflow saved before submission, link-checked in code,
`dry_run`, `estimate_credits`, sidecar, predictions committed blind before the artifact exists.

## Open, and not mine

The Director's two windows stay open and non-blocking: **masthead gold** (three gilded spires
where the fixture declares one) and **G7's colour** (red as authored, landed on two views). The
`_NOT_CLEARED` lift, the side-stroke derivation and the brush fixture are the next dispatch,
already written.

## What I got wrong, in one place

Predictions: **3 of 10 clean on Arm T, 2 of 7 on Arm G7**, and two Arm T rows were not merely
wrong but *inverted* — T3 and T10, both because I reasoned from projected area on a subject
that answers by rigging. The `fill_holes` artifact was mine and would have put a false 0.632
into the record had I not checked it. The sub-40° window I built for Arm G7 took its edge from
a cluster statistic and applied it to pixels, so it measured warm-above-the-floor rather than
red — the fourth moving-denominator instance in this repo and the first in an instrument I had
written an hour earlier.
