# E22 — ruling: the gates an environment variable deletes

**Advisor, 2026-08-08.** Report: [E22-gates-report.md](E22-gates-report.md).
Predictions: [E22-predictions.md](E22-predictions.md), committed at `a729e6e` before
the first file under `tools/` was opened. Spec:
[E22-gates-not-asserts-kickoff.md](E22-gates-not-asserts-kickoff.md).

Every number below that decides something was re-measured at this seat. Where my
measurement and the report's disagree, both are printed.

---

## Ruling 1 — THE ARC IS ACCEPTED

The four gates pass, the conversion is a pure move, and the compensator gate — the row
this dispatch scored **1** — was carried out more completely than it was written.

Re-measured here, independently of the report:

| claim | report | this seat |
|---|---|---|
| suite, artifacts tier live | 275 | **275 passed in 180.42s** |
| ANDON asserts left in the seven files | 0 | **0**, by my own AST walk |
| `EXIT_REFUSED` | 4 | **4** (`facet_index.py:123`) |
| `parse_verify` keys on `rc != 0` | yes | **yes** (`record_mcp.py:430,433`) — indifferent to which non-zero |
| `run_contract` catches `AssertionError` | `:208`, before the broad handler | **`:215`, and the broad `except Exception` is at `:231`** — the ordering holds |
| CI on `f878b8b` | green | **success**, verified by run id |

**And the thesis itself, measured as a before/after pair on one gate rather than taken
from the report.** `RecordError('NOT_A_REAL_CODE', …)`, four interpreter modes, the
same gate at the pre-E22 tree and at HEAD:

```
                          483627a (pre-E22)     HEAD (post-E22)
python                    GATE FIRED            GATE FIRED
python  PYTHONOPTIMIZE=1  GATE SILENT           GATE FIRED
python -O                 GATE SILENT           GATE FIRED
python -O PYTHONOPTIMIZE=1 GATE SILENT          GATE FIRED
```

The defect was real, it is repaired, and neither half of that is inherited.

---

## Ruling 2 — F1 IS UPHELD. THE CENSUS WAS THE ADVISOR'S ERROR, AND IT WAS MADE TWICE.

Measured at this seat, over the pre-E22 tree read straight from git blobs, with an AST
walk written without opening the executor's instrument:

```
483627a  tools/ , 150 python files
  assert statements                294  across 72 files
    carrying the ANDON token       278  across 62 files
    carrying no ANDON token         16
```

**Reproduces the report exactly.** The dispatch's *"~207 non-ANDON asserts … developer
sanity checks"* described a class of **16**.

**How the 207 was manufactured, because that is the transferable part.** E21 Ruling 2 —
which I wrote the amendment to and did not check — published a table of ANDON counts for
**five tools**, summing to 86, and reported it as **87**. The dispatch then computed the
excluded class as `294 − 87 = 207`. **A five-tool subtotal was subtracted from a
repo-wide total**, and the difference was given a name, a character ("developer sanity
checks") and a reason to be left alone. Every per-tool cell in that table reproduces to
the digit. The two totals derived from them are the only wrong numbers, and both are
derivations rather than measurements.

**Owned, in two places.** E21 Ruling 2 is my predecessor's. The amendment that added a
standards block and an Environment section to this dispatch is **mine, written this
session** — I read the scope clause closely enough to score its compensators at 1 and
did not spend the two tool calls that would have falsified its central number. The
seat's own standing instruction is *measure before ruling*; I applied it to the
compensator row and not to the row above it.

---

## Ruling 3 — THE ANDON TOKEN IS THE RIGHT AXIS. IT IS RATIFIED, NOT OVERTURNED.

The report asks (open question 1) whether the token is the wrong axis and the real scope
is *"every assert that guards an irreversible step."* **It is not.** This is the one
place I depart from the direction the report leans, and it is decided by reading all
**15** surviving non-ANDON asserts rather than by reasoning about them:

```
6   tools/superseded/*      off the route BY DESIGN - kept runnable so they fail the same way
3   "no mesh in GLB"        input validation on a missing argument, in verify/ and superseded/
2   shape-match checks      diagnostics comparing a frame against its mask
2   basis-vector checks     project_twins:476-477, the camera convention
1   labels/images match     verify/head_crop, a user error
1   texpass_iter:454   \    labelled IMPLEMENTATION:, NOT ANDON, deliberately
1   project_twins:800  /
```

The last two decide it. Both sit **inside files E22 just converted**, one of them in the
**write-head**, and both were left as `assert` because they do not carry the token — and
both carry a comment explaining that choice:

> *"The invariant this introduces forecloses over-erosion BY CONSTRUCTION, so a halt
> aimed there would fire on correct work (E08 A3's lesson). Asserted as an implementation
> check, not gated on area."* — `texpass_iter.py:451-453`

> *"…promoted to an andon, and halting on it fired on correct work once already."*
> — `project_twins.py:795`

**That is not an unmarked gate. That is an author declining andon status, in writing,
citing a ruling.** The token is a maintained taxonomy, not a marker someone forgot to
type — which is exactly the property an axis needs. `-O` deletes these two, and it costs
nothing, because an invariant foreclosed by construction cannot fire on correct code.

So the dispatch's **characterisation** was right and its **cardinality** was wrong by
191. The class it described exists; 191 declared gates were misfiled into it by
arithmetic.

**The standing law is unchanged and now has its scope stated exactly:** a check carrying
`ANDON` is its author's declaration that it decides whether an irreversible step
proceeds, and such a check must `raise`. A check carrying `IMPLEMENTATION` is a
developer's sanity check and may remain an `assert`. **A third category — a gate whose
author never declared it — is not evidence against the axis; it is a documentation
defect at that site, and it is repaired by writing the token, not by widening a rule.**

---

## Ruling 4 — THE REMAINING SCOPE IS 191 SITES IN 56 FILES, NOT 192 IN 57

The report says *"192 ANDON-carrying gates in 57 files the scope never named."*
Measured here: **191 across 56.**

```
278 pre-E22 ANDON asserts  −  87 converted carrying the token  =  191
     (88 sites were converted; record_mcp.py:189 carries no token)
```

The 192 counts `facet_index.py:343` as outside the scope. It was **in** scope and **was**
converted, and that file now holds zero. The slip is exactly the shape of the one the
report caught in the dispatch — a subtotal read as a total — and it lands in the number
that will scope the next arc, which is where it does the most damage. Corrected before
it gets there. **This is the second consecutive arc in which the scope number, not the
work, was the defect.**

**And the distribution decides the unit of work**, which the report did not measure:

| where | sites | files | what they guard |
|---|---|---|---|
| `tools/` top level | **57** | 12 | **the route** — `bake_hero_prep` 15, `brush_cloud_step` 9, `subject_profile` 6, `silhouette_masks`, `resample_atlas`, `cull_unseen`, `palette_gate`, `export_asset_source` |
| `tools/diagnostics/` | **132** | 42 | measurement instruments — sheets, probes, reports |
| `tools/superseded/` | 1 | 1 | off-route by design |
| `tools/verify/` | 1 | 1 | a render check |

**These are not one job.** The 57 route sites stand between the process and the four
accepted assets — `silhouette_masks.py:160` is the one whose own message reads *"Fix
before generating anything"*, and at `:165` the file writes `silhouettes.json`. The 132
diagnostics sites mislead a reader when they fail silently; they do not corrupt an
artifact. Same repair, different risk, different anchors available.

**Ruled: E23 takes the 57 route sites**, under E22's bar exactly — pure move, whole-file
AST equality against the prior commit, anchors where they exist, and the tree manifest
before the first replay. **The 132 diagnostics sites are a separate, later, mechanical
arc.** `superseded/`'s one site is **not converted**: those tools are kept so anyone can
run them and watch them fail the same way, and changing how they fail is the one thing
that would spoil them.

---

## Ruling 5 — F2: DO NOT UNIFY THE EXCEPTION TYPES. RECORD THE CONSTRAINT INSTEAD.

Three ANDONs already `raise SystemExit` (`project_twins:281`, `e11_manifest:267`,
`e11_export_turnaround:108`). The executor reported them and did not touch them, which
was right on the pure-move bar.

`raise SystemExit` is **not deletable by `-O`**, so it does not carry the defect this arc
exists to fix, and normalising a type nobody ruled is not a pure move. **They stay.**

The constraint that comes with that, recorded because it is a trap for a later seat:
`run_contract`'s fired-gate branch keys on `AssertionError`, and `SystemExit` is
re-raised untouched one handler above it. **If any of those three tools ever moves into a
shipped command, its ANDON exits through argparse's contract rather than through
`GATE_FIRED`, and it will not carry `EXIT_REFUSED`.** That is a condition on a future
move, not a defect today — all three are unpublished research tools.

---

## Ruling 6 — `4 = REFUSED` DOES NOT EXTEND TO THE RESEARCH TOOLS

Open question 3. **No**, and the executor was right not to take it on its own authority.

E21 Ruling 4 ruled the exit-code registry of the **two published commands**. The 34
research scripts have no `run_contract`, no registry, and no operator contract to be
inconsistent with — a fired ANDON there exits `1` with a traceback, which is CPython's
default and not a claim anyone made. Building an exit-code registry across 34 unpublished
scripts is the same purchase `SHIP_GATE`'s B1 line already refuses: a large change to
accepted-asset tooling bought for a checkbox.

The asymmetry is now written down rather than latent: **the two installed commands carry
the registry; the research tools carry the `ANDON:` convention.** Both are disclosed in
`SECURITY.md`. Re-opens if a research tool is ever published.

---

## Ruling 7 — THE `mcp_support` HARDENING IS ADOPTED

Open question 4. The executor replaced the fixture's hardcoded `1` with
`facet_index.EXIT_REFUSED` and flagged it as beyond the literal carry.

**Adopted, and it should have been in the dispatch.** E21's F3 named that constant as a
value nothing compared against a live run. Re-typing `4` there would have reproduced the
exact defect that let it be wrong — a second copy of a number, free to drift. Reading the
tool's own constant removes the copy rather than updating it.

Declaring it instead of slipping it in is the behaviour the seat wants. Noted as
**adopted**, not merely permitted.

---

## Ruling 8 — THE CERTIFICATE SCHEMA IS **NOT** BUMPED, AND THE REAL GAP IS NAMED

Open question 5 / P23. `CERT_SCHEMA = "facet-record-index-certificate/1"` stays.

`verify_exit_code`'s name and type are unchanged; only the set of values it can hold
widened. The certificate **never declared that domain**, so no consumer could have been
reading a promise that broke. In-repo, nothing enumerates it — `parse_verify` keys on
zero versus non-zero, measured.

**A free integer is not a reason, and neither is a free version.** Bumping a schema
version tells every reader "something changed that you must handle." Spending that signal
on a change no reader can observe teaches readers to ignore the next bump, which is the
one that will matter.

**The actual defect is that the domain was never written down.** Remediation, owner
advisor, next fold touching `record_mcp`: state the domain of `verify_exit_code` in the
certificate's schema note, so the *next* widening has something to be measured against.
That is the repair; the version bump would have been the paint over it.

---

## Ruling 9 — THE ASSERT LAW ENTERS `CLAUDE.md` NOW. IT SHOULD HAVE ENTERED TWO SESSIONS AGO.

E21 Ruling 2 ended: *"**THE NEW STANDING LAW, and it goes in CLAUDE.md at the next
fold**."* Measured at this seat: `CLAUDE.md` contains **zero** occurrences of it. There
have been several folds since, four of them mine today.

The law was written, ruled, and then lived only inside a ruling document — which is
precisely the failure mode this repo built a queryable record to escape, and it is why a
dispatch could rest on a phantom class for a whole arc without anything contradicting it.
Folded in this commit, with E22's measurement attached and the `IMPLEMENTATION` carve-out
Ruling 3 established.

---

## Ruling 10 — P18'S MISS IS THE ARC'S SECOND LAW

The executor predicted **4** out-of-scope asserts before a write, band 2–6; measured
**175**. The predictions file records the reasoning: an untutored estimate of 8–12,
**halved** on E21's calibration lesson that this repo's density predictions run ~2× high.

The report's own reading is correct and is adopted verbatim as a standing law:

> **Check that the population is real before you predict its density.** A quantity
> predicted about a mis-specified population cannot be right, and a calibration ritual
> applied to it gives you a way to feel careful while being wrong about the thing
> underneath.

This is the sharpest thing in the arc. The executor was handed a class that did not
exist, predicted a property of it, corrected the prediction *away* from the truth using a
discipline earned in this repo, and then diagnosed exactly that when the number came
back. **The miss is worth more than the hit would have been**, and it is scored as a miss
in their own report rather than explained away.

Note also **P14, scored a miss-shaped hit and reported as such**: T26 survived the
conversion, but it drives a subprocess and keys on `rc != 0` plus stderr text, so the
exception type was never what saved it. Verified here. The reason `AssertionError` is
mandatory is `run_contract:215` — a different site in a different file. Reporting a
correct outcome reached by wrong reasoning, unprompted, is the behaviour that makes an
executor's numbers worth ruling on.

---

## Ruling 11 — F1b IS A DIAGNOSTIC, AND IT IS CORRECTLY NOT A GATE

175 ANDON asserts followed by a write in their own scope, by a static source-order walk,
tightened after a hand-check that had counted `.copy()` and `str.replace()` as writes.

The executor states its limits before using the number, says it **under-counts on
purpose**, and refuses to promote it. That is this repo's own distinction — *a diagnostic
and a gate are different objects* — applied without being told. **Upheld as a
diagnostic.** It is required in any E23 report; it may not gate one. The three named
sites were checked here and quote their source verbatim.

---

## What is NOT ruled, and stays open

- **P5** — `fit_background` at frame-edge figures. Still the repo's highest-value
  unopened question. Untouched by this arc.
- **The `q`-verb defect** found at the v0.2.0 read-back (`docs/known-defects.md`,
  *Tooling defects*): `facet-index q` answers from an index that does not exist. Ruling 6
  narrows it — `q` is a **published** command, so the registry does apply and the honest
  code is `EXIT_REFUSED`. Still unruled as to remedy; it is not E23's.
- **The certificate's domain note** (Ruling 8's remediation).
- **The three testability seams**, U3's logging flag, the measurement MCP.

## Release

**E22 is not released by this ruling.** v0.3.0 carries the conversion and `4 = REFUSED`,
and firing it is the Director's act, not a consequence of accepting the arc.

---

## The advisor's record, this arc

**The miss:** I amended this dispatch — adding a standards block and an Environment
section, scoring its compensator row at 1 and writing three binding items under it — and
in the same pass I read the scope clause without checking the number it rested on. Two
tool calls falsified it afterwards. I applied *measure before ruling* to the row I was
adding and not to the row above it, which is the more specific version of the seat's own
failure mode: **I check the thing I am touching and inherit the thing next to it.**

**The compensator amendment was worth it and that is measurable**, so it is recorded
beside the miss rather than as consolation: the manifest it made mandatory covered 7,312
files across the whole recorded root — wider than the four named trees, which the
executor then showed do not exist at the paths the note gave (P16). It held at 0 changed,
three times. The row scored 1 because it deserved 1.

**What worked:** re-measuring the census from git blobs before ruling on it; reading all
15 surviving non-ANDON asserts instead of reasoning about the class; firing one gate in
four interpreter modes at both trees rather than accepting the report's control;
reconciling 191 against 192 before it scoped the next arc.
