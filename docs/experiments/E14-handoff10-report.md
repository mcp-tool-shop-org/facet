# E14 handoff 10 — the dense export: the accepted longsword becomes dataset asset #4

**Executor session, 2026-08-08 05:50–06:15.** Run under session handoff 10 (E14
Ruling 32b's on-acceptance item; method precedent
[E12-executor-kickoff.md](E12-executor-kickoff.md) session handoff 16, whose
report is [E12-handoff16-report.md](E12-handoff16-report.md); manifest
requirements from [E11-ruling.md](E11-ruling.md) addenda 4). Blind predictions
registered first at `34c9fc1`
([E14-handoff10-predictions.md](E14-handoff10-predictions.md)) and scored at the
end of this report.

**No generation, no GPU, 0 credits.** emit and every per-view product are open3d
CPU raycasts. **Nothing under `E14_strokes\run\`, `E14_strokes\garnet\` or
`E14_prep\` was opened for writing** — 708 files snapshotted before the run
(path, length, mtime ticks) and re-compared after: **0 created, 0 changed, 0
re-stamped** (§7). No ingest was performed and nothing was written in the lane
repo.

Tools changed: [`tools/e11_manifest.py`](../../tools/e11_manifest.py) (the
read-only operands mode, the longsword subject, per-subject palette / operands /
reference-view dispatch) · [`tools/e11_export_turnaround.py`](../../tools/e11_export_turnaround.py)
(the X4 arm and `view_products`' optional `class_flat` path). Commits `4411f4c`
(the read-only plumbing **alone**, so the anchor baseline was measurable before
any new declaration existed) and `bdcfe3a`.

**Watchdog, reported both ends.** Alive at session start — VRAM 3,821/32,607 MiB,
27,379 below the 31,200 ceiling. Alive at session end — 3,992/32,607 MiB. No
restart needed and none performed; **no GPU leg exists in this dispatch** to
exercise it.

---

## 1. Task 0 — the tools read before either was invoked

Both were read in full first, with the inherited claims checked against source in
the same breath (the calibration standard). Three things came out of the reading.

### 1.1 The dispatch's own inherited numbers — checked, all three hold

| dispatch claim | checked against | outcome |
|---|---|---|
| `longsword_hero.glb`, sha `ab62bb4bd753f2cef4db74d0` | the file, sha256'd this session | **holds** — and 52,046,888 bytes |
| register terms `ultra-realistic, worn metal, harsh directional light` | `prop.json` `restylize_views.py.prompt`'s tail, verbatim | **holds** |
| `lora-w 0.0` | `prop.json` at **both** stages (`restylize_views.py`, `texpass_brush.py`) | **holds** |

### 1.2 The anchor path as dispatched would have written into the dragon's committed tree

Registered as **P2b before the remedy was written**.
`e11_manifest.py`'s `build_tone_operands(tree)` ran unconditionally for any
subject declaring a tone transform, and it `json.dump`s
`tone_transform_operands.json` plus copies two files into `_operands_sources/`
**inside the subject's own tree**. `--no-copy` covered the declared copies; it did
not cover this, and `--out` does not redirect it. So re-emitting the dragon's
manifest for the anchor — the one thing the dispatch orders first — would have
rewritten three files under `E13_stroke\export\turnaround\`, a tree the lane
holds sha-verified pointers into and E12 Ruling 28 makes citable-only.

The bytes would almost certainly have been identical. That is not the property the
read-only claim rests on, and identical-bytes-different-mtime is exactly the shape
of a silent write.

**The remedy, committed alone** (`4411f4c`): `--no-copy` now covers the operands
assembly — both source files verified by sha256 against their sources, the
assembled sidecar compared content-for-content against what the tool would write,
**nothing written**, and a halt if any of the three is missing rather than
creating it. Same read-only substitution handoff 16 made for the copies, and
strictly more checking than the write path performs.

### 1.3 Where each declared value comes from — stated before the code was written

| declared value | source, and how it reaches the manifest |
|---|---|
| `identity.subject_name` | `"longsword"` — literal in the subject config |
| `asset.style.register.terms` | `["ultra-realistic", "worn metal", "harsh directional light"]` — `prop.json`'s `restylize_views.py.prompt` **tail**, verbatim; the same three words are [canon/LONGSWORD-IDENTITY.md](../../canon/LONGSWORD-IDENTITY.md)'s STYLE-SUPPLIED rows. `ruling: "E14 Ruling 5a; EARNED at E14 Ruling 32a"` |
| `asset.style.lora` | `{"declared": "none"}` — `lora-w 0.0` at both generation stages, expressed as the positive declaration the lane requires |
| `asset.tone_transform.*` | the garnet re-projection, §4.2 — every field with its own source |
| `asset.tone_transform.reference` | **derived, not typed**: reference view index 0 → yaw verified against `E14_prep/masks/silhouettes.json` → `y000_e00` through the same `key_of`/`safe_id` construction the render ids come from, then asserted to be a render id this manifest declares |
| `asset.render_derivation` | `{kind: "emit", generated: false, record: "E11 Ruling 2"}` — literal, and what makes per-render `generation` blocks a refused category error |
| `channels[].palette` | the six-class map, §3.1 |
| `view_owner.npy` | stage 1b's owner sidecar, chosen on evidence — §3.2 |
| `palette` | **read from [canon/E14-longsword-palette.json](../../canon/E14-longsword-palette.json) at runtime**, never transcribed; the suspension translated at the boundary (§4.3) |
| `acceptance` | E14 Ruling 32, with the three judged screenshots named |
| `captions.subject` | authored from LONGSWORD-IDENTITY's five elements / six terms |
| `pairs` | six, not eight — §4.4 |

---

## 2. Task 1 — the capability anchored before it was used, and again after

The dragon is the nearest committed manifest and it was **born under this tool at
1.3.0 with all four declaration blocks**, so unlike handoff 16's galleon case
there is no ruled deviation to subtract. The anchor was run twice.

| | sha256 | bytes |
|---|---|---|
| committed `E13_stroke\export\turnaround\asset-source.json` | `7ea3771013f1ee43…` | 18,399 |
| regenerated, read-only, **after the plumbing commit** | `7ea3771013f1ee43…` | 18,399 |
| regenerated, read-only, **after the whole longsword subject + the reference-view refactor landed** | `7ea3771013f1ee43…` | 18,399 |

**Byte-identical both times, 0 bytes differing** — and the sha reproduces
[E12-handoff16-report.md](E12-handoff16-report.md) §4's recorded
`7ea3771013f1ee43…` from a different session. The second run is the stronger one:
the capability that changes nothing when unused, re-checked *after* the change
rather than only before it.

Both anchor outputs went to a scratch path. **The dragon's tree was not touched**:
no file under `E13_stroke\export\turnaround\` carries an mtime inside this
session.

**The galleon was not run.** The dispatch names it a second anchor "if the first
is ambiguous"; the first was not, and handoff 16 already established that the
galleon differs from HEAD by exactly `renders_are` under E11 Ruling 3 — re-running
it would reproduce a known ruled deviation, not add information. Recorded so the
omission is a decision rather than a gap.

---

## 3. Task 2 — the dense export

Recorded invocation: `E14_strokes\export\run_export.ps1`. Wall clock **2 m 00 s**
(06:05:12 → 06:07:12) for the export arm.

**26 cameras**, derived at runtime from `profiles/prop.json`'s
`cull_unseen.py.production` — 24 yaws at 15° plus `0,55` and `180,55`. Same list
as the beast's; the galleon ran 28. **× 2 channels** (asset, prov).

**Every emit carried `--profile` and every emitted frame was asserted 240×1024**
(Ruling 29c's trap: an unprofiled emit silently produces a 752-wide frame). The
set of frames the run produced is exactly `{(240, 1024)}` — 53 emits, one shape.

### 3.1 The class map — five non-background classes, a first on this route

The provenance atlas is an exact **6-colour** map and its counts reproduce the
record to the texel:

| class | rgb | texels | % of valid |
|---|---|---|---|
| background | 16,16,18 | 13,115,313 | — |
| stage-1b projection | 118,146,110 | 1,588,943 | 43.391 |
| **garnet re-projection** | 220,60,220 | 66,468 | 1.815 |
| **collar repair** | 40,230,230 | 1,436 | 0.039 |
| brush (8 strokes) | 240,176,48 | 75,890 | 2.072 |
| dilation (finalize) | 150,90,150 | 1,929,166 | 52.682 |

The five partition all **3,661,903** valid texels exactly, and reference
(stage-1b + garnet + repair) = **1,656,847 = 45.246%**, which is Ruling 31b's
45.25 / 2.07 / 52.68 to the digit. No replay needed, as with W3 and the dragon.

Every prior subject's atlas carried three classes, so `view_products`' claim
encoding (`0` reference / `1..254` brush / `255` dilation) cannot express this
one. The arm passes a per-texel **class index** instead, through a new optional
`class_flat` parameter; absent, all three predecessors take the identical code
path (the anchor in §2 is what says so).

X-H3's lossless leg holds at six classes: the indexed atlas is pixel-identical to
the truecolor source through the PLTE round-trip.

### 3.2 ⚠ The owner channel — two candidate sidecars, and only one of them agrees

The dispatch says stage 1b carries a real ownership record and asks what the
exporter emits. **Two** numeric owner arrays exist for this subject, and they are
not interchangeable:

| | owned | reference texels **unowned** | owned **outside** reference |
|---|---|---|---|
| `E14_prep\stage1\stage1b_atlas_owner.npy` | **1,656,847** | **0** | **0** |
| `E14_strokes\garnet\reproj_corrected\atlas_owner.npy` | 1,658,221 | 211 | 1,585 |

The dragon's ANDON — *every reference texel owned, nothing outside owning* —
**passes on stage 1b's array and fails on the re-projection's.** The mechanism is
Ruling 27b's own catch one layer over: the corrected re-projection's **atlas
write** was restricted to territory ∩ holes, and its **owner sidecar beside it
never was**, so it records the ownership of an unrestricted six-twin projection
whose +1,374 stray styled texels the restriction kept out of the asset. Its
1,585 outside-reference owners are that same drift, and its 211 unowned reference
texels are the key moving under a colour-only edit.

**Declared: stage 1b's array**, as `view_owner.npy`. It is the one that describes
the partition the accepted asset actually carries. The alternative is **not**
copied into the tree — it stays at its own path, its numbers ride in
`x4_run.json`'s `owner_sidecar_comparison` and in this table, and putting 16.8 MB
of an unrequested alternative inside a tree the lane holds sha-pointers into
would be paying a durability cost for a disposition nobody has asked for. Named
here so a ruling that wants a composite knows exactly where both operands are.

**⚠ The owner values are POSITIONAL indices, not view numbers**, and this is a
live hazard rather than a note: ids run 0–5 while the projected views are
**0, 1, 3, 4, 5, 7** (views 2 and 6 have no accepted twin — Ruling 20). A
consumer reading id `2` as "view 2" would read the *excluded* view. The mapping
is **verified, not assumed**: each id's texel count is asserted against
`stage1b_provenance_legend.json`'s own per-view committed counts —

| owner id | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| view | 0 | 1 | **3** | **4** | **5** | **7** |
| texels (both records) | 278,792 | 263,591 | 264,331 | 251,724 | 279,486 | 318,923 |

— six exact matches. The mapping rides in the manifest's `view_owner` channel
note and in `x4_run.json`.

**The display channel is absent**, honestly: no `owner_atlas.png` was ever built
for this subject, and synthesizing one would be inventing a channel rather than
exporting one (the X2 clause). Third subject in the dragon's configuration
(galleon: both; W3: neither; dragon and longsword: numeric only).

### 3.3 The anchors — 16 of them, against artifacts this run did not produce

The eight route yaws have recorded renders on **both** channels —
`run\final\render_final\flat_<yaw>.png` and `run\final\render_prov\flat_<yaw>.png`
— emitted by handoff 9 step 4 through this same emit path, same prep, same GLB,
same profile.

**16 / 16 byte-identical.** No pixel comparison was needed; the branch that would
have run one did not fire.

**X-H1 purity spot check: byte-identical.** *Works-perfectly test, stated in the
predictions:* the two files compared are produced independently — one from the
export's own `_state/asset`, one from a separately constructed
`_state/asset_rerun` in a different directory.

### 3.4 What the tree contains

**457 files, 191.5 MB**, at `E14_strokes\export\turnaround\`.

| | count | MB |
|---|---|---|
| `.npy` | 32 | 86.1 |
| `.png` | 314 | 55.7 |
| `.glb` | 1 | 49.6 |
| `.json` | 110 | 0.1 |

Per view: `asset.png`, `prov.png`, `silhouette.png`, `prov_class_<vid>.png` (born
indexed), `owner_id_<vid>.npy`, `loss_mask_<vid>.png`, `admission_<vid>.json`,
`cam.json`. Plus the copied `mesh.glb`, `atlas.png`, indexed
`provenance_atlas.png`, `view_owner.npy`, `styled_mask.npy`, the six clay↔twin
pairs, `tone_transform_operands.json`, `_operands_sources/` and `x4_run.json`.

**81.6 MB of that is `_state` emit scratch** — the same shape the galleon (88.8 MB)
and the dragon (99.3 MB) carry, so precedent-consistent and not a deviation.
Recorded because the lane holds sha-pointers into this directory and its size is
part of the durability commitment.

### 3.5 Per-view class shares

| | reference (1b + garnet + repair) | stage-1b | garnet | repair | brush | dilation |
|---|---|---|---|---|---|---|
| 24 eye-level yaws | **90.71 – 95.73** (mean 93.39) | 83.78 – 93.45 | 2.19 – 6.76 | 0.05 – 0.17 | 1.36 – 5.32 | 1.96 – 3.52 |
| `y+000_e+55` | 87.21 | 83.69 | 3.52 | 0.00 | 3.31 | 8.65 |
| `y+180_e+55` | 87.00 | 83.45 | 3.54 | 0.00 | 3.11 | 9.11 |

The elevated pair sits **3.5 points below the lowest eye-level view** and its
dilation share is 2.5–4× any eye-level camera's — a sword seen from 55° above
returns more of the surfaces no eye-level camera reached. Handoff 9's rendered
provenance measured the eight route yaws with a *different* instrument (pooled
88.71% reference, plus a 4.23% resampling-boundary class this export's
born-indexed `prov_class` does not have); the two are not the same quantity and
are not put in one column.

The mirror pairs agree closely throughout (0/180, 45/225, 90/270, 135/315),
which is the bilateral-symmetry fact behaving.

---

## 4. Task 3 — the manifest

`asset-source.json`, sha256 `58ff010c1c372f9b…`, 20,345 bytes, schema **1.3.0**,
asset id `e14_longsword_dense`, 26 renders, 5 channel declarations, **no
`renders[].generation` block anywhere**.

### 4.1 The reference view — verified against the record, not asserted

Two independent records agree, and the tool now checks the first mechanically
before deriving anything:

- `E14_prep/masks/silhouettes.json`: `"step": 45.0` with view `"0"` at
  `"yaw": 0.0` — **view 0 = yaw 0**.
- `garnet/garnet_operands_final.json`'s `reference.path` is
  `E14_prep\pair\PAIR_swordclay_0.png` — the accepted pair's view 0.

`verify_ref_view()` asserts `yaw == view_index × step` against the subject's own
recorded frame table, and the render id is then derived from the verified yaw
through the render-id construction, giving `y000_e00`; a second assert requires it
to be an id this manifest declares. The same function re-verified the dragon's
`view 1 = yaw 45` against `frame_00003.json` during the anchor — a claim that had
only ever been checked by hand before.

### 4.2 ⚠ The contract question, answered: the tone transform IS declared

**The reading, taken and registered before the artifact existed (P8): declare
it.** The 1.3.0 contract requires `kind`, `reference` and `operands`, and offers
`space`, `scope`, `record`, `reversible`. The block's stated purpose is that this
lane measures colour and "an undeclared upstream tone map is a systematic
covariate sitting under every one of those numbers"
([`lib/asset-source.js:87–111`](file:///E:/AI/style-dataset-lab/lib/asset-source.js)).
The garnet re-projection is exactly that object: deterministic, generation-free,
applied to generated views before they became projection sources, and it moved
**hue** — the quantity the lane's palette gate measures.

Declared, every value with its source:

| field | value | source |
|---|---|---|
| `kind` | `hue-rotation` | Ruling 26c/1 (T3); deliberately **not** `lab-stats-transfer`, so grouping by kind cannot conflate this with the dragon's |
| `space` | `CIELAB` | the rotation is about the achromatic axis; **checked, not asserted** — `C_before == C_after` and `L_before == L_after` in all six operand rows |
| `scope` | stone-mask on four of eight generation views (1/3/5/7), above the C\* 12.0 floor; 67,904 texels = 1.854% of valid | the operands file + `demotion.json` |
| `reversible` | `true` | a rotation by a recorded per-view angle with C\* and L untouched inverts by −θ; the lane records the claim without verifying it, which it says out loud |
| `reference` | `y000_e00` | §4.1 |
| `operands` | `tone_transform_operands.json` | assembled, below |

**The stretch, named:** the dragon's transform was whole-figure on all eight
projection sources; this one is a masked sub-region on **four of eight**. `scope`
is a free string and says so exactly. The alternative — declare nothing, report
the gap — was available and produces **no lane notice at all** (there is no
`ASSET_TONE_TRANSFORM_ABSENT` code), which is precisely the silence 1.3.0's own
`render_derivation` lesson was built to eliminate. The reading is the executor's;
the disposition is the advisor's, and every operand rides beside the manifest
either way.

**⚠ The trap this nearly walked into, and how it was caught.**
`garnet/corrected/` contains **six** corrected twins — 0, 1, 3, 4, 5, 7 — and a
reader who took that directory as "the projection input set" would declare six
transformed views. Measured: the corrected 0 and 4 differ from their originals by
**1,858 px and 1,657 px**, in the stone rows 87–142, at max 31 and 10 levels —
real edits, not re-encodings. But
[E14-handoff7-garnet-reprojection-report.md](E14-handoff7-garnet-reprojection-report.md)
§2 says what actually went in: *twins 1/3/5/7 at the ruled rotations, twins 0/4
unrotated — the original files, not my corrected copies.* Those two are the
derivation's **near-no-op controls** (Ruling 26a), computed to test the
instrument, never projected. Declaring six would have attributed a transform to
two views that did not receive one.

The assembled `tone_transform_operands.json` therefore separates them: `views`
carries the **four applied** rows, `_computed_not_applied` carries 0 and 4 with
the reason. Three assertions run at assembly, all halting:

1. **Two records of every rotation agree** — each row's `rotation_deg` against
   `T3_rotations.npy`'s array (0: −25.46, 1: +51.80, 3: +34.47, 4: −8.36,
   5: +55.45, 7: +48.01).
2. **The four applied rotations equal the ruled values** +51.80 / +34.47 /
   +55.45 / +48.01 (Ruling 26c/5).
3. **C\* and L are identical before and after in every row** — the property that
   makes `space` and `reversible` sourced statements rather than adjectives.

Plus one that tests the *word* "near-no-op": the worst not-applied control's
median ΔE (2.143) must be smaller than the smallest applied rotation's (3.712).

Six files ride in `_operands_sources/` with their shas —
`garnet_operands_final.json`, `T3_rotations.npy`, `garnet_derivation.json` and
the **four applied** corrected twins, which are the transform's outputs and what
makes it replayable.

### 4.3 The palette, and the fourth suspension translation

Read from canon at runtime. `min_chroma: 12.0`; three bands — `wine`
[332, 32], `gold` [42, 104], `lavender-rim` [292, 314]. Canon suspends **both**
gate bounds (Ruling 17d: report-only, no clean baseline until this subject's own
twins existed). The lane allows null for `max_offpalette_pct` and requires an
integer for `max_offpalette_blob_px`, so the blob suspension is translated at the
boundary into the whole-atlas sentinel **16777216** — a value no connected
component can reach, gating nothing, unmistakable for a measured threshold.
**Fourth application** of the E04 Ruling 29 pattern, and the tool halts if canon
ever grows a real bound under **either** key.

The `lavender-rim` band **is** exported, and that is the opposite of the dragon's
disposition for a principled reason: canon puts it in `allowed_bands`, which
`palette_gate.py` reads, whereas the dragon's suspended blue-violet stratum lives
in a key the gate does not read (E12 Ruling 15c). It is annotated in the manifest
as the rim-admission it is — covering no declared material, 92.8% rim support at
median depth 1.00 px — so a consumer cannot read it as a material band.

### 4.4 Six pairs, not eight

Views **2 and 6 carry no `pair`**: view 6 was excluded by the Director's own
overrule (Ruling 20) and view 2 was never accepted, so no twin exists for either.
The other six declare `{clay, twin}` where `twin` is the **accepted twin as
generated** (`E14_prep/twins/out/TWIN_swordclay_<v>.png`) — what stage 1b
projected, and the source of 1,588,943 of the 1,656,847 reference texels.

This is a deliberate difference from the dragon, whose `pair.twin` was the
*post-transform* image, and it follows the same rule: **the twin side is the one
this asset's paint actually came from.** On the dragon that was the harmonized
set, because harmonization fed all the paint; here the tone transform fed 1.854%
of the atlas, so the pre-transform twins are the honest pair and the four
corrected ones ride in `_operands_sources/`. **This is the executor's
construction**, like handoff 16's operands assembly; the alternative is named and
its files are in the tree.

### 4.5 The lane's reading — zero gap notices, first run

`sdlab asset ingest <tree> --project facet-assets --dry-run`, run from the lane's
own codebase at schema 1.3.0. **26 registered, 0 rejected, dryRun true.**

Notices, complete:

| code | kind |
|---|---|
| `ASSET_TONE_TRANSFORM_DECLARED` | info |
| `ASSET_RENDERS_ARE_DERIVATIONS` | info |

**Gap notices: 0.** Exactly the dragon's pair, and the tone-transform notice
quotes this subject's own declaration back: *"sources carrying a declared
'hue-rotation' tone transform toward y000_e00."* The three gap codes that exist
(`ASSET_STYLE_UNDECLARED`, `ASSET_SUBJECT_NAME_ABSENT`,
`ASSET_GENERATION_PROVENANCE_ABSENT`) are each closed by a block this manifest
declares.

The lane's own acceptance tests were then run read-only — all six `lib-asset`
files, **101 pass, 0 fail**, THE DRAGON SHAPE among them. The contract has not
drifted between what facet was told and what the lane accepts, and the six-class
categorical palette passed its PLTE proof on the first run (the sub-prediction
that named it as the likely failure point is **untested** — nothing fired).

**The lane repo is untouched** — `git status --short` empty before and after.

**Off-palette diagnostics**, quoted because they are new numbers and because both
bounds are suspended so they gate nothing: per-view **0.1145% – 0.4306%**,
largest blob **3 – 27 px**, quietest `y180_e00`, loudest `y090_e00`. For scale
without a verdict: the dragon measured 1.90–9.19% with blobs of 985–15,333 px
through the same gate. No bound is proposed here.

---

## 5. Predictions, scored

| # | prediction | outcome |
|---|---|---|
| P1 | 26 cameras (**not blind** — read from the profile) | **right**, 26 |
| P2a | the dragon's manifest comes back byte-identical | **right**, 0 bytes differing — and again after the refactor |
| P2b | the anchor path as dispatched writes into the dragon's committed tree | **right**; the remedy landed before the anchor ran |
| P3 | zero gap notices at 1.3.0, first run, exactly two info notices | **right** |
| P3b | if anything fires it fires on the six-class palette proof | **untested** — nothing fired |
| P4 | numeric owner present, display absent (**partly not blind**) | **right** |
| P4b | the sidecar owns exactly 1,656,847 including the repair's 1,436 | **right** — on stage 1b's array. The registered risk landed somewhere I did not predict: the *other* array fails the same check (§3.2) |
| P5 | purity spot check byte-identical | **right** |
| P6 | 16/16 recorded-artifact anchors byte-identical | **right** |
| P7 | view 0 = yaw 0 | **right**, from two records, now checked mechanically |
| P8 | the contract has an honest slot; declare it | **taken as registered**; zero gap notices and the lane echoes the declaration |
| P9 | six-class palette · six pairs · fourth suspension translation · lavender-rim exported | **right**, all four |
| P10 | eye-level reference 90–95%, brush 1–4%, dilation 2–4% | **split** — reference 90.71–95.73 (two views just over the ceiling), dilation 1.96–3.52 (one view just under the floor), **brush FALSIFIED**: 1.36–5.32, six views above 4% |
| P10b | the elevated pair's reference share sits **inside** the eye-level range | **WRONG** — 87.21 and 87.00 against an eye-level floor of 90.71 |
| P11 | tree 150–350 MB | **right**, 191.5 MB |
| P12 | 0 credits, no GPU, export leg 2–6 min | credits and GPU **right**; wall clock **2 m 00 s**, at the floor |

**P10b is the one worth keeping.** I predicted the elevated cameras would sit
inside the eye-level band because "a sword seen from 55° above shows the same
blade faces, unlike a dragon's wing tops." The direction was right and the size
was wrong in the useful way: the drop is **3.5 points** where the dragon's was
~15 and the galleon's ~20, so the mechanism reasoning held — but it is a drop, not
a null, and its shape is in the *dilation* column (8.65% and 9.11% against
1.96–3.52% at eye level), not in brush. What an elevated camera on this subject
returns is the crossguard's upper faces and the blade's flat, which are exactly
the surfaces the eye-level ring reached least. I reasoned about which *elements*
are visible and should have reasoned about which *texels* were reachable — the
same distinction handoff 16's P6 got wrong from the other direction.

P10's brush miss is the smaller sibling: I took the brush share from handoff 9's
**rendered** provenance (1.78% pooled) without accounting for its 4.23%
resampling-boundary class, which the exact texel-id raycast redistributes into
the real classes. Brush is the thinnest structure in the atlas, so it takes the
largest relative share of that redistribution.

---

## 6. The durability line

`E:\AI\training\facet_next\E14_strokes\export\turnaround\` **joins the
must-not-move list**, beside the three E11 addenda and handoff 16 already name:

- `E:\AI\training\facet_next\E04_stroke\export\turnaround\`
- `E:\AI\training\facet_E08\ARMB\export\turnaround\`
- `E:\AI\training\facet_next\E13_stroke\export\turnaround\`

The lane ingests mesh, atlas and every texture-space channel as
`materialized: false` — sha-verified pointers into these trees. The dataset's hold
on those channels depends on the directories continuing to exist, and they belong
in any backup that claims to cover the dataset. One exception rides the other way:
`tone_transform_operands.json` is **materialized** at ingest by the lane's own
1.2.0 rule, so the operands survive independently of this tree.

**A second dependency is named here because this subject introduced it:** the
declared `view_owner.npy` is a copy of `E14_prep\stage1\stage1b_atlas_owner.npy`,
and the *alternative* owner array this report weighs against it
(`E14_strokes\garnet\reproj_corrected\atlas_owner.npy`) is **not** in any export
tree. If a ruling ever wants the composite described in §3.2, that file must
still exist.

---

## 7. What is NOT established, and what is open for the ruling

- **The owner-sidecar choice (§3.2) is the executor's, made on a measurement.**
  Stage 1b's array passes the route's own ANDON and the re-projection's fails it,
  which is why it was chosen — but the stone territory's *colour* came from the
  corrected re-projection, and on that territory the two arrays disagree about
  **1,339 of 67,904 texels (2.0%)**, of which 211 are unowned in the
  re-projection's. A composite (stage 1b everywhere, the re-projection's ids on
  the garnet territory) is constructible and was **not** built: it would be a
  synthesized channel, and the X2 clause says export one or omit it.
- **The pair's twin side (§4.4) is the executor's construction**, differing from
  the dragon's on a stated rule rather than by accident.
- **`renders[].tone_transform`** (the per-render boolean the lane offers) is
  **not** emitted — the same disposition handoff 16 took. On this subject it would
  be a harder call than on the dragon: the transform reached 1.854% of the atlas,
  so "does THIS render carry it" is a question about visibility rather than a
  constant. Named in case the advisor wants it.
- **No ingest was performed.** The Director's lane-side paste is the next act, and
  the dry-run's digits are what a live run should reproduce.
- **The `_state` emit scratch** (81.6 MB, precedent-consistent) is undeclared
  working output inside a tree the lane will point into. Not a problem this
  session found a reason to fix; recorded so nobody discovers it later.
- **Read-only claim, how it was checked:** 708 files under `E14_strokes\run`,
  `E14_strokes\garnet` and `E14_prep` were snapshotted (path, length, mtime
  ticks) before the run and re-compared after — **0 new, 0 changed, 0
  re-stamped**. The check is mtime-based, which would not catch a
  write-then-restore; nothing in this session's code path opens those files for
  writing, and the copies are reads.
- **The seeded-question regression handoff 9 reported (its §11) is untouched by
  this session** — no comparables table in this report restates another subject's
  accepted mix as its own numbers; the one cross-subject comparison (§4.5's
  off-palette scale) names the dragon explicitly as a different asset.

---

## 8. Standards compliance (this run)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the recipe is `run_export.ps1`, not the transcript; camera set read from the profile at runtime and the frame asserted on all 53 emits; every declared value carries its named source (§1.3); manifest, GLB, atlas and operands sha256s recorded; predictions committed blind at `34c9fc1` before any measurement, and the read-only plumbing committed alone at `4411f4c` so the anchor baseline preceded every declaration |
| ANDON_AUTHORITY | 3 | the capability anchored byte-identical before use **and again after the change**; class counts halt against the record; the owner/class agreement halts and its failing candidate is reported rather than adopted; the id→view mapping halts against stage 1b's legend; the operands assembly halts on rotation disagreement, on any C\*/L movement, and on a control that is not a near-no-op; the palette translation halts if canon grows a bound under either key; the reference id halts if it is not a declared render |
| NAMED_COMPENSATORS | 3 | read-only inputs throughout, checked file-by-file against a pre-run snapshot; `--no-copy` extended so the anchor could not write into a prior subject's tree; anchor outputs to scratch; no ingest, no lane-repo write, nothing irreversible; undo is deleting one new directory and reverting three commits |
| DECOMPOSE_BY_SECRETS | 3 | facet declares, the lane judges shape — the seam held, and the lane caught what facet cannot self-check (npy dtypes against bytes, path containment, PLTE ⊆ palette at six classes); palette read from canon rather than transcribed; the reference id derived through the id construction after the frame table verified the view index |
| UNCERTAINTY_GATED_HUMANS | 3 | the ingest stays the Director's paste; the contract question was answered as a **registered reading with its stretch named**, not resolved silently; two executor constructions flagged with their alternatives and their operands retained; nothing ranked or recommended |
| EXTERNAL_VERIFIER | 3 | the lane's validator and its 101 acceptance tests are a different codebase judging this output, and both were run; the 16 byte anchors are against artifacts this run did not produce; the dragon anchor's sha reproduces a figure recorded by a different session; the rotation operands are asserted against a second recorded copy in a different file format |

**Reported, not ruled. The session stays open.**
