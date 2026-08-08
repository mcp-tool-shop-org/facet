# E20 — unit coverage report

**Executor session, 2026-08-08.** Re-fired after the halt in
[E20-gate-halt.md](E20-gate-halt.md); both parked conditions met (E18 halted and
was ruled; `tests/fixtures/` authorship ruled to E18 by E20-ruling 2).

**End state: 202 tests passing, 140.67 s full / 47.01 s hermetic** (the tier CI
runs — 194 passed, 8 artifacts deselected). E20 added **110 tests in three new
files**, 11.64 s on their own. No failures, no re-run needed, so
E18-ruling 2l's run-then-rerun disposition was not exercised.

| | before E20 | after |
|---|---|---|
| tests | 92 | **202** |
| files under `tests/` | 15 + fixtures | 18 + fixtures |
| tools with a test that reaches them | 8 | **10** |
| guard sites demonstrably fired | 9 | **17** |

---

## 1. The mount — the dress rehearsal, and its premise was wrong

The dispatch says: *"you are the FIRST session in this repo with the true
in-session mount — `.mcp.json` predates you, so `mcp__facet-record__*` tools
exist."*

**Measured: they do not exist in this session, and `.mcp.json` does not predate
it.**

| fact | measurement |
|---|---|
| this session's start | ~11:23 (its first clock read was 11:23:36) |
| `.mcp.json` filesystem mtime | **11:30:42** — 7 minutes *after* |
| `.mcp.json` committed | 11:34:02, `5c4fa27` |
| `ToolSearch` by keyword | no `mcp__facet-record__*` tools |
| `ToolSearch select:` on all six names | `No matching deferred tools found` |

MCP servers mount at session start. This is the **same continuous session** that
was running when E18 created `.mcp.json` — the re-fire arrived as a new turn in
the parked session, not as the fresh session E18's ruling anticipated. So the
first-true-mount seat is still open, and it belongs to whichever session starts
next.

**The server itself is not the problem** — that was checked before concluding
anything. A standalone stdio `initialize` returns a well-formed result and exit
0, including its own instructions string ("Query this repo's governed decision
record instead of reading it").

### So the record was queried, through E18's own client

Rather than fall back to reading, the session drove the **same `MCPServer`
instance** through the SDK's `Client` exactly as `tests/mcp_support.py` does —
the server's dispatch, schema validation and error wrapping, minus the literal
wire. A scratch-only helper; no repo file added.

**What that was like, since the dispatch asks:**

- **`record_health` earned its keep in the first five minutes.** It came back
  `serving: false`, `INDEX_NEVER_VERIFIED`, *"the certificate describes a
  different index (certified a5c6afd0f138..., present d9f097eb45a7...)"* — the
  tracked DB and its certificate had drifted apart across the session boundary —
  and its hint named the exact fix. The tool that never refuses is how you learn
  the others are refusing, and that design decision paid immediately.
- **`record_build` ran the E15 ritual as one act**: build + all five legs +
  certificate, `state: PASSED`, determinism leg **byte-identity**, seeded 19/19,
  **3.17 s**. One call where the ritual used to be two steps that could be
  separated.
- **`record_query` answered a natural-language question at rank 1.** The query
  *"the fixtures builder pattern who authors it"* returned **E20-ruling Ruling 2**
  as row 1 of 6 — a ruling written hours earlier, found without knowing it
  existed. The holding line was enough to choose the pointer; `record_get` then
  returned the ruling's own 14 lines instead of opening a 5,640-byte document.
- **The certificate rides every response.** For an executor this is the part that
  matters most: it is not possible to read a stale index here without being told
  the index is stale, in the same payload as the answer.
- **One friction worth recording.** A hand-rolled stdio client got correct
  answers to `initialize` and `tools/list` and then **silently returned nothing
  for `tools/call`** — exit 0, empty stderr, no error. A silent no-answer is the
  worst failure shape for a client, and the fix was to stop hand-rolling and use
  the house pattern that already existed. Whether the server should answer or
  refuse a `tools/call` that reaches it that way is E18's lane, so it is
  **flagged here, not investigated**.
- **Boundary, stated plainly:** the record was queried; the *tool sources* were
  read directly. The index maps the record, not the code, and U1–U6 are about
  code. Query-first replaced document-reading, not source-reading.

---

## 2. THE STRUCTURAL FINDING — three of the six units are not units

This reshaped the session and it is the report's most consequential item.

**U2, U4 and U5 cannot be written as dispatched, because the tools are scripts,
not modules.** Measured by AST over each file's module-level body:

| tool | function defs | module-level body | importable? |
|---|---|---|---|
| `tools/facet_index.py` | many | constants + defs, `main` guarded | **yes** (U1 ran) |
| `tools/mask_geometry.py` | 1 | nothing executable | **yes** (U2 ran) |
| `tools/project_twins.py` | 8 | `ap.parse_args()` at L220, then the whole projection L235–L934 — raycast at L252, asserts at L885/886/908, image writes at L910–929 | **no** |
| `tools/texpass_finalize.py` | **0** | the entire tool | **no** |
| `tools/verify/mesh_stats.py` | 4 | pipeline at module level, `parse_args` at L52 | **no** |
| `tools/texpass_iter.py` | — | parses argv at import (already recorded in conftest) | **no** |

`texpass_finalize.py` is the sharpest case: **zero function definitions**. Both
lookup paths and all three ANDONs are straight-line module-level code, so U4's
"surface-aware nearest-painted-in-3D on a small synthetic mesh with
hand-computable answers" has nothing to call. `project_twins`' `figure_mask`
(L315) and `fit_background` (L345) — U2's named targets — are *defined after*
the pipeline starts executing, so importing the module runs the projection before
those names exist.

Also corrected: **`mesh_stats.py` is not in `tools/`** — it lives at
`tools/verify/mesh_stats.py`. The halt report's census scanned `tools/*.py` only
and therefore missed it, along with `tools/verify/` and `tools/diagnostics/`
entirely. `tools/` holds **150** python files, not 33.

### The seams are PROPOSED, not taken

The dispatch permits "testability seams under the law (tests + anchor, same
commit, proposed in the report if non-trivial)". Extracting a whole script's body
is non-trivial by any measure, and `texpass_finalize`'s output is byte-anchored
by T7 — so nothing was restructured. Proposed for the ruling:

1. **`project_twins`: move `figure_mask` and `fit_background` into
   `mask_geometry.py`, beside `local_thickness`.** The precedent is exact and
   blessed: `local_thickness` was extracted there for E16-10 for this very
   reason, with the twin-projection anchor re-run across the extraction. This
   would make U2's real targets — including the border-ring contamination
   question in P5 — unit-testable at all.
2. **`texpass_finalize`: wrap the body in `main()` behind a `__main__` guard, and
   lift the lookup into a function taking arrays.** T7's byte-identity anchor is
   the re-run that proves the extraction moved nothing.
3. **`mesh_stats`: `main()` guard only.** `measure(path, label)` is already a
   function; it is unreachable solely because import executes the pipeline.

Each is one commit with its anchor re-run, and each unlocks a unit E20 was asked
for and could not deliver. **The executor does not decide whether to take them.**

---

## 3. Per-tool coverage

| unit | tool | landed | remaining, and why |
|---|---|---|---|
| **U1** | `facet_index.py` | **68 tests (T24)** — both arc derivations + the asymmetry, discovery patterns with near-misses, the measured 151/152 marker convention and its closure exception both directions, the required space before the dash, the unnumbered handoff header, the status-position law with its adjectival case, `paragraphs`' blank-line discriminator with true line numbers, `bold_lead_title` across wrapped lines + the unclosed run, `one_line`/`strip_md`/`find_date` boundaries, the supersession verbs' conservative under-count, the claim families' range/cardinal split and the starts-at-1 rule, the ambiguous suffixes, `ARC_RE`, `classify_document`, the tokenizer's never-empty guarantee, `_sequence_gaps` as a set property with a can-fail leg | `parse_*` end-to-end row shapes stay T1's (whole-build replay); `_parse_amendments`/`_parse_subs` block-splitting not unit-reached |
| **U2a** | `mask_geometry.py` | **33 tests (T25)** — equality with an independently written explicit-disc oracle on 8 shapes, `R = ceil(W/2)` measured then pinned, monotonicity, thin-beside-wide separation, the off-mask characterization, and **the A3 safety property per width with margins** | — (the module is fully covered; it is 33 lines) |
| **U2b** | `project_twins.py` core | **nothing** | `fit_background`, `figure_mask` unreachable — §2. P5 and P6 stand unresolved; seam 1 unlocks them |
| **U3** | `texpass_iter.py` write-head | **nothing new** | T2b (E18) covers the hermetic selftest on D2; T11 covers `--edge-mode`. The A32 byte-identity property as a *unit* with a violated-by-construction leg, the job-mask derivation, and the emit-guard message contract (P11) remain. Subprocess-only, and D2 is the substrate — deliverable without a seam |
| **U4** | `texpass_finalize.py` | **9 tests (T26)** — both lookup paths, **all three ANDONs fired and proved to refuse the write**, a clean run firing neither, the structural-vs-earned zero distinguished, edge-length scale-invariance, and the tessellation lever proving it is measured per mesh | no unit-level lookup on a hand-computable mesh — §2, seam 2 |
| **U5** | `tools/verify/mesh_stats.py` | **nothing new** | T12 covers the warning condition by subprocess. The four subject classes' geometry, the `rect_frac` 0.99/1.0/1.01 boundary (P15), the welded-vs-unwelded shell census, and the frame math (P16) remain. Needs synthetic GLBs — a fixture beside D2 — and seam 3 for `measure()` |
| **U6** | all of `tools/` | **the census, §4** | per-guard can-fail treatment for the 392 unfired sites is a program, not a session — §4 gives the prioritized strata |

---

## 4. U6 — the guards-can-fail census

Scope per **E20-ruling 3**: every `assert`/ANDON/refusal in `tools/`,
`record_mcp.py` included, and the audit **cites** the existing test that fires a
guard rather than re-proving it.

**Method, with its bound stated.** Guard sites are found by **AST** — an
`assert`, a `raise`, a `sys.exit` call — not by grep, so a comment that merely
*names* an ANDON is not counted as one. Firedness is detected by sliding an
18-character window over each guard's own static message text and asking whether
any window appears in the test suite. **This is a lower bound:** a test that
fires a guard without quoting its message is invisible to it. The first cut of
the detector asked the question backwards (whole message run present in the
tests) and **undercounted its own author's tests 2 of 3** — fixed, and recorded
here because a census whose method miscounts in a known direction is worth less
than one that says so.

| stratum | files | guard sites | with "ANDON" | demonstrably fired |
|---|---|---|---|---|
| `tools/*.py` (top level) | 31 | **204** | 161 | **15** |
| `tools/verify/` | 6 | 8 | 1 | 0 |
| `tools/diagnostics/` | 65 | 186 | 160 | 2 |
| `tools/superseded/` | 7 | 11 | 1 | 0 |
| **TOTAL** | **109** | **409** | **323** | **17 (4.2%)** |

Top-level alone: **15 of 204 = 7.4%**.

**The 17 fired**, with what fires them:

| guard | fired by |
|---|---|
| `record_mcp.py` L291/298/305 (`CONVENTIONS_INVALID`, `SEEDED_SET_INVALID` ×2) | E18's T19–T22 |
| `record_mcp.py` L497/509/514/516/525/534 (certificate + verify refusals) | E18's T20/T21 |
| `texpass_finalize.py` L129/132/176 (both distance ANDONs + uniform atlas) | **E20's T26** |
| `texpass_iter.py` L497 (`ANDON: holes did not shrink`) | T11 / T2b |
| `facet_index.py` L186 (the discovery inverse guard) | T4 |
| `e11_export_turnaround.py` L278 (owner-atlas purity ANDON) | an existing test quoting it |
| `e14_pair_readout.py` L78, `e14_repair_collar.py` L133 | existing diagnostics tests |

**The largest unfired class, and the priority:** `e11_manifest.py` (37 guards, 0
fired) and `e11_export_turnaround.py` (26 guards, 1 fired) — **63 guard sites,
one fired**, in two ~50 KB export-path tools. `project_twins.py` is next at 19
guards, 0 fired.

**A scope question for the ruling, flagged not decided.** `tools/superseded/` (11
sites) holds approaches kept *because they fail* — "anyone can run those tools and
watch them fail the same way." A can-fail test there would assert that a
falsified approach still fails, which may be exactly right or exactly pointless.
Likewise `tools/diagnostics/` is 65 research instruments, 186 sites, and E19
already treated that class as out of scope for a different gate. The census
reports the strata separately so the advisor can rule on which of the 409 the
audit is actually about; **E20 does not narrow it unilaterally.**

---

## 5. Predictions scored

Committed blind in [E20-predictions.md](E20-predictions.md) before any unit's
internals were read. **8 hit, 3 missed, 1 partial, 6 unsettled** (the units that
could not run), plus 2 lookups that were never predictions.

| id | outcome | measurement |
|---|---|---|
| P0 | **L** | not a prediction, as disclosed |
| P1 | **HIT** | mainline forms passed unchanged; the only two failures in T24's first run were my own wrong expectations |
| P2 | **MISS** | predicted loose anchoring in the status-position law. `classify` is case-sensitive and correct; the adjectival sentence returns `None`. My model was inverted — the convention rules are the well-guarded part, because this one had already been found and fixed once and its docstring carries the story |
| P3 | **MISS** | the closure exception is exactly scoped, both directions clean. Single special cases are safer here than I credited |
| P4 | unsettled | the claim-family *patterns* are covered; AMBIGUOUS *routing* is T5's, and no misclassification was found or looked for at that level |
| P5 | unsettled | `fit_background` unreachable (§2). The border-ring contamination question is untested and now a named worklist item |
| P6 | unsettled | `figure_mask` unreachable (§2) |
| P7 | **PARTIAL** | right place, wrong severity. Parity IS real — `R = ceil(W/2)`, so W=1 and W=2 both return 1 — but it is designed integer quantization, not an off-by-one defect |
| P8 | **HIT** | the A3 property holds, zero violations over 10 widths. Tightest margin **×1.50 at W=1** (peel 0.333 px against a true half-width of 0.500); every wider structure ≥ ×2.25. Agrees with E16-10's measurement on real structures |
| P9 | **HIT** | `mask_geometry` is numerically correct and its finding is exactly an interface contract: **R is nonzero off the mask**. Better than predicted — a consumer had already been bitten (`texpass_iter:437`, 38,041 texels vs 4,344) and both consumers now gate membership explicitly |
| P10 | **L** | D2 was absent then; it exists now |
| P11 | unsettled | write-head commit properties not reached this session |
| P12 | **FALSIFIED** | my highest-confidence defect prediction. The edge length is **measured per mesh** and the tool prints "(measured on this mesh)". My first test asserted a 3× rescale would move it, measured 1.00000 twice, and the cause was **normalization** (L103 divides by `max|component|`), which is *required* because the gate is a ratio and both operands must share a frame. The premise was mine. Tessellation is the lever that actually tests per-mesh-ness, and it passes |
| P13 | **HIT** | both distance ANDONs fire, exit 1, **and refuse before writing the atlas** — a third (uniform atlas) fired too |
| P14 | **HIT** | the structural and earned zeros are distinguishable, and it was the cheapest proof in the session. The tool already labels its own: "STRUCTURAL in surface-aware mode ... not a measured pass" |
| P15 | unsettled | `mesh_stats` unreachable (§2) |
| P16 | unsettled | frame math not reached |
| P17 | **HIT, to the decimal** | predicted the grep census overstates distinct guards ~2:1. Measured **431 grep-shaped lines against 204 AST sites over the same top-level files = 2.11:1** |
| P18 | **HIT, both halves** | predicted <15% fired and the e11 pair as the largest untested class. Measured **4.2% overall / 7.4% top-level**, and the e11 pair is **63 sites with 1 fired** — the largest by a wide margin |
| P19 | **HIT** | `record_mcp.py` is in U6's scope; E20-ruling 3 confirmed it and refined the treatment to cite-not-re-prove |

**The calibration lesson.** My three misses cluster: P2, P3 and P12 all predicted
a defect where the record had *already documented the fix*. Each of those
functions carries the story of the bug it once had, and I read the story as a
live risk instead of as a closed one. The predictions that landed (P8, P17, P18)
were about **quantities**, not about whether someone had been careless.

---

## 6. Findings, per the assertion law

Reported with evidence; **no test pins any of these either way** before the
ruling.

**F1 — `github_slug` has zero callers and makes an unverifiable external claim.**
Defined at `facet_index.py:261`, named for "GitHub's heading anchor algorithm",
and called nowhere in `tools/` or `tests/`. It collapses whitespace *runs*
(`\s+` → one hyphen), so `## Ruling 25 — The Thing` yields `-ruling-25-the-thing-…`
where a per-space replacement would give a double hyphen. Whether that matches
GitHub could not be verified offline. Nothing depends on the answer today. The
test pins only what the implementation states as its own intent, and explicitly
not the collapse. *Disposition for the ruling: verify against a rendered anchor,
or retire the function.*

**F2 — `texpass_iter:437`'s comment is imprecise about a real defect it fixed.**
It says an off-mask candidate "has d_s = 0 and **thick_s = 0**". Measured:
`local_thickness` returns **nonzero** values off the mask for background within
`r` of a core (T25 pins this). So for background *near* the figure `thr` is
positive and `d_s = 0` is correctly rejected; the admit-everything failure needs
background *far* from any core. The conclusion and the fix are unaffected — the
explicit membership check is right either way, and the recorded 38,041-vs-4,344
measurement stands. Only the stated mechanism is narrower than the comment
implies. *Low severity; a comment correction, not a code change.*

**F3 — a `tools/call` that reaches the server by a hand-rolled stdio client can
get no answer at all**, silently: exit 0, empty stderr, `initialize` and
`tools/list` answered normally, `tools/call` returning nothing. Not diagnosed —
E18's lane. Flagged because a silent no-answer is the worst failure shape a
client can meet, and the repo's own law is that a check which cannot fail is not
a check; a call that cannot answer *or* refuse is the same family.

**F4 — the halt report's census was wrong in scope and in kind**, corrected in §2
and §4 of this report: it scanned `tools/*.py` (33 files) where `tools/` holds
150, and it counted grep-shaped lines where the guards are AST nodes. Recorded as
a finding against my own instrument rather than quietly replaced.

---

## 7. Lane and law compliance

- **No `conftest.py` edit.** Three new files at T24/T25/T26 (E18 holds T19–T23).
  The two conftest fixtures used — `facet_index_mod`, `built_db` — already
  existed; `built_db` keeps T24 off the tracked DB.
- **E18's fixture consumed, never edited** (E20-ruling 2). T26 copies
  `selftest_min` into `tmp_path` and places the mesh where finalize looks for it;
  an autouse fixture hashes the committed tree before and after **every** test in
  the file and fails if a byte moved.
- **No tool behavior changed.** Zero seams taken; three proposed in §2.
- **Source is ASCII bytes** in all three files. The dash constants are built with
  `chr()` rather than typed — a first pass converted them to `"--"`, which would
  have left every dash test **passing while testing nothing**, since the dash
  class is one character and a two-hyphen stand-in matches on its first hyphen.
  A weakened test that still passes is worse than a failing one.
- **No coverage theater.** Every test asserts an outcome. The two tests whose
  only job is a negative (`_declines_to_guess`, `_a_clean_run_does_not_fire_either_andon`)
  exist as the other half of a can-fail pair and say so.
- **CI runtime budget respected**: hermetic tier 47.01 s against the ~3 minute
  bound. Nothing new carries `slow`.
- **No memory-store write. DB and certificate left uncommitted** per E18-ruling
  2's amended pair cadence; `record_build` regenerated both at session start.

---

## 8. The worklist this leaves

In the order it is cheapest to pay:

1. **U3** — the write-head's commit properties on D2. No seam needed, substrate
   exists.
2. **U5** — synthetic GLBs for the four subject classes, the `rect_frac`
   boundary, the frame math. A fixture beside D2, plus seam 3 for `measure()`.
3. **Seam 1** → U2b, which unlocks P5's border-ring question — the one
   unresolved prediction with a named failure mode nobody has looked for.
4. **Seam 2** → U4 at unit level.
5. **U6's can-fail program**, prioritized by §4: the e11 pair first (63 sites, 1
   fired), then `project_twins` (19, 0).

**HALT.** The advisor rules at `E20-ruling.md`.
