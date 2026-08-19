# E71 — fill the holes, then look again

**Advisor spec, 2026-08-19. One executor seat. Tree
`E:\AI\training\facet_E71\`. Spend: 0. Local only.**

**Direction (the Director, 2026-08-19): E70 sheet APPROVED.** Identity
holds, garment set is right, none of the five named failure modes
present at his eye. The brush conversation is open. The first sitting
is a **fill**, not a quality stroke.

## What is already paid

- Atlas: `E:\AI\training\facet_E69\bake\atlas_widescope.png` (do not
  mutate in place).
- Prep: `E:\AI\training\facet_E67\prep\`.
- Holes: 1,468 new texels at vest-front, collar, shoulder, hair
  speckle — the withheld set, sitting where E68/E69 measured them.
- Look construction: E70's sheet (twin | mesh, head + collar crops,
  flat light, footer). Reuse that construction so the two sheets
  compare.

## The fill

`texpass_finalize.py --surface-aware` on a **copy** of the E69 state.

`--surface-aware` is E07 L1: every hole takes its nearest painted
texel **in 3D**. Do not use the default atlas-space flood — that walk
was measured to pull colour from another island (E07 Gate 0: 74.9%).
A1 has no blade; this is not thin-extent. It is neighbour colour
across a 0.0423% hole set.

Write `--out` under this tree. Gate C: the E69 atlas bytes on disk
are unchanged at close.

## The look (the thing that can fail)

Same cameras, same crops, same footer as E70:

*the warm rim light in the twins is still paint; the overlay dots are
still the map.*

Sheet: E70 mesh | E71 filled mesh, plus the accepted twin as the
reference column. Head and collar crops required. Rank nothing.

Failure modes this sheet must be able to show: seams, through-
projection, bald crown, cream-as-wall, identity gone, **plus** fill
bleed (a hole taking the wrong neighbour — vest cream, hair backdrop,
collar plum).

## Out of scope

Brush. Cloud. Retuning 2% / dE 10. Re-bake. Binding. A ring regen.

## Prediction

The pale vest-front band and collar speckle will take neighbouring
plum/cream. If they take wall-grey or the wrong garment, that is
bleed and the fill is rejected; the brush still does not open on
those texels.

## Dispatch record

- 2026-08-19 — spec written on the Director's APPROVED of E70. First
  target is the holes. Stroke-one of the brush loop is not this arc.

---

## Standards compliance

Scored 0-3 against the six workflow standards, per the repo rule.

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every input is a named file with a recorded sha256 (E70 Gate A/C manifests). No generation, no model, no seed - the whole arc is deterministic local tooling at pinned paths. The two arms differ in one file (`holes.png`) and nothing else. |
| ANDON_AUTHORITY | **3** | `texpass_finalize.py` carries three `raise AssertionError` ANDONs (lines 79, 132, 136, 181) - E22-converted, not bare `assert`, so `python -O` cannot delete them. Gate C halts on any mutation of the E69 atlas. The seat halts and reports; it does not retune `--max-edge-median` or `--max-frac-beyond`. |
| NAMED_COMPENSATORS | **3** | Every write lands under `E:\AI\training\facet_E71\`. Compensator for the whole arc: `Remove-Item -Recurse E:\AI\training\facet_E71\` - owner, the executor seat. No irreversible step exists: no publish, no push, no cloud call, no mutation of any prior tree. Gate C asserts the E69 bytes unchanged at close, which is the compensator's own test. |
| DECOMPOSE_BY_SECRETS | **2** | The fill mechanism (`texpass_finalize`), the reachability partition (`__reachable__`, computed at bake time), the render (`turn_render`) and the bleed instrument (`palette_gate`) are four separate tools that change for four different reasons. Not 3: the sheet builder is a one-off script under the arc tree, so its layout decisions and its evidence selection are not separated. |
| UNCERTAINTY_GATED_HUMANS | **3** | One human checkpoint, at the end, gated on the only question no instrument answers: does the filled figure still look like the man. The Director's eye is the acceptance gate; nothing below ranks or grades the artifact. The seat states its predictions before looking, and discloses whether each was blind. |
| EXTERNAL_VERIFIER | **2** | `palette_gate.py`'s bands come from `canon/A1-palette.json`, derived at E57 from the reference and never fit to this question - a reference derived from something other than what it gates. Differential form (E70 renders vs E71 renders) means the instrument cannot pass by construction. Not 3: the fill and the reachability partition come from the same codebase, so the Arm R / Arm F render comparison is a self-check, and is reported as one. |

## AMENDMENT 1 - 2026-08-19 - the fill population above is FALSIFIED

**The advisor measured the artifacts this spec names before dispatching it. The
sentence "It is neighbour colour across a 0.0423% hole set" is wrong by 1,392x, and
every consequence of it in the sections above is withdrawn.**

`texpass_finalize.py` fills `valid & holes`, reading `holes.png` from `--state`
(`tools/texpass_finalize.py:64`). In a `project_twins` output, `holes.png` is written
at `tools/project_twins.py:1006` and means **every valid texel the eight-camera
projection did not write** - not the withheld set. The word is overloaded in this
codebase: `tools/e10_layer_seed.py:13` documents "holes" as emit's word for the region
to paint, which is a different population again.

Measured on `facet_E69\bake\atlas_widescope_holes.png` against
`facet_E67\prep\mask.npy`, and cross-read from `diag_widescope.npz`'s own atlas-level
arrays (`__reachable__`, `__styled__`, `__holes__`, `__valid__`), which were computed
at bake time and never fit to this question:

| class | texels | share of valid |
|---|---|---|
| valid | 3,470,348 | 100% |
| written (`__styled__`) | 1,425,925 | 41.09% |
| **`holes.png` marks** | **2,044,423** | **58.91%** |
| reachable by some camera (`__reachable__`) | 1,484,271 | 42.77% |
| **unreachable - no camera in the ring ever sees it** | **1,986,077** | **57.23%** |
| **reachable but unwritten** | **58,346** | **1.68%** |

So the command this spec commissions fills **2,044,423** texels, of which **97.1% are
surface no camera in the eight-view ring can render**. The Director's named target -
E69's 1,468 marginal withheld texels - is **0.072%** of what the command would touch.

**Three consequences, and they change the arc rather than trim it.**

1. **The two ANDONs would be graded on the wrong population.** `--max-edge-median 3.0`
   and `--max-frac-beyond 0.05` gate the *source distance* of each lookup. An
   unreachable texel's nearest painted 3D neighbour is far away *by construction* -
   being unreachable is what puts distance between it and any painted surface. Diluting
   the gate with 1.99M such lookups makes it a statement about atlas topology, not about
   whether the Director's holes took a good neighbour. Whether it fires is for the seat
   to measure; that it would be measuring something else is settled.

2. **The sheet could not answer the question it was written for.** 1,468 texels inside a
   2.04M-texel fill is a rounding error. An arm must be graded only on what it can move.

3. **A fact worth stating plainly, because it is startling and it is the record's own
   law paying off: the Director approved, at his eye, a mesh whose atlas is 58.91%
   unfilled.** E70 packed `atlas_widescope.png` as-is. That is the atlas-share-is-not-
   screen-share law in its cleanest form - 97.1% of the unfilled is invisible to every
   camera. It also means **filling is a change to an approved state**, not a completion
   of an unfinished one, and it must be justified rather than assumed.

### The corrected arc - two arms, one graded

Both are free, local, and one command each. The scoping is done in **data, not code**:
write a scoped `holes.png` into the copied state. No tool is modified.

- **Arm R (GRADED).** `holes.png` = `__reachable__ & ~__styled__` - 58,346 texels. This
  is the population a camera can see, and it contains the Director's 1,468. The two
  ANDONs are graded here and mean what they say. The partition comes from the bake's own
  geometry, computed before this arc existed and never fit to it.
- **Arm F (REPORTED, NOT GRADED).** `holes.png` unchanged - the full 2,044,423. This is
  the operation the spec above commissioned; it runs so that its question stays answered
  rather than deleted. Its ANDON readings are reported as what they are: a statement
  about atlas topology.

**Gate D, new, and it validates the partition rather than the fill.** If `__reachable__`
is correct, Arm R and Arm F must render **pixel-identically** across all eight cameras.
Compare **pixels, not file bytes** - a PNG hash mismatch is not evidence a render
changed, and that has produced two false halts in this repo. A non-zero pixel difference
does not condemn the fill; it means `__reachable__` is wrong, and that is a finding about
the bake worth more than this arc.

### The bleed instrument the spec left to the eye alone

`tools/palette_gate.py` already exists, takes `--palette --images --masks`, and asks the
specification's question - *does this carry colour the specification never declared* -
against `canon/A1-palette.json`, derived at E57 from the reference and never fit to this.
It reports total off-palette count **and** largest connected component, which is this
repo's two-threshold law for separating one wrong garment from ordinary speckle.

Run it **differentially**: the same cameras and masks over E70's renders and Arm R's
renders. A gate that fires on the baseline too is not evidence about the fill; the delta
is. It carries a chroma-floor question - below a chroma floor hue is not a colour - and
the seat verifies the floor is present before quoting any hue.

This does not replace the eye. It means the sheet is not the only thing that can fail.

### The `--state` construction, named so it is not improvised

`texpass_finalize.py` requires `--state` to contain `atlas.png`, `holes.png` and
`styled_mask.npy` under exactly those names. The E69 outputs carry a `_widescope`
infix. The seat copies and renames into a fresh state directory under `facet_E71\`;
it never renames in place. `--prep` is `facet_E67\prep` (holds `mask.npy`).

### Reuse, not commission - every tool this arc needs already exists

Enumerated before writing this amendment, because commissioning past an existing tool
is the failure this repo has paid for five times:

- fill - `tools/texpass_finalize.py --surface-aware` (E07 L1), with its three ANDONs
- reachability - `diag_widescope.npz` `__reachable__` / `__styled__`, already computed
- pack - `tools/bake_hero_pack.py`
- render - `tools/verify/turn_render.py --profile profiles/a1.json --flat`
- silhouette - `tools/silhouette_masks.py --prep facet_E67\prep --profile profiles/a1.json`
- crops + layout - `E:\AI\training\facet_E70\scripts\e70_build_sheet.py`, `crop_boxes.json`
- bleed - `tools/palette_gate.py` with `canon/A1-palette.json`

**E51's fill family was enumerated and is NOT the right family here, stated so the next
session does not re-enumerate it.** `fill_repair_e51.py` (arms A/B) and `orphan_fill.py`
act on the *twin-sampling* side - which view supports a texel, under which silhouette.
E71's question is the *atlas-neighbour* side: a texel no view supports at all, taking
colour from painted surface near it in 3D. Different family, correctly chosen. What E51
contributes is `palette_gate.py`, which it built and which this amendment adopts.

### Predictions - the seat writes these BEFORE it looks

Required, each with a stated band, each disclosing whether it was blind:

- **P1** - Arm R median source distance, in median triangle edges (the
  `--max-edge-median` reading). State the band before running.
- **P2** - Arm F median source distance. State whether you expect it above or below P1,
  and why, before running.
- **P3** - Gate D: the number of differing pixels between Arm R and Arm F renders,
  summed over eight views. A prediction of zero is a real prediction; say what a non-zero
  would mean before you see it.
- **P4** - the palette_gate delta (E70 renders vs Arm R renders): total off-palette
  texels and largest connected component. **Before predicting, compute what the
  instrument reads when the answer is definitely yes and definitely no, and predict
  inside that interval** - a prediction outside what the instrument can return could not
  have been right at any state of the world.

### Amended out of scope

Everything the spec listed, plus: modifying `texpass_finalize.py` (the scoping is data);
retuning `--max-edge-median` or `--max-frac-beyond`; and ranking the arms. **Neither arm
is a candidate for adoption in this arc.** The output is a sheet and a set of numbers.

### Dispatch record, amended

- 2026-08-19 - Amendment 1. The advisor measured the spec's own named artifacts before
  dispatching and falsified its fill population: 2,044,423 texels, not 1,468. The error
  is the unit/population family this repo has now recorded a dozen times - a real number
  (E69's measured 1,468 marginal cost) attached to a different object (everything
  `holes.png` marks). The advisor's own, caught before a seat spent a session on it,
  which is the only reason it is cheap.

## AMENDMENT 2 - 2026-08-19 - what the holes actually contain, measured

Measured at the same sitting as Amendment 1, read-only, on
`facet_E69\bake\atlas_widescope.png`:

| population | texels | distinct colours | value |
|---|---|---|---|
| `valid & holes` (all) | 2,044,423 | **1** | RGB(107, 107, 107) |
| of which unreachable | 1,986,077 | **1** | RGB(107, 107, 107) |
| of which reachable-unwritten | 58,346 | **1** | RGB(107, 107, 107) |
| written (`__styled__`) | 1,425,925 | 162,113 | mean RGB(93.5, 66.8, 58.2) |

**Every hole texel carries one flat mid-grey, and it is a declared parameter, not an
artifact**: `project_twins.py:191` takes `--hole-grey`, default `0.42`, and
0.42 x 255 = 107.1 -> 107. Nothing about the fallback is derived from the paint.

**This confirms, by exact measurement, a hypothesis E70's seat offered and honourably
declined to call confirmed.** That report described "a consistent grey tessellated
pattern" seen in the atlas in UV space and refused to claim a pixel-exact correlation
with the rendered pale patches. The correlation is now exact on the atlas side: the
pattern is a single colour occupying every unwritten valid texel.

Three things follow, and they sharpen the arc rather than change it:

1. **The Director's named defect has a value.** The lighter vertical band at the vest
   front-centre, and the pale patches at collar and shoulder, are grey 107 showing
   through where no camera wrote. The fill's job is stated precisely: replace grey 107
   with real neighbouring paint at texels a camera can see.
2. **Gate D gets sharper.** Since every hole is the identical colour, Arm R and Arm F
   differ only in *which* grey-107 texels stop being grey. If `__reachable__` is right,
   the 1,986,077 unreachable ones never reach a camera and the two arms' eight renders
   are pixel-identical. There is no confound from the arms starting at different values.
3. **The seat must report where grey 107 survives Arm R.** A reachable texel is not
   necessarily rendered by *these eight* cameras at a resolution that shows it. Grey
   remaining in an Arm R render is not a fill failure; it is the reachable set and the
   camera set disagreeing, and it should be named as that rather than as bleed.

## AMENDMENT 3 - 2026-08-19 - the approved atlas has no recorded recipe

Found while verifying Amendment 1's inputs, and it is about the artifact the Director
approved rather than about this arc. Stated here because E71 is the next arc to touch
that atlas.

**The two flags the approved state needed are OFF or wrong by default.**
`--headband-bg-withhold` is a `store_true` (off by default) and `--bg-withhold-scope`
defaults to `"headband"`. The whole-figure state E69 produced, E70 packed, and the
Director approved required **both** `--headband-bg-withhold` and
`--bg-withhold-scope all`.

Verified at source rather than inferred, three independent ways:

- `E:\AI\training\facet_E69\logs\widescope_joint8_console.txt` prints `WHOLE-FIGURE`
  **9 times** - the tool's own scope banner, which reads `head-band` at the default.
- E69's report states the joint run's atlas totals, and they match this session's own
  independent measurement of `atlas_widescope.png` exactly: **1,425,925 written /
  2,044,423 holes**.
- `project_twins.py:884-912` - with the switch off, the code path is byte-identical to
  the pre-E68 tool.

**So re-running the route on A1 at defaults reproduces the PRE-E68 behaviour, not the
state that was approved.** Nothing in `profiles/a1.json`, in the repo, or in the tree's
own logs records the producing command: the console echoes derived frame parameters
(`--fit-axis height`, `margin 1.204`, `aspect 576,1024`) but no literal invocation
exists anywhere this session could find.

This is this repo's own law firing on a fresh artifact: **a recipe that does not
reproduce its output is not a recipe** - the same shape as the canon twin, whose
parameters were never in the repo. The record's own remedy applies unchanged and is
adopted here rather than re-derived:

- **The artifact stands.** It is approved, it is on disk, its sha256 is recorded at
  E70 Gate A/C. Nothing is withdrawn.
- **Its provenance is recorded as INCOMPLETE rather than implied.** That is this
  amendment.
- **Do not sweep for the recipe.** A reconstruction that reproduces the bytes cannot be
  verified as *the* recipe, and the artifact is already in hand. E71 must not attempt it.
- **Fix the generator so the next one is reproducible.** The durable repair is to make
  `project_twins.py` write its own resolved argv (and tool sha256) into the state
  directory it produces, so provenance is a by-product of running rather than an act of
  console archaeology afterwards. That is *prefer eliminating a risk to gating it*, and
  it is NOT this arc's work - E71 does not run `project_twins`.

**A second, smaller finding of the same family.** `profiles/a1.json`'s
`_out_of_scope_this_profile` states that the `project_twins.py` block is unpopulated
because A1 "has not been baked, painted, projected or culled" and populating it "would
be values arriving by invention rather than measurement." **That was true when written
and is now false**: A1 has been projected (E67/E68/E69) and baked (E70), at the
Director's approval. The profile's own stated condition for populating the block is
therefore met - the values would now arrive by measurement. Populating it is a real
job (the full flag set, not the two withhold flags alone) and belongs to the seat that
next runs the route, not to this arc.

**Related, and repaired in this same fold rather than left:** `--bg-withhold-scope`
landed at E68 and was widened at E69 without a decision in any route profile, which
left `tests/test_t16_registry_sweep.py` red on 5 legs through the E69 and E70 folds -
both of which reported a green suite. The flag is now classified `_per_invocation` in
all four route profiles and T16's pins moved in the same commit. See that test's own
comment for why the classification is the right one rather than the convenient one.

## AMENDMENT 4 - 2026-08-19 - the record watches three of five profiles

Found while verifying Amendment 3, and it is the same debt seen from the record's side.

`docs/index/conventions.json` `corpora.profile_files` declares three:

```
profiles/beast.json   profiles/character.json   profiles/ship.json
```

**There are five on disk.** `profiles/prop.json` and `profiles/a1.json` are undeclared,
and `git log -S "profiles/prop.json" -- docs/index/conventions.json` returns nothing -
neither has ever been declared. This is an omission of long standing, not a regression.

Measured consequences, not inferred:

- `record_health` reports **446 corpus files**; `certificate.corpus_manifest` computed
  from the repo's own code returns **443**, all markdown, no profiles.

**That 443/446 gap is not itself the defect, and saying so loosely would put a wrong
mechanism in the record.** Traced to source: `tools/record_mcp.py:292` defines the
served corpus as `record_markdown() + PROFILE_FILES`, while the shared library's
`certificate.corpus_manifest` walks `record_markdown()` alone
(`record-index/record_index/certificate.py:56`), and `record_markdown` returns
`corpora.record_top_files` - which is `CLAUDE.md` and `README.md` - plus every `.md`
under `corpora.record_roots`. So the server adds the profiles on purpose and the library
function is simply narrower. **Two consequences, and the second is the sharper one:**

- the declared profile set is short by two, so **even the server watches only three of
  five**; and
- **the server and the library disagree about what the corpus IS**, which means a
  CLI-built index and an MCP-built index certify different things. In practice the
  server's definition is the operative one - only MCP `record_build` writes the
  certificate - but the divergence is real and a profile edit is visible to one path and
  invisible to the other.
- This session edited all four route profiles. The staleness banner named **three** of
  them. `prop.json` moved with no signal at all.
- `parse_decisions` builds the `decisions` table by walking `profile_files`, so **two
  profiles' decisions are simply not in the record.**
- Leg 0 checks *declared-but-absent* and structurally cannot see *present-but-undeclared*.
  A file that exists and is not declared is invisible to the verifier by construction -
  the same shape as this repo's other blind checks, and the reason it has survived.

**`profiles/a1.json` is one of the two**, which is why this sits beside Amendment 3
rather than in a separate note: A1 is the approved character, and the moment its
`project_twins.py` block is populated with the measured values Amendment 3 describes,
that population lands in a file the record is not watching.

**Not repaired in the E71 fold, and the reason is scope rather than doubt.** Declaring
the two files adds rows to the `decisions` table and moves the corpus count, so it needs
its own commit with its own count surfaces re-pinned and its own suite run - riding it on
a commit about hole-filling would conflate two changes and make both harder to read
later. It is named here so it cannot be lost, and it is the advisor's next item.

**E71 does not touch it.** The seat does not run `project_twins`, does not edit any
profile, and does not edit `conventions.json`.

## RULING - 2026-08-19 - the amended spec is the one that runs

Ruled at the Director's word, on the measurements in Amendments 1-4:

- **The amended spec is dispatched; the original is not.** Its fill population was wrong
  and every consequence of it is withdrawn.
- **Arm R is the graded fill** (58,346 reachable-unwritten, containing the 1,468).
  **Arm F runs so the original question stays answered, and is not graded.**
- **Gate D compares PIXELS, never PNG hashes.** If the two arms' renders differ,
  `__reachable__` is wrong, and **that finding outranks the fill.**
- **Neither arm is adopted this sitting.** The output is the sheet and the numbers.
- **Filling visible grey is justified; flooding the 1,986,077 unseen texels is not.**
  That is the whole reason the graded arm is scoped to what a camera can reach.
- **The brush stays shut.** E71 is free and local.
- **T16 is folded BEFORE the seat is dispatched, not with the fill** - a separate commit,
  so the suite repair and the arc do not read as one change.

### The two debts, ruled OUT of this arc

1. **The approved bake has no recipe.** The artifact stands; its provenance is recorded
   as INCOMPLETE. **The next `project_twins` run writes its resolved argv into the state
   directory it produces**, and **`profiles/a1.json` is populated from measurement by the
   seat that runs the route** - not by E71, which does not run `project_twins` at all.
2. **`profiles/a1.json` and `profiles/prop.json` are absent from
   `conventions.json` `corpora.profile_files`**, so the record cannot see the approved
   character's profile. Its own commit, its own count surfaces. Not E71.

### On the T16 classification

`_per_invocation` is the right class **on the condition that E68 used `headband` and E69
used `all`**, which is what makes no single value correct for the route. Both were
verified at source before the classification was applied: E68's rule is the head-band
scope by its own report and by the tool's default, and E69's joint run prints
`WHOLE-FIGURE` nine times in
`E:\AI\training\facet_E69\logs\widescope_joint8_console.txt`.
