# E30 — the polish arc's entry gates: per-profile anchors for W3, the galleon and the dragon

**Written by the advisor, 2026-08-09, at the Director's word releasing the polish arc:**
*"We'll keep working on the measurement tools before we publish, but there's no need to
wait on the polish."* Halts at `E30-polish-anchor-gates-report.md`; the advisor rules at
`E30-ruling.md`.

**This runs alongside a live E28 task-3 seat.** The coordination section is not boilerplate
— read it before your first command.

---

## The question

[E14 Ruling 35](E14-ruling.md) is the Director's own binding clause: **every polish lane
OPENS with a per-profile anchor gate** — the subject's recorded artifacts replayed
byte-identical against its citable tree BEFORE any polish work, each replay landing as a
**permanent per-subject artifacts-tier test in the same commit**. His words for why:

> *"We're going to basically have to verify everything when we get to the polish pass, one
> profile at a time. It's going to be painful and expensive, but this is what happens when
> something like this is neglected."*

**The sword already has its gates** — T7–T12: finalize replay, ceiling, elevated,
projection, edge mode, mesh_stats. **W3, the galleon and the dragon owe theirs.** This arc
pays that tax, once, and leaves coverage behind.

**No polish work happens in this arc.** Not one pixel of any accepted asset changes. The
deliverable is the gates that let polish begin.

## What an anchor gate is, exactly — read T7 before writing anything

`tests/test_t07_finalize_replay.py`'s docstring is the specification and it is short. The
properties that make it an anchor rather than a smoke test:

1. **The anchor is the recorded artifact's OWN BYTES.** The replay's output is compared
   file-to-file. **No sha256 literal appears in test code** — a literal is a number someone
   typed, and it can be typed to match.
2. **The recorded tree is read-only, in place.** The tool reads `--state` and writes only to
   `--out` / `--json`, which the test points at a temp path. Every write was audited before
   the recorded run was touched.
3. **The test re-hashes its inputs afterward to prove the citable tree did not move.** That
   leg is not optional and it is why this arc can run beside a manifest-gated seat.
4. `@pytest.mark.artifacts` + `@pytest.mark.slow`, so CI deselects it by design — these need
   trees that are not in git.

**Build each new anchor to that shape.** Where a subject's stage cannot meet it, that is a
finding, not a licence to lower the bar.

## The work

For **each of the three subjects** — W3 (`facet_E08/ARMB`), the galleon
(`facet_next/E04_stroke`), the dragon (`facet_next/E13_stroke`) — verify the tree path
before using it rather than inheriting it from this sentence:

1. **Enumerate what is replayable.** Which recorded stages have a recorded invocation with
   recorded parameters and a recorded output? The sword has six. **Do not assume the other
   three have six**, and do not pad to six.
   ⚠ **E27 Ruling 5's law applies directly here**: a real population whose members were
   never checked for the property still breaks the prediction. Before predicting how many
   anchors a subject yields, check that "has a replayable recorded invocation" is even
   *defined* for each of its stages.
2. **Build the anchors**, one test per replay, to T7's shape.
3. **Report what cannot be anchored and why** — per subject, per stage. A subject that
   yields two honest anchors is a better result than one padded to six.

## ⛔ A FAILING ANCHOR IS A FINDING. HALT — DO NOT REPAIR.

**This is the most important instruction in this dispatch.** These trees are the four
accepted assets. If a replay does not reproduce:

- **Do not adjust the tool. Do not adjust the anchor. Do not re-run with a changed
  parameter.** A session that changed a parameter and re-ran when a gate fired hit the same
  gate harder.
- **Halt, and report it with its evidence**: what was replayed, from what recorded
  parameters, what came back, and the shape of the difference — not only its magnitude.
- The precedent is [E16-5](E16-ruling.md), whose anchor **failed honestly** and was ruled at
  the honest condition rather than tuned into passing. That is the outcome to aim for if the
  measurement points there.
- ⚠ **And check the comparison before believing a failure**: *file bytes are not pixel
  values*. A PNG hash mismatch on a pixel-identical render has produced **two false halts**
  in this repo. `tools/verify/anchor_compare.py` now exists precisely for this and reports
  both tiers plus the residual's shape — **use it** rather than a bare hash, and say in the
  report which tier decided.

## Predictions — committed BEFORE the first replay

Write `E30-predictions.md` and commit it before any anchor runs. Point estimate, band, and
a blind/not-blind disclosure per row.

- **P1** — total anchors buildable across the three subjects.
- **P2** — per subject: W3 / galleon / dragon. State the unit: one *anchor* = one replayable
  recorded stage meeting all four of T7's properties.
- **P3** — how many replays reproduce byte-identically on the first run.
- **P4** — how many stages are **not** anchorable, and the dominant reason.
- **P5** — behavioural: will any anchor need the pixel tier rather than the byte tier to
  render a correct verdict? Name what would make that true before you look.

⚠ **Six consecutive arcs have missed on a unit or a population rather than on the work.**
Name the unit and the denominator before each number. **No calibration haircut** — E22's
P18 halved an untutored estimate on this repo's own lesson and measured 175 against 4.

## Gates

1. **The tree manifest is taken BEFORE the first replay and re-checked at the close** —
   7,312 files, **0 added / 0 removed / 0 changed**. E23's instrument covers it in ~50 s.
   ⚠ A live sibling seat gates on this same number; a stray write breaks their arc as well
   as yours.
2. **Every replay writes to a scratch path.** Never into a recorded tree. Scripts create
   their own output directories.
3. **No sha256 literal in test code.** Compare artifact bytes to artifact bytes.
4. **Every anchor carries the input re-hash leg** (T7's third property).
5. **A failing anchor halts the arc** — see above.
6. `git diff --name-status -- tools/` must be **EMPTY**. This arc writes tests and docs
   only. If you believe a tool must change, that is a finding for the ruling.
7. **CI green**, run id resolved before it is written; `NOT YET RUN` until it is.

## ⚠ COORDINATION — a live E28 task-3 seat shares this working copy

Measured separation, not assumed: **task 3 owns `tools/diagnostics/texel_provenance.py`,
`tools/measure_mcp.py`, `tools/instrument_census.py` and tests T47–T49. This arc writes no
tool code at all** (gate 6), which makes the tool surface disjoint by construction.

- **T-numbers are allocated by the advisor to prevent a collision: E30 takes T50+.**
  T46 is taken; T47–T49 are task 3's. Do not take a number below T50.
- **`docs/experiments/README.md` is the ADVISOR's** this arc — the row is folded at the
  ruling. Do not touch it; a status table edited by two live seats is how E26's drift
  happened.
- **File-scoped `git add`, always** — and diff each file before staging it. *File-scoped
  `add` bounds which files you commit, not whose work is in them* (E28 Ruling 16, the
  advisor's own miss this session).
- `git fetch && git merge --ff-only origin/main`, **not** `pull --rebase`. ⚠ That guard
  watches the REMOTE and cannot see a sibling's local commit — **re-measure any quantity you
  assert against the tree you are about to commit.**
- `cancel-in-progress: true` means a parallel push cancels your CI run; gate 7 is satisfied
  by the first *completed* run whose tree contains your commit, and the report names what
  else was in it.
- **Do not touch `docs/index/facet.db` or its certificate.** The advisor folds the pair.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every anchor pins a recorded invocation to a recorded output, byte-for-byte, under the absolute pinned interpreter; the whole deliverable *is* pinning |
| ANDON_AUTHORITY | 3 | gate 5 halts the arc on a failing anchor with an explicit no-repair clause; gates 1–4 and 6 are hard; every ANDON written here `raise`s |
| NAMED_COMPENSATORS | 3 | the arc writes **tests and docs only** — `git revert` restores everything. The one real hazard is the recorded trees, and it is addressed by construction: read-only in place, scratch outputs, manifest before and after, halt on any delta |
| DECOMPOSE_BY_SECRETS | 3 | one anchor per subject per stage — subject-specific facts stay in the subject's own test, and nothing is shared across the three lanes |
| UNCERTAINTY_GATED_HUMANS | 3 | a failing anchor is routed to the Director's judgment rather than repaired; "what cannot be anchored and why" is a reported finding, not a gap to fill silently |
| EXTERNAL_VERIFIER | 3 | the anchor pattern **is** the external verifier — the recorded artifact's own bytes, produced before this session existed, with no literal in test code for anyone to fit to |

## Out of scope

- **Any polish work.** No accepted asset changes. This arc builds the gates only.
- **The sword** — T7–T12 exist; re-deriving them is not this arc's work.
- **Any tool change** (gate 6). A needed change is a finding.
- **`tools/` at all**, the index DB and certificate, `docs/experiments/README.md`.
- **E28 task 3** — a sibling seat owns it. A defect found in its files is reported, not fixed.
- **The publish** — deferred at the Director's word until the measurement tools settle.

## Environment

```
python    E:\AI-Models\trellis2-env\Scripts\python.exe      <- ABSOLUTE, always
blender   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"   -b -P only
trees     E:\AI\training\facet_E08\ARMB\  ·  ...\facet_next\E04_stroke\  ·  ...\E13_stroke\
```

- **Bare `python` lacks `open3d` and `mcp`.** T18 refuses the wrong interpreter in one line.
- **Blender runs through PowerShell**, always `-b -P`. Git Bash mangles the paths.
- The **VRAM watchdog is alive** (restarted 2026-08-09, heartbeat verified advancing).
  Generation is cloud-only and **this arc generates nothing** — replays are local.
- **The recorded trees are not in git and have no revert.** Manifest first, always.
- **ASCII prints.** `argparse` eats leading minus signs — use `--views=-30,0,30`.

## Halt

Report at `E30-polish-anchor-gates-report.md`.

- **State predictions before you look**, and disclose whether each was blind.
- **Never judge whether output is good.** Produce measurements. *Verified, shipped, works,
  decisive, validated, proven* do not belong in the report or a commit message.
- **A negative result is a full success.** If a subject yields one anchor, say so plainly.
  If an anchor fails, that is the arc's most valuable output — halt and report it.
- **Do not write to the memory store.** The advisor folds findings into the repo.
