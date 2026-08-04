# E04 Task 2 — subject profiles. The classification IS the deliverable.

**Executor session, 2026-08-04.** Local only, no GPU, no generation. Spec:
[docs/profiles-design.md](../profiles-design.md), agreed with the Director. Charter, his
words: *"create profiles so that we don't break the humanoid character pipeline to make the
ship."*

**Both pre-registered gates pass.** Byte-identity: three anchors, zero differing pixels.
Completeness: 115 constants classified, 59 profile / 56 code, none unplaced.

**No judgement of any value's quality appears here.** This says which column a constant
belongs in and why; whether a value is *good* was settled at Gate 1 and is not reopened.

---

## 1. The rule that decides the column, stated before the table

> **A value goes in the profile unless there is a stated reason it is subject-independent.
> The burden of proof is on "principle".**

That direction is deliberate and it follows the design note's own logic: *"If E04 needs a
change outside the profile, that is the signal that something in the shared code was never a
principle."* For the signal to mean anything, everything we cannot defend as a law has to be
inside. Over-including costs the ship one decision; under-including costs the character the
path the Director just accepted.

## 2. Gate 1 — byte-identity. The profile is a relocation, not a change.

Three anchors, run with the character profile loaded:

| anchor | result |
|---|---|
| 8-camera stage-1 projection vs `stage1_8cam.png` | **0 differing px** on atlas, `_holes.png` and `_styled_mask.npy` |
| `e08_acceptance` | `anchor OK` — styled reproduces E06's 681,212 |
| `emit` of stroke 1 (`y+090_e+00`) vs its saved job | `render.png`, `mask.png`, `hit.png`, `thin.png` all **byte-identical**; `render.png` sha256 `111232f57681ce1e…` is the value the run log recorded as `render_local_sha256` |

The 8-camera anchor's invocation was not written down anywhere. It was reconstructed from
the 2-camera recipe recorded in E08's intersection regression plus the twins, and it
reproduces the banked atlas to the pixel **before** any profile existed — so the baseline is
established independently of the thing being tested:

```
project_twins.py --prep facet_E06/C1/prep
                 --view 0=facet_E08/ARMB/twins/twin_0.png   ... --view 7=...twin_7.png
                 --edge-absolute
                 --out stage1_8cam.png
```

**The emit anchor is the one that proves the profile is load-bearing rather than inert.**
Run with `--profile` and *without* `--thin-extent 0.03` on the command line, it still
withheld 12,248 px — the value arrived from the file. A profile whose values never reach a
tool would pass a pixel comparison trivially.

### The byte-identity gate is narrow, and one error slipped past it

It exercises three code paths. It never runs `cull_unseen`, `bake_hero_prep`,
`smart_decimate`, `restylize_views` or the render tools, so a mistranscribed value in any of
those would sail through. **One did.** I wrote the character's ten cameras into
`cull_unseen --production`; that flag defaults to a **24-yaw 15° sweep plus the elevated
pair** — deliberately denser than any subject's camera set, because the visibility
classifier must cover cameras nobody has added yet. The profile would have narrowed a safety
superset into a subject list, and no gate in the dispatch would have noticed.

Caught by reading, then made mechanical:
[`e04_profile_check.py`](../../tools/diagnostics/e04_profile_check.py) compares **every**
profile value against that flag's `default=` in the tool's source, statically, for all
tools at once:

```
[chk] character.json: 64 values checked against 11 tools
[chk] PURE RELOCATION: every profile value equals its tool's own default.
```

One argued exception, declared on the command line rather than hidden:
`texpass_iter --thin-extent`, source default `0.0`, profile `0.03`. The tool's default is
"off"; `0.03` is the value the accepted run passed explicitly, and capturing it is the point
— the recipe stops living in a shell history. The emit anchor proves it arrives.

*(That checker had a bug of its own: its first version was not string-aware and stopped at
the comma inside `default="360,240,700,600"`, reporting five sound values as unevaluable.
Fixed before any conclusion rested on it.)*

## 3. Gate 2 — completeness

Enumerated mechanically across twenty route-active tools rather than from memory: every
`add_argument` brace-matched out of the source, its default extracted.

```
PROFILE  59      CODE  56      N/A  91  (required paths, store_true flags, default=None)
```

**115 classified, none unplaced.** The N/A column is required file paths, boolean flags and
`default=None` placeholders — not constants in the sense that matters. Each is listed in §6.

## 4. PROFILE — it was a subject assumption all along

Full values, each with its own `why` and `from`, are in
[`profiles/character.json`](../../profiles/character.json). Grouped by what they actually
are:

| group | constants | why this is subject data |
|---|---|---|
| **The face rect** | `crop 360,240,700,600` + `crop-res 1024`, in **five** tools (prep, smart_decimate, head_render, mesh_stats, and project_twins' head band) | It says where **this character's head is**. It has no referent on a subject without a face. The single most-replicated subject value in the pipeline |
| **Framing** | `aspect 752,1024`, `w/h 752/1024`, `step 45.0`, `views 0..7` | Portrait, fit-to-height, eight even yaws. A galleon is wider than tall |
| **Allocation** | `head-scale 3.0`, `target`, `body-weight 0.8`, `factor 3.0`, `pad-frac 1.5`, `res 4096`, `unseen-strip 24.0` | Every one presumes one privileged region and one everything-else |
| **Acceptance** | `facing-min 0.45`, `head-facing-min 0.18`, `edge-dist 7.0`, `head-edge-dist 3.0`, **`edge-ref 700.0`**, `edge-floor 2.5`, `edge-min-struct 50`, `power 6.0` | `edge-ref` is literally **one character's figure width in twin pixels, used as a denominator for every subject**. The head variants encode that a privileged region exists |
| **Brush** | `facing-min 0.25`, `edge-dist 4.0`, `mask-dilate 9`, **`thin-extent 0.03`** | `thin-extent` was sized to a **greatsword** — the smallest value filling the blade solid. Rigging is thinner by an order of magnitude |
| **Halts** | **`reg-iou-min 0.80`**, `bbox-tol 0.25`, `bg-de 10.0`, `bg-max-pct 2.0`, `min-seen 0.30`, `max-seen 0.90` | `reg-iou-min` was derived from **both sides of a measured line on W3's twins** (0.8329–0.9533 against failures ≤ 0.578). A new subject has neither distribution |
| **Generation recipe** | `seed 770700`, `steps 20`, `cfg 2.5`, `denoise 0.92`, `lora-w 0.75`, `cn-strength 0.9/1.0`, `canny 0.4/0.8`, `contour-width 3` | Validated against this subject's twins. Not principles, and not obviously portable to a hull |
| **Identity** | `--prompt` and `--negative` in **`restylize_views` and `texpass_brush`** | See §5 — this is the finding |
| **Fixtures** (referenced, not copied) | the W3 palette JSON (bands, `min_chroma 12.0`, `blob 800`), twin prompts, brush prompts | Already versioned files before profiles existed. The profile **points** at them: two copies of a threshold is how a threshold drifts |

## 5. The finding: a character's identity was a default in two shared tools

`restylize_views.py` and `texpass_brush.py` both default `--prompt` to:

> *"a burly bald warrior with a long red beard, dark green knitted sleeveless tunic, polished
> gold pauldrons, gold necklace, dark red layered cloth skirt with a leather belt, heavy dark
> boots, holding a massive greatsword…"*

This repo's central architectural result is that **identity belongs to the prompt** — the
prompt beat mesh, LoRA and control on 8 of 8 contradicted elements at a 7.4× separation. So
that string is the most subject-specific object in the entire pipeline, and it was sitting
as a fallback default inside the two tools any future subject must run.

It is harmless on the accepted route, which passes per-view prompts from a file and never
reaches the fallback. It is not harmless for E04: **`restylize_views` run on a galleon
without `--prompts` asks the model for a bald warrior.** Relocated to the profile at the
identical value (so the relocation stays pure); the code default is left standing because
changing it is a behaviour change, and the ship profile must override it. Recorded here as
the trap it is.

## 6. CODE — real principles, and the argument for each

| constant(s) | tools | why this is NOT subject data |
|---|---|---|
| `bias 3e-3`, `noffs 1.5e-3` | cull_unseen, project_twins, texpass_iter | Ray-offset epsilons in a normalised frame. Numerical, not geometric |
| `bound 0.55` | prep, smart_decimate, head_render, mesh_stats | The std-frame half-extent **convention** every tool shares. Changing it per subject would desynchronise five tools |
| `edge-frac 1/3` | project_twins | **A3's invariant.** Erosion may never exceed a third of a structure's own local half-width — bounds over-erosion *by construction*, and for a bar the area removed equals it exactly. A derived law, not a tuned number |
| `max-edge-median 3.0`, `beyond-edges 20.0`, `max-frac-beyond 0.05` | texpass_finalize | Stated in **median triangle edges**, and the edge length is measured from *this* mesh at run time. The unit normalises the subject away |
| `cameras 46`, `production` (24-yaw sweep), `rings 1`, `samples 4`, `raster-res 1504`, `iou-res 1880`, `iou-cameras`, `max-recession 1e-3`, `max-missed-area 0.005` | cull_unseen | A visibility **superset** construction plus its gate. `iou-res` is deliberately different from `raster-res` so the gate samples a different grid than the classifier — equal values would make it a tautology |
| `island-margin 0.001`, `pack-margin 0.001` | bake_hero_prep | A function of atlas resolution and chart size, not of who the subject is. ⚠ Re-measure if a subject's chart statistics differ materially — 0.004 took packed coverage to 4.01% where 0.001 gives 18.76% |
| `angle-limit 1.15` | bake_hero_prep | **Off-route** (only reached under `--reunwrap`; native UVs are the default) and independently falsified — it moved chart count 0.8% |
| `tol 0.06`, `erode 5` | restylize_views | ⚠ **Kept in code as a known defect, not as a principle.** The 0.06 key is the global constant that excludes the greatsword band in every view (median residual 0.0645–0.0657 against the 0.06 cut). Making it a profile value would let each subject tune around a broken mechanism instead of fixing it. It belongs to the blade arm |
| `hole-grey 0.42` | project_twins | ⚠ **A design collision, recorded and unchanged** per the dispatch. It equals emit's background fill by construction, so an unpainted hole on real surface is indistinguishable from background *by colour* — which produced a false ANDON in E08 and cost a void. The remedy is to read geometry, which every instrument now does; separating the two constants is a design note, not this task |
| `exposure 0.85`, `bg 0.181,0.181,0.188` | turn_render | Matched to the reference renders these must line up with; `bg` is derived by `e08_bg_derive.py` rather than chosen |
| `weld-dist 1e-5` | smart_decimate | Merge-by-distance epsilon. Physics of the seam-split export |
| `tol 1.0`, `conc-tol 4.0`, `dilate 9` | brush_cloud_step | ANDON bounds in 8-bit levels. Sub-unit is a codec boundary |
| `host`, `model` paths, `tag`, `yaw-offset 0.0`, `scale`, `grid 256`, `curv-samples 4000`, `views 4,5,6` | various | Endpoints, filename labels and instrument sampling density. Not behaviour |

## 7. Borderline cases, argued rather than filed silently

- **`res 4096` (atlas)** → **PROFILE.** Arguable as a production-tier constant shared by
  every subject. Filed as subject data because a galleon at the same texel density has a
  different surface area, so the number cannot be right for both by construction.
- **`power 6.0`** → **PROFILE.** It does **not** affect ownership (argmax is invariant under
  a monotone power), only the facing-weighted blend. Filed as profile because it trades
  softness against ghosting and that is a look decision.
- **`facing-min 0.45`** → **PROFILE.** Sixty-three degrees is defensible as a general
  obliqueness limit, which is a real argument for "code". Filed as profile because nothing
  in the record establishes it as subject-independent, and the burden is on "principle".
- **`island-margin`/`pack-margin`** → **CODE**, with a re-measure warning. The mechanism is
  atlas-resolution arithmetic; the *optimum* depends on chart statistics, which is a mesh
  property. Closest call in the table.
- **`min-seen 0.30` / `max-seen 0.90`** → **PROFILE.** They bound what fraction of a subject
  is interior surface. A hull hides a whole below-decks; a standing figure hides finger gaps.
- **`smart_decimate` block** → **PROFILE, marked `DECLARED, NOT AS-RUN`.** The accepted
  asset never passes through this tool — E06's recipe hands `cull_unseen` and
  `bake_hero_prep` the already-decimated `W3_287k.glb` directly. Its constants are still
  subject data, but no byte of the accepted asset depends on them, so `target` carries the
  tool's own default rather than any run's value. Recorded because my first draft wrote
  `150000` there, which is an experiment's number, not the route's.

## 8. Corrections to inherited claims

**The dispatch's seed list is stale on one item.** It lists *"`texpass_finalize`'s hardcoded
triangle-edge length (E07 flagged it; per-mesh)"* as a constant to classify. It is **already
per-mesh** — `texpass_finalize.py:95-106` loads `prep_uv.glb` and takes the median edge
length from that mesh at run time, with a comment saying exactly why: *"The scale must come
from THIS mesh — a hardcoded constant is the same family as the blade pixel-rectangle the
loop was rewritten to remove."* Fixed before this task; classified as CODE because the unit
normalises the subject away.

## 9. `profiles/ship.json` — a draft whose absences are the content

Drafted from the design note's stressor table. **Most of it is deliberately empty**, and
that is the deliverable rather than a gap:

- **Measured:** all three staged concepts are **1216 × 1024 = 1.188 W/H**. The frame is
  landscape, confirming that half of the stressor table.
- **Not measurable yet, and not guessed:** the *subject's* aspect. A corner-median key over
  all four corners returns the **full frame** as the subject bbox on all three concepts
  (fill 64.2 / 67.5 / 79.3%) — they are clay renders on a soft gradient with a cast shadow,
  the exact configuration this repo has recorded keying failing on three times. **Keying was
  not retried with a different threshold.** The subject aspect is suspended until Task 3's
  mesh exists, and is then read off geometry. A landscape *frame* does not establish that
  the *mesh* is wider than tall, and `fit_axis` keys off the mesh.
- **SUSPENDED, named individually:** `reg-iou-min` (needs both sides of a measured line on
  its own twins), `bbox-tol`, the whole framing group, the whole allocation group, the
  camera set, `thin-extent`, the acceptance family, the generation recipe.
- **Required and not written:** the galleon palette fixture. On this subject the off-palette
  gate carries weight no eye can, and the W3 palette — red beard, gold pauldrons, green
  knitted tunic — must never be pointed at a ship.
- **Recorded as a decision, not an omission:** `mesh_gate: none`, `head_rect_metrics: false`.

**The sharpest entry is `thin-extent`.** `0.030` is the smallest value that fills a
*greatsword* solid. Ratlines, shrouds and stays are visible as single-pixel lines in all
three concepts. Inheriting the character value would not be merely unportable — it would
hand the entire rigging to the diffusion brush.

## 10. E04 Ruling 2 — `project_twins` now saves what it computes

Both objects existed at projection time and were discarded. Task 1 had to reconstruct the
ownership map from `diag_8cam`'s accepted sets, and could not obtain the blend at all — which
is exactly the "shading versus content" split that report marks as not established.

- `<out>_owner.npy` — int8, which view won each texel, −1 unstyled.
- `<out>_blend.png` — `B`, the facing-weighted blend. Its difference from the ownership map
  is precisely what the σ=16 levelling corrects at low frequency, so *"why did levelling not
  touch a ΔE 13 step"* becomes answerable from disk.

Additive: written after the atlas, from copies. The 8-camera anchor was re-run **after**
adding them and is still 0 differing px.

**The sidecar immediately corrected Task 1 in place.** Against ground truth, that report's
ownership reconstruction is wrong by **one texel of 2,402,810** — index 1,786,017, where
`y+180` and `y+225` differ by 2.3e-8 in float64 and round to the *identical* float32 that
`project_twins` actually compares, so the strict `>` keeps it with the earlier view. Nothing
in Task 1's conclusions moves; the correction is recorded there with the measurement.

## 11. What was NOT done, and why

- **`texpass_loop.ps1` is not profile-wired.** Its `$default_order` spiral is subject data
  and belongs in a profile, but it already reads `_order` from the prompts JSON — which the
  profile references as a fixture. Wiring PowerShell to the Python loader would add a second
  mechanism for one value already externalised. **Recorded as a deliberate gap**, not an
  oversight.
- **Diagnostics under `tools/diagnostics/` are deliberately not wired.** They exist to
  reproduce historical numbers; a profile that could shift `e08_acceptance`'s floors would
  let a future session move an anchor. `e08_acceptance` is run here unwired and lands 681,212.
- **No code default was changed.** Every relocation carries the same value, including the
  identity prompt, so `git` shows no behaviour change to argue about.

## 12. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Three byte-identity anchors, one of them a sha256 that matches the run log's independently recorded value; the 8-camera invocation reconstructed and verified against the banked atlas *before* the profile existed; `e04_profile_check` pins every value to its source default statically |
| ANDON_AUTHORITY | **3** | The loader raises on an unknown key, a missing `why`, a missing `from` and a malformed entry; `e04_profile_check` exits non-zero on any mismatch and did, catching a real error |
| NAMED_COMPENSATORS | **3** | Additive only — new files plus one-line wiring; `git` is the undo; `ARMB/state` and every banked atlas untouched, verified by re-running the anchor from scratch state copies |
| DECOMPOSE_BY_SECRETS | **3** | This task *is* that standard applied. 115 constants argued into two columns with the burden of proof stated before the table, borderline cases carrying their argument |
| UNCERTAINTY_GATED_HUMANS | **3** | The ship profile suspends rather than guesses, names each suspension, and states what must be measured to lift it. The one place a number could have been invented — the subject aspect — is left empty with the reason |
| EXTERNAL_VERIFIER | **2** | `e04_profile_check` checks the profile against a source of truth its author did not write; the emit anchor is checked against a hash recorded by a different session. No second model — `skip:`, as the dispatch allows |

---

**Both gates pass. Proceeding to Task 3.**
