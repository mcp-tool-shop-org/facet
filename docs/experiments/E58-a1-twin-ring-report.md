# E58 report — the A1 twin ring: the first spend, behind the gate, over an anchor

**Executor seat (Sonnet), background agent. Charter:
[E58-a1-twin-ring-kickoff.md](E58-a1-twin-ring-kickoff.md). Written as-you-go, uncommitted —
the advisor commits by pathspec after review.**

This document reports measurements only. It does not judge whether any image, mesh, or
control is good — that is the Director's call. Words like verified/shipped/works/decisive/
validated/proven do not appear below in that sense.

**Ceiling: 11 generations (1 anchor + 8 ring + up to 2 re-rolls). Live tally at the top of
every section below.**

**Stage order actually run, and why it differs from the charter's A-B-C-D-E-F-G prose
order**: the dispatch's own text states "Zero generations happen before Stage B's refusal
demonstration is in your report" — this overrides the charter's plain lettering for the
*spend* action specifically (Stage A is a spend, Stage B is not). Actual order: MCP
reachability check -> Stage A prep (no spend: graph extraction, topology check, dry_run,
catalog check) -> **Stage B complete, in full, before any spend** -> Stage C -> Stage D ->
[Stage A real submission next] -> Stage E -> Stage F -> Stage G.

---

## MCP reachability — VERIFIED FIRST

`comfy-cloud`, `facet-record`, `facet-measure` MCP tool schemas all loaded successfully via
`ToolSearch` at session start (`estimate_credits`, `submit_workflow`, `run_saved_workflow`,
`get_job_status`, `wait_for_job`, `get_output`, `list_saved_workflows`, `upload_file`,
`get_saved_workflow`; `record_query`, `record_get`, `record_build`, `record_verify`;
`anchor_check`, `measure_report`, `texel_provenance`). **Full arc proceeds** — the
charter's Stage-E-halt fallback (submission-ready artifacts enumerated for the advisor to
submit) is not needed.

---

## MAJOR FINDING — the charter's Stage B premise is stale, verified not assumed

The charter's "What binds" section states, citing E54 (2026-08-17): *"E54 measured three
doors with no canon binding, and `e12_pair_cloud_step` — which authors the paid twin
graph — is one of them. No submission happens through an unbound door."* This was TRUE
when E54 measured it (E54's own census table, task 3, row 4: router column "**NO**").

**Directly verified against HEAD (commit `b9cd53c`) — it is no longer true.**
`tools/diagnostics/e12_pair_cloud_step.py` at HEAD calls `canon_gate.require_canon()` at
lines 104-109, before the graph dict is built (line 125) and before `--out` is written
(lines 252-253), wrapped `except canon_gate.Andon as e: raise SystemExit(str(e))`
(fail-closed, `raise` not `assert` — confirmed by grep: zero bare `assert` statements
anywhere in the file). `git diff HEAD -- tools/diagnostics/e12_pair_cloud_step.py` returns
**empty** — this is committed history, not uncommitted work from this or a prior seat.

**Why the premise went stale.** E54's own report names "two seats live" — its own census
fed directly into a concurrent "router round" that shipped as v0.6.0 (`79b8fb6`, "the canon
becomes data, the gate stands in front of the money") and v0.7.0 (`c72f66a`/`32b139f`, "the
gate closes fail-closed at every authoring site"). **The v0.7.0 release notes state
explicitly**: *"Wired at restylize_views, texpass_brush, brush_cloud_step ... and
e12_pair_cloud_step, which authors the paid twin graph."* The E58 charter (written
2026-08-18, one day after E54) cites E54's finding without re-verifying it against the
v0.6.0/v0.7.0 commits that closed the exact hole E54 named — the CLAUDE.md law in direct
action: *"An inherited claim is a hypothesis wearing a fact's clothes."*

**There is already shipped test coverage for exactly this door**: `tests/test_t94_fail_closed.py`
has `test_t94_e12_without_escape_writes_nothing` and
`test_t94_e12_galleon_escape_is_named_in_output`, both PASSING under the repo's pinned
interpreter (confirmed this session — see the interpreter trap below).

**Consequence**: Stage B's "bind the door" instruction is not needed — the door is already
bound. The demonstration is still run, aimed at A1 specifically (no prior test exercises
A1's own canon through this door).

**Environment trap hit once, self-caught**: the bare `python` on PATH is Python 3.14 with
no `open3d`/`mcp`/`cv2` installed. Running `tests/test_t91_canon_in_path.py` /
`test_t97_canon_bind.py` under it produced the repo's own `E17 Ruling 2` ANDON ("this
interpreter cannot import open3d, mcp, cv2, record_index"), refusing rather than silently
misreporting. Re-ran with the pinned interpreter
(`E:\AI-Models\trellis2-env\Scripts\python.exe`) — 22/22 passed.

---

## Stage B — the door is bound (spend: 0). COMPLETE.

Working files: `E:\AI\training\facet_E58\stageB\` (`build_fixtures.py`,
`prompts_intact.json`, `prompts_stripped.json`, `profile_demo.json` — a throwaway
demonstration profile, explicitly NOT Stage D's real values —, `transcript_stripped.txt`,
`transcript_intact.txt`, `test_stageD_prompt.py`).

### Run 1 — N3 stripped, expect REFUSE naming the phrase

Fixture: A1-RECIPE.json's ratified `positive_text`, minus `", an umber sash"` (N3), run
through `e12_pair_cloud_step.py --key K0 --prompts prompts_stripped.json --profile
profile_demo.json --render-name r.png --control-name c.png --out out_stripped.json
--subject A1` (no `--no-canon`).

```
ANDON: canon does not cover ratified prompt: missing=[{'surface': 'sash', 'phrase': 'an umber sash'}]
forbidden=[] unlicensed=[{'span': 'full body character concept single figure centered standing
relaxed pose facing camera arms slightly away body hands empty open feet planted visible soft
even studio lighting warm colour shadows over'}]; unratified named not required: []
```
rc != 0, `--out` NOT written (`out_stripped.json` confirmed absent by `ls`). **REFUSE, naming
the missing phrase exactly** — the demonstration the charter asked for.

### Run 2 — restore, full intact ratified prompt

Same command, `--prompts prompts_intact.json` (byte-restored, no strip).

```
ANDON: canon does not cover ratified prompt: missing=[] forbidden=[]
unlicensed=[{'span': 'full body character concept single figure centered standing relaxed pose
facing camera arms slightly away body hands empty open feet planted visible soft even studio
lighting warm colour shadows over'}]; unratified named not required: []
```

**Still refuses — for a DIFFERENT reason than "restore and pass".** `missing=[]` (every
ratified phrase present, confirmed — this is the SAME text E57's Gate 0 already hit 18/18),
but `unlicensed` is non-empty. Read `canon_gate.check_prompt()` / `unlicensed_residue()` /
`licensed_phrases()` directly (not inferred): `ok = (not missing) and (not forbidden) and
(not unlicensed)` — **unlicensed blocks exactly like missing does**, per the function's own
docstring: *"Unlicensed is a refuse. There is no warn."*

**This is a genuine, structural fact about A1's canon, not a bug.** The reference's raw
`positive_text` contains pose/lighting staging prose ("Full-body character concept, single
figure centered, standing in a relaxed A-pose facing the camera, arms slightly away from the
body, hands empty and open, feet planted and visible" and "soft even studio lighting with
warm colour in the shadows") that `A1-IDENTITY.md` itself already names *"generation
staging, not identity"* and that was deliberately NOT promoted to a ratified `legal_clauses`
entry at ratification — only 4 of the staging phrases were (`stage_bg`, `stage_no_weapons`,
`stage_no_held`, `stage_clear_sil`). `licensed_phrases()` = every surface-occupant phrase
(any provenance) + `blocked_additions` + `legal_clauses` — 10 NAMED + `proportions` (mesh) +
`brushwork` (style, subsumed by `style_paint`'s longer phrase) + 8 `legal_clauses` = the
same 18 phrases Gate 0 checked, plus 2. The pose sentence was written for the ANCHOR's
txt2img generation (no ControlNet — text has to carry the pose); the RING's twins are
ControlNet-constrained (pose comes from the control image), so this sentence was never meant
to recur in the twin prompt.

### Consequence for Stage D, verified BEFORE committing anything

Composed a candidate twin prompt from exactly the 18 ratified phrases (10 NAMED + 8
`legal_clauses`) as a comma-separated list of noun phrases — the SAME convention already
proven for the dragon/beast (`profiles/beast.json`'s prompt: *"a winged dragon, deep
moss-green scaled hide, ..."* — E12 Ruling 9c, *"every element its own noun phrase"*), not a
copy of the reference's raw prose. Tested directly against the live mechanism
(`facet_E58\stageB\test_stageD_prompt.py`):

```
ok=True
missing=[]
forbidden=[]
unlicensed=[]
required=16
prompt_len=462
require_canon gated=True note=None
```

`required=16` (not 18): `check_prompt()`'s `required` counter is scoped to
`scope_surface_ids` (surfaces requiring a "prompt"-provenance occupant — 16 of A1's 19
surface rows, matching the census's own "16/16 ratified" reading), a narrower count than the
18 licensed *phrase strings* `unlicensed_residue` checks against. Both readings are reported
so neither is mistaken for the other.

This candidate string became `profiles/a1.json`'s `tools.restylize_views.py.prompt` and
every view's entry in `docs/experiments/E58-a1-twin-prompts.json` (Stage D, below).

---

## Stage A — prep (no spend yet; the real submission runs after Stage D, below)

### The most verbatim replay available: the literal original graph

`extract_recipe.py` (E57) pulled specific FIELDS out of the PNG's embedded
`info["prompt"]`. This arc instead pulled the WHOLE graph, unmodified
(`E:\AI\training\facet_E58\extract_full_graph.py`, reading `canon/A1_reference.png` via
PIL) to `E:\AI\training\facet_E58\reference\A1_full_graph.json` — 19 nodes, matching E57's
field-level extraction exactly: switch node `238:229` = `false` selects `steps=50`
(`238:224`) / `cfg=4.0` (`238:223`) / `UNETLoader 238:226
"qwen_image_2512_fp8_e4m3fn.safetensors"` (NOT the LoRA branch) at all three switches it
gates. **Zero ControlNet nodes anywhere in the 19-node graph** (trivially satisfies "no
ControlNet" — there is nothing to remove). This is the most defensible "verbatim" replay:
the literal graph that produced the reference, not a hand-rebuilt equivalent, submitted
byte-for-byte unmodified (not even `filename_prefix` touched).

### Link-topology check, per the E04 G7 law

`E:\AI\training\facet_E58\check_topology.py` — the same three checks
`e12_pair_cloud_step.py` runs on its own authored graph (self-links, dangling targets,
orphans unreachable from the output node), applied to the graph pulled from the PNG rather
than one this session built:

```
TOPOLOGY CHECK PASSED: E:\AI\training\facet_E58\reference\A1_full_graph.json
  nodes=19  links=22  reachable_from_60=19  orphans=0
```

Additionally ran `submit_workflow(..., dry_run=true)`: `{"status":"validated","warnings":
[],"submitted":false}`. Per the E04 G7 law this is a signal, not the guarantee (a dry_run
PASS did not catch E04's self-referencing link); the code-level topology check above is the
guarantee, and both agree.

### Venue catalog check — every model in the graph, present under its exact filename

`search_models` (all `source: "comfy-cloud"`, exact filename match):

| model | node role | present |
|---|---|---|
| `qwen_image_2512_fp8_e4m3fn.safetensors` | UNETLoader (active branch) | YES — diffusion_model |
| `qwen_2.5_vl_7b_fp8_scaled.safetensors` | CLIPLoader | YES — text_encoder |
| `qwen_image_vae.safetensors` | VAELoader | YES — vae |
| `Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors` | LoraLoaderModelOnly (inactive branch) | YES — lora |

`ComfySwitchNode` confirmed present in the venue's core node catalog (`search_nodes`,
`pack: "core"`). `get_server_info`: production, `cloud.comfy.org`, version 0.40.1,
authenticated (OAuth).

### `estimate_credits` — flagged, not taken at face value

```
0 credits - no paid API nodes found in this workflow.
```

The tool's own caveat: GPU and queue time are excluded from the total. This graph is a
local-OSS-model workflow (UNETLoader/CLIPLoader), billed by GPU-second on this venue, not a
metered partner API node — the class of cost this estimator is built to price. **"0
credits" here means "this estimator cannot price this workflow shape," not "this generation
is free."** The arc's ceiling accounting stays in GENERATION COUNT (per the charter), which
this finding does not change.

---

## Stage C — controls from the approved mesh (spend: 0). COMPLETE.

### Frame derivation — MEASURED, not inherited

`tools/diagnostics/e12_frame.py` (the recorded Gate-0 frame deriver, same tool used to
derive the beast's/ship's/longsword's own frames) against
`facet_E57\mesh\A1_1024_cascade_seed42.glb`:

```
[frame] A1  extent (Blender xyz) x=0.5611 y=0.2214 z=1.0012
[frame]   widest AXIS / height   = 0.5604   (E04's quantity: max(ex,ey)/ez)
[frame]   worst of 8 YAWS / height = 0.5604   at view 0   (+0.00% over the axis number)
[frame]   1024 * 0.5604 = 573.9 -> round up to /16 -> RENDER 576x1024
[frame]   horizontal margin at the worst view: 1.2085 (vertical 1.2040 by construction)
```

**A1's own derived frame is 576×1024 — not W3's inherited 752×1024**, which is what
E57's own clay/flat renders used (no `--profile` was passed at that stage, so
`turn_render.py`'s bare defaults applied). The coverage ANDON built into `e12_frame.py`
(checked in the opposite direction from the derivation, so it can actually fail) did not
fire. Worst yaw is view 0 (front), essentially equal to the axis-only ratio — this
character has no diagonal-worse-than-axis effect (unlike the dragon's wingspread case
`e12_frame.py`'s own docstring names).

### Renders and masks

8-view clay render, `turn_render.py` via PowerShell/Blender 5.2, at 576×1024, height-fit,
margin 1.204 → `facet_E58\controls\clay\a1clay_{0-7}.png`, all 8 present.

8-view exact raycast silhouette, `silhouette_masks.py` — needs a `prep_uv.glb` at
`--prep DIR`. **Disclosed, not concealed**: A1 has not been through `bake_hero_prep.py`
(the UV-unwrap/atlas-bake stage — texpass/painting scope, explicitly out of this arc). The
raycast core (`RaycastingScene` over vertices+faces) does not need UVs at all, so A1's raw
mesh was copied byte-identical to `facet_E58\controls\prep\prep_uv.glb` (sha256 confirmed
identical to `facet_E57\mesh\A1_1024_cascade_seed42.glb`,
`cdf276e794fe3de119c4ca9a328f43fe39d0f03e27c5fb0044ba2a0d93573ade`) — no bake step run, just
a raycastable copy at the path the tool expects:

```
[sil] mesh 711,524 verts  990,679 tris   v_ext 1.203441  h_ext 0.676936
[sil] view 0  yaw    0.0deg  29.662% of frame  bbox 476x850  -> a1sil_0.png
[sil] view 1  yaw   45.0deg  27.021% of frame  bbox 352x850  -> a1sil_1.png
[sil] view 2  yaw   90.0deg  18.123% of frame  bbox 188x850  -> a1sil_2.png
[sil] view 3  yaw  135.0deg  27.123% of frame  bbox 349x850  -> a1sil_3.png
[sil] view 4  yaw  180.0deg  29.662% of frame  bbox 476x850  -> a1sil_4.png
[sil] view 5  yaw  225.0deg  27.021% of frame  bbox 352x850  -> a1sil_5.png
[sil] view 6  yaw  270.0deg  18.123% of frame  bbox 188x850  -> a1sil_6.png
[sil] view 7  yaw  315.0deg  27.123% of frame  bbox 349x850  -> a1sil_7.png
```

No ANDON fired (each view's silhouette percent-of-frame is within the tool's
[0.5%, 60%) sanity band). Front/back (views 0/4) and the two profile views (2/6) read
identical bbox pairs — consistent with a front/back-symmetric standing figure, this
mesh's own geometry, not assumed.

### Canny+contour controls, via the recorded route (`restylize_views.py --emit-only`)

`restylize_views.py --emit-only --inputs <8 clay> --masks <8 silhouettes> --canon
canon/a1.surfaces.json --subject A1 --prompt "<the Stage-B-verified 18-phrase candidate>"`:

```
[restyle] a1clay_0: control image 24,453 px (canny 18,295 + contour 10,699); figure mask 29.7%
[restyle] a1clay_1: control image 20,882 px (canny 15,805 + contour 8,882); figure mask 27.0%
[restyle] a1clay_2: control image 12,547 px (canny 9,403 + contour 5,537); figure mask 18.1%
[restyle] a1clay_3: control image 15,981 px (canny 11,128 + contour 8,489); figure mask 27.1%
[restyle] a1clay_4: control image 17,920 px (canny 11,747 + contour 10,699); figure mask 29.7%
[restyle] a1clay_5: control image 16,134 px (canny 11,068 + contour 8,882); figure mask 27.0%
[restyle] a1clay_6: control image 13,245 px (canny 10,118 + contour 5,537); figure mask 18.1%
[restyle] a1clay_7: control image 19,177 px (canny 14,354 + contour 8,489); figure mask 27.1%
```

No ANDON fired (every view's contour count exceeds the tool's 500px floor). Canon gate ran
clean — no `[canon] UNGATED` / unratified line printed, consistent with the 16/16 ratified,
zero-missing, zero-unlicensed reading Stage B already established for this exact prompt.

**Disclosed as a first-run operating point, not measured**: canny-low/high used the tool's
own defaults (0.4/0.8) — no subject-specific canny-sensitivity sweep was run (the E12/E14
dragon/longsword precedent for deriving a ruled pair is out of this arc's charter scope).
Flagged in `profiles/a1.json` and here: the dragon's own record shows grey-on-grey clay
commonly needs a MUCH lower pair (0.05/0.10 dragon, 0.10/0.25 longsword) than this tool
default. A future arc may need to measure and rule this for A1 the same way.

### Gate C — bbox-check every control against its silhouette + sha256 every byte

`facet_E58\controls\gate_c_check.py`:

```
view 0  control_bbox=(49, 86, 478, 852)  mask_bbox=(50, 87, 476, 850)  sil_report_wh=[476, 850]  ok=True
view 1  control_bbox=(90, 86, 354, 852)  mask_bbox=(91, 87, 352, 850)  sil_report_wh=[352, 850]  ok=True
view 2  control_bbox=(193, 86, 190, 852)  mask_bbox=(194, 87, 188, 850)  sil_report_wh=[188, 850]  ok=True
view 3  control_bbox=(95, 86, 351, 852)  mask_bbox=(96, 87, 349, 850)  sil_report_wh=[349, 850]  ok=True
view 4  control_bbox=(49, 86, 478, 852)  mask_bbox=(50, 87, 476, 850)  sil_report_wh=[476, 850]  ok=True
view 5  control_bbox=(132, 86, 354, 852)  mask_bbox=(133, 87, 352, 850)  sil_report_wh=[352, 850]  ok=True
view 6  control_bbox=(193, 86, 190, 852)  mask_bbox=(194, 87, 188, 850)  sil_report_wh=[188, 850]  ok=True
view 7  control_bbox=(130, 86, 351, 852)  mask_bbox=(131, 87, 349, 850)  sil_report_wh=[349, 850]  ok=True
GATE C: PASSED (8/8 views, bbox within margin, all sha256 recorded)
```

Every control bbox sits within ~1-2px of its own mask's bbox (consistent with the
morphological-gradient contour's dilation at `contour-width=3`), and every mask bbox
exactly matches `silhouette_masks.py`'s own reported bbox. **Gate C: PASSED.** All 16
control+mask bytes sha256'd into `facet_E58\controls\ctrl\gate_c_report.json` (full hashes
also on disk; omitted here for length — see that file).

---

## Stage D — the A1 profile (spend: 0). COMPLETE.

### `profiles/a1.json` authored

Full file at `E:\AI\facet\profiles\a1.json`. Every recipe value (seed/steps/cfg/denoise/
lora-w/cn-strength) is disclosed as a **FIRST-RUN OPERATING POINT** at the studio's
established twin-restylize values (W3 `profiles/character.json` + longsword
`profiles/prop.json` both cite E08 for seed=770700/steps=20/cfg=2.5; W3's own twin
denoise=0.92, lora-w=0.75 [the saltroad house style — NOT the beast's Director-ruled 0.0,
which followed a REJECTED pair A1 has no equivalent of yet], cn-strength=0.9) — **not**
values measured on A1 itself, since there is no prior A1 generation to relocate values from
(unlike W3's own profile, which extracted an ACCEPTED asset's own recipe). Negative text is
`canon/A1-RECIPE.json`'s own CJK negative, verbatim, per the charter's explicit "negative
from the recipe" instruction — the first subject whose negative carries its own recorded
provenance rather than the studio-wide generic negative.

Seeds pinned NOW, before any submission: **all 8 views share seed 770700** (the studio's
twin-generation seed, W3/longsword lineage) — no per-subject seed variation has precedent
in this repo's prior twin generations; the render+control pairing differentiates each view,
not the seed. Recorded explicitly in the profile and here, per "pin per-view seeds now,
record them." The ONE allowed spec-violation re-roll (if triggered at Stage F) uses a NEW,
recorded seed and is not this value.

`docs/experiments/E58-a1-twin-prompts.json` authored: all 8 views carry the IDENTICAL
18-phrase prompt (composed and verified in Stage B). **Disclosed deviation from the
W3/dragon per-view-drop convention** ("a rear camera is never told about a beard"): the
charter's own Stage D text asks the twin prompt to carry EVERY ratified phrase, not a
per-view-visible subset — read literally rather than silently importing the older
per-subject convention. Flagged for a future ruling.

### CENSUS_ROWS pairing updated

`tools/canon_gate.py`: A1's row 4th field moved `"profiles/character.json"` (E57's
placeholder, W3's own profile, paired only because it was the one CENSUS_ROWS-shaped file
that existed) → `"profiles/a1.json"` (A1's own).

**`census` output, verbatim, before/after** (interpreter:
`E:\AI-Models\trellis2-env\Scripts\python.exe`):

```
subject      named   occupancy   ratified   prof_hit surfaces
...
A1              10       16/16      16/16      10/10 canon/a1.surfaces.json     <- AFTER (was 0/10)
```//

**`resolve --subject A1`, verbatim, complete, ASCII:**
```
E:\AI\facet\canon\a1.surfaces.json
```
Exit code 0.

**Stage D's own completion condition, verified**: `canon_gate` resolves A1 against
`profiles/a1.json` with **zero missing ratified phrases** — `prof_hit` moved 0/10 → 10/10,
and the fuller `check_prompt()` reading (Stage B) already showed `missing=[]`,
`forbidden=[]`, `unlicensed=[]`, `ok=True` for this exact prompt.

### Tests, in the same change-set, collection-count-neutral by design

`tests/test_t91_canon_in_path.py::test_t91_census_does_not_invent_surfaces` extended IN
PLACE (not a new function — deliberately, per the T34-cascade finding below) with:
`rows["A1"]["profile"] == "profiles/a1.json"`, `profile_named == 10`, `profile_hits == 10`,
plus a full `check_prompt()` pass (`ok`, `required == 16`) mirroring
`test_t91_longsword_profile_covers_its_canon`'s shape but folded into the same function.

**Why not a new test function, disclosed**: read `tests/test_t34_front_door_counts.py` in
full before deciding. T34's pins are ALL derived DYNAMICALLY from a fresh
`pytest --collect-only` subprocess at test-run time, cross-checked against hardcoded digits
on README.md (×8 languages), SHIP_GATE.md, site-config.ts, and handbook pages. **Any new
collected test item anywhere in the suite would require regenerating all eight README
translations in the same commit** (the studio's translation rule: Sonnet kickoff sessions
defer translation runs to the user/advisor) — far outside this arc's charter. Extending an
existing, non-parametrized test function in place — E57's own precedent for A1's first test
addition — adds zero new collected items.

**Verified directly, not assumed**: `pytest --collect-only -q` reports **1339** both before
and after this edit (E57's own baseline was 1338; the +1 is the E54/E57 report files already
in the corpus at this seat's start, unrelated to this seat's own edits).

**Full local verification, all green**:
- `tests/test_t91_canon_in_path.py`: 12/12 passed (includes the extended test).
- `tests/test_t97_canon_bind.py` + `test_t92_canon_router.py` + `test_t93_canon_worksheet.py`
  + `test_t94_fail_closed.py`: 48/48 passed — no cross-contamination from the CENSUS_ROWS
  edit, and both e12-specific fail-closed tests still pass.
- Full hermetic suite (`-m "not artifacts"`): **1 failed, 1284 passed, 54 deselected**
  (523.93s). Read from the printed tally line, not the shell wrapper's own reported exit
  code — the backgrounded command's exit code read 0 because its last piped command
  (`wc -l`) succeeded regardless of pytest's result, the exact "pipe exit codes lie" trap
  the dispatch names.

### Finding, out of this arc's scope: a pre-existing CRLF defect from E57, now committed

The one hermetic failure, `test_t06_no_crlf_in_tracked_text_files`, names
`canon/A1-RECIPE.json` and `canon/A1-palette.json` — both `worktree w/crlf` despite
`.gitattributes` declaring `eol=lf` for them, consistent with Python's `json.dump()`
through a plain `open(path, "w")` on Windows (translates `\n` to `\r\n` without
`newline=""`; both files were written this way at E57). **Confirmed not touched by this
session**: `git status --short -- canon/A1-RECIPE.json canon/A1-palette.json` returns
empty (no diff against HEAD). **Not fixed here** — outside E58's chartered stages, not
this seat's file, and a line-ending rewrite changes the files' own bytes for a repair this
arc was not asked to make. Reported for the advisor.

### A commit landed mid-session, from the advisor's own seat

Three new commits appeared between this session's start and the hermetic-suite check:
`bdad934` ("E57: A1, the reference-first exemplar..."), `a09ac3c` ("Seeded fixture follows
the law row it names..."), `40df0ac` ("Index rebuilt over E57+E58..."). The ~20 files dirty
at this session's start (CLAUDE.md, 8 READMEs, SHIP_GATE.md, docs/advisor-kickoff.md,
docs/experiments/README.md, docs/index/conventions.json, docs/instrument-census.*, 2 site
files, all of E57's `canon/` outputs, E57's kickoff+report, E58's kickoff) are now clean.
**No conflict with this seat's own edits**: `git diff --stat` on `tools/canon_gate.py` /
`tests/test_t91_canon_in_path.py` against the new HEAD shows clean diffs (12 / 28 changed
lines), not a garbled merge, and every file this seat read and relied on shows **zero**
diff against the new HEAD (same bytes throughout this session) — nothing measured needs to
be redone.

---

## Stage A — real submission (spend: 1). Ceiling: 1/11 generations spent.

### Submission

`submit_workflow` on the untouched `A1_full_graph.json` (byte-for-byte identical to what
was dry-run and topology-checked above — not even `filename_prefix` changed), `confirm:
true`. Response: `{"prompt_id":"9d9d6a9f-39a0-433d-afcc-24874d22f604","lifted_from_save":
false,"status":"succeeded","warnings":[]}` — **"succeeded" here means the submission was
accepted**, not that generation had finished (`get_output` immediately after returned
`job.not_ready`). `get_job_status` showed `in_progress`; `wait_for_job` timed out once at
~25s (still `in_progress`) then returned `completed` on the second call.

Output retrieved (`get_output`, `client_os: windows`) and downloaded via the tool's own
emitted `curl.exe` command, redirected to
`E:\AI\training\facet_E58\reference\A1_anchor_output.png` (1,615,366 bytes) instead of the
suggested Downloads path.

### Gate A — measurement

`E:\AI\training\facet_E58\gate_a_measure.py` against `canon/A1_reference.png`:

```
anchor sha256=2d0f45a4e254a4def0502d2e26f96f8b61c4a67629d9ad3bcaea66c7f26f013e
reference sha256=9417cd6492df34354e5d3f3d7809bf89ddd074f5b1b18725c166a59b97b48dde
byte_identical=False
anchor size=(1136, 1472)  reference size=(1136, 1472)
GLOBAL dE: mean=0.0000 median=0.0000 p90=0.0000 p95=0.0000 p99=0.0000 max=0.0000 std=0.0000
ELEVATED (dE > 1.0000, 3x global median): 0 px (0.0000% of frame)
COARSE FIGURE-REGION (bbox 198,41,914,1376, E57 human-read, NOT a segmentation):
  inside : mean=0.0000 median=0.0000 p95=0.0000 max=0.0000 (n=955,860)
  outside: mean=0.0000 median=0.0000 p95=0.0000 max=0.0000 (n=716,332)
```

Sizes match exactly (1136×1472 both — the same 8x-latent-rounding behaviour E57 already
found: the declared 1140-wide latent decodes to 1136, reproducibly). File-level sha256
differs (PNG encoder metadata — this repo's own documented "a PNG hash mismatch is not
evidence a render changed"), so checked one level deeper: **the raw RGB pixel arrays are
byte-for-byte identical.**

```
pixel-array byte-identical (RGB): True
max abs channel diff: 0
num differing pixels (any channel): 0 / 1,672,192
```

**Zero differing pixels out of 1,672,192.** Every ΔE statistic (global, figure-region,
background-region) reads exactly 0.0000 because there is no pixel-level difference to
measure — this is pixel-perfect reproduction, not merely "uniform residual within the
0.84-precedent scale." No spatial map is meaningfully non-blank; written anyway
(`gate_a_dE_map.png`) for the record.

### Gate A verdict: ACCEPTED

Pre-registered reading: *"byte-identical or uniform-residual ΔE at the 0.84-precedent
scale → anchor ACCEPTED, boundary recorded in every later report; concentrated/structural
residual → HALT."* Pixel-array identity is a stronger result than either branch of that
reading names (not merely within the 0.84-precedent scale — exactly zero). **ACCEPTED.**
Boundary recorded: this rig's replay of this exact graph, on this venue, at this time,
reproduces the reference's own pixels exactly — a materially better outcome than the
repo's prior hardware anchor (ΔE 0.84 against a 1.07 no-response floor), which is
recorded here as the comparison point per the standing law, not as a claim that this
result generalizes to every future replay.

### Venue model/version strings, beside the recipe's

| field | recipe (`canon/A1-RECIPE.json`) | venue catalog (`search_models`) |
|---|---|---|
| UNET | `qwen_image_2512_fp8_e4m3fn.safetensors` | same, `source: "comfy-cloud"`, type `diffusion_model` |
| CLIP | `qwen_2.5_vl_7b_fp8_scaled.safetensors` | same, `source: "comfy-cloud"`, type `text_encoder` |
| VAE | `qwen_image_vae.safetensors` | same, `source: "comfy-cloud"`, type `vae` |
| LoRA (inactive branch) | `Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors` | same, `source: "comfy-cloud"`, type `lora` |

Identical strings on both sides — consistent with (not proof of, but consistent with) the
pixel-perfect reproduction above. `get_server_info`: production, `cloud.comfy.org`, version
0.40.1.

---

## Stage E — the ring (spend: 8). Ceiling: 9/11 generations spent.

### Uploads and graph authoring

16 files uploaded (`upload_file`, 8 clay renders + 8 controls) — remote/hosted session, so
each returned a `curl.exe -X PUT` command run via PowerShell; all 16 succeeded, cloud names
captured in `facet_E58\controls\upload_names.json`.

`e12_pair_cloud_step.py` run 8 times (one per view), `--profile profiles/a1.json --subject
A1`, uploaded render/control names, `--prefix a1_ring_v{i}`. Every run: `[pre-flight] PASS
against a1.json: six recipe values equal the decided block; --prompts IS _fixtures.
twin_prompts and the graph's strings are that file's; 18 links resolve, no self-link, no
dangling target, no orphan.` Pinned values confirmed identical across all 8: seed 770700,
steps 20, cfg 2.5, denoise 0.92, lora_w 0.75, cn 0.9. Independently re-verified with this
arc's own `check_topology.py` (separate from the tool's internal check) — 8/8 pass, 15
nodes / 18 links / 0 orphans each. All 8 graphs sha256'd (`facet_E58\ring\graph_{0-7}.json`).

`estimate_credits` on the (structurally identical) graph shape: same "0 credits - no paid
API nodes found" result and the same GPU/queue-time-exclusion caveat as the anchor — noted,
not taken as a free-generation claim.

### Submission

`submit_batch` (per the tool's own guidance: "2+ independent generations in one request ->
call submit_batch ONCE"), all 8 as `submit_workflow` items, `confirm: true`:
`{"submitted":8,"failed":[]}`. `wait_for_batch` (2 calls, first timed out at 4/8 ready,
second returned all 8 `ready`, 0 `failed`). `get_batch_output` returned all 8 signed URLs;
downloaded via PowerShell to `facet_E58\ring\a1_ring_v{0-7}.png`.

### Gate E — per view, before any measurement

```
view 0: size=(576, 1024) expected=(576, 1024) OK
view 1: size=(576, 1024) expected=(576, 1024) OK
view 2: size=(576, 1024) expected=(576, 1024) OK
view 3: size=(576, 1024) expected=(576, 1024) OK
view 4: size=(576, 1024) expected=(576, 1024) OK
view 5: size=(576, 1024) expected=(576, 1024) OK
view 6: size=(576, 1024) expected=(576, 1024) OK
view 7: size=(576, 1024) expected=(576, 1024) OK
GATE E: PASSED (8/8 delivered frame == requested frame exactly)
```

No VAE-rounding mismatch on any view (576 is div-16-legal by construction, per Stage C's
own derivation).

---

## Stage F — measurement (spend: 0 unless re-roll; NONE spent)

### Registration IoU + painted fraction (keyed vs exact silhouette)

**Method, and its caveat, stated up front.** There is no exact-silhouette equivalent for
"what did the twin itself paint as figure" — that requires classifying the TWIN's own
pixels, which needs SOME keying. This repo's corner-median keying is retired after three
prior failures; the prescribed repair (CLAUDE.md) is a border-ring bilinear background fit.
Reused directly from E57 (`gate2_bbox_check.py.figure_bbox_border_ring`, imported, not
reimplemented) rather than commissioning a new method. **Reported as a diagnostic reading
of whether the model's visible output tracks the ControlNet's geometric constraint, not a
validated ground truth** — the same caveat E57 itself gave this method on the reference
image, which is a materially different background (studio backdrop painted fresh by the
model here, not the render tool's own uniform grey).

```
view  IoU     painted_frac  exact_frac   perim_px
0     0.8747  0.2925        0.2966       4153
1     0.9259  0.2693        0.2702       3498
2     0.7453  0.2045        0.1812       2253
3     0.9103  0.2715        0.2712       3354
4     0.8988  0.3020        0.2966       4153
5     0.8794  0.2811        0.2702       3498
6     0.4490  0.3526        0.1812       2253
7     0.8181  0.2810        0.2712       3354
```

No threshold invented (per the charter). **View 6 stands out**: IoU 0.4490 (the other seven
range 0.75-0.93), and its keyed painted fraction (0.3526) is nearly DOUBLE the exact
silhouette's own fraction (0.1812) — the keyed method found far more "figure" than the
geometry says should exist. This could mean the border-ring fit failed on this specific
view's backdrop (its own disclosed failure mode), or that the model painted content beyond
the exact silhouette, or genuine registration drift; distinguishing these is not something
this measurement can do alone, and no such distinction is claimed here.

### Off-palette, two units (never area alone, per the standing law)

**Structural caveat, load-bearing for reading every number below.** `canon/A1-palette.json`
was derived at E57 Stage 1 from the RAW reference image — the anchor's own recipe carries
`switch=false` (NO LoRA, confirmed Stage A). The ring's twins run through `lora-w: 0.75`
(the saltroad house-style LoRA) — the FIRST time any A1 image has been generated through
that LoRA. Every other ratified subject's palette (W3, galleon, beast, longsword) was
measured FROM an already-LoRA-styled image, so this gap is specific to A1: **the bands
below describe a non-LoRA reference; the twins being measured are the first LoRA-styled A1
images that have ever existed.** Bands derived at `facet_E58\stageF\a1_gate_bands.json`
(hue_centre +/- 10 deg per material, the studio's own named "CONVENTION, not a measurement"
— `canon/E04-galleon-palette.json`'s blue band precedent), chroma floor 12.0 unchanged.
Gate bounds NULL throughout (the E04-galleon precedent: no baseline exists until this
subject's own twins do) — `palette_gate.py --report-only`.

```
view  figure_px  offpal_px  offpal_%_AREA  blob_px  offpal_per_PERIM  blob_per_PERIM  dominant_hue      dominant_share
0     174,952    95,931     54.83%         20,524   23.10             4.94            340-350 deg       31%
1     159,375    51,922     32.58%         26,300   14.84             7.52            130-140 deg       49%
2     106,893    27,535     25.76%         11,276   12.22             5.00            10-20 deg         26%
3     159,976    99,514     62.21%         47,438   29.67             14.14           350-360 deg       62%
4     174,952    122,587    70.07%         98,478   29.52             23.71           350-360 deg       66%
5     159,376    97,819     61.38%         37,717   27.96             10.78           350-360 deg       66%
6     106,893    39,245     36.71%         17,512   17.42             7.77            350-360 deg       37%
7     159,976    102,102    63.82%         57,678   30.44             17.20           350-360 deg       36%
```

Both units reported per the charter and per CLAUDE.md's own law ("normalise a boundary
quantity by perimeter, not by area"); `palette_gate.py`'s own built-in `%` is area-based
and is reported as such, not silently treated as the perimeter reading.

**Far above this repo's own "clean" precedent** (5-104 px on clean views in the palette
gate's own founding record; the single confirmed contamination instance measured
4,882-5,068 px in one blob). Six of eight views show a DOMINANT off-palette hue in the
350-360 deg (red/magenta) band — a hue family covered by NONE of A1's ten derived bands
(all ten sit between 28.5 and 129.3 deg). Dominant-hue median RGB values across views are
consistently dark reddish-brown (e.g. `(85,33,52)`, `(66,34,42)`, `(70,35,43)`) — visually
consistent with shadow-toned skin or garment regions reading redder than the pre-LoRA
reference's own measured bands, though this sentence states what the numbers show, not what
caused them.

**No judgment is made here about whether this constitutes the charter's "material not in
the ratified canon."** The structural gap above (bands measured pre-LoRA, twins measured
post-LoRA, for the first time on this subject) means this measurement cannot by itself
distinguish "the LoRA's own house style shifts hue in a way the Director would consider
within spec" from "a genuine wrong-material spec violation" — that is exactly the
distinction CLAUDE.md reserves for the Director's eye ("a metric that cannot separate an
asset he rejected from one he accepted is not a metric," "canon is not a taste question to
be routed around... no metric approximates it"). **This seat does not trigger a re-roll.**
Spending one of the two reserved re-roll credits on this seat's own reading of these numbers
would be exactly the "tuning toward a number" the executor rules forbid. The finding is
reported in full, with the sheet, for the Director's/advisor's decision.

Full data: `facet_E58\stageF\stage_f_report.json`, `facet_E58\stageF\palette_report.json`,
per-view overlay PNGs at `facet_E58\stageF\overlay\`.

---

## Stage G — the Director's sheet

`E:\AI\training\facet_E58\build_e58_sheet.py` (adapted from E57's own sheet builder, same
ethic: native full-size files untouched on disk, this PNG an explicitly-downscaled
overview, provenance footer with sha256). Output: `facet_E58\sheets\E58_director_sheet.png`
(1892x1929) + `E58_director_sheet_manifest.json` (every source file's sha256).

Layout: reference shown once (front-on only — it has no per-view counterpart) | control x8 |
twin x8 (IoU + area off-palette annotated per view, the low-IoU view 6 marked) | E57's own
clay x8 shown beneath for silhouette-shape reference (explicitly labelled as a DIFFERENT
frame, 752x1024 vs this arc's 576x1024 — not a pixel-comparable row, a shape reference
only). Full-size per-view PNGs remain on disk, untouched, at the paths named in the
manifest. **The sheet reports measurements; it makes no quality claim, per the charter and
per role.**

---

## Premises vs measured

| premise | source | status | resolution |
|---|---|---|---|
| Comfy Cloud MCP tools reachable | charter ASSUMED | VERIFIED | ToolSearch loaded all schemas at session start; full arc proceeded, no Stage-E-halt fallback needed |
| `e12_pair_cloud_step.py` has NO canon binding | charter, citing E54 (2026-08-17) | **MEASURED FALSE** | Already bound at HEAD via v0.6.0/v0.7.0's "gate closes fail-closed at every authoring site" (commits `79b8fb6`/`c72f66a`, both post-date E54's own measurement). Confirmed by direct code read, `git diff HEAD` (empty), and two already-passing tests in `test_t94_fail_closed.py` |
| Any saved workflows on the account relevant to this door | charter ASSUMED | CHECKED, COMPLETE | `list_saved_workflows` enumerated in full (77 total, both pages, `has_more: false` confirmed on the second) — none is A1-specific (all named for other subjects: ships, saltroad warrior/officer, logos, armature/VACE tests); this arc's 8 ring graphs were authored fresh via `e12_pair_cloud_step.py`, not pulled from a saved workflow |
| W3's camera pattern (v_ext = bbox_z * 1.204) transfers to A1 | charter ASSUMED | VERIFIED, own numbers derived | `e12_frame.py` on A1's own mesh: 576x1024 (NOT W3's 752x1024, which E57's renders used only because no `--profile` was passed at that stage) |
| A1-palette.json bands can gate the ring's twins directly | implicit (charter names the file as "Bands: canon/A1-palette.json") | **MEASURED: SCHEMA MISMATCH, WORKED AROUND, GAP DISCLOSED** | `A1-palette.json` uses a hue-centre-per-material schema, not `palette_gate.py`'s `allowed_bands` hue-range schema; derived bands via the studio's own named "convention, not measurement" (+/-10 deg). Deeper gap: bands measured pre-LoRA, ring twins are post-LoRA (first time for this subject) — reported at length in Stage F, not resolved |
| The recipe's models exist on the venue | charter Stage A instruction | VERIFIED | All four (UNET/CLIP/VAE/LoRA) present under exact matching filenames, `source: comfy-cloud` |

---

## Predictions and outcomes

| # | prediction | blind? | interval | outcome |
|---|---|---|---|---|
| P1 (Gate A) | Anchor replay reproduces the reference within the 0.84-precedent ΔE scale (uniform residual = float-kernel class, per the standing hardware-anchor law) | Yes — stated before submission, in the charter itself, not this seat's own addition | byte-identical OR uniform ΔE at ~0.84 scale = ACCEPT | **EXCEEDED**: pixel-array byte-identical, ΔE 0.0000 exactly, stronger than either named branch |
| P2 (Stage B) | The door (`e12_pair_cloud_step.py`) needs binding before use | Charter's own premise, inherited from E54 | binding required | **FALSE, MEASURED BEFORE ACTING**: already bound at HEAD; demonstration run anyway, against A1's own canon specifically |
| P3 (Stage B) | The reference's own full positive_text, already Gate-0-verified 18/18, will pass the door's canon check cleanly | Not stated in the charter; this seat's own expectation before testing | pass (missing=[], unlicensed=[]) | **FALSE**: missing=[] as expected, but unlicensed fires on undeclared pose/lighting staging prose — caught before Stage D was written, not after |
| P4 (Stage C) | A1's own derived frame differs from W3's inherited 752x1024 | Not stated in the charter; this seat's own expectation from reading `turn_render.py`'s defaults | some frame, unspecified | **HELD**: 576x1024, substantially narrower |
| P5 (Gate E) | All 8 delivered frames equal the requested 576x1024 exactly | Charter's own VAE-rounding law, applied to a div-16 frame | exact match, no crop | **HELD**: 8/8 exact |
| P6 (Stage F) | No prediction stated for the off-palette magnitude — the charter asks for measurement, not a bound | N/A | N/A | **REPORTED**: far above this repo's own clean precedent, with the LoRA-baseline-gap structural caveat; no verdict rendered |

---

## Gates summary

| gate | state | evidence |
|---|---|---|
| MCP reachability | PASSED | ToolSearch loaded comfy-cloud/facet-record/facet-measure at session start |
| Stage B refusal demonstration | PASSED (door already bound) | N3-stripped prompt REFUSED naming the phrase; full reference prompt REFUSED on unlicensed residue (a distinct, real finding); Stage-B-composed candidate prompt PASSED clean (ok=True) — all three transcripts verbatim above, all before any generation |
| Gate A (anchor pixel comparison) | **ACCEPTED** | 0 differing pixels of 1,672,192; ΔE 0.0000 every statistic; sizes match (1136x1472); file-sha256 differs (encoder metadata only, confirmed via pixel-array comparison) |
| Gate C (control bbox-check) | PASSED | 8/8 views, control bbox within ~1-2px of mask bbox (contour-dilation-consistent); all 16 control+mask bytes sha256'd |
| Gate D (canon_gate resolves A1 against its own profile) | PASSED | `census`: A1 prof_hit 10/10 (was 0/10 against the placeholder); `resolve --subject A1` exit 0; `check_prompt`: ok=True, missing=[], forbidden=[], unlicensed=[] |
| Gate E (delivered == requested frame) | PASSED | 8/8 views, 576x1024 exact, no VAE-rounding mismatch |
| Stage F spec-violation re-roll | **NOT TRIGGERED — deferred, not decided** | Off-palette numbers are large and structurally confounded by the untested pre-LoRA-bands-vs-post-LoRA-twins gap; distinguishing "LoRA house style" from "genuine wrong material" is the Director's judgment, not this seat's. 0 of 2 reserved re-roll credits spent |
| Hermetic suite (out of this arc's own stages, run as a broader precaution) | 1 failed (pre-existing, E57's CRLF, not this seat's), 1284 passed, 54 deselected | Reported above; not fixed, out of chartered scope |

---

## Ceiling and spend, final tally

**11 generations allowed. 9 spent. 2 reserved, unspent, deferred to the advisor/Director's
reading of Stage F.**

| batch | spend | estimate_credits reported | actual result |
|---|---|---|---|
| Stage A anchor | 1 | "0 credits - no paid API nodes found" (flagged: GPU/queue-time excluded, not a free-generation claim) | 1 job, succeeded, Gate A ACCEPTED |
| Stage E ring | 8 | Same flagged reading on the representative graph | 8 jobs via `submit_batch`, `submitted:8 failed:0`, Gate E PASSED all 8 |
| Re-rolls | 0 of 2 | N/A — not spent | Deferred |

No true per-generation credit COST figure was obtainable from `estimate_credits` for either
batch — both graphs are local-OSS-model workflows (UNETLoader/CLIPLoader-based), which this
venue bills by GPU/queue-time, explicitly excluded from the estimator's total. This is
reported as a limitation of the tool for this workflow class, not evidence of a zero-cost
run. `get_billing_activity`/`get_usage_report` were not called this session (out of the
charter's explicit ask, which names `estimate_credits` specifically); the advisor may want
to check actual account debits against this arc's 9 submitted jobs.

---

## Working tree

`E:\AI\training\facet_E58\` — `reference\` (anchor graph + output + Gate A report),
`stageB\` (refusal demonstration), `controls\` (frame derivation, clay renders, exact
silhouettes, canny controls, Gate C report, upload names), `ring\` (8 authored graphs, 8
downloaded twins, Gate E check), `stageF\` (derived gate bands, palette report, registration
+ perimeter report, off-palette overlays), `sheets\` (the Director's sheet + manifest),
`gate_a_measure.py`, `check_topology.py`, `extract_full_graph.py`, `build_e58_sheet.py`,
`handoff.md` (kept current through every stage).

## git status --short (verbatim, at close)

```
 M tests/test_t91_canon_in_path.py
 M tools/canon_gate.py
?? docs/experiments/E58-a1-twin-prompts.json
?? docs/experiments/E58-a1-twin-ring-report.md
?? profiles/a1.json
```

`docs/experiments/E58-a1-twin-ring-kickoff.md` and all of E57's files are no longer listed
untracked — they were committed mid-session by the advisor's own seat (`bdad934`,
`a09ac3c`, `40df0ac`; see the finding above). Nothing in this seat's own change-set
conflicts with that commit (`git diff --stat` on both touched files shows clean,
reasonably-sized diffs). Nothing committed by this seat. Every file above left for the
advisor to review and commit by pathspec.

## Standards compliance, as executed (restated against the charter's own pre-registration)

1. **PIN_PER_STEP — held.** Anchor graph pulled verbatim from the PNG, unmodified even in
   `filename_prefix`; every ring graph's 6 recipe values pinned in `profiles/a1.json` with
   `{value, why, from}`; all 8 seeds pinned identical (770700) before submission; every
   control/mask/graph/twin byte sha256'd.
2. **ANDON_AUTHORITY — held.** Gate C, Gate E both ran as pre-registered checks (not
   post-hoc rationalizations); the door's fail-closed binding (Stage B) was demonstrated,
   not assumed; Stage F's spec-violation question was reported rather than resolved by this
   seat's own tuning.
3. **NAMED_COMPENSATORS — held as pre-registered.** Spent credits have no compensator by
   design (charter's own table); every other artifact this session produced lives outside
   the repo (`facet_E58\`) or is a new/never-conflicting file inside it, undo = delete.
4. **DECOMPOSE_BY_SECRETS — held.** Venue anchoring, door verification, control geometry,
   profile authoring, ring submission, and measurement stayed separate stages communicating
   through on-disk artifacts, exactly as charter specified.
5. **UNCERTAINTY_GATED_HUMANS — held, and load-bearing at the close.** The Director's own
   spend authorization gated the arc's start; Stage F's off-palette finding is returned to
   him/the advisor rather than resolved by a re-roll this seat is not authorized to decide.
6. **EXTERNAL_VERIFIER — held.** `canon_gate`, the topology checker, Gate A/C/E's pixel
   measurements, and `palette_gate.py` all verify the generator's output; the generator
   never grades itself; no quality word appears in this report in the forbidden sense.

---

*(Report complete through Stage G. `handoff.md` holds the same close-out, condensed, for
the advisor's continuity.)*

