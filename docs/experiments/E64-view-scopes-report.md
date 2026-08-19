# E64 report — the scopes fill, all four stages

Charter: [E64-view-scopes-kickoff.md](E64-view-scopes-kickoff.md)
Tree: `E:\AI\training\facet_E64\`
Spend: **2/2.** Ratification for all eight scope lists relayed by the
advisor (commit `cda174b`, verified below before any spend), Stage 2 ran
as fenced, Stage 3 sheet built. Rank nothing.

**This report was written in two sittings.** The section below through
"Candidate prompts" is the Stage 0/1 record, written and HALTED before any
ratification existed — left as originally written rather than edited
after the fact. "Stage 2" and "Stage 3", further down, are new sections
appended once ratification was verified and the spend ran.

## Premises vs measured

The charter's opening claim: "E63's Arm P was composed at `view='front'`
**even for yaw 135 and 225**... W3 never cranked because it was built
under E02; A1 cranked in the exact arc that overrode it."

Measured directly against E63's own saved graphs
(`E:\AI\training\facet_E63\stage0\graph_P_v3.json` /
`graph_P_v5.json`, node 7's `text` field): **byte-identical between the
two files**, and byte-identical to `canon_compose.compose(doc, view=0,
form="flat")` — i.e. today's front-view flat compose, unchanged. The
premise is confirmed rather than assumed: E63 submitted literally the same
front-composed prompt, containing "curious brown eyes" and "a slight
smile," for both the yaw-135 and yaw-225 cameras.

The charter's second claim: "The composer has known how to drop face
clauses on a rear compose since E60 Stage 0 — that path was never used,
because the gate requires the face phrases at subject scope and a rear
prompt could not be submitted until `scopes.views` exists." Measured: true
as stated, and the reason is stronger than "the gate requires them" alone
— confirmed by reproducing the OLD (pre-E64) behaviour directly:
`canon_gate.check_prompt(doc, prompt, scope="view:3")` on the pre-edit
canon (saved to scratch before any change this session) raised `ANDON: no
view scope 3 declared for A1`, exactly as `canon/A1-IDENTITY.md`'s own
prior state predicts. There was no view-scoped gate to submit a rear
prompt AGAINST at all, not merely one that happened to reject rear
prompts.

## What was built (Stage 0, wiring — free)

**`tools/canon_gate.py`** gains `out_of_scope_hits(doc, prompt,
scope_ids)`. Before this arc, a declared scope (E59) could only REQUIRE
in-scope phrases; nothing prevented an out-of-scope phrase from being
PRESENT, because a front-composed prompt is a strict superset of what any
narrower scope requires and so satisfied the requiring-only check
trivially. This is the other half, checked generically by surface
membership (no "face" vocabulary in this file — canon_gate.py stays
subject-agnostic; see its own module docstring's new OUT-OF-SCOPE
REFUSAL section). Wired into `check_prompt()`'s `ok` computation and a new
`out_of_scope` key in its return dict; `refuse_uncovered()` and the CLI's
`check` subcommand both surface it in their ANDON messages.
**Dormant everywhere in the live repo except this arc**: `scope_ids` is
`None` at subject scope (every real spend site — restylize_views.py,
texpass_brush.py, brush_cloud_step.py — gates there today, none passing
`scope="view:*"` yet), so the function always returns `[]` for them.

**`tools/canon_compose.py`** gains `resolve_view_scope(doc, view)`:
resolves a view to its declared scope (surface-id set, and whether it is
face-bearing) when `doc["scopes"]["views"]` names one for that camera
index (the FLAT_RING "0".."7" convention already used by
`canon_worksheet.py`, `canon_bind.py`, and E58's own `graph_N.json`
naming); returns `(None, face_visible(view))` — the OLD binary rule,
byte-for-byte — otherwise. `_garment_feature_split` gained an optional
`scope_ids` parameter generalising "emit from the scope list" to every
occupant, not just the face-bound features the old rule ever touched.
`compose()` now calls `resolve_view_scope` in place of `face_visible`
directly.

**`canon/a1.surfaces.json`** gains all eight `scopes.views` rows
("0".."7"), transcribed verbatim from the charter's table, each marked
`"status": "draft"`. A THIRD EDIT note appended to the file's top-level
`note` field records the DRAFT standing (same convention as E62's
depends_on/protected_tokens rows — schema, not a ratification mechanism;
no `ratify` flag of its own).

## Fence transcripts

**Fence 1 (existing surface ids only).** All eight rows load clean —
`load_canon()` returns without raising, `census()`/`coverage()` unchanged
(see below). The refusal side, proven by injection (not merely asserted):

```
>>> mutated["scopes"]["views"]["0"]["surfaces"].append("no-such-surface")
>>> load_canon(mutated_path)
ANDON: scopes.views.0 names unknown surface no-such-surface
```
(`_selftest_out_of_scope`, leg d, `tools/canon_gate.py`.)

**Fence 2 (emit from the scope list; can-fail legs both ways).**

*CONTAINING refuses* — the reversion proof, using E63's own real text
rather than a synthetic case:
```
>>> check_composed(doc, p_front, scope="view:3")   # p_front == E63 Arm P's actual text
{'ok': False, 'out_of_scope': [
    {'occupant': 'N6',  'phrase': 'olive skin',         'surfaces': ['face', 'neck']},
    {'occupant': 'N9',  'phrase': 'curious brown eyes',  'surfaces': ['eyes']},
    {'occupant': 'N10', 'phrase': 'a slight smile',      'surfaces': ['mouth']},
], ...}
```
Identical at `scope="view:5"`. Two of the charter's three named phrases
("curious brown eyes", "a slight smile") are caught by name through the
real gate; the third ("crisp readable facial features", `style_face`) has
no surface id to be "outside" of (fence 4) and is proven absent from the
composed text directly — `compose(doc, view=135, form="flat")` and
`compose(doc, view=225, form="flat")` both verified NOT to contain it (nor
the other two, nor "olive skin", by direct substring search — four
phrases, four `False`).

*MISSING refuses* — the pre-existing E59 mechanism, exercised at the
newly-declared `view:0` scope specifically:
```
>>> thin = p_front.replace("curious brown eyes", "")
>>> check_composed(doc, thin, scope="view:0")
{'ok': False, 'missing': [{'surface': 'eyes', 'phrase': 'curious brown eyes'}], ...}
```

**Fence 3 (ratify, then spend).** Ratification relayed by the advisor,
commit `cda174b`. **Verified independently before any spend, not taken on
report**: `git show cda174b` shows a 9-insertion/9-deletion diff touching
only the eight `"status"` fields (`"draft"` -> `"RATIFIED by the Director
2026-08-18"`) and the top-level `note`'s THIRD EDIT sentence — every
surface-id array is byte-for-byte unchanged from what this seat wrote and
census-checked pre-ratification, hands included in rows 3/4/5. `f9829bd`
(the advisor's own fold of this seat's Stage 0/1 work) diffstat matches
this report's own numbers exactly. Stage 2 ran after this check, not
before. See "Stage 2" below.

**Fence 4 (style_face is a legal_clause, not a surface).** Verified by
injection: adding the STRING `"style_face"` to a `scopes.views` surfaces
array refuses at load time with the identical mechanism as fence 1
(`style_face` is a legal_clause id, absent from `doc["surfaces"]`'s id
list, so `_validate_router_fields`'s "unknown surface" check catches it
exactly as any other invented id would):
```
>>> mutated["scopes"]["views"]["3"]["surfaces"].append("style_face")
>>> load_canon(mutated_path)
ANDON: scopes.views.3 names unknown surface style_face
```
style_face's rear-view omission is driven entirely by
`resolve_view_scope`'s `fv` computation (does the declared scope name a
face-bearing surface?), never by a clause id in a surfaces array — the
composer's own code path, not a schema trick.

## Predictions with outcomes

**Stage 0/1 mechanism — measured, not predicted.** The wiring's own
correctness (fences 1/2/4, byte-identity, census invariance) was built
and then verified directly against real data and real can-fail legs, the
same session; there was no blind guess to record here, only a design that
either holds under test or does not. It held: `canon_gate.py --selftest`
and `canon_compose.py --selftest` both exit 0 with every new marker
present; the full hermetic suite passes at 1288/54/0 failed.

**Stage 2 visual outcome — genuinely blind, disclosed, not yet checked
against anything (no pixels exist).** E63's report read the v3/v5 defect
as "face toward camera over the shoulder," present under both its Arm P
(unchanged prompt structure, denoise 0.92) and Arm C (denoise 0.80,
washed-out material). My prediction: removing "curious brown eyes" and "a
slight smile" from the v3/v5 prompt text removes ONE plausible driver of
the crank — a textual instruction to render a visible, expressive face,
competing against a rear-facing control — but does **not** address a
control-image or ControlNet-strength explanation if the crank's true
cause sits there instead. I expect **less** pull toward camera on v3/v5
relative to E63's Arm P, not a resolved crank, because the underlying
E58 defect this whole arc is named after already existed on the raw clay
control before any prompt text existed at all. This is a low-confidence,
qualitative prediction with no numeric instrument behind it (matching
E63's own report: "No numeric instrument. E59 Gate 1 stays unused") — the
Director's eye is the only thing that can check it, and Stage 2 has not
run.

## Gates

| gate | status |
|---|---|
| Fence 1 (existing ids only) | **PASSED** — 8/8 rows load; unknown-id injection refuses |
| Fence 2 (emit from scope list, both directions) | **PASSED** — reversion proof + missing proof, both verbatim above |
| Fence 3 (ratify, then spend) | **PASSED** — ratification verified independently at `cda174b` before Stage 2 ran |
| Fence 4 (style_face is a clause, not a surface) | **PASSED** — injection refuses; composer path confirmed |
| Gate E (delivered frame == requested) | **PASSED** — all 8 sheet-source panels (2 views x 4 columns) 576x1024, including both new E64 gens |
| Canon-gate + topology check on the submitted graphs | **PASSED** — `check_canon` at the correct `view:3`/`view:5` scope, `check_topology` (self-link/dangling/orphan), both in code before submission — see `build_v3v5.py` transcript below |
| One-variable diff assertion | **PASSED** — `build_v3v5.py` asserts only nodes 7 (text) and 15 (filename_prefix) differ from E63's own Arm P graphs; node 8 (negative text) asserted byte-identical |
| Census/coverage byte-identical | **PASSED** — `A1: 16/16` both before and after, full dict-equality, not just the ratio |
| T34 collected-count unmoved | **PASSED** — `test_t34_no_unaccounted_test_count_on_any_surface` and the pin leg both green; no `def test_` added anywhere, two existing functions extended in place |
| Front-view byte-identity (compose) | **PASSED** — re-derived against a scratch copy of the pre-edit canon, not asserted |
| Full hermetic suite | **PASSED** — 1288 passed, 54 deselected, 0 failed, 8 pre-existing unrelated warnings (test_t59, unrelated `re.split` deprecation) |

## Credits

**Stage 0/1: 0 spent**, no comfy-cloud tool called. **Stage 2:
`estimate_credits` returned 0 credits — no paid API nodes found** (matches
E63's own recorded note: GPU-seconds only, not metered by this estimator).
`submit_batch` ran without a spend-confirmation prompt (consistent with
"free, local-only workflows are never prompted"); 2 submitted, 0 failed.
No dollar/credit figure is returned by this pipeline's own accounting —
GPU-seconds are billed on the account's usage report, outside this tool's
visibility.

## Candidate prompts (flat form — charter fence 3: "flat form per E61")

v3 (yaw 135) and v5 (yaw 225) compose to **byte-identical text**, since
both cameras share an identical declared scope per the charter's own
table:

```
A young archivist in his 20s, a sleeveless plum long-vest with fine gold
embroidery, a cream high-collared shirt, an umber sash, slim dark-green
trousers, polished brown shoes, tousled dark curls, ink-stained
fingertips, painterly digital art with visible brushwork, rich saturated
palette, realistic stylized proportions, plain warm pale-grey studio
backdrop, no weapons, no held objects, nothing crossing the body
silhouette, head facing straight ahead, arms slightly away from the body,
hands empty and open, feet planted and visible.
```

Against E63's Arm P (identical for v3 and v5, quoted from
`graph_P_v3.json`/`graph_P_v5.json` node 7, both files byte-identical to
each other):

```
A young archivist in his 20s, a sleeveless plum long-vest with fine gold
embroidery, a cream high-collared shirt, an umber sash, slim dark-green
trousers, polished brown shoes, olive skin, tousled dark curls,
ink-stained fingertips, curious brown eyes, a slight smile, painterly
digital art with visible brushwork, rich saturated palette, crisp
readable facial features, realistic stylized proportions, plain warm
pale-grey studio backdrop, no weapons, no held objects, nothing crossing
the body silhouette, head facing straight ahead, arms slightly away from
the body, hands empty and open, feet planted and visible.
```

**One variable, exactly**: E64's text omits "olive skin," "curious brown
eyes," "a slight smile," and "crisp readable facial features" — the four
face-bearing phrases this arc's scope table excludes from v3/v5 — and is
otherwise identical, word for word. Everything else fence 3 pins (seed
770700, denoise 0.92, cfg 2.5, steps 20, euler/simple, ControlNet
`Qwen-Image-InstantX-ControlNet-Union` at strength 0.9, the E58 controls)
is read directly off `graph_P_v3.json`/`graph_P_v5.json` and is unchanged
by this arc — confirmed by inspection, not yet re-submitted.

## Stage 2 — the spend

Ratification verified (above) before this ran. Graphs built by
`E:\AI\training\facet_E64\stage2\build_v3v5.py`, base loaded verbatim
from **E63's own** `graph_P_v3.json`/`graph_P_v5.json` (not E58's raw
ring graph) — the truest available form of "one variable against E63 Arm
P": every field E63 already submitted for this exact camera (seed 770700,
denoise 0.92, cfg 2.5, steps 20, sampler euler/simple, cn strength 0.9,
both `LoadImage` nodes — the E58 controls — and the negative text
including its CJK complement) stays byte-identical; only node 7 (positive
text) changes, plus node 15 (`filename_prefix`, disclosed, cosmetic —
`a1_armP_v3` -> `a1_e64_v3`).

Build-time checks, in code, before anything reached the network:
```
[canon] E64 v135 scope=view:3: gated=True required=16 missing=[] forbidden=[] unlicensed=[] out_of_scope=[]
[topology] E64 v135: PASS (nodes=15 links=18 reachable=15 orphans=0)
[delta] E64 v135: only nodes ('7', '15') differ from E63 Arm P's own graph
[delta] E64 v135: negative text (node 8) byte-identical to E63 Arm P

[canon] E64 v225 scope=view:5: gated=True required=16 missing=[] forbidden=[] unlicensed=[] out_of_scope=[]
[topology] E64 v225: PASS (nodes=15 links=18 reachable=15 orphans=0)
[delta] E64 v225: only nodes ('7', '15') differ from E63 Arm P's own graph
[delta] E64 v225: negative text (node 8) byte-identical to E63 Arm P
```
`check_canon` runs `require_canon(..., scope="view:3"/"view:5")` — the
gate call E63 structurally could not make (no scope existed yet). `check_
topology` is the same self-link/dangling/orphan/reachability sweep E63's
own `build_arms.py` used (CLAUDE.md: a `dry_run` PASS does not prove link
sanity).

`estimate_credits`: 0 credits, no paid API nodes. `submit_batch` (2
items, `client_os=windows`): `submitted: 2, failed: []`, no
spend-confirmation prompt (consistent with the 0-credit estimate).
`wait_for_batch` → both `ready` on the second poll (first returned
`timed_out: true` with 1/2 ready, per the tool's own ~25s polling
contract). `get_batch_output` → two signed URLs, downloaded via
`curl.exe` to `E:\AI\training\facet_E64\gen\`.

**Gate E**, measured directly (`PIL.Image.size`), not assumed:
```
a1_e64_v3.png (576, 1024) RGB
a1_e64_v5.png (576, 1024) RGB
```
Delivered == requested, both.

batch_id and job_ids: `E:\AI\training\facet_E64\stage2\spend_record.md`.

## Stage 3 — the sheet

Built by `E:\AI\training\facet_E64\stage3\build_sheet.py`, adapted
directly from **E63's own** `stage3/build_sheet.py` — same "Director's
zoom" constants (`HEAD_TOP=60, HEAD_BOT=340` on the 576x1024 frame,
`FULL_H=360` for the full-body thumbnail), same sha256-footer-per-panel
convention, same `gate_e()` check run again here (all 8 source panels —
both rows' control/E58-defect/Arm-P/E64 columns — independently confirmed
576x1024 a second time, from the sheet script itself, not reused from
Stage 2's check). The fourth column is E64's own gen in place of E63's
Arm C; a new block beneath each row prints both prompts, word-wrapped,
with the four phrases E64's scope table excludes from v3/v5 highlighted
in the Arm P line (read back from E63's own `graph_P_v3.json`/
`graph_P_v5.json`, not recomposed, so the sheet quotes what was actually
submitted rather than a re-derivation of it).

Sheet: `E:\AI\training\facet_E64\stage3\E64_director_sheet.png`
(2364x1796, sha256 `3b934bef47a8...`).

**What is visible (not a ruling), same discipline E63's own report used**:
the CONTROL panel for both v3 and v5 is a rear-quarter/rear-facing
silhouette, head aligned with the body, facing away from camera. The
other three panels in both rows — E58 DEFECT, E63 ARM P, and E64
per-view — all show the head turned back toward camera with the face (or
most of it) visible, in both rows. This is the same class the E63 report
named ("face toward camera over the shoulder") and it is present in all
three raster panels this arc's sheet places beside the control, E64's own
new column included. One cosmetic note on the sheet itself: the
phrase-highlighting in the Arm P text block collapses the comma between
two adjacent highlighted phrases ("curious brown eyes" / "a slight
smile") into a double space — a rendering artifact of the highlighter,
not a change to the actual submitted or quoted text, which is reproduced
verbatim (with the comma) in the "Candidate prompts" section above and in
E63's own graph file.

Sha256 of every sheet source, computed directly (not read off the
sheet's own small-print footer):
```
a1clay_3_control.png    4cc95983834c2d9cc491f6616e3cbdfe57d5b2eb51a4af1ce474dd916e3b31ee
a1_ring_v3.png           7b628cd609a95dcae6fe1cd88ca8780be759c970c7b026230aa6c8c91a11cdb5
a1_armP_v3.png           ff886b99db92d0f3c4e27c0c76a23882e3536651b83789747869d1d975db2e90
a1_e64_v3.png            ba3518e4eebff9bd0d6eddd8eaea2fabad7a939495c2f02e12e4c9392d8dc39a
a1clay_5_control.png    45f603ff6d90dfd63e6863072db71330241a5e747fa22d036edd5536b1a26cb0
a1_ring_v5.png           1332c93bdf84ce4567d3f8a905ec1c37e8393a5d3d94f4c9bdda80254ac10aa8
a1_armP_v5.png           60c27fdfec5bb060f55abe921a392f7e142f9280014fed52ac12bdbc704e4db9
a1_e64_v5.png            491fa68268ff44e01013186a0187c65a72d893641a83a1ca300505e5152899c9
```

The Director looks at the sheet; nothing above is a ruling on it.

## Git status (verbatim, captured after this report was written)

```
On branch main
Your branch is ahead of 'origin/main' by 21 commits.

Changes not staged for commit:
	modified:   canon/a1.surfaces.json
	modified:   tests/test_t92_canon_router.py
	modified:   tools/canon_compose.py
	modified:   tools/canon_gate.py

Untracked files:
	docs/experiments/E64-view-scopes-report.md

 canon/a1.surfaces.json         |  49 +++++++-
 tests/test_t92_canon_router.py |  36 ++++++
 tools/canon_compose.py         | 277 +++++++++++++++++++++++++++++++++++++----
 tools/canon_gate.py            | 211 +++++++++++++++++++++++++++++--
 4 files changed, 538 insertions(+), 35 deletions(-)
```

(the diffstat predates this report's own untracked addition, which has no
diffstat of its own to show — a new file). No commit made — the advisor
folds by pathspec per this repo's standing rule. `docs/experiments/
README.md`'s status table is untouched: adding E64's row is the fold's own
step, not this seat's.

## Paths

- Handoff (fuller technical detail, reproduction commands, spend record):
  `E:\AI\training\facet_E64\handoff.md`
- Stage 0/1 wiring: `E:\AI\facet\tools\canon_gate.py`,
  `E:\AI\facet\tools\canon_compose.py`, `E:\AI\facet\canon\a1.surfaces.json`,
  `E:\AI\facet\tests\test_t92_canon_router.py`
- Stage 2 build script + graphs + spend record:
  `E:\AI\training\facet_E64\stage2\build_v3v5.py`,
  `graph_v3.json`, `graph_v5.json`, `spend_record.md`
- Stage 2 generations (576x1024, downloaded from Comfy Cloud):
  `E:\AI\training\facet_E64\gen\a1_e64_v3.png`,
  `a1_e64_v5.png`
- Stage 3 sheet + script: `E:\AI\training\facet_E64\stage3\build_sheet.py`,
  `E64_director_sheet.png`
- E63's own graphs this arc built from (base) and quoted verbatim (Arm P
  text, prompt diff): `E:\AI\training\facet_E63\stage0\graph_P_v3.json`,
  `graph_P_v5.json`; E63's own gens reused as sheet sources:
  `E:\AI\training\facet_E63\gen\a1_armP_v3.png`, `a1_armP_v5.png`
- E58 controls and defect ring, confirmed present, reused byte-identical:
  `E:\AI\training\facet_E58\controls\ctrl\a1clay_3_control.png`,
  `a1clay_5_control.png`; `E:\AI\training\facet_E58\ring\a1_ring_v3.png`,
  `a1_ring_v5.png`

## Out of scope, respected

cn was not raised (ControlNet strength stayed 0.9, unchanged from E63's
own graphs — verified by inspection and by the diff-assertion that only
nodes 7/15 changed). The ring was not regenerated. Profile views
(v1/v2/v6/v7 — declared in the same edit, RATIFIED, load-validated, but
with no compose()-level can-fail legs exercising them and no spend
against them) were not probed. No canon phrase was edited. No painting
occurred.
