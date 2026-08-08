# The arc, as it happened

*The chronological record of how facet got from a rejected asset to four accepted
ones. This is the narrative that used to open the README — it belongs here rather
than on the front door, because it is a history, not a status. For the current
state see [the README](../README.md); for the evidence behind any claim below see
[docs/experiments](experiments/).*

**Read it as written.** Claims later measurements overturned are kept in place with
the ⚠ annotation that overturned them. That is deliberate: the correction is more
useful than the original, and a record that hides its own mistakes is the thing this
repo exists to avoid.

---

<!-- Moved out of README.md by the E19 treatment, 2026-08-08, at the Director's
     word ("the readme reads more like a changelog"). NOT rewritten: every line
     below is byte-identical to the README it left, corrections and ⚠ annotations
     intact. The README now links here. -->

**Where it stands.** Geometry is solved: reconstruction produces real facial structure
given the right framing, and polygon budget allocation works.

**Texture is not.** Four experiments improved measurable properties of the texture stage —
the unwrap, the culled surface, the dilation source, the seam levelling — and at
[E07's Gate 1](experiments/E07-ruling-gate1.md) the Director ruled the asset **not
close**. The cause is recorded there and it is a measurement failure, not a tuning one: every
unit those experiments graded on is a **5×5 high-pass statistic**, and the defect that decides
acceptance is a **large region of the wrong material** — a steel blade wearing skin tones, a
boot carrying scattered gold and green. A region like that is smooth inside itself and
registers only its rim. An arm cut dilation source distance **70×** and took speckle below the
reference asset while changing nothing to the eye.

The structural fact underneath it: on the finished asset, **28.4% of texels come from the
styled reference, 37.7% from diffusion invention and 33.9% from interpolation**. Every
experiment up to that point improved *how the other 71.6% is filled*; none reduced it.

**What [E08](experiments/E08-ruling-gate0.md) then established — and this is the part
that generalises.** The reference stage was carrying a defect nobody had measured: the mask
telling the projector *where the surface is* was a keyed clay render missing **a quarter of
the figure**, interior rather than at the rim. Replacing it with the exact raycast silhouette
took reference coverage **28.4% → 39.1%** of valid texels, and **53.8% → 74.2%** of what two
cameras can physically reach, strictly additive, with no diffusion and no GPU.

**Restated after the intersection ([E08 Amendment 27](experiments/E08-ruling-gate0.md)).**
Those A2 figures were measured with the *trust* mask unbounded by the silhouette: paint on no
surface — every twin carries 550–8,991 px of it, and it is connected to the figure — was
setting the edge-distance field and holding erosion off the texels near it. On the current
twins that contaminated 25.3% / 19.6% of the figure's edge distances. Intersecting the trust
mask with the silhouette is now the route default, and its regression was strictly
conservative: **gains exactly zero, zero losses in the two thinnest half-width strata, every
lost texel within 5 px of paint that sat on no surface** (−7,574, measured in
[E08-intersection-regression.md](experiments/E08-intersection-regression.md)). The
standing two-camera baseline is **1,042,794 styled — 43.4% of valid, 82.4% of reachable**.

**Eight cameras are banked** ([E08-eightcam.md](experiments/E08-eightcam.md)):
**1,653,659 styled — 68.8% of valid, 92.9% of reachable** — against a reach of 1,780,546
(74.1% of valid) that matched the ceiling instrument's independently written computation to
the texel. A quarter of the gain came from union acceptance rising with camera count alone
(2.15× redundancy, no test changed) — so **an acceptance rate quoted without its camera count
is not a number** in this repo. A per-view registration halt is armed at IoU < 0.80 against
the exact silhouette, derived from both sides of the measured line (adjudicated twins
0.8329–0.9533; measured failures ≤ 0.578).

**And the architecture is now measured rather than assumed. Twins register; the prompt
carries identity.** Contradict the specification on eight elements — *silver* where gold
arrives unbidden, *black* where wine-red arrives — and the prompt wins **8 of 8**: median ΔE
**46.3** against **6.2** on five held controls, a **7.4×** separation. The LoRA, mesh and
control did not hold the character's attributes against a conflicting spec. **And it is still
the same figure** — face, build, pose, boots. Structure is held by the mesh and control;
named attributes are carried by the prompt. **This is a pipeline, not a one-character
generator.**

**The Director accepted the asset at Gate 1** (2026-08-04, ruled on the GLB at his own zoom
— [E08 Amendment 35](experiments/E08-ruling-gate0.md)). Measured provenance **68.8%
reference / 4.2% brush / 27.0% dilation** against the rejected asset's 28.4 / 37.7 / 33.9 —
reference ×2.42, diffusion invention ×0.11. *⚠ On-surface restatement, 2026-08-06
([E10-offsurface-ruling.md](experiments/E10-offsurface-ruling.md) Ruling 7): W3's bake
carries 2.5840% off-surface texels; excluding them, reach reads 74.30, styled/valid 69.28,
dilation 26.43 — the full table is in
[the report](experiments/E10-offsurface-r4ab-report.md). The on-surface family is the
standing cross-asset family; as-recorded stays beside it.* One region named at his zoom: a hard-edged
blotch on the crown, prior mechanism the documented unlevelled stroke seam (confirmation
dispatched). The post-Gate-1 quality queue demotes to optional polish.

**And the route generalises — E04's galleon is the second accepted asset** (2026-08-05,
"it looks good to me," ruled on the five-column sheets —
[E04-ruling.md](experiments/E04-ruling.md), 29 rulings — *the count read "28" here
until E15's verifier counted the record itself*). The ship ran the character's
route end to end with every subject value drawn from `profiles/ship.json` and
`canon/GALLEON-IDENTITY.md`: eight twins, six strokes, **zero credits across every
generation in the arc**. Measured mix **36.89% reference / 6.87% brush / 56.24% dilation**
— read against the subject's own pre-registered **42.72% stage-1 reach ceiling** (86.4% of
reach, beside the character's 92.8% of 74.1%): a ship hides most of itself from eye level,
and the difference is geometry, not regression. *⚠ Restated 2026-08-05, standing family FLIPPED 2026-08-06
([E10-offsurface-ruling.md](experiments/E10-offsurface-ruling.md) Rulings 1 and 7):
2.4967% of the bake's uv-valid texels carry positions not on the mesh (>1 px). On the
on-surface population the same quantities read **42.25 / 36.68 / 86.8 / 56.44 / 6.89** —
and with W3 now measured too (2.5840%, composition INVERTED: its off-surface population is
paint-depleted where the galleon's is paint-enriched, so three of five W3 headlines move
the opposite way), **the on-surface family is the standing cross-asset family**. The
as-recorded numbers stay beside it everywhere, denominators named. The population itself is
localized: 90.85% on the single outermost ring of the mask, largest blob 33 texels —
measured and bounded, no route change warranted.* The spec's central hypothesis — *no
shared-code edit needed* — was **falsified five times, and that was the payoff**: each
falsification hardened the profile system (the coverage gate and its subject-flag registry
law, the generator-legal frame constraint, two operand corrections found at fixes' second
consumers).

**E10 then closed the same day** ([E10-ruling.md](experiments/E10-ruling.md), 12
rulings, four generations, zero credits): **environment-contact layers** — the Director's
waterline, shipped as **data, not geometry**: the GLB stays whole, `waterline_z` rides in
the profile and manifest (four independent confirmations of the placed line), and the
scene's water hides the underwater body per frame. The arc's law, measured across eight
arms: **inpainting continues an asset; full-frame generation introduces new material;
layers fill by masked projection** — three inpaint attempts at ΔL\* −1.6 to −4.1 against
one full-frame at **+33.4**, one field changed. The layer machinery (second accumulating
state, two-lane profile vocabulary, base-invariance structural and proven under live
fire, straight-alpha RGBA export contract) generalises by construction: snow on boots,
mud on wheels, moss on ruins are the same contact query + layer + law. Both queued
items then ran the same evening — the `pos.npy` off-surface measurement (ruled; the
restatement above, [E10-offsurface-ruling.md](experiments/E10-offsurface-ruling.md))
and the exporter, next.

**E11 ran and was ruled the same day** ([E11-report.md](experiments/E11-report.md),
[E11-ruling.md](experiments/E11-ruling.md)): **accepted assets become training
data.** The dense-turnaround exporter is proven a pure function (two fresh emits
byte-identical on every channel; the beam anchors byte-identical to the recorded
sheets), and both subjects' dense trees — the galleon at 28 cameras with the **native
per-texel owner channel** (the first asset that has one), W3 at 26 with owner honestly
absent — validate through the sdlab lane's own codebase with **zero schema edits**. The
lane's palette gate reproduced the staged manifest's blob digits (1738 / 1495 / 263 px)
from freshly emitted renders through a different implementation. Ruled: the **emit
render generation is the standing export and training input** (the recorded
`renders_flat` are another generator's output no current invocation reproduces — frozen
in the record, superseded for training); a Gate-1 verdict covers the **asset**, renders
are post-verdict derivations by the anchored readout; **flat-only is what facet honestly
exports** — every render ships with its exact silhouette so backgrounds are
augmentation-side, and lighting would be a new renderer with its own anchors.

**E12 — the beast arc — ran designation to acceptance in three days**
([E12-ruling.md](experiments/E12-ruling.md), Rulings 1–30): the route's third
subject class, a **winged dragon**, designated from three reconstructed candidates
on full-size sheets ("3 is the winner"). What Gate 0
measured ([E12-gate0-report.md](experiments/E12-gate0-report.md)) rewrites the
priors: **9–12 welded shells against a character's 40–191 and the ship's 237–512** —
an order of magnitude more connected than anything this repo has reconstructed, every
satellite located (fangs, plus four tail spines on one candidate) — and the **wing
membranes come back as closed slabs that pinch, not sheets that hole** (0–1 boundary
edges of zero length; what breaks watertightness is edges with >2 faces, confined to
trailing rims on two candidates and running through the folded wing's field on the
designated mesh). Reconstruction **does not preserve the concepts' poses**: three
different stances all return as one symmetric wings-spread quadruped. The measurement
pass banked the subject's ceiling (**50.46% of 3,240,510 valid texels at eight
eye-level cameras**), ruled **elevated cameras NONE** (+1.77 points against a
~50-point self-occluded deficit, with the candidate ordering flipping inside
ray-sampling noise), and measured the thin-structure constraint the spec must design
against: **the character's `thin_extent` would withhold a third of the visible animal
and 60% of the wings, and no single global value separates membranes on a subject
where most detail is thin** (mask peaks at 1.78× membrane concentration). The
backdrop was derived, not inherited — and the derivation's payoff is that **W3's
"plain grey background" scores under the key's own 0.06 cut on this subject, bound by
the membranes**: the blade failure's shape pointed at the new surface class. The
first styled pair ran at zero credits — and was **REJECTED at the Director's eye**
([E12 Ruling 10](experiments/E12-ruling.md)): a generic stock dragon wearing the
right silhouette. The rejection bought two rules: **the style register is subject
data** (the saltroad painterly register two subjects earned acceptance under had been
*inherited* by a third it does not fit — the beast now runs ultra-realistic, no LoRA;
the studio plan is [docs/style-registers.md](style-registers.md)), and the
measured cause of the structural loss is the control: the profile's canny pair fires
on 5.2%/2.1% of the figure interior where the same clay carries 15.8%/11.2% at lower
thresholds — the relief never reached the ControlNet, and at denoise 0.92 the interior
was the model's to invent. The re-pair then ran under the ruled register with the canny
pair derived per subject and ruled **0.05/0.10** — the control carries 2.15× the
falsified pair's pixels — still at zero credits, and the Director's verdict is
**register CONFIRMED, pair not yet accepted**
([Ruling 11](experiments/E12-ruling.md)): *"a lot better, but the tongue is
missing and the face could be more defined."* His definition question reopened the
allocation decision by Ruling 2's own re-open clause; the ruled ladder runs
**resolution first** (a head-crop companion generation framed from the measured head
box), **geometry second and only on his sentence** (a bust-crop re-reconstruction
replaces the designated mesh — a Ruling 1 re-open, never a session's arm). Acceptance
now gates on three items in flight as handoff 5: the tongue's geometry answer on the
mesh (Gate 0 saw one on 00001/00002 and not on 00003), view 5's bounded re-roll (the
pale-tan haunch and bone-ivory membranes are spec violations on named elements), and
the companion. Handoff 5 ran all three at 0 credits
([the report](experiments/E12-handoff5-report.md)): **the mesh HAS a tongue** —
main-shell geometry, route-visible; Gate 0's omission-read falsified in one render at
mouth scale — both view-5 misses resolved on the seed alone, and the companion
measured the ladder's resolution rung: muzzle plates, nostrils and tooth rows define
at bust scale while **the eye is geometry-limited** (the clay carries brow plates, no
lens recess; a denser control produced *less* eye than the sparse one — the control
constraining invention rather than enabling it). The Director's eye then caught what
both seeds carry ([Ruling 12](experiments/E12-ruling.md)): the fixture's
pale-bone family — the word "bone" rode the prompt five times — rendering as
**exposed skeleton** on legs, tail underside and wing arms under the realistic
register, a register-family interaction the painterly register never showed at the
galleon's gold density. Canon corrected in place (D2 olive-tan, D6/D7 charcoal;
ivory is now the head's family), and the regeneration is dispatched as a new
decision bundle (handoff 6). The bundle ran at 0 credits and **the bone reads leave
at the worst seed** ([Ruling 13](experiments/E12-ruling.md)): same seed, same
control, prompt only — whole-figure pale-bone mass 28.71% → 7.69%, the rib element
gone, blade rows charcoal, wing arms green. The regeneration also measured the arc's
newest finding: **a colour term appears to reach structures that resemble the one it
names** — `pale ivory fangs` lands on the claws over `charcoal claws` in the same
string, on the view whose stem carries ivory words, while the stem without them
takes charcoal claws at the same seed — so a prompt's colour-family mass bleeds by
structural resemblance, not only by name (labelled hypothesis, two views, one
subject; the drop map's job may be larger than visibility). **The pair is
ACCEPTED** ([Ruling 14](experiments/E12-ruling.md), "I accept. Very good!"
— deviations accepted at the pair, dispositions landing with the bands
measurement): the subject's specification source and visual target exists, the
register row closes as *earned*, and the route proper is unblocked. The bands ran
against the accepted pair ([Ruling 15](experiments/E12-ruling.md)):
**warm-olive 85.4–147.3 adopted** (7 clusters, 55.23% of figure), blue-violet
honestly suspended on one cluster (a realised D3 stratum — which also caught
Ruling 8a's "no declared material occupies blue-violet" premise stale; the word
stands on the accepted pair's own anchor), the H1/H4 hue-collapse confound
**resolved — the register was not the cause** (the collapse recurs at 41.9°,
third subject, third time), and **D8 is CLOSED**: a 193 px ember-orange iris
with a vertical slit pupil, one blob, inside the head box, on an artifact that
stands. The twin gate's pair-validation then **halted itself before gating
anything** — its pre-registered third branch fired on a population nobody
anticipated, and the population has a name: **S-occlusion realised**
([Ruling 16](experiments/E12-ruling.md)) — the fixture's pre-registered
seam stressor presenting as cool marginal-chroma crevice shadow (7,293 px in
121 fragments tracing the throat seam, wing-body gap and spine bases; nothing
like the E07 garment class, which is ONE coherent blob). The gate now runs
report-structured with null bounds — the galleon's own configuration — and the
E07-class signature at the advisor's eye is the halt trigger. The eight twins
then ran at 0 credits ([Ruling 17](experiments/E12-ruling.md)) and banked
three results: **the chain reproduces exactly** (twins 1 and 5 returned zero
differing pixels of 1,835,008 against the accepted pair, from content-hash-
identical inputs); **the resemblance channel is resolved by natural
experiment** (ivory:charcoal foot ratios — fangs-term views 0.39–0.77,
no-ivory views 0.05/0.11, the bone-ivory-without-fangs view at 0.02: the
bleed rides the specific term, not family mass); and **the hue gate's cleanest
twin hid the worst defect** — a 43,999 px flat-black foreleg invisible to a
chroma-floored gate by construction, caught by the achromatic baseline, and
resolved by the one bounded re-roll (a seed defect — the calibration opposite
of the canon-caused D7 case, and the gate number *rose* as the defect left).
The Director's eye then caught the wing skeleton painted bone-ivory on the
two wing-spread views: the wing arms were D1's surface by fixture assignment
but **never named in the prompt** — the founding law measured in both
directions on one view (the named wing-claws stayed charcoal while the
unnamed bones went white). `moss-green wing arms and finger struts` now
stands in the entry; handoff 9 landed it in full on view 0 and half on view 4
([Ruling 18](experiments/E12-ruling.md)) — the compound phrase's head noun
bound and its second conjunct under-bound where the bat-anatomy prior pushes
hardest, so the term splits into two phrases and view 4 alone regenerates
(handoff 10). The same fold banked a first-of-its-kind operand lesson — a wide
measurement box that would have *manufactured* a crown regression by measuring
the wing fix entering its corners — and the Director's crown question was
answered geometry-first: the mesh carries a modelled spike fan, no ears; the
paint's merged-lobe ivory is judged at Gate 1 on the asset, by his sentence.
The Director then directed the arc's next capability
([Ruling 19](experiments/E12-ruling.md)): **the bones get the face
treatment** — the intricate structures diverge from the clay because a
full-figure frame gives the whole head ~1.6% of its pixels, so
[E13](experiments/E13-detail-pass-spec.md) makes the companion's measured
11.2× mechanism route-legal: crop-framed twins at the route's own yaws,
projected FIRST so crisp paint owns the detail texels, anchored by a
pixel-identity gate on the extended projector before anything is believed.
The Director then raised the bar to its real height
([Ruling 20](experiments/E12-ruling.md)): **these sprites are exemplars**
— they feed the training datasets, define the method, and will be displayed —
so E13 regenerates the texture route WHOLE from v8 stems rather than patching
the accumulated set, and his third unnamed-surface catch (the nape crest,
painted as crown-ivory vertebrae between D5's letter and D6's) triggered the
**occupancy audit**: every modelled structure enumerated against every
element's letter, done once — nape crest and spurs to D6, brow horns and jaw
barbels explicit in D5, legs re-confirmed smooth, no other gap found. The
current twins stand as the E12 measurement record (they bought two naming
laws, the palette correction, and the measured phenomenon that **term binding
is seed-dependent** — one seed resisted a term across three stems while its
neighbour bound it). The exemplar rebuild then ran (Rulings 21–23): **E13's
Gate 0 passed at zero differing pixels** (the projector speaks crop cameras
and provably changed nothing), the Director chose view 4's true-nape artifact,
the membrane word had its one measured iteration and **falsified itself
against its own pre-registered band** (`leathery` improved opacity while
naming a warm material — a single term cannot deliver opaque-and-cool), warm
membranes were accepted, and his "not very consistent" call — made, it turned
out, on the set's two measured tonal extremes, 7.8 L\* apart — ruled in the
**harmonization pass**: an identity-tested, operands-recorded Lab transfer
toward one reference view, now adopted as projection's input. Stage 1 then ran and was
ruled ([Ruling 24](experiments/E12-ruling.md)): **A0 stands at 87.5% of the
50.46% ceiling**; the E13 crop pass was not adopted (its paint drifts register at
bust frames — third measured instance) while its *capability* is banked permanently
(crop-camera projection proven at zero changed pixels, plus two latent projector
defects found by reading the tool before running it). The stroke lane is ruled
([Ruling 25](experiments/E12-ruling.md)): `thin_extent` 0.005 on the artifact
criterion — the arc's last deliberately-undecided value — elevated cameras closed
against their pre-registered falsifier, four strokes in spiral order, and the brush
gains its no-LoRA path anchored byte-identical on the accepted route's graphs. The
registry then caught the advisor clearing a block *in prose* — **a ruling that
decides values pays for them in registry entries** ([Ruling 26](experiments/E12-ruling.md))
— and the strokes are released toward **Gate 1 at the exemplar bar**.
Every value the subject needs lives in
`profiles/beast.json` and `canon/DRAGON-IDENTITY.md`, and the ones that arrived by
inheritance are being falsified and replaced one measured step at a time — which is
the profile system doing its job.

**GATE 1: ACCEPTED — the dragon is the route's THIRD accepted asset** (2026-08-07,
"Fantastic!! This is really good!", ruled on the GLB at the Director's own zoom —
[Ruling 28](experiments/E12-ruling.md)). The run to the gate: the sweep's
0-UNDECIDED certificate (83/83, the gate armed since handoff 2), four no-LoRA
strokes committing 99,643 texels at zero re-rolls, finalize sourcing a median
**0.92 triangle edges** with zero mean-fallback texels, pack to `dragon_hero.glb`
— **zero credits across the entire arc**. Mix **44.15% reference / 3.07% brush /
52.78% dilation of valid = 87.49 / 2.86 / 9.65 of the reachable set**: the animal
hides 49.54% of itself from every eye-level camera, so of the surface a viewer
can actually see, 87.49% is the accepted pair's own paint. The run also named the
**fifth brush signature** (dark desaturated crevice fill — 2.39× the near-black
at 0.44× the chroma of the paint it continues), measured, shown, and
pre-registered for every future brush run; the per-subject head-rect allocation
arm stays specced at the Director's timing. Next: the dense export (handoff 16 —
dataset asset #3, the first manifest under the lane's 1.3.0 contract), the
ingest, then the [E15 context index](experiments/E15-context-index-kickoff.md),
then E14.

**GATE 1: ACCEPTED — the longsword is the route's FOURTH accepted asset**
(2026-08-08, "Fantastic! I accept", ruled on `longsword_hero.glb` at the
Director's own zoom — [Ruling 32](experiments/E14-ruling.md)): the fourth
subject class at **zero credits across the entire arc**, the identity held at
five fixture elements, and the drifted stone returned to garnet by arithmetic
rather than regeneration. **The E14 arc, designation to acceptance:**
([E14-ruling.md](experiments/E14-ruling.md), Rulings 1–35, zero credits
across the whole arc — *the range read "1–23" here until the claims sweep caught it,
written before Rulings 24–35 landed in this same paragraph*): the route's fourth subject class and its **first portrait
subject** (widest-horizontal/height 0.2258 — the framing family pins HEIGHT here,
per subject, where the beast pinned width). Gate 0 reconstructed all three
longsword clays with the **cleanest topology the route has recorded** and produced
a route-wide headline: **every reconstruction this route has made is a hollow
double-walled shell**, walls ~two voxels ([Ruling 3](experiments/E14-ruling.md);
CLAUDE.md carries it). **Designated: 00001; register ruled day one** ("Ultra-realistic,
no LoRA"); the fixture ([LONGSWORD-IDENTITY.md](../canon/LONGSWORD-IDENTITY.md))
authored under the register with the occupancy audit at birth. The measurement pass
derived the canny pair per subject (0.10/0.25 — the accepted route's 0.4/0.8
falsified a second time on grey-on-grey clay) and the backdrop word (`plain
lavender background`, which materialises in the **magenta** band doing its job
8–11× over the key's cut — the word stands, its grounds corrected in place), and
**broke the off-surface "bake constant"**: the rate is a margin statistic tracking
island count (the fourth subject measured 11.09% at 46,496 islands; eroding 2 texels
drops all three prior subjects' rates 6–1300×). **The styled target pair is
ACCEPTED** ("I agree with view 0 being the best. I love it.") with one roll rejected
against the pre-registered occupancy audit — the specification working. The twin set
taught the hard lessons: **at one seed every diagonal sprawled gold and at the
cure-seed the gem drifts magenta** ("the seed buys an iron crossguard and costs a
garnet gem"); **edge-on twinning of a thin subject FAILS as a class** (zero
identity-clean rolls in four — a face-on crossguard grown from the mid-grip ring's
edge line, a death's-head where the guard should be: **a control can be obeyed and
still recompose the object when its features resemble the wrong parts**); and
**registration measures where paint sits, not what it is** (a rejected phantom
out-scored an accepted twin on IoU; the bbox law separates cleanly — no IoU bound
armed). **Stage 1b is the banked A0**: six twins, styled **45.25% of valid = 88.71%
of its pre-registered six-camera ceiling** (the dragon banked 87.5% of its own),
identity clean at the sheet-walk. Two price laws came out of the exclusions: **a
marginal is a property of an ordering, not of a camera** (a carried price overstated
43.8×), and **a reach price is not a paint price** (7.4× apart on the thin subject —
erosion and trust bind where the subject is thin). **The gem is GARNET at the
Director's one-word ruling** — the fixture holds, the artifact bends to the
identity — and **the stroke lane is RULED at HALT 1**
([Ruling 24](experiments/E14-ruling.md)): handoff 7's derivation ran the
write-head against itself (46 probes, 46 invariance-ANDON passes) and measured
the lane's honest denominator — **the achievable set is 69,239 texels = 1.891
points against the banked 210,907-texel territory**, the price law's third
instance (a territory is a reach number; an achievable set is a write-head
number; the blade closes 14.9% of its territory by design, the rim assigned to
finalize dilation from the strokes' own paint). The ruling: **eight strokes,
one per camera, hole-fill and the garnet repaint merged** (the demotion — a
recorded state operation with a named compensator — makes the drifted stone
ordinary holes; A32 untouched), spiral order with the two edge-on hazard
strokes last, `thin_extent` **decided at 0.0** (the 10d inversion is total —
the strokes the guard would protect are the ones it disarms), stroke stems
strengthening the gem's term to *deep red garnet* against the violet context
(the fixture's word unchanged). Stroke 1 then misbound twice — **both seeds
recomposed the faceted stone as a cabochon-in-a-bezel** (Ruling 20b's class
at a second structure: the stone's bright-rimmed kite resembles a
jewel-in-a-setting template; the term itself landed deep red at 770700 and
the drift's seed-dependence reproduced at the brush) — and
[Ruling 25](experiments/E14-ruling.md) took the stone OFF the
generation path: **the garnet re-projection** (hue/chroma transfer of the
four drifted twins' stone regions toward the identity's stone, L preserved,
re-projected into the demoted territory — the twins' own committed texels,
100% by construction, zero generation), the misbind made impossible rather
than watched. **The re-projection ran pixel-gate-clean and the stone is
garnet** (hue 308.6 → 22.5, the 305°-apart ownership partition now 6.6°, L
preserved to 0.088 per texel); one mask-boundary defect (1,436 collar-gold
texels rotated green) was located to the texel and restored from the
pre-stroke state under an asserted count. **All eight strokes then
committed** — 75,890 texels at zero credits, zero re-rolls, both edge-on
strokes clean on the 20b misbind watch at 4× against the clay — and the
probe's "achievable set" was falsified as a bound by its own pre-registered
falsifier: the lane committed **109.6%** of it, because each stroke's commit
enlarges the next stroke's keyed context (**a static probe of a sequential
process is a snapshot, not a bound** — Ruling 29f). The asset stands at
**47.32% styled of valid** with the stone and repair untouched by any
stroke; HALT 2 was accepted ("I love it"). **Finalize and pack then ran the
lane's tail** ([Ruling 31](experiments/E14-ruling.md)): surface-aware
dilation closed the remaining 1,929,166 texels at a median source distance
of 2.04 triangle edges — **the same absolute distance as the dragon's 0.92**,
because on a `1024_cascade` mesh the median edge IS the voxel pitch and this
mesh's triangles are 2.35× smaller (a dilation distance is quoted in both
units or the ratio misleads); the byte-level replay reproduced the atlas
exactly; the mean-fallback "zero" three subjects quoted was found to be
STRUCTURAL in surface-aware mode (a check that cannot fail is not a check —
the distance distribution is that mode's real gate, and it passed). Final mix
**45.25% reference / 2.07% brush / 52.68% dilation of valid** — and of the
surface a viewer actually sees, **88.71% is the accepted pair's own paint**.
The Director accepted the finished sword at his own zoom. **The dense export
ran the same day** ([Ruling 33](experiments/E14-ruling.md)): 26 cameras,
a six-class provenance palette (the garnet re-projection and collar repair as
their own classes — a route first), the manifest's tone transform declared as
a masked hue rotation with every operand sourced, **zero gap notices from the
sdlab lane's validator on the first run** — and **INGESTED the same day**
([Ruling 34](experiments/E14-ruling.md)): the live run reproduced the
dry run line for line, the operands materialized byte-identical, five
sha-pinned pointers went live, and the lane pushed to main at the Director's
word. **The dataset holds four dense assets** — the galleon, the dragon, the
longsword, and W3 — 114 records across five ingests. The errand batch (E16)
and the MCP-tool specs are in flight — and **the road ahead is chartered**
([Ruling 35](experiments/E14-ruling.md)): after the four MCP tools are
built and test-verified, **the polish arc** runs every accepted exemplar
through a polish pass that dogfoods the new tools, polishes the pipeline,
re-informs the dataset, re-makes the humanoid photo-real without the
saltroad LoRA, and opens the sword's activated state (Ruling 16c — its
sentence has arrived).

**E15 — the context index — is LIVE and ruled**
([E15-ruling.md](experiments/E15-ruling.md), 9 rulings):
`tools/facet_index.py` (build / verify / q / claims) generates
`docs/index/facet.db` — SQLite + FTS5 over the whole record, **ruling documents
discovered by sorted glob with an inverse guard**, verified on four legs
(byte-identical determinism across interpreters, counts against independent greps,
zero dangling pointers over 1,200+ rows, a seeded question gate — 20 questions as
of E14, every new seed measured before it enters) at **two
seats' hands**. The E14 arc proved the gate both ways in one night: its count legs
caught the advisor's own malformed fold hours after being added — and the commit
walked past the firing because verify and commit shared a shell call, minting the
standing practice that **a fold's verify and its commit never share a call**. The verifier found E04's true ruling count (29, where the prose
said 28 at three sites) by counting the record itself, and its own two self-caught
defects minted a law: **a status is read from a convention's position, never
matched in narrative prose**. The standing ritual: every advisor fold ends
`build` + `verify`; the DB commits at session boundaries; kickoffs carry one build
line after `git pull`. A session queries instead of reading — forty lines instead
of six hundred.
