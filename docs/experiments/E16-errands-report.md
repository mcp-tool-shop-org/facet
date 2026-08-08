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
