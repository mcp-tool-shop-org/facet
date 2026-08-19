# E64 report — the scopes fill, Stages 0+1 (HALTED at the spend gate)

Charter: [E64-view-scopes-kickoff.md](E64-view-scopes-kickoff.md)
Tree: `E:\AI\training\facet_E64\`
Spend: **0/2. Nothing generated.** Halted at fence 3 ("ratify, then
spend") per the charter's own Stage 1 instruction. No comfy-cloud MCP tool
was called this session.

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

**Fence 3 (ratify, then spend).** This is the gate the seat is sitting at.
**No generation has been submitted.** Stage 2 waits on the advisor
relaying the Director's ratification of the eight scope lists above.

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
| Fence 3 (ratify, then spend) | **HALTED** — the seat's current position; 0/2 spent |
| Fence 4 (style_face is a clause, not a surface) | **PASSED** — injection refuses; composer path confirmed |
| Gate E (delivered frame == requested) | **NOT RUN** — Stage 2 only |
| Census/coverage byte-identical | **PASSED** — `A1: 16/16` both before and after, full dict-equality, not just the ratio |
| T34 collected-count unmoved | **PASSED** — `test_t34_no_unaccounted_test_count_on_any_surface` and the pin leg both green; no `def test_` added anywhere, two existing functions extended in place |
| Front-view byte-identity (compose) | **PASSED** — re-derived against a scratch copy of the pre-edit canon, not asserted |
| Full hermetic suite | **PASSED** — 1288 passed, 54 deselected, 0 failed, 8 pre-existing unrelated warnings (test_t59, unrelated `re.split` deprecation) |

## Credits

**0 spent.** No comfy-cloud MCP tool (`estimate_credits`, `submit_workflow`,
`submit_batch`, `dry_run`, or otherwise) was called this session.

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

- Handoff (fuller technical detail, reproduction commands, what happens
  when ratified): `E:\AI\training\facet_E64\handoff.md`
- E63's graphs this arc reused for the reversion proof and the
  seed/denoise/control cross-check:
  `E:\AI\training\facet_E63\stage0\graph_P_v3.json`,
  `graph_P_v5.json`
- E58 controls, confirmed present, to be reused byte-identical at Stage 2:
  `E:\AI\training\facet_E58\controls\ctrl\a1clay_3_control.png`,
  `a1clay_5_control.png`
- No PNGs under `E:\AI\training\facet_E64\` yet — nothing generated.

## Out of scope, respected

cn was not raised. The ring was not regenerated. Profile views (v1/v2/v6/
v7 — declared in the same edit, DRAFT, load-validated, but with no
compose()-level can-fail legs exercising them) were not probed. No canon
phrase was edited. No painting occurred.
