# E20 — blind predictions

**Written 2026-08-08 by the executor, BEFORE reading any unit's internals and
before writing a single test.** Committed ahead of the work per the dispatch
(`E20-coverage-kickoff.md`, "Blind predictions first, committed").

Blindness is disclosed **per row** (the E19-predictions precedent). A row marked
**L** is a **LOOKUP** — a fact measured or read before the row was written, and
therefore **not a prediction** and not scoreable as one. A row marked **P** is
blind on the code it concerns.

## What had been read when these were written

CLAUDE.md in full; `docs/experiments/E20-coverage-kickoff.md` in full;
`tests/conftest.py` in full; `docs/experiments/E18-index-mcp-kickoff.md` lines
85-124; directory listings and file sizes for `tools/` and `tests/`; the guard
census quoted in P17/P18; the session-start ritual output.

**NOT read: the internals of any unit under test** — `facet_index.py`,
`project_twins.py`, `mask_geometry.py`, `texpass_iter.py`, `texpass_finalize.py`,
`mesh_stats.py`. U1-U5's rows are blind on the code.

Where a row is reasoned from a **law in CLAUDE.md** rather than from the code, it
says so. The law is the record's *claim* about the code, not the code — and an
inherited claim is a hypothesis wearing a fact's clothes, so such a row is a
prediction about whether the record still describes the tool.

---

## P0 — the sequencing gate (LOOKUP, not a prediction)

| id | statement | kind |
|---|---|---|
| **P0** | E18's halt state was **not** predicted before being checked. Checking the dispatch's own precondition was step one of the session, so E18's live state, D2's absence, and the 32 → 86 test-count growth are **measurements**, not hits. | **L** |

Stated explicitly because a gate that fires is the most tempting thing in a
session to retroactively claim you saw coming.

---

## U1 — `facet_index`'s parsers

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P1** | The mainline heading forms **pass unit probes unchanged**. T1 already adjudicates ~1,500 pointers through these parsers, so the common path is anchored by the densest test in the repo; unit tests here document rather than discover. | **P** | If mainline forms fail on synthetic-but-legal headings, T1's pointer density was covering a narrower input space than its count suggests — the count was reading as coverage. |
| **P2** | **The single most likely defect in U1 is loose regex anchoring in the status-position law** (capitals carry verdicts; lower-case "accepted" is an adjective). A convention-encoded rule has no syntax enforcing it, so a status word gets matched **inside prose** — the mention-vs-use family that has already fired twice here (E17's T18 assertion firing on its own refusal message's quotation). | **P** | If the convention rules hold and the *syntax* rules break instead, my model of where this repo's parser risk lives is inverted — conventions would be the well-guarded part. |
| **P3** | The measured-marker convention's **one closure exception** carries an off-by-one or over-fires on a second unintended heading. A lone special case is where this bug class lives. | **P** | If the exception is exactly scoped, single special cases are safer here than credited, and "exception" should stop reading as a defect smell. |
| **P4** | In the claims families, **AMBIGUOUS is where a fixture will disagree with the tool** — a residual class silently absorbs misclassifications. At least one synthetic claim string that should classify as range or cardinal lands in AMBIGUOUS. | **P** | If AMBIGUOUS is tight, the families were specified rather than accreted, and the residual-class heuristic does not apply to this parser. |

## U2 — `project_twins`' pure core + `mask_geometry`

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P5** | **`fit_background` passes on synthetic gradients including the vignette case, and has no guard for a figure that touches the frame edge.** The border ring is the estimator's sample; a figure intersecting the ring contaminates the fit. Highest-value U2 prediction, because the failure is invisible on every fixture whose figure floats clear of the border. | **P** | If a ring-contamination guard is already there, the fitted estimator was built with more care than its predecessor's history implies, and the corner-median lesson generalised further than the record says. |
| **P6** | `figure_mask` **passes** on constructed synthetic figures. Post-E16 the *is-there-surface* question is answered by geometry, and the corner-median path is named retired in CLAUDE.md. | **P** | A failure here means the retirement is complete in the record but incomplete in code — exactly the drift the repo-is-the-record discipline exists to prevent. |
| **P7** | `local_thickness` returns correct widths on synthetic shapes but carries an **off-by-one at width parity** (even vs odd) and/or at **width 1**, where "half-width" has no integer answer. | **P** | If parity is handled, the function was written against the thin-structure law rather than merely surviving it. |
| **P8** | The **A3 invariant property-tests to ZERO violations** over generated thin/wide/mixed shapes. E16-10 measured zero violations on real structures; a property test over generated shapes should agree. | **P** (blind on code; **anchored on E16-10's ruled table**) | A violation means the invariant as *implemented* is not the invariant as *ruled*, and the ruled table describes something else. That is a finding, not a test failure. |
| **P9** | `mask_geometry` (1,497 bytes) **passes numerically**; its finding, if any, is an **undocumented dtype contract** (bool vs uint8, 0/1 vs 0/255) at the boundary rather than a numeric defect. Small pure modules fail at their interfaces, not in their arithmetic. | **P** | If the numerics break in 1.5 KB, size is no proxy for correctness here and every small module needs a large module's scrutiny. |

## U3 — the `texpass_iter` write-head

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P10** | **U3 cannot run: D2 does not exist.** `tests/fixtures/` is absent; D2 is E18's deliverable and the dispatch names it U3's substrate. | **L** | — (measured, not predicted) |
| **P11** | *Conditional on D2 arriving:* the **A32 byte-identity property HOLDS** and its violated-by-construction leg **fires** — A32 has already fired live on stroke 7 of a real brush run, so it is a guard with a witnessed firing. The defect risk sits in the **emit guard's message, not its logic**: the message cannot distinguish "0 admitted because `--edge-mode global` is wrong for this structure" from "0 admitted because the job was empty". Two causes, one string. | **P** | If the message already separates them, the emit guard was written by someone bitten by exactly that ambiguity, and its message contract is stronger than the dispatch implies. |

## U4 — `texpass_finalize`'s lookup

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P12** | **Highest-confidence defect prediction of the session: the triangle-edge-length unit is still pinned to one mesh's scale.** CLAUDE.md states `texpass_finalize.py` "had that edge length hardcoded from one mesh". A synthetic mesh at a different scale exposes it — the global-constant-governs-a-local-feature family, which has cost this repo three sessions. | **P** (blind on current code; **reasoned from CLAUDE.md's claim**, itself a hypothesis) | If it is already derived per-mesh, the law's "had" is past tense and the fix landed without the record saying so — worth correcting in place either way. |
| **P13** | **Both distance ANDONs FIRE** on constructed violations. Whether they can fire is the whole question U6 exists to ask, and a constructed violation is the cheapest way to ask it. | **P** | An ANDON that cannot be fired by a deliberately constructed violation is a check that cannot fail — the class three seats paid for this week, found again. |
| **P14** | The flood path's **earned** zero and the surface-aware path's **structural** zero are distinguishable in a unit fixture, and this is the **cheapest can-fail proof in the session**. | **P** | If they are not separable at unit scale, the distinction the record draws between them needs the recorded tier to hold it. |

## U5 — `mesh_stats` + the frame-derivation math

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P15** | Fit-axis / margin / aspect **pass** across the four subject classes. The **T12 warning boundary is a `>` vs `>=` question**, and exactly one of rect_frac 0.99 / 1.0 / 1.01 sits on the wrong side of the author's intent. | **P** | If all three land as intended, the boundary was specified rather than inherited from whichever comparison operator was typed first. |
| **P16** | The frame derivation's **÷8 legality rounding can round a width DOWN below the margin it just computed**, or the ÷16 preference is documented but unenforced. CLAUDE.md says W3's 752 and the pair's 1024 "passed by luck" — luck is not a guard. | **P** (reasoned from CLAUDE.md) | If rounding is margin-aware, the luck was retired when the law was written and the law's wording is stale. |

## U6 — the guards-can-fail audit

| id | prediction | kind | what a miss teaches |
|---|---|---|---|
| **P17** | The grep census **overstates distinct fireable guards by roughly 2:1**. This repo writes long explanatory comments naming an ANDON directly above the code that raises it, so a guard is counted more than once. | **P** (the census numbers are **L** — measured before this row was written) | A ratio near 1:1 means the ANDON vocabulary appears only at raise sites and the census is closer to a guard count than credited. Above ~3:1 the census is useless as a scope estimate. |
| **P18** | **Fewer than 15%** of guard sites in tracked tools have a can-fail test today, and the **largest untested class is `e11_manifest.py` + `e11_export_turnaround.py`** — 125 guard-shaped lines across two ~50 KB tools. | **P** for the <15% and for "largest class"; the 125 and the file sizes are **L** | If coverage already exceeds 15%, the in-tool invariant discipline has been quietly doing the harness's job and U6's yield is documentation rather than discovery. |
| **P19** | **U6 cannot be closed before E18's fold.** `tools/record_mcp.py` — E18's uncommitted deliverable, 43,691 bytes, 35 guard-shaped lines — sits in `tools/`, so it is inside U6's stated scope ("every `assert`/ANDON/refusal in `tools/`"). A list built now is wrong by construction the moment E18 commits. | **P** on the ruling's intent; the file's existence and census are **L** | If the advisor rules `record_mcp.py` out of U6's scope (E18's tests are its own lane), this row is a miss worth having made explicit. |

---

## Scoring

P1-P9 and P11-P18 are scoreable only after the units run. **P10's and P19's
premises are already measured** and are reported in
`docs/experiments/E20-gate-halt.md` as the halt's evidence, not as hits.
