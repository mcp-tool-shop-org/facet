# E53 — ruling: the compound-occupant generation is not justified on the kilt

**Advisor, 2026-08-17.** This rules on item 1 of `docs/advisor-kickoff.md:60-67`, which
ranked a compound occupant on the kilt as *"the first thing worth a generation."*

**Ruling: do not spend on it. The claim it rests on is falsified by this repo's own
record, and the falsification is written in the same experiment series the claim cites.**

---

## The claim, as the kickoff states it

> N9 *green cloth panels in the kilt* is recorded as a blocked addition **that dropped**,
> and the panels are plainly in the reference. […] **Only a generation settles it.**

## What the record measures

Read complete, in context, at each locator.

**1. N9 arrives without being prompted.** Amendment 16, `docs/experiments/E08-ruling-gate0.md:1071-1073`:

> 14–15 of the 16 NAMED elements already arrive **unprompted** — the belt medallion, the
> **green skirt panels**, the ornate crossguard and the gold pommel are all present in an
> image whose prompt named none of them.

Confirmed against the generation prompt itself. `docs/experiments/E08-cloud-build-order.md:76`
is the prompt that made the shipped twins, and it contains no panel phrase at all.

**2. N9 obeys the prompt when it is named.** `docs/experiments/E08-contradiction-report.md:81`:

> **N9 skirt panels, green → grey: ΔE 47.41, C\* 40.3 → 9.1.** It responded, right alongside
> the contra class.

The contradiction arm's prompt (`docs/experiments/E08-spec-prompt.json`) names N9 as its own
noun phrase — `green cloth panels in the skirt` — beside N8's `a dark red layered cloth
skirt`. **That is the co-located form, specified from scratch, and it landed.**

**3. N9 was never measured as a drop.** Amendment 15's table
(`docs/experiments/E08-ruling-gate0.md:1013-1017`) has four rows: gold knee plates,
brown leather bracers, gold trim on the bracer, a gold plate on each outer forearm.
**N9 is not among them.** The canon file agrees with itself here and the kickoff does
not — `canon/w3.surfaces.json` records N9's reason as
`"co-location; predicted to drop (Amendment 15)"`, against N11's
`"measured drop, median dE 1.07"`. **Predicted, not measured**, and the prediction was
retracted before the run and then contradicted by it:

> Contradicting something already present is **replacement, not addition**. N9 responded at
> ΔE 47.41 alongside the contra class; my original "N5/N9/N11 predicted to drop" would have
> been wrong. — `docs/experiments/E08-ruling-gate0.md:1376-1378`

**4. The 1.07 no-response is a measurement of PATCHING, not of co-location in a spec.**
`docs/experiments/E08-ruling-gate0.md:1031-1036`:

> **N11 failed because we were patching, and a new sprite is not patched.** Retrofitting a
> gold plate onto a fur cuff that the model has already committed is a different operation
> from specifying a character from scratch […] the failure mode is specific to retrofit.

And `E08-spec-prompt.json`'s own `_purpose` field says the same thing in the artifact:
*"Nothing is added to anything: the character is specified from scratch […] rather than
patched, which is what N11 was."*

## Why the spend fails on its own terms

The panels are already in the image, and they already track the prompt. So a compound
occupant on the kilt reads **the same picture whether it works or does nothing** — the
arm's *definitely-yes* state and its *definitely-does-nothing* state are indistinguishable.

That is this repo's own law, written three arcs ago and applied here to a proposed arm
rather than to a finished one:

> Compute what your instrument reads when the thing is definitely true, and when it is
> definitely false, and predict inside that interval.

> Before adopting a metric for an arm, ask what value it takes when the arm does nothing
> and when it works perfectly — if those are the same number, it is not measuring the arm.

**The kilt has no headroom.** Amendment 16 named the element that does: *"the honest unit
is: of the elements that were absent, how many arrived? — and that denominator is one,
possibly two."* The one is **N11**.

## What is actually open — and the first step is free

**The unanswered number is whether N11 landed in the from-scratch SPEC arm.** It is named
in `E08-spec-prompt.json`. It is absent from the baseline
(`E08-contradiction-report.md:84-85`: *"N11's forearm plate does not arrive in the baseline
anyway, so there was nothing there to contradict"*). The pre-registration at
`E08-ruling-gate0.md:1051-1053` states the discriminator outright:

> **If N5 and N9 land while N11 drops, co-location is wrong too and something narrower is
> going on.**

N9 landed. **Whether N11 dropped under simultaneous from-scratch specification is not
reported anywhere in this record that I can find**, and it decides the whole question:

- **N11 landed in SPEC** → the blocked-addition class is a *patch* artifact. All three
  `blocked_additions` rows in `canon/w3.surfaces.json` are mis-classified, the schema
  repair is free, and no generation is needed at all.
- **N11 dropped in SPEC** → co-location survives from-scratch specification, and the
  forearm is the surface with real headroom. **That** is where a compound occupant is a
  well-posed question — and the Director has just ratified what the surface carries
  (Q1: the same glove and gold arm brace on both arms), so the compound phrase writes
  itself from his own naming rather than from an advisor's reading of a projection.

The SPEC arm's `prompt_id` is recorded (`E08-contradiction-report.md`, files section), so
this is an artifact lookup before it is anything else.

## What this ruling does not do

It does not touch Amendment 15, which stands on N11's patch measurement and on the
knee-plate / bracer replacements. It does not withdraw the co-location constraint. It does
not rule on N5, which has no measurement region either way. It does not edit
`canon/w3.surfaces.json` — the N9 row's `why` string is a *prediction* honestly labelled as
one, and repairing it is a canon change that rides with its own tests and the Director's
word, not a ruling's side effect.

## The advisor error this corrects, named

Two consecutive advisor seats read *"blocked addition"* in a canon row and carried it
forward as *"dropped"*, without opening the report the row cites. The row says
**predicted**. This is the same shape as the four reference readings the Director
overturned yesterday and as the three `enumerate the resource before commissioning one`
instances: **a claim inherited from our own document, asserted in the voice of a
measurement.**

The cost, had it run: one generation, on the one surface in the specification where the
answer was already on disk.

---

# E53 dispatch — did N11 land in the from-scratch SPEC arm?

**Dispatched 2026-08-17 by the advisor seat. Sonnet executor, background, open line.**
Zero spend. Everything this needs is on disk.

## The question, and why it is the only one left free

`E:\AI\training\facet_E08\SPEC\w3clay_0.png` is the from-scratch, sixteen-element arm. Its
prompt (`docs/experiments/E08-spec-prompt.json`) names N11 — `a gold plate on each outer
forearm` — as its own noun phrase. N11 is **absent from the unspecified baseline**
(`E08-contradiction-report.md:84-85`), which is what makes it the one element in the whole
specification with headroom (Amendment 16: *"that denominator is one, possibly two"*).

**Is the gold forearm plate present in that image or not?** The record does not say, and it
decides the co-location law's scope:

- **present** → the blocked-addition class is an artifact of *patching*. All three
  `blocked_additions` rows in `canon/w3.surfaces.json` are mis-classified, the repair is a
  schema edit, and no generation is needed anywhere.
- **absent** → co-location survives from-scratch specification. The **forearm**, not the
  kilt, is the surface with real headroom, and a compound occupant there becomes a
  well-posed question the Director's own ratified naming already supplies the phrase for.

## ⚠ The instrument that already failed here — read this before choosing one

`docs/experiments/E08-ruling-gate0.md:1059-1062`, verbatim:

> A gold-pixel count over the forearm crop caught the pauldron edge and read 5.6% / 5.1%
> against canon's 1.96% — **inverting the truth**, and it would have flattered the reading.
> It was reported as unusable rather than quoted.

**Do not re-derive that instrument.** Whatever you measure, first state what it reads on a
*definitely-yes* population and a *definitely-no* one, and show it does not admit the
pauldron. Two further traps this repo has already paid for and that apply directly:

- **Below a chroma floor, hue is not a colour.** Any hue number carries its chroma or it is
  not quoted. Gold sits at C\* 27–40, h 78–90 (`E08-contradiction-predictions.md`); brown
  leather and a gold plate are not separable by hue alone.
- **A global constant must not govern a local feature.** Derive any crop or tolerance from
  the forearm's own extent, not from figure width.

## What to do

1. **Enumerate before you build anything.** `E:\AI\training\facet_E08\` has `SPEC/`,
   `N11/`, `BRACER/`, `ARMOUR/`, `CONTRA/`, `ANCHOR/`, `ARMB/` and more. Read
   `SPEC\PREDICTIONS.md` and `CONTRA\PREDICTIONS.md` whole. Find the **unspecified
   baseline** image the record keeps referring to and name its path — do not assume which
   directory holds it. Three instances in this repo of commissioning something that already
   existed; check `tools/` for a crop/sheet/colour instrument before writing one.
2. **Establish the reference.** `canon\twin_front.png` and `canon\twin_back.png`. The
   Director ratified 2026-08-17 that the same brown leather glove and gold arm brace are on
   **both** arms, and that the front view shows the sword hand palm-on — which is why a
   previous advisor seat read it as bare flesh. **Open both files.** The back reference sat
   unopened through four wrong readings yesterday.
3. **The comparison, one row per arm:** reference | unspecified baseline | SPEC | (N11 patch
   arm, labelled as the patch operation, not one variable with SPEC). Forearm crop, derived
   from the forearm's own extent, **native pixels at the Director's zoom, defects first**.
4. **Report a measurement beside the crop**, with its yes/no calibration populations and its
   demonstrated non-admission of the pauldron. If no honest instrument exists here, **say
   so and ship the crop alone** — refusing to commission a metric where no honest one exists
   is a recorded advisor virtue in this repo and it is available to you too.

## Gates — halt and report

- **Gate A — the arms are what the record says they are.** Confirm from
  `E08-spec-prompt.json` that the SPEC prompt names N11, and confirm the image you crop is
  the output of that prompt (`SPEC\w3clay_0.png` plus whatever provenance that tree carries).
  If you cannot establish the image-to-prompt link, **halt** and report what is missing.
- **Gate B — the instrument does not admit the pauldron.** If your candidate measurement
  fires on the pauldron edge, **halt on the instrument**, report it as unusable, and fall
  back to the crop alone. Do not tune it.
- **Gate C — read every listing complete.** No `head`/`tail`/`Select-Object -Last` on
  anything that decides a number.
- **Gate D — no write outside `E:\AI\training\facet_E53\`.** All other `facet_E*` trees are
  read-only. Do not read `facet_E50`, `facet_E51`, `facet_E52` working trees.

## Predictions

Write `predictions.md` before you look at the SPEC forearm. Predict **presence or absence**,
with a stated reason and what would falsify it, and disclose your blindness honestly — you
will have read this document, which argues both branches on purpose so neither is the
obvious answer.

## Bounds

Zero spend, no GPU, no cloud. Do not commit; leave the change-set uncommitted. Do not write
to any memory store. Do not judge whether the output is good — **especially here**: whether
the plate is present is a measurement, whether the asset is right is the Director's. Gates
`raise`; tests ride any tool change; next free test file is **t93** (E52's seat did not take
t92, so it is free, but check before claiming it). A negative result is a full success.

Report to `docs/experiments/E53-n11-spec-arm-report.md`.
