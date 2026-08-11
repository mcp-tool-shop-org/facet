# E32 ruling — the armature mark through the route

**Seat:** advisor · **Ruled:** 2026-08-10 · **Spec:**
[E32-armature-mark-through-the-route.md](E32-armature-mark-through-the-route.md) ·
**Predictions:** [E32-gate0-predictions.md](E32-gate0-predictions.md) ·
**Report:** [E32-report.md](E32-report.md)

This seat did not run the experiment and does not judge the artifact. The Director's eye rules
on the sheet; this document rules on what the measurements mean and what the repo does next.

## 0. What this seat verified before ruling

The advisor resolves every external citation at ruling time. Resolved independently, against the
tree rather than against the report:

| claim | verdict |
|---|---|
| Gate L passed with the flag armed | **CONFIRMED.** `recon.log:1` `licence_guard: nvdiffrast/nvdiffrec blocked (non-commercial licence)`; `recon.log:406` `LICENCE OK: clean bake path`. Run line records `ptype=1024_cascade remesh=True decim=1000000`; `seed 42` is `run()`'s own default, no flag |
| `--min-iou` fired at 0.5878, exit 1, no texture | **CONFIRMED** verbatim in `project.log` |
| `ss_res` for `1024_cascade` is 32, at `trellis2_image_to_3d.py:541` | **CONFIRMED**, line and content exact. ⚠ **And it is stronger than the report claims:** two trellis2 copies exist on this rig — `TRELLIS.2-repo` and the ComfyUI vendored one, which hardcodes `ss_res = 32` at its line 3721 with the dict commented out at 1438. The value is 32 in **both**, so the mechanism claim does not depend on resolving which copy loads |
| BiRefNet resizes to 1024×1024 at `BiRefNet.py:16` | **CONFIRMED**, exact |
| `project_twins.py:220` parses argv at module level; `fit_background` at `:349` | **CONFIRMED**, both exact — the import-impossibility is real |
| Five hand-copies of the route's background model | **CONFIRMED**, and the report undersells it — see §0a |
| "First subject on this route where the nested-wall leg computes" | **CONFIRMED** for the written record — see Ruling 3 |

Not re-run by this seat: the suite counts and the HEAD baseline. Those are measurements the
report owns, and Ruling 7 puts them under a mechanical check rather than under my transcription.

### 0a. The five copies — and this ruling's own error, recorded

I first reported the five-copies claim as **unverified**: `grep "def fit_background" tools/`
returns **two**. That grep was wrong, not the report. The five copies exist under **four
different names**:

`fit_background` (`project_twins:349`) · `ring_fit` (`e12_twin_readout:106`, whose docstring
says *"project_twins' figure_mask, same construction"*) · `fit_bg` (`e14_twin_registration:48`)
· `fitted_bg_field` (`gained_bg_check:94`) · and one inline quadratic-over-border-ring
(`e08_registration:86`).

**A name-based search is not an enumeration.** That is the same law as Ruling 11, missed by the
seat citing it. Corrected before any decision rested on it — and the renaming is itself the
finding: it is why five copies of one model have stayed invisible in a repo that greps itself
constantly.

---

## Ruling 1 — The question is ANSWERED, and the answer is yes

The spec asked one question: **does TRELLIS.2 reconstruct a lattice of thin tubes?** It does.
17 of 21 openings preserved (81.0%) at a matched relative threshold, thickening of 1.174×, and
P1a's predicted bridging did not happen — the X-brace, pelvic loops, head cage and foot rings
come back open.

**Bounded, and the bounds are part of the ruling:** one subject, one class, one run, at
`1024_cascade`. E29 Ruling 5's mesh noise floor (±2,618 faces, ±1 shell, ±18 non-manifold edges)
was measured on a different subject class and was **not** re-measured here. The opening and width
figures sit far outside that floor; the shell count does not get the same protection (Ruling 4c).

## Ruling 2 — ⚑ THE FINDING: occupancy-grid resolution does not bound reconstructed topology

The executor predicted from `ss_res = 32` that a 0.65-voxel tube separated by 1.2-voxel gaps
could not survive — 0–6 openings, 1.3×–3.0× thickening. Measured: **17 openings, 1.174×**.

**This is the result, and it is a full success.** The falsifier was registered in advance, in
writing, with its own mechanism named — *"the arithmetic treats a generative sampler as a
rasterizer… if P1b comes back at or near 22, the lesson is that voxel arithmetic does not bound
a learned occupancy prior, and that is a more useful result than a hit."* It came back at 17. A
prediction that names the mechanism it might be wrong about, and is then wrong about exactly
that, is worth more than three hits.

The mechanism, as far as this evidence carries: the sparse-structure sampler is **learned**, and
the cascade decodes a continuous field *inside* occupied voxels. Voxel arithmetic is therefore a
**lower** bound on achievable detail, not an upper one.

**Adopted as a bounded finding, NOT promoted to a standing law.** One subject in a fourth class
does not carry to doctrine. This repo has just finished paying for a claim quantified wider than
its evidence base (E14 Ruling 3, narrowed by E29 Ruling 4) and this ruling will not open a second
one. It enters the record as measured, with its class named.

**What it changes now:** no future spec on this route may predict topology loss from `ss_res`
arithmetic alone without citing this measurement against it.

## Ruling 3 — P2b: the leg COMPUTED, and it reads NOT-hollow. E29's split conjunction is vindicated

E29's P5 split *"does the hollow test fire"* into two clauses, because `e14_topology.py:154`
computes `nested_wall_test` only when a second manifold piece exceeds 1% of faces:

* **Clause A — does it compute at all?** E32: **YES.** Second piece 25,450 faces = 2.67%.
  Searched the written record for a prior instance: none. E32 is the first.
* **Clause B — does it read as a nested wall?** E29 defined that reading as `inner_volume`
  negative **with `material_frac_of_outer` small** — thin walls around a cavity. E32: inner
  volume **is** negative (−0.000113198), and `material_frac_of_outer` is **0.9518** — the
  opposite of small. Boundary edges 0, so the surface is closed.

**E32 is therefore the first measurement on this route that separates the two clauses**, and it
separates them in the direction that matters: **a negative `inner_volume` alone is not the hollow
signature.** The conjunction is the signature. A nearly-solid body with a 4.8% internal void
produces the same sign on the volume term as a hollow double-walled shell does.

That is a real gain in what the instrument means, and it was only available because E29 wrote the
clauses apart instead of predicting the join. E29 Ruling 4 withdrew E14 Ruling 3's universal
quantifier and replaced it with its evidence base; **E32 supplies the first measured counterexample
outside that base.** It does not overturn E14 on the class E14 measured, and the character class
remains **UNMEASURED** on this axis — nothing here touches it.

## Ruling 4 — The `--min-iou` halt was CORRECT. The threshold does not move, and no replacement metric is commissioned

**4a. The halt is upheld without qualification.** A gate fired inside the tool performing the
irreversible step, it exited 1, no texture was written, the threshold was not lowered and the
flag was not disabled. That is the law working exactly as written, and it is the second time an
executor here has run an advisor-side gate as written and reported the evidence rather than
tuning past it.

**The diagnosis is this repo's own law landing somewhere new.** *Normalise a boundary quantity by
perimeter, not by area.* Silhouette IoU is an **area-normalised agreement score**. On a subject
whose mask is 10.8% of its own bbox, a systematic 3–4 px offset removes a large fraction of the
intersection on every member at once and adds it to the union. The overlay's evidence — every
member green-cored and in place, red and blue as thin opposed fringes along the tubes — is
consistent with a uniform offset, not with a registration collapse.

**4b. I am not choosing a new threshold or a new metric here, and the refusal is the ruling.**
Retuning a condition while looking at the result it would judge is the one move that is always
wrong, and *"0.80 is too strict for lattices"* derived from the single lattice that failed it is
exactly that move. Compounding it: silhouette IoU is a metric this repo has already been burned
by **twice** — it returned **1.00000 on a mesh with a hole clean through it**, and it was once
pre-registered to grade *character identity*, which was wrong for a different reason. A metric
with that record does not get a new threshold on one subject's say-so.

**What happens instead:** numerator and denominator are reported separately, the overlay goes in
front of the Director, and **if** projection is wanted on lattice subjects it gets its own spec
that measures the offset **directly** — *is the registration off by a fixed number of pixels, and
by how many* — rather than reading an offset through an area ratio. **Step 3 of the route does not
complete on this subject class, and that is the honest state**, not a gap to be threshold-engineered
shut.

**4c. The shell count is reported, not adopted.** 212 against a predicted 5–60, with
`pieces_manifold_adjacency` at 1,151 — the two definitions disagree by 5.4×, which is
`e14_topology`'s own pinched-surface warning. A single-run mesh comparison whose noise floor was
not measured on this class does not support a conclusion about shell count. It stands as a
reported number with its floor named **unmeasured**.

## Ruling 5 — P4d is AMBIGUOUS, as the executor scored it

The executor wrote "thinnest surviving member" without saying minimum or percentile, then
declined to take the reading that would have made it a hit (min 4.0, in band) over the ones that
would not (p01 6.0, p05 8.0, both out). **That self-scoring stands and is the correct call.** It
is this repo's unit/operand family — tenth consecutive arc — appearing this time inside an
executor's own prediction rather than in a dispatch. Recorded ambiguous; not counted a hit.

Final tally: **three hits, one ambiguous, four misses.** The misses are the result.

## Ruling 6 — Premise 5 is CORRECTED IN PLACE, not deleted

*"`pipe.run` runs `rembg`"* is retired as a description of this route. The measured mechanism:

* the segmenter is **BiRefNet at 1024×1024**, not PyPI `rembg`/u2net-at-320;
* the route hands it a 1024 LANCZOS downscale, so it runs **1:1** at its input;
* the output is **premultiplied** — partial alpha darkens toward black, so thin members lose
  luminance as well as coverage, and the reconstructor cannot distinguish *thin and faint* from
  *dark*;
* the square crop can **clip**: `[264,206,760,702]` against an alpha bbox `[266,206,758,703]` put
  1 px of the feet outside the conditioning image.

The premise **held in outcome** — no pre-keying was needed and the corner-median-keying law was
satisfied by construction — and was **wrong in mechanism**, which is what the next prediction
would have been built from. This is the eighth-member law firing on an inherited *phrase*: E29
Ruling 4's own wording carried "runs rembg" forward, and it took reading the source to find three
separate load-bearing facts hiding behind it.

## Ruling 7 — The count surfaces are reconciled by this seat, and NEVER by transcription

The executor named them, measured them, and edited nothing. **That is exactly right** and it is
what CLAUDE.md asks for.

**And the procedure carries a warning I nearly walked into.** `docs/advisor-kickoff.md` step 1:
*"⚠ RESERVE COUNT SURFACES BY NAMING T34's PINS TABLE, NEVER BY TRANSCRIBING IT. It holds SIXTEEN
pins across SIX files, plus a separate leg over the SEVEN translated READMEs. Two seats in a row
hand-listed it and each missed a different file."* The report's §9 table names six surfaces in
prose; **that list is a summary, not the authority.**

**Ruled:**

1. The reconciliation is driven off `tests/test_t34*.py`'s own `PINS` table, read at apply time,
   and off `pytest --collect-only` at the **combined** tree. No seat hand-lists the surfaces.
2. The census is regenerated by its own tool, never hand-edited —
   `python tools/instrument_census.py --committed`, diff read in `docs/instrument-census.json`,
   and the T41 pin moved **deliberately in the same commit**. That is the instruction the test's
   own failure message gives, and it is the procedure of record.
3. The pins move to whatever the combined tree measures. **I am deliberately not writing the
   integers into this ruling** — a number transcribed here becomes a fourth surface that can
   drift, and the entire point of these pins is that the tree is the authority.
4. Digit updates on the seven translated READMEs are **mechanical** — the count is the same digits
   in every language. This does **not** trigger a translation pass; step 5 of the release ritual
   is a release step and this is not a release.

## Ruling 8 — The already-red gate at HEAD is the arc's own self-reference, and it is mine to clear

`test_t41_axis_d_is_idempotent_across_runs` was red at `6e85cf9` **before the executor touched
anything**: the census's committed axis-D count for `turn_render.py` is 18, a fresh read gives 19,
and the 19th citing document is **the E32 spec commit itself**. The executor verified this in a
detached worktree at HEAD and left it alone, which was correct — regenerating a census is a
count-surface edit.

This is the E28 self-reference family, an arc's own paper contaminating the census the arc is
measured by, and it is now the **second recorded instance**. It clears with the regeneration in
Ruling 7. The report and this ruling will move the same counts again when they land, which is
precisely why all of it lands in **one** commit.

## Ruling 9 — Both instrument defects are ADOPTED with their tests

1. **`bbox_blowout` was a conjunction** requiring *both* dimensions ≥98%, so it stayed silent at
   its worst possible reading — 2048/2048 wide — and reported a contaminated key clean. E08's own
   case blows out in **one** dimension. *A check that cannot fail is not a check*, found by the
   plate within an hour of the instrument being written.
2. **`abs()` in the residual was not free.** A two-sided key cannot express *the subject is
   lighter than the ground*, so a dark region reads as subject. `--polarity` added; default stays
   `both`, so every number already produced reproduces.

The honest boundary was **asserted rather than described**: `--polarity lighter` does not rescue a
hard-edged ground (11,428 px against a true 800 in the fixture). The load-bearing path uses the
route's own segmenter via `--mask`, so no key sits on it at all. **Adopted.**

`mask_geometry.fit_background` is additive-only, with T64 extracting `project_twins`' body via
`ast`, asserting bit-identity, and carrying a companion leg proving that comparison *can* fail —
which is the fixture-side law satisfied properly. **The five copies are reported, not fixed:**
consolidating them is its own change with its own blast radius and does not ride an experiment's
commit.

## Ruling 10 — Three defects OUTSIDE this repo, routed to the Director

Not folded here, because they are not facet's to fix, and the advisor does not write to the
memory store:

* **The `character-turnaround` skill's step-3 path is wrong.** `project_texture.py` is in
  `3d-prerender/`, not `saltroad_bake_fix/tools/`; both directories were enumerated.
  ⚠ **Independently corroborated:** the studio constitution names
  `sprite-foundry/3d-prerender/` as the productized stage-3 home (corrected 2026-07-28). The
  skill is pointing at a path the map already moved.
* **The skill's required reading, `memory/character-turnaround-pipeline.md`, does not exist.**
  Searched all of `C:\Users\mikey\.claude\projects` for `*turnaround*`: zero hits. The executor
  recorded the gap and **did not pretend to have read it**, which is the right handling of a
  broken pointer in one's own dispatch.
* **`turn_render.py` exists twice and the copies differ** — `saltroad_bake_fix/tools/` (used) and
  `facet/tools/verify/`. The divergence is unmeasured; naming it is not fixing it.

## Ruling 11 — The E04 bowsprit trap fired, and the law paid out

`turn_render.py`'s 757×1024 portrait default **cropped the arms off every view** on a nearly
square subject (extent 1.0012 × 0.9699). The executor did not commission a frame tool: it found
`e12_frame.py`, already committed, which derived 1072×1024 and held the figure with margin.

*Enumerate the resource before commissioning one* — the law that has cost this repo three
sessions — **worked on the first try here.** Recorded as the law paying out, not as a defect.

---

## What the Director is asked to look at

`E:\AI\training\facet_E32\E32_gate0_sheet.png` at **full size** — concept beside eight clay views.
Two questions no number in this ruling answers:

1. **Is this the armature mark?**
2. Does the **17.7%-of-width depth** (views 2 and 6, 156 px against the front's 878) read as a
   usable object, or as a flat relief?

Question 2 decides whether the GLB is wanted as armature's brand mark. If it reads flat, that is a
reconstruction property of a subject drawn flat-on — a fact about the input, not a defect to be
tuned out of the reconstructor.

## Not adopted into doctrine by this ruling

Stated explicitly, because the Director's standing instruction is that this is a marathon and
provisional findings are not carved into doctrine:

* **Ruling 2** is one subject in a fourth class, single run, floor unmeasured on this class.
* **Ruling 3** is one measurement, and says nothing about the character class.
* **Ruling 4's** diagnosis is an **existing** law landing in a new place; it needs no new text in
  CLAUDE.md and gets none.
* **Nothing in E32 is promoted to CLAUDE.md by this ruling.** The repo has just finished paying
  for a claim quantified wider than its evidence base; this arc will not open a second one.

## This ruling's own error record

One, recorded in §0a: I reported the five-copies claim unverified on the strength of a name-based
grep, when the five copies carry four different names. Corrected before any decision rested on it.
The lesson is the one in Ruling 11, missed by the seat citing it.

---

# Addendum — ruled 2026-08-10, after the count-surface reconciliation

## Ruling 12 — REBUILD the index. The precedent is not split, and I checked it.

**The executor's reading is corrected, and the correction reverses the decision it was pointing
toward.** The report to this seat said *"`1e30db3` and `407484f` rebuilt `facet.db`; `271f741`
(E31) did not."* Measured with `git show --name-only` on all four candidates:

| commit | `docs/index/facet.db` | `docs/index/facet.db.cert.json` |
|---|---|---|
| `1e30db3` release prep | **rebuilt** | **rebuilt** |
| `407484f` handoff | **rebuilt** | **rebuilt** |
| `271f741` **E31** | **rebuilt** | **rebuilt** |
| `6e85cf9` E32 spec | untouched | untouched |

**E31 did rebuild it.** The precedent is unanimous across all three substantive commits, and the
single commit that skipped it is **the E32 spec commit — which is precisely what left the index
stale at HEAD.** The counterexample was the defect, not the precedent.

Two further facts the table makes plain: **the db and its certificate always move as a pair** —
never rebuild one without the other — and the record is facet's product, so a commit that
knowingly ships a governed index which does not know about the arc's own documents ships a known
defect.

**Ruled: rebuild the index and its certificate.**

## Ruling 13 — but in a SECOND, terminal commit — and here is the law that says why

The executor earned a real law this session and stated it precisely:

> **The census must be regenerated after every document in the commit is final, not before.** A
> derived artifact whose input includes the document describing it has a fixed point, and
> writing-then-regenerating is the only order that reaches it.

That is correct, it generalises, and **the index is the same object as the census**: it indexes
`docs/`, which contains this report and this ruling. Rebuilding it inside the experiment commit
re-opens the identical fixed point a fourth time.

**The enforceable form of the law, which is stronger than remembering the order:** put the
regeneration in a **terminal commit whose own content is not an input to the thing it
regenerates.** A git commit message is not indexed and not censused, so a commit that contains
*only* the regenerated artifacts has no inputs left to move. The fixed point is not reached
carefully — it is dissolved by construction.

**So: two commits, in this order.**

1. **The experiment** — both tools, `mask_geometry.fit_background`, `test_t64`, the report, the
   predictions, this ruling, and every count surface including the census.
2. **The index + certificate**, rebuilt together, alone, immediately after.

This deviates from the precedent in Ruling 12, which bundled them — and the deviation is the
point. Those commits were releases and a handoff, not experiments carrying documents that
describe the artifacts being derived. **This arc has hit the self-reference fixed point three
times in one session** (the census stale at HEAD, the census moving mid-commit, and
`e14_topology.py` 12 → 13 when the report first named it). Separating the terminal regeneration is
the structural fix for all three.

**Gate before the rebuild — the E15 ritual, unchanged:** `facet_index.py build` then `verify`
against a **SCRATCH `--db`**, **19/19 or stop**, because the record mount is live on the working
copy. Only after that passes is the committed `docs/index/facet.db` + `.cert.json` regenerated.
**A failing leg halts and is reported; it is not tuned past.**

## Ruling 14 — the contaminated suite run was caught correctly, and it is the same family

The executor ran two other `pytest` invocations against the same index while a full suite was in
flight, saw seven index-contending tests fail (`t13_concurrent_verifies_do_not_collide`,
`t20_verify_then_build_in_one_process`, `t29_a_passing_verify_and_claims_exit_zero`), **diagnosed
it as its own doing rather than as a regression, stopped everything, and re-ran alone.** That is
exactly right, and it is worth naming as a third form of the same underlying family: **an
instrument that contends with itself.** E28's census read a corpus containing its own output; here
a suite's index-race tests raced against the session running them.

The measurement that matters: **1 failed / 916 passed on the clean run, the single failure being
the axis-D idempotency**, cause measured rather than guessed, then corrected and regenerated to a
fixed point with **T41 at 41 passed**. Nothing in the change is a regression.

**The count-surface reconciliation is ACCEPTED as executed:** 891 → **917 full / 877 hermetic /
gap 40**, driven off T34's own `PINS` table read at apply time, census 108 → 110 rows with three
axis-D counts moved, both new tools judged axis-G `none` under the census's stated rule, T62's
`RUNNABLE` seven → nine, T33's ANDON pin 28/12 → 30/14, `SHIP_GATE.md`'s lineage preserved
(`… → 859 → 891 → 917`), and the seven translated READMEs digit-only with no translation pass.
Nothing was transcribed. That is what Ruling 7 asked for.

---

## Ruling 15 — MY OWN RULING 13 CARRIED A DEFECTIVE PROCEDURE. Corrected in place.

Ruling 13's instruction read: *"`facet_index.py build` then `verify` against a SCRATCH `--db`,
19/19 or stop. Only after that passes is the committed `docs/index/facet.db` + `.cert.json`
regenerated."*

**The outcome I named was right and the procedure I prescribed cannot produce it.** Measured:

* `write_certificate` is defined at `tools/record_mcp.py:499` and called **only** at `:931`, under
  the verb `record_build`.
* `tools/facet_index.py` never writes the certificate — it holds `CERT_SUFFIX` and a docstring
  reference, nothing more.
* The committed certificate's own field reads `written_by: tools/record_mcp.py`.

So `facet_index.py build` regenerates `facet.db` **and leaves the certificate stale**. Followed
literally, Ruling 13 would have committed a fresh db beside a certificate carrying the previous
timestamp — **a half-pair, the exact thing Ruling 12 measured must never happen.**

**Corrected procedure, and the split is the point:**

1. **Gate** — `facet_index.py build` then `verify` against a **scratch `--db`**, 19/19 or stop.
   A verification, and `facet_index.py` is the right tool for it. Unchanged.
2. **Regenerate** — the committed pair is written by **`record_build`**, which runs build and
   verify as one act by design and writes **both** files. `facet_index.py` is not the tool here.

**Why the ruling survived its own defect:** the executor checked `git status` against Ruling 12's
*"they move as a pair"* observation rather than trusting two zero exit codes. The invariant caught
the procedure built on it — a small argument for stating an invariant next to the procedure it
governs.

**And it explains Ruling 12's measurement.** The pair moves together in every prior commit not by
anyone's discipline but **because only one verb writes both**. The precedent was a property of the
tool, not a habit.

## Ruling 16 — the executor's own finding, adopted as a law

Named unprompted after its precedent reading was overturned:

> **A conclusion read off a truncated listing is not a measurement.**

Three instances in one session, every one the session's own tooling silently dropping rows: a
pytest summary read through `Select-Object -Last 12` reporting **11** failures where there were
**31**; the same shape again on the full-suite list; and `git show --stat | tail -12` cutting the
file lists into a **wrong precedent** about whether E31 rebuilt the index — an error that would
have flipped this arc's index decision had it not been re-measured.

**A distinct family from the unit/population laws.** There the population is mis-specified. Here it
is real, correctly specified, and **silently truncated by the instrument reading it**. Folded into
`CLAUDE.md`.

## The arc is closed on this seat's side

Verified independently: **`46e8369`** — 26 files, **zero** from `docs/index/`; **`6218ca9`** — the
db and certificate, alone. Tree clean, gate **19/19 all four legs**, post-rebuild `record_health`
**`SERVING`**, staleness null.

**The push is the Director's**, and the two questions the Gate 0 sheet puts to him — *is this the
armature mark*, and *does the 17.7%-of-width depth read as an object or a flat relief* — stay open
and are not this seat's to answer.
