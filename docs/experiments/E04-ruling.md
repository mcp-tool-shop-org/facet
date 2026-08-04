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
