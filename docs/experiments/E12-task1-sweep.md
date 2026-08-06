# E12 handoff 2, Task 1 — the sweep and the coverage pass on `profiles/beast.json`

**Executor session, 2026-08-05.** Both instruments run against the beast profile. Exit
condition per the dispatch is this report with every UNDECIDED member dispositioned; **0
UNDECIDED gates ARMS, not this dispatch.**

```
e04_registry_sweep.py --profile profiles/beast.json --tools tools        exit 1
e04_profile_check.py  --profile profiles/beast.json --tools tools \
                      --coverage profiles/character.json                 exit 1
```

Both exit non-zero by design — each is an ANDON that fires on any undecided flag, and the
firing is the instrument working, not a defect in the draft.

---

## 1. The registry sweep — the stronger of the two references

The sweep grades against E04's classification table rather than against `character.json`,
because (its own docstring) the character profile is *"the registry of flags the character
needed to write down, not the registry of flags that matter"* — a key sitting at the tool's
own default was never written there, so an absent key cannot be reported absent.

```
14 route-active tools; 36 flags are CODE by the table's section 6; 68 are N/A (paths/switches)
81 SUBJECT-DATA flags on this route; decided 79
   (_NOT_CLEARED 7, _not_on_route 2, _tools_not_on_route 16, value 54)
2 UNDECIDED
```

| tool | flag | tool default this subject would silently run on |
|---|---|---|
| `texpass_iter.py` | `thin-extent` | 0.0 |
| `brush_cloud_step.py` | `lane` | `'base'` |

### A correction to the dispatch's own expected-members list

The dispatch expected three kinds of member: `thin-extent` (correct), *"the `texpass_brush`
block behind its `_NOT_CLEARED` marker (lifecycle, stays)"*, and whatever the draft missed.

**`texpass_brush` does not appear in the UNDECIDED set, and should not.** `_NOT_CLEARED` is
one of Ruling 22's four decision forms, and the sweep counts it as such — all **7** of that
block's keys are in the `decided` column. The marker is doing exactly its job. The
expectation was reasonable but the instrument's contract already answers it, so the
UNDECIDED set has two members rather than the anticipated three-ish.

## 2. Disposition of every UNDECIDED member

### `texpass_iter.py --thin-extent` → **LANDS IN THIS DISPATCH**

Deliberate and anticipated. `beast.json`'s `_still_suspended.thin_extent` names it and says
the block carries no key until Task 2 measures it; the coverage pass agrees from the other
direction (`absent — reference carries 0.03`). Task 2.3 owns it: extent density on the
designated mesh, the full cost curve, and — separately — what fraction of the membrane
fields each candidate withholds.

Worth stating because it changes what a wrong value costs: the tool default is **0.0**, not
the character's 0.03. So the failure mode of leaving it undecided is not "inherits a
character number" but "runs with the guard disabled." Either way it is a decision nobody
made, which is what the sweep is for.

### `brush_cloud_step.py --lane` → **FINDING FOR THE RULING**, and it is *not* the beast draft's

Two measurements move this off "the draft missed one":

**It is open on all three profiles, including the accepted ship.**

| profile | UNDECIDED | includes `brush_cloud_step lane` |
|---|---|---|
| `beast.json` | 2 | yes |
| `ship.json` | **1 — and this is the one** | yes |
| `character.json` | 17 | yes |

The ship carried an asset through to acceptance with this flag open. (`character.json`'s 17
are the sweep working as designed against a profile whose whole claim is *relocation* —
its silences are not decisions, which is the premise the sweep was built on.)

**And no profile can decide it with a value: `brush_cloud_step.py` calls
`subject_profile.bind()` zero times.** It takes a `--profile` (required, E04 Ruling 24) and
reads `_fixtures` through `subject_profile.value()`, but it never binds, so `--lane` is not
reachable from any profile block. The sweep is asking for a decision in a form the tool
cannot receive.

That leaves exactly one expressible decision form, and the repo already has it: the
**per-job documented absence**, `texpass_iter`'s `_not_on_route` shape —

> `yaw`: SUPPLIED PER STROKE from the future brush-prompts `_order`, never from this
> profile … The tool default (90.0) must not arrive by silence.

`--lane` is the same kind of value: declared per invocation and cross-checked against the
job's state identity (the tool's own help calls it *"a declared input cross-checked against
data already in hand"* precisely so a guard cannot infer its own jurisdiction). **The
advisor's call**, and it is a class fix rather than a beast fix: a `brush_cloud_step.py`
block in the per-job form, in all three profiles or in none.

Not dispositioned as lifecycle-blocked, though it is adjacent to one: `beast.json`'s
`_NOT_CLEARED` covers `texpass_brush.py`, and the profile even names `brush_cloud_step` in
that block's `_THE_RECIPE_NUMBERS_DO_NOT_REACH_THE_CLOUD_GRAPH` note — it knows the tool
exists and that it binds nothing — but the marker is on the other tool, so the sweep is
right that this flag is undecided.

## 3. The coverage pass — what "NOT A PURE RELOCATION" means here

`e04_profile_check` asks whether a profile is a pure relocation of the tools' own defaults.
That is `character.json`'s claim and it is **explicitly not the beast's**, so the headline
line is the expected verdict rather than a finding:

```
[chk] beast.json: 54 values checked against 8 tools
[chk] NOT A PURE RELOCATION - 17 mismatches
```

All 17 are intended, and each carries its `why` and `from` — enforced at load, since
`bind()` asserts both on every entry and all eight blocks bound clean. Grouped by reason:

| reason | rows |
|---|---|
| **measured at Gate 0** | `turn_render w` 752→1792 · `silhouette_masks aspect`, `project_twins aspect`, `texpass_iter aspect` 752,1024→1792,1024 |
| **ruled** (E12 Ruling 4a / the framing family) | `fit-axis` height→width on all three consumers |
| **ruled** (E12 Ruling 2, allocation NONE) | `bake_hero_prep head-scale` 3.0→1.0 · `project_twins head-facing-min` 0.18→0.45 · `head-edge-dist` 3.0→7.0 — the head bands set equal to the body's, so they run inert |
| **suspension, expressed mechanically** | `reg-iou-min` 0.8→0.0 · `bbox-tol` 0.25→9.99 · `bg-max-pct` 2.0→100.0 |
| **subject naming** | `turn_render tag` view→dragonclay · `silhouette_masks tag` w3clay→dragonclay |
| **the protective transcription** (E04 Ruling 22) | `restylize_views prompt` — the code default is W3's literal identity string, the named accident class |
| **not evaluable by the checker** | `cull_unseen production` — see below |

Coverage against the reference: **63 of `character.json`'s keys decided, 1 UNDECIDED** —
`texpass_iter thin-extent`, the same member as §2, reached from the other direction.

Four whole-tool decisions were read back correctly by the tool and are recorded as
decisions, not gaps: `smart_decimate.py`, `verify/head_render.py`, `verify/mesh_stats.py`
(`_tools_not_on_route`) and `texpass_brush.py` (`_NOT_CLEARED`, all 7 keys).

### The one row the checker could not evaluate, checked by hand

`cull_unseen production`'s tool default is a computed expression
(`";".join([f"{y},0" for y in range(0,360,15)] + ["0,55","180,55"])`), so the static checker
reports `not evaluable` and passes over it. That is precisely the flag E06's superset rule
governs — *the visibility set must be a superset of every production camera* — and a silent
narrowing there is a documented failure class. Evaluated and compared directly:

| | |
|---|---|
| tool default cameras | 26 |
| `beast.json` cameras | 26 |
| strings identical | **True** |
| in default, absent from profile (a narrowing) | **none** |
| in profile, absent from default (needs the union re-issue) | **none** |
| all eight eye-level twin yaws covered | **True** |

No narrowing. The profile's note that any adopted elevated camera outside this list forces a
union re-issue stands as written, and Task 2.4's elevated ruling is where it would fire.

## 4. Exit state

| member | disposition |
|---|---|
| `texpass_iter thin-extent` | **lands in this dispatch** (Task 2.3) |
| `brush_cloud_step lane` | **finding for the ruling** — pre-existing on all three profiles, not profile-expressible as a value, class fix in the per-job documented form |

**UNDECIDED at the close of Task 1: 2. Neither is a defect in the beast draft.** One is the
dispatch's own planned member; the other is a repo-wide gap the beast profile is the third
to inherit and the first to have surfaced with its cross-profile evidence. **0 UNDECIDED
remains the gate on future ARMS, not on this dispatch**, and this report is Task 1's exit
condition.

## 5. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Both invocations and exit codes recorded verbatim; every count quoted from the tools' own stdout; the hand-evaluated `production` comparison shown with both operands |
| ANDON_AUTHORITY | 3 | Both instruments are ANDONs and both fired; neither was tuned or skipped; the one row an instrument could not evaluate was checked by hand rather than passed over |
| NAMED_COMPENSATORS | 3 | Read-only. One new report; no profile, tool or artifact written |
| DECOMPOSE_BY_SECRETS | 3 | The sweep grades against the classification table rather than against another subject's silences — the whole reason it exists — and the `lane` finding is dispositioned as a class fix across all three profiles rather than a beast patch |
| UNCERTAINTY_GATED_HUMANS | 3 | Neither UNDECIDED member is resolved here; `lane` goes to the advisor as a named decision with its evidence and the one expressible form identified, not as a value chosen by this seat |
| EXTERNAL_VERIFIER | 3 | Two independent instruments on different references agreed on `thin-extent`; the cross-profile run (ship, character) is the check that separated "the draft missed one" from "the class was already open", and it used the same instrument on artifacts this session did not write |
