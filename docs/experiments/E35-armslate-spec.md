# E35 — THE ARM SLATE (spec)

**Ordered by the Director, 2026-08-14.** ⚠ **Written at the EXECUTOR seat**, working from
the ruling in the kickoff tail at commit `e56eb3d`. It is a working spec — the arms, the
commands, the pre-registrations and the halt — **not a ruling**. Nothing in it decides what
a result means; that is the Director's, on the sheet.

⚠ **Seat error, owned:** the first version of this file and its kickoff fold were written in
advisor voice and pushed as a ruling (`2aa5952`). The seat was the executor's the whole time.
Content unaltered — it is enumeration and measurement — attribution corrected here and in the
kickoff block rather than deleted, because the correction is more useful than the original.

This is a **sub-arc of E35, not E36.** Nothing here creates an experiment number, so
`docs/index/conventions.json` `laws.paid_for_by` is **not** bumped and T24's span leg does
not fire. Said here so nobody helpfully creates E36.

**The order, verbatim:** view 1, seed 770700, single lever per arm, all else pinned at the
recorded recipe — (a) `euler_ancestral` · (b) flat-lighting positive vocabulary ·
(c) depth control · (d) the best pair of (a)–(c) combined, on their measurements. Per arm:
register C\* + dark census + pale measure, full-size sheet beside the recorded twin, blind
bands first. **HALT at the sheet for the Director's eye.** Budget 4 jobs → 37/45.

---

## ⚠ Three things the advisor's enumeration changed before this went out

At the top because two of them alter what the executor builds, and one is a citation this
seat had to resolve against its live source rather than repeat.

**1 — `consult #1` carries no synthetic-depth guidance. There is none anywhere in this
repo.** The order says "strength per consult #1's synthetic-depth guidance."
[comfy-consult-1.md](../comfy-consult-1.md) is 132 lines on despeckle nodes, mechanism
ranking and levers; its only ControlNet-strength line is Q2 lever #2 (`cn 0.9 → 0.6–0.7`),
which **R2-c has since struck as counter-indicated**. A grep for `synthetic` across
`docs/**/*.md` returns eight hits, every one about flat grey backdrops. **So the depth arm's
strength is not derivable from a consult, and inventing one is precisely the "condition
whose stated derivation does not describe it" failure.** The strength therefore stays at the
**recorded 0.9 / start 0.0 / end 1.0** — which is also the only value that keeps arm (c) to
one lever. If the hint modality is the variable, the strength cannot be.

**2 — the depth render needs no Blender script, and should not have one.** The order says
"author the view-1 depth render (Blender -b, recorded script)." Two measured facts against
that. `turn_render.py` runs `BLENDER_WORKBENCH` (`tools/verify/turn_render.py:121`), which
has no Z pass — so a Blender depth render means changing the engine, i.e. a *different*
camera pipeline from the one that made the init. And `tools/silhouette_masks.py` **already
raycasts this mesh at exactly turn_render's camera**, verified against it rather than
assumed (its docstring derives `cam.location` / `cam.rotation_euler` from turn_render's own
lines, and `--anchor` asserts byte-identity against known-good masks) — and at
`silhouette_masks.py:129-131` it computes `cast_rays(...)["t_hit"]` **and throws everything
away but `isfinite`**. The camera is ortho (`turn_render.py:92`), so `t_hit` *is* linear
depth along the view axis. The depth map is one already-computed array away, on the
instrument that produced the mask this whole arc has used, with an anchor flag that proves
the edit non-perturbing. A fresh Blender script would re-derive a camera this tool has
already verified — and a re-derived camera is where this repo bleeds.

⚠ **Fourth instance of *enumerate the resource before commissioning one*** in two sessions
(`e12_offsurface.py`'s nine flags · a model already on the rig · `--edge-absolute` at
`project_twins.py:103` · now `t_hit` already in the raycaster). Each was one grep from a
commission, and the commission is always the expensive branch.

**3 — arm (b) does not ADD lighting vocabulary; it REPLACES a term the Director ruled.**
The view-1 positive prompt's sixteenth and last term is already **`soft studio light`**, and
[E34-twin-prompts-r3-8view.json](E34-twin-prompts-r3-8view.json) `_register` records it as
part of R3 *"as ruled by the Director 2026-08-11."* Two consequences. The lighting surface
is **occupied**, and this repo has measured what happens when a specification adds a second
element to an occupied surface: **no response at all, ΔE 1.07, in two grammatical forms.**
Appending a flat-lighting term would most likely measure nothing and be reported as "the
lever does not work," which would be false. So arm (b) is a **one-term substitution** — and
it edits a ruled register term, **the Director's call, not the executor's**, flagged here so
he can veto arm (b) alone without touching the slate.

---

## The question

Consult #4 nominated three levers acting on the two open defect classes. R2-c then measured
that **conditioning strength is an anchoring term** — the pale class is the clay init
surviving where the sampler is least anchored (pale rises +235% / +339% as cn weakens; down
the ladder the pale marches toward the measured init on both axes, L\* → 76.43, C\* → 1.12).

**Does any single lever move the dark class, the pale class, or both, at a register the
Director will accept — and do the two best combine?**

Nothing here decides acceptance. The arms produce four twins, four measurement rows and one
sheet. **The Director's eye rules.**

---

## The baseline — view 1, seed 770700, the recorded recipe

Each number with its source, because the arms are graded against these and two of them are
easy to confuse with an eight-view mean.

| quantity | value | source |
|---|---|---|
| pale area | **278 px²** | R2-c, recorded arm (`facet_E35/diag/r2c_pale_vs_levers.json`) |
| pale L\*-rise | **4.97** | same |
| dark census (twin) | **16** components / **157 px²** | task 1 baseline, E35 report §2a |
| register C\* | **23.77** | task 2, E35 report |
| register IoU | **0.9372** | same |
| clay init, head | **L\* 76.43 · C\* 1.12** | R2-c, measured alongside |

⚠ **Do not grade against R2-a's 770700 row (pale 734.5 / rise 11.67 / dark 170.4).** That is
a **mean over eight views**; these arms are **one view**. Same instrument, different
population — the unit/population family has taken nine consecutive arcs in this repo.

**The register failure continuum, measured** (2b ladder, same view and seed): C\* **10.00 /
3.91 / 1.89** at denoise 0.85 / 0.80 / 0.72 — rungs the Director's own ruling calls register
death. **The healthy cluster, measured across every arm that held**: 22.40 / 23.77 / 24.29.
Both are used below; neither is a number this spec chose.

## The recorded graph — what each lever touches, traced

Base: `E:\AI\training\facet_E34\twin_payloads\payload_r3_v1.json`, 15 nodes.
Qwen fp8 UNET · `qwen_2.5_vl_7b_fp8_scaled` CLIP · `Qwen-Image-InstantX-ControlNet-Union` ·
`ModelSamplingAuraFlow` shift 3.1 · KSampler seed 770700, steps 20, cfg 2.5, `euler`,
`simple`, denoise 0.92 · `ControlNetApplyAdvanced` strength 0.9, start 0.0, end 1.0 ·
frame **352×1024** (÷16, generator-legal, derived in E33 §F).

*"One variable is a property of the dependency graph, not of the parameter you edited"* — so
each lever's consumers were traced, not assumed:

| lever | node.input | who else consumes it |
|---|---|---|
| (a) sampler | `13.sampler_name` | nothing — KSampler is terminal on that input |
| (b) prompt | `7.text` | `11.positive` only |
| (c) hint image | `10.image` | `11.image` only |

All three are one input with one consumer. **Any pair is therefore constructible without a
topology change** — which is what makes (d) a pair rather than a rebuild.

---

## The arms

Every payload is emitted by `payloads/make_payload.py` (it raises on an unknown node or
input, writes the override dict beside the graph, and checks link topology in code) and
**submitted verbatim**. No hand-retyped payload — E04 Arm G7's self-linked graph passed
`dry_run` and was still wrong.

### (a) `s4a_eulanc` — the sampler lineage arm

```
make_payload.py --view 1 --tag s4a_eulanc --set 13.sampler_name=euler_ancestral
```

Scheduler stays `simple`, steps stay 20, cfg stays 2.5. **Do not "match" the schedule** —
matching two things is two levers. `euler_ancestral` is present in the live 63-option COMBO
(MEASURED, E35 report Premise 4).

**Mechanism, stated so it can be wrong:** an ancestral sampler re-injects noise each step.
That gives the trajectory more to overwrite the init with (→ should attack the **pale**
class, by R2-c's anchoring logic) and breaks up repeatable fine structure (→ may attack the
**dark** class, whose components run 10× the corrector's 36 px² cap and are testimony-ruled
baked AO). Consult #1 ranked sampler last as a *driver*; consult #4 re-nominated it because
its precondition — "the denoise knee costs register" — measurably occurred.

### (b) `s4b_flatlight` — the register-term substitution arm

One comma-term out, one in, position and term count unchanged (16 → 16):

```
soft studio light   →   flat even lighting
```

Everything else in the string **byte-identical**. The new string is versioned as
`docs/experiments/E35-twin-prompts-r3L-view1.json`, built by a script that **asserts** the
new string differs from `E34-twin-prompts-r3-8view.json`'s `armclay_1` by exactly that one
comma-term and by nothing else — no file written on assertion failure. Mark it
`"_status": "PROBE - not a register change; R3 stands unless the Director rules otherwise"`.

The report prints the full before and after strings, not a description of them.

⚠ **No instrument in this slate measures identity.** C\* measures chroma; the censuses
measure defect classes; *is this still the same man* is the Director's ground truth and no
metric approximates it. The report may not use register numbers to imply identity held.

### (c) `s4c_depth` — the depth-hint arm

**Build the hint from the raycaster, not from Blender.** Add a `--depth DIR` output to
`tools/silhouette_masks.py` that writes, per view, the `t_hit` it already computes:

- finite hits only; `u8 = round(255 * (t_max − t) / (t_max − t_min))` over that view's own
  finite hits, so **near = white**; background = 0; emitted **RGB** (grey replicated).
- support **byte-identical** to the mask leg by construction — and asserted, see G3.
- write the inverted map alongside as `*_depth_far.png` in the same run. It costs nothing
  and it is the named fallback if the convention is wrong.

Invocation (`--prep`, `--aspect`, `--anchor` are existing flags):

```
silhouette_masks.py --prep E:\AI\training\facet_E33\prep_300k --out <scratch> ^
  --tag armclay --views 0,1,4 --step 45 --aspect 352,1024 ^
  --depth E:\AI\training\facet_E35\depth ^
  --anchor 0=E:\AI\training\facet_E33\masks_300k\armclay_0.png ^
  --anchor 1=E:\AI\training\facet_E33\masks_300k\armclay_1.png ^
  --anchor 4=E:\AI\training\facet_E33\masks_300k\armclay_4.png
```

Then upload `armclay_1_depth.png` and override the hint:

```
make_payload.py --view 1 --tag s4c_depth --set 10.image=<uploaded name>
```

**Strength stays 0.9, start 0.0, end 1.0** (finding 1). Topology unchanged unless the
enumeration below says otherwise.

⚠ **Two premises this arm rests on, both declared rather than claimed.**

- **The union's modality handling.** The recorded graph applies
  `Qwen-Image-InstantX-ControlNet-Union` through `ControlNetApplyAdvanced` with **no type
  selector**. A core `SetUnionControlNetType` node exists and offers `depth` — but its
  option list (`openpose · depth · hed/pidi/scribble/ted · canny/lineart/anime_lineart/mlsd
  · normal · segment · tile · repaint`) is the SDXL-union table, and a second,
  differently-typed one exists for Shakker Labs. **Whether either applies to a Qwen union is
  not established here.** Before submitting, enumerate: `get_node` on `ControlNetLoader` and
  `ControlNetApplyAdvanced`, and `search_templates` for a served Qwen-ControlNet template.
  **If a served template wires a type node into a Qwen union graph, use that wiring and
  version the revised base payload; if nothing shows it, submit image-only and say so.**
  Report what the enumeration returned either way — this is the arm's largest unknown, and
  it is resolvable at zero jobs.
- **The depth convention.** Near = white is the MiDaS / Depth-Anything convention these
  hints are usually trained against. It is an assumption, not a measurement; name it in the
  report, and the `_depth_far.png` above is why a wrong guess costs no re-render.

### (d) `s4d_pair` — the combination, on a rule fixed BEFORE the results

**This is the part that must not be chosen after looking.** What is forbidden is picking a
decision rule after seeing the outcome, so the rule is here, in the spec, unconditionally.

For each arm X ∈ {a, b, c}, against the baseline above:

```
score(X) = (1 - pale_area(X)/278) + (1 - dark_census_twin(X)/16)
```

Signed, so a class made worse subtracts. Then, in order:

1. **Register exclusion first.** Exclude any arm with **C\* ≤ 10.00**. That constant is not
   chosen — it is the *highest measured value on the register-death side* of the 2b ladder
   (10.00 / 3.91 / 1.89), and it sits below every arm that held (22.40 / 23.77 / 24.29). It
   can only exclude an arm that is unambiguously dead, and it is never re-derived.
2. Let **C** = the surviving arms with `score > 0`.
3. **|C| ≥ 2** → (d) is the **top two by score**, both levers applied to one payload.
4. **|C| = 1** → **(d) DOES NOT FIRE.** A "best pair" of one arm is not a pair. The fourth
   job returns to the ceiling and the slate reports **3 of 4 spent, 36/45**.
5. **|C| = 0** → **(d) DOES NOT FIRE**, same accounting. Three arms and a sheet is a complete
   result, and a negative result is a full success.

Ties on `score` to four decimals break toward the **lower pale area**, then toward (c), then
(b), then (a). Stated so a tie cannot become a judgement call.

⚠ **Three branches, not two.** R2-c's own lesson, folded one commit ago in the executor's
words: *a fork over a signed quantity has at least three branches — state the sign, or admit
it unknown.* Branches 4 and 5 exist because "the levers all fail" is an outcome, and the
slate must be able to return it without improvising a fourth job.

---

## Metrics and the instruments that produce them

| metric | instrument | state |
|---|---|---|
| dark census (twin) | `tools/twin_despeckle.py --mode census` at its defaults | **parameterised already** — `--images / --masks / --out-json`; no change |
| pale area + L\*-rise | `facet_E35/diag/r2c_pale_vs_levers.py` | ⚠ **subject-bound** — module-level `ARMS` list, no argparse |
| register C\* + IoU | `facet_E35/diag/t2b_register_all.py` | ⚠ same shape — read it before writing a command line |

**The pale instrument must be parameterised, not re-implemented.** Add `--twins`, `--mask`,
`--clay`, `--out-json`; keep `HEAD = slice(60, 220)`, `DL = 6.0`, `MINA = 25` and the code
path **untouched**. A cited instrument may be edited here — **no ruling in this repo forbids
it** — under the discipline the record does impose: **prove the edit non-perturbing, in the
commit that makes it.** The proof is an anchor reproducing R2-c's six published rows exactly
(recorded 278 / 4.97 · sched 932 / 12.99 · flat-0.65 1220 / 19.68 · and the three 2b rungs),
printed in the report. If any row moves, that is a fired gate — report it and halt; do not
adjust the instrument until it matches.

**Grade an arm only on what it can move.** All three metrics have already separated
artifacts the Director rejected: the pale measure graded the seed table and the R2-b
candidate, the census is the scorer the selection ran on, and C\* read 23.77 → 1.89 down a
ladder whose geometry survived. None of them returns the same number whether an arm works or
does nothing.

---

## Gates

**On the validity of the measurement, not on the outcome.** The outcome is the Director's,
and a gate that halts before the sheet reaches his eye defeats the arc. Every gate below
`raise`s — never `assert`, which `python -O` deletes silently (E21 Ruling 2 / E22 Ruling 9).

| # | gate | fires when |
|---|---|---|
| G1 | **frame** | any returned twin is not exactly **352×1024** (E04 Ruling 15's VAE truncation) |
| G2 | **single lever** | `meta.json` `overrides_applied` has ≠ 1 entry for a/b/c, ≠ 2 for d, or an entry outside the intended dict |
| G3 | **depth support** | `(depth > 0)` is not **byte-identical** to `armclay_1_mask.png` — this can fail, if normalisation clips a near-plane pixel to 0 |
| G4 | **non-perturbing edit** | `silhouette_masks.py --anchor` mismatches on views 0, 1 or 4 after the `--depth` addition |
| G5 | **instrument anchor** | the parameterised pale instrument fails to reproduce any of R2-c's six rows |
| G6 | **prompt diff** | the r3L string differs from R3's `armclay_1` by anything other than the single term `soft studio light` → `flat even lighting` |

**Deliberately NOT gated, and why**: register C\*, the two censuses, and everything about how
the twin looks. Those go on the sheet. C\* enters only as (d)'s *exclusion* at the measured
register-death value, and even there it selects a payload — it does not stop the arc.

**A fired gate is reported with its evidence and the arc halts.** Never tuned past, never
re-run with a changed parameter.

---

## Blind bands, before anything is measured

`docs/experiments/E35-armslate-blind-bands.md`, **pushed before the first arm's output is
measured**, in the executor's own ritual from [E35-predictions.md](E35-predictions.md) and
[E35-R2c-blind-bands.md](E35-R2c-blind-bands.md):

1. **What one counted thing IS**, before any number. A SPECK is not a dark pixel; the twin
   census and the flat census are different objects at different magnitudes; pale area at
   view 1 is not the eight-view mean.
2. **Blindness limit declared** — what you already know (this baseline table, R2-c's
   direction, the seed grading) and what you do not.
3. A band per arm per class, plus the **(d) selection outcome** predicted under the rule:
   which arms you expect to survive branch 1, and which branch (3 / 4 / 5) you expect to land
   in. That is a real prediction and it can miss.
4. **Predict each clause of a conjunction separately, then the join.** The join tracks the
   rarest clause, not the salient one — *improves* ∧ *register holds* ∧ *combinable* has
   three.

---

## The sheet — built BEFORE the metrics

The cheapest diagnostic in this repo is *reference | asset | provenance | error* on one
sheet, and E07 ran four arms and two gates without once building it. So:

- **Full size, 352×1024, no contact-sheet scale.** Recorded twin | (a) | (b) | (c) | (d), in
  that order, one row.
- **Head at the Director's zoom (3×)**, second row — the scale at which the pale class and
  the specks were found, and the scale his eye ruled R2-b at.
- **The depth hint as its own panel**, beside the canny control it replaced. He should see
  what arm (c) actually fed the model.
- **A walk in prose naming EVERY visible class, including out-of-scope ones.** The speck
  class was visible on the sheets E34 was accepted on, went unnamed by report and ruling
  both, and reopened an accepted asset the next day at his zoom. Name what you see even if
  no metric here measures it.

Then the metrics table, then the bands scored honestly — hits, misses and mixed, with the
mixed ones explained rather than rounded up to a hit.

---

## Out of scope

- **The cn ladder** — STRUCK as counter-indicated (R2-c). Not a fallback, not a tiebreak.
- **The 4-seed screen** — RULED DOWN (consult #4 Q3): frontier-sliding only.
- **Negative-prompt conditioning** — real but modest at cfg 2.5; not in this slate.
- **VAE precision / bf16** — deprioritised; 57 components at up to 377 texels is structural
  painting, not decode ringing.
- **The Qwen-Image-Edit 2509 route** — a route change at the Director's word; spec on file.
- **The eight-view rebuild** — 8 jobs, fires only at his pick, lands the arithmetic at 45.
- **The corrector** — bounded at 36 px² by construction; the surviving dark class is
  dominated by components 10× that cap. It cannot reach this class and is not asked to.
- **Any second view, any second seed, any re-roll.** See the budget.

## Budget and compensators

**33 of 45 spent. This slate is 3 or 4 → 36 or 37. The rebuild is 8 → 45 exactly.**

There is **no slack in the ceiling**. Therefore:

- **No re-rolls.** A twin that comes back wrong is reported as a twin that came back wrong.
  A re-roll spends the rebuild's budget and needs the Director's word.
- A submission that errors and returns no image is reported with its error and the arc
  halts; it is not silently retried.

| irreversible action | compensator | post-rollback state | owner |
|---|---|---|---|
| cloud job submitted | **none exists** — credits spend on submit | bounded before spend: ≤ 4 jobs, ≈ $0.072 at the measured $0.018/job | the executor seat |
| `--depth` added to `silhouette_masks.py` | `git revert` the commit | tool at its pre-slate behaviour; G4's anchor proves the mask leg never moved | the executor seat |
| pale instrument parameterised | `git revert` | G5's anchor proves the numbers are unchanged either way | the executor seat |
| depth PNGs written under `facet_E35\depth\` | delete the directory | no input modified; the raycaster is read-only on the mesh | the executor seat |
| docs pushed | `git revert` | docs paths fire no CI | the executor seat |

**Tests ride the commit.** `silhouette_masks.py` is repo tool code, so the `--depth` addition
carries its tests in the same commit, at **T68+** (T67 is the highest taken). At minimum: the
support-identity leg (G3) and a leg that **fails if the normalisation is removed** — a check
that cannot fail is not a check.

---

## Standards compliance

| standard | score | evidence |
|---|---|---|
| **PIN_PER_STEP** | **3** | every arm emitted by `make_payload.py` from one recorded base with an explicit override dict, base sha256 and payload sha256 in a sidecar; the depth hint comes from a repo-committed instrument whose camera derives from `--views/--step`, never a literal vector; (d)'s composition is fixed by a rule written before its inputs exist |
| **ANDON_AUTHORITY** | **3** | six gates, all `raise` (never `assert` — `python -O` deletes those); G3, G4 and G5 are constructed so they *can* fire, and G5 fires on this seat's own instrument edit; halting is specified with no skip flag |
| **NAMED_COMPENSATORS** | **2** | table above, owner per row. Not 3: the load-bearing irreversible action — a submitted cloud job — has **no** compensator and cannot have one, so it is bounded before spend instead. Declared rather than scored around |
| **DECOMPOSE_BY_SECRETS** | **3** | what varies per arm is isolated in one override dict; hint builder, census, pale measure and register measure are four instruments with JSON interfaces; the prompt is a versioned file, not a string inside a payload |
| **UNCERTAINTY_GATED_HUMANS** | **3** | exactly one human checkpoint, at the highest-uncertainty point — the artifact itself, full size, at his zoom. Arm (b) is flagged contrastively at the top ("you ruled `soft studio light` into R3; this arm replaces it") so he can veto one arm without the slate |
| **EXTERNAL_VERIFIER** | **2** | no arm grades itself: the censuses, the pale measure and C\* are instruments the arms cannot influence, and the acceptance judgement is the Director's, not any model's. Not 3: the executor seat both runs the arms and runs the instruments — the separation here is instrument-vs-generator, not model-family-vs-model-family |

**Remediation for the two 2s.** The compensator gap is structural to paid generation and is
bounded instead; no remediation is possible and pretending otherwise would be worse. The
verifier gap is real, and the honest fix is the one this arc already enforces — **the ruling
seat is not the executing seat**: the executor reports, the advisor rules, the Director
accepts. Owner: the advisor seat, standing.

---

## Halt

**At the sheet.** Report at `docs/experiments/E35-armslate-report.md`; the arc stops there
for the Director's eye. Nothing after — no rebuild, no route change, no second view — fires
without his word.

Executor rules bind: never judge whether the output is good; state predictions before looking
and disclose blindness; stop at every gate and never improvise past one; do not write to the
memory store; **a negative result is a full success** — if all three levers fail, say so
plainly and stop.
