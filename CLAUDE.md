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

## How an experiment is run — the dispatched-seat standard (Director, 2026-08-16)

**Standing from 2026-08-16: the advisor spawns the executor itself, as a background agent, and
steers it on an open line.** The Director's words, making it the standard: *"much more
effective, allowing you to freely maneuver."* He is out of the loop by default — the advisor
decides, the executor measures, and he sees an artifact when there is something for his eye.
**The advisor may also run research and study swarms (Sonnet-based) on its own authority**;
the studio protocol at `memory/research-grounded-advisor-protocol.md` governs their form.

**The model tier is the advisor's call, and the Director set the default (2026-08-16):
`Sonnet` executors for most experiments, `Opus` where technical skill is genuinely needed.**
E40 ran its three parallel seats on Sonnet and they killed the swarm's blade hypothesis, killed
the advisor's re-bake claim, caught their own degenerate metrics, and found the two-band split in
`project_twins.py` that the advisor's own spec had described wrongly — so *most* is the honest
default and not a concession. Reach for Opus when the seat must **design an instrument rather
than run one**, hold a large uncommitted refactor across many files, or reason about a
correctness argument where being subtly wrong is expensive and hard to detect. **Pick per seat,
not per arc** — one Opus seat beside two Sonnet seats is a normal shape. Research swarm agents
are Sonnet unless a brief demands otherwise.

**What this does not change.** The three roles above are untouched. The executor still never
judges quality, still predicts before it looks, still halts at every gate. The advisor still
does not execute and does not grade its own rulings. The Director's eye is still the only
acceptance gate. The separation is *why* the method works, and dispatching a seat rather than
pasting into one does not soften it — in E38 it was a dispatched seat that killed the
advisor's parked-face hypothesis, its invented threshold, its `--reunwrap` arm and its
island-count comparison.

**What it changes, and what each change cost.**

- **On-disk state is the record; a transcript is not.** Two executor transcripts were lost
  inside E38's first day, one at ~500k tokens and one without warning. Both times the arc
  continued and lost nothing but memory, because predictions, reports, scripts and arrays
  were on disk under `E:\AI\training\facet_E3*\`. **A dispatched seat writes `handoff.md`
  early and keeps it current** — not at the end, when it may not get one.
- **The dispatch IS the spec, and it must land in the repo.** An agent prompt nobody can read
  afterwards is worse than a paste block, because a paste block was at least on a screen.
  The advisor records each dispatch and each mid-flight ruling in the arc's own document.
  *E38 currently owes exactly this and the debt is the advisor's.*
- **An executor does not delegate its own core measurement to a child agent.** One seat
  spawned a background child for its bisect and then idled waiting on it — invisible to the
  advisor, unsteerable, and stalled until the advisor read the disk and unstuck it.
- **The advisor reads `git status` before every fold and commits by pathspec.** Dispatched
  seats work uncommitted in a tree the advisor also writes to. This very section was folded
  with an executor's live tool edit and its new test sitting unstaged beside it.
- **Steering mid-flight is the point.** A dispatch is a living document: an arm can be
  withdrawn, an order re-ranked, a threshold retracted while the seat runs. The corrections
  above returned within minutes of the dispatches that carried them, rather than at a session
  boundary — which is the whole difference between an error costing an exchange and an error
  costing an arc.
- **The paste-block law is not repealed; its mechanism moved.** Advisor rule 5 below exists
  because the Director once had to paste kickoffs, and a spec nobody can start is a shelf.
  Under this standard the advisor starts the seat itself, which serves that purpose more
  directly. The rule still binds for anything only the Director can begin.

**Search for prior art before deriving it (Director, 2026-08-16: *"utilize every recourse as
we experiment"*).** Standing practice, and it paid on first use. Three arcs hunted the
dark-mark class through the image generator; ~60% of it was atlas texels no bake ever writes
— a problem game artists have solved for as long as UV atlases have existed. **Four parallel
research agents against the practitioner literature returned, in about twenty minutes:** the
mechanism named verbatim in Blender's own tracker with a fix already **merged** (PR #161752,
*"if a triangle does not overlap texel center, it will be empty"*), a ~16-defect catalogue in
`ADJACENT_FACES` explaining why the `EXTEND` arm worked (PR #162226, #119393), the confirmation
that carrying UVs through decimation is the reverse of every documented pipeline, and the blunt
finding that this route skips the high-to-low transfer bake that even AI-mesh pipelines keep.

⚠ **Two of those three citations were WRONG, and this section is the proof of its own last
sentence.** Resolved at `/api/v1/` 2026-08-17, one call per id: **#161752 is merged and its
body does match** — conservative rasterization, texel-centre sampling. **#162226 is OPEN, not
merged** — an adjacent-faces margin rewrite. **#119393 is OPEN and is a single defect**
(adjacent-faces dilating inside a UV island, 4.0 against 3.6), **not a ~16-defect catalogue**;
that characterisation was a research agent's summary and nobody had opened the issue. The
correction matters because the ranking depended on it: conservative rasterization writes
chart texels a triangle overlaps and **cannot** reach a UV that lands 17 px into a packer
gutter, and adjacent-faces is not in this Blender at all. **The `~60%` in the sentence above
is also a research-agent figure about the historical dark-mark class and has never been
re-measured**; what IS measured, on the current renders, is a different and much smaller
class — see the unmapped readout below.
**Everything found that way is a hypothesis to verify locally, never a fact to adopt** — an
outside claim gets exactly the treatment an advisor's claim gets. Resolve every external
citation at its primary source before ruling on it: `projects.blender.org` 403s to a plain
fetch and answers at `/api/v1/`, and the difference between a search snippet and the issue body
was, in this instance, the difference between "matches our config" and "is a different defect in
the same setting."

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

**And its fixture-side sibling: a fixture that passes under the implementation you are
REPLACING does not test the change.** A check built to compare *parsed graphs rather than
text* — because a JSON re-dump can differ in whitespace without a value moving — reached for
the three saved/submitted pairs in its corpus as its PASS evidence. Enumerated first, all
three are **byte-identical, same sha256**: they pass under a text comparison too, so they
cannot demonstrate the one property the check exists for. Sound fixtures, useless leg. The
repair has the same shape as the law above — construct the discriminating case, and **assert
the bytes really did change before asserting the graphs compare equal**, or the leg cannot
fail — then pin the byte-identity separately so a corpus change arrives as a notification
rather than a silent weakening. **Ask of every fixture: what would this look like if the code
were wrong in the specific way this check exists to catch?**

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

**And one level below that: a real population whose members you never checked for the
property still breaks the prediction.** Fifth consecutive arc to miss on this family and
the first of this shape. E27 predicted how many of eight tools could be tested
hermetically; the eight names were real and every member was real, but the prediction
carried an unexamined assumption — *that each one has an instrument to be hermetic about*.
Three did not. 6 predicted, 4 measured, and the mechanism was scope, not fixtures. The
dispatch's ritual — write what one of the counted thing **is** before the number — keeps
the population honest and did its job; it does not ask what each member **has**. Before
predicting how a set behaves, check the behaviour is even defined for every member.

**And below that again: a composite definition is governed by its rarest clause.** Sixth
consecutive arc on the unit family. E28 pre-registered *invocable* as `argparse` ∧
`add_argument` ∧ `__main__`-guard, then predicted 60 of 99 by reasoning about the flag
surface alone. Measured: the conjunction holds on **5**, because the guard clause holds on
**6** — the components landed 93 and 6, so the prediction was *above* band on the clause it
reasoned about and off 12× on the join. The directory's house style is a straight-line
module-level script; no amount of thinking about "how disciplined is this repo" reaches 5,
because the number was never about discipline. **Predict each clause of a conjunction
separately, then the join; the join tracks the rarest clause, not the salient one.**

**An instrument that lives inside its own population must be checked against itself on
every axis, each time — and one clean check is not clearance.** E28's census reads the
corpus and `tests/`, while its output is a corpus file, its tests are test files, and its
report is a corpus file too. Four self-references in one arc; **three moved a number**: the
committed output made axis D read 99/99 on any second run; the arc's own report re-created
the same contamination at arc scale, caught by an idempotency gate that FIRED (76 → 99, 51
rows); and the repair's own can-fail fixture named a real module and moved the count it was
verifying, 44 → 45 *by the test existing*. The first self-reference check came back clean
and stopped being true two edits later. The remedies that held: **exclude the instrument's
own derived artifacts from its evidence by construction, use synthetic names in its
fixtures, and pin both with legs that fire on the contamination** — three of the four were
found by a check firing, one by reading, and the ratio is the point.

**Enumerate the resource before commissioning one — including when an executor has already
named it.** E27's report identified that `offsurface_rate` had no invocable instrument
(true: `e10_offsurface.py` binds its subject as module constants) and framed the remedy as
*parameterise it or commission a fresh one*. It had itself named `e12_offsurface.py` one
clause earlier as "the erode/margin form, excluded" — and one `grep -c add_argument`
shows that file takes **nine** flags with a required `--prep` and no hardcoded subject.
Its docstring's first line is *"E10 Ruling 4's question, any subject"*, and it exists
precisely because editing a shipped instrument whose numbers sit in a closed ruling was
refused by an earlier seat. **The instrument was already built.** This is the advisor's own
recurring failure shape — *a check whose form assumed its answer* — found in a report, so
the lesson is general: naming a resource is not enumerating it.

**A closed ruling freezes its own text, not the tool that produced its numbers.** A spec
recommended excluding a whole instrument family on the grounds that *"a shipped instrument
whose numbers are cited in a closed ruling"* may not be edited. The Director asked why that
ruling exists. **It does not.** Searched across all 25 ruling documents: **no ruling in this
repo forbids editing an instrument.** The sentence originates in one executor's docstring
explaining its own choice, and two documents then cited it as binding at three sites — both
in the words *"the record already refuses this move."* The record refuses no such thing.
What **is** ruled is narrower and stays: a correction that rewrites a closed ruling would be
revision, not correction (E10-off Ruling 1 — whose object is the ruling **document**), and
*an instrument does not change under the session using it* (E12 Ruling 6d/6e, which
**scheduled** two repairs for after the handoff rather than forbidding them). One is
textual, one temporal; neither is a permanent prohibition on a tool. **And the hazard the
folklore stood in for is real, different, and checkable: a cited number must still reproduce
from the tool at HEAD.** So a cited instrument may be edited under the discipline already
applied to 278 sites in this repo — prove the edit non-perturbing, or carry an anchor that
reproduces the cited number, **in the commit that makes the edit**. A taboo nobody can cite
is not a guard; it is an inherited claim wearing a fact's clothes, and it survived three
citations because each one was reading the last rather than the record. *The one site that
handled it correctly was the served tool's own refusal text, which routed the question to a
ruling instead of assuming one.*

**Existence of the operands is not replayability.** Seventh consecutive arc on the
unit/population family and a new member of it. E30 predicted how many recorded stages could
be anchored, checked that each one's artifacts *exist* — they all do — and missed by three,
because a replay needs a **second** thing nobody enumerated: **a tool that can still be
asked the recorded question.** `project_twins`' erosion was rebuilt under E08 A3, so the
recorded rule is no longer the default and three projections whose every input is present
are not replayable by default. The family now reads: the *unit*, the *population*, an
unchecked *property*, the rarest clause of a *conjunction*, and now the *instrument's
continued ability to express the question*. Before predicting that a record can be
reproduced, check that something can still ask it.

**And the eighth member is the one an executor has least reason to doubt: the premise it
inherited from its own dispatch.** E29's spec asserted *"there is no segmentation stage in
front of the reconstructor"*, and its P1 predicted the concept mesh would come back fused to a
dungeon wall. There is a segmentation stage — **inside** the reconstructor: `pipe.run` resizes
to a 1024 max edge, runs `rembg` where the input has no alpha, and square-crops to the alpha
bbox, so masonry filling 100% of the non-figure frame never reached the geometry. Measured
z-min slab area **0.2614%** against a predicted 6% (band 2–20%). **The sentence was the
advisor's**, and the law about inherited claims applies with most force to the one document an
executor is least likely to check. *Two minutes of reading the pipeline would have overturned
the prediction before it was written* — so read the mechanism you are predicting about, and
when you write a dispatch, mark which of its premises you measured and which you assumed.

**When you enumerate the ways a thing can break, check the thing is PRESENT before you
enumerate how it misbehaves.** E31's dispatch specified three failure layers — resolver,
missing instrument file, missing import — and asked which one each of eight tools hit. Measured,
there is a **layer 0 in front of all three**: at the shipped wheel the server module is *not in
the artifact*, so "where does it fail" has no operand. The advisor's own error, in a dispatch
rather than a prediction, and the same family as everything below: **a population of failure
modes that omits its first member.**

**And the object a count is over is part of its unit.** Ninth consecutive arc on this family.
E31 predicted how many of eight tools survive an install tier and **counted a surviving *path*
as a surviving *tool*** — several tools share one code path, so the two are different
populations wearing one number. The family now reads: the *unit*, the *population*, an unchecked
*property*, the rarest clause of a *conjunction*, the *instrument's continued ability to express
the question*, the *premise inherited from your own dispatch*, and **the object being counted**.
Its sibling in the same arc: a predicted **total** missed above band because *the term that
dominates it was never measured* — open3d's manylinux wheel is 6.5× its Windows one.

**A share measured in one space is not a claim about another.** Tenth arc, and the first where
the mis-united number was the *advisor's own reasoning basis*. Every `dilation` figure this repo
argues from is in **atlas texels**; the defect is judged in **rendered pixels**; on W3 the two
differ by **5.4×** — 26.95% of the written atlas against 4.95% of what any camera sees, a ratio of
**0.18×**. The mechanism was already written down one section away: *paint lives in big charts,
holes live in small ones*, so the same inspection paradox that makes a dilated texel's island
small makes it cheap in screen space. **Before quoting a provenance share, say which space it is
in** — and if the question is "what does the asset look like," atlas shares are the wrong space.

**And the eleventh: a prediction must not name a value the instrument cannot return.** E39's seat
predicted 75% for a rate whose **ceiling — the instrument's reading when the answer is
unambiguously yes — is 63.66%**. The prediction was above the maximum the measurement could
produce, so it could not have been right at any state of the world. Its own diagnosis is the
lesson: *"the controls were in the design and absent from the prediction."* The seat had built a
floor and a ceiling into the instrument and then reasoned about the mechanism alone when writing
the number. **Compute what your instrument reads when the thing is definitely true, and when it
is definitely false, and predict inside that interval** — the same question this repo already
asks of a metric before adopting it (*if those are the same number it is not measuring the arm*),
turned on the prediction rather than the metric.

**And the same law governs a DECISION RULE, not only a prediction: a threshold placed where the
instrument cannot discriminate is not a threshold.** E40's gold seat asked whether a colour is
the majority or the minority of the views that see it — a 50% line. Measured on the *definitely
yes* population, unambiguously gold surface, **the instrument reaches a majority only 52–62% of
the time.** So the decision line sat *above* what the instrument returns when the answer is yes,
and a 35.86%-vs-32.63% split against it means almost nothing. **Calibrate the rule against the
instrument's own yes-and-no populations before reading a verdict off it** — the seat had built
both calibration populations and reported the raw split anyway, which is how the trap survives
being known.

**A bound is not a measurement, and which direction bounds firmly is a property of the
evidence.** The same arc got this right and it is why its result is usable: *twin is clean at
this pixel* proves the colour came from elsewhere, because **one view's absence is decisive about
that view** — a firm lower bound of 29.9%. *Twin is gold at this pixel* proves only that this
view is **a** source; it cannot poll the other seven, so 70.1% is a **ceiling on the complement,
not a measurement of it**. The asymmetry was pre-registered before the number existed. **State
which side of a two-sided question your evidence can close, before you look** — otherwise the
loose side gets reported with the tight side's confidence.

**An identity envelope that does not record the dependency set is not portable.** Every
open3d-dependent number in this repo was measured against **`0.19.0+241aaee`** — a cp313
*development* wheel from Open3D's `main-devel` channel, because PyPI's latest release publishes
cp38–cp312 and **no sdist**. Four of the eight served instruments need it. The envelope carries
server version, instrument sha256 and config hash and **not** what the instrument imported, so a
number reproduced elsewhere against released `0.19.0` is compared to one produced against a
git-hash-suffixed build and *nothing in the payload can see the difference*. Nothing recorded is
withdrawn — this names a comparability component that stays invisible while one rig produces
every measurement, and becomes load-bearing the moment the tool is published.

**A row you predict to be uninformative is still a prediction, and it can miss.** E29's P4 hit
every band it stated and was wrong about what they meant: it said the face/vertex counts could
not separate the arms, said so out loud as a virtue, and the arms then differed by 3.66% —
**13.7× a noise floor that did not exist when the prediction was written.** A claim that a
measurement cannot discriminate is a claim about the measurement, and it needs the same
falsifier as any other.

**And when a tool has changed under an accepted asset, look for the era flag before
commissioning one.** E30 reported *"no flag restores the old rule"* and proposed a new mode;
`--edge-absolute` was already at `project_twins.py:103`, consumed at 754 and 797, and the
report had quoted the comment naming it while reading past it. **Third instance of
*enumerate the resource before commissioning one* in a single session** — the others were
`e12_offsurface.py`'s nine flags and a model already sitting on the rig. One grep separates
a commission from a flag that exists, and the commission is always the expensive branch.

**When two seats are live, the count surfaces are the advisor's to reconcile after both
land.** T34 pins a stated count against `pytest --collect-only` *of the tree the surfaces sit
in*, so two parallel seats adding tests **cannot both be green independently** — E30's commit
was self-consistent at 801/761, task 3's at 797/768, and only the combined tree at 808/768 is
correct for either. Neither seat can be right alone, so neither should be asked to try, and
an executor that reports the collision and touches nothing has done the right thing. Reserve
the count surfaces in the dispatch, not just the status table.

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

**A conclusion read off a truncated listing is not a measurement.** Found by an executor in E32
after its own precedent reading was overturned, and it had already fired **three times in that one
session**: a pytest summary read through `Select-Object -Last 12` reported **11** failures where
there were **31**; the same shape recurred on the full-suite list; and `git show --stat | tail -12`
cut the file lists into a **wrong precedent** about whether a prior commit rebuilt the index — an
error that would have flipped an advisor ruling had it not been re-measured. **This is a distinct
family from the unit/population laws above**: there the population is mis-specified; here it is
real, correctly specified, and **silently truncated by the instrument reading it**. `tail`, `head`,
`Select-Object -Last` and default row caps all return a plausible, well-formed, incomplete answer,
and none of them say so. When a listing decides anything, read it **complete** — count it, write it
to a file, or use a form with no cap — and prefer a command that reports a total (`| wc -l`,
`--name-only`, `--count`) so a truncation surfaces as a mismatch. **A paging flag is not a
measurement instrument.**

**And its sibling on this rig: a shell quoting form that does not expand returns a plausible
number rather than an error.** `grep -c $'\r'` does **not** expand in the Bash tool here — it
degrades to counting lines containing the letter **r**, and reported *"CRLF on 440 lines"* for a
file with **zero** CR bytes (E55). Nothing failed; a well-formed integer came back and it was
measuring a different question. **For line endings use `git ls-files --eol`**, or read the bytes
in Python. The same caution applies to any `$'…'`, `!`, or backtick form: verify the quoting
expanded before believing the count. Third member of this family and the first where the
instrument was the *shell* rather than the pager.

⚠ **Console encoding is the other one.** This rig's console is **cp1252**: printing `→`
(U+2192) from a Python script raises `UnicodeEncodeError` and kills the script *after* its
writes have landed. It happened twice in one session, both times in a count-reconciliation
script, leaving the tree half-edited and the verification line unprinted. **Keep tool output
ASCII** — the kickoff already says so, and this is why — and make any repair script
**idempotent**, because the run that dies mid-sweep is the one you have to re-run.

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

**Blender's own MCP server is a REFERENCE, never a pipeline stage** (Director, 2026-08-09:
*"use it as a reference if you're ever stumped… but it doesn't belong in the pipeline"*).
Blender Lab ships one (5.1+; we run 5.2) that attaches an add-on to a **live GUI session**
and gives an LLM natural-language access to that session's Python API — good at *what is
in this scene*: poly-count outliers, bad normals, non-uniform transforms, what a node
setup does. Reach for it when a mesh question has you stuck.

**It may not touch the route, and the reasons are measured.** Every Blender call here is
`blender -b -P <script>.py -- <args>` — **12 `-b` invocations, zero GUI sessions** — because
a recipe that does not reproduce its output is not a recipe, and an LLM improvising `bpy`
against a session produces artifacts with no recorded parameters. And its own page states
it *"will execute LLM generated code in Blender without any guards… recommended to use a
virtual machine, or a system without access to sensitive information."* **This rig holds
`E:\AI\training`** — not in git, no revert, the trees three consecutive rulings had
executors sha256-manifest 7,312 files to protect. If you use it, use it on a scratch copy
of one mesh, and bring back a hypothesis rather than a number: **a number that decides
anything comes from a recorded script**, because here the provenance of a measurement is
the product.

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
  not solid**: TRELLIS.2 `1024_cascade` reconstructions on this route are hollow double-walled
  shells — walls ~two voxels around an empty cavity, measured three independent ways (E14
  Ruling 3). ⚠ **That finding's evidence base is three longswords, a dragon and a galleon —
  prop, beast and vehicle. NO CHARACTER**, and the character is the route's founding class;
  E14 Ruling 3's own words quantify over "every reconstruction this route has made", which is
  wider than what it measured (E29 Ruling 4, read verbatim at the ruling seat). **On the
  character class the wall structure is UNMEASURED, and that is not a claim of solidity** —
  `mesh_topology`'s nested-wall leg *declines to compute* on all five character meshes tested,
  including two recorded ones, because it needs a second manifold piece above 1% of faces and
  the largest runs 98.2–98.6%. An inner wall shredded into sub-1% pieces produces exactly that
  signature **while still being hollow**. Answering it needs the other two methods
  (ray-crossing, cross-section clustering), neither of which is on the served surface.
  Meanwhile the constraint stands unchanged for every consumer: the figure's interior reads
  *outside* by parity, a volumetric consumer must address the outer wall specifically, and the
  route never meets the inner wall — invisible surface, culled by construction.

- **A single-run mesh comparison has no noise floor. Measure the floor before reading a
  difference.** Three reconstructions of one input at one seed are **bit-identical through
  `pipe.run()`, hole-filling and remeshing** — to the digit — and then diverge inside
  `to_glb`'s decimation: faces ±2,618 (**0.27%**), shells **±1**, non-manifold edges **±18**
  (E29 Ruling 5). The studio's standing *"TRELLIS is DETERMINISTIC"* is half right, and the
  wrong half is the half a mesh comparison lands in. **Nothing in this record carried such a
  floor, so every prior single-run mesh comparison here has an unmeasured one** — which does
  not overturn any of them, and does mean re-litigating one requires measuring its floor
  rather than asserting it was small. E29's own gaps run 13.7×–152× the floor, which is a
  property of that arc and not a licence.
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
