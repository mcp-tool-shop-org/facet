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

*(filled in as each errand lands — one errand, one commit, one anchor)*

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
