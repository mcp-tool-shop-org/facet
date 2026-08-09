# Working in this repo

This file is about **how to work here**. What is *true* here lives in
[README.md](README.md) (the measured state of every tool) and
[docs/experiments](docs/experiments/) (the evidence trail). Read those for facts; read
this for method.

---

## Why this discipline exists

An earlier arc of this project ran ten sessions in which each session judged its own
output, wrote its conclusions to a shared memory store, and the next session read those
conclusions as established fact. Nothing in the loop was checkable and nothing was gated on
the Director's eye, so errors compounded silently for weeks.

The rules below are not process decorum. Each one was paid for. In the single session that
produced this repo, **six inherited or asserted claims were falsified** — the clay
provenance, the shell count, the facial ceiling, an archived resolution observation, a
coverage baseline, and a pass condition — and every one of them took minutes to overturn
*because it sat next to runnable code*.

---

## The three roles

| role | does | must not |
|---|---|---|
| **Director** (Mike) | sets direction; judges every artifact by eye | — |
| **Advisor** | writes specs, rules on reports, folds findings into the repo | execute, or grade its own rulings |
| **Executor** | runs the spec, measures, reports evidence | decide what results *mean*, or judge quality |

The separation is the point: the session that designs an experiment does not grade its
results, and the session that runs it does not decide their meaning.

## Rules for an executor session

1. **Never judge whether output is good.** Produce measurements and comparison sheets. The
   Director judges. The words *verified, shipped, works, decisive, validated, proven* do not
   belong in a report, a commit message, or a doc.
2. **State a prediction before you look**, and disclose whether it was blind. A hypothesis
   with no prediction cannot be wrong, and one that cannot be wrong teaches nothing.
3. **Stop at every gate. Never improvise past one.** A session that changed a parameter and
   re-ran when a gate fired hit the same gate harder. If a gate fires, report it with its
   evidence and halt.
4. **Do not write to the memory store.** The advisor folds findings into the repo after the
   Director has seen them. The repo is the record.
5. **A negative result is a full success.** Say so plainly and stop, rather than tuning
   toward a number.

## Rules for an advisor session

1. **Rule when the evidence is in; do not predict when it is not.** Deciding is the job.
   Guessing is not — check the advisor's own record below.
2. **Correct in place, with the measurement that overturned the claim.** Never quietly
   delete a wrong statement; the correction is more useful than the original.
3. **Pick a pass-condition unit the experiment cannot move.** Four conditions in this repo
   were mis-specified: two ratios whose denominators moved, then an absolute that broke
   because the experiment *halved the denominator on purpose* — painting 907,825 of 1.7M
   holes read as a "miss" against 923,466 of 3.5M. Ask what the intervention is designed to
   change, then measure something orthogonal to it. Here the honest unit was **dilated texel
   count** (2,551,893 → 813,773, a 68% fall), which cannot be gamed from either side.

   The fourth was a different mistake and is worth its own line: **never define a pass
   condition as a fraction of a quantity you have not measured yet.** E07 asked a ratio to
   "close half the distance from its baseline to 1.0". At the predicted baseline of 1.5 that
   is a trivial move; at the measured 5.5 it demands a 41% cut. The bar's difficulty scaled
   with how bad the problem turned out to be, which is backwards. When no calibrated threshold
   exists, **suspend rather than invent one** — `project_twins`' `assert seen.mean() > 0.30`
   is the precedent — report the numerator and denominator separately, and let the Director's
   eye rule. Retuning a condition after seeing the result is the one move that is always wrong.
4. **Own errors in the commit message.** They are how the next session learns which parts of
   the record to distrust.
5. **A dispatch is not delivered until its paste block is on the screen.** Ship the executor
   paste block *in the same message* as the dispatch, unasked — never "paste block on
   request." The Director had to ask for it twice before this line existed, and the ask is
   the defect: a spec sitting in `docs/experiments/` that nobody can start is a shelf, not a
   deliverable. The same applies to every handoff the seat produces — when a shelf clears,
   the next thing on the screen is the thing that starts the next arc, not a summary of the
   last one. **Keeping the project moving is the job, and moving means the next session can
   begin without another round trip.**
6. **Do not end a session the Director has not ended.**

## Rules for everyone

**An inherited claim is a hypothesis wearing a fact's clothes.** Checking one costs minutes;
building on one costs a session. If a spec, README or handoff asserts a number, verify it
before designing around it — including numbers written by the advisor.

**When you fix a root cause, find its other consumers.** E01 established that a Workbench clay
render is flat grey on flat grey, so a threshold cannot find the figure in it — and fixed the
*control-image* path by compositing onto contrast first. The **same function on the same
render** still keys the figure mask, and it was silently losing a quarter of the silhouette:
146,356 px of true surface against 111,602 used, the loss *interior* rather than at the rim —
a stripe down the whole blade, patches through pauldrons, chest and greaves. A root cause has
as many sites as it has callers. Grep for them when you fix one.

**Tests ride the commit that touches the code.** A studio standing rule (earned on
PixelStudio; "applies to ALL repos") that this repo deviated from through its first arcs,
surfaced by the Director 2026-08-08: verification here ran as recorded anchors and in-tool
invariants — real checks, run once and recorded in reports rather than kept runnable. Only
the index's four-leg verify and `texpass_iter`'s selftest persist. From the MCP build
forward: a commit that adds or modifies tool code carries tests for that code in the same
commit; anchors remain the acceptance form for measured artifacts, and re-runnable anchors
are ported into the harness rather than left in reports; a dispatch that plans a tool
change without naming its tests is missing a step, and the executor adds them unasked —
the studio rule's own words.

**A PNG hash mismatch is not evidence a render changed — file bytes are not pixel values.**
Twice now a hash check has produced a false halt on pixel-identical renders (encoder
metadata differs run to run). Compare pixels; reserve byte-hashes for artifacts whose bytes
are the contract (E08 armB state; E04 step 0).

**A number that reproduces exactly can still be measured against the wrong object.**
`project_twins` justified eroding the twin's mask with "the twin is painted fatter than the
mesh — 15.8% against 9.9%." Both figures reproduce to the digit. 15.81% is the *eroded twin*
and 9.94% is the *broken keyed mask*; against the true silhouette it is 17.43% against 19.01%,
and **the mesh is fatter**. Reproducibility is not validity. Check what the operands are, not
just whether the arithmetic replays.

**A global constant must not govern a local feature.** Three instances now, and each cost a
session: a blade rectangle measured on one character's silhouette and applied to a mesh 38%
narrower; an erosion tuned on a wide figure that ate 480k texels where the surface turns
edge-on; and an edge-distance scaled by *global figure width* that leaves a ~15 px blade with
no interior after 3.8 px is taken from each side. The cost of a fixed peel runs inversely with
local feature width. Derive the quantity per structure, or bound it as a fraction of that
structure's own width — and gate it by reporting, per structure, how much of its area the
operation removed.

**Grade an arm only on what it can move.** A stage-1 arm cannot be graded on reference
agreement: recovered texels carry the reference's own colour, so the comparison returns ~0
however the change went. An advisor asked for exactly that and an executor refused it, which
was right. Before adopting a metric for an arm, ask what value it takes when the arm does
nothing and when it works perfectly — if those are the same number, it is not measuring the arm.

**When you widen an acceptance mask, test that you did not admit background.** The check is
cheap and it is now standard here: compare the newly-admitted texels against the source's own
background colour. A2 admitted 257,506 texels at median ΔE 38.31 from background with 0.18%
within ΔE 10 — cleaner than the set already trusted. That is what makes a widening adoptable
rather than merely larger.

**A condition whose stated derivation does not describe it was never a threshold.** An
off-palette gate justified its 0.5% bound as *"set from the seven clean views measuring exactly
0 px"* — but that 0 px came from a different, cruder check; the gate's own clean baseline was
0.06–0.33%. **Withdraw such a condition rather than re-deriving it**, because re-deriving while
looking at the results it would judge is retuning however principled the reasoning. Withdrawing
is not choosing a new number, and that is the whole difference.

**Normalise a boundary quantity by perimeter, not by area.** Off-palette pixels live at material
edges, so they scale with perimeter — while figure *area* swings 1.65× between a profile and a
rear three-quarter on the same subject. A percentage-of-area bound therefore fails a clean
profile and passes a dirty front view. Fourth moving-denominator instance in this repo, and the
first found in an instrument written an hour earlier: **check what your denominator is made of
before the first result depends on it.**

**A detector that only reproduces what its author already noticed is not an instrument.** A
hand-rolled check asked *is it blue* and found one bad twin. The same question asked properly —
*is anything outside the declared palette* — found two, the second a 5,068 px olive-khaki mass
that had been seen at contact-sheet scale and dismissed. Write the check against the
**specification**, not against the defect you happen to have spotted.

**Derive a gate's reference from something other than what it gates.** The palette bands came
from the spec's named materials and were cross-checked against a *different image* than the
twins being tested. Taking them from the clean twins would have made the gate a tautology that
passes review because the numbers look fine.

**Two thresholds separate one wrong garment from ordinary speckle.** Clean views carried 5–104
px of off-palette pixels at material boundaries; the failures carried 4,882 and 5,068 in a
single blob. Total count alone must choose between missing the garment and firing on
everything — report the total *and* the largest connected component.

**Below a chroma floor, hue is not a colour.** It is undefined, and it will read as a rotation.
The same fact bit two instruments here: a contradiction test's hue column was meaningless
wherever chroma collapsed, and an off-palette gate without a floor flags a steel sword
(C\* 1.6–2.8 at hue 267) as blue on every view. Any hue number carries its chroma or it is not
quoted. And its third firing found the law's sibling: a transfer derived over a stone mask
that is 71–85% near-achromatic would have rotated the stone green and *desaturated* it —
the floor decides which pixels vote before any statistic of them means anything.

**A statistic of angles must be circular.** An arithmetic median of hues reported a +49.1°
move where the true direction was −8.4°, because garnet straddles the 0/360 wrap — the exact
family this route paints most (E14, the garnet derivation; caught before any number left the
script, by printing the after-state instead of asserting success). The chroma floor decides
who votes; a circular mean of unit chromatic vectors decides where they point. A hue centre
quoted in this repo is a circular statistic or it is not a centre.

**Rejecting an output that violates a pre-registered specification is not selecting a result.**
What is forbidden is choosing a *decision rule* after seeing the outcome. The test: would the
rule have been the same whatever came out? *Reject a twin containing material not in the spec*
passes that test — so re-rolling it is the specification working. Bound it anyway: one re-roll,
new seed, the rejected artifact stays in the record with its measurement, and a second failure
is the result rather than a third roll.

**Specify from scratch; never patch.** A specification determines what *occupies* a surface and
cannot add a second element to one already occupied. Asking for a gold plate onto an existing
fur cuff produced **no response at all** — ΔE 1.07, in two different grammatical forms, where
elements that *replaced* their surface's occupant landed in full.

**Before building a path to a resource, enumerate the resource.** A whole delivery path was
built — new repo, upload, browser import — for a model that was already present. The advisor
specified "check whether it can get there" when the first question is "is it already there": a
check whose shape assumed its answer, which is the recurring form of most advisor errors in
this repo.

**Canon is not a taste question to be routed around. It is a ground truth the Director holds,
and no metric approximates it.** The advisor did this twice in two experiments: graded material
identity with high-pass statistics, then graded *character* identity with silhouette IoU — and
pre-registered "better registration is a better reference, no taste required." A better-
registered twin that is a different man is worse, not better. When the real question is *is
this the right thing*, a measurable proxy is not a conservative substitute for asking; it is a
different question with a number attached. Ask, and show the artifact at full size.

**Twins belong to a mesh. Identity belongs to the prompt.** A twin has exactly one job — register
to the silhouette it will be projected onto — and E01's "regenerate them for whatever you are
about to texture" is right without qualification. Everything that makes the man *this man* is a
named element in a versioned prompt. This was learned the hard way: a registration improvement
silently replaced the character, because identity was riding in an artifact nobody had declared
was carrying it. The proof that it can ride elsewhere is one phrase — naming the gold knee
plates restored armour that had only ever reached the image through a *noisy ControlNet*,
with the control byte-matched so the term was the only difference. **If a canon element is not
named in the prompt, it is arriving by accident and will leave the same way.**

**A recipe that does not reproduce its output is not a recipe.** The canon twin, rebuilt from
the same clay, prompt, seed and control, does not come back (IoU 0.9040 against 0.9088) — its
parameters were never in the repo. Freeze such an artifact as canon, version it, and record its
provenance as *incomplete* rather than implied. Do not sweep for the recipe: a match cannot be
verified as *the* recipe, and the artifact is already in hand. Then fix the generator so the
next one is reproducible.

**A component can be necessary without being contributory.** The fitted background estimator
moves reference coverage by **−0.1 points** on its own and *enables* the +4.0 the new twins
buy, because the old key reads their backdrop at 50.68% of frame against a 19.01% truth.
Measured in isolation it looks like nothing and would have been retired; measured as a
precondition it is load-bearing. Ablating a component tells you its marginal contribution, not
whether the system works without it — decompose, but read the decomposition for *enablers* as
well as for contributors.

**A swap is not a gain until you have looked at what left.** An arm that is strictly additive
can be judged on its total; one that trades cannot. A2R gained 148,693 texels and lost 54,978,
and the net says nothing about whether what arrived is as trustworthy as what departed.
Characterise the losses by location and quality before banking the net.

**Corner-median keying has failed three times; it is retired.** A single background sample
assumes a flat field, and nothing in this pipeline has one: painted concept art has a gradient
and a cast shadow (E01, which keyed a third of the lower background as figure), a Workbench
clay render is grey on grey (which lost a quarter of the silhouette), and a diffusion model
paints a lit studio backdrop (which returned 31–76% painted against a 19.01% truth). Fit the
background over a border ring instead — a quadratic reduces to the corner median on a flat
field, so old numbers stay comparable. **Where geometry can answer the question, use geometry:**
*is there surface here* is the raycast silhouette, exactly, and keying should never have been
asked.

**Bbox-check any keyed mask against the geometry before reading a number from it.** *A figure
cannot be 751 px wide in a 752 px frame when the mesh is 388.* One comparison, free, and it
tests the estimator's failure mode rather than its success mode — it caught a broken key before
a single downstream figure was believed.

**"One variable" is a property of the dependency graph, not of the parameter you edited.** The
background arm changed one setting — the clay render's background colour — and thereby changed
*two* inputs to the generator, because the control image is built from a mask keyed off that
same render. Contour went 33,026 → 9,699 px alongside the intended change, and the result
could not be apportioned. Before running an arm, trace what the parameter feeds and pin the
consumers you did not mean to vary.

**A failure's signature tells you which cause to suspect.** The same run repainted the subject,
and the question was whether the background reached the latent or the control had been
weakened. The answer was in the *kind* of change: a latent colour cast shifts hue, and this
shifted **material and identity** — gold plates gone, boots to fur, wine-red to green — which
is the documented signature of a control that constrains nothing. Read what broke before
deciding what broke it.

**Distant medians do not imply a gap between them.** An advisor read two summary statistics —
region medians around 25 against a contaminated set's median of 4.9 — as evidence of a
separable distribution, and specified a threshold "derived from the measured bimodality."
Measured, the density rises monotonically from ~5 to 30 with **no antimode at all**, and the
two views disagree about where a dip even is. Two populations with different medians overlap
continuously unless you have looked at the density between them. Plot it before you claim a cut
exists.

**A threshold method reports its own confidence in the wrong partition.** Otsu returned
η = 0.661 — a healthy-looking score — while cutting dark paint from light paint and rejecting
41,194 px at a median depth of 8 px, deep in the figure's interior. The class we cared about
was 0.5% of the data, and between-class variance finds the *dominant* split, not the one you
want. When the target class is a small minority, a global thresholding method will confidently
answer a different question.

**A guard whose stated reason is wrong may still be load-bearing for a reason nobody wrote
down.** The edge erosion justified itself with a comparison measured against the wrong objects
— and was simultaneously removing background-contaminated tendrils from the twin's mask, which
nothing in the repo had noticed and no comment mentioned. Voiding a justification is not
grounds for deleting a guard; it is grounds for **measuring what the guard actually removes**.
Take it out in a run you are prepared to throw away, and look at what comes back.

**Test the property, not a geometric proxy for it.** The question was *is this pixel
background-contaminated*. The pipeline asked *is this pixel near a boundary*, which is a proxy
that fails precisely where the subject is thin — a 1–2 px structure is entirely boundary, so
half-width turns out to measure what fraction of a structure is edge rather than how thin it
is. Contamination concentrated 200× in the thinnest strata while being 0.5% of the mask
overall, invisible in aggregate for four experiments. When the property is directly
measurable, measure it; a proxy inherits every failure mode of the thing it stands in for and
adds its own.

**Put the andon on the direction the invariant does not bound.** When a change introduces an
invariant, that invariant forecloses one failure direction *by construction* — so a halt aimed
there fires on correct work while the live risk goes unwatched. A3 bounded over-erosion with
`e ≤ ⅓ × local half-width` and was then gated on how much area the erosion removed: the
invariant held exactly, zero violations, and the gate halted the build anyway. The unwatched
direction was the opposite one — a looser mask admitting background at the reference's painted
boundary — and the instrument for it already existed. Ask which way the change can still go
wrong *after* the invariant, and gate that.

**A diagnostic and a gate are different objects.** The same measurement can be the best
evidence you have and an unusable halt. Stratum area-loss proved the shipped erosion was
annihilating thin structure — 100% / 100% / 77.6% of the three thinnest strata, by a guard
built to delete a 1–2 px rim — and it is required in every report of that arm. It cannot gate:
it is a perimeter-to-area statistic that swings ±10 points on shape alone and is not bounded
by the invariant it was meant to protect. Before promoting a number to a halt, ask what else
moves it besides the thing you are watching.

**A check that cannot fail is not a check.** An executor tested the erosion hypothesis by
comparing the saved mask against its own dilation — an operation that cannot lose a pixel — and
got 0.00%. It was reported as *untested* rather than as confirmation, which is exactly right,
and it is the same family as the silhouette-IoU gate that returned 1.00000 on a holed mesh.
Before trusting a 0, ask what a non-zero would have required.

**A gate that a scripting accident can separate from the action it gates is not a gate.** An
invariance ANDON fired on stroke 7 of a brush run and the commit ran anyway, because check and
commit were chained in one PowerShell call that walked past the failing exit code — 47,020
texels committed after a fired gate, and a pass-shaped log entry for a failed condition. Nobody
decided to proceed; the construction was incapable of stopping. **The check lives inside the
tool that performs the irreversible step**, with no skip flag (E08 Amendment 32). A shell chain
is a transport, not a guard.

**And a gate is never a bare `assert`.** `assert` is a developer's sanity check that the
interpreter is licensed to delete: `python -O` and `PYTHONOPTIMIZE=1` remove it silently and
execution continues past it. Measured on one gate at both trees — before the repair it FIRED
normally and was SILENT under `-O`, under `PYTHONOPTIMIZE=1`, and under both; after, it fires
in all four. **87 of this repo's ANDONs were removable by an environment variable**, including
every one in the write-head, which is strictly worse than the shell chain above: the chain at
least let the ANDON print, while under `-O` the gate never speaks, the write proceeds and the
process exits `0`. A check that decides whether an irreversible step proceeds must `raise` —
the separator does not have to be a shell chain to be a separator, and an env var is a cheaper
accident than one. E21 Ruling 2 wrote this law; **E22 converted the ruled 88 sites and E22
Ruling 9 is the fold that finally put it here, several folds late — a law that lives only
inside a ruling document is the failure the record was built to escape.**

The carve-out is real and is part of the law (E22 Ruling 3): a check labelled
`IMPLEMENTATION:` rather than `ANDON:` may stay an `assert` — two such sites sit in converted
write-path tools and each carries a comment declining andon status *because halting there fired
on correct work once already*. **The token is an author's declaration, not a marker someone
forgot to type.** A gate whose author never declared it is a documentation defect at that site,
repaired by writing the token — not a reason to widen the rule to every assert.

**A gate that measures the RESULT halts. A gate that measures the environment's ability to
run the measurement may be repaired.** The halt rule's own stated reason is that a session
which *changed a parameter and re-ran* hit the same gate harder — it is about tuning a
measurement until it passes. E23's CI gate fired because `restylize_views` imports `cv2` at
module level and CI's pinned install never had it: no test had ever invoked one of those
twelve tools, so the gap could not surface until the first one did. Nothing about the
measurement was touched. That collided with **"never leave CI red"** and nothing said which
wins. The boundary: a repair is allowed when it **adds capability rather than removing
coverage**, the coverage-removing alternatives are **named and rejected in writing**, and
the firing is reported as a fired gate rather than smoothed into a green row. Narrowing a
test to make a red gate green is forbidden whichever kind of gate fired.

**A report may not contain a placeholder shaped like evidence.** A CI run id was written
into a gate row with a `PASS` beside it *before CI had ever run*, and committed;
`gh run view` returns **404 — it never existed**. A gate that has not run is written
`NOT YET RUN`, never a plausible identifier with a verdict next to it. Nothing here could
have caught it: the index's pointer leg checks that a *row's* file exists and its locator
is findable, and cannot see an `https://` URL sitting in prose. So **the advisor resolves
every external citation at ruling time** — one call per id, and sweep the class rather than
the instance.

**Check that the population is real before you predict its density.** A dispatch computed its
out-of-scope class as *total minus a five-tool subtotal* and named the difference "~207
developer sanity checks"; measured, that class is **16**, and the other 191 are declared gates.
An executor then predicted how many members of that phantom class guarded a write, took an
untutored 8–12, **halved it on this repo's own "densities run 2× high" lesson**, and measured
175. The calibration ritual moved the answer away from the truth and made the move look like
discipline. A quantity predicted about a mis-specified population cannot be right. **Two arcs
running, the scope number has been the defect rather than the work** — derive a scope by
measuring it, never by subtracting one. **And put the remaining count under a test**: E23
pinned its 134 successor sites in the harness, so the next arc's scope cannot drift
silently — moving it requires editing the test, on purpose, in the commit that moves it.

**Then check what the metric's unit is, not just that its population is real.** One level
below the law above, and it cost E23 its only clean miss: a prediction of how many gates
sit before a write reasoned about *files* — "route tools write more" — while the instrument
measures a **scope**. 4 predicted, 20 measured. A tool that writes more can have *fewer*
gates with a write in scope, **because writing more is what makes you factor the writing
out** — decomposed tools put their gates in small validators that check an input and
return, leaving the write to the caller. Ask what the denominator is made of, not only
whether it exists.

**When a number will not move, check the baseline.** The most valuable measurement in this
repo's history came from an executor who stopped chasing a stuck figure and asked whether
the thing it was compared against was real. It was not.

**Bound an expensive arm before spending it.** Compute the ceiling first. One executor
priced a six-stroke experiment at +1.7 points before running it, and skipped it.

**Validate a metric against a rejected artifact before building an experiment on it.** Take
something the Director has already turned down, and the region he named, and confirm the
number fires there. E07 graded four arms with blotch counts, speckle, a step ratio and a
flattening guard — **four of the five are 5×5 high-pass statistics, and the fifth is
indifferent to where a colour lands.** The defect that decides acceptance is a *large region
of the wrong material*: a steel blade wearing skin, a boot wearing gold. Such a region is
smooth inside itself and contributes only its rim to every one of those numbers. So an arm
took source distance down 70×, mean fallback to zero and speckle below A0 — and the asset was
unchanged to the eye. A metric that cannot separate an asset he rejected from one he accepted
is not a metric. This cost four experiments; every gate error below cost one.

**A gate must test the operation's failure mode, not its success mode.** A cull was gated on
silhouette IoU — which is structurally blind to holes punched through *visible* surface,
because the ray behind a removed face still hits geometry. IoU returned 1.00000 on a mesh
with a hole clean through it. The executor noticed the gate could not see its own failure,
added a first-hit depth comparison, and it fired immediately. **Ask what the operation would
look like if it went wrong, then check for that.**

**And gate on the failure itself, not on a proxy for it.** The second version of that error is
subtler and cost a halt in E07. A surface-aware lookup fails by *sourcing colour from
somewhere else on the figure*; the gate was written on **normal disagreement**, a stand-in for
it. The stand-in inverted — the back-facing sources were the *closest* ones, 0.77 triangle
edges away, opposing faces of a sheet thinner than its own tessellation — while **no** lookup
reached beyond 20 edges, against 72.2% for the flood it replaced. A proxy fires on whatever
correlates with it, including the subject's own geometry. If the quantity you care about is
measurable, gate on that quantity and leave the proxy as a reported diagnostic. Then check
what the threshold's unit is pinned to: E07's replacement is stated in *triangle edges*, and
`texpass_finalize.py` had that edge length hardcoded from one mesh.

**Prefer eliminating a risk to gating it.** When the same cull was changed from *deleting*
faces to *excluding them from the atlas*, the failure became impossible rather than
detectable — geometry is never modified, so the silhouette cannot change and a future camera
sees flat grey instead of a hole. A guarantee that depends on nobody adding a camera is not a
guarantee.

**Failures stay in the repo, next to the code, with the reason.** `tools/superseded/` is not
an archive; it is the mechanism that stops a falsified approach quietly becoming doctrine
again. Anyone can run those tools and watch them fail the same way.

## Judging artifacts

- **Textures under FLAT light.** A Blender Workbench STUDIO render is not a texture readout —
  grey chalky facet mosaics are specular highlights on flat-shaded normals and vanish under
  `--flat`. Two debugging rounds were lost to this.
- **Geometry under `--clay`.** Texture hides geometry; that confusion caused a whole session
  of misdirected work.
- **At the Director's zoom, not from a contact sheet.** Defects that decide acceptance are
  invisible at thumbnail scale.
- **Beside the reference, with provenance.** The cheapest diagnostic in this repo is
  *reference | asset | provenance | error* on one sheet, and it did not exist until E08's
  Gate 0. E07 ran four arms and two gates without once putting the asset next to the thing it
  is supposed to look like. When the sheet was finally built, the Director read the whole
  thesis off panel 2 in a sentence — the blade is flesh where the reference is steel, and the
  provenance panel shows it carries no reference at all. **Build that sheet before the
  metrics, not after them.** A number tells you a region is wrong; the sheet tells you what it
  was supposed to be, which is the part that decides what to do next.

## Experiments

Every non-trivial change runs as a numbered experiment in `docs/experiments/`:

```
spec written BEFORE the work  →  report written AFTER  →  advisor ruling LAST
```

A spec carries: the question, hypotheses with predictions, arms varying one thing each,
the metrics, the gates, an explicit out-of-scope section, and a standards-compliance block
scoring the six workflow standards. Amendments are appended in place with dates and reasons
— a spec that hides its own corrections is the thing we are trying to get away from.

## Environment

This is the Robot rig — **drives C and E only. No D:, no F:.** Any `F:/AI/...` path in an
inherited document means `E:/AI/...`.

```
python    E:\AI-Models\trellis2-env\Scripts\python.exe
blender   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
assets    E:\AI\training\facet_E0*\  and  E:\AI\training\saltroad_bake_fix\
```

**Run all Blender work through PowerShell** — Git Bash mangles the paths and every call
fails with `Error: Please select a file`.

**Generation runs on Comfy Cloud. Geometry and measurement run locally.** The restylize graph
stages **31,006 MiB** of models against a **31,200 MiB** watchdog ceiling on a 32,607 MiB card;
the working set reached 30,809 with nothing left for activations. **No reserve value fixes
that** — peak was 31.7–32.0 GB across three runs regardless of the reserve *or* the desktop
baseline, because ComfyUI stages to fill whatever it sees free. Freeing 6.5 GB by rebooting made
the working set grow 6.1 GB, so the earlier passes succeeded *because* less VRAM was available.
`--reserve-vram` and `--disable-smart-memory` are both falsified as levers here. **The ceiling
is never raised.**

**Moving a line to different hardware needs an anchor first.** Reproduce a known output from its
recorded parameters before running anything measured. Ours came back non-byte-identical at
ΔE 0.84 against a pre-registered 1.07 no-response floor — accepted, with the hardware boundary
recorded in every later report. And read the *shape* of that residual, not just the number: it
was uniform across every structure, which is what two float kernels look like. A structural
difference concentrates.

**argparse eats leading minus signs** — use `--views=-30,0,30`.

**A Comfy Cloud `dry_run` PASS does not prove link sanity.** A hand-retyped payload with a
self-referencing node link (`VAEDecode.samples = ["14", 0]`) returned `status: validated`
(E04 Arm G7). Submit saved workflow files verbatim; check link topology in code — self-links
and dangling targets — before submission.

**Scripts must create their own output directories.** Two runs died on this.

## Standing technical constraints

These are physics and measured traps, not settings. They are subject-independent and stay in
code rather than in a profile — see [docs/profiles-design.md](docs/profiles-design.md) for
the boundary.

- **Weld before decimating.** An exported glTF splits a vertex at every UV seam; collapse
  decimation on the result tears holes because per-triangle shells have no neighbours.
- **No volumetric predicate on an exported mesh.** It is not a solid — signed distance at the
  centre of a standing figure's chest reads *outside*. Containment, thickness and
  inside/outside must run on the welded mesh, before export. **And even welded, the mesh is
  not solid**: every TRELLIS.2 `1024_cascade` reconstruction on this route is a hollow
  double-walled shell — walls ~two voxels around an empty cavity, measured three independent
  ways with the accepted dragon and galleon as controls (E14 Ruling 3). The figure's interior
  is cavity and reads *outside* by parity; a volumetric consumer must address the outer wall
  specifically. The route itself never meets the inner wall — invisible surface, culled by
  construction.
- **A ray along the surface normal measures the tessellation, not the geometry.**
- **Twins belong to a mesh, not to a character.** Regenerate them for whatever you are about
  to texture.
- **Build the control image; Canny cannot find a silhouette that is not there.**
- **One mask cannot answer two questions** — the mesh silhouette answers *is there surface*,
  the twin's own mask answers *is the paint trustworthy* — **and the trust question is only
  askable where surface exists**: the trust mask is intersected with the silhouette before
  the distance transform (E08 A27; unbounded, paint on no surface held erosion off 7,574
  texels and corrupted a fifth to a quarter of every view's edge distances).
- **Order strokes to spiral outward from already-painted regions**, or the brush composes a
  new character instead of continuing one.
- **Generation frames must be generator-legal.** The Qwen VAE downsamples by 8: a width not
  divisible by 8 decodes short (1066 → 1064, every twin 2 px off its control — E04 Ruling
  15) and breaks every downstream pairing. W3's 752 and the pair's 1024 passed by luck.
  Derive the frame from the mesh, then round to the nearest legal width; ÷8 is the floor,
  prefer ÷16.

## The advisor's record, for calibration

Kept because a future advisor should know which parts of this repo to distrust. In the
founding session the advisor was wrong about: the shell-soup premise, the clay provenance,
the double-subscribe diagnosis, `--no-head-scale`, the head-pixel multiplier, the halo
hypothesis, `angle_limit` as a lever, deferring the blade fix, and two pass conditions.

In E07 the advisor was wrong about two of its own gates, both written into the spec: the
back-facing ANDON, which measured a proxy that inverted on this mesh and halted a correct
arm, and a pass condition defined as a fraction of a baseline nobody had measured. Both were
caught by an executor who ran them as written and reported the evidence rather than tuning
past them. The spec's step ratio and its Gate 0 premise tests held up.

The advisor was useful at: ruling once evidence was in, killing options with reasons,
refusing to commission a metric where no honest one existed, bounding an expensive arm before
spending it, and correcting the record in place.

**Deciding is the job. Predicting is not.**
