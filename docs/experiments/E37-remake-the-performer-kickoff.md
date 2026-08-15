# E37 — remake the performer: generation, not repair

**Seat:** advisor · **Dispatched:** 2026-08-15, at the Director's directive relayed
from the armature seat: *remake the performer from source; no more repair arcs.* ·
**Supersedes:** E36's texture arms ([E36-ruling.md](E36-ruling.md) Ruling 1) ·
**Tests:** T71+ · **This dispatch's own commit bumps `laws.paid_for_by` to
`E3[0-7]`** — the thrice-proven rule.

## The directive, recorded

Two days of repair established that both remaining defect classes on the performer
are baked in at generation time: the dark specks are generator-painted into the
texture (E35 measured them to their floor — no lever removes them while keeping the
man), and the pure-black dots are mesh-pit shading, in no texel of atlas or GLB,
unreachable by any texture work. The fix is generation, not repair: **a new mesh and
a new texture, made clean rather than cleaned — select clean; never paint first and
repair after.**

## The question

Can the route produce a clean performer from the recorded source — a mesh without
pit shading, a texture without specks or pale patches, **the same man at the
Director's eye** — by candidate selection at each generation stage?

## The consumer's acceptance frame (armature's five requirements, verbatim in force)

1. The same character at the Director's eye — identity is canon and his call; a
   remake that loses the man fails regardless of cleanliness.
2. Texture with no pale unpainted patches (keep what E34 fixed) and no painted
   specks — **checked at candidate selection with the census instrument, before
   painting or acceptance.**
3. Mesh with no pit shading — mesh candidates checked under flat light before
   texturing (a dark mark that persists under flat light is texture; one that
   vanishes is geometry; on an untextured solid render, a lit-only dark mark is
   geometry). *(⚠ Scoped 2026-08-15, E37 Rulings 1–2: the screen this clause
   commissioned measures shading RELIEF — in round 1, substantially the source
   plate's own swirl relief — and is not demonstrated to see the rejected
   pure-black dot class, whose mechanism task 0a left UNMEASURED and which
   remains open with the UV-gap candidate live. The screen ranks candidates; it
   is not a verdict on that class.)*
4. **RGBA-true turnarounds — real alpha, not flat-255** (the S03 lesson; E36 task 0
   measured this route's turn renders at alpha 255 across the whole frame, so this
   is new deliverable work, not a checkbox: alpha composited from the raycast
   silhouette masks — exact by construction — or a transparent-film render proven
   equal to them).
5. Delivered as the previous acceptances were: GLB + sha256 + the acceptance ruling
   + accepted-with observations, tree manifest-protected read-only, the relay
   carrying path and hash.

## Premises — measured or assumed (mark the outcome in the report)

| # | premise | status |
|---|---|---|
| 1 | The source plate exists and is pinned: `E:\AI\armature\outputs\E07\concepts\00-directors-pick-clay-armature.png`, sha256 `7533832557 18db7212b21007a24fce0d9a6a101cb352662459eec690d335e0dc` (spaces ours), 1,216,363 bytes — hashed at dispatch. armature's tree is read-only to facet | **MEASURED** |
| 2 | TRELLIS is deterministic: one input at one seed is bit-identical through `pipe.run`, hole-filling and remeshing; divergence only inside `to_glb` decimation (faces ±0.27%) — so candidates come from **seed and concept variation, never re-rolls** | **MEASURED** (E29 Ruling 5) |
| 3 | The twin route's seed frontier has measured selection room: mean dark area 170.4 px² at seed 770700 against 71.9 at 987654, same recipe (E35 §2a / the close analysis) | **MEASURED** |
| 4 | The census, chroma-split and register instruments reproduce their published rows to the digit | **ASSUMED — task 0 anchors it, the E36 0f form; a failed anchor halts the arc** |
| 5 | The recorded twin recipe (qwen-image img2img + canny 0.9 · denoise 0.92 · steps 20 · cfg 2.5 · shift 3.1 · euler/simple · 352×1024-class frame · no LoRA) is the class-best measured configuration and the only served route where identity is a first-class input | **MEASURED** (E35 close; consult #5) |
| 6 | Protected trees verify 0/0/0 at open and close, receipts OUTSIDE every protected tree | **re-verify both ends** (the E36 lesson) |
| 7 | Stage-0 local clay-ify is available for concept variants: Qwen-Image-Edit-2511, Apache-2.0, weights on disk (`qwen_image_edit_2511_fp8mixed.safetensors` + encoder + VAE) | **MEASURED** (concept-prep.md; re-`Test-Path` at use) |
| 8 | The generation frame must be generator-legal: derived from the picked mesh, ÷8 floor, ÷16 preferred (E04 Ruling 15) | **MEASURED law** |

## The arc, stage by stage

**Task 0 — mechanics, zero cloud.** E15 ritual (scratch db, all legs or stop) ·
watchdog ADVANCING on two reads · manifest gates (premise 6) · instrument anchors
(premise 4) · re-hash the source plate against premise 1. Artifact home
`E:\AI\training\facet_E37\`; every receipt outside every protected tree.

**Stage A — mesh candidates. Local, zero cloud.** Round 1: **six TRELLIS seeds on
the source plate as-is** (concept variants held for round 2 — one variable per
round). Per candidate: reconstruct (`ATTN_BACKEND=sdpa`, the E33 band) → weld →
per-candidate solid renders, **lit AND `--flat`, eight views at the recorded
convention** → the pit screen: dark-mark census on the solid renders — a mark
present lit and absent flat is geometry; report **count AND largest connected
component per candidate** (the E28 Ruling 21 form), plus `mesh_stats` /
`mesh_topology`. **No numeric pass bar is invented** — candidates are ranked by the
screen and the sheet decides: **HALT at the Stage-A sheet** (per-candidate
turnarounds at full size, source plate beside them) for the Director's pick.
Identity is his; the screen's numbers ride the sheet. If no candidate reads clean,
round 2 (fresh seeds, or stage-0 concept variants) fires **only at his word**.

**Stage B — twin candidates on the picked mesh. Cloud.** Frame derived from the
picked mesh (premise 8). The recorded recipe, **prompt = the recorded R3** — ⚠ the
r3L flat-lighting term is surfaced to the Director at this stage's dispatch and
runs **only on his ratification** (it edits his ruled register term; its evidence —
pale 226/4.09 against 278/4.97, dark flat, the man kept — stands in the record).
**K = 3 full eight-view sets** at three seeds: the recorded 770700, the
measured-best 987654 (premise 3), one fresh. **The selection rule is pre-registered
in the bands file BEFORE the first job**: census every twin (dark count · area ·
largest component · chroma-split signature · register C\* · reg-IoU); select **one
GLOBAL seed** — lowest total dark census subject to the register floor and
reg-IoU ≥ 0.80 (the E34 floor; a firing HALTS with numerator and denominator) —
**per-view seed mixing is out** (it produced the rejected pale wash) and returns
only at his word. **HALT at the Stage-B sheet** (the winning set beside the source
plate, head band at 3×): identity and register are his, before any projection.

**Stage C — projection, fill, candidate. Local, zero cloud.** The E34-proven
eight-view form on the winning set: project → surface-aware fill → pack →
`performer_v3.glb` candidate. Final atlas + render census (both classes),
provenance mix, RGBA-true turnarounds (requirement 4 — alpha from the raycast
silhouette masks, pinned equal to the geometry by test), full-size sheets:
reference | candidate | provenance, head at 3×.

**Stage D — acceptance and delivery.** His eye at his zoom. On acceptance:
`facet_E37` manifested (self-excluded, receipt outside), read-only; the delivery
per requirement 5; the relay to armature carries path + sha256 (their zero-credit
acceptance survey fires on it). On rejection: the candidate and its census stay in
the record; the next round is his word.

**Mechanical vs content** — as E36 defined: validation failures, degenerate frames
and corruption signatures are MECHANICAL, one repeat per stage; census numbers,
register, and identity are CONTENT, never repeated.

---

> ## ⚖ AMENDMENT 1 — round 2 and the wood register (advisor, 2026-08-15, at the Director's word: "round 2, wood")
>
> The source plate carries generator fingerprint-swirls, measured at the
> Director's zoom and confirmed at the advisor's read of the plate itself; the
> founding law bakes them into every round-1 mesh as relief. Full grounds and
> ratifications: [E37-ruling.md](E37-ruling.md) Rulings 1–2. Operationally:
>
> - **Stage A gains round 2, zero cloud.** EDIT the picked plate locally with
>   Qwen-Image-Edit-2511 (premise 7): smooth, clean, mark-free clay — same man,
>   same pose, same framing, plain seamless background kept (no alpha, so `rembg`
>   runs). Up to three edit attempts, hashed and sidecarred, all shown beside the
>   original. **HALT at the Director's identity eye on the plate before any
>   reconstruction.** Then the SAME six pre-registered seeds on the approved
>   plate — the set unchanged so round 1 is the measured baseline — same screens,
>   Stage-A sheet v2, his pick.
> - **Requirement 3's screen is scoped** per the annotation above: it ranks
>   candidates by relief; the pure-black class's mechanism is open.
> - **Stage B's register is WOOD, not terracotta** — the E33 note became the
>   change order at his word. The wood prompt is authored at Stage B's dispatch
>   and his eye gates the register at the Stage-B sheet, the Gate-R form. The r3L
>   question is MOOT as posed (its lighting evidence stays recorded). Grain is
>   paint, never geometry.
> - **The boundary:** round 2 fixes relief. The painted-speck defence remains
>   Stage B's census selection, unchanged.

---

> ## ⚖ AMENDMENT 2 — Stage B in wood: the prompt, the probe, and the suspended floor (advisor, 2026-08-15, at the Stage-A close)
>
> Stage A closed at the Director's pick (Ruling 3: seed 987654 on the clean
> plate, `884abe04…`). Stage B runs as dispatched with these deltas:
>
> **The wood prompt, v-w1, authored here verbatim** (three named deltas from the
> recorded R3, everything else byte-preserved):
>
> ```
> a slender jointed wooden artist's mannequin, a smooth bald head, a simple
> readable face with drawn brows, closed lidded eyes, a small closed smile,
> small ears, ball-and-socket shoulders and elbows, ball-and-socket wrists and
> ankles, ball-and-socket hips and knees, fine straight wood grain across the
> torso and limbs, empty open hands, simple rounded feet, plain pale grey
> background, warm natural hardwood, matte oiled wood, soft studio light
> ```
>
> The deltas, each named: (1) the object noun — *clay mannequin* → *wooden
> artist's mannequin*; (2) the surface term — *sculpted thumbprint hatching on
> the torso and limbs* → *fine straight wood grain across the torso and limbs*,
> same grammatical slot, and the hatching term is DROPPED on Ruling 3's finding
> that it was the named source of the literal-rendered dark component; (3) the
> material close — *unglazed terracotta, matte sculpted clay* → *warm natural
> hardwood, matte oiled wood* (matte kept deliberately — every glossy register
> has failed his eye). *soft studio light* and every identity term are
> byte-preserved. The executor materializes the per-view JSON under the recorded
> prompt discipline (versioned, sidecarred, byte-pinned).
>
> **Gate-R probe first: 2 jobs.** Views 0 and 4, seed 770700, the picked mesh's
> controls, v-w1 — a register sheet beside the source plate at full size, head
> at 3×. **HALT at the Director's eye.** His register word gates the seed sets;
> a register iteration (prompt v-w2) is his call, priced at 2 jobs per round.
>
> **The register floor is SUSPENDED, not ported.** The terracotta C\* floor was
> route-measured for terracotta; no calibrated wood floor exists. C\* rides
> every report and sheet as a diagnostic; nothing gates on it
> (suspend-don't-invent). reg-IoU ≥ 0.80 stands unchanged — it is geometric and
> register-independent.
>
> **Bands:** sealed by commit before the first seed set (after Gate-R passes).
> The E35 terracotta floors are cited as reference context only — wood census
> expectations are UNMEASURED and the bands say so; three branches, UP live.
>
> **Budget inside the standing 40:** probe 2 (+2 per his-word register
> iteration) + seed sets 24 + mechanical/re-roll contingency = 40. Spend
> currently 0.

---

> ## ⚖ AMENDMENT 3 — the repair road after Stage D's rejection (advisor, 2026-08-15, at the Director's go)
>
> Stage D rejected the composed candidate (Ruling 18). The road, four phases,
> every element measured this arc or schema-verified live (consult #7 fold):
>
> **Phase 1 — one wood by construction.** TWO complete single-seed eight-view
> sets (a third only if neither censuses clean), fresh seeds pre-registered
> before submission. Uniform configuration on every view: v-w1 + the backdrop
> negative clause, `cn_strength` 1.0, the tuned controls, 368×1024, the
> recorded recipe otherwise. ⚠ The two levers were measured one-at-a-time;
> their combination is n=0 and the bands say so. Per set: both keys on all
> eight views, census total + largest component, per-view register C\* with
> the WITHIN-SET spread reported — the single-seed consistency claim is
> verified, not assumed. **Selection rule sealed before generation**: every
> view clears both keys → lowest total dark census → ties by within-set C\*
> spread. One mechanical repeat per set; content defects are NOT re-rolled —
> they go to Phase 2 by design. 16–24 jobs; spend from 35 of 80.
>
> **Phase 2 — repair in place, never re-roll.** The winning set's content
> defects and its fleck census: masked repaint at the same seed and
> conditioning (`noise_mask` path, schema-verified), feathered masks, a
> ColorMatchV2 pass over each repaint with the surrounding view as reference.
> The repair list goes to the Director's eye with the Phase-1 sheet.
>
> **Phase 3 — deterministic harmonization.** `ColorMatchV2` (live-verified;
> the deprecated original is not used), `image_ref` = the one view the
> Director approves, the other seven matched. No sampler, no seed,
> byte-reproducible; method choice reported with its numbers, not tuned
> against his eye.
>
> **Phase 4 — the proven chain.** Projection, fill, RGBA turnarounds,
> censuses, sheets — and the sheets are WALKED AT FULL SIZE at the advisor's
> seat before the Stage-D halt, every time, per Ruling 18.
>
> Out of scope: the reference-anchor model patch (later, single-variable) ·
> per-view seed mixing (dead, permanently) · any edit to protected trees.

## Blind bands

Sealed by commit before Stage B's first job: the Stage-B census expectations
against the E35 floors (seed floor: count 7–26 · area 34–139 px²; every band states
its position against it), the Stage-C provenance expectation against E34's
98.4%/95.1% styled/reachable, three branches per hypothesis, the UP branch live.
Stage A needs no bands — it spends nothing and its verdict is his eye — but its
pit-screen readings are recorded per candidate before the sheet ships.

## Budget

**Ceiling 40 cloud jobs ≈ $0.74** at the measured ≤ $0.0184/job: Stage B 24 ·
mechanical contingency 8 · one his-word re-roll round 8. Stage A and C are local
and free. Zero partner-API nodes. The ceiling is the Director's number to confirm
or move.

## Compensators — no skip

| irreversible action | compensator | owner |
|---|---|---|
| ≤ 40 cloud jobs | none exists — bounded before spend, per-stage halts, pre-registered selection | executor |
| writes under `facet_E37\` | remove the tree; re-derivable from recorded scripts + this spec | executor |
| repo commits / push | revert by commit, pathspec-scoped | executor / advisor |
| protected trees (E33/E34/E35 + eight subtrees; armature's tree) | prevention: read-only; `tree_manifest` gates at open and close; receipts outside | executor |
| the armature relay at delivery | the relay is an append-only amendment in armature's record; a wrong one is corrected in place, never deleted | advisor |

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | recorded recipe pinned; candidates are seed-enumerated; payload sidecars per job; limit: server-side weights, as always |
| ANDON_AUTHORITY | 3 | reg-IoU floor halts; register floor binds; manifest gates both ends; anchors halt the arc; every halt is a hard stop |
| NAMED_COMPENSATORS | 3 | table above; the compensator-less spend bounded before the first job |
| DECOMPOSE_BY_SECRETS | 2 | stages decomposed by generation layer (mesh / paint / assembly); selection rules per stage, sealed before spend |
| UNCERTAINTY_GATED_HUMANS | 3 | three Director halts (Stage-A pick, Stage-B set, Stage-D acceptance); identity his by law at each |
| EXTERNAL_VERIFIER | 2 | instrument anchors reproduce published rows before any new number; armature's independent zero-credit survey runs on the delivered candidate; his eye is the identity verifier by design |

## Out of scope

Repair of any recorded asset · edits to protected trees or accepted assets ·
Qwen-Image-Edit-2509 in any form (closed class-worse, E35) · partner texture nodes
(identity-blind by schema) · the corrector contract (closed with E36; its
validate-against-rejected-artifacts constraint recorded there) · the brush
(register collision unresolved; not needed by this arc's design) · per-view seed
mixing (his word only) · the `_depth_far` variant and all dual-control work.

## Count surfaces and namespace

Tests take **T71+**. This kickoff's commit adds the 37th experiment row, so **every
experiment-count surface moves in this same commit** (the T34 fourth-leg law). The
corrected order binds any test-adding commit: land pin edits → FULL suite → collect
→ surfaces → census last. Manifest gates at open and close. E15 ritual at open:
scratch db, all legs, or stop.
