# E04 Arm T — HALT before the first twin. Three findings, one of them H2's.

**Executor session, 2026-08-04.** Arm G7 is complete and reported
([E04-g7-report.md](E04-g7-report.md)). Arm T's first commands do not run as the spec writes
them. **No twin has been generated, no cloud call was made for Arm T, nothing has been
projected.** Halting per CLAUDE.md §"Rules for an executor session" item 3.

Everything below is measured. Two of the three findings were found by running the tools rather
than by reading them, and the third is a fired in-tool ANDON.

---

## Finding 1 — H2 IS FALSIFIED. Twins at the profile's ten cameras need a shared-code change.

The spec: *"**Twins**: the profile's 10 cameras (eye-8 + bow/stern @40)."* `ship.json`'s
`cameras.elevated` is `[[0,40],[180,40]]`, measured by raycast deck coverage (30.17% → 49.58%).

**No tool on the twin route can express an elevation.** Three sites, all yaw-only, all
hardcoded:

| tool | site | what it does |
|---|---|---|
| `verify/turn_render.py` | :155–158 | `cam.location = (mid.x + r·sin θ, mid.y − r·cos θ, **mid.z**)`, `rotation_euler = (90°, 0, θ)`. The camera is always at the mesh's mid-height looking horizontally. **There is no elevation argument.** |
| `silhouette_masks.py` | :120 | `dtc = [sin θ, −cos θ, **0.0**]` |
| `project_twins.py` | :316 | `cam_axes(deg)` returns `[sin θ, −cos θ, **0.0**]`; `--view IDX=PATH` derives `yaw = IDX × step` and carries no elevation channel; `up` is hardcoded `[0,0,1]` |

So an elevated twin cannot be **rendered**, cannot have its **control mask** built, and — the
decisive one — **cannot be projected even if the first two were solved.**

**This is the spec's own primary-finding test firing:** *"A change required anywhere outside
those two files is a primary finding."* It is not expressible in `ship.json`, because a profile
value must bind to a flag and **there is no flag to bind to.**

**What the architecture does instead, and why this may be a spec slip rather than a gap.** E08
reached its elevated cameras through the **brush**, not through twins: `texpass_iter emit
--yaw --el` supports arbitrary elevation and produced `job_y+090_e+00`-style jobs, and
`texpass_brush` / `brush_cloud_step` consume them. Stage 1 (twins → projection) is eye-level by
construction; stage 2 (strokes) is where elevation lives. The ship's elevated pair was measured
in Task 4a for **deck coverage**, and the spec's own strokes bullet says stroke cameras are
*"derived from the hole map… measured, not inherited"* — which is where a bow/stern-at-40 camera
would arrive on the E08 pattern.

**The ruling this needs, stated as a choice and not as a recommendation:**

1. **Twins are the eye-level eight**, and the elevated pair reaches the ship through the stroke
   stage as it did on the character — no code change, `ship.json` unchanged, and the spec's
   sentence is corrected in place; **or**
2. **Elevated twins are in scope**, and elevation is added to all three tools with byte-identity
   anchors on the character path, the way `--fit-axis` was landed in Step 0 — a Step-0-class
   work item, not a mid-arm edit.

Reading (1) leaves H2 standing; reading (2) falsifies it. **I am not choosing which**, because
the choice decides what Arm T's baseline measures and therefore what the twin-baseline halt is
a baseline *of*.

## Finding 2 — an in-tool ANDON fires on `restylize_views` the moment the ship profile loads

```
AssertionError: ANDON: profile ship.json names 'aspect' for restylize_views.py, which has
no such argument. A profile value that does not reach its tool reads as configuration and
does nothing - that is the failure this system exists to prevent.
```

`ship.json` declares `restylize_views.py: {"aspect": "1066,1024"}`. **`restylize_views.py` has
no `--aspect` flag**, and the reason is that it needs none: `grep` for `752`, `1024`, `aspect`,
`resize` and `.size` in that file returns **zero occurrences**. It reads the render and the mask
at whatever size they arrive and never reasons about the frame. The aspect reaches it through
its inputs, which `turn_render` and `silhouette_masks` already frame from the profile.

**This blocks Arm T at its first command** — `restylize_views --emit-only` builds the control
images, and the twin generation cannot start without them.

The static form of the same defect, mechanically:

```
$ e04_profile_check.py --profile profiles/ship.json --tools tools
[chk] ship.json: 14 values checked against 6 tools
[chk] NOT A PURE RELOCATION - 7 mismatches:
[chk]   verify/turn_render.py  w            source default 752 != profile value 1066
[chk]   silhouette_masks.py    tag          source default 'w3clay' != profile value 'galleonclay'
[chk]   silhouette_masks.py    aspect       source default '752,1024' != profile value '1066,1024'
[chk]   project_twins.py       aspect       source default '752,1024' != profile value '1066,1024'
[chk]   texpass_iter.py        thin-extent  source default 0.0 != profile value 0.01
[chk]   restylize_views.py     aspect       no such flag in the tool          <-- THE DEFECT
[chk]   cull_unseen.py         production   default '...' not evaluable
EXIT=1
```

**Six of those seven rows are correct and expected** — a *ship* profile is supposed to differ
from a character's defaults; that is what a profile is for. The checker was written to prove
`character.json` is a **pure relocation**, and against the ship it answers a different question.
Only the `restylize_views` row is a defect, and only `cull_unseen`'s row is a checker limitation
(its default is an expression the static reader cannot evaluate).

**Ledger note on why this was not caught earlier, not as blame but so the gap is closed:**
Ruling 12 ratified *"PURE RELOCATION at 64 values across 11 tools"* — that run was
`--profile profiles/character.json`. **Nothing has ever pointed this checker at the ship
profile.** The purity gate proves the character's values are relocations; it does not prove the
*ship's* values reach their tools, which is a second question the same instrument answers for
free. Running it per profile is one line.

**The remedy is unambiguous but it is still a post-ANDON edit, so it is proposed and not
applied:** delete the `restylize_views.py` block from `ship.json`. It changes no behaviour —
the value never reached anything — and the guard's own error text names deletion as the
principle. `ship.json` is one of the two files the spec allows to change, so this is *not*
Finding 1's class.

## Finding 3 — the ship profile renders in the framing mode Ruling 11 did NOT adjudicate

`ship.json` carries **no `fit-axis` and no `margin`** for `turn_render` or `silhouette_masks`,
so a profile-only invocation takes the code default `height`. Anchor 1c — the thing Ruling 11
adjudicated — ran at **`--fit-axis width`**. The profile as written does not reproduce the
adjudicated mode.

Measured just now, both modes, same mesh, same 1066×1024 frame, geometry against geometry
(`e04_frame_agree.py`, bound 0 px):

| view | **height** (what the profile gives) | **width** (what Ruling 11 adjudicated) |
|---|---|---|
| 0 | 0 px | 0 px |
| 1 | 1 px | **1 px** — hit 321,219 vs mask 321,218 |
| 2 | 0 px | 0 px |
| **7** | **2 px** | **0 px** |

The width column **reproduces Ruling 11 to the digit** — *"one pixel of 321,219 with an unmoved
centroid"* — which is a free replication of the adjudicated anchor on a fresh invocation. The
height column puts **2 px on view 7 where width puts 0**, and Ruling 11 was explicit that the
bound stays 0 and *"the next nonzero halts again and gets its own ruling."*

**The good news is the size of it, and it is worth banking:** the two modes differ by
**0.046%** in extent (h_ext 1.202935 vs 1.202382) and their silhouette bboxes are identical on
six of eight views, differing by 2 px on views 0 and 4 (884 vs 886). That is because the frame
width **1066 was itself derived from the mesh's own aspect** (0.99866 / 0.95975 = 1.04054;
1066/1024 = 1.04102), so the two conventions nearly coincide by construction on this subject.
**The 4.68% catastrophe the fit-axis work was built to prevent is not lurking here** — but the
mode is still not the adjudicated one, and 2 px is still not 0.

**The margin question dissolves rather than needing a decision.** `ship.json`'s
`_still_suspended` records a *"derived margin 1.2528"* alongside the claim that width-fit
*"cannot be expressed as a profile value"* — **that note is stale**, written before Step 0
created `--fit-axis` and `--margin`. And the derived 1.2528 was never used: the width run above
uses the **default 1.204** and reproduces the adjudicated anchor exactly. So the correction is
`fit-axis: "width"` on both tools, **no margin entry**, and the stale note struck.

Proposed, not applied, for the same reason as Finding 2.

### A fourth item, minor and recorded rather than raised

`ship.json` carries `tag` for `silhouette_masks` (`galleonclay`) but not for `turn_render`,
which defaults to `view`. Every recorded invocation passes `--tag` explicitly, so nothing has
ever depended on it; noted because the twin prompt file keys on input stems and would move with
the tag.

---

## What was done anyway, because no ruling changes it

Both files `ship.json` has carried as `REQUIRED, NOT WRITTEN` since Task 4a are now written.
Both are transcriptions of results already measured and ratified — no threshold is invented in
either.

- **[canon/E04-galleon-palette.json](../../canon/E04-galleon-palette.json)** — the two bands
  from Task 4d, ratified in Ruling 8. Warm `50–100` MEASURED (span 62–88, 8 clusters, 73.6% of
  the ship). Blue `273–301` **SUSPENDED** with its numerator and denominator (2 clusters,
  3.69%) and the ±10° margin named as a convention. **Both gate bounds `null`**, per the spec.
  Chroma floor 12.0 carried as **inherited**. Three things are written into it that a run must
  not be allowed to forget: the ratified pair's own baseline through this gate (5,168 px /
  1.622% / largest CC 904, a hull shadow at h 45.9 C\* 13.1 — context, not a threshold); the
  instruction to report totals **both ways** for the suspended blue band; and **G7 has no
  band** — Arm G7's red landed at h 41–45, below the warm band's 50 edge, on bands derived from
  an image where G7 had not landed. Widening to admit it would be deriving a band from the
  result it judges, so it is recorded and left.
- **[docs/experiments/E04-twin-prompts.json](E04-twin-prompts.json)** — eight eye-level stems,
  one constant identity string, with the two authorised deltas from the pair's prompt: **G6
  gilded** (Ruling 7, the Director's amendment) and **G7 head-noun** (Ruling 9 — *regardless* of
  how Arm G7 measured, which is what both pre-registered branches say). The inherited
  per-view rule is applied and its application argued: this subject has no view-specific
  *anatomy* words, only material words, and the rule says material words stay byte-identical
  across views — so one constant string is the rule, not an exception to it.

Diagnostic artifacts, all local, all cheap, none of them an arm:
`E04_armT_diag/{clay_profileonly,clay_width,masks_profileonly,masks_width}` — the eight
eye-level silhouettes at 1066×1024 in both framing modes, and views 1/7 clay in both.

## What is NOT done

No twin exists. No control image was built. No cloud call was made for Arm T (Arm G7's single
0-credit generation is the session's only submission). Nothing was projected. `ship.json` is
**unmodified** — every proposed correction above is in this document and in none of the code.

## The three questions a ruling needs to answer

1. **Twins at eight cameras or ten?** If ten, elevation is a Step-0-class work item across
   three tools with character byte-identity anchors, and H2 is falsified. If eight, the spec's
   sentence is corrected in place and the elevated pair reaches the ship through the stroke
   stage as it did on the character.
2. **Strike `restylize_views.py` from `ship.json`?** The key cannot reach its tool and the tool
   needs no such knob.
3. **Add `fit-axis: "width"` to `turn_render` and `silhouette_masks` in `ship.json`, with no
   margin entry, and strike the stale `_still_suspended` framing note?** The width mode is the
   one Ruling 11 adjudicated and it reproduces that anchor to the digit.

A fourth, smaller: should `e04_profile_check.py` run against **every** profile as a standing
step, not just the character's? It answers a different and useful question per profile, and it
would have caught Finding 2 before this session.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every finding is a file:line or a tool invocation with its full output; the framing comparison is two runs of one instrument differing in one flag |
| ANDON_AUTHORITY | **3** | The halt is the deliverable. An ANDON fired and was not worked around; a second gate (bound 0 px) fired at 2 px and was not tuned; no proposed correction was applied to any file the guards guard |
| NAMED_COMPENSATORS | **3** | No spend, no generation, no projection. Every write is a new file; `ship.json` and all route tools untouched. Undo = delete `E04_armT_diag/` and two new fixtures |
| DECOMPOSE_BY_SECRETS | **3** | This report IS that standard's test result: the arm asked for something that cannot live in the profile, and that is Finding 1 rather than a quiet edit |
| UNCERTAINTY_GATED_HUMANS | **3** | Three questions posed as choices with their consequences, none with a recommendation attached where the choice changes what the experiment measures |
| EXTERNAL_VERIFIER | **2** | Findings 2 and 3 come from tools the executor did not write asserting against sources their authors did not control — the profile loader against the tools' own argument tables, and the frame-agreement check against two independent implementations of one camera convention. `skip:` on a second model |
