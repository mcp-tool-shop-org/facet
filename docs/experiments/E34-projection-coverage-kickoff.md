# E34 — projection coverage on the performer

**Seat:** advisor · **Dispatched:** 2026-08-13 · **Priority:** ⚑ TOP — set by the Director's
word, 2026-08-13 ([known-defects.md](../known-defects.md), final entry; the priority commit
`ea34a45`). Frame confirmed contrastively with the Director before dispatch: **views-first
repair**, brush out of scope, no invented pass condition.
**Halts at:** `E34-projection-coverage-report.md` · **Predictions:** `E34-predictions.md`,
registered blind before stage 1 runs.

---

## The question

Six of the E33 performer's eight turnaround views carry unpainted texture-projection
patches — jaw, temple, shoulder, ribcage, flank; views 0 (front) and 4 (back) measure
clean. armature measured them twice (flat-alpha survey, then an RGBA-true re-render
proving texture truth), then watched them propagate into hosted-tier generations at the
same landmarks. **Does extending the performer's twin set from two views to the route's
eight, in the approved R3 register, remove them — judged by the Director's eye on the
repaired views?**

## What the record already establishes — the mechanism is not the mystery

[E33-report.md](E33-report.md) §14b–c, in its own words: the performer was projected from
**two twins only** (y+000, y+180 — the six twin candidates were three *registers* × two
views), the brush stage was **deliberately NOT RUN** (`texpass_brush.py:71` hardcodes the
saltroad LoRA and a W3 identity prompt; the local ComfyUI venue is the falsified VRAM
position), and **927,492 hole texels were closed by surface-aware dilation alone** —
*"the pale regions visible on the profile views… are dilation-filled surface, not brushed
content. That is a property of a two-view projection with no brush."* The patches sit on
lateral surface no front-or-back camera faces. The eight-view set was deferred **only**
because the register was unruled; the Director has since ruled it: **R3 — unglazed
terracotta, matte sculpted clay, soft studio light, NO LoRA** (E33 §14b, 2026-08-11).
The lever is E08's own measurement: union acceptance is a function of camera count —
eight cameras reached 92.9% of reachable on W3.

**One variable moves: the view count, 2 → 8.** Register, recipe, mesh, route and fill are
pinned. This is the E29 arm shape, applied to coverage.

## Premises — marked measured or assumed (E29's law)

| # | premise | status |
|---|---|---|
| 1 | `turn_clay_300k\` holds 8 clay views at 352×1024; `masks_300k\` holds 8 exact raycast silhouettes + `silhouettes.json` | **MEASURED in E33 §12; re-verify on disk at G0** |
| 2 | `twin_control\` holds controls for views 0/4 only; controls for 1,2,3,5,6,7 do not exist and must be built by the **same builder** that made `armclay_{0,4}_{control,mask}.png` | **MEASURED (absence, E33 §12); builder identity is G1's enumeration** |
| 3 | `e12_make_twin_prompts.py` derives per-view prompts for **all eight views** under E12's ruled view-deletions (Ruling 9d dropped the three face terms on view 4; E12 ran eight views, so its recorded prompt JSONs are the pattern) | **ASSUMED — G1 verifies against E12's recorded eight-view prompts, and against byte-reproduction of `E33-twin-prompts-r3.json`'s two entries** |
| 4 | The R3 recipe: seed 770700 · steps 20 · cfg 2.5 · denoise 0.92 · cn_strength 0.9 · shift 3.1 · euler/simple · 352×1024 · LoRA NONE · `qwen_image_fp8_e4m3fn` / `qwen_2.5_vl_7b_fp8_scaled` / `qwen_image_vae` / `Qwen-Image-InstantX-ControlNet-Union`, all four resolving by exact name on Comfy Cloud | **MEASURED, E33 §7 / premise 8** |
| 5 | `project_twins.py` takes N `--view` args (since `c469b36`); E33's exact two-view invocation is recoverable from the E33 tree/logs | **First clause MEASURED (record); second ASSUMED — G1 recovers it or halts** |
| 6 | The recorded asset `out\performer_textured.glb` = sha256 `9e20ea7d800c0ffd2cff101a5e1bcc01fa13c620bbbe3ef05ae23b093547b1aa`, 21,588,628 bytes; `E33_manifest.json` pins 117 files | **MEASURED at dispatch (hash re-run this session); re-verify at G0 and G8** |
| 7 | Cloud cost ≈ **$0.102/job** GPU-hours (bucket-delta method, attribution caveat E33 §8); partner-API credits zero on this graph | **MEASURED, E33 §8** |
| 8 | 352×1024 is generator-legal (÷16) and covers the worst yaw (0.3340 at view 0); every view fits it | **MEASURED, E33 gate F** |
| 9 | The frame confound does not apply: all controls and twins share one frame, so frame-changes-register (E13-facet) is not in play | **MEASURED by construction (one frame throughout)** |

## Rulings embedded in this dispatch — the advisor's calls, made now

**R-a. `--bg-max-pct`: the E16 Ruling 4e withdrawal GOVERNS unprofiled runs.** E33 §14b
asked this exact question and it is answered here: the ruling withdrew the *condition*
(its stated derivation was measured against a retired reference), not merely a profile
field, and its re-arm condition (derive from clean data at the polish arc's W3 re-make)
is unmet. An unprofiled run therefore passes `--bg-max-pct 100.0` **explicitly, with its
provenance stated** (premise-13 form), and reports the background probe per view as a
diagnostic that gates nothing. `project_twins.py:93`'s resurrected default 2.0 is
recorded as a tooling defect in [known-defects.md](../known-defects.md); **its repair is
NOT this arc's** — it is a route-tool behaviour change wanting its own spec and test.

**R-b. `--reg-iou-min 0.80` stays untouched, and a firing is a HALT, not a tune.** The
number is W3's and `profiles/character.json` says a new subject must not inherit it —
noted, as E33 noted it. If it fires on any view (the thin profile views are where an
area-normalised score can mislead — E32 Ruling 4's law), halt and report the numerator
and denominator separately per view. No threshold moves in this arc.

**R-c. Era flags are not used.** This is new work under today's defaults (the A3
invariant erosion). E30's W3 era-flag re-run is a different subject's unspent remedy and
stays unspent.

**R-d. The recorded asset is not touched.** The candidate lands as a **new artifact**:
`E:\AI\training\facet_E34\out\performer_textured_8view.glb`. Everything this arc writes
lands under `facet_E34\` (plus repo docs/tests); `facet_E33\` is opened read-only and
manifest-verified unchanged at open and close.

**R-e. The register is R3 as recorded, byte-level.** New twins tempt register
"improvement". The prompt stems, negative, and every sampler value are E33's; per-view
variation comes only from the mechanical deletion builder. **The Director's wood-grain
remark stays a recorded note, not a change order** (E33 §14b) — no term is added.

## The arc, stage by stage

**Stage 0 — open.** E15 ritual on a scratch `--db` (19/19 or stop). Watchdog heartbeat
advancing. Interpreter pre-check (T18's one-line refusal on bare `python`). Manifests:
the eight protected subtrees (`facet_next`, `facet_E01/E02/E05/E06/E07/E08`,
`saltroad_bake_fix` — 7,312 files / 17,072,807,610 bytes, 0/0/0 or halt) **and**
`facet_E33` against `E33_manifest.json` (117 files, 0 changed or halt). Create
`E:\AI\training\facet_E34\` (scripts create their own output directories).

**Stage 1 — enumerate (G1), then predictions.** Locate in the record: the control
builder and its recorded invocation for views 0/4; the prompt builder's eight-view
coverage; E33's exact projection invocation. **Enumerate before commissioning — three
instances of that law in one prior session were one grep from an unneeded commission.**
If any of the three cannot be recovered, HALT and report — commissioning is the
advisor's call, not this seat's. Then register `E34-predictions.md`, blind, before any
artifact is built: each clause on its own line (write what one counted thing IS before
the number), bands for — holes into finalize (E33 baseline: 927,492 of 2,444,770 valid),
styled/valid and styled/reachable (baselines 62.1% / 84.2%, reachable itself 73.7% at
two views), per-view reg-IoU by view class (front/back recorded 0.8605/0.8475), the
six named landmarks' patch survival (qualitative, per view), and total cloud spend
(ceiling below).

**Stage 2 — controls for views 1,2,3,5,6,7** by the G1-located builder. Per view:
contour ANDON ≥ 500 px, frame exactly 352×1024, mask from `masks_300k` (geometry, never
a key).

**Stage 3 — prompts.** `e12_make_twin_prompts.py` derives all eight views from R3's
recorded stem. **Gate: views 0 and 4 must reproduce `E33-twin-prompts-r3.json`'s entries
byte-exact** — if the machine reproduces the recorded two, the six are the same machine's
output. Builder failure writes no file; halt on any assertion.

**Stage 4 — six cloud twins.** Link topology checked in code before submission (no
self-links, no dangling targets, LoRA node absent, every node reachable from SaveImage);
`dry_run` expected 0 warnings — **a dry_run PASS does not prove link sanity, the code
check is the gate**. One batch of six, seed 770700, hashes pinned per submission
(control + render + returned blob + local file). Credits read before and after (GPU-hours
bucket **and** every partner line; partner lines must not move). **Ceiling: 8 jobs total
this arc.** Re-roll rule: one re-roll per spec-violating twin, new seed, recorded, the
rejected twin stays in the record with its measurement; a second failure on the same
view is a result — halt.

**Stage 5 — the twin sheet, walked before projection (G4).** Eight rows:
clay | control | twin (recorded twins in rows 0/4). Executor walks it at full size. HALT
signatures: material/register discontinuity against R3 (anything glazed, wooden, painted
or painterly), face features on views 3/4/5, keyed-bbox ≥ 98% of frame on either axis
(the E32 blowout rule — `e14_twin_registration`'s own bbox check is measured unreliable,
E33 §10 defect 1, so apply the frame-fraction rule beside it), any twin not 352×1024.
Registration diagnostic per view (suspended halts, as E33 ran it) — with the tool's
eight-label mirror assumption verified before any of its corroboration lines are read
(E33 §10 defect 2 was a six-label crash; eight labels is its design case — verify, do
not assume).

**Stage 6 — projection (G5).** `project_twins.py` with **eight** `--view` args — E33's
recovered invocation extended, every value explicit with provenance per premise-13 form,
including `--bg-max-pct 100.0` (R-a) and `--reg-iou-min 0.80` (R-b). Report per view:
reg-IoU with numerator/denominator, background probe, erosion cost by structure
half-width (E33 baseline y+000: 37.2% in the 4–8 px stratum). Then
`texpass_finalize.py --surface-aware` under the recorded gates (`--max-edge-median 3.0`,
`--max-frac-beyond 5.0`; mean fallback 0 is structural, not a pass — E14 Ruling 31d),
then `bake_hero_pack.py` → the R-d candidate path. Brush: **NOT RUN** (out of scope).
Atlas prep: reuse E33's recorded `bake_hero_prep` output if its state files are in the
tree (same mesh, same cull, same crop — enumerate); rebuild with E33's recorded flags
only if absent, and say which happened.

**Stage 7 — evidence (G7), sheet before metrics.** `turn_render.py` (the
`saltroad_bake_fix` copy, as E32/E33 used) on the candidate: the 8-view set, flat and
default lit. Build the per-view BEFORE/AFTER sheet — E33 view | E34 view | provenance
panel — **before quoting any number from this stage**. `texel_provenance` on the
candidate (and on E33's atlas state if its projection files permit; else the report's
recorded numbers are the before, boundary disclosed): per class, total **and largest
4-connected component** (E28 Ruling 21's form — a single 43k-texel patch and 43k of rim
speckle are different defects). Regression: views 0/4 sheets show no new patches; the
recorded GLB's hash unchanged.

**Stage 8 — close (G8).** Manifests re-run (both, 0/0/0). Count surfaces: **only if
tools or tests moved**, reconcile off `T34.PINS` read at apply time and
`pytest --collect-only` at the tree — never transcribe (two seats hand-listed it; each
missed a different file). New tests take **T66+**. Report lands at
`E34-projection-coverage-report.md`; commits are pathspec-scoped; push only with the
count-surface tests green locally. **No judgment words** — the Director rules on the
sheets and the GLB at his own zoom; the register question is closed (R3) and is not
re-opened by this arc.

## Hypotheses

- **H1 — coverage.** The six added cameras face the named landmarks (lateral surface),
  so the eight-view union pulls the patch texels into the styled class and dilation
  shrinks to residual grazing/interior surface. *Falsifier:* a landmark patch surviving
  eight views is surface no exterior camera faces — that redirects the remedy to an R3
  brush/inpaint question for the Director, not to more views.
- **H2 — register continuity.** R3 holds across intermediate yaws with deletion-derived
  prompts and no LoRA, as E12's register held across its eight. *Falsifier:* a material
  discontinuity on the twin sheet (G4 halt).
- **H3 — regression.** Views 0/4 stay clean; the union re-assigns some ownership but
  introduces no patches at the poles. *Falsifier:* a new patch or off-register material
  on either pole view.
- **H4 — fill health.** Holes into finalize fall from 927,492 (band: the executor's,
  blind); finalize's source-distance gates pass with more margin than E33's 1%, because
  nearer paint exists on lateral surface. *Falsifier:* a fired finalize gate — halt,
  report, never tune.

## Out of scope

The brush stage and any R3 brush configuration (a design decision — it goes to the
Director with this arc's residual-dilation evidence) · the wood-grain note · E30's W3
era-flag re-run (unspent, different subject) · `anchor_check`'s PIL refusal, the identity
envelope's dependency set, the archive-to-`D:` arc (queued) · repairs to
`e14_twin_registration.py` or `project_twins.py`'s resurrected default (recorded
defects; each wants its own commit with tests) · armature's tree (read-only, both
directions) · hosted-tier revalidation (the Director's pricing call, never assumed) ·
anchor tests for the candidate (anchors pin **accepted** behavior; the ruling
commissions them on acceptance).

## Compensators — no skip

| irreversible action | compensator | post-rollback state | owner |
|---|---|---|---|
| ≤ 8 cloud jobs, GPU-hours | **none exists** — bounded before spend: ceiling 8, one batch of 6, per-view re-roll gate, stated in predictions before submission | spend stands; unaccepted twins stay unstaged, recorded | executor (ceiling ruled here) |
| writes under `facet_E34\` | `rm -r E:\AI\training\facet_E34` | as at open (all-new directory) | executor |
| repo commits (local) | `git reset --hard <open-sha>`; pathspec-scoped commits only | tree at open | executor |
| push | `git revert` by commit | origin restored additively | advisor |
| `facet_E33\`, eight subtrees, recorded GLB | **prevention, not undo**: read-only this arc; manifest gates at open + close, halt on any delta | n/a | executor |

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | every local stage pinned (tool + flags + hashes + recorded invocations); cloud models pinned by exact catalog filename with payloads and job ids recorded. Not 3: the venue's weights are server-side and not hash-pinned — the recorded limit of this venue since E04 |
| ANDON_AUTHORITY | 3 | route ANDONs `raise` (E22/E23); G1–G8 each carry halt conditions; two live precedents on this subject of a fired gate reported rather than tuned |
| NAMED_COMPENSATORS | 3 | table above; the one compensator-less act (cloud spend) is bounded before the first submission, which is the E33-ruled form |
| DECOMPOSE_BY_SECRETS | 2 | subject values explicit with provenance (premise-13 form); no profile exists for this class yet — named gap, owner: the Director's profile decision when the class recurs, not this arc |
| UNCERTAINTY_GATED_HUMANS | 3 | frame confirmed contrastively before dispatch; the Director's eye is the acceptance gate; mid-arc contact only on fired gates |
| EXTERNAL_VERIFIER | 2 | texture-space (`texel_provenance`) and render-side (armature's survey, on request post-candidate) are independent instruments in different repos; limit: no different model family grades the twins — by design, the Director's eye decides |

## What the Director will be asked to look at

The per-view BEFORE/AFTER sheets at full size, the candidate GLB at his own zoom, and —
on his word — armature's re-run of its hole survey and RGBA-true turnaround against the
candidate (standing support, zero credits). The report carries no verdicts.
