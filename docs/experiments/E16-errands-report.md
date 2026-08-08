# E16 — the errand batch: report

**Executor session, 2026-08-08.** Dispatch:
[E16-errands-kickoff.md](E16-errands-kickoff.md). Eleven queued repairs, one
errand one commit one anchor, safest first.

---

## 0. Blind predictions, committed before any anchor ran

Written and committed in their own commit before the first tool was read into
or edited. Each names the anchor's expected outcome and, where a prediction
can be sharper than the dispatch's own wording, says something the dispatch
does not.

| # | anchor's expected outcome | the sharper prediction, where I have one |
|---|---|---|
| 1 | byte-identical DB; verify 19/19 under BOTH encodings | **The literal `↑` repair alone will NOT be sufficient.** cp1252 covers `—`, `·`, `×`; it does not cover `↑`, `→`, `≥`, `≈`. Legs 3 and 4 print *data-derived* text (document names, ruling titles) and never executed under cp1252 in the baseline, because leg 3 crashed first. I predict at least one printed row carries a character outside cp1252, so a literal-only fix moves the crash downstream rather than removing it. A stdout-level repair is needed in addition to the literal. |
| 2 | `git status` quiet after touch-and-restore; build+verify identity holds | `git add --renormalize .` stages **zero content changes** — the index is already LF (the per-commit warnings are the working-tree→index direction, so the index side is already normalised). The `.db`/`.png`/`.npy`/`.glb` binary marks change no bytes; git already treats those as binary. DB sha stays `67ebd45…`. |
| 3 | `atlas_final.png` byte-identical | Byte-identical. A print cannot move bytes, and I will assert it rather than assume it. Secondary: the recorded `run/final` inputs replay read-only into scratch without touching the citable tree. |
| 4 | profile-bound emit byte-identical; unprofiled exits non-zero | **At least one live caller lacks `--profile`** and will need an explicit frame in the same commit — that is why the guard is a repair rather than a no-op. If every caller is already profiled, the guard is free, and that is itself worth reporting. |
| 5 | every VALUE unchanged; W3/galleon/beast warning state unchanged; sword NOW warns | The sword warns and W3 does not (W3 is the instrument's native subject). **I do not know that galleon and beast stay silent** — `rect_frac_of_figure > 1` is a face-rect-larger-than-figure condition and a ship or a beast could cross it. If either crosses, the dispatch's "unchanged" expectation is wrong; that is a finding to report, not to tune around. |
| 6 | N6/N8 exact against 51.005% / 51.3342% | Exact. Caption text and a warning print cannot move a reach number. Secondary, both of 6e's claims re-measured rather than inherited: the three `SETTINGS` blocks evaluate identically, and the front-back OVERLAP line is structurally zero. |
| 7 | reproduce 53.92% within ray-sampling noise | **Reported delta, not byte-identity** — this errand changes the default. I predict the repaired default lands within ±0.5 points of the ladder-converged 53.92%, and that runtime rises substantially: a floor at ratio ≈ 1 against a default that ran 3.71× coarser than the mean face means roughly an order of magnitude more rays. |
| 8 | projection outputs byte-identical; probe percentages reported | Byte-identical outputs (the probe is report-only). The new probe percentage **falls** on most twins — Ruling 21e measured the corner-median reference wrong by ΔE 11–21 and moving a reported percentage ~4× — so I predict the new numbers are lower, by roughly a 2–4× factor. |
| 9 | same rows before and after; guard fires on a synthetic miss | Same rows — I expect the hardcoded list is currently complete, because the sessions that added handoffs maintained it. **If the glob discovers a file the list omits, rows change and the dispatch's anchor expectation is wrong**; that is the finding, and I report the delta rather than trimming the glob to match. |
| 10 | stroke 1's 4,344 texels byte-identical at the default | Byte-identical at `--edge-mode global`. The local mode's delta is reported with per-structure numbers and adopted nowhere. |
| 11 | build + verify PASSED; sweep 0 STALE / 0 new UNDECIDED | As dispatched. The risk here is a missed reader, not a wrong value — a rename that half-lands shows up as a new UNDECIDED, which is exactly what the anchor watches. |

**Baseline captured before the first change:** verify PASSES all four legs,
19/19 seeded, under `PYTHONIOENCODING=utf-8`; verify CRASHES under default
cp1252 at `facet_index.py:1768` (`UnicodeEncodeError: '↑'`) — Ruling 31f
reproducing exactly. DB after a clean build:
`67ebd4576bb450f4b79b1df9ffc603f3d5792560ec27cc99aa2ccde021d004f5`, and the
build is byte-deterministic (two consecutive builds, identical sha). The DB
in `HEAD` predates the two kickoff documents committed at `cff21e9`; the
rebuilt DB rides with errand 1, whose subject is the index tool.

---

## 1. Per-errand results

**Summary — one errand, one commit, one anchor.** Ten repairs landed; **one
halted with nothing changed** because its anchor was falsified.

| # | finding | change | anchor | commit |
|---|---|---|---|---|
| 1 | Ruling 31f — verify's `↑` crashes under cp1252 | 17 print literals folded to ASCII (AST-scoped) + stdout errors relaxed | **HELD** — 19/19 under BOTH encodings; DB byte-identical both ways | `2a86329` |
| 2 | CRLF warning on every commit | `.gitattributes`, LF pinned both sides, renormalized | **HELD** — status quiet, zero content staged, verify PASSED | `76d3c1f` |
| 3 | Ruling 31d.1 — the fallback count is structural in surface-aware mode | print branches; flood path verbatim | **HELD** — `atlas_final.png` `a0f51101…` on both sides, = the recorded artifact | `0e60e45` |
| 4 | Ruling 29c — unprofiled `emit` guesses a 752-wide frame | `emit` refuses without `--profile`/`--aspect`; 2 callers gain explicit frames | **HELD** — recorded yaw-0 job byte-identical both sides; unprofiled exits 1, writes nothing | `c8c31ee` |
| 5 | Ruling 2d — `mesh_stats`' warning fires on a proxy | **none — HALTED** | ⚠ **FAILED** — the dispatch's two clauses contradict on the data | `d0cada0` |
| 6 | Rulings 6e/10b — false captions, a check that cannot fail, unwarned bias | captions built from the values; overlap line honest; wall-floor warning; `settings_index` | **HELD** — all 19 values identical; N8 = 51.33% exact | `0defa32` |
| 7 | Ruling 10a — ray grid taken from a generation frame | grid derived from rays-per-mean-face; ratio printed; `--exact-grid` | **HELD** — 53.967% vs the recorded 53.920% | `95f8c1f` |
| 8 | Ruling 21e — the retired corner median's last live consumer | fitted border-ring surface sampled per texel; one `fit_background` | **HELD** — all five projection outputs byte-identical | `3d5b65e` |
| 9 | the kickoff list is LISTED, not discovered | sorted glob + inverse guard + printed list | **HELD** — claims sweep byte-identical; 2 hidden rows recovered | `72b955c` |
| 10 | Ruling 24c — the A3 fix's missing consumer | `--edge-mode local`, default `global`; `local_thickness` shared | **HELD** — stroke 1 = 4,344 texels, four outputs byte-identical | `006d3bd` |
| 11 | Ruling 6d — the fifth form is minted | 7 sites renamed; both readers; E16-10's debt repaid | **HELD** — 0 STALE, 0 new UNDECIDED, verify PASSED | `c284693` |

**Predictions scored — 11 committed blind, before any tool was read into.**

| # | outcome | note |
|---|---|---|
| 1 | **HELD** | and the sharper half carried it: the literal fix alone was *not* sufficient — 17 cp1252-fatal cells live in the DB |
| 2 | **HELD** | renormalize staged zero content; the index was already LF |
| 3 | **HELD** | byte-identical, and against the recorded artifact rather than itself |
| 4 | **HELD** | I predicted ≥1 live caller lacked `--profile`; there were two |
| 5 | **HELD** | I predicted I could not vouch for galleon/beast — both moved, and in the *opposite* direction to the one I was watching |
| 6 | **HELD** | captions cannot move a reach number |
| 7 | **HELD** | ±0.5 points predicted, 0.047 measured; ray count up 37×. Wall-time claim overstated — 17 s is cheap |
| 8 | **SPLIT** | direction right (6 of 7 fell); magnitude wrong (1.65× not 2–4×); and I missed the one view that *rose* — the most informative result |
| 9 | **FALSIFIED** | I said the list was complete. It was not — and I had pre-written that the delta would be the finding, so the glob was not trimmed to match |
| 10 | **HELD** | byte-identical at the default |
| 11 | **HELD** | the reader that mattered was the registry, catching flags I added an errand earlier |

**Nine held, one split, one falsified.** The two that did not hold are the two
that taught something, which is the point of predicting before looking.

**Four dispatch corrections, each found by checking the text against source
rather than building on it** — the arc's own standing lesson, paid a fifth time:

1. **E16-4** — the flag is `--aspect`, not `--frame`.
2. **E16-6** — `51.005%` is not an `e08_ceiling` output; it is a different
   camera *set* from a different tool. Two "N6"s, conflated.
3. **E16-7** — the recorded ladder needs `--fit-axis height`; at the tool's
   default the sword's frame gives 15.013%, not the recorded 13.851%.
4. **E16-8** — the probe is *not* report-only; it carries an ANDON, armed at 2.0
   on `character.json`.

---

## 1b. Per-errand detail

### E16-1 — `facet_index.py` verify ASCII repair (Ruling 31f) · ANCHOR HELD

**Finding.** The `↑` on the completeness branch crashes verify under cp1252.

**What the audit found — the dispatch named one fatal literal; there are two.**
An AST pass over every `print()` call (not a text grep — a text grep would have
swept up two things that must not move) found **17 print-literal sites carrying
non-ASCII, of which 2 are cp1252-fatal**:

| line | char | branch |
|---|---|---|
| 1768 | `↑` | completeness — **hot right now** (four arcs print above their bounds) |
| 1848 | `✗` | the FAIL report — cold, and it only runs when something is already wrong |

The second one is the worse of the pair: a verifier whose *failure* report cannot
print is the house's own named class, a check that cannot fail. Measured
before/after on a deliberately broken DB under cp1252 — HEAD dies with
`UnicodeEncodeError`; the repaired tool exits 1 and prints its three findings.

**Two things the AST scope deliberately protected.** `DASH = "[—–-]"`
(`:188`) is a *parser regex* over a record that uses all three dashes, and
`one_line()`'s `…` (`:197`) feeds **18 DB columns** — folding either to ASCII
would have changed what the index parses or what it stores, and the second would
have broken this errand's own DB anchor. Consumers checked before the shared
function was touched, per the standing law.

**The literal fix is not sufficient — the prediction held.** The loud half of
what this tool prints is the *record*, not its own prose. The live DB carries
**17 cp1252-unencodable cells**: `≤` in two ruling locators, `→` in an
experiment status, `⚠` in a handoff outcome, `Δ`/`σ` in indexed prose — and legs
3 and 4 print exactly those columns. A literal-only repair moves the crash one
leg downstream and leaves it cold until a query surfaces a row with an arrow in
it. Folding the *data* to ASCII is the wrong fix (the tool quotes the record;
`≤0.24%` is what the record says), so the repair keeps the console's own
encoding and relaxes only the errors handler
(`reconfigure(errors="backslashreplace")`): under utf-8 nothing is unencodable
and output is byte-for-byte what it was; under cp1252 a `≤` prints as `≤`
instead of taking the process down.

**ANCHOR.**

| leg | before | after |
|---|---|---|
| verify under `PYTHONIOENCODING=utf-8` | PASSED, 19/19 | PASSED, 19/19 |
| verify under default cp1252 | **CRASH** at `:1768` | PASSED, 19/19 |
| verify FAIL path under cp1252 (broken DB) | **CRASH** at `:1768` | exit 1, three readable `X` lines |
| exit code, real DB | 0 | 0 |

**DB byte-identity — held, and the anchor needed restating before it could be
read.** The in-repo DB *did* move (`67ebd457… → 04d76d3…`) and that is not the
tool: it is this report's own predictions file entering `docs/experiments/`.
Proven rather than assumed, two independent like-for-like comparisons with
HEAD's tool run from inside `tools/` so `REPO` resolves the same way:

| comparison | HEAD tool | E16-1 tool |
|---|---|---|
| build to a **fresh** path, current corpus | `bb1d7962…` | `bb1d7962…` |
| build to the **in-repo** path, current corpus | `37ed03b3…` | `37ed03b3…` |

**Byproduct finding — WITHDRAWN, corrected in place during E16-2 with the
measurement that overturned it.** I first read three distinct DB shas for what I
believed was one unchanged corpus (`04d76d3…`, `bb1d7962…`, `37ed03b3…`) and
concluded that a build's bytes depend on whether the target file pre-existed —
fresh path vs in-place overwrite. **That conclusion was wrong**, and the
controlled re-tests are in [E16-2](#e16-2--gitattributes-lf-pin--anchor-held):
fresh, overwrite, overwrite-again and overwrite-a-differently-sized-prior-DB all
return the same sha. The real cause is [§2](#2-a-session-level-finding-the-working-tree-is-shared):
a **concurrent session** is writing into this working tree, and `docs/specs/`
enters the index — so the corpus *was* changing between my readings. The claim
reproduced three times and was still invalid, which is this repo's own law
firing on me: *reproducibility is not validity — check what the operands are.*

What survives the withdrawal, because it was measured directly rather than
inferred: **leg 1 is not exposed to any of this** — it builds two fresh temps
(`.det_a`/`.det_b`) inside one process and carries a pre-registered `.dump`
fallback. I also planted stale temps to simulate a crash between leg 1's build
and its cleanup, expecting a spurious byte-identity failure; **that speculation
was also wrong** — leg 1 still reported BYTE-IDENTICAL and cleaned up.

**Prediction: HELD** (the sharper half — literal-only would be insufficient —
was the load-bearing part, and the 17 fatal DB cells are the evidence).

### E16-2 — `.gitattributes` LF pin · ANCHOR HELD

**Finding.** No `.gitattributes` at all, `core.autocrlf=true`, and a
"LF will be replaced by CRLF" warning on every commit.

**Measured before pinning, because the index parses these files.** The working
tree was *already* LF almost everywhere — 214 of 215 markdown, 148 of 148
python, both scripts, the jsonl, LICENSE. Only **17 text files** carried CRLF
(15 json, `docs/experiments/README.md`, `.gitignore`). So the pin ratifies what
the record already is rather than rewriting it.

**The check that had to come first.** `facet_index` parses this markdown, so a
worktree line-ending change could have moved the DB. Isolated before writing
`.gitattributes` — build to a fresh path, convert the 17 files, build to another
fresh path: **`6b879d3c…` both sides, byte-identical**. The parse is
line-ending insensitive.

**The file.** `* text=auto eol=lf` pins BOTH sides — index and working tree —
with per-type lines for `py/md/json/jsonl/sh/ps1` and `db/png/npy/glb` marked
binary *after* the catch-all, because later rules win. `.ps1` and `.sh` were
already LF in the tree and run that way, so pinning them preserves the status
quo rather than betting on it.

**ANCHOR.**

| check | result |
|---|---|
| `git status` after an identical-bytes touch-and-restore of README.md | **quiet** |
| `git add --renormalize .` content changes staged | **zero** — the index was already LF |
| `git add --renormalize .` vs the concurrent session's untracked files | left alone (only tracked files are renormalized) |
| build after renormalization | 655 artifacts / 483 rulings / 3411 fts, clean |
| verify after renormalization | **PASSED all four legs, 19/19**, leg 1 byte-identity |

**Prediction: HELD** — renormalize staged zero content changes, exactly because
the index side was already LF; the binary marks moved no bytes.

**One thing worth recording beyond the anchor.** Writing CRLF into README.md
still shows ` M ` in `git status`, which looks like the pin failing. It is not:
`git diff --numstat` is empty and the would-be blob (`a2feb044…`) is identical
to the index blob — the ` M ` is stat-dirtiness, cleared the next time git
touches the file. The warning direction has flipped from "LF will be replaced by
CRLF" to "CRLF will be replaced by LF", which is the pin doing its job: the
repo's canonical form is now LF and git normalises toward it.

### E16-3 — `texpass_finalize.py` surface-aware print (Ruling 31d.1) · ANCHOR HELD

**Finding.** In surface-aware mode `grown = valid.copy()` runs *before* the
dilation loop (`:135`), so `valid & ~grown` is empty by construction and `left`
is 0 on every run regardless of the atlas. Three subjects quoted that zero as a
pass; the dragon's celebrated zero was structural, not earned.

**Repair.** The print at `:158` branches. Surface-aware mode still *shows* the
number — a non-zero there would mean the construction had changed and is worth
being startled by — but labels it structural and points at the quantity that is
actually gated (the source-distance distribution, held by the two ANDONs at
`:129`/`:132`). The atlas-flood path keeps its original line verbatim.

**Read-only discipline first.** Ruling 33's ledger was paid for a dispatch that
would have written into a citable-only tree, so before touching the sword's
recorded run I audited every write in the tool: `os.makedirs` + `.save(args.out)`
+ `json.dump(args.json)` and nothing else. Both replays wrote only to scratch;
the E14 tree was read.

**ANCHOR — the recorded run replayed both sides of the change.**

| | `atlas_final.png` sha | vs recorded |
|---|---|---|
| recorded artifact | `a0f51101…` | — |
| replay, tool **before** the change | `a0f51101…` | byte-identical |
| replay, tool **after** the change | `a0f51101…` | byte-identical |

`finalize.json` also byte-identical before vs after. A print cannot move bytes —
asserted, not assumed.

**The branch condition tested by running it, not by reading it.** The risk in an
if/else is inverting it, and only the flood path can catch that. Run without
`--surface-aware` on the same inputs: `done, 0 texels took mean fallback` — the
original wording, intact. The contrast is the repair's whole point: in flood mode
`grown = have.copy()` and the loop can genuinely strand texels, so **that** zero
is earned; in surface-aware mode the same zero cannot be anything else.

**Flagged, not fixed — the JSON carries the same misleading zero.**
`rep["mean_fallback"] = 0` is written to `finalize.json` in surface-aware mode
with no indication that it is structural, and a JSON field is exactly how a
number gets quoted into three subjects' reports. Ruling 31d queued *the print*,
and the batch's named trap is fixing what no ruling queued, so the key is
untouched and byte-identity preserved. Recommend the advisor queue the JSON side.

**Prediction: HELD** (byte-identical, and the replay reproduced the recorded
artifact rather than merely matching itself).

### E16-4 — `texpass_iter emit` profile guard (Ruling 29c) · ANCHOR HELD

**Dispatch correction.** The kickoff says the flag is `--frame`; it is
**`--aspect`**. Dispatch text is hypothesis — the arc has paid for that four
times.

**Finding.** An unprofiled `emit` did not fail; it emitted at `--aspect`'s
default `752,1024`, one subject's portrait framing. The prop's own frame is
**240×1024**, so on this subject the silent default was 3.1× too wide.

**Why it was silent — measured, and it is worse than "no error".** With
`fit-axis height`, `h_ext = v_ext · W/H`, so the horizontal pixel scale is
`W/h_ext = H/v_ext` — *identical to the vertical scale regardless of W*. The
wider frame therefore renders the figure at the same size and just adds
background. Emitted at 240 and at 752 on the same state, the log reports the
**same numbers to the digit**: `49,775 figure px, 5,475 hole px` both times.
Nothing in the emit output distinguishes a right frame from a wrong one.

**Repair, scoped to `emit` only and deliberately so.** `commit` takes W/H from
the emitted `cam.json` (`cam["W"]`/`cam["H"]`, `:307-308`), not from `--aspect`,
so it cannot drift this way; gating it would fire on correct work — the repo's
own rule about putting the andon on the direction the construction leaves open.

**Callers grepped first, and the prediction HELD — two live callers lacked it.**

| caller | before | action |
|---|---|---|
| `tools/texpass_loop.ps1:119` | no `--profile`, no `--aspect` | gained `--aspect 752,1024` |
| `tools/replay_strokes.sh:41` | no `--profile`, no `--aspect` | gained `--aspect 752,1024` |
| `tools/diagnostics/e04_sheet_renders.py:37` | `--profile ship.json` | already safe |
| `tools/diagnostics/e04_replay_owner.py:40` | `--profile ship.json` (and `commit`) | already safe |

Both repaired callers are W3-era and were relying on the default being W3's
frame. The value written is the old default, so **behaviour is unchanged** — it
is now said out loud instead of inherited.

**ANCHOR.**

| check | result |
|---|---|
| profile-bound sword yaw-0 emit, tool **before** the change | `render.png` `mask.png` `hit.png` `cam.json` all **byte-identical** to the recorded `rstate_s8anchor/job_y+000_e+00` |
| profile-bound sword yaw-0 emit, tool **after** the change | all four **byte-identical** to the same recorded job |
| unprofiled `emit` | **exit 1**, the ANDON message, **0 job dirs written** — it refuses before any output |
| explicit `--aspect 752,1024`, no profile | proceeds, emits `W=752` — the legacy path preserved |
| `commit` unprofiled | not gated (fails later on its own missing `--cam`) |
| `selftest` unprofiled | not gated — `PASS`, write-head lossless, 377 texels |
| `bash -n replay_strokes.sh` / PowerShell parse of `texpass_loop.ps1` | both clean |

The citable-only tree was read, never written: the anchor state's three inputs
were copied to scratch and emit ran there.

**Prediction: HELD.**

### E16-5 — `mesh_stats` honest warning condition (Ruling 2d) · ⚠ ANCHOR FAILED — HALTED, NOTHING CHANGED

**The anchor as dispatched cannot be satisfied by the repair as dispatched, and
the two clauses contradict each other on the measured data.** Nothing was
changed. Reported rather than tuned past, per the dispatch's own instruction.

**What the dispatch asked for.** Fire the warning on `rect_frac_of_figure > 1`
(the honest condition) instead of `not up_axis_dominant` (the proxy a
tip-standing prop passes). **ANCHOR:** every VALUE unchanged; *W3/galleon/beast
warning state unchanged*; the sword NOW warns.

**All four subjects measured — the anchor's four outputs.**

| label | faces / verts | components (largest) | `extent_blender` | `up_axis_dominant` | `rect_frac_of_figure` | OLD warning | NEW warning |
|---|---|---|---|---|---|---|---|
| W3 | 287,170f / 141,561v | 38 (0.990) | `[0.4561, 0.3291, 0.9969]` | true | 0.680787 | silent | silent |
| galleon | 939,104f / 465,569v | 512 (0.929) | `[0.969, 0.4969, 0.9312]` | false | 0.327707 | **WARNS** | **silent** |
| beast | 986,814f / 485,291v | 9 (1.000) | `[1.0017, 1.0004, 0.5743]` | false | 0.568773 | **WARNS** | **silent** |
| longsword | 999,474f / 499,609v | 1 (1.000) | `[0.2262, 0.0634, 1.002]` | true | 1.902512 | silent | **WARNS** |

Verbatim, today, before any change: `WARNING galleon: vertical extent is not the
largest ([0.969, 0.4969, 0.9312])` and the same for `beast`. W3 and longsword
print no warning.

**So the swap is not additive — it is a trade.** The sword starts warning
(dispatch expected that) *and galleon and beast stop* (dispatch expected them
unchanged). Ruling 2d named the sword's `rect_frac` of 1.45–1.90 and did not
measure what the honest condition does to the two subjects the proxy currently
catches; it is 0.33 and 0.57, both comfortably under 1.

**Why I did not resolve it myself.** The obvious move —
`not up_axis_dominant or rect_frac > 1` — satisfies every clause of the anchor
exactly. That is what makes it the wrong move: it was chosen *after* seeing which
result each candidate produces, which is retuning however reasonable the
reasoning, and the repo's rule is that the one move always wrong is retuning a
condition after seeing the result it would judge. It also keeps the proxy Ruling
2d called defective, so it is not obviously the repair the ruling asked for.

**What the advisor is ruling between** — stated without a recommendation, since
this is a question about what the instrument is *for*:

1. **Replace** (the literal repair). The sword is caught; galleon and beast go
   silent. Defensible if the warning's job is *"is the face rect measuring
   something other than a face"*, since 0.33 and 0.57 are unremarkable coverages.
2. **Union** (proxy OR honest). Every clause of the anchor passes, but the proxy
   Ruling 2d called a proxy survives, and the choice was made after the fact.
3. **Two separate warnings** with distinct texts — the proxy one saying the
   figure is not upright, the honest one saying the rect exceeds the figure.
   Nothing goes silent and nothing is a proxy for the other, but it is a larger
   change than the ruling queued.

A prior question sits under all three: on a ship and a dragon there **is** no
head, so it is not clear the galleon/beast warnings were ever true positives
rather than the instrument correctly reporting that a character-shaped question
does not apply. That is Ruling 2d's own observation — *the character instrument
did not notice it was not looking at a character* — and it may mean the warning
needs a subject class, not a better threshold.

**Prediction: HELD, and it was the one that mattered.** I predicted I did not
know that galleon and beast would stay silent, and that if either crossed, the
dispatch's expectation was wrong and it was to be reported rather than tuned
around. Both crossed — in the opposite direction to the one I was watching for
(they *stop* warning rather than *start*).

### E16-6 — `e08_ceiling` captions, the overlap line, and the bias warning (Rulings 6e / 10b) · ANCHOR HELD

**Dispatch correction — the anchor's two numbers are not both this tool's.**
The kickoff asks to re-derive "the sword's N6 and N8 — exact against the recorded
51.005% / 51.3342%". `51.3342%` is `e08_ceiling`'s N8 and reproduces exactly.
**`51.0050%` is not an `e08_ceiling` output at all.** The tool's `yaws(n)` is
`[i·360/n]`, so `--sets 6` is the *evenly spaced* six (0/60/120/180/240/300) and
returns **1,871,948 = 51.12%** — which is what handoff 2 recorded and what
reproduces here. The `51.0050%` figure is the **set** 0/45/135/180/225/315 (all
eight minus 90 and 270), computed in handoff 6 by `e14_atlas_anatomy` and a
session reach script, two independent code paths; `e08_ceiling` cannot express an
arbitrary equatorial set. Both "N6"s are real and neither is wrong — the dispatch
conflated them. Anchored on the two numbers this tool actually produces.

**Both 6e defects reproduced before the repair**, exactly as recorded: all three
SETTINGS blocks printed **identical ladders** under captions reading
`head 0.18` / `uniform 0.18` while the run's floors were both 0.45, and
`front-back OVERLAP = 0`.

**Three repairs.**

1. **6e(i) captions** — every caption is now built from the values in hand, and
   identical settings collapse to one block with their names joined, so the
   output can no longer imply three measurements where there is one. With equal
   floors it prints one block plus an explicit NOTE; with unequal floors
   (`0.45`/`0.18`) it prints three, captioned `body 0.45 / head 0.18`,
   `body 0.45 / head 0.45`, `body 0.18 / head 0.18` — all true.
2. **6e(ii) overlap** — repaired rather than deleted, so the structural fact
   stays visible: at any positive floor the overlap is zero by construction
   (opposed cameras test `dot(n,d)` and `dot(n,-d)`, jointly passable only at a
   floor ≤ 0), and the old line's claim that this was "the population a
   hold-one-out comparison at N=2 would have" is replaced by the statement that
   **no such population exists on this route**.
3. **10b bias warning** — fires when `--bias` exceeds the route's ~0.00196 wall
   floor, naming the +0.97-point overstatement at N8 and stating that the value
   is deliberately unchanged for comparability. Silent at `--bias 5e-4`.

**The repair broke a consumer, and finding it is the point.**
`e14_atlas_anatomy.py:194` read `cj["settings"]["uniform 0.45"]` — a hardcoded
caption. Honest captions move, so that lookup would have failed on every new
ceiling JSON. It is **the same defect one tool over**: the caption was a *proxy*
for "the configuration whose floors are both 0.45", and the floors **are** the
configuration. `e08_ceiling` now emits a `settings_index` carrying each block's
label, floors and aliases, and the consumer selects on the floors it ran.

**ANCHOR.**

| check | result |
|---|---|
| all 19 scalar / ladder / marginal values, before vs after | **identical, zero mismatches** |
| N8 | 1,879,807 = 51.33% — exact against the recorded **51.3342%** |
| N6 (this tool's evenly-spaced six) | 1,871,948 = 51.12% — exact against handoff 2 |
| consumer, new ceiling JSON | `EXTERNAL CHECK: reproduces e08_ceiling's N8 total exactly (1,879,807)` |
| consumer, **pre-repair** ceiling JSON | same — backward-compatible caption fallback |
| consumer, floors-mismatched ceiling JSON | **ANDON refuses** — previously this class could cross-check against the wrong configuration silently |
| unequal-floors branch | three blocks, all captions true, no collapse NOTE |
| `--bias 5e-4` | no warning |

**Prediction: HELD** — captions and a warning cannot move a reach number, and
both of 6e's claims were re-measured rather than inherited.

### E16-7 — `e12_elevated` ray-grid floor (Ruling 10a) · ANCHOR HELD, and it found two more things

**Finding.** The tool took its ray grid from `--aspect`, i.e. from a *generation*
frame, which knows the subject's silhouette and nothing about its tessellation.
On the sword's 240-px frame the grid ran 3.71× coarser than the mean face and
up-facing reach came back **13.851%** against a converged **53.920%** — wrong by
3.9×, because faces below a ray cell are hit only by luck and this subject's
up-facing faces are exactly the small horizontal steps.

**Reproducing the record needed a correction first.** The recorded ladder is not
reproducible from the invocation as quoted in handoff 2 — at the tool's default
`--fit-axis width` the sword's 240×1024 frame gives ratio 3.440× and **15.013%**.
The recorded run used **`--fit-axis height`** (the prop's pinned framing value),
which gives ratio 3.708× and **13.851%** exactly. The before-anchor is only valid
once that is right.

**Repair.** `--aspect` keeps its meaning as the frame's *shape*; what it stops
deciding is the *resolution*. The extent along the fit axis is independent of the
pixel counts, and the cell is square in both modes, so the grid is solved
directly for `--rays-per-face` (default **10**, the density of the recorded
converged run at 9.71). The ratio and rays-per-mean-face are printed on every
run, derived or not, and `--exact-grid` restores the literal reading so recorded
runs stay reproducible.

**ANCHOR — reproduce the converged 53.92% at the repaired default.**

| run | frame | ratio | rays/face | eye-level eight reach |
|---|---|---|---|---|
| recorded coarse, via `--exact-grid` | 240×1024 | 3.708× | 0.27 | **13.851%** — exact |
| **repaired default** | 1462×6236 | 0.100× | 10.00 | **53.967%** |
| recorded converged | 1440×6144 | 0.10× | 9.71 | 53.920% |

**+0.047 points against the record** — inside ray-sampling noise, and the
round-1 winner's cumulative reproduces to 55.635% against 55.639%. Cost: 37× the
rays, **6.8× the wall time — 2.5 s → 17 s**, not a burden.

**Finding 1 — 53.920% is not converged, and the record's "converged" label is
not supported by its own ladder.** Laddering past the anchor:

| rays/face | 0.27 | 4.32 | 9.71 | **10.00** | 20.00 | 40.00 |
|---|---|---|---|---|---|---|
| reach | 13.851% | 51.526% | 53.920% | **53.967%** | 54.600% | 54.849% |

Still climbing at 40 rays/face. The floor at ratio ≤ 1 buys "not wrong by 3.9×",
not convergence — so the tool now prints that distinction rather than letting the
next session read 10 rays/face as converged, which is the error the record made.

**Finding 2 — the greedy winner is noise-dominated, and it flips.** At 10
rays/face round 1 picks `0/180 @ 40`; at 20 and 40 it picks `90/270 @ 55`. The
candidates are tied far inside the density drift — at 40 rays/face the four
elevated pairs land at 55.650 / 55.632 / 55.637 / **55.651**, so the winner beats
the runner-up by **0.001 points** while density alone moves the field by 0.6.
The tool reports a WINNER from a field it cannot separate. Nothing was changed
for this: the greedy selection is the ship's own method and is cited in closed
rulings. **Reported for the advisor** — on this subject the honest output is
"four candidates tied at ~55.65%, pick on other grounds", and the E06 superset
check inherits the instability (the flagged pair changes with the winner).

**Prediction: HELD on both halves** — within ±0.5 points (0.047), and the ray
count rose an order of magnitude (37×). The wall-time half was directionally
right but overstated: 17 s absolute is cheap.

### E16-8 — the background probe's corner-median reference (Ruling 21e) · ANCHOR HELD

**Dispatch correction — the probe is not report-only.** The kickoff says "the
probe is REPORT-ONLY"; `project_twins.py:835` carries an `assert p_rx <=
args.bg_max_pct` ANDON. It does not fire on this subject because `prop.json`
pins `bg-max-pct` to **100.0**, but that is a profile value, not a property of
the probe. Blast radius measured across all four profiles:

| profile | `bg-max-pct` | probe ANDON |
|---|---|---|
| prop / beast / ship | 100.0 | disarmed |
| **character** | **2.0** | **armed** |

**Repair.** The reference was a corner median of two 8×8 patches — the keying
method this repo has retired three times, found here as its **last live
consumer**. It is now the route's own fitted border-ring surface, **sampled at
each texel's own pixel**, so a texel is compared against the backdrop where it
sits rather than against a corner it is nowhere near. The fit is factored out of
`figure_mask` into `fit_background()` so there is **one** implementation of the
model rather than two that can drift; it returns float64 deliberately, which
keeps `figure_mask`'s channel-wise subtraction into a float32 residual
bit-identical to the pre-factoring code.

**ANCHOR — the projection must not move.** Same seven views, same profile, run
through HEAD's tool and the repaired tool:

| output | result |
|---|---|
| `atlas.png` · `atlas_blend.png` · `atlas_holes.png` · `atlas_owner.npy` · `atlas_styled_mask.npy` | **all five BYTE-IDENTICAL** |
| every non-probe log line | identical (only the output path differs) |

The before-run also reproduces the recorded `projection.log` exactly at y+000.0 —
3,757 texels, median dE 23.9, 15.41% — so the baseline is the record, not just
itself.

**Old vs new probe percentages, the sword's seven twins.**

| view | admitted | old ref rgb | old dE | old %<10 | new ref rgb | new dE | new %<10 |
|---|---|---|---|---|---|---|---|
| y+000 | 3,757 | (168,149,205) | 23.9 | 15.41% | (166,146,204) | 24.2 | 14.64% |
| y+045 | 6,263 | (110,93,149) | 14.3 | 30.30% | (134,112,176) | 19.6 | **18.31%** |
| y+135 | 6,360 | (111,94,151) | 9.9 | 50.68% | (137,115,180) | 16.2 | **31.64%** |
| y+180 | 5,033 | (167,148,207) | 22.0 | 13.83% | (165,144,205) | 22.4 | 13.59% |
| y+225 | 8,188 | (110,92,146) | 14.7 | 26.06% | (138,116,180) | 21.2 | **17.28%** |
| **y+270** | 15,905 | **(86,72,114)** | 20.5 | **6.23%** | (144,124,185) | 17.0 | **19.87% ↑** |
| y+315 | 13,391 | (110,94,150) | 8.7 | 60.15% | (136,115,179) | 9.0 | 54.31% |

**The finding is y+270, and it goes the wrong way on purpose.** Six views fall;
this one **rises 3.2×**. Its old corner reference was `(86,72,114)` — far darker
than every other view's ~110, because the corners there are vignetted — so
texels looked comfortably far from "background" and the view scored **6.23%, the
safest of the seven**. Against the backdrop actually behind them it is 19.87%,
mid-pack. **The retired method was not merely noisy; it under-reported risk
worst on the highest-risk view** — yaw 270 is the edge-on blade, the ribbon the
whole stroke lane existed for. A probe that reads safest exactly where the danger
is concentrated is the failure mode that matters.

**Prediction: SPLIT.** Direction HELD — the percentage falls on most twins (6 of
7). Magnitude **FALSIFIED** — I predicted a 2–4× fall; the largest is 1.65×
(30.30→18.31). And I did not anticipate a view moving **up** at all, which turned
out to be the most informative result in the errand.

**Flagged for the advisor, not ruled:** on the sword every view sits at 6–60%
before and after, i.e. 3–30× over `character.json`'s armed bound of 2.0. Either
W3's twins behave very differently or that bound is effectively vestigial — and
the reference change moves the quantity it gates. W3's prep tree has no
`meta.json` on this rig, so it was not measurable here.

### E16-9 — kickoff-glob discovery for `HANDOFF_FILES` · ANCHOR HELD, and the glob found what the list was missing

**The defect was live, and the old comment said so.** `HANDOFF_FILES` carried
three entries and its own comment read *"until it lands, every new arc's kickoff
is added HERE."* Nobody added E15's. **`E15-context-index-kickoff.md` carries two
`## Session handoff` headers**, so those two dispatches were invisible to the
handoffs table *and* to `verify`'s count legs — E15 Ruling 8b's class exactly,
one list over: a gate that can test whether a listed file lost a row but not
whether a file was missing from the list.

**Repair.** A sorted glob (`^E\d\d-.*kickoff.*\.md$`) with the arc taken from the
leading E-number — *not* by stripping from the keyword as `ruling_documents` does,
because that would yield `E04-executor` and `E15-context-index` and break every
existing anchor. It reproduces the hardcoded list's three labels exactly. The
collision the ruling docs suffer is possible here in principle and does not exist
today; it is stated in the docstring rather than silently assumed away.

**The inverse guard.** `assert_no_undiscovered_handoffs()` asks the opposite
question — *does any file in the record carry a handoff header the glob did not
reach* — which is the check the old list could not express at all. It runs on
every build.

**ANCHOR.**

| check | result |
|---|---|
| **claims sweep, before vs after** | **BYTE-IDENTICAL**, 94 lines both — the dispatch's anchor as literally worded |
| handoffs table | 29 → **31 rows**; the two new are `E15` handoffs 2 and 3 |
| per-arc counts | E04 5 · E12 15 · E14 9 unchanged; **E15 2 (new)** |
| discovered list printed in `verify` | 6 documents, with row counts and the pattern |
| E08 / E16 kickoffs (0 handoff headers) | discovered, 0 rows, prose only — harmless, same as the topical ruling files |
| guard on the real discovery set | **PASS** — nothing outside the glob carries a header |
| guard on a synthetic miss (E15 dropped from the discovered set) | **FIRES**, naming the file and the offending line |
| `verify` | **PASSED all four legs** |

The synthetic miss was injected by handing the guard a **truncated discovery
list** rather than by writing a decoy `.md` into `docs/experiments/`. That is the
same failure condition — a glob that does not reach a file that has headers — and
it keeps a stray document out of a working tree a second session is building
from ([§2](#2-a-session-level-finding-the-working-tree-is-shared)).

**Prediction: FALSIFIED, in the way I said would be the finding.** I predicted
the hardcoded list was complete because "the sessions that added handoffs
maintained it". They did not — E15's kickoff was omitted. I also wrote that if
the glob discovered an omitted file, *"rows change and the dispatch's anchor
expectation is wrong; that is the finding, and I report the delta rather than
trimming the glob to match."* That is what happened, and the glob was not
trimmed.

**Ledger, mine.** I reached for `git stash push <path>` to isolate the
before-comparison. This git rejected the subcommand form, so no stash was
created — and the paired `git stash pop` then applied the **pre-existing
session-start stash**, leaving a conflict in `docs/advisor-kickoff.md`, a file
belonging to the other session. Restored from HEAD, zero conflict markers, the
original stash intact and untouched. The comparison was redone the way the rest
of this batch does it — HEAD's tool copied into `tools/` and run directly — which
never touches git state. **In a shared working tree, do not use the stash.**

### E16-10 — the edge-dist A3 port, as an OPT-IN FLAG (Ruling 24c) · ANCHOR HELD

**Repair.** `--edge-mode local` bounds the peel by the structure's own half-width,
`min(--edge-dist, --edge-frac × local half-width)`. **`global` remains the
default and is byte-identical**; the mode is adopted nowhere and the next
subject's stroke-lane ruling opts in with its own evidence or does not.

**One implementation, not two.** The port needs `local_thickness`, which lived in
`project_twins`. `texpass_iter` cannot import that module (it parses argv at
import), so the choice was a second copy or an extraction. E16-8's own commit
message argues against the copy, so the function moved verbatim to
`tools/mask_geometry.py` and both tools import it. **The projector was re-run
across the extraction: all five outputs byte-identical.**

**ANCHOR — the default must not move.**

| check | result |
|---|---|
| recorded stroke 1, current tool, before any edit | `wrote 4,344 texels; holes 2,005,056 -> 2,000,712` — reproduces `s1b/commit.log` exactly |
| `--edge-mode global` (default) after the change | **4,344 texels**, and `atlas.png` / `holes.png` / `styled_mask.npy` / `atlas.prev.png` all **BYTE-IDENTICAL** |
| default re-checked again after every later edit | still 4,344, still byte-identical |
| `project_twins` across the `local_thickness` extraction | all five outputs **BYTE-IDENTICAL** |

**A real defect in my own first cut, caught by reading the number.** The first
version committed **38,041** texels against 4,344 with a printed median threshold
of **0.00 px**. A candidate outside the trust mask has `d_s = 0` *and*
`thick_s = 0`, so `d_s >= thr` reads `0 >= 0` and admits it — the global branch
excludes those only as a side effect of its constant being positive, so the local
branch has to say so. Mask membership is now required explicitly. The 8.8×
admission was not a result; it was the port being wrong, and the tell was a
median threshold that could not be right.

**The local mode's delta, REPORTED and adopted nowhere.** Stroke 1, yaw 0:
**4,344 → 5,675 texels, +1,331 (+30.6%)**. Per structure — 7,754 of 43,987
candidates lie inside the trust mask:

| local half-width | candidates | global admits | local admits | delta |
|---|---|---|---|---|
| 1–2 px | 89 | **0** | 84 | **+84** |
| 2–4 px | 159 | **0** | 158 | **+158** |
| 4–8 px | 1,890 | 402 | 1,286 | **+884** |
| 8–16 px | 2,920 | 1,681 | 1,877 | +196 |
| 16–32 px | 2,687 | 2,261 | 2,261 | **+0** |

That is the global-constant law's signature, measured rather than argued: the
fixed 4 px peel admits **nothing at all** from the two thinnest strata and costs
**exactly nothing** at 16–32 px. The cost of a fixed peel runs inversely with
local feature width, and the median threshold inside the mask is still 4.00 px —
the global constant binds wherever a structure is at least 12 px half-wide, so
the mode is a relaxation only where the structure is genuinely thin.

**Prediction: HELD** — byte-identical at the default.

### E16-11 — the `_per_invocation` migration (E12 Ruling 6d) · ANCHOR HELD

**A blanket rename would have been wrong, and enumerating first is what showed
it.** `_not_on_route` appears in three structurally different places, and only one
of them is Ruling 6d's fifth form:

| node | meaning | action |
|---|---|---|
| `/tools/<tool>/_not_on_route` (7 sites) | a key the profile supplies no value for | **renamed** to `_per_invocation` |
| `/_tools_not_on_route` (beast, prop, ship) | whole tools off the route | untouched |
| **`/_not_on_route` at ship's top level** | whole tools off the route, under the *key-level* name | **untouched** |

The seven renamed sites are exactly Ruling 6d's: `brush_cloud_step` `lane` on all
four profiles, `texpass_iter` `yaw`/`el` on beast, prop and ship (character has no
such block). All four files still parse.

**Byproduct finding, reported not fixed:** `ship.json` declares the *same three
tools* twice — once at top level as `_not_on_route` and again as
`_tools_not_on_route`. Only the latter is a documented top-level form and only
the latter is what the sweep reads (`prof.get("_tools_not_on_route")`), so the
first is inert. No ruling queued it, so it stands.

**Readers updated in the same commit.** `e04_registry_sweep` recognises
`_per_invocation` as a distinct `how`, *added* beside `_not_on_route` rather than
replacing it — the older form stays correct for a key genuinely not exercised on
a route, and the registry should be able to tell "never runs" from "runs every
time, supplied by the job". `e04_profile_check` merges the two for its own
narrower question. Both docstrings updated.

**Debt repaid: E16-10 had put two flags into the registry undeclared.** Adding
`--edge-mode` and `--edge-frac` made them UNDECIDED on **all four** profiles —
E16-10's own doing, caught by this errand's anchor. Both are now declared:
`edge-mode: "global"` (Ruling 24c adopted `local` nowhere; without the entry a
*mode* would arrive by silence) and `edge-frac: 1/3` (inert unless the mode is
adopted). **Flagged for the advisor:** on `project_twins` this same flag is
classified CODE in the classification table's section 6 — *"a derived law, not a
tuned number"* — and the identical reasoning applies to this tool's copy, but
moving it there is a table edit an executor should not make.

**ANCHOR.**

| check | before | after |
|---|---|---|
| beast sweep | exit 1, 2 UNDECIDED | **exit 0**, 85/85 decided, `_per_invocation 3` |
| ship sweep | exit 1, 2 UNDECIDED | **exit 0**, 85/85 decided, `_per_invocation 3` |
| prop sweep | exit 1, 3 UNDECIDED | exit 1, **1** UNDECIDED (pre-existing `texpass_brush prompt`) |
| character sweep | exit 1, 20 UNDECIDED | exit 1, **18** UNDECIDED (all pre-existing), `_per_invocation 1` |
| undecided rows, diffed line by line | — | **the only rows that changed are `edge-mode` and `edge-frac`** — 0 new, 2 repaid per profile |
| claims sweep | — | **STALE: 0** |
| build | — | 660 artifacts · 483 rulings · 31 handoffs · 225 decisions |
| verify | — | **PASSED all four legs, 19/19** |
| E16-10 stroke anchor, re-run because the profiles changed | 4,344 | **4,344**, three outputs byte-identical |
| E16-4 emit anchor, re-run for the same reason | — | all four outputs **byte-identical** (9 profile values applied now, was 7) |

**Prediction: HELD** — build and verify pass, 0 STALE, 0 new UNDECIDED. The risk I
named was "a missed reader, not a wrong value"; the reader that turned out to
matter was the registry itself, catching two flags I had added an errand earlier.

---

## 2. A session-level finding: the working tree is shared

**This repo currently has a second session writing into it** — the MCP
spec-session opened by the same `cff21e9` dispatch. Its files appeared under
`docs/specs/` while this batch was running (`comfy-preflight-spec.md` was not
there at my first `git status` and was at my second), and **`docs/specs/` enters
the index** (1 `artifacts` row, 1 `fts` row measured). It also rebuilds
`docs/index/facet.db`, which is a tracked file we both write.

That is what produced the three unreconcilable DB shas in E16-1, and it cost a
withdrawn finding. Three working rules adopted for the rest of the batch, and
recommended to the advisor as standing practice whenever two windows share a
tree:

1. **No in-repo DB sha is an anchor.** Every DB comparison in this batch builds
   to fresh scratch paths, which is what made the E16-1 tool-neutrality result
   trustworthy while the in-repo readings were not.
2. **Never `git add -A` / `git add .`** — explicit paths only, so the other
   session's work is never swept into an errand commit. (`--renormalize .` was
   checked against this specifically and only touches tracked files.)
3. **`docs/index/facet.db` stays out of errand commits** and is rebuilt once at
   the end of the batch, since both sessions regenerate it.

Verified before it was asserted: `build --db <other-path>` does **not** write
the default DB — the tool respects its declared target, so the drift is the
other session, not a silent write. The other session is also **committing to
`main`**: `E14 Ruling 34` (the ingest landed) and `E14 Ruling 35` (the polish
arc chartered) interleaved between my errand commits while this batch ran.

**The advisor reached the same class from the other side, independently.**
Ruling 35 records: *"concurrent verifies in one working copy race on
`facet.db.det_a` — observed live this fold when my verify collided with E16-1's
own; retried clean, flagged for the errand lane."* Leg 1's temp paths are fixed
(`db_path + ".det_a"` / `".det_b"`, `facet_index.py:1681–1682`), so two verifies
in one working copy write the same two files and can read each other's bytes.
That is a live defect in the determinism leg under concurrency, and it is a
second plausible contributor to E16-1's unreconcilable shas alongside the moving
corpus.

**Not taken into this batch, and flagged for the advisor's ruling.** It was
queued by a ruling that landed *after* this dispatch was written, and the
dispatch's named trap is fixing something no ruling queued. The eleven run as
dispatched; this is reported as a twelfth with a diagnosis ready — the repair is
per-process-unique temp paths, and its anchor is two concurrent verifies both
returning byte-identity.

---

## 3. What the advisor is left to rule on

Nothing here was decided by this session.

1. **E16-5, the halt.** Three candidate conditions for `mesh_stats`' warning,
   with the measurement that separates them, and the prior question of whether a
   character-shaped warning should carry a subject class at all.
2. **The twelfth errand** — leg 1's fixed temp paths racing under concurrency
   (Ruling 35 flagged it to this lane after the dispatch was written).
3. **`texpass_iter.edge-frac` classification** — declared as a profile value in
   E16-11; on `project_twins` the same flag is CODE in the classification table's
   section 6. Moving it is a table edit an executor should not make.
4. **`finalize.json`'s `mean_fallback: 0`** — the print was repaired in E16-3;
   the JSON field still carries the structural zero unlabelled, and a JSON field
   is how a number gets quoted into three subjects' reports.
5. **`e12_elevated`'s greedy winner** — the four elevated candidates are tied to
   within 0.001 points while ray density alone moves the field by 0.6, and the
   winner flips with density. The tool reports a WINNER from a field it cannot
   separate; nothing was changed, because the greedy method is cited in closed
   rulings.
6. **`53.920%` is not converged** — it rises to 54.849% at 40 rays/face. The
   record's "converged" label is not supported by its own ladder.
7. **`character.json`'s `bg-max-pct 2.0`** — the only profile arming the
   background probe, and E16-8 moved the quantity it gates. On the sword every
   view reads 6–60% both before and after, 3–30× over that bound. W3's prep tree
   has no `meta.json` on this rig, so it was not measurable here.
8. **`ship.json`'s duplicate off-route declaration** — the same three tools
   listed twice, once under a name the sweep does not read at top level.
