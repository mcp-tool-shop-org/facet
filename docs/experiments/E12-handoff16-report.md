# E12 handoff 16 — the dense export: the accepted dragon becomes dataset asset #3

**Executor session, 2026-08-07 01:49–02:10.** Run under session handoff 16 (E12
Ruling 28's on-acceptance item; requirements from
[E11-ruling.md](E11-ruling.md) addenda 4). Blind predictions registered first at
`0ac88fa`, blob `e79c51a`
([E12-handoff16-predictions.md](E12-handoff16-predictions.md)) and scored at the
end of this report.

**No generation, no GPU, 0 credits.** emit and every per-view product are open3d
CPU raycasts. **Nothing under `E13_stroke\run\`, `E13_stage1\`, `E13_twins\` or
`E12_prep\` was opened for writing** — checked by mtime after the run, empty
(§7). No ingest was performed and nothing was written in the lane repo.

Tools changed: [`tools/e11_manifest.py`](../../tools/e11_manifest.py) (`--out`,
`--no-copy`, the four 1.3.0 declaration blocks, the dragon subject) ·
[`tools/e11_export_turnaround.py`](../../tools/e11_export_turnaround.py) (the X3
arm). Commits `0966e1a` (plumbing alone, so the anchor baseline was measurable
before any declaration existed) and `09c4960`.

**Watchdog, reported both ends.** Alive at session start 01:49:27 — heartbeat age
**1 s**, PID 5132, log ticking at 2 s, VRAM 3719/32607 MiB, status `ok`. Alive at
02:09:56 — heartbeat age **1.8 s**, VRAM 3797 MiB, `ok`. No restart was needed and
none was performed. No GPU leg existed to exercise it.

---

## 1. Task 0 — the tools read before either was invoked

Both were read in full first. Two things came out of the reading that changed how
the session ran, and one of them corrects this dispatch.

### 1.1 The dispatch's anchor baseline is wrong, and it was wrong before I touched anything

The dispatch says: regenerate the galleon's manifest "with the new code and no new
declarations — it must come back byte-identical to the committed one."

`git log -S renders_are` says otherwise. **`renders_are` entered
`e11_manifest.py` in `18bdcdf`, after the galleon tree was emitted in
`20f2a0a`** — E11 Ruling 3's parked errand ("the next manifest emission adds a
one-line field… the validated trees are not churned now for a wording field"). So
HEAD's tool already could not reproduce the committed galleon manifest, by
ruling, before this session existed.

Registered as P2 before measuring, and two anchors were run in its place (§2).

### 1.2 Where each declared value comes from — stated before the code was written

| declared value | source, and how it reaches the manifest |
|---|---|
| `identity.subject_name` | `"dragon"` — literal in the subject config; the value E11 addenda 4 names |
| `asset.style.register.terms` | `["ultra-realistic", "menacing"]` — [canon/DRAGON-IDENTITY.md](../../canon/DRAGON-IDENTITY.md) STYLE-SUPPLIED row, verbatim. `ruling: "E12 Ruling 10b"` |
| `asset.style.lora` | `{"declared": "none"}` — `beast.json`'s `lora-w: 0.0` expressed as the positive declaration the lane requires; no `card` may ride beside it (the lane refuses that as self-contradiction) |
| `asset.tone_transform.{kind,space,scope,reversible}` | Rulings 22e / 23f — `lab-stats-transfer` / `CIELAB` / `figure-mask` / `true` |
| `asset.tone_transform.reference` | **derived, not typed**: the ruled reference view index (1) through the same `key_of`/`safe_id` construction the render ids come from → `y045_e00`. Yaw checked at §4.1 |
| `asset.tone_transform.operands` | an assembly of two recorded files — the one genuinely under-specified point in the dispatch, §4.2 |
| `asset.render_derivation` | `{kind: "emit", generated: false, record: "E11 Ruling 2"}` — literal, and it is what makes per-render `generation` blocks a refused category error |
| `palette` | **read from [canon/E12-beast-palette.json](../../canon/E12-beast-palette.json) at runtime**, never transcribed; the suspension translated at the boundary (§4.3) |
| `acceptance` | E12 Ruling 28, with the three judged views named |
| `captions.subject` | authored from DRAGON-IDENTITY's eleven elements as corrected (D2 olive-tan, D6/D7 charcoal) |
| `renders_are` | already in the tool since `18bdcdf`; lands on its first new emission here, as Ruling 3 intended |

---

## 2. Task 1 — the capability anchored before it was used

The anchor's stated purpose ("the capability that changes nothing when unused")
needs a baseline the capability could actually reproduce. Two were measured.
`--no-copy` was added so a prior subject's manifest could be re-emitted with its
tree **read-only**: instead of rewriting each declared copy, the flag sha256s the
file already there against its source. That is strictly more checking than the
copy path and moves no mtimes.

### P2a — HEAD's tool (plus plumbing) vs the committed galleon manifest

| | sha256 | bytes |
|---|---|---|
| committed | `396637d2030e7f01…` | 21,208 |
| regenerated | `02252d94889fb0d3…` | 21,445 |

Not byte-identical, **as predicted**. The entire difference:

- added keys: `['renders_are']` · removed keys: `[]` · **changed shared keys: `[]`**
- regenerated **minus** `renders_are` equals the committed file exactly — as JSON
  and byte-for-byte after identical re-serialisation.

No second difference, so P2a's registered halt did not fire. **The same test on
W3 gives the same single-key delta and no changed keys** — the deviation is the
ruling's, on both subjects, not a drift.

### P2b — the modified tool vs the plumbing-only tool, no new declarations

| | sha256 | bytes |
|---|---|---|
| ship, plumbing only | `02252d94889fb0d3…` | 21,445 |
| ship, with all four declaration blocks in the tool | `02252d94889fb0d3…` | 21,445 |

**Byte-identical.** The four blocks are optional inputs and a subject that
supplies none emits none — including the key ordering, which the byte comparison
is sensitive to.

**The galleon tree was not touched**: its manifest still hashes
`396637d2030e7f01…` with mtime 2026-08-05 20:44:41, and nothing in that tree has
a mtime inside this session.

---

## 3. Task 2 — the dense export

Recorded invocation: `E13_stroke\export\run_export.ps1`. Wall clock **2 m 36 s**
(02:02:15 → 02:04:51).

**26 cameras**, derived at runtime from `profiles/beast.json`'s
`cull_unseen.py.production` — 24 yaws at 15° plus `0,55` and `180,55`. The
galleon ran 28 (a ship-specific superset with four elevated), W3 26. The beast's
elevated ruling was NONE (Ruling 7), so this list is the code default.

**× 2 channels** (asset, prov). The galleon ran 3 because it had an owner display
atlas to render; this subject does not (§3.2).

### 3.1 The anchors — 16 of them, against artifacts this run did not produce

The eight route yaws already have recorded renders on **both** channels:
`run\FINAL_final_y*.png` and `run\FINAL_prov_y*.png`, emitted by
`run\render_final.ps1` through this same emit path, same prep, same GLB, same
profile — the Gate-1 sheets' own columns, which the Director's verdict was read
off.

**16 / 16 byte-identical.** This is a stronger anchor set than either predecessor
had: the galleon anchored one camera and inherited the other 27 on purity plus a
shared code path (E11 Ruling 7).

Two further checks inside the arm, both halting:

- **The claim map's class counts against the ruled mix.** The provenance atlas is
  an exact 4-colour map — background `(16,16,18)`, reference `(118,146,110)`,
  brush `(240,176,48)`, dilation `(150,90,150)` — and its counts reproduce
  Ruling 27e to the texel: **1,430,687 / 99,643 / 1,710,180 = 3,240,510 valid**.
  No replay needed, as with W3.
- **The owner sidecar against the claim map.** All 1,430,687 stage-1 texels carry
  an owner id, owner ids present are `[0..7]`, and **0** texels outside stage 1
  carry one.

**X-H1 purity spot check: byte-identical.** *Works-perfectly test, stated in the
predictions:* this check also returns "identical" if a file is compared to
itself, so the two files compared are produced independently — one from the
export's own `_state/asset`, one from a separately constructed
`_state/asset_rerun`, in different directories.

### 3.2 The owner channel — a third configuration, and it is the finding

The dispatch asked to confirm the native owner channel "rides the tree the way
the galleon's does." It rides **half** that way, and the half it does not is
honest rather than fixable here:

| | galleon | W3 | dragon |
|---|---|---|---|
| numeric `view_owner.npy` (texture) | yes | no | **yes** |
| per-view `owner_id_*.npy`, `loss_mask_*.png` | yes | no | **yes** |
| rendered `owner_view` display channel | yes | no | **no** |

The galleon's `owner_view` is emit run over `out/owner_atlas.png`, a display
atlas built during its stroke run. No such atlas was ever built for this subject.
Synthesizing one would be inventing a channel rather than exporting one — the X2
clause applied to the half that is missing — so `owner_view` is omitted from the
channel list and from every render entry, while the numeric channel and both
per-view products ride in full. The manifest and `x3_run.json` both say so.

### 3.3 What the tree contains

509 files, **290 MB**, at `E13_stroke\export\turnaround\`.

| | count | MB |
|---|---|---|
| `.png` | 367 | 120.5 |
| `.npy` | 31 | 125.5 |
| `.json` | 110 | 0.1 |
| `.glb` | 1 | 43.9 |

Per view: `asset.png`, `prov.png`, `silhouette.png`, `prov_class_<vid>.png`
(born indexed), `owner_id_<vid>.npy`, `loss_mask_<vid>.png`,
`admission_<vid>.json`, `cam.json`. Plus the copied `mesh.glb`, `atlas.png`,
indexed `provenance_atlas.png`, `view_owner.npy`, `styled_mask.npy`, the eight
clay↔twin pairs, `tone_transform_operands.json`, `_operands_sources/`, and
`x3_run.json`.

99.3 MB of that is `_state` emit scratch. **The galleon's tree carries the same
shape** (757 files, 365.4 MB, 88.8 MB scratch), so this is precedent-consistent
and not a deviation — recorded because the lane holds sha-pointers into these
directories and their size is part of the durability commitment.

### 3.4 Per-view class shares

| | reference | brush | dilation |
|---|---|---|---|
| 24 eye-level yaws | 84.49 – 90.94 (mean 87.80) | 1.92 – 7.41 | 6.27 – 10.49 |
| `y+000_e+55` | 69.96 | 7.89 | 22.09 |
| `y+180_e+55` | 81.92 | 3.78 | 14.23 |

The eye-level mean 87.80% sits beside Ruling 27e's 87.49% reference-of-reachable
— a different denominator arriving at nearly the same number, which is what the
ruling's framing predicts and is reported here as a coincidence of construction
rather than a second measurement of the same thing.

---

## 4. Task 3 — the manifest

`asset-source.json`, sha256 `7ea3771013f1ee43…`, 18,399 bytes, schema
**1.3.0**, asset id `e12_dragon_dense`, 26 renders, 5 channel declarations, **no
`renders[].generation` block anywhere**.

### 4.1 The reference view — re-checked, not asserted from memory

The dispatch orders this and it holds, from two independent records:

- `E12_gate0\frame_00003.json`: `"step": 45.0` with `"views": [0..7]`, so view
  index *n* is yaw 45*n* — **view 1 = yaw 45**.
- `harmonize\operands.json`'s own `_reference` is
  `dragonclay_1_twin_v9.png`, labelled `v1`.

The manifest derives `reference` from the view index through the same
construction that makes render ids, giving `y045_e00`, and the lane confirms it
resolves to a declared render.

### 4.2 ⚠ The operands: a decision the dispatch did not anticipate — flagged for the ruling

Addenda 4 and the dispatch both speak of "the recorded per-view harmonization
operands file", singular. **There are two, and the ruled projection input set
draws from both.** From the recorded invocation `E13_stage1\run_stage1.ps1` (the
A0 run, ruled stage 1 by Ruling 24):

- seven views from `harmonize\operands.json` (v0, v1, v2, v4, v5, v6, v7)
- **view 3 from `harmonize\operands_v3r.json`** — the 770701 cure, harmonized in
  a second pass because Ruling 23f adopted it after the first harmonization ran

`operands.json`'s own v3 row describes the **superseded** 770700 artifact.
Declaring that file alone would have pointed the lane at operands that did not
produce one of these projection sources — a false provenance claim, and worse
than a gap.

**What I did:** assembled `tone_transform_operands.json` carrying exactly the
eight rows A0 consumed, each **verbatim** from its source, each tagged with
`_source_file` and `_source_key`, under three assertions per row — the row exists
under its recorded key; the harmonized PNG it names is on disk; and that PNG's
sha256 equals the row's own `sha256_out`, so the operands describe the file that
was projected and not a namesake. Both source files are copied unchanged into
`_operands_sources/` with their shas recorded, so a ruling that prefers a
different declaration costs no re-run.

**This is the executor's construction, not a ruled one.** The alternatives were
(a) declare `operands.json` alone and carry a wrong v3 row, or (b) declare
nothing and take the gap. I took neither; the advisor may.

Incidental confirmation from the assembly's own checks: the reference row's
`mean_correction` is `[0,0,0]` and its `sha256_out` equals the raw reference
twin's hash — the transfer's identity property, arriving from a file this session
did not write.

### 4.3 The palette, and the third suspension translation

Read from canon at runtime. `min_chroma: 12.0`; one band, `warm-olive`
`[85.4, 147.3]`. Canon suspends **both** gate bounds. The lane allows null for
`max_offpalette_pct` and requires an integer for `max_offpalette_blob_px`, so the
blob suspension is translated at the boundary into the whole-atlas sentinel
**16777216** — a value no connected component can reach, gating nothing,
unmistakable for a measured threshold. Third application of the E04 Ruling 29
pattern, and the tool halts if canon ever grows a real bound underneath it.

The suspended blue-violet stratum (273.4–293.4) is **not** exported as an allowed
band, for the same reason canon keeps it in a key `palette_gate.py` does not read
(Ruling 15c): a suspended band in a consumed list is a silently armed band.

### 4.4 The lane's reading — zero gap notices, first run

`sdlab asset ingest <tree> --project facet-assets --dry-run`, run from the lane's
own codebase. **26 registered, 0 rejected, dryRun true.**

Notices, complete:

| code | kind |
|---|---|
| `ASSET_TONE_TRANSFORM_DECLARED` | info |
| `ASSET_RENDERS_ARE_DERIVATIONS` | info |

**Gap notices: 0.** Exactly the pair THE DRAGON SHAPE test asserts.

The lane's own acceptance test was then run read-only:
`node --test tests/lib-asset/asset-style-provenance.test.js` → **34 pass, 0
fail**, THE DRAGON SHAPE among them. The contract has not drifted between what
facet was told and what the lane accepts.

**The lane repo is untouched** — `git status --short` empty before and after.

Two things the lane checked that this session did not have to: the npy
declarations (`view_owner` `|i1` `[4096,4096]`, `styled_mask` `|b1`
`[4096,4096]`) were proved against actual file bytes by a different codebase, and
the containment of every declared path including the operands sidecar.

**Off-palette diagnostics** the dry-run reported, quoted because they are new
numbers and because both bounds are suspended so they gate nothing: per-view
off-palette **1.90% – 9.19%**, largest blob **985 – 15,333 px**, quietest
`y180_e00`, loudest `y270_e00`. These are diagnostics on a subject whose bounds
were deliberately never derived; no bound is proposed here.

---

## 5. Predictions, scored

| # | prediction | outcome |
|---|---|---|
| P1 | 26 cameras (**not blind** — read from the profile) | **right**, 26 |
| P2a | HEAD tool differs from the committed galleon manifest by exactly `renders_are` | **right**, and no second difference on either prior subject |
| P2b | modified tool byte-identical with no new declarations | **right**, 0 bytes differ |
| P3 | zero gap notices at 1.3.0, first run | **right** |
| P3b | if anything fires it fires on `tone_transform.reference` | **untested** — nothing fired |
| P4 | numeric owner present, display absent (**partly not blind**) | **right** |
| P5 | purity spot check byte-identical | **right** |
| P6 | eye-level 60–85%, elevated 25–55%, drop **larger** than the ship's | **WRONG, three ways** |
| P7 | view 1 = yaw 45 | **right**, from two records |
| P8 | `operands.json` is the file addenda 4 means | **WRONG as stated**; the registered risk was the real answer |
| P9 | tree 1.0–2.5 GB | **WRONG**, 0.28 GB |
| P10 | 0 credits, no GPU, 15–45 min | credits and GPU **right**; wall clock **WRONG**, 2 m 36 s |

**P6 is the one worth keeping.** Measured eye-level reference is 84.49–90.94%
against my 60–85%, and the elevated pair reads 69.96% and 81.92% against my
25–55% — and the drop from eye-level to elevated is **smaller** than the ship's
(the galleon fell 82–92% → 61–68%), where I predicted larger. The error was
conflating two denominators: I reasoned from dilation's 52.78% share of the
*atlas* and predicted what an elevated camera would *see*. Those are different
quantities, and Ruling 27e says so in the sentence I was reasoning from — the
animal hides half of itself from eye level, but what it hides is undersides,
interiors and the crevice, not the wing tops an elevated camera looks at. A
camera's visible-figure share is not readable off an atlas share, and I predicted
as though it were.

P9 and P10 were both over by large factors in the same direction — I costed a
1792×1024 render tree as though it were a 4096² one.

**My own slip, owned:** the `09c4960` commit message uses "proved" twice, a word
CLAUDE.md's executor rules put out of bounds for reports, commit messages and
docs. The statements it attaches to are factual (an assertion compared two
sha256s), but the word is on the list and I used it. This report says "checked"
and "asserted".

---

## 6. The durability line

`E:\AI\training\facet_next\E13_stroke\export\turnaround\` **joins the must-not-move
list**, beside the two E11 addenda already names:

- `E:\AI\training\facet_next\E04_stroke\export\turnaround\`
- `E:\AI\training\facet_E08\ARMB\export\turnaround\`

The lane ingests mesh, atlas and every texture-space channel as
`materialized: false` — sha-verified pointers into these trees. The dataset's
hold on those channels depends on the directories continuing to exist, and they
belong in any backup that claims to cover the dataset. One exception rides the
other way: `tone_transform_operands.json` is **materialized** at ingest by the
lane's own 1.2.0 rule, so the operands survive independently of this tree.

---

## 7. What is NOT established, and what is open for the ruling

- **The operands assembly (§4.2) is the executor's construction.** It is the one
  place this session decided something the dispatch did not name. Both source
  files ride beside it unchanged, so any other disposition is free.
- **`renders[].tone_transform`** (the per-render boolean opt-in the lane offers)
  is **not** emitted. It is optional, it would be accurate on every render here,
  and the dispatch says to invent no field addenda 4 does not name — so it was
  left out. Named in case the advisor wants it.
- **The `renders_are` wording field now exists on one subject only.** The galleon
  and W3 manifests still lack it (Ruling 3 declined to churn validated trees);
  the standing errand that re-emits them with `identity.subject_name` would add
  it there too.
- **No ingest was performed.** The Director's lane-side paste is the next act, and
  the dry-run's digits are what a live run should reproduce.
- **The `_state` emit scratch** (99.3 MB, galleon-consistent) is undeclared
  working output inside a tree the lane will point into. Not a problem this
  session found a reason to fix; recorded so nobody discovers it later as a
  surprise.
- **Read-only claim, how it was checked:** `find … -newermt "2026-08-07 01:45"`
  over `E13_stroke\run`, `E13_stage1`, `E13_twins` and `E12_prep` returns empty
  after the run. The check is mtime-based, which would not catch a
  write-then-restore; nothing in this session's code path opens those files for
  writing, and the copies are reads.

---

## 8. Standards compliance (this run)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the recipe is `run_export.ps1`, not the transcript; camera set read from the profile at runtime; every declared value carries its named source (§1.2); manifest and operands sha256s recorded; predictions hashed blind at `0ac88fa` before any measurement |
| ANDON_AUTHORITY | 3 | the capability anchored on two prior subjects before first use; class counts halt against the ruled mix; owner/claim agreement halts; 16 recorded-artifact anchors; the plumbing committed alone so the baseline was measurable before the declarations existed; the palette translation halts if canon grows a real bound |
| NAMED_COMPENSATORS | 3 | read-only inputs throughout, checked after the fact; `--no-copy` added so the anchor could not write into a prior subject's tree; anchor outputs went to scratch; no ingest, no lane-repo write, nothing irreversible; undo is deleting one new directory and reverting two commits |
| DECOMPOSE_BY_SECRETS | 3 | facet declares, the lane judges shape — the seam held, and the lane caught what facet cannot self-check (npy dtypes against bytes, path containment); palette read from canon rather than transcribed; the reference id derived through the id construction rather than typed |
| UNCERTAINTY_GATED_HUMANS | 3 | the ingest stays the Director's paste; the one under-specified decision is flagged with its alternatives and its sources retained rather than resolved silently; nothing ranked or recommended |
| EXTERNAL_VERIFIER | 3 | the lane's validator and its DRAGON SHAPE test are a different codebase judging this output, and both were run; the 16 byte anchors are against artifacts this run did not produce |

**Reported, not ruled. The session stays open.**
