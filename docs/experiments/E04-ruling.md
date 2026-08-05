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

---

## Ruling 14 (advisor, 2026-08-04) — view 5 adjudicated PASS; the twins are CLEARED; H2 is FALSIFIED by Finding B, which is the experiment paying for itself; allocation is ruled NONE

### A — view 5's 2 px: ADJUDICATED PASS, same reading as Ruling 11, bound unmoved

**The evidence is Ruling 11's second reading on every axis:** all three differing pixels
across all eight views are **on the silhouette boundary, none interior**; view 5's two are
242 px apart — scatter, not a segment; centroid (0.0, 0.0017) where a structural offset
must move it; hit bbox identical to mask bbox; the other non-90° pair (views 3/7) at 0;
opposite-view mask areas identical, which is what an orthographic silhouette must do; and
the character control's 0/0 (Ruling 11) still proves the instrument can return zero. The
prey measured 4.68% with a 34×42 px bbox gap; this is 0.0006% with no gap. A ray resolving
triangle-edge coincidences differently under two float orderings, on the yaw pair whose
axes keep irrational components — the structure the executor noted constrains the cause
without a chase, and the chase stays declined per Ruling 11.

**The mechanics, restated so this cannot drift into a tolerance:** the bound stays **0**.
This instance is adjudicated on its evidence; the next nonzero halts again and gets its own
ruling. **The eight-view row (0,1,0,0,0,2,0,0) is banked as this subject's framing anchor
state** — any future change to the framing path re-runs all eight and compares against the
row, which is stronger than the two-view gate it grew from. The voluntary extension to all
eight, and the boundary/interior classification that let the count speak, are endorsed by
name.

**The twins are CLEARED.** Nothing else gates them. Fly the batch.

### B — suspension in prose does not disarm: H2 is FALSIFIED, and this is the finding the experiment exists to buy

**The finding is ratified in full and it is a primary finding under the spec's own test.**
`subject_profile.bind()` reads only `tools`; `_gates` and `_still_suspended` are prose; a
silent profile resolves to the other subject's compiled assumptions, and both existing
instruments — the unknown-key ANDON and the purity checker — look only at values that are
*present*. The blind direction is real, it was live (`texpass_brush --prompt` still
defaults to the W3 identity string; `project_twins` would have armed W3's 0.80 halt on a
subject with no distribution), and closing it requires work outside the profile and the
fixture. **H2 as written — "no shared-code edit needed beyond Step 0's named items" — is
FALSE, and that is a full success:** the route's first non-character subject found the
profile boundary incomplete in the absent-value direction. That sentence is what E04 was
for.

**Ledger twenty-nine.** Ruling 2 named this exact accident class — *"not harmless for a
galleon run without `--prompts`"* — and I banked the sentence as a finding instead of
commissioning its detector. I then adopted the purity gate and called it "two gates, two
failure modes, keep both" — while both look the same direction. The executor found the gap
by diffing the two profiles against the tools' own argument tables, which is the check I
should have specified in Ruling 2.

**One correction to `ship.json`'s own prose, made because I read the operand before ruling
on it (the ledger-24 lesson applied):** the suspended-acceptance note calls `edge-ref
700.0` *"literally one character's figure width in twin pixels"* — true, and its
implication (re-derive per subject) inverts the semantics. The help text: erosion **is
scaled by this figure's width over that reference** — `edge-dist 7.0` at `edge-ref 700` is
a *ratio*, 1% of figure width, self-scaling per view against the subject's own measured
width, bounded below by `edge-floor` and locally by the A3 invariant. **Replacing 700 with
the ship's width would break the calibration it anchors.** The pair (7.0, 700) travels
together as one tuning fact. Corrected in the profile with this ruling.

**The remediation, ruled — and every projection-leg item is expressible as a profile value
with zero route-code change:**

1. **`project_twins` block grows to cover the family explicitly** (all flags verified
   present): `reg-iou-min: 0.0` — suspension *expressed*: the assert goes vacuous, the IoU
   still prints per view, the ship derives its own bound from its own spread after the
   baseline. `bbox-tol: 9.99` — vacuous: the assert is A27-demoted anyway and the ship's
   measured 1.95× area swing would fire the label on geometry, not defects.
   `head-facing-min: 0.45`, `head-edge-dist: 7.0` — **equal to the body values, which makes
   the head band inert**: a ship has no head, and the band machinery (crop rect from prep
   meta) runs without granting any region looser acceptance. `facing-min: 0.45`,
   `edge-dist: 7.0`, `edge-ref: 700.0`, `edge-floor: 2.5` — explicit **FIRST-RUN OPERATING
   POINTS**, not ship-derived calibrations: the ratio semantics self-scale, the A3 cap
   bounds erosion locally, and the baseline halt reports the per-view facing and edge
   diagnostics that decide whether they carry into projection. Writing a value that equals
   the default is the point: silence was the defect.
2. **`bake_hero_prep` block** per C below.
3. **`texpass_brush` gets no values yet and is FORBIDDEN on the ship until its block
   carries ruled ones** — standing law from this ruling, enforced today by the coverage
   check and by the stage-2 ruling that must precede any stroke; its prompts fixture is
   still `REQUIRED, NOT WRITTEN`.
4. **Two shared-code work items, Step-0-class, character anchors byte-identical, landed
   before stage 2:** (a) `e04_profile_check.py --coverage` — diff a profile against the
   reference profile's per-tool keys: every key the reference carries that the subject
   neither carries nor lists in an explicit `_not_on_route`/decided-absence entry is
   flagged. `character.json` **is** the registry of subject-classified flags — that is what
   it was built to be. (b) the loader learns a reserved `_NOT_CLEARED` key: binding a tool
   whose block carries it is an ANDON with the block's reason. Character path unchanged by
   construction (its profile has no such key). Together they close both directions:
   present-key-no-flag (existing ANDON) and subject-flag-no-key (coverage + tripwire).
5. `smart_decimate`, `head_render`, `mesh_stats` land in the profile's explicit
   not-on-route list — absence as a decision, recorded, which is what the executor's own
   table already argued for two of them.

### C — the bake: allocation is ruled NONE, expressed as `head-scale: 1.0`

**Ledger thirty.** The spec staged projection and the H4 ceiling without staging the bake
both consume — *"before building a path to a resource, enumerate the resource,"* E08's
lesson, in my own spec one arc later. The allocation suspension made the bake un-runnable
without a ruling and nothing in the spec surfaced that; the executor found it when the
ceiling tool stopped on a missing `meta.json`.

**The allocation decision, ruled under the Director's delegation and overrulable in a
sentence: NONE — uniform texel allocation for the baseline.** Grounds: the character's
privileged region was earned by a measurement (E01: facial structure is where acceptance
is decided, 3.1–4.5× polygons on the head); no measurement supports any privileged region
on this subject — the stern castle is a plausible guess, and the suspended note's own words
are *"not decided, not guessed."* Uniform is the null intervention: it gives any future
privileged-region arm the baseline it must beat, which a guessed region never could.

**Expression, with zero code change:** `head-scale: 1.0` — the scaling line
(`c + head_scale * (luv - c)`) is the identity at 1.0, so the head-band machinery runs
inert; the crop rect stays at its default **explicitly**, recorded as inert-at-scale-1.
Paired with B's equal-to-body head acceptance in projection, no region of the ship
receives privileged treatment anywhere in the route. **Pre-stated readings for the bake
run:** its ANDONs were written for characters (`n_head > 500`, the scale-preservation
assert at ×1); if any fires on the ship mesh, that is a Finding-1-class expressibility
limit — **report and halt, do not tune**. If the bake completes, `e08_ceiling` computes
the H4 reach ceiling **on the eight eye-level cameras** and pre-registers it before any
projection, per the spec.

### The sequence from here

1. **Twins fly now** — A is adjudicated, predictions are already blind at `b8245a7`.
2. Bake with the ruled allocation → H4 ceiling pre-registered (local; watchdog check
   applies).
3. Profile edits land with this ruling; the purity check re-run on the grown blocks is
   part of the executor's next verification (NO-SUCH-FLAG anywhere → halt, my edit).
4. **The twin-baseline halt** — the standing report (palette both ways, IoU + centroid per
   view, the pale-cluster and thin-enrichment watch items, the landing table with G7's lid
   rows) **plus** the bake/ceiling receipts. I rule the projection parameter set there,
   against the ship's own numbers.
5. The two B work items (coverage mode, `_NOT_CLEARED` loader key) land before stage 2,
   with character byte-identity anchors.

**H-status after this ruling:** H1 weakened per Ruling 13 (response, not landing — twins
re-measure). **H2 FALSIFIED** (Finding B — the primary finding). H3/H4/H5 unchanged,
awaiting twins, ceiling, and landing table respectively.

---

## Ruling 15 (advisor, 2026-08-04) — the frame is re-ruled to 1072; the bake guard gets a scale-aware fix; the batch regenerates, and that is not a re-roll

### ANDON 1 — allocation NONE is unexpressible: Finding-1-class #2, ratified, and the fix is specified

**Ratified exactly as reported.** `bake_hero_prep:381` demands `share_area >
share_area_pre * 1.2` — a growth assert that the identity can never satisfy (0.2432 →
0.2432, exact); the `--no-head-scale` branch demands the input *already* privilege a
region. **Both branches of the allocation machinery assume a privileged region exists** —
the second structural character-assumption E04 has found in route code (elevation was the
first), and H2's falsification deepens accordingly. The executor's refusal to try the
other branch as an escape is the discipline working.

**Ledger thirty-two.** Ruling 14 claimed the NONE expression needed *"zero code change"*
with the contradicting assert sitting in the tool — my own grep of that file surfaced the
scale-preservation ANDON's message text one line below the growth condition I never read.
The pre-stated failure branch saved the run from a workaround, which is what pre-stating
is for; the claim itself was checkable and unchecked.

**The fix, specified for the executor:** the guard becomes **scale-aware**. At
`head-scale 1.0` the requested transform is the identity, so the thing to verify is that
the identity *survived* — `share_area == share_area_pre` within float tolerance (measured:
exact) — and the growth clause applies only when growth was requested
(`head_scale > 1.0`, existing condition byte-unchanged on that branch). The character path
invokes at 3.0 and executes the identical code it always did — **unchanged by
construction**, Ruling 12's standard. The `--no-head-scale` branch is untouched. Then the
ship bake runs, `meta.json`/`pos`/`nor`/`mask` land, and `e08_ceiling` pre-registers H4's
reach ceiling on the eight eye-level cameras before anything projects.

### ANDON 2 — `w: 1066` is not a legal generator width. The frame is re-ruled: **1072**.

**The mechanism is confirmed from the numbers:** the Qwen VAE downsamples by 8;
1066/8 = 133.25 encodes to 133 latent columns and decodes to **1064** — every twin came
back 1064×1024 against 1066-wide controls, and `palette_gate` correctly refused the
pairing. W3's 752 and the pair's 1024 are both divisible by 8, which is why four
experiments and the pair never met this; the pair dodged it *specifically* through Ruling
6's 1024×1024 deviation. The 1066 was derived correctly from the mesh and the generator
still cannot accept it — a constraint that lived inside the cloud VAE, met by the first
landscape-frame subject. Not a ledger entry for anyone: nobody asserted legality; nobody
had ever needed to.

**The frame is 1072×1024, ruled on three grounds:** it is divisible by 16 (safe one level
deeper than the VAE's /8, against stacks that patch at 16); it is **this subject's own
Gate 0 frame** — the 1072×1024 the Gate 0 driver measured and used, precedent on-subject
in my own Ruling 6 text; and the fit is verified — at margin 1.204 the fitted width covers
1.2024 world units, vertical coverage at 1072 is 1.1486 against a mesh height of 0.9598,
so the 6 px over the derived 1066 is slack, not distortion. 1064 is rejected: /8 only, no
precedent, and 2 px *under* the derived aspect. The profile updates in place at all three
frame sites with the derivation history kept; `thin-extent`'s px scale shifts 0.56%,
within its own derivation's slack — value unchanged, noted beside it.

**A new standing constraint leaves this arc for CLAUDE.md** (subject-independent physics,
code-side per the profiles boundary): *generation frames must be generator-legal — derive
from the mesh, then round to the nearest legal width; ÷8 is the Qwen VAE's floor, prefer
÷16.* A frame-legality assert at the generation boundary joins the shared-code work-item
bundle.

### The batch regenerates at 1072 — and the A23 test says this is not a re-roll

**Would the rule have been the same whatever came out? Yes:** the frame mismatch was
caught by an ANDON on arrival, before any content judgment; the entire batch regenerates
for a mechanical legality reason independent of what any twin looks like; nothing is
selected. The 1064 batch **stays on disk as the frame-discovery record** (0 credits, so
the cost of honesty is zero). The blind predictions at `b8245a7` carry to the 1072 batch
**with two items honestly demoted from blind** — G7-landed-on-broadside and
masthead-gold were *observed* on the 1064 batch, so for those two the 1072 run tests
declared priors, not blind predictions; the demotion is recorded here so nobody later
mistakes them for blind hits.

**Consequences, enumerated:** every frame-bearing artifact regenerates at 1072 — clay
renders, exact silhouettes, control images (local, minutes). The eight-view
geometry-agreement row re-runs at the new frame and **replaces (0,1,0,0,0,2,0,0) as the
subject's framing anchor state** — the 1066 row stays in the record as its frame's
measurement; the bound stays 0; any nonzero halts for its own adjudication exactly as
before. Then the batch resubmits under the standing discipline — workflows saved,
link-checked in code, `dry_run`, `estimate_credits`.

### Endorsed by name, and the small gaps banked

**Withholding the registration numbers** — refusing to measure a frame-edge defect and
call it registration — is the grade-what-it-can-move rule applied to a *measurement*, and
it is exactly right. So is leaving crop-vs-rescale **unresolved** rather than forcing it
from artifacts that cannot show it. So is the scratchpad-copy discipline on
`palette_gate` — canon untouched, verdict column discarded, the vacuous bound proven
vacuous. The tool gap it worked around is real: **`MAXBLOB` cannot express the spec's
"no numeric pass bound"** — a null/report-only blob bound joins the work-item bundle.

**The spec-material screen stands as run:** view 2's 5.61% off-band is diffuse (largest CC
1,686 px against E08's invented-sleeve 4,882) — reported, not a garment, no re-roll
trigger; view 4's zero blue-band pixels is a bankable oddity for the baseline report.
**Masthead gold** is Ruling 6's in-spec-material-wrong-place class, correctly not
re-rolled; the placement call is the Director's, and his window opens when the baseline
report puts the twins in front of him. **G7 landing plainly on the broadside where the
cluster instrument said NEAR on a three-quarter** is the strongest prior yet that the
landing question is view-dependent — the landing table's per-view G7 rows are where it
resolves.

### The work-item bundle (all Step-0-class, character anchors, before their consumer needs them)

1. `e04_profile_check.py --coverage` (Ruling 14).
2. The `_NOT_CLEARED` loader key (Ruling 14).
3. `palette_gate` null blob bound — report-only mode (this ruling).
4. Frame-legality assert at the generation boundary (this ruling).
5. `bake_hero_prep` scale-aware guard (this ruling — **first: it gates the bake, the
   ceiling, and projection**).

### The sequence from here

1. Bake guard fix → ship bake → **H4 ceiling pre-registered on the eight**.
2. Frame artifacts regenerate at 1072 → new eight-view anchor row (nonzero halts) →
   purity check → batch resubmits.
3. **The twin-baseline halt**: the full standing report — palette both ways, IoU +
   centroid per view (now measurable against a legal frame), the watch items, the landing
   table with G7's per-view rows, masthead-gold flagged for the Director — plus the bake
   and ceiling receipts. I rule the projection parameter set there.

---

## Ruling 16 (advisor, 2026-08-04) — the bake tolerance is ruled from both sides of the line; the 1072 row is adjudicated PASS with the reading extended; ledger thirty-three is precision laundering

### Q1 — the identity tolerance: strict equality is WITHDRAWN as mis-derived; the replacement is relative 1e-6, sized against the detection target

**Ledger thirty-three, a new form: precision laundering.** Ruling 15 wrote *"(measured:
exact)"* from a 4-decimal printout **the executor had flagged as 4 dp at the time**, and
paired it with *"within float tolerance"* while specifying no tolerance. A printed value is
not the value — display precision is not measurement precision. The executor resolved the
ambiguity in the only non-inventing direction — implement strict, report full precision,
let the run decide — and that choice is endorsed by name: it is what made the premise's
falsification clean instead of pre-softened.

**The strict-equality condition is withdrawn, not retuned** — its stated derivation
("measured: exact") does not describe the measurement, which is the Ruling 10 withdrawal
test verbatim. And bit-equality was never the property: Blender stores UVs as float32,
`pack_islands` multiplies every coordinate by a global scale that cancels in the share
*ratio* but not in the last bits — the executor's own mechanism note. A guard demanding
bit-equality of float32 sums through a float pipeline is the documented
**fires-on-correct-input class, worse than no guard** (the centroid-checksum precedent,
CLAUDE.md/README).

**The replacement, derived from both sides of the line per that precedent** — noise
measured, signal derived, tolerance between them:

- **Noise side, measured:** delta 2.98e-08 absolute = exactly 2 float32 ULPs, relative
  **1.2e-07**, on a run where the identity demonstrably survived (agreement to 7
  significant figures).
- **Signal side, derived from the guard's prey:** the smallest event that can *really*
  move a share is one island's area — a median 88-texel island against the packed area is
  ~**3e-5 relative** — and the failure this guard exists to catch (the requested
  allocation not surviving packing) is **factor-level**, 10⁻¹ and up.
- **The ruled line: `abs(share_area − share_area_pre) ≤ 1e-6 × share_area_pre`** — ~8×
  above the measured noise, ≥30× below the smallest single-island event, five orders below
  the prey. The same number would have been ruled whatever the run had printed, because
  neither side of the derivation is the observed delta's to move: the noise side is ULP
  arithmetic, the signal side is island geometry.

The `< 1.0` branch raising as unspecified is endorsed — no symmetric clause gets invented
unbidden. The diff shape (`else:` → `elif args.head_scale > 1.0:`, assert body absent from
the diff) is the unchanged-by-construction standard, verified by the executor exactly as
Ruling 12 defined it.

### Q2 — the 1072 row (0,3,0,1,0,1,0,2): ADJUDICATED PASS, and reading two gains a named extension with its own discriminator

**The boundary six take Ruling 11's reading two directly:** 7 px of 2,484,048 (0.00028%),
all four axis views exactly 0 where `cam_axes`' snap applies, all four diagonals nonzero
where irrational components live, centroids ≤0.0011 px, bboxes identical. The count
growing 3 → 7 between frames is not a trend: each frame is its own float landscape, and
each frame's row is its own anchor. The two cheap confirmations are banked — pixels square
to 9 decimal places at 1072 (no anisotropy; the 6 px is margin), and the +0.56% scale
shift reproducing the thin-extent figure from an independent direction.

**The interior pixel is a mechanism Ruling 11 did not name, and the adjudication extends
the reading rather than stretching it.** View 1 (435,352) sits in a 94.7%-filled region
where **both implementations independently produce isolated 1-px tessellation pinholes**
— 8 against 7 in a 13×13 window — and disagree about one. A pinhole rim is locally a
surface/no-surface edge: the same float edge-ordering physics as the outer silhouette,
relocated to an interior gap. **The extension, with its discriminator stated so it cannot
become a tolerance:** an interior disagreement takes reading two **only where both
implementations independently show pinholes in the same neighbourhood** — the gaps must be
a measured property of the tessellation, not of one instrument. A hole one implementation
shows in surface the other renders solid, with no pinhole cluster around it, fits no
pre-registered reading and halts as its own investigation. The bound stays 0; the row is
banked as the 1072 anchor state; the next nonzero halts.

**One watch note, opened for no one:** the pinholes themselves are a tessellation property
at render resolution, present in both instruments, harmless at 1-px scale — the controls
already carried them and a ControlNet at 0.9 cannot resolve 1-px speckle. If a future
subject's pinhole *counts* grow into perforation, the weld and tessellation are where to
look — not the framing.

**Also endorsed by name:** the per-pixel verification that overturned the executor's own
assumed pinhole identity before it reached the report — *assumed (628,470), checked,
found (435,352)* — the inherited-claim rule applied to one's own sentence mid-paragraph.

### The sequence — unchanged from Ruling 15, now unblocked

Tolerance line lands → bake completes → `meta`/`pos`/`nor`/`mask` → **H4 ceiling
pre-registered on the eight** → batch resubmits under the standing discipline → **the
twin-baseline halt**, full standing report plus bake and ceiling receipts.

---

## Ruling 17 (advisor, 2026-08-04) — THE TWIN-BASELINE RULING. The eight are accepted as the ship's adjudicated stage-1 set; projection is cleared behind one named classification.

### The twins are ACCEPTED

**Registration, on the honest operand, sits inside the character's adjudicated band:**
0.8442–0.9565 against W3's 0.8329–0.9533, all eight views above W3's own worst adjudicated
view. The spec-material screen has no trigger — nothing arrived that the fixture does not
name. The eight twins are hereby **the ship's adjudicated calibration set**, which is
A27's jurisdiction logic applied to a new subject: the suspended IoU halt cannot fire on
its own calibration set, stays `0.0` through this projection, and a ship bound derives
only when a ship-side failure exemplar exists — W3's failure values are W3 geometry and do
not transfer.

**The fill_holes catch is endorsed by name and becomes a recorded subject-class fact:** a
rigged ship is porous, `binary_fill_holes` swallows enclosed background (+58% of figure),
and the raw key is this subject's figure definition — the tool now says so beside the
code. *"A collapse that large on two views and not the other six is a shape story, and
shape stories deserve an operand check"* — that sentence is the operand discipline this
repo runs on, applied by the executor to the executor.

### One named classification before projection — both readings pre-stated so nothing waits

The view-0 question is answered by one measurement the artifacts already hold: **intersect
view 0's largest off-palette component (4,562 px) with its sub-40° red mask** — and
complete the palette table's missing rows (views 1 and 2; view 2 carries 8,433 red px and
its off-palette row is materially interesting). Readings:

- **Majority-red → the component is G7's landed red** sitting outside a warm band that was
  derived from an image where G7 had not landed — the exact gap the palette fixture
  records as *"G7 has no band."* Red is a declared element; the spec-material rule has no
  trigger; **projection proceeds immediately.** The numbers already lean here hard: the
  two off-palette outlier views are the two highest-red views.
- **Majority-not-red → an unnamed material candidate** → the A23 question opens (one
  re-roll of that view, new seed, rejected artifact stays in the record) — halt for that
  ruling before projecting.

### Ruled through, so the projection dispatch is complete

1. **The operating points carry unchanged** — facing-min 0.45, edge 7.0@700, floor 2.5,
   head values body-equal. Nothing in the baseline impeaches them; the thin key-out is a
   trust-mask phenomenon upstream of acceptance; the A3 cap bounds erosion locally. The
   stage-1 report brings the per-view acceptance diagnostics that would revisit them.
   Banked beside the ceiling: the floor's pre-registered price is 55.84% − 42.72% = 13.1
   points of reach on this subject.
2. **The pale cluster's cost is accepted and stays measured — the backdrop does not
   move.** Ruling 8's overrule bar is a measurement showing an alternative *wins*, not a
   measurement that the default has the cost it was banked with. View 3's cluster mean
   sits at 0.0471 against the 0.06 cut (view 0 at 0.0627, just over); the per-pixel key
   decides texel by texel; the seven other views hold the same surface at 0.07–0.11. The
   stage-1 report must state **specifically what covered the pale-deck surface** — which
   views' paint, or holes.
3. **The centroid signature is banked:** every dy negative, paint above silhouette,
   scaling with presented rigging — reported, not gated, no exemplar. One consequence
   pre-registered: paint-above puts the waterline rim at background-adjacency risk, which
   is what the edge erosion exists for; the stage-1 edge diagnostics will show whether it
   worked.
4. **G7 is a per-view roll on a declared element** — lands 2 of 8 (port broadside,
   stern-on) with a 6,438-vs-55 mirrored-camera asymmetry, E08's blue-sleeve signature on
   an element that is *supposed* to be there. The fixture holds as amended (red,
   head-noun). Projection takes the union of accepted paint, so the lids inherit red
   exactly where accepted views carry it, and the provenance records which. H1 closes as
   measured: **the head-noun form is necessary (its absence produced zero red anywhere)
   and not sufficient (landing is a per-view roll).**
5. **The two windows that are the Director's, presented at this halt:** the G7 *colour*
   window (default red as authored, standing since Ruling 13) — and **masthead gold**: the
   fixture declares one gilded spire on the stern turret; the twins paint gold at all
   three mastheads. In-spec material, wrong place — the gate cannot see placement, no
   re-roll rule applies, and the Gate 1 sheet will show it at his zoom. If he wants the
   mastheads gold, one sentence amends the fixture (the G6 precedent); if not, the polish
   path exists. **Neither window blocks projection.**

### The stage-1 dispatch (after the classification lands red)

`project_twins`, profile-driven, all eight twins — the owner sidecar lands natively (the
ship is the first subject born with it). The stage-1 report: **share of valid AND share of
the pre-registered 42.72% ceiling** (H4's units, both, always together) · per-view
acceptance diagnostics for the operating points · the pale-deck coverage answer · edge
diagnostics at the waterline · per-view stroke-candidate hole map, since **the stroke
cameras derive from the hole map, measured, not inherited** — that derivation is the next
ruling's material. Then the halt is the stage-1 report, before any stroke.

### Executor predictions, noted for the record

Three of ten clean with two inversions, owned with their mechanism — *"I reasoned from
projected area and the subject answers by rigging."* That is this subject's first
calibration lesson and it now sits in the record where the next prediction can use it.

---

## Ruling 18 (advisor, 2026-08-04) — the classifier is withdrawn and the question re-decided on pre-recorded signatures: view 0 is G7's red, and A23 FIRES on view 7's waterline band

### Ledger thirty-four — I specified a classifier my own ruling had already falsified

The majority-sub-40° operand was mine (Ruling 17), specified while Ruling 13's own text
held *"the arrived hue sits at 41–45, outside every band."* A majority test on a window
the declared population mostly exceeds returns **not-red at perfect presence** — the
works-perfectly test, unrun again, ledger twenty-seven's exact family. The executor ran it
as written, reported the edge effect as evidence rather than re-cutting, and the sentence
that closes the loop is theirs: *"that the operand has a known edge effect on this
component is evidence for the ruling, not licence for me."* Endorsed by name, alongside
the chroma/lightness comparison nobody asked for — the discriminating evidence was built
before the ruling needed it.

**The operand is withdrawn as a classifier and retires to what it always was** — the
fixed-window *trend* instrument, valid for before/after deltas, never for majority
verdicts on populations that straddle its edge.

### View 0: G7's landed red — re-decided on signatures that pre-date this halt, so the re-decision is not a retune

The rule that replaces the withdrawn one uses no 40° cut and would have ruled identically
whatever the sub-40 fraction read: **match the component against the two pre-recorded
material signatures.** Arm G7's arrived red: h 41.1–44.9, C\* 34.3–48.1. The tar: h 40–50
at C\* just over the 12.0 floor. View 0's component: **unimodal h 41→49, C\* 36.3, L\*
26.1** — inside the arrived-red signature, 2.3× the tar's chroma, three times its
lightness, and spatially a compact block on the hull (114×79 px) rather than an edge
tracery. **It is the declared element sitting in the recorded band gap** ("G7 has no
band"). No A23 trigger. View 2's completed row is the same story at scale — 7.46%
off-palette at **87.7% red** on the view carrying the most red — and views 4/6's small
majority-not-red components (132–362 px, C\* 13.7–15.8) are the declared tar at the
band's 50° edge, boundary speckle, not candidates. **The table's four majority-not-red
rows decompose into: one declared red split by a window, two declared tar at a band edge,
and one real candidate.**

### View 7: the A23 rule FIRES — one re-roll, new seed, the rejected twin stays in the record

**The component is an unnamed material on the evidence:** a single coherent 2,002 px band
spanning x 398–686 across the **bottom of the hull** (y 896–939 of a figure ending at
939), median rgb (56,77,97), **h 262.6 at C\* 14.4** — chroma-bearing above the floor,
outside the warm band, outside the suspended blue band even at its widened 273 edge (20°
below the measured span), **0.0% red**, and absent from the canon pair (no such cluster
anywhere in 4d's table). Positionally it is not G11 — the fixture puts the sea-blue frieze
*along the bulwarks*, not at the waterline. Mechanism read, stated as inference and not
fact: the model grounding the ship in implied water. Scenery baked into a hull texture is
precisely what the projection must not inherit knowingly — E08 A23's own words.

**The bounded procedure, verbatim from the precedent:** one re-roll of view 7, new seed,
recorded; the rejected twin stays on disk and in the record with its measurement; a second
failure is the result, not a third roll. The re-rolled view runs the **full baseline row**
— registration IoU/centroid, palette both ways, landing, watch items — beside the old
row. **Pre-stated readings so nothing waits:** clean row in family with the other seven →
the eight are complete, **projection proceeds directly under Ruling 17, no further ruling
needed before the stage-1 report.** The same class again → that is the result; halt, and
the seven-vs-eight projection decision comes back to me with the measurement. The
Director's overrule window stands as always — if he *wants* a waterline, one sentence
amends the fixture and the re-roll is moot; default is the spec as authored.

### The G7 record, updated with the classification's data

Landing is now measured at component scale: view 1 at 99.5% red (956 px), view 2 at 87.7%
(3,113 px), view 0's 4,562 px block confirmed red by signature. The per-view roll stands —
view 4's mirror-camera 55 px against view 0's thousands — and H1's close is unchanged:
**the head-noun form is necessary and not sufficient; landing is a per-view roll the union
projection resolves.**

---

## Ruling 19 (advisor, 2026-08-04) — the Director's word on the waterline: it becomes a LAYER, and the window closes on a third path

**The Director, on view 7's waterline band:** *"I want to be able to add the waterline
like a layer, if that's possible. The data that we'd learn from making that work could be
applied to other models in the future."* That is not the amend-the-fixture branch and not
a plain rejection — it is a third path, and it is recorded here as the ruling on his open
window.

### What his direction and Ruling 18 agree on: the base stays clean

A clean base atlas is the **precondition** for a layer, not an alternative to it. One
view's rolled water band projected into the base would not be a waterline — it would be
partial contamination on whichever texels view 7 happens to own, invisible to seven other
cameras, impossible to toggle, and baked forever. **The A23 re-roll of view 7 proceeds
exactly as ruled**, and the re-rolled twin's cleanliness now serves two goals at once: the
E04 baseline, and the future layer's substrate.

**The rejected twin gains a second purpose**: it is the first measured exemplar of the
model spontaneously painting environment-contact content — band characterised at h 262.6,
C\* 14.4, x 398–686, y 896–939, rgb (56,77,97) — banked as reference data for the layer
experiment. A23's keep-the-rejected-artifact rule was written for evidentiary honesty;
today it also pays as data.

### E10 is named: environment-contact layers. Queued post-E04, not opened.

The experiment slot after E09 goes to the Director's idea. The sketch, recorded now so the
spec (written after E04's Gate 1) starts from it:

- **The primitive is a second accumulating state** — a layer atlas over the same UVs,
  alpha-carrying, composited in-engine (Godot and UE both take detail/decal layers
  natively), toggleable per scene: in port, at sea, dry dock.
- **The mask is geometric and exact**: a waterline is a plane intersection — *texels below
  `waterline_z`* is a per-texel query the raycast machinery already answers, the same
  family as the exact silhouette. No keying, no diffusion guesswork about *where*.
- **The content is masked generation into the layer**, not the base — `texpass_brush`'s
  masked inpainting and `texpass_iter`'s commit discipline, pointed at the layer state.
  Per-layer provenance comes free from the same replay machinery.
- **The subject data lands where subject data lives**: `waterline_z` is a profile/fixture
  value per ship. The mechanism is subject-independent — which is the generalisation the
  Director named: the same contact-mask + layer-state + compositing contract serves snow
  on boots, mud on wheels, moss on ruins, wet hulls. Each is a contact query plus a layer.
- **The dataset flywheel inherits it**: the sdlab asset-lane manifest's channel roles were
  built not-W3-shaped on purpose; a `layer` channel role is a schema entry, not a rebuild.

**Scope discipline unchanged:** nothing opens mid-arc. The sequence stands — re-roll →
projection → strokes → the ship's Gate 1 — and E10's spec is written after it, with this
ruling as its charter.

---

## Ruling 20 (advisor, 2026-08-04) — A23 closes NO; the re-rolled view 7 is ACCEPTED; the eight are complete and PROJECTION PROCEEDS

### A23's arc, ratified end to end

The waterline is **decisively gone** — 2,272 px → 0 in the exact band the rejected twin
painted, not present at any scale — and the procedure ran to the letter: deterministic
seed increment stated as arithmetic, the diff against the rejected run enumerated at two
fields in code, 0 credits, **re-roll 1 of 1 spent**, the rejected artifact preserved with
its sha and now serving as E10's founding exemplar. The exact-band check (chroma-bearing,
hue 240–273, lower 7% of figure) is the decisive instrument — built from the rejected
twin's own characterisation, answerable only by presence or absence.

### The changed row: the class is settled, the magnitude has no rule to fire, and none is invented

**The escalation was correct, and the reason was the right one line:** Ruling 17 accepted
the eight *as measured*, and the set that was accepted is not the set that would be
projected. That identity change is mine to rule on, not the executor's to wave through —
"in family" was doing load-bearing work in my pre-stated branch precisely for this case.

**The class question is settled by signature, ratified:** the replacement component
(h 43.1, C\* 15.5, L\* 10.7, rgb 47,22,13) sits squarely inside the recorded tar class —
views 4/6 measured h 42.3–44.5, C\* 13.7–15.8, L\* 8.5–12.4 — and nowhere near the
waterline class (h 262.6, C\* 14.4, **L\* 31.7**). A **declared** material (G3/G9) whose
realization sits at the warm band's 50° edge.

**The magnitude (largest CC 10,866, tar-class off-palette 9,289, row 1.74% → 4.28%)
fires nothing, and inventing a bound while looking at it is the forbidden move.** The
palette bounds are null by the spec's own design; the two-threshold instrument's job is
to flag a large component for *classification*, which happened, and the classification
answers *declared*. Re-applying Ruling 17's actual acceptance criteria to the new row:
registration **0.93017** (in the adjudicated range, unchanged to the third digit),
spec-material screen clean, watch items measured. **The re-rolled view 7 is accepted; the
eight are complete; projection proceeds under Ruling 17's dispatch.**

### Three things banked so the downstream readings are honest

1. **The band finding, queued for the re-derivation the suspension already names:** the
   warm band's 50° lower edge undercovers the declared dark materials' realization range —
   the pair's tar-brown measured h 64.4 (in-band), the twins' tar runs h 41–49 (out).
   Three instances now: the pair's own 904 px hull shadow, views 4/6's speckle, and a full
   strake at 9,289 px. The palette fixture's own path applies — *edges re-derive when the
   ship's own twins exist* — and they now do, nine twins of data. Not re-derived here:
   nothing gates on it this run.
2. **Pre-registered for the Gate 1 reading — H3's named likely site:** view 7's tar runs
   darker than its neighbours', so **owner-seam magnitude at view-7 ownership boundaries
   on the hull** is expected. The native owner sidecar measures it; the sheet's owner
   column shows it. If hull seams appear there, they were predicted here — and if the
   Director's eye lands on them, the harmonisation arm in the polish queue is their
   documented owner.
3. **The roll-generalisation, with the executor's sentence kept:** G7's red (6,438 vs 55),
   the waterline (2,272 vs 0), the tar realization (2,575 vs 9,289) — same prompt, same
   control, seeds apart. *"Spontaneous contact is a roll, and anything that's a roll
   can't be a feature until it's authored."* That is E10's charter in one line, and it is
   also the standing argument for the owner-seam harmonisation arm: per-view rolls are
   what tone harmonisation exists to reconcile.

### The dispatch is live

Stage-1 projection, Ruling 17's parameters, all nine artifacts in the record and eight in
the set. The owner sidecar lands natively. The report: share of valid **and** of the
42.72% ceiling · per-view acceptance diagnostics · the pale-deck coverage answer · edge
diagnostics at the waterline rim (the paint-above signature's named risk) · the hole map
that seeds the stroke-camera derivation. **The next halt is the stage-1 report.**

---

## Ruling 21 (advisor, 2026-08-04) — the bg-admission bound is SUSPENDED mechanically; the coverage checker moves up to NOW; ledger thirty-five is mine and it is sharp

### The ANDON fired correctly by its own terms, on a bound that does not describe this subject

**Ratified as reported.** `--bg-max-pct 2.0` at `--bg-de 10.0` is W3 calibration data
absent from the ship's block — **Finding B's class, third instance, first to fire** — and
its structure was never going to survive this subject: the denominator is the
edge-relaxation's newly-admitted set, which concentrates at rims *by construction*, and
the quantity it counts is antialiased rim mixing, which scales with **perimeter** — on a
subject whose 512 rigging shells give it a perimeter-to-area ratio nothing in the bound's
calibration history resembles. The executor's measurement settles the population's
identity: median depth 1.4–5.0 px from the boundary on every view, 0–17% deeper than
20 px, already-trusted texels at **0.01%** within ΔE 10, newly-admitted median ΔE
**31.5** — and the **Director-ratified canon pair itself measures 3.26% by the identical
test**, inside the twins' 1.26–4.81% silhouette-fraction range. The twins are not
anomalous against the artifact he approved. This is the perimeter-not-area lesson through
a third door, exactly as named.

### Ledger thirty-five — and the consequence is that the mechanical check stops being queued

Ruling 14's *"the block grows to cover the family explicitly (all flags verified
present)"* was enumerated **by hand from halt2's table** — and `--bg-de` / `--bg-max-pct`
were sitting at lines 81–85 of the argparse grep I had already run in the same session.
Same form as ledger thirty-two: the contradicting fact visible in my own tool output,
unread. Hand enumeration missed two flags; the mechanical enumeration was specified in the
same ruling and queued "before stage 2," and the third instance fired in the gap between
queued and landed. **The consequence: `e04_profile_check.py --coverage` lands NOW, before
projection re-runs** — diff the ship block against `character.json`'s per-tool keys, and
**every absent key gets an explicit decision in one pass**: a value, a vacuous
suspension, or a `_not_on_route` entry. No more whack-a-mole; the class closes, not the
instance.

### The bound: SUSPENDED, expressed mechanically, with its proper future form queued

`ship.json`'s `project_twins` block gains, by this ruling: **`bg-de: 10.0`** — unchanged,
because it is the *metric window*, and moving it would break comparability with A2's
recorded 0.18% / 38.31 — and **`bg-max-pct: 100.0`** — vacuous, the reg-iou-min pattern:
the diagnostic computes and prints per view, the halt cannot fire, and the ship derives a
real bound from clean measured data after the atlas exists. **Choosing any number today —
per-subject, perimeter-normalised, or interior-fraction — would be deriving a threshold
while looking at the result it judges.** The gate's proper future form is recorded for
that derivation: normalise the rim quantity by perimeter (the standing CLAUDE.md rule),
and gate the **interior fraction** separately — the >20 px population is the real prey's
home, with one known collision to check first: the pale deck (G10) is a *declared*
material near the backdrop's value, so interior-near-backdrop is not automatically
background there. The proxy's limits get stated before its bound exists, for once.

**The protection story during suspension, so nobody mistakes this for running naked:**
trust ∧ geometry stays armed at both stages · the edge erosion removes the bulk rim (the
ratio semantics give ~10.6 px nominal on this subject's width) · A3's thin-strata
protection is a **ruled trade whose cost this rim population is** — and the trade just
validated spectacularly: **erosion removed 0.0% of the 1–2 px and 2–4 px strata on the
subject whose declared stressor is thin structure**, against the retired erosion's
100% / 100% / 77.6% annihilation on the character · the in-tool commit gates stay armed.
The stage-1 report mandates the full per-view bg diagnostics — % within ΔE 10 under
**both** denominators, median ΔE, the depth distribution, and the interior fraction with
its pale-deck overlap checked.

**Endorsed by name:** measuring what the 19.06% *is* before reporting it; the canon-pair
comparison that placed the twins inside the approved artifact's own range; and touching
nothing — not the bound, not the profile, not the tool — while the ruling was mine to
make. The suggestion that the two flags join the profile explicitly even at tool values
is ratified and generalised by the coverage pass above.

### Sequence

Coverage pass → every absent key decided explicitly in `ship.json` → purity re-check →
**projection re-runs** → the stage-1 report, which remains the next halt.

---

## Ruling 22 (advisor, 2026-08-04) — the 41 are decided in one pass: three buckets, two decision rules, and a fourth decision form

**`--coverage` is ratified as built** — exiting non-zero on any undecided key makes it a
gate rather than a briefing, which is the difference Finding B existed to teach.

**Bucket A (13 keys, whole off-route tools): RATIFIED.** `head_render` and `mesh_stats`
(the ship's own `_gates` already declare head instruments meaningless; Gate 0 recorded the
front-view-rect warning as the instrument noticing correctly) and `smart_decimate` (never
ran — raw TRELLIS topology, the bake's own "native UVs, no re-unwrap"). The decisions
exist in prose; the executor lands them in whatever shape the checker reads. Moving a
written reason to where the instrument can see it is exactly what this pass is for.

**Bucket B (21 route keys on W3 numbers): two decision rules, applied by the executor to
every key — no key gets a bespoke argument:**

1. **SPENT** — a key already consumed by a run in the record gets **the value that ran**,
   marked SPENT with the run as provenance. `bake_hero_prep.res: 4096` is the worked
   example, and the executor's framing is adopted verbatim: *the record should say the
   ship chose 4096 rather than that nobody asked.* The nine `restylize_views` recipe keys
   are the same class — the eight twins ran on them — and writing them **closes
   `_still_suspended`'s generation-recipe entry**: the anchor it was awaiting exists, and
   recording what happened is not choosing something new.
2. **LIVE** — a key awaiting its first consumption gets the code default as an explicit
   **FIRST-RUN OPERATING POINT**, the Ruling 14 pattern verbatim: silence was the defect,
   an explicit value is a decision, and the next halt's diagnostics decide what carries.

**Bucket C (7 keys behind `_NOT_CLEARED`): the marker is ruled the FOURTH accepted
decision form, and the strongest.** A `_NOT_CLEARED` block decides its whole tool — the
tool is forbidden, so per-key values would be theatre — and the lifecycle is the point:
**when a ruling lifts the block, its keys revert to undecided and coverage fires again**,
which forces the stage-2 ruling to decide them as the price of clearing the tool. The
executor's refusal to widen the accepted forms unilaterally is endorsed by name — *"a
checker that accepts markers it wasn't specified to accept is how silence creeps back
in"* is this arc's Finding B stated as a design rule, and it goes in the record.

**Sequence unchanged:** the executor lands all 41 under these rules in one commit →
coverage exits 0 → purity re-check green → **projection re-runs** → the stage-1 report,
still the next halt.

---

## Ruling 23 (advisor, 2026-08-04) — STAGE 1 RATIFIED. The stroke stage is dispatched: decks by the measured pair, sides by derivation, the bottom by decision, the prompts by the measured rule.

### Ratified, with the arc's best number named

**36.89% of valid · 86.4% of the pre-registered reach ceiling** — and the ceiling itself
**cross-validated from the inside**: `project_twins` printed reachable/valid 42.7%
against `e08_ceiling`'s pre-registered 42.72%, two tools, different days, same number.
That is what pre-registration is for. **H4 confirms on the only like-with-like ratio**:
character 92.8% of reach, ship 86.4% — 6.4 points, not 31.9; the rest is geometry the
spec predicted before any twin existed. The bg suspension is vindicated in full (every
view would have halted at 2.0; the highest fractions sit on the smallest denominators —
a perimeter statistic in disguise, exactly as ruled; **trusted core 0.00–0.01%
everywhere**). And the pale-deck question resolves the honest way: the deck is not
mis-painted, it is **unpainted** — 24.99% styled against 40.05% — absence of coverage,
exactly as `ship.json` predicted. *Whatever fixes the deck is a camera or a stroke, not
a backdrop* — adopted as the closing line on the backdrop question.

### The stroke dispatch, structured by the hole map's own decomposition

**91% of holes are geometry, not misses** (1,782,458 beyond the ceiling; 181,400
reachable-but-unpainted). The target is two coherent surfaces, and each gets its ruling:

1. **Decks (upward-facing, 75.01% holed): the measured elevated pair is the stroke set,
   no re-derivation needed.** Task 4a already measured it as the best two-camera deck
   answer (30.17% → 49.58%, bow/stern beats beam, 40° the measured peak). Cite 4a; do
   not re-derive what is already derived. **Pre-registered so Gate 1 reads honestly:**
   the deck plateaus near 53% even at twelve cameras — after the pair's strokes, roughly
   half the deck's holes remain and fall to dilation. That is the subject's geometry,
   priced before the first stroke.
2. **Sides (54.14% holed, and the 181,400 reachable-but-unpainted): derive the side
   strokes from the hole map** the way 4a derived deck cameras — per candidate yaw,
   raycast what fraction of side-class hole surface it first-hits, greedy by marginal
   coverage, and **report the table with the proposed set**. The waterline rim (19.44%
   styled, the least-covered region) is side-low surface — state specifically what the
   proposed set buys it, since E10's layer needs a painted base there.
3. **The hull bottom (downward-facing, 74.91% holed): NO strokes this arc — ruled, with
   the reasoning on the record.** The ship floats: E10's charter already establishes the
   below-waterline surface as underwater in every floating presentation, the 2.5D camera
   never sees a floating hull's bottom, and no measured consumer exists for that paint.
   Bottom holes fall to dilation from hull-adjacent paint — planking continuing planking.
   *Bound an expensive arm before spending it*: bottom strokes would be spend on surface
   with no viewer. *If a future scene beaches or dry-docks the ship, a below-arm runs
   then, with its own cameras* — and the Director's one-sentence overrule window is open
   as always.

### The brush fixture, ruled by the measured rule

**`brush_prompts` = the twin-prompts constant string, per stroke.** The twin file's own
argument transfers whole: this subject has no view-specific anatomy words, material words
stay byte-identical across views (E08 B4 held with the control locking orientation), so
the correct application of the per-view rule is one constant string — for strokes exactly
as for twins. The executor lands the file mechanically beside the camera derivation;
`_fixtures.brush_prompts` closes.

### Lifting `_NOT_CLEARED`, by its own lifecycle

The stroke dispatch is the stage-2 ruling Ruling 22's lifecycle demands: lifting the
block reverts `texpass_brush`'s keys to undecided and **coverage fires — that firing is
the procedure, not a defect**. Each key gets its explicit decision in the same commit:
the prompt from the brush fixture above; the recipe keys as **FIRST-RUN OPERATING
POINTS** at the accepted character route's values (they are what Gate 1 accepted; the
per-stroke sidecars measure whether they carry). Coverage back to 0, purity green, then
strokes fly — cloud, per-stroke sidecars, in-tool gates unchanged.

### The next halt

The **stroke-camera derivation report**: the side-stroke table with marginal coverage,
the proposed full stroke set and order (the spiral is subject data — derive it from
where stage 1 left paint, per `_still_suspended`), the waterline-rim answer, and the
lifted-block key decisions. I rule the set; then the strokes run to the finalize → pack
→ **Gate 1 sheet** — five columns, both elevated cameras and a beam view, textures under
`--flat`, full size, the Director's eye.

---

## Ruling 24 (advisor, 2026-08-05) — the stroke set is RULED at six; the coincidence becomes a checked equality before anything flies; ledger thirty-six is an operand-kind error of mine

### The set: SIX strokes — the deck pair plus the proposed four, order B

**The funnel is the ruling's whole basis, and it was bought by a falsified prediction
that named its own failure mode in advance** — that is the prediction discipline paying
at full price, endorsed by name. The side class is **occlusion-bound** (64.28% of side
holes occluded on every one of 26 candidates, zero never-facing), the reachable ceiling
is 239,219 texels, the proposed four take 60.47% of it, and **all sixteen remaining
candidates together add at most 5.43 points**. Four more strokes past the proposed set
would buy ~1.4 points of valid across four more generations — on a subject where the
per-view roll is measured three times over (G7's 6,438-vs-55, the waterline, the tar).
The bound argues against the longer set and the ruling follows the bound. **Order B
(ring sweep, deck pair last) is ratified as derived** — anchoring simulated at each
stroke's turn across four candidate orders, which is what "the spiral is subject data"
was supposed to mean.

**Deck expectations re-registered on the measured number — and ledger thirty-six is
mine:** Ruling 23's "roughly half the deck's holes remain" read Task 4a's *visibility
coverage* (49.58%) as *committable share*; measured, the pair commits 200,660 texels and
**73.56% of deck holes remain**. An operand-kind error — the exact class the executor
self-corrected on thin-extent in the same report — and the correction generalises: **a
pre-registered expectation names its operand kind like any other check.** The
thin-extent correction is ratified the same way: 15.79–48.66% of per-stroke committable
holes against the record's 10.20%-of-visible-area — both true, different denominators in
kind; stroke planning uses the per-stroke figure from here.

### The negative deviation: RATIFIED as flagged

W3's brush negative carries eight belt terms — negatives *earned* from that character's
observed brush defects, which makes them subject data. Importing them would arm
character-derived values on the galleon, the standing prohibition. The ship's negative
is its own spent value; **if the ship's strokes roll a recurring artifact class, its
negative terms get measured then** — the W3 pattern applied per subject, not W3's
answers.

### Finding B, site four: the coincidence becomes a checked equality before any stroke flies

`brush_cloud_step.py:38` hardcodes five recipe values and binds no profile; the ship's
strokes run through it; the decided keys agree with it **by coincidence of value, not
construction**. Before the first stroke: **a pre-flight assertion lands inside
`brush_cloud_step`** (A32 — the check lives in the tool that acts): the values entering
the graph are compared against the decided `texpass_brush` profile block, **HALT on any
disagreement**, no skip flag. That closes the live risk at one-time cost. The class fix
— `brush_cloud_step` binding the profile properly — joins the shared-code bundle
(Step-0-class, character anchors), with the reason coverage was blind recorded beside
it: **the coverage reference is `character.json`'s tool blocks, and a tool with no block
there inherits the character's blind spots into the registry itself.**

### Cleared to fly, with the sheet's reading pre-registered

Strokes → finalize → pack → renders → **the five-column Gate 1 sheet**, no ruling
between here and the sheet unless an in-tool gate fires (any firing halts as usual; the
new pre-flight is one of them). Re-registered so the finished mix is read honestly: deck
ends ~44.8% styled after the pair; the waterline rim sits near 55% of ship average
(E10's base caution stands); dilation carries the hull bottom (444,364), the
occlusion-bound side remainder (~616k), and the rigging — **the finished asset will run
dilation-heavy relative to the character's 27.0%, and that number was priced here, on
geometry, before the first stroke flew.** The instrument's own anchors are endorsed: the
ceiling reproduced byte-equal inside a new tool, eight stage-1 figures re-derived at
zero mismatches, purity and coverage declared before the edit rather than read off
after.

---

## Ruling 25 (advisor, 2026-08-05) — the third frame consumer is pinned (ledger thirty-seven); the registry's definition is corrected; one sweep, then the strokes fly

### The guard is RATIFIED, and two of its design choices go in the record by name

**Required, not optional** — *"an optional guard is a skip flag with a different name"*
sits beside A32 from today on. **Provenance, not value, for the prompts** — value
equality would have fired on correct work, because `character.json` carries the stale
default that E08's fixture exists to supersede; a check's failure mode was examined
before the check was adopted, which is the discipline the record keeps asking for. The
byte anchor (E08's recorded stroke-1 workflow rebuilt exactly) and the three proven
firings — each exit 1, each writing nothing submittable — complete it. Ratified as
landed.

### The frame: two keys ruled in, and ledger thirty-seven is mine

`texpass_iter` gains `aspect: 1072,1024` and `fit-axis: width` — the same values decided
twice already in this profile, now on the **third consumer**. The tool's own header says
the three must agree; **Ruling 12 item 3 had named `texpass_iter`'s 752×1024 as the
third hardcoded frame**, and Ruling 13 pinned the fix on two consumers anyway. The
record held the list and I did not re-read it — the exact family as ledger twenty-two,
one abstraction level up. The catch chain is endorsed in full: the selftest run because
the header says to run it; the 1.29% model-vs-emit discrepancy chased **because a
raycast through the same grid should agree exactly** — direction, not magnitude, is what
made it a lead; and the measured consequence (four of six cameras clipping, the deck
pair at 5.87%/5.90%, every lost pixel off the bow and stern where G1 and G5/G6/G12
live) established *before* anything was characterised. The brush would have composed at
denoise 1.0 against a ship running off both edges of its own render.

### The registry's definition is corrected — the sharpest sentence of the arc is now law

*"0 UNDECIDED means every flag the character bothered to write down is decided. It does
not mean every flag that matters is."* Ruling 14 defined `character.json` as *the*
registry of subject-classified flags; measured at two sites now (a tool with no block,
a key at the character's own default), that definition was wrong by incompleteness.
**Corrected: `character.json` is the registry of flags the character needed to write.
The true registry is Task 2's classification table** — every constant it marks
subject-data, whether or not the character's value differs from the code default. Two
consequences:

1. **Immediate, before any stroke:** one sweep — the classification table's subject-data
   rows against `ship.json`'s decisions; any tool+key with no explicit decision gets one
   under Ruling 22's four forms, in one commit. Minutes, and the fifth instance of this
   class does not get to fire mid-stroke.
2. **The bundle item upgrades:** coverage's reference becomes a machine-readable
   subject-flag registry derived from the classification table, replacing the
   `character.json` diff. Step-0-class, with the two measured blind spots as its test
   cases.

### Then the strokes fly

Keys landed (this ruling's commit) → the sweep → coverage and purity green → selftest at
the ship frame → emits regenerate at the ruled frame → the pre-flight guard green per
stroke → **the six strokes, order B** → finalize → pack → renders → **the five-column
Gate 1 sheet**. No ruling between here and the sheet unless a gate fires. Everything
Ruling 24 rests on stands — the derivation read its frame from arguments that defaulted
correctly; the pipeline, not the derivation, carried the defect.

---

## Ruling 26 (advisor, 2026-08-05) — invar's operand becomes geometry at bounds untouched; stroke 1 is CLEARED to commit from the downloaded artifact; ledger thirty-eight

### The ANDON fired on A32's documented-unsound operand, at its second consumer

`brush_cloud_step.py:267` defines *outside the figure* as `|render − 107| < 1.5` —
colour as a proxy for absence of surface — while `texpass_iter commit`'s A32-corrected
block, thirty lines of comment included, says in its own words: *0.42 is also
`--hole-grey`, so an unpainted hole on real surface is indistinguishable from background
by colour, by construction… test the property, not a proxy for it.* **A32 fixed one
consumer. `invar` kept the proxy, and it only executes when a stroke flies — this is the
first stroke since.** The measured decomposition is decisive and it is the same shape as
A32's own: the halting component is 93% ON geometry and 93% inside the job mask — dark
tarred planking painted onto the hull's foot, the least-covered region on the subject,
by the stroke dispatched to serve it. The brush doing its job, halted by a check calling
real surface *background*.

**Ledger thirty-eight.** *When you fix a root cause, find its other consumers* is
CLAUDE.md's own rule, written from E01's keying lesson — and A32's fold, which was mine,
did not run the grep. Second instance in two legs of a fix applied at some of its sites
(Ruling 25's frame was the first). The bundle's registry item gains a sibling
observation: the repo's correction discipline needs the consumer-grep to be part of the
fold, not a virtue remembered afterwards.

### The fix, ruled: geometry operand, bounds untouched

`invar`'s *outside* becomes the dilated complement of `hit.png` — the same operand, the
same dilation role, and the same reasoning as commit's corrected block; **a missing
`hit.png` HALTS** (an invariance check with no geometry cannot test, and the existing
`n_out` assert already embodies that philosophy). **`--tol 1.0` and `--conc-tol 4.0` do
not move** — the executor's same-bounds demonstration (mean 0.216 → 0.020, max 106 → 11,
largest component 1,515 → 40 px, HALT → PASS) is the proof the bounds were never the
problem, and it was run as a diagnostic beside the fired gate rather than as a bypass of
it, which is the difference the record keeps rewarding. **Anchor before the fix is
trusted:** corrected `invar` runs over E08's recorded accepted stroke jobs — all must
PASS; any firing on an accepted stroke is a finding and a halt, not a tuning input.

### Stroke 1: CLEARED to commit from the downloaded artifact

No regeneration and no re-roll — nothing here is a content failure. The artifact is
seed-stamped with its saved workflow, the gate that fired was measuring with a broken
operand, and the content is the dispatched paint on the dispatched surface. Commit runs
under `texpass_iter`'s own in-tool gates as always.

### The sweep and its findings, RATIFIED

**80 subject-data flags on the route, 80 decided, exit 0** — the corrected registry law
applied mechanically one leg after it was written. The `--margin 1.204` decision is
ratified **with the supersession stated honestly**: Ruling 13's "no margin entry ON
PURPOSE" was anti-invention (do not pin a *different* margin), not pro-silence; an
explicit 1.204 is the same adjudicated value made visible, which is what the corrected
law demands. The `--bg` decision is the sweep's best move — **SPENT with a byte anchor**,
the twins' own control rebuilt identically rather than asserted equivalent. The
`$null -eq $null` self-catch — a comparison printing BYTE-IDENTICAL for files that do
not exist, found and fixed by its own author mid-sweep — is *a check that cannot fail is
not a check* applied to one's own instrument, endorsed by name. The walker's N/A-rule
proxy (argparse *action* standing in for *role*) goes to the bundle beside the registry
item.

### Sequence

Land the operand fix → the E08 anchor passes → **commit stroke 1 from disk** → strokes
2–6 under the corrected gate → finalize → pack → renders → **the five-column Gate 1
sheet**. No ruling between here and the sheet unless a gate fires.

---

## Ruling 27 (advisor, 2026-08-05) — the stage-2 run is RATIFIED end to end. GATE 1 IS OPEN: the galleon goes to the Director's eye.

### The run, ratified

**The anchor did what anchors are for:** corrected `invar` passes all eight E08 accepted
strokes — including stroke 7, the original false-ANDON stroke, now at **0 px** under the
honest operand — and the corrected check was then **proven able to fail** before being
trusted, which is the house discipline applied without being asked. Six strokes committed
in order B, every gate green on the geometry operand (largest hot component 8–95 px
against the 200 bound), pre-flight guard PASS per stroke, six submissions, **0 credits**
— and one placeholder mask name caught on the *saved file* before submission, now
foreclosed by a 64-hex assertion on input names. The E07 record read correctly at the
finalize fork: **neither arm was adopted, so the accepted route is the default flood** —
the surface-aware primitive stays in the post-Gate-1 queue where E07 left it.

### The mix, read as pre-registered — and the model behaved as declared

> **reference 36.89% · brush 6.87% · dilation 56.24%** — against the character's
> 68.8 / 4.2 / 27.0, which is NOT the comparison; the ceiling is.

Reference stands at **86.4% of this subject's 42.72% reach ceiling** (character: 92.8% of
74.1%). Brush runs **1.6× the character's share**. Dilation carries the hull bottom, the
occlusion-bound side remainder, and the rigging — every point of it priced on geometry
before the first stroke flew (Rulings 23–24). Deck 24.99% → 41.76% against a modelled
44.82; foot 19.44% → 24.41% against 26.37; **every actual sits below every modelled
figure** — the derivation declared itself an upper bound twice and held everywhere, which
is what makes its numbers usable for the next subject.

### The instruments built for the sheet, endorsed

Ownership reconstructed by **re-running the shipped commits to byte-identity** rather
than reimplementing the filter chain — the replay that cannot diverge from itself was
named as such and checked by bytes instead. `gate1_sheet` gained its fifth column
**additively** with the character anchor byte-identical on the no-new-flags path, and
flushed another hardcoded subject value on the way (`--mask-tag`, the profile class,
recorded). `emit` as the deck-camera renderer is correct twice over: it is the only
renderer that can reach the elevated cameras, and its raycast output has no lighting —
**the flat readout CLAUDE.md requires for judging texture**. The beam-view twin
comparison (ΔE median 7.43 / mean 11.32 / p90 26.24) is recorded beside the sheets,
lower on every column than the accepted character's comparable views — reported, not
judged.

### GATE 1 IS OPEN

The artifacts: `E:\AI\training\facet_next\E04_stroke\out\` — **`GATE1_sheet_beam.png`**,
**`GATE1_sheet_deck.png`**, the per-column panels at all three ruled cameras, and
**`galleon_final.glb`** (43 MB) for the Blender zoom that ruled E08. The verdict is the
Director's, at his zoom, in a sentence. The reading frame, all pre-registered: provenance
reads against the **42.72% ceiling**, never the character's raw mix · owner seams are
**expected** on hull and sails, likeliest at view-7's boundaries (Ruling 20) · the
dilation-heavy finish was priced on geometry (Ruling 24) · the executor points two
regions without judging them — **the deck's brush-composed region where pale scrubbed
decking should read, and the hull foot at 55% of the ship's average base coat** — and
his two windows remain open for one sentence each: **masthead gold** (fixture says one
spire; the twins painted three) and **G7's colour** (red as authored, landed 2-of-8 as a
per-view roll). His word closes the arc; the hypothesis scoring and the E04 close follow
it.

---

## Ruling 28 (advisor, 2026-08-05) — GATE 1: ACCEPTED. The delegated windows are decided. E04 CLOSES.

**The Director's verdict, in his words: "Dude, it looks good to me."** Ruled on the
sheets at his eye. On the pointed regions and the open windows: *"I don't even know the
areas of the ship that you're talking about. You're the advisor"* — the windows pass to
me under his standing delegation, and they are decided here.

### The delegated decisions

1. **Masthead gold: RATIFIED INTO THE FIXTURE.** The accepted asset carries gold at all
   three mastheads; the fixture declared one spire. An identity source that does not
   describe the accepted artifact is the exact incoherence this repo exists to prevent —
   *an element not named in the prompt is arriving by accident and will leave the same
   way.* Naming it is what makes it stay. `GALLEON-IDENTITY.md` gains **G13, gilded
   masthead finials**, with the full history in the row: never authored, arrived
   unprompted, flagged through two rulings with the window open, accepted with the
   asset, named under delegation.
2. **G7: the window CLOSES on red as authored.** The head-noun form is in the fixture
   since Ruling 13, the lids read plainly on the accepted broadside, and the per-view
   roll is characterised in the record. Nothing moves.
3. **The two pointed regions demote to the polish queue**, exactly as E08's queue
   demoted at its Gate 1: the deck's brush-composed read and the hull foot's thin base
   are optional polish on an accepted asset — the hull foot already has an owner in
   E10's charter (the layer needs a base coat there; a foot-serving stroke arm is the
   candidate if E10 wants it).

### The hypotheses, scored at close

| # | verdict | the number |
|---|---|---|
| H1 | **supported in weakened form** | the head-noun form is necessary (zero red anywhere without it) and not sufficient — landing is a per-view roll (6,438 vs 55 px on mirrored cameras); the element floor was withdrawn as structurally unreachable (Ruling 13) |
| H2 | **FALSIFIED — the experiment's payoff** | five primary findings under the spec's own test: silent inheritance (four sites), elevation's stage boundary, allocation expressibility, frame legality, the invar operand. Each hardened the system: the coverage gate, the registry law, the classification-table sweep, the frame constraint in CLAUDE.md, two operand corrections at second consumers |
| H3 | **unrefuted, instrumented, not numerically scored** | the owner sidecar is native and the sheet carries the owner column; the Director's eye named no seam at his zoom. The named-site measurement (view-7 boundaries, `e04_blotch`) remains runnable from artifacts on disk if the polish queue ever wants it |
| H4 | **CONFIRMED** | ceiling pre-registered at 42.72%, achieved 86.4% of it, 6.4 points below the character on the only like-for-like ratio — and the ceiling cross-validated byte-equal from inside a second tool |
| H5 | **CONFIRMED** | the landing table at the pair's own level — median 10–11 of 12 across eight twins on a subject with no face, the two shortfalls (G7's roll, the tar's band-edge realization) characterised to the pixel |

### The arc, closed

**Every generation in E04 cost zero credits** — the G7 arm, nine twins, six strokes, one
re-roll. Two executor sessions ran it; both were exceptional, and the pattern that
defined them is the pattern this repo was built to teach: *the selftest run because the
header says so; the 1.29% chased because direction matters more than magnitude; the
guard proven able to fail before being trusted; the halt taken with the artifact already
in hand.* The advisor's ledger closed the arc at **thirty-eight entries**, fourteen of
them this arc — and the honest summary of those fourteen is one sentence: every one was
an operand, an enumeration, or a precision claim that a measurement was already sitting
somewhere to check. **The record survives contact with itself. That is the whole
method.**

**What follows E04, queued and not opened:** the E10 spec (the Director's waterline
layer, Ruling 19's charter) · the galleon into sdlab as **asset #2** — the first with a
native owner channel, the flywheel's second turn · the dense-turnaround exporter spec
(facet's debt to the asset lane) · both subjects' polish queues, all optional · the
shared-code bundle (registry rebuild, `_NOT_CLEARED` loader key, `palette_gate` null
blob bound, frame-legality assert, `brush_cloud_step` profile binding). The Director
picks; nothing runs unbidden.

---

## Ruling 29 (advisor, 2026-08-05) — the asset-2 blob-bound halt: suspension is TRANSLATED at the export boundary; canon's null stands; the schema learns suspension in its own lane

**The halt is ratified** — the executor carried canon's ruled `null` into the manifest,
let sdlab's validator refuse, invented nothing, and proved the refusal was one field by
probing the full chain with a throwaway beside the shipped manifest. The measured
context is banked as the class's newest instance: **W3's 800 px blob bound would reject
two of the three renders of the asset the Director accepted** (blobs 1,738 / 1,495 /
263) — a global constant travelling between subjects **through a schema** for the first
time, where every prior instance travelled through code.

**The resolution: the export tool translates suspension into the unreachable sentinel
at the boundary** — `max_offpalette_blob_px: 16777216` (the whole 4096² atlas, a bound
no blob can reach) with an adjacent annotation naming it a SUSPENSION encoding and
citing Ruling 8. This is E04's own established pattern (`bbox-tol 9.99`,
`bg-max-pct 100.0`): suspension expressed as a value the consumer actually receives.
**Canon keeps its `null`** — the facet record's semantics ("no bound exists yet") are
not traded for interchange convenience; the translation lives in the export tool with
its reason, which is what an export tool is for. **The class fix is filed to the lane
that owns it:** the sdlab schema should learn explicit suspension (null + required
reason) because a schema that demands an integer forces exactly the invention the
non-circularity rule forbids — the only numbers derivable are the ones the bound would
judge. That item goes to the sdlab session's queue through the Director, who holds it.

The base-asset sha discipline (hashed before and after every write, inside the tool, no
skip flag) and the not-even-`--dry-run` restraint on the ingest are endorsed as run.
Task 1 completes on the sentinel translation; the ingest remains the sdlab session's.
