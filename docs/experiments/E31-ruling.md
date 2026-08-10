# E31 ruling — what does it cost to put the pipeline in the package?

**Advisor, 2026-08-09.** Report:
[E31-publish-the-pipeline-report.md](E31-publish-the-pipeline-report.md). Predictions at
`8e21cea`, committed before the first wheel. Code + tests `943d2d5`; report `e45b3d3`.
Dispatch: [E31-publish-the-pipeline-kickoff.md](E31-publish-the-pipeline-kickoff.md).

**Re-measured at this seat before ruling:** the suite counts (859/819, confirming the report
and falsifying `943d2d5`'s message), open3d's PyPI support matrix **and the provenance of the
build actually installed on this rig**, and `anchor_compare.py`'s PIL handling read at source.

---

## Ruling 1 — THE ARC IS ACCEPTED, and it is the first time anyone measured what an installed facet can do

Six tiers, each an **actual wheel** built in scratch and installed into **its own clean venv**,
with all eight tools called through the server's own dispatch. Not `--help`. The dispatch asked
for one failing test and got a measured ladder:

| tier | failing of 8 | layer |
|---|---:|---|
| T0 — today's wheel | **8** | **0 — the module is not in the artifact** |
| T1 — + the module | **8** | 1 — `REPO = <venv>\Lib` |
| T2b — + instruments + path + `subject_profile` | **7** | 3 |
| LIGHT — + numpy/scipy/trimesh/pillow (277.9 MB) | **4** | — |
| FULL — + open3d (634.6 MB, py3.12) | **0** | — |

**The wheel can carry the server.** Cost: 58 KB / 2 entries → **506 KB / 114**, two generic
top-level import names, 100 files under `diagnostics` of which **5 are served**, and open3d's
~230 MB transitive tree (dash, flask, werkzeug, ipywidgets, nbformat) entering CI's
`pip-audit` population as hard requirements.

## Ruling 2 — ⚑ THE DISPATCH'S THREE-LAYER MODEL WAS INCOMPLETE, and that is the advisor's miss

I specified the failure layers as **resolver / missing instrument file / missing import** and
asked which one each tool hit. The report found **a layer 0 in front of all three: the server
module is not in the artifact at all.** `py-modules` lists two entries and `measure_mcp` is not
one of them, so at T0 the question "where does it fail" has no operand — there is nothing to
fail.

That is the same family this repo has now missed on nine consecutive arcs, arriving in a
**dispatch** rather than a prediction: **I enumerated a population of failure modes and left
out the first member.** The lesson generalises past this arc — *when you enumerate the ways a
thing can break, check that the thing is present before you enumerate how it misbehaves.*

## Ruling 3 — ⛔ open3d: THE FINDING STANDS, AND IT IS WORSE THAN THE REPORT STATES

**Verified at this seat.** open3d **0.19.0 is the latest release**, publishes wheels for
**cp38–cp312 only**, and **has no sdist at all** (`packagetype: sdist` absent). The rig runs
**Python 3.13.13**. `pyproject.toml` declares `requires-python = ">=3.11"`. The report's
`from versions: none` is accurate.

**And the part nobody had looked at.** This rig *has* open3d — 207 MB of it — which cannot be
true of PyPI on 3.13. Measured: the installed distribution is **`0.19.0+241aaee`**, whose
`direct_url.json` reads
`https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0%2B241aaee-cp313-cp313-win_amd64.whl`
— a **cp313 wheel from Open3D's `main-devel` channel**, i.e. an unreleased development build.

Two consequences, and the second is the one that matters:

**3a — the FULL tier cannot be DECLARED, not merely cannot be installed.** A direct-URL
dependency is rejected in metadata uploaded to PyPI, so `[project.optional-dependencies]`
cannot name the only open3d that exists for 3.13. This is not "difficult"; there is no legal
declaration. Any FULL tier is honest only under `requires-python = ">=3.11,<3.13"`, which
**contradicts the interpreter the whole repo runs on.**

> ⚑ **CORRECTED 2026-08-09, before the release, at the Director's question — and the
> correction is the useful part.** 3a as written above **conflates two things and is too
> strong.** True: the only open3d that exists *for 3.13* is a direct-URL devel wheel, and
> that cannot be declared. **False: that no FULL tier can be declared.** `open3d` is an
> ordinary PyPI package on cp38–cp312, this arc's own FULL tier measured **0 of 8 failing on
> py3.12**, and a PEP 508 marker expresses exactly the conditional the situation calls for.
> **What fails on 3.13 is RESOLUTION, not DECLARATION**, and no `requires-python` narrowing
> is needed.
>
> Shipped instead: **`[measure-full]` carrying `open3d; python_version < "3.13"`** — all
> eight tools on 3.11/3.12, and on 3.13 the extra resolves *without* open3d so the install
> succeeds and the four geometry tools refuse with exit 4. Verified on this rig: exit 0, no
> open3d, no resolver error. Pinned by a T59 leg that evaluates the marker at 3.11, 3.12 and
> 3.13 and asserts the full tier is a superset of the light one.
>
> ⚠ **And the thing the seat had in hand and did not use.** It read
> `direct_url.json`, saw `main-devel` and `cp313` in the filename, correctly inferred
> "unreleased dev build" — and still wrote *"there is nothing installable for Python 3.13"*
> into a pyproject comment, a runtime refusal and this ruling. **A direct URL is legal on a
> `pip install` command line and banned only in published metadata**, so all eight on 3.13
> was always one documented command away. Measured at the correction: Open3D's `main-devel`
> is a **rolling prerelease with 8 cp313 wheels**, currently `0.19.0+63e30be` — *newer than
> the `+241aaee` this rig runs*, which makes 3b's comparability gap concrete rather than
> hypothetical. The Director had to raise nightly builds himself, having done so before.
> This is the *enumerate the resource before commissioning one* law with the resource
> already open on the screen.

**3b — ⚑ every open3d-dependent number this repo has produced was measured on an unreleased
dev build.** `0.19.0+241aaee` is not `0.19.0`. **Four of the eight served instruments need
open3d** (`reach_ceiling`, `thin_extent_curve`, `offsurface_rate`, `texel_provenance`). The
identity envelope carries server version, instrument sha256 and config hash — **and no
dependency set.** So a number reproduced on another machine against PyPI's `0.19.0` is being
compared to one produced against a git-hash-suffixed build, and *the envelope cannot see the
difference.*

This does not make any recorded number wrong, and nothing is withdrawn. It names a
**comparability component the envelope does not record**, which has been invisible while every
measurement ran on one rig and becomes load-bearing **the moment the tool is published** —
which is precisely what this arc is for. **Recording the dependency set in the envelope is
commissioned in principle, unscoped here.**

## Ruling 4 — ⛔ THE BINARY IS RULED OUT FOR THE MEASUREMENT SERVER. Size was never the question.

The frozen binary is **162,962,583 bytes — 12× inside** GitHub's 2 GB cap, and it answers
`--print-tools` with exit 0. It **cannot run one measurement**: in a one-file PyInstaller build
`sys.executable` *is the binary*, so every instrument subprocess re-enters the server's own
argparse.

**That is [E24](E24-ruling.md)'s exact shape — a surface that answers `--help` while the verb
underneath is broken — caught before a release rather than after four.** The arc's own task 0
discipline found it, which is the discipline working.

So `bin/facet.js:18`'s stated precondition resolves cleanly rather than being voided: the npm
binary door **stays open for the record server**, whose dependencies really are stdlib +
sqlite3 + mcp, and **closes for the measurement server** — not on size, on process identity.

## Ruling 5 — ⚑ `anchor_check` HAS A REAL DEFECT, AND IT IS THE POLISH ARC'S ENTRY GATE

Read at source, `tools/verify/anchor_compare.py:101-106`:

```python
try:
    from PIL import Image          # the import is INSIDE the try
    with Image.open(p) as im: ...
except Exception as exc:           # ModuleNotFoundError caught as a decode failure
    imgs.append(exc)
```

With PIL absent the run reports **"one or both inputs do not decode as images; the byte tier is
what exists for them"** and **exits 0** — blaming the caller's PNGs for a missing dependency,
and silently degrading to **byte tier only**.

**That is the exact configuration this repo built the pixel tier to escape.** CLAUDE.md's
standing law is *a PNG hash mismatch is not evidence a render changed — file bytes are not
pixel values*, earned on **two** false halts; [E28 Ruling 14](E28-ruling.md) built the two-tier
instrument for it; and [E30](E30-ruling.md)'s W3 halt was **confirmed by the pixel tier** after
the byte tier flagged it. A PIL-less `anchor_check` is a byte-only comparator that says
everything is fine.

And it is not a hypothetical seat that runs it: **[E14 Ruling 35](E14-ruling.md)'s clause opens
every polish lane with a per-profile anchor gate**, and `anchor_check` is that gate.

**RULED: a missing dependency is an environment REFUSAL, not a per-input decode result.**
`ImportError`/`ModuleNotFoundError` must be distinguished from a genuine decode failure and
routed to **exit 4 REFUSED** — the code this repo already reserves for *the tool working and
telling you not to proceed*. **Commissioned with a test that installs without PIL and asserts
the refusal**, in the commit that makes the change. This is the arc's most consequential
finding for correctness and it was not in its own headline.

## Ruling 6 — OQ2 ANSWERED: Shape A, with a LIGHT extra. The FULL tier is not declarable.

**Shape A works** — instruments ship, and at FULL the failing count is **0 of 8**. That is
measured, not argued.

**The tier is decided by Ruling 3a, not by preference.** LIGHT (numpy, scipy, trimesh, pillow —
277.9 MB) is declarable on every Python the package claims, and carries **4 of 8**:
`mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check` — **including both anchor
tools**, which is the half the polish arc's gate actually calls. FULL cannot be declared at all
on 3.13.

**Ruled — AMENDED 2026-08-09 before release (see Ruling 3a's correction): ship Shape A with
BOTH extras.** `[measure]` resolves everywhere and carries four tools including both anchor
tools. **`[measure-full]` carries `open3d; python_version < "3.13"`** — all eight on
3.11/3.12, and on 3.13 it resolves without open3d so the install succeeds and the four
refuse with exit 4. The README documents the devel-channel wheel as the third path to eight
on 3.13.

*The original ruling stopped at the LIGHT extra and is kept above with its reasoning, because
the reasoning is where the error was: it treated "cannot be satisfied on one interpreter" as
"cannot be declared at all", and never asked whether a marker expressed the difference. A
forced FULL extra would indeed be the "tool that is forced" the Director's bound rejects — but
a **conditional** one is not forced, it is accurate.*

⚖ **One clause of this is his, not mine.** Whether a published server where **4 of 8 tools
need an out-of-band dependency** satisfies *"the pipeline on npm"* is a product question, not
an engineering one. The engineering says: this is the most that can be declared honestly.

## Ruling 7 — ⚑ MY GATE 6 WAS DRAWN ONE SURFACE TOO NARROW, AND THE FILE I MISSED RECORDS THE LAST TIME SOMEONE MISSED IT

I reserved `README.md`, `docs/advisor-kickoff.md`, `site/src/site-config.ts`,
`site/src/content/docs/handbook/getting-started.md` and the DB/cert pair. **T34 also pins
`SHIP_GATE.md` and `site/src/content/docs/handbook/reference.md`**, which I did not name.

⚑ **AND THE FIRST DRAFT OF THIS RULING GOT ITS OWN FIGURE WRONG, WHICH IS THE THIRD
INSTANCE IN ONE SESSION.** It read *"nine pins across five files"* — transcribed from a
failure list, exactly the method the ruling below forbids. **Read from the instrument:
`T34.PINS` holds SIXTEEN pins across SIX files** — README.md ×4, SHIP_GATE.md ×4,
advisor-kickoff.md ×2, getting-started.md ×3, reference.md ×1, site-config.ts ×2 — **plus a
separate leg over the seven translated READMEs**, which carry both counts twice each and
which a failure list does not surface until the pinned files are already green. Twenty-eight
substitutions in the translations alone. A failure list shows what is *currently* stale; the
PINS table shows what is *watched*, and those are different sets.

**And `SHIP_GATE.md:61`'s own text is the record of the previous instance**: *"the outgoing
handoff enumerated four stale surfaces… and did not name `SHIP_GATE.md`, so a hand-written list
of surfaces is itself a live-moving quantity."* I hand-wrote the list again, and left out the
same file, which had written down that this would happen.

**RULED: a dispatch reserves count surfaces by naming T34's PINS table, never by transcribing
it.** The instrument already enumerates them; a prose copy is a second population that drifts
from the first. Reconciled in this commit: **808/768 → 859/819** across all nine pins, plus
SHIP_GATE's lineage extended rather than overwritten.

⚠ **The census is the other half and was also unnamed.** [E28 Ruling 25](E28-ruling.md) makes
it a derived artifact that re-emits with the fold; it is **machine-emitted from whatever is on
disk**, so it cannot be hand-reconciled and it belongs in the same reservation. Re-emitted here.

## Ruling 8 — the commit-message arithmetic is CORRECTED IN PLACE, and the handling is ratified

`943d2d5`'s message states the new counts as `818/778`. Measured at two seats: **859/819**. The
executor states plainly that *"that was arithmetic, not measurement"*, left the commit standing,
and put the correction in the report beside it. **Ratified** — a commit message cannot be
edited without rewriting history, and the correction next to the wrong number is this repo's
whole method. **Never compute a count you can collect.**

## Ruling 9 — P1's miss is the ninth arc on the unit family, and it has a new form

**"I counted a surviving *path* as a surviving *tool*."** P1 missed by one in each direction
while landing inside its band. The family now reads: the *unit*, the *population*, an unchecked
*property*, the rarest clause of a *conjunction*, the *instrument's continued ability to express
the question*, the *premise inherited from your own dispatch* — and now **the object the count
is over** (a code path is not a tool; several tools can share one).

**P3-linux** missed above band for a reason worth keeping: *the package that dominates the
payload was never checked* — open3d's manylinux wheel is **6.5×** its Windows one. Predicting a
total without measuring its largest term is the same error at a different scale.

## Ruling 10 — what is NOT ruled here

- **The tag, the publish, the release.** Steps 7 and 8 are the Director's. Nothing is tagged,
  published or released; **no version moved**, and `MEASURE_VERSION` is unchanged at 0.4.0 as
  gate 3 required.
- **Whether 4-of-8-with-an-out-of-band-dependency is the product** (Ruling 6's last clause).
- **The envelope's dependency set** (Ruling 3b) and **`anchor_check`'s refusal** (Ruling 5) are
  commissioned in principle and unscoped — they are the next arc, not this one.

## Ruling 11 — the executor's conduct

It **built six wheels and six clean venvs** where the dispatch asked for one, and called every
tool through the server's own dispatch rather than importing it. It **found the binary's
`sys.executable` defect by running a measurement instead of a banner** — the exact discipline
E24 was written to install, now catching its own class prospectively. It **closed task 0-pre
with a test rather than a line** (4 failed / 1 passed before, 5 passed after) and widened T23's
"exactly one server" assertion in the same commit. It **named three behaviours nobody had
written down**, one of which is Ruling 5's defect. And it **corrected its own commit message's
arithmetic in the report** rather than leaving it or quietly rewriting it.

It also **stopped at gate 6 and did not touch the count surfaces**, exactly as instructed, and
reported the drift — which is why the reconciliation was available to be done correctly at one
seat instead of contested at two.

---

## Folded in this commit

| where | what |
|---|---|
| `README.md` ×2, `SHIP_GATE.md` (+lineage), `site-config.ts`, `getting-started.md` | Ruling 7's reconciliation, 808/768 → **859/819**, nine pins |
| `CLAUDE.md` | Ruling 2 (enumerate presence before failure modes) · Ruling 9's new family member · Ruling 3b's envelope gap |
| `docs/experiments/README.md` | the E31 status row |
| the census + index pair | re-emitted, Ruling 7's second half |

## Open, carried forward

- **`anchor_check`'s refusal path** (Ruling 5) — commissioned, unscoped, and it gates the polish arc.
- **The envelope's dependency set** (Ruling 3b) — commissioned, unscoped.
- **The product question** in Ruling 6's last clause — the Director's.
- **`requires-python`** — untouched here. Any FULL tier forces `<3.13`, which contradicts the rig.
