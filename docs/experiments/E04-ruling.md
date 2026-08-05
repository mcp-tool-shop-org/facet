# E04 — the ruling document

Advisor rulings for the E04 arc, in the E08 pattern: rulings appended in place with dates
and reasons, corrections in place with the measurement that overturned them. The closed E08
record is [E08-ruling-gate0.md](E08-ruling-gate0.md); the dispatch is
[E04-executor-kickoff.md](E04-executor-kickoff.md).

---

## Ruling 1 (advisor, 2026-08-04) — the crown is an OWNER SEAM. A new defect class is named, and my prior is falsified the right way.

**Ratified in full.** The Director's blotch is a **stage-1 inter-camera ownership seam**:
`argmax(facing)` hands the crown half to the yaw-090 twin and half to the yaw-135 twin, and
**the two sources disagree about the scalp by ΔE 17.97** on surface both see above the
pipeline's own facing floor (per-texel median 17.56, p90 32.00) — of which 10.3–13.8
survives into the atlas as a hard edge. Claim-only boundaries explain **0.0–1.3%** of the
head's strong steps on every camera; owner-only explain 43.5–77.8%; the null control
collapses on the region (100% → 4.7%). The alternates are measured and dismissed on their
own numbers: chart fragmentation at 1.67–3.00 against the seam's 15.75–19.33, dilation the
flattest class present — and **0.0% dilation in the region at all**.

### Why this class is dangerous, and why nothing caught it

Two structural properties. **It is provenance-blind by construction** — both sides of the
edge are class TWINS, so the instrument that decided E07 cannot see it. And **it lives on
the best surface, not the worst**: the crown is 89.2% stage-1 covered against 59.8% outside
the head band, precisely because `--head-facing-min 0.18` exists to keep the head off the
brush. This is not a shortage of paint; it is a disagreement between two *good* sources.
The defect is **multi-view tone inconsistency between independently generated twins**,
surfacing wherever ownership switches — an argmax over sources that were never harmonised.

**It is subject-independent and it is going to the galleon.** Every value involved is
code-level, not profile-level, and a ship is mostly large smooth surfaces — hull planking
under eight independently toned twins will carry owner seams wherever neighbours disagree.
E04's Gate 1 should *expect* them; this arm may earn its priority there rather than on the
accepted warrior.

### The prior — falsified properly, and ledger nineteen

Amendment 35 stated the prior as a prior, named alternates, and the check was built not to
assume its answer — **this is the falsification working as designed**, the contrast to
Amendment 32's "known object." What goes in the ledger is *how* the prior was built:
**it contradicted a flag whose entire purpose was to prevent the situation I described.**
I claimed the crown was where "grazing stage-1 paint, both elevated strokes, and dilation
meet" — while `--head-facing-min 0.18` against the body's 0.45 exists precisely so the head
band does not go to the brush. An unread flag, again in a file I had open for other reasons.
And the guess propagated: three of the executor's nine predictions inherited it and fell
together. **Standing correction: a dispatch prior carries its evidence status — *measured*,
*inferred from the record*, or *unread guess* — because an unlabeled prior travels as fact
and bends the predictions built downstream of it.**

The prior's defect is real on this asset — `TWINS|BRUSH` seams measure 12.6–31.4,
concentrated at the elevated cameras. Right defect, wrong region.

### Rulings that follow

1. **The owner-seam arm is specified as its own polish arm**, distinct from the stroke-seam
   levelling arm, and it inherits the Director's named region. Targeting data: source
   disagreement ΔE 17.97 / median 17.56, atlas step 10.3–13.8 across the y090|y135 line;
   the fair-set machinery in `e04_seam_sources.py` is the calibration instrument a
   harmonisation fix would be measured with. **Its first question is why stage 1's σ=16
   levelling did not touch a ΔE 13 step** — scale, or boundary class it never applied to.
   Candidate fixes, one pre-convicted: naive cross-view averaging is **ghosting**
   (`bake_multiview_glb`'s conviction stands); the live candidates are pre-projection tone
   harmonisation between twins over co-visible surface, and cross-owner levelling at a
   scale matched to the step. If research grounding is commissioned for the multi-view
   consistency question, **RG01's citation gate re-runs through Crossref first** — its
   findings are currently unverified.
2. **`project_twins` saves what it computes.** The ownership map and the facing-weighted
   blend both exist at projection time and are discarded; the executor had to reconstruct
   one and could not obtain the other, which is exactly the "shading vs content" split the
   report marks as not established. Owner-map and blend sidecars become standing outputs —
   folded into Task 2's refactor touch, with the byte-identity gates still binding on the
   existing outputs (additive sidecars move no atlas byte).
3. **The polish queue, restated with the named region reassigned:** dilation flood (27.0%
   of valid — still the largest class) · **owner seams** (the Director's named region;
   will recur on E04) · stroke-seam levelling (12.6–31.4, elevated cameras) · blade band ·
   A3's cap. All post-Gate-1 polish; **the galleon runs first, per the Director.**
4. **The watchdog died hard twice today.** Before Task 3's TRELLIS reconstructions, read
   `_watchdog_KILL.log` / the DEAD sentinel's reason and report it — a protection process
   that keeps dying hard is itself a defect, and Task 3 is the first GPU work since.
5. **Tasks 2 and 3 are CLEARED to proceed** as dispatched.

### Endorsed by name

Predictions hashed before any artifact was opened — twice, the source test separately
before it ran. The claim map built with no replay and asserted against four recorded counts
plus two checks it did not need to pass. S1 falsified by its own operand, corrected with an
**inherited** floor rather than a chosen one, and still reported falsified rather than
softened. The null control published with the one place it does not collapse cleanly. The
`--head-facing-min` claim verified before commit — *"that is the exact error I am
reporting"* — and the 0.003% numeric coincidence flagged so nobody builds on it. Six of
nine predictions wrong, every one reported with its reason. **That is what a falsified
prior is supposed to look like from the inside.**

---

## Ruling 2 (advisor, 2026-08-04) — Tasks 2 and 3 ratified. The profile-purity check is standing, the prompt finding is the headline, and the watchdog gap leaves this repo.

**Both tasks are ratified.** Three byte-identity anchors at zero differing pixels — including
an 8-camera invocation that had never been written down, reconstructed and verified against
the banked atlas *before* any profile existed, which is the anchor-first discipline applied
without being asked. 115 constants classified with none unplaced. Three galleons
reconstructed at seed 42, measured identically, sheeted at full size, and the halt is at the
designation gate where it belongs.

### Ledger twenty — my gate was narrow, and the executor's near-miss walked through it

The byte-identity gate I specified exercised **three tools of eleven**. The executor's
`cull_unseen` error — writing the character's ten cameras over a deliberately denser 24-yaw
safety superset — would have narrowed a margin into a subject list, **and my gate could not
have fired**, because nothing in the dispatch re-runs that tool. Caught by reading, then
made mechanical: `e04_profile_check.py` compares every profile value against its flag's
source default across all tools at once. **Adopted as the standing profile-purity gate.**
Byte-identity proves the anchored path did not move; the source-default comparison proves
the *unanchored* paths did not either. Two gates, two failure modes, keep both.

### The finding that justifies the whole extraction

`restylize_views` and `texpass_brush` both defaulted `--prompt` to **this character's
literal identity string** — in the repo whose central measured result is that identity
belongs to the prompt. Harmless on the accepted route, which passes prompts from a file;
**not harmless for a galleon run without `--prompts`**, which would have asked the cloud
for a burly bald warrior with a long red beard. The exact accident class the architecture
exists to kill, sitting in shared tools as a default, found by the discipline built to find
it. Relocated same-value, so purity holds.

Also ratified: the owner-map sidecar paying on its first day — Task 1's ownership
reconstruction corrected in place by **one texel of 2,402,810** (a float64 tie that the
tool's float32 comparison keeps with the earlier view). A correction that small, made that
precisely, is the record working.

### The watchdog finding is a real protection gap, and it is not facet's to fix

**153 breach detections in five minutes, VRAM pinned at 31,851–31,903 MiB, zero kills** —
the kill list is an allow-list of four interpreters, the holder wasn't on it, and the log
never records *what* held the memory. Until that is fixed, the watchdog protects against
exactly four processes and is blind spectacle against everything else (ollama's
`llama-server` runs on this rig and is not listed). Spawned as its own task outside this
repo: log per-process VRAM at every breach so the next burst names its culprit, and
escalate loudly when an abort kills nothing. The allow-list's membership is the Director's
design call, not mine — the task proposes options, the logging is unconditional.

Recorded, not actioned mid-arc: `trellis2` reaches `sys.path` through a **retired repo's
checkout** — a proper install into `trellis2-env` is a rig chore for a quiet moment, and
the runner carries the `PYTHONPATH` with the reason meanwhile. And the backend record —
`flash_attn` loaded where `sdpa` was requested — is endorsed as written: **what ran is what
the log says**, and E02's recorded `sdpa` must not be read onto any of today's meshes.

### The designation, cleared to the Director

Three sheets go to him at full size with the measured differences beside them and **no
ranking**: shells 237 / 274 / 512 (rigging returns as disconnected filaments; a downstream
welding question, not a quality score), largest shell 88.0–92.9%, all three wider than tall
(1.041–1.114 — the first measured support for `fit_axis: width`), and no shared bow
orientation, so "front" is declared per candidate at designation. **Rejecting all three is
a legitimate outcome** — the clays are cheap to re-concept, and a designation is not a
settlement for whatever arrived. After his pick: the advisor authors the galleon's identity
fixture and palette bands, and `ship.json`'s suspended values get measured from the
designated mesh.

---

## Ruling 3 (advisor, 2026-08-04) — DESIGNATED: candidate 00006. The fixture is authored.

**The Director designated 00006** at the Gate 0 sheets ("they look great" — pick made on the
full-size sheets, all three judged good). Recorded: 00006 carries the most rigging filaments
(512 shells) and the squarest profile (1.041) of the three — his eye weighed that against
the sheets and chose it; neither number ranked anything.

**[canon/GALLEON-IDENTITY.md](../../canon/GALLEON-IDENTITY.md) is authored** — twelve NAMED
elements in the measured grammar (own noun phrases, no additions onto occupied surfaces),
MESH-SUPPLIED and STYLE-SUPPLIED tables, and three pre-registered stressors: **S1**, canvas
is the blade problem at sail scale (G4 authored warm-tan in canon partly for that reason —
an authoring choice, not a tuned threshold); **S2**, the rigging is the thin-policy
stressor; **S3**, nobody knows a galleon's palette by eye, so the gate carries the judgment
and its numeric bands derive from the fixture's materials, cross-checked against the styled
target pair once it exists — never against the twins they will gate. Deliberate and worth
noticing: **blue is in-palette on this subject** — W3's off-palette detector colour is a
declared material here, which is palette-as-subject-data made concrete.

Unlike W3's, this spec is authored **forward** — the styled target pair will be generated
from it. The fixture is the Director's to overrule in a sentence, line by line.

**Next dispatch:** measure `ship.json`'s suspended values from the designated mesh (framing,
cameras — decks need looking *into* — thin-extent, the declared "front"), generate the
styled target pair from the fixture, derive the palette bands, then the E04 spec proper.

---

## Ruling 4 (advisor, 2026-08-04) — S1's physics was mine and it was inverted. Canon corrected in place; the backdrop becomes a declared lever.

**The fixture check is ratified and the move itself is the precedent:** checking a canon
claim against artifacts already on disk *before* a dispatch inherits it is the
inherited-claim rule applied upstream, and it cost nothing. **Ledger twenty-one:** I wrote
a mechanism into canon unchecked while the checking artifact sat on disk — and the error's
form is precise: I conflated **two instruments' failure physics**. The palette gate fails
at low *chroma* (hue undefined); the key fails at small *value-distance from the backdrop*.
Steel happened to be both, and I generalised from the wrong one: against a mid-grey
backdrop, white is the *safest* value (0.5343, 8.9× the cut) and "pale canvas is the same
physics" was backwards. Corrected in the fixture with the measurement; **G4 stays tan** on
its surviving grounds — the executor's line is the standard: *a choice with one wrong
reason and three good ones is still the choice.*

**The real S1-class exposure is G9**, measured: thin structure keys out 4.2–6.8× more than
bulk regardless of its named colour, because a 1–2 px line antialiases toward the backdrop.
S1 and S2 merge into one failure whose element is the rigging — a strengthening of the
fixture pointing at a different element.

**The backdrop is promoted to declared fixture data** (S-backdrop): it is prompted, one
word, and it is the only free operand in the key. The dispatch derives it — maximise the
minimum distance from every declared material, weighted toward the dark thin elements —
and records the derivation. Noted explicitly: this does **not** reopen E08's parked
blue-background arm, which changed the *clay render's* compositing and broke the control
chain; this chooses what the *diffusion model paints* behind a fresh subject, which is
subject data the galleon gets to set from birth. And the backdrop must avoid **G11's
declared blue** — the collision the old grey default never had to think about.

**G11's cost is accepted as costed:** admitting blue takes the forbidden hue span from
170° to ~120°, and G6/G11 are hue-adjacent. The dispatch derives both bands tightly and
**reports whether they merge** — the gate's power on this subject becomes a measured
quantity either way, which is better than an assumed one.

---

## Ruling 5 (advisor, 2026-08-04) — 4a/4b ratified. The backdrop is WHITE, the fit-axis finding is the profile design working, and 4c is cleared with three pins.

**Ratified in full**, and the method wins are named: the union rescoring (single-elevation
scores answered a question nobody asked — the executor corrected its own operand before the
numbers meant anything); the shell-topology criterion **falsified and reported as the full
success it is** (the rigging lives in the main shell, attached to its masts); the antimode
refused on the density plot (a 7% dip is a shoulder, not a cut — the E08 A4 rule holding on
a new subject); and thin 0.010 adopted as **a judged trade with its cost curve published**,
which is exactly how the character's own value was born. Three of five backdrop predictions
falsified with one owned cause — *reasoned about the metric instead of the materials* — and
for the record, the thin-weighting clause the derivation ignored was mine, and the
measurement showed it moot.

**The backdrop is `plain white`** — 2.5× the blade-killing quantity, with the unconstrained
optimum (saturated blue) disqualified twice for reasons that were in the fixture before the
derivation ran. Bank the caveat with it: the material colours are **estimates from the
fixture's words**, so 4d re-runs the derivation against colours measured from the pair —
and the loop is bounded now, before it exists: if the re-derivation dethrones white, that
implicates the pair's own backdrop, so the pair re-generates once on the new answer and a
second dethroning is a halt, not an iteration.

**The `turn_render` finding is the profile design earning its keep** — `ortho_scale =
size.z * 1.204` has no fit-axis knob, so width-fit *cannot be a profile value*, which per
`profiles-design.md` means the height-fit was never a principle; it was W3's portrait
assumption compiled into shared code. Recorded, not fixed, correctly: **the fix is deferred
to the E04 spec proper as a named work item** — a fit-axis flag defaulting to the old
behaviour, landed with byte-identity anchors on the character path, same shape as
`--trust-intersect`. 4c does not wait for it: the Gate 0 driver already measures per-mesh
frames.

**Two expectation-setting numbers, banked before anyone is surprised by them.** Deck
coverage plateaus near **53% at twelve cameras** — half this subject is unreachable from
outside, so the ship's reference share will run structurally lower than the character's
74.1% reach, with dilation and brush carrying more. That is geometry, not a pipeline
regression, and the Gate 1 read must not treat it as one. And **bow/stern elevation beats
beam** (49.58% vs 41.93%) — a subject-specific fact nothing in the character line
predicted; 40° adopted as the measured peak over the inherited 55. Consequence flagged for
the E04 spec: **`cull_unseen`'s production superset must be a superset of the ship's
cameras** — the 24-yaw set predates elevated ±40 pairs, and E06's rule is that the
visibility set covers every production camera, always.

**A new instrument limitation, named:** `thin_extent` measures extent **along the view
ray**, so a grazing hull rim and an edge-on sail register as thin — a conflation a
greatsword never triggered, and the reason the character's 0.030 is visibly wrong here.
Lives in `ship.json` beside the value; the structural-thickness replacement is an arm for
another day, not a patch for this one.

**4c is CLEARED with three pins:** (1) the pair is **canny-locked to the designated mesh's
own renders** — the W3 canon-pair precedent; build the control from the Gate 0 driver's
measured frames and the exact-silhouette machinery, never a keyed render; (2) the backdrop
word is white per 4b; (3) the sidecar declares at birth: *specification source and visual
target, never a projection reference.* Recipe discipline as dispatched — JSON before
submission, `dry_run`, `estimate_credits`, the live LoRA card name, one re-roll bound.

---

## Ruling 6 (advisor, 2026-08-04) — 4c ratified with its deviation; the pin was mine and the frame convention had a second consumer

**Ratified, deviation included.** My pin said the Gate 0 driver's 1072×1024 frames; the
executor measured that `silhouette_masks` derives `h_ext` from `v_ext = bbox_z × 1.204`
while `turn_render` maps that scale to the **larger** axis — on any landscape frame the two
disagree by construction (here exactly 1.2097/1.1556 = 4.68%, IoU 0.75), and a control
built from them canny-locks the model to a silhouette 4.7% off its own render. Generating
at **1024×1024**, where the conventions coincide (agreement 0.24%), was an input-side call
correctly decided without escalation. **Ledger twenty-two:** I pinned a frame without
tracing the mask tool's convention — the one-variable rule's dependency-graph clause,
violated in a pin. Consequence folded into the spec's work item: **the fit-axis fix moves
`turn_render` and `silhouette_masks` together** or every landscape subject silently
misregisters — the deferred finding has two consumers, and the executor found the second
one before it cost anything.

**Banked: the prompt only partly controls the backdrop.** Asked white, realised
rgb(175,175,175) — the lever moved the backdrop from W3's ~114 to ~175 of an asked 255,
and the key margin improved (1.48% at/under the cut against W3's 1.77–2.45%) but less than
the derivation predicted, **because the derivation assumed asked = realised.** 4d
re-derives against the **realised** backdrop and **measured** material colours; Ruling 5's
loop bound applies with realised values. Asked-vs-realised is now a named gap every future
backdrop argument must state which side of it lives on.

**G6 did not land, and the classification is exactly right:** the spire reads gold —
in-spec material in the wrong place, an *element that did not land*, not off-palette; no
re-roll under the stated rule. This is the fixture's founding question answered with its
first ship datum, and it goes to 4d as measurement: **the twelve-element landing table**,
W3-style, against the pair. Whether G6 is strengthened, contradiction-tested, or amended
to gold is decided after the table exists — and the canon call is the Director's overrule
window, which is open now that the pair is in front of him. Default absent his word: G6
stays verdigris as authored, and the E04 spec treats the miss as a measured fact.

**4d is CLEARED:** the landing table · bands from the fixture's materials cross-checked
against the pair's measured colours · the backdrop re-derivation on realised values · the
G6/G11 merge question · *suspend rather than invent* standing wherever the data is thin.

---

## Ruling 7 (advisor, 2026-08-04) — the Director approves the pair; G6 amends to gold; the overrule window closes

**"I love the gold. I approve."** The styled target pair is **ratified as the ship's canon
target** — frozen, versioned, specification source and visual target, never a projection
reference, exactly as its sidecar declared at birth. **G6 amends in place** from verdigris
copper to a gilded spire, joining the gold family.

**The distinction that keeps this honest, stated so it cannot become a laundering
precedent:** this is not a spec tuned until it passes. The measured fact is preserved —
verdigris was asked, gold arrived, and the landing table records that history — and the
amendment was made by the **canon's owner looking at the artifact**, which is his gate and
nobody else's. A spec author softening a miss is forbidden; a Director ruling that the
arrived material is the ship he wants is the system's whole point. The W3 precedent is N6:
a term that misnames what canon actually wants gets struck by the owner, on sight.

**Consequences for 4d, all simplifying:** the G6/G11 merge question is **mooted** —
verdigris leaves the palette, sea-blue stands alone, and the forbidden hue span *recovers*
most of what G11 spent, which strengthens the gate on exactly the subject where it carries
the judgment. The landing table now scores the amended G6 (gilded spire: **landed**) while
recording the original ask as the measured history. The backdrop re-derivation loses one
mid-green material and should barely move.

4d proceeds. After it: the E04 spec proper, from the advisor, with every number in hand.

---

## Ruling 8 (advisor, 2026-08-04) — Task 4 closes. The gate is stronger than costed, the backdrop decision moves to the spec on the operative number, and G7 sits in the open window.

**4d ratified, and the clustering method with it** — a cluster table measures what is
there and can return *"nothing like this is present,"* which a hand-placed disc never can;
it earned that property immediately by finding no red anywhere on the ship. The stated
limit is carried honestly: LANDED means the colour is present, not placed — the gate's
known blind spot governs the table that feeds it.

**The bands: ratified as measured, and both prior costings die.** Twelve names collapse to
two hue groups, and the ship's forbidden span is **288° (80.0%) against W3's 170°
(47.2%)** — the gate is *stronger* on the subject where it carries the judgment, reversing
the executor's Task-1 warning and my Ruling 4 acceptance of it in one measurement. The
Director's gold amendment did half of that work. **The blue band stays suspended** on its
3.69% denominator with the ±10° margin named as convention — suspend rather than invent,
correctly applied.

**G7 red-lined gun port lids: the window is open.** No red exists on the ship above the
chroma floor — an element that did not land, G6's class exactly, no re-roll. **Default
absent the Director's word: G7 stays red as authored**, and the E04 spec gains what is
actually a valuable thing — a known-miss element to test landing mechanisms against
(stronger phrasing, ordering, or the contradiction protocol). His one-sentence overrule to
brown-as-arrived stands open, per the G6 precedent.

**The backdrop: the regression is in the metric, and the decision moves to the spec on the
operative number.** Two facts that pull apart: the min-distance metric says the realised
backdrop (173) is *worse* than W3's grey (0.1000 vs 0.1451) — driven by a near-neutral
pale cluster (rgb 198,195,192 · 4.62% · C\* 2.2, below the chroma floor and thus invisible
to the palette gate) that no derivation anticipated. But the **operative** quantity — the
fraction of silhouette pixels at or under the key cut — measured **1.48% on the pair
against the accepted character's 1.77–2.45%.** The repo's rule is to gate on the failure
itself, not a proxy for it, and min-distance is the proxy here. **Ruling 5's regeneration
clause is overtaken:** the pair is Director-ratified canon (Ruling 7) and a derivation
metric does not outrank his eye — the pair stands, and its realised backdrop is now simply
*data* for the twins' backdrop decision. **The spec's default, stated now so it is not
chosen while looking at twin results: the twins' backdrop word stays `plain white`** — its
ask→realise transfer is the only one measured (255→173), and its operative margin beats
the accepted baseline. Chasing the metric optimum through an unmeasured transfer function
would trade a measured 1.48% for an unknown; the spec may overrule this default only with
a measurement, not a derivation. The pale cluster is banked as a named watch item: below
the chroma floor, ungated by palette, tightest key margin on the asset — the E04 twins'
keying reports it per view.

**Task 4 is closed.** Next: the E04 spec proper, from the advisor — the fit-axis work item
(`turn_render` + `silhouette_masks` together, character anchors byte-identical), the cull
superset grown to the ship's cameras, the route staged on the measured profile, the
landing-test design for G7, and the gates this arc has earned, derived per subject.

---

## Ruling 9 (advisor, 2026-08-04) — G7 stays red, the executor's reasoning is ratified, and ledger twenty-three is mine

**Ratified as decided under the Director's delegation.** The executor's table is the
finding: G7 is the **only** element of twelve whose colour term modifies a *sub-feature*
("red-**lined**" lids) rather than occupying its head noun — and the only element that
missed. That is not a new hypothesis; it is the **second instance of the documented
occupancy mechanism** (the W3 gold-plate-on-fur-cuff no-response, ΔE 1.07 in two
grammatical forms), and the first on a non-character subject.

**Ledger twenty-three:** the fixture's own Form section — which I wrote — predicts that
additions onto occupied surfaces drop, and **G7 was already an addition when I authored it
one table below that sentence.** The executor built the prompt from it without catching it
either; the landing table caught us both. A rule quoted in a header does not check the
table under it; only an instrument does.

**The spec inherits the test as designed:** restate G7 as `red gun port lids` — one word
removed — under the W3 contradiction methodology: byte-matched control, same seed, one
generation, the lid clusters measured before and after. Lands → the occupancy mechanism is
confirmed on a second subject. Misses → the cause is size, occlusion, or the LoRA's warm
register, which is also worth knowing. *Amending to brown would have traded a free
experiment for a tidier document* — the executor's sentence, kept.

---

## Ruling 10 (advisor, 2026-08-04) — the ≤0.24% anchor bound is WITHDRAWN, and the replacement is geometry against geometry at bound zero

**The bound is withdrawn, not retuned — and it was never a threshold.** Its derivation was
a single reading of a keyed-clay bbox statistic at threshold 26, adopted with no noise
floor ever characterised — **and its operand is a technique this repo retired**:
`silhouette_masks`' own docstring says the mask cannot be thresholded off the clay render,
which is E01's founding lesson and the reason A2 exists. The anchor was measuring its own
instrument's antialiasing fringe. **Ledger twenty-four:** I wrote a keyed-clay bound into
a spec, in the repo that retired keyed clay, one arc after quoting that retirement. Fourth
member of the mis-derived-bound family (E07's ratio, the percentage bound, A32's
byte-equality premise, this).

**The replacement the executor proposed and correctly declined to build is now specified:**
compare `silhouette_masks`' raycast against a raycast built under `turn_render`'s camera
parameters — **geometry against geometry, same mesh, same frame, bound 0 px.** Why
specifying it now is not retuning by another route, stated against the test that decides:
the check derives from standing law (*geometry answers "is there surface"; keying never
does*), not from the fired number — it would be the same check whatever 1c had read; its
bound is **stricter** than the withdrawn one, not looser; and **its outcome is unknown** —
it can fail, and nobody has run it. The 70-threshold was refused precisely because its
passing was already known; this check's passing is not. The keyed-bbox comparison was
always a proxy for the real property — **camera-convention identity** — and the
replacement tests the property. Pre-stated readings: **0 px → anchor passes.** A handful
of boundary pixels in uniform scatter → float edge-ordering at the silhouette; report the
count and halt for a ruling, do not tune. A structural offset → the gate's real prey;
halt. For scale, the failure class it exists to catch measured 4.68%.

**The hash lesson goes to CLAUDE.md** — twice bitten is a rule: a PNG hash mismatch is not
evidence a render changed; file bytes are not pixel values. The executor's false alarm was
caught before it reached a conclusion and owned in the report, which is the difference
between an error and a defect.

**Step 0 resumes:** anchor 1c re-runs on the geometry check; items 2–4 and the arms are
unchanged. Nothing else in the spec moves.

---

## Ruling 11 (advisor, 2026-08-04) — anchor 1c: ADJUDICATED PASS under the pre-registered float reading. The bound does not move.

**The 1 px is Ruling 10's second reading, decided by the numbers:** centroid shift
(−0.0004, −0.0009) px where a structural offset must move it; bboxes identical on both
axes; the other ship view at 0; and — the load-bearing part, as the executor named it —
**the character control at exactly 0 on both views**, which proves the instrument can
return 0 and makes 1 px a real, tiny disagreement rather than tolerance slop. One pixel of
321,219 with an unmoved centroid is a ray resolving a triangle-edge coincidence
differently under two float orderings. The prey this anchor hunts measured 4.68% with a
34×42 px bbox gap; this is 0.0003% with no gap at all.

**The mechanics of the pass, stated so it cannot become a tolerance:** the bound stays
**0**. This *instance* is adjudicated on its evidence; the next nonzero halts again and
gets its own ruling. That is what the halt-for-ruling branch is for — the gate keeps its
authority precisely because no number moved.

**The pixel-chase is declined**, with the executor's own reason adopted: locating the
triangle would be work aimed at making a fired gate go away, and the gate's question —
convention identity — is discharged. And the refusal to adopt a bound of 1 *because its
passing was already known* is the second application of the retune test to oneself in two
rulings; it is the standard now.

Recorded with approval: the fit-axis change closes with the cleanest anchor set of the
arc — the character path at **zero differing pixels on renders, masks, and geometry**.

**Step 0 items 2–4 are cleared. Then Arm G7, then Arm T, per the spec.** The next
scheduled meeting point is the spec's own twin-baseline halt — measure, report, ruling
before projection — or any fired gate before it.

---

## Ruling 12 (advisor, 2026-08-04) — Step 0 complete and ratified. Two spec corrections, one of them mine.

**All four items pass and are ratified**: fit-axis at zero differing pixels on the
character path across renders, masks and geometry (ship adjudicated at Ruling 11); the
cull superset; emit framing byte-identical with the profile loaded; PURE RELOCATION at 64
values across 11 tools.

**Item 2: my spec's anchor premise was false — ledger twenty-five.** I wrote *"its cameras
were already covered"* without enumerating the default: the 24-yaw + dual-55 sweep does
**not** contain the ship's 0/180 @ 40, so the assumption would have walked the run into
the exact E06 violation the item existed to prevent. The executor's shape is ratified as
the standing pattern: **the subject supplies its own superset — the full code default plus
its cameras, never a narrowing** — which keeps its own Task 2 law (a subject list never
replaces a safety superset) and makes the character's cull unchanged *by construction*,
which is stronger than re-measured. Enumerate before asserting coverage; a spec line is
not exempt.

**Item 3: the third hardcoded frame** — `texpass_iter`'s 752×1024, one subject's portrait
framing in a shared tool, the class the profile exercise exists to flush and has now
flushed three times. Three fit-axis blocks cross-naming each other is the repo's accepted
pattern (the levelling blocks do the same); consolidation is a post-arc tidy, not a
mid-arc churn.

**The context-boundary stop is endorsed by name**: a generation run you cannot see through
is worse than a clean halt at a passed anchor set. Arms G7 and T go to a fresh session;
the handoff is in the kickoff.

---

## Ruling 13 (advisor, 2026-08-04) — Arm G7 ratified with its floor WITHDRAWN; Arm T unblocked on all three questions; two of the three blockers were mine

### Arm G7 — the third outcome is the finding, and the pass reading is withdrawn

**The report is ratified in full** — the byte-match proven by content-addressed filenames
rather than asserted, the two-field diff enumerated over every node input, the mis-specified
secondary window reported as mis-specified with its own hue breakdown as the correction, and
the disagreement between the two readings promoted to the headline. That is the standard.

**The pre-registered pass reading is WITHDRAWN, not failed-and-excused — and the difference
is load-bearing.** The branch I wrote asked red to clear "the pair's measured element floor"
(1.42–1.56% of silhouette — the smallest share carrying a LANDED element). The lids' entire
physical extent is ~0.4–0.5% of the silhouette: at a **perfect** landing the measurement
cannot exceed ~0.5% and the reading returns FAIL. A condition that returns the same verdict
when the arm does nothing and when it works perfectly is not measuring the arm — CLAUDE.md's
works-perfectly test, which I did not run before writing the branch. **Ledger twenty-seven**,
the mis-derived-bound family's fifth member. The floor stays in the landing table as the
descriptive statistic it is; it stops being a pass condition for any element whose extent
sits at or under it. No replacement bar is chosen — that would be retuning with the result
on the table.

**What the measurements establish, read without the withdrawn bar:** a real, element-local
response — three-to-four lid components at ΔE 16.5–27.3 with hue rotating 66–70 → 41–45 and
chroma *rising*, against a whole-ship median of 0.87, itself below the 1.07 no-response
floor; and 352 → 1,169 px (3.3×) below hue 40° on a window fixed before the run — the
non-circular number. Where `red-lined` produced nothing anywhere (4d measured no red above
the chroma floor), `red gun port lids` put paint on exactly the named structures at a
byte-matched control. **What they do not establish: a landing.** The nearest cluster stops
at ΔE 28.3 from canonical red and the arrived hue sits outside every band. P1 and P3 are
FALSE as pre-registered; the mechanism inference survives only in the weakened form the
report's §9 states — *response, not landing*, size now the leading alternate. **G7's landing
verdict moves to the twins' landing table**: lid clusters and the fixed sub-40° window
reported per view, numerator and denominator, no bound — the same measure-report-rule mode
as every first-run gate on this subject.

One correction to the report's prose, so the record carries the ratio: 0.37–0.44% against a
1.42–1.56% floor is **3.2–4.2×** under it, not "an order of magnitude." The report's own
tables carry the right numbers; the headline sentence rounds up.

Banked from the run: **a cloud `dry_run` PASS does not prove link sanity** — a
self-referencing node link returned `status: validated`; submit saved workflow files
verbatim and check topology in code (added to CLAUDE.md's environment section).

**The fixture amends G7 to the head-noun form** — `red gun port lids` — under Ruling 9's
grammar, which ruled the restatement correct *regardless* before this arm ran. The twins
take it, the prompt file already carries it, and the fixture must match the prompt: the
identity source and its transcription cannot be allowed to diverge. The COLOUR question —
red as authored, the arrived h 41–45, or neither — is the Director's window, per the G6
precedent; default absent his word is red as authored. The palette file's G7-has-no-band
entry stands exactly as written: deriving a band from the arm's own result is the tautology
the non-circularity rule forbids.

### The three questions

**1. EIGHT — the spec line was mine, and H2 stands.** Verified against source before ruling:
`turn_render` fixes its camera at `mid.z` (:155–158), `silhouette_masks` and `project_twins`
hardcode the ray z to 0 (:120, :316), E08's eight stage-1 cameras are all-yaw (the eightcam
table), and elevation enters the route at `texpass_iter emit --el` — the brush. The accepted
route's stage 1 is eye-level **by construction**; the elevated pair is Task 4a deck-coverage
data whose consumers are the cull superset (Step 0 item 2, done) and the stroke-camera
derivation the spec's own strokes bullet already specifies. My Arm T line assigned it to a
stage that never had it — **ledger twenty-six**, the same family as twenty-five: enumerate
before asserting; a spec line is not exempt. The spec is corrected in place (its Amendment
1); a spec transcription error cannot falsify H2, which remains live and is tested by what
remains. **The elevated-twin capability is recorded as a named possible arm** — Step-0-class,
three tools, character byte-identity anchors, would raise stage 1's deck ceiling above the
eye-level eight's 30.17% of upward-facing area — and is NOT opened; whether deck reference
is bought at stage 1 or stage 2 is a question for after the baseline exists, and it is the
Director's if it is anyone's. **H4's reach ceiling is computed on the eight eye-level
cameras** and pre-registered before projection, per the spec.

**2. STRUCK.** The `restylize_views` block loses its `aspect` key — the value never reached
anything (zero frame references in the tool; the frame arrives through its inputs), and the
loader's unknown-key ANDON fired exactly as designed. The block keeps its backdrop
annotation and gains the strike note. **The executor's fourth question is answered YES and
is standing law: `e04_profile_check.py` runs against EVERY profile before any arm consumes
it** — for the character it proves pure relocation; for any other subject it proves every
value reaches its tool, the same instrument answering a second question for free. **Ledger
twenty-eight:** Ruling 12 ratified "PURE RELOCATION at 64 values" on a run I never pointed
at the ship profile, and the dead key sat in `ship.json` from Task 4a until a tool loaded
it — same class as ledger twenty: the gate existed and its scope was narrow. Pre-ruled so no
halt round-trip is needed: until the checker learns two verdicts, its VALUE-DIFFERS rows on
a non-character profile are the profile *working* — a ship differing from character defaults
is the point; only a NO-SUCH-FLAG row is a defect. Teaching the checker that distinction
(two verdict classes, exit codes to match, and the `cull_unseen` evaluability limit) is a
queued diagnostic work item, not a route-tool change.

**3. ADDED.** `fit-axis: width` lands on `turn_render` AND `silhouette_masks` in
`ship.json` — the two consumers move together, Ruling 6's lesson expressed as one profile
value per tool — with **no margin entry**: the adjudicated run used the code default 1.204,
and the "derived margin 1.2528" in the suspended note was never used by any ruled run. The
stale `_still_suspended` framing note is corrected in place with the measurement. The
executor's width column reproducing Ruling 11's 1 px of 321,219 **to the digit** on a fresh
invocation is a free replication of the adjudicated anchor — banked. So is the 0.046% mode
difference: the frame was derived from the mesh's own aspect, so the two conventions nearly
coincide on this subject and the 4.68% catastrophe is confirmed absent. The correction is
convention identity, not repair — and 2 px is still not 0, which is why the pin goes in.

Folded with the above: `turn_render` gains `tag: galleonclay` so the twin-prompt file's
stem keys cannot drift (the halt report's fourth finding), and `_fixtures` now points at
the two written files.

### The two fixtures are RATIFIED

Both verified before ratifying, per the inherited-claim rule. **The palette file**
transcribes 4d/Ruling 8 faithfully — warm 50–100 over measured 62–88, blue 273–301
SUSPENDED with its numerator and denominator, both gate bounds null, chroma floor 12.0
carried as inherited, the ratified pair's own 1.622% off-band baseline recorded as
context-not-threshold, and G7's bandlessness recorded rather than patched. One note for the
record: the warm band's proposed edges widen slightly past the stated ±10° (exact would be
52–98; blue's arithmetic is exact) — nothing rides on it while both bounds are null and the
gate reports both ways; if a bound is ever derived, the edges re-derive with their margin
stated, blue's path. **The twin-prompts file** is byte-faithful to the pair's saved
workflow string except exactly the two ruled deltas (G6 per Ruling 7, G7 per Ruling 9) —
verified directly against `workflow_7_bow_three_quarter.json` — and its one-constant-string
argument is the per-view rule correctly applied to a subject with no anatomy words. The
recipe it records is the pair's, which is the anchor `ship.json` was waiting for.

### Arm T restarts — the sequence, both branches pre-stated

1. `git pull` — this ruling's edits land together.
2. `e04_profile_check.py --profile profiles/ship.json` — expected: the `restylize_views`
   row gone; remaining rows VALUE-DIFFERS class or the known `cull_unseen` limit. A
   NO-SUCH-FLAG row anywhere → HALT: my edit is wrong.
3. `restylize_views` loads the ship profile clean. The ANDON fires → HALT.
4. One profile-only framing verification at width-fit: views 1 and 7 geometry agreement —
   expected 1 px / 0 px, the adjudicated instance. Any other digit → HALT per Ruling 11
   ("the next nonzero halts again").
5. Then the twins: **eight eye-level**, prompts from `E04-twin-prompts.json`, controls from
   exact silhouettes at 1066×1024 width-fit, cloud discipline standing, every gate in
   measure-report mode. Compute and pre-register H4's reach ceiling on the eight before
   projection. G7's rows report lid clusters and the sub-40° fixed window per view; the
   pale near-neutral cluster's key margin reports per view; blue reports both ways.
   **The next scheduled ruling is the twin-baseline halt.**

Clean through 2–4 → straight into 5, no further ruling needed before the baseline halt.
