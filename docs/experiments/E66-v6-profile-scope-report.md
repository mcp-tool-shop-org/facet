# E66 report — view 6, two generations

**Written 2026-08-18. Executor: this session (the re-roll seat).
Tree `E:\AI\training\facet_E66\`. Spend: 2 generations total (1 at the
Director's own hand, pre-dating this session; 1 this session, the
one-re-roll law's single new-seed roll). No repo tool code changed —
`canon/a1.surfaces.json`, `tools/canon_compose.py`, `tools/canon_gate.py`
were read, never edited, by this session.**

This report covers BOTH E66 generations at view 6 (yaw 270, true
profile), per dispatch. It does not judge, rank, or recommend — the
Director's eye rules the cell (docs/experiments/README.md's own words
for this row).

## What this arc is

E65's sheet was, in the Director's own reading, perfect except view 6:
the head turned toward the camera when it should stay in profile. E66
dropped `eyes` and `mouth` from `scopes.views["6"]` (style_face follows)
while keeping `hair`, `face` (olive skin), and `neck` — ratified
2026-08-19, "eyes and mouth dropped." The Director ran that generation
himself (seed 770700) and it fixed the head — "RULED DONE AT THE
ADVISOR'S EYE." But it opened a second question: the chest/collar region
painted a tan buttoned panel where canon names a cream high-collared
shirt. That is the third distinct phantom garment at this view across
three rolls (E58: brown stole; E65: unnamed chest element; E66: tan
panel) — instability, not a stable prior, per the README status row.
The one-re-roll law licenses exactly one new-seed roll. This session ran
it.

## Premises checked, not assumed

The dispatch instructed composing the view:6 prompt "from the CURRENT
ratified scopes." Rather than assume the canon had not moved since the
Director's own hand-run generation, `build_reroll.py` recomposed the
prompt live from `canon/a1.surfaces.json` at HEAD and asserted it was
byte-identical to the recorded graph's own node 7 text before doing
anything else. It was:

```
A young archivist in his 20s, a sleeveless plum long-vest with fine gold
embroidery, a cream high-collared shirt, an umber sash, slim dark-green
trousers, polished brown shoes, olive skin, tousled dark curls,
ink-stained fingertips, painterly digital art with visible brushwork,
rich saturated palette, realistic stylized proportions, plain warm
pale-grey studio backdrop, no weapons, no held objects, nothing crossing
the body silhouette, head facing straight ahead, arms slightly away from
the body, hands empty and open, feet planted and visible.
```

Identical for both generations — the prompt is not the variable under
test; the seed is.

## Generation 1 — the Director's own hand (pre-dates this session)

- **Seed 770700**, denoise 0.92, cfg 2.5, steps 20, euler/simple,
  `Qwen-Image-InstantX-ControlNet-Union` strength 0.9, LoRA
  `saltroad_style_v2_lowlr` strength 0.75, 576x1024.
- Graph: `E:\AI\training\facet_E66\stage0\graph_v6.json`.
- Output: `E:\AI\training\facet_E66\gen\a1_e66_v6.png` (576x1024,
  confirmed this session — Gate E PASS).
- Diffed against `facet_E65\stage2\graph_6.json` (this session, `diff`):
  changes ONLY nodes 15 (`filename_prefix`: `a1_e65_v6` ->
  `a1_e66_v6`) and 7 (positive text — drops `curious brown eyes`,
  `a slight smile`, and `crisp readable facial features`). Nodes 9/10
  (twin pixels, E58 v6 control) byte-identical to E65's own v6 graph.
- Head: in true profile with the body, nose to frame-left, matching the
  clay — ruled done.
- Chest/collar: a **tan buttoned panel** — see description below.

## Generation 2 — this session's re-roll

**One generation. Seed 314159 (new for this view). Everything else
byte-identical to Generation 1**, proven by a diff-assertion in code, not
asserted by hand.

### Build (`E:\AI\training\facet_E66\reroll\build_reroll.py`)

Full transcript: `E:\AI\training\facet_E66\reroll\build_reroll.log`.

1. **Recompose check** — `canon_compose.compose(doc, view=270,
   form="flat")` against live `canon/a1.surfaces.json` == the recorded
   graph's node 7 text, byte-identical. The ratified scope had not moved
   since the Director's hand-run generation.
2. **Gate at view:6** — `canon_gate.require_canon(prompt, subject="A1",
   scope="view:6")`:
   ```
   gated=True required=18 missing=[] forbidden=[] unlicensed=[] out_of_scope=[]
   ```
   PASS, before any submission.
3. **Diff-assertion** — the script walks every node id in the base graph
   and the candidate graph; for node 13 (KSampler) it walks every input
   key individually. The only recorded difference anywhere in the graph:
   `13.inputs.seed` (770700 -> 314159). Confirmed a second, independent
   way: a raw `diff` of the two written JSON files (both serialized
   `indent=1, sort_keys=True`, the same convention the recorded graph
   already used) shows exactly one changed line:
   ```
   79c79
   <    "seed": 770700,
   ---
   >    "seed": 314159,
   ```
4. **Link-topology check** (self-links, dangling targets, bad output
   indices, orphan reachability from the `SaveImage` node) — PASS on
   both the base and candidate graphs: `nodes=15 links=18 reachable=15
   orphans=0`.

Candidate graph written to
`E:\AI\training\facet_E66\reroll\graph_v6_seed314159.json`.

### Credits

`estimate_credits` on the candidate graph, reported before submission:
**0 credits — no paid API nodes found**. This is an OSS/local ComfyUI
graph (UNETLoader/CLIPLoader/VAELoader/ControlNetLoader/
LoraLoaderModelOnly/KSampler/VAEDecode/SaveImage) — GPU time only,
matching every prior generation this arc. `submit_workflow`'s
credit-spend confirmation gate applies to paid API nodes only; none are
present, so no confirmation prompt fired.

### Submission

- `dry_run: true` — `status: validated`, one warning: `Node #5
  (LoraLoaderModelOnly): "lora_name" ... was not found in the bundled
  node index` — a bundled-catalog-lag warning on the studio's own
  uploaded LoRA name, not a rejection; the same warning appears on every
  prior generation this arc that uses this LoRA. CLAUDE.md's own law ("a
  dry_run PASS does not prove link sanity") is why the code-level
  topology check above ran independently rather than relying on this.
- Real submission: `prompt_id 7acb17b9-06b9-4813-b06b-8ff2259e9afd`,
  `status: succeeded_with_warnings` (same benign warning only).
- `wait_for_job` — first poll timed out in-progress (~25s), second poll:
  `status: succeeded`, `warnings: []`.
- `get_output` — downloaded via the tool's own emitted `curl.exe`
  command (run by this session, not handed to the Director), to
  `E:\AI\training\facet_E66\reroll\gen\a1_e66_v6_seed314159.png`,
  633,626 bytes. The original `facet_E66\gen\a1_e66_v6.png` was never
  touched — both generations are on disk regardless of outcome, per the
  one-re-roll law.

### Gate E

`E:\AI\training\facet_E66\reroll\..\..\gate_e_check.log` (script run
this session, checked both E66 generations plus the two sheet baseline
images):

```
reroll seed-314159:            576x1024  PASS
E66 original seed-770700:      576x1024  PASS
E58 v6 baseline:                576x1024  (informational, matches)
clay_6:                         752x1024  (Blender render, not gated — informational)
```

Delivered == requested for both E66 generations.

## The sheet

`E:\AI\training\facet_E66\reroll\sheet\E66_reroll_sheet.png`
(3190x1352 px, script `build_reroll_sheet.py`, log
`build_reroll_sheet.log`). Four panels — clay_6 | E58 v6 baseline | E66
seed-770700 (rejected, kept in record) | this roll seed-314159 — each a
full-body thumbnail (460 px tall) plus a chest/collar crop row beneath
at 2x upscale (crop box `(120,110)-(460,430)` on the three 576x1024
generations; shifted, not re-registered, for clay_6's wider 752 px
frame). No verdict text, no ranking rendered onto the sheet. Per-panel
sha256 and Gate E status are printed on the sheet itself and in the log:

```
CLAY_6                    752x1024  (not gated)          sha256 a41a0c63c31a5056
E58 v6 BASELINE            576x1024  GATE E PASS           sha256 6436707ecd36842a
E66 seed-770700 (tan panel) 576x1024  GATE E PASS          sha256 effe8c04ca9372ff
E66 RE-ROLL seed-314159    576x1024  GATE E PASS           sha256 f7bb3c643262e08c
```

## Chest/collar description — both generations, factual, uncertainty stated

**This is a seat's description of what is visually present, not a
measurement and not a verdict** (E64's own law, quoted in this session's
dispatch: "a seat's sentence about its own output is not a measurement").
No instrument can adjudicate garment identity at a true profile — E65
measured zero isolable sleeve-sides at this view, and the same geometry
argument applies to the chest/collar seam. This is the Director's eye's
class. Both crops are in the sheet above at 2x upscale for his own
inspection; what follows is this seat's best-effort factual read, hedged
where the read is uncertain.

**Generation 1 (seed 770700, the recorded/rejected artifact).** The
standing collar at the throat reads as a solid tan/ochre-brown, with a
thin sliver of white visible right at its very top edge. Below it, in
the gap where the plum outer vest opens at the front (its armhole), the
same tan/ochre-brown continues down the torso as a distinct panel,
bordered on its forward edge by a gold/tan piped trim that matches the
vest's own armhole piping, and carries a visible vertical row of small
round brass-toned buttons. This reads as a separate buttoned garment —
a waistcoat-like layer between the outer vest and the cream shirt sleeve
— brown/tan in hue, not cream. The cream is visible only on the sleeve.

**Generation 2 (seed 314159, this session's roll).** The standing collar
at the throat reads as the SAME dark plum/maroon as the outer vest
itself (not tan) — again with a thin white/cream sliver visible right at
its top edge, similar in character to Generation 1's sliver but on a
different base hue. Below the collar, the torso panel visible through
the vest's front opening also reads as plum/maroon rather than tan or
cream, with a few small dark (not brass-bright) buttons faintly visible
partway down — fewer and less prominent than Generation 1's row. A
separate element is visible crossing diagonally from the shoulder down
toward the back — a darker maroon/brown band or strap-like shape. This
seat cannot say with confidence what that element is meant to represent:
it could be the vest's own back panel or a lining edge made visible by
the profile angle and the vest's sleeveless cut (the clay geometry, see
below, shows the mesh opens at the armhole in a way that could expose an
inner surface here), or it could be an unnamed accessory the model
introduced on its own, the way E58's roll introduced an unnamed stole.
This seat did not attempt to resolve which. Net read: neither the tan of
Generation 1 nor a clearly cream collar/panel matching the canon phrase
is present in Generation 2 — the collar and visible torso panel are
closer in hue to the vest than to the shirt, with an additional element
of uncertain identity at the shoulder.

**One geometry observation, offered as an observation, not a causal
claim.** `clay_6.png` (the mesh render, no color) shows a subtle raised,
segmented ridge pattern sculpted into the chest surface under the vest
opening — visible in the sheet's crop row as faint horizontal facets
running down the torso. This seat notes that three separate rolls at
this view (E58, E66-770700, E66-314159) have each painted SOME kind of
buttoned or segmented panel in roughly that location, in three different
colors. Whether the sculpted ridge is influencing the ControlNet toward
painting a buttoned panel there regardless of prompt content is a
hypothesis this seat has not tested and does not assert — it is offered
because CLAUDE.md's own standing rule is to search for a mechanism before
re-rolling again, and because a repeated pattern across independently-
seeded rolls is worth naming even when its cause is unmeasured.

## What this session did NOT do

- No ranking, no verdict, no recommendation on either generation.
- No third roll. The one-re-roll law is spent; this session stops here
  regardless of what the chest/collar crop shows.
- No edit to `canon/a1.surfaces.json`, `tools/canon_compose.py`, or
  `tools/canon_gate.py` — read-only this session.
- No memory-store write.
- No git commit.

## Git status (verbatim, re-checked after writing this report — not
assumed)

```
$ git status
On branch main
Your branch is ahead of 'origin/main' by 32 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/experiments/E66-v6-profile-scope-report.md

nothing added to commit but untracked files present (use "git add" to track)
```

Before this report existed, the tree was clean (`nothing to commit,
working tree clean`, checked at session start). This report's own file
is the only change this session made inside the git repo; everything
else this session touched lives under `E:\AI\training\facet_E66\`,
outside version control. This session has not staged or committed
anything — the advisor folds.

## Paths

- Base graph (Generation 1, recorded): `E:\AI\training\facet_E66\stage0\graph_v6.json`
- Generation 1 output: `E:\AI\training\facet_E66\gen\a1_e66_v6.png`
- Re-roll build script: `E:\AI\training\facet_E66\reroll\build_reroll.py`
- Re-roll build log: `E:\AI\training\facet_E66\reroll\build_reroll.log`
- Re-roll candidate graph: `E:\AI\training\facet_E66\reroll\graph_v6_seed314159.json`
- Generation 2 output: `E:\AI\training\facet_E66\reroll\gen\a1_e66_v6_seed314159.png`
- Sheet script: `E:\AI\training\facet_E66\reroll\sheet\build_reroll_sheet.py`
- Sheet: `E:\AI\training\facet_E66\reroll\sheet\E66_reroll_sheet.png`
- Gate E check: `E:\AI\training\facet_E66\reroll\..\gate_e_check.log`
  (scratchpad copy; rerun trivially from the paths listed in this report)

## Director verdict (2026-08-19)

**66 REROLL is the winner.** Seed 314159 is the accepted v6 cell.

Head: true profile, with the body. Chest: nearest of the four rolls to
the declared materials; the remaining maroon diagonal is accepted as
part of this cell, not a reason to reject it. The seed-770700 frame
stays in the record as a rejected kept artifact. The one-re-roll law
stays spent. No third roll.

This closes A1's twin stage: E65 v0–v5 and v7, plus this frame as v6.
Manifest: `E:\AI\training\facet_A1_accepted_ring\MANIFEST.json`.

- Handoff (live record, kept current through this session):
  `E:\AI\training\facet_E66\reroll\handoff.md`
- Job: `prompt_id 7acb17b9-06b9-4813-b06b-8ff2259e9afd`

## Out of scope (unchanged from the kickoff)

The other seven views; a ring regen; cn (never touched — strength stayed
0.9, byte-identical); W3; painting; N9 re-word; a third roll of any kind.

## Standards compliance (CLAUDE.md workflow-standards.md, scored 0-3)

- **PIN_PER_STEP** — 3. Every field of the submitted graph is pinned and
  logged (`build_reroll.log`); the diff-assertion proves byte-identity
  of every non-seed field against the recorded Generation 1 graph, and
  the recompose check proves the prompt is pinned to live canon rather
  than retyped.
- **ANDON_AUTHORITY** — 3. `check_topology`/`check_canon`/the diff-
  assertion all `raise SystemExit` (not silent, not a bare `assert`) on
  any deviation; the recompose-mismatch branch would have halted the
  entire session before any spend had canon moved.
- **NAMED_COMPENSATORS** — n/a-with-note. The one irreversible action
  (`submit_workflow`, GPU spend) has no undo — Comfy Cloud generation
  cannot be un-run — but it is bounded to exactly one call by the
  one-re-roll law itself, `estimate_credits` was reported before it
  (0 credits), and the rejected/candidate artifacts are both retained
  rather than deleted, which is this class of action's own compensator
  (the record, not a reversal).
- **DECOMPOSE_BY_SECRETS** — 3. Recompose-check, canon-gate, diff-
  assertion, and topology-check are four separate functions/blocks in
  `build_reroll.py`; the sheet-builder is a separate script entirely,
  touching only display code.
- **UNCERTAINTY_GATED_HUMANS** — 3. The chest/collar description above
  is explicitly hedged, declines to resolve the shoulder element's
  identity, and defers the actual verdict to the Director's eye rather
  than proposing a threshold or a ranking.
- **EXTERNAL_VERIFIER** — 2. The canon gate (`canon_gate.py`) and the
  topology sweep are both existing, unmodified instruments this session
  did not author; not 3 because the chest/collar read itself has no
  external verifier available at all — the report says so rather than
  inventing a proxy metric for it (CLAUDE.md's own law: "Canon is not a
  taste question to be routed around... no metric approximates it").
