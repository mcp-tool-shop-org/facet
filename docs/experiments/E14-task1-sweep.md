# E14 handoff 2, Task 1 — the sweep and the coverage pass on `profiles/prop.json`

**Executor session, 2026-08-07.** Predictions committed blind in `d11fd32`
([E14-handoff2-predictions.md](E14-handoff2-predictions.md) §1) before either instrument
ran. Exit condition per the dispatch is this report with every UNDECIDED member
dispositioned; **0 UNDECIDED gates ARMS, not this dispatch.**

```
e04_registry_sweep.py --profile profiles/prop.json --tools tools        exit 1
e04_profile_check.py  --profile profiles/prop.json --tools tools \
                      --coverage profiles/character.json                exit 1
```

Both exit non-zero by design — each is an ANDON that fires on any undecided flag, and the
firing is the instrument working, not a defect in the draft.

---

## 1. The registry sweep

```
14 route-active tools; 36 flags are CODE by the table's section 6; 71 are N/A (paths/switches)
83 SUBJECT-DATA flags on this route; decided 80
   (_NOT_CLEARED 7, _not_on_route 3, _tools_not_on_route 16, value 54)
3 UNDECIDED
```

| tool | flag | tool default this subject would silently run on |
|---|---|---|
| `restylize_views.py` | `canny-high` | 0.8 |
| `restylize_views.py` | `canny-low` | 0.4 |
| `texpass_iter.py` | `thin-extent` | 0.0 |

**Exactly the three the dispatch pre-stated, and no fourth.** The draft's `_NOT_CLEARED`
marker (7 keys) and its three `_not_on_route` entries all counted DECIDED, which is the
recognized-forms contract holding.

## 2. Disposition of every UNDECIDED member

### `texpass_iter.py --thin-extent` → **LANDS IN THIS DISPATCH** (curve), **value at a later ruling**

`prop.json`'s `_still_suspended.thin_extent` names it, and the coverage pass reaches the same
member from the other direction (`absent — reference carries 0.03`). Task 2.3 owns the *curve*;
the profile is explicit that the *value* is decided at this subject's own ruling with the curve
and artifact crops in the room — the beast's deferral pattern.

Worth restating because it changes what leaving it open costs: the tool default is **0.0**, not
the character's 0.03. The failure mode of silence here is not "inherits a character number" but
**"runs with the guard disabled"**, and on the route's thinnest subject that is the direction
worth naming.

### `restylize_views.py --canny-low` and `--canny-high` → **LAND IN THIS DISPATCH** (Task 3.1)

Deliberate, and the profile says so: `_still_suspended.canny_pair` records that the accepted
route's 0.4/0.8 was falsified on grey-on-grey clay (E12 Rulings 10c/11a) and that *"the sweep
counting them UNDECIDED is the expected state, exactly as the beast's thin-extent was."*
Two members rather than one, because the pair is two flags and the sweep counts flags.

**These are the pair the advisor rules mid-dispatch.** They do not close in this report.

### Nothing else. `brush_cloud_step --lane` did NOT appear, and that is the E12 fix landing.

E12's sweep found `--lane` UNDECIDED on **all three** profiles then in existence, including the
accepted ship, and dispositioned it as a **class fix**: a `brush_cloud_step.py` block in the
per-invocation documented-absence form, *"in all three profiles or in none."* Re-measured this
session with the same instrument on artifacts this session did not write:

| profile | `brush_cloud_step.py` block | `--lane` UNDECIDED |
|---|---|---|
| `character.json` | `_not_on_route` | no |
| `ship.json` | `_not_on_route` | no |
| `beast.json` | `_not_on_route` | no |
| **`prop.json`** | `_not_on_route` | **no** |

**The class fix is complete route-wide**, and `prop.json` is the first profile authored with it
from birth rather than patched into it.

## 3. ⚠ The cross-profile run found something, and it is not the prop draft's

Running the same sweep on all four profiles — the check that separated *"the draft missed one"*
from *"the class was already open"* on the beast — turns up a member on the **accepted ship**:

| profile | UNDECIDED | which |
|---|---|---|
| `character.json` | 18 | its own silences; see §5 |
| **`ship.json`** | **2** | **`project_twins fit-axis`, `project_twins margin`** |
| `beast.json` | **0** | — |
| `prop.json` | 3 | the three above |

Verified directly against the files rather than taken from the instrument. **The framing family
`{aspect, fit-axis, margin}` on its four consumers:**

| profile | `turn_render` | `silhouette_masks` | `project_twins` | `texpass_iter` |
|---|---|---|---|---|
| character | SILENT → `height` | SILENT → `height` | SILENT → `height` | SILENT → `height` |
| **ship** | **`width`** | **`width`** | **SILENT → `height`** | **`width`** |
| beast | `width` | `width` | `width` | `width` |
| prop | `height` | `height` | `height` | `height` |

**`ship.json` is the only profile whose framing family is internally split.** Three consumers
say `width`; the fourth is silent and takes the tool's `height`. Character is silent on all four
and is coherent by construction — its silences *are* its claim, and the tool defaults *are* the
character's values (a height-fit subject). Beast and prop are coherent by pinning.

**The magnitude is on the record already, in the tool's own source.** `project_twins.py:190–208`
carries the E13 handoff-13 measurement of exactly this split, made on the beast:

```
width-fit derivation      bbox [152,85,1639,938]  520,644 px  IoU 1.000000
this tool's derivation    bbox [154,87,1637,936]  517,340 px  IoU 0.986006
```

— the derived frame 1.003313 of the render's, *"every sample sits up to 0.33% of its distance
from frame centre too far in — 2 px at the figure's own bbox edge on view 0."*

**What this report claims and what it does not.** It claims the configuration fact: as
`ship.json` stands today, its projector would run height-fit against masks rendered width-fit.
It does **not** claim the accepted galleon's shipped asset is misregistered — the `--fit-axis`
flag did not exist when that asset was made, its default is the pre-E13 expression every
pre-E13 anchor reproduces, and what the ship actually ran with is a question about the ship's
own record, not about today's profile. **Finding for the ruling**, and the same shape as the
`lane` finding it replaces: E12 Ruling 26a *"completed the pin"*, the beast got it, `prop.json`
got it at draft — and the ship, which is where Ruling 24a **exposed** the slot, did not.

## 4. The coverage pass

```
[chk] prop.json: 54 values checked against 9 tools
[chk] NOT A PURE RELOCATION - 15 mismatches
```

`prop.json` does not claim to be a pure relocation, so the headline is the expected verdict
rather than a finding. All 15 are intended and each carries its `why` and `from` — enforced at
load, since `bind()` asserts both on every entry and all nine blocks bound clean.

| reason | rows |
|---|---|
| **measured at Gate 0** | `turn_render w` 752→240 · `silhouette_masks aspect`, `project_twins aspect`, `texpass_iter aspect` 752,1024→240,1024 |
| **ruled** (E14 Ruling 4, allocation NONE) | `bake_hero_prep head-scale` 3.0→1.0 · `project_twins head-facing-min` 0.18→0.45 · `head-edge-dist` 3.0→7.0 — head bands set equal to the body's so they run inert |
| **ruled** (E14 Ruling 5a, the register) | `restylize_views lora-w` 0.75→0.0 |
| **suspension, expressed mechanically** | `reg-iou-min` 0.8→0.0 · `bbox-tol` 0.25→9.99 · `bg-max-pct` 2.0→100.0 |
| **subject naming** | `turn_render tag` view→swordclay · `silhouette_masks tag` w3clay→swordclay |
| **the protective transcription** (E04 Ruling 22) | `restylize_views prompt` — the code default is W3's literal identity string, the named accident class |
| **not evaluable by the checker** | `cull_unseen production` — §4.1 |

**`fit-axis` and `margin` are absent from this table on every consumer, and that is correct**:
this subject's family value is `height`, which *is* the tool default, so pinning it produces no
mismatch. The pin still matters — it makes the value a decision rather than a silence, and
`prop.json`'s `fit-axis` note says so explicitly. Section 3 is what that distinction is worth.

Coverage against the reference: **61 of `character.json`'s keys decided, 3 UNDECIDED** — the
same three as §1, reached from the other direction. Four whole-tool decisions were read back
correctly and recorded as decisions rather than gaps: `smart_decimate.py`,
`verify/head_render.py`, `verify/mesh_stats.py` (`_tools_not_on_route`) and `texpass_brush.py`
(`_NOT_CLEARED`, all 7 keys).

### 4.1 The one row the checker could not evaluate, checked by hand

`cull_unseen production`'s tool default is a computed expression, so the static checker reports
`not evaluable` and passes over it. That is the flag E06's superset rule governs, and a silent
narrowing there is a documented failure class. Evaluated and compared directly:

| | |
|---|---|
| tool default cameras | 26 |
| `prop.json` cameras | 26 |
| strings identical | **True** |
| in default, absent from profile (a narrowing) | **none** |
| in profile, absent from default (needs the union re-issue) | **none** |
| all eight eye-level twin yaws covered | **True** |
| elevated cameras already in the superset | `0,55` · `180,55` |

No narrowing. The profile's note — that any adopted elevated camera outside this list forces a
union re-issue — stands as written, and **Task 2.4's elevated measurement is where it would
fire**. Recorded now because the answer changes what that task's disposition costs: if the
measurement adopts an elevated camera at elevation 55 on yaw 0 or 180, no re-issue is needed at
all; any other elevation or yaw forces one.

## 5. `character.json`'s 18, stated so the table above is not misread

The character profile carries **18 UNDECIDED** and this is not a defect being reported here.
Its whole claim is *relocation* — its silences are not decisions, which is the premise the
sweep was built on, and its silences resolve to the tool defaults which **are** the character's
own measurements. Quoted because §3 puts four profiles in one table and a reader could take
the 18 as a comparable number. It is not comparable; it is a different kind of file.

## 6. Predictions scored

| # | prediction | outcome | measured |
|---|---|---|---|
| S1 | both instruments exit non-zero | **held** | exit 1 / exit 1 |
| S2 | `thin-extent` UNDECIDED | **held** | present |
| S3 | `canny-low` **and** `canny-high`, two members | **held** | both present |
| S4 | `brush_cloud_step lane` does NOT appear | **held** | absent on all four profiles; `_not_on_route` counted DECIDED |
| S5 | total UNDECIDED = 3 | **held exactly** | 3 |
| S6 | 12–22 mismatches, NOT A PURE RELOCATION | **held** | 15 |
| S7 | `production` 26 cameras, byte-identical, no narrowing, `not evaluable` by the checker | **held, all five clauses** | as tabled |
| S8 | no `bake_hero_prep` flag UNDECIDED despite four absent keys | **held** | the classification table calls them CODE/N-A |

**Eight of eight — and the caveat E12's Task 3 report earned applies here word for word.**
These are predictions about *a file the advisor had just authored and an instrument whose
contract is written down*, not about an unmeasured subject. S4 is the only one that was a real
bet (I flagged it as the one I was least sure of, because whether the sweep accepts
`prop.json`'s dict-shaped `_not_on_route` was a code fact I chose not to check), and it came in.
The scoreboard here should not be read against §2 of the measurement report, where the
predictions are about a subject nobody has measured.

**What the scoring missed entirely:** nothing in the prediction file anticipated §3. The
cross-profile run was in the plan as *corroboration* for S4 and it returned a finding on a
different flag on a different profile — which is the E12 precedent's actual lesson about that
run, repeating.

## 7. Exit state

| member | disposition |
|---|---|
| `texpass_iter thin-extent` | **lands in this dispatch** — the curve (Task 2.3); the **value** is a later ruling, per the profile |
| `restylize_views canny-low` | **lands in this dispatch** — Task 3.1, ruled by the advisor mid-dispatch |
| `restylize_views canny-high` | **lands in this dispatch** — same |
| *(not a prop member)* `ship.json project_twins fit-axis` / `margin` | **finding for the ruling** — the framing family's fourth-consumer pin never landed on the accepted ship; §3 |

**UNDECIDED at the close of Task 1: 3. None is a defect in the prop draft** — all three are the
dispatch's own planned members, and the fourth row is a pre-existing gap on another profile that
this session's cross-profile run surfaced. **0 UNDECIDED remains the gate on future ARMS, not on
this dispatch**, and this report is Task 1's exit condition.

## 8. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Both invocations and exit codes recorded verbatim; every count quoted from the tools' own stdout; the hand-evaluated `production` comparison shown with both operands; the framing-family matrix read directly from the four profile files rather than from the instrument's summary |
| ANDON_AUTHORITY | 3 | Both instruments are ANDONs and both fired; neither tuned nor skipped; the one row an instrument could not evaluate was checked by hand rather than passed over |
| NAMED_COMPENSATORS | 3 | Read-only. One new report; no profile, tool or artifact written |
| DECOMPOSE_BY_SECRETS | 3 | The sweep grades against the classification table rather than another subject's silences; §3's finding is dispositioned as another profile's gap rather than folded into the prop draft, and §5 states why `character.json`'s 18 is not a comparable number |
| UNCERTAINTY_GATED_HUMANS | 3 | No UNDECIDED member is resolved here — the canny pair explicitly goes to the advisor mid-dispatch, and the thin-extent **value** is left to its own ruling with only the curve landing in this dispatch. §3 goes up as a named decision with its measured magnitude, not as a value chosen by this seat |
| EXTERNAL_VERIFIER | 3 | Two independent instruments on different references agreed on all three members; the cross-profile run used the same instrument on artifacts this session did not write, and its finding was then verified a second way by reading the four profiles' framing-family keys directly; the magnitude quoted in §3 comes from a measurement recorded in `project_twins.py`'s own source by a different session |
